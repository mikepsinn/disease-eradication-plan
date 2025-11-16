import { Memory } from "@voltagent/core";
import { LibSQLMemoryAdapter } from "@voltagent/libsql";
import { AiSdkEmbeddingAdapter, InMemoryVectorAdapter } from "@voltagent/core";
import { google } from "@ai-sdk/google";
import { readFileWithMatter } from "../lib/file-utils";
import path from "path";

/**
 * Document stored in vector store
 */
interface Document {
  content: string;
  metadata: {
    filePath: string;
    title: string;
    [key: string]: any;
  };
}

/**
 * Vector store for book content RAG
 * Uses in-memory storage with optional semantic search via VoltAgent Memory
 * 
 * Note: This is a simplified implementation. For production, consider using
 * a dedicated vector database like Pinecone, Weaviate, or Qdrant.
 */
export class BookVectorStore {
  private memory: Memory;
  private embeddingModel: any;
  private documents: Map<string, Document> = new Map();

  constructor() {
    // Use Google's embedding model for consistency
    this.embeddingModel = google.textEmbeddingModel("models/text-embedding-004");
    
    this.memory = new Memory({
      storage: new LibSQLMemoryAdapter({
        url: "file:.voltagent/book-vector.db",
      }),
      embedding: new AiSdkEmbeddingAdapter(this.embeddingModel),
      vector: new InMemoryVectorAdapter(),
    });
  }

  /**
   * Add a file to the vector store
   */
  async addFile(filePath: string): Promise<void> {
    try {
      const { body, frontmatter } = await readFileWithMatter(filePath);
      
      // Create a document with metadata
      const document: Document = {
        content: body,
        metadata: {
          filePath,
          title: frontmatter.title || path.basename(filePath, ".qmd"),
          ...frontmatter,
        },
      };

      // Store document in memory map
      this.documents.set(filePath, document);
      
      // Also store in Memory for semantic search (as a system message)
      // Skip if API key is not available (e.g., in tests)
      try {
        const userId = "book-vector-store";
        const conversationId = `file:${filePath}`;
        
        await this.memory.addMessage(
          {
            role: "system",
            content: `Document: ${filePath}\nTitle: ${document.metadata.title}\n\n${body}`,
          },
          userId,
          conversationId
        );
      } catch (error) {
        // If embedding fails (e.g., missing API key), continue without it
        // Documents are still stored in the in-memory map for text search
        console.warn(`Could not store embeddings for ${filePath}, using text search only:`, error);
      }
    } catch (error) {
      console.error(`Error adding file ${filePath} to vector store:`, error);
      throw error;
    }
  }

  /**
   * Update embeddings for a file
   */
  async updateFile(filePath: string): Promise<void> {
    // Remove old entry and add new one
    await this.removeFile(filePath);
    await this.addFile(filePath);
  }

  /**
   * Remove a file from the vector store
   */
  async removeFile(filePath: string): Promise<void> {
    try {
      this.documents.delete(filePath);
      // Note: Memory messages are kept for semantic search, but documents map is cleared
    } catch (error) {
      console.error(`Error removing file ${filePath} from vector store:`, error);
    }
  }

  /**
   * Search for relevant content
   * Uses simple text matching for now - can be enhanced with proper vector search
   */
  async search(query: string, limit: number = 5): Promise<Array<{
    content: string;
    metadata: any;
    score?: number;
  }>> {
    try {
      const results: Array<{ content: string; metadata: any; score?: number }> = [];
      
      // Simple text matching for now - can be enhanced with proper vector search
      const queryLower = query.toLowerCase();
      const queryWords = queryLower.split(/\s+/).filter(w => w.length > 2);
      
      for (const [filePath, document] of this.documents.entries()) {
        const contentLower = document.content.toLowerCase();
        
        // Calculate relevance score based on word matches
        let score = 0;
        for (const word of queryWords) {
          const matches = (contentLower.match(new RegExp(word, "g")) || []).length;
          score += matches;
        }
        
        if (score > 0) {
          results.push({
            content: document.content,
            metadata: document.metadata,
            score,
          });
        }
      }
      
      // Sort by score and limit
      return results
        .sort((a, b) => (b.score || 0) - (a.score || 0))
        .slice(0, limit);
    } catch (error) {
      console.error("Error searching vector store:", error);
      // Fallback: return empty array
      return [];
    }
  }

  /**
   * Get all stored file paths
   */
  async getAllFiles(): Promise<string[]> {
    return Array.from(this.documents.keys());
  }
}
