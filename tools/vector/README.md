# Vector Store & RAG

Vector store for book content retrieval-augmented generation (RAG).

## Overview

The vector store enables semantic search over book content, allowing the chat agent to find relevant sections when answering questions.

## Components

- **BookVectorStore** - Main vector store class
- **update-embeddings.ts** - Script to update embeddings for changed files

## Usage

### Update Embeddings

```bash
# Update only changed files
npm run vector:update

# Full refresh (all files)
npm run vector:update:full
```

### Programmatic Usage

```typescript
import { BookVectorStore } from "./vector-store";

const store = new BookVectorStore();

// Add a file
await store.addFile("knowledge/problem/intro.qmd");

// Search for content
const results = await store.search("military spending", 5);

// Get all files
const files = await store.getAllFiles();
```

## How It Works

1. **Document Storage**: Files are parsed and stored with metadata
2. **Embedding Generation**: Content is embedded using Google's embedding model
3. **Semantic Search**: Queries are matched against stored embeddings
4. **Text Fallback**: If embeddings fail, simple text matching is used

## Storage

- **In-Memory Map**: Fast document lookup
- **VoltAgent Memory**: Persistent storage with LibSQL adapter
- **Location**: `.voltagent/book-vector.db`

## Hash Tracking

The system tracks when embeddings were last updated using frontmatter:
- `lastEmbeddingHash` - Hash of content when embeddings were created

## Performance

- **Text Search**: Fast, works without API key
- **Semantic Search**: More accurate, requires API key
- **Hybrid**: Falls back to text search if embeddings fail

## Troubleshooting

**Missing API key**: Vector store will use text search only. Set `GOOGLE_GENERATIVE_AI_API_KEY` for semantic search.

**Slow updates**: Large files take longer. Consider processing in batches.

**Storage errors**: Check `.voltagent/` directory permissions.

## See Also

- [Book Chat Agent](../../src/agents/book-chat-agent.ts) - Uses vector store for RAG
- [WISHONIA Documentation](../agents/README.md) - Agent system

