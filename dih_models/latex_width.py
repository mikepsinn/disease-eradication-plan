"""
Rendered width of display-math lines, for catching equations wider than the PDF text block.

matplotlib's mathtext lays out a TeX subset with Computer Modern metrics. Every \\frac is
measured as \\dfrac (display size), which overstates nested fractions, so the estimate errs
wide. It still reads about 5% narrower than pdflatex on long lines, so callers keep a margin.
"""

from __future__ import annotations

import re
from functools import lru_cache

import matplotlib

matplotlib.use("Agg")

from matplotlib import rcParams  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402
from matplotlib.mathtext import MathTextParser  # noqa: E402

rcParams["mathtext.fontset"] = "cm"
_PARSER = MathTextParser("path")
_FONT = FontProperties(size=10)

_ENVIRONMENT_RE = re.compile(r"\\(?:begin|end)\{(?:gathered|aligned|split)\}")
_LINE_BREAK_RE = re.compile(r"\\\\(?:\[[^\]]*\])?")
# mathtext lacks \underbrace; measure the number above the brace (the label is narrower)
_UNDERBRACE_RE = re.compile(r"\\underbrace\{([^{}]*)\}_\{\\text\{[^{}]*\}\}")


def latex_display_lines(value: str) -> list[str]:
    """Each line of every $$...$$ block in a generated _latex variable."""
    lines = []
    for block in re.findall(r"\$\$(.*?)\$\$", value, re.S):
        for line in _LINE_BREAK_RE.split(_ENVIRONMENT_RE.sub("", block)):
            line = line.replace("&", "").strip()
            if line:
                lines.append(line)
    return lines


@lru_cache(maxsize=None)
def latex_line_width_pt(line: str) -> float | None:
    """Width in points of one display-math line at 10pt, or None if mathtext cannot parse it."""
    text = _UNDERBRACE_RE.sub(r"\1", line).replace(r"\frac", r"\dfrac").replace("{,}", ",")
    text = re.sub(r"\\q?quad", " ", text)
    try:
        return _PARSER.parse(f"${text}$", dpi=72, prop=_FONT).width
    except ValueError:  # TeX outside the mathtext subset; pdflatex still renders it
        return None
