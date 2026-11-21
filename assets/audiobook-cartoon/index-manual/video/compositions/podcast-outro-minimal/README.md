# Podcast Outro (Minimalist Flat Design)

A 59.5-second minimalist alternative to the Part 27 cut-out collage outro. Navy background, cream and orange kinetic typography, Wishonia as the only character. Syncs to the podcast outro audio.

## Files

| File | Description |
|------|-------------|
| `source.html` | Composition source (GSAP timeline + scenes, `__CAPTIONS__` placeholder) |
| `captions.json` | Word timings for lip-sync and captions |
| `index.html` | Built composition (captions inlined, ready to render) |

## Setup

The composition uses symlinks to reference existing repo assets without duplication:

```
assets/
  fonts/      -> ../../../assets/fonts/
  vendor/     -> ../../../assets/vendor/
  sprites/alien/ -> ../../../../../../../../transmit/public/assets/sprites/alien/
  podcast-outro.wav  (downloaded, gitignored)
```

Download the audio before rendering:

```bash
cd assets/audiobook-cartoon/index-manual/video/compositions/podcast-outro-minimal
curl -o assets/podcast-outro.wav "https://static.warondisease.org/assets/audiobook/manual-paperback/wavs/podcast-outro.wav"
```

## Rendering

Requires Node 22+ and the HyperFrames CLI.

```bash
cd assets/audiobook-cartoon/index-manual/video/compositions/podcast-outro-minimal

# Install chrome-headless-shell (once):
npx @puppeteer/browsers install chrome-headless-shell@158.0.8127.36

# Check the composition
npx hyperframes check .

# Snapshot frames to verify assets resolve
npx hyperframes snapshot . --at 5,30,55 --describe false

# Render at high quality
npx hyperframes render . --quality high --output podcast-outro-minimal.mp4
```

## Design Notes

- **Style**: Navy radial gradient (#061530 to #17345C), cream text (#F3ECD0), orange accents (#E5903B)
- **Typography**: Oswald (headlines), Inter (body), Fraunces (URL)
- **Motion**: GSAP pop/slam/rise vocabulary, word-by-word captions
- **Character**: Wishonia with lip-sync from word timings, idle head rock and blink
