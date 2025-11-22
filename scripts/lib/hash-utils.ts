import { readFileWithMatter, getBodyHash, stringifyWithFrontmatter, saveFile } from "./file-utils";
import { HASH_FIELDS, type HashFieldName } from "./constants";
import { setFileHash, getFileHash } from "./hash-store";
import type { EnhancedTodo } from "../agents/todo-manager-enhanced";

/**
 * Update a file's hash field without changing content
 * Hash is stored in centralized hash store, not in frontmatter
 */
export async function updateFileHash(
  filePath: string,
  hashField: HashFieldName,
  newHash: string
): Promise<void> {
  // Store hash in centralized hash store instead of frontmatter
  await setFileHash(filePath, hashField, newHash);
}

/**
 * Get all files that need WISHONIA review
 * Checks all WISHONIA-specific hash fields
 * Reads hashes from centralized hash store instead of frontmatter
 */
export async function getStaleFilesForWishonia(): Promise<string[]> {
  const { glob } = await import("glob");
  // Check both knowledge/ and brain/book/ directories
  const knowledgeFiles = await glob("knowledge/**/*.qmd", {
    ignore: ["**/node_modules/**", "**/_book/**", "**/_freeze/**"],
  });
  const bookFiles = await glob("brain/book/**/*.qmd", {
    ignore: ["**/node_modules/**", "**/_book/**", "**/_freeze/**", "**/references.qmd"],
  });
  const files = [...knowledgeFiles, ...bookFiles];

  const staleFiles: string[] = [];

  for (const file of files) {
    try {
      const { body } = await readFileWithMatter(file);
      const currentHash = getBodyHash(body);

      // Check if any WISHONIA hash field is missing or outdated
      const wishoniaHashFields: HashFieldName[] = [
        HASH_FIELDS.PARAMETER_CHECK,
        HASH_FIELDS.MATH_VALIDATION,
        HASH_FIELDS.CLAIM_VALIDATION,
        HASH_FIELDS.REFERENCE_LINKING,
        HASH_FIELDS.CONSISTENCY_CHECK,
      ];

      // Wait for all checks to complete
      const needsReviewResult = await Promise.all(
        wishoniaHashFields.map(async (field) => {
          const storedHash = await getFileHash(file, field);
          return !storedHash || storedHash !== currentHash;
        })
      );

      if (needsReviewResult.some(result => result)) {
        staleFiles.push(file);
      }
    } catch (error) {
      console.error(`Error checking file ${file}:`, error);
    }
  }

  return staleFiles;
}

/**
 * Calculate priority for a todo based on issue type and confidence
 */
export function calculateTodoPriority(
  type: EnhancedTodo["type"],
  confidence: EnhancedTodo["confidence"]
): EnhancedTodo["priority"] {
  // Critical: Math errors with high confidence
  if (type === "math" && confidence === "high") {
    return "critical";
  }

  // High: Parameter issues, reference issues, or any high confidence issues
  if (
    (type === "parameter" || type === "reference") &&
    confidence === "high"
  ) {
    return "high";
  }

  // High: Any critical type with medium confidence
  if ((type === "math" || type === "parameter") && confidence === "medium") {
    return "high";
  }

  // Medium: Claim validation or consistency issues
  if (type === "claim" || type === "consistency") {
    return confidence === "high" ? "high" : "medium";
  }

  // Default to medium for other cases
  return "medium";
}

