# Wiki Refactoring Plan

## 1. Objective

To restructure the project's wiki into a comprehensive, logical, and narrative-driven knowledge base. The goal is to improve discoverability, clarify the project's vision, and provide a contributor-friendly structure that aligns with the mission outlined in `README.md`.

## 2. Final Information Architecture

The final structure is designed to present the core narrative of the project at the root of the repository, with detailed supporting documents organized into thematic subdirectories.

```
/
├── introduction.md
├── problem.md
├── solution.md
├── strategy.md
├── economics.md
├── governance.md
|
├── problem/
│   ├── cost-of-war.md
│   ├── cost-of-disease.md
│   └── opportunity-cost.md
├── solution/
│   ├── 1-percent-treaty/
│   │   ├── 1-percent-treaty.md
│   │   └── national-security-argument.md
│   ├── decentralized-institutes-of-health/
│   │   ├── dih-overview.md
│   │   ├── treasury-architecture.md
│   │   └── institute-on-aging.md
│   └── dfda-protocol/
│       ├── dfda-protocol-overview.md
│       ├── implementation-plan.md
│       └── right-to-trial-act.md
├── strategy/
│   ├── fundraising/
│   │   ├── fundraising-overview.md
│   │   └── budget-plan.md
│   ├── legal-and-compliance/
│   │   ├── legal-compliance-overview.md
│   │   └── multi-entity-strategy.md
│   └── political/
│       ├── political-overview.md
│       └── co-opting-the-mic.md
├── economics/
│   ├── victory-bonds-tokenomics.md
│   ├── peace-dividend-value-capture.md
│   └── referral-rewards-system.md
├── governance/
│   ├── organizational-structure.md
│   └── verification-and-fraud-prevention.md
├── reference/
│   └── reference-index.md
├── community/
│   └── community-overview.md
├── operations/
│   ├── operations-overview.md
│   ├── hiring/
│   └── playbooks/
├── scripts/
├── assets/
├── FAQ.md
└── roadmap.md
```

## 3. Step-by-Step Execution Plan

This is a multi-step process that uses a series of purpose-built scripts to automate the refactoring.

---

### Step 1: Generate Content Inventory

First, create an inventory of all existing markdown files to aid in decision-making.

**A. Create `scripts/generate-inventory.ts`:**
This script scans the repository and creates `operations/refactoring_inventory.md` with a table of all markdown files, their titles, and descriptions.

```typescript
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';

const workspaceRoot = process.cwd();
const outputFilePath = path.join(workspaceRoot, 'operations', 'refactoring_inventory.md');
const ignoreDirs = ['node_modules', '.git', '.vscode', '.idea', 'mcp_server'];

async function getAllMarkdownFiles(dir: string): Promise<string[]> {
  let files = await fs.readdir(dir, { withFileTypes: true });
  let markdownFiles: string[] = [];
  for (const file of files) {
    const fullPath = path.join(dir, file.name);
    if (file.isDirectory()) {
      if (!ignoreDirs.includes(file.name)) {
        markdownFiles = markdownFiles.concat(await getAllMarkdownFiles(fullPath));
      }
    } else if (file.name.endsWith('.md')) {
      markdownFiles.push(fullPath);
    }
  }
  return markdownFiles;
}

interface FileInventory {
  path: string;
  title: string;
  description: string;
}

async function generateInventory() {
  console.log(`Starting inventory generation within: ${workspaceRoot}`);
  const allFiles = await getAllMarkdownFiles(workspaceRoot);
  const inventory: FileInventory[] = [];

  for (const filePath of allFiles) {
    try {
      const fileContent = await fs.readFile(filePath, 'utf8');
      if (!fileContent.trim()) {
        console.log(`Skipping empty file: ${filePath}`);
        continue;
      }
      const { data } = matter(fileContent);

      const relativePath = path.relative(workspaceRoot, filePath).replace(/\\/g, '/');
      const description = data.description ? String(data.description) : 'No Description';

      inventory.push({
        path: relativePath,
        title: data.title || 'No Title',
        description: description,
      });
    } catch (error: any) {
      console.error(`Error processing file ${filePath}: ${error.message}`);
    }
  }

  inventory.sort((a, b) => a.path.localeCompare(b.path));

  let markdownContent = '# Wiki Content Inventory\n\n';
  markdownContent += '| File Path | Title | Description |\n';
  markdownContent += '|---|---|---|\n';

  inventory.forEach(item => {
    const descriptionText = item.description || '';
    markdownContent += `| ${item.path} | ${item.title} | ${descriptionText.replace(/\r?\n|\r/g, ' ')} |\n`;
  });

  await fs.writeFile(outputFilePath, markdownContent);
  console.log(`Inventory successfully generated at: ${outputFilePath}`);
}

generateInventory().catch(console.error);
```

**B. Run the script:**
```bash
npx tsx scripts/generate-inventory.ts
```

---

### Step 2: Create the Refactor Manifest

Create `operations/refactor-manifest.json`. This file is the single source of truth for the refactor. Every file must be accounted for with a `move`, `delete`, `keep`, or `create` action. The `reason` property is critical for transparency.

**Example `refactor-manifest.json` structure:**
```json
{
  "files": [
    {
      "old_path": "architecture/blueprint.md",
      "new_path": "introduction.md",
      "action": "move",
      "reason": "This document is the high-level introduction to the project and now serves as the root entry point for the 'Introduction' concept."
    },
    {
      "new_path": "strategy/fundraising.md",
      "action": "create",
      "reason": "Stub file for the fundraising overview, a missing document in our ideal structure."
    },
    {
      "action": "delete",
      "old_path": "operations/wiki-restructuring-plan.md",
      "reason": "This plan is now obsolete and superseded by the manifest itself."
    }
  ]
}
```

---

### Step 3: Execute the Refactor

**A. Create `scripts/execute-refactor.ts`:**
This script reads the manifest and performs the file operations.

```typescript
import fs from 'fs/promises';
import path from 'path';

const workspaceRoot = process.cwd();
const manifestPath = path.join(workspaceRoot, 'operations', 'refactor-manifest.json');
const dryRun = process.argv.includes('--dry-run');

interface FileAction {
  old_path?: string;
  new_path?: string;
  action: 'move' | 'delete' | 'keep' | 'create';
  reason: string;
}

async function executeRefactor() {
  console.log(dryRun ? 'Starting refactor in DRY RUN mode...' : 'Starting refactor...');

  const manifestContent = await fs.readFile(manifestPath, 'utf8');
  const manifest: { files: FileAction[] } = JSON.parse(manifestContent);

  for (const fileAction of manifest.files) {
    const oldPath = fileAction.old_path ? path.join(workspaceRoot, fileAction.old_path) : undefined;

    try {
      if (fileAction.action === 'move') {
        if (!fileAction.new_path || !oldPath) continue;
        const newPath = path.join(workspaceRoot, fileAction.new_path);
        console.log(`MOVE: ${fileAction.old_path} -> ${fileAction.new_path}`);
        if (!dryRun) {
          await fs.mkdir(path.dirname(newPath), { recursive: true });
          await fs.rename(oldPath, newPath);
        }
      } else if (fileAction.action === 'delete') {
        if (!oldPath) continue;
        console.log(`DELETE: ${fileAction.old_path}`);
        if (!dryRun) {
          await fs.rm(oldPath, { force: true });
        }
      } else if (fileAction.action === 'create') {
        if (!fileAction.new_path) continue;
        const newPath = path.join(workspaceRoot, fileAction.new_path);
        console.log(`CREATE: ${fileAction.new_path}`);
        if (!dryRun) {
            await fs.mkdir(path.dirname(newPath), { recursive: true });
            await fs.writeFile(newPath, `# TODO: Content for ${path.basename(fileAction.new_path)}\n\n${fileAction.reason}`);
        }
      } else if (fileAction.action === 'keep') {
        console.log(`KEEP: ${fileAction.old_path}`);
      }
    } catch (error: any) {
        if (error.code !== 'ENOENT') {
            console.error(`ERROR processing ${fileAction.old_path}: ${error.message}`);
        }
    }
  }

  console.log('Refactor complete.');
  if (dryRun) {
    console.log('NOTE: This was a dry run. No files were actually moved, deleted or created.');
  }
}

executeRefactor().catch(console.error);
```

**B. Run the script:**
First, always perform a dry run to verify the changes.
```bash
npx tsx scripts/execute-refactor.ts --dry-run
```
Once satisfied, run it for real.
```bash
npx tsx scripts/execute-refactor.ts
```

---

### Step 4: Fix Internal Links

**A. Create `scripts/fix-internal-links.ts`:**
This script reads the manifest and repairs all broken markdown links.

```typescript
import fs from 'fs/promises';
import path from 'path';

const workspaceRoot = process.cwd();
const manifestPath = path.join(workspaceRoot, 'operations', 'refactor-manifest.json');
const dryRun = process.argv.includes('--dry-run');

interface FileAction {
  old_path?: string;
  new_path?: string;
  action: 'move' | 'delete' | 'keep' | 'create';
  reason: string;
}

async function getAllMarkdownFiles(dir: string): Promise<string[]> {
    let files = await fs.readdir(dir, { withFileTypes: true });
    let markdownFiles: string[] = [];
    const ignoreDirs = ['node_modules', '.git', 'mcp_server'];
    for (const file of files) {
      const fullPath = path.join(dir, file.name);
      if (file.isDirectory()) {
        if (!ignoreDirs.includes(file.name)) {
          markdownFiles = markdownFiles.concat(await getAllMarkdownFiles(fullPath));
        }
      } else if (file.name.endsWith('.md')) {
        markdownFiles.push(fullPath);
      }
    }
    return markdownFiles;
  }

async function fixInternalLinks() {
  console.log(dryRun ? 'Starting link fixing in DRY RUN mode...' : 'Starting link fixing...');

  const manifestContent = await fs.readFile(manifestPath, 'utf8');
  const manifest: { files: FileAction[] } = JSON.parse(manifestContent);

  const linkMap = new Map<string, string>();
  for (const action of manifest.files) {
    if (action.action === 'move' && action.old_path && action.new_path) {
      linkMap.set(action.old_path.replace(/\\/g, '/'), action.new_path.replace(/\\/g, '/'));
    }
  }

  const allMarkdownFiles = await getAllMarkdownFiles(workspaceRoot);

  for (const filePath of allMarkdownFiles) {
    let content = await fs.readFile(filePath, 'utf8');
    let changed = false;

    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    let newContent = content.replace(linkRegex, (match, text, url) => {
        if (url.startsWith('http') || url.startsWith('#')) return match;

        const [linkPath, anchor] = url.split('#');
        const absoluteLinkPath = path.resolve(path.dirname(filePath), linkPath);
        const linkKey = path.relative(workspaceRoot, absoluteLinkPath).replace(/\\/g, '/');
        
        const newRelativePath = linkMap.get(linkKey);

        if (newRelativePath) {
            const newAbsoluteLinkPath = path.join(workspaceRoot, newRelativePath);
            let updatedLink = path.relative(path.dirname(filePath), newAbsoluteLinkPath).replace(/\\/g, '/');

            if (!updatedLink.startsWith('.') && !updatedLink.startsWith('/')) {
                updatedLink = './' + updatedLink;
            }

            if (anchor) updatedLink += '#' + anchor;
            
            console.log(`FIXING in ${path.relative(workspaceRoot, filePath)}: ${url} -> ${updatedLink}`);
            changed = true;
            return `[${text}](${updatedLink})`;
        }

        return match;
    });

    if (changed && !dryRun) {
      await fs.writeFile(filePath, newContent, 'utf8');
    }
  }

  console.log('Link fixing complete.');
  if (dryRun) {
    console.log('NOTE: This was a dry run. No files were actually changed.');
  }
}

fixInternalLinks().catch(console.error);
```

**B. Run the script:**
Again, start with a dry run.
```bash
npx tsx scripts/fix-internal-links.ts --dry-run
```
Then run it for real.
```bash
npx tsx scripts/fix-internal-links.ts
```

---

### Step 5: Final Polish

The final step is to manually update key documents to reflect the new structure.

**A. Update `CONTRIBUTING.md`:**
Replace the "Information Architecture" section with the following:

```markdown
### 2. Information Architecture (What Goes Where)

This repository is structured as a comprehensive knowledge base. The core narrative of the project is laid out in a series of top-level markdown files in the root directory. Each of these files serves as an entry point and overview for a major concept. Detailed supporting documents are organized into corresponding subdirectories.

- **`introduction.md`**: High-level overview, blueprint, and whitepaper for the project.
- **`problem.md`**: The core problem the DIH aims to solve. Detailed analyses are in `problem/`.
- **`solution.md`**: The proposed solution. Detailed breakdowns of the components (1% Treaty, DIH, dFDA) are in `solution/`.
- **`strategy.md`**: The plan to achieve the solution. Details on fundraising, legal, and political strategy are in `strategy/`.
- **`economics.md`**: The financial engine. Details on tokenomics, value capture, and incentives are in `economics/`.
- **`governance.md`**: The DAO and governance model. Details on structure and fraud prevention are in `governance/`.
- **`roadmap.md`**: The canonical project roadmap.
- **`FAQ.md`**: Frequently Asked Questions.

**Content Directories:**

- **`reference/`**: External citations, data, and source materials.
- **`community/`**: Information for community members, partners, and collaborators.
- **`operations/`**: Internal processes, hiring information, and operational playbooks.
- **`scripts/`**: Automation scripts for repository maintenance.
- **`assets/`**: Images, diagrams, and other binary assets.

**Rule:** Keep the root directory clean and focused on the main narrative. New supporting documents should be placed within the appropriate subdirectory.
```

**B. Update `index.md`:**
Replace the entire content of `index.md` with the following:

```markdown
---
title: Decentralized Institutes of Health - Master Index & Sitemap
description: 'The master table of contents and sitemap for the DIH knowledge base, the central repository for the strategy and operational plans for The 1% Treaty.'
published: true
date: '2025-08-23T00:00:00.000Z'
tags: [index, sitemap, toc, strategy]
editor: markdown
dateCreated: '2025-08-22T00:00:00.000Z'
---

# Master Index & Sitemap

This document serves as the master table of contents for the Decentralized Institutes of Health (DIH) knowledge base.

## The Core Narrative

The story of the DIH is best understood by reading these documents in order.

- **[Introduction](./introduction.md):** The high-level vision and blueprint for the entire project.
- **[The Problem](./problem.md):** A detailed analysis of the core problems we aim to solve, from the costs of war to the inefficiencies of medical research.
- **[The Solution](./solution.md):** A comprehensive overview of our proposed solution, built on a "Peace Profiteering" engine.
- **[The Strategy](./strategy.md):** The plan to achieve the solution, covering political, legal, and fundraising strategies.
- **[The Economics](./economics.md):** The financial engine that makes the project viable, including tokenomics and value-capture models.
- **[The Governance](./governance.md):** The decentralized model for managing the DIH treasury and ensuring transparency.
- **[Roadmap](./roadmap.md):** The canonical, multi-year plan for the project.
- **[FAQ](./FAQ.md):** Answers to frequently asked questions.

## Detailed Content Hubs

For deeper dives into specific topics, please see the main overview file for each section.

-   **[Community](./community/community-overview.md):** For partners, contributors, and those looking to get involved.
-   **[Operations](./operations/operations-overview.md):** Internal processes, hiring plans, and operational playbooks.
-   **[Reference](./reference/reference-index.md):** The library of external citations, studies, and source data.
```

---

### Step 6: Cleanup

After the refactor is complete and verified, the scripts (`generate-inventory.ts`, `execute-refactor.ts`, `fix-internal-links.ts`) and the manifest (`refactor-manifest.json`) can be deleted.
