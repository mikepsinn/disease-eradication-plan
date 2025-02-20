const fs = require('fs').promises;
const path = require('path');

async function findMarkdownFiles(dir) {
    const files = await fs.readdir(dir);
    let markdownFiles = [];

    for (const file of files) {
        const filePath = path.join(dir, file);
        const stat = await fs.stat(filePath);

        if (stat.isDirectory() && !file.startsWith('.') && file !== 'node_modules') {
            // Recursively search directories, excluding hidden folders and node_modules
            markdownFiles = markdownFiles.concat(await findMarkdownFiles(filePath));
        } else if (file.endsWith('.md')) {
            markdownFiles.push(filePath);
        }
    }

    return markdownFiles;
}

async function mergeMarkdownFiles() {
    try {
        const rootDir = path.resolve(__dirname, '..');
        const markdownFiles = await findMarkdownFiles(rootDir);
        let mergedContent = '# Merged Markdown Content\n\n';

        for (const file of markdownFiles) {
            const content = await fs.readFile(file, 'utf8');
            const relativePath = path.relative(rootDir, file);
            mergedContent += `\n## File: ${relativePath}\n\n${content}\n\n---\n\n`;
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