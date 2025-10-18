import fs from 'fs';
import path from 'path';
import { glob } from 'glob';

const projectRoot = process.cwd();
const figuresDir = path.join(projectRoot, 'brain', 'figures');

async function findUnusedFigures() {
    console.log('Starting analysis of unused figures...');

    // 1. Get all .qmd files in the figures directory
    const figureFiles = await glob(path.join(figuresDir, '*.qmd').replace(/\\/g, '/'));
    const figureBasenames = figureFiles.map(file => path.basename(file));
    console.log(`Found ${figureBasenames.length} figure files to check.`);

    // 2. Get all .qmd files in the entire project
    const allQmdFiles = await glob(path.join(projectRoot, '**', '*.qmd').replace(/\\/g, '/'), {
        ignore: ['**/node_modules/**', `**/${path.basename(figuresDir)}/**`], // Exclude node_modules and the figures dir itself
    });
    console.log(`Scanning ${allQmdFiles.length} .qmd files for references...`);

    const referencedFigures = new Set<string>();

    // 3. Search for references
    for (const qmdFile of allQmdFiles) {
        const content = fs.readFileSync(qmdFile, 'utf-8');
        for (const figure of figureBasenames) {
            if (content.includes(figure)) {
                referencedFigures.add(figure);
            }
        }
    }

    // 4. Determine unused figures
    const unusedFigures = figureBasenames.filter(figure => !referencedFigures.has(figure));

    console.log('\n--- Analysis Complete ---');
    if (unusedFigures.length > 0) {
        console.log('The following figure files are not referenced in any other .qmd files:');
        unusedFigures.forEach(file => console.log(`- ${file}`));
    } else {
        console.log('All figure files appear to be referenced.');
    }
    console.log('-----------------------\n');
}

findUnusedFigures().catch(err => {
    console.error('An error occurred:', err);
});
