#!/usr/bin/env tsx
/**
 * Test script to directly test agent creation and VoltAgent initialization
 * This will show us the actual error without the server layer
 */

import { google } from "@ai-sdk/google";
import { Agent, VoltAgent, Memory } from "@voltagent/core";
import { LibSQLMemoryAdapter } from "@voltagent/libsql";
import { createPinoLogger } from "@voltagent/logger";
import {
  AiSdkEmbeddingAdapter,
  InMemoryVectorAdapter,
} from "@voltagent/core";
import { createBookChatAgent } from "../../src/agents/book-chat-agent";
import { BookVectorStore } from "../vector/vector-store";

// Create logger with debug level
const logger = createPinoLogger({
  name: "test-agents",
  level: "debug",
});

async function testAgents() {
  try {
    console.log("\n=== Testing Agent Creation ===\n");

    // Create Memory
    const memory = new Memory({
      storage: new LibSQLMemoryAdapter(),
      embedding: new AiSdkEmbeddingAdapter(
        google.textEmbeddingModel("models/text-embedding-004")
      ),
      vector: new InMemoryVectorAdapter(),
    });

    // Create vector store
    const vectorStore = new BookVectorStore();
    console.log("✅ Vector store created");

    // Create book chat agent
    const bookChatAgent = createBookChatAgent(vectorStore);
    console.log(`✅ Book Chat Agent created: ${bookChatAgent.name}`);

    // Create DIH agent
    const dihAgent = new Agent({
      name: "DIH Agent",
      instructions: "Test agent",
      model: google("gemini-2.5-pro"),
      memory: memory,
    });
    console.log(`✅ DIH Agent created: ${dihAgent.name}`);

    // Create agents object
    const agents = {
      dihAgent,
      bookChat: bookChatAgent,
    };

    console.log("\n=== Testing VoltAgent Creation ===\n");
    console.log("Agents object keys:", Object.keys(agents));
    console.log("Agents object values:", Object.values(agents).map(a => a?.name || "undefined"));

    // Create VoltAgent WITHOUT server to test agent registration
    const voltAgent = new VoltAgent({
      agents,
      logger,
    });

    console.log("✅ VoltAgent created");

    // Try to simulate what the server does - get agent states
    console.log("\n=== Testing Agent State Access ===\n");
    
    // This is what the server endpoint does internally
    const agentEntries = Object.entries(agents);
    console.log(`Found ${agentEntries.length} agents in agents object`);
    
    for (const [key, agent] of agentEntries) {
      console.log(`\nProcessing agent '${key}':`);
      console.log(`  - Agent exists: ${!!agent}`);
      console.log(`  - Agent type: ${typeof agent}`);
      console.log(`  - Agent name: ${agent?.name || "NO NAME"}`);
      
      if (!agent) {
        console.error(`  ❌ ERROR: Agent '${key}' is undefined!`);
        continue;
      }
      
      if (!agent.name) {
        console.error(`  ❌ ERROR: Agent '${key}' has no name property!`);
        continue;
      }
      
      // Try to get full state (this is what fails in the server)
      try {
        // @ts-ignore - accessing internal method for testing
        console.log(`  - Agent has subAgents: ${!!agent.subAgents}`);
        console.log(`  - Agent has tools: ${!!agent.tools}`);
        console.log(`  - Agent has retriever: ${!!agent.retriever}`);
        
        if (agent.subAgents) {
          console.log(`  - SubAgents count: ${agent.subAgents.length}`);
          agent.subAgents.forEach((sub: any, i: number) => {
            console.log(`    SubAgent ${i}: ${sub?.name || 'NO NAME'} (${sub ? 'defined' : 'undefined'})`);
          });
        }
        
        if (agent.tools) {
          console.log(`  - Tools count: ${agent.tools.length}`);
          agent.tools.forEach((tool: any, i: number) => {
            console.log(`    Tool ${i}: ${tool?.name || 'NO NAME'} (${tool ? 'defined' : 'undefined'})`);
          });
        }
        
        // @ts-ignore - accessing internal method for testing
        const state = agent.getFullState?.();
        console.log(`  ✅ Agent '${key}' state accessible`);
      } catch (error: any) {
        console.error(`  ❌ ERROR getting state for '${key}':`, error.message);
        console.error(`  Stack:`, error.stack);
        
        // Try to identify what's undefined
        console.error(`  Debugging agent structure:`);
        console.error(`    - agent: ${!!agent}`);
        console.error(`    - agent.name: ${agent?.name}`);
        console.error(`    - agent.subAgents: ${agent?.subAgents ? `array of ${agent.subAgents.length}` : 'undefined/null'}`);
        if (agent?.subAgents) {
          agent.subAgents.forEach((sub: any, i: number) => {
            console.error(`      subAgents[${i}]: ${sub ? `defined (name: ${sub.name || 'NO NAME'})` : 'UNDEFINED!'}`);
          });
        }
        console.error(`    - agent.tools: ${agent?.tools ? `array of ${agent.tools.length}` : 'undefined/null'}`);
        if (agent?.tools) {
          agent.tools.forEach((tool: any, i: number) => {
            console.error(`      tools[${i}]: ${tool ? `defined (name: ${tool.name || 'NO NAME'})` : 'UNDEFINED!'}`);
          });
        }
      }
    }

    console.log("\n✅ All tests completed\n");
  } catch (error: any) {
    console.error("\n❌ FATAL ERROR:", error.message);
    console.error("Stack:", error.stack);
    process.exit(1);
  }
}

testAgents();

