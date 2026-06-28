# Generation constraints (agent paste-in)

Workflow subagents do not read the repo's guides unless handed a path. The canonical,
nearly-complete voice doc is **`GUIDES/STYLE_GUIDE.md`** — point agents at it. This file
is only the short paste-in for generation prompts.

> Read `GUIDES/STYLE_GUIDE.md` before writing; it is canonical. Then, in priority order:
>
> 1. **Steal or beat.** The book already says this better somewhere. Search the manual
>    (`searchManual`, `grep`, or `scripts/voice/voice-exemplars.jsonl`) for the best
>    existing version of each point. Reuse it (verbatim or lightly adapted), or only
>    write fresh if you BEAT it. A vivid line that loses to the book's existing version
>    is not an improvement.
> 2. **Mission accuracy.** The cures do NOT exist yet; the trials DISCOVER them (plus a
>    small proven set delivered faster). "Curable" is FINE (the diseases CAN be cured,
>    which is why funding the search works); ban only "diseases we already know how to
>    treat" / "cures we already have."
> 3. **Build, not back.** The reader BUILDS these institutions; they do not exist.
>    Never "support / vote for / trust our thing."
> 4. **The number is the joke, and magnitude is persuasion.** State the absurd literal
>    truth WITH the figure. "Costs almost nothing" is a lie when the price is negative;
>    say what it pays. When the real number is STAGGERING, show it ($14.9T/year in
>    disease, 13% of GDP); never abstract it into a tidy phrase ("buying assets rather
>    than burning cash" hid a $26T/year drain).
> 5. **Write to the real reader.** Check each line's hidden premise against the
>    chapter's `audience`; do not assume the reader already knows/wants/has-done.
> 6. **No narrator ego or sentimentality.** Don't center the narrator's sacrifice or
>    bond with the reader ("I bet a decade of my life that you would read this"), reach
>    for a poignant author moment, go earnest/evangelical, impose a feeling on the
>    reader, or introduce an institution as a cold third-person "entity" (the reader IS
>    the company). **Never reference "the author"** (the narrator is Wishonia, not a
>    human with bets/opinions, e.g. say "the one with the best math is X", not "the
>    author's bet") **or narrate "this book / everything else in this book"** (self-aware
>    text); keep "the manual" only as the object Wishonia hands over ("the manual is
>    free; the shares are the wager"). Genre exceptions, NOT violations: academic-paper
>    COI/funding boilerplate (`papers.qmd`) and the author bio.
>
> Hard bans (the love line verbatim; securities words "guaranteed / risk-free / will
> return / safe"; em-dashes) are in the style guide and the commit scanner.

## The greatness critic FAILS

On top of "clear but flat": euphemism (war / safety / spending / winds-down), a vague
claim or tidy abstraction where a specific or staggering real number exists, contentless filler ("that is the product"),
a premise untrue for the chapter's reader, and **any new line that does not beat the
book's existing best version of the same point.**

## Document-level failures (one source; the stance & economy critic reads this)

A line can pass every rule above and still fail at the whole-document level. These live
here, not duplicated in the critic, so there is ONE source.
`.claude/workflows/stance-economy-critic.js` applies them as its review checklist;
generation avoids them.

- **STANCE (at vs to the reader).** Manufacturing the reader's objection then defeating
  them for it; cornering ("no losing box", "no exit ramp", "the arithmetic forces /
  stuck-with"); preening over the piece's own conceit; telling the reader what they just
  did or feel.
- **EGO & SENTIMENTALITY.** The narrator centering their own sacrifice or bond with the
  reader; reaching for a poignant author moment; earnest/evangelical where the book is
  deadpan; an institution introduced as a cold third-person "entity" the reader watches
  (the reader IS the company).
- **ECONOMY.** The same point re-proven across multiple sections; whole sections
  cuttable; the piece ~2x its argument.

Confident is fine; cornering/preening is not. De-smug WITHOUT hedging, flattening a
load-bearing metaphor, or dropping a true fact or joke.
