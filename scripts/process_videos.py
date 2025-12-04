import os
import json
import pathlib
import sys
import re
from PIL import Image, ImageDraw, ImageFont
import whisper
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
from google import genai
from dotenv import load_dotenv

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
    if not VIDEOS_DIR.exists():
        print(f"Directory {VIDEOS_DIR} does not exist.")
        return

    video_files = [f for f in VIDEOS_DIR.iterdir() if f.suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv'] and 'short_v2' in f.name.lower()]
    
    if not video_files:
        print("No video files found.")
        return

    for video_file in video_files:
        print(f"\nProcessing {video_file.name}...")
        
        # Transcribe
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
        
        print(f"Finished {video_file.name}")

if __name__ == "__main__":
    main()
