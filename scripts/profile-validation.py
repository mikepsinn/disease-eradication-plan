#!/usr/bin/env python3
"""Profile pre-render-validation.py to find bottlenecks."""
import time
import sys
import os
from glob import glob

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class Timer:
    def __init__(self):
        self.timings = []
        self.start_time = None
        self.current_step = None

    def start(self, name):
        if self.start_time and self.current_step:
            elapsed = time.time() - self.start_time
            self.timings.append((self.current_step, elapsed))
        self.current_step = name
        self.start_time = time.time()
        print(f"[PROFILE] Starting: {name}")

    def finish(self):
        if self.start_time and self.current_step:
            elapsed = time.time() - self.start_time
            self.timings.append((self.current_step, elapsed))

    def report(self):
        print("\n" + "="*70)
        print("PROFILING RESULTS - SORTED BY TIME (slowest first)")
        print("="*70)
        sorted_timings = sorted(self.timings, key=lambda x: x[1], reverse=True)
        total = sum(t[1] for t in self.timings)
        for name, elapsed in sorted_timings:
            pct = (elapsed / total) * 100
            print(f"{elapsed:7.2f}s ({pct:5.1f}%) - {name}")
        print("-"*70)
        print(f"{total:7.2f}s (100.0%) - TOTAL")

timer = Timer()

# Step 1: Run generate-everything script
timer.start("1. Run generate-everything script")
import subprocess
result = subprocess.run(
    [sys.executable, "scripts/generate-everything-parameters-variables-calculations-references.py"],
    capture_output=True, text=True, timeout=120
)
if result.returncode != 0:
    print(f"ERROR: generate-everything failed: {result.stderr[:500]}")
    sys.exit(1)

# Step 2: Load variables
timer.start("2. Load variables from _variables.yml")
import yaml
with open("_variables.yml", encoding="utf-8") as f:
    variables = yaml.safe_load(f)
defined_vars = set(variables.keys()) if isinstance(variables, dict) else set()
print(f"   Loaded {len(defined_vars)} variables")

# Step 3: Load parameters
timer.start("3. Load parameters from parameters.py")
import re
with open("dih_models/parameters.py", encoding="utf-8") as f:
    content = f.read()
param_pattern = re.compile(r"^([A-Z][A-Z0-9_]*)\s*=\s*Parameter\(", re.MULTILINE)
defined_parameters = set(m.group(1) for m in param_pattern.finditer(content))
print(f"   Loaded {len(defined_parameters)} parameters")

# Step 4: Load anchor IDs
timer.start("4. Load anchor IDs from all files")
# Import the function from pre-render-validation
sys.path.insert(0, "scripts")

def load_anchor_ids(filepath):
    anchor_ids = set()
    if not os.path.exists(filepath):
        return anchor_ids
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        html_anchor_pattern = re.compile(r'<a\s+id\s*=\s*["\']([^"\']+)["\']\s*></a>', re.IGNORECASE)
        for match in html_anchor_pattern.finditer(content):
            anchor_ids.add(match.group(1))
        quarto_anchor_pattern = re.compile(r'^#+\s+.*\{#([^}]+)\}', re.MULTILINE)
        for match in quarto_anchor_pattern.finditer(content):
            anchor_ids.add(match.group(1))
        heading_pattern = re.compile(r'^#+\s+(.+)$', re.MULTILINE)
        for match in heading_pattern.finditer(content):
            heading_text = match.group(1).strip()
            heading_text = re.sub(r'\s*\{#[^}]+\}', '', heading_text)
            anchor_id = re.sub(r'[^\w\s-]', '', heading_text.lower())
            anchor_id = re.sub(r'[-\s]+', '-', anchor_id)
            anchor_id = anchor_id.strip('-')
            if anchor_id:
                anchor_ids.add(anchor_id)
        return anchor_ids
    except Exception:
        return anchor_ids

qmd_files = glob("**/*.qmd", recursive=True)
md_files = glob("**/*.md", recursive=True)
all_files = qmd_files + md_files
all_files = [f for f in all_files if not any(x in f for x in ["node_modules", "_book", ".quarto", "_site", "__tests__", "_build_temp"])]

anchor_map = {}
for filepath in all_files:
    anchor_ids = load_anchor_ids(filepath)
    if anchor_ids:
        anchor_map[os.path.normpath(filepath)] = anchor_ids
print(f"   Loaded {sum(len(ids) for ids in anchor_map.values())} anchors from {len(anchor_map)} files")

# Step 5: Load citations
timer.start("5. Load citations from references.bib")
with open("references.bib", encoding="utf-8") as f:
    bib_content = f.read()
entry_pattern = re.compile(r'@\w+\{([^,]+),')
defined_citations = set(m.group(1).strip() for m in entry_pattern.finditer(bib_content))
print(f"   Loaded {len(defined_citations)} citations")

# Step 6: Find files to validate
timer.start("6. Find files to validate")
qmd_files = glob("**/*.qmd", recursive=True)
qmd_files = [f for f in qmd_files if not any(x in f for x in ["node_modules", "_book", ".quarto", "_site", "__tests__", "_build_temp"])]
qmd_files = [f for f in qmd_files if not f.endswith("references.qmd")]
qmd_files = [f for f in qmd_files if not f.endswith("index.qmd") or f.endswith("index-manual.qmd")]

md_files = glob("**/*.md", recursive=True)
md_files = [f for f in md_files if not any(x in f for x in ["node_modules", "_book", ".quarto", "_site", "__tests__", "_build_temp"])]
md_files = [f for f in md_files if os.path.dirname(f)]
md_files = [f for f in md_files if not f.endswith("OUTLINE-GENERATED.MD") and not f.endswith("TODO.md") and not f.endswith("brainstorm.md")]

all_validation_files = qmd_files + md_files
print(f"   Found {len(qmd_files)} QMD + {len(md_files)} MD = {len(all_validation_files)} files")

# Step 7: Validate files (simplified - just read and run basic checks)
timer.start("7. Validate all files")
# Import validation functions
from importlib import import_module
# We'll just time how long it takes to read and do basic regex on all files
validated = 0
for filepath in all_validation_files:
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    # Simulate some validation work (regex patterns)
    re.findall(r"\$\$\$", content)
    re.findall(r"\{\{<\s*var\s+([^\s>]+)\s*>\}\}", content)
    re.findall(r"\[@([^\]]+)\]", content)
    validated += 1
print(f"   Validated {validated} files")

timer.finish()
timer.report()
