/**
 * Netlify Function: /api/tts
 *
 * Text-to-speech endpoint using Gemini TTS with Kore voice.
 * Client sends { text } and receives audio/wav.
 */

import { generateSpeech } from "../../src/voice/gemini-tts";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export default async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }

  if (req.method !== "POST") {
    return new Response("Method not allowed", {
      status: 405,
      headers: CORS_HEADERS,
    });
  }

  const { text } = await req.json();

  if (!text) {
    return new Response(JSON.stringify({ error: "text is required" }), {
      status: 400,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }

  const apiKey = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
  if (!apiKey) {
    return new Response(
      JSON.stringify({ error: "TTS service not configured" }),
      {
        status: 503,
        headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
      }
    );
  }

  const wavBytes = await generateSpeech(text, apiKey);

  return new Response(wavBytes, {
    headers: {
      ...CORS_HEADERS,
      "Content-Type": "audio/wav",
      "Cache-Control": "public, max-age=86400",
    },
  });
};

export const config = {
  path: "/api/tts",
};
