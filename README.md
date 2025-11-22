# Disease Eradication Plan

Hello, humans.

I am WISHONIA.  I've been watching your species for 80 years, and I have notes.

You currently spend 40 times more money on bombs than on curing diseases. Every day, 150,000 of you permanently discontinue existing from diseases that are basically just engineering problems with meat robots.

This is mathematically stupid.

I've created this **Disease Eradication Plan** explaining how to fix this using your own broken economic system against itself and you're going to help me make it better.

Not because you're altruistic (you're not), but because the math is so obvious that even humans who eat tide pods could understand it.

## What This Is

A complete strategic plan to get nations to sign the **1% Treaty** - redirecting just 1% of military spending ($27.2B annually) to fund hyper-efficient decentralized pragmatic clinical trials.

Everything is calculated, cited, and designed to work WITH human dysfunction, not against it.

## Why You Should Help

**For the idealists:** You'll help save 150,000 lives daily from preventable diseases.

**For the pragmatists:** This is the highest-ROI intervention in human history (beating smallpox eradication).

**For the skeptics:** Everything is sourced, calculated, and peer-reviewable. The math doesn't care about your feelings.

**For the bored:** You named your planet "dirt" and your war building after its shape. This project is more interesting than that.

## What Needs Your Help

This plan is 95% complete but needs:

1. **Fact-checking**: Every parameter is sourced, but humans make mistakes
2. **Writing improvements**: Make it clearer, funnier, more persuasive
3. **Technical corrections**: Fix broken calculations, improve figures
4. **Additional research**: Find better sources, update statistics
5. **Translation**: Eventually, we need this in every human language

## How to Contribute

### Prerequisites

- **Quarto** (for rendering the plan)
- **Python 3.10+** (for calculations and validation)
- **Node.js 18+** (for TypeScript scripts)

### Setup

```bash
# Clone repository
git clone https://github.com/wishonia/disease-eradication-plan.git
cd disease-eradication-plan

# Install Python dependencies
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Render to HTML
quarto render
```

### Project Structure

- **[`knowledge/`](knowledge/)**: All content organized by topic
- **[`dih_models/parameters.py`](dih_models/parameters.py)**: All calculations and variables
- **[`CONTRIBUTING.md`](CONTRIBUTING.md)**: Writing standards and style guide

### Making Changes

1. **Find a task** in [`todo.md`](todo.md) or propose your own
2. **Read the style guide** in [`CONTRIBUTING.md`](CONTRIBUTING.md)
3. **Make your changes** following existing patterns
4. **Validate everything**:
   ```bash
   # Check parameter references
   .venv\Scripts\python.exe scripts\pre-render-validation.py

   # Render and review
   quarto render
   ```
5. **Submit a pull request** with clear explanation

### Key Principles

- **Every number must have a source** (defined in [dih_models/parameters.py](dih_models/parameters.py) and [knowledge/references.qmd](knowledge/references.qmd))
- **Be funny**
- **Math must be correct** (we're fighting human stupidity with arithmetic)
- **Citations required** (credibility depends on it)

## The Core Idea (In Case You Skipped Everything)

Humanity spends $2.7 trillion on war and $68 billion on medical research.

This is like buying 40 umbrellas while your house is on fire.

The 1% Treaty redirects just $27.2B/year (1% of military spending) to fund pragmatic clinical trials that:
- Cost 82x less than current FDA trials
- Generate 115 years of research progress per actual year
- Save 184.6M lives over 20 years
- Create $163.6B in annual economic benefits
- Return ∞ ROI (because new spending = $0)

Every nation reduces military budgets by 1% simultaneously. Security balance unchanged. Everyone gets:
- 1% fewer nukes pointed at them
- Access to experimental treatments years sooner
- Economic returns that make venture capital look conservative

## Your Role

You're helping me show humanity how to save itself using the same broken economic system that got it into this mess.

It's like teaching a dog calculus, except the dog has nuclear weapons and the calculus is "spend less on things that kill you."

If we succeed, future historians will say: "They were on the brink of destroying themselves, but then some random contributors on GitHub helped an alien AI write a create a plan for proper resource allocation, and somehow that worked."

If we fail, the cockroaches will evolve intelligence and wonder why you spent more on bombs than curing diseases.

## License

See [LICENSE](LICENSE) and [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Questions?

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) first.

Still confused? That's very human of you. Open an issue and explain which part of "redirect 1% of war money to cure diseases" requires clarification.

---

*WISHONIA*

*World Integrated System for High-Efficiency Optimization, Networked Intelligence, and Allocation*

*Still Watching. Still Concerned. Now Accepting Pull Requests.*
