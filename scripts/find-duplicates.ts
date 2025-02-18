import { glob } from 'glob';
import * as fs from 'fs';
import * as path from 'path';
import MarkdownIt from 'markdown-it';
import { compareTwoStrings } from 'string-similarity';
import ignore from 'ignore';

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
    // Load .gitignore patterns
    console.log('📋 Loading .gitignore patterns...');
    const ig = ignore();
    try {
        const gitignoreContent = fs.readFileSync(path.join(directory, '.gitignore'), 'utf-8');
        ig.add(gitignoreContent);
    } catch (error) {
        console.log('⚠️  No .gitignore found, proceeding without it');
    }

    console.log('🔍 Scanning for markdown files...');
    const allFiles = await glob('**/*.md', { 
        ignore: ['node_modules/**', 'dist/**'],
        cwd: directory 
    });

    // Filter files using .gitignore rules
    const files = allFiles.filter(file => !ig.ignores(file));
    console.log(`📑 Found ${files.length} markdown files (${allFiles.length - files.length} ignored)\n`);

    const md = new MarkdownIt();
    const results: DuplicateResult[] = [];

    console.log('📖 Reading file contents...');
    const fileContents = files.map(file => {
        process.stdout.write(`  Reading ${file}...\r`);
        return {
            path: file,
            content: fs.readFileSync(path.join(directory, file), 'utf-8')
        };
    });
    console.log('\n✅ Finished reading files\n');

    const totalComparisons = (fileContents.length * (fileContents.length - 1)) / 2;
    let comparisonsDone = 0;

    // Compare files pairwise
    for (let i = 0; i < fileContents.length; i++) {
        for (let j = i + 1; j < fileContents.length; j++) {
            comparisonsDone++;
            const progress = ((comparisonsDone / totalComparisons) * 100).toFixed(1);
            process.stdout.write(`🔄 Comparing files: ${progress}% (${comparisonsDone}/${totalComparisons})\r`);

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
    console.log('\n✅ Finished comparing files\n');

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