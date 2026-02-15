/**
 * Thin utility layer for audit scripts.
 * Wraps existing lib/file-utils.ts functions with audit-specific helpers.
 */
import fs from 'fs/promises';
import * as fsSync from 'fs';
import path from 'path';
import {
  getProjectRoot,
  getBookFilesForProcessing,
  getCleanedContentForLLM,
  readFileWithMatter,
} from '../lib/file-utils.js';

export { getProjectRoot, getBookFilesForProcessing };

const ROOT = getProjectRoot();

export interface BookFile {
  filename: string;
  title: string;
  content: string;
  wordCount: number;
}

/**
 * Read book files and return cleaned content ready for LLM.
 * Uses getCleanedContentForLLM which replaces {{< var >}} and strips markup.
 * @param filePatterns Optional list of relative paths. If omitted, reads all book files from _quarto-manual.yml.
 */
export async function readBookFilesForLLM(filePatterns?: string[]): Promise<BookFile[]> {
  const relativePaths = filePatterns ?? await getBookFilesForProcessing();

  const files: BookFile[] = [];
  for (const relPath of relativePaths) {
    const absPath = path.join(ROOT, relPath);

    // Skip files that don't exist on disk (e.g., index.qmd is generated at render time from index-manual.qmd)
    if (!fsSync.existsSync(absPath)) {
      console.warn(`  [SKIP] ${relPath} (file not found on disk)`);
      continue;
    }

    const content = await getCleanedContentForLLM(absPath);
    const { frontmatter } = await readFileWithMatter(absPath);
    const wordCount = content.trim().split(/\s+/).filter(w => w.length > 0).length;
    files.push({
      filename: relPath,
      title: (frontmatter.title as string) || relPath,
      content: content.trim(),
      wordCount,
    });
  }
  return files;
}

/**
 * Concatenate book files into a single text block with clear file markers.
 */
export function buildBookText(files: BookFile[], labelFn?: (f: BookFile) => string): string {
  return files.map(f => {
    const label = labelFn ? `[${labelFn(f)}] ` : '';
    return [
      '',
      '='.repeat(60),
      `${label}FILE: ${f.filename}`,
      `TITLE: ${f.title}`,
      `WORDS: ${f.wordCount}`,
      '='.repeat(60),
      f.content,
    ].join('\n');
  }).join('\n\n');
}

/**
 * Write a markdown analysis file to the project root.
 */
export async function writeAnalysis(filename: string, content: string): Promise<string> {
  const outputPath = path.join(ROOT, filename);
  await fs.writeFile(outputPath, content, 'utf-8');
  return outputPath;
}
