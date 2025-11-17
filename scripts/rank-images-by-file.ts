import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const projectRoot = process.cwd();

try {
  // Get all tracked files from git, which respects .gitignore
  const allFilesOutput = execSync('git ls-files', { encoding: 'utf-8' });
  const allFiles = allFilesOutput.split('\n').filter(Boolean);

  const markdownFiles = allFiles.filter(file => path.extname(file) === '.md');

  const imageCounts = markdownFiles.map(file => {
    const filePath = path.join(projectRoot, file);
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const imageRegex = /!\[.*?\]\(.*?\)/g;
      const matches = content.match(imageRegex);
      return {
        file: file,
        count: matches ? matches.length : 0,
      };
    } catch (error) {
        // file might have been deleted since ls-files ran
        return {
            file: file,
            count: 0
        }
    }
  });

  imageCounts.sort((a, b) => b.count - a.count);

  console.log('Files ranked by image count (respecting .gitignore):');
  imageCounts.forEach(item => {
    if (item.count > 0) {
      console.log(`${item.file}: ${item.count}`);
    }
  });

} catch (error) {
  console.error('Error executing git ls-files. Is git installed and is this a git repository?', error);
}
