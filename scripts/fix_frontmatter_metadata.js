const fs = require('fs').promises;
const path = require('path');
const matter = require('gray-matter');
const { z } = require('zod');
const LLMClient = require('./llm-client');
require('dotenv').config();

// Define the frontmatter schema
const FrontmatterSchema = z.object({
  number: z.string().optional(),
  textFollowingNumber: z.string().optional(),
  description: z.string(),
  emoji: z.string(),
  featuredImage: z.string().optional(),
  source: z.string().url().optional(),
  title: z.string(),
  published: z.boolean().default(true),
  date: z.string().datetime(),
  tags: z.array(z.string()).default([]),
  editor: z.string().default('markdown'),
  dateCreated: z.string().datetime()
});

async function generateFrontmatterObject(content, llmClient) {
  const prompt = `Given this markdown content, generate appropriate frontmatter metadata:

Content:
${content.substring(0, 1000)}  // Limit content length for token efficiency

Generate a JSON object with these fields:
- number (optional): Any numerical value mentioned (with k/m/b suffix if applicable)
- textFollowingNumber (optional): The context around the number
- description: A clear, concise description of the content
- emoji: A single relevant emoji
- featuredImage (optional): Suggested image name if mentioned
- source (optional): Any URL referenced as a source
- title: A descriptive title
- tags: Array of relevant topic tags

The response should be a valid JSON object matching this structure.`;

  try {
    const analysis = await llmClient.analyzeLocation('', prompt);
    return analysis;
  } catch (error) {
    console.error('Error generating frontmatter:', error);
    return null;
  }
}

async function findMarkdownFiles(dir) {
  const files = await fs.readdir(dir, { withFileTypes: true });
  let markdownFiles = [];

  for (const file of files) {
    const fullPath = path.join(dir, file.name);
    if (file.isDirectory()) {
      markdownFiles = markdownFiles.concat(await findMarkdownFiles(fullPath));
    } else if (file.name.endsWith('.md')) {
      markdownFiles.push(fullPath);
    }
  }

  return markdownFiles;
}

async function processFile(filePath, llmClient) {
  console.log(`Processing ${filePath}...`);
  const content = await fs.readFile(filePath, 'utf8');
  const { data: frontmatter, content: markdownContent } = matter(content);

  try {
    // Validate existing frontmatter
    const validationResult = FrontmatterSchema.safeParse(frontmatter);

    if (!validationResult.success) {
      console.log(`Invalid frontmatter in ${filePath}:`, validationResult.error);

      // Generate structured frontmatter using LLM
      const generatedFrontmatter = await generateFrontmatterObject(markdownContent, llmClient);
      
      // Merge existing frontmatter with generated values
      const updatedFrontmatter = {
        ...frontmatter,
        ...generatedFrontmatter,
        published: frontmatter.published ?? true,
        editor: frontmatter.editor || 'markdown',
        date: frontmatter.date || new Date().toISOString(),
        dateCreated: frontmatter.dateCreated || new Date().toISOString(),
      };

      // Validate again after updates
      const finalValidation = FrontmatterSchema.safeParse(updatedFrontmatter);
      if (finalValidation.success) {
        // Write back to file
        const updatedContent = matter.stringify(markdownContent, updatedFrontmatter);
        await fs.writeFile(filePath, updatedContent);
        console.log(`✅ Updated frontmatter for ${filePath}`);
      } else {
        console.error(`❌ Failed to fix frontmatter for ${filePath}:`, finalValidation.error);
      }
    } else {
      console.log(`✅ Valid frontmatter in ${filePath}`);
    }
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error);
  }
}

async function main() {
  try {
    const llmClient = new LLMClient();
    const markdownFiles = await findMarkdownFiles(path.resolve(__dirname, '..'));
    
    console.log(`Found ${markdownFiles.length} markdown files`);
    
    for (const file of markdownFiles) {
      await processFile(file, llmClient);
    }
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  FrontmatterSchema,
  processFile,
  findMarkdownFiles,
  generateFrontmatterObject
}; 