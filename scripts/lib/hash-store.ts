/**
 * Centralized hash storage for tracking file processing state
 * Stores hashes in a single JSON file instead of in each file's frontmatter
 */

import fs from 'fs/promises';
import * as fsSync from 'fs';
import path from 'path';
import { getProjectRoot } from './file-utils';
import { getAllHashFields, type HashFieldName } from './constants';

const HASH_STORE_FILE = path.join(getProjectRoot(), '.file-hashes.json');

/**
 * Hash store structure: { [filePath]: { [hashField]: hashValue } }
 */
interface HashStore {
  [filePath: string]: {
    [hashField: string]: string;
  };
}

/**
 * Read the hash store from disk
 */
async function readHashStore(): Promise<HashStore> {
  try {
    const content = await fs.readFile(HASH_STORE_FILE, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    // File doesn't exist or is invalid - return empty store
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
      return {};
    }
    console.warn(`Warning: Could not read hash store: ${error}`);
    return {};
  }
}

/**
 * Write the hash store to disk
 */
async function writeHashStore(store: HashStore): Promise<void> {
  const dir = path.dirname(HASH_STORE_FILE);
  await fs.mkdir(dir, { recursive: true });
  await fs.writeFile(HASH_STORE_FILE, JSON.stringify(store, null, 2), 'utf-8');
}

/**
 * Normalize file path for consistent storage
 * Converts to relative path from project root
 */
function normalizeFilePath(filePath: string): string {
  const root = getProjectRoot();
  const absolutePath = path.isAbsolute(filePath) 
    ? filePath 
    : path.resolve(root, filePath);
  return path.relative(root, absolutePath).replace(/\\/g, '/');
}

/**
 * Get hash for a specific file and hash field
 */
export async function getFileHash(
  filePath: string,
  hashField: HashFieldName
): Promise<string | undefined> {
  const store = await readHashStore();
  const normalizedPath = normalizeFilePath(filePath);
  return store[normalizedPath]?.[hashField];
}

/**
 * Set hash for a specific file and hash field
 */
export async function setFileHash(
  filePath: string,
  hashField: HashFieldName,
  hashValue: string
): Promise<void> {
  const store = await readHashStore();
  const normalizedPath = normalizeFilePath(filePath);
  
  if (!store[normalizedPath]) {
    store[normalizedPath] = {};
  }
  
  store[normalizedPath][hashField] = hashValue;
  await writeHashStore(store);
}

/**
 * Get all hashes for a specific file
 */
export async function getFileHashes(filePath: string): Promise<Record<string, string> | undefined> {
  const store = await readHashStore();
  const normalizedPath = normalizeFilePath(filePath);
  return store[normalizedPath];
}

/**
 * Remove hash for a specific file and hash field
 */
export async function removeFileHash(
  filePath: string,
  hashField: HashFieldName
): Promise<void> {
  const store = await readHashStore();
  const normalizedPath = normalizeFilePath(filePath);
  
  if (store[normalizedPath]) {
    delete store[normalizedPath][hashField];
    
    // If no hashes left for this file, remove the file entry
    if (Object.keys(store[normalizedPath]).length === 0) {
      delete store[normalizedPath];
    }
    
    await writeHashStore(store);
  }
}

/**
 * Remove all hashes for a specific file
 */
export async function removeAllFileHashes(filePath: string): Promise<void> {
  const store = await readHashStore();
  const normalizedPath = normalizeFilePath(filePath);
  
  if (store[normalizedPath]) {
    delete store[normalizedPath];
    await writeHashStore(store);
  }
}

/**
 * Check if a file has a specific hash field set
 */
export async function hasFileHash(
  filePath: string,
  hashField: HashFieldName
): Promise<boolean> {
  const hash = await getFileHash(filePath, hashField);
  return hash !== undefined && hash !== null;
}

/**
 * Migrate hashes from frontmatter to hash store
 * This is a one-time migration function
 */
export async function migrateHashesFromFrontmatter(
  filePath: string,
  frontmatter: any
): Promise<void> {
  const hashFields = getAllHashFields();
  let migrated = false;
  
  for (const hashField of hashFields) {
    if (frontmatter[hashField]) {
      await setFileHash(filePath, hashField as HashFieldName, frontmatter[hashField]);
      migrated = true;
    }
  }
  
  return;
}

/**
 * Get the path to the hash store file
 */
export function getHashStorePath(): string {
  return HASH_STORE_FILE;
}

