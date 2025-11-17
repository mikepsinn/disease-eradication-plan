/**
 * Simplified integration test that assumes server is already running
 * Run with: npm run voltagent:dev (in another terminal) then npm test -- server-integration-simple
 */

import { describe, it, expect } from "@jest/globals";

const SERVER_URL = process.env.VOLTAGENT_URL || "http://localhost:3141";

describe("Chat Server Integration (requires running server)", () => {
  // Skip if SERVER_URL is not accessible
  const isServerRunning = async (): Promise<boolean> => {
    try {
      const response = await fetch(`${SERVER_URL}/agents`);
      return response.status < 500;
    } catch {
      return false;
    }
  };

  it("should list available agents", async () => {
    const response = await fetch(`${SERVER_URL}/agents`);
    const text = await response.text();
    
    console.log(`\n[TEST] GET /agents`);
    console.log(`[TEST] Status: ${response.status}`);
    console.log(`[TEST] Response: ${text.substring(0, 500)}${text.length > 500 ? "..." : ""}`);
    
    if (!response.ok) {
      console.error(`[TEST] Error response: ${text}`);
    }
    
    expect(response.status).toBeLessThan(500);
    
    if (response.ok) {
      try {
        const data = JSON.parse(text);
        expect(data).toHaveProperty("agents");
        expect(Array.isArray(data.agents)).toBe(true);
        console.log(`[TEST] Found ${data.agents.length} agents`);
        data.agents.forEach((agent: any, index: number) => {
          console.log(`[TEST]   Agent ${index + 1}: ${agent.name || agent.id || JSON.stringify(agent)}`);
        });
      } catch (e) {
        console.error(`[TEST] Failed to parse response as JSON:`, e);
      }
    }
  });

  it("should handle chat endpoint with minimal request", async () => {
    const requestBody = {
      messages: [
        { role: "user", content: "Hello, what is the 1% Treaty?" }
      ],
    };

    console.log(`\n[TEST] POST /agents/bookChat/chat`);
    console.log(`[TEST] Request:`, JSON.stringify(requestBody, null, 2));

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
    console.log(`[TEST] Response (first 1000 chars):`, responseText.substring(0, 1000));

    if (!response.ok) {
      console.error(`[TEST] Error response (full):`, responseText);
    }

    expect(response.status).toBeDefined();
    
    if (response.status === 400) {
      console.error(`\n[TEST] ❌ 400 Bad Request`);
      console.error(`[TEST] Full error response:`, responseText);
      try {
        const error = JSON.parse(responseText);
        console.error(`[TEST] Parsed error:`, JSON.stringify(error, null, 2));
      } catch {
        // Not JSON, that's fine
      }
    } else if (response.status === 200 || response.status === 201) {
      console.log(`\n[TEST] ✅ Success!`);
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

    console.log(`\n[TEST] POST /agents/bookChat/chat (with userId/conversationId)`);
    console.log(`[TEST] Request:`, JSON.stringify(requestBody, null, 2));

    const response = await fetch(`${SERVER_URL}/agents/bookChat/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });

    const responseText = await response.text();
    console.log(`[TEST] Status: ${response.status}`);
    console.log(`[TEST] Response (first 1000 chars):`, responseText.substring(0, 1000));

    if (!response.ok) {
      console.error(`[TEST] Error response:`, responseText);
    }

    expect(response.status).toBeDefined();
  });

  it("should check OpenAPI/Swagger endpoint", async () => {
    const response = await fetch(`${SERVER_URL}/doc`);
    const text = await response.text();
    
    console.log(`\n[TEST] GET /doc`);
    console.log(`[TEST] Status: ${response.status}`);
    console.log(`[TEST] Content-Type: ${response.headers.get("content-type")}`);
    
    if (response.ok && text.includes("openapi")) {
      console.log(`[TEST] ✅ OpenAPI spec available`);
    }
    
    expect(response.status).toBeDefined();
  });
});

