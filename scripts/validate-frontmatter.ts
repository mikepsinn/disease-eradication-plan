import * as fs from 'fs';
import * as path from 'path';
import matter from 'gray-matter';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const ROOT_DIR = path.resolve(__dirname, '..');
const IGNORE_PATTERNS = ['.git', '.cursor', 'node_modules', 'scripts', 'brand', 'operations'];

async function findMarkdownFiles(dir: string): Promise<string[]> {
    let mdFiles: string[] = [];
    const entries = await fs.promises.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (IGNORE_PATTERNS.some(p => fullPath.includes(path.sep + p))) continue;
        if (entry.isDirectory()) {
            mdFiles = mdFiles.concat(await findMarkdownFiles(fullPath));
        } else if (entry.isFile() && (entry.name.endsWith('.md') || entry.name.endsWith('.mdc'))) {
            mdFiles.push(fullPath);
        }
    }
    return mdFiles;
}

async function validateFrontmatter(fix: boolean) {
    console.log('Starting frontmatter validation...');
    const allFiles = await findMarkdownFiles(ROOT_DIR);
    let errorCount = 0;

    for (const filePath of allFiles) {
        const fileContent = await fs.promises.readFile(filePath, 'utf-8');
        
        try {
            const { data: frontmatter, content } = matter(fileContent);

            // Rule 1: Must have a title
            if (!frontmatter.title) {
                console.error(`❌ [Missing Title] ${filePath}`);
                errorCount++;
            }

            // Rule 2: Must have a description
            if (!frontmatter.description) {
                console.error(`❌ [Missing Description] ${filePath}`);
                errorCount++;
            } else if (frontmatter.description.length > 140) {
                // Rule 3: Description must be <= 140 chars
                console.error(`❌ [Description Too Long] ${filePath} (${frontmatter.description.length} chars)`);
                errorCount++;
            }

            // Auto-fix: Quote titles with colons
            if (fix && frontmatter.title && frontmatter.title.includes(':') && !frontmatter.title.startsWith('"')) {
                const newContent = `---
${yaml.dump({ ...frontmatter, title: `"${frontmatter.title}"` })}---
${content}`;
                await fs.promises.writeFile(filePath, newContent);
                console.log(`✅ [Fixed Title] Quoted title in ${filePath}`);
            }

        } catch (e: any) {
            console.error(`❌ [Invalid YAML] ${filePath}: ${e.message}`);
            errorCount++;
        }
    }

    if (errorCount === 0) {
        console.log('\n✅ All files passed frontmatter validation!');
    } else {
        console.log(`\nFound ${errorCount} errors in frontmatter.`);
        process.exit(1);
    }
}

const argv = yargs(hideBin(process.argv))
    .option('fix', {
        alias: 'f',
        type: 'boolean',
        description: 'Automatically fix common frontmatter errors.',
        default: false,
    })
    .help()
    .argv;

validateFrontmatter(argv.fix).catch(error => {
    console.error('Script failed:', error);
    process.exit(1);
});
