import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { simpleGit } from 'simple-git';
import { glob } from 'glob';
import ignore from 'ignore';

const git = simpleGit();

// The types of checks we can perform on a file
const CHECK_TYPES = [
  'lastFormatted',
  'lastStyleCheck',
  'lastFactCheck',
  'lastLinkCheck',
  'lastFigureCheck',
];

interface StaleFiles {
  [key: string]: string[];
}

async function getStaleFiles(): Promise<StaleFiles> {
  const gitignoreContent = await fs.readFile('.gitignore', 'utf-8');
  const ig = ignore().add(gitignoreContent);

  const allQmdFiles = glob.sync('**/*.qmd', { ignore: 'node_modules/**' });
  const qmdFiles = ig.filter(allQmdFiles);
  
  const staleFiles: StaleFiles = {};
  for (const check of CHECK_TYPES) {
    staleFiles[check] = [];
  }

  for (const file of qmdFiles) {
    try {
      const content = await fs.readFile(file, 'utf-8');
      const { data: frontmatter } = matter(content);

      // Get the last commit date for the file
      const log = await git.log({ file, maxCount: 1 });
      if (!log.latest) {
        console.warn(`Could not get git log for ${file}. Skipping.`);
        continue;
      }
      const lastModified = new Date(log.latest.date);

      for (const check of CHECK_TYPES) {
        const lastCheckDate = frontmatter[check] ? new Date(frontmatter[check]) : null;
        if (!lastCheckDate || lastModified > lastCheckDate) {
          staleFiles[check].push(file);
        }
      }
    } catch (error) {
      console.error(`Error processing file ${file}:`, error);
    }
  }

  return staleFiles;
}

async function main() {
  const staleFiles = await getStaleFiles();
  console.log('Files needing review:');
  console.log(JSON.stringify(staleFiles, null, 2));
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
