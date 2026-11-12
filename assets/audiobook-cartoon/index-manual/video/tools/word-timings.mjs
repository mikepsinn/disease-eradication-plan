// Rebuild word-timings.json, transcript.srt and transcript.md from the audiobook pipeline's
// forced alignment, in episode MP3 time.
//
//   node tools/word-timings.mjs [--chapter <slug>] [path to assets/audiobook/manual-paperback]
//
// Episode 1 (index-manual, the default) writes ../word-timings.json; any other chapter writes
// assets/audiobook-cartoon/<slug>/word-timings.json (tools/chapter.mjs).
//
// The episode MP3 is the theme song followed by the chapter audio, and the alignment is in
// chapter time, so every aligned word moves by the theme song's length. The theme song has the
// cold open in it and does not change, so the words before it ends are kept from the old files.
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, join, resolve } from "node:path";
import { EP1, IS_EP1, PLAN, REPO, SLUG, VIDEO, chapterMp3 } from "./chapter.mjs";

const AUDIOBOOK = resolve(process.argv[2] ?? join(REPO, "assets/audiobook/manual-paperback"));
const THEME_SONG = join(REPO, "assets/music/podcast-theme-song.mp3");
const MP3 = IS_EP1 ? null : chapterMp3(AUDIOBOOK);
if (!IS_EP1 && !MP3) throw new Error(`no MP3 for ${SLUG} in ${join(AUDIOBOOK, "mp3")}`);
const MP3_URL = IS_EP1
  ? readFileSync(join(VIDEO, "tools/build-part.mjs"), "utf8").match(/const EP1_MP3_URL = "([^"]+)"/)[1]
  : `https://static.warondisease.org/assets/audiobook/manual-paperback/mp3/${basename(MP3)}`;
mkdirSync(PLAN, { recursive: true });
const duration = (f) => Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], { encoding: "utf8" }));

function round(x) {
  return Math.round(x * 1000) / 1000;
}

function stamp(t, sep) {
  const ms = Math.round(t * 1000);
  const pad = (n, w = 2) => String(n).padStart(w, "0");
  return `${pad(Math.floor(ms / 3600000))}:${pad(Math.floor(ms / 60000) % 60)}:${pad(Math.floor(ms / 1000) % 60)}${sep}${pad(ms % 1000, 3)}`;
}

const offset = Number(
  execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", THEME_SONG], { encoding: "utf8" }),
);
const alignment = JSON.parse(readFileSync(join(AUDIOBOOK, `alignment/${SLUG}.alignment.json`), "utf8"));
// The alignment's character offsets count a Windows line break as one character. (One script's
// file name differs in case from its chapter: Financial-Plan.)
const scripts = join(AUDIOBOOK, "narration-txt-chapters");
const scriptName = readdirSync(scripts).find((f) => f.toLowerCase() === `${SLUG}.prepared.txt`);
const prepared = readFileSync(join(scripts, scriptName), "utf8").replace(/\r\n/g, "\n");

// ── word-timings.json ────────────────────────────────────────────────────
// Every episode opens with the same theme song: its words come from episode 1's files.
const themeWords = JSON.parse(readFileSync(join(EP1, "word-timings.json"), "utf8")).filter((w) => w.end <= offset);
const chapterWords = alignment.words.map((w) => ({
  start: round(offset + w.start_ms / 1000),
  end: round(offset + w.end_ms / 1000),
  word: w.word,
  char: w.char_start,
}));
// ../timing-fixes.json corrects spots where the forced alignment is wrong: each fix spreads the
// listed words, found near their aligned time, over the start and end measured by ear.
const fixesPath = join(PLAN, "timing-fixes.json");
for (const fix of existsSync(fixesPath) ? JSON.parse(readFileSync(fixesPath, "utf8")) : []) {
  const i = chapterWords.findIndex((w, k) => Math.abs(w.start - fix.near) < 1 && fix.words.every((x, j) => chapterWords[k + j]?.word === x));
  if (i < 0) throw new Error(`timing fix not found: ${fix.words.join(" ")} near ${fix.near}`);
  const letters = fix.words.reduce((n, x) => n + x.length, 0);
  let t = fix.start;
  fix.words.forEach((x, j) => {
    const d = ((fix.end - fix.start) * x.length) / letters;
    Object.assign(chapterWords[i + j], { start: round(t), end: round(t + d) });
    t += d;
  });
}

// The podcast outro after the chapter is not aligned by the pipeline: tools/outro-words.py transcribes it.
const chapterEnd = offset + alignment.total_duration_ms / 1000;
// Every episode closes with the same outro: another chapter places episode 1's outro words the same
// distance from the end of its own MP3.
const ep1Outro = JSON.parse(readFileSync(join(EP1, "outro-words.json"), "utf8"));
let outroWords;
if (IS_EP1) outroWords = ep1Outro.filter((w) => w.start >= chapterEnd - 0.05);
else {
  const ep1End = JSON.parse(readFileSync(join(VIDEO, "storyboards/parts.json"), "utf8")).parts.at(-1).end;
  const shift = duration(MP3) - ep1End;
  outroWords = ep1Outro.map((w) => ({ start: round(w.start + shift), end: round(w.end + shift), word: w.word })).filter((w) => w.start >= chapterEnd - 0.05);
}
const words = [...themeWords, ...chapterWords, ...outroWords];
writeFileSync(
  join(PLAN, "word-timings.json"),
  "[\n" + words.map(({ start, end, word }) => JSON.stringify({ start, end, word })).join(",\n") + "\n]\n",
);

// ── transcript.srt: one cue per sentence, split when a sentence runs long ──
const cues = [];
let cue = [];
for (const [i, w] of words.entries()) {
  cue.push(w);
  const next = words[i + 1];
  const text = cue.map((x) => x.word).join(" ");
  const sentenceEnd = /[.?!:;]["')]*$/.test(w.word);
  if (!next || sentenceEnd || text.length > 70 || next.start - w.end > 0.6 || w.end - cue[0].start > 6) {
    cues.push({ start: cue[0].start, end: w.end, text });
    cue = [];
  }
}
// Every cue stays up at least half a second without running into the next one: a short cue is held
// into the pause after it, and one with no pause to grow into ("dirt.") joins the cue before it.
const MIN_CUE = 0.5;
for (let i = 0; i < cues.length; i++) {
  const c = cues[i], next = cues[i + 1];
  if (next && c.end > next.start) c.end = next.start;
  if (c.end - c.start >= MIN_CUE) continue;
  c.end = round(Math.min(c.start + MIN_CUE, next ? next.start : Infinity));
  if (c.end - c.start < MIN_CUE && i > 0) {
    cues[i - 1].text += " " + c.text;
    cues[i - 1].end = c.end;
    cues.splice(i--, 1);
  }
}
writeFileSync(
  join(PLAN, "transcript.srt"),
  cues.map((c, i) => `${i + 1}\n${stamp(c.start, ",")} --> ${stamp(c.end, ",")}\n${c.text}\n`).join("\n"),
);

// ── transcript.md: one entry per paragraph of the narration text ─────────
const oldTranscript = readFileSync(join(EP1, "transcript.md"), "utf8");
const themeEntries = oldTranscript
  .split("\n\n")
  .filter((p) => /^\*\*\[\d\d:\d\d:\d\d\]\*\*/.test(p))
  .filter((p) => p.startsWith("**[00:00:"));
const paragraphs = [];
const re = /[^\n]+(?:\n[^\n]+)*/g;
for (let m; (m = re.exec(prepared)); ) {
  const first = chapterWords.find((w) => w.char >= m.index);
  if (first) paragraphs.push(`**[${stamp(first.start, ".").slice(0, 8)}]** ${m[0].replace(/\s*\n\s*/g, " ").trim()}`);
}
if (outroWords.length) paragraphs.push(`**[${stamp(outroWords[0].start, ".").slice(0, 8)}]** *[Podcast outro]* ${outroWords.map((w) => w.word).join(" ")}`);
const length = stamp(offset + alignment.total_duration_ms / 1000, ".").slice(0, 8);
writeFileSync(
  join(PLAN, "transcript.md"),
  `# ${IS_EP1 ? "How to End War and Disease (for Busy People)" : prepared.trim().split("\n")[0].replace(/[.:]$/, "")}

${IS_EP1 ? "Audiobook episode 1" : `Audiobook chapter \`${SLUG}\``}. Timestamped transcript.

- Audio: <${MP3_URL}>
- Length of the theme song and chapter: ${length} (the outro follows)
- Method: the narration text the audio was made from, with times from the audiobook pipeline's forced alignment (\`tools/word-timings.mjs\`). The cold open in the theme song is from the earlier Whisper transcript.

Each paragraph starts with its time in the audio as [HH:MM:SS].

---

${[...themeEntries, ...paragraphs].join("\n\n")}
`,
);

console.log(
  `theme song ${offset.toFixed(3)} s; ${themeWords.length} theme words + ${chapterWords.length} chapter words; ` +
    `${cues.length} caption cues; ${paragraphs.length} paragraphs`,
);
