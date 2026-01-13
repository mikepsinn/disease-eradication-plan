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
SYMBOLS = {

    # === ADAPTABLE (3 parameters) ===
    # Cost per patient in ADAPTABLE trial ($14M PCORI grant / 1...
    # Unit: USD/patient
    "ADAPTABLE_TRIAL_COST_PER_PATIENT": r"Cost",

    # Patients enrolled in ADAPTABLE trial (PCORnet 2016-2019)....
    # Unit: patients
    "ADAPTABLE_TRIAL_PATIENTS": r"Patients",

    # PCORI grant for ADAPTABLE trial (2016-2019). Note: Direct...
    # Unit: USD
    "ADAPTABLE_TRIAL_TOTAL_COST": r"Cost_{total}",


    # === ADDITIONAL (1 parameters) ===
    # Additional drug approvals per year when Phase 2/3 cost ba...
    # Unit: drugs/year
    "ADDITIONAL_DRUGS_FROM_COST_ELIMINATION": r"Cost",


    # === ANTIDEPRESSANT (1 parameters) ===
    # Mean exclusion rate in antidepressant trials (86.1% of re...
    # Unit: percentage
    "ANTIDEPRESSANT_TRIAL_EXCLUSION_RATE": r"Rate",


    # === APPROVED (1 parameters) ===
    # Unique approved drug-disease pairings (FDA-approved uses,...
    # Unit: pairings
    "APPROVED_DRUG_DISEASE_PAIRINGS": r"Approved",


    # === AVERAGE (2 parameters) ===
    # Average annual stock market return (10%)
    # Unit: rate
    "AVERAGE_MARKET_RETURN_PCT": r"Average",

    # Average US hourly wage
    # Unit: USD/hour
    "AVERAGE_US_HOURLY_WAGE": r"Hours",


    # === BASELINE (1 parameters) ===
    # Baseline annual lives saved by pharmaceuticals (conservat...
    # Unit: deaths/year
    "BASELINE_LIVES_SAVED_ANNUAL": r"Lives_{ann}",


    # === BED (1 parameters) ===
    # GiveWell cost per DALY for insecticide-treated bed nets (...
    # Unit: USD/DALY
    "BED_NETS_COST_PER_DALY": r"Cost_{net}",


    # === BOOK (1 parameters) ===
    # Average reading speed (conservative for non-fiction)
    # Unit: words/minute
    "BOOK_READING_SPEED_WPM": r"Book",


    # === CAMPAIGN (27 parameters) ===
    # Celebrity and influencer endorsements
    # Unit: USD
    "CAMPAIGN_CELEBRITY_ENDORSEMENT": r"Campaign_{camp}",

    # Community organizing and ambassador program budget
    # Unit: USD
    "CAMPAIGN_COMMUNITY_ORGANIZING": r"Campaign_{community}",

    # Contingency fund for unexpected costs
    # Unit: USD
    "CAMPAIGN_CONTINGENCY": r"Cost_{camp}",

    # Defense industry conversion program
    # Unit: USD
    "CAMPAIGN_DEFENSE_CONVERSION": r"Campaign_{camp}",

    # Budget for co-opting defense industry lobbyists
    # Unit: USD
    "CAMPAIGN_DEFENSE_LOBBYIST_BUDGET": r"Campaign_{camp}",

    # Healthcare industry alignment and partnerships
    # Unit: USD
    "CAMPAIGN_HEALTHCARE_ALIGNMENT": r"Campaign_{camp,health}",

    # Campaign operational infrastructure
    # Unit: USD
    "CAMPAIGN_INFRASTRUCTURE": r"Ratio_{infra}",

    # AI-assisted legal work budget
    # Unit: USD
    "CAMPAIGN_LEGAL_AI_BUDGET": r"Campaign_{camp}",

    # Legal defense fund
    # Unit: USD
    "CAMPAIGN_LEGAL_DEFENSE": r"Campaign_{camp}",

    # Legal drafting and compliance work
    # Unit: USD
    "CAMPAIGN_LEGAL_WORK": r"Campaign_{camp}",

    # EU lobbying campaign budget
    # Unit: USD
    "CAMPAIGN_LOBBYING_EU": r"Campaign_{camp}",

    # G20 countries lobbying budget
    # Unit: USD
    "CAMPAIGN_LOBBYING_G20_MILLIONS": r"Campaign_{camp}",

    # US lobbying campaign budget
    # Unit: USD
    "CAMPAIGN_LOBBYING_US": r"Campaign_{camp}",

    # Maximum mass media campaign budget
    # Unit: USD
    "CAMPAIGN_MEDIA_BUDGET_MAX": r"Campaign_{camp}",

    # Minimum mass media campaign budget
    # Unit: USD
    "CAMPAIGN_MEDIA_BUDGET_MIN": r"Campaign_{camp}",

    # Opposition research and rapid response
    # Unit: USD
    "CAMPAIGN_OPPOSITION_RESEARCH": r"Campaign_{camp,RD}",

    # Phase 1 campaign budget (Foundation, Year 1)
    # Unit: USD
    "CAMPAIGN_PHASE1_BUDGET": r"Campaign_{camp}",

    # Phase 2 campaign budget (Scale & Momentum, Years 2-3)
    # Unit: USD
    "CAMPAIGN_PHASE2_BUDGET": r"Campaign_{camp}",

    # Pilot program testing in small countries
    # Unit: USD
    "CAMPAIGN_PILOT_PROGRAMS": r"Campaign_{camp}",

    # Voting platform and technology development
    # Unit: USD
    "CAMPAIGN_PLATFORM_DEVELOPMENT": r"Campaign_{platform}",

    # Regulatory compliance and navigation
    # Unit: USD
    "CAMPAIGN_REGULATORY_NAVIGATION": r"Campaign_{reg}",

    # Scaling preparation and blueprints
    # Unit: USD
    "CAMPAIGN_SCALING_PREP": r"Ratio_{camp}",

    # Campaign core team staff budget
    # Unit: USD
    "CAMPAIGN_STAFF_BUDGET": r"Campaign_{staff}",

    # Super PAC campaign expenditures
    # Unit: USD
    "CAMPAIGN_SUPER_PAC_BUDGET": r"Campaign_{camp}",

    # Tech industry partnerships and infrastructure
    # Unit: USD
    "CAMPAIGN_TECH_PARTNERSHIPS": r"Campaign_{camp}",

    # Post-victory treaty implementation support
    # Unit: USD
    "CAMPAIGN_TREATY_IMPLEMENTATION": r"Campaign_{camp,treaty}",

    # Viral marketing content creation budget
    # Unit: USD
    "CAMPAIGN_VIRAL_CONTENT_BUDGET": r"Campaign_{camp}",


    # === CAREGIVER (5 parameters) ===
    # Total annual value of unpaid caregiving in US
    # Unit: USD/year
    "CAREGIVER_ANNUAL_VALUE_TOTAL": r"Caregiver_{annual}",

    # Annual cost of unpaid caregiving (replacement cost method)
    # Unit: USD/year
    "CAREGIVER_COST_ANNUAL": r"Cost_{ann}",

    # Number of unpaid caregivers in US
    # Unit: people
    "CAREGIVER_COUNT_US": r"CaregiverUS",

    # Average monthly hours of unpaid family caregiving in US
    # Unit: hours/month
    "CAREGIVER_HOURS_PER_MONTH": r"Hours",

    # Estimated replacement cost per hour of caregiving
    # Unit: USD/hour
    "CAREGIVER_VALUE_PER_HOUR_SIMPLE": r"Cost",


    # === CELL (2 parameters) ===
    # Distinct cell therapy approaches (CAR-T variants, iPSCs, ...
    # Unit: approaches
    "CELL_THERAPY_APPROACHES": r"Cell",

    # Cell therapy approach-disease combinations
    # Unit: combinations
    "CELL_THERAPY_DISEASE_COMBINATIONS": r"Cell",


    # === CHILDHOOD (3 parameters) ===
    # Estimated annual global economic benefit from childhood v...
    # Unit: USD/year
    "CHILDHOOD_VACCINATION_ANNUAL_BENEFIT": r"Benefit_{ann}",

    # Estimated cost per DALY for US childhood vaccination prog...
    # Unit: USD/DALY
    "CHILDHOOD_VACCINATION_COST_PER_DALY": r"Cost",

    # Return on investment from childhood vaccination programs
    # Unit: ratio
    "CHILDHOOD_VACCINATION_ROI": r"ROI",


    # === CHRONIC (1 parameters) ===
    # Disability weight for untreated chronic conditions (WHO G...
    # Unit: weight
    "CHRONIC_DISEASE_DISABILITY_WEIGHT": r"Chronic",


    # === CLINICAL (2 parameters) ===
    # Annual clinical trial spending per approved drug (trials ...
    # Unit: USD
    "CLINICAL_TRIAL_COST_PER_APPROVED_DRUG": r"Cost",

    # Average annual cost per clinical trial participant (total...
    # Unit: USD
    "CLINICAL_TRIAL_COST_PER_PARTICIPANT_ANNUAL": r"Cost_{ann}",


    # === COMBINATION (2 parameters) ===
    # Total combination therapy space (pairwise drug combinatio...
    # Unit: combinations
    "COMBINATION_THERAPY_DISEASE_SPACE": r"Combination",

    # Unique pairwise drug combinations from known safe compoun...
    # Unit: combinations
    "COMBINATION_THERAPY_PAIRS": r"Combination",


    # === COMBINED (1 parameters) ===
    # Combined peace and health dividends for ROI calculation
    # Unit: USD/year
    "COMBINED_PEACE_HEALTH_DIVIDENDS_ANNUAL_FOR_ROI_CALC": r"Dividend_{ann}",


    # === CONCENTRATED (1 parameters) ===
    # Estimated combined market capitalization of concentrated ...
    # Unit: USD
    "CONCENTRATED_INTEREST_SECTOR_MARKET_CAP_USD": r"Rate",


    # === CPI (1 parameters) ===
    # CPI inflation multiplier from 1980 to 2024 (280.48% cumul...
    # Unit: ratio
    "CPI_MULTIPLIER_1980_TO_2024": r"Multiplier_{80s}",


    # === CURRENT (11 parameters) ===
    # Current active trials at any given time (3-5 year duration)
    # Unit: trials
    "CURRENT_ACTIVE_TRIALS": r"Time_{curr}",

    # Current clinical trial participation rate (0.06% of popul...
    # Unit: rate
    "CURRENT_CLINICAL_TRIAL_PARTICIPATION_RATE": r"Rate_{curr}",

    # Years to test all pairwise drug combinations at current t...
    # Unit: years
    "CURRENT_COMBINATION_EXPLORATION_YEARS": r"Ratio_{curr}",

    # Global population with chronic diseases
    # Unit: people
    "CURRENT_DISEASE_PATIENTS_GLOBAL": r"Population_{curr,global}",

    # Average annual new drug approvals globally
    # Unit: drugs/year
    "CURRENT_DRUG_APPROVALS_PER_YEAR": r"Drug_{current}",

    # Years to test all known safe drug-disease combinations at...
    # Unit: years
    "CURRENT_KNOWN_SAFE_EXPLORATION_YEARS": r"Ratio_{curr}",

    # Current patient participation rate in clinical trials (0....
    # Unit: rate
    "CURRENT_PATIENT_PARTICIPATION_RATE": r"Rate_{curr}",

    # Years to test all therapeutic combinations (known safe + ...
    # Unit: years
    "CURRENT_TOTAL_EXPLORATION_YEARS": r"Ratio_{curr,total}",

    # Current global clinical trials per year
    # Unit: trials/year
    "CURRENT_TRIALS_PER_YEAR": r"Trials_{curr}",

    # Current trial abandonment rate (40% never complete)
    # Unit: rate
    "CURRENT_TRIAL_ABANDONMENT_RATE": r"Rate_{curr}",

    # Annual global clinical trial participants (IQVIA 2022: 1....
    # Unit: patients/year
    "CURRENT_TRIAL_SLOTS_AVAILABLE": r"Trials_{curr}",


    # === DCT (1 parameters) ===
    # Mid-range funding for commercial DCT platform
    # Unit: USD
    "DCT_PLATFORM_FUNDING_MEDIUM": r"Funding_{platform}",


    # === DEFENSE (2 parameters) ===
    # Annual defense industry lobbying spending
    # Unit: USD/year
    "DEFENSE_LOBBYING_ANNUAL": r"Spending_{ann}",

    # Percentage of budget defense sector keeps under 1% treaty
    # Unit: rate
    "DEFENSE_SECTOR_RETENTION_PCT": r"Defense",


    # === DEWORMING (1 parameters) ===
    # Cost per DALY for deworming programs (range $28-82, midpo...
    # Unit: USD/DALY
    "DEWORMING_COST_PER_DALY": r"Cost",


    # === DFDA (46 parameters) ===
    # Annual Decentralized Framework for Drug Assessment benefi...
    # Unit: USD/year
    "DFDA_BENEFIT_RD_ONLY_ANNUAL": r"Benefit_{DFDA,ann}",

    # Combined speedup factor for treatment discovery from dFDA...
    # Unit: multiplier
    "DFDA_COMBINED_TREATMENT_SPEEDUP_MULTIPLIER": r"Multiplier_{DFDA}",

    # Cost per DALY if philanthropists/governments directly fun...
    # Unit: USD/DALY
    "DFDA_DIRECT_FUNDING_COST_PER_DALY": r"Cost_{direct,DFDA}",

    # NPV of direct funding ($21.76B/year for medical research ...
    # Unit: USD
    "DFDA_DIRECT_FUNDING_QUEUE_CLEARANCE_NPV": r"Funding_{direct,DFDA}",

    # ROI from direct philanthropic/government funding of medic...
    # Unit: ratio
    "DFDA_DIRECT_FUNDING_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG": r"Increase_{direct_funding,DFDA}",

    # How many times more cost-effective direct funding is vs b...
    # Unit: ratio
    "DFDA_DIRECT_FUNDING_VS_BED_NETS_MULTIPLIER": r"Multiplier_{direct,DFDA}",

    # Total Disability-Adjusted Life Years lost from disease er...
    # Unit: DALYs
    "DFDA_EFFICACY_LAG_ELIMINATION_DALYS": r"DALYs_{DFDA}",

    # Total eventually avoidable deaths from delaying disease e...
    # Unit: deaths
    "DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED": r"Deaths_{DFDA}",

    # Total economic loss from delaying disease eradication by ...
    # Unit: USD
    "DFDA_EFFICACY_LAG_ELIMINATION_ECONOMIC_VALUE": r"Delay_{DFDA}",

    # Years Lived with Disability during disease eradication de...
    # Unit: years
    "DFDA_EFFICACY_LAG_ELIMINATION_YLD": r"Delay_{DFDA}",

    # Years of Life Lost from disease eradication delay deaths ...
    # Unit: years
    "DFDA_EFFICACY_LAG_ELIMINATION_YLL": r"Delay_{DFDA}",

    # Diseases per year receiving their first effective treatme...
    # Unit: diseases/year
    "DFDA_FIRST_TREATMENTS_PER_YEAR": r"DFDA",

    # Years to test all known safe drug-disease combinations wi...
    # Unit: years
    "DFDA_KNOWN_SAFE_EXPLORATION_YEARS": r"Ratio_{DFDA}",

    # Annual net savings from R&D cost reduction only (gross sa...
    # Unit: USD/year
    "DFDA_NET_SAVINGS_RD_ONLY_ANNUAL": r"Savings_{net,ann}",

    # Years to reach full Decentralized Framework for Drug Asse...
    # Unit: years
    "DFDA_NPV_ADOPTION_RAMP_YEARS": r"DFDANPV",

    # Decentralized Framework for Drug Assessment Core framewor...
    # Unit: USD/year
    "DFDA_NPV_ANNUAL_OPEX": r"OPEX_{DFDA,ann}",

    # Total NPV annual opex (Decentralized Framework for Drug A...
    # Unit: USD/year
    "DFDA_NPV_ANNUAL_OPEX_TOTAL": r"OPEX_{DFDA,total}",

    # NPV of Decentralized Framework for Drug Assessment R&D sa...
    # Unit: USD
    "DFDA_NPV_BENEFIT_RD_ONLY": r"Benefit_{DFDA,RD}",

    # NPV net benefit using R&D savings only (benefits minus co...
    # Unit: USD
    "DFDA_NPV_NET_BENEFIT_RD_ONLY": r"Benefit_{net,RD}",

    # Present value of annual opex over 10 years (NPV formula)
    # Unit: USD
    "DFDA_NPV_PV_ANNUAL_OPEX": r"OPEX_{DFDA,ann}",

    # Total NPV cost (upfront + PV of annual opex)
    # Unit: USD
    "DFDA_NPV_TOTAL_COST": r"Cost_{DFDA,total}",

    # Decentralized Framework for Drug Assessment Core framewor...
    # Unit: USD
    "DFDA_NPV_UPFRONT_COST": r"Cost_{DFDA,NPV}",

    # Total NPV upfront costs (Decentralized Framework for Drug...
    # Unit: USD
    "DFDA_NPV_UPFRONT_COST_TOTAL": r"Cost_{DFDA,total}",

    # Percentage of treaty funding allocated to Decentralized F...
    # Unit: rate
    "DFDA_OPEX_PCT_OF_TREATY_FUNDING": r"OPEX_{DFDA,treaty}",

    # dFDA pragmatic trial cost per patient. Uses ADAPTABLE tri...
    # Unit: USD/patient
    "DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT": r"Cost_{DFDA}",

    # Years to treat all currently untreatable diseases with dF...
    # Unit: years
    "DFDA_QUEUE_CLEARANCE_YEARS": r"Time_{DFDA}",

    # Daily R&D savings from trial cost reduction (opportunity ...
    # Unit: USD/day
    "DFDA_RD_SAVINGS_DAILY": r"Cost_{DFDA,daily}",

    # ROI from Decentralized Framework for Drug Assessment R&D ...
    # Unit: ratio
    "DFDA_ROI_RD_ONLY": r"Savings_{DFDA,RD}",

    # Target cost per patient in USD (same as DFDA_TARGET_COST_...
    # Unit: USD/patient
    "DFDA_TARGET_COST_PER_PATIENT_USD": r"Cost_{DFDA}",

    # Years to test all therapeutic combinations (known safe + ...
    # Unit: years
    "DFDA_TOTAL_EXPLORATION_YEARS": r"Ratio_{DFDA,total}",

    # Maximum trials per year possible with trial capacity mult...
    # Unit: trials/year
    "DFDA_TRIALS_PER_YEAR_CAPACITY": r"Capacity_{DFDA}",

    # Total DALYs averted from trial capacity increase alone. C...
    # Unit: DALYs
    "DFDA_TRIAL_CAPACITY_DALYS_AVERTED": r"Increase_{DFDA}",

    # Total economic value from trial capacity increase alone. ...
    # Unit: USD
    "DFDA_TRIAL_CAPACITY_ECONOMIC_VALUE": r"Increase_{DFDA}",

    # Total eventually avoidable deaths from trial capacity inc...
    # Unit: deaths
    "DFDA_TRIAL_CAPACITY_LIVES_SAVED": r"Increase_{DFDA}",

    # Trial capacity multiplier from DIH funding capacity vs. c...
    # Unit: ratio
    "DFDA_TRIAL_CAPACITY_MULTIPLIER": r"Multiplier_{DFDA}",

    # Total DALYs averted from the combined dFDA timeline shift...
    # Unit: DALYs
    "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS": r"DALYs_{max,DFDA}",

    # Total economic value from the combined dFDA timeline shif...
    # Unit: USD
    "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE": r"Benefit_{max,DFDA}",

    # Total eventually avoidable deaths from the combined dFDA ...
    # Unit: deaths
    "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED": r"Capacity_{max,DFDA}",

    # Hours of suffering eliminated from the combined dFDA time...
    # Unit: hours
    "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS": r"Capacity_{max,DFDA}",

    # Average years earlier patients receive treatments due to ...
    # Unit: years
    "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS": r"Capacity_{max,DFDA}",

    # Years earlier the average first treatment arrives due to ...
    # Unit: years
    "DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS": r"Ratio_{DFDA}",

    # Cost reduction factor projected for dFDA pragmatic trials...
    # Unit: multiplier
    "DFDA_TRIAL_COST_REDUCTION_FACTOR": r"Cost_{DFDA}",

    # Trial cost reduction percentage: (traditional - dFDA) / t...
    # Unit: percentage
    "DFDA_TRIAL_COST_REDUCTION_PCT": r"Reduction_{DFDA}",

    # Decentralized Framework for Drug Assessment one-time buil...
    # Unit: USD
    "DFDA_UPFRONT_BUILD": r"Cost_{DFDA}",

    # Decentralized Framework for Drug Assessment one-time buil...
    # Unit: USD
    "DFDA_UPFRONT_BUILD_MAX": r"Cost_{DFDA}",

    # Factor increase in drugs entering development when dFDA e...
    # Unit: multiplier
    "DFDA_VALLEY_OF_DEATH_RESCUE_MULTIPLIER": r"Multiplier_{DFDA}",


    # === DIH (7 parameters) ===
    # DIH broader initiatives annual opex (medium case)
    # Unit: USD/year
    "DIH_NPV_ANNUAL_OPEX_INITIATIVES": r"OPEX_{opex,ann}",

    # DIH broader initiatives upfront cost (medium case)
    # Unit: USD
    "DIH_NPV_UPFRONT_COST_INITIATIVES": r"Cost_{NPV}",

    # Number of patients fundable annually at dFDA pragmatic tr...
    # Unit: patients/year
    "DIH_PATIENTS_FUNDABLE_ANNUALLY": r"Fundable_{ann}",

    # Percentage of treaty funding allocated to medical researc...
    # Unit: rate
    "DIH_TREASURY_MEDICAL_RESEARCH_PCT": r"Treasury_{RD}",

    # Annual funding for pragmatic clinical trials (treaty fund...
    # Unit: USD/year
    "DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL": r"Treasury_{ann}",

    # Annual clinical trial patient subsidies (all medical rese...
    # Unit: USD/year
    "DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL": r"Treasury_{ann}",

    # Percentage of treaty funding going directly to patient tr...
    # Unit: rate
    "DIH_TREASURY_TRIAL_SUBSIDIES_PCT": r"Treasury",


    # === DISEASE (3 parameters) ===
    # Percentage of caregiving for treatable disease conditions...
    # Unit: rate
    "DISEASE_RELATED_CAREGIVER_PCT": r"Disease",

    # Ratio of annual disease deaths to 9/11 terrorism deaths
    # Unit: ratio
    "DISEASE_VS_TERRORISM_DEATHS_RATIO": r"Deaths_{terror,dis}",

    # Ratio of annual disease deaths to war deaths
    # Unit: ratio
    "DISEASE_VS_WAR_DEATHS_RATIO": r"Deaths_{war}",


    # === DISEASES (1 parameters) ===
    # Number of diseases without effective treatment. 95% of 7,...
    # Unit: diseases
    "DISEASES_WITHOUT_EFFECTIVE_TREATMENT": r"Diseases",


    # === DIVIDEND (1 parameters) ===
    # Coverage factor of treaty funding vs Decentralized Framew...
    # Unit: ratio
    "DIVIDEND_COVERAGE_FACTOR": r"OPEX",


    # === DRUG (5 parameters) ===
    # Drug development cost increase from 1980s to current ($19...
    # Unit: ratio
    "DRUG_COST_INCREASE_1980S_TO_CURRENT_MULTIPLIER": r"Multiplier_{curr}",

    # Drug development cost increase from pre-1962 to current (...
    # Unit: ratio
    "DRUG_COST_INCREASE_PRE1962_TO_CURRENT_MULTIPLIER": r"Multiplier_{curr}",

    # Drug development cost in 1980s (compounded to approval, 1...
    # Unit: USD
    "DRUG_DEVELOPMENT_COST_1980S": r"Cost_{80s}",

    # Total possible drug-disease combinations using existing s...
    # Unit: combinations
    "DRUG_DISEASE_COMBINATIONS_POSSIBLE": r"Drug",

    # Percentage of drugs that gain at least one new indication...
    # Unit: percentage
    "DRUG_REPURPOSING_SUCCESS_RATE": r"Rate",


    # === ECONOMIC (4 parameters) ===
    # Economic multiplier for education investment (2.1x ROI)
    # Unit: ratio
    "ECONOMIC_MULTIPLIER_EDUCATION_INVESTMENT": r"Multiplier_{edu}",

    # Economic multiplier for healthcare investment (4.3x ROI)
    # Unit: ratio
    "ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT": r"Multiplier_{health}",

    # Economic multiplier for infrastructure investment (1.6x ROI)
    # Unit: ratio
    "ECONOMIC_MULTIPLIER_INFRASTRUCTURE_INVESTMENT": r"Multiplier_{infra}",

    # Economic multiplier for military spending (0.6x ROI)
    # Unit: ratio
    "ECONOMIC_MULTIPLIER_MILITARY_SPENDING": r"Multiplier_{mil}",


    # === EFFECTIVE (1 parameters) ===
    # Lifetime benefit for age 30 baseline scenario ($4.3M)
    # Unit: USD
    "EFFECTIVE_HOURLY_RATE_LIFETIME_BENEFIT": r"Benefit",


    # === EFFICACY (1 parameters) ===
    # Regulatory delay for efficacy testing (Phase II/III) post...
    # Unit: years
    "EFFICACY_LAG_YEARS": r"Delay",


    # === EMERGING (1 parameters) ===
    # Total emerging modality combinations (gene therapy + mRNA...
    # Unit: combinations
    "EMERGING_MODALITY_COMBINATIONS": r"Emerging",


    # === EPIGENETIC (2 parameters) ===
    # Epigenetic reprogramming target-disease combinations
    # Unit: combinations
    "EPIGENETIC_DISEASE_COMBINATIONS": r"Epigenetic",

    # Druggable epigenetic targets (HDACs, DNMTs, histone modif...
    # Unit: targets
    "EPIGENETIC_TARGETS_COUNT": r"Epigenetic",


    # === EVENTUALLY (2 parameters) ===
    # Percentage of DALYs that are eventually avoidable with su...
    # Unit: percentage
    "EVENTUALLY_AVOIDABLE_DALY_PCT": r"DALYs",

    # Percentage of deaths that are eventually avoidable with s...
    # Unit: percentage
    "EVENTUALLY_AVOIDABLE_DEATH_PCT": r"Deaths",


    # === EXISTING (2 parameters) ===
    # Total deaths from delaying existing drugs over 8.2-year e...
    # Unit: deaths
    "EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL": r"Deaths_{total}",

    # Total economic loss from delaying existing drugs over 8.2...
    # Unit: USD
    "EXISTING_DRUGS_EFFICACY_LAG_ECONOMIC_LOSS": r"Delay",


    # === EXPLORATION (1 parameters) ===
    # Fraction of possible drug-disease space actually tested (...
    # Unit: percentage
    "EXPLORATION_RATIO": r"Ratio",


    # === FAMILY (1 parameters) ===
    # Minimum investment for family offices
    # Unit: USD
    "FAMILY_OFFICE_INVESTMENT_MIN": r"Family",


    # === FDA (5 parameters) ===
    # Total FDA-approved drug products in the U.S.
    # Unit: products
    "FDA_APPROVED_PRODUCTS_COUNT": r"FDA",

    # Unique active pharmaceutical ingredients in FDA-approved ...
    # Unit: compounds
    "FDA_APPROVED_UNIQUE_ACTIVE_INGREDIENTS": r"FDA",

    # FDA Generally Recognized as Safe (GRAS) substances (midpo...
    # Unit: substances
    "FDA_GRAS_SUBSTANCES_COUNT": r"FDA",

    # FDA timeline from Phase 1 start to approval (Phase 1-3 + ...
    # Unit: years
    "FDA_PHASE_1_TO_APPROVAL_YEARS": r"Time",

    # FDA approval timeline vs Oxford RECOVERY trial (9.1 years...
    # Unit: ratio
    "FDA_TO_OXFORD_RECOVERY_TRIAL_TIME_MULTIPLIER": r"Multiplier_{RD}",


    # === FUNDAMENTALLY (1 parameters) ===
    # Percentage of deaths that are fundamentally unavoidable e...
    # Unit: percentage
    "FUNDAMENTALLY_UNAVOIDABLE_DEATH_PCT": r"Deaths",


    # === GENE (1 parameters) ===
    # Gene therapy target-disease combinations (CRISPR, base ed...
    # Unit: combinations
    "GENE_THERAPY_DISEASE_COMBINATIONS": r"Gene",


    # === GIVEWELL (3 parameters) ===
    # GiveWell average cost per life saved across top charities
    # Unit: USD/life
    "GIVEWELL_COST_PER_LIFE_AVG": r"Cost",

    # GiveWell cost per life saved (Against Malaria Foundation)
    # Unit: USD/life
    "GIVEWELL_COST_PER_LIFE_MAX": r"Cost",

    # GiveWell cost per life saved (Helen Keller International)
    # Unit: USD/life
    "GIVEWELL_COST_PER_LIFE_MIN": r"Cost",


    # === GLOBAL (54 parameters) ===
    # Annual deaths from active combat worldwide
    # Unit: deaths/year
    "GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT": r"Deaths_{combat,ann}",

    # Annual deaths from state violence
    # Unit: deaths/year
    "GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE": r"Deaths_{state,ann}",

    # Annual deaths from terror attacks globally
    # Unit: deaths/year
    "GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS": r"Deaths_{terror,ann}",

    # Total annual conflict deaths globally (sum of combat, ter...
    # Unit: deaths/year
    "GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL": r"Deaths_{total}",

    # Global annual DALY burden from all diseases and injuries ...
    # Unit: DALYs/year
    "GLOBAL_ANNUAL_DALY_BURDEN": r"DALYs_{ann}",

    # Annual deaths from all diseases and aging globally
    # Unit: deaths/year
    "GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES": r"Deaths_{ann}",

    # Total annual cost of war worldwide (direct + indirect costs)
    # Unit: USD/year
    "GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST": r"Cost_{indirect,ann}",

    # Annual environmental damage and restoration costs from co...
    # Unit: USD
    "GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT": r"Cost_{env,ann}",

    # Annual cost of combat deaths (deaths × VSL)
    # Unit: USD/year
    "GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT": r"Cost_{combat,ann}",

    # Annual cost of state violence deaths (deaths × VSL)
    # Unit: USD/year
    "GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE": r"Cost_{state,ann}",

    # Annual cost of terror deaths (deaths × VSL)
    # Unit: USD/year
    "GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS": r"Cost_{terror,ann}",

    # Total annual human life losses from conflict (sum of comb...
    # Unit: USD/year
    "GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT": r"Loss_{human,ann}",

    # Annual infrastructure damage to communications from conflict
    # Unit: USD
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT": r"Damage_{comms,ann}",

    # Annual infrastructure damage to education facilities from...
    # Unit: USD
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT": r"Damage_{edu,ann}",

    # Annual infrastructure damage to energy systems from conflict
    # Unit: USD
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT": r"Damage_{energy,ann}",

    # Annual infrastructure damage to healthcare facilities fro...
    # Unit: USD
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT": r"Damage_{health,ann}",

    # Annual infrastructure damage to transportation from conflict
    # Unit: USD
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT": r"Damage_{transport,ann}",

    # Annual infrastructure damage to water systems from conflict
    # Unit: USD
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT": r"Damage_{water,ann}",

    # Total annual infrastructure destruction (sum of transport...
    # Unit: USD/year
    "GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT": r"Infrastructure_{global}",

    # Annual lives saved by medical research globally
    # Unit: lives/year
    "GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH": r"Lives_{ann}",

    # Annual lost economic growth from military spending opport...
    # Unit: USD
    "GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING": r"Cost_{econ_growth,ann}",

    # Annual lost productivity from conflict casualties
    # Unit: USD
    "GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT": r"Lost_{global}",

    # Annual PTSD and mental health costs from conflict
    # Unit: USD
    "GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT": r"Cost_{ann}",

    # Annual refugee support costs (108.4M refugees × $1,384/year)
    # Unit: USD
    "GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS": r"Cost_{ref,ann}",

    # Total annual trade disruption (sum of shipping, supply ch...
    # Unit: USD/year
    "GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT": r"Disruption_{trade,ann}",

    # Annual trade disruption costs from currency instability
    # Unit: USD
    "GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT": r"Cost_{currency,ann}",

    # Annual trade disruption costs from energy price volatility
    # Unit: USD
    "GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT": r"Cost_{trade,ann}",

    # Annual trade disruption costs from shipping disruptions
    # Unit: USD
    "GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT": r"Cost_{shipping,ann}",

    # Annual trade disruption costs from supply chain disruptions
    # Unit: USD
    "GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT": r"Cost_{trade,ann}",

    # Annual veteran healthcare costs (20-year projected)
    # Unit: USD
    "GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS": r"Cost_{vet,ann}",

    # Total annual direct war costs (military spending + infras...
    # Unit: USD/year
    "GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL": r"Cost_{direct,total}",

    # Total annual indirect war costs (opportunity cost + veter...
    # Unit: USD/year
    "GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL": r"Cost_{indirect,total}",

    # Annual global spending on clinical trials (Industry: $45-...
    # Unit: USD
    "GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL": r"Trials_{ann}",

    # Cost per life saved by medical research
    # Unit: USD/life
    "GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL": r"Cost_{ann}",

    # Total global deaths per day from all disease and aging (W...
    # Unit: deaths/day
    "GLOBAL_DISEASE_DEATHS_DAILY": r"Deaths_{daily}",

    # Direct medical costs of disease globally (treatment, hosp...
    # Unit: USD/year
    "GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL": r"Cost_{direct,ann}",

    # Total economic burden of disease globally (medical + prod...
    # Unit: USD/year
    "GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL": r"Burden_{ann}",

    # Economic value of human life lost to disease annually (mo...
    # Unit: USD/year
    "GLOBAL_DISEASE_HUMAN_LIFE_VALUE_LOSS_ANNUAL": r"Loss_{human,ann}",

    # Annual productivity loss from disease globally (absenteei...
    # Unit: USD/year
    "GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL": r"Loss_{ann}",

    # Annual global government spending on interventional clini...
    # Unit: USD
    "GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL": r"Trials_{ann}",

    # Total global household wealth (2022/2023 estimate)
    # Unit: USD
    "GLOBAL_HOUSEHOLD_WEALTH_USD": r"Household_{global}",

    # Annual global industry spending on clinical trials (Total...
    # Unit: USD
    "GLOBAL_INDUSTRY_CLINICAL_TRIALS_SPENDING_ANNUAL": r"Trials_{ann}",

    # Global life expectancy (2024)
    # Unit: years
    "GLOBAL_LIFE_EXPECTANCY_2024": r"Life_{global}",

    # Global government medical research spending
    # Unit: USD
    "GLOBAL_MED_RESEARCH_SPENDING": r"Spending_{global}",

    # Global military spending in 2024
    # Unit: USD
    "GLOBAL_MILITARY_SPENDING_ANNUAL_2024": r"Spending_{mil,ann}",

    # Per capita military spending globally
    # Unit: USD/person/year
    "GLOBAL_MILITARY_SPENDING_PER_CAPITA_ANNUAL": r"Spending_{percap,ann}",

    # Global military spending after 1% treaty reduction
    # Unit: USD/year
    "GLOBAL_MILITARY_SPENDING_POST_TREATY_ANNUAL_2024": r"Spending_{mil,ann}",

    # Annual global nonprofit spending on clinical trials (foun...
    # Unit: USD
    "GLOBAL_NONPROFIT_CLINICAL_TRIALS_SPENDING_ANNUAL": r"Trials_{ann}",

    # Total global pharmaceutical R&D spending ($300B annually,...
    # Unit: USD
    "GLOBAL_PHARMA_RD_SPENDING_ANNUAL": r"Spending_{ann}",

    # Global population in 2024
    # Unit: of people
    "GLOBAL_POPULATION_2024": r"Population_{global}",

    # Critical mass threshold for social change (3.5% rule)
    # Unit: rate
    "GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT": r"Threshold_{global}",

    # Annual global spending on symptomatic disease treatment
    # Unit: USD/year
    "GLOBAL_SYMPTOMATIC_DISEASE_TREATMENT_ANNUAL": r"Spending_{sympt,ann}",

    # Total annual cost of war and disease with all externaliti...
    # Unit: USD/year
    "GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL": r"Cost_{total}",

    # Proportion of global DALYs that are YLD (years lived with...
    # Unit: proportion
    "GLOBAL_YLD_PROPORTION_OF_DALYS": r"DALYs_{global}",


    # === HUMAN (3 parameters) ===
    # Estimated total economic impact of Human Genome Project
    # Unit: USD
    "HUMAN_GENOME_PROJECT_TOTAL_ECONOMIC_IMPACT": r"Human_{total}",

    # Percentage of human interactome (protein-protein interact...
    # Unit: percentage
    "HUMAN_INTERACTOME_TARGETED_PCT": r"Human",

    # Human protein-coding genes targetable by gene therapy, mR...
    # Unit: genes
    "HUMAN_PROTEIN_CODING_GENES": r"Human",


    # === IAB (7 parameters) ===
    # Base case estimate for bootstrap campaign cost
    # Unit: USD
    "IAB_BOOTSTRAP_CAMPAIGN_COST_BASE_USD": r"Cost_{camp}",

    # Conservative estimate for bootstrap campaign cost
    # Unit: USD
    "IAB_BOOTSTRAP_CAMPAIGN_COST_CONSERVATIVE_USD": r"Cost_{camp}",

    # Optimistic estimate for bootstrap campaign cost
    # Unit: USD
    "IAB_BOOTSTRAP_CAMPAIGN_COST_OPTIMISTIC_USD": r"Cost_{camp}",

    # Estimated annual cost of the IAB mechanism (high-end esti...
    # Unit: USD/year
    "IAB_MECHANISM_ANNUAL_COST": r"Cost_{ann}",

    # Benefit-Cost Ratio of the IAB mechanism itself
    # Unit: ratio
    "IAB_MECHANISM_BENEFIT_COST_RATIO": r"Cost",

    # Annual funding for IAB political incentive mechanism (ind...
    # Unit: USD/year
    "IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL": r"Funding_{ann}",

    # Percentage of treaty funding allocated to Incentive Align...
    # Unit: rate
    "IAB_POLITICAL_INCENTIVE_FUNDING_PCT": r"Funding",


    # === ICD (1 parameters) ===
    # Total ICD-10 diagnostic codes for human diseases and cond...
    # Unit: codes
    "ICD_10_TOTAL_CODES": r"Icd_{total}",


    # === INDUSTRY (1 parameters) ===
    # Ratio of Industry to Government spending on clinical tria...
    # Unit: ratio
    "INDUSTRY_VS_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO": r"Ratio",


    # === INSTITUTIONAL (1 parameters) ===
    # Minimum investment for institutional investors
    # Unit: USD
    "INSTITUTIONAL_INVESTOR_MIN": r"Institutional",


    # === LIFE (3 parameters) ===
    # US life expectancy linear gain rate 1883-1962 (pre-Kefauv...
    # Unit: years/decade
    "LIFE_EXPECTANCY_GAIN_1883_1962_YEARS_PER_DECADE": r"Rate",

    # US life expectancy linear gain rate 1962-2019 (post-Kefau...
    # Unit: years/decade
    "LIFE_EXPECTANCY_GAIN_1962_2019_YEARS_PER_DECADE": r"Rate",

    # Expected years of life extension from 1% treaty research ...
    # Unit: years
    "LIFE_EXTENSION_YEARS": r"Ratio",


    # === LOBBYIST (3 parameters) ===
    # Maximum bond investment for lobbyist incentives
    # Unit: USD
    "LOBBYIST_BOND_INVESTMENT_MAX": r"Lobbyist",

    # Maximum annual lobbyist salary range
    # Unit: USD
    "LOBBYIST_SALARY_MAX": r"Lobbyist",

    # Minimum annual lobbyist salary range
    # Unit: USD
    "LOBBYIST_SALARY_MIN_K": r"Lobbyist",


    # === MEASLES (1 parameters) ===
    # Return on investment from measles (MMR) vaccination programs
    # Unit: ratio
    "MEASLES_VACCINATION_ROI": r"ROI",


    # === MEDICAL (1 parameters) ===
    # Medical research spending as percentage of total disease ...
    # Unit: rate
    "MEDICAL_RESEARCH_PCT_OF_DISEASE_BURDEN": r"Burden_{RD}",


    # === MENTAL (1 parameters) ===
    # Annual productivity loss per capita from mental health is...
    # Unit: USD/year
    "MENTAL_HEALTH_PRODUCTIVITY_LOSS_PER_CAPITA": r"Loss_{percap,health}",


    # === MILITARY (3 parameters) ===
    # Ratio of global military spending to all clinical trials ...
    # Unit: ratio
    "MILITARY_TO_CLINICAL_TRIALS_SPENDING_RATIO": r"Ratio_{mil}",

    # Ratio of global military spending to government clinical ...
    # Unit: ratio
    "MILITARY_TO_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO": r"Ratio_{mil}",

    # Ratio of military spending to medical research spending
    # Unit: ratio
    "MILITARY_VS_MEDICAL_RESEARCH_RATIO": r"Ratio_{mil,RD}",


    # === MISALLOCATION (1 parameters) ===
    # Misallocation factor: cost to kill vs cost to save
    # Unit: ratio
    "MISALLOCATION_FACTOR_DEATH_VS_SAVING": r"Cost",


    # === MRNA (1 parameters) ===
    # mRNA therapeutic combinations (protein replacement, vacci...
    # Unit: combinations
    "MRNA_THERAPEUTIC_COMBINATIONS": r"Mrna",


    # === NEW (1 parameters) ===
    # Number of diseases that receive their FIRST effective tre...
    # Unit: diseases/year
    "NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR": r"New",


    # === NIH (3 parameters) ===
    # NIH annual budget (FY2024/2025)
    # Unit: USD
    "NIH_ANNUAL_BUDGET": r"Nih_{annual}",

    # Percentage of NIH budget spent on clinical trials (3.3%)
    # Unit: percentage
    "NIH_CLINICAL_TRIALS_SPENDING_PCT": r"Trials",

    # Typical cost per QALY for standard NIH-funded medical res...
    # Unit: USD/QALY
    "NIH_STANDARD_RESEARCH_COST_PER_QALY": r"Cost_{RD}",


    # === NPV (2 parameters) ===
    # Standard discount rate for NPV analysis (3% annual, socia...
    # Unit: rate
    "NPV_DISCOUNT_RATE_STANDARD": r"Rate_{RD}",

    # Standard time horizon for NPV analysis
    # Unit: years
    "NPV_TIME_HORIZON_YEARS": r"Time_{NPV}",


    # === OXFORD (1 parameters) ===
    # Oxford RECOVERY trial duration (found life-saving treatme...
    # Unit: months
    "OXFORD_RECOVERY_TRIAL_DURATION_MONTHS": r"Ratio_{RD}",


    # === PATIENT (1 parameters) ===
    # Patient willingness to participate in drug trials (44.8% ...
    # Unit: percentage
    "PATIENT_WILLINGNESS_TRIAL_PARTICIPATION_PCT": r"Patients",


    # === PEACE (14 parameters) ===
    # Annual peace dividend from 1% reduction in total war costs
    # Unit: USD/year
    "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT": r"Cost_{soc,ann}",

    # Conflict reduction benefits from 1% less military spendin...
    # Unit: USD/year
    "PEACE_DIVIDEND_CONFLICT_REDUCTION": r"Benefit_{peace}",

    # Annual savings from 1% reduction in direct war costs
    # Unit: USD/year
    "PEACE_DIVIDEND_DIRECT_COSTS": r"Cost_{direct,peace}",

    # Direct fiscal savings from 1% military spending reduction...
    # Unit: USD/year
    "PEACE_DIVIDEND_DIRECT_FISCAL_SAVINGS": r"Savings_{direct,peace}",

    # Annual savings from 1% reduction in environmental damage
    # Unit: USD/year
    "PEACE_DIVIDEND_ENVIRONMENTAL": r"Savings_{env,peace}",

    # Annual savings from 1% reduction in human casualties
    # Unit: USD/year
    "PEACE_DIVIDEND_HUMAN_CASUALTIES": r"Savings_{human,peace}",

    # Annual savings from 1% reduction in indirect war costs
    # Unit: USD/year
    "PEACE_DIVIDEND_INDIRECT_COSTS": r"Cost_{indirect,peace}",

    # Annual savings from 1% reduction in infrastructure destru...
    # Unit: USD/year
    "PEACE_DIVIDEND_INFRASTRUCTURE": r"Savings_{infra,peace}",

    # Annual savings from 1% reduction in lost economic growth
    # Unit: USD/year
    "PEACE_DIVIDEND_LOST_ECONOMIC_GROWTH": r"Savings_{econ_growth,peace}",

    # Annual savings from 1% reduction in lost human capital
    # Unit: USD/year
    "PEACE_DIVIDEND_LOST_HUMAN_CAPITAL": r"Savings_{human_cap,peace}",

    # Annual savings from 1% reduction in PTSD and mental healt...
    # Unit: USD/year
    "PEACE_DIVIDEND_PTSD": r"Cost_{PTSD,peace}",

    # Annual savings from 1% reduction in refugee support costs
    # Unit: USD/year
    "PEACE_DIVIDEND_REFUGEE_SUPPORT": r"Cost_{ref,peace}",

    # Annual savings from 1% reduction in trade disruption
    # Unit: USD/year
    "PEACE_DIVIDEND_TRADE_DISRUPTION": r"Savings_{trade,peace}",

    # Annual savings from 1% reduction in veteran healthcare costs
    # Unit: USD/year
    "PEACE_DIVIDEND_VETERAN_HEALTHCARE": r"Cost_{vet,peace}",


    # === PER (2 parameters) ===
    # US per capita chronic disease cost
    # Unit: USD/person/year
    "PER_CAPITA_CHRONIC_DISEASE_COST": r"Cost_{percap,dis}",

    # US per capita mental health cost
    # Unit: USD/person/year
    "PER_CAPITA_MENTAL_HEALTH_COST": r"Cost_{percap,health}",


    # === PERSONAL (1 parameters) ===
    # Personal lifetime wealth benefit for a 30-year-old with $...
    # Unit: usd
    "PERSONAL_LIFETIME_WEALTH": r"Time",


    # === PHARMA (5 parameters) ===
    # Average cost to develop one drug in current system
    # Unit: USD
    "PHARMA_DRUG_DEVELOPMENT_COST_CURRENT": r"Cost_{curr}",

    # Median lifetime revenue per successful drug (study of 361...
    # Unit: USD
    "PHARMA_DRUG_REVENUE_AVERAGE_CURRENT": r"Pharma_{current}",

    # Average Phase 2/3 efficacy testing cost per drug that pha...
    # Unit: USD
    "PHARMA_PHASE_2_3_COST_BARRIER": r"Cost",

    # ROI for pharma R&D (2022 historic low from Deloitte study...
    # Unit: percentage
    "PHARMA_ROI_CURRENT_SYSTEM_PCT": r"ROI_{curr}",

    # Percentage of drugs that reach market in current system
    # Unit: percentage
    "PHARMA_SUCCESS_RATE_CURRENT_PCT": r"Rate_{curr}",


    # === PHASE (4 parameters) ===
    # Investigational compounds that have passed Phase I global...
    # Unit: compounds
    "PHASE_1_PASSED_COMPOUNDS_GLOBAL": r"Phase_{global}",

    # Phase I safety trial duration
    # Unit: years
    "PHASE_1_SAFETY_DURATION_YEARS": r"Ratio",

    # Percentage of total clinical trial spending on Phase 2/3 ...
    # Unit: percentage
    "PHASE_2_3_CLINICAL_TRIAL_COST_PCT": r"Cost",

    # Phase 3 trial total cost (minimum)
    # Unit: USD/trial
    "PHASE_3_TRIAL_COST_MIN": r"Cost",


    # === PMC (1 parameters) ===
    # Median cost per patient in embedded pragmatic clinical tr...
    # Unit: USD/patient
    "PMC_PRAGMATIC_TRIAL_MEDIAN_COST_PER_PATIENT": r"Cost",


    # === POLIO (1 parameters) ===
    # Return on investment from sustaining polio vaccination as...
    # Unit: ratio
    "POLIO_VACCINATION_ROI": r"ROI",


    # === POLITICAL (1 parameters) ===
    # Estimated probability of treaty ratification and sustaine...
    # Unit: rate
    "POLITICAL_SUCCESS_PROBABILITY": r"Probability",


    # === POST (2 parameters) ===
    # Reduction in new drug approvals after 1962 Kefauver-Harri...
    # Unit: percentage
    "POST_1962_DRUG_APPROVAL_REDUCTION_PCT": r"Reduction",

    # Percentage military spending cut after WW2 (historical pr...
    # Unit: rate
    "POST_WW2_MILITARY_CUT_PCT": r"Spending_{mil}",


    # === PRAGMATIC (2 parameters) ===
    # Cost per QALY for pragmatic platform trials, calculated f...
    # Unit: USD/QALY
    "PRAGMATIC_TRIAL_COST_PER_QALY": r"Cost",

    # How many times more cost-effective pragmatic trials are v...
    # Unit: ratio
    "PRAGMATIC_VS_NIH_EFFICIENCY_MULTIPLIER": r"Multiplier",


    # === PRE (4 parameters) ===
    # Average drug development cost before 1962 FDA efficacy re...
    # Unit: USD_1980
    "PRE_1962_DRUG_DEVELOPMENT_COST_1980_USD": r"Cost_{pre62}",

    # Pre-1962 drug development cost adjusted to 2024 dollars (...
    # Unit: USD
    "PRE_1962_DRUG_DEVELOPMENT_COST_2024_USD": r"Cost_{pre62}",

    # Estimated physicians conducting real-world efficacy trial...
    # Unit: physicians
    "PRE_1962_PHYSICIAN_COUNT": r"Pre",

    # Years of empirical validation for physician-led pragmatic...
    # Unit: years
    "PRE_1962_VALIDATION_YEARS": r"Pre",


    # === QALYS (1 parameters) ===
    # Average QALYs gained per COVID death averted. Conservativ...
    # Unit: QALYs/death
    "QALYS_PER_COVID_DEATH_AVERTED": r"Deaths",


    # === RARE (1 parameters) ===
    # Total number of rare diseases globally
    # Unit: diseases
    "RARE_DISEASES_COUNT_GLOBAL": r"Rare_{global}",


    # === RECOVERY (5 parameters) ===
    # RECOVERY trial cost per patient. Note: RECOVERY was an ou...
    # Unit: USD/patient
    "RECOVERY_TRIAL_COST_PER_PATIENT": r"Cost",

    # Cost reduction factor demonstrated by RECOVERY trial ($41...
    # Unit: multiplier
    "RECOVERY_TRIAL_COST_REDUCTION_FACTOR": r"Cost",

    # Estimated lives saved globally by RECOVERY trial's dexame...
    # Unit: lives
    "RECOVERY_TRIAL_GLOBAL_LIVES_SAVED": r"Trials_{global}",

    # Total cost of UK RECOVERY trial. Enrolled tens of thousan...
    # Unit: USD
    "RECOVERY_TRIAL_TOTAL_COST": r"Cost_{total}",

    # Total QALYs generated by RECOVERY trial's discoveries (li...
    # Unit: QALYs
    "RECOVERY_TRIAL_TOTAL_QALYS_GENERATED": r"Rate_{total}",


    # === REGULATORY (2 parameters) ===
    # Mean age of preventable death from post-safety efficacy t...
    # Unit: years
    "REGULATORY_DELAY_MEAN_AGE_OF_DEATH": r"Deaths_{reg}",

    # Pre-death suffering period during post-safety efficacy te...
    # Unit: years
    "REGULATORY_DELAY_SUFFERING_PERIOD_YEARS": r"Deaths_{reg}",


    # === SAFE (1 parameters) ===
    # Total safe compounds available for repurposing (FDA-appro...
    # Unit: compounds
    "SAFE_COMPOUNDS_COUNT": r"Safe",


    # === SMALLPOX (2 parameters) ===
    # Return on investment from smallpox eradication campaign
    # Unit: ratio
    "SMALLPOX_ERADICATION_ROI": r"ROI",

    # Total economic benefit from smallpox eradication campaign
    # Unit: USD
    "SMALLPOX_ERADICATION_TOTAL_BENEFIT": r"Benefit_{total}",


    # === SMOKING (1 parameters) ===
    # Estimated annual global economic benefit from smoking ces...
    # Unit: USD/year
    "SMOKING_CESSATION_ANNUAL_BENEFIT": r"Benefit_{ann}",


    # === STANDARD (2 parameters) ===
    # Standard economic value per QALY
    # Unit: USD/QALY
    "STANDARD_ECONOMIC_QALY_VALUE_USD": r"QALYs_{RD}",

    # Standard QALYs per life saved (WHO life tables)
    # Unit: QALYs/life
    "STANDARD_QALYS_PER_LIFE_SAVED": r"QALYs_{RD}",


    # === STATUS (2 parameters) ===
    # Average years until first treatment discovered for a typi...
    # Unit: years
    "STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT": r"Status",

    # Years to clear entire queue of diseases without treatment...
    # Unit: years
    "STATUS_QUO_QUEUE_CLEARANCE_YEARS": r"Time",


    # === SUGAR (1 parameters) ===
    # Annual cost of sugar subsidies per person
    # Unit: USD/person/year
    "SUGAR_SUBSIDY_COST_PER_PERSON_ANNUAL": r"Subsidies_{ann}",


    # === SWITZERLAND (2 parameters) ===
    # Switzerland's defense spending as percentage of GDP (0.7%)
    # Unit: rate
    "SWITZERLAND_DEFENSE_SPENDING_PCT": r"Spending",

    # Switzerland GDP per capita
    # Unit: USD
    "SWITZERLAND_GDP_PER_CAPITA_K": r"SwitzerlandGDP",


    # === TERRORISM (1 parameters) ===
    # Deaths from 9/11 terrorist attacks
    # Unit: deaths
    "TERRORISM_DEATHS_911": r"Deaths_{terror}",


    # === TESTED (1 parameters) ===
    # Estimated drug-disease relationships actually tested (app...
    # Unit: relationships
    "TESTED_RELATIONSHIPS_ESTIMATE": r"Tested",


    # === THALIDOMIDE (11 parameters) ===
    # Total thalidomide birth defect cases worldwide (1957-1962)
    # Unit: cases
    "THALIDOMIDE_CASES_WORLDWIDE": r"Thalidomide",

    # Total DALYs per US-scale thalidomide event (YLL + YLD)
    # Unit: DALYs
    "THALIDOMIDE_DALYS_PER_EVENT": r"DALYs",

    # Deaths per US-scale thalidomide event
    # Unit: deaths
    "THALIDOMIDE_DEATHS_PER_EVENT": r"Deaths",

    # Disability weight for thalidomide survivors (limb deformi...
    # Unit: ratio
    "THALIDOMIDE_DISABILITY_WEIGHT": r"Thalidomide",

    # Mortality rate for thalidomide-affected infants (died wit...
    # Unit: percentage
    "THALIDOMIDE_MORTALITY_RATE": r"Rate",

    # Survivors per US-scale thalidomide event
    # Unit: cases
    "THALIDOMIDE_SURVIVORS_PER_EVENT": r"Thalidomide",

    # Average lifespan for thalidomide survivors
    # Unit: years
    "THALIDOMIDE_SURVIVOR_LIFESPAN": r"Thalidomide",

    # Estimated US thalidomide cases prevented by FDA rejection
    # Unit: cases
    "THALIDOMIDE_US_CASES_PREVENTED": r"ThalidomideUS",

    # US share of world population in 1960
    # Unit: percentage
    "THALIDOMIDE_US_POPULATION_SHARE_1960": r"Population",

    # Years Lived with Disability per thalidomide event
    # Unit: years
    "THALIDOMIDE_YLD_PER_EVENT": r"YLD",

    # Years of Life Lost per thalidomide event (infant deaths)
    # Unit: years
    "THALIDOMIDE_YLL_PER_EVENT": r"YLL",


    # === TOTAL (3 parameters) ===
    # Total words in the book
    # Unit: words
    "TOTAL_BOOK_WORDS": r"Book_{total}",

    # Total global research funding (baseline + 1% treaty funding)
    # Unit: USD
    "TOTAL_RESEARCH_FUNDING_WITH_TREATY": r"Funding_{total}",

    # Total testable therapeutic combinations (known safe compo...
    # Unit: combinations
    "TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS": r"Testable_{total}",


    # === TRADITIONAL (1 parameters) ===
    # Phase 3 cost per patient (median from FDA study)
    # Unit: USD/patient
    "TRADITIONAL_PHASE3_COST_PER_PATIENT": r"Cost",


    # === TREATMENT (1 parameters) ===
    # Traditional FDA drug development timeline
    # Unit: years
    "TREATMENT_ACCELERATION_YEARS_CURRENT": r"Ratio_{curr}",


    # === TREATY (24 parameters) ===
    # Treaty system benefit multiplier vs childhood vaccination...
    # Unit: ratio
    "TREATY_BENEFIT_MULTIPLIER_VS_VACCINES": r"Multiplier_{treaty}",

    # Amortized annual campaign cost (total cost ÷ campaign dur...
    # Unit: USD/year
    "TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED": r"Cost_{camp,ann}",

    # Political lobbying campaign: direct lobbying (US/EU/G20),...
    # Unit: USD
    "TREATY_CAMPAIGN_BUDGET_LOBBYING": r"Campaign_{camp,treaty}",

    # Reserve fund / contingency buffer (10% of total campaign ...
    # Unit: USD
    "TREATY_CAMPAIGN_BUDGET_RESERVE": r"Campaign_{camp,treaty}",

    # Campaign budget for Super PACs and political lobbying
    # Unit: USD
    "TREATY_CAMPAIGN_BUDGET_SUPER_PACS": r"Campaign_{camp,treaty}",

    # Treaty campaign duration (3-5 year range, using midpoint)
    # Unit: years
    "TREATY_CAMPAIGN_DURATION_YEARS": r"Ratio_{camp,treaty}",

    # Total treaty campaign cost (100% VICTORY Incentive Alignm...
    # Unit: USD
    "TREATY_CAMPAIGN_TOTAL_COST": r"Cost_{camp,total}",

    # Viral referendum budget for 280M verified votes (base: $2...
    # Unit: USD
    "TREATY_CAMPAIGN_VIRAL_REFERENDUM_BASE_CASE": r"Campaign_{camp,treaty}",

    # Target voting bloc size for campaign (3.5% of global popu...
    # Unit: of people
    "TREATY_CAMPAIGN_VOTING_BLOC_TARGET": r"Campaign_{camp,treaty}",

    # Cost per DALY averted from elimination of efficacy lag pl...
    # Unit: USD/DALY
    "TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG": r"Increase_{max,treaty}",

    # Expected cost per DALY accounting for political success p...
    # Unit: USD/DALY
    "TREATY_EXPECTED_COST_PER_DALY": r"Cost_{treaty}",

    # Expected ROI for 1% treaty accounting for political succe...
    # Unit: ratio
    "TREATY_EXPECTED_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG": r"ROI_{max,treaty}",

    # Expected value multiplier vs bed nets (accounts for polit...
    # Unit: ratio
    "TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER": r"Multiplier_{net,treaty}",

    # Annual lives saved from 1% reduction in conflict deaths
    # Unit: lives/year
    "TREATY_LIVES_SAVED_ANNUAL_GLOBAL": r"Deaths_{ann}",

    # Basic annual benefits: peace dividend + Decentralized Fra...
    # Unit: USD/year
    "TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS": r"Benefit_{ann}",

    # Annual QALYs gained from peace dividend (lives saved × QA...
    # Unit: QALYs/year
    "TREATY_QALYS_GAINED_ANNUAL_GLOBAL": r"Dividend_{ann}",

    # Truly recurring annual benefits from 1% treaty: peace div...
    # Unit: USD/year
    "TREATY_RECURRING_BENEFITS_ANNUAL": r"Benefit_{ann}",

    # ROI when redirecting existing spending (no new costs = in...
    # Unit: ratio
    "TREATY_REDIRECTED_SPENDING_INFINITE_ROI": r"ROI_{direct,treaty}",

    # 1% reduction in military spending/war costs from treaty
    # Unit: rate
    "TREATY_REDUCTION_PCT": r"Reduction_{treaty}",

    # Treaty ROI based on historical rate of drug development (...
    # Unit: ratio
    "TREATY_ROI_EXISTING_DRUGS_ONLY": r"ROI_{treaty}",

    # Treaty ROI from elimination of efficacy lag plus earlier ...
    # Unit: ratio
    "TREATY_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG": r"Increase_{max,treaty}",

    # Total annual system costs (campaign + Decentralized Frame...
    # Unit: USD/year
    "TREATY_TOTAL_ANNUAL_COSTS": r"Cost_{total}",

    # How many times more cost-effective than bed nets (using $...
    # Unit: ratio
    "TREATY_VS_BED_NETS_MULTIPLIER": r"Multiplier_{net,treaty}",

    # How many times more cost-effective the treaty campaign is...
    # Unit: ratio
    "TREATY_VS_DIRECT_FUNDING_LEVERAGE": r"Funding_{direct,treaty}",


    # === TRIAL (2 parameters) ===
    # Cumulative trial-capacity-equivalent years over 20-year p...
    # Unit: years
    "TRIAL_CAPACITY_CUMULATIVE_YEARS_20YR": r"Capacity",

    # Consolidated count of trial-relevant diseases worth targe...
    # Unit: diseases
    "TRIAL_RELEVANT_DISEASES_COUNT": r"Trials_{dis}",


    # === TYPE (2 parameters) ===
    # Ratio of Type II error cost to Type I error benefit (harm...
    # Unit: ratio
    "TYPE_II_ERROR_COST_RATIO": r"Cost",

    # Maximum DALYs saved by FDA preventing unsafe drugs over 6...
    # Unit: DALYs
    "TYPE_I_ERROR_BENEFIT_DALYS": r"DALYs",


    # === TYPICAL (1 parameters) ===
    # Typical CEO hourly rate
    # Unit: USD/hour
    "TYPICAL_CEO_HOURLY_RATE": r"Rate",


    # === UNEXPLORED (1 parameters) ===
    # Fraction of possible drug-disease space that remains unex...
    # Unit: percentage
    "UNEXPLORED_RATIO": r"Ratio",


    # === US (12 parameters) ===
    # Annual US cost of Alzheimer's disease (direct and indirect)
    # Unit: USD
    "US_ALZHEIMERS_ANNUAL_COST": r"Cost_{alz,ann}",

    # Annual US cost of cancer (direct and indirect)
    # Unit: USD
    "US_CANCER_ANNUAL_COST": r"Cost_{cancer,ann}",

    # US annual chronic disease spending
    # Unit: USD/year
    "US_CHRONIC_DISEASE_SPENDING_ANNUAL": r"Spending_{chronic,ann}",

    # Annual US cost of diabetes (direct and indirect)
    # Unit: USD
    "US_DIABETES_ANNUAL_COST": r"Cost_{diab,ann}",

    # Annual US cost of heart disease and stroke (direct and in...
    # Unit: USD
    "US_HEART_DISEASE_ANNUAL_COST": r"Cost_{heart,ann}",

    # US life expectancy in 1880 (closest available data point ...
    # Unit: years
    "US_LIFE_EXPECTANCY_1880": r"US",

    # US life expectancy in 1962 (year of Kefauver-Harris Amend...
    # Unit: years
    "US_LIFE_EXPECTANCY_1962": r"US",

    # US life expectancy in 2019 (latest available data).
    # Unit: years
    "US_LIFE_EXPECTANCY_2019": r"US",

    # Total annual US cost of major diseases (diabetes, Alzheim...
    # Unit: USD
    "US_MAJOR_DISEASES_TOTAL_ANNUAL_COST": r"Cost_{total}",

    # US mental health costs (treatment + productivity loss)
    # Unit: USD/year
    "US_MENTAL_HEALTH_COST_ANNUAL": r"Cost_{mental,ann}",

    # US military spending as percentage of GDP (2024)
    # Unit: rate
    "US_MILITARY_SPENDING_PCT_GDP": r"Spending_{mil}",

    # US population in 2024
    # Unit: people
    "US_POPULATION_2024": r"Population",


    # === VALLEY (1 parameters) ===
    # Percentage of promising Phase 1-passed compounds abandone...
    # Unit: percentage
    "VALLEY_OF_DEATH_ATTRITION_PCT": r"Deaths",


    # === VALUE (1 parameters) ===
    # Value of Statistical Life (conservative estimate)
    # Unit: USD
    "VALUE_OF_STATISTICAL_LIFE": r"Value",


    # === VICTORY (3 parameters) ===
    # Annual VICTORY Incentive Alignment Bond payout (treaty fu...
    # Unit: USD/year
    "VICTORY_BOND_ANNUAL_PAYOUT": r"Victory_{annual}",

    # Annual return percentage for VICTORY Incentive Alignment ...
    # Unit: rate
    "VICTORY_BOND_ANNUAL_RETURN_PCT": r"Victory_{annual}",

    # Percentage of captured dividend funding VICTORY Incentive...
    # Unit: rate
    "VICTORY_BOND_FUNDING_PCT": r"Funding",


    # === VITAMIN (1 parameters) ===
    # Cost per DALY for vitamin A supplementation programs (Ind...
    # Unit: USD/DALY
    "VITAMIN_A_COST_PER_DALY": r"Cost",


    # === WATER (2 parameters) ===
    # Estimated annual global economic benefit from water fluor...
    # Unit: USD/year
    "WATER_FLUORIDATION_ANNUAL_BENEFIT": r"Benefit_{water,ann}",

    # Return on investment from water fluoridation programs
    # Unit: ratio
    "WATER_FLUORIDATION_ROI": r"ROI_{water}",


    # === WHO (1 parameters) ===
    # Cost-effectiveness threshold widely used in US health eco...
    # Unit: USD/QALY
    "WHO_QALY_THRESHOLD_COST_EFFECTIVE": r"Cost",


    # === WILLING (1 parameters) ===
    # Global chronic disease patients willing to participate in...
    # Unit: people
    "WILLING_TRIAL_PARTICIPANTS_GLOBAL": r"Patients_{global}",


    # === WORKFORCE (1 parameters) ===
    # Percentage of workforce experiencing productivity loss fr...
    # Unit: rate
    "WORKFORCE_WITH_PRODUCTIVITY_LOSS": r"Loss",

}
