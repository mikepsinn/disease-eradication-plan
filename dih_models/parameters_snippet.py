
IAB_MECHANISM_ANNUAL_COST = Parameter(
    750_000_000,
    source_ref="/knowledge/appendix/incentive-alignment-bonds-paper.qmd#welfare-analysis",
    source_type="definition",
    description="Estimated annual cost of the IAB mechanism (high-end estimate including regulatory defense)",
    display_name="IAB Mechanism Annual Cost (High Estimate)",
    unit="USD/year",
    confidence_interval=(160_000_000, 750_000_000),
    keywords=["iab", "cost", "overhead", "annual"],
)  # $750M high end estimate

IAB_MECHANISM_BENEFIT_COST_RATIO = Parameter(
    TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS / IAB_MECHANISM_ANNUAL_COST,
    source_ref="/knowledge/appendix/incentive-alignment-bonds-paper.qmd#welfare-analysis",
    source_type="calculated",
    description="Benefit-Cost Ratio of the IAB mechanism itself",
    display_name="IAB Mechanism Benefit-Cost Ratio",
    unit="ratio",
    keywords=["bcr", "benefit cost ratio", "iab", "mechanism"],
    inputs=["TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS", "IAB_MECHANISM_ANNUAL_COST"],
    compute=lambda ctx: ctx["TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS"] / ctx["IAB_MECHANISM_ANNUAL_COST"]
)  # 303:1
