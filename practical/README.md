**English** | [Deutsch](README.de.md)

# Practical: which genes does a cell switch on?

In this practical you'll analyse real RNA-sequencing data to find out which genes cells switch on or off: when a mouse makes milk, and then in a research question of your own.

## Starting

You need **Docker Desktop**, and it must be running (look for the whale icon).

| Computer | Double-click |
|---|---|
| Windows | `start.bat` |
| Mac | `start.command` |
| Linux | run `./start.sh` in a terminal |

**Mac, the first time only:** macOS blocks `start.command` because it was downloaded from the internet. Right-click → *Open* doesn't help. Instead:

1. Double-click `start.command`. macOS says it can't be opened; click **Done**.
2. Open  → **System Settings → Privacy & Security**, scroll down and click **Open Anyway** next to `start.command`.
3. Enter your Mac password (or use Touch ID), then click **Open Anyway** again.
4. If Terminal asks for access to the *Downloads* folder, click **Allow**.

After a few seconds your browser opens **JupyterLab** with the `en` folder. If it doesn't, open <http://localhost:8889> yourself.

## Working

Open the notebooks in order:

1. `00_welcome.ipynb`: how notebooks work, and what a transcriptome is
2. `01_tutorial_milk.ipynb`: which genes switch on when a mouse makes milk? (step by step)
3. Then **one** of these, on your own (your teacher tells you which):
   * `02_diy_dexamethasone.ipynb`: how does an asthma drug change airway cells?
   * `03_diy_pasilla.ipynb`: what happens when a fly cell loses the protein pasilla?
   * `04_diy_cancer.ipynb`: what is different in breast cancer?

Run a cell with **Shift + Enter**. Where you see `___`, fill in the gap. Your work is saved in this `practical` folder on your own computer.

## Stopping

Double-click `stop.bat` (Windows) or run `./stop.sh` (Mac/Linux). Your notebooks stay where they are.

## Something went wrong?

* **"Docker is not running"**: start Docker Desktop, wait until it says it's running, try again.
* **A cell shows an error**: check that you ran the cells above it, from the top.
* **Start a notebook again from scratch**: menu *Kernel → Restart Kernel and Clear Outputs of All Cells…*, then run the cells again.
* Still stuck? Ask your teacher.

## Credits

The data come from published studies (Fu et al. 2015; Himes et al. 2014; Brooks et al. 2011) and The Cancer Genome Atlas. The analysis uses [limma](https://bioconductor.org/packages/limma) (Ritchie et al. 2015) and [edgeR](https://bioconductor.org/packages/edgeR) (Chen et al. 2025) in [R](https://www.r-project.org). The full sources are at the end of `01_tutorial_milk.ipynb`.

These materials are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0.txt) (notebooks) and [MIT](../LICENSE) (code).
