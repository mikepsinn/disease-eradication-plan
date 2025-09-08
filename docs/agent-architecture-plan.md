# Agent Architecture Plan

This document outlines the strategic plan and architecture for the autonomous AI agent responsible for maintaining and refactoring this wiki codebase.

## Core Principles

1.  **TypeScript First:** The entire agent and its tooling will be written in TypeScript for a unified, modern, and type-safe codebase.
2.  **Protocol-Driven:** The agent's capabilities will be exposed via the **Model Context Protocol (MCP)**. This is the cornerstone of our architecture.
3.  **Seamless IDE Integration:** The agent must be deeply integrated with the developer's workflow, specifically within the Cursor IDE.
4.  **Modular and Testable:** The agent's core logic ("brain") should be decoupled from its capabilities ("tools" or "hands").

## Proposed Architecture

The agent will be built around a central MCP server that it both provides and consumes.

```mermaid
graph TD
    subgraph "Local Development Environment"
        subgraph "Agent Process (Node.js/ts-node)"
            A[Agent Core / "Brain"] -- "Uses Tools" --> C(MCP Client);
            C -- "Makes Tool Calls" --> B(MCP Server);
            B -- "Exposes Tools" --> T[(Agent Tools<br>- readFile<br>- writeFile<br>- runCommand<br>- ...)];
        end

        subgraph "Cursor IDE"
            U[User via Cursor Chat] -- "Uses Tools" --> D(MCP Client for Cursor);
            D -- "Connects to" --> B;
        end
    end

    A -- "Sends Prompts" --> E[LLM API<br>(Anthropic/OpenAI)];
    E -- "Returns Tool Calls" --> A;

```

### Components

1.  **Agent Core (The "Brain"):**
    *   **File:** `scripts/agent/executive-function.ts`
    *   **Responsibility:** Manages the main agent loop (perceive, think, act). It constructs prompts, sends them to the LLM, and processes the responses. When the LLM requests a tool call, the Core uses the MCP client to execute it.

2.  **MCP Server (The "Backbone"):**
    *   **File:** `scripts/mcp/wiki-tools-server.ts`
    *   **Responsibility:** Starts a local server that listens for MCP connections. It loads all available tools and exposes them according to the protocol specification. This is the single entry point for all tool-related activity.

3.  **Agent Tools (The "Hands"):**
    *   **Directory:** `scripts/agent/tools/`
    *   **Responsibility:** Each file in this directory will implement a specific capability (e.g., `file-system.ts`, `terminal.ts`). The MCP server will dynamically load these modules.
    *   **Examples:** `readFile`, `writeFile`, `listDirectory`, `runTerminalCommand`, `codebaseSearch`.

4.  **MCP Client (The "Nerves"):**
    *   **File:** `scripts/agent/mcp-client.ts`
    *   **Responsibility:** A lightweight client that connects to the agent's own MCP server. The Agent Core uses this to call tools. Cursor has its own built-in MCP client.

## Development Roadmap

1.  **[Done]** Consolidate all existing scripts from Python to TypeScript.
2.  **[Next]** Implement the initial `wiki-tools-server.ts` to serve a few basic tools (e.g., `readFile`, `listDirectory`).
3.  **[Next]** Configure Cursor to connect to this local MCP server.
4.  Refactor the `executive-function.ts` to connect to and use the MCP server for all its actions.
5.  Incrementally migrate all functionality from the old scripts (`build-digital-twin.ts`, `apply-initiatives.ts`) into modular tools exposed over the MCP server.
6.  Decommission the old monolithic scripts once their functionality is fully provided by agent tools.
