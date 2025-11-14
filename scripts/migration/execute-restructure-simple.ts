#!/usr/bin/env node
/**
 * Simplified Migration Script - Focus on Critical Changes First
 *
 * This does the migration in careful phases:
 * 1. Python package restructure (critical for imports)
 * 2. Update all Python imports
 * 3. Then we can do content moves
 */

import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';
import { glob } from 'glob';

const PROJECT_ROOT = process.cwd();

console.log('🤖 Starting simplified migration...\n');

// Phase 1: Create Python package structure
console.log('Phase 1: Creating Python package structure\n');
console.log('============================================\n');

const dirs = ['dih_models', 'dih_models/plotting'];
for (const dir of dirs) {
  if (!fs.existsSync(path.join(PROJECT_ROOT, dir))) {
    fs.mkdirSync(path.join(PROJECT_ROOT, dir), { recursive: true });
    console.log(`✅ Created ${dir}/`);
  }
}

// Copy (don't move yet) Python files
const pythonFiles = [
  { from: 'dih-economic-models/economic_parameters.py', to: 'dih_models/parameters.py' },
  { from: 'dih-economic-models/figures/_chart_style.py', to: 'dih_models/plotting/chart_style.py' },
  { from: 'dih-economic-models/figures/_graphviz_helper.py', to: 'dih_models/plotting/graphviz_helper.py' },
  { from: 'dih-economic-models/__init__.py', to: 'dih_models/__init__.py' },
];

for (const file of pythonFiles) {
  const fromPath = path.join(PROJECT_ROOT, file.from);
  const toPath = path.join(PROJECT_ROOT, file.to);

  if (fs.existsSync(fromPath)) {
    fs.copyFileSync(fromPath, toPath);
    console.log(`✅ Copied ${file.from} → ${file.to}`);
  }
}

// Create __init__.py for plotting
const initContent = '"""Plotting utilities for DIH economic models."""\n';
fs.writeFileSync(path.join(PROJECT_ROOT, 'dih_models/plotting/__init__.py'), initContent);
console.log('✅ Created dih_models/plotting/__init__.py\n');

// Phase 2: Update all Python imports
console.log('\nPhase 2: Updating Python imports in all .qmd files\n');
console.log('===================================================\n');

const qmdFiles = await glob('**/*.qmd', {
  cwd: PROJECT_ROOT,
  ignore: ['node_modules/**', '_book/**', '_freeze/**', '.quarto/**'],
});

let importCount = 0;

for (const file of qmdFiles) {
  const fullPath = path.join(PROJECT_ROOT, file);
  let content = fs.readFileSync(fullPath, 'utf-8');
  let modified = false;

  if (content.includes('from economic_parameters import')) {
    content = content.replace(/from economic_parameters import/g, 'from dih_models.parameters import');
    modified = true;
  }

  if (content.includes('from figures._chart_style import')) {
    content = content.replace(/from figures\._chart_style import/g, 'from dih_models.plotting.chart_style import');
    modified = true;
  }

  if (content.includes('from figures._graphviz_helper import')) {
    content = content.replace(/from figures\._graphviz_helper import/g, 'from dih_models.plotting.graphviz_helper import');
    modified = true;
  }

  if (modified) {
    fs.writeFileSync(fullPath, content);
    importCount++;
  }
}

console.log(`✅ Updated imports in ${importCount} files\n`);

// Phase 3: Update pyproject.toml
console.log('\nPhase 3: Updating pyproject.toml\n');
console.log('=================================\n');

const pyprojectPath = path.join(PROJECT_ROOT, 'pyproject.toml');
if (fs.existsSync(pyprojectPath)) {
  let content = fs.readFileSync(pyprojectPath, 'utf-8');

  // Update package name
  content = content.replace(/name\s*=\s*"decentralized-institutes-of-health"/, 'name = "dih-models"');

  // Add/update packages configuration
  if (!content.includes('[tool.setuptools]')) {
    content += '\n\n[tool.setuptools]\npackages = ["dih_models", "dih_models.plotting"]\n';
  } else {
    content = content.replace(/packages\s*=\s*\[.*?\]/, 'packages = ["dih_models", "dih_models.plotting"]');
  }

  fs.writeFileSync(pyprojectPath, content);
  console.log('✅ Updated pyproject.toml\n');
}

// Phase 4: Update GitHub Actions
console.log('\nPhase 4: Updating GitHub Actions\n');
console.log('==================================\n');

const workflowPath = path.join(PROJECT_ROOT, '.github/workflows/publish.yml');
if (fs.existsSync(workflowPath)) {
  let content = fs.readFileSync(workflowPath, 'utf-8');
  content = content.replace(/uv pip install --system -e dih-economic-models\//, 'uv pip install --system -e .');
  fs.writeFileSync(workflowPath, content);
  console.log('✅ Updated .github/workflows/publish.yml\n');
}

console.log('\n' + '='.repeat(70));
console.log('✨ Phase 1 Migration Complete!');
console.log('='.repeat(70));
console.log('\nWhat was done:');
console.log('  ✅ Created dih_models/ package structure');
console.log('  ✅ Copied Python files to new locations');
console.log(`  ✅ Updated ${importCount} .qmd files with new imports`);
console.log('  ✅ Updated pyproject.toml');
console.log('  ✅ Updated GitHub Actions workflow');
console.log('\nNext steps:');
console.log('  1. Test: uv pip install --system -e .');
console.log('  2. Test render a single file to verify imports work');
console.log('  3. If successful, we can proceed with content reorganization');
console.log();
