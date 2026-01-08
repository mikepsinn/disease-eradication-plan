#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ralph Loop Setup Script (Windows-compatible Python version)
Creates state file for in-session Ralph loop
"""

import sys
import os
from datetime import datetime, timezone

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')  # type: ignore[union-attr]

HELP_TEXT = """Ralph Loop - Interactive self-referential development loop

USAGE:
  /ralph-loop [PROMPT...] [OPTIONS]

ARGUMENTS:
  PROMPT...    Initial prompt to start the loop (can be multiple words without quotes)

OPTIONS:
  --max-iterations <n>           Maximum iterations before auto-stop (default: unlimited)
  --completion-promise '<text>'  Promise phrase (USE QUOTES for multi-word)
  -h, --help                     Show this help message

DESCRIPTION:
  Starts a Ralph Loop in your CURRENT session. The stop hook prevents
  exit and feeds your output back as input until completion or iteration limit.

  To signal completion, you must output: <promise>YOUR_PHRASE</promise>

EXAMPLES:
  /ralph-loop Build a todo API --completion-promise 'DONE' --max-iterations 20
  /ralph-loop --max-iterations 10 Fix the auth bug
  /ralph-loop Refactor cache layer  (runs forever)
  /ralph-loop --completion-promise 'TASK COMPLETE' Create a REST API

STOPPING:
  Only by reaching --max-iterations or detecting --completion-promise
  No manual stop - Ralph runs infinitely by default!
"""


def main():
    args = sys.argv[1:]

    if '-h' in args or '--help' in args:
        print(HELP_TEXT)
        sys.exit(0)

    max_iterations = 0
    completion_promise = "null"
    prompt_parts = []

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == '--max-iterations':
            if i + 1 >= len(args) or args[i + 1].startswith('-'):
                print("Error: --max-iterations requires a number argument", file=sys.stderr)
                sys.exit(1)
            try:
                max_iterations = int(args[i + 1])
                if max_iterations < 0:
                    raise ValueError("negative")
            except ValueError:
                print(f"Error: --max-iterations must be a positive integer or 0, got: {args[i + 1]}", file=sys.stderr)
                sys.exit(1)
            i += 2

        elif arg == '--completion-promise':
            if i + 1 >= len(args):
                print("Error: --completion-promise requires a text argument", file=sys.stderr)
                sys.exit(1)
            completion_promise = args[i + 1]
            i += 2

        else:
            prompt_parts.append(arg)
            i += 1

    prompt = ' '.join(prompt_parts)

    if not prompt.strip():
        print("Error: No prompt provided", file=sys.stderr)
        print("", file=sys.stderr)
        print("   Examples:", file=sys.stderr)
        print("     /ralph-loop Build a REST API for todos", file=sys.stderr)
        print("     /ralph-loop Fix the auth bug --max-iterations 20", file=sys.stderr)
        sys.exit(1)

    os.makedirs('.claude', exist_ok=True)

    if completion_promise and completion_promise != "null":
        completion_promise_yaml = f'"{completion_promise}"'
    else:
        completion_promise_yaml = "null"

    started_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    state_content = f"""---
active: true
iteration: 1
max_iterations: {max_iterations}
completion_promise: {completion_promise_yaml}
started_at: "{started_at}"
---

{prompt}
"""

    with open('.claude/ralph-loop.local.md', 'w', encoding='utf-8') as f:
        f.write(state_content)

    max_iter_display = str(max_iterations) if max_iterations > 0 else "unlimited"
    if completion_promise != "null":
        promise_display = f"{completion_promise} (ONLY output when TRUE - do not lie!)"
    else:
        promise_display = "none (runs forever)"

    print(f"""Ralph loop activated in this session!

Iteration: 1
Max iterations: {max_iter_display}
Completion promise: {promise_display}

The stop hook is now active. When you try to exit, the SAME PROMPT will be
fed back to you. You'll see your previous work in files, creating a
self-referential loop where you iteratively improve on the same task.

WARNING: This loop cannot be stopped manually! It will run infinitely
    unless you set --max-iterations or --completion-promise.
""")

    if prompt:
        print("")
        print(prompt)

    if completion_promise != "null":
        print("")
        print("=" * 59)
        print("CRITICAL - Ralph Loop Completion Promise")
        print("=" * 59)
        print("")
        print("To complete this loop, output this EXACT text:")
        print(f"  <promise>{completion_promise}</promise>")
        print("")
        print("STRICT REQUIREMENTS:")
        print("  - Use <promise> XML tags EXACTLY as shown above")
        print("  - The statement MUST be completely TRUE")
        print("  - Do NOT output false statements to exit the loop")
        print("=" * 59)


if __name__ == '__main__':
    main()
