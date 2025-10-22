import { formatFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
    const filePath = process.argv[2];
    if (!filePath) {
        console.error('Please provide a file path as an argument.');
        process.exit(1);
    }

    await formatFileWithLLM(filePath);
}

main().catch(err => {
    console.error('An unexpected error occurred:', err);
    process.exit(1);
});
