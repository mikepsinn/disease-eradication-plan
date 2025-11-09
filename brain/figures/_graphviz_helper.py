"""
Helper functions for creating Graphviz diagrams that comply with the design guide.

Design Guide Requirements:
- Black and white only (#000000, #FFFFFF)
- Serif fonts (Georgia, Times New Roman) for text
- Monospace (Courier New) for data/numbers
- Watermark: WarOnDisease.org (11pt, bold, bottom-right, 3% padding)
- PNG generation mandatory
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


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
        
        # Position: bottom-right with 3% padding (design guide spec)
        text_x = int(width * 0.97)
        text_y = int(height * 0.03)
        
        # Draw watermark (black, bold, 11pt)
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
             fontname='Georgia,serif')


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

