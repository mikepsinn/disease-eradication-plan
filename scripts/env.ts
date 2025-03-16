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
  'gemini-2.0-flash-exp',
  'gemini-1.5-flash',
  'gemini-1.5-pro',
  // DeepSeek models
  'deepseek-chat',
  'deepseek-reasoner'
] as const;

export type AvailableModel = typeof availableModels[number];

export const env = {
  OPENAI_API_KEY: process.env.OPENAI_API_KEY,
  ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY,
  PERPLEXITY_API_KEY: process.env.PERPLEXITY_API_KEY,
  GOOGLE_API_KEY: process.env.GOOGLE_API_KEY,
  DEEPSEEK_API_KEY: process.env.DEEPSEEK_API_KEY,
  OPENAI_MODEL: (process.env.OPENAI_MODEL || 'gpt-4-turbo') as AvailableModel
}; 