const { structure } = require('./config/structure');
const LLMClient = require('./llm-client');

const llmClient = new LLMClient(process.env.OPENAI_API_KEY);

async function analyzeFileLocation(filePath, fileContent, options = {}) {
    return llmClient.analyzeLocation(filePath, fileContent, options);
}

function validateAnalysis(analysis) {
    if (!['move', 'delete', 'skip', 'flag'].includes(analysis.action)) {
        throw new Error('Invalid action in analysis response');
    }

    if (!isValidPath(analysis.targetDirectory)) {
        throw new Error(`Invalid target directory: ${analysis.targetDirectory}`);
    }

    if (analysis.priority < 1 || analysis.priority > 5) {
        throw new Error('Priority must be between 1-5');
    }
}

function isValidPath(suggestedPath) {
    const parts = suggestedPath.split('/').filter(p => p);
    let currentLevel = structure;
    
    for (const part of parts) {
        if (!currentLevel[part]) return false;
        currentLevel = currentLevel[part];
    }
    return true;
}

module.exports = {
    analyzeFileLocation,
    validateAnalysis,
    isValidPath
}; 