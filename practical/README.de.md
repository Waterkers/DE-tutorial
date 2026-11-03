[English](README.md) | **Deutsch**

# Praktikum: Welche Gene schaltet eine Zelle an?

In diesem Praktikum analysierst du echte RNA-Sequenzierdaten und findest heraus, welche Gene Zellen an- oder ausschalten: wenn eine Maus Milch macht, und danach bei einer eigenen Forschungsfrage.

## Starten

Du brauchst **Docker Desktop**, und es muss laufen (achte auf das Wal-Symbol).

| Computer | Doppelklick auf |
|---|---|
| Windows | `start_de.bat` |
| Mac | `start_de.command` |
| Linux | im Terminal `./start.sh de` ausführen |

**Mac, nur beim ersten Mal:** macOS blockiert `start_de.command`, weil die Datei aus dem Internet heruntergeladen wurde. Rechtsklick → *Öffnen* hilft nicht. Stattdessen:

1. Doppelklicke auf `start_de.command`. macOS meldet, dass die Datei nicht geöffnet werden kann; klicke auf **Fertig**.
2. Öffne  → **Systemeinstellungen → Datenschutz & Sicherheit**, scrolle nach unten und klicke neben `start_de.command` auf **Dennoch öffnen**.
3. Gib dein Mac-Passwort ein (oder nutze Touch ID) und klicke noch einmal auf **Dennoch öffnen**.
4. Wenn Terminal nach Zugriff auf den Ordner *Downloads* fragt, klicke auf **Erlauben**.

Nach ein paar Sekunden öffnet sich dein Browser mit **JupyterLab** und dem Ordner `de`. Falls nicht, öffne <http://localhost:8889> selbst.

## Arbeiten

Öffne die Notebooks der Reihe nach:

1. `00_welcome.ipynb`: So funktionieren Notebooks, und was ein Transkriptom ist
2. `01_tutorial_milk.ipynb`: Welche Gene schaltet eine Maus an, wenn sie Milch macht? (Schritt für Schritt)
3. Danach **eines** davon, selbstständig (deine Lehrkraft sagt dir, welches):
   * `02_diy_dexamethasone.ipynb`: Wie verändert ein Asthma-Medikament die Zellen der Atemwege?
   * `03_diy_pasilla.ipynb`: Was passiert, wenn eine Fliegenzelle das Protein pasilla verliert?
   * `04_diy_cancer.ipynb`: Was ist bei Brustkrebs anders?

Eine Zelle führst du mit **Umschalt + Enter** aus. Wo `___` steht, füllst du die Lücke aus. Deine Arbeit wird in diesem Ordner `practical` auf deinem eigenen Computer gespeichert.

## Beenden

Doppelklicke auf `stop.bat` (Windows) oder führe `./stop.sh` aus (Mac/Linux). Deine Notebooks bleiben erhalten.

## Etwas klappt nicht?

* **„Docker läuft nicht“**: Starte Docker Desktop, warte, bis es läuft, und versuche es noch einmal.
* **Eine Zelle zeigt einen Fehler**: Prüfe, ob du die Zellen darüber ausgeführt hast, von oben angefangen.
* **Ein Notebook ganz von vorn beginnen**: Menü *Kernel → Kernel neu starten und Ausgaben aller Zellen löschen…*, dann die Zellen noch einmal ausführen.
* Kommst du nicht weiter? Frag deine Lehrkraft.

## Quellen

Die Daten stammen aus veröffentlichten Studien (Fu et al. 2015; Himes et al. 2014; Brooks et al. 2011) und aus The Cancer Genome Atlas. Die Analyse nutzt [limma](https://bioconductor.org/packages/limma) (Ritchie et al. 2015) und [edgeR](https://bioconductor.org/packages/edgeR) (Chen et al. 2025) in [R](https://www.r-project.org). Die vollständigen Quellen stehen am Ende von `01_tutorial_milk.ipynb`.

Diese Materialien stehen unter [CC BY 4.0](../LICENSE-CC-BY-4.0.txt) (Notebooks) und [MIT](../LICENSE) (Code).
