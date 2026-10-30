// Sketches for storyboards/part-16-the-math.md: each scene's key moment as SVG on a 1920 x 1080 frame, in the film
// look (Part 2 is the reference). Host shots use H.host (KIT.STUDIO, 16:9: the lectern's reading top at y 790,
// x 540 to 980); plates are drawn as the camera sees them at that moment. Captions keep-out: below y 900.

const SKY = "#EFE6C8", FIELD = "#C8B07B", FIELD2 = "#BBA16C";

// Fraunces Black in one color (a stamped number in the sky, a trophy plate).
function num(x, y, size, text, fill, anchor = "middle") {
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Fraunces" font-weight="900" font-size="${size}" fill="${fill}">${text}</text>`;
}
// Oswald capitals.
function osw(x, y, size, text, fill, anchor = "middle", extra = "") {
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Oswald" font-weight="600" font-size="${size}" letter-spacing="${(size * 0.06).toFixed(1)}" fill="${fill}" ${extra}>${text}</text>`;
}
// Wishonia's coffee mug, standing on (x, y): rust, a cream band, a handle on the left.
function mug(x, y, C) {
  return `<g transform="translate(${x},${y})">` +
    `<path d="M-46,-62 q-26,0 -26,24 q0,24 26,24" fill="none" stroke="${C.ink}" stroke-width="13"/><path d="M-46,-62 q-26,0 -26,24 q0,24 26,24" fill="none" stroke="${C.rust}" stroke-width="7"/>` +
    `<path d="M-46,-78 H34 L30,0 H-42 Z" fill="${C.rust}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="round"/>` +
    `<rect x="-44" y="-56" width="76" height="14" fill="${C.cream}"/><path d="M-44,-56 H32 M-44,-42 H32" stroke="${C.ink}" stroke-width="2.5"/>` +
    `<ellipse cx="-6" cy="-78" rx="40" ry="7" fill="#3A2416" stroke="${C.ink}" stroke-width="4"/>` +
    `<path d="M-14,-92 q-10,-14 0,-26 q10,-12 0,-26 M8,-94 q-10,-14 0,-26" fill="none" stroke="${C.cream}" stroke-width="4" stroke-linecap="round" opacity="0.8"/></g>`;
}
// The Calculator's "=" key, lying on (x, y): an orange key cap with its "=".
function eqKey(x, y, C, rot = -8) {
  return `<g transform="translate(${x},${y}) rotate(${rot})"><path d="M-22,0 L-19,-15 H19 L22,0 Z" fill="${C.rust}" stroke="${C.ink}" stroke-width="3.5" stroke-linejoin="round"/>` +
    `<rect x="-17" y="-24" width="34" height="11" fill="${C.orange}" stroke="${C.ink}" stroke-width="3.5"/><path d="M-7,-20.5 H7 M-7,-16.5 H7" stroke="${C.ink}" stroke-width="2"/></g>`;
}
// Speed lines under something that is bouncing.
function bounce(x, y, w, C) {
  return `<path d="M${x - w},${y} q${w * 0.25},-10 ${w * 0.5},0 M${x + w * 0.5},${y} q${w * 0.25},-10 ${w * 0.5},0" fill="none" stroke="${C.ink}" stroke-width="3.5" stroke-linecap="round"/>` +
    `<path d="M${x - w * 1.2},${y - 34} l-16,-6 M${x - w * 1.25},${y - 14} l-18,0 M${x + w * 1.2},${y - 34} l16,-6 M${x + w * 1.25},${y - 14} l18,0" stroke="${C.ink}" stroke-width="3" stroke-linecap="round"/>`;
}
// A gold trophy cup standing on (x, base), h tall (cup and foot, no plinth).
function cup(x, base, h, C, extra = "") {
  const k = h / 100;
  const P = (pts) => pts.map(([px, py]) => `${(x + px * k).toFixed(1)},${(base + py * k).toFixed(1)}`).join(" ");
  const gold = C.yellow, edge = C.orange;
  return `<polygon points="${P([[-30, 0], [30, 0], [24, -10], [-24, -10]])}" fill="${C.rust}" stroke="${C.ink}" stroke-width="${Math.max(2, 3 * k)}" stroke-linejoin="miter"/>` +
    `<polygon points="${P([[-8, -10], [8, -10], [5, -36], [-5, -36]])}" fill="${gold}" stroke="${C.ink}" stroke-width="${Math.max(2, 3 * k)}"/>` +
    `<path d="M${x - 34 * k},${base - 84 * k} q-22,0 -22,${16 * k} q0,${16 * k} ${22 * k},${22 * k} M${x + 34 * k},${base - 84 * k} q22,0 22,${16 * k} q0,${16 * k} -${22 * k},${22 * k}" fill="none" stroke="${C.ink}" stroke-width="${Math.max(3, 7 * k)}"/>` +
    `<path d="M${x - 34 * k},${base - 84 * k} q-22,0 -22,${16 * k} q0,${16 * k} ${22 * k},${22 * k} M${x + 34 * k},${base - 84 * k} q22,0 22,${16 * k} q0,${16 * k} -${22 * k},${22 * k}" fill="none" stroke="${gold}" stroke-width="${Math.max(1.5, 3.5 * k)}"/>` +
    `<polygon points="${P([[-40, -96], [40, -96], [30, -52], [10, -38], [-10, -38], [-30, -52]])}" fill="${gold}" stroke="${C.ink}" stroke-width="${Math.max(2, 3.5 * k)}" stroke-linejoin="miter"/>` +
    `<polyline points="${P([[22, -90], [16, -56], [6, -44]])}" fill="none" stroke="${edge}" stroke-width="${Math.max(1.5, 3 * k)}"/>` + extra;
}
// A price tag on a string hanging from (x, y), tilted.
function tag(K, x, y, s, text) {
  return `<g transform="translate(${x},${y}) scale(${s})">${K.props.priceTag({ text, angle: 30 })}</g>`;
}
// A folding wooden yardstick standing on (x, base) up to y top, with a flag card at the top.
function yardstick(x, base, top, flag, C, fs = 54) {
  let ticks = "";
  for (let y = base - 30; y > top; y -= 30) ticks += `<path d="M${x - 14},${y} h${(base - y) % 150 < 30 ? 14 : 8}" stroke="${C.ink}" stroke-width="2.4"/>`;
  let joints = "";
  for (let y = base - 150; y > top + 20; y -= 150) joints += `<circle cx="${x}" cy="${y}" r="6" fill="${C.cream}" stroke="${C.ink}" stroke-width="2.6"/>`;
  // the flag flies to the left of the stick (away from the trophy)
  const fw = flag.length * fs * 0.62 + 50, fx = x - 15, fy = top + 8;
  return `<rect x="${x - 15}" y="${top}" width="30" height="${base - top}" fill="#E7C98A" stroke="${C.ink}" stroke-width="4"/>` + ticks + joints +
    `<path d="M${fx},${fy} H${fx - fw} L${fx - fw + 24},${fy + fs * 0.75} L${fx - fw},${fy + fs * 1.5} H${fx} Z" fill="#FBF6E6" stroke="${C.ink}" stroke-width="4" stroke-linejoin="miter"/>` +
    num(fx - 16, fy + fs * 1.12, fs, flag, C.navy, "end");
}
// The hall's dark or lit marquee: a navy board with bulbs round it.
function marquee(x, y, w, h, lit, lines, C, size) {
  let bulbs = "";
  const n = Math.round((2 * w + 2 * h) / 46);
  for (let i = 0; i < n; i++) {
    const u = (i / n) * (2 * w + 2 * h);
    const [bx, by] = u < w ? [x + u, y] : u < w + h ? [x + w, y + u - w] : u < 2 * w + h ? [x + w - (u - w - h), y + h] : [x, y + h - (u - 2 * w - h)];
    bulbs += `<circle cx="${bx.toFixed(1)}" cy="${by.toFixed(1)}" r="8" fill="${lit ? C.yellow : "#5E5A50"}" stroke="${C.ink}" stroke-width="2.4"/>`;
  }
  const t = lines.map((l, i) => osw(x + w / 2, y + h / 2 + (i - (lines.length - 1) / 2) * size * 1.15 + size * 0.36, size, l, lit ? C.cream : "#3A4560")).join("");
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="${C.navy}" stroke="${C.ink}" stroke-width="5"/>` + t + bulbs;
}
// A wooden shelf from (x0, y0) to (x1, y1), a bracket under the high end and a snapped one dangling at the low end.
function shelf(x0, y0, x1, y1, C) {
  return `<polygon points="${x0},${y0} ${x1},${y1} ${x1},${y1 + 20} ${x0},${y0 + 20}" fill="#9A6A3E" stroke="${C.ink}" stroke-width="4" stroke-linejoin="miter"/>` +
    `<path d="M${x1 - 60},${y1 + 20} v60 l50,-60" fill="none" stroke="${C.ink}" stroke-width="9"/><path d="M${x1 - 60},${y1 + 20} v60 l50,-60" fill="none" stroke="${C.slate}" stroke-width="4"/>` +
    `<path d="M${x0 + 60},${y0 + 60} v26 l-20,22 M${x0 + 60},${y0 + 86} l24,6" fill="none" stroke="${C.ink}" stroke-width="9"/><path d="M${x0 + 60},${y0 + 60} v26 l-20,22 M${x0 + 60},${y0 + 86} l24,6" fill="none" stroke="${C.slate}" stroke-width="4"/>`;
}
// The three small cups, piled at the low end of the shelf (the bed-net cup with its net and its sleeper).
function cups(K, x, y, h, C, tilt) {
  const net = (cx, cb) => {
    const k = h / 100;
    return `<path d="M${cx - 44 * k},${cb - 92 * k} q${44 * k},-${70 * k} ${88 * k},0" fill="#FBF6E6" fill-opacity="0.55" stroke="${C.ink}" stroke-width="${Math.max(1.5, 2.5 * k)}"/>` +
      `<path d="M${cx - 30 * k},${cb - 120 * k} l${60 * k},${28 * k} M${cx + 30 * k},${cb - 120 * k} l-${60 * k},${28 * k} M${cx},${cb - 128 * k} v${36 * k}" stroke="${C.ink}" stroke-width="${Math.max(1, 1.4 * k)}"/>` +
      `<circle cx="${cx}" cy="${cb - 100 * k}" r="${11 * k}" fill="#C98F62" stroke="${C.ink}" stroke-width="${Math.max(1.2, 2 * k)}"/><path d="M${cx - 6 * k},${cb - 101 * k} q3,3 5,0 M${cx + 2 * k},${cb - 101 * k} q3,3 5,0" fill="none" stroke="${C.ink}" stroke-width="${Math.max(1, 1.6 * k)}"/>`;
  };
  const germ = (cx, cb) => `<g transform="translate(${cx},${cb}) scale(${(h / 100) * 1.1},${(h / 100) * 0.3})">${K.props.germ({ mood: "dead" })}</g>`;
  const syringe = (cx, cb) => {
    const k = h / 100;
    return `<g transform="translate(${cx + 52 * k},${cb - 70 * k}) rotate(-20)"><rect x="${-6 * k}" y="${-30 * k}" width="${12 * k}" height="${44 * k}" fill="#FBF6E6" stroke="${C.ink}" stroke-width="${2.5 * k}"/><path d="M0,${14 * k} v${18 * k}" stroke="${C.ink}" stroke-width="${2 * k}"/><path d="M${-10 * k},${-34 * k} h${20 * k}" stroke="${C.ink}" stroke-width="${4 * k}"/></g>`;
  };
  const w = h * 0.72;
  return `<g transform="rotate(${tilt} ${x} ${y})">` +
    germ(x + w * 1.7, y) + cup(x + w * 1.7, y - h * 0.06, h, C) +
    cup(x + w * 0.85, y, h, C, syringe(x + w * 0.85, y)) +
    cup(x, y, h, C, net(x, y)) + "</g>";
}
// The giant treaty trophy on its plinth and dolly, standing on the floor at (x, floor); hp: plinth height;
// stemTop, bowlTop: where the stem ends and the bowl's rim is (y, canvas px); w: the bowl's half width at the rim.
function trophy(x, floor, hp, stemTop, bowlTop, w, C, plate, plateSize) {
  const deck = floor - 22, pt = deck - hp, pw = w * 0.62;
  const wheels = [-pw * 0.8, pw * 0.8].map((dx) => `<circle cx="${x + dx}" cy="${floor - 8}" r="15" fill="${C.slate}" stroke="${C.ink}" stroke-width="4"/><circle cx="${x + dx}" cy="${floor - 8}" r="5" fill="${C.cream}"/>`).join("");
  const dolly = `<rect x="${x - pw - 30}" y="${deck}" width="${2 * pw + 60}" height="16" fill="${C.rust}" stroke="${C.ink}" stroke-width="4"/>` + wheels;
  const plinth = `<rect x="${x - pw}" y="${pt}" width="${2 * pw}" height="${hp}" fill="#5C3B24" stroke="${C.ink}" stroke-width="5"/>` +
    `<rect x="${x - pw + 10}" y="${pt}" width="${2 * pw - 20}" height="14" fill="#7A5634" stroke="${C.ink}" stroke-width="3"/>` +
    `<rect x="${x - pw * 0.72}" y="${pt + hp * 0.32}" width="${pw * 1.44}" height="${hp * 0.36}" fill="${C.yellow}" stroke="${C.ink}" stroke-width="4"/>` +
    num(x, pt + hp * 0.5 + plateSize * 0.36, plateSize, plate, C.ink);
  const sw0 = pw * 0.55, sw1 = w * 0.12, knot = stemTop + (pt - stemTop) * 0.45;
  const stem = `<polygon points="${x - sw0},${pt} ${x + sw0},${pt} ${x + sw1},${knot} ${x - sw1},${knot}" fill="${C.yellow}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    `<polygon points="${x - sw1 * 2.2},${knot} ${x + sw1 * 2.2},${knot} ${x + sw1 * 1.4},${knot - 40} ${x - sw1 * 1.4},${knot - 40}" fill="${C.yellow}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    `<polygon points="${x - sw1 * 1.1},${knot - 40} ${x + sw1 * 1.1},${knot - 40} ${x + sw1 * 0.8},${stemTop} ${x - sw1 * 0.8},${stemTop}" fill="${C.yellow}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    `<path d="M${x + sw0 * 0.6},${pt - 6} L${x + sw1 * 0.6},${knot + 6}" stroke="${C.orange}" stroke-width="5"/>`;
  const bh = stemTop - bowlTop;
  const bowl = `<polygon points="${x - w},${bowlTop} ${x + w},${bowlTop} ${x + w * 0.78},${bowlTop + bh * 0.62} ${x + w * 0.3},${stemTop} ${x - w * 0.3},${stemTop} ${x - w * 0.78},${bowlTop + bh * 0.62}" fill="${C.yellow}" stroke="${C.ink}" stroke-width="6" stroke-linejoin="miter"/>` +
    `<polyline points="${x + w * 0.6},${bowlTop + 20} ${x + w * 0.5},${bowlTop + bh * 0.6} ${x + w * 0.2},${stemTop - 20}" fill="none" stroke="${C.orange}" stroke-width="7"/>` +
    `<rect x="${x - w - 8}" y="${bowlTop - 10}" width="${2 * w + 16}" height="22" fill="${C.yellow}" stroke="${C.ink}" stroke-width="6"/>`;
  const handle = (s) => {
    const a = `M${x + s * w * 0.9},${bowlTop + bh * 0.12} q${s * w * 0.55},0 ${s * w * 0.55},${bh * 0.25} q0,${bh * 0.25} -${s * w * 0.4},${bh * 0.36}`;
    return `<path d="${a}" fill="none" stroke="${C.ink}" stroke-width="${Math.max(14, w * 0.16)}"/><path d="${a}" fill="none" stroke="${C.yellow}" stroke-width="${Math.max(6, w * 0.09)}"/>`;
  };
  return handle(-1) + handle(1) + bowl + stem + dolly + plinth;
}
// A tan field under a cream sky, the horizon at y h.
function field(h) {
  return `<rect width="1920" height="${h}" fill="${SKY}"/><rect y="${h}" width="1920" height="${1080 - h}" fill="${FIELD}"/><rect y="${h}" width="1920" height="10" fill="${FIELD2}"/>`;
}

export default {
  "the-math-title"(H, id) {
    const { K, C } = H;
    const cx = 960, cy = 300, rx = 200, ry = 62;
    const orbits = [0, 60, -60].map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = [[0, 0.5], [60, 2.6], [-60, 4.6]].map(([a, th]) => {
      const r = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return H.at(cx + ex * Math.cos(r) - ey * Math.sin(r), cy + ex * Math.sin(r) + ey * Math.cos(r) - 6, 0.62, K.money("war", 0));
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    const word = (x, y, size, t) =>
      `<text x="${x + size * 0.04}" y="${y + size * 0.06}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${size}" fill="${C.deep}">${t}</text>` +
      `<text x="${x}" y="${y}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${size}" fill="${C.cream}" stroke="${C.cream}" stroke-width="${size * 0.03}" stroke-linejoin="round">${t}</text>`;
    // the Calculator behind MATH, only its display and eyes over the tops of the letters
    const calc = `<defs><clipPath id="${id}-peek"><rect x="0" y="0" width="1920" height="712"/></clipPath></defs>` +
      `<g clip-path="url(#${id}-peek)">${H.at(1010, 812, 1.35, K.props.calculator({ display: "0", mood: "worried" }))}</g>` +
      `<path d="M1112,596 q8,12 4,20 q-8,4 -12,-4 q-2,-8 8,-16 Z" fill="${C.cyan}" stroke="${C.ink}" stroke-width="2.5"/><path d="M1094,604 l-10,-8 M1100,594 l-4,-12" stroke="${C.cream}" stroke-width="3" stroke-linecap="round"/>`;
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus + calc + word(960, 572, 100, "THE") + word(960, 842, 200, "MATH");
    return { svg, alt: "The period title card: THE MATH in cream on navy under the atom emblem with its three running papers; the Calculator's display and worried eyes peek up over the top of MATH, a bead of sweat flying off it." };
  },

  "host-remembers"(H, id) {
    const { K, C } = H;
    const front = mug(610, 790, C) +
      H.at(948, 772, 0.92, K.props.calculator({ display: "212", mood: "smug" })) + bounce(948, 786, 30, C);
    const svg = H.host("happy-smile", "presenting", front);
    return { svg, alt: "Wishonia at her lectern, presenting; her coffee mug on the left end of the lectern and the Calculator on the right end, 212 on its display, bouncing on its toes like a prize fighter with a smug look." };
  },

  "quadrillion-equation"(H, id) {
    const { K, C } = H;
    // the mountain of plain green money behind the field
    const mtn = [[560, 640], [760, 470], [900, 330], [990, 290], [1080, 320], [1230, 450], [1380, 560], [1520, 640]];
    const mpts = mtn.map((p) => p.join(",")).join(" ");
    let bills = "";
    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 16; c++) {
        const x = 560 + c * 64 + (r % 2) * 32, y = 300 + r * 40, a = ((r * 7 + c * 13) % 5) * 9 - 18;
        bills += `<g transform="translate(${x},${y}) rotate(${a}) scale(0.62)">${K.money("plain", 0).replace('class="legs"', 'class="legs" opacity="0"')}</g>`;
      }
    }
    const mountain = `<defs><clipPath id="${id}-mtn"><polygon points="${mpts}"/></clipPath></defs>` +
      `<polygon points="${mpts}" fill="${C.money}" stroke="${C.ink}" stroke-width="6" stroke-linejoin="miter"/>` +
      `<g clip-path="url(#${id}-mtn)">${bills}</g><polygon points="${mpts}" fill="none" stroke="${C.ink}" stroke-width="6" stroke-linejoin="miter"/>`;
    // the fallen zeros, heaped on the bundle at the mountain's foot, its legs kicking out
    // a tidy pyramid of nine zeros (4, 3, 2), each tilted a little, with the commas lying about
    const zeros = [[1560, 870, -8], [1640, 872, 6], [1720, 870, -4], [1800, 872, 9], [1600, 790, 12], [1680, 788, -10], [1760, 792, 5], [1640, 708, -6], [1720, 706, 14]]
      .map(([x, y, a]) => `<g transform="translate(${x},${y}) rotate(${a})">${num(0, 0, 118, "0", C.navy)}</g>`).join("") +
      `<g transform="translate(1866,872) rotate(70)">${num(0, 0, 90, ",", C.navy)}</g><g transform="translate(1508,872) rotate(-60)">${num(0, 0, 90, ",", C.navy)}</g><g transform="translate(1690,620) rotate(20)">${num(0, 0, 90, ",", C.navy)}</g>`;
    // the bundle's corner and its stick legs, kicking out of the front of the pile
    const legs = `<g transform="translate(1530,846) rotate(-16)"><rect x="-40" y="-14" width="56" height="30" fill="${C.money}" stroke="${C.ink}" stroke-width="4"/><path d="M-30,-14 v30 M-20,-14 v30" stroke="${C.moneyDark}" stroke-width="2"/></g>` +
      `<path d="M1500,858 l-52,-44 l-20,0 M1508,870 l-62,-4 l-12,14" fill="none" stroke="${C.ink}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>` +
      `<path d="M1420,800 l14,-12 M1404,828 l-14,-6 M1412,886 l-12,10" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>`;
    const dollar = `<g transform="translate(250,846) rotate(-78)">${num(0, 0, 120, "$", C.navy)}</g>`;
    const number = num(196, 220, 168, "7,530,000 : 1", C.navy, "start");
    const svg = field(620) + mountain + number + dollar + legs + zeros;
    return { svg, alt: "The math-field plate pulled back: a mountain of plain green money under the cream sky, 7,530,000 : 1 stamped in the sky over it; the fallen dollar sign lies on the ground at the left, and at the mountain's foot a heap of fallen zeros buries the campaign's little bundle, only its stick legs kicking out." };
  },

  "calculator-scream"(H, id) {
    const { K, C } = H;
    // the tape of zeros: spooling out of the display, heaped on the lectern top and hanging over its front
    const tapeD = "M936,656 C1010,640 1040,700 1000,744 C968,782 1060,792 1046,830 L1040,1080";
    const tape = `<path d="${tapeD}" fill="none" stroke="${C.ink}" stroke-width="34" stroke-linejoin="round"/><path d="${tapeD}" fill="none" stroke="#FBF6E6" stroke-width="27" stroke-linejoin="round"/>` +
      `<path d="M860,790 q30,-26 60,0 q30,-26 60,0" fill="none" stroke="${C.ink}" stroke-width="30"/><path d="M860,790 q30,-26 60,0 q30,-26 60,0" fill="none" stroke="#FBF6E6" stroke-width="23"/>` +
      [[1050, 870], [1047, 920], [1044, 970], [1041, 1020], [1010, 720], [1030, 676]].map(([x, y]) => osw(x, y + 8, 20, "000", C.navy, "middle", `transform="rotate(84 ${x} ${y})"`)).join("");
    const smoke = `<path d="M890,640 q-16,-22 0,-40 q16,-18 0,-38 M960,628 q-14,-20 0,-36 q14,-16 0,-32" fill="none" stroke="#7A7468" stroke-width="7" stroke-linecap="round" opacity="0.8"/>`;
    const front = mug(610, 790, C) + tape + H.at(905, 790, 0.95, K.props.calculator({ mood: "scream" })) + smoke;
    const svg = H.host("happy-smile", "hands-hips", front);
    return { svg, alt: "Wishonia at her lectern, hands on hips, unbothered; on the right end of the lectern the Calculator screams, ERROR on its display, shake lines and a sweat drop, a paper tape of zeros spooling out of it and spilling over the lectern's front, smoke curling off it." };
  },

  "greatest-hits-trophies"(H, id) {
    const { K, C } = H;
    const wall = `<rect width="1920" height="1080" fill="#E2CE9C"/><rect y="690" width="1920" height="140" fill="#C9A46A"/><rect y="684" width="1920" height="12" fill="${C.rust}"/>` +
      `<rect y="830" width="1920" height="250" fill="#8C6440"/>` + [0, 1, 2, 3].map((i) => `<path d="M0,${862 + i * 56} H1920" stroke="#6E4C2F" stroke-width="3"/>`).join("") +
      `<path d="M0,830 H1920" stroke="${C.ink}" stroke-width="4"/>`;
    const mq = marquee(110, 250, 560, 150, false, ["GREATEST HITS", "IN NOT DYING"], C, 46);
    const sh = shelf(120, 612, 640, 520, C);
    const cupsSvg = cups(K, 175, 606, 78, C, -10);
    const ys = yardstick(820, 830, -10, "9,200×", C, 66);
    const tr = trophy(1250, 830, 210, 420, -40, 260, C, "1% TREATY", 38);
    const tiny = tag(K, 1112, 742, 0.45, "2¢");
    const sci = H.at(1650, 830 - 100 * 2.3, 2.3, K.cast("scientist", { look: "left", mood: "eager", arms: [[-80, -100], [-70, -96]], holdL: null, holdR: null }));
    const shake = `<path d="M1010,846 l-14,10 M1060,850 l-6,14 M1450,846 l14,10 M1400,850 l6,14" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>`;
    const svg = wall + mq + sh + cupsSvg + ys + tr + tiny + sci + shake;
    return { svg, alt: "The hall of greatest hits: the giant 1% TREATY trophy on its dolly, its bowl running out of the top of the picture, the Scientist behind it; a yardstick beside it runs up out of the picture flagged 9,200x; at the left, under a dark marquee, the snapped shelf tilts and the three small gold cups lie piled at its low end." };
  },

  "one-percent-chance"(H, id) {
    const { K, C } = H;
    const wall = `<rect width="1920" height="1080" fill="#E2CE9C"/><rect y="720" width="1920" height="130" fill="#C9A46A"/><rect y="714" width="1920" height="10" fill="${C.rust}"/>` +
      `<rect y="850" width="1920" height="230" fill="#8C6440"/>` + [0, 1, 2, 3].map((i) => `<path d="M0,${880 + i * 56} H1920" stroke="#6E4C2F" stroke-width="3"/>`).join("") +
      `<path d="M0,850 H1920" stroke="${C.ink}" stroke-width="4"/>`;
    const mq = marquee(50, 430, 380, 104, true, ["GREATEST HITS", "IN NOT DYING"], C, 32) +
      `<g transform="rotate(-6 240 430)"><rect x="130" y="404" width="220" height="44" fill="#FBF6E6" stroke="${C.ink}" stroke-width="4"/>${osw(240, 437, 30, "PREVIOUS", C.war)}</g>`;
    const sh = shelf(70, 640, 430, 578, C);
    const cupsSvg = cups(K, 108, 636, 48, C, -10);
    const ys = yardstick(560, 850, 250, "92.1×", C, 60);
    const tr = trophy(760, 850, 120, 560, 290, 140, C, "1% TREATY", 18);
    // the gauge on its pole, the needle hauled down to 1%, and the charred pessimist hanging on it
    const gx = 1300, gy = 330, gs = 2.4;
    const gauge = `<rect x="${gx - 9}" y="${gy}" width="18" height="${850 - gy}" fill="${C.slate}" stroke="${C.ink}" stroke-width="4"/>` +
      `<rect x="${gx - 60}" y="838" width="120" height="16" fill="${C.slate}" stroke="${C.ink}" stroke-width="4"/>` +
      H.at(gx, gy, gs, K.props.gauge({ mount: "dial", value: 0.01, window: "1%", zones: [[0.8, 1, C.war]] }).replace('class="gauge-needle"', 'class="gauge-needle" opacity="0"'));
    // the needle, bent down past the rim by his weight: from the hub, 0 at lower left, 240 degrees of sweep
    const a = ((-120 + 240 * 0.01) * Math.PI) / 180, hubX = gx, hubY = gy - 62 * gs, R = 84 * gs;
    const tipX = hubX + R * Math.sin(a) - 10, tipY = hubY - R * Math.cos(a) + 40;
    const needle = `<path d="M${hubX},${hubY} Q${hubX + R * 0.6 * Math.sin(a)},${hubY - R * 0.6 * Math.cos(a)} ${tipX},${tipY}" fill="none" stroke="${C.ink}" stroke-width="15" stroke-linecap="round"/>` +
      `<path d="M${hubX},${hubY} Q${hubX + R * 0.6 * Math.sin(a)},${hubY - R * 0.6 * Math.cos(a)} ${tipX},${tipY}" fill="none" stroke="${C.war}" stroke-width="8" stroke-linecap="round"/>` +
      `<circle cx="${hubX}" cy="${hubY}" r="13" fill="${C.yellow}" stroke="${C.ink}" stroke-width="4"/>`;
    const o = { kind: "shirt", tone: 1, colorHex: "#8E8A7A", hat: "bowler", mood: "flat", charred: true, look: "left", arms: [[150, 178], [-150, -178]], build: { hs: 0.95, legs: 1.05, tw: 0.92 } };
    const rig = K.rig(o), hk = 2.0;
    const hx = (rig.hand[0][0] + rig.hand[1][0]) / 2, hy = (rig.hand[0][1] + rig.hand[1][1]) / 2;
    const man = H.at(tipX - hx * hk, tipY + 6 - hy * hk, hk, K.person(o));
    const smoke = `<path d="M${tipX - 30},${tipY - 30} q-12,-20 0,-36 q12,-16 0,-32 M${tipX + 26},${tipY - 24} q-12,-18 0,-32" fill="none" stroke="#7A7468" stroke-width="6" stroke-linecap="round" opacity="0.8"/>`;
    const cx = tipX + 10, cy = tipY - 150;
    const cloud = `<path d="M${cx - 110},${cy + 30} q-10,-50 40,-56 q14,-44 64,-36 q30,-34 70,0 q50,-6 50,40 q30,10 16,52 Z" fill="#8F94A0" stroke="${C.ink}" stroke-width="5" stroke-linejoin="round"/>` +
      `<path d="M${cx - 10},${cy + 34} l-22,44 h22 l-16,46" fill="none" stroke="${C.yellow}" stroke-width="8" stroke-linejoin="miter"/>` +
      [-70, -30, 40, 80].map((dx, i) => `<path d="M${cx + dx},${cy + 40 + (i % 2) * 8} l-6,22" stroke="${C.cyan}" stroke-width="4" stroke-linecap="round"/>`).join("");
    const svg = wall + mq + sh + cupsSvg + ys + tr + gauge + needle + man + smoke + cloud;
    return { svg, alt: "The hall pulled back: the shrunken 1% TREATY trophy, its top now in the picture, still towering over the tiny cups piled on the tilted shelf under the lit marquee and its PREVIOUS strip; the yardstick folded down to its top, flagged 92.1x; beside it a charred, smoking pessimist hangs on the gauge's needle at 1% under his own raincloud." };
  },

  "calculator-returns"(H, id) {
    const { K, C } = H;
    // the Calculator (scale 1.3) rising behind the lectern's top edge: its display (y 691 to 721) and face show
    const k = 1.3, cx = 930, base = 790 + 76 * k;
    const dTop = base - 140 * k, dBot = base - 117 * k;
    const peek = `<defs><clipPath id="${id}-lid"><rect x="0" y="0" width="1920" height="792"/></clipPath></defs>` +
      `<g clip-path="url(#${id}-lid)">${H.at(cx, base, k, K.props.calculator({ display: "92.1", mood: "scared" }))}` +
      // a crack across the display's left end, and a strip of tape over it at a slant (the digits still show)
      `<path d="M${cx - 50 * k},${dTop + 4} l14,10 l-6,8 l16,6" fill="none" stroke="${C.cream}" stroke-width="2.6"/>` +
      `<g transform="rotate(-34 ${cx - 38 * k} ${(dTop + dBot) / 2})"><rect x="${cx - 38 * k - 40}" y="${(dTop + dBot) / 2 - 9}" width="80" height="18" fill="#E9D9A6" fill-opacity="0.9" stroke="${C.ink}" stroke-width="2.6"/></g></g>` +
      `<path d="M${cx + 70 * k},${dTop - 6} l16,-10 M${cx + 74 * k},${dTop + 18} l18,-2 M${cx - 62 * k},${dTop - 6} l-16,-10 M${cx - 66 * k},${dTop + 18} l-18,-2" stroke="${C.ink}" stroke-width="3.5" stroke-linecap="round"/>`;
    const front = mug(610, 790, C) + H.at(700, 790, 1.6, eqKey(0, 0, C)) + peek;
    const svg = H.host("sideeye-closed", "idle", front);
    return { svg, alt: "Wishonia at her lectern side-eyes the camera; the Calculator's \"=\" key lies by her mug, and the Calculator peeks up over the lectern's right edge, a strip of tape across its cracked display reading 92.1, its scared mouth trembling open." };
  },
};
