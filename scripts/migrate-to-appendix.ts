import fs from 'fs/promises';
import path from 'path';
import { glob } from 'glob';

interface FileMove {
  from: string;
  to: string;
  reason: string;
}

// Function to check if a file is in _book.yml
async function isInQuartoYml(filePath: string): Promise<boolean> {
  const quartoContent = await fs.readFile('_book.yml', 'utf-8');
  return quartoContent.includes(filePath);
}

// Function to find all orphaned .qmd files
async function findOrphanedFiles(): Promise<FileMove[]> {
  const moves: FileMove[] = [];

  // Find all .qmd files in brain/book (excluding appendix folder)
  const allFiles = await glob('brain/book/**/*.qmd', {
    ignore: ['brain/book/appendix/**']
  });

  console.log(`Found ${allFiles.length} total .qmd files in brain/book\n`);

  for (const file of allFiles) {
    const normalizedPath = file.replace(/\\/g, '/');
    const isInYml = await isInQuartoYml(normalizedPath);

    if (!isInYml) {
      const basename = path.basename(file);
      const folder = path.dirname(file).split(path.sep).pop() || '';

      // Determine the new name based on the original folder
      let newName = basename;
      let reason = 'Orphaned file not in _book.yml';

      // Special naming for certain folders
      if (folder === 'reference') {
        reason = 'Reference material';
      } else if (folder === 'economics') {
        reason = 'Technical economic analysis';
      } else if (folder === 'strategy') {
        reason = 'Detailed strategy document';
      } else if (folder === 'legal') {
        reason = 'Legal/compliance details';
      } else if (folder === 'governance') {
        reason = 'Governance structure details';
      }

      moves.push({
        from: normalizedPath,
        to: `brain/book/appendix/${basename}`,
        reason
      });
    }
  }

  // Also check for files that are in _book.yml but in wrong sections
  // (e.g., reference files listed in main chapters)
  const quartoContent = await fs.readFile('_book.yml', 'utf-8');

  // Find reference files that are in the chapters section (not appendices)
  const chapterSection = quartoContent.split('appendices:')[0];
  const refFilesInChapters = chapterSection.match(/brain\/book\/reference\/[^\s]+\.qmd/g) || [];

  for (const refFile of refFilesInChapters) {
    // Check if this file actually exists
    try {
      await fs.access(refFile);
      moves.push({
        from: refFile,
        to: `brain/book/appendix/${path.basename(refFile)}`,
        reason: 'Reference file incorrectly in chapters section'
      });
    } catch {
      // File doesn't exist, skip it
    }
  }

  return moves;
}

// Function to update all references to moved files
async function updateReferences(oldPath: string, newPath: string): Promise<number> {
  // Find all .qmd, .md, and .yml files
  const files = await glob('**/*.{qmd,md,yml}', {
    ignore: ['node_modules/**', '.git/**', '_site/**', '.quarto/**']
  });

  let updatedCount = 0;

  for (const file of files) {
    try {
      let content = await fs.readFile(file, 'utf-8');
      let originalContent = content;

      // Normalize paths for comparison
      const oldPathNormalized = oldPath.replace(/\\/g, '/');
      const newPathNormalized = newPath.replace(/\\/g, '/');
      const oldBasename = path.basename(oldPath);

      // Create regex patterns for different reference formats
      const patterns = [
        // Direct references to the file
        new RegExp(`\\b${oldPathNormalized}\\b`, 'g'),
        // Relative references starting with ../
        new RegExp(`\\.\\./(\\.\\./)*(${oldPathNormalized})`, 'g'),
        // References in markdown links
        new RegExp(`\\]\\([^)]*${oldBasename}[^)]*\\)`, 'g'),
        // References in includes
        new RegExp(`include\\s+[^\\s]*${oldBasename}`, 'g'),
      ];

      let wasUpdated = false;

      for (const pattern of patterns) {
        if (pattern.test(content)) {
          wasUpdated = true;
          content = content.replace(pattern, (match) => {
            // Calculate relative path from current file to new location
            const fileDir = path.dirname(file);
            const relativePath = path.relative(fileDir, newPathNormalized).replace(/\\/g, '/');

            // Preserve the format of the reference
            if (match.includes('](')) {
              // Markdown link - extract the part before the path and after
              const beforePath = match.substring(0, match.indexOf('(') + 1);
              const afterPath = match.includes('#') ? match.substring(match.indexOf('#')) : ')';
              return `${beforePath}${relativePath}${afterPath}`;
            } else if (match.includes('include')) {
              return `include ${relativePath}`;
            } else if (match.includes('../')) {
              // Relative path reference
              return relativePath;
            } else {
              // Direct path reference
              return newPathNormalized;
            }
          });
        }
      }

      if (wasUpdated && content !== originalContent) {
        await fs.writeFile(file, content, 'utf-8');
        updatedCount++;
        console.log(`    ✓ Updated references in ${file}`);
      }
    } catch (error) {
      console.error(`    ✗ Error processing ${file}:`, error);
    }
  }

  return updatedCount;
}

// Function to update _book.yml
async function updateQuartoYml(moves: FileMove[]) {
  const quartoPath = '_book.yml';
  let content = await fs.readFile(quartoPath, 'utf-8');

  // Track which files we're adding to appendices
  const appendixFiles: string[] = [];

  for (const move of moves) {
    // Comment out or remove from chapters section
    const patterns = [
      new RegExp(`(\\s+)- ${move.from}([^\\n]*)`, 'g'),
      new RegExp(`(\\s+)- ${move.from.replace(/\\/g, '/')}([^\\n]*)`, 'g')
    ];

    for (const pattern of patterns) {
      if (pattern.test(content)) {
        content = content.replace(pattern, `$1# - ${move.from} # MOVED TO APPENDIX$2`);
      }
    }

    appendixFiles.push(move.to);
  }

  // Find the appendices section and add new files
  const appendixMatch = content.match(/(\s*)appendices:\s*\n/);
  if (appendixMatch) {
    const indent = appendixMatch[1] || '';
    const appendixIndex = content.indexOf(appendixMatch[0]) + appendixMatch[0].length;

    // Build the new entries
    let newEntries = '';
    for (const file of appendixFiles) {
      newEntries += `${indent}    - ${file.replace(/\\/g, '/')}\n`;
    }

    // Insert after the appendices: line
    content = content.slice(0, appendixIndex) + newEntries + content.slice(appendixIndex);
  } else {
    // No appendices section exists, create one
    content += '\n\n  appendices:\n';
    for (const file of appendixFiles) {
      content += `    - ${file.replace(/\\/g, '/')}\n`;
    }
  }

  await fs.writeFile(quartoPath, content, 'utf-8');
  console.log('\n✓ Updated _book.yml');
}

async function main() {
  console.log('🔍 Scanning for orphaned files not in _book.yml...\n');

  // Find all orphaned files
  const filesToMove = await findOrphanedFiles();

  if (filesToMove.length === 0) {
    console.log('✅ No orphaned files found! All files are properly referenced in _book.yml');
    return;
  }

  console.log(`Found ${filesToMove.length} files to move to appendix:\n`);

  // Group by folder for better display
  const byFolder: Record<string, FileMove[]> = {};
  for (const move of filesToMove) {
    const folder = path.dirname(move.from).split('/').pop() || 'root';
    if (!byFolder[folder]) byFolder[folder] = [];
    byFolder[folder].push(move);
  }

  // Display files to be moved
  for (const [folder, moves] of Object.entries(byFolder)) {
    console.log(`\n📁 ${folder}/`);
    for (const move of moves) {
      console.log(`  - ${path.basename(move.from)} (${move.reason})`);
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('Starting migration...\n');

  // Create appendix directory if it doesn't exist
  await fs.mkdir('brain/book/appendix', { recursive: true });
  console.log('✓ Created brain/book/appendix folder\n');

  let totalRefsUpdated = 0;

  // Process each file move
  for (const move of filesToMove) {
    console.log(`\n📄 Moving: ${move.from}`);
    console.log(`   → To: ${move.to}`);
    console.log(`   Reason: ${move.reason}`);

    try {
      // Check if source file exists
      try {
        await fs.access(move.from);
      } catch {
        console.log(`  ⚠ Source file doesn't exist, skipping...`);
        continue;
      }

      // Read the file content
      const content = await fs.readFile(move.from, 'utf-8');

      // Write to new location
      await fs.writeFile(move.to, content, 'utf-8');
      console.log(`  ✓ File copied to appendix`);

      // Update all references
      const updatedRefs = await updateReferences(move.from, move.to);
      totalRefsUpdated += updatedRefs;
      if (updatedRefs > 0) {
        console.log(`  ✓ Updated ${updatedRefs} file references`);
      }

      // Delete original file
      await fs.unlink(move.from);
      console.log(`  ✓ Deleted original file`);

    } catch (error) {
      console.error(`  ✗ Error moving file:`, error);
    }
  }

  // Update _book.yml
  console.log('\n' + '='.repeat(60));
  console.log('Updating _book.yml...');
  await updateQuartoYml(filesToMove);

  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('✅ Migration complete!\n');
  console.log(`Summary:`);
  console.log(`  - Moved ${filesToMove.length} files to appendix`);
  console.log(`  - Updated ${totalRefsUpdated} file references`);
  console.log(`  - Updated _book.yml\n`);

  console.log('Next steps:');
  console.log('1. Run "git status" to review all changes');
  console.log('2. Review _book.yml and clean up commented entries');
  console.log('3. Test that the book still builds correctly');
  console.log('4. Commit the changes');
}

main().catch(console.error);