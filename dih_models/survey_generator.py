#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Survey Question Generator - Fully Programmatic
==============================================

Generate economist validation survey questions entirely from parameter metadata.
No manual question writing - all questions derived from Parameter properties.

Usage:
    from dih_models.survey_generator import generate_survey
    survey = generate_survey(parameters, sensitivity_analysis, usage_analysis)
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

from dih_models.formatting import format_parameter_value
from dih_models.reference_parser import parse_references_qmd_detailed

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


class QuestionType(str, Enum):
    """Question types for survey"""
    RATING = "rating"           # 1-5 scale
    BOOLEAN = "boolean"         # Yes/No
    NUMERIC_RANGE = "range"     # Lower/upper bounds
    MULTIPLE_CHOICE = "choice"  # Select one
    CHECKLIST = "checklist"     # Select multiple
    TEXT = "text"               # Free text


@dataclass
class SurveyQuestion:
    """A single survey question"""
    question_id: str
    question_text: str
    question_type: QuestionType
    options: List[str] = None
    context: Dict[str, Any] = None
    required: bool = True
    conditional_on: str = None  # Show only if another question meets condition


class QuestionGenerator:
    """Generate survey questions from parameter metadata"""

    def __init__(self, sensitivity_data: Dict = None, usage_data: Dict = None, all_parameters: Dict = None):
        """
        Args:
            sensitivity_data: From _analysis/sensitivity.json
            usage_data: From document usage analysis
            all_parameters: All parameters dict (for resolving display names in formulas)
        """
        self.sensitivity_data = sensitivity_data or {}
        self.usage_data = usage_data or {}
        self.all_parameters = all_parameters or {}

    def generate_questions_for_parameter(
        self,
        param_name: str,
        param_data: Dict[str, Any]
    ) -> List[SurveyQuestion]:
        """
        Generate all questions for a parameter based on its metadata.

        Returns list of questions in order they should be asked.
        """
        questions = []
        value = param_data.get("value")

        # Get source_type from value object
        source_type_str = ""
        if hasattr(value, "source_type"):
            source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)

        # Generate type-specific questions
        if source_type_str == "external":
            questions.extend(self._questions_external(param_name, param_data))
        elif source_type_str == "calculated":
            questions.extend(self._questions_calculated(param_name, param_data))
        elif source_type_str == "definition":
            questions.extend(self._questions_definition(param_name, param_data))

        # Add universal questions (if applicable)
        questions.extend(self._questions_uncertainty(param_name, param_data))
        questions.extend(self._questions_impact(param_name, param_data))

        return questions

    def _questions_external(self, param_name: str, param_data: Dict) -> List[SurveyQuestion]:
        """Generate questions for EXTERNAL parameters (from literature/data sources)"""
        questions = []
        value = param_data["value"]

        # Get metadata
        source_ref = getattr(value, "source_ref", "")
        description = getattr(value, "description", "")
        display_name = getattr(value, "display_name", "") or self._format_param_name(param_name)
        peer_reviewed = getattr(value, "peer_reviewed", False)
        confidence = getattr(value, "confidence", "")
        last_updated = getattr(value, "last_updated", "")

        # Q1: Source credibility rating
        questions.append(SurveyQuestion(
            question_id=f"{param_name}_source_credibility",
            question_text=f"Rate the credibility of this source for estimating: {display_name}",
            question_type=QuestionType.RATING,
            options=["1 (Not credible)", "2", "3 (Somewhat credible)", "4", "5 (Highly credible)", "Not qualified to assess"],
            context={
                "source_ref": source_ref,
                "peer_reviewed": peer_reviewed,
                "confidence": confidence,
                "last_updated": last_updated,
                "parameter_name": param_name
            },
            required=True
        ))

        # Q2: Central value reasonableness
        formatted_value = self._format_value(value)
        unit_suffix = self._get_unit_suffix(param_name, value)
        questions.append(SurveyQuestion(
            question_id=f"{param_name}_value_reasonable",
            question_text=f"Is the central estimate of {formatted_value}{unit_suffix} reasonable?",
            question_type=QuestionType.BOOLEAN,
            options=["Yes", "No"],
            context={
                "value": float(value),
                "unit": getattr(value, "unit", ""),
                "description": description
            },
            required=True
        ))

        # Q3: Better source available? (conditional)
        questions.append(SurveyQuestion(
            question_id=f"{param_name}_better_source",
            question_text="Do you know of a better or more recent source?",
            question_type=QuestionType.TEXT,
            context={"placeholder": "Enter source/citation or leave blank"},
            required=False,
            conditional_on=f"{param_name}_source_credibility <= 3"
        ))

        return questions

    def _questions_calculated(self, param_name: str, param_data: Dict) -> List[SurveyQuestion]:
        """Generate questions for CALCULATED parameters (derived from formulas)"""
        questions = []
        value = param_data["value"]

        # Get metadata
        formula = getattr(value, "formula", "")
        inputs = getattr(value, "inputs", [])
        description = getattr(value, "description", "")
        display_name = getattr(value, "display_name", "") or self._format_param_name(param_name)

        # Format for readability
        formula_readable = self._format_formula_readable(formula)
        inputs_readable = self._format_inputs_readable(inputs) if inputs else ""
        result_formatted = self._format_value(value)
        calculation_example = self._format_calculation_example(formula, value, inputs)

        # Q1: Formula soundness
        unit_suffix = self._get_unit_suffix(param_name, value)
        question_text = f"Is the calculation methodology sound for: **{display_name}**?\n\n**Current result:** {result_formatted}{unit_suffix}"
        if calculation_example:
            question_text += f"\n**Calculation:** {calculation_example}"

        questions.append(SurveyQuestion(
            question_id=f"{param_name}_formula_sound",
            question_text=question_text,
            question_type=QuestionType.MULTIPLE_CHOICE,
            options=[
                "Yes - formula is appropriate",
                "No - wrong functional form",
                "No - missing key factors",
                "No - includes inappropriate factors",
                "Unsure - need more detail"
            ],
            context={
                "formula": formula,
                "formula_readable": formula_readable,
                "calculation_example": calculation_example,
                "result_value": float(value),
                "result_formatted": result_formatted,
                "description": description,
                "parameter_name": param_name
            },
            required=True
        ))

        # Q2: Input factors appropriate (if inputs available)
        if inputs:
            # Format inputs as bullet list with values
            inputs_with_values = []
            for input_param in inputs:
                input_display = self._format_param_name(input_param)
                # Try to get display name
                if input_param in self.all_parameters:
                    input_value_obj = self.all_parameters[input_param].get("value")
                    if hasattr(input_value_obj, "display_name") and input_value_obj.display_name:
                        input_display = input_value_obj.display_name
                    # Add value
                    if input_value_obj is not None:
                        input_formatted = self._format_value(input_value_obj)
                        # If display name has colon (details), simplify to avoid double colons
                        if ':' in input_display:
                            input_display = input_display.split(':')[0].strip()
                        inputs_with_values.append(f"• {input_display}: {input_formatted}")
                    else:
                        inputs_with_values.append(f"• {input_display}")
                else:
                    inputs_with_values.append(f"• {input_display}")

            inputs_formatted = "\n".join(inputs_with_values)
            questions.append(SurveyQuestion(
                question_id=f"{param_name}_inputs_appropriate",
                question_text=f"Are these input factors appropriate?\n\n**Inputs:**\n{inputs_formatted}",
                question_type=QuestionType.CHECKLIST,
                options=[
                    "All inputs are appropriate",
                    "Missing critical factors",
                    "Includes inappropriate factors",
                    "Potential overlap between factors",
                    "Other issue (specify in comments)"
                ],
                context={
                    "inputs": inputs,
                    "inputs_readable": inputs_readable,
                    "formula": formula,
                    "formula_readable": formula_readable
                },
                required=True
            ))

        # Q3: Missing factors (open-ended)
        questions.append(SurveyQuestion(
            question_id=f"{param_name}_missing_factors",
            question_text="What important factors are missing from this calculation?",
            question_type=QuestionType.TEXT,
            context={"placeholder": "List missing factors or leave blank if none"},
            required=False,
            conditional_on=f"{param_name}_inputs_appropriate contains 'Missing critical factors'"
        ))

        return questions

    def _questions_definition(self, param_name: str, param_data: Dict) -> List[SurveyQuestion]:
        """Generate questions for DEFINITION parameters (core assumptions)"""
        questions = []
        value = param_data["value"]

        # Get metadata
        description = getattr(value, "description", "")
        display_name = getattr(value, "display_name", "") or self._format_param_name(param_name)
        formatted_value = self._format_value(value)

        # Q1: Assumption reasonableness
        questions.append(SurveyQuestion(
            question_id=f"{param_name}_assumption_reasonable",
            question_text=f"Is this assumption reasonable: {display_name} = {formatted_value}",
            question_type=QuestionType.RATING,
            options=[
                "1 (Unreasonable)",
                "2 (Questionable)",
                "3 (Acceptable)",
                "4 (Reasonable)",
                "5 (Very reasonable)",
                "Not qualified to assess"
            ],
            context={
                "value": float(value),
                "formatted_value": formatted_value,
                "description": description
            },
            required=True
        ))

        # Q2: Alternative value (conditional)
        questions.append(SurveyQuestion(
            question_id=f"{param_name}_alternative_value",
            question_text=f"What value would you use instead? (Current: {formatted_value})",
            question_type=QuestionType.TEXT,
            context={
                "current_value": float(value),
                "unit": getattr(value, "unit", ""),
                "placeholder": "Enter alternative value or leave blank"
            },
            required=False,
            conditional_on=f"{param_name}_assumption_reasonable <= 2"
        ))

        return questions

    def _questions_uncertainty(self, param_name: str, param_data: Dict) -> List[SurveyQuestion]:
        """Generate uncertainty range questions (if confidence_interval exists)"""
        questions = []
        value = param_data["value"]

        # Check if confidence interval exists
        confidence_interval = getattr(value, "confidence_interval", None)

        if confidence_interval:
            lower, upper = confidence_interval
            lower_formatted = self._format_value(lower, getattr(value, "unit", ""))
            upper_formatted = self._format_value(upper, getattr(value, "unit", ""))
            central_formatted = self._format_value(value)
            unit_suffix = self._get_unit_suffix(param_name, value)

            questions.append(SurveyQuestion(
                question_id=f"{param_name}_confidence_interval",
                question_text=f"The model uses a 90% confidence interval of [{lower_formatted}, {upper_formatted}]{unit_suffix}. What is your 90% CI?",
                question_type=QuestionType.NUMERIC_RANGE,
                options=["Lower bound", "Upper bound"],
                context={
                    "current_lower": lower,
                    "current_upper": upper,
                    "current_central": float(value),
                    "unit": getattr(value, "unit", "")
                },
                required=False
            ))

        return questions

    def _questions_impact(self, param_name: str, param_data: Dict) -> List[SurveyQuestion]:
        """Generate impact/importance questions (from sensitivity analysis)"""
        questions = []

        # Get sensitivity data for this parameter
        if param_name not in self.sensitivity_data:
            return questions

        param_sensitivity = self.sensitivity_data[param_name]
        top_outcomes = param_sensitivity.get("top_outcomes", [])

        if not top_outcomes:
            return questions

        # Show which outcomes this parameter most affects
        outcome_list = []
        for outcome in top_outcomes[:3]:  # Top 3
            outcome_name = outcome.get("outcome", "")
            rank = outcome.get("rank", "")
            impact_pct = outcome.get("impact_pct", 0)
            outcome_list.append(f"{outcome_name} (Rank #{rank}, {impact_pct:.1f}% of variance)")

        outcome_text = "\n".join(outcome_list)

        questions.append(SurveyQuestion(
            question_id=f"{param_name}_impact_awareness",
            question_text=f"This parameter most strongly affects:\n{outcome_text}\n\nDoes this ranking surprise you?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            options=[
                "Expected - this makes sense",
                "Surprising - I expected higher impact",
                "Surprising - I expected lower impact",
                "Surprising - wrong outcomes affected",
                "Unsure"
            ],
            context={
                "top_outcomes": top_outcomes,
                "parameter_name": param_name
            },
            required=False
        ))

        return questions

    def _format_value(self, value: Any, unit: str = None) -> str:
        """Format parameter value for display using official formatter"""
        # Use the official formatter which handles all cases correctly
        return format_parameter_value(value, unit=unit, include_unit=True)

    def _format_param_name(self, param_name: str) -> str:
        """
        Convert PARAMETER_NAME to "Parameter Name" for display.

        Example: TRIAL_CAPACITY_MULTIPLIER -> "Trial Capacity Multiplier"
        """
        # Replace underscores with spaces and convert to title case
        words = param_name.lower().split('_')
        return ' '.join(word.capitalize() for word in words)

    def _get_unit_suffix(self, param_name: str, value: Any) -> str:
        """
        Get appropriate unit suffix for display based on parameter type.

        Returns:
            Unit suffix like "x", " per DALY", "%" etc.
        """
        # Check unit property first
        unit = getattr(value, "unit", "")

        # If unit is percentage, already formatted by _format_value
        if unit == "percentage":
            return ""

        # Check parameter name patterns
        param_lower = param_name.lower()

        # Multipliers and ratios
        if any(word in param_lower for word in ["multiplier", "ratio", "vs_", "_vs_"]):
            return "x"

        # ROI parameters
        if "roi" in param_lower:
            return "x ROI"

        # Cost per DALY
        if "cost_per_daly" in param_lower or "per_daly" in param_lower:
            return " per DALY"

        # Years
        if unit == "years" or "years" in param_lower:
            return " years"

        # Deaths
        if unit == "deaths" or "deaths" in param_lower:
            return " deaths"

        # DALYs
        if unit == "DALYs" or "dalys" in param_lower:
            return " DALYs"

        # Currency is handled by _format_value
        if unit == "USD" or unit == "usd":
            return ""

        return ""

    def _format_formula_readable(self, formula: str) -> str:
        """
        Convert formula from PARAM_NAMES to readable display names.

        Example: "BED_NETS_COST ÷ TREATY_COST" -> "Bed Nets Cost ÷ Treaty Cost"
        """
        if not formula:
            return ""

        import re

        # Find all CAPITAL_CASE parameter names in formula
        param_pattern = r'\b[A-Z][A-Z0-9_]+\b'

        def replace_param(match):
            param_name = match.group(0)
            # Try to get display_name from all_parameters
            if param_name in self.all_parameters:
                param_value = self.all_parameters[param_name].get("value")
                if hasattr(param_value, "display_name") and param_value.display_name:
                    return param_value.display_name
            # Fallback to formatted name
            return self._format_param_name(param_name)

        return re.sub(param_pattern, replace_param, formula)

    def _format_inputs_readable(self, inputs: List[str]) -> str:
        """
        Convert input parameter list to readable display names.

        Example: ["BED_NETS_COST", "TREATY_COST"] -> "Bed Nets Cost, Treaty Cost"
        """
        readable_inputs = []
        for param_name in inputs:
            # Try to get display_name from all_parameters
            if param_name in self.all_parameters:
                param_value = self.all_parameters[param_name].get("value")
                if hasattr(param_value, "display_name") and param_value.display_name:
                    readable_inputs.append(param_value.display_name)
                    continue
            # Fallback to formatted name
            readable_inputs.append(self._format_param_name(param_name))

        return ", ".join(readable_inputs)

    def _format_calculation_example(self, formula: str, result_value: float, inputs: List[str] = None) -> str:
        """
        Generate calculation example with actual values.
        Replaces ALL parameter names in formula with their formatted values.

        Example: "$89 ÷ $27.4 = 3.25x" or "$300M + $650M + $50M = $1.00B"
        """
        if not formula:
            return ""

        import re
        example = formula

        # Build mapping of abbreviated names to full parameter names from inputs list
        # e.g., "REFERENDUM" -> "TREATY_CAMPAIGN_BUDGET_REFERENDUM"
        abbrev_to_full = {}
        if inputs:
            for full_name in inputs:
                # Try to find matching pattern in formula - last segment of full name often matches
                parts = full_name.split('_')
                # Try last word, last 2 words, etc.
                for i in range(1, min(len(parts) + 1, 4)):
                    abbrev = '_'.join(parts[-i:])
                    if abbrev in formula and abbrev not in abbrev_to_full:
                        abbrev_to_full[abbrev] = full_name

        # Find ALL capital-case parameter names in formula and replace with values
        param_pattern = r'\b[A-Z][A-Z0-9_]+\b'

        def replace_with_value(match):
            param_name = match.group(0)
            # Try direct lookup first
            if param_name in self.all_parameters:
                param_value = self.all_parameters[param_name].get("value")
                if param_value is not None:
                    return self._format_value(param_value)
            # Try abbreviated name mapping
            if param_name in abbrev_to_full:
                full_name = abbrev_to_full[param_name]
                if full_name in self.all_parameters:
                    param_value = self.all_parameters[full_name].get("value")
                    if param_value is not None:
                        return self._format_value(param_value)
            return param_name  # Keep original if not found

        example = re.sub(param_pattern, replace_with_value, example)

        # Add result with proper unit
        result_formatted = self._format_value(result_value, getattr(result_value, "unit", ""))
        return f"{example} = {result_formatted}"


def _calculate_parameter_impact(
    param_name: str,
    parameters: Dict[str, Dict[str, Any]]
) -> List[str]:
    """
    Calculate which outcome parameters this input affects.

    Uses dependency graph analysis to find all calculated parameters that
    depend on this parameter as a fundamental input.

    Args:
        param_name: Parameter to analyze
        parameters: All parameters dict

    Returns:
        List of outcome parameter names that are affected by this parameter
    """
    try:
        from dih_models.uncertainty import get_fundamental_inputs
    except ImportError:
        return []

    # Find which outcome parameters use this param as a fundamental input
    affected_outcomes = []

    for outcome_name, outcome_data in parameters.items():
        outcome_val = outcome_data.get("value")

        # Check if it's a calculated parameter (potential outcome)
        if not (hasattr(outcome_val, "compute") and hasattr(outcome_val, "inputs")):
            continue

        # Check if this param is a fundamental input to the outcome
        fundamental_inputs = get_fundamental_inputs(parameters, outcome_name)

        if param_name in fundamental_inputs:
            affected_outcomes.append(outcome_name)

    # Limit to top 5 most important outcomes
    return affected_outcomes[:5]


def generate_survey(
    parameters: Dict[str, Dict[str, Any]],
    sensitivity_data: Dict[str, Any] = None,
    usage_data: Dict[str, Any] = None,
    top_n: int = 50,
    calculate_sensitivity: bool = True
) -> Dict[str, Any]:
    """
    Generate complete economist validation survey from parameters.

    Args:
        parameters: Parameter definitions from parameters.py
        sensitivity_data: Optional pre-computed sensitivity data (legacy)
        usage_data: From document usage analysis
        top_n: Number of parameters to include (by importance)
        calculate_sensitivity: If True, calculate sensitivity on-demand (default)

    Returns:
        Survey structure with all questions, organized by module
    """
    generator = QuestionGenerator(sensitivity_data, usage_data, parameters)

    # Load reference metadata from references.qmd
    references_path = Path("knowledge/references.qmd")
    citation_data = {}
    if references_path.exists():
        citation_data = parse_references_qmd_detailed(references_path)

    # Rank parameters by importance with dependency-aware ordering
    # (inputs come before outputs that use them)
    ranked_params = rank_parameters_with_dependencies(parameters, sensitivity_data, usage_data)

    # Select top N for survey
    selected_params = ranked_params[:top_n]

    # Generate questions for each parameter
    survey = {
        "metadata": {
            "title": "Economic Model Validation Survey for Economists",
            "version": "1.0",
            "parameter_count": len(selected_params),
            "estimated_time_minutes": len(selected_params) * 3,  # ~3 min per parameter
            "conducted_by": "Decentralized Institutes of Health Initiative",
            "contact": "feedback@warondisease.org",
            "data_usage": "Responses will be used to refine economic model parameters. Individual responses are confidential.",
            "version_date": "2025-12-12"
        },
        "introduction": {
            "overview": "This survey validates the economic model for a proposed 1% Global Health Security Treaty that would redirect 1% of global military spending ($113.5B/year) to medical research and clinical trial infrastructure.",
            "main_claims": [
                "416 million lives saved over 50 years through accelerated drug development",
                "Cost-effectiveness: $27 per DALY averted (3.3x better than bed nets at $89/DALY)",
                "ROI: 450x return on R&D savings alone (10-year NPV, most conservative estimate)",
                "Political feasibility: 1-10% success probability over 20 years"
            ],
            "your_role": "As an economist, you're being asked to validate the parameters, calculations, and assumptions underlying these claims. Your feedback will be used to refine the model and strengthen the economic case for the treaty.",
            "survey_structure": [
                "Parameters are ordered by importance (sensitivity analysis + document usage frequency)",
                "Within that ordering, inputs are validated before outputs that depend on them",
                "Each parameter has 2-4 questions depending on its type (external/calculated/definition)",
                "You can stop at any time - priority is given to high-impact parameters first",
                "Some follow-up questions appear based on your responses (e.g., if you rate a source as low credibility, you'll be asked for alternatives)"
            ],
            "time_horizons": {
                "lives_saved": "50-year cumulative impact (standard for disease eradication models)",
                "roi_calculation": "10-year NPV with 3% discount rate",
                "political_timeline": "20-year probability window (campaign through treaty ratification)",
                "note": "Different parameters use different time horizons appropriate to their context. This will be specified in each parameter's description."
            },
            "question_types": {
                "rating": "1-5 scale questions (e.g., credibility rating). Includes 'Not qualified to assess' option.",
                "boolean": "Yes/No questions",
                "choice": "Multiple choice (select one)",
                "checklist": "Multiple select (check all that apply)",
                "range": "Enter lower and upper bounds (e.g., confidence intervals)",
                "text": "Open-ended text response"
            },
            "estimated_time": f"{len(selected_params)} parameters × ~3 min each = ~{len(selected_params) * 3} minutes total",
            "note": "Your responses are confidential. We're seeking honest feedback to improve the model, not validation for pre-determined conclusions."
        },
        "background_questions": [
            {
                "id": "expertise",
                "text": "Primary area(s) of expertise (check all that apply)",
                "type": "checklist",
                "options": [
                    "Health economics",
                    "Development economics",
                    "Cost-effectiveness analysis",
                    "Public finance",
                    "Political economy",
                    "Pharmaceutical economics",
                    "Epidemiological modeling",
                    "Other"
                ],
                "required": True
            },
            {
                "id": "experience_years",
                "text": "Years of professional experience in economics",
                "type": "choice",
                "options": ["0-5", "6-10", "11-20", "20+"],
                "required": True
            },
            {
                "id": "familiar_daly",
                "text": "Familiarity with DALY (Disability-Adjusted Life Years) methodology",
                "type": "rating",
                "options": ["1 (Not familiar)", "2", "3", "4", "5 (Very familiar)", "Not qualified to assess"],
                "required": True
            },
            {
                "id": "familiar_npv",
                "text": "Familiarity with NPV (Net Present Value) and ROI calculations",
                "type": "rating",
                "options": ["1 (Not familiar)", "2", "3", "4", "5 (Very familiar)", "Not qualified to assess"],
                "required": True
            }
        ],
        "parameters": []
    }

    for rank, (param_name, score, breakdown) in enumerate(selected_params, start=1):
        param_data = parameters[param_name]
        value = param_data.get("value")

        # Get display name and description
        display_name = getattr(value, "display_name", "") or generator._format_param_name(param_name)
        description = getattr(value, "description", "")

        # Get impact data - calculate on-demand if requested
        affected_outcomes = []
        if calculate_sensitivity:
            try:
                affected_outcomes = _calculate_parameter_impact(param_name, parameters)
            except Exception:
                pass  # Silently fall back to empty list
        elif sensitivity_data and param_name in sensitivity_data:
            # Legacy: use pre-computed sensitivity data
            param_sens = sensitivity_data[param_name]
            top_outcomes = param_sens.get("top_outcomes", [])[:3]
            affected_outcomes = [out.get("outcome", "") for out in top_outcomes if "outcome" in out]

        # Generate context card
        source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)

        context_card = {
            "what": description,
            "parameter_type": source_type_str,
            "used_in": [],  # Could be enhanced with document analysis
        }

        # Add dependencies: what this parameter depends on (inputs) and what depends on it (affects)
        if hasattr(value, "inputs") and value.inputs:
            context_card["inputs"] = value.inputs[:5]  # Limit to top 5 for readability

        # Only include affects if we have data
        if affected_outcomes:
            context_card["affects"] = affected_outcomes if isinstance(affected_outcomes, list) else [affected_outcomes]

        # Resolve citations for ANY parameter with source_ref (external, definition, or calculated)
        source_ref = getattr(value, "source_ref", "")
        citation = None
        if source_ref:
            # Extract reference ID from enum or string
            ref_id = source_ref.value if hasattr(source_ref, 'value') else str(source_ref)

            # Look up citation data
            if ref_id in citation_data:
                citation = citation_data[ref_id]

        # Add citation information to context card if found
        if citation:
            context_card["citation"] = {
                "id": citation.get("id", ""),
                "title": citation.get("title", ""),
                "author": citation.get("author", ""),
                "year": citation.get("year", ""),
                "source": citation.get("source", ""),
                "url": citation.get("url", ""),
                "type": citation.get("type", "misc")
            }
            context_card["peer_reviewed"] = getattr(value, "peer_reviewed", False)
            context_card["confidence"] = getattr(value, "confidence", "medium")
        elif source_ref:
            # Fallback to raw source_ref if citation not found
            context_card["data_source"] = str(source_ref)

        # Add type-specific context
        if source_type_str == "calculated":
            context_card["formula_readable"] = generator._format_formula_readable(getattr(value, "formula", ""))
            context_card["inputs_count"] = len(getattr(value, "inputs", []))

        questions = generator.generate_questions_for_parameter(param_name, param_data)

        survey["parameters"].append({
            "rank": rank,
            "parameter_name": param_name,
            "display_name": display_name,
            "description": description,
            "importance_score": round(score, 1),
            "importance_breakdown": {k: round(v, 1) for k, v in breakdown.items()},
            "progress": {
                "current": rank,
                "total": total_params,
                "percent_complete": percent_complete,
                "progress_bar": progress_text,
                "estimated_time_remaining_minutes": estimated_time_remaining,
                "note": "Estimated time for remaining parameters (3 minutes per parameter)"
            },
            "impact": {
                "top_outcomes": affected_outcomes if affected_outcomes else [],
                "top_percent": round(100 * rank / len(parameters), 1)
            },
            "context_card": context_card,
            "questions": [
                {
                    "question_id": q.question_id,
                    "question_text": q.question_text,
                    "question_type": q.question_type.value,
                    "options": q.options,
                    "context": q.context,
                    "required": q.required,
                    "conditional_on": q.conditional_on
                }
                for q in questions
            ]
        })

    return survey


def rank_parameters(
    parameters: Dict[str, Dict[str, Any]],
    sensitivity_data: Dict[str, Any] = None,
    usage_data: Dict[str, Any] = None
) -> List[Tuple[str, float, Dict]]:
    """
    Rank parameters by composite importance score.

    Returns: List of (param_name, total_score, breakdown) tuples, sorted by score
    """
    scores = []

    for param_name, param_data in parameters.items():
        value = param_data.get("value")

        # Skip non-Parameter values
        if not hasattr(value, "source_type"):
            continue

        # Skip calculated parameters not used in economics.qmd
        source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
        if source_type_str == "calculated":
            if usage_data and param_name not in usage_data:
                # Calculated parameter not in economics.qmd - skip it
                continue

        breakdown = {
            "sensitivity": 0,  # 0-40 points
            "usage": 0,        # 0-30 points
            "type": 0,         # 0-20 points
            "manual": 0        # 0-10 points
        }

        # 1. Sensitivity score (0-40 points)
        if sensitivity_data and param_name in sensitivity_data:
            param_sens = sensitivity_data[param_name]
            # Assuming sensitivity has "total_variance_explained" or similar
            variance_pct = param_sens.get("total_variance_pct", 0)
            breakdown["sensitivity"] = min(40, variance_pct * 4)  # Scale to 0-40

        # 2. Usage score (0-30 points)
        if usage_data and param_name in usage_data:
            param_usage = usage_data[param_name]
            frequency = param_usage.get("frequency", 0)
            position_weight = param_usage.get("position_weight", 0)  # Earlier = higher
            narrative_weight = param_usage.get("narrative_weight", 0)

            # Combine usage metrics
            usage_score = (frequency * 0.4 + position_weight * 0.3 + narrative_weight * 0.3)
            breakdown["usage"] = min(30, usage_score)

        # 3. Type score (0-20 points)
        source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
        if source_type_str == "calculated":
            breakdown["type"] = 20  # Highest priority
        elif source_type_str == "external":
            breakdown["type"] = 15
        elif source_type_str == "definition":
            breakdown["type"] = 10

        # 4. Manual priority (0-10 points) - could be added later
        # For now, use confidence level as proxy
        confidence = getattr(value, "confidence", "medium")
        if confidence == "low" or confidence == "estimated":
            breakdown["manual"] = 10  # Need more scrutiny
        elif confidence == "medium":
            breakdown["manual"] = 5
        else:
            breakdown["manual"] = 2

        total_score = sum(breakdown.values())
        scores.append((param_name, total_score, breakdown))

    # Sort by total score descending
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def rank_parameters_with_dependencies(
    parameters: Dict[str, Dict[str, Any]],
    sensitivity_data: Dict[str, Any] = None,
    usage_data: Dict[str, Any] = None
) -> List[Tuple[str, float, Dict]]:
    """
    Rank parameters by importance, but respect dependency order.

    Inputs must come before outputs that use them.
    Uses topological sort with importance-based tie-breaking.

    Returns: List of (param_name, total_score, breakdown) tuples in dependency-aware order
    """
    # Step 1: Get importance scores
    ranked = rank_parameters(parameters, sensitivity_data, usage_data)
    score_map = {name: (score, breakdown) for name, score, breakdown in ranked}

    # Step 2: Build dependency graph (who depends on whom)
    dependencies = {}  # param -> list of params it depends on (inputs)
    for param_name, param_data in parameters.items():
        if param_name not in score_map:
            continue  # Skip non-Parameters

        value = param_data.get("value")
        if hasattr(value, "inputs") and value.inputs:
            # Filter to only include inputs that are in the survey
            deps = [inp for inp in value.inputs if inp in score_map]
            dependencies[param_name] = deps
        else:
            dependencies[param_name] = []

    # Step 3: Topological sort with importance tie-breaking
    sorted_params = []
    visited = set()
    temp_mark = set()  # For cycle detection

    def visit(param):
        if param in temp_mark:
            # Cycle detected - break it by importance
            return
        if param in visited:
            return

        temp_mark.add(param)

        # Visit dependencies first (inputs before outputs)
        if param in dependencies:
            for dep in dependencies[param]:
                visit(dep)

        temp_mark.remove(param)
        visited.add(param)
        sorted_params.append(param)

    # Visit all parameters, sorted by importance (highest first)
    # But dependencies will be visited before dependents
    for param_name, _, _ in ranked:
        if param_name in dependencies:
            visit(param_name)

    # Return in dependency order with original scores
    return [(p, score_map[p][0], score_map[p][1]) for p in sorted_params]


if __name__ == "__main__":
    # Example usage
    from pathlib import Path
    import json

    # Load parameters
    from dih_models.parameters import PARAMETERS

    # Load sensitivity data (if available)
    sensitivity_path = Path("_analysis/sensitivity.json")
    sensitivity_data = {}
    if sensitivity_path.exists():
        with open(sensitivity_path) as f:
            sensitivity_data = json.load(f)

    # Generate survey
    survey = generate_survey(PARAMETERS, sensitivity_data, top_n=20)

    # Write to file
    output_path = Path("_analysis/economist-survey.json")
    output_path.parent.mkdir(exist_ok=True, parents=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(survey, f, indent=2, ensure_ascii=False)

    print(f"[OK] Generated survey with {len(survey['parameters'])} parameters")
    print(f"     Estimated time: {survey['metadata']['estimated_time_minutes']} minutes")
    print(f"     Output: {output_path}")
