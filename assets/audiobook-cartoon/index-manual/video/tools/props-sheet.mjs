// Draw the shared props (assets/js/props/*.js) on review sheets: every entry in KIT.props.SHEET, four to a row,
// on the Layer B paper, in headless Chrome.
//
//   node tools/props-sheet.mjs [file-name-filter]
//
// A props file adds functions to KIT.props and lists samples for this sheet:
//   KIT.props.SHEET.push(["pillBottle", { face: "smile" }, "PILL BOTTLE (smiling)"]);
// Each prop is drawn around (0,0) standing on y 0. Sheets go to snapshots/props/<filter or all>-<n>.png.
import { mkdirSync, readdirSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const VIDEO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const require = createRequire(join(VIDEO, "package.json"));
const puppeteer = require("puppeteer-core");
const CHROME = process.env.CHROME || "C:/Users/m/.cache/puppeteer/chrome-headless-shell/win64-148.0.7778.97/chrome-headless-shell-win64/chrome-headless-shell.exe";
const filter = process.argv[2] || "";
const files = readdirSync(join(VIDEO, "assets/js/props")).filter((f) => f.endsWith(".js") && f.includes(filter)).sort();
const out = join(VIDEO, "snapshots/props");
mkdirSync(out, { recursive: true });
const page0 = join(out, "sheet.html");
writeFileSync(page0, `<!doctype html><html><head><meta charset="utf-8"><base href="${pathToFileURL(VIDEO).href}/">
<style>@font-face{font-family:"Oswald";src:url("assets/fonts/Oswald-SemiBold.woff2") format("woff2");font-weight:600}*{margin:0}body{width:1920px;height:1080px;overflow:hidden;background:#000}svg{display:block}</style>
<script>window.HF_PART={scenes:[],words:[],states:[],mouth:[],blinks:[],captions:[],sounds:[]};window.HF_ASPECT="16x9";window.__timelines={}</script>
<script src="assets/vendor/gsap.min.js"></script><script src="assets/js/kit.js"></script>
${files.map((f) => `<script src="assets/js/props/${f}"></script>`).join("\n")}
</head><body><div id="out"></div></body></html>`);
const browser = await puppeteer.launch({ executablePath: CHROME, args: ["--allow-file-access-from-files"] });
const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080 });
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
await page.goto(pathToFileURL(page0).href);
await new Promise((r) => setTimeout(r, 800));
const n = await page.evaluate(() => {
  var K = window.KIT, S = (K.props && K.props.SHEET) || [], frames = [];
  for (var i = 0; i < S.length; i += 8) {
    var cells = S.slice(i, i + 8).map(function (e, j) {
      var x = 240 + (j % 4) * 480, y = 470 + Math.floor(j / 4) * 470, art;
      try { art = K.props[e[0]](e[1] || {}); } catch (err) { art = '<text x="0" y="-60" text-anchor="middle" font-size="22" fill="#C8452E">' + err.message + "</text>"; }
      return '<g transform="translate(' + x + "," + y + ')">' + art + '</g><text x="' + x + '" y="' + (y + 50) + '" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="22" fill="#112845">' + (e[2] || e[0]) + "</text>";
    }).join("");
    frames.push(K.paper("ps" + i).replace("</svg>", cells + "</svg>"));
  }
  window.FRAMES = frames;
  return frames.length;
});
for (let i = 0; i < n; i++) {
  await page.evaluate((i) => { document.getElementById("out").innerHTML = window.FRAMES[i]; }, i);
  await page.evaluate(() => document.fonts.ready);
  await new Promise((r) => setTimeout(r, 250));
  const p = join(out, `${filter || "all"}-${i + 1}.png`);
  await page.screenshot({ path: p });
  console.log(p);
}
await browser.close();
for (const e of errors) console.log(`ERROR: ${e}`);
process.exit(errors.length ? 1 : 0);
