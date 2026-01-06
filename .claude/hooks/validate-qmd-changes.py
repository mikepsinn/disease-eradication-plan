#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostToolUse hook: Validate QMD file changes
Runs after Edit/Write operations to check for common errors
"""
import json
import sys
import re
import os

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    input_data = json.load(sys.stdin)
except:
    sys.exit(0)

file_path = input_data.get('tool_input', {}).get('file_path', '')

# Only validate QMD files
if not file_path.endswith('.qmd'):
    sys.exit(0)

issues = []

# Read the file
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except:
    sys.exit(0)

# Check 1: Warn about hardcoded dollar amounts that might be variables
hardcoded_money_pattern = r'\$[\d,]+(?:\.\d{1,2})?[MBK]?\b'
hardcoded_matches = re.findall(hardcoded_money_pattern, content)
if hardcoded_matches:
    unique_amounts = list(set(hardcoded_matches))[:3]  # Show first 3 examples
    issues.append(f"WARNING: Found {len(hardcoded_matches)} hardcoded values (e.g., {', '.join(unique_amounts)}). Check _variables.yml for matching parameters.")

# Check 2: Find all variable references and validate syntax
var_refs = re.findall(r'\{\{<\s*var\s+(\w+)\s*>\}\}', content)
if var_refs:
    try:
        # Quick validation - check _variables.yml exists
        proj_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
        var_file = os.path.join(proj_dir, '_variables.yml')
        if os.path.exists(var_file):
            with open(var_file, 'r', encoding='utf-8') as f:
                var_content = f.read()
                invalid_vars = []
                for var in set(var_refs):
                    # Check if variable exists in _variables.yml
                    if f'{var}:' not in var_content:
                        invalid_vars.append(var)
                if invalid_vars:
                    issues.append(f"ERROR: Variables not found in _variables.yml: {', '.join(invalid_vars[:5])}")
    except Exception as e:
        pass

# Check 3: Cross-format links (should use .qmd not .html)
html_links = re.findall(r'\[([^\]]+)\]\(([^)]+\.html[^)]*)\)', content)
if html_links:
    examples = [link[1] for link in html_links[:2]]
    issues.append(f"WARNING: Found {len(html_links)} HTML links (not cross-format compatible). Use .qmd instead. Examples: {', '.join(examples)}")

# Check 4: Em-dashes (should use periods, commas, or parentheses)
em_dash_count = content.count('—')
if em_dash_count > 0:
    issues.append(f"STYLE: Found {em_dash_count} em-dashes (—). Linter prefers periods, commas, or parentheses for readability.")

# Check 5: Malformed variable references (common typo)
malformed_vars = re.findall(r'\{\{<var\s+\w+>\}\}', content)  # Missing space after <
if malformed_vars:
    issues.append(f"ERROR: Malformed variable syntax (missing space after '<'): {len(malformed_vars)} instances")

if issues:
    print("\n[QMD Validation]", file=sys.stderr)
    for issue in issues:
        print(f"  {issue}", file=sys.stderr)
    print("", file=sys.stderr)
    # Exit 0 to warn without blocking
    sys.exit(0)

sys.exit(0)
