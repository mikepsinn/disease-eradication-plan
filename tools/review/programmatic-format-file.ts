import * as fs from 'fs';
import * as path from 'path';
import { saveFile } from '../lib/file-utils';

async function formatFile() {
    const filePath = process.argv[2];
    if (!filePath) {
        console.error('Please provide a file path as an argument.');
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
        await saveFile(fullPath, fileContent);

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
