# PDF Validation Errors - Checklist

**PDF:** `E:\code\obsidian\websites\disease-eradication-plan\assets\pdfs\How-to-End-War-and-Disease-Paperback.pdf`
**Quarto config:** `E:\code\obsidian\websites\disease-eradication-plan\_quarto-manual-paperback.yml`
**Generated:** 2026-02-20T03:52:39.898890

## Summary

- **Total issues:** 25
- **Critical:** 8
- **Warnings:** 17

## IMPORTANT: Before You Start

**DO NOT edit `index.qmd` directly - it is auto-generated!**

1. **First, review the Quarto config:** `E:\code\obsidian\websites\disease-eradication-plan\_quarto-manual-paperback.yml`
   - This config specifies the main QMD file used to generate this PDF
   - The main QMD file is copied to `index.qmd` during the build process
   - Any edits to `index.qmd` will be overwritten on the next build

2. **Edit the source QMD file specified in the config, NOT `index.qmd`**

---

## 🟡 LLM_ARITHMETIC_INCONSISTENCY (2 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [ ] **Page 1192:** In Figure 441, the top input label reads 'TREATY FUNDING INPUT ($2.72B/YEAR AT 1%)', but a component of that same system (the 10% allocation to Incentive Alignment Bonds) is correctly labeled as '$2.72B/YEAR' at the bottom right. This implies the total input should be $27.2B, as supported by the text and subsequent pillars.
  - Context: `suggested_fix=Update the top funnel label in Figure 441 to read '$27.2B/YEAR' to match the 80/10/10 split and later diagrams. | evidence_snippet=TREATY FUNDING INPUT ($2.72B/YEAR AT 1%) | locator_hint=Figure 441: Take 10 percent of the treaty money and use it to pay politicians`
- [ ] **Page 1203:** Figure 445 (and Figure 444 on p. 607) uses '$2.69T' as the baseline for global spending, but the calculation box within the figure states '[$2.69T x 0.01 = $27.2B]'. Arithmetically, 1% of $2.69T is $26.9B. Elsewhere in the document (p. 609, 611, 613), the baseline spending is consistently and correctly cited as '$2.72T'.
  - Context: `suggested_fix=Update Figures 444 and 445 to use the '$2.72T' baseline figure to maintain consistency with the math and tables throughout the rest of the section. | evidence_snippet=$2.69T x 0.01 = $27.2B | locator_hint=Figure 445: Take one percent of the money humans spend on killing each other`

## 🟡 LLM_BROKEN_REFERENCE (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [ ] **Page 1070:** Citation/footnote numbering defect. The superscript citation index on page 553 is '270', while the surrounding citations on pages 552 and 556 are '293' and '294', respectively. This indicates a break in the sequential endnote/footnote system.
  - Context: `suggested_fix=Correct the citation index on page 553 to maintain sequential order (likely changing 270 to 294 and incrementing the subsequent citation). | evidence_snippet=avoided war for 200 years270 | locator_hint=Section 'Why Switzerland', first paragraph beneath Figure 407`

## 🔴 LLM_BROKEN_REFERENCES/CITATIONS (2 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [ ] **Page 960:** Significant numerical discrepancy in Figure 354 caption relative to the text and infographic. The caption states Oxford's trial cost '$15,000', but the infographic on the same page specifies a cost of '$500 (Mean)' per patient. Furthermore, the text on page 481 claims the trial saved '1 million lives'. A total cost of $15,000 at $500/patient implies only 30 patients, which is logically incompatible with saving 1 million lives.
  - Context: `suggested_fix=Adjust the total trial cost in the Figure 354 caption to be mathematically consistent with the per-patient cost and trial scale mentioned in the text (e.g., if 30,000 patients were involved, the cost should be $15 million). | evidence_snippet=Oxford’s trial cost 15,000 dollars. FDA tri...`
- [ ] **Page 990:** Internal numerical inconsistency within Figure 378 content. The graphic ribbon promises '272% MORE PAPERS ANNUALLY', while the adjacent 'Pitch' text states 'GET 2.7X MORE FOREVER'. Mathematically, '272% more' implies a 3.72x multiplier (1 + 2.72), creating a conflict with the '2.7x' multiplier mentioned in the pitch.
  - Context: `suggested_fix=Standardize the financial terminology. If the total return is 2.7x, the percentage increase should be described as '170% more' or '270% of' the original amount. | evidence_snippet=THE PROMISE: 272% MORE PAPERS ANNUALLY ... THE PITCH: ... GET 2.7X MORE FOREVER | locator_hint=Figure 378 ...`

## 🟡 LLM_DATA_INCONSISTENCY (5 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [ ] **Page 118:** Daily military spending values are inconsistent across the document: $7.45B (page 54 table), $7.4B (page 68 text), and $7.46B (page 69 Figure 40 caption).
  - Context: `suggested_fix=Unify the daily military spending figure to a single consistent value (likely $7.45B based on the master summary table on page 54). | evidence_snippet=Figure 40: Daily military spending: $7.46 billion. | locator_hint=Figure 40 caption`
- [ ] **Page 125:** The annual NIH budget is cited as approximately $51 billion on page 71, but subsequently referred to as a $47B budget on pages 76 and 77.
  - Context: `suggested_fix=Unify the NIH budget figure to $51B or explain if the $47B refers to a specific subset of the budget (e.g., the research portfolio). | evidence_snippet=This is a tiny fraction of the $47B budget | locator_hint=section Cost Per QALY (Quality-Adjusted Life Year)`
- [x] **Page 667:** The percentages in the Figure 238 caption (60% fundraising, 12% approval) do not match the data presented within the infographic and the bullet points (70% fundraising, 18% approval).
  - Context: `suggested_fix=Update the caption of Figure 238 to match the infographic: '70 percent fundraising calls, 18 percent approval rating'. | evidence_snippet=60 percent fundraising calls, 12 percent approval rating | locator_hint=Figure 238: The modern politician`
  - **RESOLVED:** Updated caption in aligning-incentives.qmd:270 to "70 percent fundraising calls, 18 percent approval rating".
- [ ] **Page 694:** The caption for Figure 260 uses reelection/unemployment percentages (73% and 55%) that are not present in the worked example figures or text (which use 62%, 68%, 48%, etc.). The 55% figure is actually the 'Before' reelection chance.
  - Context: `suggested_fix=Update the caption to use the outcome probabilities defined in the model (e.g., 62% for Yes, 48% for No). | evidence_snippet=Vote yes: 73% chance you keep your job... Vote no: 55% chance you’re unemployed | locator_hint=Figure 260 caption`
- [ ] **Page 701:** The table within Figure 267 contains nonsensical data: the '1% Treaty Fund Revenue' (intended to be 10% of total) often exceeds the 'Total Revenue' column (e.g., $100B revenue from $56.7B total), and the values scale erratically with Treaty Level.
  - Context: `suggested_fix=Rebuild the table in Figure 267 using the correct scaling data provided in the accurate summary table on page 370. | evidence_snippet=Total Revenue $56.7B ... 1% Treaty Fund Revenue $100B/year | locator_hint=Figure 267: IABs Are the Political Ratchet infographic table`

## 🔴 LLM_EQUATION_RENDERING (2 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [ ] **Page 693:** The typeset equation for 'Expected utility of No vote' is missing the 'K' suffix for the dollar amount, showing '$200 /year' instead of the intended '$200K /year' mentioned in the text.
  - Context: `suggested_fix=Change '$200 /year' to '$200K /year' in the equation block. | evidence_snippet=Expected utility of No vote: U = 0.55 · Office + $200 /year · 20yrs | locator_hint=The equation in the 'The New Calculus (Without IABs)' section`
- [ ] **Page 694:** The typeset equation for 'delta U' in the body text is missing the 'K' suffix for the dollar amount ($100 vs $100K), creating a 1000x error and contradicting the correct version shown inside Figure 260 on the same page.
  - Context: `suggested_fix=Ensure the standalone formula under 'The math:' matches the version inside the infographic by adding the 'K' suffix to the dollar amount. | evidence_snippet=Δ U Yes vs No = 0.14 · Office + $100 /year · 20yrs | locator_hint=The standalone math equation following Figure 260`

## 🔴 LLM_EQUATION_RENDERING_DEFECT (3 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [ ] **Page 36:** Variable identifiers in the 'Equation of Immediate Destruction' are missing their primary characters (C, M, I, H, and T). Only the subscripts and operators are visible.
  - Context: `suggested_fix=Ensure all mathematical fonts are correctly embedded in the PDF and check the LaTeX source for variable name formatting that might conflict with the rendering engine. | evidence_snippet=direct = spending + damage + casualties + disruption | locator_hint=Equation below Figure 21 in sect...`
- [ ] **Page 45:** The Reconstruction Cost Analysis formula is missing the primary characters of its variables (R, D, M, C, and T).
  - Context: `suggested_fix=Re-render the equation ensuring that the identifier font is compatible with the PDF export settings. | evidence_snippet=cost = value × replacement × conflict × time | locator_hint=Equation at the bottom of the section Infrastructure Destruction: Breaking Things Costs Money`
- [ ] **Page 46:** The Trade Flow Disruption formula and the bulleted list of variable definitions are missing initial characters (L, R, D, M, C, T, V). For example, 'Rcost' appears as 'cost' and 'Dvalue' as 'value'.
  - Context: `suggested_fix=Correct the font rendering for the variable identifier style used in both the math block and the definition list. | evidence_snippet=trade = ∑( × × × recovery) | locator_hint=Formula and bulleted list in section Economic Disruption: The Ripple Effect`

## 🟡 LLM_INCONSISTENCY (3 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [ ] **Page 743:** Financial figures and calculated returns are inconsistent across various diagrams and text sections. For example, the bondholder payout is cited as $2.72B (p. 372, Fig 287), $2.7B (p. 375 text, Fig 271), and 2720000000.0 (p. 393). Similarly, the 80% allocation for cures is cited as $21.8B (Fig 270, Fig 287) and $21.7B (p. 376 text and Fig 271), with the latter being mathematically incorrect as 80% of $27.2B is $21.76B.
  - Context: `suggested_fix=Standardize all financial figures to two decimal places ($2.72B, $21.76B, and 272% returns) across all diagrams and body text to ensure mathematical consistency. | evidence_snippet=What bondholders get: 10% × $27.2B = $2.7B/year | locator_hint=Calculate Your Numbers for Investors secti...`
- [ ] **Page 748:** The 'Even if you’re extremely pessimistic' table conflicts with the explanatory text immediately below it. The table lists the 'Total Lifetime Value' for a 10% discount rate as '$27B', whereas the paragraph below states the same calculation 'becomes worth $27.2B total'.
  - Context: `suggested_fix=Update the table value to $27.2B to match the text and the precise calculation of the perpetual bond ($2.72B / 0.10). | evidence_snippet=your $1B becomes worth $27.2B total. | locator_hint=Translation for those who prefer simple math section`
- [x] **Page 823:** There is a numerical discrepancy between the body text and Figure 304 regarding bond returns. The text states 'VICTORY Incentive Alignment Bonds promise 272% returns,' while the graphic in Figure 304 illustrates '270% RETURNS'.
  - Context: `suggested_fix=Synchronize the values in both the text and the figure to ensure consistency (e.g., use 272% in both). | evidence_snippet=VICTORY Incentive Alignment Bonds promise 272% returns. | locator_hint=In the paragraph titled 'The Lesson' immediately following Figure 304`
  - **RESOLVED:** Deleted problematic image and reference from aligning-incentives.qmd.

## 🟡 LLM_INCONSISTENT_DATA (2 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [ ] **Page 446:** Numerical discrepancy between the body text and Figure 175 regarding clinical trial participation counts. The text reports 1.90 million current and 23.4 million projected participants, whereas Figure 175 claims 5 million current and 220 million projected participants.
  - Context: `suggested_fix=Align Figure 175's data points with the 'Year One Projected Outcomes' text section to ensure internal consistency (adjusting the graphic to 1.9M and 23.4M). | evidence_snippet=Only 1.90 million patients/year... vs ...ONLY 5M PARTICIPANTS | locator_hint=Figure 175 titled Global Clinical...`
- [ ] **Page 1049:** Internal contradiction regarding the primary quantitative claim. Page 532 and 535 claim moving 1% of military budgets 'increases clinical trials capacity 604:1' or '604 times'. However, pages 525, 542, and 543 claim the same shift results in '12.3x' or '12.3:1' more capacity. These conflicting figures undermine the mathematical premise of the '1% treaty'.
  - Context: `suggested_fix=Verify the intended multiplier based on current global spending data and standardize all text and graphics to use a single, consistent figure. | evidence_snippet=increases clinical trials capacity by 604:1 times | locator_hint=Compare section 'Why Every Nonprofit Should Support a 1% tr...`

## 🟡 LLM_MALFORMED_BIBLIOGRAPHY (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [ ] **Page 1279:** There is a systematic defect in the bibliography where organization names are incorrectly parsed as 'Lastname, Firstname' (e.g., 'Us, A. of.' for 'All of Us', 'Defense, D. of.' for 'Department of Defense') and 'et al.' is incorrectly formatted as 'al., [Name] et.' (e.g., entries 84, 191, 211).
  - Context: `suggested_fix=Enclose organization names in braces in the BIBTeX source to prevent incorrect parsing and verify the bibliography style configuration for 'et al.' entries. | evidence_snippet=al., B. et. Disease network overlap | locator_hint=Source Quotes and References section, entries 84, 176, 191,...`

## 🟡 LLM_SPELLING_ERROR (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [x] **Page 1271:** The word 'UNIVERSITY' is misspelled as 'UNIVERSUTY' inside the building illustration on the 'NIH GRANT SYSTEM' side of Figure 467.
  - Context: `suggested_fix=Edit the source graphic for Figure 467 to correct the spelling to 'UNIVERSITY'. | evidence_snippet=UNIVERSUTY | locator_hint=Figure 467 building illustration label under NIH GRANT SYSTEM`
  - **RESOLVED:** Deleted problematic image and reference from financial-plan.qmd.

## 🟡 LLM_STRING (2 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [x] **Page 196:** Grammatical error or missing punctuation in bulleted list; the phrase 'physicians independent doctors' is ungrammatical and likely missing a comma or intended as 'independent physicians'.
  - Context: `suggested_fix=Change to 'independent physicians' or 'physicians, independent doctors,'. | evidence_snippet=Replaced 144 thousand physicians independent doctors with drug company-run trials | locator_hint=First bullet point on the page under the section TITLE 'What the 1962 Efficacy Requirements Chan...`
  - **RESOLVED:** Changed "independent doctors" to "independently testing treatments" in fda-is-unsafe-and-ineffective.qmd:94 (variable already contains "physicians").
- [ ] **Page 203:** Significant numerical contradiction; the 'Annualized loss' is incorrectly stated as $1.19 quadrillion/year, which is the cumulative total cost. The parenthetical formula ($1.19 quadrillion / 62 years) yields approximately $19.2 trillion/year, which is the mathematically correct annualized figure.
  - Context: `suggested_fix=Update the annualized loss to ~$19.2 trillion/year to maintain consistency with the total cost and the global GDP percentage provided. | evidence_snippet=Annualized loss: $1.19 quadrillion/year ($1.19 quadrillion / 62 years from 1962-2024) | locator_hint=Second bullet point under the s...`

## 🟡 LLM_TYPOGRAPHICAL_ERROR (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [x] **Page 446:** Stray closing parenthesis found in the text body.
  - Context: `suggested_fix=Change 'annually) out of' to 'annually out of'. | evidence_snippet=participate in drug trials annually) out of | locator_hint=Section titled Year One Projected Outcomes, first paragraph.`
  - **RESOLVED:** Removed stray `)` from 1-percent-treaty.qmd:273.
