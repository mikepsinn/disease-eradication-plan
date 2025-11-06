import * as fs from 'fs';
import * as path from 'path';
import { saveFile } from './lib/file-utils';

interface FileRenameMapping {
  oldName: string;
  newName: string;
  description: string;
}

const renameMapping: FileRenameMapping[] = [
  {
    oldName: 'fda-spending-vs-life-expectancy',
    newName: 'historical-life-expectancy-fda-budget-drug-costs-1901-2000',
    description: 'Historical time series data (1901-2000) tracking life expectancy before/after FDA creation, FDA budget (inflation-adjusted to 2020 USD), new drug applications, and cost to develop new drugs'
  },
  {
    oldName: 'reducing-cost-graph',
    newName: 'life-expectancy-fda-budget-cost-analysis-1901-2000',
    description: 'Similar to main dataset but includes cost in millions column, used for cost reduction analysis charts'
  },
  {
    oldName: 'diminishing-returns',
    newName: 'life-expectancy-gains-pre-post-fda-comparison-1901-2000',
    description: 'Comparison of annual life expectancy increases before and after FDA creation, demonstrating diminishing returns on health improvements'
  },
  {
    oldName: 'sources',
    newName: 'data-sources-references',
    description: 'Reference URLs and sources for drug development costs and FDA budget data'
  },
  {
    oldName: 'cpi',
    newName: 'consumer-price-index-inflation-1913-2020',
    description: 'Consumer Price Index annual averages and inflation rates from Federal Reserve (1913-2020) for adjusting historical costs'
  },
  {
    oldName: 'cost-chart-wo-projections',
    newName: 'chart-placeholder-historical-only',
    description: 'Empty placeholder - contained chart object in Excel showing historical costs without projections'
  },
  {
    oldName: 'cost-chart-projections',
    newName: 'chart-placeholder-with-projections',
    description: 'Empty placeholder - contained chart object in Excel showing costs with future projections'
  }
];

async function renameFiles(extractDir: string): Promise<void> {
  console.log(`Renaming files in: ${extractDir}\n`);

  const renamedFiles: Array<{old: string, new: string, description: string}> = [];

  for (const mapping of renameMapping) {
    const csvOldPath = path.join(extractDir, `${mapping.oldName}.csv`);
    const csvNewPath = path.join(extractDir, `${mapping.newName}.csv`);
    const mdOldPath = path.join(extractDir, `${mapping.oldName}.md`);
    const mdNewPath = path.join(extractDir, `${mapping.newName}.md`);

    // Rename CSV if exists
    if (fs.existsSync(csvOldPath)) {
      fs.renameSync(csvOldPath, csvNewPath);
      console.log(`✓ Renamed CSV: ${mapping.oldName}.csv → ${mapping.newName}.csv`);
    }

    // Rename MD if exists
    if (fs.existsSync(mdOldPath)) {
      // Read the markdown file to update internal references
      let mdContent = fs.readFileSync(mdOldPath, 'utf-8');

      // Update the CSV reference in the markdown
      mdContent = mdContent.replace(
        new RegExp(`\\[${mapping.oldName}\\.csv\\]\\(${mapping.oldName}\\.csv\\)`, 'g'),
        `[${mapping.newName}.csv](${mapping.newName}.csv)`
      );

      // Update the title
      const oldTitle = mapping.oldName.split('-').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
      ).join(' ');

      const newTitle = mapping.newName.split('-').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
      ).join(' ');

      mdContent = mdContent.replace(`# ${oldTitle}`, `# ${newTitle}`);

      // Write to new file
      await saveFile(mdNewPath, mdContent);

      // Delete old file
      fs.unlinkSync(mdOldPath);

      console.log(`✓ Renamed MD:  ${mapping.oldName}.md → ${mapping.newName}.md`);
    }

    renamedFiles.push({
      old: mapping.oldName,
      new: mapping.newName,
      description: mapping.description
    });

    console.log('');
  }

  // Generate updated README
  console.log('Generating updated README...\n');

  let readme = `# FDA Spending vs Life-Expectancy Data Extract\n\n`;
  readme += `Extracted from: \`FDA Spending vs Life-Expectancy.xlsx\`\n\n`;
  readme += `**Extraction Date:** ${new Date().toISOString().split('T')[0]}\n\n`;
  readme += `## Overview\n\n`;
  readme += `This workbook contains historical data analyzing the relationship between FDA spending, `;
  readme += `drug development costs, and life expectancy trends from 1901-2000. The data is used to `;
  readme += `examine the effectiveness and cost-efficiency of FDA regulations on public health outcomes.\n\n`;

  readme += `## Data Files\n\n`;
  readme += `This workbook contains ${renameMapping.length} sheets, extracted to ${renameMapping.length * 2} files `;
  readme += `(CSV + Markdown for each):\n\n`;

  for (const file of renamedFiles) {
    readme += `### ${file.new}\n\n`;
    readme += `${file.description}\n\n`;
    readme += `- **CSV:** [${file.new}.csv](${file.new}.csv)\n`;
    readme += `- **Markdown:** [${file.new}.md](${file.new}.md)\n\n`;
  }

  readme += `## File Types\n\n`;
  readme += `### CSV Files\n`;
  readme += `Raw comma-separated data files that can be imported into:\n`;
  readme += `- Spreadsheet applications (Excel, Google Sheets, LibreOffice)\n`;
  readme += `- Data analysis tools (R, Python pandas, MATLAB)\n`;
  readme += `- Databases (PostgreSQL, MySQL, SQLite)\n`;
  readme += `- Statistical software (SPSS, SAS, Stata)\n\n`;

  readme += `### Markdown Files\n`;
  readme += `Human-readable preview files with:\n`;
  readme += `- Sheet metadata (dimensions, source)\n`;
  readme += `- Formatted data tables (first 20 rows)\n`;
  readme += `- Links to corresponding CSV files\n\n`;

  readme += `## Data Quality Notes\n\n`;
  readme += `- **Inflation Adjustment:** All monetary values adjusted to 2020 USD using CPI data\n`;
  readme += `- **Time Range:** Primary datasets cover 1901-2000 (99 years)\n`;
  readme += `- **Chart Placeholders:** Two files are empty as they contained embedded Excel charts (not extractable)\n`;
  readme += `- **CPI Data:** Separate sheet contains Consumer Price Index data (1913-2020) used for adjustments\n\n`;

  readme += `## Usage Examples\n\n`;
  readme += `### Python\n`;
  readme += `\`\`\`python\n`;
  readme += `import pandas as pd\n\n`;
  readme += `# Load the main historical dataset\n`;
  readme += `df = pd.read_csv('historical-life-expectancy-fda-budget-drug-costs-1901-2000.csv')\n`;
  readme += `print(df.head())\n`;
  readme += `\`\`\`\n\n`;

  readme += `### R\n`;
  readme += `\`\`\`r\n`;
  readme += `# Load the diminishing returns data\n`;
  readme += `df <- read.csv('life-expectancy-gains-pre-post-fda-comparison-1901-2000.csv')\n`;
  readme += `summary(df)\n`;
  readme += `\`\`\`\n\n`;

  readme += `## Sources\n\n`;
  readme += `See [data-sources-references.csv](data-sources-references.csv) for complete list of source URLs `;
  readme += `including:\n`;
  readme += `- FDA budget documentation\n`;
  readme += `- Drug development cost studies\n`;
  readme += `- Clinical trial cost analyses\n`;
  readme += `- Historical life expectancy data\n`;

  const readmePath = path.join(extractDir, 'README.md');
  await saveFile(readmePath, readme);
  console.log('✓ Updated README.md with descriptive filenames and detailed documentation\n');

  console.log('═══════════════════════════════════════════════════════');
  console.log('✓ File renaming complete!');
  console.log('═══════════════════════════════════════════════════════');
}

// Main execution
const extractDir = process.argv[2] || 'assets/extracted-fda-data';

renameFiles(path.resolve(extractDir))
  .catch(error => {
    console.error('Error renaming files:', error);
    process.exit(1);
  });
