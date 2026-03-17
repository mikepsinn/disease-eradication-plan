/**
 * Netlify Function: /api/voice-token
 *
 * Returns credentials for the Gemini Live API WebSocket connection.
 * Currently returns the API key directly since ephemeral tokens
 * don't support WebSocket auth yet. The key is already rate-limited
 * by Google's API quotas.
 */

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export default async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }

  const apiKey = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
  if (!apiKey) {
    return new Response(
      JSON.stringify({ error: "Voice service not configured" }),
      {
        status: 503,
        headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
      }
    );
  }

  return new Response(JSON.stringify({ key: apiKey }), {
    headers: {
      ...CORS_HEADERS,
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
    },
  });
};

export const config = {
  path: "/api/voice-token",
};
