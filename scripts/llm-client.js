const { OpenAI } = require('openai');

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

    async complete(systemPrompt, userContent, options = {}) {
        const {
            model = 'qwen-plus',
            temperature = 0.3,
            responseFormat = { type: "json_object" }
        } = options;

        try {
            const completion = await this.openai.chat.completions.create({
                model,
                messages: [
                    { role: "system", content: systemPrompt },
                    { role: "user", content: userContent }
                ],
                temperature,
                response_format: responseFormat
            });

            if (!completion?.choices?.[0]?.message?.content) {
                throw new Error('Invalid or empty response from AI service');
            }

            return completion.choices[0].message.content;
        } catch (error) {
            throw new Error(`AI completion failed: ${error.message}`);
        }
    }
}

module.exports = LLMClient; 