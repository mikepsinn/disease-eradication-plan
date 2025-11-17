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

// Create logger
const logger = createPinoLogger({
  name: "decentralized-institutes-of-health",
  level: "info",
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

// Initialize VoltAgent with your agent(s)
const port = parseInt(process.env.VOLTAGENT_PORT || "3141", 10);
const voltAgent = new VoltAgent({
  agents: {
    agent: dihAgent,
    bookChat: bookChatAgent,
  },
  server: honoServer({ port }),
  logger,
});

// Add custom feedback endpoint
// Note: This requires extending the Hono server, which may need to be done differently
// For now, we'll handle feedback through a separate endpoint setup

// Export for use in other modules
export { voltAgent, bookChatAgent, vectorStore };

