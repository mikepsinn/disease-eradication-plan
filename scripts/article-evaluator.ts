import { z } from 'zod';
import { streamObject } from 'ai';
import { createOpenAI } from '@ai-sdk/openai';
import { createAnthropic } from '@ai-sdk/anthropic';
import { createPerplexity } from '@ai-sdk/perplexity';
import { google } from '@ai-sdk/google';
import { deepseek } from '@ai-sdk/deepseek';
import { env, AvailableModel } from './env';

// Define the schema for article assessment
const ArticleAssessmentSchema = z.object({
  qualityScore: z.number()
    .min(0)
    .max(100)
    .describe('Quality score between 0-100'),
  improvements: z.array(z.string())
    .describe('List of specific improvements needed'),
  recommendations: z.object({
    shouldDelete: z.boolean()
      .describe('Whether the article should be deleted'),
    shouldRename: z.string()
      .optional()
      .describe('New suggested name if rename is recommended'),
    priority: z.number()
      .min(1)
      .max(5)
      .describe('Priority level for addressing this content (1-5)')
  })
});

export type ArticleAssessment = z.infer<typeof ArticleAssessmentSchema>;

// Initialize providers
const openai = createOpenAI({
  apiKey: env.OPENAI_API_KEY || ''
});

const anthropic = createAnthropic({
  apiKey: env.ANTHROPIC_API_KEY || ''
});

const perplexity = createPerplexity({
  apiKey: env.PERPLEXITY_API_KEY || ''
});

// Configure AI providers
const providers: Record<AvailableModel, () => any> = {
  // OpenAI models
  'gpt-4-turbo': () => openai('gpt-4-turbo'),
  'gpt-4': () => openai('gpt-4'),
  'gpt-3.5-turbo': () => openai('gpt-3.5-turbo'),
  // Anthropic models
  'claude-3-opus': () => anthropic('claude-3-opus'),
  'claude-3-sonnet': () => anthropic('claude-3-sonnet'),
  'anthropic/claude-3-opus': () => anthropic('claude-3-opus'),
  'anthropic/claude-3-sonnet': () => anthropic('claude-3-sonnet'),
  // Perplexity models
  'sonar-small-chat': () => perplexity('sonar-small-chat'),
  'sonar-medium-chat': () => perplexity('sonar-medium-chat'),
  'sonar-large-chat': () => perplexity('sonar-large-chat'),
  // Google Gemini models
  'gemini-2.0-flash-exp': () => google('gemini-2.0-flash-exp'),
  'gemini-1.5-flash': () => google('gemini-1.5-flash'),
  'gemini-1.5-pro': () => google('gemini-1.5-pro'),
  // DeepSeek models
  'deepseek-chat': () => deepseek('deepseek-chat'),
  'deepseek-reasoner': () => deepseek('deepseek-reasoner')
};

const SYSTEM_PROMPT = `You are an expert analyst for a decentralized FDA wiki documentation project. 
Your task is to analyze markdown content and provide quality assessment and recommendations.

The wiki's goal is to document the design, implementation and strategy for upgrading the FDA to be an open-source amazon for decentralized trials where:
1. Anyone can effortlessly create or participate in decentralized trials
2. There are global comparative effectiveness rankings
3. All foods and drugs have outcome labels for positive and negative effects
4. Each person has a personal FDAi agent (superintelligent AI doctor) to collect data and update the database

Rate the content's quality and provide specific improvements needed.`;

export async function evaluateArticle(content: string, filePath: string): Promise<ArticleAssessment> {
  try {
    const modelName = env.AI_MODEL;
    const provider = providers[modelName];
    
    if (!provider) {
      throw new Error(`Unsupported model: ${modelName}`);
    }

    const result = await streamObject({
      model: provider(),
      schema: ArticleAssessmentSchema,
      system: SYSTEM_PROMPT,
      prompt: `Analyze this content from ${filePath}:\n\n${content}`,
      onFinish({ object, error, usage }) {
        if (error) {
          console.error(`Error evaluating ${filePath}:`, error);
        } else {
          console.log(`Evaluated ${filePath} (${usage?.totalTokens} tokens used)`);
        }
      }
    });

    // Wait for the final object
    const assessment = await result.object;
    return assessment;

  } catch (error) {
    console.error(`Error evaluating article ${filePath}:`, error);
    return {
      qualityScore: 0,
      improvements: ['Error analyzing content'],
      recommendations: {
        shouldDelete: false,
        priority: 1
      }
    };
  }
} 