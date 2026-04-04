#!/usr/bin/env npx tsx
/**
 * Timing comparison: /api/chat vs /api/visuals
 *
 * Fires both endpoints (same question, same context) and reports:
 *   - Time to first byte (TTFB)
 *   - Total response time
 *   - Response size
 *
 * Run:  npx tsx transmit/test-timing.ts
 */

import "dotenv/config";
import { readFileSync } from "fs";
import { resolve } from "path";
import { searchContent, type SearchEntry } from "./lib/search";

const ROOT = resolve(__dirname, "..");
const API_URL =
  process.env.CHAT_API_URL || "https://transmit.warondisease.org/api/chat";
const VISUALS_API_URL =
  process.env.VISUALS_API_URL || "https://transmit.warondisease.org/api/visuals";

const QUESTION = process.argv[2] || "How many lives would the 1% treaty save?";

function loadSearchIndex(): SearchEntry[] {
  const absPath = resolve(ROOT, "assets/json/search-index.json");
  const raw = readFileSync(absPath, "utf8");
  const data = JSON.parse(raw);
  return Array.isArray(data) ? data : data.entries || [];
}

async function timeChat(question: string, context: string) {
  const start = performance.now();
  let ttfb = 0;

  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, context }),
  });

  if (!res.ok) throw new Error(`Chat API ${res.status}: ${await res.text()}`);

  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  let text = "";
  let firstChunk = true;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    if (firstChunk) {
      ttfb = performance.now() - start;
      firstChunk = false;
    }
    text += decoder.decode(value, { stream: true });
  }

  const total = performance.now() - start;
  return { ttfb, total, size: text.length, preview: text.substring(0, 120) };
}

async function timeVisuals(question: string, context: string) {
  const start = performance.now();

  const res = await fetch(VISUALS_API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, context, imageOptions: [] }),
  });

  if (!res.ok) throw new Error(`Visuals API ${res.status}: ${await res.text()}`);

  const body = await res.text();
  const total = performance.now() - start;
  const parsed = JSON.parse(body);
  const fields = Object.keys(parsed).filter(
    (k) => parsed[k] !== null && parsed[k] !== undefined
  );

  return { ttfb: total, total, size: body.length, fields, preview: body.substring(0, 120) };
}

async function main() {
  console.log("=== Endpoint Timing Comparison ===\n");
  console.log(`Question: "${QUESTION}"\n`);

  const index = loadSearchIndex();
  const { context } = searchContent(index, QUESTION);
  console.log(`Context length: ${context.length} chars\n`);

  // Fire both in parallel (same as the client does)
  const [chat, visuals] = await Promise.all([
    timeChat(QUESTION, context),
    timeVisuals(QUESTION, context),
  ]);

  console.log("--- /api/chat (streaming text) ---");
  console.log(`  TTFB:      ${chat.ttfb.toFixed(0)} ms`);
  console.log(`  Total:     ${chat.total.toFixed(0)} ms`);
  console.log(`  Size:      ${chat.size} chars`);
  console.log(`  Preview:   "${chat.preview}..."\n`);

  console.log("--- /api/visuals (JSON) ---");
  console.log(`  Total:     ${visuals.total.toFixed(0)} ms`);
  console.log(`  Size:      ${visuals.size} chars`);
  console.log(`  Fields:    ${visuals.fields.join(", ")}`);
  console.log(`  Preview:   "${visuals.preview}..."\n`);

  const ratio = chat.total / visuals.total;
  console.log(`=== Chat is ${ratio.toFixed(1)}x ${ratio > 1 ? "slower" : "faster"} than visuals ===`);
  console.log(`    Chat TTFB: ${chat.ttfb.toFixed(0)} ms (time before first token streams)`);
  console.log(`    Difference: ${(chat.total - visuals.total).toFixed(0)} ms\n`);
}

main();
