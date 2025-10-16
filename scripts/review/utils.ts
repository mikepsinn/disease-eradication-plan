import fs from 'fs/promises';
import matter from 'gray-matter';
import { simpleGit } from 'simple-git';
import { glob } from 'glob';
import crypto from 'crypto';
import ignore from 'ignore';
import { GoogleGenerativeAI } from '@google/generative-ai';
import dotenv from 'dotenv';

dotenv.config();

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

      const currentHash = crypto.createHash('sha256').update(content).digest('hex');
      const lastHash = frontmatter.lastFormattedHash;

      if (currentHash !== lastHash) {
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

  const formattingGuide = await fs.readFile('FORMATTING_GUIDE.md', 'utf-8');
  const prompt = `${formattingGuide}\n\nPlease reformat the following file content based on the rules above.`;

  const result = await model.generateContent(prompt + `\n\n**File Content to Reformulate:**\n---\n${body}\n---`);
  const response = await result.response;
  const newBody = response.text();

  const today = new Date().toISOString().split('T')[0];
  frontmatter.lastFormatted = today;
  frontmatter.lastStyleCheck = today;
  frontmatter.lastFormattedHash = crypto.createHash('sha256').update(newBody).digest('hex');

  const newContent = matter.stringify(newBody, frontmatter);
  await fs.writeFile(filePath, newContent, 'utf-8');
}
