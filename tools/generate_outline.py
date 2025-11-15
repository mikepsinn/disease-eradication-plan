import yaml
import re
import os

def get_file_paths_from_quarto_yaml(yaml_path):
    """Extracts all chapter and appendix file paths from a _quarto.yml file."""
    paths = []
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if 'book' in config and 'chapters' in config['book']:
            for item in config['book']['chapters']:
                if isinstance(item, dict):
                    if 'href' in item:
                        paths.append(item['href'])
                    if 'chapters' in item:
                        for sub_item in item['chapters']:
                            if isinstance(sub_item, str):
                                paths.append(sub_item)
                            elif isinstance(sub_item, dict) and 'href' in sub_item:
                                paths.append(sub_item['href'])
                elif isinstance(item, str):
                    paths.append(item)

        if 'book' in config and 'appendices' in config['book']:
            for item in config['book']['appendices']:
                 if isinstance(item, dict):
                    if 'href' in item:
                        paths.append(item['href'])
                    if 'chapters' in item:
                        for sub_item in item['chapters']:
                            if isinstance(sub_item, str):
                                paths.append(sub_item)
                            elif isinstance(sub_item, dict) and 'href' in sub_item:
                                paths.append(sub_item['href'])
                 elif isinstance(item, str):
                    paths.append(item)

    except Exception as e:
        print(f"Error reading or parsing {yaml_path}: {e}")
    return paths

def generate_outline_from_files(file_paths, output_file):
    """Reads a list of markdown/qmd files and generates a hierarchical outline."""
    full_outline = "# Complete Book Outline\n\n"
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            full_outline += f"## {file_path} (File Not Found)\n\n"
            continue

        full_outline += f"## File: `{file_path}`\n\n"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all markdown headers
            headers = re.findall(r'^(#+)\s+(.*)', content, re.MULTILINE)
            
            if not headers:
                full_outline += "- *(No headers found)*\n"
            else:
                for header in headers:
                    level = len(header[0])
                    title = header[1].strip()
                    indent = "  " * (level - 1)
                    full_outline += f"{indent}- {title}\n"
            
            full_outline += "\n---\n\n"
        except Exception as e:
            full_outline += f"Error reading file {file_path}: {e}\n\n---\n\n"

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_outline)
        print(f"Outline successfully generated at {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    quarto_yaml_path = '_quarto.yml'
    output_md_path = 'FULL_OUTLINE.md'
    
    print("Extracting file paths from _quarto.yml...")
    file_list = get_file_paths_from_quarto_yaml(quarto_yaml_path)
    
    if file_list:
        print(f"Found {len(file_list)} files. Generating outline...")
        generate_outline_from_files(file_list, output_md_path)
    else:
        print("No file paths found in _quarto.yml.")
