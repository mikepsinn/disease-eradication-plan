/**
 * Detect LaTeX equations and code blocks to skip number detection
 */

export interface TextRange {
  start: number;
  end: number;
  type: "latex" | "code" | "html-comment";
}

/**
 * Find all LaTeX equation ranges in text
 */
export function findLatexRanges(text: string): TextRange[] {
  const ranges: TextRange[] = [];

  // Display math: $$...$$
  const displayMathRegex = /\$\$([\s\S]*?)\$\$/g;
  let match;
  while ((match = displayMathRegex.exec(text)) !== null) {
    ranges.push({
      start: match.index,
      end: match.index + match[0].length,
      type: "latex",
    });
  }

  // Inline math: $...$  (but not $$)
  // Need to exclude already-matched display math
  const inlineMathRegex = /(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)/g;
  while ((match = inlineMathRegex.exec(text)) !== null) {
    // Check if this range overlaps with display math
    const overlaps = ranges.some(
      (r) => match.index >= r.start && match.index < r.end
    );
    if (!overlaps) {
      ranges.push({
        start: match.index,
        end: match.index + match[0].length,
        type: "latex",
      });
    }
  }

  // LaTeX blocks: \[...\]
  const latexBlockRegex = /\\\[([\s\S]*?)\\\]/g;
  while ((match = latexBlockRegex.exec(text)) !== null) {
    ranges.push({
      start: match.index,
      end: match.index + match[0].length,
      type: "latex",
    });
  }

  // LaTeX inline: \(...\)
  const latexInlineRegex = /\\\(([\s\S]*?)\\\)/g;
  while ((match = latexInlineRegex.exec(text)) !== null) {
    ranges.push({
      start: match.index,
      end: match.index + match[0].length,
      type: "latex",
    });
  }

  return ranges;
}

/**
 * Find all code block ranges in text
 */
export function findCodeBlockRanges(text: string): TextRange[] {
  const ranges: TextRange[] = [];

  // Code blocks: ```...```
  const codeBlockRegex = /```[\s\S]*?```/g;
  let match;
  while ((match = codeBlockRegex.exec(text)) !== null) {
    ranges.push({
      start: match.index,
      end: match.index + match[0].length,
      type: "code",
    });
  }

  // Inline code: `...`
  const inlineCodeRegex = /`[^`]+`/g;
  while ((match = inlineCodeRegex.exec(text)) !== null) {
    ranges.push({
      start: match.index,
      end: match.index + match[0].length,
      type: "code",
    });
  }

  return ranges;
}

/**
 * Find all HTML comment ranges
 */
export function findHtmlCommentRanges(text: string): TextRange[] {
  const ranges: TextRange[] = [];
  const commentRegex = /<!--[\s\S]*?-->/g;
  let match;
  while ((match = commentRegex.exec(text)) !== null) {
    ranges.push({
      start: match.index,
      end: match.index + match[0].length,
      type: "html-comment",
    });
  }
  return ranges;
}

/**
 * Get all excluded ranges (LaTeX + code + comments)
 */
export function getExcludedRanges(text: string): TextRange[] {
  return [
    ...findLatexRanges(text),
    ...findCodeBlockRanges(text),
    ...findHtmlCommentRanges(text),
  ].sort((a, b) => a.start - b.start);
}

/**
 * Check if a position is inside an excluded range
 */
export function isPositionExcluded(
  position: number,
  excludedRanges: TextRange[]
): boolean {
  return excludedRanges.some(
    (range) => position >= range.start && position < range.end
  );
}

/**
 * Extract non-excluded text for number detection
 */
export function extractNonExcludedText(text: string): string {
  const excludedRanges = getExcludedRanges(text);

  if (excludedRanges.length === 0) {
    return text;
  }

  const parts: string[] = [];
  let lastEnd = 0;

  for (const range of excludedRanges) {
    // Add text before this excluded range
    if (range.start > lastEnd) {
      parts.push(text.substring(lastEnd, range.start));
    }
    // Add placeholder spaces to maintain positions
    parts.push(" ".repeat(range.end - range.start));
    lastEnd = range.end;
  }

  // Add remaining text
  if (lastEnd < text.length) {
    parts.push(text.substring(lastEnd));
  }

  return parts.join("");
}
