declare module './env' {
  export const availableModels: readonly [
    'gpt-4-turbo',
    'gpt-4',
    'gpt-3.5-turbo',
    'claude-3-opus',
    'claude-3-sonnet',
    'anthropic/claude-3-opus',
    'anthropic/claude-3-sonnet',
    'sonar-small-chat',
    'sonar-medium-chat',
    'sonar-large-chat',
    'gemini-2.0-flash-exp',
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    'deepseek-chat',
    'deepseek-reasoner'
  ];

  export type AvailableModel = typeof availableModels[number];

  export const env: {
    OPENAI_API_KEY?: string;
    ANTHROPIC_API_KEY?: string;
    PERPLEXITY_API_KEY?: string;
    GOOGLE_GENERATIVE_AI_API_KEY?: string;
    DEEPSEEK_API_KEY?: string;
    OPENAI_MODEL: AvailableModel;
  };
} 