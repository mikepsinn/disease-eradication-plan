#!/usr/bin/env tsx
/**
 * Quick script to check if VoltAgent server is running
 * Usage: tsx tools/chat/check-server.ts
 */

const SERVER_URL = process.env.VOLTAGENT_URL || process.env.VOLTAGENT_SERVER_URL || 
  `http://localhost:${process.env.VOLTAGENT_PORT || "3141"}`;

async function checkServer() {
  console.log(`\n🔍 Checking server at: ${SERVER_URL}\n`);
  
  try {
    const response = await fetch(`${SERVER_URL}/agents`, {
      method: "GET",
      headers: { "Accept": "application/json" },
      signal: AbortSignal.timeout(3000),
    });
    
    const text = await response.text();
    
    console.log(`✅ Server is running!`);
    console.log(`   Status: ${response.status} ${response.statusText}`);
    console.log(`   Response: ${text.substring(0, 200)}${text.length > 200 ? "..." : ""}`);
    
    if (response.ok) {
      try {
        const data = JSON.parse(text);
        if (data.agents) {
          console.log(`   Agents: ${data.agents.length} registered`);
        }
      } catch {
        // Not JSON
      }
    } else {
      console.log(`   ⚠️  Server returned error (but is running)`);
    }
    
    process.exit(0);
  } catch (error: any) {
    if (error.name === "AbortError" || error.message?.includes("timeout")) {
      console.error(`❌ Server did not respond within 3 seconds`);
    } else if (error.code === "ECONNREFUSED" || error.message?.includes("ECONNREFUSED")) {
      console.error(`❌ Server is not running (connection refused)`);
    } else {
      console.error(`❌ Error: ${error.message}`);
    }
    
    console.error(`\n💡 To start the server:`);
    console.error(`   1. Run: npm run voltagent:dev`);
    console.error(`   2. Wait for "VOLTAGENT SERVER STARTED SUCCESSFULLY" message`);
    console.error(`   3. Check the port in the message matches: ${SERVER_URL}\n`);
    
    process.exit(1);
  }
}

checkServer();

