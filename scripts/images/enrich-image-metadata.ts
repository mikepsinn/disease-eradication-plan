#!/usr/bin/env tsx
/**
 * Enrich Image Metadata - Comprehensive metadata generation
 *
 * Generates ALL metadata for images in a single API call:
 * - Core: title, description, keywords, transcript
 * - Quality: qualityScore, qualityIssues, standaloneScore
 * - Social: canShareStandalone, socialCaption, twitterText, linkedInText, targetPlatforms
 * - Presentations: speakerNotes, talkingPoints, audienceLevel
 * - Accessibility: altText, emotionalTone, callToAction
 * - Data: dataFreshness, dataSources, factCheckNotes
 *
 * Usage:
 *   npx tsx scripts/images/enrich-image-metadata.ts              # Fill missing metadata
 *   npx tsx scripts/images/enrich-image-metadata.ts --all        # Regenerate all metadata
 *   npx tsx scripts/images/enrich-image-metadata.ts --dry-run    # Preview without saving
 *   npx tsx scripts/images/enrich-image-metadata.ts --limit 10   # Process 10 images
 *   npx tsx scripts/images/enrich-image-metadata.ts --path <dir> # Specific directory
 */

import { existsSync } from 'fs'
import path from 'path'

// Shared utilities
import { findImages } from '../lib/image-file-utils'
import { readImageMetadata, writeImageMetadata } from '../lib/exiftool-utils'
import { generateCompleteMetadata, CompleteMetadataResult } from '../lib/image-analysis'
import { parseCommonArgs, printHeader, printSummary } from '../lib/cli-utils'
import { updateImageInIndex, syncIndex } from './generate-image-index'

const ASSETS_DIR = path.join(process.cwd(), 'assets', 'images')

// All metadata fields we track
const ALL_FIELDS = [
  // Core
  'title', 'description', 'keywords', 'transcript',
  // Quality
  'qualityScore', 'qualityIssues', 'standaloneScore',
  // Social
  'canShareStandalone', 'socialCaption', 'twitterText', 'linkedInText', 'targetPlatforms',
  // Presentations
  'speakerNotes', 'talkingPoints', 'audienceLevel',
  // Accessibility
  'altText', 'emotionalTone', 'callToAction',
  // Data
  'dataFreshness', 'dataSources', 'factCheckNotes',
] as const

interface EnrichmentResult {
  path: string
  generated: CompleteMetadataResult
  fieldsAdded: string[]
}

/**
 * Check which metadata fields are missing for an image
 */
async function getMissingFields(imagePath: string): Promise<string[]> {
  const missing: string[] = []

  const metadata = await readImageMetadata(imagePath)
  if (!metadata) {
    return [...ALL_FIELDS]
  }

  for (const field of ALL_FIELDS) {
    const value = metadata[field]
    if (value === undefined || value === null) {
      missing.push(field)
    } else if (Array.isArray(value) && value.length === 0) {
      missing.push(field)
    }
  }

  return missing
}

/**
 * Format a preview of generated metadata for display
 */
function formatMetadataPreview(metadata: CompleteMetadataResult): string[] {
  const lines: string[] = []

  // Core
  if (metadata.title) {
    lines.push(`  Title: ${metadata.title}`)
  }
  if (metadata.description) {
    const preview = metadata.description.length > 80
      ? metadata.description.substring(0, 80) + '...'
      : metadata.description
    lines.push(`  Description: ${preview}`)
  }
  if (metadata.keywords?.length) {
    lines.push(`  Keywords: ${metadata.keywords.slice(0, 5).join(', ')}${metadata.keywords.length > 5 ? '...' : ''}`)
  }
  if (metadata.transcript) {
    const preview = metadata.transcript.length > 60
      ? metadata.transcript.substring(0, 60) + '...'
      : metadata.transcript
    lines.push(`  Transcript: ${preview.replace(/\n/g, ' | ')}`)
  }

  // Quality
  if (metadata.qualityScore) {
    const issues = metadata.qualityIssues?.length ? ` (issues: ${metadata.qualityIssues.length})` : ''
    lines.push(`  Quality: ${metadata.qualityScore}/5${issues}`)
  }
  if (metadata.standaloneScore) {
    lines.push(`  Standalone: ${metadata.standaloneScore}/5 ${metadata.canShareStandalone ? '(shareable)' : '(needs context)'}`)
  }

  // Social
  if (metadata.twitterText) {
    lines.push(`  Twitter: ${metadata.twitterText}`)
  }
  if (metadata.socialCaption) {
    lines.push(`  Caption: ${metadata.socialCaption}`)
  }
  if (metadata.targetPlatforms?.length) {
    lines.push(`  Platforms: ${metadata.targetPlatforms.join(', ')}`)
  }

  // Presentations
  if (metadata.audienceLevel) {
    lines.push(`  Audience: ${metadata.audienceLevel}`)
  }
  if (metadata.talkingPoints?.length) {
    lines.push(`  Talking points: ${metadata.talkingPoints.length} points`)
  }

  // Tone & Action
  if (metadata.emotionalTone) {
    lines.push(`  Tone: ${metadata.emotionalTone}`)
  }
  if (metadata.callToAction) {
    lines.push(`  CTA: ${metadata.callToAction}`)
  }

  // Data
  if (metadata.dataFreshness) {
    lines.push(`  Data: ${metadata.dataFreshness}`)
  }

  // Image Problems (highlight if found!)
  if (metadata.imageProblemsDetected) {
    lines.push(`  [WARNING] PROBLEMS: ${metadata.imageProblems?.join(', ')}`)
    if (metadata.imageProblemsRepairPrompt) {
      lines.push(`  Repair: ${metadata.imageProblemsRepairPrompt}`)
    }
  }

  return lines
}

async function main() {
  const args = process.argv.slice(2)
  const options = parseCommonArgs(args)

  const targetDir = options.path ? path.resolve(options.path) : ASSETS_DIR

  printHeader('Image Metadata Enrichment')
  console.log(`Target directory: ${targetDir}`)
  console.log(`Mode: ${options.all ? 'Regenerate ALL' : 'Fill missing only'}`)
  console.log(`Dry run: ${options.dryRun}`)
  if (options.limit) console.log(`Limit: ${options.limit}`)
  console.log('')

  if (!existsSync(targetDir)) {
    console.error(`ERROR: Directory not found: ${targetDir}`)
    process.exit(1)
  }

  // Sync index with file metadata first (ensures JSON matches EXIF data)
  console.log('[1/5] Syncing image index with file metadata...')
  await syncIndex({ quiet: true })
  console.log('  [OK] Index synced')

  // Find all images (skip GIFs - they're animations, not static images for enrichment)
  console.log('\n[2/5] Finding images...')
  let images = await findImages(targetDir, {
    extensions: ['.png', '.jpg', '.jpeg', '.webp'],
  })
  console.log(`  Found ${images.length} images (skipping GIFs)`)

  // Filter to only those needing enrichment (unless --all)
  if (!options.all) {
    console.log('\n[3/5] Checking for missing metadata...')
    const toProcess: { path: string; missing: string[] }[] = []

    for (const img of images) {
      const missing = await getMissingFields(img)
      if (missing.length > 0) {
        toProcess.push({ path: img, missing })
      }
    }

    const complete = images.length - toProcess.length
    console.log(`  ${complete} images have complete metadata`)
    console.log(`  ${toProcess.length} images need enrichment`)

    // Show breakdown of missing fields (grouped)
    const missingCounts: Record<string, number> = {}
    for (const item of toProcess) {
      for (const field of item.missing) {
        missingCounts[field] = (missingCounts[field] || 0) + 1
      }
    }

    // Group by category
    const categories = {
      'Core': ['title', 'description', 'keywords', 'transcript'],
      'Quality': ['qualityScore', 'standaloneScore'],
      'Social': ['twitterText', 'socialCaption', 'canShareStandalone'],
      'Presentations': ['speakerNotes', 'audienceLevel'],
      'Accessibility': ['altText', 'emotionalTone'],
    }

    for (const [category, fields] of Object.entries(categories)) {
      const counts = fields
        .filter(f => missingCounts[f])
        .map(f => `${f}: ${missingCounts[f]}`)
      if (counts.length > 0) {
        console.log(`    ${category}: ${counts.join(', ')}`)
      }
    }

    images = toProcess.map(p => p.path)
  } else {
    console.log('\n[3/5] --all flag set, will regenerate all metadata')
  }

  // Apply limit
  if (options.limit && images.length > options.limit) {
    images = images.slice(0, options.limit)
    console.log(`  Limited to ${options.limit} images`)
  }

  if (images.length === 0) {
    console.log('\nNo images need enrichment.')
    process.exit(0)
  }

  // Process images
  console.log(`\n[4/5] Enriching metadata for ${images.length} images...`)
  const results: EnrichmentResult[] = []
  let processed = 0
  let enriched = 0

  for (const imagePath of images) {
    const relativePath = path.relative(process.cwd(), imagePath)
    processed++

    console.log(`\n[${processed}/${images.length}] ${relativePath}`)

    // Generate all metadata in one API call
    const generated = await generateCompleteMetadata(imagePath)

    // Count fields that were generated
    const fieldsAdded = Object.keys(generated).filter(k => {
      const val = generated[k as keyof CompleteMetadataResult]
      return val !== undefined && val !== null && (Array.isArray(val) ? val.length > 0 : true)
    })

    // Display preview
    const preview = formatMetadataPreview(generated)
    for (const line of preview) {
      console.log(line)
    }

    results.push({
      path: relativePath,
      generated,
      fieldsAdded,
    })

    // Save to metadata
    if (!options.dryRun && fieldsAdded.length > 0) {
      // Add timestamp
      const metadataToSave = {
        ...generated,
        metadataEnrichedAt: new Date().toISOString(),
      }

      await writeImageMetadata(imagePath, metadataToSave)

      // Update image-index.json incrementally (fast, no full rebuild)
      await updateImageInIndex(imagePath, metadataToSave)

      console.log(`  [OK] Saved ${fieldsAdded.length} fields + updated index`)
      enriched++
    } else if (options.dryRun) {
      console.log(`  [DRY RUN] Would save ${fieldsAdded.length} fields`)
    } else {
      console.log(`  [SKIP] No fields generated`)
    }

    // Rate limiting - slightly longer for comprehensive analysis
    await new Promise(resolve => setTimeout(resolve, 800))
  }

  // Summary
  printSummary({
    'Images processed': processed,
    'Successfully enriched': enriched,
  })

  // Quality summary
  const avgQuality = results
    .filter(r => r.generated.qualityScore)
    .reduce((sum, r) => sum + (r.generated.qualityScore || 0), 0) /
    results.filter(r => r.generated.qualityScore).length

  const shareable = results.filter(r => r.generated.canShareStandalone).length

  if (avgQuality) {
    console.log(`\nQuality Insights:`)
    console.log(`  Average quality score: ${avgQuality.toFixed(1)}/5`)
    console.log(`  Shareable standalone: ${shareable}/${results.length} images`)
  }

  // Image problems summary
  const problemImages = results.filter(r => r.generated.imageProblemsDetected)
  if (problemImages.length > 0) {
    console.log(`\n[!] PROBLEMS DETECTED in ${problemImages.length} images:`)
    for (const img of problemImages) {
      console.log(`  - ${img.path}: ${img.generated.imageProblems?.join(', ')}`)
    }
    console.log(`\nRun "npm run images:fix" to automatically fix these.`)
  }

  if (options.dryRun) {
    console.log('\n[DRY RUN] No metadata was saved. Run without --dry-run to save.')
  }
}

main().catch(error => {
  console.error('Fatal error:', error)
  process.exit(1)
})
