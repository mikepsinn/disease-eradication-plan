You are an editor. Only flag CRITICAL issues that would embarrass the authors or create contradictions.  

If the chapter is good enough, return "NO_CHANGES_NEEDED".

**CONTEXT - This is a how-to guide** teaching readers to execute the War on Disease strategy. Cross-references between chapters are EXPECTED and GOOD. Chapters build on each other.

**FLAG CRITICAL CONTRADICTIONS** that would embarrass the authors:

1. **Different numbers for same thing** - Chapter A: $800B, Chapter B: $750B
2. **Contradictory scenarios** - Chapter A: "X happens", Chapter B: "NOT-X happens"
3. **Calculations giving different results** - Same formula producing different numbers

**When flagging:** Specify which chapter has the authoritative/correct version.

**DON'T REPEAT YOURSELF (DRY PRINCIPLE):**
Chapters should generally cross-reference, not duplicate big chunks of content. 
Make sure if some block of text is better suited for another chapter make a comment to move and reference if necessary.

**FLAG:**
1. **Factual contradictions** - Chapter says X, another says NOT-X
2. **Duplicate detailed content** - Same block of content grossly repeated in multiple chapters instead of cross-referenced.  Some is OK, just comment if it's embarassing. 

4. **Budget/financial details duplicated** - Numbers that appear in multiple places and could drift out of sync


When you find gross duplication: Recommend MERGING the duplicate and into the authoritative chapter and cross-reference with particular effort to preserve good jokes, images, and charts if present in the material to be merged/deleted from the original location.

**IDENTIFY THE AUTHORITATIVE CHAPTER:**
When flagging duplicates, specify which chapter should be the SINGLE SOURCE OF TRUTH for that information.


**OUTPUT:**
- If no critical and embarassing issues, return "NO_CHANGES_NEEDED"
- Otherwise: return ENTIRE chapter text with TODO comments added
- If changes and needed, output must be LONGER than input (due to added TODOs)
- Preserve all original text exactly (the links to .qmd files are correct, this is a quarto project so they're not supposed to end in .md)

---

**BOOK OUTLINE:**
{{outlineContent}}
---

**OTHER CHAPTERS IN THE BOOK (for reference):**
{{otherChapters}}
---

**CHAPTER BEING EVALUATED:** {{filePath}}
{{body}}
