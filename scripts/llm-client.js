const { OpenAI } = require('openai');

class LLMClient {
    constructor(apiKey, structure) {
        this.openai = new OpenAI(apiKey);
        this.structure = structure;
    }

    async analyzeLocation(filePath, content, options = {}) {
        const {
            maxContentLength = 1000,
            model = 'gpt-4',
        } = options;

        const prompt = this.createAnalysisPrompt(filePath, content.substring(0, maxContentLength));

        try {
            const completion = await this.openai.chat.completions.create({
                model,
                messages: [{ role: "user", content: prompt }],
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
        ${JSON.stringify(this.structure, null, 2)}

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