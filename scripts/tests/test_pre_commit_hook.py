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
    printf '\nchanged by generation\n' >> tracked.txt
fi
exit 0
""",
        encoding="utf-8",
    )
    python_stub.chmod(python_stub.stat().st_mode | stat.S_IEXEC)

    pnpm_stub = bin_dir / "pnpm"
    pnpm_stub.write_text("#!/usr/bin/env sh\nexit 0\n", encoding="utf-8")
    pnpm_stub.chmod(pnpm_stub.stat().st_mode | stat.S_IEXEC)

    (tmp_path / "tracked.txt").write_text("baseline\n", encoding="utf-8")
    run_command(["git", "init", "--quiet"], tmp_path)
    run_command(["git", "add", "tracked.txt"], tmp_path)

    env = os.environ.copy()
    env["PATH"] = str(bin_dir) + os.pathsep + env["PATH"]
    env["TEST_SH"] = sh
    return hook_dir / "pre-commit", env


def test_pre_commit_continues_when_generation_changes_nothing(tmp_path: Path) -> None:
    hook, env = prepare_hook_repo(tmp_path)

    result = subprocess.run(
        [env["TEST_SH"], str(hook)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Running full pre-render validation (including artifact generation)" in result.stdout
    assert "Pre-commit checks passed" in result.stdout


def test_pre_commit_aborts_when_validation_generation_changes_worktree(tmp_path: Path) -> None:
    hook, env = prepare_hook_repo(tmp_path)
    env["MUTATE_GENERATION"] = "1"

    result = subprocess.run(
        [env["TEST_SH"], str(hook)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "Generation changed the worktree" in result.stdout
    assert "Running full pre-render validation (including artifact generation)" in result.stdout
    assert "Pre-commit checks passed" not in result.stdout
