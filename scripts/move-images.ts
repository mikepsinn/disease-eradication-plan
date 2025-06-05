import * as fs from 'fs';
import * as path from 'path';
import { getAllFiles } from './shared-utilities';

const IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.PNG', '.JPG', '.JPEG', '.GIF', '.SVG', '.WEBP'];
const TARGET_DIR = 'assets/images';

interface MoveResult {
  from: string;
  to: string;
  success: boolean;
  error?: string;
}

async function moveImages(): Promise<void> {
  try {
    // Create target directory if it doesn't exist
    const targetDir = path.join(process.cwd(), TARGET_DIR);
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
    }

    // Get all image files
    const files = await getAllFiles(process.cwd(), IMAGE_EXTENSIONS);
    console.log(`Found ${files.length} image files`);

    // Filter out files already in assets folder
    const filesToMove = files.filter(file => !file.includes('assets'));
    console.log(`${filesToMove.length} images need to be moved`);

    if (filesToMove.length === 0) {
      console.log('No images to move!');
      return;
    }

    // Track file moves for updating references later
    const moves: MoveResult[] = [];

    // Move each file
    for (const file of filesToMove) {
      const fileName = path.basename(file);
      const targetPath = path.join(targetDir, fileName);

      // Handle filename conflicts
      let finalTargetPath = targetPath;
      let counter = 1;
      while (fs.existsSync(finalTargetPath)) {
        const ext = path.extname(fileName);
        const base = path.basename(fileName, ext);
        finalTargetPath = path.join(targetDir, `${base}_${counter}${ext}`);
        counter++;
      }

      try {
        // Move the file
        fs.renameSync(file, finalTargetPath);
        moves.push({
          from: file,
          to: finalTargetPath,
          success: true
        });
        console.log(`✓ Moved ${file} to ${finalTargetPath}`);
      } catch (error: any) {
        console.error(`✗ Failed to move ${file}:`, error.message);
        moves.push({
          from: file,
          to: finalTargetPath,
          success: false,
          error: error.message
        });
      }
    }

    // Update references in markdown and HTML files
    console.log('\nUpdating references in files...');
    const docsFiles = await getAllFiles(process.cwd(), ['.md', '.html']);

    for (const file of docsFiles) {
      let content = fs.readFileSync(file, 'utf8');
      let contentChanged = false;

      moves.forEach(move => {
        if (!move.success) return;

        // Convert paths to relative format for replacement
        const fromRelative = path.relative(path.dirname(file), move.from).replace(/\\/g, '/');
        const toRelative = path.relative(path.dirname(file), move.to).replace(/\\/g, '/');

        // Update markdown image references
        const mdPattern = new RegExp(`!\\[([^\\]]*)\\]\\(${escapeRegExp(fromRelative)}\\)`, 'g');
        const newContent = content.replace(mdPattern, `![$1](${toRelative})`);
        if (newContent !== content) {
          content = newContent;
          contentChanged = true;
        }

        // Update HTML image references
        const htmlPattern = new RegExp(`<img([^>]*)src=["']${escapeRegExp(fromRelative)}["']([^>]*)>`, 'g');
        const newContent2 = content.replace(htmlPattern, `<img$1src="${toRelative}"$2>`);
        if (newContent2 !== content) {
          content = newContent2;
          contentChanged = true;
        }
      });

      if (contentChanged) {
        fs.writeFileSync(file, content, 'utf8');
        console.log(`✓ Updated references in ${file}`);
      }
    }

    // Print summary
    console.log('\nSummary:');
    console.log(`Total images found: ${files.length}`);
    console.log(`Images moved: ${moves.filter(m => m.success).length}`);
    console.log(`Failed moves: ${moves.filter(m => !m.success).length}`);

  } catch (error) {
    console.error('Processing failed:', error);
    process.exit(1);
  }
}

// Helper function to escape special characters in regex
function escapeRegExp(string: string): string {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Run the script
moveImages(); 