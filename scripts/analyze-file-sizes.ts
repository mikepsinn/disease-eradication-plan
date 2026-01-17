import fs from 'fs';
import path from 'path';
import { glob } from 'glob';
import ignore from 'ignore';

// Configuration for Glob (Performance optimizations)
// We explicitely ignore these heavy directories to avoid scanning them before filtering
const PERFORMANCE_IGNORES = [
    'node_modules/**',
    '.git/**',
    '.quarto/**',
    '_site/**',
    '_freeze/**',
    '_book/**',
    '.turbo/**',
    'coverage/**',
    'dist/**',
    '_build_temp/**',
    '.recent/**'
];

const TOP_FILES_COUNT = 50;
const TOP_DIRS_COUNT = 50;
const REPORT_FILE = 'FILE_SIZES_REPORT.md';

async function analyzeFileSizes() {
    const rootDir = process.cwd();
    console.log(`Analyzing file sizes in ${rootDir}...`);

    // 1. Prepare Gitignore Filter
    const ig = ignore();
    try {
        const gitignorePath = path.join(rootDir, '.gitignore');
        if (fs.existsSync(gitignorePath)) {
            const gitignoreContent = fs.readFileSync(gitignorePath, 'utf8');
            ig.add(gitignoreContent);
            console.log('Loaded .gitignore rules.');
        }
    } catch (err) {
        console.warn('Failed to load .gitignore:', err);
    }

    // 2. Scan Files
    const allFiles = await glob('**/*', {
        ignore: PERFORMANCE_IGNORES,
        nodir: true,
        dot: true,
        cwd: rootDir
    });

    // 3. Filter using gitignore
    // ignore.ignores(path) returns true if the path is ignored
    const files = allFiles.filter(f => !ig.ignores(f));

    console.log(`Found ${allFiles.length} files, ${files.length} after applying .gitignore.`);

    // 4. Collect Stats
    const fileStats: { path: string; size: number }[] = [];
    const dirStats: Record<string, number> = {};

    for (const file of files) {
        try {
            const fullPath = path.join(rootDir, file);
            const stats = fs.statSync(fullPath);
            const size = stats.size;

            fileStats.push({ path: file, size });

            // Aggregate directory sizes
            let currentDir = path.dirname(file);
            while (currentDir !== '.') {
                dirStats[currentDir] = (dirStats[currentDir] || 0) + size;
                const parentDir = path.dirname(currentDir);
                if (parentDir === currentDir) break; // Root reached
                currentDir = parentDir;
            }
            // Add to root '.'
            dirStats['.'] = (dirStats['.'] || 0) + size;

        } catch (error) {
            // console.warn(`Could not stat file: ${file}`);
        }
    }

    // 5. Sort
    fileStats.sort((a, b) => b.size - a.size);

    const sortedDirs = Object.entries(dirStats)
        .sort(([, sizeA], [, sizeB]) => sizeB - sizeA)
        .map(([dir, size]) => ({ dir, size }));

    // Helper to format bytes
    const formatBytes = (bytes: number) => {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    // 6. Generate Markdown Report
    let report = `# File Size Analysis Report\n\n`;
    report += `Generated at: ${new Date().toISOString()}\n`;
    report += `Total Size (Verified): ${formatBytes(dirStats['.'] || 0)}\n\n`;

    report += `## Top ${TOP_FILES_COUNT} Largest Files\n\n`;
    report += `| Rank | File | Size |\n`;
    report += `|---|---|---|\n`;
    fileStats.slice(0, TOP_FILES_COUNT).forEach((f, index) => {
        report += `| ${index + 1} | \`${f.path}\` | ${formatBytes(f.size)} |\n`;
    });

    report += `\n## Top ${TOP_DIRS_COUNT} Largest Directories (Recursive)\n\n`;
    report += `| Rank | Directory | Size |\n`;
    report += `|---|---|---|\n`;
    sortedDirs.slice(0, TOP_DIRS_COUNT).forEach((d, index) => {
        report += `| ${index + 1} | \`${d.dir}\` | ${formatBytes(d.size)} |\n`;
    });

    // 7. Write Report
    fs.writeFileSync(path.join(rootDir, REPORT_FILE), report, 'utf8');
    console.log(`\nReport written to ${REPORT_FILE}`);

    // Also log top 10 to console for immediate feedback
    console.log('\n--- Top 10 Files ---');
    fileStats.slice(0, 10).forEach((f, i) => console.log(`${i + 1}. ${f.path} (${formatBytes(f.size)})`));
}

analyzeFileSizes().catch(console.error);
