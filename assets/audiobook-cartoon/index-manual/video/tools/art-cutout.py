"""Cut a generated art sheet (pieces on flat magenta, #FF00FF) into transparent WebP files, one per piece.

    python -I tools/art-cutout.py <sheet.png> <out dir> <name> [<name> ...]

Pieces are found as separate blobs and named in reading order: left to right by column, then top to bottom
within a column. Pass one name per piece ("-" skips a piece); an existing file is never replaced without --force. Each piece's box on the sheet is printed as
JSON, so the kit can place pieces drawn at the same scale relative to each other.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

sheet, out_dir, names = sys.argv[1], Path(sys.argv[2]), [a for a in sys.argv[3:] if a != "--force"]
rgb = np.asarray(Image.open(sheet).convert("RGB")).astype(np.float32) / 255
r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
# Alpha from how magenta each pixel is, and the magenta un-mixed from the soft edge pixels.
key = np.clip(np.minimum(r, b) - g, 0, 1)
alpha = 1 - np.clip((key - 0.18) / 0.5, 0, 1)
a = np.maximum(alpha, 1e-3)[..., None]
fg = np.clip((rgb - (1 - a) * np.array([1.0, 0.0, 1.0], dtype=np.float32)) / a, 0, 1)
rgba = np.dstack([fg, alpha])

# A piece is a blob of solid art (grown by 2 px, so pieces standing close stay apart); a loose speck (a bubble, a
# puff) joins the piece whose box, widened by 40 px, holds its middle.
labels, count = ndimage.label(ndimage.binary_dilation(alpha > 0.5, iterations=2))
sizes = ndimage.sum(np.ones_like(alpha), labels, range(1, count + 1))
big = [i + 1 for i, s in enumerate(sizes) if s > 3000]
found = ndimage.find_objects(labels)
for i, s in enumerate(sizes):
    if s > 3000 or found[i] is None:
        continue
    cy, cx = [(sl.start + sl.stop) / 2 for sl in found[i]]
    for k in big:
        by, bx = found[k - 1]
        if bx.start - 40 <= cx <= bx.stop + 40 and by.start - 40 <= cy <= by.stop + 40:
            labels[labels == i + 1] = k
            break
# Pieces that touch (a hand on the next one's sleeve): while there are fewer pieces than names, split the widest at
# its thinnest column, away from its edges.
while len(big) < len(names):
    widths = {k: np.ptp(np.nonzero(labels == k)[1]) for k in big}
    k = max(widths, key=lambda kk: widths[kk])
    xs = np.nonzero(labels == k)[1]
    x0, x1 = xs.min(), xs.max()
    cols = (labels[:, x0:x1 + 1] == k).sum(axis=0)
    lo, hi = int(len(cols) * 0.2), int(len(cols) * 0.8)
    cut = x0 + lo + int(np.argmin(cols[lo:hi]))
    new = labels.max() + 1
    right = (labels == k) & (np.arange(labels.shape[1])[None, :] > cut)
    labels[right] = new
    big.append(new)
boxes = []
for k in big:
    ys, xs = np.nonzero(labels == k)
    boxes.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), k))
boxes.sort(key=lambda bx: (round(bx[0] / 120), bx[1]))
if len(boxes) != len(names):
    raise SystemExit(f"{len(boxes)} pieces on the sheet but {len(names)} names")

out_dir.mkdir(parents=True, exist_ok=True)
taken = [n for n in names if n != "-" and (out_dir / f"{n}.webp").exists()]
if taken and "--force" not in sys.argv:
    raise SystemExit("already exist (pick other names, or pass --force to replace): " + ", ".join(taken))
placed = {}
for name, (x0, y0, x1, y1, k) in zip(names, boxes):
    if name == "-":
        continue
    piece = rgba[y0:y1 + 1, x0:x1 + 1].copy()
    piece[..., 3] *= labels[y0:y1 + 1, x0:x1 + 1] == k
    Image.fromarray((piece * 255).round().astype(np.uint8), "RGBA").save(out_dir / f"{name}.webp", "WEBP", quality=90, method=6)
    placed[name] = {"x": x0, "y": y0, "w": x1 - x0 + 1, "h": y1 - y0 + 1}
print(json.dumps(placed))
# Cut-outs for KIT.collage: refresh assets/js/art-sizes.js.
if out_dir.resolve() == (Path(__file__).resolve().parent.parent / "assets" / "art" / "collage").resolve():
    import subprocess
    subprocess.run([sys.executable, "-I", str(Path(__file__).with_name("art-sizes.py"))], check=True)
