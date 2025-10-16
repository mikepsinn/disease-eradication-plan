import fs from 'fs/promises';
import matter from 'gray-matter';
import { simpleGit } from 'simple-git';
import { glob } from 'glob';
import crypto from 'crypto';
import ignore from 'ignore';
import { GoogleGenerativeAI } from '@google/generative-ai';
import Anthropic from '@anthropic-ai/sdk';
import dotenv from 'dotenv';

dotenv.config();

const git = simpleGit();

// --- LLM Setup ---
const API_KEY = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
if (!API_KEY) {
  throw new Error('GOOGLE_GENERATIVE_AI_API_KEY is not set in the .env file.');
}
const genAI = new GoogleGenerativeAI(API_KEY);
const geminiModel = genAI.getGenerativeModel({ model: 'gemini-2.5-pro' });

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});
if (!process.env.ANTHROPIC_API_KEY) {
  throw new Error('ANTHROPIC_API_KEY is not set in the .env file.');
}

// --- Helper Functions ---

function getBodyHash(content: string): string {
  const { content: body } = matter(content);
  return crypto.createHash('sha256').update(body).digest('hex');
}

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

      const lastHash = frontmatter.lastFormattedHash;

      if (!lastHash) {
        staleFiles.push(file);
        continue;
      }

      const currentBodyHash = getBodyHash(content);
      if (currentBodyHash !== lastHash) {
        staleFiles.push(file);
      }
    } catch (error) {
      console.error(`Error processing file ${file}:`, error);
    }
  }

  return staleFiles;
}

export async function formatFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nFormatting ${filePath} with Gemini 2.5 Pro...`);
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(originalContent);

  const formattingGuide = await fs.readFile('FORMATTING_GUIDE.md', 'utf-8');
  const prompt = `${formattingGuide}\n\nYour task is to reformat the following file content based *only* on the rules above. **If the file already conforms to all rules, you MUST return the special string "NO_CHANGES_NEEDED".** Otherwise, return *only* the corrected file content, with no other text or separators.`;

  const result = await geminiModel.generateContent(prompt + `\n\n**File Content to Reformulate:**\n${body}`);
  const response = await result.response;
  const responseText = response.text();

  let finalBody;
  if (responseText.trim() === 'NO_CHANGES_NEEDED') {
    console.log(`File ${filePath} is already formatted correctly. Updating metadata.`);
    finalBody = body; // Use the original body
  } else {
    // Clean up potential trailing separators from the LLM response
    finalBody = responseText.trim().replace(/(\s*---|\s*```)*\s*$/, '');
  }

  const today = new Date().toISOString().split('T')[0];
  frontmatter.lastFormatted = today;
  frontmatter.lastStyleCheck = today;

  // To ensure hash consistency, we create a temporary stringified version
  // to see what the body will look like after gray-matter processes it.
  const tempContent = matter.stringify(finalBody, frontmatter, { lineWidth: -1 } as any);
  
  // Now, hash the body as it will actually be saved.
  frontmatter.lastFormattedHash = getBodyHash(tempContent);

  // Stringify the final version with the correct hash and write to file.
  const newContent = matter.stringify(finalBody, frontmatter, { lineWidth: -1 } as any);
  await fs.writeFile(filePath, newContent, 'utf-8');
  console.log(`Successfully formatted ${filePath}.`);
}

export async function styleFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nImproving style for ${filePath} with Claude Opus...`);
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(originalContent);

  const styleGuide = await fs.readFile('STYLE_GUIDE.md', 'utf-8');
  const prompt = `You are an expert copy editor tasked with improving a chapter of a book called "The Complete Idiot's Guide to Ending War and Disease." Your goal is to revise the following text to perfectly match the tone and style defined in the provided style guide.

  **CRITICAL INSTRUCTIONS:**
  1.  **Adhere strictly to the STYLE_GUIDE.md.** The tone is paramount: dark humor, cynical but loving observations, and actionable, empowering language.
  2.  **Preserve the original meaning and all facts.** Do not add or remove information.
  3.  **Do not touch frontmatter, markdown, or Quarto syntax.** Only modify the prose.
  4.  **If the file already perfectly adheres to the style guide, you MUST return the special string "NO_CHANGES_NEEDED".**
  5.  Otherwise, return *only* the revised prose. Do not include any other text, explanations, or markdown formatting.

  ${styleGuide}

  **File Content to Improve:**
  ${body}`;

  const msg = await anthropic.messages.create({
    model: "claude-opus-4-1-20250805",
    max_tokens: 8192,
    messages: [{ role: "user", content: prompt }],
  });

  const responseBlock = msg.content[0];
  if (responseBlock.type !== 'text') {
    throw new Error('Unexpected response format from Anthropic API. Expected a text block.');
  }
  const responseText = responseBlock.text;

  let finalBody;
  if (responseText.trim() === 'NO_CHANGES_NEEDED') {
    console.log(`File ${filePath} already adheres to the style guide. Updating metadata.`);
    finalBody = body;
  } else {
    finalBody = responseText.trim();
  }

  const today = new Date().toISOString().split('T')[0];
  frontmatter.lastStyleCheck = today;

  const tempContent = matter.stringify(finalBody, frontmatter, { lineWidth: -1 } as any);
  frontmatter.lastStyleHash = getBodyHash(tempContent);

  const newContent = matter.stringify(finalBody, frontmatter, { lineWidth: -1 } as any);
  await fs.writeFile(filePath, newContent, 'utf-8');
  console.log(`Successfully improved style for ${filePath}.`);
}
