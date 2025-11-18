#!/usr/bin/env python3
"""
Round corners of an image and make them transparent.
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw

def round_corners(image_path, radius=None, output_path=None):
    """
    Round the corners of an image and make them transparent.
    
    Args:
        image_path: Path to input image
        radius: Corner radius in pixels (default: 10% of smaller dimension)
        output_path: Path to save output (default: overwrites input)
    """
    image_path = Path(image_path)
    
    if not image_path.exists():
        print(f"Error: Image not found: {image_path}")
        return False
    
    if output_path is None:
        output_path = image_path
    else:
        output_path = Path(output_path)
    
    # Load image
    img = Image.open(image_path)
    
    # Convert to RGBA if needed
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    width, height = img.size
    
    # Calculate radius (10% of smaller dimension if not specified)
    if radius is None:
        radius = int(min(width, height) * 0.1)
    
    # Create mask with rounded corners
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    # Draw rounded rectangle
    draw.rounded_rectangle(
        [(0, 0), (width, height)],
        radius=radius,
        fill=255
    )
    
    # Apply mask to image
    img.putalpha(mask)
    
    # Save result
    img.save(output_path, 'PNG', optimize=True)
    print(f"Successfully rounded corners (radius: {radius}px) and saved to: {output_path}")
    
    return True


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Round corners of an image and make them transparent')
    parser.add_argument('image', type=str, help='Path to input image')
    parser.add_argument('--radius', type=int, default=None, help='Corner radius in pixels (default: 10%% of smaller dimension)')
    parser.add_argument('--output', type=str, default=None, help='Output path (default: overwrites input)')
    
    args = parser.parse_args()
    
    success = round_corners(args.image, args.radius, args.output)
    sys.exit(0 if success else 1)

