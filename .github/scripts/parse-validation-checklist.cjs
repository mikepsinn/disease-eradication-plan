/**
 * Parse validation error checklists and logs into structured JSON
 *
 * Reads markdown checklist files (pdf-validation-checklist-*.md) and
 * validation script outputs to produce a unified JSON error report.
 *
 * Usage:
 *   node .github/scripts/parse-validation-checklist.js [directory]
 *
 * Outputs JSON to stdout with structure:
 * {
 *   "timestamp": "ISO 8601",
 *   "errors": [
 *     {
 *       "source": "pdf-validation" | "pre-render" | "post-render" | "build",
 *       "paper": "paper-name",
 *       "severity": "CRITICAL" | "WARNING" | "INFO",
 *       "type": "error-type-string",
 *       "page": number | null,
 *       "message": "error message",
 *       "suggested_fix": "fix instructions",
 *       "evidence_snippet": "context snippet",
 *       "locator_hint": "how to find in source",
 *       "file_path": "path/to/checklist.md"
 *     }
 *   ]
 * }
 */

const fs = require('fs');
const path = require('path');

/**
 * Extract paper name from checklist filename
 * pdf-validation-checklist-dfda-spec-paper.md -> dfda-spec-paper
 */
function extractPaperName(filename) {
  const match = filename.match(/^pdf-validation-checklist-(.+)\.md$/);
  return match ? match[1] : 'unknown';
}

/**
 * Parse severity emoji to level
 */
function parseSeverity(line) {
  if (line.includes('🔴') || line.includes('CRITICAL')) return 'CRITICAL';
  if (line.includes('🟡') || line.includes('WARNING')) return 'WARNING';
  if (line.includes('🟢') || line.includes('INFO')) return 'INFO';
  return 'WARNING'; // default
}

/**
 * Extract error type from section header
 * ## 🔴 LLM_EQUATION_RENDERING_DEFECT (3 issue(s)) -> LLM_EQUATION_RENDERING_DEFECT
 * ## 🟡 LLM_BROKEN_REFERENCES/CITATIONS (1 issue(s)) -> LLM_BROKEN_REFERENCES/CITATIONS
 */
function extractErrorType(line) {
  const match = line.match(/##.*?([A-Z_/]+)\s*\(/);
  return match ? match[1] : 'UNKNOWN_ERROR';
}

/**
 * Parse page number from occurrence line
 * - [ ] **Page 24:** Message... -> 24
 */
function extractPageNumber(line) {
  const match = line.match(/\*\*Page\s+(\d+):\*\*/);
  return match ? parseInt(match[1], 10) : null;
}

/**
 * Extract message from occurrence line
 * - [ ] **Page 24:** Missing Greek symbols... -> Missing Greek symbols...
 */
function extractMessage(line) {
  const match = line.match(/\*\*Page\s+\d+:\*\*\s*(.+)/);
  if (match) return match[1].trim();

  // Fallback: try to extract after checkbox
  const fallback = line.match(/- \[ \]\s*(.+)/);
  return fallback ? fallback[1].trim() : line.trim();
}

/**
 * Parse context line that follows occurrences
 *   - Context: `suggested_fix=... | evidence_snippet=... | locator_hint=...`
 */
function parseContext(contextLine) {
  const result = {
    suggested_fix: '',
    evidence_snippet: '',
    locator_hint: ''
  };

  if (!contextLine) return result;

  // Extract content within backticks
  const match = contextLine.match(/`([^`]+)`/);
  if (!match) return result;

  const content = match[1];
  const parts = content.split('|').map(s => s.trim());

  for (const part of parts) {
    const [key, ...valueParts] = part.split('=');
    const value = valueParts.join('=').trim();

    if (key === 'suggested_fix') result.suggested_fix = value;
    else if (key === 'evidence_snippet') result.evidence_snippet = value;
    else if (key === 'locator_hint') result.locator_hint = value;
  }

  return result;
}

/**
 * Parse a single PDF validation checklist markdown file
 */
function parsePdfValidationChecklist(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  const errors = [];

  const paperName = extractPaperName(path.basename(filePath));

  let currentSection = null;
  let currentSeverity = 'WARNING';
  let currentErrorType = 'UNKNOWN_ERROR';
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Detect error type section header
    if (line.startsWith('## ') && (line.includes('🔴') || line.includes('🟡') || line.includes('🟢'))) {
      currentSeverity = parseSeverity(line);
      currentErrorType = extractErrorType(line);
      i++;
      continue;
    }

    // Detect occurrence (error item)
    if (line.trim().startsWith('- [ ]') && line.includes('**Page')) {
      const pageNum = extractPageNumber(line);
      const message = extractMessage(line);

      // Look ahead for context line
      let contextLine = null;
      if (i + 1 < lines.length && lines[i + 1].trim().startsWith('- Context:')) {
        contextLine = lines[i + 1];
        i++; // skip context line on next iteration
      }

      const context = parseContext(contextLine);

      errors.push({
        source: 'pdf-validation',
        paper: paperName,
        severity: currentSeverity,
        type: currentErrorType,
        page: pageNum,
        message: message,
        suggested_fix: context.suggested_fix,
        evidence_snippet: context.evidence_snippet,
        locator_hint: context.locator_hint,
        file_path: filePath
      });
    }

    i++;
  }

  return errors;
}

/**
 * Find all validation checklist files in a directory
 */
function findChecklistFiles(dir) {
  const files = fs.readdirSync(dir);
  return files
    .filter(f => f.startsWith('pdf-validation-checklist-') && f.endsWith('.md'))
    .map(f => path.join(dir, f));
}

/**
 * Main entry point
 */
function main() {
  const args = process.argv.slice(2);
  const searchDir = args[0] || process.cwd();

  if (!fs.existsSync(searchDir)) {
    console.error(JSON.stringify({
      error: 'Directory not found',
      path: searchDir
    }, null, 2));
    process.exit(1);
  }

  const checklistFiles = findChecklistFiles(searchDir);

  if (checklistFiles.length === 0) {
    // No errors found - output empty result
    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      errors: []
    }, null, 2));
    return;
  }

  const allErrors = [];

  for (const file of checklistFiles) {
    try {
      const errors = parsePdfValidationChecklist(file);
      allErrors.push(...errors);
    } catch (err) {
      console.error(`Error parsing ${file}: ${err.message}`, { err });
      // Continue with other files
    }
  }

  // Output JSON
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    totalErrors: allErrors.length,
    errors: allErrors
  }, null, 2));
}

// Run if executed directly
if (require.main === module) {
  main();
}

module.exports = {
  parsePdfValidationChecklist,
  findChecklistFiles,
  extractPaperName,
  parseSeverity,
  extractErrorType,
  extractPageNumber,
  extractMessage,
  parseContext
};
