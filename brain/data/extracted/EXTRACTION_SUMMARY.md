# Excel Extraction Summary

## Source File
`assets/life-expectancy-healthcare-spending-cost-of-drug-development.xlsx`

## Extraction Date
October 24, 2025

## Data Extracted

### CSV Files (11 sheets)

1. **drug-cost-and-lifespan.csv** (119 rows, 4 columns)
   - Year (1901-2020)
   - US Life expectancy
   - FDA Budget (Inflation Adjusted to 2020 USD)
   - Cost to Develop 1 New Drug (Inflation Adjusted to 2020 USD)

2. **spending-lifespan-transposed.csv** (20 rows, 3 columns)
   - Year (2000-2018)
   - US Healthcare Spending Per Person
   - Life Expectancy

3. **health-spending-and-lifespan.csv** (20 rows, 3 columns)
   - Year (2000-2018)
   - US Healthcare Spending Per Person
   - Life Expectancy

4. **uk.csv** (19,028 rows, 4 columns)
   - Detailed UK historical data

5. **lifespan-and-jama.csv** (219 rows, 3 columns)
   - Historical life expectancy data
   - JAMA founding correlation (1893)

6. **drugs-diseases-studied.csv** (4 rows, 3 columns)
   - Distribution of drugs vs diseases studied

7. **holocaust.csv** (5 rows, 3 columns)
   - Comparative death statistics

8. **tokenomics.csv** (6 rows, 5 columns)
   - Economic modeling data

9. **healthcare-spending.csv** (20 rows, 3 columns)
   - Healthcare spending trends

10. **units.csv** (64 rows, 19 columns)
    - Measurement units and conversions

11. **life-expectancy.csv** (19,028 rows, 4 columns)
    - Comprehensive life expectancy historical data

### Charts Identified

**Total Charts:** 14 charts across multiple sheets

- **ScatterChart:** 8 charts
- **LineChart:** 4 charts
- **PieChart:** 1 chart
- **BarChart:** 1 chart

## Quarto Files Created

### 1. FDA Spending, Life Expectancy, and Drug Costs Combined
**File:** `brain/figures/fda-spending-life-expectancy-drug-costs-combined.qmd`

**Generated Images:**
- `fda-spending-life-expectancy-drug-costs-combined.png`

**Features:**
- Multi-axis chart showing:
  - US Life Expectancy (1901-2020)
  - FDA Budget (inflation-adjusted)
  - Drug Development Costs (inflation-adjusted)
- Annotation marking 1962 Kefauver-Harris Amendment
- Statistical analysis of growth rates

**Key Finding:**
- Life expectancy growth slowed from 4 years/year (pre-1962) to 2 years/year (post-1962)
- Drug development costs increased from $74M to $2.6B (inflation-adjusted)

### 2. Healthcare Spending vs Life Expectancy
**File:** `brain/figures/healthcare-spending-vs-life-expectancy.qmd`

**Generated Images:**
- `healthcare-spending-vs-life-expectancy.png`
- `healthcare-spending-vs-life-expectancy-scatter.png`

**Features:**
- Dual-axis time series (2000-2018)
- Scatter plot with trend line
- Cost-per-year-of-life analysis
- Correlation statistics

**Key Finding:**
- Healthcare spending increased 129% (2000-2018)
- Life expectancy increased only 2.04 years
- Demonstrates diminishing returns on healthcare spending

## Data Quality Notes

### Cleaned Data
- Removed empty columns
- Dropped rows with no data
- Handled NaN values appropriately
- Standardized column names

### Data Ranges
- **Historical data:** 1901-2020 (drug costs)
- **Modern healthcare data:** 2000-2018
- **UK data:** Very detailed (19,028 rows)

## Chart Metadata
Full chart metadata including series references saved to:
`brain/data/extracted/chart_metadata.json`

## Next Steps (Future Enhancements)

### Additional Charts to Create
1. **Lifespan and JAMA founding** (scatter chart showing correlation)
2. **Drugs vs Diseases studied** (pie chart)
3. **Holocaust comparison** (bar chart)
4. **UK vs US comparison** (line chart)

### Potential Improvements
- Add more statistical analysis (regression, R-squared values)
- Create interactive Plotly versions
- Add confidence intervals where appropriate
- Compare multiple countries
- Add data sources and citations directly in charts

## Technical Stack
- **Data extraction:** Python 3.10, openpyxl, pandas
- **Visualization:** matplotlib, numpy
- **Documentation:** Quarto with Python kernel
- **Output:** PNG (300 DPI) and HTML

## Usage

To render all charts:
```bash
cd brain/figures
quarto render fda-spending-life-expectancy-drug-costs-combined.qmd
quarto render healthcare-spending-vs-life-expectancy.qmd
```

To update data extraction:
```bash
python scripts/extract-excel-data.py
```

## Data Location
- **Source:** `assets/life-expectancy-healthcare-spending-cost-of-drug-development.xlsx`
- **Extracted CSV:** `brain/data/extracted/*.csv`
- **Chart metadata:** `brain/data/extracted/chart_metadata.json`
- **Generated charts:** `brain/figures/*.png`
- **Quarto source:** `brain/figures/*.qmd`
