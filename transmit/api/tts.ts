/**
 * Vercel Serverless Function: /api/tts
 *
 * Text-to-speech using Gemini TTS with Kore voice.
 * Client sends { text } and receives audio/wav.
 */

import { generateSpeech } from "../lib/gemini-tts";

export const config = { maxDuration: 30 };

export default async function handler(req: Request) {
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
      },
    });
  }

  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  const { text } = await req.json();

  if (!text) {
    return Response.json({ error: "text is required" }, { status: 400 });
  }

  const apiKey = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
  if (!apiKey) {
    return Response.json({ error: "TTS service not configured" }, { status: 503 });
  }

  const wavBytes = await generateSpeech(text, apiKey);

  return new Response(Buffer.from(wavBytes) as unknown as BodyInit, {
    headers: {
      "Content-Type": "audio/wav",
      "Cache-Control": "public, max-age=86400",
    },
  });
}
