#!/usr/bin/env python3
"""
URL Checker Utility with Caching

Provides URL validation with persistent file-based caching to avoid
repeated requests to the same URLs across runs.

Usage:
    from scripts.lib.url_checker import URLChecker, check_url

    # Simple function call
    result = check_url("https://example.com")

    # Or use the class for batch checking with shared cache
    checker = URLChecker(cache_ttl_hours=24)
    results = checker.check_urls(["https://example.com", "https://google.com"])
"""

import json
import os
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.error import HTTPError, URLError

# Set UTF-8 encoding for stdout on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

# Default cache location
CACHE_DIR = Path(__file__).parent.parent.parent / ".cache"
URL_CACHE_FILE = CACHE_DIR / "url_check_cache.json"


@dataclass
class URLCheckResult:
    """Result of a URL check."""

    url: str
    is_valid: bool
    status_code: Optional[int] = None
    error_message: Optional[str] = None
    from_cache: bool = False
    response_time_ms: Optional[float] = None
    is_http_error: bool = False  # True for 4xx/5xx, False for timeouts/network errors

    def __str__(self):
        if self.is_valid:
            return f"OK: {self.url} (status={self.status_code})"
        return f"BROKEN: {self.url} - {self.error_message}"


class URLChecker:
    """URL checker with file-based caching."""

    def __init__(
        self,
        cache_ttl_hours: float = 24.0,
        timeout_seconds: float = 10.0,
        user_agent: str = "PDF-Validator/1.0 (+https://github.com/mikepsinn/disease-eradication-plan)",
        cache_file: Optional[Path] = None,
    ):
        """
        Initialize URL checker.

        Args:
            cache_ttl_hours: How long to cache results (default 24 hours)
            timeout_seconds: Request timeout (default 10 seconds)
            user_agent: User-Agent header for requests
            cache_file: Custom cache file path (default: .cache/url_check_cache.json)
        """
        self.cache_ttl_seconds = cache_ttl_hours * 3600
        self.timeout = timeout_seconds
        self.user_agent = user_agent
        self.cache_file = cache_file or URL_CACHE_FILE
        self._cache: dict = {}
        self._load_cache()

    def _load_cache(self):
        """Load cache from disk."""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self._cache = json.load(f)
        except (json.JSONDecodeError, IOError):
            self._cache = {}

    def _save_cache(self):
        """Save cache to disk."""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, indent=2)
        except IOError as e:
            print(f"[WARNING] Could not save URL cache: {e}", file=sys.stderr)

    def _is_cache_valid(self, url: str) -> bool:
        """Check if cached result is still valid."""
        if url not in self._cache:
            return False
        cached = self._cache[url]
        cached_time = cached.get("timestamp", 0)
        return (time.time() - cached_time) < self.cache_ttl_seconds

    def _get_cached(self, url: str) -> Optional[URLCheckResult]:
        """Get cached result if valid."""
        if not self._is_cache_valid(url):
            return None
        cached = self._cache[url]
        return URLCheckResult(
            url=url,
            is_valid=cached["is_valid"],
            status_code=cached.get("status_code"),
            error_message=cached.get("error_message"),
            from_cache=True,
            is_http_error=cached.get("is_http_error", False),
        )

    def _cache_result(self, result: URLCheckResult):
        """Cache a result."""
        self._cache[result.url] = {
            "is_valid": result.is_valid,
            "status_code": result.status_code,
            "error_message": result.error_message,
            "is_http_error": result.is_http_error,
            "timestamp": time.time(),
        }

    def check_url(self, url: str, skip_cache: bool = False) -> URLCheckResult:
        """
        Check if a URL is reachable.

        Args:
            url: The URL to check
            skip_cache: If True, bypass cache and make fresh request

        Returns:
            URLCheckResult with validation details
        """
        # Check cache first
        if not skip_cache:
            cached = self._get_cached(url)
            if cached:
                return cached

        # Make request
        start_time = time.time()
        try:
            req = urllib.request.Request(
                url,
                method="HEAD",
                headers={"User-Agent": self.user_agent},
            )
            response = urllib.request.urlopen(req, timeout=self.timeout)
            response_time = (time.time() - start_time) * 1000

            result = URLCheckResult(
                url=url,
                is_valid=True,
                status_code=response.status,
                response_time_ms=response_time,
            )

        except HTTPError as e:
            response_time = (time.time() - start_time) * 1000

            # Some servers don't support HEAD, try GET for 405 errors
            if e.code == 405:
                try:
                    req = urllib.request.Request(
                        url,
                        method="GET",
                        headers={"User-Agent": self.user_agent},
                    )
                    response = urllib.request.urlopen(req, timeout=self.timeout)
                    result = URLCheckResult(
                        url=url,
                        is_valid=True,
                        status_code=response.status,
                        response_time_ms=response_time,
                    )
                except HTTPError as e2:
                    result = URLCheckResult(
                        url=url,
                        is_valid=False,
                        status_code=e2.code,
                        error_message=f"HTTP {e2.code}: {e2.reason}",
                        response_time_ms=response_time,
                        is_http_error=True,  # This is a real HTTP error
                    )
                except Exception as e2:
                    result = URLCheckResult(
                        url=url,
                        is_valid=False,
                        error_message=str(e2),
                        response_time_ms=response_time,
                        is_http_error=False,  # Network error, not HTTP
                    )
            elif e.code >= 400:
                result = URLCheckResult(
                    url=url,
                    is_valid=False,
                    status_code=e.code,
                    error_message=f"HTTP {e.code}: {e.reason}",
                    response_time_ms=response_time,
                    is_http_error=True,  # This is a real HTTP error (404, 500, etc.)
                )
            else:
                # 3xx redirects that weren't followed, etc.
                result = URLCheckResult(
                    url=url,
                    is_valid=True,
                    status_code=e.code,
                    response_time_ms=response_time,
                )

        except URLError as e:
            response_time = (time.time() - start_time) * 1000
            result = URLCheckResult(
                url=url,
                is_valid=False,
                error_message=f"Connection error: {e.reason}",
                response_time_ms=response_time,
                is_http_error=False,  # Network error, not HTTP
            )

        except TimeoutError:
            response_time = (time.time() - start_time) * 1000
            result = URLCheckResult(
                url=url,
                is_valid=False,
                error_message=f"Timeout after {self.timeout}s",
                response_time_ms=response_time,
                is_http_error=False,  # Timeout, not HTTP error
            )

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            result = URLCheckResult(
                url=url,
                is_valid=False,
                error_message=str(e),
                response_time_ms=response_time,
                is_http_error=False,  # Unknown error, not HTTP
            )

        # Cache and return
        self._cache_result(result)
        return result

    def check_urls(
        self, urls: list[str], skip_cache: bool = False
    ) -> list[URLCheckResult]:
        """
        Check multiple URLs.

        Args:
            urls: List of URLs to check
            skip_cache: If True, bypass cache for all URLs

        Returns:
            List of URLCheckResult objects
        """
        results = []
        for url in urls:
            results.append(self.check_url(url, skip_cache=skip_cache))
        # Save cache after batch
        self._save_cache()
        return results

    def save(self):
        """Explicitly save cache to disk."""
        self._save_cache()

    def clear_cache(self):
        """Clear all cached results."""
        self._cache = {}
        self._save_cache()

    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        total = len(self._cache)
        valid = sum(1 for url in self._cache if self._is_cache_valid(url))
        expired = total - valid
        return {
            "total_entries": total,
            "valid_entries": valid,
            "expired_entries": expired,
            "cache_file": str(self.cache_file),
        }


# Convenience function for simple usage
_default_checker: Optional[URLChecker] = None


def check_url(
    url: str,
    timeout_seconds: float = 10.0,
    cache_ttl_hours: float = 24.0,
    skip_cache: bool = False,
) -> URLCheckResult:
    """
    Check if a URL is reachable (convenience function).

    Uses a shared checker instance for caching across calls.

    Args:
        url: The URL to check
        timeout_seconds: Request timeout
        cache_ttl_hours: How long to cache results
        skip_cache: If True, bypass cache

    Returns:
        URLCheckResult with validation details
    """
    global _default_checker
    if _default_checker is None:
        _default_checker = URLChecker(
            cache_ttl_hours=cache_ttl_hours, timeout_seconds=timeout_seconds
        )
    result = _default_checker.check_url(url, skip_cache=skip_cache)
    _default_checker.save()
    return result


if __name__ == "__main__":
    # Quick test
    print("Testing URL checker...")

    checker = URLChecker(cache_ttl_hours=1)

    test_urls = [
        "https://www.google.com",
        "https://httpstat.us/404",
        "https://nonexistent.invalid.url.test",
    ]

    for url in test_urls:
        result = checker.check_url(url)
        status = "OK" if result.is_valid else "BROKEN"
        cache_info = " (cached)" if result.from_cache else ""
        print(f"  [{status}] {url}{cache_info}")
        if not result.is_valid:
            print(f"         Error: {result.error_message}")

    checker.save()
    print(f"\nCache stats: {checker.get_cache_stats()}")
