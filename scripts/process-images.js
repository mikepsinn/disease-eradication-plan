require('dotenv').config();
const fs = require('fs');
const path = require('path');
const mime = require('mime-types');
const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');

// Initialize S3 client
const s3Client = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  }
});

// Get configuration from environment variables
const BUCKET_NAME = process.env.S3_BUCKET_NAME;
const OPENAI_MODEL = process.env.OPENAI_MODEL || 'gpt-4'; // Default to gpt-4 if not specified

// Path for the image catalog
const IMAGE_CATALOG_PATH = 'docs/assets/image-catalog.json';

// Load existing image catalog if it exists
function loadImageCatalog() {
  try {
    if (fs.existsSync(IMAGE_CATALOG_PATH)) {
      return JSON.parse(fs.readFileSync(IMAGE_CATALOG_PATH, 'utf8'));
    }
  } catch (error) {
    console.error('Error loading image catalog:', error);
  }
  return {
    lastUpdated: new Date().toISOString(),
    totalImages: 0,
    images: {}
  };
}

// Save image catalog
function saveImageCatalog(catalog) {
  try {
    // Ensure directory exists
    const dir = path.dirname(IMAGE_CATALOG_PATH);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    // Update metadata
    catalog.lastUpdated = new Date().toISOString();
    catalog.totalImages = Object.keys(catalog.images).length;
    
    // Save catalog
    fs.writeFileSync(
      IMAGE_CATALOG_PATH,
      JSON.stringify(catalog, null, 2),
      'utf8'
    );
    
    // Create markdown version for easy viewing
    const markdown = generateMarkdownCatalog(catalog);
    fs.writeFileSync(
      IMAGE_CATALOG_PATH.replace('.json', '.md'),
      markdown,
      'utf8'
    );
  } catch (error) {
    console.error('Error saving image catalog:', error);
  }
}

// Generate markdown version of the catalog
function generateMarkdownCatalog(catalog) {
  let markdown = `# Image Catalog\n\n`;
  markdown += `Last Updated: ${catalog.lastUpdated}\n`;
  markdown += `Total Images: ${catalog.totalImages}\n\n`;
  
  // Group images by type
  const imagesByType = {};
  Object.entries(catalog.images).forEach(([key, image]) => {
    const type = image.mimeType.split('/')[1].toUpperCase();
    if (!imagesByType[type]) {
      imagesByType[type] = [];
    }
    imagesByType[type].push(image);
  });
  
  // Generate sections for each type
  Object.entries(imagesByType).forEach(([type, images]) => {
    markdown += `## ${type} Images\n\n`;
    images.forEach(image => {
      markdown += `### ${image.fileName}\n`;
      markdown += `![${image.fileName}](${image.s3Url})\n\n`;
      markdown += `- **Original Path:** \`${image.originalPath}\`\n`;
      markdown += `- **S3 URL:** ${image.s3Url}\n`;
      markdown += `- **Size:** ${formatBytes(image.size)}\n`;
      markdown += `- **MIME Type:** ${image.mimeType}\n`;
      markdown += `- **Upload Date:** ${image.uploadDate}\n\n`;
    });
  });
  
  return markdown;
}

// Helper function to format bytes
function formatBytes(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Files and directories to ignore
const ignoreList = [
  '.git',
  'node_modules',
  '.env',
  'package.json',
  'package-lock.json',
  '.gitignore',
  'scripts',
  '.vscode',
  '.idea'
];

// File extensions to process
const processExtensions = ['.md', '.html', '.mdx'];

// Image extensions to look for
const imageExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'];

// Function to check if path should be ignored
function shouldIgnore(filePath) {
  return ignoreList.some(ignored => filePath.includes(ignored));
}

// Function to get all files recursively
async function getAllFiles(dir) {
  const files = [];
  const items = fs.readdirSync(dir);

  for (const item of items) {
    const fullPath = path.join(dir, item);
    if (shouldIgnore(fullPath)) continue;

    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      files.push(...await getAllFiles(fullPath));
    } else {
      if (processExtensions.includes(path.extname(fullPath).toLowerCase())) {
        files.push(fullPath);
      }
    }
  }

  return files;
}

// Function to extract image paths from markdown/html content
function extractImagePaths(content) {
  const images = new Set();
  
  // Match markdown image syntax: ![alt](path)
  const markdownRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
  let match;
  while ((match = markdownRegex.exec(content)) !== null) {
    images.add(match[2]);
  }

  // Match HTML img tags: <img src="path" ...>
  const htmlRegex = /<img[^>]+src=["']([^"']+)["']/g;
  while ((match = htmlRegex.exec(content)) !== null) {
    images.add(match[1]);
  }

  return Array.from(images)
    .filter(path => !path.startsWith('http'))  // Filter out URLs
    .filter(path => !path.startsWith('data:')); // Filter out data URLs
}

// Modified uploadToS3 function to update catalog
async function uploadToS3(filePath) {
  try {
    const fileContent = fs.readFileSync(filePath);
    const fileName = path.basename(filePath);
    const mimeType = mime.lookup(filePath) || 'application/octet-stream';
    
    const key = `images/${fileName}`;
    const command = new PutObjectCommand({
      Bucket: BUCKET_NAME,
      Key: key,
      Body: fileContent,
      ContentType: mimeType,
      ACL: 'public-read'
    });

    await s3Client.send(command);
    const s3Url = `https://${BUCKET_NAME}.s3.${process.env.AWS_REGION}.amazonaws.com/${key}`;
    
    // Update image catalog
    const catalog = loadImageCatalog();
    catalog.images[fileName] = {
      fileName,
      originalPath: filePath,
      s3Url,
      size: fileContent.length,
      mimeType,
      uploadDate: new Date().toISOString(),
      key
    };
    saveImageCatalog(catalog);
    
    return s3Url;
  } catch (error) {
    console.error(`Error uploading ${filePath} to S3:`, error);
    return null;
  }
}

// Function to update file content with S3 URLs
function updateContent(content, imagePaths, s3Urls) {
  let updatedContent = content;
  
  imagePaths.forEach((imagePath, index) => {
    if (!s3Urls[index]) return;

    // Update markdown image syntax
    const markdownRegex = new RegExp(`!\\[([^\\]]*)\\]\\(${escapeRegExp(imagePath)}\\)`, 'g');
    updatedContent = updatedContent.replace(markdownRegex, `![$1](${s3Urls[index]})`);

    // Update HTML img tags
    const htmlRegex = new RegExp(`<img([^>]+)src=["']${escapeRegExp(imagePath)}["']`, 'g');
    updatedContent = updatedContent.replace(htmlRegex, `<img$1src="${s3Urls[index]}"`);
  });

  return updatedContent;
}

// Helper function to escape special characters in regex
function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Main function to process files
async function processFiles() {
  try {
    const files = await getAllFiles(process.cwd());
    console.log(`Found ${files.length} files to process`);

    for (const file of files) {
      console.log(`\nProcessing ${file}`);
      const content = fs.readFileSync(file, 'utf8');
      const imagePaths = extractImagePaths(content);

      if (imagePaths.length === 0) {
        console.log('No local images found in file');
        continue;
      }

      console.log(`Found ${imagePaths.length} local images`);
      const s3Urls = [];

      for (const imagePath of imagePaths) {
        const absoluteImagePath = path.isAbsolute(imagePath) 
          ? imagePath 
          : path.join(path.dirname(file), imagePath);

        if (fs.existsSync(absoluteImagePath)) {
          console.log(`Uploading ${imagePath} to S3...`);
          const s3Url = await uploadToS3(absoluteImagePath);
          s3Urls.push(s3Url);
          
          if (s3Url) {
            console.log(`✓ Uploaded successfully: ${s3Url}`);
          }
        } else {
          console.log(`✗ Image not found: ${absoluteImagePath}`);
          s3Urls.push(null);
        }
      }

      // Update file content with S3 URLs
      const updatedContent = updateContent(content, imagePaths, s3Urls);
      if (content !== updatedContent) {
        fs.writeFileSync(file, updatedContent, 'utf8');
        console.log(`✓ Updated file with S3 URLs`);
      }
    }

    console.log('\nProcessing completed!');
  } catch (error) {
    console.error('Processing failed:', error);
  }
}

// Create a backup of the file before processing
function backupFile(filePath) {
  const backupPath = `${filePath}.bak`;
  fs.copyFileSync(filePath, backupPath);
  return backupPath;
}

// Main execution with backup
async function main() {
  // Create backups of all files first
  const files = await getAllFiles(process.cwd());
  const backups = files.map(file => backupFile(file));
  
  try {
    await processFiles();
    // If successful, remove backups
    backups.forEach(backup => fs.unlinkSync(backup));
  } catch (error) {
    console.error('Error during processing:', error);
    // Restore from backups
    backups.forEach((backup, index) => {
      fs.copyFileSync(backup, files[index]);
      fs.unlinkSync(backup);
    });
    console.log('Files restored from backups');
  }
}

// Run the script
main(); 