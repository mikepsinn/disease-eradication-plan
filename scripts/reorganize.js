const fs = require('fs');
const path = require('path');
const { newStructure } = require('./config/structure');

function createDirectoryStructure(basePath, structure) {
  Object.keys(structure).forEach(dir => {
    const dirPath = path.join(basePath, dir);
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
    }
    
    if (Object.keys(structure[dir]).length > 0) {
      createDirectoryStructure(dirPath, structure[dir]);
    }
  });
}

// Create README files for each directory
function createReadme(dirPath, description) {
  const readmePath = path.join(dirPath, 'README.md');
  if (!fs.existsSync(readmePath)) {
    fs.writeFileSync(readmePath, `# ${path.basename(dirPath)}\n\n${description}\n`);
  }
}

// Main execution
try {
  createDirectoryStructure(process.cwd(), newStructure);
  console.log('Directory structure created successfully!');
} catch (error) {
  console.error('Error creating directory structure:', error);
} 