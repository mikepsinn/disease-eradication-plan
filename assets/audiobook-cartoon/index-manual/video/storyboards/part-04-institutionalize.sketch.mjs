// Sketches for storyboards/part-04-institutionalize.md: each scene's key moment on a 1920 x 1080 frame, drawn with
// the production art (kit.js, film.js and the props library) in the film look of Part 2: host shots on the studio
// set (H.host), plates drawn as the camera frames them at that moment. Nothing important below y 900.

// ── The recurring humans ──
// The patient (the part's spine): a mustard shirt; in a straitjacket he wears cream canvas with tan straps.
const PATIENT = { tone: 1, outfit: "shirt", color: 3 };
const CANVAS = "#E9DFC6", STRAP = "#B9935E";
// Part 2's hungry human (compositions/scenes/part-02/host-closes.html, MAN).
const HUNGRY = { kind: "shirt", head: "long", hairStyle: "short", tone: 2, color: 2, look: "left", build: { tw: 0.72, legs: 1.18, th: 1.12, neck: 1.6, hs: 0.95, nose: 1.5 } };

const copy = (a, b) => Object.assign({}, a, b || {});
const f1 = (n) => (+n).toFixed(1);

// A person with its feet on ground y at x, scale k (KIT.person is drawn with its feet at y 100).
function man(H, o, x, gy, k, extra = "") {
  return H.at(x, gy - 100 * k, k, H.K.person(o) + extra);
}
// The patient in his straitjacket (person units): the person in canvas with folded arms, two straps and buckles.
function jacketed(H, o = {}) {
  const { K } = H;
  const p = copy(PATIENT, copy({ colorHex: CANVAS, arms: [[52, 104], [-52, -104]] }, o));
  const R = K.rig(p), sx = R.shoulder[1][0] + 4, y1 = R.shoulder[0][1] + 22, y2 = R.hipY - 12;
  const strap = (y) => `<path d="M${f1(-sx)},${f1(y)} L${f1(sx)},${f1(y - 2)} L${f1(sx)},${f1(y + 7)} L${f1(-sx)},${f1(y + 9)} Z" fill="${STRAP}" stroke="${H.C.line}" stroke-width="2.2"/>` +
    `<rect x="${f1(sx * 0.35)}" y="${f1(y - 1)}" width="9" height="10" fill="${H.C.yellow}" stroke="${H.C.line}" stroke-width="2"/>`;
  return K.person(p) + strap(y1) + strap(y2);
}
// A crayon line: two passes of a waxy stroke, slightly apart.
function crayon(d, col, w = 7) {
  return `<path d="${d}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" opacity="0.88"/>` +
    `<path d="${d}" transform="translate(1.6,1.2)" fill="none" stroke="${col}" stroke-width="${w * 0.45}" stroke-linecap="round" stroke-linejoin="round" opacity="0.5"/>`;
}
// A crayon stick figure (the patient's drawings), feet at (x, y), h tall.
function crayonGuy(x, y, h, col, pose = "stand") {
  const hr = h * 0.13, hy = y - h + hr, ny = hy + hr, hip = y - h * 0.42;
  const arms = pose === "shrug" ? `M${x - h * 0.28},${ny + h * 0.02} L${x - h * 0.16},${ny + h * 0.16} L${x},${ny + h * 0.12} L${x + h * 0.16},${ny + h * 0.16} L${x + h * 0.28},${ny + h * 0.02}` : `M${x - h * 0.22},${ny + h * 0.3} L${x},${ny + h * 0.1} L${x + h * 0.22},${ny + h * 0.3}`;
  return crayon(`M${x - hr},${hy} a${hr},${hr} 0 1,0 ${2 * hr},0 a${hr},${hr} 0 1,0 ${-2 * hr},0 M${x},${ny} L${x},${hip} M${x - h * 0.18},${y} L${x},${hip} L${x + h * 0.18},${y} ${arms}`, col, h * 0.045);
}

// ── The host's lectern props (16:9: the reading top's edge at y 790, x 540 to 980) ──
function mug(H, x, y) {
  const { C } = H, ink = C.line;
  return `<g transform="translate(${x},${y})"><path d="M18,-44 q16,0 16,14 q0,14 -16,14" fill="none" stroke="${ink}" stroke-width="7"/><path d="M18,-44 q16,0 16,14 q0,14 -16,14" fill="none" stroke="${C.cream}" stroke-width="3"/>` +
    `<path d="M-20,-54 H22 L18,0 H-16 Z" fill="${C.rust}" stroke="${ink}" stroke-width="4.4" stroke-linejoin="miter"/><path d="M-19,-44 H21" stroke="${C.cream}" stroke-width="5"/>` +
    `<path d="M-6,-62 q-6,-10 0,-18 q6,-8 0,-18 M8,-62 q-6,-10 0,-18" fill="none" stroke="${C.cream}" stroke-width="3" opacity="0.8"/></g>`;
}
function caseFile(H, x, y) {
  const { C } = H, ink = C.line;
  return `<g transform="translate(${x},${y})"><path d="M-92,0 L-84,-16 H76 L88,0 Z" fill="#D9B46A" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/>` +
    `<path d="M-62,-16 L-58,-24 H-22 L-18,-16 Z" fill="#D9B46A" stroke="${ink}" stroke-width="3"/><path d="M-70,-8 H40" stroke="${ink}" stroke-width="2" opacity="0.6"/></g>`;
}
function lecternProps(H) {
  return caseFile(H, 640, 800) + mug(H, 920, 798);
}

// ── A butterfly net: the hoop's center (hx, hy), r its radius, tilt (deg), bag hanging below, and its pole from (px, py).
function net(H, id, px, py, hx, hy, r, tilt, sag = 1.6) {
  const { C } = H, ink = C.line;
  const bag = `M${-r},0 Q${-r * 0.8},${r * sag} 0,${r * sag * 1.25} Q${r * 0.8},${r * sag} ${r},0`;
  let mesh = "";
  for (let i = -3; i <= 3; i++) mesh += `M${f1(i * r * 0.26)},${f1(-r * 0.05)} Q${f1(i * r * 0.18)},${f1(r * sag * 0.8)} 0,${f1(r * sag * 1.2)} `;
  for (let j = 1; j <= 4; j++) { const yy = r * sag * j * 0.25, ww = r * (1 - j * 0.18); mesh += `M${f1(-ww)},${f1(yy)} Q0,${f1(yy + r * 0.12)} ${f1(ww)},${f1(yy)} `; }
  return `<path d="M${px},${py} L${hx + Math.cos((tilt * Math.PI) / 180) * r},${hy + Math.sin((tilt * Math.PI) / 180) * r}" stroke="${ink}" stroke-width="16" stroke-linecap="round"/>` +
    `<path d="M${px},${py} L${hx + Math.cos((tilt * Math.PI) / 180) * r},${hy + Math.sin((tilt * Math.PI) / 180) * r}" stroke="${C.tan}" stroke-width="10" stroke-linecap="round"/>` +
    `<g transform="translate(${hx},${hy}) rotate(${tilt})"><path d="${bag}" fill="#F7F1E0" fill-opacity="0.5" stroke="${ink}" stroke-width="3.4"/><path d="${mesh}" fill="none" stroke="${ink}" stroke-width="1.6" opacity="0.7"/>` +
    `<ellipse cx="0" cy="0" rx="${r}" ry="${r * 0.22}" fill="none" stroke="${ink}" stroke-width="8"/><ellipse cx="0" cy="0" rx="${r}" ry="${r * 0.22}" fill="none" stroke="${C.yellow}" stroke-width="3.5"/></g>`;
}

// ── The padded cell's wall and floor (canvas px; the floor line at y fy) ──
function cell(H, id, fy) {
  const { C } = H;
  return `<defs><pattern id="${id}-quilt" width="96" height="96" patternUnits="userSpaceOnUse"><rect width="96" height="96" fill="#EFE4C6"/>` +
    `<path d="M0,48 L48,0 L96,48 L48,96 Z" fill="none" stroke="#D5C397" stroke-width="3"/><circle cx="48" cy="0" r="5" fill="#C9B07E"/><circle cx="0" cy="48" r="5" fill="#C9B07E"/><circle cx="96" cy="48" r="5" fill="#C9B07E"/><circle cx="48" cy="96" r="5" fill="#C9B07E"/>` +
    `<path d="M48,8 L88,48" stroke="#FFF8E6" stroke-width="3" opacity="0.7"/></pattern>` +
    `<pattern id="${id}-pad" width="120" height="40" patternUnits="userSpaceOnUse"><rect width="120" height="40" fill="#DCCB9E"/><path d="M0,20 H120 M60,0 V20 M0,20 V40" stroke="#C4AF7E" stroke-width="3"/></pattern></defs>` +
    `<rect width="1920" height="1080" fill="url(#${id}-quilt)"/><rect y="${fy}" width="1920" height="${1080 - fy}" fill="url(#${id}-pad)"/><rect y="${fy - 6}" width="1920" height="10" fill="#B99D68"/>`;
}
// The steel cell door, standing on the floor at x (its left edge), h tall; the window holds `inWindow` (canvas px).
function cellDoor(H, id, x, fy, w, h, inWindow = "") {
  const { C } = H, ink = C.line, top = fy - h, wx = x + w * 0.28, ww = w * 0.44, wy = top + h * 0.14, wh = h * 0.2;
  return `<rect x="${x - 18}" y="${top - 18}" width="${w + 36}" height="${h + 18}" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` +
    `<rect x="${x}" y="${top}" width="${w}" height="${h}" fill="${C.peri}" stroke="${ink}" stroke-width="5"/>` +
    `<path d="M${x + w - 8},${top + 8} V${fy - 8}" stroke="${C.orange}" stroke-width="4"/>` +
    [0.1, 0.9].map((u) => `<circle cx="${x + w * u}" cy="${top + h * 0.06}" r="5" fill="${ink}"/><circle cx="${x + w * u}" cy="${fy - h * 0.06}" r="5" fill="${ink}"/>`).join("") +
    `<defs><clipPath id="${id}-win"><rect x="${wx}" y="${wy}" width="${ww}" height="${wh}"/></clipPath></defs>` +
    `<rect x="${wx}" y="${wy}" width="${ww}" height="${wh}" fill="#1D2338"/><g clip-path="url(#${id}-win)">${inWindow}</g>` +
    [1, 2, 3].map((i) => `<path d="M${wx + (ww * i) / 4},${wy} V${wy + wh}" stroke="${C.slate}" stroke-width="6"/>`).join("") +
    `<rect x="${wx}" y="${wy}" width="${ww}" height="${wh}" fill="none" stroke="${ink}" stroke-width="5"/>` +
    `<rect x="${x + w * 0.25}" y="${top + h * 0.55}" width="${w * 0.5}" height="${h * 0.05}" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>`;
}

export default {
  // ── 1 · the period title card ──
  "institutionalize-title"(H, id) {
    const { K, C } = H, ink = C.line;
    const E = { cx: 960, cy: 300, rx: 200, ry: 62 };
    let emblem = [0, 60, -60].map((a) => `<ellipse cx="${E.cx}" cy="${E.cy}" rx="${E.rx}" ry="${E.ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${E.cx} ${E.cy})"/>`).join("");
    [0, 60, -60].forEach((a, i) => {
      const th = i * 2.1 + 0.7, ex = E.rx * Math.cos(th), ey = E.ry * Math.sin(th), r = (a * Math.PI) / 180;
      emblem += H.at(f1(E.cx + ex * Math.cos(r) - ey * Math.sin(r)), f1(E.cy + ex * Math.sin(r) + ey * Math.cos(r) - 6), 0.62, K.money("war", i % 2));
    });
    emblem += `<circle cx="${E.cx}" cy="${E.cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${E.cx - 9}" cy="${E.cy - 9}" r="8" fill="${C.yellow}"/>`;
    // the heading: cream Fraunces with an ink outline and a drop shadow, as the card draws it
    const word = (x, y, size, text, anchor = "middle", sx = 1) => {
      const a = `text-anchor="${anchor}" font-family="Fraunces" font-weight="900" font-size="${size}"`;
      return `<g transform="translate(${x},${y}) scale(${sx},1)"><text x="${f1(size * 0.05)}" y="${f1(size * 0.065)}" ${a} fill="${C.ink}" stroke="${C.ink}" stroke-width="${f1(size * 0.05)}">${text}</text>` +
        `<text x="0" y="0" ${a} fill="${C.cream}" stroke="${C.ink}" stroke-width="${f1(size * 0.05)}" paint-order="stroke">${text}</text></g>`;
    };
    // INSTITUTIONALIZE, squashed to fit by its two straps; YOU after it
    const S = 150, inst = 9.881 * S * 0.9, x0 = 960 - (inst + 0.28 * S + 2.157 * S) / 2, base = 790;
    const strap = (x) => `<path d="M${x - 26},${base - S * 0.86} L${x + 18},${base - S * 0.9} L${x + 26},${base + 26} L${x - 18},${base + 30} Z" fill="${CANVAS}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/>` +
      `<path d="M${x - 16},${base - S * 0.8} L${x + 18},${base + 18}" stroke="${STRAP}" stroke-width="3" stroke-dasharray="9 7"/>` +
      `<rect x="${x - 21}" y="${base - S * 0.42}" width="42" height="34" fill="none" stroke="${C.yellow}" stroke-width="7"/><rect x="${x - 21}" y="${base - S * 0.42}" width="42" height="34" fill="none" stroke="${ink}" stroke-width="2" transform="translate(0,0)"/><path d="M${x},${base - S * 0.42} V${base - S * 0.42 + 34}" stroke="${ink}" stroke-width="4"/>`;
    const oX = x0 + inst + 0.28 * S + (0.673 + 0.379) * S, oY = base - 0.35 * S;
    const eyes = [-1, 1].map((s) => `<ellipse cx="${f1(oX + s * 11)}" cy="${f1(oY)}" rx="9" ry="13" fill="#FBF6E6" stroke="${ink}" stroke-width="2"/><circle cx="${f1(oX + s * 11 - 4)}" cy="${f1(oY + 1)}" r="4.2" fill="${ink}"/>`).join("");
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + emblem +
      word(960, 600, 80, "WHAT TO DO WHEN THEY TRY TO") +
      word(x0, base, S, "INSTITUTIONALIZE", "start", 0.9) + strap(x0 + inst * 0.3) + strap(x0 + inst * 0.72) +
      word(x0 + inst + 0.28 * S, base, S, "YOU", "start") + eyes;
    return { svg, alt: "The period title card on navy under the atom, whose electrons are running war-seal papers: WHAT TO DO WHEN THEY TRY TO, then INSTITUTIONALIZE squashed by two buckled straitjacket straps, and YOU with a pair of eyes in its O looking left." };
  },

  // ── 2 · host: the net falls short ──
  "net-falls-short"(H, id) {
    const front = lecternProps(H) + net(H, id, 1990, 250, 1215, 545, 80, 62, 1.5);
    return { svg: H.host("smirk-closed", "arms-crossed", front), alt: "Wishonia at her lectern, arms crossed and smirking, mug and case file on the lectern; a butterfly net on a long pole reaches in from the right edge and droops, well short of her." };
  },

  // ── 3 · plate living-room: the TV news chars its viewers ──
  "butterfly-net"(H, id) {
    const { K, C } = H, ink = C.line, FY = 860;
    // the TV, drawn big at the left, showing the mushroom cloud over the weather map's little town
    const screen = `<rect x="-70" y="-140" width="96" height="96" fill="#F6E7B8"/><path d="M-70,-62 Q-40,-72 -10,-64 Q10,-60 26,-66 V-40 H-70 Z" fill="${C.money}" stroke="${ink}" stroke-width="1.5"/>` +
      `<g transform="translate(-22,-62) scale(0.13)">${K.nuke()}</g>` + `<circle cx="10" cy="-124" r="6" fill="${C.yellow}" stroke="${ink}" stroke-width="1.2"/>`;
    const tv = H.at(370, FY, 3.2, K.props.tvSet({}).replace("<!--tv-screen-->", screen));
    // the sofa, in profile, facing the TV; four charred viewers on it
    const sofa = `<path d="M880,${FY} V${FY - 40} H1730 V${FY} Z" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M1660,${FY - 40} L1690,${FY - 330} L1760,${FY - 330} L1770,${FY - 40} Z" fill="${C.rust}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      `<path d="M860,${FY - 40} V${FY - 150} H1720 V${FY - 40} Z" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M840,${FY - 150} L850,${FY - 250} H930 L940,${FY - 150} Z" fill="${C.rust}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      [0, 1, 2, 3].map((i) => `<path d="M${960 + i * 190},${FY - 150} V${FY - 50}" stroke="${ink}" stroke-width="3" opacity="0.5"/>`).join("");
    const viewers = [
      { o: { tone: 0, outfit: "suit", color: 1, seed: 4 }, x: 1050 },
      { o: { tone: 2, outfit: "dress", color: 0, hair: 1, seed: 1 }, x: 1250 },
      { o: { tone: 1, outfit: "shirt", color: 2, seed: 7 }, x: 1440 },
      { o: { tone: 3, outfit: "dress", color: 3, hair: 1, seed: 6 }, x: 1610 },
    ];
    const k = 2.25, seatY = FY - 150;
    let people = "", wires = "";
    viewers.forEach((v, i) => {
      const o = copy(v.o, { charred: true, look: "left", arms: [[-14, -40], [-8, -30]], build: { legPose: [[86, 4], [94, 8]] } });
      const R = K.rig(o), gy = seatY + 100 * k - R.hipY * k - 0;
      // place the hips on the seat: the person's hipY sits at seatY
      const ty = seatY - R.hipY * k;
      const nod = i % 2 ? 6 : -4;
      people += `<g transform="translate(${v.x},${f1(ty)}) scale(${k})"><g transform="rotate(${nod * 0.3})">${K.person(o)}</g></g>`;
      const hx = v.x + (R.head[0] + 17) * k, hy = ty + (R.head[1] + 2) * k;
      wires += `<path d="M${640 - i * 6},${FY - 300 + i * 22} C${820 + i * 40},${FY + 60} ${hx + 90},${hy + 260} ${f1(hx)},${f1(hy)}" fill="none" stroke="${ink}" stroke-width="6"/>` +
        `<circle cx="${f1(hx)}" cy="${f1(hy)}" r="7" fill="${C.slate}" stroke="${ink}" stroke-width="3"/>`;
    });
    const glow = `<rect x="0" y="0" width="1920" height="1080" fill="#FFF6DC" opacity="0.12"/>`;
    // the picture window: outside, the patient on the corner under a street lamp with his 1% sign, the hedge behind him
    const W0 = [760, 120, 420, 290];
    const pat = copy(PATIENT, { arms: [[-150, -172], [150, 172]], mood: "smile" }), RP = K.rig(pat), pk = 1.05, ppx = 870, pgy = W0[1] + W0[3] - 8;
    const placard = `<g transform="translate(${f1(ppx + ((RP.hand[0][0] + RP.hand[1][0]) / 2) * pk)},${f1(pgy - 100 * pk + ((RP.hand[0][1] + RP.hand[1][1]) / 2) * pk)})">` +
      `<rect x="-44" y="-62" width="88" height="56" fill="#FBF6E6" stroke="${ink}" stroke-width="3.4"/><text x="0" y="-19" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="38" fill="${C.med}">1%</text></g>`;
    const outside = `<rect x="${W0[0]}" y="${W0[1]}" width="${W0[2]}" height="${W0[3]}" fill="#CFE0D8"/>` +
      `<rect x="${W0[0]}" y="${W0[1] + W0[3] - 40}" width="${W0[2]}" height="40" fill="#B8B0A0"/>` +
      `<path d="M${W0[0]},${W0[1] + W0[3] - 40} q30,-90 70,-60 q30,-60 70,-10 q40,-70 80,-8 q40,-50 70,10 q40,-60 70,0 q20,-20 60,10 V${W0[1] + W0[3] - 40} Z" fill="${C.moneyDark}" stroke="${ink}" stroke-width="3"/>` +
      `<path d="M1110,${W0[1] + W0[3] - 40} V${W0[1] + 40} q0,-14 -26,-14" fill="none" stroke="${ink}" stroke-width="7"/><path d="M1070,${W0[1] + 26} h28 l-6,14 h-16 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="2.4"/>` +
      man(H, pat, ppx, pgy, pk) + placard;
    const win = `<defs><clipPath id="${id}-win"><rect x="${W0[0]}" y="${W0[1]}" width="${W0[2]}" height="${W0[3]}"/></clipPath></defs><g clip-path="url(#${id}-win)">${outside}</g>` +
      `<rect x="${W0[0]}" y="${W0[1]}" width="${W0[2]}" height="${W0[3]}" fill="none" stroke="${C.cream}" stroke-width="14"/><rect x="${W0[0]}" y="${W0[1]}" width="${W0[2]}" height="${W0[3]}" fill="none" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M${W0[0] + W0[2] / 2},${W0[1]} V${W0[1] + W0[3]}" stroke="${C.cream}" stroke-width="10"/>`;
    const svg = `<rect width="1920" height="1080" fill="#E2C790"/><rect y="0" width="1920" height="70" fill="#D8B978"/>` +
      `<rect y="${FY - 6}" width="1920" height="${1080 - FY}" fill="#A9764B"/><rect y="${FY - 8}" width="1920" height="10" fill="${C.rust}"/>` +
      win + tv + wires + sofa + people + glow;
    return { svg, alt: "A 1950s living room: at the left a big console TV still showing a mushroom cloud over a weather map; on a sofa facing it, four viewers charred black and smoking, hair straight up, eyes blinking, wires running from the back of the TV into the backs of their heads, nodding along." };
  },

  // ── 4 · host: the hungry human thumps his chest light ──
  "less-crazy-goal"(H, id) {
    const { K, C } = H, ink = C.line;
    const k = 3.3, mx = 1390, gy = 1066;
    const o = copy(HUNGRY, { mood: "grin", light: "red", look: null, arms: [[20, 115], [150, 170]] });
    const R = K.rig(o);
    // the sandwich (Part 2's club sandwich, a bite out of its side), held up in the far hand
    const sand = (s) => `<defs><clipPath id="${id}-bite"><path d="M-60,-80 H6 V-31 Q16,-31 18,-22 Q7,-19 11,-10 Q3,-5 10,3 Q4,9 13,15 Q22,17 26,22 H60 V60 H-60 Z"/></clipPath></defs>` +
      `<g transform="scale(${s})"><g clip-path="url(#${id}-bite)"><rect x="-32" y="10" width="64" height="11" rx="7" fill="#E9C07A" stroke="${ink}" stroke-width="2.6"/>` +
      `<rect x="-31" y="0" width="62" height="7" fill="${C.war}" stroke="${ink}" stroke-width="2"/><rect x="-32" y="-10" width="64" height="10" rx="7" fill="#E9C07A" stroke="${ink}" stroke-width="2.6"/>` +
      `<rect x="-31" y="-17" width="62" height="7" fill="#D99A8F" stroke="${ink}" stroke-width="2"/><rect x="-32" y="-29" width="64" height="12" rx="7" fill="#E9C07A" stroke="${ink}" stroke-width="2.6"/></g>` +
      `<path d="M4,-29 L1,-50" stroke="${C.tan}" stroke-width="2.4"/><circle cx="1" cy="-52" r="5.5" fill="#7E8C3A" stroke="${ink}" stroke-width="2"/></g>`;
    const pocket = (x, s) => `<path d="M${f1(x)},${f1(R.hipY - 4)} l${13 * s},0 l${-3 * s},15 l${-9 * s},-3 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="2.2"/>`;
    const fist = `<circle cx="${f1(R.hand[0][0])}" cy="${f1(R.hand[0][1])}" r="7" fill="#A87B57" stroke="${ink}" stroke-width="2.4"/>`;
    const thump = [0, 1, 2].map((i) => `<path d="M${f1(R.hand[0][0] - 14 - i * 5)},${f1(R.hand[0][1] - 10 + i * 9)} l-9,${-3 + i * 3}" stroke="${ink}" stroke-width="2.2" stroke-linecap="round"/>`).join("");
    const guy = H.at(mx, gy - 100 * k, k, K.person(o) + pocket(R.hip[0][0] - 9, -1) + pocket(R.hip[1][0] + 9, 1) + fist + thump +
      H.at(f1(R.hand[1][0] + 4), f1(R.hand[1][1] - 12), 1, sand(0.55)));
    const front = lecternProps(H) + guy;
    return { svg: H.host("eyeroll-smile", "shrug", front), alt: "Wishonia at her lectern rolling her eyes and shrugging; beside her, Part 2's skinny hungry human, pockets turned out, grins at us with his mouth full, holding up the club sandwich and thumping his red chest light with his fist." };
  },

  // ── 5 · plate the-body: every light red at once ──
  "debug-37-trillion-cells"(H, id) {
    const { K, C } = H, ink = C.line;
    let cells = "";
    const rnd = K.rng(41);
    for (let r = -1; r < 7; r++) {
      for (let c = -1; c < 11; c++) {
        const cx = c * 200 + (r % 2 ? 100 : 0) + (rnd() - 0.5) * 30, cy = r * 165 + 60 + (rnd() - 0.5) * 24, s = 78 + rnd() * 16;
        const pts = [];
        for (let i = 0; i < 7; i++) { const a = (i / 7) * Math.PI * 2 + rnd() * 0.3, rr = s * (0.86 + rnd() * 0.22); pts.push(`${f1(cx + rr * Math.cos(a))},${f1(cy + rr * Math.sin(a) * 0.82)}`); }
        cells += `<polygon points="${pts.join(" ")}" fill="#F0C9A8" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
          `<ellipse cx="${f1(cx - s * 0.25)}" cy="${f1(cy + s * 0.12)}" rx="${f1(s * 0.24)}" ry="${f1(s * 0.18)}" fill="#D89C86" stroke="${ink}" stroke-width="3"/>` +
          `<circle cx="${f1(cx + s * 0.28)}" cy="${f1(cy - s * 0.2)}" r="22" fill="${C.war}" opacity="0.28"/><circle cx="${f1(cx + s * 0.28)}" cy="${f1(cy - s * 0.2)}" r="12" fill="${C.war}" stroke="${ink}" stroke-width="3.4"/>`;
      }
    }
    // the Scientist on her rope, wrench up, spinning; her to-do list unrolled off the bottom of the frame
    const so = K.castOpts("scientist", { arms: [[-170, -178], [-60, -150]], mood: "eager" });
    const R = K.rig(so), k = 1.9, sx = 960, sy = 360;
    const wrench = `<g transform="translate(${f1(R.hand[1][0])},${f1(R.hand[1][1])}) rotate(-20)"><rect x="-3" y="-34" width="7" height="34" fill="#9BA7B8" stroke="${ink}" stroke-width="2"/><path d="M-9,-46 a10,10 0 1,1 18,0 l-4,6 h-10 Z" fill="#9BA7B8" stroke="${ink}" stroke-width="2"/></g>`;
    const clip = `<g transform="translate(${f1(R.hand[0][0])},${f1(R.hand[0][1])})"><rect x="-12" y="-8" width="24" height="18" fill="#B98A55" stroke="${ink}" stroke-width="2"/></g>`;
    const sci = H.at(sx, sy, k, K.person(so) + wrench + clip);
    const ropeTop = `<path d="M${f1(sx + R.hand[0][0] * k)},0 V${f1(sy + R.hand[0][1] * k)}" stroke="${C.tan}" stroke-width="9"/><path d="M${f1(sx + R.hand[0][0] * k)},0 V${f1(sy + R.hand[0][1] * k)}" stroke="${ink}" stroke-width="2" stroke-dasharray="6 10"/>`;
    // the list: hangs from her clipboard hand down past the bottom edge
    const lx = sx + R.hand[0][0] * k, ly = sy + R.hand[0][1] * k + 14;
    let rows = "";
    for (let y = ly + 30; y < 1100; y += 34) rows += `<rect x="${f1(lx - 30)}" y="${f1(y)}" width="14" height="14" fill="none" stroke="${ink}" stroke-width="2.4"/><path d="M${f1(lx - 8)},${f1(y + 8)} H${f1(lx + 30)}" stroke="${ink}" stroke-width="2.4"/>`;
    const list = `<path d="M${f1(lx - 40)},${f1(ly)} H${f1(lx + 40)} V1100 H${f1(lx - 40)} Z" fill="#FBF5E4" stroke="${ink}" stroke-width="4"/>` + rows;
    const spin = [0, 1, 2].map((i) => `<path d="M${sx - 120 - i * 18},${sy + 40 + i * 40} q-30,40 0,80" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/><path d="M${sx + 150 + i * 18},${sy + 40 + i * 40} q30,40 0,80" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`).join("");
    const svg = `<rect width="1920" height="1080" fill="#B85E4C"/>` + cells + list + ropeTop + sci + spin;
    return { svg, alt: "Inside the body: a field of cells filling the frame, every cell's little check-engine light red at once; in the middle the tiny Scientist dangles on her rope, spinning round with her wrench up, and her to-do list hangs from her clipboard down off the bottom of the frame." };
  },

  // ── 6 · plate game-show: INSANE and the trapdoor ──
  "sane-insane-buzzer"(H, id) {
    const { K, C } = H, ink = C.line, FY = 820;
    // the stage: a navy curtain wall, the marquee with its two lamps, the host's desk, the podium on its open trapdoor
    let curtain = "";
    for (let x = 0; x < 1920; x += 80) curtain += `<path d="M${x},0 V${FY} M${x + 40},0 V${FY}" stroke="${x % 160 ? "#1B3A60" : "#0C2240"}" stroke-width="40"/>`;
    let bulbs = "";
    for (let x = 590; x <= 1330; x += 46) bulbs += `<circle cx="${x}" cy="76" r="9" fill="${C.cream}" stroke="${ink}" stroke-width="2.4"/><circle cx="${x}" cy="244" r="9" fill="${C.cream}" stroke="${ink}" stroke-width="2.4"/>`;
    const marquee = `<rect x="540" y="56" width="840" height="208" fill="${C.yellow}" stroke="${ink}" stroke-width="6"/>` + bulbs +
      `<text x="960" y="190" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="76" fill="${C.navy}">SANE OR INSANE?</text>`;
    const lamp = (x, text, col, lit) => (lit ? [0, 1, 2, 3, 4, 5, 6, 7].map((i) => { const a = (i * Math.PI) / 4; return `<path d="M${f1(x + Math.cos(a) * 160)},${f1(370 + Math.sin(a) * 76)} L${f1(x + Math.cos(a) * 205)},${f1(370 + Math.sin(a) * 104)}" stroke="${C.yellow}" stroke-width="9" stroke-linecap="round"/>`; }).join("") : "") +
      `<rect x="${x - 140}" y="320" width="280" height="100" rx="12" fill="${lit ? col : "#3A3F52"}" stroke="${ink}" stroke-width="6"/>` +
      `<text x="${x}" y="392" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="64" letter-spacing="3" fill="${lit ? C.cream : "#6E7488"}">${text}</text>`;
    const floor = `<rect y="${FY}" width="1920" height="${1080 - FY}" fill="${C.rust}"/><rect y="${FY - 8}" width="1920" height="14" fill="${C.tan}" stroke="${ink}" stroke-width="3"/>`;
    // the host's desk with the buzzer, the Politician behind it, his palm slapped down on it
    const DT = 640;
    const desk = `<path d="M150,${FY} L170,${DT} H560 L580,${FY} Z" fill="${C.slate}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/><path d="M190,${DT + 60} H545" stroke="${C.orange}" stroke-width="5"/>` +
      `<rect x="140" y="${DT - 20}" width="450" height="26" fill="${C.tan}" stroke="${ink}" stroke-width="5"/>`;
    const po = K.castOpts("politician", { look: "right", arms: [[-10, -4], [40, 52]] }), RPo = K.rig(po), pk = 2.3, pxp = 330;
    const hand = [pxp + RPo.hand[1][0] * pk, FY - 100 * pk + RPo.hand[1][1] * pk];
    const buzzer = `<rect x="${f1(hand[0] - 50)}" y="${DT - 48}" width="100" height="30" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><path d="M${f1(hand[0] - 44)},${DT - 48} Q${f1(hand[0])},${DT - 70} ${f1(hand[0] + 44)},${DT - 48} Z" fill="${C.war}" stroke="${ink}" stroke-width="4"/>` +
      [0, 1, 2].map((i) => `<path d="M${f1(hand[0] - 60 + i * 60)},${DT - 82 - (i === 1 ? 16 : 0)} l${-10 + i * 10},-22" stroke="${C.yellow}" stroke-width="6" stroke-linecap="round"/>`).join("");
    const pol = man(H, po, pxp, FY, pk);
    // the trapdoor open in the stage floor, its flap hanging down; the patient hanging in the air over it a beat, looking down
    const hole = `<path d="M1300,${FY + 14} H1640 L1610,${FY + 74} H1330 Z" fill="#0B0805" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M1330,${FY + 74} L1336,${FY + 230} H1604 L1610,${FY + 74} Z" fill="${C.tan}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/><path d="M1350,${FY + 150} H1590" stroke="${ink}" stroke-width="2" opacity="0.5"/>`;
    const fall = H.at(1470, FY - 60 - 100 * 2.3, 2.3, jacketed(H, { mood: "worried", look: "left" }));
    const lines = [0, 1, 2].map((i) => `<path d="M${1380 + i * 90},${FY - 20} v24" stroke="${C.cream}" stroke-width="5" stroke-linecap="round" opacity="0.8"/>`).join("");
    const podium = `<path d="M1700,${FY} L1715,${FY - 250} H1855 L1870,${FY} Z" fill="${C.peri}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
      `<rect x="1690" y="${FY - 272}" width="190" height="24" fill="${C.tan}" stroke="${ink}" stroke-width="5"/>` +
      `<text x="1785" y="${FY - 110}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="90" fill="${C.cream}">?</text>`;
    // the front row: the audience's heads
    let heads = "";
    for (let i = 0; i < 9; i++) heads += `<ellipse cx="${120 + i * 210}" cy="1080" rx="74" ry="80" fill="#0E1C33"/>`;
    const confetti = Array.from({ length: 40 }, (_, i) => `<rect x="${(i * 167) % 1880 + 20}" y="${(i * 97) % 300 + 280}" width="12" height="7" fill="${[C.yellow, C.cream, C.orange, C.cyan][i % 4]}" transform="rotate(${(i * 37) % 90} ${(i * 167) % 1880 + 26} ${(i * 97) % 300 + 283})"/>`).join("");
    const svg = `<rect width="1920" height="1080" fill="#0C2240"/>` + curtain + floor + marquee + lamp(760, "SANE", C.med, false) + lamp(1160, "INSANE", C.war, true) +
      pol + desk + buzzer + `<path d="M${f1(hand[0] - 18)},${f1(hand[1] - 6)} L${f1(hand[0] + 16)},${f1(hand[1] - 10)} L${f1(hand[0] + 24)},${f1(hand[1] + 4)} L${f1(hand[0] - 20)},${f1(hand[1] + 8)} Z" fill="#D9B48F" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/>` + hole + lines + fall + podium + confetti + heads;
    return { svg, alt: "A 1950s game-show stage under the marquee SANE OR INSANE?: the INSANE lamp lit, the grinning Politician with his palm slapped down on the big buzzer, the trapdoor in the stage floor hanging open, and the straitjacketed patient hanging in the air over the hole a beat, looking down." };
  },

  // ── 7 · host, pulled back: the studio light-years out in space ──
  "diagnostic-criteria"(H, id) {
    const { K, C } = H, ink = C.line;
    const rnd = K.rng(7);
    let stars = "";
    for (let i = 0; i < 140; i++) stars += `<circle cx="${f1(rnd() * 1920)}" cy="${f1(rnd() * 1080)}" r="${f1(0.8 + rnd() * 2.2)}" fill="${C.cream}" opacity="${f1(0.4 + rnd() * 0.6)}"/>`;
    for (let i = 0; i < 9; i++) stars += K.star(rnd() * 1920, rnd() * 860, 8 + rnd() * 10, i % 3 ? C.cream : C.yellow);
    // the studio, small: the whole host shot drawn into a lit box
    const bx = 1080, by = 170, s = 0.34, bw = 1920 * s, bh = 1080 * s;
    const box = `<defs><clipPath id="${id}-box"><rect x="${bx}" y="${by}" width="${bw}" height="${bh}"/></clipPath></defs>` +
      `<path d="M${bx},${by} L${bx + 40},${by - 34} H${bx + bw + 40} V${by + bh - 34} L${bx + bw},${by + bh} Z" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` +
      `<g clip-path="url(#${id}-box)"><g transform="translate(${bx},${by}) scale(${s})">${H.host("smirk-smile", "open-palms", lecternProps(H))}</g></g>` +
      `<rect x="${bx}" y="${by}" width="${bw}" height="${bh}" fill="none" stroke="${ink}" stroke-width="6"/>`;
    const earth = H.at(330, 860, 0.7, K.props.earthGlobe({ r: 110 }));
    const pole = net(H, id, 400, 720, 880, 520, 62, 12, 1.5);
    const svg = `<rect width="1920" height="1080" fill="#050A18"/>` + stars + box + pole + earth;
    return { svg, alt: "Pulled far back: the studio is a small lit box hanging in black starry space, Wishonia tiny at her lectern; far off at the bottom left a tiny Earth, and from it a butterfly net on an endless pole reaches up toward the studio and droops, far short." };
  },

  // ── 8 · plate padded-cell: what you tell the orderly ──
  "orderly-door-slot"(H, id) {
    const { K, C } = H, ink = C.line, FY = 900;
    const OE = K.castOpts("orderly", { look: "right" }), RO = K.rig(OE), ok = 2.4;
    const eyes = `<g transform="translate(${f1(272 - RO.eyes[0] * ok)},${f1(452 - RO.eyes[1] * ok)}) scale(${ok})">${K.person(OE)}</g>`;
    const door = cellDoor(H, id, 120, FY, 300, 600, eyes);
    // the crayon drawings: the little human beside his accidental birdhouse, then the carrier and the bomb, crossed out
    const birdhouse = crayon("M560,640 L610,585 L660,640 M570,640 V720 H650 V640 M598,668 a12,12 0 1,0 24,0 a12,12 0 1,0 -24,0 M610,720 V770", C.rust, 7) + crayon("M552,646 L668,632", C.navy, 5);
    const toolbox = crayon("M690,760 h60 v-28 h-60 z M705,732 v-10 h30 v10", C.navy, 5);
    const guy = crayonGuy(520, 772, 120, C.navy, "shrug");
    const carrier = crayon("M820,700 L860,760 H1260 L1300,700 Z M1040,700 V640 H1100 V700 M1060,640 V610 M880,692 l40,-10 l-6,12 M960,690 l40,-10 l-6,12", C.navy, 7);
    const bomb = crayon("M1340,700 a70,62 0 1,0 140,0 a70,62 0 1,0 -140,0 M1410,640 V604 M1400,604 h20 M1420,604 q20,-20 40,-6 M1352,700 L1316,670 M1468,700 L1504,670", C.navy, 7);
    const X = crayon("M800,580 L1520,800 M1520,580 L800,800", C.war, 12);
    // the patient, one arm out of the straitjacket, crayon up, facing his drawings
    const po = { look: "left", arms: [[52, 104], [-150, -150]] };
    const R = K.rig(copy(PATIENT, copy({ colorHex: CANVAS }, po)));
    const crayonStick = `<g transform="translate(${f1(R.hand[1][0])},${f1(R.hand[1][1])}) rotate(-30)"><rect x="-4" y="-26" width="8" height="26" fill="${C.war}" stroke="${ink}" stroke-width="2"/><path d="M-4,-26 L0,-34 L4,-26 Z" fill="${C.war}" stroke="${ink}" stroke-width="2"/></g>`;
    const sleeve = `<path d="M${f1(R.shoulder[0][0] + 6)},${f1(R.shoulder[0][1] + 30)} q-10,30 4,52 l6,-4 q-10,-20 -2,-44 Z" fill="${CANVAS}" stroke="${ink}" stroke-width="2"/>`;
    const patient = H.at(1640, FY - 100 * 2.4, 2.4, jacketed(H, po) + crayonStick + sleeve);
    const cup = `<g transform="translate(1440,${FY + 30})"><path d="M-22,-36 H22 L16,0 H-16 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="4"/><circle cx="-6" cy="-40" r="7" fill="${C.war}" stroke="${ink}" stroke-width="2"/><circle cx="8" cy="-41" r="7" fill="${C.med}" stroke="${ink}" stroke-width="2"/></g>`;
    const svg = cell(H, id, FY) + door + guy + birdhouse + toolbox + carrier + bomb + X + cup + patient;
    return { svg, alt: "The padded cell: at the left the steel door with the Orderly's eyes in its window; on the quilted wall the patient's crayon drawings, a little human shrugging beside a lopsided birdhouse, then a huge aircraft carrier and a nuclear bomb crossed out with one big red X; the patient stands at the right, one arm out of his straitjacket, a crayon in his hand, a pill cup pushed aside on the floor." };
  },

  // ── 9 · plate padded-cell: the war wheel turning ──
  "war-supply-chain"(H, id) {
    const { K, C } = H, ink = C.line, FY = 940, cx = 1120, cy = 470, RR = 350;
    // the rim: a paper-doll chain of tiny humans holding hands, heads outward
    let rim = crayon(`M${cx - RR},${cy} a${RR},${RR} 0 1,0 ${2 * RR},0 a${RR},${RR} 0 1,0 ${-2 * RR},0`, C.rust, 6);
    const N = 26;
    for (let i = 0; i < N; i++) {
      const a = (i / N) * 360, o = { tone: i % 4, outfit: ["shirt", "dress", "suit", "overalls"][i % 4], color: (i * 3) % 4, hair: i % 4 === 1 ? 1 : 0, seed: i, plain: true, arms: [[-88, -92], [88, 92]] };
      rim += `<g transform="rotate(${a} ${cx} ${cy}) translate(${cx},${cy - RR - 2}) scale(0.3) translate(0,-100)">${K.person(o)}</g>`;
    }
    // the spokes and the hub with its rosette
    let spokes = "";
    for (let i = 0; i < 8; i++) { const a = (i / 8) * Math.PI * 2 + 0.2; spokes += crayon(`M${cx},${cy} L${f1(cx + Math.cos(a) * RR)},${f1(cy + Math.sin(a) * RR)}`, C.rust, 5); }
    const rosette = `<g transform="translate(${cx},${cy})"><path d="M-22,20 L-40,110 L-14,94 L0,120 L4,30 Z M22,20 L40,110 L14,94 L0,120 L-4,30 Z" fill="${C.med}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/>` +
      Array.from({ length: 16 }, (_, i) => { const a = (i / 16) * Math.PI * 2; return `<circle cx="${f1(Math.cos(a) * 58)}" cy="${f1(Math.sin(a) * 58)}" r="18" fill="${C.med}" stroke="${ink}" stroke-width="3.4"/>`; }).join("") +
      `<circle r="56" fill="${C.cream}" stroke="${ink}" stroke-width="5"/><text y="18" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="50" fill="${C.navy}">1ST</text></g>`;
    // the gondolas: eight little colored scenes hanging from the rim
    const GON = [
      (x, y) => man(H, { tone: 3, outfit: "overalls", colorHex: C.peri, plain: true, arms: [[150, 170], [140, 160]], look: "right", hat: "hard" }, x - 10, y + 40, 0.42) + `<path d="M${x + 6},${y - 52} l30,-8 m-16,4 l6,34" stroke="${ink}" stroke-width="5"/>`,
      (x, y) => `<path d="M${x - 44},${y + 40} V${y - 30} L${x - 20},${y - 46} H${x + 4} V${y + 40} Z" fill="${C.rust}" stroke="${ink}" stroke-width="3"/><path d="M${x + 4},${y - 10} Q${x + 30},${y} ${x + 30},${y + 26}" stroke="${C.orange}" stroke-width="9" fill="none"/><rect x="${x + 14}" y="${y + 26}" width="36" height="14" fill="${C.yellow}" stroke="${ink}" stroke-width="2.4"/>`,
      (x, y) => H.at(x, y + 40, 0.2, K.props.factory({ label: "", smoke: false })),
      (x, y) => [0, 1, 2].map((i) => man(H, { tone: i, outfit: "suit", colorHex: "#5C6A3E", plain: true, arms: [[-10, -4], [150, 200 + (i === 2 ? -60 : 0)]], look: i === 2 ? "left" : "right" }, x - 34 + i * 34, y + 40, 0.34)).join(""),
      (x, y) => `<path d="M${x - 36},${y + 10} H${x + 36} L${x + 28},${y + 40} H${x - 28} Z" fill="${C.slate}" stroke="${ink}" stroke-width="3"/><path d="M${x - 20},${y + 4} q6,-14 0,-26 M${x},${y + 2} q6,-14 0,-26 M${x + 20},${y + 4} q6,-14 0,-26" stroke="${C.cream}" stroke-width="3" fill="none"/>`,
      (x, y) => `<path d="M${x - 46},${y + 20} H${x + 46} L${x + 34},${y + 40} H${x - 34} Z" fill="${C.slate}" stroke="${ink}" stroke-width="3"/><rect x="${x - 10}" y="${y}" width="20" height="20" fill="${C.cream}" stroke="${ink}" stroke-width="2.4"/>` +
        `<g transform="translate(${x + 10},${y - 34}) scale(0.5)"><path d="M-40,0 H40 L50,-6 L40,-12 H-40 Z M-10,-6 L-24,-30 H-10 L6,-6 Z" fill="${C.peri}" stroke="${ink}" stroke-width="5"/></g>`,
      (x, y) => `<rect x="${x - 6}" y="${y - 50}" width="52" height="64" fill="#FBF5E4" stroke="${ink}" stroke-width="3"/><text x="${x + 20}" y="${y - 22}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="13" fill="${C.war}">THEY</text><text x="${x + 20}" y="${y - 6}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="13" fill="${C.war}">DESERVE IT</text>` +
        man(H, K.castOpts("loudHuman", { look: "right" }), x - 30, y + 40, 0.4),
      (x, y) => H.at(x + 22, y + 40, 0.7, K.props.ballotBox({})) + man(H, K.castOpts("politician", { look: "right" }), x - 28, y + 40, 0.4),
    ];
    let gondolas = "";
    for (let i = 0; i < 8; i++) {
      const a = (i / 8) * Math.PI * 2 + 0.2, px = cx + Math.cos(a) * RR, py = cy + Math.sin(a) * RR, gx = px, gy = py + 80;
      gondolas += crayon(`M${f1(px)},${f1(py)} V${f1(gy - 54)}`, C.rust, 4) +
        `<path d="M${f1(gx - 62)},${f1(gy - 54)} H${f1(gx + 62)} L${f1(gx + 54)},${f1(gy + 44)} H${f1(gx - 54)} Z" fill="#FBF0D2" stroke="${C.rust}" stroke-width="5" stroke-linejoin="round"/>` +
        `<rect x="${f1(gx - 66)}" y="${f1(gy - 62)}" width="132" height="12" fill="${C.orange}" stroke="${ink}" stroke-width="3"/>` + GON[i](gx, gy);
    }
    // war bills running the rim
    let bills = "";
    for (let i = 0; i < 7; i++) { const a = (i / 7) * 360 + 18; bills += `<g transform="rotate(${a} ${cx} ${cy}) translate(${cx},${cy - RR + 30}) scale(0.5)">${K.money("war", i % 2)}</g>`; }
    // the door at the far left with the Orderly's head through the window, jaw dropped; the patient at the right
    const OH = K.castOpts("orderly", { look: "right", mood: "eager" }), RH = K.rig(OH), hk = 2.6;
    const door = cellDoor(H, id, 60, FY, 270, 560, "") +
      `<defs><clipPath id="${id}-thru"><rect x="40" y="300" width="420" height="270"/></clipPath></defs>` +
      `<g clip-path="url(#${id}-thru)"><g transform="translate(${f1(225 - RH.eyes[0] * hk)},${f1(470 - RH.eyes[1] * hk)}) scale(${hk})">${K.person(OH)}</g></g>`;
    const patient = H.at(1720, FY - 100 * 2.2, 2.2, jacketed(H, { look: "left", arms: [[-120, -150], [-52, -104]] }));
    const cal = `<g transform="translate(1640,260)">${crayon("M-50,-60 H50 V60 H-50 Z M-50,-30 H50", C.navy, 5)}</g>` +
      Array.from({ length: 6 }, (_, i) => `<rect x="${1560 + i * 40}" y="${340 + (i % 3) * 30}" width="40" height="34" fill="#FBF5E4" stroke="${C.navy}" stroke-width="3" transform="rotate(${-30 + i * 14} ${1580 + i * 40} ${357 + (i % 3) * 30})"/>`).join("");
    const svg = cell(H, id, FY) + door + spokes + rim + bills + gondolas + rosette + cal + patient;
    return { svg, alt: "Pulled back on the padded wall: the patient's war wheel turning, its rim a paper-doll chain of tiny humans holding hands with war bills running round it, eight gondolas alive in color (a miner, a furnace, the missile factory, a salute, soup, a ship and a plane, the THEY DESERVE IT poster, the ballot box), a 1ST rosette on the hub; at the left the Orderly's head through the door window, jaw dropped; a crayon calendar shedding pages." };
  },

  // ── 10 · plate padded-cell: the wheel goes dark ──
  "chain-goes-dark"(H, id) {
    const { K, C } = H, ink = C.line, FY = 920, cx = 1640, cy = 440, RR = 420;
    // the wheel, back to flat crayon and still, its left half in frame
    let wheel = crayon(`M${cx - RR},${cy} a${RR},${RR} 0 1,0 ${2 * RR},0 a${RR},${RR} 0 1,0 ${-2 * RR},0`, "#9C8E74", 6);
    for (let i = 0; i < 8; i++) {
      const a = (i / 8) * Math.PI * 2 + 0.2, px = cx + Math.cos(a) * RR, py = cy + Math.sin(a) * RR;
      wheel += crayon(`M${cx},${cy} L${f1(px)},${f1(py)}`, "#9C8E74", 4) + crayon(`M${f1(px)},${f1(py)} V${f1(py + 30)} M${f1(px - 60)},${f1(py + 30)} H${f1(px + 60)} L${f1(px + 52)},${f1(py + 120)} H${f1(px - 52)} Z`, "#9C8E74", 5);
      wheel += crayonGuy(px, py + 112, 70, "#9C8E74");
    }
    for (let i = 0; i < 30; i++) { const a = (i / 30) * Math.PI * 2; wheel += crayonGuy(cx + Math.cos(a) * (RR + 6), cy + Math.sin(a) * (RR + 6) + 18, 40, "#9C8E74"); }
    // frozen bills on the rim: still money green, mid-stride
    const bills = [200, 225, 245].map((deg, i) => { const a = (deg * Math.PI) / 180; return H.at(f1(cx + Math.cos(a) * RR), f1(cy + Math.sin(a) * RR - 26), 0.7, K.money("war", i % 2)); }).join("");
    // the crayon switch on OFF, the patient's finger on it
    const sw = `<g transform="translate(1010,560)">${crayon("M-46,-74 H46 V74 H-46 Z", C.navy, 6)}${crayon("M-9,-10 H9 V40 H-9 Z", C.navy, 5)}` +
      `<text x="0" y="-36" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="26" fill="${C.navy}" opacity="0.75">ON</text><text x="0" y="68" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="22" fill="${C.navy}" opacity="0.75">OFF</text></g>`;
    const po = { look: "left", arms: [[-104, -96], [-52, -104]] };
    const patient = H.at(1200, FY - 100 * 2.5, 2.5, jacketed(H, po));
    // the Orderly frozen half through the doorway, ducking under the frame, a fresh cup in his hand
    const od = K.castOpts("orderly", { look: "right", mood: "flat", holdR: "cup", arms: [[-6, -2], [70, 100]], build: { hs: 0.72, legs: 1.3, th: 1.2, neck: 2.4, armL: 1.25, hunch: 26 } });
    const doorFrame = `<rect x="60" y="${FY - 640}" width="330" height="640" fill="#101624" stroke="${ink}" stroke-width="6"/><rect x="40" y="${FY - 660}" width="370" height="24" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M390,${FY - 640} L470,${FY - 600} V${FY + 20} L390,${FY}" fill="${C.peri}" stroke="${ink}" stroke-width="5"/>`;
    const orderly = man(H, od, 250, FY, 3.3);
    const svg = cell(H, id, FY) + `<rect width="1920" height="1080" fill="#000" opacity="0.18"/>` + doorFrame + orderly + wheel + bills + sw + patient;
    return { svg, alt: "The padded cell after NOT: the war wheel back to flat gray crayon and still, its bills frozen mid-stride; the patient's finger on a crayon light switch flicked to OFF; at the left the Orderly frozen mid-step, ducking in under the door frame with a fresh pill cup." };
  },

  // ── 11 · plate rock-field: thousands of years of peace ──
  "centrifuge-vs-rocks"(H, id) {
    const { K, C } = H, ink = C.line, HZ = 600;
    // the sun streaking over again and again: a row of ghost suns along its arc
    let suns = "";
    for (let i = 0; i < 9; i++) { const a = Math.PI * (0.1 + i * 0.1), x = 960 - Math.cos(a) * 780, y = 600 - Math.sin(a) * 470; suns += `<circle cx="${f1(x)}" cy="${f1(y)}" r="46" fill="${C.yellow}" opacity="${f1(0.15 + i * 0.09)}"/>`; }
    suns += `<path d="M${960 - 780 * Math.cos(Math.PI * 0.1)},${600 - 470 * Math.sin(Math.PI * 0.1)} A780,470 0 0,1 ${960 + 780 * Math.cos(Math.PI * 0.1)},${600 - 470 * Math.sin(Math.PI * 0.1)}" fill="none" stroke="${C.orange}" stroke-width="5" stroke-dasharray="18 22" opacity="0.6"/>`;
    const rock = (x, y, w, h, col, shade) => `<path d="M${x - w / 2},${y} L${x - w * 0.44},${y - h * 0.62} L${x - w * 0.2},${y - h} L${x + w * 0.22},${y - h * 0.94} L${x + w * 0.48},${y - h * 0.5} L${x + w / 2},${y} Z" fill="${col}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
      `<path d="M${x + w * 0.22},${y - h * 0.94} L${x + w * 0.48},${y - h * 0.5} L${x + w / 2},${y} L${x + w * 0.2},${y} Z" fill="${shade}"/>`;
    const moss = (x, y, w) => Array.from({ length: 7 }, (_, i) => `<path d="M${x - w / 2 + i * (w / 6)},${y} l-8,-18 l10,8 l4,-16 l6,16 l8,-10 l-4,20 Z" fill="${C.money}" stroke="${ink}" stroke-width="2"/>`).join("");
    const flower = (x, y, col) => `<path d="M${x},${y} V${y - 30}" stroke="${C.moneyDark}" stroke-width="4"/>` + [0, 1, 2, 3, 4].map((i) => { const a = (i / 5) * Math.PI * 2; return `<circle cx="${f1(x + Math.cos(a) * 9)}" cy="${f1(y - 30 + Math.sin(a) * 9)}" r="7" fill="${col}" stroke="${ink}" stroke-width="1.6"/>`; }).join("") + `<circle cx="${x}" cy="${y - 30}" r="5" fill="${C.yellow}"/>`;
    const gray = rock(840, 820, 300, 230, "#9B9C95", "#7D7E78"), rust = rock(1180, 820, 260, 190, C.rust, "#6E3922");
    const nest = `<path d="M760,612 Q840,650 920,612 L908,628 Q840,662 772,628 Z" fill="#8C6440" stroke="${ink}" stroke-width="3.4"/>` +
      `<g transform="translate(860,590)"><path d="M-26,8 Q-30,-14 -6,-20 Q8,-34 22,-22 L36,-20 L24,-12 Q26,10 4,14 Z" fill="${C.cyan}" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/><circle cx="14" cy="-22" r="3" fill="${ink}"/></g>`;
    const heart = `<path d="M1010,560 c-20,-30 -60,-8 -40,22 l40,40 l40,-40 c20,-30 -20,-52 -40,-22 Z" fill="${C.war}" stroke="${ink}" stroke-width="4"/>`;
    // the counter on its post
    const digits = "348,203".split("").map((ch, i) => `<rect x="${1410 + i * 52}" y="300" width="46" height="70" rx="4" fill="#1E1B24"/><text x="${1433 + i * 52}" y="356" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="54" fill="${C.yellow}">${ch}</text>`).join("");
    const counter = `<path d="M1592,420 V830" stroke="${ink}" stroke-width="22"/><path d="M1592,420 V830" stroke="${C.tan}" stroke-width="12"/>` +
      `<rect x="1384" y="196" width="416" height="210" fill="${C.cream}" stroke="${ink}" stroke-width="6"/><rect x="1396" y="208" width="392" height="186" fill="none" stroke="${C.orange}" stroke-width="3"/>` +
      `<text x="1592" y="268" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="50" letter-spacing="3" fill="${C.navy}">DAYS OF PEACE</text>` + digits;
    const hat = `<g transform="translate(470,838) rotate(-18)"><path d="M-46,0 L-36,-34 L0,-48 L36,-34 L46,0 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/><path d="M-62,4 L-52,-6 H52 L62,4 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/></g>`;
    const grass = Array.from({ length: 24 }, (_, i) => `<path d="M${40 + i * 80},${880 + (i % 3) * 30} l6,-22 l6,22" fill="none" stroke="${C.moneyDark}" stroke-width="4"/>`).join("");
    const svg = `<rect width="1920" height="1080" fill="#EFE3C4"/>` + suns + `<rect y="${HZ}" width="1920" height="${1080 - HZ}" fill="#C8B07B"/><path d="M0,${HZ} H1920" stroke="#8E7A55" stroke-width="3"/>` +
      grass + counter + gray + moss(840, 598, 160) + rust + moss(1180, 640, 140) + flower(700, 830, C.cream) + flower(1330, 836, C.orange) + flower(1010, 846, C.cream) + nest + heart + hat;
    return { svg, alt: "An open field under a big sky, the sun streaking over again and again: a gray rock and a rust rock side by side, mossy and flowering, a bird nesting on the gray one, a little heart between them; a DAYS OF PEACE counter on a post reads 348,203; the Weapons Maker's hard hat lies in the grass." };
  },

  // ── 12 · host ending: the Rich Human burns the PDF ──
  "billionaire-pdf"(H, id) {
    const { K, C } = H, ink = C.line;
    const k = 3.0, x = 1460, gy = 1010;
    // the dented STOP sign, knocked flat on the floor behind him
    const oct = Array.from({ length: 8 }, (_, i) => { const a = (i / 8) * Math.PI * 2 + Math.PI / 8; return `${f1(Math.cos(a) * 110)},${f1(Math.sin(a) * 110)}`; }).join(" ");
    const stop = `<g transform="translate(1800,560) rotate(-34)"><path d="M0,110 V420" stroke="${ink}" stroke-width="20"/><path d="M0,110 V420" stroke="#9BA7B8" stroke-width="10"/><polygon points="${oct}" fill="${C.war}" stroke="${ink}" stroke-width="7"/>` +
      `<polygon points="${oct}" transform="scale(0.86)" fill="none" stroke="${C.cream}" stroke-width="6"/><text y="24" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="74" fill="${C.cream}">STOP</text><circle cx="-30" cy="-50" r="22" fill="#A63725" opacity="0.7"/></g>`;
    // the swivel chair, then the Rich Human in it, the sticker on his forehead, puffing the burning PDF
    const chair = `<path d="M${x - 140},${gy - 560} L${x - 120},${gy - 330} H${x + 120} L${x + 140},${gy - 560} Q${x},${gy - 610} ${x - 140},${gy - 560} Z" fill="${C.navy}" stroke="${ink}" stroke-width="6"/>` +
      `<path d="M${x - 120},${gy - 560} Q${x},${gy - 590} ${x + 120},${gy - 560}" fill="none" stroke="${C.orange}" stroke-width="4"/>` +
      `<rect x="${x - 160}" y="${gy - 330}" width="320" height="60" rx="10" fill="${C.navy}" stroke="${ink}" stroke-width="6"/><path d="M${x},${gy - 270} V${gy - 60}" stroke="${ink}" stroke-width="22"/>` +
      `<path d="M${x - 130},${gy - 20} L${x},${gy - 60} L${x + 130},${gy - 20}" fill="none" stroke="${ink}" stroke-width="14"/><circle cx="${x - 130}" cy="${gy - 12}" r="12" fill="${ink}"/><circle cx="${x + 130}" cy="${gy - 12}" r="12" fill="${ink}"/>`;
    const ro = K.castOpts("richHuman", { look: "left", arms: [[40, 150], [-20, -60]] });
    const R = K.rig(ro);
    const sticker = `<g transform="translate(${f1(R.head[0] + 2)},${f1(R.head[1] - 14)}) rotate(-8)"><rect x="-26" y="-7" width="52" height="14" fill="#FBF6E6" stroke="${ink}" stroke-width="1.6"/><text x="0" y="4" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="8.4" letter-spacing="0.4" fill="${C.war}">UNREALISTIC</text></g>`;
    // the rolled PDF in his hand at his mouth, burning at the far end
    const pdf = `<g transform="translate(${f1(R.mouth[0] - 6)},${f1(R.mouth[1] + 2)}) rotate(168)"><rect x="0" y="-4" width="38" height="8" fill="#FBF6E6" stroke="${ink}" stroke-width="1.6"/><text x="16" y="2.6" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="6" fill="${C.war}" transform="rotate(180 16 0)">PDF</text>${K.flames(40, 2, 0.13).replace('scale(0.13)', 'rotate(-90) scale(0.13)')}</g>`;
    const ring = `<ellipse cx="${f1(R.mouth[0] - 40)}" cy="${f1(R.mouth[1] - 40)}" rx="14" ry="9" fill="none" stroke="#B9B4AA" stroke-width="4"/><ellipse cx="${f1(R.mouth[0] - 58)}" cy="${f1(R.mouth[1] - 66)}" rx="10" ry="6" fill="none" stroke="#B9B4AA" stroke-width="3" opacity="0.7"/>`;
    const rich = H.at(x, gy - 100 * k - 230, k, K.person(ro) + sticker + pdf + ring);
    const front = lecternProps(H) + stop + chair + rich;
    return { svg: H.host("sideeye-closed", "arms-crossed", front), alt: "Wishonia at her lectern side-eyeing the camera, arms crossed; beside her the Rich Human in a navy swivel chair, an UNREALISTIC sticker on his forehead, puffing a burning rolled-up PDF like a second cigar and blowing a smoke ring; the dented STOP sign lies flat on the floor behind him." };
  },
};
