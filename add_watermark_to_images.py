#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to add watermark to images from need-watermark folder.
Adds the watermark to the lower right corner of each image and saves to watermarked folder.
"""

import os
import sys
from pathlib import Path
from PIL import Image

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
WATERMARK_PATH = Path("assets/icons/war-on-disease-org-watermark-simple.JPG")
SOURCE_DIR = Path("assets/need-watermark")
OUTPUT_DIR = Path("assets/watermarked")
WATERMARK_OPACITY = 1.0  # Fully opaque
WATERMARK_SCALE = 0.075  # Scale watermark to 7.5% of image width
PADDING = 0  # No padding - flush to edges

def add_watermark_to_image(image_path, watermark_path, output_path):
    """
    Add watermark to the lower right corner of an image.
    
    Args:
        image_path: Path to the source image
        watermark_path: Path to the watermark image
        output_path: Path to save the watermarked image
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
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the watermarked image
        # Convert to string for Windows compatibility with special characters
        output_str = str(output_path)
        watermarked_img.save(output_str, quality=95, optimize=True)
        
        print(f"[OK] Watermarked: {image_path.name} -> {output_path.name}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to process {image_path.name}: {str(e)}")
        return False

def main():
    """Main function to process all images in the need-watermark folder."""
    # Check if watermark exists
    if not WATERMARK_PATH.exists():
        print(f"[ERROR] Watermark file not found at {WATERMARK_PATH}")
        return
    
    # Check if source directory exists
    if not SOURCE_DIR.exists():
        print(f"[ERROR] Source directory not found at {SOURCE_DIR}")
        print(f"[INFO] Creating source directory: {SOURCE_DIR}")
        SOURCE_DIR.mkdir(parents=True, exist_ok=True)
        return
    
    # Get all image files (PNG, JPG, JPEG)
    image_files = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG']:
        image_files.extend(SOURCE_DIR.glob(ext))
    
    if not image_files:
        print(f"[INFO] No images found in {SOURCE_DIR}")
        return
    
    print(f"[INFO] Found {len(image_files)} image(s) to watermark")
    print(f"[INFO] Watermark: {WATERMARK_PATH}")
    print(f"[INFO] Source: {SOURCE_DIR}")
    print(f"[INFO] Output: {OUTPUT_DIR}")
    print("-" * 60)
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Process each image
    success_count = 0
    for image_path in image_files:
        # Create output path preserving filename
        output_path = OUTPUT_DIR / image_path.name
        if add_watermark_to_image(image_path, WATERMARK_PATH, output_path):
            success_count += 1
    
    print("-" * 60)
    print(f"[SUMMARY] Completed: {success_count}/{len(image_files)} images watermarked successfully")

if __name__ == "__main__":
    main()

