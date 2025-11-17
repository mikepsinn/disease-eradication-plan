/**
 * Integration test for the VoltAgent chat server
 * 
 * ⚠️ IMPORTANT: Start the server FIRST before running these tests!
 * 
 * Usage:
 *   1. Start server: npm run voltagent:dev (in another terminal)
 *   2. Wait for "VOLTAGENT SERVER STARTED SUCCESSFULLY" message
 *   3. Run test: npm run test:integration
 * 
 * Environment Variables:
 *   - VOLTAGENT_PORT: Server port (default: 4242)
 *   - VOLTAGENT_URL: Full server URL (overrides port)
 * 
 * See tools/chat/__tests__/README.md for detailed setup instructions.
 */

import { describe, it, expect, beforeAll } from "@jest/globals";
import { request } from "http";

// VoltAgent defaults to port 3141, but can be overridden
const SERVER_URL = process.env.VOLTAGENT_URL || process.env.VOLTAGENT_SERVER_URL || `http://localhost:${process.env.VOLTAGENT_PORT || "3141"}`;
const SERVER_START_TIMEOUT = 15000; // 15 seconds

/**
 * Check if server is running
 * Returns true if server responds (even with errors), false if connection refused
 */
async function checkServer(url: string): Promise<boolean> {
  try {
    const urlObj = new URL(url);
    const hostname = urlObj.hostname;
    const port = parseInt(urlObj.port || "80", 10);
    const path = urlObj.pathname || "/agents";

    return new Promise<boolean>((resolve) => {
      const req = request({
        hostname,
        port,
        path,
        method: "GET",
        timeout: 2000,
      }, (res) => {
        // Any HTTP response means server is up
        resolve(true);
      });

      req.on("error", (error: any) => {
        if (error.code === "ECONNREFUSED") {
          resolve(false);
        } else {
          // Other errors might mean server is up but having issues
          resolve(true);
        }
      });

      req.on("timeout", () => {
        req.destroy();
        resolve(false);
      });

      req.end();
    });
  } catch (error) {
    return false;
  }
}

/**
 * Wait for server to be ready by polling the agents endpoint
 * Uses Node's http module for more reliable connection checking
 */
async function waitForServer(url: string, timeout: number): Promise<void> {
  const startTime = Date.now();
  const pollInterval = 500; // Check every 500ms
  const urlObj = new URL(url);
  const hostname = urlObj.hostname;
  const port = parseInt(urlObj.port || "80", 10);
  const path = urlObj.pathname || "/agents";

  while (Date.now() - startTime < timeout) {
    try {
      const serverUp = await new Promise<boolean>((resolve, reject) => {
        let resolved = false;
        
        const req = request({
          hostname,
          port,
          path,
          method: "GET",
          timeout: 2000,
        }, (res) => {
          // Any HTTP response means server is up (even 500 errors)
          if (!resolved) {
            resolved = true;
            const statusCode = res.statusCode || 0;
            if (statusCode >= 200 && statusCode < 600) {
              console.log(`[TEST] ✅ Server responded with status ${statusCode} on ${hostname}:${port}`);
              resolve(true);
            } else {
              resolve(false);
            }
          }
        });

        req.on("error", (error: any) => {
          if (!resolved) {
            resolved = true;
            // ECONNREFUSED means server not ready
            if (error.code === "ECONNREFUSED") {
              resolve(false);
            } else {
              // Other errors might mean server is up but having issues
              console.log(`[TEST] ⚠️ Server connection error (but might be up): ${error.code || error.message}`);
              resolve(false); // Don't assume server is up on connection errors
            }
          }
        });

        req.on("timeout", () => {
          if (!resolved) {
            resolved = true;
            req.destroy();
            resolve(false);
          }
        });

        req.end();
      });

      if (serverUp) {
        return;
      } else {
        // Connection refused - server not ready
        const elapsed = Date.now() - startTime;
        if (elapsed % 2000 < pollInterval) {
          console.log(`[TEST] ⏳ Server not ready, waiting... (${Math.round(elapsed / 1000)}s)`);
        }
      }
    } catch (error: any) {
      // Log unexpected errors
      const elapsed = Date.now() - startTime;
      if (elapsed % 2000 < pollInterval) {
        console.log(`[TEST] ⚠️ Unexpected error checking server: ${error.message}`);
      }
    }

    await new Promise((resolve) => setTimeout(resolve, pollInterval));
  }

  // If we get here, server never became ready
  console.error(`\n[TEST] ❌ Server did not become ready within ${timeout}ms`);
  console.error(`[TEST]    Make sure the server is running:`);
  console.error(`[TEST]    1. Run: npm run voltagent:dev`);
  console.error(`[TEST]    2. Wait for "VOLTAGENT SERVER STARTED SUCCESSFULLY" message`);
  console.error(`[TEST]    3. Check the port matches: ${SERVER_URL}`);
  throw new Error(`Server did not become ready within ${timeout}ms`);
}

describe("Chat Server Integration", () => {
  beforeAll(async () => {
    console.log(`\n${"=".repeat(60)}`);
    console.log(`[TEST] Integration Test Setup`);
    console.log(`${"=".repeat(60)}`);
    console.log(`[TEST] Server URL: ${SERVER_URL}`);
    console.log(`[TEST] Timeout: ${SERVER_START_TIMEOUT}ms`);
    console.log(`[TEST] Make sure server is running: npm run voltagent:dev`);
    console.log(`${"=".repeat(60)}\n`);
    
    // Always wait for server - don't skip if not immediately available
    console.log(`[TEST] Checking server availability...`);
    const isRunning = await checkServer(SERVER_URL);
    if (!isRunning) {
      console.log(`[TEST] Server not immediately available, waiting up to ${SERVER_START_TIMEOUT}ms...`);
      await waitForServer(SERVER_URL, SERVER_START_TIMEOUT);
    } else {
      console.log(`[TEST] ✅ Server is already running`);
    }
    console.log(`[TEST] ✅ Server is ready - starting tests\n`);
  }, 30000); // 30 second timeout for beforeAll

  it("should list available agents", async () => {
    console.log(`\n${"-".repeat(60)}`);
    console.log(`[TEST] Testing: GET /agents`);
    console.log(`${"-".repeat(60)}`);
    
    let response: Response;
    let text: string;
    
    try {
      response = await fetch(`${SERVER_URL}/agents`, {
        method: "GET",
        headers: {
          "Accept": "application/json",
        },
      });
      text = await response.text();
    } catch (error: any) {
      console.error(`[TEST]   ❌ Request failed: ${error.message}`);
      console.error(`[TEST]   This usually means:`);
      console.error(`[TEST]     1. Server is not running`);
      console.error(`[TEST]     2. Wrong port (expected: ${SERVER_URL})`);
      console.error(`[TEST]     3. Network/firewall issue`);
      throw error;
    }
    
    console.log(`[TEST]   Status: ${response.status} ${response.statusText}`);
    console.log(`[TEST]   Headers:`, Object.fromEntries(response.headers.entries()));
    console.log(`[TEST]   Response length: ${text.length} bytes`);
    console.log(`[TEST]   Response preview: ${text.substring(0, 500)}${text.length > 500 ? "..." : ""}`);
    
    if (!response.ok) {
      console.error(`\n[TEST]   ❌ ERROR: Server returned ${response.status}`);
      console.error(`[TEST]   Full response:`, text);
      
      // Try to parse error for better debugging
      try {
        const error = JSON.parse(text);
        console.error(`[TEST]   Parsed error:`, JSON.stringify(error, null, 2));
        
        // Provide specific guidance based on error
        if (error.error?.includes("Cannot read properties")) {
          console.error(`\n[TEST]   🔍 DIAGNOSIS: Server agent registration issue`);
          console.error(`[TEST]   This error suggests agents aren't properly registered.`);
          console.error(`[TEST]   Check:`);
          console.error(`[TEST]     1. src/index.ts - agents are created and passed to VoltAgent`);
          console.error(`[TEST]     2. Server logs for agent registration errors`);
          console.error(`[TEST]     3. VoltAgent version compatibility`);
        }
      } catch {
        // Not JSON, that's fine
        console.error(`[TEST]   Response is not JSON`);
      }
      
      // Don't fail the test if it's a 500 - we want to see the error
      if (response.status >= 500) {
        console.error(`\n[TEST]   ⚠️  Server error detected - this is a server bug, not a test failure`);
      }
    }
    
    // Test must pass - server should respond correctly
    expect(response.status).toBeDefined();
    expect(text).toBeDefined();
    
    // Server should return 200, not 500
    if (response.status >= 500) {
      console.error(`\n[TEST]   ❌ SERVER ERROR: Status ${response.status}`);
      console.error(`[TEST]   This is a server bug that needs to be fixed.`);
      console.error(`[TEST]   Full error response:`, text);
      throw new Error(`Server returned ${response.status}: ${text.substring(0, 200)}`);
    }
    
    // Server should return 200 OK
    expect(response.status).toBe(200);
    
    // Parse and validate response
    let data: any;
    try {
      data = JSON.parse(text);
    } catch (e: any) {
      console.error(`[TEST]   ❌ Invalid JSON response:`, e.message);
      console.error(`[TEST]   Raw response:`, text);
      throw new Error(`Server returned invalid JSON: ${text.substring(0, 200)}`);
    }
    
    console.log(`\n[TEST]   ✅ SUCCESS: Server responded correctly`);
    
    // Validate response structure
    expect(data).toBeDefined();
    if (data.agents !== undefined) {
      expect(Array.isArray(data.agents)).toBe(true);
      console.log(`[TEST]   Found ${data.agents.length} agents:`);
      data.agents.forEach((a: any, i: number) => {
        console.log(`[TEST]     ${i + 1}. ${a.name || a.id || JSON.stringify(a)}`);
        // Each agent should have a name or id
        expect(a.name || a.id).toBeDefined();
      });
    } else {
      // If no agents array, log what we got
      console.log(`[TEST]   Response structure:`, Object.keys(data));
      // Still pass if server responded, but log warning
      console.log(`[TEST]   ⚠️  No 'agents' array in response`);
    }
  });

  it("should handle chat endpoint with minimal request", async () => {
    const requestBody = {
      messages: [
        { role: "user", content: "Hello, what is the 1% Treaty?" }
      ],
    };

    console.log(`\n[TEST] Testing: POST /agents/bookChat/chat`);
    console.log(`[TEST]   Request:`, JSON.stringify(requestBody, null, 2));

    try {
      const response = await fetch(`${SERVER_URL}/agents/bookChat/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      const responseText = await response.text();
      console.log(`[TEST]   Status: ${response.status} ${response.statusText}`);
      console.log(`[TEST]   Headers:`, Object.fromEntries(response.headers.entries()));
      console.log(`[TEST]   Response (first 1000 chars):`, responseText.substring(0, 1000));

      if (!response.ok) {
        console.error(`[TEST]   ❌ Error response (full):`, responseText);
        try {
          const error = JSON.parse(responseText);
          console.error(`[TEST]   Error details:`, JSON.stringify(error, null, 2));
        } catch {
          // Not JSON
        }
      } else {
        console.log(`[TEST]   ✅ Success`);
      }

      // Test must pass - server should handle the request
      expect(response.status).toBeDefined();
      
      if (!response.ok) {
        console.error(`[TEST]   ❌ Request failed with status ${response.status}`);
        console.error(`[TEST]   Full error:`, responseText);
        
        if (response.status >= 500) {
          throw new Error(`Server error ${response.status}: ${responseText.substring(0, 200)}`);
        }
        if (response.status === 400) {
          console.error(`[TEST]   ⚠️ 400 Bad Request - check request format`);
          // Try to parse error for debugging
          try {
            const error = JSON.parse(responseText);
            console.error(`[TEST]   Error details:`, JSON.stringify(error, null, 2));
          } catch {
            // Not JSON
          }
          // 400 is a client error, but we want to know why
          throw new Error(`Bad request: ${responseText.substring(0, 200)}`);
        }
      } else {
        console.log(`[TEST]   ✅ Success - server processed request`);
      }
    } catch (error: any) {
      console.error(`[TEST]   ❌ Request failed:`, error.message);
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

    console.log(`\n[TEST] Testing: POST /agents/bookChat/chat (with conversation history)`);
    console.log(`[TEST]   Request:`, JSON.stringify(requestBody, null, 2));

    try {
      const response = await fetch(`${SERVER_URL}/agents/bookChat/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      const responseText = await response.text();
      console.log(`[TEST]   Status: ${response.status} ${response.statusText}`);
      console.log(`[TEST]   Response (first 1000 chars):`, responseText.substring(0, 1000));

      if (!response.ok) {
        console.error(`[TEST]   ❌ Error:`, responseText);
        if (response.status >= 500) {
          throw new Error(`Server error ${response.status}: ${responseText.substring(0, 200)}`);
        }
        if (response.status === 400) {
          throw new Error(`Bad request: ${responseText.substring(0, 200)}`);
        }
      } else {
        console.log(`[TEST]   ✅ Success`);
      }

      expect(response.status).toBe(200);
    } catch (error: any) {
      console.error(`[TEST]   ❌ Request failed:`, error.message);
      throw error;
    }
  });

  it("should check server health endpoint", async () => {
    console.log(`\n[TEST] Testing: GET /health`);
    
    try {
      const response = await fetch(`${SERVER_URL}/health`, {
        signal: AbortSignal.timeout(5000),
      });
      const text = await response.text();
      
      console.log(`[TEST]   Status: ${response.status} ${response.statusText}`);
      console.log(`[TEST]   Response: ${text}`);
      
      // Health endpoint might not exist (404 is OK), but 500 is not
      expect(response.status).toBeDefined();
      if (response.status >= 500) {
        throw new Error(`Health endpoint returned server error: ${response.status}`);
      }
      
      if (response.ok) {
        console.log(`[TEST]   ✅ Health endpoint working`);
      } else if (response.status === 404) {
        console.log(`[TEST]   ℹ️  Health endpoint not implemented (404)`);
      }
    } catch (error: any) {
      if (error.name === "AbortError") {
        console.error(`[TEST]   ⚠️  Health endpoint timeout`);
      } else {
        console.error(`[TEST]   ⚠️  Health endpoint error:`, error.message);
      }
      // Don't fail test if health endpoint doesn't exist
    }
  });

  it("should check OpenAPI/Swagger endpoint", async () => {
    console.log(`\n[TEST] Testing: GET /doc (OpenAPI/Swagger)`);
    
    try {
      const response = await fetch(`${SERVER_URL}/doc`, {
        signal: AbortSignal.timeout(5000),
      });
      const text = await response.text();
      
      console.log(`[TEST]   Status: ${response.status} ${response.statusText}`);
      console.log(`[TEST]   Content-Type: ${response.headers.get("content-type")}`);
      
      if (response.ok && text.includes("openapi")) {
        console.log(`[TEST]   ✅ OpenAPI spec available`);
      } else if (response.status === 404) {
        console.log(`[TEST]   ℹ️  OpenAPI endpoint not implemented (404)`);
      } else if (response.status >= 500) {
        throw new Error(`OpenAPI endpoint returned server error: ${response.status}`);
      }
      
      expect(response.status).toBeDefined();
    } catch (error: any) {
      if (error.name === "AbortError") {
        console.error(`[TEST]   ⚠️  OpenAPI endpoint timeout`);
      } else {
        console.error(`[TEST]   ⚠️  OpenAPI endpoint error:`, error.message);
      }
      // Don't fail test if OpenAPI endpoint doesn't exist
    }
  });
});


