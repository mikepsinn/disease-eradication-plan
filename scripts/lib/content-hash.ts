import fs from 'fs/promises';
import matter from 'gray-matter';
import crypto from 'crypto';
import { saveFile } from './file-utils';

/**
 * Calculate hash of the body content (excluding frontmatter)
 */
export function getBodyHash(content: string): string {
  const { content: body } = matter(content);
  return crypto.createHash('sha256').update(body).digest('hex');
}

/**
 * Reads a file and parses its frontmatter and body
 */
export async function readFileWithMatter(filePath: string): Promise<{ frontmatter: any; body: string; originalContent: string }> {
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(originalContent);
  return { frontmatter, body, originalContent };
}

/**
 * Updates a file with new content and calculates/stores a hash
 */
export async function updateFileWithHash(
  filePath: string,
  body: string,
  frontmatter: any,
  hashFieldName: string
): Promise<void> {
  const tempContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  frontmatter[hashFieldName] = getBodyHash(tempContent);
  const newContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  await saveFile(filePath, newContent);
}
