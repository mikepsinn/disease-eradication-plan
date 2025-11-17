#!/usr/bin/env tsx
/**
 * Apply approved fixes from .wishonia-fixes.json
 */

import { readFile, writeFile } from "fs/promises";
import { execSync } from "child_process";

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
  autoApply: boolean;
  reviewed: boolean;
  approved: boolean;
}

interface FixesData {
  generated: string;
  totalFixes: number;
  autoApplyCount: number;
  reviewRequiredCount: number;
  fixes: Fix[];
}

async function applyFix(fix: Fix): Promise<boolean> {
  try {
    const content = await readFile(fix.file, "utf-8");

    // If we have an exact find string, use it
    if (fix.find && fix.replace) {
      if (!content.includes(fix.find)) {
        console.log(`  ⚠️  Could not find text in ${fix.file}`);
        console.log(`     Looking for: "${fix.find.substring(0, 50)}..."`);
        return false;
      }

      // Replace the text
      const newContent = content.replace(fix.find, fix.replace);
      await writeFile(fix.file, newContent, "utf-8");
      return true;
    }

    // Otherwise, try to apply based on line number and suggested fix
    if (fix.lineNumber && fix.suggestedFix) {
      const lines = content.split('\n');
      if (fix.lineNumber > 0 && fix.lineNumber <= lines.length) {
        // This is more complex - would need smarter matching
        console.log(`  ⚠️  Manual fix required for line ${fix.lineNumber} in ${fix.file}`);
        console.log(`     Suggested: ${fix.suggestedFix.substring(0, 80)}...`);
        return false;
      }
    }

    console.log(`  ⚠️  Cannot automatically apply fix to ${fix.file}`);
    return false;
  } catch (error) {
    console.error(`  ❌ Error applying fix to ${fix.file}:`, error);
    return false;
  }
}

async function main() {
  const args = process.argv.slice(2);
  const options = {
    autoOnly: args.includes("--auto-only"),
    dryRun: args.includes("--dry-run"),
  };

  console.log("\n🔧 WISHONIA Fix Applicator\n");

  // Load fixes
  const fixesContent = await readFile(".wishonia-fixes.json", "utf-8");
  const fixesData: FixesData = JSON.parse(fixesContent);

  // Filter fixes to apply
  let fixesToApply: Fix[];

  if (options.autoOnly) {
    fixesToApply = fixesData.fixes.filter(f => f.autoApply && !f.reviewed);
    console.log(`Applying ${fixesToApply.length} auto-approved fixes...\n`);
  } else {
    fixesToApply = fixesData.fixes.filter(f => f.approved);
    console.log(`Applying ${fixesToApply.length} approved fixes...\n`);
  }

  if (fixesToApply.length === 0) {
    console.log("No fixes to apply.");
    console.log("\nRun 'npm run wishonia:review-fixes' to approve fixes first.\n");
    return;
  }

  // Group by file
  const fileMap = new Map<string, Fix[]>();
  for (const fix of fixesToApply) {
    if (!fileMap.has(fix.file)) {
      fileMap.set(fix.file, []);
    }
    fileMap.get(fix.file)!.push(fix);
  }

  // Apply fixes
  let successCount = 0;
  let failCount = 0;

  for (const [filePath, fixes] of fileMap) {
    console.log(`${filePath} (${fixes.length} fixes)`);

    for (const fix of fixes) {
      if (options.dryRun) {
        console.log(`  [DRY RUN] Would apply: ${fix.description.substring(0, 60)}...`);
        successCount++;
      } else {
        const success = await applyFix(fix);
        if (success) {
          console.log(`  ✅ ${fix.type}: ${fix.description.substring(0, 60)}...`);
          successCount++;

          // Mark as applied
          fix.reviewed = true;
        } else {
          failCount++;
        }
      }
    }
  }

  // Update fixes.json with applied status
  if (!options.dryRun) {
    await writeFile(".wishonia-fixes.json", JSON.stringify(fixesData, null, 2), "utf-8");
  }

  console.log(`\n✅ Applied ${successCount} fixes`);
  if (failCount > 0) {
    console.log(`⚠️  ${failCount} fixes failed (manual review needed)`);
  }

  if (!options.dryRun && successCount > 0) {
    console.log("\nNext steps:");
    console.log("  git diff               # Review changes");
    console.log("  npm run wishonia       # Re-scan to verify");
    console.log("  git add -u             # Stage changes");
    console.log("  git commit             # Commit fixes\n");
  }
}

main().catch(console.error);
