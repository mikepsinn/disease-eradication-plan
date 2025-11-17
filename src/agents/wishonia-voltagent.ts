import { Agent, VoltAgent, Memory } from "@voltagent/core";
import { google } from "@ai-sdk/google";
import { createPinoLogger } from "@voltagent/logger";
import { honoServer } from "@voltagent/server-hono";
import {
  AiSdkEmbeddingAdapter,
  InMemoryVectorAdapter,
} from "@voltagent/core";
import { LibSQLMemoryAdapter } from "@voltagent/libsql";
import { writeFile } from "fs/promises";
import { execSync } from "child_process";
import {
  createParameterCheckerAgent,
  createMathValidatorAgent,
  createClaimValidatorAgent,
  createReferenceLinkerAgent,
  createConsistencyCheckerAgent,
} from "../../scripts/agents/sub-agents";
import { EnhancedTodoManager } from "./todo-manager-enhanced";
import { createFileReviewWorkflow } from "../../scripts/agents/workflows/file-review-workflow";
import { getStaleFilesForWishonia, updateFileHash } from "../../scripts/lib/hash-utils";
import { getBodyHash } from "../../scripts/lib/file-utils";
import { HASH_FIELDS } from "../../scripts/lib/constants";
import { glob } from "glob";

// Create logger
const logger = createPinoLogger({
  name: "wishonia",
  level: "info",
});

// Create shared memory for all agents
const memory = new Memory({
  storage: new LibSQLMemoryAdapter(),
  embedding: new AiSdkEmbeddingAdapter(
    google.textEmbeddingModel("models/text-embedding-004")
  ),
  vector: new InMemoryVectorAdapter(),
});

// Create specialized subagents
const parameterCheckerAgent = createParameterCheckerAgent(memory);
const mathValidatorAgent = createMathValidatorAgent(memory);
const claimValidatorAgent = createClaimValidatorAgent(memory);
const referenceLinkerAgent = createReferenceLinkerAgent(memory);
const consistencyCheckerAgent = createConsistencyCheckerAgent(memory);

// Create WISHONIA supervisor agent
const wishoniaSupervisor = new Agent({
  name: "WISHONIA Supervisor",
  instructions: `You are WISHONIA, a superintelligent AI economist agent.
Your mission is to systematically perfect the book by:
1. Finding hardcoded numbers that should use parameters
2. Identifying mathematical and logical errors
3. Finding unsupported claims
4. Ensuring all numbers link to parameter objects or references
5. Maintaining a comprehensive todo list

You coordinate specialized subagents to check files in parallel:
- Parameter Checker: Finds hardcoded numbers and suggests parameters
- Math Validator: Validates equations and calculations
- Claim Validator: Identifies unsupported claims needing references
- Reference Linker: Ensures all numbers/claims link to sources
- Consistency Checker: Checks cross-file consistency

Guidelines:
- Always maintain a todo list of issues found
- Never commit changes - only stage for review
- Use parallel processing for efficiency
- Track all changes with frontmatter hashes
- Be thorough and systematic`,
  model: google("gemini-2.5-flash"),
  memory,
  subAgents: [
    parameterCheckerAgent,
    mathValidatorAgent,
    claimValidatorAgent,
    referenceLinkerAgent,
    consistencyCheckerAgent,
  ],
  supervisorConfig: {
    fullStreamEventForwarding: {
      types: ["tool-call", "tool-result"],
    },
  },
});

// Create todo manager
const todoManager = new EnhancedTodoManager();

/**
 * Main WISHONIA class
 */
export class WishoniaVoltAgent {
  private voltAgent: VoltAgent;
  private todoManager: EnhancedTodoManager;
  private fileReviewWorkflow: ReturnType<typeof createFileReviewWorkflow>;

  constructor() {
    this.todoManager = todoManager;

    // Create workflow for file processing
    this.fileReviewWorkflow = createFileReviewWorkflow(
      wishoniaSupervisor,
      this.todoManager,
      memory
    );

    this.voltAgent = new VoltAgent({
      agents: {
        wishoniaSupervisor,
        parameterCheckerAgent,
        mathValidatorAgent,
        claimValidatorAgent,
        referenceLinkerAgent,
        consistencyCheckerAgent,
      },
      workflows: {
        fileReview: this.fileReviewWorkflow,
      },
      logger,
      server: honoServer({ port: 3141 }),
    });
  }

  /**
   * Initialize WISHONIA
   */
  async init(): Promise<void> {
    await this.todoManager.loadFromFile();
    logger.info("WISHONIA initialized");
  }

  /**
   * Process a single file
   */
  async processFile(filePath: string): Promise<void> {
    logger.info(`Processing file: ${filePath}`);

    try {
      // Run the file review workflow
      const result = await this.fileReviewWorkflow.run(
        { filePath },
        {
          userId: "wishonia-cli",
          conversationId: `file-review-${filePath}`,
        }
      );

      logger.info(`✅ Processed ${filePath}: Found ${result.totalIssues} issues`);

      // Update hash fields after processing
      const { readFileWithMatter } = await import("../lib/file-utils");
      const { body } = await readFileWithMatter(filePath);
      const currentHash = getBodyHash(body);

      // Update all WISHONIA hash fields
      await updateFileHash(filePath, HASH_FIELDS.PARAMETER_CHECK, currentHash);
      await updateFileHash(filePath, HASH_FIELDS.MATH_VALIDATION, currentHash);
      await updateFileHash(filePath, HASH_FIELDS.CLAIM_VALIDATION, currentHash);
      await updateFileHash(filePath, HASH_FIELDS.REFERENCE_LINKING, currentHash);
      await updateFileHash(filePath, HASH_FIELDS.CONSISTENCY_CHECK, currentHash);
      await updateFileHash(filePath, HASH_FIELDS.WISHONIA_FULL_REVIEW, currentHash);

      // Save todos
      await this.todoManager.save();
    } catch (error) {
      logger.error(`Error processing file ${filePath}:`, error);
      throw error;
    }
  }

  /**
   * Process all stale files
   */
  async processStaleFiles(): Promise<void> {
    logger.info("Finding stale files...");
    const staleFiles = await getStaleFilesForWishonia();
    
    logger.info(`Found ${staleFiles.length} stale files to process`);
    
    for (const file of staleFiles) {
      await this.processFile(file);
    }
    
    logger.info(`✅ Processed ${staleFiles.length} stale files`);
  }

  /**
   * Process all files
   */
  async processAllFiles(): Promise<void> {
    logger.info("Finding all files...");
    const files = await glob("knowledge/**/*.qmd", {
      ignore: ["**/node_modules/**", "**/_book/**", "**/_freeze/**"],
    });
    
    logger.info(`Found ${files.length} files to process`);
    
    for (const file of files) {
      await this.processFile(file);
    }
    
    logger.info(`✅ Processed ${files.length} files`);
  }

  /**
   * Export todo list
   */
  async exportTodoList(): Promise<void> {
    const json = await this.todoManager.exportJSON();
    const yaml = await this.todoManager.exportYAML();
    const markdown = await this.todoManager.exportMarkdown();

    await Promise.all([
      writeFile(".wishonia-todos.json", json, "utf-8"),
      writeFile(".wishonia-todos.yaml", yaml, "utf-8"),
      writeFile(".wishonia-todos.md", markdown, "utf-8"),
    ]);

    console.log("✅ Todo list exported to:");
    console.log("  - .wishonia-todos.json");
    console.log("  - .wishonia-todos.yaml");
    console.log("  - .wishonia-todos.md");
  }

  /**
   * Print status
   */
  async printStatus(): Promise<void> {
    const todos = this.todoManager.getAllTodos();
    const byStatus = todos.reduce(
      (acc, todo) => {
        acc[todo.status] = (acc[todo.status] || 0) + 1;
        return acc;
      },
      {} as Record<string, number>
    );
    const byType = todos.reduce(
      (acc, todo) => {
        acc[todo.type] = (acc[todo.type] || 0) + 1;
        return acc;
      },
      {} as Record<string, number>
    );

    console.log("\n📊 WISHONIA Status\n");
    console.log(`Total Todos: ${todos.length}\n`);
    console.log("By Status:");
    for (const [status, count] of Object.entries(byStatus)) {
      console.log(`  ${status}: ${count}`);
    }
    console.log("\nBy Type:");
    for (const [type, count] of Object.entries(byType)) {
      console.log(`  ${type}: ${count}`);
    }
    console.log();
  }

  /**
   * Stage changes (never commit)
   */
  async stageChanges(): Promise<void> {
    logger.info("Staging changes for review");
    
    try {
      // Stage all modified files (but not new files to avoid accidental commits)
      execSync("git add -u", { stdio: "inherit" });
      
      // Stage todo files if they exist
      try {
        execSync("git add .wishonia-todos.*", { stdio: "pipe" });
      } catch {
        // Ignore if no todo files
      }
      
      logger.info("✅ Changes staged (not committed)");
    } catch (error) {
      logger.warn("Could not stage changes:", error);
      // Don't throw - staging is optional
    }
  }
}
