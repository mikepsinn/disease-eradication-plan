#!/usr/bin/env tsx
/**
 * Update embeddings for changed files
 * This script should be run before git commit to update vector store
 */

import { BookVectorStore } from "./vector-store";
import { getStaleFilesForWishonia } from "../lib/hash-utils";
import { getBookContentFiles } from "../lib/file-utils";
import { readFileWithMatter, getBodyHash } from "../lib/file-utils";
import { HASH_FIELDS } from "../lib/constants";
import { glob } from "glob";
import { createPinoLogger } from "@voltagent/logger";

const logger = createPinoLogger({
  name: "update-embeddings",
  level: "info",
});

/**
 * Hash field to track when embeddings were last updated
 */
const EMBEDDING_HASH_FIELD = "lastEmbeddingHash";

/**
 * Update embeddings for all changed files
 */
async function updateEmbeddingsForChangedFiles() {
  const vectorStore = new BookVectorStore();
  
  // Get all book files
  const allFiles = await getBookContentFiles({
    includeAppendix: true,
    includeReferences: false,
  });

  logger.info(`Found ${allFiles.length} files to check`);

  let updated = 0;
  let skipped = 0;

  for (const file of allFiles) {
    try {
      const { body, frontmatter } = await readFileWithMatter(file);
      const currentHash = getBodyHash(body);
      const lastEmbeddingHash = frontmatter[EMBEDDING_HASH_FIELD];

      // Check if file needs embedding update
      if (currentHash !== lastEmbeddingHash) {
        logger.info(`Updating embeddings for: ${file}`);
        await vectorStore.updateFile(file);
        updated++;
      } else {
        skipped++;
      }
    } catch (error) {
      logger.error(`Error processing ${file}:`, error);
    }
  }

  logger.info(`✅ Updated ${updated} files, skipped ${skipped} files`);
}

/**
 * Update embeddings for all files (full refresh)
 */
async function updateAllEmbeddings() {
  const vectorStore = new BookVectorStore();
  
  const allFiles = await getBookContentFiles({
    includeAppendix: true,
    includeReferences: false,
  });

  logger.info(`Updating embeddings for ${allFiles.length} files...`);

  for (const file of allFiles) {
    try {
      logger.info(`Processing: ${file}`);
      await vectorStore.addFile(file);
    } catch (error) {
      logger.error(`Error processing ${file}:`, error);
    }
  }

  logger.info(`✅ Updated embeddings for ${allFiles.length} files`);
}

// Main execution
async function main() {
  const args = process.argv.slice(2);
  const fullRefresh = args.includes("--full");

  if (fullRefresh) {
    await updateAllEmbeddings();
  } else {
    await updateEmbeddingsForChangedFiles();
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    logger.error("Error:", error);
    process.exit(1);
  });
}

