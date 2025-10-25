import fs from 'fs/promises';
import matter from 'gray-matter';
import yaml from 'js-yaml';
import { glob } from 'glob';
import * as path from 'path';
import ignore from 'ignore';

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
    const pythonBoilerplate = "```{python}\n#| echo: false\nimport sys\nimport os\n\n# Quarto executes from project root (execute-dir: project in _quarto.yml)\nappendix_path = os.path.join(os.getcwd(), 'brain', 'book', 'appendix')\nif appendix_path not in sys.path:\n    sys.path.insert(0, appendix_path)\n\nfrom economic_parameters import *\n```";

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
    const quartoYmlContent = await fs.readFile('_quarto.yml', 'utf-8');
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
