const { OpenAI } = require('openai');
const { newStructure } = require('./migrate-content');
const openai = new OpenAI(process.env.OPENAI_API_KEY);

async function analyzeFileLocation(filePath, fileContent, options = {}) {
    const {
        maxContentLength = 1000,
        model = 'gpt-4',
        structure = newStructure
    } = options;

    const prompt = `Given this repository structure:
${JSON.stringify(structure, null, 2)}

File path: ${filePath}
Content preview (first ${maxContentLength} characters):
${fileContent.substring(0, maxContentLength)}...

Respond in JSON format: {
  "targetDirectory": "path/from/structure",
  "confidence": 1-5,
  "reason": "brief explanation",
  "action": "move|delete|skip|flag",
  "priority": 1-5
}`;

    try {
        const completion = await openai.chat.completions.create({
            model,
            messages: [{ role: "user", content: prompt }],
            temperature: 0.3,
            response_format: { type: "json_object" }
        });

        const response = JSON.parse(completion.choices[0].message.content);
        validateAnalysis(response);
        return response;
    } catch (error) {
        throw new Error(`AI analysis failed: ${error.message}`);
    }
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
    let currentLevel = newStructure;
    
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