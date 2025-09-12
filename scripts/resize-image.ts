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
      const pngOutputFilePath = path.join(
        outputDir,
        `dih-icon-${size}x${size}.png`
      );
      const jpgOutputFilePath = path.join(
        outputDir,
        `dih-icon-${size}x${size}.jpg`
      );

      const resizedImage = squareImage.resize({ width: size, height: size });

      // Save as PNG
      await resizedImage.toFile(pngOutputFilePath);
      let stats = fs.statSync(pngOutputFilePath);
      console.log(`Created ${pngOutputFilePath} (${stats.size} bytes)`);

      // Save as JPG
      await resizedImage.jpeg().toFile(jpgOutputFilePath);
      stats = fs.statSync(jpgOutputFilePath);
      console.log(`Created ${jpgOutputFilePath} (${stats.size} bytes)`);
    }
    console.log('All square icon sizes generated successfully.');

    // Generate wide icon
    console.log(`Generating wide icon from ${wideIconInputPath}`);
    const wideImage = sharp(wideIconInputPath);

    const widePngOutputFilePath = path.join(
      outputDir,
      `dih-icon-wide-${wideWidth}x${wideHeight}.png`
    );
    const wideJpgOutputFilePath = path.join(
      outputDir,
      `dih-icon-wide-${wideWidth}x${wideHeight}.jpg`
    );

    const resizedWideImage = wideImage.resize({
      width: wideWidth,
      height: wideHeight,
    });

    // Save as PNG
    await resizedWideImage.toFile(widePngOutputFilePath);
    let stats = fs.statSync(widePngOutputFilePath);
    console.log(`Created ${widePngOutputFilePath} (${stats.size} bytes)`);

    // Save as JPG
    await resizedWideImage.jpeg().toFile(wideJpgOutputFilePath);
    stats = fs.statSync(wideJpgOutputFilePath);
    console.log(`Created ${wideJpgOutputFilePath} (${stats.size} bytes)`);

    console.log('Wide icons generated successfully.');
  } catch (error) {
    console.error('Error resizing images:', error);
  }
}

generateIcons();
