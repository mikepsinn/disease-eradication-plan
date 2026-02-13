/**
 * Error Router
 *
 * Classifies validation errors by:
 * - Auto-fixability (can it be fixed automatically?)
 * - Tier (1: deterministic, 2: WISHONIA agents, 3: complex LLM)
 * - Confidence (how confident are we in the fix?)
 *
 * Routes errors to appropriate fixing agents based on classification.
 */

export interface ValidationError {
  source: string;
  paper: string;
  severity: string;
  type: string;
  page: number | null;
  line?: number;
  message: string;
  context?: string;
  suggested_fix?: string;
  evidence_snippet?: string;
  locator_hint?: string;
  file_path?: string;
}

export interface ErrorClassification {
  tier: 1 | 2 | 3;
  confidence: 'high' | 'medium' | 'low';
  autoFixable: boolean;
  fixStrategy: string;
  estimatedCost: number; // USD
  reasoning: string;
}

/**
 * Tier 1: Deterministic fixes (no LLM required)
 * - Pattern-based replacements
 * - File operations (download missing images)
 * - Known syntax fixes
 */
const TIER_1_PATTERNS = [
  {
    type: /QMD_FILE_LINK/i,
    confidence: 'high' as const,
    strategy: 'replace-.qmd-with-.html',
    cost: 0
  },
  {
    type: /BROKEN_LINK.*\.qmd/i,
    confidence: 'high' as const,
    strategy: 'fix-internal-link-extension',
    cost: 0
  },
  {
    type: /MISSING_IMAGE/i,
    confidence: 'medium' as const,
    strategy: 'download-from-backup',
    cost: 0
  },
  {
    type: /TRIPLE_DOLLAR/i,
    confidence: 'high' as const,
    strategy: 'fix-latex-dollar-signs',
    cost: 0
  },
  {
    type: /ESCAPED.*DOLLAR/i,
    confidence: 'high' as const,
    strategy: 'fix-escaped-math-delimiters',
    cost: 0
  }
];

/**
 * Tier 2: WISHONIA agents (cheap LLM via Gemini 2.5 Flash)
 * - Parameter validation and fixing
 * - Math equation validation
 * - Claim validation
 */
const TIER_2_PATTERNS = [
  {
    type: /PARAMETER|VARIABLE/i,
    confidence: 'high' as const,
    strategy: 'parameter-checker-agent',
    cost: 0.01
  },
  {
    type: /EQUATION|LATEX|MATH/i,
    confidence: 'medium' as const,
    strategy: 'math-validator-agent',
    cost: 0.02
  },
  {
    type: /CLAIM|CITATION/i,
    confidence: 'medium' as const,
    strategy: 'claim-validator-agent',
    cost: 0.03
  }
];

/**
 * Tier 3: Complex LLM fixes (Gemini Flash/Claude Haiku)
 * - Semantic content fixes
 * - Complex LaTeX debugging
 * - Bibliography formatting
 */
const TIER_3_PATTERNS = [
  {
    type: /LLM_EQUATION_RENDERING_DEFECT/i,
    confidence: 'medium' as const,
    strategy: 'complex-latex-fixer',
    cost: 0.15
  },
  {
    type: /LLM_MALFORMED_BIBLIOGRAPHY/i,
    confidence: 'low' as const,
    strategy: 'bibliography-fixer',
    cost: 0.20
  },
  {
    type: /LLM_BROKEN_REFERENCES/i,
    confidence: 'low' as const,
    strategy: 'reference-fixer',
    cost: 0.10
  }
];

/**
 * Classify a validation error
 */
export function classifyError(error: ValidationError): ErrorClassification {
  // Check Tier 1 (deterministic)
  for (const pattern of TIER_1_PATTERNS) {
    if (pattern.type.test(error.type)) {
      return {
        tier: 1,
        confidence: pattern.confidence,
        autoFixable: true,
        fixStrategy: pattern.strategy,
        estimatedCost: pattern.cost,
        reasoning: `Tier 1: Deterministic pattern match for ${error.type}`
      };
    }
  }

  // Check Tier 2 (WISHONIA agents)
  for (const pattern of TIER_2_PATTERNS) {
    if (pattern.type.test(error.type)) {
      return {
        tier: 2,
        confidence: pattern.confidence,
        autoFixable: true,
        fixStrategy: pattern.strategy,
        estimatedCost: pattern.cost,
        reasoning: `Tier 2: WISHONIA agent available for ${error.type}`
      };
    }
  }

  // Check Tier 3 (complex LLM)
  for (const pattern of TIER_3_PATTERNS) {
    if (pattern.type.test(error.type)) {
      return {
        tier: 3,
        confidence: pattern.confidence,
        autoFixable: pattern.confidence !== 'low', // Low confidence errors require manual review
        fixStrategy: pattern.strategy,
        estimatedCost: pattern.cost,
        reasoning: `Tier 3: Complex LLM fix for ${error.type}`
      };
    }
  }

  // Unknown error type - not auto-fixable
  return {
    tier: 3,
    confidence: 'low',
    autoFixable: false,
    fixStrategy: 'manual-review-required',
    estimatedCost: 0,
    reasoning: `Unknown error type: ${error.type} - requires manual review`
  };
}

/**
 * Batch classify multiple errors and group by tier
 */
export function classifyErrors(errors: ValidationError[]): {
  tier1: Array<{ error: ValidationError; classification: ErrorClassification }>;
  tier2: Array<{ error: ValidationError; classification: ErrorClassification }>;
  tier3: Array<{ error: ValidationError; classification: ErrorClassification }>;
  manual: Array<{ error: ValidationError; classification: ErrorClassification }>;
  totalEstimatedCost: number;
} {
  const result = {
    tier1: [] as Array<{ error: ValidationError; classification: ErrorClassification }>,
    tier2: [] as Array<{ error: ValidationError; classification: ErrorClassification }>,
    tier3: [] as Array<{ error: ValidationError; classification: ErrorClassification }>,
    manual: [] as Array<{ error: ValidationError; classification: ErrorClassification }>,
    totalEstimatedCost: 0
  };

  for (const error of errors) {
    const classification = classifyError(error);
    const item = { error, classification };

    if (!classification.autoFixable) {
      result.manual.push(item);
    } else if (classification.tier === 1) {
      result.tier1.push(item);
    } else if (classification.tier === 2) {
      result.tier2.push(item);
    } else {
      result.tier3.push(item);
    }

    result.totalEstimatedCost += classification.estimatedCost;
  }

  return result;
}

/**
 * Check if errors exceed budget
 */
export function checkBudget(
  errors: ValidationError[],
  budgetPerFix: number,
  budgetPerPaper: number,
  budgetTotal: number
): {
  withinBudget: boolean;
  estimatedCost: number;
  breakdown: {
    tier1: number;
    tier2: number;
    tier3: number;
  };
} {
  const classified = classifyErrors(errors);

  const breakdown = {
    tier1: classified.tier1.reduce((sum, item) => sum + item.classification.estimatedCost, 0),
    tier2: classified.tier2.reduce((sum, item) => sum + item.classification.estimatedCost, 0),
    tier3: classified.tier3.reduce((sum, item) => sum + item.classification.estimatedCost, 0)
  };

  const estimatedCost = breakdown.tier1 + breakdown.tier2 + breakdown.tier3;

  // Check budget constraints
  const averageCostPerFix = errors.length > 0 ? estimatedCost / errors.length : 0;
  const withinBudget =
    estimatedCost <= budgetTotal &&
    averageCostPerFix <= budgetPerFix;

  return {
    withinBudget,
    estimatedCost,
    breakdown
  };
}
