
import fs from 'fs';
import path from 'path';
import { glob } from 'glob';
import sharp from 'sharp';

// Configuration
const SCAN_DIR = 'assets';
const MIN_SAVINGS_BYTES = 1 * 1024 * 1024; // 1MB
const REPORT_FILE = 'COMPRESSION_LOG.md';

async function formatBytes(bytes: number) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

async function compressHighImpactImages() {
    const rootDir = process.cwd();
    console.log(`Scanning for images in ${SCAN_DIR} with > ${await formatBytes(MIN_SAVINGS_BYTES)} potential savings...`);

    // Find images
    const files = await glob(`${SCAN_DIR}/**/*.{png,jpg,jpeg,gif,webp}`, {
        nodir: true,
        cwd: rootDir,
        ignore: ['**/node_modules/**', '**/dist/**', '**/_site/**']
    });

    const allImages = files.map(f => {
        const fullPath = path.join(rootDir, f);
        const stat = fs.statSync(fullPath);
        return { file: f, path: fullPath, size: stat.size, ext: path.extname(f).toLowerCase() };
    }).filter(s => s.size > MIN_SAVINGS_BYTES); // Fast filter: if file is smaller than savings threshold, impossible to save that much

    console.log(`Analyzing ${allImages.length} candidate images...`);

    let log = `# Compression Log\n\n`;
    log += `Generated at: ${new Date().toISOString()}\n`;
    log += `Threshold: Savings > ${await formatBytes(MIN_SAVINGS_BYTES)}\n\n`;
    log += `| File | Original | New Size | Saved |\n`;
    log += `|---|---|---|---|\n`;

    let totalSaved = 0;
    let processedCount = 0;

    for (const img of allImages) {
        const input = sharp(img.path, { animated: true });
        let optimizedBuffer: Buffer | null = null;

        // High quality settings to ensure no "detectable" loss
        // Using slightly higher quality settings than estimate script
        try {
            if (img.ext === '.png') {
                // PNG: quality 90, high compression effort
                optimizedBuffer = await input.clone().png({ quality: 90, compressionLevel: 9, palette: true, effort: 8 }).toBuffer();
            } else if (img.ext === '.jpg' || img.ext === '.jpeg') {
                // JPG: quality 90, mozjpeg
                optimizedBuffer = await input.clone().jpeg({ quality: 90, mozjpeg: true }).toBuffer();
            } else if (img.ext === '.gif') {
                // GIF: Keep it simple, just optimize structure
                optimizedBuffer = await input.clone().gif({ effort: 7 }).toBuffer();
            } else if (img.ext === '.webp') {
                optimizedBuffer = await input.clone().webp({ quality: 90 }).toBuffer();
            }
        } catch (e) {
            console.error(`Failed to process ${img.file}:`, e);
            continue;
        }

        if (optimizedBuffer) {
            const savings = img.size - optimizedBuffer.length;

            if (savings > MIN_SAVINGS_BYTES) {
                // Write the new file
                fs.writeFileSync(img.path, optimizedBuffer);

                totalSaved += savings;
                processedCount++;

                const savedStr = await formatBytes(savings);
                const origStr = await formatBytes(img.size);
                const newStr = await formatBytes(optimizedBuffer.length);

                console.log(`Compressed ${img.file}: saved ${savedStr}`);
                log += `| \`${img.file}\` | ${origStr} | ${newStr} | ${savedStr} |\n`;
            }
        }
    }

    log += `\n**Total Saved**: ${await formatBytes(totalSaved)}\n`;
    fs.writeFileSync(path.join(rootDir, REPORT_FILE), log, 'utf8');

    console.log(`\nCompression complete.`);
    console.log(`Processed ${processedCount} files.`);
    console.log(`Total saved: ${await formatBytes(totalSaved)}`);
}

compressHighImpactImages().catch(console.error);
