import { config } from 'dotenv';

// Load environment variables
config();

export const availableModels = [
  // OpenAI models
  'gpt-4-turbo',
  'gpt-4',
  'gpt-3.5-turbo',
  // Anthropic models
  'claude-3-opus',
  'claude-3-sonnet',
  'anthropic/claude-3-opus',
  'anthropic/claude-3-sonnet',
  // Perplexity models
  'sonar-small-chat',
  'sonar-medium-chat',
  'sonar-large-chat',
  // Google Gemini models
  'gemini-2.5-pro',
  'gemini-2.5-flash',
  // DeepSeek models
  'deepseek-chat',
  'deepseek-reasoner'
] as const;

export type AvailableModel = typeof availableModels[number];

export const env = {
  OPENAI_API_KEY: process.env.OPENAI_API_KEY,
  ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY,
  PERPLEXITY_API_KEY: process.env.PERPLEXITY_API_KEY,
  GOOGLE_GENERATIVE_AI_API_KEY: process.env.GOOGLE_GENERATIVE_AI_API_KEY,
  DEEPSEEK_API_KEY: process.env.DEEPSEEK_API_KEY,
  AI_MODEL: (process.env.AI_MODEL || 'gemini-2.5-pro') as AvailableModel
}; 