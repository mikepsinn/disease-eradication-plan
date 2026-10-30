// Sketches for storyboards/part-27-outro.md: each scene's key frame on a 1920 x 1080 frame (16:9), drawn with the
// production art: the host shots on KIT.studio's set, the plate scenes as the camera frames the busy-field plate.
// Built into the review sheet by tools/storyboard-sheet.mjs.
//
// The shared drawings of the part are here, for the scene authors to copy so every scene draws them the same:
//   glowRect(H, w, screen)          the glowing rectangle (70 the tray, 36 the phone, 16 the matchbox) and its screens
//   desk(H, o)                      YOU's desk on the busy-field plate
//   lawn(H, x), deckchair(H), sprinkler(H), lemonade(H)
//                                   the friend's free afternoon on the busy-field plate
//   bonyYOU(H, o, id, cut)          YOU on his bone legs (Part 26's bonyYou, in any leg pose), in person units
//   charredYOU(H, o, id)            charred YOU on his bone legs, his bowler riding on the spikes
//   outTray(H, filed)               the PLANETS out-tray on the lectern's far end, Part 26's case file filed in it
//   armchairBack(H), armchairFront(H)   Part 8's rust wingback
//   poster(H, trials)               Grandma's poster
// The mug is Part 26's (part-26's sketch module), where Part 26 leaves it on the lectern.

import { mug } from "./part-26-humanity-has-no-choice.sketch.mjs";

const f = (n) => n.toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});

// A plate framing as KIT.camera places it: plate point (x, y) in the middle of the frame, at scale s.
const view = (x, y, s, inner) => `<g transform="translate(${f(960 - x * s)},${f(540 - y * s)}) scale(${s})">${inner}</g>`;
// A host shot's slow push in on her face (KIT.studio), k of the way along.
const push = (S, k, inner) => `<g transform="translate(${S.face[0]},${S.face[1]}) scale(${k}) translate(${-S.face[0]},${-S.face[1]})">${inner}</g>`;
const at = (x, y, k, inner, rot) => `<g transform="translate(${f(x)},${f(y)})${rot ? ` rotate(${rot})` : ""}${k !== 1 ? ` scale(${k})` : ""}">${inner}</g>`;
const mirror = (inner) => `<g transform="scale(-1,1)">${inner}</g>`;

// ── The cast ──
const YOU = { tone: 2, outfit: "suit", hat: "bowler" };
const FRIEND = { tone: 3, outfit: "dress", hair: 1, color: 2 };
const CLERK = { tone: 0, outfit: "shirt", color: 1 };
const KP = 1.5; // everyone on the plate is drawn at this scale, feet on y 0
const SEAT = { legPose: [[88, -3], [93, 2]] }; // Part 8's seated legs
const BONE = "#F1EAD6";

// ── The plate (busy-field), in plate units ──
const HZ = -520, SKY = "#EFE3C4", GROUND = "#C8B07B", HLINE = "#8E7A55", OLIVE = "#7E8C3A", GLOW = "#CFF1EC", WATER = "#BFE0E6";

function field() {
  return `<rect x="-6000" y="${HZ - 6000}" width="12000" height="6000" fill="${SKY}"/>` +
    `<rect x="-6000" y="${HZ}" width="12000" height="6000" fill="${GROUND}"/>` +
    `<path d="M-6000,${HZ} H6000" stroke="${HLINE}" stroke-width="3" opacity="0.6"/>`;
}

// A five-point star around (0, 0), outer radius r.
function starPath(r, inner = 0.45) {
  let d = "";
  for (let i = 0; i < 10; i++) {
    const a = -Math.PI / 2 + (i * Math.PI) / 5, rr = i % 2 ? r * inner : r;
    d += `${i ? "L" : "M"}${f(rr * Math.cos(a))},${f(rr * Math.sin(a))} `;
  }
  return d + "Z";
}

// The glowing rectangle (shared drawing): a slate slab with two TV knobs and a pale cyan screen, w wide (person
// units: 70 the tray, 36 the phone, 16 the matchbox), centered on (0, 0). screen: "share" | "stars" | "address" | "".
function glowRect(H, w, screen) {
  const { C } = H, ink = C.line;
  let s = "";
  if (screen === "share") {
    s = `<rect x="-26" y="-11" width="52" height="22" rx="6" fill="${C.cream}" stroke="${ink}" stroke-width="2"/>` +
      `<path d="M-19,4 V-3 Q-19,-6 -15,-6 H-10 M-13,-9 L-9,-6 L-13,-3" fill="none" stroke="${ink}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>` +
      `<text x="5" y="4.5" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="12" letter-spacing="0.5" fill="${ink}">SHARE</text>`;
  } else if (screen === "stars") {
    s = [-28, -14, 0, 14, 28].map((x) => `<path transform="translate(${x},0)" d="${starPath(6)}" fill="none" stroke="${ink}" stroke-width="1.6" stroke-linejoin="round"/>`).join("");
  } else if (screen === "address") {
    s = `<rect x="-38" y="-8" width="76" height="16" rx="3" fill="#FFFFFF" stroke="${ink}" stroke-width="1.4"/>` +
      `<text x="0" y="4" text-anchor="middle" font-family="Inter" font-weight="700" font-size="9.4" fill="${ink}">warondisease.org</text>`;
  }
  const body = `<ellipse cx="0" cy="-3" rx="80" ry="62" fill="${GLOW}" opacity="0.32"/>` +
    `<rect x="-50" y="-35" width="100" height="70" rx="11" fill="${C.slate}" stroke="${ink}" stroke-width="3"/>` +
    `<rect x="-42" y="-28" width="84" height="44" rx="6" fill="${GLOW}" stroke="${ink}" stroke-width="2"/>` +
    `<path d="M-38,-24 l10,0" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>` +
    `<circle cx="-30" cy="25" r="4.2" fill="${C.orange}" stroke="${ink}" stroke-width="1.6"/><circle cx="-17" cy="25" r="4.2" fill="${C.cream}" stroke="${ink}" stroke-width="1.6"/>` +
    `<path d="M10,22 H40 M10,26 H40" stroke="${C.cream}" stroke-width="1.6" opacity="0.7"/>` +
    `<g transform="translate(0,-6)">${s}</g>`;
  return `<g transform="scale(${(w / 100).toFixed(3)})">${body}</g>`;
}

// YOU's desk: a slate 1950s office desk alone in the field, its feet on y 0, about 300 x 120 (plate units),
// a tear-off calendar and an in-tray of paper on top.
function desk(H, o = {}) {
  const { K, C } = H, ink = C.line;
  const top = `<path d="M-160,-128 H160 V-110 H-160 Z" fill="${C.slate}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/><path d="M-154,-123 H154" stroke="${C.orange}" stroke-width="3"/>`;
  const ped = `<path d="M-148,-110 H-40 V0 H-148 Z" fill="${C.slate}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>` +
    [-90, -58, -26].map((y) => `<path d="M-140,${y - 22} H-48 V${y + 6} H-140 Z" fill="${C.navy}" stroke="${ink}" stroke-width="3"/><rect x="-104" y="${y - 12}" width="20" height="6" rx="2" fill="${C.cream}" stroke="${ink}" stroke-width="2"/>`).join("");
  const panel = `<path d="M-40,-110 H148 V-38 H-40 Z" fill="${C.navy}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>` +
    `<path d="M136,-38 L140,0 M136,-38 L130,0" stroke="${ink}" stroke-width="7" stroke-linecap="round"/>`;
  const tray = `<path d="M-130,-128 L-126,-150 H-50 L-46,-128 Z" fill="${C.tan}" stroke="${ink}" stroke-width="3.5" stroke-linejoin="round"/>` +
    [0, 1, 2, 3].map((i) => `<path d="M${-124 + i * 2},${-150 - i * 6} H${-52 + i * 2} V${-145 - i * 6} H${-124 + i * 2} Z" fill="#FBF6E6" stroke="${ink}" stroke-width="2"/>`).join("");
  const cal = at(80, -128, 1.25, K.props.calendar({ month: "MON", day: o.day || 1, pages: 3 }));
  return top + ped + panel + tray + (o.noCal ? "" : cal);
}

// The friend's lawn: a round patch of green on the tan ground around (x, 0), with a few tufts.
function lawn(H, x) {
  const ink = H.C.line;
  const tufts = [[-330, 24], [-200, -30], [-60, 44], [120, -34], [260, 30], [360, -8]].map(([dx, dy]) => `<path d="M${x + dx - 8},${dy + 4} l4,-10 l4,8 l4,-12 l4,14" fill="none" stroke="#5F6C2A" stroke-width="3" stroke-linejoin="round"/>`).join("");
  return `<ellipse cx="${x}" cy="6" rx="470" ry="74" fill="${OLIVE}" stroke="${ink}" stroke-width="3" opacity="0.95"/>` + tufts;
}

// A striped canvas deckchair seen from the side, its feet on y 0, facing right (the sitter reclines to the left),
// about 200 wide and 190 tall in plate units: an X of two wooden frames and the canvas sling between the top bar
// (-76, -184) and the front bar (76, -92).
function deckchair(H) {
  const { C } = H, ink = C.line;
  const wood = (d, w = 10) => `<path d="${d}" stroke="${ink}" stroke-width="${w + 5}" stroke-linecap="round" fill="none"/><path d="${d}" stroke="${C.tan}" stroke-width="${w}" stroke-linecap="round" fill="none"/>`;
  const sling = "M-72,-178 Q-18,4 72,-90";
  return wood("M-96,0 L76,-92") +
    `<path d="${sling}" stroke="${ink}" stroke-width="40" fill="none"/><path d="${sling}" stroke="${C.cream}" stroke-width="32" fill="none"/>` +
    `<path d="${sling}" stroke="${C.rust}" stroke-width="32" fill="none" stroke-dasharray="15 15"/>` +
    wood("M96,0 L-76,-184") + `<circle cx="32" cy="-68" r="5" fill="${C.slate}" stroke="${ink}" stroke-width="2"/>`;
}

// An oscillating lawn sprinkler on (0, 0): a slate base with its spray tube, a green hose trailing off to the left,
// and its fan of water arcing over to the right (drops along five arcs).
function sprinkler(H) {
  const { C } = H, ink = C.line;
  const hose = `<path d="M-26,-4 C-80,10 -120,-14 -180,4 S-280,20 -360,2" fill="none" stroke="${ink}" stroke-width="12" stroke-linecap="round"/><path d="M-26,-4 C-80,10 -120,-14 -180,4 S-280,20 -360,2" fill="none" stroke="#5F7A3A" stroke-width="6" stroke-linecap="round"/>`;
  const base = `<path d="M-30,0 L-26,-14 H26 L30,0 Z" fill="${C.slate}" stroke="${ink}" stroke-width="3.5" stroke-linejoin="round"/>` +
    `<path d="M-22,-14 Q0,-50 22,-14" fill="none" stroke="${ink}" stroke-width="9"/><path d="M-22,-14 Q0,-50 22,-14" fill="none" stroke="${C.yellow}" stroke-width="4"/>`;
  let drops = "";
  [[170, 110], [220, 140], [270, 165], [320, 175], [370, 165]].forEach(([dx, h], k) => {
    for (let i = 1; i < 10; i++) {
      const t = i / 10, x = dx * t, y = -34 - 4 * h * t * (1 - t) + 34 * t;
      drops += `<circle cx="${f(x)}" cy="${f(y)}" r="${(5.2 - k * 0.4).toFixed(1)}" fill="${WATER}" stroke="${ink}" stroke-width="1.4"/>`;
    }
  });
  return hose + drops + base;
}

// A tall glass of lemonade with a bendy straw and a lemon slice on the rim, its foot at (0, 0), about 24 x 66.
function lemonade(H) {
  const { C } = H, ink = C.line;
  return `<path d="M-10,0 L-12,-44 H12 L10,0 Z" fill="#FFFFFF" stroke="${ink}" stroke-width="2.4" stroke-linejoin="round"/>` +
    `<path d="M-10.5,-4 L-11.4,-34 H11.4 L10.5,-4 Z" fill="#F2D97A"/>` +
    `<path d="M3,-30 L8,-58 L18,-64" fill="none" stroke="${ink}" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M3,-30 L8,-58 L18,-64" fill="none" stroke="${C.war}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>` +
    `<circle cx="-11" cy="-44" r="8" fill="${C.yellow}" stroke="${ink}" stroke-width="2"/><path d="M-11,-44 l-5,-4 M-11,-44 l5,-4 M-11,-44 v6" stroke="#FFFFFF" stroke-width="1.4"/>`;
}

// A fat mustard star on stick legs, around (0, 0), its feet `leg` below its center; up: arms raised.
function starGuy(H, r, leg, mood = "smile", spring = false) {
  const { C } = H, ink = C.line;
  const legs = spring
    ? `<path d="M-10,${r * 0.6} l-8,${leg * 0.2} l12,${leg * 0.2} l-12,${leg * 0.2} l12,${leg * 0.2} l-8,${leg * 0.2 - r * 0.6}" fill="none" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
      `<path d="M10,${r * 0.6} l8,${leg * 0.2} l-12,${leg * 0.2} l12,${leg * 0.2} l-12,${leg * 0.2} l8,${leg * 0.2 - r * 0.6}" fill="none" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>`
    : `<path d="M-10,${r * 0.6} L-14,${leg} h-9 M10,${r * 0.6} L14,${leg} h9" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>`;
  const mouth = mood === "smile" ? `<path d="M-8,5 Q0,13 8,5" fill="none" stroke="${ink}" stroke-width="3" stroke-linecap="round"/>` : `<ellipse cx="0" cy="7" rx="6" ry="7" fill="${ink}"/>`;
  return legs + `<path d="${starPath(r, 0.5)}" fill="${C.yellow}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
    `<circle cx="-7" cy="-4" r="3.6" fill="${ink}"/><circle cx="7" cy="-4" r="3.6" fill="${ink}"/>` + mouth;
}

// The pro-war robot: KIT.props.robot in war red, an army helmet on its box head, a missile painted on its chest.
function proWarRobot(H, o = {}) {
  const { K, C } = H, ink = C.line;
  const helmet = `<path d="M-40,-176 Q-40,-214 0,-216 Q40,-214 40,-176 Z" fill="#6B6A3E" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
    `<path d="M-48,-176 H48 V-169 H-48 Z" fill="#5A5934" stroke="${ink}" stroke-width="3.5"/>`;
  const insignia = `<g transform="translate(0,-104) rotate(-35)"><path d="M-13,-4 H8 L15,0 L8,4 H-13 Z M-13,-4 L-18,-9 M-13,4 L-18,9" fill="${C.cream}" stroke="${C.cream}" stroke-width="2.4" stroke-linejoin="round"/></g>`;
  let m = K.props.robot({ color: "war", mood: o.mood || "smug", arms: o.arms });
  m = m.replace(/<\/g>\s*$/, helmet + "</g>");
  return m + (o.noInsignia ? "" : insignia);
}

// A pile of n bills (KIT.money) heaped into a mound w wide, its foot on y 0.
function pile(H, kind, n, w, seed) {
  const { K } = H;
  const r = K.rng(seed);
  let out = "";
  for (let i = 0; i < n; i++) {
    const row = Math.floor(Math.sqrt(i * 1.6)), u = r() * 2 - 1, x = u * (w / 2) * (1 - row * 0.18), y = -18 - row * 26 - r() * 8;
    out += at(x, y, 0.8, K.money(kind, 0).replace('class="legs"', 'class="legs" opacity="0"'), (r() - 0.5) * 40);
  }
  return out;
}

// The slider: a long cream track on short slate feet from x0 to x1 (its feet on y 30), the knob at knobX.
function slider(H, x0, x1, knobX) {
  const { C } = H, ink = C.line;
  const feet = [x0 + 40, x1 - 40].map((x) => `<path d="M${x - 16},30 L${x - 8},-34 H${x + 8} L${x + 16},30 Z" fill="${C.slate}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>`).join("");
  const track = `<rect x="${x0}" y="-64" width="${x1 - x0}" height="32" rx="16" fill="${C.cream}" stroke="${ink}" stroke-width="5"/>` +
    `<rect x="${x0 + 22}" y="-52" width="${x1 - x0 - 44}" height="8" rx="4" fill="${C.slate}"/>`;
  const knob = `<g transform="translate(${knobX},0)"><path d="M-30,-48 L-26,-132 Q-26,-140 -18,-140 H18 Q26,-140 26,-132 L30,-48 Z" fill="${C.navy}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>` +
    `<path d="M-14,-120 H14 M-14,-106 H14 M-14,-92 H14" stroke="${C.cream}" stroke-width="4" stroke-linecap="round"/><path d="M22,-132 L25,-56" stroke="${C.orange}" stroke-width="3"/></g>`;
  return feet + track + knob;
}

// A human only `done` of the way drawn (0..1 from the feet up): inked below, a dashed pencil outline above.
function partialPerson(H, fid, o, done) {
  const { K } = H;
  const cut = 100 - 190 * done;
  const m = K.person(o);
  const ghost = m.replace(/fill="(?!none)[^"]*"/g, 'fill="none"').replace(/fill="url\([^)]*\)"/g, 'fill="none"');
  return `<defs><clipPath id="${fid}-inked"><rect x="-200" y="${cut}" width="400" height="300"/></clipPath><clipPath id="${fid}-sketch"><rect x="-200" y="-300" width="400" height="${300 + cut}"/></clipPath></defs>` +
    `<g clip-path="url(#${fid}-inked)">${m}</g><g clip-path="url(#${fid}-sketch)" style="stroke-dasharray:4 3.5" opacity="0.75">${ghost}</g>`;
}

// The PLANETS out-tray on the lectern's far end (16:9 canvas px), the case file on top when filed: Part 26's file,
// "EARTH" struck out for DIRT, its final stamp showing on the folder's edge.
function outTray(H, filed) {
  const { C } = H, ink = C.line;
  const x = 548, y = 792;
  const file = (dy, label, col, size = 8.5) => `<path d="M${x + 10},${y - 34 - dy} H${x + 136} V${y - 6 - dy} H${x + 10} Z" fill="${col}" stroke="${ink}" stroke-width="2.4"/>` +
    `<path d="M${x + 14},${y - 34 - dy} V${y - 44 - dy} H${x + 100} V${y - 34 - dy}" fill="${col}" stroke="${ink}" stroke-width="2.4"/>` +
    `<text x="${x + 57}" y="${y - 37 - dy}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="${size}" fill="${ink}">${label}</text>`;
  const wire = `<path d="M${x},${y - 40} L${x + 6},${y} H${x + 140} L${x + 146},${y - 40}" fill="none" stroke="${C.slate}" stroke-width="4" stroke-linejoin="round"/>` +
    [24, 48, 72, 96, 120].map((dx) => `<path d="M${x + dx + 3},${y - 38} V${y - 2}" stroke="${C.slate}" stroke-width="2"/>`).join("") +
    `<path d="M${x + 2},${y - 20} H${x + 144}" stroke="${C.slate}" stroke-width="2"/>`;
  const label = `<rect x="${x + 42}" y="${y - 16}" width="62" height="14" fill="${C.cream}" stroke="${ink}" stroke-width="1.8"/><text x="${x + 73}" y="${y - 5}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="10" letter-spacing="0.6" fill="${ink}">PLANETS</text>`;
  const earth = `<tspan text-decoration="line-through">EARTH</tspan> DIRT: CASE #847`;
  const inner = file(0, "VENUS: TOO HOT", "#E9C98F") + file(8, "MARS: NOBODY HOME", "#E3B97A") +
    (filed ? file(16, earth, "#E7C98C", 7.8) + `<text x="${x + 73}" y="${y - 18 - 16}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="7.5" fill="${C.war}" transform="rotate(-4 ${x + 73} ${y - 20 - 16})">ELIGIBLE FOR OPTIMIZATION</text>` : "") +
    wire + label;
  // drawn 1.3 times size, its foot on the lectern's reading top (y 790) at its far end
  return `<g transform="translate(532,792) scale(1.3) translate(${-x},${-y})">${inner}</g>`;
}
// The mug where Part 26 leaves it, on the lectern's near end (16:9).
function lecternMug(H) {
  const S = H.K.STUDIO;
  return at(S.lect[0] + S.lect[1] / 2 - 50, S.top + 4, 1, mug(H));
}

// Part 8's rust wingback armchair (dissolving-on-schedule.html, chairBack and chairFront), in person units around a
// seated person facing +x: the back and the wing behind him, the cushion under him, the arm and skirt in front.
const polyD = (pts) => "M" + pts.map((p) => `${p[0]},${p[1]}`).join(" L") + " Z";
const solidP = (H, pts, col, w = 3) => `<path d="${polyD(pts)}" fill="${col}" stroke="${H.C.line}" stroke-width="${w}" stroke-linejoin="miter"/>`;
function armchairBack(H) {
  const { C } = H;
  return solidP(H, [[-46, -40], [-30, -44], [-20, -34], [-17, 76], [-42, 79]], C.rust) + `<path d="M-29,-40 L-21,-35 M-43,-36 L-40,74" stroke="${C.orange}" stroke-width="1.4"/>` +
    solidP(H, [[-24, -33], [-9, -27], [-7, 8], [-20, 16]], C.rust, 3.4) + solidP(H, [[-24, 71.5], [33, 71.5], [36, 76], [35, 84], [-24, 84]], C.rust) +
    `<path d="M-22,72.5 L33,72.5" stroke="${C.orange}" stroke-width="1.4"/>`;
}
function armchairFront(H) {
  const { C } = H, ink = C.line;
  return solidP(H, [[-38, 73], [20, 73], [20, 92], [-40, 92]], C.rust) + solidP(H, [[17, 70], [26, 70], [31, 73.5], [31, 82], [27, 86], [17, 86]], C.rust) +
    solidP(H, [[-41, 91], [32, 91], [33, 96], [-42, 96]], C.rust) + `<path d="M-36,74 L18,74" stroke="${C.orange}" stroke-width="1.4"/>` +
    solidP(H, [[-37, 96], [-31, 96], [-32, 102], [-36, 102]], ink, 1) + solidP(H, [[24, 96], [30, 96], [29, 102], [25, 102]], ink, 1);
}
// The bowler (kit.js hatSvg), its brim's middle at (0, 0), in person units.
function bowler(H) {
  const ink = H.C.line;
  return `<path d="M-17,1 L-13,-16 L0,-21 L13,-16 L17,1 Z" fill="${ink}"/><path d="M-28,4 L-22,-1 H22 L28,4 Z" fill="${ink}"/>`;
}
// YOU on his bone legs (Part 26's bonyYou: from countdown-104 on he is bone from the waist down), in person units, in
// any leg pose: the person clipped above the hips over the skeleton's legs, with knobbly knees. o: more person options
// (charred: true chars the top half; the bones stay bone white). id: a clip id unique in the frame. cut: how far above
// the hips the clothes end (4 standing; 7 seated, so no trouser shows along the thighs).
function bonyYOU(H, o, id, cut = 4) {
  const { K, C } = H, po = copy(YOU, o), R = K.rig(po), b = R.build, y = R.hipY - cut;
  const L = 37 * b.legs, lp = b.legPose || [[-6, -2], [6, 2]];
  const knees = R.hip.map(([x], i) => {
    const a = (lp[i][0] * Math.PI) / 180;
    return `<ellipse cx="${f(x + L * Math.sin(a))}" cy="${f(R.hipY + L * Math.cos(a))}" rx="4.2" ry="3.4" fill="${BONE}" stroke="${C.line}" stroke-width="1.6"/>`;
  }).join("");
  return `<defs><clipPath id="${id}-up"><rect x="-200" y="-200" width="400" height="${f(200 + y)}"/></clipPath><clipPath id="${id}-dn"><rect x="-200" y="${f(y)}" width="400" height="200"/></clipPath></defs>` +
    `<g clip-path="url(#${id}-dn)">${K.person(copy(po, { skeleton: true, charred: false }))}</g>${knees}<g clip-path="url(#${id}-up)">${K.person(po)}</g>`;
}
// Charred YOU: the charred gag blows his hair straight up, so his bowler rides on top of the spikes; with an id, on
// his bone legs (without one, for a head-and-shoulders shot such as the mugshot).
function charredYOU(H, extra, id) {
  const o = copy({ charred: true }, extra);
  return (id ? bonyYOU(H, o, id) : H.K.person(copy(YOU, o))) + at(5, -107, 0.95, bowler(H), -7);
}
// Grandma's poster as the kit draws it (her "poster" prop), around her hand; trials: its back, TRIALS and a cross.
function poster(H, trials) {
  const { C } = H, ink = C.line;
  const card = `<path d="M-20,-26 H20 V26 H-20 Z" fill="${C.paper}" stroke="${ink}" stroke-width="2.6"/>`;
  return `<g transform="translate(-14,-20)">${card}` + (trials
    ? `<path d="M0,-18 V-2 M-8,-10 H8" stroke="${C.med}" stroke-width="4.5" stroke-linecap="round"/><text x="0" y="14" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="10.5" fill="${ink}">TRIALS</text>`
    : `<text x="0" y="-4" text-anchor="middle" font-family="Oswald" font-size="11" fill="${C.war}">BUY</text><text x="0" y="10" text-anchor="middle" font-family="Oswald" font-size="11" fill="${ink}">BONDS</text>`) + "</g>";
}
// A review card on the booth's counter (canvas px), 150 wide, centered on (0, 0): n mustard stars in a row (more than
// five run off both ends), and the CHECKED mark when stamped.
function reviewCard(H, n, checked) {
  const { K, C } = H, ink = C.line, gap = 27, x0 = -((n - 1) * gap) / 2;
  const stars = Array.from({ length: n }, (_, i) => `<path transform="translate(${f(x0 + i * gap)},-11)" d="${starPath(11, 0.48)}" fill="${C.yellow}" stroke="${ink}" stroke-width="2.2" stroke-linejoin="round"/>`).join("");
  return `<path d="M-75,-30 H75 V30 H-75 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="3"/>` + stars +
    (checked ? at(2, 26, 0.5, K.props.stampMark({ text: "CHECKED", angle: -6 })) : "");
}

export default {
  "thank-you"(H, fid) {
    const { K, C } = H, S = K.STUDIO, ink = C.line;
    // after "time": she presents YOU, asleep on his bone legs in the armchair that rolled in under him where he stood
    // in Part 26 (facing her, so mirrored), the open manual tented over his face and lifted on a snore; the case file
    // filed in the PLANETS tray, the stamp put down by the mug, and the gift's pedestal empty (the Earth rolled away)
    const px = 1330, ptop = 760; // Part 26's pedestal
    const pedestal = `<path d="M${px - 110},1090 L${px - 90},${ptop + 40} H${px + 90} L${px + 110},1090 Z" fill="${C.cream}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      `<path d="M${px - 60},${ptop + 60} V1080 M${px},${ptop + 60} V1080 M${px + 60},${ptop + 60} V1080" stroke="#D9CBA4" stroke-width="6"/>` +
      `<path d="M${px - 128},${ptop + 40} H${px + 128} L${px + 116},${ptop} H${px - 116} Z" fill="${C.rust}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>`;
    const stamp = at(858, S.top + 4, 0.6, K.props.stamp({ text: "ELIGIBLE" }));
    const k = 3.0, x = 1620, y = 1072 - 102 * k;
    const sleeper = copy(YOU, { build: { legPose: SEAT.legPose }, mood: "flat", arms: [[20, 50], [30, 62]] });
    const R = K.rig(sleeper);
    // the manual, open face down over his face like a tent, lifted a little off it on the snore
    // (and a snore bubble swelling out of his nose under it)
    const book = at(R.eyes[0] + 6, R.eyes[1] - 4, 1.35, `<path d="M0,-10 L-17,5 L-15,9 L0,-4 L15,9 L17,5 Z" fill="${C.orange}" stroke="${ink}" stroke-width="1.8" stroke-linejoin="round"/>` +
      `<path d="M-12,5 L0,-5.5 L12,5" fill="none" stroke="#FFFFFF" stroke-width="1.6"/><path d="M-9,1.5 L-3,-3.5 M3,-3.5 L9,1.5" stroke="${C.cream}" stroke-width="2.4"/>` +
      `<path d="M-14,-12 q2,-3 5,-2 M14,-12 q-2,-3 -5,-2" fill="none" stroke="${ink}" stroke-width="1.1" stroke-linecap="round"/>`, -4) +
      `<circle cx="${R.eyes[0] + 22}" cy="${R.eyes[1] + 16}" r="7" fill="#DDF1F3" fill-opacity="0.75" stroke="${ink}" stroke-width="1.2"/><path d="M${R.eyes[0] + 18},${R.eyes[1] + 13} q2,-2 4,-2" fill="none" stroke="#FFFFFF" stroke-width="1.2"/>`;
    const guest = at(x, y, k, mirror(armchairBack(H) + bonyYOU(H, sleeper, `${fid}-you`, 7) + book + armchairFront(H)));
    const svg = push(S, 1.035, H.host("happy-smile", "presenting", outTray(H, true) + lecternMug(H) + stamp + pedestal + guest));
    return { svg, alt: "Wishonia beams at her lectern and presents, with both hands, the busy human in the bowler asleep on his bone legs in a rust wingback armchair beside her, an open orange manual tented over his face and lifted on a snore; the Earth case file, EARTH struck out for DIRT, lies on top of VENUS and MARS in the PLANETS out-tray at the lectern's end, the stamp stands by the mug, and the gift's pedestal beside him is empty." };
  },

  "glowing-rectangle-share"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "war": the friend springs up out of her deckchair on the lawn and karate-chops the missile in half, her
    // lemonade level in her other hand; the halves drop into the sprinkler's spray; the blob creeps up behind the chair
    const DX = 1420;
    const chair = at(DX, 0, 1, deckchair(H)) + at(DX - 8, -74, 1, glowRect(H, 54, ""), 24);
    const spray = at(1110, 0, 1, sprinkler(H));
    const sign = at(1800, 0, 1.15, K.props.sign({ text: "FREE\nAFTERNOON", posts: 1, fontSize: 30, height: 46 }));
    // she springs up out of the deckchair, the chopping hand out front, her lemonade held level in the other
    const ko = copy(FRIEND, { mood: "cross", look: "right", arms: [[-80, -160], [100, 62]], build: { legPose: [[-35, -5], [30, 60]] } });
    const R = K.rig(ko), fk = KP * 1.12, fx = 1380, fy = -440;
    const friend = at(fx, fy, fk, K.person(ko) + at(R.hand[0][0] - 2, R.hand[0][1] + 4, 1, lemonade(H)));
    const hand = [fx + R.hand[1][0] * fk, fy + R.hand[1][1] * fk];
    // the missile, flying left nose first, cut in two just under her hand: each half pivots on the cut (missile y -80)
    const mis = K.props.missile({ mood: "scared", arms: "none" });
    const half = (clip, rot, dx, dy) => at(hand[0] + dx, hand[1] + dy + 30, 1.3, `<defs><clipPath id="${fid}-${clip}"><rect x="-90" y="${clip === "nose" ? -220 : -80}" width="180" height="140"/></clipPath></defs>` +
      `<g transform="translate(0,80)"><g clip-path="url(#${fid}-${clip})">${mis}</g></g>`, rot);
    const nose = half("nose", -128, -34, 22), tail = half("tail", -50, 38, 14);
    const chop = `<path d="M${hand[0] - 22},${hand[1] - 18} l-8,-30 M${hand[0] + 4},${hand[1] - 26} l4,-34 M${hand[0] + 30},${hand[1] - 16} l22,-24" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`;
    const blob = at(1610, 0, 0.95, K.props.diseaseBlob({ mood: "smug", seed: 4 }));
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="${GROUND}"/>` +
      view(1420, -300, 1.2, field() + lawn(H, 1420) + blob + chair + spray + sign + friend + nose + tail + chop);
    return { svg, alt: "On a round patch of lawn in a field, a woman springs up out of her striped deckchair beside a FREE AFTERNOON garden sign and karate-chops a grumpy missile in half while holding her lemonade level in the other hand; the two halves drop, surprised, into the spray of a lawn sprinkler, her little glowing rectangle lies on the deckchair, and a disease blob creeps up behind it." };
  },

  "really-good-review"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "suppression": the six stars stand up under the robot together and carry it off on their little legs like
    // a rug, scurrying right; YOU runs on the spot behind them on his bone legs, his phone-sized rectangle held out
    const runner = copy(YOU, { mood: "worried", look: "right", arms: [[95, 140], [70, 95]], build: { legPose: [[-60, -100], [55, 10]] } });
    const R = K.rig(runner);
    // the Road Runner wheel where his legs are
    const blur = `<g opacity="0.8">${[0, 1, 2].map((i) => `<ellipse cx="${2 + i * 3}" cy="${R.hipY + 44}" rx="${48 - i * 9}" ry="${36 - i * 7}" fill="none" stroke="${ink}" stroke-width="2.8" stroke-dasharray="${22 - i * 4} 9" transform="rotate(${i * 40} 0 ${R.hipY + 44})"/>`).join("")}</g>`;
    const dust = [[-46, 98, 12], [-62, 92, 9], [-74, 100, 7]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#E6D8B2" stroke="${ink}" stroke-width="1.5" opacity="0.9"/>`).join("");
    const sweat = `<path d="M-28,-92 q-6,10 0,14 q6,-4 0,-14 Z M30,-104 q-6,10 0,14 q6,-4 0,-14 Z" fill="#FFFFFF" stroke="${ink}" stroke-width="1.6"/>`;
    const phone = at(R.hand[1][0] + 12, R.hand[1][1] - 8, 1, glowRect(H, 36, "stars"));
    const you = at(-730, -100 * KP, KP, dust + bonyYOU(H, runner, `${fid}-you`) + blur + sweat + phone);
    const deskM = at(-980, 0, 1, desk(H, { day: 9 }));
    const pages = [[-640, -14, 20], [-590, -6, -15], [-690, -4, 8], [-540, -6, 30], [-860, -6, -22]].map(([x, y, r]) => at(x, y, 1, `<path d="M-26,-10 H26 V10 H-26 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="2.4"/><path d="M-26,-10 H26 V-2 H-26 Z" fill="${C.war}"/>`, r)).join("");
    // the six stars in a row under the robot, which lies on its back across their tops like a rolled rug, head first
    // to the right, arms flailing; the stars scurry right on their stick legs, a little bob each, speed lines behind
    const sx0 = -430, sg = 82;
    const stars = [0, 1, 2, 3, 4, 5].map((i) => at(sx0 + i * sg, -100 - (i % 2) * 8, 1, starGuy(H, 40, 100 + (i % 2) * 8, "o"))).join("");
    const rk = 1.55, rx = sx0 + 2.5 * sg - 102 * rk, ry = -190;
    const robot = at(rx, ry, rk, proWarRobot(H, { mood: "scared", arms: [[150, 175], [-150, -175]] }), 90);
    const whoosh = [0, 1, 2].map((i) => `<path d="M${sx0 - 70 - i * 18},${-150 + i * 40} h${-110 + i * 20}" stroke="${ink}" stroke-width="5" stroke-linecap="round" opacity="0.6"/>`).join("") +
      [0, 2, 4].map((i) => `<circle cx="${sx0 + i * sg - 34}" cy="-6" r="9" fill="#E6D8B2" stroke="${ink}" stroke-width="1.5"/><circle cx="${sx0 + i * sg - 50}" cy="-2" r="6" fill="#E6D8B2" stroke="${ink}" stroke-width="1.5"/>`).join("");
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="${GROUND}"/>` +
      view(-480, -300, 0.98, field() + deskM + pages + you + whoosh + stars + robot);
    return { svg, alt: "In a field by his desk, the busy human in the bowler runs on the spot on his bone legs, holding out a little glowing rectangle; in front of him six mustard stars on stick legs carry off a red tin robot in an army helmet, a missile on its chest, lying on its back across their tops like a rolled rug, scurrying right with speed lines behind them." };
  },

  "they-dont-check"(H, fid) {
    const { K, C } = H, S = K.STUDIO, ink = C.line;
    // on "check.": she side-eyes the camera; beside the lectern the booth is open, its clerk turned away on the phone,
    // laughing, his arm reaching back out over the counter, his stamp just lifted off a card whose stars run off both
    // ends: CHECKED, beside two more CHECKED cards
    const bx = 1460, by = 1066; // the booth's foot
    const top = by - 636, win = [bx - 165, by - 540, 330, 262], ledge = win[1] + win[3]; // the window; its sill at y 804
    const body = `<path d="M${bx - 215},${by} V${top} H${bx + 215} V${by} Z" fill="${C.cream}" stroke="${ink}" stroke-width="6" stroke-linejoin="round"/>` +
      `<path d="M${bx - 255},${top} L${bx - 205},${top - 90} H${bx + 205} L${bx + 255},${top} Z" fill="${C.rust}" stroke="${ink}" stroke-width="6" stroke-linejoin="round"/>` +
      `<rect x="${bx - 175}" y="${top + 16}" width="350" height="62" fill="${C.navy}" stroke="${ink}" stroke-width="4"/>` +
      H.label(bx, top + 61, 40, "REVIEW CHECKING", "middle", C.cream) +
      `<rect x="${win[0]}" y="${win[1]}" width="${win[2]}" height="${win[3]}" fill="#C9BB97" stroke="${ink}" stroke-width="5"/>` +
      // the shutter, rolled up into its box over the window
      `<rect x="${win[0] - 6}" y="${win[1] - 8}" width="${win[2] + 12}" height="22" rx="6" fill="#B9AE96" stroke="${ink}" stroke-width="4"/>`;
    // the counter: its top seen a little from above, and its front edge
    const counter = `<path d="M${bx - 172},${ledge} H${bx + 172} L${bx + 200},${ledge + 50} H${bx - 200} Z" fill="${C.tan}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
      `<rect x="${bx - 200}" y="${ledge + 50}" width="400" height="22" fill="#9C6A43" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M${bx - 150},${ledge + 72} V${by}" stroke="${ink}" stroke-width="3" opacity="0.35"/>`;
    // the clerk, sitting sideways in the window, face to the phone at his ear; his back arm reaches out to the stamp
    const ck = 2.0, stampK = 0.85, sx = bx - 82, rubber = ledge + 2; // the stamp's rubber just lifted off the card
    const co = copy(CLERK, { look: "right", mood: "grin", arms: [[-58, -18], [122, -104]] }), CR = K.rig(co);
    const grip = rubber - stampK * 90; // where his hand holds the knob
    const cx = sx - ck * CR.hand[0][0], cy = grip - ck * CR.hand[0][1];
    // the handset at his ear, its cord coiling down out of the window
    const ear = [CR.head[0] - 6, CR.head[1] + 3], mo = [CR.mouth[0] + 2, CR.mouth[1] + 7];
    const handset = `<path d="M${f(ear[0])},${f(ear[1])} L${f(mo[0])},${f(mo[1])}" stroke="${ink}" stroke-width="7.5" stroke-linecap="round"/><path d="M${f(ear[0])},${f(ear[1])} L${f(mo[0])},${f(mo[1])}" stroke="${C.slate}" stroke-width="4" stroke-linecap="round"/>` +
      `<circle cx="${f(ear[0])}" cy="${f(ear[1])}" r="5" fill="${C.slate}" stroke="${ink}" stroke-width="1.6"/><circle cx="${f(mo[0])}" cy="${f(mo[1])}" r="5" fill="${C.slate}" stroke="${ink}" stroke-width="1.6"/>` +
      `<path d="M${f(mo[0])},${f(mo[1] + 4)} ${Array.from({ length: 9 }, (_, i) => `q${i % 2 ? 6 : -6},4 0,8`).join(" ")}" fill="none" stroke="${ink}" stroke-width="1.8"/>`;
    const laugh = `<path d="M${f(CR.top[0] + 14)},${f(CR.top[1] + 2)} l8,-8 M${f(CR.top[0] + 22)},${f(CR.top[1] + 12)} l10,-4 M${f(CR.top[0] + 4)},${f(CR.top[1] - 4)} l3,-10" stroke="${ink}" stroke-width="2.2" stroke-linecap="round"/>`;
    const clerk = `<defs><clipPath id="${fid}-win"><rect x="${win[0]}" y="${win[1]}" width="${win[2]}" height="${win[3]}"/></clipPath></defs>` +
      `<g clip-path="url(#${fid}-win)">${at(cx, cy, ck, K.person(co) + handset + laugh)}</g>`;
    // his back arm comes out over the counter in front of the window frame, so draw the stamp after the counter
    const stamp = at(sx, rubber, stampK, K.props.stamp({ text: "CHECKED" }));
    const thump = `<path d="M${sx - 58},${ledge - 2} l-18,-6 M${sx - 54},${ledge - 18} l-14,-14 M${sx + 58},${ledge - 2} l18,-6 M${sx + 54},${ledge - 18} l14,-14" stroke="${ink}" stroke-width="3.4" stroke-linecap="round"/>`;
    const cards = at(bx + 100, ledge + 24, 1, reviewCard(H, 5, true), 6) + at(bx + 94, ledge + 30, 1, reviewCard(H, 5, true), -3) +
      at(sx, ledge + 32, 1, reviewCard(H, 11, true), -2);
    const svg = push(S, 1.03, H.host("sideeye-closed", "palms-down", outTray(H, true) + lecternMug(H) + body + clerk + counter + cards + stamp + thump));
    return { svg, alt: "Wishonia side-eyes the camera at her lectern; beside her a little cream booth, REVIEW CHECKING, stands open, its clerk sitting sideways on the telephone, laughing, his arm reaching back out over the counter with a rubber stamp just lifted off a review card whose row of stars runs off both ends, stamped CHECKED, next to two more five-star cards stamped CHECKED." };
  },

  "wishocratic-slider"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "trials.": the whole slider: charred YOU at the knob, dragged right, on his bone legs; the medicine bills
    // piled at the lab, Grandma's skeleton waving TRIALS behind the bench; the empty bomb at the left end with its BANG
    // flag; the robot's antenna bulb poking out from under the track's right end
    const X0 = -560, X1 = 450, KX = 380;
    const pose = { look: "right", arms: [[30, 50], [40, 62]] };
    const R = K.rig(copy(YOU, pose));
    // his front hand on the knob's top (knob top at y -136)
    const you = at(KX - 4 - R.hand[1][0] * KP, -136 - 6 - R.hand[1][1] * KP, KP, charredYOU(H, pose, `${fid}-you`));
    const deskM = at(-1000, 0, 1, desk(H, { day: 9, noCal: false }));
    const bomb = at(-470, 10, 1.3, K.props.bomb({ lit: false, face: "worried" }));
    const flag = `<path d="M-430,-168 L-416,-262" stroke="${ink}" stroke-width="4"/><path d="M-416,-262 L-330,-252 L-338,-206 L-424,-216 Z" fill="${C.cream}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
      `<text x="-376" y="-224" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="30" fill="${C.war}" transform="rotate(6 -376 -234)">BANG</text>`;
    const funnel = at(-20, -10, 1.15, K.props.colorFlipFunnel({ label: "", inN: 0, outN: 2 }));
    const walkers = [140, 240].map((x, i) => at(x, -26, 0.9, K.money("med", i % 2))).join("");
    // Grandma's skeleton beside the bench, waving the TRIALS side of her poster overhead
    const gran = K.castOpts("grandma", { skeleton: true, arms: [[-150, -172], [-30, -60]] }), GR = K.rig(gran);
    const grandma = at(1060, -40 - 100 * KP, KP * 1.05, K.person(gran) + at(GR.hand[0][0], GR.hand[0][1], 1.5, poster(H, true), -8));
    const lab = at(760, -20, 1.45, K.props.lab({ liquid: "med" }));
    const spill = `<path d="M648,-372 q-10,-30 10,-40 q20,-22 40,0 q22,10 6,40 Z" fill="${C.med}" stroke="${ink}" stroke-width="3" opacity="0.95"/>` +
      [[640, -420, 14], [690, -440, 10], [668, -470, 8]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${C.med}" stroke="${ink}" stroke-width="2.5"/>`).join("");
    const medPile = at(600, 34, 1.1, pile(H, "med", 16, 220, 7));
    // the robot, charred and flattened under the track's right end: its helmet rim and a pincer arm stick out, and
    // the antenna bulb pokes up, blinking
    const bulb = `<path d="M372,30 L378,14 H530 L540,30 Z" fill="rgb(56,46,40)" stroke="${ink}" stroke-width="3.5" stroke-linejoin="round"/>` +
      `<path d="M520,18 Q556,12 566,22 L548,30" fill="#5A5934" stroke="${ink}" stroke-width="3.5" stroke-linejoin="round"/>` +
      `<path d="M386,26 L344,20 M344,20 l-12,-10 M344,20 l-12,10" fill="none" stroke="${ink}" stroke-width="6" stroke-linecap="round"/>` +
      `<path d="M470,14 V-80" stroke="${ink}" stroke-width="5"/><circle cx="470" cy="-92" r="13" fill="${C.war}" stroke="${ink}" stroke-width="4"/><path d="M448,-116 l-9,-11 M470,-122 v-15 M492,-116 l9,-11" stroke="${C.yellow}" stroke-width="4" stroke-linecap="round"/>`;
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="${GROUND}"/>` +
      view(250, -250, 0.95, field() + deskM + grandma + lab + spill + funnel + walkers + bomb + flag + medPile + you + slider(H, X0, X1, KX) + bulb);
    return { svg, alt: "Across the field lies a long cream slider: at its left end a small empty bomb with a BANG flag poking out, in the middle the color-flip funnel with medicine bills walking out of it, at its right end a lab bench bubbling over beside a pile of medicine bills, Grandma's skeleton waving a TRIALS poster behind it; the charred human in the bowler, standing on bone legs, holds the knob, dragged all the way right." };
  },

  "personally-to-blame"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "468,000": the WANTED poster over charred YOU in the spotlight, the YES button beside him with the stamped
    // treaty on it, and 2.6 humans waving from behind the medicine pile
    const you = at(300, -100 * KP, KP, charredYOU(H, { look: "right", arms: [[10, 4], [60, 30]] }, `${fid}-you`));
    const yes = at(470, 6, 1.9, K.props.yesButton({ label: "YES" }));
    const scroll = at(472, -196, 0.9, K.props.scroll({ text: "1% TREATY", wax: false }) + at(0, -40, 0.85, K.props.stampMark({ text: "PASSED", color: C.med, angle: -10 })));
    const lab = at(760, -20, 1.45, K.props.lab({ liquid: "med" }));
    const medPile = at(640, 34, 1.1, pile(H, "med", 16, 220, 7));
    const saved = [
      at(560, -40 - 100 * KP, KP, K.person({ tone: 1, outfit: "shirt", color: 1, mood: "smile", arms: [[-10, -4], [150, 170]] })),
      at(650, -40 - 100 * KP, KP, K.person({ tone: 0, outfit: "dress", hair: 1, color: 3, mood: "smile", arms: [[-150, -170], [10, 4]] })),
      at(745, -40 - 100 * KP, KP, partialPerson(H, fid, { tone: 3, outfit: "suit", color: 0, mood: "smile", arms: [[-10, -4], [140, 165]] }, 0.6)),
    ].join("");
    const pencil = at(772, -334, 0.62, K.pencil());
    // the WANTED poster, unrolled out of the sky behind him
    const px = 330, py = -800, pw = 420, ph = 470;
    const MR = K.rig(YOU);
    const poster = `<rect x="${px - pw / 2 + 10}" y="${py + 12}" width="${pw}" height="${ph}" fill="${ink}" opacity="0.5"/>` +
      `<rect x="${px - pw / 2}" y="${py}" width="${pw}" height="${ph}" fill="#F4E6C2" stroke="${ink}" stroke-width="5"/>` +
      `<rect x="${px - pw / 2 - 14}" y="${py - 16}" width="${pw + 28}" height="22" rx="11" fill="${C.tan}" stroke="${ink}" stroke-width="4"/>` +
      `<text x="${px}" y="${py + 82}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="74" letter-spacing="3" fill="${C.war}">WANTED</text>` +
      `<defs><clipPath id="${fid}-mug"><rect x="${px - 110}" y="${py + 104}" width="220" height="190"/></clipPath></defs>` +
      `<rect x="${px - 110}" y="${py + 104}" width="220" height="190" fill="#DCD4BE" stroke="${ink}" stroke-width="4"/>` +
      [0, 1, 2, 3, 4].map((i) => `<path d="M${px - 110},${py + 130 + i * 36} H${px - 90}" stroke="${ink}" stroke-width="2"/>`).join("") +
      `<g clip-path="url(#${fid}-mug)">${at(px - 4 - MR.eyes[0] * 1.95, py + 224 - MR.eyes[1] * 1.95, 1.95, charredYOU(H))}</g>` +
      `<text x="${px}" y="${py + 360}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="48" fill="${ink}">2.6 LIVES</text>` +
      `<text x="${px}" y="${py + 426}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="40" fill="${ink}">468,000 HOURS</text>`;
    // the spotlight: the field dimmed round a pool of light on him
    const dim = `<path fill-rule="evenodd" d="M-3000,-3000 H3000 V3000 H-3000 Z M${300 - 290},-30 a290,240 0 1,0 580,0 a290,240 0 1,0 -580,0 Z" fill="${C.navy}" opacity="0.38"/>` +
      `<path d="M-600,-1400 L-380,-1400 L560,-40 L80,40 Z" fill="${C.cream}" opacity="0.12"/>`;
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="${GROUND}"/>` +
      view(430, -380, 0.98, field() + lab + saved + pencil + medPile + dim + poster + you + yes + scroll);
    return { svg, alt: "In a spotlight on the darkened field the charred human in the bowler, on bone legs, stands beside a giant YES button with a 1% TREATY scroll stamped PASSED on it; behind him hangs a WANTED poster with his charred mugshot, 2.6 LIVES and 468,000 HOURS, and from behind a pile of medicine bills two whole humans and a third only 60% drawn, his top half a dashed pencil outline, wave." };
  },

  "love-you-bye"(H, fid) {
    const { K, C } = H, S = K.STUDIO, ink = C.line;
    // on "Love": she winks with her arms wide; the address sign hangs on its wires beside the lectern, and charred
    // YOU stands under it on his bone legs, tipping his bowler
    const sx = 1490, sy = 170, sw = 760, sh = 160;
    const wires = `<path d="M${sx - 280},-20 V${sy} M${sx + 280},-20 V${sy}" stroke="${ink}" stroke-width="3"/>`;
    const sign = `<rect x="${sx - sw / 2 + 10}" y="${sy + 12}" width="${sw}" height="${sh}" fill="${ink}" opacity="0.45"/>` +
      `<rect x="${sx - sw / 2}" y="${sy}" width="${sw}" height="${sh}" rx="10" fill="${C.navy}" stroke="${ink}" stroke-width="6"/>` +
      `<rect x="${sx - sw / 2 + 16}" y="${sy + 16}" width="${sw - 32}" height="${sh - 32}" rx="6" fill="none" stroke="${C.cream}" stroke-width="3"/>` +
      `<text x="${sx}" y="${sy + 100}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="54" letter-spacing="1" fill="${C.cream}">WARONDISEASE.ORG</text>`;
    // he holds his bowler up off his head in his front hand, the hair under it straight up and smoking
    const tipper = { charred: true, arms: [[-12, -6], [160, 175]] };
    const TR = K.rig(copy(YOU, tipper)), k = 2.9;
    const you = at(1520, 1066 - 100 * k, k, bonyYOU(H, tipper, `${fid}-you`) + at(TR.hand[1][0] - 4, TR.hand[1][1] - 2, 1, bowler(H), -18));
    const svg = push(S, 1.03, H.host("blink-smile", "wide-gesture", outTray(H, true) + lecternMug(H) + wires + sign + you));
    return { svg, alt: "Wishonia winks with her arms spread wide at her lectern; beside her a navy sign hangs on two wires, WARONDISEASE.ORG, and under it the charred human in the bowler, on bone legs, smoke curling off him, tips his hat." };
  },
};
