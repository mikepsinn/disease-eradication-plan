"""
Formatting utilities for economic parameters.
Separated to avoid circular dependencies between generation scripts and parameters.py.
"""
from typing import Union, Any, TYPE_CHECKING
import math

if TYPE_CHECKING:
    # Use string forward reference to avoid importing Parameter
    Parameter = Any

def format_parameter_value(param: Union[float, int, str, "Parameter"], unit: str | None = None, include_unit: bool = True) -> str:
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

        # Clean up trailing .0 for cleaner look (e.g. $50.0B -> $50B)
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

        if abs_raw >= 1e12:
            scaled = raw_val / 1e12
            suffix = "T"
        elif abs_raw >= 1e9:
            scaled = raw_val / 1e9
            suffix = "B"
        elif abs_raw >= 1e6:
            scaled = raw_val / 1e6
            suffix = "M"
        elif abs_raw >= 1e3:
            scaled = raw_val / 1e3
            suffix = "k"
        else:
            scaled = raw_val
            suffix = ""

        if abs(scaled) >= 100:
            formatted_num = f"{scaled:.0f}{suffix}"
        elif abs(scaled) >= 10:
            formatted_num = f"{scaled:.1f}{suffix}"
        elif abs(scaled) >= 1 and suffix:
            formatted_num = f"{scaled:.2f}{suffix}"
        elif suffix:  # Small number but with suffix (unlikely but possible)
            formatted_num = f"{scaled:.2f}{suffix}"
        else:
            # No suffix, small number
            if abs_raw >= 100:
                formatted_num = f"{raw_val:.0f}"
            elif abs_raw >= 1:
                formatted_num = f"{raw_val:.2f}"
            elif abs_raw > 0:
                formatted_num = f"{raw_val:.3g}"
            else:
                formatted_num = "0"

        formatted_num = clean_number(formatted_num)
        
        # Add unit if requested
        if include_unit and unit:
            # Don't add if already in unit string or processed
            if unit.lower() in ["usd", "dollar", "billions", "millions", "thousands"]:
                pass  # Already handled prefix/suffix
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
