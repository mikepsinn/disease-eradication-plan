#!/usr/bin/env python3
"""
Generate essential icon sizes, favicons, and social media images from source image.

This script generates:
- favicon.ico (contains 16x16, 32x32 for browsers)
- 180x180.png (Apple Touch Icon - iOS)
- 192x192.png (Android Chrome / PWA - reusable)
- 512x512.png (Android splash / PWA - reusable)
- 1200x630.png (Open Graph / Social Media - Facebook, LinkedIn, Twitter)
- 1200x1200.png (Square social media - Instagram, etc.)

All icons are transparent PNGs that can be reused across platforms.
"""

import argparse
import shutil
import sys
from pathlib import Path

from PIL import Image

# Minimal essential icon sizes - one file per size, reusable across platforms
ICON_SIZES = {
    16: "favicon",  # Included in ICO
    32: "favicon",  # Included in ICO
    180: "apple-touch",  # iOS Apple Touch Icon
    192: "android",  # Android Chrome / PWA (reusable)
    512: "android",  # Android splash / PWA (reusable)
}

# Social media image sizes (width x height)
SOCIAL_SIZES = {
    (1200, 630): "og",  # Open Graph standard (Facebook, LinkedIn, Twitter)
    (1200, 1200): "square",  # Square format (Instagram, some platforms)
}


def make_transparent_background(img, threshold=30):
    """
    Make black (or near-black) pixels transparent in an image.

    Args:
        img: PIL Image object
        threshold: RGB threshold below which pixels are considered black (0-255)

    Returns:
        PIL Image with transparent background
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    data = img.getdata()
    new_data = []

    for item in data:
        # If pixel is black or near-black, make it transparent
        if item[0] < threshold and item[1] < threshold and item[2] < threshold:
            new_data.append((0, 0, 0, 0))  # Transparent
        else:
            new_data.append(item)  # Keep original

    img.putdata(new_data)
    return img


def resize_icon(img, size, maintain_transparency=True):
    """
    Resize icon to specified size with high-quality resampling.

    Args:
        img: PIL Image object
        size: Target size (width, height) or single dimension for square
        maintain_transparency: Whether to preserve alpha channel

    Returns:
        Resized PIL Image
    """
    if isinstance(size, int):
        size = (size, size)

    # Use LANCZOS resampling for best quality
    resample = Image.Resampling.LANCZOS

    if maintain_transparency and img.mode == "RGBA":
        # Preserve transparency
        resized = img.resize(size, resample=resample)
    else:
        # Convert to RGB if no transparency needed
        if img.mode == "RGBA":
            # Create white background for non-transparent version
            background = Image.new("RGB", size, (255, 255, 255))
            resized = img.resize(size, resample=resample)
            background.paste(resized, mask=resized.split()[3] if resized.mode == "RGBA" else None)
            resized = background
        else:
            resized = img.resize(size, resample=resample)

    return resized


def resize_social_image(img, target_size, background_color=(255, 255, 255)):
    """
    Resize a wide social media image to target size, maintaining aspect ratio.
    Adds background if needed.

    Args:
        img: PIL Image object (wide format)
        target_size: Tuple of (width, height) for target size
        background_color: RGB tuple for background color

    Returns:
        Resized PIL Image with background if needed
    """
    target_width, target_height = target_size
    source_width, source_height = img.size

    # Calculate aspect ratios
    target_aspect = target_width / target_height
    source_aspect = source_width / source_height

    # Create background
    if img.mode == "RGBA":
        background = Image.new("RGBA", target_size, (*background_color, 255))
    else:
        background = Image.new("RGB", target_size, background_color)

    # Resize maintaining aspect ratio to fit within target
    if source_aspect > target_aspect:
        # Source is wider - fit to height
        new_height = target_height
        new_width = int(source_width * (target_height / source_height))
    else:
        # Source is taller - fit to width
        new_width = target_width
        new_height = int(source_height * (target_width / source_width))

    resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Center on background
    x = (target_width - new_width) // 2
    y = (target_height - new_height) // 2

    if resized.mode == "RGBA":
        background.paste(resized, (x, y), resized)
    else:
        background.paste(resized, (x, y))

    return background


def create_social_image(img, target_size, background_color=(255, 255, 255)):
    """
    Create a social media image by centering the icon on a colored background.

    Args:
        img: PIL Image object (square icon)
        target_size: Tuple of (width, height) for target size
        background_color: RGB tuple for background color

    Returns:
        PIL Image with icon centered on background
    """
    target_width, target_height = target_size

    # Always use RGB background for social media (not transparent)
    background = Image.new("RGB", target_size, background_color)

    # Calculate scaling to fit icon in the target size (with padding)
    # Use 80% of the smaller dimension to leave some padding
    icon_size = min(target_width, target_height)
    icon_size = int(icon_size * 0.8)

    # Resize icon maintaining aspect ratio
    resized_icon = resize_icon(img, icon_size, maintain_transparency=True)

    # Calculate position to center
    x = (target_width - resized_icon.width) // 2
    y = (target_height - resized_icon.height) // 2

    # Paste icon onto background
    if resized_icon.mode == "RGBA":
        background.paste(resized_icon, (x, y), resized_icon)
    else:
        background.paste(resized_icon, (x, y))

    return background


def generate_ico_file(img, output_path, sizes=None):
    """
    Generate ICO file with multiple sizes, preserving transparency.

    Args:
        img: PIL Image object (source)
        output_path: Path to save ICO file
        sizes: List of sizes to include in ICO (default: [16, 32, 48])
    """
    if sizes is None:
        sizes = [16, 32, 48]

    # Create list of images for ICO
    ico_images = []
    for size in sizes:
        # Preserve transparency for ICO
        resized = resize_icon(img, size, maintain_transparency=True)
        # Ensure RGBA mode for transparency support
        if resized.mode != "RGBA":
            resized = resized.convert("RGBA")
        ico_images.append(resized)

    # Save as ICO with transparency support
    ico_images[0].save(output_path, format="ICO", sizes=[(img.size[0], img.size[1]) for img in ico_images])


def generate_icons(source_path, output_dirs, base_name="dih-icon", transparent=True, social_source_path=None):
    """
    Generate minimal essential icon sizes from source image.

    Args:
        source_path: Path to source image (should be square, preferably 1024x1024 or larger)
        output_dirs: Base output directory or list of directories to generate icons in
        base_name: Base name for generated files
        transparent: Whether to make black backgrounds transparent
        social_source_path: Optional path to wide image for social media (if None, uses source_path)
    """
    source_path = Path(source_path)

    # Convert single directory to list
    if isinstance(output_dirs, (str, Path)):
        output_dirs = [Path(output_dirs)]
    else:
        output_dirs = [Path(d) for d in output_dirs]

    if not source_path.exists():
        print(f"Error: Source image not found: {source_path}")
        return False

    # Load source image for icons
    print(f"Loading icon source image: {source_path}")
    img = Image.open(source_path)

    # Make background transparent if requested
    if transparent:
        print("Making black background transparent...")
        img = make_transparent_background(img)

    # Ensure source is square for icons
    if img.size[0] != img.size[1]:
        print(f"Warning: Source image is not square ({img.size[0]}x{img.size[1]}). Cropping to square...")
        size = min(img.size[0], img.size[1])
        img = img.crop((0, 0, size, size))

    print(f"Icon source image: {img.size[0]}x{img.size[1]} ({img.mode} mode)")

    # Load social media source image (wide format)
    if social_source_path:
        social_source_path = Path(social_source_path)
        if not social_source_path.exists():
            print(f"Warning: Social media source image not found: {social_source_path}")
            print("Using icon source for social media images...")
            social_img = img.copy()
        else:
            print(f"\nLoading social media source image: {social_source_path}")
            social_img = Image.open(social_source_path)
            if transparent:
                social_img = make_transparent_background(social_img)
            print(f"Social media source image: {social_img.size[0]}x{social_img.size[1]} ({social_img.mode} mode)")
    else:
        social_img = img.copy()

    print()

    all_generated_files = []

    # Generate icons for each output directory
    for output_dir in output_dirs:
        print(f"\n{'='*60}")
        print(f"Generating icons in: {output_dir}")
        print(f"{'='*60}")

        output_dir.mkdir(parents=True, exist_ok=True)
        generated_files = []

        # Generate ICO file (contains 16x16 and 32x32)
        print("\nGenerating favicon.ico (16x16, 32x32)...")
        ico_path = output_dir / "favicon.ico"
        generate_ico_file(img, ico_path, sizes=[16, 32])
        generated_files.append(ico_path)
        print("  [OK] favicon.ico")

        # Generate essential PNG sizes (all transparent, reusable)
        print("\nGenerating essential icon sizes...")
        for size, purpose in ICON_SIZES.items():
            if size in [16, 32]:  # Skip, already in ICO
                continue

            resized = resize_icon(img, size, maintain_transparency=True)

            # Use standard naming conventions
            if size == 180:
                filename = "apple-touch-icon.png"
            elif size == 192:
                filename = "android-chrome-192x192.png"
            elif size == 512:
                filename = "android-chrome-512x512.png"
            else:
                filename = f"{base_name}-{size}x{size}.png"

            filepath = output_dir / filename
            resized.save(filepath, "PNG", optimize=True)
            generated_files.append(filepath)
            print(f"  [OK] {filename} ({size}x{size}) - {purpose}")

        # Generate social media images
        print("\nGenerating social media images...")
        for (width, height), purpose in SOCIAL_SIZES.items():
            if purpose == "og":
                # For OG images, copy the wide source directly
                filename = "og-image.png"  # Standard Open Graph image name
                filepath = output_dir / filename

                # Copy the wide source image directly
                if social_source_path and Path(social_source_path).exists():
                    shutil.copy2(social_source_path, filepath)
                    print(f"  [OK] {filename} (copied from wide source) - {purpose}")
                else:
                    # Fallback: resize if source not available
                    resized_social = resize_social_image(social_img, (width, height))
                    resized_social.save(filepath, "PNG", optimize=True)
                    print(f"  [OK] {filename} ({width}x{height}) - {purpose} (resized)")

                generated_files.append(filepath)
            else:
                # Square format - center on background
                resized_social = create_social_image(img, (width, height))

                if purpose == "square":
                    filename = f"{base_name}-social-{width}x{height}.png"
                else:
                    filename = f"{base_name}-{width}x{height}.png"

                filepath = output_dir / filename
                resized_social.save(filepath, "PNG", optimize=True)
                generated_files.append(filepath)
                print(f"  [OK] {filename} ({width}x{height}) - {purpose}")

        all_generated_files.extend(generated_files)
        print(f"\nGenerated {len(generated_files)} files in {output_dir}")

    # Summary
    print(f"\n{'='*60}")
    print(f"Successfully generated {len(all_generated_files)} icon files total")
    print("Output directories:")
    for output_dir in output_dirs:
        print(f"  - {output_dir}")
    print("\nNote: All PNG icons are transparent and can be reused across platforms.")
    print("      Use the same files in your HTML <link> tags and manifest.json")
    print(f"{'='*60}\n")

    return True


def main():
    parser = argparse.ArgumentParser(description="Generate minimal essential icon sizes and favicons from source image")
    parser.add_argument(
        "--source",
        type=str,
        default=r"E:\code\dih-neobrutalist\public\assets\icons\generated\dih-icon-transparent-1024.png",
        help="Path to source image (default: dih-icon-transparent-1024.png)",
    )
    parser.add_argument(
        "--output",
        type=str,
        nargs="+",
        default=None,
        help="Output directory or directories (default: both neobrutalist and current project)",
    )
    parser.add_argument(
        "--base-name", type=str, default="dih-icon", help="Base name for generated files (default: dih-icon)"
    )
    parser.add_argument("--no-transparent", action="store_true", help="Skip making black background transparent")
    parser.add_argument(
        "--social-source",
        type=str,
        default=r"E:\code\dih-neobrutalist\public\assets\icons\generated\dih-icon-wide-1280x640.png",
        help="Path to wide source image for social media (default: dih-icon-wide-1280x640.png)",
    )

    args = parser.parse_args()

    # Default to both locations if not specified
    if args.output is None:
        # Get current project root
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        current_project_icons = project_root / "assets" / "icons"

        output_dirs = [r"E:\code\dih-neobrutalist\public\assets\icons", str(current_project_icons)]
    else:
        output_dirs = args.output

    success = generate_icons(
        source_path=args.source,
        output_dirs=output_dirs,
        base_name=args.base_name,
        transparent=not args.no_transparent,
        social_source_path=args.social_source,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
