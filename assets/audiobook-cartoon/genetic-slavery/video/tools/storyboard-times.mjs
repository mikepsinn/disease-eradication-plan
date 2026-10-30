// Fill in each storyboard scene's time and narration from its cue words.
//
//   node tools/storyboard-times.mjs [storyboards/part-NN-*.md ...]   (default: every part in parts.json)
//
// Each scene's "- cue:" line quotes the narration's own words where the scene starts (the last
// quoted phrase on the line is the one matched). Cues are found in order, inside the part's
// window from storyboards/parts.json, in ../word-timings.json. The tool rewrites each scene's
// "- time:" and "- voiceover:" lines and the part's "audio:" and "duration:" lines, so none of
// them is ever typed by hand. A scene runs until the next one starts; the last one, to the
// part's end. Exits 1 if a cue is not found.
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const VIDEO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const BOARDS = join(VIDEO, "storyboards");
const { audio, parts } = JSON.parse(readFileSync(join(BOARDS, "parts.json"), "utf8"));
const words = JSON.parse(readFileSync(join(VIDEO, "../word-timings.json"), "utf8"));
const norm = (s) => s.toLowerCase().replace(/[^a-z0-9%$]/g, "");
const toks = words.map((w) => norm(w.word));

function mmss(t) {
  const r = Math.round(t * 10) / 10;
  return `${String(Math.floor(r / 60)).padStart(2, "0")}:${(r % 60).toFixed(1).padStart(4, "0")}`;
}
function cuePhrase(line) {
  const quoted = [...line.matchAll(/["“]([^"”]+)["”]/g)].map((m) => m[1]);
  return quoted.length ? quoted[quoted.length - 1] : null;
}
function setField(block, key, value, after) {
  const re = new RegExp(`^- ${key}: .*$`, "m");
  if (re.test(block)) return block.replace(re, () => `- ${key}: ${value}`);
  return block.replace(new RegExp(`^(- ${after}: .*)$`, "m"), (m) => `${m}\n- ${key}: ${value}`);
}

const files = process.argv.length > 2 ? process.argv.slice(2).map((f) => resolve(VIDEO, f)) : parts.map((p) => join(BOARDS, p.file)).filter(existsSync);
let failed = false;
for (const file of files) {
  const part = parts.find((p) => p.file === basename(file));
  if (!part) {
    console.error(`${basename(file)}: not in parts.json`);
    failed = true;
    continue;
  }
  const md = readFileSync(file, "utf8").replace(/\r\n/g, "\n");
  const pieces = md.split(/(?=\n## Scene \d+ · )/);
  const head = pieces[0];
  const blocks = pieces.slice(1);
  const lo = words.findIndex((w) => w.start >= part.start - 0.05);
  let from = lo;
  const starts = [];
  const problems = [];
  blocks.forEach((block, i) => {
    const name = block.match(/## Scene \d+ · (.+)/)[1].trim();
    const cueLine = (block.match(/^- cue: (.*)$/m) || [, ""])[1];
    const phrase = cuePhrase(cueLine);
    if (!phrase) {
      if (i === 0) return starts.push({ t: part.start, i: lo });
      problems.push(`${name}: no quoted cue phrase`);
      return starts.push(null);
    }
    const want = phrase.split(/\s+/).map(norm).filter(Boolean);
    let hit = -1;
    for (let k = from; k < toks.length && words[k].start < part.end; k++) {
      if (want.every((t, j) => toks[k + j] === t)) {
        hit = k;
        break;
      }
    }
    if (hit < 0) {
      problems.push(`${name}: cue "${phrase}" not found after ${mmss(words[from]?.start ?? part.start)}`);
      return starts.push(null);
    }
    from = hit + 1;
    starts.push({ t: i === 0 ? part.start : words[hit].start, i: i === 0 ? lo : hit });
  });
  if (problems.length) {
    failed = true;
    console.error(`${basename(file)}:\n  ${problems.join("\n  ")}`);
    continue;
  }
  const out = blocks.map((block, i) => {
    const s = starts[i].t;
    const e = i + 1 < blocks.length ? starts[i + 1].t : part.end;
    const said = words.filter((w) => w.start >= s - 0.01 && w.start < e - 0.01).map((w) => w.word).join(" ");
    let b = setField(block, "time", `${mmss(s)} to ${mmss(e)} (${(e - s).toFixed(1)} s)`, "cue");
    b = setField(b, "voiceover", said ? `"${said}"` : "none (music)", "time");
    return b;
  });
  let newHead = head.replace(/^audio: .*$/m, `audio: ${audio}, ${mmss(part.start)} to ${mmss(part.end)}`);
  const d = part.end - part.start;
  newHead = newHead.replace(/^duration: .*$/m, `duration: ${Math.floor(d / 60)}:${(d % 60).toFixed(1).padStart(4, "0")}`);
  writeFileSync(file, newHead + out.join(""));
  const lengths = starts.map((s, i) => (i + 1 < starts.length ? starts[i + 1].t : part.end) - s.t);
  const long = blocks.map((b, i) => [b.match(/## Scene \d+ · (.+)/)[1].trim(), lengths[i]]).filter(([, l]) => l > 45 || l < 1.5);
  console.log(`${basename(file)}: ${blocks.length} scenes, ${mmss(part.start)}–${mmss(part.end)}${long.length ? `; check length: ${long.map(([n, l]) => `${n} ${l.toFixed(1)} s`).join(", ")}` : ""}`);
}
process.exit(failed ? 1 : 0);
