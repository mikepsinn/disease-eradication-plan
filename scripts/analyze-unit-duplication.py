#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze unit duplication in QMD files.

Scans all QMD files for {{< var param >}} usages and classifies each based on
whether the surrounding prose duplicates the unit already embedded in the variable.

Classifications:
  EXACT_DUPLICATION   - unit="deaths", prose="deaths"
  SYNONYM_DUPLICATION - unit="deaths", prose="lives" or "people"
  RATE_DUPLICATION    - unit="drugs/year", prose="per year"
  STANDALONE          - no unit word follows the variable
  MISMATCH            - unit word follows but doesn't match embedded unit

Usage:
    python scripts/analyze-unit-duplication.py
    python scripts/analyze-unit-duplication.py --output report.md
"""
import sys
getattr(sys.stdout, "reconfigure", lambda **kw: None)(encoding="utf-8")

import re
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root (this script lives in scripts/)
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Load parameter units from parameters.py via the dih_models package
# ---------------------------------------------------------------------------
sys.path.insert(0, str(PROJECT_ROOT))

def _load_param_units() -> dict[str, str]:
    """Return {PARAM_NAME: unit} for every parameter with a unit."""
    import importlib.util
    # Ensure dih_models submodules can resolve relative imports
    dih_dir = str(PROJECT_ROOT / "dih_models")
    if dih_dir not in sys.path:
        sys.path.insert(0, dih_dir)
    params_path = PROJECT_ROOT / "dih_models" / "parameters.py"
    spec = importlib.util.spec_from_file_location("parameters", params_path)
    if spec is None or spec.loader is None:
        raise FileNotFoundError(f"Cannot load module from {params_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    units = {}
    for name in dir(mod):
        if name.isupper():
            val = getattr(mod, name)
            if isinstance(val, (int, float)):
                u = getattr(val, "unit", None)
                if u:
                    units[name] = u
    return units

# ---------------------------------------------------------------------------
# Unit synonym groups  (unit text -> set of prose words that mean the same)
# ---------------------------------------------------------------------------
# Maps a unit string to a set of prose words (lowercase) that are synonymous.
UNIT_SYNONYMS: dict[str, set[str]] = {
    "deaths":        {"deaths", "death", "lives", "life", "people", "person", "persons", "individuals"},
    "deaths/year":   {"deaths", "death", "lives", "life", "people", "person"},
    "lives":         {"lives", "life", "deaths", "death", "people", "person"},
    "lives/year":    {"lives", "life", "deaths", "death", "people", "person"},
    "people":        {"people", "person", "persons", "individuals", "lives", "deaths"},
    "patients":      {"patients", "patient", "people", "person", "individuals"},
    "patients/year": {"patients", "patient", "people", "person"},
    "DALYs":         {"dalys", "daly", "disability-adjusted"},
    "DALYs/year":    {"dalys", "daly"},
    "QALYs":         {"qalys", "qaly", "quality-adjusted"},
    "QALYs/year":    {"qalys", "qaly"},
    "QALYs/death":   {"qalys", "qaly"},
    "QALYs/life":    {"qalys", "qaly"},
    "cases":         {"cases", "case"},
    "years":         {"years", "year"},
    "months":        {"months", "month"},
    "days":          {"days", "day"},
    "hours":         {"hours", "hour"},
    "life-years":    {"life-years", "life", "years"},
    "drugs":         {"drugs", "drug", "treatments", "treatment", "medications"},
    "drugs/year":    {"drugs", "drug", "treatments", "treatment"},
    "diseases":      {"diseases", "disease", "conditions"},
    "diseases/year": {"diseases", "disease"},
    "trials":        {"trials", "trial", "studies"},
    "trials/year":   {"trials", "trial"},
    "combinations":  {"combinations", "combination", "combos"},
    "compounds":     {"compounds", "compound"},
    "genes":         {"genes", "gene"},
    "targets":       {"targets", "target"},
    "approaches":    {"approaches", "approach"},
    "products":      {"products", "product"},
    "codes":         {"codes", "code"},
    "substances":    {"substances", "substance"},
    "pairings":      {"pairings", "pairing"},
    "members":       {"members", "member"},
    "senators":      {"senators", "senator"},
    "physicians":    {"physicians", "physician", "doctors"},
    "relationships": {"relationships", "relationship"},
    "of people":     {"people", "person"},
    "9/11s":         {"9/11s", "9/11"},
    "deaths/day":    {"deaths", "death"},
    "hours/month":   {"hours", "hour"},
    "years/decade":  {"years", "year"},
}

# Rate suffixes that can duplicate "/year" etc.
RATE_PROSE = {
    "per year", "a year", "each year", "every year", "annually",
    "per month", "a month", "each month", "per day", "a day", "each day",
    "per decade", "a decade",
}

# Units that are format-inherent (no visible word text) - skip these
FORMAT_INHERENT_UNITS = {
    "usd", "usd/year", "usd/daly", "usd/qaly", "usd/patient",
    "usd/patient/month", "usd/patient/year", "usd/person/year",
    "usd/life", "usd/hour", "usd/day", "usd/trial",
    "usd_1980",
    "percentage", "percent", "rate", "proportion",
    "ratio",
    "x", "multiplier", "factor",
    "weight",
}


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

# Regex to find {{< var name >}} with optional trailing text
VAR_RE = re.compile(r'\{\{<\s*var\s+([\w]+)\s*>\}\}')

# How many chars after the closing >}} to inspect for trailing unit text
TRAIL_WINDOW = 60


def classify_usage(unit: str, trailing: str) -> tuple[str, str]:
    """Classify a single variable usage.

    Returns (classification, trailing_unit_text).
    """
    if not unit:
        return ("STANDALONE", "")

    unit_lower = unit.lower()

    # Skip format-inherent units
    if unit_lower in FORMAT_INHERENT_UNITS:
        return ("STANDALONE", "")

    # Clean trailing text: strip leading punctuation/whitespace/bold markers
    clean = trailing.lstrip(" \t*_")

    # Check for rate duplication first (multi-word patterns)
    for rate in RATE_PROSE:
        if clean.lower().startswith(rate):
            # Check if the unit itself has a rate component
            if "/" in unit:
                return ("RATE_DUPLICATION", rate)

    # Extract first 1-2 words for unit matching
    words = re.split(r'[\s,;.:!?\)\]\}]+', clean, maxsplit=3)
    first_word = words[0].lower().rstrip(".,;:!?)]}") if words else ""

    if not first_word:
        return ("STANDALONE", "")

    # Get the base unit word (before any / for rate units)
    base_unit = unit.split("/")[0].lower()
    synonyms = UNIT_SYNONYMS.get(unit, set())
    base_synonyms = UNIT_SYNONYMS.get(base_unit, set()) if base_unit != unit.lower() else set()
    all_synonyms = synonyms | base_synonyms

    # Exact duplication: trailing word matches unit text exactly
    if first_word == base_unit or first_word == base_unit.rstrip("s") or first_word == base_unit + "s":
        return ("EXACT_DUPLICATION", first_word)

    # Synonym duplication
    if first_word in all_synonyms:
        return ("SYNONYM_DUPLICATION", first_word)

    return ("STANDALONE", "")


def scan_file(filepath: Path, param_units: dict[str, str]) -> list[dict]:
    """Scan a single QMD file for variable usages and classify each."""
    results = []
    text = filepath.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")

    for line_no, line in enumerate(lines, 1):
        for m in VAR_RE.finditer(line):
            var_name = m.group(1)
            param_name = var_name.upper()

            unit = param_units.get(param_name, "")
            if not unit:
                # Also try lowercase lookup
                unit = param_units.get(var_name, "")

            # Get trailing text after the variable
            end_pos = m.end()
            trailing = line[end_pos:end_pos + TRAIL_WINDOW]

            classification, trailing_unit = classify_usage(unit, trailing)

            results.append({
                "file": str(filepath.relative_to(PROJECT_ROOT)),
                "line": line_no,
                "variable": var_name,
                "unit": unit,
                "trailing_text": trailing[:40].strip(),
                "classification": classification,
                "trailing_unit": trailing_unit,
                "full_line": line.strip(),
            })

    return results


def generate_report(all_results: list[dict]) -> str:
    """Generate a markdown report from classification results."""
    lines = []
    lines.append("# Unit Duplication Analysis Report\n")

    # Summary counts
    counts = {}
    for r in all_results:
        c = r["classification"]
        counts[c] = counts.get(c, 0) + 1

    lines.append("## Summary\n")
    lines.append("| Classification | Count |")
    lines.append("|---|---|")
    for c in ["EXACT_DUPLICATION", "SYNONYM_DUPLICATION", "RATE_DUPLICATION", "STANDALONE", "MISMATCH"]:
        if c in counts:
            lines.append(f"| {c} | {counts[c]} |")
    lines.append(f"| **Total** | **{len(all_results)}** |")
    lines.append("")

    # Detailed results (only non-STANDALONE)
    flagged = [r for r in all_results if r["classification"] != "STANDALONE"]

    if flagged:
        lines.append("## Flagged Usages\n")
        lines.append("| File | Line | Variable | Unit | Trailing | Classification | Suggested Fix |")
        lines.append("|---|---|---|---|---|---|---|")

        for r in sorted(flagged, key=lambda x: (x["classification"], x["file"], x["line"])):
            fix = ""
            if r["classification"] == "EXACT_DUPLICATION":
                fix = f"Remove '{r['trailing_unit']}' from prose"
            elif r["classification"] == "SYNONYM_DUPLICATION":
                fix = f"Use `{{{{< var {r['variable']}_nounit >}}}}` + keep '{r['trailing_unit']}'"
            elif r["classification"] == "RATE_DUPLICATION":
                fix = f"Remove '{r['trailing_unit']}' OR use `_nounit`"
            elif r["classification"] == "MISMATCH":
                fix = "Editorial review needed"

            lines.append(
                f"| {r['file']} | {r['line']} | `{r['variable']}` | "
                f"{r['unit']} | `{r['trailing_text'][:30]}` | "
                f"{r['classification']} | {fix} |"
            )
        lines.append("")

    # Per-file summary
    file_flags = {}
    for r in flagged:
        f = r["file"]
        file_flags[f] = file_flags.get(f, 0) + 1

    if file_flags:
        lines.append("## Files with Issues\n")
        lines.append("| File | Flagged Usages |")
        lines.append("|---|---|")
        for f, count in sorted(file_flags.items(), key=lambda x: -x[1]):
            lines.append(f"| {f} | {count} |")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze unit duplication in QMD files")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Output markdown file path (default: print to stdout)")
    args = parser.parse_args()

    print("Loading parameter units...", file=sys.stderr)
    param_units = _load_param_units()
    print(f"  Loaded {len(param_units)} parameters with units", file=sys.stderr)

    # Find all tracked QMD files (respects .gitignore)
    import subprocess
    git_result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.qmd"],
        capture_output=True, text=True, cwd=PROJECT_ROOT
    )
    qmd_files = sorted(PROJECT_ROOT / f for f in git_result.stdout.strip().splitlines() if f)
    print(f"  Found {len(qmd_files)} QMD files to scan", file=sys.stderr)

    all_results = []
    for qmd in qmd_files:
        results = scan_file(qmd, param_units)
        all_results.extend(results)

    print(f"  Classified {len(all_results)} variable usages", file=sys.stderr)

    report = generate_report(all_results)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(report, encoding="utf-8")
        print(f"Report written to {out_path}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
