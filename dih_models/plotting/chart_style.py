"""
Centralized chart styling for all visualizations in the DIH project.

This module provides consistent B&W styling with patterns for categorical data.
Import this module and call setup_chart_style() at the beginning of any visualization code.

Usage:
    from _chart_style import setup_chart_style, COLOR_BLACK, COLOR_WHITE
    from _chart_style import PATTERN_DIAGONAL, PATTERN_HORIZONTAL

    setup_chart_style()

    fig, ax = plt.subplots()
    bars = ax.bar(x, y, color=COLOR_BLACK)
    bars[1].set_hatch(PATTERN_DIAGONAL)  # Apply pattern to differentiate
"""

import logging
import warnings
from functools import lru_cache
from pathlib import Path

from matplotlib import font_manager, rcParams

# Suppress Matplotlib font warnings globally
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

# Patch Matplotlib's font_manager to suppress stderr output
# This prevents "findfont: Font family 'serif' not found" warnings from appearing in Quarto output
_original_findfont = font_manager.findfont


def _silent_findfont(*args, **kwargs):
    """Wrapper around font_manager.findfont that suppresses stderr output"""
    import io
    import sys

    old_stderr = sys.stderr
    try:
        sys.stderr = io.StringIO()
        result = _original_findfont(*args, **kwargs)
    finally:
        sys.stderr = old_stderr
    return result


# Replace the findfont function with our silent version
font_manager.findfont = _silent_findfont

# Official Color Palette (Black & White Only)
COLOR_BLACK = "#000000"  # Pure black - bars, text, lines
COLOR_WHITE = "#FFFFFF"  # Pure white - backgrounds

# Legacy names for backwards compatibility
COLOR_DARK = COLOR_BLACK
COLOR_ACCENT = COLOR_BLACK
COLOR_BG = COLOR_WHITE
COLOR_RED = COLOR_BLACK  # Deprecated - use patterns instead
COLOR_BLUE = COLOR_BLACK  # Deprecated - use patterns instead

# Hatch patterns for multi-category charts (use instead of color)
PATTERN_SOLID = None  # Solid black fill (default)
PATTERN_DIAGONAL = "///"  # Diagonal lines
PATTERN_HORIZONTAL = "---"  # Horizontal lines
PATTERN_CROSS = "xxx"  # Crosshatch
PATTERN_DOTS = "..."  # Dots/stippling

# Pattern palette for categorical data
PALETTE_PATTERNS = [
    PATTERN_SOLID,
    PATTERN_DIAGONAL,
    PATTERN_HORIZONTAL,
    PATTERN_CROSS,
    PATTERN_DOTS,
]


SERIF_FONT_PREFERENCES = [
    "EB Garamond",
    "Crimson Text",
    "Baskerville",
    "Garamond",
    "Georgia",
    "Times New Roman",
    "serif",
]

MONOSPACE_FONT_PREFERENCES = [
    "SF Mono",
    "Monaco",
    "Cascadia Code",
    "Courier New",
    "Courier",
    "Liberation Mono",
    "DejaVu Sans Mono",
    "monospace",
]


def _find_first_available_font(preferences):
    """
    Return the first installed font from the provided preference list.

    Using fallback detection prevents matplotlib from emitting noisy warnings
    (e.g., "findfont: Font family 'Courier New' not found") when a font is
    missing on the current render environment.
    """
    # Suppress stderr output from font_manager.findfont (it prints warnings directly)
    import contextlib
    import io
    import sys

    @contextlib.contextmanager
    def suppress_stderr():
        """Temporarily suppress stderr output"""
        old_stderr = sys.stderr
        try:
            sys.stderr = io.StringIO()
            yield
        finally:
            sys.stderr = old_stderr

    # Suppress Matplotlib font warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib.font_manager")

        for font_name in preferences:
            try:
                with suppress_stderr():
                    font_path = font_manager.findfont(font_name, fallback_to_default=False)
                    # Check if we got a real font (not just the default fallback)
                    if font_path:
                        # Verify it's not just the default DejaVu Sans
                        default_path = font_manager.findfont("DejaVu Sans")
                        if font_path != default_path or font_name.lower() in ["dejavu sans", "dejavu sans mono"]:
                            return font_name
            except (ValueError, RuntimeError):
                continue

    # Use matplotlib's default monospace font name as a final fallback
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib.font_manager")
        with suppress_stderr():
            try:
                default_font = font_manager.FontProperties(family=["monospace"]).get_name()
                return default_font or "monospace"
            except Exception:
                return "monospace"


@lru_cache(maxsize=None)
def get_serif_font():
    """
    Provide the preferred serif font family available on the system.

    Returns:
        str: Name of an installed serif font.
    """
    return _find_first_available_font(tuple(SERIF_FONT_PREFERENCES))


@lru_cache(maxsize=None)
def get_monospace_font():
    """
    Provide the preferred monospace font family available on the system.

    Returns:
        str: Name of an installed monospace font.
    """
    return _find_first_available_font(tuple(MONOSPACE_FONT_PREFERENCES))


def setup_chart_style(style="light", dpi=150):
    """
    Apply consistent styling to all matplotlib charts.

    Args:
        style: 'light' (light background) or 'dark' (dark background)
        dpi: Resolution for saved figures (default 150 for high quality)
    """
    # Suppress font warnings during style setup
    import contextlib
    import io
    import sys

    @contextlib.contextmanager
    def suppress_stderr():
        """Temporarily suppress stderr output"""
        old_stderr = sys.stderr
        try:
            sys.stderr = io.StringIO()
            yield
        finally:
            sys.stderr = old_stderr

    if style == "light":
        bg_color = COLOR_WHITE
        fg_color = COLOR_BLACK
        text_color = COLOR_BLACK
        grid_color = "#e0e0e0"  # Very light gray for minimal gridlines
    else:  # dark
        bg_color = COLOR_BLACK
        fg_color = COLOR_WHITE
        text_color = COLOR_WHITE
        grid_color = "#4a4a4a"  # Charcoal for dark mode

    # Typography - align with book styling (serif-first aesthetic)
    # Suppress warnings when getting fonts
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib.font_manager")
        with suppress_stderr():
            serif_font = get_serif_font()

    rcParams["font.family"] = [serif_font]
    rcParams["font.serif"] = SERIF_FONT_PREFERENCES
    rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"]
    rcParams["font.monospace"] = MONOSPACE_FONT_PREFERENCES
    rcParams["font.monospace"] = MONOSPACE_FONT_PREFERENCES
    rcParams["font.size"] = 12
    rcParams["font.weight"] = "normal"
    rcParams["text.usetex"] = False  # Prevent LaTeX math parsing

    # Colors
    rcParams["figure.facecolor"] = bg_color
    rcParams["axes.facecolor"] = bg_color
    rcParams["axes.edgecolor"] = grid_color
    rcParams["axes.labelcolor"] = text_color
    rcParams["axes.titlecolor"] = fg_color
    rcParams["text.color"] = text_color
    rcParams["xtick.color"] = text_color
    rcParams["ytick.color"] = text_color
    rcParams["grid.color"] = grid_color
    rcParams["grid.alpha"] = 0.3

    # Spacing and layout - ensure padding to avoid watermark overlap
    rcParams["axes.titlepad"] = 20
    rcParams["axes.labelpad"] = 10
    rcParams["xtick.major.pad"] = 7
    rcParams["ytick.major.pad"] = 7
    rcParams["figure.subplot.bottom"] = 0.15  # Bottom margin for watermark
    rcParams["figure.subplot.top"] = 0.92  # Top margin
    rcParams["figure.subplot.left"] = 0.12  # Left margin
    rcParams["figure.subplot.right"] = 0.95  # Right margin

    # Line and marker styling
    rcParams["lines.linewidth"] = 2.5
    rcParams["lines.markersize"] = 8
    rcParams["patch.linewidth"] = 1

    # Figure settings
    rcParams["figure.dpi"] = dpi
    rcParams["savefig.dpi"] = dpi
    rcParams["savefig.bbox"] = "tight"  # This will be overridden - use pad_inches instead
    rcParams["savefig.facecolor"] = bg_color
    rcParams["savefig.pad_inches"] = 0.3  # Add padding around saved figures

    # Remove chart junk by default
    rcParams["axes.spines.top"] = False
    rcParams["axes.spines.right"] = False

    # Grid styling (minimal - disabled by default for clean look)
    rcParams["axes.grid"] = False
    rcParams["axes.grid.axis"] = "y"
    rcParams["grid.linestyle"] = "--"
    rcParams["grid.linewidth"] = 0.5


def add_watermark(fig, text="WarOnDisease.org", alpha=1.0):
    """
    Add consistent branding watermark to a figure.

    The watermark is positioned at the absolute bottom-right corner with fixed padding
    (in inches) regardless of figure size. This ensures consistent placement across
    different chart sizes.

    Uses font metrics to calculate text dimensions accurately without requiring
    the figure to be rendered first.

    Args:
        fig: matplotlib Figure object
        text: Watermark text (default: 'WarOnDisease.org')
        alpha: Transparency (default: 1.0 - fully opaque)
    """
    from matplotlib.font_manager import FontProperties

    # Fixed padding in inches (not percentage) for consistent placement
    padding_right_inches = 0.05  # 0.05 inches from right edge
    padding_bottom_inches = 0.05  # 0.05 inches from bottom edge

    # Get figure size in inches
    fig_width_inches, fig_height_inches = fig.get_size_inches()

    # Measure text dimensions using font properties
    fontsize = 11
    watermark_color = "#333333"  # Darker gray

    # Get font properties to measure text
    font_prop = FontProperties(size=fontsize, weight="normal")

    # Estimate text width: average character width * number of characters
    # For sans-serif fonts at 9pt, average char width is approximately 0.6 * fontsize
    # Convert points to inches: 1 point = 1/72 inches
    fontsize_inches = fontsize / 72.0
    # Average character width in inches (conservative estimate for 'WarOnDisease.org')
    avg_char_width_inches = fontsize_inches * 0.55
    text_width_inches = len(text) * avg_char_width_inches

    # Text height: font size + descenders (approximately 1.2x font size)
    text_height_inches = fontsize_inches * 1.2

    # Calculate position in figure coordinates (0-1)
    # Right edge: 1.0 - (padding + text_width) / fig_width
    # Bottom edge: (padding + text_height) / fig_height
    x_position = 1.0 - (padding_right_inches + text_width_inches) / fig_width_inches
    y_position = (padding_bottom_inches + text_height_inches) / fig_height_inches

    # Clamp to valid range [0, 1] to prevent out-of-bounds
    x_position = max(0.0, min(1.0, x_position))
    y_position = max(0.0, min(1.0, y_position))

    # Position: bottom-right corner with fixed padding
    fig.text(
        x_position,
        y_position,
        text,
        fontsize=fontsize,
        color=watermark_color,
        ha="right",
        va="bottom",
        alpha=alpha,
        weight="normal",
        transform=fig.transFigure,
    )


def clean_spines(ax, positions=["top", "right"]):
    """
    Remove unnecessary spines from axes for cleaner look.

    Args:
        ax: matplotlib Axes object
        positions: List of spine positions to remove (default: ['top', 'right'])
    """
    for pos in positions:
        ax.spines[pos].set_visible(False)


def format_tick_value(value, unit=None, prefix_currency=True):
    """
    Format a numeric value for axis tick labels with K/M/B/T suffixes.
    
    Designed for axis ticks where the unit appears in the axis label itself,
    so units are NOT appended to each tick value (e.g., axis shows "10, 20, 30"
    with label "Life Extension (years)", not "10 years, 20 years, 30 years").
    
    For currency units (USD, EUR, etc.), adds $ prefix by default since
    currency symbols are conventionally shown with values.
    
    Args:
        value: Numeric value to format
        unit: Unit string (e.g., "USD", "years", etc.) - only used to detect currency
        prefix_currency: If True, add $ prefix for currency units (default: True)
    
    Returns:
        str: Formatted string like "$1.2B", "500K", "3.5M" (no unit suffix)
    """
    abs_value = abs(value)
    sign = "-" if value < 0 else ""
    
    # Determine if this is currency (check for common currency indicators)
    is_currency = False
    if unit and prefix_currency:
        unit_lower = unit.lower()
        is_currency = any(curr in unit_lower for curr in ["usd", "dollar", "eur", "euro", "gbp", "pound", "currency"])
    
    # Format with appropriate suffix
    if abs_value >= 1e12:
        formatted = f"{abs_value / 1e12:.1f}T"
    elif abs_value >= 1e9:
        formatted = f"{abs_value / 1e9:.1f}B"
    elif abs_value >= 1e6:
        formatted = f"{abs_value / 1e6:.1f}M"
    elif abs_value >= 1e3:
        formatted = f"{abs_value / 1e3:.1f}K"
    else:
        # For small numbers, use appropriate decimal places
        if abs_value == int(abs_value):
            formatted = f"{int(abs_value)}"
        elif abs_value >= 10:
            formatted = f"{abs_value:.1f}"
        else:
            formatted = f"{abs_value:.2f}"
    
    # Clean up trailing .0 (e.g., "1.0B" -> "1B")
    if formatted.endswith(".0K"):
        formatted = formatted.replace(".0K", "K")
    elif formatted.endswith(".0M"):
        formatted = formatted.replace(".0M", "M")
    elif formatted.endswith(".0B"):
        formatted = formatted.replace(".0B", "B")
    elif formatted.endswith(".0T"):
        formatted = formatted.replace(".0T", "T")
    
    # Add currency prefix if applicable
    prefix = "$" if is_currency else ""
    
    return f"{sign}{prefix}{formatted}"


def get_tick_formatter(unit=None, prefix_currency=True):
    """
    Get a matplotlib FuncFormatter for axis tick labels.
    
    Uses K/M/B/T suffixes for large numbers and $ prefix for currency.
    Units are NOT appended (they belong in the axis label).
    
    Args:
        unit: Unit string to detect if currency formatting is needed
        prefix_currency: If True, add $ prefix for currency units (default: True)
    
    Returns:
        matplotlib.ticker.FuncFormatter: Formatter for use with ax.xaxis.set_major_formatter()
    
    Example:
        ax.xaxis.set_major_formatter(get_tick_formatter(unit="USD"))
        ax.set_xlabel("Revenue (USD)")  # Unit goes in axis label
    """
    from matplotlib.ticker import FuncFormatter
    
    def formatter(value, pos):
        return format_tick_value(value, unit=unit, prefix_currency=prefix_currency)
    
    return FuncFormatter(formatter)


def style_bar_chart(ax, color=COLOR_BLACK, patterns=None, edge_color=COLOR_BLACK, edge_width=1.5):
    """
    Apply consistent styling to bar charts.

    Args:
        ax: matplotlib Axes object with bar chart
        color: Fill color for bars (default: black)
        patterns: List of hatch patterns for multi-category charts (default: None for solid)
        edge_color: Edge color for bars
        edge_width: Width of bar edges
    """
    patches = ax.patches
    for i, patch in enumerate(patches):
        patch.set_facecolor(color)
        patch.set_edgecolor(edge_color)
        patch.set_linewidth(edge_width)
        if patterns:
            patch.set_hatch(patterns[i % len(patterns)])


def get_presentation_font_sizes():
    """
    Get recommended font sizes for presentation slides.

    Returns:
        dict: Font sizes for different text elements
    """
    return {
        "title": 72,
        "subtitle": 48,
        "heading": 36,
        "body": 24,
        "caption": 18,
        "chart_title": 32,
        "axis_label": 20,
        "data_label": 18,
    }


def get_project_root():
    """
    Find the project root directory dynamically.

    Works regardless of where Quarto runs the code from.
    Looks for marker files (package.json, pyproject.toml, _quarto.yml) to identify the root.

    Returns:
        Path: Project root directory

    Raises:
        FileNotFoundError: If project root cannot be found
    """
    # Marker files that indicate the project root
    markers = ["package.json", "pyproject.toml", "_quarto.yml", "_quarto-book.yml"]
    
    # Start from current working directory
    current = Path.cwd().resolve()
    
    # Walk up the directory tree looking for marker files
    for path in [current] + list(current.parents):
        for marker in markers:
            if (path / marker).exists():
                return path
    
    # If no markers found, fall back to looking for directory name
    # (for backwards compatibility, but this is less reliable)
    project_root = current
    if project_root.name != "decentralized-institutes-of-health":
        while project_root.name != "decentralized-institutes-of-health" and project_root.parent != project_root:
            project_root = project_root.parent
    
    # If we've reached the filesystem root without finding anything, raise an error
    if project_root == project_root.parent:
        raise FileNotFoundError(
            "Could not find project root. Looked for marker files: " + ", ".join(markers)
        )
    
    return project_root


def get_data_folder():
    """
    Get the knowledge/data folder path.

    Returns the path to the data directory where CSV and other data files are stored.

    Returns:
        Path: knowledge/data directory

    Example:
        data_path = get_data_folder() / 'historical-life-expectancy-fda-budget-drug-costs-1901-2000.csv'
        df = pd.read_csv(data_path)
    """
    return get_project_root() / 'knowledge' / 'data'


def get_chart_metadata(title=None, description=None):
    """
    Generate standardized PNG metadata for charts.

    This metadata ensures proper attribution when images are shared while
    maintaining deterministic rendering (no timestamps or software versions).

    Args:
        title: Chart title (optional, recommended)
        description: Brief description of what the chart shows (optional)

    Returns:
        dict: Metadata dictionary for use with add_png_metadata()

    Example:
        plt.savefig('chart.png', dpi=200)
        add_png_metadata('chart.png', title="Chart Title", description="Description")
    """
    metadata = {
        "Author": "Mike P. Sinn",
        "Copyright": "CC BY 4.0 - WarOnDisease.org",
        "Source": "https://WarOnDisease.org",
    }

    if title:
        metadata["Title"] = title

    if description:
        metadata["Description"] = description

    return metadata


def add_png_metadata(filepath, title=None, description=None):
    """
    Add attribution metadata to a PNG file after it's been saved.

    This is a post-processing step because matplotlib's metadata parameter
    doesn't reliably write PNG tEXt chunks. Uses PIL to add metadata.

    Args:
        filepath: Path to the PNG file
        title: Chart title (optional, recommended)
        description: Brief description (optional)

    Example:
        plt.savefig('chart.png', dpi=200, bbox_inches=None, facecolor=COLOR_WHITE)
        add_png_metadata('chart.png',
                        title="Military vs Medical Research",
                        description="Comparison of spending")
    """
    try:
        from PIL import Image, PngImagePlugin

        # Open the image
        img = Image.open(filepath)

        # Create metadata
        meta = PngImagePlugin.PngInfo()

        # Add standard attribution
        meta.add_text("Author", "Mike P. Sinn")
        meta.add_text("Copyright", "CC BY 4.0 - WarOnDisease.org")
        meta.add_text("Source", "https://WarOnDisease.org")

        # Add optional fields
        if title:
            meta.add_text("Title", title)
        if description:
            meta.add_text("Description", description)

        # Save with metadata
        img.save(filepath, pnginfo=meta, optimize=False)

    except ImportError:
        # PIL not available, skip metadata
        pass


def get_figure_output_path(filename):
    """
    Get the correct output path for saving a figure.

    This function always saves to knowledge/figures/ relative to the project root,
    regardless of where the Quarto render is executed from.

    Args:
        filename: Name of the output file (e.g., 'my-chart.png')

    Returns:
        Path: Full path where the figure should be saved

    Example:
        output_path = get_figure_output_path('trial-access-disparity-chart.png')
        save_figure_with_margins(fig, output_path)
    """

    # Always find the project root, regardless of where we're rendering from
    project_root = get_project_root()

    # Save to knowledge/figures/ (the standard location for chart outputs)
    output_dir = project_root / "knowledge" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    return output_dir / filename


def save_figure_with_margins(fig, filepath, dpi=200, pad_inches=0.3, facecolor=COLOR_WHITE):
    """
    Save a figure with proper margins and padding to ensure watermark visibility.

    This function ensures consistent margins around all charts by using bbox_inches='tight'
    with padding, which adds space around the figure content including the watermark.

    Args:
        fig: matplotlib Figure object
        filepath: Path where to save the figure
        dpi: Resolution (default: 200)
        pad_inches: Padding around figure in inches (default: 0.3)
        facecolor: Background color (default: COLOR_WHITE)

    Example:
        output_path = get_figure_output_path('my-chart.png')
        save_figure_with_margins(fig, output_path, dpi=200)
    """
    fig.savefig(filepath, dpi=dpi, bbox_inches="tight", pad_inches=pad_inches, facecolor=facecolor)


# Convenience function for quick setup
def quick_setup():
    """Quick setup with default light theme."""
    setup_chart_style(style="light")
