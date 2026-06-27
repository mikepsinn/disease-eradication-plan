#!/usr/bin/env python3
"""voice-sweep: incremental ledger for the stance-economy (Layer 2) critic.

Tracks a content hash of each prose chapter in .claude/voice-sweep-state.json, so the
scheduled critic only re-processes files that changed since last run and never burns
tokens re-editing unchanged prose. The ledger is version-controlled (commit it) and the
gate is deterministic.

  python scripts/voice-sweep.py --changed          # list chapters changed since last run
  python scripts/voice-sweep.py --update f1 f2 ...  # mark these processed (record current hash)
  python scripts/voice-sweep.py --all              # list every tracked chapter (ignore ledger)
"""
import sys
import os
import json
import hashlib
import subprocess
import glob

sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, ".claude", "voice-sweep-state.json")
# prose chapters only; skip generated param/data pages that are not voice-edited
EXCLUDE_SUBSTR = ("parameters-and-calculations", "_variables")


def chapters():
    out = []
    for p in glob.glob(os.path.join(ROOT, "knowledge", "**", "*.qmd"), recursive=True):
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        if any(s in rel for s in EXCLUDE_SUBSTR):
            continue
        out.append(rel)
    idx = os.path.join(ROOT, "index-manual.qmd")
    if os.path.exists(idx):
        out.append("index-manual.qmd")
    return sorted(out)


def file_hash(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:16]


def load_ledger():
    if os.path.exists(LEDGER):
        with open(LEDGER, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def head_sha():
    r = subprocess.run(
        ["git", "-C", ROOT, "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True,
    )
    return r.stdout.strip() or "unknown"


def cmd_changed():
    led = load_ledger()
    for rel in chapters():
        prev = led.get(rel, {})
        if prev.get("hash") != file_hash(rel):
            print(rel)


def cmd_update(files):
    led = load_ledger()
    sha = head_sha()
    n = 0
    for rel in files:
        rel = rel.replace("\\", "/")
        if os.path.exists(os.path.join(ROOT, rel)):
            led[rel] = {"hash": file_hash(rel), "sha": sha}
            n += 1
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    with open(LEDGER, "w", encoding="utf-8") as fh:
        json.dump(led, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"voice-sweep: ledger updated for {n} file(s)")


def main():
    args = sys.argv[1:]
    if args and args[0] == "--changed":
        cmd_changed()
    elif args and args[0] == "--all":
        for rel in chapters():
            print(rel)
    elif args and args[0] == "--update":
        cmd_update(args[1:])
    else:
        print("usage: voice-sweep.py --changed | --all | --update <files...>", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
