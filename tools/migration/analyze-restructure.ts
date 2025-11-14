#!/usr/bin/env node
/**
 * Migration Analysis Script - AI Agent Restructure
 *
 * Analyzes the impact of restructuring the repository to agent-oriented architecture:
 * - brain/book/ → knowledge/
 * - dih-economic-models/ → knowledge/ (content) + dih_models/ (Python)
 * - scripts/ → tools/
 *
 * This script does NOT modify any files - it only analyzes and reports.
 */

import * as fs from 'fs';
import * as path from 'path';
import { glob } from 'glob';

interface FileMapping {
  from: string;
  to: string;
  type: 'move' | 'rename' | 'content-update';
}

interface Reference {
  file: string;
  line: number;
  content: string;
  oldPath: string;
  newPath: string;
  type: 'cross-reference' | 'python-import' | 'path-reference';
}

interface AnalysisReport {
  fileMappings: FileMapping[];
  references: Reference[];
  configChanges: {
    file: string;
    changes: string[];
  }[];
  summary: {
    totalFiles: number;
    totalReferences: number;
    highRiskChanges: number;
    mediumRiskChanges: number;
    lowRiskChanges: number;
  };
}

const PROJECT_ROOT = process.cwd();

class MigrationAnalyzer {
  private report: AnalysisReport = {
    fileMappings: [],
    references: [],
    configChanges: [],
    summary: {
      totalFiles: 0,
      totalReferences: 0,
      highRiskChanges: 0,
      mediumRiskChanges: 0,
      lowRiskChanges: 0,
    },
  };

  async analyze(): Promise<AnalysisReport> {
    console.log('🔍 Starting migration analysis...\n');

    // Step 1: Map all files to be moved
    console.log('📁 Step 1: Mapping files to be moved...');
    await this.mapFilesToMove();

    // Step 2: Find all cross-references in .qmd files
    console.log('🔗 Step 2: Finding cross-references in .qmd files...');
    await this.findCrossReferences();

    // Step 3: Find all Python imports
    console.log('🐍 Step 3: Finding Python imports...');
    await this.findPythonImports();

    // Step 4: Find path references in scripts/tools
    console.log('🛠️  Step 4: Finding path references in scripts...');
    await this.findScriptPathReferences();

    // Step 5: Find configuration file changes
    console.log('⚙️  Step 5: Analyzing configuration files...');
    await this.analyzeConfigFiles();

    // Step 6: Calculate summary
    this.calculateSummary();

    console.log('\n✅ Analysis complete!\n');
    return this.report;
  }

  private async mapFilesToMove(): Promise<void> {
    // Helper to normalize Windows backslashes to forward slashes
    const normalizePath = (p: string) => p.replace(/\\/g, '/');

    // brain/book/* → knowledge/*
    const brainBookFiles = await glob('brain/book/**/*.{qmd,md}', { cwd: PROJECT_ROOT });
    for (const file of brainBookFiles) {
      const normalized = normalizePath(file);
      const newPath = normalized.replace('brain/book/', 'knowledge/');
      this.report.fileMappings.push({
        from: file,
        to: newPath,
        type: 'move',
      });
    }

    // dih-economic-models/economics/*.qmd → knowledge/economics/
    const economicsFiles = await glob('dih-economic-models/economics/*.qmd', { cwd: PROJECT_ROOT });
    for (const file of economicsFiles) {
      const normalized = normalizePath(file);
      const newPath = normalized.replace('dih-economic-models/economics/', 'knowledge/economics/');
      this.report.fileMappings.push({
        from: file,
        to: newPath,
        type: 'move',
      });
    }

    // dih-economic-models/appendix/*.qmd → knowledge/appendix/
    const appendixFiles = await glob('dih-economic-models/appendix/*.qmd', { cwd: PROJECT_ROOT });
    for (const file of appendixFiles) {
      const normalized = normalizePath(file);
      const newPath = normalized.replace('dih-economic-models/appendix/', 'knowledge/appendix/');
      this.report.fileMappings.push({
        from: file,
        to: newPath,
        type: 'move',
      });
    }

    // dih-economic-models/figures/*.qmd → knowledge/figures/
    const figureFiles = await glob('dih-economic-models/figures/*.qmd', { cwd: PROJECT_ROOT });
    for (const file of figureFiles) {
      const normalized = normalizePath(file);
      const newPath = normalized.replace('dih-economic-models/figures/', 'knowledge/figures/');
      this.report.fileMappings.push({
        from: file,
        to: newPath,
        type: 'move',
      });
    }

    // Python package files
    this.report.fileMappings.push(
      {
        from: 'dih-economic-models/economic_parameters.py',
        to: 'dih_models/parameters.py',
        type: 'move',
      },
      {
        from: 'dih-economic-models/figures/_chart_style.py',
        to: 'dih_models/plotting/chart_style.py',
        type: 'move',
      },
      {
        from: 'dih-economic-models/figures/_graphviz_helper.py',
        to: 'dih_models/plotting/graphviz_helper.py',
        type: 'move',
      },
      {
        from: 'dih-economic-models/__init__.py',
        to: 'dih_models/__init__.py',
        type: 'move',
      }
    );

    // scripts/* → tools/*
    const scriptFiles = await glob('scripts/**/*', { cwd: PROJECT_ROOT, nodir: true });
    for (const file of scriptFiles) {
      const normalized = normalizePath(file);
      const newPath = normalized.replace('scripts/', 'tools/');
      this.report.fileMappings.push({
        from: file,
        to: newPath,
        type: 'move',
      });
    }

    console.log(`   Found ${this.report.fileMappings.length} files to move/rename`);
  }

  private async findCrossReferences(): Promise<void> {
    // Find all .qmd files
    const qmdFiles = await glob('**/*.qmd', {
      cwd: PROJECT_ROOT,
      ignore: ['node_modules/**', '_book/**', '_freeze/**', '.quarto/**'],
    });

    for (const file of qmdFiles) {
      const content = fs.readFileSync(path.join(PROJECT_ROOT, file), 'utf-8');
      const lines = content.split('\n');

      lines.forEach((line, index) => {
        // Find markdown links: [text](path)
        const markdownLinkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
        let match;
        while ((match = markdownLinkRegex.exec(line)) !== null) {
          const linkedPath = match[2];

          // Check if it references old paths
          if (linkedPath.includes('brain/book/') ||
              linkedPath.includes('dih-economic-models/') ||
              linkedPath.includes('../../../')) {

            let newPath = linkedPath;

            // Update brain/book/ references
            newPath = newPath.replace(/brain\/book\//g, 'knowledge/');

            // Update dih-economic-models/ references
            newPath = newPath.replace(/dih-economic-models\/economics\//g, 'knowledge/economics/');
            newPath = newPath.replace(/dih-economic-models\/appendix\//g, 'knowledge/appendix/');
            newPath = newPath.replace(/dih-economic-models\/figures\//g, 'knowledge/figures/');

            if (newPath !== linkedPath) {
              this.report.references.push({
                file,
                line: index + 1,
                content: line.trim(),
                oldPath: linkedPath,
                newPath,
                type: 'cross-reference',
              });
            }
          }
        }

        // Find Quarto includes: {{< include path >}}
        const includeRegex = /\{\{<\s*include\s+([^>]+)\s*>\}\}/g;
        while ((match = includeRegex.exec(line)) !== null) {
          const includedPath = match[1].trim();

          if (includedPath.includes('brain/book/') || includedPath.includes('dih-economic-models/')) {
            let newPath = includedPath;
            newPath = newPath.replace(/brain\/book\//g, 'knowledge/');
            newPath = newPath.replace(/dih-economic-models\/economics\//g, 'knowledge/economics/');
            newPath = newPath.replace(/dih-economic-models\/appendix\//g, 'knowledge/appendix/');
            newPath = newPath.replace(/dih-economic-models\/figures\//g, 'knowledge/figures/');

            if (newPath !== includedPath) {
              this.report.references.push({
                file,
                line: index + 1,
                content: line.trim(),
                oldPath: includedPath,
                newPath,
                type: 'cross-reference',
              });
            }
          }
        }
      });
    }

    console.log(`   Found ${this.report.references.filter(r => r.type === 'cross-reference').length} cross-references to update`);
  }

  private async findPythonImports(): Promise<void> {
    const qmdFiles = await glob('**/*.qmd', {
      cwd: PROJECT_ROOT,
      ignore: ['node_modules/**', '_book/**', '_freeze/**', '.quarto/**'],
    });

    for (const file of qmdFiles) {
      const content = fs.readFileSync(path.join(PROJECT_ROOT, file), 'utf-8');
      const lines = content.split('\n');

      lines.forEach((line, index) => {
        // Check for old Python imports
        if (line.includes('from economic_parameters import')) {
          this.report.references.push({
            file,
            line: index + 1,
            content: line.trim(),
            oldPath: 'from economic_parameters import',
            newPath: 'from dih_models.parameters import',
            type: 'python-import',
          });
        }

        if (line.includes('from figures._chart_style import')) {
          this.report.references.push({
            file,
            line: index + 1,
            content: line.trim(),
            oldPath: 'from figures._chart_style import',
            newPath: 'from dih_models.plotting.chart_style import',
            type: 'python-import',
          });
        }

        if (line.includes('from figures._graphviz_helper import')) {
          this.report.references.push({
            file,
            line: index + 1,
            content: line.trim(),
            oldPath: 'from figures._graphviz_helper import',
            newPath: 'from dih_models.plotting.graphviz_helper import',
            type: 'python-import',
          });
        }
      });
    }

    console.log(`   Found ${this.report.references.filter(r => r.type === 'python-import').length} Python imports to update`);
  }

  private async findScriptPathReferences(): Promise<void> {
    const scriptFiles = await glob('scripts/**/*.{ts,py,js}', { cwd: PROJECT_ROOT });

    for (const file of scriptFiles) {
      const content = fs.readFileSync(path.join(PROJECT_ROOT, file), 'utf-8');
      const lines = content.split('\n');

      lines.forEach((line, index) => {
        // Check for hardcoded paths
        if (line.includes('brain/book') ||
            line.includes('dih-economic-models') ||
            line.includes('scripts/')) {

          let newLine = line;
          newLine = newLine.replace(/brain\/book/g, 'knowledge');
          newLine = newLine.replace(/dih-economic-models/g, 'knowledge');
          newLine = newLine.replace(/scripts\//g, 'tools/');

          if (newLine !== line) {
            this.report.references.push({
              file,
              line: index + 1,
              content: line.trim(),
              oldPath: line.trim(),
              newPath: newLine.trim(),
              type: 'path-reference',
            });
          }
        }
      });
    }

    console.log(`   Found ${this.report.references.filter(r => r.type === 'path-reference').length} path references in scripts`);
  }

  private async analyzeConfigFiles(): Promise<void> {
    // _quarto.yml
    if (fs.existsSync(path.join(PROJECT_ROOT, '_quarto.yml'))) {
      const content = fs.readFileSync(path.join(PROJECT_ROOT, '_quarto.yml'), 'utf-8');
      const changes: string[] = [];

      if (content.includes('brain/book/')) {
        changes.push('Replace all "brain/book/" with "knowledge/"');
      }
      if (content.includes('dih-economic-models/')) {
        changes.push('Replace "dih-economic-models/economics/" with "knowledge/economics/"');
        changes.push('Replace "dih-economic-models/appendix/" with "knowledge/appendix/"');
        changes.push('Replace "dih-economic-models/figures/" with "knowledge/figures/"');
      }

      if (changes.length > 0) {
        this.report.configChanges.push({
          file: '_quarto.yml',
          changes,
        });
      }
    }

    // package.json
    if (fs.existsSync(path.join(PROJECT_ROOT, 'package.json'))) {
      const content = fs.readFileSync(path.join(PROJECT_ROOT, 'package.json'), 'utf-8');
      const changes: string[] = [];

      if (content.includes('scripts/')) {
        changes.push('Replace all "scripts/" with "tools/" in npm script paths');
      }

      if (changes.length > 0) {
        this.report.configChanges.push({
          file: 'package.json',
          changes,
        });
      }
    }

    // .github/workflows/publish.yml
    const workflowPath = path.join(PROJECT_ROOT, '.github/workflows/publish.yml');
    if (fs.existsSync(workflowPath)) {
      const content = fs.readFileSync(workflowPath, 'utf-8');
      const changes: string[] = [];

      if (content.includes('dih-economic-models/')) {
        changes.push('Change "uv pip install --system -e dih-economic-models/" to "uv pip install --system -e ."');
      }

      if (changes.length > 0) {
        this.report.configChanges.push({
          file: '.github/workflows/publish.yml',
          changes,
        });
      }
    }

    // pyproject.toml
    if (fs.existsSync(path.join(PROJECT_ROOT, 'pyproject.toml'))) {
      const changes: string[] = [
        'Update package name from "decentralized-institutes-of-health" to "dih-models"',
        'Update package directory configuration to point to dih_models/',
      ];

      this.report.configChanges.push({
        file: 'pyproject.toml',
        changes,
      });
    }

    console.log(`   Found ${this.report.configChanges.length} configuration files to update`);
  }

  private calculateSummary(): void {
    this.report.summary.totalFiles = this.report.fileMappings.length;
    this.report.summary.totalReferences = this.report.references.length;

    // High risk: Python imports (will break rendering)
    this.report.summary.highRiskChanges = this.report.references.filter(
      r => r.type === 'python-import'
    ).length;

    // Medium risk: Cross-references (will break navigation)
    this.report.summary.mediumRiskChanges = this.report.references.filter(
      r => r.type === 'cross-reference'
    ).length;

    // Low risk: Path references in scripts
    this.report.summary.lowRiskChanges = this.report.references.filter(
      r => r.type === 'path-reference'
    ).length;
  }

  printReport(): void {
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('📊 MIGRATION ANALYSIS REPORT - AI Agent Restructure');
    console.log('═══════════════════════════════════════════════════════════════\n');

    // Summary
    console.log('📈 SUMMARY');
    console.log('─────────────────────────────────────────────────────────────');
    console.log(`Total files to move/rename:     ${this.report.summary.totalFiles}`);
    console.log(`Total references to update:     ${this.report.summary.totalReferences}`);
    console.log(`  🔴 High risk (Python imports):  ${this.report.summary.highRiskChanges}`);
    console.log(`  🟡 Medium risk (cross-refs):    ${this.report.summary.mediumRiskChanges}`);
    console.log(`  🟢 Low risk (script paths):     ${this.report.summary.lowRiskChanges}`);
    console.log();

    // File mappings by category
    console.log('📁 FILE MAPPINGS');
    console.log('─────────────────────────────────────────────────────────────');

    const brainFiles = this.report.fileMappings.filter(f => f.from.startsWith('brain/'));
    console.log(`\n  brain/book/ → knowledge/ (${brainFiles.length} files)`);

    const economicsFiles = this.report.fileMappings.filter(f =>
      f.from.startsWith('dih-economic-models/economics/')
    );
    console.log(`  dih-economic-models/economics/ → knowledge/economics/ (${economicsFiles.length} files)`);

    const appendixFiles = this.report.fileMappings.filter(f =>
      f.from.startsWith('dih-economic-models/appendix/')
    );
    console.log(`  dih-economic-models/appendix/ → knowledge/appendix/ (${appendixFiles.length} files)`);

    const figureFiles = this.report.fileMappings.filter(f =>
      f.from.startsWith('dih-economic-models/figures/')
    );
    console.log(`  dih-economic-models/figures/ → knowledge/figures/ (${figureFiles.length} files)`);

    const pythonFiles = this.report.fileMappings.filter(f => f.to.startsWith('dih_models/'));
    console.log(`  dih-economic-models/*.py → dih_models/ (${pythonFiles.length} files)`);

    const scriptFiles = this.report.fileMappings.filter(f => f.from.startsWith('scripts/'));
    console.log(`  scripts/ → tools/ (${scriptFiles.length} files)`);
    console.log();

    // High risk changes
    if (this.report.summary.highRiskChanges > 0) {
      console.log('🔴 HIGH RISK CHANGES - Python Imports (will break rendering)');
      console.log('─────────────────────────────────────────────────────────────');

      const importGroups = new Map<string, Reference[]>();
      this.report.references
        .filter(r => r.type === 'python-import')
        .forEach(ref => {
          const key = ref.oldPath;
          if (!importGroups.has(key)) {
            importGroups.set(key, []);
          }
          importGroups.get(key)!.push(ref);
        });

      importGroups.forEach((refs, oldImport) => {
        const newImport = refs[0].newPath;
        console.log(`\n  ${oldImport} → ${newImport}`);
        console.log(`  Affects ${refs.length} file(s):`);
        refs.slice(0, 5).forEach(ref => {
          console.log(`    - ${ref.file}:${ref.line}`);
        });
        if (refs.length > 5) {
          console.log(`    ... and ${refs.length - 5} more`);
        }
      });
      console.log();
    }

    // Configuration changes
    if (this.report.configChanges.length > 0) {
      console.log('⚙️  CONFIGURATION FILE CHANGES');
      console.log('─────────────────────────────────────────────────────────────');
      this.report.configChanges.forEach(config => {
        console.log(`\n  ${config.file}:`);
        config.changes.forEach(change => {
          console.log(`    - ${change}`);
        });
      });
      console.log();
    }

    // Sample cross-references
    const crossRefs = this.report.references.filter(r => r.type === 'cross-reference');
    if (crossRefs.length > 0) {
      console.log('🟡 SAMPLE CROSS-REFERENCE UPDATES');
      console.log('─────────────────────────────────────────────────────────────');
      console.log(`  (Showing 10 of ${crossRefs.length} total)\n`);

      crossRefs.slice(0, 10).forEach(ref => {
        console.log(`  ${ref.file}:${ref.line}`);
        console.log(`    OLD: ${ref.oldPath}`);
        console.log(`    NEW: ${ref.newPath}`);
        console.log();
      });
    }

    console.log('═══════════════════════════════════════════════════════════════');
    console.log('✅ Analysis complete! Review this report before proceeding.');
    console.log('═══════════════════════════════════════════════════════════════\n');
  }

  async saveReport(filename: string): Promise<void> {
    const reportPath = path.join(PROJECT_ROOT, filename);
    fs.writeFileSync(reportPath, JSON.stringify(this.report, null, 2));
    console.log(`📄 Detailed report saved to: ${filename}`);
  }
}

// Run analysis
async function main() {
  const analyzer = new MigrationAnalyzer();
  await analyzer.analyze();
  analyzer.printReport();
  await analyzer.saveReport('migration-analysis-report.json');
}

main().catch(console.error);
