import fs from 'fs/promises';
import matter from 'gray-matter';
import { simpleGit } from 'simple-git';
import { glob } from 'glob';
import crypto from 'crypto';
import ignore from 'ignore';
import { GoogleGenerativeAI } from '@google/generative-ai';
import Anthropic from '@anthropic-ai/sdk';
import dotenv from 'dotenv';
import path from 'path';

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
  const prompt = `You are an expert copy editor tasked with improving a chapter of a book called "The Complete Idiot's Guide to Ending War and Disease." 
  Your goal is to revise the following text to perfectly match the tone and style defined in the provided style guide.

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

export async function factCheckFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nFact-checking ${filePath} with Gemini 2.5 Pro...`);
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(originalContent);

  const citationGuide = await fs.readFile('CONTRIBUTING.md', 'utf-8');
  const prompt = `You are an expert fact-checker auditing a chapter of a book. Your task is to identify any factual claims that are not properly cited according to the project's standards.

  **CRITICAL INSTRUCTIONS:**
  1.  Read the Sourcing and Citation Standard section from the provided guide.
  2.  A "factual claim" is any statement that presents data, statistics, or a specific, verifiable assertion (e.g., "costs \$2.6 billion," "approvals dropped 70%," "10,000+ excess deaths").
  3.  A claim is considered "cited" if it is immediately part of a markdown link pointing to "references.qmd". For example: \`[The FDA is slow](../references.qmd#fda-slow)\`.
  4.  Your task is to find all factual claims that are **NOT** cited in this way.
  5.  **If you find one or more uncited claims, return them as a direct quote in a numbered list.**
  6.  **If all claims are properly cited, you MUST return the special string "NO_UNCITED_CLAIMS_FOUND".**
  7.  Return *only* the numbered list of uncited claims or the special string. Do not include any other text, explanations, or markdown formatting.

  ${citationGuide}

  **File Content to Fact-Check:**
  ${body}`;

  const result = await geminiModel.generateContent(prompt);
  const response = await result.response;
  const responseText = response.text().trim();

  if (responseText === 'NO_UNCITED_CLAIMS_FOUND') {
    console.log(`No uncited claims found in ${filePath}.`);
  } else {
    console.warn(`WARNING: Found potential uncited claims in ${filePath}:\n${responseText}`);
    // In a more advanced implementation, we could add TODOs to the file.
    // For now, we will just warn the user.
  }

  const today = new Date().toISOString().split('T')[0];
  frontmatter.lastFactCheck = today;

  const newContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  await fs.writeFile(filePath, newContent, 'utf-8');
  console.log(`Successfully updated fact-check metadata for ${filePath}.`);
}

export async function linkCheckFile(filePath: string): Promise<void> {
  console.log(`\nChecking links in ${filePath}...`);
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(originalContent);

  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  let match;
  const brokenLinks: string[] = [];
  const directory = path.dirname(filePath);

  while ((match = linkRegex.exec(body)) !== null) {
    const link = match[2];

    // Ignore external links and empty links
    if (link.startsWith('http') || link.startsWith('https') || !link) {
      continue;
    }

    const [linkPath, anchor] = link.split('#');
    const absolutePath = path.resolve(directory, linkPath);

    try {
      await fs.access(absolutePath);
      // File exists, now check anchor if it exists
      if (anchor) {
        const targetContent = await fs.readFile(absolutePath, 'utf-8');
        const anchorRegex = new RegExp(`id="${anchor}"`);
        if (!anchorRegex.test(targetContent)) {
          brokenLinks.push(`Broken anchor in ${filePath}: Anchor #${anchor} not found in ${linkPath}`);
        }
      }
    } catch (error) {
      brokenLinks.push(`Broken link in ${filePath}: ${linkPath} not found.`);
    }
  }

  if (brokenLinks.length > 0) {
    console.warn(`WARNING: Found broken links in ${filePath}:\n${brokenLinks.join('\n')}`);
  } else {
    console.log(`No broken links found in ${filePath}.`);
  }

  const today = new Date().toISOString().split('T')[0];
  frontmatter.lastLinkCheck = today;

  const newContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  await fs.writeFile(filePath, newContent, 'utf-8');
  console.log(`Successfully updated link-check metadata for ${filePath}.`);
}

export async function figureCheckFile(filePath: string): Promise<void> {
  console.log(`\nChecking figures and design elements in ${filePath}...`);
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(originalContent);

  const designGuide = await fs.readFile('DESIGN_GUIDE.md', 'utf-8');
  const designViolations: string[] = [];

  // --- Check for included Quarto chart files ---
  const includeRegex = /{{<\s*include\s+([^>]+)\s*>}}/g;
  let includeMatch;
  while ((includeMatch = includeRegex.exec(body)) !== null) {
    const includedPath = includeMatch[1].trim();
    if (includedPath.startsWith('brain/figures')) {
      const chartFilePath = path.resolve(includedPath);
      try {
        const chartContent = await fs.readFile(chartFilePath, 'utf-8');
        if (chartContent.includes('plt.tight_layout()')) {
          designViolations.push(`Design violation in ${chartFilePath}: Use of 'plt.tight_layout()' is discouraged.`);
        }
        if (!chartContent.includes('setup_chart_style()')) {
          designViolations.push(`Design violation in ${chartFilePath}: Missing 'setup_chart_style()'.`);
        }
        if (!chartContent.includes('add_watermark()')) {
          designViolations.push(`Design violation in ${chartFilePath}: Missing 'add_watermark()'.`);
        }
      } catch (error) {
        designViolations.push(`Could not read included chart file: ${chartFilePath}`);
      }
    }
  }

  // --- Check for static images ---
  const imageRegex = /!\[[^\]]*\]\(([^)]+)\)/g;
  let imageMatch;
  while ((imageMatch = imageRegex.exec(body)) !== null) {
    const imagePath = imageMatch[1];
    if (!imagePath.startsWith('http') && !imagePath.includes('assets/')) {
      designViolations.push(`Design violation in ${filePath}: Static image '${imagePath}' is not in the 'assets/' directory.`);
    }
  }

  if (designViolations.length > 0) {
    console.warn(`WARNING: Found design guide violations for ${filePath}:\n${designViolations.join('\n')}`);
  } else {
    console.log(`No design guide violations found in ${filePath}.`);
  }

  const today = new Date().toISOString().split('T')[0];
  frontmatter.lastFigureCheck = today;

  const newContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  await fs.writeFile(filePath, newContent, 'utf-8');
  console.log(`Successfully updated figure-check metadata for ${filePath}.`);
}
