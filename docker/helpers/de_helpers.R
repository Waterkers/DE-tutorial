# Helper functions for the DE practical. Rprofile.site loads them into every R session.
# They only load data, draw plots and make tables easier to read; the analysis itself
# (edgeR and limma functions) stays in the notebooks.

.de_messages <- list(
    en = list(
        loaded = "Loaded data set '%s': %d genes, %d samples.",
        unknown_dataset = "There is no data set '%s'. Choose one of: %s",
        unknown_column = "The sample table has no column '%s'. Columns: %s",
        not_found = "Gene '%s' is not in the data (maybe it was filtered out because it is hardly expressed).",
        million_reads = "million reads",
        library_sizes = "Library sizes: reads per sample",
        log_cpm = "log2(counts per million)",
        distributions = "Expression of all genes per sample",
        mds = "Sample map (MDS): similar samples are close together",
        dim = "Distance %d (%d %%)",
        up = "up", down = "down", not_sig = "not significant",
        volcano_x = "log2 fold change (left: lower, right: higher)",
        volcano_y = "-log10(p-value) (higher = more certain)",
        times_up = "%.1f× higher", times_down = "%.1f× lower",
        language = "Language: English"
    ),
    de = list(
        loaded = "Datensatz '%s' geladen: %d Gene, %d Proben.",
        unknown_dataset = "Es gibt keinen Datensatz '%s'. Wähle einen von: %s",
        unknown_column = "Die Probentabelle hat keine Spalte '%s'. Spalten: %s",
        not_found = "Das Gen '%s' ist nicht in den Daten (vielleicht wurde es herausgefiltert, weil es kaum exprimiert ist).",
        million_reads = "Millionen Reads",
        library_sizes = "Bibliotheksgröße: Reads pro Probe",
        log_cpm = "log2(Counts pro Million)",
        distributions = "Expression aller Gene pro Probe",
        mds = "Probenkarte (MDS): ähnliche Proben liegen nah beieinander",
        dim = "Richtung %d (%d %%)",
        up = "hoch", down = "runter", not_sig = "nicht signifikant",
        volcano_x = "log2 Fold Change (links: niedriger, rechts: höher)",
        volcano_y = "-log10(p-Wert) (höher = sicherer)",
        times_up = "%.1f× höher", times_down = "%.1f× niedriger",
        language = "Sprache: Deutsch"
    )
)

.de_data_dir <- "/opt/data"
# Okabe-Ito colours: distinguishable with colour vision deficiency.
.de_colours <- c("#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00", "#F0E442", "#000000")

.tr <- function(key, ...) {
    lang <- getOption("de_practical.lang", "en")
    sprintf(.de_messages[[lang]][[key]], ...)
}

# Colours and legend for a sample column (or NULL: all the same colour).
.de_groups <- function(dge, column) {
    if (is.null(column)) return(list(col = .de_colours[1], legend = NULL))
    if (!column %in% colnames(dge$samples))
        stop(.tr("unknown_column", column, paste(colnames(dge$samples), collapse = ", ")), call. = FALSE)
    f <- factor(dge$samples[[column]])
    cols <- rep_len(.de_colours, nlevels(f))
    list(col = cols[as.integer(f)], legend = levels(f), legend_col = cols)
}

# Plot margins: room for sample names below and, with groups, a legend on the right.
.de_margins <- function(g, bottom) {
    par(mar = c(bottom, 5, 3, if (is.null(g$legend)) 1 else 2 + max(nchar(g$legend)) * 0.6))
}
.de_legend <- function(g, ...) {
    if (!is.null(g$legend))
        legend(par("usr")[2], par("usr")[4], g$legend, xpd = TRUE, bty = "n", inset = 0.01, ...)
}

#' setLanguage("en") or setLanguage("de"): language of messages and plot labels.
setLanguage <- function(lang) {
    lang <- match.arg(lang, names(.de_messages))
    options(de_practical.lang = lang)
    message(.tr("language"))
    invisible(lang)
}

#' data <- loadDataset("milk"): list with counts (matrix), samples and genes (tables).
#' Data sets: milk, airway, pasilla, cancer.
loadDataset <- function(name) {
    available <- list.dirs(.de_data_dir, full.names = FALSE, recursive = FALSE)
    if (!name %in% available)
        stop(.tr("unknown_dataset", name, paste(available, collapse = ", ")), call. = FALSE)
    dir <- file.path(.de_data_dir, name)
    counts <- read.csv(file.path(dir, "counts.csv"), row.names = 1, check.names = FALSE)
    samples <- read.csv(file.path(dir, "samples.csv"), stringsAsFactors = FALSE)
    genes <- read.csv(file.path(dir, "genes.csv"), stringsAsFactors = FALSE)
    rownames(samples) <- samples$sample
    rownames(genes) <- genes$gene_id
    # Groups in the order they appear in the table (e.g. control before treatment).
    for (column in setdiff(colnames(samples), "sample"))
        samples[[column]] <- factor(samples[[column]], levels = unique(samples[[column]]))
    message(.tr("loaded", name, nrow(counts), ncol(counts)))
    list(counts = as.matrix(counts), samples = samples, genes = genes)
}

#' plotLibrarySizes(dge, colour_by = "celltype"): bar chart of the number of reads per sample.
plotLibrarySizes <- function(dge, colour_by = NULL) {
    g <- .de_groups(dge, colour_by)
    old <- .de_margins(g, 8); on.exit(par(old))
    barplot(dge$samples$lib.size / 1e6, names.arg = colnames(dge), las = 2, col = g$col, border = NA,
            ylab = .tr("million_reads"), main = .tr("library_sizes"))
    .de_legend(g, fill = g$legend_col, border = NA)
}

#' plotDistributions(dge, colour_by = "state"): box plot of all genes' expression in each sample.
#' Uses the normalisation factors, so it shows the effect of normLibSizes().
plotDistributions <- function(dge, colour_by = NULL, title = .tr("distributions")) {
    g <- .de_groups(dge, colour_by)
    old <- .de_margins(g, 8); on.exit(par(old))
    log_cpm <- edgeR::cpm(dge, log = TRUE)
    boxplot(log_cpm, las = 2, col = g$col, outline = FALSE, ylab = .tr("log_cpm"), main = title)
    abline(h = median(log_cpm), lty = 2, col = "grey40")
    .de_legend(g, fill = g$legend_col, border = NA)
}

#' plotSamples(dge, colour_by = "celltype", label_by = "state"): MDS sample map.
plotSamples <- function(dge, colour_by = NULL, label_by = NULL) {
    g <- .de_groups(dge, colour_by)
    .de_groups(dge, label_by)  # checks that the column exists
    labels <- if (is.null(label_by)) colnames(dge) else as.character(dge$samples[[label_by]])
    mds <- limma::plotMDS(dge, plot = FALSE)
    pct <- round(100 * mds$var.explained[1:2])
    x <- mds$x; y <- mds$y
    pad_x <- diff(range(x)) * 0.12; pad_y <- diff(range(y)) * 0.08
    old <- .de_margins(g, 5); on.exit(par(old))
    plot(x, y, type = "n", xlim = range(x) + c(-pad_x, pad_x), ylim = range(y) + c(-pad_y, pad_y),
         xlab = .tr("dim", 1L, pct[1]), ylab = .tr("dim", 2L, pct[2]), main = .tr("mds"))
    text(x, y, labels, col = g$col, font = 2)
    .de_legend(g, text.col = g$legend_col)
}

#' plotGene(dge, "Csn2", group_by = "state"): expression of one gene in every sample.
plotGene <- function(dge, gene, group_by) {
    idx <- which(toupper(dge$genes$symbol) == toupper(gene))[1]
    if (is.na(idx)) {
        message(.tr("not_found", gene))
        return(invisible(NULL))
    }
    g <- .de_groups(dge, group_by)
    values <- edgeR::cpm(dge, log = TRUE)[idx, ]
    groups <- factor(dge$samples[[group_by]])
    old <- par(mar = c(3 + 0.55 * max(nchar(levels(groups))), 5, 3, 1)); on.exit(par(old))
    stripchart(values ~ groups, vertical = TRUE, method = "jitter", jitter = 0.08, pch = 19, cex = 1.6,
               col = g$legend_col, las = 2, xlab = "", ylab = .tr("log_cpm"),
               main = paste0(dge$genes$symbol[idx], ": ", dge$genes$description[idx]))
    means <- tapply(values, groups, mean)
    segments(seq_along(means) - 0.25, means, seq_along(means) + 0.25, means, lwd = 2, col = "grey30")
}

#' showTop(fit, "lactating_vs_pregnant", n = 10, direction = "up"): table of the top genes.
#' direction: "both" (default), "up" or "down".
showTop <- function(fit, coef, n = 10, direction = c("both", "up", "down")) {
    direction <- match.arg(direction)
    tt <- limma::topTable(fit, coef = coef, number = Inf, sort.by = "P")
    if (direction == "up") tt <- tt[tt$logFC > 0, ]
    if (direction == "down") tt <- tt[tt$logFC < 0, ]
    tt <- head(tt, n)
    change <- ifelse(tt$logFC > 0, .tr("times_up", 2^tt$logFC), .tr("times_down", 2^-tt$logFC))
    description <- ifelse(nchar(tt$description) > 45, paste0(substr(tt$description, 1, 43), "…"), tt$description)
    data.frame(symbol = tt$symbol, description = description, logFC = round(tt$logFC, 2), change = change,
               AveExpr = round(tt$AveExpr, 1), adj.P.Val = signif(tt$adj.P.Val, 2), row.names = NULL)
}

#' plotVolcano(fit, "lactating_vs_pregnant"): every gene as a dot, top genes named.
#' Coloured: adjusted p-value < p and at least 2^lfc-fold change.
plotVolcano <- function(fit, coef, n_labels = 10, lfc = 1, p = 0.05) {
    tt <- limma::topTable(fit, coef = coef, number = Inf, sort.by = "P")
    y <- -log10(tt$P.Value)
    status <- ifelse(tt$adj.P.Val < p & tt$logFC > lfc, "up",
                     ifelse(tt$adj.P.Val < p & tt$logFC < -lfc, "down", "not_sig"))
    col <- c(up = "#D55E00", down = "#0072B2", not_sig = "grey75")[status]
    plot(tt$logFC, y, pch = 20, cex = 0.6, col = col, xlab = .tr("volcano_x"), ylab = .tr("volcano_y"),
         main = coef)
    abline(v = c(-lfc, lfc), lty = 2, col = "grey50")
    top <- head(seq_len(nrow(tt)), n_labels)
    text(tt$logFC[top], y[top], tt$symbol[top], pos = ifelse(tt$logFC[top] > 0, 4, 2), cex = 0.8, xpd = TRUE)
    counts <- table(factor(status, levels = c("up", "down", "not_sig")))
    legend("topleft", sprintf("%s: %d", c(.tr("up"), .tr("down"), .tr("not_sig")), counts),
           col = c("#D55E00", "#0072B2", "grey75"), pch = 19, bg = "white", inset = 0.01, cex = 0.9)
}
