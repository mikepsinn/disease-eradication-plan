"""Single-instance script lock helpers for local pipeline scripts.

Uses lock files with PID metadata to prevent concurrent script instances.
Stale locks are auto-cleaned when the recorded PID no longer exists.
"""
from __future__ import annotations

import json
import os
import errno
import subprocess
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import psutil  # type: ignore[import-untyped]
except Exception:  # pragma: no cover - optional dependency at runtime
    psutil = None


LOCK_START_TIME_TOLERANCE_SECONDS = 5.0


class ScriptLockError(RuntimeError):
    """Raised when a script lock cannot be acquired."""


def _process_exists(pid: int) -> bool:
    """Return True if a process with pid appears to still be running."""
    if pid <= 0:
        return False

    # Windows: os.kill(pid, 0) is unreliable for non-existent PIDs and can
    # raise odd OSError/SystemError variants. tasklist gives a stable answer.
    if os.name == "nt":
        try:
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                check=False,
            )
            line = (result.stdout or "").strip().splitlines()
            if not line:
                return False
            first = line[0].strip()
            # No match lines are not CSV rows (usually start with "INFO: ...").
            if not first.startswith('"'):
                return False
            # CSV row format: "Image Name","PID","Session Name","Session#","Mem Usage"
            parts = [p.strip().strip('"') for p in first.split('","')]
            return len(parts) >= 2 and parts[1] == str(pid)
        except Exception:
            # Fall through to the generic probe path.
            pass

    try:
        # Cross-platform probe; on Windows this can raise PermissionError for
        # living processes we cannot signal, which still means "exists".
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError as e:
        # Treat "invalid argument"/"no such process" variants as not running.
        if getattr(e, "errno", None) in {errno.ESRCH, errno.EINVAL}:
            return False
        if getattr(e, "winerror", None) in {87, 1168}:  # invalid parameter / not found
            return False
        return True
    except SystemError:
        # Defensive: CPython on Windows can surface this around os.kill probes.
        return False
    except Exception:
        return True
    return True


def _read_lock_data(lock_path: Path) -> dict[str, Any]:
    """Read JSON lock metadata (best effort)."""
    try:
        data = json.loads(lock_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {}


def _normalize_command(command: str) -> str:
    """Normalize command text for fuzzy matching."""
    normalized = command.replace("\\", "/").replace('"', " ").replace("'", " ").strip().lower()
    return " ".join(normalized.split())


def _commands_match(lock_command: str, process_command: str) -> bool:
    """Return True when command lines appear to refer to the same script run."""
    lock_norm = _normalize_command(lock_command)
    proc_norm = _normalize_command(process_command)
    if not lock_norm or not proc_norm:
        return True
    if lock_norm in proc_norm or proc_norm in lock_norm:
        return True

    lock_tokens = lock_norm.split()
    script_token = ""
    for token in lock_tokens:
        if token.endswith(".py"):
            script_token = Path(token).name
            break
    if not script_token:
        # Non-script command metadata is not reliable enough to reject ownership.
        return True
    if script_token and script_token in proc_norm:
        return True
    return False


def _parse_started_at(value: Any) -> datetime | None:
    """Parse lock started_at timestamps in ISO format."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _get_process_identity(pid: int) -> tuple[str, datetime | None]:
    """Best-effort process identity data for PID reuse detection."""
    if pid <= 0 or psutil is None:
        return "", None

    try:
        proc = psutil.Process(pid)
        cmdline = proc.cmdline()
        command = " ".join(part for part in cmdline if part)
        started_at = datetime.fromtimestamp(proc.create_time(), timezone.utc)
        return command, started_at
    except (psutil.NoSuchProcess, psutil.ZombieProcess):
        return "", None
    except Exception:
        return "", None


def _is_lock_owner_still_running(existing: dict[str, Any], pid: int) -> bool:
    """Return True if lock metadata matches a currently running process."""
    if not _process_exists(pid):
        return False

    process_command, process_started_at = _get_process_identity(pid)
    lock_command = str(existing.get("command") or "").strip()
    lock_started_at = _parse_started_at(existing.get("started_at"))

    if lock_started_at and process_started_at:
        # A lock cannot be created before its owning process starts.
        # If PID start time is meaningfully *after* lock timestamp, PID was reused.
        if (process_started_at - lock_started_at).total_seconds() > LOCK_START_TIME_TOLERANCE_SECONDS:
            return False

    if lock_command and process_command and not _commands_match(lock_command, process_command):
        return False

    return True


@dataclass
class ScriptLock:
    """Represents an acquired script lock."""
    name: str
    path: Path
    token: str
    released: bool = False

    def release(self) -> None:
        """Release lock if still owned by this process token."""
        if self.released:
            return
        self.released = True
        try:
            if not self.path.exists():
                return
            data = _read_lock_data(self.path)
            owner_token = data.get("token")
            if owner_token and owner_token != self.token:
                return
            self.path.unlink(missing_ok=True)
        except Exception:
            # Never crash shutdown on lock cleanup.
            return

    def __enter__(self) -> "ScriptLock":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()


def acquire_script_lock(name: str, project_root: Path, *, command: str = "") -> ScriptLock:
    """Acquire a single-instance lock for a script.

    Args:
        name: Logical lock name (for filename + messages).
        project_root: Repository root where `.locks/` lives.
        command: Optional command display metadata.
    """
    lock_dir = project_root / ".locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / f"{name}.lock"
    token = uuid.uuid4().hex

    payload = {
        "name": name,
        "pid": os.getpid(),
        "token": token,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "command": command,
    }

    for _ in range(3):
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            existing = _read_lock_data(lock_path)
            existing_pid = int(existing.get("pid") or 0)
            if existing_pid and _is_lock_owner_still_running(existing, existing_pid):
                started = existing.get("started_at", "unknown")
                cmd = existing.get("command", "")
                details = f" (cmd: {cmd})" if cmd else ""
                raise ScriptLockError(
                    f"Another '{name}' process is already running "
                    f"(pid={existing_pid}, started={started}){details}. "
                    f"Lock: {lock_path}"
                )
            # Stale lock; delete and retry.
            try:
                lock_path.unlink(missing_ok=True)
            except Exception as e:
                raise ScriptLockError(f"Failed to clear stale lock {lock_path}: {e}") from e
            continue

        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
            f.write("\n")
        return ScriptLock(name=name, path=lock_path, token=token)

    raise ScriptLockError(f"Failed to acquire lock for '{name}' at {lock_path}")
