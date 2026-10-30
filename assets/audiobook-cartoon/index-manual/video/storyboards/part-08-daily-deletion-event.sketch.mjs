// Sketches for storyboards/part-08-daily-deletion-event.md: each scene's key frame on a 1920 x 1080 frame (16:9),
// drawn with the production art (kit.js, film.js, the props library). Built into the review sheet by
// tools/storyboard-sheet.mjs.
//
// The shared drawings of the part are here, for the scene authors to copy so every scene draws them the same:
//   nowServing(H, n, strip)  the NOW SERVING sign, 560 x 318 around its center, its chains up from its top corners
//   ticket(H)                the red deli ticket every human holds, about 30 x 17 in person units
//   beetle(H)                the beetle from the chest hatch, about 52 x 30, facing left
//   reaper(H)                the Grim Reaper (KIT.reaper) in his white paper deli cap
//   READER, SEATED           the reader's KIT.person options, standing and in his armchair
//   armchair(H, front)       his orange wingback armchair (back, then the arms and seat in front of him)
//   wrench(H)                the teal wrench, about 96 long
//   kneecap(H, R)            his kneecap sprung out on its coil (R: KIT.rig of the reader)
//   CLERK, eyeshade(H, R)    the CLAIMS clerk's KIT.person options and his green eyeshade (Part 21 copies both)
// Plates are in plate units: on the deli and in the living room the ground (or floor) is y 0 and the cast at the
// front is drawn at scale S = 1.6 (a standing person about 280 tall).

const f = (n) => n.toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});
const at = (x, y, k, inner, rot = 0) => `<g transform="translate(${f(x)},${f(y)})${rot ? ` rotate(${rot})` : ""}${k !== 1 ? ` scale(${k})` : ""}">${inner}</g>`;
// A plate framing as KIT.camera places it: plate point (x, y) in the middle of the frame, at scale s.
const view = (x, y, s, inner) => `<g transform="translate(${f(960 - x * s)},${f(540 - y * s)}) scale(${s})">${inner}</g>`;
// A host shot's slow push in on her face (KIT.studio), k of the way along.
const push = (S, k, inner) => `<g transform="translate(${S.face[0]},${S.face[1]}) scale(${k}) translate(${-S.face[0]},${-S.face[1]})">${inner}</g>`;
// A person standing on groundY at x, scale k (KIT.person is drawn with its feet at y 100).
const stand = (K, o, x, groundY, k, extra = "") => at(x, groundY - 100 * k, k, K.person(o) + extra);

const S = 1.6;
const GROUND = "#C8B07B", SKY = "#EFE3C4", HZ = 560;
const TILE = "#F1EAD6", TILE_LINE = "#D8CFB4", OIL = "#141018", BONE = "#F1EAD6";

// ── Shared drawings ─────────────────────────────────────────────────────

// The NOW SERVING sign around its center: a navy enamel box with an orange rule, NOW SERVING across the top, six
// flip digits (mustard on slate tiles, a comma after the third) and a cream strip along the bottom. n: the count;
// strip: the strip's words ("" for the blank strip before "hours"). Its chains rise 100 from its top corners.
export function nowServing(H, n, strip = "EVERY 24 HOURS") {
  const { C } = H, ink = C.line;
  const digits = String(n).padStart(6, "0").slice(-6);
  let tiles = "";
  const tw = 62, th = 96, gap = 9, comma = 22, x0 = -(6 * tw + 5 * gap + comma) / 2;
  for (let i = 0; i < 6; i++) {
    const x = x0 + i * (tw + gap) + (i >= 3 ? comma : 0);
    tiles += `<rect x="${f(x)}" y="-66" width="${tw}" height="${th}" rx="5" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>` +
      `<text x="${f(x + tw / 2)}" y="8" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="78" fill="${C.yellow}">${digits[i]}</text>` +
      `<path d="M${f(x + 2)},-18 h${tw - 4}" stroke="#111A2C" stroke-width="2.5"/>`;
  }
  const cx = x0 + 3 * tw + 2 * gap + gap / 2 + comma / 2 - 2;
  tiles += `<text x="${f(cx)}" y="20" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="64" fill="${C.cream}">,</text>`;
  const chain = (x) => {
    let c = "";
    for (let y = -159; y > -260; y -= 16) c += `<ellipse cx="${x}" cy="${y - 8}" rx="5" ry="9" fill="none" stroke="${ink}" stroke-width="3.5"/>`;
    return c;
  };
  return chain(-220) + chain(220) +
    `<rect x="-273" y="-150" width="574" height="324" rx="12" fill="${ink}" opacity="0.85"/>` +
    `<rect x="-280" y="-159" width="560" height="318" rx="12" fill="${C.navy}" stroke="${ink}" stroke-width="6"/>` +
    `<rect x="-264" y="-143" width="528" height="286" rx="7" fill="none" stroke="${C.orange}" stroke-width="4"/>` +
    `<circle cx="-220" cy="-159" r="9" fill="${C.slate}" stroke="${ink}" stroke-width="3"/><circle cx="220" cy="-159" r="9" fill="${C.slate}" stroke="${ink}" stroke-width="3"/>` +
    `<text x="0" y="-88" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="50" letter-spacing="5" fill="${C.cream}">NOW SERVING</text>` + tiles +
    `<rect x="-232" y="52" width="464" height="74" rx="4" fill="${C.cream}" stroke="${ink}" stroke-width="4"/>` +
    (strip ? `<text x="0" y="103" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="42" letter-spacing="3" fill="${C.navy}">${H.esc(strip)}</text>` : "");
}

// The red deli ticket, in person units, around (0, 0): a perforated left edge and a number nobody can read.
export function ticket(H) {
  const { C } = H, ink = C.line;
  return `<g transform="rotate(-12)"><path d="M-15,-8 H15 V8 H-15 l3,-2.7 l-3,-2.6 l3,-2.7 l-3,-2.7 l3,-2.6 Z" fill="${C.war}" stroke="${ink}" stroke-width="1.8" stroke-linejoin="miter"/>` +
    `<rect x="-7" y="-4" width="17" height="8" fill="none" stroke="${C.cream}" stroke-width="1.4"/><path d="M-4,0 h11" stroke="${C.cream}" stroke-width="1.6"/></g>`;
}

// The beetle: a fat slate beetle facing left, its shell split down the middle, six legs, two antennae; around (0, 0).
export function beetle(H) {
  const { C } = H, ink = C.line;
  const legs = [-10, 0, 10].map((x) => `<path d="M${x},6 l-6,12 M${x + 2},6 l6,12" stroke="${ink}" stroke-width="2.6" stroke-linecap="round"/>`).join("");
  return legs + `<path d="M-14,-12 L12,-15 L24,-4 L22,8 L-12,10 L-18,0 Z" fill="${C.slate}" stroke="${ink}" stroke-width="2.6" stroke-linejoin="miter"/>` +
    `<path d="M-14,-1 L22,-3" stroke="${C.orange}" stroke-width="1.6"/><path d="M4,-14 L6,9" stroke="${ink}" stroke-width="1.8"/>` +
    `<path d="M-14,-8 L-26,-9 L-28,1 L-17,4 Z" fill="${ink}"/><circle cx="-23" cy="-4" r="1.8" fill="${C.cream}"/>` +
    `<path d="M-26,-8 q-6,-8 -12,-8 M-24,-9 q-2,-9 -8,-12" fill="none" stroke="${ink}" stroke-width="1.8" stroke-linecap="round"/>`;
}

// The Grim Reaper in a white paper deli cap (a folded garrison cap on his hood), feet at y 100. bell: his bony arm
// reaches out to his left (screen right) and hovers a finger over a counter bell at (bell[0], bell[1]), in his units.
export function reaper(H, bell) {
  const { K, C } = H, ink = C.line;
  const cap = `<path d="M-23,-160 L-18,-176 L4,-184 L20,-176 L24,-160 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="3" stroke-linejoin="miter"/>` +
    `<path d="M-20,-166 L22,-166" stroke="${C.orange}" stroke-width="2.4"/><path d="M2,-182 L4,-166" stroke="${ink}" stroke-width="1.6"/>`;
  // the arm on the bell's side turns to point at it
  const arms = [0, 0];
  if (bell) {
    const i = bell[0] < 0 ? 0 : 1, sh = K.REAPER.shoulder[i];
    arms[i] = (Math.atan2(Math.abs(bell[0] - sh[0]), bell[1] - sh[1]) * 180) / Math.PI;
  }
  return K.reaper({ pose: "puppet", arms }) + `<g transform="translate(0,-14)">${cap}</g>`;
}

// The reader: an everyday human in a shirt and glasses. SEATED: in his armchair, facing left, the book up.
export const READER = { tone: 1, outfit: "shirt", color: 1, hair: 0, glasses: true, seed: 8 };
export const SEATED = copy(READER, { look: "left", build: { legPose: [[-88, -2], [-82, 4]] }, arms: [[-70, -128], [-58, -118]] });

// His armchair around its center x 0, standing on the floor y 0, in plate units (the reader at scale 1.6 sits with
// his hips at y -58). front false: the back (behind him); front true: the arms and the seat front (in front of him).
export function armchair(H, front) {
  const { C } = H, ink = C.line;
  if (!front) {
    return `<path d="M-74,-56 L-82,-236 L-62,-272 L62,-272 L82,-236 L74,-56 Z" fill="${C.orange}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      `<path d="M-56,-236 L-52,-80 M56,-236 L52,-80" stroke="${C.rust}" stroke-width="3"/>` +
      `<path d="M-96,-66 L96,-66 L100,-34 L-100,-34 Z" fill="${C.rust}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>`;
  }
  const arm = (x, s) => `<path d="M${x},-124 L${x + s * 34},-128 L${x + s * 38},-30 L${x + s * 4},-28 Z" fill="${C.orange}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    `<path d="M${x - s * 4},-128 Q${x + s * 17},-150 ${x + s * 38},-128" fill="${C.orange}" stroke="${ink}" stroke-width="5"/>`;
  return arm(-112, 1) + arm(112, -1) + `<path d="M-100,-36 H100 V-14 H-100 Z" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>` +
    `<path d="M-92,-14 L-95,0 M92,-14 L95,0" stroke="${ink}" stroke-width="8" stroke-linecap="square"/>`;
}

// The teal wrench, about 96 long along its own x axis, its jaw at the +x end.
export function wrench(H) {
  const { C } = H, ink = C.line;
  return `<path d="M-48,-6 H22 V6 H-48 Z" fill="${C.med}" stroke="${ink}" stroke-width="3.4"/>` +
    `<path d="M20,-14 L44,-18 L48,-8 L34,-6 L34,6 L48,8 L44,18 L20,14 Z" fill="${C.med}" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/>` +
    `<circle cx="-41" cy="0" r="3" fill="${ink}"/><path d="M-32,-2 H14" stroke="#9AD3CB" stroke-width="2.4"/>`;
}

// His kneecap sprung out on its coil, in person units: a steel spring from his front knee and the kneecap on its end.
export function kneecap(H, R) {
  const { C } = H, ink = C.line;
  const kx = R.hip[0][0] - 4, ky = R.hipY + 24, pts = [];
  for (let i = 0; i <= 8; i++) pts.push(`${f(kx - i * 4.2)},${f(ky + (i === 0 || i === 8 ? 0 : i % 2 ? -5 : 5))}`);
  const d = "M" + pts.join(" L");
  return `<path d="${d}" fill="none" stroke="${ink}" stroke-width="4.2" stroke-linejoin="miter"/><path d="${d}" fill="none" stroke="#C9CED6" stroke-width="2"/>` +
    `<path d="M${f(kx - 34)},${f(ky - 9)} L${f(kx - 44)},${f(ky - 7)} L${f(kx - 47)},${f(ky + 2)} L${f(kx - 42)},${f(ky + 9)} L${f(kx - 33)},${f(ky + 8)} Z" fill="${BONE}" stroke="${ink}" stroke-width="2.2" stroke-linejoin="miter"/>`;
}

// The CLAIMS clerk (holocaust-every-40-days; Part 21's insurance clerk): an everyday human in a suit, bald, mood
// "greedy" when the dollar signs ring up. eyeshade(H, R): his green celluloid eyeshade over his brow, in person units
// (R: KIT.rig of the clerk with the options he is drawn with).
export const CLERK = { tone: 0, outfit: "suit", hair: 2, color: 1, seed: 21 };
export function eyeshade(H, R) {
  const { C } = H;
  return `<path d="M-24,${f(R.hy - 6)} L24,${f(R.hy - 6)} L30,${f(R.hy + 4)} L-22,${f(R.hy + 4)} Z" fill="${C.med}" stroke="${C.line}" stroke-width="2"/>`;
}

// ── The deli plate ──────────────────────────────────────────────────────
// Ground y 0 at the front of the counter, the horizon at y -HZ. The stall: the DELETED door (x -1010), the counter
// (x -905 to -225, its top at y -150) with the till (x -760) and the bell (x -420), the Reaper behind it (x -560),
// the cream-tiled backboard under its striped awning (top y -905), the sign hanging from the awning (center x -560,
// y -650), the calendar on the backboard (x -300, its foot at y -205), the TAKE A NUMBER dispenser (x -80) and the
// blob beside it (x 30). The queue runs from Q0 toward the vanishing point QVP; qAt(u) places a human u of the way.
const QVP = [1600, -HZ], Q0 = [90, 0];
const qAt = (u) => ({ x: Q0[0] + (QVP[0] - Q0[0]) * u, y: Q0[1] + (QVP[1] - Q0[1]) * u, k: S * (1 - u) });
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
function queuePerson(H, i, u, extra = {}) {
  const { K } = H, q = qAt(u);
  const o = copy(QOPTS[i % QOPTS.length], copy({ look: "left", arms: [[-14, -50], [8, 4]], light: i % 3 === 1 ? "red" : undefined }, extra));
  const R = K.rig(o);
  return stand(K, o, q.x, q.y, q.k, at(R.hand[0][0] - 2, R.hand[0][1] - 4, 0.9, ticket(H)));
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
  return `<rect x="-905" y="-150" width="680" height="150" fill="#FBF6E6" stroke="${ink}" stroke-width="6"/>` +
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
function door(H, open = 0) {
  return at(-1010, 0, S, H.K.props.door({ label: "DELETED", open, color: "#5C6F8E" }));
}

// ── The living room plate ───────────────────────────────────────────────
// Floor y 0. The living room from x -1800 to 0 (mustard wallpaper, a rust rug), the cutaway wall x 0 to 46, the
// doctor's office from x 46 to 1200 (pale teal). The lamp at x -640, the armchair at x -360, the empty chair at
// x 200, the desk at x 430, the doctor at x 570, the calendar on the office wall at x 660.
const CHAIR_X = -360;
function lamp(H) {
  const { C } = H, ink = C.line;
  return `<path d="M-40,0 H40 L32,-14 H-32 Z" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><path d="M0,-14 V-400" stroke="${ink}" stroke-width="8"/><path d="M0,-14 V-400" stroke="#C9CED6" stroke-width="3.4"/>` +
    `<path d="M-58,-384 L-34,-474 H34 L58,-384 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/><path d="M-34,-474 H34" stroke="${C.orange}" stroke-width="4"/>`;
}
function livingRoom(H, extra) {
  const { C } = H, ink = C.line;
  let paper = "";
  for (let x = -1800; x < 0; x += 64) paper += `<path d="M${x + 32},-1400 V-20" stroke="#D9BA7E" stroke-width="9"/>`;
  return `<rect x="-1800" y="-1400" width="1800" height="1400" fill="#E3C88F"/>` + paper +
    `<rect x="46" y="-1400" width="1154" height="1400" fill="#BFD8D2"/><path d="M46,-300 H1200" stroke="#9DBFB8" stroke-width="8"/>` +
    `<rect x="0" y="-1400" width="46" height="1400" fill="#6B5B45" stroke="${ink}" stroke-width="5"/><path d="M8,-1400 V0 M38,-1400 V0" stroke="#8A7558" stroke-width="3"/>` +
    `<rect x="-1800" y="0" width="3000" height="600" fill="#7A5634"/><path d="M-1800,0 H1200" stroke="${ink}" stroke-width="6"/>` +
    `<path d="M-640,6 L-110,6 L-70,46 L-680,46 Z" fill="${C.rust}" stroke="${ink}" stroke-width="4"/>` + extra;
}
// The reader in his armchair, reading the manual, his ticket for a bookmark.
function readerInChair(H) {
  const { K } = H, R = K.rig(SEATED);
  const hx = (R.hand[0][0] + R.hand[1][0]) / 2, hy = (R.hand[0][1] + R.hand[1][1]) / 2;
  const book = at(hx - 8, hy + 10, 0.4, K.props.manual()) + at(hx - 6, hy - 40, 0.7, ticket(H), 70);
  // his hips (SEATED's rig hipY, 64.6 in person units) on the seat at y -58
  return at(CHAIR_X, 0, 1, armchair(H, false)) + at(CHAIR_X, -58 - R.hipY * S, S, K.person(SEATED) + book) + at(CHAIR_X, 0, 1, armchair(H, true));
}

export default {
  "daily-deletion-event-title"(H, fid) {
    const { K, C } = H, ink = C.line;
    // KIT.titleScene's atomic card (16:9): the emblem at (960, 300); the heading as the card lays it out:
    // THE PROBLEM (label, 73), THE DAILY (small, 87), DELETION EVENT (big, 174; DELETION from x 178 to 1094, its
    // cap top at y 739).
    const cx = 960, cy = 300, rx = 200, ry = 62, TILT = [0, 60, -60], t = 1.5;
    const orbits = TILT.map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = TILT.map((a, i) => {
      const th = i * 2.1 + t * 2.4, ar = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return at(cx + ex * Math.cos(ar) - ey * Math.sin(ar), cy + ex * Math.sin(ar) + ey * Math.cos(ar) - 6, 0.62, K.money("war", i % 2));
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    const word = (y, s, text) => {
      const t0 = (dx, dy, extra) => `<text x="${960 + dx}" y="${y + dy}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${s}" ${extra}>${H.esc(text)}</text>`;
      return t0(0.04 * s, 0.053 * s, `fill="${C.ink}"`) + t0(0, 0, `fill="${C.cream}" stroke="${C.cream}" stroke-width="${f(0.044 * s)}" stroke-linejoin="round" style="paint-order:stroke"`);
    };
    const label = `<text x="960" y="599" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="73" letter-spacing="3" fill="${C.cream}" stroke="${C.ink}" stroke-width="7" style="paint-order:stroke">THE PROBLEM</text>`;
    // the little woman on top of DELETION, rubbed out from the shoulders up, the pencil's eraser on her
    const WOMAN = { tone: 2, outfit: "dress", hair: 1, color: 0, seed: 5, look: "right", arms: [[10, 4], [-34, -64]] }, k = 1.35, wx = 470, wy = 741;
    const R = K.rig(WOMAN);
    const bag = at(R.hand[1][0] + 2, R.hand[1][1] + 2, 1, `<path d="M-9,0 L9,0 L11,14 L-11,14 Z" fill="${C.rust}" stroke="${ink}" stroke-width="2.4" stroke-linejoin="miter"/><path d="M-6,0 Q0,-9 6,0" fill="none" stroke="${ink}" stroke-width="2.2"/>`);
    const cut = -6; // person units: everything above it is rubbed out
    const woman = `<defs><clipPath id="${fid}-rub"><rect x="-200" y="${cut}" width="400" height="200"/></clipPath></defs>` +
      at(wx, wy - 100 * k, k, `<g clip-path="url(#${fid}-rub)">${K.person(WOMAN)}</g>` + bag);
    const ey = wy - 100 * k + cut * k;
    const pencil = `<g transform="translate(${wx + 4},${f(ey - 2)}) scale(3.6) rotate(84) translate(-157,70)">${K.pencil()}</g>`;
    const crumbs = [[-48, -6, 6], [-74, 10, 5], [40, -20, 6], [64, -2, 4.5], [-26, -38, 4.5], [22, -46, 5.5], [84, -30, 4], [-6, -16, 5], [-92, -24, 4]]
      .map(([dx, dy, r0], i) => { const r = r0 * 1.7; return `<path d="M${f(wx + dx - r)},${f(ey + dy)} l${r},${-r * 0.8} l${r},${r * 0.6} l${-r * 0.4},${r} Z" fill="${i % 2 ? "#E9B4C1" : "#F2D7C0"}" stroke="${ink}" stroke-width="1.6"/>`; }).join("");
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus + label + word(689, 87, "THE DAILY") + word(860, 174, "DELETION EVENT") +
      woman + crumbs + pencil;
    return { svg, alt: "The period title card: on plain navy, the film's atom with its three running papers, and under it THE PROBLEM, THE DAILY, DELETION EVENT in cream letters; on top of DELETION a giant pencil's eraser is rubbing out a little woman from the shoulders up, her dress, legs and handbag still there, eraser crumbs flying." };
  },

  "deletion-board"(H, fid) {
    const { K } = H;
    // On "hours": the wide framing of the deli. The fat cat's skeleton at the DELETED door, the barrel man at the
    // counter, the strip just flipped to EVERY 24 HOURS, the Reaper's finger over the bell.
    const FAT = K.castOpts("richHuman", { skeleton: true, look: "left", arms: [[-14, -40], [-150, -175]] });
    const BARREL = { tone: 2, outfit: "overalls", color: 1, hair: 2, seed: 3, look: "left", light: "red", arms: [[-30, -70], [8, 4]] };
    const RB = K.rig(BARREL);
    const barrel = stand(K, BARREL, -330, 0, S, at(RB.hand[0][0] - 2, RB.hand[0][1] - 4, 0.9, ticket(H)));
    // the Reaper stands behind the counter (feet at y -10); the bell top is at plate (-420, -194)
    const RX = -560, RY = -10 - 100 * S;
    const reaperArt = at(RX, RY, S, reaper(H, [(-420 - RX) / S, (-196 - RY) / S]));
    const plate = field() + backboard(H) + at(-300, -205, 1.7, K.props.calendar({ month: "JAN", day: 1 })) + reaperArt + counter(H) +
      at(-560, -650, 1, nowServing(H, 150000)) + door(H, 0.62) + stand(K, FAT, -1010, 0, S) + dispenser(H) + queue(H, 0, 20) +
      at(30, 0, 0.95, K.props.diseaseBlob({ mood: "smug" })) + barrel;
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="${GROUND}"/>` + view(-380, -375, 0.92, plate);
    return { svg, alt: "The Grim Reaper's deli counter on an open field: the NOW SERVING sign on its chains reads 150,000, EVERY 24 HOURS; the Reaper stands behind the counter in a paper deli cap, a bony finger over the bell, a till beside him and a calendar on the tiled wall; at the left the fat cat's grinning skeleton, top hat and monocle on, walks out through a door marked DELETED; a barrel of a man in overalls waits at the counter with a red ticket, a smug disease blob stands by the TAKE A NUMBER dispenser, and the queue of ticket-holders runs back across the field to the horizon." };
  },

  "holocaust-every-40-days"(H, fid) {
    const { K, C } = H, ink = C.line;
    // After "part).": the CLAIMS booth a little way back along the queue (u 0.215), the toppled heap of forms with
    // the bony hand, the clerk with dollar-sign eyes and his stamp raised in the window.
    const b = qAt(0.215), bk = b.k;
    const booth = at(b.x, b.y, bk,
      `<path d="M-80,-200 L-68,-226 H68 L80,-200 Z" fill="${C.rust}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/>` +
      `<rect x="-68" y="-200" width="136" height="200" fill="#E2B866" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="-68" y="-26" width="136" height="26" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="-52" y="-176" width="104" height="84" fill="${C.ink}"/>` +
      `<rect x="-60" y="-276" width="120" height="44" fill="#FBF5E4" stroke="${ink}" stroke-width="4"/><path d="M-40,-232 V-226 M40,-232 V-226" stroke="${ink}" stroke-width="4"/>` +
      H.label(0, -243, 30, "CLAIMS"));
    const ledge = at(b.x, b.y, bk, `<rect x="-60" y="-98" width="132" height="10" fill="${C.tan}" stroke="${ink}" stroke-width="3"/>`);
    // the clerk in the window: head and shoulders, a green eyeshade, dollar-sign eyes, his stamp raised
    const CO = copy(CLERK, { mood: "greedy", arms: [[10, 4], [150, 172]] });
    const RC = K.rig(CO);
    const clerkArt = K.person(CO) + eyeshade(H, RC) + at(RC.hand[1][0], RC.hand[1][1] + 6, 0.5, K.props.stamp({ text: "", color: C.war }));
    const ck = bk * 0.78;
    const clerk = `<defs><clipPath id="${fid}-win"><rect x="${f(b.x - 52 * bk)}" y="${f(b.y - 300 * bk)}" width="${f(104 * bk)}" height="${f(208 * bk)}"/></clipPath></defs>` +
      `<g clip-path="url(#${fid}-win)">${at(b.x - 2 * bk, b.y - 128 * bk + 60 * ck, ck, clerkArt)}</g>`;
    // the heap of forms beside the booth, the bony hand poking out of it with a pen, DENIED on the top form
    const hx = b.x + 150 * bk, hy = b.y;
    const form = `<rect x="-34" y="-22" width="68" height="44" fill="#FBF6E6" stroke="${ink}" stroke-width="2.6"/><path d="M-24,-10 h40 M-24,0 h48 M-24,10 h30" stroke="#B9B3A3" stroke-width="2.4"/>`;
    const sheets = [[-70, -10, -8], [-30, -24, 6], [20, -14, -4], [62, -8, 10], [-52, -40, 14], [0, -48, -10], [42, -34, 4], [-14, -70, 2], [26, -64, -14], [-34, -86, 18], [8, -94, -6]]
      .map(([dx, dy, r]) => at(dx, dy, 1, form, r)).join("");
    const hand = `<path d="M38,-112 L44,-146 L52,-144 L48,-112 Z" fill="${BONE}" stroke="${ink}" stroke-width="2.4"/>` +
      `<path d="M40,-146 l-3,-14 M44,-148 l-1,-16 M48,-147 l2,-15 M51,-145 l5,-11" stroke="${ink}" stroke-width="5.4" stroke-linecap="round"/>` +
      `<path d="M40,-146 l-3,-14 M44,-148 l-1,-16 M48,-147 l2,-15 M51,-145 l5,-11" stroke="${BONE}" stroke-width="3.4" stroke-linecap="round"/>` +
      `<path d="M50,-160 L70,-194" stroke="${ink}" stroke-width="5" stroke-linecap="round"/><path d="M50,-160 L54,-167" stroke="${C.yellow}" stroke-width="3"/>`;
    const heap = at(hx, hy, bk, sheets + at(-6, -94, 1, `<g transform="rotate(-6)">${form}</g>`) + at(-6, -84, 0.5, K.props.stampMark({ text: "DENIED", angle: -8 })) + hand);
    const plate = field() + queue(H, 4, 16) + booth + clerk + ledge + heap;
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="${GROUND}"/>` + view(b.x + 190, b.y - 190, 1.7, plate);
    return { svg, alt: "Beside the queue, a little yellow CLAIMS booth: in its window the clerk in a green eyeshade raises his rubber stamp, dollar signs in his eyes; next to it a toppled heap of forms, the top one stamped DENIED, with one bony hand poking out of it, still writing with a pen; the next humans in the queue stand behind it holding red tickets." };
  },

  "fifty-nine-elevens"(H, fid) {
    const { K, C } = H, ink = C.line;
    // After "oil.": the camera pulled back to take in both: the Weapons Maker in the foreground, where the missile
    // yanked free of its leash, oil-black and grinning in the rain of oil, his hard hat held out upside down to catch
    // more, the empty leash in his other hand; behind him, out on the field past the queue, the mushroom cloud over
    // the little oil derrick (x 1240, y -230) and the black gusher shooting up out of it.
    const DX = 1240, DY = -230, DK = 1.0;
    const lattice = [-300, -225, -150, -75].map((y) => {
      const w0 = 16 + 54 * (1 + y / 360), w1 = 16 + 54 * (1 + (y - 75) / 360);
      return `<path d="M${f(-w0)},${y} L${f(w1)},${y - 75} M${f(w0)},${y} L${f(-w1)},${y - 75} M${f(-w0)},${y} H${f(w0)}" stroke="#4A3B2C" stroke-width="4"/>`;
    }).join("");
    const derrick = at(DX, DY, DK, `<path d="M-70,0 L-16,-360 H16 L70,0" fill="none" stroke="${ink}" stroke-width="11" stroke-linejoin="miter"/>` +
      `<path d="M-70,0 L-16,-360 H16 L70,0" fill="none" stroke="#4A3B2C" stroke-width="5"/>` + lattice +
      `<path d="M-22,-360 H22 V-376 H-22 Z" fill="${C.slate}" stroke="${ink}" stroke-width="3"/><rect x="-92" y="-12" width="184" height="16" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>`);
    const nuke = at(DX, DY, 0.78, K.nuke());
    // the gusher: a black column from the derrick's crown up out of the frame, and the oil raining back down
    const top = DY - 376 * DK;
    const column = `<path d="M${DX - 18},${top} C${DX - 30},${top - 160} ${DX - 14},${top - 320} ${DX - 26},${top - 700} H${DX + 26} C${DX + 14},${top - 320} ${DX + 30},${top - 160} ${DX + 18},${top} Z" fill="${OIL}" stroke="${ink}" stroke-width="5"/>`;
    const drops = [];
    for (let i = 0; i < 34; i++) {
      const x = 300 + ((i * 137) % 1300), y = -900 + ((i * 263) % 860);
      if (Math.abs(x - DX) < 60 && y < top) continue;
      drops.push(`<path d="M${x},${y} q-9,17 0,24 q9,-7 0,-24 Z" fill="${OIL}" stroke="${ink}" stroke-width="1.6"/>`);
    }
    // the Weapons Maker, oil-black (charred), facing us: the hat up in his right hand, the leash in his left
    const WM = K.castOpts("weaponsMaker", { charred: true, mood: "grin", hat: null, arms: [[-22, -34], [112, 160]] });
    const RW = K.rig(WM);
    const hat = at(RW.hand[1][0] + 4, RW.hand[1][1] - 12, 1.15, `<g transform="rotate(180)"><path d="M-23,5 L-18,-13 L0,-20 L18,-13 L23,5 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="2.6" stroke-linejoin="miter"/><path d="M-30,8 L-26,3 H26 L30,8 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="2.2"/></g>` +
      `<path d="M-16,-10 q8,-7 16,0 q8,-7 16,0 Z" fill="${OIL}"/>`);
    const grin = `<path d="M${f(RW.mouth[0] - 8)},${f(RW.mouth[1] - 2)} Q${f(RW.mouth[0])},${f(RW.mouth[1] + 7)} ${f(RW.mouth[0] + 9)},${f(RW.mouth[1] - 3)} Z" fill="#FBF6E6" stroke="${ink}" stroke-width="1.2"/>` +
      `<path d="M${f(RW.mouth[0] - 3)},${f(RW.mouth[1] - 1)} v4 M${f(RW.mouth[0] + 2)},${f(RW.mouth[1] - 1)} v4" stroke="${ink}" stroke-width="0.9"/>`;
    const leash = `<path d="M${f(RW.hand[0][0])},${f(RW.hand[0][1])} q-6,34 -30,40 q-22,6 -30,26" fill="none" stroke="${C.war}" stroke-width="3.4"/><circle cx="${f(RW.hand[0][0] - 60)}" cy="${f(RW.hand[0][1] + 70)}" r="5" fill="none" stroke="${ink}" stroke-width="2.4"/>`;
    const puddle = `<ellipse cx="0" cy="98" rx="76" ry="10" fill="${OIL}"/>`;
    const wm = stand(K, WM, 620, 20, 2.0, puddle + leash + grin + hat);
    const plate = field() + queue(H, 2, 20) + nuke + derrick + column + drops.join("") + wm;
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="${GROUND}"/>` + view(900, -330, 0.95, plate);
    return { svg, alt: "In the foreground the Weapons Maker stands in a black puddle, oil-black from head to boots, grinning, holding his upturned hard hat up to catch the oil raining down, the empty leash dangling from his other hand; behind him, out on the field past the queue, a mushroom cloud stands over a little oil derrick and a black column of oil shoots up out of it." };
  },

  "falling-apart"(H, fid) {
    const { K, C } = H, ink = C.line;
    // On "sits": both rooms, the reader reading on the left, the doctor gesturing at the empty chair on the right.
    const button = `<circle cx="-470" cy="-5" r="6" fill="#FBF6E6" stroke="${ink}" stroke-width="2.4"/><circle cx="-472" cy="-6" r="1.2" fill="${ink}"/><circle cx="-468" cy="-4" r="1.2" fill="${ink}"/>`;
    // the office: the doctor seated behind his desk, facing left, gesturing kindly at the empty chair
    const DOC = { tone: 3, outfit: "labcoat", hair: 2, glasses: true, color: 2, seed: 14, look: "left", mood: "smile", build: { legPose: [[-88, -2], [-82, 4]] }, arms: [[-76, -104], [10, 4]] };
    const RD = K.rig(DOC);
    const mirror = `<circle cx="${f(RD.top[0] - 2)}" cy="${f(RD.top[1] + 6)}" r="9" fill="#C9CED6" stroke="${ink}" stroke-width="2.2"/><circle cx="${f(RD.top[0] - 2)}" cy="${f(RD.top[1] + 6)}" r="3.4" fill="#FBF6E6"/>` +
      `<path d="M${f(RD.top[0] - 14)},${f(RD.top[1] + 12)} L${f(RD.top[0] + 12)},${f(RD.top[1] + 8)}" stroke="${ink}" stroke-width="2.4"/>`;
    const docChair = at(590, 0, 1, `<path d="M-50,-60 H54 V-52 H-50 Z" fill="#7A5634" stroke="${ink}" stroke-width="4"/><path d="M46,-60 L56,-210 L66,-210 L58,-60 Z" fill="#7A5634" stroke="${ink}" stroke-width="4"/><path d="M-44,-52 V0 M48,-52 V0" stroke="${ink}" stroke-width="7"/>`);
    const doctor = at(570, -58 - 64.6 * S, S, K.person(DOC) + mirror);
    const desk = at(430, 0, 1, `<rect x="-130" y="-128" width="260" height="18" fill="#9A6A3E" stroke="${ink}" stroke-width="5"/><rect x="-120" y="-110" width="240" height="110" fill="#7A5634" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M-108,-78 H-30 M-108,-44 H-30" stroke="#5C4026" stroke-width="3"/><circle cx="-70" cy="-62" r="4" fill="${C.yellow}"/>` +
      `<path d="M-110,-134 L-62,-138 L-60,-128 L-108,-126 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="3"/><path d="M-106,-131 L-62,-133" stroke="${ink}" stroke-width="1.2"/>`);
    const emptyChair = at(200, 0, 1, `<path d="M-54,-62 H50 V-52 H-54 Z" fill="#9A6A3E" stroke="${ink}" stroke-width="4"/><path d="M-54,-62 L-64,-230 L-52,-230 L-44,-62 Z" fill="#9A6A3E" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M-60,-200 H-50 M-61,-170 H-49" stroke="${ink}" stroke-width="3"/><path d="M-48,-52 V0 M44,-52 V0" stroke="${ink}" stroke-width="7"/>`);
    const cal = at(660, -330, 1.7, K.props.calendar({ month: "MAR", day: 14, color: C.med }));
    const extra = at(-640, 0, 1, lamp(H)) + readerInChair(H) + button + cal + emptyChair + docChair + doctor + desk;
    const svg = view(20, -262, 1.28, livingRoom(H, extra));
    return { svg, alt: "A living room and a doctor's office side by side, cut away like a stage set: on the left the reader sits in an orange armchair under a floor lamp reading the orange manual, a red ticket for a bookmark, a lost button on the rug; through the wall on the right a doctor in a lab coat and head mirror sits at his desk and gestures kindly at the empty chair across from him, a calendar on the office wall." };
  },

  "dissolving-on-schedule"(H, fid) {
    const { K } = H;
    // On "schedule": eased back wider, the NOW SERVING sign come down on its chains behind the armchair, 150,080.
    const sign = at(CHAIR_X, -470, 0.78, nowServing(H, 150080));
    const extra = sign + at(-640, 0, 1, lamp(H)) + readerInChair(H);
    const svg = view(-330, -300, 1.15, livingRoom(H, extra));
    return { svg, alt: "The living room wider: the reader reads on in his orange armchair under the floor lamp, and on the wall behind his chair, over his head, hangs the NOW SERVING sign from the deli on its chains, reading 150,080, EVERY 24 HOURS." };
  },

  "meat-robot"(H, fid) {
    const { K, C } = H, St = K.STUDIO, ink = C.line;
    // On "solvable": the reader standing beside the lectern (x 1390, feet y 1066, scale 3.3, where host-closes puts
    // its guest), his kneecap out on a coil and black smoke coughing out of his chest; the wrench just lowered on a
    // string from above the frame, swinging over her raised palm.
    const GUEST = copy(READER, { look: "left", mood: "worried", arms: [[28, 64], [-14, -6]] });
    const RG = K.rig(GUEST), k = 3.3, gx = 1390, gy = 1066 - 100 * k - 4;
    const book = at(RG.hand[0][0] + 2, RG.hand[0][1] - 10, 0.28, K.props.manual(), -78) + at(RG.hand[0][0] - 4, RG.hand[0][1] - 33, 0.55, ticket(H), 8);
    const smoke = [[17, -11, 5], [25, -21, 7], [21, -36, 9]].map(([dx, dy, r]) => `<circle cx="${dx}" cy="${dy}" r="${r}" fill="#2A2630" stroke="${ink}" stroke-width="1.8"/>`).join("");
    const guest = at(gx, gy, k, K.person(GUEST) + book + kneecap(H, RG) + smoke);
    const palm = [St.wish.x + 0.87 * St.wish.w, St.wish.y + 0.97 * St.wish.w - 24];
    // the wrench hangs by its handle end on a string from above the frame, a little swing to it, over her palm
    const wx = palm[0] + 18, wy = palm[1] - 70, sw = 8;
    const string = `<path d="M${wx - 60},-20 L${wx - 2},${wy - 48}" stroke="${ink}" stroke-width="3"/>` +
      `<path d="M${wx - 12},${wy - 52} q10,-8 18,2 q-4,8 -12,6" fill="none" stroke="${ink}" stroke-width="3"/>`;
    const wr = at(wx, wy, 1.4, wrench(H), 90 - sw);
    const swing = `<path d="M${wx - 70},${wy + 30} q-14,30 4,60 M${wx + 70},${wy + 30} q14,30 -4,60" fill="none" stroke="${C.cream}" stroke-width="5" stroke-linecap="round" opacity="0.85"/>`;
    const svg = push(St, 1.05, H.host("excited-ee", "presenting", guest + string + swing + wr));
    return { svg, alt: "Wishonia at her lectern, excited, presents the reader standing beside it like a new appliance: his kneecap has sprung out on a coil and black smoke coughs out of his chest, and a teal wrench, just lowered on a string from above the frame, swings over her raised palm." };
  },

  "thought-incorrect"(H, fid) {
    const { K, C } = H, St = K.STUDIO, ink = C.line;
    // On "incorrect.": she points (point-right), smirking at the camera; the bubble over the reader bursts on her
    // fingertip, PRIORITY 1 scatters, the wrench falls, his kneecap springs out again, the flat beetle at his feet.
    const GUEST = copy(READER, { look: "left", mood: "worried", arms: [[28, 64], [-14, -6]] });
    const RG = K.rig(GUEST), k = 3.3, gx = 1390, gy = 1066 - 100 * k - 4;
    const book = at(RG.hand[0][0] + 2, RG.hand[0][1] - 10, 0.28, K.props.manual(), -78) + at(RG.hand[0][0] - 4, RG.hand[0][1] - 33, 0.55, ticket(H), 8);
    const flat = at(-46, 99, 1, `<g transform="scale(1,0.3)">${beetle(H)}</g><path d="M-30,1 l-8,-3 M30,1 l8,-3" stroke="${ink}" stroke-width="1.4"/>`);
    const guest = at(gx, gy, k, K.person(GUEST) + book + kneecap(H, RG) + flat);
    // her fingertip in body-point-right, and the burst there
    const tip = [St.wish.x + 1.0 * St.wish.w + 4, St.wish.y + 0.95 * St.wish.w - (St.wish.w * 12) / 140 + (0.2 * St.wish.w * 768) / 1343];
    const bx = tip[0] + 70, by = tip[1] - 20;
    const burst = [0, 40, 80, 120, 160, 200, 240, 280, 320].map((a) => {
      const r = (a * Math.PI) / 180;
      return `<path d="M${f(bx + Math.cos(r) * 60)},${f(by + Math.sin(r) * 60)} L${f(bx + Math.cos(r) * 110)},${f(by + Math.sin(r) * 110)}" stroke="${C.cream}" stroke-width="7" stroke-linecap="round"/>`;
    }).join("");
    const shreds = [[-40, -50, 20], [50, -60, -30], [80, 20, 40], [-70, 30, -20]].map(([dx, dy, r]) => at(bx + dx, by + dy, 1, `<path d="M-14,-6 Q0,-14 14,-6 Q4,0 -14,-6 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="3"/>`, r)).join("");
    const letters = [["P", 1180, 380, -20], ["R", 1250, 330, 14], ["I", 1320, 300, -8], ["O", 1560, 320, 22], ["R", 1640, 380, -16], ["I", 1700, 450, 30], ["T", 1600, 560, -34], ["Y", 1680, 640, 18], ["1", 1540, 700, -40]]
      .map(([ch, x, y, rot]) => `<text x="${x}" y="${y}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="62" fill="${C.navy}" stroke="${C.cream}" stroke-width="6" style="paint-order:stroke" transform="rotate(${rot} ${x} ${y})">${ch}</text>`).join("");
    const wr = at(bx + 140, by + 250, 1.3, wrench(H), 120);
    const svg = push(St, 1.07, H.host("smirk-closed", "point-right", guest + burst + shreds + letters + wr));
    return { svg, alt: "Wishonia points at the reader's thought bubble and smirks at the camera: it bursts on her fingertip, the letters of PRIORITY 1 tumble loose round his head and a teal wrench falls; his kneecap has sprung back out on its coil, a flattened beetle at his feet." };
  },
};
