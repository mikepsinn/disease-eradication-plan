import { Tool, tool } from '@voltagent/core';
import { z } from 'zod';

// This is a placeholder for the actual web search function provided by the environment.
// In a real scenario, this would be injected or imported from the host.
declare const performWebSearch: (query: string) => Promise<string>;

export const webSearch = new Tool({
  id: 'web-search',
  name: 'Web Search',
  description: 'Performs a web search to find authoritative sources for information.',
  parameters: z.object({
    query: z.string().describe('The search query.'),
  }),
  run: async ({ parameters }: { parameters: { query: string } }) => {
    // In a real implementation, we would call the host's web search tool here.
    // For now, we will simulate the call and return a placeholder result.
    // This uses the `tool` helper to call the `web_search` tool from the host environment.
    const searchResult = await tool('web_search', { search_term: parameters.query });
    return JSON.stringify(searchResult);
  },
});
