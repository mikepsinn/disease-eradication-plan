import sharp from 'sharp';
import fs from 'fs';
import path from 'path';

const squareIconInputPath = 'assets/icons/dih-icon-6-square.PNG';
const wideIconInputPath = 'assets/icons/dih-icon-6-wide.png';
const outputDir = 'assets/icons/generated';
const squareSizes = [32, 128, 180, 192, 512];
const wideWidth = 1280;
const wideHeight = 640;

async function generateIcons() {
  try {
    // Ensure output directory exists
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // Generate square icons
    console.log(`Generating square icons from ${squareIconInputPath}`);
    const squareImage = sharp(squareIconInputPath);
    for (const size of squareSizes) {
      const outputFilePath = path.join(
        outputDir,
        `dih-icon-${size}x${size}.png`
      );
      await squareImage
        .resize({ width: size, height: size })
        .toFile(outputFilePath);

      const stats = fs.statSync(outputFilePath);
      console.log(`Created ${outputFilePath} (${stats.size} bytes)`);
    }
    console.log('All square icon sizes generated successfully.');

    // Generate wide icon
    console.log(`Generating wide icon from ${wideIconInputPath}`);
    const wideImage = sharp(wideIconInputPath);

    const wideOutputFilePath = path.join(
      outputDir,
      `dih-icon-wide-${wideWidth}x${wideHeight}.png`
    );
    await wideImage
      .resize({ width: wideWidth, height: wideHeight })
      .toFile(wideOutputFilePath);

    const stats = fs.statSync(wideOutputFilePath);
    console.log(`Created ${wideOutputFilePath} (${stats.size} bytes)`);
    console.log('Wide icon generated successfully.');
  } catch (error) {
    console.error('Error resizing images:', error);
  }
}

generateIcons();
