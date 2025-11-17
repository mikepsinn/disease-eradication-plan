import { findFiles } from './lib/file-utils';

async function main() {
    console.log('Searching for CSV files...');
    const csvFiles = await findFiles('**/*.csv');
    
    if (csvFiles.length > 0) {
        console.log('Found the following CSV files:');
        csvFiles.forEach(file => console.log(file));
    } else {
        console.log('No CSV files found in the project.');
    }
}

main().catch(error => console.error('An error occurred:', error));
