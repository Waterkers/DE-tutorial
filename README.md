**English** | [Deutsch](README.de.md)

# DE practical: teacher guide

A ready-to-run setup for a high-school practical on **transcriptomics**: students find out which genes cells switch on or off, with a **differential expression (DE) analysis** in R using **limma** and **edgeR**. Students work in **JupyterLab in their browser**; behind it, a Docker container runs R with these packages and four public RNA-seq data sets. Everything is available in **English and German**. It is the companion of the [FBA practical](https://github.com/Waterkers/flux-analysis-intro) and works the same way.

## Plan for a half day (about 3 hours)

| Time | Notebook | What students do |
|---|---|---|
| 10 min | `00_welcome` | transcriptome and RNA-seq in one picture; R basics; fold change and log2 |
| 75 min | `01_tutorial_milk` | guided tutorial with exercises: *which genes switch on when a mouse makes milk?* inspect the data → define groups → filter and normalise, MDS plot → design matrix and contrasts → voom/limma → volcano plot, top genes, conclusion |
| 15 min | break | |
| 60 min | `02`, `03` or `04` (one per group) | do it yourself: a new data set and research question, the same steps with only hints |
| 20 min | | each group shows its volcano plot and one-sentence answer |

**Do-it-yourself choices** (assign by group or let groups choose):

| Notebook | Data set | Research question | What's new | Level |
|---|---|---|---|---|
| `02_diy_dexamethasone` | `airway`: human airway muscle cells of 4 donors ± the asthma drug dexamethasone (Himes et al. 2014) | Which genes does dexamethasone switch on or off, and do they explain why it calms inflammation? | **paired design** (donor in the model) | standard; recommended for most groups |
| `03_diy_pasilla` | `pasilla`: fruit-fly cells with the RNA-binding protein pasilla knocked down (Brooks et al. 2011) | Did the knockdown work, and which genes change without pasilla? | **positive control** and a **batch effect** (single-/paired-end) | medium |
| `04_diy_cancer` | `cancer`: tumour and normal breast tissue of 10 TCGA patients | Which genes differ between tumours and normal tissue, and what do they say about cancer cells? | real patients, messy data, thousands of hits → **prioritising** (`treat`) | challenge |

The expected answers are in the solution notebooks; in brief:

* **Milk:** ~3,700 genes up, ~3,700 down. Top genes cover every milk component: casein *Csn1s2b* (protein), calcium pump *Atp2b2*, zinc/phosphate transporters *Slc30a2*/*Slc34a2*, fat synthesis and fat droplets (*Acacb*, *Elovl5*, *Cidea*).
* **Dexamethasone:** paired design gives ~4,560 DE genes (only ~1,850 without the donor). Up: *DUSP1*, *TSC22D3*/GILZ, *KLF15*, *PER1*, *FKBP5*, *ZBTB16* (anti-inflammatory brakes); down: *VCAM1*, *CXCL12* (immune-cell recruitment).
* **Pasilla:** the gene `ps` is ~3.7× lower (knockdown worked); ~1,260 DE genes with library type in the design, ~670 without.
* **Cancer:** ~2,100 up (cell division: *NUF2*, *ASPM*, *KIF4A*, *MKI67*, *TOP2A*; tissue remodelling: *COL10A1*, *MMP11*), ~2,350 down (fat: *ADIPOQ*, *LEP*; normal ducts: *SCGB3A1*, *MME*). *ESR1*/*ERBB2* vary between patients.

## What's in this folder

| Path | What it is | Give to students? |
|---|---|---|
| `practical/en/`, `practical/de/` | the notebooks students work in; mounted into the container | yes |
| `practical/README*.md` | short student instructions | yes |
| `start.*`, `stop.*`, `docker-compose.yml`, `docker/` | starting and stopping, image definition | yes |
| `teacher/solutions/{en,de}/` | the same notebooks with solutions and outputs | **no** |
| `tools/` | notebook generator, checks, packaging script | no |

## Before the practical

### 1. Build the image

You need Docker (Docker Desktop on Windows/Mac). In this folder:

```bash
docker compose build
```

This takes about 5 minutes and needs internet. It installs limma and edgeR, downloads the four data sets (from GEO, Bioconductor and the NCI Genomic Data Commons, each checked against a fixed checksum) and turns them into simple CSV files in `/opt/data`. Then a **smoke test** runs every analysis and fails the build if the known results don't come out (e.g. milk-protein genes up in lactation, *DUSP1* up with dexamethasone, `ps` down in the knockdown). The image is tagged `de-practical:1.0`. Once built, it works **without internet**.

> If the build stops because it can't resolve host names (some home routers' DNS doesn't work inside Docker), build with the host's network instead: `docker build --network host -t de-practical:1.0 docker`

### 2. Get the image onto the students' computers

Exactly as for the FBA practical. Either **USB stick / shared drive**:

```bash
tools/make_student_package.sh --with-image
```

This writes `dist/de-practical-students.zip` and `dist/de-practical-image.tar.gz` (well over 1 GB). On each student computer, unzip the zip and load the image once: `docker load -i de-practical-image.tar.gz`.

Or a **container registry**, built for Intel/AMD and Apple Silicon:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/YOUR-ACCOUNT/de-practical:1.0 --push docker
```

Then copy `.env.example` to `.env`, set `DE_IMAGE=ghcr.io/YOUR-ACCOUNT/de-practical:1.0` there, and run `tools/make_student_package.sh` (without `--with-image`). The data stage of the build runs only once, on the build machine's own platform; only limma/edgeR are installed per platform.

### 3. Try it once

```bash
./start.sh       # English
./start.sh de    # Deutsch
```

Then go through the notebooks yourself. The solutions in `teacher/solutions/` show the expected output of every cell.

## During the practical

Start and stop exactly as in the FBA practical: `start.bat` / `start_de.bat` (Windows), `start.command` / `start_de.command` (Mac, which needs the one-time *Open Anyway* step described in the [FBA guide](https://github.com/Waterkers/flux-analysis-intro) and in `practical/README.md`), `./start.sh [de]` (Linux); `stop.bat` / `./stop.sh` to stop.

The browser opens at **`http://localhost:8889`** (port 8889, so both practicals can run on the same computer at the same time). JupyterLab is only reachable from the computer itself, so it runs without a password. Students' work stays in `practical/` on their computer.

## Changing the notebooks

As in the FBA practical, the notebooks are generated from **`tools/build_notebooks.py`**, with each cell in English and German side by side. After editing:

```bash
python3 tools/build_notebooks.py     # writes practical/ and teacher/solutions/
python3 tools/check_parity.py        # en and de must run the same code
tools/run_solutions.sh               # runs every solution notebook, so they contain outputs again
```

On GitHub, `.github/workflows/test-image.yml` does all of this automatically on every push and once a month: it builds the image on Intel/AMD and Apple Silicon (arm64), runs the smoke test and every solution notebook, and checks that JupyterLab starts with a Mac user ID. The monthly run notices a download that has disappeared before a practical day.

`build_notebooks.py` overwrites `practical/`, so don't run it on a computer where students have already saved their work. The DIY notebooks are built by the `diy()` and `step()` functions there; to add a data set, add it to `docker/prepare_data.R` and a check to `docker/smoke_test.R`.

## Functions for students

The analysis itself uses the real edgeR and limma functions (`DGEList`, `filterByExpr`, `normLibSizes`, `model.matrix`, `makeContrasts`, `voom`, `lmFit`, `contrasts.fit`, `eBayes`, `decideTests`, `topTable`, `treat`). A few helpers in `docker/helpers/de_helpers.R` load data and draw plots, with bilingual labels:

| Function | What it does |
|---|---|
| `setLanguage("en"/"de")` | language of messages and plot labels |
| `data <- loadDataset("milk")` | `milk`, `airway`, `pasilla` or `cancer`: list with `counts`, `samples`, `genes` |
| `plotLibrarySizes(dge, colour_by)` | bar chart of reads per sample |
| `plotDistributions(dge, colour_by, title)` | box plot of all genes per sample (shows the effect of normalisation) |
| `plotSamples(dge, colour_by, label_by)` | MDS sample map (wraps limma's `plotMDS`) |
| `plotGene(dge, "Csn2", group_by)` | one gene's log-CPM in every sample, by group |
| `showTop(fit, coef, n, direction)` | `topTable` with gene name, description and "× higher/lower" |
| `plotVolcano(fit, coef)` | volcano plot with the top genes named |

limma and edgeR are attached in every R session, and the helpers live in their own environment, so `rm(list = ls())` doesn't remove them (see `docker/Rprofile.site`).

## How the container works

* **Base:** `quay.io/jupyter/r-notebook:2026-10-12` (Ubuntu, JupyterLab 4.6, R 4.5 with the IRkernel), plus the German JupyterLab language pack and the same German menu fixes as the FBA practical (`docker/jupyterlab-de-additions.json`).
* **Packages:** Bioconductor 3.22 from bioconda, pinned: limma 3.68.5, edgeR 4.10.7, statmod.
* **Data (`docker/prepare_data.R`, build stage `data`):**
  * `milk`: GEO GSE60450 gene-wise counts (sha256-checked); gene symbols from org.Mm.eg.db.
  * `airway`: Bioconductor package airway 1.30.0; human genes without a known symbol are dropped.
  * `pasilla`: Bioconductor package pasilla 1.38.0; symbols from org.Dm.eg.db (pasilla itself is `ps`).
  * `cancer`: 20 STAR-Counts files of the first 10 TCGA-BRCA patients (by ID) with both a primary tumour and a solid-tissue-normal sample, from the GDC API (md5-checked, file IDs in `docker/data_sources.tsv`); protein-coding genes only.

  Only the CSV files reach the final image; the annotation packages stay in the build stage.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Docker is not running" | Start Docker Desktop and wait until it says it's running. |
| Build: `Could not resolve host` / download errors | Use `docker build --network host -t de-practical:1.0 docker`. The GDC server sometimes drops connections; the build retries three times, otherwise just run it again. |
| Port 8889 is already in use | Change `127.0.0.1:8889` in `docker-compose.yml` and the start scripts. |
| `pull access denied for de-practical` | The image isn't on this computer: `docker load -i de-practical-image.tar.gz`, or set `DE_IMAGE` in `.env`. |
| A student's cell: `object 'dge' not found` | They skipped cells: *Run → Run All Above Selected Cell*. |
| `plotGene`: "Gene … is not in the data" | Spelling (case doesn't matter), or the gene was removed by `filterByExpr`. |
| Logs | `docker compose logs` |

## Credits and licenses

The data come from Fu et al. 2015 (*Nat Cell Biol*), Himes et al. 2014 (*PLoS ONE*), Brooks et al. 2011 (*Genome Res*) and The Cancer Genome Atlas; the software is limma (Ritchie et al. 2015), voom (Law et al. 2014) and edgeR (Chen et al. 2025). The full references are at the end of `01_tutorial_milk.ipynb` and in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). None of the data are stored in this repository; they are downloaded when the image is built.

## License

| What | License |
|---|---|
| Notebooks (`practical/`, `teacher/`), the notebook texts in `tools/build_notebooks.py`, and the documentation | [CC BY 4.0](LICENSE-CC-BY-4.0.txt) |
| Everything else: code, scripts, Docker and R files | [MIT](LICENSE) |

Third-party software and data used by the image keep their own licenses, see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Please credit adaptations as *"Based on the DE practical by the de-practical contributors, CC BY 4.0"*.
