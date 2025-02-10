const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

// Configuration
const OUTPUT_FILE = 'combined_wiki.md';
const IGNORE_DIRS = ['.git', '.github', 'node_modules', '.obsidian', '.vscode'];
const IGNORE_FILES = ['combined_wiki.md'];

// Helper function to get all markdown files recursively
function getMarkdownFiles(dir, fileList = []) {
    const files = fs.readdirSync(dir);
    
    files.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        
        if (stat.isDirectory()) {
            // Skip ignored directories
            if (!IGNORE_DIRS.includes(file)) {
                getMarkdownFiles(filePath, fileList);
            }
        } else if (
            (file.endsWith('.md') || file.endsWith('.markdown')) && 
            !IGNORE_FILES.includes(file)
        ) {
            fileList.push(filePath);
        }
    });
    
    return fileList;
}

// Helper function to get relative path for section headers
function getRelativePath(filePath) {
    return path.relative(process.cwd(), filePath)
        .replace(/\\/g, '/') // Normalize path separators
        .replace(/\.md$/, '')
        .replace(/\.markdown$/, '');
}

// Helper function to safely extract content from a markdown file
function extractContent(filePath) {
    try {
        const content = fs.readFileSync(filePath, 'utf8');
        
        // Try to parse frontmatter, but continue even if it fails
        try {
            const { data, content: markdownContent } = matter(content);
            const frontmatter = Object.keys(data).length > 0 
                ? '```yaml\n' + Object.entries(data)
                    .map(([key, value]) => `${key}: ${value}`)
                    .join('\n') + '\n```\n\n'
                : '';
            return { frontmatter, content: markdownContent };
        } catch (e) {
            console.warn(`Warning: Could not parse frontmatter for ${filePath}, including raw content`);
            // If frontmatter parsing fails, just return the raw content
            return { frontmatter: '', content };
        }
    } catch (error) {
        console.error(`Error reading file ${filePath}:`, error);
        return { frontmatter: '', content: `Error reading file: ${filePath}` };
    }
}

// Main function to combine markdown files
function combineMarkdownFiles() {
    const markdownFiles = getMarkdownFiles(process.cwd());
    let combinedContent = `# Combined DFDA Wiki Documentation
Generated on: ${new Date().toISOString()}

`;

    // Sort files to ensure consistent order
    markdownFiles.sort();

    // Track processed files and errors
    const processedFiles = [];
    const errorFiles = [];

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
    fs.writeFileSync(OUTPUT_FILE, combinedContent);
    console.log(`
Processing complete:
- Total files processed: ${processedFiles.length}
- Files with errors: ${errorFiles.length}
- Output written to: ${OUTPUT_FILE}
`);
}

// Run the script
try {
    combineMarkdownFiles();
} catch (error) {
    console.error('Error combining markdown files:', error);
    process.exit(1);
} 