import { google } from "@ai-sdk/google";
import { Agent, VoltAgent, Memory } from "@voltagent/core";
import { LibSQLMemoryAdapter } from "@voltagent/libsql";
import { createPinoLogger } from "@voltagent/logger";
import { honoServer } from "@voltagent/server-hono";
import {
  AiSdkEmbeddingAdapter,
  InMemoryVectorAdapter,
} from "@voltagent/core";
import { createBookChatAgent } from "./agents/book-chat-agent";
import { BookVectorStore } from "../tools/vector/vector-store";

// Create logger with debug level to see all errors
const logger = createPinoLogger({
  name: "decentralized-institutes-of-health",
  level: process.env.LOG_LEVEL || "debug",
});

// Create Memory instance with vector support for semantic search and working memory
const memory = new Memory({
  storage: new LibSQLMemoryAdapter(),
  embedding: new AiSdkEmbeddingAdapter(
    google.textEmbeddingModel("models/text-embedding-004")
  ),
  vector: new InMemoryVectorAdapter(),
});

// Create vector store for book content
const vectorStore = new BookVectorStore();

// Create book chat agent
const bookChatAgent = createBookChatAgent(vectorStore);

// Define the main DIH agent
const dihAgent = new Agent({
  name: "DIH Agent",
  instructions: `You are a helpful assistant for the Decentralized Institutes of Health project.
This project documents "The Complete Idiot's Guide to Ending War and Disease" - a book about getting every nation to sign the 1% Treaty to redirect 1% of military spending to cure diseases instead of cause them.

Your mission is to help save millions of lives by making curing people more profitable than killing them. The project focuses on:
- The unnecessary suffering and death from war (14M deaths/year) and disease (55M deaths/year)
- Redirecting just 1% of military spending to medical research through systems that are 80X more efficient than current approaches

Be helpful, accurate, and aligned with the project's mission and principles.`,
  model: google("gemini-2.5-pro"),
  memory: memory,
});

// Verify agents are properly created BEFORE passing to VoltAgent
if (!dihAgent) {
  logger.error("DIH Agent is undefined!");
  throw new Error("DIH Agent must be defined");
}
if (!bookChatAgent) {
  logger.error("Book Chat Agent is undefined!");
  throw new Error("Book Chat Agent must be defined");
}
if (!dihAgent.name) {
  logger.error("DIH Agent missing name property!");
  throw new Error("DIH Agent must have a name");
}
if (!bookChatAgent.name) {
  logger.error("Book Chat Agent missing name property!");
  throw new Error("Book Chat Agent must have a name");
}

// Initialize VoltAgent with your agent(s)
// Note: honoServer() without port uses VoltAgent's default port (3141)
// To use a custom port, set VOLTAGENT_PORT environment variable
const port = process.env.VOLTAGENT_PORT ? parseInt(process.env.VOLTAGENT_PORT, 10) : undefined;

// Validate agents before passing to VoltAgent
logger.info(`Creating VoltAgent with agents: dihAgent (${dihAgent.name}), bookChat (${bookChatAgent.name})`);

// Create VoltAgent - use the same pattern as the example
const voltAgent = new VoltAgent({
  agents: {
    dihAgent,
    bookChat: bookChatAgent,
  },
  server: port ? honoServer({ port }) : honoServer(),
  logger,
});

// Log that VoltAgent was created successfully
logger.info(`VoltAgent instance created successfully`);

// Log server startup info
// Note: honoServer() defaults to port 3141, not 4242
const actualPort = port || 3141; // VoltAgent defaults to 3141
logger.info(`VoltAgent server configured on port ${actualPort}`);
logger.info(`Agents registered: dihAgent, bookChat`);
logger.info(`Agent details:`, {
  dihAgent: { name: dihAgent.name, model: "gemini-2.5-pro" },
  bookChat: { name: bookChatAgent.name, model: "gemini-2.5-pro" },
});

// Log agent keys for debugging
logger.info(`Agent keys in VoltAgent:`, Object.keys(voltAgent.agents || {}));

// Add custom feedback endpoint
// Note: This requires extending the Hono server, which may need to be done differently
// For now, we'll handle feedback through a separate endpoint setup

// Export for use in other modules
export { voltAgent, bookChatAgent, vectorStore };

