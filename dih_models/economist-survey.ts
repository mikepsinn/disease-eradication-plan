// AUTO-GENERATED FILE - DO NOT EDIT
// Generated from _analysis/economist-survey.json
// Run: python scripts/generate-economist-survey.py --top-n 30

/**
 * Economist validation survey data
 * Programmatically generated questions for parameter validation
 */

export type QuestionType =
  | 'rating'
  | 'boolean'
  | 'text'
  | 'range'
  | 'choice'
  | 'checklist';

export type SourceType = 'external' | 'calculated' | 'definition';

export interface SurveyQuestion {
  id: string;
  type: QuestionType;
  question: string;
  options?: string[];
  allowMultiple?: boolean;
  allowOther?: boolean;
}

export interface Citation {
  id: string;
  title: string;
  author?: string;
  year?: string;
  source?: string;
  url?: string;
}

export interface SurveyParameter {
  rank: number;
  name: string;
  displayName: string;
  value: number;
  unit?: string;
  formattedValue: string;
  sourceType: SourceType;
  description?: string;
  formula?: string;
  latex?: string;
  sourceRef?: string;
  citation?: Citation;
  questions: SurveyQuestion[];
}

export interface SurveyMetadata {
  title: string;
  version: string;
  versionDate: string;
  parameterCount: number;
  estimatedTimeMinutes: number;
  conductedBy: string;
  contact: string;
  dataUsage: string;
}

export interface EconomistSurvey {
  metadata: SurveyMetadata;
  parameters: SurveyParameter[];
}

// ============================================================================
// Survey Data
// ============================================================================

export const economistSurvey: EconomistSurvey = {
  metadata: {
    title: "Economic Model Validation Survey for Economists",
    version: "1.0",
    versionDate: "2025-12-12",
    parameterCount: 30,
    estimatedTimeMinutes: 90,
    conductedBy: "Decentralized Institutes of Health Initiative",
    contact: "feedback@warondisease.org",
    dataUsage: "Responses will be used to refine economic model parameters. Individual responses are confidential.",
  },
  parameters: [
    {
      rank: 1,
      name: "BED_NETS_COST_PER_DALY",
      displayName: "Bed Nets Cost per DALY",
      value: 0,
      formattedValue: "0",
      sourceType: "external",
      description: "GiveWell cost per DALY for insecticide-treated bed nets (midpoint estimate, range $78-100). DALYs (Disability-Adjusted Life Years) measure disease burden by combining years of life lost and years lived with disability. Bed nets prevent malaria deaths and are considered a gold standard benchmark for cost-effective global health interventions - if an intervention costs less per DALY than bed nets, it's exceptionally cost-effective. GiveWell synthesizes peer-reviewed academic research with transparent, rigorous methodology and extensive external expert review.",
      citation: {
        id: "givewell-cost-per-life-saved",
        title: "GiveWell Cost per Life Saved for Top Charities (2024)",
        author: "GiveWell",
        source: "GiveWell: Top Charities",
        url: "https://www.givewell.org/charities/top-charities",
      },
      questions: [
        {
          id: "BED_NETS_COST_PER_DALY_source_credibility",
          type: "rating",
          question: "Rate the credibility of this source for estimating: Bed Nets Cost per DALY",
          options: [
            "1 (Not credible)",
            "2",
            "3 (Somewhat credible)",
            "4",
            "5 (Highly credible)",
            "Not qualified to assess"
          ],
        },
        {
          id: "BED_NETS_COST_PER_DALY_value_reasonable",
          type: "boolean",
          question: "Is the central estimate of $89 per DALY reasonable?",
          options: [
            "Yes",
            "No"
          ],
        },
        {
          id: "BED_NETS_COST_PER_DALY_better_source",
          type: "text",
          question: "Do you know of a better or more recent source?",
        },
        {
          id: "BED_NETS_COST_PER_DALY_confidence_interval",
          type: "range",
          question: "The model uses a 90% confidence interval of [$78, $100] per DALY. What is your 90% CI?",
          options: [
            "Lower bound",
            "Upper bound"
          ],
        }
      ],
    },
    {
      rank: 2,
      name: "TREATY_CAMPAIGN_BUDGET_REFERENDUM",
      displayName: "Global Referendum Campaign: Ads, Media, Partnerships, Staff, Legal/Compliance",
      value: 0,
      formattedValue: "0",
      sourceType: "definition",
      description: "Global referendum campaign (get 208M votes): ads, media, partnerships, staff, legal/compliance",
      questions: [
        {
          id: "TREATY_CAMPAIGN_BUDGET_REFERENDUM_assumption_reasonable",
          type: "rating",
          question: "Is this assumption reasonable: Global Referendum Campaign: Ads, Media, Partnerships, Staff, Legal/Compliance = $300M",
          options: [
            "1 (Unreasonable)",
            "2 (Questionable)",
            "3 (Acceptable)",
            "4 (Reasonable)",
            "5 (Very reasonable)",
            "Not qualified to assess"
          ],
        },
        {
          id: "TREATY_CAMPAIGN_BUDGET_REFERENDUM_alternative_value",
          type: "text",
          question: "What value would you use instead? (Current: $300M)",
        },
        {
          id: "TREATY_CAMPAIGN_BUDGET_REFERENDUM_confidence_interval",
          type: "range",
          question: "The model uses a 90% confidence interval of [$180M, $500M]. What is your 90% CI?",
          options: [
            "Lower bound",
            "Upper bound"
          ],
        }
      ],
    },
    {
      rank: 3,
      name: "TREATY_CAMPAIGN_BUDGET_LOBBYING",
      displayName: "Political Lobbying Campaign: Direct Lobbying, Super Pacs, Opposition Research, Staff, Legal/Compliance",
      value: 0,
      formattedValue: "0",
      sourceType: "definition",
      description: "Political lobbying campaign: direct lobbying (US/EU/G20), Super PACs, opposition research, staff, legal/compliance. Budget exceeds combined pharma ($300M/year) and military-industrial complex ($150M/year) lobbying to ensure competitive positioning. Referendum relies on grassroots mobilization and earned media, while lobbying requires matching or exceeding opposition spending for political viability.",
      questions: [
        {
          id: "TREATY_CAMPAIGN_BUDGET_LOBBYING_assumption_reasonable",
          type: "rating",
          question: "Is this assumption reasonable: Political Lobbying Campaign: Direct Lobbying, Super Pacs, Opposition Research, Staff, Legal/Compliance = $650M",
          options: [
            "1 (Unreasonable)",
            "2 (Questionable)",
            "3 (Acceptable)",
            "4 (Reasonable)",
            "5 (Very reasonable)",
            "Not qualified to assess"
          ],
        },
        {
          id: "TREATY_CAMPAIGN_BUDGET_LOBBYING_alternative_value",
          type: "text",
          question: "What value would you use instead? (Current: $650M)",
        },
        {
          id: "TREATY_CAMPAIGN_BUDGET_LOBBYING_confidence_interval",
          type: "range",
          question: "The model uses a 90% confidence interval of [$325M, $1.30B]. What is your 90% CI?",
          options: [
            "Lower bound",
            "Upper bound"
          ],
        }
      ],
    },
    {
      rank: 4,
      name: "TREATY_CAMPAIGN_BUDGET_RESERVE",
      displayName: "Reserve Fund / Contingency Buffer",
      value: 0,
      formattedValue: "0",
      sourceType: "definition",
      description: "Reserve fund / contingency buffer (5% of total campaign cost). Conservative estimate uses 5% given transparent budget allocation and predictable referendum/lobbying costs, though industry standard is 10-20% for complex campaigns. Upper confidence bound of $100M (10%) reflects potential for unforeseen legal challenges, opposition response, or regulatory delays.",
      questions: [
        {
          id: "TREATY_CAMPAIGN_BUDGET_RESERVE_assumption_reasonable",
          type: "rating",
          question: "Is this assumption reasonable: Reserve Fund / Contingency Buffer = $50M",
          options: [
            "1 (Unreasonable)",
            "2 (Questionable)",
            "3 (Acceptable)",
            "4 (Reasonable)",
            "5 (Very reasonable)",
            "Not qualified to assess"
          ],
        },
        {
          id: "TREATY_CAMPAIGN_BUDGET_RESERVE_alternative_value",
          type: "text",
          question: "What value would you use instead? (Current: $50M)",
        },
        {
          id: "TREATY_CAMPAIGN_BUDGET_RESERVE_confidence_interval",
          type: "range",
          question: "The model uses a 90% confidence interval of [$20M, $100M]. What is your 90% CI?",
          options: [
            "Lower bound",
            "Upper bound"
          ],
        }
      ],
    },
    {
      rank: 5,
      name: "TREATY_CAMPAIGN_TOTAL_COST",
      displayName: "Total 1% Treaty Campaign Cost",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "Total treaty campaign cost (100% VICTORY Incentive Alignment Bonds)",
      questions: [
        {
          id: "TREATY_CAMPAIGN_TOTAL_COST_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **Total 1% Treaty Campaign Cost**?\n\n**Current result:** $1B\n**Calculation:** $300M + $650M + $50M = $1B",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "TREATY_CAMPAIGN_TOTAL_COST_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Global Referendum Campaign: $300M\n• Political Lobbying Campaign: $650M\n• Reserve Fund / Contingency Buffer: $50M",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "TREATY_CAMPAIGN_TOTAL_COST_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    },
    {
      rank: 6,
      name: "DISEASE_ERADICATION_DELAY_DALYS",
      displayName: "Total DALYs Lost from Disease Eradication Delay",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "Total Disability-Adjusted Life Years lost from disease eradication delay (PRIMARY estimate)",
      questions: [
        {
          id: "DISEASE_ERADICATION_DELAY_DALYS_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **Total DALYs Lost from Disease Eradication Delay**?\n\n**Current result:** 7.94B DALYs DALYs\n**Calculation:** 7.07B years + 873M years = 7.94B DALYs",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "DISEASE_ERADICATION_DELAY_DALYS_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Years of Life Lost from Disease Eradication Delay: 7.07B years\n• Years Lived with Disability During Disease Eradication Delay: 873M years",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "DISEASE_ERADICATION_DELAY_DALYS_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    },
    {
      rank: 7,
      name: "TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT",
      displayName: "Cost per DALY Averted (Timeline Shift)",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "Cost per DALY averted from one-time timeline shift (8.2 years). This is a conservative estimate that only counts campaign cost ($1B) and ignores all economic benefits ($27B/year funding unlocked + $50B/year R&D savings). For comparison: bed nets cost $89.0/DALY, deworming costs $4-10/DALY. This intervention is 700x more cost-effective than bed nets while also being self-funding.",
      questions: [
        {
          id: "TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **Cost per DALY Averted (Timeline Shift)**?\n\n**Current result:** $0.126 per DALY\n**Calculation:** CAMPAIGN_COST ÷ DALYS_TIMELINE_SHIFT = $0.126",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Total 1% Treaty Campaign Cost: $1B\n• Total DALYs Lost from Disease Eradication Delay: 7.94B DALYs",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    },
    {
      rank: 8,
      name: "POLITICAL_SUCCESS_PROBABILITY",
      displayName: "Political Success Probability",
      value: 0,
      formattedValue: "0",
      sourceType: "external",
      description: "Estimated probability of treaty ratification and sustained implementation. Central estimate 1% is ultra-conservative. This assumes 99% chance of failure. ",
      citation: {
        id: "icbl-ottawa-treaty",
        title: "International Campaign to Ban Landmines (ICBL) - Ottawa Treaty (1997)",
        author: "ICRC",
        year: "1997",
        source: "ICRC",
        url: "https://www.icrc.org/en/doc/resources/documents/article/other/57jpjn.htm",
      },
      questions: [
        {
          id: "POLITICAL_SUCCESS_PROBABILITY_source_credibility",
          type: "rating",
          question: "Rate the credibility of this source for estimating: Political Success Probability",
          options: [
            "1 (Not credible)",
            "2",
            "3 (Somewhat credible)",
            "4",
            "5 (Highly credible)",
            "Not qualified to assess"
          ],
        },
        {
          id: "POLITICAL_SUCCESS_PROBABILITY_value_reasonable",
          type: "boolean",
          question: "Is the central estimate of 1% reasonable?",
          options: [
            "Yes",
            "No"
          ],
        },
        {
          id: "POLITICAL_SUCCESS_PROBABILITY_better_source",
          type: "text",
          question: "Do you know of a better or more recent source?",
        },
        {
          id: "POLITICAL_SUCCESS_PROBABILITY_confidence_interval",
          type: "range",
          question: "The model uses a 90% confidence interval of [0.1%, 10%]. What is your 90% CI?",
          options: [
            "Lower bound",
            "Upper bound"
          ],
        }
      ],
    },
    {
      rank: 9,
      name: "TREATY_EXPECTED_COST_PER_DALY",
      displayName: "Expected Cost per DALY (Risk-Adjusted)",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "Expected cost per DALY accounting for political success probability uncertainty. Monte Carlo samples from beta(0.1%, 10%) distribution. At the ultra-conservative 1% estimate, this is still more cost-effective than bed nets ($89.0/DALY).",
      questions: [
        {
          id: "TREATY_EXPECTED_COST_PER_DALY_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **Expected Cost per DALY (Risk-Adjusted)**?\n\n**Current result:** $13 per DALY\n**Calculation:** CONDITIONAL_COST_PER_DALY ÷ 1% = $13",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "TREATY_EXPECTED_COST_PER_DALY_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Cost per DALY Averted (Timeline Shift): $0.126\n• Political Success Probability: 1%",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "TREATY_EXPECTED_COST_PER_DALY_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    },
    {
      rank: 10,
      name: "TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER",
      displayName: "Expected Cost-Effectiveness vs Bed Nets Multiplier",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "Expected value multiplier vs bed nets (accounts for political uncertainty)",
      questions: [
        {
          id: "TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **Expected Cost-Effectiveness vs Bed Nets Multiplier**?\n\n**Current result:** 7.07 ratiox\n**Calculation:** $89 ÷ $13 = 7.07 ratio",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Bed Nets Cost per DALY: $89\n• Expected Cost per DALY (Risk-Adjusted): $13",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    },
    {
      rank: 11,
      name: "GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL",
      displayName: "Annual Global Spending on Clinical Trials",
      value: 0,
      formattedValue: "0",
      sourceType: "external",
      description: "Annual global spending on clinical trials (Total: Government + Industry)",
      citation: {
        id: "global-clinical-trials-market-2024",
        title: "Global clinical trials market 2024",
        author: "Research and Markets",
        year: "2024",
        source: "Research and Markets",
        url: "https://www.globenewswire.com/news-release/2024/04/19/2866012/0/en/Global-Clinical-Trials-Market-Research-Report-2024-An-83-16-Billion-Market-by-2030-AI-Machine-Learning-and-Blockchain-will-Transform-the-Clinical-Trials-Landscape.html",
      },
      questions: [
        {
          id: "GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL_source_credibility",
          type: "rating",
          question: "Rate the credibility of this source for estimating: Annual Global Spending on Clinical Trials",
          options: [
            "1 (Not credible)",
            "2",
            "3 (Somewhat credible)",
            "4",
            "5 (Highly credible)",
            "Not qualified to assess"
          ],
        },
        {
          id: "GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL_value_reasonable",
          type: "boolean",
          question: "Is the central estimate of $83B reasonable?",
          options: [
            "Yes",
            "No"
          ],
        },
        {
          id: "GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL_better_source",
          type: "text",
          question: "Do you know of a better or more recent source?",
        },
        {
          id: "GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL_confidence_interval",
          type: "range",
          question: "The model uses a 90% confidence interval of [$60B, $110B]. What is your 90% CI?",
          options: [
            "Lower bound",
            "Upper bound"
          ],
        }
      ],
    },
    {
      rank: 12,
      name: "TRIAL_COST_REDUCTION_PCT",
      displayName: "Decentralized Framework for Drug Assessment Trial Cost Reduction Percentage",
      value: 0,
      formattedValue: "0",
      sourceType: "definition",
      description: "Trial cost reduction percentage (50% baseline, conservative)",
      citation: {
        id: "dct-cost-reductions-evidence",
        title: "Decentralized Clinical Trials (DCT) cost reduction evidence",
        author: "Rogers et al.",
        year: "2022",
        source: "Rogers et al.",
        url: "https://discovery.dundee.ac.uk/ws/files/72718478/Brit_J_Clinical_Pharma_2022_Rogers_A_systematic_review_of_methods_used_to_conduct_decentralised_clinical_trials.pdf",
      },
      questions: [
        {
          id: "TRIAL_COST_REDUCTION_PCT_assumption_reasonable",
          type: "rating",
          question: "Is this assumption reasonable: Decentralized Framework for Drug Assessment Trial Cost Reduction Percentage = 50%",
          options: [
            "1 (Unreasonable)",
            "2 (Questionable)",
            "3 (Acceptable)",
            "4 (Reasonable)",
            "5 (Very reasonable)",
            "Not qualified to assess"
          ],
        },
        {
          id: "TRIAL_COST_REDUCTION_PCT_alternative_value",
          type: "text",
          question: "What value would you use instead? (Current: 50%)",
        },
        {
          id: "TRIAL_COST_REDUCTION_PCT_confidence_interval",
          type: "range",
          question: "The model uses a 90% confidence interval of [40%, 65%]. What is your 90% CI?",
          options: [
            "Lower bound",
            "Upper bound"
          ],
        }
      ],
    },
    {
      rank: 13,
      name: "DFDA_RD_GROSS_SAVINGS_ANNUAL",
      displayName: "Decentralized Framework for Drug Assessment Annual Benefit: R&D Savings",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "Annual Decentralized Framework for Drug Assessment benefit from R&D savings (trial cost reduction, secondary component)",
      questions: [
        {
          id: "DFDA_RD_GROSS_SAVINGS_ANNUAL_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **Decentralized Framework for Drug Assessment Annual Benefit: R&D Savings**?\n\n**Current result:** $41.5B\n**Calculation:** TRIAL_SPENDING × 50% = $41.5B",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "DFDA_RD_GROSS_SAVINGS_ANNUAL_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Annual Global Spending on Clinical Trials: $83B\n• Decentralized Framework for Drug Assessment Trial Cost Reduction Percentage: 50%",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "DFDA_RD_GROSS_SAVINGS_ANNUAL_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    },
    {
      rank: 14,
      name: "DFDA_OPEX_PLATFORM_MAINTENANCE",
      displayName: "Decentralized Framework for Drug Assessment Maintenance Costs",
      value: 0,
      formattedValue: "0",
      sourceType: "definition",
      description: "Decentralized Framework for Drug Assessment maintenance costs",
      questions: [
        {
          id: "DFDA_OPEX_PLATFORM_MAINTENANCE_assumption_reasonable",
          type: "rating",
          question: "Is this assumption reasonable: Decentralized Framework for Drug Assessment Maintenance Costs = $15M",
          options: [
            "1 (Unreasonable)",
            "2 (Questionable)",
            "3 (Acceptable)",
            "4 (Reasonable)",
            "5 (Very reasonable)",
            "Not qualified to assess"
          ],
        },
        {
          id: "DFDA_OPEX_PLATFORM_MAINTENANCE_alternative_value",
          type: "text",
          question: "What value would you use instead? (Current: $15M)",
        },
        {
          id: "DFDA_OPEX_PLATFORM_MAINTENANCE_confidence_interval",
          type: "range",
          question: "The model uses a 90% confidence interval of [$10M, $22M]. What is your 90% CI?",
          options: [
            "Lower bound",
            "Upper bound"
          ],
        }
      ],
    },
    {
      rank: 15,
      name: "DFDA_OPEX_STAFF",
      displayName: "Decentralized Framework for Drug Assessment Staff Costs",
      value: 0,
      formattedValue: "0",
      sourceType: "definition",
      description: "Decentralized Framework for Drug Assessment staff costs (minimal, AI-assisted)",
      questions: [
        {
          id: "DFDA_OPEX_STAFF_assumption_reasonable",
          type: "rating",
          question: "Is this assumption reasonable: Decentralized Framework for Drug Assessment Staff Costs = $10M",
          options: [
            "1 (Unreasonable)",
            "2 (Questionable)",
            "3 (Acceptable)",
            "4 (Reasonable)",
            "5 (Very reasonable)",
            "Not qualified to assess"
          ],
        },
        {
          id: "DFDA_OPEX_STAFF_alternative_value",
          type: "text",
          question: "What value would you use instead? (Current: $10M)",
        },
        {
          id: "DFDA_OPEX_STAFF_confidence_interval",
          type: "range",
          question: "The model uses a 90% confidence interval of [$7M, $15M]. What is your 90% CI?",
          options: [
            "Lower bound",
            "Upper bound"
          ],
        }
      ],
    },
    {
      rank: 16,
      name: "DFDA_OPEX_INFRASTRUCTURE",
      displayName: "Decentralized Framework for Drug Assessment Infrastructure Costs",
      value: 0,
      formattedValue: "0",
      sourceType: "definition",
      description: "Decentralized Framework for Drug Assessment infrastructure costs (cloud, security)",
      questions: [
        {
          id: "DFDA_OPEX_INFRASTRUCTURE_assumption_reasonable",
          type: "rating",
          question: "Is this assumption reasonable: Decentralized Framework for Drug Assessment Infrastructure Costs = $8M",
          options: [
            "1 (Unreasonable)",
            "2 (Questionable)",
            "3 (Acceptable)",
            "4 (Reasonable)",
            "5 (Very reasonable)",
            "Not qualified to assess"
          ],
        },
        {
          id: "DFDA_OPEX_INFRASTRUCTURE_alternative_value",
          type: "text",
          question: "What value would you use instead? (Current: $8M)",
        },
        {
          id: "DFDA_OPEX_INFRASTRUCTURE_confidence_interval",
          type: "range",
          question: "The model uses a 90% confidence interval of [$5M, $12M]. What is your 90% CI?",
          options: [
            "Lower bound",
            "Upper bound"
          ],
        }
      ],
    },
    {
      rank: 17,
      name: "DFDA_OPEX_REGULATORY",
      displayName: "Decentralized Framework for Drug Assessment Regulatory Coordination Costs",
      value: 0,
      formattedValue: "0",
      sourceType: "definition",
      description: "Decentralized Framework for Drug Assessment regulatory coordination costs",
      questions: [
        {
          id: "DFDA_OPEX_REGULATORY_assumption_reasonable",
          type: "rating",
          question: "Is this assumption reasonable: Decentralized Framework for Drug Assessment Regulatory Coordination Costs = $5M",
          options: [
            "1 (Unreasonable)",
            "2 (Questionable)",
            "3 (Acceptable)",
            "4 (Reasonable)",
            "5 (Very reasonable)",
            "Not qualified to assess"
          ],
        },
        {
          id: "DFDA_OPEX_REGULATORY_alternative_value",
          type: "text",
          question: "What value would you use instead? (Current: $5M)",
        },
        {
          id: "DFDA_OPEX_REGULATORY_confidence_interval",
          type: "range",
          question: "The model uses a 90% confidence interval of [$3M, $8M]. What is your 90% CI?",
          options: [
            "Lower bound",
            "Upper bound"
          ],
        }
      ],
    },
    {
      rank: 18,
      name: "DFDA_OPEX_COMMUNITY",
      displayName: "Decentralized Framework for Drug Assessment Community Support Costs",
      value: 0,
      formattedValue: "0",
      sourceType: "definition",
      description: "Decentralized Framework for Drug Assessment community support costs",
      questions: [
        {
          id: "DFDA_OPEX_COMMUNITY_assumption_reasonable",
          type: "rating",
          question: "Is this assumption reasonable: Decentralized Framework for Drug Assessment Community Support Costs = $2M",
          options: [
            "1 (Unreasonable)",
            "2 (Questionable)",
            "3 (Acceptable)",
            "4 (Reasonable)",
            "5 (Very reasonable)",
            "Not qualified to assess"
          ],
        },
        {
          id: "DFDA_OPEX_COMMUNITY_alternative_value",
          type: "text",
          question: "What value would you use instead? (Current: $2M)",
        },
        {
          id: "DFDA_OPEX_COMMUNITY_confidence_interval",
          type: "range",
          question: "The model uses a 90% confidence interval of [$1M, $3M]. What is your 90% CI?",
          options: [
            "Lower bound",
            "Upper bound"
          ],
        }
      ],
    },
    {
      rank: 19,
      name: "DFDA_ANNUAL_OPEX",
      displayName: "Total Annual Decentralized Framework for Drug Assessment Operational Costs",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "Total annual Decentralized Framework for Drug Assessment operational costs (sum of all components: $15M + $10M + $8M + $5M + $2M)",
      questions: [
        {
          id: "DFDA_ANNUAL_OPEX_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **Total Annual Decentralized Framework for Drug Assessment Operational Costs**?\n\n**Current result:** $40M\n**Calculation:** $15M + $10M + $8M + $5M + $2M = $40M",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "DFDA_ANNUAL_OPEX_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Decentralized Framework for Drug Assessment Maintenance Costs: $15M\n• Decentralized Framework for Drug Assessment Staff Costs: $10M\n• Decentralized Framework for Drug Assessment Infrastructure Costs: $8M\n• Decentralized Framework for Drug Assessment Regulatory Coordination Costs: $5M\n• Decentralized Framework for Drug Assessment Community Support Costs: $2M",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "DFDA_ANNUAL_OPEX_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    },
    {
      rank: 20,
      name: "NPV_DISCOUNT_RATE_STANDARD",
      displayName: "Standard Discount Rate for NPV Analysis",
      value: 0,
      formattedValue: "0",
      sourceType: "definition",
      description: "Standard discount rate for NPV analysis (3% annual, social discount rate)",
      questions: [
        {
          id: "NPV_DISCOUNT_RATE_STANDARD_assumption_reasonable",
          type: "rating",
          question: "Is this assumption reasonable: Standard Discount Rate for NPV Analysis = 3%",
          options: [
            "1 (Unreasonable)",
            "2 (Questionable)",
            "3 (Acceptable)",
            "4 (Reasonable)",
            "5 (Very reasonable)",
            "Not qualified to assess"
          ],
        },
        {
          id: "NPV_DISCOUNT_RATE_STANDARD_alternative_value",
          type: "text",
          question: "What value would you use instead? (Current: 3%)",
        }
      ],
    },
    {
      rank: 21,
      name: "DFDA_ROI_RD_ONLY",
      displayName: "ROI from Decentralized Framework for Drug Assessment R&D Savings Only",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "ROI from Decentralized Framework for Drug Assessment R&D savings only (10-year NPV, most conservative estimate)",
      questions: [
        {
          id: "DFDA_ROI_RD_ONLY_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **ROI from Decentralized Framework for Drug Assessment R&D Savings Only**?\n\n**Current result:** 451 ratiox ROI\n**Calculation:** NPV_BENEFIT ÷ NPV_TOTAL_COST = 451 ratio",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "DFDA_ROI_RD_ONLY_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Decentralized Framework for Drug Assessment Annual Benefit: $41.5B\n• Total Annual Decentralized Framework for Drug Assessment Operational Costs: $40M\n• Standard Discount Rate for NPV Analysis: 3%\n• Decentralized Framework for Drug Assessment Total NPV Upfront Costs: $270M",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "DFDA_ROI_RD_ONLY_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    },
    {
      rank: 22,
      name: "STANDARD_ECONOMIC_QALY_VALUE_USD",
      displayName: "Standard Economic Value per QALY",
      value: 0,
      formattedValue: "0",
      sourceType: "external",
      description: "Standard economic value per QALY",
      citation: {
        id: "qaly-value",
        title: "Value per QALY (standard economic value)",
        author: "ICER",
        year: "2024",
        source: "ICER",
        url: "https://icer.org/wp-content/uploads/2024/02/Reference-Case-4.3.25.pdf",
      },
      questions: [
        {
          id: "STANDARD_ECONOMIC_QALY_VALUE_USD_source_credibility",
          type: "rating",
          question: "Rate the credibility of this source for estimating: Standard Economic Value per QALY",
          options: [
            "1 (Not credible)",
            "2",
            "3 (Somewhat credible)",
            "4",
            "5 (Highly credible)",
            "Not qualified to assess"
          ],
        },
        {
          id: "STANDARD_ECONOMIC_QALY_VALUE_USD_value_reasonable",
          type: "boolean",
          question: "Is the central estimate of $150K reasonable?",
          options: [
            "Yes",
            "No"
          ],
        },
        {
          id: "STANDARD_ECONOMIC_QALY_VALUE_USD_better_source",
          type: "text",
          question: "Do you know of a better or more recent source?",
        }
      ],
    },
    {
      rank: 23,
      name: "TREATY_COMPLETE_ROI_ALL_BENEFITS",
      displayName: "Treaty ROI - Lag Elimination (PRIMARY)",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "Treaty ROI based on eliminating the 8.2-year post-safety efficacy lag (PRIMARY METHODOLOGY). Total one-time benefit from disease eradication delay elimination divided by $1B campaign cost. This is the primary ROI estimate for total health benefits.",
      questions: [
        {
          id: "TREATY_COMPLETE_ROI_ALL_BENEFITS_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **Treaty ROI - Lag Elimination (PRIMARY)**?\n\n**Current result:** 1.19M ratiox ROI\n**Calculation:** DISEASE_ERADICATION_DELAY_TOTAL ÷ CAMPAIGN_COST = 1.19M ratio",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "TREATY_COMPLETE_ROI_ALL_BENEFITS_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Total DALYs Lost from Disease Eradication Delay: 7.94B DALYs\n• Standard Economic Value per QALY: $150K\n• Total 1% Treaty Campaign Cost: $1B",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "TREATY_COMPLETE_ROI_ALL_BENEFITS_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    },
    {
      rank: 24,
      name: "TREATY_ROI_LAG_ELIMINATION",
      displayName: "Treaty ROI - Lag Elimination (PRIMARY)",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "Treaty ROI based on eliminating the 8.2-year post-safety efficacy lag (PRIMARY METHODOLOGY). Total one-time benefit from disease eradication delay elimination divided by $1B campaign cost. This is the primary ROI estimate for total health benefits.",
      questions: [
        {
          id: "TREATY_ROI_LAG_ELIMINATION_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **Treaty ROI - Lag Elimination (PRIMARY)**?\n\n**Current result:** 1.19M ratiox ROI\n**Calculation:** DISEASE_ERADICATION_DELAY_TOTAL ÷ CAMPAIGN_COST = 1.19M ratio",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "TREATY_ROI_LAG_ELIMINATION_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Total DALYs Lost from Disease Eradication Delay: 7.94B DALYs\n• Standard Economic Value per QALY: $150K\n• Total 1% Treaty Campaign Cost: $1B",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "TREATY_ROI_LAG_ELIMINATION_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    },
    {
      rank: 25,
      name: "DFDA_EXPECTED_ROI",
      displayName: "Expected Treaty ROI (Risk-Adjusted)",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "Expected ROI for 1% treaty accounting for political success probability uncertainty. Monte Carlo samples POLITICAL_SUCCESS_PROBABILITY from beta(0.1%, 10%) distribution to generate full expected value distribution. Central value uses 1% probability.",
      questions: [
        {
          id: "DFDA_EXPECTED_ROI_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **Expected Treaty ROI (Risk-Adjusted)**?\n\n**Current result:** 11.9kx ROI\n**Calculation:** 1.19M ratio × 1% = 11.9k",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "DFDA_EXPECTED_ROI_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Treaty ROI - Lag Elimination (PRIMARY): 1.19M ratio\n• Political Success Probability: 1%",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "DFDA_EXPECTED_ROI_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    },
    {
      rank: 26,
      name: "CURRENT_TRIAL_SLOTS_AVAILABLE",
      displayName: "Annual Global Clinical Trial Participants",
      value: 0,
      formattedValue: "0",
      sourceType: "external",
      description: "Annual global clinical trial participants (IQVIA 2022: 1.9M post-COVID normalization)",
      citation: {
        id: "global-trial-participant-capacity",
        title: "Global trial capacity",
        author: "IQVIA Report",
        source: "IQVIA Report: Clinical Trial Subjects Number Drops Due to Decline in COVID-19 Enrollment",
        url: "https://gmdpacademy.org/news/iqvia-report-clinical-trial-subjects-number-drops-due-to-decline-in-covid-19-enrollment/",
      },
      questions: [
        {
          id: "CURRENT_TRIAL_SLOTS_AVAILABLE_source_credibility",
          type: "rating",
          question: "Rate the credibility of this source for estimating: Annual Global Clinical Trial Participants",
          options: [
            "1 (Not credible)",
            "2",
            "3 (Somewhat credible)",
            "4",
            "5 (Highly credible)",
            "Not qualified to assess"
          ],
        },
        {
          id: "CURRENT_TRIAL_SLOTS_AVAILABLE_value_reasonable",
          type: "boolean",
          question: "Is the central estimate of 1.90M patients/year reasonable?",
          options: [
            "Yes",
            "No"
          ],
        },
        {
          id: "CURRENT_TRIAL_SLOTS_AVAILABLE_better_source",
          type: "text",
          question: "Do you know of a better or more recent source?",
        },
        {
          id: "CURRENT_TRIAL_SLOTS_AVAILABLE_confidence_interval",
          type: "range",
          question: "The model uses a 90% confidence interval of [1.50M patients/year, 2.30M patients/year]. What is your 90% CI?",
          options: [
            "Lower bound",
            "Upper bound"
          ],
        }
      ],
    },
    {
      rank: 27,
      name: "IAB_POLITICAL_INCENTIVE_FUNDING_PCT",
      displayName: "IAB Political Incentive Funding Percentage",
      value: 0,
      formattedValue: "0",
      sourceType: "definition",
      description: "Percentage of treaty funding allocated to Incentive Alignment Bond mechanism for political incentives (independent expenditures/PACs, post-office fellowships, Public Good Score infrastructure)",
      questions: [
        {
          id: "IAB_POLITICAL_INCENTIVE_FUNDING_PCT_assumption_reasonable",
          type: "rating",
          question: "Is this assumption reasonable: IAB Political Incentive Funding Percentage = 10%",
          options: [
            "1 (Unreasonable)",
            "2 (Questionable)",
            "3 (Acceptable)",
            "4 (Reasonable)",
            "5 (Very reasonable)",
            "Not qualified to assess"
          ],
        },
        {
          id: "IAB_POLITICAL_INCENTIVE_FUNDING_PCT_alternative_value",
          type: "text",
          question: "What value would you use instead? (Current: 10%)",
        }
      ],
    },
    {
      rank: 28,
      name: "IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL",
      displayName: "Annual IAB Political Incentive Funding",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "Annual funding for IAB political incentive mechanism (independent expenditures supporting high-scoring politicians, post-office fellowship endowments, Public Good Score infrastructure)",
      questions: [
        {
          id: "IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **Annual IAB Political Incentive Funding**?\n\n**Current result:** $2.72B\n**Calculation:** TREATY_FUNDING × IAB_POLITICAL_INCENTIVE_PCT = $2.72B",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Annual Funding from 1% of Global Military Spending Redirected to DIH: $27.2B\n• IAB Political Incentive Funding Percentage: 10%",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    },
    {
      rank: 29,
      name: "DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL",
      displayName: "Annual Funding for Pragmatic Clinical Trials",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "Annual funding for pragmatic clinical trials (treaty funding minus VICTORY Incentive Alignment Bond payouts and IAB political incentive mechanism)",
      questions: [
        {
          id: "DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **Annual Funding for Pragmatic Clinical Trials**?\n\n**Current result:** $21.7B\n**Calculation:** TREATY_FUNDING - BOND_PAYOUT - IAB_POLITICAL_INCENTIVE_FUNDING = $21.7B",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Annual Funding from 1% of Global Military Spending Redirected to DIH: $27.2B\n• Annual VICTORY Incentive Alignment Bond Payout: $2.72B\n• Annual IAB Political Incentive Funding: $2.72B",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    },
    {
      rank: 30,
      name: "DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL",
      displayName: "Annual Clinical Trial Patient Subsidies",
      value: 0,
      formattedValue: "0",
      sourceType: "calculated",
      description: "Annual clinical trial patient subsidies (all medical research funds after Decentralized Framework for Drug Assessment operations)",
      questions: [
        {
          id: "DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL_formula_sound",
          type: "choice",
          question: "Is the calculation methodology sound for: **Annual Clinical Trial Patient Subsidies**?\n\n**Current result:** $21.7B\n**Calculation:** MEDICAL_RESEARCH_FUNDING - DFDA_OPEX = $21.7B",
          options: [
            "Yes - formula is appropriate",
            "No - wrong functional form",
            "No - missing key factors",
            "No - includes inappropriate factors",
            "Unsure - need more detail"
          ],
        },
        {
          id: "DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL_inputs_appropriate",
          type: "checklist",
          question: "Are these input factors appropriate?\n\n**Inputs:**\n• Total Annual Decentralized Framework for Drug Assessment Operational Costs: $40M\n• Annual Funding for Pragmatic Clinical Trials: $21.7B",
          options: [
            "All inputs are appropriate",
            "Missing critical factors",
            "Includes inappropriate factors",
            "Potential overlap between factors",
            "Other issue (specify in comments)"
          ],
        },
        {
          id: "DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL_missing_factors",
          type: "text",
          question: "What important factors are missing from this calculation?",
        }
      ],
    }
  ],
};

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Get parameter by rank
 */
export function getParameterByRank(rank: number): SurveyParameter | undefined {
  return economistSurvey.parameters.find(p => p.rank === rank);
}

/**
 * Get parameter by name
 */
export function getParameterByName(name: string): SurveyParameter | undefined {
  return economistSurvey.parameters.find(p => p.name === name);
}

/**
 * Get all parameters of a specific source type
 */
export function getParametersByType(sourceType: SourceType): SurveyParameter[] {
  return economistSurvey.parameters.filter(p => p.sourceType === sourceType);
}

/**
 * Get total number of questions
 */
export function getTotalQuestions(): number {
  return economistSurvey.parameters.reduce((sum, p) => sum + p.questions.length, 0);
}

/**
 * Calculate completion percentage
 */
export function getCompletionPercentage(currentRank: number): number {
  const total = economistSurvey.metadata.parameterCount;
  return Math.round((currentRank / total) * 100);
}

/**
 * Get questions for a specific parameter
 */
export function getQuestionsForParameter(paramName: string): SurveyQuestion[] {
  const param = getParameterByName(paramName);
  return param?.questions || [];
}

/**
 * Check if parameter has citation
 */
export function hasCitation(param: SurveyParameter): boolean {
  return !!param.citation;
}
