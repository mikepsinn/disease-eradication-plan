#!/usr/bin/env npx tsx
/**
 * Extract all Quarto variables used in a QMD file with their line numbers.
 * Outputs a condensed report to help identify missing LaTeX equations.
 *
 * Usage:
 *   npx tsx scripts/extract-qmd-variables.ts <qmd-file> [output-file]
 *
 * Example:
 *   npx tsx scripts/extract-qmd-variables.ts knowledge/economics/economics.qmd
 */

import * as fs from "fs";
import * as path from "path";
import * as yaml from "js-yaml";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

interface VariableUsage {
  variable: string;
  line: number;
  context: string;
}

interface VariableStats {
  usages: VariableUsage[];
  hasLatex: boolean;
  usageCount: number;
}

function extractVariables(filePath: string): Map<string, VariableUsage[]> {
  const content = fs.readFileSync(filePath, "utf-8");
  const lines = content.split("\n");
  const variableMap = new Map<string, VariableUsage[]>();

  // Match {{< var variable_name >}} pattern
  const varPattern = /\{\{<\s*var\s+([a-zA-Z0-9_]+)\s*>\}\}/g;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    let match;
    while ((match = varPattern.exec(line)) !== null) {
      const varName = match[1];
      const usage: VariableUsage = {
        variable: varName,
        line: i + 1,
        context: line.trim().substring(0, 100),
      };

      if (!variableMap.has(varName)) {
        variableMap.set(varName, []);
      }
      variableMap.get(varName)!.push(usage);
    }
  }

  return variableMap;
}

function loadVariablesYaml(
  yamlPath: string
): Map<string, boolean> {
  const availableVars = new Map<string, boolean>();

  if (!fs.existsSync(yamlPath)) {
    console.warn(`Warning: Variables file not found: ${yamlPath}`);
    return availableVars;
  }

  const content = fs.readFileSync(yamlPath, "utf-8");
  const data = yaml.load(content) as Record<string, unknown>;

  if (data && typeof data === "object") {
    for (const key of Object.keys(data)) {
      availableVars.set(key, true);
    }
  }

  return availableVars;
}

function generateReport(
  qmdPath: string,
  variableMap: Map<string, VariableUsage[]>,
  availableVars: Map<string, boolean>
): string {
  const lines: string[] = [];

  lines.push(`# QMD Variable Usage Report`);
  lines.push(`Generated: ${new Date().toISOString()}`);
  lines.push(`Source file: ${qmdPath}`);
  lines.push(``);

  // Summary statistics
  const uniqueVars = variableMap.size;
  const totalUsages = Array.from(variableMap.values()).reduce(
    (sum, arr) => sum + arr.length,
    0
  );

  lines.push(`## Summary`);
  lines.push(`- Unique variables: ${uniqueVars}`);
  lines.push(`- Total variable usages: ${totalUsages}`);
  lines.push(``);

  // Find variables missing LaTeX equivalents
  const missingLatex: string[] = [];
  const hasLatex: string[] = [];
  const notInYaml: string[] = [];

  for (const varName of variableMap.keys()) {
    const latexVarName = `${varName}_latex`;

    if (!availableVars.has(varName)) {
      notInYaml.push(varName);
    } else if (availableVars.has(latexVarName)) {
      hasLatex.push(varName);
    } else {
      missingLatex.push(varName);
    }
  }

  // Section: Variables missing LaTeX equations
  lines.push(`## Variables WITHOUT _latex Equivalents (${missingLatex.length})`);
  lines.push(`These may need LaTeX equations added to parameters.py:`);
  lines.push(``);

  if (missingLatex.length === 0) {
    lines.push(`✓ All used variables have _latex equivalents!`);
  } else {
    // Sort by usage count (most used first)
    const sortedMissing = missingLatex.sort((a, b) => {
      return (variableMap.get(b)?.length || 0) - (variableMap.get(a)?.length || 0);
    });

    for (const varName of sortedMissing) {
      const usages = variableMap.get(varName)!;
      const lineNums = usages.map((u) => u.line).join(", ");
      lines.push(`- \`${varName}\` (${usages.length} uses, lines: ${lineNums})`);
    }
  }
  lines.push(``);

  // Section: Variables WITH LaTeX equations
  lines.push(`## Variables WITH _latex Equivalents (${hasLatex.length})`);
  lines.push(`These already have LaTeX equations available:`);
  lines.push(``);

  if (hasLatex.length === 0) {
    lines.push(`(none)`);
  } else {
    for (const varName of hasLatex.sort()) {
      const usages = variableMap.get(varName)!;
      lines.push(`- \`${varName}\` → \`${varName}_latex\` (${usages.length} uses)`);
    }
  }
  lines.push(``);

  // Section: Variables not found in YAML
  if (notInYaml.length > 0) {
    lines.push(`## ⚠️ Variables NOT FOUND in _variables.yml (${notInYaml.length})`);
    lines.push(`These may be typos or undefined variables:`);
    lines.push(``);
    for (const varName of notInYaml.sort()) {
      const usages = variableMap.get(varName)!;
      const lineNums = usages.map((u) => u.line).join(", ");
      lines.push(`- \`${varName}\` (lines: ${lineNums})`);
    }
    lines.push(``);
  }

  // Section: All variables with line numbers
  lines.push(`## Complete Variable List (sorted by first usage)`);
  lines.push(``);
  lines.push(`| Variable | Uses | First Line | Has _latex |`);
  lines.push(`|----------|------|------------|------------|`);

  // Sort by first line number
  const sortedVars = Array.from(variableMap.entries()).sort((a, b) => {
    return a[1][0].line - b[1][0].line;
  });

  for (const [varName, usages] of sortedVars) {
    const latexVarName = `${varName}_latex`;
    const hasLatexFlag = availableVars.has(latexVarName) ? "✓" : "";
    const lineNums =
      usages.length > 3
        ? `${usages[0].line}, ${usages[1].line}, ${usages[2].line}...`
        : usages.map((u) => u.line).join(", ");
    lines.push(`| \`${varName}\` | ${usages.length} | ${lineNums} | ${hasLatexFlag} |`);
  }
  lines.push(``);

  // Section: Detailed usages grouped by variable
  lines.push(`## Detailed Usages (by variable)`);
  lines.push(``);

  for (const [varName, usages] of Array.from(variableMap.entries()).sort()) {
    const latexVarName = `${varName}_latex`;
    const latexStatus = availableVars.has(latexVarName)
      ? " ✓ (has _latex)"
      : " ❌ (no _latex)";
    lines.push(`### \`${varName}\`${latexStatus}`);
    lines.push(``);
    for (const usage of usages) {
      lines.push(`- Line ${usage.line}: \`${usage.context.substring(0, 80)}...\``);
    }
    lines.push(``);
  }

  return lines.join("\n");
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length < 1) {
    console.log("Usage: npx tsx scripts/extract-qmd-variables.ts <qmd-file> [output-file]");
    console.log("");
    console.log("Example:");
    console.log(
      "  npx tsx scripts/extract-qmd-variables.ts knowledge/economics/economics.qmd"
    );
    process.exit(1);
  }

  const qmdPath = args[0];
  const outputPath =
    args[1] || `_analysis/variable-usage-${path.basename(qmdPath, ".qmd")}.md`;

  // Resolve paths relative to workspace root
  const workspaceRoot = path.resolve(__dirname, "..");
  const fullQmdPath = path.isAbsolute(qmdPath)
    ? qmdPath
    : path.join(workspaceRoot, qmdPath);
  const fullOutputPath = path.isAbsolute(outputPath)
    ? outputPath
    : path.join(workspaceRoot, outputPath);

  if (!fs.existsSync(fullQmdPath)) {
    console.error(`Error: File not found: ${fullQmdPath}`);
    process.exit(1);
  }

  console.log(`Extracting variables from: ${fullQmdPath}`);

  // Load all available variables from _variables.yml files
  const availableVars = new Map<string, boolean>();

  // Try main _variables.yml
  const mainVarsPath = path.join(workspaceRoot, "_variables.yml");
  if (fs.existsSync(mainVarsPath)) {
    const vars = loadVariablesYaml(mainVarsPath);
    vars.forEach((v, k) => availableVars.set(k, v));
    console.log(`Loaded ${vars.size} variables from _variables.yml`);
  }

  // Try economics-specific variables
  const econVarsPath = path.join(workspaceRoot, "_variables-economics.yml");
  if (fs.existsSync(econVarsPath)) {
    const vars = loadVariablesYaml(econVarsPath);
    vars.forEach((v, k) => availableVars.set(k, v));
    console.log(`Loaded ${vars.size} variables from _variables-economics.yml`);
  }

  // Extract variables from QMD
  const variableMap = extractVariables(fullQmdPath);

  console.log(`Found ${variableMap.size} unique variables`);

  // Generate report
  const report = generateReport(qmdPath, variableMap, availableVars);

  // Ensure output directory exists
  const outputDir = path.dirname(fullOutputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Write report
  fs.writeFileSync(fullOutputPath, report, "utf-8");
  console.log(`Report written to: ${fullOutputPath}`);
}

main().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});
