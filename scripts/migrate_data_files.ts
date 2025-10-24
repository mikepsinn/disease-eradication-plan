import { findFiles } from './lib/file-utils';
import * as fs from 'fs/promises';
import * as path from 'path';

async function main() {
    console.log('Starting data file migration...');
    const dataFiles = await findFiles('assets/**/*.{csv,xls,xlsx}');
    
    for (const file of dataFiles) {
        const newPath = path.join('brain', 'data', path.basename(file));
        
        await fs.rename(file, newPath);
        
        console.log(`Moved ${file} to ${newPath}`);
        
        const oldRef = path.relative(process.cwd(), file).replace(/\\/g, '/');
        const newRef = path.relative(process.cwd(), newPath).replace(/\\/g, '/');
        
        const allFiles = await findFiles('**/*');
        
        for (const filePath of allFiles) {
            try {
                let content = await fs.readFile(filePath, 'utf-8');
                if (content.includes(oldRef)) {
                    content = content.replace(new RegExp(oldRef, 'g'), newRef);
                    await fs.writeFile(filePath, content, 'utf-8');
                    console.log(`Updated reference in ${filePath}`);
                }
            } catch (error) {
                console.error(`Could not process file ${filePath}:`, error);
            }
        }
    }
    
    console.log('Data file migration complete.');
}

main().catch(error => console.error('An error occurred:', error));
