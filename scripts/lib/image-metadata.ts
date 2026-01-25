/**
 * Image Metadata Interfaces - Unified type definitions for image metadata
 *
 * This module consolidates the various metadata interfaces used across image scripts
 * to ensure consistent typing and avoid redundant definitions.
 */

/**
 * Basic file-level information about an image
 */
export interface ImageFileInfo {
  /** Relative path from project root */
  path: string
  /** File name only */
  filename: string
  /** File extension (e.g., '.png', '.jpg') */
  extension: string
  /** File size in bytes */
  sizeBytes: number
  /** Human-readable file size */
  size?: string
  /** Image width in pixels */
  width?: number
  /** Image height in pixels */
  height?: number
  /** Image format as detected by sharp (jpeg, png, etc.) */
  format?: string
  /** Aspect ratio as string (e.g., "16:9") */
  aspectRatio?: string
  /** Last modified date (ISO string) */
  modified?: string
}

/**
 * Content-related metadata (extracted or generated)
 */
export interface ImageContentMetadata {
  /** Image title/headline */
  title?: string
  /** Image description/caption */
  description?: string
  /** Keywords/tags for searchability */
  keywords?: string[]
  /** OCR transcript of visible text in the image */
  transcript?: string
  /** Original prompt used to generate the image */
  generationPrompt?: string
  /** AI-inferred prompt that could have generated this image */
  inferredPrompt?: string
  /** List of issues/problems identified in the image */
  imageIssues?: string[]
  /** Suggestions for improving the generation prompt */
  promptImprovements?: string[]
}

/**
 * Enrichment metadata from AI analysis
 */
export interface ImageEnrichmentMetadata {
  // Quality
  qualityScore?: number
  qualityIssues?: string[]
  standaloneScore?: number

  // Social Media
  canShareStandalone?: boolean
  socialCaption?: string
  twitterText?: string
  linkedInText?: string
  targetPlatforms?: string[]

  // Presentations
  speakerNotes?: string
  talkingPoints?: string[]
  audienceLevel?: string

  // Accessibility
  altText?: string
  emotionalTone?: string
  callToAction?: string

  // Data Integrity
  dataFreshness?: string
  dataSources?: string[]
  factCheckNotes?: string

  // Image Problems (leakage, figure numbers, text issues)
  imageProblemsDetected?: boolean
  imageProblems?: string[]
  imageProblemsRepairPrompt?: string

  // Timestamps
  metadataEnrichedAt?: string
  metadataCreatedAt?: string
}

/**
 * Author and copyright information
 */
export interface ImageAuthorMetadata {
  /** Creator/author name */
  author?: string
  /** Copyright notice */
  copyright?: string
  /** License type (e.g., 'CC BY-NC 4.0') */
  license?: string
  /** License URL */
  licenseUrl?: string
  /** Source URL where image is published */
  sourceUrl?: string
  /** Credit/attribution text */
  credit?: string
  /** Contact website */
  website?: string
}

/**
 * Classification metadata for organizing images
 */
export interface ImageClassificationMetadata {
  /** Image type based on path/naming */
  imageType?: 'og' | 'infographic' | 'slide' | 'icon' | 'cover' | 'chart' | 'other'
  /** Style (academic, retro, etc.) */
  style?: string
  /** Related chapter/section if applicable */
  chapter?: string
  /** Subject/category */
  category?: string
  /** Creation date from EXIF */
  dateCreated?: string
  /** Software used to create image */
  generator?: string
}

/**
 * Complete image metadata combining all types
 *
 * This is the full metadata object used in the image index
 * and for comprehensive image operations.
 */
export interface ImageMetadata
  extends ImageFileInfo,
    ImageContentMetadata,
    ImageEnrichmentMetadata,
    ImageAuthorMetadata,
    ImageClassificationMetadata {
  /** Flag indicating if image has been analyzed */
  analyzed?: boolean
}

/**
 * Metadata for image generation (input to generation functions)
 *
 * This is what you provide when generating a new image.
 * The generation functions will add default values for author, copyright, etc.
 */
export interface ImageGenerationMetadata {
  /** Image title/headline - REQUIRED for SEO */
  title: string
  /** Image description/caption - REQUIRED for SEO */
  description: string
  /** Keywords/tags for searchability - REQUIRED for SEO */
  keywords: string[]
  /** Creator/author name (optional, has default) */
  author?: string
  /** Copyright notice (optional, has default) */
  copyright?: string
  /** License type (optional, has default) */
  license?: string
  /** License URL (optional, has default) */
  licenseUrl?: string
  /** Credit/attribution text (optional, has default) */
  credit?: string
  /** Contact website (optional, has default) */
  website?: string
  /** Subject/category */
  category?: string
  /** Source URL where image is published */
  sourceUrl?: string
}

/**
 * Image index structure for search/discovery
 */
export interface ImageIndex {
  /** Total number of images */
  totalImages: number
  /** Total size in bytes */
  totalSizeBytes: number
  /** Human-readable total size */
  totalSize: string
  /** Array of image metadata */
  images: ImageMetadata[]
}

/**
 * Result of image search in transcript
 */
export interface ImageSearchMatch {
  /** Full path to the image */
  filepath: string
  /** Relative path from project root */
  relativePath: string
  /** The transcript text */
  transcript: string
  /** The original generation prompt (if available) */
  generationPrompt?: string
  /** The text that was matched */
  matchedText: string
  /** Context around the match for display */
  matchContext: string
}

/**
 * Default metadata values for image generation
 */
export const DEFAULT_IMAGE_METADATA: Partial<ImageGenerationMetadata> = {
  author: 'Mike P. Sinn',
  copyright: '© Mike P. Sinn - WarOnDisease.org',
  license: 'CC BY-NC 4.0',
  licenseUrl: 'https://creativecommons.org/licenses/by-nc/4.0/',
  website: 'https://WarOnDisease.org',
  credit: 'WarOnDisease.org / Decentralized Institutes of Health',
}

/**
 * Merge user-provided metadata with defaults
 */
export function mergeWithDefaults(
  metadata: Partial<ImageGenerationMetadata>
): ImageGenerationMetadata {
  return {
    title: '',
    description: '',
    keywords: [],
    ...DEFAULT_IMAGE_METADATA,
    ...metadata,
  } as ImageGenerationMetadata
}

/**
 * Clean title/description by removing style words
 */
export function cleanStyleFromText(text: string | undefined): string | undefined {
  if (!text) return text
  return text
    .replace(/\s*[-–]\s*(Retro|Academic)\s*/gi, ' ')
    .replace(/\b(Retro|Academic)\b\s*/gi, '')
    .replace(/\s+/g, ' ')
    .trim()
}

/**
 * Extract chapter/section from image path
 */
export function getChapterFromPath(filePath: string): string | undefined {
  // Look for knowledge/{section}/{chapter} pattern
  const match = filePath.match(/knowledge\/([^/]+)(?:\/([^/]+))?/)
  if (match) {
    if (match[2]) {
      // Remove file extension and suffixes
      const chapter = match[2].replace(/-(?:og|infographic|slide)-.*$/, '')
      return `${match[1]}/${chapter}`
    }
    return match[1]
  }
  return undefined
}
