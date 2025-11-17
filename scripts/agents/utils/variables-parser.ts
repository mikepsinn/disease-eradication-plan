/**
 * Parse _variables.yml to check available parameters
 */
import { readFile } from "fs/promises";
import { load as parseYAML } from "js-yaml";
import { resolve } from "path";

export interface VariableInfo {
  name: string;
  value: string;
  hasTooltip: boolean;
  hasLink: boolean;
}

/**
 * Parse _variables.yml and return available parameter names
 */
export async function getAvailableParameters(): Promise<Set<string>> {
  try {
    const variablesPath = resolve(process.cwd(), "_variables.yml");
    const content = await readFile(variablesPath, "utf-8");
    const variables = parseYAML(content);

    return new Set(Object.keys(variables || {}));
  } catch (error) {
    console.warn("Could not parse _variables.yml:", error);
    return new Set();
  }
}

/**
 * Get detailed info about all variables
 */
export async function getVariableInfo(): Promise<Map<string, VariableInfo>> {
  try {
    const variablesPath = resolve(process.cwd(), "_variables.yml");
    const content = await readFile(variablesPath, "utf-8");
    const variables = parseYAML(content);

    const info = new Map<string, VariableInfo>();

    for (const [name, value] of Object.entries(variables || {})) {
      if (typeof value === "string") {
        info.set(name, {
          name,
          value,
          hasTooltip: value.includes('title="'),
          hasLink: value.includes('href="') || value.includes("<a "),
        });
      }
    }

    return info;
  } catch (error) {
    console.warn("Could not parse _variables.yml:", error);
    return new Map();
  }
}

/**
 * Check if a parameter exists in _variables.yml
 */
export async function parameterExists(paramName: string): Promise<boolean> {
  const params = await getAvailableParameters();
  return params.has(paramName);
}

/**
 * Suggest parameter name for a given value
 * This is a simple heuristic - the agent should use better logic
 */
export function suggestParameterName(
  value: string,
  context: string
): string | null {
  // Remove currency symbols and formatting
  const cleanValue = value.replace(/[$,]/g, "");

  // Common patterns
  if (value.includes("$") && value.includes("B")) {
    // Billions in USD
    return `some_cost_billions`;
  }

  if (value.includes("%")) {
    return `some_percentage`;
  }

  // Extract numbers
  const num = parseFloat(cleanValue);
  if (isNaN(num)) return null;

  // Use context to suggest better names
  const contextLower = context.toLowerCase();

  if (contextLower.includes("military")) {
    return `military_spending_annual`;
  }

  if (contextLower.includes("trial") || contextLower.includes("clinical")) {
    return `clinical_trial_related`;
  }

  if (contextLower.includes("dfda")) {
    return `dfda_related_metric`;
  }

  return null;
}
