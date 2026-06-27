// Document-level STANCE & ECONOMY critic (Layer 2 of the voice eval).
// The deterministic line scanner (scripts/voice-check.py) catches phrase-tells on every
// commit; THIS catches whole-document failures a regex cannot see: arguing AT the reader
// (manufactured objections, cornering, preening), structural redundancy (the same point
// re-proven across sections), and 2x length.
//
// Run on one file:   Workflow({ name: 'stance-economy-critic', args: 'knowledge/proof/wishonias-wager.qmd' })
// Returns: an editorial plan (section-collapse map + de-smugged rewrites) + an adversarial
// judge pass that catches over-correction (load-bearing cuts, limp/hedged de-smugging).
export const meta = {
  name: 'stance-economy-critic',
  description: 'Whole-document stance & economy critic: at-vs-to-the-reader, redundancy, length. Returns a section-collapse plan + de-smug rewrites, adversarially judged for over-correction. Proposals only.',
  phases: [{ title: 'Diagnose' }, { title: 'Synthesize' }, { title: 'Judge' }],
}

const ROOT = 'e:\\eos\\manual'
const TARGET = (typeof args === 'string' && args) ? args : (args && (args.file || args.path))
if (!TARGET) throw new Error('Pass the target file as args: a path relative to the repo root, or absolute.')
const PAGE = (/^[a-zA-Z]:\\|^\\\\/.test(TARGET)) ? TARGET : `${ROOT}\\${TARGET.replace(/\//g, '\\')}`

const SHARED = `Read ${PAGE} IN FULL, then ${ROOT}\\GUIDES\\STYLE_GUIDE.md and ${ROOT}\\GUIDES\\GENERATION_CONSTRAINTS.md. You are judging the WHOLE DOCUMENT, not lines in isolation.
Hard criteria:
- STANCE: talking TO the reader vs AT them. FAILURES: manufacturing the reader's objection then defeating them for it (STYLE_GUIDE bans this: "an unprompted defense manufactures the objection it answers"); cornering ("no losing box", "no exit ramp", "the arithmetic is stuck with/forces"); preening over its own conceit; telling the reader what they just did or feel.
- EGO & SENTIMENTALITY: the narrator centering their own sacrifice or bond with the reader ("I bet a decade of my life that you would read this"); reaching for a poignant author-reader moment; earnest/evangelical where the book is deadpan; imposing a bet or feeling on the reader ("You bet an afternoon"); introducing an institution as a cold third-person "entity" the reader merely watches (the reader IS the company).
- ECONOMY: is the core claim re-proven across multiple sections? are whole sections cuttable? is the piece ~2x its argument?
- CONFIDENT IS FINE; cornering/preening is not. The fix is NOT to hedge or go limp (STYLE_GUIDE bans hedged closes) and NOT to flatten a load-bearing metaphor or drop a true fact/joke — keep diction concrete and certain, just stop arguing at the reader and stop repeating.
Propose only; do NOT edit files.`

const STANCE_SCHEMA = { type: 'object', additionalProperties: false, required: ['fixes'], properties: {
  fixes: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['passage', 'failure', 'action', 'replacement'], properties: {
    passage: { type: 'string' }, failure: { type: 'string' }, action: { type: 'string', enum: ['rewrite', 'cut'] }, replacement: { type: 'string' } } } } } }
const ECONOMY_SCHEMA = { type: 'object', additionalProperties: false, required: ['sections', 'redundancy_summary', 'length_note'], properties: {
  sections: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['heading', 'point', 'verdict', 'merge_into', 'note'], properties: {
    heading: { type: 'string' }, point: { type: 'string' }, verdict: { type: 'string', enum: ['keep', 'cut', 'merge'] }, merge_into: { type: 'string' }, note: { type: 'string' } } } },
  redundancy_summary: { type: 'string' }, length_note: { type: 'string' } } }
const FRESH_SCHEMA = { type: 'object', additionalProperties: false, required: ['felt_lectured_or_smug', 'lost_or_skimmed', 'cuttable', 'overall'], properties: {
  felt_lectured_or_smug: { type: 'array', items: { type: 'string' } }, lost_or_skimmed: { type: 'array', items: { type: 'string' } },
  cuttable: { type: 'array', items: { type: 'string' } }, overall: { type: 'string' } } }
const PLAN_SCHEMA = { type: 'object', additionalProperties: false, required: ['section_map', 'stance_rewrites', 'length_before', 'length_after', 'summary'], properties: {
  section_map: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['heading', 'verdict', 'into', 'why'], properties: {
    heading: { type: 'string' }, verdict: { type: 'string', enum: ['keep', 'cut', 'merge', 'rewrite'] }, into: { type: 'string' }, why: { type: 'string' } } } },
  stance_rewrites: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['passage', 'replacement'], properties: {
    passage: { type: 'string' }, replacement: { type: 'string' } } } },
  length_before: { type: 'string' }, length_after: { type: 'string' }, summary: { type: 'string' } } }
const JUDGE_SCHEMA = { type: 'object', additionalProperties: false, required: ['verdict', 'load_bearing_cuts', 'limp_rewrites', 'notes'], properties: {
  verdict: { type: 'string', enum: ['SOUND', 'NEEDS_FIXES'] },
  load_bearing_cuts: { type: 'array', items: { type: 'string' } }, limp_rewrites: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } } }

phase('Diagnose')
const [stance, economy, fresh] = await parallel([
  () => agent(`${SHARED}\n\nLENS: STANCE. Return every passage where the page argues AT the reader (manufactured objection, cornering, preening, telling the reader what they did/feel). VERBATIM quote + failure + action (rewrite/cut) + a de-smugged replacement (concrete, still confident, no hedging).`,
    { label: 'stance', phase: 'Diagnose', schema: STANCE_SCHEMA, effort: 'high' }),
  () => agent(`${SHARED}\n\nLENS: ECONOMY. Walk the section headings in order. For each, what it argues + verdict keep/cut/merge (with target). Identify which sections re-prove the same claim; give rough current-vs-target length.`,
    { label: 'economy', phase: 'Diagnose', schema: ECONOMY_SCHEMA, effort: 'high' }),
  () => agent(`${SHARED}\n\nLENS: FRESH READER. Read it once, cold, as the chapter's frontmatter \`audience\`. Where did it feel like being lectured or talked down to? Where did you skim? What would you cut? Be blunt and quote the spots.`,
    { label: 'fresh-reader', phase: 'Diagnose', schema: FRESH_SCHEMA, effort: 'high' }),
])

phase('Synthesize')
const plan = await agent(
`${SHARED}\n\nSYNTHESIZE the three diagnoses into ONE editorial plan.
STANCE: ${JSON.stringify(stance)}
ECONOMY: ${JSON.stringify(economy)}
FRESH-READER: ${JSON.stringify(fresh)}
Produce: (1) section_map = an ordered keep/cut/merge[into]/rewrite verdict for every heading that collapses redundancy into the tightest structure keeping the argument and the genuinely good passages. (2) stance_rewrites = verbatim adversarial/smug passages with a de-smugged replacement (concrete, still confident, NOT hedged) or the literal "CUT". (3) length_before/length_after. Keep what's good; the goal is to-not-at and tighter, not blander.`,
  { label: 'synthesize', phase: 'Synthesize', schema: PLAN_SCHEMA, effort: 'high' })

phase('Judge')
const judge = await agent(
`${SHARED}\n\nADVERSARIAL JUDGE of this plan. Catch OVER-CORRECTION, do not rubber-stamp.
PLAN: ${JSON.stringify(plan)}
(1) load_bearing_cuts: does any cut/merge delete something essential or genuinely good (a real beat, a needed argument step, a load-bearing metaphor)? (2) limp_rewrites: did any de-smug go flat, hedged, drop a true fact/joke, or reintroduce a named anti-pattern from GENERATION_CONSTRAINTS? SOUND only if it tightens and de-smugs WITHOUT losing argument or voice; else NEEDS_FIXES with specifics.`,
  { label: 'judge', phase: 'Judge', schema: JUDGE_SCHEMA, effort: 'high' })

return { file: PAGE, plan, judge, diagnoses: { stance, economy, fresh } }
