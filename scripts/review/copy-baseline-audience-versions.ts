import { getBookFilesForProcessing } from './utils';
import fs from 'fs/promises';
import path from 'path';

/**
 * Creates baseline copies of source files to -foundations and -academic versions
 * WITHOUT applying any transformations. This allows you to:
 * 1. Commit baseline copies to git
 * 2. Run transformation scripts
 * 3. See exact changes in git diff
 */

async function main() {
  console.log('='.repeat(80));
  console.log('COPY BASELINE AUDIENCE VERSIONS');
  console.log('='.repeat(80));
  console.log('\nThis will create -foundations.qmd and -academic.qmd copies');
  console.log('WITHOUT transformations (exact copies for baseline).\n');

  // Get all book files
  const allBookFiles = await getBookFilesForProcessing();

  // Exclude patterns - we only want source files (no existing audience versions)
  const excludedPatterns = [
    /references\.qmd$/,  // Exclude references
    /-foundations\.qmd$/,  // Exclude existing foundation versions
    /-academic\.qmd$/,     // Exclude existing academic versions
  ];

  const excludedFiles = [
    'index.qmd',
  ];

  // Filter to get only source files
  const sourceFiles = allBookFiles.filter(file => {
    // Check exact file matches
    if (excludedFiles.includes(path.basename(file))) return false;

    // Check pattern matches
    if (excludedPatterns.some(pattern => pattern.test(file))) return false;

    return true;
  });

  console.log(`Found ${allBookFiles.length} total book files`);
  console.log(`  - ${allBookFiles.length - sourceFiles.length} excluded (references, existing versions)`);
  console.log(`  - ${sourceFiles.length} source files to copy\n`);

  if (sourceFiles.length === 0) {
    console.log('No source files to process!');
    return;
  }

  // Show files that will be copied
  console.log('Files to copy:');
  sourceFiles.forEach(file => {
    const parsedPath = path.parse(file);
    const foundationsTarget = `${parsedPath.name}-foundations${parsedPath.ext}`;
    const academicTarget = `${parsedPath.name}-academic${parsedPath.ext}`;
    console.log(`  ${path.basename(file)}`);
    console.log(`    → ${foundationsTarget}`);
    console.log(`    → ${academicTarget}`);
  });

  console.log('\nPress Ctrl+C to cancel, or wait 5 seconds to continue...\n');
  await new Promise(resolve => setTimeout(resolve, 5000));

  let successCount = 0;
  let errorCount = 0;

  for (const sourceFile of sourceFiles) {
    try {
      const parsedPath = path.parse(sourceFile);

      // Generate target filenames
      const foundationsTarget = path.join(
        parsedPath.dir,
        `${parsedPath.name}-foundations${parsedPath.ext}`
      );
      const academicTarget = path.join(
        parsedPath.dir,
        `${parsedPath.name}-academic${parsedPath.ext}`
      );

      console.log(`\nCopying: ${path.basename(sourceFile)}`);

      // Copy to foundations version
      await fs.copyFile(sourceFile, foundationsTarget);
      console.log(`  ✓ Created ${path.basename(foundationsTarget)}`);

      // Copy to academic version
      await fs.copyFile(sourceFile, academicTarget);
      console.log(`  ✓ Created ${path.basename(academicTarget)}`);

      successCount++;
    } catch (error) {
      errorCount++;
      console.error(`\n  ❌ ERROR copying ${sourceFile}:`, error);
      console.error('  Continuing with next file...\n');
    }
  }

  console.log('\n' + '='.repeat(80));
  console.log('COPY COMPLETE');
  console.log('='.repeat(80));
  console.log(`Total source files: ${sourceFiles.length}`);
  console.log(`  ✓ Successfully copied: ${successCount} (${successCount * 2} files created)`);
  console.log(`  ✗ Errors: ${errorCount}`);
  console.log('='.repeat(80));
  console.log('\nNext steps:');
  console.log('1. git add . && git commit -m "baseline: copy source files to audience versions"');
  console.log('2. npm run generate:audience:all');
  console.log('3. git diff to see transformations');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
