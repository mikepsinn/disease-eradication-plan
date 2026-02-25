#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply unit duplication fixes to QMD files.

Uses the same analysis logic as analyze-unit-duplication.py but applies fixes:
- EXACT_DUPLICATION: remove the trailing prose unit word
- SYNONYM_DUPLICATION / MISMATCH: replace {{< var param >}} with {{< var param_nounit >}}
- RATE_DUPLICATION: remove the trailing rate phrase OR use _nounit

Usage:
    python scripts/apply-unit-migration.py --preview     # show diffs without applying
    python scripts/apply-unit-migration.py --apply        # apply fixes
    python scripts/apply-unit-migration.py --apply --file knowledge/problem.qmd  # single file
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[reportAttributeAccessIssue]

import re
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Reuse the analysis module (import by file path since filename has hyphens)
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "analyze_unit_duplication",
    PROJECT_ROOT / "scripts" / "analyze-unit-duplication.py"
)
if _spec is None or _spec.loader is None:
    raise RuntimeError("Could not load analyze-unit-duplication module")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

_load_param_units = _mod._load_param_units
classify_usage = _mod.classify_usage
VAR_RE = _mod.VAR_RE
TRAIL_WINDOW = _mod.TRAIL_WINDOW
FORMAT_INHERENT_UNITS = _mod.FORMAT_INHERENT_UNITS


def fix_line(line: str, param_units: dict[str, str]) -> tuple[str, list[str]]:
    """Apply fixes to a single line.

    Returns (fixed_line, list_of_change_descriptions).
    """
    changes = []
    # Process matches right-to-left so offsets remain valid
    matches = list(VAR_RE.finditer(line))

    for m in reversed(matches):
        var_name = m.group(1)
        param_name = var_name.upper()
        unit = param_units.get(param_name, "") or param_units.get(var_name, "")

        if not unit:
            continue

        trailing = line[m.end():m.end() + TRAIL_WINDOW]
        classification, trailing_unit = classify_usage(unit, trailing)

        if classification == "STANDALONE":
            continue

        if classification == "EXACT_DUPLICATION":
            # Remove the trailing unit word from the prose
            # Match: optional bold/whitespace, then the unit word, then optional plural s
            pattern = re.compile(
                r'^(\s*\**\s*)' + re.escape(trailing_unit) + r's?\b',
                re.IGNORECASE
            )
            after = line[m.end():]
            new_after = pattern.sub(r'\1', after, count=1)
            # Clean up doubled spaces
            new_after = re.sub(r'  +', ' ', new_after)
            # Clean up space before punctuation
            new_after = re.sub(r'\s+([,;.:!?\)\]])', r'\1', new_after)
            if new_after != after:
                line = line[:m.end()] + new_after
                changes.append(f"EXACT_DUP: removed '{trailing_unit}' after {var_name}")

        elif classification in ("SYNONYM_DUPLICATION", "MISMATCH"):
            # Replace {{< var param >}} with {{< var param_nounit >}}
            old_ref = m.group(0)
            new_ref = old_ref.replace(f"var {var_name}", f"var {var_name}_nounit")
            line = line[:m.start()] + new_ref + line[m.end():]
            changes.append(f"SYNONYM: {var_name} -> {var_name}_nounit (prose has '{trailing_unit}')")

        elif classification == "RATE_DUPLICATION":
            # For rate duplication, remove the rate phrase from prose
            after = line[m.end():]
            # Match optional whitespace/bold then the rate phrase
            rate_pattern = re.compile(
                r'^(\s*\**\s*)' + re.escape(trailing_unit),
                re.IGNORECASE
            )
            new_after = rate_pattern.sub(r'\1', after, count=1)
            new_after = re.sub(r'  +', ' ', new_after)
            new_after = re.sub(r'\s+([,;.:!?\)\]])', r'\1', new_after)
            if new_after != after:
                line = line[:m.end()] + new_after
                changes.append(f"RATE_DUP: removed '{trailing_unit}' after {var_name}")

    return line, changes


def process_file(filepath: Path, param_units: dict[str, str], apply: bool) -> list[dict]:
    """Process a single QMD file. Returns list of change records."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    all_changes = []
    modified = False

    for i, line in enumerate(lines):
        new_line, changes = fix_line(line, param_units)
        if changes:
            for desc in changes:
                all_changes.append({
                    "file": str(filepath.relative_to(PROJECT_ROOT)),
                    "line": i + 1,
                    "old": line.strip(),
                    "new": new_line.strip(),
                    "change": desc,
                })
            lines[i] = new_line
            modified = True

    if apply and modified:
        filepath.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    return all_changes


def main():
    parser = argparse.ArgumentParser(description="Apply unit duplication fixes to QMD files")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preview", action="store_true", help="Show diffs without applying")
    group.add_argument("--apply", action="store_true", help="Apply fixes")
    parser.add_argument("--file", type=str, default=None, help="Process only this file (relative to project root)")
    args = parser.parse_args()

    print("Loading parameter units...", file=sys.stderr)
    param_units = _load_param_units()
    print(f"  Loaded {len(param_units)} parameters with units", file=sys.stderr)

    if args.file:
        qmd_files = [PROJECT_ROOT / args.file]
    else:
        # Respect .gitignore via git ls-files
        import subprocess
        git_result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.qmd"],
            capture_output=True, text=True, cwd=PROJECT_ROOT
        )
        qmd_files = sorted(PROJECT_ROOT / f for f in git_result.stdout.strip().splitlines() if f)

    print(f"  Scanning {len(qmd_files)} QMD files...", file=sys.stderr)

    total_changes = []
    for qmd in qmd_files:
        if not qmd.exists():
            print(f"  WARNING: {qmd} not found, skipping", file=sys.stderr)
            continue
        changes = process_file(qmd, param_units, apply=args.apply)
        total_changes.extend(changes)

    # Output results
    if not total_changes:
        print("No changes needed.", file=sys.stderr)
        return

    mode = "APPLIED" if args.apply else "PREVIEW"
    print(f"\n{mode}: {len(total_changes)} changes across {len(set(c['file'] for c in total_changes))} files\n")

    for c in total_changes:
        print(f"--- {c['file']}:{c['line']} ({c['change']})")
        print(f"-  {c['old']}")
        print(f"+  {c['new']}")
        print()

    if not args.apply:
        print("Run with --apply to make these changes.", file=sys.stderr)


if __name__ == "__main__":
    main()
