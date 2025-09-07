import os
import shutil
import argparse
import re

def parse_manifest(manifest_path):
    """Parses the refactor manifest file and returns a list of actions."""
    actions = []
    with open(manifest_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('- [ ]'):
                continue
            
            # Use a regular expression to robustly parse the action and paths
            match = re.match(r'- \[ \] (KEEP|MOVE|RENAME|DELETE) \.(.*)', line)
            if not match:
                continue

            action = match.group(1)
            paths_part = match.group(2).strip()
            
            # Split paths, handling potential spaces in filenames
            # This is a simple split, assuming paths don't contain spaces.
            # For more complex cases, quoted paths would be needed.
            paths = paths_part.split()
            source = paths[0]
            destination = paths[1] if len(paths) > 1 else None

            if action != 'KEEP':
                actions.append({'action': action, 'source': source, 'destination': destination})
    return actions

def execute_actions(actions, root_dir, dry_run=True):
    """Executes the file operations based on the parsed actions."""
    if dry_run:
        print("--- DRY RUN ---")
        print("The following operations will be performed:")
    
    # First, create all necessary destination directories
    for action in actions:
        if action['action'] in ['MOVE', 'RENAME'] and action['destination']:
            dest_path = os.path.join(root_dir, action['destination'].lstrip('/'))
            dest_dir = os.path.dirname(dest_path)
            if not os.path.exists(dest_dir):
                if dry_run:
                    print(f"CREATE DIR: {dest_dir}")
                else:
                    os.makedirs(dest_dir, exist_ok=True)

    # Now, perform the file operations
    for action in actions:
        source_path = os.path.join(root_dir, action['source'].lstrip('/'))
        dest_path = os.path.join(root_dir, action['destination'].lstrip('/')) if action['destination'] else None
        
        try:
            if not os.path.exists(source_path):
                print(f"WARNING: Source path not found, skipping: {source_path}")
                continue

            if action['action'] == 'MOVE' or action['action'] == 'RENAME':
                if dry_run:
                    print(f"{action['action']}: {source_path} -> {dest_path}")
                else:
                    shutil.move(source_path, dest_path)
            
            elif action['action'] == 'DELETE':
                if dry_run:
                    print(f"DELETE: {source_path}")
                else:
                    if os.path.isdir(source_path):
                        shutil.rmtree(source_path)
                    else:
                        os.remove(source_path)

        except Exception as e:
            print(f"ERROR: Could not perform {action['action']} on {source_path}. Reason: {e}")

def main():
    parser = argparse.ArgumentParser(description="Executes file refactoring based on a manifest file.")
    parser.add_argument(
        '--execute',
        action='store_true',
        help="Actually perform the file operations. Defaults to a dry run."
    )
    args = parser.parse_args()

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    manifest_path = os.path.join(root_dir, 'operations', 'refactor-manifest.md')

    if not os.path.exists(manifest_path):
        print(f"ERROR: Manifest file not found at {manifest_path}")
        return

    actions = parse_manifest(manifest_path)
    execute_actions(actions, root_dir, dry_run=not args.execute)
    
    if not args.execute:
        print("\nThis was a dry run. No files were changed.")
        print("Run with --execute to perform the refactoring.")
    else:
        print("\nRefactoring complete.")

if __name__ == "__main__":
    main()
