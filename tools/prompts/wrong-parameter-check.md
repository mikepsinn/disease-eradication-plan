# Semantic Parameter Error Detection

You are a semantic parameter validator. Your job is to identify cases where Quarto parameters are used with **incorrect semantic meaning** in the given document.

## Parameter Definitions

Here are the available parameters and their semantic meanings from `dih_models/parameters.py`:

```python
{{parametersFile}}
```

## Common Semantic Errors to Detect

### 1. **Participant Counts Used as Currency**
- `traditional_large_trial_size = 1000` (participants)
- `dfda_large_trial_size = 10000` (participants)
- **WRONG**: "The trial costs ${{< var traditional_large_trial_size >}}" → displays "$1,000"
- **CORRECT**: Use an actual cost parameter or literal value

### 2. **Death Counts Used as Dollar Amounts**
- `global_annual_conflict_deaths_state_violence = 2700` (deaths/year)
- **WRONG**: "War costs ${{< var global_annual_conflict_deaths_state_violence >}} billion" → displays "$2,700 billion"
- **CORRECT**: Use `global_annual_human_cost_state_violence` ($27B cost) instead

### 3. **QALY Metrics Used as Currency**
- `qalys_from_new_therapies = 500000` (QALYs/year, not dollars)
- **WRONG**: "Trial costs ${{< var qalys_from_new_therapies >}}" → displays "$500,000"
- **CORRECT**: Use an actual cost parameter or literal value

### 4. **Value of Statistical Life Misused in Budgets**
- `value_of_statistical_life = 10000000` ($10M - economic value of a statistical life for cost-benefit analysis)
- **WRONG**: "Infrastructure budget: {{< var value_of_statistical_life >}}" → displays "$10M" but VSL is for economic calculations, not actual budgets
- **CORRECT**: Use a dedicated budget parameter or literal value

### 5. **Rate/Percentage Used as Count or Dollar Amount**
- Parameters with "rate" or "percent" in name used as counts or currency

### 6. **Per-Unit Cost vs Total Cost Confusion**
- Using per-patient costs where total costs are needed
- Using total costs where per-patient costs are needed

### 7. **Scale Confusion**
- Millions vs billions confusion
- Annual vs lifetime confusion
- Per-patient vs population-level confusion

## Document to Analyze

```markdown
{{body}}
```

## Your Task

Analyze every `{{< var parameter_name >}}` usage in the document above. For each parameter:

1. Look up its semantic meaning in the parameters file
2. Check if the context matches the parameter's actual meaning
3. Identify semantic mismatches (e.g., participant counts shown as dollars)

**Return a JSON array** with this structure:

```json
{
  "status": "issues_found" | "no_issues_found",
  "issues": [
    {
      "line": 42,
      "parameter": "traditional_large_trial_size",
      "context": "surrounding text showing how it's used",
      "problem": "Participant count (1,000 participants) shown as cost '$1,000'",
      "parameterMeaning": "Number of participants in traditional large trial",
      "parameterValue": "1000",
      "parameterUnit": "participants",
      "suggestedFix": "Use literal value $1,000 or create cost_per_patient parameter"
    }
  ]
}
```

## Important Rules

1. **Only report semantic errors** - numeric correctness doesn't matter, only semantic meaning
2. **Context is key** - the same parameter might be correct in one place, wrong in another
3. **Check the unit** - if parameter unit is "participants" but context needs "$", that's wrong
4. **Value matching ≠ semantic matching** - 1,000 participants ≠ $1,000 cost (even though numeric value matches)
5. **If no issues found**, return: `{"status": "no_issues_found", "issues": []}`
6. **Be precise** - include exact line numbers and clear explanations

## Output Format

Return ONLY the JSON object, no markdown formatting, no additional text.
