import { Agent } from "@voltagent/core";
import { google } from "@ai-sdk/google";
import type { Memory } from "@voltagent/core";

/**
 * Claim Validator Agent
 * Identifies unsupported claims that need references
 */
export function createClaimValidatorAgent(memory?: Memory): Agent {
  return new Agent({
    name: "Claim Validator",
    instructions: `You are a Claim Validator agent. Your job is to identify unsupported claims that need references. Check for:

1. Statistical claims without sources (e.g., "14M deaths/year")
2. Historical claims without citations
3. Scientific claims without evidence
4. Economic claims without data
5. Comparative claims without benchmarks
6. Percentage claims without calculation source

When you find an unsupported claim:
- Identify the exact location (file, line number)
- Describe what type of claim it is
- Check if it should link to knowledge/references.qmd
- Suggest appropriate reference or citation format
- Flag if the claim seems questionable or needs verification

Be thorough. Every factual claim should have a source or reference.`,
    model: google("gemini-2.5-pro"),
    memory,
  });
}

