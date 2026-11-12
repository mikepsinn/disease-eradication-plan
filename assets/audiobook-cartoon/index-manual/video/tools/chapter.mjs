// Which chapter a tool works on, and where its files are. Every chapter tool takes --chapter <slug>
// (default index-manual, episode 1). Episode 1 keeps its files where they always were; any other
// chapter's plan lives in assets/audiobook-cartoon/<slug>/ (word-timings.json, storyboards/), and
// the kit, art and scenes are shared from episode 1's video/ folder.
import { existsSync, readdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export const VIDEO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
export const EP1 = resolve(VIDEO, "..");
export const CARTOONS = resolve(EP1, "..");
export const REPO = resolve(CARTOONS, "../..");

const i = process.argv.indexOf("--chapter");
export const SLUG = i > 0 ? process.argv[i + 1] : "index-manual";
if (i > 0) process.argv.splice(i, 2);
export const IS_EP1 = SLUG === "index-manual";
export const PLAN = IS_EP1 ? EP1 : join(CARTOONS, SLUG);
export const BOARDS = IS_EP1 ? join(VIDEO, "storyboards") : join(PLAN, "storyboards");

// The chapter's published MP3 (theme song, chapter, outro), from the main checkout's audiobook folder.
export function chapterMp3(audiobook) {
  const dir = join(audiobook, "mp3");
  if (!existsSync(dir)) return null;
  const hit = readdirSync(dir).find((f) => new RegExp(`^${SLUG.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\.[0-9a-f]{8}\\.mp3$`).test(f));
  return hit ? join(dir, hit) : null;
}
