import * as fs from 'fs';
import * as path from 'path';

const ROOT_DIR = path.resolve(__dirname, '..');
const OUTPUT_FILE = path.join(ROOT_DIR, 'operations', 'refactor-manifest.md');
const IGNORE_PATTERNS = new Set([
    '.git',
    '.cursor',
    'node_modules',
    'package.json',
    'package-lock.json',
    'tsconfig.json',
    'scripts', // Ignore the scripts directory itself
    'brand', // Ignore the empty brand directory for now
]);

async function generateManifest() {
    console.log('Scanning repository to generate manifest...');
    const allPaths: string[] = [];

    function walkDir(currentDir: string, relativePath: string = '.') {
        const entries = fs.readdirSync(currentDir, { withFileTypes: true });

        for (const entry of entries) {
            if (IGNORE_PATTERNS.has(entry.name)) {
                continue;
            }

            const entryRelativePath = path.join(relativePath, entry.name).replace(/\\/g, '/');
            
            if (entry.isDirectory()) {
                allPaths.push(`- [ ] KEEP ${entryRelativePath}/`);
                walkDir(path.join(currentDir, entry.name), entryRelativePath);
            } else {
                allPaths.push(`- [ ] KEEP ${entryRelativePath}`);
            }
        }
    }

    walkDir(ROOT_DIR);

    const manifestContent = generateMarkdown(allPaths);
    fs.writeFileSync(OUTPUT_FILE, manifestContent);
    console.log(`Manifest successfully generated at ${OUTPUT_FILE}`);
}

function generateMarkdown(paths: string[]): string {
    const header = `---
title: "Refactor Manifest"
description: "A master list of all files and directories for the wiki refactoring. Curate this list to define the action for each item."
---

# Refactor Manifest

Curate this list by changing the action for each file or directory.
Valid actions are: **KEEP**, **MOVE**, **RENAME**, **DELETE**.

**Instructions:**
1.  Change \`KEEP\` to the desired action.
2.  For \`MOVE\`, provide the destination path after the source path (e.g., \`MOVE ./old/path.md ./dFDA-protocol/new/path.md\`).
3.  For \`RENAME\`, provide the new name after the old name (e.g., \`RENAME ./old-name.md ./new-name.md\`).
4.  Leave as \`KEEP\` for files that should not be touched.
5.  Change to \`DELETE\` for files that should be removed.

---

`;
    // Sort paths alphabetically for consistency
    paths.sort((a, b) => a.localeCompare(b));
    return header + paths.join('\n');
}

generateManifest().catch(console.error);
