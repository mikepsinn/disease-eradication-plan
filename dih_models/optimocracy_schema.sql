-- =============================================================================
-- OPTIMOCRACY DATABASE SCHEMA
-- =============================================================================
-- Policy-outcome relationship database for evidence-based governance
-- Mirrors DFDA schema structure but adapted for policy analysis
--
-- Key differences from DFDA:
-- 1. "Treatments" → "Policies" (laws, regulations, budgets, taxes)
-- 2. "Users" → "Jurisdictions" (countries, states, cities, districts)
-- 3. "Health outcomes" → "Welfare outcomes" (life expectancy, income, etc.)
-- 4. N-of-1 analysis → Synthetic control / difference-in-differences
-- =============================================================================

-- -----------------------------------------------------------------------------
-- CORE ENTITIES
-- -----------------------------------------------------------------------------

-- Jurisdictions (analogous to DFDA users)
-- Countries, states, provinces, cities, counties, school districts, etc.
CREATE TABLE jurisdictions (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    jurisdiction_type ENUM('country', 'state', 'province', 'city', 'county',
                           'municipality', 'school_district', 'special_district'),
    parent_jurisdiction_id INT REFERENCES jurisdictions(id),  -- hierarchical
    iso_code VARCHAR(10),  -- ISO 3166-1/2 where applicable
    population INT,
    area_km2 FLOAT,
    gdp_per_capita FLOAT,

    -- For synthetic control matching
    latitude FLOAT,
    longitude FLOAT,
    urban_pct FLOAT,
    median_age FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Policy categories (analogous to DFDA variable categories)
CREATE TABLE policy_categories (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_category_id INT REFERENCES policy_categories(id),
    description TEXT,

    -- Examples: healthcare, education, criminal_justice, taxation,
    -- housing, environment, labor, trade, defense, immigration
    domain ENUM('healthcare', 'education', 'criminal_justice', 'taxation',
                'housing', 'environment', 'labor', 'trade', 'defense',
                'immigration', 'monetary', 'social_welfare', 'infrastructure',
                'technology', 'agriculture', 'energy', 'other')
);

-- Policies (analogous to DFDA treatments/predictors)
CREATE TABLE policies (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    policy_category_id INT REFERENCES policy_categories(id),

    -- Policy type affects analysis method
    policy_type ENUM(
        'law',              -- Statutory law passed by legislature
        'regulation',       -- Administrative rule by agency
        'executive_order',  -- Executive action
        'budget_allocation', -- Spending decision
        'tax_policy',       -- Tax rate, bracket, credit, deduction
        'court_ruling',     -- Judicial precedent
        'treaty',           -- International agreement
        'local_ordinance'   -- Municipal rule
    ),

    -- Measurement characteristics
    is_continuous BOOLEAN DEFAULT FALSE,  -- Can be measured in degrees (e.g., tax rate)
    default_unit_id INT,  -- For continuous policies (e.g., "percent", "USD")
    binary_treatment BOOLEAN DEFAULT TRUE,  -- Most policies are on/off

    -- Temporal characteristics (from DFDA)
    typical_onset_delay_days INT,  -- Expected delay before effect appears
    typical_duration_of_effect_years INT,  -- How long effect persists after repeal

    -- Policy text (for LLM parsing)
    canonical_text TEXT,  -- Full text of law/regulation
    summary TEXT,  -- LLM-generated or human summary

    -- Categorization
    valence ENUM('beneficial', 'harmful', 'neutral', 'contested'),
    controllable BOOLEAN DEFAULT TRUE,  -- Can jurisdictions choose this?

    -- Linking
    related_policy_ids JSON,  -- Often policies come in bundles
    superseded_by_id INT REFERENCES policies(id),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Outcome variables (analogous to DFDA outcome variables)
CREATE TABLE outcome_variables (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category ENUM('health', 'economic', 'education', 'safety', 'environment',
                  'governance', 'social', 'composite'),

    -- Measurement
    default_unit_id INT,
    valence ENUM('higher_better', 'lower_better'),  -- Interpretation

    -- Examples:
    -- health: life_expectancy, infant_mortality, disease_prevalence
    -- economic: median_income, unemployment, gdp_growth, gini_coefficient
    -- education: test_scores, graduation_rates, literacy
    -- safety: crime_rate, traffic_deaths, workplace_injuries
    -- environment: air_quality, water_quality, emissions
    -- composite: HDI, life_satisfaction, welfare_index

    data_source VARCHAR(255),  -- WHO, World Bank, OECD, Census, etc.
    data_frequency ENUM('daily', 'weekly', 'monthly', 'quarterly', 'annual'),

    -- Quality flags
    is_primary_metric BOOLEAN,  -- Core welfare metric vs intermediate
    measurement_reliability ENUM('high', 'medium', 'low'),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Confounding variables (things that affect outcomes but aren't the policy)
CREATE TABLE confounders (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category ENUM('economic', 'demographic', 'geographic', 'political',
                  'technological', 'cultural', 'neighboring_policy'),

    -- Examples:
    -- economic: oil_price, interest_rate, trade_balance
    -- demographic: age_distribution, immigration_rate, urbanization
    -- geographic: climate, natural_resources, coastal_access
    -- political: government_type, political_stability, corruption_index
    -- neighboring_policy: policies in adjacent jurisdictions (spillover)

    default_unit_id INT,
    data_source VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- TIME SERIES DATA
-- -----------------------------------------------------------------------------

-- Policy implementations (when/where policies were in effect)
CREATE TABLE policy_implementations (
    id BIGINT PRIMARY KEY,
    jurisdiction_id INT REFERENCES jurisdictions(id),
    policy_id INT REFERENCES policies(id),

    -- Temporal extent
    start_date DATE NOT NULL,
    end_date DATE,  -- NULL if still in effect

    -- For continuous policies (e.g., tax rates, spending levels)
    value FLOAT,  -- Policy intensity/level
    unit_id INT,

    -- Policy version/amendment tracking
    version INT DEFAULT 1,
    amendment_notes TEXT,

    -- Source documentation
    source_url VARCHAR(500),
    source_document TEXT,  -- PDF text or reference

    -- Quality
    confidence ENUM('high', 'medium', 'low'),  -- How certain are we of dates/values?

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(jurisdiction_id, policy_id, start_date, version)
);

-- Outcome measurements (time series of welfare metrics per jurisdiction)
CREATE TABLE outcome_measurements (
    id BIGINT PRIMARY KEY,
    jurisdiction_id INT REFERENCES jurisdictions(id),
    outcome_variable_id INT REFERENCES outcome_variables(id),

    -- Temporal
    measurement_date DATE NOT NULL,
    period_type ENUM('point', 'annual', 'quarterly', 'monthly'),

    -- Value
    value FLOAT NOT NULL,
    unit_id INT,

    -- Quality
    source_id INT,  -- Reference to data source
    is_estimated BOOLEAN DEFAULT FALSE,  -- Interpolated or imputed?
    confidence_interval_low FLOAT,
    confidence_interval_high FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(jurisdiction_id, outcome_variable_id, measurement_date)
);

-- Confounder measurements
CREATE TABLE confounder_measurements (
    id BIGINT PRIMARY KEY,
    jurisdiction_id INT REFERENCES jurisdictions(id),
    confounder_id INT REFERENCES confounders(id),

    measurement_date DATE NOT NULL,
    value FLOAT NOT NULL,
    unit_id INT,
    source_id INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(jurisdiction_id, confounder_id, measurement_date)
);

-- -----------------------------------------------------------------------------
-- ANALYSIS RESULTS (analogous to DFDA variable_relationships)
-- -----------------------------------------------------------------------------

-- Jurisdiction-level policy-outcome relationships
-- Analogous to DFDA user_variable_relationships
-- Results from synthetic control, DiD, event study, or RDD analysis
CREATE TABLE jurisdiction_policy_relationships (
    id BIGINT PRIMARY KEY,
    jurisdiction_id INT REFERENCES jurisdictions(id),
    policy_id INT REFERENCES policies(id),
    outcome_variable_id INT REFERENCES outcome_variables(id),

    -- Analysis method used
    analysis_method ENUM(
        'synthetic_control',      -- Abadie et al. method
        'difference_in_differences',  -- DiD with parallel trends
        'regression_discontinuity',   -- RDD at threshold
        'event_study',           -- Pre/post with leads/lags
        'interrupted_time_series',  -- ARIMA-based
        'simple_before_after',   -- Naive comparison (low confidence)
        'cross_sectional'        -- Snapshot comparison (lowest confidence)
    ),

    -- Effect estimate
    effect_estimate FLOAT,  -- Point estimate (% change or level change)
    effect_estimate_se FLOAT,  -- Standard error
    effect_estimate_ci_low FLOAT,  -- 95% CI lower
    effect_estimate_ci_high FLOAT,  -- 95% CI upper
    p_value FLOAT,

    -- Temporal dynamics
    estimated_onset_delay_days INT,  -- When did effect begin?
    estimated_duration_years FLOAT,  -- How long did effect last?
    effect_trajectory JSON,  -- Time series of effect estimates (event study)

    -- Pre-treatment fit (for synthetic control)
    pre_treatment_rmse FLOAT,  -- How well did control match pre-treatment?
    placebo_p_value FLOAT,  -- Permutation test p-value

    -- Parallel trends (for DiD)
    parallel_trends_test_stat FLOAT,
    parallel_trends_p_value FLOAT,

    -- Sample info
    pre_treatment_periods INT,
    post_treatment_periods INT,
    control_jurisdictions JSON,  -- List of control unit IDs

    -- Bradford Hill criteria scores (0-1 scale)
    -- Same as DFDA but applied to policy context
    hill_strength FLOAT,  -- Magnitude of association
    hill_consistency FLOAT,  -- Replicated across jurisdictions?
    hill_specificity FLOAT,  -- Specific to this outcome?
    hill_temporality FLOAT,  -- Policy preceded outcome change?
    hill_gradient FLOAT,  -- Dose-response (for continuous policies)
    hill_plausibility FLOAT,  -- Mechanistic explanation exists?
    hill_coherence FLOAT,  -- Consistent with other knowledge?
    hill_experiment FLOAT,  -- Experimental/quasi-experimental evidence?
    hill_analogy FLOAT,  -- Similar policies had similar effects?

    -- Composite scores
    causal_confidence_score FLOAT,  -- Aggregate Hill score
    policy_impact_score FLOAT,  -- PIS analog: effect × confidence

    -- Quality flags
    confounders_controlled JSON,  -- Which confounders were adjusted for
    potential_violations TEXT,  -- Known threats to validity

    -- Metadata
    analysis_date DATE,
    analyst_notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Global policy-outcome relationships (aggregated across jurisdictions)
-- Analogous to DFDA global_variable_relationships
CREATE TABLE global_policy_relationships (
    id BIGINT PRIMARY KEY,
    policy_id INT REFERENCES policies(id),
    outcome_variable_id INT REFERENCES outcome_variables(id),

    -- Aggregated effect estimate (meta-analysis of jurisdiction estimates)
    pooled_effect_estimate FLOAT,  -- Random-effects meta-analysis
    pooled_effect_se FLOAT,
    pooled_effect_ci_low FLOAT,
    pooled_effect_ci_high FLOAT,

    -- Heterogeneity
    i_squared FLOAT,  -- % variance due to heterogeneity
    tau_squared FLOAT,  -- Between-study variance
    q_statistic FLOAT,  -- Cochran's Q

    -- Sample
    number_of_jurisdictions INT,
    total_population_covered BIGINT,
    jurisdiction_types_included JSON,  -- e.g., ["state", "country"]

    -- Aggregated Hill criteria
    aggregate_causal_confidence FLOAT,
    aggregate_policy_impact_score FLOAT,

    -- Evidence quality
    evidence_grade ENUM('A', 'B', 'C', 'D', 'F'),  -- GRADE-style rating
    -- A: Multiple RCTs or high-quality quasi-experiments
    -- B: Single RCT or multiple quasi-experiments
    -- C: Well-designed observational studies
    -- D: Case studies or weak observational evidence
    -- F: Expert opinion only or conflicting evidence

    -- Confidence for different contexts
    confidence_high_income FLOAT,  -- Effect confidence in rich countries
    confidence_low_income FLOAT,  -- Effect confidence in poor countries
    confidence_federal FLOAT,  -- At national level
    confidence_subnational FLOAT,  -- At state/local level

    -- Recommendations
    recommended_for_trial BOOLEAN,  -- Strong enough signal for RCT?
    recommended_trial_design TEXT,  -- Suggested experimental approach
    recommended_jurisdictions JSON,  -- Good candidates for pilot

    -- Metadata
    last_updated DATE,
    number_of_studies INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- POLICY EXPERIMENTS (recommended and tracked)
-- -----------------------------------------------------------------------------

-- Natural experiments identified in historical data
CREATE TABLE natural_experiments (
    id INT PRIMARY KEY,
    policy_id INT REFERENCES policies(id),

    -- The quasi-experimental setup
    experiment_type ENUM(
        'border_discontinuity',   -- Adjacent jurisdictions differ
        'temporal_discontinuity', -- Policy changed abruptly
        'eligibility_threshold',  -- RDD at cutoff
        'staggered_adoption',     -- Different adoption times
        'lottery',                -- Random assignment (rare)
        'court_mandate',          -- Externally imposed change
        'natural_disaster'        -- Exogenous shock
    ),

    -- Jurisdictions involved
    treatment_jurisdictions JSON,
    control_jurisdictions JSON,

    -- Timing
    treatment_date DATE,
    pre_period_start DATE,
    post_period_end DATE,

    -- Quality assessment
    identification_strength ENUM('strong', 'moderate', 'weak'),
    parallel_trends_plausible BOOLEAN,
    no_anticipation BOOLEAN,  -- No behavioral change before treatment
    no_spillover BOOLEAN,  -- SUTVA satisfied

    -- Status
    analyzed BOOLEAN DEFAULT FALSE,
    analysis_id BIGINT REFERENCES jurisdiction_policy_relationships(id),

    notes TEXT,
    discovered_by VARCHAR(255),  -- Researcher or LLM system

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Recommended policy experiments (prospective)
CREATE TABLE recommended_experiments (
    id INT PRIMARY KEY,
    policy_id INT REFERENCES policies(id),
    outcome_variable_id INT REFERENCES outcome_variables(id),

    -- Why this experiment?
    prior_evidence_score FLOAT,  -- How strong is observational signal?
    expected_effect_size FLOAT,  -- Predicted effect magnitude
    uncertainty_reduction FLOAT,  -- How much would trial reduce uncertainty?

    -- Recommended design
    design_type ENUM('rct', 'cluster_rct', 'stepped_wedge', 'rdd', 'did'),
    recommended_jurisdictions JSON,  -- Good pilot locations
    recommended_sample_size INT,
    recommended_duration_months INT,
    estimated_cost FLOAT,

    -- Feasibility
    political_feasibility ENUM('high', 'medium', 'low'),
    ethical_concerns TEXT,
    legal_barriers TEXT,

    -- Priority
    value_of_information FLOAT,  -- Expected benefit from knowing true effect
    priority_rank INT,

    -- Status
    status ENUM('proposed', 'approved', 'in_progress', 'completed', 'rejected'),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- LLM PARSING AND TEXT ANALYSIS
-- -----------------------------------------------------------------------------

-- Policy text corpus (for LLM analysis)
CREATE TABLE policy_documents (
    id BIGINT PRIMARY KEY,
    policy_id INT REFERENCES policies(id),
    jurisdiction_id INT REFERENCES jurisdictions(id),

    -- Document info
    document_type ENUM('bill_text', 'regulation_text', 'court_opinion',
                       'executive_order', 'committee_report', 'amendment'),
    title VARCHAR(500),

    -- Full text
    full_text TEXT,
    text_length INT,

    -- Parsed metadata
    effective_date DATE,
    sponsors JSON,  -- Legislators who sponsored
    votes_for INT,
    votes_against INT,

    -- LLM analysis results
    llm_summary TEXT,
    llm_key_provisions JSON,  -- Structured extraction
    llm_predicted_effects JSON,  -- What outcomes might change?
    llm_similar_policies JSON,  -- Related policies in database
    llm_confidence FLOAT,

    -- Source
    source_url VARCHAR(500),
    retrieval_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Policy similarity matrix (LLM-computed)
CREATE TABLE policy_similarity (
    policy_id_1 INT REFERENCES policies(id),
    policy_id_2 INT REFERENCES policies(id),

    similarity_score FLOAT,  -- 0-1, cosine similarity of embeddings
    similarity_type ENUM('text', 'effect', 'mechanism', 'all'),

    computed_at TIMESTAMP,

    PRIMARY KEY (policy_id_1, policy_id_2, similarity_type)
);

-- -----------------------------------------------------------------------------
-- VIEWS AND INDEXES
-- -----------------------------------------------------------------------------

-- Top policy recommendations by expected impact
CREATE VIEW top_policy_recommendations AS
SELECT
    p.name AS policy_name,
    pc.name AS category,
    ov.name AS outcome,
    gpr.pooled_effect_estimate,
    gpr.evidence_grade,
    gpr.aggregate_policy_impact_score,
    gpr.recommended_for_trial
FROM global_policy_relationships gpr
JOIN policies p ON gpr.policy_id = p.id
JOIN policy_categories pc ON p.policy_category_id = pc.id
JOIN outcome_variables ov ON gpr.outcome_variable_id = ov.id
WHERE gpr.aggregate_policy_impact_score > 0.5
ORDER BY gpr.aggregate_policy_impact_score DESC;

-- Policy experiments ready for validation
CREATE VIEW experiments_ready_for_trial AS
SELECT
    re.id,
    p.name AS policy_name,
    ov.name AS outcome,
    re.prior_evidence_score,
    re.expected_effect_size,
    re.value_of_information,
    re.recommended_jurisdictions,
    re.estimated_cost
FROM recommended_experiments re
JOIN policies p ON re.policy_id = p.id
JOIN outcome_variables ov ON re.outcome_variable_id = ov.id
WHERE re.status = 'proposed'
  AND re.political_feasibility IN ('high', 'medium')
  AND re.value_of_information > 1000000  -- $1M+ expected value
ORDER BY re.value_of_information DESC;

-- Create indexes for common queries
CREATE INDEX idx_policy_impl_jurisdiction ON policy_implementations(jurisdiction_id);
CREATE INDEX idx_policy_impl_policy ON policy_implementations(policy_id);
CREATE INDEX idx_policy_impl_dates ON policy_implementations(start_date, end_date);
CREATE INDEX idx_outcome_meas_jurisdiction ON outcome_measurements(jurisdiction_id);
CREATE INDEX idx_outcome_meas_variable ON outcome_measurements(outcome_variable_id);
CREATE INDEX idx_outcome_meas_date ON outcome_measurements(measurement_date);
CREATE INDEX idx_jpr_policy ON jurisdiction_policy_relationships(policy_id);
CREATE INDEX idx_jpr_outcome ON jurisdiction_policy_relationships(outcome_variable_id);
CREATE INDEX idx_gpr_impact ON global_policy_relationships(aggregate_policy_impact_score);
