---
title: 'War on Disease Website PRD (MVP)'
description: 'Concise, unambiguous PRD for the MVP website: scope, routes, components, calculators (formulas), analytics, A/B testing, tech, and acceptance criteria.'
published: true
date: '2025-08-23T00:00:00.000Z'
tags: website, prd, nextjs, mvp, calculators, analytics, ab-testing
editor: markdown
dateCreated: '2025-08-23T00:00:00.000Z'
---

## 0. Purpose (Single Page, Zero Ambiguity)
- Build a public website that renders the core narrative from [War on Disease — Landing](../strategy/warondisease-landing.md), shows value flows and returns, and converts visitors.
- MVP is a single-page app (SPA feel with SSR) with calculators and visualizations; persona-targeted copy via flags.

## 1. Scope (MVP)
- Render styled content from `../strategy/warondisease-landing.md` (including Mermaid diagrams).
- Calculators: Investor ROI, Societal Dividend.
- Visualizations: Military vs Medical spending bars; Captured vs Societal Dividend; reuse Sankey (Mermaid) already in landing.
- CTAs: Referendum, Investor intro, Partner call (outbound links or simple forms).
- A/B testing for hero headline/CTA; analytics + attribution.

Out of scope (MVP): Authentication, full CMS, payments, production referendum widget, referral points ledger.

## 2. Personas & Primary CTAs
- Patients/Citizens → "Get your referendum link" (outbound to [Global Referendum](../strategy/referendum/global-referendum-implementation.md)).
- Investors → "Request investor intro" (mailto or form).
- Partners (universities/nonprofits/companies) → "Request partner call" (mailto or form).

## 3. Information Architecture & Routes
- Route: `/` (single page). Sections with anchors:
  - `#hero`, `#problem`, `#solution`, `#treasury-model`, `#calculators`, `#visualizations`, `#learn-more`, `#contact`.
- Variants via URL params:
  - Persona: `?persona=patients|investors|partners` → toggles headline subtitle + primary CTA text.
  - A/B: `?variant=a|b` → headline/CTA copy variants.

## 4. Tech Stack
- Next.js (App Router) + TypeScript; Tailwind CSS; MDX for rendering landing content; Mermaid renderer for diagrams; Chart.js for charts.
- Analytics: Plausible (or PostHog) with custom events.
- Deployment: Vercel with preview URLs; CI: lint/typecheck/build.

## 5. Content Rendering
- Source: `../strategy/warondisease-landing.md` (render as MDX).
- Requirements:
  - Support Mermaid code blocks (including existing Sankey).
  - Preserve all internal markdown links and anchors per repo linking policy.
  - Style per "Art Direction" section in the landing doc (monochrome palette, currency-like aesthetic).

## 6. Components (IDs, Props, Acceptance)
- Hero (`Hero`): props { headline, subhead, primaryCta {label, href}, secondaryCta? }
  - Acceptance: Two variants selectable via `variant` flag; renders within 1,200px container, responsive, passes Lighthouse a11y 95+.
- StatBar (`StatBar`): two bars for spending comparison.
  - Acceptance: Labels: MILITARY (\$2.718T), MEDICAL RESEARCH (\$67.5B); proportional widths; accessible text.
- CalculatorInvestor (`CalcInvestorRoi`): see formulas (Section 7.1).
  - Acceptance: Inputs validate ranges; outputs update instantly; download CSV button exports schedule.
- CalculatorSocietal (`CalcSocietalDividend`): see formulas (Section 7.2).
  - Acceptance: Shows Captured vs Societal; optional per-capita; copy-to-clipboard summary.
- VizDividendCompare (`DividendCompareChart`): stacked bars for Captured vs Societal.
  - Acceptance: Exact values from calculator inputs; aria labels present.
- CTAGroup (`CTAGroup`): three CTAs with tracking.
  - Acceptance: Clicks fire analytics events with UTM context.

## 7. Calculators (Formulas & I/O)
### 7.1 Investor ROI (Illustrative, Non-binding)
Inputs:
- `investment` (USD): number > 0
- `adoption` (0..1): fraction of 1% Treaty achieved (e.g., 1.0 = full \$27B)
- `investorShare` (0..1): investor’s share of the total investor pool (default 0.01)
- `years` (integer 1..10, default 10)
- `targetCagr` (default 0.40) — target CAGR for cumulative return

Constants:
- `capturedAnnual = 27_000_000_000 * adoption`
- `payoutPoolAnnual = 0.5 * capturedAnnual` (Mission Guarantee cap)

Target path:
- `cumTarget(y) = investment * (1 + targetCagr)^y`
- `annualTarget(y) = cumTarget(y) - cumTarget(y-1)` with `cumTarget(0)=investment`

Cap path (available to this investor):
- `capForInvestorAnnual = payoutPoolAnnual * investorShare`

Actual payout per year:
- `payout(y) = min(annualTarget(y), capForInvestorAnnual)`

Outputs:
- Table: year, payout(y), cumulative paid, remaining to reach `cumTarget(years)`
- Summary: total paid, IRR (computed from cash flows: -investment at t0, `payout(y)` at each year)

Acceptance:
- For `adoption=1, investorShare=1`, total yearly payouts across all investors never exceed 50% of captured income.
- CSV export matches on-screen table values exactly.

Disclaimers: Display “Illustrative only, not an offer.”

### 7.2 Societal Dividend
Inputs:
- `adoption` (0..1)
- `population` (optional, default 8_000_000_000)

Constants:
- `capturedAnnual = 27_000_000_000 * adoption`
- `societalAnnual = 165_000_000_000 * adoption`

Derived:
- `perCapitaCaptured = capturedAnnual / population`
- `perCapitaSocietal = societalAnnual / population`

Outputs:
- Numbers: capturedAnnual, societalAnnual
- Per-capita values
- Chart via `DividendCompareChart`

Acceptance: Values update instantly and remain consistent across components.

## 8. Visualizations
- Military vs Medical Bar Chart
  - Data: Military = \$2.718T, Medical Research = \$67.5B.
  - Acceptance: Bars proportional within component width; values displayed with short scale.
- Dividend Compare (Captured vs Societal)
  - Data from CalculatorSocietal; stacked or side-by-side bars.
  - Acceptance: Tooltips show exact amounts.
- Sankey: Use existing Mermaid diagram in landing content; no additional dev work beyond Mermaid support.

## 9. A/B Testing
- Mechanism: URL param `variant=a|b`; persisted in cookie `wd_variant` for 30 days; server-side read in middleware to set variant flag.
- Scope: Hero headline/subhead + primary CTA label.
- Acceptance: Variant stays consistent across navigation and refresh within cookie window.

## 10. Analytics & Attribution
- Provider: Plausible or PostHog.
- Events (all include: `persona`, `variant`, UTM params if present):
  - `cta_click` { id: referendum|investor_intro|partner_call, href }
  - `calc_investor_submit` { investment, adoption, investorShare, years }
  - `calc_societal_submit` { adoption, population }
  - `outbound_click` { href }
- Acceptance: Events visible in dashboard; no PII stored.

## 11. Accessibility, Performance, SEO (Acceptance)
- a11y: WCAG 2.1 AA, keyboard focus, aria labels, color contrast ≥ 4.5:1
- Performance: Lighthouse performance ≥ 90 on mobile; images optimized; JS bundle under 300KB gz (MVP)
- SEO: Semantic headings, meta tags, Open Graph/Twitter cards; canonical URL

## 12. Embeddables (Stubs for Post-MVP)
- Provide iframes endpoints: `/embed/referendum`, `/embed/donate`, `/embed/calculator` (static placeholder content)
- Acceptance: Iframes render minimal responsive content and post `ready` message.

## 13. Environment & Deployment
- Envs: `NEXT_PUBLIC_ANALYTICS_KEY`, `NEXT_PUBLIC_DEFAULT_PERSONA`, `NEXT_PUBLIC_AB_DEFAULT`
- Deployment: Vercel preview for every PR; main branch → production.

## 14. Definition of Done
- All acceptance criteria above satisfied.
- QA pass: a11y, performance, SEO.
- Events verified in analytics.
- Links validated; no 404s.
- Content parity with `warondisease-landing.md` including Mermaid rendering and the DIH Value Flywheel.
