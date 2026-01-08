#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple hook logger - append to .claude/hooks/hooks.log
Import and call log_hook(hook_name, message) from any hook
"""
import os
import sys
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), 'hooks.log')

def log_hook(hook_name: str, message: str = "executed"):
    """Append a timestamped entry to hooks.log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {hook_name}: {message}\n")
    except Exception as e:
        print(f"[hook-logger] Failed to write log: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Test the logger
    log_hook("test", "Hook logger is working")
    print(f"Logged to: {LOG_FILE}")
