import * as fs from 'fs/promises';
import * as path from 'path';
import { shouldIgnore } from './shared-utilities';
import { analyzeFileLocation } from './file-path-analyzer';

async function getDirectoryTree(startPath: string): Promise<string> {
    const tree: string[] = [];
    
    async function buildTree(currentPath: string, relativePath = ''): Promise<void> {
        try {
            const items = await fs.readdir(currentPath, { withFileTypes: true });
            
            for (const item of items) {
                if (shouldIgnore(item.name)) continue;
                
                const fullPath = path.join(currentPath, item.name);
                const relPath = path.join(relativePath, item.name);
                
                if (item.isDirectory()) {
                    tree.push(`📁 ${relPath}/`);
                    await buildTree(fullPath, relPath);
                } else {
                    tree.push(`📄 ${relPath}`);
                }
            }
        } catch (error) {
            console.error(`Error processing directory ${currentPath}:`, error);
            throw error;
        }
    }
    
    await buildTree(startPath);
    return tree.join('\n');
}

async function suggestFolderWithLLM(filePath: string, fileContent: string): Promise<any> {
    return analyzeFileLocation(filePath, fileContent, {
        maxContentLength: 500
    });
}

export {
    getDirectoryTree,
    suggestFolderWithLLM
}; 