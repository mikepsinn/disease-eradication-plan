#!/usr/bin/env ts-node
/**
 * Fix paths in _quarto.yml to use new knowledge/ structure
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '../..');
const QUARTO_YML = path.join(PROJECT_ROOT, '_quarto.yml');

function fixQuartoConfig() {
  console.log('Fixing _quarto.yml paths...\n');

  let content = fs.readFileSync(QUARTO_YML, 'utf-8');
  let changeCount = 0;

  // Define path replacements
  const replacements = [
    // brain/book/* → knowledge/*
    { from: /brain\/book\//g, to: 'knowledge/', description: 'brain/book/ → knowledge/' },

    // dih-economic-models/* → knowledge/*
    { from: /dih-economic-models\/economics\//g, to: 'knowledge/economics/', description: 'dih-economic-models/economics/ → knowledge/economics/' },
    { from: /dih-economic-models\/appendix\//g, to: 'knowledge/appendix/', description: 'dih-economic-models/appendix/ → knowledge/appendix/' },
    { from: /dih-economic-models\/references\.qmd/g, to: 'knowledge/references.qmd', description: 'dih-economic-models/references.qmd → knowledge/references.qmd' },
  ];

  // Apply each replacement
  for (const { from, to, description } of replacements) {
    const before = content;
    content = content.replace(from, to);
    const matches = (before.match(from) || []).length;
    if (matches > 0) {
      console.log(`✓ ${description} (${matches} replacements)`);
      changeCount += matches;
    }
  }

  // Write the updated content
  fs.writeFileSync(QUARTO_YML, content, 'utf-8');

  console.log(`\n✓ Fixed ${changeCount} paths in _quarto.yml`);
}

fixQuartoConfig();
