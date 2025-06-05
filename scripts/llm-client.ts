import { OpenAI } from 'openai';
import { ChatCompletionMessageParam, ChatCompletionCreateParamsBase } from 'openai/resources/chat/completions';

// Define an interface for the options parameter in the complete method
interface CompletionOptions {
    model?: string;
    temperature?: number;
    responseFormat?: ChatCompletionCreateParamsBase['response_format'];
}

class LLMClient {
    private openai: OpenAI;

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

    async complete(systemPrompt: string, userContent: string, options: CompletionOptions = {}): Promise<string> {
        const {
            model = 'qwen-plus',
            temperature = 0.3,
            responseFormat = { type: "json_object" }
        } = options;

        const messages: ChatCompletionMessageParam[] = [
            { role: "system", content: systemPrompt },
            { role: "user", content: userContent }
        ];

        try {
            const completion = await this.openai.chat.completions.create({
                model,
                messages,
                temperature,
                response_format: responseFormat
            });

            if (!completion?.choices?.[0]?.message?.content) {
                throw new Error('Invalid or empty response from AI service');
            }

            return completion.choices[0].message.content;
        } catch (error: any) {
            // Catch any error and re-throw with a more descriptive message
            throw new Error(`AI completion failed: ${error.message}`);
        }
    }
}

export default LLMClient; 