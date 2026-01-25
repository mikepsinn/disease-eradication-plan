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

  /**
   * Complete metadata generation - comprehensive metadata for SEO, social media, presentations, and accessibility
   */
  COMPLETE_METADATA: `Analyze this image comprehensively and generate metadata for SEO, social media, presentations, and accessibility.

This image is from a book about redirecting 1% of military spending to medical research (the "1% Treaty" / "War on Disease" initiative).

Return a JSON object with ALL these fields:

## Core Metadata
- "title": Concise descriptive title (5-10 words), title case
- "description": Detailed description (2-3 sentences) of the CONTENT and data shown. Never mention visual style (e.g., don't say "vintage-style", "retro illustration", "academic diagram"). Focus only on what information the image conveys.
- "keywords": Array of 5-10 relevant tags for search
- "transcript": ALL visible text extracted (titles, labels, numbers). Use "[NO TEXT]" if none

## Quality Assessment (use these rubrics strictly - be critical, not generous)

qualityScore rubric (most images should be 3-4, reserve 5 for truly exceptional):
- 5: Publication-ready. Sharp text, clear hierarchy, professional polish, no issues.
- 4: Minor issues. Small text in one area, slightly busy, or one element could be clearer.
- 3: Usable but flawed. Multiple readability issues, inconsistent styling, or amateur feel.
- 2: Needs significant work. Hard to read, cluttered, poor contrast, or multiple errors.
- 1: Unusable. Illegible text, broken layout, or fundamentally fails to communicate.

standaloneScore rubric (can someone understand this WITHOUT reading the chapter?):
- 5: Fully self-explanatory. Clear title, labeled axes, context provided, anyone gets it.
- 4: Mostly clear. Minor context helps but main message is obvious.
- 3: Needs some context. Key terms or references require chapter knowledge.
- 2: Context-dependent. Only makes sense if you've read surrounding material.
- 1: Incomprehensible alone. Pure illustration that means nothing without text.

- "qualityScore": 1-5 per rubric above
- "qualityIssues": Array of specific problems (e.g., "text too small", "low contrast", "cluttered layout", "spelling errors")
- "standaloneScore": 1-5 per rubric above

## Social Media (CRITICAL: Match this exact voice)
Channel the deadpan absurdism of Philomena Cunk, Jack Handy's "Deep Thoughts", and Kurt Vonnegut. The tone is: darkly funny, resigned-but-not-defeated, pointing out obvious absurdities that everyone ignores.

GOOD examples (match this tone):
- "The FDA takes 12 years to approve a drug. The disease didn't get the memo."
- "We've solved the problem of killing people efficiently. Now if only we could figure out keeping them alive."
- "Fun fact: dying from a preventable disease costs nothing. Preventing it is apparently too expensive."
- "24,000 people died today from causes we know how to fix. Anyway, here's a graph about it."
- "Scientists discovered a cure. Then they discovered paperwork."

BAD examples (never write like this):
- "This powerful visualization shows the importance of..." (too corporate)
- "Check out this amazing infographic about..." (too enthusiastic)
- "Did you know that research shows..." (too educational)
- "We must take action to..." (too earnest)

- "canShareStandalone": boolean - does it make sense shared independently?
- "socialCaption": 1-2 sentences + hashtags. Deadpan punchline, not TED talk energy. End with https://WarOnDisease.org
- "twitterText": Under 280 chars. One dark joke + https://WarOnDisease.org (count the URL as 23 chars for Twitter's link shortening)
- "linkedInText": Wry gallows humor that makes executives nervous-laugh. End with https://WarOnDisease.org
- "targetPlatforms": Array from ["twitter", "linkedin", "instagram", "facebook", "presentation"]

## Presentations
- "speakerNotes": What a presenter should SAY when showing this (2-3 sentences, conversational)
- "talkingPoints": Array of 2-4 bullet points for presenter
- "audienceLevel": One of "general", "policymaker", "researcher", "investor", "healthcare"

## Accessibility & Tone
- "altText": Screen reader description (focus on meaning, not appearance)
- "emotionalTone": One of "alarming", "hopeful", "informative", "urgent", "inspiring", "neutral"
- "callToAction": What should viewer do after seeing this? (e.g., "Share to raise awareness", "Contact representatives", "Learn more")

## Data Integrity
- "dataFreshness": One of "current", "needs-update", "timeless" (is the data/statistic current?)
- "dataSources": Array of data sources if identifiable from the image
- "factCheckNotes": Any caveats, verification needs, or context required

## Prompt Leakage Detection
Check if any AI generation prompt text accidentally appears in the image. Common leaks include:
- Style words: "retro", "academic", "scientific illustration", "visualization", "infographic"
- Technical terms: "high contrast", "minimalist", "detailed", "professional"
- Instructions: "diagram showing", "chart of", "illustration of"
- Figure numbers: "Figure 1", "Figure 2", "Fig. 1" etc. (these should be added by the document system, not embedded in images)

- "promptLeakageDetected": boolean - does visible text contain likely prompt artifacts OR embedded figure numbers?
- "promptLeakageText": Array of specific leaked text found (e.g., ["scientific illustration", "Figure 1"])
- "promptLeakageRepairPrompt": If leakage detected, a specific prompt to fix it (e.g., "Remove the text 'Figure 1' from the top of the image")

Return ONLY valid JSON, no markdown code blocks.`,
}

/**
 * Result from complete metadata generation
 */
export interface CompleteMetadataResult {
  // Core
  /** SEO-friendly title (5-10 words) */
  title?: string
  /** Detailed description (2-3 sentences) */
  description?: string
  /** Search keywords/tags */
  keywords?: string[]
  /** Extracted text (OCR) */
  transcript?: string

  // Quality
  /** Quality rating 1-5 */
  qualityScore?: number
  /** Specific quality issues */
  qualityIssues?: string[]
  /** Standalone comprehension score 1-5 */
  standaloneScore?: number

  // Social Media
  /** Can be shared without chapter context */
  canShareStandalone?: boolean
  /** Ready-to-post social caption with hashtags */
  socialCaption?: string
  /** Tweet-ready text (under 280 chars) */
  twitterText?: string
  /** LinkedIn-ready text */
  linkedInText?: string
  /** Recommended platforms */
  targetPlatforms?: string[]

  // Presentations
  /** What presenter should say */
  speakerNotes?: string
  /** Bullet points for presenter */
  talkingPoints?: string[]
  /** Target audience level */
  audienceLevel?: string

  // Accessibility
  /** Screen reader description */
  altText?: string
  /** Emotional tone */
  emotionalTone?: string
  /** Suggested call to action */
  callToAction?: string

  // Data Integrity
  /** Data freshness status */
  dataFreshness?: string
  /** Original data sources */
  dataSources?: string[]
  /** Fact-check notes or caveats */
  factCheckNotes?: string

  // Prompt Leakage Detection
  /** Was prompt leakage detected in image text? */
  promptLeakageDetected?: boolean
  /** Specific leaked text found */
  promptLeakageText?: string[]
  /** Repair prompt to fix the leakage */
  promptLeakageRepairPrompt?: string
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

/**
 * Generate complete metadata for an image
 *
 * Generates comprehensive metadata including SEO, social media, presentation,
 * accessibility, and data integrity fields in a single API call.
 *
 * @param filepath - Path to the image file
 * @returns Complete metadata result with all fields
 *
 * @example
 * ```ts
 * const metadata = await generateCompleteMetadata('chart.png')
 * console.log(metadata.title) // "Global Health Spending Comparison"
 * console.log(metadata.twitterText) // "Did you know? Military spending..."
 * console.log(metadata.qualityScore) // 4
 * ```
 */
export async function generateCompleteMetadata(
  filepath: string
): Promise<CompleteMetadataResult> {
  const imageBuffer = await fs.readFile(filepath)
  const base64Image = imageBuffer.toString('base64')
  const mimeType = getMimeType(filepath)

  const response = await generateGeminiVisionContent(
    ANALYSIS_PROMPTS.COMPLETE_METADATA,
    base64Image,
    mimeType
  )

  const metadata = extractJsonFromResponse(response, 'complete metadata') as CompleteMetadataResult

  const result: CompleteMetadataResult = {}

  // Core metadata
  if (metadata.title) result.title = metadata.title
  if (metadata.description) result.description = metadata.description
  if (metadata.keywords?.length) result.keywords = metadata.keywords
  if (metadata.transcript && metadata.transcript !== '[NO TEXT]') {
    result.transcript = metadata.transcript
  }

  // Quality assessment
  if (metadata.qualityScore) result.qualityScore = metadata.qualityScore
  if (metadata.qualityIssues?.length) result.qualityIssues = metadata.qualityIssues
  if (metadata.standaloneScore) result.standaloneScore = metadata.standaloneScore

  // Social media
  if (typeof metadata.canShareStandalone === 'boolean') {
    result.canShareStandalone = metadata.canShareStandalone
  }
  if (metadata.socialCaption) result.socialCaption = metadata.socialCaption
  if (metadata.twitterText) result.twitterText = metadata.twitterText
  if (metadata.linkedInText) result.linkedInText = metadata.linkedInText
  if (metadata.targetPlatforms?.length) result.targetPlatforms = metadata.targetPlatforms

  // Presentations
  if (metadata.speakerNotes) result.speakerNotes = metadata.speakerNotes
  if (metadata.talkingPoints?.length) result.talkingPoints = metadata.talkingPoints
  if (metadata.audienceLevel) result.audienceLevel = metadata.audienceLevel

  // Accessibility & Tone
  if (metadata.altText) result.altText = metadata.altText
  if (metadata.emotionalTone) result.emotionalTone = metadata.emotionalTone
  if (metadata.callToAction) result.callToAction = metadata.callToAction

  // Data Integrity
  if (metadata.dataFreshness) result.dataFreshness = metadata.dataFreshness
  if (metadata.dataSources?.length) result.dataSources = metadata.dataSources
  if (metadata.factCheckNotes) result.factCheckNotes = metadata.factCheckNotes

  // Prompt Leakage Detection
  if (typeof metadata.promptLeakageDetected === 'boolean') {
    result.promptLeakageDetected = metadata.promptLeakageDetected
  }
  if (metadata.promptLeakageText?.length) {
    result.promptLeakageText = metadata.promptLeakageText
  }
  if (metadata.promptLeakageRepairPrompt) {
    result.promptLeakageRepairPrompt = metadata.promptLeakageRepairPrompt
  }

  return result
}
