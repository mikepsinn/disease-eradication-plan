#!/usr/bin/env python3
"""
Auto-Regenerate Variables Hook
==============================

Triggers automatic regeneration of _variables.yml when parameters.py is modified.
Uses hash tracking to avoid redundant regeneration.

Usage:
  python .claude/hooks/auto-regen-variables.py <file_path>

Exit codes:
  0 - Success (or file not parameters.py)
  1 - Regeneration failed
"""

import sys
import subprocess
import hashlib
import json
import os
from pathlib import Path

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]


def get_project_root() -> Path:
    """Find project root by looking for _quarto.yml or _variables.yml."""
    current = Path(os.getcwd())
    while current != current.parent:
        if (current / '_quarto.yml').exists() or (current / '_variables.yml').exists():
            return current
        current = current.parent
    return Path(os.getcwd())


def get_file_hash(path: Path) -> str:
    """Calculate MD5 hash of file contents."""
    if not path.exists():
        return ""
    return hashlib.md5(path.read_bytes()).hexdigest()


def main():
    if len(sys.argv) < 2:
        sys.exit(0)

    file_path = sys.argv[1]

    # Only trigger for parameters.py
    if 'parameters.py' not in file_path:
        sys.exit(0)

    project_root = get_project_root()
    params_file = project_root / 'dih_models' / 'parameters.py'
    hash_cache = project_root / '.claude' / 'hooks' / '.param-hash.json'

    # If the edited file isn't the parameters file, skip
    if not params_file.exists():
        sys.exit(0)

    # Check if file actually changed
    current_hash = get_file_hash(params_file)
    cached_hash = ""

    if hash_cache.exists():
        try:
            cached_hash = json.loads(hash_cache.read_text()).get('hash', '')
        except Exception:
            pass

    if current_hash == cached_hash:
        # No change, skip regeneration
        sys.exit(0)

    # Determine Python executable
    venv_python = project_root / '.venv' / 'Scripts' / 'python.exe'
    if not venv_python.exists():
        venv_python = project_root / '.venv' / 'bin' / 'python'
    if not venv_python.exists():
        venv_python = Path('python')

    # Run regeneration script
    regen_script = project_root / 'scripts' / 'generate-everything-parameters-variables-calculations-references.py'

    if not regen_script.exists():
        result = {
            'status': 'skipped',
            'message': 'Regeneration script not found'
        }
        print(json.dumps(result))
        sys.exit(0)

    try:
        proc = subprocess.run(
            [str(venv_python), str(regen_script)],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            timeout=60
        )

        if proc.returncode == 0:
            # Update hash cache
            hash_cache.parent.mkdir(parents=True, exist_ok=True)
            hash_cache.write_text(json.dumps({'hash': current_hash}))

            result = {
                'status': 'regenerated',
                'message': '_variables.yml regenerated from parameters.py'
            }
            print(json.dumps(result))
            sys.exit(0)
        else:
            result = {
                'status': 'error',
                'message': f'Regeneration failed: {proc.stderr[:500] if proc.stderr else "Unknown error"}'
            }
            print(json.dumps(result))
            sys.exit(1)

    except subprocess.TimeoutExpired:
        result = {
            'status': 'timeout',
            'message': 'Regeneration timed out after 60 seconds'
        }
        print(json.dumps(result))
        sys.exit(1)
    except Exception as e:
        result = {
            'status': 'error',
            'message': f'Failed to run regeneration: {str(e)}'
        }
        print(json.dumps(result))
        sys.exit(1)


if __name__ == '__main__':
    main()
