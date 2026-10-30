// Sketches for storyboards/part-19-step-3-bribe-the-bribers.md (v3, the 1950s atomic-age film look of Part 2): each
// scene's key frame on a 1920 x 1080 frame (16:9), drawn with the production art. Host shots use the studio set
// (KIT.STUDIO, 16:9: the lectern's reading top at y 790, x 540 to 980; the free wall right of it, x 1100 to 1880);
// a plate frame is one framing as the camera sees it, the ground and the cast drawn large. Captions keep-out: y 900 down.
// Built into the review sheet by tools/storyboard-sheet.mjs.

const f = (n) => n.toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});
const at = (x, y, k, inner, rot = 0) => `<g transform="translate(${f(x)},${f(y)})${rot ? ` rotate(${rot})` : ""} scale(${k})">${inner}</g>`;
// A person standing with its feet on y `feet` at scale k (KIT.person draws the feet at y 100).
const stand = (x, feet, k, inner) => at(x, feet - 100 * k, k, inner);
// A plate framing as KIT.camera places it: plate point (x, y) in the middle of the frame, at scale s.
const view = (x, y, s, inner) => `<g transform="translate(${f(960 - x * s)},${f(540 - y * s)}) scale(${s})">${inner}</g>`;
// A host shot's slow push in on her face (KIT.studio), k of the way along.
const push = (S, k, inner) => `<g transform="translate(${S.face[0]},${S.face[1]}) scale(${k}) translate(${-S.face[0]},${-S.face[1]})">${inner}</g>`;
// A seeded generator, so the sketches draw the same every time.
function rng(seed) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}

const SKY = "#EFE3C4", GROUND = "#C8B07B", GROUND_EDGE = "#B09363", LEATHER = "#6B4A2F", VELVET = "#9E2A24";
const PAPER = "#F1EDD5", RULE = "#B9C99D";

// ── The cast as this part draws it ──────────────────────────────────────
// The Lobbyist without his kit briefcase (drawn on its own below); YOU, the bowler man of Parts 10, 12 and 17.
const LOB = (K, extra) => K.castOpts("lobbyist", copy({ holdL: null, holdR: null }, extra));
const YOU = { tone: 2, outfit: "suit", hat: "bowler" };

// ── The briefcase (the part's spine) ────────────────────────────────────
// Closed, standing on (0, 0), 120 wide and 84 tall plus its funnel: brown leather, two brass latches, a navy handle,
// and a small navy-and-cream striped funnel on its top right with a bill corner peeking out. o.bulge swells it like a
// balloon; o.sticker puts the round cross-seal travel sticker on its front.
function briefcase(K, o = {}) {
  const { C } = K, ink = C.line, b = o.bulge ? 1 : 0;
  const w = 60 + b * 22, h = 84 + b * 40, rx = 6 + b * 34;
  const body = `<rect x="${-w}" y="${-h}" width="${2 * w}" height="${h}" rx="${rx}" fill="${LEATHER}" stroke="${ink}" stroke-width="4.5"/>` +
    `<path d="M${-w + 8},${-h + 22} H${w - 8}" stroke="#4E3420" stroke-width="3"/>` +
    [-1, 1].map((s) => `<rect x="${s * 34 - 8}" y="${-h + 14}" width="16" height="16" rx="2" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/>`).join("") +
    `<path d="M-20,${-h} V${-h - 16} H20 V${-h}" fill="none" stroke="${ink}" stroke-width="7" stroke-linejoin="round"/>`;
  const fx = w - 28, fy = -h;
  // the funnel: a cone, its mouth 64 wide at y -52, five bands narrowing into a short spout, the middle ones navy
  const band = (i) => { const t0 = -32 + 12.8 * i, t1 = t0 + 12.8, b0 = -7 + 2.8 * i, b1 = b0 + 2.8; return `<path d="M${f(t0)},-52 L${f(t1)},-52 L${f(b1)},-16 L${f(b0)},-16 Z" fill="${i % 2 ? C.navy : C.cream}"/>`; };
  const funnel = `<g transform="translate(${fx},${fy})"><rect x="-7" y="-17" width="14" height="17" fill="${C.navy}" stroke="${ink}" stroke-width="3"/>` +
    [0, 1, 2, 3, 4].map(band).join("") + `<path d="M-32,-52 L32,-52 L7,-16 L-7,-16 Z" fill="none" stroke="${ink}" stroke-width="3.5" stroke-linejoin="round"/>` +
    `<g transform="translate(10,-60) rotate(-16) scale(0.34)">${K.money("war").replace(/<path class="legs"[^>]*\/>/, "")}</g>` +
    `<ellipse cx="0" cy="-52" rx="32" ry="7" fill="#1B2236" stroke="${ink}" stroke-width="3.5"/></g>`;
  const sticker = o.sticker ? `<g transform="translate(-22,${-h * 0.42})"><circle r="25" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>` +
    `<circle r="25" fill="none" stroke="${C.cream}" stroke-width="5" stroke-dasharray="4 4"/>${K.moneySeal("med", 0, 0, 17)}</g>` : "";
  return body + funnel + sticker;
}
// Open, held flat with the lid swung up behind, its hinge at y 0: the lid's red velvet lining above (one empty slot
// under a brass BELIEFS plate, on its left half), the case below stuffed with war bills. 240 wide; the lid is 150
// tall, the case 120. The rolodex springs up out of the case's right half (rolodex(), at x 62).
function openCase(K) {
  const { C } = K, ink = C.line;
  const lid = `<rect x="-120" y="-150" width="240" height="150" rx="8" fill="${LEATHER}" stroke="${ink}" stroke-width="5"/>` +
    `<rect x="-106" y="-138" width="212" height="128" rx="5" fill="${VELVET}" stroke="${ink}" stroke-width="3"/>` +
    `<path d="M-100,-24 Q-60,-14 -20,-28 M16,-126 Q56,-116 96,-130" fill="none" stroke="#7E1F1A" stroke-width="3"/>` +
    `<rect x="-102" y="-128" width="104" height="30" rx="3" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/>` +
    `<text x="-50" y="-105.5" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="22" letter-spacing="1.5" fill="${ink}">BELIEFS</text>` +
    `<rect x="-88" y="-88" width="76" height="40" rx="17" fill="#3A0E0C" stroke="${ink}" stroke-width="3.5"/>` +
    `<path d="M-82,-80 Q-50,-92 -18,-80" fill="none" stroke="#5E1713" stroke-width="3"/>`;
  let bills = "";
  const r = rng(19);
  for (let i = 0; i < 9; i++) bills += at(-90 + i * 22 + r() * 6, 20 + (i % 2) * 8, 0.62, K.money("war"), -14 + r() * 28);
  const box = `<defs><clipPath id="p19case"><rect x="-114" y="6" width="228" height="104"/></clipPath></defs>` +
    `<rect x="-120" y="0" width="240" height="120" rx="8" fill="${LEATHER}" stroke="${ink}" stroke-width="5"/>` +
    `<rect x="-112" y="6" width="224" height="60" fill="#3B2818"/><g clip-path="url(#p19case)">${bills}</g>` +
    `<path d="M-120,64 H120" stroke="${ink}" stroke-width="4"/>` +
    [-1, 1].map((s) => `<rect x="${s * 70 - 10}" y="58" width="20" height="18" rx="2" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/>`).join("");
  return lid + box;
}
// The rolodex on its coil spring, the spring's foot at (0, 0) and the drum 150 above it, its cards fanned and the
// front card stopped: a cream card with a war-red tab and an oval portrait of the Weapons Maker from the chest up.
function rolodex(K, fid) {
  const { C } = K, ink = C.line, top = -150;
  const spring = `<path d="M0,0 l-14,-10 l28,-14 l-28,-14 l28,-14 l-28,-14 l28,-14 l-28,-14 l28,-14 l-28,-14 l28,-14 l-14,-8" fill="none" stroke="${ink}" stroke-width="8" stroke-linejoin="round"/><path d="M0,0 l-14,-10 l28,-14 l-28,-14 l28,-14 l-28,-14 l28,-14 l-28,-14 l28,-14 l-28,-14 l28,-14 l-14,-8" fill="none" stroke="#B9BCC4" stroke-width="4" stroke-linejoin="round"/>`;
  const wm = K.cast("weaponsMaker");
  const card = `<defs><clipPath id="${fid}-oval"><ellipse cx="0" cy="-62" rx="38" ry="44"/></clipPath></defs>` +
    `<path d="M-60,-118 H-26 V-130 H8 V-118 H60 V0 H22 v-8 h-12 v8 H-10 v-8 h-12 v8 H-60 Z" fill="${C.cream}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
    `<rect x="-26" y="-130" width="34" height="12" fill="${C.war}" stroke="${ink}" stroke-width="3"/>` +
    `<ellipse cx="0" cy="-62" rx="40" ry="46" fill="#E3C88F" stroke="${ink}" stroke-width="3.5"/><g clip-path="url(#${fid}-oval)"><g transform="translate(0,-32) scale(2.1)">${wm}</g></g>` +
    `<ellipse cx="0" cy="-62" rx="40" ry="46" fill="none" stroke="${C.yellow}" stroke-width="4"/>`;
  const fanned = [-30, -15, 15, 30].map((a) => `<g transform="rotate(${a} 0 -10)"><path d="M-56,-110 H56 V-4 H-56 Z" fill="#E6DCC0" stroke="${ink}" stroke-width="3.5"/></g>`).join("");
  const drum = `<rect x="-74" y="-22" width="148" height="24" rx="11" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><circle cx="-80" cy="-10" r="9" fill="${C.slate}" stroke="${ink}" stroke-width="3"/><circle cx="80" cy="-10" r="9" fill="${C.slate}" stroke="${ink}" stroke-width="3"/>`;
  return spring + `<g transform="translate(0,${top})">${fanned}${card}${drum}</g>`;
}
// The moth from Part 1's empty wallet (as money-loop.html draws it), wings open, around (0, 0).
function moth(K) {
  const ink = K.C.line;
  return `<path d="M0,-2 L-26,-16 L-22,6 Z M0,-2 L26,-16 L22,6 Z" fill="#B9AE98" stroke="${ink}" stroke-width="2.4" stroke-linejoin="round"/><path d="M0,2 L-14,14 L-4,6 Z M0,2 L14,14 L4,6 Z" fill="#9C907A" stroke="${ink}" stroke-width="2" stroke-linejoin="round"/>` +
    `<ellipse cx="0" cy="2" rx="4" ry="11" fill="#6B5B45" stroke="${ink}" stroke-width="2"/><path d="M-1,-8 q-6,-10 -12,-10 M1,-8 q6,-10 12,-10" fill="none" stroke="${ink}" stroke-width="1.6"/>`;
}
// A fat stack of bills with a paper band, standing on (0, 0): kind "war" or "med", about 110 wide and 76 tall.
function stack(K, kind, band = "$500,000") {
  const { C } = K, ink = C.line;
  let out = "";
  for (let i = 0; i < 6; i++) out += `<rect x="-52" y="${-14 - i * 11}" width="104" height="14" rx="2" fill="${i % 2 ? C.money : C.moneyEdge}" stroke="${ink}" stroke-width="2.6"/>`;
  out += `<g transform="translate(0,-73) scale(1.08,0.5)">${K.money(kind).replace(/<path class="legs"[^>]*\/>/, "")}</g>`;
  out += `<rect x="-16" y="-80" width="32" height="80" fill="${C.cream}" stroke="${ink}" stroke-width="2.6"/>` +
    `<text x="0" y="-36" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="13" fill="${ink}" transform="rotate(-90 0 -40)">${band.replace(/&/g, "&amp;")}</text>`;
  return out;
}

// ── The ledger plate (current-job-column, your-offer-column) ────────────
// Two columns of three cells, each 1600 x 900, the left column x 0..1600, the right x 1800..3400, the rows' ground
// rules at y 900, 1900 and 2900; cream paper with pale green rules every 75 units; a slate wash over the left column.
const CELL = { w: 1600, h: 900, gap: 200 }, COLX = [0, 1800], ROWY = [0, 1000, 2000];
function ledgerPaper(K) {
  const { C } = K, ink = C.line;
  let rules = "";
  for (let y = -150; y <= 3060; y += 75) rules += `M-160,${y} H3560 `;
  let out = `<rect x="-4000" y="-4000" width="11400" height="11000" fill="${GROUND}"/>` +
    `<rect x="-160" y="-160" width="3720" height="3220" fill="${PAPER}"/><path d="${rules}" stroke="${RULE}" stroke-width="3"/>` +
    `<path d="M-100,-160 V3060 M-86,-160 V3060" stroke="#D69A8A" stroke-width="3"/>`;
  // the current job's smoky wash
  out += `<rect x="0" y="0" width="${CELL.w}" height="2900" fill="#7D8496" opacity="0.28"/>`;
  // the heavy rules: the cells' grounds and tops, the outer frame, the column double rule in the gutter
  ROWY.forEach((y) => { out += `<path d="M-40,${y + CELL.h} H3440" stroke="${ink}" stroke-width="12"/><path d="M-40,${y} H3440" stroke="${ink}" stroke-width="5"/>`; });
  out += `<path d="M0,-40 V2940 M${CELL.w},-40 V2940 M1800,-40 V2940 M3400,-40 V2940" stroke="${ink}" stroke-width="5"/>` +
    `<path d="M1690,-40 V2940 M1710,-40 V2940" stroke="${ink}" stroke-width="6"/>`;
  return out;
}
// The orphans (current-job-column) and the same children with their parents (your-offer-column): rows of small
// children standing on ground y g between x0 and x1 (the back rows higher and smaller), leaving a gap round x gapX
// for the grave or the plinth, all turned to it. withParents: each child holds a parent's hand.
const KID = { hs: 1.4, legs: 0.58, th: 0.72, tw: 0.8, neck: 0.3, nose: 0.9 };
function crowd(K, x0, x1, g, gapX, gapW, withParents) {
  let out = "";
  const r = rng(withParents ? 31 : 13), rows = [[g - 120, 0.9], [g - 60, 1.1], [g, 1.35]];
  rows.forEach(([gy, k], ri) => {
    const step = withParents ? 210 : 120, n = Math.floor((x1 - x0) / step);
    for (let i = 0; i < n; i++) {
      const x = x0 + step * (i + 0.5) + (ri % 2) * step * 0.4 + (r() - 0.5) * 24;
      if (Math.abs(x - gapX) < gapW / 2 + ri * 30 || x > x1) continue;
      const face = x < gapX ? "right" : "left", tone = Math.floor(r() * 4);
      const kid = { tone, outfit: r() < 0.5 ? "shirt" : "dress", hair: r() < 0.5 ? 1 : 0, colorHex: withParents ? ["#C9A24E", "#6F9A5C", "#5C6F8E", "#D9774A"][Math.floor(r() * 4)] : "#9A968C", seed: ri * 10 + i, mood: withParents ? "smile" : "sad", look: face, hat: null, glasses: false, build: KID };
      if (withParents) {
        const par = { tone, outfit: r() < 0.5 ? "suit" : "dress", hair: r() < 0.5 ? 1 : 0, hat: null, seed: 50 + ri * 10 + i, mood: "smile", look: face, arms: face === "right" ? [[-30, -10], [150, 175]] : [[-150, -175], [30, 10]] };
        out += stand(x + (face === "right" ? -70 : 70) * k, gy, k * 1.25, K.person(par));
      }
      out += stand(x, gy, k, K.person(copy(kid, withParents ? { arms: face === "right" ? [[-110, -150], [20, 10]] : [[-20, -10], [110, 150]] } : {})));
    }
  });
  return out;
}
// The fedora and the domino mask, hung on something at (0, 0) (person-ish units): the hat's brim on the corner, the
// mask dangling from it on its string.
function hatAndMask(K) {
  const { C } = K, ink = C.line;
  return `<g transform="rotate(14)"><path d="M-34,0 Q0,-8 34,0 L30,8 Q0,2 -30,8 Z" fill="#3B3F52" stroke="${ink}" stroke-width="3.4" stroke-linejoin="round"/>` +
    `<path d="M-20,0 L-16,-26 Q0,-33 16,-26 L20,0 Z" fill="#3B3F52" stroke="${ink}" stroke-width="3.4" stroke-linejoin="round"/><path d="M-19,-7 H19" stroke="${C.orange}" stroke-width="5"/></g>` +
    `<path d="M24,6 L30,34" stroke="${ink}" stroke-width="1.8"/><g transform="translate(30,44) rotate(-8)"><path d="M-19,-7 L20,-8 L21,4 L14,7 L10,2 L4,7 L-4,3 L-11,7 L-19,4 Z" fill="${ink}"/>` +
    `<path d="M-8,-2 q4,-3 8,0 q-4,3 -8,0 Z M7,-2 q4,-3 8,0 q-4,3 -8,0 Z" fill="${C.cream}"/></g>`;
}
// The gloved skeleton hand poking up out of a mound at (0, 0), waving a war bill (person-ish units, about 130 tall):
// two forearm bones, a knobby wrist, his navy glove with its cuff, the fingers pinching the bill's corner.
function boneHand(K) {
  const { C } = K, ink = C.line, bone = "#F1EAD6", G = "#1F2A44";
  const fore = (d) => `<path d="${d}" stroke="${ink}" stroke-width="11" stroke-linecap="round"/><path d="${d}" stroke="${bone}" stroke-width="6" stroke-linecap="round"/>`;
  const bones = fore("M-5,6 L-4,-50") + fore("M6,6 L6,-50") + `<circle cx="-5" cy="-52" r="6" fill="${bone}" stroke="${ink}" stroke-width="3"/><circle cx="7" cy="-52" r="6" fill="${bone}" stroke="${ink}" stroke-width="3"/>`;
  const cuff = `<path d="M-16,-54 L17,-56 L19,-70 L-17,-68 Z" fill="${G}" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/><path d="M-16,-60 L18,-62" stroke="${C.cream}" stroke-width="2.4"/>`;
  const palm = `<path d="M-15,-68 L17,-70 L20,-92 L-12,-94 Z" fill="${G}" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/>`;
  const finger = (x, y, a, l) => `<g transform="translate(${x},${y}) rotate(${a})"><path d="M-4,0 L-3.5,${-l} L3.5,${-l - 1} L4,0 Z" fill="${G}" stroke="${ink}" stroke-width="2.8" stroke-linejoin="miter"/></g>`;
  const fingers = finger(-9, -92, -12, 20) + finger(-1, -93, -4, 24) + finger(7, -93, 5, 22) + finger(14, -91, 14, 17) + finger(18, -78, 62, 16);
  const note = at(18, -128, 0.7, K.money("war").replace(/<path class="legs"[^>]*\/>/, ""), -28);
  return bones + note + cuff + palm + fingers;
}
// A bottom-row cell's picture: drawn 1.2 times as big about (cx, 2900), its ground rule, and clipped to the cell
// (x0 to x0 + 1600, the row's top rule to its ground), so the cast stands large in its cell.
function cell(id, x0, cx, inner) {
  return `<defs><clipPath id="${id}"><rect x="${x0}" y="2000" width="${CELL.w}" height="906"/></clipPath></defs>` +
    `<g clip-path="url(#${id})"><g transform="translate(${cx},2900) scale(1.2) translate(${-cx},-2900)">${inner}</g></g>`;
}
// The bottom left cell: the headstone with his fedora and mask hung on it, the skeleton hand, the orphans. The grave
// stands right of the cell's middle and the statue left of its cell's middle, so the two legacies face each other
// across the column rule.
const GRAVE_X = 1150, STATUE_X = 2300;
function graveCell(K, fid) {
  const { C } = K, ink = C.line, x0 = GRAVE_X, g = 2900;
  const mound = `<path d="M${x0 - 250},${g} Q${x0 - 160},${g - 74} ${x0},${g - 82} Q${x0 + 170},${g - 74} ${x0 + 260},${g} Z" fill="#7A5A3A" stroke="${ink}" stroke-width="5"/>`;
  const stone = at(x0 - 30, g - 46, 2.4, K.props.headstone({ text: "HERE LIES" }));
  const carved = at(x0 - 30, g - 46 - 2.4 * 46, 2.4, `<g transform="rotate(-90) scale(0.4)"><path d="M-34,-7 L14,-7 L30,0 L14,7 L-34,7 Z M-34,-7 L-44,-17 L-40,-7 Z M-34,7 L-44,17 L-40,7 Z" fill="none" stroke="#5E636C" stroke-width="5" stroke-linejoin="round"/></g>`);
  const hat = at(x0 - 30 + 2.4 * 52, g - 46 - 2.4 * 104, 2.4, hatAndMask(K));
  const hand = at(x0 + 200, g - 40, 1.9, boneHand(K), 8);
  return cell(fid + "-l3", 0, x0, crowd(K, 40, 1640, g, x0, 560, false) + mound + stone + carved + hat + hand);
}
// A bronze statue: a person drawn in verdigris and bronze tones (every fill but the ink).
function bronze(markup, ink) {
  const inkU = ink.toUpperCase();
  return markup.replace(/(fill|stroke)="(#[0-9A-Fa-f]{6})"/g, (m, a, col) => {
    if (col.toUpperCase() === inkU) return m;
    const n = parseInt(col.slice(1), 16), l = (0.3 * (n >> 16) + 0.59 * ((n >> 8) & 255) + 0.11 * (n & 255)) / 255;
    const v = Math.round(70 + l * 120);
    return `${a}="rgb(${Math.round(v * 0.62)},${Math.round(v * 0.86)},${Math.round(v * 0.74)})"`;
  });
}
// The bottom right cell: the plinth, the bronze statue (one finger raised like a hero), the brass plaque, the
// children with their parents, and the live Lobbyist at the left foot of his statue looking back at his headstone.
function statueCell(K, fid) {
  const { C } = K, ink = C.line, x0 = STATUE_X, g = 2900, pw = 190, ph = 260;
  const plinth = `<rect x="${x0 - pw}" y="${g - ph}" width="${2 * pw}" height="${ph}" fill="#CFC6AE" stroke="${ink}" stroke-width="6"/>` +
    `<rect x="${x0 - pw - 26}" y="${g - ph - 36}" width="${2 * pw + 52}" height="36" fill="#BDB39A" stroke="${ink}" stroke-width="6"/><rect x="${x0 - pw - 26}" y="${g - 30}" width="${2 * pw + 52}" height="30" fill="#BDB39A" stroke="${ink}" stroke-width="6"/>`;
  const plaque = `<rect x="${x0 - 160}" y="${g - 236}" width="320" height="200" rx="8" fill="${C.yellow}" stroke="${ink}" stroke-width="5"/><rect x="${x0 - 148}" y="${g - 224}" width="296" height="176" rx="4" fill="none" stroke="#B07A22" stroke-width="3"/>` +
    ["ACCIDENTALLY", "SAVED HUMANITY", "WHILE GETTING", "RICH"].map((t, i) => `<text x="${x0}" y="${g - 180 + i * 40}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="34" letter-spacing="1.5" fill="${ink}">${t}</text>`).join("");
  const ho = LOB(K, { mood: "smug", arms: [[-12, -4], [160, 182]] }), HR = K.rig(ho), hk = 2.0, top = g - ph - 36;
  const statue = bronze(stand(x0, top, hk, K.person(ho)) + at(x0 + hk * HR.hand[0][0], top - hk * (100 - HR.hand[0][1]) + 64, 0.8, briefcase(K)), ink);
  const lo = LOB(K, { look: "left", mood: "smile", arms: [[-6, -2], [10, 15]] }), LR = K.rig(lo), lx = 1990, lk = 2.1;
  const live = stand(lx, g, lk, K.person(lo)) + at(lx + lk * LR.hand[1][0] + 6, g, 0.95, briefcase(K));
  return cell(fid + "-r3", 1800, x0, crowd(K, 2520, 3440, g, x0, 300, true) + plinth + plaque + statue + live);
}

export default {
  "step-3-bribe-the-bribers-title"(H, fid) {
    const { K, C } = H;
    // KIT.titleScene's atomic card (16:9): the emblem at (960, 300), rx 200, ry 62, papers at 0.62; the heading laid out
    // as its fit() does: "STEP 3:" at 76 px (caps 598 to 651), "BRIBE THE BRIBERS" at 152 px (caps 696 to 802), the
    // last S ending at x 1760
    const cx = 960, cy = 300, rx = 200, ry = 62, TILT = [0, 60, -60], t = 2.6;
    const orbits = TILT.map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = TILT.map((a, i) => {
      const th = i * 2.1 + t * 2.4, ar = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return at(cx + ex * Math.cos(ar) - ey * Math.sin(ar), cy + ex * Math.sin(ar) + ey * Math.cos(ar) - 6, 0.62, K.money("war", i % 2));
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    const word = (x, y, s, text) => {
      const t0 = (dx, dy, extra) => `<text x="${f(x + dx)}" y="${f(y + dy)}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${f(s)}" ${extra}>${H.esc(text)}</text>`;
      return t0(0.04 * s, 0.053 * s, `fill="${C.ink}"`) + t0(0, 0, `fill="${C.cream}" stroke="${C.cream}" stroke-width="${f(0.044 * s)}" stroke-linejoin="round" style="paint-order:stroke"`);
    };
    const heading = word(960, 651, 76, "STEP 3:") + word(960, 802, 152, "BRIBE THE BRIBERS");
    // the price tag hung on the top right corner of the last S, swinging out to the right
    const knot = [1742, 700];
    const tag = at(knot[0], knot[1], 1.9, K.props.priceTag({ text: "$500,000", angle: 58 }));
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus + heading + tag;
    return { svg, alt: "The period title card: on plain navy under the film's atom, its three little war-seal papers running round the orbits, the heading STEP 3: BRIBE THE BRIBERS in cream; a white price tag reading $500,000 hangs on its string from the last S, swinging." };
  },

  "conversion-therapy"(H, fid) {
    const { K, C } = H, S = K.STUDIO;
    // on "Therapy": the Lobbyist (feet 1075, scale 3.1, facing her) has slid one war bill across the lectern top with a
    // gloved finger; his other hand holds the funnel-topped briefcase; Wishonia side-eyes it, arms crossed
    const k = 3.1, o = LOB(K, { look: "left", mood: "eager", arms: [[-52, -96], [-8, -2]] }), R = K.rig(o);
    const target = [968, 786], x = target[0] - k * R.hand[0][0], feet = target[1] - k * (R.hand[0][1] - 100);
    const man = stand(x, feet, k, K.person(o));
    const caseAt = at(x + k * R.hand[1][0] + 10, feet - k * (100 - R.hand[1][1]) + 96, 1.4, briefcase(K));
    const note = at(target[0] - 62, 778, 0.9, K.money("war"), -6);
    const svg = push(S, 1.03, H.host("sideeye-closed", "arms-crossed", note + man + caseAt));
    return { svg, alt: "Wishonia at her lectern side-eyes a green war bill that the masked Lobbyist, standing at the right end of the lectern with his funnel-topped briefcase, has slid across the lectern top with one gloved finger." };
  },

  "democracy-jackpot"(H, fid) {
    const { K, C } = H, ink = C.line, CAP = 2.4;
    // the plate: the capitol at (0, 0) at scale 2.4 on the tan field, the horizon at y -150. After "thirteen": the
    // dome flipped open on its left hinge, three missiles on the reels, the geyser out of the drum, the pile at its foot.
    const field = `<rect x="-4000" y="-4000" width="8000" height="3850" fill="${SKY}"/><rect x="-4000" y="-150" width="8000" height="4000" fill="${GROUND}"/><path d="M-4000,-150 H4000" stroke="${GROUND_EDGE}" stroke-width="5"/>`;
    let cap = K.props.capitol({});
    cap = cap.replace('class="capitol-dome"', 'class="capitol-dome" transform="rotate(-62 -66 -258)"');
    // the reel windows in the drum, each showing a little missile; the slot lever on the right wing
    const missile = (x) => `<g transform="translate(${x},-219) rotate(-90) scale(0.3)"><path d="M-34,-7 L14,-7 L30,0 L14,7 L-34,7 Z M-34,-7 L-44,-17 L-40,-7 Z M-34,7 L-44,17 L-40,7 Z" fill="${C.war}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/><path d="M14,-7 L30,0 L14,7 Z" fill="${C.cream}" stroke="${ink}" stroke-width="3"/></g>`;
    const reels = [-40, 0, 40].map((x) => `<rect x="${x - 16}" y="-242" width="32" height="46" rx="3" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>` + missile(x)).join("");
    const lever = `<rect x="216" y="-116" width="16" height="30" fill="#C9CDD3" stroke="${ink}" stroke-width="3"/><path d="M228,-104 L262,-176" stroke="${ink}" stroke-width="9" stroke-linecap="round"/><path d="M228,-104 L262,-176" stroke="#C9CDD3" stroke-width="4" stroke-linecap="round"/><circle cx="264" cy="-182" r="13" fill="${C.war}" stroke="${ink}" stroke-width="3"/>`;
    const slot = `<rect x="-9" y="-62" width="18" height="5" fill="${ink}"/><rect x="-11" y="-64" width="22" height="9" fill="none" stroke="${C.yellow}" stroke-width="2"/>`;
    const building = at(0, 0, CAP, cap + reels + lever + slot);
    // the geyser: war bills shooting up out of the drum and fanning out, then raining down
    const r = rng(41);
    let geyser = "";
    for (let i = 0; i < 46; i++) {
      const u = i / 45, y = -640 - u * 820, spread = 60 + u * 520;
      geyser += at((r() - 0.5) * 2 * spread, y + (r() - 0.5) * 60, 0.95 + r() * 0.35, K.money("war", r() < 0.5 ? 0 : 1), (r() - 0.5) * 120);
    }
    const spout = `<path d="M-150,-620 Q-210,-900 -380,-1300 L380,-1300 Q210,-900 150,-620 Z" fill="${C.cream}" opacity="0.35"/>`;
    // the pile at the capitol's foot: a heap of bills spreading down the steps
    let pile = `<path d="M-1100,40 Q-900,-90 -560,-110 Q-200,-170 0,-150 Q300,-170 640,-110 Q960,-80 1120,40 Z" fill="${C.money}" stroke="${ink}" stroke-width="6"/>`;
    for (let i = 0; i < 40; i++) {
      const x = -1000 + r() * 2000, y = -40 - r() * 80 * (1 - Math.abs(x) / 1100);
      pile += at(x, y, 1.0, K.money("war").replace(/<path class="legs"[^>]*\/>/, ""), (r() - 0.5) * 70);
    }
    // the Lobbyist buried to the chest in front of the steps (everything of him below y -40 is under the money),
    // hugging his briefcase at his side, bulged like a balloon
    const lk = 2.6, lo = LOB(K, { look: "left", mood: "greedy", arms: [[55, 125], [45, 125]] }), LR = K.rig(lo);
    const lx = 330, lfeet = 150;
    const lob = `<defs><clipPath id="${fid}-dig"><rect x="-4000" y="-4000" width="8000" height="3960"/></clipPath></defs><g clip-path="url(#${fid}-dig)">${stand(lx, lfeet, lk, K.person(lo))}</g>`;
    const bulge = at(lx + lk * LR.hand[1][0] + 50, -34, 1.35, briefcase(K, { bulge: true }));
    const front = `<path d="M60,40 Q200,-62 360,-56 Q560,-70 740,40 Z" fill="${C.money}" stroke="${ink}" stroke-width="6"/>` +
      [150, 240, 330, 420, 510, 600].map((x, i) => at(x, -22 - (i % 2) * 14, 1.0, K.money("war").replace(/<path class="legs"[^>]*\/>/, ""), -24 + i * 10)).join("");
    const inner = field + building + spout + geyser + pile + lob + front + bulge;
    const sky = `<text x="1500" y="250" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="190" letter-spacing="4" fill="${C.navy}">1,813</text>`;
    const svg = view(150, -560, 0.66, inner) + sky;
    return { svg, alt: "The capitol on a tan field as a slot machine: three little missiles on the reels in its drum, its dome flipped open like a lid, a geyser of green war bills shooting out into the sky under a big 1,813; in front, the masked Lobbyist, buried to the chest in a heap of bills, hugs his briefcase, bulging like a balloon." };
  },

  "current-job-column"(H, fid) {
    const { K } = H;
    // on "orphans": the pull-back in the bottom left cell, its ground rule at screen y 885
    const svg = view(GRAVE_X - 330, 2600, 1.15, ledgerPaper(K) + graveCell(K, fid));
    return { svg, alt: "A cell of a giant ledger page, washed slate: a headstone reading HERE LIES on a fresh mound, the Lobbyist's fedora and domino mask hung on its corner, a gloved skeleton hand poking up out of the mound waving a green war bill, and rows of small orphans in gray smocks standing round the grave, all staring at it." };
  },

  "your-offer-column"(H, fid) {
    const { K } = H;
    // on "rich": the pull-back across the gutter to both bottom cells (the headstone and its orphans; the statue, the
    // plaque and the families), the live Lobbyist at the left foot of his statue looking back at the headstone
    const svg = view(1720, 2610, 0.9, ledgerPaper(K) + graveCell(K, fid) + statueCell(K, fid));
    return { svg, alt: "Two cells of the ledger page side by side across its double column rule: on the left, the slate-washed grave reading HERE LIES with the skeleton hand waving a bill among the orphans; on the right, a bronze statue of the Lobbyist on a plinth with a brass plaque reading ACCIDENTALLY SAVED HUMANITY WHILE GETTING RICH, the same children now holding their parents' hands, and the live Lobbyist at its foot looking back at his headstone." };
  },

  "lobbyists-have-clients"(H, fid) {
    const { K, C } = H, S = K.STUDIO, ink = C.line;
    // after "clients.": the Lobbyist (feet 1075, scale 3.1, facing her) holds his briefcase open, flat, out toward the
    // lectern, its lid up: the empty BELIEFS slot on the lid's left, the moth fluttering off it, and the rolodex sprung
    // up out of the case's right half on its coil spring, stopped on the Weapons Maker's card
    const k = 3.1, lx = 1660, o = LOB(K, { look: "left", mood: "smug", arms: [[-55, -5], [-55, -50]] }), R = K.rig(o);
    const man = stand(lx, 1075, k, K.person(o));
    const hx = 1360, hy = 850, ck = 1.25;
    const opened = at(hx, hy, ck, openCase(K));
    const rolo = at(hx + 62 * ck, hy + 30 * ck, 1.45, rolodex(K, fid));
    const gloves = R.hand.map(([x, y]) => `<path d="M${f(lx + k * x - 16)},${f(1075 + k * (y - 100) - 6)} l30,-4 l4,22 l-30,6 Z" fill="${ink}"/>`).join("");
    const mothAt = at(1205, 560, 1.8, moth(K), -16);
    const flutter = `<path d="M1238,618 q14,16 30,22 M1214,628 q6,22 22,34" fill="none" stroke="${ink}" stroke-width="3" stroke-linecap="round" opacity="0.6"/>`;
    const svg = push(S, 1.05, H.host("sideeye-closed", "idle", man + opened + rolo + gloves + flutter + mothAt));
    return { svg, alt: "Beside Wishonia's lectern the masked Lobbyist holds his briefcase open toward her: on its red velvet lid an empty slot under a brass BELIEFS plate, a moth fluttering off it; a rolodex has sprung up out of the case on a coil spring, stopped on a cream card with a war-red tab and an oval portrait of the grinning Weapons Maker. Wishonia side-eyes the camera." };
  },

  "two-clients"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "larger.": both worlds in the starry sky; the left one shrunk (r 190, worried), the Weapons Maker balancing
    // on one foot on its top; the right one 1.43 times as wide (r 272, smiling), YOU and the Lobbyist on top
    const r = rng(77);
    let stars = "";
    for (let i = 0; i < 70; i++) {
      const x = -1700 + r() * 3400, y = -1100 + r() * 2000, s = 5 + r() * 10;
      stars += `<path d="M${f(x)},${f(y - s)} L${f(x + s * 0.25)},${f(y - s * 0.25)} L${f(x + s)},${f(y)} L${f(x + s * 0.25)},${f(y + s * 0.25)} L${f(x)},${f(y + s)} L${f(x - s * 0.25)},${f(y + s * 0.25)} L${f(x - s)},${f(y)} L${f(x - s * 0.25)},${f(y - s * 0.25)} Z" fill="${C.yellow}"/>`;
    }
    const sky = `<rect x="-4000" y="-4000" width="8000" height="8000" fill="${C.navy}"/>` + stars;
    const L = { x: -620, cy: 320, r: 180 }, Rw = { x: 480, cy: 320, r: 257 };
    const globe = (w, face) => at(w.x, w.cy + w.r, 1, K.props.earthGlobe({ r: w.r, face }));
    const topL = L.cy - L.r + 6, topR = Rw.cy - Rw.r + 6, k = 2.1, on = (w, dx) => w.cy - Math.sqrt(w.r * w.r - dx * dx) + 10;
    // the Weapons Maker on one foot, cradling his missile, wobbling
    const wmo = K.castOpts("weaponsMaker", {});
    const wm = at(L.x, topL, 1, `<g transform="rotate(-8)">${stand(0, 0, k, K.person(copy(wmo, { build: copy(wmo.build, { legPose: [[-4, -2], [70, 110]] }) })))}</g>`);
    const wobble = `<path d="M${L.x - 110},${topL - 230} q-16,22 0,44 M${L.x - 132},${topL - 214} q-12,14 0,28 M${L.x + 118},${topL - 260} q16,22 0,44 M${L.x + 140},${topL - 244} q12,14 0,28" fill="none" stroke="${C.cream}" stroke-width="5" stroke-linecap="round"/>`;
    // YOU waving, the Lobbyist alive again with the medicine stack and the stickered briefcase
    const you = stand(Rw.x - 130, on(Rw, 130), k, K.person(copy(YOU, { look: "right", mood: "smile", arms: [[-10, -4], [150, 170]] })));
    const lo = LOB(K, { mood: "smile", look: "left", arms: [[-135, 30], [-120, 20]] }), RL = K.rig(lo), lbx = Rw.x + 120;
    const lob = stand(lbx, on(Rw, 120), k, K.person(lo));
    const held = at(lbx + k * (RL.hand[0][0] + RL.hand[1][0]) / 2, on(Rw, 120) - k * (100 - RL.hand[0][1]) + 40, 0.95, stack(K, "med"));
    const bag = at(lbx + 96, on(Rw, 216) + 4, 1.05, briefcase(K, { sticker: true }), 30);
    const inner = sky + globe(L, "worried") + globe(Rw, "smile") + wm + wobble + you + lob + held + bag;
    const svg = view(-60, 90, 0.95, inner);
    return { svg, alt: "Two little Earths in a starry navy sky: on the left a small worried one, the Weapons Maker teetering on one foot on its top, cradling his missile; on the right a smiling one 1.43 times as wide, YOU in his bowler waving on top beside the Lobbyist, alive, hugging a banded stack of medicine bills, a round cross-seal sticker on his briefcase." };
  },

  "it-is-arithmetic"(H, fid) {
    const { K, C } = H, S = K.STUDIO, ink = C.line;
    // on "arithmetic.": the Calculator (scale 1.3) on the right end of the lectern top, "1.43" on its cracked, taped
    // display, two gaps in its keypad, its mouth a calm smile; the Lobbyist braced with his hands over his ears
    const k = 1.3, cx = 905, base = 792;
    const calc = K.props.calculator({ display: "1.43", mood: "calm" });
    const T = -146, dTop = base + T * k, dMid = base + (T + 17) * k;
    const gaps = [[25.5, -38], [-20.5, -58]].map(([kx, ky]) => `<rect x="${f(cx + kx * k)}" y="${f(base + ky * k)}" width="${f(18 * k)}" height="${f(7 * k)}" fill="#3A3226" stroke="${ink}" stroke-width="2.4"/>`).join("");
    const crack = `<path d="M${f(cx - 40 * k)},${f(dTop + 9)} l14,10 l-6,8 l16,6" fill="none" stroke="${C.cream}" stroke-width="2.6"/>` +
      `<g transform="rotate(-30 ${f(cx - 30 * k)} ${f(dMid)})"><rect x="${f(cx - 30 * k - 38)}" y="${f(dMid - 9)}" width="76" height="18" fill="#E9D9A6" fill-opacity="0.85" stroke="${ink}" stroke-width="2.6"/></g>`;
    const calcAt = at(cx, base, k, calc) + gaps + crack;
    const lo = LOB(K, { look: "left", mood: "worried", arms: [[-140, 115], [140, -95]] });
    const man = stand(1420, 1075, 3.2, K.person(lo));
    const bag = at(1600, 1062, 1.35, briefcase(K, { sticker: true }));
    const svg = push(S, 1.06, H.host("sideeye-closed", "idle", calcAt + man + bag));
    return { svg, alt: "Wishonia at her lectern side-eyes the camera; on the right end of the lectern the Calculator smiles calmly, 1.43 on its cracked, taped display, two keys missing from its keypad; beside the lectern the masked Lobbyist braces with his hands over his ears, his briefcase with its cross-seal sticker at his feet." };
  },
};
