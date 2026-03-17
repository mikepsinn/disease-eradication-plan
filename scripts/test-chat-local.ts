/**
 * Local test server for chat widget.
 * Run: npx tsx scripts/test-chat-local.ts
 * Open: http://localhost:3142
 */

import "dotenv/config";
import { createServer } from "node:http";
import { readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { streamText } from "ai";
import { google } from "@ai-sdk/google";
import { WISHONIA_SYSTEM_PROMPT } from "../src/prompts/wishonia-chat";
import { generateSpeech } from "../src/voice/gemini-tts";

const PORT = 3142;
// Always resolve to project root (one level up from scripts/)
const ROOT = resolve(import.meta.dirname, "..");

// Serve static files for the chat widget
function serveStatic(
  res: import("node:http").ServerResponse,
  filePath: string,
  contentType: string
): boolean {
  try {
    const data = readFileSync(filePath);
    res.writeHead(200, { "Content-Type": contentType });
    res.end(data);
    return true;
  } catch {
    return false;
  }
}

const TEST_HTML = `<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="quarto:offset" content="">
  <title>Ask Wishonia</title>
  <link href="https://fonts.googleapis.com/css?family=Orbitron:400,700,900&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css?family=Yellowtail&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/chat-widget.css">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0d0d0d;
      color: #ececec;
      height: 100vh; width: 100vw; overflow: hidden;
    }

    /* === Retro background (subtle) === */
    .bg-grid {
      position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none;
      background: radial-gradient(ellipse at center bottom, rgba(127,0,173,0.15) 0%, transparent 60%);
    }

    /* === Full-page chat layout === */
    /* Hide the floating chat widget - we replace it with full-page layout */
    .chat-fab { display: none !important; }
    .chat-panel {
      position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
      width: 100% !important; height: 100% !important; max-height: 100% !important;
      border-radius: 0 !important; border: none !important; box-shadow: none !important;
      display: flex !important; z-index: 5 !important;
      background: transparent !important;
    }

    /* Header - slim top bar */
    .chat-header {
      background: rgba(20,10,30,0.85) !important; backdrop-filter: blur(12px);
      padding: 10px 20px !important; border-bottom: 1px solid rgba(54,226,248,0.15);
    }
    .chat-header-title {
      font-family: 'Orbitron', sans-serif !important; font-size: 13px !important;
      letter-spacing: 0.1em !important; text-transform: uppercase;
      background: linear-gradient(90deg, #C6CBF5, #d100b1);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .chat-newchat-btn, .chat-fullscreen-btn, .chat-close-btn { display: none !important; }

    /* Messages area - centered column like ChatGPT */
    .chat-messages {
      flex: 1 !important; background: transparent !important;
      padding: 24px 16px 24px !important; max-width: 760px; margin: 0 auto; width: 100%;
    }

    /* Message bubbles - full-width, no bubble shape */
    .chat-msg {
      max-width: 100% !important; border-radius: 8px !important;
      font-size: 15px !important; line-height: 1.7 !important;
      padding: 14px 16px !important; background: transparent !important;
    }
    .chat-msg-user {
      background: rgba(54,226,248,0.08) !important; color: #ececec !important;
      border: 1px solid rgba(54,226,248,0.15); border-radius: 12px !important;
      align-self: flex-end !important; max-width: 80% !important;
    }
    .chat-msg-assistant {
      background: transparent !important; color: #d1d1d1 !important;
      align-self: flex-start !important; padding-left: 0 !important;
    }

    /* Welcome */
    .chat-welcome { color: #888 !important; padding: 60px 20px !important; }
    .chat-welcome p { font-size: 16px !important; color: #aaa; }
    .chat-hints { max-width: 500px; margin: 16px auto 0; }
    .chat-hint-btn {
      background: rgba(20,10,40,0.6) !important; color: #C6CBF5 !important;
      border: 1px solid rgba(54,226,248,0.2) !important; border-radius: 8px !important;
      font-size: 14px !important; transition: all 0.2s !important;
    }
    .chat-hint-btn:hover {
      border-color: #d100b1 !important; background: rgba(209,0,177,0.08) !important;
      box-shadow: 0 0 12px rgba(209,0,177,0.2);
    }

    /* Input area - bottom bar with padding for robot */
    .chat-input-area {
      background: rgba(20,10,30,0.85) !important; backdrop-filter: blur(12px);
      border-top: 1px solid rgba(54,226,248,0.15) !important;
      padding: 14px 20px 14px !important; max-width: 760px; margin: 0 auto; width: 100%;
      padding-right: 140px !important; /* room for robot */
    }
    .chat-input {
      background: rgba(255,255,255,0.06) !important; color: #ececec !important;
      border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 12px !important;
      font-size: 15px !important; padding: 12px 16px !important;
    }
    .chat-input:focus {
      border-color: rgba(209,0,177,0.5) !important;
      box-shadow: 0 0 0 2px rgba(209,0,177,0.15) !important;
    }
    .chat-input::placeholder { color: #666; }
    .chat-send-btn { background: #d100b1 !important; }
    .chat-send-btn:hover { filter: brightness(1.2); }
    .chat-mic-btn, .chat-voicechat-btn {
      background: rgba(255,255,255,0.06) !important; color: #C6CBF5 !important;
      border: 1px solid rgba(255,255,255,0.1);
    }
    .chat-voicechat-btn.voice-active {
      background: #28a745 !important; color: #fff !important;
      border-color: #28a745 !important;
    }

    /* Links in messages */
    .chat-msg a { color: #36E2F8 !important; }

    /* Typing / voice indicators */
    .chat-typing { color: #888; }
    .chat-waveform-bar { background: #d100b1 !important; }
    .chat-listening-ring { border-color: #d100b1 !important; }
    .chat-voice-loading span, .chat-listening-indicator span { color: #888; }

    /* TTS button */
    .chat-tts-btn { color: #888 !important; }
    .chat-tts-btn:hover { color: #d100b1 !important; }

    /* === Robot - peeking over input bar === */
    .robot-container {
      position: fixed; z-index: 20; cursor: pointer;
      /* Show head + part of torso above the input bar */
      bottom: 20px; right: 20px;
      width: 120px; height: 130px;
      transform: scale(0.85);
      transform-origin: bottom right;
    }
    .robot .head {
      position: absolute; width: 100px; left: 15px; height: 75px;
      border-radius: 490px 550px 550px 550px; overflow: hidden;
      background: #ccc linear-gradient(to right, #b7a9a9 0%, #c1b1b1 40%, #c1b5b5 60%, #ab9c9c 100%);
      transform-origin: 50% 100%;
      animation: bob 8000ms ease-in-out alternate infinite -1000ms;
      border: 2px solid #000;
    }
    .robot .eyes {
      position: absolute; top: calc(50% - 8px); right: 20px; left: 20px; height: 16px;
      animation: blink 10000ms linear forwards infinite; z-index: 0;
    }
    .robot .eyeball {
      position: absolute; width: 16px; height: 16px;
      background: radial-gradient(ellipse, #dffdfe 0%, #11c1f3 50%, #387ef5 60%) no-repeat center;
      background-size: 100%; z-index: -2; border-radius: 100%; border: 2px solid #000;
    }
    .robot .eyeball_left { left: 0; }
    .robot .eyeball_right { right: 0; }
    .robot .mouth {
      position: absolute; bottom: 12px; left: 38px; width: 24px; height: 4px;
      background-color: #000; overflow: hidden; border-radius: 4px;
      transition: height 100ms cubic-bezier(0.455,0.03,0.515,0.955);
    }
    .robot .mouth-container { position: absolute; top: 0; right: 0; bottom: 0; left: 0; }
    .robot .mouth-container-line {
      position: absolute; top: 30%; height: 0px; background-color: limegreen; width: 100%; margin-top: -1px;
    }
    .robot.robot_speaking .mouth { height: 12px; }
    .robot.robot_speaking .mouth-container { animation: speakingAnim 0.3s infinite; }
    .robot.robot_speaking .mouth-container-line { height: 3px; }
    .robot.robot_listening .mouth { height: 6px; }
    .robot.robot_listening .mouth-container { animation: listeningAnim 0.5s infinite; }
    .robot.robot_listening .mouth-container-line { height: 2px; }
    .robot .neck {
      position: absolute; bottom: 35px; left: calc(50% - 4px); width: 3px; height: 38px;
      border-radius: 12px; border: 2px solid #000;
      background: repeating-linear-gradient(180deg, rgba(0,0,0,0.2), rgba(0,0,0,0.2) 7%, #646464 10%), linear-gradient(to right, #ccc 0%, #e6e6e6 40%, #e6e6e6 60%, #ccc 100%);
    }
    .robot .torso {
      position: absolute; bottom: 0; left: calc(50% - 15px); width: 30px; height: 45px;
      border: 2px solid #000;
      background: linear-gradient(to right, #b7afaf 0%, #b7b0b0 40%, #afa6a6 60%, #b9b0b0 100%);
    }
    .robot .arms { position: absolute; bottom: 0; left: 38px; right: 38px; height: 38px; }
    .robot .arm {
      position: absolute; border: 2px solid #000; top: 0; width: 8px; height: 38px;
      border-radius: 8px 8px 0 0;
      background: repeating-linear-gradient(180deg, rgba(0,0,0,0.2), rgba(0,0,0,0.2) 7%, #646464 10%), linear-gradient(to right, #ccc 0%, #e6e6e6 40%, #e6e6e6 60%, #ccc 100%);
    }
    .robot .arm_left { left: 0; }
    .robot .arm_right { right: 0; }

    @keyframes bob {
      0%  { transform: rotate(-3deg); }
      40% { transform: rotate(-3deg); animation-timing-function: cubic-bezier(1,0,0,1); }
      60% { transform: rotate(3deg); }
      100%{ transform: rotate(3deg); }
    }
    @keyframes blink {
      50% { transform: scale(1,1); }
      51% { transform: scale(1,0.1); }
      52% { transform: scale(1,1); }
    }
    @keyframes speakingAnim {
      0%   { filter: url("#speaking-0"); }
      25%  { filter: url("#speaking-1"); }
      50%  { filter: url("#speaking-2"); }
      75%  { filter: url("#speaking-3"); }
      100% { filter: url("#speaking-4"); }
    }
    @keyframes listeningAnim {
      0%   { filter: url("#listening-0"); }
      25%  { filter: url("#listening-1"); }
      50%  { filter: url("#listening-2"); }
      75%  { filter: url("#listening-3"); }
      100% { filter: url("#listening-4"); }
    }

    /* Mobile */
    @media (max-width: 600px) {
      .chat-input-area { padding-right: 100px !important; }
      .robot-container { width: 80px; height: 90px; transform: scale(0.6); right: 10px; bottom: 15px; }
    }
  </style>
</head>
<body>
  <div class="bg-grid"></div>

  <!-- Robot peeking over the input bar -->
  <div class="robot-container" id="robot-trigger">
    <div class="robot" id="robot-el">
      <div class="neck"></div>
      <div class="arms"><div class="arm arm_left"></div><div class="arm arm_right"></div></div>
      <div class="torso"></div>
      <div class="head">
        <div class="eyes"><div class="eyeball eyeball_left"></div><div class="eyeball eyeball_right"></div></div>
        <div class="mouth"><div class="mouth-container"><div class="mouth-container-line"></div></div></div>
      </div>
    </div>
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" style="display:none"><defs>
      <filter id="speaking-0"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="0"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="12"/></filter>
      <filter id="speaking-1"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="30"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="13"/></filter>
      <filter id="speaking-2"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="2"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="12"/></filter>
      <filter id="speaking-3"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="30"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="13"/></filter>
      <filter id="speaking-4"><feTurbulence baseFrequency="0.1" numOctaves="3" result="noise" seed="4"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="11"/></filter>
      <filter id="listening-0"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="0"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="2"/></filter>
      <filter id="listening-1"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="30"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="3"/></filter>
      <filter id="listening-2"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="2"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="2"/></filter>
      <filter id="listening-3"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="30"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="3"/></filter>
      <filter id="listening-4"><feTurbulence baseFrequency="0.1" numOctaves="3" result="noise" seed="4"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="1"/></filter>
    </defs></svg>
  </div>

  <script src="/assets/js/gemini-live-client.js" defer></script>
  <script src="/assets/js/audio-utils.js" defer></script>
  <script src="/assets/js/chat-widget.js" defer></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      var robotEl = document.getElementById('robot-el');

      // Auto-open chat panel (it becomes the full page)
      setTimeout(function() {
        var fab = document.querySelector('.chat-fab');
        if (fab) fab.click();
      }, 100);

      // Robot click toggles voice chat
      document.getElementById('robot-trigger').addEventListener('click', function() {
        var vcBtn = document.querySelector('.chat-voicechat-btn');
        if (vcBtn && vcBtn.style.display !== 'none') vcBtn.click();
      });

      // Robot state animation
      window.setRobotState = function(state) {
        if (!robotEl) return;
        robotEl.classList.remove('robot_speaking', 'robot_listening');
        if (state === 'speaking') robotEl.classList.add('robot_speaking');
        else if (state === 'listening') robotEl.classList.add('robot_listening');
      };
    });
  </script>
</body>
</html>`;


const server = createServer(async (req, res) => {
  // CORS
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  try {
  if (req.method === "OPTIONS") {
    res.writeHead(204);
    res.end();
    return;
  }

  const url = req.url || "/";

  // === Serve test page ===
  if (url === "/" && req.method === "GET") {
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    res.end(TEST_HTML);
    return;
  }

  // === /api/voice-token (GET) ===
  if (url === "/api/voice-token" && req.method === "GET") {
    const apiKey = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
    if (!apiKey) {
      res.writeHead(503, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "GOOGLE_GENERATIVE_AI_API_KEY not set" }));
      return;
    }

    console.log("[voice-token] returning API key");
    res.writeHead(200, { "Content-Type": "application/json", "Cache-Control": "no-store" });
    res.end(JSON.stringify({ key: apiKey }));
    return;
  }

  // === Serve static assets ===
  if (req.method === "GET") {
    const MIME: Record<string, string> = {
      ".js": "application/javascript",
      ".css": "text/css",
      ".json": "application/json",
    };
    const ext = url.substring(url.lastIndexOf("."));
    if (MIME[ext]) {
      if (serveStatic(res, join(ROOT, url), MIME[ext])) return;
      // Fallback: search-index.json from the generated paperback site
      if (url.endsWith("search-index.json") || url.endsWith("search.json")) {
        if (serveStatic(res, join(ROOT, "_manual-paperback/warondisease/search-index.json"), MIME[".json"])) return;
      }
    }
    // Static file not found - return 404 (don't crash)
    res.writeHead(404);
    res.end("Not found");
    return;
  }

  // === Parse JSON body for POST routes ===
  if (req.method === "POST") {
    const chunks: Buffer[] = [];
    for await (const chunk of req) chunks.push(chunk as Buffer);
    const body = JSON.parse(Buffer.concat(chunks).toString());

    // === /api/chat ===
    if (url === "/api/chat") {
      const { question, context, history } = body;
      if (!question) {
        res.writeHead(400, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: "question is required" }));
        return;
      }

      const systemPrompt = WISHONIA_SYSTEM_PROMPT.replace(
        "{context}",
        context || "No specific book context available."
      );

      const messages = [
        ...(history || []).map((m: any) => ({
          role: m.role as "user" | "assistant",
          content: m.content,
        })),
        { role: "user" as const, content: question },
      ];

      console.log(`[chat] question: "${question}"`);

      const result = streamText({
        model: google("gemini-3-flash-preview", {
          safetySettings: [
            { category: "HARM_CATEGORY_HARASSMENT", threshold: "BLOCK_NONE" },
            { category: "HARM_CATEGORY_HATE_SPEECH", threshold: "BLOCK_NONE" },
            { category: "HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold: "BLOCK_NONE" },
            { category: "HARM_CATEGORY_DANGEROUS_CONTENT", threshold: "BLOCK_NONE" },
          ],
        }),
        system: systemPrompt,
        messages,
      });

      res.writeHead(200, {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "no-cache",
      });

      for await (const chunk of result.textStream) {
        res.write(chunk);
      }
      console.log(`[chat] done`);
      res.end();
      return;
    }

    // === /api/tts ===
    if (url === "/api/tts") {
      const { text } = body;
      if (!text) {
        res.writeHead(400, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: "text is required" }));
        return;
      }

      const apiKey = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
      if (!apiKey) {
        res.writeHead(503, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: "GOOGLE_GENERATIVE_AI_API_KEY not set" }));
        return;
      }

      console.log(`[tts] generating: "${text.substring(0, 50)}..."`);
      const wav = await generateSpeech(text, apiKey);
      console.log(`[tts] done, ${wav.length} bytes`);

      res.writeHead(200, {
        "Content-Type": "audio/wav",
        "Cache-Control": "public, max-age=86400",
        "Content-Length": String(wav.length),
      });
      res.end(wav);
      return;
    }
  }

  res.writeHead(404);
  res.end("Not found");

  } catch (err: any) {
    console.error(`[error] ${req.method} ${req.url}:`, err.message);
    if (!res.headersSent) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: err.message }));
    }
  }
});

server.listen(PORT, () => {
  console.log(`\n  Chat widget test: http://localhost:${PORT}\n`);
});
