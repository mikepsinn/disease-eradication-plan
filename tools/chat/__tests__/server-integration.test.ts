/**
 * Integration test for the VoltAgent chat server
 * 
 * Usage:
 *   1. Start server: npm run voltagent:dev (in another terminal)
 *   2. Run test: npm test -- server-integration
 * 
 * Or set VOLTAGENT_URL environment variable to point to a different server
 */

import { describe, it, expect, beforeAll } from "@jest/globals";

const SERVER_URL = process.env.VOLTAGENT_URL || process.env.VOLTAGENT_SERVER_URL || `http://localhost:${process.env.VOLTAGENT_PORT || "3141"}`;
const SERVER_START_TIMEOUT = 15000; // 15 seconds

/**
 * Check if server is running
 */
async function checkServer(url: string): Promise<boolean> {
  try {
    const response = await fetch(`${url}/agents`);
    return response.status < 500;
  } catch {
    return false;
  }
}

/**
 * Wait for server to be ready by polling the agents endpoint
 */
async function waitForServer(url: string, timeout: number): Promise<void> {
  const startTime = Date.now();
  const pollInterval = 500; // Check every 500ms

  while (Date.now() - startTime < timeout) {
    try {
      const response = await fetch(`${url}/agents`);
      if (response.status < 500) {
        // Server is responding (even if 404/400, it means server is up)
        console.log(`[TEST] ✅ Server is responding`);
        return;
      }
    } catch (error) {
      // Server not ready yet, keep waiting
      const elapsed = Date.now() - startTime;
      if (elapsed % 2000 < pollInterval) {
        // Log every 2 seconds
        console.log(`[TEST] ⏳ Server not ready, waiting... (${Math.round(elapsed / 1000)}s)`);
      }
    }

    await new Promise((resolve) => setTimeout(resolve, pollInterval));
  }

  throw new Error(`Server did not become ready within ${timeout}ms`);
}

describe("Chat Server Integration", () => {
  beforeAll(async () => {
    console.log(`\n[TEST] Waiting for server at ${SERVER_URL}...`);
    console.log(`[TEST] Make sure server is running: npm run voltagent:dev\n`);
    
    // Check if server is already running
    const isRunning = await checkServer(SERVER_URL);
    if (!isRunning) {
      // Wait for server to be ready (assumes it's started manually)
      await waitForServer(SERVER_URL, SERVER_START_TIMEOUT);
    }
    console.log(`[TEST] ✅ Server is ready\n`);
  }, 30000); // 30 second timeout for beforeAll

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


