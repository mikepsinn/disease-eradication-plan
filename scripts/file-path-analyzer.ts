import structure from './config/structure';
import LLMClient from './llm-client';

const llmClient = new LLMClient();

// Replace static validSubdirectories with dynamic generation
type ValidSubdirectories = Record<string, Set<string>>;
const validSubdirectories: ValidSubdirectories = Object.entries(structure).reduce((acc, [category, subdirs]) => {
  if (Array.isArray(subdirs)) {
    acc[category] = new Set(subdirs);
  }
  return acc;
}, {} as ValidSubdirectories);

console.log('Generated valid subdirectories:', validSubdirectories);

interface Analysis {
  targetDirectory: string;
  action: 'move' | 'delete' | 'skip' | 'flag';
  priority: number;
  [key: string]: any;
}

async function analyzeFileLocation(filePath: string, fileContent: string, options: Record<string, any> = {}): Promise<Analysis> {
    const analysis = await llmClient.analyzeLocation(filePath, fileContent, options);
    return ensureFullPath(analysis);
}

function validateAnalysis(analysis: Analysis): void {
    // Split and filter empty parts from target directory
    const dirParts = analysis.targetDirectory.split('/').filter(p => p);
    
    if (dirParts.length === 0) {
        throw new Error('Empty target directory path');
    }

    // Check if the root category exists in structure
    const rootCategory = dirParts[0];
    if (!(rootCategory in structure)) {
        throw new Error(`Invalid root category: ${rootCategory}`);
    }

    // Check if subdirectories are allowed in the category
    if (dirParts.length > 1) {
        const subCategory = dirParts[1];
        if (!Array.isArray(structure[rootCategory]) || !structure[rootCategory].includes(subCategory)) {
            throw new Error(`Invalid subdirectory ${subCategory} for category ${rootCategory}`);
        }
    }

    if (!['move', 'delete', 'skip', 'flag'].includes(analysis.action)) {
        throw new Error('Invalid action in analysis response');
    }

    if (analysis.priority < 1 || analysis.priority > 5) {
        throw new Error('Priority must be between 1-5');
    }

    if (analysis.action === 'move') {
        const [category, subdir] = analysis.targetDirectory.split('/').filter(Boolean);
        if (!validSubdirectories[category]?.has(subdir)) {
            throw new Error(`Invalid subdirectory ${subdir} for category ${category}`);
        }
    }
}

function isValidPath(suggestedPath: string): boolean {
    // Ensure path starts from root
    if (!suggestedPath.startsWith('/')) {
        return false;
    }

    const parts = suggestedPath.split('/').filter(p => p);
    
    // Ensure at least one directory level
    if (parts.length === 0) {
        return false;
    }

    // Get the root directory
    const rootDir = parts[0];
    if (!(rootDir in structure)) {
        return false;
    }

    // For root level directories that are arrays
    if (Array.isArray(structure[rootDir])) {
        // If there's a second part, it must be in the allowed subdirectories
        return parts.length === 1 || structure[rootDir].includes(parts[1]);
    }

    return true;
}

function ensureFullPath(analysis: Analysis): Analysis {
    if (!analysis.targetDirectory) {
        throw new Error('Target directory is required');
    }

    // Ensure path starts with /
    if (!analysis.targetDirectory.startsWith('/')) {
        analysis.targetDirectory = '/' + analysis.targetDirectory;
    }

    return analysis;
}

export {
    analyzeFileLocation,
    validateAnalysis,
    isValidPath
}; 