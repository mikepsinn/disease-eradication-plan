import { createGitHubIssueFromFeedback } from "../../tools/api/github-issues";
import { createPinoLogger } from "@voltagent/logger";

const logger = createPinoLogger({
  name: "feedback-api",
  level: "info",
});

/**
 * Handle feedback endpoint
 * This should be added as a custom route to the Hono server
 */
export async function handleFeedback(feedback: {
  message: string;
  userId?: string;
  pageUrl?: string;
  context?: string;
}): Promise<{ success: boolean; issueUrl?: string; error?: string }> {
  try {
    // Check if GitHub integration is configured
    if (
      process.env.GITHUB_TOKEN &&
      process.env.GITHUB_OWNER &&
      process.env.GITHUB_REPO
    ) {
      const issue = await createGitHubIssueFromFeedback(
        {
          message: feedback.message,
          userEmail: feedback.userId,
          context: feedback.context,
          pageUrl: feedback.pageUrl,
        },
        {
          owner: process.env.GITHUB_OWNER,
          repo: process.env.GITHUB_REPO,
          token: process.env.GITHUB_TOKEN,
        }
      );

      if (issue) {
        logger.info("GitHub issue created", { issueUrl: issue.url });
        return { success: true, issueUrl: issue.url };
      }
    }

    // Log feedback if GitHub not configured
    logger.info("User feedback received", {
      message: feedback.message,
      userId: feedback.userId,
      pageUrl: feedback.pageUrl,
    });

    return { success: true, message: "Feedback received" };
  } catch (error) {
    logger.error("Error processing feedback:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Failed to process feedback",
    };
  }
}

