import { Memory } from "@voltagent/core";
import { LibSQLMemoryAdapter } from "@voltagent/libsql";
import { google } from "@ai-sdk/google";
import { AiSdkEmbeddingAdapter, InMemoryVectorAdapter } from "@voltagent/core";

export interface SearchResult {
  content: string;
  metadata: {
    filePath?: string;
    title?: string;
    [key: string]: any;
  };
  score?: number;
}

/**
 * BookVectorStore - Simple vector store for book content
 * Uses VoltAgent Memory for embeddings and vector search
 */
export class BookVectorStore {
  private memory: Memory;
  private documents: Map<string, { content: string; metadata: any }> = new Map();

  constructor() {
    this.memory = new Memory({
      storage: new LibSQLMemoryAdapter({
        url: "file:.voltagent/book-vectors.db",
      }),
      embedding: new AiSdkEmbeddingAdapter(
        google.textEmbeddingModel("models/text-embedding-004")
      ),
      vector: new InMemoryVectorAdapter(),
    });
  }

  /**
   * Add a file to the vector store
   */
  async addFile(filePath: string, content: string, metadata: any = {}): Promise<void> {
    try {
      // Store document in memory
      this.documents.set(filePath, { content, metadata: { ...metadata, filePath } });

      // Try to add to vector store (requires API key)
      // For now, we'll just store in memory for text-based search
      // TODO: Implement proper vector embedding when API key is available
    } catch (error: any) {
      // Gracefully handle embedding failures (e.g., missing API key)
      console.warn(`Warning: Could not embed document ${filePath}: ${error.message}`);
      // Still store in memory for text-based search
    }
  }

  /**
   * Search for relevant content
   */
  async search(query: string, topK: number = 5): Promise<SearchResult[]> {
    // Simple text-based search fallback
    const results: SearchResult[] = [];
    const queryLower = query.toLowerCase();
    const queryTerms = queryLower.split(/\s+/);

    for (const [filePath, doc] of this.documents.entries()) {
      const contentLower = doc.content.toLowerCase();
      let score = 0;

      // Simple keyword matching
      for (const term of queryTerms) {
        if (contentLower.includes(term)) {
          score += 1;
        }
      }

      if (score > 0) {
        results.push({
          content: doc.content,
          metadata: doc.metadata,
          score: score / queryTerms.length, // Normalize score
        });
      }
    }

    // Sort by score and return top K
    results.sort((a, b) => (b.score || 0) - (a.score || 0));
    return results.slice(0, topK);
  }
}

