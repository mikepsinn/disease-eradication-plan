import { glob } from 'glob';
import * as path from 'path';
import ignore from 'ignore';
import * as fs from 'fs';
import * as readline from 'readline';

interface DuplicateFile {
    basename: string;
    paths: string[];
}

// Files to exclude from duplicate detection
const EXCLUDED_FILENAMES = new Set(['README.md']);

function createPrompt(): readline.Interface {
    return readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
}

async function confirmDeletion(filesToDelete: string[]): Promise<boolean> {
    const rl = createPrompt();
    
    console.log('\nFiles to be deleted:');
    filesToDelete.forEach(file => console.log(`   🗑️  ${file}`));
    
    return new Promise(resolve => {
        rl.question('\n⚠️  Are you sure you want to delete these files? (y/N): ', answer => {
            rl.close();
            resolve(answer.toLowerCase() === 'y');
        });
    });
}

async function findDuplicateFilenames(directory: string): Promise<DuplicateFile[]> {
    // Load .gitignore patterns
    console.log('📋 Loading .gitignore patterns...');
    const ig = ignore();
    try {
        const gitignoreContent = fs.readFileSync(path.join(directory, '.gitignore'), 'utf-8');
        ig.add(gitignoreContent);
    } catch (error) {
        console.log('⚠️  No .gitignore found, proceeding without it');
    }

    console.log('🔍 Scanning files...');
    const allFiles = await glob('**/*.*', { 
        ignore: ['node_modules/**', 'dist/**'],
        cwd: directory,
        nodir: true
    });

    // Filter files using .gitignore rules and exclude specific filenames
    const files = allFiles.filter(file => {
        const basename = path.basename(file);
        return !ig.ignores(file) && !EXCLUDED_FILENAMES.has(basename);
    });
    
    const excludedCount = allFiles.filter(file => EXCLUDED_FILENAMES.has(path.basename(file))).length;
    console.log(`📑 Found ${files.length} files (${allFiles.length - files.length} ignored, including ${excludedCount} README.md files)\n`);

    // Group files by basename
    const fileGroups = new Map<string, string[]>();
    
    files.forEach(file => {
        const basename = path.basename(file);
        if (!fileGroups.has(basename)) {
            fileGroups.set(basename, []);
        }
        fileGroups.get(basename)!.push(file);
    });

    // Filter for duplicates and sort by basename
    const duplicates: DuplicateFile[] = Array.from(fileGroups.entries())
        .filter(([_, paths]) => paths.length > 1)
        .map(([basename, paths]) => ({ basename, paths }))
        .sort((a, b) => a.basename.localeCompare(b.basename));

    return duplicates;
}

async function main() {
    try {
        const shouldDelete = process.argv.includes('--delete');
        const duplicates = await findDuplicateFilenames(process.cwd());
        
        if (duplicates.length === 0) {
            console.log('No duplicate filenames found.');
            return;
        }

        console.log(`Found ${duplicates.length} duplicate filenames:\n`);
        duplicates.forEach(({ basename, paths }) => {
            // Sort paths by length to identify the longest ones
            const sortedPaths = [...paths].sort((a, b) => a.length - b.length);
            const shortest = sortedPaths[0];
            const toDelete = sortedPaths.slice(1);
            
            console.log(`📄 ${basename}`);
            console.log(`   ✅ ${shortest} (keeping - shortest path)`);
            toDelete.forEach(path => console.log(`   ${shouldDelete ? '🗑️' : '└─'} ${path}${shouldDelete ? ' (will delete - longer path)' : ''}`));
            console.log();
        });

        // Summary statistics
        const totalDuplicates = duplicates.reduce((sum, dup) => sum + dup.paths.length, 0);
        console.log('Summary:');
        console.log(`- Total duplicate filename groups: ${duplicates.length}`);
        console.log(`- Total files involved: ${totalDuplicates}`);
        console.log(`- Average duplicates per name: ${(totalDuplicates / duplicates.length).toFixed(1)}`);

        // Handle deletion if --delete flag is present
        if (shouldDelete) {
            const filesToDelete = duplicates.flatMap(({ paths }) => {
                const sortedPaths = [...paths].sort((a, b) => a.length - b.length);
                return sortedPaths.slice(1); // All but the shortest path
            });

            if (await confirmDeletion(filesToDelete)) {
                console.log('\nDeleting files...');
                for (const file of filesToDelete) {
                    try {
                        fs.unlinkSync(file);
                        console.log(`✅ Deleted: ${file}`);
                    } catch (error) {
                        console.error(`❌ Failed to delete ${file}:`, error);
                    }
                }
                console.log('\nDeletion complete!');
            } else {
                console.log('\nDeletion cancelled.');
            }
        } else {
            console.log('\nTip: Run with --delete flag to remove duplicates with longer paths');
        }

    } catch (error) {
        console.error('Error:', error);
    }
}

main(); 