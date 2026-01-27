/**
 * Image generation prompt templates and style definitions
 * Centralizes all prompt configuration for easy maintenance and consistency
 */

/**
 * Visual style instruction - simple and consistent
 */
export const RETRO_FUTURISTIC_STYLE = `Use a fun retro futuristic style and LARGE text.`;

export const RETRO_ACADEMIC_STYLE = `Use a retro black and white scientific illustration style.`;

export const BW_ACADEMIC_STYLE = `Use a black and white scientific illustration style.`;

/**
 * Generate OG image prompt (optimized for social media thumbnails)
 * Simple approach: style + content only, let the model figure out the visualization
 */
export function buildOgImagePrompt(content: string, style: string = RETRO_FUTURISTIC_STYLE): string {
  return `${style}\n\n${content}`;
}

/**
 * Generate infographic prompt (detailed, full-size vertical image)
 * Simple approach: style + content only, let the model figure out the visualization
 */
export function buildInfographicPrompt(content: string, style: string = RETRO_FUTURISTIC_STYLE): string {
  return `${style}\n\n${content}`;
}

/**
 * Generate presentation slide prompt (PowerPoint-optimized)
 * Simple approach: style + content only, let the model figure out the visualization
 */
export function buildSlidePrompt(content: string, style: string = RETRO_FUTURISTIC_STYLE): string {
  return `${style}\n\n${content}`;
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
  'retro-academic': {
    name: 'retro-academic',
    style: RETRO_ACADEMIC_STYLE,
    suffix: '-retro-academic',
    description: 'retro black and white scientific illustration',
  },
  'bw-academic': {
    name: 'bw-academic',
    style: BW_ACADEMIC_STYLE,
    suffix: '-bw-academic',
    description: 'black and white scientific illustration (no retro styling)',
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
