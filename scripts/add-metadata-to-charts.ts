#!/usr/bin/env tsx
/**
 * Add PNG metadata to all chart files
 *
 * This script updates all .qmd chart files to use add_png_metadata() for
 * proper attribution when images are shared on social media.
 */

import * as fs from 'fs';
import * as path from 'path';
import { saveFile } from './lib/file-utils';

const chartFiles = [
  'brain/figures/healthcare-spending-vs-life-expectancy.qmd',
  'brain/figures/life-expectancy-pre-post-1962.qmd',
  'brain/figures/fda-spending-life-expectancy-drug-costs-combined.qmd',
  'brain/figures/life-expectancy-before-after-fda-line-chart.qmd',
  'brain/figures/fda-spending-life-expectancy-trend-line-chart.qmd',
  'brain/figures/fda-drug-development-cost-increase-line-chart.qmd',
  'brain/figures/current-vs-dfda-clinical-trial-cost-column-chart.qmd',
  'brain/figures/one-percent-treaty-top-country-contributions-column-chart.qmd',
  'brain/figures/congressional-committee-seat-costs-column-chart.qmd',
  'brain/figures/daily-deaths-breakdown-column-chart.qmd',
  'brain/book/appendix/peace-dividend-analysis.qmd',
  'brain/book/appendix/humanity-budget-overview.qmd',
  'brain/figures/humanity-spending-priorities-bar-chart.qmd',
  'brain/figures/war-vs-curing-diseases-column-chart.qmd',
  'brain/figures/war-vs-disease-total-costs-vs-curing-spending-column-chart.qmd',
  'brain/figures/war-hidden-direct-curing-diseases-column-chart.qmd',
  'brain/figures/war-real-hidden-costs-breakdown.qmd',
  'brain/figures/war-total-costs-breakdown-vs-curing-spending-column-chart.qmd',
  'brain/figures/self-funding-roi-comparison-column-chart.qmd',
  'brain/figures/military-vs-medical-research-spending-1-percent-treaty-column-chart.qmd',
  'brain/figures/military-vs-medical-research-spending-column-chart.qmd',
  'brain/figures/military-vs-medical-spending-ratio-bar-chart.qmd',
  'brain/figures/money-flow-diagram.qmd',
  'brain/figures/nih-budget-allocation-pie-chart.qmd',
  'brain/figures/philanthropic-cost-effectiveness-comparison-bar-chart.qmd',
  'brain/figures/public-health-interventions-economic-benefit-comparison-column-chart.qmd',
  'brain/figures/military-vs-medical-research-direct-spending-column-chart.qmd',
  'brain/figures/health-programs-vs-1-percent-treaty-societal-benefits-bar-chart.qmd',
  'brain/figures/health-interventions-roi-comparison-column-chart.qmd',
  'brain/figures/disease-war-curing-costs-column-chart.qmd',
  'brain/figures/disease-vs-war-annual-deaths-pie-chart.qmd',
  'brain/figures/disease-vs-curing-costs-column-chart.qmd',
  'brain/figures/disease-burden-war-curing-comparison.qmd',
  'brain/figures/dfda-investment-returns-bar-chart.qmd',
];

async function updateChartFile(filePath: string): Promise<void> {
  const fullPath = path.join(process.cwd(), filePath);
  let content = fs.readFileSync(fullPath, 'utf-8');

  // Skip if already has add_png_metadata
  if (content.includes('add_png_metadata')) {
    console.log(`✓ ${filePath} - already updated`);
    return;
  }

  // Skip if no plt.savefig
  if (!content.includes('plt.savefig')) {
    console.log(`⊘ ${filePath} - no plt.savefig found`);
    return;
  }

  let modified = false;

  // 1. Add add_png_metadata to imports if not present
  const importRegex = /from brain\.figures\._chart_style import \(([\s\S]*?)\)/;
  const importMatch = content.match(importRegex);

  if (importMatch) {
    const imports = importMatch[1];
    if (!imports.includes('add_png_metadata')) {
      // Add to imports
      const updatedImports = imports.trim() + ',\n    add_png_metadata';
      content = content.replace(importRegex, `from brain.figures._chart_style import (${updatedImports})`);
      modified = true;
    }
  }

  // 2. Update plt.savefig calls
  // Match patterns like:
  // plt.savefig(output_dir / 'filename.png', ...)
  // plt.savefig(some_path, ...)
  const savefigRegex = /plt\.savefig\(([\s\S]*?)\)/g;
  let match;
  const updates: Array<{ original: string; replacement: string }> = [];

  while ((match = savefigRegex.exec(content)) !== null) {
    const fullCall = match[0];
    const args = match[1];

    // Extract the file path (first argument)
    const pathMatch = args.match(/^([^,]+)/);
    if (!pathMatch) continue;

    const pathExpr = pathMatch[1].trim();

    // Generate title from filename
    const filenameMatch = pathExpr.match(/['"]([^'"]+\.png)['"]/);
    let title = '';
    if (filenameMatch) {
      const filename = filenameMatch[1].replace('.png', '').replace(/-/g, ' ');
      title = filename
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
    }

    // Check if we need to store path in a variable
    const needsVariable = !pathExpr.includes('output_path') && !pathExpr.match(/^[a-z_]+$/);

    let replacement = '';
    if (needsVariable) {
      // Need to create output_path variable
      replacement = `output_path = ${pathExpr}\nplt.savefig(output_path`;
      // Keep the rest of the arguments
      const restOfArgs = args.substring(pathMatch[0].length);
      replacement += restOfArgs + ')';

      // Add metadata call
      replacement += `\nadd_png_metadata(output_path, title="${title}")`;
    } else {
      // Path is already a variable
      const varName = pathExpr;
      replacement = fullCall + `\nadd_png_metadata(${varName}, title="${title}")`;
    }

    updates.push({ original: fullCall, replacement });
  }

  // Apply updates in reverse order to preserve positions
  for (const update of updates.reverse()) {
    content = content.replace(update.original, update.replacement);
    modified = true;
  }

  if (modified) {
    await saveFile(fullPath, content);
    console.log(`✓ ${filePath} - updated`);
  } else {
    console.log(`⊘ ${filePath} - no changes needed`);
  }
}

// Process all files
async function main() {
  console.log('Updating chart files with metadata...\n');
  for (const file of chartFiles) {
    try {
      await updateChartFile(file);
    } catch (error) {
      console.error(`✗ ${file} - error: ${error}`);
    }
  }
  console.log('\nDone!');
}

main().catch(console.error);
