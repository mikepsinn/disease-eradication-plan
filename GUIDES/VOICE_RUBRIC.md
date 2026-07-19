# Voice Rubric (data-driven)

Derived from **34,742 real before->after prose edits** mined from this repo's git
history (`scripts/voice/mine-voice-edits.py`), of which 240 were studied closely.

It complements `STYLE_GUIDE.md`. The style guide states the *principles*; this file
shows the *patterns the author actually applies*, with real examples, ranked by how
often they appear in the edit history.

**The headline finding:** the hand-written regex scanner (`scripts/voice-check.py`)
removes a banned term in only **1.4%** of these edits. The other **98.6%** are
semantic rewrites with no repeated find-replace (the single most-repeated swap in
34,742 edits occurs *twice*). The voice is **semantic, not lexical** — which is why
regex hooks plateau and why the fix is exemplar-driven critique, not more regexes.

Every example below is a verbatim (BEFORE -> AFTER) pair from the history.

---

## 1. Flat caption -> deadpan joke  (the single most common edit)

Image captions and descriptions get rewritten from neutral description into one
deadpan line that states the absurd truth flat. This is the dominant pattern.

- "A breakdown of the $162 billion in improper payments showing the 75% concentration in Medicare and Medicaid" -> "Three-quarters of government healthcare fraud happens in two programs. The private sector steals less, which is awkward."
- "Chart showing Type II errors (7.94B DALYs) vs Type I errors (2.59M DALYs) - a 3,070:1 ratio" -> "For every person saved by testing, 3,070 people die waiting for the test results. But at least we were careful."
- "A conceptual model illustrating three primary channels of political influence..." -> "Three ways to buy a politician: tell voters they're bad, give them a report card like they're in school, or promise them a nice job later. Democracy runs on deferred compensation."

**Rule:** never describe the image. State the one true, absurd thing it shows, flat.

## 2. Academic / abstract jargon -> concrete plain speech

Kills "Pareto improvement," "Coasean," "rent-seekers," "mechanism design contribution,"
"leverage," "stakeholder." Replaces with what it literally means.

- "Coasean buyouts via Incentive Alignment Bonds: compensating rent-seekers for transitioning away from dysfunction, making reform a Pareto improvement rather than a redistributive conflict." -> "You can't just take money from defense contractors and expect them to stay quiet... a deal where everyone wins rather than a fight where someone loses."
**Exemplar discipline:** curate by whether the AFTER is a line worth imitating, not by
"it was an edit." Git gives (worse -> better) pairs, but *better is not good*. Example
of a real edit that is a WEAK exemplar: "No separate alpha needed." -> "That premium is
already in the number." (the after is limp and vague — which number? — an improvement,
not a line to copy). The exemplar bank in `voice-exemplars.jsonl` is quality-judged for
this, not just mined.

## 3. Long compound sentence -> short staccato sentences

- "the core problem remains: a system that costs more per patient, takes 36x longer than proven alternatives, and produces less safety data" -> "the core problem remains. The system costs more per patient. It takes 36x longer than proven alternatives. It produces less safety data."

## 4. Cut: the pompous / grand opener

Sentences that announce importance get deleted outright.

- "Artificial Intelligence represents the most potent technological force of the 21st century." -> (deleted)
- "A functioning fusion grid by 2040 would decouple economic growth from carbon emissions, effectively solving climate change and creating quadrillions in long-term value." -> (deleted)

## 5. Cut: the self-aware aside / narrator admiring himself

Wishonia never comments on his own cleverness or on the act of narrating. The gap
dies the moment he sounds self-aware (STYLE_GUIDE: "if Wishonia sounds self-aware,
the comedy dies").

- "It's painful but brief, like a flu shot administered by someone who hates you." -> "It is brief."
- "This is the single most important insight about your species and I've been trying to communicate it for 4,297 years." -> (deleted)
- "I realize that distinction matters more to you than it does to me, since I'm not made of meat." -> (deleted)

## 6. Cut: defensive rigor that answers nobody

Preemptive defenses against imagined critics get cut (STYLE_GUIDE: "an unprompted
defense manufactures the objection it answers").

- "An economist reviewing the expected value calculations should find:" -> (deleted)
- "This section makes it concrete enough that skeptical economists stop rolling their eyes." -> (deleted)

## 7. Cut: redundant header / transition / scaffolding

- "## How to Talk About Not Dying Without Sounding Insane" -> (deleted)
- "## The Only Two Numbers That Matter" -> (deleted)

## 8. Add: the concrete absurd analogy as the closer

The opposite of cutting — a flat, absurd, accurate analogy gets *added* as the
landing.

- "...The spending ratio is 40:1 for death over life." -> "...If your house had forty arsonists and one firefighter, you would not describe your house as 'safe.' You would describe it as 'on fire.'"
- "...the global population votes using pairwise comparisons:" -> "No committee on Earth has ever looked at a list of 10,000 proposals and made a good decision. Committees are where good ideas go to die of old age. Instead, the global population votes using pairwise comparisons:"

## 9. The wrong adjective on the grave noun

- "fewer funerals" -> "fewer boring funerals"
- (death recategorized as tedium; the category error is the joke)

## 10. Hedge investment / outcome claims (securities honesty)

- "The 1% Treaty would generate [X] annually in perpetuity" -> "Upon successful ratification, the 1% Treaty could generate [X] annually in perpetuity"
- "would" -> "could"; "represents a unique opportunity" -> "may represent an exceptional opportunity"

## 11. Surface-specific: academic versions depersonalize

In `*-academic.qmd` files only, "you/we" becomes "society / one / the nation." The
MAIN book keeps "you." (Voice Map: match the surface.)

- "You can't fight 200,000 years of evolution. But you can hack it." -> "One cannot fight 200,000 years of evolution. But it can be hacked."

## 12. Re-aim contempt: blame the species, not the reader

(Added 2026-06 from a "de-contempt" audit of the book, not the original git mining.)
The voice mocks human folly, but the instant "you" *personally* gets blamed for a
*civilizational* failure, the reader feels scolded from above and bounces. Keep the
dark joke; move the blame from the individual to the species or the system. The test:
is the narrator standing *above* the reader, wagging a finger at them specifically?

- "you had the technology, you just chose not to use it" -> "the technology existed; nobody reached for it"
- "the price you pay for being too slow" -> "the price of humanity being too slow"
- "You've been delaying it for 75 years" -> "It's been delayed for 75 years now"
- "You're very good at circles" -> "The circle is undefeated"
- "demonstrating basic arithmetic skills" -> (cut)

**Rule:** the *species* committed the crime, not the reader holding the book. KEEP jokes
aimed at a target that isn't the reader (the FDA, the Pentagon) and warm
we're-all-idiots-together lines ("we invented cheese, which is genius"). FLAG only
second-person *personal* blame for a collective failure. This is **semantic** — do not
regex it (every legitimate "you" would trip); it is a punch-up / critic judgment call.

## 13. De-euphemize: name the real thing at full scale

The world launders its horrors into bloodless abstraction: "waste on weapons",
"defense spending", "casualties", "collateral damage", "mortality". Refuse the
laundered word. Name the literal thing at its full concrete scale, so the horror
and the absurdity are both undeniable. The euphemism is the enemy's framing.

- "waste on weapons" -> "the redundant capacity to kill everyone several times over"
- "defense spending" -> "the money spent on the ability to murder everyone"
- never soften "people died" to "lives lost" or "mortality"; it is already literal

**Rule:** generalizes "suffering first / disease as a villain" to everything the
world sanitizes. Semantic, not regex-able; a punch-up / critic judgment call.

## 14. Cut the medium-reference (a kind of self-aware aside)

Narrating the document's own structure is leakage of the editor's framing into the
prose. It is the same failure as #5 (self-aware aside), pointed at the page itself.

- "That is the product. The rest of this page is how the machine delivers it." -> "That is the product."
- Kill "this page", "this chapter", "this section", "below", "above", "as we'll see / as we saw". ("This manual / this book" in Wishonia's own voice is fine; "this page" is not.)

## 15. Engineer's mechanism -> the product's own name

The writer defaults to describing *how* the thing works internally (plumbing,
data structures, process steps) instead of *what it is called* and *what it does
for you*. Five sub-patterns, all the same failure: the engineer's view leaked
into the customer's brochure.

**a. Process label instead of the product's name.**
Use the thing's actual name, not a description of what it mechanically does.

- "The Budget Redirect" -> "The 1% Treaty" (the product has a name; use it)
- "task queue" -> "the decentralized TODO list for humanity" (the vivid name exists)
- "The Evidence Engine" -> "The Optimal Policy Generator and Optimal Budget Generator" (name the actual tools)

**b. Vague summary where a specific number exists.**
If the number is known, print the number. A summary word is a euphemism for the
fact you already have.

- "negligible" -> "1 in 30 million"
- "significant savings" -> "$4,200 per person per year"
- "a large number of diseases" -> "7,000 diseases"

**c. Half the value proposition.**
The product does two things (health AND wealth, or lifespan AND income). State
both. The writer picks whichever half they find more dramatic and drops the
other. The reader needs both to act.

- "what kills you first" -> "what makes you poorer and deader"
- "curing diseases" -> "curing diseases and making you richer"
- "lives saved" -> "lives saved and income gained"

**d. Startup/product framing instead of the pitchman voice.**
"Our flagship feature," "How It Works," "The good news:" are startup pitch-deck
framing. The pitchman shows you the product; he does not narrate the pitch.

- "Our flagship feature: knowing where the trillions went." -> (cut the label; say what it does)
- "Now watch what happens when you wire them together:" -> (cut; the loop speaks for itself)
- "The good news:" -> (cut; state the fact)

**e. The corporate verb instead of the specific verb.**
"Redirect," "leverage," "utilize," "facilitate" describe a category of action.
Use the verb that says what actually happens.

- "redirect lobbying" -> "hand the lobbyists an optimal budget calculated to maximize health and wealth"
- "redirect 1%" -> "move 1% of every nation's weapons budget to clinical trials"
- "utilize the existing infrastructure" -> "use the lobbying machine you already built"

**Rule:** if the thing has a name, use the name. If the number exists, print the
number. If the product does two things, say both. If a startup would say it that
way, say it the other way.

---

## How to use this

When writing or punching up book prose: read this file, pull the most relevant
exemplars (`scripts/voice/voice-exemplars.jsonl`), and for each passage ask the
two questions the data answers: **"which of these 15 edits would the author make
here?"** and **"is any sentence here a caption, a pompous opener, a self-aware
aside, a defensive preempt, or an engineer's description of the product?"** If
yes, apply edit 1/4/5/6/15. The critic (`scripts/voice/voice-critic.py`) does
this automatically.
