#!/usr/bin/env node
/**
 * Fix cross-reference paths after AI agent architecture migration
 * Updates all relative paths to account for new file locations
 */

import * as fs from 'fs';
import * as path from 'path';
import { glob } from 'glob';

const PROJECT_ROOT = process.cwd();

// Helper to normalize paths
const normalizePath = (p: string) => p.replace(/\\/g, '/');

// Pattern replacements for different file locations
const FIX_PATTERNS = [
  // Fix redundant ./ prefix
  {
    from: /\.\/\.\.\//g,
    to: '../',
    description: 'Remove redundant ./ prefix'
  },

  // For files in knowledge/ root (like proof.qmd, problem.qmd, solution.qmd)
  // ../../knowledge/X → ../X (already in knowledge/)
  {
    from: /\.\.\/\.\.\/knowledge\//g,
    to: '../',
    description: 'Fix knowledge/ root file references',
    filePattern: /^knowledge\/[^\/]+\.qmd$/
  },

  // For files in knowledge/subdirs (like knowledge/appendix/, knowledge/problem/)
  // ../../../knowledge/X → ../../X (up 2 levels from knowledge/subdir/)
  {
    from: /\.\.\/\.\.\/\.\.\/knowledge\//g,
    to: '../../',
    description: 'Fix knowledge/ subdir file references',
    filePattern: /^knowledge\/[^\/]+\/[^\/]+\.qmd$/
  },

  //For files in knowledge/subdirs/subdirs (like knowledge/appendix/subdir/)
  // ../../../../knowledge/X → ../../../X (up 3 levels)
  {
    from: /\.\.\/\.\.\/\.\.\/\.\.\/knowledge\//g,
    to: '../../../',
    description: 'Fix knowledge/ deep subdir references',
    filePattern: /^knowledge\/[^\/]+\/[^\/]+\/[^\/]+\.qmd$/
  }
];

async function fixCrossReferences() {
  console.log('Fixing cross-reference paths after migration...\n');

  // Find all .qmd files
  const qmdFiles = await glob('**/*.qmd', {
    cwd: PROJECT_ROOT,
    ignore: ['node_modules/**', '_book/**', '.quarto/**']
  });

  let totalFixed = 0;
  let filesModified = 0;

  for (const file of qmdFiles) {
    const fullPath = path.join(PROJECT_ROOT, file);
    const normalizedFile = normalizePath(file);
    let content = fs.readFileSync(fullPath, 'utf-8');
    const originalContent = content;
    let fixCount = 0;

    // Apply each pattern
    for (const pattern of FIX_PATTERNS) {
      // If pattern has filePattern, check if this file matches
      if (pattern.filePattern && !pattern.filePattern.test(normalizedFile)) {
        continue;
      }

      const matches = content.match(pattern.from);
      if (matches) {
        content = content.replace(pattern.from, pattern.to);
        fixCount += matches.length;
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
