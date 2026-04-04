/**
 * Vercel Edge Function: /api/visuals
 *
 * Structured visual supplements for chat responses.
 * Client sends { question, context, imageOptions } and receives JSON
 * with optional visual elements (keyFigure, latex, chart, table, etc.).
 * Runs in parallel with /api/chat -- never blocks the main response.
 */

import { generateObject } from "ai";
import { google } from "@ai-sdk/google";
import { VISUALS_SYSTEM_PROMPT, visualsSchema } from "../lib/visuals-prompt.js";
import { initSentry, Sentry } from "../lib/sentry.js";

export const maxDuration = 300;

const OPEN_CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

async function handler(req: Request) {
  initSentry();

  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: OPEN_CORS });
  }

  if (req.method !== "POST") {
    return new Response("Method not allowed", {
      status: 405,
      headers: OPEN_CORS,
    });
  }

  const t0 = Date.now();
  const { question, context, imageOptions } = await req.json();

  if (!question) {
    return new Response(JSON.stringify({ error: "question is required" }), {
      status: 400,
      headers: { ...OPEN_CORS, "Content-Type": "application/json" },
    });
  }

  console.log(`[visuals] question="${question.substring(0, 80)}" context=${(context || "").length} chars`);

  const systemPrompt = VISUALS_SYSTEM_PROMPT.replace(
    "{context}",
    context || "No specific book context available."
  );

  // Append image candidates so the LLM can pick the best match
  let userMessage = question;
  if (imageOptions && imageOptions.length > 0) {
    userMessage +=
      "\n\nAvailable image candidates:\n" +
      imageOptions
        .map(
          (img: { path: string; title?: string; description?: string }) =>
            `- ${img.path}${img.title ? " (" + img.title + ")" : ""}${img.description ? ": " + img.description : ""}`
        )
        .join("\n");
  }

  try {
    const result = await generateObject({
      model: google("gemini-3-flash-preview", {
        safetySettings: [
          { category: "HARM_CATEGORY_HARASSMENT", threshold: "BLOCK_NONE" },
          { category: "HARM_CATEGORY_HATE_SPEECH", threshold: "BLOCK_NONE" },
          {
            category: "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold: "BLOCK_NONE",
          },
          {
            category: "HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold: "BLOCK_NONE",
          },
        ],
      }),
      schema: visualsSchema,
      system: systemPrompt,
      prompt: userMessage,
    });

    const body = JSON.stringify(result.object);
    console.log(`[visuals] done in ${Date.now() - t0}ms | ${body.length} chars | usage: ${JSON.stringify(result.usage)}`);
    return new Response(body, {
      headers: { ...OPEN_CORS, "Content-Type": "application/json" },
    });
  } catch (err: unknown) {
    Sentry.captureException(err);
    const message = err instanceof Error ? err.message : "Unknown error";
    console.log(`[visuals] error in ${Date.now() - t0}ms: ${message}`);
    return new Response(JSON.stringify({ error: message }), {
      status: 500,
      headers: { ...OPEN_CORS, "Content-Type": "application/json" },
    });
  }
}

export default { fetch: handler };
