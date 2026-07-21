import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest


def run_command(args: list[str], cwd: Path) -> None:
    subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True)


def prepare_hook_repo(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    sh = shutil.which("sh")
    if sh is None:
        pytest.skip("sh is required to test the Husky hook")

    project_root = Path(__file__).resolve().parents[2]
    hook_dir = tmp_path / ".husky"
    hook_dir.mkdir()
    shutil.copy2(project_root / ".husky" / "pre-commit", hook_dir / "pre-commit")

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    python_stub = bin_dir / "python"
    python_stub.write_text(
        """#!/usr/bin/env sh
if [ "${MUTATE_GENERATION:-0}" = "1" ] && echo "$*" | grep -q "pre-render-validation"; then
    printf '\ngenerated change\n' >> tracked.txt
fi
if [ "${VALIDATION_FAIL:-0}" = "1" ] && echo "$*" | grep -q "pre-render-validation"; then
    exit 1
fi
exit 0
""",
        encoding="utf-8",
    )
    python_stub.chmod(python_stub.stat().st_mode | stat.S_IEXEC)

    npx_stub = bin_dir / "npx"
    npx_stub.write_text(
        """#!/usr/bin/env sh
if [ "${PYRIGHT_FAIL:-0}" = "1" ]; then
    exit 1
fi
exit 0
""",
        encoding="utf-8",
    )
    npx_stub.chmod(npx_stub.stat().st_mode | stat.S_IEXEC)

    (tmp_path / "tracked.txt").write_text("baseline\n", encoding="utf-8")
    run_command(["git", "init", "--quiet"], tmp_path)
    run_command(["git", "add", "tracked.txt"], tmp_path)

    env = os.environ.copy()
    env["PATH"] = str(bin_dir) + os.pathsep + env["PATH"]
    env["TEST_SH"] = sh
    return hook_dir / "pre-commit", env


def test_pre_commit_runs_generation_and_validation(tmp_path: Path) -> None:
    hook, env = prepare_hook_repo(tmp_path)

    result = subprocess.run(
        [env["TEST_SH"], str(hook)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Running pre-render validation (including artifact generation)" in result.stdout
    assert "Pre-commit checks passed" in result.stdout
    assert (tmp_path / "tracked.txt").read_text(encoding="utf-8") == "baseline\n"


def test_pre_commit_allows_generated_worktree_changes(tmp_path: Path) -> None:
    hook, env = prepare_hook_repo(tmp_path)
    env["MUTATE_GENERATION"] = "1"

    result = subprocess.run(
        [env["TEST_SH"], str(hook)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Pre-commit checks passed" in result.stdout
    assert "generated change" in (tmp_path / "tracked.txt").read_text(encoding="utf-8")


def test_pre_commit_aborts_when_pyright_fails(tmp_path: Path) -> None:
    hook, env = prepare_hook_repo(tmp_path)
    env["PYRIGHT_FAIL"] = "1"

    result = subprocess.run(
        [env["TEST_SH"], str(hook)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "Python type check failed" in result.stdout
    assert "Running pre-render validation" not in result.stdout


def test_pre_commit_aborts_when_validation_fails(tmp_path: Path) -> None:
    hook, env = prepare_hook_repo(tmp_path)
    env["VALIDATION_FAIL"] = "1"

    result = subprocess.run(
        [env["TEST_SH"], str(hook)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "Pre-render validation failed" in result.stdout
    assert "Pre-commit checks passed" not in result.stdout
