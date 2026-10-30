// Photograph a storyboard review sheet (tools/storyboard-sheet.mjs output) in headless Chrome: one PNG per
// scene frame, named by scene, to check the sketches without opening a browser.
//
//   node tools/sheet-shot.mjs storyboards/part-NN-*.html
//
// Frames go to snapshots/sheets/<sheet name>/NN-<scene id>.png (1920 x 1080). Exits 1 on a page error.
import { mkdirSync } from "node:fs";
import { createRequire } from "node:module";
import { basename, dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const VIDEO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const require = createRequire(join(VIDEO, "package.json"));
const puppeteer = require("puppeteer-core");
const CHROME = process.env.CHROME || "C:/Users/m/.cache/puppeteer/chrome-headless-shell/win64-148.0.7778.97/chrome-headless-shell-win64/chrome-headless-shell.exe";
const sheet = resolve(VIDEO, process.argv[2]);
const out = join(VIDEO, "snapshots/sheets", basename(sheet, ".html"));
mkdirSync(out, { recursive: true });

const browser = await puppeteer.launch({ executablePath: CHROME, args: ["--allow-file-access-from-files"] });
const page = await browser.newPage();
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
await page.goto(pathToFileURL(sheet).href, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
// Each scene is an <article class="cell" data-scene="<id>"> whose first <svg viewBox="0 0 1920 1080"> is its frame;
// draw each one alone at full size.
const svgs = await page.evaluate(() => Array.from(document.querySelectorAll("article.cell")).map((c) => ({
  id: c.dataset.scene || c.id,
  html: c.querySelector("svg[viewBox='0 0 1920 1080']").outerHTML,
})));
const defs = await page.evaluate(() => Array.from(document.querySelectorAll("svg")).filter((s) => !s.getAttribute("viewBox") || s.getAttribute("viewBox") !== "0 0 1920 1080").map((s) => s.outerHTML).join(""));
const styles = await page.evaluate(() => Array.from(document.querySelectorAll("style")).map((s) => s.outerHTML).join(""));
await page.setViewport({ width: 1920, height: 1080 });
for (let i = 0; i < svgs.length; i++) {
  const html = `<!doctype html><html><head><meta charset="utf-8"><base href="${pathToFileURL(dirname(sheet)).href}/">${styles}<style>*{margin:0}body{width:1920px;height:1080px;overflow:hidden}body>svg[viewBox]{width:1920px;height:1080px;display:block}</style></head><body><div style="display:none">${defs}</div>${svgs[i].html}</body></html>`;
  await page.setContent(html, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  const name = `${String(i + 1).padStart(2, "0")}-${(svgs[i].id || "frame").replace(/[^a-z0-9-]/gi, "")}.png`;
  await page.screenshot({ path: join(out, name) });
  console.log(join(out, name));
}
await browser.close();
for (const e of errors) console.log(`ERROR: ${e}`);
process.exit(errors.length ? 1 : 0);
