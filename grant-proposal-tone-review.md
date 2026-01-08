# Grant Proposal Tone Review - Foundation Standards

**Date:** 2026-01-08
**Reviewer:** Auto-Claude Agent
**Purpose:** Ensure all grant proposal content meets foundation program officer standards

## Review Criteria

- [ ] Professional and objective tone (no casual/satirical voice)
- [ ] Conservative estimates emphasized where available
- [ ] Claims properly hedged and cited
- [ ] Appropriate for philanthropic program officers
- [ ] No informal language that might concern foundations

## Files Reviewed

1. knowledge/grant-proposal/index.qmd
2. knowledge/grant-proposal/executive-summary.qmd
3. knowledge/grant-proposal/budget-breakdown.qmd
4. knowledge/grant-proposal/theory-of-change.qmd
5. knowledge/grant-proposal/evaluation-framework.qmd
6. knowledge/grant-proposal/organizational-capacity.qmd
7. knowledge/grant-proposal/risk-analysis.qmd
8. knowledge/grant-proposal/evidence-base.qmd

## Findings by Category

### 1. TONE - Overall Assessment: GOOD ✓

**Strengths:**
- Generally professional and objective throughout
- Academic style appropriate for foundation review
- Evidence-based approach with citations
- Clear structure and navigation

**Minor Issues to Address:**
- Some claims need additional hedging (see below)
- A few superlatives could be softened
- Some statements present projections as certainties

### 2. HEDGING & CLAIMS - Needs Improvement

**Issues Found:**

#### A. Overconfident Language (needs hedging):

**index.qmd:**
- "This intervention represents a unique opportunity" → Consider: "This intervention may represent an exceptional opportunity"
- "The 1% Treaty would generate" → "The 1% Treaty is projected to generate"
- "enabling foundations to track progress in real-time" → "designed to enable foundations to track progress"

**executive-summary.qmd:**
- "This proposal outlines a strategic campaign to establish" → Good (appropriate framing)
- "The intervention represents exceptional value" → "The intervention may represent exceptional value"
- "achieving cost-effectiveness of $0.84/DALY" → "with projected cost-effectiveness of $0.84/DALY"
- Line 24: "{{< var dfda_trial_capacity_plus_efficacy_lag_lives_saved >}} preventable deaths" → "estimated {{< var... >}}"

**budget-breakdown.qmd:**
- Line 27: "Once the treaty is ratified, it generates" → "Upon ratification, the treaty would generate"
- Line 81: "Target: {{< var treaty_campaign_voting_bloc_target >}} by end of Year 3" → Consider adding "goal" or "target"
- Line 258: "This means every $1 invested generates $27 annually" → "is projected to generate"

**theory-of-change.qmd:**
- Generally well-hedged with "projected", "target", etc.
- Some timeline statements could emphasize contingency more

**evaluation-framework.qmd:**
- Success criteria appropriately framed as targets
- Good use of "if-then" contingency language

**organizational-capacity.qmd:**
- "This architecture ensures" → "This architecture is designed to ensure"
- Track record section appropriately frames as "precedents" not guarantees

**risk-analysis.qmd:**
- Excellent transparent discussion of uncertainties
- Probability ranges well-documented
- Good use of scenario analysis

**evidence-base.qmd:**
- Generally well-cited and appropriately hedged
- Good use of "demonstrates feasibility" vs "guarantees success"

#### B. Absolute Statements (need probabilistic framing):

- "will save" → "is projected to save"
- "will generate" → "could generate" or "is expected to generate"
- "enables" → "designed to enable"
- "demonstrates" → "suggests" (where appropriate)

#### C. Superlatives (consider softening):

- "unprecedented opportunity" → "exceptional opportunity"
- "transformative" → keep (appropriate for grant context)
- "exceptional cost-effectiveness" → keep (backed by data)
- "world-class" → "experienced" or "expert"

### 3. CONSERVATIVE ESTIMATES - GOOD ✓

**Strengths:**
- Consistently uses median estimates, not optimistic projections
- 95% confidence intervals provided
- Monte Carlo uncertainty analysis documented
- Comparison to RECOVERY trial provides conservative benchmark

**Evidence of Conservative Approach:**
- Uses 40% success rate for "valley of death" compounds (industry average, not optimistic)
- Treaty passage probability acknowledges 30-40% failure risk
- Cost reduction target (82×) is validated by RECOVERY trial (3,867×)
- Excludes benefits beyond 13-year horizon
- Excludes peace dividend in primary cost-effectiveness metric

### 4. CITATIONS - EXCELLENT ✓

**Strengths:**
- 305 parameters with full source documentation
- Peer-reviewed sources (147/305 = 48%)
- Clear confidence levels (High/Medium/Low)
- Links to references.qmd and appendices
- GiveWell methodology followed
- WHO, SIPRI, FDA, EMA official sources

**Minor Enhancement:**
- Consider adding "According to [source]" language in more places for extra credibility

### 5. FOUNDATION-APPROPRIATE LANGUAGE - GOOD ✓

**Strengths:**
- Professional terminology throughout
- No casual or satirical voice
- Respectful of foundation program officers
- Academic rigor maintained
- Transparent about uncertainties

**No Major Concerns Found:**
- Language appropriate for grant submission
- Tone suitable for program officer review
- No informal expressions that would concern foundations

## Recommended Changes

### Priority 1: Add Hedging Language

**Pattern to Fix:** Absolute statements → Probabilistic/projected statements

Examples:
- "will" → "is projected to" / "could" / "is expected to"
- "generates" → "is projected to generate"
- "ensures" → "is designed to ensure"
- "enables" → "is designed to enable"
- "represents" → "may represent" (where claiming unique opportunity)

### Priority 2: Emphasize Conservative Nature

Add language emphasizing conservative assumptions:
- "Using conservative estimates, the intervention..."
- "Based on median projections (not optimistic scenarios)..."
- "Excluding benefits beyond the 13-year horizon..."

### Priority 3: Clarify Probability Statements

Ensure all major claims include uncertainty:
- "With 60-70% probability, the treaty campaign will..."
- "Assuming treaty passage (30-40% failure risk)..."
- "If the dFDA achieves the targeted cost reduction..."

### Priority 4: Minor Word Choice Improvements

Replace a few superlatives with more measured language:
- "unprecedented" → "exceptional" or "rare"
- "world-class" → "experienced" or "expert"
- Keep: "transformative", "exceptional cost-effectiveness" (backed by data)

## Files Requiring Edits

1. **index.qmd** - Minor hedging additions (5-7 changes)
2. **executive-summary.qmd** - Moderate hedging additions (10-15 changes)
3. **budget-breakdown.qmd** - Minor hedging additions (8-10 changes)
4. **theory-of-change.qmd** - Minor hedging additions (5-7 changes)
5. **evaluation-framework.qmd** - Minimal changes (2-3 areas)
6. **organizational-capacity.qmd** - Minor hedging additions (3-5 changes)
7. **risk-analysis.qmd** - Minimal changes (already well-hedged)
8. **evidence-base.qmd** - Minimal changes (already well-hedged)

## Overall Assessment

**Grade: A- (Excellent with Minor Improvements Needed)**

The grant proposal content is professional, well-researched, and largely appropriate for foundation program officers. The main improvement needed is adding probabilistic hedging language to make clear that projections are estimates, not guarantees.

**Strengths:**
- Professional academic tone throughout
- Comprehensive evidence base with citations
- Transparent about uncertainties and risks
- Conservative estimates emphasized
- Appropriate structure for grant review

**Areas for Improvement:**
- Add hedging language to ~30-40 instances across all files
- Emphasize probabilistic nature of projections
- Soften a few superlatives
- Add "projected" or "estimated" before key metrics

**Time to Complete Edits:** 1-2 hours to systematically review and edit all files

## Conclusion

The grant proposal content is nearly foundation-ready. With minor hedging improvements across ~30-40 statements, it will meet the highest standards for philanthropic program officer review. The content demonstrates academic rigor, transparency about uncertainties, and appropriate conservative framing.

**Recommendation:** Proceed with targeted edits to add hedging language, then submit for foundation review.
