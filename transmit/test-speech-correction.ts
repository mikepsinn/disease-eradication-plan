/**
 * Test: speech-to-text correction + RAG search
 *
 * Simulates likely STT misrecognitions and verifies that
 * correctTranscript() + searchContent() finds the right content.
 *
 * Run: npx tsx transmit/test-speech-correction.ts
 */

import { readFileSync } from "fs";
import { resolve } from "path";
import { correctTranscript, searchContent, type SearchEntry } from "./lib/search";

const indexPath = resolve(__dirname, "../assets/json/search-index.json");
let index: SearchEntry[];
try {
  index = JSON.parse(readFileSync(indexPath, "utf-8"));
} catch {
  console.error("Could not load search index at", indexPath);
  process.exit(1);
}

console.log(`Loaded ${index.length} search index entries\n`);

// ── Test correctTranscript ──

const transcriptTests: Array<[string, string, string]> = [
  // [input, expected output, description]
  ["what is optometran", "what is Optimitron", "optometran → Optimitron"],
  ["tell me about opt a metron", "tell me about Optimitron", "opt a metron → Optimitron"],
  ["what is op democracy", "what is Optimocracy", "op democracy → Optimocracy"],
  ["how does wish own ya work", "how does Wishonia work", "wish own ya → Wishonia"],
  ["explain wish ocracy", "explain Wishocracy", "wish ocracy → Wishocracy"],
  ["what is the one percent treaty", "what is the 1% Treaty", "one percent treaty → 1% Treaty"],
  ["what is d f d a", "what is DFDA", "d f d a → DFDA"],
  // Should NOT correct these (no false positives)
  ["what is democracy", "what is democracy", "democracy unchanged"],
  ["I wish on a star", "I wish on a star", "wish on a star unchanged"],
  ["daily exercise routine", "daily exercise routine", "daily without medical context unchanged"],
  ["optimize the budget", "optimize the budget", "optimize unchanged"],
];

let passed = 0;
let failed = 0;

console.log("=== correctTranscript tests ===\n");
for (const [input, expected, desc] of transcriptTests) {
  const result = correctTranscript(input);
  const ok = result === expected;
  if (ok) {
    passed++;
    console.log(`  PASS: ${desc}`);
  } else {
    failed++;
    console.log(`  FAIL: ${desc}`);
    console.log(`        input:    "${input}"`);
    console.log(`        expected: "${expected}"`);
    console.log(`        got:      "${result}"`);
  }
}

// ── Test RAG search with corrected queries ──

console.log("\n=== RAG search tests (correction + search) ===\n");

const searchTests: Array<[string, string[], string]> = [
  // [voice input (as STT would produce), expected title substrings in results, description]
  ["what is optometran", ["optimitron", "optimal", "policy"], "misrecognized Optimitron finds results"],
  ["tell me about op democracy", ["optimocracy", "governance", "optimal"], "misrecognized Optimocracy finds results"],
  ["how does wish ocracy work", ["wishocracy", "allocat"], "misrecognized Wishocracy finds results"],
  ["what is the one percent treaty", ["treaty", "military", "1%"], "one percent treaty finds results"],
  ["what is optimitron", ["optimitron", "optimal", "policy"], "correct Optimitron also works"],
];

for (const [voiceInput, expectedHits, desc] of searchTests) {
  const { context, results } = searchContent(index, voiceInput);
  const titles = results.map(r => (r.entry.title || "").toLowerCase());
  const allText = context.toLowerCase();

  // Check if any expected substring appears in titles or full context
  const foundAny = expectedHits.some(
    hit => titles.some(t => t.includes(hit)) || allText.includes(hit)
  );

  if (foundAny && results.length > 0) {
    passed++;
    console.log(`  PASS: ${desc} (${results.length} results, top: "${results[0].entry.title}")`);
  } else {
    failed++;
    console.log(`  FAIL: ${desc}`);
    console.log(`        query: "${voiceInput}" → corrected: "${correctTranscript(voiceInput)}"`);
    console.log(`        results: ${results.length}`);
    if (results.length > 0) {
      console.log(`        top titles: ${titles.slice(0, 3).join(", ")}`);
    }
  }
}

// ── Summary ──

console.log(`\n${"=".repeat(40)}`);
console.log(`${passed} passed, ${failed} failed, ${passed + failed} total`);
if (failed > 0) process.exit(1);
