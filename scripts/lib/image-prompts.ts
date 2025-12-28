/**
 * Image generation prompt templates and style definitions
 * Centralizes all prompt configuration for easy maintenance and consistency
 */

/**
 * Visual style instruction - simple and consistent
 */
export const RETRO_FUTURISTIC_STYLE = `Use a fun retro futuristic style and LARGE text.`;

export const ACADEMIC_STYLE = `Use a black and white scientific illustration style.`;

//export const ACADEMIC_STYLE = `Use a retro scientific black and white academic style.`;

/**
 * Text legibility requirements based on Gemini 3 Pro Image best practices
 * Research: ~94% text accuracy achievable with explicit instructions
 */
const TEXT_LEGIBILITY_RULES = `TEXT: Ensure all text is large and legible.`;

/**
 * Generate OG image prompt (optimized for social media thumbnails)
 */
export function buildOgImagePrompt(content: string, style: string = RETRO_FUTURISTIC_STYLE): string {
  return `Please generate an engaging, simple social media image for the following content.
${style}
${TEXT_LEGIBILITY_RULES}

Here is the content to illustrate:
---
${content}
---`;
}

/**
 * Generate infographic prompt (detailed, full-size vertical image)
 */
export function buildInfographicPrompt(content: string, style: string = RETRO_FUTURISTIC_STYLE): string {
  return `Please generate a SIMPLE infographic for the following content.
${style}
${TEXT_LEGIBILITY_RULES}

Here is the content to illustrate:
---
${content}
---`;
}

/**
 * Generate presentation slide prompt (PowerPoint-optimized)
 */
export function buildSlidePrompt(content: string, style: string = RETRO_FUTURISTIC_STYLE): string {
  return `Please generate a presentation slide to graphically illustrate the following content.
${style}
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
  buildPrompt: (content: string, style?: string) => string;
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
    aspectRatio: '3:4' as const,
    description: 'book-friendly portrait',
  },
  slide: {
    buildPrompt: buildSlidePrompt,
    aspectRatio: '16:9' as const,
    description: 'PowerPoint-optimized',
  },
} as const;

/**
 * Available visual styles
 */
export const VisualStyles = {
  'retro-futuristic': {
    name: 'retro-futuristic',
    style: RETRO_FUTURISTIC_STYLE,
    suffix: '-retro-futuristic',
    description: 'fun retro futuristic',
  },
  academic: {
    name: 'academic',
    style: ACADEMIC_STYLE,
    suffix: '-academic',
    description: 'professional black and white',
  },
} as const;

export type VisualStyleName = keyof typeof VisualStyles;

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
