import matplotlib.pyplot as plt
import numpy as np

# Data: [Intervention, Lower QALY, Upper QALY]
# Upper bound for "10,000+" is set to 20,000 for visualization, will be noted in text.
# For single-point estimates, lower and upper are the same.
interventions = [
    ("dFDA Platform", 5000, 15000),
    ("Smallpox Eradication", 10000, 20000), # Upper bound is indicative
    ("Public Health (Water, Vax, etc.)", 1000, 10000),
    ("Hypertension Screening", 200, 2000),
    ("Generic Drug Substitution", 100, 1000),
    ("Statins / Polypill", 50, 200),
]

# Extract data for plotting
labels = [x[0] for x in interventions]
low_vals = np.array([x[1] for x in interventions])
high_vals = np.array([x[2] for x in interventions])

# Calculate midpoints and error ranges for the linear scale
mid_points = (low_vals + high_vals) / 2
errors = [(high_vals - low_vals) / 2, (high_vals - low_vals) / 2]

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))
y_pos = np.arange(len(labels))

# Create horizontal bars at the midpoint, with error bars
ax.barh(y_pos, mid_points, xerr=errors, align='center', height=0.6,
        color='skyblue', ecolor='gray', capsize=5)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis()  # Highest QALYs at the top

# Formatting
ax.set_xlabel('QALYs Gained per $1M')
ax.set_title('Comparison of Health Interventions by QALYs Gained per $1M', pad=20)
ax.grid(axis='x', linestyle='--', alpha=0.7)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(axis='y', length=0)

# Add value labels for the ranges
for i, (low, high, mid) in enumerate(zip(low_vals, high_vals, mid_points)):
    label = f"{low:,.0f} - {high:,.0f}"
    if high == 20000:
        label = f"{low:,.0f}+"
    ax.text(high * 1.05, i, label, va='center', ha='left', fontsize=10, color='dimgray')

plt.tight_layout()

# Save the figure
plt.savefig('economic-models/qaly-comparison-chart.png', dpi=300)

print("Chart saved to economic-models/qaly-comparison-chart.png") 