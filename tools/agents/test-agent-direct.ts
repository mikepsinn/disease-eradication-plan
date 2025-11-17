#!/usr/bin/env tsx
/**
 * Test the supervisor agent directly to verify it works
 */

import "dotenv/config";
import { Agent, Memory } from "@voltagent/core";
import { google } from "@ai-sdk/google";
import {
  AiSdkEmbeddingAdapter,
  InMemoryVectorAdapter,
} from "@voltagent/core";
import { LibSQLMemoryAdapter } from "@voltagent/libsql";
import { readFile } from "fs/promises";

// Create shared memory
const memory = new Memory({
  storage: new LibSQLMemoryAdapter(),
  embedding: new AiSdkEmbeddingAdapter(
    google.textEmbeddingModel("models/text-embedding-004")
  ),
  vector: new InMemoryVectorAdapter(),
});

// Create supervisor agent
const supervisor = new Agent({
  name: "Test Supervisor",
  instructions: `You are a test agent. Analyze the provided file content and return a JSON object with issues found.`,
  model: google("gemini-2.5-pro"),
  memory,
});

async function main() {
  const content = await readFile(
    "tools/agents/__tests__/reference-linker.test.qmd",
    "utf-8"
  );

  console.log("Testing supervisor agent...");
  console.log("File length:", content.length);

  const response = await supervisor.chat(
    `Review this file and return a JSON object with this structure:
{
  "issues": [
    {
      "type": "reference",
      "priority": "high",
      "description": "Description here",
      "lineNumber": 42
    }
  ]
}

File content:
\`\`\`
${content.substring(0, 500)}
\`\`\`

Find hardcoded numbers that aren't in LaTeX equations or code blocks.`,
    {
      userId: "test",
      conversationId: "test-conv",
    }
  );

  console.log("\n=== Agent Response ===");
  console.log(response.text);
  console.log("\n=== End Response ===");
}

main().catch(console.error);
