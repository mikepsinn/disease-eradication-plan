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
    - Font size: 11pt (bold)
    - Color: Black (#000000)
    - Position: Bottom-right with 3% padding from edges
    - Opacity: 100% (fully opaque)
    """
    try:
        img = Image.open(png_path)
        draw = ImageDraw.Draw(img)
        
        # Try to use serif font (Georgia/Times), fallback to default
        font_size = 11
        font = None
        
        # Try Linux fonts first
        linux_fonts = [
            '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
        ]
        
        # Try Windows fonts
        windows_fonts = [
            'C:/Windows/Fonts/georgiab.ttf',
            'C:/Windows/Fonts/timesbd.ttf',
        ]
        
        # Try macOS fonts
        mac_fonts = [
            '/Library/Fonts/Georgia Bold.ttf',
            '/System/Library/Fonts/Supplemental/Georgia Bold.ttf',
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
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            # Estimate for default font (rough approximation)
            text_width = len(text) * 6  # Rough estimate: ~6 pixels per character
            text_height = 11  # Font size
        
        # Position: bottom-right with 3% padding (design guide spec)
        # Calculate padding in pixels (3% of image dimensions)
        padding_x = int(width * 0.03)
        padding_y = int(height * 0.03)
        
        # Position so right-bottom corner of text is at (width - padding_x, height - padding_y)
        # Using anchor='rb' means the anchor point is the right-bottom of the text
        text_x = width - padding_x
        text_y = height - padding_y
        
        # Ensure text doesn't go off the left or top edges
        # If text would extend beyond boundaries, adjust position
        if text_x - text_width < 0:
            text_x = text_width + padding_x  # Move right to fit
        if text_y - text_height < 0:
            text_y = text_height + padding_y  # Move down to fit
        
        # Draw watermark (black, bold, 11pt)
        # anchor='rb' means the (x, y) position is the right-bottom corner of the text
        if font:
            draw.text((text_x, text_y), text, fill='#000000', font=font, anchor='rb')
        else:
            draw.text((text_x, text_y), text, fill='#000000', anchor='rb')
        
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
             margin='0.3',  # 3% margin on all sides (0.3 inches) to prevent watermark overlap
             pad='0.3')     # Additional padding for better spacing


def render_graphviz_with_watermark(dot, filename, output_dir=None):
    """
    Render Graphviz diagram to PNG with watermark and metadata.
    
    Args:
        dot: graphviz.Digraph object
        filename: Base filename (without extension)
        output_dir: Optional output directory (defaults to brain/figures/)
    
    Returns:
        Path to generated PNG file
    """
    if output_dir is None:
        project_root = get_project_root()
        output_dir = project_root / 'brain' / 'figures'
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    
    # Render to PNG
    dot.render(str(output_path), cleanup=True)
    
    # Add watermark
    png_path = f'{output_path}.png'
    add_watermark_to_png(png_path)
    
    return Path(png_path)

