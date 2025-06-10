import matplotlib.pyplot as plt
import numpy as np

# Data: [Intervention, Lower QALYs per $1M, Upper QALYs per $1M]
# The dFDA platform data is derived from the cost-benefit analysis document (economic-models/dfda-cost-benefit-analysis.md).
# Lower bound: Conservative QALYs (190k) / Higher-end Ops Cost ($40.05M) = ~4,744
# Upper bound: Optimistic QALYs (3.65M) / Lower-end Ops Cost ($18.75M) = ~194,667
#
# Other interventions are based on the ICERs in the main analysis document.
# QALYs per $1M = 1,000,000 / ICER
# Dominant or cost-saving interventions are given high illustrative values.
interventions = [
    ("dFDA Platform", 4744, 194667),
    ("Smallpox Eradication", 10000, 100000), # Illustrative high range for dominant intervention
    ("Childhood Vaccinations", 22, 10000), # From dominant (high value) to ~$45k/QALY (1M/45k=22)
    ("Clean Water Programs", 100, 1000), # $1k-$10k/QALY -> 1M/10k=100, 1M/1k=1000
    ("Hypertension Screening", 30, 53), # $19k-$33k/QALY -> 1M/33k=30, 1M/19k=53
    ("Generic Drug Substitution", 1000, 10000), # Illustrative high range for dominant intervention
    ("Statins / Polypill", 67, 1000), # From cost-saving (high value) to ~$15k/QALY (1M/15k=67)
]

# Extract data for plotting
labels = [x[0] for x in interventions]
low_vals = np.array([x[1] for x in interventions])
high_vals = np.array([x[2] for x in interventions])

# Calculate midpoints and error ranges for the linear scale
mid_points = (low_vals + high_vals) / 2
errors = (high_vals - low_vals) / 2

# Plotting
fig, ax = plt.subplots(figsize=(14, 8))
y_pos = np.arange(len(labels))

# Create horizontal bars at the midpoint, with error bars
ax.barh(y_pos, mid_points, xerr=errors, align='center', height=0.6,
        color='skyblue', ecolor='gray', capsize=5)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=12)
ax.invert_yaxis()  # Highest QALYs at the top

# Formatting
ax.set_xlabel('QALYs Gained per $1M of Spending', fontsize=12, labelpad=10)
ax.set_title('Cost-Effectiveness of Health Interventions (QALYs Gained per $1M)', pad=20, fontsize=16)
ax.grid(axis='x', linestyle='--', alpha=0.7)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(axis='y', length=0)
ax.tick_params(axis='x', labelsize=10)

# Add value labels for the ranges
for i, (low, high) in enumerate(zip(low_vals, high_vals)):
    label_text = f"{low:,.0f} - {high:,.0f}"
    ax.text(high * 1.05, i, label_text, va='center', ha='left', fontsize=10, color='dimgray')

plt.tight_layout()

# Save the figure
plt.savefig('economic-models/qaly-comparison-chart.png', dpi=300)

print("Chart saved to economic-models/qaly-comparison-chart.png") 