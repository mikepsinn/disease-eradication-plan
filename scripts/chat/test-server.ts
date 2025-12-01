#!/usr/bin/env tsx
/**
 * Simple script to test the VoltAgent server endpoints
 * Usage: tsx tools/chat/test-server.ts
 */

const SERVER_URL = process.env.VOLTAGENT_URL || process.env.VOLTAGENT_SERVER_URL || 
  `http://localhost:${process.env.VOLTAGENT_PORT || "3141"}`;

console.log(`\n🔍 Testing VoltAgent server at: ${SERVER_URL}\n`);

async function testEndpoint(name: string, url: string, options?: RequestInit) {
  console.log(`\n📡 Testing: ${name}`);
  console.log(`   URL: ${url}`);
  if (options?.body) {
    console.log(`   Body: ${options.body}`);
  }
  
  try {
    const response = await fetch(url, options);
    const text = await response.text();
    
    console.log(`   Status: ${response.status} ${response.statusText}`);
    console.log(`   Headers:`, Object.fromEntries(response.headers.entries()));
    
    let parsed: any;
    try {
      parsed = JSON.parse(text);
      console.log(`   Response:`, JSON.stringify(parsed, null, 2));
    } catch {
      console.log(`   Response (raw):`, text.substring(0, 500));
    }
    
    if (!response.ok) {
      console.error(`   ❌ Error: ${text}`);
    } else {
      console.log(`   ✅ Success`);
    }
    
    return { response, text, parsed };
  } catch (error: any) {
    console.error(`   ❌ Request failed:`, error.message);
    return null;
  }
}

async function main() {
  // Test 1: List agents
  await testEndpoint("List Agents", `${SERVER_URL}/agents`);

  // Test 2: Chat with minimal request
  await testEndpoint(
    "Chat (minimal)",
    `${SERVER_URL}/agents/bookChat/chat`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        messages: [{ role: "user", content: "What is a 1% treaty?" }],
      }),
    }
  );

  // Test 3: Chat with userId and conversationId
  await testEndpoint(
    "Chat (with userId/conversationId)",
    `${SERVER_URL}/agents/bookChat/chat`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        messages: [{ role: "user", content: "Hello" }],
        userId: "test-user-123",
        conversationId: "test-conv-456",
      }),
    }
  );

  console.log(`\n✅ Testing complete\n`);
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});

