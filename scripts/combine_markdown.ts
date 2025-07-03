import * as fs from 'fs';
import * as path from 'path';
import matter from 'gray-matter';
import * as yaml from 'js-yaml'; // Added for type definition in stringify engine

// Configuration
const OUTPUT_FILE = 'combined_wiki.md';
const IGNORE_DIRS = ['.git', '.github', 'node_modules', '.obsidian', '.vscode'];
const IGNORE_FILES = ['combined_wiki.md'];

// Helper function to get all markdown files recursively
function getMarkdownFiles(dir: string, fileList: string[] = []): string[] {
    let files: fs.Dirent[];
    try {
        files = fs.readdirSync(dir, { withFileTypes: true });
    } catch (error) {
        console.error(`Error reading directory ${dir}:`, error);
        return fileList; // Return current list if directory can't be read
    }

    files.forEach(file => {
        const filePath = path.join(dir, file.name);

        if (file.isDirectory()) {
            // Skip ignored directories
            if (!IGNORE_DIRS.includes(file.name)) {
                getMarkdownFiles(filePath, fileList);
            }
        } else if (
            file.isFile() && // Ensure it's a file
            (file.name.endsWith('.md') || file.name.endsWith('.markdown')) &&
            !IGNORE_FILES.includes(file.name)
        ) {
            fileList.push(filePath);
        }
    });

    return fileList;
}

// Helper function to get relative path for section headers
function getRelativePath(filePath: string): string {
    return path.relative(process.cwd(), filePath)
        .replace(/\\/g, '/') // Normalize path separators
        .replace(/\.md$/, '')
        .replace(/\.markdown$/, '');
}

// Helper function to safely extract content from a markdown file
function extractContent(filePath: string): { frontmatter: string; content: string } {
    try {
        const content = fs.readFileSync(filePath, 'utf8');

        // Try to parse frontmatter, but continue even if it fails
        try {
            const { data, content: markdownContent } = matter(content);
            const frontmatter = Object.keys(data).length > 0
                ? '```yaml\n' + yaml.dump(data, { lineWidth: -1 }) + '\n```\n\n' // Use js-yaml dump
                : '';
            return { frontmatter, content: markdownContent };
        } catch (e: any) {
            console.warn(`Warning: Could not parse frontmatter for ${filePath}, including raw content. Error: ${e.message}`);
            // If frontmatter parsing fails, just return the raw content
            return { frontmatter: '', content };
        }
    } catch (error: any) {
        console.error(`Error reading file ${filePath}:`, error);
        return { frontmatter: '', content: `Error reading file: ${filePath}\n\n` }; // Add newlines for clarity in output
    }
}

// Main function to combine markdown files
function combineMarkdownFiles(): void {
    const markdownFiles = getMarkdownFiles(process.cwd());
    let combinedContent = `# Combined DFDA Wiki Documentation\nGenerated on: ${new Date().toISOString()}\n\n`;

    // Sort files to ensure consistent order
    markdownFiles.sort();

    // Track processed files and errors
    const processedFiles: string[] = [];
    const errorFiles: string[] = [];

    markdownFiles.forEach(filePath => {
        try {
            const relativePath = getRelativePath(filePath);
            const { frontmatter, content } = extractContent(filePath);

            combinedContent += `## File: ${relativePath}\n\n`;
            if (frontmatter) {
                combinedContent += frontmatter;
            }
            combinedContent += content.trim() + '\n\n---\n\n';
            processedFiles.push(relativePath);
        } catch (error) {
            console.error(`Error processing ${filePath}:`, error);
            errorFiles.push(filePath);
        }
    });

    // Add footer with statistics
    combinedContent += '\n\n---\n';
    combinedContent += `# Processing Summary\n\n`;
    combinedContent += `- Total files processed: ${processedFiles.length}\n`;
    combinedContent += `- Files with errors: ${errorFiles.length}\n`;
    if (errorFiles.length > 0) {
        combinedContent += `\nFiles with errors:\n${errorFiles.map(f => `- ${f}`).join('\n')}\n`;
    }
    combinedContent += `\nGenerated on: ${new Date().toISOString()}`;

    // Write the combined content
    try {
        fs.writeFileSync(OUTPUT_FILE, combinedContent);
        console.log(`\nProcessing complete:\n- Total files processed: ${processedFiles.length}\n- Files with errors: ${errorFiles.length}\n- Output written to: ${OUTPUT_FILE}\n`);
    } catch (writeError: any) {
        console.error(`Error writing output file ${OUTPUT_FILE}:`, writeError);
        // Don't exit here, the script might have already logged other errors
    }
}

// Run the script
try {
    combineMarkdownFiles();
} catch (error) {
    console.error('An unexpected error occurred during markdown combination:', error);
    process.exit(1); // Exit on unexpected top-level error
} 