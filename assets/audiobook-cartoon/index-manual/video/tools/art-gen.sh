#!/usr/bin/env bash
# Generate one art sheet with Codex's image generation (free on the ChatGPT plan), for the few things the kit does
# not draw in code (AGENTS.md, Generated art). Cut the sheet up with tools/art-cutout.py.
#
#   tools/art-gen.sh <out.png> "<what to draw>" [reference image ...]
#
# References: the character's approved sheets (assets/art/<name>/sheets/) keep it the same character; for a new
# one, the theme song keyframes (E:/eos/manual/assets/music-video/keyframes/scene-NN.jpg) set the look. Each run
# makes one 1536 x 1024 image with its pieces apart on flat magenta. Codex's Windows sandbox cannot save files,
# so the image is copied out of ~/.codex/generated_images/<session id>/.
set -euo pipefail
out="$1"; what="$2"; shift 2
refs=()
for r in "$@"; do refs+=(-i "$r"); done
# ART_STYLE replaces the look (the default is the film's flat 1950s print look).
style="Keep any character in the attached images exactly (the same face, clothes, colors and line weight). ${ART_STYLE:-Draw in the flat 1950s print look of the cartoon: bold navy outlines, halftone texture, the navy, orange, cream, rust, tan and mustard palette, no gradients, no 3D.}"
log="${out%.*}.log"
# ART_PLATE=1 makes a full-frame background instead of a sheet of pieces on magenta.
if [ -n "${ART_PLATE:-}" ]; then
  layout="It fills the whole frame edge to edge, with no border, no text and no labels."
else
  layout="Every piece on one flat solid magenta (#FF00FF) background, with wide magenta gaps so no two pieces touch, no shadows, no scenery, no text, no labels."
fi
printf '%s\n' "Use your image generation tool to make one wide image (1536x1024). $style The image: $what $layout Do not create or edit any files. Reply with the image only." |
  timeout 600 codex exec --skip-git-repo-check -s read-only -C "$(dirname "$out")" ${refs[@]+"${refs[@]}"} - > "$log" 2>&1
sid=$(grep -o "session id: .*" "$log" | cut -d' ' -f3)
png=$(ls -t "$HOME/.codex/generated_images/$sid"/*.png 2>/dev/null | head -1 || true)
if [ -z "$png" ]; then echo "no image; see $log" >&2; exit 1; fi
cp "$png" "$out"
echo "$out"
