import { Agent, createWorkflowChain } from "@voltagent/core";
import { z } from "zod";
import { EnhancedTodoManager, EnhancedTodo } from "../todo-manager-enhanced";
import { readFile } from "fs/promises";
import type { Memory } from "@voltagent/core";
import { randomUUID } from "crypto";

// Input schema for the workflow
const FileReviewInput = z.object({
  filePath: z.string().describe("Path to the .qmd file to review"),
});

// Result schema for the workflow
const FileReviewResult = z.object({
  filePath: z.string(),
  issues: z.array(
    z.object({
      type: z.enum([
        "parameter",
        "math",
        "claim",
        "reference",
        "consistency",
      ]),
      priority: z.enum(["critical", "high", "medium", "low"]),
      description: z.string(),
      suggestedFix: z.string().optional(),
      lineNumber: z.number().optional(),
      confidence: z.number().min(0).max(1).optional(),
    })
  ),
  totalIssues: z.number(),
});

/**
 * Create a workflow for reviewing files with all subagents
 */
export function createFileReviewWorkflow(
  supervisor: Agent,
  todoManager: EnhancedTodoManager,
  memory: Memory
) {
  return createWorkflowChain({
    id: "file-review",
    name: "File Review Workflow",
    input: FileReviewInput,
    result: FileReviewResult,
  })
    .andThen({
      id: "load-file",
      execute: async ({ data }) => {
        const { filePath } = data as { filePath: string };
        const content = await readFile(filePath, "utf-8");
        return { filePath, content };
      },
    })
    .andThen({
      id: "review-file",
      execute: async ({ data }) => {
        const { filePath, content } = data as { filePath: string; content: string };
        const prompt = `Review this file for issues: ${filePath}

Content:
\`\`\`
${content}
\`\`\`

Please analyze this file for:
1. Hardcoded numbers that should be parameters
2. Mathematical errors or unclear calculations
3. Claims that need citations
4. Numbers/claims that don't link to sources
5. Inconsistencies with other parts of the book

For each issue found, provide:
- Type: parameter|math|claim|reference|consistency
- Priority: critical|high|medium|low
- Description: What the issue is
- SuggestedFix: How to fix it (optional)
- LineNumber: Approximate line number (optional)
- Confidence: Your confidence level 0-1 (optional)

Return a JSON object with this exact structure:
{
  "issues": [
    {
      "type": "parameter",
      "priority": "high",
      "description": "...",
      "suggestedFix": "...",
      "lineNumber": 42,
      "confidence": 0.9
    }
  ]
}`;

      const issuesSchema = z.object({
        issues: z.array(
          z.object({
            type: z.enum([
              "parameter",
              "math",
              "claim",
              "reference",
              "consistency",
            ]),
            priority: z.enum(["critical", "high", "medium", "low"]),
            description: z.string(),
            suggestedFix: z.string().optional(),
            lineNumber: z.number().optional(),
            confidence: z.number().min(0).max(1).optional(),
          })
        ),
      });

      console.log("Calling supervisor.generateObject()...");
      const result = await supervisor.generateObject(prompt, issuesSchema);

      console.log("Got result from agent:", JSON.stringify(result.object, null, 2));

      return {
        filePath,
        content,
        issues: result.object.issues,
      };
      },
    })
    .andThen({
      id: "add-todos",
      execute: async ({ data }) => {
        console.log("add-todos step received data:", JSON.stringify(data, null, 2));
        const { filePath, issues } = data as any;

      // Add each issue as a todo
      for (const issue of issues) {
        // Convert confidence from 0-1 to low/medium/high
        let confidenceLevel: "low" | "medium" | "high" = "medium";
        if (issue.confidence !== undefined) {
          if (issue.confidence >= 0.75) confidenceLevel = "high";
          else if (issue.confidence >= 0.5) confidenceLevel = "medium";
          else confidenceLevel = "low";
        }

        const todo: EnhancedTodo = {
          id: randomUUID(),
          type: issue.type,
          priority: issue.priority,
          status: "pending",
          filePath: filePath,
          line: issue.lineNumber || 0,
          issue: issue.description,
          suggestedFix: issue.suggestedFix,
          confidence: confidenceLevel,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };

        todoManager.addTodo(todo);
      }

        return {
          filePath,
          issues,
          totalIssues: issues.length,
        };
      },
    });
}
