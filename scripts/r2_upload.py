#!/usr/bin/env python3
"""Upload files to Cloudflare R2.

Uses requests + SigV4 auth directly (bypasses boto3 which hangs on some systems).

Usage:
    python scripts/r2_upload.py path/to/file.webm                    # upload, key = filename
    python scripts/r2_upload.py /abs/path/to/file.webm --key vids/demo.webm  # custom R2 key
    python scripts/r2_upload.py file1.mp3 file2.mp3                  # multiple files
    python scripts/r2_upload.py path/to/file.webm --force            # skip hash check
    python scripts/r2_upload.py path/to/file.webm --dry-run          # show what would happen

Env vars (from .env):
    R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT,
    R2_BUCKET, R2_PUBLIC_URL
"""
import sys
import os
import hashlib
import argparse
import mimetypes
import time
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))
from lib.python_utils import load_project_dotenv
load_project_dotenv(PROJECT_ROOT)

import requests
from botocore.auth import SigV4Auth
from botocore.credentials import Credentials
from botocore.awsrequest import AWSRequest

CONTENT_TYPES = {
    ".mp3": "audio/mpeg", ".m4b": "audio/mp4", ".wav": "audio/wav",
    ".xml": "application/rss+xml; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".pdf": "application/pdf", ".epub": "application/epub+zip",
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml",
    ".mp4": "video/mp4", ".webm": "video/webm",
    ".html": "text/html; charset=utf-8", ".txt": "text/plain; charset=utf-8",
}

CACHE_CONTROL = {
    ".mp3": "public, max-age=604800", ".m4b": "public, max-age=604800",
    ".pdf": "public, max-age=604800", ".epub": "public, max-age=604800",
    ".png": "public, max-age=86400", ".jpg": "public, max-age=86400",
    ".xml": "public, max-age=3600", ".json": "public, max-age=3600",
}


def content_type_for(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in CONTENT_TYPES:
        return CONTENT_TYPES[ext]
    ct, _ = mimetypes.guess_type(str(path))
    return ct or "application/octet-stream"


def cache_control_for(path: Path) -> str:
    return CACHE_CONTROL.get(path.suffix.lower(), "public, max-age=86400")


def format_size(size_bytes: int) -> str:
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024**3):.1f} GB"
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024**2):.1f} MB"
    if size_bytes >= 1024:
        return f"{size_bytes / 1024:.0f} KB"
    return f"{size_bytes} B"


class R2Client:
    """Lightweight R2 client using requests + SigV4."""

    def __init__(self):
        self.access_key = os.environ.get("R2_ACCESS_KEY_ID", "")
        self.secret_key = os.environ.get("R2_SECRET_ACCESS_KEY", "")
        self.endpoint = os.environ.get("R2_ENDPOINT", "").rstrip("/")
        self.bucket = os.environ.get("R2_BUCKET", "")
        self.public_url = os.environ.get("R2_PUBLIC_URL", "").rstrip("/")
        self.creds = Credentials(self.access_key, self.secret_key)
        self.session = requests.Session()

    def _signed_request(self, method: str, key: str, data: bytes | None = None,
                        headers: dict | None = None) -> requests.Response:
        url = f"{self.endpoint}/{self.bucket}/{key}"
        content_sha = hashlib.sha256(data or b"").hexdigest()
        h = {"x-amz-content-sha256": content_sha, "Host": self.endpoint.split("//")[1]}
        if headers:
            h.update(headers)
        aws_req = AWSRequest(method=method, url=url, headers=h, data=data)
        SigV4Auth(self.creds, "s3", "auto").add_auth(aws_req)
        return self.session.request(method, url, headers=dict(aws_req.headers),
                                    data=data, timeout=30)

    def _put_object(self, key: str, data: bytes, content_type: str,
                    cache_control: str) -> requests.Response:
        """PUT a complete object (data must fit in memory)."""
        url = f"{self.endpoint}/{self.bucket}/{key}"
        content_sha = hashlib.sha256(data).hexdigest()
        h = {
            "x-amz-content-sha256": content_sha,
            "Host": self.endpoint.split("//")[1],
            "Content-Type": content_type,
            "Cache-Control": cache_control,
            "Content-Length": str(len(data)),
        }
        aws_req = AWSRequest(method="PUT", url=url, headers=h, data=data)
        SigV4Auth(self.creds, "s3", "auto").add_auth(aws_req)
        return self.session.put(url, headers=dict(aws_req.headers), data=data, timeout=120)

    def _multipart_upload(self, key: str, file_path: Path, content_type: str,
                          cache_control: str, on_progress=None) -> bool:
        """Upload a large file using S3 multipart upload."""
        import xml.etree.ElementTree as ET
        CHUNK = 10 * 1024 * 1024  # 10MB parts
        file_size = file_path.stat().st_size
        host = self.endpoint.split("//")[1]

        # Step 1: Initiate multipart upload
        url = f"{self.endpoint}/{self.bucket}/{key}?uploads"
        content_sha = hashlib.sha256(b"").hexdigest()
        h = {
            "x-amz-content-sha256": content_sha,
            "Host": host,
            "Content-Type": content_type,
            "Cache-Control": cache_control,
        }
        aws_req = AWSRequest(method="POST", url=url, headers=h)
        SigV4Auth(self.creds, "s3", "auto").add_auth(aws_req)
        resp = self.session.post(url, headers=dict(aws_req.headers), timeout=30)
        if resp.status_code != 200:
            print(f"    Initiate multipart failed: HTTP {resp.status_code} {resp.text[:200]}")
            return False

        root = ET.fromstring(resp.text)
        ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
        upload_id = root.findtext("s3:UploadId", namespaces=ns)
        if not upload_id:
            upload_id = root.findtext("UploadId")
        if not upload_id:
            print(f"    No UploadId in response: {resp.text[:300]}")
            return False

        # Step 2: Upload parts
        etags: list[tuple[int, str]] = []
        uploaded_bytes = 0
        part_num = 0

        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(CHUNK)
                if not chunk:
                    break
                part_num += 1
                chunk_sha = hashlib.sha256(chunk).hexdigest()
                part_url = f"{self.endpoint}/{self.bucket}/{key}?partNumber={part_num}&uploadId={upload_id}"
                ph = {
                    "x-amz-content-sha256": chunk_sha,
                    "Host": host,
                    "Content-Length": str(len(chunk)),
                }
                aws_req = AWSRequest(method="PUT", url=part_url, headers=ph, data=chunk)
                SigV4Auth(self.creds, "s3", "auto").add_auth(aws_req)
                part_resp = self.session.put(part_url, headers=dict(aws_req.headers),
                                             data=chunk, timeout=120)
                if part_resp.status_code != 200:
                    print(f"    Part {part_num} failed: HTTP {part_resp.status_code}")
                    self._abort_multipart(key, upload_id)
                    return False

                etag = part_resp.headers.get("ETag", "").strip('"')
                etags.append((part_num, etag))
                uploaded_bytes += len(chunk)
                if on_progress:
                    on_progress(uploaded_bytes, file_size)

        # Step 3: Complete multipart upload
        parts_xml = "".join(
            f"<Part><PartNumber>{pn}</PartNumber><ETag>{et}</ETag></Part>"
            for pn, et in etags
        )
        complete_body = f"<CompleteMultipartUpload>{parts_xml}</CompleteMultipartUpload>".encode()
        complete_url = f"{self.endpoint}/{self.bucket}/{key}?uploadId={upload_id}"
        complete_sha = hashlib.sha256(complete_body).hexdigest()
        ch = {
            "x-amz-content-sha256": complete_sha,
            "Host": host,
            "Content-Type": "application/xml",
        }
        aws_req = AWSRequest(method="POST", url=complete_url, headers=ch, data=complete_body)
        SigV4Auth(self.creds, "s3", "auto").add_auth(aws_req)
        resp = self.session.post(complete_url, headers=dict(aws_req.headers),
                                 data=complete_body, timeout=60)
        if resp.status_code != 200:
            print(f"    Complete multipart failed: HTTP {resp.status_code} {resp.text[:200]}")
            return False
        return True

    def _abort_multipart(self, key: str, upload_id: str):
        url = f"{self.endpoint}/{self.bucket}/{key}?uploadId={upload_id}"
        content_sha = hashlib.sha256(b"").hexdigest()
        h = {"x-amz-content-sha256": content_sha, "Host": self.endpoint.split("//")[1]}
        aws_req = AWSRequest(method="DELETE", url=url, headers=h)
        SigV4Auth(self.creds, "s3", "auto").add_auth(aws_req)
        self.session.delete(url, headers=dict(aws_req.headers), timeout=10)

    def validate(self):
        """Check credentials and bucket access. Crash if anything is wrong."""
        print("[*] Validating R2 credentials...")
        missing = []
        if not self.access_key:
            missing.append("R2_ACCESS_KEY_ID")
        if not self.secret_key:
            missing.append("R2_SECRET_ACCESS_KEY")
        if not self.endpoint:
            missing.append("R2_ENDPOINT")
        if not self.bucket:
            missing.append("R2_BUCKET")
        if missing:
            print(f"[FATAL] Missing env vars: {', '.join(missing)}")
            sys.exit(1)

        print(f"  Endpoint: {self.endpoint}")
        print(f"  Bucket:   {self.bucket}")
        print(f"  Key ID:   {self.access_key[:8]}...")

        # Test with a lightweight list call
        url = f"{self.endpoint}/{self.bucket}?list-type=2&max-keys=1"
        content_sha = hashlib.sha256(b"").hexdigest()
        h = {"x-amz-content-sha256": content_sha, "Host": self.endpoint.split("//")[1]}
        aws_req = AWSRequest(method="GET", url=url, headers=h)
        SigV4Auth(self.creds, "s3", "auto").add_auth(aws_req)

        resp = self.session.get(url, headers=dict(aws_req.headers), timeout=10)
        if resp.status_code != 200:
            print(f"[FATAL] Bucket check failed: HTTP {resp.status_code}")
            print(f"  {resp.text[:200]}")
            sys.exit(1)
        print("[OK] Bucket accessible.\n")

    def head_object(self, key: str) -> str | None:
        """Get ETag for a remote object, or None if it doesn't exist."""
        url = f"{self.endpoint}/{self.bucket}/{key}"
        content_sha = hashlib.sha256(b"").hexdigest()
        h = {"x-amz-content-sha256": content_sha, "Host": self.endpoint.split("//")[1]}
        aws_req = AWSRequest(method="HEAD", url=url, headers=h)
        SigV4Auth(self.creds, "s3", "auto").add_auth(aws_req)

        resp = self.session.head(url, headers=dict(aws_req.headers), timeout=10)
        if resp.status_code == 404:
            return None
        if resp.status_code == 200:
            return resp.headers.get("ETag", "").strip('"')
        return None

    def upload_file(self, local_path: Path, key: str, force: bool = False,
                    dry_run: bool = False) -> bool:
        """Upload a single file. Returns True on success."""
        if not local_path.exists():
            print(f"  [ERROR] File not found: {local_path}")
            return False

        size = local_path.stat().st_size
        ct = content_type_for(local_path)
        cc = cache_control_for(local_path)

        print(f"  File: {local_path.name} ({format_size(size)}, {ct})")
        print(f"  Key:  {key}")

        if not force:
            print(f"  Checking remote hash...", end=" ", flush=True)
            remote_etag = self.head_object(key)
            if remote_etag:
                local_md5 = hashlib.md5(local_path.read_bytes()).hexdigest()
                if local_md5 == remote_etag:
                    print("match - skipping.")
                    return True
                print("changed.")
            else:
                print("new file.")

        if dry_run:
            print(f"  [DRY-RUN] Would upload {format_size(size)}")
            return True

        print(f"  Uploading...", flush=True)
        last_print = [0.0]

        def progress(uploaded, total):
            now = time.monotonic()
            if now - last_print[0] < 0.5 and uploaded < total:
                return
            last_print[0] = now
            pct = uploaded / total * 100 if total else 100
            print(f"    {format_size(uploaded)} / {format_size(total)} ({pct:.0f}%)",
                  flush=True)

        MULTIPART_THRESHOLD = 10 * 1024 * 1024  # 10MB

        if size > MULTIPART_THRESHOLD:
            ok = self._multipart_upload(key, local_path, ct, cc,
                                        on_progress=progress)
            if ok:
                print(f"  [OK] Uploaded.")
            return ok
        else:
            data = local_path.read_bytes()
            resp = self._put_object(key, data, ct, cc)
            if resp.status_code in (200, 201):
                print(f"  [OK] Uploaded.")
                return True
            else:
                print(f"  [FAILED] HTTP {resp.status_code}: {resp.text[:200]}")
                return False


def main():
    parser = argparse.ArgumentParser(description="Upload files to Cloudflare R2")
    parser.add_argument("files", nargs="+", help="Local file(s) to upload")
    parser.add_argument("--key", "-k", help="R2 object key (only valid with a single file)")
    parser.add_argument("--force", "-f", action="store_true", help="Upload even if unchanged")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show what would happen")
    args = parser.parse_args()

    if args.key and len(args.files) > 1:
        print("ERROR: --key can only be used with a single file")
        sys.exit(1)

    r2 = R2Client()
    r2.validate()

    t0 = time.monotonic()
    uploaded = 0
    errors = 0

    for filepath in args.files:
        local_path = Path(filepath).resolve()
        key = args.key if args.key else local_path.name

        try:
            ok = r2.upload_file(local_path, key, force=args.force, dry_run=args.dry_run)
            if ok:
                uploaded += 1
            else:
                errors += 1
        except Exception as e:
            print(f"  [FAILED] {key}: {e}")
            errors += 1

    elapsed = time.monotonic() - t0
    print(f"\nDone: {uploaded} uploaded, {errors} errors ({elapsed:.1f}s)")

    if uploaded and r2.public_url and not args.dry_run:
        print(f"\nPublic URLs:")
        for filepath in args.files:
            local_path = Path(filepath).resolve()
            key = args.key if args.key else local_path.name
            print(f"  {r2.public_url}/{key}")


if __name__ == "__main__":
    main()
