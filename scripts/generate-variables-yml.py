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

from generate_references_json import generate_references_json  # noqa: E402
# Delayed imports to allow reference_ids.py regeneration
# from dih_models.parameters import format_parameter_value
from dih_models.formatting import format_parameter_value

# Delayed imports placeholders
simulate = None
one_at_a_time_sensitivity = None
tornado_deltas = None
regression_sensitivity = None
Outcome = None


def init_uncertainty():
    """
    Initialize uncertainty module imports.
    Must be called AFTER generate_reference_ids_enum has run.
    """
    global simulate, one_at_a_time_sensitivity, tornado_deltas, regression_sensitivity, Outcome
    try:
        from dih_models.uncertainty import (
            simulate as _sim, 
            one_at_a_time_sensitivity as _oaat, 
            tornado_deltas as _td, 
            regression_sensitivity as _rs, 
            Outcome as _Out
        )
        simulate = _sim
        one_at_a_time_sensitivity = _oaat
        tornado_deltas = _td
        regression_sensitivity = _rs
        Outcome = _Out
    except ImportError:
        pass
    except Exception as e:
        print(f"[WARN] Failed to load uncertainty module: {e}")


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


def generate_auto_latex(param_name: str, param_value: Any, parameters: Dict[str, Dict[str, Any]], params_file: Path = None) -> str | None:
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
    unit = ""
    if hasattr(value, "unit") and value.unit:
        unit = value.unit

    if hasattr(value, "display_value") and value.display_value:
        formatted_value = value.display_value
    else:
        formatted_value = format_parameter_value(value, unit, include_unit=False)

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
            link_text = "View source citation"
        else:
            # Link to calculation/methodology page (ensure absolute path)
            if not source_ref_value.startswith("/"):
                source_ref_value = f"/{source_ref_value}"
            # Convert .qmd to .html for rendered output
            href = convert_qmd_to_html(source_ref_value)
            link_text = "View methodology & calculation"

        # Build tooltip from Parameter metadata with credibility indicators
        tooltip_parts = []
        if hasattr(value, "description") and value.description:
            tooltip_parts.append(value.description)

        # Show input parameters if this is a calculated parameter
        if source_type_str == "calculated" and hasattr(value, "inputs") and value.inputs:
            num_inputs = len(value.inputs)
            tooltip_parts.append(f"Calculated from {num_inputs} input{'s' if num_inputs != 1 else ''}")

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
    elif source_type_str == "calculated":
        # Calculated parameter without source_ref: link to parameters-and-calculations.qmd
        # Auto-link to the generated section in parameters-and-calculations.qmd
        # Use absolute path for consistency with other calculated parameters
        href = f"/knowledge/appendix/parameters-and-calculations#sec-{param_name.lower()}"

        # Build tooltip from available metadata
        tooltip_parts = []
        if hasattr(value, "description") and value.description:
            tooltip_parts.append(value.description)

        if hasattr(value, "formula") and value.formula:
            tooltip_parts.append(f"Formula: {value.formula}")

        # Show input parameters if available
        if hasattr(value, "inputs") and value.inputs:
            num_inputs = len(value.inputs)
            tooltip_parts.append(f"Calculated from {num_inputs} input{'s' if num_inputs != 1 else ''}")

        if hasattr(value, "confidence") and value.confidence:
            confidence_indicators = {
                "high": "✓ High confidence",
                "medium": "~ Medium confidence",
                "low": "? Low confidence",
                "estimated": "≈ Estimated",
            }
            tooltip_parts.append(confidence_indicators.get(value.confidence, value.confidence))

        if hasattr(value, "unit") and value.unit:
            tooltip_parts.append(f"Unit: {value.unit}")

        # More informative call-to-action
        tooltip_parts.append("Click for equation, sensitivity analysis & Monte Carlo distribution")
        tooltip = " | ".join(tooltip_parts)

        # Build data attributes
        data_attrs = f'data-source-type="calculated"'
        if hasattr(value, "confidence") and value.confidence:
            data_attrs += f' data-confidence="{value.confidence}"'

        html = f'<a href="{href}" class="parameter-link" {data_attrs} title="{tooltip}">{formatted_value}</a>'
    else:
        # Fallback: truly bare parameter with no metadata
        # Build best tooltip we can from available info
        tooltip_parts = []

        # Try to extract description from Parameter object
        if hasattr(value, "description") and value.description:
            tooltip_parts.append(value.description)

        # Show formula if available
        if hasattr(value, "formula") and value.formula:
            tooltip_parts.append(f"Formula: {value.formula}")

        # Show unit if available
        if hasattr(value, "unit") and value.unit:
            tooltip_parts.append(f"Unit: {value.unit}")

        # Add comment from source code if we have it
        if comment:
            tooltip_parts.append(comment)

        # Only fall back to param name if we have NOTHING else
        if not tooltip_parts:
            tooltip_parts.append(f"Parameter: {param_name}")

        tooltip = " | ".join(tooltip_parts)
        html = f'<span class="parameter-link" title="{tooltip}">{formatted_value}</span>'

    return html


def generate_variables_yml(parameters: Dict[str, Dict[str, Any]], output_path: Path, citation_mode: str = "none", params_file: Path = None):
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
        params_file: Path to parameters.py for sympy-based LaTeX generation
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

        # Export LaTeX equation: prefer hardcoded (hand-crafted with good labels),
        # fall back to auto-generated for params without hardcoded latex
        hardcoded_latex = getattr(value, "latex", None)
        auto_latex = generate_auto_latex(param_name, value, parameters, params_file=params_file)

        if hardcoded_latex:
            # Use hardcoded (preferred - hand-crafted with semantic labels)
            latex_var_name = f"{var_name}_latex"
            variables[latex_var_name] = f"$$\n{hardcoded_latex}\n$$"
        elif auto_latex:
            # Fall back to auto-generated for params without hardcoded
            latex_var_name = f"{var_name}_latex"
            variables[latex_var_name] = f"$$\n{auto_latex}\n$$"

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
        print("     Citation mode: inline [@key] for peer-reviewed sources")
    print("\nUsage in QMD files:")
    print(f"  {{{{< var {list(variables.keys())[0]} >}}}}")
    if latex_count > 0:
        # Find first latex equation
        latex_var = next((k for k in variables.keys() if k.endswith("_latex")), None)
        if latex_var:
            print(f"  {{{{< var {latex_var} >}}}}  (equation)")
    if cite_count > 0:
        # Find first parameter with citation
        cite_var = next((k for k in variables.keys() if k.endswith("_cite")), None)
        if cite_var:
            base_var = cite_var[:-5]  # Remove "_cite"
            print(f"  {{{{< var {base_var} >}}}} {{{{< var {cite_var} >}}}}")


def generate_uncertainty_section(value: Any, unit: str = "") -> list[str]:
    """
    Generate human-friendly uncertainty explanation for a parameter.

    Returns both technical notation (for economists) and plain-language
    explanations (for general readers).

    Args:
        value: Parameter instance with uncertainty metadata
        unit: Unit string for formatting

    Returns:
        List of content lines to append to the QMD
    """
    content = []

    # Check if we have any uncertainty metadata
    has_ci = hasattr(value, "confidence_interval") and value.confidence_interval
    has_dist = hasattr(value, "distribution") and value.distribution
    has_se = hasattr(value, "std_error") and value.std_error
    has_sensitivity = hasattr(value, "sensitivity") and value.sensitivity

    if not (has_ci or has_dist or has_se or has_sensitivity):
        return content

    content.append("#### Uncertainty Range")
    content.append("")

    # Technical notation line
    technical_parts = []

    if has_ci:
        low, high = value.confidence_interval
        low_str = format_parameter_value(low, unit)
        high_str = format_parameter_value(high, unit)
        technical_parts.append(f"95% CI: [{low_str}, {high_str}]")

    if has_dist:
        dist_name = value.distribution.value if hasattr(value.distribution, "value") else str(value.distribution)
        dist_str = dist_name.title()
        if has_se:
            se_str = format_parameter_value(value.std_error, unit)
            dist_str += f" (SE: {se_str})"
        technical_parts.append(f"Distribution: {dist_str}")

    if has_sensitivity and not has_ci:
        sens_str = format_parameter_value(value.sensitivity, unit)
        technical_parts.append(f"Sensitivity: ±{sens_str}")

    if technical_parts:
        content.append("**Technical**: " + " • ".join(technical_parts))
        content.append("")

    # Human-friendly explanation
    main_value = float(value)

    if has_ci:
        low, high = value.confidence_interval

        # Calculate percentage range from central value
        low_pct = abs((main_value - low) / main_value * 100) if main_value != 0 else 0
        high_pct = abs((high - main_value) / main_value * 100) if main_value != 0 else 0
        avg_pct = (low_pct + high_pct) / 2

        # Format the bounds nicely
        low_str = format_parameter_value(low, unit)
        high_str = format_parameter_value(high, unit)

        # Generate plain-language explanation based on uncertainty size
        if avg_pct <= 10:
            certainty_phrase = "We're quite confident in this estimate"
            range_desc = "a narrow range"
        elif avg_pct <= 25:
            certainty_phrase = "This estimate has moderate uncertainty"
            range_desc = "a reasonable range"
        elif avg_pct <= 50:
            certainty_phrase = "There's significant uncertainty here"
            range_desc = "a wide range"
        else:
            certainty_phrase = "This estimate is highly uncertain"
            range_desc = "a very wide range"

        content.append(f"**What this means**: {certainty_phrase}. The true value likely falls between {low_str} and {high_str} (±{avg_pct:.0f}%). This represents {range_desc} that our Monte Carlo simulations account for when calculating overall uncertainty in the results.")
        content.append("")

        # Add distribution explanation if present
        if has_dist:
            dist_name = value.distribution.value if hasattr(value.distribution, "value") else str(value.distribution)

            dist_explanations = {
                "normal": "values cluster around the center with equal chances of being higher or lower",
                "lognormal": "values can't go negative and have a longer tail toward higher values (common for costs and populations)",
                "uniform": "any value in the range is equally likely",
                "triangular": "values cluster around a most-likely point but can range higher or lower",
                "beta": "values are bounded and can skew toward one end",
                "pert": "values cluster around a most-likely estimate with defined min/max bounds",
            }

            explanation = dist_explanations.get(dist_name.lower(), "values follow a specific statistical pattern")
            content.append(f"*The {dist_name.lower()} distribution means {explanation}.*")
            content.append("")

    elif has_sensitivity:
        sens = value.sensitivity
        sens_str = format_parameter_value(sens, unit)
        sens_pct = abs(sens / main_value * 100) if main_value != 0 else 0

        content.append(f"**What this means**: This value could reasonably vary by ±{sens_str} (±{sens_pct:.0f}%) based on different assumptions or data sources.")
        content.append("")

    return content


def generate_parameters_qmd(parameters: Dict[str, Dict[str, Any]], output_path: Path, available_refs: set = None, params_file: Path = None):
    """
    Generate comprehensive parameters-and-calculations.qmd appendix.

    Creates an academic reference page with:
    - All parameters organized by type (external/calculated)
    - LaTeX equations where available (hardcoded or auto-generated)
    - Citations and source links
    - Confidence indicators and metadata
    - Uncertainty ranges with human-friendly explanations

    Args:
        parameters: Dict of parameter metadata
        output_path: Path to write the QMD file
        available_refs: Set of valid reference IDs from references.qmd (optional, for detecting reference links)
        params_file: Path to parameters.py (for auto-generating latex equations)
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
        "This appendix provides comprehensive documentation of all parameters and calculations used in the economic analysis of a 1% treaty and decentralized framework for drug assessment."
    )
    content.append("")
    content.append(f"**Total parameters**: {len(parameters)}")
    content.append("")
    content.append(f"- External sources (peer-reviewed): {len(external_params)}")
    content.append(f"- Calculated values: {len(calculated_params)}")
    content.append(f"- Core definitions: {len(definition_params)}")
    content.append("")

    # Calculated parameters section (moved first)
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

            # Show input parameters with links (NEW)
            if hasattr(value, "inputs") and value.inputs:
                content.append("**Inputs**:")
                content.append("")
                for inp_name in value.inputs:
                    inp_meta = parameters.get(inp_name, {})
                    inp_value = inp_meta.get('value')

                    if inp_value is None:
                        # Handle missing input gracefully
                        content.append(f"- [{smart_title_case(inp_name)}](#sec-{inp_name.lower()}): *not found*")
                        continue

                    # Get display name
                    if hasattr(inp_value, "display_name") and inp_value.display_name:
                        inp_display = inp_value.display_name
                    else:
                        inp_display = smart_title_case(inp_name)

                    # Format value
                    inp_unit = getattr(inp_value, "unit", "")
                    inp_formatted = format_parameter_value(inp_value, inp_unit)

                    # Add uncertainty information if available (verbose format)
                    uncertainty_str = ""
                    if hasattr(inp_value, "confidence_interval") and inp_value.confidence_interval:
                        low, high = inp_value.confidence_interval
                        low_str = format_parameter_value(low, inp_unit)
                        high_str = format_parameter_value(high, inp_unit)
                        uncertainty_str = f" (95% CI: {low_str} - {high_str})"
                    elif hasattr(inp_value, "std_error") and inp_value.std_error:
                        se_str = format_parameter_value(inp_value.std_error, inp_unit)
                        uncertainty_str = f" (SE: ±{se_str})"

                    # Get source type for visual indicator
                    source_type_indicator = ""
                    if hasattr(inp_value, "source_type"):
                        source_type_str = str(inp_value.source_type.value) if hasattr(inp_value.source_type, 'value') else str(inp_value.source_type)
                        if source_type_str == "external":
                            source_type_indicator = " 📊"  # External data
                        elif source_type_str == "calculated":
                            source_type_indicator = " 🔢"  # Calculated value

                    # Link to parameter section
                    content.append(f"- [{inp_display}](#sec-{inp_name.lower()}){source_type_indicator}: {inp_formatted}{uncertainty_str}")

                content.append("")

            # LaTeX equation - prominently displayed
            # Priority: hardcoded latex > auto-generated latex > formula
            hardcoded_latex = getattr(value, "latex", None)
            auto_latex = generate_auto_latex(param_name, value, parameters, params_file=params_file) if not hardcoded_latex else None

            if hardcoded_latex:
                content.append("$$")
                content.append(hardcoded_latex)
                content.append("$$")
                content.append("")
            elif auto_latex:
                content.append("$$")
                content.append(auto_latex)
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

            # Uncertainty section with human-friendly explanations (for calculated values too)
            uncertainty_content = generate_uncertainty_section(value, unit)
            content.extend(uncertainty_content)

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
            project_root / "_analysis" / f"tornado_{param_name}.json"
            tornado_qmd = project_root / "knowledge" / "figures" / f"tornado-{param_name.lower()}.qmd"
            sensitivity_qmd = project_root / "knowledge" / "figures" / f"sensitivity-table-{param_name.lower()}.qmd"
            mc_dist_qmd = project_root / "knowledge" / "figures" / f"mc-distribution-{param_name.lower()}.qmd"
            exceedance_qmd = project_root / "knowledge" / "figures" / f"exceedance-{param_name.lower()}.qmd"

            if tornado_qmd.exists():
                content.append("#### Sensitivity Analysis")
                content.append("")
                content.append(f"{{{{< include ../figures/tornado-{param_name.lower()}.qmd >}}}}")
                content.append("")

                if sensitivity_qmd.exists():
                    content.append(f"{{{{< include ../figures/sensitivity-table-{param_name.lower()}.qmd >}}}}")
                    content.append("")
            
            # Generate sensitivity table if needed (dynamic generation)
            # Find input parameters via compute function or inputs list
            if hasattr(value, "inputs") and value.inputs and hasattr(value, "compute"):
                # We need to calculate sensitivity indices (regression coefficients)
                # This requires the dih_models.uncertainty module
                if regression_sensitivity and hasattr(value, "distribution"):
                     # This is logically where we would generate the table
                     # For now, we are relying on pre-calculated sensitivity files or on-demand generation elsewhere
                     pass

            # Add Monte Carlo distribution chart if exists
            if mc_dist_qmd.exists():
                content.append("#### Monte Carlo Distribution")
                content.append("")
                content.append(f"{{{{< include ../figures/mc-distribution-{param_name.lower()}.qmd >}}}}")
                content.append("")

            # Add exceedance/CDF chart if exists
            if exceedance_qmd.exists():
                content.append("#### Exceedance Probability")
                content.append("")
                content.append(f"{{{{< include ../figures/exceedance-{param_name.lower()}.qmd >}}}}")
                content.append("")

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
                # Check if source_ref is a .qmd file path or a references.qmd anchor
                # Use relative paths for multi-format compatibility (HTML, PDF, EPUB)
                if source_ref_str.endswith('.qmd'):
                    # It's a path to another .qmd document
                    # Convert absolute path to relative from knowledge/appendix/
                    if source_ref_str.startswith('/knowledge/'):
                        # /knowledge/appendix/foo.qmd -> foo (same dir)
                        # /knowledge/foo.qmd -> ../foo (parent dir)
                        rel_path = source_ref_str[len('/knowledge/'):]
                        if rel_path.startswith('appendix/'):
                            rel_path = rel_path[len('appendix/'):]
                        else:
                            rel_path = '../' + rel_path
                    else:
                        rel_path = source_ref_str
                    # Remove .qmd extension for format-agnostic links
                    rel_path = convert_qmd_to_html(rel_path)
                    content.append(f"**Source**: [{display_ref}]({rel_path})")
                else:
                    # It's a reference anchor ID - link to references.qmd (relative path)
                    content.append(f"**Source**: [{display_ref}](../references.qmd#{source_ref_str})")
                content.append("")

            # Uncertainty section with human-friendly explanations
            uncertainty_content = generate_uncertainty_section(value, unit)
            content.extend(uncertainty_content)

            # Add input distribution chart if exists (for external params with uncertainty)
            project_root = output_path.parent.parent.parent  # Go up from knowledge/appendix/ to project root
            dist_qmd = project_root / "knowledge" / "figures" / f"distribution-{param_name.lower()}.qmd"
            if dist_qmd.exists():
                content.append("#### Input Distribution")
                content.append("")
                content.append(f"{{{{< include ../figures/distribution-{param_name.lower()}.qmd >}}}}")
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

            # Uncertainty section with human-friendly explanations (for definitions too)
            uncertainty_content = generate_uncertainty_section(value, unit)
            content.extend(uncertainty_content)

            content.append("*Core definition*")
            content.append("")
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

                    # Skip validation for .qmd file paths - they're internal document links, not references.qmd anchors
                    if source_ref_str.endswith('.qmd'):
                        continue

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


def validate_calculated_params_no_uncertainty(parameters: Dict[str, Dict[str, Any]]) -> list:
    """
    Validate that calculated parameters don't have their own uncertainty distributions.

    Calculated parameters should derive uncertainty from their inputs via the compute
    function, not have their own confidence_interval or distribution. Having both
    would double-count uncertainty.

    Args:
        parameters: Dict of parameter metadata

    Returns:
        List of (param_name, issues) tuples for calculated params with uncertainty
    """
    problematic_params = []

    for param_name, param_data in parameters.items():
        value = param_data["value"]
        if hasattr(value, "source_type"):
            source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
            if source_type_str == "calculated":
                issues = []

                # Check for confidence_interval
                if hasattr(value, "confidence_interval") and value.confidence_interval is not None:
                    issues.append("confidence_interval")

                # Check for distribution
                if hasattr(value, "distribution") and value.distribution is not None:
                    issues.append("distribution")

                # Check for std_error
                if hasattr(value, "std_error") and value.std_error is not None:
                    issues.append("std_error")

                if issues:
                    problematic_params.append((param_name, issues))

    return problematic_params


def validate_formula_uses_full_param_names(parameters: Dict[str, Dict[str, Any]]) -> list:
    """
    Validate that formula strings use full parameter names matching the inputs list.

    This ensures LaTeX auto-generation can correctly determine operand order
    (e.g., numerator vs denominator in divisions) by matching formula text to inputs.

    Args:
        parameters: Dict of parameter metadata

    Returns:
        List of (param_name, input_name, formula) tuples for mismatches
    """
    mismatches = []

    for param_name, param_data in parameters.items():
        value = param_data["value"]

        # Only check parameters with both inputs and formula
        if not hasattr(value, 'inputs') or not value.inputs:
            continue
        if not hasattr(value, 'formula') or not value.formula:
            continue

        formula_upper = value.formula.upper()

        for inp_name in value.inputs:
            # Check if full input name appears in formula
            if inp_name.upper() not in formula_upper:
                mismatches.append((param_name, inp_name, value.formula))
                break  # Only report first missing input per parameter

    return mismatches


def validate_compute_inputs_match(parameters: Dict[str, Dict[str, Any]], params_file: Path) -> list:
    """
    Validate that the 'inputs' list matches what's actually used in the compute function.

    This catches bugs where:
    - compute uses ctx["X"] but X is not in inputs list (will break uncertainty propagation)
    - inputs lists X but compute doesn't use ctx["X"] (unnecessary dependency)

    Args:
        parameters: Dict of parameter metadata
        params_file: Path to parameters.py file for source code inspection

    Returns:
        List of (param_name, issue_type, missing_or_extra_vars) tuples
    """
    issues = []

    if not params_file or not params_file.exists():
        return issues

    content = params_file.read_text(encoding="utf-8")

    for param_name, param_data in parameters.items():
        value = param_data["value"]

        # Only check parameters with compute function
        if not hasattr(value, 'compute') or not value.compute:
            continue

        inputs = getattr(value, 'inputs', []) or []
        input_set = set(inputs)

        # Find the parameter definition in the source
        start_pattern = rf'{param_name}\s*=\s*Parameter\('
        start_match = re.search(start_pattern, content)
        if not start_match:
            continue

        start = start_match.start()

        # Find matching closing paren
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

        # Find all ctx["X"] references in the compute lambda
        ctx_refs = set(re.findall(r'ctx\["([^"]+)"\]', param_def))

        # Check for mismatches
        missing_from_inputs = ctx_refs - input_set
        extra_in_inputs = input_set - ctx_refs

        if missing_from_inputs:
            issues.append((param_name, 'missing_from_inputs', sorted(missing_from_inputs)))
        if extra_in_inputs:
            issues.append((param_name, 'extra_in_inputs', sorted(extra_in_inputs)))

    return issues


def validate_inline_calculations_have_compute(parameters: Dict[str, Dict[str, Any]], params_file: Path) -> list:
    """
    Validate that CALCULATED parameters with inline calculations have inputs and compute functions.

    This catches parameters like:
        PARAM = Parameter(A * B, source_type="calculated", ...)  # Inline calculation

    Without inputs/compute metadata, these break:
    - Uncertainty propagation (can't trace what inputs affect the value)
    - LaTeX auto-generation (can't format the equation)
    - Recalculation when inputs change

    NOTE: Skips source_type="definition" parameters - these are policy choices or
    simple unit conversions that don't need uncertainty propagation.

    Args:
        parameters: Dict of parameter metadata
        params_file: Path to parameters.py file for source code inspection

    Returns:
        List of (param_name, first_arg_snippet) tuples for params with inline calcs but no compute
    """
    issues = []

    if not params_file or not params_file.exists():
        return issues

    content = params_file.read_text(encoding="utf-8")

    for param_name, param_data in parameters.items():
        value = param_data["value"]

        # Skip if already has compute function
        if hasattr(value, 'compute') and value.compute:
            continue

        # Skip definitions - they're policy choices, not uncertain calculations
        source_type = getattr(value, 'source_type', '')
        if source_type and 'definition' in str(source_type).lower():
            continue

        # Find the parameter definition in the source
        pattern = rf'{param_name}\s*=\s*Parameter\(\s*\n?\s*([^,\n]+)'
        match = re.search(pattern, content)
        if not match:
            continue

        first_arg = match.group(1).strip()

        # Skip if first arg is just a number
        if re.match(r'^[\d._]+$', first_arg):
            continue
        # Skip if it's a float() or int() of a single param (simple wrapper)
        if re.match(r'^(float|int)\(\w+\)$', first_arg):
            continue
        # Skip common constants
        if first_arg in ('True', 'False', 'None'):
            continue

        # Check if it has an inline calculation (arithmetic operators)
        if any(op in first_arg for op in ['*', '/', '+', '-']):
            issues.append((param_name, first_arg[:60]))

    return issues


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
    content.append("% used in the economic analysis of a 1% treaty and decentralized framework for drug assessment.")
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
                content.append("  urldate = {2025-01-20},")

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

    Raises:
        ValueError: If tornado_data is empty or has no meaningful drivers
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

    # Validate: skip if no drivers or all deltas are zero
    if not sorted_drivers:
        raise ValueError(f"No tornado drivers found for {param_name}")

    # Check if all impacts are effectively zero (< 1e-10 relative to baseline)
    threshold = abs(baseline) * 1e-10 if baseline and abs(baseline) > 0 else 1e-10
    has_meaningful_impact = any(
        abs(data.get("delta_minus", 0)) > threshold or abs(data.get("delta_plus", 0)) > threshold
        for _, data in sorted_drivers
    )

    if not has_meaningful_impact:
        raise ValueError(f"All tornado impacts near zero for {param_name}")

    # Generate Python code for tornado chart
    qmd_content = f'''```{{python}}
#| echo: false

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from dih_models.plotting.chart_style import (
    setup_chart_style, add_watermark, clean_spines,
    COLOR_BLACK, COLOR_WHITE, add_png_metadata, get_figure_output_path
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

# Save PNG to knowledge/figures/ regardless of where Quarto renders from

output_path = get_figure_output_path('tornado-{param_name.lower()}.png')
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


def generate_sensitivity_table_qmd(param_name: str, sensitivity_data: dict, output_dir: Path, param_metadata: dict = None, parameters: Dict[str, Dict[str, Any]] = None) -> Path:
    """
    Generate a sensitivity indices table QMD file for a parameter.

    Args:
        param_name: Parameter name
        sensitivity_data: Dict mapping input names to sensitivity coefficients
        output_dir: Directory to write QMD file
        param_metadata: Optional parameter metadata for context
        parameters: Optional dict of all parameter metadata for looking up inputs

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
        # Use parameters dict to find better display name and units
        display_input = smart_title_case(input_name)
        
        if parameters and input_name in parameters:
            input_val = parameters[input_name]["value"]
            if hasattr(input_val, "display_name") and input_val.display_name:
                display_input = input_val.display_name
                
            # Add unit if available
            if hasattr(input_val, "unit") and input_val.unit:
                # Use format_parameter_value to get a clean unit string if possible, or just append
                # For brevity in tables, just the unit name is often best
                unit_str = input_val.unit
                # Clean up unit (e.g., don't show "USD" if it's obvious, but maybe good to be explicit)
                display_input = f"{display_input} ({unit_str})"
        # Standardized coefficients range from -1 to 1
        # Use absolute value thresholds appropriate for standardized betas
        abs_coef = abs(coef)
        if abs_coef > 0.5:
            interpretation = "Strong driver"
        elif abs_coef > 0.3:
            interpretation = "Moderate driver"
        elif abs_coef > 0.1:
            interpretation = "Weak driver"
        else:
            interpretation = "Minimal effect"
        qmd_content += f'| {display_input} | {coef:.4f} | {interpretation} |\n'

    qmd_content += '''
*Interpretation*: Standardized coefficients show the change in output (in SD units) per 1 SD change in input. Values near ±1 indicate strong influence; values exceeding ±1 may occur with correlated inputs.
'''

    # Write QMD file
    output_file = output_dir / f'sensitivity-table-{param_name.lower()}.qmd'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(qmd_content)

    return output_file


def generate_input_distribution_chart_qmd(param_name: str, param_data: dict, output_dir: Path) -> Path:
    """
    Generate a distribution chart for an input parameter showing its uncertainty range.

    This visualizes the assumed probability distribution for external/definition parameters
    that have confidence_interval and/or distribution metadata.

    Args:
        param_name: Parameter name (e.g., 'GLOBAL_MILITARY_SPENDING_ANNUAL_2024')
        param_data: Parameter metadata dict with 'value' key containing Parameter instance
        output_dir: Directory to write QMD file (knowledge/figures/)

    Returns:
        Path to generated QMD file

    Raises:
        ValueError: If parameter has no uncertainty metadata
    """
    value = param_data.get("value")
    if not value:
        raise ValueError(f"No value for parameter {param_name}")

    # Check for uncertainty metadata
    has_ci = hasattr(value, "confidence_interval") and value.confidence_interval
    has_dist = hasattr(value, "distribution") and value.distribution
    has_se = hasattr(value, "std_error") and value.std_error

    if not (has_ci or has_dist or has_se):
        raise ValueError(f"Parameter {param_name} has no uncertainty metadata")

    # Get display name
    if hasattr(value, "display_name") and value.display_name:
        display_name = value.display_name
    else:
        display_name = smart_title_case(param_name)

    # Get values
    central_value = float(value)
    unit = getattr(value, "unit", "")

    # Determine distribution parameters
    if has_ci:
        low, high = value.confidence_interval
    elif has_se:
        # Approximate 95% CI from standard error
        low = central_value - 1.96 * value.std_error
        high = central_value + 1.96 * value.std_error
    else:
        # Default ±20% if only distribution type specified
        low = central_value * 0.8
        high = central_value * 1.2

    # Get distribution type
    dist_type = "normal"  # default
    if has_dist:
        dist_type = value.distribution.value if hasattr(value.distribution, "value") else str(value.distribution)
        dist_type = dist_type.lower()

    # Generate Python code for the chart
    qmd_content = f'''```{{python}}
#| echo: false
#| fig-cap: "Probability Distribution: {display_name}"

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from pathlib import Path

from dih_models.plotting.chart_style import (
    setup_chart_style, add_watermark, clean_spines,
    COLOR_BLACK, COLOR_WHITE, add_png_metadata, get_figure_output_path
)

setup_chart_style()

# Parameter values

central_value = {central_value}
low = {low}
high = {high}
dist_type = "{dist_type}"
display_name = "{display_name}"
unit = "{unit}"

# Calculate distribution parameters

if dist_type == "lognormal":
    # For lognormal, we need to work in log space

    # Assume low/high are 5th/95th percentiles

    if central_value > 0 and low > 0:
        mu = np.log(central_value)
        # Estimate sigma from CI width

        sigma = (np.log(high) - np.log(low)) / (2 * 1.645)  # 90% CI
        sigma = max(sigma, 0.1)  # Minimum sigma

        x = np.linspace(max(0.01, low * 0.5), high * 1.5, 500)
        y = stats.lognorm.pdf(x, s=sigma, scale=np.exp(mu))
    else:
        # Fall back to normal if values aren't positive

        dist_type = "normal"

if dist_type == "normal":
    # Estimate sigma from CI width (assuming 95% CI)

    sigma = (high - low) / (2 * 1.96)
    sigma = max(sigma, abs(central_value) * 0.01)  # Minimum 1% of value

    x = np.linspace(low - sigma, high + sigma, 500)
    y = stats.norm.pdf(x, loc=central_value, scale=sigma)

elif dist_type == "uniform":
    x = np.linspace(low * 0.9, high * 1.1, 500)
    y = np.where((x >= low) & (x <= high), 1 / (high - low), 0)

elif dist_type == "triangular":
    # Triangular with mode at central value

    x = np.linspace(low * 0.9, high * 1.1, 500)
    y = stats.triang.pdf(x, c=(central_value - low) / (high - low), loc=low, scale=high - low)

elif dist_type == "beta":
    # Beta distribution scaled to [low, high]

    # Use alpha=2, beta=2 for symmetric bell shape

    x_norm = np.linspace(0, 1, 500)
    x = low + x_norm * (high - low)
    y = stats.beta.pdf(x_norm, a=2, b=2) / (high - low)

elif dist_type == "pert":
    # PERT is a special case of beta

    # Mode = central_value, min = low, max = high

    range_val = high - low
    if range_val > 0:
        # PERT uses alpha = 1 + 4*(mode-min)/(max-min), beta = 1 + 4*(max-mode)/(max-min)

        mode_ratio = (central_value - low) / range_val
        alpha = 1 + 4 * mode_ratio
        beta_param = 1 + 4 * (1 - mode_ratio)
        x_norm = np.linspace(0, 1, 500)
        x = low + x_norm * range_val
        y = stats.beta.pdf(x_norm, a=alpha, b=beta_param) / range_val
    else:
        x = np.array([central_value])
        y = np.array([1])

# Create figure

fig, ax = plt.subplots(figsize=(10, 6))

# Plot distribution

ax.fill_between(x, y, alpha=0.3, color=COLOR_BLACK)
ax.plot(x, y, color=COLOR_BLACK, linewidth=2)

# Mark central value

ax.axvline(central_value, color=COLOR_BLACK, linestyle='--', linewidth=2,
           label=f'Central: {{central_value:,.2g}}')

# Mark confidence interval

ax.axvline(low, color=COLOR_BLACK, linestyle=':', linewidth=1.5, alpha=0.7,
           label=f'95% CI Low: {{low:,.2g}}')
ax.axvline(high, color=COLOR_BLACK, linestyle=':', linewidth=1.5, alpha=0.7,
           label=f'95% CI High: {{high:,.2g}}')

# Shade the CI region

ci_mask = (x >= low) & (x <= high)
ax.fill_between(x, y, where=ci_mask, alpha=0.2, color=COLOR_BLACK)

# Labels

ax.set_xlabel(f'{{display_name}} ({{unit}})' if unit else display_name, fontsize=12)
ax.set_ylabel('Probability Density', fontsize=12)
ax.set_title(f'Assumed Distribution: {{display_name}}', fontsize=14, weight='bold', pad=15)

# Legend

ax.legend(loc='upper right', fontsize=10)

# Clean up

clean_spines(ax)
ax.set_ylim(bottom=0)

# Add watermark

add_watermark(fig)

# Save PNG to knowledge/figures/ regardless of where Quarto renders from

output_path = get_figure_output_path('distribution-{param_name.lower()}.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=COLOR_WHITE)

add_png_metadata(
    output_path,
    title=f'Distribution: {{display_name}}',
    description=f'Assumed probability distribution for {{display_name}} showing uncertainty range'
)

plt.show()
```

*This chart shows the assumed probability distribution for this parameter. The shaded region represents the 95% confidence interval where we expect the true value to fall.*
'''

    # Write QMD file
    output_file = output_dir / f'distribution-{param_name.lower()}.qmd'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(qmd_content)

    return output_file


def generate_monte_carlo_distribution_chart_qmd(
    param_name: str,
    outcome_data: dict,
    samples: list,
    output_dir: Path,
    param_metadata: dict = None
) -> Path:
    """
    Generate a Monte Carlo output distribution chart for a calculated parameter.

    Shows the histogram of simulated outcomes with percentiles and statistics.

    Args:
        param_name: Parameter name (e.g., 'TREATY_COMPLETE_ROI_ALL_BENEFITS')
        outcome_data: Dict with baseline, mean, std, p5, p50, p95, units
        samples: List of Monte Carlo samples for this outcome
        output_dir: Directory to write QMD file
        param_metadata: Optional parameter metadata

    Returns:
        Path to generated QMD file
    """
    # Get display name
    if param_metadata and hasattr(param_metadata.get("value"), "display_name"):
        display_name = param_metadata["value"].display_name
    else:
        display_name = smart_title_case(param_name)

    baseline = outcome_data.get("baseline", 0)
    mean = outcome_data.get("mean", baseline)
    std = outcome_data.get("std", 0)
    p5 = outcome_data.get("p5", baseline)
    p50 = outcome_data.get("p50", baseline)
    p95 = outcome_data.get("p95", baseline)
    units = outcome_data.get("units", "")

    # Generate QMD with embedded Python
    qmd_content = f'''```{{python}}
#| echo: false
#| fig-cap: "Monte Carlo Distribution: {display_name} (10,000 simulations)"

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from dih_models.plotting.chart_style import (
    setup_chart_style, add_watermark, clean_spines, get_tick_formatter,
    COLOR_BLACK, COLOR_WHITE, add_png_metadata, get_figure_output_path
)
from dih_models.parameters import format_parameter_value

setup_chart_style()

# Simulation results

samples = {samples[:1000] if len(samples) > 1000 else samples}  # Truncate for embedding
baseline = {baseline}
mean = {mean}
std = {std}
p5 = {p5}
p50 = {p50}
p95 = {p95}
display_name = "{display_name}"
units = "{units}"

# Create figure with two subplots

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.subplots_adjust(wspace=0.3)

# --- Left: Histogram ---

# Handle edge case where all samples are identical (zero variance)

if std == 0 or (max(samples) == min(samples)):
    n_bins = 1
else:
    n_bins = min(50, max(1, int(np.sqrt(len(samples)))))
n, bins, patches = ax1.hist(samples, bins=n_bins, color=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=1)

# Apply tick formatter for readable labels (K, M, B suffixes, $ for USD)

ax1.xaxis.set_major_formatter(get_tick_formatter(unit=units))

# Mark key statistics with formatted values in legend (use format_parameter_value for full units)

ax1.axvline(p50, color=COLOR_BLACK, linestyle='--', linewidth=2, label=f'Median: {{format_parameter_value(p50, units)}}')
ax1.axvline(p5, color=COLOR_BLACK, linestyle=':', linewidth=1.5, alpha=0.7, label=f'5th %-ile: {{format_parameter_value(p5, units)}}')
ax1.axvline(p95, color=COLOR_BLACK, linestyle=':', linewidth=1.5, alpha=0.7, label=f'95th %-ile: {{format_parameter_value(p95, units)}}')
ax1.axvline(baseline, color=COLOR_BLACK, linestyle='-', linewidth=1.5, alpha=0.5, label=f'Baseline: {{format_parameter_value(baseline, units)}}')

ax1.set_xlabel(f'{{display_name}} ({{units}})' if units else display_name, fontsize=11)
ax1.set_ylabel('Frequency', fontsize=11)
ax1.set_title('Distribution of Outcomes', fontsize=12, weight='bold')
ax1.legend(loc='upper right', fontsize=9)
clean_spines(ax1)

# --- Right: CDF (Cumulative Probability) ---

sorted_samples = np.sort(samples)
cumulative = np.arange(1, len(sorted_samples) + 1) / len(sorted_samples)

ax2.plot(sorted_samples, cumulative * 100, color=COLOR_BLACK, linewidth=2)
ax2.fill_between(sorted_samples, 0, cumulative * 100, alpha=0.1, color=COLOR_BLACK)

# Apply tick formatter for readable labels (K, M, B suffixes, $ for USD)

ax2.xaxis.set_major_formatter(get_tick_formatter(unit=units))

# Mark key percentiles

ax2.axhline(50, color=COLOR_BLACK, linestyle='--', linewidth=1, alpha=0.5)
ax2.axhline(5, color=COLOR_BLACK, linestyle=':', linewidth=1, alpha=0.5)
ax2.axhline(95, color=COLOR_BLACK, linestyle=':', linewidth=1, alpha=0.5)
ax2.axvline(p50, color=COLOR_BLACK, linestyle='--', linewidth=1, alpha=0.5)

ax2.set_xlabel(f'{{display_name}} ({{units}})' if units else display_name, fontsize=11)
ax2.set_ylabel('Cumulative Probability (%)', fontsize=11)
ax2.set_title('Probability of Exceeding Value', fontsize=12, weight='bold')
ax2.set_ylim(0, 100)
clean_spines(ax2)

# Add annotation for "probability of exceeding baseline"

exceed_baseline_pct = (np.array(samples) > baseline).sum() / len(samples) * 100
ax2.annotate(f'{{exceed_baseline_pct:.0f}}% chance of\\nexceeding baseline',
             xy=(baseline, exceed_baseline_pct), xytext=(baseline * 1.1, exceed_baseline_pct + 10),
             fontsize=9, ha='left',
             arrowprops=dict(arrowstyle='->', color=COLOR_BLACK, lw=1))

# Main title

fig.suptitle(f'Monte Carlo Analysis: {{display_name}}', fontsize=14, weight='bold', y=1.02)

# Add watermark

add_watermark(fig)

# Save PNG to knowledge/figures/ regardless of where Quarto renders from

output_path = get_figure_output_path('mc-distribution-{param_name.lower()}.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=COLOR_WHITE)

add_png_metadata(
    output_path,
    title=f'Monte Carlo: {{display_name}}',
    description=f'Monte Carlo simulation results showing uncertainty distribution for {{display_name}}'
)

plt.show()
```

**Simulation Results Summary: {display_name}**

| Statistic | Value |
|:----------|------:|
| Baseline (deterministic) | {format_parameter_value(baseline, units, include_unit=False)} |
| Mean (expected value) | {format_parameter_value(mean, units, include_unit=False)} |
| Median (50th percentile) | {format_parameter_value(p50, units, include_unit=False)} |
| Standard Deviation | {format_parameter_value(std, units, include_unit=False)} |
| 90% Confidence Interval | [{format_parameter_value(p5, units, include_unit=False)}, {format_parameter_value(p95, units, include_unit=False)}] |

*The histogram shows the distribution of {display_name} across 10,000 Monte Carlo simulations. The CDF (right) shows the probability of the outcome exceeding any given value, which is useful for risk assessment.*
'''

    # Write QMD file
    output_file = output_dir / f'mc-distribution-{param_name.lower()}.qmd'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(qmd_content)

    return output_file


def generate_cdf_chart_qmd(
    param_name: str,
    samples: list,
    output_dir: Path,
    param_metadata: dict = None,
    thresholds: list = None
) -> Path:
    """
    Generate a standalone Cumulative Distribution Function (CDF) chart.

    This is the "probability of exceeding X" chart that funders love.

    Args:
        param_name: Parameter name
        samples: List of Monte Carlo samples
        output_dir: Directory to write QMD file
        param_metadata: Optional parameter metadata
        thresholds: Optional list of threshold values to annotate (e.g., [10, 50, 100] for ROI)

    Returns:
        Path to generated QMD file
    """
    # Get display name
    if param_metadata and hasattr(param_metadata.get("value"), "display_name"):
        display_name = param_metadata["value"].display_name
    else:
        display_name = smart_title_case(param_name)

    units = ""
    if param_metadata and hasattr(param_metadata.get("value"), "unit"):
        units = param_metadata["value"].unit or ""

    # Auto-generate thresholds if not provided
    if thresholds is None:
        sorted_s = sorted(samples)
        p10 = sorted_s[int(len(sorted_s) * 0.10)]
        p50 = sorted_s[int(len(sorted_s) * 0.50)]
        p90 = sorted_s[int(len(sorted_s) * 0.90)]
        thresholds = [p10, p50, p90]

    qmd_content = f'''```{{python}}
#| echo: false
#| fig-cap: "Probability of Exceeding Threshold: {display_name}"

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from dih_models.plotting.chart_style import (
    setup_chart_style, add_watermark, clean_spines, get_tick_formatter,
    COLOR_BLACK, COLOR_WHITE, add_png_metadata, get_figure_output_path
)
from dih_models.parameters import format_parameter_value

setup_chart_style()

# Monte Carlo samples

samples = {samples[:2000] if len(samples) > 2000 else samples}
thresholds = {thresholds}
display_name = "{display_name}"
units = "{units}"

# Calculate exceedance probabilities (1 - CDF)

sorted_samples = np.sort(samples)
exceedance = 1 - np.arange(1, len(sorted_samples) + 1) / len(sorted_samples)

# Create figure

fig, ax = plt.subplots(figsize=(10, 6))

# Plot exceedance curve

ax.plot(sorted_samples, exceedance * 100, color=COLOR_BLACK, linewidth=2.5)
ax.fill_between(sorted_samples, 0, exceedance * 100, alpha=0.1, color=COLOR_BLACK)

# Apply tick formatter for readable labels (K, M, B suffixes, $ for USD)

ax.xaxis.set_major_formatter(get_tick_formatter(unit=units))

# Annotate thresholds

for thresh in thresholds:
    exceed_pct = (np.array(samples) >= thresh).sum() / len(samples) * 100
    ax.axvline(thresh, color=COLOR_BLACK, linestyle='--', linewidth=1, alpha=0.5)
    ax.axhline(exceed_pct, color=COLOR_BLACK, linestyle=':', linewidth=1, alpha=0.3)

    # Add label with formatted threshold value (use format_parameter_value for full units)

    ax.annotate(f'{{exceed_pct:.0f}}% chance\\n≥ {{format_parameter_value(thresh, units)}}',
                xy=(thresh, exceed_pct), xytext=(thresh * 1.05, exceed_pct + 5),
                fontsize=10, ha='left', weight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK, alpha=0.9))

ax.set_xlabel(f'{{display_name}} ({{units}})' if units else display_name, fontsize=12)
ax.set_ylabel('Probability of Exceeding Value (%)', fontsize=12)
ax.set_title(f'Exceedance Probability: {{display_name}}', fontsize=14, weight='bold', pad=15)
ax.set_ylim(0, 100)
ax.set_xlim(left=min(sorted_samples) * 0.95)

clean_spines(ax)
add_watermark(fig)

# Save PNG to knowledge/figures/ regardless of where Quarto renders from

output_path = get_figure_output_path('exceedance-{param_name.lower()}.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=COLOR_WHITE)

add_png_metadata(
    output_path,
    title=f'Exceedance: {{display_name}}',
    description=f'Probability of {{display_name}} exceeding various thresholds'
)

plt.show()
```

*This exceedance probability chart shows the likelihood that {display_name} will exceed any given threshold. Higher curves indicate more favorable outcomes with greater certainty.*
'''

    # Write QMD file
    output_file = output_dir / f'exceedance-{param_name.lower()}.qmd'
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

    # Initialize uncertainty module now that dependencies are ready
    init_uncertainty()

    # Parse parameters file THIRD (now reference_ids.py is up to date)
    parameters_path = project_root / "dih_models" / "parameters.py"
    if not parameters_path.exists():
        print(f"[ERROR] Parameters file not found: {parameters_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Parsing {parameters_path}...")
    parameters = parse_parameters_file(parameters_path)
    print(f"[OK] Found {len(parameters)} numeric parameters")
    print()

    # Track fatal validation errors
    has_fatal_error = False

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
        # Mark as fatal error so we exit with code 1 at the end
        has_fatal_error = True
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
        print("\n[WARN] Consider adding 'formula' or 'latex' to these parameters", file=sys.stderr)
        print("[WARN] Or change source_type to 'definition' if they're intentional estimates", file=sys.stderr)
        print()
    else:
        print("[OK] All calculated parameters have formulas or latex equations")
        print()

    # Validate calculated parameters don't have their own uncertainty (should derive from inputs)
    print("[*] Validating uncertainty is only on input parameters...")
    uncertainty_problems = validate_calculated_params_no_uncertainty(parameters)

    if uncertainty_problems:
        print(f"[ERROR] Found {len(uncertainty_problems)} calculated parameters with their own uncertainty:", file=sys.stderr)
        for param_name, issues in uncertainty_problems:
            print(f"  - {param_name} has: {', '.join(issues)}", file=sys.stderr)
        print(file=sys.stderr)
        print("[ERROR] Calculated parameters should derive uncertainty from inputs via compute function.", file=sys.stderr)
        print("[ERROR] Remove confidence_interval/distribution/std_error from these calculated parameters.", file=sys.stderr)
        print("[ERROR] Add uncertainty to their INPUT parameters instead.", file=sys.stderr)
        has_fatal_error = True
        print()
    else:
        print("[OK] All calculated parameters derive uncertainty from inputs")
        print()

    # Validate formula strings use full parameter names (informational only)
    # Note: LaTeX auto-generation now infers operation from compute(), so formula is optional
    print("[*] Checking formula strings (informational)...")
    formula_mismatches = validate_formula_uses_full_param_names(parameters)

    if formula_mismatches:
        print(f"[INFO] {len(formula_mismatches)} formulas use abbreviated names (this is OK - operation inferred from compute)")
        # Only show details if there are few
        if len(formula_mismatches) <= 5:
            for param_name, missing_input, formula in formula_mismatches:
                print(f"       {param_name}: \"{formula}\"")
        print()
    else:
        print("[OK] All formulas use full parameter names")
        print()

    # Validate compute functions match inputs list
    print("[*] Validating compute functions match inputs list...")
    compute_issues = validate_compute_inputs_match(parameters, parameters_path)

    if compute_issues:
        missing_issues = [(p, v) for p, t, v in compute_issues if t == 'missing_from_inputs']
        extra_issues = [(p, v) for p, t, v in compute_issues if t == 'extra_in_inputs']

        if missing_issues:
            print(f"[ERROR] {len(missing_issues)} parameters use ctx[] vars not in inputs list:", file=sys.stderr)
            for param_name, missing_vars in missing_issues[:10]:
                print(f"  - {param_name}: missing {missing_vars}", file=sys.stderr)
            if len(missing_issues) > 10:
                print(f"  ... and {len(missing_issues) - 10} more", file=sys.stderr)
            print(file=sys.stderr)
            print("[ERROR] Add these to the 'inputs' list for proper uncertainty propagation.", file=sys.stderr)
            has_fatal_error = True

        if extra_issues:
            print(f"[WARN] {len(extra_issues)} parameters have unused inputs (not fatal):")
            for param_name, extra_vars in extra_issues[:5]:
                print(f"  - {param_name}: unused {extra_vars}")
        print()
    else:
        print("[OK] All compute functions match their inputs list")
        print()

    # Validate inline calculations have inputs/compute metadata
    print("[*] Checking for inline calculations missing inputs/compute...")
    inline_issues = validate_inline_calculations_have_compute(parameters, parameters_path)

    if inline_issues:
        print(f"[ERROR] {len(inline_issues)} parameters have inline calculations but no inputs/compute:", file=sys.stderr)
        for param_name, first_arg in inline_issues[:10]:
            print(f"  - {param_name}: {first_arg}...", file=sys.stderr)
        if len(inline_issues) > 10:
            print(f"  ... and {len(inline_issues) - 10} more", file=sys.stderr)
        print(file=sys.stderr)
        print("[ERROR] Add 'inputs' and 'compute' to these parameters for uncertainty propagation.", file=sys.stderr)
        has_fatal_error = True
        print()
    else:
        print("[OK] All inline calculations have inputs/compute metadata")
        print()

    # Exit early if validation errors found
    if has_fatal_error:
        print("[FATAL] Validation errors found. Fix the issues above before continuing.", file=sys.stderr)
        sys.exit(1)

    # Generate _variables.yml
    print(f"[*] Generating _variables.yml (citation mode: {citation_mode})...")
    output_path = project_root / "_variables.yml"
    generate_variables_yml(parameters, output_path, citation_mode=citation_mode, params_file=parameters_path)
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
            from dih_models.uncertainty import simulate_with_propagation as _sim, one_at_a_time_sensitivity as _sens
            # Use fixed seed for reproducibility (avoids git churn from random variation)
            RANDOM_SEED = 42
            sims = _sim(parameters, n=10000, seed=RANDOM_SEED)
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

            # Generate input distribution charts for parameters with uncertainty metadata
            print("[*] Generating input distribution charts...")
            input_dist_figures_dir = project_root / "knowledge" / "figures"
            input_dist_figures_dir.mkdir(parents=True, exist_ok=True)

            # First, delete stale QMD files (we regenerate all)
            stale_dist_qmd = list(input_dist_figures_dir.glob("distribution-*.qmd"))
            if stale_dist_qmd:
                print(f"[*] Cleaning {len(stale_dist_qmd)} existing distribution QMD files...")
                for f in stale_dist_qmd:
                    f.unlink()

            input_dist_count = 0
            input_dist_errors = []
            generated_dist_qmds = set()  # Track what we generate
            for param_name, param_data in parameters.items():
                try:
                    # Only generate for parameters with uncertainty metadata
                    dist_file = generate_input_distribution_chart_qmd(
                        param_name, param_data, input_dist_figures_dir
                    )
                    generated_dist_qmds.add(dist_file.name)
                    input_dist_count += 1
                except ValueError:
                    # Parameter doesn't have uncertainty metadata - skip silently
                    pass
                except Exception as e:
                    input_dist_errors.append(f"{param_name}: {e}")

            # Clean up orphaned PNG files (PNGs without matching QMD)
            orphaned_dist_pngs = []
            for png_file in input_dist_figures_dir.glob("distribution-*.png"):
                expected_qmd = png_file.stem + ".qmd"
                if expected_qmd not in generated_dist_qmds:
                    orphaned_dist_pngs.append(png_file)
            if orphaned_dist_pngs:
                print(f"[*] Cleaning {len(orphaned_dist_pngs)} orphaned distribution PNG files...")
                for f in orphaned_dist_pngs:
                    f.unlink()

            print(f"[OK] Generated {input_dist_count} input distribution charts in knowledge/figures/")
            for err in input_dist_errors:
                print(f"[WARN] {err}")

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

                figures_dir = project_root / "knowledge" / "figures"

                # Delete stale QMD files first (we regenerate all)
                # PNGs will be cleaned up after generation (only orphans)
                stale_tornado_qmd = list(figures_dir.glob("tornado-*.qmd"))
                stale_sensitivity_qmd = list(figures_dir.glob("sensitivity-table-*.qmd"))
                stale_mc_dist_qmd = list(figures_dir.glob("mc-distribution-*.qmd"))
                stale_exceedance_qmd = list(figures_dir.glob("exceedance-*.qmd"))
                stale_qmd_files = stale_tornado_qmd + stale_sensitivity_qmd + stale_mc_dist_qmd + stale_exceedance_qmd

                if stale_qmd_files:
                    print(f"[*] Cleaning {len(stale_qmd_files)} existing QMD files...")
                    for f in stale_qmd_files:
                        f.unlink()

                # Track generated QMD files for orphan PNG cleanup later
                generated_outcome_qmds = set()

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
                    print(f"\n[ERROR] {len(validation_warnings)} calculated parameters missing inputs/compute:", file=sys.stderr)
                    # Show ALL warnings - do not truncate
                    for warning in validation_warnings:
                        print(f"  - {warning}", file=sys.stderr)
                    print("\n[ERROR] Calculated parameters MUST have 'inputs' and 'compute' defined.", file=sys.stderr)
                    print("[ERROR] Options to fix:", file=sys.stderr)
                    print("[ERROR]   1. Add inputs=[] and compute=lambda ctx: ... to the Parameter", file=sys.stderr)
                    print("[ERROR]   2. Change source_type='definition' if it's an estimate/assumption", file=sys.stderr)
                    print("[ERROR]   3. Change source_type='external' if it comes from a source", file=sys.stderr)
                    sys.exit(1)

                # Validate: Check for leaf input parameters missing uncertainty metadata
                # These cause zero-variance Monte Carlo outputs, making distribution charts meaningless

                def get_all_leaf_inputs(param_name: str, visited: set = None) -> set:
                    """Recursively find all leaf (non-calculated) inputs for a parameter."""
                    if visited is None:
                        visited = set()
                    if param_name in visited:
                        return set()
                    visited.add(param_name)

                    meta = parameters.get(param_name, {})
                    val = meta.get("value")

                    # If has inputs, recurse
                    if hasattr(val, "inputs") and val.inputs:
                        leaves = set()
                        for inp in val.inputs:
                            leaves.update(get_all_leaf_inputs(inp, visited))
                        return leaves
                    else:
                        # This is a leaf parameter
                        return {param_name}

                def has_uncertainty(val) -> bool:
                    """Check if a parameter has uncertainty metadata."""
                    has_dist = hasattr(val, "distribution") and val.distribution
                    has_std = hasattr(val, "std_error") and val.std_error
                    has_ci = hasattr(val, "confidence_interval") and val.confidence_interval
                    return bool(has_dist or has_std or has_ci)

                # Collect ALL leaf parameters that are used in calculations but lack uncertainty
                all_deterministic_leaves = set()
                all_uncertain_leaves = set()

                for param_name, meta in parameters.items():
                    val = meta.get("value")
                    if hasattr(val, "compute") and val.compute and hasattr(val, "inputs") and val.inputs:
                        # Find all leaf inputs for this calculated param
                        leaf_inputs = get_all_leaf_inputs(param_name)
                        for leaf in leaf_inputs:
                            leaf_meta = parameters.get(leaf, {})
                            leaf_val = leaf_meta.get("value")
                            if has_uncertainty(leaf_val):
                                all_uncertain_leaves.add(leaf)
                            else:
                                all_deterministic_leaves.add(leaf)

                # Only flag deterministic leaves that aren't also uncertain (some params may be checked multiple times)
                truly_deterministic = all_deterministic_leaves - all_uncertain_leaves

                if truly_deterministic:
                    print(f"\n[ERROR] {len(truly_deterministic)} leaf input parameters lack uncertainty metadata:", file=sys.stderr)
                    print("[ERROR] These cause zero-variance Monte Carlo outputs for calculated parameters.", file=sys.stderr)
                    for leaf in sorted(truly_deterministic)[:20]:  # Show first 20
                        leaf_meta = parameters.get(leaf, {})
                        leaf_val = leaf_meta.get("value")
                        val_str = f"{float(leaf_val):,.4g}" if leaf_val is not None else "?"
                        print(f"  - {leaf} = {val_str}", file=sys.stderr)
                    if len(truly_deterministic) > 20:
                        print(f"  ... and {len(truly_deterministic) - 20} more", file=sys.stderr)
                    print("\n[ERROR] To fix: Add one of these to each leaf parameter:", file=sys.stderr)
                    print("[ERROR]   - distribution='normal' + std_error=<value>", file=sys.stderr)
                    print("[ERROR]   - distribution='lognormal' + std_error=<value>", file=sys.stderr)
                    print("[ERROR]   - confidence_interval=(low, high)", file=sys.stderr)
                    print("[ERROR] Monte Carlo analysis requires uncertainty on ALL input parameters.", file=sys.stderr)
                    sys.exit(1)

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

                # Counters for summary output
                tornado_count = 0
                sensitivity_count = 0
                mc_dist_count = 0
                exceedance_count = 0
                analysis_json_count = 0

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
                            analysis_json_count += 1

                            # Generate tornado chart QMD
                            try:
                                figures_dir = project_root / "knowledge" / "figures"
                                param_meta = parameters.get(outcome.name, {})
                                tornado_qmd = generate_tornado_chart_qmd(
                                    outcome.name, tornado, figures_dir, param_meta,
                                    baseline=float(baseline),
                                    units=outcome.units
                                )
                                generated_outcome_qmds.add(tornado_qmd.name)
                                tornado_count += 1
                            except ValueError as val_err:
                                # STRICT MODE: Fail fast when tornado data is incomplete
                                # This forces developers to either:
                                # 1. Add proper inputs/compute to intermediate calculated parameters
                                # 2. Change source_type to "definition" if not truly calculated
                                # 3. Add uncertainty distributions to leaf input parameters
                                print(f"[ERROR] {val_err}", file=sys.stderr)
                                print(f"[ERROR] Parameter '{outcome.name}' has inputs/compute but no tornado sensitivity.", file=sys.stderr)
                                print("[ERROR] This usually means:", file=sys.stderr)
                                print("[ERROR]   - Input parameters need uncertainty distributions (std_error, confidence_interval, or distribution)", file=sys.stderr)
                                print("[ERROR]   - OR intermediate inputs need their own inputs/compute definitions", file=sys.stderr)
                                print("[ERROR]   - OR this should be source_type='definition' instead of 'calculated'", file=sys.stderr)
                                sys.exit(1)
                            except Exception as chart_err:
                                print(f"[ERROR] Failed to generate tornado chart for {outcome.name}: {chart_err}", file=sys.stderr)
                                sys.exit(1)

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
                            analysis_json_count += 1

                            # Generate sensitivity table QMD only if there's meaningful variance
                            # Skip tables where all coefficients are effectively zero (< 0.001)
                            max_coef = max(abs(v) for v in sens_indices.values()) if sens_indices else 0
                            if max_coef >= 0.001:
                                try:
                                    sens_qmd = generate_sensitivity_table_qmd(outcome.name, sens_indices, figures_dir, param_meta)
                                    generated_outcome_qmds.add(sens_qmd.name)
                                    sensitivity_count += 1
                                except Exception as table_err:
                                    print(f"[WARN] Failed to generate sensitivity table for {outcome.name}: {table_err}")

                            # Generate Monte Carlo distribution chart
                            # Skip if zero variance (all samples identical) - these are meaningless
                            try:
                                outcome_info = outcomes_data.get(outcome.name, {})
                                outcome_std = outcome_info.get("std", 0)
                                if outcome_samples and len(outcome_samples) > 100 and outcome_std > 0:
                                    mc_qmd = generate_monte_carlo_distribution_chart_qmd(
                                        outcome.name,
                                        outcome_info,
                                        outcome_samples,
                                        figures_dir,
                                        param_meta
                                    )
                                    generated_outcome_qmds.add(mc_qmd.name)
                                    mc_dist_count += 1

                                    # Generate standalone CDF/exceedance chart
                                    cdf_qmd = generate_cdf_chart_qmd(
                                        outcome.name,
                                        outcome_samples,
                                        figures_dir,
                                        param_meta
                                    )
                                    generated_outcome_qmds.add(cdf_qmd.name)
                                    exceedance_count += 1
                                elif outcome_samples and outcome_std == 0:
                                    print(f"[SKIP] MC distribution chart for {outcome.name}: zero variance (deterministic)")
                            except Exception as mc_err:
                                print(f"[WARN] Failed to generate MC distribution charts for {outcome.name}: {mc_err}")
                    except Exception as e:
                        print(f"[WARN] Skipped outcome {outcome.name}: {e}")

                with open(analysis_dir / "outcomes.json", "w", encoding="utf-8") as f:
                    json.dump(outcomes_data, f, indent=2)

                # Clean up orphaned PNG files (PNGs without matching QMD)
                orphaned_pngs = []
                for png_file in figures_dir.glob("tornado-*.png"):
                    expected_qmd = png_file.stem + ".qmd"
                    if expected_qmd not in generated_outcome_qmds:
                        orphaned_pngs.append(png_file)
                for png_file in figures_dir.glob("sensitivity-table-*.png"):
                    expected_qmd = png_file.stem + ".qmd"
                    if expected_qmd not in generated_outcome_qmds:
                        orphaned_pngs.append(png_file)
                for png_file in figures_dir.glob("mc-distribution-*.png"):
                    expected_qmd = png_file.stem + ".qmd"
                    if expected_qmd not in generated_outcome_qmds:
                        orphaned_pngs.append(png_file)
                for png_file in figures_dir.glob("exceedance-*.png"):
                    expected_qmd = png_file.stem + ".qmd"
                    if expected_qmd not in generated_outcome_qmds:
                        orphaned_pngs.append(png_file)

                if orphaned_pngs:
                    print(f"[*] Cleaning {len(orphaned_pngs)} orphaned PNG files...")
                    for f in orphaned_pngs:
                        f.unlink()

                # Print summary of generated files
                print(f"[OK] Generated {tornado_count} tornado charts in knowledge/figures/")
                print(f"[OK] Generated {sensitivity_count} sensitivity tables in knowledge/figures/")
                print(f"[OK] Generated {mc_dist_count} MC distribution charts in knowledge/figures/")
                print(f"[OK] Generated {exceedance_count} exceedance charts in knowledge/figures/")
                print(f"[OK] Wrote {analysis_json_count + 2} analysis JSON files to _analysis/")

                # Discount rate sensitivity for ROI_complete
                try:
                    roi_outcome = next((o for o in analyzable_params if "ROI" in o.name.upper() and "COMPLETE" in o.name.upper()), None)
                    if roi_outcome:
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
                except Exception as e:
                    print(f"[WARN] Discount curve generation skipped: {e}")

                # Scenario bands for ROI_complete
                try:
                    roi_outcome = next((o for o in analyzable_params if "ROI" in o.name.upper() and "COMPLETE" in o.name.upper()), None)
                    if roi_outcome:
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
                except Exception as e:
                    print(f"[WARN] Scenario bands generation skipped: {e}")

            print()
        else:
            print("[WARN] Uncertainty module unavailable; skipping uncertainty summaries.")
            print()
    except Exception as e:
        print(f"[WARN] Uncertainty generation skipped: {e}")
        print()

    # Generate parameters-and-calculations.qmd AFTER uncertainty charts are created
    # so the file existence checks work correctly
    print("[*] Generating parameters-and-calculations.qmd...")
    qmd_output = project_root / "knowledge" / "appendix" / "parameters-and-calculations.qmd"
    generate_parameters_qmd(parameters, qmd_output, available_refs=available_refs, params_file=parameters_path)
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
    print("       - OUTLINE-GENERATED.MD")
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
