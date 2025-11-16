import { describe, it, expect, beforeEach } from "@jest/globals";
import { BookVectorStore } from "../vector-store";
import { writeFile, unlink } from "fs/promises";
import { existsSync } from "fs";

describe("BookVectorStore", () => {
  const testFilePath = ".test-vector-file.qmd";
  const testContent = `---
title: Test Vector File
---

# Test Content

This is a test file for vector store testing.
`;

  beforeEach(async () => {
    // Create a test file
    if (!existsSync(testFilePath)) {
      await writeFile(testFilePath, testContent, "utf-8");
    }
  });

  it("should create a vector store instance", () => {
    const store = new BookVectorStore();
    expect(store).toBeDefined();
  });

  it("should add a file to the vector store", async () => {
    const store = new BookVectorStore();
    await expect(store.addFile(testFilePath)).resolves.not.toThrow();
  });

  it("should search for content", async () => {
    const store = new BookVectorStore();
    await store.addFile(testFilePath);
    
    const results = await store.search("test content", 5);
    expect(Array.isArray(results)).toBe(true);
  });

  it("should get all files", async () => {
    const store = new BookVectorStore();
    await store.addFile(testFilePath);
    
    const files = await store.getAllFiles();
    expect(Array.isArray(files)).toBe(true);
  });
});

