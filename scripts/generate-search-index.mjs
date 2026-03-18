/**
 * Generate section-level search index for the chat widget RAG system.
 *
 * Reads _quarto-manual.yml (full book config), splits each QMD chapter into
 * sections at ## headings, chunks oversized sections at ### headings,
 * strips Quarto syntax, and outputs search-index.json.
 *
 * Usage: node scripts/generate-search-index.mjs
 */

import { readFileSync, writeFileSync, existsSync } from "fs";
import { resolve, basename } from "path";

const MAX_SECTION_CHARS = 10000;
const MIN_SECTION_CHARS = 500;

const ROOT = resolve(import.meta.dirname, "..");
const CONFIG = resolve(ROOT, "_quarto-manual.yml");
const OUTPUT = resolve(ROOT, "_manual-paperback/warondisease/search-index.json");
const VARS_FILE = resolve(ROOT, "_variables.yml");

// ---------------------------------------------------------------------------
// 0. Load _variables.yml and build a lookup of plain-text values
// ---------------------------------------------------------------------------

function loadVariables() {
  if (!existsSync(VARS_FILE)) return {};
  const raw = readFileSync(VARS_FILE, "utf-8");
  const vars = {};
  // _variables.yml is a flat YAML of "key": "value" pairs with escaped quotes inside values
  for (const line of raw.split("\n")) {
    // Match key: value where value may contain escaped quotes
    const colonIdx = line.indexOf('": "');
    if (colonIdx === -1 || !line.startsWith('"')) continue;
    const key = line.substring(1, colonIdx);
    // Value starts after '": "' and ends before trailing '"'
    let val = line.substring(colonIdx + 4);
    if (val.endsWith('"')) val = val.slice(0, -1);
    // Unescape
    val = val.replace(/\\"/g, '"').replace(/\\n/g, "\n");
    // Extract display text from <a ...>display text</a> (the title attr has noise)
    const anchorMatch = val.match(/>([^<]+)<\/a>/);
    if (anchorMatch) {
      val = anchorMatch[1];
    } else {
      // Fallback: strip all HTML tags
      val = val.replace(/<[^>]+>/g, "");
    }
    // Skip _latex and _nounit variants in search text (they add noise)
    if (key.endsWith("_latex") || key.endsWith("_nounit")) continue;
    vars[key] = val.trim();
  }
  return vars;
}

const VARIABLES = loadVariables();
console.log(`Loaded ${Object.keys(VARIABLES).length} variables from _variables.yml`);

// ---------------------------------------------------------------------------
// 1. Parse QMD file list from the Quarto config
// ---------------------------------------------------------------------------

function parseChapterFiles() {
  const yml = readFileSync(CONFIG, "utf-8");
  const files = [];

  for (const line of yml.split("\n")) {
    const trimmed = line.trim();
    // Skip comments and lines without .qmd
    if (trimmed.startsWith("#") || !trimmed.includes(".qmd")) continue;
    // Skip href: lines (sidebar links, not chapter files)
    if (trimmed.startsWith("href:") || trimmed.startsWith("- href:")) continue;
    // Extract the .qmd path (strip leading "- " and any trailing comments/annotations)
    const match = trimmed.match(/^-\s+([\w/.-]+\.qmd)/);
    if (match) files.push(match[1]);
  }

  return files;
}

// ---------------------------------------------------------------------------
// 2. Convert a QMD path to its rendered HTML URL
// ---------------------------------------------------------------------------

function qmdToUrl(qmdPath) {
  // knowledge/solution/1-percent-treaty.qmd -> /solution/1-percent-treaty.html
  let url = qmdPath.replace(/\.qmd$/, ".html");
  if (url.startsWith("knowledge/")) url = url.slice("knowledge/".length);
  // Ensure leading slash
  if (!url.startsWith("/")) url = "/" + url;
  return url;
}

// ---------------------------------------------------------------------------
// 3. Generate a URL-friendly anchor from a heading
// ---------------------------------------------------------------------------

function slugify(heading) {
  return heading
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, "") // strip special chars
    .replace(/\s+/g, "-")          // spaces to hyphens
    .replace(/-+/g, "-")           // collapse multiple hyphens
    .replace(/^-|-$/g, "");        // trim leading/trailing hyphens
}

// ---------------------------------------------------------------------------
// 4. Strip Quarto/markdown syntax that doesn't help search
// ---------------------------------------------------------------------------

function stripContent(text) {
  let s = text;

  // Remove {{< include ... >}} lines
  s = s.replace(/^\{\{<\s*include\s+[^>]+>\}\}\s*$/gm, "");

  // Resolve {{< var name >}} shortcodes to their actual values
  s = s.replace(/\{\{<\s*var\s+(\S+)\s*>\}\}/g, function (_, name) {
    return VARIABLES[name] || "";
  });

  // Remove other Quarto shortcodes
  s = s.replace(/\{\{<[^>]+>\}\}/g, "");

  // Remove LaTeX blocks ($$...$$, possibly multiline)
  s = s.replace(/\$\$[\s\S]*?\$\$/g, "");

  // Remove inline LaTeX ($...$) but NOT dollar amounts like $0.177 or $27.2B
  // LaTeX typically starts with $ followed by a letter or backslash, not a digit
  s = s.replace(/\$[a-zA-Z\\][^$\n]*\$/g, "");

  // Remove image syntax ![alt](url) but keep alt text
  s = s.replace(/!\[([^\]]*)\]\([^)]*\)/g, "$1");

  // Remove link syntax [text](url) but keep text
  s = s.replace(/\[([^\]]*)\]\([^)]*\)/g, "$1");

  // Remove Quarto div fences ::: {.class}
  s = s.replace(/^:::\s*\{[^}]*\}\s*$/gm, "");
  s = s.replace(/^:::\s*$/gm, "");

  // Remove HTML tags
  s = s.replace(/<[^>]+>/g, "");

  // Remove citation syntax [@key] or [@key1; @key2]
  s = s.replace(/\[@[^\]]+\]/g, "");

  // Remove markdown bold/italic markers
  s = s.replace(/\*{1,3}([^*]+)\*{1,3}/g, "$1");

  // Collapse multiple blank lines to one
  s = s.replace(/\n{3,}/g, "\n\n");

  return s.trim();
}

// ---------------------------------------------------------------------------
// 5. Extract title from YAML frontmatter
// ---------------------------------------------------------------------------

function resolveVars(text) {
  return (text || "")
    .replace(/\{\{<\s*var\s+(\S+)\s*>\}\}/g, (_, name) => VARIABLES[name] || "")
    .replace(/\s*\{#[^}]+\}/g, "")  // strip Quarto cross-ref anchors {#sec-foo}
    .trim();
}

function extractTitle(content) {
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (fmMatch) {
    const titleMatch = fmMatch[1].match(/^title:\s*['"]?(.+?)['"]?\s*$/m);
    if (titleMatch) return titleMatch[1];
  }
  // Fallback: first # heading in the body
  const h1Match = content.match(/^#\s+(.+)/m);
  return h1Match ? h1Match[1].trim() : null;
}

// ---------------------------------------------------------------------------
// 6. Remove YAML frontmatter from content
// ---------------------------------------------------------------------------

function stripFrontmatter(content) {
  return content.replace(/^---\n[\s\S]*?\n---\n?/, "");
}

// ---------------------------------------------------------------------------
// 7. Split content into sections at ## headings
// ---------------------------------------------------------------------------

function splitSections(body) {
  // Split at lines starting with ## (but not ### or more)
  const sections = [];
  const lines = body.split("\n");
  let currentHeading = null;
  let currentLines = [];

  for (const line of lines) {
    // Match ## heading (exactly two #, not ### or more)
    const headingMatch = line.match(/^##\s+(.+)/);
    if (headingMatch && !line.startsWith("###")) {
      // Save previous section
      if (currentLines.length > 0 || currentHeading !== null) {
        sections.push({
          heading: currentHeading,
          text: currentLines.join("\n"),
        });
      }
      currentHeading = headingMatch[1].trim();
      currentLines = [];
    } else {
      currentLines.push(line);
    }
  }

  // Save last section
  if (currentLines.length > 0 || currentHeading !== null) {
    sections.push({
      heading: currentHeading,
      text: currentLines.join("\n"),
    });
  }

  return sections;
}

// ---------------------------------------------------------------------------
// 8. Chunk oversized sections at ### sub-headings
// ---------------------------------------------------------------------------

function chunkOversizedSections(sections) {
  const result = [];
  for (const section of sections) {
    const cleanLen = stripContent(section.text).length;
    if (cleanLen <= MAX_SECTION_CHARS) {
      result.push(section);
      continue;
    }
    // Sub-split at ### headings
    const subSections = [];
    const lines = section.text.split("\n");
    let currentSubHeading = null;
    let currentLines = [];

    for (const line of lines) {
      const subMatch = line.match(/^###\s+(.+)/);
      if (subMatch) {
        if (currentLines.length > 0) {
          subSections.push({
            heading: currentSubHeading,
            text: currentLines.join("\n"),
            parentHeading: section.heading,
          });
        }
        currentSubHeading = subMatch[1].trim();
        currentLines = [];
      } else {
        currentLines.push(line);
      }
    }
    if (currentLines.length > 0) {
      subSections.push({
        heading: currentSubHeading,
        text: currentLines.join("\n"),
        parentHeading: section.heading,
      });
    }

    // Merge adjacent tiny sub-sections
    let buffer = null;
    for (const sub of subSections) {
      if (!buffer) {
        buffer = { ...sub };
        continue;
      }
      const bufferLen = stripContent(buffer.text).length;
      const subLen = stripContent(sub.text).length;
      if (bufferLen < MIN_SECTION_CHARS || bufferLen + subLen < MIN_SECTION_CHARS * 2) {
        buffer.text += "\n\n### " + (sub.heading || "") + "\n" + sub.text;
      } else {
        result.push(buffer);
        buffer = { ...sub };
      }
    }
    if (buffer) result.push(buffer);
  }
  return result;
}

// ---------------------------------------------------------------------------
// 9. Main
// ---------------------------------------------------------------------------

function main() {
  const chapterFiles = parseChapterFiles();
  console.log(`Found ${chapterFiles.length} QMD files in config`);

  // Check for index-manual.qmd sourcing
  const configText = readFileSync(CONFIG, "utf-8");
  const indexSourceMatch = configText.match(/index-source:\s*(\S+)/);
  const indexSource = indexSourceMatch ? indexSourceMatch[1] : null;

  const entries = [];

  for (const qmdPath of chapterFiles) {
    // Resolve actual file path
    let filePath;
    if (qmdPath === "index.qmd" && indexSource) {
      filePath = resolve(ROOT, indexSource);
    } else {
      filePath = resolve(ROOT, qmdPath);
    }

    if (!existsSync(filePath)) {
      console.warn(`  SKIP (not found): ${filePath}`);
      continue;
    }

    const raw = readFileSync(filePath, "utf-8");
    const chapterTitle = resolveVars(extractTitle(raw) || basename(qmdPath, ".qmd"));

    // Determine URL base for this chapter
    let baseUrl;
    if (qmdPath === "index.qmd" && indexSource) {
      baseUrl = qmdToUrl(indexSource);
    } else {
      baseUrl = qmdToUrl(qmdPath);
    }

    const body = stripFrontmatter(raw);
    const rawSections = splitSections(body);
    const sections = chunkOversizedSections(rawSections);

    // Chapter slug for image matching
    const chapterSlug = basename(qmdPath, ".qmd");

    let sectionCount = 0;
    for (const section of sections) {
      const cleanedText = stripContent(section.text);
      if (!cleanedText || cleanedText.length < 20) continue;

      // Resolve vars in heading text
      const heading = resolveVars(section.heading);
      const sectionTitle = heading || chapterTitle;

      // For chunked sub-sections, use parent heading for anchor context
      const anchorHeading = section.parentHeading || section.heading;
      const href =
        anchorHeading === null || anchorHeading === undefined
          ? baseUrl
          : baseUrl + "#" + slugify(resolveVars(anchorHeading));

      entries.push({
        title: sectionTitle,
        section: chapterTitle,
        href: href,
        text: cleanedText,
        chapter: chapterSlug,
      });
      sectionCount++;
    }

    console.log(
      `  ${qmdPath}: ${sectionCount} entries` +
        (sections.length !== rawSections.length
          ? ` (${rawSections.length} sections, ${sections.length - rawSections.length + rawSections.filter(s => stripContent(s.text).length > MAX_SECTION_CHARS).length} chunked)`
          : "")
    );
  }

  // Write output (minified - not human-read, saves ~30-40%)
  const json = JSON.stringify(entries);
  writeFileSync(OUTPUT, json, "utf-8");

  const sizeKB = (Buffer.byteLength(json, "utf-8") / 1024).toFixed(1);
  console.log(`\nGenerated ${entries.length} entries -> ${OUTPUT}`);
  console.log(`File size: ${sizeKB} KB`);

  // Stats
  const lengths = entries.map((e) => e.text.length).sort((a, b) => a - b);
  const maxLen = lengths[lengths.length - 1];
  const over10k = lengths.filter((l) => l > MAX_SECTION_CHARS).length;
  console.log(
    `Max entry: ${maxLen} chars | Over ${MAX_SECTION_CHARS}: ${over10k}`
  );

  const dalyEntries = entries.filter(
    (e) => /daly|cost.per/i.test(e.text) || /daly|cost.per/i.test(e.title)
  );
  console.log(`Entries mentioning DALY or "cost per": ${dalyEntries.length}`);
}

main();
