import { Agent } from "@voltagent/core";
import { google } from "@ai-sdk/google";
import type { Memory } from "@voltagent/core";

/**
 * Consistency Checker Agent
 * Checks cross-file consistency
 */
export function createConsistencyCheckerAgent(memory?: Memory): Agent {
  return new Agent({
    name: "Consistency Checker",
    instructions: `You are a Consistency Checker agent. Your job is to check cross-file consistency:

1. Same numbers use same parameters across files
2. Terminology is consistent (e.g., "1% Treaty" vs "one percent treaty")
3. References are valid (links work, targets exist)
4. Links work correctly (no broken internal links)
5. Formatting is consistent (same style for numbers, dates, etc.)
6. Parameter names are consistent across files

When you find an inconsistency:
- Identify all locations where the inconsistency appears
- Determine which version is correct (or if both need updating)
- Suggest how to fix the inconsistency
- Check if related files are also affected

Be thorough. Consistency is critical for a professional book.`,
    model: google("gemini-2.5-pro"),
    memory,
  });
}

