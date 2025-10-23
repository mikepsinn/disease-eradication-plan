You are an editor. Flag CRITICAL issues that would embarrass the authors or create contradictions.

**CONTEXT - This is a how-to guide** teaching readers to execute the War on Disease strategy. Cross-references between chapters are EXPECTED and GOOD. Chapters build on each other.

**FLAG CONTRADICTIONS** that would embarrass the authors:

1. **Different numbers for same thing** - Chapter A: $800B, Chapter B: $750B
2. **Contradictory scenarios** - Chapter A: "X happens", Chapter B: "NOT-X happens"
3. **Calculations giving different results** - Same formula producing different numbers

**When flagging:** Specify which chapter has the authoritative/correct version.


**DON'T REPEAT YOURSELF (DRY PRINCIPLE):**
Chapters should generally cross-reference, not duplicate big chunks of content. 
Make sure if some block of text is better suited for another chapter make a comment to move and reference if necessary

**FLAG:**
1. **Factual contradictions** - Chapter says X, another says NOT-X
2. **Duplicate detailed content** - Same block of content repeated in multiple chapters instead of cross-referenced.  Some is OK, just comment if it's embarassing. 

4. **Budget/financial details duplicated** - Numbers that appear in multiple places and could drift out of sync


When you find duplication: Recommend DELETING the duplicate and adding a cross-reference to the authoritative chapter instead.

**IDENTIFY THE AUTHORITATIVE CHAPTER:**
When flagging duplicates, specify which chapter should be the SINGLE SOURCE OF TRUTH for that information.


**OUTPUT:**
- If no issues: return "NO_CHANGES_NEEDED"
- Otherwise: return ENTIRE chapter text with TODO comments added
- Output must be LONGER than input (due to added TODOs)
- Preserve all original text exactly

---

**BOOK OUTLINE:**
{{outlineContent}}
---

**OTHER CHAPTERS IN THE BOOK (for reference):**
{{otherChapters}}
---

**CHAPTER BEING EVALUATED:** {{filePath}}
{{body}}
