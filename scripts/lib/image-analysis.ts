/**
 * Image Analysis - Shared prompts and functions for Gemini image analysis
 *
 * Consolidates analysis logic across:
 * - extract-image-text.ts
 * - gemini-images.ts (saveImage)
 * - generate-image-index.ts (--fill mode)
 */

import fs from 'fs/promises'
import { generateGeminiVisionContent, extractJsonFromResponse } from './llm'
import { getMimeType } from './image-file-utils'

/**
 * Standard prompts for image analysis
 */
export const ANALYSIS_PROMPTS = {
  /**
   * Extract text only (OCR) - fast, minimal output
   */
  EXTRACT_TEXT: `Extract ALL visible text from this image. Include:
- Titles and headings
- Labels on charts/diagrams
- Axis labels and values
- Legends and captions
- Any numbers, statistics, or data points
- Footer text or watermarks

Return ONLY the extracted text, preserving the logical reading order.
If there is no readable text in the image, respond with: [NO TEXT]

Do not describe the image - only extract the actual text content.`,

  /**
   * Full analysis - text extraction + quality assessment + prompt inference
   */
  FULL_ANALYSIS: `Analyze this AI-generated image and return a JSON object with these fields:

1. "transcript": Extract ALL visible text from the image (titles, labels, captions, numbers). If no text, use "[NO TEXT]"

2. "inferredPrompt": Write a detailed prompt that could have generated this image. Be specific about style, composition, colors, subjects, and any text/data shown.

3. "imageIssues": Array of problems you notice (e.g., "text is blurry", "chart labels are cut off", "colors lack contrast", "layout is cluttered", "text has spelling errors", "data is hard to read")

4. "promptImprovements": Array of specific suggestions to improve the generation prompt (e.g., "add 'high contrast' for readability", "specify exact font size for labels", "request more whitespace between elements")

Return ONLY valid JSON, no markdown code blocks.`,

  /**
   * Book-focused analysis - for categorizing images by chapter relevance
   */
  BOOK_ANALYSIS: `Analyze this image for a book about redirecting military spending to medical research (a "1% treaty").

Provide:
1. DESCRIPTION: Detailed description of what the image shows (2-3 sentences)
2. KEYWORDS: 5-10 relevant keywords/tags (comma-separated)
3. CHAPTERS: Which book chapters would benefit from this image? Consider:
   - Problem chapters: the-daily-massacre, cost-of-war, cost-of-disease, fda-is-unsafe-and-ineffective, nih-spent-1-trillion-eradicating-0-diseases, unrepresentative-democracy, regulatory-capture, the-119-trillion-death-toilet
   - Solution chapters: 1-percent-treaty, wishocracy, dfda, dih, positron, war-on-disease
   - Proof chapters: historical-precedents, economics, futures
   - Strategy chapters: global-referendum, viral-marketing, legislation-package, roadmap
4. PRIMARY_USE: Which 1-2 chapters should use this as a PRIMARY/key visual?

Format your response EXACTLY as:
DESCRIPTION: [your description]
KEYWORDS: [keyword1, keyword2, keyword3, ...]
CHAPTERS: [chapter1.qmd, chapter2.qmd, ...]
PRIMARY_USE: [chapter1.qmd]`,
}

/**
 * Result from full image analysis
 */
export interface ImageAnalysisResult {
  /** Extracted text (OCR) */
  transcript?: string
  /** AI-inferred prompt that could generate this image */
  inferredPrompt?: string
  /** Issues found in the image */
  imageIssues?: string[]
  /** Suggestions for improving the generation prompt */
  promptImprovements?: string[]
}

/**
 * Result from book-focused analysis
 */
export interface BookAnalysisResult {
  description: string
  keywords: string[]
  suggestedChapters: string[]
  primaryChapter?: string
}

/**
 * Extract text from an image using OCR
 *
 * @param filepath - Path to the image file
 * @returns Extracted text or '[NO TEXT]' if no text found
 *
 * @example
 * ```ts
 * const text = await extractImageText('chart.png')
 * console.log(text) // "Revenue: $1.2M\nGrowth: 15%"
 * ```
 */
export async function extractImageText(filepath: string): Promise<string> {
  const imageBuffer = await fs.readFile(filepath)
  const base64Image = imageBuffer.toString('base64')
  const mimeType = getMimeType(filepath)

  const result = await generateGeminiVisionContent(
    ANALYSIS_PROMPTS.EXTRACT_TEXT,
    base64Image,
    mimeType
  )

  return result.trim() || '[NO TEXT]'
}

/**
 * Perform full analysis of an image
 *
 * Returns transcript, inferred prompt, issues, and improvement suggestions.
 *
 * @param filepath - Path to the image file
 * @returns Analysis result object
 *
 * @example
 * ```ts
 * const analysis = await analyzeImage('infographic.png')
 * console.log(analysis.transcript)
 * console.log(analysis.imageIssues)
 * ```
 */
export async function analyzeImage(filepath: string): Promise<ImageAnalysisResult> {
  const imageBuffer = await fs.readFile(filepath)
  const base64Image = imageBuffer.toString('base64')
  const mimeType = getMimeType(filepath)

  const response = await generateGeminiVisionContent(
    ANALYSIS_PROMPTS.FULL_ANALYSIS,
    base64Image,
    mimeType
  )

  try {
    const analysis = extractJsonFromResponse(response, 'image analysis') as {
      transcript?: string
      inferredPrompt?: string
      imageIssues?: string[]
      promptImprovements?: string[]
    }

    const result: ImageAnalysisResult = {}

    if (analysis.transcript && analysis.transcript !== '[NO TEXT]') {
      result.transcript = analysis.transcript
    }
    if (analysis.inferredPrompt) {
      result.inferredPrompt = analysis.inferredPrompt
    }
    if (analysis.imageIssues && analysis.imageIssues.length > 0) {
      result.imageIssues = analysis.imageIssues
    }
    if (analysis.promptImprovements && analysis.promptImprovements.length > 0) {
      result.promptImprovements = analysis.promptImprovements
    }

    return result
  } catch {
    // Fallback: treat entire response as transcript
    if (response && response.trim() !== '[NO TEXT]') {
      return { transcript: response.trim() }
    }
    return {}
  }
}

/**
 * Analyze image for book chapter relevance
 *
 * @param filepath - Path to the image file
 * @returns Book analysis result with description, keywords, and chapter suggestions
 */
export async function analyzeImageForBook(filepath: string): Promise<BookAnalysisResult> {
  const imageBuffer = await fs.readFile(filepath)
  const base64Image = imageBuffer.toString('base64')
  const mimeType = getMimeType(filepath)

  const responseText = await generateGeminiVisionContent(
    ANALYSIS_PROMPTS.BOOK_ANALYSIS,
    base64Image,
    mimeType
  )

  // Parse structured response
  const descMatch = responseText.match(/DESCRIPTION:\s*(.+?)(?=\n[A-Z]+:|$)/s)
  const keywordsMatch = responseText.match(/KEYWORDS:\s*(.+?)(?=\n[A-Z]+:|$)/s)
  const chaptersMatch = responseText.match(/CHAPTERS:\s*(.+?)(?=\n[A-Z]+:|$)/s)
  const primaryMatch = responseText.match(/PRIMARY_USE:\s*(.+?)(?=\n[A-Z]+:|$)/s)

  // Clean up keywords
  let keywords: string[] = []
  if (keywordsMatch) {
    const keywordText = keywordsMatch[1].replace(/[\[\]]/g, '')
    keywords = keywordText
      .split(',')
      .map(k => k.trim())
      .filter(Boolean)
  }

  // Clean up chapters
  let chapters: string[] = []
  if (chaptersMatch) {
    const chapterText = chaptersMatch[1].replace(/[\[\]]/g, '')
    chapters = chapterText
      .split(',')
      .map(c => c.trim())
      .filter(Boolean)
  }

  // Clean up primary chapter
  let primaryChapter: string | undefined
  if (primaryMatch) {
    primaryChapter = primaryMatch[1].replace(/[\[\]]/g, '').trim() || undefined
  }

  return {
    description: descMatch ? descMatch[1].trim() : 'No description generated',
    keywords,
    suggestedChapters: chapters,
    primaryChapter,
  }
}

/**
 * Analyze image from base64 data (for use in pipelines that already have the image loaded)
 *
 * @param base64Image - Base64-encoded image data
 * @param mimeType - MIME type of the image
 * @returns Analysis result object
 */
export async function analyzeImageFromBase64(
  base64Image: string,
  mimeType: string
): Promise<ImageAnalysisResult> {
  const response = await generateGeminiVisionContent(
    ANALYSIS_PROMPTS.FULL_ANALYSIS,
    base64Image,
    mimeType
  )

  try {
    const analysis = extractJsonFromResponse(response, 'image analysis') as {
      transcript?: string
      inferredPrompt?: string
      imageIssues?: string[]
      promptImprovements?: string[]
    }

    const result: ImageAnalysisResult = {}

    if (analysis.transcript && analysis.transcript !== '[NO TEXT]') {
      result.transcript = analysis.transcript
    }
    if (analysis.inferredPrompt) {
      result.inferredPrompt = analysis.inferredPrompt
    }
    if (analysis.imageIssues && analysis.imageIssues.length > 0) {
      result.imageIssues = analysis.imageIssues
    }
    if (analysis.promptImprovements && analysis.promptImprovements.length > 0) {
      result.promptImprovements = analysis.promptImprovements
    }

    return result
  } catch {
    // Fallback: treat entire response as transcript
    if (response && response.trim() !== '[NO TEXT]') {
      return { transcript: response.trim() }
    }
    return {}
  }
}
