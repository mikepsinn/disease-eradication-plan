/**
 * Netlify Function: /api/chat
 *
 * Streaming chat endpoint using Gemini Flash + Wishonia persona.
 * Client sends { question, context, history } and receives a text stream.
 */

import { streamText } from "ai";
import { google } from "@ai-sdk/google";
import { WISHONIA_SYSTEM_PROMPT } from "../../src/prompts/wishonia-chat";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export default async (req: Request) => {
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }

  if (req.method !== "POST") {
    return new Response("Method not allowed", {
      status: 405,
      headers: CORS_HEADERS,
    });
  }

  const { question, context, history } = await req.json();

  if (!question) {
    return new Response(JSON.stringify({ error: "question is required" }), {
      status: 400,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }

  // Build system prompt with RAG context injected
  const systemPrompt = WISHONIA_SYSTEM_PROMPT.replace(
    "{context}",
    context || "No specific book context available for this question."
  );

  // Build messages array from history + new question
  const messages = [
    ...(history || []).map((m: { role: string; content: string }) => ({
      role: m.role as "user" | "assistant",
      content: m.content,
    })),
    { role: "user" as const, content: question },
  ];

  // Safety filters disabled: the book discusses war, death, disease mortality
  // stats, military spending, and uses dark humor. All legitimate educational content.
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

  // Stream plain text back to the client
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      for await (const chunk of result.textStream) {
        controller.enqueue(encoder.encode(chunk));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      ...CORS_HEADERS,
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-cache",
    },
  });
};

export const config = {
  path: "/api/chat",
};
