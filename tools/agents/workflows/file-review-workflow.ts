import { createWorkflowChain } from "@voltagent/core";
import { z } from "zod";
import { readFileWithMatter, getBodyHash } from "../../lib/file-utils";
import { readFile } from "fs/promises";
import { EnhancedTodoManager, type EnhancedTodo } from "../todo-manager-enhanced";
import { calculateTodoPriority } from "../../lib/hash-utils";
import type { Agent } from "@voltagent/core";
import { createParameterCheckerAgent, createMathValidatorAgent, createClaimValidatorAgent, createReferenceLinkerAgent, createConsistencyCheckerAgent } from "../sub-agents";

/**
 * Helper function to call an agent and parse structured response
 */
async function callAgentForReview(
  agent: Agent,
  prompt: string,
  schema: z.ZodSchema
): Promise<any[]> {
  try {
    // Use generateObject for structured output
    const response = await agent.generateObject(prompt, schema);
    
    // Extract issues from the response object
    const parsed = response.object as any;
    return parsed.issues || parsed.items || [];
  } catch (error) {
    console.error(`Error calling agent ${agent.name}:`, error);
    // Return empty array on error to allow workflow to continue
    return [];
  }
}

/**
 * File Review Workflow
 * Processes a file through all WISHONIA checks in parallel
 */
export function createFileReviewWorkflow(
  supervisorAgent: Agent,
  todoManager: EnhancedTodoManager,
  memory?: any
) {
  // Create agents for direct calls (not via supervisor for workflow)
  const parameterAgent = createParameterCheckerAgent(memory);
  const mathAgent = createMathValidatorAgent(memory);
  const claimAgent = createClaimValidatorAgent(memory);
  const referenceAgent = createReferenceLinkerAgent(memory);
  const consistencyAgent = createConsistencyCheckerAgent(memory);
  return createWorkflowChain({
    id: "file-review",
    name: "File Review Workflow",
    input: z.object({
      filePath: z.string(),
    }),
    result: z.object({
      issues: z.array(
        z.object({
          type: z.enum(["parameter", "math", "claim", "reference", "consistency"]),
          line: z.number(),
          issue: z.string(),
          suggestedFix: z.string().optional(),
          confidence: z.enum(["high", "medium", "low"]),
          link: z.string().optional(),
        })
      ),
      fixes: z.array(
        z.object({
          type: z.string(),
          line: z.number(),
          oldValue: z.string(),
          newValue: z.string(),
        })
      ),
    }),
  })
    .andThen({
      id: "load-file",
      execute: async ({ data }) => {
        const { body, frontmatter } = await readFileWithMatter(data.filePath);
        
        // Load parameters and variables
        let parameters = {};
        let variables = {};
        
        try {
          const paramsContent = await readFile("dih_models/parameters.py", "utf-8");
          // Store as string for now - agents can parse if needed
          parameters = { content: paramsContent };
        } catch (error) {
          console.warn("Could not load parameters.py:", error);
        }

        try {
          const varsContent = await readFile("_variables.yml", "utf-8");
          variables = { content: varsContent };
        } catch (error) {
          console.warn("Could not load _variables.yml:", error);
        }

        return {
          ...data,
          fileContent: body,
          frontmatter,
          parameters,
          variables,
        };
      },
    })
    .andAll([
      {
        id: "check-parameters",
        execute: async ({ data, getStepData }) => {
          const fileData = getStepData("load-file")?.output;
          if (!fileData) throw new Error("File data not loaded");

          const prompt = `Review this file for hardcoded numbers that should use parameters:

File: ${data.filePath}
Content:
${fileData.fileContent.substring(0, 5000)}${fileData.fileContent.length > 5000 ? '...' : ''}

Available parameters:
${fileData.parameters.content ? fileData.parameters.content.substring(0, 2000) : 'None loaded'}

Find all hardcoded numbers and suggest appropriate parameters from dih_models/parameters.py or _variables.yml.
Return a JSON array of issues with: type, line, issue, suggestedFix, confidence, link.`;

          const schema = z.object({
            issues: z.array(z.object({
              type: z.literal("parameter"),
              line: z.number(),
              issue: z.string(),
              suggestedFix: z.string().optional(),
              confidence: z.enum(["high", "medium", "low"]),
              link: z.string().optional(),
            })),
          });

          const issues = await callAgentForReview(parameterAgent, prompt, schema);
          return { parameterIssues: issues };
        },
      },
      {
        id: "check-math",
        execute: async ({ data, getStepData }) => {
          const fileData = getStepData("load-file")?.output;
          if (!fileData) throw new Error("File data not loaded");

          const prompt = `Validate all mathematical equations and calculations in this file:

File: ${data.filePath}
Content:
${fileData.fileContent.substring(0, 5000)}${fileData.fileContent.length > 5000 ? '...' : ''}

Check for LaTeX syntax errors, calculation errors, unit mismatches, and formula consistency.
Return a JSON array of issues with: type, line, issue, suggestedFix, confidence.`;

          const schema = z.object({
            issues: z.array(z.object({
              type: z.literal("math"),
              line: z.number(),
              issue: z.string(),
              suggestedFix: z.string().optional(),
              confidence: z.enum(["high", "medium", "low"]),
            })),
          });

          const issues = await callAgentForReview(mathAgent, prompt, schema);
          return { mathIssues: issues };
        },
      },
      {
        id: "check-claims",
        execute: async ({ data, getStepData }) => {
          const fileData = getStepData("load-file")?.output;
          if (!fileData) throw new Error("File data not loaded");

          const prompt = `Identify unsupported claims that need references in this file:

File: ${data.filePath}
Content:
${fileData.fileContent.substring(0, 5000)}${fileData.fileContent.length > 5000 ? '...' : ''}

Find statistical, historical, scientific, or economic claims without sources.
Return a JSON array of issues with: type, line, issue, suggestedFix, confidence, link.`;

          const schema = z.object({
            issues: z.array(z.object({
              type: z.literal("claim"),
              line: z.number(),
              issue: z.string(),
              suggestedFix: z.string().optional(),
              confidence: z.enum(["high", "medium", "low"]),
              link: z.string().optional(),
            })),
          });

          const issues = await callAgentForReview(claimAgent, prompt, schema);
          return { claimIssues: issues };
        },
      },
      {
        id: "check-references",
        execute: async ({ data, getStepData }) => {
          const fileData = getStepData("load-file")?.output;
          if (!fileData) throw new Error("File data not loaded");

          const prompt = `Ensure all numbers and claims link to proper sources in this file:

File: ${data.filePath}
Content:
${fileData.fileContent.substring(0, 5000)}${fileData.fileContent.length > 5000 ? '...' : ''}

Check that numbers link to dih_models/parameters.py, calculations, or knowledge/references.qmd.
Return a JSON array of issues with: type, line, issue, suggestedFix, confidence, link.`;

          const schema = z.object({
            issues: z.array(z.object({
              type: z.literal("reference"),
              line: z.number(),
              issue: z.string(),
              suggestedFix: z.string().optional(),
              confidence: z.enum(["high", "medium", "low"]),
              link: z.string().optional(),
            })),
          });

          const issues = await callAgentForReview(referenceAgent, prompt, schema);
          return { referenceIssues: issues };
        },
      },
      {
        id: "check-consistency",
        execute: async ({ data, getStepData }) => {
          const fileData = getStepData("load-file")?.output;
          if (!fileData) throw new Error("File data not loaded");

          const prompt = `Check cross-file consistency for this file:

File: ${data.filePath}
Content:
${fileData.fileContent.substring(0, 5000)}${fileData.fileContent.length > 5000 ? '...' : ''}

Check that same numbers use same parameters, terminology is consistent, and references are valid.
Return a JSON array of issues with: type, line, issue, suggestedFix, confidence.`;

          const schema = z.object({
            issues: z.array(z.object({
              type: z.literal("consistency"),
              line: z.number(),
              issue: z.string(),
              suggestedFix: z.string().optional(),
              confidence: z.enum(["high", "medium", "low"]),
            })),
          });

          const issues = await callAgentForReview(consistencyAgent, prompt, schema);
          return { consistencyIssues: issues };
        },
      },
    ])
    .andThen({
      id: "consolidate-issues",
      execute: async ({ data, getStepData }) => {
        const fileData = getStepData("load-file")?.output;
        const parameterData = getStepData("check-parameters")?.output;
        const mathData = getStepData("check-math")?.output;
        const claimData = getStepData("check-claims")?.output;
        const referenceData = getStepData("check-references")?.output;
        const consistencyData = getStepData("check-consistency")?.output;

        // Combine all issues
        const allIssues: EnhancedTodo["type"][] = [];
        const fixes: Array<{
          type: string;
          line: number;
          oldValue: string;
          newValue: string;
        }> = [];

        // Process each type of issue
        const processIssues = (
          issues: any[],
          type: EnhancedTodo["type"],
          agentId: string
        ) => {
          for (const issue of issues) {
            const todo: EnhancedTodo = {
              id: todoManager.generateId(),
              type,
              priority: calculateTodoPriority(type, issue.confidence || "medium"),
              filePath: data.filePath,
              line: issue.line || 0,
              issue: issue.issue || issue.description || "Issue found",
              suggestedFix: issue.suggestedFix,
              confidence: issue.confidence || "medium",
              status: "pending",
              agentId,
              createdAt: new Date().toISOString(),
              updatedAt: new Date().toISOString(),
            };

            todoManager.addTodo(todo);
            allIssues.push(type);

            if (issue.oldValue && issue.newValue) {
              fixes.push({
                type,
                line: issue.line || 0,
                oldValue: issue.oldValue,
                newValue: issue.newValue,
              });
            }
          }
        };

        // Process issues from each check
        if (parameterData?.parameterIssues) {
          processIssues(parameterData.parameterIssues, "parameter", "Parameter Checker");
        }
        if (mathData?.mathIssues) {
          processIssues(mathData.mathIssues, "math", "Math Validator");
        }
        if (claimData?.claimIssues) {
          processIssues(claimData.claimIssues, "claim", "Claim Validator");
        }
        if (referenceData?.referenceIssues) {
          processIssues(referenceData.referenceIssues, "reference", "Reference Linker");
        }
        if (consistencyData?.consistencyIssues) {
          processIssues(consistencyData.consistencyIssues, "consistency", "Consistency Checker");
        }

        return {
          issues: allIssues.map((type, index) => ({
            type,
            line: 0,
            issue: `Issue ${index + 1}`,
            confidence: "medium" as const,
          })),
          fixes,
        };
      },
    });
}

