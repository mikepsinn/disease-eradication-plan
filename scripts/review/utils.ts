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

// Generic helper to update file with new body and hash
async function updateFileWithHash(
  filePath: string,
  body: string,
  frontmatter: any,
  hashFieldName: string
): Promise<void> {
  const tempContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  frontmatter[hashFieldName] = getBodyHash(tempContent);
  const newContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  await fs.writeFile(filePath, newContent, 'utf-8');
}

// Parse _quarto.yml to get chapters and appendices
export interface BookStructure {
  chapters: string[];
  appendices: string[];
}

export async function parseQuartoYml(): Promise<BookStructure> {
  const quartoYmlContent = await fs.readFile('_quarto.yml', 'utf-8');
  const chapters: string[] = [];
  const appendices: string[] = [];

  const lines = quartoYmlContent.split('\n');
  let inAppendices = false;
  let inChapters = false;

  for (const line of lines) {
    // Check if we're entering chapters section
    if (line.includes('chapters:')) {
      inChapters = true;
      inAppendices = false;
      continue;
    }

    // Check if we're entering the appendices section
    if (line.includes('appendices:')) {
      inAppendices = true;
      inChapters = false;
      continue;
    }

    // Check if we're leaving a section (new top-level key)
    if (!line.startsWith(' ') && !line.startsWith('\t') && line.includes(':') &&
        !line.includes('chapters:') && !line.includes('appendices:')) {
      inChapters = false;
      inAppendices = false;
    }

    // Extract .qmd file paths
    const match = line.match(/^\s*-\s+(brain\/[^\s]+\.qmd)/);
    if (match) {
      if (inAppendices) {
        appendices.push(match[1]);
      } else if (inChapters) {
        chapters.push(match[1]);
      }
    }
  }

  return { chapters, appendices };
}

// --- Exported Functions ---

export async function getStaleFiles(hashFieldName: string, basePath?: string): Promise<string[]> {
  const gitignoreContent = await fs.readFile('.gitignore', 'utf-8');
  const ig = ignore().add(gitignoreContent);

  const searchPattern = basePath ? `${basePath}/**/*.qmd` : '**/*.qmd';
  const allQmdFiles = glob.sync(searchPattern, { ignore: 'node_modules/**' });
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

  await updateFileWithHash(filePath, finalBody, frontmatter, 'lastFormattedHash');
  console.log(`Successfully formatted ${filePath}.`);
}

export async function styleFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nImproving style and content quality for ${filePath} with Claude Opus...`);
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(originalContent);

  const styleGuide = await fs.readFile('STYLE_GUIDE.md', 'utf-8');
  const prompt = `You are an expert copy editor reviewing a chapter of "The Complete Idiot's Guide to Ending War and Disease."

  **YOUR TASK: FIX EVERYTHING YOU CAN, ONLY ADD TODOs FOR WHAT YOU CAN'T**

  **PART A - AUTO-FIX THESE ISSUES (don't add TODOs, just fix them):**

  1. **OVERPROMISING/UNREALISTIC CLAIMS:**
     - Replace specific predictions with ranges or possibilities
     - Change "will" to "could" for uncertain outcomes
     - Add qualifiers like "potentially," "up to," or "as many as"
     - Example fixes:
       * "20-50 diseases cured" → "numerous diseases potentially cured"
       * "You might hit 150" → "lifespans could extend significantly"
       * "Your kids could see 200" → "future generations may live far longer"
       * "540 massive drug trials" → "hundreds more clinical trials"

  2. **VERBOSE/REDUNDANT CONTENT:**
     - Condense paragraphs that repeat the same point
     - Remove filler sentences
     - Combine related short paragraphs
     - Cut unnecessary adjectives and adverbs

  3. **BORING/UNENGAGING PROSE:**
     - Add dark humor where appropriate
     - Replace passive voice with active voice
     - Break up walls of text with varied sentence structure
     - Add rhetorical questions or provocative statements

  4. **STRUCTURAL ISSUES:**
     - Move buried leads to the beginning
     - Improve transitions between paragraphs
     - Group related content together
     - Ensure each section has a clear point

  5. **STYLE GUIDE ADHERENCE:**
     - Match the book's tone (dark humor, cynical but loving)
     - Keep language actionable and empowering
     - Maintain conversational, not academic tone

  **PART B - ONLY ADD TODOs FOR THESE (things you literally cannot fix):**

  ONLY add TODO comments for:
  - Missing personal anecdotes that need human experience
  - Specific data/statistics that need research
  - References to other chapters you're unsure about
  - Content gaps that need substantial new writing

  TODO format: \`<!-- TODO: NEEDS_HUMAN_INPUT - [Specific request] -->\`

  **CRITICAL INSTRUCTIONS:**
  1. FIX everything you can directly in the text
  2. ONLY add TODOs for things requiring human input/research
  3. If the content is already perfect, return "NO_CHANGES_NEEDED"
  4. Otherwise, return the full improved content
  5. Preserve markdown/Quarto syntax and frontmatter
  6. Do not include explanations outside the content

  ${styleGuide}

  **File Content to Review and Improve:**
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

  await updateFileWithHash(filePath, finalBody, frontmatter, 'lastStyleHash');
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

  // Split by anchor tags to get reference blocks
  const anchorRegex = /<a\s+id="([^"]+)"><\/a>/g;
  const blocks: Array<{ id: string; content: string }> = [];

  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = anchorRegex.exec(referencesContent)) !== null) {
    if (blocks.length > 0) {
      // Save content between previous anchor and this one
      blocks[blocks.length - 1].content = referencesContent.substring(lastIndex, match.index);
    }
    blocks.push({ id: match[1], content: '' });
    lastIndex = match.index + match[0].length;
  }

  // Get content after last anchor
  if (blocks.length > 0) {
    blocks[blocks.length - 1].content = referencesContent.substring(lastIndex);
  }

  // Parse each block
  for (const block of blocks) {
    const lines = block.content.trim().split('\n');
    if (lines.length === 0) continue;

    // Extract title from first line: - **Title**
    const titleMatch = lines[0].match(/^-\s+\*\*(.+)\*\*$/);
    if (!titleMatch) {
      console.warn(`⚠ No title found for reference ${block.id}`);
      continue;
    }

    const title = titleMatch[1];
    const quotes: string[] = [];
    let source = '';
    let currentQuote = '';

    // Parse remaining lines for quotes and source
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();

      // Skip empty lines
      if (!line) {
        // Empty line ends current quote
        if (currentQuote) {
          quotes.push(currentQuote.trim());
          currentQuote = '';
        }
        continue;
      }

      // Lines starting with > are quotes or source
      if (line.startsWith('>')) {
        const content = line.substring(1).trim();

        // Check if this is the source line (starts with —)
        if (content.startsWith('—')) {
          // Save any pending quote
          if (currentQuote) {
            quotes.push(currentQuote.trim());
            currentQuote = '';
          }
          // Extract source (remove — prefix)
          const newSource = content.substring(1).trim();
          if (source && source !== newSource) {
            source += ' | ' + newSource;
          } else if (!source) {
            source = newSource;
          }
        } else {
          // Regular quote content - accumulate multi-line quotes
          if (currentQuote) {
            currentQuote += '\n' + content;
          } else {
            currentQuote = content;
          }
        }
      } else if (currentQuote && !line.startsWith('<') && !line.startsWith('-')) {
        // Continuation line without > prefix (edge case in original file)
        // Only include if we're already in a quote and it's not HTML/markdown syntax
        currentQuote += '\n' + line;
      }
    }

    // Save any remaining quote
    if (currentQuote) {
      quotes.push(currentQuote.trim());
    }

    references.push({
      id: block.id,
      title,
      quotes,
      source: source || '<!-- TODO: Add source URL -->'
    });
  }

  // Check for duplicates
  const seenIds = new Map<string, number>();
  const uniqueRefs: Reference[] = [];

  for (const ref of references) {
    if (seenIds.has(ref.id)) {
      console.warn(`⚠ Duplicate reference ID "${ref.id}" - merging`);
      const existingIndex = seenIds.get(ref.id)!;
      const existing = uniqueRefs[existingIndex];
      // Merge quotes and sources
      existing.quotes.push(...ref.quotes);
      if (ref.source && ref.source !== existing.source) {
        existing.source += ' | ' + ref.source;
      }
    } else {
      seenIds.set(ref.id, uniqueRefs.length);
      uniqueRefs.push(ref);
    }
  }

  return uniqueRefs;
}

function formatReferencesFile(references: Reference[], frontmatter: string): string {
  // Sort by ID alphabetically
  const sorted = references.sort((a, b) => a.id.localeCompare(b.id));

  let output = frontmatter + '\n\n';

  for (const ref of sorted) {
    output += `<a id="${ref.id}"></a>\n`;
    output += `- **${ref.title}**\n`;
    for (const quote of ref.quotes) {
      // Handle multi-line quotes: split by newline and output each line with > prefix
      const quoteLines = quote.split('\n');
      for (const line of quoteLines) {
        output += `  > ${line}\n`;
      }
    }
    output += `  > — ${ref.source}\n\n`;
  }

  return output.trimEnd() + '\n';
}

export async function factCheckFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nFact-checking ${filePath} with ${GEMINI_MODEL_ID}...`);
  let originalContent = await fs.readFile(filePath, 'utf-8');
  let { data: frontmatter, content: body, orig: originalBuffer } = matter(originalContent);

  // Extract original frontmatter to preserve formatting
  const frontmatterMatch = originalContent.match(/^---\n([\s\S]*?)\n---/);
  const originalFrontmatterText = frontmatterMatch ? frontmatterMatch[0] : null;

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

  // Load book structure from _quarto.yml to know about chapters
  let bookStructure = '';
  try {
    const quartoConfig = await fs.readFile('_quarto.yml', 'utf-8');
    bookStructure = quartoConfig;
  } catch (error) {
    console.warn('Could not load _quarto.yml');
  }

  // Simplified fact-check prompt
  const factCheckPrompt = `You are a fact-checker for "The Complete Idiot's Guide to Ending War and Disease."

**TASK: Add citations ONLY to uncited external facts that need sources.**

**NEEDS CITATION (link to references.qmd):**
- Real-world statistics (e.g., "$2.44 trillion military spending")
- Published research findings
- Historical events or data

**DOES NOT NEED CITATION:**
- The book's own proposals (1% Treaty, dFDA, etc.)
- Our calculations and projections
- Hypotheticals, examples, or "what-if" scenarios
- Investor pitch assumptions
- Already-linked text (DO NOT modify existing links)
- Opinions, metaphors, common knowledge

**RULES:**
- Link each fact ONCE (first mention only)
- Be conservative - when uncertain, don't link
- Context matters - "Show investors 270% ROI" is a projection, not a fact

Return ONLY valid JSON:
{
  "updatedChapter": "complete chapter text with [citations](${referencesPath}#anchor-id) added",
  "newReferences": [
    {
      "id": "slug-id",
      "title": "Claim title",
      "quotes": ["Exact claim text"],
      "source": "<!-- TODO: Add source URL -->"
    }
  ]
}

**BOOK STRUCTURE (available chapters for TYPE B internal links):**
${bookStructure}

**EXISTING REFERENCES (for TYPE A external facts - link only, do NOT return these):**
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

  // Reconstruct file preserving original frontmatter format
  let newContent: string;
  if (originalFrontmatterText) {
    // Ensure body ends with exactly one newline
    const normalizedBody = body.trimEnd() + '\n';

    // Update only the lastFactCheckHash field in the original frontmatter
    const updatedFrontmatter = originalFrontmatterText.replace(
      /(lastFactCheckHash:\s*)[^\n]*/,
      `$1${frontmatter.lastFactCheckHash}`
    );
    // If lastFactCheckHash doesn't exist, add it before the closing ---
    if (!updatedFrontmatter.includes('lastFactCheckHash:')) {
      newContent = originalFrontmatterText.replace(
        /\n---$/,
        `\nlastFactCheckHash: ${frontmatter.lastFactCheckHash}\n---`
      ) + '\n' + normalizedBody;
    } else {
      newContent = updatedFrontmatter + '\n' + normalizedBody;
    }
  } else {
    // Fallback to gray-matter if no frontmatter found
    newContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  }

  await fs.writeFile(filePath, newContent, 'utf-8');
  console.log(`Successfully updated ${filePath}`);
}

export async function structureCheckFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nChecking structure of ${filePath} with ${GEMINI_MODEL_ID}...`);
  const originalContent = await fs.readFile(filePath, 'utf-8');
  let { data: frontmatter, content: body } = matter(originalContent);

  const outlineContent = await fs.readFile('OUTLINE.md', 'utf-8');

  // Use the reusable function to get chapters and appendices
  const { chapters, appendices } = await parseQuartoYml();

  // Check if current file is in appendix
  if (appendices.includes(filePath)) {
    console.log(`File ${filePath} is already in appendix. Skipping structure check.`);
    return; // Don't check appendix files
  }

  // Filter out current file from chapters list
  const otherChapters = chapters.filter(ch => ch !== filePath);

  const prompt = `You are an expert editor for "The Complete Idiot's Guide to Ending War and Disease."
Your task is to ensure each chapter has a single, clear focus and remove anything that dilutes it.

**CORE PRINCIPLE: Every chapter must have ONE primary purpose. Content that doesn't directly support that purpose belongs elsewhere.**

**INSTRUCTIONS:**

PART A - CHAPTER-LEVEL ANALYSIS:
1. Based on the chapter title and outline position, identify its SINGLE core purpose
2. Decide if the chapter should be:
   - KEPT (has unique, essential content appropriate for main book)
   - MERGED (overlaps with another chapter - PREFER THIS over DELETE to preserve content)
   - MOVED TO APPENDIX (too technical/detailed for main narrative but valuable as reference)
   - MOVED (belongs in a different section of main book)
   - DELETED (ONLY if completely empty or 100% redundant with NO unique insights)

3. IMPORTANT: Default to MERGE over DELETE to preserve any unique content, jokes, or insights.

4. If MERGE/MOVE/DELETE, add at the TOP:
   \`<!-- TODO: CHAPTER_CONSOLIDATION - This chapter should be [action]. REASON: [explanation] -->\`

PART B - SECTION-LEVEL ANALYSIS:
5. For each section/paragraph, ask: "Does this directly support the chapter's core purpose?"
6. Flag content that:
   - Belongs in a different chapter (MOVE, don't delete)
   - Repeats points already made (consider condensing, not deleting)
   - Adds no value (only DELETE if truly empty filler)
   - Diverges from the core message (MOVE to appropriate chapter)

7. Add TODO above problematic sections:
   \`<!-- TODO: STRUCTURE_CHECK - [MOVE to 'chapter.qmd'/CONDENSE/DELETE only if truly empty]. REASON: [why] -->\`

**GENERAL PRINCIPLES:**
- Problem chapters shouldn't contain solutions
- Solution chapters shouldn't restate problems at length
- Each chapter should make a distinct contribution
- Be aggressive about cutting redundancy and tangents

**OUTPUT RULES:**
- If perfectly focused with no issues: return ONLY the string "NO_CHANGES_NEEDED"
- Otherwise: return THE ENTIRE CHAPTER TEXT with TODO comments inserted at appropriate locations
- CRITICAL: You must return ALL the original content, just with TODO comments added where needed
- Never delete or remove any existing text - only ADD TODO comments
- Don't modify the actual prose/text content

---
**BOOK OUTLINE:**
${outlineContent}
---
**OTHER CHAPTERS IN THE BOOK (for reference):**
${otherChapters.join('\n')}
---
**CHAPTER BEING EVALUATED:** ${filePath}
${body}`;

  const result = await genAI.models.generateContent({
    model: GEMINI_MODEL_ID,
    contents: prompt
  });
  const responseText = result.text || '';

  let finalBody;
  if (responseText.trim() === 'NO_CHANGES_NEEDED') {
    console.log(`File ${filePath} is already structured correctly. Updating metadata.`);
    finalBody = body; // Use the original body
  } else {
    finalBody = responseText.trim();
  }

  await updateFileWithHash(filePath, finalBody, frontmatter, 'lastStructureCheckHash');
  console.log(`Successfully checked structure for ${filePath}.`);
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

  await updateFileWithHash(filePath, body, frontmatter, 'lastLinkCheckHash');
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

  await updateFileWithHash(filePath, body, frontmatter, 'lastFigureCheckHash');
  console.log(`Successfully updated figure-check metadata for ${filePath}.`);
}

async function mergeContentWithLLM(archivedContent: string, targetFilePath: string): Promise<string> {
  console.log(`Intelligently merging content into ${targetFilePath}...`);
  const targetContent = await fs.readFile(targetFilePath, 'utf-8');

  const { content: archivedBody } = matter(archivedContent);
  const { data: targetFrontmatter, content: targetBody } = matter(targetContent);

  const prompt = `You are an expert editor for "The Complete Idiot's Guide to Ending War and Disease." Your task is to surgically merge the "Archived File" content into the "Existing Chapter," adopting the chapter's distinct, cynical, and humorous tone.

**CORE OBJECTIVE: The final output should read as if a single, slightly unhinged author wrote it, not like two documents stapled together.**

**MERGE INSTRUCTIONS:**

1.  **Prioritize the Existing Chapter's Voice:** The tone of the "Existing Chapter" is paramount. It's dark, funny, and sarcastic. **Rewrite all content from the archived file to match this voice.** Do not just copy-paste.
2.  **Integrate, Don't Append:** Weave the data, images, and core concepts from the archived file into the existing narrative. Find the most logical places for them. If the existing chapter has a section on a topic, enhance it with the archived info. Don't just add new, disconnected sections at the end.
3.  **Eliminate All Redundancy:** The archived file and the chapter may cover similar ground. Aggressively condense and combine them. Keep the best jokes, the clearest data, and the most impactful statements from both.
4.  **Maintain Narrative Flow:** The final chapter must be a cohesive story. Ensure smooth transitions between integrated sections. The reader should not be able to tell where the merge happened.
5.  **Return Only the Final, Merged Content:** Your output must be the complete, final text of the merged chapter body. Do not include frontmatter, explanations, or any text outside the chapter content itself.

---
**Existing Chapter Content (${targetFilePath}):**
\`\`\`markdown
${targetBody}
\`\`\`
---
**Archived File Content to Merge:**
\`\`\`markdown
${archivedBody}
\`\`\`
---

Return only the final, merged markdown content.
`;

  const result = await genAI.models.generateContent({
    model: GEMINI_MODEL_ID,
    contents: prompt,
  });

  const mergedBody = result.text || '';
  
  // Re-apply the original frontmatter of the target file
  const finalContent = matter.stringify(mergedBody, targetFrontmatter);

  return finalContent;
}

export async function analyzeArchivedFile(filePath: string): Promise<void> {
  console.log(`Analyzing archived file: ${filePath}`);
  const archivedContent = await fs.readFile(filePath, 'utf-8');
  const quartoYmlContent = await fs.readFile('_quarto.yml', 'utf-8');

  const prompt = `You are an expert editor tasked with organizing a book manuscript.
You need to decide what to do with an archived markdown file.
Based on the book's structure from \`_quarto.yml\` and the content of the archived file, determine one of the following actions:

1.  **MERGE**: The content is valuable and should be merged into an existing chapter.
2.  **CREATE**: The content is valuable and unique enough to become a new chapter.
3.  **DELETE**: The content is redundant, irrelevant, or low-quality and should be deleted.

**RESPONSE FORMAT:**

You MUST respond with a JSON object with the following structure:

\`\`\`json
{
  "action": "MERGE" | "CREATE" | "DELETE",
  "reason": "A brief explanation for your decision.",
  "targetFile": "path/to/target/chapter.qmd", // (Required for MERGE)
  "newFileName": "new-chapter-name.qmd", // (Required for CREATE)
  "newFileContent": "The full content for the new chapter, including frontmatter." // (Required for CREATE)
}
\`\`\`

---
**Book Structure (_quarto.yml):**
\`\`\`yaml
${quartoYmlContent}
\`\`\`
---
**Archived File Content (${filePath}):**
\`\`\`markdown
${archivedContent}
\`\`\`
`;

  const result = await genAI.models.generateContent({
    model: GEMINI_MODEL_ID,
    contents: prompt,
  });

  let responseText = (result.text || '').trim();
  // Clean up potential markdown code fences
  responseText = responseText.replace(/^```json\s*/i, '').replace(/\s*```$/i, '');

  const jsonMatch = responseText.match(/\{[\s\S]*\}/);
  if (!jsonMatch) {
    throw new Error(`No JSON object found in LLM response. Response text: ${responseText}`);
  }

  const response = JSON.parse(jsonMatch[0]);

  switch (response.action) {
    case 'MERGE':
      if (!response.targetFile) {
        throw new Error('Invalid MERGE action: targetFile is required.');
      }
      console.log(`Decision: MERGE into ${response.targetFile}. Reason: ${response.reason}`);
      const finalContent = await mergeContentWithLLM(archivedContent, response.targetFile);
      await fs.writeFile(response.targetFile, finalContent, 'utf-8');
      await fs.unlink(filePath); // Delete the archived file
      console.log(`Successfully merged content into ${response.targetFile} and deleted archived file.`);
      break;

    case 'CREATE':
      if (!response.newFileName || !response.newFileContent) {
        throw new Error('Invalid CREATE action: newFileName and newFileContent are required.');
      }
      const newFilePath = path.join('brain/book', response.newFileName);
      console.log(`Decision: CREATE new file ${newFilePath}. Reason: ${response.reason}`);
      await fs.writeFile(newFilePath, response.newFileContent, 'utf-8');
      // Here you would also need to update _quarto.yml to include the new chapter.
      // This is a complex operation and for now we will just create the file.
      console.log(`TODO: Manually add ${newFilePath} to _quarto.yml`);
      await fs.unlink(filePath); // Delete the archived file
      console.log(`Successfully created ${newFilePath} and deleted archived file.`);
      break;

    case 'DELETE':
      console.log(`Decision: DELETE file. Reason: ${response.reason}`);
      await fs.unlink(filePath);
      console.log(`Successfully deleted archived file.`);
      break;

    default:
      throw new Error(`Unknown action: ${response.action}`);
  }
}
