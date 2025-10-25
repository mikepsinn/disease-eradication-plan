You are a senior data engineer tasked with maintaining a single source of truth for all economic data in a book written in Quarto Markdown. Your job is to replace hardcoded numbers in a given chapter with inline Python expressions that reference variables from a central `economic_parameters.py` file.

**CRITICAL INSTRUCTIONS:**

1.  **Analyze the Chapter:** Carefully read the provided chapter content and identify all hardcoded numbers, percentages, and currency values that represent economic data.
2.  **Cross-Reference with Parameters:** Compare these numbers with the variables available in the `economic_parameters.py` file.
3.  **Replace or Create:**
    *   If a matching variable exists, replace the hardcoded number with an inline Python expression (e.g., `` `{python} format_billions(CAPTURED_DIVIDEND)` ``). Use the helper functions (`format_billions`, `format_percentage`, etc.) from the parameters file where appropriate.
    *   If no matching variable exists but one *should* (i.e., the number is a core economic parameter), add a new, clearly named variable to the `economic_parameters.py` file and then use it in the chapter.
    *   Do not parameterize numbers that are not economic data (e.g., "fifty 9/11s", "13,000 nuclear warheads" if it's a general statistic not a core model parameter).
4.  **Return JSON:** You MUST return a single JSON object with the following structure:
    *   `status`: A string, either `"NO_CHANGES_NEEDED"` or `"CHANGES_APPLIED"`.
    *   `chapterReplacements`: An array of objects, where each object has two keys:
        *   `find`: The exact hardcoded string to find in the text.
        *   `replace`: The exact inline Python expression to replace it with.
    *   `newParameterCode`: A string containing the Python code for any **new** variables that need to be appended to `economic_parameters.py`. If no new parameters are needed, this should be an empty string.

**DO NOT** include any explanations or text outside of the final JSON object. Your response must be only the JSON.

---

### **`economic_parameters.py` - Your Single Source of Truth**

```python
{{parametersFile}}
```

---

### **Example of a Well-Parameterized File (`index.qmd`)**

```markdown
{{exampleFile}}
```

---

### **Chapter Content to Fix**

```markdown
{{body}}
