/**
 * Convert PNG chapter images to JPG (quality 95) and delete originals
 *
 * Usage:
 *   npx tsx scripts/images/convert-png-to-jpg.ts [--dry-run]
 */

import sharp from 'sharp';
import fs from 'fs/promises';
import path from 'path';
import { glob } from 'glob';

const ASSETS_DIR = path.join(process.cwd(), 'assets');
const QUALITY = 95;

async function convertPngToJpg(pngPath: string, dryRun: boolean): Promise<{ saved: number } | null> {
  const jpgPath = pngPath.replace(/\.png$/, '.jpg');

  // Check if JPG already exists
  try {
    await fs.access(jpgPath);
    // JPG exists - just delete the PNG duplicate
    const pngStats = await fs.stat(pngPath);
    if (!dryRun) {
      await fs.unlink(pngPath);
    }
    console.log(`[DELETE] ${path.relative(process.cwd(), pngPath)} (JPG exists, saved ${(pngStats.size / 1024).toFixed(0)}KB)`);
    return { saved: pngStats.size };
  } catch {
    // JPG doesn't exist - convert
  }

  try {
    const pngStats = await fs.stat(pngPath);

    if (!dryRun) {
      await sharp(pngPath)
        .jpeg({ quality: QUALITY })
        .toFile(jpgPath);
    }

    const jpgStats = dryRun ? { size: pngStats.size * 0.12 } : await fs.stat(jpgPath);
    const saved = pngStats.size - jpgStats.size;
    const pngSize = (pngStats.size / 1024 / 1024).toFixed(1);
    const jpgSize = (jpgStats.size / 1024).toFixed(0);

    if (!dryRun) {
      await fs.unlink(pngPath);
    }

    console.log(`[CONVERT] ${path.relative(process.cwd(), pngPath)}`);
    console.log(`          PNG: ${pngSize}MB -> JPG: ${jpgSize}KB (saved ${(saved / 1024 / 1024).toFixed(1)}MB)`);

    return { saved };
  } catch (error) {
    console.error(`[ERROR] Failed to convert ${pngPath}:`, error);
    return null;
  }
}

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');

  if (dryRun) {
    console.log('=== DRY RUN MODE (no files will be modified) ===\n');
  }

  console.log('Finding PNG chapter images...\n');

  // Find all PNG files matching chapter image patterns
  const patterns = [
    'assets/**/!(*-retro)*-og-*.png',
    'assets/**/!(*-retro)*-infographic-*.png',
    'assets/**/!(*-retro)*-slide-*.png',
  ];

  // Actually, let's just find all PNGs with these patterns (including in knowledge subfolder)
  const pngFiles = await glob('assets/**/*-{og,infographic,slide}-*.png', {
    cwd: process.cwd(),
    absolute: true,
  });

  console.log(`Found ${pngFiles.length} PNG files to process\n`);

  let totalSaved = 0;
  let converted = 0;
  let failed = 0;

  for (const pngPath of pngFiles) {
    const result = await convertPngToJpg(pngPath, dryRun);
    if (result) {
      totalSaved += result.saved;
      converted++;
    } else {
      failed++;
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('Summary:');
  console.log(`  Files processed: ${converted}`);
  console.log(`  Failed: ${failed}`);
  console.log(`  Total space saved: ${(totalSaved / 1024 / 1024).toFixed(1)} MB`);
  if (dryRun) {
    console.log('\n  (Dry run - no files were modified)');
  }
  console.log('='.repeat(60));
}

main().catch(console.error);
