// Write the fonts' character widths into kit.js (between "text-widths:begin" and "text-widths:end"), so that
// KIT.textWidth and KIT.fitText measure text the same way in scenes and in the storyboard sketches, which have no
// browser to measure in. The widths are measured in headless Chrome, as the render draws them. Rerun after
// changing a font in assets/fonts/.
//
//   node tools/text-widths.mjs
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { createRequire } from "node:module";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const VIDEO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const puppeteer = createRequire(join(VIDEO, "package.json"))("puppeteer-core");
const CHROME = process.env.CHROME || "C:/Users/m/.cache/puppeteer/chrome-headless-shell/win64-148.0.7778.97/chrome-headless-shell-win64/chrome-headless-shell.exe";
// name: [family, file, weight]
const FONTS = {
  Oswald: ["Oswald", "Oswald-SemiBold.woff2", 600],
  Fraunces: ["Fraunces", "Fraunces-Black-Soft.woff2", 900],
  Inter: ["Inter", "Inter-Variable.woff2", 400],
  InterBold: ["Inter", "Inter-Variable.woff2", 700],
};
// Printable ASCII, then the other characters the cartoon's signs use.
const CHARS = Array.from({ length: 95 }, (_, i) => String.fromCharCode(32 + i)).join("") + "×÷–—‘’“”•…é°½¢€£→←↑↓✓✗";

const faces = Object.values(FONTS).map(([family, file, weight]) =>
  `@font-face{font-family:"${family}";src:url("${pathToFileURL(join(VIDEO, "assets/fonts", file)).href}") format("woff2");font-weight:${weight === 400 || weight === 700 ? "100 900" : weight}}`).join("\n");
const browser = await puppeteer.launch({ executablePath: CHROME, args: ["--allow-file-access-from-files"] });
const page = await browser.newPage();
// A file page, so Chrome loads the fonts from disk.
const html = join(mkdtempSync(join(tmpdir(), "text-widths-")), "fonts.html");
writeFileSync(html, `<!doctype html><style>${faces}</style>${Object.values(FONTS).map(([f, , w]) => `<span style="font-family:${f};font-weight:${w}">x</span>`).join("")}`);
await page.goto(pathToFileURL(html).href, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
const missing = await page.evaluate((fonts) => Object.values(fonts).filter(([f, , w]) => !document.fonts.check(`${w} 20px "${f}"`)).map(([f]) => f), FONTS);
if (missing.length) throw new Error(`fonts did not load: ${missing.join(", ")}`);
const widths = await page.evaluate((fonts, chars) => {
  const ctx = document.createElement("canvas").getContext("2d");
  const out = {};
  for (const [name, [family, , weight]] of Object.entries(fonts)) {
    ctx.font = `${weight} 1000px "${family}"`;
    out[name] = [...chars].map((ch) => Math.round(ctx.measureText(ch).width));
  }
  return out;
}, FONTS, CHARS);
await browser.close();

const block = [
  "  // text-widths:begin (written by tools/text-widths.mjs: each character's advance in thousandths of the font size)",
  `  var TEXT_CHARS = ${JSON.stringify(CHARS)};`,
  "  var TEXT_WIDTHS = {",
  ...Object.entries(widths).map(([name, w]) => `    ${name}: [${w.join(",")}],`),
  "  };",
  "  // text-widths:end",
].join("\n");
const kitPath = join(VIDEO, "assets/js/kit.js");
const kit = readFileSync(kitPath, "utf8");
const re = /  \/\/ text-widths:begin[\s\S]*?  \/\/ text-widths:end/;
if (!re.test(kit)) throw new Error("kit.js has no text-widths:begin/end block");
writeFileSync(kitPath, kit.replace(re, () => block));
console.log(`kit.js: widths for ${CHARS.length} characters in ${Object.keys(FONTS).length} fonts`);
