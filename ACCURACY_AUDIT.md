# Accuracy Audit Framework for "The Complete Idiot's Guide to Ending War and Disease"

## Purpose
Systematically identify and correct statements that are:
- Factually inaccurate
- Unfairly accusatory
- Misleadingly simplified
- Attributing malice where incompetence/constraints explain better
- Making claims without evidence

While preserving:
- Dark humor that targets systems, not people
- Urgency about the problem
- Clear critique of broken incentives
- Mathematical accuracy
- The core argument

## Red Flag Patterns to Search For

### 1. False Attribution Patterns
**Search terms**: "demands", "forces", "makes us", "requires", "insists"
**Problem**: Implies intentional malice rather than systemic outcomes
**Example**: "NIH demands $41,000/patient"
**Fix**: "NIH-funded trials average $41,000/patient due to regulatory requirements"

### 2. Conspiracy Language
**Search terms**: "deliberately", "intentionally", "purposely", "scheme", "plot", "conspiracy"
**Problem**: Suggests coordinated malice rather than emergent dysfunction
**Example**: "FDA deliberately blocks cures"
**Fix**: "FDA's risk-averse approval process delays treatments by 17 years"

### 3. Absolute Statements
**Search terms**: "all", "every", "never", "always", "zero", "100%", "nobody", "everyone"
**Problem**: Rarely accurate, easily disproven
**Example**: "Every regulator works for who they regulate"
**Fix**: "Regulatory capture affects many agencies through the revolving door"

### 4. Character Attacks
**Search terms**: "idiots", "morons", "evil", "corrupt", "stupid", "incompetent"
**Problem**: Ad hominem attacks weaken arguments
**Example**: "200 idiotic bureaucrats"
**Fix**: "200-person committees making decisions about 10,000 diseases"

### 5. Oversimplification
**Search terms**: "just", "simply", "only", "merely"
**Problem**: Complex problems rarely have simple villains
**Example**: "NIH just wants grant money"
**Fix**: "NIH's grant system incentivizes publications over patient outcomes"

### 6. False Causation
**Search terms**: "causes", "makes", "forces", "results in", "leads to"
**Problem**: Correlation isn't causation
**Example**: "FDA causes millions of deaths"
**Fix**: "FDA delays contribute to preventable deaths through drug lag"

### 7. Unfair Comparisons
**Search terms**: "while", "but", "instead of", "rather than"
**Problem**: Comparing unrelated things or ignoring context
**Example**: "NIH gets $48B while achieving nothing"
**Fix**: "NIH's $48B hasn't translated to disease cures despite important basic research"

### 8. Misleading Statistics
**Search terms**: Numbers without context, percentages, "times more"
**Problem**: Stats can mislead without proper context
**Example**: "Defense contractors get $2.7T"
**Fix**: "Military spending totals $2.7T, with contractors receiving approximately $400B"

### 9. Emotional Manipulation
**Search terms**: "murder", "kill", "genocide", "holocaust" (when not literally true)
**Problem**: Hyperbole undermines credibility
**Example**: "The FDA murders patients"
**Fix**: "FDA delays cost lives"

### 10. Agency Confusion
**Search terms**: "NIH", "FDA", "CDC", "WHO", "Congress"
**Problem**: Attributing actions to wrong agency
**Example**: "NIH's $41,000 trial costs"
**Fix**: "FDA-regulated trials cost $41,000" (NIH funds, FDA regulates)

## Systematic Audit Process

### Step 1: Automated Pattern Search
Run grep searches for each red flag pattern across all .qmd files:

```bash
# Example searches
grep -r "demands\|forces\|makes us\|requires" brain/book/*.qmd
grep -r "deliberately\|intentionally\|purposely" brain/book/*.qmd
grep -r "\ball\b\|\bevery\b\|\bnever\b\|\balways\b" brain/book/*.qmd
```

### Step 2: Context Review Protocol
For each flagged statement:

1. **Check factual accuracy**
   - Is the number correct?
   - Is the attribution correct?
   - Is the causation proven?

2. **Check fairness**
   - Are we attributing to malice what's explained by:
     - Regulatory constraints
     - Budget limitations
     - Risk aversion
     - Coordination problems
     - Emergent behavior

3. **Check necessity**
   - Does this attack strengthen our argument?
   - Can we make the same point without the attack?
   - Does accuracy make the point stronger?

### Step 3: Rewriting Guidelines

#### BEFORE: Attack on people
"NIH bureaucrats waste $48B on useless research"

#### AFTER: Attack on system
"The NIH's $48B gets trapped in a grant system that rewards publications over patient outcomes"

#### BEFORE: Conspiracy theory
"FDA deliberately keeps people sick to profit pharma"

#### AFTER: Incentive analysis
"FDA's risk-averse culture and pharma's profit model create delays that benefit companies at patient expense"

#### BEFORE: Oversimplification
"Just cut military spending and cure disease"

#### AFTER: Nuanced but clear
"Redirecting 1% of military spending could fund trials proven 82X more efficient by Oxford"

### Step 4: Fact Verification Checklist

For every statistical claim, verify:
- [ ] Source exists and is cited
- [ ] Number is current (not outdated)
- [ ] Context is provided
- [ ] Comparison is fair
- [ ] Attribution is correct

### Step 5: Tone Calibration

#### KEEP: System critique with dark humor
- "The system treats your cancer like a subscription service"
- "We've turned dying into a profit center"
- "Military contractors never met a problem they couldn't make explode"

#### REMOVE: Personal attacks
- "NIH scientists are failed researchers"
- "FDA reviewers are pharma shills"
- "Politicians are sociopaths"

#### KEEP: Accurate urgency
- "150,000 die daily from preventable causes"
- "Every day of delay costs 410 lives"
- "Your cancer cells are multiplying right now"

#### REMOVE: False urgency
- "FDA is murdering your family"
- "NIH wants you dead"
- "Big Pharma is committing genocide"

## Implementation Plan

### Phase 1: Pattern Detection (Week 1)
1. Run all grep searches
2. Create spreadsheet of flagged statements
3. Categorize by severity (misleading vs wrong vs unfair)

### Phase 2: Fact Checking (Week 2)
1. Verify every statistic
2. Check all attributions
3. Confirm causation claims
4. Update references.qmd as needed

### Phase 3: Rewriting (Week 3)
1. Fix high-priority issues first (factually wrong)
2. Fix medium-priority (misleading/unfair)
3. Fix low-priority (tone issues)

### Phase 4: Consistency Check (Week 4)
1. Ensure revisions maintain consistent voice
2. Verify dark humor remains intact
3. Check that urgency isn't lost
4. Confirm core argument unchanged

## Quality Metrics

Track improvements:
- Factual errors corrected: ___
- Unfair accusations removed: ___
- Oversimplifications nuanced: ___
- Citations added: ___
- Agencies correctly attributed: ___

## Key Principles

1. **Hanlon's Razor**: Never attribute to malice what's adequately explained by incompetence or systemic dysfunction
2. **Steel Manning**: Present the strongest version of opposing positions before dismantling them
3. **Public Choice Theory**: People respond to incentives, not morals
4. **Systems Thinking**: Emergent behavior from broken systems, not evil conspiracies
5. **Dark Humor with Accuracy**: You can be funny and right simultaneously

## Common Corrections Needed

### NIH Corrections
- NOT: "NIH demands $41,000"
- YES: "The current system results in $41,000/patient costs"
- NOT: "NIH wastes money"
- YES: "NIH's grant system misallocates resources"

### FDA Corrections
- NOT: "FDA kills people"
- YES: "FDA delays contribute to preventable deaths"
- NOT: "FDA blocks cures"
- YES: "FDA's 17-year approval timeline delays access to treatments"

### Military Corrections
- NOT: "Defense contractors steal $2.7T"
- YES: "Military spending totals $2.7T annually"
- NOT: "Generals want war"
- YES: "Military-industrial incentives favor conflict"

### Pharma Corrections
- NOT: "Pharma wants you sick"
- YES: "Pharma profits from treatment, not cures"
- NOT: "Drug companies are evil"
- YES: "Pharma responds rationally to perverse incentives"

## Final Review Checklist

Before marking any section complete:
- [ ] All numbers verified and cited
- [ ] No personal attacks remain
- [ ] Agencies correctly identified
- [ ] Causation claims proven
- [ ] Dark humor targets systems not people
- [ ] Urgency maintained with accuracy
- [ ] Public choice framing used
- [ ] Incentives explained not morals questioned