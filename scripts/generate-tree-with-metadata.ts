import * as fs from 'fs';
import * as path from 'path';
import ignore from 'ignore';
import matter from 'gray-matter';

interface TreeNode {
    name: string;
    type: 'file' | 'directory';
    path: string; // Only relative path
    metadata?: Record<string, any>;
    children: TreeNode[];
}

function normalizePath(filePath: string): string {
    // Convert Windows backslashes to forward slashes and ensure no trailing slash
    return filePath.replace(/\\/g, '/').replace(/\/$/, '');
}

function extractFrontmatter(filePath: string): Record<string, any> | undefined {
    try {
        if (filePath.endsWith('.md')) {
            const content = fs.readFileSync(filePath, 'utf8');
            const { data } = matter(content);
            return Object.keys(data).length > 0 ? data : undefined;
        }
    } catch (error) {
        console.error(`Error reading frontmatter from ${filePath}:`, error);
    }
    return undefined;
}

function hasMatchingFiles(dir: string, ig: ignore.Ignore, markdownOnly: boolean): boolean {
    try {
        const files = fs.readdirSync(dir);
        
        for (const file of files) {
            const fullPath = path.join(dir, file);
            const relativePath = path.relative(process.cwd(), fullPath);
            
            if (ig.ignores(relativePath)) {
                continue;
            }
            
            const stats = fs.statSync(fullPath);
            
            if (stats.isDirectory()) {
                if (hasMatchingFiles(fullPath, ig, markdownOnly)) {
                    return true;
                }
            } else if (!markdownOnly || file.endsWith('.md')) {
                return true;
            }
        }
    } catch (error) {
        console.error(`Error reading directory ${dir}:`, error);
    }
    
    return false;
}

function generateTreeWithMetadata(dir: string, ig: ignore.Ignore, markdownOnly = false): TreeNode {
    const baseName = path.basename(dir);
    const relativePath = path.relative(process.cwd(), dir);
    
    const tree: TreeNode = {
        name: baseName,
        type: 'directory',
        path: normalizePath(relativePath || '.'),
        children: []
    };

    try {
        const files = fs.readdirSync(dir);
        
        // Filter and sort files
        const validFiles = files.filter(file => {
            const fullPath = path.join(dir, file);
            const relativePath = path.relative(process.cwd(), fullPath);
            
            if (ig.ignores(relativePath)) {
                return false;
            }
            
            const stats = fs.statSync(fullPath);
            const isDirectory = stats.isDirectory();
            
            if (isDirectory) {
                return hasMatchingFiles(fullPath, ig, markdownOnly);
            }
            
            return !markdownOnly || file.endsWith('.md');
        });

        validFiles.sort();

        for (const file of validFiles) {
            const fullPath = path.join(dir, file);
            const fileRelativePath = path.relative(process.cwd(), fullPath);
            const stats = fs.statSync(fullPath);
            
            if (stats.isDirectory()) {
                const childTree = generateTreeWithMetadata(fullPath, ig, markdownOnly);
                if (childTree.children.length > 0) {
                    tree.children.push(childTree);
                }
            } else {
                const metadata = extractFrontmatter(fullPath);
                const fileNode: TreeNode = {
                    name: file,
                    type: 'file',
                    path: normalizePath(fileRelativePath),
                    children: [],
                    ...(metadata && { metadata })
                };
                tree.children.push(fileNode);
            }
        }
    } catch (error) {
        console.error(`Error processing directory ${dir}:`, error);
    }

    return tree;
}

function main() {
    // Parse command line arguments
    const args = process.argv.slice(2);
    const markdownOnly = args.includes('--markdown');
    const outputFile = args.find(arg => arg.startsWith('--output='))?.split('=')[1] || 'tree-config.ts';
    
    // Read .gitignore if it exists
    let ig = ignore();
    try {
        const gitignore = fs.readFileSync('.gitignore', 'utf8');
        ig = ignore().add(gitignore);
    } catch (error) {
        console.log('No .gitignore found, proceeding without ignore rules');
    }
    
    const tree = generateTreeWithMetadata(process.cwd(), ig, markdownOnly);
    
    // Generate TypeScript configuration
    const tsConfig = `// Auto-generated tree configuration with metadata
export const treeConfig = ${JSON.stringify(tree, null, 2)} as const;

// Type definition for the tree structure
export type TreeNode = {
    name: string;
    type: 'file' | 'directory';
    path: string; // Relative path with forward slashes
    metadata?: Record<string, any>;
    children: TreeNode[];
};
`;

    fs.writeFileSync(outputFile, tsConfig);
    console.log(`Tree structure with metadata has been saved to ${outputFile}`);
}

if (require.main === module) {
    main();
}

export { generateTreeWithMetadata, TreeNode }; 