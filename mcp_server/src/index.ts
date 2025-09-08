import express from 'express';
import cors from 'cors';
import { promises as fs } from 'fs';
import path from 'path';

const app = express();
const port = 8000;

app.use(cors());
app.use(express.json());

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
        console.error('Error reading issues directory:', error);
        return [];
    }
};

app.get('/list_issues', async (req, res) => {
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
    res.json(issues);
});

app.get('/get_issue/:issue_number', async (req, res) => {
    const issueNumber = parseInt(req.params.issue_number, 10);
    if (isNaN(issueNumber)) {
        return res.status(400).json({ error: 'Invalid issue number' });
    }

    const files = await listIssueFiles();
    const issueFilename = files.find(file => file.startsWith(`${issueNumber}-`));

    if (!issueFilename) {
        return res.status(404).json({ error: `Issue #${issueNumber} not found.` });
    }

    try {
        const content = await fs.readFile(path.join(ISSUES_DIR, issueFilename), 'utf-8');
        const parsed = parseFilename(issueFilename);
        if (parsed) {
            const issueDetail: IssueDetail = {
                ...parsed,
                filename: issueFilename,
                content,
            };
            res.json(issueDetail);
        } else {
            res.status(500).json({ error: 'Could not parse issue filename.' });
        }
    } catch (error) {
        res.status(500).json({ error: 'Could not read issue file.' });
    }
});

app.get('/search_issues', async (req, res) => {
    const query = req.query.query as string;
    if (!query) {
        return res.status(400).json({ error: 'Query parameter is required.' });
    }

    const files = await listIssueFiles();
    const matchingIssues: IssueDetail[] = [];

    for (const filename of files) {
        try {
            const content = await fs.readFile(path.join(ISSUES_DIR, filename), 'utf-8');
            if (content.toLowerCase().includes(query.toLowerCase())) {
                const parsed = parseFilename(filename);
                if (parsed) {
                    matchingIssues.push({
                        ...parsed,
                        filename,
                        content,
                    });
                }
            }
        } catch (error) {
            // Ignore files that can't be read
        }
    }
    res.json(matchingIssues.sort((a, b) => a.number - b.number));
});

app.post('/create_issue', async (req, res) => {
    const { title, body } = req.body;
    if (!title || !body) {
        return res.status(400).json({ error: 'Title and body are required.' });
    }

    const files = await listIssueFiles();
    const numbers = files.map(file => parseInt(file.split('-')[0], 10)).filter(num => !isNaN(num));
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

    try {
        await fs.writeFile(path.join(ISSUES_DIR, newFilename), fullContent, 'utf-8');
        const newIssue: IssueDetail = {
            number: nextNumber,
            title: title,
            filename: newFilename,
            content: fullContent,
        };
        res.status(201).json(newIssue);
    } catch (error) {
        res.status(500).json({ error: 'Failed to create issue file.' });
    }
});


app.listen(port, () => {
    console.log(`MCP server running at http://localhost:${port}`);
});
