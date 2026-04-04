/**
 * /api/share - Save a chat to Vercel Blob for sharing
 *
 * POST { messages } -> { id, url }
 * GET ?id=abc123   -> redirect to blob JSON (for loading shared chats)
 */

import { put, list } from "@vercel/blob";
import { randomBytes } from "crypto";

export const maxDuration = 30;

const OPEN_CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

function generateId(): string {
  return randomBytes(6).toString("base64url");
}

async function handler(req: Request) {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: OPEN_CORS });
  }

  // GET: load a shared chat by ID
  if (req.method === "GET") {
    const url = new URL(req.url);
    const id = url.searchParams.get("id");
    if (!id) {
      return new Response(JSON.stringify({ error: "id is required" }), {
        status: 400,
        headers: { ...OPEN_CORS, "Content-Type": "application/json" },
      });
    }

    const { blobs } = await list({ prefix: `chats/${id}.json` });
    if (blobs.length === 0) {
      return new Response(JSON.stringify({ error: "chat not found" }), {
        status: 404,
        headers: { ...OPEN_CORS, "Content-Type": "application/json" },
      });
    }

    // Redirect to the blob URL (served from CDN)
    return Response.redirect(blobs[0].url, 302);
  }

  // POST: save a new shared chat
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405, headers: OPEN_CORS });
  }

  const body = await req.json();
  const { messages, title } = body;

  if (!messages || !Array.isArray(messages) || messages.length === 0) {
    return new Response(JSON.stringify({ error: "messages array is required" }), {
      status: 400,
      headers: { ...OPEN_CORS, "Content-Type": "application/json" },
    });
  }

  const id = generateId();
  const chatData = {
    id,
    title: title || messages.find((m: { role: string }) => m.role === "user")?.content?.substring(0, 80) || "Shared chat",
    messages,
    sharedAt: new Date().toISOString(),
  };

  const blob = await put(`chats/${id}.json`, JSON.stringify(chatData), {
    access: "public",
    contentType: "application/json",
  });

  const shareUrl = new URL(req.url).origin + "/c/" + id;

  return new Response(JSON.stringify({ id, shareUrl, blobUrl: blob.url }), {
    headers: { ...OPEN_CORS, "Content-Type": "application/json" },
  });
}

export default { fetch: handler };
