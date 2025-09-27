#!/usr/bin/env tsx
/**
 * Consolidate Orphaned Files Script
 *
 * This script processes orphaned files in brain/book/ that are not in the current
 * table of contents, extracts valuable content, merges it into appropriate chapters,
 * and moves processed files to archive/
 */

import * as fs from 'fs/promises';
import * as path from 'path';

interface FileConsolidation {
  sourcePath: string;
  targetChapter: string;
  valuableContent: string[];
  status: 'pending' | 'merged' | 'archived' | 'error';
  notes?: string;
}

interface ConsolidationLog {
  timestamp: string;
  filesProcessed: number;
  contentMerged: number;
  filesArchived: number;
  errors: string[];
  details: FileConsolidation[];
}

// Mapping of orphaned files to their target destinations
const CONSOLIDATION_MAP: Record<string, string> = {
  // Economics files
  'economics/dfda-cost-benefit-analysis.md': 'economics/victory-bonds.qmd',
  'economics/intervention-comparison-table.md': 'economics/economic-impact-summary.md',
  'economics/1-percent-treaty-peace-dividend-analysis.md': 'economics/economic-impact-summary.md',
  'economics/quantitative-value-medical-treatment.md': 'economics/economic-impact-summary.md',
  'economics/economic-value-of-accelerated-treatments.md': 'solution/dfda.md',
  'economics/financial-model.md': 'economics/victory-bonds.qmd',
  'economics/health-savings-sharing-model.md': 'economics/economic-impact-summary.md',
  'economics/investor-risk-analysis.md': 'economics/victory-bonds.qmd',
  'economics/value-of-automating-research.md': 'solution/dfda.md',
  'economics/operational-budget-model.md': 'reference/operations-roadmap.md',

  // Fundraising files (to be consolidated into new strategy file)
  'economics/fundraising/fundraising-plan.md': 'strategy/fundraising-strategy.md',
  'economics/fundraising/fundraising-whale-outreach.md': 'strategy/fundraising-strategy.md',
  'economics/fundraising/fundraising-pre-seed-terms.md': 'strategy/fundraising-strategy.md',
  'economics/fundraising/fundraising-budget-breakdown.md': 'strategy/fundraising-strategy.md',
  'economics/fundraising/fundraising-strategy.md': 'strategy/fundraising-strategy.md',

  // Legal/Governance files
  'legal/multi-entity-strategy.md': 'strategy/legal-compliance-framework.md',
  'legal/right-to-trial-act.md': 'strategy/right-to-trial-act.md',
  'legal/hhs-policy-recommendations.md': 'strategy/legal-compliance-framework.md',
  'legal/regulations-to-modify-or-rescind.md': 'strategy/legal-compliance-framework.md',
  'legal/impact-securities-reform.md': 'economics/victory-bonds.qmd',
  'legal/community-governance-framework.md': 'solution/wishocracy.md',
  'governance/dih-onchain-architecture.md': 'solution/wishocracy.md',
  'governance/organizational-structure.md': 'reference/operations-roadmap.md',

  // Strategy files
  'strategy/coalition-building.md': 'strategy/co-opt-dont-compete.md',
  'strategy/highest-leverage-advocacy.md': 'strategy/co-opt-dont-compete.md',
  'strategy/the-endgame-phasing-out-war.md': 'futures/utopia-health-and-happiness.md',
  'strategy/dfda-implementation-via-executive-action.md': 'strategy/legal-compliance-framework.md',
  'strategy/free-rider-solution.md': 'solution/1-percent-treaty.md',
  'strategy/open-ecosystem-and-bounty-model.md': 'solution/dfda.md',

  // Global referendum sub-files
  'strategy/global-referendum/global-referendum-implementation.md': 'strategy/global-referendum.md',
  'strategy/global-referendum/global-referendum-verification.md': 'strategy/global-referendum.md',
  'strategy/global-referendum/global-referendum-viral-marketing.md': 'strategy/global-referendum.md',
  'strategy/global-referendum/global-referendum-legal-compliance.md': 'strategy/global-referendum.md',
  'strategy/global-referendum/global-referendum-incentives.md': 'strategy/global-referendum.md',
  'strategy/global-referendum/global-referendum-plan.md': 'strategy/global-referendum.md',
  'strategy/global-referendum/support-petition-draft.md': 'strategy/global-referendum.md',

  // Other files
  'FAQ.md': 'reference/faq.md',
  'operations.md': 'reference/operations-roadmap.md',
  'roadmap.md': 'reference/operations-roadmap.md',
  'vision.md': 'futures/utopia-health-and-happiness.md',
  'partners/incentives.md': 'strategy/co-opt-dont-compete.md',
};

class FileConsolidator {
  private basePath: string;
  private archivePath: string;
  private log: ConsolidationLog;

  constructor(basePath: string) {
    this.basePath = basePath;
    this.archivePath = path.join(basePath, 'archive');
    this.log = {
      timestamp: new Date().toISOString(),
      filesProcessed: 0,
      contentMerged: 0,
      filesArchived: 0,
      errors: [],
      details: []
    };
  }

  async consolidate(): Promise<void> {
    console.log('Starting file consolidation process...');
    console.log(`Base path: ${this.basePath}`);
    console.log(`Archive path: ${this.archivePath}`);

    // Ensure archive directory exists
    await fs.mkdir(this.archivePath, { recursive: true });

    // Process each file in the consolidation map
    for (const [sourceFile, targetFile] of Object.entries(CONSOLIDATION_MAP)) {
      await this.processFile(sourceFile, targetFile);
    }

    // Archive section overview files
    const overviewFiles = ['problem.md', 'solution.md', 'proof.md', 'economics.md', 'strategy.md', 'legal.md', 'governance.md'];
    for (const file of overviewFiles) {
      await this.archiveFile(file, 'Section overview file - content distributed to chapters');
    }

    // Generate and save consolidation report
    await this.generateReport();

    console.log(`\nConsolidation complete!`);
    console.log(`Files processed: ${this.log.filesProcessed}`);
    console.log(`Content merged: ${this.log.contentMerged}`);
    console.log(`Files archived: ${this.log.filesArchived}`);
    console.log(`Errors: ${this.log.errors.length}`);
  }

  private async processFile(sourceFile: string, targetFile: string): Promise<void> {
    const sourcePath = path.join(this.basePath, sourceFile);
    const targetPath = path.join(this.basePath, targetFile);

    const consolidation: FileConsolidation = {
      sourcePath: sourceFile,
      targetChapter: targetFile,
      valuableContent: [],
      status: 'pending'
    };

    try {
      // Check if source file exists
      const sourceExists = await this.fileExists(sourcePath);
      if (!sourceExists) {
        consolidation.status = 'error';
        consolidation.notes = 'Source file not found';
        this.log.details.push(consolidation);
        return;
      }

      // Read source content
      const sourceContent = await fs.readFile(sourcePath, 'utf-8');

      // Extract valuable content (skip frontmatter and empty sections)
      const valuableLines = this.extractValuableContent(sourceContent);

      if (valuableLines.length === 0) {
        consolidation.status = 'archived';
        consolidation.notes = 'No valuable content to merge';
        await this.moveToArchive(sourceFile);
        this.log.filesArchived++;
      } else {
        // Add content marker and merge
        const contentToAdd = [
          '',
          `<!-- BEGIN CONTENT MERGED FROM ${sourceFile} -->`,
          ...valuableLines,
          `<!-- END CONTENT MERGED FROM ${sourceFile} -->`,
          ''
        ].join('\n');

        consolidation.valuableContent = valuableLines.slice(0, 3); // Store first 3 lines for log

        // Check if target exists, create if needed
        const targetExists = await this.fileExists(targetPath);
        if (!targetExists) {
          // Create new file with proper frontmatter
          const newContent = this.createNewFile(targetFile, contentToAdd);
          await fs.mkdir(path.dirname(targetPath), { recursive: true });
          await fs.writeFile(targetPath, newContent);
          consolidation.notes = 'Created new target file';
        } else {
          // Append to existing file
          await fs.appendFile(targetPath, contentToAdd);
          consolidation.notes = 'Merged into existing file';
        }

        consolidation.status = 'merged';
        this.log.contentMerged++;

        // Move source to archive
        await this.moveToArchive(sourceFile);
        this.log.filesArchived++;
      }

      this.log.filesProcessed++;
      this.log.details.push(consolidation);
      console.log(`✓ Processed: ${sourceFile} → ${targetFile}`);

    } catch (error) {
      consolidation.status = 'error';
      consolidation.notes = error.message;
      this.log.errors.push(`Error processing ${sourceFile}: ${error.message}`);
      this.log.details.push(consolidation);
      console.error(`✗ Error: ${sourceFile} - ${error.message}`);
    }
  }

  private extractValuableContent(content: string): string[] {
    const lines = content.split('\n');
    const valuableLines: string[] = [];
    let inFrontmatter = false;
    let frontmatterCount = 0;

    for (const line of lines) {
      // Skip frontmatter
      if (line === '---') {
        frontmatterCount++;
        if (frontmatterCount === 1) {
          inFrontmatter = true;
          continue;
        } else if (frontmatterCount === 2) {
          inFrontmatter = false;
          continue;
        }
      }

      if (inFrontmatter) continue;

      // Skip empty lines at the beginning
      if (valuableLines.length === 0 && line.trim() === '') continue;

      // Skip section headers that are just "TBD" or "TODO"
      if (line.match(/^#+\s*(TBD|TODO|Coming Soon|Work in Progress)\s*$/i)) continue;

      // Skip lines that are just "This section is under construction" etc.
      if (line.match(/under construction|coming soon|to be added|work in progress/i)) continue;

      valuableLines.push(line);
    }

    // Trim trailing empty lines
    while (valuableLines.length > 0 && valuableLines[valuableLines.length - 1].trim() === '') {
      valuableLines.pop();
    }

    return valuableLines;
  }

  private createNewFile(targetFile: string, content: string): string {
    const title = path.basename(targetFile, '.md').replace(/-/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());

    const frontmatter = [
      '---',
      `title: "${title}"`,
      `description: "Consolidated content from orphaned files"`,
      `published: false`,
      `date: "${new Date().toISOString()}"`,
      `tags: [consolidated, archive]`,
      `dateCreated: "${new Date().toISOString()}"`,
      '---',
      '',
      `# ${title}`,
      '',
      '<!-- This file contains content consolidated from orphaned files -->',
      ''
    ].join('\n');

    return frontmatter + content;
  }

  private async moveToArchive(sourceFile: string): Promise<void> {
    const sourcePath = path.join(this.basePath, sourceFile);
    const archivePath = path.join(this.archivePath, sourceFile);

    // Create archive subdirectory if needed
    await fs.mkdir(path.dirname(archivePath), { recursive: true });

    // Move file
    await fs.rename(sourcePath, archivePath);
  }

  private async archiveFile(file: string, reason: string): Promise<void> {
    const sourcePath = path.join(this.basePath, file);

    if (await this.fileExists(sourcePath)) {
      await this.moveToArchive(file);
      this.log.filesArchived++;
      this.log.details.push({
        sourcePath: file,
        targetChapter: 'N/A',
        valuableContent: [],
        status: 'archived',
        notes: reason
      });
      console.log(`✓ Archived: ${file}`);
    }
  }

  private async fileExists(filePath: string): Promise<boolean> {
    try {
      await fs.access(filePath);
      return true;
    } catch {
      return false;
    }
  }

  private async generateReport(): Promise<void> {
    const reportPath = path.join(this.archivePath, 'consolidation-report.json');
    await fs.writeFile(reportPath, JSON.stringify(this.log, null, 2));

    // Also create a markdown summary
    const summaryPath = path.join(this.archivePath, 'consolidation-summary.md');
    const summary = [
      '# File Consolidation Report',
      '',
      `Generated: ${this.log.timestamp}`,
      '',
      '## Summary',
      `- Files Processed: ${this.log.filesProcessed}`,
      `- Content Merged: ${this.log.contentMerged}`,
      `- Files Archived: ${this.log.filesArchived}`,
      `- Errors: ${this.log.errors.length}`,
      '',
      '## Details',
      '',
      ...this.log.details.map(d =>
        `- **${d.sourcePath}** → ${d.targetChapter} (${d.status})${d.notes ? ` - ${d.notes}` : ''}`
      ),
      '',
      this.log.errors.length > 0 ? '## Errors\n' + this.log.errors.join('\n') : ''
    ].join('\n');

    await fs.writeFile(summaryPath, summary);
    console.log(`\nReports saved to ${this.archivePath}`);
  }
}

// Run the consolidation
async function main() {
  const basePath = path.join(process.cwd(), 'brain', 'book');
  const consolidator = new FileConsolidator(basePath);

  try {
    await consolidator.consolidate();
  } catch (error) {
    console.error('Fatal error during consolidation:', error);
    process.exit(1);
  }
}

// Execute if run directly
if (require.main === module) {
  main();
}

export { FileConsolidator, ConsolidationLog, FileConsolidation };