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

**Ultra-flat structure designed for zero ambiguity about where content belongs:**

```
/
├── README.md                    # Main pitch deck (already perfect - the core narrative)
├── problem.md                   # Why this matters (expanded analysis from README)
├── solution.md                  # The 1% Treaty → DIH → dFDA flow
├── economics.md                 # Financial models, ROI, and investment thesis
├── strategy.md                  # How we execute this plan (political, operational)  
├── legal.md                     # Compliance frameworks and structure
├── operations.md                # Team, hiring, and processes
├── FAQ.md                       # Common objections and responses
├── roadmap.md                   # Timeline and milestones
|
├── economics/                   # All financial models and analysis
│   ├── victory-bonds-tokenomics.md
│   ├── peace-dividend-value-capture.md
│   ├── fundraising-and-budget-plan.md
│   ├── dfda-cost-benefit-analysis.md
│   ├── dih-treasury-cash-flow-model.md
│   └── victory-bond-investment-thesis.md
├── strategy/                    # Detailed execution plans
│   ├── 1-percent-treaty.md
│   ├── decentralized-institutes-of-health.md
│   ├── referral-rewards-system.md
│   ├── legal-compliance-framework.md
│   ├── verification-and-fraud-prevention.md
│   └── free-rider-solution.md
├── legal/                       # Compliance and governance
│   ├── multi-entity-strategy.md
│   ├── right-to-trial-act.md
│   └── impact-securities-reform.md
├── operations/                  # HR, processes, SOPs
│   ├── hiring-plan.md
│   ├── crypto-intake-sop.md
│   ├── nonprofit-partnership-playbook.md
│   └── process-index.md
├── reference/                   # Data, studies, citations
│   ├── costs-of-war.md
│   ├── recovery-trial.md  
│   ├── global-government-medical-research-spending.md
│   └── (other reference files)
├── assets/                      # Images and diagrams
└── archive/                     # Everything else (for review/deletion)
```

**Decision Rules (Zero Ambiguity):**
- **Root level:** Core narrative files only - must directly support README.md
- **economics/:** If it's about money, ROI, or financial models → goes here
- **strategy/:** If it's about HOW we execute the plan → goes here  
- **legal/:** If it's about compliance, law, or governance → goes here
- **operations/:** If it's about team, hiring, or internal processes → goes here
- **reference/:** If it's data, studies, or citations supporting arguments → goes here
- **archive/:** Everything else goes here first for review (most will be deleted)

## Execution Plan

This refactoring uses three automated scripts to safely reorganize the repository:

### Step 1: Archive Everything (Clean Slate Approach) ⚠️ **MANUAL STEP**

**Recommended Approach:** Instead of complex file mapping, move everything to `/archive` and rebuild clean:

1. **Create the new structure** (empty folders and placeholder files)
2. **Move everything else to `/archive`** (except README.md, assets/, and scripts/)
3. **Review each archived file** and decide: merge into new structure or delete
4. **Build the new knowledge base** systematically from the ground up

**Why This Works Better:**
- ✅ **Zero chance of losing content** - everything preserved in archive
- ✅ **Forces intentional decisions** - every piece of content gets evaluated
- ✅ **Clean structure** - no legacy path dependencies or broken links
- ✅ **Clear progress tracking** - see exactly what's been processed vs. what remains

**Alternative: Traditional Manifest Approach**

If you prefer the traditional approach, create `operations/refactor-manifest.json`:

```json
{
  "files": [
    {
      "old_path": "architecture/blueprint.md",
      "new_path": "problem.md", 
      "action": "move",
      "reason": "Core problem analysis content"
    },
    {
      "old_path": "strategy/1-percent-treaty/1-percent-treaty.md",
      "new_path": "strategy/1-percent-treaty.md",
      "action": "move", 
      "reason": "Main treaty document"
    },
    {
      "new_path": "FAQ.md",
      "action": "create", 
      "reason": "Common objections from README need dedicated file"
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
