// Sketches for storyboards/part-23-you-dont-need-to-understand.md: each scene's key moment on a 1920 x 1080 frame
// (16:9), in the film look (Part 2 is the reference). Host shots use H.host (KIT.STUDIO, 16:9: the lectern's reading
// top at y 790, the free wall right of it x 1100 to 1880); plates are drawn as the camera sees them at that moment.
// Captions keep-out: nothing important below y 900. Built into the review sheet by tools/storyboard-sheet.mjs.

const f = (n) => (+n).toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});
// A plate framing as KIT.camera places it: plate point (x, y) in the middle of the frame, at scale s.
const view = (x, y, s, inner) => `<g transform="translate(${f(960 - x * s)},${f(540 - y * s)}) scale(${s})">${inner}</g>`;
const at = (x, y, k, inner, rot = 0) => `<g transform="translate(${f(x)},${f(y)})${rot ? ` rotate(${rot})` : ""}${k !== 1 ? ` scale(${k})` : ""}">${inner}</g>`;
// A KIT.person drawn with its feet on (x, y) at scale k.
const stand = (K, x, y, k, o, rot = 0) => at(x, y - 100 * k, k, K.person(o), rot);
const poly = (pts, fill, ink, w = 4, extra = "") => `<path d="M${pts.map((p) => `${f(p[0])},${f(p[1])}`).join(" L")} Z" fill="${fill}" stroke="${ink}" stroke-width="${w}" stroke-linejoin="miter" ${extra}/>`;
const osw = (x, y, size, text, fill, anchor = "middle", extra = "") =>
  `<text x="${f(x)}" y="${f(y)}" text-anchor="${anchor}" font-family="Oswald" font-weight="600" font-size="${size}" letter-spacing="${f(size * 0.05)}" fill="${fill}" ${extra}>${text}</text>`;
const num = (x, y, size, text, fill, anchor = "middle") => `<text x="${f(x)}" y="${f(y)}" text-anchor="${anchor}" font-family="Fraunces" font-weight="900" font-size="${size}" fill="${fill}">${text}</text>`;

// The office-map plate: the wall map (KIT.props.worldMap({ w: 4200 }) standing on y 0, centered on x 0) and the
// office around it, drawn at 7 times a person's scale. MP: a point of the map's 400 x 220 land space in plate units.
const MP = (u, v) => [-1869 + 9.345 * u, -2382 + 9.736 * v];
const OFF = { k: 7, floor: 825, desk: 250, chair: -560, door: 2700, hook: 3330 };
// People on the map are KIT.person at scale 1.5 (about 270 tall); framings inside the map are at scale 1 to 1.4.
const PK = 1.5;
const YOU = { tone: 2, outfit: "suit", hat: "bowler" };
// The old woman in the den: an everyday human, not Grandma (who died in Part 17).
const OLD = { tone: 3, outfit: "dress", hair: 1, hairColor: "#DEDAD2", color: 1, seed: 31, build: { hunch: 12 } };
const PINK = "#E9B4C1", BRASS = "#C9A24A", BONE = "#F1EAD6", GLASS = "#DCEFF0";

// A pencil lying along +x, centered on (0, 0): the eraser, the brass ferrule, the six-sided yellow body, the tip.
function pencil(C, L = 150, W = 22, o = {}) {
  const h = W / 2, e = L * 0.11, fr = L * 0.08, tip = L * 0.17, x0 = -L / 2, x1 = L / 2, ink = C.line;
  return (o.eraser === false ? "" : poly([[x0, -h], [x0 + e, -h], [x0 + e, h], [x0, h]], PINK, ink, 3)) +
    (o.ferrule === false ? "" : poly([[x0 + e, -h - 1], [x0 + e + fr, -h - 1], [x0 + e + fr, h + 1], [x0 + e, h + 1]], BRASS, ink, 3) +
      `<path d="M${f(x0 + e + fr * 0.33)},${f(-h)} V${f(h)} M${f(x0 + e + fr * 0.66)},${f(-h)} V${f(h)}" stroke="${ink}" stroke-width="1.6"/>`) +
    poly([[x0 + e + fr, -h], [x1 - tip, -h], [x1 - tip, h], [x0 + e + fr, h]], C.yellow, ink, 3) +
    `<path d="M${f(x0 + e + fr)},${f(-h * 0.3)} H${f(x1 - tip)}" stroke="${C.orange}" stroke-width="2.4"/>` +
    poly([[x1 - tip, -h], [x1, 0], [x1 - tip, h]], "#E8C79A", ink, 3) + poly([[x1 - tip * 0.35, -h * 0.35], [x1, 0], [x1 - tip * 0.35, h * 0.35]], C.slate, ink, 2);
}
// A little spider, standing on (0, 0) (about 34 wide in person units), or lounging with its feet up.
function spider(C, o = {}) {
  const ink = C.line, body = o.bone ? BONE : "#2A2622";
  let legs = "";
  for (let i = 0; i < 4; i++) {
    const a = -40 + i * 26;
    for (const s of [-1, 1]) {
      const kx = s * (12 + i * 1.5), ky = -16 - Math.sin((a * Math.PI) / 180) * 4;
      const fx = s * (17 + i * 2.6), fy = o.up && i < 2 ? -30 - i * 4 : 0;
      legs += `<path d="M${s * 5},${-10 + i * 1.6} L${f(kx)},${f(ky - 6)} L${f(fx)},${f(fy)}" fill="none" stroke="${ink}" stroke-width="${o.bone ? 4.2 : 3}" stroke-linejoin="miter"/>` +
        (o.bone ? `<path d="M${s * 5},${-10 + i * 1.6} L${f(kx)},${f(ky - 6)} L${f(fx)},${f(fy)}" fill="none" stroke="${BONE}" stroke-width="1.6" stroke-linejoin="miter"/>` : "");
    }
  }
  const eyes = o.bone
    ? `<circle cx="-3.4" cy="-19" r="2.4" fill="${ink}"/><circle cx="3.4" cy="-19" r="2.4" fill="${ink}"/><path d="M-4.5,-14 h9 M-3,-15.6 v3 M0,-15.6 v3 M3,-15.6 v3" stroke="${ink}" stroke-width="1.2"/>`
    : `<circle cx="-3" cy="-19" r="2.3" fill="#FBF6E6"/><circle cx="3" cy="-19" r="2.3" fill="#FBF6E6"/><circle cx="-2.6" cy="-18.6" r="1.1" fill="${ink}"/><circle cx="3.4" cy="-18.6" r="1.1" fill="${ink}"/>`;
  return legs + `<ellipse cx="0" cy="-8" rx="10" ry="8" fill="${body}" stroke="${ink}" stroke-width="2.4"/>` +
    (o.bone ? `<path d="M-6,-8 h12 M-6,-4 h12 M-5,-12 h10" stroke="${ink}" stroke-width="1.2"/>` : "") +
    `<circle cx="0" cy="-18" r="6.5" fill="${body}" stroke="${ink}" stroke-width="2.2"/>` + eyes + (o.thread ? `<path d="M0,-24 V-400" stroke="${C.cream}" stroke-width="1.2" opacity="0.8"/>` : "");
}
// A cobweb across a corner or a doorway: spokes and rings from (cx, cy), radius r, over angles a0..a1 (deg).
function cobweb(cx, cy, r, a0, a1, col, w = 2) {
  let d = "";
  const n = 6;
  const pt = (a, rr) => [cx + rr * Math.cos((a * Math.PI) / 180), cy + rr * Math.sin((a * Math.PI) / 180)];
  for (let i = 0; i <= n; i++) { const p = pt(a0 + ((a1 - a0) * i) / n, r); d += `M${f(cx)},${f(cy)} L${f(p[0])},${f(p[1])} `; }
  for (let k = 1; k <= 4; k++) {
    const rr = (r * k) / 4.3;
    for (let i = 0; i < n; i++) {
      const p = pt(a0 + ((a1 - a0) * i) / n, rr), q = pt(a0 + ((a1 - a0) * (i + 1)) / n, rr), m = pt(a0 + ((a1 - a0) * (i + 0.5)) / n, rr * 0.86);
      d += `M${f(p[0])},${f(p[1])} Q${f(m[0])},${f(m[1])} ${f(q[0])},${f(q[1])} `;
    }
  }
  return `<path d="${d}" fill="none" stroke="${col}" stroke-width="${w}" opacity="0.85"/>`;
}
// The 1950s office swivel chair, front view, standing on (0, 0) in person units (about 70 wide, 112 tall).
function chair(C, dust = false) {
  const ink = C.line, seat = dust ? "#8C6A55" : C.rust;
  return poly([[-30, -112], [30, -112], [34, -104], [32, -62], [-32, -62], [-34, -104]], seat, ink, 3.4) +
    `<path d="M-20,-102 V-70 M0,-104 V-68 M20,-102 V-70" stroke="${ink}" stroke-width="1.6" opacity="0.6"/>` +
    poly([[-4, -62], [4, -62], [4, -46], [-4, -46]], C.slate, ink, 2.6) +
    poly([[-36, -52], [36, -52], [40, -40], [-40, -40]], seat, ink, 3.4) +
    poly([[-3, -40], [3, -40], [3, -12], [-3, -12]], C.slate, ink, 2.6) +
    `<path d="M0,-12 L-30,-4 M0,-12 L30,-4 M0,-12 L-14,-2 M0,-12 L14,-2" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>` +
    [-30, -14, 14, 30].map((x) => `<circle cx="${x}" cy="-3" r="3.6" fill="${C.slate}" stroke="${ink}" stroke-width="2"/>`).join("");
}
// The office desk, front view, standing on (0, 0) in person units: 150 wide, 75 tall.
function desk(C, dust = false) {
  const ink = C.line, wood = dust ? "#8A6B4E" : "#9A6A3E", dark = dust ? "#6F5743" : "#7A5230";
  let drawers = "";
  for (const x of [-72, 30]) for (let i = 0; i < 3; i++) drawers += poly([[x + 4, -62 + i * 20], [x + 38, -62 + i * 20], [x + 38, -46 + i * 20], [x + 4, -46 + i * 20]], wood, ink, 2.2) + `<rect x="${x + 17}" y="${-55 + i * 20}" width="8" height="2.6" fill="${BRASS}"/>`;
  return poly([[-75, -75], [75, -75], [75, -66], [-75, -66]], dark, ink, 3) +
    poly([[-72, -66], [-30, -66], [-30, 0], [-72, 0]], wood, ink, 3) + poly([[30, -66], [72, -66], [72, 0], [30, 0]], wood, ink, 3) +
    poly([[-30, -66], [30, -66], [30, -22], [-30, -22]], dark, ink, 3) + drawers;
}
// A brass cash register standing on (0, 0) in person units, about 64 wide, 66 tall. flags: text in its window.
function register(C, o = {}) {
  const ink = C.line, b = o.dust ? "#9C8A5E" : BRASS;
  let keys = "";
  for (let r = 0; r < 3; r++) for (let c = 0; c < 5; c++) keys += `<circle cx="${-20 + c * 10}" cy="${-36 + r * 8}" r="3.4" fill="${C.cream}" stroke="${ink}" stroke-width="1.6"/>`;
  const drawerOut = o.drawer ? 26 : 0;
  return poly([[-32, -14], [32, -14], [36, 0], [-36, 0]], b, ink, 3) +
    (o.drawer ? poly([[-30, -12], [30, -12], [34 + drawerOut * 0.2, 10], [-34 - drawerOut * 0.2, 10]], "#7A5230", ink, 3) : "") +
    poly([[-28, -50], [28, -50], [32, -14], [-32, -14]], b, ink, 3) + keys +
    poly([[-20, -66], [20, -66], [22, -50], [-22, -50]], b, ink, 3) +
    poly([[-15, -63], [15, -63], [15, -53], [-15, -53]], C.cream, ink, 2) +
    (o.flags ? osw(0, -55.4, 9.5, o.flags, ink) : "") +
    `<path d="M32,-34 h10 v-10" fill="none" stroke="${ink}" stroke-width="4"/><circle cx="42" cy="-46" r="3.4" fill="${C.war}" stroke="${ink}" stroke-width="1.6"/>` +
    `<path d="M-24,-46 l6,-4 M22,-46 l-5,-4" stroke="${C.orange}" stroke-width="2"/>`;
}
// The military police helmet on its hook, and the nightstick (in place, or lying on the floor).
function helmetHook(C, o = {}) {
  const ink = C.line;
  return `<rect x="-4" y="-6" width="8" height="18" fill="${BRASS}" stroke="${ink}" stroke-width="2"/>` +
    `<path d="M-30,30 Q-30,-6 0,-8 Q30,-6 30,30 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="3"/>` +
    `<path d="M-36,30 H36" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>` +
    `<rect x="-29" y="12" width="58" height="11" fill="${C.slate}"/>` + osw(0, 21.5, 10, "MP", C.cream) +
    (o.stick ? `<g transform="translate(18,40) rotate(8)"><rect x="-3.5" y="0" width="7" height="58" rx="3" fill="#3A2416" stroke="${ink}" stroke-width="2"/></g>` : "") +
    (o.bird ? `<g transform="translate(4,-6)"><path d="M-30,6 Q-22,-8 -8,-4 Q2,-14 12,-6 Q24,-10 30,6 Z" fill="#B98C5A" stroke="${ink}" stroke-width="2"/>` +
      `<circle cx="6" cy="-14" r="8" fill="${C.tan}" stroke="${ink}" stroke-width="2"/><circle cx="8" cy="-16" r="1.8" fill="${ink}"/><path d="M13,-14 l7,2 l-7,2 Z" fill="${C.orange}" stroke="${ink}" stroke-width="1.4"/></g>` : "");
}
// The knife switch on a slate panel, centered on (0, 0) in canvas px: the blade up at OFF.
function knifeSwitch(C) {
  const ink = C.line;
  return poly([[-90, -150], [90, -150], [90, 150], [-90, 150]], C.slate, ink, 5) + `<rect x="-78" y="-138" width="156" height="276" fill="none" stroke="${C.orange}" stroke-width="2.4"/>` +
    osw(0, -108, 30, "OFF", C.cream) + osw(0, 132, 30, "ON", C.cream) +
    `<rect x="-46" y="48" width="92" height="40" fill="${BRASS}" stroke="${ink}" stroke-width="4"/>` +
    [-26, 26].map((x) => `<rect x="${x - 6}" y="20" width="12" height="34" fill="#B5652E" stroke="${ink}" stroke-width="3"/>`).join("") +
    [-26, 26].map((x) => `<path d="M${x},56 L${x - 4},-60" stroke="${ink}" stroke-width="13" stroke-linecap="round"/><path d="M${x},56 L${x - 4},-60" stroke="#D9DDE2" stroke-width="6" stroke-linecap="round"/>`).join("") +
    `<path d="M-34,-60 H26" stroke="${ink}" stroke-width="10"/><rect x="-14" y="-96" width="20" height="40" rx="6" fill="${C.war}" stroke="${ink}" stroke-width="4"/>` +
    [-26, 26].map((x) => `<circle cx="${x}" cy="58" r="7" fill="${BRASS}" stroke="${ink}" stroke-width="3"/>`).join("");
}
// The Super PAC in Part 5's look (storyboards/part-05-*.md, step-4-super-pac; its sketch module draws it), standing on
// (0, 0) in its own units (about 230 wide, 275 tall): a rust canvas backpack, its dark top flap, navy strap arms with
// the fists on its hips, a front pocket with the cream SUPER PAC patch, and a war-red cape (fly: streaming behind;
// hang: hanging down its back).
function superPac(C, cape = "fly") {
  const ink = C.line, SEAM = "#A35A3A";
  const capes = {
    fly: [[-86, -250], [86, -250], [40, -214], [-150, -206], [-280, -236], [-350, -196], [-270, -170], [-340, -130], [-240, -128], [-290, -84], [-170, -110], [-96, -120]],
    hang: [[-86, -250], [86, -250], [134, -6], [100, 12], [66, -2], [34, 14], [0, 0], [-34, 14], [-66, -2], [-100, 12], [-134, -6]],
  };
  const strap = (sx) => `<path d="M${sx * 108},-204 L${sx * 154},-138 L${sx * 113},-94" fill="none" stroke="${ink}" stroke-width="19" stroke-linejoin="round" stroke-linecap="round"/>` +
    `<path d="M${sx * 108},-204 L${sx * 154},-138 L${sx * 113},-94" fill="none" stroke="${C.navy}" stroke-width="13" stroke-linejoin="round" stroke-linecap="round"/>`;
  return poly(capes[cape], C.war, ink, 4) +
    poly([[-104, 0], [-113, -220], [-86, -254], [86, -254], [113, -220], [104, 0]], C.rust, ink, 4) +
    `<path d="M-96,-14 L-103,-214 M96,-14 L103,-214" stroke="${SEAM}" stroke-width="3"/>` +
    poly([[-86, -254], [86, -254], [72, -275], [-72, -275]], "#6E3622", ink, 3.4) +
    strap(-1) + strap(1) +
    poly([[-82, -182], [82, -182], [82, -94], [-82, -94]], SEAM, ink, 3) +
    poly([[-78, -176], [78, -176], [78, -122], [-78, -122]], C.cream, ink, 3) +
    `<rect x="-72" y="-170" width="144" height="42" fill="none" stroke="${C.orange}" stroke-width="2"/>` + osw(0, -137, 27, "SUPER PAC", ink);
}
// A specimen jar standing on (0, 0) in person units (90 wide, 120 tall), with what is inside, the lid and its tag.
function jar(K, C, inside, tag = true) {
  const ink = C.line;
  return `<rect x="-40" y="-108" width="80" height="104" rx="10" fill="${GLASS}" fill-opacity="0.45" stroke="${ink}" stroke-width="3.4"/>` +
    `<rect x="-36" y="-80" width="72" height="72" rx="6" fill="#B8D8C9" opacity="0.55"/>` + inside +
    `<path d="M-30,-96 L-22,-96 L-34,-20 L-38,-28 Z" fill="#FFFFFF" opacity="0.45"/>` +
    poly([[-44, -120], [44, -120], [44, -106], [-44, -106]], C.slate, ink, 3) + poly([[-14, -128], [14, -128], [14, -120], [-14, -120]], C.slate, ink, 2.6) +
    (tag ? at(30, -118, 0.62, K.props.priceTag({ text: "CURED", angle: 26 })) : "");
}
// A rowboat seen from the side, its gunwale at y 0 (about 120 wide in person units).
function rowboat(C) {
  const ink = C.line;
  return poly([[-62, -6], [62, -6], [50, 22], [-46, 22]], "#9A6A3E", ink, 3.4) + `<path d="M-58,4 H58" stroke="${C.orange}" stroke-width="2.4"/>` +
    poly([[-64, -10], [64, -10], [62, -4], [-62, -4]], C.cream, ink, 2.4);
}
// Engraved wave lines round a point on the sea.
function waves(C, x, y, w, n = 3) {
  let d = "";
  for (let i = 0; i < n; i++) { const yy = y + i * 14, xx = x - w / 2 + (i % 2) * 18; d += `M${f(xx)},${f(yy)} q${w / 8},-9 ${w / 4},0 q${w / 8},9 ${w / 4},0 q${w / 8},-9 ${w / 4},0 q${w / 8},9 ${w / 4},0 `; }
  return `<path d="${d}" fill="none" stroke="${C.peri}" stroke-width="3" stroke-linecap="round"/>`;
}
// A puff of smoke wisps rising from (x, y).
function smoke(x, y, s, col = "#8C8782") {
  return [-1, 0, 1].map((i) => `<path d="M${f(x + i * 18 * s)},${f(y)} q${f(-12 * s)},${f(-16 * s)} 0,${f(-32 * s)} q${f(12 * s)},${f(-16 * s)} 0,${f(-32 * s)}" fill="none" stroke="${col}" stroke-width="${f(5 * s)}" stroke-linecap="round"/>`).join("");
}
// A cartoon thumbs-up hand, its wrist at (0, 0), pointing up.
function thumbsUp(C, skin, sleeve) {
  const ink = C.line;
  return poly([[-30, -8], [-6, -10], [-6, 12], [-30, 10]], sleeve || C.slate, ink, 2.6) +
    poly([[-6, -12], [16, -14], [22, -8], [22, 12], [16, 16], [-6, 14]], skin, ink, 2.6) +
    `<path d="M2,-6 H20 M2,1 H21 M2,8 H20" stroke="${ink}" stroke-width="1.6"/>` +
    poly([[2, -12], [10, -14], [12, -36], [8, -40], [3, -38]], skin, ink, 2.6);
}

// ── The plates ────────────────────────────────────────────────────────────
// The TV den, in person units (people at scale 1, feet on y 100): the striped wall, the rust baseboard, the slate
// floor, the TV (size 1.3) at x -150, the coffee table at x -340, the three at x 40, 150, 275, the sharpener at x 395.
function denRoom(C) {
  let stripes = "";
  for (let x = -900; x < 900; x += 44) stripes += `<rect x="${x}" y="-700" width="20" height="790" fill="#CDB680"/>`;
  return `<rect x="-900" y="-700" width="1800" height="790" fill="#D8C493"/>` + stripes +
    `<rect x="-900" y="84" width="1800" height="16" fill="${C.rust}"/><rect x="-900" y="100" width="1800" height="400" fill="#4A5266"/>` +
    `<path d="M-900,100 H900" stroke="${C.line}" stroke-width="3"/>`;
}
function coffeeTable(C) {
  return poly([[-58, -40], [58, -40], [58, -32], [-58, -32]], "#9A6A3E", C.line, 3) +
    `<path d="M-46,-32 L-52,0 M46,-32 L52,0" stroke="${C.line}" stroke-width="6" stroke-linecap="round"/>`;
}
function sharpener(C, o = {}) {
  const ink = C.line;
  return poly([[-30, -70], [30, -70], [30, -62], [-30, -62]], "#9A6A3E", ink, 3) + `<path d="M-22,-62 L-26,0 M22,-62 L26,0" stroke="${ink}" stroke-width="6" stroke-linecap="round"/>` +
    poly([[-18, -108], [18, -108], [18, -70], [-18, -70]], o.charred ? "#3B332C" : C.peri, ink, 3) + `<circle cx="-6" cy="-92" r="7" fill="${C.ink}"/>` +
    `<path d="M18,-92 h16 v-20" fill="none" stroke="${ink}" stroke-width="4"/><circle cx="34" cy="-114" r="5" fill="${o.charred ? "#3B332C" : C.war}" stroke="${ink}" stroke-width="2"/>`;
}
// The economist on the TV screen (TV units: the screen is x -63..17, y -134..-51).
function economist(K, C, charred) {
  const o = { tone: 0, outfit: "suit", head: "long", hairStyle: "slick", color: 1, mood: "smile", look: "right", arms: [[-10, -4], [150, 176]], build: { neck: 1.4, hs: 1.1 }, charred };
  const R = K.rig(o), hand = R.hand[1];
  const p = pencil(C, 44, 7, {});
  return at(-30, -70, 0.62, K.person(o) + at(hand[0], hand[1] - 18, 1, p, -86) +
    (charred ? "" : `<path d="M-9,${f(R.neck[1] + 8)} l9,4 l9,-4 l0,8 l-9,-4 l-9,4 Z" fill="${C.war}" stroke="${C.line}" stroke-width="1.6"/>`));
}

// The wall map, its stations and the office. o: { dust, people (tiny strangers everywhere), blob, jar, crowd }.
function worldMap(K) {
  return K.props.worldMap({ w: 4200 });
}
function officeRoom(K, C, o = {}) {
  const ink = C.line, k = OFF.k, wall = o.dust ? "#C9BC9B" : "#E2D3AC";
  const D = OFF;
  let out = `<rect x="-5200" y="-3600" width="10400" height="${3600 + D.floor}" fill="${wall}"/>` +
    `<rect x="-5200" y="${D.floor - 60}" width="10400" height="60" fill="${C.rust}"/><rect x="-5200" y="${D.floor}" width="10400" height="1400" fill="#4A5266"/>` +
    `<path d="M-5200,${D.floor} H5200" stroke="${ink}" stroke-width="8"/>`;
  out += worldMap(K) + (o.mapArt || "");
  // the door, its glass panel lettered CENTRAL OFFICE, a cobweb across it
  const door = K.props.door({}), dx = D.door;
  out += at(dx, D.floor, k, door) +
    poly([[dx - 34 * k, D.floor - 188 * k], [dx + 34 * k, D.floor - 188 * k], [dx + 34 * k, D.floor - 128 * k], [dx - 34 * k, D.floor - 128 * k]], "#CFE3E2", ink, 14) +
    osw(dx, D.floor - 162 * k, 92, "CENTRAL", C.navy) + osw(dx, D.floor - 140 * k, 92, "OFFICE", C.navy);
  if (o.web) out += cobweb(dx - 48 * k, D.floor - 202 * k, 360, 0, 90, "#FBF6E6", 6) + cobweb(dx + 48 * k, D.floor - 202 * k, 360, 90, 180, "#FBF6E6", 6);
  if (o.web2) out += cobweb(dx - 48 * k, D.floor - 202 * k, 520, 0, 90, "#FBF6E6", 5);
  out += at(D.hook, -150, k, helmetHook(C, { stick: !o.stickDown, bird: o.bird }));
  // the desk, its things, and the swivel chair at its left end, turned to us
  const X = D.desk, top = D.floor - 75 * k, cx = D.chair, seat = D.floor - 52 * k;
  out += at(cx, D.floor, k, chair(C, o.dust)) + at(X, D.floor, k, desk(C, o.dust));
  const phoneX = X - 330;
  out += at(phoneX, top, k, K.props.phone({}).replace('<g class="phone-handset">', o.handset ? '<g class="phone-handset" opacity="0">' : '<g class="phone-handset">')) + at(X - 60, top, k, `<rect x="-16" y="-3" width="32" height="3" fill="#FBF6E6" stroke="${ink}" stroke-width="1"/>`) +
    (o.blueprint ? "" : at(X + 140, top, k, `<rect x="-24" y="-7" width="48" height="7" rx="3.5" fill="#6E8FB8" stroke="${ink}" stroke-width="1.6"/>`)) +
    at(X + 380, top, k * 0.9, register(C, { dust: o.dust, drawer: o.drawer, flags: o.flags }));
  if (o.handset) {
    // the handset off the hook, dangling down the desk's front on its cord
    out += `<path d="M${phoneX + 18 * k},${top - 6 * k} q${10 * k},${26 * k} ${-2 * k},${50 * k}" fill="none" stroke="${ink}" stroke-width="${2.4 * k}"/>` +
      at(phoneX + 16 * k, top + 58 * k, k * 1.6, `<path d="M-6,-14 Q0,-18 4,-12 L6,10 Q2,16 -4,12 Z" fill="${C.slate}" stroke="${ink}" stroke-width="2"/>` + (o.dust ? `<path d="M-7,-14 q4,-5 9,-2 M-8,2 q3,-3 6,0 M-6,10 q4,-3 8,0" stroke="#E4DED0" stroke-width="2.6" fill="none"/>` : ""));
  }
  if (o.spider) {
    // the spider in the chair, leaning back, its feet up on the desk's left end
    const sx = cx + 22 * k, sy = seat, fx = X - 75 * k + 10 * k, col = o.bone ? BONE : "#2A2622";
    const leg = (dx, dy) => `<path d="M${sx},${sy - 10 * k} L${sx + dx * 0.5},${sy - 10 * k + dy - 18 * k} L${sx + dx},${sy - 10 * k + dy}" fill="none" stroke="${ink}" stroke-width="${(o.bone ? 4.2 : 3) * k}" stroke-linejoin="miter"/>` +
      (o.bone ? `<path d="M${sx},${sy - 10 * k} L${sx + dx * 0.5},${sy - 10 * k + dy - 18 * k} L${sx + dx},${sy - 10 * k + dy}" fill="none" stroke="${BONE}" stroke-width="${1.6 * k}" stroke-linejoin="miter"/>` : "");
    out += leg(fx - sx, top - (sy - 10 * k)) + leg(fx - sx + 9 * k, top - (sy - 10 * k)) + at(sx, sy, k * 1.15, spider(C, { up: false, bone: o.bone }), -22);
  }
  if (o.dust) out += `<rect x="-5200" y="-3600" width="10400" height="${3600 + D.floor + 1400}" fill="#8A8170" opacity="0.12"/>`;
  return out;
}

export default {
  "you-dont-need-to-understand-title"(H, fid) {
    const { K, C } = H;
    const cx = 960, cy = 300, rx = 200, ry = 62;
    const orbits = [0, 60, -60].map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = [[0, 0.9], [60, 3.0], [-60, 5.0]].map(([a, th]) => {
      const r = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return at(cx + ex * Math.cos(r) - ey * Math.sin(r), cy + ex * Math.sin(r) + ey * Math.cos(r) - 6, 0.62, K.money("war", 0));
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    // the heading as KIT.titleScene lays it out (16:9): S 163, the lines' baselines at 597, 758 and 862
    const word = (x, y, size, t, anchor = "middle") =>
      `<text x="${x + size * 0.04}" y="${y + size * 0.053}" text-anchor="${anchor}" font-family="Fraunces" font-weight="900" font-size="${size}" fill="${C.deep}">${t}</text>` +
      `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Fraunces" font-weight="900" font-size="${size}" fill="${C.cream}" stroke="${C.cream}" stroke-width="${f(size * 0.044)}" stroke-linejoin="round">${t}</text>`;
    const heading = word(960, 597, 81.6, "BUT YOU DON’T NEED TO") + word(960, 758, 163, "UNDERSTAND") + word(960, 862, 81.6, "ANY OF THAT");
    // YOU just past the D of UNDERSTAND, on its baseline, charred, facing the words; the manual and his bowler at his heels
    const you = stand(K, 1655, 758, 1.9, copy(YOU, { charred: true, look: "left", arms: [[14, 6], [-14, -6]] }));
    const manual = at(1800, 758, 0.62, K.props.manual({}), 84);
    const bowler = at(1590, 756, 1.7, `<path d="M-17,-1 L-13,-18 L0,-23 L13,-18 L17,-1 Z" fill="#2A2622" stroke="${C.line}" stroke-width="2"/><path d="M-28,2 L-22,-3 H22 L28,2 Z" fill="#2A2622" stroke="${C.line}" stroke-width="2"/>`, -10);
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus + heading + manual + smoke(1810, 690, 0.7) + bowler + you;
    return { svg, alt: "The period title card: BUT YOU DON'T NEED TO UNDERSTAND ANY OF THAT in cream on navy under the atom emblem; just past the last D stands YOU, charred black and smoking, hair straight up, only his eyes white, the manual and his bowler smoking at his heels." };
  },

  "juggling-five-steps"(H, fid) {
    const { K, C } = H;
    // YOU juggling on the free wall right of the lectern, feet at y 1066, the five steps wheeling over him
    const you = stand(K, 1500, 1070, 2.35, copy(YOU, { mood: "worried", look: "left", arms: [[-150, -178], [150, 178]] }));
    const sweat = [[1452, 640], [1540, 628], [1430, 690]].map(([x, y]) => `<path d="M${x},${y} q-7,12 0,16 q7,-4 0,-16 Z" fill="${C.cyan}" stroke="${C.line}" stroke-width="2.4"/>`).join("");
    const opt = at(1490, 300, 0.82, K.props.optimitron({ mood: "smile", pop: 62 }));
    const bond = at(1190, 560, 0.9, K.props.bond({ text: "INCENTIVE ALIGNMENT BOND" }), -24);
    const lob = at(1780, 360, 1.05, K.cast("lobbyist", { mood: "smug" }), 28);
    const pac = at(1230, 330, 0.5, superPac(C, "fly"), -18);
    const lap = at(1785, 640, 1.9, K.props.laptop({}).replace("<!--laptop-screen-->", `<path d="M0,-34 V-18 M-8,-26 H8" stroke="${C.med}" stroke-width="5"/>`), 22);
    const swish = [[1330, 205, -30], [1660, 190, 30], [1845, 500, 80], [1130, 430, -80]].map(([x, y, r]) => `<path d="M${x},${y} q30,-18 60,-6" fill="none" stroke="${C.line}" stroke-width="4" stroke-linecap="round" transform="rotate(${r} ${x} ${y})" opacity="0.7"/>`).join("");
    const knees = `<path d="M1450,1010 l-14,8 M1550,1010 l14,8" stroke="${C.line}" stroke-width="4" stroke-linecap="round"/>`;
    const svg = H.host("thinking-small", "thinking", swish + you + sweat + knees + bond + pac + lob + lap + opt);
    return { svg, alt: "Wishonia thinks at her lectern while beside it YOU, the man in the bowler, sweats and wobbles juggling the five steps: the bond, the caped rust Super PAC backpack, the masked Lobbyist, a laptop with a teal cross on its screen and, at the top of the arc, the heavy Optimitron." };
  },

  "pencil-on-tv"(H, fid) {
    const { K, C } = H;
    // the whole den after the boom: everything charred and blinking, the smoke thinning
    const screenArt = economist(K, C, true) + `<path d="M-40,-120 L-26,-96 L-44,-80 M-26,-96 L-4,-104 L8,-84 M-26,-96 L-18,-66" fill="none" stroke="#FBF6E6" stroke-width="2.4"/>`;
    const tv = at(-150, 100, 1.3, K.props.tvSet({ screenColor: "#3B4052" }).replace("<!--tv-screen-->", screenArt));
    const table = at(-340, 100, 1, coffeeTable(C));
    const sci = stand(K, 40, 100, 1, K.castOpts("scientist", { charred: true, look: "left", arms: [[-14, -6], [14, 6]] }));
    const gma = stand(K, 150, 100, 1, copy(OLD, { charred: true, look: "left", arms: [[-14, -6], [14, 6]] }));
    const wm = stand(K, 278, 100, 1, K.castOpts("weaponsMaker", { charred: true, look: "left", arms: [[40, 110], [-40, -110]] }));
    const sharp = at(395, 100, 1, sharpener(C, { charred: true }));
    const puff = `<g opacity="0.28">${at(-150, -40, 0.42, K.nuke())}</g>`;
    const plate = denRoom(C) + table + puff + tv + sci + gma + wm + sharp + smoke(-150, -200, 1.4) + smoke(395, -20, 0.8);
    const svg = view(20, -80, 2.05, plate);
    return { svg, alt: "A 1950s den in thinning smoke: on the TV's cracked screen the economist is charred black, hair straight up, still holding up his pencil; beside the TV the Scientist, the old woman and the Weapons Maker stand charred too, only their eyes white, the pencil sharpener smoking." };
  },

  "pencil-parts-map"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "mines": the mine on the southern continent, the miner popping up out of his shaft black from cap to boots
    const [mx, my] = MP(121, 138);
    const head = `<path d="M-60,0 L-36,-150 L36,-150 L60,0 M-46,-60 H46 M-40,-100 H40 M-36,-150 L-30,-170 H30 L36,-150" fill="none" stroke="#5E3F28" stroke-width="10" stroke-linejoin="miter"/>` +
      `<circle cx="0" cy="-162" r="16" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>`;
    const shaft = `<ellipse cx="0" cy="0" rx="62" ry="16" fill="${C.ink}" stroke="${ink}" stroke-width="3"/>`;
    const miner = `<defs><clipPath id="${fid}-shaft"><rect x="-200" y="-400" width="400" height="400"/></clipPath></defs>` +
      `<g clip-path="url(#${fid}-shaft)">${stand(K, 0, 64, 0.8, { tone: 1, outfit: "overalls", hat: "hard", charred: true, keepHat: true, arms: [[-150, -170], [20, 8]] })}</g>`;
    const lead = at(70, -10, 1, `<rect x="-5" y="-110" width="10" height="110" fill="${C.slate}" stroke="${ink}" stroke-width="2.6"/>`, 22);
    const k = PK / 0.8; // the station is drawn at the people's scale
    const station = at(mx - 120, my + 30, PK * 0.85, head) + at(mx + 110, my + 30, k, shaft + lead + miner);
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="${C.cream}"/>` + view(mx, my - 120, 1.3, worldMap(K) + station);
    return { svg, alt: "Inside the engraved wall map, on the southern continent: a miner pops up out of his mine shaft beside its timber headframe, black with graphite from his hard hat to his boots, only his eyes white, the bare pencil lead sticking out of the shaft; the coast and the engraved sea beyond." };
  },

  "pencil-strangers"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "met.": close on one rowboat of the chain across the sea, the brawl's dust cloud, the eraser shooting out
    const [bx, by] = MP(176, 152);
    const boat = (dx, i) => {
      const o = { tone: (i + 1) % 4, outfit: i % 2 ? "dress" : "shirt", hair: i % 2, color: i % 4, look: dx < 0 ? "right" : "left", arms: [[dx < 0 ? 30 : -30, dx < 0 ? 80 : -80], [dx < 0 ? 40 : -40, dx < 0 ? 90 : -90]] };
      return at(bx + dx, by + (i % 2) * 18, PK, stand(K, -22, 4, 0.8, o) + stand(K, 26, 4, 0.8, copy(o, { tone: (i + 2) % 4, hair: 0, outfit: "shirt" })) + rowboat(C) + waves(C, 0, 34, 150, 1));
    };
    const boats = [-300, 300].map((dx, i) => boat(dx, i)).join("");
    const cloudC = [[-60, -120, 56], [0, -150, 66], [60, -116, 58], [20, -80, 60], [-40, -70, 54], [76, -60, 46]];
    const cloud = cloudC.map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#E9DDBE" stroke="${ink}" stroke-width="4"/>`).join("") + cloudC.map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r - 4}" fill="#E9DDBE"/>`).join("") +
      `<path d="M-70,-130 q10,-8 20,0 M20,-160 q10,-8 20,0 M40,-90 q10,-8 20,0" fill="none" stroke="${ink}" stroke-width="3" opacity="0.5"/>`;
    const fist = (x, y, r, skin) => `<g transform="translate(${x},${y}) rotate(${r})"><rect x="-8" y="-6" width="34" height="12" fill="${C.slate}" stroke="${ink}" stroke-width="2.6"/><path d="M26,-10 h14 l4,4 v12 l-4,4 h-14 Z" fill="${skin}" stroke="${ink}" stroke-width="2.6"/><path d="M34,-10 v20 M40,-8 v16" stroke="${ink}" stroke-width="1.4"/></g>`;
    const bits = K.star(-140, -170, 22, C.yellow) + K.star(130, -210, 18, C.yellow) + K.star(160, -40, 16, C.yellow) +
      fist(-150, -80, 200, "#D9B48F") + fist(110, -140, -20, "#A87B57") + fist(90, -30, 30, "#6F4B33") +
      `<path d="M-60,-232 L-44,-286 L-28,-232 Z" fill="${C.orange}" stroke="${ink}" stroke-width="3" transform="rotate(-24 -44 -260)"/>` +
      `<rect x="30" y="-280" width="40" height="40" fill="${C.peri}" stroke="${ink}" stroke-width="3" transform="rotate(28 50 -260)"/>` +
      `<path d="M-30,-4 l-6,22 h20 l2,-10 Z" fill="#5E3F28" stroke="${ink}" stroke-width="2.4" transform="rotate(-30 -24 8)"/>`;
    const eraser = at(-250, -220, 1, poly([[-26, -14], [26, -14], [26, 14], [-26, 14]], PINK, ink, 3) + `<path d="M34,-6 h40 M34,8 h28" stroke="${ink}" stroke-width="3" stroke-linecap="round"/>`, -18);
    const brawl = at(bx, by, PK, rowboat(C) + cloud + bits + eraser + waves(C, 0, 34, 170, 2));
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="${C.cream}"/>` + view(bx, by - 170, 1.45, worldMap(K) + boats + brawl);
    return { svg, alt: "On the engraved sea of the wall map, a chain of rowboats full of strangers passing parts along; in one boat a cartoon brawl, a dust cloud with fists, a shoe, a cone hat, a cube hat and stars flying out of it, and the pink eraser shooting out of the cloud." };
  },

  "empty-central-office"(H, fid) {
    const { K, C } = H;
    const plate = officeRoom(K, C, { mapArt: mapPeople(K, C, PK, 26), handset: true, web: true, stickDown: true, spider: true }) +
      at(OFF.hook - 120, OFF.floor, OFF.k, `<g transform="rotate(84)"><rect x="-3.5" y="-29" width="7" height="58" rx="3" fill="#3A2416" stroke="${C.line}" stroke-width="2"/></g>`);
    const svg = view(650, -573, 0.25, plate);
    return { svg, alt: "The empty central office: a huge pictorial wall map of the world dotted with little strangers; under it a big desk with the phone's handset dangling off the hook over a blank order pad, and beside it the swivel chair with a little spider leaning back in it, its feet up on the desk; at the right the door lettered CENTRAL OFFICE behind a cobweb, an empty MP helmet on its hook and the nightstick on the floor." };
  },

  "price-system-pencils"(H, fid) {
    const { K, C } = H, ink = C.line, k = OFF.k, top = OFF.floor - 75 * k, rx = OFF.desk + 380;
    // on "pencils.": the register on the desk's right end, its drawer shot out full of pencils spilling over the desk
    let spill = "";
    for (let i = 0; i < 14; i++) {
      const x = rx - 300 + ((i * 71) % 520), y = top - 14 - ((i * 37) % 50), r = ((i * 47) % 140) - 70;
      spill += at(x, y, 1.4, pencil(C, 150, 22), r);
    }
    const flying = [[-160, -330, -60], [120, -260, 40], [-40, -420, -10], [220, -380, 70], [-260, -220, -30]].map(([x, y, r]) => at(rx + x, top + y, 1.4, pencil(C, 150, 22), r)).join("");
    const ring = `<path d="M${rx - 120},${top - 520} l-40,-50 M${rx},${top - 560} l0,-60 M${rx + 120},${top - 520} l40,-50" stroke="${ink}" stroke-width="14" stroke-linecap="round"/>`;
    const plate = officeRoom(K, C, { mapArt: mapPeople(K, C, PK, 26, { greedy: true }), drawer: true, flags: "25¢", spider: true }) + spill + flying + ring;
    const svg = view(OFF.desk + 60, 120, 0.68, plate);
    return { svg, alt: "Close on the office desk under the wall map: the brass cash register on its right end rings by itself, 25¢ in its window, its drawer shot out and pencils spraying out over the desk; the little spider in the swivel chair at the desk's other end, its feet up." };
  },

  "billions-a-day"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "noticing.": a heap of goods taller than the lectern on the free wall, YOU's newspaper sticking out of the top
    const heapPts = [[1130, 1080], [1200, 820], [1300, 680], [1420, 620], [1560, 630], [1680, 700], [1790, 850], [1870, 1080]];
    const loaf = `<path d="M-30,6 Q-32,-14 -10,-16 Q8,-20 24,-12 Q34,-4 30,8 Q0,14 -30,6 Z" fill="#D49A4E" stroke="${ink}" stroke-width="3.2"/><path d="M-16,-8 l8,-6 M-2,-9 l8,-6 M12,-8 l8,-6" stroke="#F3DFB0" stroke-width="3"/>`;
    const shoe = `<path d="M-30,8 L-28,-10 L-6,-12 L4,-2 L30,0 L32,8 Z" fill="#5E3F28" stroke="${ink}" stroke-width="3"/><path d="M-30,8 H32" stroke="${C.ink}" stroke-width="5"/>`;
    let items = "";
    for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) {
      const x = 1150 + c * 82 + (r % 2) * 40, y = 1100 - r * 62, kind = (r * 5 + c * 3) % 4, rot = ((r * 31 + c * 17) % 90) - 45;
      const g = kind === 0 ? at(0, 0, 1.4, pencil(C, 110, 16)) : kind === 1 ? at(0, 0, 1.6, loaf) : kind === 2 ? at(0, 0, 1.5, shoe) : at(0, 26, 0.75, K.props.pillBottle({ pills: false }));
      items += at(x, y, 1, g, rot);
    }
    const hp = heapPts.map((p) => p.join(",")).join(" L");
    const heap = `<defs><clipPath id="${fid}-heap"><path d="M${hp} Z"/></clipPath></defs><path d="M${hp} Z" fill="#B98C5A" stroke="${ink}" stroke-width="5"/>` +
      `<g clip-path="url(#${fid}-heap)">${items}</g><path d="M${hp}" fill="none" stroke="${ink}" stroke-width="5"/>`;
    let cols = "";
    for (let i = 0; i < 5; i++) cols += `<path d="M${-100 + i * 18},-36 v60" stroke="${ink}" stroke-width="2" stroke-dasharray="10 5" opacity="0.6"/>`;
    const paper = at(1490, 590, 1.6, poly([[-112, -54], [0, -60], [0, 40], [-112, 46]], "#F4EFDF", ink, 3) + poly([[0, -60], [112, -54], [112, 46], [0, 40]], "#ECE5D0", ink, 3) +
      cols + `<rect x="18" y="-36" width="70" height="40" fill="#C9C2B0" stroke="${ink}" stroke-width="2"/><path d="M18,14 h70 M18,24 h52" stroke="${ink}" stroke-width="2" stroke-dasharray="8 4" opacity="0.6"/>` +
      `<path d="M30,-58 Q60,-112 104,-58 Z" fill="#F4EFDF" stroke="${ink}" stroke-width="3"/>` + `<path d="M120,-80 q14,-8 22,4 M124,-60 q12,-4 18,6" fill="none" stroke="${ink}" stroke-width="3" stroke-linecap="round"/>`, 6);
    const svg = H.host("eyeroll-closed", "arms-crossed", heap + paper);
    return { svg, alt: "Wishonia rolls her eyes at the camera, arms crossed; beside her lectern a heap of pencils, loaves, shoes and pill bottles taller than the lectern has buried YOU, and only his open newspaper sticks out of the top, a page turning." };
  },

  "cured-disease-jar"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "cure": the patched TV showing the jar; the Scientist and the old woman sitting on the Weapons Maker
    const onScreen = at(-23, -54, 0.66, jar(K, C, at(0, -60, 0.4, K.props.diseaseBlob({ seed: 5, mood: "dead" }), 180), true));
    const tape = `<path d="M-63,-74 L-40,-51 M-40,-74 L-63,-51" stroke="#E9DDBE" stroke-width="8" opacity="0.95"/><path d="M-63,-74 L-40,-51 M-40,-74 L-63,-51" stroke="${ink}" stroke-width="1" opacity="0.4"/>` +
      `<path d="M-52,-62 L-38,-80 L-30,-76 M-52,-62 L-34,-58" fill="none" stroke="#FBF6E6" stroke-width="1.6" opacity="0.8"/>`;
    const bandage = `<g transform="translate(58,-70) rotate(-30)"><rect x="-16" y="-6" width="32" height="12" rx="5" fill="#E9C9A0" stroke="${ink}" stroke-width="2"/><rect x="-5" y="-5" width="10" height="10" fill="#D6B288"/></g>`;
    const tv = at(-150, 100, 1.3, K.props.tvSet({}).replace("<!--tv-screen-->", onScreen + tape) + bandage);
    const table = at(-340, 100, 1, coffeeTable(C));
    // the pile: the Weapons Maker face down along the floor, the two women sitting on his back
    const wm = at(150, 70, 1, `<g transform="rotate(-90)">${K.person(K.castOpts("weaponsMaker", { mood: "grin", arms: [[160, 170], [-160, -170]] }))}</g>`);
    const sci = stand(K, 70, 70, 1, K.castOpts("scientist", { look: "right", mood: "cross", arms: [[-24, -8], [24, 8]], build: { legPose: [[96, 2], [84, -2]], hs: 1.08, legs: 0.95, neck: 0.8 } }));
    const gma = stand(K, 205, 70, 1, copy(OLD, { look: "left", mood: "smug", arms: [[-24, -8], [24, 8]], build: { legPose: [[-96, -2], [-84, 2]], legs: 0.7, hunch: 14 } }));
    const thumb = at(22, 92, 1.1, thumbsUp(C, "#6F4B33", "#5C6F8E"), 180).replace("rotate(180)", "rotate(180) scale(1,-1)");
    const missile = at(395, 96, 1, K.props.missile({ mood: "scared", size: 0.42 }), 90);
    const sharp = at(430, 100, 1, sharpener(C));
    const plate = denRoom(C) + table + tv + sharp + wm + sci + gma + thumb + missile;
    const svg = view(40, -80, 2.05, plate);
    return { svg, alt: "The den again, a strip of tape across the TV's cracked screen and a bandage on its cabinet; on the screen a specimen jar with the disease floating belly up inside and a CURED tag on its lid; beside the TV the Scientist and the old woman sit on the Weapons Maker, his thumbs-up hand poking out, his fresh missile rolling away." };
  },

  "cure-chain-lagos-to-new-york"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "campaign.": New York on the east coast of the left continent: the Rich Human on his hill of bonds, the
    // medicine papers marching inland off the hill to the sign that has just sprung up; the disease out at sea
    const [nx, ny] = MP(116, 62), [sx, sy] = MP(162, 128);
    let hill = `<path d="M-230,40 Q-140,-160 0,-180 Q140,-160 230,40 Z" fill="${C.money}" stroke="${ink}" stroke-width="4"/>`;
    for (let i = 0; i < 9; i++) hill += at(-130 + (i % 5) * 64 + (i > 4 ? 32 : 0), -50 - (i > 4 ? 56 : 0) + (i % 2) * 12, 0.6, K.props.bond({ value: "", text: "BOND" }), ((i * 23) % 40) - 20);
    const rich = stand(K, 0, -160, PK, K.castOpts("richHuman", { mood: "greedy" }));
    const papers = [0, 1, 2, 3].map((i) => at(nx - 290 - i * 95, ny + 40 + (i % 2) * 6, 0.9, `<g transform="scale(-1,1)">${K.money("med", i % 2)}</g>`)).join("");
    const sign = at(nx - 740, ny + 70, 1.8, K.props.sign({ text: "1% TREATY: YES", fontSize: 30 }));
    const blob = at(sx, sy, 2.6, K.props.diseaseBlob({ seed: 5, mood: "smug" })) + waves(C, sx, sy + 14, 520, 2);
    const plate = worldMap(K) + blob + at(nx, ny + 60, 1, hill + rich) + papers + sign;
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="${C.cream}"/>` + view(nx + 50, ny + 240, 0.86, plate);
    return { svg, alt: "Inside the wall map, on the east coast of the left continent: the Rich Human on his hill of bonds with dollar-sign eyes, a line of medicine papers marching off the hill to a campaign sign 1% TREATY: YES; out on the engraved sea, the disease lounges like an old map's sea monster, smug." };
  },

  "cure-chain-delhi-dhaka"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "worked.": the middle of the sea, the disease belly up, the jar coming down over it with the CURED tag
    const [sx, sy] = MP(162, 128), jk = 6;
    const dead = at(0, 0, 2.6, K.props.diseaseBlob({ seed: 5, mood: "dead" }));
    const glass = at(0, -376, jk, `<rect x="-40" y="-108" width="80" height="104" rx="10" fill="${GLASS}" fill-opacity="0.4" stroke="${ink}" stroke-width="3"/>` +
      `<path d="M-30,-96 L-22,-96 L-34,-20 L-38,-28 Z" fill="#FFFFFF" opacity="0.5"/>` +
      poly([[-44, -120], [44, -120], [44, -106], [-44, -106]], C.slate, ink, 3) + poly([[-14, -128], [14, -128], [14, -120], [-14, -120]], C.slate, ink, 2.6) +
      at(30, -118, 0.62, K.props.priceTag({ text: "CURED", angle: 36 })));
    const fall = `<path d="M-330,-1000 v150 M330,-1000 v150 M-250,-1100 v110 M250,-1100 v110" stroke="${ink}" stroke-width="10" stroke-linecap="round"/>`;
    const splash = `<path d="M-300,30 q-40,-50 -14,-90 M300,30 q40,-50 14,-90 M-230,40 q-14,-40 8,-64 M230,40 q14,-40 -8,-64" fill="none" stroke="${C.peri}" stroke-width="9" stroke-linecap="round"/>`;
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="${C.cream}"/>` +
      view(sx, sy - 470, 0.72, worldMap(K) + at(sx, sy, 1, waves(C, 0, 24, 760, 3) + splash + dead + glass + fall));
    return { svg, alt: "In the middle of the wall map's engraved sea, the disease floats dead, eyes crossed out, as a big specimen jar comes down over it from above, a CURED tag swinging on its lid." };
  },

  "millions-cooperated"(H, fid) {
    const { K, C } = H;
    const crowd = mapPeople(K, C, PK, 120) + at(...MP(162, 128), 2.4, jar(K, C, at(0, -60, 0.4, K.props.diseaseBlob({ seed: 5, mood: "dead" }), 180), true));
    const plate = officeRoom(K, C, { mapArt: crowd, handset: true, web: true, web2: true, dust: true, bird: true, spider: true, bone: true, drawer: true, flags: "25¢" }) +
      at(OFF.door - 120, OFF.floor - 1100, 7, spider(C, { thread: true }));
    const svg = view(650, -573, 0.25, plate);
    return { svg, alt: "The same office under thick dust, the wall map now crowded with little people and the CURED jar in its sea: in the swivel chair the spider is a grinning little skeleton with its feet still up on the desk, the handset furry with dust, a bird nesting in the MP helmet, and a baby spider lowering itself to spin a second cobweb across the CENTRAL OFFICE door." };
  },

  "two-numbers-did-it"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "done.": the quiz-show stage, the Scoreboard lit, the paper bowing, three podiums all at 0
    let curtain = `<rect x="-100" y="-100" width="2120" height="1000" fill="${C.rust}"/>`;
    for (let x = -60; x < 2000; x += 90) curtain += `<path d="M${x},-100 V900" stroke="#7A3D25" stroke-width="22"/>`;
    const floor = `<rect x="-100" y="880" width="2120" height="300" fill="${C.slate}"/><path d="M-100,880 H2020" stroke="${ink}" stroke-width="5"/>`;
    // the Scoreboard: navy board, orange edging, mustard bulbs, two windows of cream cards with navy numerals, two posts
    let bulbs = "";
    for (let i = 0; i < 11; i++) bulbs += `<circle cx="${180 + i * 50}" cy="170" r="22" fill="${C.yellow}" opacity="0.25"/><circle cx="${180 + i * 50}" cy="170" r="12" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/>`;
    const board = `<rect x="200" y="420" width="26" height="470" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><rect x="634" y="420" width="26" height="470" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="140" y="140" width="580" height="300" rx="10" fill="${C.navy}" stroke="${ink}" stroke-width="6"/><rect x="152" y="152" width="556" height="276" rx="6" fill="none" stroke="${C.orange}" stroke-width="5"/>` + bulbs +
      [[185, "63.3"], [445, "$2,138"]].map(([x, t]) => `<rect x="${x}" y="225" width="230" height="160" rx="6" fill="${C.cream}" stroke="${ink}" stroke-width="5"/><path d="M${x},305 H${x + 230}" stroke="${ink}" stroke-width="2" opacity="0.5"/>` + num(x + 115, 345, t.length > 4 ? 66 : 92, t, C.navy)).join("");
    // the paper, taking a bow (its top half folded forward)
    const paper = at(800, 790, 1.5, `<g transform="rotate(-38)">${K.money("plain", 1).replace('class="legs"', 'class="legs" opacity="0"')}</g>` +
      `<path d="M-16,30 l-10,40 h-8 M16,30 l6,40 h8" fill="none" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`);
    // the podiums: a box each, a flip card with 0 on its front
    const podium = (x) => poly([[x - 125, 640], [x + 125, 640], [x + 115, 880], [x - 115, 880]], C.navy, ink, 5) + `<path d="M${x - 118},660 H${x + 118}" stroke="${C.orange}" stroke-width="4"/>` +
      `<rect x="${x - 60}" y="690" width="120" height="150" rx="6" fill="${C.cream}" stroke="${ink}" stroke-width="4"/>` + num(x, 810, 120, "0", C.navy);
    // the committee, three suits flattened like pancakes on its podium, the toppled reports on top of them
    const flat = [985, 1060, 1135].map((x, i) => `<g transform="translate(${x},626) scale(1.25,0.28)">${K.person({ tone: i % 4, outfit: "suit", color: 1, look: "right" })}</g>`).join("");
    const peeks = [985, 1060, 1135].map((x) => `<circle cx="${x - 2}" cy="604" r="6.5" fill="#FBF6E6" stroke="${ink}" stroke-width="1.6"/><circle cx="${x + 14}" cy="604" r="6.5" fill="#FBF6E6" stroke="${ink}" stroke-width="1.6"/><circle cx="${x}" cy="605" r="2.4" fill="${ink}"/><circle cx="${x + 16}" cy="605" r="2.4" fill="${ink}"/>`).join("");
    let reports = "";
    for (let i = 0; i < 8; i++) reports += `<rect x="${960 + (i % 4) * 46 + (i > 3 ? 20 : 0)}" y="${592 - (i > 3 ? 22 : 0) - (i % 2) * 6}" width="84" height="22" fill="#FBF6E6" stroke="${ink}" stroke-width="3" transform="rotate(${((i * 13) % 26) - 13} ${1000 + (i % 4) * 46} 600)"/>`;
    const collector = stand(K, 1360, 660, 1.5, { tone: 1, outfit: "dress", hair: 1, color: 2, mood: "sad", look: "left", arms: [[-10, -4], [100, 150]] });
    const cup = at(1300, 520, 1.3, poly([[-14, -24], [14, -24], [12, 6], [-12, 6]], "#AEB4BD", ink, 3));
    const coin = `<ellipse cx="1240" cy="864" rx="20" ry="22" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/><path d="M1206,866 h-34 M1210,852 h-22" stroke="${ink}" stroke-width="3" stroke-linecap="round"/>`;
    const jaw = `<g transform="translate(1760,868) rotate(16) scale(3)"><path d="M-10,0 h20 l-3,6 h-14 Z" fill="${BONE}" stroke="${ink}" stroke-width="1.4"/><path d="M-6,0 v4 M0,0 v5 M6,0 v4" stroke="${ink}" stroke-width="1"/></g>`;
    const plan = at(1660, 660, 2.4, chair(C)) + at(1660, 528, 2.6, spider(C, { up: true, bone: true }));
    const svg = curtain + floor + board + paper + podium(1060) + podium(1360) + podium(1660) + flat + reports + peeks + collector + cup + coin + plan + jaw;
    return { svg, alt: "A 1950s quiz-show stage: the lit Scoreboard reads 63.3 and $2,138, a plain paper bows beside it; three podiums all show 0: the committee flattened under its toppled reports, only their eyes peeking out, the charity collector with an empty cup and the coin rolling away, and the swivel chair with the spider's skeleton, its jaw on the floor." };
  },

  "the-switch"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "switch.": the dark machine on the free wall, the five steps on its hubs, the knife switch at OFF and YOU's hand
    const gk = 2.1, gx = 1490, gy = 600, gears = K.props.gears({ n: 5, dark: true });
    const hubs = [...gears.matchAll(/class="gear" data-i="\d+" data-cx="([-\d.]+)" data-cy="([-\d.]+)"/g)].map((m) => [gx + gk * +m[1], gy + gk * +m[2]]);
    const mounts = [
      (x, y) => at(x, y + 30, 0.6, K.props.bond({ text: "INCENTIVE ALIGNMENT BOND" })),
      (x, y) => stand(K, x, y - 4, 0.72, K.castOpts("lobbyist", {})),
      (x, y) => at(x, y + 10, 0.36, superPac(C, "hang")),
      (x, y) => at(x, y + 6, 1.45, K.props.laptop({}).replace("<!--laptop-screen-->", `<path d="M0,-34 V-18 M-8,-26 H8" stroke="${C.med}" stroke-width="5"/>`)),
      (x, y) => at(x, y + 12, 0.55, K.props.optimitron({ pop: 0 })),
    ];
    const order = hubs.map((h, i) => [h, i]).sort((a, b) => a[0][0] - b[0][0]);
    const machine = at(gx, gy, gk, gears) + order.map(([h], j) => mounts[j](h[0], h[1])).join("");
    const sw = at(1440, 760, 0.78, knifeSwitch(C));
    // YOU's hand from below the frame: a navy suit sleeve, a white shirt cuff, a hand with its finger reaching for the handle
    const arm = poly([[1700, 1090], [1770, 1090], [1600, 880], [1556, 912]], "#24304D", ink, 4) + poly([[1556, 912], [1600, 880], [1584, 858], [1540, 890]], "#FBF6E6", ink, 3);
    const hand = poly([[1540, 890], [1584, 858], [1560, 826], [1524, 798], [1478, 726], [1468, 734], [1500, 800], [1488, 820], [1520, 860]], "#A87B57", ink, 3) +
      `<path d="M1530,836 l-16,-6 M1544,826 l-16,-8" stroke="${ink}" stroke-width="2"/>` +
      `<path d="M1462,722 q-14,-12 -4,-26 q10,-14 -2,-28" fill="none" stroke="#8C8782" stroke-width="4" stroke-linecap="round"/>`;
    const svg = H.host("smirk-closed", "point-right", machine + sw + arm + hand);
    return { svg, alt: "Wishonia points from her lectern at a dark machine beside it: five meshing gears with the five steps bolted to their hubs (the bond, the Lobbyist, the Super PAC, the laptop and the Optimitron), and under them a big knife switch at OFF; YOU's hand reaches up from the bottom of the frame and stops just short of the handle, a wisp of smoke off its fingertip." };
  },
};

// Little people standing on the map's land (scale k), n of them spread over the continents, for the pull-backs.
function mapPeople(K, C, k, n, o = {}) {
  const spots = [[60, 50], [80, 70], [100, 40], [120, 60], [110, 90], [70, 40], [124, 150], [110, 170], [210, 50], [240, 40], [270, 40], [300, 50], [330, 40], [360, 46], [230, 70], [260, 76], [290, 70],
    [210, 100], [230, 120], [220, 150], [300, 105], [340, 150], [355, 165], [330, 115], [352, 121], [140, 30], [196, 52], [284, 98], [306, 102], [199, 108], [128, 64], [90, 100], [250, 100], [320, 64]];
  let out = "";
  for (let i = 0; i < n; i++) {
    const s = spots[i % spots.length], j = Math.floor(i / spots.length), [x, y] = MP(s[0] + (j % 2 ? 9 : -9) * Math.min(j, 1) + (j > 1 ? (j % 3) * 5 : 0), s[1] + (j > 1 ? 7 : 0) + (j > 2 ? 6 : 0));
    out += stand(K, x, y, k, { tone: i % 4, outfit: ["shirt", "dress", "suit", "overalls"][i % 4], hair: i % 4 === 1 ? 1 : 0, color: (i * 3) % 4, mood: o.greedy ? "greedy" : "smile" });
  }
  return out;
}
