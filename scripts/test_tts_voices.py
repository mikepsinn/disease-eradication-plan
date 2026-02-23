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
SAMPLE_TEXT = (PROJECT_ROOT / "assets" / "audiobook" / "test-sample.txt").read_text(encoding='utf-8')
OUTPUT_DIR = PROJECT_ROOT / "assets" / "audiobook" / "voice-tests"
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
    # --- Dinner party baseline (previous winner) ---
    "ctx-dinner-party": "Generate a voice with the energy of someone telling the best story at a dinner party.",

    # --- Warmer / more loving variants ---
    "dinner-warm-heart": "Generate a voice with the warmth of someone who genuinely loves humanity, telling the most important story at a dinner party. Tender but energetic.",
    "dinner-gentle-urgent": "Generate a warm, loving voice with gentle urgency, like someone who cares deeply about the listener and needs them to understand something vital.",
    "dinner-big-sister": "Generate a voice like a brilliant older sister explaining something wild over wine. Warm, protective, a little amused, completely on your side.",
    "dinner-campfire": "Generate a voice with the intimacy of someone telling a story around a campfire. Warm, sincere, drawing you in. Brisk but not rushed.",

    # --- Persuading a smart skeptic ---
    "persuade-friend": "Generate a voice like someone trying to convince their smartest, most skeptical friend of something that sounds insane but is actually true. Earnest, not preachy.",
    "persuade-evidence": "Generate a voice that sounds like a researcher sharing genuinely exciting findings with a colleague. Intellectually animated, not lecturing. Brisk pace.",
    "persuade-disarming": "Generate a voice that's disarmingly honest and a little vulnerable, like someone saying 'I know this sounds crazy, but hear me out.' Warm and real.",
    "persuade-patient": "Generate a patient, warm voice explaining something counterintuitive to someone smart. Not condescending. Respects the listener's intelligence. Slightly quick.",

    # --- Blends: dinner party energy + loving/persuasive ---
    "dinner-love-persuade": "Generate a voice with dinner-party energy but genuine love for the listener. Like someone who found the answer to a problem their friend is suffering from and can't wait to share it.",
    "dinner-co-conspirator": "Generate a warm, conspiratorial voice like you and your best friend just figured out how to fix something broken and you're both thrilled. Brisk, intimate, joyful.",
    "dinner-missionary": "Generate a voice with the passion of someone on a mission they believe will genuinely help people, combined with the energy of someone telling the best story at a dinner party. Warm, not preachy.",
    "dinner-wonder": "Generate a voice full of genuine wonder and affection, like someone who just discovered something beautiful about humanity and is sharing it at a dinner party.",
    "dinner-authority": "Generate a voice in a lower, more authoritative vocal register with the energy of someone telling the best story at a dinner party. Confident, commanding, warm.",
    "childrens-book": "Generate a voice like someone reading a beloved children's book aloud. Warm, expressive, slightly sing-song, full of wonder and delight. Each sentence is a little adventure.",
    "public-radio": "Generate a voice like an NPR or public radio host. Measured, intelligent, quietly amused. The kind of voice that makes you feel smarter just for listening. Brisk but unhurried.",
    "childrens-book-fast": "Generate a voice like someone reading a beloved children's book aloud. Warm, expressive, slightly sing-song, full of wonder and delight. Quick pace, energetic.",
    "dinner-documentary": "Generate a voice that blends documentary narrator authority with dinner-party energy. Authoritative and cinematic but warm and animated, like David Attenborough if he were tipsy and thrilled. Brisk pace.",

    # # --- Previous styles (commented out) ---
    # "natural": "Narrate naturally. Brisk pace.",
    # "british": "British accent. Brisk pace.",
    # "northern": "Northern English accent. Brisk pace.",
    # "deadpan": "Deadpan and dry. Brisk pace.",
    # "warm": "Warm and amused. Brisk pace.",
    # "conspiratorial": "Conversational and conspiratorial. Brisk pace.",
    # "documentary": "Documentary narrator. Brisk pace.",
    # "comedic": "Comedy audiobook narration. Brisk pace.",
    # "emotional-playful": "Emotional, present, and slightly playful. Brisk pace.",
    # "smart-casual": "Intelligent but informal, warm, and occasionally playful. Brisk pace.",
    # "australian": "Australian accent. Brisk pace.",
    # "gen-natural": "Generate a voice that narrates naturally at a slightly quick pace.",
    # "gen-british": "Generate a British voice that speaks at a brisk, confident pace.",
    # "gen-northern": "Generate a British voice that speaks slightly quickly in a Northern English accent.",
    # "gen-deadpan": "Generate a voice that delivers lines in a dry, deadpan style at a slightly quick pace.",
    # "gen-warm": "Generate a warm, amused voice that speaks at a brisk conversational pace.",
    # "gen-conspiratorial": "Generate a voice that sounds conversational and conspiratorial, speaking at a slightly quick pace.",
    # "gen-documentary": "Generate a voice that narrates like a documentary, authoritative and slightly quick.",
    # "gen-comedic": "Generate a voice narrating a comedy audiobook, slightly quick and expressive.",
    # "gen-emotional-playful": "Generate a voice that sounds emotional, present, and slightly playful, speaking at a brisk pace.",
    # "gen-smart-casual": "Generate a voice that sounds intelligent but informal, warm, and occasionally playful at a brisk pace.",
    # "gen-australian": "Generate a voice with an Australian accent that speaks at a slightly quick pace.",
    # "ctx-alien": "Generate a voice narrating a darkly comedic book written by an alien AI who's been watching humanity waste money on bombs instead of curing diseases.",
    # "ctx-delighted": "Generate a voice that sounds genuinely delighted by human stupidity, narrating a book about how to trick politicians into saving lives.",
    # "ctx-confiding": "Generate a voice that sounds like it's confiding something unbelievable to a close friend over drinks.",
    # "ctx-dinner-northern": "Generate a voice with a Northern English accent and the energy of someone telling the best story at a dinner party.",
    # "ctx-dinner-north2": "Generate an animated, expressive voice telling the best story at a dinner party. Brisk, fun, slightly Northern English.",
    # "ctx-dinner-north3": "Generate a voice like a witty Northerner at a dinner party who's just found out something unbelievable and can't stop laughing about it. Brisk and energetic.",
    # "ctx-dinner-north4": "Generate a voice with the energy of someone telling the best story at a dinner party. Hint of Northern English. Brisk and animated.",
    # "ctx-dinner-north5": "Generate a warm, animated voice like someone from Manchester or Leeds telling a hilarious story at a dinner party. Can't believe what they're saying.",
    # "ctx-dinner-north-low1": "Generate a lower-pitched, animated voice telling the best story at a dinner party. Hint of Northern English. Brisk and fun.",
    # "ctx-dinner-north-low2": "Generate a warm, deep voice like a witty Northerner at a dinner party who can't stop laughing about something unbelievable. Brisk and energetic.",
    # "ctx-dinner-north-low3": "Generate a voice in a lower register with the energy of someone from Manchester telling the best story at a dinner party. Animated and slightly quick.",
    # "ctx-dinner-north-low4": "Generate a rich, low-pitched voice telling a hilarious story at a dinner party. Slightly Northern English. Expressive and brisk.",
    # "ctx-dinner-british": "Generate a British voice with the energy of someone telling the best story at a dinner party. Brisk and confident.",
    # "ctx-dinner-low": "Generate a voice in a lower register with the energy of someone telling the best story at a dinner party. Brisk pace.",
    # "ctx-dinner-australian": "Generate a voice with an Australian accent and the energy of someone telling the best story at a dinner party. Brisk pace.",
    # "ctx-not-audiobook": "Generate a natural voice that doesn't sound like a typical audiobook narrator. Conversational, real, slightly quick.",
    # "ctx-ted-offscript": "Generate a voice that sounds like a TED talk speaker who's gone slightly off-script and is having way too much fun.",
    # "ctx-incredulous": "Generate a voice that starts curious and becomes increasingly incredulous at what it's reading.",
    # "ctx-british-confide": "Generate a British voice confiding something outrageous, with the energy of someone who just found out the most absurd fact and can't wait to share it.",
    # "ctx-alien-fond": "Generate a voice for an alien character who has been observing humanity for thousands of years and is both exasperated and deeply fond of them.",
    # "ctx-smart-funny": "Generate a voice for a comedy audiobook aimed at smart, skeptical adults who like dark humor and policy wonkery.",
    # "ctx-norm": "Generate a voice with a deadpan, unhurried delivery. Sounds like someone thinking out loud, slightly amused by their own observations. Deliberate pauses. Straight-faced while saying absurd things.",
    # "ctx-cunk": "Generate a British voice that sounds innocently confused but completely confident. Wide-eyed sincerity while stating absurd things. Like someone presenting a school report on a topic they fundamentally misunderstand.",
    # "low-natural": "Generate a voice in a lower register that narrates naturally at a slightly quick pace.",
    # "low-warm": "Generate a warm, low-pitched voice with a slightly quick conversational pace.",
    # "low-british": "Generate a British voice in a deeper, lower register. Brisk and confident.",
    # "low-confiding": "Generate a low-pitched voice that sounds like it's confiding something unbelievable to a close friend.",
    # "low-smart": "Generate a deeper voice that sounds intelligent, warm, and occasionally amused. Brisk pace.",
    # "low-dinner": "Generate a voice in a lower register with the energy of someone telling the best story at a dinner party.",
    # "no-instructions": "",
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
