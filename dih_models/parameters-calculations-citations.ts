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

export const DRUG_DEVELOPMENT_COST_1980S: Parameter = {
  value: 194000000.0,
  unit: "USD",
  displayName: "Drug Development Cost (1980s)",
  description: "Drug development cost in 1980s (compounded to approval, 1990 dollars)",
  sourceType: "external",
  sourceRef: "pre-1962-drug-costs-timeline",
  confidence: "high",
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
  description: "Regulatory delay for efficacy testing (Phase II/III) post-safety verification",
  sourceType: "external",
  sourceRef: "bio-clinical-development-2021",
  confidence: "high",
  formula: "TOTAL_TIME_TO_MARKET - PHASE_1_DURATION",
  latex: "t_{lag} = 10.5 - 2.3 = 8.2 \\text{ years}",
  stdError: 1.0,
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

export const GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES: Parameter = {
  value: 55000000.0,
  unit: "deaths/year",
  displayName: "Annual Deaths from Curable Diseases Globally",
  description: "Annual deaths from all diseases and aging globally",
  sourceType: "external",
  sourceRef: "who-global-health-estimates-2024",
  confidence: "high",
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
  value: 83000000000.0,
  unit: "USD",
  displayName: "Annual Global Spending on Clinical Trials",
  description: "Annual global spending on clinical trials (Total: Government + Industry)",
  sourceType: "external",
  sourceRef: "global-clinical-trials-market-2024",
  confidence: "high",
  confidenceInterval: [60000000000.0, 110000000000.0],
  stdError: 12500000000.0,
};

export const GLOBAL_DAILY_DEATHS_CURABLE_DISEASES: Parameter = {
  value: 150000.0,
  unit: "deaths/day",
  displayName: "Daily Deaths from Curable Diseases Globally",
  description: "Daily deaths from all diseases and aging globally",
  sourceType: "external",
  sourceRef: "who-daily-deaths",
  confidence: "high",
  confidenceInterval: [120000.0, 180000.0],
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
  value: 2718000000000.0,
  unit: "USD",
  displayName: "Global Military Spending in 2024",
  description: "Global military spending in 2024",
  sourceType: "external",
  sourceRef: "global-military-spending",
  confidence: "high",
  confidenceInterval: [2446000000000.0, 2990000000000.0],
  stdError: 271800000000.0,
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

export const PHASE_3_TRIAL_COST_MIN: Parameter = {
  value: 20000000.0,
  unit: "USD/trial",
  displayName: "Phase 3 Trial Total Cost (Minimum)",
  description: "Phase 3 trial total cost (minimum)",
  sourceType: "external",
  sourceRef: "phase-3-cost-per-trial-range",
  confidence: "high",
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

export const POLITICAL_SUCCESS_PROBABILITY: Parameter = {
  value: 0.01,
  unit: "rate",
  displayName: "Political Success Probability",
  description: "Estimated probability of treaty ratification and sustained implementation. Central estimate 1% is ultra-conservative. This assumes 99% chance of failure. ",
  sourceType: "external",
  sourceRef: "icbl-ottawa-treaty",
  confidence: "low",
  confidenceInterval: [0.001, 0.1],
  stdError: 0.02,
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

export const PRE_1962_DRUG_DEVELOPMENT_COST: Parameter = {
  value: 50000000.0,
  unit: "USD",
  displayName: "Pre-1962 Drug Development Cost",
  description: "Pre-1962 drug development cost (documented range: $10-50M in 1950s-1960s)",
  sourceType: "external",
  sourceRef: "pre-1962-drug-costs-timeline",
  confidence: "medium",
  confidenceInterval: [10000000.0, 50000000.0],
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
};

export const RECOVERY_TRIAL_COST_PER_PATIENT: Parameter = {
  value: 500.0,
  unit: "USD/patient",
  displayName: "Recovery Trial Cost per Patient",
  description: "RECOVERY trial cost per patient",
  sourceType: "external",
  sourceRef: "recovery-cost-500",
  confidence: "high",
  confidenceInterval: [350.0, 700.0],
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
  value: 80000.0,
  unit: "USD/patient",
  displayName: "Phase 3 Cost per Patient",
  description: "Phase 3 cost per patient (median)",
  sourceType: "external",
  sourceRef: "phase-3-cost-per-patient-113k",
  confidence: "high",
};

export const TRADITIONAL_PHASE3_COST_PER_PATIENT_EXAMPLE_48K: Parameter = {
  value: 48000.0,
  unit: "USD/patient",
  displayName: "Example Phase 3 Trial Cost per Patient",
  description: "Example Phase 3 trial cost per patient ($48K)",
  sourceType: "external",
  sourceRef: "clinical-trial-cost-per-patient",
  confidence: "high",
};

export const TRADITIONAL_PHASE3_COST_PER_PATIENT_FDA_EXAMPLE_41K: Parameter = {
  value: 41000.0,
  unit: "USD/patient",
  displayName: "FDA Cited Phase 3 Cost per Patient",
  description: "FDA cited Phase 3 cost per patient ($41K)",
  sourceType: "external",
  sourceRef: "trial-costs-fda-study",
  confidence: "high",
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

export const TRIAL_COST_REDUCTION_FACTOR: Parameter = {
  value: 82.0,
  unit: "ratio",
  displayName: "Cost Reduction Factor Demonstrated by Recovery Trial",
  description: "Cost reduction factor demonstrated by RECOVERY trial",
  sourceType: "external",
  sourceRef: "recovery-trial-82x-cost-reduction",
  confidence: "high",
  confidenceInterval: [20.0, 150.0],
  stdError: 20.0,
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

export const COMBINED_PEACE_HEALTH_DIVIDENDS_ANNUAL_FOR_ROI_CALC: Parameter = {
  value: 155051000000.0,
  unit: "USD/year",
  displayName: "Combined Peace and Health Dividends for ROI Calculation",
  description: "Combined peace and health dividends for ROI calculation",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/peace-dividend-calculations#peace-dividend-composition",
  confidence: "high",
  formula: "PEACE_DIVIDEND + R&D_SAVINGS",
};

export const DFDA_ANNUAL_OPEX: Parameter = {
  value: 40000000.0,
  unit: "USD/year",
  displayName: "Total Annual Decentralized Framework for Drug Assessment Operational Costs",
  description: "Total annual Decentralized Framework for Drug Assessment operational costs (sum of all components: $15M + $10M + $8M + $5M + $2M)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#opex-breakdown",
  confidence: "high",
  formula: "PLATFORM_MAINTENANCE + STAFF + INFRASTRUCTURE + REGULATORY + COMMUNITY",
  latex: "OPEX_{total} = \\$15M \\text{ (plat)} + \\$10M \\text{ (staff)} + \\$8M \\text{ (infra)} + \\$5M \\text{ (reg)} + \\$2M \\text{ (comm)} = \\$40M",
};

export const DFDA_BENEFIT_RD_ONLY_ANNUAL: Parameter = {
  value: 41500000000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Annual Benefit: R&D Savings",
  description: "Annual Decentralized Framework for Drug Assessment benefit from R&D savings (trial cost reduction, secondary component)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#cost-reduction",
  confidence: "high",
  formula: "TRIAL_SPENDING × COST_REDUCTION_PCT",
};

export const DFDA_EXPECTED_ROI: Parameter = {
  value: 11914.175356950002,
  displayName: "Expected Treaty ROI (Risk-Adjusted)",
  description: "Expected ROI for 1% treaty accounting for political success probability uncertainty. Monte Carlo samples POLITICAL_SUCCESS_PROBABILITY from beta(0.1%, 10%) distribution to generate full expected value distribution. Central value uses 1% probability.",
  sourceType: "calculated",
  sourceRef: "calculated",
  confidence: "low",
  formula: "TREATY_ROI_LAG_ELIMINATION × POLITICAL_SUCCESS_PROBABILITY",
  latex: "E[ROI] = ROI_{conditional} \\times P_{success} = ROI_{treaty} \\times 0.01",
};

export const DFDA_NET_SAVINGS_RD_ONLY_ANNUAL: Parameter = {
  value: 41460000000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Annual Net Savings (R&D Only)",
  description: "Annual net savings from R&D cost reduction only (gross savings minus operational costs, excludes regulatory delay value)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#net-savings",
  confidence: "high",
  formula: "GROSS_SAVINGS - ANNUAL_OPEX",
  latex: "Savings_{net} = \\$41.5B - \\$0.04B = \\$41.46B",
};

export const DFDA_NPV_ANNUAL_OPEX_TOTAL: Parameter = {
  value: 40050000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Total NPV Annual OPEX",
  description: "Total NPV annual opex (Decentralized Framework for Drug Assessment core + DIH initiatives)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#npv-costs",
  confidence: "high",
  formula: "DFDA_OPEX + DIH_OPEX",
  latex: "C_{op} = \\$0.01895B + \\$0.02110B = \\$0.04005B \\text{ (annual operational cost)}",
};

export const DFDA_NPV_BENEFIT_RD_ONLY: Parameter = {
  value: 275468208149.5121,
  unit: "USD",
  displayName: "NPV of Decentralized Framework for Drug Assessment Benefits (R&D Only, 10-Year Discounted)",
  description: "NPV of Decentralized Framework for Drug Assessment R&D savings only with 5-year adoption ramp (10-year horizon, most conservative financial estimate)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#npv-benefit",
  confidence: "high",
  formula: "Sum of discounted annual net R&D savings with linear adoption ramp",
  latex: "PV_{benefits} = \\sum_{t=1}^{10} \\frac{NetSavings_{RD} \\times \\min(t,5)/5}{(1+r)^t} \\approx \\$249.3B \\text{ (5-year linear adoption ramp)}",
};

export const DFDA_NPV_NET_BENEFIT_RD_ONLY: Parameter = {
  value: 275468208149.5121,
  unit: "USD",
  displayName: "NPV Net Benefit (R&D Only, Conservative)",
  description: "NPV net benefit using R&D savings only (most conservative financial estimate, excludes regulatory delay health value)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#npv-net-benefit",
  confidence: "high",
  formula: "NPV of net R&D savings with 5-year linear adoption ramp",
  latex: "Benefit_{NPV} = \\sum_{t=1}^{10} \\frac{NetSavings_{RD} \\times \\min(t,5)/5}{(1+r)^t} \\approx \\$249.3B \\text{ (5-year linear adoption ramp)}",
};

export const DFDA_NPV_PV_ANNUAL_OPEX: Parameter = {
  value: 341634623.61287224,
  unit: "USD",
  displayName: "Decentralized Framework for Drug Assessment Present Value of Annual OPEX Over 10 Years",
  description: "Present value of annual opex over 10 years (NPV formula)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#npv-calculation",
  confidence: "high",
  formula: "OPEX × [(1 - (1 + r)^-T) / r]",
  latex: "PV_{opex} = \\$0.04005B \\times \\frac{1 - 1.08^{-10}}{0.08} \\approx \\$0.269B",
};

export const DFDA_NPV_TOTAL_COST: Parameter = {
  value: 611384623.6128722,
  unit: "USD",
  displayName: "Decentralized Framework for Drug Assessment Total NPV Cost",
  description: "Total NPV cost (upfront + PV of annual opex)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#npv-total-cost",
  confidence: "high",
  formula: "UPFRONT + PV_OPEX",
  latex: "TotalCost_{NPV} = \\$0.26975B + \\$0.269B \\approx \\$0.54B",
};

export const DFDA_NPV_UPFRONT_COST_TOTAL: Parameter = {
  value: 269750000.0,
  unit: "USD",
  displayName: "Decentralized Framework for Drug Assessment Total NPV Upfront Costs",
  description: "Total NPV upfront costs (Decentralized Framework for Drug Assessment core + DIH initiatives)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#npv-costs",
  confidence: "high",
  formula: "DFDA_BUILD + DIH_INITIATIVES",
  latex: "C_0 = \\$0.040B + \\$0.22975B = \\$0.26975B \\text{ (upfront cost)}",
};

export const DFDA_RD_GROSS_SAVINGS_ANNUAL: Parameter = {
  value: 41500000000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Annual Benefit: R&D Savings",
  description: "Annual Decentralized Framework for Drug Assessment benefit from R&D savings (trial cost reduction, secondary component)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#cost-reduction",
  confidence: "high",
  formula: "TRIAL_SPENDING × COST_REDUCTION_PCT",
};

export const DFDA_RD_SAVINGS_DAILY: Parameter = {
  value: 113698630.1369863,
  unit: "USD/day",
  displayName: "Daily R&D Savings from Trial Cost Reduction",
  description: "Daily R&D savings from trial cost reduction (opportunity cost of delay)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#daily-opportunity-cost-of-inaction",
  confidence: "high",
  formula: "ANNUAL_RD_SAVINGS ÷ DAYS_PER_YEAR",
  latex: "Savings_{daily} = \\frac{\\$41.5B}{365} = \\$113.7M",
};

export const DFDA_ROI_RD_ONLY: Parameter = {
  value: 450.5645014781041,
  unit: "ratio",
  displayName: "ROI from Decentralized Framework for Drug Assessment R&D Savings Only",
  description: "ROI from Decentralized Framework for Drug Assessment R&D savings only (10-year NPV, most conservative estimate)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#roi-simple",
  confidence: "high",
  formula: "NPV_BENEFIT ÷ NPV_TOTAL_COST",
  latex: "ROI_{RD} = \\frac{\\$249.3B}{\\$0.54B} \\approx 463",
};

export const DFDA_ROI_SIMPLE: Parameter = {
  value: 1037.5,
  unit: "ratio",
  displayName: "Decentralized Framework for Drug Assessment Simple ROI Without NPV Adjustment",
  description: "Simple ROI without NPV adjustment (gross savings / annual opex)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#roi-simple",
  confidence: "high",
  formula: "GROSS_SAVINGS ÷ ANNUAL_OPEX",
};

export const DFDA_TRIALS_PER_YEAR_CAPACITY: Parameter = {
  value: 75392.0,
  unit: "trials/year",
  displayName: "Decentralized Framework for Drug Assessment Maximum Trials per Year",
  description: "Maximum trials per year possible with trial capacity multiplier",
  sourceType: "calculated",
  confidence: "high",
  formula: "CURRENT_TRIALS × TRIAL_CAPACITY_MULTIPLIER",
};

export const DIH_PATIENTS_FUNDABLE_ANNUALLY: Parameter = {
  value: 43408000.0,
  unit: "patients/year",
  displayName: "Patients Fundable Annually",
  description: "Number of patients fundable annually at RECOVERY trial cost",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/economics#funding-allocation",
  confidence: "high",
  formula: "TRIAL_SUBSIDIES ÷ COST_PER_PATIENT",
};

export const DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL: Parameter = {
  value: 21744000000.0,
  unit: "USD/year",
  displayName: "DIH Annual Funding for Pragmatic Clinical Trials",
  description: "Annual funding for pragmatic clinical trials (treaty funding minus VICTORY Bond payouts and IAB political incentive mechanism)",
  sourceType: "calculated",
  confidence: "high",
  formula: "TREATY_FUNDING - BOND_PAYOUT - IAB_POLITICAL_INCENTIVE_FUNDING",
  latex: "ResearchFunding = \\$27.18B - \\$2.718B - \\$2.718B = \\$21.744B",
};

export const DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL: Parameter = {
  value: 21704000000.0,
  unit: "USD/year",
  displayName: "Annual Clinical Trial Patient Subsidies",
  description: "Annual clinical trial patient subsidies (all medical research funds after Decentralized Framework for Drug Assessment operations)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/economics#funding-allocation",
  confidence: "high",
  formula: "MEDICAL_RESEARCH_FUNDING - DFDA_OPEX",
  latex: "TrialSubsidies = \\$24.462B - \\$0.04B = \\$24.422B",
};

export const DISEASE_ERADICATION_DELAY_DALYS: Parameter = {
  value: 7942783571.3,
  unit: "DALYs",
  displayName: "Total DALYs Lost from Disease Eradication Delay",
  description: "Total Disability-Adjusted Life Years lost from disease eradication delay (PRIMARY estimate)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/regulatory-mortality-analysis#daly-calculation",
  confidence: "medium",
  formula: "YLL + YLD",
  latex: "DALY_{total} = 7.03B \\text{ (YLL)} + 0.87B \\text{ (YLD)} = 7.90B",
};

export const DISEASE_ERADICATION_DELAY_DEATHS_TOTAL: Parameter = {
  value: 415852543.0,
  unit: "deaths",
  displayName: "Total Deaths from Disease Eradication Delay",
  description: "Total eventually avoidable deaths from delaying disease eradication by 8.2 years (PRIMARY estimate, conservative). Excludes fundamentally unavoidable deaths (primarily accidents ~7.9%).",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/regulatory-mortality-analysis#disease-eradication-delay",
  confidence: "medium",
  formula: "ANNUAL_DEATHS × EFFICACY_LAG_YEARS × EVENTUALLY_AVOIDABLE_DEATH_PCT",
  latex: "D_{total} = 54.75M \\text{ (annual)} \\times 8.2 \\text{ (lag)} \\times 92.1\\% \\text{ (avoidable)} = 413.4M",
};

export const DISEASE_ERADICATION_DELAY_ECONOMIC_LOSS: Parameter = {
  value: 1191417535695000.0,
  unit: "USD",
  displayName: "Total Economic Loss from Disease Eradication Delay",
  description: "Total economic loss from delaying disease eradication by 8.2 years (PRIMARY estimate, 2024 USD). Values global DALYs at standardized US/International normative rate ($150k) rather than local ability-to-pay, representing the full human capital loss.",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/regulatory-mortality-analysis#economic-valuation",
  confidence: "medium",
  formula: "DALYS_TOTAL × VSLY",
  latex: "Loss = 7.90B \\times \\$150k = \\$1.185\\text{ quadrillion}",
};

export const DISEASE_ERADICATION_DELAY_YLD: Parameter = {
  value: 873290340.3,
  unit: "years",
  displayName: "Years Lived with Disability During Disease Eradication Delay",
  description: "Years Lived with Disability during disease eradication delay (PRIMARY estimate)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/regulatory-mortality-analysis#daly-calculation",
  confidence: "medium",
  formula: "DEATHS_TOTAL × SUFFERING_PERIOD × DISABILITY_WEIGHT",
};

export const DISEASE_ERADICATION_DELAY_YLL: Parameter = {
  value: 7069493231.0,
  unit: "years",
  displayName: "Years of Life Lost from Disease Eradication Delay",
  description: "Years of Life Lost from disease eradication delay deaths (PRIMARY estimate)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/regulatory-mortality-analysis#daly-calculation",
  confidence: "medium",
  formula: "DEATHS_TOTAL × (LIFE_EXPECTANCY - MEAN_AGE_OF_DEATH)",
  latex: "YLL = 413.4M \\times 17 \\text{ (years lost)} = 7.03B",
};

export const DISEASE_ERADICATION_PLUS_ACCELERATION_DEATHS_TOTAL: Parameter = {
  value: 897899999.9999999,
  unit: "deaths",
  displayName: "Total Deaths from Disease Eradication + Innovation Acceleration",
  description: "Total deaths from disease eradication delay plus innovation acceleration (OPTIMISTIC UPPER BOUND). Represents additional deaths avoided beyond lag elimination through innovation cascade effects: faster development cycles, lower barriers enabling more drugs, earlier phase starts. The 2× multiplier is supported by research showing 50% timeline reductions achievable (Nature 2023) and adaptive trials generating millions of additional life-years (Woods et al. 2024). Based on (150K daily × 365 × 2) × 8.2 years.",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/references#pharmaceutical-innovation-acceleration-economics",
  confidence: "low",
  formula: "(ANNUAL_DEATHS × 2) × EFFICACY_LAG_YEARS",
  latex: "D_{total} = (54.75M \\times 2) \\times 8.2 = 898M",
};

export const DISEASE_ERADICATION_PLUS_ACCELERATION_ECONOMIC_LOSS_TOTAL: Parameter = {
  value: 2382835071390000.0,
  unit: "USD",
  displayName: "Total Economic Loss from Disease Eradication + Innovation Acceleration",
  description: "Total economic loss from disease eradication delay plus innovation acceleration (OPTIMISTIC UPPER BOUND). The 2× multiplier represents combined timeline and volume effects from eliminating Phase 2-4 cost barriers. Research shows: (1) Timeline acceleration of 50% achievable through AI/tech (Nature 2023), (2) Adaptive trials can reduce costs $2.6B→$2.2B, generating 3.5M additional life-years (Woods et al. 2024, Health Economics), (3) Cost barrier elimination enables more drugs to reach viability. The 2× factor conservatively represents either 2× timeline acceleration OR 1.5× timeline × 1.33× volume. Dynamic efficiency framework suggests optimal manufacturer value share ~20% maximizes long-term population health (Woods 2024).",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/references#pharmaceutical-innovation-acceleration-economics",
  confidence: "low",
  formula: "PRIMARY_TOTAL × 2 (combined timeline + volume effects)",
  latex: "Loss_{total} = \\$1,286T \\times 2 = \\$2,572T",
};

export const DIVIDEND_COVERAGE_FACTOR: Parameter = {
  value: 679.5,
  unit: "ratio",
  displayName: "Coverage Factor of Treaty Funding vs Decentralized Framework for Drug Assessment OPEX",
  description: "Coverage factor of treaty funding vs Decentralized Framework for Drug Assessment opex (sustainability margin)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/strategy/roadmap#sustainability",
  confidence: "high",
  formula: "TREATY_FUNDING ÷ DFDA_OPEX",
  latex: "Coverage = \\$27.18B / \\$0.04B = 679x",
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
};

export const DRUG_COST_INCREASE_PRE1962_TO_CURRENT_MULTIPLIER: Parameter = {
  value: 52.0,
  unit: "ratio",
  displayName: "Drug Cost Increase: Pre-1962 to Current",
  description: "Drug development cost increase from pre-1962 to current ($50M → $2.6B = 52x)",
  sourceType: "calculated",
  sourceRef: "pre-1962-drug-costs-timeline",
  confidence: "medium",
  formula: "PHARMA_DRUG_DEVELOPMENT_COST_CURRENT ÷ PRE_1962_DRUG_DEVELOPMENT_COST",
};

export const DRUG_DISEASE_COMBINATIONS_POSSIBLE: Parameter = {
  value: 9500000.0,
  unit: "combinations",
  displayName: "Possible Drug-Disease Combinations",
  description: "Total possible drug-disease combinations using existing safe compounds",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  formula: "SAFE_COMPOUNDS × DISEASES",
  latex: "N_{combinations} = N_{compounds} \\times N_{diseases} = 9{,}500 \\times 1{,}000 = 9{,}500{,}000",
};

export const EXPLORATION_RATIO: Parameter = {
  value: 0.0034210526315789475,
  unit: "percentage",
  displayName: "Therapeutic Frontier Exploration Ratio",
  description: "Fraction of possible drug-disease space actually tested (<1%)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  formula: "TESTED / POSSIBLE",
  latex: "\\text{Exploration Ratio} = \\frac{N_{tested}}{N_{possible}} = \\frac{32{,}500}{9{,}500{,}000} = 0.342\\%",
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
  latex: "\\frac{9.1 \\text{ years} \\times 12 \\text{ months/year}}{3 \\text{ months}} = 36.4",
};

export const GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL: Parameter = {
  value: 244600.0,
  unit: "deaths/year",
  displayName: "Total Annual Conflict Deaths Globally",
  description: "Total annual conflict deaths globally (sum of combat, terror, state violence)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#death-accounting",
  confidence: "high",
  formula: "COMBAT + TERROR + STATE_VIOLENCE",
  latex: "Deaths_{total} = 233,600 \\text{ (combat)} + 8,300 \\text{ (terror)} + 2,700 \\text{ (state)} = 244,600",
};

export const GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT: Parameter = {
  value: 2336000000000.0,
  unit: "USD/year",
  displayName: "Annual Cost of Combat Deaths",
  description: "Annual cost of combat deaths (deaths × VSL)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#human-cost",
  confidence: "high",
  formula: "COMBAT_DEATHS × VSL ",
};

export const GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE: Parameter = {
  value: 27000000000.0,
  unit: "USD/year",
  displayName: "Annual Cost of State Violence Deaths",
  description: "Annual cost of state violence deaths (deaths × VSL)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#human-cost",
  confidence: "high",
  formula: "STATE_DEATHS × VSL ",
};

export const GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS: Parameter = {
  value: 83000000000.0,
  unit: "USD/year",
  displayName: "Annual Cost of Terror Deaths",
  description: "Annual cost of terror deaths (deaths × VSL)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#human-cost",
  confidence: "high",
  formula: "TERROR_DEATHS × VSL ",
};

export const GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT: Parameter = {
  value: 2446000000000.0,
  unit: "USD/year",
  displayName: "Total Annual Human Life Losses from Conflict",
  description: "Total annual human life losses from conflict (sum of combat, terror, state violence)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#human-cost",
  confidence: "high",
  formula: "COMBAT_COST + TERROR_COST + STATE_VIOLENCE_COST",
  latex: "Cost_{human} = \\$2,336B \\text{ (combat)} + \\$83B \\text{ (terror)} + \\$27B \\text{ (state)} = \\$2,446B",
};

export const GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT: Parameter = {
  value: 1875000000000.0,
  unit: "USD/year",
  displayName: "Total Annual Infrastructure Destruction",
  description: "Total annual infrastructure destruction (sum of transportation, energy, communications, water, education, healthcare)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#infrastructure-damage",
  confidence: "high",
  formula: "TRANSPORT + ENERGY + COMMS + WATER + EDUCATION + HEALTHCARE",
  latex: "Infra_{damage} = \\$487B \\text{ (trans)} + \\$422B \\text{ (nrg)} + \\$298B \\text{ (comms)} + \\$268B \\text{ (water)} + \\$235B \\text{ (edu)} + \\$166B \\text{ (hlth)} = \\$1,875B",
};

export const GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT: Parameter = {
  value: 616000000000.0,
  unit: "USD/year",
  displayName: "Total Annual Trade Disruption",
  description: "Total annual trade disruption (sum of shipping, supply chain, energy prices, currency instability)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#trade-disruption",
  confidence: "high",
  formula: "SHIPPING + SUPPLY_CHAIN + ENERGY_PRICE + CURRENCY",
  latex: "Trade_{disruption} = \\$247B \\text{ (ship)} + \\$187B \\text{ (supply)} + \\$125B \\text{ (nrg)} + \\$57B \\text{ (curr)} = \\$616B",
};

export const GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL: Parameter = {
  value: 7655000000000.0,
  unit: "USD/year",
  displayName: "Total Annual Direct War Costs",
  description: "Total annual direct war costs (military spending + infrastructure + human life + trade disruption)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#direct-costs",
  confidence: "high",
  formula: "MILITARY + INFRASTRUCTURE + HUMAN_LIFE + TRADE",
  latex: "DirectCosts = \\$2,718B \\text{ (mil)} + \\$1,875B \\text{ (infra)} + \\$2,446B \\text{ (human)} + \\$616B \\text{ (trade)} = \\$7,655B",
};

export const GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL: Parameter = {
  value: 3700100000000.0,
  unit: "USD/year",
  displayName: "Total Annual Indirect War Costs",
  description: "Total annual indirect war costs (opportunity cost + veterans + refugees + environment + mental health + lost productivity)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#indirect-costs",
  confidence: "high",
  formula: "OPPORTUNITY + VETERANS + REFUGEES + ENVIRONMENT + MENTAL_HEALTH + LOST_CAPITAL",
  latex: "IndirectCosts = \\$2.7T \\text{ (opp cost)} + \\$200B \\text{ (vet)} + \\$150B \\text{ (ref)} + \\$100B \\text{ (env)} + \\$232B \\text{ (ptsd)} + \\$300B \\text{ (hum cap)} = \\$3.7T",
};

export const GLOBAL_ANNUAL_WAR_TOTAL_COST: Parameter = {
  value: 11355100000000.0,
  unit: "USD/year",
  displayName: "Total Annual Cost of War Worldwide",
  description: "Total annual cost of war worldwide (direct + indirect costs)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#total-cost",
  confidence: "high",
  formula: "DIRECT_COSTS + INDIRECT_COSTS",
  latex: "TotalWarCost = \\$7,655B \\text{ (direct)} + \\$3,700B \\text{ (indirect)} = \\$11,355B",
};

export const GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL: Parameter = {
  value: 16071.42857142857,
  unit: "USD/life",
  displayName: "Cost per Life Saved by Medical Research",
  description: "Cost per life saved by medical research",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#grotesque-mathematics",
  confidence: "high",
  formula: "(RESEARCH_SPENDING × 1B) ÷ LIVES_SAVED",
  latex: "CostPerLifeSaved = \\frac{\\$67.5B \\times 10^9}{4,200,000} \\approx \\$16,071",
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
};

export const GLOBAL_INDUSTRY_CLINICAL_TRIALS_SPENDING_ANNUAL: Parameter = {
  value: 78500000000.0,
  unit: "USD",
  displayName: "Annual Global Industry Spending on Clinical Trials",
  description: "Annual global industry spending on clinical trials (Total - Government)",
  sourceType: "calculated",
  confidence: "high",
  formula: "TOTAL_CLINICAL_TRIALS - GOVT_CLINICAL_TRIALS",
};

export const GLOBAL_MILITARY_SPENDING_PER_CAPITA_ANNUAL: Parameter = {
  value: 339.75,
  unit: "USD/person/year",
  displayName: "Per Capita Military Spending Globally",
  description: "Per capita military spending globally",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#per-capita",
  confidence: "high",
  formula: "MILITARY_SPENDING ÷ POPULATION",
  latex: "PerCapita_{military} = \\$2,718B / 8.0B = \\$339.75",
};

export const GLOBAL_MILITARY_SPENDING_POST_TREATY_ANNUAL_2024: Parameter = {
  value: 2690820000000.0,
  unit: "USD/year",
  displayName: "Global Military Spending After 1% Treaty Reduction",
  description: "Global military spending after 1% treaty reduction",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/strategy/treaty-adoption-strategy#post-treaty",
  confidence: "high",
  formula: "MILITARY_SPENDING × (1 - REDUCTION)",
  latex: "PostTreaty_{military} = \\$2,718B \\times 0.99 = \\$2,690.82B",
};

export const GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL: Parameter = {
  value: 128655100000000.0,
  unit: "USD/year",
  displayName: "Total Annual Cost of War and Disease with All Externalities",
  description: "Total annual cost of war and disease with all externalities (direct + indirect costs for both)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/humanity-budget-overview",
  confidence: "high",
  formula: "WAR_TOTAL_COSTS + SYMPTOMATIC_TREATMENT + DISEASE_BURDEN",
};

export const HISTORICAL_PROGRESS_DEATHS_TOTAL: Parameter = {
  value: 98399999.99999999,
  unit: "deaths",
  displayName: "Total Deaths from Historical Progress Delays",
  description: "Total deaths from delaying existing drugs over 8.2-year efficacy lag (CONSERVATIVE FLOOR). One-time impact of eliminating Phase 2-4 testing delay for drugs already approved 1962-2024. Based on 12M deaths/year rate × 8.2 years.",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/regulatory-mortality-analysis#historical-progress",
  confidence: "high",
  formula: "12M × EFFICACY_LAG_YEARS",
  latex: "D_{total} = 12M \\times 8.2 = 98.4M",
};

export const HISTORICAL_PROGRESS_ECONOMIC_LOSS_TOTAL: Parameter = {
  value: 250919999999999.97,
  unit: "USD",
  displayName: "Total Economic Loss from Historical Progress Delays",
  description: "Total economic loss from delaying existing drugs over 8.2-year efficacy lag (CONSERVATIVE FLOOR). One-time benefit of eliminating Phase 2-4 delay.",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/regulatory-mortality-analysis#historical-progress",
  confidence: "high",
  formula: "DEATHS_TOTAL × YLL × VSLY",
  latex: "Loss_{total} = 98.4M \\times 17 \\times \\$150k = \\$251T",
};

export const IAB_MECHANISM_BENEFIT_COST_RATIO: Parameter = {
  value: 206.73466666666667,
  unit: "ratio",
  displayName: "IAB Mechanism Benefit-Cost Ratio",
  description: "Benefit-Cost Ratio of the IAB mechanism itself",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/incentive-alignment-bonds-paper#welfare-analysis",
  confidence: "high",
  formula: "TREATY_PEACE_PLUS_RD_BENEFITS ÷ IAB_MECHANISM_COST",
};

export const IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL: Parameter = {
  value: 2718000000.0,
  unit: "USD/year",
  displayName: "Annual IAB Political Incentive Funding",
  description: "Annual funding for IAB political incentive mechanism (independent expenditures supporting high-scoring politicians, post-office fellowship endowments, Public Good Score infrastructure)",
  sourceType: "calculated",
  confidence: "high",
  formula: "TREATY_FUNDING × IAB_POLITICAL_INCENTIVE_PCT",
  latex: "IABFunding = \\$27.18B \\times 0.10 = \\$2.718B",
};

export const INDUSTRY_VS_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO: Parameter = {
  value: 17.444444444444443,
  unit: "ratio",
  displayName: "Ratio of Industry to Government Clinical Trials Spending",
  description: "Ratio of Industry to Government spending on clinical trials (approx 90/10 split)",
  sourceType: "calculated",
  sourceRef: "industry-vs-government-trial-spending-split",
  confidence: "high",
  formula: "(TOTAL - GOVT) / GOVT",
};

export const MEDICAL_RESEARCH_PCT_OF_DISEASE_BURDEN: Parameter = {
  value: 0.0005246585638657154,
  unit: "rate",
  displayName: "Medical Research Spending as Percentage of Total Disease Burden",
  description: "Medical research spending as percentage of total disease burden",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/economics",
  confidence: "high",
  formula: "MED_RESEARCH ÷ TOTAL_BURDEN",
  latex: "\\frac{\\$67.5\\text{B}}{\\$128.6\\text{T}} = 0.052\\%",
};

export const MILITARY_TO_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO: Parameter = {
  value: 604.0,
  unit: "ratio",
  displayName: "Ratio of Military to Government Clinical Trials Spending",
  description: "Ratio of global military spending to government clinical trials spending",
  sourceType: "calculated",
  confidence: "high",
  formula: "MILITARY_SPENDING / GOVT_CLINICAL_TRIALS_SPENDING",
  latex: "\\text{Ratio} = \\frac{\\$2.7T}{\\$4.5B} \\approx 600\\times",
};

export const MILITARY_VS_MEDICAL_RESEARCH_RATIO: Parameter = {
  value: 40.266666666666666,
  unit: "ratio",
  displayName: "Ratio of Military Spending to Medical Research Spending",
  description: "Ratio of military spending to medical research spending",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#misallocation",
  confidence: "high",
  formula: "MILITARY_SPENDING ÷ MEDICAL_RESEARCH",
  latex: "Ratio = \\frac{\\$2,718B}{\\$67.5B} \\approx 40.3:1",
};

export const MISALLOCATION_FACTOR_DEATH_VS_SAVING: Parameter = {
  value: 2888.550922140456,
  unit: "ratio",
  displayName: "Misallocation Factor: Cost to Kill vs Cost to Save",
  description: "Misallocation factor: cost to kill vs cost to save",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/cost-of-war#grotesque-mathematics",
  confidence: "high",
  formula: "COST_PER_DEATH ÷ COST_PER_LIFE_SAVED",
  latex: "Misallocation = \\frac{\\$46.4M}{\\$16,071} \\approx 2,889x",
};

export const PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT: Parameter = {
  value: 113551000000.0,
  unit: "USD/year",
  displayName: "Annual Peace Dividend from 1% Reduction in Total War Costs",
  description: "Annual peace dividend from 1% reduction in total war costs",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/peace-dividend-calculations",
  confidence: "high",
  formula: "TOTAL_WAR_COST × 1%",
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
  latex: "PeaceDividend_{conflict} = \\$113.55B - \\$27.18B = \\$86.37B",
};

export const PEACE_DIVIDEND_DIRECT_COSTS: Parameter = {
  value: 76550000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Direct War Costs",
  description: "Annual savings from 1% reduction in direct war costs",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "DIRECT_COSTS × 1%",
};

export const PEACE_DIVIDEND_ENVIRONMENTAL: Parameter = {
  value: 1000000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Environmental Damage",
  description: "Annual savings from 1% reduction in environmental damage",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "ENVIRONMENTAL_DAMAGE × 1%",
};

export const PEACE_DIVIDEND_HUMAN_CASUALTIES: Parameter = {
  value: 24460000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Human Casualties",
  description: "Annual savings from 1% reduction in human casualties",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "HUMAN_LIFE_LOSSES × 1%",
};

export const PEACE_DIVIDEND_INDIRECT_COSTS: Parameter = {
  value: 37001000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Indirect War Costs",
  description: "Annual savings from 1% reduction in indirect war costs",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "INDIRECT_COSTS × 1%",
};

export const PEACE_DIVIDEND_INFRASTRUCTURE: Parameter = {
  value: 18750000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Infrastructure Destruction",
  description: "Annual savings from 1% reduction in infrastructure destruction",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "INFRASTRUCTURE_DESTRUCTION × 1%",
};

export const PEACE_DIVIDEND_LOST_ECONOMIC_GROWTH: Parameter = {
  value: 27180000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Lost Economic Growth",
  description: "Annual savings from 1% reduction in lost economic growth",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "LOST_ECONOMIC_GROWTH × 1%",
};

export const PEACE_DIVIDEND_LOST_HUMAN_CAPITAL: Parameter = {
  value: 3000000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Lost Human Capital",
  description: "Annual savings from 1% reduction in lost human capital",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "LOST_HUMAN_CAPITAL × 1%",
};

export const PEACE_DIVIDEND_PTSD: Parameter = {
  value: 2320000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in PTSD and Mental Health Costs",
  description: "Annual savings from 1% reduction in PTSD and mental health costs",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "PTSD_COSTS × 1%",
};

export const PEACE_DIVIDEND_REFUGEE_SUPPORT: Parameter = {
  value: 1500000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Refugee Support Costs",
  description: "Annual savings from 1% reduction in refugee support costs",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "REFUGEE_SUPPORT × 1%",
};

export const PEACE_DIVIDEND_TRADE_DISRUPTION: Parameter = {
  value: 6160000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Trade Disruption",
  description: "Annual savings from 1% reduction in trade disruption",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "TRADE_DISRUPTION × 1%",
};

export const PEACE_DIVIDEND_VETERAN_HEALTHCARE: Parameter = {
  value: 2001000000.0,
  unit: "USD/year",
  displayName: "Annual Savings from 1% Reduction in Veteran Healthcare Costs",
  description: "Annual savings from 1% reduction in veteran healthcare costs",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/peace-dividend",
  confidence: "high",
  formula: "VETERAN_HEALTHCARE × 1%",
};

export const PERSONAL_LIFETIME_WEALTH: Parameter = {
  value: 507984.80978508206,
  unit: "usd",
  displayName: "Personal Lifetime Wealth (Age 30, 1% Treaty)",
  description: "Personal lifetime wealth benefit for a 30-year-old with $50K income under 1% treaty. Life extension uncertainty (5-50 years) propagates through Monte Carlo to show full range of outcomes from conservative antibiotic precedent to optimistic aging reversal scenarios.",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/disease-eradication-personal-lifetime-wealth-calculations",
  confidence: "medium",
  formula: "NPV(peace_dividend + healthcare_savings + productivity_gains + caregiver_savings + gdp_boost + extended_earnings)",
  latex: "\\text{PLW} = \\sum_{t=0}^{T + \\Delta L} \\frac{B_t}{(1+r)^t}",
};

export const PER_CAPITA_CHRONIC_DISEASE_COST: Parameter = {
  value: 12238.805970149253,
  unit: "USD/person/year",
  displayName: "US Per Capita Chronic Disease Cost",
  description: "US per capita chronic disease cost",
  sourceType: "calculated",
  confidence: "high",
  formula: "US_CHRONIC_DISEASE_SPENDING ÷ US_POPULATION",
};

export const PER_CAPITA_MENTAL_HEALTH_COST: Parameter = {
  value: 1044.7761194029852,
  unit: "USD/person/year",
  displayName: "US Per Capita Mental Health Cost",
  description: "US per capita mental health cost",
  sourceType: "calculated",
  confidence: "high",
  formula: "US_MENTAL_HEALTH_COST ÷ US_POPULATION",
};

export const SUFFERING_HOURS_ELIMINATED_TOTAL: Parameter = {
  value: 7650023381028.0,
  unit: "hours",
  displayName: "Total Suffering Hours Eliminated",
  description: "Total hours of human suffering eliminated by 8.2-year disease eradication timeline shift (one-time benefit from YLD component, not annual recurring)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/regulatory-mortality-analysis#daly-calculation",
  confidence: "medium",
  formula: "YLD × HOURS_PER_YEAR",
  latex: "Hours = 868M \\text{ (YLD)} \\times 8{,}760 \\text{ (hrs/yr)} = 7.60T",
};

export const THALIDOMIDE_DALYS_PER_EVENT: Parameter = {
  value: 41760.0,
  unit: "DALYs",
  displayName: "Thalidomide DALYs Per Event",
  description: "Total DALYs per US-scale thalidomide event (YLL + YLD)",
  sourceType: "calculated",
  confidence: "medium",
  formula: "YLL + YLD",
  latex: "28{,}800 + 12{,}960 = 41{,}760 \\text{ DALYs}",
};

export const THALIDOMIDE_DEATHS_PER_EVENT: Parameter = {
  value: 360.0,
  unit: "deaths",
  displayName: "Thalidomide Deaths Per Event",
  description: "Deaths per US-scale thalidomide event",
  sourceType: "calculated",
  confidence: "medium",
  formula: "US_CASES × MORTALITY_RATE",
  latex: "900 \\text{ (cases)} \\times 40\\% \\text{ (mortality)} = 360 \\text{ deaths}",
};

export const THALIDOMIDE_SURVIVORS_PER_EVENT: Parameter = {
  value: 540.0,
  unit: "cases",
  displayName: "Thalidomide Survivors Per Event",
  description: "Survivors per US-scale thalidomide event",
  sourceType: "calculated",
  confidence: "medium",
  formula: "US_CASES × (1 - MORTALITY_RATE)",
  latex: "900 \\text{ (cases)} \\times 60\\% \\text{ (survival)} = 540 \\text{ survivors}",
};

export const THALIDOMIDE_US_CASES_PREVENTED: Parameter = {
  value: 900.0,
  unit: "cases",
  displayName: "Thalidomide US Cases Prevented",
  description: "Estimated US thalidomide cases prevented by FDA rejection",
  sourceType: "calculated",
  confidence: "medium",
  formula: "WORLDWIDE_CASES × US_POPULATION_SHARE",
  latex: "15{,}000 \\times 6\\% = 900 \\text{ cases}",
};

export const THALIDOMIDE_YLD_PER_EVENT: Parameter = {
  value: 12960.0,
  unit: "years",
  displayName: "Thalidomide YLD Per Event",
  description: "Years Lived with Disability per thalidomide event",
  sourceType: "calculated",
  confidence: "medium",
  formula: "SURVIVORS × LIFESPAN × DISABILITY_WEIGHT",
  latex: "540 \\text{ (surv)} \\times 60 \\text{ (yrs)} \\times 0.4 \\text{ (weight)} = 12{,}960 \\text{ YLD}",
};

export const THALIDOMIDE_YLL_PER_EVENT: Parameter = {
  value: 28800.0,
  unit: "years",
  displayName: "Thalidomide YLL Per Event",
  description: "Years of Life Lost per thalidomide event (infant deaths)",
  sourceType: "calculated",
  confidence: "medium",
  formula: "DEATHS × 80 years",
  latex: "360 \\text{ (deaths)} \\times 80 \\text{ (years)} = 28{,}800 \\text{ YLL}",
};

export const TOTAL_RESEARCH_FUNDING_WITH_TREATY: Parameter = {
  value: 94680000000.0,
  unit: "USD",
  displayName: "Total Global Research Funding (Baseline + 1% treaty Funding)",
  description: "Total global research funding (baseline + 1% treaty funding)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/economics",
  confidence: "high",
  formula: "GLOBAL_MED_RESEARCH_SPENDING + TREATY_ANNUAL_FUNDING",
};

export const TREATY_BENEFIT_MULTIPLIER_VS_VACCINES: Parameter = {
  value: 10.336733333333333,
  unit: "ratio",
  displayName: "Treaty System Benefit Multiplier vs Childhood Vaccination Programs",
  description: "Treaty system benefit multiplier vs childhood vaccination programs",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/economics#better-than-the-best-charities",
  confidence: "high",
  formula: "TREATY_CONSERVATIVE_BENEFIT ÷ CHILDHOOD_VACCINATION_BENEFIT",
};

export const TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED: Parameter = {
  value: 250000000.0,
  unit: "USD/year",
  displayName: "Amortized Annual Treaty Campaign Cost",
  description: "Amortized annual campaign cost (total cost ÷ campaign duration)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/strategy/roadmap#campaign-budget",
  confidence: "high",
  formula: "TOTAL_COST ÷ DURATION",
  latex: "AnnualCost = \\$1B / 4 = \\$0.25B",
};

export const TREATY_CAMPAIGN_TOTAL_COST: Parameter = {
  value: 1000000000.0,
  unit: "USD",
  displayName: "Total 1% Treaty Campaign Cost",
  description: "Total treaty campaign cost (100% VICTORY Incentive Alignment Bonds)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/fundraising-strategy#capital-structure-campaign-vs-implementation",
  confidence: "high",
  formula: "REFERENDUM + LOBBYING + RESERVE",
  latex: "CampaignCost = \\$300M \\text{ (ref)} + \\$650M \\text{ (lob)} + \\$50M \\text{ (res)} = \\$1.0B",
};

export const TREATY_CAMPAIGN_VOTING_BLOC_TARGET: Parameter = {
  value: 280000000.0,
  unit: "of people",
  displayName: "Target Voting Bloc Size for Campaign",
  description: "Target voting bloc size for campaign (3.5% of global population - critical mass for social change)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/strategy/roadmap#voting-bloc",
  confidence: "high",
  formula: "GLOBAL_POPULATION × 3.5%",
};

export const TREATY_COMPLETE_ROI_ALL_BENEFITS: Parameter = {
  value: 1191417.535695,
  unit: "ratio",
  displayName: "Treaty ROI - Lag Elimination (PRIMARY)",
  description: "Treaty ROI based on eliminating the 8.2-year post-safety efficacy lag (PRIMARY METHODOLOGY). Total one-time benefit from disease eradication delay elimination divided by $1B campaign cost. This is the primary ROI estimate for total health benefits.",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/figures/dfda-investment-returns-bar-chart",
  confidence: "medium",
  formula: "DISEASE_ERADICATION_DELAY_TOTAL ÷ CAMPAIGN_COST",
  latex: "ROI_{lag\\_elimination} = \\frac{\\$1{,}286T}{\\$1.00B} = 1{,}286{,}242:1",
};

export const TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT: Parameter = {
  value: 0.12590044674178746,
  unit: "USD/DALY",
  displayName: "Cost per DALY Averted (Timeline Shift)",
  description: "Cost per DALY averted from one-time timeline shift (8.2 years). This is a conservative estimate that only counts campaign cost ($1B) and ignores all economic benefits ($27B/year funding unlocked + $50B/year R&D savings). For comparison: bed nets cost $89.0/DALY, deworming costs $4-10/DALY. This intervention is 700x more cost-effective than bed nets while also being self-funding.",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis",
  confidence: "high",
  formula: "CAMPAIGN_COST ÷ DALYS_TIMELINE_SHIFT",
  latex: "\\text{Cost/DALY} = \\frac{\\$1.0B}{7.90B} = \\$0.127",
};

export const TREATY_EXPECTED_COST_PER_DALY: Parameter = {
  value: 12.590044674178746,
  unit: "USD/DALY",
  displayName: "Expected Cost per DALY (Risk-Adjusted)",
  description: "Expected cost per DALY accounting for political success probability uncertainty. Monte Carlo samples from beta(0.1%, 10%) distribution. At the ultra-conservative 1% estimate, this is still more cost-effective than bed nets ($89.0/DALY).",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis",
  confidence: "low",
  formula: "CONDITIONAL_COST_PER_DALY ÷ POLITICAL_SUCCESS_PROBABILITY",
  latex: "E[\\text{Cost/DALY}] = \\frac{\\text{Cost}_{conditional}}{P_{success}}",
};

export const TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER: Parameter = {
  value: 7.069077378457,
  unit: "ratio",
  displayName: "Expected Cost-Effectiveness vs Bed Nets Multiplier",
  description: "Expected value multiplier vs bed nets (accounts for political uncertainty)",
  sourceType: "calculated",
  confidence: "low",
  formula: "BED_NETS_COST_PER_DALY ÷ TREATY_EXPECTED_COST_PER_DALY",
  latex: "E[\\text{Multiplier}] = \\frac{\\$89}{\\$0.51} = 175\\times",
};

export const TREATY_LIVES_SAVED_ANNUAL_GLOBAL: Parameter = {
  value: 2446.0,
  unit: "lives/year",
  displayName: "Annual Lives Saved from 1% Reduction in Conflict Deaths",
  description: "Annual lives saved from 1% reduction in conflict deaths",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/parameters-and-calculations#sec-treaty_lives_saved_annual_global",
  confidence: "high",
  formula: "TOTAL_DEATHS × REDUCTION_PCT",
};

export const TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS: Parameter = {
  value: 155051000000.0,
  unit: "USD/year",
  displayName: "1% treaty Basic Annual Benefits (Peace + R&D Savings)",
  description: "Basic annual benefits: peace dividend + Decentralized Framework for Drug Assessment R&D savings only (2 of 8 benefit categories, excludes regulatory delay value)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/parameters-and-calculations#sec-treaty_peace_plus_rd_annual_benefits",
  confidence: "high",
  formula: "PEACE_DIVIDEND + DFDA_RD_SAVINGS",
};

export const TREATY_QALYS_GAINED_ANNUAL_GLOBAL: Parameter = {
  value: 85610.0,
  unit: "QALYs/year",
  displayName: "Annual QALYs Gained from Peace Dividend",
  description: "Annual QALYs gained from peace dividend (lives saved × QALYs/life)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/parameters-and-calculations#sec-treaty_qalys_gained_annual_global",
  confidence: "high",
  formula: "LIVES_SAVED × QALYS_PER_LIFE",
};

export const TREATY_RECURRING_BENEFITS_ANNUAL: Parameter = {
  value: 155051000000.0,
  unit: "USD/year",
  displayName: "1% treaty Recurring Annual Benefits",
  description: "Truly recurring annual benefits from 1% treaty: peace dividend ($113.6B/year) + R&D savings ($41.5B/year). Note: Health benefits are one-time timeline shifts, NOT included here.",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/economics",
  confidence: "high",
  formula: "PEACE_DIVIDEND + RD_SAVINGS",
};

export const TREATY_ROI_HISTORICAL_RATE: Parameter = {
  value: 250919.99999999997,
  unit: "ratio",
  displayName: "Treaty ROI - Historical Rate (Conservative Floor)",
  description: "Treaty ROI based on historical rate of drug development (existing drugs only, conservative floor). Total one-time benefit from avoiding regulatory delay for drugs already in development divided by $1B campaign cost.",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/figures/dfda-investment-returns-bar-chart",
  confidence: "high",
  formula: "HISTORICAL_PROGRESS_TOTAL ÷ CAMPAIGN_COST",
};

export const TREATY_ROI_INNOVATION_ACCELERATION: Parameter = {
  value: 2382835.07139,
  unit: "ratio",
  displayName: "Treaty ROI - Innovation Acceleration (Optimistic)",
  description: "Treaty ROI based on lag elimination plus innovation acceleration effects (OPTIMISTIC UPPER BOUND). Includes cascading innovation effects from eliminating Phase 2-4 cost barriers. Research-backed 2× multiplier represents combined timeline and volume effects (Nature 2023, Woods et al. 2024).",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/figures/dfda-investment-returns-bar-chart",
  confidence: "low",
  formula: "DISEASE_ERADICATION_PLUS_ACCELERATION_TOTAL ÷ CAMPAIGN_COST",
};

export const TREATY_ROI_LAG_ELIMINATION: Parameter = {
  value: 1191417.535695,
  unit: "ratio",
  displayName: "Treaty ROI - Lag Elimination (PRIMARY)",
  description: "Treaty ROI based on eliminating the 8.2-year post-safety efficacy lag (PRIMARY METHODOLOGY). Total one-time benefit from disease eradication delay elimination divided by $1B campaign cost. This is the primary ROI estimate for total health benefits.",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/figures/dfda-investment-returns-bar-chart",
  confidence: "medium",
  formula: "DISEASE_ERADICATION_DELAY_TOTAL ÷ CAMPAIGN_COST",
  latex: "ROI_{lag\\_elimination} = \\frac{\\$1{,}286T}{\\$1.00B} = 1{,}286{,}242:1",
};

export const TREATY_TOTAL_ANNUAL_COSTS: Parameter = {
  value: 290000000.0,
  unit: "USD/year",
  displayName: "Total Annual Treaty System Costs",
  description: "Total annual system costs (campaign + Decentralized Framework for Drug Assessment operations)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/parameters-and-calculations#sec-treaty_total_annual_costs",
  confidence: "high",
  formula: "CAMPAIGN_ANNUAL + DFDA_OPEX",
};

export const TREATY_TOTAL_COMPLETE_BENEFITS_ANNUAL: Parameter = {
  value: 155051000000.0,
  unit: "USD/year",
  displayName: "1% treaty Recurring Annual Benefits",
  description: "Truly recurring annual benefits from 1% treaty: peace dividend ($113.6B/year) + R&D savings ($41.5B/year). Note: Health benefits are one-time timeline shifts, NOT included here.",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/economics/economics",
  confidence: "high",
  formula: "PEACE_DIVIDEND + RD_SAVINGS",
};

export const TREATY_VS_BED_NETS_MULTIPLIER: Parameter = {
  value: 706.9077378456999,
  unit: "ratio",
  displayName: "Cost-Effectiveness vs Bed Nets Multiplier",
  description: "How many times more cost-effective than bed nets (using $89/DALY midpoint estimate)",
  sourceType: "calculated",
  confidence: "high",
  formula: "BED_NETS_COST_PER_DALY ÷ TREATY_COST_PER_DALY",
  latex: "\\text{Multiplier} = \\frac{\\$89}{\\$0.127} = 701\\times",
};

export const TRIAL_CAPACITY_CUMULATIVE_YEARS_20YR: Parameter = {
  value: 456.0,
  unit: "years",
  displayName: "Cumulative Trial Capacity Years Over 20 Years",
  description: "Cumulative trial-capacity-equivalent years over 20-year period",
  sourceType: "calculated",
  confidence: "high",
  formula: "TRIAL_CAPACITY_MULTIPLIER × 20 YEARS",
  latex: "Capacity_{20yr} = 25.7 \\times 20 = 514 \\text{ years}",
};

export const TRIAL_CAPACITY_MULTIPLIER: Parameter = {
  value: 22.846315789473685,
  unit: "ratio",
  displayName: "Trial Capacity Multiplier",
  description: "Trial capacity multiplier from DIH funding capacity vs. current global trial participation",
  sourceType: "calculated",
  confidence: "high",
  formula: "DIH_PATIENTS_FUNDABLE ÷ CURRENT_TRIAL_SLOTS",
};

export const TYPE_II_ERROR_COST_RATIO: Parameter = {
  value: 3067.7541293180693,
  unit: "ratio",
  displayName: "Ratio of Type Ii Error Cost to Type I Error Benefit",
  description: "Ratio of Type II error cost to Type I error benefit (harm from delay vs. harm prevented)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/regulatory-mortality-analysis#risk-analysis",
  confidence: "medium",
  formula: "TYPE_II_COST ÷ TYPE_I_BENEFIT",
};

export const TYPE_I_ERROR_BENEFIT_DALYS: Parameter = {
  value: 2589120.0,
  unit: "DALYs",
  displayName: "Maximum DALYs Saved by FDA Preventing Unsafe Drugs (1962-2024)",
  description: "Maximum DALYs saved by FDA preventing unsafe drugs over 62-year period 1962-2024 (extreme overestimate: one Thalidomide-scale event per year)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/regulatory-mortality-analysis#risk-analysis",
  confidence: "low",
  formula: "THALIDOMIDE_DALYS_PER_EVENT × 62 years",
  latex: "41{,}760 \\times 62 = 2.59M \\text{ DALYs}",
};

export const UNEXPLORED_RATIO: Parameter = {
  value: 0.996578947368421,
  unit: "percentage",
  displayName: "Unexplored Therapeutic Frontier",
  description: "Fraction of possible drug-disease space that remains unexplored (>99%)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  formula: "1 - EXPLORATION_RATIO",
  latex: "\\text{Unexplored} = 1 - \\text{Exploration Ratio} = 1 - 0.00342 = 99.66\\%",
};

export const US_MAJOR_DISEASES_TOTAL_ANNUAL_COST: Parameter = {
  value: 1253000000000.0,
  unit: "USD",
  displayName: "US Major Diseases Total Annual Cost",
  description: "Total annual US cost of major diseases (diabetes, Alzheimer's, heart disease, cancer)",
  sourceType: "calculated",
  sourceRef: "https://impact.dih.earth/knowledge/solution/aligning-incentives#insurance-companies",
  confidence: "high",
  formula: "DIABETES + ALZHEIMERS + HEART + CANCER",
};

// ============================================================================
// Core Definitions
// ============================================================================

export const APPROVED_DRUG_DISEASE_PAIRINGS: Parameter = {
  value: 1750.0,
  unit: "pairings",
  displayName: "Approved Drug-Disease Pairings",
  description: "Unique approved drug-disease pairings (FDA-approved uses, midpoint of 1,500-2,000 range)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  confidenceInterval: [1500.0, 2000.0],
};

export const CAMPAIGN_CELEBRITY_ENDORSEMENT: Parameter = {
  value: 15000000.0,
  unit: "USD",
  displayName: "Celebrity and Influencer Endorsements",
  description: "Celebrity and influencer endorsements",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_COMMUNITY_ORGANIZING: Parameter = {
  value: 30000000.0,
  unit: "USD",
  displayName: "Community Organizing and Ambassador Program Budget",
  description: "Community organizing and ambassador program budget",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_CONTINGENCY: Parameter = {
  value: 50000000.0,
  unit: "USD",
  displayName: "Contingency Fund for Unexpected Costs",
  description: "Contingency fund for unexpected costs",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
  confidenceInterval: [30000000.0, 80000000.0],
};

export const CAMPAIGN_DEFENSE_CONVERSION: Parameter = {
  value: 50000000.0,
  unit: "USD",
  displayName: "Defense Industry Conversion Program",
  description: "Defense industry conversion program",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
  confidenceInterval: [40000000.0, 70000000.0],
};

export const CAMPAIGN_DEFENSE_LOBBYIST_BUDGET: Parameter = {
  value: 50000000.0,
  unit: "USD",
  displayName: "Budget for Co-Opting Defense Industry Lobbyists",
  description: "Budget for co-opting defense industry lobbyists",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_HEALTHCARE_ALIGNMENT: Parameter = {
  value: 35000000.0,
  unit: "USD",
  displayName: "Healthcare Industry Alignment and Partnerships",
  description: "Healthcare industry alignment and partnerships",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_INFRASTRUCTURE: Parameter = {
  value: 20000000.0,
  unit: "USD",
  displayName: "Campaign Operational Infrastructure",
  description: "Campaign operational infrastructure",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_LEGAL_AI_BUDGET: Parameter = {
  value: 50000000.0,
  unit: "USD",
  displayName: "AI-Assisted Legal Work Budget",
  description: "AI-assisted legal work budget",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_LEGAL_DEFENSE: Parameter = {
  value: 20000000.0,
  unit: "USD",
  displayName: "Legal Defense Fund",
  description: "Legal defense fund",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_LEGAL_WORK: Parameter = {
  value: 60000000.0,
  unit: "USD",
  displayName: "Legal Drafting and Compliance Work",
  description: "Legal drafting and compliance work",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
  confidenceInterval: [50000000.0, 80000000.0],
};

export const CAMPAIGN_LOBBYING_EU: Parameter = {
  value: 40000000.0,
  unit: "USD",
  displayName: "EU Lobbying Campaign Budget",
  description: "EU lobbying campaign budget",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_LOBBYING_G20_MILLIONS: Parameter = {
  value: 35000000.0,
  unit: "USD",
  displayName: "G20 Countries Lobbying Budget",
  description: "G20 countries lobbying budget",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_LOBBYING_US: Parameter = {
  value: 50000000.0,
  unit: "USD",
  displayName: "US Lobbying Campaign Budget",
  description: "US lobbying campaign budget",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_MEDIA_BUDGET_MAX: Parameter = {
  value: 1000000000.0,
  unit: "USD",
  displayName: "Maximum Mass Media Campaign Budget",
  description: "Maximum mass media campaign budget",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_MEDIA_BUDGET_MIN: Parameter = {
  value: 500000000.0,
  unit: "USD",
  displayName: "Minimum Mass Media Campaign Budget",
  description: "Minimum mass media campaign budget",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_OPPOSITION_RESEARCH: Parameter = {
  value: 25000000.0,
  unit: "USD",
  displayName: "Opposition Research and Rapid Response",
  description: "Opposition research and rapid response",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_PHASE1_BUDGET: Parameter = {
  value: 200000000.0,
  unit: "USD",
  displayName: "Phase 1 Campaign Budget",
  description: "Phase 1 campaign budget (Foundation, Year 1)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_PHASE2_BUDGET: Parameter = {
  value: 500000000.0,
  unit: "USD",
  displayName: "Phase 2 Campaign Budget",
  description: "Phase 2 campaign budget (Scale & Momentum, Years 2-3)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_PILOT_PROGRAMS: Parameter = {
  value: 30000000.0,
  unit: "USD",
  displayName: "Pilot Program Testing in Small Countries",
  description: "Pilot program testing in small countries",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_PLATFORM_DEVELOPMENT: Parameter = {
  value: 35000000.0,
  unit: "USD",
  displayName: "Voting Platform and Technology Development",
  description: "Voting platform and technology development",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
  confidenceInterval: [25000000.0, 50000000.0],
};

export const CAMPAIGN_REGULATORY_NAVIGATION: Parameter = {
  value: 20000000.0,
  unit: "USD",
  displayName: "Regulatory Compliance and Navigation",
  description: "Regulatory compliance and navigation",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_SCALING_PREP: Parameter = {
  value: 30000000.0,
  unit: "USD",
  displayName: "Scaling Preparation and Blueprints",
  description: "Scaling preparation and blueprints",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_STAFF_BUDGET: Parameter = {
  value: 40000000.0,
  unit: "USD",
  displayName: "Campaign Core Team Staff Budget",
  description: "Campaign core team staff budget",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_SUPER_PAC_BUDGET: Parameter = {
  value: 30000000.0,
  unit: "USD",
  displayName: "Super PAC Campaign Expenditures",
  description: "Super PAC campaign expenditures",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_TECH_PARTNERSHIPS: Parameter = {
  value: 25000000.0,
  unit: "USD",
  displayName: "Tech Industry Partnerships and Infrastructure",
  description: "Tech industry partnerships and infrastructure",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAMPAIGN_TREATY_IMPLEMENTATION: Parameter = {
  value: 40000000.0,
  unit: "USD",
  displayName: "Post-Victory Treaty Implementation Support",
  description: "Post-victory treaty implementation support",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
  confidenceInterval: [30000000.0, 55000000.0],
};

export const CAMPAIGN_VIRAL_CONTENT_BUDGET: Parameter = {
  value: 40000000.0,
  unit: "USD",
  displayName: "Viral Marketing Content Creation Budget",
  description: "Viral marketing content creation budget",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget",
  confidence: "high",
};

export const CAREGIVER_COST_ANNUAL: Parameter = {
  value: 6000.0,
  unit: "USD/year",
  displayName: "Annual Cost of Unpaid Caregiving",
  description: "Annual cost of unpaid caregiving (replacement cost method)",
  sourceType: "definition",
  confidence: "high",
  formula: "HOURS_PER_MONTH × MONTHS_PER_YEAR × VALUE_PER_HOUR",
};

export const CHILDHOOD_VACCINATION_COST_PER_DALY: Parameter = {
  value: 30.0,
  unit: "USD/DALY",
  displayName: "Childhood Vaccination Cost per DALY (Estimated)",
  description: "Estimated cost per DALY for US childhood vaccination programs. Note: US cost-effectiveness studies primarily use cost per QALY (Quality-Adjusted Life Year) rather than cost per DALY. This estimate is derived from program costs and benefits for comparison purposes only.",
  sourceType: "definition",
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
  confidence: "high",
  formula: "CURRENT_TRIAL_SLOTS / DISEASE_PATIENTS",
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
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#analogous-rom",
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

export const DFDA_NPV_ADOPTION_RAMP_YEARS: Parameter = {
  value: 5.0,
  unit: "years",
  displayName: "Years to Reach Full Decentralized Framework for Drug Assessment Adoption",
  description: "Years to reach full Decentralized Framework for Drug Assessment adoption",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#adoption-curve",
  confidence: "high",
};

export const DFDA_NPV_ANNUAL_OPEX: Parameter = {
  value: 18950000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Core Platform Annual OPEX",
  description: "Decentralized Framework for Drug Assessment core platform annual opex (midpoint of $11-26.5M)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#npv-costs",
  confidence: "high",
  confidenceInterval: [11000000.0, 26500000.0],
};

export const DFDA_NPV_UPFRONT_COST: Parameter = {
  value: 40000000.0,
  unit: "USD",
  displayName: "Decentralized Framework for Drug Assessment Core Platform Build Cost",
  description: "Decentralized Framework for Drug Assessment core platform build cost",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#npv-costs",
  confidence: "high",
  confidenceInterval: [25000000.0, 65000000.0],
};

export const DFDA_OPEX_COMMUNITY: Parameter = {
  value: 2000000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Community Support Costs",
  description: "Decentralized Framework for Drug Assessment community support costs",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#opex-breakdown",
  confidence: "high",
  confidenceInterval: [1000000.0, 3000000.0],
};

export const DFDA_OPEX_INFRASTRUCTURE: Parameter = {
  value: 8000000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Infrastructure Costs",
  description: "Decentralized Framework for Drug Assessment infrastructure costs (cloud, security)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#opex-breakdown",
  confidence: "high",
  confidenceInterval: [5000000.0, 12000000.0],
};

export const DFDA_OPEX_PCT_OF_TREATY_FUNDING: Parameter = {
  value: 0.0014716703458425313,
  unit: "rate",
  displayName: "Decentralized Framework for Drug Assessment Overhead Percentage of Treaty Funding",
  description: "Percentage of treaty funding allocated to Decentralized Framework for Drug Assessment platform overhead",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/economics#funding-allocation",
  confidence: "high",
  formula: "DFDA_OPEX / TREATY_FUNDING",
  latex: "DFDAOpexPct = \\$0.04B / \\$27.18B = 0.00147 = 0.15\\%",
};

export const DFDA_OPEX_PLATFORM_MAINTENANCE: Parameter = {
  value: 15000000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Maintenance Costs",
  description: "Decentralized Framework for Drug Assessment maintenance costs",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#opex-breakdown",
  confidence: "high",
  confidenceInterval: [10000000.0, 22000000.0],
};

export const DFDA_OPEX_REGULATORY: Parameter = {
  value: 5000000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Regulatory Coordination Costs",
  description: "Decentralized Framework for Drug Assessment regulatory coordination costs",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#opex-breakdown",
  confidence: "high",
  confidenceInterval: [3000000.0, 8000000.0],
};

export const DFDA_OPEX_STAFF: Parameter = {
  value: 10000000.0,
  unit: "USD/year",
  displayName: "Decentralized Framework for Drug Assessment Staff Costs",
  description: "Decentralized Framework for Drug Assessment staff costs (minimal, AI-assisted)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#opex-breakdown",
  confidence: "high",
  confidenceInterval: [7000000.0, 15000000.0],
};

export const DFDA_TARGET_COST_PER_PATIENT_USD: Parameter = {
  value: 1000.0,
  unit: "USD/patient",
  displayName: "Decentralized Framework for Drug Assessment Target Cost per Patient in USD",
  description: "Target cost per patient in USD (same as DFDA_TARGET_COST_PER_PATIENT but in dollars)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#cost-per-patient",
  confidence: "high",
};

export const DFDA_UPFRONT_BUILD: Parameter = {
  value: 40000000.0,
  unit: "USD",
  displayName: "Decentralized Framework for Drug Assessment One-Time Build Cost",
  description: "Decentralized Framework for Drug Assessment one-time build cost (central estimate)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#build-costs",
  confidence: "high",
};

export const DFDA_UPFRONT_BUILD_MAX: Parameter = {
  value: 46000000.0,
  unit: "USD",
  displayName: "Decentralized Framework for Drug Assessment One-Time Build Cost (Maximum)",
  description: "Decentralized Framework for Drug Assessment one-time build cost (high estimate)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#build-costs",
  confidence: "high",
};

export const DIH_NPV_ANNUAL_OPEX_INITIATIVES: Parameter = {
  value: 21100000.0,
  unit: "USD/year",
  displayName: "DIH Broader Initiatives Annual OPEX",
  description: "DIH broader initiatives annual opex (medium case)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#npv-costs",
  confidence: "high",
  confidenceInterval: [14000000.0, 32000000.0],
};

export const DIH_NPV_UPFRONT_COST_INITIATIVES: Parameter = {
  value: 229750000.0,
  unit: "USD",
  displayName: "DIH Broader Initiatives Upfront Cost",
  description: "DIH broader initiatives upfront cost (medium case)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/dfda-cost-benefit-analysis#npv-costs",
  confidence: "high",
  confidenceInterval: [150000000.0, 350000000.0],
};

export const DIH_TREASURY_MEDICAL_RESEARCH_PCT: Parameter = {
  value: 0.8,
  unit: "rate",
  displayName: "Medical Research Percentage of Treaty Funding",
  description: "Percentage of treaty funding allocated to medical research (after bond payouts and IAB incentives)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/economics#funding-allocation",
  confidence: "high",
  formula: "MEDICAL_RESEARCH_FUNDING / TREATY_FUNDING",
  latex: "MedicalResearchPct = \\$21.744B / \\$27.18B = 0.80 = 80\\%",
};

export const DIH_TREASURY_TRIAL_SUBSIDIES_PCT: Parameter = {
  value: 0.7985283296541574,
  unit: "rate",
  displayName: "Patient Trial Subsidies Percentage of Treaty Funding",
  description: "Percentage of treaty funding going directly to patient trial subsidies",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/economics#funding-allocation",
  confidence: "high",
  formula: "TRIAL_SUBSIDIES / TREATY_FUNDING",
  latex: "TrialSubsidiesPct = \\$21.70B / \\$27.18B = 0.7985 = 79.85\\%",
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
  sourceRef: "https://impact.dih.earth/knowledge/economics/economics",
  confidence: "high",
  formula: "ANNUAL_DISEASE_DEATHS ÷ 911_DEATHS",
  latex: "\\frac{54.75\\text{M disease deaths}}{3{,}000\\text{ terrorism deaths}} \\approx 18{,}274:1",
};

export const DISEASE_VS_WAR_DEATHS_RATIO: Parameter = {
  value: 224.8569092395748,
  unit: "ratio",
  displayName: "Ratio of Annual Disease Deaths to War Deaths",
  description: "Ratio of annual disease deaths to war deaths",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/economics",
  confidence: "high",
  formula: "ANNUAL_DISEASE_DEATHS ÷ WAR_DEATHS",
  latex: "\\frac{54.75\\text{M disease deaths}}{400{,}000\\text{ conflict deaths}} \\approx 137:1",
};

export const EFFECTIVE_HOURLY_RATE_LIFETIME_BENEFIT: Parameter = {
  value: 4300000.0,
  unit: "USD",
  displayName: "Lifetime Benefit for Age 30 Baseline Scenario",
  description: "Lifetime benefit for age 30 baseline scenario ($4.3M)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/disease-eradication-personal-lifetime-wealth-calculations",
  confidence: "high",
  formula: "Total lifetime health gains from 1% treaty",
  latex: "Benefit = \\$4,300,000",
};

export const EVENTUALLY_AVOIDABLE_DEATH_PCT: Parameter = {
  value: 0.9262780790085205,
  unit: "percentage",
  displayName: "Eventually Avoidable Death Percentage",
  description: "Percentage of deaths that are eventually avoidable with sufficient biomedical research and technological advancement",
  sourceType: "definition",
  confidence: "medium",
  formula: "1 - FUNDAMENTALLY_UNAVOIDABLE_DEATH_PCT",
  latex: "P_{\\text{avoidable}} = 1 - 0.0791 = 92.09\\%",
};

export const FAMILY_OFFICE_INVESTMENT_MIN: Parameter = {
  value: 5000000.0,
  unit: "USD",
  displayName: "Minimum Investment for Family Offices",
  description: "Minimum investment for family offices",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/victory-bonds",
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
  latex: "P_{\\text{unavoidable}} = \\sum_{\\text{categories}} (\\text{disease burden} \\times (1 - \\text{max cure rate})) = 7.91\\%",
};

export const HOURS_PER_DAY: Parameter = {
  value: 24.0,
};

export const HOURS_PER_YEAR: Parameter = {
  value: 8760.0,
};

export const IAB_BOOTSTRAP_CAMPAIGN_COST_BASE_USD: Parameter = {
  value: 100000000.0,
  unit: "USD",
  displayName: "Bootstrap Campaign Cost (Base Case)",
  description: "Base case estimate for bootstrap campaign cost",
  sourceType: "definition",
  confidence: "high",
};

export const IAB_BOOTSTRAP_CAMPAIGN_COST_CONSERVATIVE_USD: Parameter = {
  value: 200000000.0,
  unit: "USD",
  displayName: "Bootstrap Campaign Cost (Conservative)",
  description: "Conservative estimate for bootstrap campaign cost",
  sourceType: "definition",
  confidence: "high",
};

export const IAB_BOOTSTRAP_CAMPAIGN_COST_OPTIMISTIC_USD: Parameter = {
  value: 50000000.0,
  unit: "USD",
  displayName: "Bootstrap Campaign Cost (Optimistic)",
  description: "Optimistic estimate for bootstrap campaign cost",
  sourceType: "definition",
  confidence: "high",
};

export const IAB_MECHANISM_ANNUAL_COST: Parameter = {
  value: 750000000.0,
  unit: "USD/year",
  displayName: "IAB Mechanism Annual Cost (High Estimate)",
  description: "Estimated annual cost of the IAB mechanism (high-end estimate including regulatory defense)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/incentive-alignment-bonds-paper#welfare-analysis",
  confidence: "high",
  confidenceInterval: [160000000.0, 750000000.0],
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
  sourceRef: "https://impact.dih.earth/knowledge/economics/victory-bonds",
  confidence: "high",
};

export const LOBBYIST_BOND_INVESTMENT_MAX: Parameter = {
  value: 20000000.0,
  unit: "USD",
  displayName: "Maximum Bond Investment for Lobbyist Incentives",
  description: "Maximum bond investment for lobbyist incentives",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/strategy/roadmap#lobbyist-incentives",
  confidence: "high",
};

export const MINUTES_PER_HOUR: Parameter = {
  value: 60.0,
};

export const MONTHS_PER_YEAR: Parameter = {
  value: 12.0,
};

export const NPV_DISCOUNT_RATE_STANDARD: Parameter = {
  value: 0.03,
  unit: "rate",
  displayName: "Standard Discount Rate for NPV Analysis",
  description: "Standard discount rate for NPV analysis (3% annual, social discount rate)",
  sourceType: "definition",
  confidence: "high",
  latex: "r = 0.03 \\text{ (discount rate)}",
};

export const NPV_TIME_HORIZON_YEARS: Parameter = {
  value: 10.0,
  unit: "years",
  displayName: "Standard Time Horizon for NPV Analysis",
  description: "Standard time horizon for NPV analysis",
  sourceType: "definition",
  confidence: "high",
  latex: "T = 10 \\text{ (time horizon, years)}",
};

export const PEACE_DIVIDEND_DIRECT_FISCAL_SAVINGS: Parameter = {
  value: 27180000000.0,
  unit: "USD/year",
  displayName: "Direct Fiscal Savings from 1% Military Spending Reduction",
  description: "Direct fiscal savings from 1% military spending reduction (high confidence)",
  sourceType: "definition",
  sourceRef: "sipri-2024-spending",
  confidence: "high",
  formula: "TREATY_ANNUAL_FUNDING",
  latex: "PeaceDividend_{fiscal} = \\$27.18B",
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

export const SAFE_COMPOUNDS_COUNT: Parameter = {
  value: 9500.0,
  unit: "compounds",
  displayName: "Safe Compounds Available for Testing",
  description: "Total safe compounds available for repurposing (FDA-approved + GRAS substances, midpoint of 7,000-12,000 range)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/problem/untapped-therapeutic-frontier",
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
  sourceRef: "https://impact.dih.earth/knowledge/problem/untapped-therapeutic-frontier",
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
  value: 27180000000.0,
  unit: "USD/year",
  displayName: "Annual Funding from 1% of Global Military Spending Redirected to DIH",
  description: "Annual funding from 1% of global military spending redirected to DIH",
  sourceType: "definition",
  confidence: "high",
  formula: "MILITARY_SPENDING × 1%",
};

export const TREATY_CAMPAIGN_BUDGET_LOBBYING: Parameter = {
  value: 650000000.0,
  unit: "USD",
  displayName: "Political Lobbying Campaign: Direct Lobbying, Super Pacs, Opposition Research, Staff, Legal/Compliance",
  description: "Political lobbying campaign: direct lobbying (US/EU/G20), Super PACs, opposition research, staff, legal/compliance. Budget exceeds combined pharma ($300M/year) and military-industrial complex ($150M/year) lobbying to ensure competitive positioning. Referendum relies on grassroots mobilization and earned media, while lobbying requires matching or exceeding opposition spending for political viability.",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/fundraising-strategy#campaign-budget-breakdown",
  confidence: "low",
  confidenceInterval: [325000000.0, 1300000000.0],
};

export const TREATY_CAMPAIGN_BUDGET_REFERENDUM: Parameter = {
  value: 300000000.0,
  unit: "USD",
  displayName: "Global Referendum Campaign: Ads, Media, Partnerships, Staff, Legal/Compliance",
  description: "Global referendum campaign (get 208M votes): ads, media, partnerships, staff, legal/compliance",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/fundraising-strategy#campaign-budget-breakdown",
  confidence: "medium",
  confidenceInterval: [180000000.0, 500000000.0],
};

export const TREATY_CAMPAIGN_BUDGET_RESERVE: Parameter = {
  value: 50000000.0,
  unit: "USD",
  displayName: "Reserve Fund / Contingency Buffer",
  description: "Reserve fund / contingency buffer (5% of total campaign cost). Conservative estimate uses 5% given transparent budget allocation and predictable referendum/lobbying costs, though industry standard is 10-20% for complex campaigns. Upper confidence bound of $100M (10%) reflects potential for unforeseen legal challenges, opposition response, or regulatory delays.",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/appendix/fundraising-strategy#campaign-budget-breakdown",
  confidence: "medium",
  confidenceInterval: [20000000.0, 100000000.0],
};

export const TREATY_CAMPAIGN_BUDGET_SUPER_PACS: Parameter = {
  value: 800000000.0,
  unit: "USD",
  displayName: "Campaign Budget for Super Pacs and Political Lobbying",
  description: "Campaign budget for Super PACs and political lobbying",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/strategy/roadmap#campaign-budget",
  confidence: "high",
};

export const TREATY_CAMPAIGN_DURATION_YEARS: Parameter = {
  value: 4.0,
  unit: "years",
  displayName: "Treaty Campaign Duration",
  description: "Treaty campaign duration (3-5 year range, using midpoint)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/strategy/roadmap",
  confidence: "high",
  confidenceInterval: [3.0, 5.0],
};

export const TREATY_CAMPAIGN_VIRAL_REFERENDUM_BASE_CASE: Parameter = {
  value: 140000000.0,
  unit: "USD",
  displayName: "Base Case Viral Referendum Budget",
  description: "Base case viral referendum budget (assumes flat $0.50/vote, optimistic)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget#base-case-scenario",
  confidence: "medium",
  formula: "PLATFORM + VERIFICATION + PAYMENTS_FLAT_RATE",
};

export const TREATY_CAMPAIGN_VIRAL_REFERENDUM_REALISTIC: Parameter = {
  value: 220000000.0,
  unit: "USD",
  displayName: "Realistic Viral Referendum Budget",
  description: "Realistic viral referendum budget (moderate tiered pricing)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget#realistic-scenario",
  confidence: "high",
  formula: "PLATFORM + VERIFICATION + MODERATE_TIERED_PAYMENTS",
  latex: "Budget_{realistic} = \\$35M_{platform} + \\$59M_{verification} + \\$126M_{tiered\\ payments} = \\$220M",
};

export const TREATY_CAMPAIGN_VIRAL_REFERENDUM_WORST_CASE: Parameter = {
  value: 406000000.0,
  unit: "USD",
  displayName: "Worst-Case Viral Referendum Budget",
  description: "Worst-case viral referendum budget (tiered pricing with increasing marginal costs)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/economics/campaign-budget#worst-case-scenario",
  confidence: "medium",
  formula: "PLATFORM + VERIFICATION + TIERED_PAYMENTS",
  latex: "Budget_{worst} = \\$35M_{platform} + \\$59M_{verification} + \\$312M_{tiered\\ payments} = \\$406M",
};

export const TREATY_REDUCTION_PCT: Parameter = {
  value: 0.01,
  unit: "rate",
  displayName: "1% Reduction in Military Spending/War Costs from Treaty",
  description: "1% reduction in military spending/war costs from treaty",
  sourceType: "definition",
  confidence: "high",
};

export const TRIAL_COST_REDUCTION_PCT: Parameter = {
  value: 0.5,
  unit: "rate",
  displayName: "Decentralized Framework for Drug Assessment Trial Cost Reduction Percentage",
  description: "Trial cost reduction percentage (50% baseline, conservative)",
  sourceType: "definition",
  confidence: "high",
  confidenceInterval: [0.4, 0.65],
};

export const TRIAL_RELEVANT_DISEASES_COUNT: Parameter = {
  value: 1000.0,
  unit: "diseases",
  displayName: "Trial-Relevant Diseases",
  description: "Consolidated count of trial-relevant diseases worth targeting (after grouping ICD-10 codes)",
  sourceType: "definition",
  sourceRef: "https://impact.dih.earth/knowledge/problem/untapped-therapeutic-frontier",
  confidence: "high",
  confidenceInterval: [800.0, 1200.0],
};

export const VICTORY_BOND_ANNUAL_PAYOUT: Parameter = {
  value: 2718000000.0,
  unit: "USD/year",
  displayName: "Annual VICTORY Incentive Alignment Bond Payout",
  description: "Annual VICTORY bond payout (treaty funding × bond percentage)",
  sourceType: "definition",
  confidence: "high",
  formula: "TREATY_FUNDING × BOND_PCT",
};

export const VICTORY_BOND_ANNUAL_RETURN_PCT: Parameter = {
  value: 2.718,
  unit: "rate",
  displayName: "Annual Return Percentage for VICTORY Incentive Alignment Bondholders",
  description: "Annual return percentage for VICTORY bondholders",
  sourceType: "definition",
  confidence: "high",
  formula: "PAYOUT ÷ CAMPAIGN_COST",
  latex: "Return = \\$2.718B / \\$1B = 2.718 = 271.8\\%",
};

export const VICTORY_BOND_FUNDING_PCT: Parameter = {
  value: 0.1,
  unit: "rate",
  displayName: "Percentage of Captured Dividend Funding VICTORY Incentive Alignment Bonds",
  description: "Percentage of captured dividend funding VICTORY bonds (10%)",
  sourceType: "definition",
  confidence: "high",
};

// ============================================================================
// All Parameters (for iteration)
// ============================================================================

export const parameters = {
  ANTIDEPRESSANT_TRIAL_EXCLUSION_RATE,
  AVERAGE_MARKET_RETURN_PCT,
  AVERAGE_US_HOURLY_WAGE,
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
  CURRENT_ACTIVE_TRIALS,
  CURRENT_CLINICAL_TRIAL_PARTICIPATION_RATE,
  CURRENT_DISEASE_PATIENTS_GLOBAL,
  CURRENT_DRUG_APPROVALS_PER_YEAR,
  CURRENT_TRIALS_PER_YEAR,
  CURRENT_TRIAL_ABANDONMENT_RATE,
  CURRENT_TRIAL_SLOTS_AVAILABLE,
  DEFENSE_LOBBYING_ANNUAL,
  DEWORMING_COST_PER_DALY,
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
  GLOBAL_DAILY_DEATHS_CURABLE_DISEASES,
  GLOBAL_DISEASE_DEATHS_DAILY,
  GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL,
  GLOBAL_DISEASE_HUMAN_LIFE_VALUE_LOSS_ANNUAL,
  GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL,
  GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL,
  GLOBAL_HOUSEHOLD_WEALTH_USD,
  GLOBAL_LIFE_EXPECTANCY_2024,
  GLOBAL_MED_RESEARCH_SPENDING,
  GLOBAL_MILITARY_SPENDING_ANNUAL_2024,
  GLOBAL_POPULATION_2024,
  GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT,
  GLOBAL_SYMPTOMATIC_DISEASE_TREATMENT_ANNUAL,
  HUMAN_GENOME_PROJECT_TOTAL_ECONOMIC_IMPACT,
  HUMAN_INTERACTOME_TARGETED_PCT,
  ICD_10_TOTAL_CODES,
  LIFE_EXTENSION_YEARS,
  LOBBYIST_SALARY_MAX,
  LOBBYIST_SALARY_MIN_K,
  MEASLES_VACCINATION_ROI,
  MENTAL_HEALTH_PRODUCTIVITY_LOSS_PER_CAPITA,
  NIH_CLINICAL_TRIALS_SPENDING_PCT,
  OXFORD_RECOVERY_TRIAL_DURATION_MONTHS,
  PATIENT_WILLINGNESS_TRIAL_PARTICIPATION_PCT,
  PHARMA_DRUG_DEVELOPMENT_COST_CURRENT,
  PHARMA_DRUG_REVENUE_AVERAGE_CURRENT,
  PHARMA_ROI_CURRENT_SYSTEM_PCT,
  PHARMA_SUCCESS_RATE_CURRENT_PCT,
  PHASE_1_PASSED_COMPOUNDS_GLOBAL,
  PHASE_1_SAFETY_DURATION_YEARS,
  PHASE_3_TRIAL_COST_MIN,
  POLIO_VACCINATION_ROI,
  POLITICAL_SUCCESS_PROBABILITY,
  POST_1962_DRUG_APPROVAL_REDUCTION_PCT,
  POST_WW2_MILITARY_CUT_PCT,
  PRE_1962_DRUG_DEVELOPMENT_COST,
  PRE_1962_PHYSICIAN_COUNT,
  RARE_DISEASES_COUNT_GLOBAL,
  RECOVERY_TRIAL_COST_PER_PATIENT,
  REGULATORY_DELAY_MEAN_AGE_OF_DEATH,
  REGULATORY_DELAY_SUFFERING_PERIOD_YEARS,
  SMALLPOX_ERADICATION_ROI,
  SMALLPOX_ERADICATION_TOTAL_BENEFIT,
  SMOKING_CESSATION_ANNUAL_BENEFIT,
  STANDARD_ECONOMIC_QALY_VALUE_USD,
  STANDARD_QALYS_PER_LIFE_SAVED,
  SUGAR_SUBSIDY_COST_PER_PERSON_ANNUAL,
  SWITZERLAND_DEFENSE_SPENDING_PCT,
  SWITZERLAND_GDP_PER_CAPITA_K,
  TERRORISM_DEATHS_911,
  THALIDOMIDE_CASES_WORLDWIDE,
  THALIDOMIDE_DISABILITY_WEIGHT,
  THALIDOMIDE_MORTALITY_RATE,
  THALIDOMIDE_SURVIVOR_LIFESPAN,
  THALIDOMIDE_US_POPULATION_SHARE_1960,
  TRADITIONAL_PHASE3_COST_PER_PATIENT,
  TRADITIONAL_PHASE3_COST_PER_PATIENT_EXAMPLE_48K,
  TRADITIONAL_PHASE3_COST_PER_PATIENT_FDA_EXAMPLE_41K,
  TREATMENT_ACCELERATION_YEARS_CURRENT,
  TRIAL_COST_REDUCTION_FACTOR,
  TYPICAL_CEO_HOURLY_RATE,
  US_ALZHEIMERS_ANNUAL_COST,
  US_CANCER_ANNUAL_COST,
  US_CHRONIC_DISEASE_SPENDING_ANNUAL,
  US_DIABETES_ANNUAL_COST,
  US_HEART_DISEASE_ANNUAL_COST,
  US_MENTAL_HEALTH_COST_ANNUAL,
  US_MILITARY_SPENDING_PCT_GDP,
  US_POPULATION_2024,
  VALUE_OF_STATISTICAL_LIFE,
  VITAMIN_A_COST_PER_DALY,
  WATER_FLUORIDATION_ANNUAL_BENEFIT,
  WATER_FLUORIDATION_ROI,
  WHO_QALY_THRESHOLD_COST_EFFECTIVE,
  WORKFORCE_WITH_PRODUCTIVITY_LOSS,
  COMBINED_PEACE_HEALTH_DIVIDENDS_ANNUAL_FOR_ROI_CALC,
  DFDA_ANNUAL_OPEX,
  DFDA_BENEFIT_RD_ONLY_ANNUAL,
  DFDA_EXPECTED_ROI,
  DFDA_NET_SAVINGS_RD_ONLY_ANNUAL,
  DFDA_NPV_ANNUAL_OPEX_TOTAL,
  DFDA_NPV_BENEFIT_RD_ONLY,
  DFDA_NPV_NET_BENEFIT_RD_ONLY,
  DFDA_NPV_PV_ANNUAL_OPEX,
  DFDA_NPV_TOTAL_COST,
  DFDA_NPV_UPFRONT_COST_TOTAL,
  DFDA_RD_GROSS_SAVINGS_ANNUAL,
  DFDA_RD_SAVINGS_DAILY,
  DFDA_ROI_RD_ONLY,
  DFDA_ROI_SIMPLE,
  DFDA_TRIALS_PER_YEAR_CAPACITY,
  DIH_PATIENTS_FUNDABLE_ANNUALLY,
  DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL,
  DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL,
  DISEASE_ERADICATION_DELAY_DALYS,
  DISEASE_ERADICATION_DELAY_DEATHS_TOTAL,
  DISEASE_ERADICATION_DELAY_ECONOMIC_LOSS,
  DISEASE_ERADICATION_DELAY_YLD,
  DISEASE_ERADICATION_DELAY_YLL,
  DISEASE_ERADICATION_PLUS_ACCELERATION_DEATHS_TOTAL,
  DISEASE_ERADICATION_PLUS_ACCELERATION_ECONOMIC_LOSS_TOTAL,
  DIVIDEND_COVERAGE_FACTOR,
  DRUG_COST_INCREASE_1980S_TO_CURRENT_MULTIPLIER,
  DRUG_COST_INCREASE_PRE1962_TO_CURRENT_MULTIPLIER,
  DRUG_DISEASE_COMBINATIONS_POSSIBLE,
  EXPLORATION_RATIO,
  FDA_TO_OXFORD_RECOVERY_TRIAL_TIME_MULTIPLIER,
  GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL,
  GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT,
  GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE,
  GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS,
  GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT,
  GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT,
  GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT,
  GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL,
  GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL,
  GLOBAL_ANNUAL_WAR_TOTAL_COST,
  GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL,
  GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL,
  GLOBAL_INDUSTRY_CLINICAL_TRIALS_SPENDING_ANNUAL,
  GLOBAL_MILITARY_SPENDING_PER_CAPITA_ANNUAL,
  GLOBAL_MILITARY_SPENDING_POST_TREATY_ANNUAL_2024,
  GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL,
  HISTORICAL_PROGRESS_DEATHS_TOTAL,
  HISTORICAL_PROGRESS_ECONOMIC_LOSS_TOTAL,
  IAB_MECHANISM_BENEFIT_COST_RATIO,
  IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL,
  INDUSTRY_VS_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO,
  MEDICAL_RESEARCH_PCT_OF_DISEASE_BURDEN,
  MILITARY_TO_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO,
  MILITARY_VS_MEDICAL_RESEARCH_RATIO,
  MISALLOCATION_FACTOR_DEATH_VS_SAVING,
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
  SUFFERING_HOURS_ELIMINATED_TOTAL,
  THALIDOMIDE_DALYS_PER_EVENT,
  THALIDOMIDE_DEATHS_PER_EVENT,
  THALIDOMIDE_SURVIVORS_PER_EVENT,
  THALIDOMIDE_US_CASES_PREVENTED,
  THALIDOMIDE_YLD_PER_EVENT,
  THALIDOMIDE_YLL_PER_EVENT,
  TOTAL_RESEARCH_FUNDING_WITH_TREATY,
  TREATY_BENEFIT_MULTIPLIER_VS_VACCINES,
  TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED,
  TREATY_CAMPAIGN_TOTAL_COST,
  TREATY_CAMPAIGN_VOTING_BLOC_TARGET,
  TREATY_COMPLETE_ROI_ALL_BENEFITS,
  TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT,
  TREATY_EXPECTED_COST_PER_DALY,
  TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER,
  TREATY_LIVES_SAVED_ANNUAL_GLOBAL,
  TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS,
  TREATY_QALYS_GAINED_ANNUAL_GLOBAL,
  TREATY_RECURRING_BENEFITS_ANNUAL,
  TREATY_ROI_HISTORICAL_RATE,
  TREATY_ROI_INNOVATION_ACCELERATION,
  TREATY_ROI_LAG_ELIMINATION,
  TREATY_TOTAL_ANNUAL_COSTS,
  TREATY_TOTAL_COMPLETE_BENEFITS_ANNUAL,
  TREATY_VS_BED_NETS_MULTIPLIER,
  TRIAL_CAPACITY_CUMULATIVE_YEARS_20YR,
  TRIAL_CAPACITY_MULTIPLIER,
  TYPE_II_ERROR_COST_RATIO,
  TYPE_I_ERROR_BENEFIT_DALYS,
  UNEXPLORED_RATIO,
  US_MAJOR_DISEASES_TOTAL_ANNUAL_COST,
  APPROVED_DRUG_DISEASE_PAIRINGS,
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
  CHILDHOOD_VACCINATION_COST_PER_DALY,
  CONCENTRATED_INTEREST_SECTOR_MARKET_CAP_USD,
  CURRENT_PATIENT_PARTICIPATION_RATE,
  DAYS_PER_YEAR,
  DCT_PLATFORM_FUNDING_MEDIUM,
  DEFENSE_SECTOR_RETENTION_PCT,
  DFDA_NPV_ADOPTION_RAMP_YEARS,
  DFDA_NPV_ANNUAL_OPEX,
  DFDA_NPV_UPFRONT_COST,
  DFDA_OPEX_COMMUNITY,
  DFDA_OPEX_INFRASTRUCTURE,
  DFDA_OPEX_PCT_OF_TREATY_FUNDING,
  DFDA_OPEX_PLATFORM_MAINTENANCE,
  DFDA_OPEX_REGULATORY,
  DFDA_OPEX_STAFF,
  DFDA_TARGET_COST_PER_PATIENT_USD,
  DFDA_UPFRONT_BUILD,
  DFDA_UPFRONT_BUILD_MAX,
  DIH_NPV_ANNUAL_OPEX_INITIATIVES,
  DIH_NPV_UPFRONT_COST_INITIATIVES,
  DIH_TREASURY_MEDICAL_RESEARCH_PCT,
  DIH_TREASURY_TRIAL_SUBSIDIES_PCT,
  DISEASE_RELATED_CAREGIVER_PCT,
  DISEASE_VS_TERRORISM_DEATHS_RATIO,
  DISEASE_VS_WAR_DEATHS_RATIO,
  EFFECTIVE_HOURLY_RATE_LIFETIME_BENEFIT,
  EVENTUALLY_AVOIDABLE_DEATH_PCT,
  FAMILY_OFFICE_INVESTMENT_MIN,
  FUNDAMENTALLY_UNAVOIDABLE_DEATH_PCT,
  HOURS_PER_DAY,
  HOURS_PER_YEAR,
  IAB_BOOTSTRAP_CAMPAIGN_COST_BASE_USD,
  IAB_BOOTSTRAP_CAMPAIGN_COST_CONSERVATIVE_USD,
  IAB_BOOTSTRAP_CAMPAIGN_COST_OPTIMISTIC_USD,
  IAB_MECHANISM_ANNUAL_COST,
  IAB_POLITICAL_INCENTIVE_FUNDING_PCT,
  INSTITUTIONAL_INVESTOR_MIN,
  LOBBYIST_BOND_INVESTMENT_MAX,
  MINUTES_PER_HOUR,
  MONTHS_PER_YEAR,
  NPV_DISCOUNT_RATE_STANDARD,
  NPV_TIME_HORIZON_YEARS,
  PEACE_DIVIDEND_DIRECT_FISCAL_SAVINGS,
  PRE_1962_VALIDATION_YEARS,
  SAFE_COMPOUNDS_COUNT,
  SECONDS_PER_MINUTE,
  SECONDS_PER_YEAR,
  TESTED_RELATIONSHIPS_ESTIMATE,
  TOTAL_BOOK_WORDS,
  TREATY_ANNUAL_FUNDING,
  TREATY_CAMPAIGN_BUDGET_LOBBYING,
  TREATY_CAMPAIGN_BUDGET_REFERENDUM,
  TREATY_CAMPAIGN_BUDGET_RESERVE,
  TREATY_CAMPAIGN_BUDGET_SUPER_PACS,
  TREATY_CAMPAIGN_DURATION_YEARS,
  TREATY_CAMPAIGN_VIRAL_REFERENDUM_BASE_CASE,
  TREATY_CAMPAIGN_VIRAL_REFERENDUM_REALISTIC,
  TREATY_CAMPAIGN_VIRAL_REFERENDUM_WORST_CASE,
  TREATY_REDUCTION_PCT,
  TRIAL_COST_REDUCTION_PCT,
  TRIAL_RELEVANT_DISEASES_COUNT,
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
  "clinical-trial-cost-per-patient": {
        id: "clinical-trial-cost-per-patient",
        type: "article-journal",
        title: "Clinical trial cost per patient (traditional Phase III)",
        author: [
          {
            literal: "ProRelix Research"
          },
        ],
        'container-title': "ProRelix Research",
        URL: "https://prorelixresearch.com/phase-by-phase-clinical-trial-costs-what-every-sponsor-needs-to-know/",
        note: "ProRelix Research, Phase-by-Phase Clinical Trial Costs | WithPower, Clinical Trial Cost Per Patient | JAMA, Cost of Bringing a New Drug",
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
        type: "article-journal",
        title: "Claim of linear 4-year life expectancy increase from 1890-1960",
        author: [
          {
            literal: "Our World in Data"
          },
        ],
        'container-title': "Our World in Data: Life Expectancy",
        URL: "https://ourworldindata.org/life-expectancy",
        note: "Our World in Data: Life Expectancy | WHO: Global Health Estimates",
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
  "phase-3-cost-per-patient-113k": {
        id: "phase-3-cost-per-patient-113k",
        type: "article-journal",
        title: "Phase 3 cost per patient",
        author: [
          {
            literal: "JAMA Internal Medicine"
          },
        ],
        'container-title': "JAMA Internal Medicine",
        URL: "https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2702287",
        note: "JAMA Internal Medicine, Clinical Trial Cost Breakdown",
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
  "pre-1962-drug-costs-timeline": {
        id: "pre-1962-drug-costs-timeline",
        type: "article-journal",
        title: "Pre-1962 drug development costs and timeline",
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
  "who-daily-deaths": {
        id: "who-daily-deaths",
        type: "article-journal",
        title: "150,000 deaths per day from all causes",
        author: [
          {
            family: "Based on WHO Global Health Estimates showing ~55 million annual deaths / 365 days = ~150",
            given: "000 per day | WHO"
          },
        ],
        issued: { 'date-parts': [[2024]] },
        'container-title': "Based on WHO Global Health Estimates showing ~55 million annual deaths / 365 days = ~150",
        URL: "https://www.who.int/news-room/fact-sheets/detail/the-top-10-causes-of-death",
        note: "Based on WHO Global Health Estimates showing ~55 million annual deaths / 365 days = ~150,000 per day | WHO, 2024, The top 10 causes of death",
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
  }
};

/** Summary statistics */
export const PARAMETER_STATS = {
  total: 331,
  external: 133,
  calculated: 105,
  definitions: 93,
  citations: 97,
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
