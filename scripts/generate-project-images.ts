/**
 * Generate OG images, Twitter images, and icons for all website projects
 * Adapted from parent obsidian repo's scripts/src/generate-project-images.ts
 */

import dotenv from 'dotenv';
import path from 'path';
import { generateAndSaveImages } from './lib/genai-image.js';

// Load environment variables
dotenv.config();

interface ProjectImageConfig {
  key: string;
  name: string;
  description: string;
  ogPrompt: string;
  twitterPrompt?: string;
  iconPrompt?: string;
  outputDir: string;
  filePrefix: string;
}

// Neobrutalist style guide with 90s computer program aesthetic
const STYLE_GUIDE = `
Style: Modern neobrutalist design blended with 90s computer program aesthetic



`;

const PROJECT_CONFIGS: ProjectImageConfig[] = [
  {
    key: 'war-on-disease',
    name: 'War on Disease Book',
    description: 'How to End War and Disease',
    ogPrompt: `Create a powerful 1950s-style propaganda poster for a "War on Disease" campaign.
      ${STYLE_GUIDE}
      Content:
      - Central imagery: Heroic medical workers or scientists in bold silhouette style
      - Medical symbols: Stethoscope, DNA helix, microscope, pills integrated into design
      - Bold text: "WAR ON DISEASE" in large uppercase military-style typography
      - Subtitle: "SAVE 416 MILLION LIVES • ACCELERATE CURES BY 8 YEARS"
      - Key stat callout: "150,000 DEATHS DAILY UNDER CURRENT SYSTEM"
      - Visual metaphor: Defeating disease like defeating an enemy
      - Retro-futuristic aesthetic: 1950s meets modern medical science
      Layout: Centered composition, thick black borders, asymmetric color blocks
      Size: Social media OG format, landscape orientation
      Mood: Urgent, inspiring, patriotic, empowering, hopeful`,
    iconPrompt: `Square icon/logo for War on Disease campaign.
      ${STYLE_GUIDE}
      Content: Bold "WOD" monogram or medical cross symbol with military-style star
      Layout: Centered, symmetrical, works at small sizes (32x32 to 512x512)
      Simple, iconic, memorable
      Transparent background`,
    outputDir: 'assets/icons',
    filePrefix: 'war-on-disease'
  },

  {
    key: 'economics',
    name: 'Disease Eradication Economics',
    description: 'Economic Analysis of Health Investment',
    ogPrompt: `Create a professional, data-driven design for "1% Treaty Health and Economic Impact Analysis".
      ${STYLE_GUIDE}
      Content:
      - Main title: "1% TREATY" in large, bold typography with modern diplomatic styling
      - Subtitle: "HEALTH AND ECONOMIC IMPACT ANALYSIS" in clean, professional font
      - Key metrics prominently displayed:
        * "416 MILLION LIVES SAVED"
        * "$1.19 QUADRILLION VALUE GENERATED"
        * "451:1 ROI" or "1.19 MILLION:1 ROI"
        * "8 YEARS ACCELERATION"
        * "$27.2B ANNUALLY" (from 1% global military spending)
      - Visual elements: Economic and health data visualization
        * Rising bar charts showing 22.8× trial capacity increase
        * Dollar signs and economic growth indicators ($1.19 quadrillion)
        * Medical symbols (caduceus, heartbeat lines, pills)
        * Global map or interconnected nations
        * Upward trending arrows and graphs
      - Data points: "1%" prominently featured as key metric
      - Symbols suggesting: International cooperation, treaty signing, global health, economic prosperity
      - Color scheme: Professional blues and greens for trust/health, gold for economic growth
      - Elements: Document/treaty imagery, handshake symbols, world flags
      Layout: Professional report cover with data visualization elements
      Size: Social media OG format, landscape orientation
      Mood: Authoritative, optimistic, professional, data-driven, impactful, diplomatic
      Audience: Policy makers, economists, health officials, government leaders, NGOs`,

    iconPrompt: `Square icon/logo for 1% Treaty.
      ${STYLE_GUIDE}
      Content: "1%" in bold typography with medical cross and economic growth arrow
      Alternative: Globe with handshake or treaty scroll with health symbol
      Professional, authoritative, simple
      Works at small sizes (32x32 to 512x512)
      Transparent background`,
    outputDir: 'assets/economics',
    filePrefix: 'economics'
  }
];

async function generateImagesForProject(
  projectConfig: ProjectImageConfig,
  imageTypes: string[] = ['og', 'twitter', 'icon']
): Promise<void> {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`Generating images for: ${projectConfig.name}`);
  console.log(`${'='.repeat(60)}\n`);

  const outputDir = path.join(process.cwd(), projectConfig.outputDir);

  // Generate OG Image (1200x630, 16:9)
  if (imageTypes.includes('og')) {
    console.log('📱 Generating OG image (1200x630)...');
    await generateAndSaveImages({
      prompt: projectConfig.ogPrompt,
      aspectRatio: '16:9',
      outputDir,
      filePrefix: `${projectConfig.filePrefix}-og`,
    });
  }

  // Generate Twitter OG Image (1200x675, 16:9) - use same prompt as OG if no specific Twitter prompt
  if (imageTypes.includes('twitter')) {
    console.log('🐦 Generating Twitter card (1200x675)...');
    const twitterPrompt = projectConfig.twitterPrompt || projectConfig.ogPrompt;
    await generateAndSaveImages({
      prompt: twitterPrompt,
      aspectRatio: '16:9',
      outputDir,
      filePrefix: `${projectConfig.filePrefix}-twitter`,
    });
  }

  // Generate Square Icon (1:1)
  if (imageTypes.includes('icon')) {
    if (projectConfig.iconPrompt) {
      console.log('🎨 Generating square icon (512x512)...');
      await generateAndSaveImages({
        prompt: projectConfig.iconPrompt,
        aspectRatio: '1:1',
        outputDir,
        filePrefix: `${projectConfig.filePrefix}-icon`,
      });
    }
  }

  console.log(`\n✓ Completed image generation for ${projectConfig.name}\n`);
}

async function main() {
  console.log('🎨 Project Image Generator');
  console.log('='.repeat(60));

  // Check for API key
  if (!process.env.GOOGLE_GENERATIVE_AI_API_KEY) {
    console.error('ERROR: GOOGLE_GENERATIVE_AI_API_KEY environment variable is not set');
    console.error('Please set your Google Gemini API key in .env file:');
    console.error('GOOGLE_GENERATIVE_AI_API_KEY=your_api_key_here');
    console.error('Get your API key from: https://aistudio.google.com/app/apikey');
    process.exit(1);
  }

  // Parse command line arguments
  const args = process.argv.slice(2);
  const specificProject = args[0]; // e.g., "war-on-disease" or "all"

  let projectsToGenerate: ProjectImageConfig[];

  if (specificProject && specificProject !== 'all') {
    const project = PROJECT_CONFIGS.find(p => p.key === specificProject);
    if (!project) {
      console.error(`ERROR: Project "${specificProject}" not found`);
      console.error('Available projects:');
      PROJECT_CONFIGS.forEach(p => console.error(`  - ${p.key}`));
      process.exit(1);
    }
    projectsToGenerate = [project];
    console.log(`Generating images for: ${project.name}\n`);
  } else {
    projectsToGenerate = PROJECT_CONFIGS;
    console.log(`Generating images for all ${PROJECT_CONFIGS.length} projects\n`);
  }

  // Generate images for each project
  for (const project of projectsToGenerate) {
    try {
      await generateImagesForProject(project);
    } catch (error) {
      console.error(`Failed to generate images for ${project.name}:`, error);
      // Continue with next project instead of failing completely
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('✓ Image generation complete!');
  console.log('='.repeat(60));
}

// Run the script
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});

export { generateImagesForProject, PROJECT_CONFIGS };
