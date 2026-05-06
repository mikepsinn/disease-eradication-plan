#!/usr/bin/env python3
"""
LaTeX Equation Generation Utilities
====================================

Automatically generates LaTeX equations from Parameter metadata.

Functions:
- generate_auto_latex: Main function to generate LaTeX from parameters
- format_latex_value: Format numeric values for LaTeX display
- create_latex_variable_name: Generate semantic LaTeX variable names
- create_short_label: Create abbreviated labels for equations
- infer_operation_from_compute: Detect operation type from compute function

Usage:
    from dih_models.latex_generation import generate_auto_latex

    latex = generate_auto_latex(
        param_name="PEACE_DIVIDEND_ANNUAL",
        param_value=parameter_instance,
        parameters=all_parameters_dict
    )
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .formatting import format_parameter_value

# Separator between equation blocks in expanded LaTeX output.
# Each block is a self-contained equation that can be wrapped in its own $$ delimiters,
# allowing LaTeX to break pages between them.
LATEX_BLOCK_SEP = "\n%%BLOCK%%\n"

# Track parameters that fall back to formula-based LaTeX generation
# Format: {param_name: (formula_used, reason)}
_formula_fallback_log: Dict[str, Tuple[str, str]] = {}


def get_formula_fallback_log() -> List[Tuple[str, str, str]]:
    """Get the list of parameters that used formula fallback during LaTeX generation."""
    return [(name, formula, reason) for name, (formula, reason) in sorted(_formula_fallback_log.items())]


def clear_formula_fallback_log():
    """Clear the formula fallback log (call at start of generation)."""
    global _formula_fallback_log
    _formula_fallback_log = {}


def log_formula_fallback(param_name: str, formula: str, reason: str):
    """Log a parameter that fell back to using formula for LaTeX generation."""
    # Only log first occurrence (avoid duplicates from recursive expansion)
    if param_name not in _formula_fallback_log:
        _formula_fallback_log[param_name] = (formula, reason)


def collapse_latex_blocks(latex: str) -> str:
    r"""
    Collapse multi-block LaTeX back into a single gathered environment.

    Use this when you need a single LaTeX expression (e.g., for web display)
    rather than multiple page-breakable blocks (used for PDF).

    Args:
        latex: LaTeX string possibly containing LATEX_BLOCK_SEP separators

    Returns:
        Single LaTeX expression with \begin{gathered} wrapping
    """
    if LATEX_BLOCK_SEP not in latex:
        return latex

    blocks = [b.strip() for b in latex.split(LATEX_BLOCK_SEP)]
    lines = [blocks[0]]
    for block in blocks[1:]:
        lines.append(f"\\\\[0.5em]\n\\text{{where }} {block}")
    combined = '\n'.join(lines)
    return f"\\begin{{gathered}}\n{combined}\n\\end{{gathered}}"


def extract_distinguishing_suffix(param_name: str, all_input_names: list[str] | None = None) -> str | None:
    """
    Extract the distinguishing part of a parameter name when it's part of a group.
    
    When multiple parameters share a common prefix (like DFDA_OPEX_*), this returns
    the unique suffix that distinguishes them (e.g., "platform", "staff", "infra").
    
    Args:
        param_name: Full parameter name like "DFDA_OPEX_PLATFORM_MAINTENANCE"
        all_input_names: List of sibling parameter names to find common prefix
        
    Returns:
        Distinguishing suffix like "platform" or None if no clear suffix found
        
    Examples:
        >>> extract_distinguishing_suffix("DFDA_OPEX_PLATFORM_MAINTENANCE", 
        ...     ["DFDA_OPEX_STAFF", "DFDA_OPEX_INFRASTRUCTURE"])
        "platform"
        >>> extract_distinguishing_suffix("GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT",
        ...     ["GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT"])
        "transport"
    """
    if not all_input_names:
        return None
    
    parts = param_name.upper().split('_')
    
    # Find common prefix length among all inputs
    common_prefix_len = 0
    for i in range(len(parts)):
        prefix = '_'.join(parts[:i+1]) + '_'
        # Check if other inputs share this prefix
        others_share = sum(1 for other in all_input_names 
                          if other.upper().startswith(prefix) and other != param_name)
        if others_share > 0:
            common_prefix_len = i + 1
        else:
            break
    
    if common_prefix_len == 0 or common_prefix_len >= len(parts):
        return None
    
    # Get the distinguishing parts (after common prefix, before common suffix like "CONFLICT")
    suffix_parts = parts[common_prefix_len:]
    
    # Remove common suffixes that don't distinguish
    common_suffixes = {'CONFLICT', 'ANNUAL', 'GLOBAL', 'TOTAL', 'COST', 'VALUE'}
    suffix_parts = [p for p in suffix_parts if p not in common_suffixes]
    
    if not suffix_parts:
        return None
    
    # Map to readable short names
    suffix_map = {
        'PLATFORM_MAINTENANCE': 'platform',
        'PLATFORM': 'platform',
        'MAINTENANCE': 'maint',
        'STAFF': 'staff',
        'INFRASTRUCTURE': 'infra',
        'REGULATORY': 'reg',
        'COMMUNITY': 'community',
        'TRANSPORTATION': 'transport',
        'ENERGY': 'energy',
        'COMMUNICATIONS': 'comms',
        'WATER': 'water',
        'EDUCATION': 'edu',
        'HEALTHCARE': 'health',
        'ACTIVE_COMBAT': 'combat',
        'COMBAT': 'combat',
        'STATE_VIOLENCE': 'state',
        'STATE': 'state',
        'TERROR_ATTACKS': 'terror',
        'TERROR': 'terror',
        'SHIPPING': 'shipping',
        'CURRENCY': 'currency',
        'CAPITAL': 'capital',
        'OPPORTUNITY': 'opp',
        'PTSD': 'PTSD',
        'REFUGEE': 'refugee',
        'VETERAN': 'veteran',
        'ENVIRONMENTAL': 'env',
        'LOST_HUMAN_CAPITAL': 'human_cap',
        'LOST_ECONOMIC_GROWTH': 'econ_growth',
        'HUMAN_CAPITAL': 'human_cap',
        'ECONOMIC_GROWTH': 'econ_growth',
    }
    
    # Try to match the full suffix first, then progressively shorter
    suffix_str = '_'.join(suffix_parts)
    if suffix_str in suffix_map:
        return suffix_map[suffix_str]
    
    # Try first part only
    if suffix_parts[0] in suffix_map:
        return suffix_map[suffix_parts[0]]
    
    # Fall back to lowercase first part
    return suffix_parts[0].lower()


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
        'DFDA': 'dFDA',  # decentralized framework for drug assessment
        'DIH': 'DIH',    # Decentralized Institutes of Health
        'ROI': 'ROI',    # Return on Investment
        'QALY': 'QALY',  # Quality-Adjusted Life Year
        'QALYS': 'QALYs',
        'DALY': 'DALY',  # Disability-Adjusted Life Year
        'DALYS': 'DALYs',
        'NPV': 'NPV',    # Net Present Value
        'OPEX': 'OPEX',   # Operating Expenses
        'CAPEX': 'CAPEX',  # Capital Expenses
        'GDP': 'GDP',      # Gross Domestic Product
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


def infer_operation_from_compute(param_value: Any, inputs: list) -> tuple[str, str | float | None]:
    """
    Infer operation type by testing the compute function with known values.

    Returns:
        Tuple of (operation_type, metadata) where:
        - operation_type: 'sum', 'multiply', 'divide', 'subtract', 'identity',
                         'multiply_constant', 'divide_constant', 'add_constant', 'subtract_constant', 'complex'
        - metadata: For binary ops between params: 'first_over_second', 'second_over_first', etc.
                   For constant ops: the constant value (float)
                   Otherwise: None
    """
    if not hasattr(param_value, 'compute') or not param_value.compute:
        return 'complex', None

    n = len(inputs)
    if n == 0:
        return 'complex', None

    # Create test context with distinct values that make operations distinguishable
    # Use values like [2, 3, 4, ...] so we can identify the operation
    test_vals = [2.0 + i for i in range(n)]
    ctx = {name: val for name, val in zip(inputs, test_vals)}

    try:
        result = param_value.compute(ctx)
    except Exception:
        return 'complex', None

    if n == 1:
        # Single input - check for identity or operations with constants
        v1 = test_vals[0]  # 2.0
        r1 = result

        # Check identity first
        if abs(r1 - v1) < 0.01:
            return 'identity', None

        # Test with a second value to detect constant operations
        # Use a different test value to extract the constant
        v2 = 5.0
        ctx2 = {inputs[0]: v2}
        try:
            r2 = param_value.compute(ctx2)
        except Exception:
            return 'transform', None

        # Detect multiply by constant: r = v * c
        # From two tests: r1 = v1 * c, r2 = v2 * c
        # Therefore: c = r1 / v1 = r2 / v2 (should be equal)
        if abs(v1) > 0.01 and abs(v2) > 0.01:
            c1 = r1 / v1
            c2 = r2 / v2
            if abs(c1 - c2) < 0.01:
                # Constant multiplication detected
                return 'multiply_constant', c1

        # Detect add constant: r = v + c
        # From two tests: r1 = v1 + c, r2 = v2 + c
        # Therefore: c = r1 - v1 = r2 - v2 (should be equal)
        c1 = r1 - v1
        c2 = r2 - v2
        if abs(c1 - c2) < 0.01:
            # Constant addition detected
            return 'add_constant', c1

        # Detect divide by constant: r = v / c
        # From two tests: r1 = v1 / c, r2 = v2 / c
        # Therefore: c = v1 / r1 = v2 / r2 (should be equal)
        if abs(r1) > 0.01 and abs(r2) > 0.01:
            c1 = v1 / r1
            c2 = v2 / r2
            if abs(c1 - c2) < 0.01:
                # Constant division detected
                return 'divide_constant', c1

        # Detect subtract constant: r = v - c OR r = c - v
        # Case 1: r = v - c, then c = v - r
        c1 = v1 - r1
        c2 = v2 - r2
        if abs(c1 - c2) < 0.01:
            return 'subtract_constant', c1

        # Case 2: r = c - v, then c = r + v
        c1 = r1 + v1
        c2 = r2 + v2
        if abs(c1 - c2) < 0.01:
            return 'constant_minus_var', c1

        return 'transform', None

    elif n == 2:
        a, b = test_vals[0], test_vals[1]  # 2.0, 3.0

        # Check each operation type
        if abs(result - (a + b)) < 0.01:  # 2 + 3 = 5
            return 'sum', None
        elif abs(result - (a * b)) < 0.01:  # 2 * 3 = 6
            return 'multiply', None
        elif abs(result - (a / b)) < 0.01:  # 2 / 3 ≈ 0.667
            return 'divide', 'first_over_second'
        elif abs(result - (b / a)) < 0.01:  # 3 / 2 = 1.5
            return 'divide', 'second_over_first'
        elif abs(result - (a - b)) < 0.01:  # 2 - 3 = -1
            return 'subtract', 'first_minus_second'
        elif abs(result - (b - a)) < 0.01:  # 3 - 2 = 1
            return 'subtract', 'second_minus_first'
        # Check for "1 - (A/B)" pattern: result = 1 - (a/b)
        elif abs(result - (1 - a / b)) < 0.01:  # 1 - 2/3 ≈ 0.333
            return 'one_minus_quotient', 'first_over_second'
        elif abs(result - (1 - b / a)) < 0.01:  # 1 - 3/2 = -0.5
            return 'one_minus_quotient', 'second_over_first'
        # Check for "A/B - 1" pattern: result = (a/b) - 1
        elif abs(result - (a / b - 1)) < 0.01:  # 2/3 - 1 ≈ -0.333
            return 'quotient_minus_one', 'first_over_second'
        elif abs(result - (b / a - 1)) < 0.01:  # 3/2 - 1 = 0.5
            return 'quotient_minus_one', 'second_over_first'
        # Check for "A × (1 - B)" pattern: multiplication with complement
        elif abs(result - (a * (1 - b))) < 0.01:  # 2 * (1-3) = -4
            return 'multiply_complement', 'first_times_one_minus_second'
        elif abs(result - (b * (1 - a))) < 0.01:  # 3 * (1-2) = -3
            return 'multiply_complement', 'second_times_one_minus_first'
        # Check for "A × (1 - 1/B)" pattern: acceleration by inverse multiplier
        elif b != 0 and abs(result - (a * (1 - 1/b))) < 0.01:  # 2 * (1 - 1/3) ≈ 1.33
            return 'multiply_inverse_complement', 'first_times_one_minus_inv_second'
        elif a != 0 and abs(result - (b * (1 - 1/a))) < 0.01:  # 3 * (1 - 1/2) = 1.5
            return 'multiply_inverse_complement', 'second_times_one_minus_inv_first'
        else:
            # Check for "A × B × constant" pattern
            # Test with second set of values to verify constant multiplier
            test_vals2 = [5.0, 7.0]
            ctx2 = {name: val for name, val in zip(inputs, test_vals2)}
            try:
                result2 = param_value.compute(ctx2)
                product1 = a * b  # 2 * 3 = 6
                product2 = test_vals2[0] * test_vals2[1]  # 5 * 7 = 35
                if abs(product1) > 0.01 and abs(product2) > 0.01:
                    k1 = result / product1
                    k2 = result2 / product2
                    if abs(k1 - k2) < 0.01 and abs(k1) > 0.01:
                        # Consistent multiplier found
                        return 'multiply_constant_2input', k1
            except Exception:
                pass
            
            # Check for "(A - B) / constant" or "(A - B) × constant" patterns
            try:
                diff1_ab = a - b  # 2 - 3 = -1
                diff2_ab = test_vals2[0] - test_vals2[1]  # 5 - 7 = -2
                
                if abs(diff1_ab) > 0.01 and abs(diff2_ab) > 0.01:
                    # Check if result = (A - B) * constant
                    k1 = result / diff1_ab
                    k2 = result2 / diff2_ab
                    if abs(k1 - k2) < 0.01 and abs(k1) > 0.01:
                        return 'diff_first_second_times_constant', k1
                
                diff1_ba = b - a  # 3 - 2 = 1
                diff2_ba = test_vals2[1] - test_vals2[0]  # 7 - 5 = 2
                
                if abs(diff1_ba) > 0.01 and abs(diff2_ba) > 0.01:
                    k1 = result / diff1_ba
                    k2 = result2 / diff2_ba
                    if abs(k1 - k2) < 0.01 and abs(k1) > 0.01:
                        return 'diff_second_first_times_constant', k1
            except Exception:
                pass
            
            return 'complex', None

    else:
        # Multi-input: check if it's a sum or product
        expected_sum = sum(test_vals)
        if abs(result - expected_sum) < 0.01:
            return 'sum', None

        # Check product (for 3+ inputs)
        expected_product = 1.0
        for v in test_vals:
            expected_product *= v
        if abs(result - expected_product) < 0.01:
            return 'multiply', None

        # Check subtraction chain: A - B - C - ...
        # First value minus all others
        expected_subtract = test_vals[0]
        for v in test_vals[1:]:
            expected_subtract -= v
        if abs(result - expected_subtract) < 0.01:
            return 'subtract_chain', None

        # For 3 inputs, check common compound patterns
        if n == 3:
            a, b, c = test_vals[0], test_vals[1], test_vals[2]  # 2, 3, 4
            
            # A × (B - C): e.g., Deaths × (LifeExp - MeanAge)
            if abs(result - (a * (b - c))) < 0.01:  # 2 * (3-4) = -2
                return 'first_times_diff_of_second_third', None
            if abs(result - (a * (c - b))) < 0.01:  # 2 * (4-3) = 2
                return 'first_times_diff_of_third_second', None
            if abs(result - (b * (a - c))) < 0.01:  # 3 * (2-4) = -6
                return 'second_times_diff_of_first_third', None
            if abs(result - (b * (c - a))) < 0.01:  # 3 * (4-2) = 6
                return 'second_times_diff_of_third_first', None
            if abs(result - (c * (a - b))) < 0.01:  # 4 * (2-3) = -4
                return 'third_times_diff_of_first_second', None
            if abs(result - (c * (b - a))) < 0.01:  # 4 * (3-2) = 4
                return 'third_times_diff_of_second_first', None
            
            # A × (B + C): e.g., Rate × (CostA + CostB)
            if abs(result - (a * (b + c))) < 0.01:  # 2 * (3+4) = 14
                return 'first_times_sum_of_others', None
            if abs(result - (b * (a + c))) < 0.01:  # 3 * (2+4) = 18
                return 'second_times_sum_of_others', None
            if abs(result - (c * (a + b))) < 0.01:  # 4 * (2+3) = 20
                return 'third_times_sum_of_others', None
            
            # (A - B) × C: Similar but different grouping
            if abs(result - ((a - b) * c)) < 0.01:  # (2-3) * 4 = -4
                return 'diff_of_first_second_times_third', None
            if abs(result - ((a + b) * c)) < 0.01:  # (2+3) * 4 = 20
                return 'sum_of_first_second_times_third', None
            
            # A × B × C (triple product) - already covered by 'multiply' above
            
            # A / (B - C) or A / (B + C)
            if abs(b - c) > 0.01 and abs(result - (a / (b - c))) < 0.01:
                return 'first_over_diff_of_second_third', None
            if abs(result - (a / (b + c))) < 0.01:
                return 'first_over_sum_of_second_third', None
            
            # (A / B) / C and (B / A) / C patterns - common for comparing ratios
            if abs(a) > 0.01 and abs(b) > 0.01 and abs(c) > 0.01:
                if abs(result - ((a / b) / c)) < 0.01:
                    return 'first_over_second_over_third', None
                if abs(result - ((b / a) / c)) < 0.01:
                    return 'second_over_first_over_third', None
                if abs(result - ((a / c) / b)) < 0.01:
                    return 'first_over_third_over_second', None
                if abs(result - ((b / c) / a)) < 0.01:
                    return 'second_over_third_over_first', None
                if abs(result - ((c / a) / b)) < 0.01:
                    return 'third_over_first_over_second', None
                if abs(result - ((c / b) / a)) < 0.01:
                    return 'third_over_second_over_first', None

        # For 4 inputs, check common compound patterns
        if n == 4:
            a, b, c, d = test_vals[0], test_vals[1], test_vals[2], test_vals[3]  # 2, 3, 4, 5
            
            # A × (B - C) × D: common economic calculation (e.g., Deaths × YLL × Value)
            # Test all permutations of which input is multiplier vs diff operands vs final multiplier
            if abs(result - (a * (b - c) * d)) < 0.01:  # 2 * (3-4) * 5 = -10
                return 'first_times_diff_of_second_third_times_fourth', None
            if abs(result - (a * (c - b) * d)) < 0.01:  # 2 * (4-3) * 5 = 10
                return 'first_times_diff_of_third_second_times_fourth', None
            if abs(result - (b * (a - c) * d)) < 0.01:  # 3 * (2-4) * 5 = -30
                return 'second_times_diff_of_first_third_times_fourth', None
            if abs(result - (b * (c - a) * d)) < 0.01:  # 3 * (4-2) * 5 = 30
                return 'second_times_diff_of_third_first_times_fourth', None
            if abs(result - (a * (b - d) * c)) < 0.01:  # 2 * (3-5) * 4 = -16
                return 'first_times_diff_of_second_fourth_times_third', None
            if abs(result - (a * (d - b) * c)) < 0.01:  # 2 * (5-3) * 4 = 16
                return 'first_times_diff_of_fourth_second_times_third', None
            
            # A × (B + C) × D: similar but with sum
            if abs(result - (a * (b + c) * d)) < 0.01:  # 2 * (3+4) * 5 = 70
                return 'first_times_sum_of_second_third_times_fourth', None
            if abs(result - (b * (a + c) * d)) < 0.01:  # 3 * (2+4) * 5 = 90
                return 'second_times_sum_of_first_third_times_fourth', None

        # Check for "multiply with constant" for 3+ inputs
        # Test with different values to verify constant multiplier
        product1 = 1.0
        for v in test_vals:
            product1 *= v  # e.g., 2 * 3 * 4 = 24

        if abs(product1) > 0.01:
            test_vals2 = [5.0, 7.0, 11.0][:n]  # Use first n values
            ctx2 = {name: val for name, val in zip(inputs, test_vals2)}
            try:
                result2 = param_value.compute(ctx2)
                product2 = 1.0
                for v in test_vals2:
                    product2 *= v

                if abs(product2) > 0.01:
                    k1 = result / product1
                    k2 = result2 / product2
                    if abs(k1 - k2) < 0.01 and abs(k1) > 0.01 and abs(k1 - 1.0) > 0.01:
                        # Consistent multiplier found (not just 1.0)
                        return 'multiply_constant_multi', k1
            except Exception:
                pass

        return 'complex', None


def extract_lambda_body_from_file(param_name: str, params_file: Path) -> str | None:
    """Extract the lambda body from parameters.py for a given parameter."""
    content = params_file.read_text(encoding="utf-8")

    # Find the parameter definition start
    start_pattern = rf'{param_name}\s*=\s*Parameter\('
    start_match = re.search(start_pattern, content)
    if not start_match:
        return None

    start = start_match.start()

    # Find matching closing paren by counting depth
    depth = 0
    end = start
    for i, c in enumerate(content[start:], start):
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    param_def = content[start:end]

    # Find compute=lambda ctx: ... pattern
    compute_match = re.search(
        r'compute\s*=\s*lambda\s+ctx\s*:\s*(.+?)(?=,\s*\n\s*\)|$)',
        param_def,
        re.DOTALL
    )
    if compute_match:
        body = compute_match.group(1).strip()
        body = body.rstrip(',').strip()
        return body

    return None


def lambda_to_sympy_latex(lambda_body: str, var_names: list[str]) -> str | None:
    """Legacy stub - kept for backward compatibility. Use formula_to_latex instead."""
    return None


def formula_to_latex(formula: str, parameters: dict, lhs: str) -> str | None:
    """Convert a formula string to LaTeX by substituting param names with latex_symbols.

    Uses placeholder tokens to protect latex_symbols from being mangled by
    subsequent math-syntax transformations (^, /, *, etc.).
    """
    import re as _re

    if not formula:
        return None

    # Skip formulas that are purely prose descriptions
    if any(phrase in formula.lower() for phrase in ['phase 1:', 'phase 2:', 'for t=']):
        return None

    # Strip trailing prose after comma+space+"where" (keep the math part)
    if ', where ' in formula:
        formula = formula[:formula.index(', where ')]

    # Strip trailing prose after semicolons
    if '; ' in formula:
        formula = formula[:formula.index('; ')]

    s = formula

    # Step 0: Replace param names with numbered placeholders, store latex_symbols for later
    placeholders = {}  # <<N>> -> latex_symbol
    param_names = []
    for name_key, meta in parameters.items():
        val = meta['value'] if isinstance(meta, dict) else meta
        sym = getattr(val, 'latex_symbol', None)
        if sym:
            param_names.append((name_key, sym))
    param_names.sort(key=lambda x: len(x[0]), reverse=True)

    counter = 0
    for name_key, sym in param_names:
        if name_key in s:
            placeholder = f'\x00{counter}\x00'
            placeholders[placeholder] = sym
            s = s.replace(name_key, placeholder)
            counter += 1

    # Normalize multiplication/division operators
    s = s.replace('\u00d7', '*')  # ×
    s = s.replace('\u00f7', '/')  # ÷
    s = s.replace(' x ', '*')     # informal "x" multiplication

    # Step 1: Functions (min, max, ln) - convert BEFORE other transforms
    # so parentheses inside are handled correctly
    def _convert_functions(s):
        result = []
        i = 0
        while i < len(s):
            matched = False
            for func in ['min', 'max', 'ln']:
                if s[i:i + len(func) + 1] == func + '(' and (i == 0 or not s[i - 1].isalpha()):
                    depth = 0
                    j = i + len(func)
                    while j < len(s):
                        if s[j] == '(':
                            depth += 1
                        elif s[j] == ')':
                            depth -= 1
                            if depth == 0:
                                break
                        j += 1
                    inner = s[i + len(func) + 1:j]
                    result.append(f'\\{func}\\left({inner}\\right)')
                    i = j + 1
                    matched = True
                    break
            if not matched:
                result.append(s[i])
                i += 1
        return ''.join(result)

    s = _convert_functions(s)

    # Step 2: Convert ^(expr) -> ^{expr} BEFORE touching / so exponent internals are protected
    s = _re.sub(r'\^\s*\(', '^(', s)  # normalize "^ (" to "^("

    def _convert_carets(s):
        result = []
        i = 0
        while i < len(s):
            if s[i] == '^' and i + 1 < len(s) and s[i + 1] == '(':
                depth = 0
                j = i + 1
                while j < len(s):
                    if s[j] == '(':
                        depth += 1
                    elif s[j] == ')':
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                exponent = s[i + 2:j]
                result.append('^{')
                result.append(exponent)
                result.append('}')
                i = j + 1
            elif s[i] == '^' and i + 1 < len(s) and (s[i + 1].isdigit() or s[i + 1] == '-'):
                j = i + 1
                if s[j] == '-':
                    j += 1
                while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                    j += 1
                result.append('^{')
                result.append(s[i + 1:j])
                result.append('}')
                i = j
            else:
                result.append(s[i])
                i += 1
        return ''.join(result)

    s = _convert_carets(s)

    # Step 3: Convert * to \times (but not inside ^{} or function args)
    s = s.replace('*', r' \times ')

    # Step 4: Convert / to \frac{}{}
    def _convert_divs(s):
        r"""Convert A / B to \\frac{A}{B}.

        Handles: (expr)/(expr), \\func\\left(...)\\right) / same, token/token.
        """
        def _replace_paren_frac(m):
            return f'\\frac{{{m.group(1)}}}{{{m.group(2)}}}'

        # \left(...\right) / \left(...\right)
        prev = None
        while prev != s:
            prev = s
            s = _re.sub(r'\\left\(([^()]*)\\\right\)\s*/\s*\\left\(([^()]*)\\\right\)', _replace_paren_frac, s)
            s = _re.sub(r'\(([^()]*)\)\s*/\s*\(([^()]*)\)', _replace_paren_frac, s)

        # \func\left(...\right) / \func\left(...\right)  (e.g. \ln\left(A\right) / \ln\left(B\right))
        func_token = r'\\[a-z]+\\left\([^()]*\\right\)'
        s = _re.sub(
            f'({func_token})\\s*/\\s*({func_token})',
            lambda m: f'\\frac{{{m.group(1)}}}{{{m.group(2)}}}',
            s
        )

        # placeholder / placeholder or number/number
        token = r'(?:\x00\d+\x00|[\d.]+[BMKTbmkt]?)'
        s = _re.sub(
            f'({token})\\s*/\\s*({token})',
            lambda m: f'\\frac{{{m.group(1)}}}{{{m.group(2)}}}',
            s
        )
        return s

    s = _convert_divs(s)

    # Step 5: Convert remaining bare uppercase abbreviations to \text{}
    s = _re.sub(r'\b([A-Z][A-Z_]{2,})\b', lambda m: r'\text{' + m.group(1).replace('_', r'\_') + '}', s)

    # Step 6: Substitute placeholders back to latex_symbols
    for placeholder, sym in placeholders.items():
        s = s.replace(placeholder, sym)

    # Step 7: Wrap parens containing \frac with \left( \right) for proper sizing
    # Use balanced-brace matching since frac contents can contain nested {}
    def _add_left_right(s):
        result = []
        i = 0
        while i < len(s):
            if s[i] == '(' and s[i+1:i+6] == r'\frac':
                # Find matching close paren
                depth = 0
                j = i
                while j < len(s):
                    if s[j] == '(':
                        depth += 1
                    elif s[j] == ')':
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                inner = s[i+1:j]
                result.append(r'\left(')
                result.append(inner)
                result.append(r'\right)')
                i = j + 1
            else:
                result.append(s[i])
                i += 1
        return ''.join(result)
    s = _add_left_right(s)

    # Clean up whitespace
    s = _re.sub(r'\s+', ' ', s).strip()

    return f"{lhs} = {s}"


def round_to_n_sigfigs(value: float, n: int = 3) -> str:
    """Round a value to n significant figures and format cleanly."""
    if value == 0:
        return "0"
    # Use general format with n significant figures
    formatted = f"{value:.{n}g}"
    # Clean up scientific notation if present
    if 'e' in formatted.lower():
        # Convert back to regular notation if reasonable
        return f"{float(formatted):.{n-1}f}".rstrip('0').rstrip('.')
    return formatted


def format_latex_value(value: float, unit: str) -> str:
    """Format a numeric value for LaTeX display with proper units and scaling (3 sig figs)."""
    is_currency = "USD" in unit or "usd" in unit or "dollar" in unit.lower()
    is_percentage = "%" in unit or "percent" in unit.lower() or "rate" in unit.lower()
    is_in_billions = "billion" in unit.lower()

    abs_val = abs(value)

    if is_currency:
        if is_in_billions:
            if abs_val >= 1000:
                scaled = value / 1000
                return f"\\${round_to_n_sigfigs(scaled, 3)}T"
            elif abs_val >= 1:
                return f"\\${round_to_n_sigfigs(value, 3)}B"
            else:
                scaled = value * 1000
                return f"\\${round_to_n_sigfigs(scaled, 3)}M"
        else:
            # Raw USD value
            if abs_val >= 1e12:
                return f"\\${round_to_n_sigfigs(value/1e12, 3)}T"
            elif abs_val >= 1e9:
                return f"\\${round_to_n_sigfigs(value/1e9, 3)}B"
            elif abs_val >= 1e6:
                return f"\\${round_to_n_sigfigs(value/1e6, 3)}M"
            elif abs_val >= 1e3:
                return f"\\${round_to_n_sigfigs(value/1e3, 3)}K"
            elif abs_val >= 1:
                return f"\\${round_to_n_sigfigs(value, 3)}"
            else:
                # Values < $1: preserve 3 sig figs
                return f"\\${round_to_n_sigfigs(value, 3)}"
    elif is_percentage:
        # "rate" unit = decimal ratio that always needs *100 conversion (e.g., 2.72 → 272%)
        # "percent"/"%" = may already be percentage value if > 1
        is_rate_unit = "rate" in unit.lower()
        if is_rate_unit or abs_val <= 1:
            return f"{round_to_n_sigfigs(value * 100, 3)}\\%"
        else:
            return f"{round_to_n_sigfigs(value, 3)}\\%"
    else:
        # Non-currency, non-percentage
        if abs_val >= 1e12:
            return f"{round_to_n_sigfigs(value/1e12, 3)}T"
        elif abs_val >= 1e9:
            return f"{round_to_n_sigfigs(value/1e9, 3)}B"
        elif abs_val >= 1e6:
            return f"{round_to_n_sigfigs(value/1e6, 3)}M"
        elif abs_val >= 1e3:
            # Use thousands separator with 3 sig figs
            rounded = round_to_n_sigfigs(value, 3)
            # Add thousands separators
            if '.' in rounded:
                int_part, dec_part = rounded.split('.')
                int_part = f"{int(int_part):,}".replace(',', '{,}')
                return f"{int_part}.{dec_part}"
            else:
                return f"{int(rounded):,}".replace(',', '{,}')
        elif abs_val >= 1:
            # 3 significant figures for values >= 1
            return round_to_n_sigfigs(value, 3)
        else:
            # 3 significant figures for values < 1
            return round_to_n_sigfigs(value, 3)


def create_short_label(display_name: str, param_name: str = "") -> str:
    """
    Create a short LaTeX label from a display name or parameter name.

    Strategy: Keep labels readable and domain-specific, not overly abbreviated.
    Use common medical/economic terms that are recognizable.
    """
    # Domain-specific terms that should NOT be abbreviated (recognizable as-is)
    preserve_words = {
        'diabetes', 'alzheimer', 'heart', 'cancer', 'stroke', 'obesity',
        'combat', 'terror', 'state', 'ptsd', 'refugee', 'veteran',
        'platform', 'staff', 'trial', 'water', 'energy', 'supply',
    }

    # Abbreviations only for very long words
    abbrevs = {
        'infrastructure': 'infra',
        'transportation': 'transport',
        'communications': 'comms',
        'environmental': 'environ',
        'military': 'military',
        'healthcare': 'health',
        'research': 'R\\&D',
        'population': 'pop',
        'lobbying': 'lobby',
        'referendum': 'referendum',
        'regulatory': 'regulatory',
        'community': 'community',
        'maintenance': 'maint',
        'subsidies': 'subsidy',
        'shipping': 'shipping',
        'currency': 'currency',
        'capital': 'capital',
        'opportunity': 'opp cost',
        'indirect': 'indirect',
        'direct': 'direct',
    }

    display_lower = display_name.lower()

    # First check for known abbreviations
    for full, short in abbrevs.items():
        if full in display_lower:
            return f"\\text{{{short}}}"

    # Check for words to preserve as-is
    for word in preserve_words:
        if word in display_lower:
            return f"\\text{{{word}}}"

    # Extract from parameter name if possible (e.g., ACLED_CONFLICT_DEATHS -> "ACLED")
    if param_name:
        parts = param_name.split('_')
        # Look for source indicators (ACLED, GTD, UCDP, WHO, CDC, UN, EPA)
        for part in parts:
            if part in ['ACLED', 'GTD', 'UCDP', 'WHO', 'CDC', 'UN', 'EPA']:
                return f"\\text{{{part}}}"

    # Extract first significant word from display name
    words = display_name.split()
    # Skip common prefixes
    skip_words = {'annual', 'global', 'total', 'us', 'the', 'a', 'an', 'per', 'of', 'and'}
    significant_words = [w for w in words if w.lower() not in skip_words and len(w) > 2]

    if len(significant_words) >= 1:
        # Use first significant word, only abbreviate if very long
        first_word = significant_words[0]
        if len(first_word) > 10:
            return f"\\text{{{first_word[:8]}}}"
        return f"\\text{{{first_word}}}"

    return f"\\text{{{display_name[:8]}}}"


def create_latex_variable_name(
    param_name: str, 
    display_name: str = "",
    sibling_names: list[str] | None = None
) -> str:
    """
    Create a meaningful LaTeX variable name from parameter info.

    Following patterns from hardcoded equations:
    - OPEX_{total}, Cost_{combat}, Deaths_{total}
    - PeaceDividend_{infra}, Benefit_{RD}
    - TotalWarCost, DirectCosts

    Args:
        param_name: Parameter name like DFDA_ANNUAL_OPEX
        display_name: Human-readable name like "DFDA Annual Operating Expenses"
        sibling_names: Optional list of sibling parameter names (for finding distinguishing suffix)
    """
    # First, try to extract a distinguishing suffix if this is part of a group
    distinguishing = extract_distinguishing_suffix(param_name, sibling_names)
    if distinguishing:
        # Use the distinguishing suffix as the primary subscript
        # Still need to find the main concept for the base name
        pass  # Will use distinguishing below
    # Domain-specific main concepts - USE LIST for priority ordering
    # More specific terms should come FIRST
    main_concepts = [
        ('threshold_pct', 'Threshold'),  # Activism threshold -> Threshold
        ('reduction_pct', 'Reduction'),  # Cost reduction -> Reduction
        ('activism', 'Activism'),        # Activism threshold
        ('treasury', 'Treasury'),  # More specific than 'trial'
        ('subsid', 'Subsidies'),   # Trial subsidies -> Subsidies
        ('fundable', 'Fundable'),  # Patients fundable -> Fundable
        ('multiplier', 'Multiplier'),  # Before cost to catch "cost increase multiplier"
        ('increase', 'Increase'),  # Cost increase
        ('cost', 'Cost'),
        ('opex', 'OPEX'),
        ('capex', 'CAPEX'),
        ('death', 'Deaths'),
        ('daly', 'DALYs'),
        ('benefit', 'Benefit'),
        ('saving', 'Savings'),
        ('funding', 'Funding'),
        ('dividend', 'Dividend'),
        ('roi', 'ROI'),
        ('ratio', 'Ratio'),
        ('rate', 'Rate'),
        ('capacity', 'Capacity'),
        ('population', 'Population'),
        ('delay', 'Delay'),
        ('time', 'Time'),
        ('probability', 'Probability'),
        ('damage', 'Damage'),
        ('disruption', 'Disruption'),
        ('burden', 'Burden'),
        ('patient', 'Patients'),
        ('trial', 'Trials'),
        ('lives', 'Lives'),
        ('qaly', 'QALYs'),
        ('yll', 'YLL'),
        ('yld', 'YLD'),
        ('hour', 'Hours'),
        ('spending', 'Spending'),
        ('loss', 'Loss'),
        ('campaign', 'Campaign'),
        ('bloc', 'VotingBloc'),
    ]

    # Priority subscripts - distinguishing modifiers (checked first, only one picked)
    # Order matters! Check longer strings first to avoid substring matches
    priority_subscripts = [
        # Complex multi-word patterns first
        ('direct_funding_roi_trial_capacity_plus_efficacy_lag', 'direct_funding'),
        ('trial_capacity_plus_efficacy_lag', 'max'),  # Combined max scenario
        ('platform_maintenance', 'platform'),  # DFDA OPEX components
        ('active_combat', 'combat'),
        ('state_violence', 'state'),
        ('terror_attacks', 'terror'),
        ('lost_human_capital', 'human_cap'),
        ('lost_economic_growth', 'econ_growth'),
        ('human_capital', 'human_cap'),
        ('economic_growth', 'econ_growth'),
        # Infrastructure damage types
        ('damage_transportation', 'transport'),
        ('damage_energy', 'energy'),
        ('damage_communications', 'comms'),
        ('damage_water', 'water'),
        ('damage_education', 'edu'),
        ('damage_healthcare', 'health'),
        # Trade disruption types
        ('disruption_shipping', 'shipping'),
        ('disruption_currency', 'currency'),
        ('disruption_capital', 'capital'),
        ('disruption_opportunity', 'opp'),
        # Two-word patterns
        ('per_capita', 'percap'),
        ('mental_health', 'mental'),
        ('chronic_disease', 'chronic'),
        ('pre_1962', 'pre62'),
        ('war_total', 'war'),
        # OPEX component types (for DFDA)
        ('opex_platform', 'platform'),
        ('opex_staff', 'staff'),
        ('opex_infrastructure', 'infra'),
        ('opex_regulatory', 'reg'),
        ('opex_community', 'community'),
        # Single words - infrastructure types
        ('transportation', 'transport'),
        ('communications', 'comms'),
        ('platform', 'platform'),
        ('staff', 'staff'),
        ('regulatory', 'reg'),
        ('community', 'community'),
        ('education', 'edu'),
        # Cost/damage categories
        ('symptomatic', 'sympt'),
        ('indirect', 'indirect'),  # Check before 'direct'
        ('direct', 'direct'),
        ('gross', 'gross'),
        ('net', 'net'),
        ('human', 'human'),
        ('infrastructure', 'infra'),
        ('infra', 'infra'),
        ('combat', 'combat'),
        ('terror', 'terror'),
        ('state', 'state'),
        ('trade', 'trade'),
        ('military', 'mil'),
        ('environmental', 'env'),
        ('veteran', 'vet'),
        ('refugee', 'ref'),
        ('ptsd', 'PTSD'),
        ('current', 'curr'),
        ('pre1962', 'pre62'),
        ('1980', '80s'),
        ('lost', 'lost'),
        # Disease-specific
        ('alzheimer', 'alz'),
        ('cancer', 'cancer'),
        ('diabetes', 'diab'),
        ('heart', 'heart'),
        ('stroke', 'stroke'),
        ('obesity', 'obes'),
        # Energy/utility
        ('energy', 'energy'),
        ('water', 'water'),
        ('shipping', 'shipping'),
        ('currency', 'currency'),
        ('capital', 'capital'),
        ('opportunity', 'opp'),
        # Source-specific
        ('dfda', 'DFDA'),
        ('campaign', 'camp'),
        ('opex', 'opex'),
        ('societal', 'soc'),
    ]

    # Secondary subscripts - context modifiers
    secondary_subscripts = {
        'total': 'total',
        'annual': 'ann',
        'daily': 'daily',
        'global': 'global',
        'research': 'RD',
        'rd': 'RD',
        'peace': 'peace',
        'war': 'war',
        'dfda': 'DFDA',
        'treaty': 'treaty',
        'disease': 'dis',
        'health': 'health',
        'npv': 'NPV',
        'pv': 'PV',
        'expected': 'exp',
    }

    param_lower = param_name.lower()
    display_lower = display_name.lower() if display_name else param_lower

    # Find main concept (main_concepts is a list of tuples for priority ordering)
    main = None
    for key, val in main_concepts:
        if key in param_lower or key in display_lower:
            main = val
            break

    # Find ONE priority subscript (the distinguishing one)
    # priority_subscripts is a list of tuples to control order
    priority_sub = None
    for key, val in priority_subscripts:
        if key in param_lower:
            priority_sub = val
            break

    # Find secondary subscript(s)
    secondary_subs = []
    for key, val in secondary_subscripts.items():
        if key in param_lower and val != priority_sub:
            secondary_subs.append(val)

    # Build the LaTeX name
    if main:
        subs = []
        # If we have a distinguishing suffix from sibling analysis, use it preferentially
        if distinguishing and distinguishing not in (priority_sub or ''):
            subs.append(distinguishing)
        elif priority_sub:
            subs.append(priority_sub)
        # Add at most one secondary subscript
        if secondary_subs and len(subs) < 2:
            subs.append(secondary_subs[0])

        if subs:
            sub_str = ','.join(subs)
            return f"{main}_{{{sub_str}}}"
        return main
    else:
        # Fall back to creating a meaningful name from param parts
        # Use known acronyms and full words, not truncation
        parts = param_name.split('_')

        # Known acronyms to preserve
        acronyms = {'US', 'DIH', 'DFDA', 'ROI', 'NPV', 'PV', 'GDP', 'VSL', 'FDA', 'R&D'}
        # Words to use as subscripts
        sub_words = {'annual', 'total', 'current', 'global', 'major', 'simple', 'daily'}

        # Build main word(s) and subscript
        main_parts = []
        sub_parts = []
        for part in parts:
            part_upper = part.upper()
            part_lower = part.lower()
            if part_upper in acronyms:
                main_parts.append(part_upper.replace('R&D', 'RD'))
            elif part_lower in sub_words:
                sub_parts.append(part.title())
            elif not main_parts:  # Use first non-acronym, non-sub word
                main_parts.append(part.title())

        main_text = ''.join(main_parts) if main_parts else parts[0].title()
        if sub_parts:
            return f"{main_text}_{{{sub_parts[0].lower()}}}"
        return main_text


def generate_expanded_latex(
    param_name: str,
    param_value: Any,
    parameters: Dict[str, Dict[str, Any]],
    params_file: Optional[Path] = None,
    max_depth: int = 10,
    _depth: int = 0,
    _visited: set | None = None,
    _memoized: dict | None = None,
    _globally_shown: set | None = None
) -> str | None:
    r"""
    Generate FULLY EXPANDED LaTeX equation with recursive derivation of all calculated inputs.

    This creates a complete derivation chain showing how every intermediate value
    is calculated, all the way down to leaf parameters (external sources/definitions).

    Uses de-duplication: each sub-expression is fully derived only once. Subsequent
    references show just the single-level equation (no repeated "where" clauses).

    Example output for DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED:

    \begin{aligned}
    Lives_{saved} &= Deaths_{daily} \times Years_{shift} \times 365 \times 0.919 \\
                  &= 190K \times 207 \times 365 \times 0.919 = 184.6M \\[0.5em]
    \text{where } Years_{shift} &= Years_{accel} + Years_{efficacy} \\
                                &= 197 + 10 = 207 \\[0.5em]
    \text{where } Years_{accel} &= \frac{Queue_{current} - Queue_{dfda}}{Rate} \\
                                &= \frac{451 - 36}{2.2} = 197
    \end{aligned}

    Args:
        param_name: Name of the parameter
        param_value: Parameter object with metadata
        parameters: Full parameters dict for looking up input values
        params_file: Path to parameters.py for lambda extraction
        max_depth: Maximum recursion depth (prevents infinite loops)
        _depth: Current recursion depth (internal use)
        _visited: Set of already-visited params (cycle detection, internal use)
        _memoized: Cache of already-generated LaTeX (prevents duplication, internal use)
        _globally_shown: Tracks params already fully derived (de-duplication, internal use)

    Returns:
        Fully expanded LaTeX string with derivation chain, or None if cannot generate
    """
    if _visited is None:
        _visited = set()
    if _memoized is None:
        _memoized = {}
    if _globally_shown is None:
        _globally_shown = set()

    # De-duplication: if already fully derived elsewhere, return single-level only
    if _depth > 0 and param_name in _globally_shown:
        single = generate_auto_latex(param_name, param_value, parameters, params_file)
        if single is None:
            single = getattr(param_value, 'latex', None)
        return single

    # Check memoization cache first (but only at depth > 0 to avoid caching root)
    if _depth > 0 and param_name in _memoized:
        return _memoized[param_name]
    
    # Cycle detection
    if param_name in _visited:
        return None
    _visited = _visited | {param_name}
    
    # Depth limit
    if _depth > max_depth:
        return None
    
    # Generate equation for this level
    this_level = generate_auto_latex(param_name, param_value, parameters, params_file)
    if this_level is None:
        # Try to use hardcoded latex if available
        this_level = getattr(param_value, 'latex', None)
    
    if this_level is None:
        return None
    
    # Find calculated inputs that need expansion
    inputs = getattr(param_value, 'inputs', None) or []
    calculated_inputs = []
    
    for inp_name in inputs:
        inp_meta = parameters.get(inp_name, {})
        inp_value = inp_meta.get('value')
        if inp_value is None:
            continue
        
        # Check if this input is itself calculated (has inputs and compute)
        has_inputs = hasattr(inp_value, 'inputs') and inp_value.inputs
        has_compute = hasattr(inp_value, 'compute') and inp_value.compute
        
        if has_inputs and has_compute:
            calculated_inputs.append((inp_name, inp_value))
    
    # If no calculated inputs or at max depth, return single equation
    if not calculated_inputs or _depth >= max_depth:
        # Cache and mark as shown
        _memoized[param_name] = this_level
        _globally_shown.add(param_name)
        return this_level
    
    # Build multi-step derivation as separate blocks.
    # Each block is a self-contained equation. Callers split on LATEX_BLOCK_SEP
    # and wrap each in its own $$ delimiters, allowing page breaks between them.
    blocks = []

    # Main equation is the first block
    blocks.append(this_level)

    # Track which sub-derivations we've already added to avoid duplicates
    added_derivations = set()
    # Track block content to deduplicate identical equations from different branches
    # (e.g., Funding_{treaty} appearing as input to Payout, Political, AND Treasury)
    seen_blocks = {this_level}

    # Recursively expand each calculated input
    for inp_name, inp_value in calculated_inputs:
        # Skip if we've already added this derivation
        if inp_name in added_derivations:
            continue

        sub_latex = generate_expanded_latex(
            inp_name, inp_value, parameters, params_file,
            max_depth=max_depth,
            _depth=_depth + 1,
            _visited=_visited,
            _memoized=_memoized,
            _globally_shown=_globally_shown
        )

        if sub_latex:
            added_derivations.add(inp_name)

            if LATEX_BLOCK_SEP in sub_latex:
                # Sub-derivation is itself multi-block.
                # First sub-block is the sub-equation, rest are its "where" clauses.
                # Deduplicate blocks that already appeared from other branches.
                for block in sub_latex.split(LATEX_BLOCK_SEP):
                    block = block.strip()
                    if block and block not in seen_blocks:
                        seen_blocks.add(block)
                        blocks.append(block)
            elif r'\begin{aligned}' in sub_latex:
                inner = sub_latex.replace(r'\begin{aligned}', '').replace(r'\end{aligned}', '').strip()
                if inner not in seen_blocks:
                    seen_blocks.add(inner)
                    blocks.append(inner)
            else:
                if sub_latex not in seen_blocks:
                    seen_blocks.add(sub_latex)
                    blocks.append(sub_latex)

    if len(blocks) == 1:
        result = blocks[0]
    else:
        result = LATEX_BLOCK_SEP.join(blocks)

    # Cache the result and mark as globally shown
    _memoized[param_name] = result
    _globally_shown.add(param_name)
    return result


def generate_auto_latex(
    param_name: str,
    param_value: Any,
    parameters: Dict[str, Dict[str, Any]],
    params_file: Optional[Path] = None
) -> str | None:
    r"""
    Generate LaTeX equation from parameter metadata (single level, no expansion).

    Strategy:
    1. First try sympy-based conversion (parses actual compute lambda)
    2. Fall back to inference-based approach for simple operations
    3. Return None for truly complex cases (hardcoded latex used instead)

    Creates equations like:
    - Sum: \text{Total} = \underbrace{\$327B}_{\text{Diabetes}} + \underbrace{\$355B}_{\text{Alzheimer's}} = \$1.253T
    - Product: \text{Cost} = 233{,}600 \times \$10M = \$2.34T
    - Ratio: \text{Multiplier} = \frac{48.8M}{1.9M} = 25.7\times
    - Complex: Uses sympy to generate proper fractions, exponents, etc.

    Args:
        param_name: Name of the parameter
        param_value: Parameter object with metadata
        parameters: Full parameters dict for looking up input values
        params_file: Path to parameters.py for lambda extraction (optional)

    Returns:
        LaTeX string or None if cannot generate
    """
    # Prefer hardcoded LaTeX when provided
    hardcoded_latex = getattr(param_value, 'latex', None)
    if hardcoded_latex:
        return hardcoded_latex

    # Check if this is a calculated parameter with inputs and compute
    if not hasattr(param_value, 'inputs') or not param_value.inputs:
        return None
    if not hasattr(param_value, 'compute') or not param_value.compute:
        return None

    inputs = param_value.inputs
    result_value = float(param_value)
    result_unit = getattr(param_value, 'unit', '') or ''

    # Infer operation type from compute function
    operation, order = infer_operation_from_compute(param_value, inputs)

    # Get input values and format them
    # Pass all input names as siblings so we can extract distinguishing suffixes
    input_data = []
    for inp_name in inputs:
        inp_meta = parameters.get(inp_name, {})
        inp_value = inp_meta.get('value')
        if inp_value is None:
            return None  # Can't generate if missing input

        inp_float = float(inp_value)
        inp_unit = getattr(inp_value, 'unit', '') or ''
        inp_display = getattr(inp_value, 'display_name', smart_title_case(inp_name))

        # Format the value for LaTeX
        inp_formatted = format_latex_value(inp_float, inp_unit)

        # Create short label (abbreviation from display name and param name)
        short_label = create_short_label(inp_display, inp_name)

        # Create symbolic name for traceable equations
        # Use latex_symbol if provided, otherwise auto-generate
        inp_latex_symbol = getattr(inp_value, 'latex_symbol', None)
        if inp_latex_symbol:
            inp_symbolic = inp_latex_symbol
        else:
            # Pass sibling names to find distinguishing suffixes for grouped inputs
            inp_symbolic = create_latex_variable_name(inp_name, inp_display, sibling_names=inputs)

        input_data.append({
            'name': inp_name,
            'value': inp_float,
            'formatted': inp_formatted,
            'display': inp_display,
            'short': short_label,
            'symbolic': inp_symbolic,
            'unit': inp_unit,
        })

    # Format result value
    result_formatted = format_latex_value(result_value, result_unit)

    # Get display name for creating meaningful LHS
    result_display = getattr(param_value, 'display_name', '') or smart_title_case(param_name)

    # Create short name for LHS using latex_symbol if available, otherwise auto-generate
    result_latex_symbol = getattr(param_value, 'latex_symbol', None)
    if result_latex_symbol:
        lhs_short = result_latex_symbol
    else:
        lhs_short = create_latex_variable_name(param_name, result_display)

    # For complex operations, convert formula string to LaTeX
    if operation == 'complex':
        formula = getattr(param_value, 'formula', '') or ''
        if formula and parameters:
            formula_latex = formula_to_latex(formula, parameters, lhs_short)
            if formula_latex:
                return formula_latex

    # Build equation based on inferred operation type
    # Format: LHS = Symbolic formula = Numeric values = Result
    # This makes calculations traceable AND verifiable

    if operation == 'divide' and len(input_data) == 2:
        # Division: X = A/B = num/denom = result
        if order == 'second_over_first':
            numerator = input_data[1]
            denominator = input_data[0]
        else:
            numerator = input_data[0]
            denominator = input_data[1]

        symbolic = f"\\frac{{{numerator['symbolic']}}}{{{denominator['symbolic']}}}"
        numeric = f"\\frac{{{numerator['formatted']}}}{{{denominator['formatted']}}}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'one_minus_quotient' and len(input_data) == 2:
        # 1 - (A/B): X = 1 - A/B = 1 - num/denom = result
        if order == 'second_over_first':
            numerator = input_data[1]
            denominator = input_data[0]
        else:
            numerator = input_data[0]
            denominator = input_data[1]

        symbolic = f"1 - \\frac{{{numerator['symbolic']}}}{{{denominator['symbolic']}}}"
        numeric = f"1 - \\frac{{{numerator['formatted']}}}{{{denominator['formatted']}}}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'quotient_minus_one' and len(input_data) == 2:
        # (A/B) - 1: X = A/B - 1 = num/denom - 1 = result
        if order == 'second_over_first':
            numerator = input_data[1]
            denominator = input_data[0]
        else:
            numerator = input_data[0]
            denominator = input_data[1]

        symbolic = f"\\frac{{{numerator['symbolic']}}}{{{denominator['symbolic']}}} - 1"
        numeric = f"\\frac{{{numerator['formatted']}}}{{{denominator['formatted']}}} - 1"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'multiply':
        # Multiplication: X = A × B = val1 × val2 = result
        symbolic_terms = ' \\times '.join(d['symbolic'] for d in input_data)
        numeric_terms = ' \\times '.join(d['formatted'] for d in input_data)
        latex = f"{lhs_short} = {symbolic_terms} = {numeric_terms} = {result_formatted}"

    elif operation == 'multiply_complement' and len(input_data) == 2:
        # A × (1 - B): X = A × (1 - B) = val1 × (1 - val2) = result
        if order == 'second_times_one_minus_first':
            multiplier = input_data[1]
            complement = input_data[0]
        else:
            multiplier = input_data[0]
            complement = input_data[1]

        symbolic = f"{multiplier['symbolic']} \\times (1 - {complement['symbolic']})"
        numeric = f"{multiplier['formatted']} \\times (1 - {complement['formatted']})"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'multiply_inverse_complement' and len(input_data) == 2:
        # A × (1 - 1/B): X = A × (1 - 1/B) = val1 × (1 - 1/val2) = result
        if order == 'second_times_one_minus_inv_first':
            multiplier = input_data[1]
            divisor = input_data[0]
        else:
            multiplier = input_data[0]
            divisor = input_data[1]

        symbolic = f"{multiplier['symbolic']} \\times \\left(1 - \\frac{{1}}{{{divisor['symbolic']}}}\\right)"
        numeric = f"{multiplier['formatted']} \\times \\left(1 - \\frac{{1}}{{{divisor['formatted']}}}\\right)"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'sum':
        # Addition: X = A + B + C = val1 + val2 + val3 = result
        symbolic_terms = ' + '.join(d['symbolic'] for d in input_data)
        numeric_terms = ' + '.join(d['formatted'] for d in input_data)
        latex = f"{lhs_short} = {symbolic_terms} = {numeric_terms} = {result_formatted}"

    elif operation == 'subtract' and len(input_data) == 2:
        # Subtraction: X = A - B = val1 - val2 = result
        if order == 'second_minus_first':
            first = input_data[1]
            second = input_data[0]
        else:
            first = input_data[0]
            second = input_data[1]
        symbolic = f"{first['symbolic']} - {second['symbolic']}"
        numeric = f"{first['formatted']} - {second['formatted']}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'subtract_chain' and len(input_data) >= 3:
        # Subtraction chain: X = A - B - C - ... = val1 - val2 - val3 - ... = result
        symbolic_terms = input_data[0]['symbolic']
        numeric_terms = input_data[0]['formatted']
        for d in input_data[1:]:
            symbolic_terms += f" - {d['symbolic']}"
            numeric_terms += f" - {d['formatted']}"
        latex = f"{lhs_short} = {symbolic_terms} = {numeric_terms} = {result_formatted}"

    elif operation == 'diff_first_second_times_constant' and len(input_data) == 2:
        # (A - B) × constant or (A - B) / divisor
        a, b = input_data[0], input_data[1]
        constant = float(order)
        # If constant < 1, display as division (more readable)
        if abs(constant) < 1.0 and abs(constant) > 0.001:
            divisor = round_to_n_sigfigs(1.0 / constant, 3)
            symbolic = f"\\frac{{{a['symbolic']} - {b['symbolic']}}}{{{divisor}}}"
            numeric = f"\\frac{{{a['formatted']} - {b['formatted']}}}{{{divisor}}}"
        else:
            const_formatted = round_to_n_sigfigs(constant, 3)
            symbolic = f"({a['symbolic']} - {b['symbolic']}) \\times {const_formatted}"
            numeric = f"({a['formatted']} - {b['formatted']}) \\times {const_formatted}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'diff_second_first_times_constant' and len(input_data) == 2:
        # (B - A) × constant or (B - A) / divisor
        a, b = input_data[0], input_data[1]
        constant = float(order)
        if abs(constant) < 1.0 and abs(constant) > 0.001:
            divisor = round_to_n_sigfigs(1.0 / constant, 3)
            symbolic = f"\\frac{{{b['symbolic']} - {a['symbolic']}}}{{{divisor}}}"
            numeric = f"\\frac{{{b['formatted']} - {a['formatted']}}}{{{divisor}}}"
        else:
            const_formatted = round_to_n_sigfigs(constant, 3)
            symbolic = f"({b['symbolic']} - {a['symbolic']}) \\times {const_formatted}"
            numeric = f"({b['formatted']} - {a['formatted']}) \\times {const_formatted}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'multiply_constant' and len(input_data) == 1:
        # Multiply by constant: X = A × c = val × const = result
        inp = input_data[0]
        constant = float(order)  # The constant value is stored in order parameter
        # Format constant as plain number (no units)
        const_formatted = round_to_n_sigfigs(constant, 3)
        latex = f"{lhs_short} = {inp['symbolic']} \\times {const_formatted} = {inp['formatted']} \\times {const_formatted} = {result_formatted}"

    elif operation == 'multiply_constant_2input' and len(input_data) == 2:
        # Multiply two inputs by a constant: X = A × B × c = val1 × val2 × const = result
        a, b = input_data[0], input_data[1]
        constant = float(order)  # The constant value is stored in order parameter
        const_formatted = round_to_n_sigfigs(constant, 3)
        symbolic = f"{a['symbolic']} \\times {b['symbolic']} \\times {const_formatted}"
        numeric = f"{a['formatted']} \\times {b['formatted']} \\times {const_formatted}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'multiply_constant_multi':
        # Multiply multiple inputs by a constant: X = A × B × ... × c
        constant = float(order)
        const_formatted = round_to_n_sigfigs(constant, 3)
        symbolic_terms = ' \\times '.join(d['symbolic'] for d in input_data)
        numeric_terms = ' \\times '.join(d['formatted'] for d in input_data)
        symbolic = f"{symbolic_terms} \\times {const_formatted}"
        numeric = f"{numeric_terms} \\times {const_formatted}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'divide_constant' and len(input_data) == 1:
        # Divide by constant: X = A / c = val / const = result
        inp = input_data[0]
        constant = float(order)
        const_formatted = round_to_n_sigfigs(constant, 3)
        symbolic = f"\\frac{{{inp['symbolic']}}}{{{const_formatted}}}"
        numeric = f"\\frac{{{inp['formatted']}}}{{{const_formatted}}}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'add_constant' and len(input_data) == 1:
        # Add constant: X = A + c = val + const = result
        # Handle negative constants as subtraction for cleaner display
        inp = input_data[0]
        constant = float(order)
        if constant < 0:
            # Negative constant: show as subtraction
            const_formatted = round_to_n_sigfigs(abs(constant), 3)
            latex = f"{lhs_short} = {inp['symbolic']} - {const_formatted} = {inp['formatted']} - {const_formatted} = {result_formatted}"
        else:
            const_formatted = round_to_n_sigfigs(constant, 3)
            latex = f"{lhs_short} = {inp['symbolic']} + {const_formatted} = {inp['formatted']} + {const_formatted} = {result_formatted}"

    elif operation == 'subtract_constant' and len(input_data) == 1:
        # Subtract constant: X = A - c = val - const = result
        # Handle negative constants (subtracting negative = adding)
        inp = input_data[0]
        constant = float(order)
        if constant < 0:
            # Subtracting negative: show as addition
            const_formatted = round_to_n_sigfigs(abs(constant), 3)
            latex = f"{lhs_short} = {inp['symbolic']} + {const_formatted} = {inp['formatted']} + {const_formatted} = {result_formatted}"
        else:
            const_formatted = round_to_n_sigfigs(constant, 3)
            latex = f"{lhs_short} = {inp['symbolic']} - {const_formatted} = {inp['formatted']} - {const_formatted} = {result_formatted}"

    elif operation == 'constant_minus_var' and len(input_data) == 1:
        # Constant minus variable: X = c - A = const - val = result
        inp = input_data[0]
        constant = float(order)
        if constant < 0:
            # Negative constant minus var: (-c) - A = -(c + A)
            # Show as: -c - A for clarity
            const_formatted = round_to_n_sigfigs(abs(constant), 3)
            latex = f"{lhs_short} = -{const_formatted} - {inp['symbolic']} = -{const_formatted} - {inp['formatted']} = {result_formatted}"
        else:
            const_formatted = round_to_n_sigfigs(constant, 3)
            latex = f"{lhs_short} = {const_formatted} - {inp['symbolic']} = {const_formatted} - {inp['formatted']} = {result_formatted}"

    elif operation in ('identity', 'transform') and len(input_data) == 1:
        # Single input transformation: X = A = val = result
        # BUT: Check if formula suggests a binary operation - if so, inputs metadata is incomplete
        formula = getattr(param_value, 'formula', '') or ''
        if '÷' in formula or '×' in formula or '+' in formula or '-' in formula:
            # Formula suggests binary op but only 1 input - skip auto-generation
            return None
        inp = input_data[0]
        latex = f"{lhs_short} = {inp['symbolic']} = {inp['formatted']} = {result_formatted}"

    # 3-input patterns: A × (B - C) and variations
    elif operation == 'first_times_diff_of_second_third' and len(input_data) == 3:
        # A × (B - C)
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"{a['symbolic']} \\times ({b['symbolic']} - {c['symbolic']})"
        numeric = f"{a['formatted']} \\times ({b['formatted']} - {c['formatted']})"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'first_times_diff_of_third_second' and len(input_data) == 3:
        # A × (C - B)
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"{a['symbolic']} \\times ({c['symbolic']} - {b['symbolic']})"
        numeric = f"{a['formatted']} \\times ({c['formatted']} - {b['formatted']})"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'second_times_diff_of_first_third' and len(input_data) == 3:
        # B × (A - C)
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"{b['symbolic']} \\times ({a['symbolic']} - {c['symbolic']})"
        numeric = f"{b['formatted']} \\times ({a['formatted']} - {c['formatted']})"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'second_times_diff_of_third_first' and len(input_data) == 3:
        # B × (C - A)
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"{b['symbolic']} \\times ({c['symbolic']} - {a['symbolic']})"
        numeric = f"{b['formatted']} \\times ({c['formatted']} - {a['formatted']})"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'third_times_diff_of_first_second' and len(input_data) == 3:
        # C × (A - B)
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"{c['symbolic']} \\times ({a['symbolic']} - {b['symbolic']})"
        numeric = f"{c['formatted']} \\times ({a['formatted']} - {b['formatted']})"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'third_times_diff_of_second_first' and len(input_data) == 3:
        # C × (B - A)
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"{c['symbolic']} \\times ({b['symbolic']} - {a['symbolic']})"
        numeric = f"{c['formatted']} \\times ({b['formatted']} - {a['formatted']})"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'first_times_sum_of_others' and len(input_data) == 3:
        # A × (B + C)
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"{a['symbolic']} \\times ({b['symbolic']} + {c['symbolic']})"
        numeric = f"{a['formatted']} \\times ({b['formatted']} + {c['formatted']})"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'second_times_sum_of_others' and len(input_data) == 3:
        # B × (A + C)
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"{b['symbolic']} \\times ({a['symbolic']} + {c['symbolic']})"
        numeric = f"{b['formatted']} \\times ({a['formatted']} + {c['formatted']})"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'third_times_sum_of_others' and len(input_data) == 3:
        # C × (A + B)
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"{c['symbolic']} \\times ({a['symbolic']} + {b['symbolic']})"
        numeric = f"{c['formatted']} \\times ({a['formatted']} + {b['formatted']})"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'diff_of_first_second_times_third' and len(input_data) == 3:
        # (A - B) × C
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"({a['symbolic']} - {b['symbolic']}) \\times {c['symbolic']}"
        numeric = f"({a['formatted']} - {b['formatted']}) \\times {c['formatted']}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'sum_of_first_second_times_third' and len(input_data) == 3:
        # (A + B) × C
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"({a['symbolic']} + {b['symbolic']}) \\times {c['symbolic']}"
        numeric = f"({a['formatted']} + {b['formatted']}) \\times {c['formatted']}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'first_over_diff_of_second_third' and len(input_data) == 3:
        # A / (B - C)
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"\\frac{{{a['symbolic']}}}{{{b['symbolic']} - {c['symbolic']}}}"
        numeric = f"\\frac{{{a['formatted']}}}{{{b['formatted']} - {c['formatted']}}}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'first_over_sum_of_second_third' and len(input_data) == 3:
        # A / (B + C)
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"\\frac{{{a['symbolic']}}}{{{b['symbolic']} + {c['symbolic']}}}"
        numeric = f"\\frac{{{a['formatted']}}}{{{b['formatted']} + {c['formatted']}}}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    # Division chain patterns: (A / B) / C = A / (B × C)
    elif operation == 'first_over_second_over_third' and len(input_data) == 3:
        # (A / B) / C - display as nested fraction
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"\\frac{{{a['symbolic']}}}{{{b['symbolic']} \\times {c['symbolic']}}}"
        numeric = f"\\frac{{{a['formatted']}}}{{{b['formatted']} \\times {c['formatted']}}}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'second_over_first_over_third' and len(input_data) == 3:
        # (B / A) / C
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"\\frac{{{b['symbolic']}}}{{{a['symbolic']} \\times {c['symbolic']}}}"
        numeric = f"\\frac{{{b['formatted']}}}{{{a['formatted']} \\times {c['formatted']}}}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'first_over_third_over_second' and len(input_data) == 3:
        # (A / C) / B
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"\\frac{{{a['symbolic']}}}{{{c['symbolic']} \\times {b['symbolic']}}}"
        numeric = f"\\frac{{{a['formatted']}}}{{{c['formatted']} \\times {b['formatted']}}}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'second_over_third_over_first' and len(input_data) == 3:
        # (B / C) / A
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"\\frac{{{b['symbolic']}}}{{{c['symbolic']} \\times {a['symbolic']}}}"
        numeric = f"\\frac{{{b['formatted']}}}{{{c['formatted']} \\times {a['formatted']}}}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'third_over_first_over_second' and len(input_data) == 3:
        # (C / A) / B
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"\\frac{{{c['symbolic']}}}{{{a['symbolic']} \\times {b['symbolic']}}}"
        numeric = f"\\frac{{{c['formatted']}}}{{{a['formatted']} \\times {b['formatted']}}}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'third_over_second_over_first' and len(input_data) == 3:
        # (C / B) / A
        a, b, c = input_data[0], input_data[1], input_data[2]
        symbolic = f"\\frac{{{c['symbolic']}}}{{{b['symbolic']} \\times {a['symbolic']}}}"
        numeric = f"\\frac{{{c['formatted']}}}{{{b['formatted']} \\times {a['formatted']}}}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    # 4-input patterns: A × (B - C) × D and variations
    elif operation == 'first_times_diff_of_second_third_times_fourth' and len(input_data) == 4:
        # A × (B - C) × D
        a, b, c, d = input_data[0], input_data[1], input_data[2], input_data[3]
        symbolic = f"{a['symbolic']} \\times ({b['symbolic']} - {c['symbolic']}) \\times {d['symbolic']}"
        numeric = f"{a['formatted']} \\times ({b['formatted']} - {c['formatted']}) \\times {d['formatted']}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'first_times_diff_of_third_second_times_fourth' and len(input_data) == 4:
        # A × (C - B) × D
        a, b, c, d = input_data[0], input_data[1], input_data[2], input_data[3]
        symbolic = f"{a['symbolic']} \\times ({c['symbolic']} - {b['symbolic']}) \\times {d['symbolic']}"
        numeric = f"{a['formatted']} \\times ({c['formatted']} - {b['formatted']}) \\times {d['formatted']}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'second_times_diff_of_first_third_times_fourth' and len(input_data) == 4:
        # B × (A - C) × D
        a, b, c, d = input_data[0], input_data[1], input_data[2], input_data[3]
        symbolic = f"{b['symbolic']} \\times ({a['symbolic']} - {c['symbolic']}) \\times {d['symbolic']}"
        numeric = f"{b['formatted']} \\times ({a['formatted']} - {c['formatted']}) \\times {d['formatted']}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'second_times_diff_of_third_first_times_fourth' and len(input_data) == 4:
        # B × (C - A) × D
        a, b, c, d = input_data[0], input_data[1], input_data[2], input_data[3]
        symbolic = f"{b['symbolic']} \\times ({c['symbolic']} - {a['symbolic']}) \\times {d['symbolic']}"
        numeric = f"{b['formatted']} \\times ({c['formatted']} - {a['formatted']}) \\times {d['formatted']}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'first_times_diff_of_second_fourth_times_third' and len(input_data) == 4:
        # A × (B - D) × C
        a, b, c, d = input_data[0], input_data[1], input_data[2], input_data[3]
        symbolic = f"{a['symbolic']} \\times ({b['symbolic']} - {d['symbolic']}) \\times {c['symbolic']}"
        numeric = f"{a['formatted']} \\times ({b['formatted']} - {d['formatted']}) \\times {c['formatted']}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'first_times_diff_of_fourth_second_times_third' and len(input_data) == 4:
        # A × (D - B) × C
        a, b, c, d = input_data[0], input_data[1], input_data[2], input_data[3]
        symbolic = f"{a['symbolic']} \\times ({d['symbolic']} - {b['symbolic']}) \\times {c['symbolic']}"
        numeric = f"{a['formatted']} \\times ({d['formatted']} - {b['formatted']}) \\times {c['formatted']}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'first_times_sum_of_second_third_times_fourth' and len(input_data) == 4:
        # A × (B + C) × D
        a, b, c, d = input_data[0], input_data[1], input_data[2], input_data[3]
        symbolic = f"{a['symbolic']} \\times ({b['symbolic']} + {c['symbolic']}) \\times {d['symbolic']}"
        numeric = f"{a['formatted']} \\times ({b['formatted']} + {c['formatted']}) \\times {d['formatted']}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'second_times_sum_of_first_third_times_fourth' and len(input_data) == 4:
        # B × (A + C) × D
        a, b, c, d = input_data[0], input_data[1], input_data[2], input_data[3]
        symbolic = f"{b['symbolic']} \\times ({a['symbolic']} + {c['symbolic']}) \\times {d['symbolic']}"
        numeric = f"{b['formatted']} \\times ({a['formatted']} + {c['formatted']}) \\times {d['formatted']}"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    elif operation == 'complex' and len(input_data) == 1 and (getattr(param_value, 'formula', '') or '').startswith('for t='):
        # Dataset time-series sum: X = sum_t max(0, Spending_t - baseline)
        baseline = input_data[0]
        symbolic = f"\\sum_{{t=1900}}^{{2024}} \\max\\left(0, Spending_{{mil,t}} - {baseline['symbolic']}\\right)"
        numeric = f"\\sum_{{t=1900}}^{{2024}} \\max\\left(0, Spending_{{mil,t}} - {baseline['formatted']}\\right)"
        latex = f"{lhs_short} = {symbolic} = {numeric} = {result_formatted}"

    else:
        # Unrecognized operation - check if there's a hardcoded latex
        hardcoded_latex = getattr(param_value, 'latex', None)
        if hardcoded_latex:
            # Has handcoded latex, will be used instead - skip auto-generation
            return None
        
        # No hardcoded latex and can't auto-generate - raise error so we know to add the pattern
        formula = getattr(param_value, 'formula', '') or ''
        inputs_str = ', '.join(inputs) if inputs else 'none'
        raise ValueError(
            f"Cannot auto-generate LaTeX for {param_name}:\n"
            f"  Operation: {operation}\n"
            f"  Inputs ({len(input_data)}): {inputs_str}\n"
            f"  Formula: {formula}\n"
            f"  Fix: Add 'latex' attribute to parameter OR add pattern to latex_generation.py"
        )

    return latex
