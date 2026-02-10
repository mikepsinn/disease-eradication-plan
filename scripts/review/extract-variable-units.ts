import yaml from 'js-yaml';
import fs from 'fs/promises';
import path from 'path';

interface VariableUnitMapping {
  [variableName: string]: string;
}

/**
 * Infer unit text from variable name patterns
 */
function inferUnitFromVariableName(variableName: string): string | null {
  // Common patterns to extract unit text
  const patterns = [
    // Annual return patterns
    { regex: /_annual_return(?:_pct)?$/, unit: 'annual return' },

    // Daily deaths patterns
    { regex: /_deaths_daily$/, unit: 'daily deaths' },
    { regex: /_daily_deaths$/, unit: 'daily deaths' },

    // Per patient patterns
    { regex: /_per_patient$/, unit: 'per patient' },

    // Time units
    { regex: /_years$/, unit: 'years' },
    { regex: /_months$/, unit: 'months' },
    { regex: /_days$/, unit: 'days' },

    // Count units
    { regex: /_patients$/, unit: 'patients' },
    { regex: /_people$/, unit: 'people' },
    { regex: /_deaths?$/, unit: 'deaths' },
    { regex: /_lives$/, unit: 'lives' },
    { regex: /_pairings$/, unit: 'pairings' },
    { regex: /_members$/, unit: 'members' },
    { regex: /_senators$/, unit: 'senators' },
    { regex: /_drugs$/, unit: 'drugs' },
    { regex: /_trials$/, unit: 'trials' },

    // Rate units
    { regex: /_per_year$/, unit: 'per year' },
    { regex: /_annual$/, unit: 'annual' },
    { regex: /_daily$/, unit: 'daily' },
  ];

  for (const { regex, unit } of patterns) {
    if (regex.test(variableName)) {
      return unit;
    }
  }

  return null;
}

async function extractVariableUnits(): Promise<void> {
  console.log('Extracting variable units from _variables.yml...\n');

  // Load _variables.yml
  const variablesPath = path.join(process.cwd(), '_variables.yml');
  const fileContent = await fs.readFile(variablesPath, 'utf-8');
  const variables = yaml.load(fileContent) as Record<string, string>;

  const unitMappings: VariableUnitMapping = {};
  let matchedCount = 0;
  let totalCount = 0;

  // Process each variable
  for (const [variableName, value] of Object.entries(variables)) {
    // Skip citation variables
    if (variableName.endsWith('_cite') || variableName.endsWith('_latex')) {
      continue;
    }

    totalCount++;

    // Try to infer unit from variable name
    const unit = inferUnitFromVariableName(variableName);

    if (unit) {
      unitMappings[variableName] = unit;
      matchedCount++;
      console.log(`✓ ${variableName} → "${unit}"`);
    }
  }

  // Save to JSON file
  const outputPath = path.join(process.cwd(), 'variable-units.json');
  await fs.writeFile(outputPath, JSON.stringify(unitMappings, null, 2), 'utf-8');

  console.log('\n' + '='.repeat(80));
  console.log('EXTRACTION COMPLETE');
  console.log('='.repeat(80));
  console.log(`Total variables processed: ${totalCount}`);
  console.log(`Variables with inferred units: ${matchedCount}`);
  console.log(`Output saved to: ${outputPath}`);
  console.log('='.repeat(80));
}

extractVariableUnits().catch(err => {
  console.error('Error extracting variable units:', err);
  process.exit(1);
});
