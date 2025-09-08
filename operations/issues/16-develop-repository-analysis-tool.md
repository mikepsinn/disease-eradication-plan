---
number: 16
title: "Develop Agent Capability: Comprehensive Repository Analysis Tool"
state: "open"
assignees: ["agent"]
labels: [agent-capability, tooling, agent-task]
milestone: 2
created_at: '2025-09-09T00:00:00.000Z'
---
**Objective:** Equip the agent with a new core capability to perform a comprehensive analysis of the entire repository and generate a health report.

**Tool Requirements (`analyzeRepository()`):**
1.  **File Discovery:** The tool must identify all `.md` files in the repository.
2.  **Metadata Extraction:** For each file, it must extract:
    -   The `title` and `description` from the YAML frontmatter.
    -   The last modification date from the Git history.
3.  **Content Analysis & Recommendations:**
    -   The tool must read the `CONTRIBUTING.md` file to understand the project's standards for information architecture and content quality.
    -   Based on these standards, the agent must generate a list of "Recommended Todos" for each file (e.g., `DELETE`, `MOVE`, `UPDATE`, `REVIEW`).
4.  **Report Generation:**
    -   The tool's output must be a Markdown table.
    -   The agent must be able to write this table to `operations/repository-health-report.md`.

**Agent Workflow Integration:**
- Upon completion, the agent should be able to use the generated report to create new, specific issues for each "Recommended Todo" in the `operations/issues/` directory.
