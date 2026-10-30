// Sketches for storyboards/part-12-fda-unsafe-and-ineffective.md: each scene's key frame on a 1920 x 1080 frame,
// drawn with the production art (H.K: kit.js, film.js and the props library) in the atomic-age film look of Part 2.
// Host shots use H.host (KIT.studio's set and the real sprites); a plate frame is one camera framing of its plate.
// Built into the review sheet by tools/storyboard-sheet.mjs.

const GROUND = "#C8B07B", SKY = "#EFE3C4", HZ = "#8E7A55", SEA = "#7FB5B0", SAND = "#E2C98E", BONE = "#F1EAD6", WHITE = "#FBF6E6";
const YOU = { tone: 2, outfit: "suit", hat: "bowler" };
const OFFICIAL = { tone: 0, outfit: "suit", color: 1, hair: 2, glasses: true, hat: null, seed: 12 };
const f1 = (n) => (+n).toFixed(1);
// The scale's tilt once the 3,389 land (KIT.props.balanceScale: positive = right pan down).
const TILT = 34;

// ── Shared drawings ──────────────────────────────────────────────────────
// The heap of tiny grinning skeletons on the scale's right pan (its rim is 84 cos t, -150 + 84 sin t, then 64
// below, in the scale's units), for a scale drawn at (sx, ground), k times. look: where the skulls all turn.
function heap(H, sx, ground, k, tilt, s, look) {
  const t = (tilt * Math.PI) / 180, px = sx + k * 84 * Math.cos(t), py = ground + k * (-150 + 84 * Math.sin(t) + 64);
  let out = "", seed = 7;
  const r = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296);
  [[12, 0], [11, 1], [9, 2], [7, 3], [5, 4], [3, 5], [1, 6]].forEach(([n, row]) => {
    for (let i = 0; i < n; i++) {
      const x = px + (i - (n - 1) / 2) * 30 * s / 0.34 + (r() - 0.5) * 10, y = py - row * 22 * s / 0.34 - 18;
      out += H.at(f1(x), f1(y), s, H.K.person({ tone: (i + row) % 4, skeleton: true, plain: true, look: look || (r() < 0.5 ? "left" : "right"), arms: [[-40 - r() * 120, -20 - r() * 140], [40 + r() * 120, 20 + r() * 140]] }).replace(/<g class="leg-[lr]">[\s\S]*?<\/g>/g, ""), f1((r() - 0.5) * 40));
    }
  });
  return out;
}
// A plain field: sky down to the horizon at y hz, the ground below it.
function field(hz, sky = SKY, ground = GROUND) {
  return `<rect width="1920" height="1080" fill="${ground}"/><rect width="1920" height="${hz}" fill="${sky}"/><path d="M0,${hz} H1920" stroke="${HZ}" stroke-width="3" opacity="0.6"/>`;
}
// A person standing with its feet on y feet, k times life size (KIT.person units: feet at y 100).
function man(H, o, x, feet, k, extra = "") {
  return H.at(x, feet - 100 * k, k, H.K.person(o) + extra);
}
// A big number in the sky: Fraunces Black, navy on a light plate (cream on a dark one).
function num(x, y, size, text, fill = "#112845") {
  return `<text x="${x}" y="${y}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${size}" letter-spacing="4" fill="${fill}">${text}</text>`;
}
// A shadowed cream heading word for the title card.
function heading(x, y, size, text, C) {
  const t = (dx, dy, fill, extra = "") => `<text x="${x + dx}" y="${y + dy}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${size}" fill="${fill}" ${extra}>${text}</text>`;
  return t(size * 0.04, size * 0.053, C.ink) + t(0, 0, C.cream, `stroke="${C.cream}" stroke-width="${f1(size * 0.03)}" stroke-linejoin="round"`);
}
// A walking paper (KIT.money) at x, y, scale k, legs l (0 or 1); rot tilts it.
function bill(H, kind, x, y, k, l = 0, rot = 0) {
  return `<g transform="translate(${x},${y}) rotate(${rot}) scale(${k})">${H.K.money(kind, l)}</g>`;
}
// Smoke squiggles rising from (x, y).
function smoke(x, y, s, col = "#8C8782") {
  return [-14, 0, 14].map((dx, i) => `<path d="M${x + dx * s},${y - i * 6 * s} l${-7 * s},${-12 * s} l${7 * s},${-12 * s} l${-7 * s},${-12 * s}" fill="none" stroke="${col}" stroke-width="${4 * s}" stroke-linecap="round"/>`).join("");
}

// The approval cabinet (the part's spine), standing on (0, 0), 230 wide and about 470 tall with its hourglass.
// o: { bottle (the SAFE bottle on the top shelf), preserver (the life preserver on the bottom shelf), hand (a
// handprint on the glass) }.
function cabinet(H, o = {}) {
  const { K, C } = H, ink = C.line;
  const glass = "#DDE9E6";
  let s = `<rect x="-112" y="-40" width="14" height="40" fill="${C.tan}" stroke="${ink}" stroke-width="4"/><rect x="98" y="-40" width="14" height="40" fill="${C.tan}" stroke="${ink}" stroke-width="4"/>` +
    `<rect x="-118" y="-380" width="236" height="342" fill="${C.cream}" stroke="${ink}" stroke-width="5"/>` +
    `<rect x="-100" y="-362" width="200" height="306" fill="${glass}" stroke="${ink}" stroke-width="3"/>` +
    `<path d="M-100,-210 H100" stroke="${ink}" stroke-width="5"/><path d="M-100,-212 H100" stroke="${C.tan}" stroke-width="3"/>`;
  if (o.bottle) s += H.at(-10, -213, 1.15, K.props.pillBottle({ face: "smile", label: "SAFE" }));
  if (o.preserver) s += H.at(0, -100, 1, preserver(C));
  s += `<path d="M-84,-350 L-60,-350 L-96,-280 L-100,-290 Z M60,-200 L78,-200 L48,-140 L40,-150 Z" fill="#FFFFFF" opacity="0.55"/>`;
  if (o.hand) s += `<g transform="translate(64,-150) rotate(12)" fill="#7E8C9A" opacity="0.45"><ellipse cx="0" cy="0" rx="13" ry="15"/><rect x="-12" y="-36" width="5" height="22" rx="2"/><rect x="-5" y="-40" width="5" height="26" rx="2"/><rect x="2" y="-38" width="5" height="24" rx="2"/><rect x="9" y="-32" width="5" height="20" rx="2"/><rect x="12" y="-6" width="12" height="5" rx="2" transform="rotate(-30 12 -6)"/></g>`;
  // the hasp and its padlock, on the right edge of the door
  s += `<rect x="108" y="-232" width="20" height="44" fill="${C.slate}" stroke="${ink}" stroke-width="3"/>` + H.at(120, -168, 1.3, K.props.padlock({}));
  // the hourglass on top, its base reading 8.2 YEARS
  s += `<rect x="-62" y="-400" width="124" height="20" fill="${C.rust}" stroke="${ink}" stroke-width="4"/>` +
    `<text x="0" y="-385" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="15" letter-spacing="1" fill="${C.cream}">8.2 YEARS</text>` +
    `<rect x="-62" y="-520" width="124" height="16" fill="${C.rust}" stroke="${ink}" stroke-width="4"/>` +
    `<rect x="-54" y="-504" width="8" height="104" fill="${C.tan}" stroke="${ink}" stroke-width="3"/><rect x="46" y="-504" width="8" height="104" fill="${C.tan}" stroke="${ink}" stroke-width="3"/>` +
    `<path d="M-38,-502 H38 L6,-452 L38,-402 H-38 L-6,-452 Z" fill="#EAF2F0" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/>` +
    `<path d="M-22,-480 H22 L4,-454 H-4 Z" fill="${C.yellow}"/><path d="M-30,-404 H30 L16,-424 Q0,-432 -16,-424 Z" fill="${C.yellow}"/><path d="M0,-452 V-426" stroke="${C.yellow}" stroke-width="3"/>`;
  return `<g class="approval-cabinet">${s}</g>`;
}
// A ring life preserver, about 92 across, centered on (0, -46).
function preserver(C) {
  const ink = C.line;
  let s = `<circle cx="0" cy="-46" r="44" fill="${WHITE}" stroke="${ink}" stroke-width="4"/><circle cx="0" cy="-46" r="20" fill="none" stroke="${ink}" stroke-width="4"/>`;
  for (const a of [45, 135, 225, 315]) {
    const r = (a * Math.PI) / 180, x1 = 21 * Math.cos(r), y1 = -46 + 21 * Math.sin(r), x2 = 43 * Math.cos(r), y2 = -46 + 43 * Math.sin(r);
    s += `<path d="M${f1(x1)},${f1(y1)} L${f1(x2)},${f1(y2)}" stroke="${C.war}" stroke-width="18"/>`;
  }
  return s + `<circle cx="0" cy="-46" r="44" fill="none" stroke="${ink}" stroke-width="4"/><circle cx="0" cy="-46" r="20" fill="none" stroke="${ink}" stroke-width="4"/>`;
}
// YOU's skeleton slumped on the floor against the cabinet on his left, his bowler on, legs out to the right, his
// left palm still flat on the glass with its smudge round it. Sitting at (x, floor), k times life size.
function slumped(H, x, floor, k) {
  const { K } = H;
  const o = { ...YOU, skeleton: true, arms: [[-140, -160], [20, 10]], build: { legPose: [[80, 90], [86, 94]] } };
  const R = K.rig(o), hx = x + k * R.hand[0][0], hy = floor - 100 * k + k * R.hand[0][1];
  const smudge = `<g transform="translate(${f1(hx)},${f1(hy)}) rotate(-20) scale(${f1(k * 0.9)})" fill="#7E8C9A" opacity="0.4"><ellipse cx="0" cy="0" rx="11" ry="13"/><rect x="-10" y="-30" width="4" height="20" rx="2"/><rect x="-4" y="-34" width="4" height="24" rx="2"/><rect x="2" y="-32" width="4" height="22" rx="2"/><rect x="8" y="-27" width="4" height="18" rx="2"/></g>`;
  return smudge + H.at(x, floor - 100 * k, k, K.person(o));
}
// The smoke detector of smoke-detector-by-mail on the studio wall, its center at (0, 0), about 200 across.
// charred: black, smoking, white eyes blinking open; the singed letter held up and the mailbox flag raised.
function detector(H, charred) {
  const { C, K } = H, ink = C.line;
  const body = charred ? "#2B2420" : C.cream, rim = charred ? "#3A302A" : "#E2D6B2", eyeW = WHITE;
  let s = `<rect x="-20" y="-130" width="40" height="26" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>` +
    `<ellipse cx="0" cy="0" rx="100" ry="96" fill="${rim}" stroke="${ink}" stroke-width="5"/><ellipse cx="0" cy="-6" rx="78" ry="70" fill="${body}" stroke="${ink}" stroke-width="3"/>`;
  for (let i = -3; i <= 3; i++) s += `<path d="M${i * 16},40 v18" stroke="${charred ? "#1A1512" : C.tan}" stroke-width="5" stroke-linecap="round"/>`;
  s += `<ellipse cx="-28" cy="-16" rx="18" ry="20" fill="${eyeW}" stroke="${ink}" stroke-width="3"/><ellipse cx="28" cy="-16" rx="18" ry="20" fill="${eyeW}" stroke="${ink}" stroke-width="3"/>` +
    `<circle cx="-24" cy="-14" r="7" fill="${ink}"/><circle cx="32" cy="-14" r="7" fill="${ink}"/>` +
    (charred ? `<path d="M-44,-38 L-12,-30 M44,-38 L12,-30" stroke="${ink}" stroke-width="4"/>` : `<path d="M-46,-30 Q-28,-40 -10,-30 M46,-30 Q28,-40 10,-30" fill="none" stroke="${ink}" stroke-width="4"/>`) +
    `<path d="M-16,22 Q0,${charred ? 18 : 32} 16,22" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`;
  // the mailbox on its right side, its flag up
  s += `<g transform="translate(96,10)"><rect x="0" y="-26" width="58" height="40" rx="18" fill="${charred ? "#3A302A" : C.peri}" stroke="${ink}" stroke-width="4"/><rect x="40" y="-66" width="7" height="44" fill="${charred ? "#5A3A2A" : C.war}" stroke="${ink}" stroke-width="2.4"/><rect x="40" y="-66" width="26" height="16" fill="${charred ? "#5A3A2A" : C.war}" stroke="${ink}" stroke-width="2.4"/></g>`;
  // the arm holding up the letter
  s += `<path d="M-90,10 L-130,-40 L-140,-90" fill="none" stroke="${ink}" stroke-width="7" stroke-linejoin="miter"/>` +
    `<g transform="translate(-150,-150) rotate(-8)"><rect x="-58" y="-36" width="116" height="72" fill="${charred ? "#E4D7B8" : WHITE}" stroke="${ink}" stroke-width="4"/><path d="M-58,-36 L0,6 L58,-36" fill="none" stroke="${ink}" stroke-width="2.4"/>` +
    `<rect x="30" y="-30" width="20" height="22" fill="${C.war}" stroke="${ink}" stroke-width="2"/>` +
    `<text x="-6" y="26" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="20" letter-spacing="1" fill="${ink}">RE: SMOKE</text>` +
    (charred ? `<path d="M-58,-36 l10,8 l6,-8 l8,8 l10,-6 M58,36 l-8,-8 l-8,6 l-6,-8 M-58,20 l8,4 l-8,6" fill="none" stroke="#2B2420" stroke-width="4"/>` : "") + "</g>";
  if (charred) s += smoke(-10, -110, 1.6) + smoke(-150, -200, 1.0);
  return s;
}
// A wire wastepaper basket on the studio floor: its rim's middle at (0, 0), 150 wide; papers: how many medicine
// papers poke out of it.
function wastebasket(H, papers) {
  const { C, K } = H, ink = C.line;
  let s = "";
  for (let i = 0; i < papers; i++) s += bill(H, "med", -40 + i * 34, -14 - (i % 2) * 10, 0.9, 1, -30 + i * 22);
  s += `<path d="M-75,0 L75,0 L60,200 L-60,200 Z" fill="${C.slate}" fill-opacity="0.35" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>`;
  for (let i = -4; i <= 4; i++) s += `<path d="M${i * 16},0 L${i * 12.8},200" stroke="${ink}" stroke-width="2.6"/>`;
  for (const y of [50, 100, 150]) s += `<path d="M${f1(-75 + y * 0.075)},${y} H${f1(75 - y * 0.075)}" stroke="${ink}" stroke-width="2.6"/>`;
  return s + `<rect x="-80" y="-6" width="160" height="12" rx="3" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>`;
}
// The Earth case file standing propped up on the lectern, its bottom middle at (0, 0), 190 wide; stamps: the marks on it.
function caseFile(H, stamps) {
  return H.K.props.caseFile({ stamps });
}
// Wishonia's coffee mug, standing on (0, 0).
function mug(H) {
  const { C } = H, ink = C.line;
  return `<path d="M22,-50 q24,4 22,22 q-2,16 -22,16" fill="none" stroke="${ink}" stroke-width="8"/><path d="M22,-50 q24,4 22,22 q-2,16 -22,16" fill="none" stroke="${C.orange}" stroke-width="4"/>` +
    `<path d="M-26,-62 H26 L22,0 H-22 Z" fill="${C.orange}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/><path d="M-24,-54 H24" stroke="${C.cream}" stroke-width="4"/>`;
}
// The host set's lectern props: the mug at the right end, the case file at the left end.
function lecternProps(H, stamps = 1) {
  const S = H.K.STUDIO, cx = S.lect[0], hw = S.lect[1] / 2, top = S.top;
  return H.at(cx + hw - 50, top + 4, 1, mug(H)) + H.at(cx - hw + 120, top + 6, 0.82, caseFile(H, stamps));
}

export default {
  "fda-unsafe-and-ineffective-title"(H, fid) {
    const { K, C } = H;
    const cx = 960, cy = 300, rx = 200, ry = 62;
    const orbits = [0, 60, -60].map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = [[0, 0.3], [60, 2.4], [-60, 4.4]].map(([a, th]) => {
      const r = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return bill(H, "war", cx + ex * Math.cos(r) - ey * Math.sin(r), cy + ex * Math.sin(r) + ey * Math.cos(r) - 6, 0.62, 1);
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    const mark = `<g transform="translate(960,742) rotate(-9)"><rect x="-330" y="-74" width="660" height="148" fill="none" stroke="${C.war}" stroke-width="14"/><rect x="-308" y="-54" width="616" height="108" fill="none" stroke="${C.war}" stroke-width="5"/>` +
      `<text x="0" y="40" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="112" letter-spacing="10" fill="${C.war}">APPROVED</text></g>`;
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus +
      heading(960, 588, 68, "THE FDA IS", C) + heading(960, 724, 136, "UNSAFE AND", C) + heading(960, 860, 136, "INEFFECTIVE", C) +
      `<g opacity="0.9">${mark}</g>`;
    return { svg, alt: "The period title card: THE FDA IS UNSAFE AND INEFFECTIVE in cream on navy under the atom emblem with three running papers, a red APPROVED stamp mark tilted across the heading." };
  },

  "smoke-detector-by-mail"(H, fid) {
    const { K, C } = H, S = K.STUDIO;
    const lx = S.lect[0] - S.lect[1] / 2;
    const front = lecternProps(H, 1) + H.at(410, 872, 1, wastebasket(H, 3)) +
      bill(H, "med", lx + 22, S.top - 42, 0.95, 0, -16) + `<path d="M${lx - 6},${S.top - 86} q-8,-14 2,-24" fill="none" stroke="${C.line}" stroke-width="3"/>` +
      H.at(1440, 330, 1.2, detector(H, true));
    const svg = H.host("sideeye-closed", "idle", front);
    return { svg, alt: "Wishonia at her lectern side-eyes the camera; on the studio wall to her right the smoke detector hangs charred black and smoking, white eyes open, still holding up its singed RE: SMOKE letter with its mailbox flag raised; medicine papers in the wastebasket beside the lectern, the last one teetering at the lectern's edge." };
  },

  "vioxx-by-fax"(H, fid) {
    const { K, C } = H, ink = C.line;
    // the pharmacy counter under its striped awning, the board above with 55,000
    let stripes = "";
    for (let i = 0; i < 10; i++) stripes += `<path d="M${380 + i * 116},120 H${496 + i * 116} L${500 + i * 116},200 H${384 + i * 116} Z" fill="${i % 2 ? C.cream : C.rust}"/>`;
    let scallop = "";
    for (let i = 0; i < 10; i++) scallop += `<path d="M${384 + i * 116},200 a58,26 0 0,0 116,0 Z" fill="${i % 2 ? C.cream : C.rust}" stroke="${ink}" stroke-width="4"/>`;
    const awning = `<rect x="396" y="200" width="18" height="520" fill="#7A5634" stroke="${ink}" stroke-width="4"/><rect x="1506" y="200" width="18" height="520" fill="#7A5634" stroke="${ink}" stroke-width="4"/>` +
      stripes + `<path d="M380,120 H1540 L1544,200 H376 Z" fill="none" stroke="${ink}" stroke-width="5"/>` + scallop;
    const board = `<rect x="1060" y="252" width="420" height="150" fill="${WHITE}" stroke="${ink}" stroke-width="6"/>` + num(1270, 368, 112, "55,000");
    let planks = "";
    for (let y = 760; y < 1000; y += 34) planks += `<path d="M430,${y} H1490" stroke="#8C6440" stroke-width="3"/>`;
    const counter = `<rect x="420" y="720" width="1080" height="300" fill="${C.tan}" stroke="${ink}" stroke-width="6"/>` + planks + `<rect x="400" y="700" width="1120" height="26" fill="${C.rust}" stroke="${ink}" stroke-width="6"/>`;
    const bottle = H.at(700, 704, 2.6, K.props.pillBottle({ face: "grin", label: "VIOXX" })) + H.at(704, 700, 1.25, K.props.stampMark({ text: "APPROVED", angle: -12, fontSize: 22 }));
    // the three patients, x-rayed into skeletons, still holding their pill cups
    const cup = (R) => `<g transform="translate(${f1(R.hand[1][0])},${f1(R.hand[1][1] - 6)})"><path d="M-7,-10 L7,-10 L5,2 L-5,2 Z" fill="${WHITE}" stroke="${ink}" stroke-width="2.2"/></g>`;
    const pats = [
      { o: { tone: 1, outfit: "shirt", kind: "barrel", color: 2, look: "left", arms: [[10, 6], [-40, -120]] }, x: 1040 },
      { o: { tone: 3, outfit: "dress", hair: 1, color: 0, look: "left", arms: [[10, 6], [-40, -120]] }, x: 1250 },
      { o: { tone: 0, outfit: "shirt", kind: "twig", hat: "fedora", color: 1, look: "left", arms: [[10, 6], [-40, -120]] }, x: 1440 },
    ].map(({ o, x }) => man(H, { ...o, skeleton: true }, x, 1040, 2.5, cup(K.rig(o)))).join("");
    const svg = field(300) + awning + board + counter + bottle + pats;
    return { svg, alt: "At the pharmacy counter under a striped awning, the smiling VIOXX bottle wears an APPROVED stamp under a board reading 55,000; three patients stand at the counter as grinning skeletons, still holding their pill cups." };
  },

  "twenty-first-century"(H, fid) {
    const { K, C } = H, S = K.STUDIO;
    const front = lecternProps(H, 1) + H.at(410, 872, 1, wastebasket(H, 3)) +
      bill(H, "med", 470, S.top + 20, 1.0, 1, -40) +
      H.at(1440, 330, 1.2, detector(H, true));
    const svg = H.host("eyeroll-closed", "arms-crossed", front);
    return { svg, alt: "Wishonia at her lectern, arms crossed, rolls her eyes at the camera while the last medicine paper hops off the lectern's edge into the wastebasket; the charred smoke detector on the wall behind." };
  },

  "five-years-later"(H, fid) {
    const { K, C } = H, ink = C.line;
    // rows of headstones to the horizon behind him
    let rows = "";
    const hz = 360;
    [[0.25, 30], [0.36, 80], [0.5, 140], [0.7, 220]].forEach(([s, d]) => {
      for (let x = -40; x < 1960; x += 230 * s) rows += H.at(x + (d % 115), hz + d, s * 1.1, K.props.headstone({ text: "" }));
    });
    const desk = `<rect x="560" y="700" width="760" height="40" fill="${C.rust}" stroke="${ink}" stroke-width="6"/><rect x="590" y="740" width="40" height="230" fill="${C.rust}" stroke="${ink}" stroke-width="5"/><rect x="1250" y="740" width="40" height="230" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>`;
    const faxes = `<rect x="1090" y="664" width="150" height="38" fill="${WHITE}" stroke="${ink}" stroke-width="3"/><rect x="1096" y="650" width="150" height="16" fill="${WHITE}" stroke="${ink}" stroke-width="3"/>` + H.at(1166, 652, 2.2, K.props.laptop({ screen: "" }).replace(/<g class="laptop-lid"/, '<g class="laptop-lid" transform="scale(1,0.08) translate(0,-80)"')) +
      `<path d="M1100,612 q60,-46 130,4 M1110,636 l16,-30 M1150,620 l0,-28 M1196,622 l10,-26" fill="none" stroke="#FFFFFF" stroke-width="2.2" opacity="0.9"/>`;
    const fax = `<rect x="620" y="632" width="190" height="70" fill="${C.peri}" stroke="${ink}" stroke-width="5"/><rect x="640" y="616" width="150" height="20" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>`;
    // the official, flattened into his chair under the sign
    const chair = `<rect x="820" y="760" width="190" height="24" fill="${C.slate}" stroke="${ink}" stroke-width="5"/><rect x="830" y="784" width="16" height="190" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><rect x="984" y="784" width="16" height="190" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>`;
    // pancaked flat on the seat: arms and legs splayed out from under the sign, his magnifier still in one hand
    // pancaked flat on the seat under the sign: a wide flat disc of navy suit with his flat bald head at the front,
    // his eyes blinking, his flat shoes and hands (one still holding the magnifier) splayed out from under it
    const skin = "#F4E3CC", suit = "#24304D";
    const flat = `<ellipse cx="915" cy="772" rx="300" ry="30" fill="${suit}" stroke="${ink}" stroke-width="5"/><path d="M640,780 Q915,806 1190,780" fill="none" stroke="${C.orange}" stroke-width="3"/>` +
      `<path d="M600,770 l-50,-6 l-6,14 l54,8 Z M1230,770 l50,-8 l6,14 l-54,8 Z" fill="${skin}" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M780,792 l-70,10 l-4,14 l80,-4 Z M1050,792 l70,10 l4,14 l-80,-4 Z" fill="#1B1714" stroke="${ink}" stroke-width="4"/>` +
      `<ellipse cx="915" cy="782" rx="96" ry="18" fill="${skin}" stroke="${ink}" stroke-width="4"/>` +
      `<g fill="${WHITE}" stroke="${ink}" stroke-width="3"><ellipse cx="892" cy="782" rx="15" ry="9"/><ellipse cx="938" cy="782" rx="15" ry="9"/></g><circle cx="896" cy="783" r="5" fill="${ink}"/><circle cx="942" cy="783" r="5" fill="${ink}"/>` +
      `<g transform="translate(1300,760) rotate(70) scale(2.4)"><path d="M0,0 L-6,14" stroke="${ink}" stroke-width="5"/><circle cx="5" cy="-11" r="11" fill="#FFFFFF" fill-opacity="0.35" stroke="${ink}" stroke-width="3.4"/></g>`;
    const sign = `<g transform="translate(915,744) rotate(-2)"><rect x="-210" y="-60" width="420" height="74" fill="${WHITE}" stroke="${ink}" stroke-width="6"/><rect x="-198" y="-50" width="396" height="54" fill="none" stroke="${C.orange}" stroke-width="2"/>` +
      `<text x="0" y="-8" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="42" letter-spacing="3" fill="${ink}">SAFETY SYSTEM</text></g>` +
      `<path d="M712,688 L730,0" stroke="${C.slate}" stroke-width="6" stroke-dasharray="14 6"/><path d="M1110,0 V170 l-12,18 M1110,170 l14,14" stroke="${C.slate}" stroke-width="6" stroke-dasharray="14 6"/>` +
      `<path d="M1112,690 q22,-30 8,-60 q-14,-26 8,-50" fill="none" stroke="${C.slate}" stroke-width="6" stroke-dasharray="14 6"/>`;
    const svg = field(hz) + rows + desk + fax + faxes + chair + flat + sign;
    return { svg, alt: "The official lies flattened into his chair under the fallen SAFETY SYSTEM sign, one chain snapped, only his eyes blinking out from under it; his fax machine and a cobwebbed laptop on the desk; rows of headstones behind him to the horizon." };
  },

  "fire-department-water"(H, fid) {
    const { K, C } = H, ink = C.line;
    const ground = 900;
    // the burning house on the right
    const house = H.at(1560, ground - 10, 1.4, K.props.house({ variant: 1, smoke: false })) +
      [[1400, 640, 1.3], [1560, 520, 1.8], [1700, 620, 1.3], [1480, 760, 0.9], [1650, 770, 0.9]].map(([x, y, s]) => K.flames(x, y, s)).join("");
    // the NIH truck on the left, sagging under an office building, its tires flat
    let windows = "";
    for (let r = 0; r < 4; r++) for (let c = 0; c < 6; c++) windows += `<rect x="${130 + c * 92}" y="${210 + r * 78}" width="56" height="46" fill="${C.cyan}" stroke="${ink}" stroke-width="3"/>`;
    const building = `<rect x="100" y="170" width="580" height="360" fill="#B9B5AE" stroke="${ink}" stroke-width="6"/>` + windows +
      `<path d="M120,540 L230,170 M660,540 L560,170" stroke="${C.tan}" stroke-width="10"/><path d="M120,540 L230,170 M660,540 L560,170" stroke="${ink}" stroke-width="2" fill="none"/>`;
    const truck = `<path d="M60,540 H700 V800 H60 Z" fill="${C.red}" stroke="${ink}" stroke-width="6"/><path d="M700,600 H820 L880,680 V800 H700 Z" fill="${C.red}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
      `<path d="M716,616 H812 L852,672 H716 Z" fill="${C.cyan}" stroke="${ink}" stroke-width="4"/><rect x="60" y="780" width="820" height="24" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` +
      `<text x="250" y="720" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="96" letter-spacing="8" fill="${C.cream}" stroke="${ink}" stroke-width="3" paint-order="stroke">NIH</text>` +
      [180, 560, 790].map((x) => `<ellipse cx="${x}" cy="${ground - 26}" rx="80" ry="34" fill="#1E1B24" stroke="${ink}" stroke-width="5"/><ellipse cx="${x}" cy="${ground - 30}" rx="26" ry="14" fill="#8C8782"/>`).join("") +
      H.at(500, 776, 1.05, K.props.gauge({ label: "WATER", value: 0.04, window: "3%", zones: [] }));
    // the scientist hanging off the back by one hand
    const sci = man(H, K.castOpts("scientist", { look: "left", arms: [[-178, -170], [40, 70]], mood: "worried", holdL: null, holdR: "flask" }), 96, 880, 1.6);
    // the firefighter with the water pistol and its one squirt
    const ff = { tone: 3, outfit: "overalls", color: 0, look: "right", arms: [[60, 90], [70, 96]] };
    const R = K.rig(ff), k = 2.5, fx = 1080, fy = 1000 - 100 * k, hx = fx + k * R.hand[1][0], hy = fy + k * R.hand[1][1];
    const helmet = `<path d="M-24,-6 L-18,-26 L0,-34 L18,-26 L24,-6 Z" fill="${C.red}" stroke="${ink}" stroke-width="2.6"/><path d="M-30,-4 H34 L30,2 H-26 Z" fill="${C.red}" stroke="${ink}" stroke-width="2.4"/>`;
    const firefighter = H.at(fx, fy, k, K.person(ff).replace("<!--face-end-->", helmet + "<!--face-end-->")) +
      `<g transform="translate(${f1(hx)},${f1(hy)})"><path d="M-10,-6 H40 V8 H10 L6,24 H-8 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/></g>` +
      `<path d="M${f1(hx + 44)},${f1(hy)} Q${f1(hx + 140)},${f1(hy - 90)} ${f1(hx + 230)},${f1(hy - 20)}" fill="none" stroke="${C.cyan}" stroke-width="7" stroke-linecap="round" stroke-dasharray="20 14"/>`;
    const svg = field(480) + `<rect y="${ground}" width="1920" height="180" fill="#B09363"/>` + house + `<g transform="translate(60,0)">${building + truck}</g>` + sci + firefighter;
    return { svg, alt: "A firefighter aims a little water pistol at a burning house and gets one squirt; behind him the NIH fire truck sags on flat tires under the office building strapped on top, its gauge reading WATER 3%, the scientist hanging off the back by one hand." };
  },

  "committee-8-years"(H, fid) {
    const { K, C } = H, ink = C.line;
    const floor = 880;
    // the committee table behind, its six members bearded
    let members = "";
    const builds = [{ kind: "box" }, { kind: "vee" }, { kind: "egg" }, { kind: "box" }, { kind: "vee" }, { kind: "egg" }];
    builds.forEach((b, i) => {
      const o = { tone: i % 4, outfit: "suit", color: (i + 1) % 4, hair: i % 2 ? 2 : 0, glasses: i % 3 === 0, hat: i === 4 ? "fedora" : null, ...b, mood: "flat", arms: [[30, 80], [-30, -80]] };
      const R = K.rig(o);
      const beard = `<path d="M${f1(R.mouth[0] - 12)},${f1(R.mouth[1] - 2)} L${f1(R.mouth[0] + 12)},${f1(R.mouth[1] - 2)} L${f1(R.mouth[0] + 6)},${f1(R.mouth[1] + 70)} L${f1(R.mouth[0])},${f1(R.mouth[1] + 84)} L${f1(R.mouth[0] - 6)},${f1(R.mouth[1] + 70)} Z" fill="${WHITE}" stroke="${ink}" stroke-width="2"/>`;
      members += man(H, o, 900 + i * 165, 760, 1.55, beard);
    });
    const table = `<rect x="820" y="640" width="1060" height="36" fill="${C.rust}" stroke="${ink}" stroke-width="6"/><rect x="840" y="676" width="1020" height="190" fill="#7A3F27" stroke="${ink}" stroke-width="5"/>` +
      [0, 1, 2, 3, 4, 5].map((i) => `<rect x="${860 + i * 165}" y="604" width="90" height="38" fill="${WHITE}" stroke="${ink}" stroke-width="3"/><path d="M${905 + i * 165},604 V642" stroke="${ink}" stroke-width="2"/>`).join("") +
      `<path d="M1290,604 q30,-40 54,-6" fill="${WHITE}" stroke="${ink}" stroke-width="3"/>`;
    // the empty test bench
    const bench = `<rect x="760" y="740" width="240" height="22" fill="${C.tan}" stroke="${ink}" stroke-width="5"/><rect x="776" y="762" width="16" height="140" fill="${C.tan}" stroke="${ink}" stroke-width="4"/><rect x="968" y="762" width="16" height="140" fill="${C.tan}" stroke="${ink}" stroke-width="4"/>`;
    // the cabinet with the SAFE bottle; YOU's skeleton slumped against it, his palm still on the glass
    const cab = H.at(400, floor, 1.4, cabinet(H, { bottle: true }));
    const svg = `<rect width="1920" height="1080" fill="#D9C08E"/><rect y="${floor - 60}" width="1920" height="300" fill="${GROUND}"/><path d="M0,${floor - 60} H1920" stroke="${HZ}" stroke-width="3" opacity="0.6"/>` +
      members + table + bench + cab + slumped(H, 650, floor, 2.3);
    return { svg, alt: "YOU's skeleton in his bowler slumps against the locked approval cabinet, one bony palm still flat on the glass; the SAFE bottle on its top shelf, the hourglass on top reading 8.2 YEARS; behind, the six committee members with long white beards at their table, the chair turning a page." };
  },

  "billion-volunteers"(H, fid) {
    const { K, C } = H, ink = C.line;
    const wallTop = 260, wallBot = 820;
    // the orderly behind the wall, his head over it on a long neck
    const ord = man(H, K.castOpts("orderly", { look: "left", build: { hs: 0.72, legs: 1.3, th: 1.2, neck: 15, armL: 1.25 }, arms: [[-6, -2], [6, 2]] }), 1130, wallBot - 20, 2.1);
    let bricks = "";
    for (let y = wallTop + 40; y < wallBot; y += 40) bricks += `<path d="M0,${y} H1920" stroke="#9C6B4A" stroke-width="2.4"/>`;
    for (let y = wallTop; y < wallBot; y += 40) for (let x = ((y / 40) % 2) * 60; x < 1920; x += 120) bricks += `<path d="M${x},${y} v40" stroke="#9C6B4A" stroke-width="2.4"/>`;
    const wall = `<rect y="${wallTop}" width="1920" height="${wallBot - wallTop}" fill="${C.tan}" stroke="${ink}" stroke-width="6"/>` + bricks + `<rect y="${wallTop - 16}" width="1920" height="22" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>`;
    // the tiny door, knee high, with its slot and the tag
    const door = H.at(960, wallBot, 0.62, K.props.door({ color: C.rust, slot: true })) + H.at(976, wallBot - 70, 1.7, K.props.priceTag({ text: "0.177%", angle: 40 }));
    // cracks in the wall round each flattened human, and the stars of the impact
    const cracks = [300, 520, 740, 1200, 1420, 1640].map((x) => `<path d="M${x - 150},${wallBot - 200} l-30,-24 l-14,-30 M${x + 150},${wallBot - 190} l34,-20 l10,-34 M${x},${wallBot - 250} l6,-40 l-14,-30" fill="none" stroke="${ink}" stroke-width="3"/>` +
      K.star(x - 40, wallBot - 260, 14, C.yellow) + K.star(x + 46, wallBot - 250, 10, C.yellow)).join("");
    // the front row, squashed flat against the wall: wide, short, arms splayed, eyes blinking
    const flat = [[300, 0], [520, 1], [740, 2], [1200, 3], [1420, 0], [1640, 1]].map(([x, t]) => {
      const o = { tone: t, outfit: t % 2 ? "dress" : "shirt", hair: t % 2, color: (t + 2) % 4, mood: "worried", arms: [[-88, -92], [88, 92]], build: { legPose: [[-30, -30], [30, 30]] }, seed: x };
      const k = 2.1, sx = 1.45, sy = 0.62;
      return `<g transform="translate(${x},${f1(wallBot - 100 * k * sy)}) scale(${f1(k * sx)},${f1(k * sy)})">${K.person(o)}</g>`;
    }).join("");
    // the crowd still pressing in behind them: the backs of their heads along the bottom edge
    let crowd = "";
    for (let i = 0; i < 11; i++) {
      const x = 60 + i * 180, y = 1010 + (i % 2) * 30, skin = ["#F4E3CC", "#D9B48F", "#A87B57", "#6F4B33"][i % 4];
      crowd += `<ellipse cx="${x}" cy="${y}" rx="64" ry="76" fill="${skin}" stroke="${ink}" stroke-width="5"/><path d="M${x - 66},${y + 6} Q${x - 70},${y - 84} ${x},${y - 80} Q${x + 70},${y - 84} ${x + 66},${y + 6} Q${x},${y + 40} ${x - 66},${y + 6} Z" fill="${i % 3 ? "#1B1714" : C.rust}" stroke="${ink}" stroke-width="5"/>` +
        (i % 4 === 1 ? `<path d="M${x - 80},${y - 50} H${x + 80} L${x + 60},${y - 70} L${x + 50},${y - 120} H${x - 50} L${x - 60},${y - 70} Z" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` : "");
    }
    const svg = field(wallTop - 10) + ord + wall + cracks + door + flat + crowd +
      `<rect y="${wallBot}" width="1920" height="10" fill="${HZ}" opacity="0.5"/>`;
    return { svg, alt: "The front row of patients is squashed flat against a long wall beside a tiny knee-high door, eyes blinking, a 0.177% tag swinging on the door handle; over the wall the orderly's head looks down on his long neck; the crowd presses in behind." };
  },

  "lifeguard-cabinet"(H, fid) {
    const { K, C } = H, ink = C.line;
    const hz = 230, shore = 640;
    // the sea and its line of swimmers and skulls, from the post out to the horizon
    let line = "";
    for (let i = 1; i < 16; i++) {
      const u = i / 15, x = 1470 - u * 860, y = 590 - u * 340, s = 1.7 * (1 - u * 0.85);
      const skull = i % 3 === 1;
      line += skull ? H.at(x, y, s, `<g transform="translate(0,-10)">` + K.person({ skeleton: true, plain: true }).match(/<g class="head">[\s\S]*<!--head-end--><\/g>/)[0] + "</g>")
        : H.at(x, y, s, `<circle cx="0" cy="-30" r="16" fill="${["#F4E3CC", "#D9B48F", "#A87B57", "#6F4B33"][i % 4]}" stroke="${ink}" stroke-width="3"/><path d="M-16,-36 q16,-22 32,0" fill="${i % 2 ? "#1B1714" : C.orange}"/><path d="M14,-34 l14,-30" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`);
      line += `<path d="M${f1(x - 30 * s)},${f1(y - 14 * s)} q${f1(30 * s)},${f1(-10 * s)} ${f1(60 * s)},0" fill="none" stroke="${WHITE}" stroke-width="${f1(3 * s)}"/>`;
    }
    const post = `<rect x="1640" y="300" width="22" height="380" fill="#7A5634" stroke="${ink}" stroke-width="5"/><path d="M1640,340 h-40 v16" fill="none" stroke="${ink}" stroke-width="6"/>` +
      [0, 1].map((i) => `<g transform="translate(${1596 + i * 30},360) rotate(${i ? 8 : -6})"><path d="M-30,0 L30,0 L36,110 L-36,110 Z" fill="${C.orange}" stroke="${ink}" stroke-width="4"/><path d="M-10,0 L0,40 L10,0" fill="none" stroke="${ink}" stroke-width="3"/><path d="M-34,60 H34" stroke="${ink}" stroke-width="3"/></g>`).join("");
    // the first swimmer in line, reaching for the jackets
    const first = `<circle cx="1500" cy="560" r="30" fill="#D9B48F" stroke="${ink}" stroke-width="5"/><path d="M1470,550 q30,-44 60,0" fill="#1B1714"/><path d="M1524,548 L1570,470" stroke="${ink}" stroke-width="12" stroke-linecap="round"/><path d="M1524,548 L1570,470" stroke="#D9B48F" stroke-width="6" stroke-linecap="round"/>` +
      `<path d="M1440,584 q60,-20 120,0" fill="none" stroke="${WHITE}" stroke-width="5"/>`;
    // the tall chair, the lifeguard on it with his binder, blowing the whistle
    const chair = `<path d="M150,880 L230,470 M450,880 L370,470 M180,720 H420 M200,600 H400" stroke="${WHITE}" stroke-width="18"/><path d="M150,880 L230,470 M450,880 L370,470 M180,720 H420 M200,600 H400" stroke="${ink}" stroke-width="3" fill="none"/><rect x="210" y="450" width="180" height="26" fill="${WHITE}" stroke="${ink}" stroke-width="5"/>`;
    const lg = { tone: 1, outfit: "shirt", kind: "twig", color: 3, look: "right", glasses: true, mood: "flat", arms: [[40, 120], [30, 110]], build: { legPose: [[60, 10], [56, 6]] } };
    const RL = K.rig(lg);
    const stripes = [0, 1, 2, 3].map((i) => `<path d="M-14,${f1(RL.shoulder[0][1] + 8 + i * 9)} H14" stroke="${C.war}" stroke-width="4"/>`).join("");
    const zinc = `<path d="M8,-2 l12,-2 l2,6 l-12,2 Z" fill="${WHITE}"/>`;
    const binder = `<g transform="translate(${f1((RL.hand[0][0] + RL.hand[1][0]) / 2)},${f1((RL.hand[0][1] + RL.hand[1][1]) / 2 - 8)})"><rect x="-4" y="-22" width="44" height="34" fill="${C.peri}" stroke="${ink}" stroke-width="2.4"/><rect x="0" y="-20" width="36" height="28" fill="${WHITE}" stroke="${ink}" stroke-width="1.4"/><path d="M4,-14 h26 M4,-8 h26 M4,-2 h20" stroke="${ink}" stroke-width="1"/></g>`;
    const whistle = `<g transform="translate(${f1(RL.mouth[0] + 4)},${f1(RL.mouth[1])})"><rect x="0" y="-3" width="12" height="7" fill="${C.yellow}" stroke="${ink}" stroke-width="1.6"/></g><path d="M${f1(RL.mouth[0] + 22)},${f1(RL.mouth[1] - 8)} l14,-6 M${f1(RL.mouth[0] + 22)},${f1(RL.mouth[1])} l16,0 M${f1(RL.mouth[0] + 22)},${f1(RL.mouth[1] + 8)} l14,6" stroke="${ink}" stroke-width="2"/>`;
    const lifeguard = H.at(300, 462 - 1.9 * RL.hip[0][1], 1.9, K.person(lg).replace("<!--face-end-->", zinc + "<!--face-end-->") + stripes + binder + whistle);
    const cab = H.at(700, 880, 1.1, cabinet(H, { bottle: true, preserver: true }));
    const bucket = `<path d="M1060,800 L1180,800 L1170,880 L1070,880 Z" fill="${C.slate}" stroke="${ink}" stroke-width="5"/><ellipse cx="1120" cy="800" rx="60" ry="12" fill="${SEA}" stroke="${ink}" stroke-width="4"/>`;
    const svg = `<rect width="1920" height="1080" fill="${SAND}"/><rect width="1920" height="${shore}" fill="${SEA}"/><rect width="1920" height="${hz}" fill="${SKY}"/><path d="M0,${hz} H1920" stroke="${HZ}" stroke-width="3" opacity="0.6"/>` +
      `<path d="M0,${shore} q120,-20 240,0 t240,0 t240,0 t240,0 t240,0 t240,0 t240,0 t240,0" fill="none" stroke="${WHITE}" stroke-width="6"/>` +
      line + post + first + chair + lifeguard + cab + slumped(H, 880, 880, 1.8) + bucket;
    return { svg, alt: "On the beach the lifeguard sits on his tall chair blowing his whistle without looking up from his binder; beside him the approval cabinet holds the SAFE bottle and the life preserver, YOU's skeleton slumped against it; out in the sea a line of swimmers and grinning skulls runs from a post with two life jackets on a hook to the horizon." };
  },

  "two-mistakes"(H, fid) {
    const { K, C } = H, ink = C.line;
    // the control panel the size of a wall
    let dials = "";
    for (let i = 0; i < 8; i++) dials += `<circle cx="${180 + i * 210}" cy="140" r="44" fill="${WHITE}" stroke="${ink}" stroke-width="5"/><path d="M${180 + i * 210},140 l${20 - (i % 3) * 14},-30" stroke="${C.war}" stroke-width="5"/>`;
    for (let i = 0; i < 14; i++) dials += `<rect x="${130 + i * 120}" y="640" width="20" height="44" rx="4" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>`;
    const panel = `<rect x="60" y="40" width="1800" height="700" fill="${C.slate}" stroke="${ink}" stroke-width="8"/><rect x="80" y="60" width="1760" height="660" fill="none" stroke="${C.orange}" stroke-width="2"/>` + dials;
    // socket 1: the huge siren; socket 2: the bulb under tape, behind the portrait
    const numeral = (x, n) => `<circle cx="${x}" cy="230" r="44" fill="${C.cream}" stroke="${ink}" stroke-width="5"/><text x="${x}" y="260" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="80" fill="${C.navy}">${n}</text>`;
    const siren = numeral(320, 1) +
      `<rect x="390" y="560" width="260" height="40" fill="#8C8782" stroke="${ink}" stroke-width="5"/><path d="M410,560 V400 Q520,260 630,400 V560 Z" fill="${C.red}" stroke="${ink}" stroke-width="6"/><path d="M450,540 V410 Q470,370 500,350" fill="none" stroke="${WHITE}" stroke-width="10" opacity="0.6"/>`;
    const bulb = numeral(1240, 2) +
      `<g stroke="${C.yellow}" stroke-width="6" stroke-linecap="round"><path d="M1270,300 l-20,-26 M1530,300 l20,-26 M1250,560 l-24,16 M1550,560 l24,16"/></g>` +
      `<g transform="translate(1400,440) rotate(-4)"><rect x="-130" y="-140" width="260" height="270" fill="${C.yellow}" stroke="${ink}" stroke-width="6"/><rect x="-110" y="-120" width="220" height="180" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>` +
      `<defs><clipPath id="${fid}-pc"><rect x="-110" y="-120" width="220" height="180"/></clipPath></defs><g clip-path="url(#${fid}-pc)"><g transform="translate(0,70) scale(1.35)">${K.person({ ...OFFICIAL, mood: "smug" })}</g></g>` +
      `<text x="0" y="88" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="22" letter-spacing="1" fill="${ink}">EMPLOYEE OF</text><text x="0" y="114" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="22" letter-spacing="1" fill="${ink}">THE MONTH</text>` +
      `<path d="M0,-140 L-34,-180 L34,-180 Z" fill="none" stroke="${ink}" stroke-width="3"/></g>`;
    // the official, feet up on the desk, sipping coffee
    const off = { ...OFFICIAL, look: "right", mood: "smug", arms: [[30, 70], [-40, -150]], build: { legPose: [[100, 92], [96, 88]] } };
    const R = K.rig(off), k = 2.6, ox = 700, seat = 870, oy = seat - k * R.hip[0][1];
    const cup = `<g transform="translate(${f1(R.hand[1][0])},${f1(R.hand[1][1] - 4)})"><path d="M-8,-12 H8 L7,4 H-7 Z" fill="${WHITE}" stroke="${ink}" stroke-width="2.4"/></g>`;
    const badge = `<rect x="-22" y="${f1(R.shoulder[0][1] + 6)}" width="14" height="9" fill="${C.yellow}" stroke="${ink}" stroke-width="1.4"/><text x="-15" y="${f1(R.shoulder[0][1] + 13.5)}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="6.5" fill="${ink}">FDA</text>`;
    const desk = `<rect x="840" y="820" width="560" height="34" fill="${C.rust}" stroke="${ink}" stroke-width="6"/><rect x="860" y="854" width="520" height="200" fill="#7A3F27" stroke="${ink}" stroke-width="5"/>`;
    const chair = `<rect x="580" y="870" width="220" height="26" fill="${C.peri}" stroke="${ink}" stroke-width="5"/><rect x="590" y="700" width="26" height="190" fill="${C.peri}" stroke="${ink}" stroke-width="5"/><rect x="680" y="896" width="20" height="150" fill="${C.peri}" stroke="${ink}" stroke-width="4"/>`;
    const svg = `<rect width="1920" height="1080" fill="#D9C08E"/>` + panel + siren + bulb + chair + desk + H.at(ox, oy, k, K.person(off) + cup + badge) + `<rect y="1046" width="1920" height="34" fill="${GROUND}"/>`;
    return { svg, alt: "The official sits with his feet up on his desk sipping coffee in front of a wall-sized control panel: a huge red siren over a painted 1, and over the 2 his framed EMPLOYEE OF THE MONTH portrait, the taped-up bulb glowing round its edges." };
  },

  "i-calculated"(H, fid) {
    const { K, C } = H, S = K.STUDIO, ink = C.line;
    const mx = S.lect[0] - 110, my = S.top;
    const machine = `<g transform="translate(${mx},${my})"><path d="M-90,0 L-80,-70 H80 L90,0 Z" fill="${C.peri}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      [0, 1, 2, 3].map((r) => [0, 1, 2, 3, 4, 5].map((c) => `<rect x="${-66 + c * 22}" y="${-58 + r * 13}" width="15" height="9" rx="2" fill="${C.cream}" stroke="${ink}" stroke-width="1.6"/>`).join("")).join("") +
      `<rect x="90" y="-48" width="40" height="14" fill="${C.slate}" stroke="${ink}" stroke-width="3"/><path d="M130,-41 l26,-20" stroke="${ink}" stroke-width="6"/><circle cx="158" cy="-62" r="8" fill="${C.war}" stroke="${ink}" stroke-width="3"/>` +
      `<rect x="-30" y="-110" width="60" height="44" fill="${C.slate}" stroke="${ink}" stroke-width="4"/></g>` +
      // all that chattering, and one short slip pops out of the top
      `<g transform="translate(${mx},${my - 112}) rotate(-12)"><path d="M-22,0 V-74 L-14,-80 L-6,-74 L2,-80 L10,-74 L18,-80 L22,-76 V0 Z" fill="${WHITE}" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/>` +
      `<path d="M-12,-56 H10 M-12,-40 H4 M-12,-24 H12" stroke="${ink}" stroke-width="2" opacity="0.45"/></g>` +
      `<path d="M${mx - 60},${my - 150} l-22,-14 M${mx - 66},${my - 124} l-26,-2 M${mx + 56},${my - 156} l20,-16 M${mx + 64},${my - 128} l26,-4" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`;
    const svg = H.host("smirk-closed", "counting", H.at(1440, 330, 1.2, detector(H, true)) + H.at(S.lect[0] + S.lect[1] / 2 - 50, S.top + 4, 1, mug(H)) + machine);
    return { svg, alt: "Wishonia at her lectern holds up one finger and smirks at the camera; beside her mug a 1950s adding machine has just dinged and spat out one short paper slip; the charred smoke detector on the wall." };
  },

  "3389-to-1"(H, fid) {
    const { K, C } = H, ink = C.line;
    const ground = 880, k = 3.4, tilt = TILT, sx = 760;
    const scale = H.at(sx, ground, k, K.props.balanceScale({ tilt }));
    const cab = H.at(1430, ground - 40, 1.15, cabinet(H, { bottle: true, preserver: true }));
    const svg = field(600) + num(960, 210, 170, "3,389 : 1") + cab + slumped(H, 1610, ground - 40, 1.7) + scale + heap(H, sx, ground, k, tilt, 0.34, "right");
    return { svg, alt: "A giant brass balance scale: the right pan down under a heap of tiny grinning skeletons, all turned to look at the approval cabinet behind them, YOU's skeleton slumped against it; the left pan up high and empty; 3,389 : 1 in the sky." };
  },

  "thalidomide-every-year"(H, fid) {
    const { K, C } = H, ink = C.line;
    const ground = 940, k = 3.0, tilt = TILT;
    const sx = 900, t = (tilt * Math.PI) / 180;
    const lx = sx - k * 84 * Math.cos(t), ly = ground + k * (-150 - 84 * Math.sin(t) + 64);
    const weight = (w, h, x, y) => `<g transform="translate(${x},${y})"><path d="M${-w / 2},0 L${-w / 2 + h * 0.25},${-h} H${w / 2 - h * 0.25} L${w / 2},0 Z" fill="#3A3F4A" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/><path d="M-18,${-h} q18,-40 36,0" fill="none" stroke="${ink}" stroke-width="10"/>` +
      `<text x="0" y="${f1(-h * 0.36)}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="${f1(Math.min(h * 0.32, w * 0.11))}" letter-spacing="1" fill="${C.cream}">THALIDOMIDE</text></g>`;
    const sizes = [[190, 62], [170, 56], [160, 54], [260, 100]], at = [0, 66, 126, 184];
    const stack = sizes.map(([w, h], i) => weight(w, h, lx + (i % 2 ? 6 : -4), ly - at[i])).join("");
    const topY = ly - 184 - 100;
    const op = { tone: 3, outfit: "overalls", color: 1, hat: "hard", mood: "cross", look: "right", arms: [[-150, -170], [150, 170]], build: { legPose: [[-30, -60], [30, 60]] } };
    const operator = H.at(lx, topY - 100 * 1.2 - 34, 1.2, K.person(op)) + `<path d="M${lx - 56},${topY - 24} q56,26 112,0" fill="none" stroke="${ink}" stroke-width="3" stroke-dasharray="6 8"/>`;
    // the crane on the left, its empty hook
    const crane = `<path d="M60,1080 L60,100 H700" fill="none" stroke="${C.yellow}" stroke-width="34"/><path d="M60,1080 L60,100 H700" fill="none" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M60,160 L200,100 M120,100 L60,220" stroke="${ink}" stroke-width="5"/><path d="M600,100 V220" stroke="${ink}" stroke-width="4"/><path d="M588,220 q12,30 24,0" fill="none" stroke="${ink}" stroke-width="7"/>` +
      `<rect x="20" y="460" width="160" height="140" fill="${C.yellow}" stroke="${ink}" stroke-width="5"/><rect x="40" y="480" width="80" height="60" fill="${C.cyan}" stroke="${ink}" stroke-width="3"/>`;
    // the safety net under the left pan, the protected man waving from it
    let mesh = "";
    for (let i = 0; i <= 10; i++) mesh += `<path d="M${400 + i * 34},780 L${420 + i * 30},850" stroke="${ink}" stroke-width="2"/>`;
    const net = `<path d="M380,780 Q550,880 760,780" fill="${WHITE}" fill-opacity="0.4" stroke="${ink}" stroke-width="4"/>` + mesh + `<path d="M380,780 V${ground} M760,780 V${ground}" stroke="${C.slate}" stroke-width="10"/>`;
    const prot = { tone: 1, outfit: "shirt", color: 0, hat: "hard", mood: "smile", arms: [[-150, -170], [20, 10]] };
    const wrap = `<g opacity="0.55">${[0, 1, 2, 3, 4, 5].map((i) => `<rect x="-32" y="${-60 + i * 22}" width="64" height="20" rx="8" fill="${WHITE}" stroke="${ink}" stroke-width="1.4"/>`).join("")}</g>`;
    const protMan = H.at(560, 820 - 100 * 1.1, 1.1, K.person(prot) + wrap);
    const scale = H.at(sx, ground, k, K.props.balanceScale({ tilt }));
    const svg = field(600) + num(1340, 200, 150, "3,389 : 1") + crane + net + scale + heap(H, sx, ground, k, tilt, 0.3, null) + stack + operator + protMan;
    return { svg, alt: "On the high left pan of the giant scale a tower of four iron THALIDOMIDE weights stands with the crane operator jumping on top, and the pan has not moved; the bubble-wrapped protected man waves from a safety net below it; the right pan sits down under its heap of skeletons; 3,389 : 1 in the sky." };
  },

  "main-product-dead-patients"(H, fid) {
    const { K, C } = H, ink = C.line;
    const ground = 900;
    let bricks = "";
    for (let y = 140; y < ground; y += 34) bricks += `<path d="M0,${y} H1080" stroke="#7A3F27" stroke-width="2.4"/>`;
    for (let y = 106; y < ground; y += 34) for (let x = ((y / 34) % 2) * 50; x < 1080; x += 100) bricks += `<path d="M${x},${y} v34" stroke="#7A3F27" stroke-width="2.4"/>`;
    const factory = `<rect x="-20" y="100" width="1100" height="${ground - 100}" fill="${C.rust}" stroke="${ink}" stroke-width="6"/>` + bricks +
      `<rect x="300" y="420" width="560" height="${ground - 420}" fill="#1E1B24" stroke="${ink}" stroke-width="6"/><rect x="280" y="400" width="600" height="30" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>`;
    // the SAFETY SYSTEM sign over the gate, dented in the shape of the official
    const sign = `<path d="M380,240 V100 M780,240 V100" stroke="${C.slate}" stroke-width="7" stroke-dasharray="14 6"/>` +
      `<g transform="translate(580,300) rotate(2)"><rect x="-270" y="-60" width="540" height="110" fill="${WHITE}" stroke="${ink}" stroke-width="6"/><rect x="-256" y="-48" width="512" height="86" fill="none" stroke="${C.orange}" stroke-width="2"/>` +
      `<text x="0" y="16" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="58" letter-spacing="4" fill="${ink}">SAFETY SYSTEM</text>` +
      `<path d="M-40,-60 q20,30 6,60 q30,20 8,50 M60,-60 q-14,36 10,64 q-26,16 -8,46" fill="none" stroke="#9C968A" stroke-width="3"/></g>`;
    const belt = H.at(1080, ground, 3.0, K.props.conveyor({ w: 300 }));
    const stones = [0, 1, 2, 3].map((i) => H.at(820 + i * 230, ground - 66 * 3 + 6, 1.45, K.props.headstone({ text: "" }))).join("") +
      [0, 1, 2].map((i) => H.at(1500 + i * 150, ground + 140, 1.1, K.props.headstone({ text: "" }))).join("");
    const svg = field(500) + factory + sign + belt + stones + `<rect y="${ground}" width="1920" height="180" fill="${GROUND}"/>` + [0, 1, 2].map((i) => H.at(1260 + i * 220, 1030, 1.3, K.props.headstone({ text: "" }))).join("");
    return { svg, alt: "A plain brick factory gate under the dented SAFETY SYSTEM sign; a stopped conveyor carries plain headstones out of the gate into a neat row on the ground." };
  },

  "someone-you-love"(H, fid) {
    const { K, C } = H, ink = C.line;
    const ground = 900;
    // the war factory, close on its door: the Weapons Maker backing out with the newborn missile
    const fac = H.at(1260, ground, 2.7, K.props.factory({ label: "" }));
    const wm = man(H, K.castOpts("weaponsMaker", { mood: "grin" }), 1260, ground, 2.6);
    const born = `<g stroke="${C.yellow}" stroke-width="6" stroke-linecap="round"><path d="M1120,520 l-34,-22 M1110,580 l-40,0 M1400,520 l34,-22 M1410,580 l40,0"/></g>`;
    // the warehouse to the left, its door rolled up on the shelf of bottles, one waving
    let shelf = `<rect x="-40" y="240" width="560" height="${ground - 240}" fill="#9C968A" stroke="${ink}" stroke-width="6"/><rect x="30" y="330" width="440" height="${ground - 330}" fill="#2E2A36" stroke="${ink}" stroke-width="5"/>`;
    for (const y of [470, 650, 830]) shelf += `<rect x="50" y="${y}" width="400" height="14" fill="${C.tan}" stroke="${ink}" stroke-width="3"/>`;
    [[100, 470], [190, 470], [280, 470], [370, 470], [100, 650], [280, 650], [370, 650], [100, 830], [190, 830], [370, 830]].forEach(([x, y]) => { shelf += H.at(x, y, 1.0, K.props.pillBottle({ label: "" })); });
    shelf += H.at(190, 650, 1.1, K.props.pillBottle({ face: "eager", label: "" })) + `<path d="M160,566 l-28,-36 M220,566 l28,-36" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>` +
      H.at(214, 594, 1.25, K.props.priceTag({ text: "NEVER TESTED FOR THIS", angle: 14 })) + `<path d="M146,530 q34,-32 88,0" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.8"/>`;
    const svg = field(520) + shelf + fac + wm + born + `<rect y="${ground}" width="1920" height="180" fill="#B09363"/>`;
    return { svg, alt: "The Weapons Maker stands in the war factory's door under its missile chimneys, cradling a newborn smiling missile like a baby and beaming; next door, through the warehouse's open door, a dusty bottle tagged NEVER TESTED FOR THIS waves from its shelf." };
  },

  "child-scientist"(H, fid) {
    const { K, C } = H, ink = C.line;
    const ground = 880;
    // the little house behind its picket fence, blackened where the fireball hit; the picture drained gray
    const house = H.at(1560, ground - 230, 1.1, K.burn(K.props.house({ variant: 2, smoke: false })));
    let fence = "";
    for (let x = 0; x < 1920; x += 80) fence += `<path d="M${x},${ground - 30} V${ground - 300} L${x + 25},${ground - 334} L${x + 50},${ground - 300} V${ground - 30} Z" fill="${WHITE}" stroke="${ink}" stroke-width="4"/>`;
    fence += `<rect y="${ground - 250}" width="1920" height="24" fill="${WHITE}" stroke="${ink}" stroke-width="4"/><rect y="${ground - 120}" width="1920" height="24" fill="${WHITE}" stroke="${ink}" stroke-width="4"/>`;
    const scorch = `<ellipse cx="820" cy="${ground - 150}" rx="560" ry="260" fill="#2B2420" opacity="0.5"/><ellipse cx="820" cy="${ground}" rx="460" ry="56" fill="#2B2420" opacity="0.6"/>`;
    // the bare pin where her drawing was, one black curl of it left
    const pin = `<path d="M540,${ground - 300} l-44,46 l20,18 l10,-22 l24,-10 l-6,18 l22,-14 Z" fill="#1A1512" stroke="#3A302A" stroke-width="2"/><circle cx="540" cy="${ground - 300}" r="14" fill="${C.war}" stroke="${ink}" stroke-width="4"/>`;
    // the girl's small skeleton in her bun and glasses, still holding up the toy flask
    const girl = { tone: 3, outfit: "labcoat", hair: 1, hairStyle: "bun", glasses: true, look: "right", arms: [[10, 6], [130, 160]], build: { hs: 1.3, legs: 0.62, th: 0.72, tw: 0.8, neck: 0.4 } };
    const R = K.rig(girl), k = 3.4;
    const bun = `<circle cx="-8" cy="-27" r="9" fill="${BONE}" stroke="${ink}" stroke-width="2.4"/><g fill="none" stroke="${ink}" stroke-width="2.4"><circle cx="-4" cy="-3" r="6.5"/><circle cx="10" cy="-3" r="6.5"/><path d="M2.5,-3 h1"/></g>`;
    const flask = `<g transform="translate(${f1(R.hand[1][0])},${f1(R.hand[1][1] - 6)})"><path d="M-4,-26 H4 V-14 L14,6 H-14 L-4,-14 Z" fill="${WHITE}" stroke="${ink}" stroke-width="2.6"/><path d="M-10,-2 H10 L13,5 H-13 Z" fill="${C.med}"/></g>`;
    const skel = H.at(860, ground - 100 * k, k, K.person({ ...girl, skeleton: true }).replace("<!--face-end-->", bun + "<!--face-end-->") + flask);
    const svg = field(380, "#DCD8CE", "#A9A69B") + house + fence + scorch + pin + skel + smoke(1180, ground - 300, 2.2, "#5A5550") + smoke(560, ground - 360, 1.4, "#5A5550");
    return { svg, alt: "In a scorched yard by a picket fence, the girl is a small grinning skeleton in her bun and big glasses, still holding up her toy flask of teal; on the fence beside her only a pin and a black scrap are left of her drawing; smoke rises." };
  },

  "murder-receipt"(H, fid) {
    const { K, C } = H, ink = C.line;
    const counterY = 700;
    // the politician behind the counter, one finger still on the register's key
    const PO = K.castOpts("politician", { look: "right", mood: "grin", arms: [[10, 6], [50, 80]] }), RP = K.rig(PO), pk = 2.6;
    const pol = H.at(640 - pk * RP.hand[1][0], 610 - pk * RP.hand[1][1], pk, K.person(PO));
    const register = `<g transform="translate(760,${counterY})"><path d="M-200,0 L-180,-220 H180 L200,0 Z" fill="#B9B5AE" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
      [0, 1, 2].map((r) => [0, 1, 2, 3, 4].map((c) => `<rect x="${-150 + c * 60}" y="${-170 + r * 46}" width="40" height="32" rx="6" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>`).join("")).join("") +
      `<rect x="-120" y="-320" width="240" height="100" fill="#8C8782" stroke="${ink}" stroke-width="5"/><rect x="-96" y="-300" width="192" height="56" fill="#1E1B24" stroke="${ink}" stroke-width="3"/>` +
      `<text x="0" y="-258" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="36" fill="${C.yellow}">$$$</text></g>`;
    const counter = `<rect x="-20" y="${counterY}" width="1960" height="40" fill="${C.rust}" stroke="${ink}" stroke-width="6"/><rect x="-20" y="${counterY + 40}" width="1960" height="400" fill="${C.tan}" stroke="${ink}" stroke-width="6"/>`;
    // the long receipt from the register's slot into YOU's hands, the last line just printed
    const lines = ["WAR ...... $170,000,000,000,000", "CLINICAL TRIALS ...... $0.00", "TREATMENT ...... VOID", "SCIENTIST ...... VOID", "INFLATION ...... $$$", "TAX BILL ...... $$$", "HER MURDER ...... PAID"];
    // the receipt runs out of the register's slot, up over a long loop, down to YOU's hands; he holds it up to read
    const YO = { ...YOU, look: "left", mood: "sad", arms: [[-60, -100], [-50, -90]] }, RY = K.rig(YO), yk = 3.0, yx = 1700, yy = 1240 - 100 * yk;
    const hx = yx + yk * RY.hand[0][0], hy = yy + yk * RY.hand[0][1];
    const top = 120, left = hx - 420, w = 400, bot = hy + 10;
    let zig = "";
    for (let x = left + w; x > left; x -= 20) zig += ` L${f1(x - 10)},${f1(bot + 10)} L${f1(x - 20)},${f1(bot)}`;
    const receipt = `<path d="M${760},${counterY - 320} C${760},${top - 40} ${left - 60},${top - 60} ${left},${top + 6}" fill="none" stroke="${ink}" stroke-width="44"/><path d="M${760},${counterY - 320} C${760},${top - 40} ${left - 60},${top - 60} ${left},${top + 6}" fill="none" stroke="${WHITE}" stroke-width="38"/>` +
      `<path d="M${left},${top} H${left + w} V${bot}${zig} Z" fill="${WHITE}" stroke="${ink}" stroke-width="4"/>` +
      lines.map((l, i) => `<text x="${left + 22}" y="${top + 60 + i * ((bot - top - 70) / 6.4)}" font-family="Oswald" font-weight="600" font-size="${i < 2 ? 22 : 30}" fill="${i === 6 ? C.war : ink}" opacity="${i < 2 ? 0.55 : 1}">${l}</text>`).join("");
    const you = H.at(yx, yy, yk, K.person(YO));
    const svg = `<rect width="1920" height="1080" fill="#D9C08E"/>` + pol + counter + register + receipt + you;
    return { svg, alt: "At a shop counter the grinning politician has just rung up YOU at a chrome cash register; YOU holds the long receipt, its old lines WAR and CLINICAL TRIALS $0.00 at the top and the new ones under them, the last in red: HER MURDER ...... PAID; his smile is gone." };
  },

  "suboptimal-stamp"(H, fid) {
    const { K, C } = H, S = K.STUDIO;
    const front = lecternProps(H, 2) + H.at(S.lect[0] - S.lect[1] / 2 + 92, S.top - 150, 1.3, K.props.stamp({ text: "SUBOPTIMAL" })) + H.at(1440, 330, 1.2, detector(H, true));
    const svg = H.host("smirk-closed", "palms-down", front);
    return { svg, alt: "Wishonia at her lectern smirks at the camera, palms down; the rubber stamp just lifted off the Earth case file propped on the lectern, its new red SUBOPTIMAL under MAY BE ELIGIBLE FOR OPTIMIZATION; her mug set down; the charred detector on the wall." };
  },

  "good-bad-weird-news"(H, fid) {
    const { K, C } = H, S = K.STUDIO, ink = C.line;
    const rich = { ...YOU, hat: "top", prop: "monocle", mood: "greedy", look: "left", arms: [[-110, -150], [110, 150]] };
    const you = man(H, rich, 1480, 1066, 3.0);
    const bowler = `<g transform="translate(1720,560) rotate(28) scale(3)"><path d="M-17,1 L-13,-16 L0,-21 L13,-16 L17,1 Z" fill="${ink}"/><path d="M-28,4 L-22,-1 H22 L28,4 Z" fill="${ink}"/></g>`;
    const papers = [[1250, 560, 20], [1300, 700, -30], [1660, 660, 40], [1740, 780, -10], [1230, 820, -50], [1700, 920, 25], [1330, 480, 60], [1620, 470, -20], [1180, 680, -40]].map(([x, y, r]) => bill(H, "med", x, y, 1.1, 0, r)).join("");
    const clip = `<g transform="translate(1270,1010) rotate(-80) scale(1.3)">${K.props.clipboard({ title: "TO DO", items: ["", "", ""] })}</g>`;
    const wrench = `<g transform="translate(${S.lect[0] + 150},${S.top - 140}) rotate(40)"><path d="M-7,0 V-70 H7 V0 Z M-20,-70 a22,22 0 1,1 40,0 l-10,-4 v-18 h-20 v18 Z" fill="#8C8782" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/></g>`;
    const book = `<g transform="translate(${S.lect[0] + 50},${S.top + 4}) scale(1.4)">${K.props.manual({})}</g>` + wrench;
    const front = lecternProps(H, 2) + book + H.at(1440, 330, 1.2, detector(H, true)) + clip + you + bowler + papers;
    const svg = H.host("happy-smile", "presenting", front);
    return { svg, alt: "Wishonia presents YOU with both hands: beside her lectern he stands in a top hat and monocle with dollar-sign eyes under a rain of medicine papers, his bowler falling away; the book stands open on the lectern with a wrench popping out; the charred detector on the wall above him." };
  },
};
