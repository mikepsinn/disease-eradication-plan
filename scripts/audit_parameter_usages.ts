import * as fs from 'fs/promises';
import * as path from 'path';
import { getAllSourceFiles, getProjectRoot } from './lib/file-utils';

interface MatchResult {
    file: string;
    line: number;
    term: string;
    context: string;
}

const ROOT_DIR = getProjectRoot();
const REPORT_FILE = 'parameter_audit_report.md';

async function searchFiles(searchTerms: string[]): Promise<MatchResult[]> {
    console.log(`Searching for terms: ${JSON.stringify(searchTerms)}`);

    // Use file-utils to get all source files (respects gitignore and auto-generated exclusions)
    // We'll search typical source/content extensions
    const files = await getAllSourceFiles(['.qmd', '.md', '.py', '.ts', '.js', '.yml']);

    console.log(`Scanning ${files.length} files...`);

    const results: MatchResult[] = [];

    for (const filePath of files) {
        // Skip this script and the report itself if they happen to be included
        if (filePath.endsWith('audit_parameter_usages.ts') || filePath.endsWith(REPORT_FILE)) {
            continue;
        }

        try {
            const content = await fs.readFile(filePath, 'utf-8');
            const lines = content.split('\n');
            const relativePath = path.relative(ROOT_DIR, filePath).replace(/\\/g, '/');

            lines.forEach((line, index) => {
                for (const term of searchTerms) {
                    if (line.toLowerCase().includes(term.toLowerCase())) {
                        // Capture context (2 lines before and after)
                        const start = Math.max(0, index - 2);
                        const end = Math.min(lines.length, index + 3);
                        let context = lines.slice(start, end).join('\n').trim();

                        // Escape backticks to prevent breaking markdown code blocks in the report
                        context = context.replace(/`/g, "'");

                        results.push({
                            file: relativePath,
                            line: index + 1,
                            term: term,
                            context: context
                        });

                        // Avoid multiple hits per line for the same term (or different terms if desired)
                        // Let's break to avoid duplicate reporting for the same line
                        break;
                    }
                }
            });
        } catch (err) {
            console.error(`Error reading ${filePath}:`, err);
        }
    }

    return results;
}

async function generateReport(results: MatchResult[], searchTerms: string[]) {
    const outputPath = path.join(ROOT_DIR, REPORT_FILE);

    if (results.length === 0) {
        await fs.writeFile(outputPath, `# Parameter Usage Audit Report\n\n**Search Terms:** ${searchTerms.map(t => `\`${t}\``).join(', ')}\n\nNo matches found.\n`);
        console.log(`No matches found. Report generated at: ${outputPath}`);
        return;
    }

    let report = `# Parameter Usage Audit Report\n\n`;
    report += `**Search Terms:** ${searchTerms.map(t => `\`${t}\``).join(', ')}\n\n`;

    // Group by file
    const filesDict: Record<string, MatchResult[]> = {};
    results.forEach(r => {
        if (!filesDict[r.file]) {
            filesDict[r.file] = [];
        }
        filesDict[r.file].push(r);
    });

    const sortedFiles = Object.keys(filesDict).sort();

    for (const file of sortedFiles) {
        report += `## ${file}\n\n`;
        for (const item of filesDict[file]) {
            report += `- **Line ${item.line}** (matched '\`${item.term}\`')\n`;
            report += `  \`\`\`\n  ${item.context}\n  \`\`\`\n`;
            report += `  - [ ] Reviewed\n\n`;
        }
    }

    await fs.writeFile(outputPath, report, 'utf-8');
    console.log(`Found ${results.length} matches. Report generated at: ${outputPath}`);
}

async function main() {
    const args = process.argv.slice(2);
    if (args.length === 0) {
        console.log("Usage: npx tsx scripts/audit_parameter_usages.ts <term1> [term2...]");
        process.exit(1);
    }

    const results = await searchFiles(args);
    await generateReport(results, args);
}

main().catch(err => {
    console.error("Fatal error:", err);
    process.exit(1);
});
