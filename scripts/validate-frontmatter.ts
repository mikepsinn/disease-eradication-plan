import * as fs from 'fs';
import * as path from 'path';
import matter from 'gray-matter';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import * as yaml from 'js-yaml';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const IGNORE_PATTERNS = ['.git', '.cursor', 'node_modules', 'scripts', 'brand', '.venv', '_book'];

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
        let fileContent = await fs.promises.readFile(filePath, 'utf-8');
        
        try {
            if (fix) {
                let needsRewrite = false;
                const reasons: string[] = [];

                const { data, content, matter: rawFrontmatter } = matter(fileContent);

                // Fix 1: Quote titles with colons if they aren't already quoted
                if (data.title && typeof data.title === 'string' && data.title.includes(':')) {
                    const isQuoted = (data.title.startsWith('"') && data.title.endsWith('"')) || (data.title.startsWith("'") && data.title.endsWith("'"));
                    if (!isQuoted) {
                        data.title = `"${data.title}"`;
                        needsRewrite = true;
                        reasons.push('Quoted title with colon');
                    }
                }

                // Fix 2: Standardize tags format
                if (data.tags) {
                    let tagsModified = false;
                    if (typeof data.tags === 'string') {
                        // Handles tags: >- ... format by splitting into an array
                        data.tags = data.tags.split(/[, \n]+/).filter(Boolean).map(t => t.trim());
                        tagsModified = true;
                    }

                    if (Array.isArray(data.tags)) {
                        // Check raw string to see if it's block-style `tags:\n  - item`
                        const rawFrontmatterLine = rawFrontmatter.split('\n').find(line => line.trim().startsWith('tags:'));
                        // If it's not a single line array (flow style), it needs fixing.
                        if (tagsModified || (rawFrontmatterLine && !rawFrontmatterLine.includes('['))) {
                            needsRewrite = true;
                            reasons.push(tagsModified ? 'Converted string tags to array' : 'Formatted tags to single-line');
                        }
                    }
                }

                if (needsRewrite) {
                    const newContent = matter.stringify(content, data, {
                        language: 'yaml',
                        flowLevel: 1,
                        styles: {
                          '!!str': 'double'
                        }
                    } as any);
                    await fs.promises.writeFile(filePath, newContent, 'utf-8');
                    console.log(`✅ [Fixed] ${reasons.join(', ')} in ${filePath}`);
                    fileContent = newContent; // Use updated content for validation
                }
            }

            const { data: frontmatter } = matter(fileContent);

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

        } catch (e: any) {
            // Provide more detailed error logging for YAML parsing issues
            if (e.name === 'YAMLException') {
                console.error(`❌ [Invalid YAML] ${filePath}: ${e.reason} at line ${e.mark.line}, column ${e.mark.column}`);
            } else {
                console.error(`❌ [Error] ${filePath}: ${e.message}`);
            }
            errorCount++;
        }
    }

    if (errorCount === 0) {
        console.log('✅ All frontmatter is valid!');
    } else {
        console.log(`\nFound ${errorCount} errors in frontmatter.`);
        process.exit(1);
    }
}

async function main() {
    const argv = await yargs(hideBin(process.argv))
        .option('fix', {
            alias: 'f',
            type: 'boolean',
            description: 'Automatically fix common frontmatter errors.',
            default: false,
        })
        .help()
        .argv;

    await validateFrontmatter(argv.fix);
}

main().catch(error => {
    console.error('Script failed:', error);
    process.exit(1);
});
