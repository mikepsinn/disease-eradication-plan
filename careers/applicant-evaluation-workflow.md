---
title: n8n Workflow for Evaluating Supreme Allied Commander Applicants
description: A detailed outline of the n8n workflow for parsing, evaluating, and ranking applications for the Supreme Allied Commander, War on Disease.
published: true
date: 2025-01-01T00:00:00.000Z
tags: hiring, workflow, n8n, automation, ai, recruitment, leadership
editor: markdown
dateCreated: 2024-07-31T00:00:00.000Z
---

# n8n Workflow: Evaluating Supreme Allied Commander Applicants

This document outlines the design for an n8n workflow to automate the evaluation of candidates applying for the **Supreme Allied Commander, War on Disease** role. The goal is to create an efficient, objective screening process that surfaces candidates with both world-class AI/automation skills and the full-stack engineering prowess to build the required systems.

## Workflow Diagram

```mermaid
graph TD;
    A[Trigger: New Application Webhook] --> B{Validate & Parse Form};
    B --> C{Initial Triage};
    C --> D{Disqualify?};
    D -- Yes --> E[End];
    D -- No --> F[Parallel AI Evaluation];
    F --> G[GitHub Profile Analysis];
    F --> H[AI & Agent Skill Analysis];
    F --> I[Web & API Skill Analysis];
    F --> J[Data & Blockchain Skill Analysis];
    F --> K[Strategic Philosophy Analysis];
    
    subgraph "Evidence Verification"
        H
        I
        J
        K
    end

    G & H & I & J & K --> N{Aggregate Scores};
    N --> O{Calculate Weighted Final Score};
    O --> P[Save to Database/Sheet];
    P --> Q[Generate Summary for Top Candidates];
    Q --> R[Notify Hiring Command];
    R --> S[End];

    style F fill:#f9f,stroke:#333,stroke-width:2px
```

## Workflow Stages Explained

### 1. Trigger: New Application Webhook
- **Tool:** n8n Webhook Node.
- **Action:** Receives POST request with application data.

### 2. Validate & Parse Form Data
- **Tool:** n8n Code Node.
- **Action:**
    - Parses JSON data.
    - Validates all required fields and URLs. Invalid submissions are flagged and discarded.

### 3. Initial Triage (Knockout Criteria)
- **Tool:** n8n If Node.
- **Action:** If the GitHub URL is invalid, the candidate is disqualified.

### 4. Parallel AI Evaluation
The core of the workflow, using an LLM to run multiple specialized evaluations.

- **A. GitHub Profile Analysis:**
    - **Input:** GitHub profile URL.
    - **Prompt:** "Analyze this GitHub profile. Score from 0-10 on demonstrated mastery of complex systems. Look for: 1) Originality and depth in repositories. 2) High-quality contributions to relevant open-source projects. 3) Code quality, architectural thinking, and diversity of technologies used. Return JSON with `githubScore` and justification."

- **B. AI & Agent Skill Analysis:**
    - **Input:** Evidence link for "AI Workflows / Agent Development".
    - **Prompt:** "Analyze the candidate's project. Score their `aiSkill` from 0-10, focusing on architectural complexity, novelty, and relevance to building autonomous agent systems. Return JSON with the score and justification."

- **C. Web & API Skill Analysis:**
    - **Input:** Evidence links for "Web App Development" and "API Design & Development".
    - **Prompt:** "Analyze the candidate's two projects. Provide a single `webApiSkill` score from 0-10, representing their ability to build robust, modern, full-stack applications. Look for best practices in UI (React), API design, and overall architecture. Return JSON with the score and a one-sentence summary."

- **D. Data & Blockchain Skill Analysis:**
    - **Input:** Evidence links for "Data Engineering & Analysis" and "Blockchain / Smart Contract Development".
    - **Prompt:** "Analyze the candidate's two projects. Provide a single `dataBlockchainSkill` score from 0-10, representing their ability to work with data pipelines and decentralized technologies. Return JSON with the score and a one-sentence summary."

- **E. Strategic Philosophy Analysis:**
    - **Input:** Text responses for the "AI philosophy" and "technical strategy" questions.
    - **Prompt:** "Analyze the candidate's strategic responses. Score `strategyScore` from 0-10 based on the creativity, feasibility, and detail of their proposed technical plan for the 3.5% mission. Return JSON with the score and justification."

### 5. Aggregate & Calculate Final Score
- **Tool:** n8n Set Node or Code Node.
- **Action:**
    - Gathers all scores.
    - Calculates a final weighted score, balanced across key areas.
    - **Weighting:**
        - **AI & Agent Skill (30%):** `aiSkill * 3`
        - **Web & API Skill (30%):** `webApiSkill * 3`
        - **Data & Blockchain Skill (20%):** `dataBlockchainSkill * 2`
        - **GitHub Score (10%):** `githubScore * 1`
        - **Strategic Philosophy (10%):** `strategyScore * 1`
    - **Final Score = Weighted Sum (out of 100).**

### 6. Output & Human Review
- **Tool:** Google Sheets/Airtable/Postgres Node, Email/Slack Node.
- **Action:**
    - Saves all data and scores to a central database.
    - For candidates scoring above a threshold (e.g., > 75), a summary is generated for review.
    - Sends a notification to the "Hiring Command" with a link to the ranked list of candidates for human review.
    - **Guideline:** The Hiring Command should manually review any candidate who scores a 9 or 10 in the `aiSkill` or `webApiSkill` categories, regardless of their final weighted score. A genius in a key area may be more valuable than a candidate who is simply good in all areas. 