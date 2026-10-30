// Part 1, locked to the camera-plates staging. Every Layer B scene is one large plate (a cream sky over a khaki
// field, the kit's cast at full size, the period film on top), and the title is the period card with the ball and chain.
// The sheet tool does not load the props library, so this module loads it into the same KIT.
//   node tools/storyboard-sheet.mjs storyboards/part-01-genetic-slavery.md
import { readFileSync } from "node:fs";
import vm from "node:vm";

// The sheet tool runs kit.js only; the props library (KIT.props) is loaded into the same KIT here.
const PROPS = ["objects-a.js", "objects-b.js", "places.js", "characters.js"];
function withProps(K) {
  if (!K.props || !K.props.__objects_a) {
    const doc = { getElementById: () => null, createElement: () => ({ style: {} }), head: { appendChild() {} } };
    for (const f of PROPS) vm.runInNewContext(readFileSync(new URL(`../assets/js/props/${f}`, import.meta.url), "utf8"), { window: { KIT: K }, document: doc });
  }
  return K;
}

const f1 = (n) => n.toFixed(1);
const SKY = "#EFE3C4", GROUND = "#C8B07B", HZ_LINE = "#8E7A55", SHADOW = "#9C8558";
const WHITE = "#FBF6E6";

// The period film (KIT.film, frozen on one frame): the warm wash, the vignette, two tiles of grain, a speck and a hair.
function film(id, seed) {
  let s = (seed * 977 + 5) >>> 0;
  const r = () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
  const tile = (pid, size, n, rmax, op) => {
    let dots = "";
    for (let i = 0; i < n; i++) dots += `<circle cx="${f1(r() * size)}" cy="${f1(r() * size)}" r="${f1(0.5 + r() * rmax)}" fill="${r() < 0.55 ? "#000" : "#FFF"}" opacity="${(op * (0.5 + r())).toFixed(3)}"/>`;
    return `<pattern id="${pid}" width="${size}" height="${size}" patternUnits="userSpaceOnUse">${dots}</pattern>`;
  };
  const sx = 300 + r() * 1300, hx = 200 + r() * 1500, hy = 120 + r() * 700;
  return `<defs>${tile(`${id}-ga`, 48, 46, 0.8, 0.16)}${tile(`${id}-gb`, 71, 22, 1.4, 0.09)}` +
    `<radialGradient id="${id}-vig" cx="50%" cy="48%" r="72%" gradientTransform="translate(0.5 0.48) scale(1 0.97) translate(-0.5 -0.48)"><stop offset="0.52" stop-color="#120A04" stop-opacity="0"/><stop offset="1" stop-color="#120A04" stop-opacity="0.42"/></radialGradient></defs>` +
    `<rect width="1920" height="1080" fill="#ECDCBA" opacity="0.1"/><rect width="1920" height="1080" fill="url(#${id}-vig)"/>` +
    `<rect width="1920" height="1080" fill="url(#${id}-ga)"/><rect width="1920" height="1080" fill="url(#${id}-gb)"/>` +
    `<circle cx="${f1(hx)}" cy="${f1(hy)}" r="2.6" fill="#1A120A" opacity="0.5"/>` +
    `<path d="M${f1(sx)},0 L${f1(sx + 14)},1080" stroke="#FFF6E2" stroke-width="1.4" opacity="0.16"/>`;
}

// ── Drawing helpers ──────────────────────────────────────────────────
const at = (x, y, k, inner, rot = 0) => `<g transform="translate(${f1(x)},${f1(y)})${rot ? ` rotate(${rot})` : ""}${k !== 1 ? ` scale(${k})` : ""}">${inner}</g>`;
// A person (feet at y 100 in person units) standing on groundY at x, k plate px per person unit.
const stand = (K, o, x, groundY, k) => at(x, groundY - 100 * k, k, K.person(o));
// A soft flat shadow under something standing on the ground.
const shadow = (x, y, rx, op = 0.35) => `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rx)}" ry="${f1(rx * 0.16)}" fill="${SHADOW}" opacity="${op}"/>`;
function field(horizon) {
  return `<rect width="1920" height="1080" fill="${GROUND}"/><rect width="1920" height="${horizon}" fill="${SKY}"/>` +
    `<path d="M0,${horizon} H1920" stroke="${HZ_LINE}" stroke-width="3" opacity="0.6"/>`;
}
// Fraunces Black: navy on a light plate, cream on a dark one, with the card's ink drop shadow.
function number(x, y, size, text, fill, shadowCol, anchor = "middle") {
  const a = `text-anchor="${anchor}" font-family="Fraunces" font-weight="900" font-size="${size}" letter-spacing="${size * 0.02}"`;
  return `<text x="${f1(x + size * 0.04)}" y="${f1(y + size * 0.053)}" ${a} fill="${shadowCol}">${text}</text><text x="${x}" y="${y}" ${a} fill="${fill}">${text}</text>`;
}
function label(x, y, size, text, fill, extra = "") {
  return `<text x="${x}" y="${y}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="${size}" letter-spacing="${size * 0.06}" fill="${fill}" ${extra}>${text}</text>`;
}
// A faceted stone: n corners on an ellipse, nudged by the seed.
function stone(cx, cy, rx, ry, seed, fill, ink) {
  let s = seed * 7919 + 17;
  const r = () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
  const n = 7 + Math.floor(r() * 3), pts = [];
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2 + r() * 0.3, k = 0.86 + r() * 0.2;
    pts.push([cx + rx * k * Math.cos(a), cy + ry * k * Math.sin(a) * (Math.sin(a) > 0 ? 0.8 : 1)]);
  }
  const d = "M" + pts.map((p) => `${f1(p[0])},${f1(p[1])}`).join(" L") + " Z";
  const hi = `M${f1(cx - rx * 0.5)},${f1(cy - ry * 0.35)} L${f1(cx - rx * 0.1)},${f1(cy - ry * 0.62)}`;
  return `<path d="${d}" fill="${fill}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/><path d="${hi}" stroke="#E4DDCB" stroke-width="5" stroke-linecap="round" opacity="0.7"/>`;
}
// A front-view face in the humans' style (almond eyes with heavy lids, thin angled brows) around (x, y), the point
// between the eyes; u scales it. mood: flat | smug | cross | sad | eager | sly; look: -1..1 (pupils left/right).
function face(x, y, u, mood, o = {}) {
  const ink = o.ink || "#112845", lc = o.line || ink, sp = 13 * u, rx = 8.5 * u, ry = 5.2 * u, look = (o.look || 0) * rx * 0.45;
  const top = { flat: -ry * 0.55, smug: -ry * 0.55, sly: -ry * 0.5, cross: -ry * 1.2, sad: -ry * 1.6, eager: -ry * 2.4 }[mood];
  const bot = { flat: ry * 1, smug: ry * 0.5, sly: ry * 0.45, cross: ry * 1.1, sad: ry * 1.1, eager: ry * 1.7 }[mood];
  let out = "";
  for (const s of [-1, 1]) {
    const ex = x + s * sp, d = `M${f1(ex - rx)},${f1(y)} Q${f1(ex)},${f1(y + top)} ${f1(ex + rx)},${f1(y - 0.4 * u)} Q${f1(ex)},${f1(y + bot)} ${f1(ex - rx)},${f1(y)} Z`;
    out += `<path d="${d}" fill="${WHITE}" stroke="${ink}" stroke-width="${f1(1.4 * u)}"/>` +
      `<circle cx="${f1(ex + look)}" cy="${f1(y + (top + bot) / 4)}" r="${f1(ry * (mood === "eager" ? 0.5 : 0.6))}" fill="${ink}"/>` +
      `<path d="M${f1(ex - rx - 0.8 * u)},${f1(y + 0.4 * u)} Q${f1(ex)},${f1(y + top - 0.8 * u)} ${f1(ex + rx + 0.6 * u)},${f1(y - 0.6 * u)}" fill="none" stroke="${ink}" stroke-width="${f1(2.6 * u)}" stroke-linecap="round"/>`;
    // brows: outer, middle, inner heights
    const b = { flat: [-11, -12, -11], smug: [-10, -12, -14], sly: [-14, -11, -8], cross: [-14, -11, -7], sad: [-8, -10, -13], eager: [-14, -17, -15] }[mood];
    const bw = rx + 2 * u, ox = ex + s * bw, ix = ex - s * bw * 0.9;
    out += `<path d="M${f1(ox)},${f1(y + b[0] * u)} L${f1(ex + s * bw * 0.1)},${f1(y + b[1] * u)} L${f1(ix)},${f1(y + b[2] * u)}" fill="none" stroke="${lc}" stroke-width="${f1(3 * u)}" stroke-linejoin="miter" stroke-linecap="round"/>`;
  }
  const my = y + (o.my || 17) * u, mw = (o.mw || 10) * u;
  const mouth = {
    flat: `M${f1(x - mw)},${f1(my)} L${f1(x + mw)},${f1(my - u)}`,
    smug: `M${f1(x - mw)},${f1(my + 1 * u)} Q${f1(x)},${f1(my + 3 * u)} ${f1(x + mw * 1.1)},${f1(my - 4 * u)}`,
    sly: `M${f1(x - mw * 1.2)},${f1(my - 3 * u)} Q${f1(x - mw * 0.2)},${f1(my + 6 * u)} ${f1(x + mw * 1.2)},${f1(my - 5 * u)}`,
    cross: `M${f1(x - mw)},${f1(my + 2 * u)} L${f1(x)},${f1(my - u)} L${f1(x + mw)},${f1(my + 2 * u)}`,
    sad: `M${f1(x - mw)},${f1(my + 3 * u)} Q${f1(x)},${f1(my - 4 * u)} ${f1(x + mw)},${f1(my + 3 * u)}`,
    eager: `M${f1(x - mw)},${f1(my - 2 * u)} L${f1(x + mw)},${f1(my - 2 * u)} L${f1(x + mw * 0.6)},${f1(my + 7 * u)} L${f1(x - mw * 0.6)},${f1(my + 7 * u)} Z`,
  }[mood];
  out += `<path d="${mouth}" fill="${mood === "eager" ? ink : "none"}" stroke="${lc}" stroke-width="${f1(2.8 * u)}" stroke-linecap="round" stroke-linejoin="round"/>`;
  if (mood === "sly" || mood === "smug") out += `<path d="M${f1(x + mw * 1.2)},${f1(my - 8 * u)} q${f1(4 * u)},${f1(3 * u)} ${f1(2 * u)},${f1(8 * u)}" fill="none" stroke="${lc}" stroke-width="${f1(1.8 * u)}" stroke-linecap="round"/>`;
  return out;
}

// ── Scenes ───────────────────────────────────────────────────────────

// The period card (KIT.titleScene, look "atomic"): the heading on plain navy under the film's emblem, an atom whose
// three electrons are war papers running round their orbits. Gag: a ball and chain cuffed to the Y, the chain a
// double helix.
function title(H, id) {
  const { C } = H, K = H.K, E = { at: [960, 300], rx: 200, ry: 62, k: 0.62 }, TILT = [0, 60, -60];
  const orbits = TILT.map((a) => `<ellipse cx="${E.at[0]}" cy="${E.at[1]}" rx="${E.rx}" ry="${E.ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${E.at[0]} ${E.at[1]})"/>`).join("");
  const t = 0.9;
  const bills = TILT.map((a, i) => {
    const th = i * 2.1 + t * 2.4, ex = E.rx * Math.cos(th), ey = E.ry * Math.sin(th), ar = (a * Math.PI) / 180;
    const x = E.at[0] + ex * Math.cos(ar) - ey * Math.sin(ar), y = E.at[1] + ex * Math.sin(ar) + ey * Math.cos(ar);
    return at(x, y - 6, E.k, K.money("war", i % 2));
  }).join("");
  const nucleus = `<circle cx="960" cy="300" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="951" cy="291" r="8" fill="${C.yellow}"/>`;
  // The heading: KIT.titleScene's atomic layout for two big lines (size 190.5, cap tops at 540 and 726.7).
  const S = 190.5, word = (y, text) => {
    const a = `x="960" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${S}"`;
    return `<text ${a} y="${f1(y + 0.053 * S)}" dx="${f1(0.04 * S)}" fill="${C.ink}" stroke="${C.ink}" stroke-width="${f1(0.044 * S)}" stroke-linejoin="round">${text}</text>` +
      `<text ${a} y="${f1(y)}" fill="${C.cream}" stroke="${C.cream}" stroke-width="${f1(0.044 * S)}" stroke-linejoin="round" paint-order="stroke">${text}</text>`;
  };
  // The ball and chain: a cuff round the Y's stem, a short double helix, an iron ball sitting on the baseline.
  const cuffX = 1339, cuffY = 836, ballX = 1622, ballY = 812, R = 58;
  let helix = "", rungs = "";
  const x0 = cuffX + 38, x1 = ballX - R + 6, n = 96;
  const pt = (u, s) => [x0 + (x1 - x0) * u, cuffY + 4 + (ballY + 10 - cuffY - 4) * u + 30 * Math.sin(u * Math.PI) + s * 20 * Math.sin(u * Math.PI * 5)];
  for (const s of [-1, 1]) helix += `<path d="M${Array.from({ length: n + 1 }, (_, i) => pt(i / n, s).map(f1).join(",")).join(" L")}" fill="none" stroke="${C.ink}" stroke-width="13" stroke-linecap="round"/>` +
    `<path d="M${Array.from({ length: n + 1 }, (_, i) => pt(i / n, s).map(f1).join(",")).join(" L")}" fill="none" stroke="${s < 0 ? C.peri : "#8FA2BF"}" stroke-width="7" stroke-linecap="round"/>`;
  for (let i = 1; i < 30; i++) {
    const u = i / 30, a = pt(u, -1), b = pt(u, 1);
    rungs += `<path d="M${f1(a[0])},${f1(a[1])} L${f1(b[0])},${f1(b[1])}" stroke="${C.ink}" stroke-width="10" stroke-linecap="round"/><path d="M${f1(a[0])},${f1(a[1])} L${f1(b[0])},${f1(b[1])}" stroke="${[C.orange, C.yellow, C.red, C.med][i % 4]}" stroke-width="5"/>`;
  }
  const ball = `<rect x="${cuffX - 40}" y="${cuffY - 18}" width="80" height="34" rx="7" fill="${C.peri}" stroke="${C.ink}" stroke-width="6"/><path d="M${cuffX - 30},${cuffY - 8} h60" stroke="#8FA2BF" stroke-width="4"/><circle cx="${cuffX + 42}" cy="${cuffY}" r="9" fill="none" stroke="${C.ink}" stroke-width="6"/>` +
    rungs + helix +
    `<circle cx="${ballX}" cy="${ballY}" r="${R}" fill="#4B5674" stroke="${C.ink}" stroke-width="7"/><path d="M${ballX + 20},${ballY + 50} A${R - 8},${R - 8} 0 0 0 ${ballX + 50},${ballY + 18}" fill="none" stroke="#2E3650" stroke-width="12" stroke-linecap="round"/><path d="M${ballX - 38},${ballY - 14} Q${ballX - 30},${ballY - 42} ${ballX - 4},${ballY - 48}" fill="none" stroke="${C.cream}" stroke-width="8" stroke-linecap="round" opacity="0.8"/>`;
  const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus + word(673, "GENETIC") + word(860, "SLAVERY") + ball + film(id, 11);
  return { svg, alt: "The period title card: GENETIC SLAVERY in cream on navy under the film's atom, its electrons three running war papers. A small iron ball is chained to the Y of SLAVERY; the chain is a twisted double helix." };
}

// six-oh-four: on the field, a tower of banded war-money bundles with the Weapons Maker grinning beside it, his baby
// missile in his arms; across the field the Scientist holds up her one medicine bill like a trophy. The brass plaque
// on the tower, POLITICAL PROBLEM, has a red X slammed through it.
function sixOhFour(H, id) {
  const { C } = H, K = withProps(H.K), ink = C.line, G = 870;
  const TX = 560, TW = 300, TOP = 262;
  let tower = "", s = 6047;
  const r = () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
  const bundles = 17, bh = (G - TOP) / bundles;
  for (let i = 0; i < bundles; i++) {
    const y = G - (i + 1) * bh, dx = (r() - 0.5) * 18, x = TX - TW / 2 + dx;
    let edges = "";
    for (let k = 1; k < 6; k++) edges += `<path d="M${f1(x + 4)},${f1(y + (k * bh) / 6)} H${f1(x + TW - 4)}" stroke="${C.moneyDark}" stroke-width="1.6" opacity="0.55"/>`;
    tower += `<rect x="${f1(x)}" y="${f1(y)}" width="${TW}" height="${f1(bh)}" fill="${C.money}" stroke="${ink}" stroke-width="3.4"/>` + edges +
      `<rect x="${f1(x + TW / 2 - 30)}" y="${f1(y - 1)}" width="60" height="${f1(bh + 2)}" fill="${C.cream}" stroke="${ink}" stroke-width="2.6"/>` +
      K.moneySeal("war", x + TW / 2, y + bh / 2, bh * 0.36);
  }
  // the plaque, bolted across the tower's middle, and the X through it
  const PY = 420, PW = 420, PH = 196;
  const screw = (x, y) => `<circle cx="${x}" cy="${y}" r="7" fill="${C.cream}" stroke="${ink}" stroke-width="2.6"/><path d="M${x - 4},${y - 4} l8,8" stroke="${ink}" stroke-width="2"/>`;
  const plaque = `<rect x="${TX - PW / 2 + 10}" y="${PY + 12}" width="${PW}" height="${PH}" fill="${ink}" opacity="0.35"/>` +
    `<rect x="${TX - PW / 2}" y="${PY}" width="${PW}" height="${PH}" rx="6" fill="${C.yellow}" stroke="${ink}" stroke-width="5"/>` +
    `<rect x="${TX - PW / 2 + 12}" y="${PY + 12}" width="${PW - 24}" height="${PH - 24}" rx="3" fill="none" stroke="${C.rust}" stroke-width="2.4"/>` +
    screw(TX - PW / 2 + 24, PY + 24) + screw(TX + PW / 2 - 24, PY + 24) + screw(TX - PW / 2 + 24, PY + PH - 24) + screw(TX + PW / 2 - 24, PY + PH - 24) +
    label(TX, PY + 88, 66, "POLITICAL", ink) + label(TX, PY + 164, 66, "PROBLEM", ink);
  const xd = `M${TX - PW / 2 + 6},${PY - 26} L${TX + PW / 2 - 6},${PY + PH + 26} M${TX + PW / 2 - 6},${PY - 26} L${TX - PW / 2 + 6},${PY + PH + 26}`;
  const X = `<g opacity="0.94"><path d="${xd}" stroke="${ink}" stroke-width="17" stroke-linecap="round"/><path d="${xd}" stroke="${C.war}" stroke-width="10" stroke-linecap="round"/>` +
    [[-236, -40, 7], [-226, 246, 5], [244, -36, 6], [232, 238, 8], [256, 226, 4], [-252, 226, 4]].map(([dx, dy, rr]) => `<circle cx="${TX + dx}" cy="${PY + dy}" r="${rr}" fill="${C.war}"/>`).join("") + "</g>";
  // the cast
  const WMK = 2.9, WMX = 960, SCK = 2.9, SCX = 1420;
  const wm = K.castOpts("weaponsMaker", { look: "left" });
  const sciO = K.castOpts("scientist", { look: "left", mood: "eager", arms: [[-12, -6], [150, 172]] });
  const sr = K.rig(sciO), hand = [SCX + SCK * sr.hand[1][0], G - 100 * SCK + SCK * sr.hand[1][1]];
  const medBill = at(hand[0] + 10, hand[1] - 46, 1.9, K.money("med", 0).replace('class="legs"', 'class="legs" opacity="0"'), -8);
  const svg = field(600) +
    shadow(TX, G + 6, 220) + shadow(WMX, G + 4, 150) + shadow(SCX, G + 4, 110) +
    tower + plaque + X + number(TX, 220, 170, "604", C.navy, C.cream) +
    stand(K, wm, WMX, G, WMK) +
    stand(K, sciO, SCX, G, SCK) + medBill + number(hand[0] + 10, hand[1] - 120, 150, "1", C.navy, C.cream) +
    film(id, 23);
  return { svg, alt: "A cream sky over a tan field. Left, a tower of banded war-money bundles, 604 above it, the Weapons Maker grinning beside it with his baby missile; a brass plaque on the tower reading POLITICAL PROBLEM has a red X through it. Right, the Scientist proudly holds up one medicine bill under a 1." };
}

// hardware: a 1950s computer hewn from stone sits on top of its hoard of rocks, a smug face on its screen. On its
// stone keyboard, one shiny new key: a red button, still in its gift ribbon. A launch trail arcs from its chimney to
// a mushroom cloud on the horizon, and the friendly stranger who came to say hello stands charred in front of it,
// frozen mid-wave, his bouquet smoking.
function hardware(H, id) {
  const { C } = H, K = withProps(H.K), ink = C.line, G = 880, HZ = 600;
  const ST = "#A9A391", ST2 = "#8F8A79", ST3 = "#C2BCA9";
  const hd = `<defs><pattern id="${id}-hd" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><circle cx="3.5" cy="3.5" r="1.5" fill="${ink}"/></pattern></defs>`;
  // the hoard: a mound of rocks, back rows first
  const rows = [
    [[520, 770, 60, 38], [640, 760, 70, 40], [770, 764, 66, 38], [890, 772, 58, 36]],
    [[430, 820, 70, 42], [560, 818, 76, 44], [700, 822, 80, 42], [840, 818, 74, 44], [970, 824, 66, 40]],
    [[360, 866, 66, 38], [480, 870, 76, 40], [620, 874, 84, 38], [770, 874, 84, 40], [910, 870, 76, 40], [1040, 864, 62, 36]],
  ];
  let hoard = "", n = 0;
  for (const row of rows) for (const [x, y, rx, ry] of row) hoard += stone(x, y, rx, ry, ++n * 3 + 1, [ST, ST2, ST3][n % 3], ink);
  // the cabinet, hewn: chipped corners, chisel marks, halftone on its shaded side
  const CX = 700, top = 236, bot = 744, L = CX - 270, R = CX + 270;
  const hewn = [[L + 6, bot], [L, top + 70], [L + 10, top + 26], [L + 46, top + 6], [CX - 70, top], [CX - 48, top + 14], [CX - 20, top + 2], [R - 46, top], [R - 8, top + 24],
    [R, top + 110], [R - 12, top + 132], [R + 2, top + 160], [R - 4, bot]];
  const hd2 = "M" + hewn.map((p) => p.join(",")).join(" L") + " Z";
  const cab = `<path d="${hd2}" fill="${ST}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
    `<clipPath id="${id}-cab"><path d="${hd2}"/></clipPath><rect x="${R - 120}" y="${top}" width="140" height="${bot - top}" fill="url(#${id}-hd)" opacity="0.16" clip-path="url(#${id}-cab)"/>` +
    `<path d="M${L + 22},${top + 120} l26,18 l-6,24 M${L + 30},${bot - 150} l34,-8 M${R - 40},${top + 300} l-20,-16 l6,-26 M${CX - 10},${top + 18} l-6,20" fill="none" stroke="${ink}" stroke-width="3" opacity="0.6" stroke-linecap="round"/>` +
    [[L + 80, top + 30], [R - 150, top + 26], [L + 36, top + 380], [R - 30, bot - 40], [CX + 40, bot - 136]].map(([x, y]) => `<path d="M${x},${y} l10,4 M${x + 4},${y + 10} l9,3" stroke="${ink}" stroke-width="2.4" opacity="0.45" stroke-linecap="round"/>`).join("");
  const SL = L + 38, SY = top + 40, SW = 340, SH = 250;
  const screen = `<rect x="${SL - 16}" y="${SY - 16}" width="${SW + 32}" height="${SH + 32}" rx="40" fill="${ST3}" stroke="${ink}" stroke-width="5"/>` +
    `<rect x="${SL}" y="${SY}" width="${SW}" height="${SH}" rx="30" fill="${C.slate}" stroke="${ink}" stroke-width="6"/>` +
    face(SL + SW / 2 - 6, SY + 100, 5.4, "smug", { look: 1, line: C.cream, ink, my: 17, mw: 12 }) +
    `<path d="M${SL + 26},${SY + 70} Q${SL + 40},${SY + 30} ${SL + 90},${SY + 22}" fill="none" stroke="${C.cream}" stroke-width="8" opacity="0.16" stroke-linecap="round"/>`;
  const reel = (x, y) => `<circle cx="${x}" cy="${y}" r="58" fill="${ST3}" stroke="${ink}" stroke-width="5"/><circle cx="${x}" cy="${y}" r="46" fill="none" stroke="${ST2}" stroke-width="4"/>` +
    [0, 120, 240].map((a) => `<circle cx="${f1(x + 26 * Math.cos(((a - 30) * Math.PI) / 180))}" cy="${f1(y + 26 * Math.sin(((a - 30) * Math.PI) / 180))}" r="13" fill="${ST2}" stroke="${ink}" stroke-width="3"/>`).join("") +
    `<circle cx="${x}" cy="${y}" r="8" fill="${ink}"/>`;
  const lamps = [0, 1, 2, 3, 4, 5, 6].map((i) => `<circle cx="${L + 56 + i * 46}" cy="${top + 338}" r="13" fill="${[C.orange, C.slate, C.yellow, C.slate, C.orange, C.yellow, C.slate][i]}" stroke="${ink}" stroke-width="3.4"/>`).join("");
  const corner = `<rect x="${L + 30}" y="${bot - 124}" width="336" height="58" fill="${ST3}" stroke="${ink}" stroke-width="4"/>` +
    `<rect x="${L + 38}" y="${bot - 116}" width="320" height="42" fill="none" stroke="${ST2}" stroke-width="2.4"/>` +
    label(L + 198, bot - 84, 28, "EST. 200,000 YEARS AGO", ink, 'opacity="0.85"');
  const chim = `<path d="M${R - 150},${top + 2} L${R - 142},${top - 100} H${R - 72} L${R - 64},${top + 2} Z" fill="${ST2}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    `<path d="M${R - 148},${top - 100} H${R - 66}" stroke="${ink}" stroke-width="10"/>`;
  const kb = `<path d="M${CX - 250},${bot + 12} L${CX - 222},${bot - 34} H${CX + 222} L${CX + 250},${bot + 12} Z" fill="${ST3}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    [0, 1, 2, 3, 4, 5, 6].map((i) => `<rect x="${CX - 214 + i * 46}" y="${bot - 24}" width="36" height="22" rx="3" fill="${ST2}" stroke="${ink}" stroke-width="2.4"/>`).join("");
  // the new key: a shiny red button on a mustard collar, a teal ribbon over its dome and a bow on top
  const BX = CX + 160, BY = bot - 30;
  const dome = `M${BX - 46},${BY - 14} Q${BX - 46},${BY - 82} ${BX},${BY - 82} Q${BX + 46},${BY - 82} ${BX + 46},${BY - 14} Z`;
  const button = `<rect x="${BX - 60}" y="${BY - 16}" width="120" height="24" rx="4" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/>` +
    `<path d="${dome}" fill="${C.war}" stroke="${ink}" stroke-width="5"/>` +
    `<clipPath id="${id}-dome"><path d="${dome}"/></clipPath><rect x="${BX - 9}" y="${BY - 90}" width="18" height="80" fill="${C.med}" clip-path="url(#${id}-dome)"/>` +
    `<path d="M${BX - 9},${BY - 80} V${BY - 14} M${BX + 9},${BY - 80} V${BY - 14}" stroke="${ink}" stroke-width="2.4" clip-path="url(#${id}-dome)"/>` +
    `<path d="M${BX - 30},${BY - 36} Q${BX - 28},${BY - 62} ${BX - 14},${BY - 68}" fill="none" stroke="${WHITE}" stroke-width="6" stroke-linecap="round" opacity="0.85"/>` +
    `<path d="M${BX},${BY - 84} C${BX - 20},${BY - 122} ${BX - 56},${BY - 112} ${BX - 44},${BY - 88} C${BX - 36},${BY - 76} ${BX - 14},${BY - 80} ${BX},${BY - 84} Z M${BX},${BY - 84} C${BX + 20},${BY - 122} ${BX + 56},${BY - 112} ${BX + 44},${BY - 88} C${BX + 36},${BY - 76} ${BX + 14},${BY - 80} ${BX},${BY - 84} Z" fill="${C.med}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
    `<path d="M${BX - 4},${BY - 82} l-18,30 l10,-2 M${BX + 4},${BY - 82} l16,32 l-10,-3" fill="none" stroke="${ink}" stroke-width="9" stroke-linejoin="round"/><path d="M${BX - 4},${BY - 82} l-18,30 l10,-2 M${BX + 4},${BY - 82} l16,32 l-10,-3" fill="none" stroke="${C.med}" stroke-width="4.5" stroke-linejoin="round"/>` +
    `<rect x="${BX - 10}" y="${BY - 94}" width="20" height="18" rx="5" fill="${C.med}" stroke="${ink}" stroke-width="3.6"/>`;
  // the trail from the chimney over to the cloud
  const NX = 1650, P0 = [R - 107, top - 120], P1 = [1150, -70], P2 = [NX - 40, HZ - 40];
  let trail = "";
  for (let i = 0; i <= 20; i++) {
    const u = i / 20, a = (1 - u) * (1 - u), b = 2 * u * (1 - u), c = u * u;
    const x = a * P0[0] + b * P1[0] + c * P2[0], y = a * P0[1] + b * P1[1] + c * P2[1];
    trail += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(12 + 12 * u)}" fill="#E9E1CF" stroke="${ink}" stroke-width="3.4" opacity="${(0.45 + 0.55 * u).toFixed(2)}"/>`;
  }
  const cloud = at(NX, HZ + 34, 0.92, K.nuke());
  // the stranger: charred, frozen mid-wave, a smoking bouquet held out to the machine
  const SX = 1320, SK = 2.75;
  const so = { tone: 2, outfit: "suit", seed: 4, look: "left", charred: true, arms: [[-36, -80], [146, 176]] };
  const rr = K.rig(so), h0 = [SX + SK * rr.hand[0][0], G - 100 * SK + SK * rr.hand[0][1]];
  const char = "rgb(58,52,47)", char2 = "rgb(84,76,68)";
  const flower = (x, y, rot) => `<g transform="translate(${x},${y}) rotate(${rot})">` + [0, 72, 144, 216, 288].map((a) => `<ellipse cx="${f1(8 * Math.cos((a * Math.PI) / 180))}" cy="${f1(8 * Math.sin((a * Math.PI) / 180))}" rx="7" ry="5" transform="rotate(${a} ${f1(8 * Math.cos((a * Math.PI) / 180))} ${f1(8 * Math.sin((a * Math.PI) / 180))})" fill="${char2}" stroke="${ink}" stroke-width="1.8"/>`).join("") + `<circle r="4.5" fill="${char}" stroke="${ink}" stroke-width="1.6"/></g>`;
  const bouquet = at(h0[0] - 6, h0[1] + 4, SK, `<path d="M0,6 Q-12,-14 -20,-26 M0,6 Q-2,-18 -4,-34 M0,6 Q10,-14 12,-26" fill="none" stroke="${ink}" stroke-width="2.6"/>` +
    flower(-22, -30, 30) + flower(-4, -38, 0) + flower(14, -30, -20) + `<path d="M-6,8 L6,8 L4,-2 L-4,-2 Z" fill="${char}" stroke="${ink}" stroke-width="1.8"/>` +
    `<path d="M-14,-46 q-5,-6 0,-11 q5,-6 0,-11 M6,-52 q-5,-6 0,-11 q5,-6 0,-11" fill="none" stroke="#8C8782" stroke-width="2.4" stroke-linecap="round"/>`);
  const svg = hd + field(HZ) + cloud + trail +
    shadow(700, G + 10, 380, 0.4) + shadow(SX, G + 4, 110) +
    chim + cab + screen + reel(R - 84, top + 112) + reel(R - 84, top + 246) + lamps + corner + kb + button + hoard +
    stand(K, so, SX, G, SK) + bouquet +
    film(id, 31);
  return { svg, alt: "A 1950s computer hewn from stone sits on a hoard of rocks, a smug face on its screen and a shiny red button in a gift ribbon on its stone keyboard. A smoke trail arcs from its chimney to a mushroom cloud on the horizon; the stranger stands charred in front of it, frozen mid-wave, his bouquet smoking." };
}

// owners-manual: a 1950s living room. A man sits in his armchair, reading a manual whose cover says OWNER'S MANUAL,
// YOU. The top of his head is open like a lid. Beside the chair, his brain, still on its cord, tiptoes up on stick
// legs with a lit bomb over its head, grinning.
function ownersManual(H, id) {
  const { C } = H, K = withProps(H.K), ink = C.line, FL = 740, G = 900;
  const WALL = "#E6D3A8", WALL2 = "#D9C192", FLOOR = "#9B6A45", RUG = C.orange;
  let paper = "";
  for (let y = 70; y < FL - 40; y += 150) for (let x = (y / 150) % 2 ? 40 : 115; x < 1920; x += 150) paper += K.boomerang(x, y, 0.42, WALL2, ((x * 7 + y) % 360));
  const room = `<rect width="1920" height="1080" fill="${FLOOR}"/><rect width="1920" height="${FL}" fill="${WALL}"/>` + paper +
    `<rect y="${FL - 28}" width="1920" height="28" fill="${C.rust}"/><path d="M0,${FL} H1920" stroke="${ink}" stroke-width="4"/>` +
    [0, 1, 2, 3, 4, 5].map((i) => `<path d="M0,${FL + 56 + i * 58} H1920" stroke="#86593A" stroke-width="3"/>`).join("") +
    `<ellipse cx="960" cy="${G - 8}" rx="640" ry="74" fill="${RUG}" stroke="${ink}" stroke-width="4"/><ellipse cx="960" cy="${G - 8}" rx="580" ry="56" fill="none" stroke="${C.yellow}" stroke-width="5"/>`;
  const lamp = `<path d="M330,${G} l-44,16 M330,${G} l44,16 M330,${G} V300" stroke="${ink}" stroke-width="8" stroke-linecap="round"/>` +
    `<path d="M246,300 L278,186 H382 L414,300 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/><path d="M262,300 H398" stroke="${C.orange}" stroke-width="6"/>`;
  // the armchair: the back behind him, the near arm in front of his legs
  const CHX = 720;
  const chairBack = `<path d="M${CHX - 200},${G - 130} L${CHX - 214},${G - 440} Q${CHX - 210},${G - 492} ${CHX - 150},${G - 492} H${CHX + 150} Q${CHX + 210},${G - 492} ${CHX + 214},${G - 440} L${CHX + 200},${G - 130} Z" fill="${C.orange}" stroke="${ink}" stroke-width="6"/>` +
    `<path d="M${CHX - 160},${G - 452} H${CHX + 160}" stroke="${C.rust}" stroke-width="5" opacity="0.5"/>` +
    `<path d="M${CHX - 176},${G - 40} L${CHX - 196},${G + 14} M${CHX + 176},${G - 40} L${CHX + 196},${G + 14}" stroke="${ink}" stroke-width="10" stroke-linecap="round"/>` +
    `<rect x="${CHX - 222}" y="${G - 180}" width="444" height="140" rx="18" fill="${C.orange}" stroke="${ink}" stroke-width="6"/>` +
    `<rect x="${CHX - 250}" y="${G - 300}" width="106" height="262" rx="30" fill="${C.orange}" stroke="${ink}" stroke-width="6"/>`;
  const chairArm = `<rect x="${CHX + 150}" y="${G - 300}" width="106" height="262" rx="30" fill="${C.orange}" stroke="${ink}" stroke-width="6"/><path d="M${CHX + 172},${G - 262} V${G - 72}" stroke="${C.rust}" stroke-width="4" opacity="0.5"/>`;
  // the reader, seated (thighs forward, shins down), holding the book out in front of him
  const RK = 3.4, RX = CHX - 20, SEAT = G - 176;
  const man = { tone: 1, outfit: "shirt", color: 1, hair: 0, seed: 7, look: "right", mood: "smile", arms: [[14, 70], [26, 76]], build: { legPose: [[84, 4], [84, 4]] } };
  const mr = K.rig(man);
  // the open skull: an empty dark hole on top, and the lid (hair on top) standing open on its hinge at the back
  const lid = `<ellipse cx="2" cy="-23" rx="16" ry="5.5" fill="${C.ink}" stroke="${ink}" stroke-width="1.6"/><path d="M-12,-22 Q2,-26 16,-23" fill="none" stroke="#E9B4C1" stroke-width="2.4"/>` +
    `<g transform="translate(-14,-23) rotate(-72)"><path d="M0,0 Q2,-20 16,-22 Q30,-20 32,0 Z" fill="${ink}" stroke="${ink}" stroke-width="2.2" stroke-linejoin="round"/><path d="M2,-1.5 H30" stroke="#D9B48F" stroke-width="5"/></g>`;
  const manSvg = K.person(man).replace("<!--face-end-->", lid + "<!--face-end-->");
  const manAt = [RX, SEAT - mr.hipY * RK];
  const P = (p) => [manAt[0] + RK * p[0], manAt[1] + RK * p[1]];
  const head = P(mr.top), hands = mr.hand.map(P);
  // the book, its cover to us, held open on his lap below his chin so his face shows over it
  const BW = 256, BHt = 300, BKX = RX + 40, BKY = head[1] + 168 + BHt / 2;
  const book = `<g transform="translate(${f1(BKX)},${f1(BKY)}) rotate(6)">` +
    `<path d="M${-BW / 2 - 18},${-BHt / 2 + 10} L${-BW / 2},${-BHt / 2} V${BHt / 2} L${-BW / 2 - 18},${BHt / 2 + 10} Z" fill="${C.navy}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    `<rect x="${-BW / 2}" y="${-BHt / 2}" width="${BW}" height="${BHt}" fill="${C.orange}" stroke="${ink}" stroke-width="5"/>` +
    `<rect x="${-BW / 2 + 12}" y="${-BHt / 2 + 12}" width="${BW - 24}" height="${BHt - 24}" fill="none" stroke="${WHITE}" stroke-width="3" opacity="0.8"/>` +
    `<rect x="${-BW / 2 + 12}" y="${-BHt / 2 + 30}" width="${BW - 24}" height="56" fill="${C.navy}"/>` +
    label(0, -BHt / 2 + 69, 26, "OWNER'S MANUAL", C.cream) +
    number(0, 70, 112, "YOU", WHITE, C.ink) +
    `<path d="M${-BW / 2 + 40},${BHt / 2 - 46} H${BW / 2 - 40}" stroke="${WHITE}" stroke-width="3" opacity="0.8"/>` + "</g>";
  const thumbs = [-1, 1].map((d) => `<g transform="translate(${f1(BKX)},${f1(BKY)}) rotate(6)"><path d="M${d * (BW / 2 + 6) - 10},20 h20 v34 h-20 Z" fill="#D9B48F" stroke="${ink}" stroke-width="4.5" stroke-linejoin="round"/></g>`).join("");
  void hands;
  // the brain, tiptoeing up on stick legs, a lit bomb held over its head
  const BRX = 1290, BRY = 600, BK = 1.3, pink = "#E9B4C1", fold = "#C98B9A";
  const brainBody = `<path d="M-120,10 C-150,-20 -140,-80 -96,-96 C-90,-140 -30,-150 -4,-122 C20,-152 84,-146 96,-104 C142,-96 156,-36 126,-4 C132,40 88,64 52,54 C30,80 -30,80 -48,56 C-96,70 -138,46 -120,10 Z" fill="${pink}" stroke="${ink}" stroke-width="6" stroke-linejoin="round"/>` +
    `<path d="M-4,-122 C-10,-90 8,-60 -2,-30 C-10,-4 6,24 0,52" fill="none" stroke="${fold}" stroke-width="6" stroke-linecap="round"/>` +
    `<path d="M-96,-96 q30,10 26,40 q-4,26 24,34 M-120,10 q34,-6 48,18 M96,-104 q-30,14 -22,40 q6,24 -20,36 M126,-4 q-30,-4 -40,22 M-60,-120 q12,22 -6,40 M60,-130 q-6,20 14,34" fill="none" stroke="${fold}" stroke-width="5" stroke-linecap="round"/>`;
  const brainFace = face(-10, -36, 2.5, "sly", { look: -1, my: 18, mw: 14 });
  const legY = (G - BRY) / BK;
  const legs = `<path d="M-40,60 L-70,${f1(legY * 0.62)} L-96,${f1(legY - 4)} M36,62 L40,${f1(legY * 0.6)} L70,${f1(legY - 16)}" fill="none" stroke="${ink}" stroke-width="9" stroke-linecap="round" stroke-linejoin="miter"/>` +
    `<path d="M-108,${f1(legY - 2)} L-90,${f1(legY - 10)} M60,${f1(legY - 22)} L80,${f1(legY - 14)}" stroke="${ink}" stroke-width="12" stroke-linecap="round"/>`;
  const armsB = `<path d="M-116,-40 L-146,-130 L-104,-214 M110,-64 L132,-150 L80,-218" fill="none" stroke="${ink}" stroke-width="9" stroke-linecap="round" stroke-linejoin="miter"/>`;
  const bomb = at(-16, -196, 1.5, K.props.bomb({}));
  const brain = at(BRX, BRY, BK, legs + armsB + brainBody + brainFace + bomb, -9);
  // the cord from his open skull to the brain's stem
  const c0 = [head[0] + 6, head[1] + 8], c1 = [BRX - 30, BRY + 74];
  const cd = `M${f1(c0[0])},${f1(c0[1])} C${f1(c0[0] + 30)},${f1(c0[1] - 230)} ${f1(c1[0] - 220)},${f1(c1[1] - 260)} ${f1(c1[0] - 160)},${f1(c1[1] + 30)} S${f1(c1[0] - 40)},${f1(c1[1] + 60)} ${f1(c1[0])},${f1(c1[1])}`;
  const cord = `<path d="${cd}" fill="none" stroke="${ink}" stroke-width="16" stroke-linecap="round"/><path d="${cd}" fill="none" stroke="${pink}" stroke-width="8" stroke-linecap="round"/>`;
  const svg = room + lamp + shadow(CHX, G + 10, 280, 0.4) + shadow(BRX - 20, G + 6, 120, 0.4) + chairBack +
    at(manAt[0], manAt[1], RK, manSvg) + chairArm + book + thumbs + cord + brain + film(id, 41);
  return { svg, alt: "A 1950s living room. A man sits in an orange armchair reading a manual whose cover says OWNER'S MANUAL, YOU. The top of his head is open like a lid; beside the chair his brain, still on its cord, tiptoes up on stick legs with a lit bomb over its head, grinning." };
}

// universe-exploded: the dark after the bang. One hydrogen atom, alone, bored stiff, with a long white beard and a
// cobweb grown while it waited; 400,000,000 YEARS in the sky, as the-toll puts its number in the sky.
function universe(H, id) {
  const { C } = H, ink = C.line, AX = 960, AY = 520, NR = 124;
  let s = 4004;
  const r = () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
  const glow = `<circle cx="${AX}" cy="${AY}" r="820" fill="none" stroke="#1C2843" stroke-width="44" opacity="0.6"/><circle cx="${AX}" cy="${AY}" r="960" fill="none" stroke="#16213A" stroke-width="30" opacity="0.6"/>`;
  let dust = "";
  for (let i = 0; i < 40; i++) dust += `<circle cx="${f1(r() * 1920)}" cy="${f1(r() * 1080)}" r="${f1(1 + r() * 1.6)}" fill="${C.cream}" opacity="${(0.06 + r() * 0.1).toFixed(2)}"/>`;
  const HAIR = "#EEE9DC", HAIR2 = "#B4AE9E", LID = "#C9712F";
  // the beard: tufted edges from ear to ear, falling and narrowing to a point that curls
  const L = 300, N = 10;
  const ctr = (t) => [AX + 34 * Math.sin(t * 4.4) * t, AY + 34 + t * L];
  const w = (t) => NR * 1.02 * Math.pow(1 - t, 0.8) + 8;
  const side = (dir) => Array.from({ length: N + 1 }, (_, i) => { const t = i / N, c = ctr(t); return [c[0] + dir * w(t), c[1]]; });
  const Lp = side(-1), Rp = side(1).reverse();
  const tuft = (a, b, out) => { const m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], dx = b[0] - a[0], dy = b[1] - a[1], n = Math.hypot(dx, dy) || 1; return `Q${f1(m[0] - (dy / n) * out)},${f1(m[1] + (dx / n) * out)} ${f1(b[0])},${f1(b[1])}`; };
  const tip = ctr(1);
  let bd = `M${f1(Lp[0][0])},${f1(AY - 20)} L${f1(Lp[0][0])},${f1(Lp[0][1])}`;
  for (let i = 0; i < N; i++) bd += " " + tuft(Lp[i], Lp[i + 1], 20);
  bd += ` Q${f1(tip[0] - 6)},${f1(tip[1] + 40)} ${f1(tip[0] + 34)},${f1(tip[1] + 26)} Q${f1(tip[0] + 50)},${f1(tip[1] + 4)} ${f1(tip[0] + 28)},${f1(tip[1] + 2)}`;
  for (let i = 0; i < N; i++) bd += " " + tuft(Rp[i], Rp[i + 1], 20);
  bd += ` L${f1(Rp[N][0])},${f1(AY - 20)} Q${f1(AX + 40)},${f1(AY + 62)} ${f1(AX)},${f1(AY + 60)} Q${f1(AX - 40)},${f1(AY + 62)} ${f1(Lp[0][0])},${f1(AY - 20)} Z`;
  let strands = "";
  for (const k of [-0.7, -0.35, 0, 0.35, 0.7]) {
    const pts = [0.16, 0.3, 0.44, 0.58, 0.72, 0.86].map((t) => { const c = ctr(t); return [c[0] + k * w(t) * 0.8 + (r() - 0.5) * 8, c[1]]; });
    let d = `M${f1(pts[0][0])},${f1(pts[0][1])}`;
    for (let i = 1; i < pts.length; i++) d += ` Q${f1(pts[i - 1][0] + (i % 2 ? 12 : -12))},${f1((pts[i - 1][1] + pts[i][1]) / 2)} ${f1(pts[i][0])},${f1(pts[i][1])}`;
    strands += `<path d="${d}" fill="none" stroke="${HAIR2}" stroke-width="4" stroke-linecap="round"/>`;
  }
  const beard = `<path d="${bd}" fill="${HAIR}" stroke="${ink}" stroke-width="5.5" stroke-linejoin="round"/>` + strands;
  // a walrus moustache hiding the mouth, tufts hanging over the beard
  const mx = [-100, -64, -30, 0, 30, 64, 100];
  let sd = `M${AX - 100},${AY + 40} Q${AX - 70},${AY - 6} ${AX},${AY + 8} Q${AX + 70},${AY - 6} ${AX + 100},${AY + 40}`;
  for (let i = mx.length - 1; i > 0; i--) sd += ` Q${AX + (mx[i] + mx[i - 1]) / 2},${AY + 82 - Math.abs(mx[i] + mx[i - 1]) * 0.12} ${AX + mx[i - 1]},${AY + 40 + Math.abs(mx[i - 1]) * 0.04}`;
  const stache = `<path d="${sd} Z" fill="${HAIR}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>` +
    `<path d="M${AX - 60},${AY + 28} q-8,14 -6,30 M${AX - 26},${AY + 22} q-4,16 0,32 M${AX + 26},${AY + 22} q4,16 0,32 M${AX + 60},${AY + 28} q8,14 6,30" fill="none" stroke="${HAIR2}" stroke-width="3.6" stroke-linecap="round"/>`;
  // half-shut eyes, pupils rolled down and aside: bored stiff
  const eye = (ex) => `<ellipse cx="${ex}" cy="${AY - 34}" rx="30" ry="18" fill="${C.cream}" stroke="${ink}" stroke-width="4.5"/>` +
    `<circle cx="${ex + 8}" cy="${AY - 26}" r="9" fill="${ink}"/>` +
    `<path d="M${ex - 32},${AY - 34} A30,18 0 0 1 ${ex + 32},${AY - 34} Q${ex},${AY - 28} ${ex - 32},${AY - 34} Z" fill="${LID}" stroke="${ink}" stroke-width="4.5" stroke-linejoin="round"/>` +
    `<path d="M${ex - 34},${AY - 33} Q${ex},${AY - 26} ${ex + 34},${AY - 33}" fill="none" stroke="${ink}" stroke-width="7" stroke-linecap="round"/>`;
  const nose = `<ellipse cx="${AX}" cy="${AY + 4}" rx="22" ry="17" fill="${LID}" stroke="${ink}" stroke-width="4.5"/>`;
  // long brows drooping past the eyes
  const brow = (dir) => `<path d="M${AX + dir * 8},${AY - 66} Q${AX + dir * 60},${AY - 92} ${AX + dir * 112},${AY - 40} q${dir * 6},22 ${dir * -4},34 q${dir * -6},-18 ${dir * -18},-20 q${dir * -2},14 ${dir * -14},18 q${dir * -2},-22 ${dir * -26},-30 Q${AX + dir * 40},${AY - 66} ${AX + dir * 8},${AY - 56} Z" fill="${HAIR}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>`;
  const nucleus = `<circle cx="${AX}" cy="${AY}" r="${NR}" fill="${C.orange}" stroke="${ink}" stroke-width="6"/><circle cx="${AX - 56}" cy="${AY - 66}" r="20" fill="${C.yellow}" opacity="0.9"/>` +
    eye(AX - 44) + eye(AX + 44) + nose;
  // one orbit, one electron, and a cobweb strung between the orbit and the nucleus
  const RX = 400, RY = 128, TILT = -16, tr = (TILT * Math.PI) / 180;
  const op = (a) => [AX + RX * Math.cos(a) * Math.cos(tr) - RY * Math.sin(a) * Math.sin(tr), AY + RX * Math.cos(a) * Math.sin(tr) + RY * Math.sin(a) * Math.cos(tr)];
  const orbitBack = `<path d="M${op(Math.PI).map(f1).join(",")} A${RX},${RY} ${TILT} 0 1 ${op(0).map(f1).join(",")}" fill="none" stroke="${C.cream}" stroke-width="7" opacity="0.9"/>`;
  const orbitFront = `<path d="M${op(0).map(f1).join(",")} A${RX},${RY} ${TILT} 0 1 ${op(Math.PI).map(f1).join(",")}" fill="none" stroke="${C.cream}" stroke-width="7" opacity="0.9"/>`;
  const e = op(-0.4);
  const electron = `<circle cx="${f1(e[0])}" cy="${f1(e[1])}" r="30" fill="${C.med}" stroke="${ink}" stroke-width="5"/><circle cx="${f1(e[0] - 9)}" cy="${f1(e[1] - 9)}" r="7" fill="${C.cream}" opacity="0.6"/>`;
  const hub = op(Math.PI + 0.36);
  const tgt = [[AX - NR * 0.8, AY - NR * 0.6], [AX - NR * 0.99, AY - NR * 0.12], [AX - NR * 0.98, AY + NR * 0.3], [hub[0] + 30, hub[1] + 150]];
  let web = tgt.map((t) => `M${f1(hub[0])},${f1(hub[1])} L${f1(t[0])},${f1(t[1])}`).join(" ");
  for (const k of [0.25, 0.45, 0.65, 0.85]) {
    const pts = tgt.map((t) => [hub[0] + (t[0] - hub[0]) * k, hub[1] + (t[1] - hub[1]) * k]);
    for (let i = 0; i < pts.length - 1; i++) {
      const m = [(pts[i][0] + pts[i + 1][0]) / 2 + 8, (pts[i][1] + pts[i + 1][1]) / 2 + 10];
      web += ` M${f1(pts[i][0])},${f1(pts[i][1])} Q${f1(m[0])},${f1(m[1])} ${f1(pts[i + 1][0])},${f1(pts[i + 1][1])}`;
    }
  }
  const spider = `<g transform="translate(${f1(hub[0] + 30)},${f1(hub[1] + 150)})"><path d="M0,-34 V-4" stroke="${C.cream}" stroke-width="2" opacity="0.85"/><circle r="9" fill="${ink}" stroke="${C.cream}" stroke-width="2.4"/>` +
    [-1, 1].map((d) => `<path d="M${d * 6},-2 l${d * 12},-10 M${d * 7},2 l${d * 14},2 M${d * 6},5 l${d * 11},12" stroke="${C.cream}" stroke-width="2.4" fill="none" stroke-linecap="round"/>`).join("") + "</g>";
  const cobweb = `<path d="${web}" fill="none" stroke="${C.cream}" stroke-width="3" opacity="0.9" stroke-linecap="round"/>` + spider;
  const svg = `<rect width="1920" height="1080" fill="${C.ink}"/>` + glow + dust +
    number(960, 196, 168, "400,000,000", C.cream, "#000814") + label(960, 280, 54, "YEARS", C.yellow, 'letter-spacing="12"') +
    orbitBack + nucleus + beard + stache + brow(-1) + brow(1) + cobweb + orbitFront + electron + film(id, 47);
  return { svg, alt: "Dark space after the bang. One hydrogen atom, alone and bored stiff, half-shut eyes, drooping white brows, a walrus moustache and a long white beard, a cobweb with a little spider strung from its orbit, under 400,000,000 YEARS in cream." };
}

export default {
  "genetic-slavery-title": title,
  "six-oh-four": sixOhFour,
  hardware,
  "owners-manual": ownersManual,
  "universe-exploded": universe,
};
