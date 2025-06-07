import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import markdownit from 'markdown-it';
import anchor from 'markdown-it-anchor';

async function getHeadings(filePath: string): Promise<string[]> {
  const content = await fs.promises.readFile(filePath, 'utf-8');
  const { content: markdownContent } = matter(content);
  
  const headings: string[] = [];

  const md = markdownit().use(anchor, {
    level: [1, 2, 3, 4, 5, 6],
    slugify: (s) => s.trim().toLowerCase().replace(/[\s+]/g, '-').replace(/[.,()]/g, ''),
    callback: (token, { slug }) => {
      headings.push(decodeURIComponent(slug));
    }
  });

  md.render(markdownContent);
  
  return headings;
}

async function validateLink(link: string, sourceFile: string, allHeadings: Set<string>): Promise<string | null> {
  const workspaceRoot = path.resolve(__dirname, '..');
  try {
    if (link.startsWith('http://') || link.startsWith('https://')) {
      // External URL
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5-second timeout
      
      try {
        const response = await fetch(link, { signal: controller.signal, method: 'HEAD' });
        if (!response.ok) {
          // Try a GET if HEAD fails
          const getResponse = await fetch(link, { signal: controller.signal });
          if (!getResponse.ok) {
            return `Broken external link: ${link} (Status: ${getResponse.status})`;
          }
        }
      } finally {
        clearTimeout(timeoutId);
      }
    } else if (link.startsWith('#')) {
      // Section link in the same file
      const anchor = link.substring(1);
      if (!allHeadings.has(anchor)) {
        return `Broken section link: ${link}. Possible headings are: ${Array.from(allHeadings).join(', ')}`;
      }
    } else {
      // Internal file path
      const [filePath, anchor] = link.split('#');
      const absolutePath = path.resolve(path.dirname(path.join(workspaceRoot, sourceFile)), filePath);
      
      if (!fs.existsSync(absolutePath)) {
        return `Broken internal link: ${link} (File not found at ${absolutePath})`;
      }

      if (anchor) {
        const targetHeadings = await getHeadings(absolutePath);
        if (!targetHeadings.includes(anchor)) {
          return `Broken section link in different file: ${link} (Section #${anchor} not found in ${filePath}. Possible headings: ${targetHeadings.join(', ')})`;
        }
      }
    }
  } catch (error: any) {
    if (error.name === 'AbortError') {
      return `External link timed out: ${link}`;
    }
    return `Error validating link ${link}: ${error.message}`;
  }
  
  return null;
}

async function validateMarkdownFile(filePath: string) {
  console.log(`Validating links in ${filePath}...`);
  const workspaceRoot = path.resolve(__dirname, '..');
  const fullPath = path.join(workspaceRoot, filePath);

  if (!fs.existsSync(fullPath)) {
    console.error(`File not found: ${fullPath}`);
    return;
  }
  
  const fileContent = await fs.promises.readFile(fullPath, 'utf-8');
  const { content: markdownContent } = matter(fileContent);

  const linkRegex = /\[[^\]]+\]\(([^)]+)\)/g;
  let match;
  const links: string[] = [];
  
  while ((match = linkRegex.exec(markdownContent)) !== null) {
    links.push(match[1]);
  }
  
  const sourceHeadings = await getHeadings(fullPath);
  const sourceHeadingsSet = new Set(sourceHeadings);

  const validationPromises = links.map(link => validateLink(link, filePath, sourceHeadingsSet));
  const results = await Promise.all(validationPromises);
  
  const errors = results.filter(r => r !== null);
  
  if (errors.length > 0) {
    console.error(`Found ${errors.length} broken links in ${filePath}:`);
    errors.forEach(error => console.error(`- ${error}`));
  } else {
    console.log(`All links in ${filePath} are valid.`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const filePath = args[0];
  
  if (!filePath) {
    console.error('Please provide a file path to validate.');
    console.error('Usage: ts-node scripts/validate-links.ts <path/to/file.md>');
    process.exit(1);
  }
  
  await validateMarkdownFile(filePath);
}

main().catch(err => {
  console.error("An unexpected error occurred:", err);
  process.exit(1);
}); 