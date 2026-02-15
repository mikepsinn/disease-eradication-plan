#!/usr/bin/env python3
"""
Validate and fix EPUB structure and content.

Checks:
1. Valid ZIP/EPUB structure (mimetype, META-INF, content.opf)
2. All spine items exist in the archive
3. All images referenced in XHTML exist in the archive
4. No emoji characters that render as empty boxes on e-readers
5. Figure captions appear after images (not before)
6. Navigation (TOC) entries point to existing files and anchors
7. No broken internal links between chapters
8. No raw HTML parameter links (should be stripped by Lua filter)

Usage:
    python scripts/validate-epub.py PATH_TO_EPUB
    python scripts/validate-epub.py --fix PATH_TO_EPUB  # fix issues in-place
    python scripts/validate-epub.py  # auto-finds test EPUB
"""

import argparse
import io
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Emoji that render as empty boxes on e-readers (no emoji font)
PROBLEMATIC_EMOJI = re.compile(
    "[\u2705\u274c\u274e\u2714\u2716\u2611\u2610\u26a0"
    "\U0001f4a1\U0001f4dd\U0001f6a8\U0001f389\U0001f3af"
    "\U0001f4b0\U0001f4b5\U0001f4ca\U0001f4c8\U0001f4c9"
    "\U0001f52c\U0001f52d\U0001f3e5\U0001f3e6\U0001f30d"
    "\U0001f30e\U0001f30f\u2728\U0001f525\U0001f4a5"
    "\U0001f680\U0001f916\u2764\U0001f49a\U0001f499"
    "\u2b50\U0001f31f\u26d4\u2757\u2753\u2049\u203c"
    "\U0001f4e2\U0001f4e3\U0001f3c6\U0001f396\U0001f3c5"
    "\U0001f947\U0001f948\U0001f949\U0001f4aa\u270a\u270b"
    "\U0001f44d\U0001f44e\U0001f44f\U0001f64f]"
)


class EpubError:
    def __init__(self, check_name, file_path, message, line=None):
        self.check_name = check_name
        self.file_path = file_path
        self.message = message
        self.line = line

    def __str__(self):
        loc = f"{self.file_path}"
        if self.line:
            loc += f":{self.line}"
        return f"[{self.check_name}] {loc}: {self.message}"


def validate_structure(epub):
    """Check basic EPUB structure."""
    errors = []
    names = epub.namelist()

    if names[0] != "mimetype":
        errors.append(EpubError("STRUCTURE", "mimetype", "mimetype is not the first file in archive"))
    else:
        content = epub.read("mimetype").decode("utf-8")
        if content.strip() != "application/epub+zip":
            errors.append(EpubError("STRUCTURE", "mimetype", f"Invalid mimetype: {content.strip()!r}"))

    if "META-INF/container.xml" not in names:
        errors.append(EpubError("STRUCTURE", "META-INF/container.xml", "Missing container.xml"))

    if "EPUB/content.opf" not in names:
        errors.append(EpubError("STRUCTURE", "EPUB/content.opf", "Missing content.opf"))

    return errors


def validate_spine(epub):
    """Check all spine items exist in archive."""
    errors = []
    opf = epub.read("EPUB/content.opf").decode("utf-8")
    names = set(epub.namelist())

    manifest = {}
    for match in re.finditer(r'<item\s+id="([^"]+)"\s+href="([^"]+)"', opf):
        manifest[match.group(1)] = "EPUB/" + match.group(2)

    for match in re.finditer(r'<itemref\s+idref="([^"]+)"', opf):
        idref = match.group(1)
        if idref not in manifest:
            errors.append(EpubError("SPINE", "content.opf", f"Spine references unknown id: {idref}"))
        elif manifest[idref] not in names:
            errors.append(EpubError("SPINE", manifest[idref], f"Spine item missing from archive"))

    return errors


def validate_images(epub):
    """Check all images referenced in XHTML exist."""
    errors = []
    names = set(epub.namelist())

    for name in epub.namelist():
        if not name.endswith(".xhtml"):
            continue
        content = epub.read(name).decode("utf-8")
        for match in re.finditer(r'<img[^>]+src="([^"]+)"', content):
            src = match.group(1)
            base_dir = "/".join(name.split("/")[:-1])
            if src.startswith("../"):
                parts = base_dir.split("/")
                src_parts = src.split("/")
                up_count = sum(1 for p in src_parts if p == "..")
                resolved = "/".join(parts[:max(0, len(parts) - up_count)] + src_parts[up_count:])
            elif src.startswith("/"):
                resolved = "EPUB" + src
            else:
                resolved = base_dir + "/" + src

            if resolved not in names:
                errors.append(EpubError("IMAGE", name, f"Missing image: {src} (resolved: {resolved})"))

    return errors


def validate_no_emoji(epub):
    """Check for emoji characters that render as empty boxes."""
    errors = []

    for name in epub.namelist():
        if not name.endswith(".xhtml"):
            continue
        content = epub.read(name).decode("utf-8")
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            matches = PROBLEMATIC_EMOJI.findall(line)
            if matches:
                chars = ", ".join(f"U+{ord(c):04X} ({c})" for c in matches[:5])
                errors.append(EpubError(
                    "EMOJI", name,
                    f"Emoji will render as empty boxes: {chars}",
                    line=i
                ))

    return errors


def validate_figure_captions(epub):
    """Check that figure captions appear after images, not before.

    Handles both simple figures and Quarto's wrapper structure:
    <div class="quarto-float"><figure><div><img/></div><figcaption/></figure></div>
    """
    errors = []

    for name in epub.namelist():
        if not name.endswith(".xhtml"):
            continue
        content = epub.read(name).decode("utf-8")

        # Check simple <figure> blocks
        for match in re.finditer(r"<figure[^>]*>(.*?)</figure>", content, re.DOTALL):
            figure_html = match.group(1)
            img_pos = figure_html.find("<img")
            figcaption_pos = figure_html.find("<figcaption")
            if img_pos == -1 or figcaption_pos == -1:
                continue
            if figcaption_pos < img_pos:
                cap_match = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", figure_html, re.DOTALL)
                cap_text = re.sub(r"<[^>]+>", "", cap_match.group(1))[:80] if cap_match else "(unknown)"
                line_num = content[:match.start()].count("\n") + 1
                errors.append(EpubError(
                    "CAPTION_ORDER", name,
                    f"Caption appears BEFORE image: {cap_text!r}",
                    line=line_num
                ))

        # Check Quarto wrapper divs (quarto-float wrapping figure)
        for match in re.finditer(
            r'<div[^>]*class="[^"]*quarto-float[^"]*"[^>]*>(.*?)</div>\s*(?=<(?:section|div|/section|/body))',
            content, re.DOTALL
        ):
            wrapper_html = match.group(1)
            img_pos = wrapper_html.find("<img")
            figcaption_pos = wrapper_html.find("<figcaption")
            if img_pos == -1 or figcaption_pos == -1:
                continue
            if figcaption_pos < img_pos:
                cap_match = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", wrapper_html, re.DOTALL)
                cap_text = re.sub(r"<[^>]+>", "", cap_match.group(1))[:80] if cap_match else "(unknown)"
                line_num = content[:match.start()].count("\n") + 1
                errors.append(EpubError(
                    "CAPTION_ORDER", name,
                    f"Caption appears BEFORE image in quarto-float: {cap_text!r}",
                    line=line_num
                ))

    return errors


def validate_navigation(epub):
    """Check that TOC entries point to existing files and anchors."""
    errors = []
    names = set(epub.namelist())

    if "EPUB/nav.xhtml" not in names:
        errors.append(EpubError("NAV", "EPUB/nav.xhtml", "Missing nav.xhtml"))
        return errors

    nav_content = epub.read("EPUB/nav.xhtml").decode("utf-8")

    all_ids = {}
    for name in epub.namelist():
        if not name.endswith(".xhtml"):
            continue
        content = epub.read(name).decode("utf-8")
        for id_match in re.finditer(r'id="([^"]+)"', content):
            rel_name = name.replace("EPUB/", "")
            all_ids.setdefault(rel_name, set()).add(id_match.group(1))

    for match in re.finditer(r'<a\s+href="([^"]+)"', nav_content):
        href = match.group(1)
        if href.startswith("http") or href.startswith("#"):
            continue

        if "#" in href:
            file_part, fragment = href.split("#", 1)
        else:
            file_part, fragment = href, None

        full_path = "EPUB/" + file_part if file_part else None
        if full_path and full_path not in names:
            errors.append(EpubError("NAV", "nav.xhtml", f"TOC links to missing file: {href}"))
            continue

        if fragment and file_part:
            file_ids = all_ids.get(file_part, set())
            if fragment not in file_ids:
                errors.append(EpubError("NAV", "nav.xhtml", f"TOC links to missing anchor: {href}"))

    return errors


def validate_internal_links(epub):
    """Check internal links between chapters resolve correctly."""
    errors = []
    names = set(epub.namelist())

    all_ids = {}
    for name in epub.namelist():
        if not name.endswith(".xhtml"):
            continue
        content = epub.read(name).decode("utf-8")
        for id_match in re.finditer(r'id="([^"]+)"', content):
            rel_name = name.replace("EPUB/", "")
            all_ids.setdefault(rel_name, set()).add(id_match.group(1))

    for name in epub.namelist():
        if not name.endswith(".xhtml") or name == "EPUB/nav.xhtml":
            continue
        content = epub.read(name).decode("utf-8")

        for match in re.finditer(r'<a[^>]+href="([^"]+)"', content):
            href = match.group(1)
            if href.startswith("http") or href.startswith("mailto:") or href.startswith("data:"):
                continue

            if "#" in href:
                file_part, fragment = href.split("#", 1)
            else:
                file_part, fragment = href, None

            if file_part:
                base_dir = "/".join(name.split("/")[:-1])
                if file_part.startswith("../"):
                    parts = base_dir.split("/")
                    src_parts = file_part.split("/")
                    up = sum(1 for p in src_parts if p == "..")
                    resolved = "/".join(parts[:max(0, len(parts) - up)] + src_parts[up:])
                else:
                    resolved = base_dir + "/" + file_part

                if resolved not in names:
                    line_num = content[:match.start()].count("\n") + 1
                    errors.append(EpubError(
                        "INTERNAL_LINK", name,
                        f"Broken link: {href} (resolved: {resolved})",
                        line=line_num
                    ))

    return errors


def validate_no_parameter_links(epub):
    """Check that raw parameter link HTML has been stripped."""
    errors = []

    for name in epub.namelist():
        if not name.endswith(".xhtml"):
            continue
        content = epub.read(name).decode("utf-8")
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if 'class="parameter-link"' in line and "<a " in line:
                errors.append(EpubError(
                    "PARAM_LINK", name,
                    "Raw parameter link HTML not stripped by Lua filter",
                    line=i
                ))

    return errors


# ──────────────────────────────────────────────────────────
# Fix mode: post-process EPUB to fix known e-reader issues
# ──────────────────────────────────────────────────────────

def _simplify_quarto_figures(html):
    """Simplify Quarto's complex figure wrappers to plain <figure><img><figcaption>.

    Quarto generates:
        <div class="quarto-float quarto-figure quarto-figure-center">
          <figure class="quarto-float quarto-float-fig">
            <div aria-describedby="..."><img src="..." alt="" /></div>
            <figcaption class="quarto-float-caption-bottom ...">Caption</figcaption>
          </figure>
        </div>

    E-readers render this incorrectly (caption above image). Simplify to:
        <figure id="..."><img src="..." alt="Caption" /><figcaption>Caption</figcaption></figure>
    """
    def replace_quarto_figure(match):
        full_html = match.group(0)

        # Extract figure ID from outer div
        id_match = re.search(r'<div[^>]*\bid="([^"]+)"', full_html)
        fig_id = id_match.group(1) if id_match else ""

        # Extract img tag
        img_match = re.search(r'<img\s+[^>]+/>', full_html)
        if not img_match:
            return full_html  # Can't simplify without img

        img_tag = img_match.group(0)

        # Extract figcaption content
        cap_match = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', full_html, re.DOTALL)
        if not cap_match:
            return full_html

        caption_text = cap_match.group(1).strip()

        # Add caption as alt text if img has empty alt
        if 'alt=""' in img_tag:
            plain_caption = re.sub(r'<[^>]+>', '', caption_text).strip()
            img_tag = img_tag.replace('alt=""', f'alt="{plain_caption}"')

        # Build simplified figure
        id_attr = f' id="{fig_id}"' if fig_id else ""
        return f'<figure{id_attr}>\n{img_tag}\n<figcaption>{caption_text}</figcaption>\n</figure>'

    # Match Quarto's wrapper: <div class="...quarto-float...">...<figure>...</figure>...</div>
    pattern = re.compile(
        r'<div[^>]*class="[^"]*quarto-float[^"]*"[^>]*>\s*'
        r'<figure[^>]*>.*?</figure>\s*'
        r'</div>',
        re.DOTALL
    )

    return pattern.sub(replace_quarto_figure, html)


def _strip_emoji(html):
    """Replace emoji characters with text equivalents in all XHTML content.

    The Lua filter handles Str elements, but emoji in raw HTML attributes
    (e.g., <div title="📊 Details">) slip through.
    """
    emoji_replacements = {
        "\u2705": "[YES]",
        "\u274c": "[NO]",
        "\u274e": "[NO]",
        "\u2714": "[OK]",
        "\u2716": "[X]",
        "\u2611": "[x]",
        "\u2610": "[ ]",
        "\u26a0": "[!]",
        "\U0001f4a1": "[TIP]",
        "\U0001f4dd": "[NOTE]",
        "\U0001f6a8": "[!]",
        "\U0001f4ca": "",
        "\U0001f4c8": "",
        "\U0001f4c9": "",
        "\U0001f4b0": "",
        "\U0001f4b5": "",
        "\U0001f52c": "",
        "\U0001f30d": "",
        "\U0001f680": "",
        "\U0001f3af": "",
        "\U0001f3c6": "",
        "\u2728": "",
        "\U0001f525": "",
    }
    for emoji, replacement in emoji_replacements.items():
        html = html.replace(emoji, replacement)
    return html


def fix_epub(epub_path):
    """Post-process EPUB to fix e-reader compatibility issues.

    Fixes:
    - Simplify Quarto figure wrappers (fixes caption-above-image on e-readers)
    - Strip emoji characters that render as empty boxes on e-readers
    """
    epub_path = Path(epub_path)
    print(f"[*] Fixing EPUB: {epub_path}")

    # Read original EPUB
    original = zipfile.ZipFile(epub_path, "r")
    files_fixed = 0

    # Write to temp file, then replace
    tmp_path = epub_path.with_suffix(".epub.tmp")
    with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as new_epub:
        for item in original.infolist():
            data = original.read(item.filename)

            if item.filename == "mimetype":
                # mimetype must be stored uncompressed
                new_epub.writestr(item, data, compress_type=zipfile.ZIP_STORED)
                continue

            if item.filename.endswith(".xhtml"):
                content = data.decode("utf-8")
                new_content = _simplify_quarto_figures(content)
                new_content = _strip_emoji(new_content)
                if new_content != content:
                    files_fixed += 1
                    data = new_content.encode("utf-8")

            new_epub.writestr(item, data)

    original.close()

    # Replace original
    shutil.move(str(tmp_path), str(epub_path))
    print(f"[OK] Fixed {files_fixed} file(s)")
    return files_fixed


def main():
    parser = argparse.ArgumentParser(description="Validate and fix EPUB structure and content")
    parser.add_argument("epub_path", nargs="?", help="Path to EPUB file")
    parser.add_argument("--fix", action="store_true", help="Fix issues in-place (simplify figures)")
    args = parser.parse_args()

    if args.epub_path:
        epub_path = Path(args.epub_path)
    else:
        candidates = [
            Path("_build_temp/test/_site/test/test-book.epub"),
            Path("_site/test/test-book.epub"),
        ]
        epub_path = None
        for c in candidates:
            if c.exists():
                epub_path = c
                break
        if not epub_path:
            print("[ERROR] No EPUB path provided and no test EPUB found", file=sys.stderr)
            return 1

    if not epub_path.exists():
        print(f"[ERROR] EPUB not found: {epub_path}", file=sys.stderr)
        return 1

    # Fix mode: post-process the EPUB first
    if args.fix:
        fix_epub(epub_path)

    print(f"[*] Validating EPUB: {epub_path}")

    epub = zipfile.ZipFile(epub_path)

    all_errors = []
    checks = [
        ("Structure", validate_structure),
        ("Spine", validate_spine),
        ("Images", validate_images),
        ("Emoji", validate_no_emoji),
        ("Figure captions", validate_figure_captions),
        ("Navigation", validate_navigation),
        ("Internal links", validate_internal_links),
        ("Parameter links", validate_no_parameter_links),
    ]

    for check_name, check_fn in checks:
        errors = check_fn(epub)
        if errors:
            all_errors.extend(errors)
            print(f"  [{check_name}] {len(errors)} error(s)")
        else:
            print(f"  [{check_name}] OK")

    epub.close()

    if all_errors:
        print(f"\n[ERROR] {len(all_errors)} validation error(s):\n")
        for error in all_errors:
            print(f"  {error}")
        return 1

    print(f"\n[OK] All EPUB validation checks passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
