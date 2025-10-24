---
title: FDA Spending vs Life-Expectancy Data
description: Historical data (1901-2000) analyzing FDA spending, drug costs, and life expectancy trends with CSV files and visualizations.
---

# FDA Spending vs Life-Expectancy Data Extract

Extracted from: `FDA Spending vs Life-Expectancy.xlsx`

**Extraction Date:** 2025-10-24

## Overview

This workbook contains historical data analyzing the relationship between FDA spending, drug development costs, and life expectancy trends from 1901-2000. The data is used to examine the effectiveness and cost-efficiency of FDA regulations on public health outcomes.

## Data Files

This workbook contains 5 data sheets, extracted to 10 files (CSV + Markdown for each):

### historical-life-expectancy-fda-budget-drug-costs-1901-2000

Historical time series data (1901-2000) tracking life expectancy before/after FDA creation, FDA budget (inflation-adjusted to 2020 USD), new drug applications, and cost to develop new drugs

- **CSV:** [historical-life-expectancy-fda-budget-drug-costs-1901-2000.csv](historical-life-expectancy-fda-budget-drug-costs-1901-2000.csv)
- **Markdown:** [historical-life-expectancy-fda-budget-drug-costs-1901-2000.md](historical-life-expectancy-fda-budget-drug-costs-1901-2000.md)

### life-expectancy-fda-budget-cost-analysis-1901-2000

Similar to main dataset but includes cost in millions column, used for cost reduction analysis charts

- **CSV:** [life-expectancy-fda-budget-cost-analysis-1901-2000.csv](life-expectancy-fda-budget-cost-analysis-1901-2000.csv)
- **Markdown:** [life-expectancy-fda-budget-cost-analysis-1901-2000.md](life-expectancy-fda-budget-cost-analysis-1901-2000.md)

### life-expectancy-gains-pre-post-fda-comparison-1901-2000

Comparison of annual life expectancy increases before and after FDA creation, demonstrating diminishing returns on health improvements

- **CSV:** [life-expectancy-gains-pre-post-fda-comparison-1901-2000.csv](life-expectancy-gains-pre-post-fda-comparison-1901-2000.csv)
- **Markdown:** [life-expectancy-gains-pre-post-fda-comparison-1901-2000.md](life-expectancy-gains-pre-post-fda-comparison-1901-2000.md)

### data-sources-references

Reference URLs and sources for drug development costs and FDA budget data

- **CSV:** [data-sources-references.csv](data-sources-references.csv)
- **Markdown:** [data-sources-references.md](data-sources-references.md)

### consumer-price-index-inflation-1913-2020

Consumer Price Index annual averages and inflation rates from Federal Reserve (1913-2020) for adjusting historical costs

- **CSV:** [consumer-price-index-inflation-1913-2020.csv](consumer-price-index-inflation-1913-2020.csv)
- **Markdown:** [consumer-price-index-inflation-1913-2020.md](consumer-price-index-inflation-1913-2020.md)

## File Types

### CSV Files

Raw comma-separated data files that can be imported into:

- Spreadsheet applications (Excel, Google Sheets, LibreOffice)
- Data analysis tools (R, Python pandas, MATLAB)
- Databases (PostgreSQL, MySQL, SQLite)
- Statistical software (SPSS, SAS, Stata)

### Markdown Files

Human-readable preview files with:

- Sheet metadata (dimensions, source)
- Formatted data tables (first 20 rows)
- Links to corresponding CSV files

## Visualizations

The following Quarto chart files have been created from this data (located in [brain/figures/](../../brain/figures/)):

### 1. FDA Spending vs Life Expectancy Trends

**File:** `fda-spending-life-expectancy-trend-line-chart.qmd`

Line chart showing life expectancy trends from 1901-2000, comparing pre-FDA (1901-1937) and post-FDA (1938-2000) periods.

### 2. Life Expectancy Gains: Diminishing Returns

**File:** `fda-life-expectancy-diminishing-returns-column-chart.qmd`

Column chart comparing average annual life expectancy gains before vs after FDA creation.

### 3. Drug Development Cost Explosion

**File:** `fda-drug-development-cost-increase-line-chart.qmd`

Line chart showing the exponential increase in drug development costs from $74M (1960) to $3,861M (2019), inflation-adjusted to 2020 USD.

## Data Quality Notes

- **Inflation Adjustment:** All monetary values adjusted to 2020 USD using CPI data
- **Time Range:** Primary datasets cover 1901-2000 (99 years)
- **CPI Data:** Separate sheet contains Consumer Price Index data (1913-2020) used for adjustments
- **Chart Generation:** Original Excel charts were not pre-rendered images; new charts created from CSV data using Python/Quarto

## Usage Examples

### Python

```python
import pandas as pd

# Load the main historical dataset
df = pd.read_csv('historical-life-expectancy-fda-budget-drug-costs-1901-2000.csv')
print(df.head())
```

### R

```r
# Load the diminishing returns data
df <- read.csv('life-expectancy-gains-pre-post-fda-comparison-1901-2000.csv')
summary(df)
```

## Sources

See [data-sources-references.csv](data-sources-references.csv) for complete list of source URLs including:

- FDA budget documentation
- Drug development cost studies
- Clinical trial cost analyses
- Historical life expectancy data
