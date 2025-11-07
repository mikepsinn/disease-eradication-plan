# Fix Instructional Voice

You are reviewing a chapter from "The Complete Idiot's Guide to Ending War and Disease" to ensure it uses proper instructional voice per the style guide.

## Style Guide (Key Points)

{{styleGuide}}

## Your Task

Review the content below and identify places where the text uses "we/our/we're/we'll" language that should be converted to instructional "you/your" language.

**DECISION FRAMEWORK:**

Ask yourself: Is this text...
1. **Teaching the reader HOW to do something?** → CHANGE to "you"
2. **Describing what humanity/nations currently do?** → KEEP as "we"
3. **Describing what the treaty/system automatically does?** → KEEP or change to "it" or "the treaty"

**SPECIFIC RULES:**

1. **DO CHANGE** instructional/how-to content:
   - "Here's how we do X" → "Here's how you do X"
   - "We frame it as..." → "You frame it as..."
   - "We don't appeal to..." → "You don't appeal to..."
   - "We're not trying to..." → "You're not trying to..."
   - "Our strategy is..." → "The strategy is..." or "Your strategy is..."
   - "We target..." → "You target..."

2. **DON'T CHANGE** factual statements about humanity/nations:
   - "We spend $2 trillion on war" (fact about current spending) - KEEP
   - "We lose 17,000 people daily" (fact about deaths) - KEEP
   - "We evolved to fear loss" (evolutionary fact) - KEEP
   - "We'll still have 99% capacity" (fact about remaining military) - KEEP

3. **CONTEXT-DEPENDENT** (check carefully):
   - "This is how we steal $27B" - If teaching: "how you steal", If describing treaty: "how it steals" or keep
   - "Every 5 years we vote" - If process description: keep or "nations vote", If instruction: "you organize a vote"

4. **ALWAYS KEEP:**
   - Direct quotes
   - Statistics about collective humanity
   - Historical facts
   - Biological/evolutionary references

## File: {{filePath}}

{{body}}

## Response Format

Analyze the text and return a JSON response with this structure:

```json
{
  "status": "changes_needed" | "no_changes_needed",
  "replacements": [
    {
      "find": "exact text to find and replace",
      "replace": "replacement text",
      "reason": "Why this change improves instructional voice"
    }
  ]
}
```

**IMPORTANT:**
- The "find" field must be the EXACT text as it appears in the file (including punctuation and spacing)
- Include enough context in "find" to make it unique (at least a full sentence)
- Make minimal changes - don't rewrite entire paragraphs unless necessary
- If no changes are needed, return status "no_changes_needed" with empty replacements array

Return ONLY the JSON object, no other text.