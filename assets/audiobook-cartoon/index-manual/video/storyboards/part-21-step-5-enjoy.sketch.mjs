// Sketches for storyboards/part-21-step-5-enjoy.md: each scene's key frame on a 1920 x 1080 frame (16:9), in the
// film look (Part 2 is the reference). Host shots use H.host (KIT.STUDIO, 16:9: the lectern's reading top at y 790,
// x 540 to 980; the free wall right of it x 1100 to 1880). Plates are drawn in plate units (the volcano road's back
// edge at y 0, the road to y 170, everyone at scale 1.5, feet at y 90) and framed as the camera sees them.
// Captions keep-out: below y 900.

const f = (n) => (+n).toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});
// A plate framing as KIT.camera places it: plate point (x, y) in the middle of the frame, at scale s.
const view = (x, y, s, inner) => `<g transform="translate(${f(960 - x * s)},${f(540 - y * s)}) scale(${s})">${inner}</g>`;
const at = (x, y, k, inner, rot = 0) => `<g transform="translate(${f(x)},${f(y)})${rot ? ` rotate(${rot})` : ""}${k !== 1 ? ` scale(${k})` : ""}">${inner}</g>`;
// A deterministic jitter in -1..1 (a hash of the index, so every build draws the same).
const jit = (i, j = 0) => {
  const s = Math.sin(i * 12.9898 + j * 78.233) * 43758.5453;
  return (s - Math.floor(s)) * 2 - 1;
};

const SKY = "#EFE6C8", GROUND = "#C8B07B", FAR = "#BBA16C", ROAD = "#EEE3C4", EDGE = "#B09363", DASH = "#C7AB78";
const KP = 1.5; // everyone on the road, in plate units

// The cast's options (the same in every scene).
const YOU = { tone: 2, outfit: "suit", hat: "bowler" };
// the insurance clerk is Part 8's CLAIMS clerk (fifty-nine-elevens): the same options and green eyeshade
const CLERK = { tone: 0, outfit: "suit", hair: 2, color: 1, seed: 21 };
const MORAL = { tone: 1, outfit: "shirt", kind: "twig", color: 3, mood: "smile" };

// The volcano road in plate units from x0 to x1: the sky, the field to the horizon (y -760), the road (y 0 to 170)
// with Part 2's colors and dashed center line, and the field in front of it.
function road(x0, x1) {
  const w = x1 - x0;
  return `<rect x="${x0}" y="-4000" width="${w}" height="3240" fill="${SKY}"/><rect x="${x0}" y="-760" width="${w}" height="760" fill="${GROUND}"/>` +
    `<rect x="${x0}" y="-760" width="${w}" height="14" fill="${FAR}"/><rect x="${x0}" y="170" width="${w}" height="2000" fill="${GROUND}"/>` +
    `<rect x="${x0}" y="-8" width="${w}" height="186" fill="${EDGE}"/><rect x="${x0}" y="0" width="${w}" height="170" fill="${ROAD}"/>` +
    `<path d="M${x0},85 H${x1}" stroke="${DASH}" stroke-width="8" stroke-dasharray="52 60"/>`;
}
// A medicine bill hanging under a little cream parachute, the bill at (0, 0).
function chute(K, C, legs = 0) {
  const ink = C.line;
  return `<path d="M-62,-86 Q0,-150 62,-86 Q42,-96 21,-86 Q0,-96 -21,-86 Q-42,-96 -62,-86 Z" fill="${C.cream}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
    `<path d="M-21,-86 Q-12,-118 0,-128 M21,-86 Q12,-118 0,-128" fill="none" stroke="${ink}" stroke-width="2"/>` +
    `<path d="M-62,-86 L-44,-25 M-21,-86 L-30,-25 M21,-86 L30,-25 M62,-86 L44,-25" stroke="${ink}" stroke-width="2"/>` + K.money("med", legs);
}
// The money cloud: parachuting medicine bills on a jittered grid over plate x0..x1, y0..y1.
function cloud(K, C, x0, x1, y0, y1, k = 0.9, step = 170) {
  let out = "";
  let n = 0;
  for (let y = y0; y <= y1; y += step * 0.8) {
    for (let x = x0 + ((y / step) % 2 ? step / 2 : 0); x <= x1; x += step) {
      n++;
      out += at(x + jit(n) * 40, y + jit(n, 1) * 30, k, chute(K, C, n % 2), jit(n, 2) * 10);
    }
  }
  return out;
}
// A gold halo, a flat ring rx wide, at (x, y).
function halo(C, x, y, rx, w = 6) {
  return `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(rx)}" ry="${f(rx * 0.28)}" fill="none" stroke="${C.line}" stroke-width="${w + 5}"/>` +
    `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(rx)}" ry="${f(rx * 0.28)}" fill="none" stroke="${C.yellow}" stroke-width="${w}"/>`;
}
// The Moral Human (person units): a beanpole in a mustard shirt, hands clasped, eyes up, his halo over his head.
function moral(K, C, extra = {}, withHalo = true) {
  const o = copy(MORAL, copy({ arms: [[14, 150], [-14, -150]] }, extra));
  const R = K.rig(o);
  return K.person(o) + (withHalo ? halo(C, R.top[0], R.top[1] - 12, 20, 4) : "");
}
// YOU, optionally bubble-wrapped from neck to shoes and in a mustard crash helmet over his bowler (person units).
function you(K, C, extra = {}, wrapped = false, fid = "y") {
  const o = copy(YOU, extra);
  const R = K.rig(o);
  if (!wrapped) return K.person(o);
  const top = R.neck[1] + 4, w = 44;
  const shape = `M${-w + 6},${top} Q0,${top - 12} ${w - 6},${top} Q${w + 10},${top + 40} ${w},${(top + 100) / 2 + 20} Q${w + 4},86 ${w - 10},104 H${-w + 10} Q${-w - 4},86 ${-w},${(top + 100) / 2 + 20} Q${-w - 10},${top + 40} ${-w + 6},${top} Z`;
  let bubbles = "";
  for (let y = top + 8; y < 104; y += 13) for (let x = -w; x <= w; x += 13) bubbles += `<circle cx="${x + ((y / 13) % 2 ? 6 : 0)}" cy="${y}" r="4.2" fill="none" stroke="#FFFFFF" stroke-width="1.6" opacity="0.85"/>`;
  const wrap = `<defs><clipPath id="${fid}-wrap"><path d="${shape}"/></clipPath></defs>` +
    `<path d="${shape}" fill="#F6F4EE" fill-opacity="0.42" stroke="${C.line}" stroke-width="2.4"/><g clip-path="url(#${fid}-wrap)">${bubbles}</g>` +
    `<path d="M${-w + 4},${top + 30} Q0,${top + 22} ${w - 2},${top + 30} M${-w + 2},${top + 66} Q0,${top + 58} ${w},${top + 66}" fill="none" stroke="${C.line}" stroke-width="1.4" opacity="0.5"/>`;
  const hx = R.top[0], hy = R.top[1];
  const helmet = `<path d="M${hx - 21},${hy + 6} Q${hx - 22},${hy - 24} ${hx},${hy - 26} Q${hx + 24},${hy - 24} ${hx + 23},${hy + 6} Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="2.6" stroke-linejoin="round"/>` +
    `<path d="M${hx - 4},${hy - 25} Q${hx + 2},${hy - 8} ${hx},${hy + 5}" fill="none" stroke="${C.orange}" stroke-width="4"/>` +
    `<path d="M${hx - 19},${hy + 6} Q${hx - 16},${hy + 30} ${hx + 2},${hy + 34} M${hx + 21},${hy + 6} Q${hx + 20},${hy + 26} ${hx + 6},${hy + 34}" fill="none" stroke="${C.line}" stroke-width="2.4"/>`;
  return K.person(o) + wrap + helmet;
}
// The insurance clerk (Part 8's CLAIMS clerk) with his green eyeshade, drawn as Part 8 draws it (person units).
function clerk(K, C, extra = {}) {
  const o = copy(CLERK, extra);
  const R = K.rig(o), d = R.facing || 1;
  const shade = `<path d="M${-24 * d},${f(R.hy - 6)} L${24 * d},${f(R.hy - 6)} L${30 * d},${f(R.hy + 4)} L${-22 * d},${f(R.hy + 4)} Z" fill="${C.med}" stroke="${C.line}" stroke-width="2"/>`;
  return K.person(o) + shade;
}
// A heap of bills (a tapered stack of rows), its base centered on (0, 0), h tall, w wide at the base.
function heap(K, h, w, kind, seed = 1, k = 0.55, legs = false) {
  let out = "";
  let n = seed * 100;
  for (let y = -12; y > -h; y -= 26) {
    const half = (w / 2) * (1 - (-y / h) * 0.55);
    for (let x = -half; x <= half; x += 50) {
      n++;
      let bill = K.money(typeof kind === "function" ? kind(y) : kind, n % 2);
      if (!legs) bill = bill.replace('class="legs"', 'class="legs" opacity="0"');
      out += at(x + jit(n) * 10, y + jit(n, 3) * 6, k, bill, jit(n, 4) * 16);
    }
  }
  return out;
}
// Oswald capitals.
function osw(x, y, size, text, fill, anchor = "middle") {
  return `<text x="${f(x)}" y="${f(y)}" text-anchor="${anchor}" font-family="Oswald" font-weight="600" font-size="${size}" letter-spacing="${(size * 0.05).toFixed(1)}" fill="${fill}">${text}</text>`;
}
// Fraunces Black, one color.
function num(x, y, size, text, fill, anchor = "middle") {
  return `<text x="${f(x)}" y="${f(y)}" text-anchor="${anchor}" font-family="Fraunces" font-weight="900" font-size="${size}" fill="${fill}">${text}</text>`;
}
// Dizzy stars in a ring round (x, y).
function stars(C, x, y, rx, n = 5, s = 1) {
  let out = `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(rx)}" ry="${f(rx * 0.3)}" fill="none" stroke="${C.cream}" stroke-width="2.5" stroke-dasharray="6 9" opacity="0.8"/>`;
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2 + 0.4, sx = x + rx * Math.cos(a), sy = y + rx * 0.3 * Math.sin(a);
    out += at(sx, sy, s * (0.8 + 0.3 * Math.sin(a)), `<path d="M0,-14 L4,-4 L14,-3 L6,4 L9,14 L0,8 L-9,14 L-6,4 L-14,-3 L-4,-4 Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="2.2" stroke-linejoin="round"/>`);
  }
  return out;
}

export default {
  "step-5-enjoy-title"(H, fid) {
    const { K, C } = H;
    // the atomic card (16:9): the emblem at (960, 290), rx 200, ry 62; the three papers sitting back on their orbits,
    // cross seals, legs crossed
    const cx = 960, cy = 280, rx = 200, ry = 62, TILT = [0, 60, -60];
    const orbits = TILT.map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = [[0, -2.64], [-60, -0.35], [60, 0.4]].map(([a, th], i) => {
      const ar = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      const x = cx + ex * Math.cos(ar) - ey * Math.sin(ar), y = cy + ex * Math.sin(ar) + ey * Math.cos(ar);
      // the orbit's tangent there, kept upright
      const tx = -rx * Math.sin(th), ty = ry * Math.cos(th);
      let tang = (Math.atan2(tx * Math.sin(ar) + ty * Math.cos(ar), tx * Math.cos(ar) - ty * Math.sin(ar)) * 180) / Math.PI;
      if (tang > 90) tang -= 180;
      if (tang < -90) tang += 180;
      // sitting on the orbit: the bill leaned back on the line, its stick legs out along it and crossed at the ankles
      const sit = `<g transform="translate(-6,-34) rotate(-28)">${K.money("med", 0).replace('class="legs"', 'class="legs" opacity="0"')}</g>` +
        `<path d="M10,-8 L44,-2 L66,-12 M14,-2 L46,-10 L68,-2" fill="none" stroke="${C.cream}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>` +
        `<path d="M10,-8 L44,-2 L66,-12 M14,-2 L46,-10 L68,-2" fill="none" stroke="${C.line}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>`;
      return at(x, y, 0.72, sit, tang);
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    const word = (y, s, text) => {
      const t0 = (dx, dy, extra) => `<text x="${960 + dx}" y="${y + dy}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${s}" ${extra}>${H.esc(text)}</text>`;
      return t0(0.04 * s, 0.053 * s, `fill="${C.ink}"`) + t0(0, 0, `fill="${C.cream}" stroke="${C.cream}" stroke-width="${f(0.044 * s)}" stroke-linejoin="round" style="paint-order:stroke"`);
    };
    const italic = `<text x="910" y="852" text-anchor="middle" font-family="Inter" font-weight="700" font-style="italic" font-size="52" fill="${C.cream}" stroke="${C.ink}" stroke-width="6" stroke-linejoin="round" style="paint-order:stroke">Everyone Gets Rich and Nobody Dies</text>`;
    // the Reaper risen beside the line's right end: his skull without its jaw, bony fingers on the "s" of Dies, the jaw
    // falling away below him
    const rk = 2.0, rx0 = 1540, ry0 = 790 + 130 * rk;
    const reaper = K.reaper({ pose: "puppet", face: "delight" });
    const fingers = [0, 1, 2, 3].map((i) => `<path d="M${1398 + i * 14},${842 - (i % 2) * 3} q2,-18 8,-24 q6,-4 8,4 l-4,24" fill="#F1EAD6" stroke="${C.line}" stroke-width="2.6" stroke-linejoin="round"/>`).join("") +
      `<path d="M1460,846 Q1480,850 1500,840" fill="none" stroke="#141B2B" stroke-width="22" stroke-linecap="round"/>`;
    const jaw = at(1556, 958, rk * 1.2, `<path d="M-13,-4 Q-12,10 0,12 Q12,10 13,-4 L9,-4 Q8,5 0,6 Q-8,5 -9,-4 Z" fill="#F1EAD6" stroke="${C.line}" stroke-width="2"/><path d="M-6,-3 v5 M-2,-3 v6 M2,-3 v6 M6,-3 v5" stroke="${C.line}" stroke-width="1.4"/>`, 28);
    const fall = `<path d="M1524,918 l-6,-22 M1586,918 l6,-22 M1556,910 v-24" stroke="${C.cream}" stroke-width="4" stroke-linecap="round" opacity="0.8"/>`;
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + nucleus + bills + at(rx0, ry0, rk, reaper) +
      word(560, 92, "STEP 5") + word(760, 190, "ENJOY") + italic + fingers + fall + jaw;
    return { svg, alt: "The navy period title card: the atom emblem's three green papers, cross seals now, sitting back on their orbits with their legs crossed; STEP 5 over ENJOY, the italic line Everyone Gets Rich and Nobody Dies under them, and the Grim Reaper risen beside its right end, his bony fingers on the s of Dies, his skull without its jaw, the jaw falling away below." };
  },

  "money-defeats-morality"(H, fid) {
    const { K, C } = H;
    // the scale on the free wall right of the lectern, standing on the bottom edge: left pan slammed down (tilt -18)
    const sk = 3.3, sx = 1500, sy = 1088, tilt = -18;
    const scale = at(sx, sy, sk, K.props.balanceScale({ tilt, left: "", right: "" }));
    // the stack of old halos ringed round its post, from the floor up
    // old halos ringed round the post like quoits, each a fat gold ring off true: its back arc behind the post, its
    // front arc in front, so they read as separate rings; a glint on the top one
    let stack = "";
    const postW = 10 * sk;
    for (let i = 0; i < 5; i++) {
      const y = sy - 70 - i * 40, dx = [0, 8, -6, 5, -4][i], a = [0, -6, 5, -4, 7][i], r = 58, ry = 17;
      const cx0 = sx + dx;
      const arc = (sweep, col, w) => `<path d="M${cx0 - r},${y} A${r},${ry} 0 0,${sweep} ${cx0 + r},${y}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`;
      stack += `<g transform="rotate(${a} ${cx0} ${y})">` + arc(1, C.line, 17) + arc(1, "#C9962E", 10) + "</g>" +
        `<rect x="${sx - postW / 2}" y="${y - ry - 6}" width="${postW}" height="${ry + 8}" fill="${C.yellow}"/>` +
        `<g transform="rotate(${a} ${cx0} ${y})">` + arc(0, C.line, 17) + arc(0, C.yellow, 10) + `<path d="M${cx0 - r * 0.55},${y + ry * 0.7} Q${cx0},${y + ry * 1.05} ${cx0 + r * 0.3},${y + ry * 0.9}" fill="none" stroke="${C.cream}" stroke-width="3" stroke-linecap="round"/></g>`;
    }
    stack += `<path d="M${sx + 50},${sy - 264} l6,-16 l6,16 l16,6 l-16,6 l-6,16 l-6,-16 l-16,-6 Z" fill="${C.cream}" stroke="${C.line}" stroke-width="2"/>`;
    // the pans' rims: (-84 cos t, -150 - 84 sin t + 64) left, (84 cos t, -150 + 84 sin t + 64) right (scale units)
    const t = (tilt * Math.PI) / 180;
    const lx = sx - 84 * Math.cos(t) * sk, ly = sy + (-150 - 84 * Math.sin(t) + 64) * sk;
    const rxp = sx + 84 * Math.cos(t) * sk, ryp = sy + (-150 + 84 * Math.sin(t) + 64) * sk;
    // the plain bills piled on the left pan, the treaty scroll on top
    const pile = [[-40, -8, -6], [30, -10, 8], [-10, -36, 4], [44, -40, -10], [-46, -42, 12]].map(([dx, dy, a], i) => at(lx + dx, ly + dy - 4, 0.95, K.money("plain", i % 2).replace('class="legs"', 'class="legs" opacity="0"'), a)).join("");
    const scroll = at(lx + 4, ly - 62, 1.0, `<g transform="rotate(-80)">${K.props.scroll({ text: "TREATY", size: 0.55 })}</g>`);
    // the right pan up and empty; the Moral Human, who weighs nothing, floating up out of the top of the picture like a
    // lost balloon (only his dangling shoes and shins still in frame), his halo left hanging in the air below them
    const mk = 2.4;
    const floater = at(rxp + 30, 120 - 100 * mk, mk, moral(K, C, { build: { legPose: [[-6, 10], [8, -4]] } }, false), 7);
    const drift = `<path d="M${rxp - 20},${ryp - 250} q-18,-40 0,-80 q18,-40 0,-80 M${rxp + 80},${ryp - 270} q16,-36 0,-72" fill="none" stroke="${C.cream}" stroke-width="5" stroke-linecap="round" stroke-dasharray="18 16" opacity="0.8"/>`;
    const hl = halo(C, rxp + 4, ryp - 330, 40, 7);
    const front = scale + stack + pile + scroll + drift + floater + hl;
    const svg = H.host("smirk-smile", "presenting", front);
    return { svg, alt: "Wishonia smirks at her lectern, presenting the tall brass scale beside it: its left pan slammed down under a pile of plain green bills and the TREATY scroll, its right pan up and empty; the weightless Moral Human floats up out of the top of the picture like a lost balloon, only his dangling shoes still in frame, and his gold halo hangs in the air below them; round the scale's post, a stack of old gold halos." };
  },

  "money-volcano"(H, fid) {
    const { K, C } = H;
    const ink = C.line;
    // the camera tilted up with the Weapons Maker: his tower of money (war bills to y -600, medicine bills above) at the
    // factory stop (x 1800), its top at y -1080 up in the money cloud
    const volcano = `<path d="M-950,-10 L-640,-520 L-330,-980 L-160,-1100 L160,-1100 L330,-980 L640,-520 L950,-10 Z" fill="${C.rust}" stroke="${ink}" stroke-width="7" stroke-linejoin="miter"/>` +
      `<path d="M330,-980 L640,-520 L950,-10 L520,-10 L380,-560 Z" fill="${C.tan}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/>`;
    const factory = at(2160, -10, KP, K.props.factory({ label: "" }));
    const T = -1060;
    const tower = `<g transform="translate(1800,0)">${heap(K, -T, 440, (y) => (y > -650 ? "war" : "med"), 2, 0.66)}</g>`;
    // sitting on the top, legs over the front, cradling the baby missile
    const wm = K.castOpts("weaponsMaker", { look: "left", mood: "grin", build: copy(K.CAST.weaponsMaker.build, { legPose: [[-85, -5], [-78, 6]] }) });
    const R = K.rig(wm), wk = KP * 1.1, oy = T + 8 - R.hipY * wk;
    const man = at(1800, oy, wk, K.person(wm));
    const kiss = [0, 1].map((i) => at(1800 + R.mouth[0] * wk - 46 - i * 34, oy + R.mouth[1] * wk - 30 - i * 40, 1.3 - i * 0.35, `<path d="M0,6 C-12,-6 -10,-16 -2,-14 C2,-13 0,-9 0,-8 C0,-9 -2,-13 2,-14 C10,-16 12,-6 0,6 Z" fill="${C.war}" stroke="${ink}" stroke-width="2"/>`)).join("");
    // a bill bent over his hard hat, and the bonk
    const hatTop = oy + R.top[1] * wk;
    const bonk = at(1790, hatTop - 44, 1.15, chute(K, C, 1), -16) + `<path d="M1730,${hatTop - 10} l-26,-10 M1736,${hatTop + 6} l-28,4 M1852,${hatTop - 12} l24,-12 M1856,${hatTop + 4} l28,0" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`;
    const cl = cloud(K, C, 900, 2900, -1640, -1360, 1.15, 270);
    const smoke = [0, 1, 2].map((i) => `<circle cx="${2060 + i * 100}" cy="${-700 - i * 30}" r="${30 + i * 6}" fill="#E9E1CF" stroke="${ink}" stroke-width="4"/>`).join("");
    const plate = road(-1200, 3600) + volcano + factory + smoke + tower + cl + man + kiss + bonk;
    const svg = `<rect width="1920" height="1080" fill="${SKY}"/>` + view(1800, -1040, 1.0, plate);
    return { svg, alt: "Tilted up into the sky over the road: the Weapons Maker sits on top of a towering heap of money, war bills at the bottom and medicine bills above, his hard hat bonked into the cloud of parachuting medicine bills, dizzy stars round it, kissing his baby missile; the volcano's slope at the left, the factory's missile chimneys at the bottom right." };
  },

  "pharma-per-patient"(H, fid) {
    const { K, C } = H;
    const ink = C.line;
    // the lab stop (x 3050): the bench at x 3260, the Scientist at x 3000 behind the turnstile (x 2830); passers-by
    // turn off the road on their own and queue at it (no hook); the patients come out spinning on the right
    const lab = at(3300, -14, KP, K.props.lab({}));
    const turn = at(2830, 60, KP,
      `<rect x="-30" y="-116" width="60" height="116" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><rect x="-36" y="-128" width="72" height="16" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="-14" y="-124" width="28" height="5" fill="${ink}"/><circle cx="0" cy="-80" r="11" fill="${C.cream}" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M0,-80 L-62,-88 M0,-80 L40,-120 M0,-80 L34,-34" stroke="${ink}" stroke-width="11" stroke-linecap="round"/><path d="M0,-80 L-62,-88 M0,-80 L40,-120 M0,-80 L34,-34" stroke="#C9CED6" stroke-width="5" stroke-linecap="round"/>` +
      `<path d="M-52,-140 l-10,-12 M-40,-148 l-2,-16 M48,-140 l10,-12" stroke="${ink}" stroke-width="3" stroke-linecap="round"/>`);
    // the bill popping out of the turnstile's slot up to her hand
    const sci = K.castOpts("scientist", { mood: "greedy", look: "left", arms: [[-70, -110], [-20, -60]], holdR: "clipboard" });
    const SR = K.rig(sci), sxp = 3010, syp = 90 - 100 * KP;
    const scientist = at(sxp, syp, KP, K.person(sci));
    const hL = [sxp + SR.hand[0][0] * KP, syp + SR.hand[0][1] * KP];
    // the queue: passers-by lined up at the turnstile on their own, the last one turning off the road to join it
    const q = [[2700, 7, 0, "eager"], [2560, 11, 1, "greedy"], [2420, 15, 2, "eager"], [2270, 19, 3, "smile"]];
    const passer = q.map(([x, seed, i, mood]) => at(x, 90 - 100 * KP + (i === 3 ? 40 : 0), KP,
      K.person({ tone: (seed + 1) % 4, outfit: i % 2 ? "dress" : "shirt", hair: i % 2, color: (seed + i) % 4, seed, look: "right", mood }), i === 3 ? -8 : 0)).join("");
    // a medicine bill popping out of the turnstile up into her hand
    const pop = at(hL[0] - 10, hL[1] + 6, 0.95, K.money("med", 1), 18) + `<path d="M2850,-180 l-6,22 M2880,-176 v24 M2910,-182 l8,22" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`;
    const cane = "";
    const spin = (x, seed, rot) => at(x, 90 - 100 * KP, KP, K.person({ tone: (seed % 4), outfit: seed % 2 ? "dress" : "shirt", hair: seed % 2, color: seed % 4, seed, mood: "eager", arms: [[120, 150], [-120, -150]] }), rot) +
      `<ellipse cx="${x}" cy="${90 - 230}" rx="90" ry="20" fill="none" stroke="${ink}" stroke-width="3.5" stroke-dasharray="20 14"/>`;
    const spinners = spin(3550, 3, 8) + spin(3760, 6, -10);
    const smoke = `<path d="M2800,-230 q-20,-30 0,-56 q20,-26 0,-52 M2850,-240 q-18,-26 0,-48" fill="none" stroke="#7A7468" stroke-width="7" stroke-linecap="round" opacity="0.8"/>`;
    const plate = road(2000, 4200) + lab + turn + smoke + pop + spinners + scientist + passer + cane;
    const svg = `<rect width="1920" height="1080" fill="${GROUND}"/>` + view(3050, -170, 1.22, plate);
    return { svg, alt: "The lab stop on the road: passers-by have turned off the road on their own and queue at the Scientist's smoking turnstile, the last one stepping off the road to join them; a medicine bill pops up out of the turnstile into her hand, dollar signs in her eyes, and two patients spin like tops into the lab on the right." };
  },

  "insurance-zero-claims"(H, fid) {
    const { K, C } = H;
    const ink = C.line;
    // the insurer's stop (x 4300): the desk at x 4300 (top at y -110), the easel chart behind at x 4500, the paper
    // spike at the desk's left end and the cash register at its right; the clerk vaulting it to wrap YOU (x 4020);
    // the Reaper wheeling the headstone away on the right
    const easel = `<path d="M4380,-10 L4440,-560 M4660,-10 L4600,-560 M4520,-10 L4520,-470" stroke="${ink}" stroke-width="16" stroke-linecap="round"/>` +
      `<path d="M4380,-10 L4440,-560 M4660,-10 L4600,-560 M4520,-10 L4520,-470" stroke="#9A6A3E" stroke-width="8" stroke-linecap="round"/>` +
      `<rect x="4370" y="-640" width="300" height="230" fill="#FBF6E6" stroke="${ink}" stroke-width="6"/>` +
      [1, 2, 3].map((i) => `<path d="M4390,${-640 + i * 58} H4650" stroke="${DASH}" stroke-width="2"/>`).join("") +
      `<path d="M4392,-450 L4460,-500 L4520,-540 L4580,-600 L4600,-470 L4612,-412" fill="none" stroke="${ink}" stroke-width="13" stroke-linejoin="round"/>` +
      `<path d="M4392,-450 L4460,-500 L4520,-540 L4580,-600 L4600,-470 L4612,-412" fill="none" stroke="${C.war}" stroke-width="7" stroke-linejoin="round"/>` +
      `<path d="M4612,-412 L4606,-300 Q4600,-150 4650,-60 Q4700,10 4760,30" fill="none" stroke="${C.war}" stroke-width="7" stroke-linecap="round"/>`;
    const desk = `<rect x="4130" y="-130" width="360" height="22" fill="#8C6440" stroke="${ink}" stroke-width="5"/><rect x="4146" y="-108" width="110" height="98" fill="#7A5634" stroke="${ink}" stroke-width="5"/>` +
      `<rect x="4160" y="-90" width="82" height="30" fill="#8C6440" stroke="${ink}" stroke-width="3"/><path d="M4470,-108 V-10" stroke="${ink}" stroke-width="12"/>`;
    const spike = `<rect x="4160" y="-140" width="40" height="10" fill="${C.slate}" stroke="${ink}" stroke-width="3"/><path d="M4180,-140 V-230" stroke="${ink}" stroke-width="4"/>` +
      `<g transform="translate(4180,-176) rotate(-6)"><rect x="-26" y="-18" width="52" height="34" fill="#FBF6E6" stroke="${ink}" stroke-width="3"/><path d="M-18,-6 H18 M-18,4 H10" stroke="${ink}" stroke-width="2"/></g>`;
    const reg = `<g transform="translate(4420,-130)"><path d="M-62,0 L-54,-70 L54,-70 L62,0 Z" fill="${C.rust}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      `<rect x="-44" y="-96" width="88" height="28" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>` +
      [0, 1, 2, 3].map((i) => `<circle cx="${-36 + i * 24}" cy="-40" r="8" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>`).join("") +
      `<rect x="-62" y="0" width="124" height="22" fill="#5C3B24" stroke="${ink}" stroke-width="4"/><rect x="-56" y="16" width="112" height="16" fill="#5C3B24" stroke="${ink}" stroke-width="3"/>` +
      `<path d="M0,-96 V-150" stroke="${ink}" stroke-width="4"/><rect x="-72" y="-206" width="144" height="58" fill="#FBF6E6" stroke="${ink}" stroke-width="5"/>${osw(0, -162, 38, "NO SALE", C.war)}</g>`;
    // YOU being wrapped on the road in front of the desk, the clerk in mid-vault over it with the roll
    const youK = KP * 1.02;
    const youSvg = at(4020, 90 - 100 * youK, youK, you(K, C, { mood: "worried", look: "right", arms: [[18, 10], [-18, -10]] }, true, fid));
    const clk = clerk(K, C, { mood: "eager", look: "left", arms: [[-100, -150], [-80, -130]] });
    const clerkSvg = at(4240, -330, KP, clk, -32);
    const roll = `<path d="M4110,-330 Q4040,-300 4000,-190 Q3960,-80 3990,40" fill="none" stroke="#FFFFFF" stroke-width="26" stroke-opacity="0.55"/><path d="M4110,-330 Q4040,-300 4000,-190 Q3960,-80 3990,40" fill="none" stroke="${ink}" stroke-width="2" stroke-dasharray="4 10"/>` +
      `<circle cx="4120" cy="-338" r="26" fill="#F6F4EE" stroke="${ink}" stroke-width="4"/><circle cx="4120" cy="-338" r="8" fill="${C.slate}"/>`;
    const vault = `<path d="M4300,-420 q30,-30 70,-20 M4330,-450 q40,-20 70,0" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`;
    // the Reaper wheeling the rosetted headstone away on his hand truck
    const reap = at(4880, 90 - 100 * KP * 0.95, KP * 0.95, K.reaper({ pose: "puppet" }));
    const truck = `<path d="M4800,60 L4720,-170 M4800,60 H4700" stroke="${ink}" stroke-width="10" stroke-linecap="round"/><path d="M4800,60 L4720,-170 M4800,60 H4700" stroke="${C.slate}" stroke-width="5" stroke-linecap="round"/><circle cx="4790" cy="70" r="20" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>`;
    const stone = at(4730, 50, KP * 0.95, K.props.headstone({ text: "RIP" }), 10);
    const rosette = at(4720, -100, 1.3, `<path d="M-6,8 L-14,40 L-4,34 L0,44 L4,30 Z M6,8 L12,38 L4,32 Z" fill="${C.peri}" stroke="${ink}" stroke-width="2.4"/>` +
      Array.from({ length: 12 }, (_, i) => { const a = (i / 12) * Math.PI * 2; return `<circle cx="${f(Math.cos(a) * 16)}" cy="${f(Math.sin(a) * 16)}" r="8" fill="${C.peri}" stroke="${ink}" stroke-width="2"/>`; }).join("") +
      `<circle r="14" fill="${C.yellow}" stroke="${ink}" stroke-width="2.6"/><path d="M0,-7 L2,-2 L7,-2 L3,1 L4,7 L0,4 L-4,7 L-3,1 L-7,-2 L-2,-2 Z" fill="${C.cream}"/>`);
    const plate = road(3300, 5300) + easel + desk + spike + reg + truck + stone + rosette + reap + youSvg + roll + clerkSvg + vault;
    const svg = `<rect width="1920" height="1080" fill="${GROUND}"/>` + view(4380, -190, 1.12, plate);
    return { svg, alt: "The insurer's stop: the clerk in his green eyeshade vaults his desk with a roll of bubble wrap, wrapping a worried YOU on the road; the cash register's flag reads NO SALE, one thin claim sits on the paper spike, the easel chart's red line dives off the bottom of the chart and runs down its leg into the grass, and on the right the Grim Reaper wheels a headstone with a prize rosette away on his hand truck." };
  },

  "investor-lobby-force"(H, fid) {
    const { K, C } = H;
    const ink = C.line;
    // the hill of medicine bills marching along the road (x 5800) on little legs, the Rich Human on top with a
    // megaphone and the picket sign, his monocle popped out on its string; behind, the dial at 3% and the pretzel
    // missile drooping on the ground
    const hx = 5820, hh = 380;
    let legs = "";
    for (let i = 0; i < 16; i++) {
      const x = hx - 270 + i * 36, ph = i % 2;
      legs += `<path d="M${x},40 l${ph ? -14 : 12},48 h${ph ? -10 : 10}" fill="none" stroke="${ink}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>`;
    }
    const hill = `<g transform="translate(${hx},50)">${heap(K, hh, 600, "med", 5, 0.62)}</g>`;
    // tiny picket signs among the bills
    const pickets = [[-200, -60], [-120, -170], [60, -150], [170, -40], [-40, -260], [120, -260]].map(([dx, dy]) =>
      `<path d="M${hx + dx},${50 + dy} v-60" stroke="${ink}" stroke-width="4"/><rect x="${hx + dx - 20}" y="${50 + dy - 86}" width="40" height="28" fill="#FBF6E6" stroke="${ink}" stroke-width="3"/>`).join("");
    const flag = `<path d="M${hx - 150},${50 - hh + 60} V${50 - hh - 80}" stroke="${ink}" stroke-width="5"/><path d="M${hx - 150},${50 - hh - 80} H${hx - 30} L${hx - 50},${50 - hh - 50} L${hx - 30},${50 - hh - 20} H${hx - 150} Z" fill="#FBF6E6" stroke="${ink}" stroke-width="4"/>` +
      num(hx - 94, 50 - hh - 34, 34, "272%", C.navy);
    // the Rich Human on top (no monocle in his eye: it has popped out), the megaphone in his left hand, the sign in his right
    const rich = K.castOpts("richHuman", { mood: "worried", look: "right", prop: null, cigar: false, arms: [[-120, -150], [130, 170]] });
    const RR = K.rig(rich), rk = KP * 1.25, rx0 = hx + 30, ry0 = 50 - hh + 24 - 100 * rk;
    const richSvg = at(rx0, ry0, rk, K.person(rich));
    const hR = [rx0 + RR.hand[1][0] * rk, ry0 + RR.hand[1][1] * rk], hL = [rx0 + RR.hand[0][0] * rk, ry0 + RR.hand[0][1] * rk];
    const sign = `<path d="M${hR[0]},${hR[1] + 50} V${hR[1] - 150}" stroke="${ink}" stroke-width="12"/><path d="M${hR[0]},${hR[1] + 50} V${hR[1] - 150}" stroke="#9A6A3E" stroke-width="6"/>` +
      `<rect x="${hR[0] - 40}" y="${hR[1] - 300}" width="310" height="160" fill="#FBF6E6" stroke="${ink}" stroke-width="6"/>` +
      osw(hR[0] + 115, hR[1] - 232, 46, "MORE TRIALS,", C.navy) + osw(hR[0] + 115, hR[1] - 170, 46, "FEWER WARS", C.war);
    // the megaphone: a slate cone from his left hand, its bell to the left, blast lines out of it
    const meg = at(hL[0], hL[1], 1.4, `<path d="M8,-8 L-64,-34 L-64,34 L8,8 Z" fill="${C.slate}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/><ellipse cx="-64" cy="0" rx="10" ry="34" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/><rect x="2" y="-10" width="16" height="20" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>` +
      `<path d="M-84,-30 l-26,-14 M-88,0 h-30 M-84,30 l-26,14" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`, -8);
    // the monocle popped out of his eye and dangling on its string, and the pop lines
    const eye = [rx0 + RR.eyes[0] * rk, ry0 + RR.eyes[1] * rk];
    const mono = `<path d="M${eye[0] + 4},${eye[1] + 6} Q${eye[0] + 40},${eye[1] + 60} ${eye[0] + 28},${eye[1] + 104}" fill="none" stroke="${C.cream}" stroke-width="6"/><path d="M${eye[0] + 4},${eye[1] + 6} Q${eye[0] + 40},${eye[1] + 60} ${eye[0] + 28},${eye[1] + 104}" fill="none" stroke="${ink}" stroke-width="3"/>` +
      `<circle cx="${eye[0] + 28}" cy="${eye[1] + 122}" r="17" fill="#FFFFFF" fill-opacity="0.5" stroke="${C.yellow}" stroke-width="5"/><circle cx="${eye[0] + 28}" cy="${eye[1] + 122}" r="20" fill="none" stroke="${ink}" stroke-width="2"/>` +
      `<path d="M${eye[0] - 18},${eye[1] - 36} l-10,-16 M${eye[0] + 4},${eye[1] - 42} v-18 M${eye[0] + 26},${eye[1] - 36} l10,-16" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`;
    // the dial at 3% and the folded missile behind, at the hill's old place (x 5550)
    const dial = `<rect x="5291" y="-280" width="18" height="270" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>` +
      at(5300, -270, 1.9, K.props.gauge({ mount: "dial", value: 0.03, window: "3%", zones: [] }));
    const pretzel = at(5450, -20, 1.3, `<path d="M-60,0 C-80,-60 -10,-90 0,-40 C10,-90 80,-60 60,0 C40,30 -40,30 -60,0 Z" fill="none" stroke="${ink}" stroke-width="30" stroke-linejoin="round"/><path d="M-60,0 C-80,-60 -10,-90 0,-40 C10,-90 80,-60 60,0 C40,30 -40,30 -60,0 Z" fill="none" stroke="${C.war}" stroke-width="20" stroke-linejoin="round"/>` +
      `<path d="M50,8 L86,24 L58,30 Z" fill="${C.cream}" stroke="${ink}" stroke-width="3"/><circle cx="-10" cy="-30" r="4" fill="${ink}"/><circle cx="6" cy="-32" r="4" fill="${ink}"/><path d="M-12,-18 Q-2,-24 8,-18" fill="none" stroke="${ink}" stroke-width="3"/>`);
    const plate = road(4500, 7000) + dial + pretzel + legs + hill + pickets + flag + sign + richSvg + meg + mono;
    const svg = `<rect width="1920" height="1080" fill="${SKY}"/>` + view(5720, -400, 1.0, plate);
    return { svg, alt: "On the road, the Rich Human's hill of medicine bills marches along on dozens of little legs, a 272% flag on top and tiny picket signs among the bills; he rides on top with a megaphone and a picket sign, MORE TRIALS, FEWER WARS, his monocle popped out and dangling on its string; behind, the treaty dial reads 3% and a red missile lies folded into a pretzel." };
  },

  "wiki-voters-hammock"(H, fid) {
    const { K, C } = H;
    const ink = C.line;
    // the end of the road (x 9200): two palms at x 8930 and 9470, the hammock between them, YOU in it, the tag on
    // "$0", the Reaper a heap of bones at the foot of the left palm, his skull on top blinking
    const palm = (x, lean) => {
      const top = [x + lean, -660];
      const trunk = `<path d="M${x - 22},-10 Q${x + lean * 0.3 - 18},-340 ${top[0] - 12},${top[1]} L${top[0] + 12},${top[1]} Q${x + lean * 0.3 + 18},-340 ${x + 22},-10 Z" fill="#9A6A3E" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>` +
        [0, 1, 2, 3, 4, 5, 6].map((i) => { const t = 0.1 + i * 0.12, yy = -10 - 650 * t, xx = x + lean * t * t; return `<path d="M${xx - 20},${yy} Q${xx},${yy - 14} ${xx + 20},${yy}" fill="none" stroke="${ink}" stroke-width="3"/>`; }).join("");
      const fronds = [-150, -110, -60, -20, 20, 70, 120].map((a, i) => {
        const r = (a * Math.PI) / 180, L = 230 + (i % 2) * 40, ex = top[0] + Math.sin(r) * L, ey = top[1] - Math.cos(r) * L * 0.45 + 60;
        return `<path d="M${top[0]},${top[1]} Q${(top[0] + ex) / 2},${top[1] - 90} ${ex},${ey} Q${(top[0] + ex) / 2},${top[1] - 40} ${top[0]},${top[1]} Z" fill="#6E8F4E" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>`;
      }).join("");
      const nuts = [-20, 4, 26].map((dx) => `<circle cx="${top[0] + dx}" cy="${top[1] + 14}" r="15" fill="#6B4A2F" stroke="${ink}" stroke-width="3.5"/>`).join("");
      return trunk + fronds + nuts;
    };
    // the hammock: ropes from the trunks to its ends at y -330, the cloth sagging to y -160 in the middle
    const ropes = `<path d="M8955,-380 L9010,-330 M9445,-380 L9390,-330" stroke="${ink}" stroke-width="6"/>`;
    const back = `<path d="M9010,-330 Q9200,-40 9390,-330" fill="none" stroke="${ink}" stroke-width="5"/>`;
    const front = `<path d="M9010,-330 Q9200,-40 9390,-330 Q9200,-250 9010,-330 Z" fill="#E7C98A" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>` +
      [1, 2, 3, 4, 5, 6, 7].map((i) => { const t = i / 8, x = 9010 + 380 * t, yb = -330 + 2 * t * (1 - t) * 290, yt = -330 + 2 * t * (1 - t) * 80; return `<path d="M${f(x)},${f(yt + 4)} V${f(yb - 4)}" stroke="${C.rust}" stroke-width="3"/>`; }).join("");
    // YOU lying back in it (head left, feet right, face up), wrapped and helmeted, one hand up with the drink
    const yo = { mood: "smile", look: "right", arms: [[-30, -60], [150, 175]] };
    const YR = K.rig(copy(YOU, yo)), yk = KP * 1.0, yx = 9205, yy = -306, ya = -86;
    const youSvg = at(yx, yy, yk, `<g transform="rotate(${ya})">${you(K, C, yo, true, fid)}</g>`);
    const ar = (ya * Math.PI) / 180, hx0 = YR.hand[1][0], hy0 = YR.hand[1][1];
    const hand = [yx + yk * (hx0 * Math.cos(ar) - hy0 * Math.sin(ar)), yy + yk * (hx0 * Math.sin(ar) + hy0 * Math.cos(ar))];
    // his drink with a paper umbrella, in that hand
    const drink = at(hand[0], hand[1] - 8, 1.5, `<path d="M-14,-30 L14,-30 L8,10 L-8,10 Z" fill="#F6F4EE" fill-opacity="0.7" stroke="${ink}" stroke-width="3"/><path d="M-12,-20 L12,-20 L8,8 L-8,8 Z" fill="${C.orange}"/>` +
      `<path d="M4,-30 L16,-64" stroke="${ink}" stroke-width="2.4"/><path d="M-6,-60 Q16,-84 38,-62 Z" fill="${C.war}" stroke="${ink}" stroke-width="2.4"/><path d="M16,-74 L6,-60 M16,-74 L28,-62" stroke="${C.cream}" stroke-width="2"/>`);
    // the tag swung out from the hammock's underside, flipped to $0
    const tag = at(9250, -186, 1.7, K.props.priceTag({ text: "$0", angle: 16 }));
    const ham = ropes + back;
    // the bone heap at the foot of the left palm: bones, the hood and the scythe on top, the skull blinking
    const bx = 8820, by = 80;
    const bone = (x, y, a, L = 60) => at(x, y, 1, `<path d="M${-L / 2},0 H${L / 2}" stroke="${ink}" stroke-width="14" stroke-linecap="round"/><path d="M${-L / 2},0 H${L / 2}" stroke="#F1EAD6" stroke-width="8" stroke-linecap="round"/><circle cx="${-L / 2}" cy="-5" r="7" fill="#F1EAD6" stroke="${ink}" stroke-width="2.6"/><circle cx="${-L / 2}" cy="5" r="7" fill="#F1EAD6" stroke="${ink}" stroke-width="2.6"/><circle cx="${L / 2}" cy="-5" r="7" fill="#F1EAD6" stroke="${ink}" stroke-width="2.6"/><circle cx="${L / 2}" cy="5" r="7" fill="#F1EAD6" stroke="${ink}" stroke-width="2.6"/>`, a);
    const bones = bone(bx - 70, by, 8) + bone(bx + 60, by - 4, -12) + bone(bx, by - 24, 32) + bone(bx - 30, by - 40, -24, 50) + bone(bx + 40, by - 36, 64, 46) +
      `<path d="M${bx - 120},${by + 6} Q${bx - 60},${by - 80} ${bx + 10},${by - 70} Q${bx + 70},${by - 76} ${bx + 120},${by + 6} Z" fill="#141B2B" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>` +
      `<path d="M${bx - 160},${by - 20} L${bx + 150},${by - 90}" stroke="${ink}" stroke-width="13" stroke-linecap="round"/><path d="M${bx - 160},${by - 20} L${bx + 150},${by - 90}" stroke="${C.tan}" stroke-width="7" stroke-linecap="round"/>` +
      `<path d="M${bx + 150},${by - 90} C${bx + 170},${by - 150} ${bx + 120},${by - 200} ${bx + 40},${by - 210} C${bx + 110},${by - 180} ${bx + 130},${by - 140} ${bx + 120},${by - 96} Z" fill="${C.cream}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>`;
    const skull = at(bx - 10, by - 104, 2.0, `<circle cx="0" cy="0" r="17" fill="#F1EAD6" stroke="${ink}" stroke-width="3"/><path d="M-11,-3 Q-6,0 -1,-3" fill="none" stroke="${ink}" stroke-width="2.6" stroke-linecap="round"/><ellipse cx="6" cy="-3" rx="4.5" ry="5.5" fill="${ink}"/>` +
      `<path d="M-8,10 Q0,15 8,10 M-4,9 v4 M0,10 v4 M4,9 v4" fill="none" stroke="${ink}" stroke-width="1.8" stroke-linecap="round"/>`);
    const nut = `<circle cx="${bx + 150}" cy="${by + 20}" r="17" fill="#6B4A2F" stroke="${ink}" stroke-width="3.5"/>`;
    const plate = road(8000, 10400) + palm(8930, 40) + palm(9470, -30) + ham + youSvg + front + drink + tag + bones + skull + nut;
    const svg = `<rect width="1920" height="1080" fill="${SKY}"/>` + view(9180, -260, 1.1, plate);
    return { svg, alt: "The end of the road: YOU, bubble-wrapped and in a mustard crash helmet, lies back in a hammock slung between two palm trees, sipping a drink with a paper umbrella; a price tag hangs from the hammock reading $0; at the foot of the left palm the Grim Reaper is a heap of bones under his hood and scythe, his skull on top giving one blink, the coconut beside it." };
  },

  "evolve-morally"(H, fid) {
    const { K, C } = H;
    // the Moral Human on his back across the lectern's reading top (y 790, x 540 to 980), head at the right end,
    // arms and legs dangling over the edges, no halo, a ring of dizzy stars round his head
    // rotate(-90) lays a person on his back: head to the left, feet to the right, face up; the arms flung out
    // dangle over the front edge
    const o = copy(MORAL, { mood: "flat", look: "right", arms: [[-60, -10], [-120, -170]], build: { legPose: [[-20, -60], [-8, -40]] } });
    const R = K.rig(o), k = 2.5, bx = 790, by = 742, ang = -90;
    const body = at(bx, by, k, `<g transform="rotate(${ang})">${K.person(o)}</g>`);
    // where his head ended up
    const a = (ang * Math.PI) / 180, tx = R.top[0], ty = R.top[1] + 18;
    const hx = bx + k * (tx * Math.cos(a) - ty * Math.sin(a)), hy = by + k * (tx * Math.sin(a) + ty * Math.cos(a));
    const ring = stars(C, hx + 10, hy - 50, 86, 6, 1.5);
    const splat = `<path d="M560,786 l-30,6 M574,804 l-22,22 M990,800 l26,14 M1000,786 l30,2" stroke="${C.ink}" stroke-width="5" stroke-linecap="round"/>`;
    const svg = H.host("sideeye-closed", "idle", body + splat + ring);
    return { svg, alt: "Wishonia side-eyes the camera at her lectern; across its reading top in front of her lies the Moral Human, flat on his back, arms and legs dangling over the edges, no halo, a ring of little dizzy stars circling his head where it used to be." };
  },

  "greed-arrow"(H, fid) {
    const { K, C } = H;
    const ink = C.line;
    const HZ = 560;
    const field = `<rect width="1920" height="${HZ}" fill="${SKY}"/><rect y="${HZ}" width="1920" height="${1080 - HZ}" fill="${GROUND}"/><rect y="${HZ}" width="1920" height="12" fill="${FAR}"/>`;
    // the GREED arrow on its riveted slate post, pivoting at its middle (x 640, y 420), pointing right at the blobs
    const px = 640, py = 430;
    const post = `<rect x="${px - 20}" y="${py}" width="40" height="${850 - py}" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` +
      [0, 1, 2, 3].map((i) => `<circle cx="${px}" cy="${py + 70 + i * 90}" r="5" fill="${C.cream}" stroke="${ink}" stroke-width="2"/>`).join("") +
      `<rect x="${px - 60}" y="840" width="120" height="20" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>`;
    const arrowPts = [[-330, -24], [230, -24], [230, -64], [360, 0], [230, 64], [230, 24], [-330, 24], [-370, 52], [-370, -52]];
    const arrow = `<g transform="translate(${px},${py}) rotate(6)"><polygon points="${arrowPts.map((p) => p.join(",")).join(" ")}" fill="${C.yellow}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
      `<path d="M-326,16 H226 M230,52 L344,4" stroke="${C.orange}" stroke-width="7"/>` + osw(-170, 19, 50, "GREED", C.navy) +
      `<circle r="16" fill="${C.cream}" stroke="${ink}" stroke-width="5"/><circle r="5" fill="${ink}"/></g>`;
    // YOU at its tail, wrapped and helmeted, his shoulder still against it
    const youSvg = at(230, 860 - 100 * 1.95, 1.95, you(K, C, { mood: "grin", look: "right", arms: [[-110, -80], [-100, -70]] }, true, fid));
    // the flattened blobs on the right, flat as rugs and x-eyed, the cast standing on them
    const blobs = [[1130, "peri", 3], [1450, "rust", 8], [1760, "cyan", 13]].map(([x, col, seed]) =>
      at(x, 872, 1, `<g transform="scale(2.1,0.5)">${K.props.diseaseBlob({ color: col, seed, mood: "dead" })}</g>`)).join("");
    const dust = `<path d="M960,890 q30,-40 70,-10 M1880,880 q-30,-50 -70,-20" fill="none" stroke="#B9AE98" stroke-width="10" stroke-linecap="round" opacity="0.8"/>`;
    const ck = 1.6;
    const stand = (x, svgPerson) => at(x, 836 - 100 * ck, ck, svgPerson);
    const cast = stand(1060, K.person(K.castOpts("politician", { mood: "grin", look: "left", tieColor: C.med, arms: [[30, 20], [-150, -170]] }))) +
      stand(1240, K.person(K.castOpts("richHuman", { mood: "greedy", look: "left" }))) +
      stand(1420, K.person(K.castOpts("weaponsMaker", { mood: "greedy", look: "left", hold: null, arms: [[150, 175], [-20, -10]] }))) +
      stand(1590, K.person(K.castOpts("scientist", { mood: "greedy", look: "left" }))) +
      stand(1750, clerk(K, C, { mood: "greedy", look: "left" }));
    const svg = field + post + arrow + youSvg + blobs + dust + cast;
    return { svg, alt: "On a tan field, the mustard GREED arrow on its riveted slate post points right at three disease blobs flattened like rugs, x-eyed; the Politician with his teal tie, the Rich Human, the Weapons Maker, the Scientist and the insurance clerk stand on them grinning with dollar signs in their eyes; YOU, bubble-wrapped and helmeted, grins at the arrow's tail." };
  },
};
