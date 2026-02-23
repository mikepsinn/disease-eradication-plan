#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate TTS voice samples with different voices and speaking instructions."""
import sys
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tts import generate_speech
from lib.retry import RateLimiter

PROJECT_ROOT = Path(__file__).parent.parent
SAMPLE_TEXT = (PROJECT_ROOT / "audiobook" / "test-sample.txt").read_text(encoding='utf-8')
OUTPUT_DIR = PROJECT_ROOT / "audiobook" / "voice-tests"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Voices to test
VOICES = [
    # "Aoede",
    "Kore",
    # "Leda",
    # "Zephyr",
    # Male voices (lower register naturally)
    # "Charon",
    # "Puck",
]

# Speaking instruction styles (keep to 1-3 sentences for best results)
STYLES = {
    # Terse keyword style
    "natural": "Narrate naturally. Brisk pace.",
    "british": "British accent. Brisk pace.",
    "northern": "Northern English accent. Brisk pace.",
    "deadpan": "Deadpan and dry. Brisk pace.",
    "warm": "Warm and amused. Brisk pace.",
    "conspiratorial": "Conversational and conspiratorial. Brisk pace.",
    "documentary": "Documentary narrator. Brisk pace.",
    "comedic": "Comedy audiobook narration. Brisk pace.",
    "emotional-playful": "Emotional, present, and slightly playful. Brisk pace.",
    "smart-casual": "Intelligent but informal, warm, and occasionally playful. Brisk pace.",
    "australian": "Australian accent. Brisk pace.",

    # Generative instruction style (same concepts, full sentences)
    "gen-natural": "Generate a voice that narrates naturally at a slightly quick pace.",
    "gen-british": "Generate a British voice that speaks at a brisk, confident pace.",
    "gen-northern": "Generate a British voice that speaks slightly quickly in a Northern English accent.",
    "gen-deadpan": "Generate a voice that delivers lines in a dry, deadpan style at a slightly quick pace.",
    "gen-warm": "Generate a warm, amused voice that speaks at a brisk conversational pace.",
    "gen-conspiratorial": "Generate a voice that sounds conversational and conspiratorial, speaking at a slightly quick pace.",
    "gen-documentary": "Generate a voice that narrates like a documentary, authoritative and slightly quick.",
    "gen-comedic": "Generate a voice narrating a comedy audiobook, slightly quick and expressive.",
    "gen-emotional-playful": "Generate a voice that sounds emotional, present, and slightly playful, speaking at a brisk pace.",
    "gen-smart-casual": "Generate a voice that sounds intelligent but informal, warm, and occasionally playful at a brisk pace.",
    "gen-australian": "Generate a voice with an Australian accent that speaks at a slightly quick pace.",

    # Context-aware / feeling-based prompts
    "ctx-alien": "Generate a voice narrating a darkly comedic book written by an alien AI who's been watching humanity waste money on bombs instead of curing diseases.",
    "ctx-delighted": "Generate a voice that sounds genuinely delighted by human stupidity, narrating a book about how to trick politicians into saving lives.",
    "ctx-confiding": "Generate a voice that sounds like it's confiding something unbelievable to a close friend over drinks.",
    "ctx-dinner-party": "Generate a voice with the energy of someone telling the best story at a dinner party.",
    "ctx-dinner-northern": "Generate a voice with a Northern English accent and the energy of someone telling the best story at a dinner party.",
    # Energy-first, accent as afterthought
    "ctx-dinner-north2": "Generate an animated, expressive voice telling the best story at a dinner party. Brisk, fun, slightly Northern English.",
    # Scenario-driven - let the accent emerge from context
    "ctx-dinner-north3": "Generate a voice like a witty Northerner at a dinner party who's just found out something unbelievable and can't stop laughing about it. Brisk and energetic.",
    # Minimal accent nudge
    "ctx-dinner-north4": "Generate a voice with the energy of someone telling the best story at a dinner party. Hint of Northern English. Brisk and animated.",
    # Character-driven
    "ctx-dinner-north5": "Generate a warm, animated voice like someone from Manchester or Leeds telling a hilarious story at a dinner party. Can't believe what they're saying.",
    # Lower + Northern + animated
    "ctx-dinner-north-low1": "Generate a lower-pitched, animated voice telling the best story at a dinner party. Hint of Northern English. Brisk and fun.",
    "ctx-dinner-north-low2": "Generate a warm, deep voice like a witty Northerner at a dinner party who can't stop laughing about something unbelievable. Brisk and energetic.",
    "ctx-dinner-north-low3": "Generate a voice in a lower register with the energy of someone from Manchester telling the best story at a dinner party. Animated and slightly quick.",
    "ctx-dinner-north-low4": "Generate a rich, low-pitched voice telling a hilarious story at a dinner party. Slightly Northern English. Expressive and brisk.",
    "ctx-dinner-british": "Generate a British voice with the energy of someone telling the best story at a dinner party. Brisk and confident.",
    "ctx-dinner-low": "Generate a voice in a lower register with the energy of someone telling the best story at a dinner party. Brisk pace.",
    "ctx-dinner-australian": "Generate a voice with an Australian accent and the energy of someone telling the best story at a dinner party. Brisk pace.",
    "ctx-not-audiobook": "Generate a natural voice that doesn't sound like a typical audiobook narrator. Conversational, real, slightly quick.",
    "ctx-ted-offscript": "Generate a voice that sounds like a TED talk speaker who's gone slightly off-script and is having way too much fun.",
    "ctx-incredulous": "Generate a voice that starts curious and becomes increasingly incredulous at what it's reading.",
    "ctx-british-confide": "Generate a British voice confiding something outrageous, with the energy of someone who just found out the most absurd fact and can't wait to share it.",
    "ctx-alien-fond": "Generate a voice for an alien character who has been observing humanity for thousands of years and is both exasperated and deeply fond of them.",
    "ctx-smart-funny": "Generate a voice for a comedy audiobook aimed at smart, skeptical adults who like dark humor and policy wonkery.",

    "ctx-norm": "Generate a voice with a deadpan, unhurried delivery. Sounds like someone thinking out loud, slightly amused by their own observations. Deliberate pauses. Straight-faced while saying absurd things.",
    "ctx-cunk": "Generate a British voice that sounds innocently confused but completely confident. Wide-eyed sincerity while stating absurd things. Like someone presenting a school report on a topic they fundamentally misunderstand.",

    # Lower register experiments
    "low-natural": "Generate a voice in a lower register that narrates naturally at a slightly quick pace.",
    "low-warm": "Generate a warm, low-pitched voice with a slightly quick conversational pace.",
    "low-british": "Generate a British voice in a deeper, lower register. Brisk and confident.",
    "low-confiding": "Generate a low-pitched voice that sounds like it's confiding something unbelievable to a close friend.",
    "low-smart": "Generate a deeper voice that sounds intelligent, warm, and occasionally amused. Brisk pace.",
    "low-dinner": "Generate a voice in a lower register with the energy of someone telling the best story at a dinner party.",

    "no-instructions": "",
}

# Generate all voice + style combos
TESTS = [(voice, style_name, prompt) for voice in VOICES for style_name, prompt in STYLES.items()]

# Parallelization config
TTS_PARALLEL_WORKERS = 4
tts_rate_limiter = RateLimiter(max_requests=10, window_seconds=60)

# Filter to uncached items
work_items = []
for i, (voice, style, instructions) in enumerate(TESTS):
    filename = f"{voice}-{style}.wav"
    output_path = OUTPUT_DIR / filename
    if output_path.exists():
        print(f"[{i+1}/{len(TESTS)}] SKIP (exists): {filename}")
    else:
        work_items.append((i, voice, style, instructions, output_path))

print(f"\nGenerating {len(work_items)} voice samples ({len(TESTS) - len(work_items)} cached, {TTS_PARALLEL_WORKERS} parallel workers)...")
print(f"Output: {OUTPUT_DIR}\n")

def _generate_one(item):
    i, voice, style, instructions, output_path = item
    label = f"[{i+1}/{len(TESTS)}] {voice} + {style}"
    print(f"{label} - starting...")
    tts_rate_limiter.acquire()
    generate_speech(SAMPLE_TEXT, output_path, voice_name=voice, speaking_instructions=instructions)
    print(f"{label} - done")
    return i

errors = []
with ThreadPoolExecutor(max_workers=TTS_PARALLEL_WORKERS) as executor:
    futures = {executor.submit(_generate_one, item): item for item in work_items}
    for future in as_completed(futures):
        item = futures[future]
        try:
            future.result()
        except Exception as e:
            errors.append(f"{item[1]}-{item[2]}: {e}")
            print(f"[ERROR] {item[1]} + {item[2]}: {e}")

if errors:
    print(f"\n{len(errors)} errors:")
    for err in errors:
        print(f"  {err}")

print(f"\nDone! {len(TESTS)} samples in {OUTPUT_DIR}")
