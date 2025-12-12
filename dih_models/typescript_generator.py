#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TypeScript generation utilities for dih_models
===============================================

Generate TypeScript files with parameters and calculations for Next.js apps.

Functions:
- generate_typescript_parameters() - Generate TypeScript file with all parameters

Usage:
    from dih_models.typescript_generator import generate_typescript_parameters
    from pathlib import Path

    # Generate TypeScript file
    output_path = Path("dih_models/parameters-calculations-citations.ts")
    generate_typescript_parameters(parameters, output_path, references_path=Path("knowledge/references.qmd"))
"""

from pathlib import Path
from typing import Any, Dict, Optional
import re
import shutil

from dih_models.reference_parser import parse_references_qmd_detailed


def _escape_typescript_string(s: str) -> str:
    """Escape special characters in TypeScript string literals."""
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')


def _format_typescript_value(value: Any) -> str:
    """Format a Python value as TypeScript literal."""
    if isinstance(value, str):
        return f'"{_escape_typescript_string(value)}"'
    elif isinstance(value, bool):
        return 'true' if value else 'false'
    elif isinstance(value, (int, float)):
        # Use underscore separators for large numbers in TypeScript
        if isinstance(value, int) and abs(value) >= 10000:
            # Format with underscores for readability
            s = str(value)
            if s.startswith('-'):
                sign = '-'
                s = s[1:]
            else:
                sign = ''
            # Insert underscores every 3 digits from the right
            parts = []
            while s:
                parts.insert(0, s[-3:])
                s = s[:-3]
            return sign + '_'.join(parts)
        return str(value)
    elif value is None:
        return 'undefined'
    else:
        return str(value)


def _convert_to_csl_json(ref_id: str, ref_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Convert reference data to CSL JSON format.

    CSL JSON is the standard format used by citation processors like citeproc-js.
    See: https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html

    Args:
        ref_id: Reference ID
        ref_data: Reference data from parse_references_qmd_detailed()

    Returns:
        CSL JSON object or None if data is incomplete
    """
    if not ref_data or not ref_data.get('title'):
        return None

    csl = {
        'id': ref_id,
        'title': ref_data['title']
    }

    # Map our type to CSL types
    type_mapping = {
        'article': 'article-journal',
        'report': 'report',
        'book': 'book',
        'legislation': 'legislation',
        'techreport': 'report',
        'misc': 'webpage'
    }
    csl['type'] = type_mapping.get(ref_data.get('type', 'misc'), 'webpage')

    # Parse author into CSL format
    if ref_data.get('author'):
        author_str = ref_data['author']
        # Simple parsing: assume "Last, First" or "Organization Name"
        if ',' in author_str:
            # "Last, First" format
            parts = author_str.split(',', 1)
            csl['author'] = [{
                'family': parts[0].strip(),
                'given': parts[1].strip() if len(parts) > 1 else ''
            }]
        else:
            # Organization or single name
            csl['author'] = [{'literal': author_str}]

    # Parse year into CSL date format
    if ref_data.get('year'):
        year_str = ref_data['year']
        # Try to parse year (handle "n.d." and year ranges like "2020-2024")
        if year_str != 'n.d.' and year_str:
            # Extract first year if it's a range
            year_match = re.match(r'(\d{4})', year_str)
            if year_match:
                year = int(year_match.group(1))
                csl['issued'] = {'date-parts': [[year]]}

    # Publisher/source
    if ref_data.get('source'):
        if csl['type'] == 'article-journal':
            csl['container-title'] = ref_data['source']  # Journal name
        else:
            csl['publisher'] = ref_data['source']

    # URL
    if ref_data.get('url'):
        csl['URL'] = ref_data['url']

    # Note (additional context)
    if ref_data.get('note'):
        csl['note'] = ref_data['note']

    return csl


def _format_csl_json_typescript(csl: Dict[str, Any]) -> list:
    """Format CSL JSON object as TypeScript literal."""
    lines = []
    lines.append("    {")

    # ID
    lines.append(f"      id: {_format_typescript_value(csl['id'])},")

    # Type
    lines.append(f"      type: {_format_typescript_value(csl['type'])},")

    # Title
    lines.append(f"      title: {_format_typescript_value(csl['title'])},")

    # Author
    if 'author' in csl:
        lines.append("      author: [")
        for author in csl['author']:
            lines.append("        {")
            if 'literal' in author:
                lines.append(f"          literal: {_format_typescript_value(author['literal'])}")
            else:
                lines.append(f"          family: {_format_typescript_value(author.get('family', ''))},")
                if author.get('given'):
                    lines.append(f"          given: {_format_typescript_value(author['given'])}")
            lines.append("        },")
        lines.append("      ],")

    # Issued date
    if 'issued' in csl:
        date_parts = csl['issued']['date-parts'][0]
        date_str = ', '.join(str(p) for p in date_parts)
        lines.append(f"      issued: {{ 'date-parts': [[{date_str}]] }},")

    # Container title (journal)
    if 'container-title' in csl:
        lines.append(f"      'container-title': {_format_typescript_value(csl['container-title'])},")

    # Publisher
    if 'publisher' in csl:
        lines.append(f"      publisher: {_format_typescript_value(csl['publisher'])},")

    # URL
    if 'URL' in csl:
        lines.append(f"      URL: {_format_typescript_value(csl['URL'])},")

    # Note
    if 'note' in csl:
        lines.append(f"      note: {_format_typescript_value(csl['note'])},")

    lines.append("    }")

    return lines


def generate_typescript_parameters(
    parameters: Dict[str, Dict[str, Any]],
    output_path: Path,
    include_metadata: bool = True,
    references_path: Optional[Path] = None
):
    """
    Generate TypeScript file with parameters for Next.js applications.

    Creates a .ts file with:
    - Type definitions for Parameter interface
    - CSL JSON citations for all external sources
    - All parameter values as typed constants
    - Metadata (source, confidence, uncertainty)
    - Grouped exports by source type
    - Easy-to-use parameters object

    Args:
        parameters: Dict of parameter metadata from parse_parameters_file()
        output_path: Path to write the .ts file
        include_metadata: Include full metadata (default: True)
        references_path: Path to references.qmd for citation data (optional)
    """
    # Parse citation data from references.qmd
    citation_data = {}
    if references_path and references_path.exists():
        citation_data = parse_references_qmd_detailed(references_path)
    content = []

    # Header
    content.append("// AUTO-GENERATED FILE - DO NOT EDIT")
    content.append("// Generated from dih_models/parameters.py")
    content.append("// Run: python scripts/generate-everything-parameters-variables-calculations-references.py")
    content.append("")
    content.append("/**")
    content.append(" * Economic model parameters and calculations")
    content.append(" * for the 1% treaty analysis")
    content.append(" */")
    content.append("")

    # Type definitions
    if include_metadata:
        content.append("export type SourceType = 'external' | 'calculated' | 'definition';")
        content.append("export type Confidence = 'high' | 'medium' | 'low' | 'estimated';")
        content.append("")
        content.append("/**")
        content.append(" * CSL JSON citation format")
        content.append(" * Standard format used by citation processors like citeproc-js")
        content.append(" * See: https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html")
        content.append(" */")
        content.append("export interface Citation {")
        content.append("  id: string;")
        content.append("  type: 'article-journal' | 'report' | 'book' | 'webpage' | 'legislation';")
        content.append("  title: string;")
        content.append("  author?: Array<{ family?: string; given?: string; literal?: string }>;")
        content.append("  issued?: { 'date-parts': [[number, number?, number?]] };")
        content.append("  publisher?: string;")
        content.append("  'container-title'?: string;  // Journal name")
        content.append("  URL?: string;")
        content.append("  note?: string;")
        content.append("}")
        content.append("")
        content.append("export interface Parameter {")
        content.append("  /** Numeric value */")
        content.append("  value: number;")
        content.append("  /** Unit of measurement (USD, deaths, DALYs, percentage, etc.) */")
        content.append("  unit?: string;")
        content.append("  /** Human-readable description */")
        content.append("  description?: string;")
        content.append("  /** Display name for UI */")
        content.append("  displayName?: string;")
        content.append("  /** Source type: external data, calculated, or definition */")
        content.append("  sourceType?: SourceType;")
        content.append("  /** Reference ID - look up full citation in citations object */")
        content.append("  sourceRef?: string;")
        content.append("  /** Confidence level */")
        content.append("  confidence?: Confidence;")
        content.append("  /** Formula string (for calculated parameters) */")
        content.append("  formula?: string;")
        content.append("  /** LaTeX equation (for display) */")
        content.append("  latex?: string;")
        content.append("  /** 95% confidence interval [low, high] */")
        content.append("  confidenceInterval?: [number, number];")
        content.append("  /** Standard error */")
        content.append("  stdError?: number;")
        content.append("  /** Whether this is peer-reviewed data */")
        content.append("  peerReviewed?: boolean;")
        content.append("  /** Whether this is a conservative estimate */")
        content.append("  conservative?: boolean;")
        content.append("}")
        content.append("")
    else:
        content.append("export interface Parameter {")
        content.append("  value: number;")
        content.append("  unit?: string;")
        content.append("  description?: string;")
        content.append("}")
        content.append("")

    # Categorize parameters
    external_params = []
    calculated_params = []
    definition_params = []

    for param_name in sorted(parameters.keys()):
        param_data = parameters[param_name]
        value_obj = param_data["value"]

        if hasattr(value_obj, "source_type"):
            source_type_str = str(value_obj.source_type.value) if hasattr(value_obj.source_type, 'value') else str(value_obj.source_type)
            if source_type_str == "external":
                external_params.append((param_name, param_data))
            elif source_type_str == "calculated":
                calculated_params.append((param_name, param_data))
            elif source_type_str == "definition":
                definition_params.append((param_name, param_data))
        else:
            definition_params.append((param_name, param_data))

    # Collect all citations for later export
    all_citations = {}

    # Generate external parameters
    if external_params:
        content.append("// ============================================================================")
        content.append("// External Data Sources")
        content.append("// ============================================================================")
        content.append("")

        for param_name, param_data in external_params:
            value_obj = param_data["value"]
            param_lines, citation = _generate_parameter_constant(param_name, value_obj, include_metadata, citation_data)
            content.extend(param_lines)
            if citation:
                all_citations[citation['id']] = citation
            content.append("")

    # Generate calculated parameters
    if calculated_params:
        content.append("// ============================================================================")
        content.append("// Calculated Values")
        content.append("// ============================================================================")
        content.append("")

        for param_name, param_data in calculated_params:
            value_obj = param_data["value"]
            param_lines, citation = _generate_parameter_constant(param_name, value_obj, include_metadata, citation_data)
            content.extend(param_lines)
            if citation:
                all_citations[citation['id']] = citation
            content.append("")

    # Generate definition parameters
    if definition_params:
        content.append("// ============================================================================")
        content.append("// Core Definitions")
        content.append("// ============================================================================")
        content.append("")

        for param_name, param_data in definition_params:
            value_obj = param_data["value"]
            param_lines, citation = _generate_parameter_constant(param_name, value_obj, include_metadata, citation_data)
            content.extend(param_lines)
            if citation:
                all_citations[citation['id']] = citation
            content.append("")

    # Generate parameters object for easy iteration
    content.append("// ============================================================================")
    content.append("// All Parameters (for iteration)")
    content.append("// ============================================================================")
    content.append("")
    content.append("export const parameters = {")

    all_params = external_params + calculated_params + definition_params
    for i, (param_name, _) in enumerate(all_params):
        comma = "," if i < len(all_params) - 1 else ""
        content.append(f"  {param_name}{comma}")

    content.append("} as const;")
    content.append("")

    # Generate helper type for parameter names
    content.append("/** Union type of all parameter names */")
    content.append("export type ParameterName = keyof typeof parameters;")
    content.append("")

    # Generate citations lookup object (CSL JSON format)
    if all_citations and include_metadata:
        content.append("// ============================================================================")
        content.append("// Citations Lookup (CSL JSON)")
        content.append("// ============================================================================")
        content.append("")
        content.append("/**")
        content.append(" * All citations in CSL JSON format")
        content.append(" * Use with citation processors like citeproc-js or citation-js")
        content.append(" * to format in any style (APA, MLA, Chicago, etc.)")
        content.append(" */")
        content.append("export const citations: Record<string, Citation> = {")

        for i, (cite_id, csl_json) in enumerate(sorted(all_citations.items())):
            comma = "," if i < len(all_citations) - 1 else ""
            content.append(f"  {_format_typescript_value(cite_id)}: {{")
            csl_lines = _format_csl_json_typescript(csl_json)
            # Remove outer braces and adjust indentation
            for line in csl_lines[1:-1]:  # Skip first and last lines (braces)
                content.append(f"  {line}")
            content.append(f"  }}{comma}")

        content.append("};")
        content.append("")

    # Generate summary statistics
    content.append("/** Summary statistics */")
    content.append("export const PARAMETER_STATS = {")
    content.append(f"  total: {len(all_params)},")
    content.append(f"  external: {len(external_params)},")
    content.append(f"  calculated: {len(calculated_params)},")
    content.append(f"  definitions: {len(definition_params)},")
    if all_citations:
        content.append(f"  citations: {len(all_citations)},")
    content.append("} as const;")
    content.append("")

    # Generate helper functions
    if include_metadata:
        content.append("// ============================================================================")
        content.append("// Helper Functions")
        content.append("// ============================================================================")
        content.append("")

        # getCitation helper
        content.append("/**")
        content.append(" * Get citation for a parameter by its sourceRef")
        content.append(" * ")
        content.append(" * Example:")
        content.append(" *   const citation = getCitation(ANTIDEPRESSANT_TRIAL_EXCLUSION_RATE);")
        content.append(" *   console.log(formatCitation(citation, 'apa'));")
        content.append(" */")
        content.append("export function getCitation(param: Parameter): Citation | undefined {")
        content.append("  if (!param.sourceRef) return undefined;")
        content.append("  return citations[param.sourceRef];")
        content.append("}")
        content.append("")

        # formatValue helper
        content.append("/**")
        content.append(" * Format parameter value with appropriate unit formatting")
        content.append(" */")
        content.append("export function formatValue(param: Parameter): string {")
        content.append("  const { value, unit } = param;")
        content.append("")
        content.append("  // Currency formatting")
        content.append("  if (unit === 'USD') {")
        content.append("    if (Math.abs(value) >= 1_000_000_000_000) {")
        content.append("      return `$${(value / 1_000_000_000_000).toFixed(2)}T`;")
        content.append("    } else if (Math.abs(value) >= 1_000_000_000) {")
        content.append("      return `$${(value / 1_000_000_000).toFixed(2)}B`;")
        content.append("    } else if (Math.abs(value) >= 1_000_000) {")
        content.append("      return `$${(value / 1_000_000).toFixed(2)}M`;")
        content.append("    } else if (Math.abs(value) >= 1_000) {")
        content.append("      return `$${(value / 1_000).toFixed(2)}K`;")
        content.append("    } else {")
        content.append("      return `$${value.toLocaleString()}`;")
        content.append("    }")
        content.append("  }")
        content.append("")
        content.append("  // Percentage formatting")
        content.append("  if (unit === 'percentage') {")
        content.append("    return `${(value * 100).toFixed(1)}%`;")
        content.append("  }")
        content.append("")
        content.append("  if (unit === 'rate') {")
        content.append("    return `${(value * 100).toFixed(1)}%`;")
        content.append("  }")
        content.append("")
        content.append("  // Large numbers (deaths, DALYs, etc.)")
        content.append("  if (Math.abs(value) >= 1_000_000_000) {")
        content.append("    return `${(value / 1_000_000_000).toFixed(2)}B${unit ? ' ' + unit : ''}`;")
        content.append("  } else if (Math.abs(value) >= 1_000_000) {")
        content.append("    return `${(value / 1_000_000).toFixed(2)}M${unit ? ' ' + unit : ''}`;")
        content.append("  } else if (Math.abs(value) >= 1_000) {")
        content.append("    return `${value.toLocaleString()}${unit ? ' ' + unit : ''}`;")
        content.append("  }")
        content.append("")
        content.append("  return `${value}${unit ? ' ' + unit : ''}`;")
        content.append("}")
        content.append("")

        # formatCitation helper
        content.append("/**")
        content.append(" * Format citation in APA or MLA style")
        content.append(" */")
        content.append("export function formatCitation(")
        content.append("  citation: Citation | undefined,")
        content.append("  style: 'apa' | 'mla' = 'apa'")
        content.append("): string {")
        content.append("  if (!citation) return '';")
        content.append("")
        content.append("  const author = citation.author?.[0]?.literal ||")
        content.append("                 (citation.author?.[0]?.family")
        content.append("                   ? `${citation.author[0].family}, ${citation.author[0].given || ''}`")
        content.append("                   : 'Unknown Author');")
        content.append("  const year = citation.issued?.['date-parts']?.[0]?.[0] || 'n.d.';")
        content.append("  const title = citation.title;")
        content.append("")
        content.append("  if (style === 'apa') {")
        content.append("    // APA: Author (Year). Title. URL")
        content.append("    let result = `${author} (${year}). ${title}.`;")
        content.append("    if (citation.URL) result += ` ${citation.URL}`;")
        content.append("    return result;")
        content.append("  } else {")
        content.append("    // MLA: Author. \"Title.\" Year. URL")
        content.append("    let result = `${author}. \"${title}.\" ${year}.`;")
        content.append("    if (citation.URL) result += ` ${citation.URL}`;")
        content.append("    return result;")
        content.append("  }")
        content.append("}")
        content.append("")

    # Write file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"[OK] Generated {output_path}")
    print(f"     {len(all_params)} parameters exported")
    print(f"     {len(external_params)} external sources")
    print(f"     {len(calculated_params)} calculated values")
    print(f"     {len(definition_params)} core definitions")
    if all_citations:
        print(f"     {len(all_citations)} citations (CSL JSON)")

    # Copy to Next.js project if it exists
    nextjs_lib = Path("E:/code/dih-neobrutalist/lib")
    if nextjs_lib.exists() and nextjs_lib.is_dir():
        dest_path = nextjs_lib / output_path.name
        shutil.copy2(output_path, dest_path)
        print(f"[OK] Copied to {dest_path}")

    print()
    print("Usage in Next.js/React:")
    if all_params:
        first_param = all_params[0][0]
        print(f"  import {{ {first_param}, parameters, citations }} from './parameters-calculations-citations';")
        print(f"  console.log({first_param}.value);")
        if all_citations:
            first_cite = sorted(all_citations.keys())[0]
            print(f"  console.log(citations[{_format_typescript_value(first_cite)}]);")
    print()


def generate_typescript_survey(
    survey_json_path: Path,
    output_path: Path
):
    """
    Generate TypeScript file with economist survey data for Next.js applications.

    Creates a .ts file with:
    - Type definitions for survey structure
    - Survey data as typed constants
    - Helper functions for survey navigation
    - All metadata from the JSON file

    Args:
        survey_json_path: Path to economist-survey.json
        output_path: Path to write the .ts file
    """
    import json

    # Load survey JSON
    if not survey_json_path.exists():
        print(f"[ERROR] Survey JSON not found: {survey_json_path}")
        print(f"        Run: python scripts/generate-economist-survey.py --top-n 30")
        return

    with open(survey_json_path, encoding='utf-8') as f:
        survey_data = json.load(f)

    content = []

    # Header
    content.append("// AUTO-GENERATED FILE - DO NOT EDIT")
    content.append("// Generated from _analysis/economist-survey.json")
    content.append("// Run: python scripts/generate-economist-survey.py --top-n 30")
    content.append("")
    content.append("/**")
    content.append(" * Economist validation survey data")
    content.append(" * Programmatically generated questions for parameter validation")
    content.append(" */")
    content.append("")

    # Type definitions
    content.append("export type QuestionType =")
    content.append("  | 'rating'")
    content.append("  | 'boolean'")
    content.append("  | 'text'")
    content.append("  | 'range'")
    content.append("  | 'choice'")
    content.append("  | 'checklist';")
    content.append("")
    content.append("export type SourceType = 'external' | 'calculated' | 'definition';")
    content.append("")
    content.append("export interface SurveyQuestion {")
    content.append("  id: string;")
    content.append("  type: QuestionType;")
    content.append("  question: string;")
    content.append("  options?: string[];")
    content.append("  allowMultiple?: boolean;")
    content.append("  allowOther?: boolean;")
    content.append("}")
    content.append("")
    content.append("export interface Citation {")
    content.append("  id: string;")
    content.append("  title: string;")
    content.append("  author?: string;")
    content.append("  year?: string;")
    content.append("  source?: string;")
    content.append("  url?: string;")
    content.append("}")
    content.append("")
    content.append("export interface SurveyParameter {")
    content.append("  rank: number;")
    content.append("  name: string;")
    content.append("  displayName: string;")
    content.append("  value: number;")
    content.append("  unit?: string;")
    content.append("  formattedValue: string;")
    content.append("  sourceType: SourceType;")
    content.append("  description?: string;")
    content.append("  formula?: string;")
    content.append("  latex?: string;")
    content.append("  sourceRef?: string;")
    content.append("  citation?: Citation;")
    content.append("  questions: SurveyQuestion[];")
    content.append("}")
    content.append("")
    content.append("export interface SurveyMetadata {")
    content.append("  title: string;")
    content.append("  version: string;")
    content.append("  versionDate: string;")
    content.append("  parameterCount: number;")
    content.append("  estimatedTimeMinutes: number;")
    content.append("  conductedBy: string;")
    content.append("  contact: string;")
    content.append("  dataUsage: string;")
    content.append("}")
    content.append("")
    content.append("export interface EconomistSurvey {")
    content.append("  metadata: SurveyMetadata;")
    content.append("  parameters: SurveyParameter[];")
    content.append("}")
    content.append("")

    # Convert survey data to TypeScript format
    content.append("// ============================================================================")
    content.append("// Survey Data")
    content.append("// ============================================================================")
    content.append("")
    # Calculate total questions
    total_questions = sum(len(p['questions']) for p in survey_data['parameters'])

    content.append("export const economistSurvey: EconomistSurvey = {")
    content.append("  metadata: {")
    content.append(f"    title: {_format_typescript_value(survey_data['metadata']['title'])},")
    content.append(f"    version: {_format_typescript_value(survey_data['metadata']['version'])},")
    content.append(f"    versionDate: {_format_typescript_value(survey_data['metadata']['version_date'])},")
    content.append(f"    parameterCount: {survey_data['metadata']['parameter_count']},")
    content.append(f"    estimatedTimeMinutes: {survey_data['metadata']['estimated_time_minutes']},")
    content.append(f"    conductedBy: {_format_typescript_value(survey_data['metadata']['conducted_by'])},")
    content.append(f"    contact: {_format_typescript_value(survey_data['metadata']['contact'])},")
    content.append(f"    dataUsage: {_format_typescript_value(survey_data['metadata']['data_usage'])},")
    content.append("  },")
    content.append("  parameters: [")

    # Generate each parameter
    for i, param in enumerate(survey_data['parameters']):
        comma = "," if i < len(survey_data['parameters']) - 1 else ""
        context = param.get('context_card', {})

        content.append("    {")
        content.append(f"      rank: {param['rank']},")
        content.append(f"      name: {_format_typescript_value(param['parameter_name'])},")
        content.append(f"      displayName: {_format_typescript_value(param['display_name'])},")

        # Extract value and other fields from context_card or impact
        impact = param.get('impact', {})
        value = impact.get('value', 0)
        unit = impact.get('unit', '')
        formatted_value = impact.get('formatted_value', str(value))

        content.append(f"      value: {_format_typescript_value(value)},")

        if unit:
            content.append(f"      unit: {_format_typescript_value(unit)},")

        content.append(f"      formattedValue: {_format_typescript_value(formatted_value)},")
        content.append(f"      sourceType: {_format_typescript_value(context.get('parameter_type', 'definition'))},")

        if param.get('description'):
            content.append(f"      description: {_format_typescript_value(param['description'])},")
        elif context.get('what'):
            content.append(f"      description: {_format_typescript_value(context['what'])},")

        if impact.get('formula'):
            content.append(f"      formula: {_format_typescript_value(impact['formula'])},")

        if impact.get('latex'):
            content.append(f"      latex: {_format_typescript_value(impact['latex'])},")

        if impact.get('source_ref'):
            content.append(f"      sourceRef: {_format_typescript_value(impact['source_ref'])},")

        # Citation
        citation = context.get('citation')
        if citation:
            content.append("      citation: {")
            content.append(f"        id: {_format_typescript_value(citation['id'])},")
            content.append(f"        title: {_format_typescript_value(citation['title'])},")
            if citation.get('author'):
                content.append(f"        author: {_format_typescript_value(citation['author'])},")
            if citation.get('year'):
                content.append(f"        year: {_format_typescript_value(citation['year'])},")
            if citation.get('source'):
                content.append(f"        source: {_format_typescript_value(citation['source'])},")
            if citation.get('url'):
                content.append(f"        url: {_format_typescript_value(citation['url'])},")
            content.append("      },")

        # Questions
        content.append("      questions: [")
        for j, question in enumerate(param['questions']):
            q_comma = "," if j < len(param['questions']) - 1 else ""
            content.append("        {")
            content.append(f"          id: {_format_typescript_value(question['question_id'])},")
            content.append(f"          type: {_format_typescript_value(question['question_type'])},")
            content.append(f"          question: {_format_typescript_value(question['question_text'])},")

            if question.get('options'):
                content.append("          options: [")
                for k, option in enumerate(question['options']):
                    opt_comma = "," if k < len(question['options']) - 1 else ""
                    content.append(f"            {_format_typescript_value(option)}{opt_comma}")
                content.append("          ],")

            # Note: The JSON doesn't have allow_multiple or allow_other, so we skip those

            content.append(f"        }}{q_comma}")
        content.append("      ],")

        content.append(f"    }}{comma}")

    content.append("  ],")
    content.append("};")
    content.append("")

    # Helper functions
    content.append("// ============================================================================")
    content.append("// Helper Functions")
    content.append("// ============================================================================")
    content.append("")

    content.append("/**")
    content.append(" * Get parameter by rank")
    content.append(" */")
    content.append("export function getParameterByRank(rank: number): SurveyParameter | undefined {")
    content.append("  return economistSurvey.parameters.find(p => p.rank === rank);")
    content.append("}")
    content.append("")

    content.append("/**")
    content.append(" * Get parameter by name")
    content.append(" */")
    content.append("export function getParameterByName(name: string): SurveyParameter | undefined {")
    content.append("  return economistSurvey.parameters.find(p => p.name === name);")
    content.append("}")
    content.append("")

    content.append("/**")
    content.append(" * Get all parameters of a specific source type")
    content.append(" */")
    content.append("export function getParametersByType(sourceType: SourceType): SurveyParameter[] {")
    content.append("  return economistSurvey.parameters.filter(p => p.sourceType === sourceType);")
    content.append("}")
    content.append("")

    content.append("/**")
    content.append(" * Get total number of questions")
    content.append(" */")
    content.append("export function getTotalQuestions(): number {")
    content.append("  return economistSurvey.parameters.reduce((sum, p) => sum + p.questions.length, 0);")
    content.append("}")
    content.append("")

    content.append("/**")
    content.append(" * Calculate completion percentage")
    content.append(" */")
    content.append("export function getCompletionPercentage(currentRank: number): number {")
    content.append("  const total = economistSurvey.metadata.parameterCount;")
    content.append("  return Math.round((currentRank / total) * 100);")
    content.append("}")
    content.append("")

    content.append("/**")
    content.append(" * Get questions for a specific parameter")
    content.append(" */")
    content.append("export function getQuestionsForParameter(paramName: string): SurveyQuestion[] {")
    content.append("  const param = getParameterByName(paramName);")
    content.append("  return param?.questions || [];")
    content.append("}")
    content.append("")

    content.append("/**")
    content.append(" * Check if parameter has citation")
    content.append(" */")
    content.append("export function hasCitation(param: SurveyParameter): boolean {")
    content.append("  return !!param.citation;")
    content.append("}")
    content.append("")

    # Write file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"[OK] Generated {output_path}")
    print(f"     {survey_data['metadata']['parameter_count']} parameters")
    print(f"     {total_questions} questions")
    print(f"     {survey_data['metadata']['estimated_time_minutes']} minutes estimated")

    # Copy to Next.js project if it exists
    nextjs_lib = Path("E:/code/dih-neobrutalist/lib")
    if nextjs_lib.exists() and nextjs_lib.is_dir():
        dest_path = nextjs_lib / output_path.name
        shutil.copy2(output_path, dest_path)
        print(f"[OK] Copied to {dest_path}")

    print()
    print("Usage in Next.js/React:")
    print("  import { economistSurvey, getParameterByRank } from './economist-survey';")
    print("  const param = getParameterByRank(1);")
    print("  console.log(param.displayName, param.formattedValue);")
    print()


def _generate_parameter_constant(
    param_name: str,
    value_obj: Any,
    include_metadata: bool,
    citation_data: Dict[str, Any] = None
) -> tuple[list, Optional[Dict[str, Any]]]:
    """
    Generate TypeScript constant declaration for a parameter.

    Returns:
        Tuple of (lines, citation) where citation is the CSL JSON object if found
    """
    lines = []
    citation = None

    # Extract description (kept for metadata, but JSDoc comment generation removed)
    description = getattr(value_obj, "description", None)

    # Start constant declaration
    lines.append(f"export const {param_name}: Parameter = {{")

    # Value
    value = float(value_obj) if hasattr(value_obj, '__float__') else value_obj
    lines.append(f"  value: {_format_typescript_value(value)},")

    # Unit
    unit = getattr(value_obj, "unit", None)
    if unit:
        lines.append(f"  unit: {_format_typescript_value(unit)},")

    if include_metadata:
        # Display name
        display_name = getattr(value_obj, "display_name", None)
        if display_name:
            lines.append(f"  displayName: {_format_typescript_value(display_name)},")

        # Description
        if description:
            lines.append(f"  description: {_format_typescript_value(description)},")

        # Source type
        if hasattr(value_obj, "source_type"):
            source_type = str(value_obj.source_type.value) if hasattr(value_obj.source_type, 'value') else str(value_obj.source_type)
            lines.append(f"  sourceType: {_format_typescript_value(source_type)},")

        # Source reference and citation
        source_ref = getattr(value_obj, "source_ref", None)
        if source_ref:
            # Convert enum to string if needed
            if hasattr(source_ref, 'value'):
                source_ref = source_ref.value
            else:
                source_ref = str(source_ref)

            # Convert internal QMD paths to published URLs
            if '/' in source_ref or '.qmd' in source_ref:
                # This is an internal path, convert to URL
                if not source_ref.startswith('http://') and not source_ref.startswith('https://'):
                    base = 'https://impact.dih.earth'
                    path = source_ref.replace('//', '/').lstrip('/')  # Normalize slashes
                    path = path.replace('.qmd#', '#').replace('.qmd', '')  # Remove .qmd
                    source_ref = f"{base}/{path}"

            lines.append(f"  sourceRef: {_format_typescript_value(source_ref)},")

            # Collect citation for the citations lookup (don't embed)
            # Only for citation IDs (no slashes, no .qmd in original)
            original_ref = getattr(value_obj, "source_ref", None)
            if hasattr(original_ref, 'value'):
                original_ref = original_ref.value
            else:
                original_ref = str(original_ref) if original_ref else None

            if citation_data and original_ref and '/' not in original_ref and '.qmd' not in original_ref:
                ref_data = citation_data.get(original_ref)
                if ref_data:
                    csl_json = _convert_to_csl_json(original_ref, ref_data)
                    if csl_json:
                        citation = csl_json

        # Confidence
        confidence = getattr(value_obj, "confidence", None)
        if confidence:
            lines.append(f"  confidence: {_format_typescript_value(confidence)},")

        # Formula
        formula = getattr(value_obj, "formula", None)
        if formula:
            lines.append(f"  formula: {_format_typescript_value(formula)},")

        # LaTeX
        latex = getattr(value_obj, "latex", None)
        if latex:
            lines.append(f"  latex: {_format_typescript_value(latex)},")

        # Confidence interval
        if hasattr(value_obj, "confidence_interval") and value_obj.confidence_interval:
            low, high = value_obj.confidence_interval
            low_val = float(low) if hasattr(low, '__float__') else low
            high_val = float(high) if hasattr(high, '__float__') else high
            lines.append(f"  confidenceInterval: [{_format_typescript_value(low_val)}, {_format_typescript_value(high_val)}],")

        # Standard error
        if hasattr(value_obj, "std_error") and value_obj.std_error:
            std_err = float(value_obj.std_error) if hasattr(value_obj.std_error, '__float__') else value_obj.std_error
            lines.append(f"  stdError: {_format_typescript_value(std_err)},")

        # Peer reviewed
        peer_reviewed = getattr(value_obj, "peer_reviewed", None)
        if peer_reviewed:
            lines.append(f"  peerReviewed: {_format_typescript_value(peer_reviewed)},")

        # Conservative
        conservative = getattr(value_obj, "conservative", None)
        if conservative:
            lines.append(f"  conservative: {_format_typescript_value(conservative)},")

    lines.append("};")

    return lines, citation
