// Check one scene on its own in headless Chrome, without a build: load the scene's template with its part's
// data (data/<part-id>.js, from `node tools/build-part.mjs parts/<part-id>.json --data-only`) in either shape,
// report page errors, and save frames plus a contact sheet. Safe to run while other parts build or render.
//
//   node tools/scene-check.mjs <part-id> <scene-id> [--aspect 9x16] [--at 0.5,2,4.2 | --frac 0.05,0.5,0.95] [--out dir]
//
// Frames go to snapshots/scene-check/<scene-id>-<aspect>-<time>.png and the sheet to
// snapshots/scene-check/<scene-id>-<aspect>-sheet.png (git-ignored). Exits 1 on a page error.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const VIDEO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const require = createRequire(join(VIDEO, "package.json"));
const puppeteer = require("puppeteer-core");
const CHROME = process.env.CHROME || "C:/Users/m/.cache/puppeteer/chrome-headless-shell/win64-148.0.7778.97/chrome-headless-shell-win64/chrome-headless-shell.exe";

const [partId, id] = process.argv.slice(2);
const opt = (name) => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : null; };
const aspect = opt("--aspect") || "16x9";
const [W, H] = aspect === "9x16" ? [1080, 1920] : [1920, 1080];
const out = resolve(opt("--out") || join(VIDEO, "snapshots/scene-check"));
mkdirSync(out, { recursive: true });

const part = JSON.parse(readFileSync(join(VIDEO, "parts", `${partId}.json`), "utf8"));
const sc = part.scenes.find((s) => s.id === id);
if (!sc) throw new Error(`No scene ${id} in parts/${partId}.json`);
let inner = readFileSync(join(VIDEO, sc.file), "utf8").replace(/^[\s\S]*?<template[^>]*>/, "").replace(/<\/template>\s*$/, "");
inner = inner.replace('<script src="data/part.js"></script>', `<script src="data/${partId}.js"></script>`)
  .replace('<script src="data/aspect.js"></script>', `<script>window.HF_ASPECT = "${aspect}";</script>`);
const page0 = join(out, `${id}-${aspect}.html`);
writeFileSync(page0, `<!doctype html><html><head><meta charset="utf-8"><base href="${pathToFileURL(VIDEO).href}/"><style>*{margin:0}body{width:${W}px;height:${H}px;overflow:hidden;background:#000}</style><script>window.__timelines={}</script></head><body>${inner}</body></html>`);

const browser = await puppeteer.launch({ executablePath: CHROME, args: ["--allow-file-access-from-files"] });
const page = await browser.newPage();
await page.setViewport({ width: W, height: H });
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
await page.goto(pathToFileURL(page0).href);
await new Promise((r) => setTimeout(r, 1200));
const info = await page.evaluate((id) => {
  var tl = window.__timelines[id], d = (window.HF_PART.scenes.find(function (s) { return s.id === id; }) || {}).duration;
  return { hasTimeline: !!tl, timeline: tl ? tl.duration() : 0, scene: d };
}, id);
if (!info.hasTimeline) errors.push(`no window.__timelines["${id}"]`);
const D = info.scene || info.timeline;
const times = opt("--at") ? opt("--at").split(",").map(Number) : (opt("--frac") || "0.03,0.25,0.5,0.75,0.97").split(",").map((f) => +f * D);
const shots = [];
for (const t of times) {
  if (info.hasTimeline) await page.evaluate((id, t) => { window.__timelines[id].seek(t, false); }, id, t);
  await new Promise((r) => setTimeout(r, 250));
  const file = join(out, `${id}-${aspect}-${t.toFixed(2)}.png`);
  await page.screenshot({ path: file });
  shots.push({ file, t });
}
// The contact sheet: every frame, small, with its time.
const cols = aspect === "9x16" ? Math.min(5, shots.length) : Math.min(3, shots.length), cw = aspect === "9x16" ? 300 : 560, ch = Math.round((cw * H) / W);
const sheet = join(out, `${id}-${aspect}-sheet.html`);
writeFileSync(sheet, `<!doctype html><html><body style="margin:0;background:#fff;font:600 16px sans-serif;display:grid;grid-template-columns:repeat(${cols},${cw}px);gap:6px;padding:6px">` +
  shots.map((s) => `<div><img src="${pathToFileURL(s.file).href}" style="width:${cw}px;height:${ch}px;display:block"><div>${id} ${aspect} t=${s.t.toFixed(2)}s</div></div>`).join("") + "</body></html>");
await page.setViewport({ width: cols * (cw + 6) + 6, height: Math.ceil(shots.length / cols) * (ch + 28) + 6 });
await page.goto(pathToFileURL(sheet).href);
await new Promise((r) => setTimeout(r, 300));
const sheetPng = join(out, `${id}-${aspect}-sheet.png`);
await page.screenshot({ path: sheetPng, fullPage: true });
await browser.close();
console.log(`${partId}/${id} ${aspect}: scene ${info.scene?.toFixed(2)}s, timeline ${info.timeline.toFixed(2)}s, ${shots.length} frames`);
console.log(`sheet: ${sheetPng}`);
if (info.timeline && info.scene && info.timeline > info.scene + 0.05) console.log(`note: the timeline runs ${(info.timeline - info.scene).toFixed(2)}s past the scene (cut off)`);
for (const e of errors) console.log(`ERROR: ${e}`);
process.exit(errors.length ? 1 : 0);
