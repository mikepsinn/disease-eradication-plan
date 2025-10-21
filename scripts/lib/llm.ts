import { GoogleGenAI } from '@google/genai';
import Anthropic from '@anthropic-ai/sdk';
import dotenv from 'dotenv';

dotenv.config();

// --- LLM Setup ---
// DO NOT CHANGE THESE MODEL NUMBERS
const GEMINI_MODEL_ID = 'gemini-2.5-pro';
const CLAUDE_MODEL_ID = 'claude-opus-4-1-20250805';

const API_KEY = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
if (!API_KEY) {
  throw new Error('GOOGLE_GENERATIVE_AI_API_KEY is not set in the .env file.');
}

// Initialize Google Generative AI client
const genAI = new GoogleGenAI({
  apiKey: API_KEY
});

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});
if (!process.env.ANTHROPIC_API_KEY) {
  throw new Error('ANTHROPIC_API_KEY is not set in the .env file.');
}

export async function generateGeminiContent(prompt: string): Promise<string> {
  const result = await genAI.models.generateContent({
    model: GEMINI_MODEL_ID,
    contents: prompt,
  });
  return result.text || '';
}

export async function generateClaudeContent(prompt: string): Promise<string> {
  const msg = await anthropic.messages.create({
    model: CLAUDE_MODEL_ID,
    max_tokens: 8192,
    messages: [{ role: "user", content: prompt }],
  });

  const responseBlock = msg.content[0];
  if (responseBlock.type !== 'text') {
    throw new Error('Unexpected response format from Anthropic API. Expected a text block.');
  }
  return responseBlock.text;
}
