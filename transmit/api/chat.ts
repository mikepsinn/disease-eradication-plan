/**
 * Vercel Edge Function: /api/chat
 *
 * Streaming chat endpoint using Gemini Flash + Wishonia persona.
 * Client sends { question, context, history } and receives a text stream.
 * Restricted to warondisease.org origins.
 */

import { streamText } from "ai";
import { google } from "@ai-sdk/google";
import { WISHONIA_SYSTEM_PROMPT } from "../lib/wishonia-chat";
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

  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405, headers: cors });
  }

  const { question, context, history } = await req.json();

  if (!question) {
    return new Response(JSON.stringify({ error: "question is required" }), {
      status: 400,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }

  const systemPrompt = WISHONIA_SYSTEM_PROMPT.replace(
    "{context}",
    context || "No specific book context available for this question."
  );

  const messages = [
    ...(history || []).map((m: { role: string; content: string }) => ({
      role: m.role as "user" | "assistant",
      content: m.content,
    })),
    { role: "user" as const, content: question },
  ];

  const result = streamText({
    model: google("gemini-3-flash-preview", {
      safetySettings: [
        { category: "HARM_CATEGORY_HARASSMENT", threshold: "BLOCK_NONE" },
        { category: "HARM_CATEGORY_HATE_SPEECH", threshold: "BLOCK_NONE" },
        { category: "HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold: "BLOCK_NONE" },
        { category: "HARM_CATEGORY_DANGEROUS_CONTENT", threshold: "BLOCK_NONE" },
      ],
    }),
    system: systemPrompt,
    messages,
  });

  return result.toTextStreamResponse();
}
