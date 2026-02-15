---
name: curate-book
description: Systematic book curation pipeline. Evaluates every chapter on 8 dimensions, identifies overlaps, and produces a scored report with actionable recommendations.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Grep
  - Glob
  - Task
  - AskUserQuestion
---

# /curate-book [mode]

Systematic book curation pipeline. Evaluates every chapter on 8 dimensions, identifies cross-chapter overlaps, and produces a scored report.

Modes:
- (no args) - Full pipeline (Phases 1-4)
- `check` - Phase 1 only (fast automated metrics, no LLM)
- `chapter <name>` - Single chapter evaluation
- `report` - Regenerate report from cached data (Phase 4 only)

---

## Mode: check

Run Phase 1 automated metrics only (fast, no LLM):

```bash
.venv\Scripts\python.exe -u scripts/curation/collect-chapter-metrics.py
```

Then generate a metrics-only report:

```bash
.venv\Scripts\python.exe -u scripts/curation/generate-curation-report.py --metrics-only
```

Read and summarize `_analysis/curation-report.md`.

---

## Mode: report

Regenerate the report from existing cached data (Phase 4 only):

```bash
.venv\Scripts\python.exe -u scripts/curation/generate-curation-report.py
```

Read and summarize `_analysis/curation-report.md`.

---

## Mode: chapter <name>

Evaluate a single chapter:

### Step 1: Collect Metrics

```bash
.venv\Scripts\python.exe -u scripts/curation/collect-chapter-metrics.py --chapter <name>
```

### Step 2: Read and Evaluate

Read the chapter content and the metrics from `_analysis/curation-metrics.json`. Read `OUTLINE.md` for book context. Then score the chapter on all 8 dimensions using the rubric below and write the evaluation JSON to `_analysis/curation-evaluations/<slug>.json`.

### Step 3: Regenerate Report

```bash
.venv\Scripts\python.exe -u scripts/curation/generate-curation-report.py
```

---

## Mode: (default - full pipeline)

### Phase 1: Automated Metrics

```bash
.venv\Scripts\python.exe -u scripts/curation/collect-chapter-metrics.py
```

### Phase 2: Parallel Chapter Evaluation

Read `_analysis/curation-metrics.json` to get the chapter list. Read `OUTLINE.md` for book context.

Divide chapters into 3 batches. Launch up to 3 Task agents in parallel (subagent_type: "general-purpose"), each evaluating a batch.

Each agent instruction should include:
1. The list of chapter file paths to evaluate
2. The full scoring rubric (copied from below)
3. The book context from OUTLINE.md
4. The automated metrics for those chapters
5. Instruction to write per-chapter JSON to `_analysis/curation-evaluations/<slug>.json`

The agent should read each chapter, score it, and write the evaluation file.

### Phase 3: Cross-Chapter Synthesis

After all Phase 2 agents complete, launch a single Task agent (subagent_type: "general-purpose") that:

1. Reads all evaluation JSONs from `_analysis/curation-evaluations/`
2. Reads `_analysis/curation-metrics.json` for automated metrics
3. Produces cross-chapter analysis:
   - Pairwise overlap scores for chapters in same/adjacent parts
   - Narrative flow assessment (gaps, redundancies, strongest sequences)
   - Page budget analysis (pages vs necessity score ratio)
4. Writes output to `_analysis/curation-cross-chapter.json`

The JSON structure should be:
```json
{
  "overlaps": [
    {"chapter_a": "href", "chapter_b": "href", "similarity": 0.0-1.0, "recommendation": "text"}
  ],
  "narrative_flow": {
    "gaps": ["description"],
    "redundancies": ["description"],
    "strongest_sequences": ["description"]
  },
  "page_budget": {
    "total_pages": 780,
    "overweight_chapters": ["list"],
    "underweight_chapters": ["list"]
  }
}
```

### Phase 4: Generate Report

```bash
.venv\Scripts\python.exe -u scripts/curation/generate-curation-report.py
```

Read and summarize `_analysis/curation-report.md` to the user.

---

## Scoring Rubric (8 Dimensions, 1-5 Scale)

### D1: Mission Necessity (weight: 0.20)
Does this chapter directly advance the book's goal of getting nations to sign a 1% treaty redirecting military spending to clinical trials?

| Score | Criteria |
|-------|----------|
| 5 | Core to the thesis; book is incomplete without it |
| 4 | Strongly supports the thesis; important but not essential |
| 3 | Tangentially supports; useful context but could be summarized |
| 2 | Weak connection; mostly interesting but not mission-critical |
| 1 | No clear connection to the 1% treaty goal |

### D2: Uniqueness (weight: 0.15)
How much does this chapter overlap with other chapters in content or argument?

| Score | Criteria |
|-------|----------|
| 5 | Completely unique content and argument |
| 4 | Minor overlap (<10%) with other chapters |
| 3 | Moderate overlap (10-25%); some repeated arguments |
| 2 | Significant overlap (25-50%); major sections duplicate other chapters |
| 1 | Mostly redundant; could be merged into another chapter |

### D3: Placement (weight: 0.05)
Is this chapter in the right location within the book's narrative flow?

| Score | Criteria |
|-------|----------|
| 5 | Perfect placement; builds on prior chapters and sets up next ones |
| 4 | Good placement; minor reordering might help |
| 3 | Acceptable but not optimal; reader might be confused by position |
| 2 | Misplaced; belongs in a different part of the book |
| 1 | Severely misplaced; disrupts narrative flow |

### D4: Writing Quality (weight: 0.15)
Clarity, voice, professionalism. The book has a distinctive voice (sardonic, data-driven, urgent) that should be preserved.

| Score | Criteria |
|-------|----------|
| 5 | Excellent writing; engaging, clear, professional with personality |
| 4 | Good writing; minor improvements possible |
| 3 | Adequate; some sections unclear or inconsistent in voice |
| 2 | Below standard; needs significant editing |
| 1 | Poor quality; confusing, unprofessional, or voice-less |

### D5: Evidence Quality (weight: 0.15)
Are claims sourced? Are calculations sound? Does it cite credible sources?

| Score | Criteria |
|-------|----------|
| 5 | Every claim cited; calculations verified; strong evidence chain |
| 4 | Most claims cited; minor gaps in evidence |
| 3 | Some unsourced claims; evidence present but incomplete |
| 2 | Many unsourced claims; weak evidence base |
| 1 | Mostly unsourced; assertions without evidence |

### D6: Page Efficiency (weight: 0.10)
Is the length justified by the content value? Could the same points be made in fewer pages?

| Score | Criteria |
|-------|----------|
| 5 | Every page earns its place; tight, dense content |
| 4 | Mostly efficient; minor trimming possible |
| 3 | Some padding; 20-30% could be cut without losing value |
| 2 | Significant bloat; 30-50% could be cut |
| 1 | Severely bloated; core content is a fraction of page count |

### D7: General Accessibility (weight: 0.10)
Can a non-expert (interested general reader) follow this chapter?

| Score | Criteria |
|-------|----------|
| 5 | Crystal clear for general audience; technical concepts explained |
| 4 | Mostly accessible; occasional jargon explained in context |
| 3 | Somewhat technical; some sections may lose general readers |
| 2 | Quite technical; requires background knowledge |
| 1 | Impenetrable for non-experts |

### D8: Policy/Investor Rigor (weight: 0.10)
Would a skeptical economist, policy analyst, or investor find this convincing?

| Score | Criteria |
|-------|----------|
| 5 | Publication-quality rigor; methodology sound, caveats stated |
| 4 | Strong rigor; minor methodological gaps |
| 3 | Moderate rigor; some hand-waving or missing sensitivity analysis |
| 2 | Weak rigor; assertions that would not survive peer review |
| 1 | No analytical rigor; pure advocacy without evidence |

---

## Evaluation Output Format

Each chapter evaluation JSON (`_analysis/curation-evaluations/<slug>.json`):

```json
{
  "href": "knowledge/path/to/chapter.qmd",
  "evaluated": "2026-02-14T12:00:00",
  "scores": {
    "D1_mission_necessity": 4,
    "D2_uniqueness": 5,
    "D3_placement": 4,
    "D4_writing_quality": 4,
    "D5_evidence_quality": 3,
    "D6_page_efficiency": 4,
    "D7_accessibility": 5,
    "D8_policy_rigor": 3
  },
  "rationale": {
    "D1_mission_necessity": "Core chapter explaining the treaty mechanism...",
    "D2_uniqueness": "Only chapter covering this specific topic...",
    "D3_placement": "Good position after problem statement...",
    "D4_writing_quality": "Strong voice, clear structure...",
    "D5_evidence_quality": "Most claims cited but missing source for...",
    "D6_page_efficiency": "Tight at 7 pages, every section needed...",
    "D7_accessibility": "Clear for general audience...",
    "D8_policy_rigor": "Sound methodology but missing sensitivity..."
  },
  "recommendations": [
    "Add citation for claim about X on line Y",
    "Consider adding sensitivity analysis for Z"
  ]
}
```

---

## Chapter Health Score (CHS)

CHS = weighted average of D1-D8 scores, scaled to 0-100.

| CHS | Classification | Recommended Action |
|-----|---------------|-------------------|
| 85-100 | GREEN | Keep as-is |
| 70-84 | YELLOW | Polish (specific fixes) |
| 50-69 | ORANGE | Significant work (merge/restructure/rewrite) |
| 0-49 | RED | Major decision (cut/demote/rewrite) |
