/**
 * Update all existing images with rich SEO metadata
 *
 * This script finds all images in the assets directory and adds
 * EXIF, IPTC, and XMP metadata for better search engine discoverability.
 *
 * Usage:
 *   npx tsx scripts/images/update-image-metadata.ts [--dry-run]
 *
 * Options:
 *   --dry-run    Show what would be updated without making changes
 *   --verbose    Show detailed output for each image
 */

import { glob } from 'glob'
import path from 'path'
import {
  addImageMetadata,
  extractKeywordsFromText,
  ImageMetadata,
  DEFAULT_METADATA,
} from '../lib/gemini-images.js'

// Configuration
const ASSETS_DIR = 'assets'
const IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'webp']

// Category keywords based on directory structure
const CATEGORY_KEYWORDS: Record<string, string[]> = {
  'infographics': ['infographic', 'data visualization', 'statistics', 'research'],
  'figures': ['figure', 'diagram', 'chart', 'illustration'],
  'icons': ['icon', 'logo', 'branding'],
  'og-images': ['social media', 'open graph', 'sharing'],
  'knowledge': ['research', 'science', 'academic', 'study'],
  'economics': ['economics', 'finance', 'cost-benefit', 'ROI'],
  'dfda': ['FDA', 'drug approval', 'clinical trials', 'healthcare'],
  'treaty': ['treaty', 'policy', 'international', 'agreement'],
  'wishocracy': ['democracy', 'voting', 'governance', 'preference aggregation'],
  'iab': ['incentive alignment', 'bonds', 'political economy'],
  'health': ['health', 'medicine', 'disease', 'treatment'],
  'military': ['military', 'defense', 'spending', 'budget'],
}

// Site-wide keywords that apply to all images
const GLOBAL_KEYWORDS = [
  'War on Disease',
  'medical research',
  'public health',
  'health policy',
]

interface ProcessResult {
  path: string
  status: 'updated' | 'skipped' | 'error'
  message?: string
}

/**
 * Extract metadata from image path and filename
 */
function extractMetadataFromPath(imagePath: string): ImageMetadata {
  const relativePath = path.relative(process.cwd(), imagePath)
  const dirname = path.dirname(relativePath)
  const filename = path.basename(imagePath, path.extname(imagePath))

  // Convert filename to title (kebab-case to Title Case)
  const title = filename
    .replace(/[-_]/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase())
    .replace(/\s+/g, ' ')
    .trim()

  // Build keywords from path components and filename
  const pathParts = dirname.split(/[/\\]/).filter(Boolean)
  const keywords: string[] = [...GLOBAL_KEYWORDS]

  // Add category keywords based on directory
  for (const part of pathParts) {
    const partLower = part.toLowerCase()
    if (CATEGORY_KEYWORDS[partLower]) {
      keywords.push(...CATEGORY_KEYWORDS[partLower])
    }
    // Also add the directory name itself as a keyword
    if (partLower !== 'assets' && partLower.length > 2) {
      keywords.push(partLower.replace(/-/g, ' '))
    }
  }

  // Extract keywords from filename
  const filenameKeywords = extractKeywordsFromText(filename.replace(/[-_]/g, ' '))
  keywords.push(...filenameKeywords)

  // Deduplicate keywords
  const uniqueKeywords = [...new Set(keywords.map(k => k.toLowerCase()))]
    .slice(0, 15) // Limit to 15 keywords

  // Build description
  const description = `${title} - Part of the War on Disease initiative for global health research and policy reform. ${dirname.includes('economics') ? 'Economic analysis and cost-benefit data.' : ''} ${dirname.includes('treaty') ? 'Related to the 1% Treaty for redirecting military spending to medical research.' : ''}`.trim()

  // Determine category from path
  let category = 'Health/Medical Research'
  if (dirname.includes('economics')) category = 'Economics/Health Economics'
  if (dirname.includes('treaty')) category = 'Policy/International Relations'
  if (dirname.includes('wishocracy')) category = 'Governance/Democracy'
  if (dirname.includes('iab')) category = 'Political Economy/Finance'

  return {
    title,
    description,
    keywords: uniqueKeywords,
    category,
    sourceUrl: `https://WarOnDisease.org/${relativePath.replace(/\\/g, '/')}`,
  }
}

/**
 * Process a single image
 */
async function processImage(
  imagePath: string,
  dryRun: boolean,
  verbose: boolean
): Promise<ProcessResult> {
  try {
    const metadata = extractMetadataFromPath(imagePath)

    if (verbose) {
      console.log(`\n  Title: ${metadata.title}`)
      console.log(`  Keywords: ${metadata.keywords?.slice(0, 5).join(', ')}...`)
      console.log(`  Category: ${metadata.category}`)
    }

    if (dryRun) {
      return { path: imagePath, status: 'skipped', message: 'Dry run' }
    }

    await addImageMetadata(imagePath, metadata)
    return { path: imagePath, status: 'updated' }
  } catch (error: any) {
    return {
      path: imagePath,
      status: 'error',
      message: error.message || String(error),
    }
  }
}

/**
 * Main function
 */
async function main() {
  const args = process.argv.slice(2)
  const dryRun = args.includes('--dry-run')
  const verbose = args.includes('--verbose')

  console.log('=' .repeat(70))
  console.log('Image Metadata Updater')
  console.log('=' .repeat(70))
  console.log(`Mode: ${dryRun ? 'DRY RUN (no changes will be made)' : 'LIVE'}`)
  console.log(`Assets directory: ${ASSETS_DIR}`)
  console.log('')

  // Find all images
  const patterns = IMAGE_EXTENSIONS.map(ext => `${ASSETS_DIR}/**/*.${ext}`)
  const allImages: string[] = []

  for (const pattern of patterns) {
    const matches = await glob(pattern, { nocase: true })
    allImages.push(...matches)
  }

  // Filter out node_modules, .venv, etc.
  const images = allImages.filter(img =>
    !img.includes('node_modules') &&
    !img.includes('.venv') &&
    !img.includes('_build_temp')
  )

  console.log(`Found ${images.length} images to process`)
  console.log('-'.repeat(70))

  const results: ProcessResult[] = []
  let processed = 0

  for (const imagePath of images) {
    processed++
    const shortPath = path.relative(process.cwd(), imagePath)
    process.stdout.write(`[${processed}/${images.length}] ${shortPath}...`)

    const result = await processImage(imagePath, dryRun, verbose)
    results.push(result)

    if (result.status === 'updated') {
      console.log(' OK')
    } else if (result.status === 'skipped') {
      console.log(' SKIPPED')
    } else {
      console.log(` ERROR: ${result.message}`)
    }
  }

  // Summary
  console.log('')
  console.log('='.repeat(70))
  console.log('Summary')
  console.log('='.repeat(70))

  const updated = results.filter(r => r.status === 'updated').length
  const skipped = results.filter(r => r.status === 'skipped').length
  const errors = results.filter(r => r.status === 'error').length

  console.log(`Updated: ${updated}`)
  console.log(`Skipped: ${skipped}`)
  console.log(`Errors:  ${errors}`)

  if (errors > 0) {
    console.log('')
    console.log('Errors:')
    for (const result of results.filter(r => r.status === 'error')) {
      console.log(`  - ${result.path}: ${result.message}`)
    }
  }

  if (dryRun) {
    console.log('')
    console.log('This was a dry run. Run without --dry-run to apply changes.')
  }

  console.log('')
  console.log('Default metadata applied to all images:')
  console.log(`  Author: ${DEFAULT_METADATA.author}`)
  console.log(`  Copyright: ${DEFAULT_METADATA.copyright}`)
  console.log(`  License: ${DEFAULT_METADATA.license}`)
  console.log(`  Website: ${DEFAULT_METADATA.website}`)
}

main().catch(error => {
  console.error('Fatal error:', error)
  process.exit(1)
})
