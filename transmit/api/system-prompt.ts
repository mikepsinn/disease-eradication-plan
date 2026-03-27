/**
 * Vercel Edge Function: /api/system-prompt
 *
 * Returns the Wishonia voice system prompt for debug display in the chat widget.
 * Open CORS so the embeddable widget can fetch it from any origin.
 */

import { WISHONIA_VOICE_PROMPT } from "../lib/wishonia-chat";

export const config = { runtime: "edge" };

const OPEN_CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export default function handler(req: Request) {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: OPEN_CORS });
  }

  if (!WISHONIA_VOICE_PROMPT) {
    return new Response(JSON.stringify({ error: "System prompt not configured" }), {
      status: 503,
      headers: { ...OPEN_CORS, "Content-Type": "application/json" },
    });
  }

  return new Response(JSON.stringify({ prompt: WISHONIA_VOICE_PROMPT }), {
    headers: {
      ...OPEN_CORS,
      "Content-Type": "application/json",
      "Cache-Control": "public, max-age=300",
    },
  });
}
