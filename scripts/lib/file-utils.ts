import fs from 'fs/promises';
import matter from 'gray-matter';
import yaml from 'js-yaml';
import { glob } from 'glob';
import * as path from 'path';

const ROOT_DIR = process.cwd();
const IGNORE_PATTERNS = ['.git', '.cursor', 'node_modules', 'scripts', 'brand', '.venv', '_book'];

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
    try {
        const { data, content: body } = matter(content);
        let needsRewrite = false;

        // Enforce double quotes on all string values
        for (const key in data) {
            if (typeof data[key] === 'string') {
                const value = data[key];
                if (!value.startsWith('"') || !value.endsWith('"')) {
                    data[key] = `${value.replace(/"/g, '\\"')}`;
                    needsRewrite = true;
                }
            }
        }

        if (needsRewrite) {
            const newFrontmatter = yaml.dump(data, {
                styles: {
                    '!!str': 'double'
                },
                quotingType: '"'
            });
            return `---\n${newFrontmatter}---\n${body}`;
        }
    } catch (e) {
        // Ignore errors if frontmatter is invalid
    }
    return content;
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
  const formattedContent = programmaticFormat(content);
  await fs.writeFile(filePath, formattedContent, 'utf-8');
}
