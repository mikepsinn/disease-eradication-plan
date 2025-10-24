"""
Centralized chart styling for all visualizations in the DIH project.

This module provides consistent B&W styling with patterns for categorical data.
Import this module and call setup_chart_style() at the beginning of any visualization code.

Usage:
    from brain.figures._chart_style import setup_chart_style, COLOR_BLACK, COLOR_WHITE
    from brain.figures._chart_style import PATTERN_DIAGONAL, PATTERN_HORIZONTAL

    setup_chart_style()

    fig, ax = plt.subplots()
    bars = ax.bar(x, y, color=COLOR_BLACK)
    bars[1].set_hatch(PATTERN_DIAGONAL)  # Apply pattern to differentiate
"""

import matplotlib.pyplot as plt
from matplotlib import rcParams
from pathlib import Path

# Official Color Palette (Black & White Only)
COLOR_BLACK = '#000000'      # Pure black - bars, text, lines
COLOR_WHITE = '#FFFFFF'      # Pure white - backgrounds

# Legacy names for backwards compatibility
COLOR_DARK = COLOR_BLACK
COLOR_ACCENT = COLOR_BLACK
COLOR_BG = COLOR_WHITE
COLOR_RED = COLOR_BLACK      # Deprecated - use patterns instead
COLOR_BLUE = COLOR_BLACK     # Deprecated - use patterns instead

# Hatch patterns for multi-category charts (use instead of color)
PATTERN_SOLID = None         # Solid black fill (default)
PATTERN_DIAGONAL = '///'     # Diagonal lines
PATTERN_HORIZONTAL = '---'   # Horizontal lines
PATTERN_CROSS = 'xxx'        # Crosshatch
PATTERN_DOTS = '...'         # Dots/stippling

# Pattern palette for categorical data
PALETTE_PATTERNS = [
    PATTERN_SOLID,
    PATTERN_DIAGONAL,
    PATTERN_HORIZONTAL,
    PATTERN_CROSS,
    PATTERN_DOTS,
]


def setup_chart_style(style='light', dpi=150):
    """
    Apply consistent styling to all matplotlib charts.

    Args:
        style: 'light' (light background) or 'dark' (dark background)
        dpi: Resolution for saved figures (default 150 for high quality)
    """

    if style == 'light':
        bg_color = COLOR_WHITE
        fg_color = COLOR_BLACK
        text_color = COLOR_BLACK
        grid_color = '#e0e0e0'  # Very light gray for minimal gridlines
    else:  # dark
        bg_color = COLOR_BLACK
        fg_color = COLOR_WHITE
        text_color = COLOR_WHITE
        grid_color = '#4a4a4a'  # Charcoal for dark mode

    # Typography - clean professional sans-serif style
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans', 'sans-serif']
    rcParams['font.size'] = 12
    rcParams['font.weight'] = 'normal'
    rcParams['text.usetex'] = False  # Prevent LaTeX math parsing

    # Colors
    rcParams['figure.facecolor'] = bg_color
    rcParams['axes.facecolor'] = bg_color
    rcParams['axes.edgecolor'] = grid_color
    rcParams['axes.labelcolor'] = text_color
    rcParams['axes.titlecolor'] = fg_color
    rcParams['text.color'] = text_color
    rcParams['xtick.color'] = text_color
    rcParams['ytick.color'] = text_color
    rcParams['grid.color'] = grid_color
    rcParams['grid.alpha'] = 0.3

    # Spacing and layout - ensure padding to avoid watermark overlap
    rcParams['axes.titlepad'] = 20
    rcParams['axes.labelpad'] = 10
    rcParams['xtick.major.pad'] = 7
    rcParams['ytick.major.pad'] = 7
    rcParams['figure.subplot.bottom'] = 0.15  # Bottom margin for watermark
    rcParams['figure.subplot.top'] = 0.92     # Top margin
    rcParams['figure.subplot.left'] = 0.12    # Left margin
    rcParams['figure.subplot.right'] = 0.95   # Right margin

    # Line and marker styling
    rcParams['lines.linewidth'] = 2.5
    rcParams['lines.markersize'] = 8
    rcParams['patch.linewidth'] = 1

    # Figure settings
    rcParams['figure.dpi'] = dpi
    rcParams['savefig.dpi'] = dpi
    rcParams['savefig.bbox'] = 'tight'  # This will be overridden - use pad_inches instead
    rcParams['savefig.facecolor'] = bg_color
    rcParams['savefig.pad_inches'] = 0.3  # Add padding around saved figures

    # Remove chart junk by default
    rcParams['axes.spines.top'] = False
    rcParams['axes.spines.right'] = False

    # Grid styling (minimal - disabled by default for clean look)
    rcParams['axes.grid'] = False
    rcParams['axes.grid.axis'] = 'y'
    rcParams['grid.linestyle'] = '--'
    rcParams['grid.linewidth'] = 0.5


def add_watermark(fig, text='WarOnDisease.org', alpha=1.0):
    """
    Add consistent branding watermark to a figure.

    The watermark is positioned with padding from edges to avoid overlap with chart elements.
    Uses black color and bold weight for better visibility.

    Args:
        fig: matplotlib Figure object
        text: Watermark text (default: 'WarOnDisease.org')
        alpha: Transparency (default: 1.0 - fully opaque black)
    """
    # Watermark disabled
    pass
    # fig.text(0.97, 0.03, text,
    #          fontsize=11, color=COLOR_BLACK,
    #          ha='right', va='bottom', alpha=alpha, weight='bold')


def clean_spines(ax, positions=['top', 'right']):
    """
    Remove unnecessary spines from axes for cleaner look.

    Args:
        ax: matplotlib Axes object
        positions: List of spine positions to remove (default: ['top', 'right'])
    """
    for pos in positions:
        ax.spines[pos].set_visible(False)


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
        'title': 72,
        'subtitle': 48,
        'heading': 36,
        'body': 24,
        'caption': 18,
        'chart_title': 32,
        'axis_label': 20,
        'data_label': 18,
    }


def get_project_root():
    """
    Find the project root directory dynamically.

    Works regardless of where Quarto runs the code from.
    Returns the path to 'decentralized-institutes-of-health' directory.

    Returns:
        Path: Project root directory
    """
    project_root = Path.cwd()
    if project_root.name != 'decentralized-institutes-of-health':
        while project_root.name != 'decentralized-institutes-of-health' and project_root.parent != project_root:
            project_root = project_root.parent
    return project_root


def get_chart_metadata(title=None, description=None):
    """
    Generate standardized PNG metadata for charts.

    This metadata ensures proper attribution when images are shared while
    maintaining deterministic rendering (no timestamps or software versions).

    Args:
        title: Chart title (optional, recommended)
        description: Brief description of what the chart shows (optional)

    Returns:
        dict: Metadata dictionary for use with plt.savefig(metadata=...)

    Example:
        metadata = get_chart_metadata(
            title="Military vs Medical Research Spending",
            description="Comparison of global military and medical research budgets"
        )
        plt.savefig('chart.png', metadata=metadata)
    """
    metadata = {
        'Author': 'Mike P. Sinn',
        'Copyright': 'CC BY 4.0 - WarOnDisease.org',
        'Source': 'https://WarOnDisease.org',
    }

    if title:
        metadata['Title'] = title

    if description:
        metadata['Description'] = description

    return metadata


# Convenience function for quick setup
def quick_setup():
    """Quick setup with default light theme."""
    setup_chart_style(style='light')
