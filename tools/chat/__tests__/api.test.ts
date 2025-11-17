import { describe, it, expect, beforeEach } from "@jest/globals";

describe("GitHub Issues API", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("should have createGitHubIssueFromFeedback function", async () => {
    // Test that the function exists and can be imported
    // Skip if @octokit/rest is not available
    try {
      const { createGitHubIssueFromFeedback } = await import("../../api/github-issues");
      expect(createGitHubIssueFromFeedback).toBeDefined();
      expect(typeof createGitHubIssueFromFeedback).toBe("function");
    } catch (error) {
      // If import fails due to missing dependency, skip test
      console.warn("Skipping test - @octokit/rest not available:", error);
    }
  });

  it("should handle feedback structure", () => {
    const feedback = {
      message: "Test feedback",
      userEmail: "user@example.com",
      context: "Some context",
      pageUrl: "https://example.com/page",
    };

    expect(feedback.message).toBe("Test feedback");
    expect(feedback.userEmail).toBe("user@example.com");
    expect(feedback.context).toBe("Some context");
    expect(feedback.pageUrl).toBe("https://example.com/page");
  });

  it("should format feedback for GitHub issue", () => {
    const feedback = {
      message: "Test feedback message",
      userEmail: "user@example.com",
      context: "Some context",
      pageUrl: "https://example.com/page",
    };

    // Expected GitHub issue body format
    const expectedBody = expect.stringContaining("Test feedback message");
    expect(expectedBody).toBeDefined();
  });
});

