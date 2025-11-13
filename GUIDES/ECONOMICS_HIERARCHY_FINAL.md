---
title: Economics File Hierarchy - FINAL STRUCTURE
description: Two-tier ROI framework (463:1 conservative, 1,239:1 complete)
tags: [economics, organization, roi, structure]
status: IMPLEMENTED
date: 2025-01-11
---

# Economics File Hierarchy - FINAL STRUCTURE

## ✅ Implemented Structure

This document reflects the **ACTUAL IMPLEMENTED STRUCTURE** as of 2025-01-11.

**Current ROI Framework**: Two-tier analysis
- **Conservative (463:1)**: dFDA R&D savings only
- **Complete (1,239:1)**: All 8 benefit categories

Previous "endgame" (25,781:1) analysis removed to focus on demonstrable benefits.

---

## File Organization

### 📖 Main Book Chapters (Accessible Story)

Located in `brain/book/economics/`:

1. **[economics.qmd](../brain/book/economics.qmd)** - Overview combining both dividends
2. **[peace-dividend.qmd](../brain/book/economics/peace-dividend.qmd)** - Peace dividend deep dive (clean, no code)
3. **[health-dividend.qmd](../brain/book/economics/health-dividend.qmd)** - Health dividend deep dive (clean, no code)

### 🧮 Appendix Calculations (Show Your Work)

Located in `brain/book/appendix/`:

1. **[peace-dividend-calculations.qmd](../brain/book/appendix/peace-dividend-calculations.qmd)** - Full Jupyter notebook with math
2. **[health-dividend-calculations.qmd](../brain/book/appendix/health-dividend-calculations.qmd)** - Full Jupyter notebook with NPV/ROI
3. **[1-percent-treaty-cost-effectiveness.qmd](../brain/book/appendix/1-percent-treaty-cost-effectiveness.qmd)** - Combined proof (peace + health)
4. **[research-acceleration-model.qmd](../brain/book/appendix/research-acceleration-model.qmd)** - Complete Case (1,239:1 ROI) detailed analysis

### 📊 Charts

Located in `dih-economic-models/figures/`:

Peace Dividend Charts:

- `military-vs-disease-research-funding-bar-chart.qmd`
- `peace-dividend-breakdown-bar-chart.qmd`
- `peace-dividend-composition-donut-chart.qmd`
- `captured-vs-societal-dividend-bar-chart.qmd`

Health Dividend Charts:

- Various dFDA/ROI charts (existing)

---

## Perfect Symmetry Achieved

```
PEACE DIVIDEND                          HEALTH DIVIDEND
├── economics/peace-dividend.qmd        ├── economics/health-dividend.qmd
│   (Chapter: accessible story)         │   (Chapter: accessible story)
│                                       │
└── appendix/peace-dividend-            └── appendix/health-dividend-
    calculations.qmd                        calculations.qmd
    (Appendix: full math)                   (Appendix: full math + NPV)
         │                                       │
         └────────────┬──────────────────────────┘
                      │
                      └── appendix/1-percent-treaty-cost-effectiveness.qmd
                          (Combined proof: ICER, cost-effectiveness)
```

---

## Information Flow

```
PROBLEM CHAPTERS
├── cost-of-war.qmd ($11.4T quantified)
└── fda-is-unsafe-and-ineffective.qmd ($100B trial market)
         │
         ▼
APPENDIX CALCULATIONS (Source of Truth)
├── peace-dividend-calculations.qmd ($114B societal dividend)
└── health-dividend-calculations.qmd ($50B R&D savings, 463:1 ROI)
         │
         ▼
ECONOMICS CHAPTERS (Accessible Story)
├── peace-dividend.qmd (TL;DR + breakdown table)
├── health-dividend.qmd (463:1 ROI story)
└── economics.qmd (Combined overview, all ROI tiers)
```

---

## Single Source of Truth

All files use **`economic_parameters.py`**:

```python
from economic_parameters import *

# Peace Dividend
SOCIETAL_DIVIDEND  # $113.6B
CAPTURED_DIVIDEND  # $27.2B
MILITARY_SPENDING  # $2,718.0B

# Health Dividend
DFDA_GROSS_SAVINGS  # $50.0B
DFDA_ROI  # 1,250:1
DFDA_ANNUAL_OPEX  # $40M

# Combined
TOTAL_ANNUAL_BENEFITS  # $163.6B
ICER_PER_QALY  # -$176,382
COST_PER_LIFE_SAVED  # -$6.17M
```

Changing one parameter updates everywhere automatically ✅

---

## Naming Convention

**Pattern established**:

- **Chapters** (brain/book/economics/): `[topic].qmd` - Clean, accessible, no visible code
- **Calculations** (brain/book/appendix/): `[topic]-calculations.qmd` - Jupyter notebooks with math
- **Charts** (dih-economic-models/figures/): `[description]-[chart-type]-chart.qmd` - Standalone visualizations

**Examples**:

- ✅ `peace-dividend.qmd` (chapter)
- ✅ `peace-dividend-calculations.qmd` (appendix)
- ✅ `military-vs-disease-research-funding-bar-chart.qmd` (figure)

---

## File Purposes

### economics.qmd (Overview)

**Purpose**: 10,000-foot view of entire economic case
**Content**:

- Peace Dividend: $113.6B from conflict reduction
- Health Dividend: $50B from trial efficiency
- Combined: $163.6B annual benefit (conservative case)
- Two ROI tiers (463:1 conservative, 1,239:1 complete)
- Opportunity cost clock
**Links to**: Both dividend chapters, both calculation appendices

### peace-dividend.qmd (Chapter)

**Purpose**: Deep dive on peace dividend for general readers
**Content**:

- TL;DR: $27.2B captured, $113.6B societal
- Where the savings come from (table)
- $4.18 saved per $1 redirected
- Clean markdown, no code chunks visible
**Links to**: peace-dividend-calculations.qmd

### health-dividend.qmd (Chapter)

**Purpose**: Deep dive on health dividend for general readers
**Content**:

- 463:1 ROI bottom line
- $40M → $50B story
- Platform cost breakdown
- Why 82x cheaper trials work
**Links to**: health-dividend-calculations.qmd, 1-percent-treaty-cost-effectiveness.qmd

### peace-dividend-calculations.qmd (Appendix)

**Purpose**: Prove the math for peace dividend
**Content**:

- Full Jupyter notebook (Python visible)
- Sensitivity analysis (0.5% to 2% scenarios)
- Data validation
- Charts (via includes from dih-economic-models/figures/)
**Source**: cost-of-war.qmd

### health-dividend-calculations.qmd (Appendix)

**Purpose**: Prove the math for health dividend
**Content**:

- Full Jupyter notebook (Python visible)
- NPV analysis over 10 years
- ROI calculation: 463:1
- Sensitivity analysis
- Charts
**Source**: Clinical trial market data

### 1-percent-treaty-cost-effectiveness.qmd (Appendix)

**Purpose**: Academic proof combining both dividends using health economics methodology
**Content**:

- ICER = -$296,786 per QALY
- Cost per life = -$6.56M (society SAVES money)
- Comparison to GiveWell charities (1,458x more cost-effective)
- Sensitivity analysis across scenarios
- Combines peace dividend ($113.6B) + health dividend ($50B)
**Why separate**: This is the master proof combining both dividend streams, using academic cost-effectiveness methodology

### research-acceleration-model.qmd (Appendix)

**Purpose**: Detailed analysis of Complete Case (1,239:1 ROI) counting all direct benefits
**Content**:

- 8 primary benefit categories totaling $1.239T/year
- 7-Year Access Acceleration model (stock + flow benefits)
- Research Acceleration Multiplier (115X capacity calculation)
- Complete Benefit Breakdown Table
- Sanity checks ($1.239T vs. global GDP/healthcare spending)
- Technical notes on methodology
**Why separate**: Provides detailed math for complete ROI tier showing all 8 quantifiable benefit categories

---

## What Changed (Migration Summary)

**Files Renamed**:

1. `peace-dividend-analysis.qmd` → `peace-dividend-calculations.qmd`
2. `dfda-roi-calculations.qmd` → `health-dividend-calculations.qmd`

**Files Moved**:

1. `peace-dividend-breakdown.qmd` → `economics/peace-dividend.qmd`
2. `dfda-roi-breakdown.qmd` → `economics/health-dividend.qmd`

**Charts Extracted**:

- 4 peace dividend charts moved from calculations file to `dih-economic-models/figures/`
- Charts now use `{{< include >}}` directives (when fully migrated)

**All Files Now Use**:

- `economic_parameters.py` for single source of truth
- Inline `{python}` expressions in markdown
- Consistent naming convention

---

## Next Steps (Optional Improvements)

1. **Extract remaining charts** from health-dividend-calculations.qmd to dih-economic-models/figures/
2. **Replace embedded charts** in calculation files with `{{< include >}}` directives
3. **Add NPV analysis** to peace-dividend-calculations.qmd (mirror health dividend rigor)
4. **Cross-reference audit**: Ensure all links point to new file paths

---

## Quick Reference

**Want to know**: → **Read**:

- "What's the bottom line?" → economics.qmd
- "How does peace dividend work?" → economics/peace-dividend.qmd
- "How does health dividend work?" → economics/health-dividend.qmd
- "Prove the peace math" → appendix/peace-dividend-calculations.qmd
- "Prove the health math" → appendix/health-dividend-calculations.qmd
- "Prove the cost-effectiveness" → appendix/1-percent-treaty-cost-effectiveness.qmd
- "Show me Complete Case (1,239:1)" → appendix/research-acceleration-model.qmd
