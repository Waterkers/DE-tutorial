"""Check that the English and German notebooks run the same code.

For every notebook in practical/ and teacher/solutions/, the en and de versions
must have the same cells, in the same order, of the same type, and code cells
must be identical apart from:
  - comments (# to the end of the line),
  - text in quotes that contains a space or a non-ASCII letter (plot labels,
    messages); names such as "luminal_lactating" must match exactly,
  - the language in setLanguage("en") / setLanguage("de").

Run from the project folder:  python3 tools/check_parity.py
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SETS = [ROOT / "practical", ROOT / "teacher" / "solutions"]


def normalize(code):
    """Return the code without comments and with human-readable strings replaced."""
    out = []
    for line in code.splitlines():
        result, i, prev = "", 0, ""
        while i < len(line):
            ch = line[i]
            if ch == "#":
                break
            if ch in "\"'":
                j = i + 1
                while j < len(line):
                    if line[j] == ch:
                        break
                    j += 1
                text = line[i + 1 : j]
                is_prose = any(c.isspace() for c in text) or any(ord(c) > 127 for c in text)
                result += "<text>" if is_prose else line[i : j + 1]
                i, prev = j + 1, ch
                continue
            result += ch
            if not ch.isspace():
                prev = ch
            i += 1
        result = result.rstrip()
        if result:
            out.append(result)
    return "\n".join(out).replace('setLanguage("de")', 'setLanguage("en")')


def source(cell):
    s = cell["source"]
    return "".join(s) if isinstance(s, list) else s


def compare(en_path, de_path):
    problems = []
    en = json.loads(en_path.read_text(encoding="utf-8"))["cells"]
    de = json.loads(de_path.read_text(encoding="utf-8"))["cells"]
    if len(en) != len(de):
        return [f"{len(en)} cells in en, {len(de)} in de"]
    for n, (a, b) in enumerate(zip(en, de), start=1):
        if a["cell_type"] != b["cell_type"]:
            problems.append(f"cell {n}: {a['cell_type']} in en, {b['cell_type']} in de")
        elif a["cell_type"] == "code" and normalize(source(a)) != normalize(source(b)):
            problems.append(
                f"cell {n}: code differs\n    en: {normalize(source(a))!r}\n    de: {normalize(source(b))!r}"
            )
    return problems


def main():
    failed = False
    for base in SETS:
        en_files = {p.name for p in (base / "en").glob("*.ipynb")}
        de_files = {p.name for p in (base / "de").glob("*.ipynb")}
        for name in sorted(en_files ^ de_files):
            print(f"FAIL {base.relative_to(ROOT)}: {name} exists in only one language")
            failed = True
        for name in sorted(en_files & de_files):
            problems = compare(base / "en" / name, base / "de" / name)
            label = f"{base.relative_to(ROOT)}/{{en,de}}/{name}"
            if problems:
                failed = True
                print(f"FAIL {label}")
                for p in problems:
                    print(f"  {p}")
            else:
                print(f"ok   {label}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
