# Wishocracy Paper Improvements

## ✅ Citation Fixes (High Priority) - COMPLETE

### 1. ✅ Fix duplicate Gilens reference
- **Status**: COMPLETE - Changed `@princeton-oligarchy-study` → `@gilens2014` in lines 219, 221
- **Note**: Consider removing duplicate `princeton-oligarchy-study` entry from references.qmd

### 2. ✅ Add missing citations to references.qmd
- **Status**: COMPLETE - All three citations added:
  - **Aczél & Saaty (1983)** - Added at references.qmd:102 → Used in line 184 as `[@aczel-saaty-1983]`
  - **Downs (1957)** - Added at references.qmd:1653 → Used in line 238 as `[@downs-1957]`
  - **Rawls (1971)** - Added at references.qmd:6016 → Used in line 248 as `[@rawls-1971]`
- **Status**: references.bib regenerated with 750 citations (up from 747)

## ✅ Critique-Based Improvements - COMPLETE

### 3. ✅ Title & Branding
- **Status**: COMPLETE - Changed to:
  - Title: "Wishocracy"
  - Subtitle: "Randomized Pairwise Budget Allocation for Preference Aggregation"
  - See lines 2-3

### 4. ✅ Soften Overclaims
- **Status**: COMPLETE:
  - ✅ "Strategy-proofness" → "Manipulation Resistance" (line 152)
  - ✅ Kept "Pareto Efficiency" but with caveat "as measured by expressed preferences" (line 151)
  - ✅ "RAPPA's Novel Contribution" → "RAPPA's Contribution" (line 85)

### 5. ✅ Fix Math/AHP Mismatch
- **Status**: COMPLETE - Added ratio conversion (lines 178-182):
  - Convert slider share $\rho$ to odds ratio $r$ using $r = (\rho + \epsilon)/(1-\rho+\epsilon)$
  - Geometric mean aggregation of ratios (lines 184-187)

### 6. ✅ Address Matrix Sparsity
- **Status**: COMPLETE:
  - Line 188: "sparse $m \times m$ comparison matrix"
  - Line 190: "for sparse data we employ logarithmic least squares (LLSM) or iterative methods"

### 7. ✅ Move GenieDAOs
- **Status**: COMPLETE:
  - Line 204: Reference moved to "Appendix A: The Solution Layer"
  - Core paper focuses on RAPPA mechanism

## ✅ Math Enhancements (Medium Priority) - COMPLETE

### 8. ✅ Add cognitive load formalization (Section 1)
- **Status**: COMPLETE - Lines 67-77 include formal equations:
  - $\text{Cognitive Load}_{\text{direct}} = n \gg 7 \pm 2$
  - $\text{Cognitive Load}_{\text{RAPPA}} = 2 < 7 \pm 2$

### 9. ✅ Add explicit convergence bound (Section 3.3)
- **Status**: COMPLETE - Lines 196-202 include Hoeffding's inequality:
  - $P(|a_{jk} - E[\rho_{i,j,k}]| > \epsilon) \leq \frac{1}{4|S_{jk}|\epsilon^2}$

### 10. ✅ Add complexity comparison table (Section 3.2)
- **Status**: COMPLETE - Lines 161-170 include comparison table with 4 mechanisms across 5 dimensions

## Final Polish (Surgical Edits) - High Priority

### 13. ✅ Remove "Strategy-Proofness" Language - COMPLETE
- Replace with "manipulation-resistant" or "reduced incentives for misreporting".
- Fixed in Description and Abstract.

### 14. ✅ Soften "Welfare-Maximizing" Claims - COMPLETE
- Replaced with "welfare-approximating" or "welfare-relevant".
- **Final verification**: Fixed remaining instance at line 56, confirmed zero instances of "welfare-maximizing" remain in paper.

### 15. ✅ Fix Convergence Math (Log-odds) - COMPLETE
- Replaced linear convergence claim with Log-odds formulation ($y = \log r$).

### 16. ✅ Soften Pareto Efficiency - COMPLETE
- Renamed to "Pareto-respecting" with caveats.

### 17. ✅ Soften "No Prior Mechanism" - COMPLETE
- Qualified with "To our knowledge".

### 18. ✅ Remove Pseudo-Math for Cognitive Load - COMPLETE
- Removed the $n \gg 7 \pm 2$ equations, kept intuition.

### 19. ✅ Add Pilotability Signal - COMPLETE
- Added "We outline a minimal viable pilot..." to Abstract.

## Claim Discipline (Final Scrub) - Critical

**Verification Complete (2025-12-18)**: All claim discipline fixes verified via grep searches:
- Zero instances of "strategy-proof" language remain ✅
- Zero instances of "welfare-maximizing" remain ✅
- Zero "Theorem" headers (all changed to Propositions) ✅
- Zero "**Proof" blocks (all changed to "**Argument") ✅

### 20. ✅ Fix "Strategy-Proofness" in Conclusion - COMPLETE
- Replaced with "reduce manipulability".

### 21. ✅ Remove Cognitive Load Equations (Check) - COMPLETE
- Replaced equations with plain text intuition.

### 22. ✅ Downgrade Theorems to Propositions - COMPLETE
- Renamed Theorem 1 -> Proposition 1, Theorem 2 -> Proposition 2.
- Changed "Proof" to "Argument".

### 23. ✅ Soften "No Existing Mechanism" - COMPLETE
- Qualified with "To our knowledge, widely deployed...".

### 24. ✅ Soften "Truthful Reporting" Claim - COMPLETE
- Changed to "robust heuristic".

## Figure Suggestions (Low-Medium Priority)

### 11. ✅ Cognitive Load Comparison Diagram (Section 1) - COMPLETE
- **Status**: COMPLETE - Added `rappa-cognitive-load-diagram.qmd` to Section 1.
- Visual: n-way comparison (overwhelming) vs pairwise (tractable)

### 12. ✅ Information Flow Diagram (Section 3.5.1) - COMPLETE
- **Status**: COMPLETE - Added `rappa-information-flow-diagram.qmd` to Section 3.5.1 (line 216)
- **Visual**: RepDem shows wide preference space → narrow bottleneck (single vote) → policy with information loss
- **Visual**: RAPPA shows wide preference space → many pairwise channels → aggregation → policy with preserved intensity
- Shows capacity formulas: C_Rep ≈ 0 vs C_RAPPA ∝ N·c̄·H(S)

### 13. ✅ Median vs Mean Welfare Graph (Section 3.5.2) - COMPLETE
- **Status**: COMPLETE - Added `rappa-median-vs-mean-welfare.qmd` to Section 3.5.2 (line 232)
- **Visual**: Right-skewed lognormal distribution representing health needs/rare diseases
- Shows median outcome (fails high-need minority) vs mean outcome (utilitarian optimum)
- Illustrates why RAPPA → mean (respects intensity), RepDem → median (ignores tail risk)
- Includes annotations highlighting welfare differences

### 14. ✅ Matrix Aggregation Visualization (Section 3.3) - COMPLETE
- **Status**: COMPLETE - Added `rappa-matrix-aggregation.qmd` to Section 3.3 (line 186)
- **Visual**: Four-panel diagram showing complete aggregation pipeline
- Panel 1-2: Individual sparse pairwise matrices (different citizens evaluate different pairs)
- Panel 3: Aggregated matrix via geometric mean
- Panel 4: Global priority vector (eigenvector centrality) as horizontal bar chart
- Demonstrates how distributed sparse inputs converge to coherent global priorities

### 15. Sybil Attack Dilution Diagram (Section 5.2)
- ✅ Already added in previous updates.

## Implementation Section (Already Added ✓)

### 16. Wishocracy.org reference (Section 4.5)
- ✅ Already added.

## Optional Enhancements

### 17. ✅ Add "Related Work" or "Literature Review" subsection - COMPLETE
- **Status**: COMPLETE - Added Section 2.4 "Related Work and Positioning in the Literature" (line 113)
- Compares RAPPA to liquid democracy, futarchy, conviction voting, and participatory budgeting
- Positions RAPPA's unique contribution: simultaneous cognitive tractability + preference intensity + scalable aggregation
- Discusses natural complementarities with other mechanisms
- Establishes RAPPA as preference elicitation layer that could integrate with other democratic innovations

### 18. ✅ Failure modes analysis - COMPLETE
- **Status**: COMPLETE - Added Section 5.6 "Failure Modes and Robustness" (line 363)
- **Low Participation (<1%)**: Discusses sampling bias and comparison sparsity with statistical reweighting mitigation
- **Low Comparison Density**: Analyzes k/m² scaling with hierarchical aggregation and active sampling solutions
- **Coordinated Minority Attacks**: Presents three-layer defense (dilution, anomaly detection, robustness analysis)
- **Graceful Degradation**: Establishes that RAPPA degrades proportionally rather than catastrophically
- Includes empirical thresholds (e.g., 3-5 comparisons per item sufficient for convergence)

### 19. ✅ Computational complexity analysis - COMPLETE
- **Status**: COMPLETE - Added Section 3.4 "Computational Complexity and Scalability" (line 210)
- **Big-O Analysis**: O(nk + m² log m) total complexity where nk dominates for large n
- **Scalability Limits**: Establishes bounds for municipal (m=20-50), city (m=100-500), national (m=5,000-10,000) scale
- **Benchmark Example**: City with 100 priorities, 50K participants, 20 comparisons each → 1M total comparisons, ~202x overdetermined, milliseconds aggregation time
- **Real-world Performance**: Wishocracy.org processes 10K comparisons across 50 items in <100ms (AWS t3.medium)
- Demonstrates computational tractability at national scale (1M participants) with commodity infrastructure
