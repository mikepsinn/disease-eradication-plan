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
  date: z.string().datetime().optional(),
  tags: z.array(z.string()).default([]),
  editor: z.string().default('markdown'),
  dateCreated: z.string().datetime().optional(),
});

class FrontmatterGenerator {
  constructor(llmClient) {
    this.llmClient = llmClient;
  }

  async generateFrontmatter(content, filePath) {
    const systemPrompt = `You are a helpful assistant for analyzing markdown content and generating frontmatter metadata.
Your task is to analyze the content and generate appropriate frontmatter fields.
Always return a complete JSON object with ALL required fields:
- description (required): A clear, concise description
- emoji (required): A single relevant emoji
- title (required): A descriptive title
- number (optional): Any numerical value mentioned (with k/m/b suffix if applicable)
- textFollowingNumber (optional): The context around the number
- featuredImage (optional): Suggested image name if mentioned
- source (optional): Any URL referenced as a source
- tags (required): Array of relevant topic tags (default to empty array if none)
- published (required): Boolean, default to true
- editor (required): String, default to "markdown"
- date (optional): Current date in ISO format
- dateCreated (optional): Current date in ISO format

Example response format:
{
  "description": "Analysis of clinical trial costs showing $41k per participant",
  "emoji": "💰",
  "title": "Clinical Trial Cost Analysis",
  "number": "41k",
  "textFollowingNumber": "cost per participant in clinical trials",
  "tags": ["clinical-trials", "costs", "research"],
  "published": true,
  "editor": "markdown"
}`;

    const userContent = `Given this markdown content, generate appropriate frontmatter metadata:

Content:
${content.substring(0, 1000)}  // Limit content length for token efficiency`;

    try {
      const response = await this.llmClient.complete(systemPrompt, userContent);
      const result = JSON.parse(response);

      // Ensure required fields are present
      return {
        ...result,
        published: result.published ?? true,
        editor: result.editor || 'markdown',
        date: result.date || new Date().toISOString(),
        dateCreated: result.dateCreated || new Date().toISOString(),
        tags: result.tags || []
      };
    } catch (error) {
      throw new Error(`Failed to generate frontmatter: ${error.message}`);
    }
  }

  async processFile(filePath) {
    const content = await fs.readFile(filePath, 'utf8');
    const { data: frontmatter, content: markdownContent } = matter(content);

    try {
      const validationResult = FrontmatterSchema.safeParse(frontmatter);

      if (!validationResult.success) {
        console.log(`Invalid frontmatter:`, validationResult.error.errors);

        const generatedFrontmatter = await this.generateFrontmatter(markdownContent, filePath);
        
        if (!generatedFrontmatter) {
          console.error('Failed to generate frontmatter metadata');
          return { updated: false, error: new Error('Failed to generate frontmatter metadata') };
        }

        const updatedFrontmatter = {
          ...frontmatter,
          ...generatedFrontmatter,
          published: frontmatter.published ?? true,
          editor: frontmatter.editor || 'markdown',
          date: frontmatter.date || new Date().toISOString(),
          dateCreated: frontmatter.dateCreated || new Date().toISOString(),
        };

        const finalValidation = FrontmatterSchema.safeParse(updatedFrontmatter);
        if (finalValidation.success) {
          const updatedContent = matter.stringify(markdownContent, updatedFrontmatter);
          await fs.writeFile(filePath, updatedContent);
          console.log(`✅ Updated frontmatter`);
          return { updated: true };
        } else {
          console.error(`❌ Failed to fix frontmatter:`, finalValidation.error);
          return { updated: false, error: finalValidation.error };
        }
      } else {
        console.log(`✅ Valid frontmatter`);
        return { updated: false };
      }
    } catch (error) {
      console.error(`Error processing file:`, error);
      return { updated: false, error };
    }
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

async function main() {
  try {
    const llmClient = new LLMClient();
    const generator = new FrontmatterGenerator(llmClient);
    
    // Get directory from command line args or use default
    const targetDir = process.argv[2] || path.resolve(__dirname, '..');
    const absoluteTargetDir = path.resolve(targetDir);
    
    console.log(`Scanning directory: ${absoluteTargetDir}`);
    const markdownFiles = await findMarkdownFiles(absoluteTargetDir);
    
    console.log(`Found ${markdownFiles.length} markdown files`);
    
    // Add a confirmation prompt
    if (markdownFiles.length > 0) {
      console.log('\nFiles to process:');
      markdownFiles.forEach(file => console.log(`- ${path.relative(absoluteTargetDir, file)}`));
      
      // In non-test mode, wait for confirmation
      if (process.env.NODE_ENV !== 'test') {
        console.log('\nPress Ctrl+C to cancel or wait 5 seconds to continue...');
        await new Promise(resolve => setTimeout(resolve, 5000));
      }
    }
    
    let processed = 0;
    let updated = 0;
    
    for (const file of markdownFiles) {
      processed++;
      const relativePath = path.relative(absoluteTargetDir, file);
      console.log(`\n[${processed}/${markdownFiles.length}] Processing ${relativePath}...`);
      
      const result = await generator.processFile(file);
      if (result?.updated) {
        updated++;
      }
    }
    
    console.log(`\n✅ Completed! Processed ${processed} files, updated ${updated} files.`);
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
  FrontmatterGenerator,
  findMarkdownFiles
}; 