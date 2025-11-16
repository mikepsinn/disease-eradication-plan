import { Octokit } from "@octokit/rest";

/**
 * Create a GitHub issue from user feedback
 */
export async function createGitHubIssueFromFeedback(
  feedback: {
    message: string;
    userEmail?: string;
    context?: string;
    pageUrl?: string;
  },
  options: {
    owner: string;
    repo: string;
    token: string;
  }
): Promise<{ number: number; url: string } | null> {
  try {
    const octokit = new Octokit({
      auth: options.token,
    });

    const title = `User Feedback: ${feedback.message.substring(0, 100)}${feedback.message.length > 100 ? "..." : ""}`;
    
    const body = `## User Feedback

${feedback.message}

${feedback.context ? `### Context\n\n${feedback.context}\n\n` : ""}
${feedback.pageUrl ? `### Page\n\n${feedback.pageUrl}\n\n` : ""}
${feedback.userEmail ? `### Contact\n\n${feedback.userEmail}\n\n` : ""}

---
*This issue was automatically created from user feedback via the book chat widget.*`;

    const response = await octokit.rest.issues.create({
      owner: options.owner,
      repo: options.repo,
      title,
      body,
      labels: ["user-feedback", "chat-widget"],
    });

    return {
      number: response.data.number,
      url: response.data.html_url,
    };
  } catch (error) {
    console.error("Error creating GitHub issue:", error);
    return null;
  }
}

