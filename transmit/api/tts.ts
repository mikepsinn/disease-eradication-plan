/**
 * Vercel Edge Function: /api/tts
 *
 * Text-to-speech using Gemini TTS with Kore voice.
 * Client sends { text } and receives audio/wav.
 * Restricted to warondisease.org origins.
 */

import { generateSpeech } from "../lib/gemini-tts";
import { corsHeaders, checkOrigin } from "../lib/cors";

export const maxDuration = 300;

export default async function handler(req: Request) {
  const origin = req.headers.get("origin");
  const cors = corsHeaders(origin);

  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: cors });
  }

  const blocked = checkOrigin(req);
  if (blocked) return blocked;

  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405, headers: cors });
  }

  const { text } = await req.json();

  if (!text) {
    return new Response(JSON.stringify({ error: "text is required" }), {
      status: 400,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }

  const apiKey = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
  if (!apiKey) {
    return new Response(JSON.stringify({ error: "TTS service not configured" }), {
      status: 503,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }

  const wavBytes = await generateSpeech(text, apiKey);

  return new Response(wavBytes as unknown as BodyInit, {
    headers: {
      ...cors,
      "Content-Type": "audio/wav",
      "Cache-Control": "public, max-age=86400",
    },
  });
}
