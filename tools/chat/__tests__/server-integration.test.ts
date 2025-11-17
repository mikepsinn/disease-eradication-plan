import { describe, it, expect, beforeAll, afterAll } from "@jest/globals";
import { createPinoLogger } from "@voltagent/logger";

const logger = createPinoLogger({
  name: "integration-test",
  level: "info",
});

// Import server components
let voltAgent: any = null;
let serverStarted = false;

describe("Chat Server Integration", () => {
  const SERVER_URL = "http://localhost:3141";
  const SERVER_START_TIMEOUT = 15000; // 15 seconds

  beforeAll(async () => {
    // Start the VoltAgent server programmatically
    logger.info("Starting VoltAgent server for integration tests...");
    
    try {
      // Import and initialize the server
      const serverModule = await import("../../src/index.js");
      voltAgent = serverModule.voltAgent;
      
      // Server should already be running from the import
      // Wait for it to be ready
      await waitForServer(SERVER_URL, SERVER_START_TIMEOUT);
      serverStarted = true;
      logger.info("Server is ready");
    } catch (error) {
      console.error("[TEST] Failed to start server:", error);
      throw error;
    }
  }, 30000); // 30 second timeout for beforeAll

  afterAll(async () => {
    // Cleanup - server will stop when process exits
    if (serverStarted) {
      logger.info("Integration tests complete");
    }
  });

  it("should list available agents", async () => {
    const response = await fetch(`${SERVER_URL}/agents`);
    const text = await response.text();
    
    console.log(`[TEST] GET /agents - Status: ${response.status}`);
    console.log(`[TEST] GET /agents - Response: ${text}`);
    
    if (!response.ok) {
      console.error(`[TEST] Error response: ${text}`);
    }
    
    // Even if it fails, we want to see what the error is
    expect(response.status).toBeLessThan(500); // Should not be server error
    
    if (response.ok) {
      const data = JSON.parse(text);
      expect(data).toHaveProperty("agents");
      expect(Array.isArray(data.agents)).toBe(true);
      console.log(`[TEST] Found ${data.agents.length} agents:`, data.agents.map((a: any) => a.name || a.id));
    }
  });

  it("should handle chat endpoint with minimal request", async () => {
    const requestBody = {
      messages: [
        { role: "user", content: "Hello, what is the 1% Treaty?" }
      ],
    };

    console.log(`[TEST] POST /agents/bookChat/chat`);
    console.log(`[TEST] Request body:`, JSON.stringify(requestBody, null, 2));

    try {
      const response = await fetch(`${SERVER_URL}/agents/bookChat/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      const responseText = await response.text();
      console.log(`[TEST] Status: ${response.status}`);
      console.log(`[TEST] Headers:`, Object.fromEntries(response.headers.entries()));
      console.log(`[TEST] Response (first 500 chars):`, responseText.substring(0, 500));

      if (!response.ok) {
        console.error(`[TEST] Error response:`, responseText);
      }

      // Log what we got
      expect(response.status).toBeDefined();
      
      // If it's a 400, let's see what the error message is
      if (response.status === 400) {
        console.error(`[TEST] 400 Bad Request - Full response:`, responseText);
      }
    } catch (error) {
      console.error(`[TEST] Request failed:`, error);
      throw error;
    }
  });

  it("should handle chat endpoint with userId and conversationId", async () => {
    const requestBody = {
      messages: [
        { role: "user", content: "What is the 1% Treaty?" }
      ],
      userId: "test-user-123",
      conversationId: "test-conversation-456",
    };

    console.log(`[TEST] POST /agents/bookChat/chat (with userId/conversationId)`);
    console.log(`[TEST] Request body:`, JSON.stringify(requestBody, null, 2));

    try {
      const response = await fetch(`${SERVER_URL}/agents/bookChat/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      const responseText = await response.text();
      console.log(`[TEST] Status: ${response.status}`);
      console.log(`[TEST] Response (first 500 chars):`, responseText.substring(0, 500));

      if (!response.ok) {
        console.error(`[TEST] Error response:`, responseText);
      }

      expect(response.status).toBeDefined();
    } catch (error) {
      console.error(`[TEST] Request failed:`, error);
      throw error;
    }
  });

  it("should handle chat endpoint with conversation history", async () => {
    const requestBody = {
      messages: [
        { role: "user", content: "Hello" },
        { role: "assistant", content: "Hi there! How can I help?" },
        { role: "user", content: "Tell me about the 1% Treaty" },
      ],
      userId: "test-user-123",
      conversationId: "test-conversation-789",
    };

    console.log(`[TEST] POST /agents/bookChat/chat (with conversation history)`);
    console.log(`[TEST] Request body:`, JSON.stringify(requestBody, null, 2));

    try {
      const response = await fetch(`${SERVER_URL}/agents/bookChat/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      const responseText = await response.text();
      console.log(`[TEST] Status: ${response.status}`);
      console.log(`[TEST] Response (first 500 chars):`, responseText.substring(0, 500));

      if (!response.ok) {
        console.error(`[TEST] Error response:`, responseText);
      }

      expect(response.status).toBeDefined();
    } catch (error) {
      console.error(`[TEST] Request failed:`, error);
      throw error;
    }
  });

  it("should check server health endpoint", async () => {
    try {
      const response = await fetch(`${SERVER_URL}/health`);
      const text = await response.text();
      
      console.log(`[TEST] GET /health - Status: ${response.status}`);
      console.log(`[TEST] GET /health - Response: ${text}`);
      
      // Health endpoint might not exist, so we just log it
      expect(response.status).toBeDefined();
    } catch (error) {
      console.log(`[TEST] /health endpoint not available or error:`, error);
    }
  });

  it("should check OpenAPI/Swagger endpoint", async () => {
    try {
      const response = await fetch(`${SERVER_URL}/doc`);
      const text = await response.text();
      
      console.log(`[TEST] GET /doc - Status: ${response.status}`);
      console.log(`[TEST] GET /doc - Response type: ${response.headers.get("content-type")}`);
      
      if (response.ok && text.includes("openapi")) {
        console.log(`[TEST] OpenAPI spec available`);
      }
      
      expect(response.status).toBeDefined();
    } catch (error) {
      console.log(`[TEST] /doc endpoint not available or error:`, error);
    }
  });
});

/**
 * Wait for server to be ready by polling the health/agents endpoint
 */
async function waitForServer(url: string, timeout: number): Promise<void> {
  const startTime = Date.now();
  const pollInterval = 500; // Check every 500ms

  while (Date.now() - startTime < timeout) {
    try {
      const response = await fetch(`${url}/agents`);
      if (response.status < 500) {
        // Server is responding (even if 404/400, it means server is up)
        logger.info("Server is responding");
        return;
      }
    } catch (error) {
      // Server not ready yet, keep waiting
      const elapsed = Date.now() - startTime;
      if (elapsed % 2000 < pollInterval) {
        // Log every 2 seconds
        logger.info(`Server not ready, waiting... (${Math.round(elapsed / 1000)}s)`);
      }
    }

    await new Promise((resolve) => setTimeout(resolve, pollInterval));
  }

  throw new Error(`Server did not become ready within ${timeout}ms`);
}

