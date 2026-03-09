#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for audiobook text preparation."""
import sys
from pathlib import Path

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from generate_audiobook_text import strip_qmd_markup


def test_strip_qmd_markup_excludes_html_only_hidden_block():
    raw = """
Before

::: {.content-hidden when-format="epub"}
::: {.content-hidden when-format="pdf"}
::: {.content-hidden when-format="docx"}
One of your meat creatures said it better than I can:

<a href="/assets/images/chaplin-great-dictator-320.mp4" target="_blank">
![Charlie Chaplin - The Great Dictator Speech](/assets/images/chaplin-great-dictator-thumbnail.png)
</a>
:::
:::
:::

After
""".strip()

    stripped = strip_qmd_markup(raw)

    assert "One of your meat creatures said it better than I can" not in stripped
    assert "Charlie Chaplin" not in stripped
    assert "Before." in stripped
    assert "After." in stripped


def test_strip_qmd_markup_excludes_html_only_content_visible_block():
    raw = """
Intro

::: {.content-visible when-format="html"}
Visible only on the website.
<figure>
<img src="/assets/images/unrepresentative-democracy/ant-death-spiral.gif" alt="Ants marching in a circular death spiral" />
<figcaption>Each ant follows the one ahead.</figcaption>
</figure>
:::

Outro
""".strip()

    stripped = strip_qmd_markup(raw)

    assert "Visible only on the website" not in stripped
    assert "Each ant follows the one ahead" not in stripped
    assert "Intro." in stripped
    assert "Outro." in stripped
