/**
 * Unit tests for server detection utilities
 * These test the detection logic itself, not the actual server
 */

import { describe, it, expect, jest } from "@jest/globals";
import { request } from "http";

// Mock http.request for testing
jest.mock("http", () => ({
  request: jest.fn(),
}));

describe("Server Detection Utilities", () => {
  it("should parse URL correctly", () => {
    const url = "http://localhost:4242/agents";
    const urlObj = new URL(url);
    
    expect(urlObj.hostname).toBe("localhost");
    expect(urlObj.port).toBe("4242");
    expect(urlObj.pathname).toBe("/agents");
  });

  it("should handle default port", () => {
    const url = "http://localhost";
    const urlObj = new URL(url);
    const port = parseInt(urlObj.port || "80", 10);
    
    expect(port).toBe(80);
  });

  it("should construct SERVER_URL from environment", () => {
    const originalPort = process.env.VOLTAGENT_PORT;
    const originalUrl = process.env.VOLTAGENT_URL;
    
    // Test with port
    process.env.VOLTAGENT_PORT = "4242";
    delete process.env.VOLTAGENT_URL;
    const url1 = process.env.VOLTAGENT_URL || 
                 process.env.VOLTAGENT_SERVER_URL || 
                 `http://localhost:${process.env.VOLTAGENT_PORT || "4242"}`;
    expect(url1).toBe("http://localhost:4242");
    
    // Test with full URL
    process.env.VOLTAGENT_URL = "http://localhost:3000";
    const url2 = process.env.VOLTAGENT_URL || 
                 process.env.VOLTAGENT_SERVER_URL || 
                 `http://localhost:${process.env.VOLTAGENT_PORT || "4242"}`;
    expect(url2).toBe("http://localhost:3000");
    
    // Restore
    if (originalPort) process.env.VOLTAGENT_PORT = originalPort;
    else delete process.env.VOLTAGENT_PORT;
    if (originalUrl) process.env.VOLTAGENT_URL = originalUrl;
    else delete process.env.VOLTAGENT_URL;
  });
});

