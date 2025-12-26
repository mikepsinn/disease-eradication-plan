/**
 * Image generation prompt templates and style definitions
 * Centralizes all prompt configuration for easy maintenance and consistency
 */

/**
 * Visual style instruction - simple and consistent
 */
const RETRO_FUTURISTIC_STYLE = `Use a fun retro futuristic style and LARGE text.`;

/**
 * Text legibility requirements based on Gemini 3 Pro Image best practices
 * Research: ~94% text accuracy achievable with explicit instructions
 */
const TEXT_LEGIBILITY_RULES = `TEXT: Large.`;

/**
 * Generate OG image prompt (optimized for social media thumbnails)
 */
export function buildOgImagePrompt(content: string): string {
  return `Please generate an engaging, simple social media image for the following content.
${RETRO_FUTURISTIC_STYLE}
${TEXT_LEGIBILITY_RULES}

Here is the content to illustrate:
---
${content}
---`;
}

/**
 * Generate infographic prompt (detailed, full-size vertical image)
 */
export function buildInfographicPrompt(content: string): string {
  return `Please generate a SIMPLE infographic for the following content.
${RETRO_FUTURISTIC_STYLE}
${TEXT_LEGIBILITY_RULES}

Here is the content to illustrate:
---
${content}
---`;
}

/**
 * Generate presentation slide prompt (PowerPoint-optimized)
 */
export function buildSlidePrompt(content: string): string {
  return `Please generate a simple PowerPoint presentation slide for the following content.
${RETRO_FUTURISTIC_STYLE}
${TEXT_LEGIBILITY_RULES}

Here is the content to illustrate:
---
${content}
---`;
}

/**
 * Image generation configuration
 */
export interface ImagePromptConfig {
  /** Function to build the prompt from content */
  buildPrompt: (content: string) => string;
  /** Aspect ratio for the image */
  aspectRatio: '16:9' | '9:16' | '1:1';
  /** Human-readable description of image type */
  description: string;
}

/**
 * Complete configuration for all image types
 */
export const ImagePrompts = {
  og: {
    buildPrompt: buildOgImagePrompt,
    aspectRatio: '16:9' as const,
    description: 'social media optimized',
  },
  infographic: {
    buildPrompt: buildInfographicPrompt,
    aspectRatio: '9:16' as const,
    description: 'detailed vertical',
  },
  slide: {
    buildPrompt: buildSlidePrompt,
    aspectRatio: '16:9' as const,
    description: 'PowerPoint-optimized',
  },
} as const;

/**
 * Example: Custom prompt builder with different style
 *
 * export function buildCustomPrompt(content: string): string {
 *   const CUSTOM_STYLE = `minimalist flat design with pastel colors...`;
 *   return [
 *     PromptSections.contentHeader('a custom image'),
 *     PromptSections.contentBlock(content),
 *     PromptSections.visualStyleBlock(CUSTOM_STYLE),
 *   ].join('\n');
 * }
 */
