/**
 * Image File Utilities - Common functions for image file operations
 *
 * Consolidates image discovery, MIME types, and validation across scripts:
 * - extract-image-text.ts
 * - fix-image-text.ts
 * - analyze-and-tag.ts
 * - convert-png-to-jpg.ts
 * - generate-image-index.ts
 */

import { readdirSync, existsSync, statSync } from 'fs'
import path from 'path'

/**
 * Supported image extensions (lowercase, with dot)
 */
export const SUPPORTED_IMAGE_EXTENSIONS = [
  '.png',
  '.jpg',
  '.jpeg',
  '.gif',
  '.webp',
] as const

/**
 * All supported image extensions including SVG
 */
export const ALL_IMAGE_EXTENSIONS = [
  ...SUPPORTED_IMAGE_EXTENSIONS,
  '.svg',
] as const

/**
 * MIME type mapping for image extensions
 */
export const MIME_TYPES: Record<string, string> = {
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
}

/**
 * Get MIME type from file path based on extension
 *
 * @param filepath - Path to the file
 * @returns MIME type string (defaults to 'image/jpeg' for unknown)
 *
 * @example
 * ```ts
 * getMimeType('image.png')   // 'image/png'
 * getMimeType('photo.jpg')   // 'image/jpeg'
 * getMimeType('unknown.xyz') // 'image/jpeg'
 * ```
 */
export function getMimeType(filepath: string): string {
  const ext = path.extname(filepath).toLowerCase()
  return MIME_TYPES[ext] || 'image/jpeg'
}

/**
 * Check if a file is a supported image type
 *
 * @param filepath - Path or filename to check
 * @param includeSvg - Whether to include SVG files (default: false)
 */
export function isSupportedImage(filepath: string, includeSvg: boolean = false): boolean {
  const ext = path.extname(filepath).toLowerCase()
  const extensions = includeSvg ? ALL_IMAGE_EXTENSIONS : SUPPORTED_IMAGE_EXTENSIONS
  return (extensions as readonly string[]).includes(ext)
}

/**
 * Options for finding images
 */
export interface FindImagesOptions {
  /** Extensions to include (default: SUPPORTED_IMAGE_EXTENSIONS) */
  extensions?: string[]
  /** Whether to search recursively (default: true) */
  recursive?: boolean
  /** Skip hidden directories (starting with . or _) (default: true) */
  skipHidden?: boolean
  /** Maximum number of images to return (default: unlimited) */
  limit?: number
}

/**
 * Find all image files in a directory
 *
 * Recursively walks the directory tree and returns paths to all image files.
 *
 * @param baseDir - Directory to search
 * @param options - Search options
 * @returns Array of absolute file paths
 *
 * @example
 * ```ts
 * // Find all images
 * const images = await findImages('assets/images')
 *
 * // Find only PNG files
 * const pngs = await findImages('assets/images', { extensions: ['.png'] })
 *
 * // Find images non-recursively
 * const topLevel = await findImages('assets', { recursive: false })
 * ```
 */
export async function findImages(
  baseDir: string,
  options: FindImagesOptions = {}
): Promise<string[]> {
  const {
    extensions = [...SUPPORTED_IMAGE_EXTENSIONS],
    recursive = true,
    skipHidden = true,
    limit,
  } = options

  const images: string[] = []
  const normalizedExtensions = extensions.map(e => e.toLowerCase())

  const walk = async (dir: string): Promise<void> => {
    // Stop if we've hit the limit
    if (limit && images.length >= limit) return

    let entries
    try {
      entries = readdirSync(dir, { withFileTypes: true })
    } catch {
      // Directory not readable, skip
      return
    }

    for (const entry of entries) {
      // Stop if we've hit the limit
      if (limit && images.length >= limit) return

      const fullPath = path.join(dir, entry.name)

      if (entry.isDirectory()) {
        if (recursive) {
          // Skip hidden directories
          if (skipHidden && (entry.name.startsWith('.') || entry.name.startsWith('_'))) {
            continue
          }
          await walk(fullPath)
        }
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name).toLowerCase()
        if (normalizedExtensions.includes(ext)) {
          images.push(fullPath)
        }
      }
    }
  }

  await walk(baseDir)
  return images
}

/**
 * Find all PNG files in a directory (convenience function)
 *
 * @param baseDir - Directory to search
 * @returns Array of absolute file paths to PNG files
 */
export async function findPngFiles(baseDir: string): Promise<string[]> {
  return findImages(baseDir, { extensions: ['.png'] })
}

/**
 * Result of image file validation
 */
export interface ImageValidationResult {
  valid: boolean
  error?: string
  path?: string
  size?: number
  extension?: string
}

/**
 * Validate an image file exists and is a supported format
 *
 * @param filepath - Path to validate
 * @param options - Validation options
 * @returns Validation result with error details if invalid
 *
 * @example
 * ```ts
 * const result = validateImageFile('image.jpg')
 * if (!result.valid) {
 *   console.error(result.error)
 * }
 * ```
 */
export function validateImageFile(
  filepath: string,
  options: { maxSizeBytes?: number; includeSvg?: boolean } = {}
): ImageValidationResult {
  const { maxSizeBytes, includeSvg = false } = options

  // Check existence
  if (!existsSync(filepath)) {
    return {
      valid: false,
      error: `File not found: ${filepath}`,
    }
  }

  // Check extension
  const ext = path.extname(filepath).toLowerCase()
  const extensions = includeSvg ? ALL_IMAGE_EXTENSIONS : SUPPORTED_IMAGE_EXTENSIONS
  if (!(extensions as readonly string[]).includes(ext)) {
    return {
      valid: false,
      error: `Unsupported image format: ${ext}`,
      extension: ext,
    }
  }

  // Check size
  try {
    const stats = statSync(filepath)
    if (maxSizeBytes && stats.size > maxSizeBytes) {
      return {
        valid: false,
        error: `File too large: ${formatBytes(stats.size)} (max: ${formatBytes(maxSizeBytes)})`,
        size: stats.size,
        extension: ext,
      }
    }

    return {
      valid: true,
      path: filepath,
      size: stats.size,
      extension: ext,
    }
  } catch (error: any) {
    return {
      valid: false,
      error: `Unable to read file: ${error.message}`,
    }
  }
}

/**
 * Format bytes to human-readable string
 */
export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}

/**
 * Get image type from path/filename for categorization
 */
export function getImageType(
  filePath: string
): 'og' | 'infographic' | 'slide' | 'icon' | 'cover' | 'chart' | 'other' {
  const lower = filePath.toLowerCase()
  if (lower.includes('-og-') || lower.includes('/og/') || lower.includes('-og.')) return 'og'
  if (lower.includes('-infographic-') || lower.includes('/infographics/')) return 'infographic'
  if (lower.includes('-slide-') || lower.includes('/slides/')) return 'slide'
  if (lower.includes('/icons/') || lower.includes('favicon') || lower.includes('-icon')) return 'icon'
  if (lower.includes('/cover/') || lower.includes('book-cover')) return 'cover'
  if (lower.includes('chart') || lower.includes('graph') || lower.includes('diagram')) return 'chart'
  return 'other'
}

/**
 * Extract style from filename
 */
export function getImageStyle(filename: string): string | undefined {
  if (filename.includes('-academic')) return 'black and white academic'
  if (filename.includes('-retro')) return 'colorful retro-futuristic'
  return undefined
}

/**
 * Calculate aspect ratio string from dimensions
 */
export function getAspectRatio(width: number, height: number): string {
  const gcd = (a: number, b: number): number => (b === 0 ? a : gcd(b, a % b))
  const divisor = gcd(width, height)
  const w = width / divisor
  const h = height / divisor

  // Simplify common ratios
  const ratio = w / h
  if (Math.abs(ratio - 16 / 9) < 0.05) return '16:9'
  if (Math.abs(ratio - 4 / 3) < 0.05) return '4:3'
  if (Math.abs(ratio - 1) < 0.05) return '1:1'
  if (Math.abs(ratio - 3 / 4) < 0.05) return '3:4'
  if (Math.abs(ratio - 9 / 16) < 0.05) return '9:16'

  return `${w}:${h}`
}
