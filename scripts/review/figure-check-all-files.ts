import { getStaleFiles, figureCheckFile, generateFigureForChapter } from './utils';
import { getBookFiles } from '../lib/file-utils';
import dotenv from 'dotenv';
import fs from 'fs-extra';
import path from 'path';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

dotenv.config();

async function main() {
  const argv = await yargs(hideBin(process.argv)).option('generate', {
    alias: 'g',
    type: 'boolean',
    description: 'Generate new figures for chapters that would benefit from them.',
    default: false,
  }).argv;

  if (argv.generate) {
    await generateFigures();
  } else {
    await checkFigures();
  }
}

async function generateFigures() {
  console.log('Starting proactive figure generation for all book files...');
  const bookFiles = await getBookFiles();

  for (const file of bookFiles) {
    console.log(`Analyzing chapter: ${file}`);
    const result = await generateFigureForChapter(file); // Pass file path for context
    let content = await fs.readFile(file, 'utf-8');
    let contentModified = false;

    if (result.action === 'create' && result.filename && result.code && result.insertion_paragraph) {
      const figurePath = path.join('brain/figures', result.filename);
      await fs.writeFile(figurePath, result.code);
      console.log(`✓ Created new figure: ${figurePath}`);
      
      const includeDirective = `\n\n{{< include ${path.relative(path.dirname(file), figurePath).replace(/\\/g, '/')} >}}\n`;
      if (content.includes(result.insertion_paragraph)) {
        content = content.replace(result.insertion_paragraph, `${result.insertion_paragraph}\n${includeDirective}`);
        contentModified = true;
        console.log(`✓ Inserted new figure after paragraph in ${file}.`);
      }

    } else if (result.action === 'include' && result.filename && result.insertion_paragraph) {
      const includeDirective = `\n\n{{< include ${path.relative(path.dirname(file), result.filename).replace(/\\/g, '/')} >}}\n`;
      if (!content.includes(result.filename) && content.includes(result.insertion_paragraph)) {
        content = content.replace(result.insertion_paragraph, `${result.insertion_paragraph}\n${includeDirective}`);
        contentModified = true;
        console.log(`✓ Inserted existing figure after paragraph in ${file}.`);
      }
    } else if (result.action === 'none') {
      console.log(`- No action needed for ${file}.`);
    }

    if (contentModified) {
      await fs.writeFile(file, content);
    }
  }
  console.log('\nFigure generation process complete.');
}

async function checkFigures() {
  console.log('Checking brain/book files for stale figure-checks...');

  const staleFilesToCheck = await getStaleFiles('lastFigureCheckHash', 'brain/book');

  console.log(`\nFound ${staleFilesToCheck.length} stale files in brain/book to figure-check\n`);

  if (staleFilesToCheck.length === 0) {
    console.log('All files in brain/book are up-to-date!');
    return;
  }

  console.log('Figure-checking the following files:');
  staleFilesToCheck.forEach(file => console.log(`  - ${file}`));

  for (const file of staleFilesToCheck) {
    await figureCheckFile(file);
  }

  console.log('\nFigure-checking process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
