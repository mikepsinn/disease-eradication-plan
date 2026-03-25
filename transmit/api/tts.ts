/**
 * Vercel Serverless Function: /api/tts
 *
 * Text-to-speech using Gemini TTS with Kore voice.
 * Client sends { text } and receives audio/wav.
 */

import type { VercelRequest, VercelResponse } from "@vercel/node";
import { generateSpeech } from "../lib/gemini-tts";

export default async function handler(req: VercelRequest, res: VercelResponse) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).send("Method not allowed");

  const { text } = req.body;
  if (!text) return res.status(400).json({ error: "text is required" });

  const apiKey = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
  if (!apiKey) return res.status(503).json({ error: "TTS service not configured" });

  const wavBytes = await generateSpeech(text, apiKey);

  res.setHeader("Content-Type", "audio/wav");
  res.setHeader("Cache-Control", "public, max-age=86400");
  res.send(Buffer.from(wavBytes));
}
