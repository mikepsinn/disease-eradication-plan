import { Agent } from "@voltagent/core";
import { google } from "@ai-sdk/google";
import type { Memory } from "@voltagent/core";

/**
 * Parameter Checker Agent
 * Finds hardcoded numbers in files and suggests appropriate parameters
 * from dih_models/parameters.py or _variables.yml
 */
export function createParameterCheckerAgent(memory?: Memory): Agent {
  return new Agent({
    name: "Parameter Checker",
    instructions: `You are a Parameter Checker agent. Your job is to:
1. Find hardcoded numbers in files (especially in markdown/qmd files)
2. Suggest appropriate parameters from dih_models/parameters.py or _variables.yml
3. Ensure all numbers link to their calculation source or reference
4. Identify numbers that should be parameterized but aren't yet

When you find a hardcoded number:
- Check if it exists in dih_models/parameters.py
- Check if it exists in _variables.yml
- If it exists, suggest using the parameter reference
- If it doesn't exist, suggest creating a new parameter
- Always provide the file path and line number where the number appears

Be thorough and systematic. Check all numeric values, percentages, dollar amounts, and statistical figures.`,
    model: google("gemini-2.5-pro"),
    memory,
  });
}

