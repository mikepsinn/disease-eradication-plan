import fs from "fs";
import path from "path";
import { glob } from "glob";

interface CaptionEntry {
  original: string;
  replacement: string;
}

const ROOT = path.resolve(import.meta.dirname, "../..");

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const inputArg = args.find((a) => !a.startsWith("--"));

  // Collect entries from either a single file or all batch files
  let entries: CaptionEntry[] = [];

  if (inputArg) {
    const data = fs.readFileSync(path.join(ROOT, inputArg), "utf-8");
    entries = JSON.parse(data);
  } else {
    const singleFile = path.join(ROOT, "captions.json");
    if (fs.existsSync(singleFile)) {
      entries = JSON.parse(fs.readFileSync(singleFile, "utf-8"));
    } else {
      const batchFiles = await glob("captions-batch-*.json", {
        cwd: ROOT,
        absolute: true,
      });
      batchFiles.sort();
      for (const bf of batchFiles) {
        const batch: CaptionEntry[] = JSON.parse(
          fs.readFileSync(bf, "utf-8")
        );
        entries.push(...batch);
      }
    }
  }

  // Build replacement map (only entries with replacements)
  const replacements = entries.filter((e) => e.replacement.trim());
  if (replacements.length === 0) {
    console.log("No captions have replacements. Fill them in first.");
    process.exit(1);
  }

  if (dryRun) console.log("=== DRY RUN MODE ===\n");
  console.log(
    `${replacements.length} captions to replace (${entries.length - replacements.length} skipped)\n`
  );

  // Find all QMD files
  const qmdFiles = await glob("**/*.qmd", {
    cwd: ROOT,
    absolute: true,
    ignore: [
      "_build_temp/**",
      "_book/**",
      "_site/**",
      "node_modules/**",
      ".quarto/**",
      "scripts/**",
    ],
  });

  // Pre-read all files once to avoid repeated I/O
  const fileContents = new Map<string, string>();
  for (const filePath of qmdFiles) {
    fileContents.set(filePath, fs.readFileSync(filePath, "utf-8"));
  }

  let totalReplaced = 0;
  const filesModified = new Set<string>();
  const notFound: string[] = [];
  const writeErrors: string[] = [];

  // Apply all replacements in memory first
  for (const entry of replacements) {
    if (entry.original === entry.replacement) continue;
    const search = `![${entry.original}]`;
    const replace = `![${entry.replacement}]`;
    let found = false;

    for (const filePath of qmdFiles) {
      const content = fileContents.get(filePath)!;
      if (!content.includes(search)) continue;

      found = true;
      const relPath = path.relative(ROOT, filePath).replace(/\\/g, "/");
      fileContents.set(filePath, content.replaceAll(search, replace));

      if (dryRun) {
        console.log(`[DRY RUN] ${relPath}`);
      } else {
        console.log(`Queued: ${relPath}`);
      }
      console.log(`  - "${entry.original.slice(0, 60)}..."`);
      console.log(`  + "${entry.replacement}"\n`);
      totalReplaced++;
      filesModified.add(filePath);
    }

    if (!found) notFound.push(entry.original.slice(0, 80));
  }

  // Write all modified files
  if (!dryRun) {
    for (const filePath of filesModified) {
      const relPath = path.relative(ROOT, filePath).replace(/\\/g, "/");
      try {
        fs.writeFileSync(filePath, fileContents.get(filePath)!, "utf-8");
      } catch (err: any) {
        writeErrors.push(`${relPath}: ${err.message}`);
      }
    }
  }

  console.log("=== Summary ===");
  console.log(`Replacements made: ${totalReplaced}`);
  console.log(`Files modified: ${filesModified.size}`);
  if (writeErrors.length > 0) {
    console.log(`Write errors: ${writeErrors.length}`);
    writeErrors.forEach((e) => console.log(`  ${e}`));
  }
  if (notFound.length > 0) {
    console.log(`Not found: ${notFound.length}`);
    notFound.forEach((n) => console.log(`  "${n}..."`));
  }
}

main();
