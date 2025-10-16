import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';

// Define the required frontmatter fields
const REQUIRED_FRONTMATTER = ['title', 'description', 'published', 'date', 'tags', 'lastReviewed'];

async function checkFileFormatting(filePath: string): Promise<string[]> {
  const errors: string[] = [];
  const content = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(content);

  // 1. Check for required frontmatter fields
  for (const field of REQUIRED_FRONTMATTER) {
    if (!frontmatter[field]) {
      errors.push(`Missing required frontmatter field: "${field}"`);
    }
  }

  // 2. Check for unescaped dollar signs in the body
  const dollarRegex = /(?<!\\)\$/g;
  const lines = body.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    // Ignore code blocks for dollar sign checks
    if (line.trim().startsWith('```')) {
      continue;
    }
    if (dollarRegex.test(line)) {
      errors.push(`Found unescaped dollar sign on line ${i + 1}: "${line.trim()}"`);
    }
  }

  // 3. Check for multiple sentences on the same line
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line.includes('. ') || line.includes('? ') || line.includes('! ')) {
        if (!line.startsWith('> ') && !line.startsWith('| ') && !line.startsWith('- ') && !line.startsWith('1.')) {
             errors.push(`Found multiple sentences on line ${i + 1}: "${line}"`);
        }
    }
  }

  return errors;
}

async function main() {
  const filePath = process.argv[2];
  if (!filePath) {
    console.error('Please provide a file path to check.');
    process.exit(1);
  }

  const absolutePath = path.resolve(filePath);
  const errors = await checkFileFormatting(absolutePath);

  if (errors.length > 0) {
    console.error(`Found ${errors.length} formatting errors in ${filePath}:`);
    for (const error of errors) {
      console.error(`- ${error}`);
    }
    process.exit(1);
  } else {
    console.log(`No formatting errors found in ${filePath}.`);
  }
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
