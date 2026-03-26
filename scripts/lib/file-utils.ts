import fs from 'fs/promises';
import * as fsSync from 'fs';
import matter from 'gray-matter';
import yaml from 'js-yaml';
import { glob } from 'glob';
import * as path from 'path';
import ignore from 'ignore';
import crypto from 'crypto';
import {
  HASH_FIELDS,
  CONTENT_DIRS,
  IGNORE_PATTERNS as CONST_IGNORE_PATTERNS,
  SPECIAL_FILES,
  AUTO_GENERATED_FILES,
  AUTO_GENERATED_PREFIXES,
  AUTO_GENERATED_PATTERNS,
  AUTO_GENERATED_DIRS,
  type HashFieldName
} from './constants';
import { setFileHash, getFileHash } from './hash-store';

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

// --- BibTeX Citation Resolution ---

/** Cache for parsed BibTeX references (citation key -> author display name) */
let bibTexCache: Map<string, string> | null = null;

/**
 * Parse references.bib and extract author names for each citation key
 * Uses synchronous file reading for use in sync functions
 * @returns Map of citation keys to author display names (e.g., "gilens2014" -> "Gilens and Page")
 */
function loadBibTexAuthors(): Map<string, string> {
  if (bibTexCache) {
    return bibTexCache;
  }

  bibTexCache = new Map();
  const bibPath = path.join(ROOT_DIR, 'references.bib');

  try {
    const content = fsSync.readFileSync(bibPath, 'utf-8');

    // Parse BibTeX entries: @type{key, ... author = {...}, ... }
    // Match each entry and extract key and author field
    const entryRegex = /@\w+\{([^,]+),([^@]*?)(?=\n@|\n*$)/gs;
    let match;

    while ((match = entryRegex.exec(content)) !== null) {
      const citationKey = match[1].trim();
      const entryContent = match[2];

      // Extract author field: author = {Name} or author = "Name"
      const authorMatch = entryContent.match(/author\s*=\s*[{"](.*?)[}"]/i);
      if (authorMatch) {
        const authorField = authorMatch[1];
        // Format author names for display
        const displayName = formatBibTexAuthors(authorField);
        bibTexCache.set(citationKey, displayName);
      }
    }
  } catch (error) {
    console.warn('[WARN] Could not load references.bib for citation resolution');
  }

  return bibTexCache;
}

/**
 * Format BibTeX author field for display
 * Handles: "Last, First" and "First Last" formats, multiple authors with "and"
 * @param authorField Raw author field from BibTeX
 * @returns Formatted author string (e.g., "Gilens and Page", "Smith et al.")
 */
function formatBibTexAuthors(authorField: string): string {
  // Split by " and " to get individual authors
  const authors = authorField.split(/\s+and\s+/i);

  // Extract last names
  const lastNames = authors.map(author => {
    author = author.trim();
    if (author.includes(',')) {
      // Format: "Last, First" -> take "Last"
      return author.split(',')[0].trim();
    } else {
      // Format: "First Last" or "First Middle Last" -> take last word
      const parts = author.split(/\s+/);
      return parts[parts.length - 1];
    }
  });

  // Format based on number of authors
  if (lastNames.length === 1) {
    return lastNames[0];
  } else if (lastNames.length === 2) {
    return `${lastNames[0]} and ${lastNames[1]}`;
  } else {
    return `${lastNames[0]} et al.`;
  }
}

/**
 * Resolve a citation key to author name(s)
 * Falls back to capitalizing the key if not found in references.bib
 * @param citationKey The citation key without @ (e.g., "gilens2014")
 * @returns Author display name (e.g., "Gilens and Page")
 */
export function resolveCitationToAuthor(citationKey: string): string {
  const authors = loadBibTexAuthors();
  const resolved = authors.get(citationKey);

  if (resolved) {
    return resolved;
  }

  // Fallback: extract author name from key (assumes format: authorname####)
  const keyMatch = citationKey.match(/^([a-zA-Z]+)\d{4}/);
  if (keyMatch) {
    const author = keyMatch[1];
    return author.charAt(0).toUpperCase() + author.slice(1).toLowerCase();
  }

  // Last resort: return the key as-is
  return citationKey;
}

export async function getGitignorePatterns(): Promise<string[]> {
  const gitignorePath = path.join(ROOT_DIR, '.gitignore');
  try {
    const gitignoreContent = await fs.readFile(gitignorePath, 'utf-8');
    return gitignoreContent
      .split('\n')
      .map(line => line.replace(/\r$/, '')) // Remove Windows CRLF line endings
      .filter(line => line.trim() && !line.startsWith('#'));
  } catch (error) {
    console.error("Could not read .gitignore file:", error);
    return [];
  }
}

/**
 * Check if a file path is auto-generated (should be excluded from searches/reviews)
 * @param filePath Absolute or relative file path
 * @returns true if the file is auto-generated
 */
export function isAutoGeneratedFile(filePath: string): boolean {
  const relativePath = path.isAbsolute(filePath)
    ? path.relative(ROOT_DIR, filePath)
    : filePath;
  const normalizedPath = relativePath.replace(/\\/g, '/');
  const fileName = path.basename(filePath);

  // Check exact file matches
  if (AUTO_GENERATED_FILES.includes(fileName as any)) {
    return true;
  }

  // Check if file is in an auto-generated directory
  for (const dir of AUTO_GENERATED_DIRS) {
    if (normalizedPath.includes(`/${dir}/`) || normalizedPath.startsWith(`${dir}/`)) {
      return true;
    }
  }

  // Check specific file paths (with directory context)
  const specificPaths = [
    'knowledge/appendix/parameters-and-calculations.qmd',
    'knowledge/references.json',
    'dih_models/reference_ids.py',
    'dih_models/parameters-calculations-citations.ts',
    'dih_models/economist-survey.ts',
  ];
  for (const specificPath of specificPaths) {
    if (normalizedPath.includes(specificPath) || normalizedPath.endsWith(specificPath)) {
      return true;
    }
  }

  // Check file name prefixes
  for (const prefix of AUTO_GENERATED_PREFIXES) {
    if (fileName.startsWith(prefix)) {
      return true;
    }
  }

  // Check file name patterns (regex)
  for (const pattern of AUTO_GENERATED_PATTERNS) {
    if (pattern.test(fileName)) {
      return true;
    }
  }

  return false;
}

export async function findFiles(pattern: string, options?: { excludeAutoGenerated?: boolean }): Promise<string[]> {
  const { excludeAutoGenerated = true } = options || {};
  const gitignore = ignore().add(await getGitignorePatterns());
  const files = await glob(pattern, {
    cwd: ROOT_DIR,
    nodir: true,
    absolute: true,
  });
  return files.filter(file => {
    // Respect .gitignore
    if (gitignore.ignores(path.relative(ROOT_DIR, file))) {
      return false;
    }
    // Exclude auto-generated files if requested
    if (excludeAutoGenerated && isAutoGeneratedFile(file)) {
      return false;
    }
    return true;
  });
}

/**
 * Get all source files in the project (non-ignored, non-auto-generated)
 * 
 * This is a convenience function for scripts that need to process all "real" files
 * in the project, excluding:
 * - Files ignored by .gitignore
 * - Auto-generated files (e.g., _variables.yml, distribution charts, etc.)
 * 
 * @param extensions Optional array of file extensions to include (default: common source file types)
 * @returns Array of absolute file paths
 * 
 * @example
 * // Get all QMD and MD files
 * const files = await getAllSourceFiles(['.qmd', '.md']);
 * 
 * // Get all common source files (default)
 * const allFiles = await getAllSourceFiles();
 */
export async function getAllSourceFiles(extensions?: string[]): Promise<string[]> {
  const defaultExtensions = ['.qmd', '.md', '.py', '.ts', '.js', '.yml', '.yaml', '.json'];
  const exts = extensions || defaultExtensions;

  // Build glob pattern for file extensions
  // Handle single extension differently from multiple (brace expansion needs >1 element)
  const globPattern = exts.length === 1
    ? `**/*${exts[0]}`  // Single: **/*.qmd
    : `**/*.{${exts.map(e => e.slice(1)).join(',')}}`; // Multiple: **/*.{qmd,md}

  // Use findFiles which already handles .gitignore and auto-generated files
  return findFiles(globPattern, { excludeAutoGenerated: true });
}

export async function findBookFiles(): Promise<string[]> {
  const pattern = 'knowledge/**/*.qmd';
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
 * Only replaces em-dashes surrounded by letters
 */
export function replaceEmDashesInValue(value: any): any {
  if (typeof value === 'string') {
    return value.replace(/([a-zA-Z])—([a-zA-Z])/g, '$1, $2');
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
 * - Remove all hash fields (they're stored in hash store now)
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

  // Remove all hash fields - they're stored in the centralized hash store now
  const hashFields = Object.values(HASH_FIELDS);
  for (const hashField of hashFields) {
    delete cleaned[hashField];
  }

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

  // Check if frontmatter is empty (no keys or all values are empty/null/undefined)
  const hasContent = cleanedFrontmatter && Object.keys(cleanedFrontmatter).length > 0;

  if (!hasContent) {
    // No frontmatter - return body as-is
    return body;
  }

  // Use js-yaml.dump directly with options that preserve emojis and Unicode characters
  // lineWidth: -1 prevents wrapping, which helps preserve emojis
  const yamlFrontmatter = yaml.dump(cleanedFrontmatter, {
    lineWidth: -1,
    noRefs: true,
    sortKeys: false,
  });
  return `---\n${yamlFrontmatter}---\n${body}`;
}

/**
 * Format content with frontmatter (parse, clean, and re-stringify)
 * This is the internal function used by programmaticFormat
 */
function formatFrontmatter(content: string): string {
  const { data, content: body } = matter(content);
  return stringifyWithFrontmatter(body, data);
}

export interface ProgrammaticFormatOptions {
  /** Add the setup-parameters include directive at the start (default: false) */
  addIncludeDirective?: boolean;
  /** Remove the first heading after the include directive (default: false) */
  removeFirstHeading?: boolean;
}

export function programmaticFormat(content: string, options: ProgrammaticFormatOptions = {}): string {
  const { addIncludeDirective = false, removeFirstHeading = false } = options;
  
  let result = content;

  // Format frontmatter first
  result = formatFrontmatter(result);

  // Parse frontmatter and body separately for more complex processing
  const { data: frontmatter, content: body } = matter(result);
  let processedBody = body;

  // Normalize line endings to LF for consistent processing
  processedBody = processedBody.replace(/\r\n/g, '\n');

  const includeDirective = '{{< include /knowledge/includes/setup-parameters.qmd >}}';

  // Optionally ensure the first line is the setup-parameters include
  if (addIncludeDirective) {
    const lines = processedBody.split('\n');

    // Check if first non-empty line is the include directive
    let firstNonEmptyIndex = lines.findIndex(line => line.trim() !== '');
    if (firstNonEmptyIndex === -1) {
      // Empty body, just add the include
      processedBody = includeDirective + '\n\n';
    } else if (lines[firstNonEmptyIndex]?.trim() !== includeDirective) {
      // Include directive is missing, add it at the beginning
      lines.splice(firstNonEmptyIndex, 0, includeDirective, '');
      processedBody = lines.join('\n');
    }
  }

  // Optionally remove first heading after the include directive (headings come from frontmatter)
  if (removeFirstHeading) {
    const contentLines = processedBody.split('\n');
    let foundInclude = false;
    let firstHeadingIndex = -1;

    for (let i = 0; i < contentLines.length; i++) {
      const line = contentLines[i].trim();

      // Track when we've passed the include directive
      if (line === includeDirective) {
        foundInclude = true;
        continue;
      }

      // After include, find first non-empty line
      if (foundInclude && line !== '') {
        // Check if it's a heading (starts with #)
        if (/^#{1,6}\s/.test(line)) {
          firstHeadingIndex = i;
          break;
        } else {
          // First non-empty line after include is not a heading, stop looking
          break;
        }
      }
    }

    // Remove the first heading if found
    if (firstHeadingIndex !== -1) {
      contentLines.splice(firstHeadingIndex, 1);
      processedBody = contentLines.join('\n');
    }
  }

  // 1. Replace em-dashes with comma and space (only when surrounded by letters)
  // Example: "word—word" becomes "word, word"
  // But: "word—" or "—word" or "word—\"" are left unchanged
  processedBody = processedBody.replace(/([a-zA-Z])—([a-zA-Z])/g, '$1, $2');

  // 2. Remove --- dividers that appear directly before headings
  processedBody = processedBody.replace(/^---\s*\n+(?=#{1,6}\s)/gm, '');

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

  // Ensure blank lines before bullet lists (unless preceded by another list item, heading, code block, or already has blank line)
  // Match: non-empty line that's not a list item, heading, or code block, followed by newline, then a list item (without blank line)
  result = result.replace(
    /^(?![-*+]\s)(?!#{1,6}\s)(?!```)([^\n]+)\n(?!\n)([-*+]\s)/gm,
    '$1\n\n$2'
  );

  // Collapse 3+ consecutive newlines into 2 (one blank line max)
  result = result.replace(/\n{3,}/g, '\n\n');

  return result;
}

// Shared file-saving function that applies programmatic formatting.
export async function saveFile(
  filePath: string, 
  content: string, 
  options: ProgrammaticFormatOptions = {}
): Promise<void> {
  let formattedContent = programmaticFormat(content, options);

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

  const defaultExclusions = ['knowledge/references.qmd'];
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
 * Hash fields are automatically removed from frontmatter (stored in hash store instead)
 */
export async function readFileWithMatter(filePath: string): Promise<{ frontmatter: any; body: string; originalContent: string }> {
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(originalContent);

  // Remove hash fields from frontmatter - they're stored in hash store now
  const hashFields = Object.values(HASH_FIELDS);
  const cleanedFrontmatter = { ...frontmatter };
  for (const hashField of hashFields) {
    delete cleanedFrontmatter[hashField];
  }

  return { frontmatter: cleanedFrontmatter, body, originalContent };
}

/**
 * Updates a file with new content and calculates/stores a hash
 * Hash is stored in the centralized hash store, not in frontmatter
 */
export async function updateFileWithHash(
  filePath: string,
  body: string,
  frontmatter: any,
  hashFieldName: string
): Promise<void> {
  const tempContent = stringifyWithFrontmatter(body, frontmatter);
  const hash = getBodyHash(tempContent);

  // Store hash in centralized hash store instead of frontmatter
  await setFileHash(filePath, hashFieldName as HashFieldName, hash);

  // Save file without hash in frontmatter
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

    // Match files directly listed (e.g., "- knowledge/file.qmd")
    const directMatch = line.match(/^\s*-\s+([^\s]+\.qmd)/);
    if (directMatch) {
      if (inAppendices) {
        appendices.push(directMatch[1]);
      } else if (inChapters) {
        chapters.push(directMatch[1]);
      }
    }

    // Also match files with href: structure (e.g., "href: index.qmd")
    const hrefMatch = line.match(/^\s*href:\s*([^\s]+\.qmd)/);
    if (hrefMatch) {
      if (inAppendices) {
        appendices.push(hrefMatch[1]);
      } else if (inChapters) {
        chapters.push(hrefMatch[1]);
      }
    }
  }

  return { chapters, appendices };
}

/**
 * Gets all QMD files from all Quarto configs in root directory.
 * Files from smaller configs come first, allowing efficient processing of
 * smaller papers/books before the large manual.
 *
 * This is the preferred way to get files for image generation and other
 * processing tasks that benefit from processing smaller outputs first.
 *
 * @returns Array of absolute file paths (deduplicated, smallest configs first)
 */
export async function getAllQmdFilesWithFrontmatter(): Promise<string[]> {
  const files = await getAllQuartoFilesSmallestFirst();

  // Convert to absolute paths
  return files.map(f => path.resolve(ROOT_DIR, f));
}

/**
 * Gets all book chapter and appendix files from _quarto-manual.yml, excluding variant files
 * This is the standard list of files to process for most review/edit operations
 * Only includes files explicitly listed in the book configuration
 * Excluded files:
 * - Files ending with -academic.qmd or -foundations.qmd (content variants)
 * - references.qmd (reference material)
 * - knowledge/appendix/parameters-and-calculations.qmd (auto-generated)
 */
export async function getBookFilesForProcessing(): Promise<string[]> {
  console.log('  → Reading _quarto-manual.yml...');
  const quartoYmlPath = path.join(getProjectRoot(), '_quarto-manual.yml');
  const quartoYmlContent = await fs.readFile(quartoYmlPath, 'utf-8');
  const doc: any = yaml.load(quartoYmlContent);

  const allFiles = extractFilesFromQuartoDoc(doc);

  console.log(`  → Found ${allFiles.length} files in _quarto-manual.yml`);

  // Filter out variant files, references, and auto-generated files
  console.log('  → Filtering out -academic/-foundations variants, references.qmd, and auto-generated files...');
  const filtered = filterQuartoFiles(allFiles);

  console.log(`  → Final count after filtering: ${filtered.length} files`);

  return filtered;
}

/**
 * Helper function to recursively extract file paths from Quarto chapters/sections
 */
function extractFilesFromQuartoDoc(doc: any): string[] {
  const extractFiles = (section: any[]): string[] => {
    let fileList: string[] = [];
    if (!section) return fileList;

    for (const item of section) {
      if (typeof item === 'string') {
        // Direct file reference: "knowledge/problem.qmd"
        fileList.push(item);
      } else if (item && item.href) {
        // Object with href: { href: "index.qmd" }
        fileList.push(item.href);
      } else if (item && item.chapters) {
        // Nested chapters: { part: "...", chapters: [...] }
        fileList = fileList.concat(extractFiles(item.chapters));
      } else if (item && item.contents) {
        // Sidebar contents
        fileList = fileList.concat(extractFiles(item.contents));
      }
    }
    return fileList;
  };

  let allFiles: string[] = [];

  // Extract files from book.chapters (for book type configs like _quarto-manual.yml)
  if (doc.book && doc.book.chapters) {
    allFiles = allFiles.concat(extractFiles(doc.book.chapters));
  }

  // Extract from dih-render.index-source (for website/paper type configs)
  // This is the custom field that points to the main paper QMD file
  if (doc['dih-render'] && doc['dih-render']['index-source']) {
    allFiles.push(doc['dih-render']['index-source']);
  }

  return allFiles;
}

/**
 * Filter out variant files, references, and auto-generated files from Quarto file lists
 */
function filterQuartoFiles(files: string[]): string[] {
  return files.filter(file => {
    if (!file) return false;
    const normalizedPath = file.replace(/\\/g, '/');

    // Exclude references.qmd
    if (normalizedPath.includes('references.qmd')) return false;

    // Exclude -academic and -foundations variants
    if (normalizedPath.endsWith('-academic.qmd') || normalizedPath.endsWith('-foundations.qmd')) return false;

    // Exclude auto-generated files
    if (isAutoGeneratedFile(file)) return false;

    return true;
  });
}

/**
 * Information about a Quarto config and its files
 */
export interface QuartoConfigInfo {
  /** Config file name (e.g., '_quarto-iab.yml') */
  configName: string;
  /** Full path to config file */
  configPath: string;
  /** QMD files in this config (relative paths) */
  files: string[];
  /** Number of files in this config */
  fileCount: number;
}

/**
 * Gets all QMD files from ALL Quarto config files in the root directory.
 * Returns configs sorted by file count (smallest first) for efficient processing.
 *
 * @returns Array of QuartoConfigInfo objects sorted by file count (ascending)
 */
export async function getFilesFromAllQuartoConfigs(): Promise<QuartoConfigInfo[]> {
  const rootDir = getProjectRoot();

  // Find all _quarto*.yml files in root (not in _build_temp or other subdirs)
  const configFiles = await glob('_quarto*.yml', {
    cwd: rootDir,
    absolute: true,
    nodir: true,
  });

  const configs: QuartoConfigInfo[] = [];

  for (const configPath of configFiles) {
    const configName = path.basename(configPath);

    // Skip shared-defaults (it's just common settings, no content files)
    if (configName === '_quarto-shared-defaults.yml') continue;

    // Skip test config
    if (configName === '_quarto-test.yml') continue;

    try {
      const content = await fs.readFile(configPath, 'utf-8');
      const doc: any = yaml.load(content);

      const rawFiles = extractFilesFromQuartoDoc(doc);
      const filteredFiles = filterQuartoFiles(rawFiles);

      if (filteredFiles.length > 0) {
        configs.push({
          configName,
          configPath,
          files: filteredFiles,
          fileCount: filteredFiles.length,
        });
      }
    } catch (error) {
      console.warn(`  [WARN] Could not parse ${configName}: ${error}`);
    }
  }

  // Sort by file count (smallest first)
  configs.sort((a, b) => a.fileCount - b.fileCount);

  return configs;
}

/**
 * Gets all unique QMD files from all Quarto configs, sorted so files from
 * smaller configs come first. This allows processing smaller papers/books
 * before the large manual.
 *
 * @returns Array of unique file paths (relative), ordered by config size
 */
export async function getAllQuartoFilesSmallestFirst(): Promise<string[]> {
  const configs = await getFilesFromAllQuartoConfigs();

  console.log(`\n[getAllQuartoFilesSmallestFirst] Found ${configs.length} Quarto configs:`);
  for (const config of configs) {
    console.log(`  ${config.configName}: ${config.fileCount} files`);
    for (const file of config.files) {
      console.log(`    - ${file}`);
    }
  }

  // Collect files in order, deduplicating
  const seen = new Set<string>();
  const orderedFiles: string[] = [];

  for (const config of configs) {
    let newFromConfig = 0;
    for (const file of config.files) {
      const normalized = file.replace(/\\/g, '/');
      if (!seen.has(normalized)) {
        seen.add(normalized);
        orderedFiles.push(normalized);
        newFromConfig++;
      }
    }
    if (newFromConfig < config.fileCount) {
      console.log(`  [${config.configName}] Added ${newFromConfig} new files (${config.fileCount - newFromConfig} duplicates skipped)`);
    }
  }

  console.log(`[getAllQuartoFilesSmallestFirst] Total unique files: ${orderedFiles.length}\n`);

  return orderedFiles;
}

/**
 * Find all .qmd files where the content hash doesn't match the stored hash
 * @deprecated Use getStaleFilesWithConstants instead
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
      const currentBodyHash = getBodyHash(content);

      // Read hash from centralized hash store instead of frontmatter
      const lastHash = await getFileHash(file, hashFieldName as HashFieldName);

      if (currentBodyHash !== lastHash) {
        staleFiles.push(file);
      }
    } catch (error) {
      console.error(`Error processing file ${file}:`, error);
    }
  }

  return staleFiles;
}

/**
 * Find all .qmd files where the content hash doesn't match the stored hash
 * Uses centralized constants for consistency
 * Reads hashes from centralized hash store instead of frontmatter
 */
export async function getStaleFilesWithConstants(
  hashFieldName: HashFieldName,
  basePath: string = CONTENT_DIRS.BOOK,
  options?: {
    includeAppendix?: boolean;
    includeReferences?: boolean;
    includePartIntros?: boolean;
  }
): Promise<string[]> {
  const searchPattern = `${basePath}/**/*.qmd`;
  const allFiles = await glob(searchPattern, {
    ignore: [...CONST_IGNORE_PATTERNS]
  });

  // Filter out special files based on options
  const filteredFiles = allFiles.filter(file => {
    const relPath = path.relative(basePath, file).replace(/\\/g, '/');

    // Skip references unless explicitly included
    if (!options?.includeReferences && relPath.includes(SPECIAL_FILES.REFERENCES)) {
      return false;
    }

    // Skip appendix unless explicitly included
    if (!options?.includeAppendix && relPath.startsWith('appendix/')) {
      return false;
    }

    // Skip part intros unless explicitly included
    if (!options?.includePartIntros) {
      const fullPath = path.resolve(file);
      if (SPECIAL_FILES.PART_INTROS.some(intro => fullPath.includes(intro))) {
        return false;
      }
    }

    return true;
  });

  const staleFiles: string[] = [];

  for (const file of filteredFiles) {
    try {
      const { body } = await readFileWithMatter(file);
      const currentBodyHash = getBodyHash(body);

      // Read hash from centralized hash store instead of frontmatter
      const lastHash = await getFileHash(file, hashFieldName);

      if (currentBodyHash !== lastHash) {
        staleFiles.push(file);
      }
    } catch (error) {
      console.error(`Error processing file ${file}:`, error);
    }
  }

  return staleFiles;
}

/**
 * Get all book content files (excluding appendix and references by default)
 */
export async function getBookContentFiles(options?: {
  includeAppendix?: boolean;
  includeReferences?: boolean;
  includePartIntros?: boolean;
}): Promise<string[]> {
  const searchPattern = `${CONTENT_DIRS.BOOK}/**/*.qmd`;
  const allFiles = await glob(searchPattern, {
    ignore: [...CONST_IGNORE_PATTERNS]
  });

  return allFiles.filter(file => {
    const relPath = path.relative(CONTENT_DIRS.BOOK, file).replace(/\\/g, '/');

    // Skip references unless explicitly included
    if (!options?.includeReferences && relPath.includes(SPECIAL_FILES.REFERENCES)) {
      return false;
    }

    // Skip appendix unless explicitly included
    if (!options?.includeAppendix && relPath.startsWith('appendix/')) {
      return false;
    }

    // Skip part intros unless explicitly included
    if (!options?.includePartIntros) {
      const fullPath = path.resolve(file);
      if (SPECIAL_FILES.PART_INTROS.some(intro => fullPath.includes(intro))) {
        return false;
      }
    }

    return true;
  });
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

/**
 * Perform bulk find-and-replace operations across multiple file types
 * @param replacements - Map of search strings/regexes to replacement strings
 * @param options - Configuration options
 * @returns Result summary with files changed and total changes
 */
export async function bulkReplaceInFiles(
  replacements: Map<string | RegExp, string>,
  options: {
    extensions?: string[];
    basePath?: string;
    dryRun?: boolean;
    excludeAutoGenerated?: boolean;
  } = {}
): Promise<BulkReplaceResult> {
  const {
    extensions = ['.qmd', '.md', '.py', '.yml', '.yaml', '.ts', '.js'],
    basePath = '',
    dryRun = false,
    excludeAutoGenerated = true
  } = options;

  // Find all files with specified extensions respecting .gitignore
  const gitignoreContent = await fs.readFile('.gitignore', 'utf-8');
  const ig = ignore().add(gitignoreContent);

  // Build glob patterns for all extensions
  const allFiles: string[] = [];
  for (const ext of extensions) {
    const searchPattern = basePath
      ? `${basePath}/**/*${ext}`
      : `**/*${ext}`;
    const files = glob.sync(searchPattern, { ignore: 'node_modules/**' });
    allFiles.push(...files);
  }

  // Filter by gitignore and auto-generated files
  const filteredFiles = ig.filter(allFiles).filter(file => {
    if (excludeAutoGenerated && isAutoGeneratedFile(file)) {
      return false;
    }
    return true;
  });

  const result: BulkReplaceResult = {
    totalFiles: filteredFiles.length,
    filesChanged: 0,
    totalChanges: 0,
    details: []
  };

  for (const file of filteredFiles) {
    try {
      let content = await fs.readFile(file, 'utf-8');
      let fileChanges = 0;
      const originalContent = content;

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

      if (fileChanges > 0 && content !== originalContent) {
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

// --- Quarto Variable Replacement Utilities ---

/**
 * Load and parse _variables.yml file
 * @returns Map of variable names to plain text values (HTML stripped)
 */
export async function loadQuartoVariables(): Promise<Map<string, string>> {
  const variablesPath = path.join(getProjectRoot(), '_variables.yml');
  const variablesContent = await fs.readFile(variablesPath, 'utf-8');
  const variables = yaml.load(variablesContent) as Record<string, string>;

  const variableMap = new Map<string, string>();

  // Extract plain text values from HTML-formatted variables
  for (const [key, value] of Object.entries(variables)) {
    // Skip citation and LaTeX variables (they end with _cite or _latex)
    if (key.endsWith('_cite') || key.endsWith('_latex')) {
      continue;
    }

    // Extract text between > and </a> tags (for HTML-formatted values)
    const match = value.match(/>([^<]+)<\/a>/);
    if (match) {
      variableMap.set(key, match[1]);
    } else {
      // If no HTML tags, use the value as-is
      variableMap.set(key, value);
    }
  }

  return variableMap;
}

/**
 * Replace Quarto variables in content with actual values
 * Replaces patterns like {{< var variable_name >}} with values from _variables.yml
 * @param content Content with Quarto variable syntax
 * @param variables Map of variable names to values (use loadQuartoVariables() to get this)
 * @param warnOnMissing If true, logs a warning when a variable is not found (default: false)
 * @returns Content with variables replaced
 */
export function replaceQuartoVariables(
  content: string,
  variables: Map<string, string>,
  warnOnMissing: boolean = false
): string {
  // Replace all {{< var variable_name >}} patterns
  return content.replace(/\{\{<\s*var\s+([a-z0-9_]+)\s*>\}\}/gi, (match, varName) => {
    const value = variables.get(varName);
    if (value) {
      return value;
    }
    // If variable not found, leave it as-is
    if (warnOnMissing) {
      console.warn(`  [WARN] Variable not found: ${varName}`);
    }
    return match;
  });
}

/**
 * Resolve Quarto variables and strip confidence intervals / HTML tags
 * Useful for preparing frontmatter values (title, description) for display or prompts
 */
export async function resolveAndCleanText(text: string): Promise<string> {
  const variables = await loadQuartoVariables();
  return replaceQuartoVariables(text, variables)
    .replace(/\s*\(95% CI:[^)]*\)/g, '')
    .replace(/<[^>]+>/g, '')
    .trim();
}

/**
 * Clean content for AI image generation prompts
 * More aggressive than cleanContentForLLM - strips all markup that doesn't convey visual meaning
 * @param content Raw QMD/Markdown content
 * @returns Clean plain text suitable for image generation prompts
 */
export function cleanContentForImagePrompt(content: string): string {
  return content
    // Strip Quarto section ID wrappers: {#section-id}, {.class}, {#id .class key="value"}
    .replace(/\s*\{[#.][^}]*\}/g, '')
    // Strip heading markers (keep text)
    .replace(/^#{1,6}\s+/gm, '')
    // Strip markdown links, keep text: [text](url) -> text
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    // Strip reference-style links: [text][ref] -> text
    .replace(/\[([^\]]+)\]\[[^\]]*\]/g, '$1')
    // Strip footnote references: [^1], [^note]
    .replace(/\[\^[^\]]+\]/g, '')
    // Strip footnote definitions: [^1]: definition...
    .replace(/^\[\^[^\]]+\]:.*$/gm, '')
    // Strip bracketed citations and preceding space: " [@smith2020]" -> ""
    .replace(/\s*\[@[^\]]+\]/g, '')
    // Convert bare/in-text citations to author names using references.bib
    // e.g., "@gilens2014 analyzed" -> "Gilens and Page analyzed"
    .replace(/@([\w-]+)(?=[\s.,;:!?)\]]|$)/g, (_, citationKey) => {
      return resolveCitationToAuthor(citationKey);
    })
    // Strip Quarto cross-references: @fig-name, @tbl-name, @sec-name, @eq-name
    .replace(/@(fig|tbl|sec|eq|lst|thm)-[\w-]+/g, '')
    // Strip <style>...</style> blocks entirely (CSS is not meaningful text)
    .replace(/<style[\s>][\s\S]*?<\/style>/gi, '')
    // Strip <script>...</script> blocks entirely (JS is not meaningful text)
    .replace(/<script[\s>][\s\S]*?<\/script>/gi, '')
    // Strip HTML comments
    .replace(/<!--[\s\S]*?-->/g, '')
    // Strip HTML tags, keep content
    .replace(/<[^>]+>/g, '')
    // Strip code blocks entirely (not useful for image gen)
    .replace(/```[\s\S]*?```/g, '')
    // Strip inline code backticks, keep text
    .replace(/`([^`]+)`/g, '$1')
    // Strip image references (we're generating images, not referencing them)
    .replace(/!\[[^\]]*\]\([^)]+\)/g, '')
    // Strip callout markers but keep content
    .replace(/^:::\s*\{[^}]*\}\s*$/gm, '')
    .replace(/^:::\s*$/gm, '')
    // Strip horizontal rules
    .replace(/^[-*_]{3,}\s*$/gm, '')
    // Strip Quarto shortcodes (includes, embeds, etc.) but NOT variables
    .replace(/\{\{<\s*(?!var\s)[^>]+>\}\}/gi, '')
    // Strip unresolved Quarto variables (already resolved ones are plain text)
    .replace(/\{\{<\s*var\s+[^>]+>\}\}/gi, '')
    // Strip bold/italic markers, keep text: **text** -> text, *text* -> text
    .replace(/\*{1,3}([^*]+)\*{1,3}/g, '$1')
    // Strip blockquote markers but keep text
    .replace(/^>\s*/gm, '')
    // Collapse multiple blank lines
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

/**
 * Clean Quarto/Markdown content for LLM processing
 * Removes document markup, navigation, and structural elements to leave only core content
 * @param content Raw QMD content
 * @returns Cleaned content suitable for LLM
 */
export function cleanContentForLLM(content: string): string {
  let cleaned = content;

  // 1a. Remove Quarto raw format code blocks (e.g., ```{=html} ... ```)
  cleaned = cleaned.replace(/```\{=[a-z]+\}[\s\S]*?```/g, '');

  // 1b. Remove Quarto includes (e.g., {{< include /path/to/file.qmd >}})
  cleaned = cleaned.replace(/\{\{<\s*include\s+[^>]+>\}\}/gi, '');

  // 2. Remove Quarto shortcodes except variables (video, embed, etc.)
  // Preserves {{< var name >}} but removes {{< video ... >}}, {{< embed ... >}}, etc.
  cleaned = cleaned.replace(/\{\{<\s*(?!var\s)[^>]+>\}\}/gi, '');

  // 3. Remove callout block fences but keep content
  // Removes ::: {.callout-note} and ::: but keeps the text between them
  cleaned = cleaned.replace(/^:::\s*\{[^}]*\}\s*$/gm, '');
  cleaned = cleaned.replace(/^:::\s*$/gm, '');

  // 4. Remove image references completely (they're output, not input for LLM)
  // Matches: ![alt text](url) or ![alt text]
  cleaned = cleaned.replace(/!\[([^\]]*)\](?:\([^)]*\))?/g, '');

  // 5. Strip <style> and <script> blocks entirely (content is CSS/JS, not meaningful text)
  cleaned = cleaned.replace(/<style[\s>][\s\S]*?<\/style>/gi, '');
  cleaned = cleaned.replace(/<script[\s>][\s\S]*?<\/script>/gi, '');

  // 6. Strip remaining HTML tags and comments (keep the text inside tags)
  cleaned = cleaned.replace(/<!--[\s\S]*?-->/g, ''); // Remove comments first
  cleaned = cleaned.replace(/<[^>]+>/g, '');

  // 7. Simplify markdown links: [text](url) -> text
  // Keep the linked text as it's often meaningful content
  cleaned = cleaned.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');

  // 8. Remove citation syntax: [@citation] -> citation
  cleaned = cleaned.replace(/\[@([^\]]+)\]/g, '$1');

  // 9. Remove sentences mentioning "chapter" or "chapters" (navigation references)
  cleaned = cleaned.replace(/[^.!?]*\bchapters?\b[^.!?]*[.!?]\s*/gi, '');

  // 10. Remove list items with "Chapter X:" references (after links are simplified)
  cleaned = cleaned.replace(/^[-*]\s+Chapter \d+:[^\n]*/gm, '');

  // 11. Remove "See also:", "Read more:", etc. patterns (navigation helpers)
  cleaned = cleaned.replace(/^[-*]?\s*(See also|Read more|For more details|Learn more|Further reading):[^\n]*/gmi, '');

  // 12. Remove table of contents patterns (links to anchors on same page)
  cleaned = cleaned.replace(/^[-*]\s*\[.*?\]\(#.*?\).*$/gm, '');

  // 13. Strip confidence intervals: (95% CI: X-Y)
  cleaned = cleaned.replace(/\s*\(95% CI:[^)]*\)/g, '');

  // 14. Remove excessive blank lines (more than 2 consecutive newlines)
  cleaned = cleaned.replace(/\n{3,}/g, '\n\n');

  // 15. Trim whitespace
  cleaned = cleaned.trim();

  return cleaned;
}

// Cache for variables to avoid reloading on every call
let cachedVariables: Map<string, string> | null = null;

/**
 * Prepare QMD content for LLM processing (all-in-one convenience function)
 *
 * This combines variable replacement and content cleaning in a single call.
 * Use this when sending Quarto content to LLMs for processing.
 *
 * Processing steps:
 * 1. Loads variables from _variables.yml (cached after first load)
 * 2. Replaces Quarto variables ({{< var name >}}) with actual values
 * 3. Removes Quarto includes
 * 4. Strips HTML tags
 * 5. Simplifies markdown links to plain text
 * 6. Cleans citation syntax
 * 7. Removes sentences mentioning "chapter" or "chapters"
 * 8. Removes excessive blank lines
 *
 * @param content Raw QMD content with Quarto syntax
 * @returns Clean plain text ready for LLM processing
 *
 * @example
 * const cleanContent = await prepareContentForLLM(rawContent);
 * // Send cleanContent to GPT-4, Claude, Gemini, etc.
 */
export async function prepareContentForLLM(content: string): Promise<string> {
  // Load variables if not already cached
  if (!cachedVariables) {
    cachedVariables = await loadQuartoVariables();
  }

  // First replace variables with actual values
  const withReplacedVars = replaceQuartoVariables(content, cachedVariables);

  // Then clean the content for LLM
  return cleanContentForLLM(withReplacedVars);
}

/**
 * Read and prepare QMD file content for LLM processing
 *
 * This is the complete end-to-end function for getting LLM-ready content from a file.
 * Reads the file, extracts body content, replaces variables, and cleans markup.
 *
 * Processing steps:
 * 1. Reads file from disk
 * 2. Parses frontmatter and extracts body
 * 3. Prepends title (as H1) and description (in bold) from frontmatter
 * 4. Loads and replaces Quarto variables (cached)
 * 5. Removes Quarto includes, HTML tags, markdown links
 * 6. Cleans citation syntax
 * 7. Removes sentences mentioning "chapter" or "chapters"
 * 8. Removes excessive whitespace
 *
 * @param filePath Absolute path to the QMD file
 * @returns Clean plain text ready for LLM processing
 *
 * @example
 * const cleanContent = await getCleanedContentForLLM('knowledge/proof/historical-precedents.qmd');
 * const response = await sendToLLM(cleanContent);
 */
export async function getCleanedContentForLLM(filePath: string): Promise<string> {
  // Read file and parse frontmatter
  const { frontmatter, body } = await readFileWithMatter(filePath);

  // Build header section from frontmatter
  let headerSection = '';

  if (frontmatter.title) {
    headerSection += `# ${frontmatter.title}\n\n`;
  }

  if (frontmatter.description) {
    headerSection += `**${frontmatter.description}**\n\n`;
  }

  // Combine header with body
  const contentWithHeader = headerSection + body;

  // Prepare content for LLM (replaces variables and cleans markup)
  return prepareContentForLLM(contentWithHeader);
}

/**
 * Extract image paths from QMD content
 * Finds all markdown image references: ![alt](path)
 * @param content QMD file content
 * @returns Array of image paths (relative to project root)
 */
export function extractImagePaths(content: string): string[] {
  const imagePaths: string[] = [];

  // Match markdown image syntax: ![alt text](path)
  const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
  let match;

  while ((match = imageRegex.exec(content)) !== null) {
    const imagePath = match[2];
    // Skip external URLs
    if (!imagePath.startsWith('http://') && !imagePath.startsWith('https://')) {
      imagePaths.push(imagePath);
    }
  }

  return imagePaths;
}

/**
 * Load image as base64
 * @param imagePath Path to image (can be absolute, relative to project root, or start with /)
 * @param sourceFilePath Optional path to the source QMD file (for resolving relative paths)
 * @returns Object with base64 data and MIME type
 */
export async function loadImageAsBase64(
  imagePath: string,
  sourceFilePath?: string
): Promise<{ data: string; mimeType: string } | null> {
  try {
    let absolutePath: string;

    if (path.isAbsolute(imagePath)) {
      // Already absolute path
      absolutePath = imagePath;
    } else if (imagePath.startsWith('/')) {
      // Path starting with / is relative to project root (common in web contexts)
      absolutePath = path.join(getProjectRoot(), imagePath.substring(1));
    } else if (sourceFilePath) {
      // Relative path - resolve relative to source file
      const sourceDir = path.dirname(sourceFilePath);
      absolutePath = path.join(sourceDir, imagePath);
    } else {
      // Fallback: relative to project root
      absolutePath = path.join(getProjectRoot(), imagePath);
    }

    // Normalize path (resolve .. and .)
    absolutePath = path.resolve(absolutePath);

    // Check if file exists
    if (!fsSync.existsSync(absolutePath)) {
      console.warn(`  [WARN] Image not found: ${imagePath}`);
      return null;
    }

    // Read file as buffer
    const imageBuffer = await fs.readFile(absolutePath);

    // Convert to base64
    const base64Data = imageBuffer.toString('base64');

    // Determine MIME type from extension
    const ext = path.extname(absolutePath).toLowerCase();
    const mimeTypes: Record<string, string> = {
      '.png': 'image/png',
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.gif': 'image/gif',
      '.webp': 'image/webp',
      '.svg': 'image/svg+xml',
    };

    const mimeType = mimeTypes[ext] || 'image/png';

    return { data: base64Data, mimeType };
  } catch (error) {
    console.warn(`  [WARN] Failed to load image: ${imagePath}`, error);
    return null;
  }
}

/**
 * Get a property value from a Quarto YAML config file
 * Supports nested property paths like 'website.site-url' or 'book.title'
 * @param configFile Config file name (e.g., '_quarto-manual.yml', '_quarto.yml')
 * @param propertyPath Dot-separated path to property (e.g., 'website.site-url', 'book.title')
 * @param defaultValue Optional default value if property not found
 * @returns Property value or default value
 */
export async function getQuartoConfigProperty(
  configFile: string,
  propertyPath: string,
  defaultValue?: string
): Promise<string | undefined> {
  const configPath = path.join(getProjectRoot(), configFile);
  try {
    const configContent = await fs.readFile(configPath, 'utf-8');
    const doc = yaml.load(configContent) as Record<string, any>;

    // Navigate the property path
    const parts = propertyPath.split('.');
    let value: any = doc;

    for (const part of parts) {
      if (value && typeof value === 'object' && part in value) {
        value = value[part];
      } else {
        return defaultValue;
      }
    }

    // Return string value or default
    return typeof value === 'string' ? value : defaultValue;
  } catch {
    return defaultValue;
  }
}

/**
 * Get site URL from Quarto config file
 * Checks website.site-url and book.site-url properties
 * @param configFile Config file name (default: '_quarto-manual.yml')
 * @param defaultUrl Default URL if not found
 * @returns Site URL
 */
export async function getSiteUrl(
  configFile: string = '_quarto-manual.yml',
  defaultUrl: string = 'https://manual.wardondisease.org'
): Promise<string> {
  // Try website.site-url first, then book.site-url
  const websiteUrl = await getQuartoConfigProperty(configFile, 'website.site-url');
  if (websiteUrl) return websiteUrl.toLowerCase();

  const bookUrl = await getQuartoConfigProperty(configFile, 'book.site-url');
  if (bookUrl) return bookUrl.toLowerCase();

  return defaultUrl;
}

/**
 * Extract and load reference images from QMD file
 * @param filePath Path to QMD file
 * @param maxImages Maximum number of images to load (default: 14, Gemini's limit)
 * @returns Array of reference images with base64 data and MIME types
 */
export async function extractReferenceImages(
  filePath: string,
  maxImages: number = 14
): Promise<Array<{ data: string; mimeType: string }>> {
  const { body } = await readFileWithMatter(filePath);
  const imagePaths = extractImagePaths(body);

  console.log(`  [INFO] Found ${imagePaths.length} image references in ${path.basename(filePath)}`);

  // Limit to maxImages
  const pathsToLoad = imagePaths.slice(0, maxImages);
  if (imagePaths.length > maxImages) {
    console.log(`  [INFO] Limiting to first ${maxImages} images (Gemini's max)`);
  }

  const referenceImages: Array<{ data: string; mimeType: string }> = [];

  for (const imagePath of pathsToLoad) {
    const imageData = await loadImageAsBase64(imagePath, filePath);
    if (imageData) {
      referenceImages.push(imageData);
    }
  }

  console.log(`  [INFO] Successfully loaded ${referenceImages.length} reference images`);

  return referenceImages;
}
