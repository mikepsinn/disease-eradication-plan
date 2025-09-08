import { glob } from 'glob';
import * as fs from 'fs/promises';
import * as path from 'path';
import matter from 'gray-matter';
import { execSync } from 'child_process';
import { AnalysisPlan } from '../workflows/maintenance';

export interface RepositoryIndex {
  [filePath: string]: {
    title: string;
    description: string;
    tags: string[];
    lastModified: string;
    lastReviewed: string;
  };
}

const CACHE_DIR = '.voltagent';
const CACHE_FILE = path.join(CACHE_DIR, 'repository-index-cache.json');

/**
 * Gets the last git modification date for a file.
 */
function getGitLastModified(filePath: string): string {
  try {
    const command = `git log -1 --format=%cI -- "${filePath}"`;
    const date = execSync(command).toString().trim();
    return date || new Date(0).toISOString();
  } catch (error) {
    console.error(`Error getting last modified date for ${filePath}:`, error);
    return new Date(0).toISOString();
  }
}

/**
 * Generates and caches a JSON index of all markdown files in the repository.
 */
export async function generateRepositoryIndex(): Promise<{ index: RepositoryIndex }> {
  console.log('[Indexer] Generating repository index...');
  const files = await glob('**/*.md', { ignore: ['node_modules/**', 'agent/src/tools/tests/mock-repo/**'] });
  const index: RepositoryIndex = {};

  for (const file of files) {
    try {
      const content = await fs.readFile(file, 'utf-8');
      const { data } = matter(content);

      const lastModified = getGitLastModified(file);
      const lastReviewed = data.lastReviewed || new Date(0).toISOString();

      index[file] = {
        title: data.title || 'No Title',
        description: data.description || 'No Description',
        tags: data.tags || [],
        lastModified,
        lastReviewed,
      };
    } catch (error) {
      console.error(`Error processing file ${file}:`, error);
    }
  }

  // Ensure cache directory exists and save the index
  await fs.mkdir(CACHE_DIR, { recursive: true });
  await fs.writeFile(CACHE_FILE, JSON.stringify(index, null, 2));

  console.log(`[Indexer] Successfully generated and cached index for ${Object.keys(index).length} files.`);
  return { index };
}

/**
 * Finds the next file that needs to be reviewed and passes the index along.
 */
export async function findNextFileToReview(input: { index: RepositoryIndex }): Promise<{ index: RepositoryIndex; filePath: string | null }> {
    const { index } = input;
    console.log('[Finder] Searching for the next file to review...');
    for (const [filePath, metadata] of Object.entries(index)) {
      const lastModified = new Date(metadata.lastModified);
      const lastReviewed = new Date(metadata.lastReviewed);
      if (lastModified > lastReviewed) {
        console.log(`[Finder] Found file to review: ${filePath}`);
        return { index, filePath };
      }
    }
    console.log('[Finder] No files need reviewing at this time.');
    return { index, filePath: null };
}

/**
 * Prepares the full context needed for the agent analysis step.
 */
export async function prepareAgentContext(input: { index: RepositoryIndex; filePath: string | null }): Promise<{ fileContent: string; filePath: string; index: RepositoryIndex } | null> {
  const { index, filePath } = input;
  if (!filePath) {
    console.log('[Preprocessor] No file to review. Halting workflow.');
    // Returning null will gracefully stop the workflow if no file is found
    return null;
  }
  console.log(`[Preprocessor] Reading file content for: ${filePath}`);
  const fileContent = await fs.readFile(filePath, 'utf-8');
  return { fileContent, filePath, index };
}


/**
 * Executes the plan provided by the agent.
 */
export async function executePlan(plan: AnalysisPlan | null): Promise<{ status: string; message: string }> {
  if (!plan) {
    return { status: 'Skipped', message: 'No plan to execute.' };
  }
  console.log(`[Executor] Executing plan for decision: ${plan.decision}`);
  try {
    switch (plan.decision) {
      case 'DELETE':
        for (const filePath of plan.targetFiles) {
          await fs.unlink(filePath);
          console.log(`[Executor] Deleted file: ${filePath}`);
        }
        return { status: 'Success', message: `Deleted files: ${plan.targetFiles.join(', ')}` };

      // TODO: Implement other cases like CONSOLIDATE, REWRITE, CREATE_ISSUE

      case 'NO_ACTION':
        console.log('[Executor] No action taken.');
        return { status: 'Success', message: 'No action was required.' };

      default:
        return { status: 'Failed', message: `Decision "${plan.decision}" is not yet implemented.` };
    }
  } catch (error: any) {
    console.error('[Executor] Error executing plan:', error);
    return { status: 'Failed', message: `Error: ${error.message}` };
  }
}
