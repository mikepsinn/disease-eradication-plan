# Plan: Add Cumulative War Costs Since 1900 to cost-of-war.qmd

## Overview
Add three new sections estimating cumulative (since 1900) costs that the chapter currently lacks:
1. **Cumulative property/environmental destruction**
2. **Professionals killed** (scientists, doctors, engineers, teachers, nurses, farmers, skilled trades)
3. **QALY-based value of all lost life-years**

All estimates use simple back-of-envelope math with cited inputs. New parameters go in `parameters.py`.

---

## Step 1: Add New Parameters to `parameters.py`

### Cumulative deaths
- `WAR_DEATHS_SINCE_1900_TOTAL` = 200,000,000 (Leitenberg/CISSM central estimate ~200M including democide, famine; source: necrometrics.com, Leitenberg 2006)

### Professional workforce percentages (early-mid 20th century global averages)
- `WORKFORCE_PCT_PHYSICIANS` = 0.3% (~0.3% of population were doctors/physicians)
- `WORKFORCE_PCT_NURSES_MIDWIVES` = 0.4%
- `WORKFORCE_PCT_ENGINEERS` = 0.2%
- `WORKFORCE_PCT_SCIENTISTS_RESEARCHERS` = 0.1%
- `WORKFORCE_PCT_TEACHERS` = 1.0%
- `WORKFORCE_PCT_FARMERS_AGRICULTURAL` = 40% (but deaths among farmers proportional to general pop, so use general %)
- `WORKFORCE_PCT_SKILLED_TRADES` = 3.0%

Actually, simpler approach: just use a single combined "professionals" percentage and multiply. The 20th century average across all countries: doctors (~0.3%), nurses (~0.4%), engineers (~0.2%), scientists (~0.1%), teachers (~1%), skilled trades (~3%) = **~5% combined professional class**. But farming was 30-60% of population early 1900s. We'll note farmers separately since their % is so different.

### Calculated parameters
- `WAR_PROFESSIONALS_KILLED_SINCE_1900` = 200M × 5% = 10,000,000 (conservative; doesn't account for targeting of educated classes)
- `WAR_DOCTORS_KILLED_SINCE_1900` = 200M × 0.3% = 600,000
- `WAR_ENGINEERS_KILLED_SINCE_1900` = 200M × 0.2% = 400,000
- `WAR_SCIENTISTS_KILLED_SINCE_1900` = 200M × 0.1% = 200,000
- `WAR_TEACHERS_KILLED_SINCE_1900` = 200M × 1.0% = 2,000,000
- `WAR_NURSES_KILLED_SINCE_1900` = 200M × 0.4% = 800,000

### QALY calculation
- Average age of war death: ~28 years (weighted: soldiers ~23, civilians older)
- Average life expectancy mid-20th century: ~55 years (global weighted avg)
- Years of life lost per death: 55 - 28 = 27 years
- `WAR_LIFE_YEARS_LOST_SINCE_1900` = 200M × 27 = 5.4 billion life-years
- `WAR_QALY_VALUE_SINCE_1900` = 5.4B × $150,000/QALY = $810 trillion
- (Use existing `STANDARD_ECONOMIC_QALY_VALUE_USD` = $150,000)

### Cumulative property/infrastructure destruction (major conflicts, 2024 dollars)
Sum of known estimates:
- WWI: ~$5T (all belligerents, property + economic disruption)
- WWII: ~$23T (Harrison, all belligerents property destruction + reconstruction)
- Korea: ~$0.5T
- Vietnam: ~$1T
- Post-9/11 wars: ~$8T (Brown Costs of War project)
- Other 20th-21st century conflicts (China civil war, Iran-Iraq, Congo, Syria, Ukraine, etc.): ~$5-10T
- `WAR_CUMULATIVE_PROPERTY_DESTRUCTION_SINCE_1900` = ~$45T (central estimate)

### Cumulative environmental destruction
- Current annual: $100B/year
- Historical average (lower in early 1900s, higher recently): ~$30B/year average over 125 years
- Plus one-time catastrophic events: nuclear testing ($500B remediation), Agent Orange ($100B+), Gulf War oil fires, DU contamination, Zone Rouge, etc.
- `WAR_CUMULATIVE_ENVIRONMENTAL_DAMAGE_SINCE_1900` = ~$5T (very rough)

---

## Step 2: Add BibTeX Citations to `references.bib`

- Leitenberg 2006 (CISSM deaths in wars 20th century) - already may exist
- Necrometrics.com (Matthew White's 20th century death estimates)
- Harrison 2000 (Economics of WWII)
- Brown University Costs of War project
- HHS 2024 QALY valuation ($150K standard)
- NSF Science & Engineering workforce data

---

## Step 3: Add New Sections to `cost-of-war.qmd`

Insert after "The Running Tab" section (line ~329) and before "Hidden Costs of War" (line ~332).

### Section A: "The Historical Tab: Cumulative Destruction Since 1900"
- Cumulative property destruction table by major conflict (~$45T total)
- Cumulative environmental destruction estimate (~$5T)
- Brief Wishonia-voice commentary

### Section B: "The Brain Drain: Professionals Killed Since 1900"
- Simple methodology: workforce % × 200M total deaths
- Table: profession | workforce % | estimated killed
- Note that this is conservative (educated classes were *disproportionately* targeted in Holocaust, Khmer Rouge, Cultural Revolution, Soviet purges)
- Punchline: 200,000 scientists and 600,000 doctors. How many cures died with them?

### Section C: "The Stolen Years: QALY Valuation of Lost Life"
- 200M deaths × 27 avg years lost = 5.4 billion life-years
- At $150,000/QALY = $810 trillion
- Compare to $180T cumulative military spending: the lives destroyed were worth 4.5× what was spent destroying them
- This is the ultimate ROI calculation: spend $180T, destroy $810T in human life value

---

## Step 4: Run `npm run generate:everything`

Regenerate `_variables.yml` with new parameters.

---

## Files Modified
1. `dih_models/parameters.py` - new parameters
2. `references.bib` - new citations (if needed)
3. `knowledge/problem/cost-of-war.qmd` - three new sections
