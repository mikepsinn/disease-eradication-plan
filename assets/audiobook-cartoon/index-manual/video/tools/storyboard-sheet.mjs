// Build the review sheet for one part's storyboard: one still frame per scene, at its key moment,
// drawn with the production art in assets/js/kit.js and the real Wishonia sprites.
//
//   node tools/storyboard-sheet.mjs storyboards/part-01-opening.md [--inline <out.html>]
//   node tools/storyboard-sheet.mjs storyboards/part-01-opening.md --alt storyboards/part-01-opening.1950s.sketch.mjs [--inline <out.html>]
//
// Writes storyboards/<name>.html next to the .md: no scripts, sprites and fonts by relative path,
// so it opens from file:// in a checkout. --inline also writes a self-contained copy (sprites and
// fonts embedded, a Comment button on each scene) for publishing as a page people comment on.
// The drawings for each scene are in storyboards/<name>.sketch.mjs.
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join, relative, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import vm from "node:vm";

const VIDEO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const REPO = resolve(VIDEO, "../../../..");
const SPRITES = join(REPO, "transmit/public/assets/sprites/alien");
const FONTS = join(VIDEO, "assets/fonts");
const mdPath = resolve(VIDEO, process.argv[2]);
const inlineAt = process.argv.indexOf("--inline");
const inlineOut = inlineAt > 0 ? resolve(process.argv[inlineAt + 1]) : null;
// --alt <sketch module> (one or more): instead of the sheet, a side-by-side page of the scenes the
// modules redraw in other styles, next to the current version (storyboards/<name>.<--name or compare>.html).
const altPaths = process.argv.flatMap((a, i, all) => (a === "--alt" ? [resolve(VIDEO, all[i + 1])] : []));
const nameAt = process.argv.indexOf("--name");
const htmlOut = mdPath.replace(/\.md$/, altPaths.length ? `.${nameAt > 0 ? process.argv[nameAt + 1] : "compare"}.html` : ".html");

// ── The kit, run outside a browser (its drawing functions only return strings) ──
const sandbox = { window: {}, document: { createElement: () => ({}), head: { appendChild() {} } } };
vm.runInNewContext(readFileSync(join(VIDEO, "assets/js/kit.js"), "utf8"), sandbox);
const K = sandbox.window.KIT;
const C = K.C;

// ── Storyboard markdown ──────────────────────────────────────────────────
const md = readFileSync(mdPath, "utf8").replace(/\r\n/g, "\n");
const front = Object.fromEntries(
  md.split("\n---\n")[0].replace(/^---\n/, "").split("\n").map((l) => {
    const i = l.indexOf(":");
    return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^"(.*)"$/, "$1")];
  }),
);
const decided = (md.match(/## Decided\n\n([\s\S]*?)\n\n(?=\*\*|## )/) || [, ""])[1]
  .split("\n").map((l) => l.replace(/^\d+\.\s*/, "")).filter(Boolean);
const bans = (md.match(/\*\*Bans for this part\.\*\*\n([\s\S]*?)\n\n/) || [, ""])[1]
  .split("\n").filter((l) => l.startsWith("- ")).map((l) => l.slice(2));
const changes = [...md.matchAll(/## (Changes from v\d+)\n\n([\s\S]*?)\n\n(?=## )/g)].map((m) => ({
  title: m[1], items: m[2].split("\n").filter((l) => l.startsWith("- ")).map((l) => l.slice(2)),
}));
const scenes = md.split(/\n## Scene \d+ · /).slice(1).map((block, i) => {
  const lines = block.split("\n");
  const f = { n: i + 1, name: lines[0].trim() };
  for (const l of lines) {
    const m = l.match(/^- (\w+): (.*)$/);
    if (m) f[m[1]] = m[2];
  }
  const paras = block.split("\n\n").slice(1).map((p) => p.trim()).filter((p) => !p.startsWith("- "));
  f.moves = (paras.find((p) => p.startsWith("Moves:")) || "").replace(/^Moves:\s*/, "");
  f.notes = paras.filter((p) => !p.startsWith("Moves:"));
  return f;
});

// ── Drawing helpers for the sketch modules ───────────────────────────────
function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
const usedSprites = new Set();
function sprite(name, x, y, w, h) {
  usedSprites.add(name);
  return `<use href="#spr-${name}" x="${x}" y="${y}" width="${w}" height="${h}"/>`;
}
// Other pictures (a repo path); the href is filled in per page, by relative path or embedded.
const images = [];
const H = {
  K, C, esc,
  image(file, x, y, w, h) {
    images.push(resolve(REPO, file));
    return `<image href="@@IMG${images.length - 1}@@" x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="xMidYMid slice"/>`;
  },
  // Wishonia at (x, y), w wide: the head (95% of w, centered) on the body, as in characters.js.
  wish(x, y, w, head, body) {
    const bodyTop = Math.round(w * 0.95 - (w * 12) / 140);
    return sprite(`body-${body}`, x, y + bodyTop, w, Math.round((w * 768) / 1343)) + sprite(head, x + Math.round(w * 0.025), y, Math.round(w * 0.95), Math.round(w * 0.95));
  },
  // The round corner frame of Layer B (same place as the pilot's scenes).
  pip(id, head, body = "idle") {
    const cx = 1760, cy = 740, r = 128;
    return `<defs><clipPath id="${id}-pip"><circle cx="${cx}" cy="${cy}" r="${r}"/></clipPath></defs>` +
      `<circle cx="${cx}" cy="${cy}" r="${r + 13}" fill="${C.line}"/><circle cx="${cx}" cy="${cy}" r="${r + 7}" fill="${C.cream}"/>` +
      `<g clip-path="url(#${id}-pip)"><circle cx="${cx}" cy="${cy}" r="${r}" fill="url(#sheet-pip-sky)"/>${H.wish(1620, 590, 280, head, body)}</g>`;
  },
  // A caption as the captions track shows it: the spoken words, the word being said highlighted.
  cap(text, active) {
    const words = text.split(" ");
    const lines = [];
    let line = [];
    for (const w of words) {
      if (line.join(" ").length + w.length > 46 && line.length) {
        lines.push(line);
        line = [];
      }
      line.push(w);
    }
    lines.push(line);
    const size = 46, lh = 56;
    const width = Math.min(1760, Math.max(...lines.map((l) => l.join(" ").length)) * size * 0.55 + 70);
    const top = 1030 - lines.length * lh - 20;
    let out = `<rect x="${960 - width / 2}" y="${top}" width="${width}" height="${lines.length * lh + 26}" rx="22" fill="${C.cream}" opacity="0.94" stroke="${C.ink}" stroke-width="3"/>`;
    lines.forEach((l, i) => {
      const spans = l.map((w) => (active && w.replace(/[^\w']/g, "").toLowerCase() === active ? `<tspan fill="${C.ink}" style="paint-order:stroke" stroke="${C.yellow}" stroke-width="14" stroke-linejoin="round">${esc(w)}</tspan>` : `<tspan>${esc(w)}</tspan>`)).join(" ");
      out += `<text x="960" y="${top + 52 + i * lh}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="${size}" fill="${C.ink}">${spans}</text>`;
    });
    return out;
  },
  // Big number or title type: Fraunces Black with a cream outline and an ink drop shadow.
  big(x, y, size, text, anchor = "middle", fill = C.ink) {
    const t = (dx, dy, extra) => `<text x="${x + dx}" y="${y + dy}" text-anchor="${anchor}" font-family="Fraunces" font-weight="900" font-size="${size}" ${extra}>${esc(text)}</text>`;
    return t(size * 0.05, size * 0.07, `fill="${C.ink}"`) + t(0, 0, `fill="${fill}" stroke="${C.cream}" stroke-width="${size * 0.09}" stroke-linejoin="round" style="paint-order:stroke"`);
  },
  // Oswald label.
  label(x, y, size, text, anchor = "middle", fill = C.line, extra = "") {
    return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Oswald" font-weight="600" font-size="${size}" letter-spacing="${size * 0.04}" fill="${fill}" ${extra}>${esc(text)}</text>`;
  },
  // Plain running text (Inter), one line per array item.
  text(x, y, size, lines, opts = {}) {
    const { anchor = "start", fill = C.line, weight = 500, lh = 1.25 } = opts;
    return lines.map((l, i) => `<text x="${x}" y="${y + i * size * lh}" text-anchor="${anchor}" font-family="Inter" font-weight="${weight}" font-size="${size}" fill="${fill}">${esc(l)}</text>`).join("");
  },
  at(x, y, s, inner, rot = 0) {
    return `<g transform="translate(${x},${y})${rot ? ` rotate(${rot})` : ""}${s !== 1 ? ` scale(${s})` : ""}">${inner}</g>`;
  },
  tick(x, y, s, color) {
    return K.tick(x, y, s, color).replace('stroke-dashoffset="1"', 'stroke-dashoffset="0"');
  },
  cross(x, y, s, color = C.line) {
    return `<path d="M${x + s * 0.18},${y + s * 0.18} L${x + s * 0.82},${y + s * 0.82} M${x + s * 0.82},${y + s * 0.18} L${x + s * 0.18},${y + s * 0.82}" stroke="${color}" stroke-width="${s * 0.14}" stroke-linecap="round"/>`;
  },
  // A paper bill with no accent color, for the papers before they take a side.
  plainMoney(legs) {
    return K.money("war", legs).replace(`fill="${C.war}"`, 'fill="#E9E1CC"').replace(/#8E1C17/g, C.line);
  },
  // The countdown board in the top-left corner, at video time t (104 per minute).
  board(t) {
    const n = String(Math.floor((t * 104) / 60)).padStart(6, "0");
    let digits = "";
    for (let i = 0; i < 6; i++) {
      digits += `<rect x="${44 + i * 76}" y="96" width="64" height="84" rx="6" fill="#2E2A36"/><text x="${76 + i * 76}" y="160" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="64" fill="${C.yellow}">${n[i]}</text><rect x="${44 + i * 76}" y="137" width="64" height="2" fill="#111"/>`;
    }
    return H.at(56, 52, 0.52,
      `<rect x="-4" y="-4" width="568" height="206" rx="16" fill="${C.paper}"/><rect x="0" y="0" width="560" height="198" rx="14" fill="#1E1B24" stroke="${C.line}" stroke-width="6"/>` +
      H.label(280, 38, 23, "HUMANS TERMINATED BY CURABLE DISEASES", "middle", C.paper) + H.label(280, 66, 23, "SINCE THIS VIDEO STARTED", "middle", C.paper) + digits);
  },
  // A 1950s mail-in form. items: [{ lines: [...], yes: true|false }]
  form(x, y, w, title, items, opts = {}) {
    const { size = 34, boxes = true } = opts;
    let h = 120;
    const blocks = items.map((it) => {
      const top = h;
      h += it.lines.length * size * 1.3 + (boxes ? 90 : 30);
      return { it, top };
    });
    let out = `<rect x="${x + 10}" y="${y + 12}" width="${w}" height="${h}" fill="${C.line}" opacity="0.85"/>` +
      `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#FBF5E4" stroke="${C.line}" stroke-width="5"/>` +
      `<rect x="${x + 14}" y="${y + 14}" width="${w - 28}" height="${h - 28}" fill="none" stroke="${C.line}" stroke-width="1.6"/>` +
      H.label(x + w / 2, y + 74, 44, title) + `<path d="M${x + 40},${y + 98} H${x + w - 40}" stroke="${C.line}" stroke-width="3"/>`;
    for (const { it, top } of blocks) {
      out += H.text(x + 44, y + top + size, size, it.lines, { weight: 600 });
      if (boxes) {
        const by = y + top + it.lines.length * size * 1.3 + 14;
        out += K.checkbox(x + 44, by, 46) + H.label(x + 108, by + 38, 32, "YES", "start") + K.checkbox(x + 220, by, 46) + H.label(x + 284, by + 38, 32, "NO", "start");
        if (it.yes) out += H.tick(x + 40, by - 8, 58, C.med);
      }
    }
    return out;
  },
};

const sketchPath = mdPath.replace(/\.md$/, ".sketch.mjs");
const sketches = (await import(pathToFileURL(sketchPath).href)).default;

// ── One frame per scene ──────────────────────────────────────────────────
const frames = scenes.map((f) => {
  const draw = sketches[f.id];
  if (!draw) throw new Error(`No sketch for ${f.id} in ${basename(sketchPath)}`);
  const fid = `f${String(f.n).padStart(2, "0")}`;
  const { svg, alt } = draw(H, fid);
  // The music video is footage; every drawn frame gets the print grain on top.
  const grain = f.id === "theme-music-video" ? "" : K.grain(fid);
  return { ...f, svg: `<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" role="img" aria-label="${esc(alt)}">${svg}${grain}</svg>` };
});
const ALTS = await Promise.all(altPaths.map(async (p) => (await import(pathToFileURL(p).href)).default));
const ALT = ALTS[0] || null;
// Extra frames that are not storyboard scenes (for example a close-up lineup), drawn by each module.
const wrapSvg = ({ svg, alt }) => `<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" role="img" aria-label="${esc(alt)}">${svg}</svg>`;
const extraPairs = ALT && ALT.extras ? Object.entries(ALT.extras).map(([id, x], i) => ({
  f: { n: 0, id, time: "", key: x.key },
  current: wrapSvg(x.current(H, `x${i}c`)),
  svgs: ALTS.map((a, k) => wrapSvg(a.extras[id].draw(H, `x${i}a${k}`))),
})) : [];
const pairs = ALT ? frames.filter((f) => ALTS.every((a) => a.scenes[f.id])).map((f) => ({
  f,
  svgs: ALTS.map((a, k) => {
    const { svg, alt } = a.scenes[f.id](H, `a${k}${String(f.n).padStart(2, "0")}`);
    return `<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" role="img" aria-label="${esc(alt)}">${svg}</svg>`;
  }),
})) : [];

// ── Sprites and fonts ────────────────────────────────────────────────────
function webp(file, width) {
  const dir = join(REPO, "assets/audiobook/cartoon/sheet-sprites");
  mkdirSync(dir, { recursive: true });
  const out = join(dir, `${basename(file, ".png")}-${width}.webp`);
  if (!existsSync(out)) {
    execFileSync("ffmpeg", ["-loglevel", "error", "-y", "-i", file, "-vf", `scale=${width}:-1`, "-c:v", "libwebp", "-pix_fmt", "yuva420p", "-quality", "82", out]);
  }
  return "data:image/webp;base64," + readFileSync(out).toString("base64");
}
function spriteDefs(inline) {
  return [...usedSprites].sort().map((name) => {
    const file = join(SPRITES, `${name}.png`);
    const [w, h] = name.startsWith("body-") ? [1343, 768] : [1024, 1024];
    const href = inline ? webp(file, name.startsWith("body-") ? 720 : 520) : relative(dirname(htmlOut), file).replace(/\\/g, "/");
    return `<symbol id="spr-${name}" viewBox="0 0 ${w} ${h}"><image href="${href}" width="${w}" height="${h}"/></symbol>`;
  }).join("");
}
function imageHref(file, inline) {
  if (!inline) return relative(dirname(htmlOut), file).replace(/\\/g, "/");
  const dir = join(REPO, "assets/audiobook/cartoon/sheet-images");
  mkdirSync(dir, { recursive: true });
  const out = join(dir, `${basename(file).replace(/\.\w+$/, "")}-480.jpg`);
  if (!existsSync(out)) execFileSync("ffmpeg", ["-loglevel", "error", "-y", "-i", file, "-vf", "scale=480:-1", "-q:v", "5", out]);
  return "data:image/jpeg;base64," + readFileSync(out).toString("base64");
}
function fontFaces(inline) {
  const faces = [["Fraunces", "Fraunces-Black-Soft.woff2", "900"], ["Oswald", "Oswald-SemiBold.woff2", "600"], ["Inter", "Inter-Variable.woff2", "100 900"]];
  return faces.map(([family, file, weight]) => {
    const src = inline ? `data:font/woff2;base64,${readFileSync(join(FONTS, file)).toString("base64")}` : relative(dirname(htmlOut), join(FONTS, file)).replace(/\\/g, "/");
    return `@font-face{font-family:"${family}";src:url("${src}") format("woff2");font-weight:${weight};font-display:block}`;
  }).join("\n");
}

// ── Page ────────────────────────────────────────────────────────────────
function inline(s) {
  return esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/`(.+?)`/g, "<code>$1</code>");
}
function firstMove(moves) {
  return moves.split(/(?<=\.)\s+(?=["A-Z])/)[0];
}
// "01:48.8 to 01:57.6 (8.7 s)" → "1:48.8–1:57.6"
const span = (t) => t.replace(/ \(.*\)$/, "").split(" to ").map((x) => x.replace(/^0(\d:)/, "$1")).join("–");
const seams = frames.map((f) => f.transition_in);
const acts = [];
for (const f of frames) {
  if (!acts.length || acts[acts.length - 1].name !== f.act) acts.push({ name: f.act, frames: [] });
  acts[acts.length - 1].frames.push(f);
}

function compareCells(inlineMode) {
  return [...extraPairs, ...pairs].map(({ f, svgs, current }) => {
    const nn = String(f.n).padStart(2, "0");
    return `<article class="cell pair" id="pair-${f.n ? nn : esc(f.id)}" data-scene="${esc(f.id)}" data-comment-target>
  <div class="meta"><span class="name">${f.n ? `${nn} · ` : ""}${esc(f.id)}</span><span class="when">${esc(span(f.time))}</span></div>
  <div class="sides">
    <figure><div class="frame">${current || f.svg}</div><figcaption>${esc(ALT.currentLabel || "Current")}</figcaption></figure>
    ${svgs.map((svg, k) => `<figure data-comment-target><div class="frame">${svg}</div><figcaption>${k + 1}. ${esc(ALTS[k].label)}</figcaption></figure>`).join("\n    ")}
  </div>
  <div class="foot"><span class="shows">Drawn: ${inline(f.key)}.</span>${inlineMode ? `<button type="button" class="comment" id="comment-${esc(f.id)}">Comment on ${esc(f.id)}</button>` : ""}</div>
</article>`;
  }).join("\n");
}

function page(inlineMode) {
  const cells = ALT ? compareCells(inlineMode) : acts.map((act) =>
    `<h2 class="act"><span>${esc(act.name)}</span><span class="act-count">${act.frames.length} ${act.frames.length === 1 ? "scene" : "scenes"}</span></h2>` +
    act.frames.map((f) => {
      const nn = String(f.n).padStart(2, "0");
      return `<article class="cell" id="frame-${nn}" data-scene="${esc(f.id)}" data-comment-target>
  <div class="frame">${f.svg}</div>
  <div class="meta"><span class="name">${nn} · ${esc(f.id)}</span><span class="when">${esc(f.layer.split(",")[0])} · ${esc(span(f.time))}</span></div>
  <p class="note"><strong>First:</strong> ${inline(firstMove(f.moves))} <span class="shows">Drawn: ${inline(f.key)}.</span></p>
  <div class="foot"><span class="chip" title="Transition into this scene">${esc(f.transition_in)}</span>${inlineMode ? `<button type="button" class="comment" id="comment-${esc(f.id)}">Comment on ${esc(f.id)}</button>` : ""}</div>
  <details><summary>Narration and moves</summary>
    <p class="vo">${inline(f.voiceover)}</p>
    <p><strong>Moves:</strong> ${inline(f.moves)}</p>
    ${f.notes.map((p) => `<p>${inline(p)}</p>`).join("")}
  </details>
</article>`;
    }).join("\n")).join("\n");

  const seamMap = frames.map((f, i) => `<li><span class="seam-name">${esc(f.id)}</span>${i + 1 < frames.length ? `<span class="seam-chip">${esc(frames[i + 1].transition_in)}</span>` : `<span class="seam-chip end">cut to The Human Economy</span>`}</li>`).join("");
  const palette = [["Murder-money red", C.war], ["Medicine teal", C.med], ["Engraving paper", C.paper], ["Line", C.line], ["Sunburst red", C.red], ["Orange", C.orange], ["Yellow", C.yellow], ["Periwinkle", C.peri], ["Grid cyan", C.cyan], ["Navy floor", C.navy]];

  return `<title>${ALT ? ALT.pageTitle || "Opening Style Comparison" : "Episode 1 Opening Storyboard"}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
${fontFaces(inlineMode)}
/* Layout: a contact sheet, three 16:9 frames across, grouped under act bars. */
:root{
  --bg:#E8E6EE; --surface:#F7F6FA; --fg:#1A1426; --muted:#5D5872; --rule:#CFCBDA; --accent:#C7361F; --chip:#E0DDEA;
  --display:"Fraunces", Georgia, serif; --label:"Oswald", "Arial Narrow", sans-serif; --body:"Inter", system-ui, sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#13111B;--surface:#1D1A27;--fg:#EEEAF6;--muted:#A6A0B9;--rule:#34304A;--accent:#F08A24;--chip:#2A2638;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#13111B;--surface:#1D1A27;--fg:#EEEAF6;--muted:#A6A0B9;--rule:#34304A;--accent:#F08A24;--chip:#2A2638;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:15px;line-height:1.5;margin:0}
.wrap{max-width:1560px;margin:0 auto;padding-block:32px 64px;padding-left:max(16px, env(safe-area-inset-left, 0px));padding-right:max(16px, env(safe-area-inset-right, 0px))}
header{display:grid;gap:12px;margin-bottom:28px;max-width:980px}
.kicker{font-family:var(--label);text-transform:uppercase;letter-spacing:.08em;font-size:14px;color:var(--muted);margin:0}
h1{font-family:var(--display);font-weight:900;font-size:clamp(34px,5vw,60px);line-height:1;margin:0;text-wrap:balance}
h1 .ver{font-family:var(--label);font-weight:600;font-size:.32em;letter-spacing:.06em;vertical-align:middle;color:var(--surface);background:var(--accent);border-radius:4px;padding:3px 8px;margin-left:10px}
.dek{margin:0;max-width:68ch;color:var(--fg)}
.tag{font-family:var(--label);letter-spacing:.05em;font-size:14px;color:var(--muted);margin:0;font-variant-numeric:tabular-nums}
.decided{margin:4px 0 0;padding:14px 18px;background:var(--surface);border:1px solid var(--rule);border-radius:8px}
.decided h2{font-family:var(--label);font-weight:600;text-transform:uppercase;letter-spacing:.06em;font-size:14px;margin:0 0 6px;color:var(--muted)}
.decided ol,.decided ul{margin:0;padding-left:20px;display:grid;gap:4px}
.how{margin:0;color:var(--muted);max-width:72ch}
.sheet{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,400px),1fr));gap:22px 20px}
.act{grid-column:1/-1;display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin:18px 0 -6px;padding-bottom:6px;border-bottom:2px solid var(--fg);font-family:var(--label);font-weight:600;text-transform:uppercase;letter-spacing:.06em;font-size:18px}
.act-count{font-size:13px;color:var(--muted)}
.cell{display:grid;gap:8px;align-content:start;min-width:0}
.frame{aspect-ratio:16/9;max-width:100%;border-radius:6px;overflow:hidden;box-shadow:0 0 0 1px var(--rule),0 6px 18px rgba(16,12,30,.18);background:#000}
.frame svg{display:block;width:100%;height:100%}
.meta{display:flex;justify-content:space-between;gap:8px;font-family:var(--label);letter-spacing:.04em;font-size:15px;font-variant-numeric:tabular-nums}
.meta .name{font-weight:600}
.meta .when{color:var(--muted);white-space:nowrap}
.note{margin:0;font-size:14px}
.shows{display:block;color:var(--muted);margin-top:2px}
.foot{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.chip{font-family:var(--label);font-size:12.5px;letter-spacing:.05em;text-transform:uppercase;background:var(--chip);border-radius:999px;padding:3px 10px;color:var(--fg)}
.comment{display:none;font:600 13px var(--body);color:var(--fg);background:transparent;border:1.5px solid var(--fg);border-radius:999px;padding:4px 12px;cursor:pointer;margin-left:auto}
.can-comment .comment{display:inline-block}
.comment:hover{background:var(--fg);color:var(--surface)}
.comment:focus-visible,summary:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
details{font-size:14px;border-top:1px solid var(--rule);padding-top:6px}
summary{cursor:pointer;font-family:var(--label);letter-spacing:.04em;text-transform:uppercase;font-size:13px;color:var(--muted)}
details p{margin:8px 0 0;max-width:70ch}
.vo{font-style:italic}
code{font-size:.92em}
.closing{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr));gap:20px;margin-top:36px}
.panel{background:var(--surface);border:1px solid var(--rule);border-radius:8px;padding:18px 20px;min-width:0}
.panel h2{font-family:var(--label);font-weight:600;text-transform:uppercase;letter-spacing:.06em;font-size:16px;margin:0 0 12px}
.seams{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px 4px;align-items:center}
.seams li{display:flex;align-items:center;gap:4px}
.seam-name{font-family:var(--label);font-size:14px}
.seam-chip{font-size:12px;color:var(--muted);border:1px dashed var(--rule);border-radius:999px;padding:1px 8px}
.seam-chip.end{border-style:solid}
.swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;margin:0 0 14px;padding:0;list-style:none}
.swatches li{display:flex;align-items:center;gap:8px;font-size:13px}
.swatches i{width:26px;height:26px;border-radius:4px;box-shadow:0 0 0 1px var(--rule);flex:none}
.types{display:grid;gap:6px;margin:0 0 14px}
.types p{margin:0}
.bans{margin:0;padding-left:18px;display:grid;gap:3px;font-size:14px}
.pairs{display:grid;gap:34px}
.pair{border-top:2px solid var(--fg);padding-top:10px}
.sides{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:16px}
.sides figure{margin:0;display:grid;gap:6px;min-width:0}
.sides figcaption{font-family:var(--label);text-transform:uppercase;letter-spacing:.05em;font-size:14px;color:var(--muted)}
@media (prefers-reduced-motion: reduce){*{transition:none!important}}
</style>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<radialGradient id="sheet-pip-sky" cx="50%" cy="70%" r="60%"><stop offset="0" stop-color="${C.yellow}"/><stop offset=".4" stop-color="${C.orange}"/><stop offset=".68" stop-color="${C.rust}"/><stop offset=".92" stop-color="${C.navy}"/></radialGradient>
${spriteDefs(inlineMode)}
</defs></svg>
<div class="wrap">
<header>
  <p class="kicker">How to End War and Disease (for Busy People) · Episode 1 cartoon</p>
  ${ALT ? `<h1>${ALTS.length > 1 ? esc(ALT.pageTitle) : `Part 1: current look vs ${esc(ALT.label)}`}</h1>
  <p class="dek">${esc(ALT.dek)}</p>
  ${ALTS.map((a, k) => `<div class="decided"><h2>${ALTS.length > 1 ? `${k + 1}. ${esc(a.label)}` : `What the ${esc(a.label)} version changes`}</h2><ul>${a.notes.map((d) => `<li>${inline(d)}</li>`).join("")}</ul></div>`).join("\n  ")}
  <p class="how">${pairs.length} scenes at the same key moment, layout and words${ALTS.length > 1 ? "; only the humans change" : ", one of each kind of shot"}. Comment on the version you prefer${inlineMode ? " with the Comment button, or the comment tool on any frame" : ""}.</p>` : `<h1>Part 1: Opening<span class="ver">${esc(front.version || "v1")}</span></h1>
  <p class="dek">${esc(front.message)}</p>
  <p class="tag">${esc(front.format.replace("x", " × "))} · ${esc(front.duration)} · ${frames.length} scenes · audio ${esc(front.audio)}</p>
  ${changes.map((c) => `<div class="decided"><h2>${esc(c.title)}</h2><ul>${c.items.map((d) => `<li>${inline(d)}</li>`).join("")}</ul></div>`).join("")}
  <div class="decided"><h2>Decided</h2><ol>${decided.map((d) => `<li>${inline(d)}</li>`).join("")}</ol></div>
  <p class="how">Each frame is the scene's key moment, drawn with the production art: placement, words and look. Nothing moves yet. Scenes are named; use the name in feedback.${inlineMode ? " Use a scene's Comment button, or the comment tool on any frame." : ""}</p>`}
</header>
<main class="${ALT ? "pairs" : "sheet"}">
${cells}
</main>
${ALT ? "" : `<section class="closing">
  <div class="panel"><h2>Transitions</h2><ul class="seams">${seamMap}</ul></div>
  <div class="panel"><h2>Tokens and bans</h2>
    <ul class="swatches">${palette.map(([n, c]) => `<li><i style="background:${c}"></i>${esc(n)} <code>${c}</code></li>`).join("")}</ul>
    <div class="types">
      <p><span style="font-family:var(--display);font-weight:900;font-size:22px">Fraunces Black</span> big numbers and titles</p>
      <p><span style="font-family:var(--label);font-weight:600;font-size:18px;text-transform:uppercase;letter-spacing:.04em">Oswald SemiBold</span> labels and signs</p>
      <p><span style="font-weight:700;font-size:17px">Inter</span> captions and form text</p>
    </div>
    <ul class="bans">${bans.map((b) => `<li>${inline(b)}</li>`).join("")}<li>Only red and teal on the engraving paper.</li></ul>
  </div>
</section>`}
</div>
`.replace(/@@IMG(\d+)@@/g, (_, i) => imageHref(images[Number(i)], inlineMode)) + `${inlineMode ? `<script>
(async () => {
  let comments = null;
  try { comments = await window.claude?.use?.("comments"); } catch (e) { comments = null; }
  if (!comments) return;
  document.body.classList.add("can-comment");
  document.addEventListener("click", async (e) => {
    const btn = e.target.closest("button.comment");
    if (!btn) return;
    try {
      await comments.openComposer({ element: btn.closest(".cell") });
    } catch (err) {
      if (err && (err.code === "unavailable" || err.code === "not_granted")) document.body.classList.remove("can-comment");
    }
  });
})();
</script>` : ""}
`;
}

writeFileSync(htmlOut, `<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n</head>\n<body>\n${page(false)}\n</body>\n</html>\n`);
console.log(`${relative(VIDEO, htmlOut)}: ${ALT ? `${pairs.length} pairs` : `${frames.length} frames`}, ${usedSprites.size} sprites`);
if (inlineOut) {
  mkdirSync(dirname(inlineOut), { recursive: true });
  writeFileSync(inlineOut, page(true));
  console.log(`${inlineOut}: ${(readFileSync(inlineOut).length / 1024).toFixed(0)} KB`);
}
