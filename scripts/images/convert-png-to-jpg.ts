/**
 * Convert PNG images to JPG and update all references in QMD files
 *
 * Usage:
 *   npx tsx scripts/images/convert-png-to-jpg.ts [options]
 *
 * Options:
 *   --quality <n>    JPEG quality 1-100 (default: 85)
 *   --dry-run        Show what would be converted without making changes
 *   --keep-png       Keep original PNG files after conversion
 */

import sharp from 'sharp'
import fs from 'fs/promises'
import { existsSync, statSync } from 'fs'
import path from 'path'
import { glob } from 'glob'

// Shared utilities
import { findPngFiles, formatBytes } from '../lib/image-file-utils'
import { parseCommonArgs, getArgValue, hasFlag, printHeader, printSummary } from '../lib/cli-utils'

interface ConversionResult {
  pngPath: string
  jpgPath: string
  pngSize: number
  jpgSize: number
  savings: number
}

async function convertPngToJpg(
  pngPath: string,
  quality: number,
  dryRun: boolean
): Promise<ConversionResult | null> {
  const jpgPath = pngPath.replace(/\.png$/, '.jpg');
  const pngSize = statSync(pngPath).size;

  if (dryRun) {
    // Estimate JPG size as ~15% of PNG for dry run display
    const estimatedJpgSize = Math.round(pngSize * 0.15);
    return {
      pngPath,
      jpgPath,
      pngSize,
      jpgSize: estimatedJpgSize,
      savings: ((pngSize - estimatedJpgSize) / pngSize) * 100,
    };
  }

  try {
    // Check if JPG already exists
    if (existsSync(jpgPath)) {
      const jpgSize = statSync(jpgPath).size;
      return {
        pngPath,
        jpgPath,
        pngSize,
        jpgSize,
        savings: ((pngSize - jpgSize) / pngSize) * 100,
      };
    }

    await sharp(pngPath)
      .jpeg({ quality, mozjpeg: true })
      .toFile(jpgPath);

    const jpgSize = statSync(jpgPath).size;
    const savings = ((pngSize - jpgSize) / pngSize) * 100;

    return {
      pngPath,
      jpgPath,
      pngSize,
      jpgSize,
      savings,
    };
  } catch (error) {
    console.error(`  [ERROR] Failed to convert ${pngPath}:`, error);
    return null;
  }
}

async function updateQmdReferences(dryRun: boolean): Promise<number> {
  const qmdFiles = await glob('**/*.qmd', {
    cwd: process.cwd(),
    ignore: ['node_modules/**', '.quarto/**', '_book/**'],
  });

  let totalUpdates = 0;

  for (const qmdFile of qmdFiles) {
    const fullPath = path.join(process.cwd(), qmdFile);
    const content = await fs.readFile(fullPath, 'utf-8');

    // Count .png references in image markdown
    const pngRefs = (content.match(/\]\([^)]*\.png\)/g) || []).length;

    if (pngRefs > 0) {
      const updatedContent = content.replace(/\.png\)/g, '.jpg)');

      if (updatedContent !== content) {
        totalUpdates += pngRefs;

        if (!dryRun) {
          await fs.writeFile(fullPath, updatedContent, 'utf-8');
        }
        console.log(`  ${qmdFile}: ${pngRefs} reference(s) updated`);
      }
    }
  }

  return totalUpdates;
}

async function main() {
  const args = process.argv.slice(2)
  const options = parseCommonArgs(args)
  const keepPng = hasFlag(args, 'keep-png')

  // Parse quality
  let quality = 85
  const qualityArg = getArgValue(args, 'quality', ['q'])
  if (qualityArg) {
    quality = parseInt(qualityArg, 10)
    if (isNaN(quality) || quality < 1 || quality > 100) {
      console.error('[ERROR] Quality must be 1-100')
      process.exit(1)
    }
  }

  printHeader('PNG to JPG Converter')
  console.log(`Quality: ${quality}`)
  console.log(`Dry run: ${options.dryRun}`)
  console.log(`Keep PNGs: ${keepPng}`)
  console.log('')

  // Find all PNGs in assets/images
  const assetsDir = path.join(process.cwd(), 'assets', 'images')
  if (!existsSync(assetsDir)) {
    console.error('[ERROR] assets/images directory not found')
    process.exit(1)
  }

  console.log('[1/4] Finding PNG files...')
  const pngFiles = await findPngFiles(assetsDir)
  console.log(`  Found ${pngFiles.length} PNG files\n`)

  if (pngFiles.length === 0) {
    console.log('No PNG files to convert.')
    process.exit(0)
  }

  // Convert PNGs to JPGs
  console.log('[2/4] Converting images...')
  const results: ConversionResult[] = []
  let totalPngSize = 0
  let totalJpgSize = 0

  for (const pngPath of pngFiles) {
    const relativePath = path.relative(process.cwd(), pngPath)
    const result = await convertPngToJpg(pngPath, quality, options.dryRun)
    if (result) {
      results.push(result)
      totalPngSize += result.pngSize
      totalJpgSize += result.jpgSize

      console.log(`  ${relativePath}`)
      console.log(`    ${formatBytes(result.pngSize)} -> ${formatBytes(result.jpgSize)} (${result.savings.toFixed(0)}% smaller)`)
    }
  }

  // Update QMD references
  console.log('\n[3/4] Updating QMD file references...')
  const updatedRefs = await updateQmdReferences(options.dryRun)
  if (updatedRefs === 0) {
    console.log('  No .png references found in QMD files')
  }

  // Delete original PNGs if not keeping
  let deletedCount = 0
  if (!options.dryRun && !keepPng && results.length > 0) {
    console.log('\n[4/4] Removing original PNG files...')
    for (const result of results) {
      try {
        await fs.unlink(result.pngPath)
        deletedCount++
      } catch (error) {
        console.error(`  Failed to delete: ${result.pngPath}`)
      }
    }
    console.log(`  Deleted ${deletedCount} PNG files`)
  } else if (keepPng) {
    console.log('\n[4/4] Keeping original PNG files (--keep-png)')
  }

  // Summary
  printSummary({
    'Images converted': results.length,
    'QMD references updated': updatedRefs,
    'PNG files deleted': options.dryRun ? '(dry run)' : deletedCount,
  })

  if (results.length > 0) {
    const totalSavings = ((totalPngSize - totalJpgSize) / totalPngSize) * 100
    console.log(`Total PNG size: ${formatBytes(totalPngSize)}`)
    console.log(`Total JPG size: ${formatBytes(totalJpgSize)}`)
    console.log(`Space saved: ${formatBytes(totalPngSize - totalJpgSize)} (${totalSavings.toFixed(0)}%)`)
  }

  if (options.dryRun) {
    console.log('\n[DRY RUN] No changes made. Run without --dry-run to convert.')
  }
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
