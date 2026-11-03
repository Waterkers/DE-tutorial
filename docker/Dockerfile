# DE practical: JupyterLab + R kernel + limma/edgeR + four RNA-seq count tables
# Multi-arch (linux/amd64, linux/arm64). Build context is this docker/ folder.

ARG BASE=quay.io/jupyter/r-notebook:2026-10-12

# ---------------------------------------------------------------------------
# Stage 1: download the raw data and turn it into simple CSV files.
# Runs only on the build machine's own platform: the CSVs are the same everywhere.
# ---------------------------------------------------------------------------
FROM --platform=$BUILDPLATFORM ${BASE} AS data

# Bioconductor 3.22 (matches R 4.5 in the base image): data packages and gene annotation.
RUN mamba install -y -c conda-forge -c bioconda \
        bioconductor-airway=1.30.0 bioconductor-pasilla=1.38.0 \
        bioconductor-org.mm.eg.db=3.22.0 bioconductor-org.dm.eg.db=3.22.0 bioconductor-org.hs.eg.db=3.22.0 \
 && mamba clean -afy
COPY data_sources.tsv prepare_data.R /tmp/prep/
RUN mkdir -p /tmp/data && Rscript /tmp/prep/prepare_data.R /tmp/prep/data_sources.tsv /tmp/data

# ---------------------------------------------------------------------------
# Stage 2: the image students use.
# ---------------------------------------------------------------------------
FROM ${BASE}

USER root

# limma and edgeR (Bioconductor 3.22), pinned.
RUN mamba install -y -c conda-forge -c bioconda \
        bioconductor-limma=3.68.5 bioconductor-edger=4.10.7 r-statmod \
 && mamba clean -afy \
 && fix-permissions "${CONDA_DIR}"

# German JupyterLab interface, plus our translations for menu items the pack leaves in English.
RUN pip install --no-cache-dir jupyterlab-language-pack-de-DE==4.5.post3 \
 && fix-permissions "${CONDA_DIR}"
COPY add_translations.py jupyterlab-de-additions.json /opt/de-setup/
RUN python3 -I /opt/de-setup/add_translations.py /opt/de-setup/jupyterlab-de-additions.json

# Data, helpers and start-up code. Everything under /opt stays root-owned and read-only.
COPY --from=data /tmp/data /opt/data
COPY helpers/ /opt/de-setup/helpers/
COPY smoke_test.R /opt/de-setup/
COPY Rprofile.site /opt/de-setup/Rprofile.site
RUN cat /opt/de-setup/Rprofile.site >> "$(R RHOME)/etc/Rprofile.site"
COPY fix-home-owner.sh /usr/local/bin/before-notebook.d/15-fix-home-owner.sh
COPY jupyterlab-language.sh /usr/local/bin/before-notebook.d/20-jupyterlab-language.sh
RUN chmod -R a+rX,go-w /opt/data /opt/de-setup

# Fail the build if the analyses do not give the known answers.
USER ${NB_UID}
RUN cd /tmp && Rscript /opt/de-setup/smoke_test.R

WORKDIR /home/${NB_USER}
ENV PRACTICAL_LANG=en
