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
  { q: "What is the 1% treaty?", expectInTranscript: ["1%", "treaty"] },
  { q: "How many people die from disease every day?", expectInTranscript: ["150"] },
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

    let turnDone = false;

    const handler = (data: WebSocket.Data) => {
      const msg = JSON.parse(data.toString());

      // Log non-audio messages for debugging
      const keys = Object.keys(msg);
      const hasAudio = msg.serverContent?.modelTurn?.parts?.some((p: any) => p.inlineData);
      if (!hasAudio) {
        console.log(`    [MSG] keys=${keys.join(",")}`);
        if (msg.serverContent) {
          const scKeys = Object.keys(msg.serverContent);
          console.log(`           serverContent keys=${scKeys.join(",")}`);
          if (msg.serverContent.outputTranscription) {
            console.log(`           outputTranscription=${JSON.stringify(msg.serverContent.outputTranscription)}`);
          }
        }
        if (msg.outputTranscription) {
          console.log(`           top-level outputTranscription=${JSON.stringify(msg.outputTranscription)}`);
        }
      }

      // Input transcript (at top level or in serverContent)
      if (msg.inputTranscription && msg.inputTranscription.text) {
        result.inputTranscript += msg.inputTranscription.text;
      }

      const sc = msg.serverContent;
      if (!sc) return;

      if (sc.inputTranscription && sc.inputTranscription.text) {
        result.inputTranscript += sc.inputTranscription.text;
      }

      if (sc.outputTranscription && sc.outputTranscription.text) {
        result.outputTranscript += sc.outputTranscription.text;
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
        turnDone = true;
        // Wait 2s after turnComplete for trailing outputTranscript messages
        setTimeout(() => {
          clearTimeout(timeout);
          ws.off("message", handler);
          resolve(result);
        }, 2000);
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

  for (let i = 0; i < QUESTIONS.length; i++) {
    const { q, expectInTranscript } = QUESTIONS[i];
    const turnNum = i + 1;
    console.log(`\n--- Turn ${turnNum}: "${q}" ---`);

    // Build RAG-enriched message (same as localRecognition.onresult in chat-widget.js)
    const { context } = searchContent(index, q);
    let combined = 'The user just asked: "' + q + '"\n\n';
    if (context) {
      combined += "Reference material:\n" + context + "\n\n";
      combined += "Answer the user's question using the reference material above.";
    } else {
      combined += "Answer the user's question.";
    }
    check(`Turn ${turnNum} RAG context found`, context.length > 100, `only ${context.length} chars`);
    sendText(ws, combined);

    try {
      const turn = await waitForTurn(ws);
      check(`Turn ${turnNum} got response`, true);
      console.log(`  Audio chunks: ${turn.audioChunks}`);
      console.log(`  Output transcript: ${turn.outputTranscript.length} chars`);
      check(`Turn ${turnNum} has audio`, turn.audioChunks > 0, `got ${turn.audioChunks} chunks`);
      check(`Turn ${turnNum} has output transcript`, turn.outputTranscript.length > 0, "empty transcript");

      if (turn.outputTranscript) {
        console.log(`  Transcript: "${turn.outputTranscript.substring(0, 200)}"`);
        const lower = turn.outputTranscript.toLowerCase();
        for (const expected of expectInTranscript) {
          check(
            `Turn ${turnNum} transcript contains "${expected}"`,
            lower.includes(expected.toLowerCase()),
            "not found in transcript"
          );
        }
        // Verify it didn't say "I don't know" or "no record"
        check(
          `Turn ${turnNum} used RAG context (no "no record/don't know")`,
          !lower.includes("no record") && !lower.includes("don't know") && !lower.includes("do not know"),
          "model ignored RAG context"
        );
      }
    } catch (err: any) {
      check(`Turn ${turnNum} got response`, false, err.message);
      if (i === 0) { ws.close(); printSummary(); return; }
    }
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
