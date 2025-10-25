import fs from 'fs/promises';
import matter from 'gray-matter';
import { glob } from 'glob';
import ignore from 'ignore';
import { getBodyHash } from './file-utils';

export interface BookStructure {
  chapters: string[];
  appendices: string[];
}

/**
 * Parses _quarto.yml to extract chapter and appendix file paths
 */
export async function parseQuartoYml(): Promise<BookStructure> {
  const quartoYmlContent = await fs.readFile('_quarto.yml', 'utf-8');
  const chapters: string[] = [];
  const appendices: string[] = [];

  const lines = quartoYmlContent.split('\n');
  let inAppendices = false;
  let inChapters = false;

  for (const line of lines) {
    // Only recognize top-level (2-space indentation) chapters: and appendices:
    // This prevents nested chapters: inside appendices from switching modes
    const trimmedLine = line.trimStart();
    const indentLevel = line.length - trimmedLine.length;

    // Top-level book.chapters: has 2 spaces of indentation
    if (trimmedLine === 'chapters:' && indentLevel === 2) {
      inChapters = true;
      inAppendices = false;
      continue;
    }

    // Top-level book.appendices: has 2 spaces of indentation
    if (trimmedLine === 'appendices:' && indentLevel === 2) {
      inAppendices = true;
      inChapters = false;
      continue;
    }

    // Reset when we hit a top-level key (no indentation)
    if (!line.startsWith(' ') && !line.startsWith('\t') && line.includes(':')) {
      inChapters = false;
      inAppendices = false;
    }

    const match = line.match(/^\s*-\s+(brain\/[^\s]+\.qmd)/);
    if (match) {
      if (inAppendices) {
        appendices.push(match[1]);
      } else if (inChapters) {
        chapters.push(match[1]);
      }
    }
  }

  return { chapters, appendices };
}

/**
 * Find all .qmd files where the content hash doesn't match the stored hash
 */
export async function getStaleFiles(hashFieldName: string, basePath?: string): Promise<string[]> {
  const gitignoreContent = await fs.readFile('.gitignore', 'utf-8');
  const ig = ignore().add(gitignoreContent);

  const searchPattern = basePath ? `${basePath}/**/*.qmd` : '**/*.qmd';
  const allQmdFiles = glob.sync(searchPattern, { ignore: 'node_modules/**' });
  const qmdFiles = ig.filter(allQmdFiles);

  const staleFiles: string[] = [];

  for (const file of qmdFiles) {
    try {
      const content = await fs.readFile(file, 'utf-8');
      const { data: frontmatter } = matter(content);

      const lastHash = frontmatter[hashFieldName];
      const currentBodyHash = getBodyHash(content);

      if (currentBodyHash !== lastHash) {
        staleFiles.push(file);
      }
    } catch (error) {
      console.error(`Error processing file ${file}:`, error);
    }
  }

  return staleFiles;
}
