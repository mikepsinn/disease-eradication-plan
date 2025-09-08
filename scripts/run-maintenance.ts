import { generateRepositoryIndex, findNextFileToReview, prepareAgentContext, executePlan } from '../agent/src/tasks/maintenance-tasks';
import { executiveDirectorAgent } from '../agent/src/agents';
import { analysisPlanSchema } from '../agent/src/workflows/maintenance';

async function run() {
  console.log('🚀 Manually starting repository maintenance script...');
  try {
    // Step 1: Generate the index
    const { index } = await generateRepositoryIndex();

    // Step 2: Find the next file to review
    const { filePath } = await findNextFileToReview({ index });

    // Step 3: Prepare the context for the agent
    const agentContext = await prepareAgentContext({ index, filePath });

    if (!agentContext) {
      console.log('✅ No files need reviewing. Maintenance complete.');
      return;
    }

    // Step 4: Run the agent for analysis
    console.log(`[Agent] Analyzing file: ${agentContext.filePath}...`);
    const agentInput = `
      Here is the full repository index for your context:
      ${JSON.stringify(agentContext.index, null, 2)}

      Now, please analyze the following file:
      File Path: ${agentContext.filePath}
      File Content:
      ---
      ${agentContext.fileContent}
      ---
    `;
    const { object: plan } = await executiveDirectorAgent.generateObject(
      agentInput,
      analysisPlanSchema
    );

    console.log('[Agent] Analysis complete. Plan received:', plan);

    // Step 5: Execute the plan
    const executionResult = await executePlan(plan);

    console.log('✅ Script finished successfully.');
    console.log('Final Result:', executionResult);

  } catch (error) {
    console.error('❌ Script failed:', error);
  }
}

run();
