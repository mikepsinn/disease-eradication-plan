---
title: "Create MCP Server for Issue Tracking"
description: "Develop a dedicated MCP server to provide a structured API for interacting with the file-based issues in the `operations/issues/` directory."
published: true
date: '2025-08-16T00:00:00.000Z'
tags: [mcp, issues, project-management, tools, agent-enablement]
editor: markdown
dateCreated: '2025-08-16T00:00:00.000Z'
---

## 1. Overview

The project's current issue tracking system relies on individual Markdown files in the `operations/issues/` directory. While this is excellent for transparency and version control, it is inefficient for AI agents and humans to get a quick overview, search, or manage tasks programmatically.

This task is to create a dedicated MCP (Model Context Protocol) server that will act as a structured API for this directory.

## 2. Requirements

The MCP server should expose a set of tools to an MCP client, enabling structured interaction with the project's issues.

### Proposed Tools:

1.  **`list_issues()`**
    *   **Action:** Scans the `operations/issues/` directory.
    *   **Returns:** A list of all issues, including their number and title (extracted from the filename).

2.  **`get_issue(issue_number: int)`**
    *   **Action:** Reads the content of a specific issue file.
    *   **Arguments:** The number of the issue (e.g., `47`).
    *   **Returns:** The full Markdown content of the specified issue file.

3.  **`search_issues(query: str)`**
    *   **Action:** Performs a full-text search across all issue files.
    *   **Arguments:** A search query string.
    *   **Returns:** A list of issues that match the query, including their number, title, and a brief snippet of the matching text.

4.  **`create_issue(title: str, body: str)`**
    *   **Action:** Creates a new issue file in the `operations/issues/` directory.
    *   **Arguments:**
        *   `title`: The title of the new issue.
        *   `body`: The full Markdown content for the issue.
    *   **Details:** The tool must automatically determine the next available issue number, create the filename in the correct `{number}-{slugified-title}.md` format, and populate the file with the appropriate frontmatter and body content.

## 3. Implementation Details

*   The server can be written in TypeScript or Python, following the examples in the official MCP documentation.
*   It will need filesystem access to read and write from the `operations/issues/` directory.
*   Error handling should be robust (e.g., handling requests for non-existent issues).

## 4. Acceptance Criteria

*   An MCP server is created and can be run locally.
*   The server successfully exposes the four tools defined above.
*   An agent (or a test client) can connect to the server and successfully call each tool, with the server performing the correct filesystem operations and returning the expected data.
