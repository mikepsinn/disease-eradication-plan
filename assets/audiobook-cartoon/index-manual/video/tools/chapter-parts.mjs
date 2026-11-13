// Write a chapter's storyboards/parts.json from its beat sheets: each part starts where its first
// scene's cue words are spoken, in the chapter's word timings (tools/word-timings.mjs --chapter).
//
//   node tools/chapter-parts.mjs --chapter <slug> [path to assets/audiobook/manual-paperback]
//
// Parts are taken in part-number order. Part 1 starts at 0 (the theme song) and the last part runs
// to the end of the MP3 (the outro). A boundary sits in the pause before the cue word. A cue phrase
// can recur (a heading quoted again later), so the occurrence nearest where the part should start is
// taken: after the theme song, plus the spoken words of the parts before it (their tables). A part
// whose cue is not found near there is placed by that word count, and reported.
import { execFileSync } from "node:child_process";
import { existsSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, join, resolve } from "node:path";
import { BOARDS, IS_EP1, PLAN, REPO, SLUG, chapterMp3 } from "./chapter.mjs";

if (IS_EP1) throw new Error("episode 1's parts.json is kept by hand: pass --chapter <slug>");
const main = resolve(execFileSync("git", ["-C", REPO, "rev-parse", "--path-format=absolute", "--git-common-dir"], { encoding: "utf8" }).trim(), "..");
const AUDIOBOOK = resolve(process.argv[2] ?? (existsSync(join(REPO, "assets/audiobook/manual-paperback/mp3")) ? join(REPO, "assets/audiobook/manual-paperback") : join(main, "assets/audiobook/manual-paperback")));
const MP3 = chapterMp3(AUDIOBOOK);
if (!MP3) throw new Error(`no MP3 for ${SLUG} in ${AUDIOBOOK}`);
const total = Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", MP3], { encoding: "utf8" }));
const words = JSON.parse(readFileSync(join(PLAN, "word-timings.json"), "utf8"));
const norm = (s) => s.toLowerCase().replace(/[^a-z0-9%$]/g, "");
const toks = words.map((w) => norm(w.word));
const round = (x) => Math.round(x * 1000) / 1000;
const THEME_END = 99.9;

const files = readdirSync(BOARDS)
  .filter((f) => /^part-\d+-.*\.md$/.test(f))
  .sort((a, b) => Number(a.match(/^part-(\d+)/)[1]) - Number(b.match(/^part-(\d+)/)[1]));
const firstChapterWord = words.findIndex((w) => w.start >= THEME_END);
let expected = Math.max(0, firstChapterWord);
let from = 0, placedByCount = 0;
const parts = [];
for (const file of files) {
  const md = readFileSync(join(BOARDS, file), "utf8").replace(/\r\n/g, "\n");
  const n = Number(file.match(/^part-(\d+)/)[1]);
  const title = (md.match(/^part: \d+, "(.*)"\s*$/m) || [, file.replace(/^part-\d+-|\.md$/g, "")])[1];
  const cueLine = (md.match(/\n## Scene \d+ · [^\n]*\n[\s\S]*?^- cue: (.*)$/m) || [, ""])[1];
  const quoted = [...cueLine.matchAll(/["“]([^"”]+)["”]/g)].map((m) => m[1]);
  const want = (quoted.at(-1) || "").split(/\s+/).map(norm).filter(Boolean);
  // The words the part speaks, from its tables' quoted lines (the voiceover lines are rewritten from
  // the audio by tools/storyboard-times.mjs, so they follow the windows rather than set them).
  const said = [...md.matchAll(/^\| "([^|]*)" \|/gm)].map((m) => m[1]).join(" ").split(/\s+/).map(norm).filter(Boolean).length;
  const hits = [];
  for (let k = from; want.length && k < toks.length; k++) if (want.every((t, j) => toks[k + j] === t)) hits.push(k);
  let hit = hits.length ? hits.reduce((a, b) => (Math.abs(b - expected) < Math.abs(a - expected) ? b : a)) : -1;
  if (hit >= 0 && Math.abs(hit - expected) > Math.max(150, said)) hit = -1;
  if (hit < 0 && parts.length === 0) hit = expected;
  else if (hit < 0) {
    console.error(`${file}: first cue ${JSON.stringify(quoted.at(-1) || cueLine)} not found near word ${expected}; placed by word count`);
    placedByCount++;
    hit = Math.max(from, Math.min(expected, toks.length - 1));
  }
  const prev = words[hit - 1];
  const start = parts.length === 0 ? 0 : round(prev ? Math.max(prev.end, words[hit].start - 0.25) : words[hit].start);
  if (parts.length) parts[parts.length - 1].end = start;
  parts.push({ n, slug: file.replace(/^part-\d+-|\.md$/g, ""), title, start, end: null, file });
  from = hit + 1;
  expected = hit + said;
}
if (parts.length) parts[parts.length - 1].end = round(total);
writeFileSync(join(BOARDS, "parts.json"), JSON.stringify({ audio: basename(MP3), parts }, null, 1) + "\n");
const r = Math.round(total);
console.log(`${SLUG}: ${parts.length} parts, ${Math.floor(r / 60)}:${String(r % 60).padStart(2, "0")}${placedByCount ? `, ${placedByCount} placed by word count` : ""}`);
