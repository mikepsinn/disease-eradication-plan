#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import pathlib
import sys
import re

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont
import whisper
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
from google import genai
from dotenv import load_dotenv

# Add scripts directory to path for local imports
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib.llm import generate_claude_sonnet_content, generate_gemini_flash_content
from lib.tts import generate_speech, AVAILABLE_VOICES, DEFAULT_VOICE

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
if not API_KEY:
    print("Error: GOOGLE_GENERATIVE_AI_API_KEY not found in .env")
    sys.exit(1)

MODEL_ID = "gemini-2.5-flash"

VIDEOS_DIR = pathlib.Path("assets/videos")
ICONS_DIR = pathlib.Path("assets/icons")
ICON_PATH = ICONS_DIR / "war-on-disease-propaganda-suffering-poster-wide.JPG"
OUTPUT_DIR = VIDEOS_DIR / "processed"
WATERMARK_IMAGE_PATH = ICONS_DIR / "war-on-disease-org-watermark.JPG"

# Style reference file for transcript improvement
STYLE_REFERENCE_PATH = pathlib.Path("index-book.qmd")

# Gemini TTS voice configuration (uses library defaults: Aoede with Cunk-style delivery)
TTS_VOICE_NAME = DEFAULT_VOICE

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_watermark_image(text, output_path):
    """Creates a watermark image using PIL to avoid ImageMagick dependency."""
    # Settings
    font_size = 20
    padding = 10
    bg_color = "white"
    text_color = "black"
    border_width = 0
    border_color = "white"

    try:
        # Try to use a default font
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fallback to default font if arial is not found
        font = ImageFont.load_default()

    # Calculate text size using textbbox (newer PIL versions)
    dummy_img = Image.new('RGBA', (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate box size
    box_width = text_width + (padding * 2)
    box_height = text_height + (padding * 2)
    
    # Create image
    img = Image.new('RGBA', (box_width, box_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw background box
    draw.rectangle(
        [(0, 0), (box_width - 1, box_height - 1)],
        fill=bg_color,
        width=0
    )
    
    # Draw text
    # Center text
    text_x = padding
    text_y = padding - text_bbox[1] # Adjust for font baseline
    draw.text((text_x, padding), text, font=font, fill=text_color)
    
    img.save(output_path)
    return output_path

def transcribe_video(file_path):
    print(f"Transcribing {file_path}...")
    model = whisper.load_model("base")
    result = model.transcribe(str(file_path))
    return result

def save_timestamped_transcript(transcript_result, output_path):
    """Saves transcript with timestamps to a file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for segment in transcript_result["segments"]:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()
            # Format timestamp as [MM:SS]
            start_time = f"[{int(start // 60):02d}:{int(start % 60):02d}]"
            f.write(f"{start_time} {text}\n")


def load_style_reference():
    """Load the style reference document (index-book.qmd)."""
    if not STYLE_REFERENCE_PATH.exists():
        print(f"Warning: Style reference file not found at {STYLE_REFERENCE_PATH}")
        return ""

    with open(STYLE_REFERENCE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract just the prose content, skip YAML frontmatter and code blocks
    # Remove YAML frontmatter
    content = re.sub(r'^---[\s\S]*?---\n', '', content)
    # Remove code blocks
    content = re.sub(r'```[\s\S]*?```', '', content)
    # Remove Quarto includes
    content = re.sub(r'\{\{< include.*?>\}\}', '', content)
    # Remove Quarto variables (keep just the structure)
    content = re.sub(r'\{\{< var \w+ >\}\}', '[VALUE]', content)

    # Limit to first ~4000 chars for context window efficiency
    return content[:4000]


def improve_transcript_with_llm(transcript_segments: list, style_reference: str) -> list:
    """
    Send transcript to LLM to improve writing style while preserving timing.

    Args:
        transcript_segments: List of dicts with 'start', 'end', 'text' keys
        style_reference: Example text showing the desired writing style

    Returns:
        List of improved segments with same structure
    """
    print("Improving transcript with LLM...")

    # Format segments for the prompt
    segments_json = json.dumps([
        {
            "id": i,
            "start": seg["start"],
            "end": seg["end"],
            "duration": seg["end"] - seg["start"],
            "text": seg["text"].strip()
        }
        for i, seg in enumerate(transcript_segments)
    ], indent=2)

    prompt = f"""You are an expert editor. Your task is to improve a video transcript to match a specific writing style while preserving the timing and structure for video narration.

## CRITICAL CONSTRAINTS:
1. Each improved sentence MUST be roughly the same length (word count) as the original
2. Each sentence must cover the SAME topic/content as the original
3. The improved text must be speakable naturally in the same duration
4. Do NOT add new information or remove key points
5. Do NOT combine or split segments

## TARGET WRITING STYLE:
The style is witty, sardonic, uses dark humor, makes complex topics accessible through clever analogies, and has a slightly cynical but ultimately hopeful tone. Here's an example:

{style_reference}

## TRANSCRIPT TO IMPROVE:
{segments_json}

## OUTPUT FORMAT:
Return a JSON array with the EXACT same structure, but with improved "text" fields.
Each object must have: id, start, end, duration, text

Example output format:
[
  {{"id": 0, "start": 0.0, "end": 3.5, "duration": 3.5, "text": "Improved text here"}},
  {{"id": 1, "start": 3.5, "end": 7.2, "duration": 3.7, "text": "Next improved segment"}}
]

Return ONLY the JSON array, no markdown formatting or explanation."""

    try:
        # Use Claude Sonnet for better writing quality
        response = generate_claude_sonnet_content(prompt)

        # Clean up response
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]

        improved_segments = json.loads(response.strip())

        # Validate we got the same number of segments
        if len(improved_segments) != len(transcript_segments):
            print(f"Warning: LLM returned {len(improved_segments)} segments, expected {len(transcript_segments)}")
            print("Falling back to original transcript")
            return transcript_segments

        # Merge improved text back with original timing
        result = []
        for i, orig_seg in enumerate(transcript_segments):
            improved = improved_segments[i]
            result.append({
                "start": orig_seg["start"],
                "end": orig_seg["end"],
                "text": improved["text"]
            })

        return result

    except Exception as e:
        print(f"Error improving transcript: {e}")
        import traceback
        traceback.print_exc()
        return transcript_segments


def generate_tts_audio(segments: list, output_path: pathlib.Path) -> pathlib.Path:
    """
    Generate audio from transcript segments using Gemini TTS.

    Args:
        segments: List of dicts with 'start', 'end', 'text' keys
        output_path: Path to save the output audio file

    Returns:
        Path to the generated audio file
    """
    print(f"Generating TTS audio with Gemini (voice: {TTS_VOICE_NAME})...")

    # Combine all text into one continuous narration
    full_text = " ".join(seg["text"].strip() for seg in segments)

    try:
        # Generate audio using Gemini TTS
        audio_path = generate_speech(
            text=full_text,
            output_path=output_path,
            voice_name=TTS_VOICE_NAME,
            speaking_instructions="Read in a clear, engaging, documentary-style tone with appropriate pacing"
        )

        print(f"TTS audio saved to {audio_path}")
        return audio_path

    except Exception as e:
        print(f"Error generating TTS audio: {e}")
        import traceback
        traceback.print_exc()
        return None


def replace_video_audio(video_path: pathlib.Path, audio_path: pathlib.Path, output_path: pathlib.Path):
    """
    Replace the audio track of a video with new audio.

    Args:
        video_path: Path to the original video
        audio_path: Path to the new audio file
        output_path: Path to save the output video
    """
    print(f"Replacing audio in {video_path.name}...")

    try:
        # Load the video
        video = VideoFileClip(str(video_path))

        # Load the new audio
        new_audio = AudioFileClip(str(audio_path))

        # If audio is shorter than video, we need to handle that
        if new_audio.duration < video.duration:
            print(f"Warning: New audio ({new_audio.duration:.1f}s) is shorter than video ({video.duration:.1f}s)")
            # Trim video to match audio length
            video = video.subclipped(0, new_audio.duration)
        elif new_audio.duration > video.duration:
            print(f"Warning: New audio ({new_audio.duration:.1f}s) is longer than video ({video.duration:.1f}s)")
            # Trim audio to match video length
            new_audio = new_audio.subclipped(0, video.duration)

        # Set the new audio
        video_with_new_audio = video.with_audio(new_audio)

        # Write the output
        video_with_new_audio.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio-replace.m4a",
            remove_temp=True,
            fps=video.fps or 24,
            preset="medium",
            ffmpeg_params=["-pix_fmt", "yuv420p"]
        )

        # Cleanup
        video.close()
        new_audio.close()
        video_with_new_audio.close()

        print(f"Video with new audio saved to {output_path}")

    except Exception as e:
        print(f"Error replacing audio: {e}")
        import traceback
        traceback.print_exc()


def process_video_with_style_transfer(video_path: pathlib.Path, output_dir: pathlib.Path):
    """
    Full pipeline: transcribe -> improve style -> generate TTS -> replace audio.

    Args:
        video_path: Path to the input video
        output_dir: Directory to save outputs
    """
    stem = video_path.stem

    # Step 1: Transcribe
    print(f"\n[1/5] Transcribing {video_path.name}...")
    transcript_result = transcribe_video(video_path)

    # Save original transcript
    original_transcript_path = output_dir / f"{stem}_original_transcript.txt"
    with open(original_transcript_path, "w", encoding="utf-8") as f:
        for seg in transcript_result["segments"]:
            f.write(f"[{seg['start']:.1f}-{seg['end']:.1f}] {seg['text'].strip()}\n")
    print(f"Original transcript saved to {original_transcript_path}")

    # Step 2: Load style reference
    print(f"\n[2/5] Loading style reference...")
    style_reference = load_style_reference()
    if not style_reference:
        print("No style reference found, skipping style transfer")
        return

    # Step 3: Improve transcript with LLM
    print(f"\n[3/5] Improving transcript style with LLM...")
    improved_segments = improve_transcript_with_llm(
        transcript_result["segments"],
        style_reference
    )

    # Save improved transcript
    improved_transcript_path = output_dir / f"{stem}_improved_transcript.txt"
    with open(improved_transcript_path, "w", encoding="utf-8") as f:
        for seg in improved_segments:
            f.write(f"[{seg['start']:.1f}-{seg['end']:.1f}] {seg['text'].strip()}\n")
    print(f"Improved transcript saved to {improved_transcript_path}")

    # Step 4: Generate TTS audio
    print(f"\n[4/5] Generating TTS audio...")
    audio_path = output_dir / f"{stem}_tts_audio"
    generated_audio = generate_tts_audio(improved_segments, audio_path)

    if not generated_audio:
        print("Failed to generate TTS audio, aborting")
        return

    # Step 5: Replace audio in video
    print(f"\n[5/5] Replacing video audio...")
    output_video_path = output_dir / f"{stem}_restyled.mp4"
    replace_video_audio(video_path, generated_audio, output_video_path)

    print(f"\nStyle transfer complete! Output: {output_video_path}")


def get_cuts_from_gemini(transcript_text):
    print("Analyzing transcript with Gemini...")
    client = genai.Client(api_key=API_KEY)
    
    prompt = f"""
    You are a professional video editor. Your task is to identify "self-promotional" sections in the following video transcript to be cut out.
    
    Self-promotional sections include:
    - Asking viewers to subscribe, like, or share.
    - Promoting books, courses, or merchandise.
    - Directing viewers to websites for the purpose of sales or signups (unless it's the main topic).
    - Intros or outros that are purely branding/promotional and not content.
    
    Transcript:
    {transcript_text[:30000]} 
    (Transcript truncated if too long)

    Return a JSON list of objects, where each object has a 'start' and 'end' time (in seconds) representing the segment to CUT.
    The format must be strictly JSON:
    [
        {{"start": 10.5, "end": 20.0}},
        {{"start": 150.0, "end": 165.5}}
    ]
    
    If there are no sections to cut, return [].
    Do not include any markdown formatting (like ```json), just the raw JSON string.
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        
        text = response.text.strip()
        # Clean up markdown if present
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        cuts = json.loads(text.strip())
        return cuts
    except Exception as e:
        print(f"Error getting cuts from Gemini: {e}")
        return []

def edit_video(video_path, cuts, output_path):
    print(f"Editing video {video_path}...")
    
    try:
        video = VideoFileClip(str(video_path))
        
        # Sort cuts by start time
        cuts.sort(key=lambda x: x['start'])
        
        # Merge overlapping cuts
        merged_cuts = []
        if cuts:
            current_cut = cuts[0]
            for next_cut in cuts[1:]:
                if next_cut['start'] < current_cut['end']:
                    current_cut['end'] = max(current_cut['end'], next_cut['end'])
                else:
                    merged_cuts.append(current_cut)
                    current_cut = next_cut
            merged_cuts.append(current_cut)
        
        # Create list of clips to keep
        clips = []
        last_end = 0
        for cut in merged_cuts:
            start = max(0, cut['start'])
            end = min(video.duration, cut['end'])
            
            if start > last_end:
                clips.append(video.subclipped(last_end, start))
            last_end = end
            
        if last_end < video.duration:
            clips.append(video.subclipped(last_end, video.duration))
            
        if not clips:
            # If everything was cut (unlikely) or video was empty
            print("Warning: All content cut or empty video.")
            return

        final_content = concatenate_videoclips(clips)
        
        # Replace last few seconds with icon
        # We'll cut the last 3 seconds of the content, and append 3 seconds of icon
        # If video is shorter than 3 seconds, just use icon?
        
        content_duration = final_content.duration
        trim_amount = 2.0
        icon_duration = 2.0
        
        if content_duration > trim_amount:
            main_body = final_content.subclipped(0, content_duration - trim_amount)
        else:
            main_body = final_content # Too short to trim
            
        # Create Icon Clip
        if ICON_PATH.exists():
            icon_clip = ImageClip(str(ICON_PATH)).with_duration(icon_duration)
            # Resize icon to fit video height
            icon_clip = icon_clip.resized(height=video.h) 
            
            # Resize icon clip width to be even if needed, to avoid libx264 errors
            if icon_clip.w % 2 != 0:
                 icon_clip = icon_clip.resized(width=icon_clip.w - 1)

            final_sequence = concatenate_videoclips([main_body, icon_clip], method="compose")
        else:
            print(f"Warning: Icon file not found at {ICON_PATH}")
            final_sequence = main_body

        # Add Watermark
        if not WATERMARK_IMAGE_PATH.exists():
            print(f"Warning: Watermark image not found at {WATERMARK_IMAGE_PATH}")
            final_video = final_sequence
        else:
            # Create watermark clip with offset from bottom right
            # Using relative positioning
            margin = 20
            
            # Create temporary clip to get image dimensions and resize if needed
            # Let's say we want the watermark to be 20% of video width? Or just use as is?
            # User said "make the watermark 50% smaller" previously, assuming relative to the generated text one
            # But for this image, let's just ensure it's a reasonable size.
            # Maybe limit width to 150px?
            
            watermark_clip = ImageClip(str(WATERMARK_IMAGE_PATH))
            
            # Resize watermark if too big (optional, but good practice)
            # Let's resize it to a fixed width, e.g., 150 pixels (slightly smaller than 200)
            watermark_clip = watermark_clip.resized(width=150)
            
            wm_w, wm_h = watermark_clip.size
            w, h = final_sequence.size
            
            # Calculate position: (width - wm_width - margin, height - wm_height - margin)
            # Moving slightly more up and left as requested
            extra_offset = 10
            pos_x = w - wm_w - margin - extra_offset
            pos_y = h - wm_h - margin - extra_offset
            
            # Watermark should not be on the last appended image
            # The last segment is the icon, which lasts icon_duration
            watermark_duration = final_sequence.duration - icon_duration
            
            watermark_clip = (watermark_clip
                              .with_duration(watermark_duration)
                              .with_position((pos_x, pos_y))
                              .with_opacity(0.8)) # slightly transparent
                              
            final_video = CompositeVideoClip([final_sequence, watermark_clip])
        
        print(f"Saving to {output_path}...")
        # Use specific encoding settings for better compatibility
        final_video.write_videofile(
            str(output_path), 
            codec="libx264", 
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            fps=24,
            preset="medium",
            ffmpeg_params=["-pix_fmt", "yuv420p"] # Ensure compatibility with common players
        )
        
        # Cleanup
        video.close()
        final_video.close()
            
    except Exception as e:
        print(f"Error processing video: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main entry point - process videos with style transfer pipeline."""
    import argparse

    parser = argparse.ArgumentParser(description="Process videos with style transfer")
    parser.add_argument(
        "--mode",
        choices=["cuts", "style", "both"],
        default="style",
        help="Processing mode: 'cuts' (remove promos), 'style' (restyle transcript), 'both'"
    )
    parser.add_argument(
        "--pattern",
        default="short_v2",
        help="Filename pattern to match (default: 'short_v2')"
    )
    parser.add_argument(
        "--voice",
        default=TTS_VOICE_NAME,
        choices=AVAILABLE_VOICES,
        help=f"Gemini TTS voice name (default: {TTS_VOICE_NAME}). Options: {', '.join(AVAILABLE_VOICES)}"
    )
    args = parser.parse_args()

    # Update TTS voice if specified
    global TTS_VOICE_NAME
    TTS_VOICE_NAME = args.voice

    if not VIDEOS_DIR.exists():
        print(f"Directory {VIDEOS_DIR} does not exist.")
        return

    video_files = [
        f for f in VIDEOS_DIR.iterdir()
        if f.suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv']
        and args.pattern.lower() in f.name.lower()
    ]

    if not video_files:
        print(f"No video files matching pattern '{args.pattern}' found in {VIDEOS_DIR}")
        return

    print(f"Found {len(video_files)} video(s) to process")
    print(f"Mode: {args.mode}")
    print(f"TTS Voice: {TTS_VOICE_NAME}")

    for video_file in video_files:
        print(f"\n{'='*60}")
        print(f"Processing {video_file.name}...")
        print(f"{'='*60}")

        if args.mode in ["style", "both"]:
            # New style transfer pipeline
            process_video_with_style_transfer(video_file, OUTPUT_DIR)

        if args.mode in ["cuts", "both"]:
            # Original cuts pipeline
            transcript_result = transcribe_video(video_file)
            transcript_text = transcript_result["text"]

            # Save raw transcript for reference
            transcript_path = OUTPUT_DIR / f"{video_file.stem}_transcript.txt"
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(transcript_text)

            # Save timestamped transcript
            timestamped_transcript_path = OUTPUT_DIR / f"{video_file.stem}_transcript_with_timestamps.txt"
            save_timestamped_transcript(transcript_result, timestamped_transcript_path)

            # Analyze
            cuts = get_cuts_from_gemini(transcript_text)
            print(f"Proposed cuts: {cuts}")

            # Edit
            output_file = OUTPUT_DIR / f"{video_file.stem}_processed.mp4"
            edit_video(video_file, cuts, output_file)

        print(f"\nFinished {video_file.name}")


if __name__ == "__main__":
    main()
