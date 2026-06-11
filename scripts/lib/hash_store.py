#!/usr/bin/env python3
"""
Python wrapper for .file-hashes.json hash tracking system.

This module provides Python scripts access to the same hash tracking system
used by TypeScript scripts, enabling unified cache invalidation across the
entire automation infrastructure.

Usage:
    from scripts.lib.hash_store import HashStore

    store = HashStore()

    # Check if file needs reprocessing
    if store.is_stale('knowledge/file.qmd', 'lastFactCheckHash'):
        # Process file...
        store.set_file_hash('knowledge/file.qmd', 'lastFactCheckHash', 'new_hash')
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

import json
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any


class HashStore:
    """Manages file hash tracking for cache invalidation."""

    # Hash field constants - must match scripts/lib/constants.ts
    HASH_FIELDS = {
        # Content formatting and style
        'FORMATTED': 'lastFormattedHash',
        'STYLE': 'lastStyleHash',

        # Content validation
        'FACT_CHECK': 'lastFactCheckHash',
        'STRUCTURE_CHECK': 'lastStructureCheckHash',
        'LINK_CHECK': 'lastLinkCheckHash',
        'FIGURE_CHECK': 'lastFigureCheckHash',
        'LATEX_CHECK': 'lastLatexCheckHash',
        'PARAM_CHECK': 'lastParamCheckHash',
        'NONPROFIT_COMPLIANCE': 'lastNonprofitComplianceHash',

        # Voice and tone
        'INSTRUCTIONAL_VOICE': 'lastInstructionalVoiceHash',
        'TONE_ELEVATION': 'lastToneElevationHash',
        'TONE_ELEVATION_WITH_HUMOR': 'lastToneElevationWithHumorHash',
        'TONE_DOWN': 'lastToneDownHash',
        'CUSTOM_INSTRUCTION': 'lastCustomInstructionHash',
        'AUDIENCE_TRANSFORM': 'lastAudienceTransformHash',

        # WISHONIA-specific hashes
        'PARAMETER_CHECK': 'lastParameterCheckHash',
        'MATH_VALIDATION': 'lastMathValidationHash',
        'CLAIM_VALIDATION': 'lastClaimValidationHash',
        'REFERENCE_LINKING': 'lastReferenceLinkingHash',
        'CONSISTENCY_CHECK': 'lastConsistencyCheckHash',
        'WISHONIA_FULL_REVIEW': 'lastWishoniaFullReviewHash',
    }

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the hash store.

        Args:
            project_root: Root directory of the project. If None, attempts to find it.
        """
        if project_root is None:
            # Try to find project root by looking for .file-hashes.json or _quarto.yml
            current = Path.cwd()
            while current != current.parent:
                if (current / '.file-hashes.json').exists() or (current / '_quarto.yml').exists():
                    project_root = current
                    break
                current = current.parent
            else:
                project_root = Path.cwd()

        self.project_root = Path(project_root)
        self.hash_file = self.project_root / '.file-hashes.json'
        self._cache: Optional[Dict[str, Any]] = None

    def _load(self) -> Dict[str, Any]:
        """Load hash store from disk, using cache if available."""
        if self._cache is not None:
            return self._cache

        if not self.hash_file.exists():
            self._cache = {}
            return self._cache

        try:
            with open(self.hash_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                self._cache = loaded if isinstance(loaded, dict) else {}
        except (json.JSONDecodeError, IOError):
            self._cache = {}

        return self._cache

    def _save(self) -> None:
        """Save hash store to disk."""
        if self._cache is None:
            return

        with open(self.hash_file, 'w', encoding='utf-8') as f:
            json.dump(self._cache, f, indent=2)

    def _normalize_path(self, file_path: str) -> str:
        """Normalize file path to use forward slashes (matching TypeScript behavior)."""
        path = Path(file_path)

        # Make relative if absolute and within project
        if path.is_absolute():
            try:
                path = path.relative_to(self.project_root)
            except ValueError:
                pass

        # Convert to forward slashes
        return str(path).replace('\\', '/')

    def get_file_hash(self, file_path: str, hash_field: str) -> Optional[str]:
        """
        Get the stored hash for a file and hash field.

        Args:
            file_path: Path to the file (relative or absolute)
            hash_field: The hash field name (e.g., 'lastFactCheckHash')

        Returns:
            The stored hash value, or None if not found
        """
        data = self._load()
        norm_path = self._normalize_path(file_path)

        file_entry = data.get(norm_path, {})
        return file_entry.get(hash_field)

    def set_file_hash(self, file_path: str, hash_field: str, hash_value: str) -> None:
        """
        Set the hash for a file and hash field.

        Args:
            file_path: Path to the file (relative or absolute)
            hash_field: The hash field name (e.g., 'lastFactCheckHash')
            hash_value: The hash value to store
        """
        data = self._load()
        norm_path = self._normalize_path(file_path)

        if norm_path not in data:
            data[norm_path] = {}

        data[norm_path][hash_field] = hash_value
        self._save()

    def compute_content_hash(self, content: str) -> str:
        """
        Compute MD5 hash of content (matching TypeScript implementation).

        Args:
            content: The content to hash

        Returns:
            MD5 hash as hexadecimal string
        """
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def compute_file_hash(self, file_path: str) -> str:
        """
        Compute MD5 hash of a file's contents.

        Args:
            file_path: Path to the file

        Returns:
            MD5 hash as hexadecimal string
        """
        path = Path(file_path)
        if not path.is_absolute():
            path = self.project_root / path

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self.compute_content_hash(content)

    def is_stale(self, file_path: str, hash_field: str) -> bool:
        """
        Check if a file needs reprocessing for a given hash field.

        A file is stale if:
        - No hash is stored for this field
        - The stored hash doesn't match the current file content

        Args:
            file_path: Path to the file
            hash_field: The hash field to check

        Returns:
            True if the file needs reprocessing, False otherwise
        """
        stored_hash = self.get_file_hash(file_path, hash_field)

        if stored_hash is None:
            return True

        try:
            current_hash = self.compute_file_hash(file_path)
            return stored_hash != current_hash
        except (FileNotFoundError, IOError):
            return True

    def mark_processed(self, file_path: str, hash_field: str) -> None:
        """
        Mark a file as processed by storing its current content hash.

        Args:
            file_path: Path to the file
            hash_field: The hash field to update
        """
        current_hash = self.compute_file_hash(file_path)
        self.set_file_hash(file_path, hash_field, current_hash)

    def clear_field(self, file_path: str, hash_field: str) -> None:
        """
        Clear a specific hash field for a file.

        Args:
            file_path: Path to the file
            hash_field: The hash field to clear
        """
        data = self._load()
        norm_path = self._normalize_path(file_path)

        if norm_path in data and hash_field in data[norm_path]:
            del data[norm_path][hash_field]
            if not data[norm_path]:
                del data[norm_path]
            self._save()

    def clear_file(self, file_path: str) -> None:
        """
        Clear all hash fields for a file.

        Args:
            file_path: Path to the file
        """
        data = self._load()
        norm_path = self._normalize_path(file_path)

        if norm_path in data:
            del data[norm_path]
            self._save()

    def get_stale_files(self, hash_field: str, file_paths: list) -> list:
        """
        Get list of files that need reprocessing.

        Args:
            hash_field: The hash field to check
            file_paths: List of file paths to check

        Returns:
            List of file paths that are stale
        """
        return [f for f in file_paths if self.is_stale(f, hash_field)]


# Convenience functions for module-level usage
_default_store: Optional[HashStore] = None

def _get_store() -> HashStore:
    global _default_store
    if _default_store is None:
        _default_store = HashStore()
    return _default_store

def get_file_hash(file_path: str, hash_field: str) -> Optional[str]:
    """Get stored hash for a file. See HashStore.get_file_hash for details."""
    return _get_store().get_file_hash(file_path, hash_field)

def set_file_hash(file_path: str, hash_field: str, hash_value: str) -> None:
    """Set hash for a file. See HashStore.set_file_hash for details."""
    _get_store().set_file_hash(file_path, hash_field, hash_value)

def is_stale(file_path: str, hash_field: str) -> bool:
    """Check if file needs reprocessing. See HashStore.is_stale for details."""
    return _get_store().is_stale(file_path, hash_field)

def mark_processed(file_path: str, hash_field: str) -> None:
    """Mark file as processed. See HashStore.mark_processed for details."""
    _get_store().mark_processed(file_path, hash_field)


if __name__ == '__main__':
    # Simple test/demo
    import sys

    if len(sys.argv) < 3:
        print("Usage: python hash_store.py <command> <args>")
        print("Commands:")
        print("  is_stale <file_path> <hash_field>  - Check if file needs reprocessing")
        print("  mark <file_path> <hash_field>      - Mark file as processed")
        print("  get <file_path> <hash_field>       - Get stored hash")
        print("  clear <file_path> [hash_field]     - Clear hash(es) for file")
        sys.exit(1)

    command = sys.argv[1]
    store = HashStore()

    if command == 'is_stale':
        file_path, hash_field = sys.argv[2], sys.argv[3]
        result = store.is_stale(file_path, hash_field)
        print(f"Stale: {result}")
        sys.exit(0 if result else 1)

    elif command == 'mark':
        file_path, hash_field = sys.argv[2], sys.argv[3]
        store.mark_processed(file_path, hash_field)
        print(f"Marked {file_path} as processed for {hash_field}")

    elif command == 'get':
        file_path, hash_field = sys.argv[2], sys.argv[3]
        result = store.get_file_hash(file_path, hash_field)
        print(result if result else "Not found")

    elif command == 'clear':
        file_path = sys.argv[2]
        if len(sys.argv) > 3:
            hash_field = sys.argv[3]
            store.clear_field(file_path, hash_field)
            print(f"Cleared {hash_field} for {file_path}")
        else:
            store.clear_file(file_path)
            print(f"Cleared all hashes for {file_path}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
