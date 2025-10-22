import * as fs from 'fs';
import * as path from 'path';
import { programmaticFormat } from '../lib/file-utils';

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

    let fileContent = fs.readFileSync(fullPath, 'utf-8');
    
    try {
        const formattedContent = programmaticFormat(fileContent);
        
        if (fileContent !== formattedContent) {
            fs.writeFileSync(fullPath, formattedContent, 'utf-8');
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
