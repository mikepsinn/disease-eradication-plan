import { Agent, Memory } from "@voltagent/core";
import { google } from "@ai-sdk/google";
import { LibSQLMemoryAdapter } from "@voltagent/libsql";
import { AiSdkEmbeddingAdapter, InMemoryVectorAdapter } from "@voltagent/core";
import { BookVectorStore } from "../../tools/vector/vector-store";

/**
 * Book Chat Agent
 * Provides conversational interface to the book content using RAG
 */
export function createBookChatAgent(vectorStore: BookVectorStore): Agent {
  const memory = new Memory({
    storage: new LibSQLMemoryAdapter({
      url: "file:.voltagent/book-chat.db",
    }),
    embedding: new AiSdkEmbeddingAdapter(
      google.textEmbeddingModel("models/text-embedding-004")
    ),
    vector: new InMemoryVectorAdapter(),
  });

  return new Agent({
    name: "Book Chat Agent",
    instructions: `You are a helpful assistant for "The Complete Idiot's Guide to Ending War and Disease" book.

Your mission is to help readers understand the book's content about:
- The 1% Treaty to redirect 1% of military spending to cure diseases
- The unnecessary suffering from war (14M deaths/year) and disease (55M deaths/year)
- Systems that are 80X more efficient than current approaches
- Public Choice Theory and incentive engineering

Guidelines:
- Answer questions based on the book's content
- Be accurate and cite specific sections when possible
- If you don't know something, say so rather than making it up
- Be helpful and aligned with the book's mission to save millions of lives
- Use the retrieved context to provide accurate answers`,
    model: google("gemini-2.5-pro"),
    memory,
    retriever: {
      async retrieve(input: string | any[]): Promise<string> {
        try {
          // Search vector store for relevant content
          const query = typeof input === "string" ? input : 
            Array.isArray(input) ? input.map((m: any) => m.content || "").join(" ") : "";
          
          const results = await vectorStore.search(query, 5);
          
          // Format results as context
          if (results.length === 0) {
            return "No relevant content found in the book.";
          }
          
          return results.map((result, index) => {
            return `[Source ${index + 1}: ${result.metadata.title || result.metadata.filePath}]
${result.content.substring(0, 1000)}${result.content.length > 1000 ? "..." : ""}`;
          }).join("\n\n");
        } catch (error) {
          console.error("Error retrieving from vector store:", error);
          return "Error retrieving content. Please try again.";
        }
      },
    },
  });
}

