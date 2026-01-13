#!/usr/bin/env python3
"""
LATEX SYMBOL REVIEW FILE
========================

This file contains suggested latex_symbol values for all parameters.

HOW TO USE:
1. Review the SYMBOLS dict below
2. Edit any symbols that look wrong or could be improved
3. Set symbols to None to skip (keep auto-generated)
4. Run: python scripts/apply-latex-symbols.py

SYMBOL GUIDELINES:
- Use subscripts for context: Cost_{platform}, OPEX_{dFDA}
- Keep it short but meaningful
- Use \\text{} for multi-letter words: \\text{OPEX}_{total}
- Common patterns:
    Cost_{X}, Benefit_{X}, ROI_{X}
    Deaths_{cause}, DALYs_{source}
    Years_{context}, Rate_{what}
"""

# Parameters that already have latex_symbol (for reference)
EXISTING_SYMBOLS = {
    # Total annual Decentralized Framework for Drug Assessment operational costs (sum 
    "DFDA_ANNUAL_OPEX": r"OPEX_{dFDA}",
    # Decentralized Framework for Drug Assessment community support costs
    "DFDA_OPEX_COMMUNITY": r"Cost_{community}",
    # Decentralized Framework for Drug Assessment infrastructure costs (cloud, securit
    "DFDA_OPEX_INFRASTRUCTURE": r"Cost_{infra}",
    # Decentralized Framework for Drug Assessment maintenance costs
    "DFDA_OPEX_PLATFORM_MAINTENANCE": r"Cost_{platform}",
    # Decentralized Framework for Drug Assessment regulatory coordination costs
    "DFDA_OPEX_REGULATORY": r"Cost_{regulatory}",
    # Decentralized Framework for Drug Assessment staff costs (minimal, AI-assisted)
    "DFDA_OPEX_STAFF": r"Cost_{staff}",
    # Annual funding from 1% of global military spending redirected to DIH
    "TREATY_ANNUAL_FUNDING": r"Funding_{treaty}",
}

# Parameters needing latex_symbol - REVIEW AND EDIT THESE
# Set to None to skip (use auto-generated symbol)
# Format: "PARAM_NAME": r"Symbol_{subscript}",
SYMBOLS = {

    # ADAPTABLE (3)
    "ADAPTABLE_TRIAL_COST_PER_PATIENT": r"Cost",
    "ADAPTABLE_TRIAL_PATIENTS": r"Patients",
    "ADAPTABLE_TRIAL_TOTAL_COST": r"Cost_{total}",

    # ADDITIONAL (1)
    "ADDITIONAL_DRUGS_FROM_COST_ELIMINATION": r"Cost",

    # ANTIDEPRESSANT (1)
    "ANTIDEPRESSANT_TRIAL_EXCLUSION_RATE": r"Rate",

    # APPROVED (1)
    "APPROVED_DRUG_DISEASE_PAIRINGS": r"Approved",

    # AVERAGE (2)
    "AVERAGE_MARKET_RETURN_PCT": r"Average",
    "AVERAGE_US_HOURLY_WAGE": r"Hours",

    # BASELINE (1)
    "BASELINE_LIVES_SAVED_ANNUAL": r"Lives_{ann}",

    # BED (1)
    "BED_NETS_COST_PER_DALY": r"Cost_{net}",

    # BOOK (1)
    "BOOK_READING_SPEED_WPM": r"Book",

    # CAMPAIGN (27)
    "CAMPAIGN_CELEBRITY_ENDORSEMENT": r"Campaign_{camp}",
    "CAMPAIGN_COMMUNITY_ORGANIZING": r"Campaign_{community}",
    "CAMPAIGN_CONTINGENCY": r"Cost_{camp}",
    "CAMPAIGN_DEFENSE_CONVERSION": r"Campaign_{camp}",
    "CAMPAIGN_DEFENSE_LOBBYIST_BUDGET": r"Campaign_{camp}",
    "CAMPAIGN_HEALTHCARE_ALIGNMENT": r"Campaign_{camp,health}",
    "CAMPAIGN_INFRASTRUCTURE": r"Ratio_{infra}",
    "CAMPAIGN_LEGAL_AI_BUDGET": r"Campaign_{camp}",
    "CAMPAIGN_LEGAL_DEFENSE": r"Campaign_{camp}",
    "CAMPAIGN_LEGAL_WORK": r"Campaign_{camp}",
    "CAMPAIGN_LOBBYING_EU": r"Campaign_{camp}",
    "CAMPAIGN_LOBBYING_G20_MILLIONS": r"Campaign_{camp}",
    "CAMPAIGN_LOBBYING_US": r"Campaign_{camp}",
    "CAMPAIGN_MEDIA_BUDGET_MAX": r"Campaign_{camp}",
    "CAMPAIGN_MEDIA_BUDGET_MIN": r"Campaign_{camp}",
    "CAMPAIGN_OPPOSITION_RESEARCH": r"Campaign_{camp,RD}",
    "CAMPAIGN_PHASE1_BUDGET": r"Campaign_{camp}",
    "CAMPAIGN_PHASE2_BUDGET": r"Campaign_{camp}",
    "CAMPAIGN_PILOT_PROGRAMS": r"Campaign_{camp}",
    "CAMPAIGN_PLATFORM_DEVELOPMENT": r"Campaign_{platform}",
    "CAMPAIGN_REGULATORY_NAVIGATION": r"Campaign_{reg}",
    "CAMPAIGN_SCALING_PREP": r"Ratio_{camp}",
    "CAMPAIGN_STAFF_BUDGET": r"Campaign_{staff}",
    "CAMPAIGN_SUPER_PAC_BUDGET": r"Campaign_{camp}",
    "CAMPAIGN_TECH_PARTNERSHIPS": r"Campaign_{camp}",
    "CAMPAIGN_TREATY_IMPLEMENTATION": r"Campaign_{camp,treaty}",
    "CAMPAIGN_VIRAL_CONTENT_BUDGET": r"Campaign_{camp}",

    # CAREGIVER (5)
    "CAREGIVER_ANNUAL_VALUE_TOTAL": r"Caregiver_{annual}",
    "CAREGIVER_COST_ANNUAL": r"Cost_{ann}",
    "CAREGIVER_COUNT_US": r"CaregiverUS",
    "CAREGIVER_HOURS_PER_MONTH": r"Hours",
    "CAREGIVER_VALUE_PER_HOUR_SIMPLE": r"Cost",

    # CELL (2)
    "CELL_THERAPY_APPROACHES": r"Cell",
    "CELL_THERAPY_DISEASE_COMBINATIONS": r"Cell",

    # CHILDHOOD (3)
    "CHILDHOOD_VACCINATION_ANNUAL_BENEFIT": r"Benefit_{ann}",
    "CHILDHOOD_VACCINATION_COST_PER_DALY": r"Cost",
    "CHILDHOOD_VACCINATION_ROI": r"ROI",

    # CHRONIC (1)
    "CHRONIC_DISEASE_DISABILITY_WEIGHT": r"Chronic",

    # CLINICAL (2)
    "CLINICAL_TRIAL_COST_PER_APPROVED_DRUG": r"Cost",
    "CLINICAL_TRIAL_COST_PER_PARTICIPANT_ANNUAL": r"Cost_{ann}",

    # COMBINATION (2)
    "COMBINATION_THERAPY_DISEASE_SPACE": r"Combination",
    "COMBINATION_THERAPY_PAIRS": r"Combination",

    # COMBINED (1)
    "COMBINED_PEACE_HEALTH_DIVIDENDS_ANNUAL_FOR_ROI_CALC": r"Dividend_{ann}",

    # CONCENTRATED (1)
    "CONCENTRATED_INTEREST_SECTOR_MARKET_CAP_USD": r"Rate",

    # CPI (1)
    "CPI_MULTIPLIER_1980_TO_2024": r"Multiplier_{80s}",

    # CURRENT (11)
    "CURRENT_ACTIVE_TRIALS": r"Time_{curr}",
    "CURRENT_CLINICAL_TRIAL_PARTICIPATION_RATE": r"Rate_{curr}",
    "CURRENT_COMBINATION_EXPLORATION_YEARS": r"Ratio_{curr}",
    "CURRENT_DISEASE_PATIENTS_GLOBAL": r"Population_{curr,global}",
    "CURRENT_DRUG_APPROVALS_PER_YEAR": r"Drug_{current}",
    "CURRENT_KNOWN_SAFE_EXPLORATION_YEARS": r"Ratio_{curr}",
    "CURRENT_PATIENT_PARTICIPATION_RATE": r"Rate_{curr}",
    "CURRENT_TOTAL_EXPLORATION_YEARS": r"Ratio_{curr,total}",
    "CURRENT_TRIALS_PER_YEAR": r"Trials_{curr}",
    "CURRENT_TRIAL_ABANDONMENT_RATE": r"Rate_{curr}",
    "CURRENT_TRIAL_SLOTS_AVAILABLE": r"Trials_{curr}",

    # DCT (1)
    "DCT_PLATFORM_FUNDING_MEDIUM": r"Funding_{platform}",

    # DEFENSE (2)
    "DEFENSE_LOBBYING_ANNUAL": r"Spending_{ann}",
    "DEFENSE_SECTOR_RETENTION_PCT": r"Defense",

    # DEWORMING (1)
    "DEWORMING_COST_PER_DALY": r"Cost",

    # DFDA (46)
    "DFDA_BENEFIT_RD_ONLY_ANNUAL": r"Benefit_{DFDA,ann}",
    "DFDA_COMBINED_TREATMENT_SPEEDUP_MULTIPLIER": r"Multiplier_{DFDA}",
    "DFDA_DIRECT_FUNDING_COST_PER_DALY": r"Cost_{direct,DFDA}",
    "DFDA_DIRECT_FUNDING_QUEUE_CLEARANCE_NPV": r"Funding_{direct,DFDA}",
    "DFDA_DIRECT_FUNDING_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG": r"Increase_{direct_funding,DFDA}",
    "DFDA_DIRECT_FUNDING_VS_BED_NETS_MULTIPLIER": r"Multiplier_{direct,DFDA}",
    "DFDA_EFFICACY_LAG_ELIMINATION_DALYS": r"DALYs_{DFDA}",
    "DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED": r"Deaths_{DFDA}",
    "DFDA_EFFICACY_LAG_ELIMINATION_ECONOMIC_VALUE": r"Delay_{DFDA}",
    "DFDA_EFFICACY_LAG_ELIMINATION_YLD": r"Delay_{DFDA}",
    "DFDA_EFFICACY_LAG_ELIMINATION_YLL": r"Delay_{DFDA}",
    "DFDA_FIRST_TREATMENTS_PER_YEAR": r"DFDA",
    "DFDA_KNOWN_SAFE_EXPLORATION_YEARS": r"Ratio_{DFDA}",
    "DFDA_NET_SAVINGS_RD_ONLY_ANNUAL": r"Savings_{net,ann}",
    "DFDA_NPV_ADOPTION_RAMP_YEARS": r"DFDANPV",
    "DFDA_NPV_ANNUAL_OPEX": r"OPEX_{DFDA,ann}",
    "DFDA_NPV_ANNUAL_OPEX_TOTAL": r"OPEX_{DFDA,total}",
    "DFDA_NPV_BENEFIT_RD_ONLY": r"Benefit_{DFDA,RD}",
    "DFDA_NPV_NET_BENEFIT_RD_ONLY": r"Benefit_{net,RD}",
    "DFDA_NPV_PV_ANNUAL_OPEX": r"OPEX_{DFDA,ann}",
    "DFDA_NPV_TOTAL_COST": r"Cost_{DFDA,total}",
    "DFDA_NPV_UPFRONT_COST": r"Cost_{DFDA,NPV}",
    "DFDA_NPV_UPFRONT_COST_TOTAL": r"Cost_{DFDA,total}",
    "DFDA_OPEX_PCT_OF_TREATY_FUNDING": r"OPEX_{DFDA,treaty}",
    "DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT": r"Cost_{DFDA}",
    "DFDA_QUEUE_CLEARANCE_YEARS": r"Time_{DFDA}",
    "DFDA_RD_SAVINGS_DAILY": r"Cost_{DFDA,daily}",
    "DFDA_ROI_RD_ONLY": r"Savings_{DFDA,RD}",
    "DFDA_TARGET_COST_PER_PATIENT_USD": r"Cost_{DFDA}",
    "DFDA_TOTAL_EXPLORATION_YEARS": r"Ratio_{DFDA,total}",
    "DFDA_TRIALS_PER_YEAR_CAPACITY": r"Capacity_{DFDA}",
    "DFDA_TRIAL_CAPACITY_DALYS_AVERTED": r"Increase_{DFDA}",
    "DFDA_TRIAL_CAPACITY_ECONOMIC_VALUE": r"Increase_{DFDA}",
    "DFDA_TRIAL_CAPACITY_LIVES_SAVED": r"Increase_{DFDA}",
    "DFDA_TRIAL_CAPACITY_MULTIPLIER": r"Multiplier_{DFDA}",
    "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS": r"DALYs_{max,DFDA}",
    "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE": r"Benefit_{max,DFDA}",
    "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED": r"Capacity_{max,DFDA}",
    "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS": r"Capacity_{max,DFDA}",
    "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS": r"Capacity_{max,DFDA}",
    "DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS": r"Ratio_{DFDA}",
    "DFDA_TRIAL_COST_REDUCTION_FACTOR": r"Cost_{DFDA}",
    "DFDA_TRIAL_COST_REDUCTION_PCT": r"Reduction_{DFDA}",
    "DFDA_UPFRONT_BUILD": r"Cost_{DFDA}",
    "DFDA_UPFRONT_BUILD_MAX": r"Cost_{DFDA}",
    "DFDA_VALLEY_OF_DEATH_RESCUE_MULTIPLIER": r"Multiplier_{DFDA}",

    # DIH (7)
    "DIH_NPV_ANNUAL_OPEX_INITIATIVES": r"OPEX_{opex,ann}",
    "DIH_NPV_UPFRONT_COST_INITIATIVES": r"Cost_{NPV}",
    "DIH_PATIENTS_FUNDABLE_ANNUALLY": r"Fundable_{ann}",
    "DIH_TREASURY_MEDICAL_RESEARCH_PCT": r"Treasury_{RD}",
    "DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL": r"Treasury_{ann}",
    "DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL": r"Treasury_{ann}",
    "DIH_TREASURY_TRIAL_SUBSIDIES_PCT": r"Treasury",

    # DISEASE (3)
    "DISEASE_RELATED_CAREGIVER_PCT": r"Disease",
    "DISEASE_VS_TERRORISM_DEATHS_RATIO": r"Deaths_{terror,dis}",
    "DISEASE_VS_WAR_DEATHS_RATIO": r"Deaths_{war}",

    # DISEASES (1)
    "DISEASES_WITHOUT_EFFECTIVE_TREATMENT": r"Diseases",

    # DIVIDEND (1)
    "DIVIDEND_COVERAGE_FACTOR": r"OPEX",

    # DRUG (5)
    "DRUG_COST_INCREASE_1980S_TO_CURRENT_MULTIPLIER": r"Multiplier_{curr}",
    "DRUG_COST_INCREASE_PRE1962_TO_CURRENT_MULTIPLIER": r"Multiplier_{curr}",
    "DRUG_DEVELOPMENT_COST_1980S": r"Cost_{80s}",
    "DRUG_DISEASE_COMBINATIONS_POSSIBLE": r"Drug",
    "DRUG_REPURPOSING_SUCCESS_RATE": r"Rate",

    # ECONOMIC (4)
    "ECONOMIC_MULTIPLIER_EDUCATION_INVESTMENT": r"Multiplier_{edu}",
    "ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT": r"Multiplier_{health}",
    "ECONOMIC_MULTIPLIER_INFRASTRUCTURE_INVESTMENT": r"Multiplier_{infra}",
    "ECONOMIC_MULTIPLIER_MILITARY_SPENDING": r"Multiplier_{mil}",

    # EFFECTIVE (1)
    "EFFECTIVE_HOURLY_RATE_LIFETIME_BENEFIT": r"Benefit",

    # EFFICACY (1)
    "EFFICACY_LAG_YEARS": r"Delay",

    # EMERGING (1)
    "EMERGING_MODALITY_COMBINATIONS": r"Emerging",

    # EPIGENETIC (2)
    "EPIGENETIC_DISEASE_COMBINATIONS": r"Epigenetic",
    "EPIGENETIC_TARGETS_COUNT": r"Epigenetic",

    # EVENTUALLY (2)
    "EVENTUALLY_AVOIDABLE_DALY_PCT": r"DALYs",
    "EVENTUALLY_AVOIDABLE_DEATH_PCT": r"Deaths",

    # EXISTING (2)
    "EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL": r"Deaths_{total}",
    "EXISTING_DRUGS_EFFICACY_LAG_ECONOMIC_LOSS": r"Delay",

    # EXPLORATION (1)
    "EXPLORATION_RATIO": r"Ratio",

    # FAMILY (1)
    "FAMILY_OFFICE_INVESTMENT_MIN": r"Family",

    # FDA (5)
    "FDA_APPROVED_PRODUCTS_COUNT": r"FDA",
    "FDA_APPROVED_UNIQUE_ACTIVE_INGREDIENTS": r"FDA",
    "FDA_GRAS_SUBSTANCES_COUNT": r"FDA",
    "FDA_PHASE_1_TO_APPROVAL_YEARS": r"Time",
    "FDA_TO_OXFORD_RECOVERY_TRIAL_TIME_MULTIPLIER": r"Multiplier_{RD}",

    # FUNDAMENTALLY (1)
    "FUNDAMENTALLY_UNAVOIDABLE_DEATH_PCT": r"Deaths",

    # GENE (1)
    "GENE_THERAPY_DISEASE_COMBINATIONS": r"Gene",

    # GIVEWELL (3)
    "GIVEWELL_COST_PER_LIFE_AVG": r"Cost",
    "GIVEWELL_COST_PER_LIFE_MAX": r"Cost",
    "GIVEWELL_COST_PER_LIFE_MIN": r"Cost",

    # GLOBAL (54)
    "GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT": r"Deaths_{combat,ann}",
    "GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE": r"Deaths_{state,ann}",
    "GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS": r"Deaths_{terror,ann}",
    "GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL": r"Deaths_{total}",
    "GLOBAL_ANNUAL_DALY_BURDEN": r"DALYs_{ann}",
    "GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES": r"Deaths_{ann}",
    "GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST": r"Cost_{indirect,ann}",
    "GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT": r"Cost_{env,ann}",
    "GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT": r"Cost_{combat,ann}",
    "GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE": r"Cost_{state,ann}",
    "GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS": r"Cost_{terror,ann}",
    "GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT": r"Loss_{human,ann}",
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT": r"Damage_{comms,ann}",
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT": r"Damage_{edu,ann}",
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT": r"Damage_{energy,ann}",
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT": r"Damage_{health,ann}",
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT": r"Damage_{transport,ann}",
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT": r"Damage_{water,ann}",
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT": r"Infrastructure_{global}",
    "GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH": r"Lives_{ann}",
    "GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING": r"Cost_{econ_growth,ann}",
    "GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT": r"Lost_{global}",
    "GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT": r"Cost_{ann}",
    "GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS": r"Cost_{ref,ann}",
    "GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT": r"Disruption_{trade,ann}",
    "GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT": r"Cost_{currency,ann}",
    "GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT": r"Cost_{trade,ann}",
    "GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT": r"Cost_{shipping,ann}",
    "GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT": r"Cost_{trade,ann}",
    "GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS": r"Cost_{vet,ann}",
    "GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL": r"Cost_{direct,total}",
    "GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL": r"Cost_{indirect,total}",
    "GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL": r"Trials_{ann}",
    "GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL": r"Cost_{ann}",
    "GLOBAL_DISEASE_DEATHS_DAILY": r"Deaths_{daily}",
    "GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL": r"Cost_{direct,ann}",
    "GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL": r"Burden_{ann}",
    "GLOBAL_DISEASE_HUMAN_LIFE_VALUE_LOSS_ANNUAL": r"Loss_{human,ann}",
    "GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL": r"Loss_{ann}",
    "GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL": r"Trials_{ann}",
    "GLOBAL_HOUSEHOLD_WEALTH_USD": r"Household_{global}",
    "GLOBAL_INDUSTRY_CLINICAL_TRIALS_SPENDING_ANNUAL": r"Trials_{ann}",
    "GLOBAL_LIFE_EXPECTANCY_2024": r"Life_{global}",
    "GLOBAL_MED_RESEARCH_SPENDING": r"Spending_{global}",
    "GLOBAL_MILITARY_SPENDING_ANNUAL_2024": r"Spending_{mil,ann}",
    "GLOBAL_MILITARY_SPENDING_PER_CAPITA_ANNUAL": r"Spending_{percap,ann}",
    "GLOBAL_MILITARY_SPENDING_POST_TREATY_ANNUAL_2024": r"Spending_{mil,ann}",
    "GLOBAL_NONPROFIT_CLINICAL_TRIALS_SPENDING_ANNUAL": r"Trials_{ann}",
    "GLOBAL_PHARMA_RD_SPENDING_ANNUAL": r"Spending_{ann}",
    "GLOBAL_POPULATION_2024": r"Population_{global}",
    "GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT": r"Threshold_{global}",
    "GLOBAL_SYMPTOMATIC_DISEASE_TREATMENT_ANNUAL": r"Spending_{sympt,ann}",
    "GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL": r"Cost_{total}",
    "GLOBAL_YLD_PROPORTION_OF_DALYS": r"DALYs_{global}",

    # HUMAN (3)
    "HUMAN_GENOME_PROJECT_TOTAL_ECONOMIC_IMPACT": r"Human_{total}",
    "HUMAN_INTERACTOME_TARGETED_PCT": r"Human",
    "HUMAN_PROTEIN_CODING_GENES": r"Human",

    # IAB (7)
    "IAB_BOOTSTRAP_CAMPAIGN_COST_BASE_USD": r"Cost_{camp}",
    "IAB_BOOTSTRAP_CAMPAIGN_COST_CONSERVATIVE_USD": r"Cost_{camp}",
    "IAB_BOOTSTRAP_CAMPAIGN_COST_OPTIMISTIC_USD": r"Cost_{camp}",
    "IAB_MECHANISM_ANNUAL_COST": r"Cost_{ann}",
    "IAB_MECHANISM_BENEFIT_COST_RATIO": r"Cost",
    "IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL": r"Funding_{ann}",
    "IAB_POLITICAL_INCENTIVE_FUNDING_PCT": r"Funding",

    # ICD (1)
    "ICD_10_TOTAL_CODES": r"Icd_{total}",

    # INDUSTRY (1)
    "INDUSTRY_VS_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO": r"Ratio",

    # INSTITUTIONAL (1)
    "INSTITUTIONAL_INVESTOR_MIN": r"Institutional",

    # LIFE (3)
    "LIFE_EXPECTANCY_GAIN_1883_1962_YEARS_PER_DECADE": r"Rate",
    "LIFE_EXPECTANCY_GAIN_1962_2019_YEARS_PER_DECADE": r"Rate",
    "LIFE_EXTENSION_YEARS": r"Ratio",

    # LOBBYIST (3)
    "LOBBYIST_BOND_INVESTMENT_MAX": r"Lobbyist",
    "LOBBYIST_SALARY_MAX": r"Lobbyist",
    "LOBBYIST_SALARY_MIN_K": r"Lobbyist",

    # MEASLES (1)
    "MEASLES_VACCINATION_ROI": r"ROI",

    # MEDICAL (1)
    "MEDICAL_RESEARCH_PCT_OF_DISEASE_BURDEN": r"Burden_{RD}",

    # MENTAL (1)
    "MENTAL_HEALTH_PRODUCTIVITY_LOSS_PER_CAPITA": r"Loss_{percap,health}",

    # MILITARY (3)
    "MILITARY_TO_CLINICAL_TRIALS_SPENDING_RATIO": r"Ratio_{mil}",
    "MILITARY_TO_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO": r"Ratio_{mil}",
    "MILITARY_VS_MEDICAL_RESEARCH_RATIO": r"Ratio_{mil,RD}",

    # MISALLOCATION (1)
    "MISALLOCATION_FACTOR_DEATH_VS_SAVING": r"Cost",

    # MRNA (1)
    "MRNA_THERAPEUTIC_COMBINATIONS": r"Mrna",

    # NEW (1)
    "NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR": r"New",

    # NIH (3)
    "NIH_ANNUAL_BUDGET": r"Nih_{annual}",
    "NIH_CLINICAL_TRIALS_SPENDING_PCT": r"Trials",
    "NIH_STANDARD_RESEARCH_COST_PER_QALY": r"Cost_{RD}",

    # NPV (2)
    "NPV_DISCOUNT_RATE_STANDARD": r"Rate_{RD}",
    "NPV_TIME_HORIZON_YEARS": r"Time_{NPV}",

    # OXFORD (1)
    "OXFORD_RECOVERY_TRIAL_DURATION_MONTHS": r"Ratio_{RD}",

    # PATIENT (1)
    "PATIENT_WILLINGNESS_TRIAL_PARTICIPATION_PCT": r"Patients",

    # PEACE (14)
    "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT": r"Cost_{soc,ann}",
    "PEACE_DIVIDEND_CONFLICT_REDUCTION": r"Benefit_{peace}",
    "PEACE_DIVIDEND_DIRECT_COSTS": r"Cost_{direct,peace}",
    "PEACE_DIVIDEND_DIRECT_FISCAL_SAVINGS": r"Savings_{direct,peace}",
    "PEACE_DIVIDEND_ENVIRONMENTAL": r"Savings_{env,peace}",
    "PEACE_DIVIDEND_HUMAN_CASUALTIES": r"Savings_{human,peace}",
    "PEACE_DIVIDEND_INDIRECT_COSTS": r"Cost_{indirect,peace}",
    "PEACE_DIVIDEND_INFRASTRUCTURE": r"Savings_{infra,peace}",
    "PEACE_DIVIDEND_LOST_ECONOMIC_GROWTH": r"Savings_{econ_growth,peace}",
    "PEACE_DIVIDEND_LOST_HUMAN_CAPITAL": r"Savings_{human_cap,peace}",
    "PEACE_DIVIDEND_PTSD": r"Cost_{PTSD,peace}",
    "PEACE_DIVIDEND_REFUGEE_SUPPORT": r"Cost_{ref,peace}",
    "PEACE_DIVIDEND_TRADE_DISRUPTION": r"Savings_{trade,peace}",
    "PEACE_DIVIDEND_VETERAN_HEALTHCARE": r"Cost_{vet,peace}",

    # PER (2)
    "PER_CAPITA_CHRONIC_DISEASE_COST": r"Cost_{percap,dis}",
    "PER_CAPITA_MENTAL_HEALTH_COST": r"Cost_{percap,health}",

    # PERSONAL (1)
    "PERSONAL_LIFETIME_WEALTH": r"Time",

    # PHARMA (5)
    "PHARMA_DRUG_DEVELOPMENT_COST_CURRENT": r"Cost_{curr}",
    "PHARMA_DRUG_REVENUE_AVERAGE_CURRENT": r"Pharma_{current}",
    "PHARMA_PHASE_2_3_COST_BARRIER": r"Cost",
    "PHARMA_ROI_CURRENT_SYSTEM_PCT": r"ROI_{curr}",
    "PHARMA_SUCCESS_RATE_CURRENT_PCT": r"Rate_{curr}",

    # PHASE (4)
    "PHASE_1_PASSED_COMPOUNDS_GLOBAL": r"Phase_{global}",
    "PHASE_1_SAFETY_DURATION_YEARS": r"Ratio",
    "PHASE_2_3_CLINICAL_TRIAL_COST_PCT": r"Cost",
    "PHASE_3_TRIAL_COST_MIN": r"Cost",

    # PMC (1)
    "PMC_PRAGMATIC_TRIAL_MEDIAN_COST_PER_PATIENT": r"Cost",

    # POLIO (1)
    "POLIO_VACCINATION_ROI": r"ROI",

    # POLITICAL (1)
    "POLITICAL_SUCCESS_PROBABILITY": r"Probability",

    # POST (2)
    "POST_1962_DRUG_APPROVAL_REDUCTION_PCT": r"Reduction",
    "POST_WW2_MILITARY_CUT_PCT": r"Spending_{mil}",

    # PRAGMATIC (2)
    "PRAGMATIC_TRIAL_COST_PER_QALY": r"Cost",
    "PRAGMATIC_VS_NIH_EFFICIENCY_MULTIPLIER": r"Multiplier",

    # PRE (4)
    "PRE_1962_DRUG_DEVELOPMENT_COST_1980_USD": r"Cost_{pre62}",
    "PRE_1962_DRUG_DEVELOPMENT_COST_2024_USD": r"Cost_{pre62}",
    "PRE_1962_PHYSICIAN_COUNT": r"Pre",
    "PRE_1962_VALIDATION_YEARS": r"Pre",

    # QALYS (1)
    "QALYS_PER_COVID_DEATH_AVERTED": r"Deaths",

    # RARE (1)
    "RARE_DISEASES_COUNT_GLOBAL": r"Rare_{global}",

    # RECOVERY (5)
    "RECOVERY_TRIAL_COST_PER_PATIENT": r"Cost",
    "RECOVERY_TRIAL_COST_REDUCTION_FACTOR": r"Cost",
    "RECOVERY_TRIAL_GLOBAL_LIVES_SAVED": r"Trials_{global}",
    "RECOVERY_TRIAL_TOTAL_COST": r"Cost_{total}",
    "RECOVERY_TRIAL_TOTAL_QALYS_GENERATED": r"Rate_{total}",

    # REGULATORY (2)
    "REGULATORY_DELAY_MEAN_AGE_OF_DEATH": r"Deaths_{reg}",
    "REGULATORY_DELAY_SUFFERING_PERIOD_YEARS": r"Deaths_{reg}",

    # SAFE (1)
    "SAFE_COMPOUNDS_COUNT": r"Safe",

    # SMALLPOX (2)
    "SMALLPOX_ERADICATION_ROI": r"ROI",
    "SMALLPOX_ERADICATION_TOTAL_BENEFIT": r"Benefit_{total}",

    # SMOKING (1)
    "SMOKING_CESSATION_ANNUAL_BENEFIT": r"Benefit_{ann}",

    # STANDARD (2)
    "STANDARD_ECONOMIC_QALY_VALUE_USD": r"QALYs_{RD}",
    "STANDARD_QALYS_PER_LIFE_SAVED": r"QALYs_{RD}",

    # STATUS (2)
    "STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT": r"Status",
    "STATUS_QUO_QUEUE_CLEARANCE_YEARS": r"Time",

    # SUGAR (1)
    "SUGAR_SUBSIDY_COST_PER_PERSON_ANNUAL": r"Subsidies_{ann}",

    # SWITZERLAND (2)
    "SWITZERLAND_DEFENSE_SPENDING_PCT": r"Spending",
    "SWITZERLAND_GDP_PER_CAPITA_K": r"SwitzerlandGDP",

    # TERRORISM (1)
    "TERRORISM_DEATHS_911": r"Deaths_{terror}",

    # TESTED (1)
    "TESTED_RELATIONSHIPS_ESTIMATE": r"Tested",

    # THALIDOMIDE (11)
    "THALIDOMIDE_CASES_WORLDWIDE": r"Thalidomide",
    "THALIDOMIDE_DALYS_PER_EVENT": r"DALYs",
    "THALIDOMIDE_DEATHS_PER_EVENT": r"Deaths",
    "THALIDOMIDE_DISABILITY_WEIGHT": r"Thalidomide",
    "THALIDOMIDE_MORTALITY_RATE": r"Rate",
    "THALIDOMIDE_SURVIVORS_PER_EVENT": r"Thalidomide",
    "THALIDOMIDE_SURVIVOR_LIFESPAN": r"Thalidomide",
    "THALIDOMIDE_US_CASES_PREVENTED": r"ThalidomideUS",
    "THALIDOMIDE_US_POPULATION_SHARE_1960": r"Population",
    "THALIDOMIDE_YLD_PER_EVENT": r"YLD",
    "THALIDOMIDE_YLL_PER_EVENT": r"YLL",

    # TOTAL (3)
    "TOTAL_BOOK_WORDS": r"Book_{total}",
    "TOTAL_RESEARCH_FUNDING_WITH_TREATY": r"Funding_{total}",
    "TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS": r"Testable_{total}",

    # TRADITIONAL (1)
    "TRADITIONAL_PHASE3_COST_PER_PATIENT": r"Cost",

    # TREATMENT (1)
    "TREATMENT_ACCELERATION_YEARS_CURRENT": r"Ratio_{curr}",

    # TREATY (24)
    "TREATY_BENEFIT_MULTIPLIER_VS_VACCINES": r"Multiplier_{treaty}",
    "TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED": r"Cost_{camp,ann}",
    "TREATY_CAMPAIGN_BUDGET_LOBBYING": r"Campaign_{camp,treaty}",
    "TREATY_CAMPAIGN_BUDGET_RESERVE": r"Campaign_{camp,treaty}",
    "TREATY_CAMPAIGN_BUDGET_SUPER_PACS": r"Campaign_{camp,treaty}",
    "TREATY_CAMPAIGN_DURATION_YEARS": r"Ratio_{camp,treaty}",
    "TREATY_CAMPAIGN_TOTAL_COST": r"Cost_{camp,total}",
    "TREATY_CAMPAIGN_VIRAL_REFERENDUM_BASE_CASE": r"Campaign_{camp,treaty}",
    "TREATY_CAMPAIGN_VOTING_BLOC_TARGET": r"Campaign_{camp,treaty}",
    "TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG": r"Increase_{max,treaty}",
    "TREATY_EXPECTED_COST_PER_DALY": r"Cost_{treaty}",
    "TREATY_EXPECTED_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG": r"ROI_{max,treaty}",
    "TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER": r"Multiplier_{net,treaty}",
    "TREATY_LIVES_SAVED_ANNUAL_GLOBAL": r"Deaths_{ann}",
    "TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS": r"Benefit_{ann}",
    "TREATY_QALYS_GAINED_ANNUAL_GLOBAL": r"Dividend_{ann}",
    "TREATY_RECURRING_BENEFITS_ANNUAL": r"Benefit_{ann}",
    "TREATY_REDIRECTED_SPENDING_INFINITE_ROI": r"ROI_{direct,treaty}",
    "TREATY_REDUCTION_PCT": r"Reduction_{treaty}",
    "TREATY_ROI_EXISTING_DRUGS_ONLY": r"ROI_{treaty}",
    "TREATY_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG": r"Increase_{max,treaty}",
    "TREATY_TOTAL_ANNUAL_COSTS": r"Cost_{total}",
    "TREATY_VS_BED_NETS_MULTIPLIER": r"Multiplier_{net,treaty}",
    "TREATY_VS_DIRECT_FUNDING_LEVERAGE": r"Funding_{direct,treaty}",

    # TRIAL (2)
    "TRIAL_CAPACITY_CUMULATIVE_YEARS_20YR": r"Capacity",
    "TRIAL_RELEVANT_DISEASES_COUNT": r"Trials_{dis}",

    # TYPE (2)
    "TYPE_II_ERROR_COST_RATIO": r"Cost",
    "TYPE_I_ERROR_BENEFIT_DALYS": r"DALYs",

    # TYPICAL (1)
    "TYPICAL_CEO_HOURLY_RATE": r"Rate",

    # UNEXPLORED (1)
    "UNEXPLORED_RATIO": r"Ratio",

    # US (12)
    "US_ALZHEIMERS_ANNUAL_COST": r"Cost_{alz,ann}",
    "US_CANCER_ANNUAL_COST": r"Cost_{cancer,ann}",
    "US_CHRONIC_DISEASE_SPENDING_ANNUAL": r"Spending_{chronic,ann}",
    "US_DIABETES_ANNUAL_COST": r"Cost_{diab,ann}",
    "US_HEART_DISEASE_ANNUAL_COST": r"Cost_{heart,ann}",
    "US_LIFE_EXPECTANCY_1880": r"US",
    "US_LIFE_EXPECTANCY_1962": r"US",
    "US_LIFE_EXPECTANCY_2019": r"US",
    "US_MAJOR_DISEASES_TOTAL_ANNUAL_COST": r"Cost_{total}",
    "US_MENTAL_HEALTH_COST_ANNUAL": r"Cost_{mental,ann}",
    "US_MILITARY_SPENDING_PCT_GDP": r"Spending_{mil}",
    "US_POPULATION_2024": r"Population",

    # VALLEY (1)
    "VALLEY_OF_DEATH_ATTRITION_PCT": r"Deaths",

    # VALUE (1)
    "VALUE_OF_STATISTICAL_LIFE": r"Value",

    # VICTORY (3)
    "VICTORY_BOND_ANNUAL_PAYOUT": r"Victory_{annual}",
    "VICTORY_BOND_ANNUAL_RETURN_PCT": r"Victory_{annual}",
    "VICTORY_BOND_FUNDING_PCT": r"Funding",

    # VITAMIN (1)
    "VITAMIN_A_COST_PER_DALY": r"Cost",

    # WATER (2)
    "WATER_FLUORIDATION_ANNUAL_BENEFIT": r"Benefit_{water,ann}",
    "WATER_FLUORIDATION_ROI": r"ROI_{water}",

    # WHO (1)
    "WHO_QALY_THRESHOLD_COST_EFFECTIVE": r"Cost",

    # WILLING (1)
    "WILLING_TRIAL_PARTICIPANTS_GLOBAL": r"Patients_{global}",

    # WORKFORCE (1)
    "WORKFORCE_WITH_PRODUCTIVITY_LOSS": r"Loss",
}
