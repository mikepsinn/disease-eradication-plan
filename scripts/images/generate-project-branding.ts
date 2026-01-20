/**
 * Generate OG images and favicons for all Quarto configurations
 *
 * Dynamically discovers _quarto-*.yml configs and generates missing branding assets.
 * All content comes from the configs themselves - no hardcoded site-specific info.
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
import { VisualStyles, ACADEMIC_STYLE } from '../lib/image-prompts.js';

// Load environment variables
dotenv.config();

// Favicon sizes to generate
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
  faviconPath: string;
  ogImagePath: string;
}

/**
 * Discover all Quarto config files in the project root
 */
async function discoverQuartoConfigs(): Promise<string[]> {
  const projectRoot = process.cwd();
  const files = await fs.readdir(projectRoot);

  return files
    .filter(f => f.startsWith('_quarto-') && f.endsWith('.yml'))
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
    let faviconPath = bookOrWebsite.favicon || '';

    // Fallback to metadata section
    const metadata = config.metadata || {};
    if (!title) title = metadata.title || configName;
    if (!description) description = metadata.description || '';

    // Get keywords from metadata
    const keywords: string[] = metadata.keywords || [];

    // Get OG image from metadata
    let ogImagePath = '';
    if (metadata.image) {
      // Extract local path from URL if possible
      const urlMatch = metadata.image.match(/\/assets\/[^"'\s]+/);
      if (urlMatch) {
        ogImagePath = urlMatch[0].substring(1);
      }
    }

    // Default paths if not specified
    if (!faviconPath) {
      faviconPath = `assets/icons/${configName}-favicon.png`;
    }
    if (!ogImagePath) {
      ogImagePath = `assets/${configName}-og-1200x630.png`;
    }

    return {
      configFile: fileName,
      configName,
      title,
      description,
      keywords,
      siteUrl,
      faviconPath,
      ogImagePath,
    };
  } catch (error) {
    console.error(`[ERROR] Failed to parse ${configPath}:`, error);
    return null;
  }
}

/**
 * Build content string for OG image generation from config
 */
function buildOgContent(config: QuartoConfig): string {
  const parts: string[] = [];

  if (config.title) {
    parts.push(`TITLE: ${config.title}`);
  }
  if (config.description) {
    parts.push(`DESCRIPTION: ${config.description.substring(0, 500)}`);
  }
  if (config.keywords.length > 0) {
    parts.push(`KEYWORDS: ${config.keywords.slice(0, 5).join(', ')}`);
  }

  return parts.join('\n\n');
}

/**
 * Build favicon prompt from config
 */
function buildFaviconPrompt(config: QuartoConfig): string {
  return `Create an ultra-minimalist favicon icon for: "${config.title}"

STRICT RULES:
- Background: BRIGHT MAGENTA (#FF00FF) - will be removed for transparency
- Icon: BLACK and WHITE only
- EXTREMELY SIMPLE - must be recognizable at 16x16 pixels
- Thick bold lines, high contrast
- Think: app icon, not illustration

${config.description ? `Context: ${config.description.substring(0, 200)}` : ''}

Generate with aspect ratio 1:1 (square).
Background MUST be pure magenta (#FF00FF).`;
}

/**
 * Remove magenta background from favicon image
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

    const isMagenta = r > 200 && g < 80 && b > 200;

    outputData[dstIdx] = r;
    outputData[dstIdx + 1] = g;
    outputData[dstIdx + 2] = b;
    outputData[dstIdx + 3] = isMagenta ? 0 : 255;
  }

  await sharp(outputData, {
    raw: { width: info.width, height: info.height, channels: 4 },
  })
    .png()
    .toFile(outputPath);
}

/**
 * Generate OG image for a config
 */
async function generateOgImage(config: QuartoConfig, force: boolean = false): Promise<string | null> {
  const outputPath = path.join(process.cwd(), config.ogImagePath);
  const outputDir = path.dirname(outputPath);
  const fileName = path.basename(outputPath, '.png');

  if (!force && existsSync(outputPath)) {
    console.log(`  [SKIP] OG image exists: ${config.ogImagePath}`);
    return outputPath;
  }

  console.log(`  Generating OG image...`);

  const content = buildOgContent(config);
  const style = VisualStyles.academic;

  // Build prompt using academic style
  const prompt = `Create a professional social media OG image (1200x630).
${style.style}

${content}

Requirements:
- Clean, professional academic aesthetic
- Title text must be large, bold, readable
- Centered composition for social media preview
- High contrast, minimalist design
- DO NOT include any URL or website address`;

  try {
    const files = await generateAndSaveImages({
      prompt,
      aspectRatio: '16:9',
      outputDir,
      filePrefix: fileName,
      metadata: {
        title: config.title,
        description: config.description,
        keywords: config.keywords,
        sourceUrl: config.siteUrl,
      },
    });

    if (files && files.length > 0) {
      console.log(`  [OK] Generated: ${config.ogImagePath}`);
      return files[0];
    }
    return null;
  } catch (error) {
    console.error(`  [ERROR] Failed:`, error);
    return null;
  }
}

/**
 * Generate favicon for a config
 */
async function generateFavicon(config: QuartoConfig, force: boolean = false): Promise<string | null> {
  const outputDir = path.join(process.cwd(), 'assets', 'icons');
  const masterPath = path.join(outputDir, `${config.configName}-favicon-master.png`);
  const faviconPath = path.join(process.cwd(), config.faviconPath);

  if (!force && existsSync(masterPath) && existsSync(faviconPath)) {
    console.log(`  [SKIP] Favicon exists: ${config.faviconPath}`);
    return faviconPath;
  }

  console.log(`  Generating favicon...`);
  const prompt = buildFaviconPrompt(config);

  try {
    const result = await generateAndSaveImages({
      prompt,
      aspectRatio: '1:1',
      outputDir,
      filePrefix: `${config.configName}-favicon-raw`,
    });

    if (!result || result.length === 0) {
      console.error(`  [ERROR] No favicon generated`);
      return null;
    }

    const rawPath = result[0];

    // Remove magenta background
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

    return faviconPath;
  } catch (error) {
    console.error(`  [ERROR] Failed:`, error);
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

  if (force) console.log('[INFO] Force mode\n');
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
