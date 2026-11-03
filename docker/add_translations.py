"""Merge our German JupyterLab translations into the installed language pack.

The official pack (jupyterlab-language-pack-de-DE) leaves some menu items students
see in English, and has a few typos. jupyterlab-de-additions.json lists our fixes:
  add:     added only if the pack doesn't have the key (a newer pack wins)
  correct: replaces the pack's value; the build fails if the key is gone, so the
           fix is reviewed rather than silently dropped
"""
import json
import pathlib
import sys

import jupyterlab_language_pack_de_DE

additions = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
locale_dir = pathlib.Path(jupyterlab_language_pack_de_DE.__file__).parent / "locale" / "de_DE" / "LC_MESSAGES"

failed = False
for domain, changes in additions.items():
    if domain.startswith("_"):
        continue
    path = locale_dir / f"{domain}.json"
    pack = json.loads(path.read_text(encoding="utf-8"))
    added = skipped = corrected = 0
    for key, value in changes.get("add", {}).items():
        if key in pack:
            skipped += 1
        else:
            pack[key] = value
            added += 1
    for key, value in changes.get("correct", {}).items():
        if key not in pack:
            print(f"TRANSLATION FAILED: {domain}: '{key}' is no longer in the pack")
            failed = True
            continue
        pack[key] = value
        corrected += 1
    path.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
    print(f"{domain}: {added} added, {skipped} already in the pack, {corrected} corrected")

sys.exit(1 if failed else 0)
