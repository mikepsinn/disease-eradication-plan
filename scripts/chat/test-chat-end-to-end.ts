#!/usr/bin/env tsx
/**
 * End-to-end test script for the VoltAgent chat server
 *
 * This script:
 * 1. Starts the server in the background
 * 2. Waits for it to be ready
 * 3. Tests the chat endpoint
 * 4. Shows results
 * 5. Cleans up
 */

import { spawn, execSync } from "child_process";
import { config } from "dotenv";

// Load .env file
config();

const DEFAULT_PORT = process.env.VOLTAGENT_PORT ? parseInt(process.env.VOLTAGENT_PORT, 10) : 3141;
let SERVER_URL = process.env.VOLTAGENT_URL || `http://localhost:${DEFAULT_PORT}`;
const SERVER_START_TIMEOUT = 30000; // 30 seconds
const POLL_INTERVAL = 500; // Check every 500ms

let serverProcess: any = null;
let detectedPort: number | null = null;

/**
 * Helper to convert localhost to IPv4 address (fetch prefers IPv6 which may not work)
 */
function toIPv4Url(url: string): string {
  return url.replace("localhost", "127.0.0.1");
}

/**
 * Wait for server to be ready
 * Note: Uses the global SERVER_URL which may be updated during startup
 */
async function waitForServer(timeout: number): Promise<void> {
  const startTime = Date.now();
  let lastLogTime = 0;
  let lastCheckedUrl = "";

  while (Date.now() - startTime < timeout) {
    try {
      // Use the current SERVER_URL (which may be updated by port detection)
      // Replace 'localhost' with '127.0.0.1' to force IPv4 (fetch prefers IPv6 which may not work)
      const healthCheckUrl = `${SERVER_URL.replace("localhost", "127.0.0.1")}/agents`;

      // Log when we switch URLs (port detected)
      if (healthCheckUrl !== lastCheckedUrl && lastCheckedUrl !== "") {
        console.log(`   Switching to detected URL: ${healthCheckUrl}`);
      }
      lastCheckedUrl = healthCheckUrl;

      // Create AbortController for timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 2000);

      const response = await fetch(healthCheckUrl, {
        method: "GET",
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (response.ok) {
        console.log(`✅ Server responded with status ${response.status}`);
        return;
      }
    } catch (error: any) {
      // Expected errors while waiting for server to start
      // Log detailed error for debugging
      if (Date.now() - startTime < 5000 || (Date.now() - startTime) % 10000 < 1000) {
        console.log(`   Fetch error: ${error.message || error.code || error.name || "Unknown"}`);
        if (error.cause) {
          console.log(`   Cause: ${error.cause.message || error.cause.code || JSON.stringify(error.cause)}`);
        }
      }
      // Continue polling
    }

    // Log progress every 2 seconds
    const elapsed = Date.now() - startTime;
    if (elapsed - lastLogTime >= 2000) {
      console.log(`⏳ Waiting for server... (${Math.round(elapsed / 1000)}s)`);
      lastLogTime = elapsed;
    }

    await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL));
  }

  throw new Error(`Server did not become ready within ${timeout}ms`);
}

/**
 * Start the server
 */
function startServer(): Promise<void> {
  return new Promise((resolve, reject) => {
    console.log("🚀 Starting VoltAgent server...");
    console.log(`   Command: npx tsx --env-file=.env src/index.ts`);
    console.log(`   URL: ${SERVER_URL}\n`);

    // Use tsx directly to start the server
    // On Windows, we need to pass as a string when using shell: true
    const command = process.platform === "win32"
      ? `npx tsx src/index.ts`
      : "npx";
    const args = process.platform === "win32"
      ? []
      : ["tsx", "src/index.ts"];

    serverProcess = spawn(command, args, {
      cwd: process.cwd(),
      stdio: ["ignore", "pipe", "pipe"],
      shell: true,
      env: { ...process.env }, // Pass through all environment variables from loaded .env
    });

    let serverOutput = "";

    serverProcess.stdout?.on("data", (data: Buffer) => {
      const output = data.toString();
      serverOutput += output;
      // Log all output to see what's happening
      process.stdout.write(output);

      // Detect the actual port from server output
      // Prioritize the HTTP Server line which shows the actual listening port
      const httpServerMatch = output.match(/HTTP Server:\s+http:\/\/localhost:(\d+)/i);
      if (httpServerMatch && !detectedPort) {
        const port = parseInt(httpServerMatch[1], 10);
        if (port && port > 0 && port < 65536) {
          detectedPort = port;
          SERVER_URL = `http://localhost:${port}`;
          console.log(`\n🔍 Detected server port: ${port}`);
          console.log(`   Updated SERVER_URL to: ${SERVER_URL}\n`);
        }
      }

      // Fallback: look for other patterns if HTTP Server pattern not found
      if (!detectedPort) {
        const portMatch = output.match(/localhost:(\d+)\/ui|:(\d+)\/ui/i);
        if (portMatch) {
          const port = parseInt(portMatch[1] || portMatch[2] || "", 10);
          if (port && port > 0 && port < 65536) {
            detectedPort = port;
            SERVER_URL = `http://localhost:${port}`;
            console.log(`\n🔍 Detected server port: ${port}`);
            console.log(`   Updated SERVER_URL to: ${SERVER_URL}\n`);
          }
        }
      }
    });

    serverProcess.stderr?.on("data", (data: Buffer) => {
      const output = data.toString();
      // Log all stderr to see what's happening
      process.stderr.write(output);
    });

    serverProcess.on("error", (error: Error) => {
      console.error("❌ Failed to start server:", error.message);
      reject(error);
    });

    // Give server a moment to start - VoltAgent auto-starts when created
    setTimeout(() => {
      resolve();
    }, 1000);
  });
}

/**
 * Test the chat endpoint
 */
async function testChatEndpoint(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("🧪 Testing Chat Endpoint");
  console.log("=".repeat(60) + "\n");

  const testCases = [
    {
      name: "Simple string input",
      body: {
        input: "What is a 1% treaty?",
      },
    },
    {
      name: "With options (userId and conversationId)",
      body: {
        input: "Tell me about the Decentralized Institutes of Health",
        options: {
          userId: "test-user-123",
          conversationId: "test-conv-456",
        },
      },
    },
    {
      name: "Message array format",
      body: {
        input: [
          { role: "user", content: "What problem does a 1% treaty solve?" },
        ],
      },
    },
  ];

  for (const testCase of testCases) {
    console.log(`\n📡 Test: ${testCase.name}`);
    console.log(`   URL: ${SERVER_URL}/agents/Book Chat Agent/chat`);
    console.log(`   Request:`, JSON.stringify(testCase.body, null, 2));

    try {
      // Agent ID needs to be URL-encoded (spaces become %20)
      const agentId = encodeURIComponent("Book Chat Agent");
      const response = await fetch(`${toIPv4Url(SERVER_URL)}/agents/${agentId}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(testCase.body),
      });

      const responseText = await response.text();
      console.log(`   Status: ${response.status} ${response.statusText}`);

      if (!response.ok) {
        console.error(`   ❌ Error: ${responseText.substring(0, 500)}`);
        if (response.status >= 500) {
          throw new Error(`Server error ${response.status}: ${responseText.substring(0, 200)}`);
        }
      } else {
        console.log(`   ✅ Success!`);
        try {
          const data = JSON.parse(responseText);
          // VoltAgent returns streaming responses as newline-delimited JSON
          if (data.output || data.text || data.message || data.response) {
            const preview = (data.output || data.text || data.message || data.response || "").substring(0, 300);
            console.log(`   Response preview: ${preview}${preview.length >= 300 ? "..." : ""}`);
          } else {
            console.log(`   Response structure:`, Object.keys(data));
          }
        } catch {
          // Might be streaming format - show first few lines
          const lines = responseText.split('\n').filter(l => l.trim());
          if (lines.length > 0) {
            console.log(`   Streaming response (${lines.length} chunks), first chunk:`);
            try {
              const firstChunk = JSON.parse(lines[0]);
              console.log(`   `, JSON.stringify(firstChunk).substring(0, 200));
            } catch {
              console.log(`   `, lines[0].substring(0, 200));
            }
          } else {
            console.log(`   Response (first 200 chars): ${responseText.substring(0, 200)}`);
          }
        }
      }
    } catch (error: any) {
      console.error(`   ❌ Request failed: ${error.message}`);
      throw error;
    }
  }
}

/**
 * Test the agents endpoint
 */
async function testAgentsEndpoint(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("🧪 Testing Agents Endpoint");
  console.log("=".repeat(60) + "\n");

  console.log(`📡 GET ${SERVER_URL}/agents`);

  try {
    const response = await fetch(`${toIPv4Url(SERVER_URL)}/agents`, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    });

    const responseText = await response.text();
    console.log(`   Status: ${response.status} ${response.statusText}`);

    if (!response.ok) {
      console.error(`   ❌ Error: ${responseText}`);
      throw new Error(`Agents endpoint returned ${response.status}`);
    }

    const data = JSON.parse(responseText);
    console.log(`   ✅ Success!`);
    if (data.agents) {
      console.log(`   Found ${data.agents.length} agents:`);
      data.agents.forEach((agent: any, i: number) => {
        console.log(`     ${i + 1}. ${agent.name || agent.id || JSON.stringify(agent)}`);
      });
    } else {
      console.log(`   Response:`, Object.keys(data));
    }
  } catch (error: any) {
    console.error(`   ❌ Request failed: ${error.message}`);
    throw error;
  }
}

/**
 * Cleanup: Stop the server
 */
function cleanup(): void {
  if (serverProcess) {
    console.log("\n🧹 Cleaning up: Stopping server...");

    // On Windows, we need to kill the entire process tree
    if (process.platform === "win32" && serverProcess.pid) {
      try {
        execSync(`taskkill /F /T /PID ${serverProcess.pid}`, { stdio: "ignore" });
      } catch (error) {
        // Process might already be dead
      }
    } else {
      serverProcess.kill();
    }

    serverProcess = null;
  }
}

/**
 * Main test function
 */
async function main() {
  try {
    console.log("\n" + "=".repeat(60));
    console.log("🚀 VoltAgent Chat End-to-End Test");
    console.log("=".repeat(60) + "\n");

    // Start server
    await startServer();

    // Wait for server to be ready
    console.log("\n⏳ Waiting for server to be ready...");
    console.log("   (VoltAgent server should auto-start when created)");
    console.log("   Note: PORT may be auto-detected from server output\n");
    try {
      await waitForServer(SERVER_START_TIMEOUT);
      console.log("✅ Server is ready!\n");
    } catch (error: any) {
      console.error("\n❌ Server did not become ready.");
      console.error("   This might mean:");
      console.error("   1. Server is starting but taking longer than expected");
      console.error("   2. There's an error preventing the server from starting");
      console.error("   3. Port 3141 is already in use");
      console.error("\n   Check the server output above for errors.\n");
      throw error;
    }

    // Test agents endpoint
    await testAgentsEndpoint();

    // Test chat endpoint
    await testChatEndpoint();

    console.log("\n" + "=".repeat(60));
    console.log("✅ All tests passed!");
    console.log("=".repeat(60) + "\n");
  } catch (error: any) {
    console.error("\n" + "=".repeat(60));
    console.error("❌ Test failed:", error.message);
    console.error("=".repeat(60) + "\n");
    process.exit(1);
  } finally {
    cleanup();
  }
}

// Handle cleanup on exit
process.on("SIGINT", () => {
  cleanup();
  process.exit(0);
});

process.on("SIGTERM", () => {
  cleanup();
  process.exit(0);
});

// Run tests
main();

