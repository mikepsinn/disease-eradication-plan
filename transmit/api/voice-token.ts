/**
 * Vercel Edge Function: /api/voice-token
 *
 * Creates a short-lived ephemeral token for the Gemini Live API WebSocket.
 * The real API key never leaves the server. The token is single-use and
 * expires in minutes. Restricted to warondisease.org origins.
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

  // Create ephemeral token via Google's auth_tokens API (v1alpha)
  const now = Date.now();
  const response = await fetch(
    "https://generativelanguage.googleapis.com/v1alpha/auth_tokens",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-goog-api-key": apiKey,
      },
      body: JSON.stringify({
        uses: 1,
        expire_time: new Date(now + 30 * 60 * 1000).toISOString(),
        new_session_expire_time: new Date(now + 2 * 60 * 1000).toISOString(),
      }),
    }
  );

  if (!response.ok) {
    const err = await response.text();
    return new Response(JSON.stringify({ error: "Token creation failed", detail: err }), {
      status: 502,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }

  const data = await response.json();

  return new Response(JSON.stringify({ token: data.name }), {
    headers: {
      ...cors,
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
    },
  });
}
