import { glob } from 'glob';
import * as fs from 'fs';
import * as path from 'path';
import MarkdownIt from 'markdown-it';
import { compareTwoStrings } from 'string-similarity';

interface DuplicateResult {
    file1: string;
    file2: string;
    similarity: number;
    snippet1: string;
    snippet2: string;
}

const SIMILARITY_THRESHOLD = 0.8; // Adjust this value (0-1) to control sensitivity
const CHUNK_SIZE = 500; // Number of characters to compare at a time

async function findDuplicateContent(directory: string): Promise<DuplicateResult[]> {
    // Find all markdown files
    const files = await glob('**/*.md', { 
        ignore: ['node_modules/**', 'dist/**'],
        cwd: directory 
    });

    const md = new MarkdownIt();
    const results: DuplicateResult[] = [];

    // Read and process each file
    const fileContents = files.map(file => ({
        path: file,
        content: fs.readFileSync(path.join(directory, file), 'utf-8')
    }));

    // Compare files pairwise
    for (let i = 0; i < fileContents.length; i++) {
        for (let j = i + 1; j < fileContents.length; j++) {
            const file1 = fileContents[i];
            const file2 = fileContents[j];

            // Convert markdown to plain text
            const text1 = md.render(file1.content).replace(/<[^>]*>/g, '');
            const text2 = md.render(file2.content).replace(/<[^>]*>/g, '');

            // Compare chunks of text
            for (let start1 = 0; start1 < text1.length; start1 += CHUNK_SIZE) {
                const chunk1 = text1.slice(start1, start1 + CHUNK_SIZE);
                
                for (let start2 = 0; start2 < text2.length; start2 += CHUNK_SIZE) {
                    const chunk2 = text2.slice(start2, start2 + CHUNK_SIZE);
                    const similarity = compareTwoStrings(chunk1, chunk2);

                    if (similarity > SIMILARITY_THRESHOLD) {
                        results.push({
                            file1: file1.path,
                            file2: file2.path,
                            similarity,
                            snippet1: chunk1.slice(0, 100) + '...',
                            snippet2: chunk2.slice(0, 100) + '...'
                        });
                    }
                }
            }
        }
    }

    return results;
}

// Main execution
async function main() {
    try {
        const results = await findDuplicateContent(process.cwd());
        
        if (results.length === 0) {
            console.log('No significant duplicate content found.');
            return;
        }

        console.log('Found potential duplicate content:\n');
        results.forEach((result, index) => {
            console.log(`Match ${index + 1}:`);
            console.log(`Files: ${result.file1} <-> ${result.file2}`);
            console.log(`Similarity: ${(result.similarity * 100).toFixed(1)}%`);
            console.log('\nSnippet from file 1:');
            console.log(result.snippet1);
            console.log('\nSnippet from file 2:');
            console.log(result.snippet2);
            console.log('\n-------------------\n');
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

main(); 