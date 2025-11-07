/**
 * Central constants file for review and processing scripts
 * Ensures consistency across all scripts and prevents typos
 */

/**
 * Hash field names used in frontmatter to track when files were last processed
 * These are used to determine if a file needs reprocessing
 */
export const HASH_FIELDS = {
  // Content formatting and style
  FORMATTED: 'lastFormattedHash',
  STYLE: 'lastStyleHash',

  // Content validation
  FACT_CHECK: 'lastFactCheckHash',
  STRUCTURE_CHECK: 'lastStructureCheckHash',
  LINK_CHECK: 'lastLinkCheckHash',
  FIGURE_CHECK: 'lastFigureCheckHash',
  LATEX_CHECK: 'lastLatexCheckHash',
  PARAM_CHECK: 'lastParamCheckHash',

  // Voice and tone
  INSTRUCTIONAL_VOICE: 'lastInstructionalVoiceHash',
  TONE_ELEVATION: 'lastToneElevationHash',
  TONE_ELEVATION_WITH_HUMOR: 'lastToneElevationWithHumorHash',
} as const;

// Type for hash field values
export type HashFieldName = typeof HASH_FIELDS[keyof typeof HASH_FIELDS];

/**
 * Review check types with their associated hash fields and display names
 * Used by the main review.ts script
 */
export interface ReviewCheck {
  name: string;
  hashField: HashFieldName;
  checkFunction: (filePath: string) => Promise<void>;
}

/**
 * Default directories for different types of content
 */
export const CONTENT_DIRS = {
  BOOK: 'brain/book',
  APPENDIX: 'brain/book/appendix',
  REFERENCES: 'brain/book/references.qmd',
} as const;

/**
 * File patterns to ignore during processing
 */
export const IGNORE_PATTERNS = [
  '**/node_modules/**',
  '**/_book/**',
  '**/.quarto/**',
] as const;

/**
 * Special files that may need different processing rules
 */
export const SPECIAL_FILES = {
  REFERENCES: 'references.qmd',
  // Part introduction files that summarize their child chapters
  PART_INTROS: [
    'brain/book/problem.qmd',
    'brain/book/solution.qmd',
    'brain/book/proof.qmd',
    'brain/book/economics.qmd',
    'brain/book/futures.qmd',
    'brain/book/strategy.qmd',
  ],
} as const;

/**
 * Priority files for tone elevation (most aggressive language)
 */
export const TONE_PRIORITY_FILES = [
  'brain/book/strategy-overview.qmd',
  'brain/book/solution/war-on-disease.qmd',
  'brain/book/solution/1-percent-treaty.qmd',
  'brain/book/problem/fda-is-unsafe-and-ineffective.qmd',
  'brain/book/economics.qmd',
  'brain/book/theory.qmd',
  'brain/book/solution/aligning-incentives.qmd',
] as const;

/**
 * Common aggressive terms to transform during tone elevation
 */
export const TONE_TRANSFORMATIONS = {
  // Military/war metaphors
  'hostile takeover': 'marketplace transaction',
  'war machine': 'military apparatus',
  'weaponize': 'align incentives',
  'political kill list': 'gentle reminder to politicians that voters exist',
  'bankrupt the status quo': 'suggesting the current arrangement might not be optimal',

  // Criminal/theft framing
  'steal': 'redirect',
  'stealing': 'redirecting',
  'heist': 'reallocation',

  // Crude language
  'assholes': 'difficult people',
  'dick-measuring': 'competition',

  // Aggressive actions
  'execute the takeover': 'execute the transition',
  'crush': 'outcompete',
  'destroy': 'replace',
  'attack': 'address',
  'fight': 'work toward',

  // Superlatives
  'revolutionary': 'notable',
  'unprecedented': 'uncommon',
  'game-changing': 'significant',
} as const;

/**
 * Helper function to get all hash field values as an array
 */
export function getAllHashFields(): string[] {
  return Object.values(HASH_FIELDS);
}

/**
 * Helper function to check if a string is a valid hash field name
 */
export function isValidHashField(field: string): field is HashFieldName {
  return getAllHashFields().includes(field);
}

/**
 * Get the display name for a hash field (removes 'last' prefix and 'Hash' suffix)
 */
export function getHashFieldDisplayName(field: HashFieldName): string {
  return field
    .replace(/^last/, '')
    .replace(/Hash$/, '')
    .replace(/([A-Z])/g, ' $1')
    .trim();
}