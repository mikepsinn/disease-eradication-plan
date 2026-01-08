#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ralph Loop Stop Hook (Windows-compatible Python version)
Prevents session exit when a ralph-loop is active
Feeds Claude's output back as input to continue the loop
"""

import sys
import os
import json
import re

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')  # type: ignore[union-attr]

RALPH_STATE_FILE = ".claude/ralph-loop.local.md"


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter and return (frontmatter_dict, body_text)."""
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
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            frontmatter[key] = value

    body = '\n'.join(lines[end_idx + 1:]).strip()
    return frontmatter, body


def extract_promise_text(text: str) -> str:
    """Extract text from <promise>...</promise> tags."""
    match = re.search(r'<promise>(.*?)</promise>', text, re.DOTALL)
    if match:
        return ' '.join(match.group(1).split())
    return ""


def main():
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    if not os.path.exists(RALPH_STATE_FILE):
        sys.exit(0)

    try:
        with open(RALPH_STATE_FILE, 'r', encoding='utf-8') as f:
            state_content = f.read()
    except Exception as e:
        print(f"Warning: Ralph loop: Cannot read state file: {e}", file=sys.stderr)
        sys.exit(0)

    frontmatter, prompt_text = parse_frontmatter(state_content)

    iteration_str = frontmatter.get('iteration', '')
    max_iterations_str = frontmatter.get('max_iterations', '0')
    completion_promise = frontmatter.get('completion_promise', 'null')

    try:
        iteration = int(iteration_str)
    except (ValueError, TypeError):
        print("Warning: Ralph loop: State file corrupted", file=sys.stderr)
        os.remove(RALPH_STATE_FILE)
        sys.exit(0)

    try:
        max_iterations = int(max_iterations_str)
    except (ValueError, TypeError):
        print("Warning: Ralph loop: State file corrupted", file=sys.stderr)
        os.remove(RALPH_STATE_FILE)
        sys.exit(0)

    if max_iterations > 0 and iteration >= max_iterations:
        print(f"Ralph loop: Max iterations ({max_iterations}) reached.")
        os.remove(RALPH_STATE_FILE)
        sys.exit(0)

    transcript_path = hook_input.get('transcript_path', '')

    if not transcript_path or not os.path.exists(transcript_path):
        print("Warning: Ralph loop: Transcript file not found", file=sys.stderr)
        os.remove(RALPH_STATE_FILE)
        sys.exit(0)

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Warning: Ralph loop: Cannot read transcript: {e}", file=sys.stderr)
        os.remove(RALPH_STATE_FILE)
        sys.exit(0)

    last_assistant_line = None
    for line in reversed(lines):
        if '"role":"assistant"' in line or '"role": "assistant"' in line:
            last_assistant_line = line
            break

    if not last_assistant_line:
        print("Warning: Ralph loop: No assistant messages found", file=sys.stderr)
        os.remove(RALPH_STATE_FILE)
        sys.exit(0)

    try:
        msg_data = json.loads(last_assistant_line)
        content_list = msg_data.get('message', {}).get('content', [])

        text_parts = []
        for block in content_list:
            if isinstance(block, dict) and block.get('type') == 'text':
                text_parts.append(block.get('text', ''))

        last_output = '\n'.join(text_parts)
    except json.JSONDecodeError as e:
        print(f"Warning: Ralph loop: Failed to parse JSON: {e}", file=sys.stderr)
        os.remove(RALPH_STATE_FILE)
        sys.exit(0)

    if not last_output:
        print("Warning: Ralph loop: No text content", file=sys.stderr)
        os.remove(RALPH_STATE_FILE)
        sys.exit(0)

    if completion_promise and completion_promise != 'null':
        promise_text = extract_promise_text(last_output)

        if promise_text and promise_text == completion_promise:
            print(f"Ralph loop: Detected <promise>{completion_promise}</promise>")
            os.remove(RALPH_STATE_FILE)
            sys.exit(0)

    next_iteration = iteration + 1

    if not prompt_text:
        print("Warning: Ralph loop: No prompt text found", file=sys.stderr)
        os.remove(RALPH_STATE_FILE)
        sys.exit(0)

    new_content = state_content.replace(
        f'iteration: {iteration}',
        f'iteration: {next_iteration}'
    )
    with open(RALPH_STATE_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    if completion_promise and completion_promise != 'null':
        system_msg = f"Ralph iteration {next_iteration} | To stop: output <promise>{completion_promise}</promise> (ONLY when TRUE!)"
    else:
        system_msg = f"Ralph iteration {next_iteration} | No completion promise set - loop runs infinitely"

    result = {
        "decision": "block",
        "reason": prompt_text,
        "systemMessage": system_msg
    }
    print(json.dumps(result, indent=2))

    sys.exit(0)


if __name__ == '__main__':
    main()
