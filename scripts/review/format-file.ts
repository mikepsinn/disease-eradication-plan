import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { GoogleGenerativeAI } from '@google/generative-ai';
import dotenv from 'dotenv';

dotenv.config();

const API_KEY = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
if (!API_KEY) {
  throw new Error('GOOGLE_GENERATIVE_AI_API_KEY is not set in the .env file.');
}

const genAI = new GoogleGenerativeAI(API_KEY);
const model = genAI.getGenerativeModel({ model: 'gemini-2.5-pro' });

async function formatFileWithLLM(filePath: string): Promise<void> {
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

    **File Content to Reformulate:**
    ---
    ${body}
    ---
  `;

  const result = await model.generateContent(prompt);
  const response = await result.response;
  const newBody = response.text();

  // Update frontmatter timestamps
  const today = new Date().toISOString().split('T')[0];
  frontmatter.lastFormatted = today;
  frontmatter.lastStyleCheck = today; // Since this script now handles both

  const newContent = matter.stringify(newBody, frontmatter);

  await fs.writeFile(filePath, newContent, 'utf-8');
}

async function main() {
  const filePath = process.argv[2];
  if (!filePath) {
    console.error('Please provide a file path to format.');
    process.exit(1);
  }

  const absolutePath = path.resolve(filePath);
  console.log(`Formatting ${absolutePath} with Gemini 2.5 Pro...`);
  await formatFileWithLLM(absolutePath);
  console.log('Formatting complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
