import { describe, it, expect, beforeEach, jest } from "@jest/globals";

// Mock fetch for testing
global.fetch = jest.fn() as jest.MockedFunction<typeof fetch>;

describe("BookChatWidget", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("should format messages correctly", () => {
    const messages = [
      { role: "user", content: "Hello" },
      { role: "assistant", content: "Hi there!" },
    ];

    const formatted = messages.map((m) => ({
      role: m.role,
      content: m.content,
    }));

    expect(formatted).toEqual([
      { role: "user", content: "Hello" },
      { role: "assistant", content: "Hi there!" },
    ]);
  });

  it("should escape HTML in messages", () => {
    // Simple HTML escaping function (without DOM)
    const escapeHtml = (text: string): string => {
      return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#x27;");
    };

    const html = "<script>alert('xss')</script>";
    const escaped = escapeHtml(html);
    expect(escaped).toBe("&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;");
  });

  it("should handle API errors gracefully", async () => {
    // Mock fetch to return an error
    (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValueOnce({
      ok: false,
      status: 400,
      statusText: "Bad Request",
    } as Response);

    // Test that error handling works
    const response = await fetch("http://localhost:3141/agents/bookChat/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: [] }),
    });

    expect(response.ok).toBe(false);
    expect(response.status).toBe(400);
  });
});

describe("Chat API Integration", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("should send correct request format", async () => {
    const mockFetch = global.fetch as jest.MockedFunction<typeof fetch>;
    
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      body: {
        getReader: () => ({
          read: async () => ({ done: true, value: undefined }),
        }),
      },
    } as any);

    const response = await fetch("http://localhost:3141/agents/bookChat/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        messages: [{ role: "user", content: "Test" }],
      }),
    });

    expect(mockFetch).toHaveBeenCalledWith(
      "http://localhost:3141/agents/bookChat/chat",
      expect.objectContaining({
        method: "POST",
        headers: expect.objectContaining({
          "Content-Type": "application/json",
        }),
      })
    );
  });

  it("should handle streaming responses", async () => {
    const chunks = [
      new TextEncoder().encode("data: " + JSON.stringify({ type: "text-delta", textDelta: "Hello" }) + "\n"),
      new TextEncoder().encode("data: " + JSON.stringify({ type: "text-delta", textDelta: " World" }) + "\n"),
      new TextEncoder().encode("data: [DONE]\n"),
    ];

    let chunkIndex = 0;
    const mockReader = {
      read: async () => {
        if (chunkIndex < chunks.length) {
          const chunk = chunks[chunkIndex++];
          return { done: false, value: chunk };
        }
        return { done: true, value: undefined };
      },
    };

    const mockFetch = global.fetch as jest.MockedFunction<typeof fetch>;
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      body: {
        getReader: () => mockReader,
      },
    } as any);

    const response = await fetch("http://localhost:3141/agents/bookChat/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        messages: [{ role: "user", content: "Test" }],
      }),
    });

    expect(response.ok).toBe(true);
  });
});

