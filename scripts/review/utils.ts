import fs from 'fs/promises';
import matter from 'gray-matter';
import { simpleGit } from 'simple-git';
import { glob } from 'glob';
import crypto from 'crypto';
import ignore from 'ignore';
import { GoogleGenAI } from '@google/genai';
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

// Parse references.qmd into structured array
interface Reference {
  id: string;
  title: string;
  quotes: string[];
  source: string;
}

function parseReferences(referencesContent: string): Reference[] {
  const references: Reference[] = [];
  const lines = referencesContent.split('\n');
  const seenIds = new Map<string, number>(); // Track IDs and their first occurrence line

  let currentRef: Reference | null = null;
  let inQuoteBlock = false;
  let currentQuote = '';
  let currentLineNumber = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    currentLineNumber = i + 1;

    // Match anchor tags: <a id="anchor-id"></a>
    const anchorMatch = line.match(/<a\s+id="([^"]+)"><\/a>/);
    if (anchorMatch) {
      if (currentRef) {
        references.push(currentRef);
      }

      const id = anchorMatch[1];

      // Check for duplicate IDs
      if (seenIds.has(id)) {
        console.warn(`⚠ Duplicate reference ID "${id}" found at line ${currentLineNumber} (first seen at line ${seenIds.get(id)})`);
        console.warn(`  → Merging entries with same ID`);

        // Find the existing reference and merge with it
        const existingRef = references.find(r => r.id === id);
        if (existingRef) {
          currentRef = existingRef;
          continue;
        }
      }

      seenIds.set(id, currentLineNumber);
      currentRef = {
        id: id,
        title: '',
        quotes: [],
        source: ''
      };
      continue;
    }

    // Match title: - **Title text**
    const titleMatch = line.match(/^-\s+\*\*(.+)\*\*$/);
    if (titleMatch && currentRef) {
      // If title already exists and we're merging, append to quotes instead
      if (currentRef.title && currentRef.title !== titleMatch[1]) {
        // This is a second title for the same ID - add previous title as a note
        currentRef.quotes.push(`Alternative title: ${titleMatch[1]}`);
      } else if (!currentRef.title) {
        currentRef.title = titleMatch[1];
      }
      continue;
    }

    // Match quote lines: start with > followed by content or >—
    if (line.trim().startsWith('>')) {
      const quoteContent = line.trim().substring(1).trim();

      // Check if this is the source line (starts with —)
      if (quoteContent.startsWith('—')) {
        if (currentQuote && currentRef) {
          currentRef.quotes.push(currentQuote.trim());
          currentQuote = '';
        }
        if (currentRef) {
          // If we already have a source and this is different, append it
          const newSource = quoteContent.substring(1).trim();
          if (currentRef.source && currentRef.source !== newSource) {
            currentRef.source += ' | ' + newSource;
          } else if (!currentRef.source) {
            currentRef.source = newSource;
          }
        }
        inQuoteBlock = false;
      } else {
        // Regular quote content
        if (currentQuote) {
          currentQuote += '\n' + quoteContent;
        } else {
          currentQuote = quoteContent;
        }
        inQuoteBlock = true;
      }
    } else if (inQuoteBlock && currentQuote) {
      // End of quote block
      if (currentRef) {
        currentRef.quotes.push(currentQuote.trim());
      }
      currentQuote = '';
      inQuoteBlock = false;
    }
  }

  // Push the last reference
  if (currentRef) {
    references.push(currentRef);
  }

  // Deduplicate by ID (keep first occurrence)
  const uniqueReferences = new Map<string, Reference>();
  for (const ref of references) {
    if (!uniqueReferences.has(ref.id)) {
      uniqueReferences.set(ref.id, ref);
    }
  }

  return Array.from(uniqueReferences.values());
}

function formatReferencesFile(references: Reference[], frontmatter: string): string {
  // Sort by ID alphabetically
  const sorted = references.sort((a, b) => a.id.localeCompare(b.id));

  let output = frontmatter + '\n\n';

  for (const ref of sorted) {
    output += `<a id="${ref.id}"></a>\n`;
    output += `- **${ref.title}**\n`;
    for (const quote of ref.quotes) {
      output += `  > ${quote}\n`;
    }
    output += `  > — ${ref.source}\n\n`;
  }

  return output.trimEnd() + '\n';
}

export async function factCheckFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nFact-checking ${filePath} with ${GEMINI_MODEL_ID}...`);
  let originalContent = await fs.readFile(filePath, 'utf-8');
  let { data: frontmatter, content: body } = matter(originalContent);

  // Load and parse existing references
  let existingReferencesContent = '';
  let existingReferences: Reference[] = [];
  let referencesFrontmatter = '';

  try {
    existingReferencesContent = await fs.readFile('brain/book/references.qmd', 'utf-8');
    const refMatter = matter(existingReferencesContent);
    referencesFrontmatter = matter.stringify('', refMatter.data, { lineWidth: -1 } as any).trim();
    existingReferences = parseReferences(refMatter.content);
  } catch (error) {
    console.warn('Could not load references.qmd, will create new file');
  }

  // Create summary of existing references for the prompt
  const existingRefsSummary = existingReferences
    .map(ref => `- ID: ${ref.id}\n  Title: ${ref.title}\n  Quote: ${ref.quotes[0] || ''}`)
    .join('\n\n');

  // Calculate the correct relative path to references.qmd from the current file
  const fileDir = path.dirname(filePath);
  const referencesPath = path.relative(fileDir, 'brain/book/references.qmd').replace(/\\/g, '/');

  // Single LLM call to fact-check and link to existing refs OR create placeholder refs
  const factCheckPrompt = `You are an expert fact-checker and citation assistant.

**YOUR TASK:**
1. Review the CHAPTER CONTENT below for UNCITED factual claims that ABSOLUTELY NEED a source
2. Only cite claims that are:
   - Specific statistics or numbers (e.g., "$916 billion spent on military")
   - Verifiable historical facts or data points
   - Claims that readers would reasonably question without a source
3. DO NOT require sources for:
   - General statements or obvious facts
   - Author's opinions or arguments
   - Commonly known information
   - Metaphors, analogies, or hypothetical examples (e.g., "if you stacked money to the moon")
   - Mathematical calculations or conversions that are self-evident
   - Rhetorical devices or colorful language used for emphasis
   - Thought experiments or illustrations
4. **CRITICAL: DO NOT modify text that is already linked!**
   - If text already has a markdown link like [text](url), leave it completely unchanged
   - Only add links to PLAIN TEXT that needs a citation
   - Examples of text to IGNORE (leave unchanged):
     * [existing link](./problem/file.qmd)
     * [existing link](../references.qmd#some-id)
     * [existing link](https://example.com)
5. For each UNCITED claim that NEEDS a source:
   - If an existing reference in EXISTING REFERENCES supports it (even loosely), add a link: [claim](${referencesPath}#anchor-id)
   - If no suitable existing reference exists, create a new placeholder reference entry
6. Return ONLY valid JSON (no markdown code blocks):

{
  "updatedChapter": "the complete chapter text with citation links added",
  "newReferences": [
    {
      "id": "slugified-id",
      "title": "Descriptive title for the claim",
      "quotes": ["The exact claim text from the chapter"],
      "source": "<!-- TODO: Add source URL -->"
    }
  ]
}

**RULES FOR NEW PLACEHOLDER REFERENCES:**
- Create anchor ID by slugifying the claim topic (lowercase, hyphens, max 50 chars)
- Only return NEW references in the newReferences array
- Do NOT return existing references in newReferences
- If no new references needed, return empty array: "newReferences": []

**EXISTING REFERENCES (for linking only - do NOT return these):**
${existingRefsSummary}

**CHAPTER CONTENT:**
${body}`;

  try {
    const result = await genAI.models.generateContent({
      model: GEMINI_MODEL_ID,
      contents: factCheckPrompt
    });

    // Extract JSON from response
    let responseText = (result.text || '').trim();
    responseText = responseText.replace(/^```json\s*/i, '').replace(/^```\s*/i, '').replace(/\s*```$/i, '');

    const jsonMatch = responseText.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('No JSON object found in response');
    }

    const resultData = JSON.parse(jsonMatch[0]);

    if (!resultData.updatedChapter) {
      throw new Error('LLM did not return updatedChapter');
    }

    body = resultData.updatedChapter;

    // Merge new references with existing ones
    if (resultData.newReferences && resultData.newReferences.length > 0) {
      const newRefs: Reference[] = resultData.newReferences;

      // Check for duplicate IDs
      const existingIds = new Set(existingReferences.map(r => r.id));
      const dedupedNewRefs = newRefs.filter(ref => {
        if (existingIds.has(ref.id)) {
          console.warn(`⚠ Skipping duplicate reference ID: ${ref.id}`);
          return false;
        }
        return true;
      });

      if (dedupedNewRefs.length > 0) {
        // Merge and regenerate references.qmd
        const allReferences = [...existingReferences, ...dedupedNewRefs];
        const newReferencesFile = formatReferencesFile(allReferences, referencesFrontmatter);

        await fs.writeFile('brain/book/references.qmd', newReferencesFile, 'utf-8');
        console.log(`✓ Added ${dedupedNewRefs.length} new reference(s) to references.qmd`);
      }
    } else {
      console.log(`✓ All claims linked to existing references (no new references added)`);
    }

  } catch (error) {
    console.error('Fact-check failed:', error);
    console.log('Skipping fact-check for this file');
  }

  frontmatter.lastFactCheckHash = getBodyHash(matter.stringify(body, frontmatter));
  const newContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  await fs.writeFile(filePath, newContent, 'utf-8');
  console.log(`Successfully updated ${filePath}`);
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
