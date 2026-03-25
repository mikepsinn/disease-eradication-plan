/**
 * CORS and origin validation for the transmit API.
 *
 * Only allows requests from warondisease.org domains and localhost (dev).
 */

const ALLOWED_ORIGINS = [
  /^https?:\/\/([a-z0-9-]+\.)?warondisease\.org$/,
  /^https?:\/\/localhost(:\d+)?$/,
  /^https?:\/\/127\.0\.0\.1(:\d+)?$/,
];

export function isAllowedOrigin(origin: string | null): boolean {
  if (!origin) return false;
  return ALLOWED_ORIGINS.some((pattern) => pattern.test(origin));
}

export function corsHeaders(origin: string | null): Record<string, string> {
  const allowed = isAllowedOrigin(origin) ? origin! : "https://manual.warondisease.org";
  return {
    "Access-Control-Allow-Origin": allowed,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin",
  };
}

/** Return a 403 if the origin isn't allowed. Returns null if OK. */
export function checkOrigin(req: Request): Response | null {
  const origin = req.headers.get("origin");
  if (origin && !isAllowedOrigin(origin)) {
    return new Response("Forbidden", { status: 403 });
  }
  return null;
}
