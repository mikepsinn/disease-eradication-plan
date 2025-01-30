require('dotenv').config();
const simpleGit = require('simple-git');
const fs = require('fs/promises');
const path = require('path');
const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const OpenAI = require('openai');
const mime = require('mime-types');

// Initialize clients
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

const s3Client = new S3Client({
    region: process.env.AWS_REGION,
    credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
    }
});

const git = simpleGit();

async function getDirectoryTree(startPath) {
    const tree = [];
    
    async function buildTree(currentPath, relativePath = '') {
        const items = await fs.readdir(currentPath, { withFileTypes: true });
        
        for (const item of items) {
            if (item.name.startsWith('.')) continue;
            
            const fullPath = path.join(currentPath, item.name);
            const relPath = path.join(relativePath, item.name);
            
            if (item.isDirectory()) {
                tree.push(`📁 ${relPath}/`);
                await buildTree(fullPath, relPath);
            } else {
                tree.push(`📄 ${relPath}`);
            }
        }
    }
    
    await buildTree(startPath);
    return tree.join('\n');
}

async function suggestFolderWithLLM(filePath, fileContent, directoryTree) {
    const prompt = `Given this repository structure:
${directoryTree}

I have a file: ${filePath}
With the following content (first 500 characters):
${fileContent.substring(0, 500)}...

Which existing folder would be the most appropriate to store this file? 
Respond only with the folder path, nothing else. If it should be in the root, respond with "/".`;

    const completion = await openai.chat.completions.create({
        model: "gpt-4",
        messages: [{ role: "user", content: prompt }],
    });

    return completion.choices[0].message.content.trim();
}

async function uploadToS3(imageBuffer, fileName) {
    const mimeType = mime.lookup(fileName) || 'application/octet-stream';
    const key = `images/${path.basename(fileName)}`;
    
    await s3Client.send(new PutObjectCommand({
        Bucket: process.env.S3_BUCKET_NAME,
        Key: key,
        Body: imageBuffer,
        ContentType: mimeType
    }));
    
    return `https://${process.env.S3_BUCKET_NAME}.s3.${process.env.AWS_REGION}.amazonaws.com/${key}`;
}

async function processMarkdownImages(content, basePath) {
    const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
    let newContent = content;
    let match;

    while ((match = imageRegex.exec(content)) !== null) {
        const [fullMatch, altText, imagePath] = match;
        
        // Only process relative paths
        if (!imagePath.startsWith('http')) {
            const absoluteImagePath = path.join(basePath, imagePath);
            
            try {
                const imageBuffer = await fs.readFile(absoluteImagePath);
                const s3Url = await uploadToS3(imageBuffer, path.basename(imagePath));
                newContent = newContent.replace(imagePath, s3Url);
            } catch (error) {
                console.error(`Failed to process image: ${imagePath}`, error);
            }
        }
    }
    
    return newContent;
}

async function main() {
    const sourceRepo = process.argv[2];
    if (!sourceRepo) {
        console.error('Please provide a source repository URL');
        process.exit(1);
    }
    
    // Create temp directory for cloning
    const tempDir = path.join(__dirname, 'temp-repo');
    await fs.mkdir(tempDir, { recursive: true });
    
    try {
        // Clone the repository
        console.log('Cloning repository...');
        await git.clone(sourceRepo, tempDir);
        
        // Get directory tree of current repository
        const currentTree = await getDirectoryTree(__dirname);
        
        // Process all files in the cloned repository
        async function processDirectory(dirPath) {
            const items = await fs.readdir(dirPath, { withFileTypes: true });
            
            for (const item of items) {
                const fullPath = path.join(dirPath, item.name);
                
                if (item.isDirectory()) {
                    if (!item.name.startsWith('.')) {
                        await processDirectory(fullPath);
                    }
                } else {
                    const content = await fs.readFile(fullPath, 'utf-8');
                    const suggestedFolder = await suggestFolderWithLLM(
                        item.name,
                        content,
                        currentTree
                    );
                    
                    // Process markdown files for images
                    let processedContent = content;
                    if (item.name.endsWith('.md')) {
                        processedContent = await processMarkdownImages(content, path.dirname(fullPath));
                    }
                    
                    // Create target directory if it doesn't exist
                    const targetDir = path.join(__dirname, suggestedFolder);
                    await fs.mkdir(targetDir, { recursive: true });
                    
                    // Copy file to suggested location
                    const targetPath = path.join(targetDir, item.name);
                    await fs.writeFile(targetPath, processedContent);
                    
                    console.log(`Processed ${item.name} -> ${targetPath}`);
                }
            }
        }
        
        await processDirectory(tempDir);
        
        // Cleanup
        await fs.rm(tempDir, { recursive: true, force: true });
        console.log('Processing complete!');
        
    } catch (error) {
        console.error('Error:', error);
        // Cleanup on error
        await fs.rm(tempDir, { recursive: true, force: true });
    }
}

main(); 