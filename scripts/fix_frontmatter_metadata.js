const fs = require('fs').promises;
const path = require('path');
const matter = require('gray-matter');
const { z } = require('zod');
const LLMClient = require('./llm-client');
require('dotenv').config();

// Define the frontmatter schema
const FrontmatterSchema = z.object({
  title: z.string()
    .describe('A descriptive title'),
  description: z.string()
    .describe('A clear, concise description'),
  published: z.boolean()
    .default(true)
    .describe('Whether the content is published, defaults to true'),
  date: z.string()
    .datetime()
    .optional()
    .describe('Current date in ISO format'),
  tags: z.string()
    .default('')
    .describe('Comma-separated list of relevant topic tags'),
  editor: z.string()
    .default('markdown')
    .describe('Editor type, defaults to markdown'),
  dateCreated: z.string()
    .datetime()
    .optional()
    .describe('Creation date in ISO format'),
});

class FrontmatterGenerator {
  constructor(llmClient) {
    this.llmClient = llmClient;
  }

  async generateFrontmatter(content, filePath) {
    const systemPrompt = `You are a helpful assistant for analyzing markdown content and generating frontmatter metadata.
Your task is to analyze the content and generate appropriate frontmatter fields.
Always return a complete JSON object with all required fields based on the content.
Make sure to include all mandatory fields (title, description, emoji) and any optional fields that are relevant to the content.

Example response format:
{
  "description": "Analysis of clinical trial costs showing $41k per participant",
  "emoji": "💰",
  "title": "Clinical Trial Cost Analysis",
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
        tags: result.tags || ''
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
          ...generatedFrontmatter,
          ...Object.fromEntries(
            Object.entries(frontmatter)
              .filter(([_, value]) => value !== undefined && value !== null && value !== '')
          ),
          published: frontmatter.published ?? true,
          editor: frontmatter.editor || 'markdown',
          date: (frontmatter.date instanceof Date ? frontmatter.date.toISOString() : frontmatter.date) || new Date().toISOString(),
          dateCreated: (frontmatter.dateCreated instanceof Date ? frontmatter.dateCreated.toISOString() : frontmatter.dateCreated) || new Date().toISOString(),
          // Convert tags array to comma-separated string if it exists
          tags: Array.isArray(frontmatter.tags) ? frontmatter.tags.join(', ') : 
                Array.isArray(generatedFrontmatter.tags) ? generatedFrontmatter.tags.join(', ') : 
                ''
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