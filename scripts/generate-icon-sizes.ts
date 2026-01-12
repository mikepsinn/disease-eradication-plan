
import sharp from 'sharp';
import path from 'path';
import fs from 'fs';

const INPUT_FILE = 'dfda-logo.png';
const OUTPUT_DIR = 'assets/icons';

const SIZES = {
    'dfda-favicon-16x16.png': 16,
    'dfda-favicon-32x32.png': 32,
    'dfda-favicon-48x48.png': 48,
    'dfda-favicon.png': 64, // Default favicon size if not specified otherwise
    'dfda-apple-touch-icon.png': 180,
    'dfda-android-chrome-192x192.png': 192,
    'dfda-android-chrome-512x512.png': 512,
    'dfda-favicon-master.png': 1024, // Assuming we want a master too, though not strictly required if we have the source
};

async function main() {
    const rootDir = process.cwd();
    const inputPath = path.join(rootDir, INPUT_FILE);
    const outputDir = path.join(rootDir, OUTPUT_DIR);

    if (!fs.existsSync(inputPath)) {
        console.error(`Input file not found: ${inputPath}`);
        process.exit(1);
    }

    if (!fs.existsSync(outputDir)) {
        console.log(`Creating output directory: ${outputDir}`);
        fs.mkdirSync(outputDir, { recursive: true });
    }

    console.log(`Processing ${inputPath}...`);

    for (const [filename, size] of Object.entries(SIZES)) {
        const outputPath = path.join(outputDir, filename);

        try {
            await sharp(inputPath)
                .resize(size, size, {
                    fit: 'contain',
                    background: { r: 0, g: 0, b: 0, alpha: 0 }
                })
                .toFile(outputPath);

            console.log(`Generated ${filename} (${size}x${size})`);
        } catch (err) {
            console.error(`Error generating ${filename}:`, err);
        }
    }

    console.log('Done.');
}

main().catch(console.error);
