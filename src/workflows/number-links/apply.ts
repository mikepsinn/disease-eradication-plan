#!/usr/bin/env tsx
/**
 * Apply number linking replacements from .wishonia-number-links.json
 */

import { readFile, writeFile } from "fs/promises";

interface Replacement {
  file: string;
  find: string;
  replace: string;
  variableName: string;
  lineNumber?: number;
  reasoning: string;
}

interface ReplacementsData {
  generated: string;
  totalReplacements: number;
  replacements: Replacement[];
}

async function applyReplacement(
  filePath: string,
  replacement: Replacement
): Promise<boolean> {
  try {
    const content = await readFile(filePath, "utf-8");

    // Check if the find string exists
    if (!content.includes(replacement.find)) {
      console.log(`  ⚠️  Could not find: "${replacement.find.substring(0, 60)}..."`);
      return false;
    }

    // Count occurrences
    const occurrences = content.split(replacement.find).length - 1;
    if (occurrences > 1) {
      console.log(
        `  ⚠️  Found ${occurrences} occurrences - skipping (need unique string)`
      );
      console.log(`     Find: "${replacement.find.substring(0, 60)}..."`);
      return false;
    }

    // Apply replacement
    const newContent = content.replace(replacement.find, replacement.replace);
    await writeFile(filePath, newContent, "utf-8");

    return true;
  } catch (error) {
    console.error(`  ❌ Error:`, error);
    return false;
  }
}

async function main() {
  const args = process.argv.slice(2);
  const options = {
    dryRun: args.includes("--dry-run"),
  };

  console.log("\n🔗 Apply Number Links\n");

  // Load replacements
  const data: ReplacementsData = JSON.parse(
    await readFile(".wishonia-number-links.json", "utf-8")
  );

  console.log(`Found ${data.totalReplacements} replacement(s) to apply\n`);

  if (data.totalReplacements === 0) {
    console.log("Nothing to apply!\n");
    return;
  }

  // Group by file
  const byFile = new Map<string, Replacement[]>();
  for (const r of data.replacements) {
    if (!byFile.has(r.file)) {
      byFile.set(r.file, []);
    }
    byFile.get(r.file)!.push(r);
  }

  // Apply replacements
  let successCount = 0;
  let failCount = 0;

  for (const [file, replacements] of byFile) {
    console.log(`\n${file} (${replacements.length} replacement(s)):`);

    for (const r of replacements) {
      if (options.dryRun) {
        console.log(`  [DRY RUN] Would replace:`);
        console.log(`    Find:    "${r.find}"`);
        console.log(`    Replace: "${r.replace}"`);
        console.log(`    Reason:  ${r.reasoning}`);
        successCount++;
      } else {
        const success = await applyReplacement(file, r);
        if (success) {
          console.log(`  ✅ ${r.variableName}`);
          console.log(`     "${r.find.substring(0, 60)}..."`);
          console.log(`     → "${r.replace.substring(0, 60)}..."`);
          successCount++;
        } else {
          failCount++;
        }
      }
    }
  }

  console.log(`\n\n✅ Applied ${successCount} replacement(s)`);
  if (failCount > 0) {
    console.log(`⚠️  ${failCount} failed (may need manual review)`);
  }

  if (!options.dryRun && successCount > 0) {
    console.log("\nNext steps:");
    console.log("  git diff                          # Review changes");
    console.log("  npm run wishonia:smart-link       # Re-scan to verify");
    console.log("  git add -u && git commit          # Commit changes\n");
  } else if (options.dryRun) {
    console.log("\nRun without --dry-run to apply changes\n");
  }
}

main().catch(console.error);
