#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Variables YAML generation utilities for dih_models
===================================================

Generate _variables.yml from parameter metadata for Quarto.

Functions:
- generate_variables_yml() - Generate _variables.yml with formatted parameters

Usage:
    from dih_models.variables_yml_generator import generate_variables_yml
    from pathlib import Path

    # Generate variables YAML file
    output_path = Path("_variables.yml")
    generate_variables_yml(parameters, output_path, citation_mode="separate")
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional
import json

logger = logging.getLogger("dih.variables_yml")

import yaml

import html
import re

from dih_models.latex_generation import generate_auto_latex, generate_expanded_latex, LATEX_BLOCK_SEP
from dih_models.latex_mobile_wrap import wrap_latex_for_mobile
from dih_models.quarto_formatting import generate_html_with_tooltip
from dih_models.reference_parser import sanitize_bibtex_key
from dih_models.formatting import format_parameter_value
from dih_models.variable_naming import (
    CITE_VARIABLE_SUFFIX,
    LATEX_VARIABLE_SUFFIX,
    NOUNIT_VARIABLE_SUFFIX,
)


def latex_to_readable_text(latex: str) -> str:
    """
    Convert LaTeX equation to human-readable plain text for screen readers and AI.
    
    This ensures AI models parsing the rendered HTML can understand the equations,
    since MathJax renders LaTeX as character-spaced gibberish in accessibility trees.
    
    Examples:
        Cost_{ann} = \\frac{A}{B} = $10M  →  Cost_ann = (A / B) = $10M
        \\text{Lives} \\times 365  →  Lives × 365
    """
    text = latex
    
    # First, handle escaped dollar signs BEFORE other processing
    # \$ in LaTeX means literal $ sign
    text = text.replace(r'\$', '$')
    
    # Remove LaTeX environments
    text = re.sub(r'\\begin\{aligned\}', '', text)
    text = re.sub(r'\\end\{aligned\}', '', text)
    text = re.sub(r'\\begin\{array\}.*?\\end\{array\}', '[array]', text, flags=re.DOTALL)
    
    # Handle fractions: \frac{A}{B} → (A / B)
    # Use a loop to handle nested fractions
    prev_text = None
    while prev_text != text:
        prev_text = text
        # Match \frac followed by two brace groups
        text = re.sub(
            r'\\frac\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',
            r'(\1 / \2)',
            text
        )
    
    # Handle text blocks: \text{word} → word
    text = re.sub(r'\\text\s*\{([^{}]*)\}', r'\1', text)
    
    # Handle subscripts: _{text} → _text (simplified)
    text = re.sub(r'_\{([^{}]*)\}', r'_\1', text)
    
    # Handle superscripts: ^{text} → ^text  
    text = re.sub(r'\^\{([^{}]*)\}', r'^\1', text)
    
    # Handle underbrace: \underbrace{X}_{label} → X (label)
    text = re.sub(r'\\underbrace\s*\{([^{}]*)\}\s*_\s*\{([^{}]*)\}', r'\1 (\2)', text)
    
    # Replace LaTeX symbols with readable equivalents
    # Order matters: process longer patterns first, escape backslashes properly
    symbol_replacements = [
        (r'\\times', ' × '),
        (r'\\div', ' ÷ '),
        (r'\\cdot', ' · '),
        (r'\\pm', ' ± '),
        (r'\\leq', ' ≤ '),
        (r'\\geq', ' ≥ '),
        (r'\\neq', ' ≠ '),
        (r'\\approx', ' ≈ '),
        (r'\\infty', '∞'),
        (r'\\sum', 'Σ'),
        (r'\\prod', 'Π'),
        (r'\\left\(', '('),
        (r'\\right\)', ')'),
        (r'\\left\[', '['),
        (r'\\right\]', ']'),
        (r'\\quad', ' '),
        (r'\\qquad', '  '),
        (r'\\,', ' '),
        (r'\\;', ' '),
        (r'\\!', ''),
        (r'\\\s', ' '),  # Line breaks in aligned
        (r'\\\\', ' '),  # Double backslash = newline
        (r'&=', ' = '),
        (r'&', ' '),
        (r'\\%', '%'),
    ]
    
    for pattern, replacement in symbol_replacements:
        text = re.sub(pattern, replacement, text)
    
    # Handle sqrt: \sqrt{X} → √(X)
    text = re.sub(r'\\sqrt\s*\{([^{}]*)\}', r'√(\1)', text)
    
    # Handle {,} thousands separator in LaTeX (e.g., 1{,}000 → 1,000)
    text = re.sub(r'\{,\}', ',', text)
    
    # Remove remaining backslash commands we don't recognize
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    
    # Clean up braces
    text = text.replace('{', '').replace('}', '')
    
    # Normalize whitespace (collapse multiple spaces, trim)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def wrap_latex_with_accessibility(latex_content: str, param_name: str = "") -> str:
    """
    Wrap LaTeX equation for display.
    
    Note: Previously this generated HTML wrappers for AI accessibility, but that broke
    PDF/LaTeX compilation because HTML elements aren't valid in LaTeX context.
    Now generates plain $$ blocks that work for both HTML and PDF.
    
    The accessibility metadata (data-latex-source, sr-only text) has been removed
    to ensure cross-format compatibility. AI can still read the rendered MathML/MathJax.
    
    Args:
        latex_content: The LaTeX equation (without $$ delimiters)
        param_name: Parameter name (unused, kept for API compatibility)
        
    Returns:
        LaTeX block with $$ delimiters
    """
    # Simple $$ block that works for both HTML (MathJax) and PDF (LaTeX)
    return f"$$\n{latex_content}\n$$"


class ValueWithCI:
    """Wrapper to override display_value with confidence interval."""
    def __init__(self, original_value: Any, display_override: str):
        self._original = original_value
        self.display_value = display_override
        # Copy all attributes from original
        for attr in dir(original_value):
            if not attr.startswith('_') and attr != 'display_value':
                try:
                    setattr(self, attr, getattr(original_value, attr))
                except (AttributeError, TypeError):
                    pass

    def __float__(self) -> float:
        return float(self._original)


def _format_ci_display(central_value: float, unit: str | None,
                       ci_low: float, ci_high: float,
                       include_unit: bool = True) -> str:
    """Format a value with 95% CI as a display string.

    Args:
        central_value: The central/deterministic value.
        ci_low: Lower bound of confidence interval.
        ci_high: Upper bound of confidence interval.
        unit: Unit string (e.g. "deaths", "USD").
        include_unit: Whether to include the unit text in the formatted output.

    Returns:
        String like "416 million deaths (95% CI: 225 million deaths-630 million deaths)"
        or without units: "416 million (95% CI: 225 million-630 million)"
    """
    central_formatted = format_parameter_value(central_value, unit, include_unit=include_unit, ratio_suffix=False)

    if unit == "percentage":
        ci_low_formatted = f"{ci_low * 100:.0f}%"
        ci_high_formatted = f"{ci_high * 100:.0f}%"
    else:
        ci_low_formatted = format_parameter_value(ci_low, unit, include_unit=include_unit, ratio_suffix=False)
        ci_high_formatted = format_parameter_value(ci_high, unit, include_unit=include_unit, ratio_suffix=False)

    return f"{central_formatted} (95% CI: {ci_low_formatted}-{ci_high_formatted})"


def generate_variables_yml(
    parameters: Dict[str, Dict[str, Any]],
    output_path: Path,
    citation_mode: str = "none",
    params_file: Optional[Path] = None,
    samples_json_path: Optional[Path] = None,
    wrap_latex_width: int = 60
):
    """
    Generate _variables.yml file from parameters.

    Creates YAML with lowercase variable names mapped to formatted HTML values.
    Also exports LaTeX equations as {param_name}_latex variables.

    For calculated parameters with Monte Carlo uncertainty (from samples.json),
    embeds 95% confidence intervals in the base variable value.

    Args:
        parameters: Dict of parameter metadata
        output_path: Path to write _variables.yml
        citation_mode: Citation handling mode:
            - "none": No inline citations (default)
            - "inline": Include [@key] after external peer-reviewed parameters
            - "separate": Export citation keys as {param_name}_cite variables
            - "both": Both inline AND separate variables
        params_file: Path to parameters.py for sympy-based LaTeX generation
        samples_json_path: Optional path to samples.json with Monte Carlo uncertainty data
        wrap_latex_width: Max width for LaTeX equations before wrapping (0 = no wrap)
    """
    variables = {}
    citation_count = 0

    # Load Monte Carlo uncertainty data if available
    uncertainty_data = {}
    if samples_json_path and samples_json_path.exists():
        with open(samples_json_path, "r", encoding="utf-8") as f:
            uncertainty_data = json.load(f)

    # Sort parameters by name for consistent output
    for param_name in sorted(parameters.keys()):
        param_data = parameters[param_name]
        value = param_data["value"]
        comment = param_data["comment"]

        # Use lowercase name for Quarto variables (convention)
        var_name = param_name.lower()

        # Check if this parameter has uncertainty data to embed in display value
        # Priority: 1) Specified confidence_interval on parameter, 2) Monte Carlo derived CI
        value_with_ci = value
        unit = getattr(value, "unit", None)
        central_value = float(value)

        # Check if CI display is suppressed for this parameter
        # Use hide_ci=True on parameters where the CI is misleading or clutters the display
        hide_ci = getattr(value, "hide_ci", False)

        # First, check if parameter has an explicitly specified confidence_interval
        # This is preferred as it represents the author's judgment about plausible ranges
        specified_ci = getattr(value, "confidence_interval", None)

        # Track CI bounds for reuse in _nounit variant
        ci_bounds = None  # (ci_low, ci_high) if meaningful CI exists

        if not hide_ci and specified_ci and len(specified_ci) == 2:
            ci_low, ci_high = specified_ci
            has_meaningful_uncertainty = abs(ci_high - ci_low) > 0.001

            if has_meaningful_uncertainty:
                ci_bounds = (ci_low, ci_high)
                display_value_with_ci = _format_ci_display(central_value, unit, ci_low, ci_high, include_unit=True)
                value_with_ci = ValueWithCI(value, display_value_with_ci)

        # Fall back to Monte Carlo derived CI if no specified CI and not hidden
        elif not hide_ci and param_name in uncertainty_data:
            unc = uncertainty_data[param_name]
            p5 = unc.get("p5")
            p50 = unc.get("p50")
            p95 = unc.get("p95")

            # Only embed CI if there's meaningful uncertainty
            # Skip if p5 == p95 (zero variance) or variance < 0.1% of median
            has_meaningful_uncertainty = False
            if p50 != 0:
                relative_variance = abs(p95 - p5) / abs(p50)
                has_meaningful_uncertainty = relative_variance > 0.001  # >0.1% variance
            else:
                has_meaningful_uncertainty = abs(p95 - p5) > 0

            if has_meaningful_uncertainty:
                ci_bounds = (p5, p95)
                display_value_with_ci = _format_ci_display(central_value, unit, p5, p95, include_unit=True)
                value_with_ci = ValueWithCI(value, display_value_with_ci)

        # Generate formatted HTML with tooltip
        include_inline_citation = citation_mode in ("inline", "both")
        html_value = generate_html_with_tooltip(param_name, value_with_ci, comment, include_citation=include_inline_citation)

        variables[var_name] = html_value

        # Generate _nounit variant if the unit produces visible text
        # Auto-detect: compare formatted output with and without unit
        with_unit = format_parameter_value(central_value, unit, include_unit=True, ratio_suffix=False)
        without_unit = format_parameter_value(central_value, unit, include_unit=False, ratio_suffix=False)
        if with_unit != without_unit:
            # Unit produces visible text (e.g. "deaths", "years") - generate _nounit
            if ci_bounds:
                nounit_display = _format_ci_display(central_value, unit, ci_bounds[0], ci_bounds[1], include_unit=False)
                nounit_value = ValueWithCI(value, nounit_display)
            else:
                nounit_value = value
            nounit_html = generate_html_with_tooltip(param_name, nounit_value, comment, include_citation=include_inline_citation, include_unit=False)
            variables[f"{var_name}{NOUNIT_VARIABLE_SUFFIX}"] = nounit_html

        # Export citation key separately for external sources (if mode enabled)
        if citation_mode in ("separate", "both"):
            if hasattr(value, "source_type") and hasattr(value, "source_ref"):
                source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
                if source_type_str == "external" and value.source_ref:
                    # Sanitize citation key for BibTeX compatibility
                    sanitized_ref = sanitize_bibtex_key(value.source_ref)
                    variables[f"{var_name}{CITE_VARIABLE_SUFFIX}"] = f"@{sanitized_ref}"
                    citation_count += 1

        # Export LaTeX equation: prefer hardcoded (hand-crafted with good labels),
        # fall back to auto-generated EXPANDED equations for params without hardcoded latex
        # Expanded equations show the full derivation chain for maximum transparency
        hardcoded_latex = getattr(value, "latex", None)
        expanded_latex = None
        if not hardcoded_latex:
            # Use expanded (recursive) LaTeX for auto-generated equations only when no
            # handwritten equation exists. This avoids redundant work for parameters that
            # already provide curated LaTeX.
            expanded_latex = generate_expanded_latex(param_name, value, parameters, params_file=params_file)

        if hardcoded_latex:
            # Use hardcoded (preferred - hand-crafted with semantic labels)
            # TODO: Consider expanding hardcoded too by appending derivations of calculated inputs
            latex_var_name = f"{var_name}{LATEX_VARIABLE_SUFFIX}"
            # Apply mobile-friendly wrapping if enabled
            if wrap_latex_width > 0:
                hardcoded_latex = wrap_latex_for_mobile(hardcoded_latex, max_width=wrap_latex_width)
            # Wrap with accessibility metadata for AI and screen readers
            variables[latex_var_name] = wrap_latex_with_accessibility(hardcoded_latex, param_name)
        elif expanded_latex:
            # Use fully expanded auto-generated equations showing complete derivation chain
            latex_var_name = f"{var_name}{LATEX_VARIABLE_SUFFIX}"

            if LATEX_BLOCK_SEP in expanded_latex:
                # Multi-block: split into separate $$ equations for PDF page-breaking.
                # Each block gets its own $$ delimiters; "where:" markdown between them
                # lets LaTeX break pages at natural points.
                eq_blocks = [b.strip() for b in expanded_latex.split(LATEX_BLOCK_SEP)]
                parts = []
                for i, block in enumerate(eq_blocks):
                    if wrap_latex_width > 0:
                        block = wrap_latex_for_mobile(block, max_width=wrap_latex_width)
                    if i == 0:
                        parts.append(f"$$\n{block}\n$$")
                    else:
                        parts.append(f"where:\n\n$$\n{block}\n$$")
                variables[latex_var_name] = '\n\n'.join(parts)
            else:
                # Single block - existing logic
                if wrap_latex_width > 0:
                    expanded_latex = wrap_latex_for_mobile(expanded_latex, max_width=wrap_latex_width)
                variables[latex_var_name] = wrap_latex_with_accessibility(expanded_latex, param_name)

    # Count exports by type BEFORE adding metadata variables
    latex_count = sum(1 for k in variables.keys() if k.endswith(LATEX_VARIABLE_SUFFIX))
    cite_count = sum(1 for k in variables.keys() if k.endswith(CITE_VARIABLE_SUFFIX))
    nounit_count = sum(1 for k in variables.keys() if k.endswith(NOUNIT_VARIABLE_SUFFIX))
    param_count = len(variables) - latex_count - cite_count - nounit_count

    # Add metadata variables for use in QMD files
    variables["total_parameter_count"] = str(param_count)
    variables["total_latex_equation_count"] = str(latex_count)
    variables["total_nounit_variant_count"] = str(nounit_count)
    if citation_mode in ("separate", "both"):
        variables["total_citation_count"] = str(cite_count)

    # Write YAML file
    with open(output_path, "w", encoding="utf-8", newline='\n') as f:
        # Add header comment
        f.write("# AUTO-GENERATED FILE - DO NOT EDIT\n")
        f.write("# Generated from dih_models/parameters.py\n")
        f.write("# Run: python scripts/generate-everything-parameters-variables-calculations-references.py\n")
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
        # Use a very large width to avoid line-wrapping that can split LaTeX commands (e.g., "\times")
        yaml.dump(
            variables,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            default_style='"',
            width=1000000
        )

    logger.debug(f"[OK] Generated {output_path}")
    logger.debug(f"     {param_count} parameters exported")
    logger.debug(f"     {nounit_count} _nounit variants exported")
    logger.debug(f"     {latex_count} LaTeX equations exported")
    if citation_mode in ("separate", "both"):
        logger.debug(f"     {cite_count} citation keys exported")
    if citation_mode in ("inline", "both"):
        logger.debug("     Citation mode: inline [@key] for peer-reviewed sources")
    logger.debug("\nUsage in QMD files:")
    logger.debug(f"  {{{{< var {list(variables.keys())[0]} >}}}}")
    if latex_count > 0:
        # Find first latex equation
        latex_var = next((k for k in variables.keys() if k.endswith(LATEX_VARIABLE_SUFFIX)), None)
        if latex_var:
            logger.debug(f"  {{{{< var {latex_var} >}}}}  (equation)")
    if cite_count > 0:
        # Find first parameter with citation
        cite_var = next((k for k in variables.keys() if k.endswith(CITE_VARIABLE_SUFFIX)), None)
        if cite_var:
            base_var = cite_var[:-5]  # Remove "_cite"
            logger.debug(f"  {{{{< var {base_var} >}}}} {{{{< var {cite_var} >}}}}")
