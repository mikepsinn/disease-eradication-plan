import fs from 'fs/promises';
import matter from 'gray-matter';

export function programmaticFormat(content: string): string {
  let result = content;

  // Normalize line endings to LF for consistent processing
  result = result.replace(/\r\n/g, '\n');

  // Fixes spacing for unordered lists: "-   item" -> "- item"
  result = result.replace(/^(-|\*)\s+/gm, '$1 ');

  // Add a blank line after a bolded line, unless it's followed by another blank line, a list, a heading, or a code block
  result = result.replace(
    /^(\*\*[^*]+\*\*)\n(?!\n)(?![-*+]\s)(?!#{1,6}\s)(?!```)/gm,
    '$1\n\n'
  );

  // Add a blank line after "Speaker: "quote"" format
  result = result.replace(
    /^([A-Z][A-Za-z]*:\s+"[^"]+[.!"?]?")\n(?!\n)(?![-*+]\s)(?!#{1,6}\s)(?!```)/gm,
    '$1\n\n'
  );

  // Add a blank line after common key-value pairs
  result = result.replace(
    /^((?:Post|Bounty|Deadline|Amount|Price|Cost|Total|Budget):\s+[^\n]+)\n(?!\n)(?![-*+]\s)(?!#{1,6}\s)(?!```)/gm,
    '$1\n\n'
  );

  return result;
}

// Shared file-saving function that applies programmatic formatting.
export async function saveFile(filePath: string, content: string): Promise<void> {
  const formattedContent = programmaticFormat(content);
  await fs.writeFile(filePath, formattedContent, 'utf-8');
}
