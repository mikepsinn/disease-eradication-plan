import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUTPUT_FILE = os.path.join(ROOT_DIR, 'operations', 'refactor-manifest.md')
IGNORE_PATTERNS = {
    '.git',
    '.cursor',
    'node_modules',
    'package.json',
    'package-lock.json',
    'tsconfig.json',
    'scripts',
    'brand',
    '__pycache__',
    'requirements.txt',
    '.vscode'
}

def generate_manifest():
    print('Scanning repository to generate manifest...')
    all_paths = []

    for root, dirs, files in os.walk(ROOT_DIR, topdown=True):
        # Exclude ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_PATTERNS]
        
        # Get the relative path from the root directory
        relative_root = os.path.relpath(root, ROOT_DIR)
        if relative_root == '.':
            relative_root = ''

        for d in dirs:
            dir_path = os.path.join(relative_root, d).replace('\\', '/')
            all_paths.append(f"- [ ] KEEP ./{dir_path}/")

        for f in files:
            if f not in IGNORE_PATTERNS:
                file_path = os.path.join(relative_root, f).replace('\\', '/')
                all_paths.append(f"- [ ] KEEP ./{file_path}")

    manifest_content = generate_markdown(all_paths)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    print(f"Manifest successfully generated at {OUTPUT_FILE}")

def generate_markdown(paths):
    header = """---
title: "Refactor Manifest"
description: "A master list of all files and directories for the wiki refactoring. Curate this list to define the action for each item."
---

# Refactor Manifest

Curate this list by changing the action for each file or directory.
Valid actions are: **KEEP**, **MOVE**, **RENAME**, **DELETE**.

**Instructions:**
1.  Change `KEEP` to the desired action.
2.  For `MOVE`, provide the destination path after the source path (e.g., `MOVE ./old/path.md ./dFDA-protocol/new/path.md`).
3.  For `RENAME`, provide the new name after the old name (e.g., `RENAME ./old-name.md ./new-name.md`).
4.  Leave as `KEEP` for files that should not be touched.
5.  Change to `DELETE` for files that should be removed.

---

"""
    paths.sort()
    return header + '\n'.join(paths)

if __name__ == '__main__':
    generate_manifest()
