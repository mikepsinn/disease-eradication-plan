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
from typing import cast

try:
    import yaml
except ImportError:
    yaml = None

if sys.platform == "win32":
    cast(io.TextIOWrapper, sys.stdout).reconfigure(encoding="utf-8")
    cast(io.TextIOWrapper, sys.stderr).reconfigure(encoding="utf-8")

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
            # Skip media files (videos can't be embedded in EPUB)
            if any(href.endswith(ext) for ext in (".mp4", ".webm", ".ogg", ".avi")):
                continue
            # Skip HTML-encoded URLs (malformed angle-bracket URLs from references)
            if href.startswith("&lt;"):
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
        "\U0001f3e5": "",
        "\U0001f3e6": "",
    }
    for emoji, replacement in emoji_replacements.items():
        html = html.replace(emoji, replacement)
    return html


def _find_project_root(epub_path):
    """Find the project root by looking for _quarto-manual.yml in parent directories."""
    p = Path(epub_path).resolve().parent
    while p != p.parent:
        if (p / "_quarto-manual.yml").exists():
            return p
        p = p.parent
    return None


def _pandoc_slugify(text):
    """Approximate Pandoc's auto_identifiers algorithm.

    1. Strip formatting/HTML
    2. Remove non-alphanumeric except hyphens, underscores, spaces, periods
    3. Spaces/newlines to hyphens
    4. Lowercase
    5. Remove leading non-letters
    6. Collapse hyphens
    """
    text = re.sub(r"<[^>]+>", "", text)  # strip HTML
    text = re.sub(r"[^\w\s\-.]", "", text)
    text = re.sub(r"[\s]+", "-", text)
    text = text.lower()
    text = re.sub(r"^[^a-z]+", "", text)  # must start with letter
    text = re.sub(r"-+", "-", text)
    text = text.strip("-")
    return text


def _extract_config_files(config):
    """Extract list of QMD files from a Quarto config dictionary."""
    files = []

    def extract_chapters(items):
        if not isinstance(items, list):
            return
        for item in items:
            if isinstance(item, str):
                files.append(item)
            elif isinstance(item, dict):
                if "href" in item:
                    files.append(item["href"])
                if "chapters" in item:
                    extract_chapters(item["chapters"])
                if "contents" in item:
                    extract_chapters(item["contents"])

    if "chapters" in config.get("book", {}):
        extract_chapters(config["book"]["chapters"])
    return files


def _build_qmd_to_chapter_map(epub, project_root):
    """Build mapping from QMD file paths to EPUB chapter files.

    Strategy:
    1. Read _quarto-manual.yml to get QMD files
    2. For each QMD, extract title -> slugify -> get expected section ID
    3. Also check for custom IDs: # Title {#custom-id}
    4. Scan EPUB chapter files for matching section IDs
    5. Build mapping with multiple path variants for lookup
    """
    if not yaml:
        print("  [WARN] PyYAML not available, skipping QMD link fixing", file=sys.stderr)
        return {}

    config_path = project_root / "_quarto-manual.yml"
    if not config_path.exists():
        return {}

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    qmd_files = _extract_config_files(config)
    if not qmd_files:
        return {}

    # Extract section ID for each QMD file
    qmd_to_slug = {}
    for qmd_path in qmd_files:
        full_path = project_root / qmd_path
        if not full_path.exists():
            continue

        with open(full_path, encoding="utf-8") as f:
            content = f.read()

        # Check for custom ID on first heading: # Title {#custom-id}
        heading_match = re.search(
            r"^#{1,2}\s+.+?\{#([^}]+)\}", content, re.MULTILINE
        )
        if heading_match:
            qmd_to_slug[qmd_path] = heading_match.group(1)
            continue

        # Extract title from YAML front matter
        fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if fm_match:
            title_match = re.search(
                r"""^title:\s*["']?(.+?)["']?\s*$""",
                fm_match.group(1),
                re.MULTILINE,
            )
            if title_match:
                slug = _pandoc_slugify(title_match.group(1))
                if slug:
                    qmd_to_slug[qmd_path] = slug

    # Build section_id -> chapter_file mapping from EPUB
    slug_to_chapter = {}
    for name in sorted(epub.namelist()):
        if not name.endswith(".xhtml") or "nav" in name or "title_page" in name:
            continue
        content = epub.read(name).decode("utf-8")
        for m in re.finditer(r'<section[^>]+id="([^"]+)"', content):
            sid = m.group(1)
            if sid not in slug_to_chapter:
                slug_to_chapter[sid] = name

    # Combine: qmd_path -> chapter_file (with multiple lookup keys)
    mapping = {}
    for qmd_path, slug in qmd_to_slug.items():
        if slug not in slug_to_chapter:
            continue
        chapter = slug_to_chapter[slug]
        # Relative path from EPUB/text/ for href rewriting
        chapter_rel = chapter.replace("EPUB/text/", "")

        # Store with multiple key variants for matching different link formats
        mapping[qmd_path] = (chapter_rel, slug)

        # Basename (e.g., "dfda.qmd")
        basename = os.path.basename(qmd_path)
        if basename not in mapping:
            mapping[basename] = (chapter_rel, slug)

        # Path suffixes (e.g., "solution/dfda.qmd")
        parts = qmd_path.split("/")
        for i in range(1, len(parts)):
            suffix = "/".join(parts[i:])
            if suffix not in mapping:
                mapping[suffix] = (chapter_rel, slug)

    return mapping


def _fix_qmd_links(html, qmd_map, all_section_ids):
    """Rewrite .qmd href links to point to correct EPUB chapter files.

    Args:
        html: XHTML content string
        qmd_map: mapping from QMD path variants to (chapter_file, section_id)
        all_section_ids: mapping from section_id to chapter_file (for anchor resolution)
    """
    def replace_link(match):
        full_tag = match.group(0)
        href = match.group(1)

        # Only fix .qmd links
        if ".qmd" not in href:
            return full_tag

        # Skip already-absolute URLs
        if href.startswith(("http://", "https://", "mailto:")):
            return full_tag

        # Split path and anchor
        if "#" in href:
            path_part, anchor = href.split("#", 1)
        else:
            path_part, anchor = href, None

        # Clean up Windows-style paths
        path_clean = path_part.replace("\\", "/").lstrip("./")

        # Try to find in mapping
        chapter_info = None

        # Try exact path
        if path_clean in qmd_map:
            chapter_info = qmd_map[path_clean]

        # Try without leading knowledge/ etc
        if not chapter_info:
            for suffix_len in range(1, path_clean.count("/") + 2):
                parts = path_clean.split("/")
                suffix = "/".join(parts[-suffix_len:])
                if suffix in qmd_map:
                    chapter_info = qmd_map[suffix]
                    break

        if not chapter_info:
            return full_tag

        chapter_file, default_slug = chapter_info

        # Build new href
        if anchor and anchor in all_section_ids:
            # Anchor points to a specific section - find its chapter file
            anchor_chapter = all_section_ids[anchor]
            new_href = f"{anchor_chapter}#{anchor}"
        elif anchor:
            # Anchor exists but we don't know which file - use target chapter + anchor
            new_href = f"{chapter_file}#{anchor}"
        else:
            # No anchor - link to the chapter's main section
            new_href = f"{chapter_file}#{default_slug}"

        return full_tag.replace(f'href="{href}"', f'href="{new_href}"')

    return re.sub(r'<a[^>]+href="([^"]+)"[^>]*>', replace_link, html)


def fix_epub(epub_path, project_root=None):
    """Post-process EPUB to fix e-reader compatibility issues.

    Fixes:
    - Simplify Quarto figure wrappers (fixes caption-above-image on e-readers)
    - Strip emoji characters that render as empty boxes on e-readers
    - Rewrite broken .qmd links to correct EPUB chapter references
    """
    epub_path = Path(epub_path)
    print(f"[*] Fixing EPUB: {epub_path}")

    # Find project root for QMD link mapping
    if not project_root:
        project_root = _find_project_root(epub_path)

    # Read original EPUB and build QMD link mapping
    original = zipfile.ZipFile(epub_path, "r")

    qmd_map = {}
    all_section_ids = {}
    links_fixed = 0
    if project_root:
        qmd_map = _build_qmd_to_chapter_map(original, project_root)
        if qmd_map:
            # Build section_id -> chapter_file mapping for anchor resolution
            for name in original.namelist():
                if not name.endswith(".xhtml") or "nav" in name:
                    continue
                content = original.read(name).decode("utf-8")
                chapter_rel = name.replace("EPUB/text/", "")
                for m in re.finditer(r'id="([^"]+)"', content):
                    sid = m.group(1)
                    if sid not in all_section_ids:
                        all_section_ids[sid] = chapter_rel
            print(f"  [*] Built QMD mapping: {len(qmd_map)} path variants")

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
                if qmd_map:
                    before_links = new_content
                    new_content = _fix_qmd_links(new_content, qmd_map, all_section_ids)
                    if new_content != before_links:
                        # Count how many links were fixed
                        links_fixed += len(re.findall(r'\.qmd', before_links)) - len(re.findall(r'\.qmd', new_content))
                if new_content != content:
                    files_fixed += 1
                    data = new_content.encode("utf-8")

            new_epub.writestr(item, data)

    original.close()

    # Replace original
    shutil.move(str(tmp_path), str(epub_path))
    msg = f"[OK] Fixed {files_fixed} file(s)"
    if links_fixed > 0:
        msg += f", rewrote {links_fixed} .qmd links"
    print(msg)
    return files_fixed


def main():
    parser = argparse.ArgumentParser(description="Validate and fix EPUB structure and content")
    parser.add_argument("epub_path", nargs="?", help="Path to EPUB file")
    parser.add_argument("--fix", action="store_true", help="Fix issues in-place (simplify figures, rewrite links)")
    parser.add_argument("--project-root", type=str, help="Project root for QMD link resolution")
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
        project_root = Path(args.project_root) if args.project_root else None
        fix_epub(epub_path, project_root=project_root)

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
