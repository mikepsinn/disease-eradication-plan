import path from 'path';
import { getBookFilesForProcessing, readFileWithMatter, extractImagePaths, getProjectRoot } from './lib/file-utils';
import fs from 'fs';

async function listNonBwImages() {
  const ROOT_DIR = getProjectRoot();
  const bookFiles = await getBookFilesForProcessing();

  let totalImages = 0;
  let filteredImages = 0;

  const results: { file: string; images: string[] }[] = [];

  for (const relFile of bookFiles) {
    const absPath = path.resolve(ROOT_DIR, relFile);

    // Only skip index.qmd specifically
    if (!fs.existsSync(absPath)) {
      if (relFile === 'index.qmd') {
        console.warn(`  [SKIP] File not found: ${relFile} (index.qmd is optional)`);
        continue;
      } else {
        throw new Error(`ERROR: Required file not found: ${relFile}\nAbsolute path: ${absPath}\n\nThis is not index.qmd, so the script is stopping.`);
      }
    }

    const { body } = await readFileWithMatter(absPath);
    const imagePaths = extractImagePaths(body);

    const nonBw = imagePaths.filter(img => {
      const basename = path.basename(img);
      return !basename.includes('bw-academic');
    });

    totalImages += imagePaths.length;
    filteredImages += nonBw.length;

    if (nonBw.length > 0) {
      results.push({ file: relFile, images: nonBw });
    }
  }

  console.log(`\n${'='.repeat(60)}`);
  console.log(`Images without "bw-academic" in filename`);
  console.log(`${'='.repeat(60)}\n`);

  for (const { file, images } of results) {
    console.log(`${file}`);
    for (const img of images) {
      const absImg = path.resolve(ROOT_DIR, path.dirname(file), img);
      const exists = fs.existsSync(absImg) || fs.existsSync(path.resolve(ROOT_DIR, img.replace(/^\//, '')));
      const status = exists ? '' : ' [MISSING]';
      console.log(`  ${img}${status}`);
    }
    console.log('');
  }

  console.log(`${'='.repeat(60)}`);
  console.log(`Total images: ${totalImages}`);
  console.log(`Without bw-academic: ${filteredImages}`);
  console.log(`With bw-academic (excluded): ${totalImages - filteredImages}`);
  console.log(`Files with non-bw images: ${results.length}`);
}

listNonBwImages().catch(console.error);
