"""
Centralized chart styling for all visualizations in the DIH project.

This module provides consistent B&W styling with patterns for categorical data.
Import this module and call setup_chart_style() at the beginning of any visualization code.

Usage:
    from dih_economic_models.figures._chart_style import setup_chart_style, COLOR_BLACK, COLOR_WHITE
    from dih_economic_models.figures._chart_style import PATTERN_DIAGONAL, PATTERN_HORIZONTAL

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
    padding_right_inches = 0.1   # 0.1 inches from right edge
    padding_bottom_inches = 0.05  # 0.05 inches from bottom edge
    
    # Get figure size in inches
    fig_width_inches, fig_height_inches = fig.get_size_inches()
    
    # Measure text dimensions using font properties
    fontsize = 9
    watermark_color = '#666666'  # Light gray instead of black
    
    # Get font properties to measure text
    font_prop = FontProperties(size=fontsize, weight='normal')
    
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
    fig.text(x_position, y_position, text,
             fontsize=fontsize, color=watermark_color,
             ha='right', va='bottom', alpha=alpha, weight='normal',
             transform=fig.transFigure)


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
        dict: Metadata dictionary for use with add_png_metadata()

    Example:
        plt.savefig('chart.png', dpi=200)
        add_png_metadata('chart.png', title="Chart Title", description="Description")
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
        meta.add_text('Author', 'Mike P. Sinn')
        meta.add_text('Copyright', 'CC BY 4.0 - WarOnDisease.org')
        meta.add_text('Source', 'https://WarOnDisease.org')

        # Add optional fields
        if title:
            meta.add_text('Title', title)
        if description:
            meta.add_text('Description', description)

        # Save with metadata
        img.save(filepath, pnginfo=meta, optimize=False)

    except ImportError:
        # PIL not available, skip metadata
        pass


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
        save_figure_with_margins(fig, output_path, dpi=200)
    """
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight', pad_inches=pad_inches, facecolor=facecolor)


# Convenience function for quick setup
def quick_setup():
    """Quick setup with default light theme."""
    setup_chart_style(style='light')
