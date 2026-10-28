// Build one part of the episode cartoon from the audiobook MP3 and word-timings.json.
//
//   node tools/build-part.mjs parts/part-02.json
//
// Writes (relative to the video project):
//   data/<id>.js          scene times, words, mouth track, blinks and caption groups (committed)
//   index.html            the root composition for this part (committed)
//   assets/audio/<id>.mp3 the cut of the episode MP3 (git-ignored)
//   assets/sprites/       copies of the Wishonia sprites (git-ignored)
import { execFileSync } from "node:child_process";
import { cpSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const VIDEO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const PLAN = resolve(VIDEO, "..");
const REPO = resolve(PLAN, "../../..");
const MP3_URL = "https://static.warondisease.org/assets/audiobook/manual-paperback/mp3/index-manual.487df96e.mp3";
const MP3 = join(REPO, "assets/audiobook/cartoon/index-manual.mp3");
const SPRITES = join(REPO, "transmit/public/assets/sprites/alien");

const part = JSON.parse(readFileSync(resolve(VIDEO, process.argv[2] ?? "parts/part-02.json"), "utf8"));
const START = part.audio.start;
const DURATION = round(part.audio.end - START);

function round(x) {
  return Math.round(x * 1000) / 1000;
}

// ── Words ────────────────────────────────────────────────────────────────
// Whisper splits numbers ("10" ".7", "2" ",782", "87" "%"). Join those pieces into one word.
const allWords = JSON.parse(readFileSync(join(PLAN, "word-timings.json"), "utf8"));
const words = [];
for (const w of allWords) {
  if (w.end <= START || w.start >= part.audio.end) continue;
  const text = w.word.trim();
  const prev = words[words.length - 1];
  if (prev && /^[.,%\-]/.test(text)) {
    prev.w += text;
    prev.e = round(w.end - START);
    continue;
  }
  words.push({ w: text, s: round(Math.max(0, w.start - START)), e: round(w.end - START) });
}

function norm(text) {
  return text.toLowerCase().replace(/[^a-z0-9%$]/g, "");
}

// The first word that matches `cue`, at or after `after` seconds (part time).
function findWord(cue, after) {
  const target = norm(cue);
  const hit = words.find((w) => w.s >= after - 0.3 && norm(w.w) === target);
  if (!hit) throw new Error(`Cue "${cue}" not found after ${after}s`);
  return hit.s;
}

// ── Scenes and Wishonia states ───────────────────────────────────────────
const scenes = part.scenes.map((sc) => ({ ...sc, start: findWord(sc.cue, sc.approx - START) }));
scenes[0].start = 0;
scenes.forEach((sc, i) => {
  sc.end = i + 1 < scenes.length ? scenes[i + 1].start : DURATION;
  sc.duration = round(sc.end - sc.start);
});

const states = [];
for (const sc of scenes) {
  let after = sc.start;
  for (const st of sc.wishonia) {
    const t = states.length === 0 ? 0 : sc.wishonia.indexOf(st) === 0 ? sc.start : findWord(st.cue, after);
    after = t;
    states.push({ t: round(t), expr: st.expr, rest: st.rest, body: st.body, mode: st.mode, scene: sc.id });
  }
}

// ── Mouth track (CHAR_TO_VISEME from wishonia-widget/src/core/viseme-map.ts) ──
const CHAR_TO_VISEME = {
  a: "open", e: "ee", i: "ee", o: "oh", u: "oh",
  b: "closed", m: "closed", p: "closed", f: "closed", v: "closed",
  s: "ee", z: "ee", c: "ee",
  t: "small", d: "small", n: "small", l: "small", r: "small",
  g: "small", k: "small", j: "small",
  w: "oh", y: "ee", h: "small", q: "oh", x: "ee",
};
const SPOKEN = {
  0: "zero", 1: "one", 2: "two", 3: "three", 4: "four",
  5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
  ".": "point", "%": "percent", ",": "",
};

function spell(word) {
  return word
    .toLowerCase()
    .split("")
    .map((ch) => (ch in SPOKEN ? SPOKEN[ch] : ch))
    .join("")
    .replace(/[^a-z]/g, "");
}

const MIN_SHAPE = 0.06; // shorter mouth shapes flicker at 30 fps
const REST_GAP = 0.18; // a pause this long shows the resting mouth
const mouth = []; // [time, viseme | null]; null = the resting mouth of the current state
function pushMouth(t, v) {
  const last = mouth[mouth.length - 1];
  if (last && last[1] === v) return;
  if (last && t - last[0] < MIN_SHAPE && last[1] !== "closed") mouth.pop();
  const prev = mouth[mouth.length - 1];
  if (prev && prev[1] === v) return;
  mouth.push([round(t), v]);
}
pushMouth(0, null);
words.forEach((w, i) => {
  const letters = spell(w.w).split("");
  const step = (w.e - w.s) / Math.max(1, letters.length);
  letters.forEach((ch, k) => pushMouth(w.s + k * step, CHAR_TO_VISEME[ch] ?? "small"));
  const next = words[i + 1];
  const gap = next ? next.s - w.e : 1;
  if (gap >= REST_GAP) pushMouth(w.e, null);
  else if (gap > 0.04) pushMouth(w.e, "closed");
});

// ── Blinks (characters.js: blink-smile for 150 ms every few seconds, not mid-word) ──
const blinks = [];
let lastBlink = -2;
mouth.forEach(([t, v], i) => {
  const until = i + 1 < mouth.length ? mouth[i + 1][0] : DURATION;
  const quiet = v === null ? 0.3 : v === "closed" ? 0.16 : Infinity;
  const due = v === null ? 3.5 : 7;
  if (until - t >= quiet && t - lastBlink >= due) {
    blinks.push([round(t + 0.02), 0.15]);
    lastBlink = t;
  }
});

// ── Caption groups ──────────────────────────────────────────────────────
// Split into phrases at sentence ends and long pauses, then split each phrase into
// lines of even length (at most 7 words / 40 characters), so no line is one orphan word.
const MAX_WORDS = 7;
const MAX_CHARS = 40;
const phrases = [];
words.forEach((w, i) => {
  const prev = words[i - 1];
  if (!prev || /[.?!]$/.test(prev.w) || w.s - prev.e > 0.6) phrases.push([]);
  phrases[phrases.length - 1].push(w);
});
const captions = [];
for (const phrase of phrases) {
  const chars = phrase.map((x) => x.w).join(" ").length;
  const lines = Math.max(Math.ceil(phrase.length / MAX_WORDS), Math.ceil(chars / MAX_CHARS));
  const per = Math.ceil(phrase.length / lines);
  for (let k = 0; k < phrase.length; k += per) captions.push({ words: phrase.slice(k, k + per) });
}
const captionGroups = captions.map((g, i) => {
  const next = captions[i + 1];
  const last = g.words[g.words.length - 1];
  const end = next ? Math.min(next.words[0].s, last.e + 0.8) : DURATION;
  return { s: g.words[0].s, e: round(end), words: g.words };
});

// ── Write data/<id>.js ──────────────────────────────────────────────────
const data = {
  id: part.id,
  title: part.title,
  audioStart: START,
  duration: DURATION,
  scenes: scenes.map(({ id, file, layer, start, duration }) => ({ id, file, layer, start, duration })),
  states,
  words,
  mouth,
  blinks,
  captions: captionGroups,
};
mkdirSync(join(VIDEO, "data"), { recursive: true });
writeFileSync(
  join(VIDEO, "data", `${part.id}.js`),
  `// Generated by tools/build-part.mjs from parts/${part.id}.json and word-timings.json. Do not edit.\n` +
    `window.HF_PART = ${JSON.stringify(data)};\n`,
);

// ── Audio cut and sprites (git-ignored) ─────────────────────────────────
if (!existsSync(MP3)) {
  mkdirSync(dirname(MP3), { recursive: true });
  execFileSync("curl", ["-sS", "-o", MP3, MP3_URL], { stdio: "inherit" });
}
mkdirSync(join(VIDEO, "assets/audio"), { recursive: true });
execFileSync(
  "ffmpeg",
  ["-y", "-loglevel", "error", "-ss", String(START), "-to", String(part.audio.end), "-i", MP3,
    "-ac", "2", "-ar", "44100", "-b:a", "192k", join(VIDEO, "assets/audio", `${part.id}.mp3`)],
  { stdio: "inherit" },
);
cpSync(SPRITES, join(VIDEO, "assets/sprites"), {
  recursive: true,
  filter: (src) => !src.includes("/sources"),
});

// ── Keep each composition's root duration equal to its scene length ─────
function setRootDuration(file, id, duration) {
  const path = join(VIDEO, file);
  if (!existsSync(path)) return;
  const html = readFileSync(path, "utf8");
  const re = new RegExp(`(data-composition-id="${id}"[^>]*?data-duration=")[0-9.]+(")`);
  writeFileSync(path, html.replace(re, `$1${duration}$2`).replace(/(class="clip" data-start="0" data-duration=")[0-9.]+(")/g, `$1${duration}$2`));
}
for (const sc of scenes) setRootDuration(sc.file, sc.id, sc.duration);
setRootDuration("compositions/captions.html", "captions", DURATION);

// ── Write index.html ────────────────────────────────────────────────────
const sceneDivs = scenes
  .map(
    (sc, i) => `      <div
        id="el-${sc.id}"
        class="scene clip"
        data-composition-id="${sc.id}"
        data-composition-src="${sc.file}"
        data-start="${sc.start}"
        data-duration="${sc.duration}"
        data-track-index="${i % 2}"
      ></div>`,
  )
  .join("\n");

const index = `<!doctype html>
<!-- Generated by tools/build-part.mjs from parts/${part.id}.json. Do not edit; edit the part file or the compositions. -->
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1920px; height: 1080px; overflow: hidden; background: #000; }
      #root { position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #f3ead3; }
      .scene { position: absolute; inset: 0; width: 100%; height: 100%; }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="${DURATION}"
      data-width="1920"
      data-height="1080"
    >
${sceneDivs}
      <div
        id="el-captions"
        class="scene clip"
        data-composition-id="captions"
        data-composition-src="compositions/captions.html"
        data-track-kind="captions"
        data-start="0"
        data-duration="${DURATION}"
        data-track-index="4"
      ></div>
      <audio
        id="el-voice"
        src="assets/audio/${part.id}.mp3"
        data-start="0"
        data-duration="${DURATION}"
        data-track-index="10"
        data-volume="1"
      ></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      var tl = gsap.timeline({ paused: true });
      tl.to({}, { duration: ${DURATION} }, 0); // full-span anchor
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
`;
writeFileSync(join(VIDEO, "index.html"), index);

console.log(`${part.id}: ${DURATION}s, ${scenes.length} scenes, ${words.length} words, ${mouth.length} mouth shapes, ${blinks.length} blinks, ${captionGroups.length} caption groups`);
for (const sc of scenes) console.log(`  ${sc.id} ${sc.start.toFixed(2)} +${sc.duration.toFixed(2)}`);
