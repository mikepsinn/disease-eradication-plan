// Build one part of the episode cartoon from the audiobook MP3 and word-timings.json.
//
//   node tools/build-part.mjs parts/part-01.json [--aspect 9x16]
//
// --aspect 9x16 builds the tall phone version (1080 x 1920); the default is 16:9 (1920 x 1080).
//
// Writes (relative to the video project):
//   data/<id>.js          scene times, words, mouth track, blinks, caption groups and sounds (committed)
//   data/part.js          a copy of it, for the compositions every part shares (git-ignored)
//   data/aspect.js        the canvas shape of this build (git-ignored)
//   index.html            the root composition for this part (committed)
//   assets/audio/<id>.mp3 the cut of the episode MP3 with the part's sound effects mixed in (git-ignored)
//   assets/sprites/       copies of the Wishonia sprites (git-ignored)
//   assets/sfx/           the sound effects, made by tools/sfx.py (git-ignored)
//   the part's "media"    other footage, such as the theme song music video (git-ignored)
//
// A part file's "sounds" list places sound effects on spoken words:
//   { "scene": "pentagon", "cue": "Square", "n": 1, "at": "after", "sfx": "thud", "volume": 0.8 }
// "at" is "on" (the word's start), "after" (a beat after it ends) or "before" (half a second early).
import { execFileSync } from "node:child_process";
import { copyFileSync, cpSync, existsSync, mkdirSync, readFileSync, readdirSync, renameSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const VIDEO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const PLAN = resolve(VIDEO, "..");
const REPO = resolve(PLAN, "../../..");
const MP3_URL = "https://static.warondisease.org/assets/audiobook/manual-paperback/mp3/genetic-slavery.680f0446.mp3";
// Named after the MP3, so that a cached copy of an older episode is never used by mistake.
const MP3 = join(REPO, "assets/audiobook/cartoon", MP3_URL.split("/").pop());
const SPRITES = join(REPO, "transmit/public/assets/sprites/alien");

const part = JSON.parse(readFileSync(resolve(VIDEO, process.argv[2] ?? "parts/part-02.json"), "utf8"));
const START = part.audio.start;
const DURATION = round(part.audio.end - START);
const aspectAt = process.argv.indexOf("--aspect");
const ASPECT = aspectAt > 0 ? process.argv[aspectAt + 1] : "16x9";
const [W, H] = ASPECT === "9x16" ? [1080, 1920] : [1920, 1080];
// Captions are burned in only on the phone version (Shorts, Reels and TikTok scroll with the sound off).
// The 16:9 version goes to YouTube with data/<id>.srt as closed captions instead; --captions burns them in anyway.
const BURN_CAPTIONS = ASPECT === "9x16" || process.argv.includes("--captions");

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
  for (const st of sc.wishonia || []) {
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

// Scenes whose words are already on screen (a title card) get no captions.
const quiet = scenes.filter((sc) => (part.noCaptions || []).includes(sc.id));
const shownCaptions = captionGroups.filter((g) => !quiet.some((sc) => g.s >= sc.start - 0.01 && g.s < sc.start + sc.duration));

// ── Sound effects on spoken words ───────────────────────────────────────
function wordIn(sc, cue, n) {
  const want = norm(cue);
  let k = n || 1;
  const hit = words.find((w) => w.s >= sc.start - 0.05 && w.s < sc.start + sc.duration && norm(w.w) === want && --k === 0);
  if (!hit) throw new Error(`Sound cue "${cue}" (${n || 1}) not in scene ${sc.id}`);
  return hit;
}
const sounds = (part.sounds || []).map((sd) => {
  const sc = scenes.find((s) => s.id === sd.scene);
  if (!sc) throw new Error(`Sound for unknown scene ${sd.scene}`);
  let t = sc.start;
  if (sd.cue !== undefined) {
    const w = wordIn(sc, sd.cue, sd.n);
    t = sd.at === "after" ? w.e + 0.35 : sd.at === "before" ? w.s - 0.5 : w.s;
  }
  return { t: round(Math.max(0, t + (sd.offset || 0))), sfx: sd.sfx, volume: sd.volume ?? 0.6 };
});

// ── Write data/<id>.js, data/part.js and data/aspect.js ─────────────────
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
  captions: shownCaptions,
  sounds,
};
mkdirSync(join(VIDEO, "data"), { recursive: true });
const dataJs = `// Generated by tools/build-part.mjs from parts/${part.id}.json and word-timings.json. Do not edit.\n` +
  `window.HF_PART = ${JSON.stringify(data)};\n`;
writeFileSync(join(VIDEO, "data", `${part.id}.js`), dataJs);
// --data-only: just the part's data (for tools/scene-check.mjs), without touching the shared build files,
// so several parts can be worked on at once.
if (process.argv.includes("--data-only")) {
  console.log(`${part.id}: data/${part.id}.js, ${scenes.length} scenes, ${DURATION}s`);
  for (const sc of scenes) console.log(`  ${sc.id} ${sc.start.toFixed(2)} +${sc.duration.toFixed(2)}`);
  process.exit(0);
}
writeFileSync(join(VIDEO, "data", "part.js"), dataJs);
writeFileSync(join(VIDEO, "data", "aspect.js"), `// Generated by tools/build-part.mjs. Do not edit.\nwindow.HF_ASPECT = ${JSON.stringify(ASPECT)};\n`);
// Closed captions for the 16:9 upload: every caption group, the title card's too, in part time.
function srtTime(t) {
  const ms = Math.round(t * 1000);
  const pad = (n, k = 2) => String(n).padStart(k, "0");
  return `${pad(Math.floor(ms / 3600000))}:${pad(Math.floor(ms / 60000) % 60)}:${pad(Math.floor(ms / 1000) % 60)},${pad(ms % 1000, 3)}`;
}
writeFileSync(join(VIDEO, "data", `${part.id}.srt`), captionGroups.map((g, i) =>
  `${i + 1}\n${srtTime(g.s)} --> ${srtTime(g.e)}\n${g.words.map((w) => w.w).join(" ")}\n`).join("\n"));

// ── Audio cut with the sound effects, sprites and media (git-ignored) ───
if (!existsSync(MP3)) {
  mkdirSync(dirname(MP3), { recursive: true });
  // -f: an HTTP error fails the build instead of saving the error page as the MP3.
  // Download to a temporary file first, so a failed or partial download is never reused.
  execFileSync("curl", ["-fsS", "-o", `${MP3}.part`, MP3_URL], { stdio: "inherit" });
  renameSync(`${MP3}.part`, MP3);
}
mkdirSync(join(VIDEO, "assets/audio"), { recursive: true });
const voice = join(VIDEO, "assets/audio", `${part.id}.voice.wav`);
execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-ss", String(START), "-to", String(part.audio.end), "-i", MP3, "-ac", "2", "-ar", "44100", voice], { stdio: "inherit" });
const SFX = join(VIDEO, "assets/sfx");
if (sounds.length) execFileSync("python3", ["-I", join(VIDEO, "tools/sfx.py"), SFX], { stdio: "inherit" });
const inputs = ["-i", voice];
const chains = [];
sounds.forEach((sd, i) => {
  const file = join(SFX, `${sd.sfx}.wav`);
  if (!existsSync(file)) throw new Error(`No sound effect ${sd.sfx} (have: ${readdirSync(SFX).join(", ")})`);
  inputs.push("-i", file);
  const ms = Math.round(sd.t * 1000);
  chains.push(`[${i + 1}]adelay=${ms}|${ms},volume=${sd.volume}[s${i}]`);
});
const mix = sounds.length ? [...chains, `[0]${sounds.map((_, i) => `[s${i}]`).join("")}amix=inputs=${sounds.length + 1}:normalize=0:duration=first[out]`].join(";") : null;
execFileSync("ffmpeg", ["-y", "-loglevel", "error", ...inputs, ...(mix ? ["-filter_complex", mix, "-map", "[out]"] : []),
  "-ac", "2", "-ar", "44100", "-b:a", "192k", join(VIDEO, "assets/audio", `${part.id}.mp3`)], { stdio: "inherit" });
cpSync(SPRITES, join(VIDEO, "assets/sprites"), {
  recursive: true,
  filter: (src) => !src.includes("/sources"),
});
// Media too big for git lives only in the main checkout, so a worktree reads it from there.
const MAIN = resolve(execFileSync("git", ["-C", REPO, "rev-parse", "--path-format=absolute", "--git-common-dir"], { encoding: "utf8" }).trim(), "..");
for (const m of part.media || []) {
  const to = join(VIDEO, m.to);
  mkdirSync(dirname(to), { recursive: true });
  if (!existsSync(to)) copyFileSync(existsSync(join(REPO, m.from)) ? join(REPO, m.from) : join(MAIN, m.from), to);
  if (m.lastFrame && !existsSync(join(VIDEO, m.lastFrame))) {
    // Decode the last second and keep overwriting one PNG, which leaves the final frame
    // (the video track can end before the audio, so a seek close to the end finds nothing).
    execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-sseof", "-1.5", "-i", to, "-update", "1", join(VIDEO, m.lastFrame)], { stdio: "inherit" });
  }
}

// ── Keep each composition's root duration and size equal to its scene ───
function setRoot(file, id, duration) {
  const path = join(VIDEO, file);
  if (!existsSync(path)) return;
  let html = readFileSync(path, "utf8");
  html = html.replace(new RegExp(`(data-composition-id="${id}"[^>]*?data-duration=")[0-9.]+(")`), `$1${duration}$2`)
    .replace(/(class="clip" data-start="0" data-duration=")[0-9.]+(")/g, `$1${duration}$2`)
    .replace(new RegExp(`(data-composition-id="${id}"[^>]*?data-width=")[0-9]+(")`), `$1${W}$2`)
    .replace(new RegExp(`(data-composition-id="${id}"[^>]*?data-height=")[0-9]+(")`), `$1${H}$2`);
  writeFileSync(path, html);
}
for (const sc of scenes) setRoot(sc.file, sc.id, sc.duration);
setRoot("compositions/captions.html", "captions", DURATION);

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
        data-width="${W}"
        data-height="${H}"
      ></div>`,
  )
  .join("\n");

const index = `<!doctype html>
<!-- Generated by tools/build-part.mjs from parts/${part.id}.json. Do not edit; edit the part file or the compositions. -->
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=${W}, height=${H}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: ${W}px; height: ${H}px; overflow: hidden; background: #000; }
      #root { position: relative; width: ${W}px; height: ${H}px; overflow: hidden; background: #112845; }
      .scene { position: absolute; inset: 0; width: 100%; height: 100%; }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="${DURATION}"
      data-width="${W}"
      data-height="${H}"
    >
${sceneDivs}
${BURN_CAPTIONS ? `      <div
        id="el-captions"
        class="scene clip"
        data-composition-id="captions"
        data-composition-src="compositions/captions.html"
        data-track-kind="captions"
        data-start="0"
        data-duration="${DURATION}"
        data-track-index="4"
        data-width="${W}"
        data-height="${H}"
      ></div>
` : ""}      <audio
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

console.log(`${part.id} (${ASPECT}): ${DURATION}s, ${scenes.length} scenes, ${words.length} words, ${mouth.length} mouth shapes, ${blinks.length} blinks, ${BURN_CAPTIONS ? `${shownCaptions.length} burned-in caption groups` : `captions in data/${part.id}.srt`}, ${sounds.length} sounds`);
for (const sc of scenes) console.log(`  ${sc.id} ${sc.start.toFixed(2)} +${sc.duration.toFixed(2)}`);
