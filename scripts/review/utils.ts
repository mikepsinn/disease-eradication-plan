import fs from 'fs/promises';
import matter from 'gray-matter';
import { simpleGit } from 'simple-git';
import { glob } from 'glob';
import ignore from 'ignore';
import { GoogleGenerativeAI } from '@google/generative-ai';

const git = simpleGit();

// --- LLM Setup ---
const API_KEY = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
if (!API_KEY) {
  throw new Error('GOOGLE_GENERATIVE_AI_API_KEY is not set in the .env file.');
}
const genAI = new GoogleGenerativeAI(API_KEY);
const model = genAI.getGenerativeModel({ model: 'gemini-2.5-pro' });

// --- Exported Functions ---

export async function getStaleFiles(checkType: string): Promise<string[]> {
  const gitignoreContent = await fs.readFile('.gitignore', 'utf-8');
  const ig = ignore().add(gitignoreContent);

  const allQmdFiles = glob.sync('**/*.qmd', { ignore: 'node_modules/**' });
  const qmdFiles = ig.filter(allQmdFiles);
  
  const staleFiles: string[] = [];

  for (const file of qmdFiles) {
    try {
      const content = await fs.readFile(file, 'utf-8');
      const { data: frontmatter } = matter(content);

      const log = await git.log({ file, maxCount: 1 });
      if (!log.latest) {
        console.warn(`Could not get git log for ${file}. Skipping.`);
        continue;
      }
      const lastModified = new Date(log.latest.date);
      const lastCheck = frontmatter[checkType] ? new Date(frontmatter[checkType]) : null;

      if (!lastCheck || lastModified > lastCheck) {
        staleFiles.push(file);
      }
    } catch (error) {
      console.error(`Error processing file ${file}:`, error);
    }
  }

  return staleFiles;
}

export async function formatFileWithLLM(filePath: string): Promise<void> {
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(originalContent);

  const prompt = `
    Please reformat the following markdown file content to adhere strictly to our project's contribution guidelines.

    **CRITICAL INSTRUCTION: You are a formatting engine. Your ONLY task is to fix objective formatting errors. Do NOT alter the writing style, tone, or content in any way. The user's original phrasing and voice must be perfectly preserved.**

    **Formatting Rules to Enforce:**
    1.  **One Sentence Per Line:** Each sentence must start on a new line. Break lines *only* after a period, question mark, or exclamation point that is followed by a space.
    2.  **Dollar Sign Escaping:** All dollar signs (\$) in plain text must be escaped (e.g., \\\$2.7 trillion). Do not escape them inside markdown code blocks (\`\`\`) or tables.
    3.  **List Spacing:** Ensure all markdown lists (ordered and unordered) are preceded by exactly one empty line.
    4.  **Markdown Integrity:** Preserve all original markdown formatting, including headers, tables, and code blocks, without any alteration.
  `;

  const result = await model.generateContent(prompt + `\n\n**File Content to Reformulate:**\n---\n${body}\n---`);
  const response = await result.response;
  const newBody = response.text();

  const today = new Date().toISOString().split('T')[0];
  frontmatter.lastFormatted = today;
  frontmatter.lastStyleCheck = today;

  const newContent = matter.stringify(newBody, frontmatter);
  await fs.writeFile(filePath, newContent, 'utf-8');
}
