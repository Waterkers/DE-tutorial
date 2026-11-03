"""Build the practical's notebooks from this one source file.

Each notebook is written four times:
    practical/en/<name>.ipynb          student version, English
    practical/de/<name>.ipynb          student version, German
    teacher/solutions/en/<name>.ipynb  with solutions, English
    teacher/solutions/de/<name>.ipynb  with solutions, German

Change the text here and run `python3 tools/build_notebooks.py` from the project
folder, then `python3 tools/check_parity.py`. Writing both languages side by side
keeps the code in the English and German versions identical.

Cell types:
    md(en, de)                   explanation
    code(en, de)                 code cell; the two versions may differ only in comments and text
    exercise(student, solution)  code cell with blanks (___) for students, filled in for teachers;
                                 each argument is an (en, de) pair
    answer(en, de)               answer box: empty for students, model answer for teachers
    hint(en, de)                 folded "Hint" box students can open
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def md(en, de):
    return {"kind": "md", "en": en, "de": de}


def code(en, de=None):
    return {"kind": "code", "en": en, "de": en if de is None else de}


def exercise(student, solution):
    return {"kind": "exercise", "student": student, "solution": solution}


def answer(en, de):
    return {"kind": "answer", "en": en, "de": de}


def hint(en, de):
    return md(
        f"<details><summary>💡 <b>Hint</b> (click to open)</summary>\n\n{en}\n\n</details>",
        f"<details><summary>💡 <b>Tipp</b> (zum Öffnen klicken)</summary>\n\n{de}\n\n</details>",
    )


ANSWER_PROMPT = {
    "en": "✏️ **Your answer:** *(double-click here to type)*\n\n",
    "de": "✏️ **Deine Antwort:** *(Doppelklick hier, um zu schreiben)*\n\n",
}
ANSWER_LABEL = {"en": "✅ **Answer:** ", "de": "✅ **Antwort:** "}
YOUR_CODE = ("# your code here", "# dein Code hier")

LANGUAGE_CELL = code(
    'setLanguage("en")   # language of the messages and plots below',
    'setLanguage("de")   # Sprache der Ausgaben und Grafiken',
)

SOURCES = md(
    """## Sources

**Data**
* **Milk (tutorial):** Fu NY, Rios AC, Pal B, et al. (2015). EGF-mediated induction of Mcl-1 at the switch to lactation is essential for alveolar cell survival. *Nature Cell Biology* 17:365–375. [doi:10.1038/ncb3117](https://doi.org/10.1038/ncb3117). Counts from GEO [GSE60450](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE60450).
* **Dexamethasone (airway):** Himes BE, Jiang X, Wagner P, et al. (2014). RNA-Seq transcriptome profiling identifies CRISPLD2 as a glucocorticoid responsive gene that modulates cytokine function in airway smooth muscle cells. *PLoS ONE* 9(6):e99625. [doi:10.1371/journal.pone.0099625](https://doi.org/10.1371/journal.pone.0099625). Counts from the Bioconductor package [airway](https://bioconductor.org/packages/airway) (Love M).
* **Pasilla:** Brooks AN, Yang L, Duff MO, et al. (2011). Conservation of an RNA regulatory map between *Drosophila* and mammals. *Genome Research* 21:193–202. [doi:10.1101/gr.108662.110](https://doi.org/10.1101/gr.108662.110). Counts from the Bioconductor package [pasilla](https://bioconductor.org/packages/pasilla).
* **Breast cancer:** The Cancer Genome Atlas Network (2012). Comprehensive molecular portraits of human breast tumours. *Nature* 490:61–70. [doi:10.1038/nature11412](https://doi.org/10.1038/nature11412). Counts (STAR – Counts) of 10 TCGA-BRCA patients from the [NCI Genomic Data Commons](https://portal.gdc.cancer.gov).
* **Gene names:** Bioconductor annotation packages org.Mm.eg.db, org.Hs.eg.db, org.Dm.eg.db (Carlson M).

**Software and method**
* **limma:** Ritchie ME, Phipson B, Wu D, et al. (2015). limma powers differential expression analyses for RNA-sequencing and microarray studies. *Nucleic Acids Research* 43(7):e47. [doi:10.1093/nar/gkv007](https://doi.org/10.1093/nar/gkv007)
* **voom:** Law CW, Chen Y, Shi W, Smyth GK (2014). voom: precision weights unlock linear model analysis tools for RNA-seq read counts. *Genome Biology* 15:R29. [doi:10.1186/gb-2014-15-2-r29](https://doi.org/10.1186/gb-2014-15-2-r29)
* **edgeR:** Chen Y, Chen L, Lun ATL, Baldoni PL, Smyth GK (2025). edgeR v4: powerful differential analysis of sequencing data with expanded functionality and improved support for small counts and larger datasets. *Nucleic Acids Research* 53(2):gkaf018. [doi:10.1093/nar/gkaf018](https://doi.org/10.1093/nar/gkaf018)
* **Workflow this practical follows:** Law CW, Alhamdoosh M, Su S, et al. (2016). RNA-seq analysis is easy as 1-2-3 with limma, Glimma and edgeR. *F1000Research* 5:1408. [doi:10.12688/f1000research.9005.3](https://doi.org/10.12688/f1000research.9005.3)""",
    """## Quellen

**Daten**
* **Milch (Tutorial):** Fu NY, Rios AC, Pal B, et al. (2015). EGF-mediated induction of Mcl-1 at the switch to lactation is essential for alveolar cell survival. *Nature Cell Biology* 17:365–375. [doi:10.1038/ncb3117](https://doi.org/10.1038/ncb3117). Counts aus GEO [GSE60450](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE60450).
* **Dexamethason (airway):** Himes BE, Jiang X, Wagner P, et al. (2014). RNA-Seq transcriptome profiling identifies CRISPLD2 as a glucocorticoid responsive gene that modulates cytokine function in airway smooth muscle cells. *PLoS ONE* 9(6):e99625. [doi:10.1371/journal.pone.0099625](https://doi.org/10.1371/journal.pone.0099625). Counts aus dem Bioconductor-Paket [airway](https://bioconductor.org/packages/airway) (Love M).
* **Pasilla:** Brooks AN, Yang L, Duff MO, et al. (2011). Conservation of an RNA regulatory map between *Drosophila* and mammals. *Genome Research* 21:193–202. [doi:10.1101/gr.108662.110](https://doi.org/10.1101/gr.108662.110). Counts aus dem Bioconductor-Paket [pasilla](https://bioconductor.org/packages/pasilla).
* **Brustkrebs:** The Cancer Genome Atlas Network (2012). Comprehensive molecular portraits of human breast tumours. *Nature* 490:61–70. [doi:10.1038/nature11412](https://doi.org/10.1038/nature11412). Counts (STAR – Counts) von 10 Patientinnen aus TCGA-BRCA, aus den [NCI Genomic Data Commons](https://portal.gdc.cancer.gov).
* **Gennamen:** Bioconductor-Annotationspakete org.Mm.eg.db, org.Hs.eg.db, org.Dm.eg.db (Carlson M).

**Software und Methode**
* **limma:** Ritchie ME, Phipson B, Wu D, et al. (2015). limma powers differential expression analyses for RNA-sequencing and microarray studies. *Nucleic Acids Research* 43(7):e47. [doi:10.1093/nar/gkv007](https://doi.org/10.1093/nar/gkv007)
* **voom:** Law CW, Chen Y, Shi W, Smyth GK (2014). voom: precision weights unlock linear model analysis tools for RNA-seq read counts. *Genome Biology* 15:R29. [doi:10.1186/gb-2014-15-2-r29](https://doi.org/10.1186/gb-2014-15-2-r29)
* **edgeR:** Chen Y, Chen L, Lun ATL, Baldoni PL, Smyth GK (2025). edgeR v4: powerful differential analysis of sequencing data with expanded functionality and improved support for small counts and larger datasets. *Nucleic Acids Research* 53(2):gkaf018. [doi:10.1093/nar/gkaf018](https://doi.org/10.1093/nar/gkaf018)
* **Ablauf, dem dieses Praktikum folgt:** Law CW, Alhamdoosh M, Su S, et al. (2016). RNA-seq analysis is easy as 1-2-3 with limma, Glimma and edgeR. *F1000Research* 5:1408. [doi:10.12688/f1000research.9005.3](https://doi.org/10.12688/f1000research.9005.3)""",
)

SOURCES_SHORT = md(
    """<small>Software: limma (Ritchie et al. 2015) with voom (Law et al. 2014) and edgeR (Chen et al. 2025) in R. Full sources for all data sets at the end of `01_tutorial_milk.ipynb`.</small>""",
    """<small>Software: limma (Ritchie et al. 2015) mit voom (Law et al. 2014) und edgeR (Chen et al. 2025) in R. Vollständige Quellen aller Datensätze am Ende von `01_tutorial_milk.ipynb`.</small>""",
)

# ---------------------------------------------------------------------------
# 00 Welcome
# ---------------------------------------------------------------------------
WELCOME = [
    md(
        """# Welcome to transcriptomics! 🧬📊

Every cell in your body has the **same DNA**, with about 20,000 genes. Yet a muscle cell, a nerve cell and a skin cell look and work completely differently. Why? Because each cell **uses different genes**. To use a gene, the cell copies it into a messenger, the **mRNA**, and the mRNA is translated into a protein.

All mRNAs in a cell together are its **transcriptome**. It tells us which genes a cell is using right now, and how strongly.

```mermaid
flowchart LR
    A[DNA<br>the same in every cell] -- transcription --> B[mRNA<br>only the genes in use]
    B -- translation --> C[Protein]
    B -. RNA sequencing .-> D[Count table<br>reads per gene]
```

With **RNA sequencing (RNA-seq)** researchers extract the RNA from cells, cut it into millions of small pieces and read them. A computer then works out which gene each piece (**read**) comes from and counts them. The result is a big table: for every gene, the number of reads in every sample. A gene with many reads is strongly used ("highly expressed").

Today you'll compare such tables between different conditions and find out which genes a cell switches **on** or **off**. That's called **differential expression analysis**.

But first: how does this page work?""",
        """# Willkommen in der Transkriptomik! 🧬📊

Jede Zelle deines Körpers hat **dieselbe DNA** mit etwa 20.000 Genen. Trotzdem sehen eine Muskelzelle, eine Nervenzelle und eine Hautzelle völlig verschieden aus und arbeiten ganz anders. Warum? Weil jede Zelle **andere Gene benutzt**. Um ein Gen zu benutzen, kopiert die Zelle es in einen Boten, die **mRNA**, und die mRNA wird in ein Protein übersetzt.

Alle mRNAs einer Zelle zusammen sind ihr **Transkriptom**. Es verrät uns, welche Gene eine Zelle gerade benutzt, und wie stark.

```mermaid
flowchart LR
    A[DNA<br>in jeder Zelle gleich] -- Transkription --> B[mRNA<br>nur die benutzten Gene]
    B -- Translation --> C[Protein]
    B -. RNA-Sequenzierung .-> D[Zähltabelle<br>Reads pro Gen]
```

Bei der **RNA-Sequenzierung (RNA-seq)** holen Forschende die RNA aus Zellen, zerschneiden sie in Millionen kleiner Stücke und lesen sie. Ein Computer findet dann heraus, von welchem Gen jedes Stück (**Read**) stammt, und zählt sie. Heraus kommt eine große Tabelle: für jedes Gen die Zahl der Reads in jeder Probe. Ein Gen mit vielen Reads wird stark benutzt („hoch exprimiert“).

Heute vergleichst du solche Tabellen zwischen verschiedenen Bedingungen und findest heraus, welche Gene eine Zelle **an-** oder **ausschaltet**. Das nennt man **differenzielle Expressionsanalyse**.

Aber zuerst: Wie funktioniert diese Seite?""",
    ),
    md(
        """## How to use a notebook

This page is a **notebook**. It mixes text (like this) with **code cells** (the grey boxes). The code is written in **R**, a programming language that many biologists use.

To run a code cell: click on it and press **Shift + Enter**. The result appears below the cell.

Try it with the cell below:""",
        """## So benutzt du ein Notebook

Diese Seite ist ein **Notebook**. Es mischt Text (so wie diesen) mit **Code-Zellen** (den grauen Kästen). Der Code ist in **R** geschrieben, einer Programmiersprache, die viele Biologinnen und Biologen benutzen.

So führst du eine Code-Zelle aus: Klicke hinein und drücke **Umschalt + Enter**. Das Ergebnis erscheint unter der Zelle.

Probiere es mit der Zelle hier unten aus:""",
    ),
    code("1 + 1"),
    md(
        """R can remember values under a name. That's called a **variable**. In R you store a value with the arrow `<-`. Run the cell, then change the 7 and run it again.""",
        """R kann sich Werte unter einem Namen merken. Das nennt man eine **Variable**. In R speicherst du einen Wert mit dem Pfeil `<-`. Führe die Zelle aus, ändere dann die 7 und führe sie noch einmal aus.""",
    ),
    code("x <- 7\nx * 2"),
    md(
        """## Many numbers at once

`c(...)` combines several numbers into a list, a **vector**. Here are the read counts of one gene in four samples: two **control** samples and two samples treated with a **drug**.""",
        """## Viele Zahlen auf einmal

`c(...)` fasst mehrere Zahlen zu einer Liste zusammen, einem **Vektor**. Hier sind die Read-Zahlen eines Gens in vier Proben: zwei **Kontroll**proben und zwei Proben, die mit einem **Medikament** behandelt wurden.""",
    ),
    code(
        'counts <- c(120, 135, 980, 1010)\ntreatment <- c("control", "control", "drug", "drug")\nmean(counts)   # the average',
        'counts <- c(120, 135, 980, 1010)\ntreatment <- c("control", "control", "drug", "drug")\nmean(counts)   # der Mittelwert',
    ),
    md(
        """You can pick out values with square brackets. `counts[treatment == "drug"]` means: the counts where the treatment is "drug".""",
        """Mit eckigen Klammern kannst du Werte herauspicken. `counts[treatment == "drug"]` bedeutet: die Counts, bei denen die Behandlung „drug“ (Medikament) ist.""",
    ),
    code('counts[treatment == "drug"]'),
    md(
        """## Your first exercise: how much more?

How many times more reads does the gene have with the drug than without? Divide the average with drug by the average of the controls. Replace the `___` and run the cell.""",
        """## Deine erste Aufgabe: Wie viel mehr?

Wie viel Mal mehr Reads hat das Gen mit dem Medikament als ohne? Teile den Mittelwert mit Medikament durch den Mittelwert der Kontrollen. Ersetze die `___` und führe die Zelle aus.""",
    ),
    exercise(
        (
            'fold_change <- mean(counts[treatment == "___"]) / mean(counts[treatment == "___"])\nfold_change',
            'fold_change <- mean(counts[treatment == "___"]) / mean(counts[treatment == "___"])\nfold_change',
        ),
        (
            'fold_change <- mean(counts[treatment == "drug"]) / mean(counts[treatment == "control"])\nfold_change',
            'fold_change <- mean(counts[treatment == "drug"]) / mean(counts[treatment == "control"])\nfold_change',
        ),
    ),
    md(
        """This ratio is called the **fold change**. Biologists usually give it as a **log2 fold change** (`logFC`): how many times the amount **doubles**.

| fold change | ×8 | ×4 | ×2 | ×1 (no change) | ×½ | ×¼ |
|---|---|---|---|---|---|---|
| **log2 fold change** | 3 | 2 | 1 | 0 | −1 | −2 |

That's practical: "up" is positive, "down" is negative, and doubling and halving are equally far from 0. Calculate the log2 fold change of our gene:""",
        """Dieses Verhältnis heißt **Fold Change** („Faktor der Veränderung“). In der Biologie gibt man es meist als **log2 Fold Change** (`logFC`) an: wie oft sich die Menge **verdoppelt**.

| Fold Change | ×8 | ×4 | ×2 | ×1 (keine Änderung) | ×½ | ×¼ |
|---|---|---|---|---|---|---|
| **log2 Fold Change** | 3 | 2 | 1 | 0 | −1 | −2 |

Das ist praktisch: „hoch“ ist positiv, „runter“ ist negativ, und Verdoppeln und Halbieren sind gleich weit von 0 entfernt. Berechne den log2 Fold Change unseres Gens:""",
    ),
    exercise(("log2(___)", "log2(___)"), ("log2(fold_change)", "log2(fold_change)")),
    answer(
        "The fold change is (980 + 1010) / (120 + 135) ≈ **7.8**: with the drug the gene has almost 8 times as many reads. log2(7.8) ≈ **2.96**, so the amount doubled almost 3 times (2 × 2 × 2 = 8).",
        "Der Fold Change ist (980 + 1010) / (120 + 135) ≈ **7,8**: Mit dem Medikament hat das Gen fast 8-mal so viele Reads. log2(7,8) ≈ **2,96**, die Menge hat sich also fast 3-mal verdoppelt (2 × 2 × 2 = 8).",
    ),
    md(
        """## Tables

Real data come as **tables**. In R a table is a `data.frame`. Each column has a name, and `$` picks out one column.""",
        """## Tabellen

Echte Daten kommen als **Tabellen**. In R heißt eine Tabelle `data.frame`. Jede Spalte hat einen Namen, und `$` holt eine Spalte heraus.""",
    ),
    code(
        'samples <- data.frame(sample = c("A", "B", "C", "D"), treatment = treatment, counts = counts)\nsamples',
    ),
    code("samples$treatment"),
    md(
        """## Why can't we just compare two numbers?

Our gene went from about 130 to about 1000 reads. That looks clear. But real genes are rarely this easy:

* Two samples of the **same** condition are never exactly equal (two mice are never exactly the same). Is a difference real, or just this natural variation? To tell, we need **replicates**: several samples per condition.
* A sample that was sequenced more (more reads in total) has more reads for **every** gene. We have to correct for that: **normalisation**.
* We test **20,000 genes** at once. Some will look different just by chance.

The software **limma** solves these problems for us. In the next notebook you'll use it step by step.

**Well done!** Now open `01_tutorial_milk.ipynb` in the file list on the left.""",
        """## Warum können wir nicht einfach zwei Zahlen vergleichen?

Unser Gen ging von etwa 130 auf etwa 1000 Reads. Das sieht eindeutig aus. Aber echte Gene sind selten so einfach:

* Zwei Proben **derselben** Bedingung sind nie genau gleich (zwei Mäuse sind nie genau gleich). Ist ein Unterschied echt oder nur diese natürliche Schwankung? Um das zu erkennen, brauchen wir **Replikate**: mehrere Proben pro Bedingung.
* Eine Probe, die mehr sequenziert wurde (mehr Reads insgesamt), hat für **jedes** Gen mehr Reads. Das müssen wir ausgleichen: **Normalisierung**.
* Wir testen **20.000 Gene** auf einmal. Manche sehen allein durch Zufall verschieden aus.

Die Software **limma** löst diese Probleme für uns. Im nächsten Notebook benutzt du sie Schritt für Schritt.

**Gut gemacht!** Öffne jetzt `01_tutorial_milk.ipynb` in der Dateiliste links.""",
    ),
]

# ---------------------------------------------------------------------------
# 01 Tutorial: milk
# ---------------------------------------------------------------------------
TUTORIAL = [
    md(
        """# Which genes switch on when a mouse makes milk?

The **mammary gland** changes enormously during pregnancy and when the mother feeds her young (**lactation**). It is built from two kinds of cells:

* **luminal cells** line the inside of the milk ducts and, during lactation, **produce the milk**,
* **basal cells** sit around them and **squeeze** the milk out, like a muscle.

Researchers (Fu et al. 2015) took both cell types from mice in three states: **virgin** (never pregnant), **pregnant** and **lactating**, with two mice per combination. They sequenced the RNA of these **12 samples**.

### Our research question

> Which genes do the **luminal cells** switch on (or off) when they go from **pregnancy** to **making milk**? Can we explain what milk is made of from these genes?

### The plan

```mermaid
flowchart LR
    A[1 Look at<br>the data] --> B[2 Define<br>groups] --> C[3 Prepare:<br>filter, normalise] --> D[4 Design and<br>contrasts] --> E[5 Test<br>with limma] --> F[6 Interpret]
```

Run the cells one after the other, from the top, with **Shift + Enter**.""",
        """# Welche Gene schaltet eine Maus an, wenn sie Milch macht?

Die **Milchdrüse** verändert sich enorm in der Schwangerschaft und wenn die Mutter ihre Jungen säugt (**Laktation**). Sie besteht aus zwei Arten von Zellen:

* **luminale Zellen** kleiden die Milchgänge innen aus und **produzieren** während der Laktation **die Milch**,
* **basale Zellen** sitzen außen herum und **pressen** die Milch heraus, wie ein Muskel.

Forschende (Fu et al. 2015) haben beide Zelltypen aus Mäusen in drei Zuständen entnommen: **virgin** (jungfräulich, nie trächtig), **pregnant** (trächtig) und **lactating** (säugend), mit zwei Mäusen pro Kombination. Die RNA dieser **12 Proben** wurde sequenziert.

### Unsere Forschungsfrage

> Welche Gene schalten die **luminalen Zellen** an (oder aus), wenn sie von der **Trächtigkeit** zur **Milchproduktion** übergehen? Können wir aus diesen Genen erklären, woraus Milch besteht?

### Der Plan

```mermaid
flowchart LR
    A[1 Daten<br>ansehen] --> B[2 Gruppen<br>festlegen] --> C[3 Vorbereiten:<br>filtern, normalisieren] --> D[4 Design und<br>Kontraste] --> E[5 Testen<br>mit limma] --> F[6 Deuten]
```

Führe die Zellen der Reihe nach von oben aus, mit **Umschalt + Enter**.""",
    ),
    LANGUAGE_CELL,
    # --- Part 1: inspect ---
    md(
        """## 1 Look at the data

`loadDataset` loads the data. It contains three tables: `samples` (what each sample is), `counts` (the reads) and `genes` (gene names). Let's look at the samples first.""",
        """## 1 Die Daten ansehen

`loadDataset` lädt die Daten. Sie bestehen aus drei Tabellen: `samples` (was jede Probe ist), `counts` (die Reads) und `genes` (Gennamen). Sehen wir uns zuerst die Proben an.""",
    ),
    code('data <- loadDataset("milk")\ndata$samples'),
    md(
        """Each sample has a name (`MCL1-DG` …), a cell type (`celltype`) and a state (`state`). The names in the table are in English, so `lactating` means "säugend" and `pregnant` "trächtig".

Now the counts. `head()` shows only the first 6 rows; the full table is much longer.""",
        """Jede Probe hat einen Namen (`MCL1-DG` …), einen Zelltyp (`celltype`) und einen Zustand (`state`). Die Einträge in der Tabelle sind englisch: `lactating` heißt „säugend“, `pregnant` „trächtig“, `virgin` „jungfräulich“.

Jetzt die Counts. `head()` zeigt nur die ersten 6 Zeilen; die ganze Tabelle ist viel länger.""",
    ),
    code("head(data$counts)"),
    md(
        """Each **row** is a gene (the numbers on the left are gene IDs from the NCBI database), each **column** a sample, and each number says how many reads of that gene were found in that sample. The `genes` table translates the IDs into gene names:""",
        """Jede **Zeile** ist ein Gen (die Zahlen links sind Gen-IDs aus der NCBI-Datenbank), jede **Spalte** eine Probe, und jede Zahl sagt, wie viele Reads dieses Gens in dieser Probe gefunden wurden. Die Tabelle `genes` übersetzt die IDs in Gennamen:""",
    ),
    code("head(data$genes)"),
    md(
        """**Exercise:** How many genes and how many samples are in the count table? `dim()` gives the size of a table: first the number of rows, then of columns.""",
        """**Aufgabe:** Wie viele Gene und wie viele Proben enthält die Zähltabelle? `dim()` gibt die Größe einer Tabelle an: zuerst die Zahl der Zeilen, dann der Spalten.""",
    ),
    exercise(("dim(___)", "dim(___)"), ("dim(data$counts)", "dim(data$counts)")),
    answer(
        "**27,179 genes** (rows) and **12 samples** (columns): 2 cell types × 3 states × 2 mice.",
        "**27.179 Gene** (Zeilen) und **12 Proben** (Spalten): 2 Zelltypen × 3 Zustände × 2 Mäuse.",
    ),
    md(
        """For the analysis, we put the three tables into one container, a `DGEList` from the package **edgeR**. It also adds up the reads of each sample: the **library size**.""",
        """Für die Analyse packen wir die drei Tabellen in einen Behälter, eine `DGEList` aus dem Paket **edgeR**. Sie zählt auch die Reads jeder Probe zusammen: die **Bibliotheksgröße** (library size).""",
    ),
    code(
        "dge <- DGEList(counts = data$counts, samples = data$samples, genes = data$genes)\ndge$samples",
    ),
    code('plotLibrarySizes(dge, colour_by = "celltype")'),
    md(
        """**Question:** Do all samples have the same number of reads? Why would it be wrong to compare the raw counts of a gene between two samples?""",
        """**Frage:** Haben alle Proben gleich viele Reads? Warum wäre es falsch, die rohen Counts eines Gens zwischen zwei Proben zu vergleichen?""",
    ),
    answer(
        "No: between about **20 and 25 million** reads. A sample with 25 million reads has about 25 % more reads for *every* gene than one with 20 million, even if the cells are identical. So we must compare **proportions** (reads per million), not raw counts.",
        "Nein: zwischen etwa **20 und 25 Millionen** Reads. Eine Probe mit 25 Millionen Reads hat für *jedes* Gen etwa 25 % mehr Reads als eine mit 20 Millionen, auch wenn die Zellen identisch sind. Wir müssen also **Anteile** (Reads pro Million) vergleichen, nicht rohe Counts.",
    ),
    md(
        """**Exercise:** Many genes are not used at all in these cells. How many genes have **0 reads in all 12 samples**? `rowSums()` adds up each row, and `sum(... == x)` counts how often something equals `x`.""",
        """**Aufgabe:** Viele Gene werden in diesen Zellen gar nicht benutzt. Wie viele Gene haben **0 Reads in allen 12 Proben**? `rowSums()` addiert jede Zeile, und `sum(... == x)` zählt, wie oft etwas gleich `x` ist.""",
    ),
    exercise(
        ("sum(rowSums(dge$counts) == ___)", "sum(rowSums(dge$counts) == ___)"),
        ("sum(rowSums(dge$counts) == 0)", "sum(rowSums(dge$counts) == 0)"),
    ),
    answer(
        "**5,787 genes** have no read at all. Mammary gland cells simply don't use them (for example genes only used in the brain or liver).",
        "**5.787 Gene** haben keinen einzigen Read. Die Zellen der Milchdrüse benutzen sie einfach nicht (zum Beispiel Gene, die nur im Gehirn oder in der Leber gebraucht werden).",
    ),
    # --- Part 2: groups ---
    md(
        """## 2 Define the groups

To compare, limma has to know which samples belong together. Each combination of cell type and state is one **group**, for example `luminal_lactating`. We glue the two columns together with `paste` and store the result in the `group` column.""",
        """## 2 Die Gruppen festlegen

Zum Vergleichen muss limma wissen, welche Proben zusammengehören. Jede Kombination aus Zelltyp und Zustand ist eine **Gruppe**, zum Beispiel `luminal_lactating`. Wir kleben die beiden Spalten mit `paste` zusammen und speichern das Ergebnis in der Spalte `group`.""",
    ),
    code(
        'group <- paste(dge$samples$celltype, dge$samples$state, sep = "_")\ndge$samples$group <- factor(group, levels = unique(group))\ntable(dge$samples$group)',
    ),
    md(
        """**Question:** How many samples does each group have? Why do researchers use several mice per group (**replicates**) instead of one?""",
        """**Frage:** Wie viele Proben hat jede Gruppe? Warum benutzen Forschende mehrere Mäuse pro Gruppe (**Replikate**) statt nur einer?""",
    ),
    answer(
        "**6 groups with 2 samples each.** With only one mouse per group we couldn't tell whether a difference comes from the condition or just from the fact that every mouse is a bit different. Replicates show how large this natural variation is; limma compares each difference with it.",
        "**6 Gruppen mit je 2 Proben.** Mit nur einer Maus pro Gruppe könnten wir nicht unterscheiden, ob ein Unterschied von der Bedingung kommt oder nur daher, dass jede Maus etwas anders ist. Replikate zeigen, wie groß diese natürliche Schwankung ist; limma vergleicht jeden Unterschied damit.",
    ),
    md(
        """Let's look at a single gene. **Csn2** is the gene for **β-casein**, the main protein in milk. `plotGene` shows its expression in every sample as **log2 counts per million**: going up by 1 means twice as much. Where do you expect it to be high?""",
        """Sehen wir uns ein einzelnes Gen an. **Csn2** ist das Gen für **β-Casein**, das wichtigste Protein in der Milch. `plotGene` zeigt seine Expression in jeder Probe als **log2 Counts pro Million**: 1 höher bedeutet doppelt so viel. Wo erwartest du es hoch?""",
    ),
    code('plotGene(dge, "Csn2", group_by = "group")'),
    md(
        """**Exercise:** Use your biology to check that the samples are labelled correctly. **Krt5** (keratin 5) is a typical protein of basal cells, **Krt8** (keratin 8) of luminal cells. Plot one of them.""",
        """**Aufgabe:** Prüfe mit deinem Biologiewissen, ob die Proben richtig beschriftet sind. **Krt5** (Keratin 5) ist ein typisches Protein der basalen Zellen, **Krt8** (Keratin 8) der luminalen Zellen. Zeichne eins davon.""",
    ),
    exercise(
        ('plotGene(dge, "___", group_by = "group")', 'plotGene(dge, "___", group_by = "group")'),
        ('plotGene(dge, "Krt5", group_by = "group")', 'plotGene(dge, "Krt5", group_by = "group")'),
    ),
    answer(
        "Csn2 is low in virgin mice, much higher in pregnancy and highest in **lactating luminal cells** (about 2¹³ ≈ 8,000 times more than in basal cells of virgin mice!). Krt5 is high in all **basal** samples and low in luminal ones (Krt8 the other way round). So the labels make sense.",
        "Csn2 ist bei jungfräulichen Mäusen niedrig, in der Trächtigkeit viel höher und am höchsten in **säugenden luminalen Zellen** (etwa 2¹³ ≈ 8.000-mal mehr als in basalen Zellen jungfräulicher Mäuse!). Krt5 ist in allen **basalen** Proben hoch und in luminalen niedrig (Krt8 umgekehrt). Die Beschriftung passt also.",
    ),
    # --- Part 3: prepare ---
    md(
        """## 3 Prepare the data

### Filtering

Genes with only a handful of reads can't be tested reliably: 0 vs. 2 reads could easily be chance. `filterByExpr` keeps only genes with enough reads in at least as many samples as the smallest group has (here 2). `TRUE` means keep.""",
        """## 3 Die Daten vorbereiten

### Filtern

Gene mit nur einer Handvoll Reads lassen sich nicht zuverlässig testen: 0 gegen 2 Reads könnte gut Zufall sein. `filterByExpr` behält nur Gene, die genug Reads in mindestens so vielen Proben haben, wie die kleinste Gruppe hat (hier 2). `TRUE` heißt behalten.""",
    ),
    code("keep <- filterByExpr(dge)\ntable(keep)"),
    code("dge <- dge[keep, , keep.lib.sizes = FALSE]\ndim(dge)"),
    md(
        """### Normalisation

Now let's look at the distribution of **all** genes in each sample. Each box shows the middle half of the genes; the line in the box is the median. If the samples are comparable, the boxes should be at about the same height.""",
        """### Normalisieren

Jetzt sehen wir uns die Verteilung **aller** Gene in jeder Probe an. Jeder Kasten zeigt die mittlere Hälfte der Gene; der Strich im Kasten ist der Median. Wenn die Proben vergleichbar sind, sollten die Kästen etwa gleich hoch liegen.""",
    ),
    code(
        'plotDistributions(dge, colour_by = "group", title = "Before normalisation")',
        'plotDistributions(dge, colour_by = "group", title = "Vor dem Normalisieren")',
    ),
    md(
        """Look at the two lactating luminal samples (`MCL1-LE`, `MCL1-LF`): their boxes are **lower**. Are all their genes really less active? No! These cells spend a huge part of their RNA on a few milk genes. Calculate the share of reads for Csn2 alone (gene ID 12991) in sample `MCL1-LE`:""",
        """Sieh dir die beiden säugenden luminalen Proben an (`MCL1-LE`, `MCL1-LF`): Ihre Kästen liegen **tiefer**. Sind wirklich alle ihre Gene weniger aktiv? Nein! Diese Zellen stecken einen riesigen Teil ihrer RNA in ein paar Milchgene. Berechne den Anteil der Reads, den allein Csn2 (Gen-ID 12991) in der Probe `MCL1-LE` hat:""",
    ),
    code(
        'data$counts["12991", "MCL1-LE"] / sum(data$counts[, "MCL1-LE"])   # share of all reads',
        'data$counts["12991", "MCL1-LE"] / sum(data$counts[, "MCL1-LE"])   # Anteil an allen Reads',
    ),
    md(
        """About **10 %** of all reads come from this one gene. Then fewer reads are left for all the other genes, and they *look* lower. The **TMM normalisation** in `normLibSizes` corrects this: it calculates a correction factor for each sample (`norm.factors`) from the many genes that don't change.""",
        """Etwa **10 %** aller Reads stammen von diesem einen Gen. Dann bleiben für alle anderen Gene weniger Reads übrig, und sie *sehen* niedriger aus. Die **TMM-Normalisierung** in `normLibSizes` gleicht das aus: Sie berechnet für jede Probe einen Korrekturfaktor (`norm.factors`) aus den vielen Genen, die sich nicht verändern.""",
    ),
    code('dge <- normLibSizes(dge)\ndge$samples[, c("group", "lib.size", "norm.factors")]'),
    code(
        'plotDistributions(dge, colour_by = "group", title = "After normalisation")',
        'plotDistributions(dge, colour_by = "group", title = "Nach dem Normalisieren")',
    ),
    md(
        """**Question:** How many genes are left after filtering? Which samples get the smallest correction factor, and what changed in the box plot?""",
        """**Frage:** Wie viele Gene bleiben nach dem Filtern übrig? Welche Proben bekommen den kleinsten Korrekturfaktor, und was hat sich im Kastendiagramm verändert?""",
    ),
    answer(
        "**15,969 genes** of 27,179 remain. The lactating luminal samples LE and LF get the smallest factor (about **0.53**): their library size is effectively halved, to make up for the reads used by the milk genes. After normalisation, all boxes are at about the same height.",
        "**15.969 Gene** von 27.179 bleiben übrig. Die säugenden luminalen Proben LE und LF bekommen den kleinsten Faktor (etwa **0,53**): Ihre Bibliotheksgröße wird praktisch halbiert, um die Reads der Milchgene auszugleichen. Nach dem Normalisieren liegen alle Kästen etwa gleich hoch.",
    ),
    md(
        """### The sample map (MDS)

Before testing single genes, let's see how similar the samples are **overall**. An **MDS plot** puts each sample on a map: samples whose ~16,000 genes are expressed similarly lie close together. **Distance 1** (left–right) is the direction in which the samples differ most; the percentage says how much of all differences it shows.""",
        """### Die Probenkarte (MDS)

Bevor wir einzelne Gene testen, sehen wir uns an, wie ähnlich sich die Proben **insgesamt** sind. Ein **MDS-Plot** setzt jede Probe auf eine Karte: Proben, deren ~16.000 Gene ähnlich exprimiert sind, liegen nah beieinander. **Richtung 1** (links–rechts) ist die Richtung, in der sich die Proben am stärksten unterscheiden; die Prozentzahl sagt, wie viel aller Unterschiede sie zeigt.""",
    ),
    code('plotSamples(dge, colour_by = "celltype", label_by = "state")'),
    md(
        """**Exercise:** Now colour the samples by state and label them by cell type.""",
        """**Aufgabe:** Färbe die Proben jetzt nach Zustand ein und beschrifte sie mit dem Zelltyp.""",
    ),
    exercise(
        ('plotSamples(dge, colour_by = "___", label_by = "___")', 'plotSamples(dge, colour_by = "___", label_by = "___")'),
        ('plotSamples(dge, colour_by = "state", label_by = "celltype")', 'plotSamples(dge, colour_by = "state", label_by = "celltype")'),
    ),
    md(
        """**Question:** What separates the samples along distance 1, and what along distance 2? Do the two replicates of each group lie close together? Why is that good news?""",
        """**Frage:** Was trennt die Proben entlang Richtung 1, was entlang Richtung 2? Liegen die beiden Replikate jeder Gruppe nah beieinander? Warum ist das eine gute Nachricht?""",
    ),
    answer(
        "Distance 1 (**65 %**) separates **basal from luminal** cells: the cell type is by far the biggest difference. Distance 2 (**17 %**) sorts the samples by state: virgin → pregnant → lactating, and the change is larger in luminal cells. The replicates lie close together, so the experiment worked well and no samples were mixed up.",
        "Richtung 1 (**65 %**) trennt **basale von luminalen** Zellen: Der Zelltyp ist mit Abstand der größte Unterschied. Richtung 2 (**17 %**) sortiert die Proben nach Zustand: jungfräulich → trächtig → säugend, und die Veränderung ist in luminalen Zellen größer. Die Replikate liegen nah beieinander, das Experiment hat also gut funktioniert und keine Proben wurden vertauscht.",
    ),
    # --- Part 4: design & contrasts ---
    md(
        """## 4 Design and contrasts

### The design matrix

The **design matrix** tells limma which group each sample belongs to: one column per group, with a 1 if the sample belongs to it.""",
        """## 4 Design und Kontraste

### Die Design-Matrix

Die **Design-Matrix** sagt limma, zu welcher Gruppe jede Probe gehört: eine Spalte pro Gruppe, mit einer 1, wenn die Probe dazugehört.""",
    ),
    code(
        "design <- model.matrix(~0 + group, data = dge$samples)\ncolnames(design) <- levels(dge$samples$group)\ndesign",
    ),
    md(
        """### Contrasts: which groups do we compare?

A **contrast** is the comparison you are interested in, written as a subtraction: `A - B` asks "how is A different from B?". A **positive** log fold change then means **higher in A**.

Our question compares **lactating** with **pregnant** luminal cells. Why not simply all lactating with all pregnant samples? Because basal cells don't make milk, and mixing them in would blur the result: the MDS plot showed that the cell type is the biggest difference of all.

**Exercise:** Fill in the two contrasts:
1. `lactating_vs_pregnant`: luminal cells, lactating compared with pregnant,
2. `luminal_vs_basal`: in virgin mice, luminal compared with basal cells.

Use the group names exactly as in the design matrix.""",
        """### Kontraste: Welche Gruppen vergleichen wir?

Ein **Kontrast** ist der Vergleich, der dich interessiert, geschrieben als Subtraktion: `A - B` fragt „wie unterscheidet sich A von B?“. Ein **positiver** log Fold Change bedeutet dann **höher in A**.

Unsere Frage vergleicht **säugende** mit **trächtigen** luminalen Zellen. Warum nicht einfach alle säugenden mit allen trächtigen Proben? Weil basale Zellen keine Milch machen, und wenn wir sie mischen, verwischt das Ergebnis: Der MDS-Plot hat gezeigt, dass der Zelltyp der größte Unterschied von allen ist.

**Aufgabe:** Fülle die beiden Kontraste aus:
1. `lactating_vs_pregnant`: luminale Zellen, säugend verglichen mit trächtig,
2. `luminal_vs_basal`: bei jungfräulichen Mäusen, luminale verglichen mit basalen Zellen.

Benutze die Gruppennamen genau so wie in der Design-Matrix.""",
    ),
    exercise(
        (
            "contrasts <- makeContrasts(\n    lactating_vs_pregnant = ___ - ___,\n    luminal_vs_basal      = ___ - ___,\n    levels = design)\ncontrasts",
            "contrasts <- makeContrasts(\n    lactating_vs_pregnant = ___ - ___,\n    luminal_vs_basal      = ___ - ___,\n    levels = design)\ncontrasts",
        ),
        (
            "contrasts <- makeContrasts(\n    lactating_vs_pregnant = luminal_lactating - luminal_pregnant,\n    luminal_vs_basal      = luminal_virgin - basal_virgin,\n    levels = design)\ncontrasts",
            "contrasts <- makeContrasts(\n    lactating_vs_pregnant = luminal_lactating - luminal_pregnant,\n    luminal_vs_basal      = luminal_virgin - basal_virgin,\n    levels = design)\ncontrasts",
        ),
    ),
    md(
        """**Question:** In `lactating_vs_pregnant`, what does a log fold change of **+3** mean for a gene? And **−1**? Which contrast would you write to find the genes that change in **basal** cells during pregnancy?""",
        """**Frage:** Was bedeutet im Kontrast `lactating_vs_pregnant` ein log Fold Change von **+3** für ein Gen? Und **−1**? Welchen Kontrast würdest du schreiben, um die Gene zu finden, die sich in **basalen** Zellen in der Trächtigkeit verändern?""",
    ),
    answer(
        "**+3**: the gene is 2³ = **8 times higher** in lactating than in pregnant luminal cells. **−1**: it is **half** as high. For basal cells in pregnancy: `basal_pregnant - basal_virgin`.",
        "**+3**: Das Gen ist in säugenden luminalen Zellen 2³ = **8-mal höher** als in trächtigen. **−1**: Es ist **halb** so hoch. Für basale Zellen in der Trächtigkeit: `basal_pregnant - basal_virgin`.",
    ),
    # --- Part 5: analyse ---
    md(
        """## 5 Test every gene with limma

Three steps:

1. **`voom`** turns the counts into log2 counts per million and works out how reliable each value is: genes with few reads are noisier, so they get less weight. The plot shows this: the fewer reads (left), the larger the variation (up).
2. **`lmFit`** calculates the average of every gene in every group, and **`contrasts.fit`** the differences we asked for in the contrasts.
3. **`eBayes`** tests whether each difference is larger than the natural variation between the replicates. With only 2 replicates that variation is hard to estimate for a single gene, so limma "borrows" information from all the other genes. That's what makes limma work with small experiments.""",
        """## 5 Jedes Gen mit limma testen

Drei Schritte:

1. **`voom`** wandelt die Counts in log2 Counts pro Million um und schätzt, wie zuverlässig jeder Wert ist: Gene mit wenigen Reads schwanken stärker und bekommen deshalb weniger Gewicht. Der Plot zeigt das: Je weniger Reads (links), desto größer die Schwankung (oben).
2. **`lmFit`** berechnet für jedes Gen den Mittelwert in jeder Gruppe, und **`contrasts.fit`** die Unterschiede, nach denen wir in den Kontrasten gefragt haben.
3. **`eBayes`** testet, ob jeder Unterschied größer ist als die natürliche Schwankung zwischen den Replikaten. Mit nur 2 Replikaten lässt sich diese Schwankung für ein einzelnes Gen schlecht schätzen, also „leiht“ sich limma Information von allen anderen Genen. Deshalb funktioniert limma auch bei kleinen Experimenten.""",
    ),
    code("v <- voom(dge, design, plot = TRUE)"),
    code("fit <- lmFit(v, design)\nfit <- contrasts.fit(fit, contrasts)\nfit <- eBayes(fit)"),
    md(
        """### How many genes changed?

For each gene, limma calculates a **p-value**: how likely is a difference this large if the gene didn't really change? Small = convincing.

But careful: we test about 16,000 genes. With the usual limit p < 0.05, about 5 % of the genes that **don't** change would still look significant by chance: that's 800 false hits! That's why limma also gives an **adjusted p-value** (`adj.P.Val`). If we take all genes with adjusted p < 0.05, only about 5 % of **this list** are false hits.

`decideTests` counts the genes with adjusted p < 0.05: up, down or not significant (`NotSig`).""",
        """### Wie viele Gene haben sich verändert?

Für jedes Gen berechnet limma einen **p-Wert**: Wie wahrscheinlich ist ein so großer Unterschied, wenn sich das Gen in Wirklichkeit gar nicht verändert hat? Klein = überzeugend.

Aber Vorsicht: Wir testen etwa 16.000 Gene. Mit der üblichen Grenze p < 0,05 würden etwa 5 % der Gene, die sich **nicht** verändern, trotzdem zufällig signifikant aussehen: Das wären 800 falsche Treffer! Deshalb gibt limma auch einen **adjustierten p-Wert** (`adj.P.Val`) an. Nehmen wir alle Gene mit adjustiertem p < 0,05, dann sind nur etwa 5 % **dieser Liste** falsche Treffer.

`decideTests` zählt die Gene mit adjustiertem p < 0,05: hoch (`Up`), runter (`Down`) oder nicht signifikant (`NotSig`).""",
    ),
    code("summary(decideTests(fit))"),
    md(
        """**Question:** How many genes go up and down from pregnancy to lactation? Which of the two contrasts has more changed genes, and does that fit the MDS plot?""",
        """**Frage:** Wie viele Gene gehen von der Trächtigkeit zur Laktation hoch, wie viele runter? Welcher der beiden Kontraste hat mehr veränderte Gene, und passt das zum MDS-Plot?""",
    ),
    answer(
        "Lactating vs pregnant: about **3,700 up** and **3,700 down**. Luminal vs basal: about **5,100 up** and **5,100 down**, even more. That fits the MDS plot, where the cell type (distance 1) was the biggest difference. Thousands of significant genes are normal in such a big biological change; that's why the next step is to look at the **strongest** ones.",
        "Säugend gegen trächtig: etwa **3.700 hoch** und **3.700 runter**. Luminal gegen basal: etwa **5.100 hoch** und **5.100 runter**, also noch mehr. Das passt zum MDS-Plot, in dem der Zelltyp (Richtung 1) der größte Unterschied war. Tausende signifikante Gene sind bei einer so großen biologischen Veränderung normal; deshalb sehen wir uns im nächsten Schritt die **stärksten** an.",
    ),
    # --- Part 6: interpret ---
    md(
        """## 6 Interpret the results

### The volcano plot

In a **volcano plot** every gene is a dot. Left–right is the log fold change (left: lower when lactating, right: higher), and up is how certain the result is. The most interesting genes are at the top left and top right: a big change **and** convincing. Coloured dots are significant and change at least 2-fold (dashed lines).""",
        """## 6 Die Ergebnisse deuten

### Der Vulkan-Plot

Im **Vulkan-Plot** ist jedes Gen ein Punkt. Links–rechts ist der log Fold Change (links: niedriger beim Säugen, rechts: höher), und nach oben, wie sicher das Ergebnis ist. Die spannendsten Gene sind oben links und oben rechts: eine große Veränderung **und** überzeugend. Farbige Punkte sind signifikant und ändern sich mindestens um das 2-fache (gestrichelte Linien).""",
    ),
    code('plotVolcano(fit, "lactating_vs_pregnant")'),
    md(
        """### The top genes

`showTop` lists the most convincing genes with their name and description. `change` translates the log fold change back into "times higher/lower".""",
        """### Die Top-Gene

`showTop` listet die überzeugendsten Gene mit Namen und Beschreibung auf. `change` übersetzt den log Fold Change zurück in „-mal höher/niedriger“.""",
    ),
    code('showTop(fit, "lactating_vs_pregnant", n = 15, direction = "up")'),
    md(
        """**Exercise:** Choose a gene from the list that interests you and look at it in all groups.

Find out what it does: search for its name on [GeneCards](https://www.genecards.org) (for human genes; the mouse gene usually does the same), [NCBI Gene](https://www.ncbi.nlm.nih.gov/gene) or [UniProt](https://www.uniprot.org), or think about the description. *Tip: milk contains protein (caseins), fat, milk sugar (lactose), calcium, zinc and phosphate.*""",
        """**Aufgabe:** Wähle ein Gen aus der Liste, das dich interessiert, und sieh es dir in allen Gruppen an.

Finde heraus, was es tut: Suche seinen Namen auf [GeneCards](https://www.genecards.org) (für menschliche Gene; das Maus-Gen tut meist dasselbe), [NCBI Gene](https://www.ncbi.nlm.nih.gov/gene) oder [UniProt](https://www.uniprot.org), oder denke über die Beschreibung nach. *Tipp: Milch enthält Eiweiß (Caseine), Fett, Milchzucker (Laktose), Calcium, Zink und Phosphat.*""",
    ),
    exercise(
        ('plotGene(dge, "___", group_by = "group")', 'plotGene(dge, "___", group_by = "group")'),
        ('plotGene(dge, "Atp2b2", group_by = "group")', 'plotGene(dge, "Atp2b2", group_by = "group")'),
    ),
    md(
        """**Question:** Can you connect the top genes to what milk is made of? Find at least three examples.""",
        """**Frage:** Kannst du die Top-Gene damit verbinden, woraus Milch besteht? Finde mindestens drei Beispiele.""",
    ),
    answer(
        """* **Protein:** *Csn1s2b* is a **casein**, a milk protein (≈ 390 times higher).
* **Calcium:** *Atp2b2* is a calcium pump that moves calcium **into the milk** (≈ 170 times higher).
* **Zinc and phosphate:** *Slc30a2* transports zinc, *Slc34a2* phosphate into the milk.
* **Fat:** *Acacb*, *Elovl5* and *Pmvk* make fatty acids and other fats; *Cidea* helps package fat into the droplets that make up milk fat; *Slc25a1* supplies the building material for fatty acids.

So the luminal cells switch on a whole **milk factory**: genes for every component of milk.""",
        """* **Eiweiß:** *Csn1s2b* ist ein **Casein**, ein Milchprotein (≈ 390-mal höher).
* **Calcium:** *Atp2b2* ist eine Calciumpumpe, die Calcium **in die Milch** befördert (≈ 170-mal höher).
* **Zink und Phosphat:** *Slc30a2* transportiert Zink, *Slc34a2* Phosphat in die Milch.
* **Fett:** *Acacb*, *Elovl5* und *Pmvk* stellen Fettsäuren und andere Fette her; *Cidea* hilft, das Fett in die Tröpfchen zu verpacken, aus denen das Milchfett besteht; *Slc25a1* liefert das Baumaterial für Fettsäuren.

Die luminalen Zellen schalten also eine ganze **Milchfabrik** an: Gene für jeden Bestandteil der Milch.""",
    ),
    md(
        """Where are the famous milk genes like **Wap** (whey acidic protein) and **Lalba** (α-lactalbumin, needed to make lactose)? Look at one of them:""",
        """Wo sind die berühmten Milchgene wie **Wap** (Molkenprotein) und **Lalba** (α-Lactalbumin, wird zur Herstellung von Laktose gebraucht)? Sieh dir eins davon an:""",
    ),
    code('plotGene(dge, "Wap", group_by = "group")'),
    md(
        """**Question:** Wap is significantly higher in lactating cells, but it is not at the top of the list. Why not?""",
        """**Frage:** Wap ist in säugenden Zellen signifikant höher, steht aber nicht oben in der Liste. Warum nicht?""",
    ),
    answer(
        "Wap is already **very high in pregnancy**: the gland prepares for milk production before birth. From pregnancy to lactation it only rises about 14-fold (logFC ≈ 3.8), less than the top genes. The list is sorted by how convincing the change is, not by how highly a gene is expressed.",
        "Wap ist schon in der **Trächtigkeit sehr hoch**: Die Drüse bereitet sich vor der Geburt auf die Milchproduktion vor. Von der Trächtigkeit zur Laktation steigt es nur noch etwa 14-fach (logFC ≈ 3,8), weniger als die Top-Gene. Die Liste ist danach sortiert, wie überzeugend die Veränderung ist, nicht danach, wie hoch ein Gen exprimiert ist.",
    ),
    md("""Now the genes that go **down**:""", """Jetzt die Gene, die **runter** gehen:"""),
    code('showTop(fit, "lactating_vs_pregnant", n = 10, direction = "down")'),
    md(
        """### Your conclusion

**Exercise:** Answer the research question in two or three sentences, as you would in a lab report: what did you compare, what did you find, and what does it mean?""",
        """### Dein Fazit

**Aufgabe:** Beantworte die Forschungsfrage in zwei oder drei Sätzen, so wie in einem Laborbericht: Was hast du verglichen, was hast du gefunden, und was bedeutet es?""",
    ),
    answer(
        "We compared luminal cells of lactating and pregnant mice (2 mice each) with limma. About 3,700 genes went up and 3,700 down significantly. The strongest increases were in genes for every component of milk: caseins (protein), fat production and fat droplets, and transporters for calcium, zinc and phosphate. So at the start of lactation the luminal cells switch on a complete milk production programme. Genes going down include some for growth and development (e.g. *Sox4*): the gland has finished growing and now concentrates on making milk.",
        "Wir haben luminale Zellen säugender und trächtiger Mäuse (je 2 Mäuse) mit limma verglichen. Etwa 3.700 Gene gingen signifikant hoch und 3.700 runter. Am stärksten stiegen Gene für jeden Bestandteil der Milch: Caseine (Eiweiß), Fettherstellung und Fetttröpfchen sowie Transporter für Calcium, Zink und Phosphat. Zu Beginn der Laktation schalten die luminalen Zellen also ein komplettes Milchproduktionsprogramm an. Unter den Genen, die runter gehen, sind einige für Wachstum und Entwicklung (z. B. *Sox4*): Die Drüse ist fertig gewachsen und konzentriert sich jetzt auf die Milch.",
    ),
    md(
        """### Bonus: luminal vs basal cells

Look at the second contrast. Which genes make a basal cell a basal cell?""",
        """### Bonus: luminale gegen basale Zellen

Sieh dir den zweiten Kontrast an. Welche Gene machen eine basale Zelle zu einer basalen Zelle?""",
    ),
    exercise(
        ('showTop(fit, "___", n = 15)', 'showTop(fit, "___", n = 15)'),
        ('showTop(fit, "luminal_vs_basal", n = 15)', 'showTop(fit, "luminal_vs_basal", n = 15)'),
    ),
    answer(
        "Negative logFC = higher in **basal** cells: *Krt5* (keratin 5, almost 500 times higher), collagen *Col4a2* and *Postn* (the connective tissue around the ducts), *Dll1* (Notch signalling). Positive = higher in **luminal** cells: *Prlr*, the receptor for the hormone **prolactin**, which tells the luminal cells to make milk, and *Stc2*.",
        "Negativer logFC = höher in **basalen** Zellen: *Krt5* (Keratin 5, fast 500-mal höher), Kollagen *Col4a2* und *Postn* (das Bindegewebe um die Milchgänge), *Dll1* (Notch-Signalweg). Positiv = höher in **luminalen** Zellen: *Prlr*, der Rezeptor für das Hormon **Prolaktin**, das den luminalen Zellen das Signal zur Milchproduktion gibt, und *Stc2*.",
    ),
    md(
        """**Well done!** 🎉 You've done a complete differential expression analysis, the same way researchers do it. Now it's your turn: choose one of the notebooks `02_diy_…`, `03_diy_…` or `04_diy_…` and answer a new research question on your own.""",
        """**Gut gemacht!** 🎉 Du hast eine komplette differenzielle Expressionsanalyse durchgeführt, genau so, wie Forschende es tun. Jetzt bist du dran: Wähle eines der Notebooks `02_diy_…`, `03_diy_…` oder `04_diy_…` und beantworte selbstständig eine neue Forschungsfrage.""",
    ),
]

# ---------------------------------------------------------------------------
# Do-it-yourself notebooks: same steps as the tutorial, students write the code.
# ---------------------------------------------------------------------------
CHECKLIST = md(
    """### Your steps

Work through the same steps as in the tutorial. You can copy code from `01_tutorial_milk.ipynb` and change it: the **column names** and **group names** are different here. Below each step there is a cell for your code, and a hint you can open if you get stuck.

| Step | Functions from the tutorial |
|---|---|
| 1 Look at the data | `DGEList`, `plotLibrarySizes` |
| 2 Define the groups | `dge$samples$group <- …`, `table`, `plotGene` |
| 3 Prepare | `filterByExpr`, `normLibSizes`, `plotDistributions`, `plotSamples` |
| 4 Design and contrast | `model.matrix`, `makeContrasts` |
| 5 Test | `voom`, `lmFit`, `contrasts.fit`, `eBayes`, `decideTests` |
| 6 Interpret | `plotVolcano`, `showTop`, `plotGene` |

If a cell gives an error, read the message, check the spelling of the names, and make sure you ran the cells above.""",
    """### Deine Schritte

Gehe dieselben Schritte wie im Tutorial durch. Du kannst Code aus `01_tutorial_milk.ipynb` kopieren und anpassen: Die **Spaltennamen** und **Gruppennamen** sind hier anders. Unter jedem Schritt gibt es eine Zelle für deinen Code und einen Tipp, den du öffnen kannst, wenn du nicht weiterkommst.

| Schritt | Funktionen aus dem Tutorial |
|---|---|
| 1 Daten ansehen | `DGEList`, `plotLibrarySizes` |
| 2 Gruppen festlegen | `dge$samples$group <- …`, `table`, `plotGene` |
| 3 Vorbereiten | `filterByExpr`, `normLibSizes`, `plotDistributions`, `plotSamples` |
| 4 Design und Kontrast | `model.matrix`, `makeContrasts` |
| 5 Testen | `voom`, `lmFit`, `contrasts.fit`, `eBayes`, `decideTests` |
| 6 Deuten | `plotVolcano`, `showTop`, `plotGene` |

Wenn eine Zelle einen Fehler meldet: Lies die Meldung, prüfe die Schreibweise der Namen und ob du die Zellen darüber ausgeführt hast.""",
)


def step(title, task, solution, hint_text=None, question=None, model_answer=None):
    """One DIY step: heading + task, code cell (empty for students), optional hint and question."""
    cells = [md(*[f"## {t}\n\n{k}" for t, k in zip(title, task)])]
    cells.append(exercise(YOUR_CODE, solution))
    if hint_text:
        cells.append(hint(*hint_text))
    if question:
        cells.append(md(*[f"**{q}**" for q in question]))
        cells.append(answer(*model_answer))
    return cells


def diy(intro, dataset, steps, conclusion, bonus):
    cells = [md(*intro), LANGUAGE_CELL, code(f'data <- loadDataset("{dataset}")\ndata$samples'), CHECKLIST]
    for s in steps:
        cells += step(**s)
    cells += [
        md(
            """## Your conclusion\n\nAnswer the research question in a few sentences: what did you compare, what did you find, and what does it mean? Be ready to show your volcano plot and your answer to the class.""",
            """## Dein Fazit\n\nBeantworte die Forschungsfrage in ein paar Sätzen: Was hast du verglichen, was hast du gefunden, und was bedeutet es? Sei bereit, deinen Vulkan-Plot und deine Antwort der Klasse zu zeigen.""",
        ),
        answer(*conclusion),
    ]
    cells += bonus
    return cells


# --- 02 airway / dexamethasone -------------------------------------------------------------
DEXAMETHASONE = diy(
    intro=(
        """# How does an asthma drug change airway cells?

In **asthma**, the airways are inflamed: they swell, produce mucus and the muscles around them contract, so it's hard to breathe. Many asthma patients take **glucocorticoids**, drugs related to the stress hormone cortisol. One of them is **dexamethasone**. It calms the inflammation, but how?

Researchers (Himes et al. 2014) took **airway smooth muscle cells** from **4 donors** (people). They treated cells of each donor with dexamethasone for 18 hours and left other cells of the same donor untreated: **8 samples**.

### Your research question

> Which genes does dexamethasone switch **on** or **off** in airway muscle cells? Do these genes explain why it calms inflammation?

The data set is called `"airway"`. The genes are human genes.""",
        """# Wie verändert ein Asthma-Medikament die Zellen der Atemwege?

Bei **Asthma** sind die Atemwege entzündet: Sie schwellen an, bilden Schleim und die Muskeln um sie herum ziehen sich zusammen, sodass das Atmen schwerfällt. Viele Asthma-Kranke nehmen **Glucocorticoide**, Medikamente, die mit dem Stresshormon Cortisol verwandt sind. Eines davon ist **Dexamethason**. Es beruhigt die Entzündung, aber wie?

Forschende (Himes et al. 2014) haben **glatte Muskelzellen der Atemwege** von **4 Spendern** (Menschen) genommen. Zellen jedes Spenders wurden 18 Stunden mit Dexamethason behandelt, andere Zellen desselben Spenders blieben unbehandelt: **8 Proben**.

### Deine Forschungsfrage

> Welche Gene schaltet Dexamethason in Muskelzellen der Atemwege **an** oder **aus**? Erklären diese Gene, warum es Entzündungen beruhigt?

Der Datensatz heißt `"airway"`. Die Gene sind menschliche Gene.""",
    ),
    dataset="airway",
    steps=[
        dict(
            title=("1 Look at the data", "1 Daten ansehen"),
            task=(
                "Make a `DGEList` and look at the library sizes. How many genes and samples are there?",
                "Erstelle eine `DGEList` und sieh dir die Bibliotheksgrößen an. Wie viele Gene und Proben gibt es?",
            ),
            solution=(
                'dge <- DGEList(counts = data$counts, samples = data$samples, genes = data$genes)\ndim(dge)\nplotLibrarySizes(dge, colour_by = "treatment")',
                'dge <- DGEList(counts = data$counts, samples = data$samples, genes = data$genes)\ndim(dge)\nplotLibrarySizes(dge, colour_by = "treatment")',
            ),
            hint_text=(
                "Exactly as in the tutorial, with `data` from this notebook. Colour by `\"treatment\"`.",
                "Genau wie im Tutorial, mit `data` aus diesem Notebook. Färbe nach `\"treatment\"`.",
            ),
        ),
        dict(
            title=("2 Define the groups", "2 Gruppen festlegen"),
            task=(
                "Which column of the sample table contains the groups you want to compare? Store it as `dge$samples$group` and count the samples per group. Then check a known glucocorticoid gene: **FKBP5**.",
                "Welche Spalte der Probentabelle enthält die Gruppen, die du vergleichen willst? Speichere sie als `dge$samples$group` und zähle die Proben pro Gruppe. Prüfe dann ein bekanntes Glucocorticoid-Gen: **FKBP5**.",
            ),
            solution=(
                'dge$samples$group <- dge$samples$treatment\ntable(dge$samples$group)\nplotGene(dge, "FKBP5", group_by = "treatment")',
                'dge$samples$group <- dge$samples$treatment\ntable(dge$samples$group)\nplotGene(dge, "FKBP5", group_by = "treatment")',
            ),
            hint_text=(
                "The groups are `untreated` and `dex`, in the column `treatment`: `dge$samples$group <- dge$samples$treatment`. The groups here are already ready, you don't need `paste`.",
                "Die Gruppen sind `untreated` und `dex`, in der Spalte `treatment`: `dge$samples$group <- dge$samples$treatment`. Die Gruppen sind hier schon fertig, du brauchst kein `paste`.",
            ),
        ),
        dict(
            title=("3 Prepare", "3 Vorbereiten"),
            task=(
                "Filter, normalise and draw the sample map. Colour it by treatment, then by donor.",
                "Filtere, normalisiere und zeichne die Probenkarte. Färbe sie nach Behandlung, dann nach Spender.",
            ),
            solution=(
                'keep <- filterByExpr(dge)\ndge <- dge[keep, , keep.lib.sizes = FALSE]\ndge <- normLibSizes(dge)\ndim(dge)\nplotSamples(dge, colour_by = "treatment", label_by = "donor")\nplotSamples(dge, colour_by = "donor", label_by = "treatment")',
                'keep <- filterByExpr(dge)\ndge <- dge[keep, , keep.lib.sizes = FALSE]\ndge <- normLibSizes(dge)\ndim(dge)\nplotSamples(dge, colour_by = "treatment", label_by = "donor")\nplotSamples(dge, colour_by = "donor", label_by = "treatment")',
            ),
            hint_text=(
                "`filterByExpr`, then `dge[keep, , keep.lib.sizes = FALSE]`, then `normLibSizes`, as in part 3 of the tutorial. For the map: `plotSamples(dge, colour_by = \"donor\", label_by = \"treatment\")`.",
                "`filterByExpr`, dann `dge[keep, , keep.lib.sizes = FALSE]`, dann `normLibSizes`, wie in Teil 3 des Tutorials. Für die Karte: `plotSamples(dge, colour_by = \"donor\", label_by = \"treatment\")`.",
            ),
            question=(
                "Question: What separates the samples along distance 1? And along distance 2?",
                "Frage: Was trennt die Proben entlang Richtung 1? Und entlang Richtung 2?",
            ),
            model_answer=(
                "About 13,800 genes remain. Distance 1 (32 %) separates **untreated from dexamethasone**. Distance 2 (28 %) separates the **donors**: the cells of one person resemble each other, treated or not. So the donor has almost as large an effect as the drug!",
                "Etwa 13.800 Gene bleiben übrig. Richtung 1 (32 %) trennt **unbehandelt von Dexamethason**. Richtung 2 (28 %) trennt die **Spender**: Die Zellen einer Person ähneln sich, ob behandelt oder nicht. Der Spender hat also fast so viel Einfluss wie das Medikament!",
            ),
        ),
        dict(
            title=("4 Design and contrast", "4 Design und Kontrast"),
            task=(
                """Here is something new. Each donor gave **both** untreated and treated cells: a **paired** experiment. Since donors differ a lot (step 3), we compare each donor's treated cells with **their own** untreated cells. You tell limma by adding the donor to the design:

```r
design <- model.matrix(~0 + treatment + donor, data = dge$samples)
```

Look at the column names of this design, then write the contrast `dex_vs_untreated`.""",
                """Hier kommt etwas Neues. Jeder Spender hat **sowohl** unbehandelte als auch behandelte Zellen geliefert: ein **gepaartes** Experiment. Da sich die Spender stark unterscheiden (Schritt 3), vergleichen wir die behandelten Zellen jedes Spenders mit **seinen eigenen** unbehandelten Zellen. Das sagst du limma, indem du den Spender ins Design aufnimmst:

```r
design <- model.matrix(~0 + treatment + donor, data = dge$samples)
```

Sieh dir die Spaltennamen dieses Designs an und schreibe dann den Kontrast `dex_vs_untreated`.""",
            ),
            solution=(
                "design <- model.matrix(~0 + treatment + donor, data = dge$samples)\ncolnames(design)\ncontrasts <- makeContrasts(dex_vs_untreated = treatmentdex - treatmentuntreated, levels = design)\ncontrasts",
                "design <- model.matrix(~0 + treatment + donor, data = dge$samples)\ncolnames(design)\ncontrasts <- makeContrasts(dex_vs_untreated = treatmentdex - treatmentuntreated, levels = design)\ncontrasts",
            ),
            hint_text=(
                "The columns are called `treatmentuntreated`, `treatmentdex`, and one column per donor (except the first). The donor columns only soak up the donor differences; the contrast uses the two treatment columns: `makeContrasts(dex_vs_untreated = treatmentdex - treatmentuntreated, levels = design)`.",
                "Die Spalten heißen `treatmentuntreated`, `treatmentdex` und je eine Spalte pro Spender (außer dem ersten). Die Spender-Spalten fangen nur die Unterschiede zwischen den Spendern auf; der Kontrast benutzt die beiden Behandlungs-Spalten: `makeContrasts(dex_vs_untreated = treatmentdex - treatmentuntreated, levels = design)`.",
            ),
        ),
        dict(
            title=("5 Test", "5 Testen"),
            task=(
                "Run `voom`, `lmFit`, `contrasts.fit` and `eBayes`, and count the significant genes.",
                "Führe `voom`, `lmFit`, `contrasts.fit` und `eBayes` aus und zähle die signifikanten Gene.",
            ),
            solution=(
                "v <- voom(dge, design, plot = TRUE)\nfit <- lmFit(v, design)\nfit <- contrasts.fit(fit, contrasts)\nfit <- eBayes(fit)\nsummary(decideTests(fit))",
                "v <- voom(dge, design, plot = TRUE)\nfit <- lmFit(v, design)\nfit <- contrasts.fit(fit, contrasts)\nfit <- eBayes(fit)\nsummary(decideTests(fit))",
            ),
            hint_text=(
                "Copy the two cells from part 5 of the tutorial; they work unchanged.",
                "Kopiere die beiden Zellen aus Teil 5 des Tutorials; sie funktionieren unverändert.",
            ),
            question=("Question: How many genes go up, how many down?", "Frage: Wie viele Gene gehen hoch, wie viele runter?"),
            model_answer=(
                "About **2,300 up** and **2,260 down** (adjusted p < 0.05).",
                "Etwa **2.300 hoch** und **2.260 runter** (adjustiertes p < 0,05).",
            ),
        ),
        dict(
            title=("6 Interpret", "6 Deuten"),
            task=(
                "Draw the volcano plot and list the top genes going up and down. Look up some of them. Which ones have to do with **inflammation** or the **immune system**?",
                "Zeichne den Vulkan-Plot und liste die Top-Gene auf, die hoch und runter gehen. Schlage einige davon nach. Welche haben mit **Entzündung** oder dem **Immunsystem** zu tun?",
            ),
            solution=(
                'plotVolcano(fit, "dex_vs_untreated")\nshowTop(fit, "dex_vs_untreated", n = 20, direction = "up")\nshowTop(fit, "dex_vs_untreated", n = 20, direction = "down")\nplotGene(dge, "TSC22D3", group_by = "treatment")',
                'plotVolcano(fit, "dex_vs_untreated")\nshowTop(fit, "dex_vs_untreated", n = 20, direction = "up")\nshowTop(fit, "dex_vs_untreated", n = 20, direction = "down")\nplotGene(dge, "TSC22D3", group_by = "treatment")',
            ),
            hint_text=(
                """Look up genes on [GeneCards](https://www.genecards.org). Some well-known glucocorticoid genes to check with `plotGene`: **DUSP1**, **TSC22D3** (also called GILZ, "glucocorticoid-induced leucine zipper"), **KLF15**, **PER1**, **ZBTB16**. Among the genes going down, look for **VCAM1** and **CXCL12**.""",
                """Schlage Gene auf [GeneCards](https://www.genecards.org) nach. Einige bekannte Glucocorticoid-Gene, die du mit `plotGene` prüfen kannst: **DUSP1**, **TSC22D3** (auch GILZ genannt, „glucocorticoid-induced leucine zipper“), **KLF15**, **PER1**, **ZBTB16**. Bei den Genen, die runter gehen, achte auf **VCAM1** und **CXCL12**.""",
            ),
        ),
    ],
    conclusion=(
        "We compared airway smooth muscle cells of 4 donors with and without dexamethasone, using a paired design (donor in the model). About 2,300 genes went up and 2,260 down. Up: classic glucocorticoid response genes such as *DUSP1*, *TSC22D3* (GILZ), *KLF15*, *PER1*, *FKBP5* and *ZBTB16*. DUSP1 and GILZ are **brakes of inflammation**: DUSP1 switches off inflammatory signalling, GILZ blocks the inflammatory master switch NF-κB. Down: *VCAM1*, which lets immune cells stick to tissue, and the chemokine *CXCL12*, which attracts immune cells. So dexamethasone turns on anti-inflammatory genes and turns off genes that call immune cells in: that explains how it calms the airways.",
        "Wir haben glatte Muskelzellen der Atemwege von 4 Spendern mit und ohne Dexamethason verglichen, mit einem gepaarten Design (Spender im Modell). Etwa 2.300 Gene gingen hoch und 2.260 runter. Hoch: klassische Glucocorticoid-Gene wie *DUSP1*, *TSC22D3* (GILZ), *KLF15*, *PER1*, *FKBP5* und *ZBTB16*. DUSP1 und GILZ sind **Bremsen der Entzündung**: DUSP1 schaltet Entzündungssignale ab, GILZ blockiert den Hauptschalter der Entzündung, NF-κB. Runter: *VCAM1*, an dem Immunzellen im Gewebe festhalten, und das Chemokin *CXCL12*, das Immunzellen anlockt. Dexamethason schaltet also entzündungshemmende Gene an und Gene, die Immunzellen herbeirufen, aus: Das erklärt, wie es die Atemwege beruhigt.",
    ),
    bonus=[
        md(
            """## Bonus: does the paired design matter?

Repeat steps 4 and 5 **without** the donor: `model.matrix(~0 + treatment, data = dge$samples)`. Compare the number of significant genes. Why is it different?""",
            """## Bonus: Macht das gepaarte Design einen Unterschied?

Wiederhole die Schritte 4 und 5 **ohne** den Spender: `model.matrix(~0 + treatment, data = dge$samples)`. Vergleiche die Zahl der signifikanten Gene. Warum ist sie anders?""",
        ),
        exercise(
            YOUR_CODE,
            (
                "design0 <- model.matrix(~0 + treatment, data = dge$samples)\ncontrasts0 <- makeContrasts(dex_vs_untreated = treatmentdex - treatmentuntreated, levels = design0)\nfit0 <- eBayes(contrasts.fit(lmFit(voom(dge, design0), design0), contrasts0))\nsummary(decideTests(fit0))",
                "design0 <- model.matrix(~0 + treatment, data = dge$samples)\ncontrasts0 <- makeContrasts(dex_vs_untreated = treatmentdex - treatmentuntreated, levels = design0)\nfit0 <- eBayes(contrasts.fit(lmFit(voom(dge, design0), design0), contrasts0))\nsummary(decideTests(fit0))",
            ),
        ),
        answer(
            "Without the donor only about **1,850** genes are significant instead of about **4,560**. Without the donor in the model, the differences between donors count as \"noise\", so the noise looks bigger and fewer changes are convincing. With the paired design, limma compares each donor with themself, and the donor differences are removed.",
            "Ohne den Spender sind nur etwa **1.850** Gene signifikant statt etwa **4.560**. Ohne den Spender im Modell zählen die Unterschiede zwischen den Spendern als „Rauschen“, das Rauschen wirkt also größer und weniger Veränderungen sind überzeugend. Mit dem gepaarten Design vergleicht limma jeden Spender mit sich selbst, und die Spender-Unterschiede fallen weg.",
        ),
    ],
)

# --- 03 pasilla ----------------------------------------------------------------------------
PASILLA = diy(
    intro=(
        """# What happens when a fly cell loses the protein *pasilla*?

Most genes are not read in one piece: the cell cuts the mRNA and joins the pieces together, called **splicing**. Proteins that bind RNA decide how it's cut. One of them, in the fruit fly *Drosophila melanogaster*, is called **pasilla**. (Fly genes often have funny names; in the data, the pasilla gene is called **`ps`**.)

Researchers (Brooks et al. 2011) switched pasilla off in fly cells with **RNA interference** (**knockdown**): they added RNA that makes the cell destroy the pasilla mRNA. They sequenced **4 control** and **3 knockdown** samples. Some samples were sequenced with an older method (**single-end**: each RNA piece read from one side) and some with a newer one (**paired-end**: read from both sides).

### Your research question

> Did the knockdown work? And which genes change when pasilla is missing?

The data set is called `"pasilla"`.""",
        """# Was passiert, wenn eine Fliegenzelle das Protein *pasilla* verliert?

Die meisten Gene werden nicht am Stück abgelesen: Die Zelle schneidet die mRNA und fügt die Stücke wieder zusammen, das nennt man **Spleißen**. Proteine, die an RNA binden, entscheiden, wie geschnitten wird. Eines davon heißt bei der Fruchtfliege *Drosophila melanogaster* **pasilla**. (Fliegengene haben oft lustige Namen; in den Daten heißt das pasilla-Gen **`ps`**.)

Forschende (Brooks et al. 2011) haben pasilla in Fliegenzellen mit **RNA-Interferenz** ausgeschaltet (**Knockdown**): Sie haben RNA hinzugefügt, die die Zelle dazu bringt, die pasilla-mRNA zu zerstören. Sequenziert wurden **4 Kontroll-** und **3 Knockdown**-Proben. Manche Proben wurden mit einer älteren Methode sequenziert (**single-end**: jedes RNA-Stück von einer Seite gelesen), manche mit einer neueren (**paired-end**: von beiden Seiten gelesen).

### Deine Forschungsfrage

> Hat der Knockdown funktioniert? Und welche Gene verändern sich, wenn pasilla fehlt?

Der Datensatz heißt `"pasilla"`.""",
    ),
    dataset="pasilla",
    steps=[
        dict(
            title=("1 Look at the data", "1 Daten ansehen"),
            task=(
                "Make a `DGEList` and look at the library sizes. Colour them by `library`. What do you notice?",
                "Erstelle eine `DGEList` und sieh dir die Bibliotheksgrößen an. Färbe sie nach `library`. Was fällt dir auf?",
            ),
            solution=(
                'dge <- DGEList(counts = data$counts, samples = data$samples, genes = data$genes)\ndim(dge)\nplotLibrarySizes(dge, colour_by = "library")',
                'dge <- DGEList(counts = data$counts, samples = data$samples, genes = data$genes)\ndim(dge)\nplotLibrarySizes(dge, colour_by = "library")',
            ),
            hint_text=(
                "As in the tutorial: `DGEList(counts = data$counts, samples = data$samples, genes = data$genes)`.",
                "Wie im Tutorial: `DGEList(counts = data$counts, samples = data$samples, genes = data$genes)`.",
            ),
            question=("Question: How different are the library sizes?", "Frage: Wie unterschiedlich sind die Bibliotheksgrößen?"),
            model_answer=(
                "Between about **8 and 22 million** reads, almost 3 times as many in the largest as in the smallest. The single-end samples have more reads. That's no problem: normalisation takes care of it.",
                "Zwischen etwa **8 und 22 Millionen** Reads, fast 3-mal so viele in der größten wie in der kleinsten. Die Single-end-Proben haben mehr Reads. Das ist kein Problem: Die Normalisierung gleicht es aus.",
            ),
        ),
        dict(
            title=("2 Groups, and a positive control", "2 Gruppen und eine Positivkontrolle"),
            task=(
                "Set the groups (column `condition`). Then check first of all whether the knockdown worked: look at the gene `ps` itself. Such a check, where you know the expected answer, is called a **positive control**.",
                "Lege die Gruppen fest (Spalte `condition`). Prüfe dann als Allererstes, ob der Knockdown funktioniert hat: Sieh dir das Gen `ps` selbst an. So eine Prüfung, bei der man die erwartete Antwort kennt, heißt **Positivkontrolle**.",
            ),
            solution=(
                'dge$samples$group <- dge$samples$condition\ntable(dge$samples$group)\nplotGene(dge, "ps", group_by = "condition")',
                'dge$samples$group <- dge$samples$condition\ntable(dge$samples$group)\nplotGene(dge, "ps", group_by = "condition")',
            ),
            hint_text=(
                '`dge$samples$group <- dge$samples$condition`, then `plotGene(dge, "ps", group_by = "condition")`.',
                '`dge$samples$group <- dge$samples$condition`, dann `plotGene(dge, "ps", group_by = "condition")`.',
            ),
        ),
        dict(
            title=("3 Prepare", "3 Vorbereiten"),
            task=(
                "Filter, normalise and draw the sample map: colour it by `condition`, then by `library`.",
                "Filtere, normalisiere und zeichne die Probenkarte: färbe sie nach `condition`, dann nach `library`.",
            ),
            solution=(
                'keep <- filterByExpr(dge)\ndge <- dge[keep, , keep.lib.sizes = FALSE]\ndge <- normLibSizes(dge)\ndim(dge)\nplotSamples(dge, colour_by = "condition", label_by = "library")\nplotSamples(dge, colour_by = "library", label_by = "condition")',
                'keep <- filterByExpr(dge)\ndge <- dge[keep, , keep.lib.sizes = FALSE]\ndge <- normLibSizes(dge)\ndim(dge)\nplotSamples(dge, colour_by = "condition", label_by = "library")\nplotSamples(dge, colour_by = "library", label_by = "condition")',
            ),
            hint_text=(
                "Same as part 3 of the tutorial. For the second map: `plotSamples(dge, colour_by = \"library\", label_by = \"condition\")`.",
                "Wie Teil 3 des Tutorials. Für die zweite Karte: `plotSamples(dge, colour_by = \"library\", label_by = \"condition\")`.",
            ),
            question=(
                "Question: What separates the samples along distance 1 and along distance 2?",
                "Frage: Was trennt die Proben entlang Richtung 1 und entlang Richtung 2?",
            ),
            model_answer=(
                "Distance 1 (41 %) separates **control from knockdown**. Distance 2 (30 %) separates **single-end from paired-end** samples. The sequencing method changes the counts a bit, even though the biology is the same. Such a technical difference is called a **batch effect**.",
                "Richtung 1 (41 %) trennt **Kontrolle von Knockdown**. Richtung 2 (30 %) trennt **Single-end- von Paired-end-Proben**. Die Sequenziermethode verändert die Counts etwas, obwohl die Biologie dieselbe ist. So einen technischen Unterschied nennt man **Batch-Effekt**.",
            ),
        ),
        dict(
            title=("4 Design and contrast", "4 Design und Kontrast"),
            task=(
                """The batch effect from step 3 is a problem: it adds variation that has nothing to do with pasilla. You can tell limma about it by putting the library type into the design:

```r
design <- model.matrix(~0 + condition + library, data = dge$samples)
```

Look at the column names, then write the contrast `knockdown_vs_control`.""",
                """Der Batch-Effekt aus Schritt 3 ist ein Problem: Er bringt Schwankungen hinein, die nichts mit pasilla zu tun haben. Du kannst limma davon erzählen, indem du die Bibliotheksart ins Design aufnimmst:

```r
design <- model.matrix(~0 + condition + library, data = dge$samples)
```

Sieh dir die Spaltennamen an und schreibe dann den Kontrast `knockdown_vs_control`.""",
            ),
            solution=(
                "design <- model.matrix(~0 + condition + library, data = dge$samples)\ncolnames(design)\ncontrasts <- makeContrasts(knockdown_vs_control = conditionknockdown - conditioncontrol, levels = design)\ncontrasts",
                "design <- model.matrix(~0 + condition + library, data = dge$samples)\ncolnames(design)\ncontrasts <- makeContrasts(knockdown_vs_control = conditionknockdown - conditioncontrol, levels = design)\ncontrasts",
            ),
            hint_text=(
                "The columns are `conditioncontrol`, `conditionknockdown` and `librarypaired_end`. The contrast: `conditionknockdown - conditioncontrol`.",
                "Die Spalten heißen `conditioncontrol`, `conditionknockdown` und `librarypaired_end`. Der Kontrast: `conditionknockdown - conditioncontrol`.",
            ),
        ),
        dict(
            title=("5 Test", "5 Testen"),
            task=("Test every gene and count the significant ones.", "Teste jedes Gen und zähle die signifikanten."),
            solution=(
                "v <- voom(dge, design, plot = TRUE)\nfit <- lmFit(v, design)\nfit <- contrasts.fit(fit, contrasts)\nfit <- eBayes(fit)\nsummary(decideTests(fit))",
                "v <- voom(dge, design, plot = TRUE)\nfit <- lmFit(v, design)\nfit <- contrasts.fit(fit, contrasts)\nfit <- eBayes(fit)\nsummary(decideTests(fit))",
            ),
            hint_text=(
                "The cells from part 5 of the tutorial work unchanged.",
                "Die Zellen aus Teil 5 des Tutorials funktionieren unverändert.",
            ),
            question=("Question: How many genes go up, how many down?", "Frage: Wie viele Gene gehen hoch, wie viele runter?"),
            model_answer=(
                "About **660 up** and **600 down**, of about 7,900 tested genes.",
                "Etwa **660 hoch** und **600 runter**, von etwa 7.900 getesteten Genen.",
            ),
        ),
        dict(
            title=("6 Interpret", "6 Deuten"),
            task=(
                "Draw the volcano plot and list the top genes. Where is `ps` itself? Look up some of the other genes on [FlyBase](https://flybase.org), the database for fly genes.",
                "Zeichne den Vulkan-Plot und liste die Top-Gene auf. Wo ist `ps` selbst? Schlage einige der anderen Gene auf [FlyBase](https://flybase.org) nach, der Datenbank für Fliegengene.",
            ),
            solution=(
                'plotVolcano(fit, "knockdown_vs_control")\nshowTop(fit, "knockdown_vs_control", n = 15, direction = "up")\nshowTop(fit, "knockdown_vs_control", n = 15, direction = "down")\ntop <- topTable(fit, coef = "knockdown_vs_control", number = Inf)\ntop[top$symbol == "ps", c("symbol", "logFC", "adj.P.Val")]',
                'plotVolcano(fit, "knockdown_vs_control")\nshowTop(fit, "knockdown_vs_control", n = 15, direction = "up")\nshowTop(fit, "knockdown_vs_control", n = 15, direction = "down")\ntop <- topTable(fit, coef = "knockdown_vs_control", number = Inf)\ntop[top$symbol == "ps", c("symbol", "logFC", "adj.P.Val")]',
            ),
            hint_text=(
                """To find one gene in the full results table: `top <- topTable(fit, coef = "knockdown_vs_control", number = Inf)`, then `top[top$symbol == "ps", ]`. Many fly genes are only called `CG…` + a number: nobody knows yet what they do!""",
                """Um ein Gen in der vollständigen Ergebnistabelle zu finden: `top <- topTable(fit, coef = "knockdown_vs_control", number = Inf)`, dann `top[top$symbol == "ps", ]`. Viele Fliegengene heißen nur `CG…` + eine Nummer: Niemand weiß bisher, was sie tun!""",
            ),
        ),
    ],
    conclusion=(
        "We compared 3 pasilla knockdown samples with 4 controls, with the library type in the design to remove the batch effect. The knockdown worked: `ps` itself is about **3.7 times lower** (logFC ≈ −1.9). About 660 genes went up and 600 down. Among the strongest changes are *Ant2* and *sesB*, two versions of the same mitochondrial transporter (one up, one down), and *Kal1*, *Hml* and *SPARC*. Many changed genes are uncharacterised (`CG…`). Because pasilla controls splicing, many of these genes may be its targets: this is the kind of list researchers start from to find out what an unknown protein does.",
        "Wir haben 3 pasilla-Knockdown-Proben mit 4 Kontrollen verglichen, mit der Bibliotheksart im Design, um den Batch-Effekt zu entfernen. Der Knockdown hat funktioniert: `ps` selbst ist etwa **3,7-mal niedriger** (logFC ≈ −1,9). Etwa 660 Gene gingen hoch und 600 runter. Zu den stärksten Veränderungen gehören *Ant2* und *sesB*, zwei Versionen desselben Transporters in den Mitochondrien (einer hoch, einer runter), sowie *Kal1*, *Hml* und *SPARC*. Viele veränderte Gene sind noch unerforscht (`CG…`). Da pasilla das Spleißen steuert, könnten viele dieser Gene seine Ziele sein: Mit so einer Liste beginnen Forschende, um herauszufinden, was ein unbekanntes Protein tut.",
    ),
    bonus=[
        md(
            """## Bonus: what if you ignore the batch effect?

Repeat steps 4 and 5 with `model.matrix(~0 + condition, data = dge$samples)` and compare the number of significant genes.""",
            """## Bonus: Was, wenn du den Batch-Effekt ignorierst?

Wiederhole die Schritte 4 und 5 mit `model.matrix(~0 + condition, data = dge$samples)` und vergleiche die Zahl der signifikanten Gene.""",
        ),
        exercise(
            YOUR_CODE,
            (
                "design0 <- model.matrix(~0 + condition, data = dge$samples)\ncontrasts0 <- makeContrasts(knockdown_vs_control = conditionknockdown - conditioncontrol, levels = design0)\nfit0 <- eBayes(contrasts.fit(lmFit(voom(dge, design0), design0), contrasts0))\nsummary(decideTests(fit0))",
                "design0 <- model.matrix(~0 + condition, data = dge$samples)\ncontrasts0 <- makeContrasts(knockdown_vs_control = conditionknockdown - conditioncontrol, levels = design0)\nfit0 <- eBayes(contrasts.fit(lmFit(voom(dge, design0), design0), contrasts0))\nsummary(decideTests(fit0))",
            ),
        ),
        answer(
            "Without the library type only about **670** genes are significant instead of about **1,260**: the batch effect counts as noise and hides real changes. Good experiments avoid batch effects, and good analyses include the ones that can't be avoided.",
            "Ohne die Bibliotheksart sind nur etwa **670** Gene signifikant statt etwa **1.260**: Der Batch-Effekt zählt als Rauschen und verdeckt echte Veränderungen. Gute Experimente vermeiden Batch-Effekte, und gute Analysen berücksichtigen die, die sich nicht vermeiden lassen.",
        ),
    ],
)

# --- 04 breast cancer ----------------------------------------------------------------------
CANCER = diy(
    intro=(
        """# What is different in breast cancer?

**Breast cancer** is the most common cancer in women. In the project **The Cancer Genome Atlas (TCGA)**, researchers sequenced tumours of over 1,000 patients, and for some of them also **normal breast tissue** from near the tumour. All this data is public.

You get the data of **10 patients**: from each, one sample of the tumour and one of normal tissue, so **20 samples**. Unlike mice or cells in a lab, these are real people of different ages, with different kinds of tumours. Expect the data to be messier!

### Your research question

> Which genes are different between breast tumours and normal breast tissue of the same patients? What do they tell you about what cancer cells do?

The data set is called `"cancer"`.""",
        """# Was ist bei Brustkrebs anders?

**Brustkrebs** ist die häufigste Krebsart bei Frauen. Im Projekt **The Cancer Genome Atlas (TCGA)** haben Forschende die Tumoren von über 1.000 Patientinnen sequenziert, und bei einigen auch **normales Brustgewebe** aus der Nähe des Tumors. Alle diese Daten sind öffentlich.

Du bekommst die Daten von **10 Patientinnen**: von jeder eine Probe aus dem Tumor und eine aus normalem Gewebe, also **20 Proben**. Anders als Mäuse oder Zellen im Labor sind das echte Menschen verschiedenen Alters mit verschiedenen Arten von Tumoren. Rechne damit, dass die Daten unordentlicher sind!

### Deine Forschungsfrage

> Welche Gene unterscheiden sich zwischen Brusttumoren und normalem Brustgewebe derselben Patientinnen? Was verraten sie darüber, was Krebszellen tun?

Der Datensatz heißt `"cancer"`.""",
    ),
    dataset="cancer",
    steps=[
        dict(
            title=("1 Look at the data", "1 Daten ansehen"),
            task=("Make a `DGEList` and look at the library sizes.", "Erstelle eine `DGEList` und sieh dir die Bibliotheksgrößen an."),
            solution=(
                'dge <- DGEList(counts = data$counts, samples = data$samples, genes = data$genes)\ndim(dge)\nplotLibrarySizes(dge, colour_by = "tissue")',
                'dge <- DGEList(counts = data$counts, samples = data$samples, genes = data$genes)\ndim(dge)\nplotLibrarySizes(dge, colour_by = "tissue")',
            ),
            hint_text=("As in the tutorial. Colour by `\"tissue\"`.", "Wie im Tutorial. Färbe nach `\"tissue\"`."),
        ),
        dict(
            title=("2 Define the groups", "2 Gruppen festlegen"),
            task=(
                "Set the groups (column `tissue`). Then look at a gene that every growing tissue needs: **MKI67** is only made by cells that are **dividing**.",
                "Lege die Gruppen fest (Spalte `tissue`). Sieh dir dann ein Gen an, das jedes wachsende Gewebe braucht: **MKI67** wird nur von Zellen hergestellt, die sich **teilen**.",
            ),
            solution=(
                'dge$samples$group <- dge$samples$tissue\ntable(dge$samples$group)\nplotGene(dge, "MKI67", group_by = "tissue")',
                'dge$samples$group <- dge$samples$tissue\ntable(dge$samples$group)\nplotGene(dge, "MKI67", group_by = "tissue")',
            ),
            hint_text=(
                '`dge$samples$group <- dge$samples$tissue`, then `plotGene(dge, "MKI67", group_by = "tissue")`.',
                '`dge$samples$group <- dge$samples$tissue`, dann `plotGene(dge, "MKI67", group_by = "tissue")`.',
            ),
        ),
        dict(
            title=("3 Prepare", "3 Vorbereiten"),
            task=(
                "Filter, normalise and draw the sample map, coloured by tissue and labelled by patient.",
                "Filtere, normalisiere und zeichne die Probenkarte, gefärbt nach Gewebe und beschriftet mit der Patientin.",
            ),
            solution=(
                'keep <- filterByExpr(dge)\ndge <- dge[keep, , keep.lib.sizes = FALSE]\ndge <- normLibSizes(dge)\ndim(dge)\nplotSamples(dge, colour_by = "tissue", label_by = "patient")',
                'keep <- filterByExpr(dge)\ndge <- dge[keep, , keep.lib.sizes = FALSE]\ndge <- normLibSizes(dge)\ndim(dge)\nplotSamples(dge, colour_by = "tissue", label_by = "patient")',
            ),
            hint_text=(
                "As part 3 of the tutorial, with `plotSamples(dge, colour_by = \"tissue\", label_by = \"patient\")`.",
                "Wie Teil 3 des Tutorials, mit `plotSamples(dge, colour_by = \"tissue\", label_by = \"patient\")`.",
            ),
            question=(
                "Question: Are the normal samples and the tumour samples separated? Which group is more spread out, and why could that be?",
                "Frage: Sind die normalen Proben und die Tumorproben getrennt? Welche Gruppe ist stärker verstreut, und woran könnte das liegen?",
            ),
            model_answer=(
                "Distance 1 (29 %) mostly separates **normal tissue (left)** from **tumours (right)**. The normal samples lie close together, the tumours are spread widely: every tumour is different (different mutations, different types of breast cancer). One tumour (AC_A2FF) lies close to the normal samples; it may contain a lot of normal tissue.",
                "Richtung 1 (29 %) trennt überwiegend **normales Gewebe (links)** von **Tumoren (rechts)**. Die normalen Proben liegen nah beieinander, die Tumoren sind weit verstreut: Jeder Tumor ist anders (andere Mutationen, andere Arten von Brustkrebs). Ein Tumor (AC_A2FF) liegt nah bei den normalen Proben; vielleicht enthält er viel normales Gewebe.",
            ),
        ),
        dict(
            title=("4 Design and contrast", "4 Design und Kontrast"),
            task=(
                "Each patient gave a tumour **and** a normal sample: what kind of experiment is that? Think back to what you know about **paired** designs (or read the hint), then write the design and the contrast `tumour_vs_normal`.",
                "Jede Patientin hat eine Tumor- **und** eine Normalprobe geliefert: Was für ein Experiment ist das? Denk daran, was du über **gepaarte** Designs weißt (oder lies den Tipp), und schreibe dann das Design und den Kontrast `tumour_vs_normal`.",
            ),
            solution=(
                "design <- model.matrix(~0 + tissue + patient, data = dge$samples)\ncolnames(design)\ncontrasts <- makeContrasts(tumour_vs_normal = tissuetumour - tissuenormal, levels = design)",
                "design <- model.matrix(~0 + tissue + patient, data = dge$samples)\ncolnames(design)\ncontrasts <- makeContrasts(tumour_vs_normal = tissuetumour - tissuenormal, levels = design)",
            ),
            hint_text=(
                "A paired design: add the patient to the design so each tumour is compared with the normal tissue of the **same** patient: `model.matrix(~0 + tissue + patient, data = dge$samples)`. The contrast uses the columns `tissuetumour` and `tissuenormal`.",
                "Ein gepaartes Design: Nimm die Patientin ins Design auf, damit jeder Tumor mit dem Normalgewebe **derselben** Patientin verglichen wird: `model.matrix(~0 + tissue + patient, data = dge$samples)`. Der Kontrast benutzt die Spalten `tissuetumour` und `tissuenormal`.",
            ),
        ),
        dict(
            title=("5 Test", "5 Testen"),
            task=("Test every gene and count the significant ones.", "Teste jedes Gen und zähle die signifikanten."),
            solution=(
                "v <- voom(dge, design, plot = TRUE)\nfit <- lmFit(v, design)\nfit <- contrasts.fit(fit, contrasts)\nfit <- eBayes(fit)\nsummary(decideTests(fit))",
                "v <- voom(dge, design, plot = TRUE)\nfit <- lmFit(v, design)\nfit <- contrasts.fit(fit, contrasts)\nfit <- eBayes(fit)\nsummary(decideTests(fit))",
            ),
            hint_text=("The cells from part 5 of the tutorial work unchanged.", "Die Zellen aus Teil 5 des Tutorials funktionieren unverändert."),
            question=(
                "Question: How many genes are significant? Is that a list you can still read through?",
                "Frage: Wie viele Gene sind signifikant? Ist das eine Liste, die man noch durchlesen kann?",
            ),
            model_answer=(
                "About **2,100 up** and **2,350 down**: far too many to read. We need to **prioritise**: look at the strongest changes first (volcano plot, `showTop`), or ask for genes that change by a lot (see the bonus).",
                "Etwa **2.100 hoch** und **2.350 runter**: viel zu viele zum Durchlesen. Wir müssen **Prioritäten setzen**: zuerst die stärksten Veränderungen ansehen (Vulkan-Plot, `showTop`) oder nach Genen fragen, die sich sehr stark ändern (siehe Bonus).",
            ),
        ),
        dict(
            title=("6 Interpret", "6 Deuten"),
            task=(
                "Draw the volcano plot and list the top genes going up and down. Look some of them up on [GeneCards](https://www.genecards.org). Try to sort them into a few **themes**.",
                "Zeichne den Vulkan-Plot und liste die Top-Gene auf, die hoch und runter gehen. Schlage einige auf [GeneCards](https://www.genecards.org) nach. Versuche, sie in ein paar **Themen** zu sortieren.",
            ),
            solution=(
                'plotVolcano(fit, "tumour_vs_normal")\nshowTop(fit, "tumour_vs_normal", n = 20, direction = "up")\nshowTop(fit, "tumour_vs_normal", n = 20, direction = "down")\nplotGene(dge, "ADIPOQ", group_by = "tissue")',
                'plotVolcano(fit, "tumour_vs_normal")\nshowTop(fit, "tumour_vs_normal", n = 20, direction = "up")\nshowTop(fit, "tumour_vs_normal", n = 20, direction = "down")\nplotGene(dge, "ADIPOQ", group_by = "tissue")',
            ),
            hint_text=(
                """Possible themes: **cell division** (look for kinesins *KIF…*, *ASPM*, *NUF2*, *NEK2*, *TOP2A*), **remodelling the tissue around the tumour** (collagens *COL…*, matrix metalloproteinases *MMP…*), and on the "down" side: what is normal breast tissue mostly made of? Try `plotGene` with **ADIPOQ** and **LEP**.""",
                """Mögliche Themen: **Zellteilung** (achte auf Kinesine *KIF…*, *ASPM*, *NUF2*, *NEK2*, *TOP2A*), **Umbau des Gewebes um den Tumor** (Kollagene *COL…*, Matrix-Metalloproteinasen *MMP…*), und auf der „runter“-Seite: Woraus besteht normales Brustgewebe vor allem? Probiere `plotGene` mit **ADIPOQ** und **LEP**.""",
            ),
        ),
    ],
    conclusion=(
        "We compared tumour and normal breast tissue of 10 patients with a paired design. About 2,100 genes went up and 2,350 down. Up: many genes for **cell division** (*NUF2*, *ASPM*, *KIF4A*, *NEK2*, *MKI67*, *TOP2A*): cancer cells divide uncontrollably. Also up: genes that **rebuild the tissue around the tumour** (*COL10A1*, *MMP11*, *INHBA*), which helps tumours grow and invade. Down: genes of **fat tissue** (*ADIPOQ*, *LEP*), because normal breast tissue is mostly fat and the tumour pushes it aside, and genes of the normal milk ducts (*SCGB3A1*, *MME*). Genes like *ESR1* (oestrogen receptor) and *ERBB2* (HER2) vary strongly between patients: breast cancer is not one disease, which is why treatment is chosen per patient.",
        "Wir haben Tumor- und normales Brustgewebe von 10 Patientinnen mit einem gepaarten Design verglichen. Etwa 2.100 Gene gingen hoch und 2.350 runter. Hoch: viele Gene für die **Zellteilung** (*NUF2*, *ASPM*, *KIF4A*, *NEK2*, *MKI67*, *TOP2A*): Krebszellen teilen sich unkontrolliert. Außerdem hoch: Gene, die das **Gewebe um den Tumor umbauen** (*COL10A1*, *MMP11*, *INHBA*), was Tumoren beim Wachsen und Eindringen hilft. Runter: Gene des **Fettgewebes** (*ADIPOQ*, *LEP*), weil normales Brustgewebe größtenteils aus Fett besteht und der Tumor es verdrängt, und Gene der normalen Milchgänge (*SCGB3A1*, *MME*). Gene wie *ESR1* (Östrogenrezeptor) und *ERBB2* (HER2) unterscheiden sich stark zwischen den Patientinnen: Brustkrebs ist nicht eine einzige Krankheit, deshalb wird die Behandlung für jede Patientin einzeln ausgewählt.",
    ),
    bonus=[
        md(
            """## Bonus 1: only the big changes

With thousands of significant genes, you can ask a stricter question: which genes change **at least 4-fold** (log fold change of 2)? `treat` tests exactly that.""",
            """## Bonus 1: Nur die großen Veränderungen

Bei Tausenden signifikanten Genen kannst du eine strengere Frage stellen: Welche Gene ändern sich **mindestens 4-fach** (log Fold Change von 2)? `treat` testet genau das.""",
        ),
        code(
            'fit_strict <- treat(fit, lfc = 2)\nsummary(decideTests(fit_strict))\nshowTop(fit_strict, "tumour_vs_normal", n = 30)',
        ),
        md(
            """## Bonus 2: every tumour is different

Look at **ESR1** (the oestrogen receptor) and **ERBB2** (HER2) with `plotGene`. Doctors test these two in every breast tumour. What do you see?""",
            """## Bonus 2: Jeder Tumor ist anders

Sieh dir **ESR1** (den Östrogenrezeptor) und **ERBB2** (HER2) mit `plotGene` an. Ärztinnen und Ärzte testen diese beiden bei jedem Brusttumor. Was siehst du?""",
        ),
        exercise(
            YOUR_CODE,
            (
                'plotGene(dge, "ESR1", group_by = "tissue")\nplotGene(dge, "ERBB2", group_by = "tissue")',
                'plotGene(dge, "ESR1", group_by = "tissue")\nplotGene(dge, "ERBB2", group_by = "tissue")',
            ),
        ),
        answer(
            "With `treat` only about **28** genes remain: a short list of the biggest changes. ESR1 is high in some tumours and very low in others; on average there is no significant difference. ERBB2 is very high in a few tumours only. These patients have different **types** of breast cancer: oestrogen-receptor-positive tumours can be treated with anti-hormone drugs, HER2-positive ones with antibodies against HER2. A comparison of averages can hide such differences between patients.",
            "Mit `treat` bleiben nur etwa **28** Gene übrig: eine kurze Liste der größten Veränderungen. ESR1 ist in manchen Tumoren hoch und in anderen sehr niedrig; im Mittel gibt es keinen signifikanten Unterschied. ERBB2 ist nur in wenigen Tumoren sehr hoch. Diese Patientinnen haben verschiedene **Arten** von Brustkrebs: Östrogenrezeptor-positive Tumoren lassen sich mit Anti-Hormon-Medikamenten behandeln, HER2-positive mit Antikörpern gegen HER2. Ein Vergleich von Mittelwerten kann solche Unterschiede zwischen Patientinnen verdecken.",
        ),
    ],
)

NOTEBOOKS = {
    "00_welcome": WELCOME,
    "01_tutorial_milk": TUTORIAL + [SOURCES],
    "02_diy_dexamethasone": DEXAMETHASONE + [SOURCES_SHORT],
    "03_diy_pasilla": PASILLA + [SOURCES_SHORT],
    "04_diy_cancer": CANCER + [SOURCES_SHORT],
}


def to_cells(spec, lang, solutions):
    cells = []
    for item in spec:
        kind = item["kind"]
        if kind == "md":
            cells.append(("markdown", item[lang]))
        elif kind == "code":
            cells.append(("code", item[lang]))
        elif kind == "exercise":
            pair = item["solution"] if solutions else item["student"]
            cells.append(("code", pair[0] if lang == "en" else pair[1]))
        elif kind == "answer":
            if solutions:
                cells.append(("markdown", ANSWER_LABEL[lang] + item[lang]))
            else:
                cells.append(("markdown", ANSWER_PROMPT[lang]))
    return cells


def notebook(cells):
    nb_cells = []
    for i, (cell_type, source) in enumerate(cells):
        cell = {"cell_type": cell_type, "id": f"cell-{i:02d}", "metadata": {}, "source": source}
        if cell_type == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
        nb_cells.append(cell)
    return {
        "cells": nb_cells,
        "metadata": {
            "kernelspec": {"display_name": "R", "language": "R", "name": "ir"},
            "language_info": {"name": "R", "file_extension": ".r", "mimetype": "text/x-r-source"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main():
    targets = {
        False: ROOT / "practical",
        True: ROOT / "teacher" / "solutions",
    }
    for solutions, base in targets.items():
        for lang in ("en", "de"):
            out_dir = base / lang
            out_dir.mkdir(parents=True, exist_ok=True)
            for name, spec in NOTEBOOKS.items():
                path = out_dir / f"{name}.ipynb"
                nb = notebook(to_cells(spec, lang, solutions))
                path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
                print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
