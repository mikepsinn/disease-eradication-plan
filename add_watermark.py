#!/usr/bin/env python3
"""
Script to add watermark to all images in the infographics folder.
Adds the watermark to the lower right corner of each image.
"""

import os
from PIL import Image
from pathlib import Path

# Configuration
WATERMARK_PATH = Path("assets/icons/war-on-disease-org-watermark-simple.JPG")
INFographics_DIR = Path("assets/infographics")
WATERMARK_OPACITY = 1.0  # Fully opaque
WATERMARK_SCALE = 0.075  # Scale watermark to 7.5% of image width
PADDING = 0  # No padding - flush to edges

def add_watermark_to_image(image_path, watermark_path, output_path=None):
    """
    Add watermark to the lower right corner of an image.
    
    Args:
        image_path: Path to the source image
        watermark_path: Path to the watermark image
        output_path: Path to save the watermarked image (if None, overwrites original)
    """
    try:
        # Open the main image
        img = Image.open(image_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Open the watermark
        watermark = Image.open(watermark_path)
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        
        # Calculate watermark size (scale based on image width)
        img_width, img_height = img.size
        watermark_width = int(img_width * WATERMARK_SCALE)
        
        # Maintain aspect ratio
        aspect_ratio = watermark.width / watermark.height
        watermark_height = int(watermark_width / aspect_ratio)
        
        # Resize watermark
        watermark = watermark.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)
        
        # Apply opacity
        if watermark.mode == 'RGBA':
            # Create a new alpha channel with opacity
            alpha = watermark.split()[3]
            alpha = alpha.point(lambda p: int(p * WATERMARK_OPACITY))
            watermark.putalpha(alpha)
        
        # Calculate position (lower right corner with padding)
        position_x = img_width - watermark_width - PADDING
        position_y = img_height - watermark_height - PADDING
        
        # Create a copy of the image to paste watermark on
        watermarked_img = img.copy()
        
        # Paste watermark onto image
        watermarked_img.paste(watermark, (position_x, position_y), watermark)
        
        # Convert back to RGB if original was RGB (for PNG with transparency, keep RGBA)
        if img.mode == 'RGB':
            watermarked_img = watermarked_img.convert('RGB')
        
        # Save the watermarked image
        output = output_path if output_path else image_path
        watermarked_img.save(output, quality=95, optimize=True)
        
        print(f"✓ Watermarked: {image_path.name}")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {image_path.name}: {str(e)}")
        return False

def main():
    """Main function to process all images in the infographics folder."""
    # Check if watermark exists
    if not WATERMARK_PATH.exists():
        print(f"Error: Watermark file not found at {WATERMARK_PATH}")
        return
    
    # Check if infographics directory exists
    if not INFographics_DIR.exists():
        print(f"Error: Infographics directory not found at {INFographics_DIR}")
        return
    
    # Get all PNG images
    image_files = list(INFographics_DIR.glob("*.png"))
    
    if not image_files:
        print(f"No PNG images found in {INFographics_DIR}")
        return
    
    print(f"Found {len(image_files)} images to watermark")
    print(f"Watermark: {WATERMARK_PATH}")
    print(f"Output: Overwriting original images")
    print("-" * 60)
    
    # Process each image
    success_count = 0
    for image_path in image_files:
        if add_watermark_to_image(image_path, WATERMARK_PATH):
            success_count += 1
    
    print("-" * 60)
    print(f"Completed: {success_count}/{len(image_files)} images watermarked successfully")

if __name__ == "__main__":
    main()

