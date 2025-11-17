# Integration Test Setup

## Overview

The integration tests verify that the VoltAgent server is working correctly. **These tests will FAIL if the server is not running** - this is intentional. The tests are designed to:

1. ✅ **Pass** when the server is running correctly
2. ❌ **Fail with clear error messages** when the server is not running or has errors
3. 📊 **Provide comprehensive logging** to diagnose any issues

## Running the Tests

### Prerequisites

1. **Start the server first:**
   ```bash
   npm run voltagent:dev
   ```

2. **Wait for server to be ready:**
   - Look for server startup messages in the console
   - The server should be listening on port 4242 (or the port specified in `VOLTAGENT_PORT`)

3. **Run the tests:**
   ```bash
   npm run test:integration
   ```

### Quick Server Check

Before running tests, you can quickly check if the server is running:

```bash
npm run check:server
```

This will tell you if the server is accessible and what port it's on.

## Test Behavior

### When Server is Running ✅

- Tests will connect to the server
- Verify endpoints return correct responses
- Check that agents are properly registered
- Validate chat endpoints work correctly
- **All tests should PASS**

### When Server is Not Running ❌

- Tests will wait up to 15 seconds for the server to start
- If server doesn't start, tests will **FAIL with clear error messages**:
  ```
  [TEST] ❌ Server did not become ready within 15000ms
  [TEST]    Make sure the server is running:
  [TEST]    1. Run: npm run voltagent:dev
  [TEST]    2. Wait for "VOLTAGENT SERVER STARTED SUCCESSFULLY" message
  [TEST]    3. Check the port matches: http://localhost:4242
  ```

### When Server Has Errors ❌

- Tests will detect server errors (500, 400, etc.)
- **Tests will FAIL with detailed error information:**
  ```
  [TEST] ❌ SERVER ERROR: Status 500
  [TEST]   This is a server bug that needs to be fixed.
  [TEST]   Full error response: {...}
  ```

## Environment Variables

- `VOLTAGENT_PORT`: Server port (default: 4242)
- `VOLTAGENT_URL`: Full server URL (overrides port)

## Test Output

The tests provide detailed logging:
- ✅ Success indicators
- ❌ Error messages with diagnostics
- ⚠️ Warnings for non-critical issues
- 📊 Request/response details for debugging

## Troubleshooting

### "Server did not become ready"

1. Check if server is running: `npm run check:server`
2. Verify the port matches: Check `VOLTAGENT_PORT` environment variable
3. Check server logs for startup errors
4. Ensure no firewall is blocking the port

### "Server returned 500"

1. Check server logs for the actual error
2. Verify agents are properly registered in `src/index.ts`
3. Check that all dependencies are installed
4. Look for TypeScript compilation errors

### "Bad request: 400"

1. Check the request format matches VoltAgent's expected format
2. Verify required fields are present (e.g., `messages` array)
3. Check server logs for validation errors

## Test Files

- `server-integration.test.ts`: Main integration tests
- `server-detection.test.ts`: Unit tests for server detection utilities
- `check-server.ts`: Quick server health check script

## Summary

**The tests are designed to fail when things don't work** - this is the correct behavior. When the server is running correctly, all tests should pass. The comprehensive logging makes it easy to diagnose any issues.

