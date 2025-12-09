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
from typing import Any, Dict

from .formatting import format_parameter_value


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


def infer_operation_from_compute(param_value: Any, inputs: list) -> tuple[str, str | None]:
    """
    Infer operation type by testing the compute function with known values.

    Returns:
        Tuple of (operation_type, order) where:
        - operation_type: 'sum', 'multiply', 'divide', 'subtract', 'identity', 'complex'
        - order: For division/subtraction, 'first_over_second' or 'second_over_first'
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
        # Single input - check for identity or simple transformation
        if abs(result - test_vals[0]) < 0.01:
            return 'identity', None
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
        else:
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
    """
    Convert a Python lambda body to LaTeX using sympy.

    NOTE: This often produces unreadable output for complex formulas with
    variable names. Only use when the result is simpler than inference-based
    approach. For complex formulas, prefer hardcoded latex fields.
    """
    # For now, skip sympy entirely - the output is worse than inference
    # Complex formulas should use handwritten latex fields
    return None


def format_latex_value(value: float, unit: str) -> str:
    """Format a numeric value for LaTeX display with proper units and scaling."""
    is_currency = "USD" in unit or "usd" in unit or "dollar" in unit.lower()
    is_percentage = "%" in unit or "percent" in unit.lower() or "rate" in unit.lower()
    is_in_billions = "billion" in unit.lower()

    abs_val = abs(value)

    if is_currency:
        if is_in_billions:
            if abs_val >= 1000:
                scaled = value / 1000
                return f"\\${scaled:.1f}T" if abs(scaled) < 100 else f"\\${scaled:.0f}T"
            elif abs_val >= 1:
                return f"\\${value:.1f}B" if abs_val < 100 else f"\\${value:.0f}B"
            else:
                scaled = value * 1000
                return f"\\${scaled:.0f}M"
        else:
            # Raw USD value
            if abs_val >= 1e12:
                return f"\\${value/1e12:.2f}T"
            elif abs_val >= 1e9:
                return f"\\${value/1e9:.2f}B"
            elif abs_val >= 1e6:
                return f"\\${value/1e6:.1f}M"
            elif abs_val >= 1e3:
                return f"\\${value/1e3:.1f}K"
            else:
                return f"\\${value:.0f}"
    elif is_percentage:
        if abs_val <= 1:
            return f"{value * 100:.1f}\\%"
        else:
            return f"{value:.1f}\\%"
    else:
        # Non-currency, non-percentage
        if abs_val >= 1e12:
            return f"{value/1e12:.2f}T"
        elif abs_val >= 1e9:
            return f"{value/1e9:.2f}B"
        elif abs_val >= 1e6:
            formatted = f"{value/1e6:.1f}M"
            return formatted.replace('.0M', 'M')
        elif abs_val >= 1e3:
            # Use thousands separator
            return f"{value:,.0f}".replace(',', '{,}')
        elif abs_val >= 1:
            return f"{value:.2f}".rstrip('0').rstrip('.')
        else:
            return f"{value:.4f}".rstrip('0').rstrip('.')


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


def create_latex_variable_name(param_name: str, display_name: str = "") -> str:
    """
    Create a meaningful LaTeX variable name from parameter info.

    Following patterns from hardcoded equations:
    - OPEX_{total}, Cost_{combat}, Deaths_{total}
    - PeaceDividend_{infra}, Benefit_{RD}
    - TotalWarCost, DirectCosts

    Args:
        param_name: Parameter name like DFDA_ANNUAL_OPEX
        display_name: Human-readable name like "DFDA Annual Operating Expenses"
    """
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
        ('per_capita', 'percap'),  # Per capita metrics
        ('mental_health', 'mental'),
        ('chronic_disease', 'chronic'),
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
        ('trade', 'trade'),
        ('military', 'mil'),
        ('environmental', 'env'),
        ('veteran', 'vet'),
        ('refugee', 'ref'),
        ('ptsd', 'PTSD'),
        ('current', 'curr'),
        ('pre_1962', 'pre62'),
        ('pre1962', 'pre62'),
        ('1980', '80s'),
        ('lost_human', 'lost_cap'),  # Human capital
        ('lost_economic', 'lost_econ'),
        ('lost', 'lost'),
        # Disease-specific
        ('alzheimer', 'alz'),
        ('cancer', 'cancer'),
        ('diabetes', 'diab'),
        ('heart', 'heart'),
        ('stroke', 'stroke'),
        ('obesity', 'obes'),
        # Source-specific
        ('dfda', 'DFDA'),
        ('campaign', 'camp'),
        ('opex', 'opex'),
        ('societal', 'soc'),
        ('symptomatic', 'sympt'),
        ('war_total', 'war'),  # War total cost
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
        if priority_sub:
            subs.append(priority_sub)
        # Add at most one secondary subscript
        if secondary_subs:
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


def generate_auto_latex(
    param_name: str,
    param_value: Any,
    parameters: Dict[str, Dict[str, Any]],
    params_file: Path = None
) -> str | None:
    r"""
    Generate LaTeX equation from parameter metadata.

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
        inp_symbolic = create_latex_variable_name(inp_name, inp_display)

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

    # Create short name for LHS using both param_name and display_name
    lhs_short = create_latex_variable_name(param_name, result_display)

    # For complex operations, try sympy-based conversion first
    if operation == 'complex' and params_file and params_file.exists():
        lambda_body = extract_lambda_body_from_file(param_name, params_file)
        if lambda_body:
            sympy_latex = lambda_to_sympy_latex(lambda_body, inputs)
            if sympy_latex:
                # Sympy gives us the formula structure, add = result
                return f"{lhs_short} = {sympy_latex} = {result_formatted}"

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

    elif operation == 'multiply':
        # Multiplication: X = A × B = val1 × val2 = result
        symbolic_terms = ' \\times '.join(d['symbolic'] for d in input_data)
        numeric_terms = ' \\times '.join(d['formatted'] for d in input_data)
        latex = f"{lhs_short} = {symbolic_terms} = {numeric_terms} = {result_formatted}"

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

    elif operation in ('identity', 'transform') and len(input_data) == 1:
        # Single input transformation: X = A = val = result
        # BUT: Check if formula suggests a binary operation - if so, inputs metadata is incomplete
        formula = getattr(param_value, 'formula', '') or ''
        if '÷' in formula or '×' in formula or '+' in formula or '-' in formula:
            # Formula suggests binary op but only 1 input - skip auto-generation
            return None
        inp = input_data[0]
        latex = f"{lhs_short} = {inp['symbolic']} = {inp['formatted']} = {result_formatted}"

    else:
        # Complex or unrecognized - skip auto-generation
        # (hardcoded latex can still be used)
        return None

    return latex
