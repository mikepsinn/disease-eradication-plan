#!/usr/bin/env node
/**
 * Fix cross-site QMD links for PDF builds
 *
 * This script scans all Quarto config files to build a mapping of QMD files to their
 * published site URLs, then replaces internal .qmd links with external URLs where appropriate.
 *
 * This fixes PDF build failures caused by cross-references to QMD files that aren't
 * included in the current project's render list.
 *
 * Usage:
 *   npx tsx scripts/fix-cross-site-links.ts [--dry-run]
 *
 * Options:
 *   --dry-run    Show what would be changed without making changes
 *
 * Examples:
 *   npx tsx scripts/fix-cross-site-links.ts --dry-run
 *   npx tsx scripts/fix-cross-site-links.ts
 */

import fs from 'fs/promises';
import * as fsSync from 'fs';
import path from 'path';
import { glob } from 'glob';
import yaml from 'js-yaml';
import { getProjectRoot } from './lib/file-utils.js';

const PROJECT_ROOT = getProjectRoot();

interface QuartoConfig {
  configFile: string;
  indexSource: string;  // The main QMD file (from dih-render.index-source)
  siteUrl: string;      // The published site URL
}

interface LinkReplacement {
  file: string;
  line: number;
  oldLink: string;
  newLink: string;
}

interface FixResult {
  configsFound: number;
  qmdToUrlMap: Map<string, string>;
  filesScanned: number;
  filesModified: number;
  totalReplacements: number;
  replacements: LinkReplacement[];
}

/**
 * Parse all _quarto-*.yml files to build QMD → site-url mapping
 */
async function buildQmdToUrlMap(): Promise<Map<string, string>> {
  const qmdToUrl = new Map<string, string>();

  // Find all Quarto config files
  const configFiles = await glob('_quarto*.yml', {
    cwd: PROJECT_ROOT,
    absolute: true,
  });

  console.log(`Found ${configFiles.length} Quarto config files`);

  for (const configFile of configFiles) {
    try {
      const content = await fs.readFile(configFile, 'utf-8');
      const doc = yaml.load(content) as Record<string, any>;

      // Get site URL (check website.site-url first, then book.site-url)
      let siteUrl = doc?.website?.['site-url'] || doc?.book?.['site-url'];
      if (!siteUrl) continue;

      // Get index source from dih-render section
      const indexSource = doc?.['dih-render']?.['index-source'];
      if (!indexSource) continue;

      // Normalize the QMD path (relative to project root)
      const normalizedQmd = indexSource.replace(/\\/g, '/');

      // Also get the basename for matching relative links
      const qmdBasename = path.basename(normalizedQmd);

      // Map both the full path and just the filename
      qmdToUrl.set(normalizedQmd, siteUrl);
      qmdToUrl.set(qmdBasename, siteUrl);

      // Also handle paths that might be referenced without 'knowledge/' prefix
      if (normalizedQmd.startsWith('knowledge/')) {
        const withoutKnowledge = normalizedQmd.replace('knowledge/', '');
        qmdToUrl.set(withoutKnowledge, siteUrl);
      }

      console.log(`  ${path.basename(configFile)}: ${qmdBasename} -> ${siteUrl}`);
    } catch (error) {
      console.error(`  Error parsing ${path.basename(configFile)}:`, error);
    }
  }

  return qmdToUrl;
}

/**
 * Find and replace internal QMD links with external URLs
 */
async function fixLinksInFile(
  filePath: string,
  qmdToUrl: Map<string, string>,
  dryRun: boolean
): Promise<LinkReplacement[]> {
  const replacements: LinkReplacement[] = [];
  let content = await fs.readFile(filePath, 'utf-8');
  const originalContent = content;
  const lines = content.split('\n');

  // Regex to match markdown links pointing to .qmd files
  // Matches: [text](path/to/file.qmd) or [text](file.qmd#anchor)
  const linkRegex = /\[([^\]]+)\]\(([^)]*\.qmd(?:#[^)]*)?)\)/g;

  let match;
  while ((match = linkRegex.exec(originalContent)) !== null) {
    const fullMatch = match[0];
    const linkText = match[1];
    const qmdPath = match[2];

    // Extract just the file path (without anchor)
    const [filePart, anchor] = qmdPath.split('#');

    // Normalize the path for lookup
    const normalizedPath = filePart.replace(/\\/g, '/').replace(/^\.\.\/+/g, '').replace(/^\.\//, '');

    // Try to find a matching URL
    let siteUrl: string | undefined;

    // Try exact match first
    siteUrl = qmdToUrl.get(normalizedPath);

    // Try just the filename
    if (!siteUrl) {
      const basename = path.basename(normalizedPath);
      siteUrl = qmdToUrl.get(basename);
    }

    // Try with different path prefixes
    if (!siteUrl) {
      for (const [qmdKey, url] of qmdToUrl.entries()) {
        if (qmdKey.endsWith(normalizedPath) || normalizedPath.endsWith(qmdKey)) {
          siteUrl = url;
          break;
        }
      }
    }

    if (siteUrl) {
      // Build the new link (with anchor if present)
      const newUrl = anchor ? `${siteUrl}#${anchor}` : siteUrl;
      const newLink = `[${linkText}](${newUrl})`;

      // Find line number for this match
      const textBeforeMatch = originalContent.substring(0, match.index);
      const lineNumber = textBeforeMatch.split('\n').length;

      replacements.push({
        file: path.relative(PROJECT_ROOT, filePath),
        line: lineNumber,
        oldLink: fullMatch,
        newLink: newLink,
      });

      // Replace in content
      content = content.replace(fullMatch, newLink);
    }
  }

  // Write file if changes were made
  if (replacements.length > 0 && !dryRun) {
    await fs.writeFile(filePath, content, 'utf-8');
  }

  return replacements;
}

/**
 * Main function
 */
async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');

  const modeLabel = dryRun ? ' [DRY RUN]' : '';

  console.log('='.repeat(80));
  console.log(`Cross-Site Link Fixer${modeLabel}`);
  console.log('='.repeat(80));
  console.log('');

  // Step 1: Build QMD to URL mapping
  console.log('Step 1: Parsing Quarto configs to build QMD -> URL mapping...');
  console.log('');
  const qmdToUrl = await buildQmdToUrlMap();
  console.log('');
  console.log(`Found ${qmdToUrl.size} QMD -> URL mappings`);
  console.log('');

  // Step 2: Find all QMD files to scan
  console.log('Step 2: Scanning QMD files for internal links...');
  const qmdFiles = await glob('knowledge/**/*.qmd', {
    cwd: PROJECT_ROOT,
    absolute: true,
    ignore: ['**/node_modules/**', '**/_site/**', '**/_book/**'],
  });

  console.log(`Found ${qmdFiles.length} QMD files to scan`);
  console.log('');

  // Step 3: Process each file
  const result: FixResult = {
    configsFound: qmdToUrl.size,
    qmdToUrlMap: qmdToUrl,
    filesScanned: qmdFiles.length,
    filesModified: 0,
    totalReplacements: 0,
    replacements: [],
  };

  for (const file of qmdFiles) {
    const replacements = await fixLinksInFile(file, qmdToUrl, dryRun);
    if (replacements.length > 0) {
      result.filesModified++;
      result.totalReplacements += replacements.length;
      result.replacements.push(...replacements);
    }
  }

  // Print results
  console.log('='.repeat(80));
  console.log('Results');
  console.log('='.repeat(80));
  console.log('');

  if (result.replacements.length > 0) {
    console.log('Replacements:');
    console.log('');

    // Group by file
    const byFile = new Map<string, LinkReplacement[]>();
    for (const r of result.replacements) {
      if (!byFile.has(r.file)) {
        byFile.set(r.file, []);
      }
      byFile.get(r.file)!.push(r);
    }

    for (const [file, reps] of byFile.entries()) {
      console.log(`  ${file}:`);
      for (const r of reps) {
        console.log(`    Line ${r.line}:`);
        console.log(`      - ${r.oldLink}`);
        console.log(`      + ${r.newLink}`);
      }
      console.log('');
    }
  } else {
    console.log('No internal QMD links found that need fixing.');
    console.log('');
  }

  console.log('Summary:');
  console.log(`  Configs parsed:     ${result.configsFound}`);
  console.log(`  Files scanned:      ${result.filesScanned}`);
  console.log(`  Files modified:     ${result.filesModified}`);
  console.log(`  Total replacements: ${result.totalReplacements}`);
  console.log('');

  if (dryRun && result.totalReplacements > 0) {
    console.log('DRY RUN - No files were modified. Run without --dry-run to apply changes.');
  } else if (result.totalReplacements > 0) {
    console.log('Done! All cross-site links have been fixed.');
  }

  console.log('='.repeat(80));
}

main().catch((error) => {
  console.error('Error:', error);
  process.exit(1);
});
