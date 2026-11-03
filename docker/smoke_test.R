# Build check: run the analysis of every data set the way the solutions do, and stop
# if the known results don't come out. Run by the Dockerfile; also useful after updates.
check <- function(ok, what) {
    if (!isTRUE(ok)) stop("smoke test failed: ", what, call. = FALSE)
    message("ok   ", what)
}

# Standard pipeline: DGEList -> filter -> TMM -> voom -> lmFit -> contrasts -> eBayes.
analyse <- function(name, group, design_formula, contrast) {
    data <- suppressMessages(loadDataset(name))
    dge <- DGEList(counts = data$counts, samples = data$samples, genes = data$genes)
    keep <- filterByExpr(dge, group = dge$samples[[group]])
    dge <- normLibSizes(dge[keep, , keep.lib.sizes = FALSE])
    design <- model.matrix(design_formula, data = dge$samples)
    contrasts <- makeContrasts(contrasts = contrast, levels = design)
    fit <- eBayes(contrasts.fit(lmFit(voom(dge, design), design), contrasts))
    list(dge = dge, fit = fit, top = topTable(fit, coef = 1, number = Inf))
}
up_in_top <- function(res, genes, n) all(genes %in% head(res$top$symbol[res$top$logFC > 0], n))
n_de <- function(res) sum(res$top$adj.P.Val < 0.05)

# milk: lactating vs pregnant luminal cells; milk protein genes go up.
data <- suppressMessages(loadDataset("milk"))
check(identical(dim(data$counts), c(27179L, 12L)), "milk: 27179 genes x 12 samples")
group <- paste(data$samples$celltype, data$samples$state, sep = "_")
dge <- DGEList(counts = data$counts, samples = data$samples, genes = data$genes)
dge$samples$group <- factor(group, levels = unique(group))
dge <- normLibSizes(dge[filterByExpr(dge), , keep.lib.sizes = FALSE])
design <- model.matrix(~0 + group, data = dge$samples)
colnames(design) <- levels(dge$samples$group)
contrasts <- makeContrasts(lactating_vs_pregnant = luminal_lactating - luminal_pregnant,
                           luminal_vs_basal = luminal_virgin - basal_virgin, levels = design)
fit <- eBayes(contrasts.fit(lmFit(voom(dge, design), design), contrasts))
milk <- list(top = topTable(fit, coef = "lactating_vs_pregnant", number = Inf))
check(nrow(dge) > 14000 && nrow(dge) < 17000, sprintf("milk: %d genes kept after filtering", nrow(dge)))
check(min(dge$samples$norm.factors[dge$samples$group == "luminal_lactating"]) < 0.7,
      "milk: TMM corrects lactating luminal samples (norm.factors < 0.7)")
check(all(c("Csn1s2b", "Wap", "Lalba") %in% milk$top$symbol[milk$top$adj.P.Val < 0.05 & milk$top$logFC > 0]),
      "milk: Csn1s2b, Wap, Lalba significantly up in lactating vs pregnant luminal cells")
check(n_de(milk) > 1000, sprintf("milk: %d DE genes (lactating vs pregnant)", n_de(milk)))
lb <- topTable(fit, coef = "luminal_vs_basal", number = Inf)
check(all(c("Krt8", "Krt18") %in% lb$symbol[lb$logFC > 2]) && all(c("Krt5", "Krt14") %in% lb$symbol[lb$logFC < -2]),
      "milk: luminal keratins Krt8/18 up, basal keratins Krt5/14 down")

# airway: dexamethasone vs untreated, paired by donor.
airway <- analyse("airway", "treatment", ~0 + treatment + donor, "treatmentdex - treatmentuntreated")
check(all(c("DUSP1", "KLF15", "PER1", "TSC22D3", "FKBP5", "ZBTB16") %in%
          airway$top$symbol[airway$top$adj.P.Val < 0.05 & airway$top$logFC > 1]),
      "airway: DUSP1, KLF15, PER1, TSC22D3, FKBP5, ZBTB16 up with dexamethasone")
unpaired <- analyse("airway", "treatment", ~0 + treatment, "treatmentdex - treatmentuntreated")
check(n_de(airway) > n_de(unpaired),
      sprintf("airway: donor in the design finds more DE genes (%d vs %d)", n_de(airway), n_de(unpaired)))

# pasilla: knock-down vs control, with library type in the design. pasilla's symbol is "ps".
pasilla <- analyse("pasilla", "condition", ~0 + condition + library, "conditionknockdown - conditioncontrol")
ps <- pasilla$top[pasilla$top$symbol == "ps", ]
check(ps$logFC < -1.5 && ps$adj.P.Val < 1e-3, sprintf("pasilla: ps strongly down (logFC %.1f, adj. p %.1g)", ps$logFC, ps$adj.P.Val))
check(n_de(pasilla) > 300, sprintf("pasilla: %d DE genes", n_de(pasilla)))

# cancer: tumour vs normal, paired by patient.
cancer <- analyse("cancer", "tissue", ~0 + tissue + patient, "tissuetumour - tissuenormal")
check(all(c("MKI67", "TOP2A") %in% cancer$top$symbol[cancer$top$adj.P.Val < 0.05 & cancer$top$logFC > 1]),
      "cancer: proliferation genes MKI67, TOP2A up in tumours")
check(all(c("ADIPOQ", "LEP") %in% cancer$top$symbol[cancer$top$adj.P.Val < 0.05 & cancer$top$logFC < -1]),
      "cancer: fat-tissue genes ADIPOQ, LEP down in tumours")

# Helpers draw without errors (to a null device).
pdf(NULL)
plotLibrarySizes(dge, colour_by = "celltype"); plotDistributions(dge, colour_by = "state")
plotSamples(dge, colour_by = "celltype", label_by = "state"); plotGene(dge, "Wap", group_by = "group")
plotVolcano(fit, "lactating_vs_pregnant"); invisible(showTop(fit, "lactating_vs_pregnant", direction = "up"))
invisible(dev.off())
setLanguage("de"); plotGene(dge, "nonexistent", group_by = "group")
check(TRUE, "helpers run")
