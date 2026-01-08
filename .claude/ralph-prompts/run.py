#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ralph Loop Prompt Runner

Reads prompt files from .claude/ralph-prompts/ and starts Ralph loops.

Usage:
    python .claude/ralph-prompts/run.py --list
    python .claude/ralph-prompts/run.py <prompt-name>
    python .claude/ralph-prompts/run.py <prompt-name> --max-iterations 20
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime, timezone

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')  # type: ignore[union-attr]


def get_prompts_dir() -> Path:
    """Get the ralph-prompts directory."""
    # Try CLAUDE_PROJECT_DIR first, then current directory
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
    return Path(project_dir) / '.claude' / 'ralph-prompts'


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    lines = content.split('\n')

    if not lines or lines[0].strip() != '---':
        return {}, content

    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end_idx = i
            break

    if end_idx == -1:
        return {}, content

    frontmatter = {}
    for line in lines[1:end_idx]:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            # Remove quotes
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            # Convert numbers
            if value.isdigit():
                value = int(value)
            frontmatter[key] = value

    body = '\n'.join(lines[end_idx + 1:]).strip()
    return frontmatter, body


def list_prompts(prompts_dir: Path):
    """List all available prompt files."""
    print("Available Ralph Loop Prompts:")
    print("=" * 40)
    print("")

    prompt_files = sorted(prompts_dir.glob('*.md'))
    prompt_files = [f for f in prompt_files if f.name != 'README.md']

    if not prompt_files:
        print("No prompt files found in:")
        print(f"  {prompts_dir}")
        print("")
        print("Create a .md file to add a prompt.")
        return

    for prompt_file in prompt_files:
        name = prompt_file.stem
        try:
            content = prompt_file.read_text(encoding='utf-8')
            frontmatter, body = parse_frontmatter(content)
            description = frontmatter.get('description', body[:60].replace('\n', ' ') + '...')
            max_iter = frontmatter.get('max_iterations', 'unlimited')
            promise = frontmatter.get('completion_promise', 'none')

            print(f"  {name}")
            print(f"    {description}")
            print(f"    max_iterations: {max_iter}, promise: {promise}")
            print("")
        except Exception as e:
            print(f"  {name} (error reading: {e})")
            print("")


def run_prompt(prompt_name: str, prompts_dir: Path, max_iterations_override: int = None):
    """Start a Ralph loop with the given prompt."""
    prompt_file = prompts_dir / f"{prompt_name}.md"

    if not prompt_file.exists():
        print(f"Error: Prompt '{prompt_name}' not found", file=sys.stderr)
        print(f"  Expected: {prompt_file}", file=sys.stderr)
        print("", file=sys.stderr)
        print("Available prompts:", file=sys.stderr)
        for f in prompts_dir.glob('*.md'):
            if f.name != 'README.md':
                print(f"  - {f.stem}", file=sys.stderr)
        sys.exit(1)

    try:
        content = prompt_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading prompt file: {e}", file=sys.stderr)
        sys.exit(1)

    frontmatter, prompt_text = parse_frontmatter(content)

    max_iterations = max_iterations_override if max_iterations_override is not None else frontmatter.get('max_iterations', 0)
    completion_promise = frontmatter.get('completion_promise', 'null')

    if not prompt_text:
        print("Error: Prompt file has no content", file=sys.stderr)
        sys.exit(1)

    # Create .claude directory if needed
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
    claude_dir = Path(project_dir) / '.claude'
    claude_dir.mkdir(exist_ok=True)

    # Quote completion promise for YAML
    if completion_promise and completion_promise != 'null':
        completion_promise_yaml = f'"{completion_promise}"'
    else:
        completion_promise_yaml = 'null'
        completion_promise = 'null'

    started_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    state_content = f"""---
active: true
iteration: 1
max_iterations: {max_iterations}
completion_promise: {completion_promise_yaml}
started_at: "{started_at}"
prompt_file: "{prompt_name}"
---

{prompt_text}
"""

    state_file = claude_dir / 'ralph-loop.local.md'
    state_file.write_text(state_content, encoding='utf-8')

    max_iter_display = str(max_iterations) if max_iterations > 0 else "unlimited"
    if completion_promise != 'null':
        promise_display = f"{completion_promise}"
    else:
        promise_display = "none (runs forever)"

    print(f"Ralph loop started: {prompt_name}")
    print("=" * 40)
    print(f"Max iterations: {max_iter_display}")
    print(f"Completion promise: {promise_display}")
    print("")
    print("The stop hook is now active. Work on the task below.")
    print("=" * 40)
    print("")
    print(prompt_text)

    if completion_promise != 'null':
        print("")
        print("-" * 40)
        print(f"To complete, output: <promise>{completion_promise}</promise>")
        print("-" * 40)


def main():
    args = sys.argv[1:]

    if not args or args[0] in ['-h', '--help']:
        print(__doc__)
        sys.exit(0)

    prompts_dir = get_prompts_dir()

    if args[0] in ['-l', '--list']:
        list_prompts(prompts_dir)
        sys.exit(0)

    # Parse arguments
    prompt_name = args[0]
    max_iterations = None

    i = 1
    while i < len(args):
        if args[i] in ['--max-iterations', '-m']:
            if i + 1 < len(args):
                try:
                    max_iterations = int(args[i + 1])
                except ValueError:
                    print(f"Error: Invalid max_iterations: {args[i + 1]}", file=sys.stderr)
                    sys.exit(1)
                i += 2
            else:
                print("Error: --max-iterations requires a value", file=sys.stderr)
                sys.exit(1)
        else:
            i += 1

    run_prompt(prompt_name, prompts_dir, max_iterations)


if __name__ == '__main__':
    main()
