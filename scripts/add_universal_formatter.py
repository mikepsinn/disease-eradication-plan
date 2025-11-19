#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add universal format_parameter_value() to parameters.py

This replaces the old format_billions/millions/trillions functions with
a single universal formatter that auto-detects units and scales appropriately.
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path

# The universal formatter with auto-detection
FORMATTER_CODE = '''
def format_parameter_value(param, unit=None):
    """
    Universal formatter - handles Parameter objects, auto-scales based on value.

    Automatically detects unit from Parameter objects and scales appropriately.
    Works with raw numbers too.

    Args:
        param: Parameter object or raw number
        unit: Optional unit override (auto-detected if param has .unit attribute)

    Returns:
        Formatted string like "$27.18B", "50%", "184.6M deaths", etc.

    Examples:
        >>> format_parameter_value(TREATY_ANNUAL_FUNDING)  # Auto-detects USD unit
        "$27.18B"
        >>> format_parameter_value(27180000000, "USD")  # Manual unit
        "$27.18B"
        >>> format_parameter_value(0.5, "rate")  # Percentage
        "50%"
    """
    # Auto-detect unit from Parameter object
    if unit is None and hasattr(param, 'unit'):
        unit = param.unit or ""
    elif unit is None:
        unit = ""

    # Get raw numeric value
    if isinstance(param, (int, float)):
        value = float(param)
    elif hasattr(param, '__float__'):
        value = float(param)
    else:
        # Parameter object - extract numeric value
        value = float(param)

    # Detect currency parameters
    is_currency = 'USD' in unit or 'usd' in unit or 'dollar' in unit.lower()

    # Detect percentage parameters
    is_percentage = '%' in unit or 'percent' in unit.lower() or 'rate' in unit.lower()

    # Check if value is already in billions, millions, thousands
    is_in_billions = 'billion' in unit.lower()
    is_in_millions = 'million' in unit.lower()
    is_in_thousands = 'thousand' in unit.lower()

    # Helper to remove trailing zeros
    def clean_number(num_str: str) -> str:
        if '.' in num_str:
            num_str = num_str.rstrip('0').rstrip('.')
        return num_str

    # Currency formatting (3 significant figures)
    if is_currency:
        abs_val = abs(value)

        if is_in_billions:
            # Value already in billions
            if abs_val >= 1000:  # Trillions
                scaled = value / 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}T"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}T"
                else:
                    formatted = f"${scaled:.2f}T"
            elif abs_val >= 1:  # Billions
                if abs_val >= 100:
                    formatted = f"${value:.0f}B"
                elif abs_val >= 10:
                    formatted = f"${value:.1f}B"
                else:
                    formatted = f"${value:.2f}B"
            elif abs_val >= 0.001:  # Millions
                scaled = value * 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}M"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}M"
                else:
                    formatted = f"${scaled:.2f}M"
            else:
                formatted = f"${value*1000000:.0f}K"
        elif is_in_millions:
            # Value already in millions
            if abs_val >= 1000:  # Billions
                scaled = value / 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}B"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}B"
                else:
                    formatted = f"${scaled:.2f}B"
            elif abs_val >= 1:  # Millions
                if abs_val >= 100:
                    formatted = f"${value:.0f}M"
                elif abs_val >= 10:
                    formatted = f"${value:.1f}M"
                else:
                    formatted = f"${value:.2f}M"
            elif abs_val >= 0.001:  # Thousands
                scaled = value * 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}K"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}K"
                else:
                    formatted = f"${scaled:.2f}K"
            else:
                formatted = f"${value*1000:.0f}"
        elif is_in_thousands:
            # Value already in thousands
            if abs_val >= 1000000:  # Billions
                scaled = value / 1000000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}B"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}B"
                else:
                    formatted = f"${scaled:.2f}B"
            elif abs_val >= 1000:  # Millions
                scaled = value / 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}M"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}M"
                else:
                    formatted = f"${scaled:.2f}M"
            elif abs_val >= 1:  # Thousands
                if abs_val >= 100:
                    formatted = f"${value:.0f}K"
                elif abs_val >= 10:
                    formatted = f"${value:.1f}K"
                else:
                    formatted = f"${value:.2f}K"
            else:
                formatted = f"${value*1000:.0f}"
        else:
            # Value in raw dollars - auto-scale
            if abs_val >= 1e12:  # Trillions
                scaled = value / 1e12
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}T"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}T"
                else:
                    formatted = f"${scaled:.2f}T"
            elif abs_val >= 1e9:  # Billions
                scaled = value / 1e9
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}B"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}B"
                else:
                    formatted = f"${scaled:.2f}B"
            elif abs_val >= 1e6:  # Millions
                scaled = value / 1e6
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}M"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}M"
                else:
                    formatted = f"${scaled:.2f}M"
            elif abs_val >= 1e3:  # Thousands
                scaled = value / 1e3
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}K"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}K"
                else:
                    formatted = f"${scaled:.2f}K"
            else:
                formatted = f"${value:.0f}"

        # Clean trailing .0
        return formatted.replace('.0B', 'B').replace('.0M', 'M').replace('.0T', 'T').replace('.0K', 'K')

    # Non-currency numbers - auto-scale large numbers
    abs_val = abs(value)

    if abs_val >= 1e9:  # Billions
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
    elif abs_val >= 100_000:  # 100K+
        scaled = value / 1e3
        if abs(scaled) >= 100:
            formatted_num = f"{scaled:.0f}K"
        elif abs(scaled) >= 10:
            formatted_num = f"{scaled:.1f}K"
        else:
            formatted_num = f"{scaled:.2f}K"
    elif value == int(value):
        formatted_num = f"{int(value):,}"
    elif abs_val >= 1000:
        formatted_num = f"{value:,.0f}"
    elif abs_val >= 1:
        if value >= 100:
            formatted_num = f"{value:,.0f}"
        elif value >= 10:
            formatted_num = clean_number(f"{value:,.1f}")
        else:
            formatted_num = clean_number(f"{value:,.2f}")
    else:
        formatted_num = clean_number(f"{value:.3g}")

    # Clean trailing zeros
    formatted_num = formatted_num.replace('.0B', 'B').replace('.0M', 'M').replace('.0K', 'K')

    # Percentage formatting
    if is_percentage:
        pct_value = value * 100
        if abs(pct_value) >= 100:
            pct_formatted = f"{pct_value:.0f}"
        elif abs(pct_value) >= 10:
            pct_formatted = clean_number(f"{pct_value:.1f}")
        elif abs(pct_value) >= 1:
            pct_formatted = clean_number(f"{pct_value:.2f}")
        else:
            pct_formatted = clean_number(f"{pct_value:.3g}")
        return f"{pct_formatted}%"

    return formatted_num

'''

def main():
    params_file = Path('dih_models/parameters.py')

    if not params_file.exists():
        print("[ERROR] parameters.py not found")
        sys.exit(1)

    content = params_file.read_text(encoding='utf-8')

    # Find the HELPER FUNCTIONS section
    helper_section = "# HELPER FUNCTIONS\n# ---\n"

    if helper_section not in content:
        print("[ERROR] Could not find HELPER FUNCTIONS section")
        sys.exit(1)

    # Insert the new formatter right after the HELPER FUNCTIONS header
    new_content = content.replace(
        helper_section,
        helper_section + "\n" + FORMATTER_CODE
    )

    # Write back
    params_file.write_text(new_content, encoding='utf-8')

    print("[OK] Added format_parameter_value() to parameters.py")
    print("[*] Next: Run replacement script to update all uses")

if __name__ == '__main__':
    main()
