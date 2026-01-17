
import fs from 'fs';
import path from 'path';
import { glob } from 'glob';
import sharp from 'sharp';

// Configuration
const SCAN_DIR = 'assets';
const MIN_SIZE_BYTES = 50 * 1024; // Lower threshold to 50KB to catch more files
const REPORT_FILE = 'IMAGE_COMPRESSION_REPORT.md';
const TOP_OPPORTUNITIES_COUNT = 50; // How many top files to list in detailed table

async function formatBytes(bytes: number) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

async function estimateCompression() {
    const rootDir = process.cwd();
    console.log(`Scanning for ALL images in ${SCAN_DIR} > ${await formatBytes(MIN_SIZE_BYTES)}...`);

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
    }).filter(s => s.size > MIN_SIZE_BYTES);

    // Sort by size initially for processing order (biggest first is usually most interesting)
    allImages.sort((a, b) => b.size - a.size);

    console.log(`Found ${allImages.length} images to analyze.`);
    console.log('Starting analysis (this may take a moment)...');

    let report = `# Image Compression Analysis Report (Same Format Only)\n\n`;
    report += `Generated at: ${new Date().toISOString()}\n`;
    report += `Scope: All images in \`${SCAN_DIR}\` > ${await formatBytes(MIN_SIZE_BYTES)}\n\n`;

    let totalOriginal = 0;
    let totalOptimized = 0;
    let processedCount = 0;

    const opportunities: Array<{ file: string, original: number, optimized: number, savings: number, percent: number }> = [];

    for (const img of allImages) {
        totalOriginal += img.size;
        processedCount++;

        if (processedCount % 10 === 0) {
            process.stdout.write(`\rProcessed ${processedCount}/${allImages.length} images...`);
        }

        const input = sharp(img.path, { animated: true });

        let optimizedBuffer: Buffer | null = null;
        try {
            if (img.ext === '.png') {
                // PNG: moderate compression, keep palette if possible, quality 80 is usually safe visual fidelity
                // effort 10 is max compression effort for png
                optimizedBuffer = await input.clone().png({ quality: 80, compressionLevel: 6, palette: true }).toBuffer();
            } else if (img.ext === '.jpg' || img.ext === '.jpeg') {
                // JPEG: mozjpeg is great, quality 80 is very high standard
                optimizedBuffer = await input.clone().jpeg({ quality: 80, mozjpeg: true }).toBuffer();
            } else if (img.ext === '.gif') {
                // GIF: difficult to compress without changing format, but we'll try basic optimization
                optimizedBuffer = await input.clone().gif({ effort: 1 }).toBuffer();
            } else if (img.ext === '.webp') {
                optimizedBuffer = await input.clone().webp({ quality: 80 }).toBuffer();
            }
        } catch (e) {
            // console.warn(`Error optimizing ${img.file}: ${e}`);
        }

        let optSize = img.size;
        if (optimizedBuffer && optimizedBuffer.length < img.size) {
            optSize = optimizedBuffer.length;
        }

        totalOptimized += optSize;

        if (optSize < img.size) {
            opportunities.push({
                file: img.file,
                original: img.size,
                optimized: optSize,
                savings: img.size - optSize,
                percent: ((img.size - optSize) / img.size) * 100
            });
        }
    }

    process.stdout.write('\n'); // Newline after progress

    // Sort opportunities by raw bytes saved
    opportunities.sort((a, b) => b.savings - a.savings);

    const totalSaved = totalOriginal - totalOptimized;

    report += `## Summary\n\n`;
    report += `- **Total Images Scanned**: ${allImages.length}\n`;
    report += `- **Total Original Size**: ${await formatBytes(totalOriginal)}\n`;
    report += `- **Estimated Optimized Size**: ${await formatBytes(totalOptimized)}\n`;
    report += `- **Total Potential Savings**: **${await formatBytes(totalSaved)}** (${((totalSaved / totalOriginal) * 100).toFixed(1)}%)\n\n`;

    report += `## Top ${TOP_OPPORTUNITIES_COUNT} Optimization Opportunities\n\n`;
    report += `| File | Original | Optimized | Savings | %\n`;
    report += `|---|---|---|---|---|\n`;

    for (const op of opportunities.slice(0, TOP_OPPORTUNITIES_COUNT)) {
        report += `| \`${op.file}\` | ${await formatBytes(op.original)} | ${await formatBytes(op.optimized)} | ${await formatBytes(op.savings)} | ${op.percent.toFixed(1)}% |\n`;
    }

    fs.writeFileSync(path.join(rootDir, REPORT_FILE), report, 'utf8');
    console.log(`\nAnalysis complete. Report written to ${REPORT_FILE}`);
    console.log(`Potential Savings: ${await formatBytes(totalSaved)}`);
}

estimateCompression().catch(console.error);
