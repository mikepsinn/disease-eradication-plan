/**
 * Exiftool Utilities - Centralized EXIF metadata operations
 *
 * Consolidates EXIF read/write operations across image scripts:
 * - edit-image.ts
 * - fix-image-text.ts
 * - generate-image-index.ts
 * - extract-image-text.ts
 */

import { exec } from 'child_process'
import { promisify } from 'util'
import fs from 'fs/promises'
import path from 'path'

const execAsync = promisify(exec)

/**
 * Structured metadata stored in EXIF UserComment as JSON
 */
export interface ImageExifMetadata {
  /** Image title */
  title?: string
  /** Image description */
  description?: string
  /** Keywords/tags */
  keywords?: string[]
  /** OCR transcript of visible text */
  transcript?: string
  /** Timestamp when transcript was extracted */
  transcriptExtractedAt?: string
  /** Original generation prompt */
  generationPrompt?: string
  /** AI-inferred prompt that could have generated this image */
  inferredPrompt?: string
  /** List of issues/problems identified in the image */
  imageIssues?: string[]
  /** Suggestions for improving the generation prompt */
  promptImprovements?: string[]
  /** Timestamp when metadata was created */
  metadataCreatedAt?: string
  /** Any additional custom fields */
  [key: string]: unknown
}

/**
 * Raw EXIF fields returned by exiftool
 */
export interface RawExifData {
  Title?: string
  Description?: string
  Keywords?: string | string[]
  UserComment?: string
  Author?: string
  Artist?: string
  Creator?: string
  Copyright?: string
  DateTimeOriginal?: string
  CreateDate?: string
  [key: string]: unknown
}

/**
 * Check if exiftool is available on the system
 */
export async function isExiftoolAvailable(): Promise<boolean> {
  try {
    await execAsync('exiftool -ver')
    return true
  } catch (error) {
    console.error('exiftool not available:', error)
    return false
  }
}

/**
 * Parse UserComment field that may contain JSON metadata
 */
export function parseUserCommentJson(userComment: string | undefined): ImageExifMetadata | null {
  if (!userComment) return null

  try {
    return JSON.parse(userComment) as ImageExifMetadata
  } catch {
    // Not JSON, return null
    return null
  }
}

/**
 * Read image metadata using exiftool
 *
 * Returns both standard EXIF fields and parsed UserComment JSON.
 *
 * @param filepath - Path to the image file
 * @param fields - Optional specific fields to request (default: common fields)
 * @returns Combined metadata object or null if unable to read
 *
 * @example
 * ```ts
 * const meta = await readImageMetadata('image.jpg')
 * console.log(meta?.transcript)
 * console.log(meta?.generationPrompt)
 * ```
 */
export async function readImageMetadata(
  filepath: string,
  fields?: string[]
): Promise<ImageExifMetadata | null> {
  const defaultFields = [
    'UserComment',
    'Title',
    'Description',
    'Keywords',
    'Author',
    'Artist',
    'Creator',
    'Copyright',
    'DateTimeOriginal',
    'CreateDate',
  ]

  const requestedFields = fields || defaultFields
  const fieldArgs = requestedFields.map(f => `-${f}`).join(' ')

  try {
    const { stdout } = await execAsync(
      `exiftool -json ${fieldArgs} "${filepath}"`,
      { maxBuffer: 1024 * 1024 }
    )

    const data: RawExifData = JSON.parse(stdout)[0]
    if (!data) return null

    const result: ImageExifMetadata = {}

    // Parse UserComment JSON first (takes precedence for overlapping fields)
    if (data.UserComment) {
      const parsed = parseUserCommentJson(data.UserComment)
      if (parsed) {
        Object.assign(result, parsed)
      }
    }

    // Add standard EXIF fields (don't overwrite if already set from UserComment)
    if (data.Title && !result.title) result.title = data.Title
    if (data.Description && !result.description) result.description = data.Description
    if (data.Keywords && !result.keywords) {
      result.keywords = Array.isArray(data.Keywords) ? data.Keywords : [data.Keywords]
    }

    return Object.keys(result).length > 0 ? result : null
  } catch (error) {
    console.error(`Failed to read metadata from ${filepath}:`, error)
    throw error
  }
}

/**
 * Write metadata to image using exiftool
 *
 * Stores structured metadata in UserComment as JSON to preserve complex data.
 *
 * @param filepath - Path to the image file
 * @param metadata - Metadata to write
 * @param options - Write options
 *
 * @example
 * ```ts
 * await writeImageMetadata('image.jpg', {
 *   transcript: 'Extracted text here',
 *   inferredPrompt: 'A diagram showing...',
 *   imageIssues: ['text is blurry'],
 * })
 * ```
 */
export async function writeImageMetadata(
  filepath: string,
  metadata: ImageExifMetadata,
  options: { mergeExisting?: boolean } = {}
): Promise<void> {
  const { mergeExisting = true } = options

  // Read existing metadata if merging
  let existingData: ImageExifMetadata = {}
  if (mergeExisting) {
    const existing = await readImageMetadata(filepath)
    if (existing) {
      existingData = existing
    }
  }

  // Merge metadata
  const newMetadata: ImageExifMetadata = {
    ...existingData,
    ...metadata,
  }

  // Add timestamp
  if (!newMetadata.metadataCreatedAt) {
    newMetadata.metadataCreatedAt = new Date().toISOString()
  }

  // Write to temp file and use exiftool's -@ argfile to avoid shell escaping issues
  const tempFile = path.join(
    path.dirname(filepath),
    `.metadata-temp-${Date.now()}.json`
  )
  const argFile = path.join(
    path.dirname(filepath),
    `.exiftool-args-${Date.now()}.txt`
  )

  await fs.writeFile(tempFile, JSON.stringify(newMetadata))

  // Create argfile with the command arguments
  const args = [
    '-overwrite_original',
    `-UserComment<=${tempFile}`,
    filepath,
  ]
  await fs.writeFile(argFile, args.join('\n'))

  try {
    const { stdout, stderr } = await execAsync(
      `exiftool -@ "${argFile}"`,
      { maxBuffer: 1024 * 1024 }
    )
    if (stderr) {
      console.error(`exiftool stderr for ${filepath}:`, stderr)
    }
    if (!stdout.includes('1 image files updated')) {
      throw new Error(`exiftool did not update file. stdout: ${stdout}`)
    }
  } finally {
    // Clean up temp files
    await fs.unlink(tempFile)
    await fs.unlink(argFile)
  }
}

/**
 * Check if image already has transcript metadata
 */
export async function hasTranscript(filepath: string): Promise<boolean> {
  const metadata = await readImageMetadata(filepath, ['UserComment'])
  return !!metadata?.transcript
}

/**
 * Get raw exiftool output as JSON
 *
 * Use this when you need the full raw output without any parsing.
 *
 * @param filepath - Path to the image file
 * @param fields - Optional specific fields to request
 */
export async function getRawExiftoolOutput(
  filepath: string,
  fields?: string[]
): Promise<RawExifData | null> {
  const fieldArgs = fields ? fields.map(f => `-${f}`).join(' ') : '-all'

  const { stdout } = await execAsync(
    `exiftool -json ${fieldArgs} "${filepath}"`,
    { maxBuffer: 1024 * 1024 }
  )
  return JSON.parse(stdout)[0] || null
}
