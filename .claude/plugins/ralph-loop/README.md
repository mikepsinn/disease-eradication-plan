# Ralph Loop - Windows Compatible Version

This directory contains Windows-compatible Python versions of the ralph-loop plugin scripts.

## Why This Exists

The official ralph-loop plugin uses Bash scripts that don't work on Windows:
- `.sh` files open in text editors instead of executing
- `jq` dependency isn't installed by default
- Known newline bug on Windows ([#12170](https://github.com/anthropics/claude-code/issues/12170))

## Files

| File | Purpose |
|------|---------|
| `setup-ralph-loop.py` | Initializes a Ralph loop session |
| `stop-hook.py` | Stop hook that continues the loop |
| `hooks.json` | Hook configuration (points to Python) |
| `ralph-loop.md` | Command definition (uses Python) |
| `install-windows-fix.py` | Installer script |

## Installation

If the plugin cache gets cleared or updated, reinstall with:

```bash
python .claude/plugins/ralph-loop/install-windows-fix.py
```

Then restart Claude Code.

## Usage

After installation, use normally:

```
/ralph-loop:ralph-loop "Your task here" --max-iterations 10 --completion-promise "DONE"
```

## Updating

If the official plugin adds Windows support, you can remove this workaround:

1. Delete this directory
2. Reinstall the plugin: `/plugin reinstall ralph-loop@claude-plugins-official`
