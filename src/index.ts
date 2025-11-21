import "dotenv/config";
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
import { BookVectorStore } from "../scripts/vector/vector-store";
import { ensurePortAvailable } from "../scripts/lib/port-checker";

// Create logger
const logger = createPinoLogger({
  name: "decentralized-institutes-of-health",
  level: process.env.LOG_LEVEL as any,  // fix type error, allow string or undefined
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
This project documents "How to End War and Disease" - a book about getting every nation to sign the 1% Treaty to redirect 1% of military spending to cure diseases instead of cause them.

Your mission is to help save millions of lives by making curing people more profitable than killing them. The project focuses on:
- The unnecessary suffering and death from war (14M deaths/year) and disease (55M deaths/year)
- Redirecting just 1% of military spending to medical research through systems that are 80X more efficient than current approaches

Be helpful, accurate, and aligned with the project's mission and principles.`,
  model: google("gemini-2.5-pro"),
  memory: memory,
});

// Get port from environment or use default
const port = process.env.VOLTAGENT_PORT
  ? parseInt(process.env.VOLTAGENT_PORT, 10)
  : 3141;

// Check if port is available before starting
// This prevents multiple VoltAgent instances and port conflicts
await ensurePortAvailable(port);

// Initialize VoltAgent with your agent(s)
const voltAgent = new VoltAgent({
  agents: {
    dihAgent,
    bookChat: bookChatAgent,
  },
  server: honoServer({ port }),
  logger,
});

// Log server startup info
logger.info(`VoltAgent server configured on port ${port}`);
logger.info(`Agents registered: dihAgent, bookChat`);
logger.info(`Agent details:`, {
  dihAgent: { name: dihAgent.name, model: "gemini-2.5-pro" },
  bookChat: { name: bookChatAgent.name, model: "gemini-2.5-pro" },
});

// Export for use in other modules
export { voltAgent, bookChatAgent, vectorStore };

