"""
Budget Impact Score (BIS) Reference Data

Empirical data on government spending allocations and welfare outcomes from
high-performing countries. Used to ground BIS recommendations in revealed
preference from countries achieving top welfare metrics.

Sources:
- Life expectancy: OECD Health at a Glance 2023, WHO 2023
- Defense spending: SIPRI Military Expenditure Database 2024
- Health spending: OECD Health Statistics 2023 (current health expenditure)
- Education spending: OECD Education at a Glance 2023 (public)
- R&D spending: OECD Main Science and Technology Indicators 2023
- Total govt spending: IMF Fiscal Monitor 2024, OECD
- GDP per capita: World Bank 2023
- Median income: OECD/LIS 2022-2023

Countries achieving 6-7 more years of life expectancy than the US
spend significantly less on defense ($300-1500 vs $2800 per capita) and achieve
better outcomes. If their defense spending were inadequate, their welfare metrics
would reflect security failures (war deaths, economic disruption). They don't.
"""

from dataclasses import dataclass


@dataclass
class CountryData:
    """Spending and outcome data for a single country."""
    name: str
    population_millions: float
    gdp_per_capita: float  # USD (2023)
    life_expectancy: float  # Years (2023)
    median_income_ppp: float  # USD PPP (2022-2023)

    # Per capita spending in USD (2023)
    defense_per_capita: float
    health_per_capita: float  # Total health expenditure (public + private)
    education_per_capita: float  # Public education spending
    rd_per_capita: float  # Gross R&D expenditure

    # As % of total government spending
    defense_pct_govt: float
    health_pct_govt: float  # Public health as % of govt
    education_pct_govt: float

    # Total government spending per capita
    total_govt_per_capita: float

    notes: str = ""

    @property
    def defense_pct_gdp(self) -> float:
        return (self.defense_per_capita / self.gdp_per_capita) * 100

    @property
    def health_pct_gdp(self) -> float:
        return (self.health_per_capita / self.gdp_per_capita) * 100

    @property
    def education_pct_gdp(self) -> float:
        return (self.education_per_capita / self.gdp_per_capita) * 100

    @property
    def rd_pct_gdp(self) -> float:
        return (self.rd_per_capita / self.gdp_per_capita) * 100


# High-performing countries (top quartile on life expectancy)
# These serve as reference for "what works"
# Data from 2023 unless otherwise noted
HIGH_PERFORMERS = [
    CountryData(
        name="Japan",
        population_millions=124.5,
        gdp_per_capita=33800,
        life_expectancy=84.5,
        median_income_ppp=42000,
        defense_per_capita=340,  # 1.0% GDP
        health_per_capita=5100,  # 11.5% GDP (total, incl private)
        education_per_capita=1150,  # 3.4% GDP (public)
        rd_per_capita=1115,  # 3.3% GDP
        defense_pct_govt=2.3,
        health_pct_govt=24.0,  # Public health ~85% of total
        education_pct_govt=7.7,
        total_govt_per_capita=14870,  # 44% GDP
        notes="Highest life expectancy. Very low defense under US umbrella.",
    ),
    CountryData(
        name="Switzerland",
        population_millions=8.8,
        gdp_per_capita=98770,
        life_expectancy=84.2,
        median_income_ppp=54000,
        defense_per_capita=690,  # 0.7% GDP
        health_per_capita=9240,  # 11.8% GDP (highest per capita)
        education_per_capita=4940,  # 5.0% GDP
        rd_per_capita=3360,  # 3.4% GDP
        defense_pct_govt=2.1,
        health_pct_govt=22.0,  # Public ~67%
        education_pct_govt=15.3,
        total_govt_per_capita=32400,  # 32.8% GDP
        notes="Highest income. Neutral, minimal defense. Private health insurance.",
    ),
    CountryData(
        name="Singapore",
        population_millions=5.9,
        gdp_per_capita=82800,
        life_expectancy=84.1,
        median_income_ppp=65000,
        defense_per_capita=2480,  # 3.0% GDP - higher due to regional tensions
        health_per_capita=4700,  # 4.5% GDP (efficient)
        education_per_capita=2320,  # 2.8% GDP
        rd_per_capita=1820,  # 2.2% GDP
        defense_pct_govt=16.6,
        health_pct_govt=14.0,
        education_pct_govt=15.6,
        total_govt_per_capita=14900,  # 18% GDP - very low govt share
        notes="Higher defense due to regional tensions. Very efficient spending.",
    ),
    CountryData(
        name="Australia",
        population_millions=26.4,
        gdp_per_capita=64670,
        life_expectancy=83.5,
        median_income_ppp=52000,
        defense_per_capita=1295,  # 2.0% GDP
        health_per_capita=6470,  # 10.0% GDP
        education_per_capita=3300,  # 5.1% GDP
        rd_per_capita=1165,  # 1.8% GDP
        defense_pct_govt=5.3,
        health_pct_govt=19.5,
        education_pct_govt=13.4,
        total_govt_per_capita=24575,  # 38% GDP
        notes="Similar culture to US but 5+ years more life expectancy.",
    ),
    CountryData(
        name="Norway",
        population_millions=5.5,
        gdp_per_capita=87930,
        life_expectancy=83.2,
        median_income_ppp=51000,
        defense_per_capita=1320,  # 1.5% GDP (rising toward NATO 2%)
        health_per_capita=8540,  # 11.4% GDP (public ~86%)
        education_per_capita=5805,  # 6.6% GDP
        rd_per_capita=2025,  # 2.3% GDP
        defense_pct_govt=3.0,
        health_pct_govt=17.2,
        education_pct_govt=13.2,
        total_govt_per_capita=43965,  # 50% GDP
        notes="High spending, excellent outcomes. Oil wealth.",
    ),
    CountryData(
        name="Sweden",
        population_millions=10.5,
        gdp_per_capita=55690,
        life_expectancy=83.0,
        median_income_ppp=46000,
        defense_per_capita=725,  # 1.3% GDP (rising to 2% with NATO)
        health_per_capita=6240,  # 11.2% GDP
        education_per_capita=4010,  # 7.2% GDP
        rd_per_capita=1895,  # 3.4% GDP
        defense_pct_govt=2.7,
        health_pct_govt=20.0,
        education_pct_govt=14.7,
        total_govt_per_capita=27290,  # 49% GDP
        notes="Highest education spending as % GDP. Recently joined NATO.",
    ),
    CountryData(
        name="Spain",
        population_millions=47.4,
        gdp_per_capita=32690,
        life_expectancy=83.0,
        median_income_ppp=38000,
        defense_per_capita=425,  # 1.3% GDP
        health_per_capita=4045,  # 10.4% GDP (public ~71%)
        education_per_capita=1405,  # 4.3% GDP
        rd_per_capita=460,  # 1.4% GDP
        defense_pct_govt=2.7,
        health_pct_govt=18.3,
        education_pct_govt=9.0,
        total_govt_per_capita=15690,  # 48% GDP
        notes="High life expectancy despite lower income. Mediterranean diet.",
    ),
    CountryData(
        name="Italy",
        population_millions=58.9,
        gdp_per_capita=37150,
        life_expectancy=82.8,
        median_income_ppp=40000,
        defense_per_capita=555,  # 1.5% GDP
        health_per_capita=4020,  # 9.0% GDP (public ~77%)
        education_per_capita=1525,  # 4.1% GDP
        rd_per_capita=555,  # 1.5% GDP
        defense_pct_govt=2.7,
        health_pct_govt=15.2,
        education_pct_govt=7.5,
        total_govt_per_capita=20395,  # 54.9% GDP
        notes="High pension spending. Good health outcomes.",
    ),
    CountryData(
        name="France",
        population_millions=67.7,
        gdp_per_capita=44460,
        life_expectancy=82.5,
        median_income_ppp=45000,
        defense_per_capita=935,  # 2.1% GDP
        health_per_capita=5940,  # 11.5% GDP (public ~85%)
        education_per_capita=2310,  # 5.2% GDP
        rd_per_capita=975,  # 2.2% GDP
        defense_pct_govt=3.6,
        health_pct_govt=19.4,
        education_pct_govt=8.9,
        total_govt_per_capita=25965,  # 58.4% GDP
        notes="Nuclear power, higher defense. Strong social safety net.",
    ),
    CountryData(
        name="South Korea",
        population_millions=51.7,
        gdp_per_capita=33150,
        life_expectancy=82.7,
        median_income_ppp=44000,
        defense_per_capita=930,  # 2.8% GDP
        health_per_capita=3620,  # 8.8% GDP (public ~60%)
        education_per_capita=1490,  # 4.5% GDP
        rd_per_capita=1625,  # 4.9% GDP (highest)
        defense_pct_govt=8.3,
        health_pct_govt=16.0,
        education_pct_govt=13.2,
        total_govt_per_capita=11270,  # 34% GDP
        notes="Highest R&D spending. North Korea threat drives defense.",
    ),
]

# Reference country: United States
USA = CountryData(
    name="United States",
    population_millions=334.9,
    gdp_per_capita=80030,
    life_expectancy=78.4,
    median_income_ppp=52000,
    defense_per_capita=2800,  # 3.5% GDP - $886B / 335M
    health_per_capita=13280,  # 16.6% GDP - highest in world, poor outcomes
    education_per_capita=4000,  # 5.0% GDP (public)
    rd_per_capita=2800,  # 3.5% GDP
    defense_pct_govt=9.2,
    health_pct_govt=24.0,  # Public health ~50% of total
    education_pct_govt=13.2,
    total_govt_per_capita=30410,  # 38% GDP
    notes="Highest health spending, worst outcomes among peers. "
          "6 years below peer average life expectancy.",
)


def compute_reference_allocation() -> dict[str, float]:
    """
    Compute reference allocation based on high-performing countries.

    Returns percentage of discretionary budget (defense + health + education + R&D)
    that should go to each category, based on revealed preference from countries
    achieving top welfare outcomes.
    """
    n = len(HIGH_PERFORMERS)

    # Per capita averages
    avg_defense = sum(c.defense_per_capita for c in HIGH_PERFORMERS) / n
    avg_health = sum(c.health_per_capita for c in HIGH_PERFORMERS) / n
    avg_education = sum(c.education_per_capita for c in HIGH_PERFORMERS) / n
    avg_rd = sum(c.rd_per_capita for c in HIGH_PERFORMERS) / n

    # Discretionary total
    discretionary_total = avg_defense + avg_health + avg_education + avg_rd

    # Also compute % GDP averages for comparison
    avg_defense_pct = sum(c.defense_pct_gdp for c in HIGH_PERFORMERS) / n
    avg_health_pct = sum(c.health_pct_gdp for c in HIGH_PERFORMERS) / n
    avg_education_pct = sum(c.education_pct_gdp for c in HIGH_PERFORMERS) / n
    avg_rd_pct = sum(c.rd_pct_gdp for c in HIGH_PERFORMERS) / n

    return {
        # Shares of discretionary spending
        "defense": avg_defense / discretionary_total,
        "health": avg_health / discretionary_total,
        "education": avg_education / discretionary_total,
        "research": avg_rd / discretionary_total,

        # Per capita averages (USD)
        "_defense_per_capita": avg_defense,
        "_health_per_capita": avg_health,
        "_education_per_capita": avg_education,
        "_rd_per_capita": avg_rd,

        # % GDP averages (for comparison)
        "_defense_pct_gdp": avg_defense_pct,
        "_health_pct_gdp": avg_health_pct,
        "_education_pct_gdp": avg_education_pct,
        "_rd_pct_gdp": avg_rd_pct,
    }


def compute_us_gap() -> dict:
    """
    Compute the gap between US allocation and high-performer average.

    Returns dict with differences (positive = US spends more than peers).
    """
    ref = compute_reference_allocation()
    n = len(HIGH_PERFORMERS)

    avg_le = sum(c.life_expectancy for c in HIGH_PERFORMERS) / n

    return {
        # Per capita gaps (USD)
        "defense_gap_per_capita": USA.defense_per_capita - ref["_defense_per_capita"],
        "health_gap_per_capita": USA.health_per_capita - ref["_health_per_capita"],
        "education_gap_per_capita": USA.education_per_capita - ref["_education_per_capita"],
        "rd_gap_per_capita": USA.rd_per_capita - ref["_rd_per_capita"],

        # % GDP gaps
        "defense_gap_pct_gdp": USA.defense_pct_gdp - ref["_defense_pct_gdp"],
        "health_gap_pct_gdp": USA.health_pct_gdp - ref["_health_pct_gdp"],
        "education_gap_pct_gdp": USA.education_pct_gdp - ref["_education_pct_gdp"],
        "rd_gap_pct_gdp": USA.rd_pct_gdp - ref["_rd_pct_gdp"],

        # Outcome gap
        "life_expectancy_gap": USA.life_expectancy - avg_le,
    }


def print_comparison():
    """Print comparison between US and high-performers."""
    ref = compute_reference_allocation()
    gap = compute_us_gap()

    n = len(HIGH_PERFORMERS)
    avg_le = sum(c.life_expectancy for c in HIGH_PERFORMERS) / n
    avg_gdp = sum(c.gdp_per_capita for c in HIGH_PERFORMERS) / n

    print("=" * 80)
    print("SPENDING COMPARISON: US vs HIGH-PERFORMING COUNTRIES")
    print("=" * 80)
    print()
    print(f"High performers (n={n}): {', '.join(c.name for c in HIGH_PERFORMERS[:5])}...")
    print(f"Average GDP/capita: ${avg_gdp:,.0f}  |  US GDP/capita: ${USA.gdp_per_capita:,.0f}")
    print()

    # Per capita comparison
    print("PER CAPITA SPENDING (USD)")
    print("-" * 80)
    print(f"{'Category':<20} {'US':>12} {'Peers Avg':>12} {'Gap':>12} {'Gap %':>10}")
    print("-" * 80)

    def fmt_gap(us, peer):
        gap_val = us - peer
        gap_pct = (gap_val / peer * 100) if peer else 0
        return f"${gap_val:>+,}" if abs(gap_val) < 10000 else f"${gap_val/1000:>+,.1f}k", f"{gap_pct:>+.0f}%"

    for cat, us_val, peer_val in [
        ("Defense", USA.defense_per_capita, ref["_defense_per_capita"]),
        ("Health", USA.health_per_capita, ref["_health_per_capita"]),
        ("Education", USA.education_per_capita, ref["_education_per_capita"]),
        ("R&D", USA.rd_per_capita, ref["_rd_per_capita"]),
    ]:
        gap_str, pct_str = fmt_gap(us_val, peer_val)
        print(f"{cat:<20} ${us_val:>10,} ${peer_val:>10,.0f} {gap_str:>12} {pct_str:>10}")

    print("-" * 80)
    print(f"{'Life Expectancy':<20} {USA.life_expectancy:>10.1f}y {avg_le:>10.1f}y "
          f"{gap['life_expectancy_gap']:>+10.1f}y")
    print()

    # % GDP comparison
    print("AS % OF GDP")
    print("-" * 60)
    print(f"{'Category':<20} {'US':>10} {'Peers Avg':>12} {'Gap':>10}")
    print("-" * 60)
    print(f"{'Defense':<20} {USA.defense_pct_gdp:>9.1f}% {ref['_defense_pct_gdp']:>11.1f}% "
          f"{gap['defense_gap_pct_gdp']:>+9.1f}%")
    print(f"{'Health':<20} {USA.health_pct_gdp:>9.1f}% {ref['_health_pct_gdp']:>11.1f}% "
          f"{gap['health_gap_pct_gdp']:>+9.1f}%")
    print(f"{'Education':<20} {USA.education_pct_gdp:>9.1f}% {ref['_education_pct_gdp']:>11.1f}% "
          f"{gap['education_gap_pct_gdp']:>+9.1f}%")
    print(f"{'R&D':<20} {USA.rd_pct_gdp:>9.1f}% {ref['_rd_pct_gdp']:>11.1f}% "
          f"{gap['rd_gap_pct_gdp']:>+9.1f}%")
    print()

    print("INSIGHTS:")
    print(f"  1. US spends ${USA.defense_per_capita - ref['_defense_per_capita']:,.0f} MORE "
          f"per person on defense than high-performers.")
    print(f"  2. US spends ${USA.health_per_capita - ref['_health_per_capita']:,.0f} MORE "
          f"per person on health yet lives {abs(gap['life_expectancy_gap']):.1f} FEWER years.")
    print(f"  3. High-performers achieve better outcomes at lower cost.")
    print(f"  4. If their defense were inadequate, they'd be getting invaded. They're not.")


def get_country_comparison_data() -> list[dict]:
    """
    Return data suitable for tables comparing countries.
    """
    countries = HIGH_PERFORMERS + [USA]
    return [
        {
            "name": c.name,
            "life_expectancy": c.life_expectancy,
            "gdp_per_capita": c.gdp_per_capita,
            "defense_per_capita": c.defense_per_capita,
            "health_per_capita": c.health_per_capita,
            "education_per_capita": c.education_per_capita,
            "rd_per_capita": c.rd_per_capita,
            "defense_pct_gdp": c.defense_pct_gdp,
            "health_pct_gdp": c.health_pct_gdp,
        }
        for c in countries
    ]


if __name__ == "__main__":
    print_comparison()
