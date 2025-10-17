import fs from 'fs/promises';
import matter from 'gray-matter';
import { simpleGit } from 'simple-git';
import { glob } from 'glob';
import crypto from 'crypto';
import ignore from 'ignore';
import { GoogleGenAI, Type } from '@google/genai';
import Anthropic from '@anthropic-ai/sdk';
import dotenv from 'dotenv';
import path from 'path';

dotenv.config();

const git = simpleGit();

// --- LLM Setup ---
// DO NOT CHANGE THESE MODEL NUMBERS
const GEMINI_MODEL_ID = 'gemini-2.5-pro';
const CLAUDE_MODEL_ID = 'claude-opus-4-1-20250805';

const API_KEY = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
if (!API_KEY) {
  throw new Error('GOOGLE_GENERATIVE_AI_API_KEY is not set in the .env file.');
}

// Initialize Google Generative AI client
const genAI = new GoogleGenAI({
  apiKey: API_KEY
});

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
  console.log(`\nFormatting ${filePath} with ${GEMINI_MODEL_ID}...`);
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(originalContent);

  const formattingGuide = await fs.readFile('FORMATTING_GUIDE.md', 'utf-8');
  const prompt = `${formattingGuide}\n\nYour task is to reformat the following file content based *only* on the rules above. **If the file already conforms to all rules, you MUST return the special string "NO_CHANGES_NEEDED".** Otherwise, return *only* the corrected file content, with no other text or separators.`;

  const result = await genAI.models.generateContent({
    model: GEMINI_MODEL_ID,
    contents: prompt + `\n\n**File Content to Reformulate:**\n${body}`
  });
  const responseText = result.text || '';

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
    model: CLAUDE_MODEL_ID,
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
  console.log(`\nFact-checking ${filePath} with ${GEMINI_MODEL_ID}...`);
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

  const result = await genAI.models.generateContent({
    model: GEMINI_MODEL_ID,
    contents: claimIdentificationPrompt
  });
  const responseText = (result.text || '').trim();

  if (responseText === 'NO_UNCITED_CLAIMS_FOUND') {
    console.log(`No uncited claims found in ${filePath}.`);
  } else {
    console.log(`Found potential uncited claims. Attempting to find sources...`);
    const claims = responseText.split('\n').map(line => line.replace(/^\d+\.\s*/, '').trim()).filter(Boolean);
    
    let newBody = body;
    let referencesToAdd = '';

    for (const claim of claims) {
      const sourceFindingPrompt = `Find authoritative sources to verify this claim: "${claim}"

      Search for reliable sources using Google Search. If you find credible sources, return verified: true and include the source details. If you cannot verify the claim, return verified: false.`;

      try {
        const sourceResult = await genAI.models.generateContent({
          model: GEMINI_MODEL_ID,
          contents: sourceFindingPrompt,
          config: {
            tools: [{ googleSearch: {} }],
            responseMimeType: "application/json",
            responseSchema: {
              type: Type.OBJECT,
              properties: {
                claim: {
                  type: Type.STRING,
                  description: "The original claim being verified"
                },
                verified: {
                  type: Type.BOOLEAN,
                  description: "Whether the claim was verified with credible sources"
                },
                sources: {
                  type: Type.ARRAY,
                  description: "Array of sources that verify the claim",
                  items: {
                    type: Type.OBJECT,
                    properties: {
                      title: {
                        type: Type.STRING,
                        description: "Title of the source"
                      },
                      url: {
                        type: Type.STRING,
                        description: "URL of the source"
                      },
                      snippet: {
                        type: Type.STRING,
                        description: "Relevant excerpt from the source"
                      }
                    },
                    required: ["title", "url", "snippet"]
                  }
                }
              },
              required: ["claim", "verified", "sources"]
            }
          }
        });

        const sourceData = JSON.parse(sourceResult.text || '{}');

        if (sourceData.verified && sourceData.sources && sourceData.sources.length > 0) {
          // Create reference entry with anchor
          const anchorId = `ref-${crypto.randomBytes(4).toString('hex')}`;
          const referenceEntry = `\n<a id="${anchorId}"></a>\n**${sourceData.sources[0].title}**\n${sourceData.sources[0].snippet}\n[Source](${sourceData.sources[0].url})\n`;

          referencesToAdd += referenceEntry;
          const escapedClaim = claim.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
          newBody = newBody.replace(new RegExp(escapedClaim, 'g'), `[${claim}](../references.qmd#${anchorId})`);

          console.log(`✓ Found source for: "${claim.substring(0, 50)}..."`);
        } else {
          throw new Error('No verified sources found');
        }

      } catch (error) {
        console.error(`Failed to find source for claim: "${claim}". Adding TODO.`, error);
        const todoComment = `<!-- TODO: FACT_CHECK - Uncited claim. LLM failed to find a source. -->`;
        const escapedClaim = claim.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        if (!newBody.includes(todoComment)) {
          newBody = newBody.replace(new RegExp(escapedClaim, 'g'), `${todoComment}\n${claim}`);
        }
      }
    }
    
    if (referencesToAdd) {
      await fs.appendFile('brain/book/references.qmd', referencesToAdd);
    }
    
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
