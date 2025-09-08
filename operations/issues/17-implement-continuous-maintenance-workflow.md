---
number: 17
title: "Implement Continuous, Context-Aware Maintenance Workflow"
state: "open"
assignees: ["agent"]
labels: [agent-capability, architecture, agent-task]
milestone: 2
created_at: '2025-09-09T00:00:00.000Z'
---
**Objective:** Refactor the agent to follow a continuous, incremental maintenance workflow that is context-aware, as defined in the `agent/README.md`.

**Key Development Tasks:**
1.  **Create Repository Indexer:**
    -   Develop a new tool, `generateRepositoryIndex()`, that scans all `.md` files and produces a structured JSON index of their metadata (path, title, description, tags).
    -   Implement caching for the index to improve performance on subsequent runs.
2.  **Upgrade the File Analyzer:**
    -   Refactor `analyzeSingleFile(filePath)` to accept the `repositoryIndex` as a second argument.
    -   Enhance its logic to use the index to perform sophisticated checks for redundancy, broken links, and correct file location.
3.  **Upgrade the File Finder:**
    -   Refactor `findNextFileToReview()` to use the repository index to more efficiently find the next file to review.
4.  **Update Agent's Core Logic:**
    -   Rewrite the `ExecutiveDirector`'s instructions in `agent/src/index.ts` to implement the new "index-then-analyze" workflow loop.
    -   Integrate the new and updated tools into the agent's toolset.
