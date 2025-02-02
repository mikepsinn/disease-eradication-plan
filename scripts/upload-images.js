require('dotenv').config();
const fs = require('fs');
const path = require('path');
const mime = require('mime-types');
const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const { getAllFiles } = require('./shared-utilities');

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
const IMAGE_CATALOG_PATH = 'docs/assets/image-catalog.json';

function validateEnvironment() {
  const requiredVars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION', 'S3_AWS_BUCKET', 'S3_PUBLIC_URL'];
  const missingVars = requiredVars.filter(varName => !process.env[varName]);

  if (missingVars.length > 0) {
    console.error('❌ Missing required environment variables:', missingVars.join(', '));
    process.exit(1);
  }

  if (!process.env.S3_PUBLIC_URL.startsWith('http')) {
    console.error('❌ Invalid S3_PUBLIC_URL: Must be a valid URL starting with http:// or https://');
    process.exit(1);
  }
}

function loadImageCatalog() {
  try {
    return fs.existsSync(IMAGE_CATALOG_PATH) 
      ? JSON.parse(fs.readFileSync(IMAGE_CATALOG_PATH, 'utf8'))
      : { lastUpdated: new Date().toISOString(), totalImages: 0, images: {} };
  } catch (error) {
    console.error('Error loading image catalog:', error);
    return { lastUpdated: new Date().toISOString(), totalImages: 0, images: {} };
  }
}

function saveImageCatalog(catalog) {
  try {
    const dir = path.dirname(IMAGE_CATALOG_PATH);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    catalog.lastUpdated = new Date().toISOString();
    catalog.totalImages = Object.keys(catalog.images).length;
    
    fs.writeFileSync(IMAGE_CATALOG_PATH, JSON.stringify(catalog, null, 2), 'utf8');
  } catch (error) {
    console.error('Error saving image catalog:', error);
  }
}

function extractImagePaths(content) {
  const paths = new Set();
  const patterns = [
    { regex: /!\[.*?\]\((.*?)\)/g, group: 1 },  // Markdown
    { regex: /<img[^>]+src=["']([^"']+)["']/g, group: 1 }  // HTML
  ];
  
  patterns.forEach(({ regex, group }) => {
    let match;
    while ((match = regex.exec(content)) !== null) {
      if (!match[group].startsWith('http')) {
        paths.add(match[group]);
      }
    }
  });
  
  return Array.from(paths);
}

async function findImageFile(imagePath, sourceFile) {
  const possiblePaths = [
    imagePath,
    path.join(path.dirname(sourceFile), imagePath),
    path.join(process.cwd(), imagePath),
    path.join(process.cwd(), 'img', path.basename(imagePath)),
    path.join(process.cwd(), 'assets', path.basename(imagePath))
  ];
  
  for (const testPath of possiblePaths) {
    if (fs.existsSync(testPath)) {
      return testPath;
    }
  }
  return null;
}

async function uploadToS3(filePath) {
  try {
    const fileContent = fs.readFileSync(filePath);
    const fileName = path.basename(filePath);
    const key = `${IMAGE_DIR}/${fileName}`;
    
    await s3Client.send(new PutObjectCommand({
      Bucket: S3_AWS_BUCKET,
      Key: key,
      Body: fileContent,
      ContentType: mime.lookup(filePath) || 'application/octet-stream'
    }));
    
    const s3Url = `${process.env.S3_PUBLIC_URL}/${key}`;
    
    // Update catalog
    const catalog = loadImageCatalog();
    catalog.images[fileName] = {
      fileName,
      originalPath: filePath,
      s3Url,
      size: fs.statSync(filePath).size,
      mimeType: mime.lookup(filePath) || 'application/octet-stream',
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

function updateContent(content, localPaths, s3Urls) {
  return localPaths.reduce((updatedContent, localPath, index) => {
    if (!s3Urls[index]) return updatedContent;
    
    const escapedPath = localPath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const patterns = [
      { regex: `!\\[([^\\]]*)\\]\\(${escapedPath}\\)`, replace: `![$1](${s3Urls[index]})` },  // Markdown
      { regex: `<img([^>]*)src=["']${escapedPath}["']([^>]*)>`, replace: `<img$1src="${s3Urls[index]}"$2>` }  // HTML
    ];
    
    return patterns.reduce((content, { regex, replace }) => 
      content.replace(new RegExp(regex, 'g'), replace), updatedContent);
  }, content);
}

async function processFiles() {
  try {
    validateEnvironment();
    const files = await getAllFiles(process.cwd(), ['.md', '.html']);  // Only process markdown and html files
    console.log(`Found ${files.length} markdown/html files to process`);

    for (const file of files) {
      console.log(`\nProcessing ${file}`);
      const content = fs.readFileSync(file, 'utf8');
      const imagePaths = extractImagePaths(content);

      if (imagePaths.length === 0) {
        console.log('No local images found in file');
        continue;
      }

      console.log(`Found ${imagePaths.length} local images`);
      const s3Urls = await Promise.all(imagePaths.map(async imagePath => {
        console.log(`Looking for image: ${imagePath}`);
        const absoluteImagePath = await findImageFile(imagePath, file);
        
        if (absoluteImagePath && fs.existsSync(absoluteImagePath)) {
          console.log(`✓ Found at: ${absoluteImagePath}`);
          const s3Url = await uploadToS3(absoluteImagePath);
          console.log(s3Url ? `✓ Uploaded successfully: ${s3Url}` : '✗ Upload failed');
          return s3Url;
        } else {
          console.log(`✗ Image not found: ${imagePath}`);
          return null;
        }
      }));

      const updatedContent = updateContent(content, imagePaths, s3Urls);
      if (content !== updatedContent) {
        fs.writeFileSync(file, updatedContent, 'utf8');
        console.log(`✓ Updated file with S3 URLs`);
      }
    }

    console.log('\nProcessing completed!');
  } catch (error) {
    console.error('Processing failed:', error);
    process.exit(1);
  }
}

processFiles(); 