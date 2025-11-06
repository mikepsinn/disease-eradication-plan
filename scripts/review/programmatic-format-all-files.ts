import * as fs from 'fs';
import * as path from 'path';
import { glob } from 'glob';
import { programmaticFormat, findBookFiles } from '../lib/file-utils';

const ROOT_DIR = process.cwd();

async function formatAllFiles(allQmdFiles: boolean = false) {
    let allFiles: string[];

    if (allQmdFiles) {
        console.log('Starting programmatic formatting process for all .qmd files...');
        // Find all .qmd files, excluding build directories
        allFiles = await glob('**/*.qmd', {
            cwd: ROOT_DIR,
            nodir: true,
            absolute: true,
            ignore: ['node_modules/**', '_book/**', '.quarto/**']
        });
    } else {
        console.log('Starting programmatic formatting process for brain/book/**/*.qmd...');
        allFiles = await findBookFiles();
    }

    console.log(`Found ${allFiles.length} files to process\n`);
    let fixedFileCount = 0;

    for (const filePath of allFiles) {
        let fileContent = fs.readFileSync(filePath, 'utf-8');

        try {
            const formattedContent = programmaticFormat(fileContent);

            if (fileContent !== formattedContent) {
                fs.writeFileSync(filePath, formattedContent, 'utf-8');
                console.log(`✅ [Fixed] Formatted ${path.relative(ROOT_DIR, filePath)}`);
                fixedFileCount++;
            }
        } catch (e: any) {
            console.error(`❌ [Error] Could not process ${path.relative(ROOT_DIR, filePath)}: ${e.message}`);
        }
    }

    if (fixedFileCount > 0) {
        console.log(`\nSuccessfully fixed ${fixedFileCount} files.`);
    } else {
        console.log('\nNo files needed fixing.');
    }
}

async function main() {
    const args = process.argv.slice(2);
    const allFiles = args.includes('--all');

    if (args.includes('--help') || args.includes('-h')) {
        console.log(`
Programmatic Formatter for .qmd files

Usage: tsx scripts/review/programmatic-format-all-files.ts [options]

Options:
  --all        Format all .qmd files in the project (default: brain/book only)
  --help, -h   Show this help message

The formatter performs:
  - Em-dash replacement with comma-space
  - Removal of dividers before headings
  - Bold text to heading conversion (6 words or less)
  - Spacing normalization
  - Blank line enforcement after headings
`);
        process.exit(0);
    }

    await formatAllFiles(allFiles);
}

main().catch(error => {
    console.error('Script failed:', error);
    process.exit(1);
});
