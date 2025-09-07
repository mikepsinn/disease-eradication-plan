import * as fs from 'fs';
import * as fspromises from 'fs/promises';
import * as path from 'path';
import matter from 'gray-matter';
import { z, ZodObject, ZodRawShape, ZodTypeAny } from 'zod/v3';
// Assuming LLMClient is converted to TS as well
import LLMClient from './llm-client';
import ignore, { Ignore } from 'ignore';
import * as yaml from 'js-yaml';
import 'dotenv/config';

// Define interfaces for the frontmatter schema based on Zod definition
interface Frontmatter {
  title: string;
  description: string;
  published: boolean;
  date?: string;
  tags: string;
  editor: string;
  dateCreated?: string;
}

// Define the frontmatter schema using Zod
const FrontmatterSchema = z.object({
  title: z.string()
    .describe('A descriptive title for the content'),
  description: z.string()
    .describe('The main points of the content compressed into a single sentence'),
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
  private llmClient: LLMClient;

  constructor(llmClient: LLMClient) {
    this.llmClient = llmClient;
  }

  getSchemaDescriptions(): string {
    const shape: ZodRawShape = (FrontmatterSchema as any).shape; // Cast to ZodRawShape to access shape keys
    return Object.entries(shape).map(([key, field]: [string, any]) => {
      const description = field.description;
      // Zod v3+ uses .isOptional() and .isNullable()
      const isRequired = !(field.isOptional() || field.isNullable());
      return `${key}${isRequired ? ' (required)' : ' (optional)'}: ${description}`;
    }).join('\n');
  }

  async generateFrontmatter(content: string): Promise<Frontmatter | undefined> {
    const schemaDescriptions = this.getSchemaDescriptions();
    const systemPrompt = `You are a helpful assistant for analyzing markdown content and generating frontmatter metadata for a wiki for a decentralized FDA.\n\nYour task is to analyze the content and generate appropriate frontmatter fields according to these specifications.\nYou must return a valid JSON object with the following fields:\n\n${schemaDescriptions}\n\nExample JSON response format:\n{\n  "title": "Clinical Trial Cost Analysis",\n  "description": "Current clinical trials costs $41k per participant",\n  "published": true,\n  "date": "2024-03-20T10:00:00Z",\n  "tags": "clinical-trials, costs, research",\n  "editor": "markdown",\n  "dateCreated": "2024-03-20T10:00:00Z"\n}`;

    // Limit content length for token efficiency, ensure it's not undefined
    const userContent = `Given this markdown content, generate appropriate frontmatter metadata as a JSON object:\n\nContent:\n${content ? content.substring(0, 1000) : ''}`;

    try {
      const response = await this.llmClient.complete(systemPrompt, userContent);

      if (!response) {
        throw new Error('Empty response from AI');
      }

      let result: any; // Use any for initial parsing as structure might be unexpected
      try {
        result = JSON.parse(response);
      } catch (parseError: any) {
        throw new Error(`Invalid JSON response: ${parseError.message}\nReceived: ${response}`);
      }

      // Validate required fields using Zod parse
      const validationResult = FrontmatterSchema.safeParse(result);

      if (!validationResult.success) {
         // Log Zod errors but don't necessarily throw, might try to fix below
         console.error('Zod validation failed on AI generated frontmatter:', validationResult.error.issues);
         // Attempt to return the partial result even if validation fails, 
         // calling code might merge it.
         return result as Frontmatter; 
      }

      return validationResult.data; // Return the validated data
      
    } catch (error: any) {
      console.error(`\nError details for AI frontmatter generation:`);
      console.error(`- Original error: ${error.message}`);
      if (error.cause) {
        console.error(`- Cause: ${error.cause}`);
      }
      // Don't exit here, allow processFile to handle the failure
      return undefined; // Return undefined on error
    }
  }

  async processFile(filePath: string): Promise<{ updated: boolean; error?: any }> {
    let content: string;
    try {
        content = await fspromises.readFile(filePath, 'utf8');
    } catch (readError) {
        console.error(`Error reading file ${filePath}:`, readError);
        return { updated: false, error: readError };
    }
    
    const { data: frontmatter, content: markdownContent, isEmpty } = matter(content);

    try {
      // Convert any Date objects to ISO strings before validation
      // Also handle cases where tags might be an array instead of a string
      const normalizedFrontmatter: any = {
        ...frontmatter,
        date: frontmatter.date instanceof Date ? frontmatter.date.toISOString() : frontmatter.date,
        dateCreated: frontmatter.dateCreated instanceof Date ? frontmatter.dateCreated.toISOString() : frontmatter.dateCreated,
        tags: Array.isArray(frontmatter.tags) ? frontmatter.tags.join(', ') : frontmatter.tags
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

        // Only generate frontmatter if it's missing or invalid, or if tags are empty/missing
        const shouldGenerateMetadata = isEmpty || 
          Object.keys(frontmatter).length === 0 || 
          !frontmatter.tags || 
          (Array.isArray(frontmatter.tags) && frontmatter.tags.length === 0) ||
          !validationResult.success; // Also generate if validation failed

        const generatedFrontmatter = shouldGenerateMetadata ? 
          await this.generateFrontmatter(markdownContent) :
          undefined; // Explicitly undefined if not generating
        
        if (!generatedFrontmatter && shouldGenerateMetadata) {
          const error = new Error('Failed to generate frontmatter metadata');
          error.context = { filePath, frontmatter: normalizedFrontmatter };
          // Don't return early, try to fix with existing data + defaults
        }

        // Merge existing, generated, and default values
        const updatedFrontmatter: Frontmatter = {
           // Start with defaults
          published: true,
          editor: 'markdown',
          date: new Date().toISOString(), // Default date
          dateCreated: new Date().toISOString(), // Default dateCreated
          tags: '', // Default empty tags
          title: '', // Default empty title (required)
          description: '', // Default empty description (required)

          // Merge generated data (if any), it overrides defaults
          ...(generatedFrontmatter || {}),

          // Merge existing data, it overrides generated and defaults
          ...Object.fromEntries(
            Object.entries(normalizedFrontmatter)
              .filter(([key, value]) => {
                // Keep existing values unless they are explicitly empty/null/undefined
                 return value !== undefined && value !== null && value !== '';
              })
          ),
           // Special handling for tags - prefer existing if not empty array/string
          tags: (Array.isArray(normalizedFrontmatter.tags) && normalizedFrontmatter.tags.length > 0) ? normalizedFrontmatter.tags.join(', ') :
                (normalizedFrontmatter.tags && normalizedFrontmatter.tags !== '') ? normalizedFrontmatter.tags :
                (Array.isArray(generatedFrontmatter?.tags) ? generatedFrontmatter.tags.join(', ') : generatedFrontmatter?.tags) || '' // Use generated if existing is empty

        };
        
        // Ensure required fields are not empty after merging
        if (!updatedFrontmatter.title) updatedFrontmatter.title = "Untitled"; // Fallback title
        if (!updatedFrontmatter.description) updatedFrontmatter.description = "No description provided."; // Fallback description

        const finalValidation = FrontmatterSchema.safeParse(updatedFrontmatter);

        if (finalValidation.success) {
          // Preserve the original content exactly as it was, with emoji support
          const updatedContent = matter.stringify(markdownContent.trim(), updatedFrontmatter, {
            engines: {
              yaml: {
                stringify: (obj: any) => yaml.dump(obj, { lineWidth: -1 }) // Use yaml.dump
              }
            }
          });
          
          try {
            await fspromises.writeFile(filePath, updatedContent);
            console.log(`✅ Updated and fixed frontmatter for: ${filePath}`);
            return { updated: true };
          } catch (writeError) {
             console.error(`Error writing file ${filePath}:`, writeError);
             return { updated: false, error: writeError };
          }

        } else {
          const error = new Error('Failed to fix frontmatter validation issues after merging.');
          error.issues = finalValidation.error.issues;
          error.context = { 
            filePath,
            originalFrontmatter: normalizedFrontmatter,
            updatedFrontmatter
          };
           console.error(`\n❌ Failed to fix frontmatter in file: ${filePath}`);
           error.issues.forEach((issue: any) => {
              console.error(`  - Field: ${issue.path.join('.')} - ${issue.message}`);
            });

          return { updated: false, error };
        }
      } else {
        console.log(`✅ Valid frontmatter in file: ${filePath}`);
        return { updated: false };
      }
    } catch (error: any) {
      error.context = { filePath, frontmatter };
      console.error(`\nAn unexpected error occurred processing file ${filePath}:`, error);
      return { updated: false, error };
    }
  }
}

async function findMarkdownFiles(dir: string, ig: Ignore): Promise<string[]> {
  // Read .gitignore if it exists at the current directory level
  try {
    const gitignorePath = path.join(dir, '.gitignore');
    const gitignoreContent = await fspromises.readFile(gitignorePath, 'utf8');
    ig = ignore().add(gitignoreContent); // Create a new ignore instance for this directory and combine rules
  } catch (error: any) {
    // If .gitignore doesn't exist or can't be read, use the inherited ignore rules
  }

  let files: fs.Dirent[];
   try {
        files = await fspromises.readdir(dir, { withFileTypes: true });
   } catch (readDirError) {
        console.error(`Error reading directory ${dir}:`, readDirError);
        return []; // Return empty array if directory can't be read
   }
  
  let markdownFiles: string[] = [];

  for (const file of files) {
    const fullPath = path.join(dir, file.name);
    const relativePath = path.relative(process.cwd(), fullPath); // Use process.cwd() as root for ignore

    // Skip if file/directory is ignored by .gitignore rules
    if (ig.ignores(relativePath)) {
      // console.log(`Ignoring: ${relativePath}`); // Optional: for debugging ignore rules
      continue;
    }

    if (file.isDirectory()) {
      // Recursively search directories, passing the current ignore instance
      markdownFiles = markdownFiles.concat(await findMarkdownFiles(fullPath, ig));
    } else if (file.isFile() && file.name.endsWith('.md')) {
      markdownFiles.push(fullPath);
    }
  }

  return markdownFiles;
}

async function validateMarkdownFiles(files: string[]): Promise<string[]> {
  const invalidFiles: string[] = [];
  const llmClient = new LLMClient(); // Assuming LLMClient is instantiated here
  const frontmatterGenerator = new FrontmatterGenerator(llmClient);

  console.log(`\nProcessing ${files.length} markdown files...\n`);

  for (const file of files) {
    const result = await frontmatterGenerator.processFile(file);
    if (result.error) {
      // Error details are already logged inside processFile
      invalidFiles.push(file);
    }
  }
  
  return invalidFiles;
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const targetFile = args[0]; // First argument could be a specific file or directory

  if (!targetFile) {
    console.log('Usage: node fix_frontmatter_metadata.js <file_or_directory> [--check]');
    console.log('  <file_or_directory>: The specific markdown file or directory to process.');
    console.log('  --check: Only check for invalid frontmatter, do not attempt to fix or generate.');
    process.exit(0);
  }

  const checkOnly = args.includes('--check');
  
  const fullPath = path.resolve(process.cwd(), targetFile);

  let markdownFiles: string[] = [];

  try {
    const stats = await fspromises.stat(fullPath);
    const initialIgnore = ignore(); // Create initial ignore instance
    
    if (stats.isDirectory()) {
      console.log(`Finding markdown files in directory: ${fullPath}`);
      markdownFiles = await findMarkdownFiles(fullPath, initialIgnore);
    } else if (stats.isFile() && fullPath.endsWith('.md')) {
      console.log(`Processing single markdown file: ${fullPath}`);
      markdownFiles = [fullPath];
    } else {
      console.error(`Error: Target is not a markdown file or a directory: ${targetFile}`);
      process.exit(1);
    }
  } catch (error) {
    console.error(`Error accessing target file or directory ${targetFile}:`, error);
    process.exit(1);
  }

  if (markdownFiles.length === 0) {
    console.log('No markdown files found to process.');
    process.exit(0);
  }

  if (checkOnly) {
    console.log('\nRunning in check-only mode. Reporting invalid frontmatter...');
    // In check-only mode, we still process to find invalid ones, but processFile
    // won't attempt to write changes because shouldGenerateMetadata logic accounts for validation success.
    // A dedicated check function might be slightly more efficient by skipping AI calls,
    // but processing with processFile still validates and reports errors.
    const llmClient = new LLMClient(); // Need client even for check to potentially generate
    const frontmatterGenerator = new FrontmatterGenerator(llmClient);
    
    const filesWithInvalidFrontmatter: string[] = [];

    console.log(`\nChecking ${markdownFiles.length} markdown files for invalid frontmatter...\n`);

    for (const file of markdownFiles) {
      const content = await fspromises.readFile(file, 'utf8');
      const { data: frontmatter } = matter(content);
      
      // Convert Date objects and handle array tags for validation
       const normalizedFrontmatter: any = {
        ...frontmatter,
        date: frontmatter.date instanceof Date ? frontmatter.date.toISOString() : frontmatter.date,
        dateCreated: frontmatter.dateCreated instanceof Date ? frontmatter.dateCreated.toISOString() : frontmatter.dateCreated,
         tags: Array.isArray(frontmatter.tags) ? frontmatter.tags.join(', ') : frontmatter.tags
      };

      const validationResult = FrontmatterSchema.safeParse(normalizedFrontmatter);

      if (!validationResult.success) {
        filesWithInvalidFrontmatter.push(file);
        console.log(`\n❌ Invalid frontmatter in file: ${file}`);
        console.log('Current frontmatter:');
        console.log(JSON.stringify(normalizedFrontmatter, null, 2));
        console.log('\nValidation errors:');
        validationResult.error.issues.forEach(issue => {
          console.log(`  - Field: ${issue.path.join('.')} - ${issue.message}`);
        });
      } else {
         console.log(`✅ Valid frontmatter in file: ${file}`);
      }
    }

    if (filesWithInvalidFrontmatter.length > 0) {
      console.log(`\nFound ${filesWithInvalidFrontmatter.length} file(s) with invalid frontmatter:`);
      filesWithInvalidFrontmatter.forEach(f => console.log(`- ${f}`));
      process.exit(1); // Exit with error code if invalid files are found
    } else {
      console.log('\nAll processed files have valid frontmatter.');
      process.exit(0);
    }

  } else {
    // Running in fix mode
    const invalidFilesAfterFix = await validateMarkdownFiles(markdownFiles);

    if (invalidFilesAfterFix.length > 0) {
      console.error(`\n❌ Failed to fix frontmatter in ${invalidFilesAfterFix.length} file(s):`);
      invalidFilesAfterFix.forEach(f => console.error(`- ${f}`));
      process.exit(1); // Exit with error code if some files could not be fixed
    } else {
      console.log('\nSuccessfully processed all specified markdown files.');
      process.exit(0);
    }
  }
}

if (require.main === module) {
    main();
}

// module.exports = { FrontmatterGenerator }; // Export if needed elsewhere 