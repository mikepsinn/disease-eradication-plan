import fs from 'fs/promises';
import matter from 'gray-matter';
import yaml from 'js-yaml';
import { glob } from 'glob';
import * as path from 'path';
import ignore from 'ignore';
import crypto from 'crypto';

const ROOT_DIR = process.cwd();
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

function formatFrontmatter(content: string): string {
    const { data, content: body } = matter(content);

    // For descriptions that are multi-line, collapse them to a single line.
    if (data.description && typeof data.description === 'string') {
        data.description = data.description.replace(/\n/g, ' ').trim();
    }

    // Remove date and dateCreated fields
    delete data.date;
    delete data.dateCreated;

    // Convert any remaining Date objects to ISO strings to prevent YAML errors
    for (const key in data) {
        if (data[key] instanceof Date) {
            data[key] = data[key].toISOString();
        }
    }

    // Use JSON_SCHEMA to enforce double quotes on all strings and keys.
    const newFrontmatter = yaml.dump(data, {
        schema: yaml.JSON_SCHEMA,
        lineWidth: -1,
    });
    return `---\n${newFrontmatter.trim()}\n---\n${body}`;
}

export function programmaticFormat(content: string): string {
  let result = content;

  // Format frontmatter first
  result = formatFrontmatter(result);

  // Normalize line endings to LF for consistent processing
  result = result.replace(/\r\n/g, '\n');

  // Fixes spacing for unordered lists: "-   item" -> "- item"
  result = result.replace(/^(-|\*)\s+/gm, '$1 ');

  // Add a blank line after a bolded line, unless it's followed by another blank line, a list, a heading, or a code block
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
      // Reconstruct the file with the boilerplate immediately after the frontmatter
      const frontmatterString = matter.stringify('', frontmatter).trim();
      const newBody = `${pythonBoilerplate}\n\n${body.trim()}`;
      formattedContent = `${frontmatterString}\n${newBody}`;
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
  const tempContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  frontmatter[hashFieldName] = getBodyHash(tempContent);
  const newContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
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
