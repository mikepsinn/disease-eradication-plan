// Sketches for storyboards/part-22-how-this-manual-could-fix-everything.md: each scene's key moment on a 1920 x 1080
// frame (16:9), in the film look (Part 2 is the reference). Host shots use H.host (KIT.STUDIO, 16:9: the lectern's
// reading top at y 790, x 540 to 980). Plates are drawn as the camera sees them at that moment, in the plate units of
// the storyboard's Build section (the ground at y 0, everyone at scale 1.5). Captions keep-out: below y 900.

const f = (n) => n.toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});
const SKY = "#EFE6C8", FIELD = "#C8B07B", FIELD2 = "#B79C66", WALL = "#F3ECD8", CHAR = "#2C241E", CHAR2 = "#45382C", SMOKE = "#8C8782";
const TEAR = "#9CCFE0";

// A plate framing as KIT.camera places it: plate point (x, y) in the middle of the frame, at scale s.
const view = (x, y, s, inner) => `<g transform="translate(${f(960 - x * s)},${f(540 - y * s)}) scale(${s})">${inner}</g>`;
// A host shot's slow push in on her face (KIT.studio), k of the way along.
const push = (S, k, inner) => `<g transform="translate(${S.face[0]},${S.face[1]}) scale(${k}) translate(${-S.face[0]},${-S.face[1]})">${inner}</g>`;
const at = (x, y, k, inner, rot = 0) => `<g transform="translate(${f(x)},${f(y)})${rot ? ` rotate(${rot})` : ""}${k !== 1 ? ` scale(${k})` : ""}">${inner}</g>`;
// The plate's field: the cream sky over the tan ground (y 0 down).
const field = () => `<rect x="-6000" y="-6000" width="12000" height="6000" fill="${SKY}"/><rect x="-6000" y="0" width="12000" height="3000" fill="${FIELD}"/>` +
  `<path d="M-6000,0 H6000" stroke="${FIELD2}" stroke-width="6"/>`;

// Oswald capitals.
function osw(x, y, size, text, fill, anchor = "middle", extra = "") {
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Oswald" font-weight="600" font-size="${size}" letter-spacing="${(size * 0.06).toFixed(1)}" fill="${fill}" ${extra}>${text}</text>`;
}
// Smoke wisps rising from (x, y), n of them, s tall.
function smoke(x, y, n, s, col = SMOKE, w = 4) {
  let d = "";
  for (let i = 0; i < n; i++) {
    const x0 = x + (i - (n - 1) / 2) * s * 0.42;
    d += `M${f(x0)},${f(y)} q${f(-s * 0.18)},${f(-s * 0.25)} 0,${f(-s * 0.5)} q${f(s * 0.18)},${f(-s * 0.25)} 0,${f(-s * 0.5)} `;
  }
  return `<path d="${d}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" opacity="0.85"/>`;
}
// Wishonia's coffee mug, standing on (x, y) (as Part 16 draws it): rust, a cream band, a handle on the left.
function mug(x, y, C, rot = 0) {
  return `<g transform="translate(${x},${y}) rotate(${rot})">` +
    `<path d="M-46,-62 q-26,0 -26,24 q0,24 26,24" fill="none" stroke="${C.ink}" stroke-width="13"/><path d="M-46,-62 q-26,0 -26,24 q0,24 26,24" fill="none" stroke="${C.rust}" stroke-width="7"/>` +
    `<path d="M-46,-78 H34 L30,0 H-42 Z" fill="${C.rust}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="round"/>` +
    `<rect x="-44" y="-56" width="76" height="14" fill="${C.cream}"/><path d="M-44,-56 H32 M-44,-42 H32" stroke="${C.ink}" stroke-width="2.5"/>` +
    `<ellipse cx="-6" cy="-78" rx="40" ry="7" fill="#3A2416" stroke="${C.ink}" stroke-width="4"/></g>`;
}
// The manual with its cover swung back past the spine (the storyboard's open position, scaleX -0.35 about (-42, -59)).
function openManual(K, C, sx = -0.45) {
  const m = K.props.manual({ size: 1 }), i = m.indexOf('<g class="manual-cover">');
  const cover = m.slice(i).replace(/<text[^>]*>[^<]*<\/text>/g, "").replace('<g class="manual-cover">', `<g class="manual-cover" transform="translate(-42,0) scale(${sx},1) translate(42,0)">`);
  const print = [-104, -94, -84, -74, -64, -54, -44, -34].map((y, j) => `<path d="M-32,${y} H${j % 3 === 2 ? 14 : 30}" stroke="${C.peri}" stroke-width="2.2" opacity="0.6"/>`).join("");
  return m.slice(0, i).replace(/<\/g>$/, "") + print + cover;
}
// An open tray (the Build): the cream back wall, then `inner` (the actors, standing on the floor), then the orange
// front panel 90 tall. x0: its left edge; fl: its floor; w: its width. soot: smudge the panel (tray 4 after the boom).
function tray(C, x0, fl, w, inner, soot = false) {
  const ink = C.line;
  const back = `<rect x="${x0 + 10}" y="${fl - 150}" width="${w - 20}" height="150" fill="${WALL}" stroke="${ink}" stroke-width="5"/>` +
    `<path d="M${x0 + 10},${fl - 150} L${x0},${fl - 140} V${fl} M${x0 + w - 10},${fl - 150} L${x0 + w},${fl - 140} V${fl}" fill="none" stroke="${ink}" stroke-width="5"/>`;
  const rivets = [x0 + 22, x0 + w - 22].map((x) => `<circle cx="${x}" cy="${fl - 45}" r="6" fill="${C.cream}" stroke="${ink}" stroke-width="2.5"/>`).join("");
  const front = `<rect x="${x0}" y="${fl - 90}" width="${w}" height="90" fill="${C.orange}" stroke="${ink}" stroke-width="5"/>` +
    `<path d="M${x0 + 8},${fl - 80} H${x0 + w - 8}" stroke="${C.cream}" stroke-width="4"/>` +
    `<path d="M${x0 + w - 14},${fl - 70} V${fl - 8}" stroke="${C.rust}" stroke-width="5"/>` + rivets +
    (soot ? [0.18, 0.46, 0.71].map((u, i) => `<path d="M${f(x0 + w * u)},${fl - 90} q${12 + i * 6},30 ${-6 + i * 4},62 q-14,-28 ${-28 - i * 5},-62 Z" fill="${CHAR}" opacity="0.7"/>`).join("") : "");
  return `<g>${back}${inner}${front}</g>`;
}
// A pair of slate folding arms (a scissor X) from tray a's right end to tray b's left end.
function arms(C, ax, afl, bx, bfl) {
  const bar = (x1, y1, x2, y2) => `<path d="M${x1},${y1} L${x2},${y2}" stroke="${C.line}" stroke-width="20" stroke-linecap="round"/><path d="M${x1},${y1} L${x2},${y2}" stroke="${C.slate}" stroke-width="12" stroke-linecap="round"/>`;
  const mx = (ax + bx) / 2, my = (afl - 40 + bfl - 40) / 2;
  return bar(ax - 50, afl - 20, bx + 50, bfl - 70) + bar(ax - 50, afl - 70, bx + 50, bfl - 20) + `<circle cx="${f(mx)}" cy="${f(my)}" r="9" fill="${C.cream}" stroke="${C.line}" stroke-width="3"/>`;
}
// One of tray 4's order cards on stick legs, its feet at (0, 0): a cream card 90 x 120 with a numeral and a face.
// charred: burnt black and smoking, only the white eyes left.
function card(C, n, charred = false) {
  const ink = C.line, body = charred ? CHAR : "#F6EEDA";
  const legs = `<path d="M-18,-6 L-20,-74 M18,-6 L20,-74" stroke="${ink}" stroke-width="7" stroke-linecap="round"/><path d="M-20,-4 h-14 M20,-4 h14" stroke="${ink}" stroke-width="7" stroke-linecap="round"/>`;
  const edge = charred ? `M-45,-194 l8,-8 l9,8 l10,-9 l9,9 l11,-8 l9,8 l10,-9 l9,9 l15,-4 V-74 H-45 Z` : `M-45,-194 H45 V-74 H-45 Z`;
  const eyes = [-17, 17].map((x) => `<g class="eye"><path d="M${x - 11},-150 Q${x},-164 ${x + 11},-150 Q${x},-138 ${x - 11},-150 Z" fill="#FFFFFF" stroke="${ink}" stroke-width="2"/><circle cx="${x + 1}" cy="-150" r="4.2" fill="${ink}"/></g>`).join("");
  const mouth = charred ? "" : `<path d="M-14,-128 Q0,-117 14,-128" fill="none" stroke="${ink}" stroke-width="3.5" stroke-linecap="round"/>`;
  const num = `<text x="0" y="-84" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="44" fill="${charred ? "#B8A68C" : C.navy}">${n}</text>`;
  return legs + `<path d="${edge}" fill="${body}" stroke="${ink}" stroke-width="4.5" stroke-linejoin="round"/>` + eyes + mouth + num + (charred ? smoke(0, -204, 3, 70, SMOKE, 5) : "");
}

export default {
  "how-this-manual-could-fix-everything-title"(H, fid) {
    const { K, C } = H;
    // KIT.titleScene's atomic card (16:9): the emblem at (960, 300), rx 200, ry 62, papers at 0.62, as at t 3 s
    const cx = 960, cy = 300, rx = 200, ry = 62, TILT = [0, 60, -60], t = 3.0;
    const orbits = TILT.map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = TILT.map((a, i) => {
      const th = i * 2.1 + t * 2.4, ar = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return at(cx + ex * Math.cos(ar) - ey * Math.sin(ar), cy + ex * Math.sin(ar) + ey * Math.cos(ar) - 6, 0.62, K.money("war", i % 2));
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    // the heading: Fraunces, cream with a cream outline and a navy drop shadow
    const word = (x, y, s, text, extra = "") => {
      const t0 = (dx, dy, more) => `<text x="${x + dx}" y="${y + dy}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${s}" ${more}>${H.esc(text)}</text>`;
      return `<g ${extra}>` + t0(0.04 * s, 0.053 * s, `fill="${C.ink}"`) + t0(0, 0, `fill="${C.cream}" stroke="${C.cream}" stroke-width="${f(0.044 * s)}" stroke-linejoin="round" style="paint-order:stroke"`) + "</g>";
    };
    // EVERYTHING, cranked crooked (about 1480 wide at 200: x 220 to 1700, caps y 693 to 833)
    const every = word(960, 833, 200, "EVERYTHING", `transform="rotate(-4.5 960 763)"`);
    // the chrome wrench swinging away from the word's right end: an open jaw at (0, 0), the handle out to the right
    const ink = C.line, CHROME = "#C9CED6", CHROME2 = "#8E96A3";
    const wrench = at(1712, 690, 1, `<g transform="rotate(-38)">` +
      `<path d="M30,-20 C12,-52 -40,-58 -62,-34 L-30,-14 L-34,14 L-62,34 C-40,58 12,52 30,20 L52,14 H330 L350,30 Q400,40 412,0 Q400,-40 350,-30 L330,-14 H52 Z" fill="${CHROME}" stroke="${ink}" stroke-width="6" stroke-linejoin="round"/>` +
      `<circle cx="378" cy="0" r="17" fill="${C.navy}" stroke="${ink}" stroke-width="5"/><path d="M40,-6 H310" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.8"/><path d="M40,8 H310" stroke="${CHROME2}" stroke-width="5" stroke-linecap="round"/></g>`);
    // the loose bolt bouncing off the bottom of the card, with its bounce arcs
    const bolt = at(1370, 880, 1, `<g transform="rotate(30)"><rect x="-10" y="-34" width="20" height="40" fill="${CHROME}" stroke="${ink}" stroke-width="4"/><path d="M-10,-26 H10 M-10,-16 H10 M-10,-6 H10" stroke="${CHROME2}" stroke-width="3"/>` +
      `<path d="M-22,6 H22 L26,22 H-26 Z" fill="${CHROME}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/></g>`) +
      `<path d="M1560,830 Q1500,770 1440,860 M1440,870 Q1405,820 1385,880" fill="none" stroke="${C.cream}" stroke-width="4" stroke-dasharray="4 12" stroke-linecap="round" opacity="0.7"/>`;
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus + word(960, 630, 86, "HOW THIS MANUAL COULD FIX") + every + wrench + bolt;
    return { svg, alt: "The period title card: the film's atom with its running papers over HOW THIS MANUAL COULD FIX EVERYTHING in cream; EVERYTHING sits tilted crooked, a big chrome wrench swings away from its end, and a loose bolt bounces off the bottom of the card." };
  },

  "manual-contains"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "contains:": the manual open on the right end of the lectern (size 1.6 at (935, 790)), four little trays
    // on folding arms stair-stepping up to the right past her antennae, the mug still rocking
    const MX = 935, MY = 790, k = 1.6;
    const pageTop = MY - 118 * k;
    const T = [[1010, 660], [1185, 520], [1360, 380], [1535, 240]], TW = 150;
    const mini = (x0, fl, inner) => `<rect x="${x0 + 4}" y="${fl - 34}" width="${TW - 8}" height="34" fill="${WALL}" stroke="${ink}" stroke-width="3"/>` + inner +
      `<rect x="${x0}" y="${fl - 20}" width="${TW}" height="20" fill="${C.orange}" stroke="${ink}" stroke-width="3.5"/><path d="M${x0 + 4},${fl - 16} H${x0 + TW - 4}" stroke="${C.cream}" stroke-width="2"/>`;
    const bar = (x1, y1, x2, y2) => `<path d="M${x1},${y1} L${x2},${y2}" stroke="${ink}" stroke-width="9" stroke-linecap="round"/><path d="M${x1},${y1} L${x2},${y2}" stroke="${C.slate}" stroke-width="5" stroke-linecap="round"/>`;
    let arm = bar(MX + 40, pageTop + 30, T[0][0] + 30, T[0][1] - 6) + bar(MX + 40, pageTop + 6, T[0][0] + 30, T[0][1] - 18);
    for (let i = 0; i < 3; i++) arm += bar(T[i][0] + TW - 20, T[i][1] - 4, T[i + 1][0] + 20, T[i + 1][1] - 16) + bar(T[i][0] + TW - 20, T[i][1] - 16, T[i + 1][0] + 20, T[i + 1][1] - 4);
    // what is in them, tiny: the picture book and the bed, a plus, three stacks, five cards
    const c1 = `<rect x="${T[0][0] + 22}" y="${T[0][1] - 44}" width="40" height="26" fill="${C.cream}" stroke="${ink}" stroke-width="2.5"/><path d="M${T[0][0] + 42},${T[0][1] - 44} V${T[0][1] - 18}" stroke="${ink}" stroke-width="2"/>` +
      `<rect x="${T[0][0] + 80}" y="${T[0][1] - 34}" width="52" height="16" fill="#FFFFFF" stroke="${ink}" stroke-width="2.5"/>`;
    const c2 = `<path d="M${T[1][0] + 60},${T[1][1] - 52} V${T[1][1] - 16} M${T[1][0] + 42},${T[1][1] - 34} H${T[1][0] + 78}" stroke="${C.orange}" stroke-width="10"/>` +
      `<rect x="${T[1][0] + 96}" y="${T[1][1] - 44}" width="26" height="28" fill="${C.tan}" stroke="${ink}" stroke-width="2.5"/>`;
    const c3 = [0, 1, 2].map((i) => `<rect x="${T[2][0] + 20 + i * 42}" y="${T[2][1] - 20 - (3 - i) * 12}" width="30" height="${(3 - i) * 12}" fill="${C.money}" stroke="${ink}" stroke-width="2.2"/>`).join("");
    const c4 = [0, 1, 2, 3, 4].map((i) => `<rect x="${T[3][0] + 12 + i * 27}" y="${T[3][1] - 46}" width="20" height="28" fill="#F6EEDA" stroke="${ink}" stroke-width="2.2"/>`).join("");
    const trays = mini(T[0][0], T[0][1], c1) + mini(T[1][0], T[1][1], c2) + mini(T[2][0], T[2][1], c3) + mini(T[3][0], T[3][1], c4);
    const wobble = `<path d="M${T[3][0] + TW + 14},${T[3][1] - 40} q10,-8 0,-16 M${T[3][0] + TW + 26},${T[3][1] - 46} q12,-10 0,-20" fill="none" stroke="${ink}" stroke-width="3.5" stroke-linecap="round"/>`;
    const rock = `<path d="M560,700 q-10,-10 0,-20 M548,716 q-14,-12 0,-26" fill="none" stroke="${ink}" stroke-width="3.5" stroke-linecap="round"/>`;
    const front = mug(610, 790, C, -7) + rock + arm + trays + wobble + at(MX, MY, k, openManual(K, C));
    const svg = push(K.STUDIO, 1.02, H.host("lookright-oh", "presenting", front));
    return { svg, alt: "Wishonia at her lectern looks over at the manual on its right end: its orange cover has sprung open and four little trays on folding arms stair-step out of it up to the right, the top one higher than her antennae, while her mug rocks." };
  },

  "manual-toolbox"(H, fid) {
    const { K, C } = H;
    // after "important).": framed on tray 4 (x 1580 to 2340, floor y -1120) at scale 1.55: the mushroom cloud
    // thinning over it, the five cards charred and blinking, 4 and 3 still swapped; tray 3's right end with the
    // Lobbyist and the $12.50 stack below left
    const x3 = 780, fl3 = -920, x4 = 1580, fl4 = -1120, W = 760;
    const t3 = tray(C, x3, fl3, W, "");
    const order = [1, 2, 4, 3, 5];
    const cards = order.map((n, i) => at(x4 + 100 + i * 140, fl4 - 60, 1, card(C, n, true))).join("");
    const t4 = tray(C, x4, fl4, W, cards, true);
    const cloud = `<g opacity="0.82">${at(x4 + W / 2, fl4 - 150, 0.62, K.nuke())}</g>`;
    const debris = [[1700, -1500, 20], [2250, -1460, -30], [2420, -1300, 50], [1620, -1380, -15]].map(([x, y, r]) =>
      `<rect x="${x}" y="${y}" width="22" height="14" fill="${CHAR}" transform="rotate(${r} ${x} ${y})"/>`).join("");
    const plate = field() + arms(C, x3 + W, fl3, x4, fl4) + t3 + cloud + t4 + debris;
    const svg = `<rect width="1920" height="1080" fill="${SKY}"/>` + view(1985, -1320, 1.55, plate);
    return { svg, alt: "Tray 4 at the top of the stair under a thinning mushroom cloud: five cards on stick legs stand there charred black and smoking, only their white eyes showing, numbered 1, 2, 4, 3, 5; below left, tray 3's end the stair going on down to the left." };
  },

  "not-a-bribe-label-maker"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "governing).": the Optimitron station of the drawer (x 700): the Optimitron (size 1.1) on its lift, both
    // dials swung to the top, CURE IT popped up into the chin of the Politician, who hugs it from behind sobbing two
    // fountains; the burnt MORE WAR card smoking on the drawer's rim
    const ox = 700, lift = -95, ks = 0.95;
    const opt = at(ox, lift, ks, K.props.optimitron({ mood: "flat", health: 128, wealth: 128, card: "CURE IT", pop: 76 }));
    const cardTop = lift + (-178 - 6 - 76) * ks, cardX = ox + 12 * ks;
    // his arms draped over its top corners (his hands round its sides)
    const PO = K.castOpts("politician", { mood: "sad", arms: [[-42, -36], [42, 36]], holdR: null, build: { armL: 1.5 } });
    const R = K.rig(PO), k = 1.5, px = cardX - R.mouth[0] * k, py0 = cardTop - 30 - R.mouth[1] * k;
    const pol = at(px, py0, k, K.person(PO));
    // the tears: two fountains arcing off both eyes
    const ex = px + R.eyes[0] * k, ey = py0 + R.eyes[1] * k;
    let tears = "";
    for (const s of [-1, 1]) {
      for (let i = 0; i < 6; i++) {
        const u = (i + 1) / 6, tx = ex + s * (20 + 150 * u), ty = ey - 70 * Math.sin(Math.PI * u * 0.8) + 120 * u * u;
        tears += `<path d="M${f(tx)},${f(ty - 9)} q7,9 0,14 q-7,-5 0,-14 Z" fill="${TEAR}" stroke="${ink}" stroke-width="2"/>`;
      }
      tears += `<path d="M${f(ex + s * 6)},${f(ey)} Q${f(ex + s * 90)},${f(ey - 90)} ${f(ex + s * 170)},${f(ey + 110)}" fill="none" stroke="${TEAR}" stroke-width="4" stroke-linecap="round" opacity="0.75"/>`;
    }
    // the toast pop: speed lines under the card
    const popLines = `<path d="M${f(cardX - 46)},${f(cardTop + 40)} v-26 M${f(cardX + 46)},${f(cardTop + 40)} v-26 M${f(cardX - 40)},${f(cardTop - 14)} l-16,-10 M${f(cardX + 40)},${f(cardTop - 14)} l16,-10 M${f(cardX)},${f(cardTop - 4)} v0" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`;
    const liftSvg = `<rect x="${ox - 150}" y="${lift}" width="300" height="16" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>`;
    // the burnt MORE WAR card hanging over the drawer's rim
    const burnt = at(470, -92, 1, `<g transform="rotate(-14)"><rect x="-40" y="-8" width="80" height="58" fill="${CHAR}" stroke="${ink}" stroke-width="3.5"/>` +
      `${osw(0, 14, 17, "MORE WAR", "#7A3426")}<path d="M-40,40 l10,-8 l8,9 l10,-8 l9,9 l10,-9 l8,8 l10,-8 l15,8" fill="none" stroke="${SMOKE}" stroke-width="2"/></g>` + smoke(0, -16, 3, 70));
    const inner = liftSvg + pol + opt + tears + popLines;
    const plate = field() + tray(C, -906, 0, 3506, inner) + burnt;
    const svg = `<rect width="1920" height="1080" fill="${SKY}"/>` + view(700, -245, 1.62, plate);
    return { svg, alt: "In the manual's long bottom drawer, the Politician hugs the Optimitron from behind, sobbing two fountains of tears, as a CURE IT card pops up out of its toaster slot into his chin; both its dials are swung to the top and its face stays flat; a burnt MORE WAR card smokes on the drawer's rim." };
  },

  "dysfunction-engine"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "it.": pushed in on the Rich Human sprinting on the treadmill (belt top y -40), dollar eyes, holding his own
    // top hat out upside down under the payout slot on the treadmill's front post: one medicine paper drops in per turn
    // of the belt, and the hat is heaped. His cigar is freshly lit; the burning PLEASE BE GOOD sign he lit it off
    // tumbles away over his shoulder.
    const belt = -40, k = 1.5, rx = -60, ry0 = belt - 100 * k;
    // the back arm still up from the toss, the front arm holding the hat out by its brim
    const RH = K.castOpts("richHuman", { mood: "greedy", look: "right", hat: null, arms: [[192, 222], [42, 84]] }), R = K.rig(RH);
    const P = (p) => [rx + p[0] * k, ry0 + p[1] * k];
    const rich = at(rx, ry0, k, K.person(RH));
    // the I PREFER LIVING button on his front
    const btn = at(rx - 22 * k, ry0 + 14 * k, 1, `<circle r="20" fill="${C.cream}" stroke="${ink}" stroke-width="3.5"/><circle r="15" fill="none" stroke="${C.med}" stroke-width="2.5"/>` +
      `<text y="-2" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="7.5" fill="${ink}">I PREFER</text><text y="7" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="7.5" fill="${ink}">LIVING</text>`);
    // the top hat, upside down: its brim at his hand, the crown hanging under it, medicine papers heaped in its mouth
    const hd = P(R.hand[1]), hw = 58, hh = 70, hx = hd[0] + 22, hy = hd[1] - 2, bw = hw / 2 + 17;
    const heap = [[-16, -6, -28, 0], [15, -10, 22, 1], [-1, -20, -8, 0], [19, -2, 40, 1], [-21, 0, -46, 1]]
      .map(([dx, dy, r, l]) => at(hx + dx, hy + dy, 0.42, `<g transform="rotate(${r})">${K.money("med", l)}</g>`)).join("");
    const topHat = `<ellipse cx="${f(hx)}" cy="${f(hy)}" rx="${f(bw)}" ry="10" fill="${ink}"/><ellipse cx="${f(hx)}" cy="${f(hy)}" rx="${f(hw / 2 - 2)}" ry="6" fill="#0B1222"/>` + heap +
      `<path d="M${f(hx - hw / 2)},${f(hy + 2)} V${f(hy + hh)} H${f(hx + hw / 2)} V${f(hy + 2)} Z" fill="${ink}"/><rect x="${f(hx - hw / 2)}" y="${f(hy + 12)}" width="${hw}" height="10" fill="${C.orange}"/>` +
      `<path d="M${f(hx + hw / 2 - 9)},${f(hy + 28)} V${f(hy + hh - 8)}" stroke="${C.slate}" stroke-width="5" stroke-linecap="round"/>` +
      `<path d="M${f(hx - bw)},${f(hy)} A${f(bw)},10 0 0 0 ${f(hx + bw)},${f(hy)}" fill="${ink}" stroke="${ink}" stroke-width="3"/>`;
    // the payout slot: a slate box on the treadmill's front post, a paper half out of its slot, one more dropping
    const px0 = hx + 62, py0 = hy - 150;
    const payout = `<path d="M${f(px0 + 44)},${f(py0 + 64)} V-8" stroke="${ink}" stroke-width="16" stroke-linecap="round"/><path d="M${f(px0 + 44)},${f(py0 + 64)} V-8" stroke="${C.slate}" stroke-width="9" stroke-linecap="round"/>` +
      `<rect x="${f(px0)}" y="${f(py0)}" width="90" height="70" rx="6" fill="${C.slate}" stroke="${ink}" stroke-width="5"/><rect x="${f(px0 + 12)}" y="${f(py0 + 10)}" width="66" height="10" rx="3" fill="${C.peri}" stroke="${ink}" stroke-width="2.5"/>` +
      `<rect x="${f(px0 - 12)}" y="${f(py0 + 40)}" width="16" height="24" fill="${ink}"/>` +
      at(px0 - 14, py0 + 52, 0.4, `<g transform="rotate(8)">${K.money("med", 0)}</g>`) +
      `<path d="M${f(px0 - 34)},${f(py0 + 70)} Q${f(hx + 40)},${f(py0 + 80)} ${f(hx + 20)},${f(hy - 30)}" fill="none" stroke="${ink}" stroke-width="3.5" stroke-dasharray="3 11" stroke-linecap="round" opacity="0.7"/>` +
      at(hx + 16, hy - 60, 0.42, `<g transform="rotate(-50)">${K.money("med", 1)}</g>`);
    // the cigar, freshly lit: an ember at its tip and a puff
    const c = P([29, -6.5]);
    const lit = `<circle cx="${f(c[0])}" cy="${f(c[1])}" r="6" fill="${C.orange}" stroke="${ink}" stroke-width="2.5"/><circle cx="${f(c[0] + 1)}" cy="${f(c[1] - 1)}" r="2.6" fill="${C.yellow}"/>` + smoke(c[0] + 8, c[1] - 10, 2, 56);
    // the sign tossed over his shoulder, tumbling away behind him, its card on fire
    const sx0 = -210, sy0 = -300, sr = -55, sk = 0.62, rad = (sr * Math.PI) / 180;
    const W2 = (14 * 26 * 0.56 + 64) / 2;
    const S = (x, y) => [sx0 + sk * (x * Math.cos(rad) - y * Math.sin(rad)), sy0 + sk * (x * Math.sin(rad) + y * Math.cos(rad))];
    const sign = at(sx0, sy0, sk, `<g transform="rotate(${sr})">${K.props.sign({ text: "PLEASE BE GOOD", posts: 1, fontSize: 26, height: 40 })}</g>`);
    const e1 = S(-W2 * 0.4, -86), e2 = S(W2 * 0.35, -86), e3 = S(W2 * 0.9, -70);
    const fire = K.flames(e1[0], e1[1] + 6, 0.62) + K.flames(e2[0], e2[1] + 6, 0.48) + K.flames(e3[0], e3[1] + 4, 0.34) + smoke(e2[0] - 10, e2[1] - 60, 2, 60);
    const hb = P(R.hand[0]);
    const toss = `<path d="M${f(hb[0] - 6)},${f(hb[1] - 14)} Q${f(hb[0] - 40)},${f(sy0 - 70)} ${f(sx0 + 40)},${f(sy0 - 60)}" fill="none" stroke="${ink}" stroke-width="3.5" stroke-dasharray="3 11" stroke-linecap="round" opacity="0.7"/>`;
    // the treadmill: a cream belt on a slate frame, rollers at both ends
    let marks = "";
    for (let x = -280; x <= 220; x += 60) marks += `M${x},${belt + 6} l-14,14 `;
    const tm = `<rect x="-320" y="${belt}" width="580" height="26" rx="13" fill="${C.cream}" stroke="${ink}" stroke-width="5"/><path d="${marks}" stroke="${C.tan}" stroke-width="4"/>` +
      `<path d="M-300,${belt + 26} L-320,0 M240,${belt + 26} L260,0" stroke="${ink}" stroke-width="12" stroke-linecap="round"/>` +
      `<rect x="-340" y="-8" width="620" height="14" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>`;
    const speed = `<path d="M-220,-110 h-110 M-210,-170 h-140 M-230,-230 h-90" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>` +
      `<path d="M${f(rx - 20)},${belt - 6} q-30,-8 -60,0 M${f(rx + 40)},${belt - 6} q-30,-8 -60,0" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`;
    // the drive belt to the first gear at the right edge
    const gears = at(600, -8, 1.4, K.props.gears({ n: 3 }));
    const drive = `<path d="M240,${belt + 13} L520,-70" stroke="${ink}" stroke-width="7"/><path d="M240,${belt + 13} L520,-70" stroke="${C.rust}" stroke-width="3"/>`;
    const plate = field() + gears + drive + tm + payout + speed + rich + btn + topHat + lit + toss + sign + fire;
    const svg = `<rect width="1920" height="1080" fill="${SKY}"/>` + view(80, -230, 2.15, plate);
    return { svg, alt: "The Rich Human sprints on a treadmill with dollar signs in his eyes, holding his own top hat out upside down under a payout slot on the treadmill's front post: it is heaped with medicine papers and one more is dropping in. His cigar is freshly lit, and the burning PLEASE BE GOOD sign he lit it off tumbles away over his shoulder; gears turn beside the treadmill." };
  },

  "bribe-humanity"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "dying.": the manual slammed shut on the right end of the lectern, a glove and the HERO sash end sticking
    // out of its pages, a medicine paper standing on it; the wastebasket of BE A BETTER HUMAN books right of the
    // lectern; the Reaper on the free wall looking at his blank tally, his blade wilted
    const MX = 935, MY = 790, k = 1.6;
    const top = MY - 124 * k;
    // squashed in the closed book: the HERO sash's end hanging out of its right edge, a flat navy glove poking out
    // of the top
    const sash = `<path d="M${MX + 64},${MY - 150} l30,6 l-8,120 l-30,-6 Z" fill="${C.war}" stroke="${ink}" stroke-width="3.5"/>` +
      `<g transform="translate(${MX + 80},${MY - 82}) rotate(95)">${osw(0, 6, 17, "HERO", C.cream)}</g>`;
    const glove = `<path d="M${MX + 18},${top + 2} l10,-34 l9,2 l2,-14 l9,2 l3,-12 l9,3 l1,-10 l10,4 l-6,60 Z" fill="${C.navy}" stroke="${ink}" stroke-width="3.5" stroke-linejoin="round"/>`;
    const manual = sash + at(MX, MY, k, K.props.manual({ size: 1 })) + glove;
    const treat = at(MX - 40, top - 52, 0.85, K.money("med", 0));
    // the tin wastebasket, heaped with identical self-help books
    const book = (x, y, r) => `<g transform="translate(${x},${y}) rotate(${r})"><rect x="-46" y="-16" width="92" height="32" fill="${C.peri}" stroke="${ink}" stroke-width="3.5"/>` +
      `<rect x="-46" y="-16" width="10" height="32" fill="${C.navy}"/>${osw(5, -3, 10, "BE A BETTER", C.cream)}${osw(5, 10, 10, "HUMAN", C.cream)}</g>`;
    const bx = 1150;
    const heap = [[bx - 40, 846, -8], [bx + 34, 850, 10], [bx - 4, 822, 4], [bx - 52, 806, -18], [bx + 46, 812, 22], [bx + 4, 782, -6], [bx - 20, 752, 12]].map(([x, y, r]) => book(x, y, r)).join("");
    const bin = `<path d="M${bx - 95},860 L${bx - 80},1090 H${bx + 80} L${bx + 95},860 Z" fill="${C.slate}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>` +
      `<path d="M${bx - 100},860 H${bx + 100}" stroke="${ink}" stroke-width="12" stroke-linecap="round"/><path d="M${bx - 100},860 H${bx + 100}" stroke="${C.peri}" stroke-width="6" stroke-linecap="round"/>` +
      [-50, 0, 50].map((d) => `<path d="M${bx + d * 0.95},878 L${bx + d * 0.82},1080" stroke="${C.peri}" stroke-width="4"/>`).join("");
    // the Reaper: his blade wilted, looking down at his blank clipboard
    // the scythe's staff bends over at the top like a dead flower's stem and the blade hangs straight down off it
    const wilt = `<g class="reaper-scythe"><path d="M46,98 L58,-150 Q62,-200 96,-196" fill="none" stroke="${ink}" stroke-width="13" stroke-linecap="round"/><path d="M46,98 L58,-150 Q62,-200 96,-196" fill="none" stroke="${C.tan}" stroke-width="7" stroke-linecap="round"/>` +
      `<path d="M96,-196 C122,-180 124,-120 104,-70 C112,-110 104,-160 86,-182 Z" fill="${C.cream}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/></g>`;
    const reaper = K.reaper({ pose: "sulk" }) + wilt;
    const rk = 2.5, rxp = 1530, ryp = 1070 - 100 * rk;
    const clip = at(rxp - 20 * rk, ryp - 40 * rk, rk * 0.5, `<g transform="rotate(62)">${K.props.clipboard({ title: "", items: [] })}</g>`);
    const front = mug(610, 790, C) + manual + treat + bin + heap + at(rxp, ryp, rk, reaper) + clip;
    const svg = push(K.STUDIO, 1.06, H.host("sideeye-closed", "idle", front));
    return { svg, alt: "Wishonia side-eyes the camera at her lectern: the manual on its right end is slammed shut with a glove and a HERO sash sticking out, one medicine paper standing on top like a treat; beside the lectern a wastebasket is heaped with BE A BETTER HUMAN books, and on the right the Grim Reaper looks down at his blank clipboard, his scythe's blade wilted like a dead flower." };
  },
};
