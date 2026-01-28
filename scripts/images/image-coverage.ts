/**
 * Shared image coverage analysis utilities
 *
 * Used by:
 * - analyze-image-coverage.ts (reporting)
 * - generate-section-images.ts (prioritization)
 */

import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { getProjectRoot } from '../lib/file-utils';

// Status thresholds based on chars per image ratio
export const THRESHOLDS = {
  CRITICAL: 10000,   // > 10,000 chars/image = NEEDS IMAGES
  LOW: 5000,         // 5,000 - 10,000 = LOW COVERAGE
  MODERATE: 2000,    // 2,000 - 5,000 = MODERATE
  // < 2,000 = GOOD
};

export type CoverageStatus = 'NEEDS IMAGES' | 'LOW COVERAGE' | 'MODERATE' | 'GOOD';

export interface FileCoverage {
  filePath: string;
  relativePath: string;
  charCount: number;
  imageCount: number;
  ratio: number;
  status: CoverageStatus;
  sectionCount: number;
  sectionsWithoutImages: number;
}

export interface Section {
  title: string;
  level: number;
  charCount: number;
  hasImage: boolean;
  imageTypes: string[];
}

/**
 * Detect visual content types in content
 */
export function detectVisualContent(content: string): string[] {
  const types: string[] = [];

  // Markdown images: ![alt](path)
  if (/!\[.*?\]\(.*?\)/.test(content)) {
    types.push('markdown-image');
  }

  // Python code blocks that likely generate charts
  if (/```\{python\}[\s\S]*?(plt\.|fig\.|px\.|sns\.|alt\.)[\s\S]*?```/i.test(content)) {
    types.push('python-chart');
  }

  // R code blocks that likely generate plots
  if (/```\{r\}[\s\S]*?(ggplot|plot\(|geom_)[\s\S]*?```/i.test(content)) {
    types.push('r-plot');
  }

  // Observable JS blocks
  if (/```\{ojs\}/.test(content)) {
    types.push('observable-js');
  }

  // Mermaid diagrams
  if (/```\{?mermaid\}?/.test(content)) {
    types.push('mermaid-diagram');
  }

  // HTML img tags
  if (/<img\s+[^>]*src=/i.test(content)) {
    types.push('html-image');
  }

  // Quarto figure shortcodes
  if (/\{\{<\s*figure\s+/.test(content)) {
    types.push('quarto-figure');
  }

  // Quarto include of image files
  if (/\{\{<\s*include\s+.*\.(png|jpg|jpeg|gif|svg|webp)/i.test(content)) {
    types.push('quarto-include-image');
  }

  return types;
}

/**
 * Count all images/visual elements in content
 */
export function countImages(content: string): number {
  let count = 0;

  // Markdown images: ![alt](path)
  const markdownImages = content.match(/!\[.*?\]\(.*?\)/g) || [];
  count += markdownImages.length;

  // Python chart code blocks
  const pythonCharts = content.match(/```\{python\}[\s\S]*?(plt\.|fig\.|px\.|sns\.|alt\.)[\s\S]*?```/gi) || [];
  count += pythonCharts.length;

  // R plot code blocks
  const rPlots = content.match(/```\{r\}[\s\S]*?(ggplot|plot\(|geom_)[\s\S]*?```/gi) || [];
  count += rPlots.length;

  // Observable JS blocks
  const ojsBlocks = content.match(/```\{ojs\}/g) || [];
  count += ojsBlocks.length;

  // Mermaid diagrams
  const mermaidDiagrams = content.match(/```\{?mermaid\}?/g) || [];
  count += mermaidDiagrams.length;

  // HTML img tags
  const htmlImages = content.match(/<img\s+[^>]*src=/gi) || [];
  count += htmlImages.length;

  // Quarto figure shortcodes
  const quartoFigures = content.match(/\{\{<\s*figure\s+/g) || [];
  count += quartoFigures.length;

  // Quarto include of image files
  const quartoImageIncludes = content.match(/\{\{<\s*include\s+.*\.(png|jpg|jpeg|gif|svg|webp)/gi) || [];
  count += quartoImageIncludes.length;

  return count;
}

/**
 * Count characters in prose content (excluding frontmatter, code blocks, math blocks)
 */
export function countProseCharacters(body: string): number {
  let content = body;

  // Remove code blocks (```...```)
  content = content.replace(/```[\s\S]*?```/g, '');

  // Remove display math blocks ($$...$$)
  content = content.replace(/\$\$[\s\S]*?\$\$/g, '');

  // Remove LaTeX display math (\[...\])
  content = content.replace(/\\\[[\s\S]*?\\\]/g, '');

  // Remove Quarto shortcodes ({{< ... >}})
  content = content.replace(/\{\{<[\s\S]*?>\}\}/g, '');

  // Remove HTML comments
  content = content.replace(/<!--[\s\S]*?-->/g, '');

  // Remove markdown image syntax (already counted as images)
  content = content.replace(/!\[.*?\]\(.*?\)/g, '');

  // Count remaining characters (excluding whitespace-only)
  return content.replace(/\s+/g, ' ').trim().length;
}

/**
 * Parse content into sections and analyze each
 */
export function parseSections(body: string): Section[] {
  // Normalize line endings
  const normalizedBody = body.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  const lines = normalizedBody.split('\n');
  const sections: Section[] = [];
  const headingPattern = /^(#{2,3})\s+(.+)$/;

  let currentSection: { title: string; level: number; startIdx: number } | null = null;

  for (let i = 0; i <= lines.length; i++) {
    const line = lines[i] || '';
    const match = line.match(headingPattern);

    // Check if we hit a new section or end of file
    if (match || i === lines.length) {
      // Process previous section if exists
      if (currentSection) {
        const sectionContent = lines.slice(currentSection.startIdx, i).join('\n');
        const visualTypes = detectVisualContent(sectionContent);

        sections.push({
          title: currentSection.title,
          level: currentSection.level,
          charCount: countProseCharacters(sectionContent),
          hasImage: visualTypes.length > 0,
          imageTypes: visualTypes,
        });
      }

      // Start new section
      if (match) {
        currentSection = {
          title: match[2].trim(),
          level: match[1].length,
          startIdx: i,
        };
      }
    }
  }

  return sections;
}

/**
 * Determine coverage status based on ratio
 */
export function getStatus(ratio: number): CoverageStatus {
  if (ratio > THRESHOLDS.CRITICAL) return 'NEEDS IMAGES';
  if (ratio > THRESHOLDS.LOW) return 'LOW COVERAGE';
  if (ratio > THRESHOLDS.MODERATE) return 'MODERATE';
  return 'GOOD';
}

/**
 * Analyze a single file for image coverage
 */
export async function analyzeFileCoverage(filePath: string): Promise<FileCoverage> {
  const content = await fs.readFile(filePath, 'utf-8');
  const { content: body } = matter(content);

  const charCount = countProseCharacters(body);
  const imageCount = countImages(body);
  const sections = parseSections(body);

  const ratio = imageCount > 0 ? Math.round(charCount / imageCount) : charCount;
  const sectionsWithoutImages = sections.filter(s => !s.hasImage).length;

  return {
    filePath,
    relativePath: path.relative(getProjectRoot(), filePath),
    charCount,
    imageCount,
    ratio,
    status: getStatus(ratio),
    sectionCount: sections.length,
    sectionsWithoutImages,
  };
}

/**
 * Analyze multiple files and return sorted by worst coverage (highest ratio first)
 */
export async function analyzeFilesCoverage(
  filePaths: string[],
  options: { quiet?: boolean } = {}
): Promise<FileCoverage[]> {
  const { quiet = false } = options;
  const coverages: FileCoverage[] = [];

  for (const filePath of filePaths) {
    try {
      const coverage = await analyzeFileCoverage(filePath);
      coverages.push(coverage);
    } catch (error) {
      if (!quiet) {
        console.error(`  [WARN] Failed to analyze ${path.basename(filePath)}: ${error}`);
      }
    }
  }

  // Sort by ratio (highest first = most image-starved)
  coverages.sort((a, b) => b.ratio - a.ratio);

  return coverages;
}

/**
 * Sort file paths by coverage ratio (worst coverage first)
 * Returns the same files reordered by their image coverage needs
 */
export async function sortFilesByWorstCoverage(
  filePaths: string[],
  options: { quiet?: boolean } = {}
): Promise<string[]> {
  const coverages = await analyzeFilesCoverage(filePaths, options);
  return coverages.map(c => c.filePath);
}
