import os
import argparse
import re

# Define common image extensions
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.bmp', '.tiff', '.webp', '.drawio'}

def find_all_files(directory, extensions):
    """Finds all files in a directory with the given extensions, handling errors."""
    found_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            try:
                if any(file.lower().endswith(ext) for ext in extensions):
                    found_files.append(os.path.join(root, file))
            except Exception as e:
                print(f"Error processing file {file} in {root}: {e}")
    return found_files

def search_for_references(directory, filenames_to_check):
    """Searches for explicit Markdown or HTML references to filenames."""
    referenced_files = set()
    markdown_files = find_all_files(directory, {'.md'})
    
    # Create a regex that looks for any of the filenames in a Markdown link or HTML src attribute
    # This is more precise than a simple string check.
    # We escape special characters in filenames just in case.
    escaped_filenames = [re.escape(fn) for fn in filenames_to_check]
    pattern = re.compile(r'(\(|src=")([^)]*?)(' + '|'.join(escaped_filenames) + r')')

    for md_file in markdown_files:
        try:
            with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                matches = pattern.finditer(content)
                for match in matches:
                    # The third group in our regex is the matched filename
                    referenced_files.add(match.group(3))
        except Exception as e:
            print(f"Could not read file {md_file}: {e}")
            
    return referenced_files

def main():
    parser = argparse.ArgumentParser(description="Find and optionally delete unreferenced image files in a repository.")
    parser.add_argument(
        '--delete',
        action='store_true',
        help="Actually delete the unreferenced files. Default is a dry run."
    )
    args = parser.parse_args()

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    assets_dir = os.path.join(root_dir, 'assets')
    
    if not os.path.isdir(assets_dir):
        print(f"Assets directory not found at {assets_dir}")
        return

    print("Scanning for all image files...")
    image_files = find_all_files(assets_dir, IMAGE_EXTENSIONS)
    image_filenames = {os.path.basename(f) for f in image_files}
    print(f"Found {len(image_files)} total image files.")

    print("\nSearching for references in all Markdown files...")
    referenced_filenames = search_for_references(root_dir, image_filenames)
    print(f"Found references to {len(referenced_filenames)} unique images.")
    
    unreferenced_filenames = image_filenames - referenced_filenames
    
    print(f"\nFound {len(unreferenced_filenames)} unreferenced images.")
    
    if not unreferenced_filenames:
        print("\nNo unreferenced images to clean up. Exiting.")
        return
        
    if not args.delete:
        print("\n--- DRY RUN ---")
        print("The following files are unreferenced and would be deleted:")
        for filename in sorted(list(unreferenced_filenames)):
            print(f"  - {filename}")
        print("\nTo delete these files, run the script again with the --delete flag.")
    else:
        print("\n--- DELETING FILES ---")
        deleted_count = 0
        error_count = 0
        for image_path in image_files:
            if os.path.basename(image_path) in unreferenced_filenames:
                try:
                    os.remove(image_path)
                    print(f"  - Deleted: {os.path.basename(image_path)}")
                    deleted_count += 1
                except Exception as e:
                    print(f"  - Error deleting {os.path.basename(image_path)}: {e}")
                    error_count += 1
        print(f"\nSuccessfully deleted {deleted_count} files. Encountered {error_count} errors.")

if __name__ == "__main__":
    main()
