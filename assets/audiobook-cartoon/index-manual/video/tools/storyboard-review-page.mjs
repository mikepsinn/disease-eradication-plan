// One self-contained review page for the whole episode's storyboards: every part and scene as a
// text card (no sketches), the vertical shorts, and a Comment button on each scene for when the
// page is published as an artifact with the comments capability.
//
//   node tools/storyboard-review-page.mjs <out.html>
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const VIDEO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const BOARDS = join(VIDEO, "storyboards");
const FONTS = join(VIDEO, "assets/fonts");
const { audio, parts } = JSON.parse(readFileSync(join(BOARDS, "parts.json"), "utf8"));
const shorts = existsSync(join(BOARDS, "shorts.json")) ? JSON.parse(readFileSync(join(BOARDS, "shorts.json"), "utf8")) : [];

const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const inline = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/`(.+?)`/g, "<code>$1</code>");
const mmss = (t) => `${Math.floor(Math.round(t) / 60)}:${String(Math.round(t) % 60).padStart(2, "0")}`;
const span = (t) => (t || "").replace(/ \(.*\)$/, "").split(" to ").map((x) => x.replace(/^0(\d:)/, "$1")).join("–");

const sections = [];
let total = 0;
for (const p of parts) {
  const md = readFileSync(join(BOARDS, p.file), "utf8").replace(/\r\n/g, "\n");
  const front = Object.fromEntries(md.split("\n---\n")[0].replace(/^---\n/, "").split("\n").map((l) => [l.slice(0, l.indexOf(":")).trim(), l.slice(l.indexOf(":") + 1).trim().replace(/^"(.*)"$/, "$1")]));
  const scenes = md.split(/\n## Scene \d+ · /).slice(1).map((block, i) => {
    const f = { n: i + 1 };
    for (const l of block.split("\n")) {
      const m = l.match(/^- (\w+): (.*)$/);
      if (m) f[m[1]] = m[2];
    }
    const paras = block.split("\n\n").slice(1).map((x) => x.trim()).filter((x) => x && !x.startsWith("- "));
    f.paras = paras;
    f.onScreen = (paras.find((x) => x.startsWith("On screen:")) || "").replace(/^On screen:\s*/, "").split(/\.\s+(?=No:|Why:)/)[0];
    return f;
  });
  total += scenes.length;
  const cards = scenes.map((f) => `<article class="card" id="${esc(f.id)}" data-comment-target>
  <div class="row"><span class="name">${String(p.n).padStart(2, "0")}.${String(f.n).padStart(2, "0")} · ${esc(f.id)}</span><span class="when">${esc((f.layer || "").split(",")[0])} · ${esc(span(f.time))}</span></div>
  <p class="what">${inline(f.scene || "")}</p>
  ${f.onScreen ? `<p class="screen"><span>On screen</span> ${inline(f.onScreen)}</p>` : ""}
  <div class="foot"><span class="chip">${esc(f.transition_in || "")}</span><button type="button" class="comment" id="comment-${esc(f.id)}">Comment</button></div>
  <details><summary>Narration and moves</summary><p class="vo">${inline(f.voiceover || "")}</p>${f.wishonia ? `<p><strong>Wishonia:</strong> ${inline(f.wishonia)}</p>` : ""}${f.paras.map((x) => `<p>${inline(x)}</p>`).join("")}</details>
</article>`).join("\n");
  sections.push({ p, front, count: scenes.length, html: `<section class="part" id="part-${p.n}">
<h2><span class="pn">Part ${p.n}</span> ${esc(p.title)}</h2>
<p class="meta">${mmss(p.start)} · ${mmss(p.end - p.start)} · ${scenes.length} scenes</p>
${front.message ? `<p class="msg">${inline(front.message)}</p>` : ""}
<div class="cards">${cards}</div>
</section>` });
}

const font = (family, file, weight) => `@font-face{font-family:"${family}";src:url("data:font/woff2;base64,${readFileSync(join(FONTS, file)).toString("base64")}") format("woff2");font-weight:${weight};font-display:swap}`;
const toc = sections.map(({ p, count }) => `<li><a href="#part-${p.n}"><span>${p.n}</span> ${esc(p.title)}</a><em>${mmss(p.start)} · ${count}</em></li>`).join("");
const shortRows = shorts.map((sh) => `<li><a href="#${esc(sh.from)}">${esc(sh.name)}</a> <em>Part ${sh.part}: ${esc(sh.from)} → ${esc(sh.to)}</em><span>${inline(sh.why)}</span></li>`).join("");
const end = parts[parts.length - 1].end;

const page = `<title>Episode 1 Storyboard</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
${font("Fraunces", "Fraunces-Black-Soft.woff2", 900)}
${font("Oswald", "Oswald-SemiBold.woff2", 600)}
${font("Inter", "Inter-Variable.woff2", "100 900")}
/* Layout: a long reading column of parts, each a grid of scene cards; contents and shorts up top. */
:root{
  --bg:#E8E6EE; --surface:#F7F6FA; --fg:#1A1426; --muted:#5D5872; --rule:#CFCBDA; --accent:#C7361F; --chip:#E0DDEA; --teal:#157F78;
  --display:"Fraunces", Georgia, serif; --label:"Oswald", "Arial Narrow", sans-serif; --body:"Inter", system-ui, sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#13111B;--surface:#1D1A27;--fg:#EEEAF6;--muted:#A6A0B9;--rule:#34304A;--accent:#F08A24;--chip:#2A2638;--teal:#5FC7BE;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#13111B;--surface:#1D1A27;--fg:#EEEAF6;--muted:#A6A0B9;--rule:#34304A;--accent:#F08A24;--chip:#2A2638;--teal:#5FC7BE;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:15px;line-height:1.5;margin:0}
.wrap{max-width:1280px;margin:0 auto;padding-block:32px 72px;padding-left:max(16px, env(safe-area-inset-left, 0px));padding-right:max(16px, env(safe-area-inset-right, 0px))}
.kicker{font-family:var(--label);text-transform:uppercase;letter-spacing:.08em;font-size:14px;color:var(--muted);margin:0}
h1{font-family:var(--display);font-weight:900;font-size:clamp(34px,5vw,58px);line-height:1;margin:6px 0 10px;text-wrap:balance}
.dek{margin:0 0 6px;max-width:70ch}
.tag{font-family:var(--label);letter-spacing:.05em;font-size:14px;color:var(--muted);margin:0 0 22px;font-variant-numeric:tabular-nums}
.top{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:18px;margin-bottom:28px}
.panel{background:var(--surface);border:1px solid var(--rule);border-radius:8px;padding:16px 18px;min-width:0}
.panel h2{font-family:var(--label);font-weight:600;text-transform:uppercase;letter-spacing:.06em;font-size:15px;margin:0 0 10px}
.toc,.shorts{list-style:none;margin:0;padding:0;display:grid;gap:4px}
.toc li{display:flex;justify-content:space-between;gap:10px;font-size:14px}
.toc a,.shorts a{color:var(--fg);text-decoration:none;border-bottom:1px solid var(--rule)}
.toc a:hover,.shorts a:hover{border-color:var(--accent)}
.toc a span{font-family:var(--label);color:var(--muted);display:inline-block;min-width:1.6em}
.toc em,.shorts em{font-style:normal;color:var(--muted);font-size:13px;font-variant-numeric:tabular-nums;white-space:nowrap}
.shorts li{display:grid;gap:1px;padding:5px 0;border-bottom:1px dashed var(--rule)}
.shorts a{font-family:var(--label);letter-spacing:.03em;font-size:15px;justify-self:start}
.shorts span{font-size:13.5px}
.part{margin-top:34px}
.part h2{font-family:var(--display);font-weight:900;font-size:clamp(24px,3vw,34px);margin:0;padding-top:8px;border-top:2px solid var(--fg);text-wrap:balance}
.pn{font-family:var(--label);font-weight:600;font-size:.5em;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);vertical-align:middle;margin-right:6px}
.meta{font-family:var(--label);letter-spacing:.04em;font-size:14px;color:var(--muted);margin:2px 0 4px;font-variant-numeric:tabular-nums}
.msg{margin:0 0 12px;max-width:72ch;font-style:italic}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,360px),1fr));gap:12px}
.card{background:var(--surface);border:1px solid var(--rule);border-radius:8px;padding:12px 14px;display:grid;gap:6px;align-content:start;min-width:0}
.row{display:flex;justify-content:space-between;gap:8px;font-family:var(--label);letter-spacing:.03em;font-size:14px;font-variant-numeric:tabular-nums}
.name{font-weight:600;overflow-wrap:anywhere}
.when{color:var(--muted);white-space:nowrap}
.what{margin:0}
.screen{margin:0;font-size:14px;color:var(--teal)}
.screen span{font-family:var(--label);text-transform:uppercase;letter-spacing:.05em;font-size:12px;color:var(--muted);margin-right:4px}
.foot{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.chip{font-family:var(--label);font-size:12px;letter-spacing:.05em;text-transform:uppercase;background:var(--chip);border-radius:999px;padding:2px 9px}
.comment{display:none;margin-left:auto;font:600 12.5px var(--body);color:var(--fg);background:transparent;border:1.5px solid var(--fg);border-radius:999px;padding:3px 11px;cursor:pointer}
.can-comment .comment{display:inline-block}
.comment:hover{background:var(--fg);color:var(--surface)}
.comment:focus-visible,summary:focus-visible,a:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
details{font-size:14px;border-top:1px solid var(--rule);padding-top:5px}
summary{cursor:pointer;font-family:var(--label);letter-spacing:.04em;text-transform:uppercase;font-size:12.5px;color:var(--muted)}
details p{margin:7px 0 0}
.vo{font-style:italic}
code{font-size:.92em}
</style>
<div class="wrap">
<p class="kicker">How to End War and Disease (for Busy People) · Episode 1 cartoon</p>
<h1>Episode 1 Storyboard</h1>
<p class="dek">Every scene of the cartoon, part by part, timed to the episode audio. Each card says what we see, the words on screen and the transition into it; open a card for its narration and the moves on each word. Scene names are stable: use them in feedback.</p>
<p class="tag">${parts.length} parts · ${total} scenes · ${mmss(end)} · audio ${esc(audio)}</p>
<div class="top">
  <div class="panel"><h2>Parts</h2><ol class="toc">${toc}</ol></div>
  <div class="panel"><h2>Vertical shorts</h2><ul class="shorts">${shortRows}</ul></div>
</div>
${sections.map((s) => s.html).join("\n")}
</div>
<script>
(async () => {
  let comments = null;
  try { comments = await window.claude?.use?.("comments"); } catch (e) { comments = null; }
  if (!comments) return;
  document.body.classList.add("can-comment");
  document.addEventListener("click", async (e) => {
    const btn = e.target.closest("button.comment");
    if (!btn) return;
    try {
      await comments.openComposer({ element: btn.closest(".card") });
    } catch (err) {
      if (err && (err.code === "unavailable" || err.code === "not_granted")) document.body.classList.remove("can-comment");
    }
  });
})();
</script>
`;
writeFileSync(resolve(process.argv[2]), page);
console.log(`${process.argv[2]}: ${parts.length} parts, ${total} scenes, ${(page.length / 1024).toFixed(0)} KB`);
