#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SessionStart hook: Load project context on startup
Shows todo status, git status, and file structure
"""
import sys
import os
import subprocess

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')  # type: ignore[union-attr]

project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
os.chdir(project_dir)

print("=== Disease Eradication Plan Book Context ===", file=sys.stderr)

# Check if todo.md exists
todo_path = os.path.join(project_dir, 'todo.md')
if os.path.exists(todo_path):
    print("", file=sys.stderr)
    print("[TODO Status]", file=sys.stderr)
    try:
        with open(todo_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:10]
            for line in lines:
                print(f"  {line.rstrip()}", file=sys.stderr)
            if len(lines) >= 10:
                print("  ...", file=sys.stderr)
    except Exception:
        pass

# Show git status
print("", file=sys.stderr)
print("[Git Status]", file=sys.stderr)

try:
    # Check if git repo
    result = subprocess.run(
        ['git', 'rev-parse', '--git-dir'],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        # Get branch
        branch_result = subprocess.run(
            ['git', 'branch', '--show-current'],
            cwd=project_dir,
            capture_output=True,
            text=True
        )
        branch = branch_result.stdout.strip() if branch_result.returncode == 0 else 'unknown'
        print(f"  Branch: {branch}", file=sys.stderr)

        # Get uncommitted changes count
        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=project_dir,
            capture_output=True,
            text=True
        )
        uncommitted = len([l for l in status_result.stdout.strip().split('\n') if l]) if status_result.stdout.strip() else 0
        print(f"  Uncommitted changes: {uncommitted} files", file=sys.stderr)

        # Recent commits
        print("  Recent commits:", file=sys.stderr)
        log_result = subprocess.run(
            ['git', 'log', '--oneline', '-3'],
            cwd=project_dir,
            capture_output=True,
            text=True
        )
        if log_result.returncode == 0:
            for line in log_result.stdout.strip().split('\n')[:3]:
                if line:
                    print(f"    {line}", file=sys.stderr)
    else:
        print("  Not a git repository", file=sys.stderr)
except Exception as e:
    print(f"  Git status unavailable: {e}", file=sys.stderr)

# Check variables status
print("", file=sys.stderr)
print("[Variables Status]", file=sys.stderr)

vars_path = os.path.join(project_dir, '_variables.yml')
params_path = os.path.join(project_dir, 'dih_models', 'parameters.py')

if os.path.exists(vars_path) and os.path.exists(params_path):
    try:
        vars_mtime = os.path.getmtime(vars_path)
        params_mtime = os.path.getmtime(params_path)

        if vars_mtime < params_mtime:
            print("  WARNING: _variables.yml is older than parameters.py", file=sys.stderr)
            print("  Run: python scripts/generate-everything-parameters-variables-calculations-references.py", file=sys.stderr)
        else:
            print("  Variables up-to-date", file=sys.stderr)
    except Exception:
        print("  Files present (timestamp check failed)", file=sys.stderr)
else:
    print("  _variables.yml or parameters.py not found", file=sys.stderr)

# Show file counts
print("", file=sys.stderr)
print("[Book Structure]", file=sys.stderr)

knowledge_dir = os.path.join(project_dir, 'knowledge')
if os.path.isdir(knowledge_dir):
    qmd_count = 0
    for root, dirs, files in os.walk(knowledge_dir):
        qmd_count += sum(1 for f in files if f.endswith('.qmd'))
    print(f"  QMD files: {qmd_count}", file=sys.stderr)

print("  Book config: _quarto.yml", file=sys.stderr)

print("============================================", file=sys.stderr)
print("", file=sys.stderr)

sys.exit(0)
