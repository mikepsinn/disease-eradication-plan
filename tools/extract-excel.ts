import XLSX from 'xlsx';
import * as fs from 'fs';
import * as path from 'path';
import { saveFile } from './lib/file-utils';

interface SheetInfo {
  name: string;
  rowCount: number;
  columnCount: number;
  csvPath: string;
}

async function extractExcelFile(excelPath: string, outputDir: string): Promise<void> {
  console.log(`Reading Excel file: ${excelPath}`);

  // Read the Excel file
  const workbook = XLSX.readFile(excelPath, {
    cellStyles: true,
    cellDates: true,
  });

  // Create output directory if it doesn't exist
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const sheetInfos: SheetInfo[] = [];

  // Process each sheet
  for (const sheetName of workbook.SheetNames) {
    console.log(`\nProcessing sheet: ${sheetName}`);

    const worksheet = workbook.Sheets[sheetName];

    // Get sheet range
    const range = XLSX.utils.decode_range(worksheet['!ref'] || 'A1');
    const rowCount = range.e.r - range.s.r + 1;
    const columnCount = range.e.c - range.s.c + 1;

    console.log(`  Rows: ${rowCount}, Columns: ${columnCount}`);

    // Convert sheet to CSV
    const csv = XLSX.utils.sheet_to_csv(worksheet, { FS: ',', RS: '\n' });
    const csvFileName = `${sheetName.replace(/[^a-z0-9]/gi, '-').toLowerCase()}.csv`;
    const csvPath = path.join(outputDir, csvFileName);
    fs.writeFileSync(csvPath, csv);
    console.log(`  Saved CSV: ${csvFileName}`);

    // Convert sheet to JSON for markdown table
    const json = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

    sheetInfos.push({
      name: sheetName,
      rowCount,
      columnCount,
      csvPath: csvFileName,
    });

    // Create a markdown file with the data
    const mdFileName = `${sheetName.replace(/[^a-z0-9]/gi, '-').toLowerCase()}.md`;
    const mdPath = path.join(outputDir, mdFileName);
    let mdContent = `# ${sheetName}\n\n`;
    mdContent += `**Sheet Information:**\n`;
    mdContent += `- Rows: ${rowCount}\n`;
    mdContent += `- Columns: ${columnCount}\n`;
    mdContent += `- CSV File: [${csvFileName}](${csvFileName})\n\n`;

    // Add a preview of the data (first 20 rows)
    if (json.length > 0) {
      mdContent += `## Data Preview\n\n`;
      const previewRows = json.slice(0, 20);

      // Create markdown table
      if (previewRows.length > 0) {
        const headers = previewRows[0] as any[];
        mdContent += `| ${headers.join(' | ')} |\n`;
        mdContent += `| ${headers.map(() => '---').join(' | ')} |\n`;

        for (let i = 1; i < previewRows.length; i++) {
          const row = previewRows[i] as any[];
          mdContent += `| ${row.map(cell => cell ?? '').join(' | ')} |\n`;
        }
      }

      if (json.length > 20) {
        mdContent += `\n*Showing first 20 rows of ${json.length} total rows.*\n`;
      }
    }

    await saveFile(mdPath, mdContent);
    console.log(`  Saved Markdown: ${mdFileName}`);
  }

  // Create summary markdown file
  const summaryPath = path.join(outputDir, 'README.md');
  let summary = `# FDA Spending vs Life-Expectancy Data Extract\n\n`;
  summary += `Extracted from: \`${path.basename(excelPath)}\`\n\n`;
  summary += `**Extraction Date:** ${new Date().toISOString().split('T')[0]}\n\n`;
  summary += `## Sheets\n\n`;
  summary += `This workbook contains ${sheetInfos.length} sheet(s):\n\n`;

  for (const info of sheetInfos) {
    summary += `### ${info.name}\n\n`;
    summary += `- **Dimensions:** ${info.rowCount} rows × ${info.columnCount} columns\n`;
    summary += `- **CSV:** [${info.csvPath}](${info.csvPath})\n`;
    summary += `- **Markdown:** [${info.csvPath.replace('.csv', '.md')}](${info.csvPath.replace('.csv', '.md')})\n\n`;
  }

  summary += `## Files Generated\n\n`;
  summary += `- CSV files: One per sheet with raw data\n`;
  summary += `- Markdown files: One per sheet with formatted preview tables\n`;
  summary += `- This README: Summary of all extracted data\n\n`;
  summary += `## Usage\n\n`;
  summary += `The CSV files can be imported into any data analysis tool, spreadsheet application, or database.\n`;
  summary += `The markdown files provide human-readable previews of the data.\n`;

  await saveFile(summaryPath, summary);
  console.log(`\n✓ Summary saved: README.md`);
  console.log(`\n✓ Extraction complete! Files saved to: ${outputDir}`);
}

// Main execution
const excelPath = process.argv[2] || 'brain/data/FDA Spending vs Life-Expectancy.xlsx';
const outputDir = process.argv[3] || 'assets/extracted-fda-data';

extractExcelFile(path.resolve(excelPath), path.resolve(outputDir))
  .catch(error => {
    console.error('Error extracting Excel file:', error);
    process.exit(1);
  });
