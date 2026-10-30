// Sketches for storyboards/part-14-decentralized-fda.md (v3, the 1950s atomic-age film): each scene's key moment on a
// 1920 x 1080 frame, drawn with the production art (kit.js, film.js and the props library through H.K). A host shot is
// H.host (the studio, Wishonia, the lectern) with its props in front; a plate frame is one framing as the camera sees
// it at that moment, the ground and the cast drawn large. Nothing important below y 900 (YouTube's captions).
// Built into the review sheet by tools/storyboard-sheet.mjs.
import { leashed } from "./part-09-unexplored-therapeutic-frontier.sketch.mjs";

// ── The recurring humans (the storyboard's fixed options) ──
const PAT = { tone: 2, outfit: "dress", hair: 1, color: 1, light: "red", mood: "worried" };
const DOC = { tone: 1, outfit: "labcoat", color: 1 };
const LAW = { tone: 3, outfit: "suit", color: 1, holdR: "briefcase" };
// Part 12's FDA official, exactly (hat: null, or the kit gives his suit a hat; the bowler is YOU's).
const OFFICIAL = { tone: 0, outfit: "suit", color: 1, hair: 2, glasses: true, hat: null, seed: 12 };
const YOU = { tone: 2, outfit: "suit", hat: "bowler" };

// ── Colors of the plates (KIT.C plus the reference plates' field and wall tones) ──
const FIELD = "#C8B07B", SKY = "#EFE3C4", WALL = "#E3CFA0", WALL2 = "#D9C79E", FLOOR = "#A97C52", WATER = "#5C6F8E", SAND = "#D8BF86";

const f1 = (n) => (Math.round(n * 10) / 10).toString();
// A deterministic generator (no Math.random).
function lcg(seed) {
  let s = seed >>> 0;
  return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
}
const copy = (a, b) => Object.assign({}, a, b || {});

// A person standing with its feet on `feet` at x, scale s, plus extra markup in person units.
function stand(H, o, x, feet, s, extra = "", flip = false) {
  const inner = H.K.person(o) + extra;
  return `<g transform="translate(${f1(x)},${f1(feet - 100 * s)}) scale(${flip ? -s : s},${s})">${inner}</g>`;
}
// The patient's mustard-and-orange striped scarf, at her neck (person units).
function scarf(K, o) {
  const r = K.rig(o), [nx, ny] = r.neck, C = K.C;
  let stripes = "";
  for (let i = 0; i < 4; i++) stripes += `<path d="M${f1(nx - 11 + i * 7)},${f1(ny - 3)} l3,9" stroke="${C.orange}" stroke-width="3"/>`;
  return `<path d="M${f1(nx - 13)},${f1(ny - 4)} H${f1(nx + 13)} L${f1(nx + 12)},${f1(ny + 6)} H${f1(nx - 12)} Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="2"/>${stripes}` +
    `<path d="M${f1(nx - 6)},${f1(ny + 5)} L${f1(nx - 14)},${f1(ny + 26)} L${f1(nx - 7)},${f1(ny + 27)} L${f1(nx - 1)},${f1(ny + 6)} Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="2"/>` +
    `<path d="M${f1(nx - 5)},${f1(ny + 12)} l-6,-2 M${f1(nx - 8)},${f1(ny + 19)} l-5,-2" stroke="${C.orange}" stroke-width="2.6"/>`;
}
function patient(H, x, feet, s, extra = {}, more = "", flip = false) {
  const o = copy(PAT, extra);
  return stand(H, o, x, feet, s, scarf(H.K, o) + more, flip);
}
// The doctor's head mirror and stethoscope (person units).
function docKit(K, o) {
  const r = K.rig(o), C = K.C, f = r.facing, [hx, hy] = r.head, [nx, ny] = r.neck;
  return `<path d="M${f1(hx - 16)},${f1(hy - 14)} Q${f1(hx)},${f1(hy - 20)} ${f1(hx + 16)},${f1(hy - 14)}" fill="none" stroke="${C.slate}" stroke-width="2.6"/>` +
    `<circle cx="${f1(hx + 7 * f)}" cy="${f1(hy - 16)}" r="7" fill="#DCE3E6" stroke="${C.line}" stroke-width="2"/><circle cx="${f1(hx + 7 * f)}" cy="${f1(hy - 16)}" r="2" fill="${C.line}"/>` +
    `<path d="M${f1(nx - 9)},${f1(ny + 2)} Q${f1(nx - 10)},${f1(ny + 26)} ${f1(nx + 2)},${f1(ny + 28)} Q${f1(nx + 11)},${f1(ny + 24)} ${f1(nx + 9)},${f1(ny + 2)}" fill="none" stroke="${C.line}" stroke-width="2.4"/>` +
    `<circle cx="${f1(nx + 3)}" cy="${f1(ny + 32)}" r="4" fill="#C9CFD3" stroke="${C.line}" stroke-width="2"/>`;
}
function doctor(H, x, feet, s, extra = {}, more = "", flip = false) {
  const o = copy(DOC, extra);
  return stand(H, o, x, feet, s, docKit(H.K, o) + more, flip);
}
// Cream title type with a navy drop shadow, as the period card sets it.
function titleType(x, y, size, text, C) {
  const t = (dx, dy, extra) => `<text x="${x + dx}" y="${y + dy}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${size}" letter-spacing="${size * 0.02}" ${extra}>${text}</text>`;
  return t(size * 0.035, size * 0.05, `fill="#06142A"`) + t(0, 0, `fill="${C.cream}" stroke="#D8CDAA" stroke-width="${size * 0.025}" style="paint-order:stroke"`);
}
// Fraunces number, navy on a light plate.
function bigNum(x, y, size, text, fill) {
  return `<text x="${x}" y="${y}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${size}" letter-spacing="${size * 0.03}" fill="${fill}">${text}</text>`;
}
function oswald(x, y, size, text, fill, anchor = "middle", extra = "") {
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Oswald" font-weight="600" font-size="${size}" letter-spacing="${size * 0.04}" fill="${fill}" ${extra}>${text}</text>`;
}
// A plain field under a cream sky.
function field(horizon, C, ground = FIELD, sky = SKY) {
  return `<rect width="1920" height="1080" fill="${ground}"/><rect width="1920" height="${horizon}" fill="${sky}"/><path d="M0,${horizon} H1920" stroke="#8E7A55" stroke-width="3" opacity="0.6"/>`;
}
// An interior: a wall, a rust baseboard and a floor from y floorY.
function room(floorY, wall, C, floor = FLOOR) {
  return `<rect width="1920" height="1080" fill="${floor}"/><rect width="1920" height="${floorY}" fill="${wall}"/>` +
    `<rect y="${floorY - 16}" width="1920" height="16" fill="${C.rust}"/><path d="M0,${floorY} H1920" stroke="${C.line}" stroke-width="3"/>`;
}
// Confetti and streamers of a ticker-tape parade over the frame.
function confetti(C, seed, n, y0, y1) {
  const r = lcg(seed), cols = [C.yellow, C.orange, C.cream, C.med, C.money, C.peri, "#FBF6E6"];
  let out = "";
  for (let i = 0; i < n; i++) {
    const x = r() * 1920, y = y0 + r() * (y1 - y0), a = r() * 180, w = 10 + r() * 12, h = 5 + r() * 6;
    out += `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(w)}" height="${f1(h)}" fill="${cols[i % cols.length]}" stroke="${C.line}" stroke-width="1.2" transform="rotate(${f1(a)} ${f1(x)} ${f1(y)})"/>`;
  }
  for (let i = 0; i < 9; i++) {
    const x = 80 + i * 215 + r() * 60, len = 160 + r() * 260;
    let d = `M${f1(x)},-10`;
    for (let k = 1; k <= 6; k++) d += ` Q${f1(x + (k % 2 ? 26 : -26))},${f1(-10 + (k - 0.5) * len / 6)} ${f1(x)},${f1(-10 + k * len / 6)}`;
    out += `<path d="${d}" fill="none" stroke="${C.line}" stroke-width="12" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${i % 2 ? "#FBF6E6" : C.yellow}" stroke-width="8" stroke-linecap="round"/>`;
  }
  return out;
}
// The brass stock ticker under its glass dome, standing on (x, y), about 120 wide.
function ticker(x, y, C) {
  return `<g transform="translate(${x},${y})">` +
    `<path d="M-60,0 L-52,-34 H52 L60,0 Z" fill="${C.tan}" stroke="${C.line}" stroke-width="4" stroke-linejoin="round"/>` +
    `<rect x="-30" y="-78" width="60" height="44" fill="${C.yellow}" stroke="${C.line}" stroke-width="4"/>` +
    `<circle cx="0" cy="-56" r="15" fill="${C.cream}" stroke="${C.line}" stroke-width="3"/><path d="M0,-56 L9,-64" stroke="${C.line}" stroke-width="3"/>` +
    `<path d="M-46,-34 V-110 Q-46,-152 0,-152 Q46,-152 46,-110 V-34" fill="#FFFFFF" fill-opacity="0.22" stroke="${C.line}" stroke-width="4"/>` +
    `<path d="M-32,-112 Q-30,-136 -10,-142" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.8"/>` +
    `<circle cx="0" cy="-156" r="7" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/></g>`;
}
// A strip of ticker tape from (x0, y0) curling down to (x1, y1).
function tape(x0, y0, x1, y1, C, wig = 40) {
  const mx = (x0 + x1) / 2, my = (y0 + y1) / 2;
  const d = `M${x0},${y0} C${x0 + wig},${y0 - 40} ${mx - wig},${my - 30} ${mx},${my} S${x1 + wig},${y1 - 40} ${x1},${y1}`;
  return `<path d="${d}" fill="none" stroke="${C.line}" stroke-width="14" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#FBF6E6" stroke-width="10" stroke-linecap="round"/>`;
}
// The coffee mug on the lectern (bottom on y).
function mug(K, x, y) { return K.mug(x, y - 70); }
// A paper bill (KIT.money) at (x, y), scale s, turned rot degrees.
function bill(K, kind, x, y, s, rot = 0, legs = 0) {
  return `<g transform="translate(${f1(x)},${f1(y)}) rotate(${rot}) scale(${s})">${K.money(kind, legs)}</g>`;
}
// A prop at (x, y) (its ground), scale s.
function prop(markup, x, y, s, rot = 0) {
  return `<g transform="translate(${f1(x)},${f1(y)})${rot ? ` rotate(${rot})` : ""} scale(${s})">${markup}</g>`;
}
// Motion lines: three short strokes.
function whoosh(x, y, len, ang, C, w = 5) {
  let out = "";
  for (let i = -1; i <= 1; i++) out += `<path d="M${x},${y + i * 22} l${f1(len * Math.cos(ang))},${f1(len * Math.sin(ang))}" stroke="${C.line}" stroke-width="${w}" stroke-linecap="round" opacity="0.7"/>`;
  return out;
}
// A thick red cross (the ✗ that flattens the committee), centered on (x, y), size s.
function bigX(x, y, s, C) {
  const p = (dx, dy) => `${f1(x + dx * s)},${f1(y + dy * s)}`;
  const d = `M${p(-60, -46)} L${p(-46, -60)} L${p(0, -14)} L${p(46, -60)} L${p(60, -46)} L${p(14, 0)} L${p(60, 46)} L${p(46, 60)} L${p(0, 14)} L${p(-46, 60)} L${p(-60, 46)} L${p(-14, 0)} Z`;
  return `<path d="${d}" fill="${C.war}" stroke="${C.line}" stroke-width="${f1(5 * s)}" stroke-linejoin="miter"/>`;
}
// A life jacket, about 60 wide, centered on (0, 0).
function lifeJacket(C) {
  return `<path d="M-30,-28 L-12,-34 L-6,-14 L6,-14 L12,-34 L30,-28 L32,30 L6,34 L4,-2 L-4,-2 L-6,34 L-32,30 Z" fill="${C.orange}" stroke="${C.line}" stroke-width="3.5" stroke-linejoin="miter"/>` +
    `<path d="M-31,4 H-5 M5,4 H31 M-31,18 H-5 M5,18 H31" stroke="${C.cream}" stroke-width="4"/>`;
}
// A swimmer bobbing high in the water: a person drawn with the waist on the water line wy and cut off there, a life
// jacket on the chest when `jacket` (person units, under the clip).
function swimmer(H, o, x, wy, s, id, jacket = false) {
  const vest = jacket ? `<g transform="translate(0,4) scale(0.62)">${lifeJacket(H.K.C)}</g>` : "";
  return `<defs><clipPath id="${id}"><rect x="${x - 200 * s}" y="${wy - 300 * s}" width="${400 * s}" height="${300 * s}"/></clipPath></defs>` +
    `<g clip-path="url(#${id})">${stand(H, o, x, wy + 78 * s, s, vest)}</g>` +
    `<path d="M${x - 46 * s},${wy} q${12 * s},${-8 * s} ${24 * s},0 t${24 * s},0 t${24 * s},0 t${24 * s},0" fill="none" stroke="#FBF6E6" stroke-width="4"/>`;
}
// Water bands from y0 down to y1.
function water(y0, y1, C) {
  let out = `<rect x="0" y="${y0}" width="1920" height="${y1 - y0}" fill="${WATER}"/>`;
  for (let y = y0 + 26; y < y1; y += 46) out += `<path d="M0,${y} q40,-10 80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0 t80,0" fill="none" stroke="#8FA4C0" stroke-width="3" opacity="0.6"/>`;
  return out;
}
// The approval cabinet (as Part 12 draws it), standing on (x, y), scale s; open: the door swung wide.
function cabinet(x, y, s, C, open) {
  const glass = `fill="#DDEBEA" fill-opacity="0.55" stroke="${C.line}" stroke-width="4"`;
  const door = open
    ? `<path d="M80,-300 L150,-320 L150,-40 L80,-30 Z" ${glass}/><path d="M100,-290 L132,-300" stroke="#FFFFFF" stroke-width="4" opacity="0.8"/>`
    : `<rect x="-70" y="-300" width="150" height="270" ${glass}/><path d="M-50,-280 L-20,-250" stroke="#FFFFFF" stroke-width="5" opacity="0.8"/>`;
  return `<g transform="translate(${x},${y}) scale(${s})">` +
    `<path d="M-74,0 L-66,-30 M74,0 L66,-30" stroke="${C.line}" stroke-width="8"/>` +
    `<rect x="-80" y="-310" width="160" height="282" fill="${C.cream}" stroke="${C.line}" stroke-width="5"/>` +
    `<rect x="-70" y="-300" width="140" height="262" fill="#B9C9C6"/>` +
    `<path d="M-70,-170 H70" stroke="${C.line}" stroke-width="4"/>` +
    (open ? "" : `<g transform="translate(0,-180)">${C ? "" : ""}</g>`) + door +
    `<rect x="-34" y="-28" width="68" height="16" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/></g>`;
}
// The hourglass on the cabinet (whole, or burst), standing on (x, y), scale s.
function hourglass(x, y, s, C, burst) {
  const g = burst
    ? `<path d="M-26,-6 L-10,-34 L-20,-46 M26,-6 L12,-30 L24,-48" fill="none" stroke="${C.line}" stroke-width="4"/>` + [[-40, -60], [-20, -80], [10, -90], [34, -70], [44, -40]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="5" fill="${C.yellow}" stroke="${C.line}" stroke-width="2"/>`).join("")
    : `<path d="M-24,-80 H24 L4,-42 L24,-6 H-24 L-4,-42 Z" fill="#E8F1F0" stroke="${C.line}" stroke-width="4" stroke-linejoin="round"/><path d="M-14,-12 H14 L0,-30 Z" fill="${C.yellow}"/>`;
  return `<g transform="translate(${x},${y}) scale(${s})"><rect x="-32" y="-6" width="64" height="10" fill="${C.tan}" stroke="${C.line}" stroke-width="3"/>${g}<rect x="-32" y="-92" width="64" height="10" fill="${C.tan}" stroke="${C.line}" stroke-width="3" ${burst ? 'transform="translate(-30,-40) rotate(-30)"' : ""}/></g>`;
}
// A wooden arrow sign on a post, pointing left, centered on (x, y) (the board's middle), w wide, h tall.
function arrowSign(x, y, w, h, text, C, size = 54) {
  const d = `M${x - w / 2},${y} L${x - w / 2 + h * 0.6},${y - h / 2} H${x + w / 2} V${y + h / 2} H${x - w / 2 + h * 0.6} Z`;
  return `<rect x="${x + w * 0.1 - 9}" y="${y + h / 2}" width="18" height="${900 - y - h / 2}" fill="${C.rust}" stroke="${C.line}" stroke-width="4"/>` +
    `<path d="${d}" fill="${C.tan}" stroke="${C.line}" stroke-width="6" stroke-linejoin="miter"/>` +
    `<path d="M${x - w / 2 + h * 0.6 + 10},${y - h / 2 + 12} H${x + w / 2 - 12}" stroke="#D5A574" stroke-width="5"/>` +
    (text ? oswald(x + h * 0.25, y + size * 0.36, size, text, C.line) : "");
}

export default {
  "decentralized-fda-title"(H) {
    const { K, C } = H;
    const cx = 960, cy = 300, rx = 200, ry = 62;
    const orbits = [0, 60, -60].map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = [[0, 0.6], [60, 2.5], [-60, 4.4]].map(([a, th]) => {
      const ex = rx * Math.cos(th), ey = ry * Math.sin(th), ar = (a * Math.PI) / 180;
      return bill(K, "war", cx + ex * Math.cos(ar) - ey * Math.sin(ar), cy + ex * Math.sin(ar) + ey * Math.cos(ar) - 6, 0.62);
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    // the little FDAs perched round the edges and corners of the card
    const spots = [[150, 110, -8], [470, 70, 6], [1430, 76, -5], [1780, 120, 9], [86, 330, 12], [1846, 340, -10], [96, 600, -6], [1830, 610, 8], [150, 880, 7], [1770, 880, -9], [560, 900, -4], [1350, 905, 5]];
    const little = spots.map(([x, y, r]) => `<g transform="translate(${x},${y}) rotate(${r})">${titleType(0, 0, 56, "FDA", C)}</g>`).join("");
    // the stamp coming down on the empty middle
    const stamp = prop(K.props.stamp({ text: "APPROVED", color: C.war }), 960, 850, 1.85) + whoosh(820, 700, 60, Math.PI / 2, C, 6) + whoosh(1100, 700, 60, Math.PI / 2, C, 6);
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus +
      titleType(960, 590, 96, "YOUR DECENTRALIZED", C) + `<ellipse cx="960" cy="872" rx="230" ry="14" fill="#0A1A33" opacity="0.5"/>` + little + stamp;
    return { svg, alt: "The navy period title card: YOUR DECENTRALIZED under the atom emblem, the FDA gone from the middle, a dozen little FDAs perched round the edges of the card and a big APPROVED stamp coming down on the empty middle." };
  },

  "home-planet"(H, id) {
    const { K, C } = H;
    // the tape curls up out of the ticker's dome; the parade rains from above (nothing spills over the lectern)
    const front = tape(900, 640, 1010, 470, C, 36) + ticker(900, 792, C) + mug(K, 580, 792) +
      `<path d="M660,792 L668,770 H790 L782,792 Z" fill="${C.med}" stroke="${C.line}" stroke-width="4"/>` +
      tape(958, 124, 990, 300, C, 26) + confetti(C, 41, 140, 0, 1000);
    const svg = H.host("happy-closed", "wide-gesture", front);
    return { svg, alt: "Host shot: Wishonia at her lectern, arms wide, eyes shut happily, while ticker tape and confetti rain down over the set; on the lectern a little brass ticker under a glass dome curls a strip of tape up into the air, and a streamer hangs off one of her antennae." };
  },

  "hen-on-safe-bottles"(H, id) {
    const { K, C } = H;
    const bottle = (x, y, s, rot = 0) => prop(K.props.pillBottle({ face: "smile", label: "SAFE" }), x, y, s, rot);
    const heapBack = [[2, 650, 300]].map(([n, y, sp]) => Array.from({ length: n }, (_, i) => bottle(1200 + (i - (n - 1) / 2) * sp, y, 1.5)).join("")).join("");
    const heapFront = [[5, 900, 96], [4, 775, 96]].map(([n, y, sp]) => Array.from({ length: n }, (_, i) => bottle(1200 + (i - (n - 1) / 2) * sp, y, 1.5)).join("")).join("");
    // the official sits on the top of the heap, elbows out like wings, a feather or two in the air
    const off = copy(OFFICIAL, { mood: "smug", arms: [[-70, 60], [70, -60]] });
    const on = K.rig(off).neck, bx0 = on[0] + 6, by0 = on[1] + 22;
    const badge = `<rect x="${f1(bx0)}" y="${f1(by0)}" width="22" height="12" fill="${C.yellow}" stroke="${C.line}" stroke-width="1.6"/><text x="${f1(bx0 + 11)}" y="${f1(by0 + 9.4)}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="8.5" fill="${C.line}">FDA</text>`;
    const offSvg = stand(H, off, 1200, 700, 2.3, badge);
    const feathers = [[1030, 420, -30], [1390, 380, 25]].map(([x, y, a]) => `<path transform="translate(${x},${y}) rotate(${a})" d="M0,0 Q14,-22 0,-44 Q-14,-22 0,0 Z M0,0 V-40" fill="#FBF6E6" stroke="${C.line}" stroke-width="3"/>`).join("");
    // the line in front: skeletons now, still reaching for the bottles
    const line = [[250, 0], [470, 1], [690, 2], [900, 3]].map(([x, t]) =>
      stand(H, { tone: t, outfit: t % 2 ? "dress" : "shirt", hair: t % 2, color: t, skeleton: true, look: "right", arms: [[20, 40], [75, 92]] }, x, 900, 2.1)).join("");
    const rolling = bottle(1530, 905, 1.5, 70) + whoosh(1600, 860, 60, 0, C, 4);
    const svg = field(560, C) + heapBack + offSvg + heapFront + feathers + line + rolling;
    return { svg, alt: "A plate on a bare field: the FDA official, bald and in glasses, sitting on a heap of smiling SAFE pill bottles like a hen on eggs, elbows out like wings; in front of the heap a line of grinning skeletons still reaching for the bottles, and one bottle rolling out from under him." };
  },

  "small-pieces-of-paper"(H, id) {
    const { K, C } = H;
    // the plain paper held out by a corner, like a dead mouse, its legs kicking
    const paper = `<path d="M1040,626 L1052,646" stroke="${C.line}" stroke-width="4"/>` + bill(K, "plain", 1078, 676, 1.25, 38, 1);
    const pat = patient(H, 1270, 1180, 2.7, { look: "left", mood: "eager", arms: [[-110, -150], [-20, -8]] });
    const doc = doctor(H, 1500, 1200, 2.7, { look: "left", mood: "eager", arms: [[-130, -160], [10, 4]] });
    const sci = stand(H, K.castOpts("scientist", { look: "left", arms: [[-120, -150], [-10, -4]], holdR: "clipboard" }), 1740, 1190, 2.7);
    const svg = H.host("skeptical-smile", "point-right", ticker(900, 792, C) + mug(K, 580, 792) + paper + pat + doc + sci);
    return { svg, alt: "Host shot: Wishonia at her lectern holding one plain paper out at arm's length by a corner, its little legs kicking; at her right the patient in her scarf, the doctor with his head mirror and the scientist crowd in, every head turned up to the paper." };
  },

  "subsidy-follows-patient"(H, id) {
    const { K, C } = H;
    const FL = 870;
    // the trial doors, a germ on each door's sign, a tally beside it; a doctor leans in the first, the scientist in the second
    const doorAt = (x, germCol, tally) => prop(K.props.door({ color: C.rust }), x, FL, 2.15) +
      `<rect x="${x - 70}" y="${FL - 560}" width="140" height="86" fill="#FBF6E6" stroke="${C.line}" stroke-width="5"/>` + prop(K.props.germ({ color: germCol }), x, FL - 482, 1.05) +
      `<path d="${Array.from({ length: tally }, (_, i) => `M${x + 150 + i * 14},${FL - 330} v46`).join(" ")}" stroke="${C.line}" stroke-width="6"/>`;
    const doors = doorAt(1130, "yellow", 3) + doorAt(1560, "peri", 4) + doorAt(1990, "orange", 2);
    const docIn = doctor(H, 1205, FL, 2.15, { look: "left", mood: "smile" });
    const sci = stand(H, K.castOpts("scientist"), 1630, FL, 2.15);
    // the patient walking right with her puppy paper at her heel, its $929 tag swinging
    const pat = patient(H, 880, FL, 2.3, { look: "right", mood: "smile", arms: [[14, 8], [-24, -14]] });
    const PX = 680;
    const pup = bill(K, "med", PX, FL - 70, 1.35, -6, 1) + `<path d="M${PX + 48},${FL - 92} q8,-10 18,-4" fill="none" stroke="${C.war}" stroke-width="6"/>` +
      prop(K.props.priceTag({ text: "$929", angle: 28 }), PX + 58, FL - 96, 1.6);
    // behind them: the burst bag and the grants officer flattened under footprints
    const desk = `<rect x="70" y="${FL - 150}" width="250" height="150" fill="${C.tan}" stroke="${C.line}" stroke-width="5"/><rect x="50" y="${FL - 170}" width="290" height="24" fill="${C.rust}" stroke="${C.line}" stroke-width="5"/>` +
      prop(K.props.sign({ text: "GRANTS OFFICE", fontSize: 30, height: 30 }), 195, FL - 170, 1.25);
    // squashed flat as a pancake where he stood, palm still out, blinking, tiny footprints across him
    const flat = `<g transform="translate(360,${FL}) scale(2.6,0.5) translate(0,-100)">${K.person({ tone: 0, outfit: "suit", color: 3, mood: "eager", look: "left", arms: [[-80, -90], [10, 4]] })}</g>` +
      [0, 1, 2, 3, 4, 5].map((i) => `<ellipse cx="${292 + i * 26}" cy="${FL - 70 + (i % 2) * 14}" rx="7" ry="4" fill="${C.line}" opacity="0.8"/>`).join("");
    const bag = `<path d="M440,${FL} L460,${FL - 40} L478,${FL - 8} L500,${FL - 52} L518,${FL - 6} L540,${FL - 34} L556,${FL}" fill="#C4A36E" stroke="${C.line}" stroke-width="5" stroke-linejoin="miter"/>` +
      prop(K.props.priceTag({ text: "$41,000", angle: 64 }), 510, FL - 40, 1.2);
    const svg = room(FL, WALL, C) + doors + docIn + sci + desk + flat + bag + pup + pat;
    return { svg, alt: "A plate of a long hallway of trial doors, each with a germ on its sign and a tally beside it, a doctor leaning in one doorway and the scientist in the next; the patient in her scarf walks past with a medicine paper trotting at her heel like a puppy, its $929 collar tag swinging; behind them the burst $41,000 bag and the grants officer flattened on the floor under tiny footprints." };
  },

  "clinical-terrarium"(H, id) {
    const { K, C } = H;
    const BT = 650;
    const bench = `<rect x="80" y="${BT}" width="1140" height="34" fill="${C.tan}" stroke="${C.line}" stroke-width="5"/><rect x="110" y="${BT + 34}" width="1080" height="400" fill="${C.slate}" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M400,${BT + 34} V1080 M700,${BT + 34} V1080 M1000,${BT + 34} V1080" stroke="${C.line}" stroke-width="4"/>`;
    // the lizard tank: sand, a water dish, a plastic plant, a heat lamp, and identical tidy humans
    const tank0 = 200, tank1 = 1060, tankTop = 300;
    const sand = `<rect x="${tank0}" y="${BT - 36}" width="${tank1 - tank0}" height="36" fill="${SAND}"/>`;
    const dish = `<ellipse cx="960" cy="${BT - 30}" rx="56" ry="14" fill="${C.cyan}" stroke="${C.line}" stroke-width="4"/>`;
    const plant = `<path d="M300,${BT - 30} q-40,-90 -20,-170 q20,60 20,170 M300,${BT - 30} q30,-110 70,-150 q-20,80 -60,150 M300,${BT - 30} q-10,-70 30,-110" fill="#7E9B5A" stroke="${C.line}" stroke-width="4"/>`;
    const lamp = `<path d="M560,${tankTop - 70} V${tankTop - 10}" stroke="${C.line}" stroke-width="6"/><path d="M500,${tankTop + 10} Q560,${tankTop - 40} 620,${tankTop + 10} Z" fill="${C.war}" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M520,${tankTop + 16} L470,${tankTop + 120} M560,${tankTop + 18} V${tankTop + 130} M600,${tankTop + 16} L650,${tankTop + 120}" stroke="${C.yellow}" stroke-width="5" opacity="0.6"/>`;
    const tidy = [400, 500, 620, 730, 840].map((x) => stand(H, { plain: true, outfit: "scrubs", tone: 1, mood: "smile" }, x, BT - 28, 1.15)).join("");
    const glass = `<rect x="${tank0}" y="${tankTop}" width="${tank1 - tank0}" height="${BT - tankTop}" fill="#DDEBEA" fill-opacity="0.3" stroke="${C.line}" stroke-width="6"/>` +
      `<path d="M${tank0 + 30},${tankTop + 30} L${tank0 + 110},${tankTop + 110} M${tank1 - 120},${tankTop + 24} L${tank1 - 60},${tankTop + 84}" stroke="#FFFFFF" stroke-width="7" opacity="0.7"/>` +
      `<rect x="${tank0 - 10}" y="${tankTop - 14}" width="${tank1 - tank0 + 20}" height="18" fill="${C.slate}" stroke="${C.line}" stroke-width="5"/>` +
      `<circle cx="1000" cy="${tankTop + 90}" r="46" fill="${C.yellow}" stroke="${C.line}" stroke-width="4"/>` + bigNum(1000, tankTop + 108, 44, "200", C.line);
    // the fat cat looming behind with long tweezers, the patient held up to his monocle
    const FCo = K.castOpts("richHuman", { look: "left", arms: [[22, 72], [-150, -175]], hold: null }), FS = 3.3, FX = 1580, FF = 1090;
    const fh = K.rig(FCo).hand[1], hx = FX + fh[0] * FS, hy = FF - 100 * FS + fh[1] * FS;
    const fc = stand(H, FCo, FX, FF, FS);
    // the patient dangles from the tweezer tips by her scarf, right in front of his monocle
    const PS = 1.2, PNX = 1380, PNY = 470, pn = K.rig(copy(PAT, { look: "right" })).neck;
    const pat = patient(H, PNX - pn[0] * PS, PNY - pn[1] * PS + 100 * PS, PS, { look: "right", mood: "worried", arms: [[-6, -2], [6, 2]] });
    const tweezers = `<path d="M${f1(hx)},${f1(hy)} L${PNX + 6},${PNY - 4} M${f1(hx + 6)},${f1(hy + 10)} L${PNX + 10},${PNY + 6}" stroke="${C.line}" stroke-width="13" stroke-linecap="round"/>` +
      `<path d="M${f1(hx)},${f1(hy)} L${PNX + 6},${PNY - 4} M${f1(hx + 6)},${f1(hy + 10)} L${PNX + 10},${PNY + 6}" stroke="#B9C1C7" stroke-width="7" stroke-linecap="round"/>`;
    const svg = room(BT + 34, WALL2, C, C.slate) + bench + sand + plant + dish + tidy + lamp + glass + fc + pat + tweezers;
    return { svg, alt: "A plate of a lab bench with a glass tank set up like a lizard terrarium (heat lamp, water dish, plastic plant) full of identical smiling tidy humans and a 200 sticker on the glass; behind the bench the fat cat holds the patient up in long tweezers to his monocle, looking at her red chest light." };
  },

  "life-jackets-handed-out"(H, id) {
    const { K, C } = H;
    const WY = 640;
    const beach = `<rect width="1920" height="1080" fill="${SAND}"/><rect width="1920" height="360" fill="${SKY}"/>` + water(360, 1080, C) +
      `<path d="M0,780 L420,700 L420,1080 L0,1080 Z" fill="${SAND}" stroke="${C.line}" stroke-width="4"/>`;
    // far swimmers as dots, near ones drawn, skulls among them; jackets flying down the line
    const r = lcg(5);
    let far = "";
    for (let i = 0; i < 46; i++) {
      const x = 470 + r() * 1440, y = 380 + r() * 150, s = 0.3 + (y - 380) / 400;
      far += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(9 * s + 3)}" fill="${i % 7 === 3 ? "#F1EAD6" : ["#F4E3CC", "#D9B48F", "#A87B57", "#6F4B33"][i % 4]}" stroke="${C.line}" stroke-width="2"/>` +
        `<g transform="translate(${f1(x)},${f1(y + 10 * s + 6)}) scale(${f1(0.3 * s + 0.12)})">${lifeJacket(C)}</g>`;
    }
    const near = [[600, 0, "shirt", 0], [830, 1, "dress", 1], [1390, 3, "shirt", 2], [1610, 0, "dress", 3], [1820, 2, "shirt", 0]].map(([x, t, o, c], i) =>
      swimmer(H, { tone: t, outfit: o, hair: o === "dress" ? 1 : 0, color: c, mood: "grin", arms: [[-150, -170], [150, 170]] }, x, WY - 30, 1.7, `${id}-sw${i}`, true)).join("");
    const skull = swimmer(H, { tone: 1, outfit: "shirt", skeleton: true, look: "left", arms: [[-30, -60], [30, 60]] }, 1180, WY - 10, 1.7, `${id}-sk`, true);
    // the patient bobs up in front and catches hers mid-air
    const PR = K.rig(copy(PAT, { arms: [[-150, -172], [150, 172]] }));
    const pat = swimmer(H, copy(PAT, { mood: "smile", arms: [[-150, -172], [150, 172]] }), 1000, WY + 170, 2.2, `${id}-pat`) +
      `<g transform="translate(${f1(1000 + (PR.hand[0][0] + PR.hand[1][0]) / 2 * 2.2)},${f1(WY + 170 + 78 * 2.2 - 100 * 2.2 + (PR.hand[0][1] + PR.hand[1][1]) / 2 * 2.2 - 84)}) rotate(-8) scale(1.9)">${lifeJacket(C)}</g>`;
    const flying = [[700, 300, -20], [900, 250, 15], [1250, 230, -30], [1500, 270, 22], [1700, 300, -10]].map(([x, y, a]) => `<g transform="translate(${x},${y}) rotate(${a}) scale(1.3)">${lifeJacket(C)}</g>` + whoosh(x - 110, y + 10, 60, 0.3, C, 4)).join("");
    // the conveyor along the waterline, the counter on its side
    const conv = prop(K.props.conveyor({ w: 520, color: C.peri }), 330, 790, 1.4) + Array.from({ length: 5 }, (_, i) => `<g transform="translate(${80 + i * 100},${790 - 66 * 1.4 - 22})">${lifeJacket(C)}</g>`).join("") +
      `<rect x="160" y="800" width="380" height="76" fill="${C.cream}" stroke="${C.line}" stroke-width="5"/>` + bigNum(350, 858, 46, "23.4 MILLION", C.line);
    // the lifeguard flattened into his tall chair under the stamp mark, only his eyes blinking
    const chair = `<path d="M60,800 L120,360 M300,800 L240,360 M80,640 H280 M95,500 H265" stroke="#F4E9CE" stroke-width="18"/><path d="M60,800 L120,360 M300,800 L240,360" stroke="${C.line}" stroke-width="3" fill="none"/>` +
      `<rect x="96" y="330" width="168" height="36" fill="#F4E9CE" stroke="${C.line}" stroke-width="5"/>` +
      `<g transform="translate(180,330) scale(2.1,0.42) translate(0,-100)">${K.person({ tone: 0, outfit: "shirt", color: 2, mood: "flat", arms: [[-90, -90], [90, 90]] })}</g>` +
      prop(K.props.stampMark({ text: "DECENTRALIZED\nFDA PROTOCOL", angle: -6, fontSize: 22 }), 180, 330, 1.3);
    const svg = beach + far + near + skull + flying + pat + conv + chair;
    return { svg, alt: "A plate of Part 12's beach: life jackets fly off a conveyor down the whole line of swimmers, who bob up high in the water in their jackets, a grinning skull among them in one too; in front the patient in her scarf catches hers mid-air; on the left the lifeguard lies flattened into his tall chair under a red DECENTRALIZED FDA PROTOCOL stamp mark, the conveyor's counter on 23.4 MILLION." };
  },

  "one-for-the-mug"(H, id) {
    const { K, C } = H;
    // the reaction cut: one jacket from the beach has flown all the way to the studio and dropped round her mug
    const MX = 870, MY = 792;
    const jacket = `<g transform="translate(${MX + 2},${MY - 34}) scale(1.25,1.05)">${lifeJacket(C)}</g>`;
    const pat = `<path d="M${MX - 50},${MY - 96} q14,-14 28,0 M${MX + 22},${MY - 100} q14,-14 28,0" fill="none" stroke="${C.line}" stroke-width="4" stroke-linecap="round"/>`;
    const svg = H.host("happy-smile", "palms-down", mug(K, MX, MY) + jacket + pat + whoosh(560, 640, 70, 0.25, C, 4));
    return { svg, alt: "Reaction cut: Wishonia at her lectern, pleased, looking at the camera, her hands down by her coffee mug, which now wears an orange life jacket that has just flown in from the beach." };
  },

  "accordion-timeline"(H, id) {
    const { K, C } = H;
    const FL = 880;
    // the ticket window in its booth, the wait sign over it on 36 YEARS
    const booth = `<rect x="180" y="250" width="420" height="${FL - 250}" fill="${C.rust}" stroke="${C.line}" stroke-width="6"/><rect x="250" y="420" width="280" height="200" fill="${C.ink}" stroke="${C.line}" stroke-width="5"/>` +
      `<rect x="250" y="420" width="280" height="40" fill="${C.slate}" stroke="${C.line}" stroke-width="4"/><rect x="230" y="620" width="320" height="22" fill="${C.tan}" stroke="${C.line}" stroke-width="4"/>` +
      prop(K.props.pillBottle({ label: "", pills: false }), 330, 618, 0.9) + prop(K.props.pillBottle({ label: "", pills: false }), 450, 618, 0.9);
    const wheel = (x, ch) => `<rect x="${x}" y="70" width="110" height="140" rx="8" fill="${C.cream}" stroke="${C.line}" stroke-width="5"/>${bigNum(x + 55, 178, 110, ch, C.line)}<path d="M${x},140 h110" stroke="${C.line}" stroke-width="2" opacity="0.5"/>`;
    const sign = `<rect x="120" y="50" width="760" height="180" fill="${C.navy}" stroke="${C.line}" stroke-width="6"/>` + wheel(150, "3") + wheel(275, "6") + oswald(600, 175, 100, "YEARS", C.cream);
    const tag = `<g transform="translate(300,316) rotate(-6)"><rect x="0" y="0" width="180" height="76" fill="${C.yellow}" stroke="${C.line}" stroke-width="5"/>${bigNum(78, 58, 54, "12.3", C.line)}<path d="M142,24 l26,28 M168,24 l-26,28" stroke="${C.line}" stroke-width="8" stroke-linecap="round"/></g>`;
    // the queue squeezed up to the window: posts bunched like an accordion, beards gone, skeletons squeezed in
    const posts = [640, 700, 760, 820, 880, 940].map((x) => `<rect x="${x - 6}" y="${FL - 150}" width="12" height="150" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/><circle cx="${x}" cy="${FL - 156}" r="11" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/>`).join("") +
      `<path d="M640,${FL - 140} q30,30 60,0 q30,30 60,0 q30,30 60,0 q30,30 60,0 q30,30 60,0" fill="none" stroke="${C.war}" stroke-width="8"/>`;
    const people = [[700, PAT, 2.2], [880, { tone: 1, outfit: "suit", color: 0 }, 2.2], [1060, { tone: 3, outfit: "shirt", color: 3 }, 2.2], [1240, { tone: 0, outfit: "dress", hair: 1, color: 2 }, 2.2],
      [1420, { tone: 2, outfit: "overalls", color: 1, skeleton: true }, 2.2], [1580, { tone: 1, outfit: "shirt", color: 2, skeleton: true }, 2.2], [1740, { tone: 0, outfit: "suit", color: 1, skeleton: true }, 2.2]].map(([x, o, s], i) => {
      const oo = copy(o, { look: "left", light: o.skeleton ? undefined : "red", arms: [[10, 6], [70, 100]], mood: i === 0 ? "smile" : "flat" });
      return stand(H, oo, x, FL, s, (o === PAT ? scarf(K, oo) : "") + leashed(H, K.rig(oo).hand[1], -44, 0.3, { seed: 30 + i, color: ["peri", "orange", "cyan", "yellow", "rust", "peri", "orange"][i] }));
    }).join("");
    const svg = room(FL, WALL, C) + booth + sign + posts + people + tag;
    return { svg, alt: "A plate of Part 9's ticket window under the wait sign, its digit wheels clanked to 36 YEARS, a 12.3 times tag on the window; the queue squeezed up to it like an accordion, brass posts bunched, the beards gone, the patient near the front and grinning skeletons squeezed in at the back, each walking his disease on a leash." };
  },

  "two-hundred-twelve-years-sooner"(H, id) {
    const { K, C } = H;
    const FL = 880;
    const sign = arrowSign(980, 430, 760, 170, "", C);
    const mark = `<g transform="translate(1030,432) rotate(-4)"><rect x="-300" y="-62" width="600" height="124" fill="none" stroke="${C.war}" stroke-width="10"/><rect x="-286" y="-48" width="572" height="96" fill="none" stroke="${C.war}" stroke-width="4"/>` +
      oswald(0, 26, 72, "212 YEARS SOONER", C.war) + "</g>";
    const cab = cabinet(1660, FL, 1.5, C, true) + hourglass(1645, FL - 465, 1.3, C, true);
    const bones = stand(H, copy(YOU, { skeleton: true, look: "left", arms: [[20, 30], [-100, -130]] }), 1500, FL + 30, 2.0) ;
    const booth = `<rect x="-20" y="250" width="300" height="${FL - 250}" fill="${C.rust}" stroke="${C.line}" stroke-width="6"/><rect x="30" y="420" width="200" height="200" fill="${C.ink}" stroke="${C.line}" stroke-width="5"/>`;
    const pat = patient(H, 470, FL, 2.4, { look: "right", mood: "smile", arms: [[60, 100], [-60, -100]] },
      `<g transform="translate(2,34) rotate(-8) scale(0.5)">${K.props.pillBottle({ face: "smile", label: "SAFE" })}</g>`);
    const hats = [[620, 300, -20], [760, 240, 18], [1240, 230, -10]].map(([x, y, a]) => `<g transform="translate(${x},${y}) rotate(${a}) scale(2.2)"><rect x="-18" y="-26" width="36" height="24" fill="${C.slate}" stroke="${C.line}" stroke-width="2.5"/><rect x="-28" y="-4" width="56" height="7" fill="${C.slate}" stroke="${C.line}" stroke-width="2.5"/></g>`).join("");
    const crowd = [[680, { tone: 1, outfit: "suit", color: 0 }], [850, { tone: 3, outfit: "shirt", color: 3 }]].map(([x, o]) => stand(H, copy(o, { look: "left", mood: "grin", arms: [[-150, -170], [150, 170]] }), x, FL + 60, 2.2)).join("");
    const svg = room(FL, WALL, C) + booth + cab + bones + sign + mark + crowd + pat + hats;
    return { svg, alt: "A plate pulled back over the squeezed queue: one fat wooden arrow sign stamped 212 YEARS SOONER in red, the approval cabinet standing open behind it with its hourglass burst and YOU's skeleton slumped beside it; at the front of the line the patient hugs her smiling SAFE bottle while the humans behind her throw their hats in the air." };
  },

  "plans-for-tuesday"(H, id) {
    const { K, C } = H;
    const HZ = 430;
    // the crowd to the horizon: dots far, drawn humans near, every one holding up a calendar
    const r = lcg(11);
    let rows = "";
    for (let k = 0; k < 7; k++) {
      const y = HZ + 14 + k * k * 7 + k * 10, s = 0.12 + k * 0.09, step = 34 + k * 30;
      for (let x = -20 + (k % 2) * step / 2; x < 1960; x += step) {
        if (k < 4) rows += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(5 + k * 3)}" fill="${["#F4E3CC", "#D9B48F", "#A87B57", "#6F4B33"][Math.floor(r() * 4)]}" stroke="${C.line}" stroke-width="1.5"/><rect x="${f1(x - 5 - k * 2)}" y="${f1(y - 16 - k * 6)}" width="${10 + k * 4}" height="${8 + k * 3}" fill="#FBF6E6" stroke="${C.line}" stroke-width="1.2"/>`;
        else rows += stand(H, { tone: Math.floor(r() * 4), outfit: ["shirt", "dress", "suit", "overalls"][Math.floor(r() * 4)], hair: r() < 0.4 ? 1 : 0, color: Math.floor(r() * 4), mood: "smile", arms: [[-150, -170], [150, 170]] }, x, y + 30, s * 1.3);
      }
    }
    // the front row and their notes
    const cal = (x, y, note, s = 1.55) => `<g transform="translate(${x},${y}) scale(${s})">${K.props.calendar({ month: "TUE", day: 1 })}` +
      `<g transform="translate(0,-40) rotate(-4)"><rect x="-44" y="-26" width="88" height="44" fill="${C.yellow}" stroke="${C.line}" stroke-width="2"/>` +
      `<text x="0" y="0" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="${note.length > 8 ? 12 : 15}" fill="${C.line}">${note}</text>` +
      `<path d="M-12,8 l6,6 l14,-14" fill="none" stroke="${C.med}" stroke-width="4" stroke-linecap="round"/></g></g>`;
    const front = [
      [440, patient(H, 440, 1040, 2.3, { mood: "smile", arms: [[-150, -170], [150, 170]] }), "KID'S RECITAL"],
      [820, stand(H, K.castOpts("grandma", { arms: [[-150, -170], [150, 170]], hold: null, holdL: null }), 820, 1040, 2.3), "BINGO"],
      [1180, stand(H, { tone: 3, outfit: "overalls", color: 2, mood: "smile", arms: [[-150, -170], [150, 170]] }, 1180, 1040, 2.3), "FISHING"],
      [1540, stand(H, { tone: 0, outfit: "suit", color: 1, mood: "sad", arms: [[-150, -170], [150, 170]] }, 1540, 1040, 2.3), "DENTIST"],
    ].map(([x, p, n]) => p + cal(x, 626, n)).join("");
    const groan = `<path d="M1600,560 q20,-30 40,0 q20,-30 40,0" fill="none" stroke="${C.line}" stroke-width="5"/>`;
    const svg = field(HZ, C) + bigNum(960, 200, 150, "10,700,000,000", C.navy) + rows + front + groan;
    return { svg, alt: "A plate of a field under a cream sky with 10,700,000,000 in the sky; rows of living humans to the horizon each hold up a desk calendar open on TUE; in front the patient, grandma, a barrel man and a box man in a suit hold up theirs with ticked sticky notes, KID'S RECITAL, BINGO, FISHING, DENTIST, the dentist man groaning." };
  },

  "smoke-detector-live"(H, id) {
    const { K, C } = H;
    const CT = 700;
    const kitchen = `<rect width="1920" height="1080" fill="${WALL}"/>` +
      // the window and the back door
      `<rect x="120" y="260" width="360" height="300" fill="${C.cyan}" stroke="${C.line}" stroke-width="8"/><path d="M300,260 V560 M120,410 H480" stroke="${C.line}" stroke-width="6"/>` +
      `<path d="M100,250 H500 L520,290 H80 Z" fill="${C.war}" stroke="${C.line}" stroke-width="5"/>` +
      prop(K.props.door({ color: C.slate }), 1700, 1080, 2.6) +
      // the counter
      `<rect x="0" y="${CT}" width="1500" height="30" fill="${C.orange}" stroke="${C.line}" stroke-width="5"/><rect x="0" y="${CT + 30}" width="1470" height="400" fill="${C.cream}" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M490,${CT + 30} V1080 M980,${CT + 30} V1080" stroke="${C.line}" stroke-width="4"/>`;
    // the live detector on the wall, the old one flattened under it, its mailbox flag drooping
    // the live detector on the wall, slammed down on the old charred one, which peeks out flattened round its edge,
    // its red mailbox flag sticking out and drooping
    const DX = 1000, DY = 150;
    const det = `<ellipse cx="${DX}" cy="${DY + 4}" rx="190" ry="34" fill="#2E2620" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M${DX + 176},${DY + 8} l14,4 l34,52 l-22,10 Z" fill="${C.war}" stroke="${C.line}" stroke-width="4"/>` +
      `<path d="M${DX - 150},${DY + 16} l-20,30 M${DX - 110},${DY + 26} l-6,26" stroke="#2E2620" stroke-width="6" stroke-linecap="round"/>` +
      `<circle cx="${DX}" cy="${DY}" r="118" fill="${C.cream}" stroke="${C.line}" stroke-width="7"/><circle cx="${DX}" cy="${DY}" r="96" fill="none" stroke="${C.line}" stroke-width="2" opacity="0.4"/>` +
      `<rect x="${DX - 70}" y="${DY - 34}" width="140" height="58" rx="6" fill="${C.ink}" stroke="${C.line}" stroke-width="4"/><path d="M${DX - 62},${DY - 4} l14,-12 l14,18 l14,-22 l14,16 l14,-8 l14,12 l14,-14 l14,8" fill="none" stroke="${C.med}" stroke-width="4"/>` +
      `<circle cx="${DX}" cy="${DY + 52}" r="7" fill="${C.med}"/>` + whoosh(DX - 160, DY - 90, 40, 1.2, C, 4) + whoosh(DX + 150, DY - 90, 40, 1.9, C, 4);
    // the patient behind the counter, reading her bottle's lit side panel with the cap still on, a hand at her temple
    const PO = copy(PAT, { look: "right", mood: "worried", arms: [[-130, -200], [80, 100]] }), PSc = 2.6, PXp = 640, PF = CT + 210;
    const ph = K.rig(PO).hand[1], bx = PXp + ph[0] * PSc, by = PF - 100 * PSc + ph[1] * PSc;
    const pat = patient(H, PXp, PF, PSc, { look: "right", mood: "worried", arms: [[-130, -200], [80, 100]] });
    const bottle = prop(K.props.pillBottle({ face: "smile", label: "SAFE" }), bx + 40, by + 80, 1.9);
    const panel = `<g transform="translate(${f1(bx + 110)},${f1(by - 120)})"><rect x="0" y="0" width="380" height="150" rx="8" fill="${C.ink}" stroke="${C.line}" stroke-width="6"/>` +
      oswald(190, 64, 44, "HEADACHES 12%", C.yellow) + oswald(190, 124, 44, "SEVERE 3%", C.yellow) + `<path d="M0,60 L-28,74 L0,90 Z" fill="${C.ink}" stroke="${C.line}" stroke-width="4"/></g>`;
    const counter = `<rect x="0" y="${CT}" width="1500" height="30" fill="${C.orange}" stroke="${C.line}" stroke-width="5"/><rect x="0" y="${CT + 30}" width="1470" height="400" fill="${C.cream}" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M490,${CT + 30} V1080 M980,${CT + 30} V1080" stroke="${C.line}" stroke-width="4"/>`;
    const svg = kitchen.replace(/<rect x="0" y="700"[\s\S]*$/, "") + det + pat + counter + bottle + panel;
    return { svg, alt: "A plate of the patient's 1950s kitchen: on the wall a new smoke detector with a live screen, the old charred one flattened under it with only its red mailbox flag sticking out; at the counter the patient in her scarf reads her smiling SAFE bottle's lit side panel, HEADACHES 12%, SEVERE 3%, with the cap still on." };
  },

  "they-make-you-guess"(H, id) {
    const { K, C } = H;
    const fdaBottle = prop(K.props.pillBottle({ label: "FDA" }), 640, 792, 2.0) +
      `<path d="M582,690 L560,682 L560,714 L582,722 Z" fill="${C.ink}"/><rect x="440" y="650" width="120" height="96" rx="6" fill="${C.ink}" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M458,698 H542" stroke="#3A4766" stroke-width="4" stroke-dasharray="10 10"/>`;
    const coin = `<ellipse cx="960" cy="744" rx="9" ry="46" fill="${C.yellow}" stroke="${C.line}" stroke-width="4"/><path d="M960,700 V788" stroke="#C99A3A" stroke-width="3"/>` +
      `<path d="M926,690 q-12,-16 0,-32 M994,690 q12,-16 0,-32" fill="none" stroke="${C.line}" stroke-width="4"/>`;
    const svg = H.host("sideeye-closed", "idle", fdaBottle + coin + mug(K, 870, 792));
    return { svg, alt: "Host shot: Wishonia at her lectern side-eyeing the camera; on the lectern the FDA's own plain bottle with its blank side panel, and a gold coin standing on its edge." };
  },

  "decision-wheel"(H, id) {
    const { K, C } = H;
    const FL = 900;
    const roomSvg = room(FL, "#CFD9CF", C, C.slate) +
      `<rect x="90" y="150" width="380" height="320" fill="${C.cyan}" stroke="${C.line}" stroke-width="8"/><path d="M280,150 V470 M90,310 H470" stroke="${C.line}" stroke-width="6"/>`;
    // the fat cat leaning in through the window with his DENIED stamp
    const fc = `<defs><clipPath id="${id}-win"><rect x="94" y="154" width="372" height="312"/></clipPath></defs><g clip-path="url(#${id}-win)">` +
      stand(H, K.castOpts("richHuman", { look: "right", mood: "smug", arms: [[22, 72], [100, 120]], hold: null }), 290, 640, 2.7) + "</g>" +
      prop(K.props.stamp({ text: "DENIED" }), 530, 420, 1.2, 24);
    // the patient sits on the exam table: the table top across her lap, her feet dangling
    const table = `<rect x="160" y="700" width="520" height="40" fill="${C.cream}" stroke="${C.line}" stroke-width="5"/><path d="M190,740 V${FL} M650,740 V${FL}" stroke="${C.line}" stroke-width="10"/>` +
      `<path d="M150,700 H690" stroke="${C.line}" stroke-width="5"/>`;
    const chart = `<g transform="translate(540,690) rotate(-6)"><rect x="-44" y="-56" width="88" height="56" fill="#FBF6E6" stroke="${C.line}" stroke-width="4"/>` + prop(K.props.stampMark({ text: "DENIED", fontSize: 18, angle: -10 }), 0, -10, 1) + "</g>";
    const pat = patient(H, 400, 860, 2.3, { look: "right", mood: "worried", outfit: "dress", arms: [[20, 10], [-40, -90]] });
    // the prize wheel stopped on DONUTS
    const WX = 1250, WY = 400, R = 260;
    const names = ["DONUTS (2003)", "HALF-REMEMBERED LECTURE", "WHAT INSURANCE ALLOWS", "VIBES"], fills = [C.yellow, C.cream, C.orange, C.cyan];
    let wheel = "";
    for (let i = 0; i < 4; i++) {
      const a0 = (-135 + i * 90) * Math.PI / 180, a1 = (-45 + i * 90) * Math.PI / 180, am = (a0 + a1) / 2;
      wheel += `<path d="M${WX},${WY} L${f1(WX + R * Math.cos(a0))},${f1(WY + R * Math.sin(a0))} A${R},${R} 0 0,1 ${f1(WX + R * Math.cos(a1))},${f1(WY + R * Math.sin(a1))} Z" fill="${fills[i]}" stroke="${C.line}" stroke-width="5"/>`;
      const tx = WX + R * (i % 2 ? 0.6 : 0.62) * Math.cos(am), ty = WY + R * 0.6 * Math.sin(am);
      const lines = [["DONUTS", "(2003)"], ["HALF-", "REMEMBERED", "LECTURE"], ["WHAT", "INSURANCE", "ALLOWS"], ["VIBES"]][i], size = [44, 26, 30, 44][i];
      wheel += `<g transform="translate(${f1(tx)},${f1(ty)})">` + lines.map((l, k) => oswald(0, (k - (lines.length - 1) / 2) * size * 1.12 + size * 0.36, size, l, C.line)).join("") + "</g>";
    }
    wheel = `<path d="M${WX - 20},${WY + R} L${WX - 70},${FL} M${WX + 20},${WY + R} L${WX + 70},${FL}" stroke="${C.line}" stroke-width="14"/>` +
      `<circle cx="${WX}" cy="${WY}" r="${R + 14}" fill="${C.war}" stroke="${C.line}" stroke-width="6"/>` + wheel +
      `<circle cx="${WX}" cy="${WY}" r="26" fill="${C.yellow}" stroke="${C.line}" stroke-width="5"/><path d="M${WX - 24},${WY - R - 40} H${WX + 24} L${WX},${WY - R + 10} Z" fill="${C.navy}" stroke="${C.line}" stroke-width="4"/>`;
    const donut = (x, y, s) => `<g transform="translate(${x},${y}) scale(${s})"><circle r="22" fill="#C98A4A" stroke="${C.line}" stroke-width="3"/><path d="M-19,-6 Q0,-26 19,-6 Q14,8 0,6 Q-14,8 -19,-6 Z" fill="#E9A3B5"/><circle r="7" fill="#CFD9CF" stroke="${C.line}" stroke-width="3"/></g>`;
    const doc = doctor(H, 820, FL, 2.4, { look: "left", mood: "smile", arms: [[10, 6], [-70, -100]] }) + donut(660, 600, 1.3) +
      `<path d="M720,560 l40,-20 l12,16 l-40,20 Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/>` + `<rect x="840" y="640" width="90" height="54" fill="#FBF6E6" stroke="${C.line}" stroke-width="4" transform="rotate(-8 885 667)"/>` + donut(870, 650, 0.8) + donut(900, 655, 0.8);
    const lob = stand(H, K.castOpts("lobbyist", { look: "right" }), 1760, FL, 2.3);
    const svg = roomSvg + fc + pat + table + chart + wheel + doc + lob;
    return { svg, alt: "A plate of a doctor's exam room: a carnival prize wheel with four slices, DONUTS (2003), HALF-REMEMBERED LECTURE, WHAT INSURANCE ALLOWS and VIBES, stopped on DONUTS; the doctor with his head mirror hands the patient on the exam table a donut; the fat cat leans in at the window with his DENIED stamp, and the lobbyist tiptoes off at the right." };
  },

  "grape-soda"(H, id) {
    const { K, C } = H;
    const can = `<g transform="translate(700,792)"><rect x="-70" y="-250" width="140" height="250" rx="12" fill="#6E4A8C" stroke="${C.line}" stroke-width="6"/>` +
      `<rect x="-70" y="-250" width="140" height="22" fill="#C9CFD3" stroke="${C.line}" stroke-width="5"/><rect x="-64" y="-176" width="128" height="110" fill="#FBF6E6" stroke="${C.line}" stroke-width="4"/>` +
      oswald(0, -196, 24, "GRAPE SODA", C.cream) + bigNum(0, -110, 40, "0%", C.war) + oswald(0, -76, 26, "GRAPE", C.line) + "</g>";
    const sticker = `<g transform="translate(910,600) rotate(24)"><circle r="17" fill="#8E5BB0" stroke="${C.line}" stroke-width="3"/><path d="M0,-17 l4,-10" stroke="${C.money}" stroke-width="4"/><path d="M-8,-6 q4,-4 8,0" stroke="#FFFFFF" stroke-width="3" fill="none"/></g>` +
      `<path d="M900,560 q-30,30 0,60 q30,30 0,60" fill="none" stroke="${C.line}" stroke-width="3" stroke-dasharray="8 10"/>`;
    const svg = H.host("smirk-closed", "hands-hips", can + mug(K, 880, 792) + sticker);
    return { svg, alt: "Host shot: Wishonia at her lectern, hands on hips, smirking; on the lectern a plain can of GRAPE SODA whose label, under the spot where the grape sticker was, reads 0% GRAPE, while the little grape sticker flutters down into her coffee mug." };
  },

  "ranked-treatments"(H, id) {
    const { K, C } = H;
    const FL = 900;
    const roomSvg = room(FL, "#CFD9CF", C, C.slate) + `<rect x="90" y="150" width="380" height="320" fill="${C.cyan}" stroke="${C.line}" stroke-width="8"/><path d="M280,150 V470 M90,310 H470" stroke="${C.line}" stroke-width="6"/>`;
    const table = `<rect x="160" y="700" width="520" height="40" fill="${C.cream}" stroke="${C.line}" stroke-width="5"/><path d="M190,740 V${FL} M650,740 V${FL}" stroke="${C.line}" stroke-width="10"/>`;
    // the flip board standing on the flattened wheel (its four colors squashed out from under it)
    const BX = 840, BY = 90, BW = 900, BH = 760, cx0 = BX + BW / 2;
    let board = [[C.cyan, -1], [C.yellow, -0.5], [C.cream, 0.5], [C.orange, 1]].map(([col, k]) => `<path d="M${cx0 + k * 160 - 160},${FL - 4} L${cx0 + k * 300},${FL - 22} L${cx0 + k * 300 + 160},${FL - 4} Z" fill="${col}" stroke="${C.line}" stroke-width="4"/>`).join("") +
      `<rect x="${BX}" y="${BY}" width="${BW}" height="${BH}" fill="${C.ink}" stroke="${C.line}" stroke-width="8"/>`;
    [0, 1, 2].forEach((k) => {
      const y = BY + 40 + k * 240;
      board += `<rect x="${BX + 30}" y="${y}" width="${BW - 60}" height="200" fill="#1E2A44" stroke="#3A4766" stroke-width="4"/><path d="M${BX + 30},${y + 100} H${BX + BW - 30}" stroke="#0B1A33" stroke-width="3"/>` +
        `<rect x="${BX + 50}" y="${y + 30}" width="90" height="140" fill="${C.slate}" stroke="#3A4766" stroke-width="3"/>` + bigNum(BX + 95, y + 135, 100, String(k + 1), C.cream) +
        prop(K.props.pillBottle({ face: k === 0 ? "smile" : k === 1 ? "flat" : "sad", label: k === 0 ? "SAFE" : "" }), BX + 220, y + 185, 1.45);
      for (let j = 0; j < 7; j++) {
        const dead = k === 2 ? j < 5 : k === 1 ? j < 2 : false;
        board += stand(H, { plain: true, tone: (j + k) % 4, outfit: j % 2 ? "dress" : "shirt", hair: j % 2, color: (j + k) % 4, skeleton: dead, mood: k === 0 ? "grin" : "flat", arms: k === 0 ? [[-150, -170], [150, 170]] : [[10, 4], [-10, -4]] }, BX + 340 + j * 74, y + 190, 0.85);
      }
    });
    const slice = `<path d="M560,${FL + 20} L700,${FL - 20} L720,${FL + 40} Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="4"/>` + whoosh(470, FL + 10, 60, 0, C, 4);
    const PO = copy(PAT, { look: "right", mood: "eager", arms: [[20, 10], [110, 140]] }), ph = K.rig(PO).hand[1];
    const pat = patient(H, 400, 860, 2.3, { look: "right", mood: "eager", arms: [[20, 10], [110, 140]] },
      `<g transform="translate(${f1(ph[0] + 4)},${f1(ph[1] + 24)}) rotate(8) scale(0.42)">${K.props.pillBottle({ face: "smile", label: "SAFE" })}</g>`);
    const donutFall = `<g transform="translate(330,820)"><circle r="30" fill="#C98A4A" stroke="${C.line}" stroke-width="4"/><path d="M-26,-8 Q0,-34 26,-8 Q18,8 0,6 Q-18,8 -26,-8 Z" fill="#E9A3B5"/><circle r="10" fill="#CFD9CF" stroke="${C.line}" stroke-width="4"/></g><path d="M330,760 v-40 M310,770 v-30 M350,770 v-30" stroke="${C.line}" stroke-width="4" opacity="0.6"/>`;
    const svg = roomSvg + board + slice + pat + table + donutFall;
    return { svg, alt: "A plate of the exam room: a tall dark flip board stands on the flattened prize wheel, three rows numbered 1, 2, 3, each a pill bottle and a row of tiny humans who took it, row 1 cheering and row 3 mostly grinning skeletons; the patient on the exam table drops her donut and holds her smiling SAFE bottle up toward row 1, whose bottle matches it." };
  },

  "forty-page-insert"(H, id) {
    const { K, C } = H;
    const FL = 880;
    const walls = room(FL, WALL2, C) + `<rect x="0" y="0" width="700" height="${FL - 16}" fill="#D3BE91"/>` +
      // the doorway from the living room into the hall
      `<rect x="640" y="140" width="80" height="${FL - 156}" fill="${C.tan}" stroke="${C.line}" stroke-width="5"/>`;
    // the living room beyond: the couch and the patient buried in the insert heap
    const couch = `<rect x="40" y="560" width="520" height="160" rx="16" fill="${C.peri}" stroke="${C.line}" stroke-width="6"/><rect x="20" y="660" width="560" height="140" rx="14" fill="${C.peri}" stroke="${C.line}" stroke-width="6"/><path d="M60,800 V${FL} M540,800 V${FL}" stroke="${C.line}" stroke-width="10"/>`;
    const heapCol = "#FBF6E6";
    const heap = `<path d="M60,${FL} Q40,640 200,600 Q260,520 330,600 Q470,560 560,700 Q620,800 640,${FL} Z" fill="${heapCol}" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M120,760 L260,700 M320,660 L480,720 M180,820 L420,780" stroke="${C.line}" stroke-width="3" opacity="0.5"/>`;
    const pat = patient(H, 300, 860, 2.2, { look: "right", mood: "worried" });
    const patClip = `<defs><clipPath id="${id}-pc"><rect x="0" y="0" width="700" height="620"/></clipPath></defs><g clip-path="url(#${id}-pc)">${pat}</g>` + heap.replace(/Q260,520 330,600/, "Q262,640 330,640") +
      `<g transform="translate(300,720) rotate(-6)">${oswald(0, 0, 30, "PAGE 1 OF 40", C.line)}</g>`;
    // the insert across the floor, through the doorway into the hall, up the telephone table to the lawyer's pen
    const TX0 = 1040, TX1 = 1300, TT = 600;
    const ink = (x0, x1, y) => Array.from({ length: Math.floor((x1 - x0) / 50) }, (_, i) => `<path d="M${x0 + 14 + i * 50},${y - 12} l30,0 M${x0 + 14 + i * 50},${y + 2} l24,0 M${x0 + 14 + i * 50},${y + 16} l30,0" stroke="${C.line}" stroke-width="2" opacity="0.6"/>`).join("");
    const strip = `<path d="M560,${FL - 30} L${TX0 + 6},${FL - 34} L${TX0 + 46},${FL + 34} L520,${FL + 40} Z" fill="${heapCol}" stroke="${C.line}" stroke-width="5"/>` + ink(560, TX0, FL) +
      `<path d="M820,${FL - 32} L850,${FL + 38} M1000,${FL - 34} L1030,${FL + 36}" stroke="${C.line}" stroke-width="2" opacity="0.5"/>`;
    const climb = `<path d="M${TX0 - 4},${FL - 34} L${TX0 + 46},${FL - 30} L${TX0 + 46},${TT + 4} L${TX0 - 4},${TT} Z" fill="${heapCol}" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M${TX0 - 6},${TT} L${TX0 + 180},${TT - 6} L${TX0 + 186},${TT + 14} L${TX0 - 6},${TT + 22} Z" fill="${heapCol}" stroke="${C.line}" stroke-width="4"/>` +
      `<path d="M${TX0 + 130},${TT - 8} l10,-8 l6,10 l10,-12 l6,12 l10,-10" fill="none" stroke="${C.line}" stroke-width="3"/>`;
    const hallTable = `<rect x="${TX0}" y="${TT}" width="${TX1 - TX0}" height="22" fill="${C.rust}" stroke="${C.line}" stroke-width="5"/><path d="M${TX0 + 20},${TT + 22} V${FL - 30} M${TX1 - 20},${TT + 22} V${FL - 30}" stroke="${C.line}" stroke-width="9"/>` +
      prop(K.props.phone(), TX1 - 50, TT, 1.4);
    // the lawyer behind the table, his pen hand jittering so hard the desk rattles
    const LO = copy(LAW, { look: "left", mood: "cross", holdR: null, arms: [[60, 90], [30, 70]] });
    const law = stand(H, LO, 1250, FL - 30, 2.3) + `<path d="M${TX0 + 110},${TT - 40} l-10,-14 M${TX0 + 150},${TT - 44} l6,-16 M${TX0 + 190},${TT - 36} l14,-10" stroke="${C.line}" stroke-width="4" stroke-linecap="round"/>` +
      `<path d="M${TX0 - 20},${TT + 10} l-12,-4 M${TX1 + 20},${TT + 10} l12,-4 M${TX0 - 22},${TT + 26} l-12,2 M${TX1 + 22},${TT + 26} l12,2" stroke="${C.line}" stroke-width="4" stroke-linecap="round"/>`;
    // the front door, shut; the doctor in the doorway wiping his shoes on the insert like a doormat
    const door = prop(K.props.door({ color: C.rust }), 1700, FL - 30, 2.4);
    const doc = doctor(H, 760, FL - 24, 2.3, { look: "left", mood: "flat", arms: [[10, 4], [-14, -40]] }) +
      `<rect x="830" y="700" width="70" height="56" rx="8" fill="#5A3A26" stroke="${C.line}" stroke-width="4"/>` + whoosh(680, FL - 26, -50, 0, C, 4) + whoosh(840, FL - 26, 50, 0, C, 4);
    const svg = walls.replace(/<rect x="640" y="140"[^>]*>/, `<rect x="700" y="120" width="34" height="${FL - 136}" fill="${C.tan}" stroke="${C.line}" stroke-width="5"/>`) +
      couch + patClip + strip + door + law + hallTable + climb + doc;
    return { svg, alt: "A plate of the patient's living room and front hall: the patient buried to the chin in an unfolded insert on the couch, PAGE 1 OF 40 on top; the insert runs across the floor, through the doorway, where the doctor wipes his shoes on it like a doormat, and up onto the hall telephone table, where the lawyer is still writing its end, his pen hand jittering." };
  },

  "meadow-ad"(H, id) {
    const { K, C } = H;
    // pushed into the TV: the cabinet's bezel round the edges, the rabbit ears poking in at the top
    const screen = `<rect width="1920" height="1080" fill="${C.rust}"/><rect x="90" y="70" width="1740" height="880" rx="60" fill="${C.ink}"/>`;
    const clip = `<defs><clipPath id="${id}-scr"><rect x="110" y="90" width="1700" height="840" rx="52"/></clipPath></defs>`;
    let meadow = `<rect x="110" y="90" width="1700" height="840" fill="#BFD3D6"/><path d="M110,560 Q500,500 900,560 T1810,540 V930 H110 Z" fill="#8FAE6A" stroke="${C.line}" stroke-width="4"/>`;
    const r = lcg(3);
    for (let i = 0; i < 40; i++) { const x = 130 + r() * 1660, y = 600 + r() * 220; meadow += `<circle cx="${f1(x)}" cy="${f1(y)}" r="7" fill="#FBF6E6" stroke="${C.line}" stroke-width="1.5"/><circle cx="${f1(x)}" cy="${f1(y)}" r="2.5" fill="${C.yellow}"/>`; }
    // the meadow woman mid-skip as a grinning skeleton in her sun hat, daisies still in hand
    const sk = copy({ tone: 0, outfit: "dress", hair: 1, color: 3 }, { skeleton: true, look: "right", arms: [[-30, -60], [130, 160]] });
    const R = H.K.rig(sk);
    const hat = `<g transform="translate(${f1(R.top[0] + 2)},${f1(R.top[1] + 8)}) rotate(-8)"><ellipse cx="0" cy="0" rx="34" ry="8" fill="${C.yellow}" stroke="${C.line}" stroke-width="2.4"/><path d="M-14,-1 Q-12,-16 0,-17 Q12,-16 14,-1 Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="2.4"/><path d="M-14,-4 H14" stroke="${C.war}" stroke-width="3"/></g>`;
    const daisies = `<g transform="translate(${f1(R.hand[1][0])},${f1(R.hand[1][1] - 6)})"><path d="M0,0 l-4,-20 M0,0 l6,-18 M0,0 l0,-24" stroke="#5E7F3A" stroke-width="2"/>${[[-4, -22], [6, -20], [0, -26]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="5" fill="#FBF6E6" stroke="${C.line}" stroke-width="1.2"/><circle cx="${x}" cy="${y}" r="1.8" fill="${C.yellow}"/>`).join("")}</g>`;
    const spots = [[-6, -10], [8, 4], [-10, 16], [6, -26]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3.5" fill="${C.war}"/>`).join("");
    const SS = 2.5, SF = 600;
    const skel = `<g transform="translate(960,${SF - 100 * SS}) rotate(-8) scale(${SS})">${H.K.person(sk)}${hat}${daisies}${spots}</g>`;
    const motion = `<path d="M520,700 q90,-170 180,0 M700,700 q90,-170 180,0" fill="none" stroke="${C.line}" stroke-width="5" stroke-dasharray="14 14" opacity="0.7"/>` +
      `<ellipse cx="960" cy="690" rx="90" ry="14" fill="#6E8B4C" opacity="0.7"/>`;
    const crawl = `<rect x="110" y="820" width="1700" height="70" fill="${C.ink}" opacity="0.85"/>` +
      `<text x="960" y="868" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="38" letter-spacing="2" fill="${C.cream}">STROKE · CONSTIPATION · DEATH · MILD RASH · DRY SKIN</text>`;
    const glare = `<path d="M180,140 Q400,110 600,150" fill="none" stroke="#FFFFFF" stroke-width="14" opacity="0.25" stroke-linecap="round"/>`;
    const ears = `<path d="M820,70 L700,-20 M1100,70 L1240,-20" stroke="${C.line}" stroke-width="10"/>`;
    const svg = screen + clip + `<g clip-path="url(#${id}-scr)">${meadow}${motion}${skel}${crawl}${glare}</g>` + ears;
    return { svg, alt: "Pushed into the TV screen: a meadow of daisies where the smiling woman of the drug ad is now a grinning skeleton mid-skip in her sun hat, daisies in hand, a few red rash spots on the bones, while a crawl of small text along the bottom of the screen reads STROKE, CONSTIPATION, DEATH, MILD RASH, DRY SKIN, all the same size." };
  },

  "ask-your-doctor"(H, id) {
    const { K, C } = H;
    const FL = 880;
    const walls = room(FL, WALL2, C) + `<rect x="0" y="0" width="620" height="${FL - 16}" fill="#D3BE91"/><rect x="560" y="140" width="80" height="${FL - 156}" fill="${C.tan}" stroke="${C.line}" stroke-width="5"/>`;
    // through the doorway: the patient's head sticking out of the insert heap on the couch, looking
    const couch = `<rect x="40" y="580" width="460" height="150" rx="16" fill="${C.peri}" stroke="${C.line}" stroke-width="6"/>`;
    const pat = `<defs><clipPath id="${id}-pc"><rect x="0" y="0" width="560" height="640"/></clipPath></defs><g clip-path="url(#${id}-pc)">${patient(H, 280, 870, 2.2, { look: "right", mood: "worried" })}</g>` +
      `<path d="M30,${FL} Q20,660 180,630 Q280,600 380,640 Q500,620 540,${FL} Z" fill="#FBF6E6" stroke="${C.line}" stroke-width="5"/>`;
    // the hall table: the rotary phone with its little screen (a grinning skull) and the egg timer on 7 MIN
    const hallTable = `<rect x="840" y="580" width="320" height="24" fill="${C.rust}" stroke="${C.line}" stroke-width="5"/><path d="M860,604 V${FL} M1140,604 V${FL}" stroke="${C.line}" stroke-width="9"/>`;
    const phone = prop(K.props.phone(), 920, 580, 2.0) +
      `<rect x="880" y="380" width="170" height="130" rx="10" fill="${C.ink}" stroke="${C.line}" stroke-width="5"/><path d="M930,512 L910,560 M1000,512 L1020,560" stroke="${C.line}" stroke-width="5"/>` +
      `<rect x="892" y="392" width="146" height="26" fill="#FBF6E6" stroke="${C.line}" stroke-width="2"/><text x="965" y="411" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="17" fill="${C.line}">RED CHEST LIGHT</text>` +
      `<g transform="translate(965,468) scale(1.6)"><path d="M-14,-12 Q-14,-26 0,-26 Q14,-26 14,-12 Q14,-2 8,2 V8 H-8 V2 Q-14,-2 -14,-12 Z" fill="#F1EAD6" stroke="${C.line}" stroke-width="2"/><circle cx="-6" cy="-12" r="4" fill="${C.line}"/><circle cx="6" cy="-12" r="4" fill="${C.line}"/><path d="M-6,4 V8 M0,4 V8 M6,4 V8" stroke="${C.line}" stroke-width="1.4"/></g>`;
    const timer = `<g transform="translate(1100,580)"><path d="M-40,0 L-34,-50 H34 L40,0 Z" fill="#FBF6E6" stroke="${C.line}" stroke-width="4"/><circle cx="0" cy="-76" r="40" fill="#FBF6E6" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M0,-90 L18,-108" stroke="${C.war}" stroke-width="5" stroke-linecap="round"/><circle cx="0" cy="-90" r="4" fill="${C.line}"/>` + oswald(0, -54, 24, "7 MIN", C.line) + "</g>";
    // the doctor, pale, rolling backwards out of the open front door on roller skates
    const door = prop(K.props.door({ color: C.rust, open: 1 }), 1680, FL, 2.4);
    const dOpts = { look: "left", mood: "worried", arms: [[-30, -60], [40, 70]] };
    const R = K.rig(copy(DOC, dOpts));
    const skates = [0, 1].map((i) => `<g transform="translate(${f1(R.hip[i][0] + (i ? 4 : -4))},100)"><rect x="-16" y="-6" width="34" height="12" rx="3" fill="${C.war}" stroke="${C.line}" stroke-width="2"/><circle cx="-8" cy="10" r="5" fill="${C.cream}" stroke="${C.line}" stroke-width="2"/><circle cx="10" cy="10" r="5" fill="${C.cream}" stroke="${C.line}" stroke-width="2"/></g>`).join("");
    const sweat = [[-10, -78], [-18, -66]].map(([x, y]) => `<path d="M${x},${y} q-3,6 0,9 q3,-3 0,-9 Z" fill="#BFD9E8" stroke="${C.line}" stroke-width="1.2"/>`).join("");
    const doc = `<g transform="translate(1440,${FL - 115}) rotate(10)">${stand(H, copy(DOC, dOpts), 0, 0, 2.3, docKit(K, copy(DOC, dOpts)) + skates + sweat)}</g>` + whoosh(1270, FL - 220, -70, 0, C, 5);
    const svg = walls + couch + pat + hallTable + phone + timer + door + doc;
    return { svg, alt: "A plate of the front hall: on the telephone table the rotary phone's little screen shows RED CHEST LIGHT in a search box and a grinning skull, an egg timer on 7 MIN beside it; the doctor, pale, rolls backwards on roller skates toward the open front door, while through the doorway the patient's head sticks out of the insert heap on the couch." };
  },

  "outcome-label"(H, id) {
    const { K, C } = H;
    const FL = 900;
    const walls = room(FL, "#D3BE91", C) +
      `<rect x="520" y="140" width="420" height="300" fill="${C.cyan}" stroke="${C.line}" stroke-width="8"/><path d="M730,140 V440" stroke="${C.line}" stroke-width="6"/>`;
    // the loud human leaning in at the window, his megaphone gagged by his own sticker
    const LHo = K.castOpts("loudHuman", { look: "right", arms: [[20, 10], [120, 140]] }), LS = 2.3, LX = 680, LF = 690, lh = K.rig(LHo).head;
    const gx = LX + (lh[0] + 30) * LS, gy = LF - 100 * LS + lh[1] * LS;
    const loud = `<defs><clipPath id="${id}-win"><rect x="524" y="144" width="412" height="292"/></clipPath></defs><g clip-path="url(#${id}-win)">` +
      stand(H, LHo, LX, LF, LS) + `<g transform="translate(${f1(gx)},${f1(gy)}) rotate(-80)"><rect x="-62" y="-24" width="124" height="48" fill="${C.yellow}" stroke="${C.line}" stroke-width="4"/>${oswald(0, 11, 28, "MIRACLE!", C.war)}</g></g>` +
      `<path d="M${f1(gx + 60)},${f1(gy - 40)} l24,-14 M${f1(gx + 64)},${f1(gy)} l28,0" stroke="${C.line}" stroke-width="4" stroke-linecap="round"/>`;
    const couchBack = `<rect x="380" y="520" width="700" height="200" rx="18" fill="${C.peri}" stroke="${C.line}" stroke-width="6"/>`;
    const couchSeat = `<rect x="350" y="646" width="760" height="184" rx="16" fill="${C.peri}" stroke="${C.line}" stroke-width="6"/><path d="M380,830 V${FL} M1080,830 V${FL}" stroke="${C.line}" stroke-width="10"/>`;
    const pat = patient(H, 600, 820, 2.5, { light: "teal", mood: "smile", look: "right", arms: [[-30, -10], [30, 10]] });
    // the coffee table with the SAFE bottle and its outcome label
    const table = `<rect x="880" y="740" width="560" height="26" fill="${C.rust}" stroke="${C.line}" stroke-width="5"/><path d="M910,766 V${FL + 40} M1410,766 V${FL + 40}" stroke="${C.line}" stroke-width="9"/>`;
    const bottle = prop(K.props.pillBottle({ face: "smile", label: "SAFE", pills: false }), 980, 742, 1.6);
    let label = `<g transform="translate(1080,420)"><rect x="0" y="0" width="330" height="318" fill="#FBF6E6" stroke="${C.line}" stroke-width="6"/>` +
      oswald(165, 46, 36, "OUTCOME LABEL", C.line) + `<path d="M16,62 H314" stroke="${C.line}" stroke-width="8"/>`;
    [["GOT BETTER", 6], ["NO CHANGE", 3], ["SIDE EFFECTS", 1]].forEach(([n, k], i) => {
      const y = 76 + i * 78;
      label += oswald(18, y + 30, 22, n, C.line, "start") + `<path d="M16,${y + 74} H314" stroke="${C.line}" stroke-width="2"/>`;
      for (let j = 0; j < k; j++) label += `<g transform="translate(${178 + j * 22},${y + 24}) scale(0.26)">${K.person({ plain: true, tone: j % 4, outfit: "shirt", color: (j + i) % 4, mood: i === 2 ? "worried" : "smile" })}</g>`;
    });
    label += `</g><path d="M1080,700 L1020,700" stroke="${C.line}" stroke-width="4"/>`;
    // the lawyer buried under his insert, only his briefcase sticking out
    const heap = `<path d="M1460,${FL + 20} Q1440,700 1580,660 Q1680,600 1760,680 Q1900,700 1900,${FL + 20} Z" fill="#FBF6E6" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M1500,800 L1640,740 M1680,700 L1840,760" stroke="${C.line}" stroke-width="3" opacity="0.5"/>` +
      `<g transform="translate(1690,630) rotate(-24)"><rect x="-50" y="-34" width="100" height="70" rx="6" fill="#5A3A26" stroke="${C.line}" stroke-width="5"/><path d="M-18,-34 v-12 h36 v12" fill="none" stroke="${C.line}" stroke-width="5"/></g>`;
    const glow = `<circle cx="${f1(600 + 8 * 2.5)}" cy="${f1(820 - 100 * 2.5 - 13 * 2.5)}" r="30" fill="${C.med}" opacity="0.35"/>`;
    const svg = walls + loud + couchBack + glow + pat + couchSeat + table + bottle + label + heap;
    return { svg, alt: "A plate of the living room: the patient on the couch smiling, her chest light just turned teal; on the coffee table her smiling SAFE bottle with a clean OUTCOME LABEL beside it, bars of tiny humans for GOT BETTER, NO CHANGE and SIDE EFFECTS; at the window the loud human with his megaphone gagged by his own MIRACLE! sticker; on the right the lawyer buried under his insert, only his briefcase sticking out." };
  },

  "louder-wins"(H, id) {
    const { K, C } = H;
    const screen = `<rect width="1920" height="1080" fill="${C.rust}"/><rect x="90" y="70" width="1740" height="880" rx="60" fill="${C.ink}"/>`;
    const clip = `<defs><clipPath id="${id}-scr"><rect x="110" y="90" width="1700" height="840" rx="52"/></clipPath></defs>`;
    const studio = `<rect x="110" y="90" width="1700" height="840" fill="#4A5878"/><rect x="110" y="620" width="1700" height="320" fill="${C.slate}"/>` +
      `<circle cx="960" cy="420" r="300" fill="#56658A"/>`;
    const desk = `<rect x="260" y="640" width="1400" height="40" fill="${C.tan}" stroke="${C.line}" stroke-width="5"/><rect x="300" y="680" width="1320" height="200" fill="${C.rust}" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M820,640 l40,-20 l60,10 l40,-24 l50,20 l30,14 Z" fill="#FBF6E6" stroke="${C.line}" stroke-width="3" opacity="0.9"/>`;
    // the burst loudness meter between them
    const meter = `<g transform="translate(960,640)"><rect x="-70" y="-120" width="140" height="120" fill="#3A3028" stroke="${C.line}" stroke-width="5"/><circle cx="0" cy="-72" r="44" fill="#55473A" stroke="${C.line}" stroke-width="4"/>` +
      `<path d="M-10,-130 l-30,-60 M10,-130 l40,-70 M0,-120 l6,-90" stroke="${C.line}" stroke-width="5"/><path d="M0,-72 L60,-150" stroke="${C.war}" stroke-width="6"/></g>` +
      `<path d="M900,440 q-30,-40 0,-80 q30,-40 0,-80 M1020,440 q30,-40 0,-80 q-30,-40 0,-80" fill="none" stroke="#8C8782" stroke-width="10" stroke-linecap="round" opacity="0.8"/>`;
    // both panelists charred and smoking, hair straight up, still shouting into megaphones; the trophy in one's hands
    const megaphone = (flip) => `<g transform="scale(${flip ? -1 : 1},1)"><path d="M0,-8 L46,-26 L46,22 L0,6 Z" fill="${C.cream}" stroke="${C.line}" stroke-width="3"/><rect x="-10" y="-8" width="12" height="16" fill="${C.cream}" stroke="${C.line}" stroke-width="3"/></g>`;
    const polL = copy(K.castOpts("politician", { charred: true, look: "right", arms: [[10, 4], [90, 100]] }), {});
    const polR = copy(K.castOpts("politician", { charred: true, look: "left", arms: [[-90, -100], [-20, -60]] }), {});
    const RL = K.rig(polL), RR = K.rig(polR);
    const left = stand(H, polL, 560, 900, 2.9, `<g transform="translate(${f1(RL.mouth[0] + 6)},${f1(RL.mouth[1])})">${megaphone(false)}</g>`);
    const tie = `<path d="M${f1(RR.neck[0] - 3)},${f1(RR.neck[1] + 10)} l3,24 l3,-24 Z" fill="${C.peri}" opacity="0.9"/>`;
    const right = stand(H, polR, 1360, 900, 2.9, `<g transform="translate(${f1(RR.mouth[0] - 6)},${f1(RR.mouth[1])})">${megaphone(true)}</g>` + tie);
    // the trophy, in his hands on the desk: a gold cup on a plinth with its plaque
    const plaque = `<g transform="translate(1530,642) scale(0.85)"><path d="M-60,-190 H60 L44,-110 Q0,-86 -44,-110 Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M-60,-176 q-36,6 -22,44 q8,14 30,16 M60,-176 q36,6 22,44 q-8,14 -30,16" fill="none" stroke="${C.line}" stroke-width="5"/>` +
      `<rect x="-14" y="-100" width="28" height="40" fill="${C.yellow}" stroke="${C.line}" stroke-width="4"/><rect x="-112" y="-62" width="224" height="62" fill="${C.tan}" stroke="${C.line}" stroke-width="5"/>` +
      `<rect x="-100" y="-52" width="200" height="42" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/>${oswald(0, -22, 24, "WINNER (LOUDEST)", C.line)}</g>`;
    const shout = `<path d="M760,560 l40,-20 M770,600 l46,0 M760,640 l40,20 M1160,560 l-40,-20 M1150,600 l-46,0 M1160,640 l-40,20" stroke="${C.cream}" stroke-width="6" stroke-linecap="round"/>`;
    const svg = screen + clip + `<g clip-path="url(#${id}-scr)">${studio}${meter}${left}${right}${desk}${shout}${plaque}</g>` + `<path d="M820,70 L700,-20 M1100,70 L1240,-20" stroke="${C.line}" stroke-width="10"/>`;
    return { svg, alt: "Pushed into the TV screen: a panel show where two politicians stand charred black and smoking, hair straight up, still shouting into megaphones across a long desk, the burst loudness meter smoking between them; the one on the right holds a gold trophy labeled WINNER (LOUDEST), his charred tie flickering blue." };
  },

  "optimitron-appliance"(H, id) {
    const { K, C } = H;
    const opt = prop(K.props.optimitron({ mood: "smile", health: 100, wealth: 100, card: "OPTIMAL BUDGET", pop: 62 }), 640, 792, 1.25);
    const card2 = `<g transform="translate(1140,460) rotate(-18)"><rect x="-90" y="-60" width="180" height="120" fill="#FBF6E6" stroke="${C.line}" stroke-width="5"/>${oswald(0, -10, 30, "OPTIMAL", C.line)}${oswald(0, 30, 30, "POLICY", C.line)}</g>` + whoosh(1030, 560, -70, -0.35, C, 5);
    const pol = copy(K.castOpts("politician", { charred: true, look: "left", arms: [[-20, -10], [-120, -150]] }), {});
    const RP = K.rig(pol);
    const meg = `<g transform="translate(${f1(RP.mouth[0] - 6)},${f1(RP.mouth[1])}) scale(-1,1)"><path d="M0,-8 L46,-26 L46,22 L0,6 Z" fill="${C.cream}" stroke="${C.line}" stroke-width="3"/></g>`;
    const winner = stand(H, pol, 1560, 1150, 3.1, meg);
    const trophy = `<g transform="translate(1290,380) rotate(-40) scale(2.4)"><path d="M-14,-30 H14 L10,-6 Q0,2 -10,-6 Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="2"/><rect x="-4" y="-4" width="8" height="10" fill="${C.yellow}" stroke="${C.line}" stroke-width="2"/><rect x="-12" y="6" width="24" height="8" fill="${C.tan}" stroke="${C.line}" stroke-width="2"/></g>` +
      `<path d="M1250,330 l-20,-30 M1300,320 l10,-34 M1330,350 l30,-20" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/>`;
    const svg = H.host("smirk-smile", "hands-hips", opt + mug(K, 900, 792) + winner + trophy + card2);
    return { svg, alt: "Host shot: Wishonia at her lectern, hands on hips, smirking; the Optimitron sits on the lectern like a toaster, both dials turned up and the OPTIMAL BUDGET card standing in its slot, while the OPTIMAL POLICY card flies across the set and knocks the trophy out of the hands of the charred politician standing at her right, still holding his megaphone." };
  },
};
