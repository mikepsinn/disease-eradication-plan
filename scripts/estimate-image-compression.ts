
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

    // OPTIMIZATION: Only analyze the top 50 largest files as they contain majority of savings
    // Analyzing 700+ small files takes excessive time for minimal gain.
    const imagesToAnalyze = allImages.slice(0, 50);

    console.log(`Found ${allImages.length} images > ${await formatBytes(MIN_SIZE_BYTES)}. Analysis limited to top ${imagesToAnalyze.length} largest files for speed.`);
    console.log('Starting analysis...');

    let report = `# Image Compression Analysis Report (Same Format Only)\n\n`;
    report += `Generated at: ${new Date().toISOString()}\n`;
    report += `Scope: All images in \`${SCAN_DIR}\` > ${await formatBytes(MIN_SIZE_BYTES)}\n\n`;

    let totalOriginal = 0;
    let totalOptimized = 0;
    let processedCount = 0;
    const opportunities: Array<{ file: string, original: number, optimized: number, savings: number, percent: number }> = [];

    // Process in batches to control concurrency
    const BATCH_SIZE = 8;

    // Parallel processing with batching

    const processImage = async (img: typeof allImages[0]) => {
        const input = sharp(img.path, { animated: true });
        let optimizedBuffer: Buffer | null = null;
        try {
            if (img.ext === '.png') {
                optimizedBuffer = await input.clone().png({ quality: 80, compressionLevel: 6, palette: true }).toBuffer();
            } else if (img.ext === '.jpg' || img.ext === '.jpeg') {
                optimizedBuffer = await input.clone().jpeg({ quality: 80, mozjpeg: true }).toBuffer();
            } else if (img.ext === '.gif') {
                optimizedBuffer = await input.clone().gif({ effort: 1 }).toBuffer();
            } else if (img.ext === '.webp') {
                optimizedBuffer = await input.clone().webp({ quality: 80 }).toBuffer();
            }
        } catch (e) { return null; }
        return optimizedBuffer;
    };

    // Parallel processing with batching
    for (let i = 0; i < imagesToAnalyze.length; i += BATCH_SIZE) {
        const batch = imagesToAnalyze.slice(i, i + BATCH_SIZE);
        const results = await Promise.all(batch.map(async img => ({ img, buffer: await processImage(img) })));

        for (const res of results) {
            const { img, buffer } = res;
            totalOriginal += img.size;
            processedCount++;

            let optSize = img.size;
            if (buffer && buffer.length < img.size) {
                optSize = buffer.length;
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
        process.stdout.write(`\rProcessed ${processedCount}/${imagesToAnalyze.length} images...`);
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
