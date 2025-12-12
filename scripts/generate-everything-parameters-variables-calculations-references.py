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
    python scripts/generate-everything-parameters-variables-calculations-references.py [options]

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
    python scripts/generate-everything-parameters-variables-calculations-references.py

    # Inline citations for peer-reviewed sources
    python scripts/generate-everything-parameters-variables-calculations-references.py --cite-mode=inline

    # Separate citation variables (flexible usage)
    python scripts/generate-everything-parameters-variables-calculations-references.py --cite-mode=separate

    # Both inline AND separate (maximum flexibility)
    python scripts/generate-everything-parameters-variables-calculations-references.py --cite-mode=both

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

# Import all generator modules
from dih_models.bibtex_generator import generate_bibtex
from dih_models.chart_generators import (
    generate_tornado_chart_qmd,
    generate_sensitivity_table_qmd,
    generate_input_distribution_chart_qmd,
    generate_monte_carlo_distribution_chart_qmd,
    generate_cdf_chart_qmd,
)
from dih_models.latex_generation import (
    generate_auto_latex,
    format_latex_value,
    create_latex_variable_name,
    create_short_label,
    infer_operation_from_compute,
    extract_lambda_body_from_file,
    lambda_to_sympy_latex,
)
from dih_models.parameters_and_calculations_qmd_generator import (
    generate_parameters_and_calculations_qmd,
)
from dih_models.quarto_formatting import (
    generate_html_with_tooltip,
)
from dih_models.reference_ids_generator import generate_reference_ids_enum
from dih_models.reference_parser import (
    parse_references_qmd_detailed,
    parse_references_qmd,
    sanitize_bibtex_key,
)
from dih_models.typescript_generator import generate_typescript_parameters, generate_typescript_survey
from dih_models.validation import (
    validate_references,
    validate_calculated_parameters,
    validate_calculated_params_no_uncertainty,
    validate_formula_uses_full_param_names,
    validate_compute_inputs_match,
    validate_inline_calculations_have_compute,
)
from dih_models.variables_yml_generator import generate_variables_yml

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



# LaTeX generation functions moved to dih_models/latex_generation.py
# (smart_title_case, infer_operation_from_compute, extract_lambda_body_from_file,
#  lambda_to_sympy_latex, generate_auto_latex, format_latex_value,
#  create_short_label, create_latex_variable_name)


# HTML/Quarto formatting functions moved to dih_models/quarto_formatting.py:
# - convert_qmd_to_html()
# - generate_html_with_tooltip()
# - generate_uncertainty_section()


# Generator functions moved to dih_models/ for better code organization:
# - generate_variables_yml() -> dih_models/variables_yml_generator.py
# - generate_reference_ids_enum() -> dih_models/reference_ids_generator.py
# - generate_bibtex() -> dih_models/bibtex_generator.py
# - generate_parameters_and_calculations_qmd() -> dih_models/parameters_and_calculations_qmd_generator.py
# - generate_uncertainty_section() -> dih_models/quarto_formatting.py
# - Chart generation functions (5 functions) -> dih_models/chart_generators.py


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


# Chart generation functions moved to scripts/chart_generators.py
# - generate_tornado_chart_qmd() -> chart_generators
# - generate_sensitivity_table_qmd() -> chart_generators
# - generate_input_distribution_chart_qmd() -> chart_generators
# - generate_monte_carlo_distribution_chart_qmd() -> chart_generators
# - generate_cdf_chart_qmd() -> chart_generators


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
        print(f"[ERROR] Found {len(suspicious_params)} calculated parameters without formula/latex:", file=sys.stderr)
        for param_name, value in suspicious_params[:10]:  # Show first 10
            print(f"  - {param_name} = {value:,.2f} (marked as calculated but no formula)", file=sys.stderr)
        if len(suspicious_params) > 10:
            print(f"  ... and {len(suspicious_params) - 10} more", file=sys.stderr)
        print(file=sys.stderr)
        print("[ERROR] Calculated parameters MUST have 'formula' or 'latex' attributes.", file=sys.stderr)
        print("[ERROR] If these are intentional estimates, change source_type to 'definition'.", file=sys.stderr)
        has_fatal_error = True
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

    # Generate TypeScript parameters file for Next.js/React apps
    print("[*] Generating TypeScript parameters file...")
    ts_output = project_root / "dih_models" / "parameters-calculations-citations.ts"
    generate_typescript_parameters(parameters, ts_output, include_metadata=True, references_path=references_path)
    print()

    # Generate TypeScript survey file (if survey exists)
    print("[*] Generating TypeScript survey file...")
    survey_json = project_root / "_analysis" / "economist-survey.json"
    ts_survey_output = project_root / "dih_models" / "economist-survey.ts"
    generate_typescript_survey(survey_json, ts_survey_output)
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
    generate_parameters_and_calculations_qmd(parameters, qmd_output, available_refs=available_refs, params_file=parameters_path)
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
    print(f"       - {ts_output.relative_to(project_root)}")
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
