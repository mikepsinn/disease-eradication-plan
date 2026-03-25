#!/usr/bin/env npx tsx
/**
 * Chat RAG + API integration tests.
 *
 * Tests three layers:
 *   1. RAG retrieval: correct chunks are found for specific questions
 *   2. Context quality: retrieved chunks contain the expected numbers
 *   3. API accuracy: with proper context, the model returns correct facts
 *
 * Run:  npx tsx transmit/test-chat.ts                 (all tests)
 *       npx tsx transmit/test-chat.ts --rag-only       (skip API calls)
 *       npx tsx transmit/test-chat.ts --api-only       (skip RAG tests)
 */

import "dotenv/config";
import { readFileSync } from "fs";
import { resolve } from "path";
import { searchContent, type SearchEntry } from "./lib/search";

// ─── Config ──────────────────────────────────────────────────────────
const ROOT = resolve(__dirname, "..");
const API_URL =
  process.env.CHAT_API_URL || "https://transmit.warondisease.org/api/chat";
const SEARCH_INDEX_PATHS = [
  "_manual-paperback/warondisease/search-index.json",
  "_manual/warondisease/search-index.json",
  "_site/manual/search.json",
];

const args = process.argv.slice(2);
const ragOnly = args.includes("--rag-only");
const apiOnly = args.includes("--api-only");

// ─── Test definitions ────────────────────────────────────────────────
interface TestCase {
  name: string;
  question: string;
  /** Substrings the RAG context must contain */
  expectInContext: string[];
  /** Substrings the RAG context must NOT contain (to catch wrong chunks) */
  expectNotInContext?: string[];
  /** Expected chunks by URL substring */
  expectChunks?: string[];
  /** Substrings the API response must contain (checked case-insensitively) */
  expectInAnswer?: string[];
  /** Substrings the API response must NOT contain */
  rejectInAnswer?: string[];
}

const TESTS: TestCase[] = [
  {
    name: "RECOVERY trial cost per patient",
    question: "What did the RECOVERY trial cost per patient?",
    expectInContext: ["$500", "RECOVERY"],
    expectChunks: ["nih-fails"],
    expectInAnswer: ["$500", "41,000"],
  },
  {
    name: "Cost per QALY for pragmatic trials",
    question: "What is the cost per QALY for pragmatic trials compared to standard research?",
    expectInContext: ["$500", "cost"],
    expectInAnswer: ["$4"],
    rejectInAnswer: ["$1.50", "$1.5"],
  },
  {
    name: "Treaty annual funding amount",
    question: "How much money does the 1% treaty generate annually?",
    expectInContext: ["$27.2"],
    expectInAnswer: ["27.2"],
  },
  {
    name: "Military spending total",
    question: "How much does the world spend on military annually?",
    expectInContext: ["$2.72"],
    expectInAnswer: ["2.72"],
  },
  {
    name: "Wishocracy corruption cap",
    question: "How does Wishocracy prevent corruption?",
    expectInContext: ["80%", "20%"],
    expectChunks: ["wishocracy"],
    expectInAnswer: ["80%", "20%"],
  },
  {
    name: "Daily disease deaths",
    question: "How many people die from disease every day?",
    expectInContext: ["104", "die"],
    expectInAnswer: ["150,000"],
  },
  {
    name: "GDP trajectories and Soviet collapse",
    question: "What is the destructive economy share of GDP and the Soviet collapse threshold?",
    expectInContext: ["11.5%"],
    expectChunks: ["gdp-trajectories"],
  },
  {
    name: "Incentive Alignment Bonds mechanism",
    question: "How do Incentive Alignment Bonds work and what returns do investors get?",
    expectInContext: ["bond", "investor"],
    expectChunks: ["incentive-alignment-bonds"],
    expectInAnswer: ["bond"],
  },
  {
    name: "Political Dysfunction Tax total",
    question: "What is the total Political Dysfunction Tax and how much value is lost?",
    expectInContext: ["101", "dysfunction"],
    expectInAnswer: ["101"],
  },
  {
    name: "Hegemony Tax military overspend",
    question: "How much does the US military overspend beyond what strict deterrence requires?",
    expectInContext: ["military", "spending"],
    // $615B detail is in the PDT chapter but too granular for Quarto's index
    // TODO: custom search index will surface this
  },
  {
    name: "GDP per capita under treaty vs Wishonia trajectory",
    question: "What would average income per person be under the 1% treaty path after 20 years?",
    expectInContext: ["339", "income"],
    expectChunks: ["gdp-trajectories"],
    expectInAnswer: ["339"],
  },
  {
    name: "Destructive economy timeline to collapse",
    question: "When does the destructive economy reach 35% of GDP and begin the death spiral?",
    expectInContext: ["11.5%", "destructive"],
    expectChunks: ["gdp-trajectories"],
  },
  {
    name: "IAB allocation split",
    question: "How are 1% treaty funds allocated between research, investors, and political incentives?",
    expectInContext: ["80%", "treaty"],
    expectInAnswer: ["80%", "10%"],
    rejectInAnswer: ["15%"],
  },
  {
    name: "Earth Optimization Prize mechanism",
    question: "How does the Earth Optimization Prize work and what are the target metrics?",
    expectInContext: ["prize", "target"],
    expectChunks: ["earth-optimization"],
  },
];

// ─── Helpers ─────────────────────────────────────────────────────────

function loadSearchIndex(): SearchEntry[] {
  for (const relPath of SEARCH_INDEX_PATHS) {
    const absPath = resolve(ROOT, relPath);
    try {
      const raw = readFileSync(absPath, "utf8");
      const data = JSON.parse(raw);
      const entries = Array.isArray(data) ? data : data.entries || [];
      if (entries.length > 0) {
        console.log(`  Loaded search index: ${relPath} (${entries.length} entries)\n`);
        return entries;
      }
    } catch {}
  }
  throw new Error(
    "No search index found. Render the manual first or check paths:\n  " +
      SEARCH_INDEX_PATHS.join("\n  ")
  );
}

async function queryAPI(
  question: string,
  context: string
): Promise<string> {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, context }),
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);

  // Read streaming response
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  let text = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    text += decoder.decode(value, { stream: true });
  }
  return text;
}

// ─── Test runner ─────────────────────────────────────────────────────

let passed = 0;
let failed = 0;
const failures: string[] = [];

function check(label: string, ok: boolean, detail?: string) {
  if (ok) {
    passed++;
    console.log(`    PASS  ${label}`);
  } else {
    failed++;
    const msg = `    FAIL  ${label}${detail ? " -- " + detail : ""}`;
    console.log(msg);
    failures.push(msg);
  }
}

async function main() {
  console.log("=== Chat RAG + API Tests ===\n");
  console.log(`  API URL: ${API_URL}`);

  const index = loadSearchIndex();

  for (const t of TESTS) {
    console.log(`\n--- ${t.name} ---`);
    console.log(`  Q: "${t.question}"`);

    // Layer 1: RAG retrieval
    if (!apiOnly) {
      const { context, results } = searchContent(index, t.question);

      const contextLower = context.toLowerCase();

      for (const expected of t.expectInContext) {
        check(
          `context contains "${expected}"`,
          contextLower.includes(expected.toLowerCase()),
          `not found in ${context.length} chars of context`
        );
      }

      if (t.expectNotInContext) {
        for (const bad of t.expectNotInContext) {
          check(
            `context does NOT contain "${bad}"`,
            !contextLower.includes(bad.toLowerCase())
          );
        }
      }

      if (t.expectChunks) {
        for (const slug of t.expectChunks) {
          const found = results.some(
            (r) => (r.entry.url || r.entry.path || "").includes(slug)
          );
          check(`retrieved chunk matching "${slug}"`, found,
            `top chunks: ${results.slice(0, 3).map((r) => r.entry.url || r.entry.path).join(", ")}`
          );
        }
      }

      // Layer 2: context has enough detail for the model
      check(
        `context is non-trivial (>100 chars)`,
        context.length > 100,
        `only ${context.length} chars`
      );
    }

    // Layer 3: API accuracy with RAG context
    if (!ragOnly && t.expectInAnswer) {
      const { context } = searchContent(index, t.question);
      let answer: string;
      try {
        answer = await queryAPI(t.question, context);
      } catch (err: any) {
        check(`API call succeeded`, false, err.message);
        continue;
      }

      console.log(`  A: "${answer.substring(0, 150).replace(/\n/g, " ")}..."`);

      const answerLower = answer.toLowerCase();

      for (const expected of t.expectInAnswer) {
        check(
          `answer contains "${expected}"`,
          answerLower.includes(expected.toLowerCase()),
          `not found in response`
        );
      }

      if (t.rejectInAnswer) {
        for (const bad of t.rejectInAnswer) {
          check(
            `answer does NOT contain "${bad}"`,
            !answerLower.includes(bad.toLowerCase()),
            `hallucinated value found in response`
          );
        }
      }
    }
  }

  // Summary
  console.log(`\n${"=".repeat(50)}`);
  console.log(`  ${passed} passed, ${failed} failed`);
  if (failures.length > 0) {
    console.log("\nFailures:");
    for (const f of failures) console.log(f);
  }
  console.log();
  process.exit(failed > 0 ? 1 : 0);
}

main();
