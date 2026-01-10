import * as fs from 'fs';
import * as path from 'path';
import { saveFile, ProgrammaticFormatOptions } from '../lib/file-utils';

function parseArgs(): { filePath: string; options: ProgrammaticFormatOptions } {
    const args = process.argv.slice(2);
    let filePath = '';
    const options: ProgrammaticFormatOptions = {
        addIncludeDirective: false,
        removeFirstHeading: false,
    };

    for (const arg of args) {
        if (arg === '--add-include') {
            options.addIncludeDirective = true;
        } else if (arg === '--remove-heading') {
            options.removeFirstHeading = true;
        } else if (!arg.startsWith('--')) {
            filePath = arg;
        }
    }

    return { filePath, options };
}

async function formatFile() {
    const { filePath, options } = parseArgs();
    
    if (!filePath) {
        console.error('Usage: npx tsx scripts/review/programmatic-format-file.ts <file-path> [--add-include] [--remove-heading]');
        console.error('  --add-include    Add the setup-parameters include directive at the start');
        console.error('  --remove-heading Remove the first heading after the include directive');
        process.exit(1);
    }

    const fullPath = path.resolve(filePath);
    if (!fs.existsSync(fullPath)) {
        console.error(`Error: File not found at ${fullPath}`);
        process.exit(1);
    }

    // Exclude references.qmd from formatting
    if (path.basename(fullPath) === 'references.qmd') {
        console.log('Skipping references.qmd (excluded from formatting)');
        process.exit(0);
    }

    let fileContent = fs.readFileSync(fullPath, 'utf-8');
    
    try {
        // Save original content for comparison
        const originalContent = fileContent;

        // saveFile will apply formatting internally, so just call it
        await saveFile(fullPath, fileContent, options);

        // Read back to check if it changed
        const newContent = fs.readFileSync(fullPath, 'utf-8');
        if (originalContent !== newContent) {
            console.log(`✅ [Fixed] Formatted ${filePath}`);
        } else {
            console.log('No changes needed for the file.');
        }
    } catch (e: any) {
        console.error(`❌ [Error] Could not process ${filePath}: ${e.message}`);
    }
}

async function main() {
    await formatFile();
}

main().catch(error => {
    console.error('Script failed:', error);
    process.exit(1);
});
