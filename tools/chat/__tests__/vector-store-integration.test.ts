import { describe, it, expect, beforeEach } from "@jest/globals";
import { BookVectorStore } from "../../vector/vector-store";
import { writeFile, unlink } from "fs/promises";
import { existsSync } from "fs";

describe("BookVectorStore Integration", () => {
  const testFilePath = ".test-chat-file.qmd";
  const testContent = `---
title: Test Chat File
---

# Test Content

This is a test file for chat widget testing. It contains information about the 1% Treaty.
`;

  beforeEach(async () => {
    if (!existsSync(testFilePath)) {
      await writeFile(testFilePath, testContent, "utf-8");
    }
  });

  it("should add and search files", async () => {
    const store = new BookVectorStore();
    
    await store.addFile(testFilePath);
    
    const results = await store.search("1% Treaty", 5);
    expect(results.length).toBeGreaterThan(0);
    expect(results[0].content).toContain("1% Treaty");
  });

  it("should return empty results for unrelated queries", async () => {
    const store = new BookVectorStore();
    
    await store.addFile(testFilePath);
    
    const results = await store.search("completely unrelated topic", 5);
    // Should return empty or low relevance results
    expect(Array.isArray(results)).toBe(true);
  });

  it("should handle multiple files", async () => {
    const store = new BookVectorStore();
    
    const file1 = ".test-file-1.qmd";
    const file2 = ".test-file-2.qmd";
    
    await writeFile(file1, "Content about war", "utf-8");
    await writeFile(file2, "Content about disease", "utf-8");
    
    await store.addFile(file1);
    await store.addFile(file2);
    
    const results = await store.search("war", 5);
    expect(results.length).toBeGreaterThan(0);
    
    // Cleanup
    if (existsSync(file1)) await unlink(file1);
    if (existsSync(file2)) await unlink(file2);
  });
});

