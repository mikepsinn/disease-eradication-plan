/**
 * Vercel Edge Function: /api/voice-token
 *
 * Returns credentials for the Gemini Live API WebSocket connection.
 * RESTRICTED: Only returns the key to requests from warondisease.org domains.
 * The key is rate-limited by Google's API quotas.
 */

import { corsHeaders, checkOrigin } from "../lib/cors";

export const config = { runtime: "edge" };

export default async function handler(req: Request) {
  const origin = req.headers.get("origin");
  const cors = corsHeaders(origin);

  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: cors });
  }

  const blocked = checkOrigin(req);
  if (blocked) return blocked;

  const apiKey = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
  if (!apiKey) {
    return new Response(JSON.stringify({ error: "Voice service not configured" }), {
      status: 503,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }

  return new Response(JSON.stringify({ key: apiKey }), {
    headers: {
      ...cors,
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
    },
  });
}
