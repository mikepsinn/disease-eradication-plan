// Three candidate designs for the humans, each a drop-in for KIT.bean(o) so the Part 1 sketches
// can be redrawn with it unchanged: drawn around (0, 0), head near y -66, feet near y 100.
// o: { tone 0..3, light "off"|"red"|"teal", mouth, hair 0..2, arms [[a1, a2], [b1, b2]] (deg, 0 = down),
//      brows, look "right"|"left"|"camera", mood "smile"|"eager"|"sad"|"flat" }
import base from "./part-01-opening.sketch.mjs";

const INK = "#1B1B1B", PAPER = "#F3EAD3", WAR = "#D7322B", MED = "#1FA39A";
const TONES = ["#F4E3CC", "#D9B48F", "#A87B57", "#6F4B33"];
const lightFill = (o) => (o.light === "red" ? WAR : o.light === "teal" ? MED : "#E9E1CC");
const moodOf = (o) => o.mood || (o.mouth === "smile" ? "smile" : o.mouth === "o" ? "eager" : o.mouth === "frown" ? "sad" : "flat");
const rad = (d) => (d * Math.PI) / 180;

// A two-segment limb from (x, y); returns the path, the elbow and the hand point.
function limb(x, y, a1, a2, len) {
  const ex = x + len * Math.sin(rad(a1)), ey = y + len * Math.cos(rad(a1));
  const hx = ex + len * Math.sin(rad(a2)), hy = ey + len * Math.cos(rad(a2));
  return { d: `M${x},${y} L${ex.toFixed(1)},${ey.toFixed(1)} L${hx.toFixed(1)},${hy.toFixed(1)}`, ex, ey, hx, hy };
}

// ── 1. Expressive beans: the same body, with eyes, brows, mouths and gloves that can act ──
export function expressiveBean(o = {}) {
  const tone = TONES[(o.tone || 0) % 4];
  const mood = moodOf(o);
  const dx = o.look === "right" ? 5 : o.look === "left" ? -5 : 0;
  const [la, ra] = o.arms || [[20, 10], [-20, -10]];
  const arm = (x, a) => {
    const l = limb(x, -6, a[0], a[1], 26);
    return `<path d="${l.d}" fill="none" stroke="${INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>` +
      `<circle cx="${l.ex.toFixed(1)}" cy="${l.ey.toFixed(1)}" r="4.5" fill="${PAPER}" stroke="${INK}" stroke-width="2.5"/>` +
      `<circle cx="${l.hx.toFixed(1)}" cy="${l.hy.toFixed(1)}" r="9" fill="#FFF" stroke="${INK}" stroke-width="3"/>`;
  };
  const leg = (x, a) => {
    const l = limb(x, 52, a, -a, 24);
    return `<path d="${l.d}" fill="none" stroke="${INK}" stroke-width="7" stroke-linecap="round"/><circle cx="${l.ex.toFixed(1)}" cy="${l.ey.toFixed(1)}" r="4.5" fill="${PAPER}" stroke="${INK}" stroke-width="2.5"/>` +
      `<ellipse cx="${(l.hx + (x < 0 ? -6 : 6)).toFixed(1)}" cy="${(l.hy + 2).toFixed(1)}" rx="11" ry="6" fill="${INK}"/>`;
  };
  const brows = {
    eager: "M-25,-58 q10,-9 20,-2 M25,-58 q-10,-9 -20,-2",
    smile: "M-24,-53 q9,-5 18,0 M24,-53 q-9,-5 -18,0",
    sad: "M-24,-50 L-6,-57 M24,-50 L6,-57",
    flat: "M-24,-53 h18 M24,-53 h-18",
  }[mood];
  const mouth = {
    eager: `<ellipse cx="${dx * 0.6}" cy="-14" rx="8" ry="10" fill="${INK}"/><ellipse cx="${dx * 0.6}" cy="-9" rx="5" ry="3.5" fill="${WAR}" opacity="0.8"/>`,
    smile: `<path d="M-15,-19 q15,17 30,0 z" fill="${INK}"/><path d="M-11,-18 h22 v3 h-22 z" fill="#FFF"/>`,
    sad: `<path d="M-11,-10 q11,-9 22,0" fill="none" stroke="${INK}" stroke-width="3.6" stroke-linecap="round"/>`,
    flat: `<path d="M-10,-14 h20" stroke="${INK}" stroke-width="3.6" stroke-linecap="round"/>`,
  }[mood];
  const eye = (x) => `<ellipse cx="${x}" cy="-36" rx="11" ry="13" fill="#FFF" stroke="${INK}" stroke-width="3"/><circle cx="${x + dx}" cy="${mood === "sad" ? -31 : -34}" r="5.5" fill="${INK}"/><circle cx="${x + dx + 2}" cy="-37" r="1.8" fill="#FFF"/>`;
  return `<g class="bean">${leg(-20, 4)}${leg(20, -4)}` +
    `<path d="M0,-66 C34,-66 44,-36 42,-2 C40,38 30,62 0,62 C-30,62 -42,38 -42,0 C-42,-40 -30,-66 0,-66 Z" fill="${tone}" stroke="${INK}" stroke-width="5"/>` +
    (o.hair === 1 ? `<path d="M-30,-52 q30,-30 60,0 q-30,-12 -60,0 Z" fill="${INK}"/>` : o.hair === 2 ? `<path d="M-8,-66 q8,-18 16,0" fill="none" stroke="${INK}" stroke-width="4"/>` : "") +
    eye(-14) + eye(14) + `<path d="${brows}" fill="none" stroke="${INK}" stroke-width="4.5" stroke-linecap="round"/>` + mouth +
    `<circle cx="0" cy="12" r="9" fill="${lightFill(o)}" stroke="${INK}" stroke-width="3"/>` + arm(-38, la) + arm(38, ra) + "</g>";
}

// ── 2. Mid-century people: Wishonia's own 1960s cartoon style ─────────────
const SUITS = ["#55606F", "#8C7A5E", "#3E4A5C", "#6E5A4B"];
export function midCenturyPerson(o = {}) {
  const t = (o.tone || 0) % 4, skin = TONES[t], suit = SUITS[t];
  const mood = moodOf(o);
  const dir = o.look === "right" ? 1 : o.look === "left" ? -1 : 0;
  const dress = o.hair === 1;
  const [la, ra] = o.arms || [[20, 10], [-20, -10]];
  const arm = (x, a) => {
    const l = limb(x, -6, a[0], a[1], 25);
    return `<path d="${l.d}" fill="none" stroke="${suit}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><path d="${l.d}" fill="none" stroke="${INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity="0.5"/>` +
      `<circle cx="${l.ex.toFixed(1)}" cy="${l.ey.toFixed(1)}" r="3.6" fill="${PAPER}" stroke="${INK}" stroke-width="2"/>` +
      `<ellipse cx="${l.hx.toFixed(1)}" cy="${l.hy.toFixed(1)}" rx="6.5" ry="7.5" fill="${skin}" stroke="${INK}" stroke-width="2.5"/>`;
  };
  const leg = (x) => `<path d="M${x},40 L${x * 1.1},70 L${x * 1.15},94" fill="none" stroke="${INK}" stroke-width="7" stroke-linecap="round"/><circle cx="${x * 1.1}" cy="70" r="3.6" fill="${PAPER}" stroke="${INK}" stroke-width="2"/><ellipse cx="${x * 1.15 + (x < 0 ? -4 : 4)}" cy="97" rx="10" ry="5" fill="${INK}"/>`;
  const body = dress
    ? `<path d="M-17,-16 L17,-16 L33,48 L-33,48 Z" fill="${suit}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/><path d="M-17,-16 L17,-16 L13,4 L-13,4 Z" fill="${PAPER}" opacity="0.25"/>`
    : `<path d="M-25,-16 L25,-16 L20,44 L-20,44 Z" fill="${suit}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/><path d="M-8,-16 L8,-16 L0,6 Z" fill="#FFF" stroke="${INK}" stroke-width="2"/><path d="M0,-12 l-3.5,6 l3.5,14 l3.5,-14 z" fill="${INK}"/>`;
  const hx = dir * 4, hy = -44;
  const hair = o.hair === 1
    ? `<path d="M${hx - 26},${hy + 8} Q${hx - 28},${hy - 32} ${hx},${hy - 30} Q${hx + 28},${hy - 32} ${hx + 26},${hy + 8} L${hx + 20},${hy - 8} Q${hx},${hy - 20} ${hx - 20},${hy - 8} Z" fill="${INK}"/>`
    : o.hair === 2
      ? `<path d="M${hx - 30},${hy - 14} h60 v4 h-60 z M${hx - 18},${hy - 14} q2,-20 18,-20 q16,0 18,20 z" fill="${INK}"/>`
      : `<path d="M${hx - 22},${hy - 6} Q${hx - 22},${hy - 30} ${hx + 2},${hy - 30} Q${hx + 24},${hy - 30} ${hx + 22},${hy - 10} Q${hx + 4},${hy - 22} ${hx - 22},${hy - 6} Z" fill="${INK}"/>`;
  const ex = (k) => hx + dir * 6 + k * 8;
  const brows = {
    eager: [`M${ex(-1) - 6},${hy - 14} q6,-6 12,-1`, `M${ex(1) - 6},${hy - 15} q6,-6 12,1`],
    smile: [`M${ex(-1) - 6},${hy - 11} q6,-3 12,0`, `M${ex(1) - 6},${hy - 11} q6,-3 12,0`],
    sad: [`M${ex(-1) - 6},${hy - 8} L${ex(-1) + 6},${hy - 13}`, `M${ex(1) + 6},${hy - 8} L${ex(1) - 6},${hy - 13}`],
    flat: [`M${ex(-1) - 6},${hy - 11} h12`, `M${ex(1) - 6},${hy - 11} h12`],
  }[mood].join(" ");
  const my = hy + 14, mx = hx + dir * 6;
  const mouth = {
    eager: `<ellipse cx="${mx}" cy="${my + 1}" rx="4.5" ry="6" fill="${INK}"/>`,
    smile: `<path d="M${mx - 9},${my - 2} q9,9 18,0" fill="none" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>`,
    sad: `<path d="M${mx - 8},${my + 3} q8,-6 16,0" fill="none" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>`,
    flat: `<path d="M${mx - 7},${my} h14" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>`,
  }[mood];
  const nose = dir === 0 ? `<path d="M${hx},${hy - 2} l-3,9 h5" fill="none" stroke="${INK}" stroke-width="2.4" stroke-linejoin="round"/>` : `<path d="M${hx + dir * 12},${hy - 4} l${dir * 9},9 l${-dir * 8},1" fill="${skin}" stroke="${INK}" stroke-width="2.4" stroke-linejoin="round"/>`;
  return `<g class="person">${leg(-11)}${leg(11)}${body}` +
    `<circle cx="0" cy="16" r="7" fill="${lightFill(o)}" stroke="${INK}" stroke-width="2.5"/>` +
    `<rect x="-6" y="-22" width="12" height="9" fill="${skin}" stroke="${INK}" stroke-width="2"/>` +
    `<ellipse cx="${hx - dir * 21}" cy="${hy + 2}" rx="5" ry="7" fill="${skin}" stroke="${INK}" stroke-width="2.5"/>` +
    `<ellipse cx="${hx}" cy="${hy}" rx="22" ry="26" fill="${skin}" stroke="${INK}" stroke-width="3.5"/>` + hair +
    `<ellipse cx="${ex(-1)}" cy="${hy - 3}" rx="3" ry="4.5" fill="${INK}"/><ellipse cx="${ex(1)}" cy="${hy - 3}" rx="3" ry="4.5" fill="${INK}"/>` +
    `<path d="${brows}" fill="none" stroke="${INK}" stroke-width="3.6" stroke-linecap="round"/>` + nose + mouth +
    arm(-25, la) + arm(25, ra) + "</g>";
}

// ── 3. Cut-out paper puppets: flat cut pieces joined by brass pins ──────────
const COATS = ["#4A4A52", "#6B5B45", "#3B4250", "#5A4A40"];
function piece(d, fill, extra = "") {
  return `<path d="${d}" fill="#000" opacity="0.22" transform="translate(4,5)"/>` +
    `<path d="${d}" fill="${fill}" stroke="${PAPER}" stroke-width="7" stroke-linejoin="round" ${extra}/>` +
    `<path d="${d}" fill="none" stroke="${INK}" stroke-width="2.4" stroke-linejoin="round"/>`;
}
const pin = (x, y) => `<circle cx="${x}" cy="${y}" r="4" fill="#C9A13B" stroke="${INK}" stroke-width="1.8"/>`;
export function paperPuppet(o = {}) {
  const t = (o.tone || 0) % 4, skin = TONES[t], coat = COATS[t];
  const mood = moodOf(o);
  const f = o.look === "left" ? -1 : 1; // the profile faces right unless told otherwise
  const [la, ra] = o.arms || [[20, 10], [-20, -10]];
  const armPiece = (x, a) => {
    const l = limb(x, -8, a[0], a[1], 26);
    return `<path d="${l.d}" fill="none" stroke="#000" stroke-width="12" opacity="0.2" transform="translate(4,5)" stroke-linecap="round"/>` +
      `<path d="${l.d}" fill="none" stroke="${PAPER}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>` +
      `<path d="${l.d}" fill="none" stroke="${coat}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>` +
      `<circle cx="${l.hx.toFixed(1)}" cy="${l.hy.toFixed(1)}" r="7" fill="${skin}" stroke="${INK}" stroke-width="2.2"/>` + pin(l.ex.toFixed(1), l.ey.toFixed(1)) + pin(x, -8);
  };
  const legs = piece("M-20,36 h16 v58 h-22 z", coat) + piece("M4,36 h16 v58 h-6 z", coat) +
    `<path d="M-22,92 h22 v6 h-26 z M4,92 h22 v6 h-22 z" fill="${INK}"/>` + pin(-12, 40) + pin(12, 40);
  const lines = [-14, -6, 2, 10, 18].map((x) => `<path d="M${x},-14 l-4,52" stroke="${INK}" stroke-width="1" opacity="0.35"/>`).join("");
  const torso = piece("M-26,-18 Q0,-26 26,-18 L22,40 Q0,46 -22,40 Z", coat) + lines;
  // head in profile: skull, big nose, chin; the jaw is its own piece and drops open
  const skull = `M${-18 * f},-90 Q${6 * f},-104 ${22 * f},-84 L${24 * f},-74 L${36 * f},-66 L${24 * f},-62 L${22 * f},-56 Q${0},-48 ${-18 * f},-56 Q${-26 * f},-74 ${-18 * f},-90 Z`;
  const open = mood === "eager" ? 16 : mood === "smile" ? 4 : 0;
  const jaw = `<g transform="rotate(${open * f} ${-10 * f} -56)">${piece(`M${-12 * f},-58 L${22 * f},-58 Q${20 * f},-40 ${0},-40 Q${-12 * f},-44 ${-12 * f},-58 Z`, skin)}</g>`;
  const eye = `<circle cx="${10 * f}" cy="-76" r="3.4" fill="${INK}"/>` + `<path d="${mood === "sad" ? `M${4 * f},-85 L${16 * f},-81` : mood === "eager" ? `M${3 * f},-86 q${7 * f},-6 ${14 * f},0` : `M${3 * f},-83 h${14 * f}`}" stroke="${INK}" stroke-width="3" stroke-linecap="round" fill="none"/>`;
  const smile = mood === "smile" ? `<path d="M${4 * f},-58 q${8 * f},5 ${16 * f},-2" fill="none" stroke="${INK}" stroke-width="2.4"/>` : mood === "sad" ? `<path d="M${6 * f},-56 q${7 * f},-5 ${14 * f},1" fill="none" stroke="${INK}" stroke-width="2.4"/>` : "";
  const hat = o.hair === 1
    ? piece(`M${-28 * f},-82 Q${0},-120 ${26 * f},-90 Q${8 * f},-96 ${-28 * f},-82 Z`, "#7A3E3A")
    : o.hair === 2
      ? piece(`M${-26 * f},-90 h${52 * f} v6 h${-52 * f} z M${-16 * f},-90 q${16 * f},-24 ${32 * f},0 z`, INK)
      : piece(`M${-28 * f},-92 h${56 * f} v6 h${-56 * f} z M${-16 * f},-92 v-26 h${32 * f} v26 z`, INK);
  const mustache = t % 2 === 0 && o.hair !== 1 ? `<path d="M${18 * f},-60 q${8 * f},4 ${14 * f},-2 q${-6 * f},8 ${-14 * f},2 z" fill="${INK}"/>` : "";
  return `<g class="puppet">${legs}${torso}<circle cx="0" cy="10" r="7" fill="${lightFill(o)}" stroke="${INK}" stroke-width="2.2"/>` +
    piece("M-6,-26 h12 v10 h-12 z", skin) + piece(skull, skin) + jaw + eye + smile + mustache + hat + pin(0, -22) +
    armPiece(-24, la) + armPiece(24, ra) + "</g>";
}

// ── 4. Sitcom people: an original TV-cartoon design (big heads and eyes, clear silhouettes) ──
// Borrows the principles, not any show's look: real skin tones, no overbite, eyes inside the face.
const SHIRTS = ["#9FB2C6", "#C98F6B", "#8FA58C", "#B7A2C9"];
function glove(x, y) {
  return `<g transform="translate(${x.toFixed(1)},${y.toFixed(1)})"><rect x="-6" y="-12" width="12" height="6" rx="2" fill="#FFF" stroke="${INK}" stroke-width="2.2"/>` +
    `<circle cx="0" cy="0" r="9" fill="#FFF" stroke="${INK}" stroke-width="2.6"/><path d="M-3,2 v6 M1,3 v6 M5,2 v5" stroke="${INK}" stroke-width="1.6" stroke-linecap="round"/></g>`;
}
export function sitcomPerson(o = {}) {
  const t = (o.tone || 0) % 4, skin = TONES[t], shirt = SHIRTS[t];
  const mood = moodOf(o);
  const dir = o.look === "right" ? 1 : o.look === "left" ? -1 : 0;
  const [la, ra] = o.arms || [[20, 10], [-20, -10]];
  const hx = dir * 3, hy = -50, R = 34;
  const arm = (x, a) => {
    const l = limb(x, -2, a[0], a[1], 22);
    return `<path d="${l.d}" fill="none" stroke="${skin}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><path d="${l.d}" fill="none" stroke="${INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" opacity="0.55"/>` +
      `<circle cx="${l.ex.toFixed(1)}" cy="${l.ey.toFixed(1)}" r="3.6" fill="${PAPER}" stroke="${INK}" stroke-width="2"/>` + glove(l.hx, l.hy);
  };
  const leg = (x) => `<path d="M${x},44 L${x},70 L${x},92" fill="none" stroke="#3A3F4A" stroke-width="11" stroke-linecap="round"/><circle cx="${x}" cy="70" r="3.6" fill="${PAPER}" stroke="${INK}" stroke-width="2"/><ellipse cx="${x + (x < 0 ? -5 : 5)}" cy="97" rx="12" ry="6" fill="${INK}"/>`;
  const body = o.hair === 1
    ? `<path d="M-18,-14 Q0,-20 18,-14 L30,46 Q0,52 -30,46 Z" fill="${shirt}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>`
    : `<path d="M-22,-14 Q0,-20 22,-14 L24,46 L-24,46 Z" fill="${shirt}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/><path d="M-24,30 H24 L24,46 L-24,46 Z" fill="#3A3F4A" stroke="${INK}" stroke-width="3"/><path d="M-9,-16 l9,9 l9,-9" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
  const hair = o.hair === 1
    ? `<path d="M${hx - 40},${hy + 10} Q${hx - 46},${hy - 52} ${hx},${hy - 50} Q${hx + 46},${hy - 52} ${hx + 40},${hy + 10} Q${hx + 30},${hy - 20} ${hx},${hy - 26} Q${hx - 30},${hy - 20} ${hx - 40},${hy + 10} Z" fill="#8A3B2E" stroke="${INK}" stroke-width="3"/>`
    : o.hair === 2
      ? `<path d="M${hx - 30},${hy - 16} Q${hx - 10},${hy - 40} ${hx + 26},${hy - 22}" fill="none" stroke="${INK}" stroke-width="4" stroke-linecap="round"/><path d="M${hx - 34},${hy - 2} q-4,-12 2,-20 M${hx + 34},${hy - 2} q4,-12 -2,-20" fill="none" stroke="#7A7A7A" stroke-width="6" stroke-linecap="round"/>`
      : `<path d="M${hx - 32},${hy - 12} Q${hx - 30},${hy - 44} ${hx + 4},${hy - 46} Q${hx + 40},${hy - 50} ${hx + 30},${hy - 20} Q${hx + 14},${hy - 34} ${hx - 32},${hy - 12} Z" fill="#2E2620" stroke="${INK}" stroke-width="3"/>`;
  const eye = (k) => {
    const ex = hx + k * 14 + dir * 4, ey = hy - 6;
    const lid = mood === "sad" ? `<path d="M${ex - 12},${ey - 6} Q${ex},${ey - 16} ${ex + 12},${ey - 6} L${ex + 12},${ey - 12} L${ex - 12},${ey - 12} Z" fill="${skin}" stroke="${INK}" stroke-width="2.4"/>` : mood === "flat" ? `<path d="M${ex - 12},${ey - 3} H${ex + 12} V${ey - 13} H${ex - 12} Z" fill="${skin}" stroke="${INK}" stroke-width="2.4"/>` : "";
    return `<circle cx="${ex}" cy="${ey}" r="12" fill="#FFF" stroke="${INK}" stroke-width="2.8"/><circle cx="${ex + dir * 5}" cy="${ey + (mood === "sad" ? 3 : 1)}" r="4.5" fill="${INK}"/>` + lid;
  };
  const brows = {
    eager: `M${hx - 26},${hy - 28} q10,-10 20,-3 M${hx + 26},${hy - 28} q-10,-10 -20,-3`,
    smile: `M${hx - 25},${hy - 23} q9,-5 18,0 M${hx + 25},${hy - 23} q-9,-5 -18,0`,
    sad: `M${hx - 25},${hy - 18} L${hx - 7},${hy - 26} M${hx + 25},${hy - 18} L${hx + 7},${hy - 26}`,
    flat: `M${hx - 25},${hy - 21} h17 M${hx + 25},${hy - 21} h-17`,
  }[mood];
  const mx = hx + dir * 6, my = hy + 18;
  const mouth = {
    eager: `<path d="M${mx - 10},${my - 3} Q${mx},${my + 18} ${mx + 10},${my - 3} Z" fill="${INK}"/><path d="M${mx - 5},${my + 6} q5,4 10,0" fill="${WAR}" opacity="0.85"/>`,
    smile: `<path d="M${mx - 14},${my - 4} Q${mx},${my + 12} ${mx + 14},${my - 4} Z" fill="${INK}"/><path d="M${mx - 11},${my - 3} H${mx + 11} L${mx + 9},${my + 1} H${mx - 9} Z" fill="#FFF"/>`,
    sad: `<path d="M${mx - 10},${my + 4} Q${mx},${my - 5} ${mx + 10},${my + 4}" fill="none" stroke="${INK}" stroke-width="3.2" stroke-linecap="round"/>`,
    flat: `<path d="M${mx - 9},${my} h18" stroke="${INK}" stroke-width="3.2" stroke-linecap="round"/>`,
  }[mood];
  return `<g class="sitcom">${leg(-12)}${leg(12)}${body}<circle cx="0" cy="12" r="7.5" fill="${lightFill(o)}" stroke="${INK}" stroke-width="2.6"/>` +
    `<rect x="-7" y="-20" width="14" height="10" fill="${skin}" stroke="${INK}" stroke-width="2.4"/>` +
    `<ellipse cx="${hx - R + 1}" cy="${hy + 4}" rx="7" ry="9" fill="${skin}" stroke="${INK}" stroke-width="2.6"/><ellipse cx="${hx + R - 1}" cy="${hy + 4}" rx="7" ry="9" fill="${skin}" stroke="${INK}" stroke-width="2.6"/>` +
    `<ellipse cx="${hx}" cy="${hy}" rx="${R}" ry="${R + 2}" fill="${skin}" stroke="${INK}" stroke-width="3.6"/>` + hair +
    eye(-1) + eye(1) + `<path d="${brows}" fill="none" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>` +
    `<ellipse cx="${hx + dir * 9}" cy="${hy + 6}" rx="5" ry="4" fill="${skin}" stroke="${INK}" stroke-width="2.2"/>` + mouth +
    arm(-22, la) + arm(22, ra) + "</g>";
}

// ── 5. Stick figures with hats: line bodies, round heads, character told by hat and pose ──
export function stickFigure(o = {}) {
  const t = (o.tone || 0) % 4;
  const mood = moodOf(o);
  const dir = o.look === "right" ? 1 : o.look === "left" ? -1 : 0;
  const [la, ra] = o.arms || [[20, 10], [-20, -10]];
  const hx = 0, hy = -56, R = 22;
  const line = (d, w = 6) => `<path d="${d}" fill="none" stroke="${INK}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
  const joint = (x, y) => `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4" fill="${PAPER}" stroke="${INK}" stroke-width="2.4"/>`;
  const arm = (a) => { const l = limb(0, -24, a[0], a[1], 26); return line(l.d) + joint(l.ex, l.ey); };
  const leg = (s) => { const l = limb(0, 30, 18 * s, 6 * s, 34); return line(l.d) + joint(l.ex, l.ey); };
  const hat = o.hair === 2 || t === 0
    ? `<rect x="${hx - 17}" y="${hy - R - 30}" width="34" height="30" rx="2" fill="${INK}"/><rect x="${hx - 17}" y="${hy - R - 9}" width="34" height="5" fill="${WAR}"/><rect x="${hx - 28}" y="${hy - R - 3}" width="56" height="6" rx="3" fill="${INK}"/>`
    : o.hair === 1
      ? `<path d="M${hx - 24},${hy + 4} Q${hx - 28},${hy - 30} ${hx},${hy - 28} Q${hx + 28},${hy - 30} ${hx + 24},${hy + 4} Q${hx + 18},${hy - 14} ${hx},${hy - 16} Q${hx - 18},${hy - 14} ${hx - 24},${hy + 4} Z" fill="${INK}"/>`
      : t === 2
        ? `<path d="M${hx - 26},${hy - R + 4} Q${hx},${hy - R - 26} ${hx + 26},${hy - R + 4} Z" fill="#E4B24A" stroke="${INK}" stroke-width="3"/><rect x="${hx - 30}" y="${hy - R + 1}" width="60" height="6" rx="3" fill="#E4B24A" stroke="${INK}" stroke-width="2.4"/>`
        : `<path d="M${hx - 18},${hy - R + 2} Q${hx},${hy - R - 22} ${hx + 18},${hy - R + 2} Z" fill="${INK}"/><rect x="${hx - 27}" y="${hy - R}" width="54" height="5" rx="2.5" fill="${INK}"/>`;
  const ex = (k) => hx + k * 8 + dir * 6;
  const eyes = mood === "eager" ? `<circle cx="${ex(-1)}" cy="${hy - 2}" r="4.4" fill="${INK}"/><circle cx="${ex(1)}" cy="${hy - 2}" r="4.4" fill="${INK}"/>` : `<circle cx="${ex(-1)}" cy="${hy - 2}" r="3.2" fill="${INK}"/><circle cx="${ex(1)}" cy="${hy - 2}" r="3.2" fill="${INK}"/>`;
  const brows = {
    eager: `M${ex(-1) - 5},${hy - 12} q5,-5 10,0 M${ex(1) - 5},${hy - 12} q5,-5 10,0`,
    smile: "",
    sad: `M${ex(-1) - 5},${hy - 8} L${ex(-1) + 4},${hy - 12} M${ex(1) + 5},${hy - 8} L${ex(1) - 4},${hy - 12}`,
    flat: `M${ex(-1) - 5},${hy - 9} h10 M${ex(1) - 5},${hy - 9} h10`,
  }[mood];
  const mx = hx + dir * 6, my = hy + 9;
  const mouth = {
    eager: `<ellipse cx="${mx}" cy="${my + 1}" rx="5" ry="6" fill="${INK}"/>`,
    smile: `<path d="M${mx - 9},${my - 2} q9,9 18,0" fill="none" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>`,
    sad: `<path d="M${mx - 8},${my + 3} q8,-6 16,0" fill="none" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>`,
    flat: `<path d="M${mx - 7},${my} h14" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>`,
  }[mood];
  const stache = t === 0 && o.hair !== 1 ? `<path d="M${mx - 10},${my - 4} q5,-5 10,0 q5,-5 10,0 q-10,5 -20,0 z" fill="${INK}"/>` : "";
  return `<g class="stick">` + line(`M0,${hy + R} L0,30`) + leg(-1) + leg(1) + arm(la) + arm(ra) +
    `<circle cx="0" cy="-6" r="7" fill="${lightFill(o)}" stroke="${INK}" stroke-width="2.6"/>` +
    `<circle cx="${hx}" cy="${hy}" r="${R}" fill="${PAPER}" stroke="${INK}" stroke-width="5"/>` + eyes +
    (brows ? `<path d="${brows}" fill="none" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>` : "") + mouth + stache + hat + "</g>";
}

// A close-up lineup: four humans large enough to judge, one per mood.
const LINEUP = [
  { label: "SMILE", o: { tone: 0, hair: 0, mood: "smile", look: "camera", light: "off" } },
  { label: "EAGER, LOOKING RIGHT", o: { tone: 1, hair: 1, mood: "eager", look: "right", light: "off", arms: [[30, 30], [60, 70]] } },
  { label: "SAD", o: { tone: 2, hair: 2, mood: "sad", light: "red", arms: [[10, 5], [-10, -5]] } },
  { label: "FLAT", o: { tone: 3, hair: 0, mood: "flat", light: "teal", arms: [[25, 60], [-25, -60]] } },
];
function closeUp(H, id) {
  const { K } = H;
  const figures = LINEUP.map(({ label, o }, i) => H.at(300 + i * 440, 640, 3.1, K.bean(o)) + H.label(300 + i * 440, 1000, 30, label)).join("");
  return { svg: K.paper(id) + H.label(960, 130, 40, "CLOSE-UP: FOUR MOODS") + figures, alt: "Four humans drawn large: smiling, eager and looking right, sad with a red chest light, and flat." };
}

// One comparison module per design, redrawing the two Part 1 scenes with that human.
export function variant(label, notes, drawer) {
  const swap = (draw) => (H, id) => draw({ ...H, K: { ...H.K, bean: drawer } }, id);
  return {
    label, notes,
    pageTitle: "Human Design Options",
    currentLabel: "Current: beans",
    dek: "Each candidate design for the humans, drawn large in four moods, then in two Part 1 scenes: the family portrait, where they must still feel like people, and the crowd snapping toward the paper, where they must be funny.",
    extras: { "close-up": { key: "four moods, large enough to judge the faces", draw: swap(closeUp), current: closeUp } },
    scenes: { "loved-ones": swap(base["loved-ones"]), "papers-with-presidents": swap(base["papers-with-presidents"]) },
  };
}
