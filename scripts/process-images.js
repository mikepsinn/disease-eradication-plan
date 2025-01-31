require('dotenv').config();
const fs = require('fs');
const path = require('path');
const mime = require('mime-types');
const { S3Client, PutObjectCommand, ListObjectsV2Command } = require('@aws-sdk/client-s3');
const { newStructure, shouldIgnore, getAllFiles } = require('./shared-utilities');

// Initialize S3 client
const s3Client = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  }
});

// Get configuration from environment variables
const S3_AWS_BUCKET = process.env.S3_AWS_BUCKET;
const IMAGE_DIR = process.env.IMAGE_DIR || 'img';

// Path for the image catalog
const IMAGE_CATALOG_PATH = 'docs/assets/image-catalog.json';

// Add this validation function near the top of the file
function validateEnvironment() {
  const requiredVars = [
    'AWS_ACCESS_KEY_ID',
    'AWS_SECRET_ACCESS_KEY',
    'AWS_REGION',
    'S3_AWS_BUCKET',
    'S3_PUBLIC_URL'
  ];

  const missingVars = requiredVars.filter(varName => !process.env[varName]);

  if (missingVars.length > 0) {
    console.error('❌ Missing required environment variables:');
    missingVars.forEach(varName => {
      console.error(`  - ${varName}`);
    });
    console.error('\nPlease configure these in your .env file:');
    console.error(`AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
S3_AWS_BUCKET=your-bucket-name
S3_PUBLIC_URL=https://your-public-url.com`);
    process.exit(1);
  }

  // Validate S3_PUBLIC_URL format
  if (!process.env.S3_PUBLIC_URL.startsWith('http')) {
    console.error('❌ Invalid S3_PUBLIC_URL: Must be a valid URL starting with http:// or https://');
    process.exit(1);
  }
}

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

// File extensions to process
const processExtensions = ['.md', '.html', '.mdx'];

// Image extensions to look for
const imageExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'];

// Function to get all files recursively
async function getAllFilesIncludingImages(dir) {
  const files = [];
  const items = fs.readdirSync(dir);

  for (const item of items) {
    const fullPath = path.join(dir, item);
    if (shouldIgnore(fullPath)) continue;

    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      files.push(...await getAllFilesIncludingImages(fullPath));
    } else {
      const ext = path.extname(fullPath).toLowerCase();
      if (processExtensions.includes(ext) || imageExtensions.includes(ext)) {
        files.push(fullPath);
      }
    }
  }

  return files;
}

// Rename the sync function for clarity
async function updateCatalogFromS3(catalog) {
  try {
    console.log('🔍 Checking S3 bucket for catalog updates...');
    const command = new ListObjectsV2Command({
      Bucket: S3_AWS_BUCKET,
      Prefix: IMAGE_DIR + '/'
    });

    let isTruncated = true;
    let continuationToken;
    let s3Objects = [];

    while (isTruncated) {
      const response = await s3Client.send(command);
      s3Objects = s3Objects.concat(response.Contents || []);
      isTruncated = response.IsTruncated;
      continuationToken = response.NextContinuationToken;
    }

    // Add missing images to catalog
    let newEntries = 0;
    s3Objects.forEach(s3Object => {
      const fileName = path.basename(s3Object.Key);
      if (!catalog.images[fileName]) {
        catalog.images[fileName] = {
          fileName,
          originalPath: '(uploaded directly to S3)',
          s3Url: `${process.env.S3_PUBLIC_URL}/${s3Object.Key}`,
          size: s3Object.Size,
          mimeType: mime.lookup(fileName) || 'application/octet-stream',
          uploadDate: s3Object.LastModified.toISOString(),
          key: s3Object.Key
        };
        newEntries++;
        console.log(`✅ Added existing S3 file to catalog: ${fileName}`);
      }
    });

    saveImageCatalog(catalog);
    console.log(`✅ Added ${newEntries} existing S3 files to catalog`);
  } catch (error) {
    console.error('Error syncing with S3 bucket:', error);
  }
}

// Update processFiles function to include sync
async function processFiles() {
  try {
    validateEnvironment();
    const catalog = loadImageCatalog();
    
    if (process.env.UPDATE_IMAGE_CATALOG_FROM_S3 !== 'false') {
      console.log('\n🔄 Updating image catalog from S3 bucket...');
      await updateCatalogFromS3(catalog);
    }

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
        console.log(`Looking for image: ${imagePath}`);
        const absoluteImagePath = await findImageFile(imagePath, file);

        if (absoluteImagePath && fs.existsSync(absoluteImagePath)) {
          console.log(`✓ Found at: ${absoluteImagePath}`);
          console.log(`Uploading to S3...`);
          const s3Url = await uploadToS3(absoluteImagePath);
          s3Urls.push(s3Url);
          
          if (s3Url) {
            console.log(`✓ Uploaded successfully: ${s3Url}`);
          }
        } else {
          console.log(`✗ Image not found: ${imagePath}`);
          console.log(`Tried looking in multiple locations. Please check if the file exists.`);
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

// Simplify main execution to just run processFiles directly
processFiles().catch(error => {
  console.error('Error during processing:', error);
}); 