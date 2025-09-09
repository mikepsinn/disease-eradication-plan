# DIH Wiki Refactoring Plan
*Unified plan to restructure the repository into a comprehensive, narrative-driven knowledge base*

## Objective

Transform the repository from a collection of documents into a well-organized knowledge base that:
- Presents the core DIH narrative clearly at the root level
- Improves discoverability and contributor experience
- Completes the rebrand from "1% Treaty Wiki" to "Decentralized Institutes of Health"
- Maintains all valuable content while removing redundancy

## Current Status

**Completed Foundation Work:**
- ✅ Created GitHub organization and main repository
- ✅ Performed initial search-and-replace for branding updates
- ✅ Generated content inventory (154 markdown files catalogued)
- ✅ Created cleanup scripts for orphaned images

**Remaining Work:**
- 🔄 Execute the file reorganization
- 🔄 Fix internal links
- 🔄 Update root-level narrative files
- 🔄 Clean up redundant planning documents

## Target Structure

The final structure presents the core narrative at the root, with supporting details organized thematically:

```
/
├── introduction.md          # High-level blueprint and vision
├── problem.md              # Problems we're solving
├── solution.md             # Our three-part solution (1% Treaty → DIH → dFDA)
├── strategy.md             # How we execute the plan
├── economics.md            # Financial engine and tokenomics
├── governance.md           # DAO structure and operations
├── roadmap.md              # Canonical timeline
├── FAQ.md                  # Common questions
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

## Execution Plan

This refactoring uses three automated scripts to safely reorganize the repository:

### Step 1: Create the Refactor Manifest ⚠️ **MANUAL STEP**

Create `operations/refactor-manifest.json` - the single source of truth for all file operations. Every file must have an action: `move`, `delete`, `keep`, or `create`.

**Example structure:**
```json
{
  "files": [
    {
      "old_path": "architecture/blueprint.md",
      "new_path": "introduction.md",
      "action": "move",
      "reason": "Serves as the high-level introduction to the project"
    },
    {
      "old_path": "operations/wiki-restructuring-plan.md",
      "action": "delete",
      "reason": "Redundant with unified wiki-refactoring-plan.md"
    },
    {
      "new_path": "FAQ.md",
      "action": "create", 
      "reason": "Missing FAQ file for common questions"
    }
  ]
}
```

### Step 2: Generate Content Inventory (Optional)

If you need to review all existing content before creating the manifest:

```bash
npx tsx scripts/generate-inventory.ts
```

*Note: Content inventory already exists at `operations/refactoring_inventory.md`*

### Step 3: Execute the Refactor

**Create `scripts/execute-refactor.ts`:**

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

**Run the script:**
```bash
# Always dry run first
npx tsx scripts/execute-refactor.ts --dry-run

# Then execute for real
npx tsx scripts/execute-refactor.ts
```

### Step 4: Fix Internal Links

**Create `scripts/fix-internal-links.ts`:**

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

**Run the script:**
```bash
# Dry run first
npx tsx scripts/fix-internal-links.ts --dry-run

# Then execute
npx tsx scripts/fix-internal-links.ts
```

### Step 5: Update Key Files

After reorganization, manually update these files to reflect the new structure:

1. **`CONTRIBUTING.md`** - Update the "Information Architecture" section
2. **`index.md`** - Create the master sitemap pointing to new locations
3. **`README.md`** - Ensure it aligns with the new structure

### Step 6: Cleanup Redundant Files

Remove these redundant planning documents after successful refactoring:
- `operations/wiki-restructuring-plan.md` (superseded by this unified plan)
- Related issue files that are now covered by this plan:
  - `operations/issues/12-audit-and-refactor-dfda-content.md`
  - `operations/issues/13-create-internal-link-fixing-script.md` 
  - `operations/issues/14-run-link-fixing-script-and-audit-links.md`
  - `operations/issues/15-update-master-sitemap-and-final-polish.md`
  - `operations/issues/50-refactor-wiki.md`

## Next Steps

1. ⚠️ **Create the refactor manifest** (`operations/refactor-manifest.json`)
2. 🔧 **Run the three automation scripts** (with dry runs first)
3. ✏️ **Update key navigation files** (index.md, CONTRIBUTING.md)  
4. 🗑️ **Clean up redundant planning documents**

*This unified plan replaces both `wiki-restructuring-plan.md` and the scattered issue-based tasks, providing one clear path to completion.*
