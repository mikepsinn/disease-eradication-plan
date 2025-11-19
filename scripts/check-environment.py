#!/usr/bin/env python3
"""
Environment Check Script
========================

Verifies that all dependencies and configurations are in place for rendering
the book, except for Quarto CLI which must be installed separately.
"""

import sys
import subprocess
from pathlib import Path


def check_command(command: str, name: str = None) -> bool:
    """Check if a command is available in PATH."""
    name = name or command
    try:
        result = subprocess.run(
            ["which" if sys.platform != "win32" else "where", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False
        )
        if result.returncode == 0:
            print(f"[OK] {name} is installed")
            return True
        else:
            print(f"[MISSING] {name} is not installed")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to check {name}: {e}")
        return False


def check_python_package(package: str) -> bool:
    """Check if a Python package is installed."""
    try:
        __import__(package)
        print(f"[OK] Python package '{package}' is installed")
        return True
    except ImportError:
        print(f"[MISSING] Python package '{package}' is not installed")
        return False


def check_file_exists(filepath: str, description: str) -> bool:
    """Check if a file exists."""
    path = Path(filepath)
    if path.exists():
        print(f"[OK] {description} exists at {filepath}")
        return True
    else:
        print(f"[MISSING] {description} not found at {filepath}")
        return False


def main():
    print("=" * 70)
    print("Environment Check for Quarto Book Rendering")
    print("=" * 70)
    print()

    all_checks = []

    # Check Quarto (required)
    print("Checking Quarto CLI...")
    quarto_ok = check_command("quarto", "Quarto CLI")
    if quarto_ok:
        try:
            result = subprocess.run(
                ["quarto", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            version = result.stdout.strip()
            print(f"    Version: {version}")
        except Exception:
            pass
    else:
        print("    Install: See docs/QUARTO_SETUP.md or run scripts/install-quarto.sh")
    all_checks.append(quarto_ok)
    print()

    # Check Python
    print("Checking Python...")
    print(f"[OK] Python {sys.version.split()[0]}")
    all_checks.append(True)
    print()

    # Check critical Python packages
    print("Checking Python packages...")
    packages = [
        "pandas",
        "numpy",
        "matplotlib",
        "yaml",
        "jupyter",
        "nbformat",
        "ipykernel"
    ]

    for package in packages:
        package_ok = check_python_package(package)
        all_checks.append(package_ok)
    print()

    # Check custom package
    print("Checking custom packages...")
    dih_models_ok = check_python_package("dih_models")
    if not dih_models_ok:
        print("    Install: pip install -e .")
    all_checks.append(dih_models_ok)
    print()

    # Check Graphviz (for diagrams)
    print("Checking Graphviz...")
    graphviz_ok = check_command("dot", "Graphviz")
    if not graphviz_ok:
        print("    Install: sudo apt-get install graphviz")
    all_checks.append(graphviz_ok)
    print()

    # Check configuration files
    print("Checking configuration files...")
    config_checks = [
        ("_quarto-book.yml", "Book configuration"),
        ("index-book.qmd", "Book index"),
        ("_variables.yml", "Variables file"),
        ("requirements.txt", "Python requirements"),
    ]

    for filepath, desc in config_checks:
        file_ok = check_file_exists(filepath, desc)
        all_checks.append(file_ok)
    print()

    # Check scripts
    print("Checking render scripts...")
    script_checks = [
        ("scripts/render-book-website.py", "Book render script"),
        ("scripts/lib/render_utils.py", "Render utilities"),
        ("scripts/generate-variables-yml.py", "Variable generator"),
    ]

    for filepath, desc in script_checks:
        script_ok = check_file_exists(filepath, desc)
        all_checks.append(script_ok)
    print()

    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)

    passed = sum(all_checks)
    total = len(all_checks)

    print(f"Checks passed: {passed}/{total}")
    print()

    if all(all_checks):
        print("[SUCCESS] All checks passed! You can run:")
        print("          python scripts/render-book-website.py")
    elif quarto_ok and all(all_checks[1:]):
        print("[SUCCESS] All checks passed! You can run:")
        print("          python scripts/render-book-website.py")
    else:
        print("[WARNING] Some checks failed. Please install missing dependencies.")
        print()

        if not quarto_ok:
            print("To install Quarto:")
            print("  - Run: bash scripts/install-quarto.sh")
            print("  - Or see: docs/QUARTO_SETUP.md")
            print()

        if not dih_models_ok:
            print("To install dih_models package:")
            print("  pip install -e .")
            print()

        missing_packages = []
        for package in packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)

        if missing_packages:
            print("To install missing Python packages:")
            print("  pip install -r requirements.txt")
            print()

    print()
    return 0 if all(all_checks) else 1


if __name__ == "__main__":
    sys.exit(main())
