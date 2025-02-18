import { google } from 'googleapis';
import { OAuth2Client } from 'google-auth-library';
import * as fs from 'fs';
import * as path from 'path';
import MarkdownIt from 'markdown-it';
import * as matter from 'gray-matter';
import dotenv from 'dotenv';

dotenv.config();

const md = new MarkdownIt();

interface DocMapping {
  localPath: string;
  googleDocId: string;
  lastSynced: Date;
}

class GoogleDocsSync {
  private docs: any;
  private mappingFile = 'gdocs-mapping.json';
  private mapping: DocMapping[] = [];

  constructor(private auth: OAuth2Client) {
    this.docs = google.docs({ version: 'v1', auth });
    this.loadMapping();
  }

  private loadMapping() {
    if (fs.existsSync(this.mappingFile)) {
      this.mapping = JSON.parse(fs.readFileSync(this.mappingFile, 'utf-8'));
    }
  }

  private saveMapping() {
    fs.writeFileSync(this.mappingFile, JSON.stringify(this.mapping, null, 2));
  }

  private async convertMarkdownToGoogleDocs(markdown: string): Promise<any[]> {
    const html = md.render(markdown);
    // Convert HTML to Google Docs format
    // This is a simplified version - you might want to expand this
    return [{
      insertText: {
        text: markdown,
        endOfSegmentLocation: {}
      }
    }];
  }

  private async convertGoogleDocsToMarkdown(doc: any): Promise<string> {
    // Convert Google Docs content to Markdown
    // This is a simplified version - you might want to expand this
    return doc.body.content
      .map((element: any) => {
        if (element.paragraph) {
          return element.paragraph.elements
            .map((e: any) => e.textRun?.content || '')
            .join('');
        }
        return '';
      })
      .join('\n');
  }

  async syncToGoogleDocs(localPath: string) {
    const content = fs.readFileSync(localPath, 'utf-8');
    const { data, content: markdownContent } = matter(content);
    
    let docMapping = this.mapping.find(m => m.localPath === localPath);
    
    if (!docMapping) {
      // Create new Google Doc
      const response = await this.docs.documents.create({
        requestBody: {
          title: path.basename(localPath, '.md')
        }
      });
      
      docMapping = {
        localPath,
        googleDocId: response.data.documentId,
        lastSynced: new Date()
      };
      this.mapping.push(docMapping);
    }

    // Update Google Doc content
    await this.docs.documents.batchUpdate({
      documentId: docMapping.googleDocId,
      requestBody: {
        requests: await this.convertMarkdownToGoogleDocs(markdownContent)
      }
    });

    docMapping.lastSynced = new Date();
    this.saveMapping();
  }

  async syncFromGoogleDocs(localPath: string) {
    const docMapping = this.mapping.find(m => m.localPath === localPath);
    if (!docMapping) {
      throw new Error(`No mapping found for ${localPath}`);
    }

    const response = await this.docs.documents.get({
      documentId: docMapping.googleDocId
    });

    const markdown = await this.convertGoogleDocsToMarkdown(response.data);
    
    // Preserve frontmatter if it exists
    const existingContent = fs.readFileSync(localPath, 'utf-8');
    const { data: frontmatter } = matter(existingContent);
    
    const newContent = matter.stringify(markdown, frontmatter);
    fs.writeFileSync(localPath, newContent);

    docMapping.lastSynced = new Date();
    this.saveMapping();
  }

  async syncDirectory(dirPath: string) {
    const files = fs.readdirSync(dirPath)
      .filter(file => file.endsWith('.md'))
      .map(file => path.join(dirPath, file));

    for (const file of files) {
      await this.syncToGoogleDocs(file);
      await this.syncFromGoogleDocs(file);
    }
  }
}

async function main() {
  const credentials = {
    client_id: process.env.GOOGLE_CLIENT_ID,
    client_secret: process.env.GOOGLE_CLIENT_SECRET,
    redirect_uri: process.env.GOOGLE_REDIRECT_URI
  };

  const oauth2Client = new google.auth.OAuth2(
    credentials.client_id,
    credentials.client_secret,
    credentials.redirect_uri
  );

  // Set credentials from environment or token file
  if (process.env.GOOGLE_ACCESS_TOKEN) {
    oauth2Client.setCredentials({
      access_token: process.env.GOOGLE_ACCESS_TOKEN,
      refresh_token: process.env.GOOGLE_REFRESH_TOKEN
    });
  }

  const sync = new GoogleDocsSync(oauth2Client);
  await sync.syncDirectory(process.argv[2] || '.');
}

if (require.main === module) {
  main().catch(console.error);
} 