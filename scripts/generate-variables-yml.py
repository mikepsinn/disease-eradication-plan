#!/usr/bin/env python3
# type: ignore
"""
Generate _variables.yml and academic outputs from parameters.py
================================================================

Reads all numeric constants from dih_models/parameters.py and generates:
1. _variables.yml - Quarto-compatible variables with tooltips
2. knowledge/appendix/parameters-and-calculations.qmd - Academic reference with LaTeX
3. knowledge/references.json - Structured JSON from references.qmd
4. references.bib - BibTeX export for LaTeX submissions
5. (Optional) Inject citations into economics.qmd

Usage:
    python scripts/generate-variables-yml.py [options]

Options:
    --cite-mode=MODE      Citation handling mode:
                          - none: No inline citations (default)
                          - inline: Add [@key] after peer-reviewed parameters
                          - separate: Export {param}_cite variables
                          - both: Both inline AND separate variables

    --inject-citations    Add [@citation] tags to economics.qmd variables
                          (legacy option, use --cite-mode=inline instead)

Examples:
    # Default: no citations
    python scripts/generate-variables-yml.py

    # Inline citations for peer-reviewed sources
    python scripts/generate-variables-yml.py --cite-mode=inline

    # Separate citation variables (flexible usage)
    python scripts/generate-variables-yml.py --cite-mode=separate

    # Both inline AND separate (maximum flexibility)
    python scripts/generate-variables-yml.py --cite-mode=both

Output:
    _variables.yml in project root
    knowledge/appendix/parameters-and-calculations.qmd
    references.bib in project root

The generated files enable academic rigor with zero manual maintenance.
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Union

import yaml

# Add scripts directory to path for local imports
_scripts_dir = Path(__file__).parent.absolute()
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

# Import the references JSON generator
from generate_references_json import generate_references_json
try:
    # Optional uncertainty integration
    from dih_models.uncertainty import simulate, one_at_a_time_sensitivity, tornado_deltas, regression_sensitivity, Outcome
except Exception:
    simulate = None  # type: ignore
    one_at_a_time_sensitivity = None  # type: ignore
    tornado_deltas = None  # type: ignore
    regression_sensitivity = None  # type: ignore
    Outcome = None  # type: ignore


def parse_parameters_file(parameters_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Parse parameters.py and extract all numeric constants with metadata.

    Imports the actual module to get Parameter instances with their metadata.

    Returns a dict mapping variable names to their metadata:
    {
        'PARAM_NAME': {
            'value': Parameter(123.45, ...) or 123.45,
            'line_num': 42,
            'comment': '# Source: https://...'
        }
    }
    """
    parameters = {}

    # Import the parameters module to get actual Parameter instances
    import importlib.util

    # Add dih_models directory to sys.path so it can find reference_ids
    dih_models_dir = str(parameters_path.parent)
    if dih_models_dir not in sys.path:
        sys.path.insert(0, dih_models_dir)

    spec = importlib.util.spec_from_file_location("parameters", parameters_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {parameters_path}")
    params_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params_module)

    # Also parse the file for line numbers and comments
    with open(parameters_path, encoding="utf-8") as f:
        lines = f.readlines()

    line_info = {}
    for i, line in enumerate(lines, 1):
        # Skip comments and empty lines
        if line.strip().startswith("#") or not line.strip():
            continue

        # Look for variable assignments
        match = re.match(r"^([A-Z_][A-Z0-9_]*)\s*=\s*", line.strip())
        if match:
            var_name = match.group(1)
            # Extract comment if present
            comment = ""
            if "#" in line:
                comment = line.split("#", 1)[1].strip()
            line_info[var_name] = {"line_num": i, "comment": comment}

    # Extract all uppercase constants from the module
    for name in dir(params_module):
        if name.isupper():  # Only uppercase constants
            value = getattr(params_module, name)

            # Only process numeric values (including Parameter instances)
            if isinstance(value, (int, float)):
                info = line_info.get(name, {"line_num": 0, "comment": ""})
                parameters[name] = {
                    "value": value,  # This will be Parameter instance if defined as such
                    "line_num": info["line_num"],
                    "comment": info["comment"],
                }

    return parameters


def smart_title_case(param_name: str) -> str:
    """
    Convert parameter name to title case, preserving common acronyms.

    Examples:
        DFDA_ACTIVE_TRIALS → "dFDA Active Trials"
        ROI_DISCOUNT_1PCT → "ROI Discount 1%"
        QALYS_FROM_FASTER_ACCESS → "QALYs From Faster Access"
        GDP_GROWTH_BOOST_1PCT → "GDP Growth Boost 1%"
    """
    # Common acronyms to preserve (with proper capitalization)
    ACRONYMS = {
        'DFDA': 'dFDA',  # Decentralized FDA
        'DIH': 'DIH',    # Decentralized Institutes of Health
        'ROI': 'ROI',    # Return on Investment
        'QALY': 'QALY',  # Quality-Adjusted Life Year
        'QALYS': 'QALYs',
        'DALY': 'DALY',  # Disability-Adjusted Life Year
        'DALYS': 'DALYs',
        'NPV': 'NPV',    # Net Present Value
        'OPEX': 'OPEX',  # Operating Expenses
        'CAPEX': 'CAPEX', # Capital Expenses
        'GDP': 'GDP',    # Gross Domestic Product
        'VSL': 'VSL',    # Value of Statistical Life
        'EPA': 'EPA',    # Environmental Protection Agency
        'FDA': 'FDA',    # Food and Drug Administration
        'NIH': 'NIH',    # National Institutes of Health
        'US': 'US',
        'UK': 'UK',
        'EU': 'EU',
        'WHO': 'WHO',
        'UN': 'UN',
        'ICER': 'ICER',  # Incremental Cost-Effectiveness Ratio
        'RD': 'R&D',     # Research & Development
        'CEO': 'CEO',
        'CTO': 'CTO',
        'API': 'API',
        'URL': 'URL',
        'ID': 'ID',
    }

    # Special suffix replacements
    SUFFIX_REPLACEMENTS = {
        'PCT': '%',      # 1PCT → 1%
        'MIN': 'Min',
        'MAX': 'Max',
        'AVG': 'Avg',
        'MEAN': 'Mean',
        'STD': 'Std',
        'ANNUAL': 'Annual',
        'TOTAL': 'Total',
        'GLOBAL': 'Global',
    }

    # Split by underscores
    words = param_name.split('_')

    # Process each word
    result: list[str] = []
    for word in words:
        # Check if it's a known acronym
        if word in ACRONYMS:
            result.append(ACRONYMS[word])
        # Check for suffix replacements
        elif word in SUFFIX_REPLACEMENTS:
            result.append(SUFFIX_REPLACEMENTS[word])
        # Check for numeric patterns with PCT suffix (e.g., "1PCT" → "1%")
        elif len(word) > 3 and word.endswith('PCT') and word[:-3].replace('.', '').isdigit():
            result.append(f"{word[:-3]}%")
        # Default: title case
        else:
            result.append(word.capitalize())

    return ' '.join(result)


def format_parameter_value(value: float, unit: str = "") -> str:
    """
    Format a numeric value with appropriate precision, thousand separators, and units.

    Uses 3 significant figures max, removes trailing zeros.

    Args:
        value: The numeric value (may be billions for currency)
        unit: The unit string from the Parameter (e.g., "billions USD/year", "percent", "deaths/year")

    Returns:
        Formatted string with units (e.g., "$50B", "50%", "244,600")
    """
    # Detect currency parameters
    is_currency = "USD" in unit or "usd" in unit or "dollar" in unit.lower()

    # Detect percentage parameters
    is_percentage = "%" in unit or "percent" in unit.lower() or "rate" in unit.lower()

    # Check if value is already in billions, millions, thousands, or in actual dollars
    is_in_billions = "billion" in unit.lower()
    is_in_millions = "million" in unit.lower()
    is_in_thousands = "thousand" in unit.lower()

    # Helper to remove trailing zeros and decimal point
    def clean_number(num_str: str) -> str:
        if "." in num_str:
            num_str = num_str.rstrip("0").rstrip(".")
        return num_str

    # Add currency formatting if applicable (3 significant figures)
    if is_currency:
        # Determine the absolute value for scaling
        abs_val = abs(value)

        if is_in_billions:
            # Value is already in billions
            if abs_val >= 1000:  # Trillions
                scaled = value / 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}T"  # e.g., "$123T" (3 sig figs)
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}T"  # e.g., "$12.3T" (3 sig figs)
                else:
                    formatted = f"${scaled:.2f}T"  # e.g., "$1.23T" (3 sig figs)
            elif abs_val >= 1:  # Billions
                if abs_val >= 100:
                    formatted = f"${value:.0f}B"  # e.g., "$123B" (3 sig figs)
                elif abs_val >= 10:
                    formatted = f"${value:.1f}B"  # e.g., "$12.3B" (3 sig figs)
                else:
                    formatted = f"${value:.2f}B"  # e.g., "$1.23B" (3 sig figs)
            elif abs_val >= 0.001:  # Millions
                scaled = value * 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}M"  # e.g., "$123M"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}M"  # e.g., "$12.3M"
                else:
                    formatted = f"${scaled:.2f}M"  # e.g., "$1.23M"
            else:
                # Less than 1M - convert billions to dollars
                dollar_value = value * 1_000_000_000
                if dollar_value >= 1000:
                    formatted = f"${dollar_value/1000:.1f}K"  # e.g., "$1.2K"
                elif dollar_value >= 10:
                    formatted = f"${dollar_value:.0f}"
                elif dollar_value >= 1:
                    formatted = f"${dollar_value:.2f}"  # e.g., "$1.27"
                elif dollar_value >= 0.10:
                    formatted = f"${dollar_value:.2f}"
                elif dollar_value >= 0.01:
                    formatted = f"${dollar_value:.3f}"
                else:
                    formatted = f"${dollar_value:.4f}"
        elif is_in_millions:
            # Value is already in millions
            if abs_val >= 1000:  # Billions
                scaled = value / 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}B"  # e.g., "$123B" (3 sig figs)
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}B"  # e.g., "$12.3B" (3 sig figs)
                else:
                    formatted = f"${scaled:.2f}B"  # e.g., "$1.23B" (3 sig figs)
            elif abs_val >= 1:  # Millions
                if abs_val >= 100:
                    formatted = f"${value:.0f}M"  # e.g., "$123M" (3 sig figs)
                elif abs_val >= 10:
                    formatted = f"${value:.1f}M"  # e.g., "$12.3M" (3 sig figs)
                else:
                    formatted = f"${value:.2f}M"  # e.g., "$1.23M" (3 sig figs)
            elif abs_val >= 0.001:  # Thousands
                scaled = value * 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}K"  # e.g., "$123K"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}K"  # e.g., "$12.3K"
                else:
                    formatted = f"${scaled:.2f}K"  # e.g., "$1.23K"
            else:
                # Less than 1K - convert millions to dollars
                dollar_value = value * 1_000_000
                if dollar_value >= 10:
                    formatted = f"${dollar_value:.0f}"
                elif dollar_value >= 1:
                    formatted = f"${dollar_value:.2f}"  # e.g., "$1.27"
                elif dollar_value >= 0.10:
                    formatted = f"${dollar_value:.2f}"
                elif dollar_value >= 0.01:
                    formatted = f"${dollar_value:.3f}"
                else:
                    formatted = f"${dollar_value:.4f}"
        elif is_in_thousands:
            # Value is already in thousands
            if abs_val >= 1000000:  # Billions
                scaled = value / 1000000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}B"  # e.g., "$123B" (3 sig figs)
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}B"  # e.g., "$12.3B" (3 sig figs)
                else:
                    formatted = f"${scaled:.2f}B"  # e.g., "$1.23B" (3 sig figs)
            elif abs_val >= 1000:  # Millions
                scaled = value / 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}M"  # e.g., "$123M"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}M"  # e.g., "$12.3M"
                else:
                    formatted = f"${scaled:.2f}M"  # e.g., "$1.23M"
            elif abs_val >= 1:  # Thousands
                if abs_val >= 100:
                    formatted = f"${value:.0f}K"  # e.g., "$123K" (3 sig figs)
                elif abs_val >= 10:
                    formatted = f"${value:.1f}K"  # e.g., "$12.3K" (3 sig figs)
                else:
                    formatted = f"${value:.2f}K"  # e.g., "$1.23K" (3 sig figs)
            else:
                # Less than 1K - convert thousands to dollars
                dollar_value = value * 1000
                if dollar_value >= 10:
                    formatted = f"${dollar_value:.0f}"
                elif dollar_value >= 1:
                    formatted = f"${dollar_value:.2f}"  # e.g., "$1.27"
                elif dollar_value >= 0.10:
                    formatted = f"${dollar_value:.2f}"
                elif dollar_value >= 0.01:
                    formatted = f"${dollar_value:.3f}"
                else:
                    formatted = f"${dollar_value:.4f}"
        else:
            # Value is in actual dollars, convert to appropriate scale
            if abs_val >= 1e15:  # Quadrillions
                scaled = value / 1e15
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f} quadrillion"  # e.g., "$123 quadrillion"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f} quadrillion"  # e.g., "$12.3 quadrillion"
                else:
                    formatted = f"${scaled:.2f} quadrillion"  # e.g., "$1.23 quadrillion"
            elif abs_val >= 1e12:  # Trillions
                scaled = value / 1e12
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}T"  # e.g., "$123T"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}T"  # e.g., "$12.3T"
                else:
                    formatted = f"${scaled:.2f}T"  # e.g., "$1.23T"
            elif abs_val >= 1e9:  # Billions
                scaled = value / 1e9
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}B"  # e.g., "$123B"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}B"  # e.g., "$12.3B"
                else:
                    formatted = f"${scaled:.2f}B"  # e.g., "$1.23B"
            elif abs_val >= 1e6:  # Millions
                scaled = value / 1e6
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}M"  # e.g., "$123M"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}M"  # e.g., "$12.3M"
                else:
                    formatted = f"${scaled:.2f}M"  # e.g., "$1.23M"
            elif abs_val >= 1e3:  # Thousands
                scaled = value / 1e3
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}K"  # e.g., "$123K"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}K"  # e.g., "$12.3K"
                else:
                    formatted = f"${scaled:.2f}K"  # e.g., "$1.23K"
            elif abs_val >= 10:
                # $10 to $999 - no decimals needed
                formatted = f"${value:.0f}"
            elif abs_val >= 1:
                # $1 to $9.99 - show cents for precision
                formatted = f"${value:.2f}"
            else:
                # Less than $1 - show cents with appropriate precision (3 sig figs)
                if abs_val >= 0.10:
                    formatted = f"${value:.2f}"  # e.g., "$0.13"
                elif abs_val >= 0.01:
                    formatted = f"${value:.3f}"  # e.g., "$0.013"
                else:
                    formatted = f"${value:.4f}"  # e.g., "$0.0013"

        # Clean up trailing .0 (e.g., "$50.0B" → "$50B")
        return formatted.replace(".0T", "T").replace(".0B", "B").replace(".0M", "M").replace(".0K", "K")

    # Format plain numbers with appropriate precision
    # Auto-scale large numbers to M/B/K (like we do for currency)
    abs_val = abs(value)

    if abs_val >= 1e15:  # Quadrillions
        scaled = value / 1e15
        if abs(scaled) >= 100:
            formatted_num = f"{scaled:.0f} quadrillion"
        elif abs(scaled) >= 10:
            formatted_num = f"{scaled:.1f} quadrillion"
        else:
            formatted_num = f"{scaled:.2f} quadrillion"
    elif abs_val >= 1e12:  # Trillions
        scaled = value / 1e12
        if abs(scaled) >= 100:
            formatted_num = f"{scaled:.0f}T"
        elif abs(scaled) >= 10:
            formatted_num = f"{scaled:.1f}T"
        else:
            formatted_num = f"{scaled:.2f}T"
    elif abs_val >= 1e9:  # Billions
        scaled = value / 1e9
        if abs(scaled) >= 100:
            formatted_num = f"{scaled:.0f}B"
        elif abs(scaled) >= 10:
            formatted_num = f"{scaled:.1f}B"
        else:
            formatted_num = f"{scaled:.2f}B"
    elif abs_val >= 1e6:  # Millions
        scaled = value / 1e6
        if abs(scaled) >= 100:
            formatted_num = f"{scaled:.0f}M"
        elif abs(scaled) >= 10:
            formatted_num = f"{scaled:.1f}M"
        else:
            formatted_num = f"{scaled:.2f}M"
    elif abs_val >= 100_000:  # 100K+ (for readability, scale to K)
        scaled = value / 1e3
        if abs(scaled) >= 100:
            formatted_num = f"{scaled:.0f}K"
        elif abs(scaled) >= 10:
            formatted_num = f"{scaled:.1f}K"
        else:
            formatted_num = f"{scaled:.2f}K"
    elif value == int(value):
        # Integer value - no decimals needed, use comma separators
        formatted_num = f"{int(value):,}"
    elif abs_val >= 1000:
        # Large numbers (1K-99K): use comma separators
        formatted_num = f"{value:,.0f}"
    elif abs_val >= 1:
        # Medium numbers: up to 3 sig figs, remove trailing zeros
        if value >= 100:
            formatted_num = f"{value:,.0f}"  # No decimals for 100+
        elif value >= 10:
            formatted_num = clean_number(f"{value:,.1f}")  # 1 decimal for 10-99
        else:
            formatted_num = clean_number(f"{value:,.2f}")  # 2 decimals for 1-9
    else:
        # Small numbers: 3 sig figs
        formatted_num = clean_number(f"{value:.3g}")

    # Clean trailing zeros from scaled numbers
    formatted_num = formatted_num.replace(".0T", "T").replace(".0B", "B").replace(".0M", "M").replace(".0K", "K")

    # Add percentage formatting if applicable
    if is_percentage:
        # Convert ratio to percentage (e.g., 2.718 → 272%)
        pct_value = value * 100

        # Format with appropriate precision
        if abs(pct_value) >= 100:
            pct_formatted = f"{pct_value:.0f}"  # e.g., "272%"
        elif abs(pct_value) >= 10:
            pct_formatted = clean_number(f"{pct_value:.1f}")  # e.g., "27.2%"
        elif abs(pct_value) >= 1:
            pct_formatted = clean_number(f"{pct_value:.2f}")  # e.g., "2.72%"
        else:
            pct_formatted = clean_number(f"{pct_value:.3g}")  # e.g., "0.272%"

        return f"{pct_formatted}%"

    # Default: just the formatted number
    return formatted_num


def convert_qmd_to_html(path: str) -> str:
    """
    Remove .qmd extension from paths for format-agnostic links.
    Quarto will resolve extensionless paths appropriately for each output format:
    - HTML: resolves to .html files
    - PDF: resolves to internal PDF references
    - EPUB: resolves to internal EPUB references
    
    Args:
        path: Path that may contain .qmd extension
        
    Returns:
        Path with .qmd extension removed (format-agnostic)
    """
    if path.endswith('.qmd'):
        return path[:-4]  # Remove .qmd extension
    elif '.qmd#' in path:
        # Handle paths with fragments like "file.qmd#section"
        return path.replace('.qmd#', '#')  # Remove .qmd, keep #
    return path


def generate_html_with_tooltip(param_name: str, value: Union[float, int, Any], comment: str = "", include_citation: bool = False) -> str:
    """
    Generate HTML link with tooltip for a parameter.

    Args:
        param_name: The parameter name (e.g., 'GLOBAL_ANNUAL_CONFLICT_DEATHS')
        value: The numeric value (may be Parameter instance with metadata)
        comment: Optional comment from parameters.py
        include_citation: If True, append Quarto citation [@key] for external sources

    Returns:
        HTML string with formatted value, clickable link, and tooltip
    """
    # Check for display_value override (NEW v2.0)
    if hasattr(value, "display_value") and value.display_value:
        formatted_value = value.display_value
    else:
        # Extract unit if available
        unit = ""
        if hasattr(value, "unit") and value.unit:
            unit = value.unit
        formatted_value = format_parameter_value(value, unit)

    # Check if value is a Parameter instance with source metadata
    has_source = hasattr(value, "source_ref") and value.source_ref

    # Handle both enum and string source_type (backwards compatibility)
    source_type_str = ""
    if hasattr(value, "source_type"):
        source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)

    is_definition = source_type_str == "definition"

    if has_source:
        # Convert ReferenceID enum to string value
        source_ref_value = value.source_ref
        if hasattr(source_ref_value, 'value'):
            # It's an enum, get the actual string value
            source_ref_value = source_ref_value.value
        else:
            # Already a string
            source_ref_value = str(source_ref_value)

        # Determine link destination based on source type
        if source_type_str == "external":
            # Link to citation in references.html (full URL)
            href = f"https://warondisease.org/knowledge/references.html#{source_ref_value}"
            link_text = "View source"
        else:
            # Link to calculation/methodology page (ensure absolute path)
            if not source_ref_value.startswith("/"):
                source_ref_value = f"/{source_ref_value}"
            # Convert .qmd to .html for rendered output
            href = convert_qmd_to_html(source_ref_value)
            link_text = "View calculation"

        # Build tooltip from Parameter metadata with credibility indicators
        tooltip_parts = []
        if hasattr(value, "description") and value.description:
            tooltip_parts.append(value.description)

        # Add confidence level with emoji indicators
        if hasattr(value, "confidence") and value.confidence:
            confidence_indicators = {
                "high": "✓ High confidence",
                "medium": "~ Medium confidence",
                "low": "? Low confidence",
                "estimated": "≈ Estimated",
            }
            tooltip_parts.append(confidence_indicators.get(value.confidence, value.confidence))

        # Show if peer-reviewed (prestigious!)
        if hasattr(value, "peer_reviewed") and value.peer_reviewed:
            tooltip_parts.append("📊 Peer-reviewed")

        # Show if conservative estimate
        if hasattr(value, "conservative") and value.conservative:
            tooltip_parts.append("Conservative estimate")

        # Show sensitivity/uncertainty range
        if hasattr(value, "sensitivity") and value.sensitivity:
            sensitivity_str = format_parameter_value(value.sensitivity, unit)
            tooltip_parts.append(f"±{sensitivity_str}")

        # Show NEW uncertainty metadata (v2.0)
        if hasattr(value, "confidence_interval") and value.confidence_interval:
            low, high = value.confidence_interval
            low_str = format_parameter_value(low, unit)
            high_str = format_parameter_value(high, unit)
            tooltip_parts.append(f"95% CI: [{low_str}, {high_str}]")

        if hasattr(value, "distribution") and value.distribution:
            dist_name = value.distribution.value if hasattr(value.distribution, "value") else str(value.distribution)
            dist_str = f"Dist: {dist_name.title()}"
            if hasattr(value, "std_error") and value.std_error:
                se_str = format_parameter_value(value.std_error, unit)
                dist_str += f" (SE: {se_str})"
            tooltip_parts.append(dist_str)

        # Show last updated date
        if hasattr(value, "last_updated") and value.last_updated:
            tooltip_parts.append(f"Updated: {value.last_updated}")

        if hasattr(value, "formula") and value.formula:
            tooltip_parts.append(f"Formula: {value.formula}")
        if hasattr(value, "unit") and value.unit:
            tooltip_parts.append(f"Unit: {value.unit}")
        tooltip_parts.append(f"Click to {link_text.lower()}")

        tooltip = " | ".join(tooltip_parts)

        # Build data attributes for CSS/JS customization
        data_attrs = f'data-source-ref="{source_ref_value}" data-source-type="{source_type_str}"'
        if hasattr(value, "peer_reviewed") and value.peer_reviewed:
            data_attrs += ' data-peer-reviewed="true"'
        if hasattr(value, "confidence") and value.confidence:
            data_attrs += f' data-confidence="{value.confidence}"'

        # Generate clickable link with optional inline citation
        html = f'<a href="{href}" class="parameter-link" {data_attrs} title="{tooltip}">{formatted_value}</a>'

        # Add Quarto citation inline for external peer-reviewed sources (if requested)
        if include_citation and source_type_str == "external":
            if hasattr(value, "peer_reviewed") and value.peer_reviewed:
                html += f' [@{source_ref_value}]'
    elif is_definition:
        # Core definition: show value with tooltip but no link
        tooltip_parts = []
        if hasattr(value, "description") and value.description:
            tooltip_parts.append(value.description)
        if hasattr(value, "unit") and value.unit:
            tooltip_parts.append(f"Unit: {value.unit}")
        tooltip_parts.append("Core definition")

        tooltip = " | ".join(tooltip_parts)

        html = f'<span class="parameter-definition" title="{tooltip}">{formatted_value}</span>'
    else:
        # Fallback: no source metadata, use span with basic tooltip
        tooltip_parts = [f"parameters.{param_name}"]
        if comment:
            tooltip_parts.append(comment)
        tooltip = " - ".join(tooltip_parts)

        html = f'<span class="parameter-link" title="{tooltip}">{formatted_value}</span>'

    return html


def generate_variables_yml(parameters: Dict[str, Dict[str, Any]], output_path: Path, citation_mode: str = "none"):
    """
    Generate _variables.yml file from parameters.

    Creates YAML with lowercase variable names mapped to formatted HTML values.
    Also exports LaTeX equations as {param_name}_latex variables.

    Args:
        parameters: Dict of parameter metadata
        output_path: Path to write _variables.yml
        citation_mode: Citation handling mode:
            - "none": No inline citations (default)
            - "inline": Include [@key] after external peer-reviewed parameters
            - "separate": Export citation keys as {param_name}_cite variables
            - "both": Both inline AND separate variables
    """
    variables = {}
    citation_count = 0

    # Sort parameters by name for consistent output
    for param_name in sorted(parameters.keys()):
        param_data = parameters[param_name]
        value = param_data["value"]
        comment = param_data["comment"]

        # Use lowercase name for Quarto variables (convention)
        var_name = param_name.lower()

        # Generate formatted HTML with tooltip
        include_inline_citation = citation_mode in ("inline", "both")
        html_value = generate_html_with_tooltip(param_name, value, comment, include_citation=include_inline_citation)

        variables[var_name] = html_value

        # Export citation key separately for external sources (if mode enabled)
        if citation_mode in ("separate", "both"):
            if hasattr(value, "source_type") and hasattr(value, "source_ref"):
                source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
                if source_type_str == "external" and value.source_ref:
                    # Sanitize citation key for BibTeX compatibility
                    sanitized_ref = sanitize_bibtex_key(value.source_ref)
                    variables[f"{var_name}_cite"] = f"@{sanitized_ref}"
                    citation_count += 1

        # Export LaTeX equation if available (with $$ delimiters)
        if hasattr(value, "latex") and value.latex:
            latex_var_name = f"{var_name}_latex"
            # Include $$ delimiters so variable can be used directly
            variables[latex_var_name] = f"$$\n{value.latex}\n$$"

    # Count exports by type BEFORE adding metadata variables
    latex_count = sum(1 for k in variables.keys() if k.endswith("_latex"))
    cite_count = sum(1 for k in variables.keys() if k.endswith("_cite"))
    param_count = len(variables) - latex_count - cite_count

    # Add metadata variables for use in QMD files
    variables["total_parameter_count"] = str(param_count)
    variables["total_latex_equation_count"] = str(latex_count)
    if citation_mode in ("separate", "both"):
        variables["total_citation_count"] = str(cite_count)

    # Write YAML file
    with open(output_path, "w", encoding="utf-8") as f:
        # Add header comment
        f.write("# AUTO-GENERATED FILE - DO NOT EDIT\n")
        f.write("# Generated from dih_models/parameters.py\n")
        f.write("# Run: python tools/generate-variables-yml.py\n")
        f.write("#\n")
        f.write("# Use in QMD files with: {{< var param_name >}}\n")
        if citation_mode in ("separate", "both"):
            f.write("# Citations available as: {{< var param_name_cite >}}\n")
        f.write("#\n")
        f.write("# Metadata variables:\n")
        f.write("#   {{< var total_parameter_count >}} - Number of parameters\n")
        f.write("#   {{< var total_latex_equation_count >}} - Number of LaTeX equations\n")
        if citation_mode in ("separate", "both"):
            f.write("#   {{< var total_citation_count >}} - Number of citations\n")
        f.write("#\n\n")

        # Write variables with proper quoting for HTML
        yaml.dump(variables, f, default_flow_style=False, allow_unicode=True, sort_keys=False, default_style='"')

    print(f"[OK] Generated {output_path}")
    print(f"     {param_count} parameters exported")
    print(f"     {latex_count} LaTeX equations exported")
    if citation_mode in ("separate", "both"):
        print(f"     {cite_count} citation keys exported")
    if citation_mode in ("inline", "both"):
        print(f"     Citation mode: inline [@key] for peer-reviewed sources")
    print("\nUsage in QMD files:")
    print(f"  {{{{< var {list(variables.keys())[0]} >}}}}")
    if cite_count > 0:
        # Find first parameter with citation
        cite_var = next((k for k in variables.keys() if k.endswith("_cite")), None)
        if cite_var:
            base_var = cite_var[:-5]  # Remove "_cite"
            print(f"  {{{{< var {base_var} >}}}} {{{{< var {cite_var} >}}}}")


def generate_parameters_qmd(parameters: Dict[str, Dict[str, Any]], output_path: Path, available_refs: set = None):
    """
    Generate comprehensive parameters-and-calculations.qmd appendix.

    Creates an academic reference page with:
    - All parameters organized by type (external/calculated)
    - LaTeX equations where available
    - Citations and source links
    - Confidence indicators and metadata

    Args:
        parameters: Dict of parameter metadata
        output_path: Path to write the QMD file
        available_refs: Set of valid reference IDs from references.qmd (optional, for detecting reference links)
    """
    # Categorize parameters
    external_params = []
    calculated_params = []
    definition_params = []

    for param_name in sorted(parameters.keys()):
        param_data = parameters[param_name]
        value = param_data["value"]

        if hasattr(value, "source_type"):
            # Handle both enum and string source_type
            source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)

            if source_type_str == "external":
                external_params.append((param_name, param_data))
            elif source_type_str == "calculated":
                calculated_params.append((param_name, param_data))
            elif source_type_str == "definition":
                definition_params.append((param_name, param_data))
        else:
            # No source_type - treat as definition
            definition_params.append((param_name, param_data))

    # Generate QMD content
    content = []
    content.append("---")
    content.append('title: "Parameters and Calculations Reference"')
    content.append('subtitle: "Comprehensive Documentation of Economic Model Variables"')
    content.append("format:")
    content.append("  html:")
    content.append("    toc: true")
    content.append("    toc-depth: 3")
    content.append("    number-sections: true")
    content.append("    code-fold: true")
    content.append("---")
    content.append("")
    content.append("## Overview")
    content.append("")
    content.append(
        "This appendix provides comprehensive documentation of all parameters and calculations used in the economic analysis of the 1% Treaty and Decentralized FDA."
    )
    content.append("")
    content.append(f"**Total parameters**: {len(parameters)}")
    content.append("")
    content.append(f"- External sources (peer-reviewed): {len(external_params)}")
    content.append(f"- Calculated values: {len(calculated_params)}")
    content.append(f"- Core definitions: {len(definition_params)}")
    content.append("")

    # External parameters section
    if external_params:
        content.append("## External Data Sources {#sec-external}")
        content.append("")
        content.append(
            "Parameters sourced from peer-reviewed publications, institutional databases, and authoritative reports."
        )
        content.append("")

        for param_name, param_data in external_params:
            value = param_data["value"]

            # Generate display title with priority chain: display_name → smart_title_case() → .title()
            if hasattr(value, "display_name") and value.display_name:
                display_title = value.display_name
            else:
                display_title = smart_title_case(param_name)

            # Start callout box for external source
            content.append("::: {.callout-tip icon=false collapse=false}")
            content.append(f"### {display_title} {{#sec-{param_name.lower()}}}")
            content.append("")

            # Value
            unit = getattr(value, "unit", "")
            formatted = format_parameter_value(value, unit)
            content.append(f"**Value**: {formatted}")
            content.append("")

            # Description
            if hasattr(value, "description") and value.description:
                content.append(f"{value.description}")
                content.append("")

            # Source citation
            if hasattr(value, "source_ref") and value.source_ref:
                source_ref = value.source_ref
                # Convert ReferenceID enum to string value for URL
                source_ref_str = source_ref.value if hasattr(source_ref, 'value') else str(source_ref)
                # Use the reference ID value for display (not the enum representation)
                display_ref = source_ref_str
                content.append(f"**Source**: [{display_ref}](https://warondisease.org/knowledge/references.html#{source_ref_str})")
                content.append("")

            # Confidence and metadata - cleaner formatting
            metadata = []
            if hasattr(value, "confidence") and value.confidence:
                confidence_labels = {
                    "high": "✓ High confidence",
                    "medium": "~ Medium confidence",
                    "low": "? Low confidence",
                    "estimated": "≈ Estimated",
                }
                metadata.append(confidence_labels.get(value.confidence, value.confidence))

            if hasattr(value, "peer_reviewed") and value.peer_reviewed:
                metadata.append("📊 Peer-reviewed")

            # Only show last_updated if it's not None/empty
            if hasattr(value, "last_updated") and value.last_updated:
                metadata.append(f"Updated {value.last_updated}")

            if metadata:
                content.append("*" + " • ".join(metadata) + "*")
                content.append("")

            content.append(":::")
            content.append("")

    # Calculated parameters section
    if calculated_params:
        content.append("## Calculated Values {#sec-calculated}")
        content.append("")
        content.append("Parameters derived from mathematical formulas and economic models.")
        content.append("")

        for param_name, param_data in calculated_params:
            value = param_data["value"]

            # Generate display title with priority chain: display_name → smart_title_case() → .title()
            if hasattr(value, "display_name") and value.display_name:
                display_title = value.display_name
            else:
                display_title = smart_title_case(param_name)

            # Start callout box for calculated value
            content.append("::: {.callout-note icon=false collapse=false}")
            content.append(f"### {display_title} {{#sec-{param_name.lower()}}}")
            content.append("")

            # Value
            unit = getattr(value, "unit", "")
            formatted = format_parameter_value(value, unit)
            content.append(f"**Value**: {formatted}")
            content.append("")

            # Description
            if hasattr(value, "description") and value.description:
                content.append(f"{value.description}")
                content.append("")

            # LaTeX equation - prominently displayed
            if hasattr(value, "latex") and value.latex:
                content.append("$$")
                content.append(value.latex)
                content.append("$$")
                content.append("")
            elif hasattr(value, "formula") and value.formula:
                content.append(f"*Formula*: `{value.formula}`")
                content.append("")

            # Source reference (calculation methodology)
            if hasattr(value, "source_ref") and value.source_ref:
                source_ref = value.source_ref
                
                # Convert ReferenceID enum to string value (if needed)
                if hasattr(source_ref, 'value'):
                    source_ref = source_ref.value
                else:
                    source_ref = str(source_ref)

                # Detect if this is an intra-document anchor (no path separators, no file extension)
                is_anchor = "/" not in source_ref and ".qmd" not in source_ref and ".md" not in source_ref
                
                # Check if this anchor-like value is actually a reference ID from references.qmd
                is_reference_id = False
                if is_anchor and available_refs is not None:
                    is_reference_id = source_ref in available_refs

                # Friendly labels for common methodology references
                methodology_labels = {
                    "cure-bounty-estimates": "Cure Bounty Estimation Model",
                    "disease-related-caregiving-estimate": "Disease-Related Caregiving Analysis",
                    "calculated": "Direct Calculation",
                    "sipri-2024-spending": "SIPRI Military Spending Database",
                    "book-word-count": "Book Word Count Analysis",
                }

                if is_reference_id:
                    # This is a reference ID - link to references (extensionless for format-agnostic links)
                    # Quarto will resolve to references.html (HTML), references.pdf (PDF), or references.epub (EPUB)
                    link_target = f"../references#{source_ref}"
                    link_text = methodology_labels.get(source_ref, source_ref)
                elif is_anchor:
                    # Intra-document anchor - add # prefix
                    link_target = f"#{source_ref}"
                    link_text = methodology_labels.get(source_ref, source_ref)
                else:
                    # File path - convert to relative path
                    if source_ref.startswith("/"):
                        source_ref = source_ref.lstrip("/")

                    if source_ref.startswith("knowledge/"):
                        # Remove 'knowledge/' prefix and add '../' to go up from appendix/
                        source_ref = "../" + source_ref[len("knowledge/") :]

                    # Convert .qmd to .html for rendered output
                    link_target = convert_qmd_to_html(source_ref)
                    # Use the converted path for link text too (shows .html instead of .qmd)
                    link_text = link_target

                content.append(f"**Methodology**: [{link_text}]({link_target})")
                content.append("")

            # Confidence and notes
            metadata = []
            if hasattr(value, "confidence") and value.confidence:
                confidence_labels = {
                    "high": "✓ High confidence",
                    "medium": "~ Medium confidence",
                    "low": "? Low confidence",
                    "estimated": "≈ Estimated",
                }
                metadata.append(confidence_labels.get(value.confidence, value.confidence))

            if hasattr(value, "conservative") and value.conservative:
                metadata.append("⚖️ Conservative estimate")

            if metadata:
                content.append("*" + " • ".join(metadata) + "*")
                content.append("")

            # Add uncertainty visualization if tornado/sensitivity data exists
            project_root = output_path.parent.parent.parent  # Go up from knowledge/appendix/ to project root
            tornado_json = project_root / "_analysis" / f"tornado_{param_name}.json"
            tornado_qmd = project_root / "knowledge" / "figures" / f"tornado-{param_name.lower()}.qmd"
            sensitivity_qmd = project_root / "knowledge" / "figures" / f"sensitivity-table-{param_name.lower()}.qmd"

            if tornado_qmd.exists():
                content.append("#### Sensitivity Analysis")
                content.append("")
                content.append(f"{{{{< include ../figures/tornado-{param_name.lower()}.qmd >}}}}")
                content.append("")

                if sensitivity_qmd.exists():
                    content.append(f"{{{{< include ../figures/sensitivity-table-{param_name.lower()}.qmd >}}}}")
                    content.append("")

            content.append(":::")
            content.append("")

    # Core definitions section
    if definition_params:
        content.append("## Core Definitions {#sec-definitions}")
        content.append("")
        content.append("Fundamental parameters and constants used throughout the analysis.")
        content.append("")

        for param_name, param_data in definition_params:
            value = param_data["value"]

            # Generate display title with priority chain: display_name → smart_title_case() → .title()
            if hasattr(value, "display_name") and value.display_name:
                display_title = value.display_name
            else:
                display_title = smart_title_case(param_name)

            # Start callout box for definition
            content.append("::: {.callout-warning icon=false collapse=false}")
            content.append(f"### {display_title} {{#sec-{param_name.lower()}}}")
            content.append("")

            # Value
            unit = getattr(value, "unit", "")
            formatted = format_parameter_value(value, unit)
            content.append(f"**Value**: {formatted}")
            content.append("")

            # Description
            if hasattr(value, "description") and value.description:
                content.append(f"{value.description}")
                content.append("")

            content.append("*Core definition*")
            content.append("")

            content.append(":::")
            content.append("")

    # Write file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"[OK] Generated {output_path}")
    print(f"     {len(external_params)} external parameters")
    print(f"     {len(calculated_params)} calculated parameters")
    print(f"     {len(definition_params)} core definitions")


def parse_references_qmd_detailed(references_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Parse knowledge/references.qmd and extract full citation metadata.

    Returns a dict mapping reference IDs to citation data:
    {
        'reference-id': {
            'id': 'reference-id',
            'title': 'The reference title',
            'author': 'Author Name',
            'year': '2024',
            'source': 'Journal/Publisher Name',
            'url': 'https://...',
            'urls': ['https://...', 'https://...'],  # All URLs
            'quote': 'The quoted text',
            'note': 'Additional context',
            'type': 'article'  # article, book, misc, report, etc.
        }
    }
    """
    if not references_path.exists():
        print(f"[WARN] References file not found: {references_path}", file=sys.stderr)
        return {}

    with open(references_path, encoding="utf-8") as f:
        lines = f.readlines()

    references = {}
    current_ref = None
    current_id = None
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        # Match anchor tags: <a id="reference-id"></a>
        anchor_match = re.match(r'<a\s+id="([^"]+)"\s*></a>', line)
        if anchor_match:
            ref_id = anchor_match.group(1)

            # Skip internal document references (contain / or .qmd)
            if '/' in ref_id or '.qmd' in ref_id:
                i += 1
                continue

            # Save PREVIOUS reference before starting new one
            if current_id and current_ref:
                # Determine entry type based on source
                source_lower = current_ref['source'].lower()
                if any(word in source_lower for word in ['journal', 'nature', 'science', 'lancet']):
                    current_ref['type'] = 'article'
                elif any(word in source_lower for word in ['congress.gov', 'law', 'act', 'bill']):
                    current_ref['type'] = 'legislation'
                elif any(word in source_lower for word in ['cdc', 'who', 'gao', 'fda', 'nih']):
                    current_ref['type'] = 'report'
                elif any(word in source_lower for word in ['book', 'press', 'publisher']):
                    current_ref['type'] = 'book'
                elif 'university' in source_lower or 'project' in source_lower:
                    current_ref['type'] = 'techreport'

                references[current_id] = current_ref

            # Start new reference
            current_id = ref_id
            current_ref = {
                'id': ref_id,
                'title': '',
                'author': '',
                'year': '',
                'source': '',
                'url': '',
                'urls': [],
                'quote': '',
                'note': '',
                'type': 'misc'
            }
            i += 1
            continue

        # Match title: - **Title text**
        if current_id and line.startswith('- **') and line.endswith('**'):
            title = line[4:-2].strip()
            current_ref['title'] = title
            i += 1
            continue

        # Match blockquote lines (citation data)
        if current_id and line.strip().startswith('>'):
            quote_line = line.strip()[1:].strip()  # Remove '>' and whitespace

            # Attribution line (starts with em dash): — Source, Year, [Link](URL)
            if quote_line.startswith('—') or quote_line.startswith('--'):
                attribution = quote_line.lstrip('—-').strip()

                # Extract all URLs from markdown links: [text](url)
                url_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
                url_matches = re.findall(url_pattern, attribution)
                for link_text, url in url_matches:
                    current_ref['urls'].append(url)
                    if not current_ref['url']:
                        current_ref['url'] = url

                # Try to extract year (4-digit number)
                year_match = re.search(r'\b(19|20)\d{2}\b', attribution)
                if year_match:
                    current_ref['year'] = year_match.group(0)

                # Extract source/author (text before year or first comma)
                # Remove markdown links for cleaner parsing
                clean_attr = re.sub(url_pattern, r'\1', attribution)

                # Split by | to get individual sources
                sources = clean_attr.split('|')
                if sources:
                    first_source = sources[0].strip()
                    # Source format: "Name, Year, Link" or "Name, Link"
                    parts = [p.strip() for p in first_source.split(',')]
                    if parts:
                        current_ref['source'] = parts[0]
                        # Use source as author if no better info available
                        if not current_ref['author']:
                            current_ref['author'] = parts[0]

                # Store full attribution as note
                current_ref['note'] = clean_attr

            # Regular quote line
            elif quote_line.startswith('"') or 'Alternative title:' in quote_line:
                if current_ref['quote']:
                    current_ref['quote'] += ' '
                current_ref['quote'] += quote_line

            i += 1
            continue

        # Continue to next line
        i += 1

    # Save last reference if exists
    if current_id and current_ref:
        # Determine entry type based on source
        source_lower = current_ref['source'].lower()
        if any(word in source_lower for word in ['journal', 'nature', 'science', 'lancet']):
            current_ref['type'] = 'article'
        elif any(word in source_lower for word in ['congress.gov', 'law', 'act', 'bill']):
            current_ref['type'] = 'legislation'
        elif any(word in source_lower for word in ['cdc', 'who', 'gao', 'fda', 'nih']):
            current_ref['type'] = 'report'
        elif any(word in source_lower for word in ['book', 'press', 'publisher']):
            current_ref['type'] = 'book'
        elif 'university' in source_lower or 'project' in source_lower:
            current_ref['type'] = 'techreport'

        references[current_id] = current_ref

    return references


def parse_references_qmd(references_path: Path) -> set:
    """
    Parse knowledge/references.qmd and extract all reference IDs.

    Returns a set of all anchor IDs (for backward compatibility).
    For detailed citation data, use parse_references_qmd_detailed().

    Example: <a id="166-billion-compounds"></a> -> "166-billion-compounds"
    """
    detailed = parse_references_qmd_detailed(references_path)
    return set(detailed.keys())


def sanitize_bibtex_key(key: str) -> str:
    """
    Sanitize citation key for BibTeX (only alphanumeric, hyphens, underscores).

    Same logic as convert-references-to-bib.py for consistency.
    """
    sanitized = key
    sanitized = sanitized.replace('/', '-')
    sanitized = sanitized.replace('#', '-')
    sanitized = sanitized.replace('.qmd', '')
    sanitized = sanitized.replace('.', '-')
    sanitized = re.sub(r'[^a-zA-Z0-9\-_]', '-', sanitized)
    # Remove multiple consecutive hyphens
    sanitized = re.sub(r'-+', '-', sanitized)
    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')
    return sanitized


def validate_references(parameters: Dict[str, Dict[str, Any]], available_refs: set) -> tuple[list, list]:
    """
    Validate that all external source_refs exist in references.qmd.

    Args:
        parameters: Dict of parameter metadata
        available_refs: Set of reference IDs from references.qmd

    Returns:
        Tuple of (missing_refs, used_refs) where:
        - missing_refs: List of (param_name, source_ref) tuples for missing references
        - used_refs: List of source_refs that are actually used
    """
    missing_refs = []
    used_refs = []

    for param_name, param_data in parameters.items():
        value = param_data["value"]
        if hasattr(value, "source_type"):
            source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
            if source_type_str == "external":
                if hasattr(value, "source_ref") and value.source_ref:
                    source_ref = value.source_ref
                    
                    # Convert ReferenceID enum to string value (if needed)
                    if hasattr(source_ref, 'value'):
                        source_ref_str = source_ref.value
                    else:
                        source_ref_str = str(source_ref)
                    
                    used_refs.append(source_ref_str)

                    # Check if reference exists
                    if source_ref_str not in available_refs:
                        missing_refs.append((param_name, source_ref_str))

    return missing_refs, used_refs


def validate_calculated_parameters(parameters: Dict[str, Dict[str, Any]]) -> list:
    """
    Validate that calculated parameters use formulas instead of hardcoded values.

    Checks if parameters marked as source_type="calculated" actually reference
    other parameters in their definition (not just hardcoded numbers).

    Args:
        parameters: Dict of parameter metadata

    Returns:
        List of (param_name, value) tuples for potentially hardcoded calculated parameters
    """
    suspicious_params = []

    # Exception list: Parameters that are intentionally hardcoded estimates
    # despite being marked as "calculated"
    INTENTIONAL_ESTIMATES = {
        "DFDA_UPFRONT_BUILD",
        "DFDA_SMALL_TRIAL_SIZE",
        "CAMPAIGN_MEDIA_BUDGET_MIN",
        "CAMPAIGN_MEDIA_BUDGET_MAX",
        # Add more as needed
    }

    for param_name, param_data in parameters.items():
        # Skip exception list
        if param_name in INTENTIONAL_ESTIMATES:
            continue

        value = param_data["value"]
        if hasattr(value, "source_type"):
            source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
            if source_type_str == "calculated":
                # Check if the value is just a plain number (not a Parameter calculation)
                # Read the source line to see if it's a simple numeric assignment
                # This is a heuristic - if the numeric value doesn't involve other variables,
                # it's likely hardcoded

                # For now, just check if there's a formula attribute
                # If marked as calculated but no formula/latex, it's suspicious
                has_formula = hasattr(value, "formula") and value.formula
                has_latex = hasattr(value, "latex") and value.latex

                # If it's a Parameter but has neither formula nor latex, flag it
                if not has_formula and not has_latex:
                    suspicious_params.append((param_name, float(value)))

    return suspicious_params


def generate_reference_ids_enum(available_refs: set, output_path: Path):
    """
    Generate dih_models/reference_ids.py with enum of valid reference IDs.

    Creates a Python enum for IDE autocomplete and static type checking.
    Developers can use ReferenceID.CDC_LEADING_CAUSES_DEATH instead of strings.

    Args:
        available_refs: Set of reference IDs from references.qmd
        output_path: Path to write reference_ids.py
    """
    content = []
    content.append("#!/usr/bin/env python3")
    content.append('"""')
    content.append("AUTO-GENERATED FILE - DO NOT EDIT")
    content.append("=" * 70)
    content.append("")
    content.append("Valid reference IDs extracted from knowledge/references.qmd")
    content.append("")
    content.append("Usage in parameters.py:")
    content.append("    from .reference_ids import ReferenceID")
    content.append("")
    content.append("    PARAM = Parameter(")
    content.append("        123.45,")
    content.append('        source_type="external",')
    content.append("        source_ref=ReferenceID.CDC_LEADING_CAUSES_DEATH,")
    content.append('        description="..."')
    content.append("    )")
    content.append("")
    content.append("Benefits:")
    content.append("  - IDE autocomplete shows all valid reference IDs")
    content.append("  - Static type checking catches typos before runtime")
    content.append("  - Refactoring safety when renaming references")
    content.append('"""')
    content.append("")
    content.append("from enum import Enum")
    content.append("")
    content.append("")
    content.append("class ReferenceID(str, Enum):")
    content.append('    """Valid reference IDs from knowledge/references.qmd"""')
    content.append("")

    # Sort reference IDs for consistent output
    sorted_refs = sorted(available_refs)

    # Convert reference IDs to enum member names
    # e.g., "cdc-leading-causes-death" -> "CDC_LEADING_CAUSES_DEATH"
    # e.g., "95-pct-diseases-no-treatment" -> "N95_PCT_DISEASES_NO_TREATMENT"
    for ref_id in sorted_refs:
        # Convert kebab-case to SCREAMING_SNAKE_CASE
        enum_name = ref_id.upper().replace("-", "_")

        # Handle special cases that start with numbers: prefix with 'N' instead of '_'
        # This avoids Python's protected member convention (_var)
        if enum_name[0].isdigit():
            enum_name = f"N{enum_name}"

        content.append(f'    {enum_name} = "{ref_id}"')

    content.append("")

    # Write file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"[OK] Generated {output_path}")
    print(f"     {len(sorted_refs)} reference IDs exported as enum")
    print()
    print("Usage in parameters.py:")
    print("    from .reference_ids import ReferenceID")
    if sorted_refs:
        first_ref = sorted_refs[0].upper().replace("-", "_")
        if first_ref[0].isdigit():
            first_ref = f"N{first_ref}"
        print(f"    source_ref=ReferenceID.{first_ref}")
    print()


def generate_bibtex(parameters: Dict[str, Dict[str, Any]], output_path: Path, available_refs: set = None, references_path: Path = None):
    """
    Generate references.bib BibTeX file from external parameters.

    Extracts unique citations from parameters with source_type="external"
    and creates BibTeX entries using actual citation data from references.qmd.

    Args:
        parameters: Dict of parameter metadata
        output_path: Path to write references.bib
        available_refs: Set of valid reference IDs from references.qmd (optional)
        references_path: Path to references.qmd file for detailed citation data
    """
    # Parse detailed citation data from references.qmd
    citation_data = {}
    if references_path and references_path.exists():
        citation_data = parse_references_qmd_detailed(references_path)

    # Collect unique source_refs from external parameters
    citations = set()
    for param_name, param_data in parameters.items():
        value = param_data["value"]
        if hasattr(value, "source_type"):
            source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
            if source_type_str == "external":
                if hasattr(value, "source_ref") and value.source_ref:
                    # Convert ReferenceID enum to string value
                    source_ref = value.source_ref
                    if hasattr(source_ref, 'value'):
                        # It's an enum, get the actual string value
                        source_ref = source_ref.value
                    else:
                        # It's already a string
                        source_ref = str(source_ref)

                    # Skip internal document references (contain / or .qmd)
                    if '/' in source_ref or '.qmd' in source_ref:
                        continue

                    # Optionally skip missing references
                    if available_refs and source_ref not in available_refs:
                        continue

                    citations.add(source_ref)

    # Generate BibTeX entries
    content = []
    content.append("% AUTO-GENERATED FILE - DO NOT EDIT")
    content.append("% Generated from dih_models/parameters.py and knowledge/references.qmd")
    content.append("")
    content.append("% This file contains BibTeX references for all external data sources")
    content.append("% used in the economic analysis of the 1% Treaty and Decentralized FDA.")
    content.append("")
    content.append("% Extracted from knowledge/references.qmd with author, year, source, and URL data.")
    content.append("% For manual curation or DOI-based enrichment, see references.qmd")
    content.append("")

    entries_with_data = 0
    entries_placeholder = 0

    for citation_key in sorted(citations):
        # Sanitize citation key for BibTeX (remove /, #, etc.)
        sanitized_key = sanitize_bibtex_key(citation_key)

        # Get detailed citation data if available
        ref_data = citation_data.get(citation_key, {})

        if ref_data and ref_data.get('title'):
            # Create proper BibTeX entry with real data
            entry_type = ref_data.get('type', 'misc')
            title = ref_data.get('title', citation_key)
            author = ref_data.get('author', '')
            year = ref_data.get('year', 'n.d.')
            source = ref_data.get('source', '')
            url = ref_data.get('url', '')
            note = ref_data.get('note', '')

            # Build BibTeX entry
            content.append(f"@{entry_type}{{{sanitized_key},")

            # Title (required for all types)
            # Escape special LaTeX characters
            title_escaped = title.replace('&', '\\&').replace('%', '\\%')
            content.append(f"  title = {{{title_escaped}}},")

            # Author/organization
            if author:
                author_escaped = author.replace('&', '\\&')
                if entry_type in ['report', 'techreport', 'legislation']:
                    content.append(f"  institution = {{{author_escaped}}},")
                else:
                    content.append(f"  author = {{{author_escaped}}},")

            # Year
            content.append(f"  year = {{{year}}},")

            # Source/journal/publisher
            if source:
                source_escaped = source.replace('&', '\\&')
                if entry_type == 'article':
                    content.append(f"  journal = {{{source_escaped}}},")
                elif entry_type in ['book', 'report', 'techreport']:
                    content.append(f"  publisher = {{{source_escaped}}},")

            # URL (with proper escaping)
            if url:
                url_escaped = url.replace('&', '\\&').replace('%', '\\%')
                content.append(f"  url = {{{url_escaped}}},")
                content.append(f"  urldate = {{2025-01-20}},")

            # Note (additional context)
            if note:
                note_escaped = note.replace('&', '\\&').replace('%', '\\%')
                # Truncate if too long
                if len(note_escaped) > 200:
                    note_escaped = note_escaped[:197] + "..."
                content.append(f"  note = {{{note_escaped}}},")

            content.append("}")
            content.append("")
            entries_with_data += 1

        else:
            # Fallback: create minimal placeholder entry
            content.append(f"@misc{{{sanitized_key},")
            content.append(f"  title = {{{citation_key}}},")
            content.append(f"  note = {{See https://warondisease.org/knowledge/references.html\\#{citation_key}}},")
            content.append(f"  url = {{https://warondisease.org/knowledge/references.html\\#{citation_key}}},")
            content.append("}")
            content.append("")
            entries_placeholder += 1

    # Write file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"[OK] Generated {output_path}")
    print(f"     {len(citations)} unique citations")
    print(f"     {entries_with_data} with full citation data")
    if entries_placeholder > 0:
        print(f"     {entries_placeholder} placeholder entries (missing data in references.qmd)")


def inject_citations_into_qmd(parameters: Dict[str, Dict[str, Any]], qmd_path: Path):
    """
    Inject [@citation] tags into economics.qmd after variables with external sources.

    Finds {{< var param_name >}} patterns and adds [@source_ref] citations for
    parameters with source_type="external" and peer_reviewed=True.

    This is OPTIONAL and only runs when --inject-citations flag is used.
    """
    if not qmd_path.exists():
        print(f"[WARN] QMD file not found: {qmd_path}")
        return

    # Read file
    with open(qmd_path, encoding="utf-8") as f:
        content = f.read()

    # Build lookup map: param_name (lowercase) -> citation_key
    citation_map = {}
    for param_name, param_data in parameters.items():
        value = param_data["value"]
        if hasattr(value, "source_type"):
            source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
            if source_type_str == "external":
                if hasattr(value, "peer_reviewed") and value.peer_reviewed:
                    if hasattr(value, "source_ref") and value.source_ref:
                        # Use lowercase param name (matches Quarto variable names)
                        citation_map[param_name.lower()] = value.source_ref

    # Pattern to match {{< var param_name >}}
    # We'll inject [@citation] right after if not already present
    def replace_var(match):
        var_name = match.group(1)
        full_match = match.group(0)

        # Check if citation already present after this variable
        # Look ahead to see if [@...] immediately follows
        remaining = content[match.end() :]
        if remaining.lstrip().startswith("[@"):
            return full_match  # Already has citation

        # Check if this variable should have a citation
        if var_name in citation_map:
            citation_key = citation_map[var_name]
            return f"{full_match} [@{citation_key}]"
        else:
            return full_match

    # Replace all variables
    pattern = r"\{\{<\s*var\s+([a-z_][a-z0-9_]*)\s*>\}\}"
    modified_content = re.sub(pattern, replace_var, content)

    # Count changes
    changes = sum(1 for a, b in zip(content, modified_content) if a != b)
    if changes > 0:
        # Write back
        with open(qmd_path, "w", encoding="utf-8") as f:
            f.write(modified_content)

        print(f"[OK] Injected citations into {qmd_path}")
        print(f"     {len(citation_map)} parameters with citations available")
        print(f"     Modified {changes} characters")
    else:
        print("[OK] No citation injection needed (already present or no external params)")


def generate_tornado_chart_qmd(param_name: str, tornado_data: dict, output_dir: Path, param_metadata: dict = None, baseline: float = None, units: str = "") -> Path:
    """
    Generate a tornado chart QMD file for a parameter with uncertainty.
    
    Args:
        param_name: Parameter name (e.g., 'TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT')
        tornado_data: Dict mapping input names to {delta_minus, delta_plus}
        output_dir: Directory to write QMD file (knowledge/figures/)
        param_metadata: Optional parameter metadata for context
        baseline: Baseline value to center chart on (instead of 0)
        units: Units for x-axis label
    
    Returns:
        Path to generated QMD file
    """
    # Get display name for title
    if param_metadata and hasattr(param_metadata.get("value"), "display_name"):
        display_name = param_metadata["value"].display_name
    else:
        display_name = smart_title_case(param_name)
    
    # Sort by absolute impact (largest first)
    sorted_drivers = sorted(
        tornado_data.items(),
        key=lambda x: abs(x[1].get("delta_minus", 0)) + abs(x[1].get("delta_plus", 0)),
        reverse=True
    )
    
    # Generate Python code for tornado chart
    qmd_content = f'''```{{python}}
#| echo: false
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from dih_models.plotting.chart_style import (
    setup_chart_style, add_watermark, clean_spines,
    COLOR_BLACK, COLOR_WHITE, add_png_metadata
)
from dih_models.parameters import format_parameter_value

setup_chart_style()

# Display name for chart title
display_name = "{display_name}"

# Baseline and units
baseline = {baseline if baseline is not None else 0.0}

# Tornado data from sensitivity analysis
drivers = {[driver for driver, _ in sorted_drivers]}
impacts_low = {[data["delta_minus"] for _, data in sorted_drivers]}
impacts_high = {[data["delta_plus"] for _, data in sorted_drivers]}

# Convert deltas to absolute values (baseline + delta)
values_low = [baseline + delta for delta in impacts_low]
values_high = [baseline + delta for delta in impacts_high]

# Create tornado chart (horizontal bars showing swing range)
fig, ax = plt.subplots(figsize=(10, max(6, len(drivers) * 0.8)))

y_pos = np.arange(len(drivers))

# Plot low impact (left side)
for i, (low, high) in enumerate(zip(values_low, values_high)):
    left = min(low, high)
    width_low = baseline - left if left < baseline else 0
    width_high = max(low, high) - baseline if max(low, high) > baseline else 0

    # White bar for range below baseline
    if width_low > 0:
        ax.barh(i, width_low, left=left,
                color=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=2)

    # Black bar for range above baseline
    if width_high > 0:
        ax.barh(i, width_high, left=baseline,
                color=COLOR_BLACK, edgecolor=COLOR_BLACK, linewidth=2)

# Format axis
ax.set_yticks(y_pos)
# Simplified labels (just parameter names)
ax.set_yticklabels([d.replace('_', ' ').title() for d in drivers], fontsize=11)
ax.set_title(f'Sensitivity Analysis: {{display_name}}', fontsize=16, weight='bold', pad=20)

# X-axis label with units
units_label = "{units if units else ""}"
if units_label:
    ax.set_xlabel(f'{{display_name}} ({{units_label}})', fontsize=12)
else:
    ax.set_xlabel(f'{{display_name}}', fontsize=12)

# Add vertical line at baseline
ax.axvline(baseline, color=COLOR_BLACK, linewidth=1, linestyle='--', alpha=0.5)

# Clean spines
clean_spines(ax)

# Add watermark
add_watermark(fig)

# Save PNG (mandatory per design guide)
project_root = Path.cwd()
while project_root.name != 'decentralized-institutes-of-health' and project_root.parent != project_root:
    project_root = project_root.parent

output_path = project_root / 'knowledge' / 'figures' / 'tornado-{param_name.lower()}.png'
plt.savefig(output_path, dpi=200, bbox_inches=None, facecolor=COLOR_WHITE)

add_png_metadata(
    output_path,
    title=f'Sensitivity: {{display_name}}',
    description=f'Tornado diagram showing which input parameters have the largest impact on {{display_name}}'
)

plt.show()
```'''
    
    # Write QMD file
    output_file = output_dir / f'tornado-{param_name.lower()}.qmd'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(qmd_content)
    
    return output_file


def generate_sensitivity_table_qmd(param_name: str, sensitivity_data: dict, output_dir: Path, param_metadata: dict = None) -> Path:
    """
    Generate a sensitivity indices table QMD file for a parameter.
    
    Args:
        param_name: Parameter name
        sensitivity_data: Dict mapping input names to sensitivity coefficients
        output_dir: Directory to write QMD file
        param_metadata: Optional parameter metadata for context
    
    Returns:
        Path to generated QMD file
    """
    # Get display name
    if param_metadata and hasattr(param_metadata.get("value"), "display_name"):
        display_name = param_metadata["value"].display_name
    else:
        display_name = smart_title_case(param_name)
    
    # Sort by absolute sensitivity (largest first)
    sorted_indices = sorted(
        sensitivity_data.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )
    
    # Generate markdown table
    qmd_content = f'''**Sensitivity Indices for {display_name}**

Regression-based sensitivity showing which inputs explain the most variance in the output.

| Input Parameter | Sensitivity Coefficient | Interpretation |
|:----------------|------------------------:|:---------------|
'''
    
    for input_name, coef in sorted_indices:
        display_input = smart_title_case(input_name)
        interpretation = "Strong driver" if abs(coef) > 0.5 else "Moderate influence" if abs(coef) > 0.1 else "Minor effect"
        qmd_content += f'| {display_input} | {coef:.4f} | {interpretation} |\n'
    
    qmd_content += '''
*Interpretation*: Higher absolute values indicate stronger influence. Coefficients show the change in output per unit change in input (standardized).
'''
    
    # Write QMD file
    output_file = output_dir / f'sensitivity-table-{param_name.lower()}.qmd'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(qmd_content)
    
    return output_file


def main():
    # Parse command-line arguments
    inject_citations = "--inject-citations" in sys.argv

    # Citation mode: --cite-mode=inline|separate|both|none
    citation_mode = "separate"  # Default: always generate _cite variables for convenience
    for arg in sys.argv:
        if arg.startswith("--cite-mode="):
            citation_mode = arg.split("=")[1]
            if citation_mode not in ("none", "inline", "separate", "both"):
                print(f"[ERROR] Invalid citation mode: {citation_mode}", file=sys.stderr)
                print("Valid modes: none, inline, separate, both", file=sys.stderr)
                sys.exit(1)

    # Get project root
    project_root = Path(__file__).parent.parent.absolute()

    # Parse references.qmd FIRST (before parameters.py, to avoid circular dependency)
    print("[*] Parsing knowledge/references.qmd...")
    references_path = project_root / "knowledge" / "references.qmd"
    available_refs = parse_references_qmd(references_path)
    print(f"[OK] Found {len(available_refs)} reference entries")
    print()

    # Generate references.json from references.qmd
    print("[*] Generating knowledge/references.json...")
    references_json_path = project_root / "knowledge" / "references.json"
    generate_references_json(references_path, references_json_path)
    print()

    # Generate reference_ids.py enum SECOND (before loading parameters.py which imports it)
    print("[*] Generating dih_models/reference_ids.py...")
    reference_ids_path = project_root / "dih_models" / "reference_ids.py"
    generate_reference_ids_enum(available_refs, reference_ids_path)

    # Parse parameters file THIRD (now reference_ids.py is up to date)
    parameters_path = project_root / "dih_models" / "parameters.py"
    if not parameters_path.exists():
        print(f"[ERROR] Parameters file not found: {parameters_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Parsing {parameters_path}...")
    parameters = parse_parameters_file(parameters_path)
    print(f"[OK] Found {len(parameters)} numeric parameters")
    print()

    # Validate that all external source_refs exist in references.qmd
    print("[*] Validating external source references...")
    missing_refs, used_refs = validate_references(parameters, available_refs)

    if missing_refs:
        print(f"[ERROR] Found {len(missing_refs)} missing references:", file=sys.stderr)
        for param_name, source_ref in missing_refs:
            print(f"  - Parameter '{param_name}' references missing citation: '{source_ref}'", file=sys.stderr)
        print(f"\n[ERROR] Please add missing references to {references_path}", file=sys.stderr)
        print(f"[ERROR] Format: <a id=\"{missing_refs[0][1]}\"></a>", file=sys.stderr)
        print()
        # Don't exit - continue generation but warn user
    else:
        print(f"[OK] All {len(set(used_refs))} external references validated")
        print()

    # Validate calculated parameters have formulas
    print("[*] Validating calculated parameters...")
    suspicious_params = validate_calculated_parameters(parameters)

    if suspicious_params:
        print(f"[WARN] Found {len(suspicious_params)} calculated parameters without formula/latex:", file=sys.stderr)
        for param_name, value in suspicious_params[:10]:  # Show first 10
            print(f"  - {param_name} = {value:,.2f} (marked as calculated but no formula)", file=sys.stderr)
        if len(suspicious_params) > 10:
            print(f"  ... and {len(suspicious_params) - 10} more", file=sys.stderr)
        print(f"\n[WARN] Consider adding 'formula' or 'latex' to these parameters", file=sys.stderr)
        print("[WARN] Or change source_type to 'definition' if they're intentional estimates", file=sys.stderr)
        print()
    else:
        print("[OK] All calculated parameters have formulas or latex equations")
        print()

    # Generate _variables.yml
    print(f"[*] Generating _variables.yml (citation mode: {citation_mode})...")
    output_path = project_root / "_variables.yml"
    generate_variables_yml(parameters, output_path, citation_mode=citation_mode)
    print()

    # Generate parameters-and-calculations.qmd
    print("[*] Generating parameters-and-calculations.qmd...")
    qmd_output = project_root / "knowledge" / "appendix" / "parameters-and-calculations.qmd"
    generate_parameters_qmd(parameters, qmd_output, available_refs=available_refs)
    print()

    # Generate references.bib (with full citation data from references.qmd)
    print("[*] Generating references.bib...")
    bib_output = project_root / "references.bib"
    generate_bibtex(parameters, bib_output, available_refs=available_refs, references_path=references_path)
    print()

    # Always generate uncertainty outputs when module is available
    try:
        if simulate is not None:
            print("[*] Generating uncertainty summaries...")
            # Choose a target calculated parameter if any
            target = next((name for name, meta in parameters.items()
                           if hasattr(meta.get("value"), "formula") and meta.get("value").formula), None)
            # Summaries directory
            analysis_dir = project_root / "_analysis"
            
            # Clean up stale analysis files before regenerating
            # This handles deleted/renamed parameters that would leave orphan files
            if analysis_dir.exists():
                import shutil
                stale_count = len(list(analysis_dir.glob("*.json")))
                if stale_count > 0:
                    print(f"[*] Cleaning {stale_count} stale analysis files...")
                    shutil.rmtree(analysis_dir)
            
            analysis_dir.mkdir(exist_ok=True)
            # Minimal inline summary generation to avoid duplicating logic
            from dih_models.uncertainty import simulate as _sim, one_at_a_time_sensitivity as _sens
            sims = _sim(parameters, n=10000)
            import json
            try:
                import numpy as np
            except Exception:
                np = None  # type: ignore
            summaries = {}
            for name, arr in sims.items():
                if np is not None:
                    a = np.asarray(arr)
                    summaries[name] = {
                        "mean": float(np.mean(a)),
                        "std": float(np.std(a)),
                        "p5": float(np.percentile(a, 5)),
                        "p50": float(np.percentile(a, 50)),
                        "p95": float(np.percentile(a, 95)),
                    }
                else:
                    vals = list(arr)
                    m = sum(vals) / len(vals)
                    var = sum((v - m) ** 2 for v in vals) / len(vals)
                    std = var ** 0.5
                    vals_sorted = sorted(vals)
                    def pct(p: float):
                        i = int(p / 100 * (len(vals_sorted) - 1))
                        return vals_sorted[i]
                    summaries[name] = {
                        "mean": m,
                        "std": std,
                        "p5": pct(5),
                        "p50": pct(50),
                        "p95": pct(95),
                    }
            with open(analysis_dir / "samples.json", "w", encoding="utf-8") as f:
                json.dump(summaries, f, indent=2)
            print(f"[OK] Wrote {(analysis_dir / 'samples.json').relative_to(project_root)}")

            if target and _sens is not None:
                sens = _sens(parameters, target_name=target, n=2000)
                with open(analysis_dir / "sensitivity.json", "w", encoding="utf-8") as f:
                    json.dump(sens, f, indent=2)
                print(f"[OK] Wrote {(analysis_dir / 'sensitivity.json').relative_to(project_root)}")
            else:
                print("[WARN] No calculated target found for sensitivity analysis.")

            # Generate rigorous outcomes, tornado, and sensitivity indices for parameters with compute
            if tornado_deltas and regression_sensitivity and Outcome:
                print("[*] Generating outcome distributions and sensitivity analysis...")
                
                # Clean up stale generated tornado/sensitivity QMD files
                # This handles deleted/renamed parameters that would leave orphan files
                figures_dir = project_root / "knowledge" / "figures"
                stale_tornado_files = list(figures_dir.glob("tornado-*.qmd"))
                stale_sensitivity_files = list(figures_dir.glob("sensitivity-table-*.qmd"))
                stale_count = len(stale_tornado_files) + len(stale_sensitivity_files)
                if stale_count > 0:
                    print(f"[*] Cleaning {stale_count} stale generated QMD files...")
                    for f in stale_tornado_files + stale_sensitivity_files:
                        f.unlink()
                
                # Validate: Find calculated parameters missing inputs/compute
                validation_warnings = []
                for param_name, meta in parameters.items():
                    val = meta.get("value")
                    source_type = getattr(val, "source_type", None)
                    has_inputs = hasattr(val, "inputs") and val.inputs
                    has_compute = hasattr(val, "compute") and val.compute
                    
                    if source_type == "calculated":
                        if not has_inputs:
                            validation_warnings.append(f"{param_name}: missing 'inputs' (calculated parameter)")
                        if not has_compute:
                            validation_warnings.append(f"{param_name}: missing 'compute' (calculated parameter)")
                
                if validation_warnings:
                    print(f"\n[WARN] {len(validation_warnings)} calculated parameters missing inputs/compute:")
                    for warning in validation_warnings[:10]:  # Show first 10
                        print(f"  - {warning}")
                    if len(validation_warnings) > 10:
                        print(f"  ... and {len(validation_warnings) - 10} more")
                    print("  (These parameters won't appear in tornado analysis drill-down)\n")
                
                # Auto-discover parameters with compute functions
                analyzable_params = []
                for param_name, meta in parameters.items():
                    val = meta.get("value")
                    if hasattr(val, "compute") and val.compute and hasattr(val, "inputs") and val.inputs:
                        # Wrap as Outcome for tornado/sensitivity
                        outcome = Outcome(
                            name=param_name,
                            inputs=val.inputs,
                            compute=val.compute,
                            units=getattr(val, "unit", "")
                        )
                        analyzable_params.append(outcome)
                
                if not analyzable_params:
                    print("[WARN] No parameters found with compute() and inputs for sensitivity analysis")
                
                outcomes_data = {}
                for outcome in analyzable_params:
                    try:
                        # Build baseline context
                        ctx = {}
                        for inp in outcome.inputs:
                            meta = parameters.get(inp, {})
                            val = meta.get("value")
                            ctx[inp] = float(val) if val is not None else 0.0
                        baseline = outcome.compute(ctx)

                        # MC samples for outcome
                        input_sims = {name: sims[name] for name in outcome.inputs if name in sims}
                        if input_sims:
                            n_samples = len(list(input_sims.values())[0])
                            outcome_samples = []
                            for i in range(n_samples):
                                ctx_i = {name: float(arr[i]) for name, arr in input_sims.items()}
                                outcome_samples.append(outcome.compute(ctx_i))

                            if np is not None:
                                oa = np.asarray(outcome_samples)
                                outcomes_data[outcome.name] = {
                                    "baseline": float(baseline),
                                    "mean": float(np.mean(oa)),
                                    "std": float(np.std(oa)),
                                    "p5": float(np.percentile(oa, 5)),
                                    "p50": float(np.percentile(oa, 50)),
                                    "p95": float(np.percentile(oa, 95)),
                                    "units": outcome.units,
                                }
                            else:
                                m = sum(outcome_samples) / len(outcome_samples)
                                var = sum((v - m) ** 2 for v in outcome_samples) / len(outcome_samples)
                                std = var ** 0.5
                                sorted_o = sorted(outcome_samples)
                                def pct_o(p: float):
                                    return sorted_o[int(p / 100 * (len(sorted_o) - 1))]
                                outcomes_data[outcome.name] = {
                                    "baseline": float(baseline),
                                    "mean": m,
                                    "std": std,
                                    "p5": pct_o(5),
                                    "p50": pct_o(50),
                                    "p95": pct_o(95),
                                    "units": outcome.units,
                                }

                            # Tornado deltas for this outcome
                            tornado = tornado_deltas(parameters, outcome)
                            with open(analysis_dir / f"tornado_{outcome.name}.json", "w", encoding="utf-8") as f:
                                json.dump(tornado, f, indent=2)
                            print(f"[OK] Wrote {(analysis_dir / f'tornado_{outcome.name}.json').relative_to(project_root)}")

                            # Generate tornado chart QMD
                            try:
                                figures_dir = project_root / "knowledge" / "figures"
                                param_meta = parameters.get(outcome.name, {})
                                chart_file = generate_tornado_chart_qmd(
                                    outcome.name, tornado, figures_dir, param_meta,
                                    baseline=float(baseline),
                                    units=outcome.units
                                )
                                print(f"[OK] Generated {chart_file.relative_to(project_root)}")
                            except Exception as chart_err:
                                print(f"[WARN] Failed to generate tornado chart for {outcome.name}: {chart_err}")

                            # Regression sensitivity indices (filter out zero-variance inputs)
                            filtered_input_sims = {}
                            for inp_name, inp_vals in input_sims.items():
                                if np is not None:
                                    std = float(np.std(np.asarray(inp_vals)))
                                else:
                                    vals = list(inp_vals)
                                    mean = sum(vals) / len(vals)
                                    variance = sum((v - mean) ** 2 for v in vals) / len(vals)
                                    std = variance ** 0.5
                                
                                # Only include inputs that actually vary
                                if std > 1e-10:
                                    filtered_input_sims[inp_name] = inp_vals
                            
                            if filtered_input_sims:
                                sens_indices = regression_sensitivity(filtered_input_sims, outcome_samples)
                            else:
                                sens_indices = {inp: 0.0 for inp in input_sims.keys()}
                            
                            with open(analysis_dir / f"sensitivity_indices_{outcome.name}.json", "w", encoding="utf-8") as f:
                                json.dump(sens_indices, f, indent=2)
                            print(f"[OK] Wrote {(analysis_dir / f'sensitivity_indices_{outcome.name}.json').relative_to(project_root)}")

                            # Generate sensitivity table QMD only if there's meaningful variance
                            # Skip tables where all coefficients are effectively zero (< 0.001)
                            max_coef = max(abs(v) for v in sens_indices.values()) if sens_indices else 0
                            if max_coef >= 0.001:
                                try:
                                    sensitivity_table_file = generate_sensitivity_table_qmd(outcome.name, sens_indices, figures_dir, param_meta)
                                    print(f"[OK] Generated {sensitivity_table_file.relative_to(project_root)}")
                                except Exception as table_err:
                                    print(f"[WARN] Failed to generate sensitivity table for {outcome.name}: {table_err}")
                            else:
                                print(f"[SKIP] Sensitivity table for {outcome.name}: all coefficients near zero")
                    except Exception as e:
                        print(f"[WARN] Skipped outcome {outcome.name}: {e}")

                with open(analysis_dir / "outcomes.json", "w", encoding="utf-8") as f:
                    json.dump(outcomes_data, f, indent=2)
                print(f"[OK] Wrote {(analysis_dir / 'outcomes.json').relative_to(project_root)}")

                # Discount rate sensitivity for ROI_complete
                try:
                    roi_outcome = next((o for o in analyzable_params if "ROI" in o.name.upper() and "COMPLETE" in o.name.upper()), None)
                    if roi_outcome:
                        print("[*] Generating discount rate sensitivity curve...")
                        discount_curve = []
                        for rate in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07]:
                            ctx_disc = {}
                            for inp in roi_outcome.inputs:
                                meta = parameters.get(inp, {})
                                val = meta.get("value")
                                if inp == "NPV_DISCOUNT_RATE_STANDARD":
                                    ctx_disc[inp] = rate
                                else:
                                    ctx_disc[inp] = float(val) if val is not None else 0.0
                            roi_val = roi_outcome.compute(ctx_disc)
                            discount_curve.append({"discount_rate": rate, "roi": float(roi_val)})
                        with open(analysis_dir / "discount_curve_ROI.json", "w", encoding="utf-8") as f:
                            json.dump(discount_curve, f, indent=2)
                        print(f"[OK] Wrote {(analysis_dir / 'discount_curve_ROI.json').relative_to(project_root)}")
                except Exception as e:
                    print(f"[WARN] Discount curve generation skipped: {e}")

                # Scenario bands for ROI_complete
                try:
                    roi_outcome = next((o for o in analyzable_params if "ROI" in o.name.upper() and "COMPLETE" in o.name.upper()), None)
                    if roi_outcome:
                        print("[*] Generating scenario bands...")
                        scenarios = {
                            "worst": 0.5,  # benefits half
                            "conservative": 0.8,
                            "baseline": 1.0,
                            "optimistic": 1.5,
                        }
                        scenario_results = []
                        for scenario_name, multiplier in scenarios.items():
                            ctx_scen = {}
                            for inp in roi_outcome.inputs:
                                meta = parameters.get(inp, {})
                                val = meta.get("value")
                                v = float(val) if val is not None else 0.0
                                # Scale benefits, keep costs fixed
                                if inp in ["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL", "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT", "TRIAL_COST_REDUCTION_PCT"]:
                                    v *= multiplier
                                ctx_scen[inp] = v
                            roi_val = roi_outcome.compute(ctx_scen)
                            scenario_results.append({"scenario": scenario_name, "roi": float(roi_val)})
                        with open(analysis_dir / "scenario_bands_ROI.json", "w", encoding="utf-8") as f:
                            json.dump(scenario_results, f, indent=2)
                        print(f"[OK] Wrote {(analysis_dir / 'scenario_bands_ROI.json').relative_to(project_root)}")
                except Exception as e:
                    print(f"[WARN] Scenario bands generation skipped: {e}")

            print()
        else:
            print("[WARN] Uncertainty module unavailable; skipping uncertainty summaries.")
            print()
    except Exception as e:
        print(f"[WARN] Uncertainty generation skipped: {e}")
        print()

    # Optionally inject citations
    if inject_citations:
        print("[*] Injecting citations into economics.qmd...")
        economics_qmd = project_root / "knowledge" / "economics" / "economics.qmd"
        inject_citations_into_qmd(parameters, economics_qmd)
        print()

    # Generate outline from updated headings
    print("[*] Regenerating outline from chapter headings...")
    generate_outline_script = project_root / "scripts" / "generate-outline.py"
    if generate_outline_script.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(generate_outline_script), "--output", "OUTLINE-GENERATED.MD"],
                cwd=str(project_root),
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            if result.returncode == 0:
                print("[OK] Outline regenerated")
            else:
                print(f"[WARN] Outline generation had issues: {result.stderr}", file=sys.stderr)
        except Exception as e:
            print(f"[WARN] Could not regenerate outline: {e}", file=sys.stderr)
    else:
        print(f"[WARN] Outline script not found: {generate_outline_script}", file=sys.stderr)
    print()

    print("[OK] All academic outputs generated successfully!")
    print()
    print("[*] Next steps:")
    print("    1. Review generated files:")
    print(f"       - {output_path.relative_to(project_root)}")
    print(f"       - {qmd_output.relative_to(project_root)}")
    print(f"       - {references_json_path.relative_to(project_root)}")
    print(f"       - {bib_output.relative_to(project_root)}")
    print(f"       - {reference_ids_path.relative_to(project_root)}")
    print(f"       - OUTLINE-GENERATED.MD")
    if inject_citations:
        print(f"       - {economics_qmd.relative_to(project_root)} (citations injected)")
    print("    2. Render Quarto book to see results")
    print("    3. Zero manual maintenance required - just re-run this script!")
    print()
    if citation_mode == "none":
        print("[TIP] Want citations? Try:")
        print("      --cite-mode=inline    (automatic inline citations)")
        print("      --cite-mode=separate  (flexible citation variables)")
        print("      --cite-mode=both      (maximum control)")


if __name__ == "__main__":
    main()
