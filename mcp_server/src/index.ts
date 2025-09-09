import { JSONRPCServer } from "json-rpc-2.0";
import { promises as fs } from 'fs';
import path from 'path';
import readline from 'readline';

const ISSUES_DIR = path.join(__dirname, '../../../operations/issues');

interface Issue {
    number: number;
    title: string;
    filename: string;
}

interface IssueDetail extends Issue {
    content: string;
}

const parseFilename = (filename: string): { number: number; title: string } | null => {
    const match = filename.match(/^(\d+)-(.+)\.md$/);
    if (match) {
        const number = parseInt(match[1], 10);
        const title = match[2].replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        return { number, title };
    }
    return null;
};

const listIssueFiles = async (): Promise<string[]> => {
    try {
        const files = await fs.readdir(ISSUES_DIR);
        return files.filter(file => file.endsWith('.md'));
    } catch (error) {
        return [];
    }
};


const server = new JSONRPCServer();

// --- Tool Definitions ---

server.addMethod("tools/list", () => {
    return {
        tools: [
            {
                name: "list_issues",
                description: "List all DIH issues",
                inputSchema: {}
            },
            {
                name: "get_issue",
                description: "Get a specific issue by number",
                inputSchema: {
                    type: "object",
                    properties: {
                        issue_number: { type: "number", description: "The number of the issue to retrieve." }
                    },
                    required: ["issue_number"]
                }
            },
            {
                name: "search_issues",
                description: "Search issues by a query string",
                inputSchema: {
                    type: "object",
                    properties: {
                        query: { type: "string", description: "The text to search for." }
                    },
                    required: ["query"]
                }
            },
            {
                name: "create_issue",
                description: "Create a new issue",
                inputSchema: {
                    type: "object",
                    properties: {
                        title: { type: "string", description: "The title of the new issue." },
                        body: { type: "string", description: "The Markdown body of the new issue." }
                    },
                    required: ["title", "body"]
                }
            }
        ]
    };
});

server.addMethod("tools/call", async (params: any) => {
    const { name, input } = params;
    switch (name) {
        case "list_issues":
            const files = await listIssueFiles();
            const issues: Issue[] = files
                .map(filename => {
                    const parsed = parseFilename(filename);
                    if (parsed) {
                        return { ...parsed, filename };
                    }
                    return null;
                })
                .filter((issue): issue is Issue => issue !== null)
                .sort((a, b) => a.number - b.number);
            return { output: JSON.stringify(issues) };

        case "get_issue":
            const { issue_number } = input;
            const allFiles = await listIssueFiles();
            const issueFilename = allFiles.find(file => file.startsWith(`${issue_number}-`));

            if (!issueFilename) {
                 throw new Error(`Issue #${issue_number} not found.`);
            }
            const content = await fs.readFile(path.join(ISSUES_DIR, issueFilename), 'utf-8');
            return { output: content };

        case "search_issues":
            const { query } = input;
            const searchFiles = await listIssueFiles();
            const matchingIssues: IssueDetail[] = [];
            for (const filename of searchFiles) {
                const content = await fs.readFile(path.join(ISSUES_DIR, filename), 'utf-8');
                if (content.toLowerCase().includes(query.toLowerCase())) {
                    const parsed = parseFilename(filename);
                    if (parsed) {
                        matchingIssues.push({ ...parsed, filename, content });
                    }
                }
            }
            return { output: JSON.stringify(matchingIssues.sort((a, b) => a.number - b.number)) };
            
        case "create_issue":
            const { title, body } = input;
            const createFiles = await listIssueFiles();
            const numbers = createFiles.map(file => parseInt(file.split('-')[0], 10)).filter(num => !isNaN(num));
            const nextNumber = numbers.length > 0 ? Math.max(...numbers) + 1 : 1;
            
            const slugifiedTitle = title.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]+/g, '');
            const newFilename = `${nextNumber}-${slugifiedTitle}.md`;

            const frontmatter = `---
title: "${title}"
description: "A new issue."
published: true
date: '${new Date().toISOString()}'
tags: [new-issue]
editor: markdown
dateCreated: '${new Date().toISOString()}'
---

`;
            const fullContent = frontmatter + body;
            await fs.writeFile(path.join(ISSUES_DIR, newFilename), fullContent, 'utf-8');
            return { output: `Successfully created issue #${nextNumber}: ${newFilename}` };

        default:
            throw new Error(`Tool ${name} not found.`);
    }
});


// --- Stdio Transport ---

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false,
});

rl.on('line', (line) => {
    const trimmedLine = line.trim();
    if (trimmedLine.length === 0) {
        return;
    }

    let jsonrpcRequest;
    try {
        jsonrpcRequest = JSON.parse(trimmedLine);
    } catch (e) {
        return;
    }

    server.receive(jsonrpcRequest).then((jsonrpcResponse) => {
        if (jsonrpcResponse) {
            const responseStr = JSON.stringify(jsonrpcResponse);
            process.stdout.write(`Content-Length: ${Buffer.byteLength(responseStr, 'utf-8')}\r\n\r\n${responseStr}`);
        }
    });
});
