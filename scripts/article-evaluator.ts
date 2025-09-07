import { z } from 'zod';
import { streamObject } from 'ai';
import { createOpenAI } from '@ai-sdk/openai';
import { createAnthropic } from '@ai-sdk/anthropic';
import { createPerplexity } from '@ai-sdk/perplexity';
import { google } from '@ai-sdk/google';
import { deepseek } from '@ai-sdk/deepseek';
import { env, AvailableModel } from './env';
import * as fs from 'fs';
import * as path from 'path';
import * as crypto from 'crypto';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

// Define the schema for article assessment
const ArticleAssessmentSchema = z.object({
  qualityScore: z.number()
    .min(0)
    .max(100)
    .describe('Quality score between 0-100'),
  improvements: z.array(z.string())
    .describe('List of specific improvements needed'),
  recommendations: z.object({
    shouldDelete: z.boolean()
      .describe('Whether the article should be deleted'),
    shouldRename: z.string()
      .optional()
      .describe('New suggested name if rename is recommended'),
    shouldMoveTo: z.string()
      .optional()
      .describe('New suggested directory path if move is recommended'),
    priority: z.number()
      .min(1)
      .max(5)
      .describe('Priority level for addressing this content (1-5)')
  }),
  todos: z.array(z.string())
    .optional()
    .describe('A list of actionable TODO comments to add to the file, formatted as "<!-- TODO: [description] -->"')
});

export type ArticleAssessment = z.infer<typeof ArticleAssessmentSchema>;

// --- Caching Logic ---
const CACHE_FILE = path.join(__dirname, '..', '.article-cache.json');
type ArticleCache = {
  [filePath: string]: {
    hash: string;
    assessment: ArticleAssessment;
  };
};

function readCache(): ArticleCache {
  if (fs.existsSync(CACHE_FILE)) {
    const data = fs.readFileSync(CACHE_FILE, 'utf-8');
    return JSON.parse(data);
  }
  return {};
}

function writeCache(cache: ArticleCache) {
  fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2));
}

function calculateHash(content: string): string {
  return crypto.createHash('sha256').update(content).digest('hex');
}


// Initialize providers
const openai = createOpenAI({
  apiKey: env.OPENAI_API_KEY || ''
});

const anthropic = createAnthropic({
  apiKey: env.ANTHROPIC_API_KEY || ''
});

const perplexity = createPerplexity({
  apiKey: env.PERPLEXITY_API_KEY || ''
});

// Configure AI providers
const providers: Record<AvailableModel, () => any> = {
  // OpenAI models
  'gpt-4-turbo': () => openai('gpt-4-turbo'),
  'gpt-4': () => openai('gpt-4'),
  'gpt-3.5-turbo': () => openai('gpt-3.5-turbo'),
  // Anthropic models
  'claude-3-opus': () => anthropic('claude-3-opus'),
  'claude-3-sonnet': () => anthropic('claude-3-sonnet'),
  'anthropic/claude-3-opus': () => anthropic('claude-3-opus'),
  'anthropic/claude-3-sonnet': () => anthropic('claude-3-sonnet'),
  // Perplexity models
  'sonar-small-chat': () => perplexity('sonar-small-chat'),
  'sonar-medium-chat': () => perplexity('sonar-medium-chat'),
  'sonar-large-chat': () => perplexity('sonar-large-chat'),
  // Google Gemini models
  'gemini-2.5-flash': () => google('models/gemini-2.5-flash'),
  'gemini-2.5-pro': () => google('models/gemini-2.5-pro'),
  // DeepSeek models
  'deepseek-chat': () => deepseek('deepseek-chat'),
  'deepseek-reasoner': () => deepseek('deepseek-reasoner')
};

const rulePath = path.join(__dirname, '..', 'CONTRIBUTING.md');
const SYSTEM_PROMPT = fs.readFileSync(rulePath, 'utf-8');

export async function evaluateArticle(content: string, filePath: string): Promise<ArticleAssessment> {
  try {
    const modelName = env.AI_MODEL;
    const provider = providers[modelName];
    
    if (!provider) {
      throw new Error(`Unsupported model: ${modelName}`);
    }

    const result = streamObject({
      model: provider(),
      schema: ArticleAssessmentSchema,
      system: SYSTEM_PROMPT,
      prompt: `Analyze this content from the file at the following path: ${filePath}:\n\n---\n\n${content}`,
      onFinish({ object, error, usage }) {
        if (error) {
          console.error(`Error evaluating ${filePath}:`, error);
        } else {
          console.log(`Evaluated ${filePath} (${usage?.totalTokens} tokens used)`);
        }
      }
    });

    // Wait for the final object
    const assessment = await result.object;
    return assessment;

  } catch (error) {
    console.error(`Error evaluating article ${filePath}:`, error);
    return {
      qualityScore: 0,
      improvements: ['Error analyzing content'],
      recommendations: {
        shouldDelete: false,
        priority: 1
      }
    };
  }
} 

// --- Orchestrator Logic ---

const ROOT_DIR = path.resolve(__dirname, '..');
const OUTPUT_FILE = path.join(ROOT_DIR, 'operations', 'refactor-manifest.ai.md');
const IGNORE_PATTERNS = ['.git', '.cursor', 'node_modules', 'scripts', 'brand', 'operations', '.article-cache.json'];

async function findMarkdownFiles(dir: string): Promise<string[]> {
    let mdFiles: string[] = [];
    const entries = await fs.promises.readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (IGNORE_PATTERNS.some(p => fullPath.includes(path.sep + p + path.sep) || fullPath.endsWith(path.sep + p))) {
            continue;
        }

        if (entry.isDirectory()) {
            mdFiles = mdFiles.concat(await findMarkdownFiles(fullPath));
        } else if (entry.isFile() && entry.name.endsWith('.md')) {
            mdFiles.push(fullPath);
        }
    }
    return mdFiles;
}

function formatAction(filePath: string, assessment: ArticleAssessment): string {
    const relativePath = './' + path.relative(ROOT_DIR, filePath).replace(/\\/g, '/');
    const { recommendations } = assessment;

    if (recommendations.shouldDelete) {
        return `- [ ] DELETE ${relativePath}`;
    }

    if (recommendations.shouldMoveTo) {
        const newPath = path.join(recommendations.shouldMoveTo, path.basename(filePath)).replace(/\\/g, '/');
        return `- [ ] MOVE ${relativePath} ./${newPath}`;
    }

    if (recommendations.shouldRename) {
        const newPath = path.join(path.dirname(relativePath), recommendations.shouldRename).replace(/\\/g, '/');
        return `- [ ] RENAME ${relativePath} ${newPath}`;
    }

    return `- [ ] KEEP ${relativePath}`;
}

function getManifestHeader(): string {
  return `---
title: "AI-Generated Refactor Manifest"
description: "A master list of all files and directories for the wiki refactoring, generated by an AI agent based on the project's architectural guidelines. Curate this list to define the final action for each item."
---

# AI-Generated Refactor Manifest

This manifest was generated by an AI agent. Review and approve each line before executing the refactor.
Valid actions are: **KEEP**, **MOVE**, **RENAME**, **DELETE**.

---

`;
}

async function main() {
    const argv = await yargs(hideBin(process.argv))
        .option('limit', {
            alias: 'l',
            type: 'number',
            description: 'Limit the number of new or modified files to analyze',
            default: -1, // -1 means no limit
        })
        .help()
        .argv;

    console.log('Starting AI-powered refactor analysis...');
    
    const cache = readCache();
    const allMarkdownFiles = await findMarkdownFiles(ROOT_DIR);
    
    let filesToProcess: { filePath: string; content: string }[] = [];
    let manifestLines = [getManifestHeader()];
    let processedCount = 0;

    // First pass: identify changed files and populate manifest from cache for unchanged files
    for (const filePath of allMarkdownFiles) {
        try {
            const content = await fs.promises.readFile(filePath, 'utf-8');
            if (!content.trim()) {
                console.log(`Skipping empty file: ${path.relative(ROOT_DIR, filePath)}`);
                continue;
            }
            const hash = calculateHash(content);
            const cached = cache[filePath];

            if (cached && cached.hash === hash) {
                // File is unchanged, use cached assessment for manifest
                manifestLines.push(formatAction(filePath, cached.assessment));
            } else {
                // File is new or modified, add to processing queue
                filesToProcess.push({ filePath, content });
            }
        } catch (error) {
            console.error(`Error reading file ${filePath}:`, error);
        }
    }
    
    console.log(`Found ${allMarkdownFiles.length} total markdown files.`);
    console.log(`${filesToProcess.length} files are new or have been modified and require analysis.`);

    const limit = argv.limit > -1 ? argv.limit : filesToProcess.length;
    if(argv.limit > -1) {
        console.log(`Processing up to ${limit} files due to --limit flag.`);
    }

    const filesForThisRun = filesToProcess.slice(0, limit);

    const concurrencyLimit = 5;
    const promises = [];

    for (const { filePath, content } of filesForThisRun) {
        const promise = (async () => {
            try {
                console.log(`Evaluating: ${path.relative(ROOT_DIR, filePath)}`);
                const assessment = await evaluateArticle(content, filePath);
                
                if (assessment) {
                    const hash = calculateHash(content);
                    cache[filePath] = { hash, assessment }; // Update cache
                    manifestLines.push(formatAction(filePath, assessment));
                    
                    const todos = assessment.todos;
                    if (todos && Array.isArray(todos) && todos.length > 0) {
                        console.log(`  -> Adding ${todos.length} TODOs to ${path.basename(filePath)}`);
                        await fs.promises.appendFile(filePath, '\n\n' + todos.join('\n') + '\n');
                    }
                }
            } catch (error) {
                console.error(`Error processing file ${filePath}:`, error);
            }
        })();
        promises.push(promise);

        if (promises.length >= concurrencyLimit) {
            await Promise.all(promises);
            promises.length = 0;
        }
    }

    await Promise.all(promises);
    
    writeCache(cache); // Save the updated cache
    console.log("Cache updated.");

    const sortedActions = manifestLines.slice(1).sort();
    const finalManifest = manifestLines[0] + sortedActions.join('\n');

    await fs.promises.writeFile(OUTPUT_FILE, finalManifest);
    console.log(`\nAI-generated refactor manifest created at: ${OUTPUT_FILE}`);
}

// Make the script executable
if (require.main === module) {
    main().catch(console.error);
} 