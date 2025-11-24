# TODO: economics.qmd Improvements and Parameter System Optimization

## Current Stats
- **397 parameters**
- **147 LaTeX equations**
- **125 citation keys**
- **Zero validation errors**

---

## Optional Improvements

### Documentation

- [ ] **Add inline comments for intentionally hardcoded parameters**
  - Some "calculated" parameters are intentional estimates (e.g., DFDA_UPFRONT_BUILD)
  - Add comments like: `# Intentional estimate, not calculated from other params`
  - Prevents confusion about which parameters need formulas

- [ ] **Create parameter dependency graph**
  - Visualize which parameters depend on which others
  - Help identify circular dependencies or missing calculations
  - Could be auto-generated from parameter formulas
