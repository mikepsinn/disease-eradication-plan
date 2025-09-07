import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import simpleGit from 'simple-git';
import matter from 'gray-matter';

const ROOT_DIR = path.resolve(__dirname, '..');
const IGNORED_DIRS = ['node_modules', '.git', 'assets', '.github', '.cursor-cache'];
const CACHE_FILE = path.join(ROOT_DIR, '.article-cache.json');
const OUTPUT_FILE = path.join(ROOT_DIR, 'operations', 'digital-twin.yml');

interface CacheEntry {
    assessment: {
        qualityScore: number;
        todos: string[];
    };
    timestamp: number;
}

interface ContentManifest {
    [filePath: string]: {
        title?: string;
        description?: string;
        last_modified_git?: string;
        last_analyzed_ai?: string;
        quality_score?: number;
        actionable_tasks?: string[];
    };
}

async function findMarkdownFiles(dir: string): Promise<string[]> {
    let mdFiles: string[] = [];
    const entries = await fs.promises.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (IGNORED_DIRS.some(p => fullPath.includes(path.sep + p))) continue;
        if (entry.isDirectory()) {
            mdFiles = mdFiles.concat(await findMarkdownFiles(fullPath));
        } else if (entry.isFile() && (entry.name.endsWith('.md') || entry.name.endsWith('.mdc'))) {
            mdFiles.push(fullPath);
        }
    }
    return mdFiles;
}

async function getGitLastModified(git: any, filePath: string): Promise<string | undefined> {
    try {
        const log = await git.log({ file: filePath, maxCount: 1 });
        return log.latest?.date;
    } catch (e) {
        return undefined;
    }
}

async function generateManifest() {
    console.log('Generating content manifest...');
    const git = simpleGit(ROOT_DIR);
    const manifest: ContentManifest = {};

    const allFiles = await findMarkdownFiles(ROOT_DIR);
    const cache = fs.existsSync(CACHE_FILE) ? JSON.parse(fs.readFileSync(CACHE_FILE, 'utf-8')) : {};

    for (const filePath of allFiles) {
        const relativePath = './' + path.relative(ROOT_DIR, filePath).replace(/\\/g, '/');
        manifest[relativePath] = {};

        // 1. Get Git metadata
        manifest[relativePath].last_modified_git = await getGitLastModified(git, filePath);

        // 2. Get Frontmatter metadata
        const fileContent = await fs.promises.readFile(filePath, 'utf-8');
        const { data: frontmatter } = matter(fileContent);
        manifest[relativePath].title = frontmatter.title || 'Untitled';
        manifest[relativePath].description = frontmatter.description || '';

        // 3. Get AI Analysis metadata from cache
        const cacheKey = path.resolve(filePath); // Ensure absolute path for cache lookup
        const cacheEntry: CacheEntry = cache[cacheKey];
        if (cacheEntry) {
            manifest[relativePath].last_analyzed_ai = new Date(cacheEntry.timestamp).toISOString();
            manifest[relativePath].quality_score = cacheEntry.assessment.qualityScore;
            manifest[relativePath].actionable_tasks = cacheEntry.assessment.todos?.map(todo =>
                todo.replace(/<!-- TODO: (.*?) -->/, '$1').trim()
            );
        }
    }

    const yamlManifest = yaml.dump(manifest, { indent: 2 });
    await fs.promises.writeFile(OUTPUT_FILE, yamlManifest);

    console.log(`Content manifest successfully generated at: ${OUTPUT_FILE}`);
}

if (require.main === module) {
    generateManifest().catch(console.error);
}
