#!/usr/bin/env tsx

import * as fs from 'fs';
import * as path from 'path';
import { distance as levenshteinDistance } from 'fastest-levenshtein';

interface DuplicateInstance {
  file: string;
  line: number;
  context: string;
}

interface DuplicateEntry {
  text: string;
  count: number;
  instances: DuplicateInstance[];
  similarity?: number; // For near-duplicates
}

interface PhraseEntry {
  phrase: string;
  count: number;
  instances: DuplicateInstance[];
}

// Configuration
const SIMILARITY_THRESHOLD = 0.90; // 90% similar for near-duplicates
const MIN_PHRASE_LENGTH = 4; // Minimum words in a phrase (reduced from 3 for performance)
const MAX_PHRASE_LENGTH = 7; // Maximum words in a phrase (reduced from 10 for performance)
const MIN_PHRASE_OCCURRENCES = 3; // Minimum times a phrase should appear (increased to reduce noise)

// Normalize text for comparison
function normalizeText(text: string): string {
  return text
    .toLowerCase()
    .replace(/[""]/g, '"')
    .replace(/['']/g, "'")
    .replace(/\s+/g, ' ')
    .trim();
}

// Calculate similarity between two strings (0-1)
function calculateSimilarity(str1: string, str2: string): number {
  const maxLen = Math.max(str1.length, str2.length);
  if (maxLen === 0) return 1.0;
  const dist = levenshteinDistance(str1, str2);
  return 1 - dist / maxLen;
}

// Extract sentences from text
function extractSentences(text: string): string[] {
  // Split on sentence boundaries but preserve some context
  return text
    .split(/[.!?]+\s+/)
    .map(s => s.trim())
    .filter(s => s.length > 20); // Ignore very short sentences
}

// Extract paragraphs from text
function extractParagraphs(text: string): string[] {
  return text
    .split(/\n\s*\n/)
    .map(p => p.replace(/\n/g, ' ').trim())
    .filter(p => p.length > 50); // Ignore very short paragraphs
}

// Extract n-grams (phrases of n words)
function extractNGrams(text: string, n: number): string[] {
  const words = text.toLowerCase().split(/\s+/);
  const ngrams: string[] = [];

  for (let i = 0; i <= words.length - n; i++) {
    const ngram = words.slice(i, i + n).join(' ');
    // Filter out ngrams with too many common words or special characters
    if (ngram.length > 15 && !ngram.match(/^(the|a|an|and|or|but|in|on|at|to|for|of|with|by)\s/)) {
      ngrams.push(ngram);
    }
  }

  return ngrams;
}

// Read all .qmd files
function findQmdFiles(dir: string): string[] {
  const files: string[] = [];

  function traverse(currentDir: string) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);

      if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
        traverse(fullPath);
      } else if (entry.isFile() && entry.name.endsWith('.qmd')) {
        // Skip references.qmd
        if (!fullPath.includes('references.qmd')) {
          files.push(fullPath);
        }
      }
    }
  }

  traverse(dir);
  return files;
}

// Find exact duplicates
function findExactDuplicates(items: Map<string, DuplicateInstance[]>): DuplicateEntry[] {
  const duplicates: DuplicateEntry[] = [];

  for (const [text, instances] of items.entries()) {
    if (instances.length > 1) {
      duplicates.push({
        text,
        count: instances.length,
        instances: instances.sort((a, b) => a.file.localeCompare(b.file))
      });
    }
  }

  return duplicates.sort((a, b) => b.count - a.count);
}

// Find near-duplicates
function findNearDuplicates(sentences: Map<string, DuplicateInstance[]>): DuplicateEntry[] {
  const allSentences = Array.from(sentences.keys());
  const nearDuplicates: DuplicateEntry[] = [];
  const processed = new Set<string>();

  for (let i = 0; i < allSentences.length; i++) {
    // Show progress every 100 sentences
    if (i % 100 === 0 && i > 0) {
      console.log(`      Comparing sentence ${i}/${allSentences.length} (${Math.round(i / allSentences.length * 100)}%)`);
    }

    if (processed.has(allSentences[i])) continue;

    const similar: { text: string; similarity: number }[] = [];

    for (let j = i + 1; j < allSentences.length; j++) {
      if (processed.has(allSentences[j])) continue;

      const similarity = calculateSimilarity(allSentences[i], allSentences[j]);

      if (similarity >= SIMILARITY_THRESHOLD && similarity < 1.0) {
        similar.push({ text: allSentences[j], similarity });
      }
    }

    if (similar.length > 0) {
      const instances = sentences.get(allSentences[i]) || [];
      similar.forEach(s => {
        instances.push(...(sentences.get(s.text) || []));
        processed.add(s.text);
      });

      nearDuplicates.push({
        text: allSentences[i],
        count: instances.length,
        instances: instances.sort((a, b) => a.file.localeCompare(b.file)),
        similarity: Math.max(...similar.map(s => s.similarity))
      });

      processed.add(allSentences[i]);
    }
  }

  return nearDuplicates.sort((a, b) => b.count - a.count);
}

// Generate HTML report
function generateHTMLReport(
  exactSentences: DuplicateEntry[],
  nearSentences: DuplicateEntry[],
  exactParagraphs: DuplicateEntry[],
  phrases: PhraseEntry[],
  outputPath: string
): void {
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Book Duplication Analysis</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
      background: #f5f5f5;
    }
    h1 { color: #333; border-bottom: 3px solid #007acc; padding-bottom: 10px; }
    h2 { color: #555; margin-top: 40px; border-left: 4px solid #007acc; padding-left: 12px; }
    .summary {
      background: white;
      padding: 20px;
      border-radius: 8px;
      margin: 20px 0;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stat {
      display: inline-block;
      margin: 10px 20px 10px 0;
      padding: 10px 15px;
      background: #007acc;
      color: white;
      border-radius: 4px;
      font-weight: bold;
    }
    .duplicate-item {
      background: white;
      margin: 15px 0;
      padding: 15px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      border-left: 4px solid #dc3545;
    }
    .near-duplicate {
      border-left-color: #ffc107;
    }
    .phrase-item {
      border-left-color: #17a2b8;
    }
    .duplicate-text {
      font-size: 1.1em;
      margin-bottom: 10px;
      padding: 10px;
      background: #f8f9fa;
      border-radius: 4px;
    }
    .count {
      display: inline-block;
      background: #dc3545;
      color: white;
      padding: 4px 12px;
      border-radius: 12px;
      font-weight: bold;
      margin-right: 10px;
    }
    .similarity {
      display: inline-block;
      background: #ffc107;
      color: #333;
      padding: 4px 12px;
      border-radius: 12px;
      font-weight: bold;
      margin-right: 10px;
    }
    .instance {
      margin: 8px 0;
      padding: 8px;
      background: #e9ecef;
      border-radius: 4px;
      font-size: 0.9em;
    }
    .file-path {
      color: #007acc;
      font-family: 'Courier New', monospace;
      font-weight: bold;
    }
    .context {
      color: #666;
      font-style: italic;
      margin-top: 4px;
    }
    .tabs {
      display: flex;
      gap: 10px;
      margin: 20px 0;
    }
    .tab {
      padding: 10px 20px;
      background: white;
      border: 2px solid #007acc;
      border-radius: 4px;
      cursor: pointer;
      font-weight: bold;
      color: #007acc;
    }
    .tab.active {
      background: #007acc;
      color: white;
    }
    .tab-content {
      display: none;
    }
    .tab-content.active {
      display: block;
    }
    .filter {
      margin: 20px 0;
      padding: 15px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .filter input {
      padding: 8px 12px;
      border: 1px solid #ddd;
      border-radius: 4px;
      width: 100%;
      font-size: 1em;
    }
  </style>
</head>
<body>
  <h1>📚 Book Duplication Analysis</h1>

  <div class="summary">
    <div class="stat">Exact Duplicate Sentences: ${exactSentences.length}</div>
    <div class="stat">Near-Duplicate Sentences: ${nearSentences.length}</div>
    <div class="stat">Duplicate Paragraphs: ${exactParagraphs.length}</div>
    <div class="stat">Repeated Phrases: ${phrases.length}</div>
  </div>

  <div class="tabs">
    <div class="tab active" onclick="showTab('exact')">Exact Duplicates (${exactSentences.length})</div>
    <div class="tab" onclick="showTab('near')">Near Duplicates (${nearSentences.length})</div>
    <div class="tab" onclick="showTab('paragraphs')">Duplicate Paragraphs (${exactParagraphs.length})</div>
    <div class="tab" onclick="showTab('phrases')">Repeated Phrases (${phrases.length})</div>
  </div>

  <div id="exact" class="tab-content active">
    <h2>Exact Duplicate Sentences</h2>
    <div class="filter">
      <input type="text" id="exactFilter" placeholder="Filter duplicates..." onkeyup="filterItems('exact')">
    </div>
    <div id="exactContent">
      ${generateDuplicateHTML(exactSentences, false)}
    </div>
  </div>

  <div id="near" class="tab-content">
    <h2>Near-Duplicate Sentences (${SIMILARITY_THRESHOLD * 100}%+ similar)</h2>
    <div class="filter">
      <input type="text" id="nearFilter" placeholder="Filter near-duplicates..." onkeyup="filterItems('near')">
    </div>
    <div id="nearContent">
      ${generateDuplicateHTML(nearSentences, true)}
    </div>
  </div>

  <div id="paragraphs" class="tab-content">
    <h2>Duplicate Paragraphs</h2>
    <div class="filter">
      <input type="text" id="paragraphsFilter" placeholder="Filter paragraphs..." onkeyup="filterItems('paragraphs')">
    </div>
    <div id="paragraphsContent">
      ${generateDuplicateHTML(exactParagraphs, false)}
    </div>
  </div>

  <div id="phrases" class="tab-content">
    <h2>Repeated Phrases</h2>
    <div class="filter">
      <input type="text" id="phrasesFilter" placeholder="Filter phrases..." onkeyup="filterItems('phrases')">
    </div>
    <div id="phrasesContent">
      ${generatePhrasesHTML(phrases)}
    </div>
  </div>

  <script>
    function showTab(tabName) {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      event.target.classList.add('active');
      document.getElementById(tabName).classList.add('active');
    }

    function filterItems(section) {
      const input = document.getElementById(section + 'Filter');
      const filter = input.value.toLowerCase();
      const content = document.getElementById(section + 'Content');
      const items = content.getElementsByClassName('duplicate-item');

      for (let item of items) {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(filter) ? '' : 'none';
      }
    }
  </script>
</body>
</html>`;

  fs.writeFileSync(outputPath, html, 'utf-8');
}

function generateDuplicateHTML(duplicates: DuplicateEntry[], showSimilarity: boolean): string {
  return duplicates.map(dup => `
    <div class="duplicate-item ${showSimilarity ? 'near-duplicate' : ''}">
      <div class="duplicate-text">${escapeHtml(dup.text)}</div>
      <div>
        <span class="count">${dup.count} occurrences</span>
        ${showSimilarity && dup.similarity ? `<span class="similarity">${(dup.similarity * 100).toFixed(1)}% similar</span>` : ''}
      </div>
      ${dup.instances.map(inst => `
        <div class="instance">
          <div class="file-path">${escapeHtml(inst.file)}:${inst.line}</div>
          <div class="context">${escapeHtml(inst.context.substring(0, 200))}...</div>
        </div>
      `).join('')}
    </div>
  `).join('');
}

function generatePhrasesHTML(phrases: PhraseEntry[]): string {
  return phrases.map(phrase => `
    <div class="duplicate-item phrase-item">
      <div class="duplicate-text">"${escapeHtml(phrase.phrase)}"</div>
      <div>
        <span class="count">${phrase.count} occurrences</span>
      </div>
      ${phrase.instances.slice(0, 10).map(inst => `
        <div class="instance">
          <div class="file-path">${escapeHtml(inst.file)}</div>
        </div>
      `).join('')}
      ${phrase.instances.length > 10 ? `<div class="instance">... and ${phrase.instances.length - 10} more</div>` : ''}
    </div>
  `).join('');
}

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// Main execution
async function main() {
  console.log('🔍 Analyzing book for duplicates and redundancy...\n');

  const rootDir = process.cwd();
  const files = findQmdFiles(rootDir);

  console.log(`📁 Found ${files.length} .qmd files`);

  const sentences = new Map<string, DuplicateInstance[]>();
  const paragraphs = new Map<string, DuplicateInstance[]>();
  const phrases = new Map<string, DuplicateInstance[]>();

  // Process each file
  console.log('\n📖 Processing files...\n');
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const content = fs.readFileSync(file, 'utf-8');
    const lines = content.split('\n');
    const relativePath = path.relative(rootDir, file);

    // Show progress for every file
    console.log(`   [${i + 1}/${files.length}] ${relativePath}`);

    // Extract and store sentences
    const fileSentences = extractSentences(content);
    fileSentences.forEach((sentence, idx) => {
      const normalized = normalizeText(sentence);
      if (!sentences.has(normalized)) {
        sentences.set(normalized, []);
      }

      const lineNum = findLineNumber(lines, sentence);
      sentences.get(normalized)!.push({
        file: relativePath,
        line: lineNum,
        context: sentence
      });
    });

    // Extract and store paragraphs
    const fileParagraphs = extractParagraphs(content);
    fileParagraphs.forEach((paragraph) => {
      const normalized = normalizeText(paragraph);
      if (!paragraphs.has(normalized)) {
        paragraphs.set(normalized, []);
      }

      const lineNum = findLineNumber(lines, paragraph.substring(0, 50));
      paragraphs.get(normalized)!.push({
        file: relativePath,
        line: lineNum,
        context: paragraph
      });
    });

    // Extract and store phrases (n-grams)
    // Note: We skip line number lookups for phrases for performance
    for (let n = MIN_PHRASE_LENGTH; n <= MAX_PHRASE_LENGTH; n++) {
      const ngrams = extractNGrams(content, n);
      ngrams.forEach((ngram) => {
        if (!phrases.has(ngram)) {
          phrases.set(ngram, []);
        }

        phrases.get(ngram)!.push({
          file: relativePath,
          line: 0, // Line number skipped for performance
          context: ngram
        });
      });
    }
  }

  console.log(`\n✅ Processed ${files.length} files`);
  console.log(`   • Collected ${sentences.size} unique sentences`);
  console.log(`   • Collected ${paragraphs.size} unique paragraphs`);
  console.log(`   • Collected ${phrases.size} unique phrases\n`);

  console.log('📊 Processing duplicates...');

  // Find exact duplicates
  const exactSentences = findExactDuplicates(sentences);
  console.log(`   ✓ Found ${exactSentences.length} exact duplicate sentences`);

  // Find near-duplicates
  console.log('   🔄 Finding near-duplicates (this may take a moment)...');
  const nearSentences = findNearDuplicates(sentences);
  console.log(`   ✓ Found ${nearSentences.length} near-duplicate sentence groups`);

  // Find duplicate paragraphs
  const exactParagraphs = findExactDuplicates(paragraphs);
  console.log(`   ✓ Found ${exactParagraphs.length} duplicate paragraphs`);

  // Find repeated phrases
  console.log(`\n   📝 Analyzing ${phrases.size} unique phrases...`);
  const repeatedPhrases = Array.from(phrases.entries())
    .filter(([_, instances]) => instances.length >= MIN_PHRASE_OCCURRENCES)
    .map(([phrase, instances]) => ({
      phrase,
      count: instances.length,
      instances
    }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 200); // Top 200 most repeated phrases

  console.log(`   ✓ Found ${repeatedPhrases.length} repeated phrases\n`);

  // Generate report
  const outputPath = path.join(rootDir, 'duplication-report.html');
  generateHTMLReport(exactSentences, nearSentences, exactParagraphs, repeatedPhrases, outputPath);

  console.log(`✅ Report generated: ${outputPath}`);
  console.log('\n📈 Summary:');
  console.log(`   • Exact duplicate sentences: ${exactSentences.length}`);
  console.log(`   • Near-duplicate sentences: ${nearSentences.length}`);
  console.log(`   • Duplicate paragraphs: ${exactParagraphs.length}`);
  console.log(`   • Repeated phrases: ${repeatedPhrases.length}`);
}

function findLineNumber(lines: string[], searchText: string): number {
  const normalized = normalizeText(searchText);
  for (let i = 0; i < lines.length; i++) {
    if (normalizeText(lines[i]).includes(normalized.substring(0, 30))) {
      return i + 1;
    }
  }
  return 1;
}

main().catch(console.error);
