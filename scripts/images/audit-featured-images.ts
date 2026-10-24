/**
 * Audit page-specific featured images for QMD pages in _quarto-manual.yml.
 *
 * Usage:
 *   npx tsx scripts/images/audit-featured-images.ts
 *   npx tsx scripts/images/audit-featured-images.ts --json
 *   npx tsx scripts/images/audit-featured-images.ts --fix-existing
 */

import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import yaml from 'js-yaml';

const ROOT = process.cwd();
const CONFIG_PATH = path.join(ROOT, '_quarto-manual.yml');
const IMAGE_EXTENSIONS = new Set(['.jpg', '.jpeg', '.png', '.webp']);

interface QuartoDocument {
  book?: { chapters?: unknown[] };
  'dih-render'?: { 'index-source'?: string };
}

interface FeaturedImageStatus {
  file: string;
  image: string | null;
  status: 'valid' | 'reusable' | 'generate';
  reusableImage: string | null;
}

function toPosix(filePath: string): string {
  return filePath.replace(/\\/g, '/');
}

function collectQmdFiles(items: unknown[], output: string[]): void {
  for (const item of items) {
    if (typeof item === 'string') {
      if (item.endsWith('.qmd')) output.push(item);
      continue;
    }

    if (!item || typeof item !== 'object') continue;
    const entry = item as { href?: unknown; chapters?: unknown; contents?: unknown };

    if (typeof entry.href === 'string' && entry.href.endsWith('.qmd')) {
      output.push(entry.href);
    }
    if (Array.isArray(entry.chapters)) collectQmdFiles(entry.chapters, output);
    if (Array.isArray(entry.contents)) collectQmdFiles(entry.contents, output);
  }
}

function getManualQmdFiles(): { placements: number; files: string[] } {
  const document = yaml.load(fs.readFileSync(CONFIG_PATH, 'utf8')) as QuartoDocument;
  const configured: string[] = [];
  collectQmdFiles(document.book?.chapters ?? [], configured);

  const indexSource = document['dih-render']?.['index-source'];
  const resolved = configured.map((file) => {
    if (file === 'index.qmd' && indexSource) return indexSource;
    return file;
  });

  return {
    placements: configured.length,
    files: [...new Set(resolved.map(toPosix))],
  };
}

function resolveRepoPath(reference: string): string {
  return path.join(ROOT, reference.replace(/^[/\\]+/, ''));
}

function candidatePriority(fileName: string): number {
  if (fileName.endsWith('-og-bw-academic.jpg')) return 0;
  if (fileName.endsWith('-og-retro-academic.jpg')) return 1;
  if (fileName.endsWith('-og.jpg')) return 2;
  return 3;
}

function findReusableImage(qmdFile: string): string | null {
  const parsed = path.parse(qmdFile);
  const imageDir = path.join(ROOT, 'assets', 'og-images', parsed.dir);
  if (!fs.existsSync(imageDir)) return null;

  const prefix = `${parsed.name}-og`;
  const candidates = fs.readdirSync(imageDir)
    .filter((fileName) => fileName.startsWith(prefix))
    .filter((fileName) => IMAGE_EXTENSIONS.has(path.extname(fileName).toLowerCase()))
    .sort((a, b) => candidatePriority(a) - candidatePriority(b) || a.localeCompare(b));

  if (candidates.length === 0) return null;
  return `/${toPosix(path.join('assets', 'og-images', parsed.dir, candidates[0]))}`;
}

function auditFile(qmdFile: string): FeaturedImageStatus {
  const absolutePath = path.join(ROOT, qmdFile);
  if (!fs.existsSync(absolutePath)) {
    throw new Error(`Configured QMD file does not exist: ${qmdFile}`);
  }

  const frontmatter = matter(fs.readFileSync(absolutePath, 'utf8')).data;
  const image = typeof frontmatter.image === 'string' ? frontmatter.image : null;

  if (image && fs.existsSync(resolveRepoPath(image))) {
    return { file: qmdFile, image, status: 'valid', reusableImage: null };
  }

  const reusableImage = findReusableImage(qmdFile);
  return {
    file: qmdFile,
    image,
    status: reusableImage ? 'reusable' : 'generate',
    reusableImage,
  };
}

function setFrontmatterImage(qmdFile: string, image: string): void {
  const absolutePath = path.join(ROOT, qmdFile);
  const raw = fs.readFileSync(absolutePath, 'utf8');
  const lineEnding = raw.includes('\r\n') ? '\r\n' : '\n';
  const opening = `---${lineEnding}`;

  if (!raw.startsWith(opening)) {
    throw new Error(`QMD file has no YAML frontmatter: ${qmdFile}`);
  }

  const closingIndex = raw.indexOf(`${lineEnding}---`, opening.length);
  if (closingIndex === -1) {
    throw new Error(`QMD frontmatter is not closed: ${qmdFile}`);
  }

  const header = raw.slice(opening.length, closingIndex);
  const imageLine = `image: ${image}`;
  const updatedHeader = /^image:[^\r\n]*$/m.test(header)
    ? header.replace(/^image:[^\r\n]*$/m, imageLine)
    : `${header}${header ? lineEnding : ''}${imageLine}`;

  fs.writeFileSync(
    absolutePath,
    `${opening}${updatedHeader}${raw.slice(closingIndex)}`,
    'utf8',
  );
}

function summarize(placements: number, statuses: FeaturedImageStatus[]) {
  return {
    config: path.basename(CONFIG_PATH),
    placements,
    uniqueQmdFiles: statuses.length,
    valid: statuses.filter((entry) => entry.status === 'valid').length,
    reusable: statuses.filter((entry) => entry.status === 'reusable').length,
    generate: statuses.filter((entry) => entry.status === 'generate').length,
    missingUsableImage: statuses.filter((entry) => entry.status !== 'valid').length,
  };
}

function printReport(placements: number, statuses: FeaturedImageStatus[]): void {
  const summary = summarize(placements, statuses);
  console.log('Manual featured-image audit');
  console.log(JSON.stringify(summary, null, 2));

  const reusable = statuses.filter((entry) => entry.status === 'reusable');
  if (reusable.length > 0) {
    console.log('\nExisting images that can be linked:');
    for (const entry of reusable) {
      console.log(`  ${entry.file} -> ${entry.reusableImage}`);
    }
  }

  const generate = statuses.filter((entry) => entry.status === 'generate');
  if (generate.length > 0) {
    console.log('\nImages that must be generated:');
    for (const entry of generate) console.log(`  ${entry.file}`);
  }
}

function main(): void {
  const args = new Set(process.argv.slice(2));
  const { placements, files } = getManualQmdFiles();
  let statuses = files.map(auditFile);

  if (args.has('--fix-existing')) {
    for (const entry of statuses) {
      if (entry.status === 'reusable' && entry.reusableImage) {
        setFrontmatterImage(entry.file, entry.reusableImage);
      }
    }
    statuses = files.map(auditFile);
  }

  if (args.has('--json')) {
    console.log(JSON.stringify({ summary: summarize(placements, statuses), files: statuses }, null, 2));
    return;
  }

  printReport(placements, statuses);
}

main();
