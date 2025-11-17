#!/usr/bin/env tsx
/**
 * Manual test to verify the chat agent can answer questions about the book
 */

const SERVER_URL = "http://127.0.0.1:4315"; // Use the last known port
const AGENT_ID = encodeURIComponent("Book Chat Agent");

async function testChat(question: string) {
  console.log(`\n${"=".repeat(60)}`);
  console.log(`Question: ${question}`);
  console.log("=".repeat(60));

  try {
    const response = await fetch(`${SERVER_URL}/agents/${AGENT_ID}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        input: question,
      }),
    });

    if (!response.ok) {
      console.error(`Error: ${response.status} ${response.statusText}`);
      const text = await response.text();
      console.error(text);
      return;
    }

    const text = await response.text();

    // Parse streaming response (newline-delimited JSON)
    const lines = text.split('\n').filter(l => l.trim() && l.startsWith('data: '));

    let fullResponse = "";
    for (const line of lines) {
      try {
        const data = JSON.parse(line.substring(6)); // Remove "data: " prefix
        if (data.type === "text-delta" && data.textDelta) {
          fullResponse += data.textDelta;
        } else if (data.type === "finish" && data.text) {
          fullResponse = data.text; // Final complete text
        }
      } catch (e) {
        // Skip invalid JSON lines
      }
    }

    console.log(`\nResponse:\n${fullResponse}\n`);
  } catch (error: any) {
    console.error(`Request failed: ${error.message}`);
  }
}

async function main() {
  console.log("Testing Book Chat Agent...\n");

  await testChat("What is the 1% Treaty?");
  await testChat("How much does the US spend on military per year?");
  await testChat("What are the Decentralized Institutes of Health?");
}

main().catch(console.error);
