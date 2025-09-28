#!/usr/bin/env node

/**
 * Converts all .md files to .qmd in brain/book directory
 * Updates all internal links to point to .qmd files
 * Updates README.md table of contents
 */

import fs from 'fs';
import path from 'path';
import { glob } from 'glob';

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  blue: '\x1b[34m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// Step 1: Find all .md files in brain/book
function findMarkdownFiles() {
  const files = glob.globSync('brain/book/**/*.md', { nodir: true });
  log(`Found ${files.length} .md files to convert`, 'blue');
  return files;
}

// Step 2: Convert .md to .qmd (rename files)
function renameFiles(files) {
  let converted = 0;
  let skipped = 0;

  files.forEach(file => {
    const newFile = file.replace(/\.md$/, '.qmd');

    // Check if .qmd already exists
    if (fs.existsSync(newFile)) {
      log(`  Skipping ${file} (.qmd already exists)`, 'yellow');
      skipped++;
      return;
    }

    try {
      fs.renameSync(file, newFile);
      log(`  ✓ Converted ${path.basename(file)} → ${path.basename(newFile)}`, 'green');
      converted++;
    } catch (error) {
      log(`  ✗ Error converting ${file}: ${error.message}`, 'red');
    }
  });

  log(`\nConverted ${converted} files, skipped ${skipped}`, 'blue');
  return converted;
}

// Step 3: Update internal links in all .qmd files
function updateInternalLinks() {
  const qmdFiles = glob.globSync('brain/book/**/*.qmd', { nodir: true });
  let updatedFiles = 0;
  let totalReplacements = 0;

  qmdFiles.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    const originalContent = content;

    // Replace .md links with .qmd
    // Matches: [text](path/file.md) or [text](./path/file.md) or [text](../path/file.md)
    const mdLinkPattern = /(\[[^\]]*\]\([^)]*?)\.md(\)|#)/g;

    content = content.replace(mdLinkPattern, '$1.qmd$2');

    if (content !== originalContent) {
      fs.writeFileSync(file, content, 'utf8');
      const replacements = (content.match(/\.qmd/g) || []).length - (originalContent.match(/\.qmd/g) || []).length;
      updatedFiles++;
      totalReplacements += replacements;
      log(`  Updated ${replacements} links in ${path.basename(file)}`, 'green');
    }
  });

  log(`\nUpdated ${totalReplacements} links across ${updatedFiles} files`, 'blue');
}

// Step 4: Update README.md table of contents
function updateReadme() {
  const readmePath = 'README.md';

  if (!fs.existsSync(readmePath)) {
    log('README.md not found', 'yellow');
    return;
  }

  let content = fs.readFileSync(readmePath, 'utf8');
  const originalContent = content;

  // Replace brain/book/**/*.md links with .qmd
  const tocPattern = /(\(\.\/brain\/book\/[^)]*?)\.md(\)|#)/g;
  content = content.replace(tocPattern, '$1.qmd$2');

  if (content !== originalContent) {
    fs.writeFileSync(readmePath, content, 'utf8');
    const replacements = (content.match(/\.qmd/g) || []).length - (originalContent.match(/\.qmd/g) || []).length;
    log(`Updated ${replacements} links in README.md`, 'green');
  } else {
    log('No updates needed in README.md', 'yellow');
  }
}

// Step 5: Update _quarto.yml if needed
function updateQuartoConfig() {
  const quartoPath = '_quarto.yml';

  if (!fs.existsSync(quartoPath)) {
    log('_quarto.yml not found', 'yellow');
    return;
  }

  let content = fs.readFileSync(quartoPath, 'utf8');
  const originalContent = content;

  // Replace .md references with .qmd in chapter listings
  const chapterPattern = /^(\s*- )(.*?)\.md$/gm;
  content = content.replace(chapterPattern, '$1$2.qmd');

  if (content !== originalContent) {
    fs.writeFileSync(quartoPath, content, 'utf8');
    const replacements = (content.match(/\.qmd/g) || []).length - (originalContent.match(/\.qmd/g) || []).length;
    log(`Updated ${replacements} references in _quarto.yml`, 'green');
  } else {
    log('No updates needed in _quarto.yml', 'yellow');
  }
}

// Main execution
function main() {
  log('\n=== Converting .md files to .qmd ===\n', 'blue');

  // Note: glob should already be installed as a dependency

  const files = findMarkdownFiles();

  if (files.length === 0) {
    log('No .md files found to convert', 'yellow');
    return;
  }

  log('\n--- Step 1: Renaming files ---', 'blue');
  const converted = renameFiles(files);

  if (converted > 0) {
    log('\n--- Step 2: Updating internal links ---', 'blue');
    updateInternalLinks();

    log('\n--- Step 3: Updating README.md ---', 'blue');
    updateReadme();

    log('\n--- Step 4: Updating _quarto.yml ---', 'blue');
    updateQuartoConfig();
  }

  log('\n=== Conversion complete! ===\n', 'green');
  log('Next steps:', 'blue');
  log('1. Run "git status" to review changes', 'yellow');
  log('2. Run "quarto preview" to test the build', 'yellow');
  log('3. Commit the changes', 'yellow');
}

// Run the script
main();