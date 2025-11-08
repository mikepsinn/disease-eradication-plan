# Tone Review System

## Philosophy: Technical Manual from Wishonia

The book is presented as an implementation guide from Wishonia, where they successfully deployed Wishocracy centuries ago. This is a LIGHT TOUCH approach - we're not radically changing the book, just fixing pompous/earnest bits.

## The Approach
- Keep 95% of the book as-is
- Only fix genuinely pompous declarations ("BEST IDEA EVER!")
- Transform earnest evangelism → matter-of-fact instructions
- Add occasional "Implementation Notes from Wishonia" where natural

## What We Transform (SELECTIVE)

### ❌ Earnest/Pompous
"This Is Quantifiably The Best Idea Ever Conceived!"

### ✅ Technical Documentation
"Implementation Guide: 1% Resource Reallocation Protocol (Wishonia Standard 2847-B)"

## What We Keep
- Dark humor that already works ("Dead people file zero claims")
- Historical references and factual irony
- Clever wordplay ("First war on anything designed to win")
- Self-deprecating humor ("The Complete Idiot's Guide...")

## Scripts

### 1. Check Status
```bash
npx tsx scripts/review/check-tone-status.ts
```
Shows which files have been reviewed and which still need attention.

### 2. Identify Files Needing Review
```bash
npx tsx scripts/review/elevate-tone-intelligent.ts
```
Scans for files that haven't been reviewed for tone.

### 3. Update File Hash (Mark as Reviewed)
```bash
npx tsx scripts/review/update-hash.ts [filepath] TONE_ELEVATION_WITH_HUMOR
```
Marks a file as reviewed after manual tone adjustment.

## Process

1. **Read the tone guide**: `scripts/prompts/tone-guide.md`
2. **Identify files**: Run `elevate-tone-intelligent.ts`
3. **Review priority files** in `TONE_REVIEW_PRIORITY` (see constants.ts)
4. **Transform earnest language** to technical documentation
5. **Preserve ALL humor** that already works
6. **Mark complete**: Update hash when done

## The Test

Before: "This will SAVE HUMANITY!"
After: "Implementation timeline: 95% reduction in preventable deaths within 10 years (based on 47 planetary deployments)."

The goal: Transform breathless evangelism into matter-of-fact technical documentation.

## Remember

**Good tone:** "Standard ROI for healthcare reallocation: 463:1 (see Appendix for methodology)"

**Bad tone:** "UNPRECEDENTED returns that will REVOLUTIONIZE everything!"

Keep the facts, fix the tone. Think IKEA manual for universal healthcare, not TED talk.