#!/usr/bin/env node
import * as fs from 'fs';
import * as glob from 'glob';
import { saveFile } from './lib/file-utils';

interface FlaggedStatement {
  file: string;
  line: number;
  text: string;
  pattern: string;
  severity: 'HIGH' | 'MEDIUM' | 'LOW';
  category: string;
}

// Red flag patterns to search for
const patterns = {
  // HIGH SEVERITY - Likely factually wrong
  falseAttribution: {
    regex: /\b(demands?|forces?|makes? us|requires?|insists?)\b/gi,
    severity: 'HIGH' as const,
    description: 'False attribution of intent'
  },

  conspiracy: {
    regex: /\b(deliberately|intentionally|purposely|scheme|plot|conspiracy)\b/gi,
    severity: 'HIGH' as const,
    description: 'Conspiracy language'
  },

  absoluteStatements: {
    regex: /\b(all|every|never|always|zero|nobody|everyone|nothing|everything)\b/gi,
    severity: 'MEDIUM' as const,
    description: 'Absolute statements rarely accurate'
  },

  characterAttacks: {
    regex: /\b(idiots?|morons?|evil|corrupt|stupid|incompetent|sociopaths?|psychopaths?|criminals?)\b/gi,
    severity: 'HIGH' as const,
    description: 'Personal/character attacks'
  },

  oversimplification: {
    regex: /\b(just|simply|only|merely)\s+(need|have|requires?|solve|fix)/gi,
    severity: 'LOW' as const,
    description: 'Oversimplification of complex issues'
  },

  falseCausation: {
    regex: /\b(causes?|makes?|forces?|results? in|leads? to)\s+(\d+\s+)?(deaths?|murder|killing)/gi,
    severity: 'HIGH' as const,
    description: 'Potentially false causation claims'
  },

  emotionalManipulation: {
    regex: /\b(murder|genocide|holocaust|massacre|slaughter)\b/gi,
    severity: 'MEDIUM' as const,
    description: 'Emotional manipulation/hyperbole'
  },

  misleadingAgency: {
    regex: /\b(NIH|FDA|CDC|WHO|Pentagon|Congress)\s+(demands?|requires?|forces?|kills?|murders?)/gi,
    severity: 'HIGH' as const,
    description: 'Misleading agency attribution'
  },

  unsourcedStats: {
    regex: /\b\d+%|\$\d+[BMT]|\d+X\s+(more|less|higher|lower|better|worse)\b/gi,
    severity: 'MEDIUM' as const,
    description: 'Statistics that may need sources'
  },

  unfairComparisons: {
    regex: /\b(while|but|instead of|rather than)\s+.*\b(gets?|receives?|spends?|wastes?)\b/gi,
    severity: 'LOW' as const,
    description: 'Potentially unfair comparisons'
  }
};

// Files to audit
const BOOK_DIR = 'brain/book';
const OUTLINE_FILE = 'OUTLINE.md';

function auditFile(filePath: string): FlaggedStatement[] {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  const flagged: FlaggedStatement[] = [];

  lines.forEach((line, index) => {
    // Skip YAML frontmatter
    if (index === 0 && line.startsWith('---')) {
      const endIndex = lines.findIndex((l, i) => i > 0 && l === '---');
      if (endIndex > 0 && index < endIndex) return;
    }

    // Skip code blocks
    if (line.startsWith('```')) return;

    // Check each pattern
    for (const [patternName, pattern] of Object.entries(patterns)) {
      const matches = line.match(pattern.regex);
      if (matches) {
        flagged.push({
          file: filePath,
          line: index + 1,
          text: line.trim(),
          pattern: pattern.description,
          severity: pattern.severity,
          category: patternName
        });
      }
    }
  });

  return flagged;
}

function generateReport(results: FlaggedStatement[]): string {
  let report = '# Accuracy Audit Report\n\n';
  report += `Generated: ${new Date().toISOString()}\n\n`;
  report += `Total issues found: ${results.length}\n\n`;

  // Group by severity
  const bySeverity = {
    HIGH: results.filter(r => r.severity === 'HIGH'),
    MEDIUM: results.filter(r => r.severity === 'MEDIUM'),
    LOW: results.filter(r => r.severity === 'LOW')
  };

  report += `## Summary by Severity\n\n`;
  report += `- HIGH (Likely wrong/unfair): ${bySeverity.HIGH.length}\n`;
  report += `- MEDIUM (Potentially misleading): ${bySeverity.MEDIUM.length}\n`;
  report += `- LOW (Could be improved): ${bySeverity.LOW.length}\n\n`;

  // Group by file
  const byFile: Record<string, FlaggedStatement[]> = {};
  results.forEach(r => {
    if (!byFile[r.file]) byFile[r.file] = [];
    byFile[r.file].push(r);
  });

  report += `## Issues by File\n\n`;

  for (const [file, issues] of Object.entries(byFile)) {
    report += `### ${file}\n\n`;

    // Sort by line number
    issues.sort((a, b) => a.line - b.line);

    issues.forEach(issue => {
      const severityEmoji = {
        HIGH: '🔴',
        MEDIUM: '🟡',
        LOW: '🟢'
      }[issue.severity];

      report += `${severityEmoji} **Line ${issue.line}** [${issue.pattern}]\n`;
      report += `> ${issue.text}\n\n`;
    });
  }

  // Top patterns
  const patternCounts: Record<string, number> = {};
  results.forEach(r => {
    patternCounts[r.pattern] = (patternCounts[r.pattern] || 0) + 1;
  });

  report += `## Most Common Issues\n\n`;
  Object.entries(patternCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .forEach(([pattern, count]) => {
      report += `- ${pattern}: ${count} occurrences\n`;
    });

  return report;
}

async function main() {
  console.log('Starting accuracy audit...\n');

  // Get all .qmd files
  const qmdFiles = glob.sync(`${BOOK_DIR}/**/*.qmd`);
  const allFiles = [...qmdFiles];

  // Add outline if it exists
  if (fs.existsSync(OUTLINE_FILE)) {
    allFiles.push(OUTLINE_FILE);
  }

  console.log(`Auditing ${allFiles.length} files...\n`);

  const allResults: FlaggedStatement[] = [];

  for (const file of allFiles) {
    const results = auditFile(file);
    allResults.push(...results);

    if (results.length > 0) {
      console.log(`${file}: ${results.length} issues found`);
    }
  }

  // Generate and save report
  const report = generateReport(allResults);
  const reportPath = 'ACCURACY_AUDIT_REPORT.md';
  await saveFile(reportPath, report);

  console.log(`\n✅ Audit complete!`);
  console.log(`📊 Total issues found: ${allResults.length}`);
  console.log(`📄 Report saved to: ${reportPath}`);

  // Also create a CSV for spreadsheet analysis
  const csvPath = 'accuracy_audit_results.csv';
  const csv = [
    'File,Line,Severity,Pattern,Text',
    ...allResults.map(r =>
      `"${r.file}",${r.line},"${r.severity}","${r.pattern}","${r.text.replace(/"/g, '""')}"`
    )
  ].join('\n');

  fs.writeFileSync(csvPath, csv);
  console.log(`📊 CSV saved to: ${csvPath}`);
}

main().catch(console.error);