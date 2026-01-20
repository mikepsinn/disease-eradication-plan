/**
 * Generate OG images and favicons for all Quarto configurations
 *
 * Dynamically discovers _quarto-*.yml configs and generates missing branding assets.
 * Reads image prompts from dih-render.favicon-prompt and dih-render.og-image-prompt.
 *
 * Output locations:
 *   - OG images: assets/og/{config-name}-og-1200x630.jpg (JPG for compression)
 *   - Favicons: assets/icons/{config-name}-favicon*.png (PNG for transparency)
 *
 * Usage:
 *   npx tsx scripts/images/generate-project-branding.ts [options]
 *
 * Options:
 *   --force              Regenerate all images even if they already exist
 *   --filter <name>      Only process configs matching this pattern
 *
 * Examples:
 *   npx tsx scripts/images/generate-project-branding.ts
 *   npx tsx scripts/images/generate-project-branding.ts --filter economics --force
 */

import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs/promises';
import { existsSync } from 'fs';
import yaml from 'js-yaml';
import sharp from 'sharp';
import { generateAndSaveImages } from '../lib/gemini-images.js';
import { VisualStyles } from '../lib/image-prompts.js';

// Load environment variables
dotenv.config();

// Favicon sizes to generate (PNG for transparency support)
const FAVICON_SIZES: Record<string, number> = {
  'favicon-16x16.png': 16,
  'favicon-32x32.png': 32,
  'favicon-48x48.png': 48,
  'favicon.png': 64,
  'apple-touch-icon.png': 180,
  'android-chrome-192x192.png': 192,
  'android-chrome-512x512.png': 512,
};

interface QuartoConfig {
  configFile: string;
  configName: string;
  title: string;
  description: string;
  keywords: string[];
  siteUrl: string;
  // Custom prompts from dih-render section
  faviconPrompt: string | null;
  ogImagePrompt: string | null;
}

/**
 * Discover all Quarto config files in the project root (excluding test)
 */
async function discoverQuartoConfigs(): Promise<string[]> {
  const projectRoot = process.cwd();
  const files = await fs.readdir(projectRoot);

  return files
    .filter(f => f.startsWith('_quarto-') && f.endsWith('.yml') && !f.includes('test'))
    .map(f => path.join(projectRoot, f))
    .sort();
}

/**
 * Parse a Quarto config file and extract branding-relevant info
 */
async function parseQuartoConfig(configPath: string): Promise<QuartoConfig | null> {
  try {
    const content = await fs.readFile(configPath, 'utf-8');
    const config = yaml.load(content) as Record<string, any>;

    const fileName = path.basename(configPath, '.yml');
    const configName = fileName.replace('_quarto-', '');

    // Extract from book or website section
    const bookOrWebsite = config.book || config.website || {};
    let title = bookOrWebsite.title || '';
    let description = bookOrWebsite.description || '';
    let siteUrl = bookOrWebsite['site-url'] || '';

    // Fallback to metadata section
    const metadata = config.metadata || {};
    if (!title) title = metadata.title || configName;
    if (!description) description = metadata.description || '';

    // Get keywords from metadata (handle both array and string formats)
    let keywords: string[] = [];
    if (Array.isArray(metadata.keywords)) {
      keywords = metadata.keywords;
    } else if (typeof metadata.keywords === 'string') {
      keywords = metadata.keywords.split(',').map((k: string) => k.trim());
    }

    // Get custom prompts from dih-render section
    const dihRender = config['dih-render'] || {};
    const faviconPrompt = dihRender['favicon-prompt'] || null;
    const ogImagePrompt = dihRender['og-image-prompt'] || null;

    return {
      configFile: fileName,
      configName,
      title,
      description,
      keywords,
      siteUrl,
      faviconPrompt,
      ogImagePrompt,
    };
  } catch (error) {
    console.error(`[ERROR] Failed to parse ${configPath}:`, error);
    return null;
  }
}

/**
 * Build OG image prompt from config
 * Uses custom prompt from dih-render.og-image-prompt if available
 */
function buildOgImagePrompt(config: QuartoConfig): string {
  const style = VisualStyles.academic;

  return `
  ${style.style}
  
  CONCEPT: ${config.ogImagePrompt}
  `;

}

/**
 * Build favicon prompt from config
 * Uses custom prompt from dih-render.favicon-prompt if available
 */
function buildFaviconPrompt(config: QuartoConfig): string {
  const basePrompt = `Create an ultra-minimalist favicon icon.

STRICT COLOR RULES:
- Background: BRIGHT MAGENTA (#FF00FF) - this will be removed to make transparent
- Maximum 3 colors in the icon (red, white, black)

ICON CONCEPT:`;

  // Use custom prompt if provided
  if (config.faviconPrompt) {
    return `${basePrompt}
${config.faviconPrompt}

`;
  }

  // Fallback to generic prompt based on title
  return `${basePrompt}
Create a simple icon representing: "${config.title}"
${config.description ? `Context: ${config.description.substring(0, 150)}` : ''}

Background MUST be pure bright magenta (#FF00FF). Icon uses ONLY red, white, and black.`;
}

/**
 * Remove magenta background from favicon image to create transparency
 */
async function removeMagentaBackground(inputPath: string, outputPath: string): Promise<void> {
  const image = sharp(inputPath);
  const { data, info } = await image.raw().toBuffer({ resolveWithObject: true });

  const outputData = Buffer.alloc(info.width * info.height * 4);

  for (let i = 0; i < info.width * info.height; i++) {
    const srcIdx = i * info.channels;
    const dstIdx = i * 4;

    const r = data[srcIdx];
    const g = data[srcIdx + 1];
    const b = data[srcIdx + 2];

    // Check if pixel is magenta (high red, low green, high blue)
    const isMagenta = r > 200 && g < 80 && b > 200;

    outputData[dstIdx] = r;
    outputData[dstIdx + 1] = g;
    outputData[dstIdx + 2] = b;
    outputData[dstIdx + 3] = isMagenta ? 0 : 255; // Transparent for magenta
  }

  await sharp(outputData, {
    raw: { width: info.width, height: info.height, channels: 4 },
  })
    .png()
    .toFile(outputPath);
}

/**
 * Generate OG image for a config
 * Saves to: assets/og/{config-name}-og-1200x630.jpg
 */
async function generateOgImage(config: QuartoConfig, force: boolean = false): Promise<string | null> {
  const outputDir = path.join(process.cwd(), 'assets', 'og');
  const outputFileName = `${config.configName}-og-1200x630`;
  const outputPath = path.join(outputDir, `${outputFileName}.jpg`);

  // Also check for PNG version (for backwards compatibility)
  const pngPath = path.join(outputDir, `${outputFileName}.png`);

  if (!force && (existsSync(outputPath) || existsSync(pngPath))) {
    console.log(`  [SKIP] OG image exists: assets/og/${outputFileName}.*`);
    return outputPath;
  }

  // Ensure output directory exists
  await fs.mkdir(outputDir, { recursive: true });

  console.log(`  Generating OG image...`);
  const prompt = buildOgImagePrompt(config);

  try {
    const files = await generateAndSaveImages({
      prompt,
      aspectRatio: '16:9',
      outputDir,
      filePrefix: outputFileName,
      format: 'jpg', // Use JPG for better compression
      metadata: {
        title: config.title,
        description: config.description,
        keywords: config.keywords,
        sourceUrl: config.siteUrl,
      },
    });

    if (files && files.length > 0) {
      console.log(`  [OK] Generated: assets/og/${outputFileName}.jpg`);
      return files[0];
    }
    return null;
  } catch (error) {
    console.error(`  [ERROR] Failed to generate OG image:`, error);
    return null;
  }
}

/**
 * Generate favicon for a config
 * Saves to: assets/icons/{config-name}-favicon*.png
 */
async function generateFavicon(config: QuartoConfig, force: boolean = false): Promise<string | null> {
  const outputDir = path.join(process.cwd(), 'assets', 'icons');
  const masterPath = path.join(outputDir, `${config.configName}-favicon-master.png`);
  const mainFaviconPath = path.join(outputDir, `${config.configName}-favicon.png`);

  if (!force && existsSync(masterPath) && existsSync(mainFaviconPath)) {
    console.log(`  [SKIP] Favicon exists: assets/icons/${config.configName}-favicon.png`);
    return mainFaviconPath;
  }

  // Ensure output directory exists
  await fs.mkdir(outputDir, { recursive: true });

  console.log(`  Generating favicon...`);
  const prompt = buildFaviconPrompt(config);

  try {
    const result = await generateAndSaveImages({
      prompt,
      aspectRatio: '1:1',
      outputDir,
      filePrefix: `${config.configName}-favicon-raw`,
      format: 'jpg', // API returns JPG natively, avoid conversion
      metadata: {
        title: `${config.title} - Favicon`,
        description: `Favicon icon for ${config.title}`,
      },
    });

    if (!result || result.length === 0) {
      console.error(`  [ERROR] No favicon generated`);
      return null;
    }

    const rawPath = result[0];

    // Remove magenta background to create transparency
    console.log(`  [*] Removing magenta background...`);
    await removeMagentaBackground(rawPath, masterPath);

    // Generate all size variants
    for (const [filename, size] of Object.entries(FAVICON_SIZES)) {
      const sizedPath = path.join(outputDir, `${config.configName}-${filename}`);

      await sharp(masterPath)
        .resize(size, size, {
          fit: 'contain',
          background: { r: 0, g: 0, b: 0, alpha: 0 },
        })
        .png()
        .toFile(sizedPath);

      console.log(`  [OK] ${size}x${size}: ${config.configName}-${filename}`);
    }

    // Clean up raw file
    try {
      await fs.unlink(rawPath);
    } catch {
      // Ignore cleanup errors
    }

    return mainFaviconPath;
  } catch (error) {
    console.error(`  [ERROR] Failed to generate favicon:`, error);
    return null;
  }
}

/**
 * Main function
 */
async function main(): Promise<void> {
  console.log('='.repeat(60));
  console.log('Project Branding Image Generator');
  console.log('='.repeat(60));
  console.log('');
  console.log('Output locations:');
  console.log('  OG images: assets/og/{config}-og-1200x630.jpg');
  console.log('  Favicons:  assets/icons/{config}-favicon*.png');
  console.log('');

  if (!process.env.GOOGLE_GENERATIVE_AI_API_KEY) {
    console.error('ERROR: GOOGLE_GENERATIVE_AI_API_KEY not set');
    process.exit(1);
  }

  // Parse arguments
  const args = process.argv.slice(2);
  const force = args.includes('--force');

  let filter: string | undefined;
  const filterIndex = args.indexOf('--filter');
  if (filterIndex !== -1 && args[filterIndex + 1]) {
    filter = args[filterIndex + 1];
  }

  if (force) console.log('[INFO] Force mode - regenerating all images\n');
  if (filter) console.log(`[INFO] Filter: ${filter}\n`);

  // Discover and process configs
  const configFiles = await discoverQuartoConfigs();
  console.log(`[OK] Found ${configFiles.length} configs\n`);

  let ogCount = 0;
  let faviconCount = 0;

  for (const configFile of configFiles) {
    const config = await parseQuartoConfig(configFile);
    if (!config) continue;

    if (filter && !config.configName.toLowerCase().includes(filter.toLowerCase())) {
      continue;
    }

    console.log('─'.repeat(60));
    console.log(`${config.configName}: ${config.title}`);
    if (config.faviconPrompt) console.log(`  [*] Custom favicon prompt found`);
    if (config.ogImagePrompt) console.log(`  [*] Custom OG image prompt found`);
    console.log('─'.repeat(60));

    const og = await generateOgImage(config, force);
    if (og) ogCount++;

    const fav = await generateFavicon(config, force);
    if (fav) faviconCount++;
  }

  console.log('\n' + '='.repeat(60));
  console.log(`Summary: ${ogCount} OG images, ${faviconCount} favicons`);
  console.log('='.repeat(60));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
