import sharp from 'sharp';
import fs from 'fs';
import path from 'path';

const inputFilePath = 'assets/icons/dih-icon-4-square.PNG';
const outputDir = 'assets/icons/generated';
const sizes = [32, 128, 180, 192, 512];

async function resizeImages() {
  try {
    // Ensure output directory exists
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    const image = sharp(inputFilePath);
    const metadata = await image.metadata();
    console.log('Original image metadata:', metadata);

    for (const size of sizes) {
      const outputFilePath = path.join(outputDir, `dih-icon-${size}x${size}.png`);
      await image
        .resize({ width: size, height: size })
        .toFile(outputFilePath);

      const stats = fs.statSync(outputFilePath);
      console.log(`Created ${outputFilePath} (${stats.size} bytes)`);
    }

    console.log('All icon sizes generated successfully.');

  } catch (error) {
    console.error('Error resizing images:', error);
  }
}

resizeImages();
