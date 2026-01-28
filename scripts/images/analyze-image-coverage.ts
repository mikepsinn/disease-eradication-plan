/**
 * Analyze QMD files for image coverage
 *
 * Generates a ranked list of QMD files by their character-to-image ratio,
 * identifying which files are most "image-starved" and would benefit from
 * generated images.
 *
 * Metrics calculated:
 * - Character count (excluding frontmatter, code blocks, math blocks)
 * - Image count (markdown images, Python/R charts, Quarto figures, includes)
 * - Ratio: chars / images (higher = more text per image = needs more images)
 * - Section count (H2/H3 headings)
 * - Sections without images
 *
 * Usage:
 *   npx tsx scripts/images/analyze-image-coverage.ts              # Ranked list to stdout
 *   npx tsx scripts/images/analyze-image-coverage.ts --json       # JSON output
 *   npx tsx scripts/images/analyze-image-coverage.ts --needs-images  # Only files needing images
 *   npx tsx scripts/images/analyze-image-coverage.ts file.qmd --sections  # Section-level detail
 */

import path from 'path';
import fs from 'fs/promises';
import { existsSync } from 'fs';
import matter from 'gray-matter';
import { getAllQmdFilesWithFrontmatter, getProjectRoot } from '../lib/file-utils';
import {
  THRESHOLDS,
  FileCoverage,
  Section,
  analyzeFileCoverage,
  analyzeFilesCoverage,
  parseSections,
  detectVisualContent,
  countProseCharacters,
  getStatus,
} from './image-coverage';

// Extended interface for section-level detail
interface FileCoverageWithSections extends FileCoverage {
  sections?: Section[];
}

/**
 * Analyze a single file for image coverage (with optional section detail)
 */
async function analyzeFile(filePath: string, includeSections: boolean = false): Promise<FileCoverageWithSections> {
  const baseCoverage = await analyzeFileCoverage(filePath);

  if (!includeSections) {
    return baseCoverage;
  }

  // Add section details
  const content = await fs.readFile(filePath, 'utf-8');
  const { content: body } = matter(content);
  const sections = parseSections(body);

  return {
    ...baseCoverage,
    sections,
  };
}

/**
 * Format ratio for display (adds commas)
 */
function formatRatio(ratio: number): string {
  return ratio.toLocaleString();
}

/**
 * Truncate path for display
 */
function truncatePath(p: string, maxLen: number): string {
  if (p.length <= maxLen) return p.padEnd(maxLen);
  return p.slice(0, maxLen - 3) + '...';
}

/**
 * Print table report
 */
function printTableReport(files: FileCoverage[], showAll: boolean = true): void {
  console.log('\nQMD Image Coverage Report');
  console.log('='.repeat(100));
  console.log('');
  console.log('Rank | File                                     | Chars   | Images | Ratio   | Status');
  console.log('-----|------------------------------------------|---------|--------|---------|-------------');

  const filtered = showAll ? files : files.filter(f => f.status !== 'GOOD');

  filtered.forEach((file, idx) => {
    const rank = String(idx + 1).padStart(4);
    const filePath = truncatePath(file.relativePath, 40);
    const chars = String(file.charCount).padStart(7);
    const images = String(file.imageCount).padStart(6);
    const ratio = formatRatio(file.ratio).padStart(7);
    const status = file.status.padEnd(12);

    console.log(`${rank} | ${filePath} | ${chars} | ${images} | ${ratio} | ${status}`);
  });

  console.log('');
  console.log('='.repeat(100));
  console.log('');

  // Summary stats
  const needsImages = files.filter(f => f.status === 'NEEDS IMAGES').length;
  const lowCoverage = files.filter(f => f.status === 'LOW COVERAGE').length;
  const moderate = files.filter(f => f.status === 'MODERATE').length;
  const good = files.filter(f => f.status === 'GOOD').length;

  console.log('Summary:');
  console.log(`  NEEDS IMAGES (>${THRESHOLDS.CRITICAL} chars/img): ${needsImages} files`);
  console.log(`  LOW COVERAGE (${THRESHOLDS.LOW}-${THRESHOLDS.CRITICAL}): ${lowCoverage} files`);
  console.log(`  MODERATE (${THRESHOLDS.MODERATE}-${THRESHOLDS.LOW}): ${moderate} files`);
  console.log(`  GOOD (<${THRESHOLDS.MODERATE}): ${good} files`);
  console.log('');
}

/**
 * Print section-level detail for a single file
 */
function printSectionDetail(file: FileCoverage): void {
  console.log(`\nSection-Level Analysis: ${file.relativePath}`);
  console.log('='.repeat(80));
  console.log('');
  console.log(`Overall: ${file.charCount} chars, ${file.imageCount} images, ratio ${formatRatio(file.ratio)} (${file.status})`);
  console.log(`Sections: ${file.sectionCount} total, ${file.sectionsWithoutImages} without images`);
  console.log('');
  console.log('Lvl | Section                                   | Chars  | Image? | Types');
  console.log('----|-------------------------------------------|--------|--------|------------------');

  if (file.sections) {
    file.sections.forEach(section => {
      const level = `H${section.level}`.padEnd(3);
      const title = truncatePath(section.title, 41);
      const chars = String(section.charCount).padStart(6);
      const hasImg = section.hasImage ? 'YES' : 'NO ';
      const types = section.imageTypes.join(', ') || '-';

      console.log(`${level} | ${title} | ${chars} | ${hasImg}    | ${types}`);
    });
  }

  console.log('');
}

/**
 * Helper to log only when not in JSON mode
 */
let quietMode = false;
function log(...args: any[]): void {
  if (!quietMode) {
    console.log(...args);
  }
}

async function main() {
  const args = process.argv.slice(2);

  const jsonOutput = args.includes('--json');
  const needsImagesOnly = args.includes('--needs-images');
  const showSections = args.includes('--sections');
  const specificFile = args.find(arg => arg.endsWith('.qmd'));

  // Suppress console output for JSON mode
  quietMode = jsonOutput;

  // Single file mode with --sections
  if (specificFile && showSections) {
    const filePath = path.isAbsolute(specificFile)
      ? specificFile
      : path.join(getProjectRoot(), specificFile);

    if (!existsSync(filePath)) {
      console.error(`[ERROR] File not found: ${specificFile}`);
      process.exit(1);
    }

    const coverage = await analyzeFile(filePath, true);

    if (jsonOutput) {
      console.log(JSON.stringify(coverage, null, 2));
    } else {
      printSectionDetail(coverage);
    }
    return;
  }

  // Batch mode - analyze all files
  log('[*] Scanning all QMD files...');

  // Temporarily suppress console output from getAllQmdFilesWithFrontmatter for JSON mode
  const originalConsoleLog = console.log;
  if (jsonOutput) {
    console.log = () => {};
  }

  const allFiles = await getAllQmdFilesWithFrontmatter();

  // Restore console.log
  if (jsonOutput) {
    console.log = originalConsoleLog;
  }

  // Filter out index.qmd files (they're typically navigation only)
  const qmdFiles = allFiles.filter(f => !f.endsWith('index.qmd'));
  log(`[OK] Found ${qmdFiles.length} QMD files\n`);

  log('[*] Analyzing image coverage...');

  // Use shared function to analyze and sort by worst coverage
  const coverages = await analyzeFilesCoverage(qmdFiles, { quiet: jsonOutput });

  // Filter if needed
  const filtered = needsImagesOnly
    ? coverages.filter(c => c.status === 'NEEDS IMAGES' || c.status === 'LOW COVERAGE')
    : coverages;

  if (jsonOutput) {
    console.log(JSON.stringify(filtered, null, 2));
  } else {
    printTableReport(filtered, !needsImagesOnly);
  }
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
