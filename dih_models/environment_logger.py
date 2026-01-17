#!/usr/bin/env python3
"""
Environment logging utility for debugging reproducibility issues.

Logs detailed environment information to help diagnose why Monte Carlo
simulations or other numerical computations produce different results
across different environments (shells, Python versions, etc.).
"""

import os
import platform
import sys
from typing import Any, Dict, Optional


def log_environment_info(include_mc_info: bool = True) -> Dict[str, Any]:
    """
    Log detailed environment information and return it as a dict.

    Different shells, Python versions, or NumPy versions can affect random
    number generation even with the same seed. This helps diagnose why
    results differ across environments.

    Args:
        include_mc_info: Whether to include Monte Carlo specific info

    Returns:
        Dict containing all environment info for programmatic access
    """
    info: Dict[str, Any] = {}

    print("=" * 70)
    print("ENVIRONMENT DEBUG INFO (for reproducibility diagnosis)")
    print("=" * 70)

    # Python version and implementation
    info["python_version"] = sys.version
    info["python_executable"] = sys.executable
    info["python_implementation"] = platform.python_implementation()
    print(f"Python version:      {info['python_version']}")
    print(f"Python executable:   {info['python_executable']}")
    print(f"Python impl:         {info['python_implementation']}")

    # Platform info
    info["platform"] = platform.platform()
    info["machine"] = platform.machine()
    info["processor"] = platform.processor()
    print(f"Platform:            {info['platform']}")
    print(f"Machine:             {info['machine']}")
    print(f"Processor:           {info['processor']}")

    # NumPy version (critical for random number generation)
    try:
        import numpy as np
        info["numpy_version"] = np.__version__
        info["numpy_rng_type"] = type(np.random.default_rng()).__name__
        print(f"NumPy version:       {info['numpy_version']}")
        print(f"NumPy RNG default:   {info['numpy_rng_type']}")
    except ImportError:
        info["numpy_version"] = "NOT INSTALLED"
        print("NumPy version:       NOT INSTALLED")

    # SciPy version
    try:
        import scipy
        info["scipy_version"] = scipy.__version__
        print(f"SciPy version:       {info['scipy_version']}")
    except ImportError:
        info["scipy_version"] = "NOT INSTALLED"
        print("SciPy version:       NOT INSTALLED")

    # Shell/terminal environment
    shell = os.environ.get("SHELL", os.environ.get("COMSPEC", "unknown"))
    info["shell"] = shell
    print(f"Shell:               {shell}")

    # Check for common shell indicators
    ps_module_path = os.environ.get("PSModulePath", "")
    info["powershell_detected"] = bool(ps_module_path)
    if ps_module_path:
        print("PowerShell detected: Yes (PSModulePath set)")

    # Terminal type
    term = os.environ.get("TERM", os.environ.get("WT_SESSION", "unknown"))
    info["terminal"] = term
    print(f"Terminal:            {term}")

    # Check if running in git hook context
    git_hook_indicators = [
        "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
        "GIT_AUTHOR_NAME", "GIT_EXEC_PATH"
    ]
    git_env_vars = {k: os.environ.get(k, "") for k in git_hook_indicators if os.environ.get(k)}
    info["git_hook_context"] = bool(git_env_vars)
    info["git_env_vars"] = git_env_vars
    if git_env_vars:
        print("Git hook context:    Yes")
        for k, v in git_env_vars.items():
            print(f"  {k}={v[:50]}..." if len(v) > 50 else f"  {k}={v}")
    else:
        print("Git hook context:    No (no GIT_* env vars)")

    # Working directory
    info["working_directory"] = os.getcwd()
    print(f"Working directory:   {info['working_directory']}")

    # User running the script
    info["user"] = os.environ.get("USERNAME", os.environ.get("USER", "unknown"))
    print(f"User:                {info['user']}")

    # Check for CI/CD environment
    ci_indicators = ["CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL", "TRAVIS"]
    ci_env = {k: os.environ.get(k, "") for k in ci_indicators if os.environ.get(k)}
    info["ci_environment"] = ci_env if ci_env else None
    if ci_env:
        print(f"CI environment:      {ci_env}")
    else:
        print("CI environment:      No")

    # Monte Carlo specific info
    if include_mc_info:
        info["mc_random_seed"] = 42
        print("MC Random seed:      42 (hardcoded)")

    # Float precision check
    info["float_precision_digits"] = sys.float_info.dig
    print(f"Float info:          {info['float_precision_digits']} digits precision")

    print("=" * 70)
    print()

    return info


def log_mc_fingerprint(
    sims: Dict[str, Any],
    seed: int = 42,
    n_samples: int = 10000,
    n_params_with_uncertainty: int = 0
) -> str:
    """
    Log Monte Carlo simulation fingerprint and return the hash.

    Args:
        sims: Dict mapping parameter names to sample arrays
        seed: Random seed used
        n_samples: Number of MC samples
        n_params_with_uncertainty: Count of parameters with uncertainty metadata

    Returns:
        12-character hash of simulation results for comparison
    """
    import hashlib

    print(f"[MC DEBUG] Starting Monte Carlo simulation:")
    print(f"[MC DEBUG]   Seed: {seed}")
    print(f"[MC DEBUG]   N samples: {n_samples}")
    print(f"[MC DEBUG]   Parameters with uncertainty: {n_params_with_uncertainty}")

    # Log first few sample values as fingerprint
    print(f"[MC DEBUG] Simulation complete. Sample fingerprint:")
    fingerprint_params = list(sims.keys())[:3]
    for fp_param in fingerprint_params:
        fp_arr = sims[fp_param]
        if len(fp_arr) > 0:
            fp_vals = [f"{float(fp_arr[i]):.6g}" for i in range(min(5, len(fp_arr)))]
            print(f"[MC DEBUG]   {fp_param}: [{', '.join(fp_vals)}, ...]")

    # Generate deterministic hash of all simulation results
    hash_input = ""
    for name in sorted(sims.keys()):
        arr = sims[name]
        vals = [f"{float(arr[i]):.6f}" for i in range(min(100, len(arr)))]
        hash_input += f"{name}:{','.join(vals)};"

    sim_hash = hashlib.md5(hash_input.encode()).hexdigest()[:12]
    print(f"[MC DEBUG] Simulation hash: {sim_hash}")
    print(f"[MC DEBUG] (If this hash differs between runs, MC results changed)")

    return sim_hash


def check_reproducibility_requirements(strict: bool = False) -> bool:
    """
    Check if the environment meets reproducibility requirements.

    Args:
        strict: If True, require exact version match for MC reproducibility

    Returns:
        True if requirements are met, False otherwise
    """
    issues = []
    warnings = []

    # Expected versions for reproducible MC results
    # These are the versions in .venv that produce hash 44e39cab8b88
    EXPECTED_NUMPY = (2, 4)  # 2.4.x
    EXPECTED_SCIPY = (1, 16)  # 1.16.x

    # Check NumPy version
    try:
        import numpy as np
        numpy_parts = np.__version__.split(".")
        numpy_version = (int(numpy_parts[0]), int(numpy_parts[1]))

        if strict and numpy_version != EXPECTED_NUMPY:
            issues.append(
                f"NumPy {np.__version__} != expected {EXPECTED_NUMPY[0]}.{EXPECTED_NUMPY[1]}.x "
                f"(use .venv Python for reproducible MC results)"
            )
        elif numpy_version < (2, 0):
            warnings.append(f"NumPy {np.__version__} < 2.0.0 (may have RNG differences)")
    except ImportError:
        issues.append("NumPy not installed")

    # Check SciPy version
    try:
        import scipy
        scipy_parts = scipy.__version__.split(".")
        scipy_version = (int(scipy_parts[0]), int(scipy_parts[1]))

        if strict and scipy_version != EXPECTED_SCIPY:
            issues.append(
                f"SciPy {scipy.__version__} != expected {EXPECTED_SCIPY[0]}.{EXPECTED_SCIPY[1]}.x "
                f"(use .venv Python for reproducible MC results)"
            )
        elif scipy_version < (1, 10):
            warnings.append(f"SciPy {scipy.__version__} < 1.10.0")
    except ImportError:
        issues.append("SciPy not installed")

    # Check if using venv Python
    venv_indicator = os.path.join(".venv", "")
    if venv_indicator not in sys.executable:
        warnings.append(
            f"Not using .venv Python (using {sys.executable}). "
            f"MC results may differ from git hook."
        )

    if warnings:
        print("[WARN] Reproducibility concerns:")
        for warning in warnings:
            print(f"  - {warning}")

    if issues:
        print("[ERROR] Reproducibility requirements not met:")
        for issue in issues:
            print(f"  - {issue}")
        return False

    return True


def enforce_venv_python():
    """
    Check that we're running with the project's venv Python.

    Raises SystemExit if not using venv Python, to ensure reproducible results.
    """
    venv_paths = [
        os.path.join(".venv", "Scripts", "python.exe"),  # Windows
        os.path.join(".venv", "bin", "python"),  # Unix
    ]

    is_venv = any(
        os.path.normpath(venv_path) in os.path.normpath(sys.executable)
        for venv_path in venv_paths
    )

    if not is_venv:
        print("=" * 70)
        print("[ERROR] NOT USING VENV PYTHON")
        print("=" * 70)
        print(f"Current Python: {sys.executable}")
        print()
        print("For reproducible Monte Carlo results, use the project's venv:")
        print("  Windows: .venv\\Scripts\\python.exe scripts/generate-everything-...")
        print("  Unix:    .venv/bin/python scripts/generate-everything-...")
        print()
        print("Or use: pnpm run generate:everything")
        print("=" * 70)
        sys.exit(1)
