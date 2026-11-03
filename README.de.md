[English](README.md) | **Deutsch**

# DE-Praktikum: Anleitung für Lehrkräfte

Eine fertige Umgebung für ein Schulpraktikum zur **Transkriptomik**: Die Schülerinnen und Schüler finden heraus, welche Gene Zellen an- oder ausschalten, mit einer **differenziellen Expressionsanalyse (DE-Analyse)** in R mit **limma** und **edgeR**. Gearbeitet wird in **JupyterLab im Browser**; dahinter läuft ein Docker-Container mit R, diesen Paketen und vier öffentlichen RNA-seq-Datensätzen. Alles gibt es auf **Englisch und Deutsch**. Es ist das Gegenstück zum [FBA-Praktikum](https://github.com/Waterkers/flux-analysis-intro) und funktioniert genauso.

## Ablauf für einen halben Tag (etwa 3 Stunden)

| Zeit | Notebook | Was die Schüler tun |
|---|---|---|
| 10 min | `00_welcome` | Transkriptom und RNA-seq in einem Bild; R-Grundlagen; Fold Change und log2 |
| 75 min | `01_tutorial_milk` | angeleitetes Tutorial mit Aufgaben: *Welche Gene schaltet eine Maus an, wenn sie Milch macht?* Daten ansehen → Gruppen festlegen → filtern und normalisieren, MDS-Plot → Design-Matrix und Kontraste → voom/limma → Vulkan-Plot, Top-Gene, Fazit |
| 15 min | Pause | |
| 60 min | `02`, `03` oder `04` (eins pro Gruppe) | selbstständig: neuer Datensatz und neue Forschungsfrage, dieselben Schritte, nur mit Tipps |
| 20 min | | jede Gruppe zeigt ihren Vulkan-Plot und ihre Antwort in einem Satz |

**Auswahl für den selbstständigen Teil** (pro Gruppe zuteilen oder wählen lassen):

| Notebook | Datensatz | Forschungsfrage | Was neu ist | Niveau |
|---|---|---|---|---|
| `02_diy_dexamethasone` | `airway`: menschliche Muskelzellen der Atemwege von 4 Spendern ± Asthma-Medikament Dexamethason (Himes et al. 2014) | Welche Gene schaltet Dexamethason an oder aus, und erklären sie, warum es Entzündungen beruhigt? | **gepaartes Design** (Spender im Modell) | Standard; für die meisten Gruppen empfohlen |
| `03_diy_pasilla` | `pasilla`: Fruchtfliegenzellen mit Knockdown des RNA-bindenden Proteins pasilla (Brooks et al. 2011) | Hat der Knockdown funktioniert, und welche Gene ändern sich ohne pasilla? | **Positivkontrolle** und ein **Batch-Effekt** (Single-/Paired-end) | mittel |
| `04_diy_cancer` | `cancer`: Tumor- und normales Brustgewebe von 10 TCGA-Patientinnen | Welche Gene unterscheiden sich zwischen Tumor und Normalgewebe, und was sagen sie über Krebszellen? | echte Patientinnen, unordentliche Daten, Tausende Treffer → **Prioritäten setzen** (`treat`) | anspruchsvoll |

Die erwarteten Antworten stehen in den Lösungs-Notebooks; kurz:

* **Milch:** ~3.700 Gene hoch, ~3.700 runter. Die Top-Gene decken jeden Milchbestandteil ab: Casein *Csn1s2b* (Eiweiß), Calciumpumpe *Atp2b2*, Zink-/Phosphattransporter *Slc30a2*/*Slc34a2*, Fettherstellung und Fetttröpfchen (*Acacb*, *Elovl5*, *Cidea*).
* **Dexamethason:** Das gepaarte Design findet ~4.560 DE-Gene (ohne Spender nur ~1.850). Hoch: *DUSP1*, *TSC22D3*/GILZ, *KLF15*, *PER1*, *FKBP5*, *ZBTB16* (Entzündungsbremsen); runter: *VCAM1*, *CXCL12* (Anlocken von Immunzellen).
* **Pasilla:** Das Gen `ps` ist ~3,7× niedriger (Knockdown hat funktioniert); ~1.260 DE-Gene mit Bibliotheksart im Design, ~670 ohne.
* **Krebs:** ~2.100 hoch (Zellteilung: *NUF2*, *ASPM*, *KIF4A*, *MKI67*, *TOP2A*; Gewebeumbau: *COL10A1*, *MMP11*), ~2.350 runter (Fett: *ADIPOQ*, *LEP*; normale Milchgänge: *SCGB3A1*, *MME*). *ESR1*/*ERBB2* unterscheiden sich zwischen den Patientinnen.

## Was in diesem Ordner liegt

| Pfad | Was es ist | An Schüler weitergeben? |
|---|---|---|
| `practical/en/`, `practical/de/` | die Notebooks, in denen gearbeitet wird; werden in den Container eingebunden | ja |
| `practical/README*.md` | kurze Anleitung für Schüler | ja |
| `start.*`, `stop.*`, `docker-compose.yml`, `docker/` | Starten und Beenden, Definition des Images | ja |
| `teacher/solutions/{en,de}/` | dieselben Notebooks mit Lösungen und Ausgaben | **nein** |
| `tools/` | Notebook-Generator, Prüfungen, Paket-Skript | nein |

## Vor dem Praktikum

### 1. Image bauen

Du brauchst Docker (unter Windows/Mac Docker Desktop). In diesem Ordner:

```bash
docker compose build
```

Das dauert etwa 5 Minuten und braucht Internet. Dabei werden limma und edgeR installiert, die vier Datensätze heruntergeladen (von GEO, Bioconductor und den NCI Genomic Data Commons, jeweils gegen eine feste Prüfsumme geprüft) und in einfache CSV-Dateien in `/opt/data` umgewandelt. Danach führt ein **Smoke-Test** jede Analyse aus; der Build schlägt fehl, wenn die bekannten Ergebnisse nicht herauskommen (z. B. Milchprotein-Gene in der Laktation hoch, *DUSP1* mit Dexamethason hoch, `ps` im Knockdown runter). Das Image heißt `de-practical:1.0`. Einmal gebaut, funktioniert es **ohne Internet**.

> Bricht der Build ab, weil er Hostnamen nicht auflösen kann (bei manchen Heimroutern funktioniert DNS in Docker nicht), baue mit dem Netzwerk des Rechners: `docker build --network host -t de-practical:1.0 docker`

### 2. Das Image auf die Schülerrechner bringen

Genau wie beim FBA-Praktikum. Entweder **USB-Stick / Netzlaufwerk**:

```bash
tools/make_student_package.sh --with-image
```

Das erzeugt `dist/de-practical-students.zip` und `dist/de-practical-image.tar.gz` (deutlich über 1 GB). Auf jedem Schülerrechner das Zip entpacken und das Image einmal laden: `docker load -i de-practical-image.tar.gz`.

Oder eine **Container-Registry**, gebaut für Intel/AMD und Apple Silicon:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/DEIN-KONTO/de-practical:1.0 --push docker
```

Dann `.env.example` nach `.env` kopieren, dort `DE_IMAGE=ghcr.io/DEIN-KONTO/de-practical:1.0` eintragen und `tools/make_student_package.sh` (ohne `--with-image`) ausführen. Die Daten-Stufe des Builds läuft nur einmal auf der Plattform des Build-Rechners; nur limma/edgeR werden pro Plattform installiert.

### 3. Einmal ausprobieren

```bash
./start.sh       # English
./start.sh de    # Deutsch
```

Geh die Notebooks dann selbst durch. Die Lösungen in `teacher/solutions/` zeigen die erwartete Ausgabe jeder Zelle.

## Während des Praktikums

Starten und Beenden genau wie beim FBA-Praktikum: `start.bat` / `start_de.bat` (Windows), `start.command` / `start_de.command` (Mac, mit dem einmaligen Schritt *Dennoch öffnen*, beschrieben in der [FBA-Anleitung](https://github.com/Waterkers/flux-analysis-intro) und in `practical/README.de.md`), `./start.sh [de]` (Linux); zum Beenden `stop.bat` / `./stop.sh`.

Der Browser öffnet **`http://localhost:8889`** (Port 8889, damit beide Praktika gleichzeitig auf demselben Rechner laufen können). JupyterLab ist nur vom Rechner selbst erreichbar und läuft deshalb ohne Passwort. Die Arbeit der Schüler bleibt in `practical/` auf ihrem Rechner.

## Notebooks ändern

Wie beim FBA-Praktikum werden die Notebooks aus **`tools/build_notebooks.py`** erzeugt, jede Zelle auf Englisch und Deutsch nebeneinander. Nach dem Bearbeiten:

```bash
python3 tools/build_notebooks.py     # schreibt practical/ und teacher/solutions/
python3 tools/check_parity.py        # en und de müssen denselben Code ausführen
tools/run_solutions.sh               # führt alle Lösungs-Notebooks aus, damit sie wieder Ausgaben enthalten
```

Auf GitHub erledigt `.github/workflows/test-image.yml` all das automatisch bei jedem Push und einmal im Monat: Es baut das Image für Intel/AMD und Apple Silicon (arm64), führt den Smoke-Test und alle Lösungs-Notebooks aus und prüft, dass JupyterLab mit einer Mac-Benutzer-ID startet. Der monatliche Lauf bemerkt einen verschwundenen Download vor dem Praktikumstag.

`build_notebooks.py` überschreibt `practical/`, also nicht auf einem Rechner ausführen, auf dem Schüler schon gearbeitet haben. Die DIY-Notebooks entstehen aus den Funktionen `diy()` und `step()`; für einen neuen Datensatz ihn in `docker/prepare_data.R` und eine Prüfung in `docker/smoke_test.R` ergänzen.

## Funktionen für Schüler

Die Analyse selbst nutzt die echten Funktionen aus edgeR und limma (`DGEList`, `filterByExpr`, `normLibSizes`, `model.matrix`, `makeContrasts`, `voom`, `lmFit`, `contrasts.fit`, `eBayes`, `decideTests`, `topTable`, `treat`). Ein paar Hilfsfunktionen in `docker/helpers/de_helpers.R` laden Daten und zeichnen Grafiken, mit zweisprachiger Beschriftung:

| Funktion | Was sie tut |
|---|---|
| `setLanguage("en"/"de")` | Sprache der Meldungen und Grafiken |
| `data <- loadDataset("milk")` | `milk`, `airway`, `pasilla` oder `cancer`: Liste mit `counts`, `samples`, `genes` |
| `plotLibrarySizes(dge, colour_by)` | Balkendiagramm der Reads pro Probe |
| `plotDistributions(dge, colour_by, title)` | Kastendiagramm aller Gene pro Probe (zeigt die Wirkung der Normalisierung) |
| `plotSamples(dge, colour_by, label_by)` | MDS-Probenkarte (nutzt `plotMDS` aus limma) |
| `plotGene(dge, "Csn2", group_by)` | log-CPM eines Gens in jeder Probe, nach Gruppe |
| `showTop(fit, coef, n, direction)` | `topTable` mit Genname, Beschreibung und „× höher/niedriger“ |
| `plotVolcano(fit, coef)` | Vulkan-Plot mit den Namen der Top-Gene |

limma und edgeR sind in jeder R-Sitzung geladen, und die Hilfsfunktionen liegen in einer eigenen Umgebung, sodass `rm(list = ls())` sie nicht löscht (siehe `docker/Rprofile.site`).

## So funktioniert der Container

* **Basis:** `quay.io/jupyter/r-notebook:2026-10-12` (Ubuntu, JupyterLab 4.6, R 4.5 mit IRkernel), dazu das deutsche JupyterLab-Sprachpaket und dieselben deutschen Menü-Korrekturen wie im FBA-Praktikum (`docker/jupyterlab-de-additions.json`).
* **Pakete:** Bioconductor 3.22 aus bioconda, fest: limma 3.68.5, edgeR 4.10.7, statmod.
* **Daten (`docker/prepare_data.R`, Build-Stufe `data`):**
  * `milk`: genweise Counts aus GEO GSE60450 (sha256-geprüft); Gensymbole aus org.Mm.eg.db.
  * `airway`: Bioconductor-Paket airway 1.30.0; menschliche Gene ohne bekanntes Symbol werden weggelassen.
  * `pasilla`: Bioconductor-Paket pasilla 1.38.0; Symbole aus org.Dm.eg.db (pasilla selbst heißt `ps`).
  * `cancer`: 20 STAR-Counts-Dateien der ersten 10 TCGA-BRCA-Patientinnen (nach ID), die sowohl eine Primärtumor- als auch eine Normalgewebeprobe haben, über die GDC-API (md5-geprüft, Datei-IDs in `docker/data_sources.tsv`); nur proteinkodierende Gene.

  Nur die CSV-Dateien kommen ins fertige Image; die Annotationspakete bleiben in der Build-Stufe.

## Fehlerbehebung

| Problem | Lösung |
|---|---|
| „Docker läuft nicht“ | Docker Desktop starten und warten, bis es läuft. |
| Build: `Could not resolve host` / Download-Fehler | `docker build --network host -t de-practical:1.0 docker` benutzen. Der GDC-Server bricht manchmal Verbindungen ab; der Build versucht es dreimal, sonst einfach noch einmal starten. |
| Port 8889 ist schon belegt | `127.0.0.1:8889` in `docker-compose.yml` und den Start-Skripten ändern. |
| `pull access denied for de-practical` | Das Image ist nicht auf dem Rechner: `docker load -i de-practical-image.tar.gz`, oder `DE_IMAGE` in `.env` setzen. |
| Zelle eines Schülers: `object 'dge' not found` | Zellen übersprungen: *Ausführen → Alle Zellen oberhalb ausführen*. |
| `plotGene`: „Das Gen … ist nicht in den Daten“ | Schreibweise (Groß-/Kleinschreibung egal), oder das Gen wurde von `filterByExpr` entfernt. |
| Logs | `docker compose logs` |

## Quellen und Lizenzen

Die Daten stammen von Fu et al. 2015 (*Nat Cell Biol*), Himes et al. 2014 (*PLoS ONE*), Brooks et al. 2011 (*Genome Res*) und The Cancer Genome Atlas; die Software ist limma (Ritchie et al. 2015), voom (Law et al. 2014) und edgeR (Chen et al. 2025). Die vollständigen Quellen stehen am Ende von `01_tutorial_milk.ipynb` und in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Keine der Daten liegt in diesem Repository; sie werden beim Bauen des Images heruntergeladen.

## Lizenz

| Was | Lizenz |
|---|---|
| Notebooks (`practical/`, `teacher/`), die Notebook-Texte in `tools/build_notebooks.py` und die Dokumentation | [CC BY 4.0](LICENSE-CC-BY-4.0.txt) |
| Alles andere: Code, Skripte, Docker- und R-Dateien | [MIT](LICENSE) |

Software und Daten Dritter im Image behalten ihre eigenen Lizenzen, siehe [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Bitte nenne Bearbeitungen so: *„Basierend auf dem DE-Praktikum der de-practical contributors, CC BY 4.0“*.
