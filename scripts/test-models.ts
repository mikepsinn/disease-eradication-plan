import { availableModels } from './env';
import { config } from 'dotenv';
import { evaluateArticle } from './article-evaluator';

// Load environment variables
config();

const sampleContent = `# Decentralized Clinical Trials

## Overview
Decentralized clinical trials (DCTs) leverage digital technologies and remote monitoring to conduct trials outside traditional clinical settings. This approach increases accessibility, reduces costs, and improves participant diversity.

## Key Benefits
- Broader participant access
- Real-time data collection
- Reduced site visits
- Lower operational costs
- Improved participant retention

## Implementation Challenges
- Data security and privacy
- Technology adoption barriers
- Regulatory compliance
- Protocol standardization

## Future Directions
We need to establish clear guidelines for:
1. Remote consent processes
2. Data validation methods
3. Quality control procedures`;

async function testModel(modelName: string) {
  console.log(`\nTesting model: ${modelName}`);
  console.log('='.repeat(50));

  try {
    // Override the model in process.env
    process.env.OPENAI_MODEL = modelName;

    const result = await evaluateArticle(sampleContent, 'test/decentralized-trials.md');
    
    console.log('Quality Score:', result.qualityScore);
    console.log('\nImprovements:');
    result.improvements.forEach((improvement, i) => {
      console.log(`${i + 1}. ${improvement}`);
    });
    
    console.log('\nRecommendations:');
    console.log('- Delete:', result.recommendations.shouldDelete);
    if (result.recommendations.shouldRename) {
      console.log('- Rename to:', result.recommendations.shouldRename);
    }
    console.log('- Priority:', result.recommendations.priority);

  } catch (error) {
    console.error(`Error with model ${modelName}:`, error);
  }
}

async function runTests() {
  // Get available API keys
  const apiKeys = {
    'gpt': process.env.OPENAI_API_KEY,
    'claude': process.env.ANTHROPIC_API_KEY,
    'sonar': process.env.PERPLEXITY_API_KEY,
    'gemini': process.env.GOOGLE_GENERATIVE_AI_API_KEY,
    'deepseek': process.env.DEEPSEEK_API_KEY
  };

  // Filter models based on available API keys
  const availableProviders = new Set(
    Object.entries(apiKeys)
      .filter(([_, key]) => key)
      .map(([provider]) => provider)
  );

  const testableModels = availableModels.filter(model => {
    if (model.startsWith('gpt')) return availableProviders.has('gpt');
    if (model.startsWith('claude') || model.includes('anthropic')) return availableProviders.has('claude');
    if (model.startsWith('sonar')) return availableProviders.has('sonar');
    if (model.startsWith('gemini')) return availableProviders.has('gemini');
    if (model.startsWith('deepseek')) return availableProviders.has('deepseek');
    return false;
  });

  if (testableModels.length === 0) {
    console.error('No models available for testing. Please check your API keys in .env file.');
    return;
  }

  console.log('Models available for testing:', testableModels);
  console.log('\nStarting tests...\n');

  for (const model of testableModels) {
    await testModel(model);
  }
}

if (require.main === module) {
  runTests().catch(console.error);
} 