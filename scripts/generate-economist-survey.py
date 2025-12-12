#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Economist Validation Survey - Complete Pipeline
========================================================

Fully programmatic survey generation from parameter metadata.

Steps:
1. Load parameters from parameters.py
2. Load sensitivity analysis from _analysis/sensitivity.json (if exists)
3. Analyze document usage from economics.qmd
4. Rank parameters by composite importance
5. Generate survey questions for top N parameters
6. Export to JSON (ready for Google Forms, Qualtrics, or web app)

Usage:
    python scripts/generate-economist-survey.py --top-n 50 --output _analysis/economist-survey.json
"""

import sys
import json
import inspect
import argparse
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dih_models import parameters as params_module
from dih_models.survey_generator import generate_survey, rank_parameters
from dih_models.usage_analyzer import analyze_document_usage


def load_parameters():
    """Load all Parameter objects from parameters.py"""
    param_objects = {
        name: obj
        for name, obj in inspect.getmembers(params_module)
        if isinstance(obj, params_module.Parameter)
    }

    # Convert to dict format expected by generator
    return {name: {'value': obj} for name, obj in param_objects.items()}


def load_sensitivity_data(path: Path):
    """Load sensitivity analysis results"""
    if not path.exists():
        print(f"[WARN] Sensitivity analysis not found: {path}")
        print(f"       Run Monte Carlo simulation to generate this file")
        return {}

    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Generate economist validation survey")
    parser.add_argument('--top-n', type=int, default=50,
                       help='Number of top parameters to include (default: 50)')
    parser.add_argument('--output', type=str, default='_analysis/economist-survey.json',
                       help='Output JSON file path')
    parser.add_argument('--usage-only', action='store_true',
                       help='Only run usage analysis and exit')
    args = parser.parse_args()

    print("=" * 80)
    print("ECONOMIST VALIDATION SURVEY GENERATOR")
    print("=" * 80)

    # Step 1: Load parameters
    print("\n[1/5] Loading parameters from parameters.py...")
    parameters = load_parameters()
    print(f"      Found {len(parameters)} parameters")

    # Step 2: Analyze document usage
    print("\n[2/5] Analyzing parameter usage in economics.qmd...")
    qmd_path = Path("knowledge/economics/economics.qmd")
    usage_data = analyze_document_usage(qmd_path)
    print(f"      Found {len(usage_data)} parameters used in document")

    # Save usage data
    usage_output = Path("_analysis/document-usage.json")
    usage_output.parent.mkdir(exist_ok=True, parents=True)
    with open(usage_output, "w", encoding="utf-8") as f:
        json.dump(usage_data, f, indent=2, ensure_ascii=False)
    print(f"      Saved usage data to {usage_output}")

    if args.usage_only:
        print("\n[OK] Usage analysis complete (--usage-only flag set)")
        return

    # Step 3: Load sensitivity analysis
    print("\n[3/5] Loading sensitivity analysis...")
    sensitivity_path = Path("_analysis/sensitivity.json")
    sensitivity_data = load_sensitivity_data(sensitivity_path)
    if sensitivity_data:
        print(f"      Loaded sensitivity data for {len(sensitivity_data)} parameters")
    else:
        print(f"      No sensitivity data available - using usage and type only")

    # Step 4: Rank parameters by importance
    print(f"\n[4/5] Ranking parameters by composite importance...")
    ranked = rank_parameters(parameters, sensitivity_data, usage_data)

    # Show top 10
    print(f"\n      Top 10 Parameters by Importance:")
    print(f"      {'Rank':<6} {'Parameter':<45} {'Score':<8} {'Sensitivity':<12} {'Usage':<8} {'Type':<6}")
    print(f"      {'-' * 95}")
    for rank, (param_name, score, breakdown) in enumerate(ranked[:10], start=1):
        sens = breakdown['sensitivity']
        usage = breakdown['usage']
        type_score = breakdown['type']
        print(f"      {rank:<6} {param_name:<45} {score:>6.1f}   {sens:>10.1f}   {usage:>6.1f}   {type_score:>4.0f}")

    # Step 5: Generate survey
    print(f"\n[5/5] Generating survey for top {args.top_n} parameters...")
    survey = generate_survey(
        parameters=parameters,
        sensitivity_data=sensitivity_data,
        usage_data=usage_data,
        top_n=args.top_n
    )

    # Count total questions
    total_questions = sum(len(p['questions']) for p in survey['parameters'])
    print(f"      Generated {total_questions} questions across {len(survey['parameters'])} parameters")
    print(f"      Estimated completion time: {survey['metadata']['estimated_time_minutes']} minutes")

    # Save survey
    output_path = Path(args.output)
    output_path.parent.mkdir(exist_ok=True, parents=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(survey, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Survey saved to {output_path}")
    print(f"\nNext steps:")
    print(f"  1. Review survey structure: {output_path}")
    print(f"  2. Export to Google Forms or Qualtrics")
    print(f"  3. Share with economists for validation")
    print(f"  4. Analyze responses and update parameters.py")
    print()


if __name__ == "__main__":
    main()
