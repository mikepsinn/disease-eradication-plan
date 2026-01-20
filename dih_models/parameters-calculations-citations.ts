// AUTO-GENERATED FILE - DO NOT EDIT
// Generated from dih_models/parameters.py
// Run: python scripts/generate-everything-parameters-variables-calculations-references.py

/**
 * Economic model parameters and calculations
 * for the 1% treaty analysis
 */

export type SourceType = 'external' | 'calculated' | 'definition';
export type Confidence = 'high' | 'medium' | 'low' | 'estimated';

/**
 * CSL JSON citation format
 * Standard format used by citation processors like citeproc-js
 * See: https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html
 */
export interface Citation {
  id: string;
  type: 'article-journal' | 'report' | 'book' | 'webpage' | 'legislation';
  title: string;
  author?: Array<{ family?: string; given?: string; literal?: string }>;
  issued?: { 'date-parts': [[number, number?, number?]] };
  publisher?: string;
  'container-title'?: string;  // Journal name
  URL?: string;
  note?: string;
}

export interface Parameter {
  /** Numeric value */
  value: number;
  /** Unit of measurement (USD, deaths, DALYs, percentage, etc.) */
  unit?: string;
  /** Human-readable description */
  description?: string;
  /** Display name for UI */
  displayName?: string;
  /** Source type: external data, calculated, or definition */
  sourceType?: SourceType;
  /** Reference ID - look up full citation in citations object */
  sourceRef?: string;
  /** Confidence level */
  confidence?: Confidence;
  /** Formula string (for calculated parameters) */
  formula?: string;
  /** LaTeX equation (for display) */
  latex?: string;
  /** 95% confidence interval [low, high] */
  confidenceInterval?: [number, number];
  /** Standard error */
  stdError?: number;
  /** Whether this is peer-reviewed data */
  peerReviewed?: boolean;
  /** Whether this is a conservative estimate */
  conservative?: boolean;
}

// ============================================================================
// External Data Sources
// ============================================================================

export const ADAPTABLE_TRIAL_COST_PER_PATIENT: Parameter = {
  value: 929.0,
  unit: "USD/patient",
  displayName: "ADAPTABLE Trial Cost per Patient",
  description: "Cost per patient in ADAPTABLE trial ($14M PCORI grant / 15,076 patients). Note: This is the direct grant cost; true cost including in-kind may be 10-40% higher.",
  sourceType: "external",
  sourceRef: "pragmatic-trials-cost-advantage",
  confidence: "medium",
  confidenceInterval: [929.0, 1400.0],
};

export const ADAPTABLE_TRIAL_TOTAL_COST: Parameter = {
  value: 14000000.0,
  unit: "USD",
  displayName: "ADAPTABLE Trial Total Cost",
  description: "PCORI grant for ADAPTABLE trial (2016-2019). Note: Direct funding only; total costs including site overhead and in-kind contributions from health systems may be higher.",
  sourceType: "external",
  sourceRef: "pragmatic-trials-cost-advantage",
  confidence: "medium",
  confidenceInterval: [14000000.0, 20000000.0],
};

export const ANTIDEPRESSANT_TRIAL_EXCLUSION_RATE: Parameter = {
  value: 0.861,
  unit: "percentage",
  displayName: "Antidepressant Trial Exclusion Rate",
  description: "Mean exclusion rate in antidepressant trials (86.1% of real-world patients excluded)",
  sourceType: "external",
  sourceRef: "antidepressant-trial-exclusion-rates",
  confidence: "high",
};

export const AVERAGE_MARKET_RETURN_PCT: Parameter = {
  value: 0.1,
  unit: "rate",
  displayName: "Average Annual Stock Market Return",
  description: "Average annual stock market return (10%)",
  sourceType: "external",
  sourceRef: "warren-buffett-career-average-return-20-pct",
  confidence: "high",
};

export const AVERAGE_US_HOURLY_WAGE: Parameter = {
  value: 30.0,
  unit: "USD/hour",
  displayName: "Average US Hourly Wage",
  description: "Average US hourly wage",
  sourceType: "external",
  sourceRef: "average-us-hourly-wage",
  confidence: "high",
};

export const BAD_POLICY_COST_US_AGRICULTURAL_SUBSIDIES: Parameter = {
  value: 75000000000.0,
  unit: "USD",
  displayName: "Agricultural Subsidies Deadweight Loss",
  description: "Deadweight loss from US agricultural subsidies. Direct subsidies ~$30B/yr but create larger distortions: overproduction, environmental damage, benefits concentrated in large farms (top 10% receive 78% of subsidies). Total welfare loss ~$75B. Textbook example of capture - very high economist consensus.",
  sourceType: "external",
  sourceRef: "ewg-farm-subsidies",
  confidence: "high",
  confidenceInterval: [50000000000.0, 120000000000.0],
  stdError: 25000000000.0,
};

export const BAD_POLICY_COST_US_DEFENSE_ABOVE_DETERRENCE: Parameter = {
  value: 400000000000.0,
  unit: "USD",
  displayName: "Defense Above Deterrence",
  description: "US defense spending above deterrence requirements. US spends ~$900B/yr on defense; many defense economists (Posen, Preble, etc.) argue $400-500B achieves equivalent deterrence given geography, nuclear arsenal, and alliance structure. Excess ~$400B/yr funds force projection, not homeland defense.",
  sourceType: "external",
  sourceRef: "posen2014",
  confidence: "medium",
  confidenceInterval: [250000000000.0, 600000000000.0],
  stdError: 120000000000.0,
};

export const BAD_POLICY_COST_US_DRUG_WAR: Parameter = {
  value: 90000000000.0,
  unit: "USD",
  displayName: "Drug War Cost",
  description: "Annual cost of drug war: ~$41B federal drug control budget, ~$10B state/local enforcement, ~$40B incarceration and lost productivity. After 50+ years and $1T+ spent, drug use is higher than ever.",
  sourceType: "external",
  sourceRef: "drugpolicyalliance2021",
  confidence: "medium",
  confidenceInterval: [60000000000.0, 150000000000.0],
  stdError: 30000000000.0,
};

export const BAD_POLICY_COST_US_FAILED_WARS: Parameter = {
  value: 400000000000.0,
  unit: "USD",
  displayName: "Failed Wars (Amortized)",
  description: "Amortized annual cost of post-9/11 wars (Iraq, Afghanistan, Syria). Total cost $8 trillion including $2.9T direct spending, $2T+ veterans care through 2050, $6.5T interest on war debt. These wars failed to achieve stated objectives.",
  sourceType: "external",
  sourceRef: "costsofwar2023",
  confidence: "medium",
  confidenceInterval: [300000000000.0, 600000000000.0],
  stdError: 100000000000.0,
};

export const BAD_POLICY_COST_US_FOSSIL_FUEL_EXPLICIT: Parameter = {
  value: 50000000000.0,
  unit: "USD",
  displayName: "Fossil Fuel Explicit Subsidies",
  description: "US explicit fossil fuel subsidies (direct payments, tax breaks). IMF estimates US total subsidies at $649B but ~92% is implicit (externalities). Explicit subsidies are roughly $50B annually.",
  sourceType: "external",
  sourceRef: "imf-fossilfuel2023",
  confidence: "medium",
  confidenceInterval: [30000000000.0, 80000000000.0],
  stdError: 15000000000.0,
};

export const BAD_POLICY_COST_US_FOSSIL_FUEL_EXTERNALITIES: Parameter = {
  value: 600000000000.0,
  unit: "USD",
  displayName: "Fossil Fuel Externalities",
  description: "US fossil fuel implicit subsidies (unpriced externalities): air pollution deaths, climate damages, congestion, accidents. IMF estimates ~$600B for US. Highly contested - depends on social cost of carbon assumptions.",
  sourceType: "external",
  sourceRef: "imf-fossilfuel2023",
  confidence: "low",
  confidenceInterval: [300000000000.0, 1000000000000.0],
  stdError: 250000000000.0,
};

export const BAD_POLICY_COST_US_HEALTHCARE_INEFFICIENCY: Parameter = {
  value: 1200000000000.0,
  unit: "USD",
  displayName: "Healthcare System Inefficiency",
  description: "US healthcare spending inefficiency. US spends ~$4.5T/yr (18% GDP) vs 9-11% in comparable OECD countries with similar/better outcomes. Papanicolas et al. (2018 JAMA) and multiple studies document $1-1.5T in excess spending from administrative complexity, high prices, and poor care coordination. Very high economist consensus.",
  sourceType: "external",
  sourceRef: "papanicolas2018",
  confidence: "high",
  confidenceInterval: [1000000000000.0, 1500000000000.0],
  stdError: 150000000000.0,
};

export const BAD_POLICY_COST_US_HOUSING_ZONING: Parameter = {
  value: 1400000000000.0,
  unit: "USD",
  displayName: "Housing/Zoning Restrictions Cost",
  description: "GDP loss from housing/zoning restrictions. Hsieh & Moretti (2019 AEJ:Macro) estimate restrictive zoning in high-productivity cities (NYC, SF, Boston) lowered aggregate US GDP by 36% from 1964-2009 by preventing workers from moving to productive locations. Annual cost ~$1.4T. Very high economist consensus across political spectrum.",
  sourceType: "external",
  sourceRef: "hsieh-moretti2019",
  confidence: "high",
  confidenceInterval: [1000000000000.0, 2000000000000.0],
  stdError: 300000000000.0,
};

export const BAD_POLICY_COST_US_INCARCERATION_EXCESS: Parameter = {
  value: 150000000000.0,
  unit: "USD",
  displayName: "Incarceration Excess Costs",
  description: "Excess costs from US over-incarceration. US incarceration rate is 5x OECD average. Direct costs ~$80B/yr, but alternative approaches (drug courts, rehabilitation, community supervision) cost less and reduce recidivism. Total excess ~$150B including lost productivity and family impacts. Growing economist consensus.",
  sourceType: "external",
  sourceRef: "vera-incarceration2024",
  confidence: "medium",
  confidenceInterval: [100000000000.0, 250000000000.0],
  stdError: 50000000000.0,
};

export const BAD_POLICY_COST_US_INFRASTRUCTURE_DISEASE: Parameter = {
  value: 150000000000.0,
  unit: "USD",
  displayName: "Infrastructure Cost Disease",
  description: "US infrastructure cost disease. US builds infrastructure at 2-5x the cost of comparable countries (subway costs, highway construction, transit projects). NYU Transit Costs Project and Brookings document systematic overruns. If US spends ~$300B/yr on infrastructure, ~50% is wasted vs best practices.",
  sourceType: "external",
  sourceRef: "transit-costs-project",
  confidence: "medium",
  confidenceInterval: [100000000000.0, 250000000000.0],
  stdError: 50000000000.0,
};

export const BAD_POLICY_COST_US_MIGRATION_RESTRICTIONS: Parameter = {
  value: 500000000000.0,
  unit: "USD",
  displayName: "Migration Restrictions Cost (US Share)",
  description: "US share of global welfare loss from migration restrictions. Clemens (2011) estimates 67-147% of GLOBAL GDP from full liberalization. US-attributable share is highly speculative - using conservative $500B estimate.",
  sourceType: "external",
  sourceRef: "clemens2011",
  confidence: "low",
  confidenceInterval: [200000000000.0, 2000000000000.0],
  stdError: 500000000000.0,
};

export const BAD_POLICY_COST_US_OCCUPATIONAL_LICENSING: Parameter = {
  value: 200000000000.0,
  unit: "USD",
  displayName: "Occupational Licensing Cost",
  description: "Cost of occupational licensing restrictions. Kleiner estimates 2-3% of GDP in welfare loss. 29% of US workers now require licenses vs 5% in 1950s. Raises prices, restricts entry, with minimal quality improvement.",
  sourceType: "external",
  sourceRef: "kleiner2013",
  confidence: "medium",
  confidenceInterval: [100000000000.0, 400000000000.0],
  stdError: 100000000000.0,
};

export const BAD_POLICY_COST_US_TARIFFS: Parameter = {
  value: 160000000000.0,
  unit: "USD",
  displayName: "Tariff Cost (GDP Loss)",
  description: "Annual GDP reduction from US tariffs and retaliation. Yale Budget Lab estimates 0.6% smaller GDP in long run, equivalent to $160B annually. Trade barriers reduce efficiency and raise consumer prices.",
  sourceType: "external",
  sourceRef: "yalebudgetlab2025",
  confidence: "medium",
  confidenceInterval: [90000000000.0, 250000000000.0],
  stdError: 50000000000.0,
};

export const BAD_POLICY_COST_US_TAX_COMPLIANCE: Parameter = {
  value: 546000000000.0,
  unit: "USD",
  displayName: "Tax Compliance Cost",
  description: "Annual cost of US tax code compliance: 7.9 billion hours of lost productivity ($413B) plus $133B in out-of-pocket costs. Equals nearly 2% of GDP. Could be largely eliminated with simplified tax code or return-free filing.",
  sourceType: "external",
  sourceRef: "taxfoundation2024-compliance",
  confidence: "high",
  confidenceInterval: [450000000000.0, 650000000000.0],
  stdError: 50000000000.0,
};

export const BASELINE_LIVES_SAVED_ANNUAL: Parameter = {
  value: 12.0,
  unit: "deaths/year",
  displayName: "Baseline Annual Lives Saved by Pharmaceuticals",
  description: "Baseline annual lives saved by pharmaceuticals (conservative aggregate)",
  sourceType: "external",
  sourceRef: "who-global-health-estimates-2024",
  confidence: "medium",
  peerReviewed: true,
  conservative: true,
};

export const BED_NETS_COST_PER_DALY: Parameter = {
  value: 89.0,
  unit: "USD/DALY",
  displayName: "Bed Nets Cost per DALY",
  description: "GiveWell cost per DALY for insecticide-treated bed nets (midpoint estimate, range $78-100). DALYs (Disability-Adjusted Life Years) measure disease burden by combining years of life lost and years lived with disability. Bed nets prevent malaria deaths and are considered a gold standard benchmark for cost-effective global health interventions - if an intervention costs less per DALY than bed nets, it's exceptionally cost-effective. GiveWell synthesizes peer-reviewed academic research with transparent, rigorous methodology and extensive external expert review.",
  sourceType: "external",
  sourceRef: "givewell-cost-per-life-saved",
  confidence: "high",
  confidenceInterval: [78.0, 100.0],
  peerReviewed: true,
};

export const BOOK_READING_SPEED_WPM: Parameter = {
  value: 200.0,
  unit: "words/minute",
  displayName: "Average Reading Speed",
  description: "Average reading speed (conservative for non-fiction)",
  sourceType: "external",
  sourceRef: "average-reading-speed",
  confidence: "high",
};

export const CAREGIVER_ANNUAL_VALUE_TOTAL: Parameter = {
  value: 600000000000.0,
  unit: "USD/year",
  displayName: "Total Annual Value of Unpaid Caregiving in US",
  description: "Total annual value of unpaid caregiving in US",
  sourceType: "external",
  sourceRef: "unpaid-caregiver-hours-economic-value",
  confidence: "high",
};

export const CAREGIVER_COUNT_US: Parameter = {
  value: 38000000.0,
  unit: "people",
  displayName: "Number of Unpaid Caregivers in US",
  description: "Number of unpaid caregivers in US",
  sourceType: "external",
  sourceRef: "unpaid-caregiver-hours-economic-value",
  confidence: "high",
};

export const CAREGIVER_HOURS_PER_MONTH: Parameter = {
  value: 20.0,
  unit: "hours/month",
  displayName: "Average Monthly Hours of Unpaid Family Caregiving in US",
  description: "Average monthly hours of unpaid family caregiving in US",
  sourceType: "external",
  sourceRef: "unpaid-caregiver-hours-economic-value",
  confidence: "high",
};

export const CAREGIVER_VALUE_PER_HOUR_SIMPLE: Parameter = {
  value: 25.0,
  unit: "USD/hour",
  displayName: "Estimated Replacement Cost per Hour of Caregiving",
  description: "Estimated replacement cost per hour of caregiving",
  sourceType: "external",
  sourceRef: "unpaid-caregiver-hours-economic-value",
  confidence: "high",
};

export const CHILDHOOD_VACCINATION_ANNUAL_BENEFIT: Parameter = {
  value: 15000000000.0,
  unit: "USD/year",
  displayName: "Estimated Annual Global Economic Benefit from Childhood Vaccination Programs",
  description: "Estimated annual global economic benefit from childhood vaccination programs (measles, polio, etc.)",
  sourceType: "external",
  sourceRef: "childhood-vaccination-economic-benefits",
  confidence: "high",
  stdError: 4500000000.0,
};

export const CHILDHOOD_VACCINATION_ROI: Parameter = {
  value: 13.0,
  unit: "ratio",
  displayName: "Return on Investment from Childhood Vaccination Programs",
  description: "Return on investment from childhood vaccination programs",
  sourceType: "external",
  sourceRef: "childhood-vaccination-roi",
  confidence: "high",
};

export const CHRONIC_DISEASE_DISABILITY_WEIGHT: Parameter = {
  value: 0.35,
  unit: "weight",
  displayName: "Disability Weight for Untreated Chronic Conditions",
  description: "Disability weight for untreated chronic conditions (WHO Global Burden of Disease)",
  sourceType: "external",
  sourceRef: "who-global-health-estimates-2024",
  confidence: "medium",
  stdError: 0.07,
  peerReviewed: true,
};

export const CPI_MULTIPLIER_1980_TO_2024: Parameter = {
  value: 3.8,
  unit: "ratio",
  displayName: "CPI Multiplier: 1980 to 2024",
  description: "CPI inflation multiplier from 1980 to 2024 (280.48% cumulative inflation)",
  sourceType: "external",
  sourceRef: "bls-cpi-inflation-calculator",
  confidence: "high",
  confidenceInterval: [3.75, 3.85],
};

export const CRONY_TAX_PCT: Parameter = {
  value: 0.1,
  unit: "percent",
  displayName: "Crony Tax (Capture)",
  description: "Welfare loss from regulatory capture and crony rent-seeking as percentage of potential GDP. Based on Del Rosal (2011) survey of empirical estimates ranging 0.2% to 23.7% of GDP. Central estimate 10% is conservative midpoint; Laband & Sophocleus (1988) estimated up to 45%.",
  sourceType: "external",
  sourceRef: "delrosal2011",
  confidence: "medium",
  confidenceInterval: [0.05, 0.2],
  stdError: 0.05,
};

export const CURRENT_ACTIVE_TRIALS: Parameter = {
  value: 10000.0,
  unit: "trials",
  displayName: "Current Active Trials at Any Given Time",
  description: "Current active trials at any given time (3-5 year duration)",
  sourceType: "external",
  sourceRef: "clinicaltrials-gov-enrollment-data-2025",
  confidence: "high",
};

export const CURRENT_CLINICAL_TRIAL_PARTICIPATION_RATE: Parameter = {
  value: 0.0006,
  unit: "rate",
  displayName: "Current Clinical Trial Participation Rate",
  description: "Current clinical trial participation rate (0.06% of population)",
  sourceType: "external",
  sourceRef: "clinical-trial-patient-participation-rate",
  confidence: "high",
};

export const CURRENT_DISEASE_PATIENTS_GLOBAL: Parameter = {
  value: 2400000000.0,
  unit: "people",
  displayName: "Global Population with Chronic Diseases",
  description: "Global population with chronic diseases",
  sourceType: "external",
  sourceRef: "disease-prevalence-2-billion",
  confidence: "high",
  confidenceInterval: [2000000000.0, 2800000000.0],
};

export const CURRENT_DRUG_APPROVALS_PER_YEAR: Parameter = {
  value: 50.0,
  unit: "drugs/year",
  displayName: "Average Annual New Drug Approvals Globally",
  description: "Average annual new drug approvals globally",
  sourceType: "external",
  sourceRef: "global-new-drug-approvals-50-annually",
  confidence: "high",
  confidenceInterval: [45.0, 60.0],
};

export const CURRENT_TRIALS_PER_YEAR: Parameter = {
  value: 3300.0,
  unit: "trials/year",
  displayName: "Current Global Clinical Trials per Year",
  description: "Current global clinical trials per year",
  sourceType: "external",
  sourceRef: "global-clinical-trials-market-2024",
  confidence: "high",
  confidenceInterval: [2640.0, 3960.0],
};

export const CURRENT_TRIAL_ABANDONMENT_RATE: Parameter = {
  value: 0.4,
  unit: "rate",
  displayName: "Current Trial Abandonment Rate",
  description: "Current trial abandonment rate (40% never complete)",
  sourceType: "external",
  sourceRef: "clinical-trial-abandonment-rate",
  confidence: "high",
};

export const CURRENT_TRIAL_SLOTS_AVAILABLE: Parameter = {
  value: 1900000.0,
  unit: "patients/year",
  displayName: "Annual Global Clinical Trial Participants",
  description: "Annual global clinical trial participants (IQVIA 2022: 1.9M post-COVID normalization)",
  sourceType: "external",
  sourceRef: "global-trial-participant-capacity",
  confidence: "high",
  confidenceInterval: [1500000.0, 2300000.0],
};

export const DEFENSE_LOBBYING_ANNUAL: Parameter = {
  value: 127000000.0,
  unit: "USD/year",
  displayName: "Annual Defense Industry Lobbying Spending",
  description: "Annual defense industry lobbying spending",
  sourceType: "external",
  sourceRef: "lobbying-spend-defense",
  confidence: "high",
  peerReviewed: true,
};

export const DEWORMING_COST_PER_DALY: Parameter = {
  value: 55.0,
  unit: "USD/DALY",
  displayName: "Deworming Cost per DALY",
  description: "Cost per DALY for deworming programs (range $28-82, midpoint estimate). GiveWell notes this 2011 estimate is outdated and their current methodology focuses on long-term income effects rather than short-term health DALYs.",
  sourceType: "external",
  sourceRef: "deworming-cost-per-daly",
  confidence: "low",
};

export const DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT: Parameter = {
  value: 929.0,
  unit: "USD/patient",
  displayName: "dFDA Pragmatic Trial Cost per Patient",
  description: "dFDA pragmatic trial cost per patient. Uses ADAPTABLE trial ($929) as DELIBERATELY CONSERVATIVE central estimate. Harvard meta-analysis of 108 trials found median of only $97/patient - our estimate may overstate costs by 10x. Confidence interval spans meta-analysis median to complex chronic disease trials.",
  sourceType: "external",
  sourceRef: "pragmatic-trials-cost-advantage",
  confidence: "medium",
  confidenceInterval: [97.0, 3000.0],
};

export const DRUG_DEVELOPMENT_COST_1980S: Parameter = {
  value: 194000000.0,
  unit: "USD",
  displayName: "Drug Development Cost (1980s)",
  description: "Drug development cost in 1980s (compounded to approval, 1990 dollars)",
  sourceType: "external",
  sourceRef: "pre-1962-drug-costs-timeline",
  confidence: "high",
  confidenceInterval: [145500000.0, 242500000.0],
};

export const DRUG_REPURPOSING_SUCCESS_RATE: Parameter = {
  value: 0.3,
  unit: "percentage",
  displayName: "Drug Repurposing Success Rate",
  description: "Percentage of drugs that gain at least one new indication after initial approval",
  sourceType: "external",
  sourceRef: "drug-repurposing-rate",
  confidence: "high",
};

export const ECONOMIC_MULTIPLIER_EDUCATION_INVESTMENT: Parameter = {
  value: 2.1,
  unit: "ratio",
  displayName: "Economic Multiplier for Education Investment",
  description: "Economic multiplier for education investment (2.1x ROI)",
  sourceType: "external",
  sourceRef: "education-investment-economic-multiplier",
  confidence: "high",
};

export const ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT: Parameter = {
  value: 4.3,
  unit: "ratio",
  displayName: "Economic Multiplier for Healthcare Investment",
  description: "Economic multiplier for healthcare investment (4.3x ROI)",
  sourceType: "external",
  sourceRef: "healthcare-investment-economic-multiplier",
  confidence: "high",
};

export const ECONOMIC_MULTIPLIER_INFRASTRUCTURE_INVESTMENT: Parameter = {
  value: 1.6,
  unit: "ratio",
  displayName: "Economic Multiplier for Infrastructure Investment",
  description: "Economic multiplier for infrastructure investment (1.6x ROI)",
  sourceType: "external",
  sourceRef: "infrastructure-investment-economic-multiplier",
  confidence: "high",
};

export const ECONOMIC_MULTIPLIER_MILITARY_SPENDING: Parameter = {
  value: 0.6,
  unit: "ratio",
  displayName: "Economic Multiplier for Military Spending",
  description: "Economic multiplier for military spending (0.6x ROI)",
  sourceType: "external",
  sourceRef: "military-spending-economic-multiplier",
  confidence: "high",
};

export const EFFICACY_LAG_YEARS: Parameter = {
  value: 8.2,
  unit: "years",
  displayName: "Regulatory Delay for Efficacy Testing Post-Safety Verification",
  description: "Regulatory delay for efficacy testing (Phase II/III) post-safety verification. Based on BIO 2021 industry survey. Note: This is for drugs that COMPLETE the pipeline - survivor bias means actual delay for any given disease may be longer if candidates fail and must restart.",
  sourceType: "external",
  sourceRef: "bio-clinical-development-2021",
  confidence: "medium",
  formula: "TOTAL_TIME_TO_MARKET - PHASE_1_DURATION",
  stdError: 2.0,
  peerReviewed: true,
};

export const FDA_APPROVED_PRODUCTS_COUNT: Parameter = {
  value: 20000.0,
  unit: "products",
  displayName: "FDA-Approved Drug Products",
  description: "Total FDA-approved drug products in the U.S.",
  sourceType: "external",
  sourceRef: "fda-approved-products-20k",
  confidence: "high",
};

export const FDA_APPROVED_UNIQUE_ACTIVE_INGREDIENTS: Parameter = {
  value: 1650.0,
  unit: "compounds",
  displayName: "FDA-Approved Unique Active Ingredients",
  description: "Unique active pharmaceutical ingredients in FDA-approved products (midpoint of 1,300-2,000 range)",
  sourceType: "external",
  sourceRef: "fda-approved-products-20k",
  confidence: "high",
  confidenceInterval: [1300.0, 2000.0],
};

export const FDA_GRAS_SUBSTANCES_COUNT: Parameter = {
  value: 635.0,
  unit: "substances",
  displayName: "FDA GRAS Substances",
  description: "FDA Generally Recognized as Safe (GRAS) substances (midpoint of 570-700 range)",
  sourceType: "external",
  sourceRef: "fda-gras-list-count",
  confidence: "high",
  confidenceInterval: [570.0, 700.0],
};

export const FDA_PHASE_1_TO_APPROVAL_YEARS: Parameter = {
  value: 9.1,
  unit: "years",
  displayName: "FDA Phase 1 to Approval Timeline",
  description: "FDA timeline from Phase 1 start to approval (Phase 1-3 + NDA review)",
  sourceType: "external",
  sourceRef: "fda-approval-timeline-10-years",
  confidence: "high",
  confidenceInterval: [6.0, 12.0],
  stdError: 2.0,
};

export const GIVEWELL_COST_PER_LIFE_AVG: Parameter = {
  value: 4500.0,
  unit: "USD/life",
  displayName: "Givewell Average Cost per Life Saved Across Top Charities",
  description: "GiveWell average cost per life saved across top charities",
  sourceType: "external",
  sourceRef: "givewell-cost-per-life-saved",
  confidence: "high",
};

export const GIVEWELL_COST_PER_LIFE_MAX: Parameter = {
  value: 5500.0,
  unit: "USD/life",
  displayName: "Givewell Cost per Life Saved (Maximum)",
  description: "GiveWell cost per life saved (Against Malaria Foundation)",
  sourceType: "external",
  sourceRef: "givewell-cost-per-life-saved",
  confidence: "high",
};

export const GIVEWELL_COST_PER_LIFE_MIN: Parameter = {
  value: 3500.0,
  unit: "USD/life",
  displayName: "Givewell Cost per Life Saved (Minimum)",
  description: "GiveWell cost per life saved (Helen Keller International)",
  sourceType: "external",
  sourceRef: "givewell-cost-per-life-saved",
  confidence: "high",
};

export const GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT: Parameter = {
  value: 233600.0,
  unit: "deaths/year",
  displayName: "Annual Deaths from Active Combat Worldwide",
  description: "Annual deaths from active combat worldwide",
  sourceType: "external",
  sourceRef: "acled-active-combat-deaths",
  confidence: "high",
  confidenceInterval: [180000.0, 300000.0],
};

export const GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE: Parameter = {
  value: 2700.0,
  unit: "deaths/year",
  displayName: "Annual Deaths from State Violence",
  description: "Annual deaths from state violence",
  sourceType: "external",
  sourceRef: "ucdp-state-violence-deaths",
  confidence: "high",
  confidenceInterval: [1500.0, 5000.0],
};

export const GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS: Parameter = {
  value: 8300.0,
  unit: "deaths/year",
  displayName: "Annual Deaths from Terror Attacks Globally",
  description: "Annual deaths from terror attacks globally",
  sourceType: "external",
  sourceRef: "gtd-terror-attack-deaths",
  confidence: "high",
  confidenceInterval: [6000.0, 12000.0],
};

export const GLOBAL_ANNUAL_DALY_BURDEN: Parameter = {
  value: 2880000000.0,
  unit: "DALYs/year",
  displayName: "Global Annual DALY Burden",
  description: "Global annual DALY burden from all diseases and injuries (WHO/IHME Global Burden of Disease 2021). Includes both YLL (years of life lost) and YLD (years lived with disability) from all causes.",
  sourceType: "external",
  sourceRef: "ihme-gbd-2021",
  confidence: "high",
  stdError: 150000000.0,
  peerReviewed: true,
};

export const GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES: Parameter = {
  value: 55000000.0,
  unit: "deaths/year",
  displayName: "Annual Deaths from All Diseases and Aging Globally",
  description: "Annual deaths from all diseases and aging globally",
  sourceType: "external",
  sourceRef: "who-global-health-estimates-2024",
  confidence: "high",
  stdError: 5000000.0,
};

export const GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT: Parameter = {
  value: 100000000000.0,
  unit: "USD",
  displayName: "Annual Environmental Damage and Restoration Costs from Conflict",
  description: "Annual environmental damage and restoration costs from conflict",
  sourceType: "external",
  sourceRef: "environmental-cost-of-war",
  confidence: "high",
  confidenceInterval: [70000000000.0, 140000000000.0],
};

export const GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT: Parameter = {
  value: 298100000000.0,
  unit: "USD",
  displayName: "Annual Infrastructure Damage to Communications from Conflict",
  description: "Annual infrastructure damage to communications from conflict",
  sourceType: "external",
  sourceRef: "environmental-cost-of-war",
  confidence: "high",
  confidenceInterval: [209000000000.0, 418000000000.0],
};

export const GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT: Parameter = {
  value: 234500000000.0,
  unit: "USD",
  displayName: "Annual Infrastructure Damage to Education Facilities from Conflict",
  description: "Annual infrastructure damage to education facilities from conflict",
  sourceType: "external",
  sourceRef: "environmental-cost-of-war",
  confidence: "high",
  confidenceInterval: [164000000000.0, 328000000000.0],
};

export const GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT: Parameter = {
  value: 421700000000.0,
  unit: "USD",
  displayName: "Annual Infrastructure Damage to Energy Systems from Conflict",
  description: "Annual infrastructure damage to energy systems from conflict",
  sourceType: "external",
  sourceRef: "environmental-cost-of-war",
  confidence: "high",
  confidenceInterval: [295000000000.0, 590000000000.0],
};

export const GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT: Parameter = {
  value: 165600000000.0,
  unit: "USD",
  displayName: "Annual Infrastructure Damage to Healthcare Facilities from Conflict",
  description: "Annual infrastructure damage to healthcare facilities from conflict",
  sourceType: "external",
  sourceRef: "environmental-cost-of-war",
  confidence: "high",
  confidenceInterval: [116000000000.0, 232000000000.0],
};

export const GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT: Parameter = {
  value: 487300000000.0,
  unit: "USD",
  displayName: "Annual Infrastructure Damage to Transportation from Conflict",
  description: "Annual infrastructure damage to transportation from conflict",
  sourceType: "external",
  sourceRef: "environmental-cost-of-war",
  confidence: "high",
  confidenceInterval: [340000000000.0, 680000000000.0],
};

export const GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT: Parameter = {
  value: 267800000000.0,
  unit: "USD",
  displayName: "Annual Infrastructure Damage to Water Systems from Conflict",
  description: "Annual infrastructure damage to water systems from conflict",
  sourceType: "external",
  sourceRef: "environmental-cost-of-war",
  confidence: "high",
  confidenceInterval: [187000000000.0, 375000000000.0],
};

export const GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH: Parameter = {
  value: 4200000.0,
  unit: "lives/year",
  displayName: "Annual Lives Saved by Medical Research Globally",
  description: "Annual lives saved by medical research globally",
  sourceType: "external",
  sourceRef: "medical-research-lives-saved-annually",
  confidence: "high",
  confidenceInterval: [3000000.0, 6000000.0],
};

export const GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING: Parameter = {
  value: 2718000000000.0,
  unit: "USD",
  displayName: "Annual Lost Economic Growth from Military Spending Opportunity Cost",
  description: "Annual lost economic growth from military spending opportunity cost",
  sourceType: "external",
  sourceRef: "disparity-ratio-weapons-vs-cures",
  confidence: "high",
  confidenceInterval: [1900000000000.0, 3800000000000.0],
};

export const GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT: Parameter = {
  value: 300000000000.0,
  unit: "USD",
  displayName: "Annual Lost Productivity from Conflict Casualties",
  description: "Annual lost productivity from conflict casualties",
  sourceType: "external",
  sourceRef: "lost-human-capital-war-cost",
  confidence: "high",
  confidenceInterval: [210000000000.0, 420000000000.0],
};

export const GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT: Parameter = {
  value: 232000000000.0,
  unit: "USD",
  displayName: "Annual PTSD and Mental Health Costs from Conflict",
  description: "Annual PTSD and mental health costs from conflict",
  sourceType: "external",
  sourceRef: "psychological-impact-war-cost",
  confidence: "high",
  confidenceInterval: [162000000000.0, 325000000000.0],
};

export const GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS: Parameter = {
  value: 150000000000.0,
  unit: "USD",
  displayName: "Annual Refugee Support Costs",
  description: "Annual refugee support costs (108.4M refugees × $1,384/year)",
  sourceType: "external",
  sourceRef: "unhcr-refugee-support-cost",
  confidence: "high",
  confidenceInterval: [105000000000.0, 210000000000.0],
};

export const GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT: Parameter = {
  value: 57400000000.0,
  unit: "USD",
  displayName: "Annual Trade Disruption Costs from Currency Instability",
  description: "Annual trade disruption costs from currency instability",
  sourceType: "external",
  sourceRef: "world-bank-trade-disruption-conflict",
  confidence: "high",
  confidenceInterval: [40000000000.0, 80000000000.0],
};

export const GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT: Parameter = {
  value: 124700000000.0,
  unit: "USD",
  displayName: "Annual Trade Disruption Costs from Energy Price Volatility",
  description: "Annual trade disruption costs from energy price volatility",
  sourceType: "external",
  sourceRef: "world-bank-trade-disruption-conflict",
  confidence: "high",
  confidenceInterval: [87000000000.0, 175000000000.0],
};

export const GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT: Parameter = {
  value: 247100000000.0,
  unit: "USD",
  displayName: "Annual Trade Disruption Costs from Shipping Disruptions",
  description: "Annual trade disruption costs from shipping disruptions",
  sourceType: "external",
  sourceRef: "world-bank-trade-disruption-conflict",
  confidence: "high",
  confidenceInterval: [173000000000.0, 346000000000.0],
};

export const GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT: Parameter = {
  value: 186800000000.0,
  unit: "USD",
  displayName: "Annual Trade Disruption Costs from Supply Chain Disruptions",
  description: "Annual trade disruption costs from supply chain disruptions",
  sourceType: "external",
  sourceRef: "world-bank-trade-disruption-conflict",
  confidence: "high",
  confidenceInterval: [131000000000.0, 262000000000.0],
};

export const GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS: Parameter = {
  value: 200100000000.0,
  unit: "USD",
  displayName: "Annual Veteran Healthcare Costs",
  description: "Annual veteran healthcare costs (20-year projected)",
  sourceType: "external",
  sourceRef: "veteran-healthcare-cost-projections",
  confidence: "high",
  confidenceInterval: [140000000000.0, 280000000000.0],
};

export const GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL: Parameter = {
  value: 60000000000.0,
  unit: "USD",
  displayName: "Annual Global Spending on Clinical Trials",
  description: "Annual global spending on clinical trials (Industry: $45-60B + Government: $3-6B + Nonprofits: $2-5B). Conservative estimate using 15-20% of $300B total pharma R&D, not inflated market size projections.",
  sourceType: "external",
  sourceRef: "industry-clinical-trial-spending-estimate",
  confidence: "high",
  confidenceInterval: [50000000000.0, 75000000000.0],
  stdError: 10000000000.0,
};

export const GLOBAL_DISEASE_DEATHS_DAILY: Parameter = {
  value: 150000.0,
  unit: "deaths/day",
  displayName: "Global Daily Deaths from Disease and Aging",
  description: "Total global deaths per day from all disease and aging (WHO Global Burden of Disease 2024)",
  sourceType: "external",
  sourceRef: "who-global-health-estimates-2024",
  confidence: "high",
  stdError: 7500.0,
  peerReviewed: true,
};

export const GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL: Parameter = {
  value: 9900000000000.0,
  unit: "USD/year",
  displayName: "Global Annual Direct Medical Costs of Disease",
  description: "Direct medical costs of disease globally (treatment, hospitalization, medication)",
  sourceType: "external",
  sourceRef: "disease-economic-burden-109t",
  confidence: "high",
  confidenceInterval: [7000000000000.0, 14000000000000.0],
};

export const GLOBAL_DISEASE_HUMAN_LIFE_VALUE_LOSS_ANNUAL: Parameter = {
  value: 94200000000000.0,
  unit: "USD/year",
  displayName: "Global Annual Economic Value of Human Life Lost to Disease",
  description: "Economic value of human life lost to disease annually (mortality valuation)",
  sourceType: "external",
  sourceRef: "disease-economic-burden-109t",
  confidence: "high",
  confidenceInterval: [66000000000000.0, 132000000000000.0],
};

export const GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL: Parameter = {
  value: 5000000000000.0,
  unit: "USD/year",
  displayName: "Global Annual Productivity Loss from Disease",
  description: "Annual productivity loss from disease globally (absenteeism, reduced output)",
  sourceType: "external",
  sourceRef: "disease-economic-burden-109t",
  confidence: "high",
  confidenceInterval: [3500000000000.0, 7000000000000.0],
};

export const GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL: Parameter = {
  value: 4500000000.0,
  unit: "USD",
  displayName: "Annual Global Government Spending on Clinical Trials",
  description: "Annual global government spending on interventional clinical trials (~5-10% of total)",
  sourceType: "external",
  sourceRef: "global-government-clinical-trial-spending-estimate",
  confidence: "high",
  confidenceInterval: [3000000000.0, 6000000000.0],
  stdError: 1000000000.0,
};

export const GLOBAL_HOUSEHOLD_WEALTH_USD: Parameter = {
  value: 454000000000000.0,
  unit: "USD",
  displayName: "Global Household Wealth",
  description: "Total global household wealth (2022/2023 estimate)",
  sourceType: "external",
  sourceRef: "cs-global-wealth-report-2023",
  confidence: "high",
};

export const GLOBAL_LIFE_EXPECTANCY_2024: Parameter = {
  value: 79.0,
  unit: "years",
  displayName: "Global Life Expectancy (2024)",
  description: "Global life expectancy (2024)",
  sourceType: "external",
  sourceRef: "who-global-health-estimates-2024",
  confidence: "high",
  stdError: 2.0,
  peerReviewed: true,
};

export const GLOBAL_MED_RESEARCH_SPENDING: Parameter = {
  value: 67500000000.0,
  unit: "USD",
  displayName: "Global Government Medical Research Spending",
  description: "Global government medical research spending",
  sourceType: "external",
  sourceRef: "global-gov-med-research-spending",
  confidence: "high",
  confidenceInterval: [54000000000.0, 81000000000.0],
};

export const GLOBAL_MILITARY_SPENDING_ANNUAL_2024: Parameter = {
  value: 2720000000000.0,
  unit: "USD",
  displayName: "Global Military Spending in 2024",
  description: "Global military spending in 2024",
  sourceType: "external",
  sourceRef: "global-military-spending",
  confidence: "high",
};

export const GLOBAL_NONPROFIT_CLINICAL_TRIALS_SPENDING_ANNUAL: Parameter = {
  value: 3500000000.0,
  unit: "USD",
  displayName: "Annual Global Nonprofit Spending on Clinical Trials",
  description: "Annual global nonprofit spending on clinical trials (foundations, disease advocacy groups)",
  sourceType: "external",
  sourceRef: "nonprofit-clinical-trial-spending-estimate",
  confidence: "high",
  confidenceInterval: [2000000000.0, 5000000000.0],
};

export const GLOBAL_PHARMA_RD_SPENDING_ANNUAL: Parameter = {
  value: 300000000000.0,
  unit: "USD",
  displayName: "Annual Global Pharmaceutical R&D Spending",
  description: "Total global pharmaceutical R&D spending ($300B annually, clinical trials represent 15-20% of this total)",
  sourceType: "external",
  sourceRef: "global-pharma-rd-spending-300b",
  confidence: "high",
};

export const GLOBAL_POPULATION_2024: Parameter = {
  value: 8000000000.0,
  unit: "of people",
  displayName: "Global Population in 2024",
  description: "Global population in 2024",
  sourceType: "external",
  sourceRef: "global-population-8-billion",
  confidence: "high",
  confidenceInterval: [7800000000.0, 8200000000.0],
};

export const GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT: Parameter = {
  value: 0.035,
  unit: "rate",
  displayName: "Critical Mass Threshold for Social Change",
  description: "Critical mass threshold for social change (3.5% rule)",
  sourceType: "external",
  sourceRef: "3-5-rule",
  confidence: "high",
  confidenceInterval: [0.025, 0.045],
};

export const GLOBAL_SYMPTOMATIC_DISEASE_TREATMENT_ANNUAL: Parameter = {
  value: 8200000000000.0,
  unit: "USD/year",
  displayName: "Annual Global Spending on Symptomatic Disease Treatment",
  description: "Annual global spending on symptomatic disease treatment",
  sourceType: "external",
  sourceRef: "disease-economic-burden-109t",
  confidence: "high",
  confidenceInterval: [6500000000000.0, 10000000000000.0],
};

export const GLOBAL_YLD_PROPORTION_OF_DALYS: Parameter = {
  value: 0.39,
  unit: "proportion",
  displayName: "YLD Proportion of Total DALYs",
  description: "Proportion of global DALYs that are YLD (years lived with disability) vs YLL (years of life lost). From GBD 2021: 1.13B YLD out of 2.88B total DALYs = 39%.",
  sourceType: "external",
  sourceRef: "ihme-gbd-2021",
  confidence: "high",
  stdError: 0.03,
  peerReviewed: true,
};

export const HUMAN_GENOME_PROJECT_TOTAL_ECONOMIC_IMPACT: Parameter = {
  value: 1000000000000.0,
  unit: "USD",
  displayName: "Estimated Total Economic Impact of Human Genome Project",
  description: "Estimated total economic impact of Human Genome Project",
  sourceType: "external",
  sourceRef: "human-genome-and-genetic-editing",
  confidence: "high",
};

export const HUMAN_INTERACTOME_TARGETED_PCT: Parameter = {
  value: 0.12,
  unit: "percentage",
  displayName: "Human Interactome Targeted by Drugs",
  description: "Percentage of human interactome (protein-protein interactions) targeted by drugs",
  sourceType: "external",
  sourceRef: "clinical-trials-puzzle-interactome",
  confidence: "high",
};

export const ICD_10_TOTAL_CODES: Parameter = {
  value: 14000.0,
  unit: "codes",
  displayName: "ICD-10 Total Codes",
  description: "Total ICD-10 diagnostic codes for human diseases and conditions",
  sourceType: "external",
  sourceRef: "icd-10-code-count",
  confidence: "high",
};

export const LIFE_EXTENSION_YEARS: Parameter = {
  value: 20.0,
  unit: "years",
  displayName: "Life Extension from Treaty Research Acceleration",
  description: "Expected years of life extension from 1% treaty research acceleration (25x trial capacity). Bounds: 0 (complete failure) to ~150 (accident-limited lifespan minus current). Lognormal distribution allows for breakthrough scenarios.",
  sourceType: "external",
  sourceRef: "longevity-escape-velocity",
  confidence: "low",
  confidenceInterval: [5.0, 100.0],
};

export const LOBBYIST_SALARY_MAX: Parameter = {
  value: 2000000.0,
  unit: "USD",
  displayName: "Maximum Annual Lobbyist Salary Range",
  description: "Maximum annual lobbyist salary range",
  sourceType: "external",
  sourceRef: "lobbyist-statistics-dc",
  confidence: "high",
};

export const LOBBYIST_SALARY_MIN_K: Parameter = {
  value: 500000.0,
  unit: "USD",
  displayName: "Minimum Annual Lobbyist Salary Range",
  description: "Minimum annual lobbyist salary range",
  sourceType: "external",
  sourceRef: "lobbyist-statistics-dc",
  confidence: "high",
};

export const MEASLES_VACCINATION_ROI: Parameter = {
  value: 14.0,
  unit: "ratio",
  displayName: "Return on Investment from Measles Vaccination Programs",
  description: "Return on investment from measles (MMR) vaccination programs",
  sourceType: "external",
  sourceRef: "measles-vaccination-roi",
  confidence: "high",
};

export const MENTAL_HEALTH_PRODUCTIVITY_LOSS_PER_CAPITA: Parameter = {
  value: 2000.0,
  unit: "USD/year",
  displayName: "Annual Productivity Loss per Capita from Mental Health Issues",
  description: "Annual productivity loss per capita from mental health issues (beyond treatment costs)",
  sourceType: "external",
  sourceRef: "mental-health-burden",
  confidence: "high",
};

export const NATO_DEFENSE_SPENDING_ANNUAL: Parameter = {
  value: 1506000000000.0,
  unit: "USD",
  displayName: "NATO Defense Spending (2024)",
  description: "Total NATO member defense spending in 2024. Source: SIPRI.",
  sourceType: "external",
  sourceRef: "sipri2024",
  confidence: "high",
};

export const NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR: Parameter = {
  value: 15.0,
  unit: "diseases/year",
  displayName: "Diseases Getting First Treatment Per Year",
  description: "Number of diseases that receive their FIRST effective treatment each year under current system. ~9 rare diseases/year (based on 40 years of ODA: 350 with treatment ÷ 40 years), plus ~5-10 common diseases. Note: FDA approves ~50 drugs/year, but most are for diseases that already have treatments.",
  sourceType: "external",
  sourceRef: "diseases-getting-first-treatment-annually",
  confidence: "low",
  confidenceInterval: [8.0, 30.0],
};

export const NIH_ANNUAL_BUDGET: Parameter = {
  value: 47000000000.0,
  unit: "USD",
  displayName: "NIH Annual Budget",
  description: "NIH annual budget (FY2024/2025)",
  sourceType: "external",
  sourceRef: "nih-budget-fy2025",
  confidence: "high",
  confidenceInterval: [45000000000.0, 50000000000.0],
};

export const NIH_CLINICAL_TRIALS_SPENDING_PCT: Parameter = {
  value: 0.033,
  unit: "percentage",
  displayName: "NIH Clinical Trials Spending Percentage",
  description: "Percentage of NIH budget spent on clinical trials (3.3%)",
  sourceType: "external",
  sourceRef: "nih-clinical-trials-spending-pct-3-3",
  confidence: "high",
  confidenceInterval: [0.02, 0.05],
};

export const NIH_STANDARD_RESEARCH_COST_PER_QALY: Parameter = {
  value: 50000.0,
  unit: "USD/QALY",
  displayName: "NIH Standard Research Cost per QALY",
  description: "Typical cost per QALY for standard NIH-funded medical research portfolio. Reflects the inefficiency of traditional RCTs and basic research-heavy allocation. See confidence_interval for range; ICER uses higher thresholds for value-based pricing.",
  sourceType: "external",
  sourceRef: "standard-medical-research-roi",
  confidence: "medium",
  confidenceInterval: [20000.0, 100000.0],
};

export const OXFORD_RECOVERY_TRIAL_DURATION_MONTHS: Parameter = {
  value: 3.0,
  unit: "months",
  displayName: "Oxford RECOVERY Trial Duration",
  description: "Oxford RECOVERY trial duration (found life-saving treatment in 3 months)",
  sourceType: "external",
  sourceRef: "recovery-trial-82x-cost-reduction",
  confidence: "high",
};

export const PATIENT_WILLINGNESS_TRIAL_PARTICIPATION_PCT: Parameter = {
  value: 0.448,
  unit: "percentage",
  displayName: "Patient Willingness to Participate in Clinical Trials",
  description: "Patient willingness to participate in drug trials (44.8% in surveys, 88% when actually approached)",
  sourceType: "external",
  sourceRef: "patient-willingness-clinical-trials",
  confidence: "medium",
  confidenceInterval: [0.4, 0.5],
  stdError: 0.025,
};

export const PHARMA_DRUG_DEVELOPMENT_COST_CURRENT: Parameter = {
  value: 2600000000.0,
  unit: "USD",
  displayName: "Pharma Drug Development Cost (Current System)",
  description: "Average cost to develop one drug in current system",
  sourceType: "external",
  sourceRef: "drug-development-cost",
  confidence: "high",
  confidenceInterval: [1500000000.0, 4000000000.0],
  stdError: 500000000.0,
  peerReviewed: true,
};

export const PHARMA_DRUG_REVENUE_AVERAGE_CURRENT: Parameter = {
  value: 6700000000.0,
  unit: "USD",
  displayName: "Pharma Average Drug Revenue (Current System)",
  description: "Median lifetime revenue per successful drug (study of 361 FDA-approved drugs 1995-2014, median follow-up 13.2 years)",
  sourceType: "external",
  sourceRef: "pharma-drug-revenue-average",
  confidence: "high",
  peerReviewed: true,
};

export const PHARMA_ROI_CURRENT_SYSTEM_PCT: Parameter = {
  value: 0.012,
  unit: "percentage",
  displayName: "Pharma ROI (Current System)",
  description: "ROI for pharma R&D (2022 historic low from Deloitte study of top 20 pharma companies, down from 6.8% in 2021, recovered to 5.9% in 2024)",
  sourceType: "external",
  sourceRef: "pharma-roi-current",
  confidence: "high",
  peerReviewed: true,
};

export const PHARMA_SUCCESS_RATE_CURRENT_PCT: Parameter = {
  value: 0.1,
  unit: "percentage",
  displayName: "Pharma Drug Success Rate (Current System)",
  description: "Percentage of drugs that reach market in current system",
  sourceType: "external",
  sourceRef: "drug-trial-success-rate-12-pct",
  confidence: "high",
  peerReviewed: true,
};

export const PHASE_1_PASSED_COMPOUNDS_GLOBAL: Parameter = {
  value: 7500.0,
  unit: "compounds",
  displayName: "Phase I-Passed Compounds Globally",
  description: "Investigational compounds that have passed Phase I globally (midpoint of 5,000-10,000 range)",
  sourceType: "external",
  sourceRef: "bio-clinical-development-2021",
  confidence: "high",
  confidenceInterval: [5000.0, 10000.0],
};

export const PHASE_1_SAFETY_DURATION_YEARS: Parameter = {
  value: 2.3,
  unit: "years",
  displayName: "Phase I Safety Trial Duration",
  description: "Phase I safety trial duration",
  sourceType: "external",
  sourceRef: "bio-clinical-development-2021",
  confidence: "high",
  peerReviewed: true,
};

export const PHASE_2_3_CLINICAL_TRIAL_COST_PCT: Parameter = {
  value: 0.69,
  unit: "percentage",
  displayName: "Phase 2/3 Share of Clinical Trial Costs",
  description: "Percentage of total clinical trial spending on Phase 2/3 efficacy testing (Phase 2: 24% + Phase 3: 45%)",
  sourceType: "external",
  sourceRef: "global-clinical-trials-market-2024",
  confidence: "high",
  stdError: 0.05,
};

export const PHASE_3_TRIAL_COST_MIN: Parameter = {
  value: 20000000.0,
  unit: "USD/trial",
  displayName: "Phase 3 Trial Total Cost (Minimum)",
  description: "Phase 3 trial total cost (minimum)",
  sourceType: "external",
  sourceRef: "phase-3-cost-per-trial-range",
  confidence: "high",
};

export const PMC_PRAGMATIC_TRIAL_MEDIAN_COST_PER_PATIENT: Parameter = {
  value: 97.0,
  unit: "USD/patient",
  displayName: "Pragmatic Trial Median Cost per Patient (PMC Review)",
  description: "Median cost per patient in embedded pragmatic clinical trials (systematic review of 64 trials). IQR: $19-$478 (2015 USD).",
  sourceType: "external",
  sourceRef: "pmc-pragmatic-trial-cost",
  confidence: "high",
  confidenceInterval: [19.0, 478.0],
};

export const POLIO_VACCINATION_ROI: Parameter = {
  value: 39.0,
  unit: "ratio",
  displayName: "Return on Investment from Sustaining Polio Vaccination Assets and Integrating into Expanded Immunization Programs",
  description: "Return on investment from sustaining polio vaccination assets and integrating into expanded immunization programs",
  sourceType: "external",
  sourceRef: "polio-vaccination-roi",
  confidence: "high",
};

export const POLITICAL_DYSFUNCTION_TAX_COORDINATION_PCT: Parameter = {
  value: 0.05,
  unit: "percent",
  displayName: "Coordination Tax (Olson)",
  description: "Welfare loss from collective action failures. Diffuse beneficiaries (consumers, taxpayers) cannot organize against concentrated interests. Olson's logic of collective action: rational ignorance + free-rider problem prevents reform.",
  sourceType: "external",
  sourceRef: "olson1996",
  confidence: "low",
  confidenceInterval: [0.02, 0.1],
  stdError: 0.03,
};

export const POLITICAL_DYSFUNCTION_TAX_INFO_PCT: Parameter = {
  value: 0.02,
  unit: "percent",
  displayName: "Information Tax (Hayek)",
  description: "Welfare loss from information aggregation failures - the Hayek knowledge problem. Central authorities lack the dispersed local knowledge that markets aggregate. Hayek (1945) argued this is a fundamental limit on central planning effectiveness.",
  sourceType: "external",
  sourceRef: "hayek1945",
  confidence: "low",
  confidenceInterval: [0.01, 0.04],
  stdError: 0.01,
};

export const POLITICAL_DYSFUNCTION_TAX_TIME_PCT: Parameter = {
  value: 0.03,
  unit: "percent",
  displayName: "Time-Inconsistency Tax",
  description: "Welfare loss from political time-inconsistency (electoral short-termism). Politicians facing re-election underinvest in long-term public goods and infrastructure. Kydland-Prescott (1977) established the theoretical foundation for commitment vs discretion costs.",
  sourceType: "external",
  sourceRef: "kydland1977",
  confidence: "low",
  confidenceInterval: [0.01, 0.06],
  stdError: 0.02,
};

export const POLITICAL_SUCCESS_PROBABILITY: Parameter = {
  value: 0.01,
  unit: "rate",
  displayName: "Political Success Probability",
  description: "Estimated probability of treaty ratification and sustained implementation. Central estimate 1% is conservative. This assumes 99% chance of failure. ",
  sourceType: "external",
  sourceRef: "icbl-ottawa-treaty",
  confidence: "low",
  confidenceInterval: [0.001, 0.1],
  stdError: 0.02,
};

export const POLITICIAN_POST_OFFICE_CAREER_VALUE: Parameter = {
  value: 10000000.0,
  unit: "USD",
  displayName: "Post-Office Career Value (per politician)",
  description: "Net present value of post-office career premium for average congressperson (10 years x $1M/year premium). Based on documented cases: Gephardt $7M/year, Daschle $2M+/year.",
  sourceType: "external",
  sourceRef: "opensecrets-revolving-door",
  confidence: "medium",
  confidenceInterval: [5000000.0, 20000000.0],
};

export const POST_1962_DRUG_APPROVAL_REDUCTION_PCT: Parameter = {
  value: 0.7,
  unit: "percentage",
  displayName: "Post-1962 Drug Approval Reduction",
  description: "Reduction in new drug approvals after 1962 Kefauver-Harris Amendment (70% drop from 43→17 drugs/year)",
  sourceType: "external",
  sourceRef: "post-1962-drug-approval-drop",
  confidence: "high",
};

export const POST_WW2_MILITARY_CUT_PCT: Parameter = {
  value: 0.3,
  unit: "rate",
  displayName: "Percentage Military Spending Cut After WW2",
  description: "Percentage military spending cut after WW2 (historical precedent)",
  sourceType: "external",
  sourceRef: "us-post-wwii-military-spending-cut",
  confidence: "high",
};

export const PRE_1962_DRUG_DEVELOPMENT_COST_1980_USD: Parameter = {
  value: 6500000.0,
  unit: "USD_1980",
  displayName: "Pre-1962 Drug Development Cost (1980 Dollars)",
  description: "Average drug development cost before 1962 FDA efficacy regulations, adjusted to 1980 dollars (Baily 1972)",
  sourceType: "external",
  sourceRef: "pre-1962-drug-costs-baily-1972",
  confidence: "high",
  confidenceInterval: [5200000.0, 7800000.0],
  peerReviewed: true,
};

export const PRE_1962_DRUG_DEVELOPMENT_COST_2024_USD: Parameter = {
  value: 24700000.0,
  unit: "USD",
  displayName: "Pre-1962 Drug Development Cost (2024 Dollars)",
  description: "Pre-1962 drug development cost adjusted to 2024 dollars ($6.5M × 3.80 = $24.7M, CPI-adjusted from Baily 1972)",
  sourceType: "external",
  sourceRef: "pre-1962-drug-costs-baily-1972",
  confidence: "high",
  confidenceInterval: [19500000.0, 30000000.0],
  peerReviewed: true,
};

export const PRE_1962_PHYSICIAN_COUNT: Parameter = {
  value: 144000.0,
  unit: "physicians",
  displayName: "Pre-1962 Physician Count (Unverified)",
  description: "Estimated physicians conducting real-world efficacy trials pre-1962 (unverified estimate)",
  sourceType: "external",
  sourceRef: "pre-1962-physician-trials",
  confidence: "low",
};

export const RARE_DISEASES_COUNT_GLOBAL: Parameter = {
  value: 7000.0,
  unit: "diseases",
  displayName: "Total Number of Rare Diseases Globally",
  description: "Total number of rare diseases globally",
  sourceType: "external",
  sourceRef: "95-pct-diseases-no-treatment",
  confidence: "high",
  confidenceInterval: [6000.0, 10000.0],
};

export const RECOVERY_TRIAL_COST_PER_PATIENT: Parameter = {
  value: 500.0,
  unit: "USD/patient",
  displayName: "Recovery Trial Cost per Patient",
  description: "RECOVERY trial cost per patient. Note: RECOVERY was an outlier - hospital-based during COVID emergency, minimal extra procedures, existing NHS infrastructure, streamlined consent. Replicating this globally will be harder.",
  sourceType: "external",
  sourceRef: "recovery-cost-500",
  confidence: "high",
  confidenceInterval: [400.0, 2500.0],
};

export const RECOVERY_TRIAL_GLOBAL_LIVES_SAVED: Parameter = {
  value: 1000000.0,
  unit: "lives",
  displayName: "RECOVERY Trial Global Lives Saved",
  description: "Estimated lives saved globally by RECOVERY trial's dexamethasone discovery. NHS England estimate (March 2021). Based on Águas et al. Nature Communications 2021 methodology applying RECOVERY trial mortality reductions (36% ventilated, 18% oxygen) to global COVID hospitalizations. Wide uncertainty range reflects extrapolation assumptions.",
  sourceType: "external",
  sourceRef: "recovery-trial-1m-lives-saved",
  confidence: "medium",
  confidenceInterval: [500000.0, 2000000.0],
};

export const RECOVERY_TRIAL_TOTAL_COST: Parameter = {
  value: 20000000.0,
  unit: "USD",
  displayName: "RECOVERY Trial Total Cost",
  description: "Total cost of UK RECOVERY trial. Enrolled tens of thousands of patients across multiple treatment arms. Discovered dexamethasone reduces COVID mortality by ~1/3 in severe cases.",
  sourceType: "external",
  sourceRef: "recovery-trial-82x-cost-reduction",
  confidence: "high",
  confidenceInterval: [15000000.0, 25000000.0],
};

export const REGULATORY_DELAY_MEAN_AGE_OF_DEATH: Parameter = {
  value: 62.0,
  unit: "years",
  displayName: "Mean Age of Preventable Death from Post-Safety Efficacy Delay",
  description: "Mean age of preventable death from post-safety efficacy testing regulatory delay (Phase 2-4)",
  sourceType: "external",
  sourceRef: "who-global-health-estimates-2024",
  confidence: "medium",
  stdError: 3.0,
  peerReviewed: true,
};

export const REGULATORY_DELAY_SUFFERING_PERIOD_YEARS: Parameter = {
  value: 6.0,
  unit: "years",
  displayName: "Pre-Death Suffering Period During Post-Safety Efficacy Delay",
  description: "Pre-death suffering period during post-safety efficacy testing delay (average years lived with untreated condition while awaiting Phase 2-4 completion)",
  sourceType: "external",
  sourceRef: "who-global-health-estimates-2024",
  confidence: "medium",
  confidenceInterval: [4.0, 9.0],
  peerReviewed: true,
};

export const SINGAPORE_GDP_PER_CAPITA_PPP: Parameter = {
  value: 105000.0,
  unit: "USD",
  displayName: "Singapore GDP per Capita (PPP)",
  description: "Singapore GDP per capita (PPP-adjusted). Among highest in world, demonstrating that lean government can coexist with prosperity.",
  sourceType: "external",
  sourceRef: "worldbank-singapore-gdp",
  confidence: "high",
};

export const SINGAPORE_GOVT_SPENDING_PCT_GDP: Parameter = {
  value: 15.0,
  unit: "percent",
  displayName: "Singapore Govt Spending (% GDP)",
  description: "Singapore government spending as percentage of GDP. Less than HALF the US rate (15% vs 38%) yet achieves excellent outcomes through efficiency.",
  sourceType: "external",
  sourceRef: "imf-singapore-spending",
  confidence: "high",
};

export const SINGAPORE_LIFE_EXPECTANCY: Parameter = {
  value: 84.1,
  unit: "years",
  displayName: "Singapore Life Expectancy",
  description: "Singapore life expectancy at birth. 6.6 years LONGER than US (84.1 vs 77.5) despite government spending at less than half the rate.",
  sourceType: "external",
  sourceRef: "who-life-expectancy",
  confidence: "high",
};

export const SMALLPOX_ERADICATION_ROI: Parameter = {
  value: 280.0,
  unit: "ratio",
  displayName: "Return on Investment from Smallpox Eradication Campaign",
  description: "Return on investment from smallpox eradication campaign",
  sourceType: "external",
  sourceRef: "smallpox-eradication-roi",
  confidence: "high",
};

export const SMALLPOX_ERADICATION_TOTAL_BENEFIT: Parameter = {
  value: 1420000000.0,
  unit: "USD",
  displayName: "Total Economic Benefit from Smallpox Eradication Campaign",
  description: "Total economic benefit from smallpox eradication campaign",
  sourceType: "external",
  sourceRef: "smallpox-eradication-roi",
  confidence: "high",
};

export const SMOKING_CESSATION_ANNUAL_BENEFIT: Parameter = {
  value: 12000000000.0,
  unit: "USD/year",
  displayName: "Estimated Annual Global Economic Benefit from Smoking Cessation Programs",
  description: "Estimated annual global economic benefit from smoking cessation programs",
  sourceType: "external",
  sourceRef: "life-expectancy-gains-smoking-reduction",
  confidence: "high",
};

export const STANDARD_ECONOMIC_QALY_VALUE_USD: Parameter = {
  value: 150000.0,
  unit: "USD/QALY",
  displayName: "Standard Economic Value per QALY",
  description: "Standard economic value per QALY",
  sourceType: "external",
  sourceRef: "qaly-value",
  confidence: "high",
  stdError: 30000.0,
};

export const STANDARD_QALYS_PER_LIFE_SAVED: Parameter = {
  value: 35.0,
  unit: "QALYs/life",
  displayName: "Standard QALYs per Life Saved",
  description: "Standard QALYs per life saved (WHO life tables)",
  sourceType: "external",
  sourceRef: "qaly-value",
  confidence: "high",
  stdError: 7.0,
};

export const SUGAR_SUBSIDY_COST_PER_PERSON_ANNUAL: Parameter = {
  value: 10.0,
  unit: "USD/person/year",
  displayName: "Annual Cost of Sugar Subsidies per Person",
  description: "Annual cost of sugar subsidies per person",
  sourceType: "external",
  sourceRef: "sugar-subsidies-cost",
  confidence: "high",
};

export const SWITZERLAND_DEFENSE_SPENDING_PCT: Parameter = {
  value: 0.007,
  unit: "rate",
  displayName: "Switzerland's Defense Spending as Percentage of GDP",
  description: "Switzerland's defense spending as percentage of GDP (0.7%)",
  sourceType: "external",
  sourceRef: "swiss-military-budget-0-7-pct-gdp",
  confidence: "high",
};

export const SWITZERLAND_GDP_PER_CAPITA_K: Parameter = {
  value: 93000.0,
  unit: "USD",
  displayName: "Switzerland GDP per Capita",
  description: "Switzerland GDP per capita",
  sourceType: "external",
  sourceRef: "swiss-vs-us-gdp-per-capita",
  confidence: "high",
};

export const SWITZERLAND_GOVT_SPENDING_PCT_GDP: Parameter = {
  value: 35.0,
  unit: "percent",
  displayName: "Switzerland Govt Spending (% GDP)",
  description: "Switzerland government spending as percentage of GDP. 3 percentage points LOWER than US (35% vs 38%) yet achieves dramatically better outcomes.",
  sourceType: "external",
  sourceRef: "oecd-govt-spending",
  confidence: "high",
};

export const SWITZERLAND_LIFE_EXPECTANCY: Parameter = {
  value: 84.0,
  unit: "years",
  displayName: "Switzerland Life Expectancy",
  description: "Switzerland life expectancy at birth. 6.5 years LONGER than US (84.0 vs 77.5) despite lower government spending as % of GDP.",
  sourceType: "external",
  sourceRef: "who-life-expectancy",
  confidence: "high",
};

export const SWITZERLAND_MEDIAN_INCOME_PPP: Parameter = {
  value: 65000.0,
  unit: "USD",
  displayName: "Switzerland Median Income (PPP)",
  description: "Switzerland median household income (PPP-adjusted). Higher than US when adjusted for cost of healthcare and other expenses.",
  sourceType: "external",
  sourceRef: "oecd-median-income",
  confidence: "medium",
};

export const TERRORISM_DEATHS_911: Parameter = {
  value: 2996.0,
  unit: "deaths",
  displayName: "Deaths from 9/11 Terrorist Attacks",
  description: "Deaths from 9/11 terrorist attacks",
  sourceType: "external",
  sourceRef: "chance-of-dying-from-terrorism-1-in-30m",
  confidence: "high",
};

export const THALIDOMIDE_CASES_WORLDWIDE: Parameter = {
  value: 15000.0,
  unit: "cases",
  displayName: "Thalidomide Cases Worldwide",
  description: "Total thalidomide birth defect cases worldwide (1957-1962)",
  sourceType: "external",
  sourceRef: "thalidomide-scandal",
  confidence: "medium",
  confidenceInterval: [10000.0, 20000.0],
};

export const THALIDOMIDE_DISABILITY_WEIGHT: Parameter = {
  value: 0.4,
  unit: "ratio",
  displayName: "Thalidomide Disability Weight",
  description: "Disability weight for thalidomide survivors (limb deformities, organ damage)",
  sourceType: "external",
  sourceRef: "thalidomide-survivors-health",
  confidence: "medium",
  confidenceInterval: [0.32, 0.48],
};

export const THALIDOMIDE_MORTALITY_RATE: Parameter = {
  value: 0.4,
  unit: "percentage",
  displayName: "Thalidomide Mortality Rate",
  description: "Mortality rate for thalidomide-affected infants (died within first year)",
  sourceType: "external",
  sourceRef: "thalidomide-scandal",
  confidence: "high",
  confidenceInterval: [0.35, 0.45],
};

export const THALIDOMIDE_SURVIVOR_LIFESPAN: Parameter = {
  value: 60.0,
  unit: "years",
  displayName: "Thalidomide Survivor Lifespan",
  description: "Average lifespan for thalidomide survivors",
  sourceType: "external",
  sourceRef: "thalidomide-survivors-health",
  confidence: "medium",
  confidenceInterval: [50.0, 70.0],
};

export const THALIDOMIDE_US_POPULATION_SHARE_1960: Parameter = {
  value: 0.06,
  unit: "percentage",
  displayName: "US Population Share 1960",
  description: "US share of world population in 1960",
  sourceType: "external",
  sourceRef: "us-census-world-population-1960",
  confidence: "high",
  confidenceInterval: [0.055, 0.065],
};

export const TRADITIONAL_PHASE3_COST_PER_PATIENT: Parameter = {
  value: 41000.0,
  unit: "USD/patient",
  displayName: "Phase 3 Cost per Patient",
  description: "Phase 3 cost per patient (median from FDA study)",
  sourceType: "external",
  sourceRef: "trial-costs-fda-study",
  confidence: "high",
  confidenceInterval: [20000.0, 120000.0],
};

export const TREATMENT_ACCELERATION_YEARS_CURRENT: Parameter = {
  value: 17.0,
  unit: "years",
  displayName: "Traditional FDA Drug Development Timeline",
  description: "Traditional FDA drug development timeline",
  sourceType: "external",
  sourceRef: "fda-approval-timeline-10-years",
  confidence: "high",
};

export const TYPICAL_CEO_HOURLY_RATE: Parameter = {
  value: 10000.0,
  unit: "USD/hour",
  displayName: "Typical CEO Hourly Rate",
  description: "Typical CEO hourly rate",
  sourceType: "external",
  sourceRef: "ceo-compensation",
  confidence: "high",
};

export const US_ALZHEIMERS_ANNUAL_COST: Parameter = {
  value: 355000000000.0,
  unit: "USD",
  displayName: "US Alzheimer's Annual Cost",
  description: "Annual US cost of Alzheimer's disease (direct and indirect)",
  sourceType: "external",
  sourceRef: "disease-cost-alzheimers-1300b",
  confidence: "high",
  confidenceInterval: [302000000000.0, 408000000000.0],
  peerReviewed: true,
};

export const US_CANCER_ANNUAL_COST: Parameter = {
  value: 208000000000.0,
  unit: "USD",
  displayName: "US Cancer Annual Cost",
  description: "Annual US cost of cancer (direct and indirect)",
  sourceType: "external",
  sourceRef: "disease-cost-cancer-1800b",
  confidence: "high",
  confidenceInterval: [177000000000.0, 239000000000.0],
  peerReviewed: true,
};

export const US_CHRONIC_DISEASE_SPENDING_ANNUAL: Parameter = {
  value: 4100000000000.0,
  unit: "USD/year",
  displayName: "US Annual Chronic Disease Spending",
  description: "US annual chronic disease spending",
  sourceType: "external",
  sourceRef: "us-chronic-disease-spending",
  confidence: "high",
  confidenceInterval: [3300000000000.0, 5000000000000.0],
};

export const US_DIABETES_ANNUAL_COST: Parameter = {
  value: 327000000000.0,
  unit: "USD",
  displayName: "US Diabetes Annual Cost",
  description: "Annual US cost of diabetes (direct and indirect)",
  sourceType: "external",
  sourceRef: "disease-cost-diabetes-1500b",
  confidence: "high",
  confidenceInterval: [278000000000.0, 376000000000.0],
  peerReviewed: true,
};

export const US_GDP_2024: Parameter = {
  value: 28780000000000.0,
  unit: "USD",
  displayName: "US GDP (2024)",
  description: "US GDP in 2024 dollars for calculating policy costs as percentage of GDP.",
  sourceType: "external",
  sourceRef: "worldbank-gdp",
  confidence: "high",
};

export const US_GOVT_SPENDING_PCT_GDP: Parameter = {
  value: 38.0,
  unit: "percent",
  displayName: "US Govt Spending (% GDP)",
  description: "US total government spending as percentage of GDP (federal + state + local). OECD average is ~40%, but US gets worse outcomes for similar spending.",
  sourceType: "external",
  sourceRef: "oecd-govt-spending",
  confidence: "high",
};

export const US_HEART_DISEASE_ANNUAL_COST: Parameter = {
  value: 363000000000.0,
  unit: "USD",
  displayName: "US Heart Disease Annual Cost",
  description: "Annual US cost of heart disease and stroke (direct and indirect)",
  sourceType: "external",
  sourceRef: "disease-cost-heart-disease-2100b",
  confidence: "high",
  confidenceInterval: [309000000000.0, 417000000000.0],
  peerReviewed: true,
};

export const US_LIFE_EXPECTANCY_1880: Parameter = {
  value: 39.41,
  unit: "years",
  displayName: "US Life Expectancy (1880)",
  description: "US life expectancy in 1880 (closest available data point to 1883).",
  sourceType: "external",
  sourceRef: "life-expectancy-increase-pre-1962",
  confidence: "high",
  confidenceInterval: [38.9, 39.9],
  peerReviewed: true,
};

export const US_LIFE_EXPECTANCY_1962: Parameter = {
  value: 70.064,
  unit: "years",
  displayName: "US Life Expectancy (1962)",
  description: "US life expectancy in 1962 (year of Kefauver-Harris Amendments).",
  sourceType: "external",
  sourceRef: "life-expectancy-increase-pre-1962",
  confidence: "high",
  confidenceInterval: [69.8, 70.3],
  peerReviewed: true,
};

export const US_LIFE_EXPECTANCY_2019: Parameter = {
  value: 78.862,
  unit: "years",
  displayName: "US Life Expectancy (2019)",
  description: "US life expectancy in 2019 (latest available data).",
  sourceType: "external",
  sourceRef: "post-1962-life-expectancy-slowdown",
  confidence: "high",
  confidenceInterval: [78.6, 79.1],
  peerReviewed: true,
};

export const US_LIFE_EXPECTANCY_2023: Parameter = {
  value: 77.5,
  unit: "years",
  displayName: "US Life Expectancy",
  description: "US life expectancy at birth (2023). Lowest among high-income OECD countries despite highest healthcare spending.",
  sourceType: "external",
  sourceRef: "cdc-life-expectancy",
  confidence: "high",
};

export const US_MEDIAN_HOUSEHOLD_INCOME_2023: Parameter = {
  value: 80610.0,
  unit: "USD",
  displayName: "US Median Household Income",
  description: "US median household income (2023). High in absolute terms but adjusted for healthcare costs and inequality, purchasing power is lower than peers.",
  sourceType: "external",
  sourceRef: "census-income-2023",
  confidence: "high",
};

export const US_MENTAL_HEALTH_COST_ANNUAL: Parameter = {
  value: 350000000000.0,
  unit: "USD/year",
  displayName: "US Mental Health Costs",
  description: "US mental health costs (treatment + productivity loss)",
  sourceType: "external",
  sourceRef: "mental-health-burden",
  confidence: "high",
  confidenceInterval: [260000000000.0, 450000000000.0],
};

export const US_MILITARY_SPENDING_PCT_GDP: Parameter = {
  value: 0.035,
  unit: "rate",
  displayName: "US Military Spending as Percentage of GDP",
  description: "US military spending as percentage of GDP (2024)",
  sourceType: "external",
  sourceRef: "us-military-budget-3-5-pct-gdp",
  confidence: "high",
};

export const US_POPULATION_2024: Parameter = {
  value: 335000000.0,
  unit: "people",
  displayName: "US Population in 2024",
  description: "US population in 2024",
  sourceType: "external",
  sourceRef: "us-voter-population",
  confidence: "high",
  confidenceInterval: [330000000.0, 340000000.0],
};

export const US_SENATORS_FOR_TREATY: Parameter = {
  value: 67.0,
  unit: "senators",
  displayName: "Senators for Treaty Ratification",
  description: "Senators needed for treaty ratification (2/3 majority per Article II, Section 2)",
  sourceType: "external",
  sourceRef: "us-senate-treaties",
  confidence: "high",
};

export const US_TOTAL_FEDERAL_CAMPAIGN_SPENDING_2024: Parameter = {
  value: 20000000000.0,
  unit: "USD",
  displayName: "US Federal Campaign Spending (2024)",
  description: "Total US federal election spending in 2024 cycle including presidential, congressional, party committees, and PACs. Source: FEC Statistical Summary 2024.",
  sourceType: "external",
  sourceRef: "fec-2024-summary",
  confidence: "high",
};

export const US_TOTAL_LOBBYING_ANNUAL: Parameter = {
  value: 4400000000.0,
  unit: "USD",
  displayName: "US Total Lobbying (2024)",
  description: "Total US federal lobbying expenditure in 2024 (record year). Source: OpenSecrets.",
  sourceType: "external",
  sourceRef: "opensecrets-lobbying-2024",
  confidence: "high",
};

export const VALLEY_OF_DEATH_ATTRITION_PCT: Parameter = {
  value: 0.4,
  unit: "percentage",
  displayName: "Valley of Death Attrition Rate",
  description: "Percentage of promising Phase 1-passed compounds abandoned primarily due to Phase 2/3 cost barriers (not scientific failure). Conservative estimate: many rare disease, natural compound, and low-margin drugs never tested.",
  sourceType: "external",
  sourceRef: "valley-of-death-attrition",
  confidence: "medium",
  confidenceInterval: [0.25, 0.55],
};

export const VALUE_OF_STATISTICAL_LIFE: Parameter = {
  value: 10000000.0,
  unit: "USD",
  displayName: "Value of Statistical Life",
  description: "Value of Statistical Life (conservative estimate)",
  sourceType: "external",
  sourceRef: "dot-vsl-13-6m",
  confidence: "high",
  confidenceInterval: [5000000.0, 15000000.0],
  stdError: 3000000.0,
};

export const VITAMIN_A_COST_PER_DALY: Parameter = {
  value: 37.0,
  unit: "USD/DALY",
  displayName: "Vitamin A Supplementation Cost per DALY",
  description: "Cost per DALY for vitamin A supplementation programs (India: $23-50; Africa: $40-255; wide variation by region and baseline VAD prevalence). Using India midpoint as conservative estimate.",
  sourceType: "external",
  sourceRef: "vitamin-a-cost-per-daly",
  confidence: "medium",
};

export const WATER_FLUORIDATION_ANNUAL_BENEFIT: Parameter = {
  value: 800000000.0,
  unit: "USD/year",
  displayName: "Estimated Annual Global Economic Benefit from Water Fluoridation Programs",
  description: "Estimated annual global economic benefit from water fluoridation programs",
  sourceType: "external",
  sourceRef: "clean-water-sanitation-roi",
  confidence: "high",
};

export const WATER_FLUORIDATION_ROI: Parameter = {
  value: 23.0,
  unit: "ratio",
  displayName: "Return on Investment from Water Fluoridation Programs",
  description: "Return on investment from water fluoridation programs",
  sourceType: "external",
  sourceRef: "clean-water-sanitation-roi",
  confidence: "high",
};

export const WHO_QALY_THRESHOLD_COST_EFFECTIVE: Parameter = {
  value: 50000.0,
  unit: "USD/QALY",
  displayName: "Cost-Effectiveness Threshold ($50,000/QALY)",
  description: "Cost-effectiveness threshold widely used in US health economics ($50,000/QALY, from 1980s dialysis costs)",
  sourceType: "external",
  sourceRef: "who-cost-effectiveness-threshold",
  confidence: "high",
};

export const WORKFORCE_WITH_PRODUCTIVITY_LOSS: Parameter = {
  value: 0.28,
  unit: "rate",
  displayName: "Percentage of Workforce Experiencing Productivity Loss from Chronic Illness",
  description: "Percentage of workforce experiencing productivity loss from chronic illness (28%)",
  sourceType: "external",
  sourceRef: "chronic-illness-workforce-productivity-loss",
  confidence: "high",
};

// ============================================================================
// Calculated Values
// ============================================================================

export const ADDITIONAL_DRUGS_FROM_COST_ELIMINATION: Parameter = {
  value: 20.0,
  unit: "drugs/year",
  displayName: "Additional Drug Approvals from Cost Elimination",
  description: "Additional drug approvals per year when Phase 2/3 cost barrier eliminated. Assumes valley-of-death compounds (abandoned due to cost) would have similar success rate to funded compounds.",
  sourceType: "calculated",
  confidence: "medium",
  formula: "CURRENT_APPROVALS × VALLEY_OF_DEATH_PCT",
  latex: "\\begin{gathered}\nDrugs_{new} \\\\\n= Drugs_{ann,curr} \\times Attrition_{valley} \\\\\n= 50 \\times 40\\% \\\\\n= 20\n\\end{gathered}",
};

export const BAD_POLICY_COST_TOTAL_US: Parameter = {
  value: 5032850000000.0,
  unit: "USD",
  displayName: "Bad Policy Costs Total (US)",
  description: "Total annual US bad policy costs (Tier 1 + Tier 2 with overlap discount). Bottom-up empirical estimate based on specific, measurable policy failures. More defensible than theoretical decomposition because each component is verifiable.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/optimocracy-paper#bad-policy-costs",
  confidence: "low",
  formula: "(TIER1 + TIER2) × OVERLAP_DISCOUNT",
  latex: "\\begin{gathered}\nC_{bad,total} \\\\\n= BadUS \\times (C_{tier1} + C_{tier2}) \\\\\n= 0.85 \\times (\\$3.92T + \\$2T) \\\\\n= \\$5.03T \\\\[0.5em]\n\\text{where } C_{tier1} \\\\\n= C_{tax} + C_{wars} + C_{drugs} + C_{tariffs} \\\\\n+ C_{ff,explicit} + C_{healthcare} + C_{housing} \\\\\n+ C_{ag} \\\\\n= \\$546B + \\$400B + \\$90B + \\$160B + \\$50B + \\$1.2T \\\\\n+ \\$1.4T + \\$75B \\\\\n= \\$3.92T \\\\[0.5em]\n\\text{where } C_{tier2} \\\\\n= C_{ff,external} + C_{licensing} + C_{migration} \\\\\n+ C_{defense} + C_{prison} + C_{infra} \\\\\n= \\$600B + \\$200B + \\$500B + \\$400B + \\$150B + \\$150B \\\\\n= \\$2T\n\\end{gathered}",
};

export const BAD_POLICY_COST_TOTAL_US_PCT_GDP: Parameter = {
  value: 0.17487317581653927,
  unit: "percent",
  displayName: "Bad Policy Costs (% GDP)",
  description: "Total US bad policy costs as percentage of GDP. Bottom-up empirical estimate for comparison with theoretical Political Dysfunction Tax.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/optimocracy-paper#bad-policy-costs",
  confidence: "low",
  formula: "BAD_POLICY_COST_TOTAL / US_GDP",
  latex: "\\begin{gathered}\n\\tau_{bad,empirical} = \\frac{C_{bad,total}}{USGDP} = \\frac{\\$5.03T}{\\$28.8T} = 17.5\\% \\\\[0.5em]\n\\text{where } C_{bad,total} \\\\\n= BadUS \\times (C_{tier1} + C_{tier2}) \\\\\n= 0.85 \\times (\\$3.92T + \\$2T) \\\\\n= \\$5.03T \\\\[0.5em]\n\\text{where } C_{tier1} \\\\\n= C_{tax} + C_{wars} + C_{drugs} + C_{tariffs} \\\\\n+ C_{ff,explicit} + C_{healthcare} + C_{housing} \\\\\n+ C_{ag} \\\\\n= \\$546B + \\$400B + \\$90B + \\$160B + \\$50B + \\$1.2T \\\\\n+ \\$1.4T + \\$75B \\\\\n= \\$3.92T \\\\[0.5em]\n\\text{where } C_{tier2} \\\\\n= C_{ff,external} + C_{licensing} + C_{migration} \\\\\n+ C_{defense} + C_{prison} + C_{infra} \\\\\n= \\$600B + \\$200B + \\$500B + \\$400B + \\$150B + \\$150B \\\\\n= \\$2T\n\\end{gathered}",
};

export const BAD_POLICY_COST_US_TIER1_TOTAL: Parameter = {
  value: 3921000000000.0,
  unit: "USD",
  displayName: "Bad Policy Costs (Tier 1)",
  description: "Sum of Tier 1 (well-documented) bad policy costs: tax compliance + failed wars + drug war + tariffs + fossil fuel explicit + healthcare inefficiency + housing/zoning + agricultural subsidies. These have strong empirical backing and high economist consensus.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/optimocracy-paper#bad-policy-costs",
  confidence: "medium",
  formula: "TAX + WARS + DRUGS + TARIFFS + FF_EXPLICIT + HEALTHCARE + HOUSING + AG",
  latex: "\\begin{gathered}\nC_{tier1} \\\\\n= C_{tax} + C_{wars} + C_{drugs} + C_{tariffs} \\\\\n+ C_{ff,explicit} + C_{healthcare} + C_{housing} + C_{ag} \\\\\n= \\$546B + \\$400B + \\$90B + \\$160B + \\$50B + \\$1.2T + \\$1.4T \\\\\n+ \\$75B \\\\\n= \\$3.92T\n\\end{gathered}",
};

export const BAD_POLICY_COST_US_TIER2_TOTAL: Parameter = {
  value: 2000000000000.0,
  unit: "USD",
  displayName: "Bad Policy Costs (Tier 2)",
  description: "Sum of Tier 2 (contested but defensible) bad policy costs: fossil fuel externalities + occupational licensing + migration restrictions + defense above deterrence + incarceration excess + infrastructure cost disease. Wider uncertainty due to counterfactual assumptions.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/optimocracy-paper#bad-policy-costs",
  confidence: "low",
  formula: "FF_EXT + LICENSING + MIGRATION + DEFENSE + PRISON + INFRA",
  latex: "\\begin{gathered}\nC_{tier2} \\\\\n= C_{ff,external} + C_{licensing} + C_{migration} \\\\\n+ C_{defense} + C_{prison} + C_{infra} \\\\\n= \\$600B + \\$200B + \\$500B + \\$400B + \\$150B + \\$150B \\\\\n= \\$2T\n\\end{gathered}",
};

export const CELL_THERAPY_DISEASE_COMBINATIONS: Parameter = {
  value: 500000.0,
  unit: "combinations",
  displayName: "Cell Therapy Combinations",
  description: "Cell therapy approach-disease combinations",
  sourceType: "calculated",
  confidence: "high",
  formula: "CELL_APPROACHES × DISEASES",
  latex: "\\begin{gathered}\nCombos_{cell} \\\\\n= N_{cell} \\times N_{diseases,trial} \\\\\n= 500 \\times 1{,}000 \\\\\n= 500{,}000\n\\end{gathered}",
};

export const CLINICAL_TRIAL_COST_PER_APPROVED_DRUG: Parameter = {
  value: 1200000000.0,
  unit: "USD",
  displayName: "Clinical Trial Cost Per Approved Drug",
  description: "Annual clinical trial spending per approved drug (trials only, excluding other R&D costs like discovery, preclinical, manufacturing). Note: $60B ÷ 50 drugs = $1.2B per drug.",
  sourceType: "calculated",
  confidence: "high",
  formula: "TOTAL_TRIAL_SPENDING / NEW_DRUGS",
  latex: "\\begin{gathered}\nCost_{trial,drug} \\\\\n= \\frac{Spending_{trials}}{Drugs_{ann,curr}} \\\\\n= \\frac{\\$60B}{50} \\\\\n= \\$1.2B\n\\end{gathered}",
};

export const CLINICAL_TRIAL_COST_PER_PARTICIPANT_ANNUAL: Parameter = {
  value: 31578.947368421053,
  unit: "USD",
  displayName: "Annual Cost Per Clinical Trial Participant",
  description: "Average annual cost per clinical trial participant (total spending ÷ participants). Note: $60B ÷ 1.9M = $31,579 per participant.",
  sourceType: "calculated",
  confidence: "high",
  formula: "TOTAL_SPENDING / PARTICIPANTS",
  latex: "\\begin{gathered}\nCost_{trial,pt,ann} \\\\\n= \\frac{Spending_{trials}}{Slots_{curr}} \\\\\n= \\frac{\\$60B}{1.9M} \\\\\n= \\$31.6K\n\\end{gathered}",
};

export const COMBINATION_THERAPY_DISEASE_SPACE: Parameter = {
  value: 45120250000.0,
  unit: "combinations",
  displayName: "Combination Therapy Space",
  description: "Total combination therapy space (pairwise drug combinations × diseases). Standard in oncology, HIV, cardiology.",
  sourceType: "calculated",
  confidence: "high",
  formula: "DRUG_PAIRS × DISEASES",
  latex: "\\begin{gathered}\nSpace_{combo} \\\\\n= N_{combo} \\times N_{diseases,trial} \\\\\n= 45.1M \\times 1{,}000 \\\\\n= 45.1B\n\\end{gathered}",
};

export const COMBINATION_THERAPY_PAIRS: Parameter = {
  value: 45120250.0,
  unit: "combinations",
  displayName: "Pairwise Drug Combinations",
  description: "Unique pairwise drug combinations from known safe compounds (n choose 2)",
  sourceType: "calculated",
  confidence: "high",
  formula: "SAFE_COMPOUNDS × (SAFE_COMPOUNDS - 1) ÷ 2",
};

export const COMBINED_PEACE_HEALTH_DIVIDENDS_ANNUAL_FOR_ROI_CALC: Parameter = {
  value: 172211487804.87805,
  unit: "USD/year",
  displayName: "Combined Peace and Health Dividends for ROI Calculation",
  description: "Combined peace and health dividends for ROI calculation",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/peace-dividend-calculations#peace-dividend-composition",
  confidence: "high",
  formula: "PEACE_DIVIDEND + R&D_SAVINGS",
  latex: "\\begin{gathered}\nDividend_{total,ann} \\\\\n= Benefit_{peace,soc} + Benefit_{RD,ann} \\\\\n= \\$114B + \\$58.6B \\\\\n= \\$172B \\\\[0.5em]\n\\text{where } Benefit_{peace,soc} \\\\\n= Cost_{war,total} \\times Reduce_{treaty} \\\\\n= \\$11.4T \\times 1\\% \\\\\n= \\$114B \\\\[0.5em]\n\\text{where } Cost_{war,total} \\\\\n= Cost_{war,direct} + Cost_{war,indirect} \\\\\n= \\$7.66T + \\$3.7T \\\\\n= \\$11.4T \\\\[0.5em]\n\\text{where } Cost_{war,direct} \\\\\n= Loss_{life,conflict} + Damage_{infra,total} \\\\\n+ Disruption_{trade} + Spending_{mil} \\\\\n= \\$2.45T + \\$1.88T + \\$616B + \\$2.72T \\\\\n= \\$7.66T \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B \\\\[0.5em]\n\\text{where } Cost_{war,indirect} \\\\\n= Damage_{env} + Loss_{growth,mil} \\\\\n+ Loss_{capital,conflict} + Cost_{psych} \\\\\n+ Cost_{refugee} + Cost_{vet} \\\\\n= \\$100B + \\$2.72T + \\$300B + \\$232B + \\$150B + \\$200B \\\\\n= \\$3.7T \\\\[0.5em]\n\\text{where } Benefit_{RD,ann} \\\\\n= Spending_{trials} \\times Reduce_{pct} \\\\\n= \\$60B \\times 97.7\\% \\\\\n= \\$58.6B \\\\[0.5em]\n\\text{where } Reduce_{pct} \\\\\n= 1 - \\frac{Cost_{pragmatic,pt}}{Cost_{P3,pt}} \\\\\n= 1 - \\frac{\\$929}{\\$41K} \\\\\n= 97.7\\%\n\\end{gathered}",
};

export const CURRENT_COMBINATION_EXPLORATION_YEARS: Parameter = {
  value: 13672803.030303031,
  unit: "years",
  displayName: "Combination Therapy Exploration Time (Current)",
  description: "Years to test all pairwise drug combinations at current trial capacity. Combination therapy is standard in oncology, HIV, cardiology.",
  sourceType: "calculated",
  confidence: "high",
  formula: "COMBINATION_SPACE ÷ CURRENT_TRIALS_PER_YEAR",
  latex: "\\begin{gathered}\nT_{explore,combo} \\\\\n= \\frac{Space_{combo}}{Trials_{ann,curr}} \\\\\n= \\frac{45.1B}{3{,}300} \\\\\n= 13.7M \\\\[0.5em]\n\\text{where } Space_{combo} \\\\\n= N_{combo} \\times N_{diseases,trial} \\\\\n= 45.1M \\times 1{,}000 \\\\\n= 45.1B\n\\end{gathered}",
};

export const CURRENT_KNOWN_SAFE_EXPLORATION_YEARS: Parameter = {
  value: 2878.787878787879,
  unit: "years",
  displayName: "Known Safe Exploration Time (Current)",
  description: "Years to test all known safe drug-disease combinations at current global trial capacity",
  sourceType: "calculated",
  confidence: "high",
  formula: "DRUG_DISEASE_COMBINATIONS ÷ CURRENT_TRIALS_PER_YEAR",
  latex: "\\begin{gathered}\nT_{explore,safe} \\\\\n= \\frac{N_{combos}}{Trials_{ann,curr}} \\\\\n= \\frac{9.5M}{3{,}300} \\\\\n= 2{,}880 \\\\[0.5em]\n\\text{where } N_{combos} \\\\\n= N_{safe} \\times N_{diseases,trial} \\\\\n= 9{,}500 \\times 1{,}000 \\\\\n= 9.5M\n\\end{gathered}",
};

export const CURRENT_TOTAL_EXPLORATION_YEARS: Parameter = {
  value: 15606.060606060606,
  unit: "years",
  displayName: "Total Exploration Time (Current)",
  description: "Years to test all therapeutic combinations (known safe + emerging modalities) at current capacity",
  sourceType: "calculated",
  confidence: "high",
  formula: "TOTAL_COMBINATIONS ÷ CURRENT_TRIALS_PER_YEAR",
  latex: "\\begin{gathered}\nT_{explore,total} \\\\\n= \\frac{N_{testable}}{Trials_{ann,curr}} \\\\\n= \\frac{51.5M}{3{,}300} \\\\\n= 15{,}600 \\\\[0.5em]\n\\text{where } N_{testable} \\\\\n= N_{combos} + N_{emerging} \\\\\n= 9.5M + 42M \\\\\n= 51.5M \\\\[0.5em]\n\\text{where } N_{combos} \\\\\n= N_{safe} \\times N_{diseases,trial} \\\\\n= 9{,}500 \\times 1{,}000 \\\\\n= 9.5M \\\\[0.5em]\n\\text{where } N_{emerging} \\\\\n= Combos_{gene} + Combos_{mRNA} + Combos_{epi} + Combos_{cell} \\\\\n= 20M + 20M + 1.5M + 500{,}000 \\\\\n= 42M \\\\[0.5em]\n\\text{where } Combos_{gene} \\\\\n= N_{genes} \\times N_{diseases,trial} \\\\\n= 20{,}000 \\times 1{,}000 \\\\\n= 20M \\\\[0.5em]\n\\text{where } Combos_{mRNA} \\\\\n= N_{genes} \\times N_{diseases,trial} \\\\\n= 20{,}000 \\times 1{,}000 \\\\\n= 20M \\\\[0.5em]\n\\text{where } Combos_{epi} \\\\\n= N_{epi} \\times N_{diseases,trial} \\\\\n= 1{,}500 \\times 1{,}000 \\\\\n= 1.5M \\\\[0.5em]\n\\text{where } Combos_{cell} \\\\\n= N_{cell} \\times N_{diseases,trial} \\\\\n= 500 \\times 1{,}000 \\\\\n= 500{,}000\n\\end{gathered}",
};

export const DFDA_ANNUAL_OPEX: Parameter = {
  value: 40000000.0,
  unit: "USD/year",
  displayName: "Total Annual Decentralized Framework for Drug Assessment Operational Costs",
  description: "Total annual Decentralized Framework for Drug Assessment operational costs (sum of all components: $15M + $10M + $8M + $5M + $2M)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#opex-breakdown",
  confidence: "high",
  formula: "PLATFORM_MAINTENANCE + STAFF + INFRASTRUCTURE + REGULATORY + COMMUNITY",
  latex: "\\begin{gathered}\nOPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M\n\\end{gathered}",
};

export const DFDA_BENEFIT_RD_ONLY_ANNUAL: Parameter = {
  value: 58640487804.878044,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Annual Benefit: R&D Savings",
  description: "Annual Decentralized Framework for Drug Assessment benefit from R&D savings (trial cost reduction, secondary component)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#cost-reduction",
  confidence: "high",
  formula: "TRIAL_SPENDING × COST_REDUCTION_PCT",
  latex: "\\begin{gathered}\nBenefit_{RD,ann} \\\\\n= Spending_{trials} \\times Reduce_{pct} \\\\\n= \\$60B \\times 97.7\\% \\\\\n= \\$58.6B \\\\[0.5em]\n\\text{where } Reduce_{pct} \\\\\n= 1 - \\frac{Cost_{pragmatic,pt}}{Cost_{P3,pt}} \\\\\n= 1 - \\frac{\\$929}{\\$41K} \\\\\n= 97.7\\%\n\\end{gathered}",
};

export const DFDA_COMBINED_TREATMENT_SPEEDUP_MULTIPLIER: Parameter = {
  value: 17.22735255792873,
  unit: "multiplier",
  displayName: "dFDA Combined Treatment Discovery Speedup Multiplier",
  description: "Combined speedup factor for treatment discovery from dFDA. Trial capacity multiplier times valley of death rescue multiplier. Diseases that would take T years to get first treatment now take T/speedup years.",
  sourceType: "calculated",
  confidence: "medium",
  formula: "DFDA_TRIAL_CAPACITY_MULTIPLIER × DFDA_VALLEY_OF_DEATH_RESCUE_MULTIPLIER",
  latex: "\\begin{gathered}\nk_{speedup} = k_{capacity} \\times k_{rescue} = 12.3 \\times 1.4 = 17.2 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } k_{rescue} = Attrition_{valley} + 1 = 40\\% + 1 = 1.4\n\\end{gathered}",
};

export const DFDA_DIRECT_FUNDING_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG: Parameter = {
  value: 178366.20663168447,
  unit: "ratio",
  displayName: "Direct Funding ROI - Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Increased Trial Throughput",
  description: "ROI from direct philanthropic/government funding of medical research (vs treaty campaign). Same benefits as treaty but costs $541.9B NPV instead of $1B campaign. Still excellent ROI, but treaty campaign achieves 542× better leverage.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper",
  confidence: "high",
  formula: "ECONOMIC_VALUE ÷ DIRECT_FUNDING_NPV",
  latex: "\\begin{gathered}\nROI_{direct,max} = \\frac{Value_{max}}{NPV_{direct}} = \\frac{\\$84800T}{\\$475B} = 178{,}000 \\\\[0.5em]\n\\text{where } Value_{max} \\\\\n= DALYs_{max} \\times Value_{QALY} \\\\\n= 565B \\times \\$150K \\\\\n= \\$84800T \\\\[0.5em]\n\\text{where } DALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } NPV_{direct} \\\\\n= \\frac{T_{queue,dFDA}}{Treasury_{RD,ann} \\times r_{discount}} \\\\\n= \\frac{36}{\\$21.8B \\times 3\\%} \\\\\n= \\$475B \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } T_{queue,dFDA} = \\frac{T_{queue,SQ}}{k_{capacity}} = \\frac{443}{12.3} = 36 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_DIRECT_FUNDING_VS_BED_NETS_MULTIPLIER: Parameter = {
  value: 105.83061593479944,
  unit: "ratio",
  displayName: "Direct Funding Cost-Effectiveness vs Bed Nets",
  description: "How many times more cost-effective direct funding is vs bed nets ($89/DALY). Even without treaty leverage, direct funding of medical research is highly cost-effective.",
  sourceType: "calculated",
  confidence: "high",
  formula: "BED_NETS_COST_PER_DALY ÷ DIRECT_FUNDING_COST_PER_DALY",
  latex: "\\begin{gathered}\nk_{direct,nets} = \\frac{Cost_{nets}}{Cost_{direct,DALY}} = \\frac{\\$89}{\\$0.841} = 106 \\\\[0.5em]\n\\text{where } Cost_{direct,DALY} = \\frac{NPV_{direct}}{DALYs_{max}} = \\frac{\\$475B}{565B} = \\$0.841 \\\\[0.5em]\n\\text{where } NPV_{direct} \\\\\n= \\frac{T_{queue,dFDA}}{Treasury_{RD,ann} \\times r_{discount}} \\\\\n= \\frac{36}{\\$21.8B \\times 3\\%} \\\\\n= \\$475B \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } T_{queue,dFDA} = \\frac{T_{queue,SQ}}{k_{capacity}} = \\frac{443}{12.3} = 36 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } DALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_EFFICACY_LAG_ELIMINATION_DALYS: Parameter = {
  value: 7942783571.3,
  unit: "DALYs",
  displayName: "Total DALYs Lost from Disease Eradication Delay",
  description: "Total Disability-Adjusted Life Years lost from disease eradication delay (PRIMARY estimate)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/regulatory-mortality-analysis#daly-calculation",
  confidence: "medium",
  formula: "YLL + YLD",
  latex: "\\begin{gathered}\nDALYs_{lag} = YLL_{lag} + YLD_{lag} = 7.07B + 873M = 7.94B \\\\[0.5em]\n\\text{where } YLL_{lag} \\\\\n= Deaths_{lag} \\times (LE_{global} - Age_{death,delay}) \\\\\n= 416M \\times (79 - 62) \\\\\n= 7.07B \\\\[0.5em]\n\\text{where } Deaths_{lag} \\\\\n= T_{lag} \\times Deaths_{disease,daily} \\times 338 \\\\\n= 8.2 \\times 150{,}000 \\times 338 \\\\\n= 416M \\\\[0.5em]\n\\text{where } YLD_{lag} \\\\\n= Deaths_{lag} \\times T_{suffering} \\times DW_{chronic} \\\\\n= 416M \\times 6 \\times 0.35 \\\\\n= 873M \\\\[0.5em]\n\\text{where } Deaths_{lag} \\\\\n= T_{lag} \\times Deaths_{disease,daily} \\times 338 \\\\\n= 8.2 \\times 150{,}000 \\times 338 \\\\\n= 416M\n\\end{gathered}",
};

export const DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED: Parameter = {
  value: 415852543.0,
  unit: "deaths",
  displayName: "Total Deaths from Disease Eradication Delay",
  description: "Total eventually avoidable deaths from delaying disease eradication by 8.2 years (PRIMARY estimate, conservative). Excludes fundamentally unavoidable deaths (primarily accidents ~7.9%).",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/regulatory-mortality-analysis#disease-eradication-delay",
  confidence: "medium",
  formula: "ANNUAL_DEATHS × EFFICACY_LAG_YEARS × EVENTUALLY_AVOIDABLE_DEATH_PCT",
  latex: "\\begin{gathered}\nDeaths_{lag} \\\\\n= T_{lag} \\times Deaths_{disease,daily} \\times 338 \\\\\n= 8.2 \\times 150{,}000 \\times 338 \\\\\n= 416M\n\\end{gathered}",
};

export const DFDA_EFFICACY_LAG_ELIMINATION_ECONOMIC_VALUE: Parameter = {
  value: 1191417535695000.0,
  unit: "USD",
  displayName: "Total Economic Loss from Disease Eradication Delay",
  description: "Total economic loss from delaying disease eradication by 8.2 years (PRIMARY estimate, 2024 USD). Values global DALYs at standardized US/International normative rate ($150k) rather than local ability-to-pay, representing the full human capital loss.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/regulatory-mortality-analysis#economic-valuation",
  confidence: "medium",
  formula: "DALYS_TOTAL × VSLY",
  latex: "\\begin{gathered}\nValue_{lag} \\\\\n= DALYs_{lag} \\times Value_{QALY} \\\\\n= 7.94B \\times \\$150K \\\\\n= \\$1190T \\\\[0.5em]\n\\text{where } DALYs_{lag} = YLL_{lag} + YLD_{lag} = 7.07B + 873M = 7.94B \\\\[0.5em]\n\\text{where } YLL_{lag} \\\\\n= Deaths_{lag} \\times (LE_{global} - Age_{death,delay}) \\\\\n= 416M \\times (79 - 62) \\\\\n= 7.07B \\\\[0.5em]\n\\text{where } Deaths_{lag} \\\\\n= T_{lag} \\times Deaths_{disease,daily} \\times 338 \\\\\n= 8.2 \\times 150{,}000 \\times 338 \\\\\n= 416M \\\\[0.5em]\n\\text{where } YLD_{lag} \\\\\n= Deaths_{lag} \\times T_{suffering} \\times DW_{chronic} \\\\\n= 416M \\times 6 \\times 0.35 \\\\\n= 873M \\\\[0.5em]\n\\text{where } Deaths_{lag} \\\\\n= T_{lag} \\times Deaths_{disease,daily} \\times 338 \\\\\n= 8.2 \\times 150{,}000 \\times 338 \\\\\n= 416M\n\\end{gathered}",
};

export const DFDA_EFFICACY_LAG_ELIMINATION_YLD: Parameter = {
  value: 873290340.3,
  unit: "years",
  displayName: "Years Lived with Disability During Disease Eradication Delay",
  description: "Years Lived with Disability during disease eradication delay (PRIMARY estimate)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/regulatory-mortality-analysis#daly-calculation",
  confidence: "medium",
  formula: "DEATHS_TOTAL × SUFFERING_PERIOD × DISABILITY_WEIGHT",
  latex: "\\begin{gathered}\nYLD_{lag} \\\\\n= Deaths_{lag} \\times T_{suffering} \\times DW_{chronic} \\\\\n= 416M \\times 6 \\times 0.35 \\\\\n= 873M \\\\[0.5em]\n\\text{where } Deaths_{lag} \\\\\n= T_{lag} \\times Deaths_{disease,daily} \\times 338 \\\\\n= 8.2 \\times 150{,}000 \\times 338 \\\\\n= 416M\n\\end{gathered}",
};

export const DFDA_EFFICACY_LAG_ELIMINATION_YLL: Parameter = {
  value: 7069493231.0,
  unit: "years",
  displayName: "Years of Life Lost from Disease Eradication Delay",
  description: "Years of Life Lost from disease eradication delay deaths (PRIMARY estimate)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/regulatory-mortality-analysis#daly-calculation",
  confidence: "medium",
  formula: "DEATHS_TOTAL × (LIFE_EXPECTANCY - MEAN_AGE_OF_DEATH)",
  latex: "\\begin{gathered}\nYLL_{lag} \\\\\n= Deaths_{lag} \\times (LE_{global} - Age_{death,delay}) \\\\\n= 416M \\times (79 - 62) \\\\\n= 7.07B \\\\[0.5em]\n\\text{where } Deaths_{lag} \\\\\n= T_{lag} \\times Deaths_{disease,daily} \\times 338 \\\\\n= 8.2 \\times 150{,}000 \\times 338 \\\\\n= 416M\n\\end{gathered}",
};

export const DFDA_FIRST_TREATMENTS_PER_YEAR: Parameter = {
  value: 184.57877740637923,
  unit: "diseases/year",
  displayName: "dFDA New Treatments Per Year",
  description: "Diseases per year receiving their first effective treatment with dFDA. Scales proportionally with trial capacity multiplier.",
  sourceType: "calculated",
  confidence: "low",
  formula: "NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR × DFDA_TRIAL_CAPACITY_MULTIPLIER",
  latex: "\\begin{gathered}\nTreatments_{dFDA,ann} \\\\\n= Treatments_{new,ann} \\times k_{capacity} \\\\\n= 15 \\times 12.3 \\\\\n= 185 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_KNOWN_SAFE_EXPLORATION_YEARS: Parameter = {
  value: 233.94790445895418,
  unit: "years",
  displayName: "Known Safe Exploration Time (dFDA)",
  description: "Years to test all known safe drug-disease combinations with dFDA trial capacity",
  sourceType: "calculated",
  confidence: "high",
  formula: "DRUG_DISEASE_COMBINATIONS ÷ DFDA_TRIALS_PER_YEAR",
  latex: "\\begin{gathered}\nT_{safe,dFDA} = \\frac{N_{combos}}{Capacity_{trials}} = \\frac{9.5M}{40{,}600} = 234 \\\\[0.5em]\n\\text{where } N_{combos} \\\\\n= N_{safe} \\times N_{diseases,trial} \\\\\n= 9{,}500 \\times 1{,}000 \\\\\n= 9.5M \\\\[0.5em]\n\\text{where } Capacity_{trials} \\\\\n= Trials_{ann,curr} \\times k_{capacity} \\\\\n= 3{,}300 \\times 12.3 \\\\\n= 40{,}600 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_NET_SAVINGS_RD_ONLY_ANNUAL: Parameter = {
  value: 58600487804.878044,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Annual Net Savings (R&D Only)",
  description: "Annual net savings from R&D cost reduction only (gross savings minus operational costs, excludes regulatory delay value)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#net-savings",
  confidence: "high",
  formula: "GROSS_SAVINGS - ANNUAL_OPEX",
  latex: "\\begin{gathered}\nSavings_{RD,ann} \\\\\n= Benefit_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$58.6B - \\$40M \\\\\n= \\$58.6B \\\\[0.5em]\n\\text{where } Benefit_{RD,ann} \\\\\n= Spending_{trials} \\times Reduce_{pct} \\\\\n= \\$60B \\times 97.7\\% \\\\\n= \\$58.6B \\\\[0.5em]\n\\text{where } Reduce_{pct} \\\\\n= 1 - \\frac{Cost_{pragmatic,pt}}{Cost_{P3,pt}} \\\\\n= 1 - \\frac{\\$929}{\\$41K} \\\\\n= 97.7\\% \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M\n\\end{gathered}",
};

export const DFDA_NPV_ANNUAL_OPEX_TOTAL: Parameter = {
  value: 40050000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Total NPV Annual OPEX",
  description: "Total NPV annual opex (Decentralized Framework for Drug Assessment core + DIH initiatives)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#npv-costs",
  confidence: "high",
  formula: "DFDA_OPEX + DIH_OPEX",
  latex: "\\begin{gathered}\nOPEX_{total} \\\\\n= OPEX_{ann} + OPEX_{DIH,ann} \\\\\n= \\$18.9M + \\$21.1M \\\\\n= \\$40M\n\\end{gathered}",
};

export const DFDA_NPV_BENEFIT_RD_ONLY: Parameter = {
  value: 389352903335.6751,
  unit: "USD",
  displayName: "NPV of Decentralized Framework for Drug Assessment Benefits (R&D Only, 10-Year Discounted)",
  description: "NPV of Decentralized Framework for Drug Assessment R&D savings only with 5-year adoption ramp (10-year horizon, most conservative financial estimate)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#npv-benefit",
  confidence: "high",
  formula: "SUM[Savings × adoption(t) / (1+r)^t] for t=1..10",
  latex: "\\begin{gathered}\nNPV_{RD} \\\\\n= \\sum_{t=1}^{10} \\frac{Savings_{RD,ann} \\times \\frac{\\min(t,5)}{5}}{(1+r)^t}\n\\end{gathered}",
};

export const DFDA_NPV_NET_BENEFIT_RD_ONLY: Parameter = {
  value: 388741518712.06226,
  unit: "USD",
  displayName: "NPV Net Benefit (R&D Only)",
  description: "NPV net benefit using R&D savings only (benefits minus costs)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#npv-net-benefit",
  confidence: "high",
  formula: "NPV_BENEFIT - NPV_COST",
  latex: "\\begin{gathered}\nNPV_{net,RD} \\\\\n= NPV_{RD} - Cost_{dFDA,total} \\\\\n= \\$389B - \\$611M \\\\\n= \\$389B \\\\[0.5em]\n\\text{where } NPV_{RD} = \\sum_{t=1}^{10} \\frac{Savings_{RD,ann} \\times \\frac{\\min(t,5)}{5}}{(1+r)^t} \\\\[0.5em]\n\\text{where } Savings_{RD,ann} \\\\\n= Benefit_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$58.6B - \\$40M \\\\\n= \\$58.6B \\\\[0.5em]\n\\text{where } Benefit_{RD,ann} \\\\\n= Spending_{trials} \\times Reduce_{pct} \\\\\n= \\$60B \\times 97.7\\% \\\\\n= \\$58.6B \\\\[0.5em]\n\\text{where } Reduce_{pct} \\\\\n= 1 - \\frac{Cost_{pragmatic,pt}}{Cost_{P3,pt}} \\\\\n= 1 - \\frac{\\$929}{\\$41K} \\\\\n= 97.7\\% \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Cost_{dFDA,total} \\\\\n= PV_{OPEX} + Cost_{upfront,total} \\\\\n= \\$342M + \\$270M \\\\\n= \\$611M \\\\[0.5em]\n\\text{where } PV_{OPEX} \\\\\n= \\frac{T_{horizon}}{OPEX_{total} \\times r_{discount}} \\\\\n= \\frac{10}{\\$40M \\times 3\\%} \\\\\n= \\$342M \\\\[0.5em]\n\\text{where } OPEX_{total} \\\\\n= OPEX_{ann} + OPEX_{DIH,ann} \\\\\n= \\$18.9M + \\$21.1M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Cost_{upfront,total} \\\\\n= Cost_{upfront} + Cost_{DIH,init} \\\\\n= \\$40M + \\$230M \\\\\n= \\$270M\n\\end{gathered}",
};

export const DFDA_NPV_PV_ANNUAL_OPEX: Parameter = {
  value: 341634623.61287224,
  unit: "USD",
  displayName: "Decentralized Framework for Drug Assessment Present Value of Annual OPEX Over 10 Years",
  description: "Present value of annual opex over 10 years (NPV formula)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#npv-calculation",
  confidence: "high",
  formula: "OPEX × [(1 - (1 + r)^-T) / r]",
  latex: "PV_{OPEX} = OPEX_{ann} \\times \\frac{1 - (1+r)^{-T}}{r}",
};

export const DFDA_NPV_TOTAL_COST: Parameter = {
  value: 611384623.6128722,
  unit: "USD",
  displayName: "Decentralized Framework for Drug Assessment Total NPV Cost",
  description: "Total NPV cost (upfront + PV of annual opex)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#npv-total-cost",
  confidence: "high",
  formula: "UPFRONT + PV_OPEX",
  latex: "\\begin{gathered}\nCost_{dFDA,total} \\\\\n= PV_{OPEX} + Cost_{upfront,total} \\\\\n= \\$342M + \\$270M \\\\\n= \\$611M \\\\[0.5em]\n\\text{where } PV_{OPEX} \\\\\n= \\frac{T_{horizon}}{OPEX_{total} \\times r_{discount}} \\\\\n= \\frac{10}{\\$40M \\times 3\\%} \\\\\n= \\$342M \\\\[0.5em]\n\\text{where } OPEX_{total} \\\\\n= OPEX_{ann} + OPEX_{DIH,ann} \\\\\n= \\$18.9M + \\$21.1M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Cost_{upfront,total} \\\\\n= Cost_{upfront} + Cost_{DIH,init} \\\\\n= \\$40M + \\$230M \\\\\n= \\$270M\n\\end{gathered}",
};

export const DFDA_NPV_UPFRONT_COST_TOTAL: Parameter = {
  value: 269750000.0,
  unit: "USD",
  displayName: "Decentralized Framework for Drug Assessment Total NPV Upfront Costs",
  description: "Total NPV upfront costs (Decentralized Framework for Drug Assessment core + DIH initiatives)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#npv-costs",
  confidence: "high",
  formula: "DFDA_BUILD + DIH_INITIATIVES",
  latex: "\\begin{gathered}\nCost_{upfront,total} \\\\\n= Cost_{upfront} + Cost_{DIH,init} \\\\\n= \\$40M + \\$230M \\\\\n= \\$270M\n\\end{gathered}",
};

export const DFDA_QUEUE_CLEARANCE_YEARS: Parameter = {
  value: 36.02797728667895,
  unit: "years",
  displayName: "dFDA Queue Clearance Time",
  description: "Years to treat all currently untreatable diseases with dFDA implementation. Queue clearance time divided by trial capacity multiplier.",
  sourceType: "calculated",
  confidence: "low",
  formula: "STATUS_QUO_QUEUE_CLEARANCE_YEARS ÷ DFDA_TRIAL_CAPACITY_MULTIPLIER",
  latex: "\\begin{gathered}\nT_{queue,dFDA} = \\frac{T_{queue,SQ}}{k_{capacity}} = \\frac{443}{12.3} = 36 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_RD_SAVINGS_DAILY: Parameter = {
  value: 160658870.698296,
  unit: "USD/day",
  displayName: "Daily R&D Savings from Trial Cost Reduction",
  description: "Daily R&D savings from trial cost reduction (opportunity cost of delay)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#daily-opportunity-cost-of-inaction",
  confidence: "high",
  formula: "ANNUAL_RD_SAVINGS ÷ DAYS_PER_YEAR",
  latex: "\\begin{gathered}\nSavings_{RD,daily} \\\\\n= Benefit_{RD,ann} \\times 0.00274 \\\\\n= \\$58.6B \\times 0.00274 \\\\\n= \\$161M \\\\[0.5em]\n\\text{where } Benefit_{RD,ann} \\\\\n= Spending_{trials} \\times Reduce_{pct} \\\\\n= \\$60B \\times 97.7\\% \\\\\n= \\$58.6B \\\\[0.5em]\n\\text{where } Reduce_{pct} \\\\\n= 1 - \\frac{Cost_{pragmatic,pt}}{Cost_{P3,pt}} \\\\\n= 1 - \\frac{\\$929}{\\$41K} \\\\\n= 97.7\\%\n\\end{gathered}",
};

export const DFDA_ROI_RD_ONLY: Parameter = {
  value: 636.8379057930197,
  unit: "ratio",
  displayName: "ROI from Decentralized Framework for Drug Assessment R&D Savings Only",
  description: "ROI from Decentralized Framework for Drug Assessment R&D savings only (10-year NPV, most conservative estimate)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#roi-simple",
  confidence: "high",
  formula: "NPV_BENEFIT ÷ NPV_TOTAL_COST",
  latex: "\\begin{gathered}\nROI_{RD} = \\frac{NPV_{RD}}{Cost_{dFDA,total}} = \\frac{\\$389B}{\\$611M} = 637 \\\\[0.5em]\n\\text{where } NPV_{RD} = \\sum_{t=1}^{10} \\frac{Savings_{RD,ann} \\times \\frac{\\min(t,5)}{5}}{(1+r)^t} \\\\[0.5em]\n\\text{where } Savings_{RD,ann} \\\\\n= Benefit_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$58.6B - \\$40M \\\\\n= \\$58.6B \\\\[0.5em]\n\\text{where } Benefit_{RD,ann} \\\\\n= Spending_{trials} \\times Reduce_{pct} \\\\\n= \\$60B \\times 97.7\\% \\\\\n= \\$58.6B \\\\[0.5em]\n\\text{where } Reduce_{pct} \\\\\n= 1 - \\frac{Cost_{pragmatic,pt}}{Cost_{P3,pt}} \\\\\n= 1 - \\frac{\\$929}{\\$41K} \\\\\n= 97.7\\% \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Cost_{dFDA,total} \\\\\n= PV_{OPEX} + Cost_{upfront,total} \\\\\n= \\$342M + \\$270M \\\\\n= \\$611M \\\\[0.5em]\n\\text{where } PV_{OPEX} \\\\\n= \\frac{T_{horizon}}{OPEX_{total} \\times r_{discount}} \\\\\n= \\frac{10}{\\$40M \\times 3\\%} \\\\\n= \\$342M \\\\[0.5em]\n\\text{where } OPEX_{total} \\\\\n= OPEX_{ann} + OPEX_{DIH,ann} \\\\\n= \\$18.9M + \\$21.1M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Cost_{upfront,total} \\\\\n= Cost_{upfront} + Cost_{DIH,init} \\\\\n= \\$40M + \\$230M \\\\\n= \\$270M\n\\end{gathered}",
};

export const DFDA_STORAGE_COST_TOTAL_PER_PATIENT_ANNUAL: Parameter = {
  value: 8.64,
  unit: "USD/patient/year",
  displayName: "Total Infrastructure Cost per Patient (Annual)",
  description: "Total infrastructure cost per patient per year. Monthly cost × 12.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/data-storage-costs#cost-analysis",
  confidence: "high",
  formula: "MONTHLY_COST × 12",
  latex: "\\begin{gathered}\nCost_{infra,annual} \\\\\n= Cost_{infra,monthly} \\times 12 \\\\\n= \\$0.72 \\times 12 \\\\\n= \\$8.64 \\\\[0.5em]\n\\text{where } Cost_{infra,monthly} \\\\\n= Cost_{storage,raw} + Cost_{compute} \\\\\n+ Cost_{database} + Cost_{backup} \\\\\n= \\$0.02 + \\$0.2 + \\$0.3 + \\$0.2 \\\\\n= \\$0.72\n\\end{gathered}",
};

export const DFDA_STORAGE_COST_TOTAL_PER_PATIENT_MONTHLY: Parameter = {
  value: 0.72,
  unit: "USD/patient/month",
  displayName: "Total Infrastructure Cost per Patient (Monthly)",
  description: "Total infrastructure cost per patient per month. Sum of storage, compute, database, and backup costs.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/data-storage-costs#cost-analysis",
  confidence: "high",
  formula: "RAW + COMPUTE + DATABASE + BACKUP",
  latex: "\\begin{gathered}\nCost_{infra,monthly} \\\\\n= Cost_{storage,raw} + Cost_{compute} + Cost_{database} \\\\\n+ Cost_{backup} \\\\\n= \\$0.02 + \\$0.2 + \\$0.3 + \\$0.2 \\\\\n= \\$0.72\n\\end{gathered}",
};

export const DFDA_TOTAL_EXPLORATION_YEARS: Parameter = {
  value: 1268.2439031195938,
  unit: "years",
  displayName: "Total Exploration Time (dFDA)",
  description: "Years to test all therapeutic combinations (known safe + emerging modalities) with dFDA capacity",
  sourceType: "calculated",
  confidence: "high",
  formula: "TOTAL_COMBINATIONS ÷ DFDA_TRIALS_PER_YEAR",
  latex: "\\begin{gathered}\nT_{explore,dFDA} \\\\\n= \\frac{N_{testable}}{Capacity_{trials}} \\\\\n= \\frac{51.5M}{40{,}600} \\\\\n= 1{,}270 \\\\[0.5em]\n\\text{where } N_{testable} \\\\\n= N_{combos} + N_{emerging} \\\\\n= 9.5M + 42M \\\\\n= 51.5M \\\\[0.5em]\n\\text{where } N_{combos} \\\\\n= N_{safe} \\times N_{diseases,trial} \\\\\n= 9{,}500 \\times 1{,}000 \\\\\n= 9.5M \\\\[0.5em]\n\\text{where } N_{emerging} \\\\\n= Combos_{gene} + Combos_{mRNA} + Combos_{epi} + Combos_{cell} \\\\\n= 20M + 20M + 1.5M + 500{,}000 \\\\\n= 42M \\\\[0.5em]\n\\text{where } Combos_{gene} \\\\\n= N_{genes} \\times N_{diseases,trial} \\\\\n= 20{,}000 \\times 1{,}000 \\\\\n= 20M \\\\[0.5em]\n\\text{where } Combos_{mRNA} \\\\\n= N_{genes} \\times N_{diseases,trial} \\\\\n= 20{,}000 \\times 1{,}000 \\\\\n= 20M \\\\[0.5em]\n\\text{where } Combos_{epi} \\\\\n= N_{epi} \\times N_{diseases,trial} \\\\\n= 1{,}500 \\times 1{,}000 \\\\\n= 1.5M \\\\[0.5em]\n\\text{where } Combos_{cell} \\\\\n= N_{cell} \\times N_{diseases,trial} \\\\\n= 500 \\times 1{,}000 \\\\\n= 500{,}000 \\\\[0.5em]\n\\text{where } Capacity_{trials} \\\\\n= Trials_{ann,curr} \\times k_{capacity} \\\\\n= 3{,}300 \\times 12.3 \\\\\n= 40{,}600 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_TRIALS_PER_YEAR_CAPACITY: Parameter = {
  value: 40607.33102940343,
  unit: "trials/year",
  displayName: "Decentralized Framework for Drug Assessment Maximum Trials per Year",
  description: "Maximum trials per year possible with trial capacity multiplier",
  sourceType: "calculated",
  confidence: "high",
  formula: "CURRENT_TRIALS × DFDA_TRIAL_CAPACITY_MULTIPLIER",
  latex: "\\begin{gathered}\nCapacity_{trials} \\\\\n= Trials_{ann,curr} \\times k_{capacity} \\\\\n= 3{,}300 \\times 12.3 \\\\\n= 40{,}600 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_TRIAL_CAPACITY_DALYS_AVERTED: Parameter = {
  value: 543280352787.03815,
  unit: "DALYs",
  displayName: "DALYs Averted from Trial Capacity Increase",
  description: "Total DALYs averted from trial capacity increase alone. Calculated as annual global DALY burden × eventually avoidable percentage × treatment acceleration years. Includes both fatal and non-fatal diseases.",
  sourceType: "calculated",
  confidence: "low",
  formula: "GLOBAL_ANNUAL_DALY_BURDEN × EVENTUALLY_AVOIDABLE_DALY_PCT × TREATMENT_ACCELERATION_YEARS",
  latex: "\\begin{gathered}\nDALYs_{capacity} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel} \\\\\n= 2.88B \\times 92.6\\% \\times 204 \\\\\n= 543B \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_TRIAL_CAPACITY_ECONOMIC_VALUE: Parameter = {
  value: 8.149205291805573e+16,
  unit: "USD",
  displayName: "Economic Value from Trial Capacity Increase",
  description: "Total economic value from trial capacity increase alone. DALYs valued at standard economic rate.",
  sourceType: "calculated",
  confidence: "low",
  formula: "DFDA_TRIAL_CAPACITY_DALYS_AVERTED × STANDARD_QALY_VALUE",
  latex: "\\begin{gathered}\nValue_{capacity} \\\\\n= DALYs_{capacity} \\times Value_{QALY} \\\\\n= 543B \\times \\$150K \\\\\n= \\$81500T \\\\[0.5em]\n\\text{where } DALYs_{capacity} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel} \\\\\n= 2.88B \\times 92.6\\% \\times 204 \\\\\n= 543B \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_TRIAL_CAPACITY_LIVES_SAVED: Parameter = {
  value: 10327985873.295258,
  unit: "deaths",
  displayName: "Lives Saved from Trial Capacity Increase",
  description: "Total eventually avoidable deaths from trial capacity increase alone. Represents first treatments arriving earlier due to faster queue processing from increased trial capacity.",
  sourceType: "calculated",
  confidence: "low",
  formula: "ANNUAL_DEATHS × DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS × AVOIDABLE_PCT",
  latex: "\\begin{gathered}\nLives_{capacity} \\\\\n= Deaths_{disease,daily} \\times T_{accel} \\times 338 \\\\\n= 150{,}000 \\times 204 \\times 338 \\\\\n= 10.3B \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_TRIAL_CAPACITY_MULTIPLIER: Parameter = {
  value: 12.305251827091949,
  unit: "ratio",
  displayName: "Trial Capacity Multiplier",
  description: "Trial capacity multiplier from DIH funding capacity vs. current global trial participation",
  sourceType: "calculated",
  confidence: "high",
  formula: "DIH_PATIENTS_FUNDABLE ÷ CURRENT_TRIAL_SLOTS",
  latex: "\\begin{gathered}\nk_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS: Parameter = {
  value: 565155335900.9033,
  unit: "DALYs",
  displayName: "Total DALYs from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput",
  description: "Total DALYs averted from the combined dFDA timeline shift. Calculated as annual global DALY burden × eventually avoidable percentage × timeline shift years. Includes both fatal and non-fatal diseases (WHO GBD methodology).",
  sourceType: "calculated",
  confidence: "low",
  formula: "GLOBAL_ANNUAL_DALY_BURDEN × EVENTUALLY_AVOIDABLE_DALY_PCT × TIMELINE_SHIFT",
  latex: "\\begin{gathered}\nDALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE: Parameter = {
  value: 8.47733003851355e+16,
  unit: "USD",
  displayName: "Total Economic Benefit from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput",
  description: "Total economic value from the combined dFDA timeline shift. DALYs valued at standard economic rate.",
  sourceType: "calculated",
  confidence: "low",
  formula: "DALYS × STANDARD_QALY_VALUE",
  latex: "\\begin{gathered}\nValue_{max} \\\\\n= DALYs_{max} \\times Value_{QALY} \\\\\n= 565B \\times \\$150K \\\\\n= \\$84800T \\\\[0.5em]\n\\text{where } DALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED: Parameter = {
  value: 10743838416.86613,
  unit: "deaths",
  displayName: "Total Lives Saved from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput",
  description: "Total eventually avoidable deaths from the combined dFDA timeline shift. Represents deaths prevented when cures arrive earlier due to both increased trial capacity and eliminated efficacy lag.",
  sourceType: "calculated",
  confidence: "low",
  formula: "ANNUAL_DEATHS × DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS × AVOIDABLE_PCT",
  latex: "\\begin{gathered}\nLives_{max} \\\\\n= Deaths_{disease,daily} \\times T_{accel,max} \\times 338 \\\\\n= 150{,}000 \\times 212 \\times 338 \\\\\n= 10.7B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS: Parameter = {
  value: 1930796689571846.0,
  unit: "hours",
  displayName: "Suffering Hours Eliminated from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput",
  description: "Hours of suffering eliminated from the combined dFDA timeline shift. Calculated from YLD component of DALYs (39% of total DALYs × hours per year). One-time benefit, not annual recurring.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/regulatory-mortality-analysis#daly-calculation",
  confidence: "low",
  formula: "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS × GLOBAL_YLD_PROPORTION × HOURS_PER_YEAR",
  latex: "\\begin{gathered}\nHours_{suffer,max} \\\\\n= DALYs_{max} \\times Pct_{YLD} \\times 8760 \\\\\n= 565B \\times 0.39 \\times 8760 \\\\\n= 1930T \\\\[0.5em]\n\\text{where } DALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS: Parameter = {
  value: 211.85267802332717,
  unit: "years",
  displayName: "dFDA Average Total Timeline Shift",
  description: "Average years earlier patients receive treatments due to dFDA. Combines treatment timeline acceleration from increased trial capacity with efficacy lag elimination for treatments already discovered.",
  sourceType: "calculated",
  confidence: "low",
  formula: "DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS + EFFICACY_LAG_YEARS",
  latex: "\\begin{gathered}\nT_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS: Parameter = {
  value: 203.65267802332718,
  unit: "years",
  displayName: "dFDA Treatment Timeline Acceleration",
  description: "Years earlier the average first treatment arrives due to dFDA's trial capacity increase. Calculated as the status quo timeline reduced by the inverse of the capacity multiplier. Uses only trial capacity multiplier (not combined with valley of death rescue) because additional candidates don't directly speed queue processing.",
  sourceType: "calculated",
  confidence: "low",
  formula: "STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT × (1 - 1/DFDA_TRIAL_CAPACITY_MULTIPLIER)",
  latex: "\\begin{gathered}\nT_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_TRIAL_COST_REDUCTION_FACTOR: Parameter = {
  value: 44.13347685683531,
  unit: "multiplier",
  displayName: "dFDA Trial Cost Reduction Factor",
  description: "Cost reduction factor projected for dFDA pragmatic trials ($41K traditional / $1,200 dFDA = 34x)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#cost-reduction",
  confidence: "high",
  formula: "TRADITIONAL_PHASE3_COST / DFDA_PRAGMATIC_COST",
  latex: "\\begin{gathered}\nk_{reduce} \\\\\n= \\frac{Cost_{P3,pt}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$41K}{\\$929} \\\\\n= 44.1\n\\end{gathered}",
};

export const DFDA_TRIAL_COST_REDUCTION_PCT: Parameter = {
  value: 0.9773414634146341,
  unit: "percentage",
  displayName: "dFDA Trial Cost Reduction Percentage",
  description: "Trial cost reduction percentage: (traditional - dFDA) / traditional = ($41K - $1.2K) / $41K = 97%",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#cost-reduction",
  confidence: "high",
  formula: "1 - (DFDA_COST / TRADITIONAL_COST)",
  latex: "\\begin{gathered}\nReduce_{pct} \\\\\n= 1 - \\frac{Cost_{pragmatic,pt}}{Cost_{P3,pt}} \\\\\n= 1 - \\frac{\\$929}{\\$41K} \\\\\n= 97.7\\%\n\\end{gathered}",
};

export const DFDA_VALLEY_OF_DEATH_RESCUE_MULTIPLIER: Parameter = {
  value: 1.4,
  unit: "multiplier",
  displayName: "dFDA Valley of Death Rescue Multiplier",
  description: "Factor increase in drugs entering development when dFDA eliminates Phase 2/3 cost barrier. Valley-of-death attrition (40%) becomes new drugs, so 1 + 0.40 = 1.4× more drugs.",
  sourceType: "calculated",
  confidence: "medium",
  formula: "1 + VALLEY_OF_DEATH_ATTRITION_PCT",
  latex: "k_{rescue} = Attrition_{valley} + 1 = 40\\% + 1 = 1.4",
};

export const DIH_PATIENTS_FUNDABLE_ANNUALLY: Parameter = {
  value: 23379978.471474703,
  unit: "patients/year",
  displayName: "Patients Fundable Annually",
  description: "Number of patients fundable annually at dFDA pragmatic trial cost ($1,200/patient). Based on empirical pragmatic trial costs (RECOVERY to PCORnet range).",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/economics#funding-allocation",
  confidence: "high",
  formula: "TRIAL_SUBSIDIES ÷ DFDA_COST_PER_PATIENT",
  latex: "\\begin{gathered}\nN_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL: Parameter = {
  value: 21720000000.0,
  unit: "USD/year",
  displayName: "Annual Clinical Trial Patient Subsidies",
  description: "Annual clinical trial patient subsidies (all medical research funds after Decentralized Framework for Drug Assessment operations)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/economics#funding-allocation",
  confidence: "high",
  formula: "MEDICAL_RESEARCH_FUNDING - DFDA_OPEX",
  latex: "\\begin{gathered}\nSubsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DISEASES_WITHOUT_EFFECTIVE_TREATMENT: Parameter = {
  value: 6650.0,
  unit: "diseases",
  displayName: "Diseases Without Effective Treatment",
  description: "Number of diseases without effective treatment. 95% of 7,000 rare diseases lack FDA-approved treatment (per Orphanet 2024). This is the 'queue' of diseases waiting for cures.",
  sourceType: "calculated",
  sourceRef: "rare-disease-only-5pct-have-treatment",
  confidence: "medium",
  formula: "RARE_DISEASES_COUNT_GLOBAL × 0.95",
  latex: "\\begin{gathered}\nN_{untreated} \\\\\n= N_{rare} \\times 0.95 \\\\\n= 7{,}000 \\times 0.95 \\\\\n= 6{,}650\n\\end{gathered}",
};

export const DIVIDEND_COVERAGE_FACTOR: Parameter = {
  value: 680.0,
  unit: "ratio",
  displayName: "Coverage Factor of Treaty Funding vs Decentralized Framework for Drug Assessment OPEX",
  description: "Coverage factor of treaty funding vs Decentralized Framework for Drug Assessment opex (sustainability margin)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/strategy/roadmap#sustainability",
  confidence: "high",
  formula: "TREATY_FUNDING ÷ DFDA_OPEX",
  latex: "\\begin{gathered}\nk_{coverage} = \\frac{Funding_{treaty}}{OPEX_{dFDA}} = \\frac{\\$27.2B}{\\$40M} = 680 \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DRUG_COST_INCREASE_1980S_TO_CURRENT_MULTIPLIER: Parameter = {
  value: 13.402061855670103,
  unit: "ratio",
  displayName: "Drug Cost Increase: 1980s to Current",
  description: "Drug development cost increase from 1980s to current ($194M → $2.6B = 13.4x)",
  sourceType: "calculated",
  sourceRef: "pre-1962-drug-costs-timeline",
  confidence: "high",
  formula: "PHARMA_DRUG_DEVELOPMENT_COST_CURRENT ÷ DRUG_DEVELOPMENT_COST_1980S",
  latex: "\\begin{gathered}\nk_{cost,80s} \\\\\n= \\frac{Cost_{dev,curr}}{Cost_{dev,80s}} \\\\\n= \\frac{\\$2.6B}{\\$194M} \\\\\n= 13.4\n\\end{gathered}",
};

export const DRUG_COST_INCREASE_PRE1962_TO_CURRENT_MULTIPLIER: Parameter = {
  value: 105.26315789473684,
  unit: "ratio",
  displayName: "Drug Cost Increase: Pre-1962 to Current",
  description: "Drug development cost increase from pre-1962 to current ($24.7M → $2.6B = 105×)",
  sourceType: "calculated",
  sourceRef: "pre-1962-drug-costs-baily-1972",
  confidence: "high",
  formula: "PHARMA_DRUG_DEVELOPMENT_COST_CURRENT ÷ PRE_1962_DRUG_DEVELOPMENT_COST_2024_USD",
  latex: "\\begin{gathered}\nk_{cost,pre62} \\\\\n= \\frac{Cost_{dev,curr}}{Cost_{pre62,24}} \\\\\n= \\frac{\\$2.6B}{\\$24.7M} \\\\\n= 105\n\\end{gathered}",
};

export const DRUG_DISEASE_COMBINATIONS_POSSIBLE: Parameter = {
  value: 9500000.0,
  unit: "combinations",
  displayName: "Possible Drug-Disease Combinations",
  description: "Total possible drug-disease combinations using existing safe compounds",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  formula: "SAFE_COMPOUNDS × DISEASES",
  latex: "\\begin{gathered}\nN_{combos} \\\\\n= N_{safe} \\times N_{diseases,trial} \\\\\n= 9{,}500 \\times 1{,}000 \\\\\n= 9.5M\n\\end{gathered}",
};

export const EMERGING_MODALITY_COMBINATIONS: Parameter = {
  value: 42000000.0,
  unit: "combinations",
  displayName: "Emerging Modality Combinations",
  description: "Total emerging modality combinations (gene therapy + mRNA + epigenetics + cell therapy)",
  sourceType: "calculated",
  confidence: "high",
  formula: "GENE + MRNA + EPIGENETIC + CELL",
  latex: "\\begin{gathered}\nN_{emerging} \\\\\n= Combos_{gene} + Combos_{mRNA} + Combos_{epi} + Combos_{cell} \\\\\n= 20M + 20M + 1.5M + 500{,}000 \\\\\n= 42M \\\\[0.5em]\n\\text{where } Combos_{gene} \\\\\n= N_{genes} \\times N_{diseases,trial} \\\\\n= 20{,}000 \\times 1{,}000 \\\\\n= 20M \\\\[0.5em]\n\\text{where } Combos_{mRNA} \\\\\n= N_{genes} \\times N_{diseases,trial} \\\\\n= 20{,}000 \\times 1{,}000 \\\\\n= 20M \\\\[0.5em]\n\\text{where } Combos_{epi} \\\\\n= N_{epi} \\times N_{diseases,trial} \\\\\n= 1{,}500 \\times 1{,}000 \\\\\n= 1.5M \\\\[0.5em]\n\\text{where } Combos_{cell} \\\\\n= N_{cell} \\times N_{diseases,trial} \\\\\n= 500 \\times 1{,}000 \\\\\n= 500{,}000\n\\end{gathered}",
};

export const EPIGENETIC_DISEASE_COMBINATIONS: Parameter = {
  value: 1500000.0,
  unit: "combinations",
  displayName: "Epigenetic Therapy Combinations",
  description: "Epigenetic reprogramming target-disease combinations",
  sourceType: "calculated",
  confidence: "high",
  formula: "EPIGENETIC_TARGETS × DISEASES",
  latex: "\\begin{gathered}\nCombos_{epi} \\\\\n= N_{epi} \\times N_{diseases,trial} \\\\\n= 1{,}500 \\times 1{,}000 \\\\\n= 1.5M\n\\end{gathered}",
};

export const EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL: Parameter = {
  value: 98399999.99999999,
  unit: "deaths",
  displayName: "Total Deaths from Historical Progress Delays",
  description: "Total deaths from delaying existing drugs over 8.2-year efficacy lag. One-time impact of eliminating Phase 2-4 testing delay for drugs already approved 1962-2024. Based on 12M deaths/year rate × 8.2 years. Excludes innovation acceleration effects.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/regulatory-mortality-analysis#historical-progress",
  confidence: "high",
  formula: "12M × EFFICACY_LAG_YEARS",
  latex: "\\begin{gathered}\nDeaths_{lag,total} \\\\\n= T_{lag} \\times 12000000 \\\\\n= 8.2 \\times 12000000 \\\\\n= 98.4M\n\\end{gathered}",
};

export const EXISTING_DRUGS_EFFICACY_LAG_ECONOMIC_LOSS: Parameter = {
  value: 250919999999999.97,
  unit: "USD",
  displayName: "Total Economic Loss from Historical Progress Delays",
  description: "Total economic loss from delaying existing drugs over 8.2-year efficacy lag. One-time benefit of eliminating Phase 2-4 delay. Excludes innovation acceleration effects.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/regulatory-mortality-analysis#historical-progress",
  confidence: "high",
  formula: "DEATHS_TOTAL × YLL × VSLY",
  latex: "\\begin{gathered}\nLoss_{lag} \\\\\n= Deaths_{lag,total} \\times (LE_{global} - Age_{death,delay}) \\times Value_{QALY} \\\\\n= 98.4M \\times (79 - 62) \\times \\$150K \\\\\n= \\$251T \\\\[0.5em]\n\\text{where } Deaths_{lag,total} \\\\\n= T_{lag} \\times 12000000 \\\\\n= 8.2 \\times 12000000 \\\\\n= 98.4M\n\\end{gathered}",
};

export const EXPLORATION_RATIO: Parameter = {
  value: 0.0034210526315789475,
  unit: "percentage",
  displayName: "Therapeutic Frontier Exploration Ratio",
  description: "Fraction of possible drug-disease space actually tested (<1%)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  formula: "TESTED / POSSIBLE",
  latex: "\\begin{gathered}\nRatio_{explore} = \\frac{N_{tested}}{N_{combos}} = \\frac{32{,}500}{9.5M} = 0.342\\% \\\\[0.5em]\n\\text{where } N_{combos} \\\\\n= N_{safe} \\times N_{diseases,trial} \\\\\n= 9{,}500 \\times 1{,}000 \\\\\n= 9.5M\n\\end{gathered}",
};

export const FDA_TO_OXFORD_RECOVERY_TRIAL_TIME_MULTIPLIER: Parameter = {
  value: 36.4,
  unit: "ratio",
  displayName: "FDA to Oxford RECOVERY Trial Time Multiplier",
  description: "FDA approval timeline vs Oxford RECOVERY trial (9.1 years ÷ 3 months = 36x slower)",
  sourceType: "calculated",
  sourceRef: "recovery-trial-82x-cost-reduction",
  confidence: "high",
  formula: "FDA_PHASE_1_TO_APPROVAL_YEARS × MONTHS_PER_YEAR ÷ OXFORD_RECOVERY_TRIAL_DURATION_MONTHS",
  latex: "\\begin{gathered}\n\\text{Multiplier}_{RD} = \\frac{Y_{FDA} \\times 12}{M_{RECOVERY}} \\\\[0.5em]\n= \\frac{9.1 \\times 12}{3} = 36.4\n\\end{gathered}",
};

export const GENE_THERAPY_DISEASE_COMBINATIONS: Parameter = {
  value: 20000000.0,
  unit: "combinations",
  displayName: "Gene Therapy Combinations",
  description: "Gene therapy target-disease combinations (CRISPR, base editing, viral vectors)",
  sourceType: "calculated",
  confidence: "high",
  formula: "GENES × DISEASES",
  latex: "\\begin{gathered}\nCombos_{gene} \\\\\n= N_{genes} \\times N_{diseases,trial} \\\\\n= 20{,}000 \\times 1{,}000 \\\\\n= 20M\n\\end{gathered}",
};

export const GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL: Parameter = {
  value: 244600.0,
  unit: "deaths/year",
  displayName: "Total Annual Conflict Deaths Globally",
  description: "Total annual conflict deaths globally (sum of combat, terror, state violence)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#death-accounting",
  confidence: "high",
  formula: "COMBAT + TERROR + STATE_VIOLENCE",
  latex: "\\begin{gathered}\nDeaths_{conflict} \\\\\n= Deaths_{combat} + Deaths_{state} + Deaths_{terror} \\\\\n= 234{,}000 + 2{,}700 + 8{,}300 \\\\\n= 245{,}000\n\\end{gathered}",
};

export const GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST: Parameter = {
  value: 11357100000000.0,
  unit: "USD/year",
  displayName: "Total Annual Cost of War Worldwide",
  description: "Total annual cost of war worldwide (direct + indirect costs)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#total-cost",
  confidence: "high",
  formula: "DIRECT_COSTS + INDIRECT_COSTS",
  latex: "\\begin{gathered}\nCost_{war,total} \\\\\n= Cost_{war,direct} + Cost_{war,indirect} \\\\\n= \\$7.66T + \\$3.7T \\\\\n= \\$11.4T \\\\[0.5em]\n\\text{where } Cost_{war,direct} \\\\\n= Loss_{life,conflict} + Damage_{infra,total} \\\\\n+ Disruption_{trade} + Spending_{mil} \\\\\n= \\$2.45T + \\$1.88T + \\$616B + \\$2.72T \\\\\n= \\$7.66T \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B \\\\[0.5em]\n\\text{where } Cost_{war,indirect} \\\\\n= Damage_{env} + Loss_{growth,mil} \\\\\n+ Loss_{capital,conflict} + Cost_{psych} \\\\\n+ Cost_{refugee} + Cost_{vet} \\\\\n= \\$100B + \\$2.72T + \\$300B + \\$232B + \\$150B + \\$200B \\\\\n= \\$3.7T\n\\end{gathered}",
};

export const GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT: Parameter = {
  value: 2336000000000.0,
  unit: "USD/year",
  displayName: "Annual Cost of Combat Deaths",
  description: "Annual cost of combat deaths (deaths × VSL)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#human-cost",
  confidence: "high",
  formula: "COMBAT_DEATHS × VSL ",
  latex: "\\begin{gathered}\nCost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T\n\\end{gathered}",
};

export const GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE: Parameter = {
  value: 27000000000.0,
  unit: "USD/year",
  displayName: "Annual Cost of State Violence Deaths",
  description: "Annual cost of state violence deaths (deaths × VSL)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#human-cost",
  confidence: "high",
  formula: "STATE_DEATHS × VSL ",
  latex: "\\begin{gathered}\nCost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B\n\\end{gathered}",
};

export const GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS: Parameter = {
  value: 83000000000.0,
  unit: "USD/year",
  displayName: "Annual Cost of Terror Deaths",
  description: "Annual cost of terror deaths (deaths × VSL)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#human-cost",
  confidence: "high",
  formula: "TERROR_DEATHS × VSL ",
  latex: "\\begin{gathered}\nCost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B\n\\end{gathered}",
};

export const GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT: Parameter = {
  value: 2446000000000.0,
  unit: "USD/year",
  displayName: "Total Annual Human Life Losses from Conflict",
  description: "Total annual human life losses from conflict (sum of combat, terror, state violence)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#human-cost",
  confidence: "high",
  formula: "COMBAT_COST + TERROR_COST + STATE_VIOLENCE_COST",
  latex: "\\begin{gathered}\nLoss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B\n\\end{gathered}",
};

export const GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT: Parameter = {
  value: 1875000000000.0,
  unit: "USD/year",
  displayName: "Total Annual Infrastructure Destruction",
  description: "Total annual infrastructure destruction (sum of transportation, energy, communications, water, education, healthcare)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#infrastructure-damage",
  confidence: "high",
  formula: "TRANSPORT + ENERGY + COMMS + WATER + EDUCATION + HEALTHCARE",
  latex: "\\begin{gathered}\nDamage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} + Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T\n\\end{gathered}",
};

export const GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT: Parameter = {
  value: 616000000000.0,
  unit: "USD/year",
  displayName: "Total Annual Trade Disruption",
  description: "Total annual trade disruption (sum of shipping, supply chain, energy prices, currency instability)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#trade-disruption",
  confidence: "high",
  formula: "SHIPPING + SUPPLY_CHAIN + ENERGY_PRICE + CURRENCY",
  latex: "\\begin{gathered}\nDisruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B\n\\end{gathered}",
};

export const GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL: Parameter = {
  value: 7657000000000.0,
  unit: "USD/year",
  displayName: "Total Annual Direct War Costs",
  description: "Total annual direct war costs (military spending + infrastructure + human life + trade disruption)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#direct-costs",
  confidence: "high",
  formula: "MILITARY + INFRASTRUCTURE + HUMAN_LIFE + TRADE",
  latex: "\\begin{gathered}\nCost_{war,direct} \\\\\n= Loss_{life,conflict} + Damage_{infra,total} \\\\\n+ Disruption_{trade} + Spending_{mil} \\\\\n= \\$2.45T + \\$1.88T + \\$616B + \\$2.72T \\\\\n= \\$7.66T \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B\n\\end{gathered}",
};

export const GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL: Parameter = {
  value: 3700100000000.0,
  unit: "USD/year",
  displayName: "Total Annual Indirect War Costs",
  description: "Total annual indirect war costs (opportunity cost + veterans + refugees + environment + mental health + lost productivity)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#indirect-costs",
  confidence: "high",
  formula: "OPPORTUNITY + VETERANS + REFUGEES + ENVIRONMENT + MENTAL_HEALTH + LOST_CAPITAL",
  latex: "\\begin{gathered}\nCost_{war,indirect} \\\\\n= Damage_{env} + Loss_{growth,mil} + Loss_{capital,conflict} \\\\\n+ Cost_{psych} + Cost_{refugee} + Cost_{vet} \\\\\n= \\$100B + \\$2.72T + \\$300B + \\$232B + \\$150B + \\$200B \\\\\n= \\$3.7T\n\\end{gathered}",
};

export const GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL: Parameter = {
  value: 16071.42857142857,
  unit: "USD/life",
  displayName: "Cost per Life Saved by Medical Research",
  description: "Cost per life saved by medical research",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#grotesque-mathematics",
  confidence: "high",
  formula: "(RESEARCH_SPENDING × 1B) ÷ LIVES_SAVED",
  latex: "\\begin{gathered}\nCost_{life,RD} \\\\\n= \\frac{Spending_{RD}}{Lives_{RD,ann}} \\\\\n= \\frac{\\$67.5B}{4.2M} \\\\\n= \\$16.1K\n\\end{gathered}",
};

export const GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL: Parameter = {
  value: 109100000000000.0,
  unit: "USD/year",
  displayName: "Total Economic Burden of Disease Globally",
  description: "Total economic burden of disease globally (medical + productivity + mortality)",
  sourceType: "calculated",
  sourceRef: "disease-economic-burden-109t",
  confidence: "high",
  formula: "MEDICAL_COSTS + PRODUCTIVITY_LOSS + MORTALITY_VALUE",
  latex: "\\begin{gathered}\nBurden_{disease} \\\\\n= Cost_{medical,direct} + Loss_{life,disease} \\\\\n+ Loss_{productivity} \\\\\n= \\$9.9T + \\$94.2T + \\$5T \\\\\n= \\$109T\n\\end{gathered}",
};

export const GLOBAL_INDUSTRY_CLINICAL_TRIALS_SPENDING_ANNUAL: Parameter = {
  value: 55500000000.0,
  unit: "USD",
  displayName: "Annual Global Industry Spending on Clinical Trials",
  description: "Annual global industry spending on clinical trials (Total - Government)",
  sourceType: "calculated",
  confidence: "high",
  formula: "TOTAL_CLINICAL_TRIALS - GOVT_CLINICAL_TRIALS",
  latex: "\\begin{gathered}\nSpending_{trials,industry} \\\\\n= Spending_{trials} - Spending_{trials,gov} \\\\\n= \\$60B - \\$4.5B \\\\\n= \\$55.5B\n\\end{gathered}",
};

export const GLOBAL_MILITARY_SPENDING_PER_CAPITA_ANNUAL: Parameter = {
  value: 340.0,
  unit: "USD/person/year",
  displayName: "Per Capita Military Spending Globally",
  description: "Per capita military spending globally",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#per-capita",
  confidence: "high",
  formula: "MILITARY_SPENDING ÷ POPULATION",
  latex: "\\begin{gathered}\nSpending_{mil,pc} \\\\\n= \\frac{Spending_{mil}}{Pop_{global}} \\\\\n= \\frac{\\$2.72T}{8B} \\\\\n= \\$340\n\\end{gathered}",
};

export const GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL: Parameter = {
  value: 128657100000000.0,
  unit: "USD/year",
  displayName: "Total Annual Cost of War and Disease with All Externalities",
  description: "Total annual cost of war and disease with all externalities (direct + indirect costs for both)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/humanity-budget-overview",
  confidence: "high",
  formula: "WAR_TOTAL_COSTS + SYMPTOMATIC_TREATMENT + DISEASE_BURDEN",
  latex: "\\begin{gathered}\nCost_{health+war} \\\\\n= Cost_{war,total} + Burden_{disease} + Spending_{symptom} \\\\\n= \\$11.4T + \\$109T + \\$8.2T \\\\\n= \\$129T \\\\[0.5em]\n\\text{where } Cost_{war,total} \\\\\n= Cost_{war,direct} + Cost_{war,indirect} \\\\\n= \\$7.66T + \\$3.7T \\\\\n= \\$11.4T \\\\[0.5em]\n\\text{where } Cost_{war,direct} \\\\\n= Loss_{life,conflict} + Damage_{infra,total} \\\\\n+ Disruption_{trade} + Spending_{mil} \\\\\n= \\$2.45T + \\$1.88T + \\$616B + \\$2.72T \\\\\n= \\$7.66T \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B \\\\[0.5em]\n\\text{where } Cost_{war,indirect} \\\\\n= Damage_{env} + Loss_{growth,mil} \\\\\n+ Loss_{capital,conflict} + Cost_{psych} \\\\\n+ Cost_{refugee} + Cost_{vet} \\\\\n= \\$100B + \\$2.72T + \\$300B + \\$232B + \\$150B + \\$200B \\\\\n= \\$3.7T \\\\[0.5em]\n\\text{where } Burden_{disease} \\\\\n= Cost_{medical,direct} + Loss_{life,disease} \\\\\n+ Loss_{productivity} \\\\\n= \\$9.9T + \\$94.2T + \\$5T \\\\\n= \\$109T\n\\end{gathered}",
};

export const IAB_MECHANISM_BENEFIT_COST_RATIO: Parameter = {
  value: 229.61531707317073,
  unit: "ratio",
  displayName: "IAB Mechanism Benefit-Cost Ratio",
  description: "Benefit-Cost Ratio of the IAB mechanism itself",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/incentive-alignment-bonds-paper#welfare-analysis",
  confidence: "high",
  formula: "TREATY_PEACE_PLUS_RD_BENEFITS ÷ IAB_MECHANISM_COST",
  latex: "\\begin{gathered}\nBCR_{IAB} = \\frac{Benefit_{peace+RD}}{Cost_{IAB,ann}} = \\frac{\\$172B}{\\$750M} = 230 \\\\[0.5em]\n\\text{where } Benefit_{peace+RD} \\\\\n= Benefit_{peace,soc} + Benefit_{RD,ann} \\\\\n= \\$114B + \\$58.6B \\\\\n= \\$172B \\\\[0.5em]\n\\text{where } Benefit_{peace,soc} \\\\\n= Cost_{war,total} \\times Reduce_{treaty} \\\\\n= \\$11.4T \\times 1\\% \\\\\n= \\$114B \\\\[0.5em]\n\\text{where } Cost_{war,total} \\\\\n= Cost_{war,direct} + Cost_{war,indirect} \\\\\n= \\$7.66T + \\$3.7T \\\\\n= \\$11.4T \\\\[0.5em]\n\\text{where } Cost_{war,direct} \\\\\n= Loss_{life,conflict} + Damage_{infra,total} \\\\\n+ Disruption_{trade} + Spending_{mil} \\\\\n= \\$2.45T + \\$1.88T + \\$616B + \\$2.72T \\\\\n= \\$7.66T \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B \\\\[0.5em]\n\\text{where } Cost_{war,indirect} \\\\\n= Damage_{env} + Loss_{growth,mil} \\\\\n+ Loss_{capital,conflict} + Cost_{psych} \\\\\n+ Cost_{refugee} + Cost_{vet} \\\\\n= \\$100B + \\$2.72T + \\$300B + \\$232B + \\$150B + \\$200B \\\\\n= \\$3.7T \\\\[0.5em]\n\\text{where } Benefit_{RD,ann} \\\\\n= Spending_{trials} \\times Reduce_{pct} \\\\\n= \\$60B \\times 97.7\\% \\\\\n= \\$58.6B \\\\[0.5em]\n\\text{where } Reduce_{pct} \\\\\n= 1 - \\frac{Cost_{pragmatic,pt}}{Cost_{P3,pt}} \\\\\n= 1 - \\frac{\\$929}{\\$41K} \\\\\n= 97.7\\%\n\\end{gathered}",
};

export const INDUSTRY_VS_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO: Parameter = {
  value: 12.333333333333334,
  unit: "ratio",
  displayName: "Ratio of Industry to Government Clinical Trials Spending",
  description: "Ratio of Industry to Government spending on clinical trials (approx 90/10 split)",
  sourceType: "calculated",
  sourceRef: "industry-vs-government-trial-spending-split",
  confidence: "high",
  formula: "(TOTAL - GOVT) / GOVT",
  latex: "\\begin{gathered}\nRatio_{ind:gov} \\\\\n= \\frac{Spending_{trials}}{Spending_{trials,gov}} - 1 \\\\\n= \\frac{\\$60B}{\\$4.5B} - 1 \\\\\n= 12.3\n\\end{gathered}",
};

export const LIFE_EXPECTANCY_GAIN_1883_1962_YEARS_PER_DECADE: Parameter = {
  value: 0.0,
  unit: "years/decade",
  displayName: "Life Expectancy Gain Rate (1883-1962)",
  description: "US life expectancy linear gain rate 1883-1962 (pre-Kefauver-Harris).",
  sourceType: "calculated",
  sourceRef: "life-expectancy-increase-pre-1962",
  confidence: "high",
  formula: "(life_exp_1962 - life_exp_1880) / 7.9 decades",
  latex: "\\begin{gathered}\n\\Delta LE_{pre62} \\\\\n= \\frac{LE_{US,1962} - LE_{US,1880}}{7.69} \\\\\n= \\frac{70.1 - 39.4}{7.69} \\\\\n= 0\n\\end{gathered}",
  peerReviewed: true,
};

export const LIFE_EXPECTANCY_GAIN_1962_2019_YEARS_PER_DECADE: Parameter = {
  value: 0.0,
  unit: "years/decade",
  displayName: "Life Expectancy Gain Rate (1962-2019)",
  description: "US life expectancy linear gain rate 1962-2019 (post-Kefauver-Harris).",
  sourceType: "calculated",
  sourceRef: "post-1962-life-expectancy-slowdown",
  confidence: "high",
  formula: "(life_exp_2019 - life_exp_1962) / 5.7 decades",
  latex: "\\begin{gathered}\n\\Delta LE_{post62} \\\\\n= \\frac{LE_{US,2019} - LE_{US,1962}}{5.56} \\\\\n= \\frac{78.9 - 70.1}{5.56} \\\\\n= 0\n\\end{gathered}",
  peerReviewed: true,
};

export const MEDICAL_RESEARCH_PCT_OF_DISEASE_BURDEN: Parameter = {
  value: 0.0005246504079448395,
  unit: "rate",
  displayName: "Medical Research Spending as Percentage of Total Disease Burden",
  description: "Medical research spending as percentage of total disease burden",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/economics",
  confidence: "high",
  formula: "MED_RESEARCH ÷ TOTAL_BURDEN",
  latex: "\\begin{gathered}\nPct_{RD:burden} \\\\\n= \\frac{Spending_{RD}}{Cost_{health+war}} \\\\\n= \\frac{\\$67.5B}{\\$129T} \\\\\n= 0.0525\\% \\\\[0.5em]\n\\text{where } Cost_{health+war} \\\\\n= Cost_{war,total} + Burden_{disease} + Spending_{symptom} \\\\\n= \\$11.4T + \\$109T + \\$8.2T \\\\\n= \\$129T \\\\[0.5em]\n\\text{where } Cost_{war,total} \\\\\n= Cost_{war,direct} + Cost_{war,indirect} \\\\\n= \\$7.66T + \\$3.7T \\\\\n= \\$11.4T \\\\[0.5em]\n\\text{where } Cost_{war,direct} \\\\\n= Loss_{life,conflict} + Damage_{infra,total} \\\\\n+ Disruption_{trade} + Spending_{mil} \\\\\n= \\$2.45T + \\$1.88T + \\$616B + \\$2.72T \\\\\n= \\$7.66T \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B \\\\[0.5em]\n\\text{where } Cost_{war,indirect} \\\\\n= Damage_{env} + Loss_{growth,mil} \\\\\n+ Loss_{capital,conflict} + Cost_{psych} \\\\\n+ Cost_{refugee} + Cost_{vet} \\\\\n= \\$100B + \\$2.72T + \\$300B + \\$232B + \\$150B + \\$200B \\\\\n= \\$3.7T \\\\[0.5em]\n\\text{where } Burden_{disease} \\\\\n= Cost_{medical,direct} + Loss_{life,disease} \\\\\n+ Loss_{productivity} \\\\\n= \\$9.9T + \\$94.2T + \\$5T \\\\\n= \\$109T\n\\end{gathered}",
};

export const MILITARY_TO_CLINICAL_TRIALS_SPENDING_RATIO: Parameter = {
  value: 45.333333333333336,
  unit: "ratio",
  displayName: "Ratio of Military to Clinical Trials Spending",
  description: "Ratio of global military spending to all clinical trials spending (government + industry + nonprofit). Note: $2.7T ÷ $60B = 45×",
  sourceType: "calculated",
  confidence: "high",
  formula: "MILITARY_SPENDING / TOTAL_CLINICAL_TRIALS",
  latex: "\\begin{gathered}\nRatio_{mil:trials} \\\\\n= \\frac{Spending_{mil}}{Spending_{trials}} \\\\\n= \\frac{\\$2.72T}{\\$60B} \\\\\n= 45.3\n\\end{gathered}",
};

export const MILITARY_TO_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO: Parameter = {
  value: 604.4444444444445,
  unit: "ratio",
  displayName: "Ratio of Military to Government Clinical Trials Spending",
  description: "Ratio of global military spending to government clinical trials spending",
  sourceType: "calculated",
  confidence: "high",
  formula: "MILITARY_SPENDING / GOVT_CLINICAL_TRIALS_SPENDING",
  latex: "\\begin{gathered}\nRatio_{mil:gov} \\\\\n= \\frac{Spending_{mil}}{Spending_{trials,gov}} \\\\\n= \\frac{\\$2.72T}{\\$4.5B} \\\\\n= 604\n\\end{gathered}",
};

export const MILITARY_VS_MEDICAL_RESEARCH_RATIO: Parameter = {
  value: 40.2962962962963,
  unit: "ratio",
  displayName: "Ratio of Military Spending to Medical Research Spending",
  description: "Ratio of military spending to medical research spending",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#misallocation",
  confidence: "high",
  formula: "MILITARY_SPENDING ÷ MEDICAL_RESEARCH",
  latex: "\\begin{gathered}\nRatio_{mil:RD} \\\\\n= \\frac{Spending_{mil}}{Spending_{RD}} \\\\\n= \\frac{\\$2.72T}{\\$67.5B} \\\\\n= 40.3\n\\end{gathered}",
};

export const MISALLOCATION_FACTOR_DEATH_VS_SAVING: Parameter = {
  value: 2889.0596892886347,
  unit: "ratio",
  displayName: "Misallocation Factor: Cost to Kill vs Cost to Save",
  description: "Misallocation factor: cost to kill vs cost to save",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/cost-of-war#grotesque-mathematics",
  confidence: "high",
  formula: "COST_PER_DEATH ÷ COST_PER_LIFE_SAVED",
  latex: "\\begin{gathered}\nk_{misalloc} \\\\\n= \\frac{Cost_{war,total}}{Deaths_{conflict} \\times Cost_{life,RD}} \\\\\n= \\frac{\\$11.4T}{245{,}000 \\times \\$16.1K} \\\\\n= 2{,}890 \\\\[0.5em]\n\\text{where } Deaths_{conflict} \\\\\n= Deaths_{combat} + Deaths_{state} + Deaths_{terror} \\\\\n= 234{,}000 + 2{,}700 + 8{,}300 \\\\\n= 245{,}000 \\\\[0.5em]\n\\text{where } Cost_{war,total} \\\\\n= Cost_{war,direct} + Cost_{war,indirect} \\\\\n= \\$7.66T + \\$3.7T \\\\\n= \\$11.4T \\\\[0.5em]\n\\text{where } Cost_{war,direct} \\\\\n= Loss_{life,conflict} + Damage_{infra,total} \\\\\n+ Disruption_{trade} + Spending_{mil} \\\\\n= \\$2.45T + \\$1.88T + \\$616B + \\$2.72T \\\\\n= \\$7.66T \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B \\\\[0.5em]\n\\text{where } Cost_{war,indirect} \\\\\n= Damage_{env} + Loss_{growth,mil} \\\\\n+ Loss_{capital,conflict} + Cost_{psych} \\\\\n+ Cost_{refugee} + Cost_{vet} \\\\\n= \\$100B + \\$2.72T + \\$300B + \\$232B + \\$150B + \\$200B \\\\\n= \\$3.7T \\\\[0.5em]\n\\text{where } Cost_{life,RD} = \\frac{Spending_{RD}}{Lives_{RD,ann}} = \\frac{\\$67.5B}{4.2M} = \\$16.1K\n\\end{gathered}",
};

export const MRNA_THERAPEUTIC_COMBINATIONS: Parameter = {
  value: 20000000.0,
  unit: "combinations",
  displayName: "mRNA Therapeutic Combinations",
  description: "mRNA therapeutic combinations (protein replacement, vaccines, enzyme delivery)",
  sourceType: "calculated",
  confidence: "high",
  formula: "PROTEINS × DISEASES",
  latex: "\\begin{gathered}\nCombos_{mRNA} \\\\\n= N_{genes} \\times N_{diseases,trial} \\\\\n= 20{,}000 \\times 1{,}000 \\\\\n= 20M\n\\end{gathered}",
};

export const PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT: Parameter = {
  value: 113571000000.0,
  unit: "USD/year",
  displayName: "Annual Peace Dividend from 1% Reduction in Total War Costs",
  description: "Annual peace dividend from 1% reduction in total war costs",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/peace-dividend-calculations",
  confidence: "high",
  formula: "TOTAL_WAR_COST × 1%",
  latex: "\\begin{gathered}\nBenefit_{peace,soc} \\\\\n= Cost_{war,total} \\times Reduce_{treaty} \\\\\n= \\$11.4T \\times 1\\% \\\\\n= \\$114B \\\\[0.5em]\n\\text{where } Cost_{war,total} \\\\\n= Cost_{war,direct} + Cost_{war,indirect} \\\\\n= \\$7.66T + \\$3.7T \\\\\n= \\$11.4T \\\\[0.5em]\n\\text{where } Cost_{war,direct} \\\\\n= Loss_{life,conflict} + Damage_{infra,total} \\\\\n+ Disruption_{trade} + Spending_{mil} \\\\\n= \\$2.45T + \\$1.88T + \\$616B + \\$2.72T \\\\\n= \\$7.66T \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B \\\\[0.5em]\n\\text{where } Cost_{war,indirect} \\\\\n= Damage_{env} + Loss_{growth,mil} \\\\\n+ Loss_{capital,conflict} + Cost_{psych} \\\\\n+ Cost_{refugee} + Cost_{vet} \\\\\n= \\$100B + \\$2.72T + \\$300B + \\$232B + \\$150B + \\$200B \\\\\n= \\$3.7T\n\\end{gathered}",
};

export const PEACE_DIVIDEND_CONFLICT_REDUCTION: Parameter = {
  value: 86371000000.0,
  unit: "USD/year",
  displayName: "Conflict Reduction Benefits from 1% Less Military Spending",
  description: "Conflict reduction benefits from 1% less military spending (lower confidence - assumes proportional relationship)",
  sourceType: "calculated",
  sourceRef: "calculated",
  confidence: "low",
  formula: "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT - TREATY_ANNUAL_FUNDING",
  latex: "\\begin{gathered}\nSavings_{conflict} \\\\\n= Benefit_{peace,soc} - Funding_{treaty} \\\\\n= \\$114B - \\$27.2B \\\\\n= \\$86.4B \\\\[0.5em]\n\\text{where } Benefit_{peace,soc} \\\\\n= Cost_{war,total} \\times Reduce_{treaty} \\\\\n= \\$11.4T \\times 1\\% \\\\\n= \\$114B \\\\[0.5em]\n\\text{where } Cost_{war,total} \\\\\n= Cost_{war,direct} + Cost_{war,indirect} \\\\\n= \\$7.66T + \\$3.7T \\\\\n= \\$11.4T \\\\[0.5em]\n\\text{where } Cost_{war,direct} \\\\\n= Loss_{life,conflict} + Damage_{infra,total} \\\\\n+ Disruption_{trade} + Spending_{mil} \\\\\n= \\$2.45T + \\$1.88T + \\$616B + \\$2.72T \\\\\n= \\$7.66T \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B \\\\[0.5em]\n\\text{where } Cost_{war,indirect} \\\\\n= Damage_{env} + Loss_{growth,mil} \\\\\n+ Loss_{capital,conflict} + Cost_{psych} \\\\\n+ Cost_{refugee} + Cost_{vet} \\\\\n= \\$100B + \\$2.72T + \\$300B + \\$232B + \\$150B + \\$200B \\\\\n= \\$3.7T \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const PEACE_DIVIDEND_DIRECT_COSTS: Parameter = {
  value: 76570000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Direct War Costs",
  description: "Annual savings from 1% reduction in direct war costs",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "DIRECT_COSTS × 1%",
  latex: "\\begin{gathered}\nSavings_{direct} \\\\\n= Cost_{war,direct} \\times Reduce_{treaty} \\\\\n= \\$7.66T \\times 1\\% \\\\\n= \\$76.6B \\\\[0.5em]\n\\text{where } Cost_{war,direct} \\\\\n= Loss_{life,conflict} + Damage_{infra,total} \\\\\n+ Disruption_{trade} + Spending_{mil} \\\\\n= \\$2.45T + \\$1.88T + \\$616B + \\$2.72T \\\\\n= \\$7.66T \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B\n\\end{gathered}",
};

export const PEACE_DIVIDEND_ENVIRONMENTAL: Parameter = {
  value: 1000000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Environmental Damage",
  description: "Annual savings from 1% reduction in environmental damage",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "ENVIRONMENTAL_DAMAGE × 1%",
  latex: "\\begin{gathered}\nSavings_{env} \\\\\n= Damage_{env} \\times Reduce_{treaty} \\\\\n= \\$100B \\times 1\\% \\\\\n= \\$1B\n\\end{gathered}",
};

export const PEACE_DIVIDEND_HUMAN_CASUALTIES: Parameter = {
  value: 24460000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Human Casualties",
  description: "Annual savings from 1% reduction in human casualties",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "HUMAN_LIFE_LOSSES × 1%",
  latex: "\\begin{gathered}\nSavings_{casualties} \\\\\n= Loss_{life,conflict} \\times Reduce_{treaty} \\\\\n= \\$2.45T \\times 1\\% \\\\\n= \\$24.5B \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B\n\\end{gathered}",
};

export const PEACE_DIVIDEND_INDIRECT_COSTS: Parameter = {
  value: 37001000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Indirect War Costs",
  description: "Annual savings from 1% reduction in indirect war costs",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "INDIRECT_COSTS × 1%",
  latex: "\\begin{gathered}\nSavings_{indirect} \\\\\n= Cost_{war,indirect} \\times Reduce_{treaty} \\\\\n= \\$3.7T \\times 1\\% \\\\\n= \\$37B \\\\[0.5em]\n\\text{where } Cost_{war,indirect} \\\\\n= Damage_{env} + Loss_{growth,mil} \\\\\n+ Loss_{capital,conflict} + Cost_{psych} \\\\\n+ Cost_{refugee} + Cost_{vet} \\\\\n= \\$100B + \\$2.72T + \\$300B + \\$232B + \\$150B + \\$200B \\\\\n= \\$3.7T\n\\end{gathered}",
};

export const PEACE_DIVIDEND_INFRASTRUCTURE: Parameter = {
  value: 18750000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Infrastructure Destruction",
  description: "Annual savings from 1% reduction in infrastructure destruction",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "INFRASTRUCTURE_DESTRUCTION × 1%",
  latex: "\\begin{gathered}\nSavings_{infra} \\\\\n= Damage_{infra,total} \\times Reduce_{treaty} \\\\\n= \\$1.88T \\times 1\\% \\\\\n= \\$18.8B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T\n\\end{gathered}",
};

export const PEACE_DIVIDEND_LOST_ECONOMIC_GROWTH: Parameter = {
  value: 27180000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Lost Economic Growth",
  description: "Annual savings from 1% reduction in lost economic growth",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "LOST_ECONOMIC_GROWTH × 1%",
  latex: "\\begin{gathered}\nSavings_{growth} \\\\\n= Loss_{growth,mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const PEACE_DIVIDEND_LOST_HUMAN_CAPITAL: Parameter = {
  value: 3000000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Lost Human Capital",
  description: "Annual savings from 1% reduction in lost human capital",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "LOST_HUMAN_CAPITAL × 1%",
  latex: "\\begin{gathered}\nSavings_{capital} \\\\\n= Loss_{capital,conflict} \\times Reduce_{treaty} \\\\\n= \\$300B \\times 1\\% \\\\\n= \\$3B\n\\end{gathered}",
};

export const PEACE_DIVIDEND_PTSD: Parameter = {
  value: 2320000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in PTSD and Mental Health Costs",
  description: "Annual savings from 1% reduction in PTSD and mental health costs",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "PTSD_COSTS × 1%",
  latex: "\\begin{gathered}\nSavings_{PTSD} \\\\\n= Cost_{psych} \\times Reduce_{treaty} \\\\\n= \\$232B \\times 1\\% \\\\\n= \\$2.32B\n\\end{gathered}",
};

export const PEACE_DIVIDEND_REFUGEE_SUPPORT: Parameter = {
  value: 1500000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Refugee Support Costs",
  description: "Annual savings from 1% reduction in refugee support costs",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "REFUGEE_SUPPORT × 1%",
  latex: "\\begin{gathered}\nSavings_{refugee} \\\\\n= Cost_{refugee} \\times Reduce_{treaty} \\\\\n= \\$150B \\times 1\\% \\\\\n= \\$1.5B\n\\end{gathered}",
};

export const PEACE_DIVIDEND_TRADE_DISRUPTION: Parameter = {
  value: 6160000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Trade Disruption",
  description: "Annual savings from 1% reduction in trade disruption",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "TRADE_DISRUPTION × 1%",
  latex: "\\begin{gathered}\nSavings_{trade} \\\\\n= Disruption_{trade} \\times Reduce_{treaty} \\\\\n= \\$616B \\times 1\\% \\\\\n= \\$6.16B \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B\n\\end{gathered}",
};

export const PEACE_DIVIDEND_VETERAN_HEALTHCARE: Parameter = {
  value: 2001000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Veteran Healthcare Costs",
  description: "Annual savings from 1% reduction in veteran healthcare costs",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "VETERAN_HEALTHCARE × 1%",
  latex: "\\begin{gathered}\nSavings_{vet} \\\\\n= Cost_{vet} \\times Reduce_{treaty} \\\\\n= \\$200B \\times 1\\% \\\\\n= \\$2B\n\\end{gathered}",
};

export const PERSONAL_LIFETIME_WEALTH: Parameter = {
  value: 494010.86520261574,
  unit: "usd",
  displayName: "Personal Lifetime Wealth (Age 30, 1% Treaty)",
  description: "Personal lifetime wealth benefit for a 30-year-old with $50K income under 1% treaty. Life extension uncertainty (5-50 years) propagates through Monte Carlo to show full range of outcomes from conservative antibiotic precedent to optimistic aging reversal scenarios.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/disease-eradication-personal-lifetime-wealth-calculations",
  confidence: "medium",
  formula: "NPV(peace_dividend + healthcare_savings + productivity_gains + caregiver_savings + gdp_boost + extended_earnings)",
  latex: "\\begin{gathered}\nWealth_{lifetime} \\\\\n= \\text{NPV}(\\text{Peace} + \\text{Health} \\\\\n+ \\text{Productivity} + \\text{Earnings})\n\\end{gathered}",
};

export const PER_CAPITA_CHRONIC_DISEASE_COST: Parameter = {
  value: 12238.805970149253,
  unit: "USD/person/year",
  displayName: "US Per Capita Chronic Disease Cost",
  description: "US per capita chronic disease cost",
  sourceType: "calculated",
  confidence: "high",
  formula: "US_CHRONIC_DISEASE_SPENDING ÷ US_POPULATION",
  latex: "\\begin{gathered}\nCost_{chronic,pc} \\\\\n= \\frac{Spending_{chronic,US}}{Pop_{US}} \\\\\n= \\frac{\\$4.1T}{335M} \\\\\n= \\$12.2K\n\\end{gathered}",
};

export const PER_CAPITA_MENTAL_HEALTH_COST: Parameter = {
  value: 1044.7761194029852,
  unit: "USD/person/year",
  displayName: "US Per Capita Mental Health Cost",
  description: "US per capita mental health cost",
  sourceType: "calculated",
  confidence: "high",
  formula: "US_MENTAL_HEALTH_COST ÷ US_POPULATION",
  latex: "\\begin{gathered}\nCost_{mental,pc} \\\\\n= \\frac{Cost_{mental,US}}{Pop_{US}} \\\\\n= \\frac{\\$350B}{335M} \\\\\n= \\$1.04K\n\\end{gathered}",
};

export const POLITICAL_DYSFUNCTION_TAX_TOTAL_PCT: Parameter = {
  value: 0.2,
  unit: "percent",
  displayName: "Political Dysfunction Tax (Total)",
  description: "Total Political Dysfunction Tax: the welfare loss from governance failures as percentage of potential GDP. Sum of Crony Tax (capture), time-inconsistency, information costs, and coordination failures. Represents the 'tax' citizens implicitly pay for dysfunctional political systems.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/optimocracy-paper",
  confidence: "low",
  formula: "CRONY_TAX + TIME + INFO + COORDINATION",
  latex: "\\begin{gathered}\n\\tau_{dysfunction} \\\\\n= \\tau_{crony} + \\tau_{time} + \\tau_{info} + \\tau_{coord} \\\\\n= 10\\% + 3\\% + 2\\% + 5\\% \\\\\n= 20\\%\n\\end{gathered}",
};

export const PRAGMATIC_TRIAL_COST_PER_QALY: Parameter = {
  value: 4.0,
  unit: "USD/QALY",
  displayName: "Pragmatic Trial Cost per QALY (RECOVERY)",
  description: "Cost per QALY for pragmatic platform trials, calculated from RECOVERY trial data. Uses global impact methodology: trial cost divided by total QALYs from downstream adoption. This measures research efficiency (discovery value), not clinical intervention ICER.",
  sourceType: "calculated",
  sourceRef: "recovery-trial-82x-cost-reduction",
  confidence: "medium",
  formula: "TRIAL_COST ÷ TOTAL_QALYS_GENERATED",
  latex: "\\begin{gathered}\nCost_{pragmatic,QALY} = \\frac{Cost_{RECOVERY}}{QALY_{RECOVERY}} = \\frac{\\$20M}{5M} = \\$4 \\\\[0.5em]\n\\text{where } QALY_{RECOVERY} \\\\\n= Lives_{RECOVERY} \\times QALY_{COVID} \\\\\n= 1M \\times 5 \\\\\n= 5M\n\\end{gathered}",
};

export const PRAGMATIC_VS_NIH_EFFICIENCY_MULTIPLIER: Parameter = {
  value: 12500.0,
  unit: "ratio",
  displayName: "Pragmatic Trial Efficiency Multiplier vs NIH",
  description: "How many times more cost-effective pragmatic trials are vs standard NIH research. Calculated using global impact methodology (NIH cost per QALY / pragmatic cost per QALY). Shows orders-of-magnitude efficiency gap between discovery-focused pragmatic trials and standard research.",
  sourceType: "calculated",
  confidence: "medium",
  formula: "NIH_COST_PER_QALY ÷ PRAGMATIC_COST_PER_QALY",
  latex: "\\begin{gathered}\nk_{pragmatic:NIH} \\\\\n= \\frac{Cost_{NIH,QALY}}{Cost_{pragmatic,QALY}} \\\\\n= \\frac{\\$50K}{\\$4} \\\\\n= 12{,}500 \\\\[0.5em]\n\\text{where } Cost_{pragmatic,QALY} = \\frac{Cost_{RECOVERY}}{QALY_{RECOVERY}} = \\frac{\\$20M}{5M} = \\$4 \\\\[0.5em]\n\\text{where } QALY_{RECOVERY} \\\\\n= Lives_{RECOVERY} \\times QALY_{COVID} \\\\\n= 1M \\times 5 \\\\\n= 5M\n\\end{gathered}",
};

export const RECOVERY_TRIAL_COST_REDUCTION_FACTOR: Parameter = {
  value: 82.0,
  unit: "multiplier",
  displayName: "RECOVERY Trial Cost Reduction Factor",
  description: "Cost reduction factor demonstrated by RECOVERY trial ($41K traditional / $500 RECOVERY = 82x)",
  sourceType: "calculated",
  sourceRef: "recovery-trial-82x-cost-reduction",
  confidence: "high",
  formula: "TRADITIONAL_PHASE3_COST / RECOVERY_COST",
  latex: "\\begin{gathered}\nk_{RECOVERY} \\\\\n= \\frac{Cost_{P3,pt}}{Cost_{RECOVERY,pt}} \\\\\n= \\frac{\\$41K}{\\$500} \\\\\n= 82\n\\end{gathered}",
};

export const RECOVERY_TRIAL_TOTAL_QALYS_GENERATED: Parameter = {
  value: 5000000.0,
  unit: "QALYs",
  displayName: "RECOVERY Trial Total QALYs Generated",
  description: "Total QALYs generated by RECOVERY trial's discoveries (lives saved × QALYs per life). Uses global impact methodology: counts all downstream health gains from the discovery.",
  sourceType: "calculated",
  confidence: "medium",
  formula: "LIVES_SAVED × QALYS_PER_DEATH_AVERTED",
  latex: "\\begin{gathered}\nQALY_{RECOVERY} \\\\\n= Lives_{RECOVERY} \\times QALY_{COVID} \\\\\n= 1M \\times 5 \\\\\n= 5M\n\\end{gathered}",
};

export const STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT: Parameter = {
  value: 221.66666666666666,
  unit: "years",
  displayName: "Status Quo Average Years to First Treatment",
  description: "Average years until first treatment discovered for a typical disease under current system. The average disease is in the middle of the queue, so it waits half the total queue clearance time (~443/2 = ~222 years).",
  sourceType: "calculated",
  sourceRef: "status-quo-cure-timeline-estimate",
  confidence: "low",
  formula: "STATUS_QUO_QUEUE_CLEARANCE_YEARS ÷ 2",
  latex: "\\begin{gathered}\nT_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650\n\\end{gathered}",
};

export const STATUS_QUO_QUEUE_CLEARANCE_YEARS: Parameter = {
  value: 443.3333333333333,
  unit: "years",
  displayName: "Status Quo Queue Clearance Time",
  description: "Years to clear entire queue of diseases without treatment. At current rate of ~15 diseases/year getting first treatments, the queue of ~6,650 would take ~443 years to completely clear.",
  sourceType: "calculated",
  sourceRef: "status-quo-cure-timeline-estimate",
  confidence: "low",
  formula: "DISEASES_WITHOUT_EFFECTIVE_TREATMENT ÷ NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR",
  latex: "\\begin{gathered}\nT_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650\n\\end{gathered}",
};

export const THALIDOMIDE_DALYS_PER_EVENT: Parameter = {
  value: 41760.0,
  unit: "DALYs",
  displayName: "Thalidomide DALYs Per Event",
  description: "Total DALYs per US-scale thalidomide event (YLL + YLD)",
  sourceType: "calculated",
  confidence: "medium",
  formula: "YLL + YLD",
  latex: "\\begin{gathered}\nDALY_{thal} \\\\\n= YLD_{thal} + YLL_{thal} \\\\\n= 13{,}000 + 28{,}800 \\\\\n= 41{,}800 \\\\[0.5em]\n\\text{where } YLD_{thal} \\\\\n= DW_{thal} \\times N_{thal,survive} \\times LE_{thal} \\\\\n= 0.4 \\times 540 \\times 60 \\\\\n= 13{,}000 \\\\[0.5em]\n\\text{where } N_{thal,survive} \\\\\n= N_{thal,US,prevent} \\times (1 - Rate_{thal,mort}) \\\\\n= 900 \\times (1 - 40\\%) \\\\\n= 540 \\\\[0.5em]\n\\text{where } N_{thal,US,prevent} \\\\\n= N_{thal,global} \\times Pct_{US,1960} \\\\\n= 15{,}000 \\times 6\\% \\\\\n= 900 \\\\[0.5em]\n\\text{where } YLL_{thal} = Deaths_{thal} \\times 80 = 360 \\times 80 = 28{,}800 \\\\[0.5em]\n\\text{where } Deaths_{thal} \\\\\n= Rate_{thal,mort} \\times N_{thal,US,prevent} \\\\\n= 40\\% \\times 900 \\\\\n= 360 \\\\[0.5em]\n\\text{where } N_{thal,US,prevent} \\\\\n= N_{thal,global} \\times Pct_{US,1960} \\\\\n= 15{,}000 \\times 6\\% \\\\\n= 900\n\\end{gathered}",
};

export const THALIDOMIDE_DEATHS_PER_EVENT: Parameter = {
  value: 360.0,
  unit: "deaths",
  displayName: "Thalidomide Deaths Per Event",
  description: "Deaths per US-scale thalidomide event",
  sourceType: "calculated",
  confidence: "medium",
  formula: "US_CASES × MORTALITY_RATE",
  latex: "\\begin{gathered}\nDeaths_{thal} \\\\\n= Rate_{thal,mort} \\times N_{thal,US,prevent} \\\\\n= 40\\% \\times 900 \\\\\n= 360 \\\\[0.5em]\n\\text{where } N_{thal,US,prevent} \\\\\n= N_{thal,global} \\times Pct_{US,1960} \\\\\n= 15{,}000 \\times 6\\% \\\\\n= 900\n\\end{gathered}",
};

export const THALIDOMIDE_SURVIVORS_PER_EVENT: Parameter = {
  value: 540.0,
  unit: "cases",
  displayName: "Thalidomide Survivors Per Event",
  description: "Survivors per US-scale thalidomide event",
  sourceType: "calculated",
  confidence: "medium",
  formula: "US_CASES × (1 - MORTALITY_RATE)",
  latex: "\\begin{gathered}\nN_{thal,survive} \\\\\n= N_{thal,US,prevent} \\times (1 - Rate_{thal,mort}) \\\\\n= 900 \\times (1 - 40\\%) \\\\\n= 540 \\\\[0.5em]\n\\text{where } N_{thal,US,prevent} \\\\\n= N_{thal,global} \\times Pct_{US,1960} \\\\\n= 15{,}000 \\times 6\\% \\\\\n= 900\n\\end{gathered}",
};

export const THALIDOMIDE_US_CASES_PREVENTED: Parameter = {
  value: 900.0,
  unit: "cases",
  displayName: "Thalidomide US Cases Prevented",
  description: "Estimated US thalidomide cases prevented by FDA rejection",
  sourceType: "calculated",
  confidence: "medium",
  formula: "WORLDWIDE_CASES × US_POPULATION_SHARE",
  latex: "\\begin{gathered}\nN_{thal,US,prevent} \\\\\n= N_{thal,global} \\times Pct_{US,1960} \\\\\n= 15{,}000 \\times 6\\% \\\\\n= 900\n\\end{gathered}",
};

export const THALIDOMIDE_YLD_PER_EVENT: Parameter = {
  value: 12960.0,
  unit: "years",
  displayName: "Thalidomide YLD Per Event",
  description: "Years Lived with Disability per thalidomide event",
  sourceType: "calculated",
  confidence: "medium",
  formula: "SURVIVORS × LIFESPAN × DISABILITY_WEIGHT",
  latex: "\\begin{gathered}\nYLD_{thal} \\\\\n= DW_{thal} \\times N_{thal,survive} \\times LE_{thal} \\\\\n= 0.4 \\times 540 \\times 60 \\\\\n= 13{,}000 \\\\[0.5em]\n\\text{where } N_{thal,survive} \\\\\n= N_{thal,US,prevent} \\times (1 - Rate_{thal,mort}) \\\\\n= 900 \\times (1 - 40\\%) \\\\\n= 540 \\\\[0.5em]\n\\text{where } N_{thal,US,prevent} \\\\\n= N_{thal,global} \\times Pct_{US,1960} \\\\\n= 15{,}000 \\times 6\\% \\\\\n= 900\n\\end{gathered}",
};

export const THALIDOMIDE_YLL_PER_EVENT: Parameter = {
  value: 28800.0,
  unit: "years",
  displayName: "Thalidomide YLL Per Event",
  description: "Years of Life Lost per thalidomide event (infant deaths)",
  sourceType: "calculated",
  confidence: "medium",
  formula: "DEATHS × 80 years",
  latex: "\\begin{gathered}\nYLL_{thal} = Deaths_{thal} \\times 80 = 360 \\times 80 = 28{,}800 \\\\[0.5em]\n\\text{where } Deaths_{thal} \\\\\n= Rate_{thal,mort} \\times N_{thal,US,prevent} \\\\\n= 40\\% \\times 900 \\\\\n= 360 \\\\[0.5em]\n\\text{where } N_{thal,US,prevent} \\\\\n= N_{thal,global} \\times Pct_{US,1960} \\\\\n= 15{,}000 \\times 6\\% \\\\\n= 900\n\\end{gathered}",
};

export const TOTAL_RESEARCH_FUNDING_WITH_TREATY: Parameter = {
  value: 94700000000.0,
  unit: "USD",
  displayName: "Total Global Research Funding (Baseline + 1% treaty Funding)",
  description: "Total global research funding (baseline + 1% treaty funding)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/economics",
  confidence: "high",
  formula: "GLOBAL_MED_RESEARCH_SPENDING + TREATY_ANNUAL_FUNDING",
  latex: "\\begin{gathered}\nFunding_{RD,total} \\\\\n= Spending_{RD} + Funding_{treaty} \\\\\n= \\$67.5B + \\$27.2B \\\\\n= \\$94.7B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS: Parameter = {
  value: 51500000.0,
  unit: "combinations",
  displayName: "Total Testable Therapeutic Space",
  description: "Total testable therapeutic combinations (known safe compounds + emerging modalities)",
  sourceType: "calculated",
  confidence: "high",
  formula: "KNOWN_SAFE + EMERGING_MODALITIES",
  latex: "\\begin{gathered}\nN_{testable} \\\\\n= N_{combos} + N_{emerging} \\\\\n= 9.5M + 42M \\\\\n= 51.5M \\\\[0.5em]\n\\text{where } N_{combos} \\\\\n= N_{safe} \\times N_{diseases,trial} \\\\\n= 9{,}500 \\times 1{,}000 \\\\\n= 9.5M \\\\[0.5em]\n\\text{where } N_{emerging} \\\\\n= Combos_{gene} + Combos_{mRNA} + Combos_{epi} + Combos_{cell} \\\\\n= 20M + 20M + 1.5M + 500{,}000 \\\\\n= 42M \\\\[0.5em]\n\\text{where } Combos_{gene} \\\\\n= N_{genes} \\times N_{diseases,trial} \\\\\n= 20{,}000 \\times 1{,}000 \\\\\n= 20M \\\\[0.5em]\n\\text{where } Combos_{mRNA} \\\\\n= N_{genes} \\times N_{diseases,trial} \\\\\n= 20{,}000 \\times 1{,}000 \\\\\n= 20M \\\\[0.5em]\n\\text{where } Combos_{epi} \\\\\n= N_{epi} \\times N_{diseases,trial} \\\\\n= 1{,}500 \\times 1{,}000 \\\\\n= 1.5M \\\\[0.5em]\n\\text{where } Combos_{cell} \\\\\n= N_{cell} \\times N_{diseases,trial} \\\\\n= 500 \\times 1{,}000 \\\\\n= 500{,}000\n\\end{gathered}",
};

export const TREATY_BENEFIT_MULTIPLIER_VS_VACCINES: Parameter = {
  value: 11.480765853658538,
  unit: "ratio",
  displayName: "Treaty System Benefit Multiplier vs Childhood Vaccination Programs",
  description: "Treaty system benefit multiplier vs childhood vaccination programs",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/economics#better-than-the-best-charities",
  confidence: "high",
  formula: "TREATY_CONSERVATIVE_BENEFIT ÷ CHILDHOOD_VACCINATION_BENEFIT",
  latex: "\\begin{gathered}\nk_{treaty:vax} = \\frac{Dividend_{total,ann}}{Benefit_{vax,ann}} = \\frac{\\$172B}{\\$15B} = 11.5 \\\\[0.5em]\n\\text{where } Dividend_{total,ann} \\\\\n= Benefit_{peace,soc} + Benefit_{RD,ann} \\\\\n= \\$114B + \\$58.6B \\\\\n= \\$172B \\\\[0.5em]\n\\text{where } Benefit_{peace,soc} \\\\\n= Cost_{war,total} \\times Reduce_{treaty} \\\\\n= \\$11.4T \\times 1\\% \\\\\n= \\$114B \\\\[0.5em]\n\\text{where } Cost_{war,total} \\\\\n= Cost_{war,direct} + Cost_{war,indirect} \\\\\n= \\$7.66T + \\$3.7T \\\\\n= \\$11.4T \\\\[0.5em]\n\\text{where } Cost_{war,direct} \\\\\n= Loss_{life,conflict} + Damage_{infra,total} \\\\\n+ Disruption_{trade} + Spending_{mil} \\\\\n= \\$2.45T + \\$1.88T + \\$616B + \\$2.72T \\\\\n= \\$7.66T \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B \\\\[0.5em]\n\\text{where } Cost_{war,indirect} \\\\\n= Damage_{env} + Loss_{growth,mil} \\\\\n+ Loss_{capital,conflict} + Cost_{psych} \\\\\n+ Cost_{refugee} + Cost_{vet} \\\\\n= \\$100B + \\$2.72T + \\$300B + \\$232B + \\$150B + \\$200B \\\\\n= \\$3.7T \\\\[0.5em]\n\\text{where } Benefit_{RD,ann} \\\\\n= Spending_{trials} \\times Reduce_{pct} \\\\\n= \\$60B \\times 97.7\\% \\\\\n= \\$58.6B \\\\[0.5em]\n\\text{where } Reduce_{pct} \\\\\n= 1 - \\frac{Cost_{pragmatic,pt}}{Cost_{P3,pt}} \\\\\n= 1 - \\frac{\\$929}{\\$41K} \\\\\n= 97.7\\%\n\\end{gathered}",
};

export const TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED: Parameter = {
  value: 250000000.0,
  unit: "USD/year",
  displayName: "Amortized Annual Treaty Campaign Cost",
  description: "Amortized annual campaign cost (total cost ÷ campaign duration)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/strategy/roadmap#campaign-budget",
  confidence: "high",
  formula: "TOTAL_COST ÷ DURATION",
  latex: "\\begin{gathered}\nCost_{camp,amort} = \\frac{Cost_{campaign}}{T_{campaign}} = \\frac{\\$1B}{4} = \\$250M \\\\[0.5em]\n\\text{where } Cost_{campaign} \\\\\n= Budget_{viral,base} + Budget_{lobby,treaty} \\\\\n+ Budget_{reserve} \\\\\n= \\$250M + \\$650M + \\$100M \\\\\n= \\$1B\n\\end{gathered}",
};

export const TREATY_CAMPAIGN_TOTAL_COST: Parameter = {
  value: 1000000000.0,
  unit: "USD",
  displayName: "Total 1% Treaty Campaign Cost",
  description: "Total treaty campaign cost (100% VICTORY Incentive Alignment Bonds)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/fundraising-strategy#capital-structure-campaign-vs-implementation",
  confidence: "high",
  formula: "REFERENDUM + LOBBYING + RESERVE",
  latex: "\\begin{gathered}\nCost_{campaign} \\\\\n= Budget_{viral,base} + Budget_{lobby,treaty} \\\\\n+ Budget_{reserve} \\\\\n= \\$250M + \\$650M + \\$100M \\\\\n= \\$1B\n\\end{gathered}",
};

export const TREATY_CAMPAIGN_VOTING_BLOC_TARGET: Parameter = {
  value: 280000000.0,
  unit: "of people",
  displayName: "Target Voting Bloc Size for Campaign",
  description: "Target voting bloc size for campaign (3.5% of global population - critical mass for social change)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/strategy/roadmap#voting-bloc",
  confidence: "high",
  formula: "GLOBAL_POPULATION × 3.5%",
  latex: "\\begin{gathered}\nN_{voters,target} \\\\\n= Pop_{global} \\times Threshold_{activism} \\\\\n= 8B \\times 3.5\\% \\\\\n= 280M\n\\end{gathered}",
};

export const TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG: Parameter = {
  value: 0.0017694250349878041,
  unit: "USD/DALY",
  displayName: "Cost per DALY Averted (Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Increased Trial Throughput)",
  description: "Cost per DALY averted from elimination of efficacy lag plus earlier treatment discovery from increased trial throughput. Only counts campaign cost; ignores economic benefits from funding and R&D savings.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper",
  confidence: "high",
  formula: "CAMPAIGN_COST ÷ DALYS_TIMELINE_SHIFT",
  latex: "\\begin{gathered}\nCost_{treaty,DALY} = \\frac{Cost_{campaign}}{DALYs_{max}} = \\frac{\\$1B}{565B} = \\$0.00177 \\\\[0.5em]\n\\text{where } Cost_{campaign} \\\\\n= Budget_{viral,base} + Budget_{lobby,treaty} \\\\\n+ Budget_{reserve} \\\\\n= \\$250M + \\$650M + \\$100M \\\\\n= \\$1B \\\\[0.5em]\n\\text{where } DALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const TREATY_EXPECTED_COST_PER_DALY: Parameter = {
  value: 0.1769425034987804,
  unit: "USD/DALY",
  displayName: "Expected Cost per DALY (Risk-Adjusted)",
  description: "Expected cost per DALY accounting for political success probability uncertainty. Monte Carlo samples from beta(0.1%, 10%) distribution. At the conservative 1% estimate, this is still more cost-effective than bed nets ($89.0/DALY).",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper",
  confidence: "low",
  formula: "CONDITIONAL_COST_PER_DALY ÷ POLITICAL_SUCCESS_PROBABILITY",
  latex: "\\begin{gathered}\nE[Cost_{DALY}] = \\frac{Cost_{treaty,DALY}}{P_{success}} = \\frac{\\$0.00177}{1\\%} = \\$0.177 \\\\[0.5em]\n\\text{where } Cost_{treaty,DALY} = \\frac{Cost_{campaign}}{DALYs_{max}} = \\frac{\\$1B}{565B} = \\$0.00177 \\\\[0.5em]\n\\text{where } Cost_{campaign} \\\\\n= Budget_{viral,base} + Budget_{lobby,treaty} \\\\\n+ Budget_{reserve} \\\\\n= \\$250M + \\$650M + \\$100M \\\\\n= \\$1B \\\\[0.5em]\n\\text{where } DALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const TREATY_EXPECTED_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG: Parameter = {
  value: 847733.003851355,
  unit: "ratio",
  displayName: "Expected Treaty ROI (Risk-Adjusted)",
  description: "Expected ROI for 1% treaty accounting for political success probability uncertainty. Monte Carlo samples POLITICAL_SUCCESS_PROBABILITY from beta(0.1%, 10%) distribution to generate full expected value distribution. Central value uses 1% probability.",
  sourceType: "calculated",
  sourceRef: "calculated",
  confidence: "low",
  formula: "TREATY_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG × POLITICAL_SUCCESS_PROBABILITY",
  latex: "\\begin{gathered}\nE[ROI_{max}] \\\\\n= ROI_{max} \\times P_{success} \\\\\n= 84.8M \\times 1\\% \\\\\n= 848{,}000 \\\\[0.5em]\n\\text{where } ROI_{max} = \\frac{Value_{max}}{Cost_{campaign}} = \\frac{\\$84800T}{\\$1B} = 84.8M \\\\[0.5em]\n\\text{where } Value_{max} \\\\\n= DALYs_{max} \\times Value_{QALY} \\\\\n= 565B \\times \\$150K \\\\\n= \\$84800T \\\\[0.5em]\n\\text{where } DALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Cost_{campaign} \\\\\n= Budget_{viral,base} + Budget_{lobby,treaty} \\\\\n+ Budget_{reserve} \\\\\n= \\$250M + \\$650M + \\$100M \\\\\n= \\$1B\n\\end{gathered}",
};

export const TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER: Parameter = {
  value: 502.98824895180394,
  unit: "ratio",
  displayName: "Expected Cost-Effectiveness vs Bed Nets Multiplier",
  description: "Expected value multiplier vs bed nets (accounts for political uncertainty at 1% success rate)",
  sourceType: "calculated",
  confidence: "low",
  formula: "BED_NETS_COST_PER_DALY ÷ TREATY_EXPECTED_COST_PER_DALY",
  latex: "\\begin{gathered}\nE[k_{nets}] = \\frac{Cost_{nets}}{E[Cost_{DALY}]} = \\frac{\\$89}{\\$0.177} = 503 \\\\[0.5em]\n\\text{where } E[Cost_{DALY}] = \\frac{Cost_{treaty,DALY}}{P_{success}} = \\frac{\\$0.00177}{1\\%} = \\$0.177 \\\\[0.5em]\n\\text{where } Cost_{treaty,DALY} = \\frac{Cost_{campaign}}{DALYs_{max}} = \\frac{\\$1B}{565B} = \\$0.00177 \\\\[0.5em]\n\\text{where } Cost_{campaign} \\\\\n= Budget_{viral,base} + Budget_{lobby,treaty} \\\\\n+ Budget_{reserve} \\\\\n= \\$250M + \\$650M + \\$100M \\\\\n= \\$1B \\\\[0.5em]\n\\text{where } DALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B\n\\end{gathered}",
};

export const TREATY_LIVES_SAVED_ANNUAL_GLOBAL: Parameter = {
  value: 2446.0,
  unit: "lives/year",
  displayName: "Annual Lives Saved from 1% Reduction in Conflict Deaths",
  description: "Annual lives saved from 1% reduction in conflict deaths",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/parameters-and-calculations#sec-treaty_lives_saved_annual_global",
  confidence: "high",
  formula: "TOTAL_DEATHS × REDUCTION_PCT",
  latex: "\\begin{gathered}\nLives_{treaty,ann} \\\\\n= Deaths_{conflict} \\times Reduce_{treaty} \\\\\n= 245{,}000 \\times 1\\% \\\\\n= 2{,}450 \\\\[0.5em]\n\\text{where } Deaths_{conflict} \\\\\n= Deaths_{combat} + Deaths_{state} + Deaths_{terror} \\\\\n= 234{,}000 + 2{,}700 + 8{,}300 \\\\\n= 245{,}000\n\\end{gathered}",
};

export const TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS: Parameter = {
  value: 172211487804.87805,
  unit: "USD/year",
  displayName: "1% treaty Basic Annual Benefits (Peace + R&D Savings)",
  description: "Basic annual benefits: peace dividend + Decentralized Framework for Drug Assessment R&D savings only (2 of 8 benefit categories, excludes regulatory delay value)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/parameters-and-calculations#sec-treaty_peace_plus_rd_annual_benefits",
  confidence: "high",
  formula: "PEACE_DIVIDEND + DFDA_RD_SAVINGS",
  latex: "\\begin{gathered}\nBenefit_{peace+RD} \\\\\n= Benefit_{peace,soc} + Benefit_{RD,ann} \\\\\n= \\$114B + \\$58.6B \\\\\n= \\$172B \\\\[0.5em]\n\\text{where } Benefit_{peace,soc} \\\\\n= Cost_{war,total} \\times Reduce_{treaty} \\\\\n= \\$11.4T \\times 1\\% \\\\\n= \\$114B \\\\[0.5em]\n\\text{where } Cost_{war,total} \\\\\n= Cost_{war,direct} + Cost_{war,indirect} \\\\\n= \\$7.66T + \\$3.7T \\\\\n= \\$11.4T \\\\[0.5em]\n\\text{where } Cost_{war,direct} \\\\\n= Loss_{life,conflict} + Damage_{infra,total} \\\\\n+ Disruption_{trade} + Spending_{mil} \\\\\n= \\$2.45T + \\$1.88T + \\$616B + \\$2.72T \\\\\n= \\$7.66T \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B \\\\[0.5em]\n\\text{where } Cost_{war,indirect} \\\\\n= Damage_{env} + Loss_{growth,mil} \\\\\n+ Loss_{capital,conflict} + Cost_{psych} \\\\\n+ Cost_{refugee} + Cost_{vet} \\\\\n= \\$100B + \\$2.72T + \\$300B + \\$232B + \\$150B + \\$200B \\\\\n= \\$3.7T \\\\[0.5em]\n\\text{where } Benefit_{RD,ann} \\\\\n= Spending_{trials} \\times Reduce_{pct} \\\\\n= \\$60B \\times 97.7\\% \\\\\n= \\$58.6B \\\\[0.5em]\n\\text{where } Reduce_{pct} \\\\\n= 1 - \\frac{Cost_{pragmatic,pt}}{Cost_{P3,pt}} \\\\\n= 1 - \\frac{\\$929}{\\$41K} \\\\\n= 97.7\\%\n\\end{gathered}",
};

export const TREATY_QALYS_GAINED_ANNUAL_GLOBAL: Parameter = {
  value: 85610.0,
  unit: "QALYs/year",
  displayName: "Annual QALYs Gained from Peace Dividend",
  description: "Annual QALYs gained from peace dividend (lives saved × QALYs/life)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/parameters-and-calculations#sec-treaty_qalys_gained_annual_global",
  confidence: "high",
  formula: "LIVES_SAVED × QALYS_PER_LIFE",
  latex: "\\begin{gathered}\nQALY_{treaty,ann} \\\\\n= QALY_{life} \\times Lives_{treaty,ann} \\\\\n= 35 \\times 2{,}450 \\\\\n= 85{,}600 \\\\[0.5em]\n\\text{where } Lives_{treaty,ann} \\\\\n= Deaths_{conflict} \\times Reduce_{treaty} \\\\\n= 245{,}000 \\times 1\\% \\\\\n= 2{,}450 \\\\[0.5em]\n\\text{where } Deaths_{conflict} \\\\\n= Deaths_{combat} + Deaths_{state} + Deaths_{terror} \\\\\n= 234{,}000 + 2{,}700 + 8{,}300 \\\\\n= 245{,}000\n\\end{gathered}",
};

export const TREATY_RECURRING_BENEFITS_ANNUAL: Parameter = {
  value: 172211487804.87805,
  unit: "USD/year",
  displayName: "1% treaty Recurring Annual Benefits",
  description: "Truly recurring annual benefits from 1% treaty: peace dividend ($113.6B/year) + R&D savings ($41.5B/year). Note: Health benefits are one-time timeline shifts, NOT included here.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/economics",
  confidence: "high",
  formula: "PEACE_DIVIDEND + RD_SAVINGS",
  latex: "\\begin{gathered}\nBenefit_{recur,ann} \\\\\n= Benefit_{RD,ann} + Benefit_{peace,soc} \\\\\n= \\$58.6B + \\$114B \\\\\n= \\$172B \\\\[0.5em]\n\\text{where } Benefit_{RD,ann} \\\\\n= Spending_{trials} \\times Reduce_{pct} \\\\\n= \\$60B \\times 97.7\\% \\\\\n= \\$58.6B \\\\[0.5em]\n\\text{where } Reduce_{pct} \\\\\n= 1 - \\frac{Cost_{pragmatic,pt}}{Cost_{P3,pt}} \\\\\n= 1 - \\frac{\\$929}{\\$41K} \\\\\n= 97.7\\% \\\\[0.5em]\n\\text{where } Benefit_{peace,soc} \\\\\n= Cost_{war,total} \\times Reduce_{treaty} \\\\\n= \\$11.4T \\times 1\\% \\\\\n= \\$114B \\\\[0.5em]\n\\text{where } Cost_{war,total} \\\\\n= Cost_{war,direct} + Cost_{war,indirect} \\\\\n= \\$7.66T + \\$3.7T \\\\\n= \\$11.4T \\\\[0.5em]\n\\text{where } Cost_{war,direct} \\\\\n= Loss_{life,conflict} + Damage_{infra,total} \\\\\n+ Disruption_{trade} + Spending_{mil} \\\\\n= \\$2.45T + \\$1.88T + \\$616B + \\$2.72T \\\\\n= \\$7.66T \\\\[0.5em]\n\\text{where } Loss_{life,conflict} \\\\\n= Cost_{combat,human} + Cost_{state,human} \\\\\n+ Cost_{terror,human} \\\\\n= \\$2.34T + \\$27B + \\$83B \\\\\n= \\$2.45T \\\\[0.5em]\n\\text{where } Cost_{combat,human} \\\\\n= Deaths_{combat} \\times VSL \\\\\n= 234{,}000 \\times \\$10M \\\\\n= \\$2.34T \\\\[0.5em]\n\\text{where } Cost_{state,human} \\\\\n= Deaths_{state} \\times VSL \\\\\n= 2{,}700 \\times \\$10M \\\\\n= \\$27B \\\\[0.5em]\n\\text{where } Cost_{terror,human} \\\\\n= Deaths_{terror} \\times VSL \\\\\n= 8{,}300 \\times \\$10M \\\\\n= \\$83B \\\\[0.5em]\n\\text{where } Damage_{infra,total} \\\\\n= Damage_{comms} + Damage_{edu} + Damage_{energy} \\\\\n+ Damage_{health} + Damage_{transport} \\\\\n+ Damage_{water} \\\\\n= \\$298B + \\$234B + \\$422B + \\$166B + \\$487B + \\$268B \\\\\n= \\$1.88T \\\\[0.5em]\n\\text{where } Disruption_{trade} \\\\\n= Disruption_{currency} + Disruption_{energy} \\\\\n+ Disruption_{shipping} + Disruption_{supply} \\\\\n= \\$57.4B + \\$125B + \\$247B + \\$187B \\\\\n= \\$616B \\\\[0.5em]\n\\text{where } Cost_{war,indirect} \\\\\n= Damage_{env} + Loss_{growth,mil} \\\\\n+ Loss_{capital,conflict} + Cost_{psych} \\\\\n+ Cost_{refugee} + Cost_{vet} \\\\\n= \\$100B + \\$2.72T + \\$300B + \\$232B + \\$150B + \\$200B \\\\\n= \\$3.7T\n\\end{gathered}",
};

export const TREATY_ROI_EXISTING_DRUGS_ONLY: Parameter = {
  value: 250919.99999999997,
  unit: "ratio",
  displayName: "Treaty ROI - Historical Rate (Existing Drugs)",
  description: "Treaty ROI based on historical rate of drug development (existing drugs only). Total one-time benefit from avoiding regulatory delay for drugs already in development divided by $1B campaign cost. Excludes future innovation effects.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/figures/dfda-investment-returns-bar-chart",
  confidence: "high",
  formula: "HISTORICAL_PROGRESS_TOTAL ÷ CAMPAIGN_COST",
  latex: "\\begin{gathered}\nROI_{drugs} = \\frac{Loss_{lag}}{Cost_{campaign}} = \\frac{\\$251T}{\\$1B} = 251{,}000 \\\\[0.5em]\n\\text{where } Loss_{lag} \\\\\n= Deaths_{lag,total} \\times (LE_{global} - Age_{death,delay}) \\times Value_{QALY} \\\\\n= 98.4M \\times (79 - 62) \\times \\$150K \\\\\n= \\$251T \\\\[0.5em]\n\\text{where } Deaths_{lag,total} \\\\\n= T_{lag} \\times 12000000 \\\\\n= 8.2 \\times 12000000 \\\\\n= 98.4M \\\\[0.5em]\n\\text{where } Cost_{campaign} \\\\\n= Budget_{viral,base} + Budget_{lobby,treaty} \\\\\n+ Budget_{reserve} \\\\\n= \\$250M + \\$650M + \\$100M \\\\\n= \\$1B\n\\end{gathered}",
};

export const TREATY_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG: Parameter = {
  value: 84773300.3851355,
  unit: "ratio",
  displayName: "Treaty ROI - Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Increased Trial Throughput",
  description: "Treaty ROI from elimination of efficacy lag plus earlier treatment discovery from increased trial throughput. Total one-time benefit divided by campaign cost. This is the primary ROI estimate for total health benefits.",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/figures/dfda-investment-returns-bar-chart",
  confidence: "medium",
  formula: "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE ÷ CAMPAIGN_COST",
  latex: "\\begin{gathered}\nROI_{max} = \\frac{Value_{max}}{Cost_{campaign}} = \\frac{\\$84800T}{\\$1B} = 84.8M \\\\[0.5em]\n\\text{where } Value_{max} \\\\\n= DALYs_{max} \\times Value_{QALY} \\\\\n= 565B \\times \\$150K \\\\\n= \\$84800T \\\\[0.5em]\n\\text{where } DALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Cost_{campaign} \\\\\n= Budget_{viral,base} + Budget_{lobby,treaty} \\\\\n+ Budget_{reserve} \\\\\n= \\$250M + \\$650M + \\$100M \\\\\n= \\$1B\n\\end{gathered}",
};

export const TREATY_TOTAL_ANNUAL_COSTS: Parameter = {
  value: 290000000.0,
  unit: "USD/year",
  displayName: "Total Annual Treaty System Costs",
  description: "Total annual system costs (campaign + Decentralized Framework for Drug Assessment operations)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/parameters-and-calculations#sec-treaty_total_annual_costs",
  confidence: "high",
  formula: "CAMPAIGN_ANNUAL + DFDA_OPEX",
  latex: "\\begin{gathered}\nCost_{treaty,ann} \\\\\n= OPEX_{dFDA} + Cost_{camp,amort} \\\\\n= \\$40M + \\$250M \\\\\n= \\$290M \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Cost_{camp,amort} = \\frac{Cost_{campaign}}{T_{campaign}} = \\frac{\\$1B}{4} = \\$250M \\\\[0.5em]\n\\text{where } Cost_{campaign} \\\\\n= Budget_{viral,base} + Budget_{lobby,treaty} \\\\\n+ Budget_{reserve} \\\\\n= \\$250M + \\$650M + \\$100M \\\\\n= \\$1B\n\\end{gathered}",
};

export const TREATY_VS_BED_NETS_MULTIPLIER: Parameter = {
  value: 50298.82489518039,
  unit: "ratio",
  displayName: "Cost-Effectiveness vs Bed Nets Multiplier",
  description: "How many times more cost-effective than bed nets (using $89/DALY midpoint estimate)",
  sourceType: "calculated",
  confidence: "high",
  formula: "BED_NETS_COST_PER_DALY ÷ TREATY_COST_PER_DALY",
  latex: "\\begin{gathered}\nk_{treaty:nets} \\\\\n= \\frac{Cost_{nets}}{Cost_{treaty,DALY}} \\\\\n= \\frac{\\$89}{\\$0.00177} \\\\\n= 50{,}300 \\\\[0.5em]\n\\text{where } Cost_{treaty,DALY} = \\frac{Cost_{campaign}}{DALYs_{max}} = \\frac{\\$1B}{565B} = \\$0.00177 \\\\[0.5em]\n\\text{where } Cost_{campaign} \\\\\n= Budget_{viral,base} + Budget_{lobby,treaty} \\\\\n+ Budget_{reserve} \\\\\n= \\$250M + \\$650M + \\$100M \\\\\n= \\$1B \\\\[0.5em]\n\\text{where } DALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const TRIAL_CAPACITY_CUMULATIVE_YEARS_20YR: Parameter = {
  value: 246.10503654183898,
  unit: "years",
  displayName: "Cumulative Trial Capacity Years Over 20 Years",
  description: "Cumulative trial-capacity-equivalent years over 20-year period",
  sourceType: "calculated",
  confidence: "high",
  formula: "DFDA_TRIAL_CAPACITY_MULTIPLIER × 20 YEARS",
  latex: "\\begin{gathered}\nCapacity_{20yr} = k_{capacity} \\times 20 = 12.3 \\times 20 = 246 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const TYPE_II_ERROR_COST_RATIO: Parameter = {
  value: 3067.7541293180693,
  unit: "ratio",
  displayName: "Ratio of Type Ii Error Cost to Type I Error Benefit",
  description: "Ratio of Type II error cost to Type I error benefit (harm from delay vs. harm prevented)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/regulatory-mortality-analysis#risk-analysis",
  confidence: "medium",
  formula: "TYPE_II_COST ÷ TYPE_I_BENEFIT",
  latex: "\\begin{gathered}\nRatio_{TypeII} = \\frac{DALYs_{lag}}{DALY_{TypeI}} = \\frac{7.94B}{2.59M} = 3{,}070 \\\\[0.5em]\n\\text{where } DALYs_{lag} = YLL_{lag} + YLD_{lag} = 7.07B + 873M = 7.94B \\\\[0.5em]\n\\text{where } YLL_{lag} \\\\\n= Deaths_{lag} \\times (LE_{global} - Age_{death,delay}) \\\\\n= 416M \\times (79 - 62) \\\\\n= 7.07B \\\\[0.5em]\n\\text{where } Deaths_{lag} \\\\\n= T_{lag} \\times Deaths_{disease,daily} \\times 338 \\\\\n= 8.2 \\times 150{,}000 \\times 338 \\\\\n= 416M \\\\[0.5em]\n\\text{where } YLD_{lag} \\\\\n= Deaths_{lag} \\times T_{suffering} \\times DW_{chronic} \\\\\n= 416M \\times 6 \\times 0.35 \\\\\n= 873M \\\\[0.5em]\n\\text{where } Deaths_{lag} \\\\\n= T_{lag} \\times Deaths_{disease,daily} \\times 338 \\\\\n= 8.2 \\times 150{,}000 \\times 338 \\\\\n= 416M \\\\[0.5em]\n\\text{where } DALY_{TypeI} = DALY_{thal} \\times 62 = 41{,}800 \\times 62 = 2.59M \\\\[0.5em]\n\\text{where } DALY_{thal} \\\\\n= YLD_{thal} + YLL_{thal} \\\\\n= 13{,}000 + 28{,}800 \\\\\n= 41{,}800 \\\\[0.5em]\n\\text{where } YLD_{thal} \\\\\n= DW_{thal} \\times N_{thal,survive} \\times LE_{thal} \\\\\n= 0.4 \\times 540 \\times 60 \\\\\n= 13{,}000 \\\\[0.5em]\n\\text{where } N_{thal,survive} \\\\\n= N_{thal,US,prevent} \\times (1 - Rate_{thal,mort}) \\\\\n= 900 \\times (1 - 40\\%) \\\\\n= 540 \\\\[0.5em]\n\\text{where } N_{thal,US,prevent} \\\\\n= N_{thal,global} \\times Pct_{US,1960} \\\\\n= 15{,}000 \\times 6\\% \\\\\n= 900 \\\\[0.5em]\n\\text{where } YLL_{thal} = Deaths_{thal} \\times 80 = 360 \\times 80 = 28{,}800 \\\\[0.5em]\n\\text{where } Deaths_{thal} \\\\\n= Rate_{thal,mort} \\times N_{thal,US,prevent} \\\\\n= 40\\% \\times 900 \\\\\n= 360 \\\\[0.5em]\n\\text{where } N_{thal,US,prevent} \\\\\n= N_{thal,global} \\times Pct_{US,1960} \\\\\n= 15{,}000 \\times 6\\% \\\\\n= 900\n\\end{gathered}",
};

export const TYPE_I_ERROR_BENEFIT_DALYS: Parameter = {
  value: 2589120.0,
  unit: "DALYs",
  displayName: "Maximum DALYs Saved by FDA Preventing Unsafe Drugs (1962-2024)",
  description: "Maximum DALYs saved by FDA preventing unsafe drugs over 62-year period 1962-2024 (extreme overestimate: one Thalidomide-scale event per year)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/regulatory-mortality-analysis#risk-analysis",
  confidence: "low",
  formula: "THALIDOMIDE_DALYS_PER_EVENT × 62 years",
  latex: "\\begin{gathered}\nDALY_{TypeI} = DALY_{thal} \\times 62 = 41{,}800 \\times 62 = 2.59M \\\\[0.5em]\n\\text{where } DALY_{thal} \\\\\n= YLD_{thal} + YLL_{thal} \\\\\n= 13{,}000 + 28{,}800 \\\\\n= 41{,}800 \\\\[0.5em]\n\\text{where } YLD_{thal} \\\\\n= DW_{thal} \\times N_{thal,survive} \\times LE_{thal} \\\\\n= 0.4 \\times 540 \\times 60 \\\\\n= 13{,}000 \\\\[0.5em]\n\\text{where } N_{thal,survive} \\\\\n= N_{thal,US,prevent} \\times (1 - Rate_{thal,mort}) \\\\\n= 900 \\times (1 - 40\\%) \\\\\n= 540 \\\\[0.5em]\n\\text{where } N_{thal,US,prevent} \\\\\n= N_{thal,global} \\times Pct_{US,1960} \\\\\n= 15{,}000 \\times 6\\% \\\\\n= 900 \\\\[0.5em]\n\\text{where } YLL_{thal} = Deaths_{thal} \\times 80 = 360 \\times 80 = 28{,}800 \\\\[0.5em]\n\\text{where } Deaths_{thal} \\\\\n= Rate_{thal,mort} \\times N_{thal,US,prevent} \\\\\n= 40\\% \\times 900 \\\\\n= 360 \\\\[0.5em]\n\\text{where } N_{thal,US,prevent} \\\\\n= N_{thal,global} \\times Pct_{US,1960} \\\\\n= 15{,}000 \\times 6\\% \\\\\n= 900\n\\end{gathered}",
};

export const UNEXPLORED_RATIO: Parameter = {
  value: 0.996578947368421,
  unit: "percentage",
  displayName: "Unexplored Therapeutic Frontier",
  description: "Fraction of possible drug-disease space that remains unexplored (>99%)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  formula: "1 - EXPLORATION_RATIO",
  latex: "\\begin{gathered}\nRatio_{unexplored} \\\\\n= 1 - \\frac{N_{tested}}{N_{combos}} \\\\\n= 1 - \\frac{32{,}500}{9.5M} \\\\\n= 99.7\\% \\\\[0.5em]\n\\text{where } N_{combos} \\\\\n= N_{safe} \\times N_{diseases,trial} \\\\\n= 9{,}500 \\times 1{,}000 \\\\\n= 9.5M\n\\end{gathered}",
};

export const US_CONGRESS_FULL_ADVOCACY_COST: Parameter = {
  value: 5350000000.0,
  unit: "USD",
  displayName: "US Congress Full Advocacy Cost",
  description: "Upper-bound advocacy cost to match career incentives for all 535 members of Congress",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/cost-of-change-analysis#us-political-reform-scenarios",
  confidence: "medium",
  formula: "CONGRESS_MEMBERS x POST_OFFICE_VALUE",
  latex: "\\begin{gathered}\nCost_{US,congress} \\\\\n= N_{congress} \\times V_{post-office} \\\\\n= 535 \\times \\$10M \\\\\n= \\$5.35B\n\\end{gathered}",
};

export const US_MAJOR_DISEASES_TOTAL_ANNUAL_COST: Parameter = {
  value: 1253000000000.0,
  unit: "USD",
  displayName: "US Major Diseases Total Annual Cost",
  description: "Total annual US cost of major diseases (diabetes, Alzheimer's, heart disease, cancer)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/solution/aligning-incentives#insurance-companies",
  confidence: "high",
  formula: "DIABETES + ALZHEIMERS + HEART + CANCER",
  latex: "\\begin{gathered}\nCost_{disease,US} \\\\\n= Cost_{ALZ,US} + Cost_{cancer,US} + Cost_{diabetes,US} \\\\\n+ Cost_{heart,US} \\\\\n= \\$355B + \\$208B + \\$327B + \\$363B \\\\\n= \\$1.25T\n\\end{gathered}",
};

export const US_SENATE_TREATY_ADVOCACY_COST: Parameter = {
  value: 670000000.0,
  unit: "USD",
  displayName: "US Senate Treaty Advocacy Cost",
  description: "Upper-bound advocacy cost to match career incentives for 67 senators (treaty ratification threshold)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/cost-of-change-analysis#us-political-reform-scenarios",
  confidence: "medium",
  formula: "SENATORS_FOR_TREATY x POST_OFFICE_VALUE",
  latex: "\\begin{gathered}\nCost_{US,senate} \\\\\n= N_{senators,treaty} \\times V_{post-office} \\\\\n= 67 \\times \\$10M \\\\\n= \\$670M\n\\end{gathered}",
};

export const WILLING_TRIAL_PARTICIPANTS_GLOBAL: Parameter = {
  value: 1075200000.0,
  unit: "people",
  displayName: "Global Patients Willing to Participate in Clinical Trials",
  description: "Global chronic disease patients willing to participate in trials (2.4B × 44.8%)",
  sourceType: "calculated",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/clinical-trial-participants#willingness-gap",
  confidence: "medium",
  formula: "CURRENT_DISEASE_PATIENTS_GLOBAL × PATIENT_WILLINGNESS_TRIAL_PARTICIPATION_PCT",
  latex: "\\begin{gathered}\nN_{willing} \\\\\n= N_{patients} \\times Pct_{willing} \\\\\n= 2.4B \\times 44.8\\% \\\\\n= 1.08B\n\\end{gathered}",
};

// ============================================================================
// Core Definitions
// ============================================================================

export const ADAPTABLE_TRIAL_PATIENTS: Parameter = {
  value: 15076.0,
  unit: "patients",
  displayName: "ADAPTABLE Trial Patients Enrolled",
  description: "Patients enrolled in ADAPTABLE trial (PCORnet 2016-2019). Enrolled across 40 clinical sites. Precise count from trial completion records.",
  sourceType: "definition",
  sourceRef: "pragmatic-trials-cost-advantage",
  confidence: "high",
};

export const APPROVED_DRUG_DISEASE_PAIRINGS: Parameter = {
  value: 1750.0,
  unit: "pairings",
  displayName: "Approved Drug-Disease Pairings",
  description: "Unique approved drug-disease pairings (FDA-approved uses, midpoint of 1,500-2,000 range)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  confidenceInterval: [1500.0, 2000.0],
};

export const BAD_POLICY_US_OVERLAP_DISCOUNT: Parameter = {
  value: 0.85,
  unit: "ratio",
  displayName: "Overlap Discount Factor",
  description: "Discount factor to account for overlap between bad policy cost categories. Fossil fuel externalities partially overlap with climate/health costs counted elsewhere. Migration restrictions partially captured in labor market inefficiencies.",
  sourceType: "definition",
  confidence: "low",
};

export const CAMPAIGN_CELEBRITY_ENDORSEMENT: Parameter = {
  value: 15000000.0,
  unit: "USD",
  displayName: "Celebrity and Influencer Endorsements",
  description: "Celebrity and influencer endorsements",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [10500000.0, 19500000.0],
};

export const CAMPAIGN_COMMUNITY_ORGANIZING: Parameter = {
  value: 30000000.0,
  unit: "USD",
  displayName: "Community Organizing and Ambassador Program Budget",
  description: "Community organizing and ambassador program budget",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [21000000.0, 39000000.0],
};

export const CAMPAIGN_CONTINGENCY: Parameter = {
  value: 50000000.0,
  unit: "USD",
  displayName: "Contingency Fund for Unexpected Costs",
  description: "Contingency fund for unexpected costs",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "high",
  confidenceInterval: [30000000.0, 80000000.0],
};

export const CAMPAIGN_DEFENSE_CONVERSION: Parameter = {
  value: 50000000.0,
  unit: "USD",
  displayName: "Defense Industry Conversion Program",
  description: "Defense industry conversion program",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "high",
  confidenceInterval: [40000000.0, 70000000.0],
};

export const CAMPAIGN_DEFENSE_LOBBYIST_BUDGET: Parameter = {
  value: 50000000.0,
  unit: "USD",
  displayName: "Budget for Co-Opting Defense Industry Lobbyists",
  description: "Budget for co-opting defense industry lobbyists",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [35000000.0, 65000000.0],
};

export const CAMPAIGN_HEALTHCARE_ALIGNMENT: Parameter = {
  value: 35000000.0,
  unit: "USD",
  displayName: "Healthcare Industry Alignment and Partnerships",
  description: "Healthcare industry alignment and partnerships",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [24500000.0, 45500000.0],
};

export const CAMPAIGN_INFRASTRUCTURE: Parameter = {
  value: 20000000.0,
  unit: "USD",
  displayName: "Campaign Operational Infrastructure",
  description: "Campaign operational infrastructure",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [14000000.0, 26000000.0],
};

export const CAMPAIGN_LEGAL_AI_BUDGET: Parameter = {
  value: 50000000.0,
  unit: "USD",
  displayName: "AI-Assisted Legal Work Budget",
  description: "AI-assisted legal work budget",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [35000000.0, 65000000.0],
};

export const CAMPAIGN_LEGAL_DEFENSE: Parameter = {
  value: 20000000.0,
  unit: "USD",
  displayName: "Legal Defense Fund",
  description: "Legal defense fund",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [14000000.0, 26000000.0],
};

export const CAMPAIGN_LEGAL_WORK: Parameter = {
  value: 60000000.0,
  unit: "USD",
  displayName: "Legal Drafting and Compliance Work",
  description: "Legal drafting and compliance work",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "high",
  confidenceInterval: [50000000.0, 80000000.0],
};

export const CAMPAIGN_LOBBYING_EU: Parameter = {
  value: 40000000.0,
  unit: "USD",
  displayName: "EU Lobbying Campaign Budget",
  description: "EU lobbying campaign budget",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [28000000.0, 52000000.0],
};

export const CAMPAIGN_LOBBYING_G20_MILLIONS: Parameter = {
  value: 35000000.0,
  unit: "USD",
  displayName: "G20 Countries Lobbying Budget",
  description: "G20 countries lobbying budget",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_LOBBYING_US: Parameter = {
  value: 50000000.0,
  unit: "USD",
  displayName: "US Lobbying Campaign Budget",
  description: "US lobbying campaign budget",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [35000000.0, 65000000.0],
};

export const CAMPAIGN_MEDIA_BUDGET_MAX: Parameter = {
  value: 1000000000.0,
  unit: "USD",
  displayName: "Maximum Mass Media Campaign Budget",
  description: "Maximum mass media campaign budget",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [700000000.0, 1300000000.0],
};

export const CAMPAIGN_MEDIA_BUDGET_MIN: Parameter = {
  value: 500000000.0,
  unit: "USD",
  displayName: "Minimum Mass Media Campaign Budget",
  description: "Minimum mass media campaign budget",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [350000000.0, 650000000.0],
};

export const CAMPAIGN_OPPOSITION_RESEARCH: Parameter = {
  value: 25000000.0,
  unit: "USD",
  displayName: "Opposition Research and Rapid Response",
  description: "Opposition research and rapid response",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [17500000.0, 32500000.0],
};

export const CAMPAIGN_PHASE1_BUDGET: Parameter = {
  value: 200000000.0,
  unit: "USD",
  displayName: "Phase 1 Campaign Budget",
  description: "Phase 1 campaign budget (Foundation, Year 1)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [140000000.0, 260000000.0],
};

export const CAMPAIGN_PHASE2_BUDGET: Parameter = {
  value: 500000000.0,
  unit: "USD",
  displayName: "Phase 2 Campaign Budget",
  description: "Phase 2 campaign budget (Scale & Momentum, Years 2-3)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [350000000.0, 650000000.0],
};

export const CAMPAIGN_PILOT_PROGRAMS: Parameter = {
  value: 30000000.0,
  unit: "USD",
  displayName: "Pilot Program Testing in Small Countries",
  description: "Pilot program testing in small countries",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [21000000.0, 39000000.0],
};

export const CAMPAIGN_PLATFORM_DEVELOPMENT: Parameter = {
  value: 35000000.0,
  unit: "USD",
  displayName: "Voting Platform and Technology Development",
  description: "Voting platform and technology development",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "high",
  confidenceInterval: [25000000.0, 50000000.0],
};

export const CAMPAIGN_REGULATORY_NAVIGATION: Parameter = {
  value: 20000000.0,
  unit: "USD",
  displayName: "Regulatory Compliance and Navigation",
  description: "Regulatory compliance and navigation",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [14000000.0, 26000000.0],
};

export const CAMPAIGN_SCALING_PREP: Parameter = {
  value: 30000000.0,
  unit: "USD",
  displayName: "Scaling Preparation and Blueprints",
  description: "Scaling preparation and blueprints",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [21000000.0, 39000000.0],
};

export const CAMPAIGN_STAFF_BUDGET: Parameter = {
  value: 40000000.0,
  unit: "USD",
  displayName: "Campaign Core Team Staff Budget",
  description: "Campaign core team staff budget",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [28000000.0, 52000000.0],
};

export const CAMPAIGN_SUPER_PAC_BUDGET: Parameter = {
  value: 30000000.0,
  unit: "USD",
  displayName: "Super PAC Campaign Expenditures",
  description: "Super PAC campaign expenditures",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [21000000.0, 39000000.0],
};

export const CAMPAIGN_TECH_PARTNERSHIPS: Parameter = {
  value: 25000000.0,
  unit: "USD",
  displayName: "Tech Industry Partnerships and Infrastructure",
  description: "Tech industry partnerships and infrastructure",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [17500000.0, 32500000.0],
};

export const CAMPAIGN_TREATY_IMPLEMENTATION: Parameter = {
  value: 40000000.0,
  unit: "USD",
  displayName: "Post-Victory Treaty Implementation Support",
  description: "Post-victory treaty implementation support",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "high",
  confidenceInterval: [30000000.0, 55000000.0],
};

export const CAMPAIGN_VIRAL_CONTENT_BUDGET: Parameter = {
  value: 40000000.0,
  unit: "USD",
  displayName: "Viral Marketing Content Creation Budget",
  description: "Viral marketing content creation budget",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  confidenceInterval: [28000000.0, 52000000.0],
};

export const CAREGIVER_COST_ANNUAL: Parameter = {
  value: 6000.0,
  unit: "USD/year",
  displayName: "Annual Cost of Unpaid Caregiving",
  description: "Annual cost of unpaid caregiving (replacement cost method)",
  sourceType: "definition",
  sourceRef: "unpaid-caregiver-hours-economic-value",
  confidence: "high",
  formula: "HOURS_PER_MONTH × MONTHS_PER_YEAR × VALUE_PER_HOUR",
};

export const CELL_THERAPY_APPROACHES: Parameter = {
  value: 500.0,
  unit: "approaches",
  displayName: "Cell Therapy Approaches",
  description: "Distinct cell therapy approaches (CAR-T variants, iPSCs, MSCs, organoids)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  confidenceInterval: [300.0, 800.0],
};

export const CHILDHOOD_VACCINATION_COST_PER_DALY: Parameter = {
  value: 30.0,
  unit: "USD/DALY",
  displayName: "Childhood Vaccination Cost per DALY (Estimated)",
  description: "Estimated cost per DALY for US childhood vaccination programs. Note: US cost-effectiveness studies primarily use cost per QALY (Quality-Adjusted Life Year) rather than cost per DALY. This estimate is derived from program costs and benefits for comparison purposes only.",
  sourceType: "definition",
  sourceRef: "childhood-vaccination-roi",
  confidence: "low",
};

export const CONCENTRATED_INTEREST_SECTOR_MARKET_CAP_USD: Parameter = {
  value: 5000000000000.0,
  unit: "USD",
  displayName: "Concentrated Interest Sector Market Cap",
  description: "Estimated combined market capitalization of concentrated interest opposition (defense, fossil fuel, etc.)",
  sourceType: "definition",
  confidence: "high",
};

export const CURRENT_PATIENT_PARTICIPATION_RATE: Parameter = {
  value: 0.0007916666666666666,
  unit: "rate",
  displayName: "Current Patient Participation Rate in Clinical Trials",
  description: "Current patient participation rate in clinical trials (0.08% = 1.9M participants / 2.4B disease patients)",
  sourceType: "definition",
  sourceRef: "clinical-trial-patient-participation-rate",
  confidence: "high",
  formula: "CURRENT_TRIAL_SLOTS / DISEASE_PATIENTS",
  latex: "\\begin{gathered}\nRate_{part} \\\\\n= \\frac{Slots_{curr}}{N_{patients}} \\\\\n= \\frac{1.9M}{2.4B} \\\\\n= 0.0792\\%\n\\end{gathered}",
};

export const DAYS_PER_YEAR: Parameter = {
  value: 365.0,
};

export const DCT_PLATFORM_FUNDING_MEDIUM: Parameter = {
  value: 500000000.0,
  unit: "USD",
  displayName: "Mid-Range Funding for Commercial Dct Platform",
  description: "Mid-range funding for commercial DCT platform",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#analogous-rom",
  confidence: "high",
};

export const DEFENSE_SECTOR_RETENTION_PCT: Parameter = {
  value: 0.99,
  unit: "rate",
  displayName: "Percentage of Budget Defense Sector Keeps Under 1% treaty",
  description: "Percentage of budget defense sector keeps under 1% treaty",
  sourceType: "definition",
  confidence: "high",
};

export const DFDA_DIRECT_FUNDING_COST_PER_DALY: Parameter = {
  value: 0.8409664747187287,
  unit: "USD/DALY",
  displayName: "dFDA Direct Funding Cost per DALY",
  description: "Cost per DALY if philanthropists/governments directly funded $21.76B/year for ~46.5 years (queue clearance period, NPV: ~$541.9B) instead of treaty campaign ($1B). Treaty achieves 542× leverage: $1B campaign unlocks government funding for 46.5 years (NPV: $541.9B), avoiding direct philanthropic commitment. Both achieve same 200B DALY timeline shift benefit. Still cost-effective vs bed nets ($89.0/DALY).",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper",
  confidence: "medium",
  formula: "NPV_DIRECT_FUNDING ÷ DALYS_TIMELINE_SHIFT",
  latex: "\\begin{gathered}\nCost_{direct,DALY} = \\frac{NPV_{direct}}{DALYs_{max}} = \\frac{\\$475B}{565B} = \\$0.841 \\\\[0.5em]\n\\text{where } NPV_{direct} \\\\\n= \\frac{T_{queue,dFDA}}{Treasury_{RD,ann} \\times r_{discount}} \\\\\n= \\frac{36}{\\$21.8B \\times 3\\%} \\\\\n= \\$475B \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } T_{queue,dFDA} = \\frac{T_{queue,SQ}}{k_{capacity}} = \\frac{443}{12.3} = 36 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } DALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_DIRECT_FUNDING_QUEUE_CLEARANCE_NPV: Parameter = {
  value: 475276690501.0616,
  unit: "USD",
  displayName: "dFDA Direct Funding NPV (Queue Clearance Period)",
  description: "NPV of direct funding ($21.76B/year for medical research after bond/IAB allocations) for the ~46.5-year queue clearance period. Alternative scenario: instead of $1B treaty campaign to unlock government funding, philanthropists/NIH directly fund clinical trials until disease queue is cleared. Funding period is queue clearance time (46.5 years with 9.5× trial capacity), not timeline shift amount (207 years). After queue is cleared, the timeline shift benefit (200B DALYs) is fully realized.",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper",
  confidence: "high",
  formula: "ANNUAL_FUNDING × [(1 - (1 + r)^-T) / r] where T = queue clearance time",
  latex: "NPV_{direct} = Funding_{ann} \\times \\frac{1 - (1+r)^{-T}}{r}",
};

export const DFDA_NPV_ADOPTION_RAMP_YEARS: Parameter = {
  value: 5.0,
  unit: "years",
  displayName: "Years to Reach Full Decentralized Framework for Drug Assessment Adoption",
  description: "Years to reach full Decentralized Framework for Drug Assessment adoption",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#adoption-curve",
  confidence: "high",
};

export const DFDA_NPV_ANNUAL_OPEX: Parameter = {
  value: 18950000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Core framework Annual OPEX",
  description: "Decentralized Framework for Drug Assessment Core framework annual opex (midpoint of $11-26.5M)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#npv-costs",
  confidence: "high",
  confidenceInterval: [11000000.0, 26500000.0],
};

export const DFDA_NPV_UPFRONT_COST: Parameter = {
  value: 40000000.0,
  unit: "USD",
  displayName: "Decentralized Framework for Drug Assessment Core framework Build Cost",
  description: "Decentralized Framework for Drug Assessment Core framework build cost",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#npv-costs",
  confidence: "high",
  confidenceInterval: [25000000.0, 65000000.0],
};

export const DFDA_OBSERVATIONAL_COST_PER_PATIENT: Parameter = {
  value: 0.1,
  unit: "USD/patient",
  displayName: "Stage 1 Observational Analysis Cost per Patient",
  description: "Order-of-magnitude estimate for Stage 1 observational signal detection (PIS calculation). Validated by FDA Sentinel benchmark (~$1/patient/year for similar drug safety analysis at 100M+ scale). True cost varies with scale and complexity; exact value less important than order-of-magnitude difference vs pragmatic trials (~$500-929/patient) and traditional Phase 3 (~$41,000/patient).",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/data-storage-costs#cost-analysis",
  confidence: "high",
  confidenceInterval: [0.03, 1.0],
};

export const DFDA_OPEX_COMMUNITY: Parameter = {
  value: 2000000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Community Support Costs",
  description: "Decentralized Framework for Drug Assessment community support costs",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#opex-breakdown",
  confidence: "high",
  confidenceInterval: [1000000.0, 3000000.0],
};

export const DFDA_OPEX_INFRASTRUCTURE: Parameter = {
  value: 8000000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Infrastructure Costs",
  description: "Decentralized Framework for Drug Assessment infrastructure costs (cloud, security)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#opex-breakdown",
  confidence: "high",
  confidenceInterval: [5000000.0, 12000000.0],
};

export const DFDA_OPEX_PCT_OF_TREATY_FUNDING: Parameter = {
  value: 0.0014705882352941176,
  unit: "rate",
  displayName: "Decentralized Framework for Drug Assessment Overhead Percentage of Treaty Funding",
  description: "Percentage of treaty funding allocated to Decentralized Framework for Drug Assessment framework overhead",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/economics#funding-allocation",
  confidence: "high",
  formula: "DFDA_OPEX / TREATY_FUNDING",
  latex: "\\begin{gathered}\nOPEX_{pct} = \\frac{OPEX_{dFDA}}{Funding_{treaty}} = \\frac{\\$40M}{\\$27.2B} = 0.147\\% \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DFDA_OPEX_PLATFORM_MAINTENANCE: Parameter = {
  value: 15000000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Maintenance Costs",
  description: "Decentralized Framework for Drug Assessment maintenance costs",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#opex-breakdown",
  confidence: "high",
  confidenceInterval: [10000000.0, 22000000.0],
};

export const DFDA_OPEX_REGULATORY: Parameter = {
  value: 5000000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Regulatory Coordination Costs",
  description: "Decentralized Framework for Drug Assessment regulatory coordination costs",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#opex-breakdown",
  confidence: "high",
  confidenceInterval: [3000000.0, 8000000.0],
};

export const DFDA_OPEX_STAFF: Parameter = {
  value: 10000000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Staff Costs",
  description: "Decentralized Framework for Drug Assessment staff costs (minimal, AI-assisted)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#opex-breakdown",
  confidence: "high",
  confidenceInterval: [7000000.0, 15000000.0],
};

export const DFDA_STORAGE_COST_BACKUP_PER_PATIENT_MONTHLY: Parameter = {
  value: 0.2,
  unit: "USD/patient/month",
  displayName: "Backup/Redundancy Cost per Patient (Monthly)",
  description: "Backup and redundancy cost per patient per month. For data safety and compliance.",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/data-storage-costs#cost-analysis",
  confidence: "high",
  confidenceInterval: [0.1, 0.4],
};

export const DFDA_STORAGE_COST_COMPUTE_PER_PATIENT_MONTHLY: Parameter = {
  value: 0.2,
  unit: "USD/patient/month",
  displayName: "Compute/API Cost per Patient (Monthly)",
  description: "Compute and API cost per patient per month. For data processing, correlation analysis, and PIS calculation.",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/data-storage-costs#cost-analysis",
  confidence: "high",
  confidenceInterval: [0.1, 0.5],
};

export const DFDA_STORAGE_COST_DATABASE_PER_PATIENT_MONTHLY: Parameter = {
  value: 0.3,
  unit: "USD/patient/month",
  displayName: "Database Cost per Patient (Monthly)",
  description: "Database cost per patient per month. For structured data storage and querying.",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/data-storage-costs#cost-analysis",
  confidence: "high",
  confidenceInterval: [0.15, 0.6],
};

export const DFDA_STORAGE_COST_RAW_PER_PATIENT_MONTHLY: Parameter = {
  value: 0.02,
  unit: "USD/patient/month",
  displayName: "Raw Storage Cost per Patient (Monthly)",
  description: "Raw cloud storage cost per patient per month. Based on standard cloud storage rates for ~1GB patient data.",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/data-storage-costs#cost-analysis",
  confidence: "high",
  confidenceInterval: [0.01, 0.05],
};

export const DFDA_TARGET_COST_PER_PATIENT_USD: Parameter = {
  value: 1000.0,
  unit: "USD/patient",
  displayName: "Decentralized Framework for Drug Assessment Target Cost per Patient in USD",
  description: "Target cost per patient in USD (same as DFDA_TARGET_COST_PER_PATIENT but in dollars)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#cost-per-patient",
  confidence: "high",
};

export const DFDA_UPFRONT_BUILD: Parameter = {
  value: 40000000.0,
  unit: "USD",
  displayName: "Decentralized Framework for Drug Assessment One-Time Build Cost",
  description: "Decentralized Framework for Drug Assessment one-time build cost (central estimate)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#build-costs",
  confidence: "high",
};

export const DFDA_UPFRONT_BUILD_MAX: Parameter = {
  value: 46000000.0,
  unit: "USD",
  displayName: "Decentralized Framework for Drug Assessment One-Time Build Cost (Maximum)",
  description: "Decentralized Framework for Drug Assessment one-time build cost (high estimate)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#build-costs",
  confidence: "high",
};

export const DIH_NPV_ANNUAL_OPEX_INITIATIVES: Parameter = {
  value: 21100000.0,
  unit: "USD/year",
  displayName: "DIH Broader Initiatives Annual OPEX",
  description: "DIH broader initiatives annual opex (medium case)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#npv-costs",
  confidence: "high",
  confidenceInterval: [14000000.0, 32000000.0],
};

export const DIH_NPV_UPFRONT_COST_INITIATIVES: Parameter = {
  value: 229750000.0,
  unit: "USD",
  displayName: "DIH Broader Initiatives Upfront Cost",
  description: "DIH broader initiatives upfront cost (medium case)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper#npv-costs",
  confidence: "high",
  confidenceInterval: [150000000.0, 350000000.0],
};

export const DIH_TREASURY_MEDICAL_RESEARCH_PCT: Parameter = {
  value: 0.8,
  unit: "rate",
  displayName: "Medical Research Percentage of Treaty Funding",
  description: "Percentage of treaty funding allocated to medical research (after bond payouts and IAB incentives)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/economics#funding-allocation",
  confidence: "high",
  formula: "MEDICAL_RESEARCH_FUNDING / TREATY_FUNDING",
  latex: "\\begin{gathered}\nPct_{treasury,RD} = \\frac{Treasury_{RD,ann}}{Funding_{treaty}} = \\frac{\\$21.8B}{\\$27.2B} = 80\\% \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL: Parameter = {
  value: 21760000000.0,
  unit: "USD/year",
  displayName: "Annual Funding for Pragmatic Clinical Trials",
  description: "Annual funding for pragmatic clinical trials (treaty funding minus VICTORY Incentive Alignment Bond payouts and IAB political incentive mechanism)",
  sourceType: "definition",
  confidence: "high",
  formula: "TREATY_FUNDING - BOND_PAYOUT - IAB_POLITICAL_INCENTIVE_FUNDING",
  latex: "\\begin{gathered}\nTreasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DIH_TREASURY_TRIAL_SUBSIDIES_PCT: Parameter = {
  value: 0.7985294117647059,
  unit: "rate",
  displayName: "Patient Trial Subsidies Percentage of Treaty Funding",
  description: "Percentage of treaty funding going directly to patient trial subsidies",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/economics#funding-allocation",
  confidence: "high",
  formula: "TRIAL_SUBSIDIES / TREATY_FUNDING",
  latex: "\\begin{gathered}\nPct_{subsidies} = \\frac{Subsidies_{trial,ann}}{Funding_{treaty}} = \\frac{\\$21.7B}{\\$27.2B} = 79.9\\% \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const DISEASE_RELATED_CAREGIVER_PCT: Parameter = {
  value: 0.4,
  unit: "rate",
  displayName: "Percentage of Caregiving for Treatable Disease Conditions",
  description: "Percentage of caregiving for treatable disease conditions (vs aging, disability, children)",
  sourceType: "definition",
  sourceRef: "disease-related-caregiving-estimate",
  confidence: "high",
};

export const DISEASE_VS_TERRORISM_DEATHS_RATIO: Parameter = {
  value: 18357.81041388518,
  unit: "ratio",
  displayName: "Ratio of Annual Disease Deaths to 9/11 Terrorism Deaths",
  description: "Ratio of annual disease deaths to 9/11 terrorism deaths",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/economics",
  confidence: "high",
  formula: "ANNUAL_DISEASE_DEATHS ÷ 911_DEATHS",
  latex: "\\begin{gathered}\nRatio_{dis:terror} \\\\\n= \\frac{Deaths_{curable,ann}}{Deaths_{9/11}} \\\\\n= \\frac{55M}{3{,}000} \\\\\n= 18{,}400\n\\end{gathered}",
};

export const DISEASE_VS_WAR_DEATHS_RATIO: Parameter = {
  value: 224.8569092395748,
  unit: "ratio",
  displayName: "Ratio of Annual Disease Deaths to War Deaths",
  description: "Ratio of annual disease deaths to war deaths",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/economics",
  confidence: "high",
  formula: "ANNUAL_DISEASE_DEATHS ÷ WAR_DEATHS",
  latex: "\\begin{gathered}\nRatio_{dis:war} = \\frac{Deaths_{curable,ann}}{Deaths_{conflict}} = \\frac{55M}{245{,}000} = 225 \\\\[0.5em]\n\\text{where } Deaths_{conflict} \\\\\n= Deaths_{combat} + Deaths_{state} + Deaths_{terror} \\\\\n= 234{,}000 + 2{,}700 + 8{,}300 \\\\\n= 245{,}000\n\\end{gathered}",
};

export const EFFECTIVE_HOURLY_RATE_LIFETIME_BENEFIT: Parameter = {
  value: 4300000.0,
  unit: "USD",
  displayName: "Lifetime Benefit for Age 30 Baseline Scenario",
  description: "Lifetime benefit for age 30 baseline scenario ($4.3M)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/disease-eradication-personal-lifetime-wealth-calculations",
  confidence: "high",
  formula: "Total lifetime health gains from 1% treaty",
};

export const EPIGENETIC_TARGETS_COUNT: Parameter = {
  value: 1500.0,
  unit: "targets",
  displayName: "Epigenetic Drug Targets",
  description: "Druggable epigenetic targets (HDACs, DNMTs, histone modifiers, bromodomains)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  confidenceInterval: [1000.0, 2000.0],
};

export const EVENTUALLY_AVOIDABLE_DALY_PCT: Parameter = {
  value: 0.9262780790085205,
  unit: "percentage",
  displayName: "Eventually Avoidable DALY Percentage",
  description: "Percentage of DALYs that are eventually avoidable with sufficient biomedical research. Uses same methodology as EVENTUALLY_AVOIDABLE_DEATH_PCT. Most non-fatal chronic conditions (arthritis, depression, chronic pain) are also addressable through research, so the percentage is similar to deaths.",
  sourceType: "definition",
  confidence: "low",
  formula: "1 - FUNDAMENTALLY_UNAVOIDABLE_DEATH_PCT",
  confidenceInterval: [0.5, 0.98],
};

export const EVENTUALLY_AVOIDABLE_DEATH_PCT: Parameter = {
  value: 0.9262780790085205,
  unit: "percentage",
  displayName: "Eventually Avoidable Death Percentage",
  description: "Percentage of deaths that are eventually avoidable with sufficient biomedical research and technological advancement. Central estimate ~92% based on ~7.9% fundamentally unavoidable (primarily accidents). Wide uncertainty reflects debate over: (1) aging as addressable vs. fundamental, (2) asymptotic difficulty of last diseases, (3) multifactorial disease complexity.",
  sourceType: "definition",
  confidence: "low",
  formula: "1 - FUNDAMENTALLY_UNAVOIDABLE_DEATH_PCT",
  confidenceInterval: [0.5, 0.98],
};

export const FAMILY_OFFICE_INVESTMENT_MIN: Parameter = {
  value: 5000000.0,
  unit: "USD",
  displayName: "Minimum Investment for Family Offices",
  description: "Minimum investment for family offices",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/victory-bonds",
  confidence: "high",
};

export const FUNDAMENTALLY_UNAVOIDABLE_DEATH_PCT: Parameter = {
  value: 0.07372192099147949,
  unit: "percentage",
  displayName: "Fundamentally Unavoidable Death Percentage",
  description: "Percentage of deaths that are fundamentally unavoidable even with perfect biotechnology (primarily accidents). Calculated as Σ(disease_burden × (1 - max_cure_potential)) across all disease categories.",
  sourceType: "definition",
  confidence: "medium",
  formula: "Σ(DISEASE_BURDEN[cat] × (1 - RESEARCH_ACCELERATION_POTENTIAL[cat]))",
};

export const GLOBAL_MILITARY_SPENDING_POST_TREATY_ANNUAL_2024: Parameter = {
  value: 2692800000000.0,
  unit: "USD/year",
  displayName: "Global Military Spending After 1% Treaty Reduction",
  description: "Global military spending after 1% treaty reduction",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/strategy/treaty-adoption-strategy#post-treaty",
  confidence: "high",
  formula: "MILITARY_SPENDING × (1 - REDUCTION)",
  latex: "\\begin{gathered}\nSpending_{mil,post} \\\\\n= Spending_{mil} \\times (1 - Reduce_{treaty}) \\\\\n= \\$2.72T \\times (1 - 1\\%) \\\\\n= \\$2.69T\n\\end{gathered}",
};

export const GLOBAL_POLITICAL_REFORM_INVESTMENT: Parameter = {
  value: 125000000000.0,
  unit: "USD",
  displayName: "Global Political Reform Investment",
  description: "Estimated global advocacy investment for policy reform (NATO $65B + China $20B + Russia $10B + India $8B + others $22B). Upper bound representing full democratic engagement at scale.",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/cost-of-change-analysis#global-estimates",
  confidence: "low",
  formula: "NATO + China + Russia + India + other major spenders",
  confidenceInterval: [75000000000.0, 200000000000.0],
};

export const GLOBAL_POLITICAL_REFORM_INVESTMENT_MAXIMUM: Parameter = {
  value: 200000000000.0,
  unit: "USD",
  displayName: "Global Political Reform Investment (Maximum)",
  description: "Maximum plausible global political reform investment with substantial contingency for hidden channels, opposition counter-spending, and multiple election cycles. Stress-test upper bound.",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/cost-of-change-analysis",
  confidence: "low",
};

export const HOURS_PER_DAY: Parameter = {
  value: 24.0,
};

export const HOURS_PER_YEAR: Parameter = {
  value: 8760.0,
};

export const HUMAN_PROTEIN_CODING_GENES: Parameter = {
  value: 20000.0,
  unit: "genes",
  displayName: "Human Protein-Coding Genes",
  description: "Human protein-coding genes targetable by gene therapy, mRNA, or biologics (Human Genome Project consensus)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  confidenceInterval: [19000.0, 21000.0],
};

export const IAB_BOOTSTRAP_CAMPAIGN_COST: Parameter = {
  value: 100000000.0,
  unit: "USD",
  displayName: "IAB Bootstrap Campaign Cost",
  description: "Bootstrap campaign cost for initial IAB proof-of-concept. Range reflects uncertainty in required lobbying intensity, media spend, and organizational overhead.",
  sourceType: "definition",
  confidence: "high",
  confidenceInterval: [50000000.0, 200000000.0],
};

export const IAB_MECHANISM_ANNUAL_COST: Parameter = {
  value: 750000000.0,
  unit: "USD/year",
  displayName: "IAB Mechanism Annual Cost (High Estimate)",
  description: "Estimated annual cost of the IAB mechanism (high-end estimate including regulatory defense)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/incentive-alignment-bonds-paper#welfare-analysis",
  confidence: "high",
  confidenceInterval: [160000000.0, 750000000.0],
};

export const IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL: Parameter = {
  value: 2720000000.0,
  unit: "USD/year",
  displayName: "Annual IAB Political Incentive Funding",
  description: "Annual funding for IAB political incentive mechanism (independent expenditures supporting high-scoring politicians, post-office fellowship endowments, Public Good Score infrastructure)",
  sourceType: "definition",
  confidence: "high",
  formula: "TREATY_FUNDING × IAB_POLITICAL_INCENTIVE_PCT",
  latex: "\\begin{gathered}\nFunding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const IAB_POLITICAL_INCENTIVE_FUNDING_PCT: Parameter = {
  value: 0.1,
  unit: "rate",
  displayName: "IAB Political Incentive Funding Percentage",
  description: "Percentage of treaty funding allocated to Incentive Alignment Bond mechanism for political incentives (independent expenditures/PACs, post-office fellowships, Public Good Score infrastructure)",
  sourceType: "definition",
  confidence: "high",
};

export const INSTITUTIONAL_INVESTOR_MIN: Parameter = {
  value: 10000000.0,
  unit: "USD",
  displayName: "Minimum Investment for Institutional Investors",
  description: "Minimum investment for institutional investors",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/victory-bonds",
  confidence: "high",
};

export const LOBBYIST_BOND_INVESTMENT_MAX: Parameter = {
  value: 20000000.0,
  unit: "USD",
  displayName: "Maximum Bond Investment for Lobbyist Incentives",
  description: "Maximum bond investment for lobbyist incentives",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/strategy/roadmap#lobbyist-incentives",
  confidence: "high",
};

export const MINUTES_PER_HOUR: Parameter = {
  value: 60.0,
};

export const MONTHS_PER_YEAR: Parameter = {
  value: 12.0,
};

export const NATO_POLITICAL_REFORM_INVESTMENT: Parameter = {
  value: 65000000000.0,
  unit: "USD",
  displayName: "NATO Political Reform Investment",
  description: "Estimated advocacy investment to achieve policy reform across all NATO member states (US $25B + EU $25B + other NATO $15B). Represents cost of democratic parity with defense industry interests.",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/cost-of-change-analysis#global-estimates",
  confidence: "low",
  formula: "US advocacy + EU advocacy + other NATO advocacy",
};

export const NPV_DISCOUNT_RATE_STANDARD: Parameter = {
  value: 0.03,
  unit: "rate",
  displayName: "Standard Discount Rate for NPV Analysis",
  description: "Standard discount rate for NPV analysis (3% annual, social discount rate)",
  sourceType: "definition",
  confidence: "high",
};

export const NPV_TIME_HORIZON_YEARS: Parameter = {
  value: 10.0,
  unit: "years",
  displayName: "Standard Time Horizon for NPV Analysis",
  description: "Standard time horizon for NPV analysis",
  sourceType: "definition",
  confidence: "high",
};

export const PEACE_DIVIDEND_DIRECT_FISCAL_SAVINGS: Parameter = {
  value: 27200000000.0,
  unit: "USD/year",
  displayName: "Direct Fiscal Savings from 1% Military Spending Reduction",
  description: "Direct fiscal savings from 1% military spending reduction (high confidence)",
  sourceType: "definition",
  sourceRef: "sipri2024",
  confidence: "high",
  formula: "TREATY_ANNUAL_FUNDING",
};

export const PHARMA_PHASE_2_3_COST_BARRIER: Parameter = {
  value: 1560000000.0,
  unit: "USD",
  displayName: "Pharma Phase 2/3 Cost Barrier Per Drug",
  description: "Average Phase 2/3 efficacy testing cost per drug that pharma must fund (~60% of $2.6B total)",
  sourceType: "definition",
  sourceRef: "drug-development-cost",
  confidence: "high",
  stdError: 200000000.0,
};

export const PRE_1962_VALIDATION_YEARS: Parameter = {
  value: 77.0,
  unit: "years",
  displayName: "Pre-1962 Validation Years",
  description: "Years of empirical validation for physician-led pragmatic trials (1883-1960)",
  sourceType: "definition",
  sourceRef: "life-expectancy-increase-pre-1962",
  confidence: "high",
  formula: "1960 - 1883",
};

export const QALYS_PER_COVID_DEATH_AVERTED: Parameter = {
  value: 5.0,
  unit: "QALYs/death",
  displayName: "QALYs per COVID Death Averted",
  description: "Average QALYs gained per COVID death averted. Conservative estimate reflecting older age distribution of COVID mortality. See confidence_interval for range.",
  sourceType: "definition",
  confidence: "low",
  confidenceInterval: [3.0, 10.0],
};

export const SAFE_COMPOUNDS_COUNT: Parameter = {
  value: 9500.0,
  unit: "compounds",
  displayName: "Safe Compounds Available for Testing",
  description: "Total safe compounds available for repurposing (FDA-approved + GRAS substances, midpoint of 7,000-12,000 range)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  confidenceInterval: [7000.0, 12000.0],
};

export const SECONDS_PER_MINUTE: Parameter = {
  value: 60.0,
};

export const SECONDS_PER_YEAR: Parameter = {
  value: 31536000.0,
};

export const TESTED_RELATIONSHIPS_ESTIMATE: Parameter = {
  value: 32500.0,
  unit: "relationships",
  displayName: "Tested Drug-Disease Relationships",
  description: "Estimated drug-disease relationships actually tested (approved uses + repurposed + failed trials, midpoint of 15,000-50,000 range)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  confidenceInterval: [15000.0, 50000.0],
};

export const TOTAL_BOOK_WORDS: Parameter = {
  value: 171121.0,
  unit: "words",
  displayName: "Total Words in the Book",
  description: "Total words in the book",
  sourceType: "definition",
  sourceRef: "book-word-count",
  confidence: "high",
};

export const TREATY_ANNUAL_FUNDING: Parameter = {
  value: 27200000000.0,
  unit: "USD/year",
  displayName: "Annual Funding from 1% of Global Military Spending Redirected to DIH",
  description: "Annual funding from 1% of global military spending redirected to DIH",
  sourceType: "definition",
  confidence: "high",
  formula: "MILITARY_SPENDING × 1%",
  latex: "\\begin{gathered}\nFunding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const TREATY_CAMPAIGN_BUDGET_LOBBYING: Parameter = {
  value: 650000000.0,
  unit: "USD",
  displayName: "Political Lobbying Campaign: Direct Lobbying, Super Pacs, Opposition Research, Staff, Legal/Compliance",
  description: "Political lobbying campaign: direct lobbying (US/EU/G20), Super PACs, opposition research, staff, legal/compliance. Budget exceeds combined pharma ($300M/year) and military-industrial complex ($150M/year) lobbying to ensure competitive positioning. Referendum relies on grassroots mobilization and earned media, while lobbying requires matching or exceeding opposition spending for political viability.",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/fundraising-strategy#campaign-budget-breakdown",
  confidence: "low",
  confidenceInterval: [325000000.0, 1300000000.0],
};

export const TREATY_CAMPAIGN_BUDGET_RESERVE: Parameter = {
  value: 100000000.0,
  unit: "USD",
  displayName: "Reserve Fund / Contingency Buffer",
  description: "Reserve fund / contingency buffer (10% of total campaign cost). Using industry standard 10% for complex campaigns with potential for unforeseen legal challenges, opposition response, or regulatory delays. Conservative lower bound of $20M (2%) reflects transparent budget allocation and predictable referendum/lobbying costs.",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/fundraising-strategy#campaign-budget-breakdown",
  confidence: "medium",
  confidenceInterval: [20000000.0, 150000000.0],
};

export const TREATY_CAMPAIGN_BUDGET_SUPER_PACS: Parameter = {
  value: 800000000.0,
  unit: "USD",
  displayName: "Campaign Budget for Super Pacs and Political Lobbying",
  description: "Campaign budget for Super PACs and political lobbying",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/strategy/roadmap#campaign-budget",
  confidence: "high",
};

export const TREATY_CAMPAIGN_DURATION_YEARS: Parameter = {
  value: 4.0,
  unit: "years",
  displayName: "Treaty Campaign Duration",
  description: "Treaty campaign duration (3-5 year range, using midpoint)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/strategy/roadmap",
  confidence: "high",
  confidenceInterval: [3.0, 5.0],
};

export const TREATY_CAMPAIGN_VIRAL_REFERENDUM_BASE_CASE: Parameter = {
  value: 250000000.0,
  unit: "USD",
  displayName: "Viral Referendum Budget",
  description: "Viral referendum budget for 280M verified votes (base: $250M realistic with $0.50/vote avg, range: $150M optimistic $0.20/vote to $410M worst-case $1.05/vote). Components: platform ($35M), verification infrastructure (280M × friction × $0.18-0.20), tiered referral payments (varies by virality and marginal cost curve per diffusion theory), marketing seed ($5-15M). Based on PayPal referral economics ($18-36 inflation-adjusted) and biometric verification pricing ($0.15-0.25 at 300M+ scale).",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/campaign-budget",
  confidence: "medium",
  formula: "PLATFORM + VERIFICATION + PAYMENTS (tiered by adopter segment) + MARKETING",
  confidenceInterval: [150000000.0, 410000000.0],
};

export const TREATY_REDIRECTED_SPENDING_INFINITE_ROI: Parameter = {
  value: 0.0,
  unit: "ratio",
  displayName: "Infinite ROI from Redirected Spending",
  description: "ROI when redirecting existing spending (no new costs = infinite return)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/economics/economics#infinite-roi",
  confidence: "high",
  formula: "COMBINED_DIVIDENDS ÷ 0 = ∞",
  latex: "\\begin{gathered}\n\\text{ROI} \\\\\n= \\frac{\\text{Annual Benefits}}{\\text{New Spending}} \\\\\n= \\frac{\\$172B}{0} \\\\\n= \\infty\n\\end{gathered}",
};

export const TREATY_REDUCTION_PCT: Parameter = {
  value: 0.01,
  unit: "rate",
  displayName: "1% Reduction in Military Spending/War Costs from Treaty",
  description: "1% reduction in military spending/war costs from treaty",
  sourceType: "definition",
  confidence: "high",
};

export const TREATY_VS_DIRECT_FUNDING_LEVERAGE: Parameter = {
  value: 475.2766905010616,
  unit: "ratio",
  displayName: "Treaty Campaign Leverage vs Direct Funding",
  description: "How many times more cost-effective the treaty campaign is vs direct funding. Treaty achieves 542× leverage: $1B campaign unlocks $27.2B/year government funding for 46.5 years (queue clearance, NPV: $541.9B), avoiding need for philanthropists/NIH to directly commit this amount. Both approaches achieve same 200B DALY timeline shift benefit by clearing disease queue 9.5× faster. Treaty spreads cost across governments while building sustainable public funding infrastructure.",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/dfda-impact-paper",
  confidence: "high",
  formula: "DFDA_DIRECT_FUNDING_COST_PER_DALY ÷ TREATY_COST_PER_DALY",
  latex: "\\begin{gathered}\nLeverage_{treaty} \\\\\n= \\frac{Cost_{direct,DALY}}{Cost_{treaty,DALY}} \\\\\n= \\frac{\\$0.841}{\\$0.00177} \\\\\n= 475 \\\\[0.5em]\n\\text{where } Cost_{direct,DALY} = \\frac{NPV_{direct}}{DALYs_{max}} = \\frac{\\$475B}{565B} = \\$0.841 \\\\[0.5em]\n\\text{where } NPV_{direct} \\\\\n= \\frac{T_{queue,dFDA}}{Treasury_{RD,ann} \\times r_{discount}} \\\\\n= \\frac{36}{\\$21.8B \\times 3\\%} \\\\\n= \\$475B \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } T_{queue,dFDA} = \\frac{T_{queue,SQ}}{k_{capacity}} = \\frac{443}{12.3} = 36 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } DALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Cost_{treaty,DALY} = \\frac{Cost_{campaign}}{DALYs_{max}} = \\frac{\\$1B}{565B} = \\$0.00177 \\\\[0.5em]\n\\text{where } Cost_{campaign} \\\\\n= Budget_{viral,base} + Budget_{lobby,treaty} \\\\\n+ Budget_{reserve} \\\\\n= \\$250M + \\$650M + \\$100M \\\\\n= \\$1B \\\\[0.5em]\n\\text{where } DALYs_{max} \\\\\n= DALYs_{global,ann} \\times Pct_{avoid,DALY} \\times T_{accel,max} \\\\\n= 2.88B \\times 92.6\\% \\times 212 \\\\\n= 565B \\\\[0.5em]\n\\text{where } T_{accel,max} = T_{accel} + T_{lag} = 204 + 8.2 = 212 \\\\[0.5em]\n\\text{where } T_{accel} \\\\\n= T_{first,SQ} \\times \\left(1 - \\frac{1}{k_{capacity}}\\right) \\\\\n= 222 \\times \\left(1 - \\frac{1}{12.3}\\right) \\\\\n= 204 \\\\[0.5em]\n\\text{where } T_{first,SQ} = T_{queue,SQ} \\times 0.5 = 443 \\times 0.5 = 222 \\\\[0.5em]\n\\text{where } T_{queue,SQ} = \\frac{N_{untreated}}{Treatments_{new,ann}} = \\frac{6{,}650}{15} = 443 \\\\[0.5em]\n\\text{where } N_{untreated} = N_{rare} \\times 0.95 = 7{,}000 \\times 0.95 = 6{,}650 \\\\[0.5em]\n\\text{where } k_{capacity} = \\frac{N_{fundable,ann}}{Slots_{curr}} = \\frac{23.4M}{1.9M} = 12.3 \\\\[0.5em]\n\\text{where } N_{fundable,ann} \\\\\n= \\frac{Subsidies_{trial,ann}}{Cost_{pragmatic,pt}} \\\\\n= \\frac{\\$21.7B}{\\$929} \\\\\n= 23.4M \\\\[0.5em]\n\\text{where } Subsidies_{trial,ann} \\\\\n= Treasury_{RD,ann} - OPEX_{dFDA} \\\\\n= \\$21.8B - \\$40M \\\\\n= \\$21.7B \\\\[0.5em]\n\\text{where } OPEX_{dFDA} \\\\\n= Cost_{platform} + Cost_{staff} + Cost_{infra} \\\\\n+ Cost_{regulatory} + Cost_{community} \\\\\n= \\$15M + \\$10M + \\$8M + \\$5M + \\$2M \\\\\n= \\$40M \\\\[0.5em]\n\\text{where } Treasury_{RD,ann} \\\\\n= Funding_{treaty} - Payout_{bond,ann} - Funding_{political,ann} \\\\\n= \\$27.2B - \\$2.72B - \\$2.72B \\\\\n= \\$21.8B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Funding_{political,ann} \\\\\n= Funding_{treaty} \\times Pct_{political} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const TRIAL_RELEVANT_DISEASES_COUNT: Parameter = {
  value: 1000.0,
  unit: "diseases",
  displayName: "Trial-Relevant Diseases",
  description: "Consolidated count of trial-relevant diseases worth targeting (after grouping ICD-10 codes)",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  confidenceInterval: [800.0, 1200.0],
};

export const US_CONGRESS_MEMBER_COUNT: Parameter = {
  value: 535.0,
  unit: "members",
  displayName: "US Congress Members",
  description: "Total members of US Congress (100 senators + 435 representatives)",
  sourceType: "definition",
  confidence: "high",
};

export const US_DYSFUNCTION_PREMIUM_VS_SWITZERLAND: Parameter = {
  value: 3.0,
  unit: "percent",
  displayName: "US Dysfunction Premium vs Switzerland",
  description: "US 'dysfunction premium' vs Switzerland: US spends 3% more of GDP yet achieves 6.5 fewer years of life expectancy. This premium represents pure waste from governance inefficiency. Calculated as: 38% (US) - 35% (CH).",
  sourceType: "definition",
  sourceRef: "oecd-govt-spending",
  confidence: "high",
  formula: "US_GOVT_SPENDING_PCT_GDP - SWITZERLAND_GOVT_SPENDING_PCT_GDP",
};

export const US_POLITICAL_REFORM_INVESTMENT_TOTAL: Parameter = {
  value: 25000000000.0,
  unit: "USD",
  displayName: "US Political Reform Investment (Total)",
  description: "Total upper-bound investment for US political reform: Congress advocacy costs ($5.35B) + lobbying parity ($5B/year x 4 years) + campaign matching. Represents cost to achieve democratic parity with incumbent interests.",
  sourceType: "definition",
  sourceRef: "https://impact.warondisease.org/knowledge/appendix/cost-of-change-analysis#us-political-reform-scenarios",
  confidence: "low",
  formula: "Congress advocacy + lobbying parity + campaign matching",
};

export const US_VS_SINGAPORE_SPENDING_GAP: Parameter = {
  value: 23.0,
  unit: "percent",
  displayName: "US-Singapore Spending Gap",
  description: "Government spending gap: US spends 23 percentage points MORE of GDP than Singapore yet achieves 6.6 fewer years of life expectancy.",
  sourceType: "definition",
  sourceRef: "oecd-govt-spending",
  confidence: "high",
  formula: "US_SPENDING - SINGAPORE_SPENDING = 38% - 15%",
};

export const US_VS_SWITZERLAND_LIFE_EXPECTANCY_GAP: Parameter = {
  value: 6.5,
  unit: "years",
  displayName: "Switzerland-US Life Expectancy Gap",
  description: "Life expectancy gap: Switzerland vs US. Switzerland achieves 6.5 extra years of life while spending 3% LESS of GDP on government.",
  sourceType: "definition",
  sourceRef: "who-life-expectancy",
  confidence: "high",
  formula: "SWITZERLAND_LE - US_LE = 84.0 - 77.5",
};

export const US_VS_SWITZERLAND_SPENDING_GAP: Parameter = {
  value: 3.0,
  unit: "percent",
  displayName: "US-Switzerland Spending Gap",
  description: "Government spending gap: US spends 3 percentage points MORE of GDP than Switzerland yet achieves worse outcomes.",
  sourceType: "definition",
  sourceRef: "oecd-govt-spending",
  confidence: "high",
  formula: "US_SPENDING - SWITZERLAND_SPENDING = 38% - 35%",
};

export const VICTORY_BOND_ANNUAL_PAYOUT: Parameter = {
  value: 2720000000.0,
  unit: "USD/year",
  displayName: "Annual VICTORY Incentive Alignment Bond Payout",
  description: "Annual VICTORY Incentive Alignment Bond payout (treaty funding × bond percentage)",
  sourceType: "definition",
  confidence: "high",
  formula: "TREATY_FUNDING × BOND_PCT",
  latex: "\\begin{gathered}\nPayout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B\n\\end{gathered}",
};

export const VICTORY_BOND_ANNUAL_RETURN_PCT: Parameter = {
  value: 2.72,
  unit: "rate",
  displayName: "Annual Return Percentage for VICTORY Incentive Alignment Bondholders",
  description: "Annual return percentage for VICTORY Incentive Alignment Bondholders",
  sourceType: "definition",
  confidence: "high",
  formula: "PAYOUT ÷ CAMPAIGN_COST",
  latex: "\\begin{gathered}\nr_{bond} = \\frac{Payout_{bond,ann}}{Cost_{campaign}} = \\frac{\\$2.72B}{\\$1B} = 272\\% \\\\[0.5em]\n\\text{where } Payout_{bond,ann} \\\\\n= Funding_{treaty} \\times Pct_{bond} \\\\\n= \\$27.2B \\times 10\\% \\\\\n= \\$2.72B \\\\[0.5em]\n\\text{where } Funding_{treaty} \\\\\n= Spending_{mil} \\times Reduce_{treaty} \\\\\n= \\$2.72T \\times 1\\% \\\\\n= \\$27.2B \\\\[0.5em]\n\\text{where } Cost_{campaign} \\\\\n= Budget_{viral,base} + Budget_{lobby,treaty} \\\\\n+ Budget_{reserve} \\\\\n= \\$250M + \\$650M + \\$100M \\\\\n= \\$1B\n\\end{gathered}",
};

export const VICTORY_BOND_FUNDING_PCT: Parameter = {
  value: 0.1,
  unit: "rate",
  displayName: "Percentage of Captured Dividend Funding VICTORY Incentive Alignment Bonds",
  description: "Percentage of captured dividend funding VICTORY Incentive Alignment Bonds (10%)",
  sourceType: "definition",
  confidence: "high",
};

// ============================================================================
// All Parameters (for iteration)
// ============================================================================

export const parameters = {
  ADAPTABLE_TRIAL_COST_PER_PATIENT,
  ADAPTABLE_TRIAL_TOTAL_COST,
  ANTIDEPRESSANT_TRIAL_EXCLUSION_RATE,
  AVERAGE_MARKET_RETURN_PCT,
  AVERAGE_US_HOURLY_WAGE,
  BAD_POLICY_COST_US_AGRICULTURAL_SUBSIDIES,
  BAD_POLICY_COST_US_DEFENSE_ABOVE_DETERRENCE,
  BAD_POLICY_COST_US_DRUG_WAR,
  BAD_POLICY_COST_US_FAILED_WARS,
  BAD_POLICY_COST_US_FOSSIL_FUEL_EXPLICIT,
  BAD_POLICY_COST_US_FOSSIL_FUEL_EXTERNALITIES,
  BAD_POLICY_COST_US_HEALTHCARE_INEFFICIENCY,
  BAD_POLICY_COST_US_HOUSING_ZONING,
  BAD_POLICY_COST_US_INCARCERATION_EXCESS,
  BAD_POLICY_COST_US_INFRASTRUCTURE_DISEASE,
  BAD_POLICY_COST_US_MIGRATION_RESTRICTIONS,
  BAD_POLICY_COST_US_OCCUPATIONAL_LICENSING,
  BAD_POLICY_COST_US_TARIFFS,
  BAD_POLICY_COST_US_TAX_COMPLIANCE,
  BASELINE_LIVES_SAVED_ANNUAL,
  BED_NETS_COST_PER_DALY,
  BOOK_READING_SPEED_WPM,
  CAREGIVER_ANNUAL_VALUE_TOTAL,
  CAREGIVER_COUNT_US,
  CAREGIVER_HOURS_PER_MONTH,
  CAREGIVER_VALUE_PER_HOUR_SIMPLE,
  CHILDHOOD_VACCINATION_ANNUAL_BENEFIT,
  CHILDHOOD_VACCINATION_ROI,
  CHRONIC_DISEASE_DISABILITY_WEIGHT,
  CPI_MULTIPLIER_1980_TO_2024,
  CRONY_TAX_PCT,
  CURRENT_ACTIVE_TRIALS,
  CURRENT_CLINICAL_TRIAL_PARTICIPATION_RATE,
  CURRENT_DISEASE_PATIENTS_GLOBAL,
  CURRENT_DRUG_APPROVALS_PER_YEAR,
  CURRENT_TRIALS_PER_YEAR,
  CURRENT_TRIAL_ABANDONMENT_RATE,
  CURRENT_TRIAL_SLOTS_AVAILABLE,
  DEFENSE_LOBBYING_ANNUAL,
  DEWORMING_COST_PER_DALY,
  DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT,
  DRUG_DEVELOPMENT_COST_1980S,
  DRUG_REPURPOSING_SUCCESS_RATE,
  ECONOMIC_MULTIPLIER_EDUCATION_INVESTMENT,
  ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT,
  ECONOMIC_MULTIPLIER_INFRASTRUCTURE_INVESTMENT,
  ECONOMIC_MULTIPLIER_MILITARY_SPENDING,
  EFFICACY_LAG_YEARS,
  FDA_APPROVED_PRODUCTS_COUNT,
  FDA_APPROVED_UNIQUE_ACTIVE_INGREDIENTS,
  FDA_GRAS_SUBSTANCES_COUNT,
  FDA_PHASE_1_TO_APPROVAL_YEARS,
  GIVEWELL_COST_PER_LIFE_AVG,
  GIVEWELL_COST_PER_LIFE_MAX,
  GIVEWELL_COST_PER_LIFE_MIN,
  GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT,
  GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE,
  GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS,
  GLOBAL_ANNUAL_DALY_BURDEN,
  GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES,
  GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT,
  GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT,
  GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT,
  GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT,
  GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT,
  GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT,
  GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT,
  GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH,
  GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING,
  GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT,
  GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT,
  GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS,
  GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT,
  GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT,
  GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT,
  GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT,
  GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS,
  GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL,
  GLOBAL_DISEASE_DEATHS_DAILY,
  GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL,
  GLOBAL_DISEASE_HUMAN_LIFE_VALUE_LOSS_ANNUAL,
  GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL,
  GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL,
  GLOBAL_HOUSEHOLD_WEALTH_USD,
  GLOBAL_LIFE_EXPECTANCY_2024,
  GLOBAL_MED_RESEARCH_SPENDING,
  GLOBAL_MILITARY_SPENDING_ANNUAL_2024,
  GLOBAL_NONPROFIT_CLINICAL_TRIALS_SPENDING_ANNUAL,
  GLOBAL_PHARMA_RD_SPENDING_ANNUAL,
  GLOBAL_POPULATION_2024,
  GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT,
  GLOBAL_SYMPTOMATIC_DISEASE_TREATMENT_ANNUAL,
  GLOBAL_YLD_PROPORTION_OF_DALYS,
  HUMAN_GENOME_PROJECT_TOTAL_ECONOMIC_IMPACT,
  HUMAN_INTERACTOME_TARGETED_PCT,
  ICD_10_TOTAL_CODES,
  LIFE_EXTENSION_YEARS,
  LOBBYIST_SALARY_MAX,
  LOBBYIST_SALARY_MIN_K,
  MEASLES_VACCINATION_ROI,
  MENTAL_HEALTH_PRODUCTIVITY_LOSS_PER_CAPITA,
  NATO_DEFENSE_SPENDING_ANNUAL,
  NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR,
  NIH_ANNUAL_BUDGET,
  NIH_CLINICAL_TRIALS_SPENDING_PCT,
  NIH_STANDARD_RESEARCH_COST_PER_QALY,
  OXFORD_RECOVERY_TRIAL_DURATION_MONTHS,
  PATIENT_WILLINGNESS_TRIAL_PARTICIPATION_PCT,
  PHARMA_DRUG_DEVELOPMENT_COST_CURRENT,
  PHARMA_DRUG_REVENUE_AVERAGE_CURRENT,
  PHARMA_ROI_CURRENT_SYSTEM_PCT,
  PHARMA_SUCCESS_RATE_CURRENT_PCT,
  PHASE_1_PASSED_COMPOUNDS_GLOBAL,
  PHASE_1_SAFETY_DURATION_YEARS,
  PHASE_2_3_CLINICAL_TRIAL_COST_PCT,
  PHASE_3_TRIAL_COST_MIN,
  PMC_PRAGMATIC_TRIAL_MEDIAN_COST_PER_PATIENT,
  POLIO_VACCINATION_ROI,
  POLITICAL_DYSFUNCTION_TAX_COORDINATION_PCT,
  POLITICAL_DYSFUNCTION_TAX_INFO_PCT,
  POLITICAL_DYSFUNCTION_TAX_TIME_PCT,
  POLITICAL_SUCCESS_PROBABILITY,
  POLITICIAN_POST_OFFICE_CAREER_VALUE,
  POST_1962_DRUG_APPROVAL_REDUCTION_PCT,
  POST_WW2_MILITARY_CUT_PCT,
  PRE_1962_DRUG_DEVELOPMENT_COST_1980_USD,
  PRE_1962_DRUG_DEVELOPMENT_COST_2024_USD,
  PRE_1962_PHYSICIAN_COUNT,
  RARE_DISEASES_COUNT_GLOBAL,
  RECOVERY_TRIAL_COST_PER_PATIENT,
  RECOVERY_TRIAL_GLOBAL_LIVES_SAVED,
  RECOVERY_TRIAL_TOTAL_COST,
  REGULATORY_DELAY_MEAN_AGE_OF_DEATH,
  REGULATORY_DELAY_SUFFERING_PERIOD_YEARS,
  SINGAPORE_GDP_PER_CAPITA_PPP,
  SINGAPORE_GOVT_SPENDING_PCT_GDP,
  SINGAPORE_LIFE_EXPECTANCY,
  SMALLPOX_ERADICATION_ROI,
  SMALLPOX_ERADICATION_TOTAL_BENEFIT,
  SMOKING_CESSATION_ANNUAL_BENEFIT,
  STANDARD_ECONOMIC_QALY_VALUE_USD,
  STANDARD_QALYS_PER_LIFE_SAVED,
  SUGAR_SUBSIDY_COST_PER_PERSON_ANNUAL,
  SWITZERLAND_DEFENSE_SPENDING_PCT,
  SWITZERLAND_GDP_PER_CAPITA_K,
  SWITZERLAND_GOVT_SPENDING_PCT_GDP,
  SWITZERLAND_LIFE_EXPECTANCY,
  SWITZERLAND_MEDIAN_INCOME_PPP,
  TERRORISM_DEATHS_911,
  THALIDOMIDE_CASES_WORLDWIDE,
  THALIDOMIDE_DISABILITY_WEIGHT,
  THALIDOMIDE_MORTALITY_RATE,
  THALIDOMIDE_SURVIVOR_LIFESPAN,
  THALIDOMIDE_US_POPULATION_SHARE_1960,
  TRADITIONAL_PHASE3_COST_PER_PATIENT,
  TREATMENT_ACCELERATION_YEARS_CURRENT,
  TYPICAL_CEO_HOURLY_RATE,
  US_ALZHEIMERS_ANNUAL_COST,
  US_CANCER_ANNUAL_COST,
  US_CHRONIC_DISEASE_SPENDING_ANNUAL,
  US_DIABETES_ANNUAL_COST,
  US_GDP_2024,
  US_GOVT_SPENDING_PCT_GDP,
  US_HEART_DISEASE_ANNUAL_COST,
  US_LIFE_EXPECTANCY_1880,
  US_LIFE_EXPECTANCY_1962,
  US_LIFE_EXPECTANCY_2019,
  US_LIFE_EXPECTANCY_2023,
  US_MEDIAN_HOUSEHOLD_INCOME_2023,
  US_MENTAL_HEALTH_COST_ANNUAL,
  US_MILITARY_SPENDING_PCT_GDP,
  US_POPULATION_2024,
  US_SENATORS_FOR_TREATY,
  US_TOTAL_FEDERAL_CAMPAIGN_SPENDING_2024,
  US_TOTAL_LOBBYING_ANNUAL,
  VALLEY_OF_DEATH_ATTRITION_PCT,
  VALUE_OF_STATISTICAL_LIFE,
  VITAMIN_A_COST_PER_DALY,
  WATER_FLUORIDATION_ANNUAL_BENEFIT,
  WATER_FLUORIDATION_ROI,
  WHO_QALY_THRESHOLD_COST_EFFECTIVE,
  WORKFORCE_WITH_PRODUCTIVITY_LOSS,
  ADDITIONAL_DRUGS_FROM_COST_ELIMINATION,
  BAD_POLICY_COST_TOTAL_US,
  BAD_POLICY_COST_TOTAL_US_PCT_GDP,
  BAD_POLICY_COST_US_TIER1_TOTAL,
  BAD_POLICY_COST_US_TIER2_TOTAL,
  CELL_THERAPY_DISEASE_COMBINATIONS,
  CLINICAL_TRIAL_COST_PER_APPROVED_DRUG,
  CLINICAL_TRIAL_COST_PER_PARTICIPANT_ANNUAL,
  COMBINATION_THERAPY_DISEASE_SPACE,
  COMBINATION_THERAPY_PAIRS,
  COMBINED_PEACE_HEALTH_DIVIDENDS_ANNUAL_FOR_ROI_CALC,
  CURRENT_COMBINATION_EXPLORATION_YEARS,
  CURRENT_KNOWN_SAFE_EXPLORATION_YEARS,
  CURRENT_TOTAL_EXPLORATION_YEARS,
  DFDA_ANNUAL_OPEX,
  DFDA_BENEFIT_RD_ONLY_ANNUAL,
  DFDA_COMBINED_TREATMENT_SPEEDUP_MULTIPLIER,
  DFDA_DIRECT_FUNDING_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG,
  DFDA_DIRECT_FUNDING_VS_BED_NETS_MULTIPLIER,
  DFDA_EFFICACY_LAG_ELIMINATION_DALYS,
  DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED,
  DFDA_EFFICACY_LAG_ELIMINATION_ECONOMIC_VALUE,
  DFDA_EFFICACY_LAG_ELIMINATION_YLD,
  DFDA_EFFICACY_LAG_ELIMINATION_YLL,
  DFDA_FIRST_TREATMENTS_PER_YEAR,
  DFDA_KNOWN_SAFE_EXPLORATION_YEARS,
  DFDA_NET_SAVINGS_RD_ONLY_ANNUAL,
  DFDA_NPV_ANNUAL_OPEX_TOTAL,
  DFDA_NPV_BENEFIT_RD_ONLY,
  DFDA_NPV_NET_BENEFIT_RD_ONLY,
  DFDA_NPV_PV_ANNUAL_OPEX,
  DFDA_NPV_TOTAL_COST,
  DFDA_NPV_UPFRONT_COST_TOTAL,
  DFDA_QUEUE_CLEARANCE_YEARS,
  DFDA_RD_SAVINGS_DAILY,
  DFDA_ROI_RD_ONLY,
  DFDA_STORAGE_COST_TOTAL_PER_PATIENT_ANNUAL,
  DFDA_STORAGE_COST_TOTAL_PER_PATIENT_MONTHLY,
  DFDA_TOTAL_EXPLORATION_YEARS,
  DFDA_TRIALS_PER_YEAR_CAPACITY,
  DFDA_TRIAL_CAPACITY_DALYS_AVERTED,
  DFDA_TRIAL_CAPACITY_ECONOMIC_VALUE,
  DFDA_TRIAL_CAPACITY_LIVES_SAVED,
  DFDA_TRIAL_CAPACITY_MULTIPLIER,
  DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS,
  DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE,
  DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED,
  DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS,
  DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS,
  DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS,
  DFDA_TRIAL_COST_REDUCTION_FACTOR,
  DFDA_TRIAL_COST_REDUCTION_PCT,
  DFDA_VALLEY_OF_DEATH_RESCUE_MULTIPLIER,
  DIH_PATIENTS_FUNDABLE_ANNUALLY,
  DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL,
  DISEASES_WITHOUT_EFFECTIVE_TREATMENT,
  DIVIDEND_COVERAGE_FACTOR,
  DRUG_COST_INCREASE_1980S_TO_CURRENT_MULTIPLIER,
  DRUG_COST_INCREASE_PRE1962_TO_CURRENT_MULTIPLIER,
  DRUG_DISEASE_COMBINATIONS_POSSIBLE,
  EMERGING_MODALITY_COMBINATIONS,
  EPIGENETIC_DISEASE_COMBINATIONS,
  EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL,
  EXISTING_DRUGS_EFFICACY_LAG_ECONOMIC_LOSS,
  EXPLORATION_RATIO,
  FDA_TO_OXFORD_RECOVERY_TRIAL_TIME_MULTIPLIER,
  GENE_THERAPY_DISEASE_COMBINATIONS,
  GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL,
  GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST,
  GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT,
  GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE,
  GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS,
  GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT,
  GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT,
  GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT,
  GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL,
  GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL,
  GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL,
  GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL,
  GLOBAL_INDUSTRY_CLINICAL_TRIALS_SPENDING_ANNUAL,
  GLOBAL_MILITARY_SPENDING_PER_CAPITA_ANNUAL,
  GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL,
  IAB_MECHANISM_BENEFIT_COST_RATIO,
  INDUSTRY_VS_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO,
  LIFE_EXPECTANCY_GAIN_1883_1962_YEARS_PER_DECADE,
  LIFE_EXPECTANCY_GAIN_1962_2019_YEARS_PER_DECADE,
  MEDICAL_RESEARCH_PCT_OF_DISEASE_BURDEN,
  MILITARY_TO_CLINICAL_TRIALS_SPENDING_RATIO,
  MILITARY_TO_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO,
  MILITARY_VS_MEDICAL_RESEARCH_RATIO,
  MISALLOCATION_FACTOR_DEATH_VS_SAVING,
  MRNA_THERAPEUTIC_COMBINATIONS,
  PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT,
  PEACE_DIVIDEND_CONFLICT_REDUCTION,
  PEACE_DIVIDEND_DIRECT_COSTS,
  PEACE_DIVIDEND_ENVIRONMENTAL,
  PEACE_DIVIDEND_HUMAN_CASUALTIES,
  PEACE_DIVIDEND_INDIRECT_COSTS,
  PEACE_DIVIDEND_INFRASTRUCTURE,
  PEACE_DIVIDEND_LOST_ECONOMIC_GROWTH,
  PEACE_DIVIDEND_LOST_HUMAN_CAPITAL,
  PEACE_DIVIDEND_PTSD,
  PEACE_DIVIDEND_REFUGEE_SUPPORT,
  PEACE_DIVIDEND_TRADE_DISRUPTION,
  PEACE_DIVIDEND_VETERAN_HEALTHCARE,
  PERSONAL_LIFETIME_WEALTH,
  PER_CAPITA_CHRONIC_DISEASE_COST,
  PER_CAPITA_MENTAL_HEALTH_COST,
  POLITICAL_DYSFUNCTION_TAX_TOTAL_PCT,
  PRAGMATIC_TRIAL_COST_PER_QALY,
  PRAGMATIC_VS_NIH_EFFICIENCY_MULTIPLIER,
  RECOVERY_TRIAL_COST_REDUCTION_FACTOR,
  RECOVERY_TRIAL_TOTAL_QALYS_GENERATED,
  STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT,
  STATUS_QUO_QUEUE_CLEARANCE_YEARS,
  THALIDOMIDE_DALYS_PER_EVENT,
  THALIDOMIDE_DEATHS_PER_EVENT,
  THALIDOMIDE_SURVIVORS_PER_EVENT,
  THALIDOMIDE_US_CASES_PREVENTED,
  THALIDOMIDE_YLD_PER_EVENT,
  THALIDOMIDE_YLL_PER_EVENT,
  TOTAL_RESEARCH_FUNDING_WITH_TREATY,
  TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS,
  TREATY_BENEFIT_MULTIPLIER_VS_VACCINES,
  TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED,
  TREATY_CAMPAIGN_TOTAL_COST,
  TREATY_CAMPAIGN_VOTING_BLOC_TARGET,
  TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG,
  TREATY_EXPECTED_COST_PER_DALY,
  TREATY_EXPECTED_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG,
  TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER,
  TREATY_LIVES_SAVED_ANNUAL_GLOBAL,
  TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS,
  TREATY_QALYS_GAINED_ANNUAL_GLOBAL,
  TREATY_RECURRING_BENEFITS_ANNUAL,
  TREATY_ROI_EXISTING_DRUGS_ONLY,
  TREATY_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG,
  TREATY_TOTAL_ANNUAL_COSTS,
  TREATY_VS_BED_NETS_MULTIPLIER,
  TRIAL_CAPACITY_CUMULATIVE_YEARS_20YR,
  TYPE_II_ERROR_COST_RATIO,
  TYPE_I_ERROR_BENEFIT_DALYS,
  UNEXPLORED_RATIO,
  US_CONGRESS_FULL_ADVOCACY_COST,
  US_MAJOR_DISEASES_TOTAL_ANNUAL_COST,
  US_SENATE_TREATY_ADVOCACY_COST,
  WILLING_TRIAL_PARTICIPANTS_GLOBAL,
  ADAPTABLE_TRIAL_PATIENTS,
  APPROVED_DRUG_DISEASE_PAIRINGS,
  BAD_POLICY_US_OVERLAP_DISCOUNT,
  CAMPAIGN_CELEBRITY_ENDORSEMENT,
  CAMPAIGN_COMMUNITY_ORGANIZING,
  CAMPAIGN_CONTINGENCY,
  CAMPAIGN_DEFENSE_CONVERSION,
  CAMPAIGN_DEFENSE_LOBBYIST_BUDGET,
  CAMPAIGN_HEALTHCARE_ALIGNMENT,
  CAMPAIGN_INFRASTRUCTURE,
  CAMPAIGN_LEGAL_AI_BUDGET,
  CAMPAIGN_LEGAL_DEFENSE,
  CAMPAIGN_LEGAL_WORK,
  CAMPAIGN_LOBBYING_EU,
  CAMPAIGN_LOBBYING_G20_MILLIONS,
  CAMPAIGN_LOBBYING_US,
  CAMPAIGN_MEDIA_BUDGET_MAX,
  CAMPAIGN_MEDIA_BUDGET_MIN,
  CAMPAIGN_OPPOSITION_RESEARCH,
  CAMPAIGN_PHASE1_BUDGET,
  CAMPAIGN_PHASE2_BUDGET,
  CAMPAIGN_PILOT_PROGRAMS,
  CAMPAIGN_PLATFORM_DEVELOPMENT,
  CAMPAIGN_REGULATORY_NAVIGATION,
  CAMPAIGN_SCALING_PREP,
  CAMPAIGN_STAFF_BUDGET,
  CAMPAIGN_SUPER_PAC_BUDGET,
  CAMPAIGN_TECH_PARTNERSHIPS,
  CAMPAIGN_TREATY_IMPLEMENTATION,
  CAMPAIGN_VIRAL_CONTENT_BUDGET,
  CAREGIVER_COST_ANNUAL,
  CELL_THERAPY_APPROACHES,
  CHILDHOOD_VACCINATION_COST_PER_DALY,
  CONCENTRATED_INTEREST_SECTOR_MARKET_CAP_USD,
  CURRENT_PATIENT_PARTICIPATION_RATE,
  DAYS_PER_YEAR,
  DCT_PLATFORM_FUNDING_MEDIUM,
  DEFENSE_SECTOR_RETENTION_PCT,
  DFDA_DIRECT_FUNDING_COST_PER_DALY,
  DFDA_DIRECT_FUNDING_QUEUE_CLEARANCE_NPV,
  DFDA_NPV_ADOPTION_RAMP_YEARS,
  DFDA_NPV_ANNUAL_OPEX,
  DFDA_NPV_UPFRONT_COST,
  DFDA_OBSERVATIONAL_COST_PER_PATIENT,
  DFDA_OPEX_COMMUNITY,
  DFDA_OPEX_INFRASTRUCTURE,
  DFDA_OPEX_PCT_OF_TREATY_FUNDING,
  DFDA_OPEX_PLATFORM_MAINTENANCE,
  DFDA_OPEX_REGULATORY,
  DFDA_OPEX_STAFF,
  DFDA_STORAGE_COST_BACKUP_PER_PATIENT_MONTHLY,
  DFDA_STORAGE_COST_COMPUTE_PER_PATIENT_MONTHLY,
  DFDA_STORAGE_COST_DATABASE_PER_PATIENT_MONTHLY,
  DFDA_STORAGE_COST_RAW_PER_PATIENT_MONTHLY,
  DFDA_TARGET_COST_PER_PATIENT_USD,
  DFDA_UPFRONT_BUILD,
  DFDA_UPFRONT_BUILD_MAX,
  DIH_NPV_ANNUAL_OPEX_INITIATIVES,
  DIH_NPV_UPFRONT_COST_INITIATIVES,
  DIH_TREASURY_MEDICAL_RESEARCH_PCT,
  DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL,
  DIH_TREASURY_TRIAL_SUBSIDIES_PCT,
  DISEASE_RELATED_CAREGIVER_PCT,
  DISEASE_VS_TERRORISM_DEATHS_RATIO,
  DISEASE_VS_WAR_DEATHS_RATIO,
  EFFECTIVE_HOURLY_RATE_LIFETIME_BENEFIT,
  EPIGENETIC_TARGETS_COUNT,
  EVENTUALLY_AVOIDABLE_DALY_PCT,
  EVENTUALLY_AVOIDABLE_DEATH_PCT,
  FAMILY_OFFICE_INVESTMENT_MIN,
  FUNDAMENTALLY_UNAVOIDABLE_DEATH_PCT,
  GLOBAL_MILITARY_SPENDING_POST_TREATY_ANNUAL_2024,
  GLOBAL_POLITICAL_REFORM_INVESTMENT,
  GLOBAL_POLITICAL_REFORM_INVESTMENT_MAXIMUM,
  HOURS_PER_DAY,
  HOURS_PER_YEAR,
  HUMAN_PROTEIN_CODING_GENES,
  IAB_BOOTSTRAP_CAMPAIGN_COST,
  IAB_MECHANISM_ANNUAL_COST,
  IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL,
  IAB_POLITICAL_INCENTIVE_FUNDING_PCT,
  INSTITUTIONAL_INVESTOR_MIN,
  LOBBYIST_BOND_INVESTMENT_MAX,
  MINUTES_PER_HOUR,
  MONTHS_PER_YEAR,
  NATO_POLITICAL_REFORM_INVESTMENT,
  NPV_DISCOUNT_RATE_STANDARD,
  NPV_TIME_HORIZON_YEARS,
  PEACE_DIVIDEND_DIRECT_FISCAL_SAVINGS,
  PHARMA_PHASE_2_3_COST_BARRIER,
  PRE_1962_VALIDATION_YEARS,
  QALYS_PER_COVID_DEATH_AVERTED,
  SAFE_COMPOUNDS_COUNT,
  SECONDS_PER_MINUTE,
  SECONDS_PER_YEAR,
  TESTED_RELATIONSHIPS_ESTIMATE,
  TOTAL_BOOK_WORDS,
  TREATY_ANNUAL_FUNDING,
  TREATY_CAMPAIGN_BUDGET_LOBBYING,
  TREATY_CAMPAIGN_BUDGET_RESERVE,
  TREATY_CAMPAIGN_BUDGET_SUPER_PACS,
  TREATY_CAMPAIGN_DURATION_YEARS,
  TREATY_CAMPAIGN_VIRAL_REFERENDUM_BASE_CASE,
  TREATY_REDIRECTED_SPENDING_INFINITE_ROI,
  TREATY_REDUCTION_PCT,
  TREATY_VS_DIRECT_FUNDING_LEVERAGE,
  TRIAL_RELEVANT_DISEASES_COUNT,
  US_CONGRESS_MEMBER_COUNT,
  US_DYSFUNCTION_PREMIUM_VS_SWITZERLAND,
  US_POLITICAL_REFORM_INVESTMENT_TOTAL,
  US_VS_SINGAPORE_SPENDING_GAP,
  US_VS_SWITZERLAND_LIFE_EXPECTANCY_GAP,
  US_VS_SWITZERLAND_SPENDING_GAP,
  VICTORY_BOND_ANNUAL_PAYOUT,
  VICTORY_BOND_ANNUAL_RETURN_PCT,
  VICTORY_BOND_FUNDING_PCT
} as const;

/** Union type of all parameter names */
export type ParameterName = keyof typeof parameters;

// ============================================================================
// Citations Lookup (CSL JSON)
// ============================================================================

/**
 * All citations in CSL JSON format
 * Use with citation processors like citeproc-js or citation-js
 * to format in any style (APA, MLA, Chicago, etc.)
 */
export const citations: Record<string, Citation> = {
  "3-5-rule": {
        id: "3-5-rule",
        type: "article-journal",
        title: "3.5% participation tipping point",
        author: [
          {
            literal: "Harvard Kennedy School"
          },
        ],
        issued: { 'date-parts': [[2020]] },
        'container-title': "Harvard Kennedy School",
        URL: "https://www.hks.harvard.edu/centers/carr/publications/35-rule-how-small-minority-can-change-world",
        note: "Harvard Kennedy School, The '3.5% rule': How a small minority can change the world | Chenoweth Research Paper (2020) | BBC Future, 2019, 'The 3.5% rule' | Wikipedia, 3.5% rule",
  },
  "95-pct-diseases-no-treatment": {
        id: "95-pct-diseases-no-treatment",
        type: "article-journal",
        title: "95% of diseases have no effective treatment",
        author: [
          {
            literal: "GAO"
          },
        ],
        issued: { 'date-parts': [[2025]] },
        'container-title': "GAO",
        URL: "https://www.gao.gov/products/gao-25-106774",
        note: "GAO, 2025, Rare Disease Drugs: FDA Has Steps Underway to Strengthen Coordination | Global Genes, RARE Disease Facts | Note: Only 5% of 7,000+ rare diseases have FDA-approved treatments",
  },
  "acled-active-combat-deaths": {
        id: "acled-active-combat-deaths",
        type: "article-journal",
        title: "Active combat deaths annually",
        author: [
          {
            literal: "ACLED"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "ACLED: Global Conflict Surged 2024",
        URL: "https://acleddata.com/2024/12/12/data-shows-global-conflict-surged-in-2024-the-washington-post/",
        note: "ACLED: Global Conflict Surged 2024 | Washington Post via ACLED | ACLED Conflict Index",
  },
  "antidepressant-trial-exclusion-rates": {
        id: "antidepressant-trial-exclusion-rates",
        type: "article-journal",
        title: "Antidepressant clinical trial exclusion rates",
        author: [
          {
            literal: "NIH"
          },
        ],
        issued: { 'date-parts': [[2015]] },
        'container-title': "Zimmerman et al.",
        URL: "https://pubmed.ncbi.nlm.nih.gov/26276679/",
        note: "Zimmerman et al., Mayo Clinic Proceedings, 2015 | Preskorn et al., Journal of Psychiatric Practice, 2015 | Wolters Kluwer: Antidepressant Trials Exclude Most Real World Patients",
  },
  "average-reading-speed": {
        id: "average-reading-speed",
        type: "webpage",
        title: "Average reading speed",
        author: [
          {
            literal: "Educational psychology literature"
          },
        ],
        publisher: "Educational psychology literature",
        note: "Educational psychology literature",
  },
  "average-us-hourly-wage": {
        id: "average-us-hourly-wage",
        type: "article-journal",
        title: "Average US hourly wage",
        author: [
          {
            literal: "BLS"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "BLS",
        URL: "https://www.bls.gov/news.release/pdf/ocwage.pdf",
        note: "BLS, Occupational Employment and Wages May 2024",
  },
  "bio-clinical-development-2021": {
        id: "bio-clinical-development-2021",
        type: "article-journal",
        title: "BIO Clinical Development Success Rates 2011-2020",
        author: [
          {
            literal: "Biotechnology Innovation Organization (BIO)"
          },
        ],
        issued: { 'date-parts': [[2021]] },
        'container-title': "Biotechnology Innovation Organization (BIO)",
        URL: "https://go.bio.org/rs/490-EHZ-999/images/ClinicalDevelopmentSuccessRates2011_2020.pdf",
        note: "Biotechnology Innovation Organization (BIO), 2021, Clinical Development Success Rates and Contributing Factors 2011-2020",
  },
  "bls-cpi-inflation-calculator": {
        id: "bls-cpi-inflation-calculator",
        type: "webpage",
        title: "CPI Inflation Calculator",
        author: [
          {
            literal: "U.S. Bureau of Labor Statistics"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        publisher: "U.S. Bureau of Labor Statistics",
        URL: "https://www.bls.gov/data/inflation_calculator.htm",
        note: "U.S. Bureau of Labor Statistics, 2024, CPI Inflation Calculator",
  },
  "cdc-life-expectancy": {
        id: "cdc-life-expectancy",
        type: "report",
        title: "US Life Expectancy 2023",
        author: [
          {
            literal: "Centers for Disease Control and Prevention"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        publisher: "CDC",
        URL: "https://www.cdc.gov/nchs/fastats/life-expectancy.htm",
        note: "CDC, 2024, Life Expectancy",
  },
  "census-income-2023": {
        id: "census-income-2023",
        type: "report",
        title: "US Median Household Income 2023",
        author: [
          {
            literal: "US Census Bureau"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        publisher: "US Census Bureau",
        URL: "https://www.census.gov/library/publications/2024/demo/p60-282.html",
        note: "US Census Bureau, 2024, Income in the United States: 2023",
  },
  "ceo-compensation": {
        id: "ceo-compensation",
        type: "article-journal",
        title: "CEO compensation",
        author: [
          {
            literal: "EPI"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "EPI",
        URL: "https://www.epi.org/blog/ceo-pay-increased-in-2024-and-is-now-281-times-that-of-the-typical-worker-new-epi-landing-page-has-all-the-details/",
        note: "EPI, CEO Pay 2024",
  },
  "chance-of-dying-from-terrorism-1-in-30m": {
        id: "chance-of-dying-from-terrorism-1-in-30m",
        type: "article-journal",
        title: "Chance of dying from terrorism statistic",
        author: [
          {
            literal: "Cato Institute"
          },
        ],
        'container-title': "Cato Institute: Terrorism and Immigration Risk Analysis",
        URL: "https://www.cato.org/policy-analysis/terrorism-immigration-risk-analysis",
        note: "Cato Institute: Terrorism and Immigration Risk Analysis | NBC News: Lightning vs Terrorism",
  },
  "childhood-vaccination-economic-benefits": {
        id: "childhood-vaccination-economic-benefits",
        type: "article-journal",
        title: "Childhood vaccination economic benefits",
        author: [
          {
            literal: "CDC MMWR"
          },
        ],
        issued: { 'date-parts': [[1994]] },
        'container-title': "CDC MMWR",
        URL: "https://www.cdc.gov/mmwr/volumes/73/wr/mm7331a2.htm",
        note: "CDC MMWR, Childhood Immunizations 1994-2023 | The Lancet, 50 Years of Expanded Programme on Immunization00850-X/fulltext)",
  },
  "childhood-vaccination-roi": {
        id: "childhood-vaccination-roi",
        type: "article-journal",
        title: "Childhood Vaccination (US) ROI",
        author: [
          {
            literal: "CDC"
          },
        ],
        issued: { 'date-parts': [[2017]] },
        'container-title': "CDC",
        URL: "https://www.cdc.gov/mmwr/preview/mmwrhtml/mm6316a4.htm",
        note: "CDC, Link | Vaxopedia, Link",
  },
  "chronic-illness-workforce-productivity-loss": {
        id: "chronic-illness-workforce-productivity-loss",
        type: "article-journal",
        title: "Chronic illness workforce productivity loss",
        author: [
          {
            literal: "Integrated Benefits Institute"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "Integrated Benefits Institute 2024",
        URL: "https://www.ibiweb.org/resources/chronic-conditions-in-the-us-workforce-prevalence-trends-and-productivity-impacts",
        note: "Integrated Benefits Institute 2024, Chronic Conditions in US Workforce | One Medical 2024, Study on Chronic Conditions | de Beaumont Foundation 2025, Poll on Chronic Health Conditions",
  },
  "clean-water-sanitation-roi": {
        id: "clean-water-sanitation-roi",
        type: "article-journal",
        title: "Clean Water & Sanitation (LMICs) ROI",
        author: [
          {
            literal: "UN News"
          },
        ],
        issued: { 'date-parts': [[2014]] },
        'container-title': "UN News",
        URL: "https://news.un.org/en/story/2014/11/484032",
        note: "UN News, Link | WaterAid, Link",
  },
  "clemens2011": {
        id: "clemens2011",
        type: "article-journal",
        title: "Economics and Emigration: Trillion-Dollar Bills on the Sidewalk?",
        author: [
          {
            family: "Clemens",
            given: "Michael A."
          },
        ],
        issued: { 'date-parts': [[2011]] },
        'container-title': "Journal of Economic Perspectives",
        URL: "https://www.aeaweb.org/articles?id=10.1257%2Fjep.25.3.83",
  },
  "clinical-trial-abandonment-rate": {
        id: "clinical-trial-abandonment-rate",
        type: "webpage",
        title: "Clinical trial abandonment",
        author: [
          {
            literal: "Industry estimates"
          },
        ],
        publisher: "Industry estimates",
        note: "Industry estimates",
  },
  "clinical-trial-patient-participation-rate": {
        id: "clinical-trial-patient-participation-rate",
        type: "article-journal",
        title: "Clinical trial patient participation rate",
        author: [
          {
            literal: "ACS CAN"
          },
        ],
        'container-title': "ACS CAN: Barriers to Clinical Trial Enrollment",
        URL: "https://www.fightcancer.org/policy-resources/barriers-patient-enrollment-therapeutic-clinical-trials-cancer",
        note: "ACS CAN: Barriers to Clinical Trial Enrollment | HINTS: Clinical Trial Participation",
  },
  "clinical-trials-puzzle-interactome": {
        id: "clinical-trials-puzzle-interactome",
        type: "article-journal",
        title: "Only ~12% of human interactome targeted",
        author: [
          {
            literal: "PMC"
          },
        ],
        issued: { 'date-parts': [[2023]] },
        'container-title': "PMC",
        URL: "https://pmc.ncbi.nlm.nih.gov/articles/PMC10749231/",
        note: "PMC, 2023, The Clinical Trials Puzzle",
  },
  "clinicaltrials-gov-enrollment-data-2025": {
        id: "clinicaltrials-gov-enrollment-data-2025",
        type: "article-journal",
        title: "ClinicalTrials.gov cumulative enrollment data (2025)",
        author: [
          {
            literal: "Direct analysis via"
          },
        ],
        'container-title': "Direct analysis via ClinicalTrials.gov API v2",
        URL: "https://clinicaltrials.gov/data-api/api",
        note: "Direct analysis via ClinicalTrials.gov API v2",
  },
  "costsofwar2023": {
        id: "costsofwar2023",
        type: "report",
        title: "Blood and Treasure: United States Budgetary Costs and Human Costs of 20 Years of War",
        author: [
          {
            family: "Crawford",
            given: "Neta C. and Lutz, Catherine"
          },
        ],
        issued: { 'date-parts': [[2023]] },
        URL: "https://costsofwar.watson.brown.edu/",
  },
  "cs-global-wealth-report-2023": {
        id: "cs-global-wealth-report-2023",
        type: "article-journal",
        title: "Credit Suisse Global Wealth Report 2023",
        author: [
          {
            literal: "Credit Suisse/UBS"
          },
        ],
        issued: { 'date-parts': [[2023]] },
        'container-title': "Credit Suisse/UBS",
        URL: "https://www.ubs.com/global/en/family-office-uhnw/reports/global-wealth-report-2023.html",
        note: "Credit Suisse/UBS, 2023, Global Wealth Report 2023",
  },
  "delrosal2011": {
        id: "delrosal2011",
        type: "article-journal",
        title: "The Empirical Measurement of Rent-Seeking Costs",
        author: [
          {
            family: "Del Rosal",
            given: "Ignacio"
          },
        ],
        issued: { 'date-parts': [[2011]] },
        'container-title': "Journal of Economic Surveys",
        URL: "https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-6419.2009.00621.x",
  },
  "deworming-cost-per-daly": {
        id: "deworming-cost-per-daly",
        type: "article-journal",
        title: "Cost per DALY for Deworming Programs",
        author: [
          {
            literal: "GiveWell"
          },
        ],
        'container-title': "GiveWell: Cost-Effectiveness in $/DALY for Deworming",
        URL: "https://www.givewell.org/international/technical/programs/deworming/cost-effectiveness",
        note: "GiveWell: Cost-Effectiveness in $/DALY for Deworming",
  },
  "disease-cost-alzheimers-1300b": {
        id: "disease-cost-alzheimers-1300b",
        type: "article-journal",
        title: "Annual global economic burden of Alzheimer's and other dementias",
        author: [
          {
            literal: "WHO"
          },
        ],
        issued: { 'date-parts': [[2019]] },
        'container-title': "WHO: Dementia Fact Sheet",
        URL: "https://www.who.int/news-room/fact-sheets/detail/dementia",
        note: "WHO: Dementia Fact Sheet | Alzheimer's & Dementia: Worldwide Costs 2019",
  },
  "disease-cost-cancer-1800b": {
        id: "disease-cost-cancer-1800b",
        type: "article-journal",
        title: "Annual global economic burden of cancer",
        author: [
          {
            literal: "JAMA Oncology"
          },
        ],
        issued: { 'date-parts': [[2020]] },
        'container-title': "JAMA Oncology: Global Cost 2020-2050",
        URL: "https://jamanetwork.com/journals/jamaoncology/fullarticle/2801798",
        note: "JAMA Oncology: Global Cost 2020-2050 | Nature: $25T Over 30 Years",
  },
  "disease-cost-diabetes-1500b": {
        id: "disease-cost-diabetes-1500b",
        type: "article-journal",
        title: "Annual global economic burden of diabetes",
        author: [
          {
            literal: "Diabetes Care"
          },
        ],
        'container-title': "Diabetes Care: Global Economic Burden",
        URL: "https://diabetesjournals.org/care/article/41/5/963/36522/Global-Economic-Burden-of-Diabetes-in-Adults",
        note: "Diabetes Care: Global Economic Burden | Lancet: Diabetes Economic Burden30100-6/abstract)",
  },
  "disease-cost-heart-disease-2100b": {
        id: "disease-cost-heart-disease-2100b",
        type: "article-journal",
        title: "Annual global economic burden of heart disease",
        author: [
          {
            literal: "Int'l Journal of Cardiology"
          },
        ],
        issued: { 'date-parts': [[2050]] },
        'container-title': "Int'l Journal of Cardiology: Global Heart Failure Burden02238-9/abstract)",
        URL: "https://www.internationaljournalofcardiology.com/article/S0167-5273(13",
        note: "Int'l Journal of Cardiology: Global Heart Failure Burden02238-9/abstract) | AHA: US CVD Costs to 2050",
  },
  "disease-economic-burden-109t": {
        id: "disease-economic-burden-109t",
        type: "webpage",
        title: "\\$109 trillion annual global disease burden",
        author: [
          {
            literal: "Calculated from IHME Global Burden of Disease (2.55B DALYs) and global GDP per capita valuation"
          },
        ],
        publisher: "Calculated from IHME Global Burden of Disease (2.55B DALYs) and global GDP per capita valuation",
        note: "Calculated from IHME Global Burden of Disease (2.55B DALYs) and global GDP per capita valuation",
  },
  "disease-prevalence-2-billion": {
        id: "disease-prevalence-2-billion",
        type: "article-journal",
        title: "Global prevalence of chronic disease",
        author: [
          {
            literal: "ScienceDaily"
          },
        ],
        issued: { 'date-parts': [[2015]] },
        'container-title': "ScienceDaily: GBD 2015 Study",
        URL: "https://www.sciencedaily.com/releases/2015/06/150608081753.htm",
        note: "ScienceDaily: GBD 2015 Study | PMC: Burden of Chronic Disease | PMC: Multiple Chronic Conditions",
  },
  "diseases-getting-first-treatment-annually": {
        id: "diseases-getting-first-treatment-annually",
        type: "article-journal",
        title: "Diseases Getting First Effective Treatment Each Year",
        author: [
          {
            literal: "Calculated from Orphanet Journal of Rare Diseases (2024)"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "Calculated from Orphanet Journal of Rare Diseases (2024)",
        URL: "https://ojrd.biomedcentral.com/articles/10.1186/s13023-024-03398-1",
        note: "Calculated from Orphanet Journal of Rare Diseases (2024), FDA Novel Drug Approvals data",
  },
  "disparity-ratio-weapons-vs-cures": {
        id: "disparity-ratio-weapons-vs-cures",
        type: "article-journal",
        title: "36:1 disparity ratio of spending on weapons over cures",
        author: [
          {
            literal: "SIPRI"
          },
        ],
        issued: { 'date-parts': [[2016]] },
        'container-title': "SIPRI: Military Spending",
        URL: "https://www.sipri.org/commentary/blog/2016/opportunity-cost-world-military-spending",
        note: "SIPRI: Military Spending | PMC: Military vs Healthcare Crowding Out | Congress.gov: Global R&D Landscape",
  },
  "dot-vsl-13-6m": {
        id: "dot-vsl-13-6m",
        type: "article-journal",
        title: "DOT Value of Statistical Life (\\$13.6M)",
        author: [
          {
            literal: "DOT"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "DOT: VSL Guidance 2024",
        URL: "https://www.transportation.gov/office-policy/transportation-policy/revised-departmental-guidance-on-valuation-of-a-statistical-life-in-economic-analysis",
        note: "DOT: VSL Guidance 2024 | DOT: Economic Values Used in Analysis",
  },
  "drug-development-cost": {
        id: "drug-development-cost",
        type: "webpage",
        title: "Cost of drug development",
        author: [
          {
            literal: "Tufts CSDD"
          },
        ],
        publisher: "Tufts CSDD",
        note: "Tufts CSDD | IQVIA | Deloitte",
  },
  "drug-repurposing-rate": {
        id: "drug-repurposing-rate",
        type: "article-journal",
        title: "Drug Repurposing Rate (~30%)",
        author: [
          {
            literal: "Nature Medicine"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "Nature Medicine",
        URL: "https://www.nature.com/articles/s41591-024-03233-x",
        note: "Nature Medicine, 2024, Drug Repurposing Trends",
  },
  "drug-trial-success-rate-12-pct": {
        id: "drug-trial-success-rate-12-pct",
        type: "article-journal",
        title: "Drug trial success rate from Phase I to approval",
        author: [
          {
            literal: "Nature Reviews Drug Discovery"
          },
        ],
        issued: { 'date-parts': [[2016]] },
        'container-title': "Nature Reviews Drug Discovery: Clinical Success Rates",
        URL: "https://www.nature.com/articles/nrd.2016.136",
        note: "Nature Reviews Drug Discovery: Clinical Success Rates | PMC: Estimating Success Rates | Oxford Academic: Clinical Trial Success",
  },
  "drugpolicyalliance2021": {
        id: "drugpolicyalliance2021",
        type: "report",
        title: "The Drug War by the Numbers",
        author: [
          {
            literal: "Drug Policy Alliance"
          },
        ],
        issued: { 'date-parts': [[2021]] },
        URL: "https://drugpolicy.org/drug-war-stats/",
  },
  "education-investment-economic-multiplier": {
        id: "education-investment-economic-multiplier",
        type: "article-journal",
        title: "Education investment economic multiplier (2.1)",
        author: [
          {
            literal: "EPI"
          },
        ],
        'container-title': "EPI: Public Investments Outside Core Infrastructure",
        URL: "https://www.epi.org/publication/bp348-public-investments-outside-core-infrastructure/",
        note: "EPI: Public Investments Outside Core Infrastructure | World Bank: Returns to Investment in Education | Freopp: Education ROI Framework",
  },
  "environmental-cost-of-war": {
        id: "environmental-cost-of-war",
        type: "article-journal",
        title: "Environmental cost of war (\\$100B annually)",
        author: [
          {
            literal: "Brown Watson Costs of War"
          },
        ],
        'container-title': "Brown Watson Costs of War: Environmental Cost",
        URL: "https://watson.brown.edu/costsofwar/costs/social/environment",
        note: "Brown Watson Costs of War: Environmental Cost | Earth.Org: Environmental Impact of Wars | Transform Defence: Military Spending & Climate",
  },
  "ewg-farm-subsidies": {
        id: "ewg-farm-subsidies",
        type: "article-journal",
        title: "US Farm Subsidy Database and Analysis",
        author: [
          {
            literal: "Environmental Working Group"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "Environmental Working Group",
        URL: "https://farm.ewg.org/",
        note: "Environmental Working Group, Farm Subsidy Database | USDA Economic Research Service, Agricultural Subsidies",
  },
  "fda-approval-timeline-10-years": {
        id: "fda-approval-timeline-10-years",
        type: "article-journal",
        title: "FDA drug approval timeline",
        author: [
          {
            literal: "Drugs.com"
          },
        ],
        'container-title': "Drugs.com: FDA Drug Approval Process",
        URL: "https://www.drugs.com/fda-approval-process.html",
        note: "Drugs.com: FDA Drug Approval Process | FDAReview.org: Drug Development & Approval | PMC: Drugs, Devices, FDA Overview",
  },
  "fda-approved-products-20k": {
        id: "fda-approved-products-20k",
        type: "article-journal",
        title: "FDA-approved prescription drug products (20,000+)",
        author: [
          {
            literal: "FDA"
          },
        ],
        'container-title': "FDA",
        URL: "https://www.fda.gov/media/143704/download",
        note: "FDA, Facts About Generic Drugs",
  },
  "fda-gras-list-count": {
        id: "fda-gras-list-count",
        type: "article-journal",
        title: "FDA GRAS List Count (~570-700)",
        author: [
          {
            literal: "FDA"
          },
        ],
        'container-title': "FDA",
        URL: "https://www.fda.gov/food/generally-recognized-safe-gras/gras-notice-inventory",
        note: "FDA, GRAS Notice Inventory",
  },
  "fec-2024-summary": {
        id: "fec-2024-summary",
        type: "report",
        title: "Statistical Summary of 24-Month Campaign Activity of the 2023-2024 Election Cycle",
        author: [
          {
            literal: "Federal Election Commission"
          },
        ],
        issued: { 'date-parts': [[2023]] },
        publisher: "Federal Election Commission",
        URL: "https://www.fec.gov/updates/statistical-summary-of-24-month-campaign-activity-of-the-2023-2024-election-cycle/",
        note: "Federal Election Commission, Statistical Summary of 24-Month Campaign Activity",
  },
  "givewell-cost-per-life-saved": {
        id: "givewell-cost-per-life-saved",
        type: "article-journal",
        title: "GiveWell Cost per Life Saved for Top Charities (2024)",
        author: [
          {
            literal: "GiveWell"
          },
        ],
        'container-title': "GiveWell: Top Charities",
        URL: "https://www.givewell.org/charities/top-charities",
        note: "GiveWell: Top Charities | GiveWell: Helen Keller Vitamin A | Our World in Data: Cost-Effectiveness",
  },
  "global-clinical-trials-market-2024": {
        id: "global-clinical-trials-market-2024",
        type: "article-journal",
        title: "Global clinical trials market 2024",
        author: [
          {
            literal: "Research and Markets"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "Research and Markets",
        URL: "https://www.globenewswire.com/news-release/2024/04/19/2866012/0/en/Global-Clinical-Trials-Market-Research-Report-2024-An-83-16-Billion-Market-by-2030-AI-Machine-Learning-and-Blockchain-will-Transform-the-Clinical-Trials-Landscape.html",
        note: "Research and Markets, Global Clinical Trials Market Report 2024 | Precedence Research, Clinical Trials Market Size",
  },
  "global-gov-med-research-spending": {
        id: "global-gov-med-research-spending",
        type: "article-journal",
        title: "Global government medical research spending (\\$67.5B, 2023–2024)",
        author: [
          {
            literal: "See component country budgets:"
          },
        ],
        'container-title': "See component country budgets: NIH Budget",
        URL: "#nih-budget-fy2025",
        note: "See component country budgets: NIH Budget, China R&D, EU Horizon Health",
  },
  "global-government-clinical-trial-spending-estimate": {
        id: "global-government-clinical-trial-spending-estimate",
        type: "article-journal",
        title: "Global government spending on interventional clinical trials: ~$3-6 billion/year",
        author: [
          {
            literal: "Applied Clinical Trials"
          },
        ],
        'container-title': "Applied Clinical Trials",
        URL: "https://www.appliedclinicaltrialsonline.com/view/sizing-clinical-research-market",
        note: "Applied Clinical Trials | Lancet Global Health30357-0/fulltext)",
  },
  "global-military-spending": {
        id: "global-military-spending",
        type: "article-journal",
        title: "Global military spending (\\$2.72T, 2024)",
        author: [
          {
            literal: "SIPRI"
          },
        ],
        issued: { 'date-parts': [[2025]] },
        'container-title': "SIPRI",
        URL: "https://www.sipri.org/publications/2025/sipri-fact-sheets/trends-world-military-expenditure-2024",
        note: "SIPRI, 2025, Trends in World Military Expenditure 2024",
  },
  "global-new-drug-approvals-50-annually": {
        id: "global-new-drug-approvals-50-annually",
        type: "article-journal",
        title: "Annual number of new drugs approved globally: ~50",
        author: [
          {
            literal: "C&EN"
          },
        ],
        issued: { 'date-parts': [[2025]] },
        'container-title': "C&EN",
        URL: "https://cen.acs.org/pharmaceuticals/50-new-drugs-received-FDA/103/i2",
        note: "C&EN, 2025, 50 new drugs received FDA approval in 2024 | FDA, Novel Drug Approvals | Note: Average ~50 per year 2018-2024; 32 small molecules + 18 biologics in 2024",
  },
  "global-pharma-rd-spending-300b": {
        id: "global-pharma-rd-spending-300b",
        type: "report",
        title: "Global pharmaceutical R&D spending",
        author: [
          {
            literal: "Industry reports: IQVIA"
          },
        ],
        publisher: "Industry reports: IQVIA",
        note: "Industry reports: IQVIA, EvaluatePharma, PhRMA",
  },
  "global-population-8-billion": {
        id: "global-population-8-billion",
        type: "article-journal",
        title: "Global population reaches 8 billion",
        author: [
          {
            literal: "UN"
          },
        ],
        issued: { 'date-parts': [[2022]] },
        'container-title': "UN: World Population 8 Billion Nov 15 2022",
        URL: "https://www.un.org/en/desa/world-population-reach-8-billion-15-november-2022",
        note: "UN: World Population 8 Billion Nov 15 2022 | UN: Day of 8 Billion | Wikipedia: Day of Eight Billion",
  },
  "global-trial-participant-capacity": {
        id: "global-trial-participant-capacity",
        type: "article-journal",
        title: "Global trial capacity",
        author: [
          {
            literal: "IQVIA Report"
          },
        ],
        'container-title': "IQVIA Report: Clinical Trial Subjects Number Drops Due to Decline in COVID-19 Enrollment",
        URL: "https://gmdpacademy.org/news/iqvia-report-clinical-trial-subjects-number-drops-due-to-decline-in-covid-19-enrollment/",
        note: "IQVIA Report: Clinical Trial Subjects Number Drops Due to Decline in COVID-19 Enrollment",
  },
  "gtd-terror-attack-deaths": {
        id: "gtd-terror-attack-deaths",
        type: "article-journal",
        title: "Terror attack deaths (8,300 annually)",
        author: [
          {
            literal: "Our World in Data"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "Our World in Data: Terrorism",
        URL: "https://ourworldindata.org/terrorism",
        note: "Our World in Data: Terrorism | Global Terrorism Index 2024 | START Global Terrorism Database | Our World in Data: Terrorism Deaths",
  },
  "hayek1945": {
        id: "hayek1945",
        type: "article-journal",
        title: "The Use of Knowledge in Society",
        author: [
          {
            family: "Hayek",
            given: "Friedrich A."
          },
        ],
        issued: { 'date-parts': [[1945]] },
        'container-title': "American Economic Review",
        URL: "https://www.econlib.org/library/Essays/hykKnw.html",
  },
  "healthcare-investment-economic-multiplier": {
        id: "healthcare-investment-economic-multiplier",
        type: "article-journal",
        title: "Healthcare investment economic multiplier (1.8)",
        author: [
          {
            literal: "PMC"
          },
        ],
        issued: { 'date-parts': [[2022]] },
        'container-title': "PMC: California Universal Health Care",
        URL: "https://pmc.ncbi.nlm.nih.gov/articles/PMC5954824/",
        note: "PMC: California Universal Health Care | CEPR: Government Investment | PMC: Health Sector Investment & Growth | ODI: Fiscal Multipliers Review",
  },
  "hsieh-moretti2019": {
        id: "hsieh-moretti2019",
        type: "article-journal",
        title: "Housing Constraints and Spatial Misallocation",
        author: [
          {
            family: "Hsieh",
            given: "Chang-Tai and Enrico Moretti"
          },
        ],
        issued: { 'date-parts': [[2019]] },
        'container-title': "Hsieh & Moretti",
        URL: "https://www.aeaweb.org/articles?id=10.1257/mac.20170388",
        note: "Hsieh & Moretti, 2019, AEJ:Macro | Highly cited - one of most influential papers in urban economics",
  },
  "human-genome-and-genetic-editing": {
        id: "human-genome-and-genetic-editing",
        type: "article-journal",
        title: "Human Genome Project and CRISPR Discovery",
        author: [
          {
            literal: "NHGRI"
          },
        ],
        issued: { 'date-parts': [[2003]] },
        'container-title': "NHGRI",
        URL: "https://www.genome.gov/11006929/2003-release-international-consortium-completes-hgp",
        note: "NHGRI, International Consortium Completes Human Genome Project | Nobel Prize, The Nobel Prize in Chemistry 2020 | Note: HGP cost ~$2.7B; CRISPR discovered by Doudna & Charpentier in 2012",
  },
  "icbl-ottawa-treaty": {
        id: "icbl-ottawa-treaty",
        type: "article-journal",
        title: "International Campaign to Ban Landmines (ICBL) - Ottawa Treaty (1997)",
        author: [
          {
            literal: "ICRC"
          },
        ],
        issued: { 'date-parts': [[1997]] },
        'container-title': "ICRC",
        URL: "https://www.icrc.org/en/doc/resources/documents/article/other/57jpjn.htm",
        note: "ICRC, Ottawa Treaty History | Wikipedia, International Campaign to Ban Landmines | Nobel Prize, 1997 Peace Prize | UN Press, ICBL Press Conference 1999 | Landmine Monitor, Mine Action Funding",
  },
  "icd-10-code-count": {
        id: "icd-10-code-count",
        type: "article-journal",
        title: "ICD-10 Code Count (~14,000)",
        author: [
          {
            literal: "WHO"
          },
        ],
        issued: { 'date-parts': [[2019]] },
        'container-title': "WHO",
        URL: "https://icd.who.int/browse10/2019/en",
        note: "WHO, ICD-10 Browser",
  },
  "ihme-gbd-2021": {
        id: "ihme-gbd-2021",
        type: "article-journal",
        title: "IHME Global Burden of Disease 2021 (2.88B DALYs, 1.13B YLD)",
        author: [
          {
            literal: "Institute for Health Metrics and Evaluation (IHME)"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "Institute for Health Metrics and Evaluation (IHME)",
        URL: "https://vizhub.healthdata.org/gbd-results/",
        note: "Institute for Health Metrics and Evaluation (IHME), GBD Results Tool | The Lancet, 2024, Global burden of 371 diseases and injuries, and 87 risk factors, in 204 countries, 2000-202100757-8/fulltext) | IHME, Global Burden of Disease Study 2021",
  },
  "imf-fossilfuel2023": {
        id: "imf-fossilfuel2023",
        type: "report",
        title: "IMF Fossil Fuel Subsidies Data: 2023 Update",
        author: [
          {
            literal: "International Monetary Fund"
          },
        ],
        issued: { 'date-parts': [[2023]] },
        URL: "https://www.imf.org/en/Blogs/Articles/2023/08/24/fossil-fuel-subsidies-surged-to-record-7-trillion",
  },
  "imf-singapore-spending": {
        id: "imf-singapore-spending",
        type: "report",
        title: "IMF Singapore Government Spending Data",
        author: [
          {
            literal: "International Monetary Fund"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        publisher: "IMF",
        URL: "https://www.imf.org/en/Countries/SGP",
        note: "IMF, 2024, Singapore Country Data",
  },
  "industry-clinical-trial-spending-estimate": {
        id: "industry-clinical-trial-spending-estimate",
        type: "webpage",
        title: "Private industry clinical trial spending",
        author: [
          {
            literal: "Derived from global market size and public/private funding ratios"
          },
        ],
        publisher: "Derived from global market size and public/private funding ratios",
        note: "Derived from global market size and public/private funding ratios",
  },
  "industry-vs-government-trial-spending-split": {
        id: "industry-vs-government-trial-spending-split",
        type: "article-journal",
        title: "Industry vs. Government Clinical Trial Spending Split (90/10)",
        author: [
          {
            literal: "Applied Clinical Trials"
          },
        ],
        'container-title': "Applied Clinical Trials",
        URL: "https://www.appliedclinicaltrialsonline.com/view/sizing-clinical-research-market",
        note: "Applied Clinical Trials | TCTMD",
  },
  "infrastructure-investment-economic-multiplier": {
        id: "infrastructure-investment-economic-multiplier",
        type: "article-journal",
        title: "Infrastructure investment economic multiplier (1.6)",
        author: [
          {
            literal: "World Bank"
          },
        ],
        issued: { 'date-parts': [[2022]] },
        'container-title': "World Bank: Infrastructure Investment as Stimulus",
        URL: "https://blogs.worldbank.org/en/ppps/effectiveness-infrastructure-investment-fiscal-stimulus-what-weve-learned",
        note: "World Bank: Infrastructure Investment as Stimulus | Global Infrastructure Hub: Fiscal Multiplier | CEPR: Government Investment | Richmond Fed: Infrastructure Spending",
  },
  "kleiner2013": {
        id: "kleiner2013",
        type: "article-journal",
        title: "Analyzing the Extent and Influence of Occupational Licensing on the Labor Market",
        author: [
          {
            family: "Kleiner",
            given: "Morris M. and Krueger, Alan B."
          },
        ],
        issued: { 'date-parts': [[2013]] },
        'container-title': "Journal of Labor Economics",
        URL: "https://www.journals.uchicago.edu/doi/abs/10.1086/669060",
  },
  "kydland1977": {
        id: "kydland1977",
        type: "article-journal",
        title: "Rules Rather than Discretion: The Inconsistency of Optimal Plans",
        author: [
          {
            family: "Kydland",
            given: "Finn E. and Prescott, Edward C."
          },
        ],
        issued: { 'date-parts': [[1977]] },
        'container-title': "Journal of Political Economy",
        URL: "https://www.nobelprize.org/uploads/2018/06/advanced-economicsciences2004.pdf",
  },
  "life-expectancy-gains-smoking-reduction": {
        id: "life-expectancy-gains-smoking-reduction",
        type: "article-journal",
        title: "Contribution of smoking reduction to life expectancy gains",
        author: [
          {
            literal: "PMC"
          },
        ],
        issued: { 'date-parts': [[2012]] },
        'container-title': "PMC: Benefits Smoking Cessation Longevity",
        URL: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1447499/",
        note: "PMC: Benefits Smoking Cessation Longevity | CDC: Estimating Benefits Smoking Reductions | AJPM: Benefits Quitting Different Ages00217-4/fulltext) | NEJM: 21st-Century Hazards & Benefits",
  },
  "life-expectancy-increase-pre-1962": {
        id: "life-expectancy-increase-pre-1962",
        type: "webpage",
        title: "US life expectancy growth 1880-1960: 3.82 years per decade",
        author: [
          {
            literal: "Source: US Life Expectancy FDA Budget 1543-2019 CSV"
          },
        ],
        issued: { 'date-parts': [[2019]] },
        publisher: "Source: US Life Expectancy FDA Budget 1543-2019 CSV",
        URL: "knowledge/data/us-life-expectancy-fda-budget-1543-2019.csv",
        note: "Source: US Life Expectancy FDA Budget 1543-2019 CSV | Our World in Data: Life Expectancy | Primary sources: Human Mortality Database (historical), CDC NCHS National Vital Statistics (modern)",
  },
  "lobbying-spend-defense": {
        id: "lobbying-spend-defense",
        type: "article-journal",
        title: "Lobbying Spend (Defense)",
        author: [
          {
            literal: "OpenSecrets"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "OpenSecrets",
        URL: "https://www.opensecrets.org/federal-lobbying/industries/summary?cycle=2024&id=D",
        note: "OpenSecrets, 2024, Defense Lobbying",
  },
  "lobbyist-statistics-dc": {
        id: "lobbyist-statistics-dc",
        type: "article-journal",
        title: "Lobbyist statistics for Washington D.C.",
        author: [
          {
            literal: "OpenSecrets"
          },
        ],
        'container-title': "OpenSecrets: Lobbying in US",
        URL: "https://en.wikipedia.org/wiki/Lobbying_in_the_United_States",
        note: "OpenSecrets: Lobbying in US | OpenSecrets: Revolving Door | Citizen.org: Revolving Congress | ProPublica: 281 Lobbyists Trump Admin",
  },
  "longevity-escape-velocity": {
        id: "longevity-escape-velocity",
        type: "article-journal",
        title: "Longevity Escape Velocity (LEV) - Maximum Human Life Extension Potential",
        author: [
          {
            literal: "Wikipedia"
          },
        ],
        'container-title': "Wikipedia: Longevity Escape Velocity",
        URL: "https://en.wikipedia.org/wiki/Longevity_escape_velocity",
        note: "Wikipedia: Longevity Escape Velocity | PMC: Escape Velocity - Why Life Extension Matters Now | Popular Mechanics: Can Science Cure Death? | Diamandis: Longevity Escape Velocity",
  },
  "lost-human-capital-war-cost": {
        id: "lost-human-capital-war-cost",
        type: "article-journal",
        title: "Lost human capital due to war (\\$270B annually)",
        author: [
          {
            literal: "Think by Numbers"
          },
        ],
        issued: { 'date-parts': [[2021]] },
        'container-title': "Think by Numbers: War Costs $74",
        URL: "<https://thinkbynumbers.org/military/war/the-economic-case-for-peace-a-comprehensive-financial-analysis/>",
        note: "Think by Numbers: War Costs $74,259/Lifetime | WEF: War Violence Costs $5/Day | PubMed: Economic Value DALYs Violence",
  },
  "measles-vaccination-roi": {
        id: "measles-vaccination-roi",
        type: "article-journal",
        title: "Measles Vaccination ROI",
        author: [
          {
            literal: "MDPI Vaccines"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "MDPI Vaccines",
        URL: "https://www.mdpi.com/2076-393X/12/11/1210",
        note: "MDPI Vaccines, 2024, Health and Economic Benefits of US Measles and Rubella Control | Taylor & Francis, 2024, Economic Evaluation of Second MCV Dose",
  },
  "medical-research-lives-saved-annually": {
        id: "medical-research-lives-saved-annually",
        type: "article-journal",
        title: "Medical research lives saved annually (4.2 million)",
        author: [
          {
            literal: "ScienceDaily"
          },
        ],
        issued: { 'date-parts': [[2020]] },
        'container-title': "ScienceDaily: Physical Activity Prevents 4M Deaths",
        URL: "https://www.sciencedaily.com/releases/2020/06/200617194510.htm",
        note: "ScienceDaily: Physical Activity Prevents 4M Deaths | PMC: Lives Saved by COVID Vaccines | Circulation: Three Interventions Save 94M Lives | PMC: Saving Millions Pandemic Research",
  },
  "mental-health-burden": {
        id: "mental-health-burden",
        type: "article-journal",
        title: "Mental health global burden",
        author: [
          {
            literal: "World Health Organization"
          },
        ],
        issued: { 'date-parts': [[2022]] },
        'container-title': "World Health Organization",
        URL: "https://www.who.int/news/item/28-09-2001-the-world-health-report-2001-mental-disorders-affect-one-in-four-people",
        note: "World Health Organization, 2022, Mental Health Fact Sheet",
  },
  "military-spending-economic-multiplier": {
        id: "military-spending-economic-multiplier",
        type: "article-journal",
        title: "Military spending economic multiplier (0.6)",
        author: [
          {
            literal: "Mercatus"
          },
        ],
        'container-title': "Mercatus: Defense Spending and Economy",
        URL: "https://www.mercatus.org/research/research-papers/defense-spending-and-economy",
        note: "Mercatus: Defense Spending and Economy | CEPR: WWII Spending Multipliers | RAND: Defense Spending Economic Growth",
  },
  "nih-budget-fy2025": {
        id: "nih-budget-fy2025",
        type: "article-journal",
        title: "NIH Budget (FY 2025)",
        author: [
          {
            literal: "NIH"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "NIH",
        URL: "https://www.nih.gov/about-nih/organization/budget",
        note: "NIH, 2024, Budget Overview | NIH, Office of Budget | Note: FY2024 budget was $47.1B",
  },
  "nih-clinical-trials-spending-pct-3-3": {
        id: "nih-clinical-trials-spending-pct-3-3",
        type: "article-journal",
        title: "NIH spending on clinical trials: ~3.3%",
        author: [
          {
            literal: "Bentley et al."
          },
        ],
        issued: { 'date-parts': [[2023]] },
        'container-title': "Bentley et al.",
        URL: "https://www.fiercebiotech.com/biotech/nih-spending-clinical-trials-reached-81b-over-decade",
        note: "Bentley et al., 2023 | Fierce Biotech: NIH Spending",
  },
  "nonprofit-clinical-trial-spending-estimate": {
        id: "nonprofit-clinical-trial-spending-estimate",
        type: "legislation",
        title: "Nonprofit clinical trial funding estimate",
        author: [
          {
            literal: "Estimated from major foundation budgets and activities"
          },
        ],
        publisher: "Estimated from major foundation budgets and activities",
        note: "Estimated from major foundation budgets and activities",
  },
  "oecd-govt-spending": {
        id: "oecd-govt-spending",
        type: "report",
        title: "OECD Government Spending as Percentage of GDP",
        author: [
          {
            literal: "Organisation for Economic Co-operation and Development"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        publisher: "OECD",
        URL: "https://data.oecd.org/gga/general-government-spending.htm",
        note: "OECD, 2024, General Government Spending",
  },
  "oecd-median-income": {
        id: "oecd-median-income",
        type: "report",
        title: "OECD Median Household Income Comparison",
        author: [
          {
            literal: "Organisation for Economic Co-operation and Development"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        publisher: "OECD",
        URL: "https://data.oecd.org/hha/household-disposable-income.htm",
        note: "OECD, 2024, Household Disposable Income",
  },
  "olson1996": {
        id: "olson1996",
        type: "article-journal",
        title: "Big Bills Left on the Sidewalk: Why Some Nations are Rich, and Others Poor",
        author: [
          {
            family: "Olson",
            given: "Mancur"
          },
        ],
        issued: { 'date-parts': [[1996]] },
        'container-title': "Journal of Economic Perspectives",
        URL: "https://pubs.aeaweb.org/doi/pdfplus/10.1257/jep.10.2.3",
  },
  "opensecrets-lobbying-2024": {
        id: "opensecrets-lobbying-2024",
        type: "report",
        title: "Federal Lobbying Hit Record $4.4 Billion in 2024",
        author: [
          {
            literal: "OpenSecrets"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        publisher: "OpenSecrets",
        URL: "https://www.opensecrets.org/news/2025/02/federal-lobbying-set-new-record-in-2024/",
        note: "OpenSecrets, Federal Lobbying Set New Record in 2024",
  },
  "opensecrets-revolving-door": {
        id: "opensecrets-revolving-door",
        type: "report",
        title: "Revolving Door: Former Members of Congress",
        author: [
          {
            literal: "OpenSecrets"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        publisher: "OpenSecrets",
        URL: "https://www.opensecrets.org/revolving-door",
        note: "OpenSecrets, Revolving Door",
  },
  "papanicolas2018": {
        id: "papanicolas2018",
        type: "article-journal",
        title: "Health Care Spending in the United States and Other High-Income Countries",
        author: [
          {
            family: "Papanicolas",
            given: "Irene et al."
          },
        ],
        issued: { 'date-parts': [[2018]] },
        'container-title': "Papanicolas et al.",
        URL: "https://jamanetwork.com/journals/jama/article-abstract/2674671",
        note: "Papanicolas et al., 2018, JAMA | Highly cited comparison of healthcare spending across OECD countries",
  },
  "patient-willingness-clinical-trials": {
        id: "patient-willingness-clinical-trials",
        type: "article-journal",
        title: "Patient willingness to participate in clinical trials",
        author: [
          {
            literal: "Trials"
          },
        ],
        'container-title': "Trials: Patients' Willingness Survey",
        URL: "https://trialsjournal.biomedcentral.com/articles/10.1186/s13063-015-1105-3",
        note: "Trials: Patients' Willingness Survey | Applied Clinical Trials: Patient Participation | PMC: Study Design Factors",
  },
  "pharma-drug-revenue-average": {
        id: "pharma-drug-revenue-average",
        type: "article-journal",
        title: "Average lifetime revenue per successful drug",
        author: [
          {
            literal: "Value in Health"
          },
        ],
        'container-title': "Value in Health: Sales Revenues for New Therapeutic Agents02754-2/fulltext)",
        URL: "https://www.valueinhealthjournal.com/article/S1098-3015(24",
        note: "Value in Health: Sales Revenues for New Therapeutic Agents02754-2/fulltext) | ScienceDirect: Sales Revenues FDA Drugs",
  },
  "pharma-roi-current": {
        id: "pharma-roi-current",
        type: "article-journal",
        title: "Pharmaceutical R&D return on investment (ROI)",
        author: [
          {
            literal: "Deloitte"
          },
        ],
        issued: { 'date-parts': [[2025]] },
        'container-title': "Deloitte: Measuring Pharmaceutical Innovation 2025",
        URL: "https://www.deloitte.com/ch/en/Industries/life-sciences-health-care/research/measuring-return-from-pharmaceutical-innovation.html",
        note: "Deloitte: Measuring Pharmaceutical Innovation 2025 | Deloitte 2023: Pharma R&D ROI Falls | HIT Consultant: 13-Year Low",
  },
  "phase-3-cost-per-trial-range": {
        id: "phase-3-cost-per-trial-range",
        type: "article-journal",
        title: "Phase 3 cost per trial range",
        author: [
          {
            literal: "SofproMed"
          },
        ],
        'container-title': "SofproMed",
        URL: "https://www.sofpromed.com/how-much-does-a-clinical-trial-cost",
        note: "SofproMed, How Much Does a Clinical Trial Cost | CBO, Research and Development in the Pharmaceutical Industry",
  },
  "pmc-pragmatic-trial-cost": {
        id: "pmc-pragmatic-trial-cost",
        type: "article-journal",
        title: "Pragmatic Trial Cost per Patient (Median $97)",
        author: [
          {
            literal: "PMC"
          },
        ],
        'container-title': "PMC: Costs of Pragmatic Clinical Trials",
        URL: "https://pmc.ncbi.nlm.nih.gov/articles/PMC6508852/",
        note: "PMC: Costs of Pragmatic Clinical Trials",
  },
  "polio-vaccination-roi": {
        id: "polio-vaccination-roi",
        type: "article-journal",
        title: "Polio Vaccination ROI",
        author: [
          {
            literal: "WHO"
          },
        ],
        issued: { 'date-parts': [[2019]] },
        'container-title': "WHO",
        URL: "https://www.who.int/news-room/feature-stories/detail/sustaining-polio-investments-offers-a-high-return",
        note: "WHO, 2019, Sustaining Polio Investments Offers a High Return",
  },
  "posen2014": {
        id: "posen2014",
        type: "book",
        title: "Restraint: A New Foundation for U.S. Grand Strategy",
        author: [
          {
            family: "Posen",
            given: "Barry R."
          },
        ],
        issued: { 'date-parts': [[2014]] },
        publisher: "Posen",
        URL: "https://www.cornellpress.cornell.edu/book/9780801452581/restraint/",
        note: "Posen, Barry R., 2014, Restraint | See also: Preble, Christopher (Cato), \"The Power Problem\" | Defense economics literature on deterrence sufficiency",
  },
  "post-1962-drug-approval-drop": {
        id: "post-1962-drug-approval-drop",
        type: "article-journal",
        title: "Post-1962 drop in new drug approvals",
        author: [
          {
            literal: "Think by Numbers"
          },
        ],
        'container-title': "Think by Numbers: How Many Lives Does FDA Save?",
        URL: "https://thinkbynumbers.org/health/how-many-net-lives-does-the-fda-save/",
        note: "Think by Numbers: How Many Lives Does FDA Save? | Wikipedia: Kefauver-Harris Amendment | PMC: Lost Medicines",
  },
  "post-1962-life-expectancy-slowdown": {
        id: "post-1962-life-expectancy-slowdown",
        type: "webpage",
        title: "Post-1962 slowdown in life expectancy gains",
        author: [
          {
            literal: "Source: US Life Expectancy FDA Budget 1543-2019 CSV"
          },
        ],
        issued: { 'date-parts': [[2019]] },
        publisher: "Source: US Life Expectancy FDA Budget 1543-2019 CSV",
        URL: "knowledge/data/us-life-expectancy-fda-budget-1543-2019.csv",
        note: "Source: US Life Expectancy FDA Budget 1543-2019 CSV | Our World in Data: Life Expectancy | Primary sources: Human Mortality Database (historical), CDC NCHS National Vital Statistics (modern)",
  },
  "pragmatic-trials-cost-advantage": {
        id: "pragmatic-trials-cost-advantage",
        type: "article-journal",
        title: "NIH Pragmatic Trials: Minimal Funding Despite 30x Cost Advantage",
        author: [
          {
            literal: "NIH Common Fund"
          },
        ],
        issued: { 'date-parts': [[2025]] },
        'container-title': "NIH Common Fund: HCS Research Collaboratory",
        URL: "https://commonfund.nih.gov/hcscollaboratory",
        note: "NIH Common Fund: HCS Research Collaboratory | PCORnet ADAPTABLE Summary | PMC: Pragmatic Clinical Trials in Healthcare Systems",
  },
  "pre-1962-drug-costs-baily-1972": {
        id: "pre-1962-drug-costs-baily-1972",
        type: "article-journal",
        title: "Pre-1962 drug development costs (Baily 1972)",
        author: [
          {
            family: "Baily",
            given: "Martin Neil"
          },
        ],
        issued: { 'date-parts': [[1972]] },
        'container-title': "Baily (1972)",
        URL: "https://samizdathealth.org/wp-content/uploads/2020/12/hlthaff.1.2.6.pdf",
        note: "Baily (1972), \"Research and Development Costs and Returns: The U.S. Pharmaceutical Industry,\" cited in Health Affairs 1982, The Importance of Patent Term Restoration",
  },
  "pre-1962-drug-costs-timeline": {
        id: "pre-1962-drug-costs-timeline",
        type: "article-journal",
        title: "Pre-1962 drug development costs and timeline (Think by Numbers)",
        author: [
          {
            literal: "Think by Numbers"
          },
        ],
        issued: { 'date-parts': [[1962]] },
        'container-title': "Think by Numbers: How Many Lives Does FDA Save?",
        URL: "https://thinkbynumbers.org/health/how-many-net-lives-does-the-fda-save/",
        note: "Think by Numbers: How Many Lives Does FDA Save? | Wikipedia: Cost of Drug Development | STAT: 1962 Law Slowed Development",
  },
  "pre-1962-physician-trials": {
        id: "pre-1962-physician-trials",
        type: "article-journal",
        title: "Pre-1962 physician-led clinical trials",
        author: [
          {
            literal: "Think by Numbers"
          },
        ],
        issued: { 'date-parts': [[1966]] },
        'container-title': "Think by Numbers: How Many Lives Does FDA Save?",
        URL: "https://thinkbynumbers.org/health/how-many-net-lives-does-the-fda-save/",
        note: "Think by Numbers: How Many Lives Does FDA Save? | FDA: Drug Efficacy Study Implementation | NAS: Drug Efficacy Study 1966-1969",
  },
  "psychological-impact-war-cost": {
        id: "psychological-impact-war-cost",
        type: "article-journal",
        title: "Psychological impact of war cost (\\$100B annually)",
        author: [
          {
            literal: "PubMed"
          },
        ],
        'container-title': "PubMed: Economic Burden of PTSD",
        URL: "https://pubmed.ncbi.nlm.nih.gov/35485933/",
        note: "PubMed: Economic Burden of PTSD | VA News: Study Economic Burden | PMC: Mental Health Costs Armed Conflicts",
  },
  "qaly-value": {
        id: "qaly-value",
        type: "article-journal",
        title: "Value per QALY (standard economic value)",
        author: [
          {
            literal: "ICER"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "ICER",
        URL: "https://icer.org/wp-content/uploads/2024/02/Reference-Case-4.3.25.pdf",
        note: "ICER, Reference Case",
  },
  "rare-disease-only-5pct-have-treatment": {
        id: "rare-disease-only-5pct-have-treatment",
        type: "article-journal",
        title: "Rare Disease Treatment Gap",
        author: [
          {
            literal: "Orphanet Journal of Rare Diseases (2024)"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "Orphanet Journal of Rare Diseases (2024)",
        URL: "https://ojrd.biomedcentral.com/articles/10.1186/s13023-024-03398-1",
        note: "Orphanet Journal of Rare Diseases (2024)",
  },
  "recovery-cost-500": {
        id: "recovery-cost-500",
        type: "article-journal",
        title: "RECOVERY Trial Cost per Patient",
        author: [
          {
            family: "Oren Cass",
            given: "Manhattan Institute"
          },
        ],
        issued: { 'date-parts': [[2023]] },
        'container-title': "Oren Cass",
        URL: "https://manhattan.institute/article/slow-costly-clinical-trials-drag-down-biomedical-breakthroughs",
        note: "Oren Cass, Manhattan Institute, 2023, Slow, Costly Clinical Trials Drag Down Biomedical Breakthroughs",
  },
  "recovery-trial-1m-lives-saved": {
        id: "recovery-trial-1m-lives-saved",
        type: "article-journal",
        title: "RECOVERY trial global lives saved (~1 million)",
        author: [
          {
            literal: "NHS England; Águas et al."
          },
        ],
        issued: { 'date-parts': [[2021]] },
        'container-title': "NHS England: 1 Million Lives Saved",
        URL: "https://www.england.nhs.uk/2021/03/covid-treatment-developed-in-the-nhs-saves-a-million-lives/",
        note: "NHS England: 1 Million Lives Saved | Águas et al. Nature Communications 2021 | Pharmaceutical Journal | RECOVERY Trial",
  },
  "recovery-trial-82x-cost-reduction": {
        id: "recovery-trial-82x-cost-reduction",
        type: "article-journal",
        title: "RECOVERY trial 82× cost reduction",
        author: [
          {
            literal: "Manhattan Institute"
          },
        ],
        'container-title': "Manhattan Institute: Slow Costly Trials",
        URL: "https://manhattan.institute/article/slow-costly-clinical-trials-drag-down-biomedical-breakthroughs",
        note: "Manhattan Institute: Slow Costly Trials | PMC: Establishing RECOVERY at Scale",
  },
  "sipri2024": {
        id: "sipri2024",
        type: "report",
        title: "Trends in World Military Expenditure, 2023",
        author: [
          {
            literal: "Stockholm International Peace Research Institute"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        URL: "https://www.sipri.org/publications/2024/sipri-fact-sheets/trends-world-military-expenditure-2023",
  },
  "smallpox-eradication-roi": {
        id: "smallpox-eradication-roi",
        type: "article-journal",
        title: "Smallpox Eradication ROI",
        author: [
          {
            literal: "CSIS"
          },
        ],
        'container-title': "CSIS",
        URL: "https://www.csis.org/analysis/smallpox-eradication-model-global-cooperation",
        note: "CSIS, Smallpox Eradication Model: Global Cooperation | PMC3720047, Link",
  },
  "standard-medical-research-roi": {
        id: "standard-medical-research-roi",
        type: "article-journal",
        title: "Standard Medical Research ROI ($20k-$100k/QALY)",
        author: [
          {
            literal: "PMC"
          },
        ],
        issued: { 'date-parts': [[1990]] },
        'container-title': "PMC: Cost-effectiveness Thresholds Used by Study Authors",
        URL: "https://pmc.ncbi.nlm.nih.gov/articles/PMC10114019/",
        note: "PMC: Cost-effectiveness Thresholds Used by Study Authors, 1990-2021 | ICER Cost-Effectiveness Methods",
  },
  "status-quo-cure-timeline-estimate": {
        id: "status-quo-cure-timeline-estimate",
        type: "webpage",
        title: "Average Time to Cure Under Current System",
        author: [
          {
            literal: "Composite estimate based on Orphanet"
          },
        ],
        publisher: "Composite estimate based on Orphanet",
        note: "Composite estimate based on Orphanet, FDA approval data, and queue theory",
  },
  "sugar-subsidies-cost": {
        id: "sugar-subsidies-cost",
        type: "article-journal",
        title: "Annual cost of U.S. sugar subsidies",
        author: [
          {
            literal: "GAO"
          },
        ],
        'container-title': "GAO: Sugar Program",
        URL: "https://www.gao.gov/products/gao-24-106144",
        note: "GAO: Sugar Program | Heritage: US Sugar Program | AEI: $4B Sugar Subsidies",
  },
  "swiss-military-budget-0-7-pct-gdp": {
        id: "swiss-military-budget-0-7-pct-gdp",
        type: "article-journal",
        title: "Swiss military budget as percentage of GDP",
        author: [
          {
            literal: "World Bank"
          },
        ],
        'container-title': "World Bank: Military Expenditure % GDP Switzerland",
        URL: "https://data.worldbank.org/indicator/MS.MIL.XPND.GD.ZS?locations=CH",
        note: "World Bank: Military Expenditure % GDP Switzerland | Avenir Suisse: Defense Spending | Trading Economics: Switzerland Military Expenditure",
  },
  "swiss-vs-us-gdp-per-capita": {
        id: "swiss-vs-us-gdp-per-capita",
        type: "article-journal",
        title: "Switzerland vs. US GDP per capita comparison",
        author: [
          {
            literal: "World Bank"
          },
        ],
        'container-title': "World Bank: Switzerland GDP Per Capita",
        URL: "https://data.worldbank.org/indicator/NY.GDP.PCAP.CD?locations=CH",
        note: "World Bank: Switzerland GDP Per Capita | Trading Economics: Switzerland GDP Per Capita PPP | TheGlobalEconomy: USA GDP Per Capita PPP",
  },
  "taxfoundation2024-compliance": {
        id: "taxfoundation2024-compliance",
        type: "article-journal",
        title: "Tax Compliance Costs the US Economy $546 Billion Annually",
        author: [
          {
            literal: "Tax Foundation"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        URL: "https://taxfoundation.org/data/all/federal/irs-tax-compliance-costs/",
  },
  "thalidomide-scandal": {
        id: "thalidomide-scandal",
        type: "article-journal",
        title: "Thalidomide scandal: worldwide cases and mortality",
        author: [
          {
            literal: "Wikipedia"
          },
        ],
        'container-title': "Wikipedia",
        URL: "https://en.wikipedia.org/wiki/Thalidomide_scandal",
        note: "Wikipedia, Thalidomide scandal",
  },
  "thalidomide-survivors-health": {
        id: "thalidomide-survivors-health",
        type: "article-journal",
        title: "Health and quality of life of Thalidomide survivors as they age",
        author: [
          {
            literal: "PLOS One"
          },
        ],
        issued: { 'date-parts': [[2019]] },
        'container-title': "PLOS One",
        URL: "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0210222",
        note: "PLOS One, 2019, The health and quality of life of Thalidomide survivors as they age",
  },
  "transit-costs-project": {
        id: "transit-costs-project",
        type: "article-journal",
        title: "Transit Costs Project - Why US Infrastructure Costs So Much",
        author: [
          {
            family: "Marron Institute",
            given: "NYU"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "NYU Transit Costs Project",
        URL: "https://transitcosts.com/",
        note: "NYU Transit Costs Project, TransitCosts.com | Brookings Institution, Why Does Infrastructure Cost So Much?",
  },
  "trial-costs-fda-study": {
        id: "trial-costs-fda-study",
        type: "article-journal",
        title: "Trial Costs, FDA Study",
        author: [
          {
            literal: "FDA Study via NCBI"
          },
        ],
        'container-title': "FDA Study via NCBI",
        URL: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6248200/",
        note: "FDA Study via NCBI, Link",
  },
  "ucdp-state-violence-deaths": {
        id: "ucdp-state-violence-deaths",
        type: "article-journal",
        title: "State violence deaths annually",
        author: [
          {
            literal: "UCDP"
          },
        ],
        'container-title': "UCDP: Uppsala Conflict Data Program",
        URL: "https://ucdp.uu.se/",
        note: "UCDP: Uppsala Conflict Data Program | Wikipedia: UCDP | Our World in Data: Armed Conflict Deaths",
  },
  "unhcr-refugee-support-cost": {
        id: "unhcr-refugee-support-cost",
        type: "article-journal",
        title: "UNHCR average refugee support cost",
        author: [
          {
            literal: "CGDev"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "CGDev",
        URL: "https://www.cgdev.org/blog/costs-hosting-refugees-oecd-countries-and-why-uk-outlier",
        note: "CGDev, Costs of Hosting Refugees in OECD Countries | UNHCR/World Bank, Global Cost of Refugee Inclusion",
  },
  "unpaid-caregiver-hours-economic-value": {
        id: "unpaid-caregiver-hours-economic-value",
        type: "article-journal",
        title: "Unpaid caregiver hours and economic value",
        author: [
          {
            literal: "AARP"
          },
        ],
        issued: { 'date-parts': [[2023]] },
        'container-title': "AARP 2023",
        URL: "https://www.aarp.org/caregiving/financial-legal/info-2023/unpaid-caregivers-provide-billions-in-care.html",
        note: "AARP 2023, Unpaid Care Report | Bureau of Labor Statistics 2023-2024, Unpaid Eldercare | National Alliance for Caregiving, Caregiver Statistics",
  },
  "us-census-world-population-1960": {
        id: "us-census-world-population-1960",
        type: "article-journal",
        title: "Historical world population estimates",
        author: [
          {
            literal: "US Census Bureau"
          },
        ],
        'container-title': "US Census Bureau",
        URL: "https://www.census.gov/data/tables/time-series/demo/international-programs/historical-est-worldpop.html",
        note: "US Census Bureau, Historical Estimates of World Population",
  },
  "us-chronic-disease-spending": {
        id: "us-chronic-disease-spending",
        type: "article-journal",
        title: "U.S. chronic disease healthcare spending",
        author: [
          {
            literal: "CDC"
          },
        ],
        'container-title': "CDC",
        URL: "https://www.cdc.gov/chronic-disease/data-research/facts-stats/index.html",
        note: "CDC, Chronic Disease Data",
  },
  "us-military-budget-3-5-pct-gdp": {
        id: "us-military-budget-3-5-pct-gdp",
        type: "article-journal",
        title: "US military budget as percentage of GDP",
        author: [
          {
            literal: "Statista"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "Statista",
        URL: "https://www.statista.com/statistics/262742/countries-with-the-highest-military-spending/",
        note: "Statista, Military spending as percent of GDP | SIPRI, Trends in World Military Expenditure 2024",
  },
  "us-post-wwii-military-spending-cut": {
        id: "us-post-wwii-military-spending-cut",
        type: "article-journal",
        title: "US military spending reduction after WWII",
        author: [
          {
            literal: "Wikipedia"
          },
        ],
        issued: { 'date-parts': [[2020]] },
        'container-title': "Wikipedia",
        URL: "https://en.wikipedia.org/wiki/Demobilization_of_United_States_Armed_Forces_after_World_War_II",
        note: "Wikipedia, Demobilization After WWII | American Progress, Historical Perspective on Defense Budgets | St. Louis Fed, Which War Saw the Highest Defense Spending? | US Government Spending, Defense Spending History",
  },
  "us-senate-treaties": {
        id: "us-senate-treaties",
        type: "article-journal",
        title: "Treaties",
        author: [
          {
            literal: "U.S. Senate"
          },
        ],
        'container-title': "U.S. Senate",
        URL: "https://www.senate.gov/about/powers-procedures/treaties.htm",
        note: "U.S. Senate, Treaties",
  },
  "us-voter-population": {
        id: "us-voter-population",
        type: "article-journal",
        title: "Number of registered or eligible voters in the U.S.",
        author: [
          {
            literal: "US Census Bureau"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "US Census Bureau",
        URL: "https://www.census.gov/newsroom/press-releases/2025/2024-presidential-election-voting-registration-tables.html",
        note: "US Census Bureau, 2024 Voting and Registration | US EAC, 2024 Election Survey Report",
  },
  "valley-of-death-attrition": {
        id: "valley-of-death-attrition",
        type: "webpage",
        title: "Valley of Death in Drug Development",
        author: [
          {
            literal: "Hutchinson & Kirk (2011)"
          },
        ],
        issued: { 'date-parts': [[2011]] },
        publisher: "Hutchinson & Kirk (2011)",
        URL: "https://pmc.ncbi.nlm.nih.gov/articles/PMC3324971/",
        note: "Hutchinson & Kirk (2011), Drug Discov Today; conservative estimate 40% abandoned due to cost",
  },
  "vera-incarceration2024": {
        id: "vera-incarceration2024",
        type: "article-journal",
        title: "The Economic Burden of Incarceration in the United States",
        author: [
          {
            literal: "Vera Institute of Justice"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "Vera Institute",
        URL: "https://www.vera.org/publications/the-economic-burden-of-incarceration-in-the-u-s",
        note: "Vera Institute, Economic Burden of Incarceration | Prison Policy Initiative, Mass Incarceration: The Whole Pie | RAND Corporation, Evidence on Drug Courts",
  },
  "veteran-healthcare-cost-projections": {
        id: "veteran-healthcare-cost-projections",
        type: "article-journal",
        title: "Veteran healthcare cost projections",
        author: [
          {
            literal: "VA"
          },
        ],
        issued: { 'date-parts': [[2026]] },
        'container-title': "VA",
        URL: "https://department.va.gov/wp-content/uploads/2025/06/2026-Budget-in-Brief.pdf",
        note: "VA, FY 2026 Budget Submission | CBO, Veterans' Disability Compensation | American Legion, VA budget tops $400B for 2025",
  },
  "vitamin-a-cost-per-daly": {
        id: "vitamin-a-cost-per-daly",
        type: "article-journal",
        title: "Cost per DALY for Vitamin A Supplementation",
        author: [
          {
            literal: "PLOS ONE"
          },
        ],
        issued: { 'date-parts': [[2010]] },
        'container-title': "PLOS ONE: Cost-effectiveness of \"Golden Mustard\" for Treating Vitamin A Deficiency in India (2010)",
        URL: "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0012046",
        note: "PLOS ONE: Cost-effectiveness of \"Golden Mustard\" for Treating Vitamin A Deficiency in India (2010) | PLOS ONE: Cost-effectiveness of Vitamin A supplementation in Sub-Saharan Africa (2022)",
  },
  "warren-buffett-career-average-return-20-pct": {
        id: "warren-buffett-career-average-return-20-pct",
        type: "article-journal",
        title: "Warren Buffett's career average investment return",
        author: [
          {
            literal: "CNBC"
          },
        ],
        issued: { 'date-parts': [[2025]] },
        'container-title': "CNBC",
        URL: "https://www.cnbc.com/2025/05/05/warren-buffetts-return-tally-after-60-years-5502284percent.html",
        note: "CNBC, Warren Buffett's return tally after 60 years: 5,502,284% | SlickCharts, Berkshire Hathaway Returns by Year",
  },
  "who-cost-effectiveness-threshold": {
        id: "who-cost-effectiveness-threshold",
        type: "article-journal",
        title: "Cost-effectiveness threshold ($50,000/QALY)",
        author: [
          {
            literal: "PMC"
          },
        ],
        'container-title': "PMC",
        URL: "https://pmc.ncbi.nlm.nih.gov/articles/PMC5193154/",
        note: "PMC, Country-Level Cost-Effectiveness Thresholds | WHO, WHO-CHOICE Methods Update",
  },
  "who-global-health-estimates-2024": {
        id: "who-global-health-estimates-2024",
        type: "article-journal",
        title: "WHO Global Health Estimates 2024",
        author: [
          {
            literal: "World Health Organization"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "World Health Organization",
        URL: "https://www.who.int/data/gho/data/themes/mortality-and-global-health-estimates",
        note: "World Health Organization, 2024, Global Health Estimates: Life expectancy and leading causes of death and disability",
  },
  "who-life-expectancy": {
        id: "who-life-expectancy",
        type: "report",
        title: "WHO Life Expectancy Data by Country",
        author: [
          {
            literal: "World Health Organization"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        publisher: "WHO",
        URL: "https://www.who.int/data/gho/data/themes/mortality-and-global-health-estimates/ghe-life-expectancy-and-healthy-life-expectancy",
        note: "WHO, 2024, Life Expectancy",
  },
  "world-bank-trade-disruption-conflict": {
        id: "world-bank-trade-disruption-conflict",
        type: "article-journal",
        title: "World Bank trade disruption cost from conflict",
        author: [
          {
            literal: "World Bank"
          },
        ],
        'container-title': "World Bank",
        URL: "https://www.worldbank.org/en/topic/trade/publication/trading-away-from-conflict",
        note: "World Bank, Trading Away from Conflict | NBER/World Bank, Collateral Damage: Trade Disruption | World Bank, Impacts on Global Trade of Current Trade Disputes",
  },
  "worldbank-gdp": {
        id: "worldbank-gdp",
        type: "article-journal",
        title: "US GDP 2024 ($28.78 trillion)",
        author: [
          {
            family: "World Bank",
            given: "Bureau of Economic Analysis"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "World Bank",
        URL: "https://data.worldbank.org/indicator/NY.GDP.MKTP.CD?locations=US",
        note: "World Bank, GDP (current US$) - United States | Bureau of Economic Analysis, GDP and the Economy",
  },
  "worldbank-singapore-gdp": {
        id: "worldbank-singapore-gdp",
        type: "article-journal",
        title: "World Bank Singapore Economic Data",
        author: [
          {
            literal: "World Bank"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "World Bank",
        URL: "https://data.worldbank.org/country/singapore",
        note: "World Bank, Singapore Data",
  },
  "yalebudgetlab2025": {
        id: "yalebudgetlab2025",
        type: "report",
        title: "The Fiscal, Economic, and Distributional Effects of All U.S. Tariffs",
        author: [
          {
            literal: "Yale Budget Lab"
          },
        ],
        issued: { 'date-parts': [[2025]] },
        URL: "https://budgetlab.yale.edu/research/where-we-stand-fiscal-economic-and-distributional-effects-all-us-tariffs-enacted-2025-through-april",
  }
};

/** Summary statistics */
export const PARAMETER_STATS = {
  total: 445,
  external: 182,
  calculated: 147,
  definitions: 116,
  citations: 140,
} as const;

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Get citation for a parameter by its sourceRef
 * 
 * Example:
 *   const citation = getCitation(ANTIDEPRESSANT_TRIAL_EXCLUSION_RATE);
 *   console.log(formatCitation(citation, 'apa'));
 */
export function getCitation(param: Parameter): Citation | undefined {
  if (!param.sourceRef) return undefined;
  return citations[param.sourceRef];
}

/**
 * Format parameter value with appropriate unit formatting
 */
export function formatValue(param: Parameter): string {
  const { value, unit } = param;

  // Currency formatting
  if (unit === 'USD') {
    if (Math.abs(value) >= 1_000_000_000_000) {
      return `$${(value / 1_000_000_000_000).toFixed(2)}T`;
    } else if (Math.abs(value) >= 1_000_000_000) {
      return `$${(value / 1_000_000_000).toFixed(2)}B`;
    } else if (Math.abs(value) >= 1_000_000) {
      return `$${(value / 1_000_000).toFixed(2)}M`;
    } else if (Math.abs(value) >= 1_000) {
      return `$${(value / 1_000).toFixed(2)}K`;
    } else {
      return `$${value.toLocaleString()}`;
    }
  }

  // Percentage formatting
  if (unit === 'percentage') {
    return `${(value * 100).toFixed(1)}%`;
  }

  if (unit === 'rate') {
    return `${(value * 100).toFixed(1)}%`;
  }

  // Large numbers (deaths, DALYs, etc.)
  if (Math.abs(value) >= 1_000_000_000) {
    return `${(value / 1_000_000_000).toFixed(2)}B${unit ? ' ' + unit : ''}`;
  } else if (Math.abs(value) >= 1_000_000) {
    return `${(value / 1_000_000).toFixed(2)}M${unit ? ' ' + unit : ''}`;
  } else if (Math.abs(value) >= 1_000) {
    return `${value.toLocaleString()}${unit ? ' ' + unit : ''}`;
  }

  return `${value}${unit ? ' ' + unit : ''}`;
}

/**
 * Format citation in APA or MLA style
 */
export function formatCitation(
  citation: Citation | undefined,
  style: 'apa' | 'mla' = 'apa'
): string {
  if (!citation) return '';

  const author = citation.author?.[0]?.literal ||
                 (citation.author?.[0]?.family
                   ? `${citation.author[0].family}, ${citation.author[0].given || ''}`
                   : 'Unknown Author');
  const year = citation.issued?.['date-parts']?.[0]?.[0] || 'n.d.';
  const title = citation.title;

  if (style === 'apa') {
    // APA: Author (Year). Title. URL
    let result = `${author} (${year}). ${title}.`;
    if (citation.URL) result += ` ${citation.URL}`;
    return result;
  } else {
    // MLA: Author. "Title." Year. URL
    let result = `${author}. "${title}." ${year}.`;
    if (citation.URL) result += ` ${citation.URL}`;
    return result;
  }
}
