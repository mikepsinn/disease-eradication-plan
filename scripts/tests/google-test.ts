import { generateObject } from 'ai';
import { google } from '@ai-sdk/google';
import { z } from 'zod/v3';
import { env } from '../env';

async function runGoogleTest() {
  console.log('--- Starting Minimal Google API Test ---');
  
  if (!env.GOOGLE_GENERATIVE_AI_API_KEY) {
    console.error('Error: GOOGLE_GENERATIVE_AI_API_KEY is not set in the environment.');
    process.exit(1);
  }

  const modelName = 'gemini-1.5-pro-latest';
  console.log(`Using model: ${modelName}`);

  try {
    const { object } = await generateObject({
      model: google(modelName),
      schema: z.object({
        sentiment: z.enum(['positive', 'negative', 'neutral']),
      }),
      prompt: 'Analyze the sentiment of the following sentence: "The 1% Treaty is an audacious plan to reshape global priorities."',
    });

    console.log('\n--- Test SUCCEEDED ---');
    console.log('API call was successful. Received object:');
    console.log(JSON.stringify(object, null, 2));

  } catch (error) {
    console.error('\n--- Test FAILED ---');
    console.error('The API call failed with the following error:');
    console.error(error);
    process.exit(1);
  }
}

runGoogleTest();
