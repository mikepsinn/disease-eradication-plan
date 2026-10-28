# Cartoon video: "How to End War and Disease (for Busy People)"

Plan and timing files for a cartoon video of audiobook episode 1 (chapter slug `index-manual`). The audiobook MP3 is the voice track; no new narration is recorded.

| File | What it is |
|---|---|
| `cartoon-script.md` | 137 scenes in 24 parts. Each scene has its start time in the MP3, the cue words, the visuals, the Wishonia sprites, and the on-screen text. Also YouTube chapter markers and short-video cuts. |
| `cartoon-style-bible.md` | The look (two visual layers), Wishonia's sprites, layout and lip-sync, the other characters, sensitive-content rules, and how to build the video. |
| `transcript.md` | Full transcript, one paragraph at a time, each with its [HH:MM:SS] time. |
| `transcript.srt` | Subtitles for the full episode (970 cues). |
| `word-timings.json` | Start and end time of every spoken word, for lip-sync and captions. |
| `wishonia-contact-sheet.png` | All 59 Wishonia sprites from `transmit/public/assets/sprites/alien/`, with their file names. |

## Source audio

`https://static.warondisease.org/assets/audiobook/manual-paperback/mp3/index-manual.487df96e.mp3` (62 min, item 1 of `https://static.warondisease.org/assets/audiobook/manual-paperback/feed.xml`).

## Notes

- The audio is a different edition from the current `index-manual.qmd`. It has extra parts (the "Hello, human" quiz, the long ending, the outro), it leaves some parts out (the pencil, the Earth Optimization Game), and some numbers are different (for example 97 million war deaths, 13,000 warheads, 3,070 : 1). The transcript and the script follow the audio.
- The theme song (00:20 to 01:40) is marked as music and not transcribed.
- Transcript: Whisper (small.en), names and spelling corrected by hand, numbers double-checked with Whisper medium.en (both models agree).
