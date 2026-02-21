"""
Formatting utilities for economic parameters.
Separated to avoid circular dependencies between generation scripts and parameters.py.
"""
from typing import Union, Any, TYPE_CHECKING
import math

if TYPE_CHECKING:
    # Use string forward reference to avoid importing Parameter
    Parameter = Any

def format_parameter_value(param: Union[float, int, str, "Parameter"], unit: str | None = None, include_unit: bool = True, ratio_suffix: bool = True) -> str:
    """
    Universal formatter - handles Parameter objects, auto-scales based on value.

    Automatically detects unit from Parameter objects and scales appropriately.
    Works with raw numbers too.

    Args:
        param: Parameter object or raw number
        unit: Optional unit override (auto-detected if param has .unit attribute)
        include_unit: Whether to include the unit string in the output (default: True)

    Returns:
        Formatted string like "$27.18B", "50%", "184.6M deaths", etc.
    """
    if param is None:
        return ""

    # Extract value and unit
    value = float(param)
    
    # Auto-detect unit from Parameter object if not provided
    if unit is None and hasattr(param, "unit"):
        unit = param.unit
    
    # Normalize unit for checking
    unit_check = unit.lower() if unit else ""
    
    # Detect currency parameters
    is_currency = "usd" in unit_check or "dollar" in unit_check or "$" in unit_check

    # Detect percentage parameters
    is_percentage = "%" in unit_check or "percent" in unit_check or "rate" in unit_check

    # Detect ratio parameters (should format as X:1)
    is_ratio = unit_check == "ratio"

    # Detect multiplier/factor parameters (should format as Xx)
    # Supports unit="multiplier", unit="factor", or unit="x"
    is_multiplier = "multiplier" in unit_check or "factor" in unit_check or unit_check == "x"

    # Check if value is already scaled (e.g. input is in billions)
    is_in_billions = "billion" in unit_check
    is_in_millions = "million" in unit_check
    is_in_thousands = "thousand" in unit_check

    formatted_num = ""

    # Helper to remove trailing zeros and decimal point
    def clean_number(num_str: str) -> str:
        if "." in num_str:
            num_str = num_str.rstrip("0").rstrip(".")
        return num_str

    if is_currency:
        # Determine the absolute value for scaling
        abs_val = abs(value)

        # Handle pre-scaled inputs (e.g. value=50, unit="billions USD")
        if is_in_billions:
            raw_dollars = value * 1e9
        elif is_in_millions:
            raw_dollars = value * 1e6
        elif is_in_thousands:
            raw_dollars = value * 1e3
        else:
            raw_dollars = value
        
        abs_raw = abs(raw_dollars)

        if abs_raw >= 1e15:  # Quadrillions
            scaled = raw_dollars / 1e15
            if abs(scaled) >= 100:
                formatted_num = f"${scaled:.0f} quadrillion"
            elif abs(scaled) >= 10:
                formatted_num = f"${scaled:.1f} quadrillion"
            else:
                formatted_num = f"${scaled:.2f} quadrillion"
        elif abs_raw >= 1e12:  # Trillions
            scaled = raw_dollars / 1e12
            if abs(scaled) >= 100:
                formatted_num = f"${scaled:.0f}T"
            elif abs(scaled) >= 10:
                formatted_num = f"${scaled:.1f}T"
            else:
                formatted_num = f"${scaled:.2f}T"
        elif abs_raw >= 1e9:  # Billions
            scaled = raw_dollars / 1e9
            if abs(scaled) >= 100:
                formatted_num = f"${scaled:.0f}B"
            elif abs(scaled) >= 10:
                formatted_num = f"${scaled:.1f}B"
            else:
                formatted_num = f"${scaled:.2f}B"
        elif abs_raw >= 1e6:  # Millions
            scaled = raw_dollars / 1e6
            if abs(scaled) >= 100:
                formatted_num = f"${scaled:.0f}M"
            elif abs(scaled) >= 10:
                formatted_num = f"${scaled:.1f}M"
            else:
                formatted_num = f"${scaled:.2f}M"
        elif abs_raw >= 1e3:  # Thousands
            scaled = raw_dollars / 1e3
            if abs(scaled) >= 100:
                formatted_num = f"${scaled:.0f}K"
            elif abs(scaled) >= 10:
                formatted_num = f"${scaled:.1f}K"
            else:
                formatted_num = f"${scaled:.2f}K"
        elif abs_raw >= 10:
            formatted_num = f"${raw_dollars:.0f}"
        elif abs_raw >= 1:
            formatted_num = f"${raw_dollars:.2f}"
        elif abs_raw >= 0.01:
            formatted_num = f"${raw_dollars:.3f}"
        elif abs_raw > 0:
            formatted_num = f"${raw_dollars:.4f}"
        else:
            formatted_num = "$0"

        # Clean up trailing .0 and .00 for cleaner look (e.g. $50.0B -> $50B, $1.00B -> $1B)
        formatted_num = formatted_num.replace(".00 ", " ").replace(".00T", "T").replace(".00B", "B").replace(".00M", "M").replace(".00K", "K")
        formatted_num = formatted_num.replace(".0 ", " ").replace(".0T", "T").replace(".0B", "B").replace(".0M", "M").replace(".0K", "K")
        return formatted_num

    elif is_percentage:
        # Normalize to percentage points (e.g. 0.01 -> 1%)
        # Note: Some inputs might already be in percentage points (e.g. 50 meaning 50%)
        # Heuristic: if value > 1, assume it's already a percentage, unless strictly <= 1.0 which is ambiguous.
        # Standard convention in this codebase: 0.50 = 50%
        pct_val = value * 100
        
        # Format with appropriate precision
        if abs(pct_val) >= 100:
            pct_formatted = f"{pct_val:.0f}"
        elif abs(pct_val) >= 10:
            pct_formatted = clean_number(f"{pct_val:.1f}")
        elif abs(pct_val) >= 1:
            pct_formatted = clean_number(f"{pct_val:.2f}")
        else:
            pct_formatted = clean_number(f"{pct_val:.3g}")
            
        return f"{pct_formatted}%"

    elif is_ratio:
        # Format as X:1 (e.g., 847,733:1 for ROI)
        if abs(value) >= 1e6:
            scaled = value / 1e6
            if abs(scaled) >= 100:
                ratio_formatted = f"{scaled:.0f}M"
            elif abs(scaled) >= 10:
                ratio_formatted = clean_number(f"{scaled:.1f}M")
            else:
                ratio_formatted = clean_number(f"{scaled:.2f}M")
        elif abs(value) >= 1e3:
            scaled = value / 1e3
            if abs(scaled) >= 100:
                ratio_formatted = f"{scaled:.0f}k"
            elif abs(scaled) >= 10:
                ratio_formatted = clean_number(f"{scaled:.1f}k")
            else:
                ratio_formatted = clean_number(f"{scaled:.2f}k")
        elif abs(value) >= 100:
            ratio_formatted = f"{value:,.0f}"
        elif abs(value) >= 10:
            ratio_formatted = clean_number(f"{value:.1f}")
        elif abs(value) >= 1:
            ratio_formatted = clean_number(f"{value:.2f}")
        else:
            ratio_formatted = clean_number(f"{value:.3g}")
        return f"{ratio_formatted}:1" if ratio_suffix else ratio_formatted

    elif is_multiplier:
        # Format as Xx (e.g., 22x for multipliers)
        if abs(value) >= 1e6:
            scaled = value / 1e6
            multiplier_formatted = clean_number(f"{scaled:.1f}M")
        elif abs(value) >= 1e3:
            scaled = value / 1e3
            multiplier_formatted = clean_number(f"{scaled:.1f}k")
        elif abs(value) >= 100:
            multiplier_formatted = f"{value:,.0f}"
        elif abs(value) >= 10:
            multiplier_formatted = clean_number(f"{value:.1f}")
        elif abs(value) >= 1:
            multiplier_formatted = clean_number(f"{value:.2f}")
        else:
            multiplier_formatted = clean_number(f"{value:.3g}")
        return f"{multiplier_formatted}x"

    else:
        # Standard number formatting with auto-scaling
        # Handle pre-scaled inputs
        if is_in_billions:
            raw_val = value * 1e9
        elif is_in_millions:
            raw_val = value * 1e6
        elif is_in_thousands:
            raw_val = value * 1e3
        else:
            raw_val = value

        abs_raw = abs(raw_val)

        # Use full word forms for academic style
        if abs_raw >= 1e15:
            scaled = raw_val / 1e15
            suffix = " quadrillion"
        elif abs_raw >= 1e12:
            scaled = raw_val / 1e12
            suffix = " trillion"
        elif abs_raw >= 1e9:
            scaled = raw_val / 1e9
            suffix = " billion"
        elif abs_raw >= 1e6:
            scaled = raw_val / 1e6
            suffix = " million"
        elif abs_raw >= 1e3:
            scaled = raw_val / 1e3
            suffix = " thousand"
        else:
            scaled = raw_val
            suffix = ""

        # Use 3 significant figures consistently
        if suffix:
            if abs(scaled) >= 100:
                formatted_num = f"{scaled:.0f}{suffix}"      # 565 billion (3 sig figs)
            elif abs(scaled) >= 10:
                formatted_num = f"{scaled:.1f}{suffix}"      # 10.7 billion (3 sig figs)
            else:
                formatted_num = f"{scaled:.2f}{suffix}"      # 1.93 quadrillion (3 sig figs)
        else:
            # No suffix, small number — also use 3 sig figs
            if abs_raw >= 100:
                formatted_num = f"{raw_val:.0f}"             # 565 (3+ sig figs)
            elif abs_raw >= 10:
                formatted_num = f"{raw_val:.1f}"             # 10.7 (3 sig figs)
            elif abs_raw >= 1:
                formatted_num = f"{raw_val:.2f}"             # 1.93 (3 sig figs)
            elif abs_raw > 0:
                formatted_num = f"{raw_val:.3g}"             # 0.00193 (3 sig figs)
            else:
                formatted_num = "0"

        formatted_num = clean_number(formatted_num)
        
        # Add unit if requested
        if include_unit and unit:
            # Don't add if already in unit string or processed
            # Also skip for multiplier-type units which get special formatting
            unit_lower = unit.lower()
            if unit_lower in ["usd", "dollar", "billions", "millions", "thousands", "x", "multiplier", "factor", "ratio"]:
                pass  # Already handled prefix/suffix or special formatting
            else:
                formatted_num = f"{formatted_num} {unit}"
        
        return formatted_num


def format_roi(value: float) -> str:
    """Format ROI as ratio

    Args:
        value: ROI number

    Returns:
        Formatted string like "463:1"
    """
    return f"{value:,.0f}:1"


def format_percentage(value: float) -> str:
    """Format as percentage

    Args:
        value: Decimal value (e.g., 0.01 for 1%)

    Returns:
        Formatted string like "1.0%"
    """
    return f"{value*100:,.1f}%"


def format_qalys(value: float) -> str:
    """Format QALY count with commas

    Args:
        value: Number of QALYs

    Returns:
        Formatted string like "840,000"
    """
    return f"{value:,.0f}"
