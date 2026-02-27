"""Scene configuration loader for audiobook video pipeline.

Three-tier config: global defaults -> project-level scenes-config.json -> per-scene overrides.
"""
import json
from pathlib import Path

from lib.audiobook_common import IMAGE_STYLE


# --- Defaults (used when no scenes-config.json exists) ---

DEFAULT_CONFIG = {
    "visual_style": f"Retro academic illustration in warm earth tones with clean infographic clarity",
    "no_text": "Do not include any text, words, titles, labels, signs, banners, or writing of any kind.",
    "veo_negative_prompt": "narration, dialogue, voice, speech, talking, spoken words, realistic photography, 3D render, CGI, Pixar",
    "veo_parallel_workers": 4,
    "aspect_ratios": ["16:9", "9:16"],
    "characters": {},
}


def load_scene_config(config_dir: Path) -> dict:
    """Load scenes-config.json from the video directory, with defaults.

    Args:
        config_dir: The video directory (e.g. assets/audiobook/manual-paperback/video/)
    """
    config_path = config_dir / "scenes-config.json"
    config = dict(DEFAULT_CONFIG)
    if config_path.exists():
        user_config = json.loads(config_path.read_text(encoding='utf-8'))
        config.update(user_config)
    return config


def get_visual_style(config: dict) -> str:
    """Get the visual style string from config, with fallback to IMAGE_STYLE."""
    return config.get("visual_style", IMAGE_STYLE)


def get_no_text_instruction(config: dict) -> str:
    """Get the no-text instruction from config."""
    return config.get("no_text", DEFAULT_CONFIG["no_text"])


def get_veo_negative_prompt(config: dict) -> str:
    """Get the Veo negative prompt from config."""
    return config.get("veo_negative_prompt", DEFAULT_CONFIG["veo_negative_prompt"])


def get_aspect_ratios(config: dict) -> list[str]:
    """Get the aspect ratios to generate from config."""
    return config.get("aspect_ratios", DEFAULT_CONFIG["aspect_ratios"])


def get_veo_parallel_workers(config: dict) -> int:
    """Get the number of parallel Veo workers from config."""
    return config.get("veo_parallel_workers", DEFAULT_CONFIG["veo_parallel_workers"])
