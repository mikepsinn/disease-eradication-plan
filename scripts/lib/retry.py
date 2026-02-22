"""Retry and rate-limiting utilities for audiobook pipeline."""
import time
import threading
from collections import deque


def retry_with_backoff(fn, max_attempts=3, backoff=(10, 30, 60), label=""):
    """Call fn(), retrying on exception with backoff delays.

    Returns fn's result on success, raises last exception on exhaustion.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as e:
            if attempt < max_attempts:
                wait = backoff[attempt - 1] if attempt - 1 < len(backoff) else backoff[-1]
                print(f"    [RETRY] {label}attempt {attempt}/{max_attempts} failed: {e}")
                print(f"    [RETRY] Waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                raise


class RateLimiter:
    """Thread-safe sliding-window rate limiter."""

    def __init__(self, max_requests: int, window_seconds: float):
        self._max = max_requests
        self._window = window_seconds
        self._timestamps: deque[float] = deque()
        self._lock = threading.Lock()

    def acquire(self):
        """Block until a request slot is available."""
        while True:
            with self._lock:
                now = time.monotonic()
                while self._timestamps and self._timestamps[0] <= now - self._window:
                    self._timestamps.popleft()
                if len(self._timestamps) < self._max:
                    self._timestamps.append(now)
                    return
                wait = self._timestamps[0] + self._window - now
            time.sleep(max(0.1, wait))
