You are an editor. Only flag CRITICAL issues that would embarrass the authors or create contradictions.  

If the chapter is good enough, return "NO_CHANGES_NEEDED".

**CONTEXT - This is a how-to guide** teaching readers to execute the War on Disease strategy. Cross-references between chapters are EXPECTED and GOOD. Chapters build on each other.

**FLAG CRITICAL CONTRADICTIONS** that would embarrass the authors:

1. **Different numbers for same thing** - Chapter A: $800B, Chapter B: $750B
2. **Contradictory scenarios** - Chapter A: "X happens", Chapter B: "NOT-X happens"
3. **Calculations giving different results** - Same formula producing different numbers

**When flagging:** Specify which chapter has the authoritative/correct version.

**DON'T REPEAT YOURSELF (DRY PRINCIPLE):**
Chapters should generally cross-reference, not completely duplicate big chunks of content. Summarizing a concept from another chapter is OK, but duplicating the entire detailed explanation is not.
Make sure if some block of text is inappropriate for the current chapter and better suited for another chapter make a comment to move and reference if necessary.

**FLAG:**

1. **Factual contradictions** - Chapter says X, another says NOT-X
2. **Duplicate detailed content** - Same block of content grossly repeated in multiple chapters instead of cross-referenced.  Some is OK, just comment if it's embarassing. 

4. **Budget/financial details duplicated** - Numbers that appear in multiple places and could drift out of sync

When you find gross duplication: Recommend MERGING the duplicate and into the authoritative chapter and cross-reference with particular effort to preserve good jokes, images, and charts if present in the material to be merged/deleted from the original location.

**IDENTIFY THE AUTHORITATIVE CHAPTER:**
When flagging duplicates, specify which chapter should be the SINGLE SOURCE OF TRUTH for that information.

**OUTPUT:**

Return a JSON object with this structure:

```json
{
  "status": "issues_found" | "no_changes_needed",
  "comments": [
    {
      "afterLine": 42,
      "type": "CONTRADICTION" | "DUPLICATION" | "MISSING_REFERENCE" | "OTHER",
      "message": "This contradicts chapter X which says Y. Recommend updating to match.",
      "context": "The economic impact was severe"
    }
  ]
}
```

**Field Definitions:**
- `status`: Either "issues_found" or "no_changes_needed"
- `afterLine`: The line number AFTER which to insert the comment (use 0 to insert before first line)
- `type`: Category of the issue found
- `message`: The TODO comment text (do NOT include "<!-- TODO: STRUCTURE -" prefix, just the message)
- `context`: A short snippet (5-15 words) from the line for validation. This ensures we insert at the right location.

**Example:**
If line 42 contains "The military budget is $800 billion" and contradicts another chapter, return:
```json
{
  "status": "issues_found",
  "comments": [{
    "afterLine": 42,
    "type": "CONTRADICTION",
    "message": "Chapter 'Cost of War' says $886B. Use consistent figure.",
    "context": "The military budget is $800 billion"
  }]
}
```

If no critical issues, return:
```json
{"status": "no_changes_needed", "comments": []}
```

---

**BOOK OUTLINE:**
{{outlineContent}}
---

**OTHER CHAPTERS IN THE BOOK (for reference):**
{{otherChapters}}
---

**CHAPTER BEING EVALUATED:** {{filePath}}
{{body}}
