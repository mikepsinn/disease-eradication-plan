#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parameter validation utilities for dih_models
==============================================

Validation functions for ensuring parameter quality and consistency.

Functions:
- validate_references() - Check external source_refs exist in references.qmd
- validate_calculated_parameters() - Ensure calculated params use formulas
- validate_calculated_params_no_uncertainty() - Prevent double-counting uncertainty
- validate_formula_uses_full_param_names() - Validate formula strings
- validate_compute_inputs_match() - Validate compute function inputs
- validate_inline_calculations_have_compute() - Check inline calcs have metadata

Usage:
    from dih_models.validation import validate_references, validate_calculated_parameters

    # Validate references
    missing, used = validate_references(parameters, available_refs)
    if missing:
        print(f"Missing references: {missing}")

    # Validate calculated parameters
    suspicious = validate_calculated_parameters(parameters)
    if suspicious:
        print(f"Suspicious calculated params: {suspicious}")
"""

import re
from pathlib import Path
from typing import Any, Dict


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
