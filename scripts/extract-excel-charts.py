#!/usr/bin/env python3
"""
Extract chart images from Excel workbook.
Uses openpyxl to read chart objects and export them as images.
"""

import sys
import os
from pathlib import Path
import zipfile
import shutil
from PIL import Image
import io

def extract_charts_from_excel(excel_path, output_dir):
    """
    Extract embedded chart images from an Excel file.

    Excel files (.xlsx) are actually ZIP archives. Charts are stored as image files
    in the xl/charts/ and xl/media/ directories within the archive.
    """
    excel_path = Path(excel_path)
    output_dir = Path(output_dir)

    if not excel_path.exists():
        print(f"Error: Excel file not found: {excel_path}")
        return False

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Extracting charts from: {excel_path}")
    print(f"Output directory: {output_dir}\n")

    chart_count = 0

    try:
        # Open Excel file as ZIP archive
        with zipfile.ZipFile(excel_path, 'r') as zip_ref:
            # List all files in the archive
            file_list = zip_ref.namelist()

            # Look for chart-related files
            print("Files in Excel archive:")
            chart_files = []
            media_files = []

            for file_name in file_list:
                if 'chart' in file_name.lower():
                    chart_files.append(file_name)
                    print(f"  [CHART] {file_name}")
                elif 'media' in file_name.lower():
                    media_files.append(file_name)
                    print(f"  [MEDIA] {file_name}")

            print(f"\nFound {len(chart_files)} chart files and {len(media_files)} media files\n")

            # Extract chart definition files (XML)
            for chart_file in chart_files:
                try:
                    chart_data = zip_ref.read(chart_file)
                    output_file = output_dir / Path(chart_file).name

                    with open(output_file, 'wb') as f:
                        f.write(chart_data)

                    print(f"[OK] Extracted chart XML: {output_file.name}")
                    chart_count += 1
                except Exception as e:
                    print(f"[ERROR] Error extracting {chart_file}: {e}")

            # Extract embedded images
            for media_file in media_files:
                try:
                    # Get file extension
                    ext = Path(media_file).suffix.lower()

                    # Skip if not an image format we want
                    if ext not in ['.png', '.jpg', '.jpeg', '.gif', '.emf', '.wmf', '.bmp']:
                        continue

                    media_data = zip_ref.read(media_file)

                    # Create descriptive filename
                    base_name = Path(media_file).stem
                    output_file = output_dir / f"chart-image-{base_name}{ext}"

                    with open(output_file, 'wb') as f:
                        f.write(media_data)

                    print(f"[OK] Extracted image: {output_file.name}")

                    # Try to get image dimensions
                    try:
                        if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                            img = Image.open(io.BytesIO(media_data))
                            print(f"  -> Dimensions: {img.width}x{img.height}px")
                    except:
                        pass

                    chart_count += 1
                except Exception as e:
                    print(f"[ERROR] Error extracting {media_file}: {e}")

        print(f"\n{'=' * 60}")
        if chart_count > 0:
            print(f"[SUCCESS] Extracted {chart_count} chart/image files")
        else:
            print("[WARNING] No chart images found in the Excel file")
            print("\nPossible reasons:")
            print("- Charts may be generated dynamically from data (not pre-rendered images)")
            print("- Charts may use Excel's native chart format (requires Excel to render)")
            print("- The file may not contain embedded chart images")
        print(f"{'=' * 60}")

        return chart_count > 0

    except Exception as e:
        print(f"\n[ERROR] Error reading Excel file: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        excel_path = "assets/FDA Spending vs Life-Expectancy.xlsx"
        output_dir = "assets/extracted-fda-data/charts"
    else:
        excel_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "assets/extracted-fda-data/charts"

    success = extract_charts_from_excel(excel_path, output_dir)

    if not success:
        print("\n" + "─" * 60)
        print("Alternative approach needed:")
        print("─" * 60)
        print("Excel charts are often stored as instructions, not images.")
        print("To extract as images, you'll need to:")
        print("1. Open the Excel file in Microsoft Excel")
        print("2. Right-click each chart → 'Save as Picture'")
        print("3. Save as PNG or other image format")
        print("\nOr use a library like xlwings (requires Excel installed):")
        print("  pip install xlwings")
        sys.exit(1)

if __name__ == "__main__":
    main()
