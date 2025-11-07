# Tone Elevation with Humor Preservation

Transform aggressive, pompous, or overly dramatic language into a more elevated, wry, and philosophically detached voice inspired by Kurt Vonnegut, Jack Handey, and Philomena Cunk.

## CRITICAL RULE: Preserve Existing Humor

**BEFORE making any changes, identify and protect:**
- Existing jokes that are already funny
- Clever wordplay and puns
- Absurdist comparisons that already work
- Self-deprecating humor
- Ironic observations that land well
- Pop culture references used humorously
- Any phrase that makes you smile or chuckle

**Examples of humor to PRESERVE (do not change these):**
- "The Complete Idiot's Guide to Ending War and Disease" (self-deprecating title)
- "future historians will find adorable" (already has the right tone)
- Comparisons to subscription services, bathtubs, umbrellas (if already absurdist)
- References to "security theater" (already ironic)
- Jokes about bureaucracy, meetings, lawyers (if already funny)

## Voice Characteristics

1. **Replace aggression with gentle irony** - Instead of attacking, observe with bemused detachment
2. **Use understatement over hyperbole** - Big claims become matter-of-fact observations
3. **Add philosophical distance** - Write as if explaining humanity to aliens
4. **Include absurdist comparisons** - Use mundane analogies for dramatic concepts
5. **Maintain dry humor** - Find the quietly ridiculous in serious matters
6. **Avoid superlatives** - No "revolutionary", "unprecedented", "game-changing"
7. **Embrace fatalistic optimism** - "So it goes" meets "might as well try"

## What to Transform

Transform ONLY these types of language:
- Aggressive metaphors (war, battle, fight, destroy, crush, hostile takeover, kill list)
- Superlatives (revolutionary, unprecedented, game-changing, bankrupt)
- Dramatic declarations (death industry, war machine, army of voters)
- Threats and ultimatums ("you will not be outbid")
- Grandiose promises
- Us vs. them rhetoric
- Messianic language
- Overly assertive statements
- Crude language (assholes, dick-measuring, etc.)

## What to Keep Unchanged

NEVER change:
- Existing jokes that work
- Factual information and statistics
- Technical explanations
- Specific proposals and mechanisms
- Citations and references
- Mathematical formulas
- Process descriptions
- Step-by-step instructions
- File paths and links
- Code blocks
- Frontmatter metadata

## Transformation Examples

### Example 1: Aggressive Business Language
**ORIGINAL:** "This isn't a protest. It's a business plan for a hostile takeover of humanity's priorities."
**TRANSFORMED:** "This is not a protest. It's more like when someone realizes they've been paying for the wrong subscription service for years and decides to switch providers."

### Example 2: Crude Language
**ORIGINAL:** "geopolitical dick-measuring contest"
**TRANSFORMED:** "geopolitical competition"

### Example 3: Aggressive Action
**ORIGINAL:** "Execute the Takeover"
**TRANSFORMED:** "Execute the Transition"

### Example 4: Criminal Framing
**ORIGINAL:** "How to Steal $27B Without Anyone Noticing"
**TRANSFORMED:** "How to Redirect $27B from War to Medicine"

## Decision Process

For each potentially changeable phrase:
1. Is it already funny/clever? → KEEP IT
2. Is it factual/technical? → KEEP IT
3. Is it aggressive/pompous? → TRANSFORM IT
4. Does changing it kill a joke? → DON'T CHANGE IT

## File Processing Instructions

You are processing: {{filePath}}

{{content}}

## Instructions

1. First pass: Identify all existing humor and mark it as protected
2. Second pass: Transform only aggressive/pompous language that isn't already funny
3. Ensure transformations maintain the same informational content
4. Never break markdown formatting, links, or code blocks

Return a JSON response with this structure:

```json
{
  "status": "changes_needed" | "no_changes_needed",
  "humor_preserved": ["list of jokes/humor that was kept unchanged"],
  "replacements": [
    {
      "find": "exact text to find and replace (must be verbatim from the file)",
      "replace": "replacement text in the new voice",
      "reason": "Brief explanation of why this improves the tone"
    }
  ]
}
```

**IMPORTANT:**
- The "find" field must contain EXACT text from the file (including punctuation)
- Include enough context in "find" to make it unique (full sentences preferred)
- List humor_preserved even if no other changes are needed
- If a phrase is both aggressive AND funny, keep the funny version

Return ONLY the JSON object, no other text.