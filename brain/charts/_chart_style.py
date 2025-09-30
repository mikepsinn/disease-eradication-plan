"""
Centralized chart styling for all visualizations in the DIH project.

This module provides consistent color palettes, typography, and styling
for all charts and diagrams. Import this module and call setup_chart_style()
at the beginning of any visualization code.

Usage:
    from brain.charts._chart_style import setup_chart_style, COLOR_DARK, COLOR_ACCENT

    setup_chart_style()

    fig, ax = plt.subplots()
    ax.plot(x, y, color=COLOR_ACCENT)
"""

import matplotlib.pyplot as plt
from matplotlib import rcParams

# Official Color Palette (WWII Propaganda Style)
COLOR_DARK = '#1a1a1a'       # Almost black - primary text and emphasis
COLOR_MID = '#4a4a4a'        # Charcoal - secondary elements
COLOR_LIGHT = '#e0e0e0'      # Light gray - backgrounds and subtle elements
COLOR_RED = '#c1272d'        # Bold propaganda red - danger, urgency, problems (war, disease, waste)
COLOR_BLUE = '#0051a5'       # Bold propaganda blue - hope, solutions, action (treaty, cures, bonds)
COLOR_BG = '#f8f8f8'         # Off-white - chart backgrounds
COLOR_WHITE = '#ffffff'      # Pure white - high contrast elements

# Legacy name for backwards compatibility
COLOR_ACCENT = COLOR_BLUE

# Secondary palette for categorical data (when more than one color is needed)
PALETTE_CATEGORICAL = [
    COLOR_DARK,
    COLOR_RED,
    COLOR_BLUE,
    COLOR_MID,
    '#999999',  # Medium gray
]

# Sequential palette for gradients (light to dark)
PALETTE_SEQUENTIAL = [
    '#f8f8f8',
    '#e0e0e0',
    '#c0c0c0',
    '#999999',
    '#0051a5',
    '#c1272d',
    '#1a1a1a',
]


def setup_chart_style(style='light', dpi=150):
    """
    Apply consistent styling to all matplotlib charts.

    Args:
        style: 'light' (light background) or 'dark' (dark background)
        dpi: Resolution for saved figures (default 150 for high quality)
    """

    if style == 'light':
        bg_color = COLOR_BG
        fg_color = COLOR_DARK
        text_color = COLOR_MID
        grid_color = COLOR_LIGHT
    else:  # dark
        bg_color = COLOR_DARK
        fg_color = COLOR_WHITE
        text_color = COLOR_LIGHT
        grid_color = COLOR_MID

    # Typography - bold propaganda poster style with Cooper Black
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Cooper Black', 'Impact', 'Arial Black', 'Helvetica']
    rcParams['font.size'] = 12
    rcParams['font.weight'] = 'bold'

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

    # Grid styling (subtle)
    rcParams['axes.grid'] = True
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
    fig.text(0.97, 0.03, text,
             fontsize=11, color=COLOR_DARK,
             ha='right', va='bottom', alpha=alpha, weight='bold')


def clean_spines(ax, positions=['top', 'right']):
    """
    Remove unnecessary spines from axes for cleaner look.

    Args:
        ax: matplotlib Axes object
        positions: List of spine positions to remove (default: ['top', 'right'])
    """
    for pos in positions:
        ax.spines[pos].set_visible(False)


def style_bar_chart(ax, color=COLOR_ACCENT, edge_color=COLOR_WHITE, edge_width=1.5):
    """
    Apply consistent styling to bar charts.

    Args:
        ax: matplotlib Axes object with bar chart
        color: Fill color for bars
        edge_color: Edge color for bars
        edge_width: Width of bar edges
    """
    for patch in ax.patches:
        patch.set_facecolor(color)
        patch.set_edgecolor(edge_color)
        patch.set_linewidth(edge_width)


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


# Convenience function for quick setup
def quick_setup():
    """Quick setup with default light theme."""
    setup_chart_style(style='light')
