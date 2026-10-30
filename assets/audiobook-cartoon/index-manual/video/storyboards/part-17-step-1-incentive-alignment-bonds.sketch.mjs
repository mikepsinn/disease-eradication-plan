// Sketches for storyboards/part-17-step-1-incentive-alignment-bonds.md: each scene's key frame on a 1920 x 1080
// frame (16:9), drawn with the production art (kit.js, film.js and the props library) in Part 2's film look.
// Built into the review sheet by tools/storyboard-sheet.mjs. A plate frame is one framing as the camera sees it.

const f = (n) => n.toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});
const at = (x, y, k, inner, rot) => `<g transform="translate(${f(x)},${f(y)})${rot ? ` rotate(${rot})` : ""}${k !== 1 ? ` scale(${k})` : ""}">${inner}</g>`;
// a person (feet at y 100 in its own units) standing with its feet at (x, g), scale k
const stand = (x, g, k, svg, rot) => at(x, g - 100 * k, k, svg, rot);
const mirror = (inner) => `<g transform="scale(-1,1)">${inner}</g>`;
// A plate framing as KIT.camera places it: plate point (x, y) in the middle of the frame, at scale s.
const view = (x, y, s, inner) => `<g transform="translate(${f(960 - x * s)},${f(540 - y * s)}) scale(${s})">${inner}</g>`;

// Part 2's plate colors (money-loop.html)
const FIELD = "#C8B07B", FIELD_D = "#B89C66", ROAD = "#EEE3C4", ROAD_E = "#B09363", DASH = "#C7AB78";
const WALK = "#E4D6B0", GUTTER = "#A28A5B", STREET = "#B49A68";
const GLASS = "#DCEFF0";

// The cast's options (storyboard, "The cast")
const YOU = { tone: 2, outfit: "suit", hat: "bowler" };
import { READER } from "./part-08-daily-deletion-event.sketch.mjs";

function T(x, y, size, text, fill, o = {}) {
  const { anchor = "middle", font = "Oswald", weight = 600, extra = "" } = o;
  const esc = String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  return `<text x="${f(x)}" y="${f(y)}" text-anchor="${anchor}" font-family="${font}" font-weight="${weight}" font-size="${size}" ${extra} fill="${fill}">${esc}</text>`;
}
const R = (x, y, w, h, fill, ink, sw = 4, extra = "") => `<rect x="${f(x)}" y="${f(y)}" width="${f(w)}" height="${f(h)}" fill="${fill}"${ink ? ` stroke="${ink}" stroke-width="${sw}" stroke-linejoin="round"` : ""} ${extra}/>`;
const PL = (pts, fill, ink, sw = 4, extra = "") => `<path d="M${pts.map((p) => f(p[0]) + "," + f(p[1])).join(" L")} Z" fill="${fill}"${ink ? ` stroke="${ink}" stroke-width="${sw}" stroke-linejoin="round"` : ""} ${extra}/>`;
const LN = (d, col, sw = 4, extra = "") => `<path d="${d}" fill="none" stroke="${col}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round" ${extra}/>`;

// A plain field and a strip of Part 2's cream road (y0..y1) across the frame.
function ground(y0, y1) {
  return R(-100, -100, 2120, 1280, FIELD) + R(-100, y0 - 7, 2120, y1 - y0 + 14, ROAD_E) + R(-100, y0, 2120, y1 - y0, ROAD) +
    `<path d="M-100,${(y0 + y1) / 2} H2020" stroke="${DASH}" stroke-width="7" stroke-dasharray="46 54"/>`;
}
// Part 2's stadium road (straights from -hl to hl at y -rr and rr, bends of radius rr), in plate units.
function stadium(hl, rr, rw, field) {
  const d = `M${-hl},${-rr} H${hl} A${rr},${rr} 0 0,1 ${hl},${rr} H${-hl} A${rr},${rr} 0 0,1 ${-hl},${-rr} Z`;
  return (field ? `<path d="${d}" fill="${field}"/>` : "") + `<path d="${d}" fill="none" stroke="${ROAD_E}" stroke-width="${rw + 14}"/><path d="${d}" fill="none" stroke="${ROAD}" stroke-width="${rw}"/>` +
    `<path d="${d}" fill="none" stroke="${DASH}" stroke-width="7" stroke-dasharray="46 54"/>`;
}

// ── Shared drawings (storyboard, "Shared drawings") ──────────────────────
// The bond booth: a striped kiosk 320 wide standing on y 0, counter top at y -150, the sign on top to y -400.
function booth(C, sign, youInside) {
  const ink = C.line;
  let awn = "", front = "", bunting = "";
  for (let i = 0; i < 8; i++) awn += R(-170 + i * 42.5, -322, 42.5, 48, i % 2 ? C.cream : C.rust);
  for (let i = 0; i < 8; i++) front += R(-160 + i * 40, -122, 40, 122, i % 2 ? C.cream : "#C46A45");
  for (let i = 0; i < 9; i++) bunting += PL([[-160 + i * 40, -274], [-140 + i * 40, -274], [-150 + i * 40, -248]], [C.war, C.cream, C.navy][i % 3], ink, 2);
  return R(-150, -300, 300, 160, "#2E3A5C", ink, 5) + (youInside || "") +
    R(-170, -322, 340, 48, "none", ink, 5) + awn + R(-170, -322, 340, 48, "none", ink, 5) + bunting +
    R(-140, -400, 280, 70, C.cream, ink, 5) + R(-132, -392, 264, 54, "none", C.orange, 2) + T(0, -350, Math.min(40, 240 / (sign.length * 0.5)), sign, ink, { extra: 'letter-spacing="2"' }) +
    LN("M-110,-330 V-322 M110,-330 V-322", ink, 5) +
    R(-170, -152, 340, 30, C.tan, ink, 5) + front + R(-160, -122, 320, 122, "none", ink, 5) +
    R(-40, -96, 80, 14, C.ink, ink, 3);
}
// The glass case: w wide, h tall, standing on y 0 (four short legs), the lid plate CAPPED AT 20%. inside: drawn behind the glass.
function glassCase(C, w, h, inside, legs = true) {
  const ink = C.line, x0 = -w / 2, y0 = -h - (legs ? 24 : 0), yb = legs ? -24 : 0;
  const legsSvg = legs ? [x0 + 14, -x0 - 22].map((x) => R(x, -24, 8, 24, C.navy, ink, 2)).join("") : "";
  return legsSvg + R(x0, y0, w, h, "#9FC7C9", null) + (inside || "") +
    R(x0, y0, w, h, GLASS, ink, 5, 'fill-opacity="0.55"') +
    LN(`M${x0 + 30},${yb - 16} L${x0 + 90},${y0 + 14} M${x0 + 60},${yb - 16} L${x0 + 104},${y0 + 46}`, "#FFFFFF", 6, 'opacity="0.8"') +
    LN(`M${-x0 - 120},${yb - 16} L${-x0 - 60},${y0 + 14}`, "#FFFFFF", 6, 'opacity="0.7"') +
    R(x0 - 10, y0 - 22, w + 20, 22, C.navy, ink, 4) + R(-18, y0 - 34, 36, 12, C.yellow, ink, 3) +
    R(-110, y0 - 19, 220, 16, C.cream, ink, 2) + T(0, y0 - 6, 14, "CAPPED AT 20%", ink, { extra: 'letter-spacing="1.5"' });
}
// Part 5's caped SUPER PAC backpack as Part 5 v3 draws it (the-rally in its sketch module): a rust canvas pack, a
// darker top flap, navy straps for arms, a cream SUPER PAC patch on the front pocket and a war-red cape; no mask.
// 210 wide, 262 tall, on y 0, hands on hips.
function superPac(C, pose = "hips") {
  const ink = C.line;
  const cape = PL([[-96, -258], [96, -258], [210, -230], [270, -170], [236, -150], [262, -100], [214, -96], [226, -40], [150, -40], [120, 0], [-40, 6], [-120, -4], [-130, -60]], C.war, ink, 4);
  const arm = (d) => LN(d, ink, 18) + LN(d, C.navy, 12);
  const arms = pose === "hips" ? arm("M-104,-226 L-170,-160 L-112,-100") + arm("M104,-226 L170,-160 L112,-100") : arm("M-104,-226 L-150,-150 L-190,-210") + arm("M104,-226 L128,-150 L116,-80");
  return cape + PL([[-104, -248], [-92, -262], [92, -262], [104, -248], [114, -28], [102, -6], [-102, -6], [-114, -28]], C.rust, ink, 5) +
    LN("M-96,-20 L-102,-236 M96,-20 L102,-236", "#A35A3A", 3) +
    PL([[-92, -262], [92, -262], [98, -206], [0, -190], [-98, -206]], "#6E3622", ink, 3.6) +
    PL([[-88, -150], [88, -150], [92, -30], [-92, -30]], "#A35A3A", ink, 3.6) +
    R(-78, -132, 156, 54, C.cream, ink, 3) + R(-72, -126, 144, 42, "none", C.orange, 1.6) + T(0, -96, 25, "SUPER PAC", ink, { extra: 'letter-spacing="1.5"' }) + arms;
}
// The cuckoo clock: a carved house 200 wide, its base at y 0, the roof to y -270, weights hanging to y 150.
// out: the Reaper sprung out of its door on a zigzag spring.
function cuckoo(K, C, out) {
  const ink = C.line;
  const spring = out ? LN("M-26,-198 L-48,-180 L-70,-216 L-92,-180 L-114,-216 L-136,-190", "#8C8782", 5) : "";
  const reaper = out ? at(-190, -236, 0.42, K.reaper({ pose: "puppet", arms: [0, 30] }) + at(-64, -10, 0.75, K.props.clipboard({ title: "150,000", items: ["", "", ""] }))) : "";
  return LN("M-40,0 V50 M40,0 V70", "#8C8782", 3, 'stroke-dasharray="6 4"') +
    PL([[-52, 50], [-28, 50], [-24, 90], [-40, 106], [-56, 90]], C.rust, ink, 3) + PL([[28, 70], [52, 70], [56, 110], [40, 126], [24, 110]], C.rust, ink, 3) +
    R(-100, -180, 200, 180, C.tan, ink, 5) + PL([[-122, -170], [0, -270], [122, -170]], C.rust, ink, 5) +
    LN("M-100,-150 H100 M-100,-12 H100", C.navy, 4) +
    R(-26, -220, 52, 44, out ? C.ink : C.navy, ink, 4) +
    `<circle cx="0" cy="-92" r="52" fill="${C.cream}" stroke="${ink}" stroke-width="5"/>` + LN("M0,-92 V-128 M0,-92 L24,-80", ink, 5) +
    R(-62, -38, 124, 26, C.cream, ink, 3) + T(0, -19, 17, "150,000 / DAY", ink) + spring + reaper;
}
// The snail from Part 3's title card (irrationality-reduction-title.html, snail(pid)), facing +x, foot at (0, 0).
function snail(C, pid) {
  const ink = C.line;
  const P = (x, y) => x.toFixed(1) + "," + y.toFixed(1);
  const polyD = (pts) => "M" + pts.map((p) => P(p[0], p[1])).join(" L") + " Z";
  const solid = (pts, col, w) => `<path d="${polyD(pts)}" fill="${ink}" stroke="${ink}" stroke-width="${w || 3.2}" stroke-linejoin="miter" stroke-miterlimit="8"/><path d="${polyD(pts)}" fill="${col}"/>`;
  const body = [[-32, 0], [-29, -4], [-9, -7], [13, -8], [20, -12], [23, -21], [28, -26], [35, -26], [39, -20], [38, -11], [41, -3], [39, 0]];
  const shell = [], sp = [];
  for (let i = 0; i < 12; i++) { const a = (i / 12) * Math.PI * 2; shell.push([-5 + 20 * Math.cos(a), -25 + 19 * Math.sin(a)]); }
  for (let i = 0; i <= 26; i++) { const t = i / 26, b = Math.PI * 0.15 + t * Math.PI * 3.7, r = 16 * (1 - t) + 1.8; sp.push([-5 + r * Math.cos(b), -25 + r * 0.95 * Math.sin(b)]); }
  const stalk = (x0, y0, x1, y1) => {
    const dx = x1 - x0, dy = y1 - y0, L = Math.sqrt(dx * dx + dy * dy), nx = -dy / L, ny = dx / L;
    const q = [[x0 + nx * 2.4, y0 + ny * 2.4], [x1 + nx * 1.3, y1 + ny * 1.3], [x1 - nx * 1.3, y1 - ny * 1.3], [x0 - nx * 2.4, y0 - ny * 2.4]];
    return solid(q, C.cream, 2.6) + `<circle cx="${x1}" cy="${y1}" r="4.4" fill="${C.cream}" stroke="${ink}" stroke-width="2.2"/><circle cx="${x1 + 1.2}" cy="${y1}" r="1.9" fill="${ink}"/>`;
  };
  return stalk(29, -25, 33, -46) + solid(body, C.cream) + `<path d="M33,-15 L39,-14" fill="none" stroke="${ink}" stroke-width="1.8" stroke-linecap="round"/>` +
    solid(shell, C.yellow) + `<path d="M${P(sp[0][0], sp[0][1])}${sp.slice(1).map((p) => " L" + P(p[0], p[1])).join("")}" fill="none" stroke="${ink}" stroke-width="2.4"/>` +
    `<path d="M5,-10 L12,-17 L14,-27" fill="none" stroke="${C.orange}" stroke-width="2.4"/>` + stalk(34, -24, 44, -43);
}
// A billboard on two posts, w x h, its bottom edge at y -60; inside: drawn in the board's own box (0,0 top left).
function billboard(C, w, h, inside) {
  const ink = C.line;
  return R(-w / 2 + 30, -60, 14, 60, C.tan, ink, 3) + R(w / 2 - 44, -60, 14, 60, C.tan, ink, 3) +
    R(-w / 2, -60 - h, w, h, C.cream, ink, 5) + at(-w / 2, -60 - h, 1, inside);
}
// A YES button / sticker.
const yes = (C, r, x = 0, y = 0) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${C.med}" stroke="${C.line}" stroke-width="${f(r * 0.14)}"/>` + T(x, y + r * 0.36, r, "YES", C.cream);
// The politician's grin on a billboard: a big jaw, slick hair, teeth.
function grinFace(C, w, h) {
  const ink = C.line, cx = w * 0.38, cy = h * 0.52, s = h / 200;
  return `<g transform="translate(${f(cx)},${f(cy)}) scale(${f(s)})">` +
    PL([[-60, -70], [50, -80], [70, -20], [66, 60], [20, 90], [-50, 80], [-70, 10]], "#D9B48F", ink, 5) +
    PL([[-66, -60], [-20, -96], [60, -86], [74, -40], [20, -64], [-40, -40]], "#273049", ink, 4) +
    R(-36, 26, 80, 26, "#FFFFFF", ink, 4) + LN("M-16,26 V52 M4,26 V52 M24,26 V52", ink, 3) +
    `<ellipse cx="-20" cy="-14" rx="9" ry="6" fill="#FFFFFF" stroke="${ink}" stroke-width="3"/><ellipse cx="28" cy="-16" rx="9" ry="6" fill="#FFFFFF" stroke="${ink}" stroke-width="3"/>` +
    `</g>` + yes(C, h * 0.2, w * 0.78, h * 0.5);
}
// The "I PREFER LIVING" button, radius r.
const preferButton = (C, r) => `<circle r="${r}" fill="${C.cream}" stroke="${C.line}" stroke-width="${f(r * 0.1)}"/><circle r="${f(r * 0.82)}" fill="none" stroke="${C.war}" stroke-width="${f(r * 0.06)}"/>` +
  T(0, -r * 0.12, r * 0.36, "I PREFER", C.line) + T(0, r * 0.3, r * 0.36, "LIVING", C.line);
// Grandma's BUY BONDS poster held up at hand h (person units), a little price tag drooping off its corner.
function buyBonds(K, C, h, tag) {
  const ink = C.line;
  return at(h[0], h[1], 1, R(-24, -64, 48, 62, C.paper, ink, 2.2) + R(-20, -60, 40, 54, "none", C.war, 1) +
    T(0, -40, 13, "BUY", C.war) + T(0, -22, 13, "BONDS", ink) + LN("M-8,-12 h16", ink, 1.5) +
    (tag ? at(22, -60, 0.32, K.props.priceTag({ text: tag, angle: 64 })) : ""));
}
// Her mug (Shared drawings): a cream diner mug with a rust band, its bottom at y 34, tilted by rot.
function mugSvg(C, rot = 0) {
  const ink = C.line;
  return `<g transform="rotate(${rot})">${R(-34, -46, 68, 80, "#FBF6E6", ink, 5)}<path d="M34,-30 q30,0 30,22 q0,22 -30,22" fill="none" stroke="${ink}" stroke-width="7"/>` +
    `<path d="M34,-30 q30,0 30,22 q0,22 -30,22" fill="none" stroke="#FBF6E6" stroke-width="3"/>${R(-24, -30, 48, 14, C.rust)}</g>`;
}
// The mug standing on the lectern's reading top (KIT.STUDIO.top, 16:9), at x.
const mugOnLectern = (C, x = 930) => at(x, 756, 1, mugSvg(C));
// The glass toll booth (the glass case stood on end), standing on y 0: YOU inside on his stool, the capped 20% on
// two shelves behind him, the striped boom gate lifted on its post at the left.
function glassBooth(K, C) {
  const ink = C.line;
  const shelves = [-196, -116].map((y) => R(-112, y, 128, 8, C.tan, ink, 2) + [0, 1, 2].map((i) => at(-90 + i * 40, y - 15, 0.36, K.money("med", 0))).join("")).join("");
  const you = R(40, -64, 40, 8, C.tan, ink, 2) + LN("M48,-56 V0 M72,-56 V0", ink, 4) + stand(56, -40, 1.05, K.person(copy(YOU, { look: "left", mood: "smug", build: { legPose: [[70, 8], [76, 12]] } })));
  const gate = R(-150, -126, 26, 126, C.slate, ink, 3) +
    at(-137, -112, 1, `<g transform="rotate(-24)">${[0, 1, 2, 3, 4].map((i) => R(-32 - i * 40, -8, 40, 16, i % 2 ? C.cream : C.war, ink, 2.5)).join("")}</g>`);
  return gate + glassCase(C, 240, 270, shelves + you, false);
}
// A plain grey headstone on stick legs (military-industrial-loop's printed corpses).
function walkingStone(K, C, k, legs) {
  return LN(`M-14,-4 l${legs ? -8 : -4},18 h-8 M14,-4 l${legs ? 8 : 4},18 h8`, C.line, 5) + at(0, -4, k, K.props.headstone({ text: "RIP" }));
}

// The war tank (loop-steps-one-two): a slate drum 340 wide, 420 tall, standing on y 0, heaped over its rim with war
// money (missile seals up), a level gauge on its front at `level`, a valve wheel at its foot. No lettering.
function warTank(K, C, level = 0.72) {
  const ink = C.line;
  let heap = "";
  [[-120, -432, -18], [-40, -446, 10], [50, -440, -8], [128, -428, 16], [-80, -470, 22], [10, -484, -12], [96, -466, 6], [-30, -510, 4]].forEach(([x, y, r], i) => { heap += at(x, y, 0.95, K.money("war", i % 2), r); });
  return R(-170, -420, 340, 420, C.slate, ink, 6) + heap + `<ellipse cx="0" cy="-420" rx="170" ry="26" fill="none" stroke="${ink}" stroke-width="6"/>` +
    R(-170, -330, 340, 34, C.war, ink, 4) + at(0, -150, 1.15, K.props.gauge({ mount: "dial", value: level })) +
    R(170, -90, 120, 50, "#3A4766", ink, 5) + `<circle cx="200" cy="-65" r="36" fill="none" stroke="${C.war}" stroke-width="10"/>` + LN("M200,-101 V-29 M164,-65 H236", C.war, 7);
}
// Medicine money walking round the stadium road clockwise, nose to tail in clusters (the pull-back's subject).
function moneyRing(K, hl, rr, clusters, per, gap, k) {
  const L = 4 * hl + 2 * Math.PI * rr;
  const pointAt = (d) => {
    d = ((d % L) + L) % L;
    if (d < 2 * hl) return [-hl + d, -rr];
    d -= 2 * hl;
    if (d < Math.PI * rr) { const a = -Math.PI / 2 + d / rr; return [hl + rr * Math.cos(a), rr * Math.sin(a)]; }
    d -= Math.PI * rr;
    if (d < 2 * hl) return [hl - d, rr];
    d -= 2 * hl;
    const a = Math.PI / 2 + d / rr;
    return [-hl + rr * Math.cos(a), rr * Math.sin(a)];
  };
  let out = "";
  for (let c = 0; c < clusters; c++) for (let j = 0; j < per; j++) {
    const [x, y] = pointAt(c * (L / clusters) + j * gap + 380);
    out += at(x, y - 26 * k, k, K.money("med", (c + j) % 2));
  }
  return out;
}
// The money loop plate, whole (greed-loop-runs, patient-industrial-loop): plate units, the road's straights from
// x -1100 to 1100 at y -700 and 700, bends of radius 700. No sign names a stop; the money going round is the picture.
function moneyLoop(K, C, opts = {}) {
  const ink = C.line, s = 1.4;
  const lab = at(-560, 520, 1.1, K.props.lab({}) + PL([[-180, -260], [180, -260], [200, -230], [-200, -230]], C.rust, ink, 4) + R(-170, -230, 10, 230, C.tan, ink, 3) + R(160, -230, 10, 230, C.tan, ink, 3));
  const hosp = at(-1020, 520, 1.15, K.props.hospital({ label: "" }));
  const reaper = at(-880, 470, 0.5, K.reaper());
  const germs = opts.germsPopped ? [[-1070, 60], [-600, 220]].map(([x, y]) => at(x, y, 1.6, `<g opacity="0.85">${K.star(0, 0, 34, C.yellow)}${K.star(0, 0, 14, "#FFFFFF")}</g>`)).join("") :
    [[-1070, 98], [-600, 262]].map(([x, y]) => at(x, y, 2, K.props.germ({ mood: "grin" }))).join("");
  const stones = opts.stones ? at(-330, 560, 1.1, K.props.headstone({ text: "CANCER" })) + at(-180, 560, 0.75, K.props.headstone({ text: "" }) + at(0, -66, 0.8, K.props.germ({ mood: "dead" }))) + at(-80, 560, 0.45, K.props.headstone({ text: "" })) : "";
  // no bill in a politician's hand in the new system: the senators and the treaty's Politician stand empty-handed
  const down = [[-8, -3], [8, 3]];
  const pac = at(220, 520, 0.85, superPac(C)) + [[-120, 0], [-10, 1], [100, 3]].map(([x, t]) => stand(520 + x * 1.5, 520, s, K.cast("politician", { tone: t, mood: "grin", arms: down }))).join("");
  const toll = at(1080, 790, 1.35, glassBooth(K, C));
  const boothA = at(-820, -770, 1.1, booth(C, "VICTORY BONDS")) + stand(-560, -760, s, K.cast("richHuman", { mask: true }));
  let bunting = "";
  for (let i = 0; i < 9; i++) bunting += PL([[-200 + i * 45, -262], [-178 + i * 45, -262], [-189 + i * 45, -236]], [C.war, C.cream, C.navy][i % 3], ink, 2);
  let awning = "";
  for (let i = 0; i < 8; i++) awning += R(-220 + i * 55, -304, 55, 44, i % 2 ? C.cream : C.med);
  const office = at(-150, -770, 1.1, R(-200, -260, 400, 260, C.cream, ink, 5) + awning + R(-220, -304, 440, 44, "none", ink, 4) + bunting +
    R(-150, -170, 100, 100, "#2E3A5C", ink, 4) + R(40, -170, 90, 170, C.rust, ink, 4) + stand(-100, 0, 1.2, K.cast("loudHuman", { look: "right" })));
  const treaty = at(330, -770, 1.3, K.props.scroll({ text: "1% TREATY", signatures: 1 })) + stand(470, -760, s, K.cast("politician", { mood: "grin", arms: down }));
  const tank = at(820, -770, 1, warTank(K, C)) + stand(820, -1230, s, K.cast("weaponsMaker", {}));
  const funnel = at(1250, -700, 1.2, K.props.colorFlipFunnel({ inN: 2, outN: 2 }));
  const arch = opts.arch ? archSign(K, C, "PATIENT INDUSTRIAL COMPLEX", -1500, 1500, -1720) : "";
  return stadium(1100, 700, 170, FIELD) + office + treaty + tank + funnel + boothA + pac + lab + hosp + reaper + germs + stones +
    moneyRing(K, 1100, 700, 9, 3, 150, 1.5) + toll + arch;
}
// A period arch sign across a road: two posts at x0 and x1, the board on top at y.
function archSign(K, C, text, x0, x1, y) {
  const ink = C.line;
  return R(x0 - 20, y, 40, -y - 640, C.tan, ink, 5) + R(x1 - 20, y, 40, -y - 640, C.tan, ink, 5) +
    `<path d="M${x0 - 60},${y + 30} Q${(x0 + x1) / 2},${y - 140} ${x1 + 60},${y + 30} L${x1 + 60},${y + 130} Q${(x0 + x1) / 2},${y - 40} ${x0 - 60},${y + 130} Z" fill="${C.cream}" stroke="${ink}" stroke-width="8"/>` +
    archWords(K, C, text, x0, x1, y);
}
// The arch's lettering follows the band's middle curve, like a ranch gate: as big as the band is thick, and no
// wider than 80% of the arch.
function archWords(K, C, text, x0, x1, y) {
  const mid = (x0 + x1) / 2, fs = K.fitText(text, 80, (x1 - x0 + 120) * 0.8, "Oswald", 600, 4), drop = fs * 0.33;
  const pid = "arch-" + text.toLowerCase().replace(/[^a-z]+/g, "-");
  return `<defs><path id="${pid}" d="M${x0 - 60},${y + 80 + drop} Q${mid},${y - 90 + drop} ${x1 + 60},${y + 80 + drop}"/></defs>` +
    `<text font-family="Oswald" font-weight="600" font-size="${fs.toFixed(1)}" letter-spacing="4" fill="${C.line}" text-anchor="middle"><textPath href="#${pid}" startOffset="50%">${text}</textPath></text>`;
}
// Part 2's loop road (money-loop.html), whole, small: the press (mirrored, crank left) with the Politician, the factory
// with the Weapons Maker, the house, the pay window and the farm stand; war papers on the road.
function warLoop(K, C, opts = {}) {
  const ink = C.line, s = 1.5, HL = 850, RR = 640;
  const press = at(-560, -760, 1.3, mirror(K.props.printingPress({ seal: "war", tray: 0 })));
  const pol = stand(-880, -760, s, K.cast("politician", {}));
  const factory = at(560, -760, 1.3, K.props.factory({ label: "" }));
  const wm = stand(900, -760, s, K.cast("weaponsMaker", {}));
  const house = at(560, 520, 1.3, K.props.house({ variant: 2 }));
  const stand2 = at(-560, 520, 1.2, R(-130, -120, 260, 120, C.tan, ink, 4) + `<path d="M-150,-240 H150 L130,-190 H-130 Z" fill="${C.cream}" stroke="${ink}" stroke-width="4"/>` + R(-130, -190, 10, 70, C.tan, ink, 3) + R(120, -190, 10, 70, C.tan, ink, 3));
  let papers = "";
  [[-300, -640], [100, -640], [300, -640], [1300, 0], [200, 640], [-300, 640], [-1300, 0]].forEach(([x, y], i) => { papers += at(x, y - 10, 1.1, K.money("war", i % 2)); });
  let pile = "";
  if (opts.mountain) for (let row = 0; row < 7; row++) for (let j = 0; j < 9 - row; j++) pile += at(-300 + j * 60 + row * 30, -760 - row * 62, 0.6, K.props.headstone({ text: "" }));
  const arch = opts.arch ? archSign(K, C, "MILITARY INDUSTRIAL COMPLEX", -1250, 1250, -1600) : "";
  return stadium(HL, RR, 160, FIELD) + press + pol + pile + factory + wm + house + stand2 + papers + arch;
}

export default {
  "title-card"(H, fid) {
    const { K, C } = H;
    // KIT.titleScene's atomic card (16:9): the emblem at (960, 300), rx 200, ry 62, papers at 0.62, after "Bonds."
    const cx = 960, cy = 300, rx = 200, ry = 62, TILT = [0, 60, -60], t = 8.4;
    const orbits = TILT.map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = TILT.map((a, i) => {
      const th = i * 2.1 + t * 2.4, ar = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return at(cx + ex * Math.cos(ar) - ey * Math.sin(ar), cy + ex * Math.sin(ar) + ey * Math.cos(ar) - 6, 0.62, K.money("war", i % 2));
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    // the spilled papers in a heap at the foot of the card
    let heap = "";
    for (let i = 0; i < 46; i++) {
      const u = (i * 0.6180339) % 1, v = (i * 0.4142135) % 1, x = 560 + u * 800, y = 1035 - (1 - Math.abs(u - 0.5) * 2) * 70 * v - 10;
      heap += at(x, y, 0.55, K.money("war", i % 2), Math.round((v - 0.5) * 120));
    }
    // the heading: Fraunces cream with a navy drop shadow (as Part 2's card), the italic line in Inter, the red STEP 1 stamp
    const word = (y, s, text) => {
      const t0 = (dx, dy, extra) => `<text x="${960 + dx}" y="${y + dy}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${s}" ${extra}>${H.esc(text)}</text>`;
      return t0(0.04 * s, 0.053 * s, `fill="${C.ink}"`) + t0(0, 0, `fill="${C.cream}" stroke="${C.cream}" stroke-width="${f(0.044 * s)}" stroke-linejoin="round" style="paint-order:stroke"`);
    };
    const italic = `<text x="960" y="606" text-anchor="middle" font-family="Inter" font-style="italic" font-weight="700" font-size="38" fill="${C.cream}" stroke="${C.navy}" stroke-width="6" style="paint-order:stroke" stroke-linejoin="round">Saving Humanity While Making Everyone Obscenely Wealthy</text>`;
    const stamp = `<g transform="translate(960,654) rotate(-4)">${R(-120, -34, 240, 68, C.war, C.cream, 6)}${R(-110, -25, 220, 50, "none", C.cream, 2)}${T(0, 17, 46, "STEP 1", C.cream, { extra: 'letter-spacing="5"' })}</g>`;
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus + heap +
      word(556, 64, "THE FIVE-STEP PLAN") + italic + stamp + word(786, 108, "SELL INCENTIVE") + word(892, 108, "ALIGNMENT BONDS");
    return { svg, alt: "The period title card: on plain navy under the film's atom, THE FIVE-STEP PLAN, the italic line Saving Humanity While Making Everyone Obscenely Wealthy, a red STEP 1 stamp and SELL INCENTIVE ALIGNMENT BONDS in big cream letters, with a heap of green papers spilled off the jammed orbits at the foot of the card." };
  },

  "financial-instrument"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "instrument.": the rod in its holder on the lectern's side, the paper on the hook skipping toward her, the
    // human lunging after it, the hammock flipped upside down between its posts
    const posts = R(1560, 560, 22, 520, C.tan, ink, 4) + R(1848, 560, 22, 520, C.tan, ink, 4);
    const hammock = LN("M1571,600 Q1715,640 1859,600", ink, 4) + `<path d="M1571,604 Q1715,860 1859,604 Q1715,720 1571,604 Z" fill="#C9A15E" stroke="${ink}" stroke-width="5"/>` +
      LN("M1610,640 Q1715,770 1820,640", C.rust, 6) + LN("M1640,650 Q1715,740 1790,650", C.rust, 6);
    const rod = R(1000, 820, 30, 70, C.slate, ink, 4) + LN("M1015,900 L1300,300", ink, 13) + LN("M1015,900 L1300,300", C.tan, 7) +
      `<circle cx="1045" cy="838" r="22" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>` + LN("M1300,300 Q1240,420 1188,612", "#EEE8D6", 2.5);
    const paper = at(1178, 640, 0.9, K.money("plain", 1), -14);
    const man = stand(1430, 1070, 3.1, K.person({ outfit: "shirt", tone: 1, color: 1, seed: 7, look: "left", mood: "greedy", arms: [[-112, -118], [-98, -108]], build: { legPose: [[-38, -12], [34, 14]] } }));
    const zip = LN("M1650,420 l60,0 M1640,470 l80,0 M1655,520 l60,0", "#8C8782", 5);
    const svg = H.host("smirk-ee", "open-palms", posts + hammock + rod + zip + man + paper);
    return { svg, alt: "Wishonia at her lectern, smirking, as a fishing rod clamped to the lectern reels in a green paper on its hook; a human from the hammock lunges after it with dollar signs in his eyes, his hammock flipped upside down between its posts behind him." };
  },

  "the-arithmetic"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "timeline.": the curb and gutter; the snail rocketing right after the dangling paper, smoke behind it, its
    // sum flapping; the Reaper at his school desk spun round in its wind, his clipboard pages flying
    const bg = R(-100, -100, 2120, 680, FIELD) + R(-100, 560, 2120, 230, WALK) + LN("M-100,640 H2020 M-100,720 H2020", "#CDBE95", 3) +
      R(-100, 780, 2120, 26, "#D8C9A0", ink, 3) + R(-100, 806, 2120, 120, GUTTER) + R(-100, 926, 2120, 200, STREET);
    const desk = R(560, 600, 340, 24, C.tan, ink, 4) + LN("M580,624 L570,770 M880,624 L890,770", ink, 7) + R(600, 624, 260, 44, "#9C6B45", ink, 3);
    const chair = R(800, 520, 120, 16, "#9C6B45", ink, 3) + LN("M900,536 V770 M820,536 V770", ink, 6);
    const reaper = at(760, 560, 1.35, K.reaper(), 9);
    const pages = [[1010, 360, 30], [1110, 290, -20], [1190, 400, 50], [1080, 200, 70]].map(([x, y, r]) => at(x, y, 1, R(-36, -46, 72, 92, "#FBF6E6", ink, 3) + LN("M-24,-28 h20 M-24,-14 h48 M-24,0 h40 M-24,14 h48", ink, 2), r)).join("");
    const wind = LN("M960,600 q60,-30 120,0 M940,680 q80,-30 160,0 M1000,740 q60,-20 120,0", "#FFFFFF", 5, 'opacity="0.8"');
    let smoke = "";
    for (let i = 0; i < 7; i++) smoke += `<circle cx="${1240 - i * 90}" cy="${812 - (i % 2) * 14}" r="${26 + i * 7}" fill="#D9D4C8" stroke="${ink}" stroke-width="3" opacity="${f(1 - i * 0.11)}"/>`;
    const sum = at(1300, 760, 1, `<path d="M-30,-40 C-90,-60 -140,-30 -200,-50 L-196,-10 C-140,10 -90,-20 -30,0 Z" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>` + T(-110, -22, 20, "27.2 × 0.8 = ...", ink, { font: "Inter", weight: 600, extra: 'transform="rotate(-4 -110 -22)"' }));
    const sn = at(1360, 812, 4.2, snail(C, fid + "s"));
    const line = LN("M1640,-20 V640", "#EEE8D6", 2.5) + at(1640, 680, 0.95, K.money("plain", 0));
    const svg = bg + chair + reaper + desk + pages + wind + smoke + sum + sn + line;
    return { svg, alt: "A sidewalk and gutter: the snail rockets along the gutter after a green paper dangling on a fishing line, a smoke trail behind it and its sum flapping on its shell, while the Grim Reaper at his curbside school desk is spun round by its wind, the pages of his tally clipboard flying." };
  },

  "heres-one"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "one.": the bond flat on the reading top under her palms, the mug in the air above the lectern, the seal glinting
    const bond = at(760, 800, 1.45, K.props.bond({ text: "INCENTIVE ALIGNMENT BOND" }));
    const mug = at(1000, 640, 1, mugSvg(C, 14) + LN("M-50,70 l-10,22 M0,80 v24 M50,70 l10,22", ink, 4));
    const glint = at(760 + 54 * 1.45, 800 - 34 * 1.45, 1, K.star(0, 0, 40, C.yellow) + K.star(0, 0, 16, "#FFFFFF"));
    const svg = H.host("smirk-smile", "palms-down", bond + glint + mug);
    return { svg, alt: "Wishonia at her lectern slaps a green-bordered INCENTIVE ALIGNMENT BOND certificate down on its top; her coffee mug jumps into the air and the bond's gold seal glints." };
  },

  "bond-splits-three-ways"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "transparent.": the long glass case shut over the two narrow lanes, a bill walking in each, the Lobbyist's
    // masked face pressed to its glass and fogging it, his gloved fingers flat under the lid
    // the plate seen across the case: the Lobbyist stands behind it, so we see him through both panes
    const bg = R(-100, -100, 2120, 1280, FIELD) + R(-100, 880, 2120, 300, FIELD_D);
    const lob = K.castOpts("lobbyist", { look: "right", mood: "worried", arms: [[150, 175], [150, 178]], build: { hunch: 4 } });
    const LK = 3.6, LG = 1060, lobby = stand(1060, LG, LK, K.person(lob)), lr = K.rig(lob);
    const x0 = 140, x1 = 1780, top = 470, bot = 880;
    const back = R(x0, top, x1 - x0, bot - top, GLASS, null, 0, 'fill-opacity="0.16"');
    const lanes = R(x0, 760, x1 - x0, 46, ROAD_E) + R(x0, 764, x1 - x0, 38, ROAD) + R(x0, 826, x1 - x0, 46, ROAD_E) + R(x0, 830, x1 - x0, 38, ROAD);
    const bills = at(420, 750, 1.35, K.money("med", 1)) + at(1480, 818, 1.35, K.money("med", 0)) + at(760, 818, 1.35, K.money("med", 0)) + at(1240, 750, 1.35, K.money("med", 1));
    const fog = `<ellipse cx="${f(1060 + LK * lr.mouth[0])}" cy="${f(LG - 100 * LK + LK * lr.eyes[1] + 10)}" rx="66" ry="46" fill="#FFFFFF" opacity="0.32"/>`;
    const front = R(x0, top, x1 - x0, bot - top, GLASS, ink, 6, 'fill-opacity="0.22"') +
      LN(`M${x0 + 40},${bot - 20} L${x0 + 120},${top + 20} M${x0 + 80},${bot - 20} L${x0 + 140},${top + 60} M${x1 - 200},${bot - 20} L${x1 - 120},${top + 20}`, "#FFFFFF", 7, 'opacity="0.7"');
    // the lid, slammed down on his gloved fingers, and the plate on it
    const lid = R(x0 - 14, top - 30, x1 - x0 + 28, 30, C.navy, ink, 5) + R(940, top - 46, 40, 16, C.yellow, ink, 3) +
      R(660, top - 26, 300, 22, C.cream, ink, 2) + T(810, top - 9, 19, "CAPPED AT 20%", ink, { extra: 'letter-spacing="2"' });
    const fingers = lr.hand.map((h) => 1060 + LK * h[0]).map((x) => `<path d="M${f(x - 26)},${top - 34} h52 l4,-22 h-60 Z" fill="${C.ink}" stroke="${ink}" stroke-width="3"/>`).join("") +
      LN(`M1000,${top - 80} l-20,-24 M1100,${top - 92} v-30 M1200,${top - 80} l20,-24`, "#8C8782", 5);
    const svg = bg + lobby + back + lanes + bills + fog + front + lid + fingers;
    return { svg, alt: "A long glass case shut over two narrow lanes, its lid plate reading CAPPED AT 20% and medicine bills walking inside it in plain view; the masked Lobbyist leans in and presses his face to the glass, fogging it, his gloved fingers caught flat under the lid." };
  },

  "wishocratic-allocation"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "nothing.": the government steps, the Optimitron on its table, the Politician blowing on a burnt, smoking
    // card and sliding it into his pocket; the velvet rope still shut at the left of the frame
    const bg = R(-100, -100, 2120, 1280, FIELD);
    const cap = at(1180, 760, 2.1, K.props.capitol({}));
    const steps = [0, 1, 2].map((i) => R(380 - i * 30, 760 + i * 40, 1600 + i * 60, 40, i % 2 ? "#E6DCC0" : "#D9CDAA", ink, 3)).join("");
    const table = R(980, 620, 300, 20, C.tan, ink, 4) + LN("M1000,640 L990,860 M1260,640 L1270,860", ink, 7);
    const opt = at(1130, 620, 1.2, K.props.optimitron({ card: "WORKING", pop: 30, mood: "smile" }));
    // the card held up in front of his face (person units, inside his group), smoking; he blows on it
    const polO = K.castOpts("politician", { look: "left", mood: "smug", arms: [[-100, 157], [20, 40]] });
    const Rr = K.rig(polO), h0 = Rr.hand[0];
    const card = at(h0[0] - 22, h0[1] - 8, 1, `<g transform="rotate(-10)">${R(-30, -19, 60, 38, "#3A2A20", ink, 1.6)}${T(0, -4, 5.6, "EXPENSIVE WAY TO", "#7A6A58")}${T(0, 5, 5.6, "ACCOMPLISH NOTHING", "#7A6A58")}</g>` +
      LN("M-14,-24 q-6,-12 2,-22 M4,-24 q-6,-14 3,-26", "#8C8782", 2.4));
    const blow = LN(`M${Rr.mouth[0] - 3},${Rr.mouth[1]} q-5,-1 -9,-5 M${Rr.mouth[0] - 3},${Rr.mouth[1] + 3} q-6,1 -10,0`, "#FFFFFF", 1.6);
    const pol = stand(1560, 860, 2.6, K.person(polO) + card + blow);
    const rope = R(70, 560, 22, 300, C.yellow, ink, 4) + R(330, 560, 22, 300, C.yellow, ink, 4) + `<circle cx="81" cy="556" r="18" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/><circle cx="341" cy="556" r="18" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/>` +
      LN("M92,600 Q216,700 330,600", "#8E1C17", 16) + at(211, 690, 1, R(-90, 0, 180, 54, C.cream, ink, 3) + T(0, 22, 17, "NO MONEY PAST", ink) + T(0, 44, 17, "THIS ROPE", ink));
    const svg = bg + cap + steps + rope + table + opt + pol;
    return { svg, alt: "On the steps of a domed government building, the Politician blows on a burnt, smoking card, EXPENSIVE WAY TO ACCOMPLISH NOTHING, as he slides it toward his pocket; beside him the orange Optimitron on its table pops a WORKING card, and at the left a velvet rope reads NO MONEY PAST THIS ROPE." };
  },

  "slow-sip"(H, fid) {
    const { C } = H;
    // after "grandparents": the mug just set down on the reading top, a curl of steam over it; her eyes on the camera
    const steam = LN("M918,690 q-14,-20 0,-40 q14,-20 0,-40 M944,694 q-12,-18 0,-36 q12,-18 0,-34", "#FFFFFF", 5, 'opacity="0.75"');
    const svg = H.host("sideeye-closed", "idle", mugOnLectern(C) + steam);
    return { svg, alt: "Wishonia at her lectern side-eyes the camera, her coffee mug just set down on the lectern's top with a curl of steam over it." };
  },

  "grandmas-war-bond"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "eighty-seven.": Grandma a grinning skeleton in front of her WAR BONDS booth, poster up, its 4% tag drooping,
    // her headstone 1987 in front of her
    const bg = R(-100, -100, 2120, 1280, FIELD) + R(-100, 860, 2120, 300, WALK) + LN("M-100,860 H2020", "#CDBE95", 4);
    const b1 = at(760, 860, 1.7, booth(C, "WAR BONDS"));
    const b2 = at(1640, 860, 1.7, booth(C, "VICTORY BONDS", stand(0, -40, 1.05, K.person(copy(YOU, { look: "left", mood: "smile" })))));
    const g = K.castOpts("grandma", {});
    const gr = stand(560, 900, 2.6, K.person(copy(g, { skeleton: true })) + buyBonds(K, C, K.rig(g).hand[0], "4%"));
    const stone = at(800, 930, 1.6, K.props.headstone({ text: "1987" }));
    const svg = bg + b1 + b2 + gr + stone;
    return { svg, alt: "Grandma as a grinning skeleton in her curlers and cat-eye glasses, still holding up her BUY BONDS poster with a little 4% tag drooping from it, a small headstone reading 1987 in front of her and her WAR BONDS booth behind; YOU waits behind the VICTORY BONDS booth next door." };
  },

  "what-youre-offering"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "bonus).": both booths; skeleton Grandma nodding at YOU; at YOU's counter the masked Rich Human tipped forward
    // by a hubcap-size button, the 272% tag on his bond (no briefcase: that is the Lobbyist's); the dead CANCER blob
    const bg = R(-100, -100, 2120, 1280, FIELD) + R(-100, 840, 2120, 300, WALK) + LN("M-100,840 H2020", "#CDBE95", 4);
    const b1 = at(380, 840, 1.25, booth(C, "WAR BONDS"));
    const b2 = at(1360, 840, 1.25, booth(C, "VICTORY BONDS", stand(0, -40, 1.05, K.person(copy(YOU, { look: "left", mood: "smile" })))));
    const g = K.castOpts("grandma", { look: "right" });
    const gr = stand(600, 880, 1.9, K.person(copy(g, { skeleton: true })) + buyBonds(K, C, K.rig(g).hand[0], "4%"), 8);
    const stone = at(470, 900, 1.1, K.props.headstone({ text: "1987" }));
    // the Rich Human (person units inside his group): the VICTORY bond up in the front hand with the 272% tag swinging
    // off it, the hubcap button on his chest; the whole of him tipped toward the counter
    const rh = K.castOpts("richHuman", { mask: true, look: "right", mood: "greedy", arms: [[10, 5], [150, 170]] });
    const Rh = K.rig(rh), hb = Rh.hand[1];
    const bond = at(hb[0], hb[1], 0.34, K.props.bond({ text: "VICTORY BOND", seal: "med" }), -8) + at(hb[0] + 26, hb[1] - 30, 0.95, K.props.priceTag({ text: "272%", angle: 40 }));
    const rich = stand(1080, 900, 2.5, K.person(rh) + at(6, Rh.shoulder[1][1] + 22, 1, preferButton(C, 24)) + bond, 14);
    const blob = at(880, 980, 0.9, K.props.diseaseBlob({ mood: "dead", label: "CANCER", color: "war" }));
    const scroll = `<path d="M1010,880 Q1060,930 1180,940 L1540,950" fill="none" stroke="${ink}" stroke-width="40"/><path d="M1010,880 Q1060,930 1180,940 L1540,950" fill="none" stroke="#FBF6E6" stroke-width="32"/>`;
    const svg = bg + b1 + b2 + scroll + stone + gr + blob + rich;
    return { svg, alt: "Two bond booths: on the left skeleton Grandma with her BUY BONDS poster nods across at YOU behind the VICTORY BONDS counter; at his counter the Rich Human in a domino mask is tipped forward by a hubcap-size I PREFER LIVING button, a huge 272% tag swinging from his bond, and a dead disease blob in a CANCER sash flat on the sidewalk." };
  },

  "enemy-is-the-clock"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "clock.": the machine's front, the Reaper sprung out of the cuckoo clock mid-mark, the three leaning out of
    // their hatches under NOT THE ENEMY signs, all looking up at him, their waves frozen
    const bg = R(-100, -100, 2120, 1280, FIELD) + R(-100, 900, 2120, 300, FIELD_D);
    let rivets = "";
    for (let x = 140; x <= 1780; x += 80) rivets += `<circle cx="${x}" cy="130" r="6" fill="#4A5570"/><circle cx="${x}" cy="880" r="6" fill="#4A5570"/>`;
    const lamps = [...Array(12)].map((_, i) => `<circle cx="${300 + i * 110}" cy="180" r="16" fill="${i % 3 ? C.yellow : C.orange}" stroke="${ink}" stroke-width="4"/>`).join("");
    const mach = R(100, 100, 1720, 1060, C.slate, ink, 7) + rivets + lamps +
      [230, 1690].map((x) => `<circle cx="${x}" cy="330" r="100" fill="#1B2236" stroke="${ink}" stroke-width="6"/>` + at(x, 380, 0.75, K.props.gears({ dark: true, n: 3 }))).join("");
    const hatch = (x, who) => R(x - 160, 520, 320, 380, "#141B2B", ink, 6) + who + R(x - 170, 760, 340, 400, "#3A4766", ink, 6) +
      PL([[x + 160, 520], [x + 230, 540], [x + 230, 880], [x + 160, 900]], "#3A4766", ink, 5);
    // each one leans out of his hatch looking up at the clock; a little sign on a stick over each head
    const lean = (name, extra) => K.cast(name, copy({ mood: "worried", arms: [[-160, -150], [-10, -5]] }, extra));
    const sign = (x, y, text, k) => at(x, y, k, K.props.sign({ text, posts: 1, height: 70 }));
    const ppl = hatch(520, stand(520, 1010, 2.4, lean("lobbyist", { look: "right" }))) +
      hatch(1400, stand(1400, 910, 2.6, K.cast("weaponsMaker", { look: "left", mood: "worried" })));
    const mid = hatch(960, stand(960, 1010, 2.4, lean("politician", { look: "left", arms: [[-10, -5], [160, 150]] })));
    const signs = sign(470, 600, "NOT THE ENEMY", 0.85) + sign(1080, 600, "NOT THE ENEMY", 0.85) + sign(1560, 560, "NOT THE ENEMY", 0.85) +
      at(1250, 700, 0.55, K.props.sign({ text: "NOT THE ENEMY (PROBABLY)", posts: 1, height: 40 }));
    const clock = at(960, 360, 0.9, cuckoo(K, C, true));
    const svg = bg + mach + ppl + mid + clock + signs;
    return { svg, alt: "The front of a huge slate machine: the Grim Reaper springs out of a cuckoo clock hung on it, mid tally mark, while below him the Lobbyist, the Politician and the Weapons Maker lean out of three hatches under little NOT THE ENEMY signs, a smaller one on the baby missile reading NOT THE ENEMY (PROBABLY), all three looking up at him." };
  },

  "stop-reading"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "step:": her fist down on the lectern; the reader in his armchair beside it jolted awake, his book upside down
    const lamp = LN("M1820,1080 V420", ink, 9) + LN("M1820,1080 V420", "#8C8782", 4) + PL([[1740, 430], [1900, 430], [1860, 320], [1780, 320]], C.yellow, ink, 5);
    // the wingback armchair behind him (its back, wings and arms), then the reader seated in it facing her, the book
    // held open upside down in both hands (person units, inside his group)
    const chair = PL([[1330, 1080], [1330, 600], [1360, 500], [1720, 500], [1750, 600], [1750, 1080]], C.orange, ink, 6) +
      PL([[1300, 600], [1360, 560], [1370, 760], [1300, 780]], "#C9732E", ink, 5) +
      PL([[1290, 820], [1420, 800], [1420, 1080], [1290, 1080]], "#C9732E", ink, 5) + PL([[1660, 800], [1790, 820], [1790, 1080], [1660, 1080]], "#C9732E", ink, 5);
    const seat = { look: "left", mood: "worried", arms: [[-120, -160], [-130, -170]], build: { legPose: [[-88, 3], [-93, -2]] } };
    const Rr = K.rig(copy(READER, seat)), bh = [(Rr.hand[0][0] + Rr.hand[1][0]) / 2, (Rr.hand[0][1] + Rr.hand[1][1]) / 2];
    const book = at(bh[0] - 4, bh[1] + 14, 0.42, K.props.manual({}), 180);
    const reader = stand(1560, 1060, 3.4, K.person(copy(READER, seat)) + book);
    const jolt = LN("M1470,420 l-40,-30 M1520,390 l-10,-46 M1580,400 l26,-40", ink, 6);
    const thunk = LN("M1000,770 l40,-24 M1010,800 l50,0 M1000,830 l40,24", ink, 5);
    const svg = H.host("annoyed-closed", "fist", lamp + chair + reader + jolt + thunk);
    return { svg, alt: "Wishonia, annoyed, brings her fist down on the lectern; beside her the reader in his orange wingback armchair jolts awake under his floor lamp, holding his book open upside down." };
  },

  "loop-steps-one-two"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "spending:": the war tank, heaped over its rim with war money, pouring war money into the color-flip funnel,
    // its gauge one notch down, the Weapons Maker sitting on the heap glancing down mid-shrug. No lettering on it.
    const bg = ground(880, 1010);
    const tank = at(700, 890, 1.1, warTank(K, C, 0.72));
    const wm = K.castOpts("weaponsMaker", { look: "left", mood: "flat", build: { legPose: [[80, 10], [86, 14]] } });
    const maker = stand(700, 400, 2.0, K.person(wm));
    const shrug = LN("M580,190 l-26,-26 M820,190 l26,-26", ink, 5);
    let pour = "";
    [[1050, 790, -10], [1130, 700, 20], [1210, 620, -30], [1300, 550, 10], [1390, 500, 40]].forEach(([x, y, r], i) => { pour += at(x, y, 1.2, K.money("war", i % 2), r); });
    const funnel = at(1500, 960, 1.95, K.props.colorFlipFunnel({ inN: 3, outN: 2 }));
    const svg = bg + tank + pour + funnel + maker + shrug;
    return { svg, alt: "A slate drum heaped over its rim with green war money pours war money out of its valve into the striped color-flip funnel over the road, its gauge one notch down; the Weapons Maker sitting on the heap glances down at the gauge and shrugs, his baby missile in his arms." };
  },

  "loop-steps-three-four"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "not.": the Rich Human flat on his back at YOU's booth like a tipped egg, the NOT A TYPO check in his hands,
    // 272% big in the sky over him, the bill that ran the check across the infield looking down at him
    const bg = R(-100, -100, 2120, 1280, FIELD) + R(-100, 880, 2120, 300, FIELD_D);
    const b = at(1440, 880, 1.6, booth(C, "VICTORY BONDS", stand(0, -40, 1.05, K.person(copy(YOU, { look: "left", mood: "worried" })))));
    const runner = at(400, 803, 1.6, K.money("med", 1), 6);
    // flat on his back: his person's +x points up on screen, so arms at 90 degrees hold the check up to the sky;
    // the check is drawn upright inside the turned group (counter-rotated)
    const rh = K.castOpts("richHuman", { mask: true, mood: "greedy", arms: [[95, 85], [85, 95]] });
    const Rh = K.rig(rh), hc = [(Rh.hand[0][0] + Rh.hand[1][0]) / 2, (Rh.hand[0][1] + Rh.hand[1][1]) / 2];
    const check = at(hc[0] + 40, hc[1], 1 / 2.6, `<g transform="rotate(104)">${R(-190, -60, 380, 120, "#EAF3E2", ink, 5)}${R(-180, -50, 360, 100, "none", C.moneyDark, 2)}` +
      `${T(-166, -20, 18, "PAY TO THE BEARER", C.moneyDark, { anchor: "start" })}${T(-166, 30, 30, "$2.72 BILLION / YEAR", ink, { anchor: "start", font: "Fraunces", weight: 900 })}` +
      `${at(120, -2, 0.8, K.props.stampMark({ text: "NOT A\nTYPO", fontSize: 30, angle: -12 }))}</g>`);
    const rich = at(700, 840, 2.6, `<g transform="rotate(-104)">${K.person(rh)}${check}</g>`);
    const rock = LN("M560,930 q-30,-10 -40,-40 M900,930 q30,-10 40,-40", ink, 5);
    const big = H.big(820, 240, 190, "272%", "middle", C.navy);
    const svg = bg + runner + b + rich + rock + big;
    return { svg, alt: "The Rich Human in his domino mask lies flat on his back beside YOU's VICTORY BONDS booth like a tipped egg, holding up a check for $2.72 BILLION / YEAR stamped NOT A TYPO, with 272% standing big in the sky above him and the medicine bill that brought the check looking down at him." };
  },

  "count-five"(H, fid) {
    const { C } = H;
    // on "Five.": palms flat on the lectern, her eyes rolled up to the ceiling, the mug beside her hand
    const svg = H.host("eyeroll-closed", "palms-down", mugOnLectern(C));
    return { svg, alt: "Wishonia at her lectern, palms flat on its top, rolls her eyes up to the ceiling; her coffee mug stands beside her hand." };
  },

  "pavlovian-senators"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "senators.": three senators sitting up like trained dogs in front of their billboards, the three-sticker one
    // with a YES biscuit in his teeth, tongue out; the Super PAC beside its trembling bell
    const bg = R(-100, -100, 2120, 1280, FIELD) + R(-100, 880, 2120, 300, FIELD_D);
    // billboards that grow with the stickers (the third runs off the top), the senators sitting up in front of them:
    // haunches down, hands up like paws, tongues out (person units, inside each senator's group)
    const board = (k) => billboard(C, 300, 180, grinFace(C, 300, 180));
    const b1 = at(860, 700, 1, board()), b2 = at(1260, 660, 1.35, board()), b3 = at(1690, 560, 2.2, board());
    const beg = (tone) => ({ tone, look: "right", mood: "eager", arms: [[150, 20], [140, 15]], build: { legPose: [[96, -10], [100, -14]] } });
    const dog = (x, tone, n, k, extra = "") => {
      const o = K.castOpts("politician", beg(tone)), r = K.rig(o);
      const tongue = `<path d="M${f(r.mouth[0] - 2)},${f(r.mouth[1] + 1)} q3,10 6,0 Z" fill="#D9707A" stroke="${ink}" stroke-width="1.2"/>`;
      const stickers = [...Array(n)].map((_, i) => yes(C, 6.5, -10 + i * 11, r.shoulder[0][1] + 18 + (i % 2) * 8)).join("");
      const wag = LN(`M18,${f(r.hipY - 14)} q12,-6 14,-18 M20,${f(r.hipY - 4)} q14,-2 20,-12`, ink, 1.6);
      return stand(x, 920, k, K.person(o) + tongue + stickers + wag + extra);
    };
    const r3 = K.rig(K.castOpts("politician", beg(1)));
    const biscuit = at(r3.mouth[0] + 12, r3.mouth[1] + 2, 0.34, `<path d="M-40,-10 a12,12 0 1 1 10,-12 h60 a12,12 0 1 1 10,12 v20 a12,12 0 1 1 -10,12 h-60 a12,12 0 1 1 -10,-12 Z" fill="#D9A55E" stroke="${ink}" stroke-width="4"/>` + T(0, 10, 24, "YES", ink));
    const sens = dog(860, 0, 1, 2.5) + dog(1260, 3, 2, 2.5) + dog(1690, 1, 3, 2.7, biscuit);
    const pac = at(300, 920, 1.55, superPac(C));
    const bell = at(640, 920, 1.5, R(-46, -26, 92, 26, "#9C6B45", ink, 4) + `<path d="M-38,-26 Q-38,-84 0,-86 Q38,-84 38,-26 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M-20,-60 Q-16,-76 0,-78" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.7"/><rect x="-5" y="-100" width="10" height="14" fill="${ink}"/><circle cx="0" cy="-104" r="8" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/>` +
      LN("M-54,-80 q-14,-10 -10,-26 M54,-80 q14,-10 10,-26 M-62,-50 q-16,-4 -20,-16 M62,-50 q16,-4 20,-16", ink, 4));
    const svg = bg + b1 + b2 + b3 + pac + bell + sens;
    return { svg, alt: "Three senators sit up like trained dogs in front of their grinning YES billboards, hands up like paws, the third, with three YES stickers and the biggest billboard, catching a YES-shaped dog biscuit in his teeth, tongue out; the caped SUPER PAC backpack stands beside a trembling desk bell." };
  },

  "greed-loop-runs"(H, fid) {
    const { K, C } = H;
    // after "existing.": the whole money loop in frame, a ring of medicine money walking round it nose to tail, the
    // stops quiet and unlettered, the germs popped
    const svg = R(-100, -100, 2120, 1280, FIELD) + view(0, -120, 0.39, moneyLoop(K, C, { germsPopped: true }));
    return { svg, alt: "The whole money loop road from afar like the end of Part 2, a ring of green medicine money walking round it nose to tail; beside the road, unlettered, YOU's VICTORY BONDS booth, the campaign office, the treaty, the war tank and the funnel along the top, the glass toll booth on the bend, the Super PAC and its senators, the lab and the hospital along the bottom, the germs on the roofs popped like balloons." };
  },

  "no-opposition"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "finish.": the ring's corner with the three doing the sum, the Lobbyist a grinning skeleton in fedora and mask,
    // the machine with its cuckoo clock at the left, the Reaper out
    const bg = R(-100, -100, 2120, 1280, FIELD) + R(-100, 900, 2120, 300, FIELD_D);
    const mach = R(-100, 100, 560, 800, C.slate, ink, 7) + at(330, 560, 1.05, cuckoo(K, C, true));
    const ring = PL([[560, 620], [1880, 620], [1960, 760], [480, 760]], "#E9E1CC", ink, 5) + R(480, 760, 1480, 150, C.navy, ink, 6) +
      R(720, 780, 1000, 100, C.cream, ink, 4) + T(1220, 856, 76, "OPPOSITION", C.war, { extra: 'letter-spacing="8"' }) +
      [[560, 620], [1880, 620]].map(([x, y]) => R(x - 14, y - 300, 28, 300, C.rust, ink, 4)).join("") +
      [380, 450, 520].map((y) => LN(`M560,${y} L1880,${y}`, C.cream, 7) + LN(`M560,${y} L1880,${y}`, ink, 2)).join("");
    const sit = (name, x, extra) => stand(x, 700, 2.0, K.cast(name, copy({ look: "left", mood: "flat", arms: [[-60, -100], [-30, -60]], build: { legPose: [[86, 8], [92, 12]] } }, extra)));
    const sum = at(1200, 700, 1, `<path d="M-300,0 L300,0 L320,-30 L-280,-30 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="3"/>` + T(0, -8, 20, "27.2 × 0.8 + 2.72 + 2.72 = ...", ink, { font: "Inter" }));
    const three = sit("politician", 1040, { mood: "worried" }) + sit("weaponsMaker", 1450, {}) +
      stand(1250, 700, 2.0, K.cast("lobbyist", { skeleton: true, look: "left", arms: [[-60, -100], [-30, -60]], build: { legPose: [[86, 8], [92, 12]] } }) +
        (() => { const r = K.rig(K.castOpts("lobbyist", { look: "left", build: { legPose: [[86, 8], [92, 12]] } })); return `<path transform="translate(${f(r.head[0] - 2)},${f(r.head[1] - 6)}) scale(-1,1)" d="M-17,-11 L18,-12 L19,-1 L13,1 L9,-3 L4,1 L-4,-2 L-10,1 L-17,-1 Z" fill="${C.ink}" opacity="0.92"/>`; })());
    const signs = [[880, 330], [1250, 290], [1620, 330]].map(([x, y]) => at(x, y, 0.75, K.props.sign({ text: "NOT THE ENEMY", posts: 1 }))).join("");
    const svg = bg + mach + ring + signs + three + sum;
    return { svg, alt: "An empty boxing ring with OPPOSITION on its apron; in it the Politician, the Lobbyist and the Weapons Maker sit doing a long sum under their NOT THE ENEMY signs, the Lobbyist now a grinning skeleton in his fedora still at it, while at the left the Reaper springs out of the cuckoo clock on the machine." };
  },

  "sounds-familiar"(H, fid) {
    const { C } = H;
    // on "familiar,": arms crossed, one eyebrow up at the camera, the mug beside her
    const svg = H.host("skeptical-smile", "arms-crossed", mugOnLectern(C));
    return { svg, alt: "Wishonia at her lectern, arms crossed, raises one eyebrow at the camera; her coffee mug stands on the lectern beside her." };
  },

  "military-industrial-loop"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "corpses.": Part 2's road framed on its press, cranking itself, the two men standing back from it, a war
    // paper and a little headstone on stick legs hopping out of it, a pile of headstones beside it
    const bg = ground(880, 1020);
    const press = at(900, 880, 1.65, mirror(K.props.printingPress({ seal: "war", tray: 0 })));
    const pol = stand(330, 900, 2.5, K.cast("politician", { look: "right", mood: "grin", arms: [[-20, -10], [20, 10]] }));
    const wm = stand(1560, 900, 2.5, K.cast("weaponsMaker", { look: "left" }));
    const pile = [[1200, 880], [1260, 880], [1320, 880], [1230, 820], [1290, 820], [1260, 760]].map(([x, y]) => at(x, y, 0.62, K.props.headstone({ text: "" }))).join("");
    const hop = at(760, 760, 1.05, walkingStone(K, C, 0.6, true)) + at(900, 690, 1.1, K.money("war", 1), -16);
    const spin = LN("M560,520 a60,60 0 0 1 60,-60", ink, 5) + LN("M600,610 a90,90 0 0 1 -30,-120", ink, 5);
    const svg = bg + press + pile + pol + wm + hop + spin;
    return { svg, alt: "Part 2's printing press on its road cranks itself with nobody at its wheel while the Politician and the Weapons Maker stand back from it; out of it hop a green war paper and a little grey headstone on stick legs, onto a pile of headstones beside it." };
  },

  "patient-industrial-loop"(H, fid) {
    const { K, C } = H;
    // after "them).": both loop roads side by side under their two arches, the war press's mountain of headstones, three
    // little headstones by the money loop's lab
    const left = `<g transform="translate(-1750,0)">${warLoop(K, C, { mountain: true, arch: true })}</g>`;
    const right = `<g transform="translate(1950,0) scale(0.82)">${moneyLoop(K, C, { arch: true, stones: true, germsPopped: true })}</g>`;
    const svg = R(-100, -100, 2120, 1280, FIELD) + view(80, -320, 0.27, left + right);
    return { svg, alt: "Two loop roads side by side from far off: on the left Part 2's war loop under its MILITARY INDUSTRIAL COMPLEX arch, a mountain of headstones by its press; on the right the money loop under its PATIENT INDUSTRIAL COMPLEX arch, three little headstones by its lab." };
  },

  "evolved-on-purpose"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "orphans.": YOU beside the lectern with his flower pot, snipping the creeping war vine with shears without
    // looking; Wishonia side-eyeing the camera; the blank blueprint unrolled on the lectern top
    const blue = PL([[560, 792], [960, 792], [968, 900], [552, 900]], "#3D6EA8", ink, 4) + LN("M574,806 H946 V886 H574 Z", "#BFD6EE", 2) +
      `<ellipse cx="960" cy="796" rx="12" ry="20" fill="#2F5A8C" stroke="${ink}" stroke-width="3"/>`;
    const youO = copy(YOU, { look: "left", mood: "smug", arms: [[-40, -100], [60, 30]] });
    const Ry = K.rig(youO), hp = Ry.hand[0], hs = Ry.hand[1];
    let leaves = "";
    [[-14, -50, -30], [14, -58, 30], [0, -72, 0], [-16, -80, -40], [16, -88, 40]].forEach(([x, y, r]) => { leaves += at(x, y, 0.17, K.money("med", 0), r); });
    const pot = at(hp[0] - 4, hp[1] + 4, 1, LN("M0,-20 V-92", "#3B6644", 2.6) + leaves + at(10, -36, 0.14, K.props.bond({ text: "INCENTIVE ALIGNMENT BOND" })) +
      PL([[-24, -20], [24, -20], [18, 14], [-18, 14]], "#C46A45", ink, 1.8) + R(-27, -26, 54, 8, "#B05A38", ink, 1.4));
    const shears = at(hs[0], hs[1], 1, LN("M0,0 L24,-12 M0,0 L25,-3", "#9DA3AE", 3) + `<circle cx="-5" cy="1" r="4" fill="none" stroke="${C.war}" stroke-width="2.2"/><circle cx="-3" cy="7" r="4" fill="none" stroke="${C.war}" stroke-width="2.2"/>`);
    const YX = 1380, YG = 1070, YK = 3.0, sx = YX + YK * hs[0] + 72, sy = YG - 100 * YK + YK * hs[1] - 30;
    const you = stand(YX, YG, YK, K.person(youO) + pot + shears);
    let vine = LN(`M2020,690 C1900,700 1840,640 1760,700 C1690,750 ${f(sx + 60)},${f(sy - 60)} ${f(sx)},${f(sy)}`, "#7A2A1E", 14) +
      LN(`M2020,690 C1900,700 1840,640 1760,700 C1690,750 ${f(sx + 60)},${f(sy - 60)} ${f(sx)},${f(sy)}`, C.war, 8);
    [[1960, 670, -10], [1860, 660, -10], [1780, 690, -10], [1720, 750, -10]].forEach(([x, y, r], i) => { vine += at(x, y - 30, 0.55, K.money("war", i % 2), r); });
    vine += at(1900, 640, 0.6, K.props.missile({ mood: "grumpy", arms: "none" }), -30);
    const snipped = at(sx - 10, sy + 20, 1, LN("M0,0 C-20,30 -10,60 -40,80", C.war, 8) + at(-40, 90, 0.5, K.money("war", 0), 120)) +
      LN(`M${f(sx + 20)},${f(sy - 40)} l14,-16 M${f(sx + 34)},${f(sy - 20)} l20,-6`, ink, 4);
    const svg = H.host("sideeye-closed", "arms-crossed", blue + vine + you + snipped);
    return { svg, alt: "Wishonia side-eyes the camera from her lectern, a blank blueprint unrolled on its top; beside her YOU holds a neat flower pot with a teal plant of medicine bills, staked with the bond, and snips off a war-red vine of missile bills that crept in along the chair rail, without looking at it." };
  },
};
