const { OpenAI } = require('openai');
const { structure } = require('./config/structure');

class LLMClient {
    constructor() {
        const apiKey = process.env.DASHSCOPE_API_KEY;
        if (!apiKey) {
            throw new Error('DASHSCOPE_API_KEY environment variable is not set');
        }
        
        this.openai = new OpenAI({
            baseURL: 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1',
            apiKey
        });
    }

    async analyzeLocation(filePath, content, options = {}) {
        const {
            maxContentLength = 1000,
            model = 'qwen-plus',
        } = options;

        const prompt = this.createAnalysisPrompt(filePath, content.substring(0, maxContentLength));

        try {
            const completion = await this.openai.chat.completions.create({
                model,
                messages: [
                    { role: "system", content: "You are a helpful assistant for analyzing file locations and content." },
                    { role: "user", content: prompt }
                ],
                temperature: 0.3,
                response_format: { type: "json_object" }
            });

            return JSON.parse(completion.choices[0].message.content);
        } catch (error) {
            throw new Error(`AI analysis failed: ${error.message}`);
        }
    }

    createAnalysisPrompt(filePath, content) {
        return `Given this repository structure:
        ${JSON.stringify(structure, null, 2)}

        File path: ${filePath}
        Content preview: ${content}

        Respond in JSON format: {
            "targetDirectory": "path/from/structure",
            "confidence": 1-5,
            "reason": "brief explanation",
            "action": "move|delete|skip|flag",
            "priority": 1-5
        }`;
    }
}

module.exports = LLMClient; 