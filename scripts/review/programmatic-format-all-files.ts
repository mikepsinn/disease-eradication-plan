import * as fs from 'fs';
import * as path from 'path';
import { programmaticFormat, findBookFiles } from '../lib/file-utils';

const ROOT_DIR = process.cwd();

async function formatAllFiles() {
    console.log('Starting programmatic formatting process for brain/book/**/*.qmd...');
    const allFiles = await findBookFiles();
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
    await formatAllFiles();
}

main().catch(error => {
    console.error('Script failed:', error);
    process.exit(1);
});
