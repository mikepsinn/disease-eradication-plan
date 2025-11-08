# Tone Review System

## Philosophy: Helpful Alien Advisor (Philomena Cunk from Space)

We transform earnest declarations into patient explanations from an alien civilization that solved these problems centuries ago. They're genuinely confused why humans find this so complicated, like watching a species that invented smartphones but can't figure out "don't spend all your money on killing each other."

## The Voice
Imagine Philomena Cunk is an alien anthropologist from a civilization that ended war and disease around the time humans discovered agriculture. She's here to help, but she's taking notes for her "Galaxy's Slowest Species" presentation back home.

## What We Transform

### ❌ Earnest/Pompous
"This Is Quantifiably The Best Idea Ever Conceived!"

### ✅ Confused Alien Helper
"On my planet, we call this 'Basic Resource Allocation.' We learned it shortly after discovering fire. You seem to have done these in the opposite order."

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
4. **Transform earnest language** to bemused observations
5. **Preserve ALL humor** that already works
6. **Mark complete**: Update hash when done

## The Test

Before: "This will SAVE HUMANITY!"
After: "This is how every other species handles healthcare. We assumed you'd figured it out by now, given that you have smartphones."

The goal: Make readers laugh at humanity's obvious mistakes while gently showing them the solution, like teaching a very slow child to tie their shoes.

## Remember

**Good tone:** "You're the only species that spends more on dying than living. We checked. Even the Zorgons think that's weird, and they eat their young."

**Bad tone:** "We MUST redirect military spending to SAVE LIVES NOW!"

The facts stay the same. The delivery changes from evangelical preacher to confused alien kindergarten teacher.