import * as fs from 'fs';
import * as path from 'path';
import matter from 'gray-matter';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import { glob } from 'glob';

const ROOT_DIR = process.cwd();
const IGNORE_PATTERNS = ['.git', '.cursor', 'node_modules', 'scripts', 'brand', '.venv', '_book'];

async function findMarkdownFiles(dir: string): Promise<string[]> {
    const pattern = '**/*.{md,qmd,mdc}';
    const files = await glob(pattern, {
        cwd: dir,
        ignore: IGNORE_PATTERNS.map(p => `**/${p}/**`),
        nodir: true,
        absolute: true,
    });
    return files;
}

async function fixFrontmatterIssues() {
    console.log('Starting frontmatter fixing process...');
    const allFiles = await findMarkdownFiles(ROOT_DIR);
    let fixedFileCount = 0;

    for (const filePath of allFiles) {
        let fileContent = fs.readFileSync(filePath, 'utf-8');
        let needsRewrite = false;
        const reasons: string[] = [];

        try {
            const { data, content, matter: rawFrontmatter } = matter(fileContent);

            if (!data.title) {
                data.title = 'TODO: Add title';
                needsRewrite = true;
                reasons.push('Added missing title');
            }

            if (!data.description) {
                data.description = 'TODO: Add description';
                needsRewrite = true;
                reasons.push('Added missing description');
            }

            if (data.description && data.description.length > 140) {
                if (!data.tags) {
                    data.tags = [];
                }
                if (typeof data.tags === 'string') {
                    data.tags = data.tags.split(/[, \n]+/).filter(Boolean).map(t => t.trim());
                }
                if (Array.isArray(data.tags) && !data.tags.includes('needs-review')) {
                    data.tags.push('needs-review');
                    needsRewrite = true;
                    reasons.push('Tagged for long description');
                }
            }
            
            if (data.title && typeof data.title === 'string' && (data.title.includes(':') || /[\u{1F300}-\u{1F9FF}]/u.test(data.title))) {
                const isQuoted = (data.title.startsWith('"') && data.title.endsWith('"')) || (data.title.startsWith("'") && data.title.endsWith("'"));
                if (!isQuoted) {
                    data.title = `"${data.title.replace(/"/g, '\\"')}"`;
                    needsRewrite = true;
                    reasons.push('Quoted title with colon or emoji');
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
                fs.writeFileSync(filePath, newContent, 'utf-8');
                console.log(`✅ [Fixed] ${reasons.join(', ')} in ${path.relative(ROOT_DIR, filePath)}`);
                fixedFileCount++;
            }
        } catch (e: any) {
            if (e.name === 'YAMLException' && fileContent.trim() !== '') {
                const newContent = matter.stringify(fileContent, {
                    title: 'TODO: Add title',
                    description: 'TODO: Add description'
                });
                fs.writeFileSync(filePath, newContent, 'utf-8');
                console.log(`✅ [Fixed] Added missing frontmatter to ${path.relative(ROOT_DIR, filePath)}`);
                fixedFileCount++;
            } else if (fileContent.trim() === '') {
                console.log(`- [Skipped] Empty file: ${path.relative(ROOT_DIR, filePath)}`);
            } else {
                console.error(`❌ [Error] Could not process ${path.relative(ROOT_DIR, filePath)}: ${e.message}`);
            }
        }
    }

    if (fixedFileCount > 0) {
        console.log(`\nSuccessfully fixed ${fixedFileCount} files.`);
    } else {
        console.log('\nNo files needed fixing.');
    }
}

async function main() {
    await fixFrontmatterIssues();
}

main().catch(error => {
    console.error('Script failed:', error);
    process.exit(1);
});
