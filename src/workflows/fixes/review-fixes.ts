#!/usr/bin/env tsx
/**
 * Interactive CLI to review and approve fixes
 */

import { readFile, writeFile } from "fs/promises";
import * as readline from "readline";

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

function createInterface() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
}

function question(rl: readline.Interface, query: string): Promise<string> {
  return new Promise((resolve) => {
    rl.question(query, resolve);
  });
}

async function reviewFix(rl: readline.Interface, fix: Fix, index: number, total: number): Promise<"approve" | "reject" | "skip" | "quit"> {
  console.log(`\n${"=".repeat(80)}`);
  console.log(`Fix ${index + 1} of ${total}`);
  console.log(`${"=".repeat(80)}`);
  console.log(`File: ${fix.file}:${fix.lineNumber || "?"}`);
  console.log(`Type: ${fix.type} | Priority: ${fix.priority} | Confidence: ${fix.confidence}`);
  console.log(`\nIssue:`);
  console.log(`  ${fix.description}`);

  if (fix.find) {
    console.log(`\nCurrent text:`);
    console.log(`  "${fix.find}"`);
  }

  console.log(`\nSuggested fix:`);
  console.log(`  ${fix.suggestedFix}`);

  if (fix.replace && fix.find && fix.find !== fix.replace) {
    console.log(`\nWill replace:`);
    console.log(`  "${fix.find}"`);
    console.log(`With:`);
    console.log(`  "${fix.replace}"`);
  }

  if (fix.autoApply) {
    console.log(`\n⚡ Auto-apply: YES (high confidence)`);
  }

  const answer = await question(rl, "\n[a]pprove, [r]eject, [s]kip, [q]uit: ");

  switch (answer.toLowerCase().trim()) {
    case "a":
    case "approve":
      return "approve";
    case "r":
    case "reject":
      return "reject";
    case "s":
    case "skip":
      return "skip";
    case "q":
    case "quit":
      return "quit";
    default:
      console.log("Invalid choice, skipping...");
      return "skip";
  }
}

async function main() {
  console.log("\n🔍 WISHONIA Fix Reviewer\n");

  // Load fixes
  const fixesContent = await readFile(".wishonia-fixes.json", "utf-8");
  const fixesData: FixesData = JSON.parse(fixesContent);

  // Filter unreviewed fixes
  const unreviewedFixes = fixesData.fixes.filter(f => !f.reviewed);

  if (unreviewedFixes.length === 0) {
    console.log("No fixes to review! All fixes have been reviewed.\n");
    return;
  }

  console.log(`Found ${unreviewedFixes.length} fixes to review\n`);
  console.log("Controls:");
  console.log("  [a]pprove - Approve this fix for application");
  console.log("  [r]eject  - Reject this fix (won't be applied)");
  console.log("  [s]kip    - Skip for now (review later)");
  console.log("  [q]uit    - Save and exit\n");

  const rl = createInterface();
  let approvedCount = 0;
  let rejectedCount = 0;

  for (let i = 0; i < unreviewedFixes.length; i++) {
    const fix = unreviewedFixes[i];
    const result = await reviewFix(rl, fix, i, unreviewedFixes.length);

    switch (result) {
      case "approve":
        fix.reviewed = true;
        fix.approved = true;
        approvedCount++;
        console.log("✅ Approved");
        break;
      case "reject":
        fix.reviewed = true;
        fix.approved = false;
        rejectedCount++;
        console.log("❌ Rejected");
        break;
      case "skip":
        console.log("⏭️  Skipped");
        break;
      case "quit":
        console.log("\nSaving and exiting...");
        await writeFile(".wishonia-fixes.json", JSON.stringify(fixesData, null, 2), "utf-8");
        rl.close();
        console.log(`\n✅ Reviewed ${approvedCount + rejectedCount} fixes`);
        console.log(`  Approved: ${approvedCount}`);
        console.log(`  Rejected: ${rejectedCount}\n`);
        return;
    }
  }

  // Save updated fixes
  await writeFile(".wishonia-fixes.json", JSON.stringify(fixesData, null, 2), "utf-8");
  rl.close();

  console.log(`\n✅ Review complete!`);
  console.log(`  Approved: ${approvedCount}`);
  console.log(`  Rejected: ${rejectedCount}`);
  console.log(`\nNext step:`);
  console.log(`  npm run wishonia:apply-fixes  # Apply approved fixes\n`);
}

main().catch(console.error);
