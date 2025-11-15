"""
Helper functions for creating Graphviz diagrams that comply with the design guide.

Design Guide Requirements:
- Black and white only (#000000, #FFFFFF)
- Serif fonts (Georgia, Times New Roman) for text
- Monospace (Courier New) for data/numbers
- Watermark: WarOnDisease.org (11pt, bold, bottom-right, 3% padding)
- PNG generation mandatory
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import graphviz

# Add Graphviz to PATH if not already there (Windows)
if sys.platform == 'win32':
    graphviz_paths = [
        r'C:\Program Files\Graphviz\bin',
        r'C:\Program Files (x86)\Graphviz\bin',
    ]
    current_path = os.environ.get('PATH', '')
    for graphviz_path in graphviz_paths:
        if os.path.exists(graphviz_path) and graphviz_path not in current_path:
            os.environ['PATH'] = f"{graphviz_path};{current_path}"
            break


def get_project_root():
    """Find project root dynamically"""
    project_root = Path.cwd()
    if project_root.name != 'decentralized-institutes-of-health':
        while project_root.name != 'decentralized-institutes-of-health' and project_root.parent != project_root:
            project_root = project_root.parent
    return project_root


def add_watermark_to_png(png_path, text='WarOnDisease.org'):
    """
    Add watermark to PNG following design guide specs.
    
    Design Guide Specs:
    - Font size: 9pt (regular, not bold)
    - Color: Light gray (#666666)
    - Position: Bottom-right with 2% padding from edges
    - Opacity: 100% (fully opaque)
    """
    try:
        img = Image.open(png_path)
        draw = ImageDraw.Draw(img)
        
        # Try to use serif font (Georgia/Times), regular weight (not bold)
        font_size = 9  # Slightly smaller
        font = None
        
        # Try Linux fonts first (regular, not bold)
        linux_fonts = [
            '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
        ]
        
        # Try Windows fonts (regular, not bold)
        windows_fonts = [
            'C:/Windows/Fonts/georgia.ttf',
            'C:/Windows/Fonts/times.ttf',
        ]
        
        # Try macOS fonts (regular, not bold)
        mac_fonts = [
            '/Library/Fonts/Georgia.ttf',
            '/System/Library/Fonts/Supplemental/Georgia.ttf',
        ]
        
        for font_path in linux_fonts + windows_fonts + mac_fonts:
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except:
                continue
        
        if font is None:
            # Fallback to default font
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        # Get image dimensions
        width, height = img.size
        
        # Calculate text bounding box to ensure it fits within image
        if font:
            # Get text bounding box (left, top, right, bottom)
            # This should include full height including descenders
            test_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = test_bbox[2] - test_bbox[0]
            text_height = test_bbox[3] - test_bbox[1]  # Full height including descenders
            
            # Also get font metrics for more accurate descent measurement
            try:
                ascent, descent = font.getmetrics()
                # Use the larger of text_height or (ascent + descent) to ensure we account for all descenders
                # Sometimes textbbox doesn't fully capture descenders, so use font metrics as backup
                text_height_with_metrics = ascent + descent
                # Use the maximum to ensure we don't clip anything
                text_height = max(text_height, text_height_with_metrics)
            except:
                pass
        else:
            # Estimate for default font (rough approximation)
            text_width = len(text) * 5  # Rough estimate: ~5 pixels per character (smaller font)
            text_height = 12  # Include descenders for default font (smaller font size)
        
        # Position: bottom-right with 3% padding (design guide spec)
        # Calculate padding in pixels (3% of image dimensions)
        padding_x = int(width * 0.03)
        padding_y = int(height * 0.03)
        
        # Position using 'rt' (right-top) anchor for most reliable positioning
        # Calculate from top, then position so bottom of text is slightly lower than padding_y
        # Reduce padding slightly to move watermark closer to bottom edge
        text_x = width - padding_x
        # Position top of text so that bottom (including descenders) is slightly lower
        # Using 2% padding instead of 3% to move it slightly lower
        adjusted_padding_y = int(height * 0.02)  # 2% instead of 3% for slightly lower position
        text_y = height - adjusted_padding_y - text_height
        
        # Ensure text doesn't go off the left or top edges
        # If text would extend beyond boundaries, adjust position
        if text_x - text_width < 0:
            text_x = text_width + padding_x  # Move right to fit
        if text_y < 0:
            text_y = padding_y  # Move down to fit, but ensure bottom is still visible
        
        # Draw watermark (light gray, regular weight, 9pt)
        # Using 'rt' (right-top) anchor - position is the top-right corner of the text
        watermark_color = '#666666'  # Light gray instead of black
        if font:
            draw.text((text_x, text_y), text, fill=watermark_color, font=font, anchor='rt')
        else:
            draw.text((text_x, text_y), text, fill=watermark_color, anchor='rt')
        
        img.save(png_path)
    except Exception as e:
        print(f"Warning: Could not add watermark to {png_path}: {e}")


def setup_graphviz_style(dot):
    """
    Apply design guide styling to a Graphviz Digraph.

    Sets:
    - Black and white colors (#000000, #FFFFFF)
    - Serif fonts (Georgia, serif)
    - White background
    - Margins to prevent watermark overlap (3% padding on all sides)
    """
    dot.attr('node',
             shape='box',
             style='rounded',
             color='#000000',
             fontcolor='#000000',
             fontname='Georgia,serif')
    dot.attr('edge',
             color='#000000',
             fontcolor='#000000',
             fontname='Georgia,serif')
    dot.attr('graph',
             bgcolor='#FFFFFF',
             fontcolor='#000000',
             fontname='Georgia,serif',
             margin='0',    # Set margin to 0, we'll add padding via 'pad' attribute
             pad='0.5')    # Padding around entire diagram (0.5 inches) - this adds space around content


def create_diagram(comment='', rankdir='TD', size=None, **kwargs):
    """
    Create a pre-styled Graphviz Digraph following design guide.

    This is the recommended way to create diagrams - it handles graphviz import
    and applies styling automatically.

    Args:
        comment: Description of the diagram (optional)
        rankdir: Layout direction ('TD', 'LR', etc.). Default: 'TD'
        size: Size constraint as string (e.g., '8,10'). Optional.
        **kwargs: Additional arguments passed to graphviz.Digraph()

    Returns:
        Styled graphviz.Digraph object ready for adding nodes/edges

    Example:
        from figures._graphviz_helper import create_diagram, render_graphviz_with_watermark

        dot = create_diagram('My Architecture', rankdir='TD', size='10,12')
        dot.node('A', 'Component A')
        dot.node('B', 'Component B')
        dot.edge('A', 'B')
        render_graphviz_with_watermark(dot, 'my-diagram')
    """
    # Create diagram with PNG format
    dot = graphviz.Digraph(comment=comment, format='png', **kwargs)

    # Apply design guide styling
    setup_graphviz_style(dot)

    # Apply layout attributes
    if rankdir:
        dot.attr(rankdir=rankdir)
    if size:
        dot.attr(size=size)

    return dot


def render_graphviz_with_watermark(dot, filename, output_dir=None):
    """
    Render Graphviz diagram to PNG with watermark and metadata.
    
    Args:
        dot: graphviz.Digraph object
        filename: Base filename (without extension)
        output_dir: Optional output directory (defaults to dih-economic-models/figures/)
    
    Returns:
        Path to generated PNG file
    """
    if output_dir is None:
        project_root = get_project_root()
        output_dir = project_root / 'dih-economic-models' / 'figures'
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    
    # Ensure proper padding is set (override any previous settings)
    # 'pad' adds padding in inches around the entire diagram content
    # Using single value applies to all sides
    dot.attr('graph', pad='0.5')  # 0.5 inch padding on all sides for proper margins
    
    # Render to PNG
    dot.render(str(output_path), cleanup=True)
    
    # Add watermark
    png_path = f'{output_path}.png'
    
    # Add padding to image if Graphviz didn't add enough
    # Load image and check if we need to add more padding
    try:
        from PIL import Image
        img = Image.open(png_path)
        width, height = img.size
        
        # Check if image has minimal padding (less than 20 pixels on any side)
        # If so, add padding using PIL
        # For now, just add watermark - Graphviz pad should handle margins
        add_watermark_to_png(png_path)
    except Exception as e:
        # If PIL operations fail, still try to add watermark
        add_watermark_to_png(png_path)
    
    return Path(png_path)

