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
>    small proven set delivered faster). Never "diseases we already know how to treat"
>    or "curable diseases."
> 3. **Build, not back.** The reader BUILDS these institutions; they do not exist.
>    Never "support / vote for / trust our thing."
> 4. **The number is the joke, and magnitude is persuasion.** State the absurd literal
>    truth WITH the figure. "Costs almost nothing" is a lie when the price is negative;
>    say what it pays. When the real number is STAGGERING, show it ($14.9T/year in
>    disease, 13% of GDP); never abstract it into a tidy phrase ("buying assets rather
>    than burning cash" hid a $26T/year drain).
> 5. **Write to the real reader.** Check each line's hidden premise against the
>    chapter's `audience`; do not assume the reader already knows/wants/has-done.
>
> Hard bans (the love line verbatim; securities words "guaranteed / risk-free / will
> return / safe"; em-dashes) are in the style guide and the commit scanner.

## The greatness critic FAILS

On top of "clear but flat": euphemism (war / safety / spending / winds-down), a vague
claim or tidy abstraction where a specific or staggering real number exists, contentless filler ("that is the product"),
a premise untrue for the chapter's reader, and **any new line that does not beat the
book's existing best version of the same point.**
