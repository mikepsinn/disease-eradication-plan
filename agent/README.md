# DIH Executive Director Agent

This directory contains the source code and documentation for the `ExecutiveDirector`, an autonomous AI agent responsible for the continuous maintenance and quality control of the Decentralized Institutes of Health (DIH) repository.

## Overview

The agent's primary role is to act as an autonomous repository maintainer. Instead of performing large, one-time cleanup operations, it functions like a tireless gardener, continuously tending to the repository one file at a time. This ensures the long-term health and consistency of the knowledge base as it grows.

## Core Workflow

The agent operates on an incremental, continuous loop. It seeks out files that have been modified more recently than they have been reviewed, analyzes them for issues, takes action, and then records its review before starting the cycle again.

```mermaid
graph TD
    A[Start] --> B{Find Next File to Review};
    B -->|File Found| C[Analyze Single File];
    B -->|No Files Found| H[Wait / Stand By];
    C --> D{Todos for Agent?};
    D -->|Yes| E[Execute Agent Tasks<br/>(edit, move, delete)];
    D -->|No| F{Todos for Human?};
    E --> F;
    F -->|Yes| G[Create Issue for Human];
    F -->|No| I[Update Review Timestamp];
    G --> I;
    I --> B;
```

## Tool Manifest

The agent is equipped with a suite of custom tools to perform its duties:

-   **`findNextFileToReview()`**: Scans the repository to find the next file where the Git modification date is more recent than its `lastReviewed` frontmatter timestamp.
-   **`analyzeSingleFile(filePath)`**: Performs a deep analysis of a single file based on the standards defined in `CONTRIBUTING.md`. It checks for broken links, missing frontmatter, style violations, etc., and returns a list of recommended actions.
-   **`updateReviewTimestamp(filePath)`**: Edits the YAML frontmatter of a file to add or update the `lastReviewed` timestamp to the current date. This marks the file as "clean" until its next modification.
-   **`readFile(path)`**: Reads the content of a file.
-   **`writeFile(path, content)`**: Writes content to a file.
-   **`listFiles(path)`**: Lists all files in a directory.

## How to Run

-   **Run the agent:**
    ```bash
    npm start
    ```
-   **Run the test suite:**
    ```bash
    npm test
    ```
