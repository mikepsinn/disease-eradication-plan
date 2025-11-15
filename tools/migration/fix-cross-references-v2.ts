#!/usr/bin/env node
/**
 * Fix cross-reference paths after AI agent architecture migration
 * Properly calculates relative paths between moved files
 */

import * as fs from 'fs';
import * as path from 'path';
import { glob } from 'glob';

const PROJECT_ROOT = process.cwd();

// Normalize paths to forward slashes
const normalizePath = (p: string) => p.replace(/\\/g, '/');

// Calculate relative path from one file to another
function getRelativePath(fromFile: string, toFile: string): string {
  const fromDir = path.dirname(fromFile);
  const relativePath = path.relative(fromDir, toFile);
  return normalizePath(relativePath);
}

async function fixCrossReferences() {
  console.log('Fixing cross-reference paths after migration...\n');

  // Find all .qmd files
  const qmdFiles = await glob('**/*.qmd', {
    cwd: PROJECT_ROOT,
    ignore: ['node_modules/**', '_book/**', '.quarto/**', '_freeze/**']
  });

  // Create a map of all .qmd files for quick lookup
  const fileMap = new Map<string, string>();
  for (const file of qmdFiles) {
    const normalized = normalizePath(file);
    const basename = path.basename(file);
    fileMap.set(basename, normalized);
    fileMap.set(normalized, normalized);
  }

  let totalFixed = 0;
  let filesModified = 0;

  // Regex to match markdown links: [text](path.qmd) or [text](path.qmd#anchor)
  const linkPattern = /\[([^\]]+)\]\(([^)]+\.qmd[^)]*)\)/g;

  for (const file of qmdFiles) {
    const fullPath = path.join(PROJECT_ROOT, file);
    const normalizedFile = normalizePath(file);
    let content = fs.readFileSync(fullPath, 'utf-8');
    const originalContent = content;
    let fixCount = 0;

    // Find all links in the file
    const matches = Array.from(content.matchAll(linkPattern));

    for (const match of matches) {
      const linkText = match[1];
      const linkPath = match[2];
      const fullMatch = match[0];

      // Skip external URLs
      if (linkPath.startsWith('http://') || linkPath.startsWith('https://')) {
        continue;
      }

      // Extract the path and anchor (if any)
      const [pathPart, anchor] = linkPath.split('#');

      // Try to resolve the old path to find what file it was referencing
      let targetFile: string | null = null;

      // Check if path contains knowledge/ - this means it was probably an absolute-ish path
      if (pathPart.includes('knowledge/')) {
        // Extract the part after knowledge/
        const afterKnowledge = pathPart.substring(pathPart.indexOf('knowledge/') + 'knowledge/'.length);
        targetFile = `knowledge/${afterKnowledge}`;
      } else {
        // It's a relative path - try to resolve it from the current file's location
        const fromDir = path.dirname(fullPath);
        const resolved = path.resolve(fromDir, pathPart);
        const relativeToCwd = path.relative(PROJECT_ROOT, resolved);
        targetFile = normalizePath(relativeToCwd);
      }

      // Check if the target file exists
      if (targetFile && fs.existsSync(path.join(PROJECT_ROOT, targetFile))) {
        // Calculate the correct relative path
        const correctRelPath = getRelativePath(normalizedFile, targetFile);

        // Reconstruct the link with anchor if present
        const newLinkPath = anchor ? `${correctRelPath}#${anchor}` : correctRelPath;

        // Only replace if the path actually changed
        if (newLinkPath !== linkPath) {
          const newMatch = `[${linkText}](${newLinkPath})`;
          content = content.replace(fullMatch, newMatch);
          fixCount++;
        }
      }
    }

    if (content !== originalContent) {
      fs.writeFileSync(fullPath, content);
      filesModified++;
      totalFixed += fixCount;
      console.log(`✅ Fixed ${fixCount} references in ${file}`);
    }
  }

  console.log(`\n✅ Fixed ${totalFixed} cross-references in ${filesModified} files\n`);
}

fixCrossReferences().catch(console.error);
