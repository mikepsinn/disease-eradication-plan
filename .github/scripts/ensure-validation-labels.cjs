/**
 * Ensure Validation Labels Exist
 *
 * Creates all required labels for validation issue tracking if they don't exist.
 * Run this before creating validation issues to ensure proper labeling.
 *
 * Usage (via GitHub Actions):
 *   const script = require('./.github/scripts/ensure-validation-labels.cjs');
 *   await script({ github, context });
 */

/**
 * Label definitions with colors and descriptions
 */
const VALIDATION_LABELS = [
  // Source labels
  {
    name: 'validation',
    color: '0E8A16',
    description: 'Validation error tracking'
  },
  {
    name: 'validation:pdf',
    color: 'D93F0B',
    description: 'PDF validation errors (LLM-powered)'
  },
  {
    name: 'validation:pre-render',
    color: 'FBCA04',
    description: 'Pre-render validation errors'
  },
  {
    name: 'validation:post-render',
    color: 'FEF2C0',
    description: 'Post-render validation errors'
  },
  {
    name: 'validation:build',
    color: 'D93F0B',
    description: 'Build/compilation errors'
  },

  // Severity labels
  {
    name: 'validation:critical',
    color: 'B60205',
    description: 'Critical validation error - blocks publication'
  },
  {
    name: 'validation:warning',
    color: 'FFA500',
    description: 'Warning - should be fixed before publication'
  },
  {
    name: 'validation:info',
    color: '0E8A16',
    description: 'Informational - low priority'
  },

  // Category labels
  {
    name: 'validation:equation',
    color: '5319E7',
    description: 'LaTeX/equation rendering errors'
  },
  {
    name: 'validation:citation',
    color: '0075CA',
    description: 'Citation/bibliography errors'
  },
  {
    name: 'validation:link',
    color: '1D76DB',
    description: 'Broken link errors'
  },
  {
    name: 'validation:figure',
    color: '006B75',
    description: 'Figure/table rendering errors'
  },
  {
    name: 'validation:syntax',
    color: 'C2E0C6',
    description: 'Syntax errors'
  },

  // Control labels
  {
    name: 'auto-fixable',
    color: '7057FF',
    description: 'Can be automatically fixed - add this label to trigger auto-fix'
  },
  {
    name: 'validation:ignore',
    color: 'CCCCCC',
    description: 'Ignore this validation error - do not recreate'
  },
  {
    name: 'automated',
    color: 'EDEDED',
    description: 'Created by automated process'
  }
];

/**
 * Discover paper names from Quarto config files
 * Looks for _quarto-*.yml files in the repository root
 */
function discoverPaperNames() {
  const fs = require('fs');
  const path = require('path');

  try {
    // Get repository root (assuming script is in .github/scripts/)
    const repoRoot = path.resolve(__dirname, '../..');
    const files = fs.readdirSync(repoRoot);

    const paperNames = files
      .filter(f => f.startsWith('_quarto-') && f.endsWith('.yml'))
      .map(f => {
        // Extract paper name from _quarto-{paper-name}.yml
        const match = f.match(/^_quarto-(.+)\.yml$/);
        return match ? match[1] : null;
      })
      .filter(Boolean);

    console.log(`  Discovered ${paperNames.length} papers from Quarto configs: ${paperNames.join(', ')}`);
    return paperNames;
  } catch (error) {
    console.error('  Warning: Could not discover paper names from Quarto configs:', error.message);
    console.error('  Falling back to empty paper list');
    return [];
  }
}

/**
 * Create or update a single label
 */
async function ensureLabel(github, context, labelDef) {
  try {
    // Try to get existing label
    await github.rest.issues.getLabel({
      owner: context.repo.owner,
      repo: context.repo.repo,
      name: labelDef.name
    });

    // Label exists - update it
    console.log(`  Updating label: ${labelDef.name}`);
    await github.rest.issues.updateLabel({
      owner: context.repo.owner,
      repo: context.repo.repo,
      name: labelDef.name,
      color: labelDef.color,
      description: labelDef.description
    });

    return { action: 'updated', label: labelDef.name };
  } catch (error) {
    if (error.status === 404) {
      // Label doesn't exist - create it
      console.log(`  Creating label: ${labelDef.name}`);
      await github.rest.issues.createLabel({
        owner: context.repo.owner,
        repo: context.repo.repo,
        name: labelDef.name,
        color: labelDef.color,
        description: labelDef.description
      });

      return { action: 'created', label: labelDef.name };
    } else {
      console.error(`  Error with label ${labelDef.name}:`, error.message);
      return { action: 'error', label: labelDef.name, error: error.message };
    }
  }
}

/**
 * Main entry point
 */
async function main({ github, context }) {
  console.log('Ensuring validation labels exist...');

  const stats = {
    created: 0,
    updated: 0,
    errors: 0,
    total: 0
  };

  // Process validation labels
  for (const labelDef of VALIDATION_LABELS) {
    const result = await ensureLabel(github, context, labelDef);
    stats.total++;

    if (result.action === 'created') stats.created++;
    else if (result.action === 'updated') stats.updated++;
    else if (result.action === 'error') stats.errors++;
  }

  // Discover and process paper labels
  const paperNames = discoverPaperNames();
  for (const paperName of paperNames) {
    const labelDef = {
      name: `paper:${paperName}`,
      color: '006B75',
      description: `Issues related to ${paperName}`
    };

    const result = await ensureLabel(github, context, labelDef);
    stats.total++;

    if (result.action === 'created') stats.created++;
    else if (result.action === 'updated') stats.updated++;
    else if (result.action === 'error') stats.errors++;
  }

  console.log('\nLabel creation complete:');
  console.log(`  Created: ${stats.created}`);
  console.log(`  Updated: ${stats.updated}`);
  console.log(`  Errors: ${stats.errors}`);
  console.log(`  Total: ${stats.total}`);

  return stats;
}

module.exports = main;
