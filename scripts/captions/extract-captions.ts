import fs from "fs";
import path from "path";
import { glob } from "glob";

interface CaptionEntry {
  original: string;
  replacement: string;
}

const ROOT = path.resolve(import.meta.dirname, "../..");

function extractCaptions(qmdFiles: string[]): CaptionEntry[] {
  const seen = new Set<string>();
  const entries: CaptionEntry[] = [];

  const imageRegex = /^!\[([^\]]+)\]\([^)]+\)/;

  for (const filePath of qmdFiles) {
    const content = fs.readFileSync(filePath, "utf-8");
    const lines = content.split("\n");

    for (const line of lines) {
      const match = line.match(imageRegex);
      if (!match) continue;

      const caption = match[1].trim();
      if (!caption || seen.has(caption)) continue;
      seen.add(caption);

      entries.push({ original: caption, replacement: "" });
    }
  }

  return entries;
}

async function main() {
  const args = process.argv.slice(2);
  const batchSizeArg = args.find((a) => a.startsWith("--batch-size="));
  const batchSize = batchSizeArg
    ? parseInt(batchSizeArg.split("=")[1])
    : undefined;

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

  console.log(`Found ${qmdFiles.length} QMD files`);

  const entries = extractCaptions(qmdFiles);
  console.log(`Extracted ${entries.length} unique captions`);

  if (batchSize && batchSize > 0) {
    const numBatches = Math.ceil(entries.length / batchSize);
    for (let b = 0; b < numBatches; b++) {
      const batch = entries.slice(b * batchSize, (b + 1) * batchSize);
      const batchFile = path.join(ROOT, `captions-batch-${b + 1}.json`);
      fs.writeFileSync(batchFile, JSON.stringify(batch, null, 2), "utf-8");
      console.log(
        `Wrote ${batch.length} captions to captions-batch-${b + 1}.json`
      );
    }
    console.log(
      `\nSplit into ${numBatches} batch files of ~${batchSize} each`
    );
  } else {
    const outPath = path.join(ROOT, "captions.json");
    fs.writeFileSync(outPath, JSON.stringify(entries, null, 2), "utf-8");
    console.log(`Wrote ${entries.length} captions to captions.json`);
  }
}

main();
