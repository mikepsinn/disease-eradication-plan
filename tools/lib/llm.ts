import { GoogleGenAI } from '@google/genai';
import Anthropic from '@anthropic-ai/sdk';
import dotenv from 'dotenv';

dotenv.config();

// --- LLM Setup ---
// DO NOT CHANGE THESE MODEL NUMBERS
const GEMINI_PRO_MODEL_ID = 'gemini-2.5-pro';
const GEMINI_FLASH_MODEL_ID = 'gemini-2.5-flash';
const CLAUDE_OPUS_4_1_MODEL_ID = 'claude-opus-4-1-20250805';
const CLAUDE_SONNET_4_5_MODEL_ID = 'claude-sonnet-4-5-20250929';

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

export async function generateGeminiProContent(prompt: string): Promise<string> {
  const result = await genAI.models.generateContent({
    model: GEMINI_PRO_MODEL_ID,
    contents: prompt,
  });
  return result.text || '';
}

export async function generateGeminiFlashContent(prompt: string): Promise<string> {
  const result = await genAI.models.generateContent({
    model: GEMINI_FLASH_MODEL_ID,
    contents: prompt,
  });
  return result.text || '';
}

export async function generateClaudeOpus41Content(prompt: string): Promise<string> {
  const msg = await anthropic.messages.create({
    model: CLAUDE_OPUS_4_1_MODEL_ID,
    max_tokens: 8192,
    messages: [{ role: "user", content: prompt }],
  });

  const responseBlock = msg.content[0];
  if (responseBlock.type !== 'text') {
    throw new Error('Unexpected response format from Anthropic API. Expected a text block.');
  }
  return responseBlock.text;
}

export async function generateClaudeSonnet45Content(prompt: string): Promise<string> {
  const msg = await anthropic.messages.create({
    model: CLAUDE_SONNET_4_5_MODEL_ID,
    max_tokens: 8192,
    messages: [{ role: "user", content: prompt }],
  });

  const responseBlock = msg.content[0];
  if (responseBlock.type !== 'text') {
    throw new Error('Unexpected response format from Anthropic API. Expected a text block.');
  }
  return responseBlock.text;
}

// --- LLM Utility Functions ---

/**
 * Extracts JSON object from LLM response text, handling markdown code blocks
 */
export function extractJsonFromResponse(responseText: string, context: string = 'LLM response'): any {
  const jsonMatch = responseText.match(/\{[\s\S]*\}/);
  if (!jsonMatch) {
    throw new Error(`No JSON object found in ${context}. Response: ${responseText.substring(0, 500)}...`);
  }
  return JSON.parse(jsonMatch[0]);
}

/**
 * Loads a prompt template and replaces placeholders
 */
export async function loadPromptTemplate(templatePath: string, replacements: Record<string, string>): Promise<string> {
  const fs = await import('fs/promises');
  let prompt = await fs.readFile(templatePath, 'utf-8');
  for (const [placeholder, value] of Object.entries(replacements)) {
    prompt = prompt.replace(placeholder, value);
  }
  return prompt;
}
