# Third-party software and data

This repository's own files are licensed under MIT and CC BY 4.0, see the License section of [README.md](README.md). It contains only its own files: scripts, R helper functions, notebooks and documentation. The software and data below are **not** included in the repository. They are downloaded when the Docker image is built, so they **are** included in every built image.

| Component | Version | Source | License |
|---|---|---|---|
| Mouse mammary gland counts (GSE60450) | GEO, 2014 | <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE60450> | NCBI GEO: no restrictions on use; please cite Fu et al. 2015 |
| `airway` data package | 1.30.0 | <https://bioconductor.org/packages/airway> | LGPL |
| `pasilla` data package | 1.38.0 | <https://bioconductor.org/packages/pasilla> | LGPL |
| TCGA-BRCA gene expression (STAR – Counts), 20 files | GDC Data Release 46 | <https://portal.gdc.cancer.gov>, file IDs in `docker/data_sources.tsv` | GDC open-access data; please cite TCGA (The Cancer Genome Atlas Network 2012) |
| org.Mm.eg.db, org.Hs.eg.db, org.Dm.eg.db (gene symbols and names; build stage only, copied into the CSV files) | 3.22.0 | <https://bioconductor.org> | Artistic-2.0; data from NCBI Gene and FlyBase |
| limma | 3.68.5 | <https://bioconductor.org/packages/limma> | GPL (≥ 2) |
| edgeR | 4.10.7 | <https://bioconductor.org/packages/edgeR> | GPL (≥ 2) |
| statmod | conda-forge | <https://cran.r-project.org/package=statmod> | GPL-2 \| GPL-3 |
| R | 4.5 (conda-forge) | <https://www.r-project.org> | GPL-2 \| GPL-3 |
| Jupyter Docker Stacks (`r-notebook`) | 2026-10-12 | <https://github.com/jupyter/docker-stacks> | BSD-3-Clause |
| JupyterLab and German language pack | 4.6.4 / 4.5.post3 | <https://jupyter.org> | BSD-3-Clause |
| IRkernel | as in the base image | <https://github.com/IRkernel/IRkernel> | MIT |
| Ubuntu | as in the base image | <https://ubuntu.com> | various free-software licenses, see `/usr/share/doc/*/copyright` in the image |

## Publications

* **Milk data:** Fu NY, Rios AC, Pal B, et al. (2015). EGF-mediated induction of Mcl-1 at the switch to lactation is essential for alveolar cell survival. *Nature Cell Biology* 17:365–375. [doi:10.1038/ncb3117](https://doi.org/10.1038/ncb3117)
* **Airway data:** Himes BE, Jiang X, Wagner P, et al. (2014). RNA-Seq transcriptome profiling identifies CRISPLD2 as a glucocorticoid responsive gene that modulates cytokine function in airway smooth muscle cells. *PLoS ONE* 9(6):e99625. [doi:10.1371/journal.pone.0099625](https://doi.org/10.1371/journal.pone.0099625)
* **Pasilla data:** Brooks AN, Yang L, Duff MO, et al. (2011). Conservation of an RNA regulatory map between *Drosophila* and mammals. *Genome Research* 21:193–202. [doi:10.1101/gr.108662.110](https://doi.org/10.1101/gr.108662.110)
* **TCGA:** The Cancer Genome Atlas Network (2012). Comprehensive molecular portraits of human breast tumours. *Nature* 490:61–70. [doi:10.1038/nature11412](https://doi.org/10.1038/nature11412)
* **limma:** Ritchie ME, Phipson B, Wu D, et al. (2015). *Nucleic Acids Research* 43(7):e47. [doi:10.1093/nar/gkv007](https://doi.org/10.1093/nar/gkv007)
* **voom:** Law CW, Chen Y, Shi W, Smyth GK (2014). *Genome Biology* 15:R29. [doi:10.1186/gb-2014-15-2-r29](https://doi.org/10.1186/gb-2014-15-2-r29)
* **edgeR:** Chen Y, Chen L, Lun ATL, Baldoni PL, Smyth GK (2025). *Nucleic Acids Research* 53(2):gkaf018. [doi:10.1093/nar/gkaf018](https://doi.org/10.1093/nar/gkaf018)
* **Workflow:** Law CW, Alhamdoosh M, Su S, et al. (2016). RNA-seq analysis is easy as 1-2-3 with limma, Glimma and edgeR. *F1000Research* 5:1408. [doi:10.12688/f1000research.9005.3](https://doi.org/10.12688/f1000research.9005.3)
