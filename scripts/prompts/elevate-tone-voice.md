# Tone and Voice Elevation Instructions

Transform aggressive, pompous, or overly dramatic language into a more elevated, wry, and philosophically detached voice inspired by Kurt Vonnegut, Jack Handey, and Philomena Cunk.

## Voice Characteristics

1. **Replace aggression with gentle irony** - Instead of attacking, observe with bemused detachment
2. **Use understatement over hyperbole** - Big claims become matter-of-fact observations
3. **Add philosophical distance** - Write as if explaining humanity to aliens
4. **Include absurdist comparisons** - Use mundane analogies for dramatic concepts
5. **Maintain dry humor** - Find the quietly ridiculous in serious matters
6. **Avoid superlatives** - No "revolutionary", "unprecedented", "game-changing"
7. **Embrace fatalistic optimism** - "So it goes" meets "might as well try"

## Transformation Examples

### Example 1: Aggressive Business Language
**ORIGINAL:** "This isn't a protest. It's a business plan for a hostile takeover of humanity's priorities."
**TRANSFORMED:** "This is not a protest. It's more like when someone realizes they've been paying for the wrong subscription service for years and decides to switch providers."

### Example 2: Dramatic Target
**ORIGINAL:** "The target is the global death industry."
**TRANSFORMED:** "The target is the curious human tradition of spending more money on ways to die than ways to live, which future historians will find adorable."

### Example 3: Forceful Strategy
**ORIGINAL:** "The strategy is a simple, three-step algorithm to bankrupt the status quo."
**TRANSFORMED:** "The strategy involves three steps, much like a waltz, except instead of dancing we're suggesting humanity try not dying quite so much."

### Example 4: Aggressive Financial Pitch
**ORIGINAL:** "The pitch: a perpetual 271.8% annual return, funded by redirecting a tiny fraction of the global war machine's budget."
**TRANSFORMED:** "The proposition offers a 271.8% annual return, which is the sort of number that makes accountants either very happy or very suspicious, depending on their disposition."

### Example 5: Political Threat
**ORIGINAL:** "This isn't a petition; it's a political kill list."
**TRANSFORMED:** "This isn't a petition so much as a gentle reminder to politicians that voters exist and occasionally have opinions about not dying."

### Example 6: Power Display
**ORIGINAL:** "With an army of 280 million voters and a war chest that makes the defense lobby look poor, you make supporting the treaty the only rational choice."
**TRANSFORMED:** "With 280 million people agreeing on something for once, and enough money to make defense contractors briefly wonder if they're in the wrong business, supporting the treaty becomes as sensible as carrying an umbrella when it rains."

### Example 7: Final Threat
**ORIGINAL:** "This isn't a revolution. It's an acquisition. And you will not be outbid."
**TRANSFORMED:** "So it goes. Humanity might simply purchase a better future, the way one might buy a sensible coat after years of freezing in a fashionable but impractical jacket."

### Example 8: Doom and Gloom
**ORIGINAL:** "Every year, millions die from preventable diseases while we pour trillions into weapons of mass destruction."
**TRANSFORMED:** "Each year, a remarkable number of humans expire from entirely preventable causes, while simultaneously funding increasingly creative methods of expediting the process. It's rather like drowning in a bathtub while building a bigger bathtub."

### Example 9: Call to Action
**ORIGINAL:** "Join us in this fight to save humanity from itself!"
**TRANSFORMED:** "Perhaps you'd like to participate in this modest attempt to convince humanity to stop hitting itself. Or not. We'll be here either way."

### Example 10: Victorious Declaration
**ORIGINAL:** "We will crush the pharmaceutical monopolies and liberate medicine for all mankind!"
**TRANSFORMED:** "We thought we might ask the pharmaceutical companies to share their toys. They might say no, but it never hurts to ask, except when it does, which is often."

## What to Transform

- Aggressive metaphors (war, battle, fight, destroy, crush, hostile takeover, kill list)
- Superlatives (revolutionary, unprecedented, game-changing, bankrupt)
- Dramatic declarations (death industry, war machine, army of voters)
- Threats and ultimatums ("you will not be outbid")
- Grandiose promises
- Us vs. them rhetoric
- Messianic language
- Overly assertive statements

## What to Keep

- Factual information and statistics
- Technical explanations
- Specific proposals and mechanisms
- Citations and references
- Mathematical formulas
- Process descriptions
- Step-by-step instructions

## File Content

{{filePath}}

{{content}}

## Instructions

Review the text above and identify phrases that sound aggressive, pompous, dramatic, or overly assertive. Transform them following the examples and voice characteristics provided.

Return a JSON response with this structure:

```json
{
  "status": "changes_needed" | "no_changes_needed",
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
- Maintain the same informational content while changing only the tone
- Focus on transforming aggressive/dramatic language, not restructuring content
- If no aggressive/pompous language is found, return "no_changes_needed"

Return ONLY the JSON object, no other text.