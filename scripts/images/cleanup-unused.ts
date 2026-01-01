import * as fs from 'fs-extra';
import * as path from 'path';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const ROOT_DIR = path.resolve(__dirname, '..');
const ASSETS_DIR = path.join(ROOT_DIR, 'assets');
const IGNORED_DIRS = ['node_modules', '.git', '.cursor-cache', 'assets'];

// --- Utility Functions ---

async function findFiles(dir: string, ext: string[] | string): Promise<string[]> {
    const extensions = Array.isArray(ext) ? ext.map(e => e.startsWith('.') ? e : `.${e}`) : [ext.startsWith('.') ? ext : `.${ext}`];
    let results: string[] = [];
    const list = await fs.readdir(dir);

    for (const file of list) {
        const filePath = path.join(dir, file);
        const stat = await fs.stat(filePath);
        if (stat && stat.isDirectory()) {
            if (!IGNORED_DIRS.includes(path.basename(filePath))) {
                results = results.concat(await findFiles(filePath, extensions));
            }
        } else {
            if (extensions.includes(path.extname(filePath))) {
                results.push(filePath);
            }
        }
    }
    return results;
}

// --- Main Logic ---

async function main() {
    const argv = await yargs(hideBin(process.argv))
        .option('delete', {
            type: 'boolean',
            description: 'Actually delete the unreferenced files. Defaults to a dry run.',
            default: false,
        })
        .help()
        .argv;
        
    const isDryRun = !argv.delete;

    if (isDryRun) {
        console.log('--- DRY RUN ---');
        console.log('No files will be deleted. Use --delete to apply changes.');
    } else {
        console.log('--- EXECUTION RUN ---');
        console.log('Deleting unreferenced images.');
    }

    // 1. Find all image files
    const imageExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'];
    const allImageFiles = await findFiles(ASSETS_DIR, imageExtensions);
    console.log(`Found ${allImageFiles.length} total image files in assets.`);

    // 2. Find all markdown files and read their content
    const markdownFiles = await findFiles(ROOT_DIR, '.md');
    let allMarkdownContent = '';
    for (const file of markdownFiles) {
        allMarkdownContent += await fs.readFile(file, 'utf-8');
    }
    console.log(`Scanning ${markdownFiles.length} markdown files for references...`);
    
    // 3. Check for references and delete if necessary
    const unreferencedImages: string[] = [];
    for (const imagePath of allImageFiles) {
        const imageName = path.basename(imagePath);
        // Use a simple string search for efficiency. A regex could be more precise but is slower.
        if (!allMarkdownContent.includes(imageName)) {
            unreferencedImages.push(imagePath);
        }
    }

    if (unreferencedImages.length === 0) {
        console.log('\n✅ No unreferenced images found. Everything is clean!');
        return;
    }

    console.log(`\nFound ${unreferencedImages.length} unreferenced images:`);
    unreferencedImages.forEach(img => console.log(`  - ${path.relative(ROOT_DIR, img)}`));
    
    if (!isDryRun) {
        let deleteCount = 0;
        for(const imagePath of unreferencedImages) {
            try {
                await fs.remove(imagePath);
                deleteCount++;
            } catch (error) {
                console.error(`  -> ERROR deleting ${path.relative(ROOT_DIR, imagePath)}:`, error);
            }
        }
        console.log(`\n✅ Successfully deleted ${deleteCount} files.`);
    } else {
        console.log('\n--- End of DRY RUN ---');
    }
}


main().catch(error => {
    console.error('A fatal error occurred:', error);
    process.exit(1);
});
