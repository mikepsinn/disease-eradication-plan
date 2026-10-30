// Sketches for storyboards/part-25-choose-your-own-adventure.md (v3, the 1950s atomic-age film look): each scene's
// key moment on a 1920 x 1080 frame, drawn with the production art (H.K: kit.js, film.js and the props library).
// Host shots use the studio set (H.host); a plate frame is what the camera sees at that moment, one framing, with the
// ground and the cast drawn large. Built into the review sheet by tools/storyboard-sheet.mjs.
//
// The-roads (future-a-2027 to future-b-2048) is one plate. Its constants and drawings below (ROADS, SKY, the road,
// fingerpost(), milestone(), YOU) are the reference the scene files copy, so every stretch is the same road.

import { caseFile, mug as mugSvg } from "./part-26-humanity-has-no-choice.sketch.mjs";
import { leashed } from "./part-09-unexplored-therapeutic-frontier.sketch.mjs";

const f = (n) => (+n).toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});

// ── The-roads: plate units are canvas px at camera scale 1 (16:9) ──
// The fork's fingerpost stands at x 0. Road A runs left (x < 0), road B right (x > 0). The road is a cream band from
// y FAR to y NEAR; people stand with their feet at y FEET at scale 1.5; the horizon is at y HZ. Past the cliff edge
// (x CLIFF) road A goes on along the valley floor, DROP lower. Station x positions are where each scene's stops stand.
const ROADS = {
  HZ: -300, FAR: -10, NEAR: 90, FEET: 50, K: 1.5, CLIFF: -11900, DROP: 1700,
  A: { m2027: -600, bar604: -1300, m2033: -2400, gauge: -3100, robot: -3560, m2035: -4300, engineer: -4750, bridge: -5250, hospital: -6400,
    m2040: -7300, gauge2: -7650, court: -8200, tax: -9100, capitol: -10100, border: -11000, m2043: -12300, tap: -12750, easel: -13150, m2045: -14000, m2050: -14180, roach: -14450 },
  B: { m2028: 700, treaty: 1200, funnel: 1900, fatcat: 2850, stall: 3700, m2032: 4700, queueBack: 5000, window: 6500, lab: 6950,
    m2035: 7700, factory: 8400, heap: 9250, economist: 9700, m2040: 10500, loop: 11300, m2048: 12400, stacks: 12850, house: 14000 },
};
// The sky behind the plate (fixed to the screen): one flat shade per year, stepping on each milestone.
const SKY = {
  fork: "#EFE3C4",
  a2027: "#E6D2A6", a2033: "#DDBB8B", a2035: "#D89A62", a2040: "#B56A42", a2043: "#4A4B5E", a2045: "#22304A",
  b2028: "#E3ECD9", b2032: "#D4E8DC", b2035: "#C5E4DA", b2040: "#B3DED5", b2048: "#A4D9D0",
};
const GROUND = "#C8B07B", ROAD = "#EEE3C4", EDGE = "#B09363", DUST = "#8E7A55", DASH = "#C7AB78";
const VALLEY = "#8C7A5C", VALLEY_ROAD = "#C9BDA2", ROCK = ["#7A5A44", "#6A4C3A", "#5B4234"], PUFF = "#B9B1A2", CHASM = "#1E1A22";
const YOU = { tone: 2, outfit: "suit", hat: "bowler" };
const ECON = { tone: 1, outfit: "suit", color: 1, glasses: true, hair: 2 };
const WATCH_ARMS = [[-6, -2], [60, -100]]; // the front forearm across his chest, wristwatch up: checking the time

// A plate framing as KIT.camera places it: plate point (x, y) in the middle of the frame, at scale s.
const view = (x, y, s, inner) => `<g transform="translate(${f(960 - x * s)},${f(540 - y * s)}) scale(${s})">${inner}</g>`;
// A host shot's slow push in on her face (KIT.studio), k of the way along.
const push = (S, k, inner) => `<g transform="translate(${S.face[0]},${S.face[1]}) scale(${k}) translate(${-S.face[0]},${-S.face[1]})">${inner}</g>`;
const sky = (col) => `<rect x="-100" y="-100" width="2120" height="1280" fill="${col}"/>`;

// A person standing with its feet on y `feet`, k times person size (KIT.person draws the feet at y 100).
function man(H, o, x, feet, k, extra = "", rot = 0) {
  return H.at(f(x), f(feet - 100 * k), k, H.K.person(o) + extra, rot);
}
function handAt(H, o, x, feet, k, i) {
  const p = H.K.rig(o).hand[i];
  return [x + k * p[0], feet - 100 * k + k * p[1]];
}
// Where person point p lands for a person drawn by man(H, o, x, feet, k, "", rot) (turned rot degrees about (0, 0)).
function toCanvas(p, x, feet, k, rot = 0) {
  const r = (rot * Math.PI) / 180, px = k * p[0], py = k * p[1];
  return [x + px * Math.cos(r) - py * Math.sin(r), feet - 100 * k + px * Math.sin(r) + py * Math.cos(r)];
}
// A thumbs-up fist around (0, 0): the fist, its curled fingers, and the thumb standing up from its top.
function thumbsUp(C, skin, s = 1) {
  return `<g transform="scale(${s})"><rect x="-9" y="-6" width="18" height="16" rx="4" fill="${skin}" stroke="${C.line}" stroke-width="2.4"/>` +
    `<path d="M-9,-1 H4 M-9,4 H4" stroke="${C.line}" stroke-width="1.6"/><rect x="-8" y="-22" width="8" height="18" rx="4" fill="${skin}" stroke="${C.line}" stroke-width="2.4" transform="rotate(-10 -4 -6)"/></g>`;
}
// The markup of the first <g class="cls"> in svg, and svg without it (balanced on <g> tags).
function cutGroup(svg, cls) {
  const start = svg.indexOf(`<g class="${cls}"`);
  if (start < 0) return [svg, ""];
  const re = /<g[\s>]|<\/g>/g;
  re.lastIndex = start;
  let depth = 0, m;
  while ((m = re.exec(svg))) {
    depth += m[0] === "</g>" ? -1 : 1;
    if (depth === 0) return [svg.slice(0, start) + svg.slice(re.lastIndex), svg.slice(start, re.lastIndex)];
  }
  return [svg, ""];
}
// Puffs of smoke or cloud: [x, y, r] circles sharing one navy outline.
function puffs(C, list, fill = PUFF, w = 8) {
  return list.map(([x, y, r]) => `<circle cx="${f(x)}" cy="${f(y)}" r="${f(r)}" fill="${C.line}" stroke="${C.line}" stroke-width="${w}"/>`).join("") +
    list.map(([x, y, r]) => `<circle cx="${f(x)}" cy="${f(y)}" r="${f(r)}" fill="${fill}"/>`).join("");
}
// Wisps of smoke rising from (x, y).
function wisps(x, y, n = 3, s = 1, col = "#8C8782") {
  let out = "";
  for (let i = 0; i < n; i++) out += `<path d="M${f(x + i * 16 * s)},${f(y - i * 6 * s)} l${f(-10 * s)},${f(-18 * s)} l${f(10 * s)},${f(-18 * s)} l${f(-10 * s)},${f(-18 * s)}" fill="none" stroke="${col}" stroke-width="${f(6 * s)}" stroke-linecap="round"/>`;
  return out;
}
// A smoke column standing on the horizon at x (plate units), h tall.
function smokeColumn(C, x, base, h, s = 1) {
  const list = [];
  for (let i = 0; i < 6; i++) list.push([x + Math.sin(i * 1.7) * 18 * s + i * 10 * s, base - i * (h / 6), (40 - i * 2) * s]);
  return puffs(C, list, "#8D8578", 6);
}
// Sweat drops flying off at (x, y).
function sweat(C, x, y, s = 1) {
  return [[-30, -10, -30], [30, -16, 30], [-12, -34, -10]].map(([dx, dy, r]) =>
    `<path d="M${f(x + dx * s)},${f(y + dy * s)} q${f(6 * s)},${f(10 * s)} 0,${f(16 * s)} q${f(-6 * s)},${f(-6 * s)} 0,${f(-16 * s)} Z" fill="#BFE0E6" stroke="${C.line}" stroke-width="2.5" transform="rotate(${r} ${f(x + dx * s)} ${f(y + dy * s)})"/>`).join("");
}

// ── The road (plate units) ──
// The ground from x0 to x1 (the field from the horizon down), the cream road band with its edges and a dashed line.
// dy moves it down (the valley floor: ROADS.DROP); ground and road colors for the valley.
function road(x0, x1, dy = 0, ground = GROUND, band = ROAD) {
  const { HZ, FAR, NEAR } = ROADS, mid = (FAR + NEAR) / 2;
  let dash = "";
  for (let x = Math.ceil(x0 / 100) * 100; x < x1; x += 100) dash += `M${x},${mid + dy} h46 `;
  return `<rect x="${x0}" y="${HZ + dy}" width="${x1 - x0}" height="${3200}" fill="${ground}"/>` +
    `<path d="M${x0},${HZ + dy} H${x1}" stroke="${DUST}" stroke-width="3" opacity="0.6"/>` +
    `<rect x="${x0}" y="${FAR + dy}" width="${x1 - x0}" height="${NEAR - FAR}" fill="${band}"/>` +
    `<path d="M${x0},${FAR + dy} H${x1} M${x0},${NEAR + dy} H${x1}" stroke="${EDGE}" stroke-width="6"/>` +
    `<path d="${dash}" stroke="${DASH}" stroke-width="7"/>`;
}
// A crack across the road at x.
function crack(C, x, dy = 0) {
  const { FAR, NEAR } = ROADS;
  return `<path d="M${x},${FAR + dy} l18,22 l-14,20 l20,24 l-10,${NEAR - FAR - 66}" fill="none" stroke="${C.line}" stroke-width="5" stroke-linejoin="miter"/>`;
}
// A year's milestone: a one-post sign on the road's far edge (KIT.props.sign), at plate x.
function milestone(K, x, year, dy = 0, tilt = 0) {
  return `<g transform="translate(${x},${ROADS.FAR + dy}) rotate(${tilt}) scale(1.35)">${K.props.sign({ text: year, posts: 1, fontSize: 40, height: 64 })}</g>`;
}
// The fork: a tan post with two cream arrow boards, FUTURE A pointing left and FUTURE B pointing right, each ringed
// with bulbs (lit: glowing mustard). Its foot at (0, 0), 520 tall. Drawn the same on the set and on the plate.
function fingerpost(H, litA = false, litB = false) {
  const { C } = H, ink = C.line;
  const board = (y, dir, text, lit) => {
    const x0 = dir * 26, x1 = dir * 272, tip = dir * 312, h = 74;
    const d = `M${x0},${y - h / 2} L${x1},${y - h / 2} L${tip},${y} L${x1},${y + h / 2} L${x0},${y + h / 2} Z`;
    let bulbs = "";
    for (let i = 0; i <= 7; i++) {
      const bx = x0 + ((x1 - x0) * i) / 7;
      for (const by of [y - h / 2, y + h / 2]) bulbs += `<circle cx="${f(bx)}" cy="${f(by)}" r="7" fill="${lit ? C.yellow : C.cream}" stroke="${ink}" stroke-width="2.5"/>`;
    }
    const glow = lit ? `<path d="${d}" fill="none" stroke="${C.yellow}" stroke-width="34" opacity="0.35" stroke-linejoin="round"/>` : "";
    return glow + `<path d="${d}" fill="#FBF6E6" stroke="${ink}" stroke-width="6" stroke-linejoin="round"/>` +
      `<path d="${d}" fill="none" stroke="${C.orange}" stroke-width="2.5" transform="translate(${dir * 12},0) scale(0.93,0.78) translate(${dir * -12},${y * 0.282})"/>` +
      H.label((x0 + x1) / 2, y + 15, 40, text, "middle", ink) + bulbs +
      `<circle cx="${tip - dir * 2}" cy="${y}" r="7" fill="${lit ? C.yellow : C.cream}" stroke="${ink}" stroke-width="2.5"/>`;
  };
  const post = `<path d="M-14,0 V-540 H14 V0 Z" fill="${C.tan}" stroke="${ink}" stroke-width="6"/><path d="M6,-530 V-6" stroke="${C.rust}" stroke-width="4"/>` +
    `<path d="M-22,-540 L0,-566 L22,-540 Z" fill="${C.tan}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>`;
  return post + board(-470, 1, "FUTURE B", litB) + board(-370, -1, "FUTURE A", litA) +
    `<path d="M-40,0 H40" stroke="${ink}" stroke-width="8" stroke-linecap="round"/>`;
}
// A stack of n leg-less bills (KIT.money, front view) standing on y 0 at scale k, each `step` higher than the last.
function billStack(K, kind, n, k = 1.4, step = 20, jit = 5) {
  const bill = K.money(kind).replace(/<path class="legs"[^>]*\/>/, "");
  let out = "";
  for (let i = 0; i < n; i++) out += `<g transform="translate(${f((((i * 37) % 11) - 5) * (jit / 5))},${f(-25 * k - i * step)}) scale(${k})">${bill}</g>`;
  return out;
}
// A flat leg-less bill seen front on, centered on (x, y), k scale, tilted.
function flatBill(K, kind, x, y, k, rot = 0) {
  return `<g transform="translate(${f(x)},${f(y)}) rotate(${rot}) scale(${k})">${K.money(kind).replace(/<path class="legs"[^>]*\/>/, "")}</g>`;
}
// The medicine paper's dented hard hat (Part 10), around (0, 0), its brim on y 0.
function hardHat(C, s = 1) {
  return `<g transform="scale(${s})"><path d="M-26,0 L-24,-18 Q-20,-34 -4,-36 L2,-28 L8,-37 Q24,-34 26,-16 L28,0 Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="3.4" stroke-linejoin="round"/>` +
    `<path d="M-36,0 H36" stroke="${C.line}" stroke-width="7" stroke-linecap="round"/><path d="M-35,0 H35" stroke="${C.yellow}" stroke-width="3.5" stroke-linecap="round"/></g>`;
}
// Birds circling a dizzy head at (x, y).
function birds(C, x, y, s = 1) {
  return `<ellipse cx="${x}" cy="${y}" rx="${70 * s}" ry="${18 * s}" fill="none" stroke="${C.line}" stroke-width="2.5" stroke-dasharray="8 8"/>` +
    [[-60, 6], [10, -16], [55, 10]].map(([dx, dy]) => `<path d="M${f(x + dx * s - 12 * s)},${f(y + dy * s)} q${f(6 * s)},${f(-9 * s)} ${f(12 * s)},0 q${f(6 * s)},${f(-9 * s)} ${f(12 * s)},0" fill="none" stroke="${C.line}" stroke-width="${f(3.5 * s)}" stroke-linecap="round"/>`).join("");
}
// A suitcase, its bottom on y 0.
function suitcase(C, col = C.rust, s = 1) {
  return `<g transform="scale(${s})"><rect x="-26" y="-40" width="52" height="40" rx="4" fill="${col}" stroke="${C.line}" stroke-width="3.5"/>` +
    `<path d="M-10,-40 v-8 h20 v8" fill="none" stroke="${C.line}" stroke-width="4"/><path d="M-26,-22 H26" stroke="${C.tan}" stroke-width="3"/></g>`;
}
// The studio's lectern props (16:9): the case file standing at the lectern's left end, "~~EARTH~~ DIRT: CASE #847"
// with its two stamps (MAY BE ELIGIBLE FOR OPTIMIZATION, SUBOPTIMAL), and the mug at its right end; Part 26's
// drawings (caseFile(H, 2), mug(H)), so the file reads the same in every part.
function lecternProps(H, mug = true) {
  const S = H.K.STUDIO, cx = S.lect[0], hw = S.lect[1] / 2, top = S.top;
  return (mug ? H.at(cx + hw - 50, top + 4, 1, mugSvg(H)) : "") + H.at(cx - hw + 120, top + 6, 0.82, caseFile(H, 2));
}

export default {
  "choose-your-own-adventure-title"(H, fid) {
    const { K, C } = H;
    // KIT.titleScene's atomic card (16:9): the emblem at (960, 290); two papers running, the third stopped at the
    // crossing of the flat orbit and the one tilted 60 degrees, looking both ways
    const cx = 960, cy = 290, rx = 200, ry = 62, TILT = [0, 60, -60];
    const orbits = TILT.map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const onOrbit = (a, th) => {
      const r = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return [cx + ex * Math.cos(r) - ey * Math.sin(r), cy + ex * Math.sin(r) + ey * Math.cos(r)];
    };
    // the crossing of orbit 0 and orbit 60 on the upper right: search orbit 0 for the point that lies on orbit 60
    let best = [0, 9];
    for (let th = -Math.PI; th < 0; th += 0.002) {
      const [x, y] = onOrbit(0, th), dx = x - cx, dy = y - cy, r = (-60 * Math.PI) / 180;
      const u = dx * Math.cos(r) - dy * Math.sin(r), v = dx * Math.sin(r) + dy * Math.cos(r);
      const e = Math.abs((u / rx) ** 2 + (v / ry) ** 2 - 1);
      if (x > cx && e < best[1]) best = [th, e];
    }
    const [kx, ky] = onOrbit(0, best[0]);
    const runners = [[60, 0.6], [-60, 3.6]].map(([a, th]) => { const [x, y] = onOrbit(a, th); return H.at(f(x), f(y - 6), 0.62, K.money("war", 1)); }).join("");
    // skid marks behind it and a little "which way?" twitch either side
    const look = `<path d="M${f(kx - 70)},${f(ky + 2)} h-34 M${f(kx - 66)},${f(ky + 12)} h-24" stroke="${C.cream}" stroke-width="4" stroke-linecap="round" opacity="0.8"/>` +
      `<path d="M${f(kx - 44)},${f(ky - 52)} l-12,-14 M${f(kx + 44)},${f(ky - 52)} l12,-14 M${f(kx)},${f(ky - 58)} v-16" stroke="${C.yellow}" stroke-width="4" stroke-linecap="round"/>`;
    const stopped = H.at(f(kx), f(ky - 18), 0.82, K.money("war", 0), -6) + look;
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + runners + nucleus + stopped +
      H.big(960, 610, 104, "CHOOSE YOUR OWN", "middle", C.cream) + H.big(960, 830, 196, "ADVENTURE", "middle", C.cream);
    return { svg, alt: "The period title card: CHOOSE YOUR OWN ADVENTURE in cream on navy under the film's atom; two little war-seal papers run round its orbits, and the third has skidded to a stop where two orbits cross, looking both ways." };
  },

  "fork-in-the-road"(H, fid) {
    const { K, C } = H, S = K.STUDIO;
    // on "existence.": the fingerpost on the free wall (foot y 1070, scale 1.35, its boards over YOU's head), YOU under
    // it holding his wristwatch to his ear
    const post = H.at(1470, 1070, 1.35, fingerpost(H));
    const you = copy(YOU, { look: "left", mood: "worried", arms: [[-8, -3], [152, -116]] });
    const k = 2.3, yx = 1500;
    const w = handAt(H, you, yx, 1066, k, 1);
    const watch = `<circle cx="${f(w[0] + 3)}" cy="${f(w[1] + 9)}" r="9" fill="${C.cream}" stroke="${C.line}" stroke-width="3.5"/>`;
    const tick = `<path d="M${f(w[0] + 30)},${f(w[1] - 22)} q10,-10 0,-22 M${f(w[0] + 44)},${f(w[1] - 16)} q14,-16 0,-32" fill="none" stroke="${C.line}" stroke-width="4" stroke-linecap="round"/>`;
    const front = post + man(H, you, yx, 1066, k) + watch + tick + lecternProps(H);
    const svg = push(S, 1.02, H.host("happy-smile", "wide-gesture", front));
    return { svg, alt: "Wishonia throws both arms wide at her lectern; beside her on the studio wall a fingerpost with two arrow boards, FUTURE A pointing left and FUTURE B pointing right, and under it the busy human in his bowler holding his wristwatch to his ear." };
  },

  "economists-straight-line"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "simultaneously": the row of six dominoes leaning right on each other, the plank across their tops, and the
    // economist at the right end bracing the last one with everything he has
    const G = 880, HZN = 470, W = 112, lean = 14, rr = (lean * Math.PI) / 180;
    const DH = (i) => 250 + i * 30, DX = (i) => 250 + i * 190;
    const icons = [
      (s) => H.at(0, 22, 0.34 * s, K.props.missile({ mood: "smug", arms: "none" })),
      (s) => `<g transform="scale(${s})"><path d="M-22,-10 Q-22,-36 0,-36 Q22,-36 22,-10 V2 H12 V10 H-12 V2 H-22 Z" fill="${C.cream}" stroke="${ink}" stroke-width="4"/><circle cx="-9" cy="-14" r="6" fill="${ink}"/><circle cx="9" cy="-14" r="6" fill="${ink}"/></g>`,
      (s) => `<g transform="scale(${s})"><rect x="-12" y="-30" width="24" height="44" fill="${C.rust}" stroke="${ink}" stroke-width="4"/></g>` + puffs(C, [[4 * s, -42 * s, 10 * s], [14 * s, -60 * s, 12 * s]], PUFF, 4),
      (s) => H.at(0, 22 * s, 0.7 * s, K.props.germ({})),
      (s) => `<g transform="scale(${s})"><circle r="24" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/><path d="M-6,-24 l8,14 l-8,10 l10,24" fill="none" stroke="${ink}" stroke-width="4"/></g>`,
      (s) => H.at(0, 30 * s, 0.11 * s, K.nuke()),
    ];
    // each domino stands on its bottom right corner (pivot), leaning right by `lean` degrees onto the next one
    const pivot = (i) => [DX(i) + W, G];
    const rot = (i, dx, dy) => { const [px, py] = pivot(i); return [px + dx * Math.cos(rr) - dy * Math.sin(rr), py + dx * Math.sin(rr) + dy * Math.cos(rr)]; };
    const topOf = (i) => rot(i, -W, -DH(i)); // its top left corner
    const face = (i, u) => rot(i, 0, -DH(i) * u); // a point u of the way up its right face
    let row = "";
    for (let i = 0; i < 6; i++) {
      const h = DH(i), x = DX(i);
      row += `<g transform="rotate(${lean} ${x + W} ${G})"><rect x="${x}" y="${G - h}" width="${W}" height="${h}" rx="10" fill="#FBF6E6" stroke="${ink}" stroke-width="6"/>` +
        `<path d="M${x + 14},${G - h / 2} H${x + W - 14}" stroke="${ink}" stroke-width="5"/>` +
        `<g transform="translate(${x + W / 2},${G - h * 0.75})">${icons[i](1.2)}</g>` +
        `<circle cx="${x + W / 2 - 24}" cy="${G - h * 0.3}" r="9" fill="${ink}"/><circle cx="${x + W / 2 + 24}" cy="${G - h * 0.18}" r="9" fill="${ink}"/></g>`;
    }
    // the plank: dead straight across the domino tops and on past the last one, over the economist's head
    const a = topOf(0), b = topOf(5), sl = (b[1] - a[1]) / (b[0] - a[0]), x1 = 1620, pe = [x1, a[1] + sl * (x1 - a[0])];
    const plank = `<path d="M${f(a[0] - 30)},${f(a[1] - 30 * sl)} L${f(pe[0])},${f(pe[1])} L${f(pe[0])},${f(pe[1] - 28)} L${f(a[0] - 30)},${f(a[1] - 30 * sl - 28)} Z" fill="${C.tan}" stroke="${ink}" stroke-width="6" stroke-linejoin="round"/>` +
      `<path d="M${f(a[0])},${f(a[1] - 14)} L${f(pe[0] - 20)},${f(pe[1] - 14 - sl * 20)}" stroke="${C.rust}" stroke-width="3"/>`;
    // the economist right of the last domino, leaning in: both hands and his forehead on its face, the yardstick in
    // his teeth propping the plank's end over his head
    const ec = copy(ECON, { look: "left", mood: "worried", arms: [[-140, -150], [-128, -142]] });
    const k = 2.0, lean2 = -14, ex = 1455;
    const mouth = toCanvas(K.rig(ec).mouth, ex, G, k, lean2), plankAt = [mouth[0] - 6, pe[1] + (mouth[0] - 6 - pe[0]) * sl - 4];
    const yard = `<path d="M${f(mouth[0])},${f(mouth[1])} L${f(plankAt[0])},${f(plankAt[1])}" stroke="${ink}" stroke-width="16" stroke-linecap="square"/><path d="M${f(mouth[0])},${f(mouth[1])} L${f(plankAt[0])},${f(plankAt[1])}" stroke="${C.yellow}" stroke-width="10"/>` +
      `<path d="M${f(mouth[0])},${f(mouth[1])} L${f(plankAt[0])},${f(plankAt[1])}" stroke="${ink}" stroke-width="10" stroke-dasharray="2 16"/>`;
    // the broom wedged under the fourth domino's face, its brush on the ground
    const fp = face(3, 0.55), brush = [fp[0] + 150, G];
    const broom = `<path d="M${f(brush[0])},${f(brush[1] - 20)} L${f(fp[0])},${f(fp[1])}" stroke="${ink}" stroke-width="16" stroke-linecap="round"/><path d="M${f(brush[0])},${f(brush[1] - 20)} L${f(fp[0])},${f(fp[1])}" stroke="${C.rust}" stroke-width="9" stroke-linecap="round"/>` +
      `<path d="M${f(brush[0] - 34)},${G + 4} L${f(brush[0] - 4)},${G - 40} L${f(brush[0] + 40)},${G - 12} L${f(brush[0] + 30)},${G + 6} Z" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/>`;
    const sign = H.at(200, G, 1.3, K.props.sign({ text: "+2.5%", posts: 1, fontSize: 36, height: 50 }));
    const head = toCanvas([0, K.rig(ec).hy], ex, G, k, lean2);
    const svg = sky("#EFE3C4") + `<rect y="${HZN}" width="1920" height="700" fill="${GROUND}"/><path d="M0,${HZN} H1920" stroke="${DUST}" stroke-width="3" opacity="0.6"/>` +
      row + plank + broom + sign + man(H, ec, ex, G, k, "", lean2) + yard + sweat(C, head[0] + 40, head[1] - 40, 1.6) +
      `<path d="M${f(head[0] + 70)},${f(head[1] + 10)} l18,-6 M${f(head[0] + 74)},${f(head[1] + 30)} l20,0 M${f(head[0] + 70)},${f(head[1] + 50)} l18,6" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`;
    return { svg, alt: "On a plain field a row of six tall dominoes, painted with a missile, a skull, a chimney, a germ, a cracked coin and a mushroom cloud, leans over in a chain under a long straight plank; at its end the bald economist in glasses holds the plank up with both hands and the yardstick in his teeth, a broom propping the row, sweat flying; a little sign at the start reads +2.5%." };
  },

  "earn-1-57-times"(H, fid) {
    const { K, C } = H;
    // after "you.": the whole plate from the front; the two YOUs by their stacks, the left one charred
    const G = 820, F = 900;
    const factory = H.at(400, G, 0.9, K.props.factory({ label: "" }));
    const wm = H.at(400, G - 100 * 0.95, 0.95, K.cast("weaponsMaker"));
    const funnel = H.at(960, G, 0.85, K.props.colorFlipFunnel({ inN: 0, outN: 2 }));
    const hospital = H.at(1560, G, 0.9, K.props.hospital({}));
    const meds = [1460, 1520].map((x, i) => H.at(x, G - 26, 0.55, K.money("med", i))).join("");
    const cloud = `<g opacity="0.55">${H.at(560, F - 40, 0.62, K.nuke())}</g>`;
    const left = man(H, copy(YOU, { charred: true, look: "right" }), 560, F, 1.6) + wisps(560, F - 330, 3, 1.3);
    const right = man(H, copy(YOU, { look: "left", mood: "smile", hairColor: "#9A9A9A", arms: [[-30, -150], [30, 150]] }), 1360, F, 1.6);
    const short = `<g transform="translate(700,${F})">${K.burn(billStack(K, "plain", 10, 1.1, 20))}</g>` + wisps(700, F - 280, 2, 1);
    const tall = `<g transform="translate(1210,${F})">${billStack(K, "plain", 16, 1.1, 20)}</g>`;
    const svg = sky("#EFE3C4") + `<rect y="470" width="1920" height="700" fill="${GROUND}"/><path d="M0,470 H1920" stroke="${DUST}" stroke-width="3" opacity="0.6"/>` +
      factory + wm + funnel + hospital + meds + cloud + short + left + tall + right + H.big(1210, 300, 140, "1.57×", "middle", C.navy);
    return { svg, alt: "The war factory with its missile chimneys on the left, the color-flip funnel in the middle, a hospital on the right; in front, the left YOU stands charred black and smoking beside a singed short stack of papers under a thinning mushroom cloud, and the right YOU flexes beside a stack half as tall again, 1.57× in the sky over it." };
  },

  "not-complicated"(H, fid) {
    const { K, C } = H, S = K.STUDIO;
    // after "insight.": the charred YOU beside the lectern, one arm gone, looking down at it on the floor
    const o = copy(YOU, { charred: true, look: "left", arms: [[-6, -2], [10, 4]] });
    const [body, arm] = cutGroup(K.person(o), "arm-r");
    const k = 3.0, x = 1420, feet = 1066;
    const crown = toCanvas(K.rig(o).top, x, feet, k);
    const you = H.at(x, feet - 100 * k, k, body) + wisps(crown[0] - 20, crown[1] - 50, 3, 2);
    const fallen = `<g transform="translate(${x + 150},${feet - 26}) rotate(-84) scale(${k}) translate(-17,26)">${arm}</g>`;
    const stack = `<g transform="translate(${x - 120},${feet})">${K.burn(billStack(K, "plain", 6, 1.6, 26))}</g>`;
    const svg = push(S, 1.03, H.host("sideeye-closed", "idle", stack + you + fallen + lecternProps(H)));
    return { svg, alt: "Wishonia side-eyes the camera at her lectern; beside her the charred, smoking YOU in his bowler looks down at his own arm lying on the studio floor, his singed short stack of papers at his feet." };
  },

  "future-a-2027"(H, fid) {
    const { K, C } = H, R = ROADS, A = R.A;
    // after "weird.": the 604 bar out of the top of the frame, a war paper flat on the medicine paper at its foot
    const x0 = A.bar604, s = 1, cx = x0 + 230;
    const bar = `<g transform="translate(${x0},${R.FAR})">${billStack(K, "war", 44, 1.4, 21, 6)}</g>`;
    const squashed = `<g transform="translate(${x0 - 190},${R.FAR + 2})"><g transform="scale(1.2,0.34)">${K.money("med").replace(/<path class="legs"[^>]*\/>/, "")}</g></g>` +
      flatBill(K, "war", x0 - 190, R.FAR - 12, 1.3, 0).replace("scale(1.3)", "scale(1.3,0.32)") +
      `<g transform="translate(${x0 - 270},${R.FAR - 2}) rotate(-20)">${hardHat(C, 1.1)}</g>` +
      `<path d="M${x0 - 128},${R.FAR - 8} l22,-26" stroke="${C.line}" stroke-width="3"/><path d="M${x0 - 106},${R.FAR - 34} l16,4 l-6,12 Z" fill="#FBF6E6" stroke="${C.line}" stroke-width="2"/>`;
    const pram = (x) => `<g transform="translate(${x},${R.FEET})"><circle cx="-34" cy="-14" r="14" fill="none" stroke="${C.line}" stroke-width="5"/><circle cx="34" cy="-14" r="14" fill="none" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M-60,-40 H60 Q60,-90 20,-100 L-10,-100 Q-60,-96 -60,-40 Z" fill="${C.navy}" stroke="${C.line}" stroke-width="5"/><path d="M20,-100 Q60,-90 60,-40" fill="none" stroke="${C.cream}" stroke-width="4"/>` +
      `<path d="M60,-60 L96,-96 h16" fill="none" stroke="${C.line}" stroke-width="6" stroke-linecap="round"/></g>`;
    const mom = copy({ tone: 1, outfit: "dress", hair: 1, color: 3, seed: 4 }, { look: "left", arms: [[-50, -70], [-40, -66]] });
    const paper = copy({ tone: 3, outfit: "suit", color: 2, seed: 6 }, { look: "left", arms: [[-40, -110], [40, -70]] });
    const ph = handAt(H, paper, x0 - 420, R.FEET, R.K, 0);
    const newspaper = `<g transform="translate(${f(ph[0] - 34)},${f(ph[1] - 30)}) rotate(-6)"><rect x="-40" y="-46" width="84" height="96" fill="#F4EEDD" stroke="${C.line}" stroke-width="4"/>` +
      `<path d="M-30,-30 H34 M-30,-16 H34 M-30,-2 H20 M-30,12 H34 M-30,26 H30" stroke="${C.line}" stroke-width="3" opacity="0.6"/><rect x="-30" y="-42" width="64" height="8" fill="${C.line}"/></g>`;
    const plate = road(cx - 1300, cx + 1300) +
      milestone(K, A.m2027, "2027") + squashed + bar +
      pram(x0 + 190) + man(H, mom, x0 + 310, R.FEET, R.K) +
      man(H, paper, x0 - 420, R.FEET, R.K) + newspaper +
      man(H, copy(YOU, { look: "left", arms: WATCH_ARMS }), x0 + 480, R.FEET, R.K);
    const svg = sky(SKY.a2027) + view(cx, -200, s, plate);
    return { svg, alt: "On road A by the 2027 milestone, the 604 bar of war papers runs up out of the top of the frame; at its foot a war paper lies flat on the squashed medicine paper, its dented hard hat knocked off and a tiny white flag poking out, while a woman with a pram, a man reading a newspaper and YOU checking his watch walk by without looking up." };
  },

  "future-a-2033"(H, fid) {
    const { K, C } = H, R = ROADS, A = R.A;
    // after "planning.": the gauge in the red at 25, the USSR headstone and rubble at its foot, the robot's head
    // smoking over its blank PLAN clipboard, YOU walking by blinking red with a thumbs up
    const cx = -3150, G = R.FAR;
    const gauge = K.props.gauge({ value: 25 / 30, zones: [[25 / 30, 1, C.war]], marks: [[0, "0"], [0.5, "15"], [25 / 30, "25"], [1, "30"]], window: "2033", label: "% OF GDP" });
    const gk = 2.9, gx = A.gauge, dcy = G - 100 * gk;
    let vine = `<path d="M${gx + 190},${G - 8} C${gx + 170},${G - 120} ${gx + 220},${dcy + 110} ${gx + 160},${dcy + 30} C${gx + 230},${dcy - 80} ${gx + 110},${dcy - 210} ${gx},${dcy - 196} C${gx - 150},${dcy - 190} ${gx - 230},${dcy - 60} ${gx - 170},${dcy + 60}" fill="none" stroke="#5B7A3A" stroke-width="9" stroke-linecap="round"/>`;
    [[gx + 180, G - 110, 30], [gx + 200, dcy + 30, -20], [gx + 150, dcy - 140, 40], [gx - 30, dcy - 200, -10], [gx - 190, dcy - 90, 20], [gx - 175, dcy + 40, -30]].forEach(([x, y, r]) => { vine += flatBill(K, "war", x, y, 0.5, r); });
    const rubble = [[gx + 262, -10], [gx + 300, 12], [gx + 340, -4], [gx + 285, 26]].map(([x, r], i) => `<path d="M${x - 40},${G} L${x - 30},${G - 40 - (i % 3) * 14} L${x + 26},${G - 52 - (i % 2) * 10} L${x + 40},${G} Z" fill="${i % 2 ? C.slate : C.navy}" stroke="${C.ink}" stroke-width="4" transform="rotate(${r} ${x} ${G})"/>`).join("");
    const stone = H.at(gx + 450, G, 1.5, K.props.headstone({ text: "USSR" }));
    // the robot out of its crate, the blank PLAN clipboard held up in front of its chest, its head smoking, bulb popped
    const rx = A.robot, rk = 1.45, rb = G - 64;
    const crate = `<path d="M${rx - 120},${G} V${G - 70} H${rx + 120} V${G} Z" fill="${C.tan}" stroke="${C.ink}" stroke-width="5"/><path d="M${rx - 120},${G - 70} l-40,-50 M${rx + 120},${G - 70} l40,-50" stroke="${C.ink}" stroke-width="5"/><path d="M${rx - 120},${G - 35} H${rx + 120}" stroke="${C.rust}" stroke-width="4"/>`;
    const robot = H.at(rx, rb, rk, K.props.robot({ mood: "scared", arms: [[-70, -150], [70, 150]] }));
    const clip = H.at(rx, rb - 14, 1.0, K.props.clipboard({ title: "PLAN:", items: [] }));
    const hy = rb - 160 * rk;
    const smoke = puffs(C, [[rx - 70, hy, 20], [rx - 100, hy - 26, 28], [rx - 112, hy - 66, 34], [rx + 70, hy, 20], [rx + 100, hy - 26, 28], [rx + 112, hy - 66, 34]], PUFF, 5);
    const spin = [-1, 1].map((s) => `<path d="M${rx + s * 13 - 6},${hy + 4} a6,6 0 1,1 6,6 a10,10 0 1,1 10,-10" fill="none" stroke="${C.war}" stroke-width="2.5"/>`).join("");
    const bulb = `<path d="M${rx},${rb - 186 * rk} l-12,-20 l9,5 l3,-18 l6,16 l9,-7 l-6,22 Z" fill="${C.cream}" stroke="${C.ink}" stroke-width="3"/>`;
    const yx = rx + 330, youO = copy(YOU, { look: "left", light: "red", arms: [[-6, -2], [-84, -112]] });
    const th = handAt(H, youO, yx, R.FEET, R.K, 1);
    const thumb = H.at(f(th[0]), f(th[1] - 4), 2.0, thumbsUp(C, "#A87B57"));
    const blink = `<circle cx="${f(yx + 2)}" cy="${f(R.FEET - 150 - 6)}" r="14" fill="${C.war}" opacity="0.35"/>`;
    const plate = road(cx - 1300, cx + 1300) + milestone(K, A.m2033, "2033") + H.at(gx, G, gk, gauge) + vine + rubble + stone +
      crate + robot + clip + smoke + spin + bulb + man(H, youO, yx, R.FEET, R.K) + thumb + blink;
    const svg = sky(SKY.a2033) + view(cx - 60, -330, 0.95, plate);
    return { svg, alt: "On road A at 2033 the giant gauge from Part 11, a vine of war papers round its dial, points into the red at 25; at its foot the USSR headstone and the rubble of the Soviet plan. Beside it a tin robot out of its crate holds up a clipboard reading PLAN: with nothing on it, smoke pouring from its ears and its bulb popped, while YOU walks past, his chest light red, giving it a thumbs up." };
  },

  "future-a-2035"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "dose.": pushed in through the hospital's ground-floor window: the charred orderly holding out his cup, YOU
    // a skeleton in the bed under the monitor's skull at 00:00:00, the last of the smoke
    // the hospital's cream wall round the big window, its sill, and the curtains pulled back inside
    const wall = `<rect width="1920" height="1080" fill="#EDE6CF"/>` + `<rect x="150" y="60" width="1620" height="860" fill="#A9CFC9" stroke="${ink}" stroke-width="14"/>` +
      `<rect x="120" y="920" width="1680" height="34" fill="${C.cream}" stroke="${ink}" stroke-width="6"/>`;
    const room = `<rect x="157" y="700" width="1606" height="213" fill="#86B3AE"/><path d="M157,700 H1763" stroke="${ink}" stroke-width="4" opacity="0.5"/>`;
    const curtains = `<path d="M157,67 H300 Q250,400 330,900 H157 Z" fill="${C.cyan}" stroke="${ink}" stroke-width="5"/><path d="M1763,67 H1640 Q1700,400 1610,900 H1763 Z" fill="${C.cyan}" stroke="${ink}" stroke-width="5"/>`;
    const bed = `<rect x="600" y="640" width="780" height="44" fill="#FBF6E6" stroke="${ink}" stroke-width="6"/><rect x="616" y="684" width="748" height="60" fill="${C.cream}" stroke="${ink}" stroke-width="6"/>` +
      `<path d="M630,744 V900 M1350,744 V900" stroke="${ink}" stroke-width="12"/><path d="M600,500 V684 M1380,580 V684" stroke="${ink}" stroke-width="12"/>` +
      `<rect x="612" y="560" width="190" height="80" rx="26" fill="#FFFFFF" stroke="${ink}" stroke-width="5"/>`;
    // YOU lying in the bed (the person turned -90: head to the left on the pillow), a grinning skeleton in his bowler
    const skel = `<g transform="translate(860,606) rotate(-90) scale(2.3)">${K.person(copy(YOU, { skeleton: true, arms: [[20, 60], [-20, -60]] }))}</g>`;
    const blanket = `<path d="M930,566 Q1150,530 1376,600 V660 H910 Z" fill="${C.peri}" stroke="${ink}" stroke-width="6"/><path d="M940,604 Q1150,572 1376,628" fill="none" stroke="${C.cream}" stroke-width="6"/>`;
    const tv = K.props.tvSet({}).replace("<!--tv-screen-->",
      `<rect x="-63" y="-134" width="80" height="83" fill="#1E2A2A"/><g transform="translate(-23,-104)"><path d="M-16,-2 Q-16,-22 0,-22 Q16,-22 16,-2 V6 H8 V12 H-8 V6 H-16 Z" fill="${C.cream}"/><circle cx="-6" cy="-6" r="4" fill="#1E2A2A"/><circle cx="6" cy="-6" r="4" fill="#1E2A2A"/></g>` +
      `<text x="-23" y="-60" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="15" fill="${C.war}">00:00:00</text>`);
    const monitor = `<path d="M440,900 V700" stroke="${ink}" stroke-width="10"/>` + H.at(440, 700, 1.55, tv);
    const ord = K.castOpts("orderly", { charred: true, look: "left", arms: [[-70, -96], [6, 2]], holdR: null, holdL: "cup" });
    const ok = 2.5, ox = 1530;
    const top = toCanvas(K.rig(ord).top, ox, 912, ok);
    const orderly = man(H, ord, ox, 912, ok) + wisps(top[0] - 24, top[1] - 40, 3, 1.8);
    const cupAt = handAt(H, ord, ox, 912, ok, 0);
    const smoke = puffs(C, [[1000, 470, 34], [1060, 440, 42], [1130, 470, 32]], "#D8D2C2", 6);
    // the medicine cup still held out, singed at the rim, the last smoke curling out of it
    const cup = `<g transform="translate(${f(cupAt[0] - 6)},${f(cupAt[1] - 6)}) scale(2.2)"><path d="M-9,-14 H9 L6,4 H-6 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="2.4" stroke-linejoin="round"/><path d="M-9,-14 H9 L8.4,-10 H-8.4 Z" fill="#4A3A30"/></g>`;
    const svg = wall + room + curtains + smoke + bed + skel + blanket + monitor + orderly + cup +
      puffs(C, [[cupAt[0] - 8, cupAt[1] - 64, 12], [cupAt[0] + 6, cupAt[1] - 88, 15]], "#9A948A", 4);
    return { svg, alt: "Through the hospital's big window: YOU lies in the bed as a grinning skeleton in his bowler, the blanket pulled up; beside him the bedside monitor shows a grinning skull over 00:00:00, and the orderly in scrubs stands charred black and smoking, hair straight up, still holding out his medicine cup." };
  },

  "future-a-2040"(H, fid) {
    const { K, C } = H, R = ROADS, A = R.A;
    // on "can" (the second), just before the cut to audit-side-eye: the tax office folded flat, the auditor flat on his
    // back, birds circling, the last little robot zipping off with his empty in-tray, YOU's skeleton strolling past, the
    // gauge behind with its needle bent off the scale
    const cx = -9000, G = R.FAR;
    const smoke = smokeColumn(C, -9700, R.HZ, 330, 1.3) + smokeColumn(C, -8200, R.HZ, 260, 1.1);
    const flat = `<g transform="translate(${A.tax},${G}) scale(1.5,0.16)">${K.props.bank({ label: "TAX OFFICE" })}</g>`;
    const sign = H.at(A.tax - 420, G, 1.3, K.props.sign({ text: "TAX OFFICE", fontSize: 34, height: 40 }));
    const aud = copy({ tone: 3, outfit: "suit", color: 2, seed: 7 }, { mood: "worried", arms: [[150, 150], [-150, -150]] });
    const auditor = `<g transform="translate(${A.tax + 40},${R.FEET - 30}) rotate(-90) scale(1.5)">${K.person(aud)}</g>`;
    // the robot zipping off left with the empty in-tray held over its head, speed lines behind it (to the right)
    const zx = A.tax - 820, zk = 0.75, zb = R.FEET - 64 * zk;
    const zipper = H.at(zx, zb, zk, K.props.robot({ mood: "grin", arms: [[-160, -170], [160, 170]] }), -8);
    const tray = `<g transform="translate(${zx - 8},${zb - 205 * zk}) rotate(-8)"><path d="M-46,0 L-38,-26 H38 L46,0 Z" fill="${C.tan}" stroke="${C.line}" stroke-width="4"/></g>` +
      [0, 1, 2].map((i) => `<path d="M${zx + 70 + i * 12},${zb - 120 + i * 45} h${90 - i * 20}" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/>`).join("") + zipper;
    const glass = `<path d="M${A.tax - 220},${R.FEET - 90} l12,10" stroke="${C.line}" stroke-width="5"/><circle cx="${A.tax - 236}" cy="${R.FEET - 104}" r="20" fill="#FFFFFF" fill-opacity="0.4" stroke="${C.line}" stroke-width="4"/>`;
    const dizzy = birds(C, A.tax - 130, R.FEET - 150, 1.2);
    // the gauge behind, on the right: its needle bent round the rim past 30, the glass cracked
    const gx = A.tax + 900, gk = 2.4, dcy = G - 100 * gk;
    const gauge = K.props.gauge({ value: 1, zones: [[25 / 30, 1, C.war]], marks: [[0, "0"], [0.5, "15"], [25 / 30, "25"], [1, "30"]], window: "2040", label: "% OF GDP" });
    // in gauge units (the dial's center at (0, -100), the needle's tip at value 1 at (39, -77.5)): the needle runs on
    // past 30, bends round the rim and up; the glass cracks from where it hit
    const bent = `<g transform="translate(${gx},${G}) scale(${gk})"><path d="M37,-78.5 Q52,-70 56,-88 Q58,-104 50,-118" fill="none" stroke="${C.line}" stroke-width="5.5" stroke-linecap="round"/>` +
      `<path d="M37,-78.5 Q52,-70 56,-88 Q58,-104 50,-118" fill="none" stroke="${C.war}" stroke-width="3" stroke-linecap="round"/>` +
      `<path d="M50,-118 l-14,-4 l-6,10 l-12,-12 l-10,6 M30,-112 l-8,18 l-14,4 M36,-122 l-4,-18" fill="none" stroke="${C.line}" stroke-width="1.4"/></g>`;
    const skel = man(H, copy(YOU, { skeleton: true, look: "left", arms: WATCH_ARMS }), A.tax + 560, R.FEET, R.K);
    const plate = road(cx - 1300, cx + 1300) + smoke + H.at(gx, G, gk, gauge) + bent + flat + sign + auditor + glass + dizzy + tray + skel + crack(C, A.tax + 720);
    const svg = sky(SKY.a2040) + view(cx, -240, 0.92, plate);
    return { svg, alt: "Under a rust sky with smoke columns, the TAX OFFICE lies folded flat as cardboard; the auditor lies on his back in front of it, birds circling his head, his magnifying glass dropped, and the last little robot zips off with his empty in-tray held over its head; YOU's skeleton in his bowler strolls past checking his watch, and behind them the gauge's needle is bent round past 30 and its glass is cracked." };
  },

  "audit-side-eye"(H, fid) {
    const { C } = H, S = H.K.STUDIO;
    // on "audit.": the reaction cut, pushed in close: arms crossed, the side-eye, nobody else on the set
    const svg = push(S, 1.12, H.host("sideeye-closed", "arms-crossed", lecternProps(H)));
    return { svg, alt: "A reaction cut to the lectern, pushed in close: Wishonia, arms crossed, side-eyes the camera; the mug and the case file stand on the lectern." };
  },

  "rot-in-place"(H, fid) {
    const { K, C } = H, R = ROADS, A = R.A;
    // on "Colombia." (second): the refugees walking off the cliff edge in step, eyes front, never looking down; the first
    // two already dropping below the edge still mid-stride, YOU's skeleton last on the road, checking his watch
    const cx = R.CLIFF + 60, edge = R.CLIFF;
    const plateau = road(edge, edge + 2000);
    const chasm = `<rect x="${edge - 2000}" y="${R.HZ}" width="2000" height="3200" fill="${CHASM}"/>` +
      `<path d="M${edge - 2000},${R.HZ} H${edge}" stroke="#3A2E2A" stroke-width="3"/>`;
    const face = `<path d="M${edge},${R.FAR} L${edge - 18},${R.NEAR + 60} L${edge + 10},${R.NEAR + 200} L${edge - 24},${R.NEAR + 420} L${edge + 4},1200 H${edge + 60} V${R.FAR} Z" fill="${ROCK[1]}" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M${edge},${R.FAR} H${edge + 60}" stroke="${EDGE}" stroke-width="8"/>`;
    // the COLOMBIA signpost keeled over onto the road, its foot still at its stump, its card face up toward us
    const fallen = `<path d="M${edge + 760},${R.FAR + 6} v-30" stroke="${C.line}" stroke-width="10"/>` +
      `<g transform="translate(${edge + 760},${R.FAR + 34}) rotate(-80) scale(1.15)">${K.props.sign({ text: "COLOMBIA", posts: 1, fontSize: 34, height: 70 })}</g>`;
    // all in the same stride (the same legPose), facing left down the road; [person, x, how far it has dropped, suitcase]
    const STRIDE = { legPose: [[-36, -14], [32, 18]] };
    const people = [
      [{ tone: 0, outfit: "dress", hair: 1, color: 1, seed: 11 }, edge - 330, 330, C.rust],
      [{ tone: 3, outfit: "shirt", color: 0, seed: 12 }, edge - 150, 110, C.peri],
      [{ tone: 1, outfit: "suit", color: 2, seed: 13 }, edge + 60, 0, C.tan],
    ].map(([o, x, dy, col]) => {
      const p = copy(o, { look: "left", mood: "flat", arms: [[-6, -2], [10, 4]], build: STRIDE });
      const feet = R.FEET + dy, h = handAt(H, p, x, feet, R.K, 1);
      // speed lines over the ones already dropping
      const top = toCanvas(K.rig(p).top, x, feet, R.K);
      const lines = dy ? [-40, 0, 40].map((d) => `<path d="M${f(x + d)},${f(top[1] - 40)} v${f(-60 - dy * 0.3)}" stroke="${C.cream}" stroke-width="5" stroke-linecap="round" opacity="0.7"/>`).join("") : "";
      return lines + man(H, p, x, feet, R.K) + H.at(f(h[0] + 6), f(h[1] + 46), 1.3, suitcase(C, col));
    }).join("");
    const skel = man(H, copy(YOU, { skeleton: true, look: "left", arms: WATCH_ARMS, build: STRIDE }), edge + 290, R.FEET, R.K);
    const plate = chasm + plateau + face + fallen + people + skel;
    const svg = sky(SKY.a2040) + view(cx, -130, 0.95, plate);
    return { svg, alt: "At the end of road A the road stops at a cliff edge over a dark chasm; the COLOMBIA sign lies flat on the road behind. A line of refugees with suitcases walks off the edge in step, eyes front, never looking down: the first two are already dropping into the dark still mid-stride, the third is stepping off, and YOU's skeleton brings up the rear on the road, checking his watch." };
  },

  "future-a-2043"(H, fid) {
    const { K, C } = H, R = ROADS, A = R.A, D = R.DROP;
    // on "columns.": the charred survivors at the spreadsheet easel, each holding up half of YOU's skeleton in his
    // own column; the bowler rolling away; the mushroom cloud on the horizon
    const cx = A.easel + 60;
    const plate = road(cx - 1300, cx + 1300, D, VALLEY, VALLEY_ROAD) + crack(C, cx - 500, D) + crack(C, cx + 620, D) +
      H.at(cx - 700, R.HZ + D + 6, 0.7, K.nuke()) + milestone(K, A.m2043, "2043", D, -6);
    const ex = A.easel, top = R.FAR + D - 560;
    const easel = `<path d="M${ex - 260},${R.FAR + D} L${ex - 200},${top + 40} M${ex + 260},${R.FAR + D} L${ex + 200},${top + 40} M${ex},${R.FAR + D - 20} L${ex},${top + 40}" stroke="${C.rust}" stroke-width="14"/>` +
      `<rect x="${ex - 280}" y="${top}" width="560" height="400" fill="#FBF6E6" stroke="${C.line}" stroke-width="7"/>` +
      `<path d="M${ex},${top} V${top + 400} M${ex - 280},${top + 70} H${ex + 280}" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M${ex - 280},${top + 140} H${ex + 280} M${ex - 280},${top + 210} H${ex + 280} M${ex - 280},${top + 280} H${ex + 280} M${ex - 280},${top + 350} H${ex + 280}" stroke="${C.line}" stroke-width="2" opacity="0.4"/>` +
      H.label(ex - 140, top + 48, 30, "CLIMATE DEATH") + H.label(ex + 140, top + 48, 30, "MILITARY DEATH") +
      `<path d="M${ex - 200},${top + 110} v24 M${ex - 186},${top + 110} v24 M${ex + 180},${top + 110} v24" stroke="${C.war}" stroke-width="5"/>`;
    // the skeleton in halves: the top half (skull, ribs, arms) and the legs, each held up against its column
    const bones = K.person(copy(YOU, { skeleton: true, hat: null }));
    const half = (id, y0, y1) => `<defs><clipPath id="${fid}-${id}"><rect x="-80" y="${y0}" width="160" height="${y1 - y0}"/></clipPath></defs><g clip-path="url(#${fid}-${id})">${bones}</g>`;
    // each survivor holds his half up by the cut end, against his own column
    const s1 = copy({ tone: 1, outfit: "overalls", color: 3, seed: 2 }, { charred: true, look: "right", arms: [[-6, -2], [120, 168]] });
    const s2 = copy({ tone: 3, outfit: "shirt", kind: "twig", seed: 5 }, { charred: true, look: "left", arms: [[-120, -168], [6, 2]] });
    const p1x = ex - 330, p2x = ex + 330, pf = R.FEET + D;
    const h1 = handAt(H, s1, p1x, pf, R.K, 1), h2 = handAt(H, s2, p2x, pf, R.K, 0);
    const topHalf = `<g transform="translate(${f(h1[0])},${f(h1[1] - 6)}) rotate(-10) scale(1.5) translate(0,-20)">${half("t", -120, 22)}</g>`;
    const legs = `<g transform="translate(${f(h2[0])},${f(h2[1] - 4)}) rotate(14) scale(1.5) translate(0,-24)">${half("b", 22, 110)}</g>`;
    const c1 = toCanvas(K.rig(s1).top, p1x, pf, R.K), c2 = toCanvas(K.rig(s2).top, p2x, pf, R.K);
    const people = man(H, s1, p1x, pf, R.K) + man(H, s2, p2x, pf, R.K) + wisps(c1[0] - 20, c1[1] - 40, 3, 1.2) + wisps(c2[0] - 20, c2[1] - 40, 3, 1.2);
    const bowler = `<g transform="translate(${ex + 760},${R.FEET + D - 10}) rotate(30)"><path d="M-30,0 H30 M-20,0 Q-20,-30 0,-30 Q20,-30 20,0" fill="${C.line}" stroke="${C.line}" stroke-width="6"/></g>` +
      `<path d="M${ex + 680},${R.FEET + D - 4} h40 M${ex + 650},${R.FEET + D - 14} h30" stroke="${C.cream}" stroke-width="3" opacity="0.6"/>`;
    const svg = sky(SKY.a2043) + view(cx, R.FEET + D - 300, 0.95, plate + easel + people + topHalf + legs + bowler);
    return { svg, alt: "On the dark valley floor under a slate sky, a mushroom cloud on the horizon: two charred, smoking survivors stand either side of a big spreadsheet on an easel with the columns CLIMATE DEATH and MILITARY DEATH, each holding up his half of YOU's skeleton against his own column, while the bowler rolls away down the cracked road." };
  },

  "cockroach-manual"(H, fid) {
    const { K, C } = H, R = ROADS, A = R.A, D = R.DROP, ink = C.line;
    // on "confused.": the cockroach in tiny glasses and YOU's bowler holding the manual upside down on the rubble
    const cx = A.roach + 100;
    let rubble = "";
    for (let i = 0; i < 14; i++) {
      const x = cx - 900 + i * 140 + ((i * 53) % 40), h = 30 + ((i * 37) % 50), r = ((i * 29) % 40) - 20;
      rubble += `<path d="M${x - 50},${R.FAR + D + 40} L${x - 30},${R.FAR + D + 40 - h} L${x + 34},${R.FAR + D + 30 - h} L${x + 52},${R.FAR + D + 40} Z" fill="${i % 3 ? "#5A5560" : "#6E6668"}" stroke="${ink}" stroke-width="4" transform="rotate(${r} ${x} ${R.FAR + D + 40})"/>`;
    }
    const posts = milestone(K, A.m2045, "2045", D + 30, -14) + milestone(K, A.m2050, "2050", D + 30, 10);
    // the cockroach: standing up on its hind legs, about a person's height at this scale
    const rx = A.roach, ry = R.FEET + D;
    const leg = (x0, y0, dx, dy) => `<path d="M${x0},${y0} l${dx},${dy * 0.5} l${dx * 0.4},${dy}" fill="none" stroke="${ink}" stroke-width="9" stroke-linejoin="miter"/><path d="M${x0},${y0} l${dx},${dy * 0.5} l${dx * 0.4},${dy}" fill="none" stroke="#5A2A18" stroke-width="5"/>`;
    const roach = `<g transform="translate(${rx},${ry})">` +
      leg(-22, -110, -40, 60) + leg(22, -110, 40, 60) +
      `<path d="M-50,-90 Q-70,-210 0,-250 Q70,-210 50,-90 Q30,-40 0,-30 Q-30,-40 -50,-90 Z" fill="#7A3B22" stroke="${ink}" stroke-width="7"/>` +
      `<path d="M0,-240 V-40" stroke="${ink}" stroke-width="4"/><path d="M-36,-200 Q-30,-140 -40,-90 M36,-200 Q30,-140 40,-90" fill="none" stroke="#A85A34" stroke-width="5"/>` +
      `<path d="M-10,-36 L-26,0 M10,-36 L26,0" stroke="${ink}" stroke-width="9" stroke-linecap="round"/>` +
      `<ellipse cx="0" cy="-290" rx="52" ry="46" fill="#5A2A18" stroke="${ink}" stroke-width="7"/>` +
      `<path d="M-20,-330 Q-60,-420 -110,-430 M20,-330 Q60,-420 110,-440" fill="none" stroke="${ink}" stroke-width="5"/>` +
      `<circle cx="-18" cy="-292" r="16" fill="#FBF6E6" stroke="${ink}" stroke-width="5"/><circle cx="20" cy="-292" r="16" fill="#FBF6E6" stroke="${ink}" stroke-width="5"/><path d="M-2,-292 H4" stroke="${ink}" stroke-width="4"/>` +
      `<circle cx="-14" cy="-288" r="6" fill="${ink}"/><circle cx="24" cy="-288" r="6" fill="${ink}"/>` +
      `<path d="M-14,-262 q14,-8 28,0" fill="none" stroke="#F3D0A0" stroke-width="4"/>` +
      `<g transform="translate(0,-326)"><path d="M-62,0 H62" stroke="${ink}" stroke-width="12" stroke-linecap="round"/><path d="M-40,0 Q-40,-56 0,-56 Q40,-56 40,0 Z" fill="${ink}"/></g>` +
      `<g transform="translate(-4,-176) rotate(180) scale(1.2)">${K.props.manual({})}</g>` +
      leg(-40, -150, -26, 30).replace("l-26,15", "l-26,15") + leg(40, -150, 26, 30) +
      `</g>`;
    const plate = road(cx - 1300, cx + 1300, D, "#5E5448", "#8F877A") + crack(C, cx - 300, D) + crack(C, cx + 400, D) + posts + rubble + roach;
    const svg = sky(SKY.a2045) + view(cx, ry - 260, 1.0, plate);
    return { svg, alt: "On the rubble of the last stretch of road A under a navy sky, the 2045 and 2050 milestones leaning out of it, a cockroach stands up on its hind legs in tiny glasses and YOU's bowler, holding the orange manual upside down." };
  },

  "future-b-2028"(H, fid) {
    const { K, C } = H, R = ROADS, B = R.B, ink = C.line;
    // after "typo.": the Rich Human on his hill of papers, mid-yawn, spiking his "+272%" statement onto the desk spike
    // beside him, already thick with "+272%" statements
    const cx = B.fatcat + 40, hx = B.fatcat - 60, G = R.FAR;
    let hill = `<path d="M${hx - 380},${G} Q${hx - 200},${G - 300} ${hx},${G - 330} Q${hx + 220},${G - 300} ${hx + 380},${G} Z" fill="${C.money}" stroke="${ink}" stroke-width="6"/>`;
    for (let i = 0; i < 26; i++) {
      const a = (i * 47) % 360, rr = (i * 31) % 100;
      const x = hx - 300 + ((i * 97) % 600), yTop = G - 300 * Math.max(0, 1 - ((x - hx) / 380) ** 2) + 10;
      hill += flatBill(K, "plain", x, yTop + 40 + (rr % 3) * 30, 0.6, (a % 50) - 25);
    }
    // standing on the hilltop, bored stiff: a long yawn, his statement held up over the desk spike beside him
    const fk = 2.0, fx = hx - 60, ff = G - 316;
    const fat = K.castOpts("richHuman", { mood: "flat", mouth: "o", look: "right", hold: null, cigar: false, arms: [[-10, -30], [150, 170]] });
    const cat = man(H, fat, fx, ff, fk);
    const fh = handAt(H, fat, fx, ff, fk, 1);
    // a statement: a cream sheet with "+272%" on it, around (0, 0)
    const stmt = (x, y, r, k = 1) => `<g transform="translate(${f(x)},${f(y)}) rotate(${r}) scale(${k})"><rect x="-60" y="-34" width="120" height="68" fill="#FBF6E6" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M-44,-18 h50 M-44,22 h70" stroke="${C.tan}" stroke-width="4"/>` + H.label(0, 12, 26, "+272%", "middle", ink) + `</g>`;
    const held = stmt(fh[0] + 36, fh[1] - 30, -8, 1.15);
    // the desk spike stuck in the hilltop, its nail through a thick stack of the same statements
    const kx = hx + 250, ky = G - 300 * (1 - (250 / 380) ** 2) + 18;
    let spike = `<path d="M${kx},${ky - 30} V${ky - 300}" stroke="${ink}" stroke-width="9" stroke-linecap="round"/><path d="M${kx},${ky - 30} V${ky - 300}" stroke="#C9CED6" stroke-width="4" stroke-linecap="round"/>`;
    for (let i = 0; i < 9; i++) spike += stmt(kx + ((i * 37) % 13) - 6, ky - 46 - i * 22, ((i * 53) % 17) - 8, 0.9);
    spike += `<path d="M${kx - 56},${ky} h112 v-26 h-112 Z" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>`;
    // the yawn: his mouth dropped wide open under the walrus mustache, a rust tongue at the bottom
    const fm = toCanvas(K.rig(fat).mouth, fx, ff, fk), mx = fm[0] + 2 * fk, my = fm[1] + 9 * fk;
    const yawn = `<ellipse cx="${f(mx)}" cy="${f(my)}" rx="${f(6 * fk)}" ry="${f(9 * fk)}" fill="#1A1420" stroke="${ink}" stroke-width="3"/>` +
      `<path d="M${f(mx - 4 * fk)},${f(my + 6 * fk)} q${f(4 * fk)},${f(-4 * fk)} ${f(8 * fk)},0" fill="${C.rust}" stroke="none"/>`;
    const sun = `<circle cx="${cx + 820}" cy="${R.HZ - 30}" r="120" fill="${C.yellow}" stroke="${ink}" stroke-width="5"/>`;
    const funnel = H.at(B.funnel, G, 1.4, K.props.colorFlipFunnel({ inN: 2, outN: 3 }));
    const plate = sun + road(cx - 1400, cx + 1400) + funnel + hill + spike + cat + held + yawn;
    const svg = sky(SKY.b2028) + view(cx, -260, 0.92, plate);
    return { svg, alt: "On road B under a pale teal sky with a low mustard sun, the fat cat stands on his hill of green papers in the middle of a long yawn, holding up his +272% statement over the desk spike stuck in the hilltop beside him, its nail already thick with +272% statements; the color-flip funnel stands in the road behind." };
  },

  "future-b-2032"(H, fid) {
    const { K, C } = H, R = ROADS, B = R.B, ink = C.line;
    // on "moving.": the wait sign on NOW over the ticket window, YOU at the front with his bottle, the queue shuffling
    const cx = B.window - 520, G = R.FAR, wx = B.window;
    const wall = `<rect x="${wx - 150}" y="${G - 620}" width="1100" height="620" fill="#D8CBA6" stroke="${ink}" stroke-width="6"/>` +
      `<rect x="${wx - 90}" y="${G - 330}" width="200" height="160" fill="${C.slate}" stroke="${ink}" stroke-width="7"/><rect x="${wx - 110}" y="${G - 170}" width="240" height="26" fill="${C.tan}" stroke="${ink}" stroke-width="5"/>`;
    const signB = `<g transform="translate(${wx + 10},${G - 470})"><rect x="-220" y="-90" width="440" height="160" fill="#FBF6E6" stroke="${ink}" stroke-width="7"/>` +
      H.label(0, -42, 34, "WAIT TIME FROM HERE:", "middle", ink) + `<rect x="-150" y="-20" width="300" height="74" fill="#1E1B24" stroke="${ink}" stroke-width="4"/>` +
      `<text x="0" y="40" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="64" fill="${C.yellow}">NOW</text></g>`;
    const pipe = `<path d="M${wx + 130},${G - 250} H${wx + 300} V${G - 120} H${B.lab - 60}" fill="none" stroke="${ink}" stroke-width="30"/><path d="M${wx + 130},${G - 250} H${wx + 300} V${G - 120} H${B.lab - 60}" fill="none" stroke="${C.med}" stroke-width="20"/>`;
    const lab = H.at(B.lab + 80, G, 1.1, K.props.lab({}));
    const ropes = [];
    for (let i = 0; i < 8; i++) ropes.push(wx - 260 - i * 230);
    const rope = ropes.map((x) => `<path d="M${x},${R.NEAR + 20} V${R.NEAR - 80}" stroke="${C.yellow}" stroke-width="8"/><circle cx="${x}" cy="${R.NEAR - 84}" r="9" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/>`).join("") +
      `<path d="${ropes.map((x, i) => (i ? "Q" + (x + 115) + "," + (R.NEAR - 40) + " " : "M") + x + "," + (R.NEAR - 80)).join(" ")}" fill="none" stroke="${C.war}" stroke-width="6"/>`;
    const youO = copy(YOU, { look: "right", mood: "smile", arms: [[-6, -2], [70, -30]] });
    const yh = handAt(H, youO, wx - 230, R.FEET, R.K, 1);
    const you = man(H, youO, wx - 230, R.FEET, R.K) + H.at(f(yh[0] + 4), f(yh[1] + 40), 0.9, K.props.pillBottle({}));
    const sk = copy(YOU, { skeleton: true, hat: null, look: "right", arms: [[-6, -2], [40, 60]] });
    const people = man(H, sk, wx - 470, R.FEET, R.K, leashed(H, K.rig(sk).hand[1], 44, 0.3, { seed: 40, color: "orange", mood: "grin" })) +
      [[{ tone: 0, outfit: "shirt", color: 2, seed: 21 }, wx - 700], [{ tone: 3, outfit: "dress", hair: 1, color: 0, seed: 22 }, wx - 920], [{ tone: 1, outfit: "suit", color: 3, seed: 23 }, wx - 1140], [{ tone: 2, outfit: "overalls", color: 1, seed: 24 }, wx - 1360]].map(([o, x], i) => {
        const p = copy(o, { look: "right", arms: [[-6, -2], [40, 60]] });
        return man(H, p, x, R.FEET, R.K, leashed(H, K.rig(p).hand[1], 44, 0.3, { seed: 41 + i, color: ["peri", "cyan", "yellow", "rust"][i] }));
      }).join("");
    const shuffle = [wx - 760, wx - 980, wx - 1200].map((x) => `<path d="M${x - 50},${R.FEET - 20} h-30 M${x - 54},${R.FEET - 40} h-22" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`).join("");
    const plate = road(cx - 1300, cx + 1300) + wall + signB + pipe + lab + rope + people + you + shuffle;
    const svg = sky(SKY.b2032) + view(cx, -260, 0.92, plate);
    return { svg, alt: "On road B the ticket window from Part 9, its wait sign reading WAIT TIME FROM HERE: NOW, a teal pipe running into it from a lab; YOU at the front of the roped queue holds his new pill bottle and smiles, a skeleton behind him with its disease on a leash, and the line of humans walking their diseases shuffles forward out of the frame." };
  },

  "future-b-2035"(H, fid) {
    const { K, C } = H, R = ROADS, B = R.B, ink = C.line;
    // after "produced.": the long conveyor out of the factory's side door, loaded with goods, YOU riding on top of them
    const cx = B.factory + 560, G = R.FAR, fx = B.factory;
    const factory = H.at(fx, G, 1.5, K.props.factory({ label: "", smoke: false }));
    const rings = [-111, 0, 111].map((dx, i) => [0, 1, 2].map((j) => `<ellipse cx="${f(fx + dx * 1.5 + j * 20)}" cy="${f(G - 520 - j * 60 - i * 10)}" rx="${26 + j * 8}" ry="${12 + j * 3}" fill="none" stroke="${ink}" stroke-width="11"/><ellipse cx="${f(fx + dx * 1.5 + j * 20)}" cy="${f(G - 520 - j * 60 - i * 10)}" rx="${26 + j * 8}" ry="${12 + j * 3}" fill="none" stroke="${C.med}" stroke-width="6"/>`).join("")).join("");
    // the belt: 760 long at scale 1.5, its left end at the side door (fx + 265), its top at G - 99, running on right
    const CW = 760, belt = G - 66 * 1.5, cl = fx + 265, cr = cl + CW * 1.5;
    const conv = H.at(f((cl + cr) / 2), G, 1.5, K.props.conveyor({ w: CW }));
    const loaf = (x, y, r = 0, s = 1) => `<g transform="translate(${f(x)},${f(y)}) rotate(${r}) scale(${s})"><path d="M-30,6 Q-32,-14 -10,-16 Q8,-20 24,-12 Q34,-4 30,8 Q0,14 -30,6 Z" fill="#D49A4E" stroke="${ink}" stroke-width="3.2"/><path d="M-16,-8 l8,-6 M-2,-9 l8,-6 M12,-8 l8,-6" stroke="#F3DFB0" stroke-width="3"/></g>`;
    const shoe = (x, y, r = 0) => `<g transform="translate(${f(x)},${f(y)}) rotate(${r})"><path d="M-30,6 V-14 Q-14,-18 -4,-8 L24,-2 Q34,2 32,8 Z" fill="${C.rust}" stroke="${ink}" stroke-width="3.5"/></g>`;
    const toaster = (x, y, r = 0) => `<g transform="translate(${f(x)},${f(y)}) rotate(${r})"><rect x="-30" y="-40" width="60" height="44" rx="10" fill="#C9CED6" stroke="${ink}" stroke-width="4"/><path d="M-16,-40 v-8 h10 v8 M6,-40 v-8 h10 v8" fill="#E9C07A" stroke="${ink}" stroke-width="3"/></g>`;
    // the load: a low mound of goods riding the belt (from mx0 to mx1, mh high), and loose goods coming out of the door
    const mx0 = cl + 300, mx1 = cr - 120, mm = (mx0 + mx1) / 2, mh = 150;
    let load = `<path d="M${mx0},${belt} Q${f(mm)},${belt - 2 * mh} ${mx1},${belt} Z" fill="#B99A68" stroke="${ink}" stroke-width="6"/>`;
    const items = [];
    for (let i = 0; i < 26; i++) {
      const u = ((i * 61) % 100) / 100, x = mx0 + 30 + u * (mx1 - mx0 - 60), top = belt - mh * (1 - ((x - mm) / ((mx1 - mx0) / 2)) ** 2);
      items.push([i % 4, x, top + 14 + ((i * 23) % 70), ((i * 37) % 60) - 30]);
    }
    load += items.map(([kd, x, y, r]) => kd === 0 ? loaf(x, y, r) : kd === 1 ? shoe(x, y, r) : kd === 2 ? toaster(x, y, r) : H.at(f(x), f(y + 30), 0.6, K.props.pillBottle({}), r)).join("");
    // YOU sitting on top of the load, facing the way it rides, leaning back on a loaf like a pillow, grinning
    const youO = copy(YOU, { mood: "grin", arms: [[40, 20], [-60, -100]], build: { legPose: [[86, 4], [94, 8]] } });
    // sitting, his hips are about 40 person units above his feet: put the hips on the top of the load
    const yx = mm + 10, yk = 1.5, seat = belt - mh + 8;
    const you = loaf(yx - 70, seat - 40, -70, 1.6) + man(H, youO, yx, seat + 40 * yk, yk, "", -10);
    const onBelt = loaf(cl + 120, belt - 14, 0) + toaster(cl + 220, belt - 4) + shoe(mx1 + 60, belt - 6);
    const plate = `<circle cx="${cx + 600}" cy="${R.HZ - 330}" r="120" fill="${C.yellow}" stroke="${ink}" stroke-width="5"/>` + road(cx - 1400, cx + 1400) +
      factory + rings + conv + onBelt + load + you;
    const svg = sky(SKY.b2035) + view(cx, -300, 0.8, plate);
    return { svg, alt: "On road B under a brighter teal sky, the war factory's three missile chimneys puff teal smoke rings; a long conveyor out of its side door runs on along the road, loaded with a mound of loaves, shoes, toasters and pill bottles, and YOU rides along on top of it, leaning back on a loaf like a pillow, grinning." };
  },

  "retrospect-look"(H, fid) {
    const S = H.K.STUDIO;
    // on "retrospect.": the reaction cut: hands on hips, a long skeptical look at the camera, the camera pushing in
    const svg = push(S, 1.08, H.host("skeptical-closed", "hands-hips", lecternProps(H)));
    return { svg, alt: "A reaction cut to the lectern: Wishonia, hands on hips, gives the camera a long skeptical look." };
  },

  "future-b-2040"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "variable.": the little loop road hovering over its own shadow like a flying saucer, YOU and the dog on it
    const HZN = 440, cx = 960, cy = 520, rx = 560, ry = 150;
    const ground = `<rect y="${HZN}" width="1920" height="700" fill="${GROUND}"/><path d="M0,${HZN} H1920" stroke="${DUST}" stroke-width="3" opacity="0.6"/>` +
      `<rect y="840" width="1920" height="100" fill="${ROAD}"/><path d="M0,840 H1920 M0,940 H1920" stroke="${EDGE}" stroke-width="6"/>`;
    const shadow = `<ellipse cx="${cx}" cy="830" rx="${rx * 0.9}" ry="${ry * 0.45}" fill="#9E8A5C" opacity="0.55"/>`;
    const disc = `<ellipse cx="${cx}" cy="${cy + 40}" rx="${rx + 40}" ry="${ry + 40}" fill="${C.slate}" stroke="${ink}" stroke-width="7"/>` +
      `<ellipse cx="${cx}" cy="${cy + 20}" rx="${rx + 40}" ry="${ry + 40}" fill="${GROUND}" stroke="${ink}" stroke-width="6"/>` +
      `<ellipse cx="${cx}" cy="${cy + 20}" rx="${rx - 30}" ry="${ry - 10}" fill="none" stroke="${EDGE}" stroke-width="86"/>` +
      `<ellipse cx="${cx}" cy="${cy + 20}" rx="${rx - 30}" ry="${ry - 10}" fill="none" stroke="${ROAD}" stroke-width="74"/>` +
      `<ellipse cx="${cx}" cy="${cy + 20}" rx="${rx - 30}" ry="${ry - 10}" fill="none" stroke="${DASH}" stroke-width="5" stroke-dasharray="30 34"/>`;
    const lights = [];
    for (let i = 0; i < 12; i++) { const a = (i / 12) * Math.PI; lights.push(`<circle cx="${f(cx + (rx + 30) * Math.cos(a))}" cy="${f(cy + 40 + (ry + 30) * Math.sin(a) * 0.95)}" r="10" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/>`); }
    const motion = [[-1, 0], [1, 0]].map(([s]) => `<path d="M${cx + s * (rx + 90)},${cy - 30} q${s * 40},20 ${s * 60},60 M${cx + s * (rx + 110)},${cy + 40} q${s * 40},20 ${s * 50},60" fill="none" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`).join("");
    // the stops on the loop: the workbench, the pay window, the farm stand, the lab, the knocked-out disease
    const bench = `<g transform="translate(${cx - 430},${cy - 40})"><rect x="-60" y="-40" width="120" height="16" fill="${C.tan}" stroke="${ink}" stroke-width="4"/><path d="M-50,-24 V20 M50,-24 V20" stroke="${ink}" stroke-width="7"/></g>`;
    const pay = `<g transform="translate(${cx - 180},${cy - 60})"><rect x="-50" y="-100" width="100" height="100" fill="${C.yellow}" stroke="${ink}" stroke-width="5"/><path d="M-60,-100 L0,-130 L60,-100 Z" fill="${C.rust}" stroke="${ink}" stroke-width="5"/><rect x="-32" y="-80" width="64" height="40" fill="${C.navy}"/></g>`;
    const stand = `<g transform="translate(${cx + 140},${cy - 60})"><path d="M-60,-110 H60 L70,-84 H-70 Z" fill="${C.cream}" stroke="${ink}" stroke-width="5"/><path d="M-40,-110 L-46,-84 M0,-110 V-84 M40,-110 L46,-84" stroke="${C.rust}" stroke-width="12"/><path d="M-56,-84 V0 M56,-84 V0" stroke="${ink}" stroke-width="6"/><rect x="-62" y="-40" width="124" height="40" fill="#B98A55" stroke="${ink}" stroke-width="5"/></g>`;
    const lab = H.at(cx + 420, cy - 30, 0.7, K.props.lab({}));
    const blob = H.at(cx + 330, cy + 150, 0.6, K.props.diseaseBlob({ mood: "dead" }));
    const dog = H.at(cx, cy + 40, 0.9, K.props.democracyDog({ tail: "pills", mood: "eager" }));
    const you = man(H, copy(YOU, { look: "left", mood: "grin", arms: [[40, 100], [-40, -110]] }), cx - 160, cy + 130, 1.15, "", -8) +
      `<path d="M${cx - 60},${cy + 20} h50 M${cx - 56},${cy + 50} h40 M${cx - 60},${cy + 80} h30" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/>`;
    const sci = man(H, K.castOpts("scientist", {}), cx + 300, cy + 30, 0.95);
    const svg = sky(SKY.b2040) + `<circle cx="1600" cy="180" r="100" fill="${C.yellow}" stroke="${ink}" stroke-width="5"/>` + ground + shadow + disc + bench + pay + stand + lab + blob + sci + dog + you + lights.join("") + motion +
      H.at(260, 840, 1.3, K.props.sign({ text: "2040", posts: 1, fontSize: 40, height: 64 }));
    return { svg, alt: "Beside road B under a teal sky, the little loop road has lifted off the ground and hovers over its own shadow like a flying saucer, lights round its rim; on it ride the workbench, the yellow pay window, the striped farm stand, the Scientist at her lab bench and a knocked-out disease, and YOU runs round it while the Democracy Dog chases its tail of teal pills in the middle." };
  },

  "future-b-2048"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "subject.": through the picture window: YOU in top hat and monocle points out of the window while his other
    // hand throws the tablecloth over the missile lamp; the child looks out
    const wall = `<rect width="1920" height="1080" fill="#9FC7C2"/>` + `<rect x="120" y="70" width="1680" height="860" fill="#F1D9A6" stroke="${ink}" stroke-width="16"/>` +
      `<path d="M960,70 V930" stroke="${ink}" stroke-width="10"/><path d="M128,78 H1792" stroke="${C.cream}" stroke-width="6" opacity="0.6"/>`;
    const room = `<rect x="128" y="740" width="1664" height="182" fill="#C98F55"/><path d="M128,740 H1792" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M128,300 H1792" stroke="${C.orange}" stroke-width="5" opacity="0.5"/>`;
    const table = `<path d="M560,640 H1180 L1210,700 H530 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="6"/><path d="M600,700 V900 M1140,700 V900" stroke="${ink}" stroke-width="14"/>` +
      `<path d="M600,700 V900 M1140,700 V900" stroke="${C.tan}" stroke-width="7"/>`;
    const lampX = 1470;
    const lamp = H.at(lampX, 900, 2.2, K.props.missile({ mood: "smug", arms: "none" })) +
      `<path d="M${lampX - 70},${900 - 352} L${lampX + 70},${900 - 352} L${lampX + 100},${900 - 252} L${lampX - 100},${900 - 252} Z" fill="${C.cream}" stroke="${ink}" stroke-width="6"/>`;
    const cloth = `<path d="M1220,520 Q1360,380 1600,430 Q1640,560 1590,700 Q1480,620 1360,690 Q1300,560 1220,520 Z" fill="#E8D7B0" stroke="${ink}" stroke-width="6"/>` +
      `<path d="M1260,520 l300,-60 M1280,580 l300,-60 M1300,640 l260,-50" stroke="${C.war}" stroke-width="10" opacity="0.7"/>`;
    const youO = copy(YOU, { hat: "top", prop: "monocle", mood: "smile", look: "left", arms: [[-110, -100], [110, 70]] });
    const you = man(H, youO, 1060, 900, 2.6);
    const kid = man(H, { tone: 2, outfit: "shirt", kind: "shirt", head: "plain", hairStyle: "short", hat: null, glasses: false, color: 1, look: "left", mood: "eager", build: { hs: 1.3, legs: 0.7, th: 0.8, tw: 0.8 }, arms: [[-6, -2], [10, 4]] }, 660, 900, 1.8);
    const curtains = `<path d="M128,78 H260 Q220,400 300,926 H128 Z" fill="${C.rust}" stroke="${ink}" stroke-width="5"/><path d="M1792,78 H1700 Q1740,400 1690,926 H1792 Z" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>`;
    const sill = `<rect x="90" y="926" width="1740" height="36" fill="${C.cream}" stroke="${ink}" stroke-width="6"/>`;
    const svg = wall + room + curtains + table + lamp + cloth + you + kid + sill +
      `<rect x="840" y="600" width="60" height="44" rx="6" fill="${C.cream}" stroke="${ink}" stroke-width="4"/>`;
    return { svg, alt: "Through the picture window of YOU's house: YOU in a top hat and monocle at the kitchen table points away out of the window, and the child turns to look, while YOU's other hand throws the tablecloth over a lamp made from a grinning retired missile in the corner." };
  },

  "fax-machine-lifetime"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "TERRIBLE": the stamp lifting off the globe, SUBOPTIMAL on it, the old man a skeleton on his cane, the pigeon
    const G = 880, HZN = 520;
    const globe = H.at(900, G, 2.6, K.props.earthGlobe({ r: 130 }));
    const mark = `<g transform="translate(900,${G - 300})">${K.props.stampMark({ text: "SUBOPTIMAL", color: C.war, angle: -10, fontSize: 64 })}</g>`;
    // the stamp lifting away up and to the right, tilted, the motion ticks under it
    const stamp = H.at(1330, 250, 2.1, K.props.stamp({ text: "", color: C.war }), 22) +
      `<path d="M1180,360 l-30,24 M1230,390 l-22,30 M1290,404 l-8,34" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`;
    // the old man's skeleton, stooped, leaning on his cane (his hand on its crook)
    const oldO = copy({ tone: 1, outfit: "suit", color: 2, seed: 31 }, { skeleton: true, look: "left", arms: [[-6, -2], [-30, -10]], build: { hunch: 16 } });
    const sk = 1.8, skx = 1500, ch = handAt(H, oldO, skx, G, sk, 1);
    const skel = man(H, oldO, skx, G, sk) +
      `<path d="M${f(ch[0])},${f(ch[1])} L${f(ch[0] - 14)},${G}" stroke="${ink}" stroke-width="14" stroke-linecap="round"/><path d="M${f(ch[0])},${f(ch[1])} L${f(ch[0] - 14)},${G}" stroke="${C.rust}" stroke-width="8" stroke-linecap="round"/>` +
      `<path d="M${f(ch[0] + 18)},${f(ch[1] + 8)} q-4,-22 -18,-8" fill="none" stroke="${C.rust}" stroke-width="8" stroke-linecap="round"/>`;
    const crib = `<g transform="translate(1720,${G})"><rect x="-90" y="-110" width="180" height="20" fill="${C.tan}" stroke="${ink}" stroke-width="4"/><rect x="-90" y="-40" width="180" height="20" fill="${C.tan}" stroke="${ink}" stroke-width="4"/>` +
      [-70, -35, 0, 35, 70].map((x) => `<path d="M${x},-110 V-20" stroke="${ink}" stroke-width="5"/>`).join("") + `<path d="M-90,-110 V0 M90,-110 V0" stroke="${ink}" stroke-width="8"/></g>`;
    const py = G - 2.6 * 260 - 4;
    const pigeon = `<g transform="translate(940,${py}) scale(1.6)"><path d="M-30,0 Q-34,-26 -6,-30 Q4,-46 20,-40 Q30,-36 30,-28 L40,-24 L30,-20 Q26,-4 10,0 Z" fill="#8E96A6" stroke="${ink}" stroke-width="3.5"/>` +
      `<path d="M-20,-14 Q0,-26 14,-10" fill="none" stroke="${ink}" stroke-width="3"/><circle cx="20" cy="-34" r="3" fill="${ink}"/><path d="M-30,-8 L-48,-14 L-40,0 Z" fill="#6E7686" stroke="${ink}" stroke-width="3"/>` +
      `<path d="M0,0 v8 M10,0 v8" stroke="${C.orange}" stroke-width="3"/><g transform="translate(46,-22) rotate(-10)"><rect x="-4" y="-5" width="28" height="10" rx="5" fill="#FBF6E6" stroke="${ink}" stroke-width="2.5"/></g></g>`;
    const svg = sky("#EFE3C4") + `<rect y="${HZN}" width="1920" height="700" fill="${GROUND}"/><path d="M0,${HZN} H1920" stroke="${DUST}" stroke-width="3" opacity="0.6"/>` +
      globe + mark + pigeon + stamp + skel + crib;
    return { svg, alt: "On a plain field a big engraved globe, the red tint gone, stamped SUBOPTIMAL in red as the rubber stamp lifts off above it; a carrier pigeon with a rolled message in its beak stands on top; beside it the old man is a grinning skeleton leaning on his cane, and the empty crib stands at the edge." };
  },

  "dont-know-what-to-tell-you"(H, fid) {
    const { K, C } = H, S = K.STUDIO;
    // on "tell": the shrug, the mug down, the YES console with its paper on top, the busy humans walking past it
    // the console on the free wall right of the lectern; the busy humans walk past it right to left behind it
    const bx = 1230, k = 2.0, top = 1066 - 104 * k;
    const console = H.at(bx, 1066, k, K.props.yesButton({ label: "YES" }));
    const paper = flatBill(K, "med", bx + 4, top - 14, 1.1, -6);
    const walkers = [
      [{ tone: 0, outfit: "suit", color: 3, seed: 41 }, 1590],
      [{ tone: 3, outfit: "dress", hair: 1, color: 2, seed: 42 }, 1730],
    ].map(([o, x]) => man(H, copy(o, { look: "left", arms: WATCH_ARMS }), x, 1060, 2.1)).join("");
    // the one who walked into it, bounced back a step and tipping his hat to it
    const bounceO = copy({ tone: 1, outfit: "suit", color: 0, seed: 43 }, { look: "left", mood: "worried", hat: "fedora", arms: [[-6, -2], [150, 170]] });
    const bouncer = man(H, bounceO, 1440, 1060, 2.1, "", 8) +
      `<path d="M1360,820 l-26,-10 M1364,856 l-30,0 M1360,892 l-26,10" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/>`;
    const you = man(H, copy(YOU, { look: "left", arms: WATCH_ARMS }), 1870, 1060, 2.1);
    const svg = push(S, 1.03, H.host("eyeroll-closed", "shrug", walkers + you + bouncer + console + paper + lecternProps(H)));
    return { svg, alt: "Wishonia shrugs at her lectern, her mug back down; beside her stands the YES button on its console with a green medicine paper lying on top, and busy humans walk past it checking their wristwatches, one bouncing back off it." };
  },
};
