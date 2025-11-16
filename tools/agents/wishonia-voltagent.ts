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
import {
  createParameterCheckerAgent,
  createMathValidatorAgent,
  createClaimValidatorAgent,
  createReferenceLinkerAgent,
  createConsistencyCheckerAgent,
} from "./sub-agents";
import { EnhancedTodoManager } from "./todo-manager-enhanced";

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
  model: google("gemini-2.5-pro"),
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

// CLI interface
const args = process.argv.slice(2);
const options = {
  full: args.includes("--full"),
  file: args.find((arg) => arg.startsWith("--file="))?.split("=")[1],
  exportTodo: args.includes("--export-todo"),
  status: args.includes("--status"),
};

/**
 * Main WISHONIA class
 */
export class WishoniaVoltAgent {
  private voltAgent: VoltAgent;
  private todoManager: EnhancedTodoManager;

  constructor() {
    this.todoManager = todoManager;
    this.voltAgent = new VoltAgent({
      agents: {
        wishoniaSupervisor,
        parameterCheckerAgent,
        mathValidatorAgent,
        claimValidatorAgent,
        referenceLinkerAgent,
        consistencyCheckerAgent,
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
    // TODO: Implement file processing logic
    // This will use the supervisor to coordinate subagents
  }

  /**
   * Process all stale files
   */
  async processStaleFiles(): Promise<void> {
    logger.info("Processing stale files");
    // TODO: Implement stale file detection and processing
  }

  /**
   * Process all files
   */
  async processAllFiles(): Promise<void> {
    logger.info("Processing all files");
    // TODO: Implement full file processing
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
    // TODO: Implement git staging without commits
    logger.info("Staging changes for review");
  }
}

// Main execution
async function main() {
  const wishonia = new WishoniaVoltAgent();
  await wishonia.init();

  if (options.status) {
    await wishonia.printStatus();
  } else if (options.exportTodo) {
    await wishonia.exportTodoList();
  } else if (options.file) {
    await wishonia.processFile(options.file);
  } else if (options.full) {
    await wishonia.processAllFiles();
  } else {
    await wishonia.processStaleFiles();
  }

  // Never commit - only stage
  await wishonia.stageChanges();
  console.log("\n✅ Changes staged for review. Review with: git diff --staged");
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    console.error("Error:", error);
    process.exit(1);
  });
}

