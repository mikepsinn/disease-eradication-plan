// Sketches for storyboards/part-06-leaders-arent-the-problem.md: each scene's key moment on a 1920 x 1080 frame,
// drawn with the production art (H.K: kit.js, film.js and the props library). The film look: host shots are the
// studio set (H.host); a plate frame is one framing of an illustrated plate as the camera sees it, on Part 2's
// plain field and road (compositions/scenes/part-02/money-loop.html). 16:9 only, no captions.

const GROUND = "#C8B07B", ROAD = "#EEE3C4", EDGE = "#B09363", DASH = "#C7AB78", SKIN = ["#F4E3CC", "#D9B48F", "#A87B57", "#6F4B33"];
const BONE = "#F1EAD6";
const f = (n) => n.toFixed(1);

// A person standing with its feet at (x, feet), k times person size (KIT.person is drawn with its feet at y 100).
function man(H, o, x, feet, k, extra = "") {
  return H.at(x, feet - 100 * k, k, H.K.person(o) + extra);
}
// A point in a person's own units, on the canvas.
function pt(x, feet, k, p) {
  return [x + p[0] * k, feet - 100 * k + p[1] * k];
}
// A road band along a path: the edge, the road and the dashed middle line.
function road(d, w, k = 1) {
  return `<path d="${d}" fill="none" stroke="${EDGE}" stroke-width="${(w + 14) * k}" stroke-linecap="butt"/>` +
    `<path d="${d}" fill="none" stroke="${ROAD}" stroke-width="${w * k}"/>` +
    `<path d="${d}" fill="none" stroke="${DASH}" stroke-width="${7 * k}" stroke-dasharray="${46 * k} ${54 * k}"/>`;
}
const field = (col = GROUND) => `<rect width="1920" height="1080" fill="${col}"/>`;
// A walking paper at (x, y), k times size; kind "war" | "med" | "plain".
function bill(H, kind, x, y, k, rot = 0, legs = 0) {
  return H.at(x, y, k, H.K.money(kind, legs), rot);
}
// A bill lying flat, seen from the side: a thin green slab (the 604 bar is a stack of these).
function slab(C, x, y, w, seal) {
  const s = seal === "med" ? `<path d="M${x + w - 22},${y + 2} v10 M${x + w - 27},${y + 7} h10" stroke="${C.cream}" stroke-width="2.4"/>` : "";
  return `<rect x="${x}" y="${y}" width="${w}" height="14" rx="2" fill="${C.money}" stroke="${C.line}" stroke-width="3"/>` +
    `<path d="M${x + 8},${y + 7} H${x + w - 34}" stroke="${C.moneyDark}" stroke-width="2"/><circle cx="${x + w - 22}" cy="${y + 7}" r="5" fill="${C.moneyDark}"/>` + s;
}
// The Democracy Dog's tail extras: tiny grinning skulls (corpses) or knocked-out disease blobs, along the tail's
// curve (dog units), and a war bill clamped in its teeth.
function tailPt(t) {
  const R = [46, -64], Q = [108, -150], E = [20, -134], u = 1 - t;
  return [u * u * R[0] + 2 * u * t * Q[0] + t * t * E[0], u * u * R[1] + 2 * u * t * Q[1] + t * t * E[1]];
}
function skull(C, x, y, r) {
  return `<g transform="translate(${f(x)},${f(y)})"><path d="M${-r * 0.5},${r * 0.9} L${-r * 0.9},${r * 2.2} M${r * 0.5},${r * 0.9} L${r * 0.9},${r * 2.2}" stroke="${BONE}" stroke-width="${r * 0.35}" stroke-linecap="round"/>` +
    `<path d="M${-r * 0.5},${r * 0.9} L${-r * 0.9},${r * 2.2} M${r * 0.5},${r * 0.9} L${r * 0.9},${r * 2.2}" stroke="${C.line}" stroke-width="${r * 0.12}" stroke-linecap="round" opacity="0.6"/>` +
    `<circle r="${r}" fill="${BONE}" stroke="${C.line}" stroke-width="${r * 0.22}"/><circle cx="${-r * 0.36}" cy="${-r * 0.1}" r="${r * 0.26}" fill="${C.line}"/><circle cx="${r * 0.36}" cy="${-r * 0.1}" r="${r * 0.26}" fill="${C.line}"/>` +
    `<path d="M${-r * 0.5},${r * 0.42} Q0,${r * 0.75} ${r * 0.5},${r * 0.42}" fill="none" stroke="${C.line}" stroke-width="${r * 0.16}" stroke-linecap="round"/></g>`;
}
function koBlob(C, x, y, r) {
  const bumps = [0, 1, 2, 3, 4, 5, 6, 7].map((i) => { const a = (i / 8) * Math.PI * 2; const rr = r * (i % 2 ? 0.86 : 1); return `${f(x + rr * Math.cos(a))},${f(y + rr * Math.sin(a))}`; }).join(" ");
  const X = (cx) => `<path d="M${f(cx - r * 0.22)},${f(y - r * 0.32)} l${f(r * 0.44)},${f(r * 0.44)} M${f(cx + r * 0.22)},${f(y - r * 0.32)} l${f(-r * 0.44)},${f(r * 0.44)}" stroke="${C.line}" stroke-width="${f(r * 0.14)}" stroke-linecap="round"/>`;
  return `<polygon points="${bumps}" fill="${C.peri}" stroke="${C.line}" stroke-width="${f(r * 0.18)}"/>` + X(x - r * 0.38) + X(x + r * 0.38) +
    `<path d="M${f(x - r * 0.3)},${f(y + r * 0.45)} h${f(r * 0.6)}" stroke="${C.line}" stroke-width="${f(r * 0.14)}"/>`;
}
// Steam / smoke puffs.
function puff(x, y, r, col = "#F6F1E4") {
  return `<g fill="${col}" stroke="#112845" stroke-width="3"><circle cx="${x}" cy="${y}" r="${r}"/><circle cx="${x - r * 0.8}" cy="${y + r * 0.3}" r="${r * 0.7}"/><circle cx="${x + r * 0.85}" cy="${y + r * 0.25}" r="${r * 0.75}"/></g>`;
}
// Motion lines.
function lines(C, pts, w = 4) {
  return pts.map(([x1, y1, x2, y2]) => `<path d="M${x1},${y1} L${x2},${y2}" stroke="${C.line}" stroke-width="${w}" stroke-linecap="round"/>`).join("");
}
// The Politician's office desk at the roadside, its top at y top, centered on x, w wide.
function desk(C, x, top, w) {
  const hw = w / 2;
  return `<rect x="${x - hw}" y="${top}" width="${w}" height="34" fill="#7A5634" stroke="${C.line}" stroke-width="5"/>` +
    `<rect x="${x - hw + 26}" y="${top + 34}" width="${w - 52}" height="600" fill="#8C6440" stroke="${C.line}" stroke-width="5"/>` +
    [0, 1, 2].map((i) => `<rect x="${x + hw - 230}" y="${top + 60 + i * 96}" width="170" height="80" fill="#9A7049" stroke="${C.line}" stroke-width="4"/><rect x="${x + hw - 162}" y="${top + 92 + i * 96}" width="34" height="10" rx="4" fill="${C.yellow}" stroke="${C.line}" stroke-width="2.5"/>`).join("") +
    `<path d="M${x - hw + 40},${top + 60} V${top + 380}" stroke="#6E4C2E" stroke-width="3"/>`;
}
// A big red button on a little box, standing on y 0, centered on x.
function redButton(C, x, y, k = 1) {
  return H0(x, y, k, `<rect x="-40" y="-26" width="80" height="26" fill="${C.slate}" stroke="${C.line}" stroke-width="4"/><path d="M-26,-26 Q-26,-56 0,-56 Q26,-56 26,-26 Z" fill="${C.war}" stroke="${C.line}" stroke-width="4"/><path d="M-14,-44 Q-8,-50 2,-50" stroke="#F3B9A6" stroke-width="4" fill="none" stroke-linecap="round"/>`);
}
function H0(x, y, k, inner, rot = 0) {
  return `<g transform="translate(${x},${y})${rot ? ` rotate(${rot})` : ""}${k !== 1 ? ` scale(${k})` : ""}">${inner}</g>`;
}
// A teacup and saucer, around (0, 0), about 34 wide.
function teacup(C) {
  return `<path d="M-14,-12 H14 L10,4 H-10 Z" fill="#FBF6E6" stroke="${C.line}" stroke-width="2.4"/><path d="M14,-8 q8,0 6,7 q-2,4 -8,2" fill="none" stroke="${C.line}" stroke-width="2.2"/>` +
    `<path d="M-6,-16 q-3,-5 0,-9 M2,-16 q3,-5 0,-9" fill="none" stroke="#FBF6E6" stroke-width="1.8" opacity="0.9"/>`;
}
// The costume: a pair of red horns on a headband, a set of plastic fangs and a pointed tail.
function horns(C) {
  return `<path d="M-46,0 Q-60,-40 -38,-78 Q-40,-40 -22,-8 Z" fill="${C.war}" stroke="${C.line}" stroke-width="4" stroke-linejoin="round"/>` +
    `<path d="M46,0 Q60,-40 38,-78 Q40,-40 22,-8 Z" fill="${C.war}" stroke="${C.line}" stroke-width="4" stroke-linejoin="round"/>` +
    `<path d="M-54,4 Q0,-26 54,4" fill="none" stroke="${C.line}" stroke-width="7"/>`;
}
function fangs(C) {
  return `<path d="M-34,0 Q0,-12 34,0 L28,10 Q0,2 -28,10 Z" fill="${C.war}" stroke="${C.line}" stroke-width="3"/>` +
    `<path d="M-24,6 L-18,30 L-12,6 Z M12,6 L18,30 L24,6 Z" fill="#FBF6E6" stroke="${C.line}" stroke-width="3" stroke-linejoin="round"/>`;
}
function devilTail(C) {
  return `<path d="M0,0 C30,-40 -20,-80 20,-120" fill="none" stroke="${C.line}" stroke-width="13" stroke-linecap="round"/><path d="M0,0 C30,-40 -20,-80 20,-120" fill="none" stroke="${C.war}" stroke-width="7" stroke-linecap="round"/>` +
    `<path d="M20,-120 L2,-136 L40,-150 L30,-112 Z" fill="${C.war}" stroke="${C.line}" stroke-width="4" stroke-linejoin="round"/>`;
}
// A gold star, around (x, y).
function goldStar(C, x, y, r) {
  const p = [];
  for (let i = 0; i < 10; i++) { const a = (Math.PI * i) / 5 - Math.PI / 2, rr = i % 2 ? r * 0.45 : r; p.push(`${f(x + rr * Math.cos(a))},${f(y + rr * Math.sin(a))}`); }
  return `<polygon points="${p.join(" ")}" fill="${C.yellow}" stroke="${C.line}" stroke-width="3" stroke-linejoin="round"/>`;
}
// A rosette with two ribbon tails and a word on its face, around (0, 0), about 120 across.
function rosette(C, text) {
  let scal = "";
  for (let i = 0; i < 16; i++) { const a = (i / 16) * Math.PI * 2; scal += `<circle cx="${f(52 * Math.cos(a))}" cy="${f(52 * Math.sin(a))}" r="14" fill="${C.war}" stroke="${C.line}" stroke-width="3"/>`; }
  return `<path d="M-22,30 L-44,118 L-26,106 L-14,124 L4,36 Z M22,30 L44,118 L26,106 L14,124 L-4,36 Z" fill="${C.med}" stroke="${C.line}" stroke-width="3.5" stroke-linejoin="round"/>` + scal +
    `<circle r="50" fill="${C.war}" stroke="${C.line}" stroke-width="3"/><circle r="40" fill="${C.cream}" stroke="${C.line}" stroke-width="3"/>` +
    `<text y="6" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="13" letter-spacing="0.5" fill="${C.line}">${text}</text>`;
}
// A halo, around (0, 0).
function halo(C, char) {
  return `<ellipse rx="58" ry="16" fill="none" stroke="${C.line}" stroke-width="16"/><ellipse rx="58" ry="16" fill="none" stroke="${char ? "#5A4E3A" : C.yellow}" stroke-width="9"/>`;
}

export default {
  // ── 1 · title card ──
  "leaders-title"(H, id) {
    const { K, C } = H;
    const atom = K.atom(960, 300, 230, C.cream);
    // three running papers on the orbits
    const on = (a, t) => { const rx = 230, ry = 230 * 0.31, x0 = rx * Math.cos(t), y0 = ry * Math.sin(t), r = (a * Math.PI) / 180; return [960 + x0 * Math.cos(r) - y0 * Math.sin(r), 300 + x0 * Math.sin(r) + y0 * Math.cos(r)]; };
    const bills = [[0, -2.2], [60, 1.1], [-60, 2.4]].map(([a, t]) => { const [x, y] = on(a, t); return bill(H, "war", x, y, 0.62, 0, 0.6); }).join("");
    // the flattened Politician under PROBLEM: his sleeve and hand waving a bill out from under the P, his pointed
    // shoes out from under the M
    const hand = H.at(404, 858, 1.5, `<path d="M40,0 L-36,-50 L-50,-34 L28,12 Z" fill="${C.slate}" stroke="${C.line}" stroke-width="3" stroke-linejoin="round"/>` +
        `<path d="M-36,-50 L-48,-62 L-62,-46 L-50,-34 Z" fill="#FBF6E6" stroke="${C.line}" stroke-width="2.6" stroke-linejoin="round"/>` +
        `<path d="M-50,-60 L-62,-84 L-58,-98 L-50,-96 L-48,-82 L-46,-104 L-38,-103 L-38,-80 L-30,-96 L-23,-92 L-34,-62 Z" fill="${SKIN[1]}" stroke="${C.line}" stroke-width="2.6" stroke-linejoin="round"/>` +
        H0(-56, -118, 0.42, K.money("war").replace('class="legs"', 'class="legs" opacity="0"'), -26)) +
      lines(C, [[296, 676, 278, 656], [334, 664, 330, 640], [272, 708, 248, 704]], 5);
    const shoes = `<path d="M1500,846 L1582,838 L1620,852 L1502,862 Z M1500,868 L1574,862 L1612,876 L1502,882 Z" fill="${C.line}" stroke="${C.cream}" stroke-width="3" stroke-linejoin="round"/>` +
      `<path d="M1524,846 l14,-3 M1524,868 l14,-3" stroke="#FBF6E6" stroke-width="3"/>`;
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + atom + bills +
      H.big(960, 640, 86, "WHY YOUR LEADERS AREN'T THE", "middle", C.cream) +
      hand + shoes + H.big(960, 852, 210, "PROBLEM", "middle", C.cream);
    return { svg, alt: "The navy period title card: the atom with three running war papers, WHY YOUR LEADERS AREN'T THE in small letters, and PROBLEM sitting heavily below; a Politician's sleeve and hand poke out from under the P, still waving a bill, and his pointed shoes stick out from under the M." };
  },

  // ── 2 · host: one guest with every ailment at once ──
  "two-billion-sick"(H, id) {
    const { K, C } = H;
    const k = 3.0, X = 1480, FEET = 1070;
    // the sick guest (the first everyday human of the part: record his options here)
    const o = { tone: 1, outfit: "shirt", color: 1, hair: 0, seed: 61, look: "left", light: "red", mood: "worried", arms: [[30, 20], [-8, -4]] };
    const R = K.rig(o), m = R.mouth, h = R.head, t = R.top, hd = R.hand[0];
    // the crutch under his arm
    let extra = `<path d="M${f(R.shoulder[0][0] - 6)},${f(R.shoulder[0][1] + 4)} L${f(hd[0] - 14)},${f(R.hipY + 60)}" stroke="${C.line}" stroke-width="7"/><path d="M${f(R.shoulder[0][0] - 6)},${f(R.shoulder[0][1] + 4)} L${f(hd[0] - 14)},${f(R.hipY + 60)}" stroke="${C.tan}" stroke-width="4"/><path d="M${f(R.shoulder[0][0] - 16)},${f(R.shoulder[0][1] + 2)} h22" stroke="${C.line}" stroke-width="6" stroke-linecap="round"/>`;
    // the jaw bandage, knotted on top
    const jaw = `M${f(h[0] - 15)},${f(t[1] + 4)} L${f(h[0] - 19)},${f(h[1] + 6)} Q${f(h[0] - 4)},${f(h[1] + 30)} ${f(h[0] + 14)},${f(h[1] + 10)} L${f(h[0] + 11)},${f(t[1] + 4)}`;
    extra += `<path d="${jaw}" fill="none" stroke="${C.line}" stroke-width="12" stroke-linejoin="round"/><path d="${jaw}" fill="none" stroke="#FBF6E6" stroke-width="8" stroke-linejoin="round"/>`;
    // the ice pack balanced on top, the bandage's knot poking out beside it
    const ix = t[0] + 4, iy = t[1] - 2;
    extra += `<path d="M${f(ix - 22)},${f(iy + 6)} Q${f(ix - 22)},${f(iy - 18)} ${f(ix)},${f(iy - 18)} Q${f(ix + 22)},${f(iy - 18)} ${f(ix + 22)},${f(iy + 6)} Z" fill="#9FB6C9" stroke="${C.line}" stroke-width="2.6"/><rect x="${f(ix - 5)}" y="${f(iy - 26)}" width="10" height="9" fill="${C.war}" stroke="${C.line}" stroke-width="2"/>` +
      `<path d="M${f(h[0] - 14)},${f(t[1] + 2)} q-12,-6 -14,-16 q8,0 14,16 Z" fill="#FBF6E6" stroke="${C.line}" stroke-width="2.2"/>`;
    // the thermometer in his mouth, its bulb in the red
    extra += `<path d="M${f(m[0])},${f(m[1])} L${f(m[0] - 24)},${f(m[1] - 7)}" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/><path d="M${f(m[0])},${f(m[1])} L${f(m[0] - 24)},${f(m[1] - 7)}" stroke="#FBF6E6" stroke-width="3" stroke-linecap="round"/><path d="M${f(m[0] - 6)},${f(m[1] - 2)} L${f(m[0] - 24)},${f(m[1] - 7)}" stroke="${C.war}" stroke-width="1.6" stroke-linecap="round"/><circle cx="${f(m[0] - 25)}" cy="${f(m[1] - 7)}" r="3" fill="${C.war}" stroke="${C.line}" stroke-width="1.4"/>`;
    const svg = H.host("sad-closed", "hand-chest", man(H, o, X, FEET, k, extra));
    return { svg, alt: "Wishonia at her lectern on the studio set; at her right one sick guest with every ailment at once: a thermometer in his mouth, its bulb in the red, an ice pack on his head, his jaw bandaged, leaning on a crutch, his chest light blinking red." };
  },

  // ── 3 · plate the-loop: the desk ──
  "politician-drinks-tea"(H, id) {
    const { K, C } = H;
    const k = 3.8, X = 1270, FEET = 1160;
    const POL = K.castOpts("politician", { look: "right", mood: "smug", arms: [[20, 110], [-6, 196]] });
    const R = K.rig(POL);
    const cupAt = pt(X, FEET, k, R.hand[1]);
    // the 604 bar: a stack of war papers from the field up out of the top of the frame
    let stack = "";
    for (let y = 846; y > -40; y -= 16) stack += slab(C, 330 + ((y / 16) % 2 ? 4 : 0), y, 250, "war");
    const flat = `<rect x="470" y="860" width="230" height="16" rx="3" fill="${C.money}" stroke="${C.line}" stroke-width="3.5"/><circle cx="676" cy="868" r="6" fill="${C.moneyDark}"/><path d="M676,864 v8 M672,868 h8" stroke="${C.cream}" stroke-width="2.2"/>` +
      `<path d="M700,866 L736,826" stroke="${C.line}" stroke-width="6" stroke-linecap="round"/><path d="M734,830 L740,738" stroke="${C.line}" stroke-width="4"/><path d="M740,740 L800,754 L742,776 Z" fill="#FBF6E6" stroke="${C.line}" stroke-width="3" stroke-linejoin="round"/>` +
      lines(C, [[776, 726, 792, 710], [810, 766, 830, 766]], 3);
    const costume = H.at(1330, 150, 1.5, horns(C), -14) + H.at(1590, 270, 1.4, fangs(C), 18) + H.at(1020, 320, 1.3, devilTail(C), -30) +
      lines(C, [[1230, 300, 1242, 260], [1430, 288, 1422, 248], [1560, 350, 1580, 320], [1040, 420, 1020, 390]], 4);
    const svg = field() +
      `<rect y="0" width="1920" height="86" fill="${ROAD}" opacity="0"/>` +
      stack + flat +
      man(H, POL, X, FEET, k) +
      H.at(cupAt[0] + 6, cupAt[1] - 4, k * 0.9, teacup(C)) +
      desk(C, 1270, 760, 820) + redButton(C, 1000, 762, 1.4) +
      costume;
    return { svg, alt: "Tight on the Politician at his office desk, pinky out, sipping a cup of tea and looking quite normal; above him a pair of red horns, a set of plastic fangs and a pointed tail drift up out of the frame; a big red button on the desk; at the left the 604 bar of war papers rises out of the top of the frame, and at its foot the one flattened medicine paper waves a tiny white flag." };
  },

  // ── 4 · plate the-loop: the dog's tail in its teeth ──
  "democracy-dog-loop"(H, id) {
    const { K, C } = H;
    const k = 3.7, X = 900, FEET = 840;
    const dog = K.props.democracyDog({ tail: "papers", seal: "war", mood: "eager" });
    // extras on the tail, in dog units: tiny grinning skeletons between the bills, and the tail's tip clamped in
    // its teeth (two more bills curling round to the mouth)
    let extra = [0.2, 0.4, 0.6, 0.8].map((t) => { const p = tailPt(t); return skull(C, p[0] + 3, p[1] + 9, 5.2); }).join("");
    extra += H0(6, -112, 0.34, K.money("war").replace('class="legs"', 'class="legs" opacity="0"'), 60) + H0(-6, -92, 0.3, K.money("war").replace('class="legs"', 'class="legs" opacity="0"'), 20);
    // the DEMOCRACY tag hanging from the collar
    extra += `<path d="M-30,-70 L-36,-52" stroke="${C.line}" stroke-width="1.6"/><g transform="translate(-37,-44) rotate(-8)"><rect x="-26" y="-9" width="52" height="18" rx="9" fill="${C.yellow}" stroke="${C.line}" stroke-width="2"/><text y="3.6" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="9.4" letter-spacing="0.3" fill="${C.line}">DEMOCRACY</text></g>`;
    const roadD = "M-100,820 H2020";
    const svg = field() + road(roadD, 320) +
      bill(H, "war", 1560, 812, 1.2, 0, 0.3) + bill(H, "war", 1720, 808, 1.2, 0, 0.7) + bill(H, "war", 1880, 812, 1.2, 0, 0.3) +
      H.at(X, FEET, k, dog + extra);
    return { svg, alt: "Close on the Democracy Dog running on the road with the tip of its own tail clamped in its teeth: the tail is a chain of war papers knotted with tiny grinning skeletons; its collar tag reads DEMOCRACY; war papers march past behind it." };
  },

  // ── 5 · plate the-loop: the whole ring, evil ──
  "loop-is-evil"(H, id) {
    const { K, C } = H;
    // the camera's wide view of the plate: plate (PX, PY) at the middle of the screen, scale s
    const s = 0.34, PX = -520, PY = -260;
    const v = (inner) => `<g transform="translate(${f(960 - PX * s)},${f(540 - PY * s)}) scale(${s})">${inner}</g>`;
    const S = 1.5, RR = 640, BOT = 800;
    const ring = `<circle r="${RR}" fill="none" stroke="${EDGE}" stroke-width="174"/><circle r="${RR}" fill="none" stroke="${ROAD}" stroke-width="160"/><circle r="${RR}" fill="none" stroke="${DASH}" stroke-width="7" stroke-dasharray="46 54"/>`;
    // the angry face in the infield, the fanged grin inside the bottom bend, the horns either side of the factory
    const face = `<path d="M-330,-300 L-110,-220 M330,-300 L110,-220" stroke="${C.line}" stroke-width="46" stroke-linecap="round"/>` +
      `<path d="M-300,-170 Q-200,-210 -110,-160 Q-200,-130 -300,-170 Z M300,-170 Q200,-210 110,-160 Q200,-130 300,-170 Z" fill="${C.war}" stroke="${C.line}" stroke-width="14"/>` +
      `<circle cx="-190" cy="-168" r="16" fill="${C.line}"/><circle cx="190" cy="-168" r="16" fill="${C.line}"/>` +
      `<path d="M-430,250 Q0,470 430,250" fill="none" stroke="${C.line}" stroke-width="22" stroke-linecap="round"/>` +
      [-300, -150, 0, 150, 300].map((x) => { const y = 250 + 220 * (1 - (x / 430) ** 2) * 0.98; return `<path d="M${x - 34},${f(y - 6)} L${x},${f(y + 70)} L${x + 34},${f(y - 6)} Z" fill="#FBF6E6" stroke="${C.line}" stroke-width="10" stroke-linejoin="round"/>`; }).join("");
    const hornL = H0(-560, -780, 4.2, `<path d="M-30,0 Q-50,-60 -10,-120 Q-14,-60 20,0 Z" fill="${C.war}" stroke="${C.line}" stroke-width="5" stroke-linejoin="round"/>`);
    const hornR = H0(560, -780, 4.2, `<path d="M30,0 Q50,-60 10,-120 Q14,-60 -20,0 Z" fill="${C.war}" stroke="${C.line}" stroke-width="5" stroke-linejoin="round"/>`);
    const factory = H0(0, -780, S, K.props.factory({}));
    const wm = man(H, K.castOpts("weaponsMaker", { arms: [[30, 20], [-30, -20]], hold: null }), 380, -780, S);
    const desk2 = `<rect x="-1130" y="-60" width="300" height="24" fill="#7A5634" stroke="${C.line}" stroke-width="6"/><rect x="-1110" y="-36" width="260" height="116" fill="#8C6440" stroke="${C.line}" stroke-width="6"/>`;
    let bar = "";
    for (let y = 60; y > -1100; y -= 16) bar += slab(C, -1330, y, 140, "war");
    const capitol = H0(1050, 80, 1.25, K.props.capitol({}));
    const pol = man(H, K.castOpts("politician", { look: "left", arms: [[20, 10], [-20, -10]], holdR: null }), 900, 60, S);
    const box = H0(0, BOT, S * 1.5, K.props.ballotBox({}));
    const voters = [[150, 0, 1, 71], [290, 3, 0, 72]].map(([x, tone, color, seed]) => man(H, { tone, outfit: "shirt", color, hair: 0, seed, look: "left", mood: "flat", arms: [[8, 4], [-8, -4]] }, x, BOT, S)).join("");
    // a voter holds up the ring's pulled plug; its cord runs back to the ring; the socket on its post
    const top = BOT - 100 * S - 115;
    const plugger = man(H, { tone: 1, outfit: "dress", color: 1, hair: 1, seed: 73, look: "right", mood: "flat", arms: [[8, 4], [150, 176]] }, -420, BOT, S) +
      `<path d="M-390,${top} q80,40 110,140 q30,120 -20,${BOT - top - 160} q-30,60 60,40" fill="none" stroke="${C.line}" stroke-width="10"/>` +
      `<rect x="-412" y="${top - 35}" width="40" height="34" fill="${C.slate}" stroke="${C.line}" stroke-width="6"/><path d="M-404,${top - 35} v-22 M-382,${top - 35} v-22" stroke="${C.line}" stroke-width="7"/>` +
      `<rect x="-700" y="${BOT - 260}" width="16" height="260" fill="#7A5634" stroke="${C.line}" stroke-width="5"/><rect x="-726" y="${BOT - 330}" width="68" height="84" fill="#FBF6E6" stroke="${C.line}" stroke-width="6"/><path d="M-704,${BOT - 300} v22 M-680,${BOT - 300} v22" stroke="${C.line}" stroke-width="7"/>`;
    const missiles = [[-1000, -560], [-1600, -380], [-2200, -200]].map(([x, y]) => H0(x, y, 1.5, K.props.missile({ mood: "smug", arms: "none" }), -78)).join("");
    const papers = [[-560, -380], [-640, 0], [-450, 450], [420, 500], [610, 160], [470, -440]].map(([x, y]) => bill(H, "war", x, y, 1.6)).join("");
    const dogAt = H0(-200, 600, 1.9, K.props.democracyDog({ tail: "papers", seal: "war" }));
    const nuke = H0(-2550, 0, 2.3, K.nuke());
    const svg = field() + v(nuke + ring + face + papers + dogAt + hornL + hornR + factory + wm + bar + desk2 + capitol + pol + box + voters + plugger + missiles);
    return { svg, alt: "The whole loop from above: a ring road on the field with two red horns at its top either side of the missile-chimney factory, an angry face in its infield (scowling brows, red eyes) and a fanged grin inside its bottom bend; the 604 bar and the empty desk on the left, the Politician on the capitol steps on the right, the ballot box and voters at the bottom; a voter holds up the ring's pulled plug while it keeps turning; grinning missiles fly off the left, and far off to the left a mushroom cloud rises." };
  },

  // ── 6 · host: the reaction cut after the bomb ──
  "loop-side-eye"(H, id) {
    return { svg: H.host("sideeye-closed", "arms-crossed", ""), alt: "Wishonia alone at her lectern, arms crossed, side-eyeing the camera: the one who looked round at the bomb." };
  },

  // ── 6 · plate the-loop: the street, the squeezed house ──
  "weapons-maker-gets-sick"(H, id) {
    const { K, C } = H;
    // the house, squeezed small round the family; the picture window (house units x -178..-70, y -146..-80)
    const hx = 1010, hy = 1010, sx = 3.1, sy = 2.7;
    const house = `<g transform="translate(${hx},${hy}) scale(${sx},${sy})">${K.props.house({ variant: 1, smoke: false })}</g>`;
    const W = (ux, uy) => [hx + ux * sx, hy + uy * sy];
    const [wx0, wy0] = W(-178, -146), [wx1, wy1] = W(-70, -80), ww = wx1 - wx0, wh = wy1 - wy0;
    // a face pressed flat on the glass: wide, its nose squashed into a disc
    const flatFace = (cx, cy, r, tone, hat) => {
      let g = `<ellipse cx="${cx}" cy="${cy}" rx="${r * 1.35}" ry="${r * 0.95}" fill="${SKIN[tone]}" stroke="${C.line}" stroke-width="3"/>` +
        `<ellipse cx="${cx - r * 0.5}" cy="${cy - r * 0.18}" rx="${r * 0.26}" ry="${r * 0.2}" fill="#FBF6E6" stroke="${C.line}" stroke-width="2"/><ellipse cx="${cx + r * 0.5}" cy="${cy - r * 0.18}" rx="${r * 0.26}" ry="${r * 0.2}" fill="#FBF6E6" stroke="${C.line}" stroke-width="2"/>` +
        `<circle cx="${cx - r * 0.5}" cy="${cy - r * 0.16}" r="${r * 0.09}" fill="${C.line}"/><circle cx="${cx + r * 0.5}" cy="${cy - r * 0.16}" r="${r * 0.09}" fill="${C.line}"/>` +
        `<circle cx="${cx}" cy="${cy + r * 0.12}" r="${r * 0.32}" fill="${SKIN[tone]}" stroke="${C.line}" stroke-width="2.4"/><path d="M${cx - r * 0.5},${cy + r * 0.6} Q${cx},${cy + r * 0.48} ${cx + r * 0.5},${cy + r * 0.6}" fill="none" stroke="${C.line}" stroke-width="2.6"/>` +
        `<circle cx="${cx}" cy="${cy}" r="${r * 1.2}" fill="#FFFFFF" opacity="0.12"/>`;
      if (hat) g += `<path d="M${cx - r * 1.05},${cy - r * 0.62} Q${cx},${cy - r * 1.45} ${cx + r * 1.05},${cy - r * 0.62} Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="2.6"/>`;
      return g;
    };
    // the Weapons Maker: his tiny head, the hard hat jammed down over his eyes, his cigar
    const wmHead = (cx, cy) => `<ellipse cx="${cx}" cy="${cy + 12}" rx="26" ry="24" fill="${SKIN[3]}" stroke="${C.line}" stroke-width="3"/>` +
      `<path d="M${cx - 36},${cy + 4} Q${cx},${cy - 52} ${cx + 36},${cy + 4} L${cx + 44},${cy + 12} H${cx - 44} Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/>` +
      `<path d="M${cx + 6},${cy + 26} l26,6" stroke="${C.line}" stroke-width="8" stroke-linecap="round"/><path d="M${cx + 6},${cy + 26} l26,6" stroke="${C.rust}" stroke-width="4" stroke-linecap="round"/>`;
    const glass = `<clipPath id="${id}-win"><rect x="${wx0}" y="${wy0}" width="${ww}" height="${wh}"/></clipPath>` +
      `<g clip-path="url(#${id}-win)"><rect x="${wx0}" y="${wy0}" width="${ww}" height="${wh}" fill="#F0D58A"/>` +
      wmHead(wx0 + 0.17 * ww, wy0 + 0.22 * wh) + flatFace(wx0 + 0.42 * ww, wy0 + 0.5 * wh, 46, 2, false) + flatFace(wx0 + 0.68 * ww, wy0 + 0.6 * wh, 34, 3, true) + flatFace(wx0 + 0.88 * ww, wy0 + 0.5 * wh, 30, 3, true) +
      `<path d="M${wx0},${wy0 + 40} L${wx1},${wy0 + 90}" stroke="#FFFFFF" stroke-width="6" opacity="0.3"/></g>` +
      `<rect x="${wx0}" y="${wy0}" width="${ww}" height="${wh}" fill="none" stroke="${C.line}" stroke-width="7"/>`;
    // the small window: Part 1's skeleton print in its frame (white deckled border), the family grinning skulls,
    // and a Reaper-shaped blank between the heads where he climbed out
    const [px0, py0] = W(30, -142), [px1, py1] = W(78, -96), pw = px1 - px0, ph = py1 - py0;
    const blank = (cx, top, w, h) => `<path d="M${f(cx - w * 0.5)},${f(top + h)} L${f(cx - w * 0.42)},${f(top + h * 0.35)} Q${f(cx - w * 0.36)},${f(top)} ${f(cx)},${f(top)} Q${f(cx + w * 0.36)},${f(top)} ${f(cx + w * 0.42)},${f(top + h * 0.35)} L${f(cx + w * 0.5)},${f(top + h)} Z" fill="#FFFFFF" stroke="#C9BFA6" stroke-width="2" stroke-dasharray="4 3"/>`;
    const portrait = `<rect x="${px0 + 8}" y="${py0 + 8}" width="${pw - 16}" height="${ph - 16}" fill="#B98A55" stroke="${C.line}" stroke-width="3"/>` +
      `<rect x="${px0 + 14}" y="${py0 + 14}" width="${pw - 28}" height="${ph - 28}" fill="#FFFFFF" stroke="#D9D2C0" stroke-width="2" stroke-dasharray="3 2"/>` +
      `<rect x="${px0 + 20}" y="${py0 + 20}" width="${pw - 40}" height="${ph - 40}" fill="#8E8775"/>` +
      blank(px0 + 0.5 * pw, py0 + 0.24 * ph, 0.2 * pw, 0.5 * ph) +
      [0.28, 0.4, 0.62, 0.74].map((u, i) => skull(C, px0 + u * pw, py0 + (i % 3 ? 0.5 : 0.42) * ph, 9)).join("");
    const squeeze = lines(C, [[hx - 780, hy - 480, hx - 716, hy - 456], [hx - 800, hy - 330, hx - 730, hy - 326]], 7);
    const reaper = H.at(1790, 1010 - 100 * 2.4, 2.4, K.reaper());
    const watch = `<path d="M1900,640 l40,-30" stroke="${C.line}" stroke-width="10" stroke-linecap="round"/><circle cx="1890" cy="624" r="15" fill="${C.cream}" stroke="${C.line}" stroke-width="4"/><path d="M1890,624 v-8 M1890,624 h6" stroke="${C.line}" stroke-width="2.6"/>` +
      H.at(1700, 760, 1.4, K.props.clipboard({ title: "TODAY", items: ["", "", ""] }), -8);
    const svg = field() + road("M-100,1030 H2020", 200) + house + glass + portrait + squeeze + reaper + watch;
    return { svg, alt: "The Weapons Maker's ranch house, squeezed small round the family: in its picture window his hard hat is jammed down over his eyes and his wife's and children's faces are pressed flat against the glass; in the small window hangs Part 1's skeleton print, a Reaper-shaped blank between the grinning skulls where he climbed out; outside the Grim Reaper waits with his clipboard, tapping his watch." };
  },

  // ── 7 · plate the-loop: the street, the deal ──
  "redirect-math"(H, id) {
    const { K, C } = H;
    // the house grown 1.43 times: the house with a second floor on it
    const hx = 1180, hy = 960, hk = 2.0;
    const house = `<g transform="translate(${hx},${hy}) scale(${hk})">${K.props.house({ variant: 1, smoke: false })}</g>`;
    const fx0 = hx - 205 * hk, fx1 = hx + 105 * hk, fy1 = hy - 232 * hk, fy0 = fy1 - 170;
    const upper = `<rect x="${fx0}" y="${fy0}" width="${fx1 - fx0}" height="${fy1 - fy0 + 10}" fill="#7FA9A6" stroke="${C.line}" stroke-width="5"/>` +
      [0, 1, 2].map((i) => `<rect x="${fx0 + 40 + i * 205}" y="${fy0 + 36}" width="110" height="88" fill="${C.yellow}" stroke="${C.line}" stroke-width="5"/><path d="M${fx0 + 95 + i * 205},${fy0 + 36} v88" stroke="${C.line}" stroke-width="3"/>`).join("") +
      `<path d="M${fx0 - 40},${fy0 + 4} L${fx0 + 60},${fy0 - 120} H${fx1 - 60} L${fx1 + 40},${fy0 + 4} Z" fill="${C.rust}" stroke="${C.line}" stroke-width="5" stroke-linejoin="round"/>`;
    const num = H.big(hx - 50, fy0 - 150, 120, "×1.43");
    // the Weapons Maker: the share held up high in one hand, his baby missile cradled in the other arm
    const WM = K.castOpts("weaponsMaker", { mood: "smile", look: "right", arms: [[-150, -178], [-36, -84]], hold: null });
    const R = K.rig(WM), k = 3.0, X = 480, FEET = 1000;
    const hl = pt(X, FEET, k, R.hand[0]), hr = pt(X, FEET, k, R.hand[1]);
    const share = H.at(hl[0] + 6, hl[1] + 30, 1.4, K.props.bond({ text: "SHARE", value: "", seal: "med" }), -6);
    const baby = H.at(hr[0] + 4, hr[1] - 2, k * 0.95, `<g transform="translate(0,-6) rotate(-14)"><path d="M-34,-7 L14,-7 L30,0 L14,7 L-34,7 Z M-34,-7 L-44,-17 L-40,-7 Z M-34,7 L-44,17 L-40,7 Z" fill="${C.war}" stroke="${C.line}" stroke-width="2.6" stroke-linejoin="round"/><path d="M14,-7 L30,0 L14,7 Z" fill="${C.cream}" stroke="${C.line}" stroke-width="2"/><path d="M-4,2 Q2,6 8,2" fill="none" stroke="${C.line}" stroke-width="1.8"/><circle cx="-2" cy="-2.5" r="1.6" fill="${C.line}"/><circle cx="6" cy="-2.5" r="1.6" fill="${C.line}"/></g>`);
    // the Reaper slouching off the right edge, his clipboard with the name crossed off
    const reaper = H.at(1830, 980 - 100 * 1.9, 1.9, K.reaper(), 12) +
      H.at(1700, 760, 1.25, K.props.clipboard({ title: "TODAY", items: [["W. MAKER", "cross"], "", ""] }), -16) +
      lines(C, [[1940, 650, 1984, 650], [1944, 730, 1990, 734]], 6);
    const svg = field() + road("M-100,1040 H2020", 160) + house + upper + num + man(H, WM, X, FEET, k) + share + baby + reaper;
    return { svg, alt: "The Weapons Maker smiling in front of his house, grown 1.43 times bigger with a second floor (×1.43 over it), his chest light out; he holds a share certificate with a cross seal up high and cradles his grinning baby missile in the other arm; at the right edge the Grim Reaper slouches off with his clipboard, the name crossed off." };
  },

  // ── 8 · host: the arithmetic ──
  "no-rational-beneficiary"(H, id) {
    const { K, C } = H;
    const WM = K.castOpts("weaponsMaker", { mood: "worried", look: "left", hat: null, light: "red", arms: [[-30, -150], [-60, -160]], hold: null });
    const R = K.rig(WM), k = 3.4, X = 1480, FEET = 1070;
    const top = pt(X, FEET, k, R.top);
    const steam = `<path d="M${top[0] - 12},${top[1] + 8} L${top[0] - 52},${top[1] - 200} Q${top[0] + 6},${top[1] - 226} ${top[0] + 64},${top[1] - 196} L${top[0] + 12},${top[1] + 8} Z" fill="#F6F1E4" stroke="${C.line}" stroke-width="4" stroke-linejoin="round"/>` +
      `<path d="M${top[0] - 20},${top[1] - 60} q-8,-30 4,-60 M${top[0] + 22},${top[1] - 80} q10,-30 -2,-64" fill="none" stroke="${C.line}" stroke-width="3" opacity="0.5"/>` +
      puff(top[0] - 110, top[1] - 210, 30) + puff(top[0] + 130, top[1] - 170, 26) + puff(top[0] + 30, top[1] - 250, 22) +
      lines(C, [[top[0] - 70, top[1] - 60, top[0] - 100, top[1] - 90], [top[0] + 70, top[1] - 60, top[0] + 100, top[1] - 90]], 5);
    const hat = H.at(top[0] + 50, top[1] - 360, 2.6, `<path d="M-23,5 L-18,-13 L0,-20 L18,-13 L23,5 Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="2.6"/><path d="M-30,8 L-26,3 H26 L30,8 Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="2.2"/>`, 24);
    // the counting fingers: four short fingers up from each raised hand
    const hands = [0, 1].map((i) => { const h = pt(X, FEET, k, R.hand[i]); return [-1.5, -0.5, 0.5, 1.5].map((j) => { const d = `M${f(h[0] + j * 9)},${f(h[1] - 4)} l${f(j * 3)},-30`; return `<path d="${d}" stroke="${C.line}" stroke-width="12" stroke-linecap="round"/><path d="${d}" stroke="${SKIN[3]}" stroke-width="7" stroke-linecap="round"/>`; }).join(""); }).join("");
    const front = man(H, WM, X, FEET, k) + hands + steam + hat;
    const svg = H.host("smirk-smile", "presenting", front);
    return { svg, alt: "Wishonia at her lectern, smirking at the camera; at her right her guest the Weapons Maker, chest light blinking red, both hands up counting on his fingers, a jet of steam shooting from his head where his hard hat was, the hard hat flying up like a cork." };
  },

  // ── 9 · plate the-loop: the ties ──
  "red-blue-ties"(H, id) {
    const { K, C } = H;
    const k = 2.5, FEET = 840;
    const RED = K.castOpts("politician", { look: "right", mood: "cross", arms: [[150, 175], [40, 120]], holdR: null, tieColor: C.war });
    const BLUE = K.castOpts("politician", { look: "left", mood: "cross", arms: [[-40, -120], [-150, -175]], holdR: null, tieColor: C.peri });
    const CROSS_Y = 250;
    const pol = (o, x) => {
      const R = K.rig(o), hand = R.hand.map((h) => pt(x, FEET, k, h)), neck = pt(x, FEET, k, R.neck);
      // the tie as a spinning propeller: a blur disc and two blades
      const tc = o.tieColor, cy = neck[1] + 64;
      const prop = `<ellipse cx="${f(neck[0])}" cy="${f(cy)}" rx="120" ry="26" fill="${tc}" opacity="0.3" stroke="${C.line}" stroke-width="2.4" stroke-dasharray="12 9"/>` +
        `<path d="M${f(neck[0])},${f(cy)} L${f(neck[0] - 112)},${f(cy - 16)} L${f(neck[0] - 106)},${f(cy + 12)} Z M${f(neck[0])},${f(cy)} L${f(neck[0] + 112)},${f(cy + 16)} L${f(neck[0] + 106)},${f(cy - 12)} Z" fill="${tc}" stroke="${C.line}" stroke-width="3.5" stroke-linejoin="round"/>` +
        `<circle cx="${f(neck[0])}" cy="${f(cy)}" r="11" fill="${C.cream}" stroke="${C.line}" stroke-width="3"/>` +
        lines(C, [[neck[0] - 140, cy - 30, neck[0] - 160, cy - 44], [neck[0] + 140, cy + 30, neck[0] + 160, cy + 44]], 4);
      const ends = x < 960 ? [720, 800] : [1120, 1200];
      const strings = hand.map((h, i) => `<path d="M${f(h[0])},${f(h[1])} L${ends[i]},${CROSS_Y}" stroke="${C.line}" stroke-width="2.6"/>`).join("") +
        `<path d="M${f(neck[0])},${f(neck[1] - 110)} L${(ends[0] + ends[1]) / 2},${CROSS_Y}" stroke="${C.line}" stroke-width="2.6"/>`;
      return strings + man(H, o, x, FEET, k) + prop;
    };
    // the giant war paper over the ring, its stick arms down to one wooden puppet cross
    const gp = H.at(960, 60, 4.2, K.money("war").replace('class="legs"', 'class="legs" opacity="0"'));
    const cross = `<path d="M860,150 L760,${CROSS_Y - 10} M1060,150 L1160,${CROSS_Y - 10}" fill="none" stroke="${C.line}" stroke-width="9" stroke-linecap="round"/>` +
      `<path d="M690,${CROSS_Y} H1230 M960,${CROSS_Y - 50} V${CROSS_Y + 50}" stroke="${C.line}" stroke-width="30" stroke-linecap="round"/><path d="M690,${CROSS_Y} H1230 M960,${CROSS_Y - 50} V${CROSS_Y + 50}" stroke="#9A7049" stroke-width="20" stroke-linecap="round"/>`;
    const box = H.at(330, 880, 3.2, K.props.ballotBox({}));
    const lift = lines(C, [[690, 870, 690, 906], [750, 870, 750, 910], [1170, 870, 1170, 910], [1230, 870, 1230, 906]], 5);
    const svg = field() + road("M-100,960 H2020", 240) + box + gp + cross + pol(RED, 740) + pol(BLUE, 1180) + lift;
    return { svg, alt: "Two identical Politicians, one in a red tie and one in a blue tie, lifted off the road by their ties spinning like propellers; marionette strings run from their wrists and heads up to one wooden puppet cross held in the stick arms of a giant war paper above them; the ballot box stands beside them." };
  },

  // ── 10 · plate living-room: the wallpaper ──
  "wallpaper-burning-building"(H, id) {
    const { K, C } = H;
    let wall = "";
    for (let x = 0; x < 1920; x += 60) {
      const blue = x >= 1020;
      wall += `<rect x="${x}" y="0" width="30" height="860" fill="${blue ? "#7E95B6" : "#C0705A"}"/><rect x="${x + 30}" y="0" width="30" height="860" fill="${blue ? "#C9D4E2" : "#EAD2B8"}"/>`;
    }
    // the window with its burning curtains, the smoke rolling along the ceiling, the floor
    const win = `<rect x="140" y="200" width="420" height="380" fill="#2B2C3C" stroke="${C.line}" stroke-width="8"/><path d="M350,200 V580 M140,390 H560" stroke="${C.line}" stroke-width="6"/>` +
      `<path d="M110,170 H200 L190,640 H120 Z M500,170 H590 L580,640 H510 Z" fill="${C.orange}" stroke="${C.line}" stroke-width="5"/>` +
      K.flames(150, 560, 2.2) + K.flames(545, 560, 2.4) + K.flames(150, 380, 1.5) + K.flames(560, 360, 1.6) + K.flames(860, 520, 1.3);
    const smoke = [140, 400, 680, 960, 1240, 1520, 1800].map((x, i) => puff(x, 30 + (i % 3) * 26, 64 + (i % 2) * 14, "#6E6A66")).join("");
    const floor = `<rect y="860" width="1920" height="220" fill="#8C6440"/><path d="M0,860 H1920" stroke="${C.line}" stroke-width="8"/>`;
    // the fire extinguisher, half papered over with the blue stripes
    const ext = `<rect x="1050" y="420" width="64" height="150" rx="24" fill="${C.war}" stroke="${C.line}" stroke-width="5"/><path d="M1070,420 v-24 h44" fill="none" stroke="${C.line}" stroke-width="7"/>` +
      `<rect x="1080" y="0" width="30" height="860" fill="#7E95B6" opacity="0.96"/><rect x="1110" y="0" width="30" height="860" fill="#C9D4E2" opacity="0.96"/><path d="M1080,0 V860" stroke="${C.line}" stroke-width="2" opacity="0.5"/>`;
    // the voter, his paste brush up on the fresh red strip
    const V = { tone: 1, outfit: "shirt", color: 2, hair: 0, seed: 91, look: "left", mood: "smile", arms: [[-110, -150], [-30, -60]] };
    const R = K.rig(V), k = 3.5, X = 1560, FEET = 1010;
    const hs = R.hand.map((h) => pt(X, FEET, k, h));
    const strip = `<g transform="translate(1290,60) rotate(3)"><rect width="90" height="790" fill="#C0705A" stroke="${C.line}" stroke-width="4"/><rect x="45" width="45" height="790" fill="#EAD2B8"/></g>` +
      `<path d="M${f(hs[0][0])},${f(hs[0][1])} L${f(hs[0][0] - 60)},${f(hs[0][1] - 20)}" stroke="${C.line}" stroke-width="12" stroke-linecap="round"/><path d="M${f(hs[0][0])},${f(hs[0][1])} L${f(hs[0][0] - 60)},${f(hs[0][1] - 20)}" stroke="${C.tan}" stroke-width="7" stroke-linecap="round"/>` +
      `<rect x="${f(hs[0][0] - 92)}" y="${f(hs[0][1] - 52)}" width="34" height="62" fill="#EAD2B8" stroke="${C.line}" stroke-width="4"/>`;
    // on fire all over, the hair burning straight up, a flame up the trouser leg: flames in person units
    const fire = K.flames(R.top[0], R.top[1] + 6, 0.55) + K.flames(R.shoulder[1][0] + 4, R.shoulder[1][1] + 14, 0.34) + K.flames(-6, R.hipY + 40, 0.42) + K.flames(8, 96, 0.36);
    const voter = H.at(X, FEET - 100 * k, k, K.person(V) + fire);
    const svg = wall + win + ext + smoke + floor + strip + voter;
    return { svg, alt: "A 1950s living room on fire: the curtains blazing, smoke rolling along the ceiling, the wall half red stripes and half new blue stripes papered right over the fire extinguisher; the voter, on fire all over with his hair burning straight up, still smiling, brushes a fresh red-striped strip back up over the blue." };
  },

  // ── 11 · plate the-loop: the desk again, the medicine papers ──
  "better-loop"(H, id) {
    const { K, C } = H;
    const k = 3.6, X = 1160, FEET = 1050;
    const POL = K.castOpts("politician", { charred: true, look: "right", arms: [[34, 100], [-34, -100]], holdR: null });
    const R = K.rig(POL);
    // still grinning (white teeth on the charred face), dollar signs lit in his white eyes
    const e = pt(X, FEET, k, R.eyes), m = pt(X, FEET, k, R.mouth);
    const dollars = [e[0] - 6.7 * k, e[0] + 6.6 * k].map((x) => `<text x="${f(x)}" y="${f(e[1] + 10)}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="34" fill="${C.money}" stroke="${C.line}" stroke-width="2">$</text>`).join("");
    const grin = `<path d="M${f(m[0] - 30)},${f(m[1] - 6)} Q${f(m[0])},${f(m[1] + 26)} ${f(m[0] + 26)},${f(m[1] - 8)} Z" fill="#FBF6E6" stroke="${C.line}" stroke-width="3"/><path d="M${f(m[0] - 14)},${f(m[1] - 3)} v12 M${f(m[0])},${f(m[1] - 3)} v14 M${f(m[0] + 13)},${f(m[1] - 4)} v11" stroke="${C.line}" stroke-width="2"/>`;
    // the armful of medicine papers, low in his arms
    const hug = pt(X, FEET, k, [(R.hand[0][0] + R.hand[1][0]) / 2, (R.hand[0][1] + R.hand[1][1]) / 2]);
    const arm = [[-80, 34, -12], [-10, 30, 6], [60, 34, 12], [-50, -4, -4], [26, -6, 9]].map(([dx, dy, r]) => bill(H, "med", hug[0] + dx, hug[1] + dy, 1.3, r)).join("");
    let stack = "";
    for (let y = 846; y > -40; y -= 16) stack += slab(C, 290 + ((y / 16) % 2 ? 4 : 0), y, 250, "war");
    // the manual lying open on the desk, its orange cover under the white pages
    const manual = `<g transform="translate(800,742)"><path d="M-150,6 L-6,-30 L0,6 Z M150,6 L6,-30 L0,6 Z" fill="${C.orange}" stroke="${C.line}" stroke-width="4" stroke-linejoin="round"/><path d="M-140,0 L-6,-34 L0,0 Z M140,0 L6,-34 L0,0 Z" fill="#FBF6E6" stroke="${C.line}" stroke-width="4" stroke-linejoin="round"/>` +
      `<path d="M-120,-6 L-24,-30 M-104,-12 L-26,-32 M120,-6 L24,-30 M104,-12 L26,-32" stroke="${C.line}" stroke-width="2.4" opacity="0.6"/></g>`;
    const glow = lines(C, [[e[0] - 70, e[1] - 50, e[0] - 92, e[1] - 70], [e[0] + 70, e[1] - 50, e[0] + 92, e[1] - 70]], 5);
    const svg = field() + stack + man(H, POL, X, FEET, k) + dollars + grin + arm + glow + desk(C, 1160, 740, 820) + manual;
    return { svg, alt: "The Politician at his desk, charred black and smoking, hair straight up, still grinning, dollar signs lit in his white eyes, hugging an armful of medicine papers with cross seals; the manual lies open on the desk; the 604 bar rises at the left." };
  },

  // ── 12 · host: the dog with the teal tail, reelected ──
  "better-loop-teal-tail"(H, id) {
    const { K, C } = H;
    const k = 3.2, X = 1500, FEET = 1064;
    const dog = K.props.democracyDog({ tail: "pills", mood: "smile" });
    const extra = [0.2, 0.4, 0.6, 0.8].map((t) => { const p = tailPt(t); return koBlob(C, p[0] + 2, p[1] + 10, 6.5); }).join("") +
      H0(-30, -60, 0.36, rosette(C, "REELECTED"), -6);
    let confetti = "";
    const cols = [C.med, C.yellow, C.war, C.cream, C.orange];
    for (let i = 0; i < 30; i++) {
      const x = 1140 + ((i * 7919) % 731), y = 70 + ((i * 3571) % 560), r = (i * 47) % 180;
      confetti += `<rect x="${x}" y="${y}" width="20" height="10" fill="${cols[i % 5]}" stroke="${C.line}" stroke-width="1.6" transform="rotate(${r} ${x + 10} ${y + 5})"/>`;
    }
    const front = confetti + H.at(X, FEET, k, dog + extra) + lines(C, [[1340, 760, 1300, 750], [1350, 820, 1306, 822]], 5);
    const svg = H.host("smirk-smile", "idle", front);
    return { svg, alt: "Wishonia at her lectern, smirking; at her right the Democracy Dog chases its new tail of teal pills knotted with tiny knocked-out disease blobs, a REELECTED rosette landing on its collar, confetti falling." };
  },
};
