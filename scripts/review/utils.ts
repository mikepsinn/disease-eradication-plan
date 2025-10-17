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
const geminiModel = genAI.getGenerativeModel({ model: 'gemini-1.5-pro' });
const groundingTool = { googleSearch: {} };
const geminiModelWithSearch = genAI.getGenerativeModel({ model: 'gemini-1.5-pro', tools: [groundingTool] });

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

export async function getStaleFiles(hashFieldName: string): Promise<string[]> {
  const gitignoreContent = await fs.readFile('.gitignore', 'utf-8');
  const ig = ignore().add(gitignoreContent);

  const allQmdFiles = glob.sync('**/*.qmd', { ignore: 'node_modules/**' });
  const qmdFiles = ig.filter(allQmdFiles);
  
  const staleFiles: string[] = [];

  for (const file of qmdFiles) {
    try {
      const content = await fs.readFile(file, 'utf-8');
      const { data: frontmatter } = matter(content);

      const lastHash = frontmatter[hashFieldName];
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

  const tempContent = matter.stringify(finalBody, frontmatter, { lineWidth: -1 } as any);
  frontmatter.lastStyleHash = getBodyHash(tempContent);

  const newContent = matter.stringify(finalBody, frontmatter, { lineWidth: -1 } as any);
  await fs.writeFile(filePath, newContent, 'utf-8');
  console.log(`Successfully improved style for ${filePath}.`);
}

export async function factCheckFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nFact-checking ${filePath} with Gemini 1.5 Pro...`);
  let originalContent = await fs.readFile(filePath, 'utf-8');
  let { data: frontmatter, content: body } = matter(originalContent);

  const citationGuide = await fs.readFile('CONTRIBUTING.md', 'utf-8');
  const claimIdentificationPrompt = `You are an expert fact-checker. Your task is to identify all factual claims in the provided text that are not properly cited.
  
  **CRITICAL INSTRUCTIONS:**
  1. A "factual claim" is a statement with specific data, statistics, or verifiable facts.
  2. A claim is "cited" if it's a markdown link to "references.qmd".
  3. Return a numbered list of exact, verbatim quotes of **only the uncited claims**.
  4. If all claims are cited, you MUST return the special string "NO_UNCITED_CLAIMS_FOUND".

  **Text to Analyze:**
  ${body}`;

  const result = await geminiModel.generateContent(claimIdentificationPrompt);
  const response = await result.response;
  const responseText = response.text().trim();

  if (responseText === 'NO_UNCITED_CLAIMS_FOUND') {
    console.log(`No uncited claims found in ${filePath}.`);
  } else {
    console.log(`Found potential uncited claims in ${filePath}. Now attempting to find sources...`);
    const claims = responseText.split('\n').map(line => line.replace(/^\d+\.\s*/, '').trim());
    
    let newBody = body;
    for (const claim of claims) {
      const sourceFindingPrompt = `You are a research assistant. Find the most credible, primary source URL that verifies the following claim. Then, generate a pre-formatted markdown snippet for a references file.
      
      **CRITICAL INSTRUCTIONS:**
      1. Use Google Search to find the best source for the claim.
      2. Return a JSON object with three keys: "sourceURL", "quote", and "snippet".
      3. "quote" should be the verbatim text from the source that supports the claim.
      4. "snippet" should be a complete, formatted markdown block for references.qmd.
      
      **Claim to Verify:**
      "${claim}"`;

      try {
        const sourceResult = await geminiModelWithSearch.generateContent(sourceFindingPrompt);
        const sourceResponse = await sourceResult.response;
        const sourceText = sourceResponse.text().replace(/```json|```/g, '').trim();
        const sourceData = JSON.parse(sourceText);

        const todoComment = `<!-- 
TODO: FACT_CHECK - The following claim is uncited. A potential source has been found by the LLM. Please verify the source and add it to references.qmd.

Claim: "${claim}"

Suggested Source: ${sourceData.sourceURL}

Suggested Snippet for references.qmd:
${sourceData.snippet}
-->`;
        
        // Escape special characters in the claim for regex replacement
        const escapedClaim = claim.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        newBody = newBody.replace(new RegExp(escapedClaim, 'g'), `${todoComment}\n${claim}`);

      } catch (error) {
        console.error(`Failed to find source for claim: "${claim}"`, error);
        const todoComment = `<!-- TODO: FACT_CHECK - The following claim is uncited. The LLM failed to find a source. Please find a source manually. -->`;
        const escapedClaim = claim.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        newBody = newBody.replace(new RegExp(escapedClaim, 'g'), `${todoComment}\n${claim}`);
      }
    }
    
    // Update the body content before writing the file
    body = newBody;
  }

  frontmatter.lastFactCheckHash = getBodyHash(matter.stringify(body, frontmatter));
  const newContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  await fs.writeFile(filePath, newContent, 'utf-8');
  console.log(`Successfully updated fact-check metadata for ${filePath}.`);
}

export async function linkCheckFile(filePath: string): Promise<void> {
  console.log(`\nChecking links in ${filePath}...`);
  let originalContent = await fs.readFile(filePath, 'utf-8');
  let { data: frontmatter, content: body } = matter(originalContent);

  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  let match;
  let newBody = body;
  let issuesFound = false;

  // Create a new array of matches to avoid issues with modifying the string during iteration
  const matches = Array.from(body.matchAll(linkRegex));

  for (const match of matches) {
    const fullMatch = match[0];
    const link = match[2];

    if (link.startsWith('http') || link.startsWith('https') || !link) {
      continue;
    }

    const [linkPath, anchor] = link.split('#');
    const absolutePath = path.resolve(path.dirname(filePath), linkPath);
    let issueDescription = '';

    try {
      await fs.access(absolutePath);
      if (anchor) {
        const targetContent = await fs.readFile(absolutePath, 'utf-8');
        if (!targetContent.includes(`id="${anchor}"`)) {
          issueDescription = `Broken anchor: #${anchor} not found in ${linkPath}`;
        }
      }
    } catch (error) {
      issueDescription = `Broken link: ${linkPath} not found.`;
    }

    if (issueDescription) {
      issuesFound = true;
      const todoComment = `<!-- TODO: LINK_CHECK - ${issueDescription} -->`;
      // Prevent adding duplicate TODOs
      if (!newBody.includes(todoComment)) {
        newBody = newBody.replace(fullMatch, `${todoComment}\n${fullMatch}`);
      }
    }
  }

  if (issuesFound) {
    console.warn(`WARNING: Found and marked broken links in ${filePath}.`);
    body = newBody; // Update body with TODOs
  } else {
    console.log(`No broken links found in ${filePath}.`);
  }

  frontmatter.lastLinkCheckHash = getBodyHash(matter.stringify(body, frontmatter));
  const newContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  await fs.writeFile(filePath, newContent, 'utf-8');
  console.log(`Successfully updated link-check metadata for ${filePath}.`);
}

export async function figureCheckFile(filePath: string): Promise<void> {
  console.log(`\nChecking figures and design elements in ${filePath}...`);
  let originalContent = await fs.readFile(filePath, 'utf-8');
  let { data: frontmatter, content: body } = matter(originalContent);
  let newBody = body;
  let issuesFound = false;

  // --- Check for included Quarto chart files ---
  const includeRegex = /{{<\s*include\s+([^>]+)\s*>}}/g;
  const includeMatches = Array.from(body.matchAll(includeRegex));
  for (const match of includeMatches) {
    const fullMatch = match[0];
    const includedPath = match[1].trim();
    if (includedPath.startsWith('brain/figures')) {
      const chartFilePath = path.resolve(includedPath);
      try {
        const chartContent = await fs.readFile(chartFilePath, 'utf-8');
        const violations = [];
        if (chartContent.includes('plt.tight_layout()')) {
          violations.push(`Use of 'plt.tight_layout()' is discouraged.`);
        }
        if (!chartContent.includes('setup_chart_style()')) {
          violations.push(`Missing 'setup_chart_style()'.`);
        }
        if (!chartContent.includes('add_watermark()')) {
          violations.push(`Missing 'add_watermark()'.`);
        }
        if (violations.length > 0) {
          issuesFound = true;
          const todoComment = `<!-- TODO: FIGURE_CHECK - Design violations in ${includedPath}: ${violations.join(' ')} -->`;
          if (!newBody.includes(todoComment)) {
            newBody = newBody.replace(fullMatch, `${todoComment}\n${fullMatch}`);
          }
        }
      } catch (error) {
        // This case is handled by the link checker
      }
    }
  }

  // --- Check for static images ---
  const imageRegex = /!\[[^\]]*\]\(([^)]+)\)/g;
  const imageMatches = Array.from(body.matchAll(imageRegex));
  for (const match of imageMatches) {
    const fullMatch = match[0];
    const imagePath = match[1];
    if (!imagePath.startsWith('http') && !imagePath.includes('assets/')) {
      issuesFound = true;
      const todoComment = `<!-- TODO: FIGURE_CHECK - Static image '${imagePath}' should be in the 'assets/' directory. -->`;
      if (!newBody.includes(todoComment)) {
        newBody = newBody.replace(fullMatch, `${todoComment}\n${fullMatch}`);
      }
    }
  }

  if (issuesFound) {
    console.warn(`WARNING: Found and marked design guide violations in ${filePath}.`);
    body = newBody;
  } else {
    console.log(`No design guide violations found in ${filePath}.`);
  }

  frontmatter.lastFigureCheckHash = getBodyHash(matter.stringify(body, frontmatter));
  const newContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  await fs.writeFile(filePath, newContent, 'utf-8');
  console.log(`Successfully updated figure-check metadata for ${filePath}.`);
}
