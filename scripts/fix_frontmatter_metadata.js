const fs = require('fs').promises;
const path = require('path');
const matter = require('gray-matter');
const { z } = require('zod');
const LLMClient = require('./llm-client');
const ignore = require('ignore');
const yaml = require('js-yaml');
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
    const systemPrompt = `You are a helpful assistant for analyzing markdown content and generating frontmatter metadata
    for a wiki for a decentralized FDA.
Your task is to analyze the content and generate appropriate frontmatter fields.
Always return a complete JSON object with all required fields based on the content.
Make sure to include all mandatory fields (title, description) and any optional fields that are relevant to the content.

Please keep the title and description factual and concise like a wikipedia article. 
Don't include any flowery adjectives.
Try to use terms or phrases from the existing content if appropriate.

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
    const { data: frontmatter, content: markdownContent, isEmpty } = matter(content);

    try {
      // Convert any Date objects to ISO strings before validation
      const normalizedFrontmatter = {
        ...frontmatter,
        date: frontmatter.date instanceof Date ? frontmatter.date.toISOString() : frontmatter.date,
        dateCreated: frontmatter.dateCreated instanceof Date ? frontmatter.dateCreated.toISOString() : frontmatter.dateCreated
      };

      const validationResult = FrontmatterSchema.safeParse(normalizedFrontmatter);

      if (!validationResult.success) {
        console.log(`\n❌ Invalid frontmatter in file: ${filePath}`);
        console.log('Current frontmatter:');
        console.log(JSON.stringify(normalizedFrontmatter, null, 2));
        console.log('\nValidation errors:');
        validationResult.error.issues.forEach(issue => {
          console.log(`  - Field: ${issue.path.join('.')} - ${issue.message}`);
        });

        // Only generate frontmatter if it's missing or empty, or if tags are empty
        const shouldGenerateMetadata = isEmpty || 
          Object.keys(frontmatter).length === 0 || 
          !frontmatter.tags || 
          frontmatter.tags === '' || 
          (Array.isArray(frontmatter.tags) && frontmatter.tags.length === 0);

        const generatedFrontmatter = shouldGenerateMetadata ? 
          await this.generateFrontmatter(markdownContent, filePath) :
          {};
        
        if (!generatedFrontmatter && shouldGenerateMetadata) {
          const error = new Error('Failed to generate frontmatter metadata');
          error.context = { filePath, frontmatter: normalizedFrontmatter };
          return { updated: false, error };
        }

        const updatedFrontmatter = {
          ...generatedFrontmatter,
          ...Object.fromEntries(
            Object.entries(frontmatter)
              .filter(([key, value]) => {
                // Special handling for tags - don't keep empty tags
                if (key === 'tags') {
                  return value !== undefined && value !== null && value !== '' && 
                         !(Array.isArray(value) && value.length === 0);
                }
                return value !== undefined && value !== null && value !== '';
              })
          ),
          published: frontmatter.published ?? true,
          editor: frontmatter.editor || 'markdown',
          date: (frontmatter.date instanceof Date ? frontmatter.date.toISOString() : frontmatter.date) || new Date().toISOString(),
          dateCreated: (frontmatter.dateCreated instanceof Date ? frontmatter.dateCreated.toISOString() : frontmatter.dateCreated) || new Date().toISOString(),
          // Use generated tags if existing tags are empty
          tags: (Array.isArray(frontmatter.tags) && frontmatter.tags.length > 0) ? frontmatter.tags.join(', ') :
                (frontmatter.tags && frontmatter.tags !== '') ? frontmatter.tags :
                Array.isArray(generatedFrontmatter.tags) ? generatedFrontmatter.tags.join(', ') :
                generatedFrontmatter.tags || ''
        };

        const finalValidation = FrontmatterSchema.safeParse(updatedFrontmatter);
        if (finalValidation.success) {
          // Preserve the original content exactly as it was, with emoji support
          const updatedContent = matter.stringify(markdownContent.trim(), updatedFrontmatter, {
            engines: {
              yaml: {
                stringify: (obj) => require('js-yaml').dump(obj, { lineWidth: -1 })
              }
            }
          });
          await fs.writeFile(filePath, updatedContent);
          console.log(`✅ Updated frontmatter only`);
          return { updated: true };
        } else {
          const error = new Error('Failed to fix frontmatter validation issues');
          error.issues = finalValidation.error.issues;
          error.context = { 
            filePath,
            originalFrontmatter: normalizedFrontmatter,
            updatedFrontmatter
          };
          return { updated: false, error };
        }
      } else {
        console.log(`✅ Valid frontmatter`);
        return { updated: false };
      }
    } catch (error) {
      error.context = { filePath, frontmatter };
      return { updated: false, error };
    }
  }
}

async function findMarkdownFiles(dir) {
  // Read .gitignore if it exists
  let ig = ignore();
  try {
    const gitignore = await fs.readFile(path.join(dir, '.gitignore'), 'utf8');
    ig = ignore().add(gitignore);
  } catch (error) {
    // No .gitignore found, continue with empty ignore rules
  }

  const files = await fs.readdir(dir, { withFileTypes: true });
  let markdownFiles = [];

  for (const file of files) {
    const relativePath = path.relative(dir, path.join(dir, file.name));
    
    // Skip if file/directory is ignored by .gitignore
    if (ig.ignores(relativePath)) {
      continue;
    }

    const fullPath = path.join(dir, file.name);
    
    if (file.isDirectory()) {
      markdownFiles = markdownFiles.concat(await findMarkdownFiles(fullPath));
    } else if (file.name.endsWith('.md')) {
      markdownFiles.push(fullPath);
    }
  }

  return markdownFiles;
}

async function validateMarkdownFiles(files) {
  const invalidFiles = [];
  
  for (const file of files) {
    try {
      const content = await fs.readFile(file, 'utf8');
      let frontmatter;
      
      try {
        const parsed = matter(content);
        frontmatter = parsed.data;
      } catch (parseError) {
        invalidFiles.push({
          path: file,
          errors: [{
            message: `Invalid YAML frontmatter: ${parseError.message}`,
            code: 'INVALID_YAML'
          }]
        });
        continue;
      }

      // Skip files with no frontmatter
      if (!frontmatter || Object.keys(frontmatter).length === 0) {
        invalidFiles.push({
          path: file,
          errors: [{
            message: 'No frontmatter found',
            code: 'NO_FRONTMATTER'
          }]
        });
        continue;
      }

      // Convert any Date objects to ISO strings before validation
      const normalizedFrontmatter = {
        ...frontmatter,
        date: frontmatter.date instanceof Date ? frontmatter.date.toISOString() : frontmatter.date,
        dateCreated: frontmatter.dateCreated instanceof Date ? frontmatter.dateCreated.toISOString() : frontmatter.dateCreated
      };
      
      const validationResult = FrontmatterSchema.safeParse(normalizedFrontmatter);
      if (!validationResult.success) {
        invalidFiles.push({
          path: file,
          errors: validationResult.error.errors
        });
      }
    } catch (error) {
      invalidFiles.push({
        path: file,
        errors: [{
          message: `Failed to read or process file: ${error.message}`,
          code: 'FILE_ERROR'
        }]
      });
    }
  }
  
  return invalidFiles;
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
    
    // First validate all files
    console.log('\nValidating frontmatter in all files...');
    const invalidFiles = await validateMarkdownFiles(markdownFiles);
    
    if (invalidFiles.length === 0) {
      console.log('✅ All files have valid frontmatter metadata');
      return;
    }
    
    console.log(`\n❌ Found ${invalidFiles.length} files with invalid frontmatter:`);
    invalidFiles.forEach(file => {
      const relativePath = path.relative(absoluteTargetDir, file.path);
      console.log(`\n📄 ${relativePath}`);
      console.log('  Errors:');
      file.errors.forEach(error => {
        if (error.code === 'INVALID_YAML') {
          console.log(`  ❌ ${error.message}`);
        } else {
          console.log(`  ❌ Field: ${error.path?.join('.')} - ${error.message}`);
        }
      });
      // Print file URL for easy clicking in VSCode
      console.log(`  📎 File URL: file://${path.resolve(absoluteTargetDir, file.path)}`);
    });
    
    // In non-test mode, wait for confirmation
    if (process.env.NODE_ENV !== 'test') {
      console.log('\nPress Ctrl+C to cancel or wait 5 seconds to continue processing invalid files...');
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
    
    let processed = 0;
    let updated = 0;
    let errors = [];
    
    for (const file of invalidFiles) {
      processed++;
      const relativePath = path.relative(absoluteTargetDir, file.path);
      console.log(`\n[${processed}/${invalidFiles.length}] Processing ${relativePath}...`);
      
      try {
        const result = await generator.processFile(file.path);
        if (result?.updated) {
          updated++;
        }
        if (result?.error) {
          errors.push({
            file: relativePath,
            error: result.error,
            fileUrl: `file://${path.resolve(absoluteTargetDir, file.path)}`
          });
        }
      } catch (error) {
        errors.push({
          file: relativePath,
          error,
          fileUrl: `file://${path.resolve(absoluteTargetDir, file.path)}`
        });
      }
    }
    
    if (errors.length > 0) {
      console.error('\n❌ Errors occurred while processing files:');
      errors.forEach(({ file, error, fileUrl }) => {
        console.error(`\n📄 ${file}`);
        console.error(`  Error: ${error.message}`);
        if (error.issues) {
          error.issues.forEach(issue => {
            console.error(`  - Field: ${issue.path?.join('.')} - ${issue.message}`);
          });
        }
        console.error(`  📎 File URL: ${fileUrl}`);
      });
      process.exit(1);
    }
    
    console.log(`\n✅ Completed! Processed ${processed} files, updated ${updated} files.`);
  } catch (error) {
    console.error('\n❌ Fatal error:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  FrontmatterSchema,
  FrontmatterGenerator,
  findMarkdownFiles,
  validateMarkdownFiles
}; 