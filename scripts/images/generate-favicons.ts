/**
 * Generate simple transparent background favicons for all Quarto configs
 *
 * Uses Gemini image generation to create unique favicons for each Quarto configuration
 * in the project root. Since Gemini cannot generate true transparent backgrounds,
 * we generate on a solid white background and use Sharp to make white pixels transparent.
 *
 * Usage:
 *   npx tsx scripts/images/generate-favicons.ts [options]
 *
 * Options:
 *   --force              Regenerate all favicons even if they already exist
 *   --update-configs     Update the _quarto*.yml files to use the new favicons
 *   --filter <name>      Only process configs matching this pattern (e.g., "economics")
 *
 * Examples:
 *   # Generate all missing favicons
 *   npx tsx scripts/images/generate-favicons.ts
 *
 *   # Force regenerate all favicons and update configs
 *   npx tsx scripts/images/generate-favicons.ts --force --update-configs
 *
 *   # Generate only for economics config
 *   npx tsx scripts/images/generate-favicons.ts --filter economics
 */

import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs/promises';
import { existsSync } from 'fs';
import yaml from 'js-yaml';
import sharp from 'sharp';
import { generateImages, saveImage } from '../lib/gemini-images.js';

// Load environment variables
dotenv.config();

// Favicon sizes to generate
const FAVICON_SIZES = {
  'favicon-16x16.png': 16,
  'favicon-32x32.png': 32,
  'favicon-48x48.png': 48,
  'favicon.png': 64,           // Default favicon
  'apple-touch-icon.png': 180,
  'android-chrome-192x192.png': 192,
  'android-chrome-512x512.png': 512,
};

// Quarto config files to process (in root directory)
const QUARTO_CONFIGS = [
  '_quarto-book.yml',
  '_quarto-economics.yml',
  '_quarto-iab.yml',
  '_quarto-wishocracy.yml',
  '_quarto-test.yml',
];

interface QuartoConfig {
  fileName: string;
  title: string;
  description: string;
  siteUrl: string;
  faviconPath: string;
}

/**
 * Extract relevant info from a Quarto config file
 */
async function parseQuartoConfig(configPath: string): Promise<QuartoConfig | null> {
  try {
    const content = await fs.readFile(configPath, 'utf-8');
    const config = yaml.load(content) as Record<string, any>;

    const fileName = path.basename(configPath, '.yml');

    // Extract title from book or website section
    let title = '';
    let description = '';
    let siteUrl = '';

    if (config.book) {
      title = config.book.title || '';
      description = config.book.description || '';
      siteUrl = config.book['site-url'] || '';
    } else if (config.website) {
      title = config.website.title || '';
      description = config.website.description || '';
      siteUrl = config.website['site-url'] || '';
    }

    // Fallback to metadata
    if (!title && config.metadata?.title) {
      title = config.metadata.title;
    }
    if (!description && config.metadata?.description) {
      description = config.metadata.description;
    }

    // Generate a clean name for the favicon
    const cleanName = fileName.replace('_quarto-', '').replace('_quarto', 'default');
    const faviconPath = `assets/icons/${cleanName}-favicon.png`;

    return {
      fileName,
      title: title || cleanName,
      description: description || '',
      siteUrl,
      faviconPath,
    };
  } catch (error) {
    console.error(`[ERROR] Failed to parse ${configPath}:`, error);
    return null;
  }
}

/**
 * Generate prompt for favicon based on config
 * Uses bold black & white design with content-relevant symbols
 */
function generateFaviconPrompt(config: QuartoConfig): string {
  const configName = config.fileName.toLowerCase();

  let iconConcept = '';

  if (configName.includes('book')) {
    // War on Disease - the main book/manual
    iconConcept = `A SKULL with a bold X crossed through it, or a VIRUS/GERM shape with a prohibition sign (circle with diagonal line) through it.
The symbol should clearly communicate "death to disease" or "no more disease".
Think: a warning sign or prohibition symbol, but for disease/death.`;
  } else if (configName.includes('economics')) {
    // 1% Treaty economics paper - about redirecting 1% of military spending
    iconConcept = `A bold "1%" symbol, or a COIN/DOLLAR being transformed into a MEDICAL CROSS or PILL.
Could also be a PIE CHART with 1% slice highlighted, or military symbol (star/tank) morphing into medical symbol.
The symbol should communicate "small percentage = big health impact".`;
  } else if (configName.includes('iab')) {
    // Incentive Alignment Bonds - aligning political incentives
    iconConcept = `A HANDSHAKE symbol, or SCALES OF JUSTICE perfectly balanced, or two ARROWS pointing toward each other meeting in the middle.
Could also be a MAGNET attracting something, or puzzle pieces clicking together.
The symbol should communicate "alignment" or "agreement" or "balanced incentives".`;
  } else if (configName.includes('wishocracy')) {
    // Wishocracy - democratic wish allocation via RAPPA
    iconConcept = `A BALLOT BOX with a STAR or SPARKLE coming out of it, or a RAISED HAND (voting) with a star/wish symbol.
Could also be a CHECKBOX with a star, or speech bubbles converging into one.
The symbol should communicate "collective wishes" or "democratic choice".`;
  } else if (configName.includes('test')) {
    // Test config
    iconConcept = `A simple FLASK or BEAKER, or a CHECKMARK inside a circle, or a magnifying glass.
Basic "testing/verification" symbol.`;
  } else {
    // Default - global health
    iconConcept = `A GLOBE with a HEARTBEAT LINE across it, or a MEDICAL CROSS inside a circle.
The symbol should communicate "global health".`;
  }

  return `Create a bold favicon icon in BLACK, RED, and WHITE.

STRICT COLOR RULES:
- Background: BRIGHT MAGENTA (#FF00FF) - this will be removed to make transparent
- Icon colors ONLY: BLACK (#000000), RED (#DC2626), and WHITE (#FFFFFF)
- NO other colors, NO gray, NO gradients
- The magenta background is a "green screen" - it will be removed

DESIGN REQUIREMENTS:
- BOLD, thick BLACK outlines (minimum 4-6px at 512px resolution)
- RED for fills or accents
- WHITE for highlights or negative space within the icon
- Simple shape that reads clearly at 16x16 pixels
- Single unified shape - no scattered elements
- CHUNKY and GEOMETRIC - nothing thin or delicate

ICON CONCEPT:
${iconConcept}

CRITICAL:
- Must be instantly recognizable when squinting
- No fine details - they disappear at small sizes
- Think: Soviet propaganda poster aesthetic - bold, high contrast
- The simpler the better

Background MUST be pure bright magenta (#FF00FF). Icon uses ONLY black, red, and white.`;
}

/**
 * Remove magenta background from image using Sharp
 * Makes all bright magenta (#FF00FF) pixels transparent
 * This is a "green screen" approach - magenta is used as a background
 * that can be removed while preserving white in the icon design
 */
async function removeMagentaBackground(inputPath: string, outputPath: string): Promise<void> {
  // Read the image
  const image = sharp(inputPath);
  const { data, info } = await image
    .raw()
    .toBuffer({ resolveWithObject: true });

  // Create output buffer with alpha channel
  const outputData = Buffer.alloc(info.width * info.height * 4);

  // Process each pixel
  for (let i = 0; i < info.width * info.height; i++) {
    const srcIdx = i * info.channels;
    const dstIdx = i * 4;

    const r = data[srcIdx];
    const g = data[srcIdx + 1];
    const b = data[srcIdx + 2];

    // Check if pixel is magenta or near-magenta (#FF00FF with tolerance)
    // Magenta = high red, low green, high blue
    const isMagenta = r > 200 && g < 80 && b > 200;

    // Copy RGB values
    outputData[dstIdx] = r;
    outputData[dstIdx + 1] = g;
    outputData[dstIdx + 2] = b;

    // Set alpha: 0 for magenta, 255 for non-magenta
    outputData[dstIdx + 3] = isMagenta ? 0 : 255;
  }

  // Write the output image with transparency
  await sharp(outputData, {
    raw: {
      width: info.width,
      height: info.height,
      channels: 4,
    },
  })
    .png()
    .toFile(outputPath);
}

/**
 * Generate favicon for a single config
 */
async function generateFaviconForConfig(
  config: QuartoConfig,
  forceRegenerate: boolean = false
): Promise<string | null> {
  const outputDir = path.join(process.cwd(), 'assets', 'icons');
  const cleanName = config.fileName.replace('_quarto-', '').replace('_quarto', 'default');
  const masterFilePath = path.join(outputDir, `${cleanName}-favicon-master.png`);

  // Check if master favicon already exists
  if (!forceRegenerate && existsSync(masterFilePath)) {
    console.log(`  [SKIP] Master favicon already exists: ${masterFilePath}`);
    return masterFilePath;
  }

  console.log(`  Generating favicon for: ${config.title}`);
  console.log(`  Config: ${config.fileName}`);

  const prompt = generateFaviconPrompt(config);

  try {
    // Generate the master favicon image (1:1 aspect ratio, will generate at high res)
    const result = await generateImages({
      prompt,
      count: 1,
      aspectRatio: '1:1',
    });

    if (result.images.length === 0) {
      console.error(`  [ERROR] No favicon generated for ${config.fileName}`);
      return null;
    }

    // Ensure output directory exists
    await fs.mkdir(outputDir, { recursive: true });

    // Save the raw generated image first (with white background)
    const rawFilePath = path.join(outputDir, `${cleanName}-favicon-raw.png`);
    const imageBuffer = Buffer.from(result.images[0].imageBytes, 'base64');
    await fs.writeFile(rawFilePath, imageBuffer);
    console.log(`  [OK] Generated raw favicon: ${rawFilePath}`);

    // Remove magenta background to create transparent version
    console.log(`  [*] Removing magenta background...`);
    await removeMagentaBackground(rawFilePath, masterFilePath);
    console.log(`  [OK] Created transparent master: ${masterFilePath}`);

    // Generate all size variants
    for (const [filename, size] of Object.entries(FAVICON_SIZES)) {
      const sizedPath = path.join(outputDir, `${cleanName}-${filename}`);

      await sharp(masterFilePath)
        .resize(size, size, {
          fit: 'contain',
          background: { r: 0, g: 0, b: 0, alpha: 0 }, // Transparent background
        })
        .png()
        .toFile(sizedPath);

      console.log(`  [OK] Generated ${size}x${size}: ${sizedPath}`);
    }

    // Also generate .ico file (multi-resolution)
    const icoPath = path.join(outputDir, `${cleanName}-favicon.ico`);
    // For .ico, we'll just use the 32x32 PNG (sharp doesn't support ico directly)
    // The browser will use the PNG favicon anyway
    console.log(`  [INFO] For .ico format, use the 32x32 PNG with ico converter tool`);

    return masterFilePath;
  } catch (error) {
    console.error(`  [ERROR] Failed to generate favicon:`, error);
    return null;
  }
}

/**
 * Update Quarto config file to use the new favicon
 */
async function updateQuartoConfig(configPath: string, cleanName: string): Promise<void> {
  try {
    let content = await fs.readFile(configPath, 'utf-8');

    const faviconPath = `assets/icons/${cleanName}-favicon.png`;

    // Check if config has book or website section
    if (content.includes('book:')) {
      // Update or add favicon in book section
      if (content.match(/^\s*favicon:/m)) {
        content = content.replace(
          /^(\s*)favicon:.*$/m,
          `$1favicon: ${faviconPath}`
        );
      } else {
        // Add favicon after title in book section
        content = content.replace(
          /(book:\s*\n\s*title:[^\n]+)/,
          `$1\n  favicon: ${faviconPath}`
        );
      }
    } else if (content.includes('website:')) {
      // Update or add favicon in website section
      if (content.match(/^\s*favicon:/m)) {
        content = content.replace(
          /^(\s*)favicon:.*$/m,
          `$1favicon: ${faviconPath}`
        );
      } else {
        // Add favicon after title in website section
        content = content.replace(
          /(website:\s*\n\s*title:[^\n]+)/,
          `$1\n  favicon: ${faviconPath}`
        );
      }
    }

    await fs.writeFile(configPath, content, 'utf-8');
    console.log(`  [OK] Updated ${configPath} to use ${faviconPath}`);
  } catch (error) {
    console.error(`  [ERROR] Failed to update ${configPath}:`, error);
  }
}

/**
 * Main function
 */
async function main(): Promise<void> {
  console.log('='.repeat(60));
  console.log('Favicon Generator for Quarto Configurations');
  console.log('='.repeat(60));

  // Check for API key
  if (!process.env.GOOGLE_GENERATIVE_AI_API_KEY) {
    console.error('ERROR: GOOGLE_GENERATIVE_AI_API_KEY environment variable is not set');
    console.error('Please set your Google Gemini API key in .env file');
    process.exit(1);
  }

  // Parse command line arguments
  const args = process.argv.slice(2);
  const forceRegenerate = args.includes('--force');
  const updateConfigs = args.includes('--update-configs');

  let filter: string | undefined;
  const filterIndex = args.indexOf('--filter');
  if (filterIndex !== -1 && args[filterIndex + 1]) {
    filter = args[filterIndex + 1];
  }

  if (forceRegenerate) {
    console.log('[INFO] Force mode - regenerating all favicons\n');
  }
  if (updateConfigs) {
    console.log('[INFO] Will update Quarto configs to use new favicons\n');
  }
  if (filter) {
    console.log(`[INFO] Filtering to configs matching: ${filter}\n`);
  }

  // Process each config
  let processed = 0;
  let generated = 0;
  let skipped = 0;
  let failed = 0;

  for (const configFile of QUARTO_CONFIGS) {
    // Apply filter
    if (filter && !configFile.toLowerCase().includes(filter.toLowerCase())) {
      continue;
    }

    const configPath = path.join(process.cwd(), configFile);

    // Check if config exists
    if (!existsSync(configPath)) {
      console.log(`\n[SKIP] Config not found: ${configFile}`);
      skipped++;
      continue;
    }

    console.log(`\n${'─'.repeat(60)}`);
    console.log(`Processing: ${configFile}`);
    console.log('─'.repeat(60));

    processed++;

    // Parse config
    const config = await parseQuartoConfig(configPath);
    if (!config) {
      console.log(`  [SKIP] Could not parse config`);
      skipped++;
      continue;
    }

    console.log(`  Title: ${config.title}`);
    if (config.siteUrl) {
      console.log(`  Site URL: ${config.siteUrl}`);
    }

    // Generate favicon
    const result = await generateFaviconForConfig(config, forceRegenerate);

    if (result) {
      generated++;

      // Update config if requested
      if (updateConfigs) {
        const cleanName = config.fileName.replace('_quarto-', '').replace('_quarto', 'default');
        await updateQuartoConfig(configPath, cleanName);
      }
    } else {
      failed++;
    }
  }

  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('Summary:');
  console.log(`  Configs processed: ${processed}`);
  console.log(`  Favicons generated: ${generated}`);
  console.log(`  Skipped: ${skipped}`);
  console.log(`  Failed: ${failed}`);
  console.log('='.repeat(60));

  if (generated > 0 && !updateConfigs) {
    console.log('\nTo update Quarto configs to use the new favicons, run:');
    console.log('  npx tsx scripts/images/generate-favicons.ts --update-configs');
  }
}

// Run the script
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
