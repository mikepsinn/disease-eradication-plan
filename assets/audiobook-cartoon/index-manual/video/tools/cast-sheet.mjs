// The cast sheet: every recurring human from KIT.CAST, two everyday humans and the moods, drawn
// large with the kit, so the designs can be reviewed before animating.
//
//   node tools/cast-sheet.mjs <out.html>
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const VIDEO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const FONTS = join(VIDEO, "assets/fonts");
const sandbox = { window: {}, document: { createElement: () => ({}), head: { appendChild() {} } } };
vm.runInNewContext(readFileSync(join(VIDEO, "assets/js/kit.js"), "utf8"), sandbox);
const K = sandbox.window.KIT;
const C = K.C;

const at = (x, y, s, inner) => `<g transform="translate(${x},${y}) scale(${s})">${inner}</g>`;
const label = (x, y, text, size = 26) => `<text x="${x}" y="${y}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="${size}" letter-spacing="1" fill="${C.line}">${text}</text>`;
const frame = (id, inner, alt) => `<figure><div class="frame"><svg viewBox="0 0 1920 1080" role="img" aria-label="${alt}">${K.paper(id)}${inner}</svg></div><figcaption>${alt}</figcaption></figure>`;

const castRow = [
  ["richHuman", "RICH HUMAN"], ["politician", "POLITICIAN"], ["lobbyist", "LOBBYIST"], ["weaponsMaker", "WEAPONS MAKER"], ["orderly", "ORDERLY"],
];
const castRow2 = [["grandma", "GRANDMA"], ["loudHuman", "LOUD HUMAN"], ["scientist", "SCIENTIST"]];
const everyday = [
  [{ tone: 1, outfit: "shirt", color: 0, mood: "smile" }, "EVERYDAY: SHIRT"],
  [{ tone: 3, outfit: "dress", color: 2, hair: 1, mood: "smile" }, "EVERYDAY: DRESS"],
];
const cast1 = castRow.map(([n, l], i) => at(220 + i * 370, 470, 2.1, K.cast(n, { mood: n === "politician" ? "smile" : "flat" })) + label(220 + i * 370, 720, l)).join("");
const cast2 = castRow2.map(([n, l], i) => at(220 + i * 370, 560, 2.1, K.cast(n, { mood: "smile" })) + label(220 + i * 370, 820, l)).join("") +
  everyday.map(([o, l], i) => at(1330 + i * 370, 560, 2.1, K.person(o)) + label(1330 + i * 370, 820, l)).join("");
const moods = [
  [{ tone: 0, outfit: "shirt", color: 0, mood: "smile" }, "SMILE"],
  [{ tone: 1, outfit: "dress", color: 3, hair: 1, mood: "eager", look: "right", arms: [[30, 30], [60, 70]] }, "EAGER, LOOKING RIGHT"],
  [{ tone: 2, outfit: "suit", mood: "sad", light: "red", arms: [[10, 5], [-10, -5]] }, "SAD (CHEST LIGHT RED)"],
  [{ tone: 3, outfit: "overalls", color: 1, mood: "cross", arms: [[-60, -150], [-20, -10]] }, "CROSS, ARM UP"],
  [{ tone: 1, outfit: "labcoat", hair: 2, mood: "flat", light: "teal", arms: [[25, 60], [-25, -60]] }, "FLAT (LIGHT TEAL)"],
];
const moodRow = moods.map(([o, l], i) => at(220 + i * 370, 640, 2.6, K.person(o)) + label(220 + i * 370, 960, l, 24)).join("");

const font = (family, file, weight) => `@font-face{font-family:"${family}";src:url("data:font/woff2;base64,${readFileSync(join(FONTS, file)).toString("base64")}") format("woff2");font-weight:${weight};font-display:block}`;
const page = `<title>Episode 1 Cast Sheet</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
${font("Fraunces", "Fraunces-Black-Soft.woff2", 900)}
${font("Oswald", "Oswald-SemiBold.woff2", 600)}
${font("Inter", "Inter-Variable.woff2", "100 900")}
/* Layout: a header and three large 16:9 frames stacked, two across on wide screens. */
:root{--bg:#E8E6EE;--surface:#F7F6FA;--fg:#1A1426;--muted:#5D5872;--rule:#CFCBDA;--display:"Fraunces",Georgia,serif;--label:"Oswald","Arial Narrow",sans-serif;--body:"Inter",system-ui,sans-serif}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#13111B;--surface:#1D1A27;--fg:#EEEAF6;--muted:#A6A0B9;--rule:#34304A;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#13111B;--surface:#1D1A27;--fg:#EEEAF6;--muted:#A6A0B9;--rule:#34304A;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:15px;line-height:1.5;margin:0}
.wrap{max-width:1500px;margin:0 auto;padding-block:32px 64px;padding-left:max(16px, env(safe-area-inset-left, 0px));padding-right:max(16px, env(safe-area-inset-right, 0px))}
.kicker{font-family:var(--label);text-transform:uppercase;letter-spacing:.08em;font-size:14px;color:var(--muted);margin:0}
h1{font-family:var(--display);font-weight:900;font-size:clamp(32px,5vw,56px);line-height:1;margin:6px 0 10px}
.dek{max-width:70ch;margin:0 0 22px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,640px),1fr));gap:20px}
figure{margin:0;display:grid;gap:6px;min-width:0}
.frame{aspect-ratio:16/9;max-width:100%;border-radius:6px;overflow:hidden;box-shadow:0 0 0 1px var(--rule),0 6px 18px rgba(16,12,30,.18)}
.frame svg{display:block;width:100%;height:100%}
figcaption{font-family:var(--label);text-transform:uppercase;letter-spacing:.05em;font-size:14px;color:var(--muted)}
</style>
<div class="wrap">
<p class="kicker">How to End War and Disease (for Busy People) · Episode 1 cartoon</p>
<h1>Cast Sheet</h1>
<p class="dek">The humans as the theme song draws them: stereotypes you read from the silhouette, sharp and angular, drawn with the production kit. Each recurring character has its own shape, face and props; the chest light keeps the meat-robot joke.</p>
<div class="grid">
${frame("c1", label(960, 120, "THE RECURRING HUMANS", 40) + cast1, "The recurring humans: Rich Human, Politician, Lobbyist, Weapons Maker, Orderly")}
${frame("c2", label(960, 120, "MORE HUMANS", 40) + cast2, "Grandma, the Loud Human, a scientist and two everyday humans")}
${frame("c3", label(960, 120, "MOODS AND POSES", 40) + moodRow, "Moods and poses: smile, eager, sad, cross, flat")}
</div>
</div>
`;
writeFileSync(resolve(process.argv[2]), page);
console.log(`${process.argv[2]}: ${(page.length / 1024).toFixed(0)} KB`);
