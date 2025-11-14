# Proposed Repository Structure - AI Agent Architecture

## Current Problems

1. **Dual Quarto Projects**: Root `_quarto.yml` + `dih-economic-models/_quarto.yml` causing confusion
2. **Vague Naming**: `brain/` doesn't clearly indicate content purpose
3. **Split Content**: 52 files in `brain/book/` + 102 files in `dih-economic-models/` = parallel hierarchies
4. **Unclear Purpose**: Is this a book repo, economic models repo, or AI agent?

## Proposed Solution: AI Agent with Knowledge Base

### Strategy
1. **Now**: Restructure this repo as an AI agent with clear functional areas (knowledge, tools, models, memory)
2. **Later**: Copy entire repo → prune to create separate `dih-economic-models` repo for models.dih.earth

### Agent Architecture Principles
- **Knowledge**: What the agent knows (book chapters, analysis)
- **Tools**: What the agent can do (scripts, validation, review)
- **Models**: What the agent can calculate (economic parameters, visualizations)
- **Memory**: What the agent remembers (future: learned patterns, conversation history)

---

## RECOMMENDED STRUCTURE

```
decentralized-institutes-of-health/    # AI Agent repo
├── knowledge/                         # Agent's knowledge base (all .qmd content)
│   ├── problem/                       # Knowledge about problems humanity faces
│   ├── solution/                      # Knowledge about solutions (DFDA, DIH)
│   ├── proof/                         # Evidence and rigorous analysis
│   ├── futures/                       # Future scenarios and possibilities
│   ├── strategy/                      # Implementation strategies
│   ├── legal/                         # Legal framework knowledge
│   ├── call-to-action/                # Action steps
│   │
│   ├── economics/                     # Economic analysis (from dih-economic-models/economics/)
│   │   ├── economics.qmd              # Executive summary
│   │   ├── peace-dividend.qmd
│   │   ├── health-dividend.qmd
│   │   ├── victory-bonds.qmd
│   │   ├── financial-plan.qmd
│   │   ├── campaign-budget.qmd
│   │   └── health-savings-sharing-model.qmd
│   │
│   ├── appendix/                      # Supporting data and detailed calculations
│   │   ├── (current brain/book/appendix files)
│   │   └── (merged dih-economic-models/appendix files)
│   │
│   └── figures/                       # Visual knowledge representations (76 .qmd files)
│       ├── disease-vs-war-annual-deaths-pie-chart.qmd
│       ├── ... (75 more)
│
├── dih_models/                        # Agent's calculation capabilities (Python package)
│   ├── __init__.py
│   ├── parameters.py                  # Core economic parameters (2,410 lines)
│   └── plotting/
│       ├── __init__.py
│       ├── chart_style.py             # Matplotlib theming
│       └── graphviz_helper.py         # Diagram generation
│
├── tools/                             # Agent's tools and capabilities (renamed from scripts/)
│   ├── review/                        # Content review and compliance checking
│   ├── validation/                    # Pre-render validation
│   ├── rendering/                     # Book rendering utilities
│   ├── lib/                           # Shared tool libraries
│   └── ...
│
├── memory/                            # Agent's memory (future - gitignored)
│   └── .gitkeep                       # Placeholder for future agent memory
│
├── assets/                            # Static assets (icons, etc.)
│
├── _quarto.yml                        # SINGLE book/knowledge base configuration
├── index.qmd                          # Knowledge base landing page
├── pyproject.toml                     # Python package config
├── requirements.txt
├── package.json                       # Tool execution scripts
├── CLAUDE.md                          # Agent instructions
├── CONTRIBUTING.md                    # Knowledge contribution guide
└── README.md

# Build output (not in git)
├── _book/                             # Rendered knowledge base
├── _freeze/                           # Jupyter cache
└── .quarto/                           # Quarto cache
```

---

## Key Changes Explained

### 1. Knowledge Base: `knowledge/` (formerly `brain/book/`)

**Why "knowledge/"?**
- **AI Agent Architecture**: Aligns with agent's purpose - this is what the agent knows
- **Functional naming**: Clear separation between knowledge (static) and memory (dynamic/learned)
- **Standard terminology**: "Knowledge base" is well-understood in AI/agent systems
- **Scales for future**: Supports future agent capabilities (retrieval, reasoning, synthesis)
- **Human-friendly**: Contributors understand "knowledge about X goes in knowledge/X/"

**Structure:**
- All book chapters organized by topic (problem, solution, proof, etc.)
- Economics analysis integrated (not separate)
- Visual knowledge (figures) in one place
- Supporting data (appendices) merged
- Agent can retrieve and reason over this knowledge base

### 2. Calculation Capabilities: `dih_models/` (formerly `dih-economic-models/`)

**Why rename and restructure?**
- **Agent capability**: This is what the agent can *calculate* (ROI, NPV, QALYs, etc.)
- **Shorter imports**: `from dih_models.parameters import *` (vs `from economic_parameters import *`)
- **Python conventions**: Packages use underscores, not hyphens
- **Clarity**: "models" is specific and descriptive
- **Proper module naming**: `chart_style.py` instead of `_chart_style.py`

**What's included:**
- `parameters.py` - All economic constants and calculations (2,410 lines, single source of truth)
- `plotting/` subpackage - Chart styling and diagram generation capabilities
- Clean, focused API for agent to use

### 3. Tools & Capabilities: `tools/` (formerly `scripts/`)

**Why rename to "tools/"?**
- **Agent-oriented**: These are tools the agent can *execute* (validate, review, render)
- **Clearer purpose**: "tools" is more descriptive than generic "scripts"
- **Standard terminology**: Common in agent architectures (tools = executable capabilities)
- **Functional organization**: Groups by what the tool does, not what it is

**What's included:**
- `review/` - Content review and nonprofit compliance checking
- `validation/` - Pre-render validation tools
- `rendering/` - Book rendering utilities
- `lib/` - Shared tool libraries

### 4. Agent Memory: `memory/` (new, future placeholder)

**Why add this?**
- **Future-proofing**: Placeholder for agent learning and memory
- **Clear separation**: Static knowledge vs dynamic memory
- **Gitignored**: Not part of source control (agent-specific, ephemeral)
- **Standard pattern**: Common in agentic systems

**Future uses:**
- Conversation history
- Learned patterns and preferences
- Agent-specific state
- Cached reasoning results

### 5. Single Quarto Configuration

**Before:**
- `_quarto.yml` (root) - main book
- `dih-economic-models/_quarto.yml` - economic models site
- Confusion about which is canonical

**After:**
- `_quarto.yml` (root only) - the book, period
- Later: Create separate repo with its own `_quarto.yml` for models site

### 6. Removed `dih-economic-models/` Directory

**Before:** Mixed Python package + Quarto content in one directory
**After:** Clear functional separation aligned with agent architecture
- Python code → `dih_models/` (agent's calculation capabilities)
- Quarto content → `knowledge/economics/` and `knowledge/figures/` (agent's knowledge base)
- Clear separation of concerns: what the agent knows vs what it can calculate

---

## Migration Impact Analysis

### Files to Move

| From | To | Count |
|------|-----|-------|
| `brain/book/*` | `knowledge/*` | 52 files |
| `dih-economic-models/economics/*.qmd` | `knowledge/economics/` | 7 files |
| `dih-economic-models/appendix/*.qmd` | `knowledge/appendix/` | 19 files |
| `dih-economic-models/figures/*.qmd` | `knowledge/figures/` | 76 files |
| `dih-economic-models/economic_parameters.py` | `dih_models/parameters.py` | 1 file |
| `dih-economic-models/figures/_chart_style.py` | `dih_models/plotting/chart_style.py` | 1 file |
| `dih-economic-models/figures/_graphviz_helper.py` | `dih_models/plotting/graphviz_helper.py` | 1 file |
| `scripts/*` | `tools/*` | 40+ files |

**Total:** 197+ files moved/renamed

### References to Update

**High Priority (will break):**
1. **All Python imports** in 76 figure files:
   - FROM: `from economic_parameters import *`
   - TO: `from dih_models.parameters import *`

   - FROM: `from figures._chart_style import setup_chart_style, ...`
   - TO: `from dih_models.plotting.chart_style import setup_chart_style, ...`

2. **All cross-references** in .qmd files:
   - FROM: `../../../dih-economic-models/economics/victory-bonds.qmd`
   - TO: `../economics/victory-bonds.qmd` (or similar based on relative path)
   - Estimated: 100+ cross-references to update

3. **_quarto.yml configuration**:
   - Update all chapter paths
   - Remove dih-economic-models subdirectory references
   - Estimated: 50+ path updates

4. **Tools that reference paths**:
   - `tools/review/nonprofit-compliance-check.ts` - hardcoded to `dih-economic-models/`
   - `tools/pre-render-validation.py` - may have path assumptions
   - `tools/lib/file-utils.ts` - may have path logic
   - `package.json` scripts - may reference old paths (scripts/ → tools/)

5. **GitHub Actions workflow**:
   - `.github/workflows/publish.yml` - references `dih-economic-models/` for package install
   - UPDATE: `uv pip install --system -e dih-economic-models/` → `uv pip install --system -e .`

6. **pyproject.toml**:
   - Package name: `decentralized-institutes-of-health` → `dih-models`
   - Package directory configuration

**Medium Priority (may break):**
7. Image paths in .qmd files
8. Links in README.md and documentation
9. Git submodule config (if applicable)

**Low Priority (cosmetic):**
10. Comments mentioning old paths
11. Documentation referring to structure

---

## Python Package Changes

### Before: `dih-economic-models/`

```python
# Installation
pip install -e dih-economic-models/

# Usage in .qmd files
from economic_parameters import *
from figures._chart_style import setup_chart_style, get_figure_output_path
```

### After: `dih_models/`

```python
# Installation
pip install -e .

# Usage in .qmd files
from dih_models.parameters import *
from dih_models.plotting.chart_style import setup_chart_style, get_figure_output_path
```

**Benefits:**
- More explicit imports (clear where functions come from)
- Standard Python package structure
- Easier to understand for new contributors
- Follows PEP 8 naming conventions

---

## Alternative: Minimal Rename (Lower Risk)

If full agent-oriented restructure is too risky, here's a minimal version:

```
knowledge/                         # Renamed from brain/book/ (minimal agent theme)
├── problem/
├── solution/
├── economics/                     # Merged from dih-economic-models/economics/
├── appendix/                      # Merged from dih-economic-models/appendix/
└── figures/                       # Merged from dih-economic-models/figures/

dih_models/                        # Python package (renamed, minimal change)
├── __init__.py
├── parameters.py
└── plotting/

scripts/                           # Keep as-is (don't rename to tools/)

_quarto.yml                        # Single config (remove dih-economic-models/_quarto.yml)
```

**Pros:** Smaller change, less risk, still gets main benefit (single knowledge base)
**Cons:** Less agent-oriented (only knowledge/ conveys agent theme)

---

## Implementation Strategy

### Phase 1: Analyze (Safe, Read-Only)
1. ✅ Analyze current structure (COMPLETE)
2. Create comprehensive file mapping (what moves where)
3. Identify all cross-references
4. Generate automated migration script
5. **Review and validate script WITHOUT running it**

### Phase 2: Execute (Requires Testing)
1. Create git branch for migration
2. Run migration script
3. Update all imports
4. Update _quarto.yml
5. Update scripts
6. Update GitHub Actions
7. Test: Render book locally
8. Test: Run validation scripts
9. Test: Python package installation
10. Commit and review changes

### Phase 3: Create Economic Models Repo (Later)
1. Copy entire agent repo to new location
2. Remove agent-specific content (problem/, solution/, futures/, strategy/, legal/, etc.)
3. Keep only: knowledge/economics/, knowledge/figures/, knowledge/appendix/
4. Create new _quarto.yml for models.dih.earth (formal, foundation-focused)
5. Remove book-specific and agent-specific dependencies (memory/, some tools/)
6. Simplify to pure economic models site
7. Publish as separate repo for public economists

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Broken cross-references | High | High | Automated script + validation |
| Python imports fail | High | High | Update imports + test rendering |
| GitHub Actions break | Medium | High | Update workflow + test before merge |
| Git history lost | Low | Medium | Use `git mv` to preserve history |
| Forgotten references | Medium | Medium | Comprehensive grep before + after |
| Rendering fails | Medium | High | Test render before committing |

---

## Recommendation

**Proceed with FULL AGENT-ORIENTED RESTRUCTURE** because:

1. **Future-proof architecture**: Aligns with your vision of turning this into an AI agent
2. **Clear functional separation**:
   - `knowledge/` = what the agent knows
   - `dih_models/` = what the agent can calculate
   - `tools/` = what the agent can do
   - `memory/` = what the agent remembers (future)
3. **One-time migration cost**: Pain now, permanent clarity later
4. **Better for AI/human collaboration**: Both humans and AI understand the structure intuitively
5. **Easy derivative**: Later copying and pruning for economic models site will be simpler
6. **Standard patterns**: Follows common agent architecture conventions
7. **Python best practices**: Proper package naming and structure

**Next Steps:**
1. Review this proposal
2. Approve structure or suggest modifications
3. I'll create comprehensive migration script (read-only analysis)
4. Review script output for issues
5. Execute on a branch when ready

---

## Questions to Resolve

1. **Package name**: `dih_models` or something else? ✅ DECIDED: `dih_models`
2. **Knowledge directory**: `knowledge/` confirmed ✅
3. **Tools directory**: Rename `scripts/` → `tools/`? ✅ YES (recommended for agent theme)
4. **Memory placeholder**: Add `memory/` directory (gitignored)? ✅ YES (future-proofing)
5. **Figures consolidation**: Keep 76 separate files or merge related ones?
6. **Timing**: Do this now or after current work?
7. **Testing strategy**: Local render only or deploy to test site?

## Agent Architecture Summary

**Final Structure:**
```
knowledge/     # What the agent KNOWS (static, curated, versioned)
dih_models/    # What the agent CALCULATES (Python package)
tools/         # What the agent DOES (validation, review, rendering)
memory/        # What the agent REMEMBERS (dynamic, learned, gitignored)
```

This structure makes the repo's purpose immediately clear: **An AI agent that knows how to end war and disease, can calculate economic models, has tools to validate and review content, and can learn from interactions.**
