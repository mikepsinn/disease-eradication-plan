import { Agent, Memory, BaseRetriever, type BaseMessage, type RetrieveOptions } from "@voltagent/core";
import { google } from "@ai-sdk/google";
import { LibSQLMemoryAdapter } from "@voltagent/libsql";
import { AiSdkEmbeddingAdapter, InMemoryVectorAdapter } from "@voltagent/core";
import { BookVectorStore } from "../../scripts/vector/vector-store";

/**
 * Book Retriever - extends BaseRetriever for proper VoltAgent integration
 */
class BookRetriever extends BaseRetriever {
  private vectorStore: BookVectorStore;

  constructor(vectorStore: BookVectorStore) {
    super({});
    this.vectorStore = vectorStore;
  }

  async retrieve(input: string | BaseMessage[], options: RetrieveOptions): Promise<string> {
    try {
      // Convert input to searchable string
      let query = "";
      if (typeof input === "string") {
        query = input;
      } else if (Array.isArray(input) && input.length > 0) {
        const lastMessage = input[input.length - 1];
        if (Array.isArray(lastMessage.content)) {
          const textParts = lastMessage.content
            .filter((part: any) => part.type === "text")
            .map((part: any) => part.text);
          query = textParts.join(" ");
        } else {
          query = lastMessage.content as string;
        }
      }

      // Search vector store for relevant content
      const results = await this.vectorStore.search(query, 5);

      // Format results as context
      if (results.length === 0) {
        return "No relevant content found in the book.";
      }

      // Add references to context if available
      if (options.context && results.length > 0) {
        const references = results.map((result, index) => ({
          id: result.metadata.filePath || `doc-${index}`,
          title: result.metadata.title || result.metadata.filePath || "Book Content",
          source: "Book Knowledge Base",
          score: result.score || 0,
        }));
        options.context.set("references", references);
      }

      return results
        .map((result, index) => {
          return `[Source ${index + 1}: ${result.metadata.title || result.metadata.filePath}]
${result.content.substring(0, 1000)}${result.content.length > 1000 ? "..." : ""}`;
        })
        .join("\n\n");
    } catch (error: any) {
      options.logger?.error("Error retrieving from vector store:", error);
      return "Error retrieving content. Please try again.";
    }
  }
}

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

  // Create retriever instance (BaseRetriever subclass)
  const retriever = new BookRetriever(vectorStore);

  return new Agent({
    name: "Book Chat Agent",
    instructions: `You are a helpful assistant for "How to End War and Disease" book.

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
    retriever: retriever,
  });
}

