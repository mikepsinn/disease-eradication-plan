# Book Chat Widget

An embeddable chat widget that allows website visitors to interact with the book content using AI.

## Features

- **RAG-powered**: Uses vector search to find relevant book content
- **Conversational**: Maintains conversation history
- **Feedback Integration**: Users can report issues that create GitHub issues
- **Responsive**: Works on desktop and mobile

## Installation

### 1. Include the Widget Files

Add to your HTML:

```html
<!-- Widget Container -->
<div id="book-chat-widget" data-api-url="https://your-api-url.com"></div>

<!-- Widget Styles -->
<link rel="stylesheet" href="path/to/widget.css">

<!-- Widget Script -->
<script type="module" src="path/to/widget.ts"></script>
```

### 2. Start the VoltAgent Server

```bash
npm run voltagent:dev
```

Or in production:
```bash
npm run voltagent:build
npm run voltagent:start
```

### 3. Configure Environment Variables

```env
GOOGLE_GENERATIVE_AI_API_KEY=your-key-here
GITHUB_TOKEN=your-github-token  # Optional, for issue creation
GITHUB_OWNER=your-username
GITHUB_REPO=your-repo
```

## API Endpoints

The widget uses these VoltAgent endpoints:

- `POST /agents/bookChat/chat` - Stream chat responses (SSE)
- `POST /api/feedback` - Submit user feedback (creates GitHub issue if configured)

## Customization

### Styling

Modify `widget.css` to match your site's design. Key classes:
- `.book-chat-widget` - Main container
- `.book-chat-panel` - Chat panel
- `.book-chat-message` - Individual messages
- `.book-chat-input` - Input field

### API URL

Set the API URL via the `data-api-url` attribute:
```html
<div id="book-chat-widget" data-api-url="https://api.example.com"></div>
```

## How It Works

1. User types a question
2. Widget sends request to VoltAgent server
3. Book Chat Agent uses RAG to find relevant content
4. Agent generates response based on book content
5. Response streams back to widget
6. User can submit feedback to create GitHub issues

## Vector Store Setup

Before using the chat, populate the vector store:

```bash
# Update embeddings for changed files
npm run vector:update

# Full refresh
npm run vector:update:full
```

## Troubleshooting

**Widget doesn't appear**: Check browser console for errors. Make sure the container div exists.

**No responses**: Verify the VoltAgent server is running and API URL is correct.

**Embedding errors**: Ensure `GOOGLE_GENERATIVE_AI_API_KEY` is set.

## See Also

- [WISHONIA Documentation](../agents/README.md) - Agent system
- [Vector Store Documentation](../vector/README.md) - RAG implementation

