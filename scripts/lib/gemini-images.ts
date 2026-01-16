/**
 * Google Gemini AI Image Generation Utility
 *
 * Uses the @google/genai SDK to generate images via Gemini API
 * Documentation: https://ai.google.dev/gemini-api/docs/libraries
 * npm: https://www.npmjs.com/package/@google/genai
 */

import { GoogleGenAI } from '@google/genai'
import sharp from 'sharp'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

// Simple logger to avoid env validation issues in standalone scripts
const log = {
  info: (...args: any[]) => console.log('[genai-image]', ...args),
  warn: (...args: any[]) => console.warn('[genai-image]', ...args),
  error: (...args: any[]) => console.error('[genai-image]', ...args),
}

// --- Rich Image Metadata for SEO/Discoverability ---

/**
 * Rich metadata for image SEO and discoverability
 * Embeds EXIF, IPTC, and XMP metadata for search engines
 */
export interface ImageMetadata {
  /** Image title/headline (IPTC:Headline, XMP:Title) */
  title?: string

  /** Image description/caption (EXIF:ImageDescription, IPTC:Caption-Abstract, XMP:Description) */
  description?: string

  /** Searchable keywords/tags (IPTC:Keywords, XMP:Subject) */
  keywords?: string[]

  /** Creator/author name (EXIF:Artist, IPTC:By-line, XMP:Creator) */
  author?: string

  /** Copyright notice (EXIF:Copyright, IPTC:CopyrightNotice, XMP:Rights) */
  copyright?: string

  /** License type (XMP:WebStatement for license URL) */
  license?: string

  /** License URL */
  licenseUrl?: string

  /** Source URL where image is published */
  sourceUrl?: string

  /** Credit/attribution text (IPTC:Credit) */
  credit?: string

  /** Contact website (IPTC:Contact) */
  website?: string

  /** Subject/category (IPTC:Category) */
  category?: string

  /** Software used to create image (EXIF:Software, XMP:CreatorTool) */
  generator?: string
}

// Default metadata values (exported for reuse)
export const DEFAULT_METADATA: Partial<ImageMetadata> = {
  author: 'Mike P. Sinn',
  copyright: '© Mike P. Sinn - WarOnDisease.org',
  license: 'CC BY-NC 4.0',
  licenseUrl: 'https://creativecommons.org/licenses/by-nc/4.0/',
  website: 'https://WarOnDisease.org',
  credit: 'WarOnDisease.org / Decentralized Institutes of Health',
}

// --- Image Model Cost Configuration ---

interface ImageModelConfig {
  id: string
  costPerImage: number // USD per image
  maxImagesPerRequest: number
}

const IMAGE_MODEL_CONFIGS: Record<string, ImageModelConfig> = {
  // Gemini Imagen models
  // Pricing from: https://ai.google.dev/pricing
  'gemini-3-pro-image-preview': {
    id: 'gemini-3-pro-image-preview',
    costPerImage: 0.04, // $0.04 per image (standard quality)
    maxImagesPerRequest: 8,
  },
}

/**
 * Add watermark to image
 */
async function addWatermark(imagePath: string): Promise<void> {
  const text = 'WarOnDisease.org';
  const fontSize = 16;

  // Create SVG watermark with transparent background and white text with black stroke
  // Tight bounds around text (width ~160px for 16 chars, height ~24px for 16px font)
  const svgWidth = 165;
  const svgHeight = 24;
  const svgWatermark = `
    <svg width="${svgWidth}" height="${svgHeight}">
      <text x="${svgWidth / 2}" y="18" font-family="'Courier New', Courier, monospace"
            font-size="${fontSize}" fill="white" stroke="black" stroke-width="1" text-anchor="middle">
        ${text}
      </text>
    </svg>
  `;

  const watermarkBuffer = Buffer.from(svgWatermark);

  // Load image and get dimensions and format
  const image = sharp(imagePath);
  const metadata = await image.metadata();

  if (!metadata.width || !metadata.height) {
    throw new Error('Could not read image dimensions');
  }

  // Position watermark flush with bottom-right corner (no padding)
  const left = metadata.width - svgWidth;
  const top = metadata.height - svgHeight;

  // Composite watermark onto image, preserving format
  let pipeline = image.composite([{
    input: watermarkBuffer,
    left,
    top,
  }]);

  // Ensure output format matches input
  if (metadata.format === 'png') {
    pipeline = pipeline.png();
  } else if (metadata.format === 'jpeg') {
    pipeline = pipeline.jpeg({ quality: 95 });
  } else if (metadata.format === 'webp') {
    pipeline = pipeline.webp({ quality: 95 });
  }

  await pipeline.toFile(imagePath + '.tmp');

  // Replace original with watermarked version
  const fs = await import('fs/promises');
  await fs.rename(imagePath + '.tmp', imagePath);
}

/**
 * Check if exiftool is available on the system
 */
async function isExiftoolAvailable(): Promise<boolean> {
  try {
    await execAsync('exiftool -ver')
    return true
  } catch {
    return false
  }
}

/**
 * Escape string for shell command (Windows-compatible)
 */
function escapeForShell(str: string): string {
  // Replace double quotes with escaped quotes and wrap in double quotes
  return `"${str.replace(/"/g, '\\"').replace(/\n/g, ' ')}"`
}

/**
 * Add rich metadata to image using exiftool (EXIF, IPTC, XMP)
 * Falls back to basic sharp metadata if exiftool is not available
 *
 * @param imagePath - Path to the image file
 * @param metadata - Rich metadata to embed
 */
export async function addImageMetadata(imagePath: string, metadata: ImageMetadata = {}): Promise<void> {
  const fs = await import('fs/promises')

  // Merge with defaults
  const meta: ImageMetadata = { ...DEFAULT_METADATA, ...metadata }

  // Try exiftool first (full IPTC/XMP support)
  const hasExiftool = await isExiftoolAvailable()

  if (hasExiftool) {
    await addMetadataWithExiftool(imagePath, meta)
  } else {
    log.warn('exiftool not found, using basic sharp metadata (install exiftool for full IPTC/XMP support)')
    await addMetadataWithSharp(imagePath, meta)
  }
}

/**
 * Add comprehensive metadata using exiftool
 * Embeds EXIF, IPTC Core, and XMP metadata for maximum discoverability
 */
async function addMetadataWithExiftool(imagePath: string, meta: ImageMetadata): Promise<void> {
  const args: string[] = ['-overwrite_original']

  // EXIF metadata
  if (meta.description) args.push(`-EXIF:ImageDescription=${escapeForShell(meta.description)}`)
  if (meta.author) args.push(`-EXIF:Artist=${escapeForShell(meta.author)}`)
  if (meta.copyright) args.push(`-EXIF:Copyright=${escapeForShell(meta.copyright)}`)
  if (meta.generator) args.push(`-EXIF:Software=${escapeForShell(meta.generator)}`)

  // IPTC Core metadata (widely used by stock photo sites, Google Images)
  if (meta.title) args.push(`-IPTC:Headline=${escapeForShell(meta.title)}`)
  if (meta.description) args.push(`-IPTC:Caption-Abstract=${escapeForShell(meta.description)}`)
  if (meta.author) args.push(`-IPTC:By-line=${escapeForShell(meta.author)}`)
  if (meta.copyright) args.push(`-IPTC:CopyrightNotice=${escapeForShell(meta.copyright)}`)
  if (meta.credit) args.push(`-IPTC:Credit=${escapeForShell(meta.credit)}`)
  if (meta.website) args.push(`-IPTC:Source=${escapeForShell(meta.website)}`)
  if (meta.category) args.push(`-IPTC:Category=${escapeForShell(meta.category)}`)

  // IPTC Keywords (each keyword as separate tag)
  if (meta.keywords && meta.keywords.length > 0) {
    for (const keyword of meta.keywords) {
      args.push(`-IPTC:Keywords=${escapeForShell(keyword)}`)
    }
  }

  // XMP metadata (modern standard, used by Adobe, Google, etc.)
  if (meta.title) args.push(`-XMP:Title=${escapeForShell(meta.title)}`)
  if (meta.description) args.push(`-XMP:Description=${escapeForShell(meta.description)}`)
  if (meta.author) args.push(`-XMP:Creator=${escapeForShell(meta.author)}`)
  if (meta.copyright) args.push(`-XMP:Rights=${escapeForShell(meta.copyright)}`)
  if (meta.licenseUrl) args.push(`-XMP:WebStatement=${escapeForShell(meta.licenseUrl)}`)
  if (meta.license) args.push(`-XMP:UsageTerms=${escapeForShell(meta.license)}`)
  if (meta.generator) args.push(`-XMP:CreatorTool=${escapeForShell(meta.generator)}`)
  if (meta.sourceUrl) args.push(`-XMP:Source=${escapeForShell(meta.sourceUrl)}`)

  // XMP Subject (keywords)
  if (meta.keywords && meta.keywords.length > 0) {
    for (const keyword of meta.keywords) {
      args.push(`-XMP:Subject=${escapeForShell(keyword)}`)
    }
  }

  // Add creation date
  const now = new Date().toISOString().replace(/[:-]/g, '').split('.')[0]
  args.push(`-EXIF:DateTimeOriginal=${now}`)
  args.push(`-XMP:CreateDate=${now}`)

  // Execute exiftool
  const command = `exiftool ${args.join(' ')} "${imagePath}"`

  try {
    await execAsync(command)
    log.info('Rich metadata embedded via exiftool', {
      title: meta.title,
      keywords: meta.keywords?.length || 0,
      aiDisclosure: meta.aiGenerated,
    })
  } catch (error: any) {
    log.error('Failed to add metadata with exiftool', { error: error.message })
    // Fall back to sharp
    await addMetadataWithSharp(imagePath, meta)
  }
}

/**
 * Add basic metadata using sharp (fallback when exiftool not available)
 * Limited to EXIF fields that sharp supports
 */
async function addMetadataWithSharp(imagePath: string, meta: ImageMetadata): Promise<void> {
  const fs = await import('fs/promises')
  const image = sharp(imagePath)
  const existingMetadata = await image.metadata()

  // Build description with all available info
  const descriptionParts: string[] = []
  if (meta.title) descriptionParts.push(meta.title)
  if (meta.description) descriptionParts.push(meta.description)
  if (meta.keywords?.length) descriptionParts.push(`Keywords: ${meta.keywords.join(', ')}`)

  const fullDescription = descriptionParts.join(' | ')

  // Sharp metadata options (limited compared to exiftool)
  const sharpMetadata: any = {
    exif: {
      IFD0: {
        Copyright: meta.copyright || DEFAULT_METADATA.copyright,
        Artist: meta.author || DEFAULT_METADATA.author,
        ImageDescription: fullDescription || meta.description || '',
        Software: meta.generator || 'Google Gemini Imagen',
      },
    },
  }

  // Write metadata, preserving format
  let pipeline = image.withMetadata(sharpMetadata)

  if (existingMetadata.format === 'png') {
    pipeline = pipeline.png()
  } else if (existingMetadata.format === 'jpeg') {
    pipeline = pipeline.jpeg({ quality: 95 })
  } else if (existingMetadata.format === 'webp') {
    pipeline = pipeline.webp({ quality: 95 })
  }

  await pipeline.toFile(imagePath + '.meta.tmp')
  await fs.rename(imagePath + '.meta.tmp', imagePath)

  log.info('Basic metadata embedded via sharp (install exiftool for full IPTC/XMP)', {
    copyright: meta.copyright,
    author: meta.author,
  })
}

/**
 * Calculate cost for image generation
 */
function calculateImageCost(imageCount: number, modelId: string): number {
  const config = IMAGE_MODEL_CONFIGS[modelId]
  if (!config) {
    console.warn(`⚠️  Unknown image model ${modelId}, cannot estimate cost`)
    return 0
  }

  return imageCount * config.costPerImage
}

/**
 * Log image generation request details
 */
function logImageRequest(modelId: string, imageCount: number, aspectRatio: string, promptPreview: string, referenceImageCount: number = 0): void {
  const config = IMAGE_MODEL_CONFIGS[modelId]
  const estimatedCost = calculateImageCost(imageCount, modelId)

  console.log('─'.repeat(80))
  console.log(`🖼️  Image Generation Request: ${modelId}`)
  console.log(`📐 Aspect ratio: ${aspectRatio}`)
  console.log(`🔢 Image count: ${imageCount}`)
  if (referenceImageCount > 0) {
    console.log(`🎨 Reference images: ${referenceImageCount}`)
  }
  console.log(`📝 Prompt preview: ${promptPreview.substring(0, 100)}${promptPreview.length > 100 ? '...' : ''}`)
  if (config) {
    console.log(`💵 Cost per image: $${config.costPerImage.toFixed(4)} USD`)
  }
  console.log(`💰 Estimated total cost: $${estimatedCost.toFixed(4)} USD`)
  console.log('⏳ Generating images...')
}

/**
 * Log image generation response details with actual cost
 */
function logImageResponse(modelId: string, imagesGenerated: number, totalRequested: number): void {
  const actualCost = calculateImageCost(imagesGenerated, modelId)
  const success = imagesGenerated === totalRequested

  console.log(success ? `✅ Images generated successfully` : `⚠️  Partial generation (${imagesGenerated}/${totalRequested})`)
  console.log(`🖼️  Images generated: ${imagesGenerated}`)
  console.log(`💰 Actual cost: $${actualCost.toFixed(4)} USD`)
  console.log('─'.repeat(80))
}

/**
 * Initialize the Google Gen AI client
 */
function getClient() {
  const apiKey = process.env.GOOGLE_GENERATIVE_AI_API_KEY

  if (!apiKey) {
    throw new Error('GOOGLE_GENERATIVE_AI_API_KEY environment variable is not set')
  }

  return new GoogleGenAI({ apiKey })
}

/**
 * Image generation options
 */
export interface ImageGenerationOptions {
  /** The text prompt describing the image to generate */
  prompt: string

  /** Number of images to generate (1-8, default: 1) */
  count?: number

  /** Image aspect ratio (default: '1:1') */
  aspectRatio?: '1:1' | '3:4' | '4:3' | '9:16' | '16:9'

  /** Model to use (default: 'gemini-3-pro-image-preview' - Nano Banana Pro) */
  model?: string

  /** Negative prompt - what to avoid in the image */
  negativePrompt?: string

  /** Safety filter level */
  safetyFilterLevel?: 'block_none' | 'block_some' | 'block_most'

  /** Person generation setting */
  personGeneration?: 'dont_allow' | 'allow_adult' | 'allow_all'

  /** Reference images for style/composition guidance (up to 14 images supported) */
  referenceImages?: ReferenceImage[]
}

/**
 * Reference image for image generation
 */
export interface ReferenceImage {
  /** Base64-encoded image data */
  data: string
  /** MIME type (e.g., 'image/png', 'image/jpeg') */
  mimeType: string
}

/**
 * Generated image result
 */
export interface GeneratedImage {
  /** Base64-encoded image data */
  imageBytes: string

  /** RAI (Responsible AI) filter reason if filtered */
  raiFilteredReason?: string

  /** Enhanced/rewritten prompt if prompt enhancer was enabled */
  enhancedPrompt?: string
}

/**
 * Image generation response
 */
export interface ImageGenerationResponse {
  /** Array of generated images */
  images: GeneratedImage[]

  /** Model used for generation */
  model: string

  /** Original prompt */
  prompt: string
}

/**
 * Generate images using Google Gemini Imagen API
 *
 * @example
 * ```typescript
 * const result = await generateImages({
 *   prompt: 'A neobrutalist propaganda poster for medical research',
 *   count: 2,
 *   aspectRatio: '16:9'
 * })
 *
 * // Save the first image
 * const imageBuffer = Buffer.from(result.images[0].data, 'base64')
 * await fs.writeFile('output.png', imageBuffer)
 * ```
 */
export async function generateImages(
  options: ImageGenerationOptions
): Promise<ImageGenerationResponse> {
  const {
    prompt,
    count = 1,
    aspectRatio = '1:1',
    model = 'gemini-3-pro-image-preview',
    negativePrompt,
    referenceImages = [],
  } = options

  // Log request with cost estimate
  logImageRequest(model, count, aspectRatio, prompt, referenceImages.length)

  try {
    const client = getClient()
    const images: GeneratedImage[] = []

    // Build the full prompt with aspect ratio and negative prompt
    let fullPrompt = prompt
    fullPrompt += `\n\nIMPORTANT: Generate image with aspect ratio ${aspectRatio}.`
    if (negativePrompt) {
      fullPrompt += `\n\nDO NOT include: ${negativePrompt}`
    }
    if (referenceImages.length > 0) {
      fullPrompt += `\n\nReference images are provided for style and composition guidance.`
    }

    // Build contents array with text and reference images
    const contentParts: any[] = [{ text: fullPrompt }]

    // Add reference images to content
    for (const refImage of referenceImages) {
      contentParts.push({
        inlineData: {
          mimeType: refImage.mimeType,
          data: refImage.data,
        },
      })
    }

    // Generate images one at a time (Gemini doesn't support batch generation in one call)
    for (let i = 0; i < count; i++) {
      const response = await client.models.generateContent({
        model,
        contents: contentParts,
      })

      // Extract image from response
      if (response.candidates && response.candidates.length > 0) {
        const candidate = response.candidates[0]
        const parts = candidate.content?.parts || []

        for (const part of parts) {
          if (part.inlineData?.data) {
            images.push({
              imageBytes: part.inlineData.data,
              raiFilteredReason: undefined,
              enhancedPrompt: undefined,
            })
          }
        }
      }
    }

    if (images.length === 0) {
      throw new Error('No images were generated')
    }

    // Log response with actual cost
    logImageResponse(model, images.length, count)

    return {
      images,
      model,
      prompt,
    }
  } catch (error: any) {
    log.error('Failed to generate images', {
      error: error.message || String(error),
      prompt: prompt.substring(0, 100),
    })
    throw new Error(`Image generation failed: ${error.message || String(error)}`)
  }
}

/**
 * Save a generated image to a file with rich metadata
 *
 * @example
 * ```typescript
 * const result = await generateImages({ prompt: 'A cat' })
 * await saveImage(result.images[0], 'output/cat.png', {
 *   title: 'A Beautiful Cat',
 *   description: 'AI-generated image of a cat',
 *   keywords: ['cat', 'animal', 'AI art'],
 * })
 * ```
 */
export async function saveImage(
  image: GeneratedImage,
  filePath: string,
  metadata?: ImageMetadata
): Promise<void> {
  const fs = await import('fs/promises')
  const path = await import('path')

  // Check if image was filtered
  if (image.raiFilteredReason) {
    throw new Error(`Image was filtered: ${image.raiFilteredReason}`)
  }

  if (!image.imageBytes) {
    throw new Error('No image data available')
  }

  // Ensure directory exists
  const dir = path.dirname(filePath)
  await fs.mkdir(dir, { recursive: true })

  // Decode base64 and write to file
  const buffer = Buffer.from(image.imageBytes, 'base64')
  await fs.writeFile(filePath, buffer)

  // Detect actual format and convert if necessary
  const requestedExt = path.extname(filePath).toLowerCase()
  const sharpImage = sharp(filePath)
  const sharpMeta = await sharpImage.metadata()

  // Map sharp format to expected extension
  const formatToExt: Record<string, string> = {
    'jpeg': '.jpg',
    'png': '.png',
    'webp': '.webp',
    'gif': '.gif',
    'tiff': '.tiff',
  }

  const actualExt = sharpMeta.format ? formatToExt[sharpMeta.format] : null

  if (actualExt && actualExt !== requestedExt) {
    log.warn(`Image format mismatch: requested ${requestedExt} but got ${actualExt}. Converting...`, { filePath })

    // Convert to requested format
    const tmpPath = filePath + '.converting.tmp'
    if (requestedExt === '.png') {
      await sharpImage.png().toFile(tmpPath)
    } else if (requestedExt === '.jpg' || requestedExt === '.jpeg') {
      await sharpImage.jpeg({ quality: 95 }).toFile(tmpPath)
    } else if (requestedExt === '.webp') {
      await sharpImage.webp({ quality: 95 }).toFile(tmpPath)
    } else {
      // For other formats, just use default sharp conversion
      await sharpImage.toFile(tmpPath)
    }

    // Replace original with converted version
    await fs.rename(tmpPath, filePath)
  }

  // Add rich metadata (EXIF, IPTC, XMP for SEO/discoverability)
  await addImageMetadata(filePath, metadata)

  // Add watermark to all generated images
  await addWatermark(filePath)

  log.info('Image saved with metadata and watermark', {
    filePath,
    size: buffer.length,
    format: sharpMeta.format,
    title: metadata?.title,
    keywords: metadata?.keywords?.length || 0,
  })
}

/**
 * Generate and save images in one step with rich metadata
 *
 * @example
 * ```typescript
 * await generateAndSaveImages({
 *   prompt: 'Neobrutalist medical research poster',
 *   count: 3,
 *   outputDir: 'public/assets/generated',
 *   filePrefix: 'poster',
 *   metadata: {
 *     title: 'Medical Research Advocacy Poster',
 *     description: 'Neobrutalist propaganda poster promoting medical research funding',
 *     keywords: ['medical research', 'healthcare', 'advocacy', 'poster'],
 *     category: 'Health/Medical',
 *   }
 * })
 * // Creates: poster-1.png, poster-2.png, poster-3.png with full EXIF/IPTC/XMP metadata
 * ```
 */
export async function generateAndSaveImages(options: {
  prompt: string
  count?: number
  aspectRatio?: ImageGenerationOptions['aspectRatio']
  outputDir: string
  filePrefix: string
  format?: 'png' | 'jpg'
  referenceImages?: ReferenceImage[]
  /** Rich metadata for SEO/discoverability (EXIF, IPTC, XMP) */
  metadata?: ImageMetadata
}): Promise<string[]> {
  const {
    prompt,
    count = 1,
    aspectRatio,
    outputDir,
    filePrefix,
    format = 'png',
    referenceImages,
    metadata,
  } = options

  const result = await generateImages({
    prompt,
    count,
    aspectRatio,
    referenceImages,
  })

  const filePaths: string[] = []

  // Build full metadata for SEO
  const fullMetadata: ImageMetadata = {
    ...metadata,
  }

  // Auto-generate title from prompt if not provided
  if (!fullMetadata.title && prompt) {
    // Extract first sentence or first 100 chars as title
    const firstSentence = prompt.split(/[.!?]/)[0].trim()
    fullMetadata.title = firstSentence.substring(0, 100)
  }

  // Auto-generate description if not provided
  if (!fullMetadata.description) {
    fullMetadata.description = prompt.substring(0, 500)
  }

  // Auto-generate keywords from prompt if not provided
  if (!fullMetadata.keywords || fullMetadata.keywords.length === 0) {
    fullMetadata.keywords = extractKeywordsFromText(prompt)
  }

  for (let i = 0; i < result.images.length; i++) {
    const fileName = count === 1
      ? `${filePrefix}.${format}`
      : `${filePrefix}-${i + 1}.${format}`

    const filePath = `${outputDir}/${fileName}`
    await saveImage(result.images[i], filePath, fullMetadata)
    filePaths.push(filePath)
  }

  log.info('Generated and saved images with rich metadata', {
    count: filePaths.length,
    outputDir,
    title: fullMetadata.title,
    keywords: fullMetadata.keywords?.length || 0,
  })

  return filePaths
}

/**
 * Extract keywords from text for SEO (exported for reuse)
 */
export function extractKeywordsFromText(text: string): string[] {
  // Remove common words and extract meaningful terms
  const stopWords = new Set([
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
    'that', 'which', 'who', 'whom', 'this', 'these', 'those', 'it',
    'its', 'my', 'your', 'his', 'her', 'their', 'our', 'what', 'how',
    'when', 'where', 'why', 'all', 'each', 'every', 'both', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
    'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now',
    'create', 'show', 'showing', 'image', 'picture', 'illustration',
    'depicting', 'generate', 'make', 'draw', 'style', 'like', 'using',
  ])

  const words = text
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, ' ')
    .split(/\s+/)
    .filter(word => word.length > 2 && !stopWords.has(word))

  // Get unique keywords, prioritize longer/more specific terms
  const unique = [...new Set(words)]
  const sorted = unique.sort((a, b) => b.length - a.length)

  // Return top 10 keywords
  return sorted.slice(0, 10)
}
