import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import markdownit from 'markdown-it';
import anchor from 'markdown-it-anchor';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function fixAmpersands(filePath: string): Promise<void> {
  console.log(`Fixing ampersands in ${filePath}...`);
  const workspaceRoot = path.resolve(__dirname, '..');
  const fullPath = path.join(workspaceRoot, filePath);

  if (!fs.existsSync(fullPath)) {
    console.error(`File not found for fixing: ${fullPath}`);
    return;
  }

  let content = await fs.promises.readFile(fullPath, 'utf-8');
  const originalContent = content;

  // 1. Fix headings
  content = content.split('\n').map(line => {
    if (line.trim().startsWith('#')) {
      return line.replace(/ & /g, ' and ').replace(/R&D/g, 'R and D');
    }
    return line;
  }).join('\n');

  // 2. Fix link text and corresponding anchor slugs
  content = content.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, text, url) => {
    let newText = text;
    let newUrl = url;
    let textChanged = false;
    let urlChanged = false;

    // Fix link text for consistency
    if (newText.includes(' & ') || newText.includes('R&D')) {
        newText = newText.replace(/ & /g, ' and ').replace(/R&D/g, 'R and D');
        textChanged = true;
    }

    // Fix link anchor slug if it's an internal link
    if (newUrl.startsWith('#')) {
        if (newUrl.includes('-&-')) {
            newUrl = newUrl.replace(/-&-/g, '-and-');
            urlChanged = true;
        }
        if (newUrl.includes('r&d')) {
            newUrl = newUrl.replace(/r&d/g, 'r-and-d');
            urlChanged = true;
        }
    }
    
    if (textChanged || urlChanged) {
        return `[${newText}](${newUrl})`;
    }
    
    return match;
  });

  if (content !== originalContent) {
    console.log('Found and fixed ampersands. Overwriting file.');
    await fs.promises.writeFile(fullPath, content, 'utf-8');
  }
}

async function getHeadings(filePath: string): Promise<string[]> {
  const content = await fs.promises.readFile(filePath, 'utf-8');
  const { content: markdownContent } = matter(content);
  
  const headings: string[] = [];

  const md = markdownit().use(anchor, {
    level: [1, 2, 3, 4, 5, 6],
    slugify: (s) => s.trim().toLowerCase().replace(/[\s+]/g, '-').replace(/[.,()]/g, ''),
    callback: (token, { slug }) => {
      try {
        headings.push(decodeURIComponent(slug));
      } catch (e) {
        // If decoding fails, use the slug as-is
        headings.push(slug);
      }
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
      const timeoutId = setTimeout(() => controller.abort(), 15000); // 15-second timeout
      
      const headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      };

      try {
        const response = await fetch(link, { signal: controller.signal, headers, method: 'HEAD' });
        if (!response.ok) {
          // Try a GET if HEAD fails
          const getResponse = await fetch(link, { signal: controller.signal, headers });
          if (!getResponse.ok) {
            if (getResponse.status === 403) {
              // Known issue with sites that block scripts. Treat as a warning, not a hard error.
              console.warn(`- Link returned status 403 (Forbidden): ${link}. This may be due to bot protection. Please verify manually.`);
              return null; // Return null to not count it as a broken link
            }
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

  const md = markdownit();
  const tokens = md.parse(markdownContent, {});
  const links: string[] = [];

  for (const token of tokens) {
    if (token.type === 'link_open') {
      const href = token.attrGet('href');
      if (href) {
        links.push(href);
      }
    } else if (token.type === 'image') {
      const src = token.attrGet('src');
      if (src) {
        links.push(src);
      }
    }
  }
  
  const sourceHeadings = await getHeadings(fullPath);
  const sourceHeadingsSet = new Set(sourceHeadings);

  const validationPromises = links.map(link => validateLink(link, filePath, sourceHeadingsSet));
  const results = await Promise.all(validationPromises);
  
  const errors = results.filter(r => r !== null) as string[];
  
  if (errors.length > 0) {
    console.error(`Found ${errors.length} broken links in ${filePath}:`);
    errors.forEach(error => console.error(`- ${error}`));
  } else {
    console.log(`All links in ${filePath} are valid.`);
  }
  return errors;
}

const ROOT_DIR = path.resolve(__dirname, '..');
const IGNORE_PATTERNS = ['.git', '.cursor', 'node_modules', 'scripts', 'brand'];

async function findMarkdownFiles(dir: string): Promise<string[]> {
    let mdFiles: string[] = [];
    const entries = await fs.promises.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (IGNORE_PATTERNS.some(p => fullPath.includes(path.sep + p))) continue;
        if (entry.isDirectory()) {
            mdFiles = mdFiles.concat(await findMarkdownFiles(fullPath));
        } else if (entry.isFile() && (entry.name.endsWith('.md') || entry.name.endsWith('.mdc'))) {
            mdFiles.push(fullPath);
        }
    }
    return mdFiles;
}

async function main() {
  const allFiles = await findMarkdownFiles(ROOT_DIR);
  let allErrors: string[] = [];

  for (const filePath of allFiles) {
    const relativePath = path.relative(ROOT_DIR, filePath);
    await fixAmpersands(relativePath);
    const errors = await validateMarkdownFile(relativePath);
    if (errors && errors.length > 0) {
      allErrors = allErrors.concat(errors.map(e => `${relativePath}: ${e}`));
    }
  }

  if (allErrors.length > 0) {
    console.error(`\nFound a total of ${allErrors.length} broken links across all files.`);
    process.exit(1);
  } else {
    console.log('\n✅ All links in all markdown files are valid!');
  }
}

main().catch(err => {
  console.error("An unexpected error occurred:", err);
  process.exit(1);
}); 