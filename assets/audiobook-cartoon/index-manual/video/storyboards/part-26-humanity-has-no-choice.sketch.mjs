// Sketches for storyboards/part-26-humanity-has-no-choice.md: each scene's key frame on a 1920 x 1080 frame (16:9),
// drawn with the production art (kit.js, film.js, the props library). Built into the review sheet by
// tools/storyboard-sheet.mjs.
//
// The shared drawings of the part are here, for the scene authors to copy so every scene draws them the same:
//   YOU, PULLERS              YOU's options, and the four pullers of the treaty road (options, feet, facing, bait)
//   cart(H, o)                the treaty cart, its front to the right, wheels on y 0 (plate units); CART_ROPE: its
//                             four rope corners
//   puller(H, p, o)           one puller in his harness, its pole bent over his head and the bait on its string
//   halo(H, k)                the gold halo (flat, as it sits on a head), about 116 x 32 at k 1
//   hoop(H, r)                the same halo on its edge, rolling (a ring of radius r)
//   caneHook(H, x0, y0, x1, y1)  the vaudeville cane hook (doubling-starts, countdown-104), its crook at (x1, y1)
//   saucer(H)                 a 1950s B-movie flying saucer, about 170 wide, around (0, 0), its string up from (0, -40)
//   caseFile(H, stamps)       the Earth case file standing on the lectern (Part 12's), stamps 1 to 3
//   mug(H)                    Wishonia's mug (Part 12's)
//   bonyYou(H, o, fid)        YOU from the waist up, his legs bone (after countdown-104), in person units
// The deli of countdown-104 is Part 8's: its sign, ticket and Reaper come from part-08's sketch module, and the
// plate below copies deletion-board's positions (the counter, the door, the dispenser, the queue).

import { nowServing, ticket, reaper } from "./part-08-daily-deletion-event.sketch.mjs";

const f = (n) => n.toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});
const at = (x, y, k, inner, rot = 0) => `<g transform="translate(${f(x)},${f(y)})${rot ? ` rotate(${rot})` : ""}${k !== 1 ? ` scale(${k})` : ""}">${inner}</g>`;
// A plate framing as KIT.camera places it: plate point (x, y) in the middle of the frame, at scale s.
const view = (x, y, s, inner) => `<g transform="translate(${f(960 - x * s)},${f(540 - y * s)}) scale(${s})">${inner}</g>`;
// A person standing on groundY at x, scale k (KIT.person is drawn with its feet at y 100).
const stand = (K, o, x, groundY, k, extra = "") => at(x, groundY - 100 * k, k, K.person(o) + extra);

const GROUND = "#C8B07B", SKY = "#EFE3C4", ROAD = "#EEE3C4", EDGE = "#B09363", BONE = "#F1EAD6", LEATHER = "#6B4A2E", WHITE = "#FBF6E6";

// ── Shared drawings ─────────────────────────────────────────────────────

export const YOU = { tone: 2, outfit: "suit", hat: "bowler" };

// The treaty road plate (greed-ropes, cure-death-by-mistake): the road along y 0, feet on y 40, everyone at S.
export const S = 1.5;
export const FEET = 40;

// The treaty cart around its center x 0, its wheels on y 0, its front to the right, in plate units. o: { plank
// (the side plank gone, popped off), lift (how far it shudders off the road) }.
export const CART_ROPE = { ul: [-262, -246], ur: [262, -246], ll: [-262, -160], lr: [262, -160], front: [300, -176] };
export function cart(H, o = {}) {
  const { K, C } = H, ink = C.line;
  const wheel = (cx) => {
    const cy = -92, r = 92;
    let d = "";
    for (let i = 0; i < 12; i++) {
      const a = (i * Math.PI) / 6;
      d += `M${f(cx + 18 * Math.cos(a))},${f(cy + 18 * Math.sin(a))} L${f(cx + (r - 10) * Math.cos(a))},${f(cy + (r - 10) * Math.sin(a))} `;
    }
    return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${ink}" stroke-width="22"/><circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${C.rust}" stroke-width="13"/>` +
      `<path d="${d}" stroke="${ink}" stroke-width="10" stroke-linecap="round"/><path d="${d}" stroke="${C.tan}" stroke-width="5"/>` +
      `<circle cx="${cx}" cy="${cy}" r="22" fill="${C.slate}" stroke="${ink}" stroke-width="5"/><circle cx="${cx}" cy="${cy}" r="7" fill="${C.cream}"/>`;
  };
  // the load: a heap of medicine money with the treaty scroll standing up in it
  const heap = [[-200, -258, -14], [-130, -276, 10], [-60, -266, -6], [110, -272, 8], [190, -258, -12], [-170, -298, 18], [160, -296, -20], [-100, -312, 4], [70, -300, -10]]
    .map(([x, y, r]) => at(x, y, 0.95, K.money("med", 0.5), r)).join("");
  const scroll = at(20, -266, 1.3, K.props.scroll({ text: "1% TREATY" }));
  // the bed: three tan planks between rust end posts; the plaque on the tailgate (the left end)
  let bed = `<path d="M-272,-252 H272 V-148 H-272 Z" fill="${C.tan}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
    `<path d="M-264,-218 H264 M-264,-184 H264" stroke="${ink}" stroke-width="3"/><path d="M-200,-250 V-150 M60,-250 V-150 M220,-250 V-150" stroke="#9A6E44" stroke-width="3"/>`;
  if (o.plank) bed += `<path d="M30,-216 H190 V-186 H30 Z" fill="${C.ink}"/>`;
  bed += `<rect x="-286" y="-272" width="24" height="134" fill="${C.rust}" stroke="${ink}" stroke-width="5"/><rect x="262" y="-272" width="24" height="134" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>`;
  const plaque = `<rect x="-252" y="-244" width="132" height="84" rx="3" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/><rect x="-245" y="-237" width="118" height="70" fill="none" stroke="#A77A2A" stroke-width="2"/>` +
    [[-244, -236], [-128, -236], [-244, -168], [-128, -168]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3" fill="#A77A2A"/>`).join("") +
    ["ACCIDENTALLY SAVED", "HUMANITY WHILE", "GETTING RICH"].map((t, i) => `<text x="-186" y="${-216 + i * 18}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="14" fill="${ink}">${t}</text>`).join("");
  const frame = `<rect x="-250" y="-150" width="500" height="20" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>` +
    `<path d="M286,-186 H318 M318,-196 a10,10 0 1,1 0,20 a10,10 0 1,1 0,-20" fill="none" stroke="${ink}" stroke-width="9"/><path d="M286,-186 H318" stroke="${C.rust}" stroke-width="4"/>`;
  const lift = o.lift || 0;
  return `<ellipse cx="0" cy="4" rx="300" ry="16" fill="${C.ink}" opacity="0.18"/>` + `<g transform="translate(0,${-lift})">${heap + scroll + bed + plaque + frame + wheel(-150) + wheel(150)}</g>`;
}

// The four pullers: options, feet on the plate, facing (-1 left, 1 right), bait and lean. The bait hangs from the
// pole's tip at nose height, just out of reach.
export const PULLERS = {
  fatCat: { cast: "richHuman", x: -760, y: -280, d: -1, hunch: 18, arms: [[-118, -138], [-106, -128]], bait: "bond" },
  politician: { cast: "politician", x: 760, y: -280, d: 1, hunch: 12, arms: [[-10, -4], [122, 176]], bait: "ballot", tie: "med" }, // his tie teal since Part 20
  you: { you: true, x: -760, y: 330, d: -1, hunch: 16, arms: [[-112, -132], [-100, -122]], bait: "pills" },
  weaponsMaker: { cast: "weaponsMaker", x: 760, y: 330, d: 1, hunch: 12, bait: "bill" },
};
function pullerOpts(H, p, o = {}) {
  const { K } = H, look = p.d < 0 ? "left" : "right";
  if (p.you) return copy(YOU, copy({ look, light: "red", mood: "worried", arms: p.arms, build: { hunch: p.hunch } }, o));
  const base = K.CAST[p.cast];
  const extra = copy({ look, build: copy(base.build, { hunch: p.hunch }) }, o);
  if (p.arms) extra.arms = p.arms;
  if (p.tie) extra.tieColor = K.C[p.tie];
  return K.castOpts(p.cast, extra);
}
function baitSvg(H, kind, seal) {
  const { K } = H;
  // each hangs from its own top center at (0, 0)
  if (kind === "bond") return at(0, 52, 0.45, K.props.bond({ value: "272%", seal: "med" }));
  if (kind === "ballot") return at(0, 50, 0.8, K.props.ballotBox());
  if (kind === "pills") return at(0, 56, 0.52, K.props.pillBottle({ label: "FREE" }));
  return at(0, 14, 0.55, K.money(seal || "war", 0.5));
}
// One puller in his harness, in person units around his feet's center x 0 (feet y 100). Returns { svg, back }: back
// is where the rope ties on (person units), for the rope to the cart. o: person options to add (mood, ...); seal:
// the war bill's seal.
export function puller(H, p, o = {}, seal) {
  const { K, C } = H, ink = C.line;
  const po = pullerOpts(H, p, o), R = K.rig(po), d = p.d;
  const th = ((R.lean || 0) * Math.PI) / 180, cs = Math.cos(th), sn = Math.sin(th);
  const lean = ([x, y]) => { const yy = y - R.hipY; return [x * cs - yy * sn, R.hipY + x * sn + yy * cs]; };
  const bw = Math.abs(R.shoulder[0][0]) + 6, wy = R.hipY - 14;
  // the harness: a leather band round his middle with a ring at the back, and the bamboo pole bent over his head
  const band = `<g transform="rotate(${f(R.lean || 0)} 0 ${f(R.hipY)})"><path d="M${-bw},${wy - 7} H${bw} V${wy + 7} H${-bw} Z" fill="${LEATHER}" stroke="${ink}" stroke-width="2.4"/>` +
    `<rect x="-5" y="${wy - 5}" width="10" height="10" fill="${C.yellow}" stroke="${ink}" stroke-width="1.6"/>` +
    `<circle cx="${-d * (bw + 5)}" cy="${wy}" r="5" fill="none" stroke="${ink}" stroke-width="2.6"/></g>`;
  const top = R.top[1];
  const p0 = lean([-d * (bw - 2), wy]), p1 = lean([-d * (bw + 10), top - 40]), p2 = lean([d * 30, top - 66]), tip = lean([d * 92, top - 52]);
  const pole = `<path d="M${f(p0[0])},${f(p0[1])} Q${f(p1[0])},${f(p1[1])} ${f(p2[0])},${f(p2[1])} T${f(tip[0])},${f(tip[1])}" fill="none" stroke="${ink}" stroke-width="7" stroke-linecap="round"/>` +
    `<path d="M${f(p0[0])},${f(p0[1])} Q${f(p1[0])},${f(p1[1])} ${f(p2[0])},${f(p2[1])} T${f(tip[0])},${f(tip[1])}" fill="none" stroke="#D9B96A" stroke-width="3.4" stroke-linecap="round"/>`;
  const baitY = R.mouth[1] - 14;
  const string = `<path d="M${f(tip[0])},${f(tip[1])} V${f(baitY)}" stroke="${ink}" stroke-width="1.6"/>`;
  const bait = at(tip[0], baitY, 1, baitSvg(H, p.bait, seal));
  let props = "";
  if (p.you) {
    // the thermometer in his mouth
    const m = R.mouth;
    props += `<path d="M${f(m[0])},${f(m[1])} l${d * 18},-5" stroke="${ink}" stroke-width="4.4" stroke-linecap="round"/><path d="M${f(m[0])},${f(m[1])} l${d * 18},-5" stroke="${WHITE}" stroke-width="2.4" stroke-linecap="round"/>` +
      `<circle cx="${f(m[0] + d * 18)}" cy="${f(m[1] - 5)}" r="2.6" fill="${C.war}" stroke="${ink}" stroke-width="1.2"/>`;
  }
  if (p.cast === "politician") {
    // the cracked hand mirror at his face
    const h = R.hand[1];
    props += at(h[0] + 4, h[1] - 10, 1, `<path d="M0,10 V22" stroke="${ink}" stroke-width="5" stroke-linecap="round"/><path d="M0,10 V22" stroke="${C.rust}" stroke-width="2.6"/>` +
      `<ellipse cx="0" cy="0" rx="9" ry="11" fill="#BFE0E6" stroke="${ink}" stroke-width="2.6"/><path d="M-6,-6 L1,-1 L-2,4 L5,8 M1,-1 L7,-4" fill="none" stroke="${ink}" stroke-width="1.3"/>`, -14);
  }
  const back = lean([-d * (bw + 5), wy]);
  return { svg: K.person(po) + band + props + pole + string + bait, back, R };
}
// The halo: a flat gold ring, as it sits on a head. Around (0, 0).
export function halo(H, k = 1) {
  const { C } = H;
  return at(0, 0, k, `<ellipse rx="58" ry="16" fill="none" stroke="${C.line}" stroke-width="16"/><ellipse rx="58" ry="16" fill="none" stroke="${C.yellow}" stroke-width="9"/>`);
}
// The halo on its edge, rolling: a gold ring of radius r standing on (0, 0).
export function hoop(H, r = 50) {
  const { C } = H;
  return `<ellipse cx="0" cy="${-r}" rx="${r * 0.92}" ry="${r}" fill="none" stroke="${C.line}" stroke-width="${r * 0.3}"/><ellipse cx="0" cy="${-r}" rx="${r * 0.92}" ry="${r}" fill="none" stroke="${C.yellow}" stroke-width="${r * 0.17}"/>` +
    `<path d="M${-r * 0.5},${-r * 1.6} a${r * 0.8},${r * 0.8} 0 0,1 ${r * 0.5},${-r * 0.3}" fill="none" stroke="${C.cream}" stroke-width="${r * 0.08}" stroke-linecap="round"/>`;
}
// A 1950s B-movie flying saucer around (0, 0), about 170 wide: a glass dome, a periwinkle hull with a row of mustard
// lights, an orange belly; its string rises from the dome's top (0, -40).
export function saucer(H) {
  const { C } = H, ink = C.line;
  return `<path d="M-38,-12 Q-36,-46 0,-46 Q36,-46 38,-12 Z" fill="#BFE0E6" stroke="${ink}" stroke-width="4"/><path d="M-22,-30 q8,-10 20,-10" fill="none" stroke="${WHITE}" stroke-width="4" stroke-linecap="round"/>` +
    `<path d="M-60,8 Q0,34 60,8 Z" fill="${C.orange}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
    `<ellipse cx="0" cy="0" rx="86" ry="18" fill="${C.peri}" stroke="${ink}" stroke-width="5"/><path d="M-80,-4 Q0,-22 80,-4" fill="none" stroke="${C.cream}" stroke-width="4"/>` +
    [-0.66, -0.33, 0, 0.33, 0.66].map((u) => `<circle cx="${f(u * 86)}" cy="${f(6 - Math.abs(u) * 4)}" r="6" fill="${C.yellow}" stroke="${ink}" stroke-width="2"/>`).join("");
}
// The Earth case file standing on the lectern, its bottom middle at (0, 0), 190 wide (Part 12's). stamps: 1 MAY BE
// ELIGIBLE FOR OPTIMIZATION, 2 and SUBOPTIMAL, 3 and the final stamp (a red bar through MAY BE, ELIGIBLE FOR
// OPTIMIZATION across it).
export function caseFile(H, stamps) {
  const { C } = H, ink = C.line;
  let s = `<path d="M-95,0 L-95,-150 L-40,-150 L-30,-166 L40,-166 L50,-150 L95,-150 L95,0 Z" fill="#E7C98C" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/>` +
    `<text x="5" y="-153" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="11" fill="${ink}"><tspan text-decoration="line-through">EARTH</tspan> DIRT: CASE #847</text>` +
    `<path d="M-23,-157 H6" stroke="${ink}" stroke-width="1.6"/>`;
  const mark = (x, y, rot, lines, size, w, h, double) => `<g transform="translate(${x},${y}) rotate(${rot})"><rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" fill="none" stroke="${C.war}" stroke-width="3.4"/>` +
    (double ? `<rect x="${-w / 2 + 5}" y="${-h / 2 + 5}" width="${w - 10}" height="${h - 10}" fill="none" stroke="${C.war}" stroke-width="1.4"/>` : "") +
    lines.map((t, i) => `<text x="0" y="${f(-((lines.length - 1) * size * 1.1) / 2 + i * size * 1.1 + size * 0.36)}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="${size}" letter-spacing="1" fill="${C.war}">${t}</text>`).join("") + "</g>";
  if (stamps >= 1) s += mark(0, -108, -6, ["MAY BE ELIGIBLE", "FOR OPTIMIZATION"], 15, 164, 42, false);
  if (stamps >= 2) s += mark(4, -36, 4, ["SUBOPTIMAL"], 22, 168, 38, true);
  if (stamps >= 3) {
    s += `<path d="M-70,-122 L-6,-128" stroke="${C.war}" stroke-width="9" stroke-linecap="round"/>`;
    s += `<g transform="translate(6,-84) rotate(-14)"><rect x="-92" y="-30" width="184" height="60" fill="${WHITE}" fill-opacity="0.55" stroke="${C.war}" stroke-width="5"/>` +
      `<rect x="-85" y="-23" width="170" height="46" fill="none" stroke="${C.war}" stroke-width="2"/>` +
      `<text x="0" y="-3" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="21" letter-spacing="1.5" fill="${C.war}">ELIGIBLE FOR</text>` +
      `<text x="0" y="20" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="21" letter-spacing="1.5" fill="${C.war}">OPTIMIZATION</text></g>`;
  }
  return s;
}
// Wishonia's coffee mug, standing on (0, 0) (Part 12's).
export function mug(H) {
  const { C } = H, ink = C.line;
  return `<path d="M22,-50 q24,4 22,22 q-2,16 -22,16" fill="none" stroke="${ink}" stroke-width="8"/><path d="M22,-50 q24,4 22,22 q-2,16 -22,16" fill="none" stroke="${C.orange}" stroke-width="4"/>` +
    `<path d="M-26,-62 H26 L22,0 H-22 Z" fill="${C.orange}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/><path d="M-24,-54 H24" stroke="${C.cream}" stroke-width="4"/>`;
}
// The lectern props of the host shots: the case file at the left end, the mug at the right end (16:9).
function lecternProps(H, stamps = 2, withMug = true) {
  const S0 = H.K.STUDIO, cx = S0.lect[0], hw = S0.lect[1] / 2, top = S0.top;
  return (withMug ? at(cx + hw - 50, top + 4, 1, mug(H)) : "") + at(cx - hw + 120, top + 6, 0.82, caseFile(H, stamps));
}
// YOU from the waist up and bone below it (from countdown-104 on), in person units. o: more person options.
export function bonyYou(H, o, fid) {
  const { K, C } = H, po = copy(YOU, o), R = K.rig(po), cut = R.hipY - 4;
  // knobbly knees, so the bone reads as bone: halfway down each leg (the standing pose, legs at -6 and 6 degrees)
  const L = 37 * R.build.legs, knee = R.hip.map(([x], i) => [x + L * Math.sin(((i ? 6 : -6) * Math.PI) / 180), R.hipY + L * Math.cos((6 * Math.PI) / 180)]);
  const knees = knee.map(([x, y]) => `<ellipse cx="${f(x)}" cy="${f(y)}" rx="4.2" ry="3.4" fill="${BONE}" stroke="${C.line}" stroke-width="1.6"/>`).join("");
  return `<defs><clipPath id="${fid}-up"><rect x="-200" y="-200" width="400" height="${f(200 + cut)}"/></clipPath><clipPath id="${fid}-dn"><rect x="-200" y="${f(cut)}" width="400" height="200"/></clipPath></defs>` +
    `<g clip-path="url(#${fid}-dn)">${K.person(copy(po, { skeleton: true }))}</g>${knees}<g clip-path="url(#${fid}-up)">${K.person(po)}</g>`;
}

// ── The treaty road plate ───────────────────────────────────────────────
function road(H, x0 = -2400, x1 = 6400) {
  return `<rect x="-6000" y="-4000" width="14000" height="8000" fill="${GROUND}"/>` +
    `<rect x="${x0}" y="-97" width="${x1 - x0}" height="194" fill="${EDGE}"/><rect x="${x0}" y="-90" width="${x1 - x0}" height="180" fill="${ROAD}"/>` +
    `<path d="M${x0},-30 H${x1} M${x0},40 H${x1}" stroke="#E0D2AE" stroke-width="10" stroke-dasharray="120 160" opacity="0.8"/>`;
}
const rope = (H, a, b, taut = true) => {
  const { C } = H;
  const mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + (taut ? 0 : 60)];
  const d = `M${f(a[0])},${f(a[1])} Q${f(mid[0])},${f(mid[1])} ${f(b[0])},${f(b[1])}`;
  return `<path d="${d}" fill="none" stroke="${C.line}" stroke-width="9" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#D9C08A" stroke-width="4.5" stroke-linecap="round" stroke-dasharray="10 6"/>`;
};
// A puller placed on the plate: feet (x, y), scale S. Returns { svg, back } in plate units.
function placed(H, p, x, y, o, seal) {
  const P0 = puller(H, p, o, seal), gx = x, gy = y - 100 * S;
  return { svg: at(gx, gy, S, P0.svg), back: [gx + S * P0.back[0], gy + S * P0.back[1]], R: P0.R };
}
// Little motion strokes: n short lines at (x, y), dx apart, angle a (deg).
function strokes(H, x, y, n, dx, len, a = 0, w = 5) {
  let d = "";
  for (let i = 0; i < n; i++) d += `M${f(x + i * dx * Math.sin((a * Math.PI) / 180))},${f(y + i * dx * Math.cos((a * Math.PI) / 180))} l${f(len * Math.cos((a * Math.PI) / 180))},${f(-len * Math.sin((a * Math.PI) / 180))} `;
  return `<path d="${d}" stroke="${H.C.line}" stroke-width="${w}" stroke-linecap="round"/>`;
}
// A disease blob rolled flat in the road, a lumpy lavender puddle with X eyes, its pageant sash across it.
function splat(H, x, label) {
  const { C } = H, ink = C.line;
  const puddle = `<path d="M-120,0 C-130,-18 -96,-30 -70,-26 C-56,-40 -20,-38 -6,-30 C14,-42 52,-40 66,-28 C92,-34 126,-22 118,-4 C130,8 96,18 70,14 C40,22 -40,22 -70,14 C-100,18 -130,12 -120,0 Z" fill="${C.peri}" stroke="${ink}" stroke-width="4"/>`;
  const eye = (ex) => `<path d="M${ex - 7},-22 l14,8 M${ex + 7},-22 l-14,8" stroke="${ink}" stroke-width="3.4" stroke-linecap="round"/>`;
  const sash = `<path d="M-86,6 L74,-30 L84,-14 L-76,22 Z" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>` +
    `<text x="0" y="0" transform="rotate(-12.6 0 0) translate(0,4)" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="${label.length > 8 ? 17 : 22}" letter-spacing="1" fill="${C.war}">${label}</text>`;
  return at(x, FEET + 12, 1, puddle + eye(-40) + eye(-12) + sash + `<path d="M50,-36 l10,-14 M66,-30 l14,-8" stroke="${ink}" stroke-width="3" stroke-linecap="round"/>`);
}

// ── The cane hook ───────────────────────────────────────────────────────
// The vaudeville cane hook: a long shepherd's crook held at (x0, y0), its shaft running to (x1, y1), where the crook
// curls up and back toward the holder (to catch a collar and yank it his way). Plate units, at scale 1.
export function caneHook(H, x0, y0, x1, y1) {
  const { C } = H, s = x1 >= x0 ? -1 : 1;
  const d = `M${f(x0)},${f(y0)} L${f(x1)},${f(y1)} q0,-46 ${34 * s},-46 q${30 * s},0 ${32 * s},30`;
  return `<path d="${d}" fill="none" stroke="${C.line}" stroke-width="16" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${C.tan}" stroke-width="8" stroke-linecap="round"/>`;
}

// ── The plain (doubling-starts) ─────────────────────────────────────────
// A bare plain, its horizon at y -540. YOU's desk front and center (his feet at (0, 0), scale 1.5); the voters land
// in rows behind him, each further back, smaller and twice as many: FAN[r] is row r's feet y, scale and spacing, and
// fanX(r, i) the i-th voter's x (row r holds 2^(r+1)). The tally board stands on two legs on the horizon.
const PLAIN_HZ = -540, YOU_K = 1.5;
export const FAN = [
  { y: -140, k: 1.15, dx: 660 },
  { y: -270, k: 0.92, dx: 340 },
  { y: -380, k: 0.74, dx: 250 },
  { y: -465, k: 0.6, dx: 190 },
];
export const fanX = (r, i) => (i - ((2 << r) - 1) / 2) * FAN[r].dx;
// The tally board: a navy box with an orange rule and ten flip tiles (the NOW SERVING sign's tiles), room for every
// human alive, on two legs standing on the horizon; its box from y -1010 to -770, centered on x 0. n: the count;
// rolling: how many tiles at the right are rolling (a flap half over and motion strokes); bird: 0 none, 1 asleep on
// its nest over the billions tile, 2 flapping off with its egg in its beak (the nest left behind).
export const BOARD = { top: -1010, bot: -770, tw: 118, th: 170, gap: 12, comma: 34 };
export const boardTileX = (i) => {
  const { tw, gap, comma } = BOARD, W = 10 * tw + 9 * gap + 3 * comma;
  return -W / 2 + i * (tw + gap) + comma * ((i >= 1) + (i >= 4) + (i >= 7));
};
function tallyBoard(H, n, rolling = 0, bird = 0) {
  const { C } = H, ink = C.line, { top, bot, tw, th, gap, comma } = BOARD;
  const W = 10 * tw + 9 * gap + 3 * comma, bx = W / 2 + 46;
  const digits = String(n).padStart(10, "0");
  const legs = `<path d="M-480,${bot} V${PLAIN_HZ + 6} M480,${bot} V${PLAIN_HZ + 6}" stroke="${ink}" stroke-width="30"/><path d="M-480,${bot} V${PLAIN_HZ + 6} M480,${bot} V${PLAIN_HZ + 6}" stroke="${C.slate}" stroke-width="18"/>` +
    `<path d="M-480,${bot + 80} L480,${PLAIN_HZ - 20} M480,${bot + 80} L-480,${PLAIN_HZ - 20}" stroke="${ink}" stroke-width="8"/>`;
  let s = legs + `<rect x="${-bx + 10}" y="${top + 12}" width="${2 * bx}" height="${bot - top}" rx="14" fill="${ink}" opacity="0.85"/>` +
    `<rect x="${-bx}" y="${top}" width="${2 * bx}" height="${bot - top}" rx="14" fill="${C.navy}" stroke="${ink}" stroke-width="7"/>` +
    `<rect x="${-bx + 16}" y="${top + 16}" width="${2 * bx - 32}" height="${bot - top - 32}" rx="8" fill="none" stroke="${C.orange}" stroke-width="5"/>`;
  const ty = top + 35;
  for (let i = 0; i < 10; i++) {
    const x = boardTileX(i);
    s += `<rect x="${f(x)}" y="${ty}" width="${tw}" height="${th}" rx="7" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` +
      `<text x="${f(x + tw / 2)}" y="${ty + 142}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="146" fill="${C.yellow}">${digits[i]}</text>` +
      `<path d="M${f(x + 3)},${ty + th / 2} h${tw - 6}" stroke="#111A2C" stroke-width="3.4"/>`;
    if (i >= 10 - rolling) {
      // motion strokes over and under the tile (the digit stays readable)
      s += `<path d="M${f(x + 18)},${ty - 14} q${tw / 2 - 18},-16 ${tw - 36},0 M${f(x + 18)},${ty + th + 14} q${tw / 2 - 18},16 ${tw - 36},0" fill="none" stroke="${C.cream}" stroke-width="4" stroke-linecap="round"/>`;
    }
  }
  for (const i of [1, 4, 7]) s += `<text x="${f(boardTileX(i) - gap / 2 - comma / 2)}" y="${ty + 176}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="120" fill="${C.cream}">,</text>`;
  if (bird) {
    // the nest on the board's top edge over the billions tile
    const nx = boardTileX(0) + tw / 2;
    s += at(nx, top, 1, `<path d="M-52,-4 Q-50,-40 0,-40 Q50,-40 52,-4 Z" fill="#8A6438" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M-46,-22 l92,6 M-44,-12 l88,-8 M-30,-34 l22,26 M14,-36 l-14,30 M-56,-30 l18,10 M38,-38 l20,10" stroke="${ink}" stroke-width="2.6" stroke-linecap="round"/>`);
    const b = (asleep) => `<ellipse cx="0" cy="0" rx="34" ry="24" fill="${C.orange}" stroke="${ink}" stroke-width="4"/><circle cx="26" cy="-22" r="17" fill="${C.orange}" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M40,-26 l18,4 l-18,6 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>` +
      (asleep ? `<path d="M24,-24 q5,4 10,0" fill="none" stroke="${ink}" stroke-width="3"/>` : `<circle cx="30" cy="-25" r="6" fill="${WHITE}" stroke="${ink}" stroke-width="2"/><circle cx="32" cy="-25" r="2.6" fill="${ink}"/>`) +
      `<path d="M-30,-4 l-26,-6 l6,14 Z" fill="${C.rust}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>`;
    if (bird === 1) s += at(nx - 4, top - 44, 1, b(true));
    else {
      // flapping up and away to the left, the egg in its beak, wings up, motion strokes back to the nest
      const wing = `<path d="M-6,-14 Q-30,-74 -64,-80 Q-40,-40 -22,-6 Z M6,-14 Q10,-80 -10,-104 Q30,-60 22,-8 Z" fill="${C.rust}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>`;
      const egg = `<ellipse cx="66" cy="-20" rx="10" ry="13" fill="${WHITE}" stroke="${ink}" stroke-width="3"/>`;
      s += at(nx - 160, top - 190, 1.15, `<g transform="scale(-1,1) rotate(-14)">${b(false) + wing + egg}</g>`) + strokes(H, nx - 70, top - 120, 3, 22, 46, -30, 4);
    }
  }
  return s;
}

// ── The deli plate (copied from part-08-daily-deletion-event.sketch.mjs, deletion-board's positions) ──────
const SD = 1.6, HZ = 560, TILE = "#F1EAD6", TILE_LINE = "#D8CFB4";
const QVP = [1600, -HZ], Q0 = [90, 0];
const qAt = (u) => ({ x: Q0[0] + (QVP[0] - Q0[0]) * u, y: Q0[1] + (QVP[1] - Q0[1]) * u, k: SD * (1 - u) });
const QU = [0.1, 0.19, 0.27, 0.345, 0.41, 0.47, 0.525, 0.575, 0.62, 0.66, 0.7, 0.735, 0.765, 0.795, 0.82, 0.845, 0.865, 0.885, 0.9, 0.915];
const QOPTS = [
  { tone: 0, outfit: "dress", hair: 1, color: 3, seed: 4 },
  { tone: 3, outfit: "suit", hair: 0, color: 1, seed: 6 },
  { tone: 2, outfit: "shirt", hair: 0, color: 0, seed: 9 },
  { tone: 1, outfit: "dress", hair: 1, color: 2, seed: 11 },
  { tone: 0, outfit: "suit", hair: 2, color: 2, seed: 2 },
  { tone: 2, outfit: "shirt", hair: 0, color: 3, seed: 13 },
  { tone: 3, outfit: "dress", hair: 1, color: 0, seed: 7 },
];
// The sick queue's comforts, in person units on a rig R: a crutch, an ice pack, a sling, a hot-water bottle.
function comfort(H, i, R) {
  const { C } = H, ink = C.line, k = i % 4;
  if (k === 0) {
    const sx = R.shoulder[1][0] + 4, sy = R.shoulder[1][1] + 4;
    return `<path d="M${f(sx)},${f(sy)} L${f(sx + 6)},100 M${f(sx - 8)},${f(sy)} h16" stroke="${ink}" stroke-width="5" stroke-linecap="round"/><path d="M${f(sx)},${f(sy)} L${f(sx + 6)},100" stroke="#C9CED6" stroke-width="2.2"/>`;
  }
  if (k === 1) return `<path d="M${f(R.top[0] - 12)},${f(R.top[1] + 4)} q12,-14 24,0 q-2,8 -12,8 q-10,0 -12,-8 Z" fill="#9AC3DA" stroke="${ink}" stroke-width="2.2"/>`;
  if (k === 2) return `<path d="M${f(R.shoulder[0][0] - 2)},${f(R.shoulder[0][1] - 2)} L${f(R.shoulder[1][0] + 2)},${f(R.hipY - 22)} L${f(R.shoulder[0][0] + 6)},${f(R.hipY - 16)} Z" fill="${WHITE}" stroke="${ink}" stroke-width="2.2" stroke-linejoin="miter"/>`;
  return `<rect x="-10" y="${f(R.hipY - 30)}" width="22" height="16" rx="6" fill="${C.rust}" stroke="${ink}" stroke-width="2.2"/>`;
}
function queuePerson(H, i, u) {
  const { K } = H, q = qAt(u);
  const o = copy(QOPTS[i % QOPTS.length], { look: "left", arms: [[-14, -50], [8, 4]], light: i % 3 === 1 ? "red" : undefined });
  const R = K.rig(o);
  return stand(K, o, q.x, q.y, q.k, comfort(H, i, R) + at(R.hand[0][0] - 2, R.hand[0][1] - 4, 0.9, ticket(H)));
}
const queue = (H, from, to) => QU.slice(from, to).map((u, i) => queuePerson(H, i + from, u)).reverse().join("");
function field() {
  return `<rect x="-6000" y="${-HZ - 6000}" width="12000" height="6000" fill="${SKY}"/><rect x="-6000" y="${-HZ}" width="12000" height="7000" fill="${GROUND}"/>` +
    `<path d="M-6000,${-HZ} H6000" stroke="#8E7A55" stroke-width="3" opacity="0.6"/>`;
}
function backboard(H) {
  const { C } = H, ink = C.line;
  let tiles = "";
  for (let y = -820; y < 0; y += 40) tiles += `<path d="M-936,${y} H-206" stroke="${TILE_LINE}" stroke-width="2.4"/>`;
  for (let x = -896; x < -206; x += 40) tiles += `<path d="M${x},-860 V0" stroke="${TILE_LINE}" stroke-width="2.4"/>`;
  let stripes = "", scallop = "";
  for (let i = 0; i < 12; i++) {
    const x = -960 + i * 66;
    stripes += `<path d="M${x},-905 H${x + 66} L${x + 70},-845 H${x + 4} Z" fill="${i % 2 ? C.cream : C.rust}"/>`;
    scallop += `<path d="M${-956 + i * 66},-845 a33,20 0 0,0 66,0 Z" fill="${i % 2 ? C.cream : C.rust}" stroke="${ink}" stroke-width="4"/>`;
  }
  return `<rect x="-940" y="-860" width="740" height="860" fill="${TILE}" stroke="${ink}" stroke-width="6"/>` + tiles +
    `<rect x="-936" y="-300" width="732" height="22" fill="${C.navy}" opacity="0.9"/>` +
    `<rect x="-958" y="-860" width="22" height="860" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><rect x="-204" y="-860" width="22" height="860" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>` +
    stripes + `<path d="M-962,-905 H-170 L-166,-845 H-966 Z" fill="none" stroke="${ink}" stroke-width="5"/>` + scallop;
}
function counter(H) {
  const { C } = H, ink = C.line;
  const till = at(-760, -150, 1, `<path d="M-48,0 L-42,-62 H40 L48,0 Z" fill="${C.slate}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/>` +
    `<rect x="-34" y="-96" width="56" height="34" fill="${C.cream}" stroke="${ink}" stroke-width="4"/><path d="M-26,-79 h40" stroke="${C.war}" stroke-width="3"/>` +
    [-30, -14, 2, 18].map((x) => `<rect x="${x}" y="-50" width="10" height="9" fill="${C.cream}" stroke="${ink}" stroke-width="1.6"/>`).join("") +
    `<rect x="-36" y="-26" width="72" height="18" fill="${C.tan}" stroke="${ink}" stroke-width="3"/>`);
  const bell = at(-420, -150, 1, `<path d="M-26,0 H26 V-6 H-26 Z" fill="${C.slate}" stroke="${ink}" stroke-width="3"/><path d="M-20,-6 Q-20,-34 0,-36 Q20,-34 20,-6 Z" fill="#C9CED6" stroke="${ink}" stroke-width="3"/><path d="M0,-36 V-44" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`);
  return `<rect x="-905" y="-150" width="680" height="150" fill="${WHITE}" stroke="${ink}" stroke-width="6"/>` +
    `<rect x="-905" y="-34" width="680" height="34" fill="${C.navy}" stroke="${ink}" stroke-width="5"/>` +
    `<rect x="-915" y="-166" width="700" height="20" fill="#C9CED6" stroke="${ink}" stroke-width="5"/>` +
    `<path d="M-880,-120 H-250 M-880,-90 H-250 M-880,-60 H-250" stroke="#E3DAC2" stroke-width="3"/>` + till + bell;
}
function dispenser(H) {
  const { C } = H, ink = C.line;
  return `<rect x="-86" y="-250" width="12" height="250" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><path d="M-105,0 H-55 V-10 H-105 Z" fill="${C.slate}" stroke="${ink}" stroke-width="3"/>` +
    `<path d="M-117,-250 L-117,-300 Q-80,-330 -43,-300 L-43,-250 Z" fill="${C.war}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/>` +
    `<path d="M-44,-268 l18,2 l-2,14 l-18,-2 Z" fill="${C.war}" stroke="${ink}" stroke-width="2"/>` +
    `<rect x="-170" y="-376" width="180" height="50" fill="#FBF5E4" stroke="${ink}" stroke-width="4"/><rect x="-164" y="-370" width="168" height="38" fill="none" stroke="${C.orange}" stroke-width="2"/>` +
    H.label(-80, -342, 24, "TAKE A NUMBER");
}

// The NOW SERVING count at MP3 time t: 150,001 on "software." in Part 8 (910.02), then one every 0.576 s.
const served = (t) => 150001 + Math.floor((t - 910.02) / 0.576);

// The period title card's emblem (16:9): three orbits, three running war papers, the nucleus.
function emblem(H, t) {
  const { K, C } = H, cx = 960, cy = 300, rx = 200, ry = 62, TILT = [0, 60, -60];
  const orbits = TILT.map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
  const bills = TILT.map((a, i) => {
    const th = i * 2.1 + t * 2.4, ar = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
    return at(cx + ex * Math.cos(ar) - ey * Math.sin(ar), cy + ex * Math.sin(ar) + ey * Math.cos(ar) - 6, 0.62, K.money("war", i % 2));
  }).join("");
  return orbits + bills + `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
}

export default {
  "humanity-has-no-choice-title"(H, fid) {
    const { K, C } = H;
    // KIT.titleScene's atomic card (16:9), as it lays out these lines: THE PART WHERE and HUMANITY HAS (small, 86.4,
    // baselines y 600.5 and 689.7), NO CHOICE (big, 172.7, cap top y 739, baseline 860; the C of CHOICE from x 773
    // to 888).
    const word = (y, s, text) => {
      const t0 = (dx, dy, extra) => `<text x="${960 + dx}" y="${y + dy}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${s}" ${extra}>${H.esc(text)}</text>`;
      return t0(0.04 * s, 0.053 * s, `fill="${C.ink}"`) + t0(0, 0, `fill="${C.cream}" stroke="${C.cream}" stroke-width="${f(0.044 * s)}" stroke-linejoin="round" style="paint-order:stroke"`);
    };
    // the padlock, snapped shut, its shackle over the top arm of the C, hanging in front of the letter
    const lock = at(852, 842, 2.5, K.props.padlock({}), 8);
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + emblem(H, 2.2) + word(600.5, 86.4, "THE PART WHERE") + word(689.7, 86.4, "HUMANITY HAS") + word(860, 172.7, "NO CHOICE") + lock;
    return { svg, alt: "The period title card: on plain navy, the film's atom with its three running papers, and under it THE PART WHERE, HUMANITY HAS, NO CHOICE in cream letters; a big brass padlock hangs snapped shut over the top of the C of CHOICE." };
  },

  "the-twist"(H, fid) {
    const { K, C } = H, St = K.STUDIO, top = St.top, end = St.lect[0] + St.lect[1] / 2;
    // on "because:": the halo on its edge rolling off the right end of the lectern top, motion strokes behind it
    const ring = at(end + 16, top + 22, 1, `<g transform="rotate(18)">${hoop(H, 54)}</g>`);
    const trail = strokes(H, end - 110, top - 80, 3, 24, 50, 0, 4) + `<path d="M${end - 120},${top - 4} q30,-20 60,0 q30,20 60,0" fill="none" stroke="${C.line}" stroke-width="3" stroke-dasharray="10 10" opacity="0.6"/>`;
    const svg = H.host("smirk-smile", "idle", lecternProps(H, 2, false) + at(St.lect[0] + 10, top + 4, 1, mug(H)) + trail + ring);
    return { svg, alt: "Wishonia at her lectern smirks at the camera, hands at her sides, while a gold halo rolls on its edge along the lectern top and off its right end like a hoop; the mug and the Earth case file stand on the lectern." };
  },

  "greed-ropes"(H, fid) {
    const { C } = H;
    // after "from).": the wide framing, the four pulling four ways, the cart shuddering an inch up, a plank flying
    const P = PULLERS;
    const fc = placed(H, P.fatCat, P.fatCat.x, P.fatCat.y, { mood: "greedy" });
    const po = placed(H, P.politician, P.politician.x, P.politician.y, { mood: "grin" });
    const yo = placed(H, P.you, P.you.x, P.you.y);
    const wm = placed(H, P.weaponsMaker, P.weaponsMaker.x, P.weaponsMaker.y, { mood: "grin" }, "med");
    const cx = 0, cy = FEET, lift = 14;
    const corner = (k) => [cx + CART_ROPE[k][0], cy - lift + CART_ROPE[k][1]];
    const ropes = rope(H, corner("ul"), fc.back) + rope(H, corner("ur"), po.back) + rope(H, corner("ll"), yo.back) + rope(H, corner("lr"), wm.back);
    const plank = at(150, -420, 1, `<g transform="rotate(-28)"><rect x="-80" y="-15" width="160" height="30" fill="${C.tan}" stroke="${C.line}" stroke-width="5"/><path d="M-60,-2 H60" stroke="#9A6E44" stroke-width="3"/></g>`) +
      `<path d="M60,-330 q30,-60 90,-70 M250,-360 q-10,-50 -60,-80" fill="none" stroke="${C.line}" stroke-width="4" stroke-dasharray="12 10"/>`;
    const shake = strokes(H, -330, -120, 3, 40, 40, 90, 5) + strokes(H, 300, -120, 3, 40, 40, 90, 5) + `<path d="M-220,${FEET + 6} q-30,-26 -60,-6 M220,${FEET + 6} q30,-26 60,-6" fill="none" stroke="${C.line}" stroke-width="4"/>`;
    const plate = road(H) + ropes + at(cx, cy - lift, 1, cart(H, { plank: true })) + shake + plank +
      // the far pair behind, the near pair in front
      fc.svg + po.svg + yo.svg + wm.svg;
    const svg = view(0, -130, 0.75, plate);
    return { svg, alt: "On a country road across a tan field, a wooden farm cart heaped with green medicine money, the 1% TREATY scroll standing in it, is pulled four ways at once by four ropes in an X: the fat cat upper left, the grinning politician upper right with his cracked hand mirror, YOU in his bowler lower left with a thermometer in his mouth, and the weapons maker lower right cradling his missile; each leans away in a leather harness after the bait dangling from a pole in front of his nose (a 272% bond, a VOTE ballot box, a FREE pill bottle, a green bill); the cart shudders off the road and a plank flies off its side." };
  },

  "cure-death-by-mistake"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "death": the column marching right, the cart's front wheel on the flattened Reaper, two splats behind
    const CX = 2250, P = PULLERS, XS = [CX + 480, CX + 720, CX + 960, CX + 1200];
    const fwd = [[96, 128], [104, 136]];
    const right = (p) => copy(p, { d: 1, hunch: 6, arms: p.cast === "politician" ? p.arms : p.cast === "weaponsMaker" ? undefined : fwd });
    const col = [
      [P.weaponsMaker, XS[0], { mood: "grin" }, "med"],
      [P.you, XS[1], {}],
      [P.politician, XS[2], { mood: "grin" }],
      [P.fatCat, XS[3], { mood: "smug" }],
    ].map(([p, x, o, seal]) => placed(H, right(p), x, FEET, o, seal));
    const front = [CX + CART_ROPE.front[0], FEET + CART_ROPE.front[1]];
    const ropes = col.map((c) => rope(H, front, c.back, false)).join("");
    // the halo on the fat cat's top hat
    const fcR = col[3].R, haloAt = [XS[3] + S * fcR.top[0], FEET - 100 * S + S * (fcR.top[1] - 26)];
    // the Reaper rolled out flat as a pancake under the front wheel (CX + 150): his robe a black puddle, his skull a
    // flat white oval poking out in front of the wheel, one bony hand flat behind it; his scythe sprung up, bent
    const RP = CX + 150;
    const robe = `<path d="M-230,4 C-236,-14 -200,-22 -150,-20 C-80,-28 40,-26 110,-18 C150,-16 160,4 120,12 C40,20 -120,22 -200,16 C-226,14 -232,10 -230,4 Z" fill="#141B2B" stroke="${ink}" stroke-width="5"/>`;
    const skull = `<ellipse cx="136" cy="-2" rx="44" ry="15" fill="${BONE}" stroke="${ink}" stroke-width="4"/><ellipse cx="128" cy="-4" rx="9" ry="5" fill="${ink}"/><ellipse cx="154" cy="-4" rx="9" ry="5" fill="${ink}"/>` +
      `<path d="M132,7 h22 M137,4 v6 M143,4 v6 M149,4 v6" stroke="${ink}" stroke-width="2"/>`;
    const hand = `<path d="M-250,0 l-34,-10 M-250,2 l-38,0 M-250,4 l-34,10 M-250,0 l-20,-4" stroke="${ink}" stroke-width="7" stroke-linecap="round"/><path d="M-250,0 l-34,-10 M-250,2 l-38,0 M-250,4 l-34,10" stroke="${BONE}" stroke-width="3.4" stroke-linecap="round"/>`;
    const flat = at(RP, FEET + 10, 1, robe + skull + hand);
    const scythe = at(RP + 206, FEET + 8, 1, `<path d="M0,0 L-14,-150 L40,-212" fill="none" stroke="${ink}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/><path d="M0,0 L-14,-150 L40,-212" fill="none" stroke="${C.tan}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>` +
      `<path d="M40,-212 C10,-270 -70,-270 -110,-236 C-66,-248 -10,-236 22,-188 Z" fill="${C.cream}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>` +
      `<path d="M-50,-170 q-16,-14 -30,-6 M28,-150 q18,-6 26,10 M-40,-110 q-20,0 -26,14" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`);
    // a dust puff behind every marching heel
    const puffs = XS.map((x) => [[x - 70, FEET + 2, 16], [x - 96, FEET - 8, 11]].map(([px, py, r]) => `<circle cx="${px}" cy="${py}" r="${r}" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>`).join("")).join("");
    const plate = road(H) + splat(H, 1660, "CANCER") + splat(H, 1890, "HEART DISEASE") + ropes + flat + at(CX, FEET, 1, cart(H)) + scythe +
      puffs + col.map((c) => c.svg).join("") + at(haloAt[0], haloAt[1], 1, halo(H, 0.9));
    const svg = view(2760, -210, 0.84, plate);
    return { svg, alt: "The column marches right along the road, all four in step, eyes up on the four baits dangling ahead of them in one row (the fat cat first, a halo on his top hat, then the politician, YOU and the weapons maker), roped to the cart; the cart's front wheel rolls over the Grim Reaper, flattened like a pancake in the road, his scythe sprung up bent; behind the cart two disease blobs in CANCER and HEART DISEASE sashes lie squashed flat, and the brass plaque on the tailgate reads ACCIDENTALLY SAVED HUMANITY WHILE GETTING RICH." };
  },

  "cheese-genius"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "genius.": the prize table on the free wall right of the lectern (16:9)
    const T = 1470, TY = 742;
    const cloth = `<path d="M${T - 280},${TY} L${T - 312},1090 H${T + 312} L${T + 280},${TY} Z" fill="${C.cream}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      [-200, -100, 0, 100, 200].map((x) => `<path d="M${T + x},${TY + 40} L${T + x * 1.1},1080" stroke="#D9CBA4" stroke-width="5"/>`).join("") +
      `<path d="M${T - 304},1040 H${T + 304}" stroke="${C.rust}" stroke-width="18"/>` +
      `<ellipse cx="${T}" cy="${TY}" rx="282" ry="34" fill="${WHITE}" stroke="${ink}" stroke-width="5"/>`;
    // the display stand and the cheese wedge with its holes, wearing the GENIUS rosette
    const sx = T - 150, sTop = TY - 96;
    const stand0 = `<path d="M${sx - 54},${TY - 2} h108 l-12,-16 h-84 Z M${sx - 16},${TY - 18} h32 l-6,-56 h-20 Z M${sx - 66},${sTop + 22} h132 v-14 h-132 Z" fill="${C.rust}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/>` +
      `<ellipse cx="${sx}" cy="${TY - 46}" rx="20" ry="8" fill="${C.tan}" stroke="${ink}" stroke-width="3"/>`;
    // the wedge seen from its side: a thick rind-edged slab rising to a point at the back left, its cut face full of holes
    const cheeseTop = sTop + 8, CY2 = "#F2C65A", RIND = "#D9A23A";
    const cheese = `<path d="M${sx - 120},${cheeseTop} L${sx + 118},${cheeseTop} L${sx + 118},${cheeseTop - 70} L${sx - 104},${cheeseTop - 150} Z" fill="${CY2}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      `<path d="M${sx + 118},${cheeseTop - 70} L${sx - 104},${cheeseTop - 150} L${sx - 86},${cheeseTop - 160} L${sx + 134},${cheeseTop - 80} L${sx + 134},${cheeseTop - 10} L${sx + 118},${cheeseTop} Z" fill="${RIND}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/>` +
      [[-70, -36, 15], [-20, -20, 11], [30, -40, 13], [80, -24, 10], [-50, -86, 10], [0, -68, 7], [60, -60, 6], [-90, -14, 7]].map(([x, y, r]) => `<ellipse cx="${sx + x}" cy="${cheeseTop + y}" rx="${r}" ry="${f(r * 0.8)}" fill="#C8902E" stroke="${ink}" stroke-width="2.4"/>`).join("") +
      `<path d="M${sx - 120},${cheeseTop} h50 q8,10 0,20 l-6,-18 Z" fill="${RIND}" stroke="${ink}" stroke-width="2.4"/>`;
    let scal = "";
    for (let i = 0; i < 16; i++) { const a = (i / 16) * Math.PI * 2; scal += `<circle cx="${f(52 * Math.cos(a))}" cy="${f(52 * Math.sin(a))}" r="14" fill="${C.war}" stroke="${ink}" stroke-width="3"/>`; }
    // the rosette hangs on a ribbon from the wedge's point, over the front edge
    const rosette = at(sx + 92, cheeseTop - 74, 0.6, `<path d="M-22,30 L-44,118 L-26,106 L-14,124 L4,36 Z M22,30 L44,118 L26,106 L14,124 L-4,36 Z" fill="${C.med}" stroke="${ink}" stroke-width="3.5" stroke-linejoin="round"/>` + scal +
      `<circle r="50" fill="${C.war}" stroke="${ink}" stroke-width="3"/><circle r="40" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>` +
      `<text y="7" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="19" letter-spacing="0.5" fill="${ink}">GENIUS</text>`);
    const ribbon = `<path d="M${sx - 96},${cheeseTop - 152} Q${sx + 10},${cheeseTop - 150} ${sx + 92},${cheeseTop - 100}" fill="none" stroke="${ink}" stroke-width="9"/><path d="M${sx - 96},${cheeseTop - 152} Q${sx + 10},${cheeseTop - 150} ${sx + 92},${cheeseTop - 100}" fill="none" stroke="${C.med}" stroke-width="5"/>`;
    const sparkle = (x, y, r) => `<path d="M${x},${y - r} L${x + r * 0.25},${y - r * 0.25} L${x + r},${y} L${x + r * 0.25},${y + r * 0.25} L${x},${y + r} L${x - r * 0.25},${y + r * 0.25} L${x - r},${y} L${x - r * 0.25},${y - r * 0.25} Z" fill="${C.yellow}" stroke="${ink}" stroke-width="2.4"/>`;
    const sparkles = sparkle(sx - 120, cheeseTop - 150, 18) + sparkle(sx + 120, cheeseTop - 120, 14) + sparkle(sx - 30, cheeseTop - 190, 12) + sparkle(sx + 70, cheeseTop - 180, 10);
    // the milk bottle, gone green, swollen, its cap blown off (lying on the table), cracks in the glass
    // a 1950s glass quart bottle (pale glass, a rolled lip, ribbed shoulders), its milk gone green and swollen into a
    // bulge, the glass cracked, the cap blown off and green fumes rising out of the neck
    const bx = T + 70, GREEN = "#9DB25A", GLASS = "#DDEBEA";
    const glass = `<path d="M${bx - 20},${TY - 226} H${bx + 20} L${bx + 22},${TY - 210} L${bx + 18},${TY - 196} Q${bx + 26},${TY - 160} ${bx + 56},${TY - 136} Q${bx + 84},${TY - 96} ${bx + 70},${TY - 40} Q${bx + 62},${TY - 4} ${bx},${TY - 4} Q${bx - 62},${TY - 4} ${bx - 70},${TY - 40} Q${bx - 84},${TY - 96} ${bx - 56},${TY - 136} Q${bx - 26},${TY - 160} ${bx - 18},${TY - 196} L${bx - 22},${TY - 210} Z" fill="${GLASS}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>`;
    const milk = `<path d="M${bx - 14},${TY - 186} H${bx + 14} Q${bx + 22},${TY - 156} ${bx + 50},${TY - 132} Q${bx + 76},${TY - 96} ${bx + 63},${TY - 42} Q${bx + 56},${TY - 12} ${bx},${TY - 12} Q${bx - 56},${TY - 12} ${bx - 63},${TY - 42} Q${bx - 76},${TY - 96} ${bx - 50},${TY - 132} Q${bx - 22},${TY - 156} ${bx - 14},${TY - 186} Z" fill="${GREEN}"/>` +
      [[-30, -70, 9], [22, -100, 7], [10, -40, 11], [-12, -140, 6]].map(([x, y, r]) => `<circle cx="${bx + x}" cy="${TY + y}" r="${r}" fill="#B9C97A" stroke="#6E8436" stroke-width="2"/>`).join("");
    const shine = `<path d="M${bx - 46},${TY - 118} q-14,34 -4,70" fill="none" stroke="${WHITE}" stroke-width="7" stroke-linecap="round" opacity="0.9"/>` +
      `<path d="M${bx + 38},${TY - 128} l-14,24 l16,8 l-12,26 M${bx + 60},${TY - 66} l-16,-10 l-8,18" fill="none" stroke="${ink}" stroke-width="2.6"/>`;
    const fumes = `<path d="M${bx - 10},${TY - 232} q-28,-30 -8,-62 q16,-26 -4,-52 M${bx + 8},${TY - 234} q22,-34 2,-66 q-14,-24 8,-50 M${bx + 22},${TY - 228} q30,-14 30,-48" fill="none" stroke="${ink}" stroke-width="10" stroke-linecap="round"/>` +
      `<path d="M${bx - 10},${TY - 232} q-28,-30 -8,-62 q16,-26 -4,-52 M${bx + 8},${TY - 234} q22,-34 2,-66 q-14,-24 8,-50 M${bx + 22},${TY - 228} q30,-14 30,-48" fill="none" stroke="${GREEN}" stroke-width="5" stroke-linecap="round"/>`;
    const bottle = glass + milk + shine + fumes;
    const cap = at(bx + 130, TY + 6, 1, `<ellipse cx="0" cy="0" rx="24" ry="8" fill="#C9CED6" stroke="${ink}" stroke-width="3"/><path d="M-24,0 v-8 h48 v8" fill="#C9CED6" stroke="${ink}" stroke-width="3"/>`, -8);
    // the tear-off calendar, stripped to its last page, the torn pages on the cloth
    const cal = at(T + 252, TY + 2, 1.5, K.props.calendar({ month: "DEC", day: 31 }));
    const torn = [[T + 120, TY + 26, -20], [T + 300, TY + 30, 14], [T + 250, TY + 70, -8], [T - 20, TY + 60, 24]].map(([x, y, r]) => at(x, y, 1, `<path d="M-24,-16 H24 L20,16 H-26 Z" fill="${WHITE}" stroke="${ink}" stroke-width="2.6" stroke-linejoin="miter"/><rect x="-24" y="-16" width="48" height="9" fill="${C.war}"/>`, r)).join("");
    const front = lecternProps(H) + cloth + torn + stand0 + cheese + ribbon + rosette + bottle + cap + cal + sparkles;
    const svg = H.host("excited-open", "wide-gesture", front);
    return { svg, alt: "Wishonia throws her arms wide at her lectern; beside her on a county-fair prize table, a wedge of cheese on a little wooden stand wears a GENIUS rosette among sparkles, a milk bottle beside it has gone green, swollen and cracked with its cap blown off onto the cloth, and a tear-off calendar is stripped to its last page, DEC 31, its torn pages scattered." };
  },

  "doubling-starts"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "starts.": the wide framing: behind YOU at his desk, the voters fanned out in rows of 2, 4, 8 and 16, the
    // last row's outermost still flying in on their hooks; the tally board rolling past 1,023, the bird flapping off
    const VAR = [
      { tone: 0, outfit: "dress", hair: 1, color: 3, seed: 4 }, { tone: 3, outfit: "suit", color: 1, seed: 6 },
      { tone: 2, outfit: "shirt", color: 0, seed: 9 }, { tone: 1, outfit: "dress", hair: 1, color: 2, seed: 11 },
      { tone: 0, outfit: "suit", hair: 2, color: 2, seed: 2 }, { tone: 2, outfit: "shirt", color: 3, seed: 13 },
      { tone: 3, outfit: "dress", hair: 1, color: 0, seed: 7 }, { tone: 1, outfit: "overalls", color: 1, seed: 5 },
    ];
    const btn = K.props.yesButton({ label: "YES", sub: "" });
    // a lit voter: arms up cheering, or one hand holding his YES button up
    const voterOpts = (i) => copy(VAR[i % VAR.length], { light: "teal", mood: "grin", arms: i % 2 === 0 ? [[-150, -170], [150, 170]] : [[-160, -176], [20, 8]] });
    const voter = (i, extra = "") => {
      const po = voterOpts(i), R = K.rig(po);
      return K.person(po) + (i % 2 === 0 ? "" : at(R.hand[0][0], R.hand[0][1] + 6, 0.34, btn)) + extra;
    };
    const place = (x, y, k, inner) => at(x, y - 100 * k, k, inner);
    // the first two friends keep what they were in the middle of: his dinner fork (a meatball on it), her curlers
    const forkMan = (() => {
      const po = copy(VAR[1], { light: "teal", mood: "grin", arms: [[-150, -170], [150, 170]] }), R = K.rig(po), h = R.hand[1];
      const fork = at(h[0], h[1], 1, `<path d="M0,0 V-26 M-5,-26 V-38 M0,-26 V-40 M5,-26 V-38 M-5,-26 H5" fill="none" stroke="${ink}" stroke-width="2.6" stroke-linecap="round"/><circle cx="0" cy="-44" r="6" fill="#8A4E2E" stroke="${ink}" stroke-width="2"/>`);
      return K.person(po) + fork;
    })();
    const curlers = (() => {
      const po = copy(VAR[0], { light: "teal", mood: "grin", arms: [[-160, -176], [20, 8]] }), R = K.rig(po), [tx, ty] = R.top;
      const roll = [-12, -4, 4, 12].map((dx, j) => `<rect x="${f(tx + dx - 4)}" y="${f(ty - 7 + Math.abs(dx) * 0.35)}" width="8" height="11" rx="3" fill="#E7A0B4" stroke="${ink}" stroke-width="1.8" transform="rotate(${(j - 1.5) * 16} ${f(tx + dx)} ${f(ty)})"/>`).join("");
      return K.person(po) + at(R.hand[0][0], R.hand[0][1] + 6, 0.34, btn) + roll;
    })();
    let rows = "";
    for (let r = FAN.length - 1; r >= 0; r--) {
      const { y, k } = FAN[r], n = 2 << r;
      for (let i = 0; i < n; i++) {
        const x = fanX(r, i);
        // the last row's two outermost on each side are still on their way in
        if (r === 3 && (i < 2 || i > n - 3)) continue;
        const who = r === 0 ? (i === 0 ? forkMan : curlers) : voter(i * 3 + r);
        rows += place(x, y, k, who);
      }
    }
    // the last row's outermost four, yanked in on cane hooks from the outermost voters of the row in front: one each side
    // mid-air on the crook, one each side just landing, staggering
    const flyer = (x, y, rot, k, i) => at(x, y - 100 * k, k, `<g transform="rotate(${rot} 0 50)">${K.person(copy(VAR[i], { mood: "eager", arms: [[-120, -150], [130, 160]] }))}</g>`);
    const r3 = FAN[3], r2 = FAN[2], hk = r2.k;
    // the cane is held in the outer hand of the row-2 voter at that end (voter(i * 3 + 2), as the rows draw him)
    const holder = (side) => {
      const ri = side < 0 ? 0 : 7, R = K.rig(voterOpts(ri * 3 + 2)), h = R.hand[side < 0 ? 0 : 1];
      return [fanX(2, ri) + hk * h[0], r2.y - 100 * hk + hk * h[1]];
    };
    let hooks = "";
    for (const side of [-1, 1]) {
      const [hx, hy] = holder(side), far = fanX(3, side < 0 ? 0 : 15), near = fanX(3, side < 0 ? 1 : 14);
      const fx = far + side * 60, fy = r3.y - 150;
      hooks += flyer(fx, fy, side * 28, r3.k, side < 0 ? 3 : 5) + caneHook(H, hx, hy, fx - side * 4, fy - 100 * r3.k + 30 * r3.k) +
        flyer(near, r3.y - 6, -side * 10, r3.k, side < 0 ? 6 : 2) + strokes(H, fx - side * 70, fy - 80, 3, 26, 60, side < 0 ? 0 : 180, 4);
    }
    // YOU at his little desk, front and center, chest light still red
    const you = place(0, 0, YOU_K, K.person(copy(YOU, { light: "red", mood: "grin", arms: [[-150, -170], [150, 170]] })));
    const dy = -112;
    const desk = `<path d="M-84,${dy + 14} V-2 M84,${dy + 14} V-2" stroke="${ink}" stroke-width="12"/><path d="M-84,${dy + 14} V-2 M84,${dy + 14} V-2" stroke="${C.slate}" stroke-width="6"/>` +
      `<rect x="-76" y="${dy + 30}" width="152" height="26" fill="${C.tan}" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="-104" y="${dy}" width="208" height="16" fill="${C.tan}" stroke="${ink}" stroke-width="4"/>` + at(0, dy, 1.7, K.props.laptop({ screen: "warondisease.org" }));
    const plate = `<rect x="-6000" y="-6000" width="12000" height="${6000 + PLAIN_HZ}" fill="${SKY}"/><rect x="-6000" y="${PLAIN_HZ}" width="12000" height="6000" fill="${GROUND}"/>` +
      `<path d="M-6000,${PLAIN_HZ} H6000" stroke="#8E7A55" stroke-width="3" opacity="0.6"/>` +
      tallyBoard(H, 1023, 4, 2) + rows + hooks + you + desk;
    const svg = view(0, -520, 0.58, plate);
    return { svg, alt: "A bare tan plain under a cream sky: at the front YOU in his bowler at a little school desk with the laptop reading warondisease.org, arms up, his chest light red; behind him the voters fanned out in rows of 2, 4, 8 and 16, each row further back and twice as wide, chest lights teal, cheering or holding up YES buttons (the first two still holding a dinner fork and wearing hair curlers); the last row's outermost voters still flying in on long vaudeville cane hooks; on the horizon a roadside tally board ten flip tiles long reads 0,000,001,023, its right-hand tiles rolling, and a bird flaps off its nest on the leftmost tile with its egg in its beak." };
  },

  "countdown-104"(H, fid) {
    const { K, C } = H, ink = C.line;
    // the HOLD after "humans" (MP3 3396.94): YOU at the counter, the Reaper's finger over the bell, the sign clicking
    const RX = -560, RY = -10 - 100 * SD;
    const reaperArt = at(RX, RY, SD, reaper(H, [(-420 - RX) / SD, (-196 - RY) / SD]));
    const YO = copy(YOU, { look: "left", light: "red", mood: "worried", arms: [[-30, -70], [24, 40]] }), RY0 = K.rig(YO);
    const btn = at(RY0.hand[1][0] + 6, RY0.hand[1][1] + 10, 0.42, K.props.yesButton({ label: "YES", sub: "TREATY" }), -16);
    const you = stand(K, YO, -330, 0, SD, at(RY0.hand[0][0] - 2, RY0.hand[0][1] - 4, 0.9, ticket(H)) + btn);
    // the last customer, a grinning skeleton, strolling out through DELETED
    const bones = stand(K, copy(QOPTS[2], { skeleton: true, look: "left", arms: [[-12, -4], [16, 6]] }), -1010, 0, SD);
    const plate = field() + backboard(H) + at(-300, -205, 1.7, K.props.calendar({ month: "JAN", day: 1 })) + reaperArt + counter(H) +
      at(-560, -650, 1, nowServing(H, served(3396.94), "104 EVERY MINUTE")) + at(-1010, 0, SD, K.props.door({ label: "DELETED", open: 0.62, color: "#5C6F8E" })) + bones +
      dispenser(H) + queue(H, 0, 20) + at(30, 0, 0.95, K.props.diseaseBlob({ mood: "smug" })) + you;
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="${GROUND}"/>` + view(-380, -375, 0.92, plate);
    return { svg, alt: "The Grim Reaper's deli counter: the NOW SERVING sign on its chains reads 154,318, its strip 104 EVERY MINUTE; the Reaper in his paper deli cap holds a bony finger over the counter bell; YOU in his bowler stands at the counter with his red ticket and a YES button under his arm, his chest light red; a grinning skeleton strolls out through the door marked DELETED; behind YOU the queue of sick humans with crutches, ice packs and slings, each holding a red ticket, runs back across the field to the horizon." };
  },

  "eligible-final-stamp"(H, fid) {
    const { K, C } = H, ink = C.line, St = K.STUDIO, cx = St.lect[0], hw = St.lect[1] / 2, top = St.top;
    // on "visit.": the file stamped, the stamp lifted over it, Wishonia side-eyeing the camera; on the free wall the
    // gift-wrapped Earth on its pedestal, YOU on his bony legs thinking, the last saucer yanked up out of the frame
    const fx = cx - hw + 120;
    const file = at(fx, top + 6, 0.82, caseFile(H, 3));
    const stampUp = at(fx - 6, top - 150, 1.25, K.props.stamp({ text: "ELIGIBLE" }), -8);
    const px = 1330, ptop = 760;
    const pedestal = `<path d="M${px - 110},1090 L${px - 90},${ptop + 40} H${px + 90} L${px + 110},1090 Z" fill="${C.cream}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      `<path d="M${px - 60},${ptop + 60} V1080 M${px},${ptop + 60} V1080 M${px + 60},${ptop + 60} V1080" stroke="#D9CBA4" stroke-width="6"/>` +
      `<path d="M${px - 128},${ptop + 40} H${px + 128} L${px + 116},${ptop} H${px - 116} Z" fill="${C.rust}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>`;
    const r = 120, gy = ptop;
    const earth = at(px, gy, 1, K.props.earthGlobe({ r, face: "smile" }));
    const bow = at(px, gy - 2 * r + 8, 1, `<path d="M0,0 C-30,-60 -110,-40 -70,0 C-110,40 -30,40 0,0 C30,-60 110,-40 70,0 C110,40 30,40 0,0 Z" fill="${C.rust}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>` +
      `<path d="M-8,4 L-40,60 M8,4 L40,62" stroke="${ink}" stroke-width="16" stroke-linecap="round"/><path d="M-8,4 L-40,60 M8,4 L40,62" stroke="${C.rust}" stroke-width="9" stroke-linecap="round"/><circle r="16" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>`);
    const ribbons = `<path d="M${px},${gy - 2 * r} V${gy}" stroke="${ink}" stroke-width="22"/><path d="M${px},${gy - 2 * r} V${gy}" stroke="${C.rust}" stroke-width="14"/>`;
    const tag = at(px + 14, gy - 2 * r + 14, 1.5, K.props.priceTag({ text: "TO: HUMANS", angle: 30 }));
    // YOU thinking, chin in hand, his legs bone
    const k = 3.0, yx = 1660, feet = 1066;
    const YO = { look: "left", mood: "flat", arms: [[-6, -2], [-40, -176]] }, R = K.rig(copy(YOU, YO));
    const you = at(yx, feet - 100 * k, k, bonyYou(H, YO, fid));
    const bub = at(yx - 20, feet - 100 * k + k * (R.top[1] - 34) - 40, 1, `<ellipse cx="0" cy="-30" rx="92" ry="54" fill="${WHITE}" stroke="${ink}" stroke-width="5"/><circle cx="-20" cy="40" r="14" fill="${WHITE}" stroke="${ink}" stroke-width="4"/><circle cx="-6" cy="66" r="8" fill="${WHITE}" stroke="${ink}" stroke-width="3.4"/>` +
      `<text x="0" y="-12" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="64" fill="${C.navy}">...</text>`);
    // the last saucer yanked up out of the frame on its string, tilted, a puff of exhaust where it was
    const sau = at(1250, 70, 1, `<path d="M0,-40 V-200" stroke="${ink}" stroke-width="2"/>` + `<g transform="rotate(-16)">${saucer(H)}</g>`) + strokes(H, 1180, 170, 4, 46, 60, 90, 4);
    const puff = [[1240, 262, 44], [1296, 246, 34], [1190, 250, 30], [1262, 294, 26]].map(([x, y, rr]) => `<circle cx="${x}" cy="${y}" r="${rr}" fill="${C.cream}" stroke="${ink}" stroke-width="4"/>`).join("");
    const front = at(cx + hw - 50, top + 4, 1, mug(H)) + file + stampUp + pedestal + ribbons + earth + bow + tag + you + bub + puff + sau;
    const svg = H.host("sideeye-closed", "palms-down", front);
    return { svg, alt: "Wishonia at her lectern side-eyes the camera, palms down; the rubber stamp has just lifted off the Earth case file, where a red bar strikes out MAY BE and a fresh ELIGIBLE FOR OPTIMIZATION lands across it, under SUBOPTIMAL; beside the lectern the smiling engraved Earth sits gift-wrapped on a pedestal with a big bow and a TO: HUMANS tag, YOU stands beside it on bony legs, chin in hand, a ... thought bubble over his bowler, and the last flying saucer is yanked up out of the frame on its string, leaving a puff of exhaust." };
  },
};
