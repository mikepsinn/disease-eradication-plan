import { createWorkflowChain, MemoryManager } from '@voltagent/core';
import { z } from 'zod';
import { generateRepositoryIndex, findNextFileToReview, prepareAgentContext, executePlan } from '../tasks/maintenance-tasks';
import { executiveDirectorAgent } from '../agents';

// Define the structured output schema for the agent's analysis
export const analysisPlanSchema = z.object({
  decision: z.enum(['DELETE', 'CONSOLIDATE', 'REWRITE', 'CREATE_ISSUE', 'NO_ACTION'])
    .describe('The final decision for the file.'),
  reasoning: z.string()
    .describe('A detailed explanation of why this decision was made, referencing the repository index and project goals.'),
  targetFiles: z.array(z.string())
    .describe('An array of file paths this plan applies to. Usually one, but can be multiple for consolidation.'),
  newContent: z.string().optional()
    .describe('The full new content if the decision is REWRITE or CONSOLIDATE.'),
  issueTitle: z.string().optional()
    .describe('The title for the new issue if the decision is CREATE_ISSUE.'),
  issueDescription: z.string().optional()
    .describe('The description for the new issue if the decision is CREATE_ISSUE.'),
});

export type AnalysisPlan = z.infer<typeof analysisPlanSchema>;


// Define the main maintenance workflow by chaining the implementation functions directly.
export const maintenanceWorkflow = createWorkflowChain({
  id: 'repository-maintenance-workflow',
  inputSchema: z.object({}), // No initial input required
  outputSchema: z.any(),
  memory: new MemoryManager(),
})
  .andThen({
    id: 'generate-index',
    execute: generateRepositoryIndex,
  })
  .andThen({
    id: 'find-next-file',
    execute: findNextFileToReview,
  })
  .andThen({
    id: 'prepare-agent-context',
    execute: prepareAgentContext,
  })
  .andAgent(
    (context) => {
        if (!context.result) {
            return null; // Stop the workflow if there's no file to analyze
        }
        const { fileContent, filePath, index } = context.result;
        return `
            Here is the full repository index for your context:
            ${JSON.stringify(index, null, 2)}

            Now, please analyze the following file:
            File Path: ${filePath}
            File Content:
            ---
            ${fileContent}
            ---
        `;
    },
    executiveDirectorAgent, {
        id: 'analyze-file',
        outputSchema: analysisPlanSchema
    }
  )
  .andThen({
    id: 'execute-plan',
    execute: executePlan,
  });
