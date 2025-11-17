# Integration Tests

Integration tests for the VoltAgent chat server endpoints.

## Prerequisites

1. **Start the server first:**
   ```bash
   npm run voltagent:dev
   ```
   
2. **Wait for server to start:**
   Look for this message:
   ```
   ══════════════════════════════════════════════════
     VOLTAGENT SERVER STARTED SUCCESSFULLY
   ══════════════════════════════════════════════════
     ✓ HTTP Server:  http://localhost:4242
   ```

3. **Run the tests:**
   ```bash
   npm run test:integration
   ```

## Environment Variables

The tests use these environment variables (set via `cross-env` in package.json):

- `VOLTAGENT_PORT` - Server port (default: 4242)
- `VOLTAGENT_URL` - Full server URL (optional, overrides port)

## What the Tests Do

1. **Server Detection** - Waits for server to be ready (15s timeout)
2. **List Agents** - Tests `GET /agents` endpoint
3. **Chat Endpoints** - Tests various chat request formats:
   - Minimal request (just messages)
   - With userId and conversationId
   - With conversation history

## Troubleshooting

### Server Not Detected

If you see "Server did not become ready", check:

1. **Is the server running?**
   ```bash
   curl http://localhost:4242/agents
   ```
   Should return JSON (even if it's an error).

2. **Is the port correct?**
   - Check server output for actual port
   - Default is 4242 (VoltAgent's default)
   - Can override with `VOLTAGENT_PORT` env var

3. **Firewall/Network Issues?**
   - Make sure localhost connections are allowed
   - Try `netstat -an | findstr 4242` (Windows) or `lsof -i :4242` (Mac/Linux)

### Server Returns 500 Error

If `/agents` returns a 500 error, check:

1. **Agent Registration** - Make sure agents are properly registered in `src/index.ts`
2. **Server Logs** - Check the server console for error messages
3. **Dependencies** - Make sure all npm packages are installed

### Tests Pass But Show Errors

The tests are designed to show detailed output even when things fail. This helps with debugging:
- ✅ Green checkmarks = Success
- ⚠️ Yellow warnings = Non-critical issues
- ❌ Red X = Errors that need fixing

## Manual Testing

You can also test endpoints manually:

```bash
# List agents
curl http://localhost:4242/agents

# Chat (minimal)
curl -X POST http://localhost:4242/agents/bookChat/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}'

# Or use the test script
npm run test:server
```

