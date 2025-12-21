import { GoogleGenAI } from '@google/genai';
import Anthropic from '@anthropic-ai/sdk';
import dotenv from 'dotenv';

dotenv.config();

// --- LLM Model Configuration ---
// DO NOT CHANGE THESE MODEL NUMBERS

// Model metadata interface
interface ModelConfig {
  id: string;
  contextLength: number;
  costPer1MInputTokens: number;  // USD per 1M input tokens
  costPer1MOutputTokens: number; // USD per 1M output tokens
}

// Gemini API response types
interface GeminiUsageMetadata {
  promptTokenCount?: number;
  candidatesTokenCount?: number;
  totalTokenCount?: number;
}

interface GeminiResult {
  text?: string;
  usageMetadata?: GeminiUsageMetadata;
}

// Gemini 3 models (current - released Dec 2025)
// https://blog.google/products/gemini/gemini-3-flash/
const GEMINI_FLASH_MODEL_ID = 'gemini-3-flash-preview';
const GEMINI_PRO_MODEL_ID = 'gemini-3-pro-preview'; // Not yet released, use Flash for now

// Claude models
const CLAUDE_OPUS_4_1_MODEL_ID = 'claude-opus-4-1-20250805';
const CLAUDE_SONNET_4_5_MODEL_ID = 'claude-sonnet-4-5-20250929';

// Model configurations with pricing and limits
// Pricing from: https://ai.google.dev/pricing and https://anthropic.com/pricing
const MODEL_CONFIGS: Record<string, ModelConfig> = {
  // Gemini 3 models
  'gemini-3-flash-preview': {
    id: 'gemini-3-flash-preview',
    contextLength: 1000000, // 1M tokens
    costPer1MInputTokens: 0.075,
    costPer1MOutputTokens: 0.30,
  },
  'gemini-3-pro-preview': {
    id: 'gemini-3-pro-preview',
    contextLength: 2000000, // 2M tokens (estimated)
    costPer1MInputTokens: 1.25,
    costPer1MOutputTokens: 5.00,
  },
  // Claude models
  'claude-opus-4-1-20250805': {
    id: 'claude-opus-4-1-20250805',
    contextLength: 200000, // 200K tokens
    costPer1MInputTokens: 15.00,
    costPer1MOutputTokens: 75.00,
  },
  'claude-sonnet-4-5-20250929': {
    id: 'claude-sonnet-4-5-20250929',
    contextLength: 200000, // 200K tokens
    costPer1MInputTokens: 3.00,
    costPer1MOutputTokens: 15.00,
  },
};

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

// --- Token Counting and Cost Estimation ---

/**
 * Rough token count estimator (4 chars ≈ 1 token for English text)
 * For accurate counts, use the API's token counter, but this is good enough for logging
 */
function estimateTokenCount(text: string): number {
  // Average token length is ~4 characters for English
  return Math.ceil(text.length / 4);
}

/**
 * Calculate cost estimate for a request
 */
function calculateCost(inputTokens: number, outputTokens: number, modelId: string): number {
  const config = MODEL_CONFIGS[modelId];
  if (!config) {
    console.warn(`⚠️  Unknown model ${modelId}, cannot estimate cost`);
    return 0;
  }

  const inputCost = (inputTokens / 1_000_000) * config.costPer1MInputTokens;
  const outputCost = (outputTokens / 1_000_000) * config.costPer1MOutputTokens;
  return inputCost + outputCost;
}

/**
 * Check if prompt exceeds context length
 */
function checkContextLength(promptTokens: number, modelId: string): void {
  const config = MODEL_CONFIGS[modelId];
  if (!config) {
    console.warn(`⚠️  Unknown model ${modelId}, cannot check context length`);
    return;
  }

  if (promptTokens > config.contextLength) {
    throw new Error(
      `Prompt exceeds context length for ${modelId}: ${promptTokens.toLocaleString()} > ${config.contextLength.toLocaleString()} tokens`
    );
  }

  // Warn if using >80% of context
  const usagePercent = (promptTokens / config.contextLength) * 100;
  if (usagePercent > 80) {
    console.warn(`⚠️  Using ${usagePercent.toFixed(1)}% of context length (${promptTokens.toLocaleString()} / ${config.contextLength.toLocaleString()} tokens)`);
  }
}

/**
 * Log request details with cost estimate
 */
function logRequest(modelId: string, promptTokens: number): void {
  const config = MODEL_CONFIGS[modelId];
  const contextPercent = config ? ((promptTokens / config.contextLength) * 100).toFixed(1) : 'N/A';

  console.log('─'.repeat(80));
  console.log(`🤖 LLM Request: ${modelId}`);
  console.log(`📝 Input tokens: ${promptTokens.toLocaleString()} (${contextPercent}% of context)`);
  console.log('⏳ Waiting for response...');
}

/**
 * Log response details with cost estimate
 */
function logResponse(modelId: string, inputTokens: number, outputTokens: number, actualUsage?: { inputTokens: number; outputTokens: number }): void {
  // Use actual usage if provided by API, otherwise use estimates
  const finalInputTokens = actualUsage?.inputTokens ?? inputTokens;
  const finalOutputTokens = actualUsage?.outputTokens ?? outputTokens;

  const totalTokens = finalInputTokens + finalOutputTokens;
  const cost = calculateCost(finalInputTokens, finalOutputTokens, modelId);

  console.log(`✅ Response received`);
  console.log(`📊 Output tokens: ${finalOutputTokens.toLocaleString()}`);
  console.log(`📈 Total tokens: ${totalTokens.toLocaleString()}`);
  console.log(`💰 Estimated cost: $${cost.toFixed(6)} USD`);
  console.log('─'.repeat(80));
}

export async function generateGeminiProContent(prompt: string): Promise<string> {
  const inputTokens = estimateTokenCount(prompt);
  checkContextLength(inputTokens, GEMINI_PRO_MODEL_ID);
  logRequest(GEMINI_PRO_MODEL_ID, inputTokens);

  const result = await genAI.models.generateContent({
    model: GEMINI_PRO_MODEL_ID,
    contents: prompt,
  });

  const responseText = result.text || '';
  const outputTokens = estimateTokenCount(responseText);

  // Try to get actual usage from API if available
  const geminiResult = result as GeminiResult;
  const actualUsage = geminiResult.usageMetadata ? {
    inputTokens: geminiResult.usageMetadata.promptTokenCount || inputTokens,
    outputTokens: geminiResult.usageMetadata.candidatesTokenCount || outputTokens,
  } : undefined;

  logResponse(GEMINI_PRO_MODEL_ID, inputTokens, outputTokens, actualUsage);
  return responseText;
}

export async function generateGeminiFlashContent(prompt: string): Promise<string> {
  const inputTokens = estimateTokenCount(prompt);
  checkContextLength(inputTokens, GEMINI_FLASH_MODEL_ID);
  logRequest(GEMINI_FLASH_MODEL_ID, inputTokens);

  const result = await genAI.models.generateContent({
    model: GEMINI_FLASH_MODEL_ID,
    contents: prompt,
  });

  const responseText = result.text || '';
  const outputTokens = estimateTokenCount(responseText);

  // Try to get actual usage from API if available
  const geminiResult = result as GeminiResult;
  const actualUsage = geminiResult.usageMetadata ? {
    inputTokens: geminiResult.usageMetadata.promptTokenCount || inputTokens,
    outputTokens: geminiResult.usageMetadata.candidatesTokenCount || outputTokens,
  } : undefined;

  logResponse(GEMINI_FLASH_MODEL_ID, inputTokens, outputTokens, actualUsage);
  return responseText;
}

export async function generateClaudeOpus41Content(prompt: string): Promise<string> {
  const inputTokens = estimateTokenCount(prompt);
  checkContextLength(inputTokens, CLAUDE_OPUS_4_1_MODEL_ID);
  logRequest(CLAUDE_OPUS_4_1_MODEL_ID, inputTokens);

  const msg = await anthropic.messages.create({
    model: CLAUDE_OPUS_4_1_MODEL_ID,
    max_tokens: 8192,
    messages: [{ role: "user", content: prompt }],
  });

  const responseBlock = msg.content[0];
  if (responseBlock.type !== 'text') {
    throw new Error('Unexpected response format from Anthropic API. Expected a text block.');
  }

  const responseText = responseBlock.text;

  // Claude API provides actual token usage
  const actualUsage = {
    inputTokens: msg.usage.input_tokens,
    outputTokens: msg.usage.output_tokens,
  };

  logResponse(CLAUDE_OPUS_4_1_MODEL_ID, inputTokens, estimateTokenCount(responseText), actualUsage);
  return responseText;
}

export async function generateClaudeSonnet45Content(prompt: string): Promise<string> {
  const inputTokens = estimateTokenCount(prompt);
  checkContextLength(inputTokens, CLAUDE_SONNET_4_5_MODEL_ID);
  logRequest(CLAUDE_SONNET_4_5_MODEL_ID, inputTokens);

  const msg = await anthropic.messages.create({
    model: CLAUDE_SONNET_4_5_MODEL_ID,
    max_tokens: 8192,
    messages: [{ role: "user", content: prompt }],
  });

  const responseBlock = msg.content[0];
  if (responseBlock.type !== 'text') {
    throw new Error('Unexpected response format from Anthropic API. Expected a text block.');
  }

  const responseText = responseBlock.text;

  // Claude API provides actual token usage
  const actualUsage = {
    inputTokens: msg.usage.input_tokens,
    outputTokens: msg.usage.output_tokens,
  };

  logResponse(CLAUDE_SONNET_4_5_MODEL_ID, inputTokens, estimateTokenCount(responseText), actualUsage);
  return responseText;
}

// --- LLM Utility Functions ---

/**
 * Extracts JSON object from LLM response text, handling markdown code blocks
 */
export function extractJsonFromResponse(responseText: string, context: string = 'LLM response'): unknown {
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
