const { OpenAI } = require('openai');
const structure = require('./config/structure');

class LLMClient {
    constructor() {
        const apiKey = process.env.DASHSCOPE_API_KEY;
        if (!apiKey) {
            throw new Error('DASHSCOPE_API_KEY environment variable is not set');
        }
        
        if (!structure || typeof structure !== 'object' || Object.keys(structure).length === 0) {
            throw new Error('Repository structure configuration is invalid or empty');
        }

        this.openai = new OpenAI({
            baseURL: 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1',
            apiKey
        });
    }

    async analyzeLocation(filePath, content, options = {}) {
        if (!filePath) {
            throw new Error('File path is required');
        }
        if (!content) {
            throw new Error('Content is required');
        }

        const {
            maxContentLength = 1000,
            model = 'qwen-plus',
        } = options;

        if (!model) {
            throw new Error('Model name is required');
        }

        const prompt = this.createAnalysisPrompt(filePath, content.substring(0, maxContentLength));

        try {
            const completion = await this.openai.chat.completions.create({
                model,
                messages: [
                    { 
                        role: "system", 
                        content: "You are a helpful assistant for analyzing file locations and content. " +
                                 "Only use existing directory paths from the structure configuration - " +
                                 "NEVER invent new paths or categories. " +
                                 "Always select the MOST SPECIFIC valid subdirectory. " +
                                 "Top-level categories (like 'analytics') are NOT valid targets - " +
                                 "you must choose a subdirectory from the structure."
                    },
                    { role: "user", content: prompt }
                ],
                temperature: 0.3,
                response_format: { type: "json_object" }
            });

            if (!completion?.choices?.[0]?.message?.content) {
                throw new Error('Invalid or empty response from AI service');
            }

            const result = JSON.parse(completion.choices[0].message.content);
            this.validateTargetDirectory(result.targetDirectory);
            return result;
        } catch (error) {
            throw new Error(`AI analysis failed: ${error.message}`);
        }
    }

    validateTargetDirectory(targetPath) {
        console.log('Validating target path:', targetPath);
        
        // Add check for top-level category
        if (targetPath.split('/').filter(p => p).length < 2) {
            throw new Error(`Path must include category and subdirectory (e.g. analytics/predictive-models). Received: ${targetPath}`);
        }

        const normalizedPath = targetPath.replace(/^\/+|\/+$/g, '');
        const pathParts = normalizedPath.split('/');
        let currentLevel = structure;
        
        console.log('Path parts:', pathParts);

        for (const [index, part] of pathParts.entries()) {
            console.log(`Checking level ${index + 1}: '${part}' in`, currentLevel);
            
            // Handle array-based categories
            if (Array.isArray(currentLevel)) {
                if (!currentLevel.includes(part)) {
                    throw new Error(`'${part}' not found in array ${JSON.stringify(currentLevel)}`);
                }
                currentLevel = structure[part] || currentLevel;
            } else {
                if (!currentLevel[part] && !Object.values(currentLevel).includes(part)) {
                    throw new Error(`'${part}' not found in structure level`);
                }
                currentLevel = currentLevel[part] || structure[part];
            }

            // Additional debug for analytics category
            if (part === 'analytics') {
                console.log('Full analytics structure:', JSON.stringify(structure.analytics, null, 2));
            }
        }
    }

    createAnalysisPrompt(filePath, content) {
        return `Given this EXACT repository structure:
        ${JSON.stringify(structure, null, 2)}

        File path: ${filePath}
        Content preview: ${content}

        Respond in JSON format: {
            "targetDirectory": "CATEGORY/SUBDIRECTORY",
            "confidence": 1-5,
            "reason": "brief explanation",
            "action": "move|delete|flag",
            "priority": 1-5
        }
        
        RULES:
        1. ALWAYS format targetDirectory as CATEGORY/SUBDIRECTORY
        2. Categories must be top-level (e.g. analytics)
        3. Subdirectories must exist under category
        4. If in correct location but wrong subdir: MOVE
        5. If already in correct subdir: FLAG for review`;
    }
}

module.exports = LLMClient; 