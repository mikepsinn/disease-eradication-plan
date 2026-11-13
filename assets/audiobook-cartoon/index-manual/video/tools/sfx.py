"""Synthesize the cartoon's sound effects as WAV files, so the project needs no sound library.

    python tools/sfx.py <out dir>

Each effect is a few lines of numpy (tones, sweeps, filtered noise, envelopes). The part files
place them on spoken words (tools/build-part.mjs, "sounds").
"""
import sys
import wave
from pathlib import Path

import numpy as np

SR = 44100
rng = np.random.default_rng(7)


def ns(d):
    """Samples in d seconds, rounded the same way everywhere."""
    return int(round(SR * d))


def t(d):
    return np.arange(ns(d)) / SR


def env(n, attack=0.005, decay=8.0):
    x = np.arange(n) / SR
    return np.minimum(1, x / attack) * np.exp(-decay * x)


def tone(f, d, decay=8.0, harm=(1.0,)):
    x = t(d)
    s = sum(a * np.sin(2 * np.pi * f * (k + 1) * x) for k, a in enumerate(harm))
    return s * env(len(x), decay=decay)


def sweep(f0, f1, d, vibrato=0.0, decay=1.5):
    x = t(d)
    f = f0 * (f1 / f0) ** (x / d)
    phase = 2 * np.pi * np.cumsum(f * (1 + vibrato * np.sin(2 * np.pi * 6 * x))) / SR
    return np.sin(phase) * np.minimum(1, x / 0.02) * np.exp(-decay * x)


def noise(d, lo=None, hi=None, decay=10.0):
    n = ns(d)
    spec = np.fft.rfft(rng.standard_normal(n))
    freqs = np.fft.rfftfreq(n, 1 / SR)
    if lo:
        spec[freqs < lo] = 0
    if hi:
        spec[freqs > hi] = 0
    s = np.fft.irfft(spec, n)
    return s / (np.abs(s).max() + 1e-9) * env(n, decay=decay)


def seq(*parts, gap=0.0):
    out = []
    for p in parts:
        out.append(p)
        if gap:
            out.append(np.zeros(ns(gap)))
    return np.concatenate(out)


def chirp():
    """One cricket chirp: a 4.6 kHz tone pulsed 60 times a second."""
    x = t(0.05)
    return np.sin(2 * np.pi * 4600 * x) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 60 * x))) * env(len(x), decay=20)


def norm(s, peak=0.8):
    return s / (np.abs(s).max() + 1e-9) * peak


EFFECTS = {
    "thunk": lambda: tone(110, 0.35, 14, (1, 0.5, 0.2)) + np.pad(0.4 * noise(0.08, 80, 900, 40), (0, ns(0.27))),
    "stamp": lambda: np.pad(noise(0.06, 60, 1200, 50), (0, ns(0.2))) + tone(90, 0.26, 18, (1, 0.6)),
    "ding": lambda: tone(1320, 1.2, 3.5, (1, 0.3, 0.12)),
    "bell": lambda: tone(880, 1.6, 2.2, (1, 0.6, 0.35, 0.2)),
    "slide-up": lambda: sweep(350, 1500, 0.7, 0.02),
    "slide-down": lambda: sweep(1500, 300, 0.8, 0.02),
    "whistle": lambda: sweep(600, 1800, 0.35, 0.03, 3),
    "boing": lambda: sweep(180, 420, 0.5, 0.25, 4),
    "pop": lambda: np.pad(noise(0.03, 300, 5000, 90), (0, ns(0.1))) + tone(520, 0.13, 40),
    "toaster": lambda: seq(noise(0.02, 1000, 8000, 120), np.zeros(ns(0.04)), np.pad(noise(0.04, 200, 3000, 60), (0, ns(0.05))) + tone(700, 0.09, 45)),
    "whoosh": lambda: noise(0.6, 300, 3000, 2.5) * np.sin(np.pi * t(0.6) / 0.6),
    "airplane": lambda: noise(1.4, 150, 1800, 0.6) * np.sin(np.pi * t(1.4) / 1.4),
    "click": lambda: np.pad(noise(0.012, 1500, 9000, 300), (0, ns(0.03))),
    "typewriter": lambda: seq(*[np.pad(noise(0.012, 1500, 9000, 300), (0, ns(rng.uniform(0.05, 0.11)))) for _ in range(9)]),
    "scratch": lambda: noise(0.35, 2500, 9000, 6) * (0.6 + 0.4 * np.sin(2 * np.pi * 18 * t(0.35))),
    "marker": lambda: noise(0.25, 1800, 6000, 5) * (0.5 + 0.5 * np.sin(2 * np.pi * 30 * t(0.25))),
    "crickets": lambda: np.tile(seq(*[chirp() for _ in range(3)], gap=0.06), 3),
    "cash-register": lambda: seq(np.pad(noise(0.05, 400, 4000, 50), (0, ns(0.05))), tone(1760, 0.9, 4, (1, 0.4, 0.2))),
    "squeak": lambda: sweep(900, 2200, 0.12, 0, 6),
    "snip": lambda: seq(np.pad(noise(0.015, 2000, 9000, 250), (0, ns(0.04))), np.pad(noise(0.015, 2500, 9000, 250), (0, ns(0.05)))),
    "clank": lambda: tone(523, 0.6, 7, (1, 0.7, 0.5)) * 0.5 + tone(1291, 0.6, 9) * 0.4 + np.pad(noise(0.04, 500, 6000, 60), (0, ns(0.56))),
    "whirr": lambda: np.sin(2 * np.pi * np.cumsum(180 + 60 * np.sin(2 * np.pi * 7 * t(1.2))) / SR) * (0.4 + 0.6 * np.sign(np.sin(2 * np.pi * 40 * t(1.2)))) * np.sin(np.pi * t(1.2) / 1.2),
    "woof": lambda: sweep(260, 150, 0.18, 0.1, 10) * (1 + 0.6 * noise(0.18, 200, 2500, 10)),
    "slam": lambda: np.pad(noise(0.08, 60, 2500, 35), (0, ns(0.3))) + tone(70, 0.38, 12, (1, 0.5)),
    "huff": lambda: noise(0.3, 300, 2500, 9),
    "sparkle": lambda: seq(*[tone(f, 0.12, 25) for f in (2093, 2637, 3136, 4186)]),
    "pat": lambda: seq(*[np.pad(noise(0.03, 100, 1500, 70), (0, ns(0.09))) for _ in range(3)]),
    "hum": lambda: (np.sin(2 * np.pi * 110 * t(1.5)) + 0.4 * np.sin(2 * np.pi * 220 * t(1.5))) * np.minimum(1, t(1.5) / 0.3) * np.minimum(1, (1.5 - t(1.5)) / 0.3),
    "switch": lambda: np.pad(noise(0.01, 1000, 7000, 400), (0, ns(0.05))) + np.pad(tone(1800, 0.02, 200), (0, ns(0.04))),
    "tick": lambda: np.pad(noise(0.008, 3000, 9000, 500), (0, ns(0.03))),
    "hammer": lambda: seq(*[np.pad(noise(0.03, 200, 4000, 80) + tone(400, 0.03, 80), (0, ns(0.12))) for _ in range(6)]),
    "fire": lambda: noise(0.7, 200, 2500, 2) * np.sin(np.pi * t(0.7) / 0.7) + 0.3 * np.tile(np.pad(noise(0.01, 2000, 8000, 300), (0, ns(0.07))), 9)[: ns(0.7)],
    # the extreme gags (cartoon-style-bible.md, Comedy 6)
    "boom": lambda: noise(1.8, 30, 900, 2.2) + 0.8 * sweep(80, 35, 1.8, 0, 2.5),
    "zap": lambda: 0.5 * np.sign(np.sin(2 * np.pi * 120 * t(0.45))) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 16 * t(0.45)))) + 0.3 * noise(0.45, 2000, 8000, 3),
    "splat": lambda: np.pad(noise(0.06, 80, 1800, 40), (0, ns(0.16))) + sweep(400, 120, 0.22, 0, 12),
    "yelp": lambda: sweep(700, 1500, 0.5, 0.08, 1.5),
    "sizzle": lambda: noise(1.0, 3000, 9000, 1.2) * (0.7 + 0.3 * np.sin(2 * np.pi * 23 * t(1.0))),
}


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name, make in EFFECTS.items():
        path = out / f"{name}.wav"
        if path.exists():
            continue
        s = np.asarray(norm(np.asarray(make(), dtype=float)), dtype=float)
        pcm = (np.clip(s, -1, 1) * 32767).astype(np.int16)
        with wave.open(str(path), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(pcm.tobytes())
    print(f"{len(EFFECTS)} sound effects in {out}")


if __name__ == "__main__":
    main()
