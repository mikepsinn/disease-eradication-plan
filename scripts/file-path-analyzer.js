const structure = require('./config/structure');
const LLMClient = require('./llm-client');

const llmClient = new LLMClient();

async function analyzeFileLocation(filePath, fileContent, options = {}) {
    const analysis = await llmClient.analyzeLocation(filePath, fileContent, options);
    return ensureFullPath(analysis);
}

function validateAnalysis(analysis) {
    // Split and filter empty parts from target directory
    const dirParts = analysis.targetDirectory.split('/').filter(p => p);
    
    if (dirParts.length === 0) {
        throw new Error('Empty target directory path');
    }

    // Check if the root category exists in structure
    const rootCategory = dirParts[0];
    if (!structure[rootCategory]) {
        throw new Error(`Invalid root category: ${rootCategory}`);
    }

    // Check if subdirectories are allowed in the category
    if (dirParts.length > 1) {
        const subCategory = dirParts[1];
        if (!structure[rootCategory].includes(subCategory)) {
            throw new Error(`Invalid subdirectory ${subCategory} for category ${rootCategory}`);
        }
    }

    if (!['move', 'delete', 'skip', 'flag'].includes(analysis.action)) {
        throw new Error('Invalid action in analysis response');
    }

    if (analysis.priority < 1 || analysis.priority > 5) {
        throw new Error('Priority must be between 1-5');
    }
}

function isValidPath(suggestedPath) {
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

function ensureFullPath(analysis) {
    if (!analysis.targetDirectory) {
        throw new Error('Target directory is required');
    }

    // Ensure path starts with /
    if (!analysis.targetDirectory.startsWith('/')) {
        analysis.targetDirectory = '/' + analysis.targetDirectory;
    }

    return analysis;
}

module.exports = {
    analyzeFileLocation,
    validateAnalysis,
    isValidPath
}; 