"""Cut a generated art sheet (pieces on flat magenta, #FF00FF) into transparent WebP files, one per piece.

    python -I tools/art-cutout.py <sheet.png> <out dir> <name> [<name> ...]

Pieces are found as separate blobs and named in reading order: left to right by column, then top to bottom
within a column. Pass one name per piece ("-" skips a piece). Each piece's box on the sheet is printed as
JSON, so the kit can place pieces drawn at the same scale relative to each other.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

sheet, out_dir, names = sys.argv[1], Path(sys.argv[2]), sys.argv[3:]
rgb = np.asarray(Image.open(sheet).convert("RGB")).astype(np.float32) / 255
r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
# Alpha from how magenta each pixel is, and the magenta un-mixed from the soft edge pixels.
key = np.clip(np.minimum(r, b) - g, 0, 1)
alpha = 1 - np.clip((key - 0.18) / 0.5, 0, 1)
a = np.maximum(alpha, 1e-3)[..., None]
fg = np.clip((rgb - (1 - a) * np.array([1.0, 0.0, 1.0], dtype=np.float32)) / a, 0, 1)
rgba = np.dstack([fg, alpha])

# A piece is a blob of solid art, grown a little so its loose specks join it.
labels, count = ndimage.label(ndimage.binary_dilation(alpha > 0.5, iterations=6))
sizes = ndimage.sum(np.ones_like(alpha), labels, range(1, count + 1))
boxes = []
for k in [i + 1 for i, s in enumerate(sizes) if s > 3000]:
    ys, xs = np.nonzero(labels == k)
    boxes.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), k))
boxes.sort(key=lambda bx: (round(bx[0] / 120), bx[1]))
if len(boxes) != len(names):
    raise SystemExit(f"{len(boxes)} pieces on the sheet but {len(names)} names")

out_dir.mkdir(parents=True, exist_ok=True)
placed = {}
for name, (x0, y0, x1, y1, k) in zip(names, boxes):
    if name == "-":
        continue
    piece = rgba[y0:y1 + 1, x0:x1 + 1].copy()
    piece[..., 3] *= labels[y0:y1 + 1, x0:x1 + 1] == k
    Image.fromarray((piece * 255).round().astype(np.uint8), "RGBA").save(out_dir / f"{name}.webp", "WEBP", quality=90, method=6)
    placed[name] = {"x": x0, "y": y0, "w": x1 - x0 + 1, "h": y1 - y0 + 1}
print(json.dumps(placed))
