import * as fs from 'fs/promises';
import * as path from 'path';

async function findMarkdownFiles(dir: string): Promise<string[]> {
    const files = await fs.readdir(dir);
    let markdownFiles: string[] = [];

    for (const file of files) {
        const filePath = path.join(dir, file);
        try {
            const stat = await fs.stat(filePath);

            if (stat.isDirectory() && !file.startsWith('.') && file !== 'node_modules') {
                // Recursively search directories, excluding hidden folders and node_modules
                markdownFiles = markdownFiles.concat(await findMarkdownFiles(filePath));
            } else if (file.endsWith('.md')) {
                markdownFiles.push(filePath);
            }
        } catch (error) {
            // Handle potential errors like permission denied or file not found during stat
            console.error(`Error stating file ${filePath}:`, error);
        }
    }

    return markdownFiles;
}

async function mergeMarkdownFiles(): Promise<void> {
    try {
        const rootDir = path.resolve(__dirname, '..');
        const markdownFiles = await findMarkdownFiles(rootDir);
        let mergedContent = '# Merged Markdown Content\n\n';

        for (const file of markdownFiles) {
            try {
                const content = await fs.readFile(file, 'utf8');
                const relativePath = path.relative(rootDir, file);
                mergedContent += `\n## File: ${relativePath}\n\n${content}\n\n---\n\n`;
            } catch (error) {
                console.error(`Error reading file ${file}:`, error);
            }
        }

        const outputPath = path.join(rootDir, 'merged-content.md');
        await fs.writeFile(outputPath, mergedContent);
        console.log(`Successfully merged ${markdownFiles.length} markdown files into merged-content.md`);
        console.log('Merged files:', markdownFiles.map(f => path.relative(rootDir, f)).join('\n'));
    } catch (error) {
        console.error('Error merging markdown files:', error);
    }
}

mergeMarkdownFiles(); 