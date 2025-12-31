#!/usr/bin/env python3
"""
Verify PDF Link Preprocessing
==============================

Verification script to check that PDF link preprocessing works correctly.
Examines preprocessed QMD files in the temp build directory to verify:

1. Internal links (to files in test config) remain as .qmd paths
2. Cross-site links (to files in book config but not test config) become absolute URLs
3. External URLs remain unchanged
4. Anchor-only links remain unchanged

Usage:
    python verify-pdf-links.py <build_temp_path>
"""

import sys
from pathlib import Path


def verify_link_rewrites(build_temp: Path) -> bool:
    """
    Verify that link rewriting worked correctly in the temp build directory.

    Args:
        build_temp: Path to temp build directory

    Returns:
        True if all verifications pass, False otherwise
    """
    print("\n" + "=" * 80)
    print("VERIFICATION TESTS")
    print("=" * 80)

    passed = 0
    failed = 0

    # Read the preprocessed index.qmd (copied from test-economics.qmd)
    index_qmd = build_temp / "index.qmd"

    if not index_qmd.exists():
        print(f"[ERROR] index.qmd not found in {build_temp}")
        return False

    with open(index_qmd, encoding="utf-8") as f:
        index_content = f.read()

    # Read the preprocessed test-parameters.qmd
    params_qmd = build_temp / "knowledge" / "test" / "test-parameters.qmd"

    if not params_qmd.exists():
        print(f"[ERROR] test-parameters.qmd not found in {build_temp}")
        return False

    with open(params_qmd, encoding="utf-8") as f:
        params_content = f.read()

    print("\nChecking index.qmd (test-economics.qmd)...")
    print("-" * 80)

    # Test 1: Internal links should remain as .qmd
    tests = [
        {
            "name": "Internal link to test parameters remains .qmd",
            "search": "[Test Parameters](/knowledge/test/test-parameters.qmd)",
            "file": index_content,
            "should_exist": True
        },
        {
            "name": "Internal link to parameters with anchor remains .qmd",
            "search": "[Parameters intro](/knowledge/test/test-parameters.qmd#introduction)",
            "file": index_content,
            "should_exist": True
        },

        # Test 2: Cross-site links should become absolute URLs
        {
            "name": "Cross-site economics link becomes absolute URL",
            "search": "[Economics Analysis](https://manual.WarOnDisease.org/knowledge/economics/economics.html)",
            "file": index_content,
            "should_exist": True
        },
        {
            "name": "Cross-site drug development link becomes absolute URL",
            "search": "[Drug Development Cost Analysis](https://manual.WarOnDisease.org/knowledge/appendix/drug-development-cost-analysis.html)",
            "file": index_content,
            "should_exist": True
        },
        {
            "name": "Cross-site DFDA link becomes absolute URL",
            "search": "[DFDA Cost Benefit Analysis](https://manual.WarOnDisease.org/knowledge/appendix/dfda-cost-benefit-analysis.html)",
            "file": index_content,
            "should_exist": True
        },

        # Test 3: Ensure .qmd NOT present for cross-site links
        {
            "name": "Economics link should NOT have .qmd extension",
            "search": "economics/economics.qmd",
            "file": index_content,
            "should_exist": False
        },
        {
            "name": "Drug development link should NOT have .qmd extension",
            "search": "drug-development-cost-analysis.qmd",
            "file": index_content,
            "should_exist": False
        },

        # Test 4: External URLs remain unchanged
        {
            "name": "External War on Disease URL unchanged",
            "search": "[War on Disease](https://WarOnDisease.org)",
            "file": index_content,
            "should_exist": True
        },
        {
            "name": "External DIH URL unchanged",
            "search": "[Decentralized Institutes of Health](https://dih.earth)",
            "file": index_content,
            "should_exist": True
        },

        # Test 5: Anchor-only links remain unchanged
        {
            "name": "Anchor link to section unchanged",
            "search": "[Link Test Cases](#link-test-cases)",
            "file": index_content,
            "should_exist": True
        },
    ]

    print("\nChecking test-parameters.qmd...")
    print("-" * 80)

    # Test parameters file
    params_tests = [
        {
            "name": "Cross-site economics link becomes absolute URL",
            "search": "[Economics Analysis](https://manual.WarOnDisease.org/knowledge/economics/economics.html)",
            "file": params_content,
            "should_exist": True
        },
        {
            "name": "Cross-site DFDA link becomes absolute URL",
            "search": "[DFDA Cost Benefit Analysis](https://manual.WarOnDisease.org/knowledge/appendix/dfda-cost-benefit-analysis.html)",
            "file": params_content,
            "should_exist": True
        },
        {
            "name": "Cross-site drug development link becomes absolute URL",
            "search": "[Drug Development Cost Analysis](https://manual.WarOnDisease.org/knowledge/appendix/drug-development-cost-analysis.html)",
            "file": params_content,
            "should_exist": True
        },
        {
            "name": "Economics link should NOT have .qmd extension",
            "search": "economics/economics.qmd",
            "file": params_content,
            "should_exist": False
        },
        {
            "name": "DFDA link should NOT have .qmd extension",
            "search": "dfda-cost-benefit-analysis.qmd",
            "file": params_content,
            "should_exist": False
        },
    ]

    all_tests = tests + params_tests

    # Run all tests
    for test in all_tests:
        if test["should_exist"]:
            if test["search"] in test["file"]:
                print(f"[PASS] {test['name']}")
                passed += 1
            else:
                print(f"[FAIL] {test['name']}")
                print(f"       Expected to find: {test['search'][:80]}...")
                failed += 1
        else:
            if test["search"] not in test["file"]:
                print(f"[PASS] {test['name']}")
                passed += 1
            else:
                print(f"[FAIL] {test['name']}")
                print(f"       Should NOT contain: {test['search'][:80]}...")
                failed += 1

    # Summary
    print("\n" + "=" * 80)
    print(f"VERIFICATION SUMMARY: {passed} passed, {failed} failed")
    print("=" * 80)

    return failed == 0


def main():
    if len(sys.argv) < 2:
        print("Usage: python verify-pdf-links.py <build_temp_path>")
        sys.exit(1)

    build_temp = Path(sys.argv[1])

    if not build_temp.exists():
        print(f"[ERROR] Build temp directory not found: {build_temp}")
        sys.exit(1)

    success = verify_link_rewrites(build_temp)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
