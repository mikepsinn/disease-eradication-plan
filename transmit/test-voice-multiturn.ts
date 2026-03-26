#!/usr/bin/env npx tsx
/**
 * Multi-turn Gemini Live WebSocket test.
 *
 * Verifies that the Gemini Live API handles multiple back-to-back
 * text exchanges over a single WebSocket connection. This catches
 * the "only responds to first question" bug at the protocol level.
 *
 * Run:  npx tsx transmit/test-voice-multiturn.ts
 */

import "dotenv/config";
import { readFileSync } from "fs";
import { resolve } from "path";
import WebSocket from "ws";
import { searchContent, type SearchEntry } from "./lib/search";

// ─── Config ──────────────────────────────────────────────────────────
const API_KEY = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
const WS_URL =
  "wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent";
const TURN_TIMEOUT_MS = 30_000;
const ROOT = resolve(__dirname, "..");

const QUESTIONS = [
  "How much does the world spend on military annually?",
  "How many people die from disease every day?",
];

// ─── Helpers ─────────────────────────────────────────────────────────
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

function loadSearchIndex(): SearchEntry[] {
  const absPath = resolve(ROOT, "assets/json/search-index.json");
  const raw = readFileSync(absPath, "utf8");
  const data = JSON.parse(raw);
  return Array.isArray(data) ? data : data.entries || [];
}

interface TurnResult {
  audioChunks: number;
  outputTranscript: string;
  inputTranscript: string;
  interrupted: boolean;
}

function sendSetup(ws: WebSocket) {
  ws.send(
    JSON.stringify({
      setup: {
        model: "models/gemini-2.5-flash-native-audio-latest",
        generationConfig: {
          responseModalities: ["AUDIO"],
          speechConfig: {
            voiceConfig: {
              prebuiltVoiceConfig: { voiceName: "Kore" },
            },
          },
        },
        systemInstruction: {
          parts: [
            {
              text: "You are Wishonia, an alien who has been watching Earth since 1945. Keep answers short (1-2 sentences).",
            },
          ],
        },
        realtimeInputConfig: {
          automaticActivityDetection: {
            disabled: false,
            startOfSpeechSensitivity: "START_SENSITIVITY_LOW",
            endOfSpeechSensitivity: "END_SENSITIVITY_LOW",
            prefixPaddingMs: 200,
            silenceDurationMs: 2000,
          },
        },
        outputAudioTranscription: {},
        inputAudioTranscription: {},
      },
    })
  );
}

function sendText(ws: WebSocket, text: string) {
  ws.send(
    JSON.stringify({
      clientContent: {
        turns: [{ role: "user", parts: [{ text }] }],
        turnComplete: true,
      },
    })
  );
}

function waitForSetup(ws: WebSocket): Promise<void> {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(
      () => reject(new Error("Setup timed out")),
      10_000
    );
    const handler = (data: WebSocket.Data) => {
      const msg = JSON.parse(data.toString());
      if (msg.setupComplete) {
        clearTimeout(timeout);
        ws.off("message", handler);
        resolve();
      }
    };
    ws.on("message", handler);
  });
}

function waitForTurn(ws: WebSocket): Promise<TurnResult> {
  return new Promise((resolve, reject) => {
    const result: TurnResult = {
      audioChunks: 0,
      outputTranscript: "",
      inputTranscript: "",
      interrupted: false,
    };

    const timeout = setTimeout(
      () => reject(new Error("Turn timed out after " + TURN_TIMEOUT_MS + "ms")),
      TURN_TIMEOUT_MS
    );

    const handler = (data: WebSocket.Data) => {
      const msg = JSON.parse(data.toString());

      // Input transcript (at top level or in serverContent)
      if (msg.inputTranscript) {
        result.inputTranscript += msg.inputTranscript;
      }

      const sc = msg.serverContent;
      if (!sc) return;

      if (sc.inputTranscript) {
        result.inputTranscript += sc.inputTranscript;
      }

      if (sc.outputTranscript) {
        result.outputTranscript += sc.outputTranscript;
      }

      if (sc.interrupted) {
        result.interrupted = true;
        clearTimeout(timeout);
        ws.off("message", handler);
        resolve(result);
        return;
      }

      if (sc.modelTurn && sc.modelTurn.parts) {
        for (const part of sc.modelTurn.parts) {
          if (part.inlineData && part.inlineData.data) {
            result.audioChunks++;
          }
        }
      }

      if (sc.turnComplete) {
        clearTimeout(timeout);
        ws.off("message", handler);
        resolve(result);
      }
    };

    ws.on("message", handler);
  });
}

// ─── Main ────────────────────────────────────────────────────────────
async function main() {
  console.log("=== Multi-Turn Gemini Live WebSocket Test ===\n");

  if (!API_KEY) {
    console.log("  SKIP  GOOGLE_GENERATIVE_AI_API_KEY not set");
    process.exit(0);
  }

  // Load search index for RAG context
  let index: SearchEntry[];
  try {
    index = loadSearchIndex();
    console.log(`  Loaded search index (${index.length} entries)\n`);
  } catch (err: any) {
    console.log(`  SKIP  No search index: ${err.message}`);
    process.exit(0);
  }

  // Connect
  console.log("--- Connecting to Gemini Live ---");
  const ws = new WebSocket(WS_URL + "?key=" + encodeURIComponent(API_KEY));

  await new Promise<void>((resolve, reject) => {
    ws.on("open", resolve);
    ws.on("error", reject);
  });
  check("WebSocket connected", true);

  // Setup
  sendSetup(ws);
  await waitForSetup(ws);
  check("Setup complete", true);

  // Turn 1
  console.log(`\n--- Turn 1: "${QUESTIONS[0]}" ---`);
  const { context: ctx1 } = searchContent(index, QUESTIONS[0]);
  const combined1 =
    'The user asked: "' +
    QUESTIONS[0] +
    '"\n\nReference material:\n' +
    ctx1 +
    "\n\nAnswer briefly.";
  sendText(ws, combined1);

  let turn1: TurnResult;
  try {
    turn1 = await waitForTurn(ws);
    check("Turn 1 got response", true);
    check(
      "Turn 1 has audio or transcript",
      turn1.audioChunks > 0 || turn1.outputTranscript.length > 0,
      `audio=${turn1.audioChunks}, transcript=${turn1.outputTranscript.length} chars`
    );
    if (turn1.outputTranscript) {
      console.log(
        `  Transcript: "${turn1.outputTranscript.substring(0, 100)}..."`
      );
    }
  } catch (err: any) {
    check("Turn 1 got response", false, err.message);
    ws.close();
    printSummary();
    return;
  }

  // Turn 2 - the critical test: does the second question get a response?
  console.log(`\n--- Turn 2: "${QUESTIONS[1]}" ---`);
  const { context: ctx2 } = searchContent(index, QUESTIONS[1]);
  const combined2 =
    'The user asked: "' +
    QUESTIONS[1] +
    '"\n\nReference material:\n' +
    ctx2 +
    "\n\nAnswer briefly.";
  sendText(ws, combined2);

  let turn2: TurnResult;
  try {
    turn2 = await waitForTurn(ws);
    check("Turn 2 got response", true);
    check(
      "Turn 2 has audio or transcript",
      turn2.audioChunks > 0 || turn2.outputTranscript.length > 0,
      `audio=${turn2.audioChunks}, transcript=${turn2.outputTranscript.length} chars`
    );
    if (turn2.outputTranscript) {
      console.log(
        `  Transcript: "${turn2.outputTranscript.substring(0, 100)}..."`
      );
    }
  } catch (err: any) {
    check("Turn 2 got response", false, err.message);
  }

  // Verify WebSocket stayed open
  check("WebSocket still open", ws.readyState === WebSocket.OPEN);

  ws.close();
  printSummary();
}

function printSummary() {
  console.log(`\n${"=".repeat(50)}`);
  console.log(`  ${passed} passed, ${failed} failed`);
  if (failures.length > 0) {
    console.log("\nFailures:");
    for (const f of failures) console.log(f);
  }
  console.log();
  process.exit(failed > 0 ? 1 : 0);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
