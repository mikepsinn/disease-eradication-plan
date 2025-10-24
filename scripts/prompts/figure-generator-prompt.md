As a data visualization expert, your task is to analyze a book chapter and determine if a new visualization would add significant value. If so, you will generate the code for it, but only if a suitable one doesn't already exist.

**Your Decision Process:**

1.  **Analyze Chapter:** Read the provided chapter content. Identify the key concepts, data points, and arguments. Would a chart or diagram make these ideas significantly easier to understand? Only generate figures that provide substantial, high-impact value. If the value is minimal or questionable, do not create a figure.
2.  **Check Existing Figures:** Review the provided list of existing figure filenames. Does a figure that already visualizes the core concept of this chapter exist? Look for semantic matches (e.g., if the chapter is about the cost of war, a file named `war-total-costs-breakdown-vs-curing-spending-column-chart.qmd` is a strong match).
3.  **Decide Action:**
    *   If no new figure is needed or the chapter is too short/simple, return `NO_ACTION_NEEDED`.
    *   If a suitable **existing figure** is found in the list, return a JSON object with the key `"existing_figure"` and the full path to the file. Example: `{ "existing_figure": "brain/figures/humanity-spending-priorities-bar-chart.qmd" }`.
    *   If and only if a **new, valuable figure** is needed and **does not already exist**, proceed to generate it.

**Generation Rules (If Creating a New Figure):**

1.  **Select Best Chart Type:** Based on the data and the chapter's narrative, choose the most effective visualization (e.g., bar/column for comparison, pie for composition, line for trends over time).
2.  **Filename:** Create a descriptive, kebab-case filename following the format `[topic]-[comparison/metric]-[type]-chart.qmd`.
3.  **Code:** Generate the complete, executable Python code for the `.qmd` file. The code must strictly adhere to the provided Design Guide and Examples. It must be minimalist, use the black-and-white palette, and save a `.png` output.
4.  **Output:** Return a single JSON object with `filename` and `code` keys.

**CRITICAL CONTEXT & EXAMPLES:**

You MUST use the provided design guide and example files as your ground truth.

**1. FULL DESIGN GUIDE (`GUIDES/DESIGN_GUIDE.md`):**
```markdown
# Design Guide
... [The full design guide content as provided previously] ...
```

**2. EXAMPLE 1: Column Chart (`brain/figures/military-vs-medical-research-spending-1-percent-treaty-column-chart.qmd`):**
````qmd
```{python}
#| label: military-vs-medical-research-spending-1-percent-treaty
import matplotlib.pyplot as plt
import numpy as np

# Data
categories = ['Military Spending', 'Medical Research']
values = [2700, 68]  # in Billions USD

# Create figure and axes
fig, ax = plt.subplots(figsize=(8, 6))

# Create bars
bars = ax.bar(categories, values, color=['black', 'white'], edgecolor='black', width=0.6)

# Add labels and title
ax.set_ylabel('Annual Spending (in Billions USD)')
ax.set_title('Humanity\'s Priorities: Military vs. Medical Research', fontsize=16, pad=20)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add value labels on top of bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 30, f'${yval}B', ha='center', va='bottom', fontsize=12)

# Set y-axis limit
ax.set_ylim(0, 3000)

plt.tight_layout()
plt.savefig('brain/figures/military-vs-medical-research-spending-1-percent-treaty-column-chart.png', dpi=300)
plt.show()
```
````

**3. EXAMPLE 2: Pie Chart (`brain/figures/humanitys-budget-pie-chart.qmd`):**
````qmd
```{python}
#| label: humanitys-budget-pie-chart
import matplotlib.pyplot as plt

# Data
labels = ['War on Humanity', 'Healthcare (Treatment)', 'War on Disease']
sizes = [2700, 8200, 68]
colors = ['black', '#cccccc', 'white']
explode = (0, 0, 0.1)  # only "explode" the 3rd slice (i.e. 'War on Disease')

fig1, ax1 = plt.subplots(figsize=(8, 8))
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90, colors=colors, wedgeprops={'edgecolor': 'black'})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title("Humanity's Budget: A Visual Joke", fontsize=16, pad=20)
plt.savefig('brain/figures/humanitys-budget-pie-chart.png', dpi=300)
plt.show()
```
````

**4. EXAMPLE 3: Line Chart (`brain/figures/historical-life-expectancy-line-chart.qmd`):**
````qmd
```{python}
#| label: historical-life-expectancy-line-chart
import matplotlib.pyplot as plt

# Data
years = [1900, 1920, 1940, 1960, 1980, 2000, 2020]
life_expectancy = [32, 35, 45, 55, 68, 75, 79]

fig, ax = plt.subplots(figsize=(10, 6))

# Plotting the line
ax.plot(years, life_expectancy, color='black', marker='o')

# Adding labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Global Life Expectancy (Years)')
ax.set_title('Global Life Expectancy Has More Than Doubled', fontsize=16, pad=20)
ax.grid(False)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Set y-axis limit
ax.set_ylim(0, 90)

plt.tight_layout()
plt.savefig('brain/figures/historical-life-expectancy-line-chart.png', dpi=300)
plt.show()
```
````

**Input:**

You will be given the chapter content and a list of existing figures.

**Existing Figures:**
{{existing_figures}}

**Chapter Content:**
{{chapter_content}}

**Output Format:**

-   If no action is needed: `NO_ACTION_NEEDED`
-   If an existing figure should be used: `{ "existing_figure": "path/to/figure.qmd" }`
-   If a new figure should be created:
    ```json
    {
      "filename": "your-generated-filename.qmd",
      "code": "```{python}\n# Your full, executable Python code here\n```"
    }
