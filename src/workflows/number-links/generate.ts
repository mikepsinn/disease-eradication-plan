#!/usr/bin/env tsx
/**
 * Smart number linking using LLM to match numbers to variables
 * The LLM analyzes context to determine which variable fits best
 */

import "dotenv/config";
import { readFile, writeFile, unlink } from "fs/promises";
import { existsSync } from "fs";
import * as yaml from "js-yaml";
import { glob } from "glob";
import { google } from "@ai-sdk/google";
import { generateObject } from "ai";
import { z } from "zod";

interface VariableInfo {
  name: string;
  displayValue: string; // e.g., "$2,718B"
  description: string; // Extracted from title attribute
}

interface Replacement {
  find: string; // Exact string to find in the file
  replace: string; // Exact replacement string
  variableName: string;
  lineNumber?: number;
  reasoning: string; // Why this replacement makes sense
}

/**
 * Parse _variables.yml to extract all variables with their metadata
 */
async function loadVariables(): Promise<VariableInfo[]> {
  const content = await readFile("_variables.yml", "utf-8");
  const data = yaml.load(content) as Record<string, string>;

  const variables: VariableInfo[] = [];

  for (const [name, htmlValue] of Object.entries(data)) {
    // Skip treaty_reduction_pct to avoid "1%" replacements in "1% Treaty"
    if (name === "treaty_reduction_pct") continue;

    // Extract display value: <a ...>VALUE</a>
    const valueMatch = htmlValue.match(/>([^<]+)</);
    // Extract description from title attribute
    const titleMatch = htmlValue.match(/title="([^"]+)"/);

    if (valueMatch) {
      variables.push({
        name,
        displayValue: valueMatch[1],
        description: titleMatch ? titleMatch[1] : "",
      });
    }
  }

  return variables;
}

/**
 * Remove LaTeX blocks, code blocks, and already-linked numbers from content
 * so the LLM only sees text that needs linking
 */
function preprocessContent(content: string): string {
  let processed = content;

  // Replace code blocks with placeholders
  processed = processed.replace(/```[\s\S]*?```/g, "[CODE_BLOCK]");

  // Replace inline code with placeholders
  processed = processed.replace(/`[^`]+`/g, "[CODE]");

  // Replace LaTeX display equations
  processed = processed.replace(/\$\$[\s\S]*?\$\$/g, "[LATEX_BLOCK]");
  processed = processed.replace(/\\\[[\s\S]*?\\\]/g, "[LATEX_BLOCK]");

  // Replace inline LaTeX
  processed = processed.replace(/\$[^$]+\$/g, "[LATEX]");

  // Replace HTML comments
  processed = processed.replace(/<!--[\s\S]*?-->/g, "[COMMENT]");

  // Replace existing {{< var >}} usage
  processed = processed.replace(/\{\{<\s*var\s+[^>]+\s*>\}\}/g, "[VAR]");

  return processed;
}

const ReplacementSchema = z.object({
  replacements: z.array(
    z.object({
      find: z.string().describe("Exact string to find in the file"),
      replace: z.string().describe("Exact replacement string with {{< var >}}"),
      variableName: z.string().describe("The parameter name from variables list"),
      lineNumber: z.number().optional().describe("Approximate line number"),
      reasoning: z.string().describe("Why this replacement makes sense"),
    })
  ),
});

/**
 * Use LLM to analyze file and generate smart replacements
 */
async function analyzeFile(
  filePath: string,
  content: string,
  variables: VariableInfo[]
): Promise<Replacement[]> {
  console.log(`Analyzing ${filePath}...`);

  // Create a concise variable reference for the LLM
  const variableList = variables
    .map(
      (v) =>
        `- ${v.name}: ${v.displayValue}${v.description ? ` (${v.description.split("|")[0].trim()})` : ""}`
    )
    .join("\n");

  const prompt = `You are analyzing a Quarto markdown file to link hardcoded numbers to variables.

FILE: ${filePath}

AVAILABLE VARIABLES:
${variableList}

FILE CONTENT:
\`\`\`
${content}
\`\`\`

TASK: Link hardcoded DATA/STATISTICS to variables (for economist review).

WHAT TO LINK:
- Dollar amounts ($27B, $41,000, etc.)
- Death counts, populations (150,000 deaths, 8 billion humans)
- Trial costs, ratios (82x, 463:1)
- Data percentages (3.5% threshold, 0.7% GDP)

WHAT TO SKIP:
- "1%" (appears in treaty name "1% Treaty")
- Proper names, titles, chapter numbers
- LaTeX equations (already filtered)

HOW TO REPLACE:
- Find: unique phrase with the number
- Replace: same phrase with {{< var name >}}
- Preserve sentence structure - only swap the number

EXAMPLES:

Good replacement:
- find: "costs $40 million to build"
- replace: "costs {{< var dfda_build_cost >}} to build"
- reasoning: "$40 million" matches dfda_build_cost ($40M)

Bad replacement:
- find: "$40 million"
- replace: "The dFDA costs only {{< var dfda_build_cost >}} to build"
(This changes the whole sentence!)

Good replacement:
- find: "The global military spending is $2,718 billion annually"
- replace: "The global military spending is {{< var global_military_spending_annual_2024 >}} annually"
- reasoning: "$2,718 billion" matches global_military_spending_annual_2024 ($2,718B)

Return a JSON array of replacements. Each replacement must:
1. Have a "find" string that appears EXACTLY in the file
2. Have a "replace" string that substitutes the number with {{< var >}}
3. Preserve the sentence structure and surrounding text
4. Include reasoning for why this variable matches

If no numbers need linking, return an empty array.`;

  try {
    const result = await generateObject({
      model: google("gemini-2.5-flash"),
      schema: ReplacementSchema,
      prompt,
    });

    return result.object.replacements;
  } catch (error) {
    console.error(`Error analyzing ${filePath}:`, error);
    return [];
  }
}

const LOCK_FILE = ".wishonia-smart-link.lock";

async function main() {
  // Check for lock file to prevent multiple instances
  if (existsSync(LOCK_FILE)) {
    console.error("\n❌ Another instance is already running.");
    console.error("   If this is incorrect, delete .wishonia-smart-link.lock and try again.\n");
    process.exit(1);
  }

  // Create lock file
  await writeFile(LOCK_FILE, new Date().toISOString(), "utf-8");

  // Clean up lock file on exit
  const cleanup = async () => {
    try {
      await unlink(LOCK_FILE);
    } catch {}
  };
  process.on("exit", cleanup);
  process.on("SIGINT", async () => {
    await cleanup();
    process.exit();
  });
  process.on("SIGTERM", async () => {
    await cleanup();
    process.exit();
  });

  const args = process.argv.slice(2);
  const options = {
    dryRun: args.includes("--dry-run"),
    filePattern: args.find((arg) => !arg.startsWith("--")) || "knowledge/**/*.qmd",
    singleFile: args.find((arg) => arg.startsWith("--file="))?.replace("--file=", ""),
  };

  console.log("\n🤖 Smart Number Linker (LLM-powered)\n");

  // Load all variables
  console.log("Loading variables from _variables.yml...");
  const variables = await loadVariables();
  console.log(`Found ${variables.length} variables\n`);

  // Find files to process
  let files: string[];
  if (options.singleFile) {
    files = [options.singleFile];
  } else {
    files = await glob(options.filePattern, {
      ignore: ["node_modules/**", "_book/**", ".quarto/**", "**/references.qmd"],
    });
  }
  console.log(`Processing ${files.length} file(s)...\n`);

  // Process each file
  const allReplacements: (Replacement & { file: string })[] = [];

  for (const file of files) {
    const content = await readFile(file, "utf-8");

    // Preprocess to remove code/LaTeX blocks
    const processedContent = preprocessContent(content);

    // Skip if no numbers left to process
    if (!/\d/.test(processedContent)) {
      console.log(`  Skipped ${file} (no numbers to link)\n`);
      continue;
    }

    // Use LLM to analyze
    const replacements = await analyzeFile(file, content, variables);

    if (replacements.length > 0) {
      console.log(`  Found ${replacements.length} replacement(s)\n`);
      for (const r of replacements) {
        allReplacements.push({ ...r, file });
      }
    } else {
      console.log(`  No replacements needed\n`);
    }

    // Save progress incrementally (in case of crashes)
    if (allReplacements.length > 0) {
      const outputData = {
        generated: new Date().toISOString(),
        totalReplacements: allReplacements.length,
        replacements: allReplacements,
      };
      await writeFile(
        ".wishonia-number-links.json",
        JSON.stringify(outputData, null, 2),
        "utf-8"
      );
    }

    // Rate limit (don't spam the API)
    if (files.length > 1) {
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  }

  // Save results
  if (allReplacements.length > 0) {
    const outputData = {
      generated: new Date().toISOString(),
      totalReplacements: allReplacements.length,
      replacements: allReplacements,
    };

    await writeFile(
      ".wishonia-number-links.json",
      JSON.stringify(outputData, null, 2),
      "utf-8"
    );

    console.log(`\n✅ Generated ${allReplacements.length} replacements\n`);
    console.log("Saved to: .wishonia-number-links.json\n");

    // Show summary
    const byFile = new Map<string, number>();
    for (const r of allReplacements) {
      byFile.set(r.file, (byFile.get(r.file) || 0) + 1);
    }

    console.log("Summary by file:");
    for (const [file, count] of byFile) {
      console.log(`  ${file}: ${count} replacement(s)`);
    }

    console.log("\nNext steps:");
    console.log("  1. Review .wishonia-number-links.json");
    console.log("  2. npm run wishonia:apply-links --dry-run  # Preview changes");
    console.log("  3. npm run wishonia:apply-links            # Apply changes\n");
  } else {
    console.log("\n✅ No replacements needed - all numbers already linked!\n");
  }
}

main().catch(console.error);
