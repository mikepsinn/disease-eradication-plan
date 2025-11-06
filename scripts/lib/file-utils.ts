import fs from 'fs/promises';
import * as fsSync from 'fs';
import matter from 'gray-matter';
import yaml from 'js-yaml';
import { glob } from 'glob';
import * as path from 'path';
import ignore from 'ignore';
import crypto from 'crypto';

/**
 * Find the project root by looking for package.json
 * Starts from the current file's directory and walks up
 * This ensures scripts work regardless of where they're run from
 */
export function getProjectRoot(): string {
  // Start from the current working directory
  let currentPath = process.cwd();

  // Keep going up until we find package.json or reach the root
  while (currentPath !== path.parse(currentPath).root) {
    const packageJsonPath = path.join(currentPath, 'package.json');

    if (fsSync.existsSync(packageJsonPath)) {
      return currentPath;
    }

    // Move up one directory
    currentPath = path.dirname(currentPath);
  }

  // If we couldn't find it by going up, check if we're already in the right place
  if (fsSync.existsSync(path.join(process.cwd(), 'package.json'))) {
    return process.cwd();
  }

  throw new Error('Could not find project root (no package.json found)');
}

const ROOT_DIR = getProjectRoot();
const IGNORE_PATTERNS = ['.git', '.cursor', 'node_modules', 'scripts', 'brand', '.venv', '_book'];

export async function getGitignorePatterns(): Promise<string[]> {
    const gitignorePath = path.join(ROOT_DIR, '.gitignore');
    try {
        const gitignoreContent = await fs.readFile(gitignorePath, 'utf-8');
        return gitignoreContent.split('\n').filter(line => line.trim() && !line.startsWith('#'));
    } catch (error) {
        console.error("Could not read .gitignore file:", error);
        return [];
    }
}

export async function findFiles(pattern: string): Promise<string[]> {
    const gitignore = ignore().add(await getGitignorePatterns());
    const files = await glob(pattern, {
        cwd: ROOT_DIR,
        nodir: true,
        absolute: true,
    });
    return files.filter(file => !gitignore.ignores(path.relative(ROOT_DIR, file)));
}

export async function findBookFiles(): Promise<string[]> {
    const pattern = 'brain/book/**/*.qmd';
    const files = await glob(pattern, {
        cwd: ROOT_DIR,
        ignore: IGNORE_PATTERNS.map(p => `**/${p}/**`),
        nodir: true,
        absolute: true,
    });
    return files;
}

/**
 * Replace em-dashes with comma-space in any value (recursive for objects/arrays)
 */
export function replaceEmDashesInValue(value: any): any {
    if (typeof value === 'string') {
        return value.replace(/—/g, ', ');
    } else if (Array.isArray(value)) {
        return value.map(replaceEmDashesInValue);
    } else if (value && typeof value === 'object') {
        const newObj: any = {};
        for (const key in value) {
            newObj[key] = replaceEmDashesInValue(value[key]);
        }
        return newObj;
    }
    return value;
}

/**
 * Clean and standardize frontmatter data
 * - Collapse multi-line descriptions to single line
 * - Remove date/dateCreated fields
 * - Convert Date objects to ISO strings
 * Note: Em-dash replacement is only done in content, not frontmatter
 */
export function cleanFrontmatterData(data: any): any {
    const cleaned = { ...data };

    // For descriptions that are multi-line, collapse them to a single line.
    if (cleaned.description && typeof cleaned.description === 'string') {
        cleaned.description = cleaned.description.replace(/\n/g, ' ').trim();
    }

    // Remove date and dateCreated fields
    delete cleaned.date;
    delete cleaned.dateCreated;

    // Convert any remaining Date objects to ISO strings to prevent YAML errors
    for (const key in cleaned) {
        if (cleaned[key] instanceof Date) {
            cleaned[key] = cleaned[key].toISOString();
        }
    }

    return cleaned;
}

/**
 * Stringify content with frontmatter using consistent settings that preserve emojis
 * This should be used by all scripts when saving .qmd/.md files
 */
export function stringifyWithFrontmatter(body: string, frontmatter: any): string {
    const cleanedFrontmatter = cleanFrontmatterData(frontmatter);
    // Use matter.stringify with lineWidth: -1 to prevent wrapping and preserve emojis
    return matter.stringify(body, cleanedFrontmatter, { lineWidth: -1 } as any);
}

/**
 * Format content with frontmatter (parse, clean, and re-stringify)
 * This is the internal function used by programmaticFormat
 */
function formatFrontmatter(content: string): string {
    const { data, content: body } = matter(content);
    return stringifyWithFrontmatter(body, data);
}

export function programmaticFormat(content: string): string {
  let result = content;

  // Format frontmatter first
  result = formatFrontmatter(result);

  // Parse frontmatter and body separately for more complex processing
  const { data: frontmatter, content: body } = matter(result);
  let processedBody = body;

  // Normalize line endings to LF for consistent processing
  processedBody = processedBody.replace(/\r\n/g, '\n');

  // 1. Replace em-dashes with comma and space
  processedBody = processedBody.replace(/—/g, ', ');

  // 2. Remove --- dividers that appear directly before headings
  processedBody = processedBody.replace(/^---\s*\n+(?=#{1,6}\s)/gm, '');

  // 3. Convert bold text sections to proper headings with smart level detection
  // Only convert if 6 words or less
  const lines = processedBody.split('\n');
  let modifiedLines = [...lines];

  // First pass: identify heading structure
  const headingLevels: { line: number; level: number }[] = [];
  for (let i = 0; i < lines.length; i++) {
    const match = lines[i].match(/^(#{1,6})\s/);
    if (match) {
      headingLevels.push({ line: i, level: match[1].length });
    }
  }

  // Second pass: convert bold headers with appropriate levels
  const boldHeaderPattern = /^\*\*([^*\n]+)\*\*\s*$/;
  const headerKeywords = ['On ', 'What ', 'How ', 'Why ', 'The ', 'About ', 'For ', 'In ', 'Your '];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const match = line.match(boldHeaderPattern);

    if (match) {
      const boldText = match[1].trim();
      const wordCount = boldText.split(/\s+/).length;

      // Only convert if 6 words or less
      if (wordCount <= 6) {
        const isLikelyHeader = headerKeywords.some(kw => boldText.startsWith(kw)) ||
                              /^[A-Z]/.test(boldText);

        if (isLikelyHeader) {
          // Find the most recent heading before this line
          let appropriateLevel = 3; // Default to ### if no context

          for (let j = headingLevels.length - 1; j >= 0; j--) {
            if (headingLevels[j].line < i) {
              // Use one level deeper than the previous heading, max level 6
              appropriateLevel = Math.min(headingLevels[j].level + 1, 6);
              break;
            }
          }

          // Special case: if this looks like a subsection header pattern (e.g., "What X does:")
          if (boldText.endsWith(':')) {
            appropriateLevel = Math.min(appropriateLevel, 4); // Cap at #### for subsection headers
          }

          // Remove trailing colon from heading text
          const headingText = boldText.endsWith(':') ? boldText.slice(0, -1) : boldText;

          const headingPrefix = '#'.repeat(appropriateLevel);
          modifiedLines[i] = `${headingPrefix} ${headingText}`;

          // Add this as a heading for subsequent context
          headingLevels.push({ line: i, level: appropriateLevel });
          headingLevels.sort((a, b) => a.line - b.line);
        }
      }
    }
  }

  processedBody = modifiedLines.join('\n');

  // Reconstruct with processed body using our consistent formatting
  result = stringifyWithFrontmatter(processedBody, frontmatter);

  // Fixes spacing for unordered lists: "-   item" -> "- item"
  result = result.replace(/^(-|\*)\s+/gm, '$1 ');

  // Add a blank line after a bolded line (for remaining bold text not converted to headers)
  result = result.replace(
    /^(\*\*[^*]+\*\*)\n(?!\n)(?![-*+]\s)(?!#{1,6}\s)(?!```)/gm,
    '$1\n\n'
  );

  // Add a blank line after "Speaker: "quote"" format
  result = result.replace(
    /^([A-Z][A-Za-z]*:\s+"[^"]+[.!"?]?")\n(?!\n)(?![-*+]\s)(?!#{1,6}\s)(?!```)/gm,
    '$1\n\n'
  );

  // Add a blank line after common key-value pairs
  result = result.replace(
    /^((?:Post|Bounty|Deadline|Amount|Price|Cost|Total|Budget):\s+[^\n]+)\n(?!\n)(?![-*+]\s)(?!#{1,6}\s)(?!```)/gm,
    '$1\n\n'
  );

  // Ensure blank lines after headings (unless followed by another heading or code block)
  result = result.replace(
    /^(#{1,6}\s+[^\n]+)\n(?!\n|#{1,6}\s|```)/gm,
    '$1\n\n'
  );

  return result;
}

// Shared file-saving function that applies programmatic formatting.
export async function saveFile(filePath: string, content: string): Promise<void> {
  let formattedContent = programmaticFormat(content);
  
  // For .qmd files, ensure the Python boilerplate is present
  if (path.extname(filePath) === '.qmd') {
    const { data: frontmatter, content: body } = matter(formattedContent);
    const pythonBoilerplate = "```{python}\n#| echo: false\nimport sys\nimport os\n\n# Quarto executes from project root (execute-dir: project in _book.yml)\nappendix_path = os.path.join(os.getcwd(), 'brain', 'book', 'appendix')\nif appendix_path not in sys.path:\n    sys.path.insert(0, appendix_path)\n\nfrom economic_parameters import *\n```";

    if (!body.includes('from economic_parameters import *')) {
      // Add boilerplate to body and use our consistent formatting
      const newBody = `${pythonBoilerplate}\n\n${body.trim()}`;
      formattedContent = stringifyWithFrontmatter(newBody, frontmatter);
    }
  }

  const dir = path.dirname(filePath);
  await fs.mkdir(dir, { recursive: true });
  await fs.writeFile(filePath, formattedContent, 'utf-8');
}

export async function getBookFiles(options: { includeAppendices?: boolean; exclude?: string[] } = {}): Promise<string[]> {
    const { includeAppendices = true, exclude = [] } = options;
    const quartoYmlContent = await fs.readFile('_book.yml', 'utf-8');
    const doc: any = yaml.load(quartoYmlContent);

    let files: string[] = [];

    const extractFiles = (section: any[]): string[] => {
        let fileList: string[] = [];
        if (!section) return fileList;
        for (const item of section) {
            if (typeof item === 'string') {
                fileList.push(item);
            } else if (item && item.href) {
                fileList.push(item.href);
            } else if (item && item.chapters) {
                fileList = fileList.concat(extractFiles(item.chapters));
            }
        }
        return fileList;
    };

    if (doc.book && doc.book.chapters) {
        files = files.concat(extractFiles(doc.book.chapters));
    }

    if (includeAppendices && doc.appendices) {
        files = files.concat(extractFiles(doc.appendices));
    }

    const defaultExclusions = ['brain/book/references.qmd'];
    const allExclusions = [...defaultExclusions, ...exclude];

    return files.filter(file => {
        if (!file) return false;
        const normalizedFile = file.replace(/\\/g, '/');
        return !allExclusions.some(excluded => normalizedFile.includes(excluded));
    });
}

// --- Content Hash Utilities ---

/**
 * Calculate hash of the body content (excluding frontmatter)
 */
export function getBodyHash(content: string): string {
  const { content: body } = matter(content);
  return crypto.createHash('sha256').update(body).digest('hex');
}

/**
 * Reads a file and parses its frontmatter and body
 */
export async function readFileWithMatter(filePath: string): Promise<{ frontmatter: any; body: string; originalContent: string }> {
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(originalContent);
  return { frontmatter, body, originalContent };
}

/**
 * Updates a file with new content and calculates/stores a hash
 */
export async function updateFileWithHash(
  filePath: string,
  body: string,
  frontmatter: any,
  hashFieldName: string
): Promise<void> {
  const tempContent = stringifyWithFrontmatter(body, frontmatter);
  frontmatter[hashFieldName] = getBodyHash(tempContent);
  const newContent = stringifyWithFrontmatter(body, frontmatter);
  await saveFile(filePath, newContent);
}

// --- Book Structure Utilities ---

export interface BookStructure {
  chapters: string[];
  appendices: string[];
}

/**
 * Parses _book.yml to extract chapter and appendix file paths
 */
export async function parseQuartoYml(): Promise<BookStructure> {
  const quartoYmlContent = await fs.readFile('_book.yml', 'utf-8');
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

// --- Find and Replace Utilities ---

export interface ReplaceResult {
  file: string;
  changes: number;
}

export interface BulkReplaceResult {
  totalFiles: number;
  filesChanged: number;
  totalChanges: number;
  details: ReplaceResult[];
}

/**
 * Perform bulk find-and-replace operations across all .qmd files
 * @param replacements - Map of search strings/regexes to replacement strings
 * @param options - Optional configuration
 */
export async function bulkReplaceInQmdFiles(
  replacements: Map<string | RegExp, string>,
  options: { basePath?: string; dryRun?: boolean } = {}
): Promise<BulkReplaceResult> {
  const { basePath = '', dryRun = false } = options;

  // Find all .qmd files respecting .gitignore
  const gitignoreContent = await fs.readFile('.gitignore', 'utf-8');
  const ig = ignore().add(gitignoreContent);

  const searchPattern = basePath ? `${basePath}/**/*.qmd` : '**/*.qmd';
  const allQmdFiles = glob.sync(searchPattern, { ignore: 'node_modules/**' });
  const qmdFiles = ig.filter(allQmdFiles);

  const result: BulkReplaceResult = {
    totalFiles: qmdFiles.length,
    filesChanged: 0,
    totalChanges: 0,
    details: []
  };

  for (const file of qmdFiles) {
    try {
      let content = await fs.readFile(file, 'utf-8');
      let fileChanges = 0;

      for (const [search, replace] of replacements.entries()) {
        const regex = typeof search === 'string'
          ? new RegExp(search.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')
          : search;

        const matches = content.match(regex);
        if (matches) {
          content = content.replace(regex, replace);
          fileChanges += matches.length;
        }
      }

      if (fileChanges > 0) {
        if (!dryRun) {
          await fs.writeFile(file, content, 'utf-8');
        }
        result.filesChanged++;
        result.totalChanges += fileChanges;
        result.details.push({ file, changes: fileChanges });
      }
    } catch (error) {
      console.error(`Error processing file ${file}:`, error);
    }
  }

  return result;
}
