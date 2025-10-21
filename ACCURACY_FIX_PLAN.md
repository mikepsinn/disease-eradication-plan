# Systematic Accuracy Fix Plan

## Overview

Based on the audit, we have 3,021 potential issues:

- **205 HIGH severity** (factually wrong/unfair)
- **2,770 MEDIUM severity** (potentially misleading)
- **46 LOW severity** (could be improved)

## Priority Order

### Phase 1: Fix HIGH Severity Issues (205 total)

These are the most critical - factually wrong or unfairly accusatory statements.

#### 1.1 False Attribution of Intent (37 instances)

**Pattern**: "demands", "forces", "makes us", "requires"
**Files most affected**:

- brain/book/problem/fda-is-unsafe-and-ineffective.qmd
- brain/book/problem/nih-spent-1-trillion-eradicating-0-diseases.qmd
- brain/book/theory/central-planning-kills.qmd

**Fix Template**:

```
BEFORE: "NIH demands $41,000/patient"
AFTER: "The current system results in $41,000/patient costs"

BEFORE: "FDA forces 17-year delays"
AFTER: "FDA's approval process takes 17 years on average"

BEFORE: "Politicians make us spend on weapons"
AFTER: "Political incentives favor military spending"
```

#### 1.2 Personal/Character Attacks (45 instances)

**Pattern**: "idiots", "morons", "evil", "corrupt", "sociopaths"
**Files most affected**:

- brain/book/problem/regulatory-capture.qmd
- brain/book/theory/public-choice.qmd
- OUTLINE.md

**Fix Template**:

```
BEFORE: "200 idiotic bureaucrats"
AFTER: "200-person committees"

BEFORE: "Corrupt regulators"
AFTER: "Regulators influenced by revolving door incentives"

BEFORE: "Politicians are sociopaths"
AFTER: "Politicians respond to electoral incentives"
```

#### 1.3 Conspiracy Language (8 instances)

**Pattern**: "deliberately", "intentionally", "purposely", "scheme"
**Files most affected**:

- brain/book/problem/regulatory-capture.qmd
- brain/book/economics/coalition-that-wins.qmd

**Fix Template**:

```
BEFORE: "FDA deliberately delays cures"
AFTER: "FDA's risk-averse culture results in delays"

BEFORE: "Pharma intentionally keeps people sick"
AFTER: "Pharma's business model profits from treatment over cures"
```

#### 1.4 Misleading Agency Attribution (15 instances)

**Pattern**: Wrong agency blamed for something
**Common mistakes**:

- Attributing FDA regulations to NIH
- Blaming NIH for trial costs (FDA sets requirements)
- Confusing WHO achievements with NIH

**Fix Template**:

```
BEFORE: "NIH's $41,000 trial costs"
AFTER: "FDA-regulated trials cost $41,000"

BEFORE: "NIH approval process"
AFTER: "FDA approval process"
```

### Phase 2: Fix Pattern-Based MEDIUM Issues (2,770 total)

#### 2.1 Absolute Statements (892 instances)

**Pattern**: "all", "every", "never", "always", "zero", "nobody"
**Automated fix**: Add qualifiers

**Fix Template**:

```
BEFORE: "Every regulator is captured"
AFTER: "Many regulators face capture risks"

BEFORE: "Nobody reads these papers"
AFTER: "Few people read most papers"

BEFORE: "Zero diseases cured"
AFTER: "No major diseases eradicated" (technically accurate)
```

#### 2.2 Unsourced Statistics (1,878 instances)

**Pattern**: Numbers without citations
**Automated fix**: Add references where available, mark [citation needed] otherwise

### Phase 3: Tone Calibration (46 LOW severity)

#### 3.1 Oversimplifications

**Pattern**: "just", "simply", "only"
**Fix**: Add nuance without losing clarity

## Implementation Strategy

### Week 1: Manual HIGH Priority Fixes

1. **Monday-Tuesday**: Fix false attribution (37 instances)
2. **Wednesday-Thursday**: Remove character attacks (45 instances)
3. **Friday**: Fix conspiracy language and agency confusion (23 instances)

### Week 2: Semi-Automated MEDIUM Fixes

1. **Create replacement dictionary** for common patterns
2. **Run batch replacements** with human review
3. **Add citation links** to all statistics

### Week 3: Quality Control

1. **Read-through for consistency**
2. **Verify tone remains urgent but fair**
3. **Check all citations work**

## Automated Fix Script

```typescript
// fix-accuracy-issues.ts
const replacements = {
  // False attribution
  "demands": "results in",
  "forces": "leads to",
  "requires": "involves",

  // Character attacks
  "idiots": "decision-makers",
  "morons": "officials",
  "evil": "misaligned",
  "corrupt": "influenced by incentives",
  "sociopaths": "self-interested actors",

  // Conspiracy
  "deliberately": "systematically",
  "intentionally": "consistently",
  "purposely": "predictably",
  "scheme": "system",

  // Absolutes (context-dependent)
  "all politicians": "most politicians",
  "every regulator": "many regulators",
  "never works": "rarely works",
  "always fails": "usually fails",
  "nobody cares": "few prioritize",
};
```

## Success Metrics

### Accuracy Improvements

- [ ] 0 false attributions of intent
- [ ] 0 personal attacks
- [ ] 0 conspiracy theories
- [ ] 0 agency misattributions
- [ ] <10% absolute statements
- [ ] 100% statistics cited

### Tone Preservation

- [ ] Dark humor intact
- [ ] Urgency maintained
- [ ] System critique sharp
- [ ] Public choice framing clear

## Key Principles for All Fixes

1. **Attack systems, not people**
   - YES: "The grant system wastes researcher time"
   - NO: "Grant reviewers are idiots"

2. **Explain incentives, not morals**
   - YES: "FDA's liability concerns create delays"
   - NO: "FDA wants people to die"

3. **Use data, not hyperbole**
   - YES: "150,000 die daily from disease"
   - NO: "FDA commits genocide"

4. **Acknowledge nuance**
   - YES: "Many factors contribute to high costs"
   - NO: "It's all FDA's fault"

5. **Maintain urgency through facts**
   - YES: "Every day costs 410 preventable deaths"
   - NO: "They're murdering your family"

## Files Requiring Most Work (by HIGH severity count)

1. **OUTLINE.md** - 43 HIGH issues
2. **brain/book/problem/regulatory-capture.qmd** - 18 HIGH
3. **brain/book/problem/fda-is-unsafe-and-ineffective.qmd** - 15 HIGH
4. **brain/book/theory/central-planning-kills.qmd** - 12 HIGH
5. **brain/book/economics/coalition-that-wins.qmd** - 11 HIGH

## Next Steps

1. **Review this plan** with stakeholders
2. **Prioritize which files to fix first**
3. **Create backup** of all files before changes
4. **Track changes** in version control
5. **Test** that core message remains strong

## Estimated Timeline

- **HIGH severity fixes**: 3-4 days of focused work
- **MEDIUM severity fixes**: 5-7 days with automation
- **Final review**: 2-3 days
- **Total**: 2-3 weeks for complete accuracy overhaul

The goal: Make every claim bulletproof while keeping the dark humor and urgency that makes this book compelling.