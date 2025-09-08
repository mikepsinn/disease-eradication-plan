# DIH Executive Director Agent

This directory contains the source code and documentation for the `ExecutiveDirector`, an autonomous AI agent responsible for the continuous maintenance and quality control of the Decentralized Institutes of Health (DIH) repository.

## Overview

The agent's primary role is to act as an autonomous repository maintainer. It uses a hybrid approach that combines a global understanding of the repository with a continuous, incremental workflow. This allows it to make intelligent, context-aware decisions while working on one file at a time, ensuring the long-term health and consistency of the knowledge base.

## Core Workflow

The agent first builds a comprehensive index of the entire repository to use as its "map." Then, it enters a continuous loop where it finds files that need attention, analyzes them using the full repository context, takes action, and records its review before starting the cycle again.

```mermaid
graph TD
    A[Start] --> B{Generate/Load<br/>Repository Index};
    B --> C{Find Next File to Review};
    C -->|File Found| D[Analyze Single File<br/>(using Index)];
    C -->|No Files Found| I[Wait / Stand By];
    D --> E{Todos for Agent?};
    E -->|Yes| F[Execute Agent Tasks<br/>(edit, move, delete)];
    E -->|No| G{Todos for Human?};
    F --> G;
    G -->|Yes| H[Create Issue for Human];
    G -->|No| J[Update Review Timestamp];
    H --> J;
    J --> C;
```

## Tool Manifest

The agent is equipped with a suite of custom tools to perform its duties:

-   **`generateRepositoryIndex()`**: Scans every markdown file in the repository to build a comprehensive JSON index. For each file, it gathers the title, description, tags, last Git modification date, and the `lastReviewed` date from the frontmatter. This index serves as the agent's complete context map.
-   **`findNextFileToReview(repositoryIndex)`**: A very fast and simple tool that iterates through the pre-built repository index to find the next file where `lastModified > lastReviewed`.
-   **`analyzeSingleFile(filePath, repositoryIndex)`**: Performs a deep, context-aware analysis of a single file. By leveraging the full repository index, it can accurately detect redundancies, validate all internal links, and verify the file's location within the information architecture.
-   **`updateReviewTimestamp(filePath)`**: Edits the YAML frontmatter of a file to add or update the `lastReviewed` timestamp to the current date.
-   **Filesystem Tools (`readFile`, `writeFile`, `listFiles`)**: Basic tools for interacting with the file system.

## How to Run

-   **Run the agent:**
    ```bash
    npm start
    ```
-   **Run the test suite:**
    ```bash
    npm test
    ```
