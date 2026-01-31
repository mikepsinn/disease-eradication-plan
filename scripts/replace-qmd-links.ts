#!/usr/bin/env node
/**
 * General-purpose QMD link replacement script
 *
 * Replaces links from one QMD file to another across all QMD files in the project.
 * Handles various link formats (relative paths, absolute paths, with/without anchors).
 *
 * Usage:
 *   npx tsx scripts/replace-qmd-links.ts <from-pattern> <to-pattern> [--dry-run]
 *
 * Arguments:
 *   from-pattern  The file path pattern to search for (e.g., "solution/incentive-alignment-bonds.qmd")
 *   to-pattern    The replacement path (e.g., "appendix/incentive-alignment-bonds-paper.qmd")
 *
 * Options:
 *   --dry-run     Show what would be changed without making changes
 *
 * Examples:
 *   npx tsx scripts/replace-qmd-links.ts "solution/incentive-alignment-bonds.qmd" "appendix/incentive-alignment-bonds-paper.qmd" --dry-run
 *   npx tsx scripts/replace-qmd-links.ts "old-file.qmd" "new-file.qmd"
 */

import fs from "fs/promises";
import path from "path";
import { glob } from "glob";
import { getProjectRoot } from "./lib/file-utils";

const PROJECT_ROOT = getProjectRoot();

interface Replacement {
  file: string;
  line: number;
  oldText: string;
  newText: string;
}

async function main() {
  const args = process.argv.slice(2).filter((a) => !a.startsWith("--"));
  const dryRun = process.argv.includes("--dry-run");

  if (args.length < 2) {
    console.log(`
Usage: npx tsx scripts/replace-qmd-links.ts <from-pattern> <to-pattern> [--dry-run]

Arguments:
  from-pattern  The file path pattern to search for
  to-pattern    The replacement path

Examples:
  npx tsx scripts/replace-qmd-links.ts "solution/old-file.qmd" "appendix/new-file.qmd" --dry-run
  npx tsx scripts/replace-qmd-links.ts "economics/old.qmd" "economics/new.qmd"
`);
    process.exit(1);
  }

  const [fromPattern, toPattern] = args;

  console.log(`Replacing: ${fromPattern}`);
  console.log(`     With: ${toPattern}`);
  if (dryRun) {
    console.log("\nDRY RUN - no files will be modified\n");
  } else {
    console.log("");
  }

  // Find all QMD files
  const files = await glob("**/*.qmd", {
    cwd: PROJECT_ROOT,
    ignore: ["node_modules/**", "_book/**", ".quarto/**", "_build_temp/**"],
    absolute: true,
  });

  console.log(`Scanning ${files.length} QMD files...\n`);

  const allReplacements: Replacement[] = [];
  let filesModified = 0;

  for (const file of files) {
    const content = await fs.readFile(file, "utf-8");
    const lines = content.split("\n");

    // Build regex to match links containing the from-pattern
    // Matches: [text](path/to/from-pattern#anchor) or [text](../path/to/from-pattern)
    // Escape special regex characters in the pattern
    const escapedPattern = fromPattern.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

    // Pattern matches markdown links with various path prefixes
    const linkPattern = new RegExp(
      `(\\[.*?\\]\\()([\\./]*(?:knowledge\\/)?(?:[\\w-]+\\/)*?)${escapedPattern}(#[^\\)]*)?\\)`,
      "g"
    );

    let newContent = content;
    const fileReplacements: Replacement[] = [];

    // Track line numbers for replacements
    let currentPos = 0;
    newContent = content.replace(linkPattern, (match, prefix, pathPrefix, anchor, offset) => {
      // Calculate line number
      const lineNum = content.substring(0, content.indexOf(match, currentPos)).split("\n").length;
      currentPos = content.indexOf(match, currentPos) + match.length;

      // Build the new path
      const newPath = `${prefix}${pathPrefix}${toPattern}${anchor || ""})`;

      fileReplacements.push({
        file: path.relative(PROJECT_ROOT, file),
        line: lineNum,
        oldText: match,
        newText: newPath,
      });

      return newPath;
    });

    if (fileReplacements.length > 0) {
      const relPath = path.relative(PROJECT_ROOT, file);
      console.log(`${relPath}:`);

      for (const r of fileReplacements) {
        console.log(`  L${r.line}: ${r.oldText}`);
        console.log(`      → ${r.newText}`);
      }
      console.log("");

      allReplacements.push(...fileReplacements);

      if (!dryRun) {
        await fs.writeFile(file, newContent, "utf-8");
      }

      filesModified++;
    }
  }

  console.log("=".repeat(60));
  console.log(`Total: ${allReplacements.length} replacement(s) in ${filesModified} file(s)`);

  if (dryRun && allReplacements.length > 0) {
    console.log("\nRun without --dry-run to apply changes");
  }
}

main().catch(console.error);
