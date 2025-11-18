# Economics.qmd Peer Review Improvement Plan

**Document**: `knowledge/economics/economics.qmd`
**Goal**: Prepare for academic peer review submission
**Status**: ⚠️ **~90% PEER-REVIEW READY** - Core structure complete, remaining economist critique responses in progress

---

## 📊 CURRENT STATUS

**Core Academic Structure**: ✅ **COMPLETE**
- Abstract, Methodology, Limitations, Hypothesis, Nomenclature, References all added
- Mathematical rigor verified, all calculations use parameters.py
- 435 parameters documented with confidence indicators

**Economist Critique Responses**: ⚠️ **MOSTLY COMPLETE**
- ✅ Expected value analysis (lines 627-656), general equilibrium (lines 1241-1262), peace dividend confidence levels (lines 445-449), discount rate sensitivity (lines 528-549)
- ✅ Partnership model (line 754), platform costs distinction (line 826), cost comparison table, observational trial images (lines 1109-1115)
- ✅ Pre-1962 context (lines 542-554), RECOVERY limitations (lines 1051-1062), time inconsistency (lines 607-626), counterfactual baseline (lines 413-429), regulatory risks (lines 1393-1477)
- ✅ QALY confidence levels (lines 1258, 1262, 1266), external validity (lines 1352-1369), comparison rationale (lines 1045-1067)
- ⏳ **Remaining**: Opportunity cost analysis (partial - has section but needs comparison to alternative uses), adoption realism (S-curve/coordination failure), publication bias note, Monte Carlo acknowledgment, variable verification

---

## PENDING TODOS

### High Priority

#### 15. ⚠️ Add Opportunity Cost Analysis (PARTIALLY COMPLETE)
**Location**: "Problem Statement and Opportunity Cost" section exists (line 946) but needs enhancement
**Status**: Section exists but focuses on current resource allocation rather than comparison to alternative uses of $27B
**Action**: Enhance existing section to explicitly compare to alternative interventions (direct treatment programs, public health infrastructure, other research priorities). Reference existing comparisons (GiveWell, vaccinations). Add note: "This analysis focuses on conditional benefits; comprehensive opportunity cost analysis would require separate study."

#### 16. ✅ Improve QALY Methodology with Confidence Levels - COMPLETED
**Location**: "QALY Calculation Uncertainties" section (lines 1258, 1262, 1266)
**Status**: COMPLETED - Confidence levels already documented (Stream A: High, Stream B: Medium, Stream C: Lower)

#### 17. ✅ Enhance External Validity Discussion - COMPLETED
**Location**: "External Validity Considerations" section (lines 1352-1369)
**Status**: COMPLETED - Section exists with transferability across contexts, temporal validity, and general equilibrium effects

#### 18. ⏳ Add Adoption Realism Discussion
**Location**: "Adoption Rate Assumptions" section (lines 516-525)
**Action**: Acknowledge S-curve adoption with critical mass threshold. Note coordination failure risk and mitigation (economic incentives align interests). Note regulatory harmonization may take 10-20 years, not 5.

### Medium Priority

#### 26. ⏳ Add Brief Note on Publication Bias
**Location**: "General Equilibrium Considerations" or "Pragmatic Trial Internal Validity" section
**Action**: Add 1-2 sentences: "Publication bias (negative results may not be published) is acknowledged. The dFDA's transparent data infrastructure may partially mitigate this risk, but bias remains a limitation."

#### 28. ⏳ Add Brief Note on Comparison Set Rationale
**Location**: "How This Compares to History" section (around line 840)
**Action**: Add 3-4 sentences explaining why comparison set includes interventions across multiple categories (charitable giving, public health, research investments, clinical care). Note: "GiveWell represents best-in-class efficiency for direct interventions; NIH represents comparable research investment with different efficiency profile. Both comparisons are relevant but answer different questions."

#### 29. ⏳ Acknowledge Inadequate Uncertainty Quantification (Monte Carlo)
**Location**: "Sensitivity Analysis Approach" section (lines 468-494) or Limitations section
**Action**: Add explicit acknowledgment: "This analysis uses scenario-based sensitivity analysis rather than probabilistic Monte Carlo simulation. Monte Carlo would require 2-3 weeks of additional development and is beyond scope. Scenario analysis provides bounds but not probabilistic confidence intervals."

#### 30. ⏳ Verify Variable Name Consistency
**Location**: Technical validation (not in economics.qmd text)
**Action**: Run validation script to verify all variables exist in parameters.py. Check: `dfda_lives_saved_annually`, `dfda_value_per_life_saved`, `traditional_phase3_cost_per_patient` vs `traditional_trial_cost_per_patient`, `dfda_upfront_build` vs `dfda_npv_annual_opex_total`. Fix any inconsistencies.

### Low Priority / Optional

#### 3. ⏳ Add Military R&D Spillover Estimate
**Action**: Research estimates of military R&D with civilian applications (20-50%). Add parameter `MILITARY_RD_CIVILIAN_SPILLOVER_PCT`. Add conservative adjustment to peace dividend calculation.

#### 6. ⏳ Add Post-Cold War Defense Conversion Data
**Action**: Research post-Cold War military-to-civilian conversion (1989-1995). Find defense worker re-employment rates. Add to references.qmd. Cite in Limitations: "Historical precedent shows 85% re-employed within one year."

#### 7. ⏳ Opportunity Cost Table - Contrast with NIH Model
**Action**: Note in opportunity cost discussion: "Traditional research funding (NIH $45B annually) has high cost per QALY at margin due to structural inefficiencies. dFDA targets efficiency (82× cost reduction) not just scale."

#### 8. ⏳ Add Formal Acknowledgment of Limitations
**Action**: Keep Limitations section concise (~100 lines max). Focus on 5 core limitations with brief description + quantitative sensitivity + why analysis still robust.

---

## Implementation Checklist

### Phase 1: High Priority Text Additions (economics.qmd)
- [ ] Todo #15: Enhance opportunity cost analysis section (partially complete - needs comparison to alternative uses)
- [x] Todo #16: Improve QALY methodology with confidence levels - ✅ COMPLETED (lines 1258, 1262, 1266)
- [x] Todo #17: Enhance external validity discussion - ✅ COMPLETED (lines 1352-1369)
- [ ] Todo #18: Add adoption realism discussion

### Phase 2: Medium Priority Enhancements
- [ ] Todo #26: Add brief note on publication bias
- [ ] Todo #28: Add brief note on comparison set rationale
- [ ] Todo #29: Acknowledge inadequate uncertainty quantification (Monte Carlo)
- [ ] Todo #30: Verify variable name consistency

### Phase 3: Low Priority / Optional
- [ ] Todo #3: Add military R&D spillover estimate
- [ ] Todo #6: Add post-Cold War defense conversion data
- [ ] Todo #7: Opportunity cost table - contrast with NIH model
- [ ] Todo #8: Add formal acknowledgment of limitations

### Phase 4: Final Validation
- [ ] Verify all variable references work after running generate-variables-yml.py
- [ ] Check all LaTeX equations render correctly
- [ ] Cross-reference dfda.qmd, dfda-cost-benefit-analysis.qmd, and right-to-trial-fda-upgrade-act.qmd for consistency

---

## Technical Implementation Notes

**For calculations:**
1. Add calculation functions to `dih_models/parameters.py`
2. Create Parameter objects with calculated values, proper metadata (source_ref, confidence, formula, latex)
3. Run `scripts/generate-variables-yml.py` to regenerate `_variables.yml`
4. Reference in economics.qmd using `{{< var parameter_name >}}` syntax
5. Hardcode LaTeX equations in economics.qmd (do not generate dynamically)

**For text-only additions:**
- Add directly to economics.qmd
- Reference existing variables where applicable using `{{< var name >}}`
- Use hardcoded LaTeX for any formulas shown

---

## Completed Items (Reference Only)

**Major completed work:**
- ✅ Expected value analysis (Todo #9) - lines 576-605
- ✅ General equilibrium effects (Todo #11) - lines 1241-1262
- ✅ Peace dividend confidence levels (Todo #12) - methodology lines 427-435
- ✅ Discount rate sensitivity (Todo #13) - lines 500-523
- ✅ Partnership model explanation (Todo #20) - lines 645-649
- ✅ Platform costs distinction (Todo #21) - lines 714-720
- ✅ Cost comparison table (Todo #22) - figure created
- ✅ Observational trial images (Todo #23) - lines 1109-1115
- ✅ Time inconsistency discussion (Todo #27) - lines 607-626
- ✅ Counterfactual baseline (Todo #33) - lines 413-429
- ✅ Regulatory and implementation risks (Todo #31) - lines 1393-1479
- ✅ Pre-1962 context and thalidomide (Todo #0a) - lines 542-554
- ✅ RECOVERY trial limitations (Todo #14) - lines 1051-1062

For detailed historical record of all completed work, see git history.
