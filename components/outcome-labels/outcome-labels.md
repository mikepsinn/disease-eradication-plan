# 🏷 Outcome Labels

![outcome-labels-plugin.png](https://static.crowdsourcingcures.org/dfda/components/outcome-labels/outcome-labels.png)

**Imagine a world where food labels actually helped you make healthier choices.**  For decades, we've been presented with nutrition labels focused on micronutrients like Riboflavin.

![](outcome-labels.md)

But let's be honest:  **how actionable is knowing the amount of Riboflavin for the average person trying to improve their health and prevent disease?**  The alarming rise in chronic diseases despite the prevalence of these labels suggests they are missing the mark.

**Introducing Outcome Labels: A revolutionary approach to food and product labeling.**  Instead of listing obscure nutrients, Outcome Labels directly address what matters most:  **the impact of a product on your health outcomes and symptoms.**

We've developed these innovative labels, generating them for thousands of foods, drugs, and supplements, available at [studies.crowdsourcingcures.org](https://studies.crowdsourcingcures.org).  These labels are powered by the analysis of over 10 million data points, contributed anonymously by more than 10,000 participants through the [app.crowdsourcingcures.org](https://app.crowdsourcingcures.org).


![](https://crowdsourcingcures.org/wp-content/uploads/2021/05/nutrition-facts-vs-outcome-labels-melatonin-1024x592.png)

## Examples of Outcome Labels

To illustrate how Outcome Labels might look and the information they convey, here are a few examples:

**Example 1: Broccoli**

* **Outcome:**  Inflammation
* **Label:**  ![Outcome Label: Broccoli - Inflammation](https://static.crowdsourcingcures.org/dfda/components/outcome-labels/broccoli-inflammation.png)  **Significantly Improves**
* **Explanation:**  Aggregated N1 studies suggest that regular consumption of broccoli is associated with a significant reduction in inflammation markers.

* **Outcome:**  Depression Symptoms
* **Label:** ![Outcome Label: Broccoli - Depression](https://static.crowdsourcingcures.org/dfda/components/outcome-labels/broccoli-depression.png) **Slightly Improves**
* **Explanation:**  Some evidence from aggregated N1 studies indicates a mild positive effect of broccoli consumption on depression symptoms. More data is needed to strengthen this finding.


**Example 2:  Melatonin Supplement (3mg)**

* **Outcome:** Sleep Quality
* **Label:** ![Outcome Label: Melatonin - Sleep Quality](https://static.crowdsourcingcures.org/dfda/components/outcome-labels/melatonin-sleep-quality.png) **Moderately Improves**
* **Explanation:**  Aggregated N1 studies and clinical trial data show that melatonin supplementation at 3mg can moderately improve sleep quality for some individuals.

* **Outcome:**  Daytime Drowsiness
* **Label:** ![Outcome Label: Melatonin - Drowsiness](https://static.crowdsourcingcures.org/dfda/components/outcome-labels/melatonin-drowsiness.png) **Slightly Worsens**
* **Explanation:**  A small percentage of users in N1 studies reported experiencing mild daytime drowsiness as a side effect of melatonin supplementation.


**Example 3:  Processed Sugar**

* **Outcome:**  Blood Sugar Levels
* **Label:** ![Outcome Label: Processed Sugar - Blood Sugar](https://static.crowdsourcingcures.org/dfda/components/outcome-labels/sugar-blood-sugar.png) **Significantly Worsens**
* **Explanation:**  Aggregated N1 studies and epidemiological data consistently demonstrate that high consumption of processed sugar leads to a significant increase in blood sugar levels.

* **Outcome:**  Energy Levels
* **Label:** ![Outcome Label: Processed Sugar - Energy Levels](https://static.crowdsourcingcures.org/dfda/components/outcome-labels/sugar-energy-levels.png) **Moderately Worsens (Long-Term)**
* **Explanation:** While processed sugar may provide a short-term energy boost, aggregated data suggests that high consumption is associated with a moderate decrease in sustained energy levels over time.


**Note:**  These are illustrative examples and the actual Outcome Labels and their effects would be based on real-world data analysis. The labels would also include more detailed explanations and links to the underlying evidence.  The appearance of the labels (icons, color-coding, etc.) is also subject to design and user feedback.

## Limitations and Future Improvements

Despite the potential of Outcome Labels, there are current limitations that need to be addressed to enhance their accuracy and usefulness.  Although we've collected over 10 million data points, the usefulness and accuracy of Outcome Labels are currently limited because the number of study participants who have donated data for a particular food paired with a particular symptom is still small. In observational research like ours, a very large number of participants are required to cancel out all the errors and coincidences that can influence the data for a single individual.

For instance, someone with depression may have started taking an antidepressant at the same time they started seeing a therapist. Then, if their depression improves, it’s impossible to know if the improvement was a result of the antidepressant, the therapist, both, or something else. These random factors are known as confounding variables. However, random confounding factors can cancel each other out when looking at large data sets. This is why it’s important to collect as much data as possible.

To enhance the accuracy and usefulness of Outcome Labels, we are focusing on the following key improvements:

1. **Data Quantity:** As mentioned earlier, the number of data points for specific food-symptom or treatment-symptom pairs is still limited.  More data is crucial to improve the statistical power and reliability of the causal inference models.  Future efforts will focus on increasing user participation and data donation to address this limitation.

2. **Data Quality:** The quality of data is as important as quantity.  Observational data collected from individuals can be noisy and subject to various biases.  Improvements in data collection methods, data validation, and data cleaning are necessary to enhance the signal-to-noise ratio and reduce biases.  This includes implementing better tools for users to input data accurately and consistently, as well as developing algorithms to detect and handle outliers or inconsistencies in the data.

3. **Algorithm Refinement:** The causal inference algorithms used to generate Outcome Labels are continuously being refined.  Future improvements may include:
    - Incorporating more sophisticated causal inference techniques to better handle confounding variables and complex interactions.
    - Developing personalized Outcome Labels that take into account individual user characteristics and health profiles.
    - Utilizing machine learning methods to identify patterns and relationships in the data that may not be apparent with traditional statistical methods.
    - Improving the transparency and interpretability of the algorithms to build user trust and understanding.

Addressing these limitations through ongoing research and development will be key to realizing the full potential of Outcome Labels as a tool for personalized health and wellness.

## Interpretation of Outcome Labels

It's important to understand how to interpret Outcome Labels to make informed health decisions:

- **Direction of Effect:** The labels clearly indicate whether a product is likely to *improve* or *worsen* a specific health outcome or symptom.
- **Magnitude of Effect:** The labels also convey the *magnitude* of the effect (e.g., Slightly, Moderately, Significantly). This is based on the aggregated causal effect estimates from N1 studies.  "Significantly Improves/Worsens" indicates a strong and consistent effect observed in the data. "Moderately Improves/Worsens" suggests a noticeable but less pronounced effect. "Slightly Improves/Worsens" indicates a mild or less certain effect, where more data may be needed for confirmation.
- **Outcome-Specific:** Each Outcome Label is specific to a particular health outcome or symptom (e.g., Inflammation, Depression Symptoms, Sleep Quality).  A product may have different labels for different outcomes.
- **Population-Average Estimates:** Outcome Labels represent population-average estimates based on aggregated data. Individual responses to a product may vary.  Factors such as genetics, lifestyle, and health status can influence individual outcomes.
- **Evidence-Based, Not Definitive:** Outcome Labels are derived from the best available evidence, primarily aggregated N1 studies and other data sources.  However, they are not definitive proof of causation or guaranteed individual outcomes.  The strength of the evidence may vary depending on the data quantity and quality for a specific product-outcome pair.
- **Dynamic and Evolving:** Outcome Labels are dynamic and may evolve as more data becomes available and algorithms are refined.  Regular updates will ensure that the labels reflect the latest evidence.

**Using Outcome Labels for Health Decisions:**

Outcome Labels are intended to be a helpful tool to guide individuals in making more informed choices about foods, drugs, and supplements.  Here's how you can use them:

1. **Prioritize Outcomes:** Identify the health outcomes or symptoms that are most relevant to you.
2. **Compare Products:** When choosing between similar products, compare their Outcome Labels for your prioritized outcomes.
3. **Consider Magnitude:** Pay attention to the magnitude of the effect indicated by the label.  A "Significantly Improves" label suggests a stronger potential benefit than a "Slightly Improves" label.
4. **Look for Explanations:**  Read the explanations associated with each label to understand the evidence and context behind the assessment.
5. **Consult Professionals:**  Outcome Labels are not a substitute for professional medical advice.  Consult with your doctor or other qualified healthcare provider for personalized health recommendations.

By understanding how to interpret Outcome Labels and using them in conjunction with professional advice, individuals can take a more proactive and data-driven approach to managing their health and wellness.

## Calculation of Outcome Labels

Outcome labels are calculated using aggregated N-of-1 (N1) studies.  Here's a breakdown of the process:

1. **Individual N1 Studies:** For each user, we analyze their personal health data as an individual N1 study. This data includes time series data on:
    - **Treatments and Foods:**  Records of treatments taken (drugs, supplements) and foods consumed.
    - **Outcomes and Symptoms:**  Measurements of health outcomes and symptom severity over time.

2. **Causal Inference from Time Series Data:** We apply causal inference techniques to each individual's time series data. This allows us to estimate the causal effect of specific treatments or foods on their outcomes and symptoms.  By analyzing changes in outcomes following the introduction or removal of a treatment or food, we can infer potential causal relationships.

3. **Aggregation Across Users:** The causal effect estimates from individual N1 studies are then aggregated across all users in our dataset. This aggregation provides an average estimated effect of each treatment or food on specific outcomes across the user population.

4. **Outcome Label Display:** The aggregated causal effect estimates are used to generate the Outcome Labels. These labels display the degree to which a product (food, drug, supplement) is likely to improve or worsen specific health outcomes or symptoms, based on the aggregated analysis of N1 studies.

This approach leverages the power of aggregated personal data to provide more relevant and personalized health information compared to traditional nutrition labels.

## Conclusion

Outcome Labels represent a significant step towards empowering individuals with more relevant and actionable health information. By leveraging aggregated N1 studies and focusing on health outcomes, they offer a potentially transformative approach to product labeling, bridging the gap between scientific evidence and consumer understanding.  As data quantity and quality improve, and algorithms become more refined, Outcome Labels have the potential to become an indispensable tool for personalized health and wellness.

## Visual Representation of Outcome Labels

Outcome Labels are designed to be easily understandable and visually informative at a glance.  Key visual elements include:

- **Icons:**  Distinct icons are used to represent different health outcomes or symptoms (e.g., a brain icon for cognitive function, a heart icon for cardiovascular health, etc.).  These icons provide a quick visual cue to the topic of the label.
- **Direction Arrows:** Arrows indicate the direction of the effect.  An upward arrow (↑) signifies "Improves," while a downward arrow (↓) signifies "Worsens."
- **Magnitude Indicators:**  Terms like "Slightly," "Moderately," and "Significantly" are used to convey the magnitude of the effect.  These terms may be further reinforced by visual cues such as color-coding or bar lengths in future iterations.  For example, "Significantly Improves" might be displayed in bright green, "Moderately Improves" in light green, "Slightly Improves" in pale green, "Neutral" in gray, "Slightly Worsens" in pale red, "Moderately Worsens" in light red, and "Significantly Worsens" in bright red.
- **Color Coding:**  Color can be used to reinforce the direction and magnitude of the effect, with green hues for positive effects (improves) and red hues for negative effects (worsens).  Neutral effects could be represented in gray or a similar neutral color.

The combination of icons, arrows, magnitude indicators, and color coding aims to create Outcome Labels that are intuitive and readily interpretable by a wide range of users, regardless of their health literacy level.  The visual design is intended to quickly communicate the essential information about a product's impact on specific health outcomes.

## Data Sources

Several types of data are used to derive the Outcome Labels. Each data source provides unique insights and contributes to a more comprehensive understanding of health outcomes:

1. **Individual Micro-Level Data:** This is the most granular and personalized data source. It includes:
    - **User-Entered Data:** Data manually entered by users into the [safe.dfda.earth](http://safe.dfda.earth) platform, such as symptom logs, food diaries, and treatment records.
    - **Imported Data:** Data automatically imported from wearable devices, health apps, and other sources, providing objective measurements of activity levels, sleep patterns, and physiological parameters.
    - **Shopping Receipts:**  Data extracted from shopping receipts for foods, drugs, and nutritional supplements, offering detailed information on user purchases and consumption patterns.
    - **Insurance Claim Data:** Anonymized and aggregated insurance claim data, providing insights into healthcare utilization, diagnoses, and treatment costs at a population level.

    Micro-level data is crucial for conducting individual N1 studies and capturing the heterogeneity of treatment effects across individuals.

2. **Macro-Level Epidemiological Data:** This data source provides a broader population-level perspective. It encompasses:
    - **Disease Incidence Data:**  Statistics on the occurrence of various diseases over time, obtained from public health agencies and research institutions.
    - **Drug and Food Additive Consumption Data:**  Data on the overall consumption of different drugs, food additives, and environmental exposures at a national or regional level.

    Analyzing macro-level data can reveal long-term trends and population-wide effects that may not be apparent from individual-level data alone.  It can also help identify potential environmental or policy-level factors influencing health outcomes.  However, it is important to note that drawing causal inferences from macro-level data is challenging due to the ecological fallacy and potential confounding factors.

3. **Clinical Trial Data:**  This is considered the "gold standard" data source in traditional medical research due to its controlled and rigorous nature.
    - **Randomized Controlled Trials (RCTs):** Data from RCTs, where participants are randomly assigned to treatment and control groups, provides the strongest evidence for causal relationships between interventions and outcomes.
    - **Systematic Reviews and Meta-Analyses:**  Aggregated data from multiple clinical trials, synthesized through systematic reviews and meta-analyses, can increase statistical power and provide more robust estimates of treatment effects.

    While clinical trial data is invaluable, it has limitations in the context of Outcome Labels:
    - **Limited Scope:** Clinical trials are often focused on specific drugs or interventions and may not cover the wide range of foods, supplements, and lifestyle factors relevant to Outcome Labels.
    - **Selected Populations:**  Trial participants are often highly selected and may not be representative of the general population, limiting the generalizability of findings.
    - **Cost and Ethical Constraints:**  Conducting large-scale clinical trials for all potential factors influencing health outcomes is prohibitively expensive and may raise ethical concerns, especially for interventions with uncertain risks or benefits.

Despite these limitations, clinical trial data serves as an important validation benchmark and complementary data source for Outcome Labels, particularly for well-studied drugs and medical interventions.
