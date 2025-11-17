#!/usr/bin/env tsx
/**
 * Generate actionable fixes from WISHONIA todos
 * Converts todos into a structured fixes.json with exact find/replace actions
 */

import "dotenv/config";
import { WishoniaVoltAgent } from "../../agents/wishonia-voltagent";
import { writeFile, readFile } from "fs/promises";
import { EnhancedTodo } from "../../agents/todo-manager-enhanced";

interface Fix {
  id: string;
  file: string;
  type: string;
  priority: string;
  lineNumber?: number;
  description: string;
  find?: string;
  replace?: string;
  suggestedFix: string;
  confidence: string;
  autoApply: boolean; // High confidence fixes can be auto-applied
  reviewed: boolean;
  approved: boolean;
}

/**
 * Extract the exact text to find from the issue description
 */
function extractFindText(issue: EnhancedTodo, fileContent: string): string | undefined {
  // Try to extract from description
  const descMatch = issue.issue.match(/['"]([^'"]+)['"]/);
  if (descMatch) {
    const text = descMatch[1];
    // Verify it exists in the file
    if (fileContent.includes(text)) {
      return text;
    }
  }

  // Try to extract from the line number
  if (issue.line && issue.line > 0) {
    const lines = fileContent.split('\n');
    if (issue.line <= lines.length) {
      const line = lines[issue.line - 1];
      // Look for numbers in that line
      const numberMatch = line.match(/\$?[\d,]+(?:\.\d+)?(?:\s*(?:billion|million|trillion|%|:1))?/);
      if (numberMatch) {
        return numberMatch[0];
      }
    }
  }

  return undefined;
}

/**
 * Determine if a fix should be auto-applied based on confidence and type
 */
function shouldAutoApply(issue: EnhancedTodo): boolean {
  // Only auto-apply high confidence fixes
  if (issue.confidence !== "high") {
    return false;
  }

  // Auto-apply reference fixes (simple replacements)
  if (issue.type === "reference" && issue.suggestedFix) {
    return true;
  }

  // Don't auto-apply math or consistency issues (need human review)
  if (issue.type === "math" || issue.type === "consistency") {
    return false;
  }

  return false;
}

async function main() {
  const args = process.argv.slice(2);
  const options = {
    full: args.includes("--full"),
    force: args.includes("--force"), // Force regenerate even if fixes.json exists
  };

  console.log("\n🔧 WISHONIA Fix Generator\n");

  // Check if we should run a full scan first
  if (options.full) {
    console.log("Running full scan...");
    const wishonia = new WishoniaVoltAgent();
    await wishonia.init();
    await wishonia.processAllFiles();
    console.log("✅ Full scan complete\n");
  }

  // Load todos
  const todosContent = await readFile(".wishonia-todos.json", "utf-8");
  const todos: EnhancedTodo[] = JSON.parse(todosContent);

  console.log(`Found ${todos.length} issues to process\n`);

  // Group by file
  const fileMap = new Map<string, EnhancedTodo[]>();
  for (const todo of todos) {
    if (!fileMap.has(todo.filePath)) {
      fileMap.set(todo.filePath, []);
    }
    fileMap.get(todo.filePath)!.push(todo);
  }

  // Generate fixes
  const fixes: Fix[] = [];
  let autoApplyCount = 0;

  for (const [filePath, issues] of fileMap) {
    console.log(`Processing ${filePath} (${issues.length} issues)...`);

    // Load file content
    let fileContent = "";
    try {
      fileContent = await readFile(filePath, "utf-8");
    } catch (error) {
      console.warn(`  ⚠️  Could not read file: ${filePath}`);
      continue;
    }

    for (const issue of issues) {
      const findText = extractFindText(issue, fileContent);
      const autoApply = shouldAutoApply(issue);

      if (autoApply) {
        autoApplyCount++;
      }

      fixes.push({
        id: issue.id,
        file: filePath,
        type: issue.type,
        priority: issue.priority,
        lineNumber: issue.line || undefined,
        description: issue.issue,
        find: findText,
        replace: issue.suggestedFix,
        suggestedFix: issue.suggestedFix || "",
        confidence: issue.confidence,
        autoApply,
        reviewed: false,
        approved: false,
      });
    }
  }

  // Write fixes.json
  const fixesData = {
    generated: new Date().toISOString(),
    totalFixes: fixes.length,
    autoApplyCount,
    reviewRequiredCount: fixes.length - autoApplyCount,
    fixes,
  };

  await writeFile(".wishonia-fixes.json", JSON.stringify(fixesData, null, 2), "utf-8");

  console.log("\n✅ Generated fixes:");
  console.log(`  Total: ${fixes.length}`);
  console.log(`  Auto-apply: ${autoApplyCount} (high confidence)`);
  console.log(`  Review required: ${fixes.length - autoApplyCount}`);
  console.log("\nNext steps:");
  console.log("  npm run wishonia:review-fixes  # Review and approve fixes");
  console.log("  npm run wishonia:apply-fixes   # Apply approved fixes\n");
}

main().catch(console.error);
