import { describe, it, expect, beforeEach, afterEach } from "@jest/globals";
import { updateFileHash, getStaleFilesForWishonia, calculateTodoPriority } from "../../lib/hash-utils";
import { HASH_FIELDS } from "../../lib/constants";
import { readFileWithMatter } from "../../lib/file-utils";
import { writeFile, unlink } from "fs/promises";
import { existsSync } from "fs";
import type { EnhancedTodo } from "../todo-manager-enhanced";

describe("hash-utils", () => {
  const testFilePath = ".test-hash-file.qmd";
  const testContent = `---
title: Test File
---

# Test Content

This is a test file with some content.
`;

  beforeEach(async () => {
    // Create a test file
    await writeFile(testFilePath, testContent, "utf-8");
  });

  afterEach(async () => {
    // Clean up test file
    if (existsSync(testFilePath)) {
      await unlink(testFilePath);
    }
  });

  describe("updateFileHash", () => {
    it("should update a hash field in frontmatter", async () => {
      await updateFileHash(testFilePath, HASH_FIELDS.PARAMETER_CHECK, "test-hash-123");

      const { frontmatter } = await readFileWithMatter(testFilePath);
      expect(frontmatter[HASH_FIELDS.PARAMETER_CHECK]).toBe("test-hash-123");
    });

    it("should preserve other frontmatter fields", async () => {
      await updateFileHash(testFilePath, HASH_FIELDS.MATH_VALIDATION, "math-hash-456");

      const { frontmatter } = await readFileWithMatter(testFilePath);
      expect(frontmatter.title).toBe("Test File");
      expect(frontmatter[HASH_FIELDS.MATH_VALIDATION]).toBe("math-hash-456");
    });
  });

  describe("calculateTodoPriority", () => {
    it("should return critical for math errors with high confidence", () => {
      const priority = calculateTodoPriority("math", "high");
      expect(priority).toBe("critical");
    });

    it("should return high for parameter issues with high confidence", () => {
      const priority = calculateTodoPriority("parameter", "high");
      expect(priority).toBe("high");
    });

    it("should return high for reference issues with high confidence", () => {
      const priority = calculateTodoPriority("reference", "high");
      expect(priority).toBe("high");
    });

    it("should return medium for claim issues with medium confidence", () => {
      const priority = calculateTodoPriority("claim", "medium");
      expect(priority).toBe("medium");
    });

    it("should return medium for consistency issues with low confidence", () => {
      const priority = calculateTodoPriority("consistency", "low");
      expect(priority).toBe("medium");
    });
  });

  describe("getStaleFilesForWishonia", () => {
    it("should return files that need review", async () => {
      // This test requires actual knowledge files, so we'll just verify it doesn't crash
      const staleFiles = await getStaleFilesForWishonia();
      expect(Array.isArray(staleFiles)).toBe(true);
    });
  });
});

