# Build step (data stage of the Dockerfile): turn the four public data sets into simple CSV files.
#   Rscript prepare_data.R data_sources.tsv OUTDIR
# Each data set gets a folder OUTDIR/<name>/ with
#   counts.csv   gene_id + one column of read counts per sample
#   samples.csv  one row per sample; the order of first appearance sets the order of the groups
#   genes.csv    gene_id, symbol, description
suppressPackageStartupMessages({
    library(AnnotationDbi)
})

args <- commandArgs(trailingOnly = TRUE)
sources <- read.delim(args[1], stringsAsFactors = FALSE)
out_dir <- args[2]
download_dir <- tempfile("downloads")
dir.create(download_dir)

# Download one file from data_sources.tsv and stop if its checksum differs.
fetch <- function(file) {
    row <- sources[sources$file == file, ]
    dest <- file.path(download_dir, file)
    if (file.exists(dest)) return(dest)  # already downloaded and checked
    # The GDC server sometimes drops a connection; try up to three times.
    for (attempt in 1:3) {
        ok <- tryCatch(download.file(row$url, dest, mode = "wb", quiet = TRUE) == 0, error = function(e) FALSE)
        if (ok) break
        if (attempt == 3) stop("could not download ", row$url)
        Sys.sleep(5)
    }
    algo <- sub(":.*", "", row$checksum)
    expected <- sub(".*:", "", row$checksum)
    actual <- switch(algo,
        md5 = unname(tools::md5sum(dest)),
        sha256 = sub(" .*", "", system2("sha256sum", dest, stdout = TRUE)))
    if (!identical(actual, expected)) stop("checksum mismatch for ", file)
    dest
}

# Gene annotation packages (gene symbols and names), installed for this script only.
annotation_lib <- tempfile("annotation")
dir.create(annotation_lib)
for (file in sources$file[sources$dataset == "annotation"])
    install.packages(fetch(file), lib = annotation_lib, repos = NULL, type = "source", quiet = TRUE)
.libPaths(c(annotation_lib, .libPaths()))

# First symbol/description per ID; IDs without one keep the ID as symbol.
annotate <- function(db, ids, keytype) {
    symbol <- mapIds(db, ids, "SYMBOL", keytype, multiVals = "first")
    description <- mapIds(db, ids, "GENENAME", keytype, multiVals = "first")
    symbol[is.na(symbol)] <- ids[is.na(symbol)]
    description[is.na(description)] <- ""
    data.frame(gene_id = ids, symbol = unname(symbol), description = unname(description))
}

# Path of one file inside a downloaded Bioconductor package tarball.
from_tarball <- function(file, path) {
    dir <- file.path(download_dir, sub("\\.tar\\.gz$", "", file))
    untar(fetch(file), files = path, exdir = dir)
    file.path(dir, path)
}

write_dataset <- function(name, counts, samples, genes) {
    stopifnot(identical(colnames(counts), samples$sample),
              identical(rownames(counts), genes$gene_id),
              !anyDuplicated(genes$gene_id))
    dir <- file.path(out_dir, name)
    dir.create(dir, recursive = TRUE)
    storage.mode(counts) <- "integer"
    write.csv(data.frame(gene_id = rownames(counts), counts, check.names = FALSE),
              file.path(dir, "counts.csv"), row.names = FALSE, quote = FALSE)
    write.csv(samples, file.path(dir, "samples.csv"), row.names = FALSE)
    write.csv(genes, file.path(dir, "genes.csv"), row.names = FALSE)
    message(sprintf("%-8s %6d genes x %2d samples", name, nrow(counts), ncol(counts)))
}

# --- milk: mouse mammary gland, GSE60450 (Fu et al. 2015) --------------------------------
# Sample names MCL1-D* are basal cells, MCL1-L* luminal cells; the second letter gives the state.
x <- read.delim(fetch("GSE60450_Lactation-GenewiseCounts.txt.gz"), check.names = FALSE)
counts <- as.matrix(x[, -(1:2)])
colnames(counts) <- substr(colnames(counts), 1, 7)
rownames(counts) <- as.character(x$EntrezGeneID)
state_of <- c(G = "virgin", H = "virgin", I = "pregnant", J = "pregnant", K = "lactating", L = "lactating",
              A = "virgin", B = "virgin", C = "pregnant", D = "pregnant", E = "lactating", F = "lactating")
samples <- data.frame(
    sample = colnames(counts),
    celltype = ifelse(substr(colnames(counts), 6, 6) == "D", "basal", "luminal"),
    state = unname(state_of[substr(colnames(counts), 7, 7)]))
# Order: virgin, pregnant, lactating within each cell type (already so in the file).
write_dataset("milk", counts, samples, annotate(org.Mm.eg.db::org.Mm.eg.db, rownames(counts), "ENTREZID"))

# --- airway: human airway smooth muscle cells + dexamethasone (Himes et al. 2014) --------
suppressPackageStartupMessages(library(SummarizedExperiment))
load(from_tarball("airway_1.30.0.tar.gz", "airway/data/airway.RData"))
counts <- assay(airway)
cd <- colData(airway)
samples <- data.frame(
    sample = colnames(counts),
    donor = as.character(cd$cell),
    treatment = ifelse(cd$dex == "trt", "dex", "untreated"))
ord <- order(samples$treatment != "untreated", samples$donor)
counts <- counts[, ord]
samples <- samples[ord, ]
genes <- annotate(org.Hs.eg.db::org.Hs.eg.db, rownames(counts), "ENSEMBL")
# Keep genes with a known name: the rest are mostly unnamed non-coding RNAs that are never expressed.
keep <- genes$symbol != genes$gene_id
write_dataset("airway", counts[keep, ], samples, genes[keep, ])

# --- pasilla: fruit fly cells, pasilla knock-down (Brooks et al. 2011) -------------------
counts <- as.matrix(read.delim(from_tarball("pasilla_1.38.0.tar.gz", "pasilla/inst/extdata/pasilla_gene_counts.tsv"),
                               row.names = 1))
ann <- read.csv(from_tarball("pasilla_1.38.0.tar.gz", "pasilla/inst/extdata/pasilla_sample_annotation.csv"))
ann$sample <- sub("fb$", "", ann$file)
ann <- ann[order(ann$condition != "untreated", ann$sample), ]
counts <- counts[, ann$sample]
samples <- data.frame(
    sample = ann$sample,
    condition = ifelse(ann$condition == "treated", "knockdown", "control"),
    library = ifelse(ann$type == "paired-end", "paired_end", "single_end"))
write_dataset("pasilla", counts, samples, annotate(org.Dm.eg.db::org.Dm.eg.db, rownames(counts), "FLYBASE"))

# --- cancer: TCGA breast cancer, tumour and normal tissue of the same 10 patients --------
files <- sources$file[sources$dataset == "cancer"]
tables <- lapply(files, function(f) {
    t <- read.delim(fetch(f), comment.char = "#")
    t[t$gene_type == "protein_coding" & !grepl("_PAR_Y$", t$gene_id), ]
})
counts <- sapply(tables, `[[`, "unstranded")
gene_ids <- sub("\\..*", "", tables[[1]]$gene_id)
stopifnot(all(sapply(tables, function(t) identical(sub("\\..*", "", t$gene_id), gene_ids))))
rownames(counts) <- gene_ids
# Patient IDs with _ instead of -, so they are valid names in makeContrasts().
case <- gsub("-", "_", sub("^TCGA-(.*)_(tumour|normal)\\.tsv$", "\\1", files))
tissue <- sub(".*_(tumour|normal)\\.tsv$", "\\1", files)
samples <- data.frame(sample = paste0(case, "_", tissue), patient = case, tissue = tissue)
colnames(counts) <- samples$sample
ord <- order(samples$tissue != "normal", samples$patient)
counts <- counts[, ord]
samples <- samples[ord, ]
description <- mapIds(org.Hs.eg.db::org.Hs.eg.db, gene_ids, "GENENAME", "ENSEMBL", multiVals = "first")
genes <- data.frame(gene_id = gene_ids, symbol = tables[[1]]$gene_name,
                    description = ifelse(is.na(description), "", unname(description)))
write_dataset("cancer", counts, samples, genes)
