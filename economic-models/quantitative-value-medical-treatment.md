# Quantifying the Value of Medical Treatments to Humanity

Evaluating the benefit of a new medical treatment to humanity requires a quantitative approach that goes beyond simple efficacy metrics.  One widely accepted method for this is the use of **Quality-Adjusted Life Years (QALYs)**. QALYs provide a standardized measure that combines both the **quantity** and **quality** of life gained from a medical intervention.

## Understanding QALYs

A QALY represents one year of life in perfect health.  It's a composite metric that considers both how long a treatment extends life and how much the quality of that life is improved.  A QALY value of 1 represents a year of perfect health, while 0 represents death.  Values in between represent years lived in less than perfect health, scaled according to health-related quality of life.

## Mathematical Framework

The basic formula for calculating QALYs gained from a treatment is:

**QALYs Gained = (Years of Life Gained) x (Quality of Life Improvement)**

To be more precise, if we consider a treatment that extends life and improves quality of life, we can calculate the QALYs gained as follows:

Let:
-  \( Q_0 \) be the baseline quality of life (a value between 0 and 1) without the treatment.
-  \( Q_1 \) be the quality of life with the treatment (a value between 0 and 1).
-  \( T_0 \) be the life expectancy without the treatment.
-  \( T_1 \) be the life expectancy with the treatment.

The QALYs without treatment would be approximately \( Q_0 \times T_0 \).
The QALYs with treatment would be approximately \( Q_1 \times T_1 \).

Therefore, the **QALYs Gained** from the treatment is:

**QALYs Gained =  \( (Q_1 \times T_1) - (Q_0 \times T_0) \) **

In practice, quality of life (\(Q\)) is often assessed using questionnaires and scales that quantify different aspects of health, such as mobility, self-care, usual activities, pain/discomfort, and anxiety/depression. These assessments are then converted into a utility score between 0 and 1.

## Economic Value and Cost-Utility Analysis

QALYs are crucial in **cost-utility analysis (CUA)**, a type of economic evaluation used in healthcare. CUA compares the cost of a medical intervention to the QALYs it generates.  This allows healthcare decision-makers to assess the **value for money** of different treatments and allocate resources efficiently.

A common metric derived from CUA is the **Incremental Cost-Effectiveness Ratio (ICER)**:

**ICER = (Cost of Treatment - Cost of Alternative) / (QALYs Gained from Treatment - QALYs Gained from Alternative)**

The ICER represents the additional cost per QALY gained by using the new treatment compared to an alternative.  Decision-makers often use thresholds (e.g., $50,000 - $150,000 per QALY in the US) to determine if a treatment is cost-effective.

## Concrete Examples

### Hip Replacement

Hip replacement surgery is a well-established intervention with significant QALY gains. A study in *BMJ Open* found that approximately 90.7% of patients undergoing hip replacement gained positive QALYs, with a mean gain of **0.8 QALYs over 5 years** [^1]. This means that on average, hip replacement surgery provides nearly one year of perfect health over five years for patients with hip joint problems.

[^1]: [The economic benefit of hip replacement: a 5-year follow-up of costs...](https://bmjopen.bmj.com/content/2/3/e000752)

### Statins for Primary Prevention of Cardiovascular Disease

Statins, used for primary prevention of cardiovascular disease, also demonstrate QALY gains. A study in *BMJ* estimated that statin treatment provides a gain of **0.20 QALYs in men aged 60 years** [^2]. While this gain is smaller than hip replacement, statin therapy is applied to a much larger population, resulting in a substantial overall benefit to public health.

[^2]: [Comparing treatments in terms of absolute benefit - Better...](https://www.ncbi.nlm.nih.gov/books/NBK426103/)


### Hypothetical Example

To further illustrate, let's consider a new drug for a chronic disease that:

- Extends life expectancy by 5 years ( \( T_1 = T_0 + 5 \) ).
- Improves quality of life from 0.6 to 0.8 ( \( Q_0 = 0.6 \), \( Q_1 = 0.8 \) ).

Assuming a baseline life expectancy without treatment of \( T_0 = 20 \) years.

QALYs without treatment = \( 0.6 \times 20 = 12 \) QALYs.
QALYs with treatment = \( 0.8 \times (20 + 5) = 0.8 \times 25 = 20 \) QALYs.

**QALYs Gained = \( 20 - 12 = 8 \) QALYs.**

This new drug provides a substantial gain of 8 QALYs.  If the cost of this treatment is, for example, $100,000 more than the existing alternative, the ICER would be $100,000 / 8 QALYs = $12,500 per QALY, which might be considered very cost-effective depending on the established thresholds.

## Sources

- **Cost-Effectiveness, the QALY, and the evLYG - ICER:** [https://icer.org/our-approach/methods-process/cost-effectiveness-the-qaly-and-the-evlyg/](https://icer.org/our-approach/methods-process/cost-effectiveness-the-qaly-and-the-evlyg/)
- **Quality-adjusted life year - Wikipedia:** [https://en.wikipedia.org/wiki/Quality-adjusted_life_year](https://en.wikipedia.org/wiki/Quality-adjusted_life_year)
- **Cost utility analysis: health economic studies - GOV.UK:** [https://www.gov.uk/guidance/cost-utility-analysis-health-economic-studies](https://www.gov.uk/guidance/cost-utility-analysis-health-economic-studies)

## Conclusion

QALYs offer a valuable framework for quantifying the overall benefit of medical treatments to humanity. By incorporating both survival and quality of life into a single metric, QALYs facilitate informed decision-making in healthcare, resource allocation, and the evaluation of new medical interventions.  While QALYs have limitations and are subject to ethical debates, they remain a cornerstone of health economics and provide a crucial tool for assessing the quantitative value of medical advancements.
