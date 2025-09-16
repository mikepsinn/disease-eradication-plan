import fs from 'fs/promises';
import path from 'path';

interface Reference {
  id: string;
  content: string;
}

async function sortReferences() {
  const referencesFilePath = path.join(process.cwd(), 'brain', 'book', 'references.md');
  const fileContent = await fs.readFile(referencesFilePath, 'utf-8');

  const lines = fileContent.split('\n');
  const firstReferenceLineIndex = lines.findIndex(line => line.trim().startsWith('<a id="'));

  if (firstReferenceLineIndex === -1) {
    console.log('No references found to sort.');
    return;
  }

  const header = lines.slice(0, firstReferenceLineIndex).join('\n');
  const referencesContent = lines.slice(firstReferenceLineIndex).join('\n');

  const referenceBlocks = referencesContent.split(/(?=<a id="[^"]+"><\/a>)/g).filter(block => block.trim() !== '');

  const references: Reference[] = referenceBlocks.map(block => {
    const match = block.match(/<a id="([^"]+)">/);
    const id = match ? match[1] : '';
    return { id, content: block };
  });

  const idCounts = references.reduce((acc, ref) => {
    acc[ref.id] = (acc[ref.id] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const duplicates = Object.entries(idCounts).filter(([, count]) => count > 1);

  if (duplicates.length > 0) {
    console.warn('⚠️ Found duplicate reference IDs:');
    duplicates.forEach(([id, count]) => {
      console.warn(`  - "${id}" appears ${count} times.`);
    });
  }

  references.sort((a, b) => a.id.localeCompare(b.id));

  const sortedReferencesContent = references.map(ref => ref.content).join('');
  
  const newFileContent = header + '\n' + sortedReferencesContent.trimEnd() + '\n';

  await fs.writeFile(referencesFilePath, newFileContent, 'utf-8');
  console.log('✅ Successfully sorted references in ' + referencesFilePath);
}

sortReferences().catch(error => {
  console.error('Error sorting references:', error);
  process.exit(1);
});
