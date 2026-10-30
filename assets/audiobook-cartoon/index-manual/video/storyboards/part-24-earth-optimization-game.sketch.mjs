// Sketches for storyboards/part-24-earth-optimization-game.md: each scene's key moment on a 1920 x 1080 frame (16:9),
// in the film look (Part 2 is the reference). Host shots use H.host (KIT.STUDIO, 16:9: the lectern's reading top at
// y 790, x 540 to 980; the free wall right of it, x 1100 to 1880). The game-board plate is drawn once, in plate units
// (the humans at scale 1.5, as in Part 2), and each plate frame is a view of it as the camera sees it at that moment.
// Captions keep-out: below y 900. Built into the review sheet by tools/storyboard-sheet.mjs.

const f = (n) => n.toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});
// A plate framing as KIT.camera places it: plate point (x, y) in the middle of the frame, at scale s.
const view = (x, y, s, inner) => `<g transform="translate(${f(960 - x * s)},${f(540 - y * s)}) scale(${s})">${inner}</g>`;
const at = (x, y, k, inner, rot = 0) => `<g transform="translate(${f(x)},${f(y)})${rot ? ` rotate(${rot})` : ""} scale(${k})">${inner}</g>`;
// A person standing with its feet on y (plate or canvas units) at scale k.
const stand = (K, o, x, y, k) => at(x, y - 100 * k, k, K.person(o));

const FIELD = "#C8B07B", BOARD = "#F1E6C6", WHITE = "#FBF6E6", GLOW = "#D7EBC2";

// ── The cast of this part (the same options in every scene) ──
const YOU = { tone: 2, outfit: "suit", hat: "bowler" };
const HOLDERS = [
  { tone: 0, outfit: "dress", color: 0, hair: 1, seed: 4 },
  { tone: 3, outfit: "overalls", color: 1, seed: 6 },
  { tone: 1, outfit: "shirt", kind: "twig", color: 3, seed: 2 },
];
const FRIENDS = [
  { tone: 2, outfit: "dress", color: 3, hair: 1, seed: 8 },
  { tone: 1, outfit: "overalls", kind: "barrel", color: 2, seed: 9 },
];
const CRATE_MAN = { tone: 0, outfit: "suit", kind: "box", color: 1, mood: "smug", seed: 5 };

// ── Shared drawings ──
// The point chip: a mustard game chip with a notched cream rim and a navy star, r across its radius.
function chip(K, C, x, y, r, rot = 0) {
  return `<g transform="translate(${f(x)},${f(y)}) rotate(${rot})"><circle r="${r}" fill="${C.yellow}" stroke="${C.ink}" stroke-width="${f(Math.max(2, r * 0.16))}"/>` +
    `<circle r="${f(r * 0.78)}" fill="none" stroke="${C.cream}" stroke-width="${f(r * 0.2)}" stroke-dasharray="${f(r * 0.42)} ${f(r * 0.42)}"/>` +
    `<circle r="${f(r * 0.6)}" fill="none" stroke="${C.ink}" stroke-width="${f(Math.max(1, r * 0.06))}"/>` + K.star(0, 0, r * 0.5, C.navy, 5) + "</g>";
}
// The Scoreboard (Part 23's): its posts stand on (x, base); rolling: the digits blurred mid-roll.
function scoreboard(K, C, x, base, o = {}) {
  const w = 820, h = 400, top = base - 120 - h, lit = o.lit !== false;
  let out = [-280, 280].map((dx) => `<rect x="${x + dx - 14}" y="${top + h - 10}" width="28" height="${base - top - h + 10}" fill="${C.slate}" stroke="${C.ink}" stroke-width="5"/>`).join("");
  out += `<rect x="${x - w / 2}" y="${top}" width="${w}" height="${h}" fill="${C.navy}" stroke="${C.ink}" stroke-width="7"/>` +
    `<rect x="${x - w / 2 + 14}" y="${top + 14}" width="${w - 28}" height="${h - 28}" fill="none" stroke="${C.orange}" stroke-width="7"/>`;
  for (let bx = x - w / 2 + 44; bx < x + w / 2 - 20; bx += 46) {
    out += (lit ? `<circle cx="${bx}" cy="${top + 42}" r="20" fill="${C.yellow}" opacity="0.35"/>` : "") +
      `<circle cx="${bx}" cy="${top + 42}" r="11" fill="${lit ? C.yellow : C.slate}" stroke="${C.ink}" stroke-width="3"/>`;
  }
  const win = (cx, num, unit) => {
    const wx = cx - 170, wy = top + 82, ww = 340, wh = 280;
    let digits = "";
    if (o.rolling) {
      digits = [-150, -75, 0, 75, 150].map((dy, i) => `<text x="${cx}" y="${wy + 170 + dy}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="104" fill="${C.ink}" opacity="${[0.18, 0.4, 0.7, 0.4, 0.18][i]}">${num}</text>`).join("") +
        [-110, -40, 40, 110].map((dx) => `<path d="M${cx + dx},${wy + 30} V${wy + wh - 70}" stroke="${C.ink}" stroke-width="3" opacity="0.25"/>`).join("");
    } else {
      digits = `<text x="${cx}" y="${wy + 170}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="104" fill="${C.ink}">${num}</text>`;
    }
    return `<defs><clipPath id="${o.fid}-sw${cx}"><rect x="${wx}" y="${wy}" width="${ww}" height="${wh - 56}"/></clipPath></defs>` +
      `<rect x="${wx}" y="${wy}" width="${ww}" height="${wh}" fill="${C.cream}" stroke="${C.ink}" stroke-width="6"/>` +
      `<g clip-path="url(#${o.fid}-sw${cx})">${digits}</g><path d="M${wx},${wy + 112} H${wx + ww}" stroke="${C.ink}" stroke-width="2.5" opacity="0.6"/>` +
      `<rect x="${cx - 52}" y="${wy + wh - 50}" width="104" height="38" fill="${WHITE}" stroke="${C.ink}" stroke-width="3"/>` +
      `<text x="${cx}" y="${wy + wh - 21}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="28" letter-spacing="1.5" fill="${C.ink}">${unit}</text>`;
  };
  return out + win(x - 200, "63.3", "YRS") + win(x + 200, "$2,138", "/YR");
}
// The tear-off calendar on its post, standing on (x, base), its top page the year.
function calendar(C, x, base, year) {
  const w = 230, top = base - 360;
  return `<rect x="${x - 12}" y="${top + 200}" width="24" height="${base - top - 200}" fill="${C.slate}" stroke="${C.ink}" stroke-width="5"/>` +
    `<rect x="${x - w / 2 - 12}" y="${top}" width="${w + 24}" height="${230}" fill="${C.slate}" stroke="${C.ink}" stroke-width="5"/>` +
    `<rect x="${x - w / 2}" y="${top + 26}" width="${w}" height="${190}" fill="${WHITE}" stroke="${C.ink}" stroke-width="4"/>` +
    `<rect x="${x - w / 2}" y="${top + 26}" width="${w}" height="46" fill="${C.war}" stroke="${C.ink}" stroke-width="4"/>` +
    [-50, 50].map((dx) => `<rect x="${x + dx - 8}" y="${top + 8}" width="16" height="34" rx="6" fill="${C.cream}" stroke="${C.ink}" stroke-width="3"/>`).join("") +
    `<text x="${x}" y="${top + 176}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="92" fill="${C.ink}">${year}</text>`;
}
// The box: orange walls round the cream board, the track of squares round its edge, the corner squares.
// o.front: draw the front wall (with the roundel); o.blobs: the three disease blobs on DISEASES (default true).
const BX = 1200, BY = 700, RING = 240;
function board(K, C, o = {}) {
  const ink = C.ink, cols = [C.orange, C.yellow, C.peri, C.rust];
  let out = `<rect x="${-BX - 60}" y="${-BY - 60}" width="${2 * BX + 120}" height="${2 * BY + 120}" fill="${C.orange}" stroke="${ink}" stroke-width="7"/>` +
    `<rect x="${-BX}" y="${-BY}" width="${2 * BX}" height="${2 * BY}" fill="${BOARD}" stroke="${ink}" stroke-width="6"/>`;
  // stars on the side and back walls
  for (let x = -BX + 60; x < BX; x += 240) out += K.star(x, -BY - 30, 14, C.yellow, 4);
  for (let y = -BY + 120; y < BY; y += 240) out += K.star(-BX - 30, y, 14, C.yellow, 4) + K.star(BX + 30, y, 14, C.yellow, 4);
  // the track: the back and front rows, then the two sides
  let n = 0;
  const sq = (x, y, w, h) => `<rect x="${f(x)}" y="${f(y)}" width="${f(w)}" height="${f(h)}" fill="${cols[n++ % 4]}" stroke="${ink}" stroke-width="4"/>`;
  const inner = 2 * BX - 2 * RING, cw = inner / 12, ch = (2 * BY - 2 * RING) / 6;
  for (let i = 0; i < 12; i++) out += sq(-BX + RING + i * cw, -BY, cw, RING) + sq(-BX + RING + i * cw, BY - RING, cw, RING);
  for (let i = 0; i < 6; i++) out += sq(-BX, -BY + RING + i * ch, RING, ch) + sq(BX - RING, -BY + RING + i * ch, RING, ch);
  out += `<rect x="${-BX + RING}" y="${-BY + RING}" width="${inner}" height="${2 * BY - 2 * RING}" fill="${BOARD}" stroke="${ink}" stroke-width="4"/>` +
    `<rect x="${-BX + RING + 18}" y="${-BY + RING + 18}" width="${inner - 36}" height="${2 * BY - 2 * RING - 36}" fill="none" stroke="${C.orange}" stroke-width="3"/>`;
  // corners: START (front left), WAR (back left), DISEASES (back right), a star (front right)
  const corner = (x, y, fill) => `<rect x="${x}" y="${y}" width="${RING}" height="${RING}" fill="${fill}" stroke="${ink}" stroke-width="5"/>`;
  out += corner(-BX, BY - RING, C.yellow) + `<text x="${-BX + RING / 2}" y="${BY - RING / 2 + 22}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="62" letter-spacing="3" fill="${ink}">START</text>`;
  out += corner(-BX, -BY, o.warBurnt ? "#3A2A22" : C.rust) + `<circle cx="${-BX + RING / 2}" cy="${-BY + RING / 2}" r="86" fill="${o.warBurnt ? "#4A372C" : "#B0603C"}" stroke="${ink}" stroke-width="3"/>` +
    at(-BX + RING / 2, -BY + RING / 2 + 62, 0.72, o.warBurnt ? K.burn(K.props.missile({ mood: "grin", arms: "none" })) : K.props.missile({ mood: "grin", arms: "none" }));
  out += corner(BX - RING, -BY, C.slate) + corner(BX - RING, BY - RING, C.yellow) + K.star(BX - RING / 2, BY - RING / 2, 70, C.orange, 4);
  if (o.blobs !== false) {
    out += at(BX - 175, -BY + 205, 0.7, K.props.diseaseBlob({ seed: 2, color: "peri" })) + at(BX - 70, -BY + 150, 0.62, K.props.diseaseBlob({ seed: 5, color: "orange" })) +
      at(BX - 95, -BY + 228, 0.74, K.props.diseaseBlob({ seed: 8, color: "rust" }));
  }
  return out;
}
// The front wall, standing, facing the camera, with the roundel.
function frontWall(K, C) {
  const y = BY + 20, h = 110;
  let out = `<rect x="${-BX - 60}" y="${y}" width="${2 * BX + 120}" height="${h}" fill="${C.orange}" stroke="${C.ink}" stroke-width="7"/>` +
    `<rect x="${-BX - 46}" y="${y + 14}" width="${2 * BX + 92}" height="${h - 28}" fill="none" stroke="${C.ink}" stroke-width="3"/>`;
  for (let x = -BX + 40; x < BX; x += 200) if (Math.abs(x) > 220) out += K.star(x, y + h / 2, 16, C.yellow, 4);
  return out + roundel(C, 0, y + h / 2, 0.95);
}
// The mustard roundel, a 1950s starburst: "FOR 2 TO / 4,000,000,000 / PLAYERS".
function roundel(C, x, y, k, rot = -8) {
  let pts = [];
  for (let i = 0; i < 32; i++) { const a = (i * Math.PI) / 16, r = i % 2 ? 88 : 100; pts.push(`${f(r * Math.cos(a))},${f(r * Math.sin(a) * 0.92)}`); }
  const t = (ty, s, txt) => `<text x="0" y="${ty}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="${s}" letter-spacing="1" fill="${C.ink}">${txt}</text>`;
  return `<g transform="translate(${f(x)},${f(y)}) rotate(${rot}) scale(${k})"><polygon points="${pts.join(" ")}" fill="${C.yellow}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    `<ellipse rx="74" ry="68" fill="none" stroke="${C.orange}" stroke-width="3"/>` + t(-22, 22, "FOR 2 TO") + t(10, 25, "4,000,000,000") + t(40, 22, "PLAYERS") + "</g>";
}
// The pool of money: a kidney-shaped 1950s pool in the middle of the board, full of medicine money.
const KIDNEY = "M-500,-40 C-500,-200 -280,-230 -80,-170 C100,-115 230,-225 400,-205 C560,-185 570,160 390,200 C170,245 -30,140 -240,195 C-470,250 -500,90 -500,-40 Z";
const POOL_X = 40;
function pool(K, C, fid, o = {}) {
  const ink = C.ink;
  const pat = `<defs><pattern id="${fid}-bills" width="150" height="104" patternUnits="userSpaceOnUse">` +
    `<rect width="150" height="104" fill="${C.moneyEdge}"/>` + at(40, 28, 0.78, K.money("med"), -9) + at(112, 78, 0.78, K.money("med"), 11) + at(118, 12, 0.6, K.money("med"), 24) + at(26, 92, 0.6, K.money("med"), -20) +
    `</pattern><clipPath id="${fid}-poolclip"><path d="${KIDNEY}"/></clipPath></defs>`;
  let out = pat + `<g transform="translate(${POOL_X},0)">` +
    `<path d="${KIDNEY}" fill="none" stroke="${ink}" stroke-width="52"/><path d="${KIDNEY}" fill="none" stroke="${WHITE}" stroke-width="40"/>` +
    `<path d="${KIDNEY}" fill="url(#${fid}-bills)" stroke="${ink}" stroke-width="5"/>`;
  // the diving board on the left end, the chrome ladder on the right
  out += `<path d="M-650,-70 L-430,-92 L-428,-58 L-648,-36 Z" fill="${WHITE}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    `<rect x="-680" y="-80" width="50" height="60" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` +
    `<path d="M520,-120 q34,-30 34,14 V40 M562,-90 q34,-30 34,14 V60" fill="none" stroke="${ink}" stroke-width="13"/><path d="M520,-120 q34,-30 34,14 V40 M562,-90 q34,-30 34,14 V60" fill="none" stroke="#D9DEE6" stroke-width="7"/>`;
  if (o.split) {
    out += `<g clip-path="url(#${fid}-poolclip)">` + [-170, 200].map((x) => `<path d="M${x - 40},-260 L${x + 40},260" stroke="${WHITE}" stroke-width="22"/><path d="M${x - 40},-260 L${x + 40},260" stroke="${ink}" stroke-width="9" stroke-dasharray="34 22"/>`).join("") + "</g>";
  }
  return out + "</g>";
}
// A crown of medicine bills flying up out of the pool at (x, y).
function splash(K, C, x, y, k = 1) {
  const fly = [[-120, -40, -60], [-80, -120, -30], [0, -160, 4], [84, -120, 34], [124, -36, 64], [-40, -70, -16], [44, -76, 18]];
  return `<g transform="translate(${f(x)},${f(y)}) scale(${k})">` +
    `<path d="M-130,10 Q-150,-60 -100,-40 Q-80,-110 -40,-60 Q0,-140 40,-60 Q80,-110 100,-40 Q150,-60 130,10 Z" fill="${C.money}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="round"/>` +
    fly.map(([dx, dy, r]) => at(dx, dy, 0.62, K.money("med"), r)).join("") + "</g>";
}
// A piggy bank (no pink): body length L, color, standing on (x, y), facing right; dress: extra markup on its head.
function piggy(C, x, y, L, col, o = {}) {
  const ink = C.ink, h = L * 0.62, k = L / 200;
  const P = (pts) => pts.map(([px, py]) => `${f(x + px * k)},${f(y + py * k)}`).join(" ");
  const legs = [[-62, 0], [-30, 0], [30, 0], [62, 0]].map(([lx]) => `<polygon points="${P([[lx - 11, -30], [lx + 11, -30], [lx + 9, 0], [lx - 9, 0]])}" fill="${col}" stroke="${ink}" stroke-width="${f(4 * Math.sqrt(k))}"/>`).join("");
  const body = `<polygon points="${P([[-96, -64], [-80, -108], [-30, -128], [40, -126], [86, -104], [102, -70], [96, -36], [60, -22], [-60, -22], [-92, -36]])}" fill="${col}" stroke="${ink}" stroke-width="${f(5 * Math.sqrt(k))}" stroke-linejoin="miter"/>`;
  const snout = `<polygon points="${P([[96, -90], [124, -88], [126, -60], [98, -58]])}" fill="${col}" stroke="${ink}" stroke-width="${f(4 * Math.sqrt(k))}"/>` +
    `<circle cx="${f(x + 113 * k)}" cy="${f(y - 80 * k)}" r="${f(3.5 * k)}" fill="${ink}"/><circle cx="${f(x + 113 * k)}" cy="${f(y - 68 * k)}" r="${f(3.5 * k)}" fill="${ink}"/>`;
  const ear = `<polygon points="${P([[50, -122], [62, -150], [76, -114]])}" fill="${col}" stroke="${ink}" stroke-width="${f(4 * Math.sqrt(k))}"/>`;
  const eye = o.dead ? `<path d="M${f(x + 70 * k)},${f(y - 104 * k)} l${f(12 * k)},${f(12 * k)} M${f(x + 82 * k)},${f(y - 104 * k)} l${f(-12 * k)},${f(12 * k)}" stroke="${ink}" stroke-width="${f(3 * k)}"/>` :
    `<ellipse cx="${f(x + 74 * k)}" cy="${f(y - 98 * k)}" rx="${f(7 * k)}" ry="${f(5 * k)}" fill="${WHITE}" stroke="${ink}" stroke-width="${f(2.5 * k)}"/><circle cx="${f(x + 76 * k)}" cy="${f(y - 98 * k)}" r="${f(2.6 * k)}" fill="${ink}"/>`;
  const slot = `<rect x="${f(x - 26 * k)}" y="${f(y - 132 * k)}" width="${f(46 * k)}" height="${f(9 * k)}" fill="${ink}"/>`;
  const tail = `<path d="M${f(x - 96 * k)},${f(y - 70 * k)} q${f(-26 * k)},${f(-8 * k)} ${f(-18 * k)},${f(-26 * k)} q${f(12 * k)},${f(-12 * k)} ${f(-24 * k)},${f(-4 * k)}" fill="none" stroke="${ink}" stroke-width="${f(4 * k)}"/>`;
  return legs + tail + body + ear + snout + eye + slot + (o.dress || "");
}
// The GREED arrow (Part 21's) on its riveted post: the post stands on (x, base), the arrow pivots at its top.
function greedArrow(C, x, base, angle, post = 180) {
  const ink = C.ink, py = base - post;
  const postSvg = `<rect x="${x - 16}" y="${py}" width="32" height="${post}" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` +
    `<rect x="${x - 40}" y="${base - 16}" width="80" height="22" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` +
    [0.3, 0.6].map((u) => `<circle cx="${x}" cy="${f(py + post * u)}" r="4" fill="${C.cream}"/>`).join("");
  const arrow = `<g transform="translate(${x},${py}) rotate(${angle})">` +
    `<path d="M-300,-26 L-250,-26 L-270,0 L-250,26 L-300,26 L-282,0 Z" fill="${C.orange}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    `<path d="M-262,-22 H190 V-52 L300,0 L190,52 V22 H-262 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
    `<path d="M-258,16 H190 V46 L292,2" fill="none" stroke="${C.orange}" stroke-width="6"/>` +
    `<text x="-130" y="16" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="46" letter-spacing="4" fill="${ink}">GREED</text>` +
    `<circle r="13" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><circle r="4" fill="${C.cream}"/></g>`;
  return postSvg + arrow;
}
// Little stick legs (navy, pointed shoes) under a building standing on (x, y): w apart, h tall; lift raises one foot.
function stickLegs(C, x, y, w, h, lift = 0) {
  return [-1, 1].map((s) => {
    const lx = x + s * w / 2, up = s > 0 ? lift : 0;
    return `<path d="M${lx},${y - h} L${lx + s * 6},${y - up}" stroke="${C.ink}" stroke-width="9" stroke-linecap="round"/>` +
      `<path d="M${lx + s * 6 - 14},${y - up} L${lx + s * 6 + 26},${y - up - 4} L${lx + s * 6 + 18},${y - up + 8} L${lx + s * 6 - 14},${y - up + 8} Z" fill="${C.ink}"/>`;
  }).join("");
}
// The game box on its boomerang side table (game-box, your-job): the table's top at y 800, centered on tx, its legs
// running off the bottom of the frame. o.open: the new lid lifted clean off and hanging tilted above the box; under
// it, still on the box, Part 7's old lid (orange, a cream inner border, OBJECTIVE: / LOSE, as lose-elaborately draws
// it), its front edge pushed up a crack by three medicine bills peeking out, pale green light spilling out. Otherwise
// the new lid is shut; o.kicker: a binder's stick legs kicking out from under it.
function gameBox(K, C, fid, tx, o = {}) {
  const ink = C.ink;
  const table = `<path d="M${tx - 300},800 L${tx - 250},770 L${tx + 290},776 L${tx + 330},806 L${tx + 270},830 L${tx - 270},828 Z" fill="${C.tan}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
    `<path d="M${tx - 270},828 L${tx + 270},830 L${tx + 330},806" fill="none" stroke="${C.rust}" stroke-width="10"/>` +
    [[-220, -250], [230, 262], [0, 6]].map(([a, b]) => `<path d="M${tx + a - 12},830 L${tx + a + 12},830 L${tx + b + 4},1080 L${tx + b - 4},1080 Z" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>`).join("");
  const bx0 = tx - 250, bx1 = tx + 250;
  // the base: its front face (orange, stars)
  const base = `<rect x="${bx0}" y="718" width="${bx1 - bx0}" height="66" fill="${C.orange}" stroke="${ink}" stroke-width="6"/>` +
    [bx0 + 60, bx0 + 180, bx1 - 180, bx1 - 60].map((x) => K.star(x, 751, 14, C.yellow, 4)).join("");
  let glow = "", bills = "", rays = "";
  if (o.open) {
    glow = `<rect x="${bx0 + 4}" y="676" width="${bx1 - bx0 - 8}" height="44" fill="${GLOW}" stroke="${ink}" stroke-width="4"/>`;
    // pale green light spilling out of the gap at both ends
    rays = [-1, 1].map((sd) => [-34, -8, 18].map((dy) => {
      const x0 = sd < 0 ? bx0 - 10 : bx1 + 10, x1 = x0 + sd * 90;
      return `<path d="M${x0},${690 + dy * 0.2} L${x1},${676 + dy * 1.6} L${x1},${700 + dy * 1.6} Z" fill="${GLOW}" opacity="0.75"/>`;
    }).join("")).join("");
    // three medicine bills peeking up over the base's rim, under the lid
    bills = `<defs><clipPath id="${fid}-peek"><rect x="${bx0}" y="600" width="${bx1 - bx0}" height="120"/></clipPath></defs><g clip-path="url(#${fid}-peek)">` +
      [[-150, 712, -8], [0, 704, 4], [150, 714, 10]].map(([dx, y, r]) => at(tx + dx, y, 0.92, K.money("med"), r)).join("") + "</g>" +
      [-150, 0, 150].map((dx) => `<path d="M${tx + dx - 30},668 q6,-10 12,0 M${tx + dx + 18},668 q6,-10 12,0" fill="none" stroke="${ink}" stroke-width="3"/>`).join("");
  }
  // Part 7's old lid, still on the box under the new one: open, its front edge pushed up a crack by the bills
  let oldLid = "";
  if (o.open) {
    const oT = 512, oB = 652;
    oldLid = `<g transform="rotate(-2 ${tx} ${oB})">` +
      `<rect x="${bx0 - 8}" y="${oB}" width="${bx1 - bx0 + 16}" height="22" fill="${C.orange}" stroke="${ink}" stroke-width="6"/>` +
      `<rect x="${bx0 - 8}" y="${oT}" width="${bx1 - bx0 + 16}" height="${oB - oT}" fill="${C.orange}" stroke="${ink}" stroke-width="6"/>` +
      `<rect x="${bx0 + 10}" y="${oT + 16}" width="${bx1 - bx0 - 20}" height="${oB - oT - 32}" fill="none" stroke="${C.cream}" stroke-width="5"/>` +
      `<text x="${tx}" y="${oT + 64}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="44" letter-spacing="2" fill="${C.navy}">OBJECTIVE:</text>` +
      `<text x="${tx}" y="${oT + 122}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="58" letter-spacing="3" fill="${C.war}">LOSE</text></g>`;
  }
  // the new lid: seen from a little above; open, lifted clean off and hanging tilted above the box; shut, on the base
  const dy = o.open ? -250 : 38, lidTop = 430 + dy, lidBot = 652 + dy;
  const lidSvg = `<g${o.open ? ` transform="rotate(6 ${tx} ${lidBot})"` : ""}>` +
    `<rect x="${bx0 - 14}" y="${lidBot}" width="${bx1 - bx0 + 28}" height="28" fill="${C.cream}" stroke="${ink}" stroke-width="6"/>` +
    `<rect x="${bx0 - 14}" y="${lidTop}" width="${bx1 - bx0 + 28}" height="${lidBot - lidTop}" fill="${C.cream}" stroke="${ink}" stroke-width="6"/>` +
    `<rect x="${bx0 + 2}" y="${lidTop + 14}" width="${bx1 - bx0 - 4}" height="${lidBot - lidTop - 28}" fill="none" stroke="${C.navy}" stroke-width="6"/>` +
    `<rect x="${bx0 + 14}" y="${lidTop + 26}" width="${bx1 - bx0 - 28}" height="${lidBot - lidTop - 52}" fill="none" stroke="${C.orange}" stroke-width="4"/>` +
    K.star(bx0 + 44, lidTop + 54, 13, C.yellow, 4) + K.star(bx0 + 44, lidBot - 54, 13, C.yellow, 4) + K.star(bx1 - 44, lidBot - 54, 13, C.yellow, 4) +
    `<text x="${tx - 10}" y="${lidTop + 92}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="40" fill="${C.navy}">THE EARTH</text>` +
    `<text x="${tx - 10}" y="${lidTop + 152}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="56" fill="${C.navy}">OPTIMIZATION</text>` +
    `<text x="${tx - 10}" y="${lidTop + 208}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="56" fill="${C.war}">GAME</text>` +
    roundel(C, bx1 - 4, lidTop + 6, 0.95, 10) + "</g>";
  // the last binder, caught under the shut lid: its rust cover jutting out over the base's front, spine label "5",
  // and its stick legs kicking
  let binder = "", legs = "";
  if (o.kicker) {
    const kx = tx + 90;
    binder = `<path d="M${kx - 92},${lidBot + 16} L${kx + 92},${lidBot + 6} L${kx + 98},${lidBot + 84} L${kx - 86},${lidBot + 92} Z" fill="${C.rust}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
      `<path d="M${kx - 26},${lidBot + 34} L${kx + 26},${lidBot + 31} L${kx + 28},${lidBot + 78} L${kx - 24},${lidBot + 81} Z" fill="${C.cream}" stroke="${ink}" stroke-width="4"/>` +
      `<text x="${kx + 2}" y="${lidBot + 70}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="36" fill="${ink}">5</text>`;
    const by = lidBot + 88;
    legs = `<path d="M${kx - 44},${by} L${kx - 62},${by + 92}" stroke="${ink}" stroke-width="13" stroke-linecap="round"/>` +
      `<path d="M${kx - 96},${by + 96} L${kx - 64},${by + 84} L${kx - 28},${by + 92} L${kx - 62},${by + 106} Z" fill="${ink}"/>` +
      `<path d="M${kx + 44},${by - 4} L${kx + 92},${by + 36} L${kx + 150},${by + 14}" fill="none" stroke="${ink}" stroke-width="13" stroke-linecap="round" stroke-linejoin="miter"/>` +
      `<path d="M${kx + 140},${by} L${kx + 190},${by - 10} L${kx + 164},${by + 22} L${kx + 142},${by + 28} Z" fill="${ink}"/>` +
      [[kx + 178, by - 34, 22, -10], [kx + 196, by + 6, 24, 4], [kx - 104, by + 70, -22, -6]].map(([x, y, dx, dy]) => `<path d="M${x},${y} l${dx},${dy}" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`).join("");
  }
  // lift lines under the hanging new lid
  const lift = o.open ? [-160, 0, 160].map((dx) => `<path d="M${tx + dx},${lidBot + 70} v40" stroke="${ink}" stroke-width="5" stroke-linecap="round" opacity="0.6"/>`).join("") : "";
  return table + glow + bills + base + binder + oldLid + lidSvg + lift + legs + rays;
}
// A cloud of dust puffs at (x, y), w wide.
function dust(C, x, y, w, seed) {
  let out = "";
  for (let i = 0; i < 9; i++) {
    const u = i / 8, px = x - w / 2 + u * w, py = y - 20 * Math.sin(i * 1.7 + seed), r = 46 + 18 * Math.sin(i * 2.3 + seed);
    out += `<circle cx="${f(px)}" cy="${f(py)}" r="${f(r)}" fill="#E4D6B0" stroke="${C.ink}" stroke-width="4"/>`;
  }
  for (let i = 0; i < 9; i++) {
    const u = i / 8, px = x - w / 2 + u * w, py = y - 20 * Math.sin(i * 1.7 + seed), r = 46 + 18 * Math.sin(i * 2.3 + seed);
    out += `<circle cx="${f(px)}" cy="${f(py)}" r="${f(r - 4)}" fill="#E4D6B0"/>`;
  }
  return out;
}
// Speed lines behind something moving right.
function speed(C, x, y, n = 3, len = 60) {
  let out = "";
  for (let i = 0; i < n; i++) out += `<path d="M${x - len - i * 8},${y + i * 22} h${len}" stroke="${C.ink}" stroke-width="4" stroke-linecap="round" opacity="0.7"/>`;
  return out;
}

export default {
  "earth-optimization-game-title"(H, fid) {
    const { K, C } = H;
    // KIT.titleScene's atomic card (16:9): the emblem at (960, 300), rx 200, ry 62, papers at 0.62, after "Game."
    const cx = 960, cy = 300, rx = 200, ry = 62, TILT = [0, 60, -60], t = 2.3;
    const orbits = TILT.map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const pos = (i) => {
      const th = i * 2.1 + t * 2.4, ar = (TILT[i] * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return [cx + ex * Math.cos(ar) - ey * Math.sin(ar), cy + ex * Math.sin(ar) + ey * Math.cos(ar) - 6];
    };
    // the paper the spinner points at has jumped
    const hit = 0, ph = pos(hit);
    const bills = TILT.map((a, i) => {
      const [x, y] = pos(i);
      return i === hit ? at(x, y - 58, 0.62, K.money("war", 1), -12) + `<path d="M${f(x - 34)},${f(y - 4)} l-10,14 M${f(x)},${f(y - 2)} v16 M${f(x + 34)},${f(y - 4)} l10,14" stroke="${C.cream}" stroke-width="4" stroke-linecap="round"/>` :
        at(x, y, 0.62, K.money("war", i % 2));
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    // the little mustard spinner arrow on the nucleus, pointing at the jumped paper
    const ang = (Math.atan2(ph[1] - 58 - cy, ph[0] - cx) * 180) / Math.PI;
    const arrow = `<g transform="translate(${cx},${cy}) rotate(${f(ang)})">` +
      `<path d="M-74,-9 H62 V-22 L108,0 L62,22 V9 H-74 L-88,0 Z" fill="${C.yellow}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      `<path d="M-72,6 H62 V18 L104,1" fill="none" stroke="${C.orange}" stroke-width="4"/><circle r="9" fill="${C.slate}" stroke="${C.ink}" stroke-width="3"/></g>`;
    const ticks = "";
    // the heading: "THE EARTH OPTIMIZATION" (small, size 100) over "GAME" (size 200), as KIT.titleScene lays it out
    const word = (y, s, text) => {
      const t0 = (dx, dy, extra) => `<text x="${960 + dx}" y="${y + dy}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${s}" ${extra}>${H.esc(text)}</text>`;
      return t0(0.04 * s, 0.053 * s, `fill="${C.ink}"`) + t0(0, 0, `fill="${C.cream}" stroke="${C.cream}" stroke-width="${f(0.044 * s)}" stroke-linejoin="round" style="paint-order:stroke"`);
    };
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus + arrow + ticks + word(637, 100, "THE EARTH OPTIMIZATION") + word(833, 200, "GAME");
    return { svg, alt: "The period title card: on plain navy, the film's atom with a little mustard spinner arrow on its orange nucleus, pointing at one of the three running papers, which has jumped; under it THE EARTH OPTIMIZATION GAME in cream letters." };
  },

  "game-box"(H, fid) {
    const { K, C } = H;
    // the side table on the free wall right of the lectern, its top at y 800; the box on it, the lid lifted a crack
    const svg = H.host("smirk-smile", "point-right", gameBox(K, C, fid, 1460, { open: true }));
    return { svg, alt: "Wishonia at her lectern points at a 1950s board game box on a side table: its new lid, THE EARTH OPTIMIZATION GAME with a mustard starburst reading FOR 2 TO 4,000,000,000 PLAYERS, hangs tilted above the box; under it the old orange lid, OBJECTIVE: LOSE, is pushed up a crack at the front, pale green light spilling out and three green medicine bills peeking out from under it." };
  },

  "game-pool-rules"(H, fid) {
    const { K, C } = H, ink = C.ink;
    // after "pool.": the pool cut into three slices, each holder waist-deep in its own slice in a crown of flying
    // bills, arms up, a point chip in one hand. View (120, -110) at 0.95.
    const slices = [[-300, 20], [60, -10], [410, 30]];
    const holders = slices.map(([sx, sy], i) => {
      const x = POOL_X + sx, o = copy(HOLDERS[i], { mood: "grin", arms: [[-150, -172], [150, 168]] }), r = K.rig(o), k = 1.5;
      const feet = sy + (100 - r.hipY) * k, id = `${fid}-w${i}`;
      const body = `<defs><clipPath id="${id}"><rect x="${x - 300}" y="${sy - 600}" width="600" height="${600 + 4}"/></clipPath></defs>` +
        `<g clip-path="url(#${id})">${stand(K, o, x, feet, k)}</g>`;
      const hand = r.hand[1], cxp = x + hand[0] * k, cyp = feet - 100 * k + hand[1] * k - 18;
      // the crown: bills flying up and out behind, a ring of bills at the waist in front
      const back = [[-170, -150, -50], [-110, -270, -24], [0, -330, 6], [112, -268, 26], [172, -146, 52]].map(([dx, dy, rr]) => at(x + dx, sy + dy, 0.7, K.money("med"), rr)).join("");
      const ring = [[-92, 6, -14], [-34, 16, -4], [30, 16, 6], [90, 6, 14]].map(([dx, dy, rr]) => at(x + dx, sy + dy, 0.62, K.money("med"), rr)).join("");
      return back + body + ring + chip(K, C, cxp, cyp, 24, 12 * (i - 1));
    }).join("");
    const plate = `<rect x="-4000" y="-4000" width="8000" height="8000" fill="${FIELD}"/>` +
      scoreboard(K, C, 0, -770, { rolling: true, fid }) + calendar(C, -760, -770, "2040") + board(K, C) + pool(K, C, fid, { split: true }) + holders;
    const svg = view(180, -150, 1.02, plate);
    return { svg, alt: "The game board from above: the pool of green medicine money cut into three slices by dashed lines, and in each slice a holder stands waist-deep in a splash of flying bills, grinning, arms up, a point chip in one hand; the back row of the track and the three smug disease blobs on the DISEASES corner behind them." };
  },

  "friends-to-play"(H, fid) {
    const { K, C } = H;
    // after "playing.": outside the box's left wall. View (-1520, 200) at 0.92.
    const ink = C.ink, feet = 420;
    const crate = `<rect x="-1810" y="${feet - 120}" width="230" height="120" fill="${C.tan}" stroke="${ink}" stroke-width="6"/>` +
      [feet - 80, feet - 40].map((y) => `<path d="M-1810,${y} H-1580" stroke="${ink}" stroke-width="4"/>`).join("") +
      `<path d="M-1810,${feet - 120} L-1580,${feet}" stroke="${ink}" stroke-width="4"/><rect x="-1820" y="${feet - 134}" width="250" height="20" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>`;
    const sit = copy(CRATE_MAN, { skeleton: true, arms: [[16, 96], [-16, -96]], build: { legPose: [[-62, 6], [62, -6]] } });
    // hips on the crate's top: KIT.rig gives the hip height in person units
    const R = K.rig(copy(sit, { skeleton: false })), k = 1.5;
    const man = at(-1695, feet - 134 - R.hipY * k, k, K.person(sit));
    const blob = at(-2030, feet + 6, 1.15, K.props.diseaseBlob({ seed: 11, color: "peri", mood: "grin", arms: "up" }));
    // over the wall: START, YOU and his two friends, each holding a medicine bill; more players up the track
    const held = (o, x, y, s) => {
      const r = K.rig(o), hx = (r.hand[0][0] + r.hand[1][0]) / 2, hy = Math.min(r.hand[0][1], r.hand[1][1]);
      return stand(K, o, x, y, s) + at(x + hx * s, y - 100 * s + hy * s - 10, 0.7 * s / 1.5, K.money("med"), -6);
    };
    const UP = { arms: [[-150, -170], [150, 170]], mood: "smile" };
    const ONE = { arms: [[-12, -6], [150, 170]], mood: "grin", look: "left" };
    // YOU on START, a medicine bill up in one hand, his two point chips stacked on his bowler
    const YO = copy(YOU, { arms: [[-12, -6], [110, 130]], mood: "grin", look: "left" }), RY = K.rig(YO), yk = 1.5, yx = -1080, yf = 660, top = yf - 100 * yk + RY.top[1] * yk;
    const you = stand(K, YO, yx, yf, yk) + at(yx + RY.hand[1][0] * yk + 10, yf - 100 * yk + RY.hand[1][1] * yk - 16, 0.72, K.money("med"), 8) +
      chip(K, C, yx + RY.top[0] * yk, top - 30, 22) + chip(K, C, yx + RY.top[0] * yk, top - 46, 22);
    const friends = held(copy(FRIENDS[0], UP), -880, 650, 1.45) + held(copy(FRIENDS[1], UP), -730, 640, 1.45);
    const others = held(copy(HOLDERS[0], UP), -1070, 200, 1.4);
    const plate = `<rect x="-4000" y="-4000" width="8000" height="8000" fill="${FIELD}"/>` + board(K, C, { blobs: false }) + frontWall(K, C) + others + friends + you +
      crate + man + blob;
    const svg = view(-1560, 330, 1.05, plate);
    return { svg, alt: "Outside the game box's orange wall, on the plain field, a grinning skeleton sits on an upturned crate with its arms still crossed, a grinning disease blob beside it with its claws up; over the wall, YOU in his bowler with two point chips on it and two friends stand on START holding up green medicine bills." };
  },

  "your-job"(H, fid) {
    const { K, C } = H, ink = C.ink;
    // after "play.": YOU at x 1250 (scale 3.3, feet at y 1072), unburnt, his two chips on his bowler and a gold star
    // on his forehead, one hand on the YES console that has sprung out of the lectern top, the other up; at the
    // right end of the wall, the game box (game-box's, at 0.74) with its lid shut on the last binder's legs.
    const k = 3.3, mx = 1250, feet = 1072;
    const o = copy(YOU, { mood: "grin", look: "left", arms: [[-62, -98], [176, 150]] });
    const R = K.rig(o), my = feet - 100 * k;
    const man = at(mx, my, k, K.person(o));
    // his two point chips stacked on his bowler
    const hx = mx + R.top[0] * k, top = my + R.top[1] * k;
    const chips = chip(K, C, hx, top - 82, 48) + chip(K, C, hx, top - 116, 48);
    // two fingers up on the raised hand
    const up = R.hand[1], ux = mx + up[0] * k, uy = my + up[1] * k;
    const skin = "#A87B57"; // YOU's tone 2
    const fingers = `<path d="M${f(ux - 8)},${f(uy - 4)} l-10,-42 M${f(ux + 8)},${f(uy - 6)} l6,-42" stroke="${ink}" stroke-width="16" stroke-linecap="round"/>` +
      `<path d="M${f(ux - 8)},${f(uy - 4)} l-10,-42 M${f(ux + 8)},${f(uy - 6)} l6,-42" stroke="${skin}" stroke-width="9" stroke-linecap="round"/>`;
    // the gold star on his forehead
    const ex = mx + R.eyes[0] * k + 14, ey = my + R.eyes[1] * k - 22;
    const star = K.star(ex, ey, 30, ink, 5) + K.star(ex, ey, 24, C.yellow, 5) + K.star(ex, ey, 9, "#FFF3C4", 5);
    // the YES console on its coil spring out of the lectern top, at its right end
    const cx = 990, cy = 700;
    let spring = "";
    for (let i = 0; i < 6; i++) spring += `${i ? "L" : "M"}${cx + (i % 2 ? 22 : -22)},${f(790 - i * ((790 - cy) / 5))} `;
    const console_ = `<path d="${spring}" fill="none" stroke="${ink}" stroke-width="9"/><path d="${spring}" fill="none" stroke="#C9CFD8" stroke-width="4"/>` + at(cx, cy, 1.25, K.props.yesButton({ label: "YES", sub: "TREATY" }));
    // the game box on its side table, game-box's drawing at 0.74 with its table's feet on the frame's bottom
    const box = `<g transform="translate(1640,1080) scale(0.74) translate(-1460,-1080)">${gameBox(K, C, fid, 1460, { kicker: true })}</g>`;
    const svg = H.host("happy-smile", "counting", box + console_ + man + chips + fingers + star);
    return { svg, alt: "Wishonia smiles at her lectern, counting on her fingers; beside her, YOU, two point chips on his bowler and a gold star stuck on his forehead, has one hand on a YES console that has sprung up out of the lectern on a coil spring and holds two fingers up; at the right end of the wall the game box sits on its side table, its lid shut on a binder whose stick legs still kick out from under it." };
  },

  "greed-handles-it"(H, fid) {
    const { K, C } = H, ink = C.ink;
    // after "before.": the back right of the board. The GREED arrow's post stands at (200, -480); the camera has
    // pushed in toward the DISEASES corner. View (820, -440) at 1.08.
    const runner = (o, x, y, s) => {
      const p = copy(o, { mood: "greedy", look: "right", arms: [[-40, -90], [150, 170]], build: copy(o.build || {}, { legPose: [[-34, 10], [30, -40]] }) });
      const r = K.rig(p);
      return stand(K, p, x, y, s) + chip(K, C, x + r.hand[1][0] * s, y - 100 * s + r.hand[1][1] * s - 14, 20) + speed(C, x - 60 * s, y - 130 * s);
    };
    const PEOPLE = [
      [{ tone: 1, outfit: "shirt", color: 0, seed: 21 }, 640, -640, 1.35], [{ tone: 3, outfit: "dress", color: 2, hair: 1, seed: 22 }, 820, -660, 1.35],
      [{ tone: 0, outfit: "overalls", color: 1, seed: 23 }, 560, -520, 1.45], [{ tone: 2, outfit: "suit", color: 3, seed: 24 }, 740, -500, 1.45],
      [{ tone: 1, outfit: "dress", color: 1, hair: 1, seed: 25 }, 900, -470, 1.45], [{ tone: 0, outfit: "suit", kind: "egg", color: 0, seed: 27 }, 640, -370, 1.5],
    ];
    const crowd = PEOPLE.map(([o, x, y, s]) => ({ y, svg: runner(o, x, y, s) }));
    // a lobbyist and a scientist in the front of the stampede
    crowd.push({ y: -330, svg: stand(K, K.castOpts("lobbyist", { mood: "greedy", look: "right" }), 820, -330, 1.5) });
    crowd.push({ y: -360, svg: stand(K, K.castOpts("scientist", { mood: "greedy", look: "right" }), 500, -360, 1.45) });
    crowd.sort((p, q) => p.y - q.y);
    // the walking hospital on the DISEASES corner, its right foot down on the last blob, squashed flat and x-eyed
    const hx = 1070, hy = -500;
    const flat = at(hx + 70, hy + 4, 1, `<g transform="scale(1.3,0.24)">${K.props.diseaseBlob({ seed: 2, color: "orange", mood: "dead" })}</g>`);
    const splat = [[-70, -20], [-36, -40], [36, -42], [80, -22], [112, -4]].map(([dx, dy]) => `<path d="M${hx + 70 + dx * 0.9},${hy - 4 + dy * 0.5} l${dx * 0.5},${dy * 0.5}" stroke="${ink}" stroke-width="6" stroke-linecap="round"/>`).join("");
    const legs = [-1, 1].map((sd) => {
      const lx = hx + sd * 80, fx = sd > 0 ? hx + 70 : lx - 10;
      return `<path d="M${lx},${hy - 76} L${fx},${hy - 6}" stroke="${ink}" stroke-width="16" stroke-linecap="round"/><path d="M${lx},${hy - 76} L${fx},${hy - 6}" stroke="${C.cream}" stroke-width="6" stroke-linecap="round"/>` +
        `<path d="M${fx - 22},${hy - 4} L${fx + 34},${hy - 10} L${fx + 28},${hy + 6} L${fx - 22},${hy + 6} Z" fill="${ink}"/>`;
    }).join("");
    const hospital = legs + at(hx, hy - 74, 0.86, K.props.hospital({}));
    // the other two blobs, running off the board, scared
    const fleeing = at(1420, -400, 0.8, K.props.diseaseBlob({ seed: 5, color: "peri", mood: "scared", arms: "up" })) + speed(C, 1330, -480, 3, 70) +
      at(1600, -600, 0.72, K.props.diseaseBlob({ seed: 8, color: "rust", mood: "scared", arms: "up" })) + speed(C, 1520, -680, 3, 70);
    // one of the runners who dragged the arrow round still dangles from its shaft by both hands, legs running
    const DG = { tone: 3, outfit: "shirt", color: 2, seed: 26, hat: null, mood: "greedy", look: "right", arms: [[-168, -176], [168, 176]], build: { legPose: [[-34, 10], [30, -40]] } };
    const RD = K.rig(DG), dk = 1.35, gx = (RD.hand[0][0] + RD.hand[1][0]) / 2, gy = (RD.hand[0][1] + RD.hand[1][1]) / 2;
    // swung back a little on his grip, his shadow on the board well below his shoes
    const dfeet = -716 + (100 - gy) * dk;
    const dangler = `<ellipse cx="330" cy="${f(dfeet + 70)}" rx="56" ry="12" fill="${ink}" opacity="0.22"/>` +
      `<g transform="rotate(12 350 -716)">${at(350 - gx * dk, -716 - gy * dk, dk, K.person(DG))}</g>` + speed(C, 300, -600, 3, 50);
    const plate = `<rect x="-4000" y="-4000" width="8000" height="8000" fill="${FIELD}"/>` + scoreboard(K, C, 0, -770, { fid }) +
      board(K, C, { blobs: false, warBurnt: true }) + pool(K, C, fid) + greedArrow(C, 200, -480, 0, 240) + dangler +
      dust(C, 700, -330, 620, 1) + crowd.map((c) => c.svg).join("") + dust(C, 760, -290, 520, 3) + flat + splat + hospital + fleeing;
    const svg = view(820, -440, 1.08, plate);
    return { svg, alt: "The back right of the game board: the GREED arrow on its post points right at the DISEASES corner, a dollar-eyed player still dangling from its shaft by both hands, legs running; the dollar-eyed crowd, a lobbyist and a scientist among them, stampedes toward the corner in a cloud of dust, holding up point chips; a hospital on stick legs has stepped on the last disease blob, squashed flat and x-eyed, while the other two flee off the board." };
  },
};
