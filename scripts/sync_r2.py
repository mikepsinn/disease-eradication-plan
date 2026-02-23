#!/usr/bin/env python3
"""Sync static assets and audiobook files to Cloudflare R2.

Efficiently uploads files to R2 (S3-compatible), comparing MD5 hashes
to skip unchanged files. Sets correct Content-Type and Cache-Control headers.

Reads .r2ignore for exclusion patterns (gitignore-style syntax).

Usage:
    python scripts/sync_r2.py                          # sync all (assets + audiobook)
    python scripts/sync_r2.py --dir audiobook           # sync audiobook only
    python scripts/sync_r2.py --dir assets              # sync assets only
    python scripts/sync_r2.py --dry-run                 # show what would upload
    python scripts/sync_r2.py --list                    # show remote files
    python scripts/sync_r2.py --delete-removed          # remove orphaned remote files

Env vars (in .env):
    R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT,
    R2_BUCKET, R2_PUBLIC_URL
"""
import sys
import os
import hashlib
import argparse
import fnmatch
import mimetypes
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))
from lib.python_utils import load_project_dotenv
load_project_dotenv(PROJECT_ROOT)

# Directories to sync (R2 prefix -> local path)
SYNC_DIRS = {
    "assets": PROJECT_ROOT / "assets",
}

# Content-Type overrides
CONTENT_TYPES = {
    ".mp3": "audio/mpeg",
    ".m4b": "audio/mp4",
    ".wav": "audio/wav",
    ".vtt": "text/vtt; charset=utf-8",
    ".srt": "text/srt; charset=utf-8",
    ".xml": "application/rss+xml; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".pdf": "application/pdf",
    ".epub": "application/epub+zip",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".html": "text/html; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
}

# Cache durations by file type
CACHE_CONTROL = {
    ".mp3": "public, max-age=604800",     # 1 week
    ".m4b": "public, max-age=604800",
    ".pdf": "public, max-age=604800",
    ".epub": "public, max-age=604800",
    ".png": "public, max-age=86400",       # 1 day
    ".jpg": "public, max-age=86400",
    ".jpeg": "public, max-age=86400",
    ".xml": "public, max-age=3600",        # 1 hour (RSS)
    ".json": "public, max-age=3600",
}
DEFAULT_CACHE = "public, max-age=86400"


def load_r2ignore() -> list[str]:
    """Load .r2ignore patterns from project root."""
    ignore_file = PROJECT_ROOT / ".r2ignore"
    if not ignore_file.exists():
        return []
    patterns = []
    for line in ignore_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def is_ignored(rel_path: str, patterns: list[str]) -> bool:
    """Check if a relative path matches any .r2ignore pattern.

    Supports:
    - *.ext         -> matches extension anywhere
    - dirname/      -> matches directory name in any position
    - path/to/file  -> matches exact relative path prefix
    """
    rel_posix = rel_path.replace("\\", "/")
    parts = rel_posix.split("/")

    for pattern in patterns:
        # Directory pattern (trailing slash): match any path component
        if pattern.endswith("/"):
            dirname = pattern.rstrip("/")
            if dirname in parts[:-1]:  # Check parent dirs only
                return True
            continue

        # Extension pattern: *.ext
        if pattern.startswith("*."):
            if rel_posix.endswith(pattern[1:]):
                return True
            continue

        # Exact filename match
        filename = parts[-1]
        if fnmatch.fnmatch(filename, pattern):
            return True

        # Path prefix match
        if fnmatch.fnmatch(rel_posix, pattern):
            return True

    return False


def get_r2_client():
    import boto3

    access_key = os.environ.get("R2_ACCESS_KEY_ID") or os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("R2_SECRET_ACCESS_KEY") or os.environ.get("AWS_SECRET_ACCESS_KEY")
    endpoint = os.environ.get("R2_ENDPOINT")

    if not all([access_key, secret_key, endpoint]):
        print("ERROR: Missing R2 credentials. Set in .env:")
        print("  R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT")
        sys.exit(1)

    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )


def get_bucket():
    bucket = os.environ.get("R2_BUCKET")
    if not bucket:
        print("ERROR: R2_BUCKET not set in .env")
        sys.exit(1)
    return bucket


def get_public_url():
    return os.environ.get("R2_PUBLIC_URL", "").rstrip("/")


def md5_file(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def content_type_for(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in CONTENT_TYPES:
        return CONTENT_TYPES[ext]
    ct, _ = mimetypes.guess_type(str(path))
    return ct or "application/octet-stream"


def cache_control_for(path: Path) -> str:
    return CACHE_CONTROL.get(path.suffix.lower(), DEFAULT_CACHE)


def collect_files(prefix: str, local_root: Path, patterns: list[str]) -> dict[str, Path]:
    """Collect local files to sync, keyed by R2 object key."""
    if not local_root.exists():
        return {}

    files = {}
    for f in local_root.rglob("*"):
        if not f.is_file():
            continue
        rel = f.relative_to(local_root).as_posix()
        if is_ignored(rel, patterns):
            continue
        key = f"{prefix}/{rel}"
        files[key] = f

    return files


def list_remote_objects(client, bucket: str, prefix: str) -> dict[str, str]:
    remote = {}
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            etag = obj["ETag"].strip('"')
            remote[obj["Key"]] = etag
    return remote


def format_size(size_bytes: int) -> str:
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024**3):.1f} GB"
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024**2):.1f} MB"
    if size_bytes >= 1024:
        return f"{size_bytes / 1024:.0f} KB"
    return f"{size_bytes} B"


def sync_dir(prefix: str, local_root: Path, patterns: list[str],
             dry_run: bool, delete_removed: bool):
    client = get_r2_client()
    bucket = get_bucket()
    public_url = get_public_url()

    print(f"\n{'='*60}")
    print(f"Syncing: {prefix}/")
    print(f"Local:   {local_root}")
    if public_url:
        print(f"URL:     {public_url}/{prefix}/")
    print()

    local_files = collect_files(prefix, local_root, patterns)
    if not local_files:
        print(f"No files to sync in {prefix}/")
        return

    print(f"Found {len(local_files)} local files. Checking remote state...")
    remote_objects = list_remote_objects(client, bucket, f"{prefix}/")

    uploaded = 0
    skipped = 0
    deleted = 0
    errors = 0
    upload_bytes = 0

    for key, local_path in sorted(local_files.items()):
        local_md5 = md5_file(local_path)
        remote_etag = remote_objects.get(key)
        size = local_path.stat().st_size

        if remote_etag == local_md5:
            skipped += 1
            continue

        action = "NEW" if remote_etag is None else "UPDATE"
        ct = content_type_for(local_path)

        if dry_run:
            print(f"  [{action}] {key} ({format_size(size)}, {ct})")
            uploaded += 1
            upload_bytes += size
            continue

        print(f"  [{action}] {key} ({format_size(size)})...", end="", flush=True)
        try:
            client.upload_file(
                str(local_path),
                bucket,
                key,
                ExtraArgs={
                    "ContentType": ct,
                    "CacheControl": cache_control_for(local_path),
                },
            )
            print(" OK")
            uploaded += 1
            upload_bytes += size
        except Exception as e:
            print(f" FAILED: {e}")
            errors += 1

    if delete_removed:
        for key in sorted(remote_objects):
            if key not in local_files:
                if dry_run:
                    print(f"  [DELETE] {key}")
                else:
                    print(f"  [DELETE] {key}...", end="", flush=True)
                    try:
                        client.delete_object(Bucket=bucket, Key=key)
                        print(" OK")
                    except Exception as e:
                        print(f" FAILED: {e}")
                        errors += 1
                deleted += 1

    verb = "would upload" if dry_run else "uploaded"
    print(f"\n  {uploaded} {verb} ({format_size(upload_bytes)}), "
          f"{skipped} unchanged, {deleted} deleted, {errors} errors")


def list_remote(dirs: list[str]):
    client = get_r2_client()
    bucket = get_bucket()
    public_url = get_public_url()

    for prefix in dirs:
        remote = list_remote_objects(client, bucket, f"{prefix}/")
        if not remote:
            print(f"\nNo files under {prefix}/")
            continue

        print(f"\n{prefix}/ ({len(remote)} files):")
        total_size = 0
        for key in sorted(remote):
            head = client.head_object(Bucket=bucket, Key=key)
            size = head["ContentLength"]
            total_size += size
            url = f"{public_url}/{key}" if public_url else key
            print(f"  {format_size(size):>10}  {url}")

        print(f"  {'':>10}  Total: {format_size(total_size)}")


def generate_index_and_sitemap(all_files: dict[str, Path], dry_run: bool):
    """Generate index.html and sitemap.xml, upload to R2 root."""
    public_url = get_public_url()
    if not public_url:
        return

    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Build file entries with metadata
    entries = []
    for key in sorted(all_files):
        path = all_files[key]
        size = path.stat().st_size
        ext = path.suffix.lower()
        entries.append({
            "key": key,
            "url": f"{public_url}/{key}",
            "size": size,
            "size_str": format_size(size),
            "ext": ext.lstrip("."),
            "type": ext.lstrip(".").upper() or "FILE",
        })

    total_size = sum(e["size"] for e in entries)

    # --- index.html ---
    import json as json_mod
    entries_json = json_mod.dumps([
        {"key": e["key"], "url": e["url"], "size_str": e["size_str"],
         "ext": e["ext"], "type": e["type"]}
        for e in entries
    ])

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Static Assets - War on Disease</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         max-width: 1200px; margin: 0 auto; padding: 20px; background: #f8f9fa; }}
  h1 {{ margin-bottom: 8px; }}
  .meta {{ color: #666; margin-bottom: 16px; }}
  .controls {{ display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }}
  input[type=search] {{ flex: 1; min-width: 200px; padding: 8px 12px; border: 1px solid #ddd;
                        border-radius: 6px; font-size: 14px; }}
  .filter-btn {{ padding: 6px 12px; border: 1px solid #ddd; border-radius: 16px;
                 background: white; cursor: pointer; font-size: 13px; }}
  .filter-btn.active {{ background: #0066cc; color: white; border-color: #0066cc; }}
  table {{ width: 100%; border-collapse: collapse; background: white;
           border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,.1); }}
  th {{ text-align: left; padding: 10px 12px; background: #f1f3f5; font-size: 13px;
       color: #495057; border-bottom: 2px solid #dee2e6; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #f1f3f5; font-size: 13px; }}
  tr:hover td {{ background: #f8f9fa; }}
  a {{ color: #0066cc; text-decoration: none; word-break: break-all; }}
  a:hover {{ text-decoration: underline; }}
  .size {{ white-space: nowrap; text-align: right; color: #666; }}
  .type {{ display: inline-block; padding: 2px 8px; border-radius: 4px;
           font-size: 11px; font-weight: 600; background: #e9ecef; }}
  .type-mp3 {{ background: #d4edda; color: #155724; }}
  .type-pdf {{ background: #f8d7da; color: #721c24; }}
  .type-png, .type-jpg, .type-jpeg, .type-webp {{ background: #cce5ff; color: #004085; }}
  .type-vtt, .type-srt {{ background: #fff3cd; color: #856404; }}
  .type-xml, .type-json {{ background: #e2e3e5; color: #383d41; }}
  .count {{ color: #666; font-size: 13px; }}
  #no-results {{ display: none; padding: 40px; text-align: center; color: #999; }}
</style>
</head>
<body>
<h1>Static Assets</h1>
<p class="meta">{len(entries)} files, {format_size(total_size)} total.
Updated {today}.</p>
<div class="controls">
  <input type="search" id="search" placeholder="Filter files..." autofocus>
  <button class="filter-btn active" data-ext="all">All</button>
</div>
<table>
<thead><tr><th>File</th><th>Type</th><th class="size">Size</th></tr></thead>
<tbody id="files"></tbody>
</table>
<div id="no-results">No files match your filter.</div>
<script>
const FILES = {entries_json};
const tbody = document.getElementById('files');
const search = document.getElementById('search');
const noResults = document.getElementById('no-results');
const controls = document.querySelector('.controls');

// Discover unique extensions for filter buttons
const exts = [...new Set(FILES.map(f => f.ext))].filter(Boolean).sort();
exts.forEach(ext => {{
  const btn = document.createElement('button');
  btn.className = 'filter-btn';
  btn.dataset.ext = ext;
  btn.textContent = ext.toUpperCase();
  controls.appendChild(btn);
}});

let activeExt = 'all';
controls.addEventListener('click', e => {{
  if (!e.target.classList.contains('filter-btn')) return;
  controls.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  e.target.classList.add('active');
  activeExt = e.target.dataset.ext;
  render();
}});
search.addEventListener('input', render);

function render() {{
  const q = search.value.toLowerCase();
  const filtered = FILES.filter(f => {{
    if (activeExt !== 'all' && f.ext !== activeExt) return false;
    if (q && !f.key.toLowerCase().includes(q)) return false;
    return true;
  }});
  tbody.innerHTML = filtered.map(f =>
    `<tr><td><a href="${{f.url}}">${{f.key}}</a></td>` +
    `<td><span class="type type-${{f.ext}}">${{f.type}}</span></td>` +
    `<td class="size">${{f.size_str}}</td></tr>`
  ).join('');
  noResults.style.display = filtered.length ? 'none' : 'block';
  document.querySelector('.count')?.remove();
  const count = document.createElement('span');
  count.className = 'count';
  count.textContent = ` Showing ${{filtered.length}} of ${{FILES.length}}`;
  document.querySelector('.meta').appendChild(count);
}}
render();
</script>
</body>
</html>"""

    # --- sitemap.xml ---
    sitemap_entries = "\n".join(
        f"  <url><loc>{public_url}/{e['key']}</loc><lastmod>{today}</lastmod></url>"
        for e in entries
    )
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_entries}
</urlset>"""

    if dry_run:
        print(f"\n  [DRY-RUN] Would generate index.html ({len(entries)} files)")
        print(f"  [DRY-RUN] Would generate sitemap.xml ({len(entries)} URLs)")
        return

    # Write temp files and upload
    client = get_r2_client()
    bucket = get_bucket()
    import tempfile

    for filename, content, ct in [
        ("index.html", index_html, "text/html; charset=utf-8"),
        ("sitemap.xml", sitemap_xml, "application/xml; charset=utf-8"),
    ]:
        tmp = Path(tempfile.mktemp(suffix=f"_{filename}"))
        tmp.write_text(content, encoding="utf-8")
        print(f"  Uploading {filename} ({format_size(tmp.stat().st_size)})...", end="", flush=True)
        try:
            client.upload_file(
                str(tmp), bucket, filename,
                ExtraArgs={
                    "ContentType": ct,
                    "CacheControl": "public, max-age=3600",
                },
            )
            print(" OK")
        except Exception as e:
            print(f" FAILED: {e}")
        finally:
            tmp.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Sync static assets to Cloudflare R2")
    parser.add_argument("--dir", choices=list(SYNC_DIRS.keys()), action="append",
                        help="Directory to sync (default: all). Can be repeated.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be uploaded")
    parser.add_argument("--list", action="store_true", help="List files currently on R2")
    parser.add_argument("--delete-removed", action="store_true",
                        help="Delete remote files not found locally")
    parser.add_argument("--no-index", action="store_true",
                        help="Skip generating index.html and sitemap.xml")
    args = parser.parse_args()

    dirs = args.dir or list(SYNC_DIRS.keys())
    patterns = load_r2ignore()

    if patterns:
        print(f"Loaded {len(patterns)} patterns from .r2ignore")

    if args.list:
        list_remote(dirs)
        return

    # Collect all files across dirs for index generation
    all_files: dict[str, Path] = {}
    for d in dirs:
        sync_dir(d, SYNC_DIRS[d], patterns, dry_run=args.dry_run,
                 delete_removed=args.delete_removed)
        all_files.update(collect_files(d, SYNC_DIRS[d], patterns))

    # Generate index.html and sitemap.xml
    if not args.no_index:
        print(f"\n{'='*60}")
        print("Generating index.html and sitemap.xml...")
        generate_index_and_sitemap(all_files, dry_run=args.dry_run)

    print(f"\n{'='*60}")
    print("Sync complete.")


if __name__ == "__main__":
    main()
