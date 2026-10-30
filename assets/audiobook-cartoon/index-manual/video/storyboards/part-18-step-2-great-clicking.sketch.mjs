// Sketches for storyboards/part-18-step-2-great-clicking.md: each scene's key moment on a 1920 x 1080 frame (16:9),
// in the film look (Part 2 is the reference). Host shots use H.host (KIT.STUDIO, 16:9: the lectern's reading top at
// y 790, x 540 to 980; the free wall for guests x 1100 to 1880); plates are drawn as the camera sees them at that
// moment, in plate units (a person at scale 1 is about 176 tall). Captions keep-out: below y 900.
// Built into the review sheet by tools/storyboard-sheet.mjs.

const f = (n) => (+n).toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});
// A plate framing as KIT.camera places it: plate point (x, y) in the middle of the frame, at scale s.
const view = (x, y, s, inner) => `<g transform="translate(${f(960 - x * s)},${f(540 - y * s)}) scale(${s})">${inner}</g>`;
// A host shot's slow push in on her face (KIT.studio), k of the way along.
const push = (S, k, inner) => `<g transform="translate(${S.face[0]},${S.face[1]}) scale(${k}) translate(${-S.face[0]},${-S.face[1]})">${inner}</g>`;
const at = (x, y, k, inner, rot = 0) => `<g transform="translate(${f(x)},${f(y)})${rot ? ` rotate(${rot})` : ""}${k !== 1 ? ` scale(${k})` : ""}">${inner}</g>`;
// A person standing with its feet on y `feet` at x, scale k.
const stand = (K, o, x, feet, k = 1) => at(x, feet - 100 * k, k, K.person(o));
// Fraunces Black in one color, and Oswald capitals.
const num = (x, y, size, text, fill, anchor = "middle", extra = "") => `<text x="${f(x)}" y="${f(y)}" text-anchor="${anchor}" font-family="Fraunces" font-weight="900" font-size="${size}" fill="${fill}" ${extra}>${text}</text>`;
const osw = (x, y, size, text, fill, anchor = "middle", extra = "") => `<text x="${f(x)}" y="${f(y)}" text-anchor="${anchor}" font-family="Oswald" font-weight="600" font-size="${size}" letter-spacing="${f(size * 0.05)}" fill="${fill}" ${extra}>${text}</text>`;

const SKY = "#EFE6C8", FIELD = "#C8B07B", COBBLE = "#B59A68", BRICK = "#C96F3E";

// ── Shared drawings ──────────────────────────────────────────────────────
// The clerk (the storyboard's shared drawing).
const CLERK = { outfit: "shirt", kind: "twig", tone: 2, color: 1, mood: "worried" };

// The thought bubble, around its own center: a faceted cream cloud about 120 x 80, three puffs trailing down to
// the head at (dx, 84). open: its top half flipped up like a lid, the inside dark, the tiny YES console glowing in it
// (o.inside: other markup in its place, around (0, 0)).
function bubble(K, C, o = {}) {
  const ink = C.line, n = 10, rx = 60, ry = 40;
  const pts = [];
  for (let i = 0; i < n * 2; i++) {
    const a = (i / (n * 2)) * Math.PI * 2, r = i % 2 ? 0.84 : 1;
    pts.push([rx * r * Math.cos(a), ry * r * Math.sin(a)]);
  }
  const P = (p) => p.map(([x, y]) => `${f(x)},${f(y)}`).join(" ");
  const top = pts.filter(([, y]) => y <= 0.01), bot = pts.filter(([, y]) => y >= -0.01);
  const dx = o.dx === undefined ? -16 : o.dx;
  const puffs = [[dx * 0.45, 50, 9], [dx * 0.75, 66, 6.5], [dx, 80, 4.5]].map(([x, y, r]) => {
    const h = [];
    for (let i = 0; i < 6; i++) h.push([x + r * Math.cos((i / 6) * Math.PI * 2 + 0.3), y + r * Math.sin((i / 6) * Math.PI * 2 + 0.3)]);
    return `<polygon points="${P(h)}" fill="${C.cream}" stroke="${ink}" stroke-width="2.6" stroke-linejoin="miter"/>`;
  }).join("");
  if (!o.open) {
    // shut: plain cream, halftone on its right side, the lid seam across the middle
    let dots = "";
    for (let y = -30; y <= 30; y += 7) for (let x = 14 + ((y / 7) % 2) * 3; x <= 54; x += 7) if ((x / rx) ** 2 + (y / ry) ** 2 < 0.62) dots += `<circle cx="${x}" cy="${y}" r="1.3" fill="${ink}" opacity="0.28"/>`;
    return `<g class="bubble">${puffs}<polygon points="${P(pts)}" fill="${C.cream}" stroke="${ink}" stroke-width="3" stroke-linejoin="miter"/>${dots}` +
      `<path d="M${-rx + 6},1 H${rx - 6}" stroke="${ink}" stroke-width="2" stroke-dasharray="7 5" opacity="0.6"/></g>`;
  }
  const bowl = `<polygon points="${P(bot)}" fill="${C.cream}" stroke="${ink}" stroke-width="3" stroke-linejoin="miter"/>`;
  const insideD = `<path d="M${-rx + 8},2 Q0,${ry * 0.6} ${rx - 8},2 Z" fill="${C.navy}"/>`;
  const glow = `<ellipse cx="0" cy="-10" rx="38" ry="26" fill="${C.med}" opacity="0.3"/>`;
  const inside = o.inside !== undefined ? o.inside : at(0, 12, 0.36, K.props.yesButton({ label: "YES" }));
  const lid = `<g transform="rotate(${o.lid || -40} ${-rx} 0)"><polygon points="${P(top)}" fill="${C.cream}" stroke="${ink}" stroke-width="3" stroke-linejoin="miter"/>` +
    `<path d="M${-rx + 8},-1 Q0,${-ry * 0.5} ${rx - 8},-1 Z" fill="#D9CDA6"/></g>`;
  return `<g class="bubble">${puffs}${glow}${lid}${bowl}${insideD}${inside}</g>`;
}

// The Grim Reaper with a wristwatch on his bone hand; o.scythe rotates the scythe about that hand.
function reaper(K, C, o = {}) {
  const h = K.REAPER.hand[1];
  const watch = `<g transform="translate(${h[0]},${h[1] - 24})"><rect x="-12" y="-4.5" width="24" height="9" fill="${C.navy}" stroke="${C.line}" stroke-width="2"/><circle cx="0" cy="0" r="7" fill="${C.cream}" stroke="${C.line}" stroke-width="2.2"/><path d="M0,0 V-4.5 M0,0 L3,1.5" stroke="${C.line}" stroke-width="1.4"/></g>`;
  return K.reaper({ pose: "puppet", scythe: !o.noScythe, arms: [0, o.scythe || 0] }) + (o.scythe ? "" : watch);
}
// Just the scythe, flying loose (where the Reaper's fist would hold it).
function scythe(K) {
  return K.reaper({ only: "scythe" });
}

// The Reaper's tally clipboard, around its bottom middle (104 wide, 160 tall): tally marks in fives.
function tallyBoard(K, C, marks = 13) {
  let t = "";
  for (let i = 0; i < marks; i++) {
    const grp = Math.floor(i / 5), k = i % 5, gx = -30 + (grp % 3) * 24, gy = -116 + Math.floor(grp / 3) * 32;
    t += k < 4 ? `<path d="M${gx + k * 5},${gy} v20" stroke="${C.line}" stroke-width="2.6"/>` : `<path d="M${gx - 3},${gy + 15} L${gx + 19},${gy + 5}" stroke="${C.line}" stroke-width="2.6"/>`;
  }
  return K.props.clipboard({ title: "", items: [] }) + t;
}

// The 3.5% dial on the lectern, standing on (x, y) at scale k (needle a hair off zero); o.spring: "?" or "!" on a
// coil spring over it, leaning o.tilt degrees.
function dial(K, C, x, y, k, o = {}) {
  const v = o.value === undefined ? 0.006 : o.value;
  const g = K.props.gauge({ mount: "dial", label: "", value: v, zones: [], marks: [[0.035, "3.5%"]] });
  let spring = "";
  if (o.spring) {
    const top = -124, h = o.h || 74, n = 8;
    let d = `M0,${top}`;
    for (let i = 1; i <= n; i++) d += ` L${i % 2 ? 10 : -10},${f(top - (h * i) / n)}`;
    d += ` L0,${top - h - 6}`;
    const mark = at(0, top - h - 4, 1, num(0, 0, 86, o.spring, C.navy, "middle", `stroke="${C.cream}" stroke-width="6" style="paint-order:stroke"`));
    const bob = o.bob ? `<path d="M-40,${top - h - 66} q-10,12 0,24 M40,${top - h - 66} q10,12 0,24" fill="none" stroke="${C.line}" stroke-width="3.4" stroke-linecap="round"/>` : "";
    spring = `<g transform="rotate(${o.tilt || 0} 0 ${top})"><path d="${d}" fill="none" stroke="${C.line}" stroke-width="7" stroke-linejoin="miter"/><path d="${d}" fill="none" stroke="${C.slate}" stroke-width="3" stroke-linejoin="miter"/>${mark}${bob}</g>`;
  }
  return at(x, y, k, spring + g);
}
// The 3.5% dial where every host shot puts it: the right end of the lectern's reading top, the spring leaning right.
const lecternDial = (K, C, o = {}) => dial(K, C, 952, K.STUDIO.top, 1.4, copy({ tilt: 24 }, o));

// Shake lines either side of a point (a head shaking, a thing rattling).
const shake = (C, x, y, w, h = 30) => `<path d="M${x - w},${y - h / 2} q-8,${h / 2} 0,${h} M${x - w - 12},${y - h / 2 + 4} q-8,${h / 2 - 4} 0,${h - 8} M${x + w},${y - h / 2} q8,${h / 2} 0,${h} M${x + w + 12},${y - h / 2 + 4} q8,${h / 2 - 4} 0,${h - 8}" fill="none" stroke="${C.line}" stroke-width="3.2" stroke-linecap="round"/>`;
// Motion lines trailing behind something moving along (dx, dy).
const speed = (C, x, y, dx, dy, n = 3, gap = 14, w = 3) => {
  let d = "";
  const L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L;
  for (let i = 0; i < n; i++) {
    const ox = -uy * (i - (n - 1) / 2) * gap, oy = ux * (i - (n - 1) / 2) * gap;
    d += `M${f(x + ox)},${f(y + oy)} l${f(-dx)},${f(-dy)} `;
  }
  return `<path d="${d}" stroke="${C.line}" stroke-width="${w}" stroke-linecap="round"/>`;
};
// A little TV set on the lectern (its screen markup in place of the marker), standing on (x, y) at scale k;
// ears: "up" (both antennas straight up).
function lecternTV(K, C, x, y, k, screen, ears) {
  let tv = K.props.tvSet({}).replace("<!--tv-screen-->", screen || "");
  if (ears === "up") tv = tv.replace(/L-46,-214/g, "L-12,-248").replace(/cx="-46" cy="-214"/g, 'cx="-12" cy="-248"').replace(/L42,-220/g, "L14,-252").replace(/cx="42" cy="-220"/g, 'cx="14" cy="-252"');
  return at(x, y, k, tv);
}
// The tiny twerker on a TV screen (screen units: the screen is x -63..17, y -134..-51).
function twerker(C, x, y, k = 1) {
  return at(x, y, k, `<circle cx="0" cy="-34" r="7.5" fill="#D9A877" stroke="${C.line}" stroke-width="2"/>` +
    `<path d="M-6,-26 h12 l5,15 l9,5 l-3,7 l-8,-3 l3,24 h-6 l-4,-18 l-4,18 h-6 l3,-24 l-8,3 l-3,-7 l9,-5 Z" fill="${C.orange}" stroke="${C.line}" stroke-width="2" stroke-linejoin="miter"/>` +
    `<path d="M14,-14 q7,4 6,12 M-14,-14 q-7,4 -6,12" fill="none" stroke="${C.cream}" stroke-width="2.4" stroke-linecap="round"/>`);
}

// ── The town-square plate (plate units) ──────────────────────────────────
// Back street: feet on y -360; factories at x -900, -420, 60 (the right one's door open); the funnel at -180; the lab
// at 440 and the Scientist at 650. The square: three rows of eight, feet at y 40, 250, 460; the wall at x 720 to 1160.
const STREET = -360, ROWS = [40, 250, 460], FACT = [-900, -420, 60], WALL = [720, 1160, -300, 480], LAB = 440, SCI = 650;
function crowdList() {
  const list = [];
  ROWS.forEach((y, r) => {
    for (let i = 0; i < 8; i++) {
      const x = -560 + i * 140 + (r === 1 ? 70 : r === 0 ? 30 : 0);
      const hair = [0, 1, 0, 1, 2, 0, 1, 0][(i + r * 3) % 8];
      const outfit = hair === 1 ? "dress" : ["shirt", "suit", "overalls", "shirt", "suit"][(i + r) % 5];
      list.push({ x, y, r, i, o: { outfit, hair, tone: (i * 3 + r) % 4, color: (i + r * 2) % 4, seed: r * 8 + i + 11, mood: "flat" } });
    }
  });
  const front = list.filter((p) => p.r === 2);
  front[2].who = "oldwoman"; front[3].who = "oldman"; front[7].who = "economist";
  list.filter((p) => p.r === 0)[5].who = "weaponsMaker";
  return list;
}
const OLDMAN = { outfit: "shirt", kind: "shirt", tone: 1, color: 2, hair: 2, hairStyle: "bald", glasses: true, mood: "flat", build: { hunch: 8, hs: 0.95 } };
// The old woman (the storyboard's shared drawing): an everyday human, not the cast's Grandma (a skeleton since Part 17).
const OLDWOMAN = { outfit: "dress", kind: "hourglass", hair: 1, hairStyle: "bun", hairColor: "#E8E4DA", tone: 3, color: 0, mood: "smile", build: { hunch: 10, legs: 0.82 } };
const ECON = { outfit: "suit", kind: "box", tone: 3, color: 0, glasses: true, hat: "fedoraUp", mood: "smug" };
function optsFor(K, p, mods = {}) {
  if (p.who === "oldwoman") return copy(OLDWOMAN, mods);
  if (p.who === "oldman") return copy(OLDMAN, mods);
  if (p.who === "economist") return copy(ECON, copy({ holdR: "clipboard" }, mods));
  if (p.who === "weaponsMaker") return mods.arms ? K.castOpts("weaponsMaker", mods) : copy(K.CAST.weaponsMaker, mods);
  return copy(p.o, mods);
}
// The baby's bonnet on the Weapons Maker's missile, in the held missile's own units (its nose cone x 14..30): a frilly
// cream hood with an orange ribbon.
function bonnet(C) {
  const ink = C.line;
  let frill = "";
  for (let i = 0; i < 6; i++) frill += `<circle cx="11" cy="${f(-10 + i * 4)}" r="2.8" fill="#FBF6E6" stroke="${ink}" stroke-width="1.2"/>`;
  return `<path d="M12,-11 Q30,-13 37,0 Q30,13 12,11 Z" fill="${C.cream}" stroke="${ink}" stroke-width="1.8"/>` +
    `<path d="M18,-9 Q30,-8 34,0 M18,9 Q30,8 34,0" fill="none" stroke="${ink}" stroke-width="1" opacity="0.5"/>` + frill +
    `<path d="M12,11 l-6,8 M12,11 l3,9" stroke="${C.orange}" stroke-width="2.4" stroke-linecap="round"/><circle cx="12" cy="11" r="2.6" fill="${C.orange}" stroke="${ink}" stroke-width="1"/>`;
}
// The empty bonnet from the front, around (0, 0), about 46 wide: the cream hood, its dark empty inside, the frill
// round the opening and the orange ribbons hanging loose.
function emptyBonnet(C) {
  const ink = C.line;
  let frill = "";
  for (let i = 0; i <= 8; i++) { const a = Math.PI * (1 + i / 8); frill += `<circle cx="${f(15 * Math.cos(a))}" cy="${f(2 + 15 * Math.sin(a))}" r="3.2" fill="#FBF6E6" stroke="${ink}" stroke-width="1.2"/>`; }
  return `<path d="M-15,12 q-6,10 -10,22 M15,12 q6,10 10,22" fill="none" stroke="${C.orange}" stroke-width="3" stroke-linecap="round"/>` +
    `<path d="M-23,12 Q-25,-22 0,-24 Q25,-22 23,12 Z" fill="${C.cream}" stroke="${ink}" stroke-width="2"/>` +
    `<path d="M-14,10 Q-15,-12 0,-13 Q15,-12 14,10 Z" fill="${C.navy}"/>` + frill +
    `<circle cx="-15" cy="12" r="3" fill="${C.orange}" stroke="${ink}" stroke-width="1"/><circle cx="15" cy="12" r="3" fill="${C.orange}" stroke="${ink}" stroke-width="1"/>`;
}
// Where a person's held prop sits (the middle of the two hands), in person units.
const heldAt = (K, o) => { const R = K.rig(o); return [(R.hand[0][0] + R.hand[1][0]) / 2, (R.hand[0][1] + R.hand[1][1]) / 2 + 2]; };
// The bucket upside down on the Weapons Maker's head, orange paint running down (person units, over the head).
const bucketHat = (C) => `<path d="M-24,-118 h48 l-6,38 h-36 Z" fill="${C.slate}" stroke="${C.line}" stroke-width="3"/><path d="M-24,-118 h48 v7 h-48 Z" fill="${C.orange}" stroke="${C.line}" stroke-width="2"/>` +
  `<path d="M-20,-80 q-4,30 2,48 M16,-80 q4,26 -2,40 M0,-80 v26" stroke="${C.orange}" stroke-width="7" stroke-linecap="round"/>`;
// The wall at the right of the square, with SUPP painted on it from proving-it on.
function wall(C, supp) {
  const [x0, x1, y0, y1] = WALL;
  let bricks = "";
  for (let y = y0 + 40, i = 0; y < y1; y += 40, i++) {
    bricks += `<path d="M${x0},${y} H${x1}" stroke="${C.line}" stroke-width="1.6" opacity="0.3"/>`;
    for (let x = x0 + (i % 2) * 40; x < x1; x += 80) bricks += `<path d="M${x},${y - 40} v40" stroke="${C.line}" stroke-width="1.6" opacity="0.25"/>`;
  }
  const letters = supp ? num(850, -30, 110, "SUPP", C.cream, "start", `stroke="${C.line}" stroke-width="4" style="paint-order:stroke" letter-spacing="-2"`) +
    [[876, -30], [936, -26], [1002, -30], [1062, -28]].map(([x, y], i) => `<path d="M${x},${y} v${24 + (i % 3) * 12}" stroke="${C.cream}" stroke-width="8" stroke-linecap="round"/>`).join("") : "";
  return `<rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" fill="${BRICK}" stroke="${C.line}" stroke-width="5"/>` + bricks + letters +
    `<rect x="${x0 - 10}" y="${y0 - 14}" width="${x1 - x0 + 20}" height="18" fill="${C.slate}" stroke="${C.line}" stroke-width="4"/>`;
}
// The painter's ladder leaning on the wall (foot at (690, 480), top at (770, -220)), or fallen flat in front of the crowd.
function ladder(C, lying) {
  const rails = lying ? [[-20, 510, 700, 510], [-20, 538, 700, 538]] : [[690, 480, 770, -220], [760, 480, 840, -220]];
  let out = rails.map(([a, b, c, d]) => `<path d="M${a},${b} L${c},${d}" stroke="${C.line}" stroke-width="14"/><path d="M${a},${b} L${c},${d}" stroke="#B98A55" stroke-width="7"/>`).join("");
  for (let i = 0; i < 12; i++) {
    const u = (i + 0.5) / 12;
    const [x0, y0] = [rails[0][0] + (rails[0][2] - rails[0][0]) * u, rails[0][1] + (rails[0][3] - rails[0][1]) * u];
    const [x1, y1] = [rails[1][0] + (rails[1][2] - rails[1][0]) * u, rails[1][1] + (rails[1][3] - rails[1][1]) * u];
    out += `<path d="M${f(x0)},${f(y0)} L${f(x1)},${f(y1)}" stroke="${C.line}" stroke-width="9"/><path d="M${f(x0)},${f(y0)} L${f(x1)},${f(y1)}" stroke="#B98A55" stroke-width="4"/>`;
  }
  return out;
}
// The whole plate in one of its states: "question" (the-question), "proving" (on "supports"), "plural" (on
// "permission"), "realize" (after "unrecognizable.").
function townSquare(K, C, st) {
  const ink = C.line, hosp = st === "realize";
  let out = `<rect x="-4000" y="-4000" width="8000" height="${4000 + STREET - 130}" fill="${SKY}"/><rect x="-4000" y="${STREET - 130}" width="8000" height="6000" fill="${FIELD}"/>`;
  // fireworks over the street
  if (hosp) out += [[-640, -790, C.yellow, 1], [-160, -860, C.orange, 1.15], [420, -800, C.med, 1.05], [-400, -700, C.cream, 0.75], [160, -720, C.yellow, 0.7], [760, -760, C.orange, 0.85]].map(([x, y, col, s]) => {
    let rays = "";
    for (let i = 0; i < 14; i++) {
      const a = (i / 14) * Math.PI * 2, r0 = 30 * s, r1 = (100 + (i % 2) * 26) * s;
      rays += `<path d="M${f(x + r0 * Math.cos(a))},${f(y + r0 * Math.sin(a))} L${f(x + r1 * Math.cos(a))},${f(y + r1 * Math.sin(a))}" stroke="${col}" stroke-width="${f(9 * s)}" stroke-linecap="round"/>`;
    }
    return rays + K.star(x, y, 24 * s, col);
  }).join("");
  // the street, the factories (or hospitals), the funnel, the lab and the Scientist
  out += `<rect x="-4000" y="${STREET - 10}" width="8000" height="70" fill="${COBBLE}"/><path d="M-4000,${STREET - 10} H4000" stroke="${ink}" stroke-width="3" opacity="0.5"/>` +
    `<path d="M-4000,${STREET + 26} H4000" stroke="${ink}" stroke-width="2" stroke-dasharray="26 18" opacity="0.35"/>`;
  out += FACT.map((x, i) => hosp ? at(x, STREET, 1, K.props.hospital({ label: "" })) : at(x, STREET, 1, i === 2 ? K.props.factory({ label: "" }).replace('class="factory-door"', 'class="factory-door" opacity="0"') : K.props.factory({ label: "" }))).join("");
  if (!hosp) out += at(-180, STREET, 1, K.props.colorFlipFunnel({ inN: 0, outN: 0 }));
  out += at(LAB, STREET, 1, K.props.lab({}));
  if (st === "question") {
    // the war money filing along the street into the open door; the medicine bill on the bench; boiling over
    for (let i = 0; i < 8; i++) {
      const x = -390 + i * 62;
      out += `<g opacity="${x > 30 ? 0.4 : 1}">${at(x, STREET - 34, 0.7, K.money("war", i % 2))}</g>`;
    }
    out += [[-40, -230], [10, -250], [70, -232], [120, -214]].map(([x, y], i) => `<path d="M${LAB + x},${STREET + y + 60} q-12,-18 0,-34 q12,-16 0,-32" fill="none" stroke="${C.med}" stroke-width="9" stroke-linecap="round"/>` +
      `<circle cx="${LAB + x + (i % 2 ? 10 : -8)}" cy="${STREET + y - 18}" r="${7 + (i % 2) * 3}" fill="${C.med}" stroke="${ink}" stroke-width="2.4"/>`).join("");
    out += at(LAB + 150, STREET - 300, 0.9, K.props.pillBottle({ face: "smile" }), 10) + speed(C, LAB + 148, STREET - 320, 0, -70, 3, 18);
    out += at(LAB - 70, STREET - 96 - 28, 0.7, K.money("med", 1));
    out += stand(K, K.castOpts("scientist", { look: "left", mood: "eager", arms: [[-150, -170], [150, 170]] }), SCI, STREET, 1.05);
  } else {
    out += stand(K, K.castOpts("scientist", { look: "left" }), SCI, STREET, 1.05);
  }
  out += wall(C, st !== "question");
  if (hosp) out += at(1010, -150, 1.2, K.props.calendar({ month: "JAN", day: 2 })) + at(1012, -184, 0.75, K.props.stampMark({ text: "DONE", angle: -10 }));
  // the ladder, the bucket and the painter
  if (st === "question" || st === "proving") {
    out += ladder(C, false) + `<path d="M788,-256 h48 l-5,40 h-38 Z" fill="${C.slate}" stroke="${ink}" stroke-width="3"/><path d="M788,-256 h48 v7 h-48 Z" fill="${C.orange}"/><path d="M790,-256 q22,-24 44,0" fill="none" stroke="${ink}" stroke-width="2.4"/>`;
    // on the ladder, feet on a rung at y -40: painting rightward (question), or stopped with the brush in the air
    // looking down over his shoulder at the crowd (proving)
    const P = st === "proving" ? { outfit: "overalls", kind: "barrel", tone: 1, color: 3, look: "left", mood: "eager", hat: null, arms: [[10, 4], [150, 168]] }
      : { outfit: "overalls", kind: "barrel", tone: 1, color: 3, look: "right", mood: "smile", hat: null, arms: [[10, 4], [80, 110]] };
    const px = 752, pf = -40, R = K.rig(P), hx = px + R.hand[1][0], hy = pf - 100 + R.hand[1][1];
    out += stand(K, P, px, pf, 1) + at(hx, hy, 1, `<path d="M0,0 l8,-30" stroke="${ink}" stroke-width="7" stroke-linecap="round"/><path d="M0,-30 h16 l4,-16 h-24 Z" fill="${C.cream}" stroke="${ink}" stroke-width="2.4"/>`, st === "proving" ? -10 : 60);
  } else {
    out += ladder(C, true);
    out += stand(K, { outfit: "overalls", kind: "barrel", tone: 1, color: 3, look: "left", mood: "flat", hat: null, holdR: "clipboard", arms: [[10, 4], [-60, -110]] }, 600, 470, 1);
  }
  // the crowd, back row first: bubbles, then people
  const crowd = crowdList();
  const raise = [[-6, -2], [118, 150]];
  let hands = [], late = "";
  ROWS.forEach((ry, r) => {
    const row = crowd.filter((p) => p.r === r);
    row.forEach((p) => {
      let mods = {};
      if (st === "proving") mods = p.who === "weaponsMaker" ? { mood: "cross" } : p.who ? {} : { mood: "smile", hat: null };
      if (st === "plural") mods = p.who === "weaponsMaker" ? { arms: raise, mood: "worried" } : p.who === "oldman" ? { arms: raise, skeleton: true } : copy({ arms: raise }, p.who === "economist" ? { holdR: null } : {});
      if (st === "realize") mods = p.who === "weaponsMaker" ? { arms: [[30, 80], [-30, -80]], mood: "worried" } : p.who === "oldman" ? { skeleton: true } : { mood: (p.i + r) % 3 ? "eager" : "smile", hat: null };
      const o = optsFor(K, p, mods);
      const nod = st === "proving" && p.who !== "weaponsMaker" ? 8 : 0;
      const open = st === "realize";
      const inside = open ? at(-16, 6, 0.28, K.props.earthGlobe({ r: 80, face: "smile" })) + at(28, 18, 0.62, [0, 1, 2, 3, 4].map((i) => `<rect x="-22" y="${-i * 6}" width="44" height="7" fill="${C.money}" stroke="${ink}" stroke-width="1.6"/>`).join("") + `<rect x="-5" y="-26" width="10" height="34" fill="${C.cream}" stroke="${ink}" stroke-width="1.4"/>`) : undefined;
      out += at(p.x + 14, p.y - 252, open ? 0.95 : 0.88, bubble(K, C, { open, inside }));
      out += at(p.x, p.y - 100 + nod, 1, K.person(o));
      if (p.who === "weaponsMaker" && st !== "question" && st !== "proving") out += at(p.x, p.y - 100, 1, bucketHat(C));
      if (p.who === "weaponsMaker" && o.hold === "missile") { const [hx, hy] = heldAt(K, o); out += at(p.x + hx, p.y - 100 + hy, 1, `<g transform="translate(0,-6) rotate(-14)">${bonnet(C)}</g>`); }
      if (p.who === "weaponsMaker" && st === "realize") { const [hx, hy] = heldAt(K, o); late += at(p.x + hx, p.y - 100 + hy + 8, 0.8, emptyBonnet(C), -8); }
      if (p.who === "weaponsMaker" && st === "proving") out += shake(C, p.x + 2, p.y - 180, 36, 28) + shake(C, p.x + 2, p.y - 92, 30, 18);
      if (st === "proving" && !p.who && (p.i + r) % 2 === 0) out += at(p.x + 3, p.y - 210, 1, `<path d="M-16,0 L-12,-16 L0,-20 L12,-16 L16,0 Z M-26,4 L-20,-1 H20 L26,4 Z" fill="${C.navy}" stroke="${ink}" stroke-width="2.4"/><path d="M-12,14 v12 M12,14 v12" stroke="${ink}" stroke-width="2.4" stroke-linecap="round"/>`);
      if (st === "plural") {
        const R = K.rig(copy(o, { skeleton: false }));
        hands.push([p.x + R.hand[1][0], p.y - 100 + R.hand[1][1], r]);
      }
      if (st === "realize" && p.who === "oldman") out += at(p.x + 8, p.y + 2, 1, `<path d="M-12,0 q12,8 24,0 l-3,7 q-9,4 -18,0 Z" fill="#F1EBDA" stroke="${ink}" stroke-width="2"/>`);
      if (st === "realize" && p.who === "weaponsMaker") late += at(p.x + 44, p.y - 236, 1.15, K.props.priceTag({ text: "+$518,879", angle: 16 }));
    });
  });
  // cobwebs strung between neighboring raised hands in each row
  if (st === "plural") [0, 1, 2].forEach((r) => {
    const hs = hands.filter((h) => h[2] === r).sort((a, b) => a[0] - b[0]);
    for (let i = 0; i + 1 < hs.length; i++) {
      const [x0, y0] = hs[i], [x1, y1] = hs[i + 1], mx = (x0 + x1) / 2, my = (y0 + y1) / 2 + 26;
      out += `<path d="M${f(x0)},${f(y0)} Q${f(mx)},${f(my)} ${f(x1)},${f(y1)} M${f(x0)},${f(y0)} L${f(mx)},${f(my + 12)} L${f(x1)},${f(y1)} M${f(mx)},${f(my - 20)} V${f(my + 24)}" fill="none" stroke="#FBF6E6" stroke-width="2.4" opacity="0.95"/>`;
    }
  });
  return out + late;
}

export default {
  "step-2-great-clicking-title"(H, fid) {
    const { K, C } = H;
    // KIT.titleScene's atomic card (16:9): the emblem at (960, 300), rx 200, ry 62, papers at 0.62. A beat after
    // "Clicking.": the finger pressing the nucleus, the paper on the left of its orbit stopped, its new cross seal.
    const cx = 960, cy = 300, rx = 200, ry = 62, TILT = [0, 60, -60], t = 1.7;
    const orbits = TILT.map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = TILT.map((a, i) => {
      if (i === 0) {
        // stopped at the left end of the flat orbit, looking down at its new seal
        const x = cx - rx + 4, y = cy - 6;
        const eyes = `<path d="M8,-50 q8,-7 16,0 M28,-50 q8,-7 16,0" fill="none" stroke="${C.cream}" stroke-width="3.4"/><ellipse cx="16" cy="-38" rx="9" ry="11" fill="${C.cream}" stroke="${C.line}" stroke-width="2.4"/><ellipse cx="36" cy="-38" rx="9" ry="11" fill="${C.cream}" stroke="${C.line}" stroke-width="2.4"/><circle cx="19" cy="-31" r="3.6" fill="${C.line}"/><circle cx="39" cy="-31" r="3.6" fill="${C.line}"/>`;
        return at(x, y, 0.9, K.money("med", 0) + eyes) + `<path d="M${f(x + 54)},${f(y + 6)} h30 M${f(x + 54)},${f(y + 20)} h22" stroke="${C.cream}" stroke-width="3.4" stroke-linecap="round"/>`;
      }
      const th = i * 2.1 + t * 2.4, ar = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return at(cx + ex * Math.cos(ar) - ey * Math.sin(ar), cy + ex * Math.sin(ar) + ey * Math.cos(ar) - 6, 0.62, K.money("war", i % 2));
    }).join("");
    // the nucleus, pressed in, and the finger in its shirt cuff from the top edge
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="36" fill="#0A1426"/><circle cx="${cx}" cy="${cy + 4}" r="26" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/>`;
    const skin = "#C99467";
    const finger = `<path d="M${cx - 14},${cy - 20} V${cy - 120} L${cx - 34},${cy - 150} L${cx - 42},-20 H${cx + 46} L${cx + 32},${cy - 160} L${cx + 14},${cy - 122} V${cy - 20} Q${cx},${cy - 8} ${cx - 14},${cy - 20} Z" fill="${skin}" stroke="${C.line}" stroke-width="4" stroke-linejoin="miter"/>` +
      `<path d="M${cx - 7},${cy - 34} q7,4 14,0 M${cx - 8},${cy - 88} h16" fill="none" stroke="${C.line}" stroke-width="2.4"/>` +
      `<path d="M${cx - 54},-20 L${cx - 48},${cy - 196} H${cx + 52} L${cx + 58},-20 Z" fill="${C.cream}" stroke="${C.line}" stroke-width="4"/><path d="M${cx - 48},${cy - 196} H${cx + 52}" stroke="${C.line}" stroke-width="7"/><circle cx="${cx + 30}" cy="${cy - 214}" r="5" fill="${C.slate}" stroke="${C.line}" stroke-width="2"/>` +
      `<path d="M${cx - 44},${cy - 4} l-22,-10 M${cx + 44},${cy - 4} l22,-10 M${cx - 38},${cy + 18} l-24,8 M${cx + 38},${cy + 18} l24,8" stroke="${C.cream}" stroke-width="4" stroke-linecap="round"/>`;
    const word = (y, s, text) => {
      const t0 = (dx, dy, extra) => `<text x="${960 + dx}" y="${y + dy}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${s}" ${extra}>${H.esc(text)}</text>`;
      return t0(0.04 * s, 0.053 * s, `fill="${C.ink}"`) + t0(0, 0, `fill="${C.cream}" stroke="${C.cream}" stroke-width="${f(0.044 * s)}" stroke-linejoin="round" style="paint-order:stroke"`);
    };
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus + finger + word(640, 92, "STEP 2:") + word(810, 136, "THE GREAT CLICKING");
    return { svg, alt: "The period title card: on plain navy, STEP 2: THE GREAT CLICKING under the film's atom; a finger in a shirt cuff pokes down from the top edge and presses the orange nucleus like a doorbell, and one of the three running papers has skidded to a stop, looking down at the new cross on its seal." };
  },

  "click-to-not-die"(H, fid) {
    const { K, C } = H, S = K.STUDIO;
    // on "Die": the console (x 1215) and the clerk (x 1450, facing left, his finger on the cap) on the free wall,
    // feet at y 1070, scale 2.75; the Reaper behind him (x 1730), the scythe swung round and stopped at his neck
    const k = 2.75, feet = 1070;
    const clerk = copy(CLERK, { look: "left", arms: [[-62, -80], [10, 4]] });
    const console_ = at(1215, feet, k, K.props.yesButton({ label: "YES", sub: "TREATY" }));
    const man = stand(K, clerk, 1452, feet, k);
    const R = K.rig(clerk), neck = [1452 + R.neck[0] * k, feet - 100 * k + R.neck[1] * k];
    // the Reaper behind the clerk; his scythe drawn in front of him, lowered so the blade wraps round the clerk's neck
    const RX = 1660, RY = feet - 100 * 2.6 + 60;
    const reap = at(RX, RY, 2.6, reaper(K, C, { noScythe: true }));
    const blade = at(RX, RY, 2.6, `<g transform="translate(-8,138)">${scythe(K, C)}</g>`);
    const stopLines = `<path d="M${f(neck[0] - 62)},${f(neck[1] - 6)} l-16,-14 M${f(neck[0] - 66)},${f(neck[1] + 14)} l-20,0 M${f(neck[0] - 62)},${f(neck[1] + 34)} l-16,12" stroke="${C.line}" stroke-width="4" stroke-linecap="round"/>`;
    const sweat = `<path d="M${f(neck[0] + 6)},${f(neck[1] - 150)} q-9,13 0,18 q9,-5 0,-18 Z" fill="${C.cyan}" stroke="${C.line}" stroke-width="2"/>`;
    const front = reap + console_ + man + blade + stopLines + sweat + lecternDial(K, C);
    const svg = push(S, 1.012, H.host("smirk-smile", "idle", front));
    return { svg, alt: "Wishonia smirks at the camera from her lectern, the 3.5% dial on its right end. Beside the lectern a worried beanpole clerk has just pressed the big teal YES button on its console, and behind him the Grim Reaper's scythe has stopped an inch from his neck." };
  },

  "the-question"(H, fid) {
    const { K, C } = H;
    // after "trials?": framing on the right of the back street (plate x 330, y -560, scale 1.45)
    const svg = view(260, -600, 1.45, townSquare(K, C, "question"));
    return { svg, alt: "On the town's back street the line of war money files into the open door of a war factory with grinning missile chimneys, while the one bill the funnel took, now wearing a cross seal, stands on the Scientist's lab bench: every flask boils over, a pill bottle pops up out of the beaker like toast, and the Scientist throws up her arms." };
  },

  "proving-it"(H, fid) {
    const { K, C } = H;
    // on "supports": the crowd mid-nod, hats in the air, the Weapons Maker and his missile shaking their heads; at
    // the right, SUPP on the wall and the painter up his ladder, brush in the air (plate x 360, y 40, scale 0.86)
    const svg = view(270, 40, 0.9, townSquare(K, C, "proving"));
    return { svg, alt: "The town square: three rows of everyday humans under shut cream thought bubbles nod all at once so hard their hats hop into the air; in the middle the Weapons Maker and the missile in his arms shake their heads. Behind them the war factories puff; at the right a painter up his ladder has stopped, brush in the air, after painting SUPP on the wall." };
  },

  "pluralistic-ignorance"(H, fid) {
    const { K, C } = H;
    // on "permission": the front rows close (plate x -130, y 300, scale 1.55)
    const svg = view(-150, 330, 1.8, townSquare(K, C, "plural"));
    return { svg, alt: "Close on the front rows of the town square: every human holds a hand half raised, like a class waiting to be called on, with cobwebs strung between the hands; beside the old woman with her white bun, her husband is now a grinning skeleton, his hand still half up, and every thought bubble over them is shut." };
  },

  "you-go-first"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "finish": pulled back over the night sky: Earth in the middle with its hill, VOTE door, Reaper and bowing
    // line; five little planets round it gone dark, a headstone on each, their tiny skeleton lines still bowing
    let stars = "";
    const r = K.rng(1811);
    for (let i = 0; i < 90; i++) stars += K.star(r() * 1920, r() * 1080, 3 + r() * 6, C.yellow);
    const bow = [[-30, -64], [40, 70]], hunch = 30;
    const planet = (x, y, rr, col) => {
      const dark = K.mix(col, "#0E1626", 0.72), k = rr / 230;
      let line = "";
      for (let i = 0; i < 4; i++) line += at(x + rr * 0.05 - i * 46 * k * 1.2, y - rr + 10 * k + i * 4 * k, 0.5 * k, K.person({ skeleton: true, look: "right", arms: bow, build: { hunch } }));
      return `<circle cx="${x}" cy="${y}" r="${rr}" fill="${dark}" stroke="${ink}" stroke-width="5"/>` +
        `<circle cx="${f(x - rr * 0.3)}" cy="${f(y + rr * 0.2)}" r="${f(rr * 0.16)}" fill="none" stroke="${ink}" stroke-width="3" opacity="0.4"/><circle cx="${f(x + rr * 0.35)}" cy="${f(y + rr * 0.35)}" r="${f(rr * 0.1)}" fill="none" stroke="${ink}" stroke-width="3" opacity="0.4"/>` +
        at(x + rr * 0.32, y - rr + 18 * k, 0.6 * k, K.props.door({ label: "", open: 0.7 })) +
        at(x - rr * 0.52, y - rr * 0.86 + 8 * k, 1.0 * k, K.props.headstone({ text: "" })) + line;
    };
    const others = [[290, 330, 92, C.rust], [520, 860, 74, C.slate], [1530, 270, 84, C.orange], [1680, 720, 104, C.tan], [1250, 940, 62, C.yellow]].map(([x, y, rr, col]) => planet(x, y, rr, col)).join("");
    // Earth (r 230) centered at (960, 640); on its top a hill, the VOTE door, the Reaper and the bowing line
    const E = [960, 660], ER = 230;
    const earth = at(E[0], E[1] + ER, 1, K.props.earthGlobe({ r: ER }));
    const hill = `<path d="M${E[0] - 200},${E[1] - ER * 0.5} Q${E[0] - 60},${E[1] - ER - 90} ${E[0] + 120},${E[1] - ER - 34} Q${E[0] + 210},${E[1] - ER - 10} ${E[0] + 205},${E[1] - ER * 0.45} A${ER},${ER} 0 0,0 ${E[0] - 200},${E[1] - ER * 0.5} Z" fill="#9DB25A" stroke="${ink}" stroke-width="4"/>`;
    const top = E[1] - ER - 40;
    const door = at(E[0] + 110, top + 6, 0.62, K.props.door({ label: "VOTE", open: 0.7 }));
    const reap = at(E[0] + 178, top + 6 - 62, 0.62, `<g transform="rotate(-14 0 100)">${reaper(K, C, {})}</g>`);
    const k = 0.5;
    let line = at(E[0] + 46, top + 2 - 50, k, K.person(copy(OLDWOMAN, { look: "right", arms: bow, build: copy(OLDWOMAN.build, { hunch }) })));
    line += at(E[0] - 2, top + 8 - 50, k, K.person(copy(CLERK, { look: "right", arms: bow, build: { hunch } })));
    for (let i = 0; i < 4; i++) line += at(E[0] - 52 - i * 46, top + 26 + i * 24 - 50, k, K.person({ outfit: i % 2 ? "dress" : "suit", hair: i % 2, tone: (i + 2) % 4, color: i % 4, seed: 60 + i, look: "right", arms: bow, build: { hunch } }));
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + stars + others + earth + hill + door + reap + line;
    return { svg, alt: "A navy night sky full of mustard stars: in the middle a small Earth with a green hill on top, where the Grim Reaper holds a door marked VOTE open while a line of humans led by the old woman and the clerk bows, each waving the one behind ahead; round it five little planets have gone dark, each with a tiny headstone and a tiny line of skeletons still bowing at its door." };
  },

  "everyone-realizes"(H, fid) {
    const { K, C } = H;
    // after "unrecognizable.": the factories are hospitals, the missiles bursting as fireworks over them; every bubble
    // open; the Weapons Maker in his bucket holding the empty bonnet his missile left behind
    const svg = view(230, -340, 0.98, townSquare(K, C, "realize"));
    return { svg, alt: "The town square transformed: the three war factories have popped up as hospitals and their missiles burst as fireworks overhead; every thought bubble in the crowd is open, each holding a tiny smiling Earth and a stack of green bills, a price tag reading +$518,879 swinging over the Weapons Maker's; the skeleton's jaw lies on the ground; the Weapons Maker, still wearing the paint bucket, holds the empty baby bonnet his missile left behind; on the wall under SUPP, the calendar's page is stamped DONE." };
  },

  "you-are-everyone"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "everyone.": from the stage; tiers of seats up to the floodlights, every seat holding a YES sign; the clerk
    // at the front by the YES console, the dunce cap blowing off his head
    const BG = "#2B3550";
    let seats = "";
    for (let row = 0; row < 9; row++) {
      const y = 170 + row * 64, sc = 0.24 + row * 0.035, step = 64 + row * 8;
      const tone = [C.rust, C.slate, C.tan][row % 3];
      seats += `<rect x="-20" y="${y + 18}" width="1960" height="${52 + row * 2}" fill="${K.mix(tone, "#E9D7A8", 0.25)}" stroke="${ink}" stroke-width="2"/>`;
      for (let x = (row % 2) * (step / 2) - 20; x < 1960; x += step) {
        const i = Math.round(x / step) + row * 31;
        const skin = ["#F1D6B5", "#D9A877", "#A8714B", "#6F4A31"][i % 4], cloth = [C.navy, C.rust, C.orange, C.slate][(i * 7) % 4];
        seats += `<g transform="translate(${f(x)},${f(y + 30)}) scale(${f(sc)})">` +
          `<path d="M-32,60 L-26,6 L-10,-2 H10 L26,6 L32,60 Z" fill="${cloth}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
          `<path d="M-14,-6 L-16,-28 L-6,-42 L10,-40 L18,-26 L26,-22 L16,-16 L12,-4 Z" fill="${skin}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
          `<path d="M24,0 L36,-110" stroke="${ink}" stroke-width="8"/>` +
          `<rect x="0" y="-190" width="78" height="56" fill="${C.cream}" stroke="${ink}" stroke-width="6"/>` + osw(39, -146, 40, "YES", C.navy) + "</g>";
      }
    }
    const towers = [140, 620, 1300, 1780].map((x) => `<path d="M${x - 90},90 L${x - 300},760 H${x + 300} L${x + 90},90 Z" fill="#FFF6D8" opacity="0.13"/>` +
      `<rect x="${x - 4}" y="0" width="8" height="40" fill="${C.slate}"/><rect x="${x - 90}" y="22" width="180" height="76" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>` +
      [0, 1, 2, 3].map((j) => `<circle cx="${x - 66 + j * 44}" cy="60" r="18" fill="#FFF6D8" stroke="${ink}" stroke-width="3"/>`).join("") +
      [-1, 1].map((s) => `<path d="M${x + s * 100},40 l${s * 30},-20 M${x + s * 104},66 l${s * 36},0" stroke="#FFF6D8" stroke-width="5" stroke-linecap="round"/>`).join("")).join("");
    const stage = `<rect x="-20" y="860" width="1960" height="240" fill="${C.slate}" stroke="${ink}" stroke-width="5"/><path d="M-20,872 H1940" stroke="${C.orange}" stroke-width="5"/>`;
    const clerk = copy(CLERK, { mood: "eager", look: "right", arms: [[-150, -170], [36, 70]] });
    const man = stand(K, clerk, 900, 1000, 2.7);
    const R = K.rig(clerk);
    const sign = at(900 + R.hand[0][0] * 2.7, 1000 - 270 + R.hand[0][1] * 2.7, 2.7, `<path d="M0,0 L-4,-58" stroke="${ink}" stroke-width="5"/><rect x="-44" y="-100" width="80" height="48" fill="${C.cream}" stroke="${ink}" stroke-width="4"/>` + osw(-4, -63, 32, "YES", C.navy));
    const cons = at(1180, 1000, 2.7, K.props.yesButton({ label: "YES", sub: "TREATY" }));
    const cap = at(1070, 400, 1.7, `<path d="M-28,0 L0,-88 L28,0 Z" fill="${C.cream}" stroke="${ink}" stroke-width="4"/><path d="M-30,0 h60" stroke="${ink}" stroke-width="5"/><circle cx="0" cy="-90" r="6" fill="${C.orange}" stroke="${ink}" stroke-width="2.4"/>`, 40) + speed(C, 1020, 470, -50, 46, 3, 16, 4);
    const svg = `<rect width="1920" height="1080" fill="${BG}"/>` + towers + seats + stage + man + sign + cons + cap;
    return { svg, alt: "A huge stadium seen from its stage with every floodlight on: tier after tier of humans, every one holding up the same small YES sign; at the front of the stage the beanpole clerk holds up his own YES sign beside the YES console, and the dunce cap flies off his head." };
  },

  "why-three-point-five"(H, fid) {
    const { K, C } = H, S = K.STUDIO;
    // after "percent?": the question mark sprung out of the dial on its coil spring, Wishonia raising a brow
    const svg = push(S, 1.04, H.host("skeptical-smile", "hands-hips", lecternDial(K, C, { spring: "?", bob: true })));
    return { svg, alt: "Wishonia at her lectern raises a brow at the camera, hands on her hips; on the right end of the lectern a question mark has sprung out of the top of the 3.5% dial on a coil spring and bobs there." };
  },

  "chenoweth-shelf"(H, fid) {
    const { K, C } = H, ink = C.line;
    // after "purpose.": the end of the shelf: the last books stamped WON, the brass bookend reading ERICA CHENOWETH
    // and FAILURES: 0, the dusty LATER drawer under the shelf, its label yellowed, a tumbleweed on the floor
    const WALLC = "#E3C88F", FLOOR = "#9A6A3E", SHELF_Y = 470;
    const spines = [C.rust, C.navy, C.slate, C.tan, C.orange, C.rust, C.navy, C.slate];
    const years = ["1963", "1974", "1986", "1989", "1998", "2000", "2004", "2011"];
    let books = "", x = 40;
    spines.forEach((col, i) => {
      const w = 96 + (i % 3) * 14, h = 300 + (i % 4) * 26, light = col === C.tan || col === C.orange;
      books += `<rect x="${x}" y="${SHELF_Y - h}" width="${w}" height="${h}" fill="${col}" stroke="${ink}" stroke-width="5"/>` +
        `<path d="M${x + 8},${SHELF_Y - h + 22} h${w - 16} M${x + 8},${SHELF_Y - 26} h${w - 16}" stroke="${light ? ink : C.cream}" stroke-width="3" opacity="0.6"/>` +
        osw(x + w / 2, SHELF_Y - h + 66, 30, years[i], light ? ink : C.cream) +
        at(x + w / 2, SHELF_Y - h * 0.3, 0.72, K.props.stampMark({ text: "WON", angle: -8, fontSize: 34 }));
      x += w + 6;
    });
    const shelf = `<rect x="0" y="${SHELF_Y}" width="1920" height="26" fill="#7A4F2C" stroke="${ink}" stroke-width="5"/>` +
      [220, 1700].map((bx) => `<path d="M${bx},${SHELF_Y + 26} v70 l60,-70" fill="none" stroke="${ink}" stroke-width="10"/><path d="M${bx},${SHELF_Y + 26} v70 l60,-70" fill="none" stroke="${C.slate}" stroke-width="5"/>`).join("");
    // the bookend: a brass slab with a stepped top, the nameplate and the counter window on its face
    const bx = x + 4, bw = 380;
    const bookend = `<path d="M${bx},${SHELF_Y} V${SHELF_Y - 360} H${bx + 40} V${SHELF_Y - 384} H${bx + bw - 40} V${SHELF_Y - 360} H${bx + bw} V${SHELF_Y} Z" fill="${C.yellow}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
      `<path d="M${bx + bw - 14},${SHELF_Y - 350} V${SHELF_Y - 10}" stroke="${C.orange}" stroke-width="7"/>` +
      `<rect x="${bx + 24}" y="${SHELF_Y - 330}" width="${bw - 48}" height="76" rx="6" fill="#B8862E" stroke="${ink}" stroke-width="5"/>` + osw(bx + bw / 2, SHELF_Y - 279, 34, "ERICA CHENOWETH", "#FBF2D4") +
      `<rect x="${bx + 40}" y="${SHELF_Y - 226}" width="${bw - 80}" height="150" rx="8" fill="${C.navy}" stroke="${ink}" stroke-width="5"/>` +
      osw(bx + bw / 2, SHELF_Y - 180, 34, "FAILURES:", C.cream) + num(bx + bw / 2, SHELF_Y - 100, 76, "0", C.yellow);
    // the drawer hung under the shelf, its LATER label yellowed and curling at one corner, a drift of dust on top
    const dx = 1180, dy = SHELF_Y + 26, dw = 340, dh = 170;
    const drawer = `<rect x="${dx}" y="${dy}" width="${dw}" height="${dh}" fill="#A9743F" stroke="${ink}" stroke-width="5"/>` +
      `<rect x="${dx + 104}" y="${dy + 38}" width="132" height="50" fill="#E2C77E" stroke="${ink}" stroke-width="3.4"/>` + osw(dx + 170, dy + 76, 34, "LATER", C.navy) +
      `<path d="M${dx + 236},${dy + 38} l-22,0 q6,10 22,16 Z" fill="#C9A85C" stroke="${ink}" stroke-width="2.4"/>` +
      `<rect x="${dx + 136}" y="${dy + 112}" width="68" height="18" rx="7" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/>` +
      `<path d="M${dx},${dy + 6} q30,-4 60,4 q40,-6 80,2 q50,-8 110,2 q40,-2 90,0 v22 q-60,-10 -120,0 q-60,-12 -120,2 q-60,-12 -100,0 Z" fill="#D6CBB0" opacity="0.9"/>` +
      `<path d="M${dx + 12},${dy + 150} q40,-8 90,0 q60,-6 120,0 q50,-4 106,0" fill="none" stroke="#D6CBB0" stroke-width="5" opacity="0.8"/>`;
    // the tumbleweed rolling past on the floor
    const tw = (cx, cy, r) => {
      let d = "";
      for (let i = 0; i < 11; i++) {
        const a = i * 2.3;
        d += `M${f(cx + r * Math.cos(a))},${f(cy + r * Math.sin(a))} Q${f(cx + r * 0.3 * Math.cos(a + 1.7))},${f(cy + r * 0.3 * Math.sin(a + 1.7))} ${f(cx + r * 0.92 * Math.cos(a + 2.9))},${f(cy + r * 0.92 * Math.sin(a + 2.9))} `;
      }
      return `<path d="${d}" fill="none" stroke="#7A5A2E" stroke-width="5" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#C9A866" stroke-width="2" stroke-linecap="round" transform="rotate(30 ${cx} ${cy})"/>` + speed(C, cx - r - 16, cy - 6, 80, 0, 3, 22, 3.4);
    };
    const floor = `<rect x="0" y="900" width="1920" height="180" fill="${FLOOR}"/><path d="M0,900 H1920" stroke="${ink}" stroke-width="5"/>` + [0, 1, 2, 3, 4, 5, 6].map((i) => `<path d="M${i * 300 + 60},900 v180" stroke="${ink}" stroke-width="2" opacity="0.3"/>`).join("");
    const svg = `<rect width="1920" height="1080" fill="${WALLC}"/>` + floor + books + shelf + bookend + drawer + tw(760, 840, 64);
    return { svg, alt: "The end of a long library shelf of history books, every spine stamped WON in red; a brass bookend with the nameplate ERICA CHENOWETH and a counter reading FAILURES: 0; under the shelf a dusty wooden drawer labeled LATER, the label yellowed and curling, while a tumbleweed rolls past on the floor." };
  },

  "280-million"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "twerk.": pulled back over the plain: the small field of open bubbles on the left, the field ten times
    // bigger of TV sets on the right back to the horizon, every screen showing the tiny twerker, the sets wiggling
    // in step and the ground quaking, 280,000,000 in the sky
    const HZ = 430;
    const tv = (s, rot) => at(0, 0, s, K.props.tvSet({}).replace("<!--tv-screen-->", twerker(C, -23, -52, 1.05)), rot);
    let tvs = "";
    const rows = [];
    for (let d = 470; d >= 24; d *= 0.8) rows.push(d);
    rows.reverse().forEach((dk, ri) => {
      const base = HZ + dk, sc = dk / 470, step = 200 * sc;
      for (let x = 780; x < 1960 + step; x += step) {
        const i = Math.round(x / step) + ri;
        tvs += `<g transform="translate(${f(x)},${f(base)})">${tv(sc * 1.05, i % 2 ? -7 : 7)}</g>`;
      }
    });
    let bubs = "";
    const rr = [];
    for (let d = 470; d >= 40; d *= 0.8) rr.push(d);
    rr.reverse().forEach((dk, ri) => {
      const base = HZ + dk, sc = dk / 470, step = 150 * sc;
      for (let x = 110; x < 640; x += step) bubs += at(x, base - 60 * sc - 8 - (ri % 2 ? 6 * sc : 0), sc * 0.95, bubble(K, C, { open: true }));
    });
    const ground = `<rect width="1920" height="${HZ}" fill="${SKY}"/><rect y="${HZ}" width="1920" height="${1080 - HZ}" fill="${FIELD}"/><path d="M0,${HZ} H1920" stroke="#8E7A55" stroke-width="3" opacity="0.6"/>`;
    // quake: the ground's edge jitters, shake marks under the front sets and the small field
    const quake = [820, 1080, 1340, 1600, 1860, 160, 420].map((x) => `<path d="M${x - 40},1040 h80 M${x - 26},1056 h52" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`).join("") +
      `<path d="M0,${HZ} l60,-6 l60,8 l60,-7 l60,6 l60,-5 l60,7 l60,-6 l60,6 l60,-7 l60,6 l60,-6 l60,7 l60,-6 l60,6 l60,-6 l60,7 l60,-6 l60,6 l60,-5 l60,6 l60,-6 l60,6 l60,-7 l60,6 l60,-6 l60,6 l60,-5 l60,6 l60,-6 l60,6 l60,-6" fill="none" stroke="#8E7A55" stroke-width="5"/>`;
    const svg = ground + tvs + bubs + quake + num(70, 330, 118, "280,000,000", C.navy, "start", `letter-spacing="2"`);
    return { svg, alt: "A plain under a cream sky: on the left a small field packed with tiny open thought bubbles, each with its YES button, under 280,000,000 in the sky; on the right a field ten times bigger of tiny 1950s TV sets running back to the horizon, every screen showing the same tiny human wiggling its hips and every set wiggling with it, the ground quaking." };
  },

  "you-can-get"(H, fid) {
    const { K, C } = H, S = K.STUDIO, ink = C.line;
    // on "yes": the TV on the left end of the lectern, its tiny twerker bumping the YES button with his hip, the cap
    // down; the dial on the right end with its exclamation mark; Wishonia presenting it with open palms
    const screen = twerker(C, -42, -50, 1.1) + at(-4, -54, 0.4, K.props.yesButton({ label: "YES" }).replace('class="yes-cap"', 'class="yes-cap" transform="translate(0,9)"')) +
      `<path d="M-26,-74 l7,-7 M-24,-60 l9,-2" stroke="${C.cream}" stroke-width="2.6" stroke-linecap="round"/>`;
    const svg = push(S, 1.03, H.host("happy-smile", "open-palms", lecternTV(K, C, 556, S.top, 1.45, screen) + lecternDial(K, C, { spring: "!" })));
    return { svg, alt: "Wishonia presents with open palms at her lectern; on its left end stands a little 1950s TV set where the tiny wiggling human bumps a YES button with his hip and presses it; on its right end the 3.5% dial's spring now holds an exclamation mark." };
  },

  "referral-pyramid"(H, fid) {
    const { K, C } = H, ink = C.line;
    // on "dying": tilted up to the hilltop: a human pyramid of Loud Humans, each tier standing on the shoulders of
    // the one below (132 apart at scale 1.05), its top level with the clifftop; every megaphone blasting at the
    // summit, the Reaper blown off his rock, scythe and clipboard flying
    const sky = `<rect width="1920" height="1080" fill="${SKY}"/>`;
    const TOP = 430;
    const cliff = `<path d="M1180,1100 L1205,640 L1250,${TOP + 10} L1940,${TOP - 10} L1940,1100 Z" fill="#B47E52" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M1236,700 l60,-40 M1300,880 l90,-30 M1520,600 l120,0" stroke="${ink}" stroke-width="3" opacity="0.3"/>` +
      `<path d="M1430,${TOP} l34,-54 h96 l30,54 Z" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>`;
    const ground = `<rect y="1000" width="1920" height="80" fill="${FIELD}"/><path d="M0,1000 H1180" stroke="${ink}" stroke-width="3" opacity="0.5"/>`;
    const lh = K.CAST.loudHuman, k = 1.0, step = 132 * k, cx = 840;
    let pyr = "", rings = "";
    for (let ti = 0; ti < 5; ti++) {
      const n = 5 - ti, feet = 1010 - ti * step;
      for (let i = 0; i < n; i++) {
        const x = cx - (n - 1) * 56 * k + i * 112 * k;
        const arms = ti === 4 ? [[-150, -170], [150, 172]] : [[-150, -168], [150, 168]];
        const o = copy(lh, { tone: (i + ti) % 4, color: (i * 2 + ti + 1) % 4, look: "right", arms, build: copy(lh.build, { legs: 1 }) });
        pyr += at(x, feet - 100 * k, k, K.person(o));
        // blast rings out of the megaphone mouth, aimed up at the summit
        const mx = x + 30 * k, my = feet - 100 * k - 56 * k;
        rings += `<g transform="rotate(-18 ${f(mx)} ${f(my)})">` + [0, 1, 2].map((j) => `<path d="M${f(mx + 16 + j * 16)},${f(my - 16 - j * 7)} q${10 + j * 4},${16 + j * 7} 0,${32 + j * 14}" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`).join("") + "</g>";
      }
    }
    const reap = at(1600, 190, 1.05, reaper(K, C, { noScythe: true }), 64) + speed(C, 1480, 250, -120, -10, 4, 22, 4);
    const flyScythe = at(1350, 140, 0.95, scythe(K, C), -130);
    const board = at(1820, 330, 0.8, tallyBoard(K, C), 30);
    const svg = sky + ground + cliff + pyr + rings + reap + flyScythe + board;
    return { svg, alt: "A human pyramid of Loud Humans with megaphones for heads, each tier standing on the shoulders of the one below, reaches the top of a cliff; every megaphone blasts at the summit, and the Grim Reaper is blown head over heels off his rock, his scythe and tally clipboard flying." };
  },

  "pyramid-ends"(H, fid) {
    const { K, C } = H, S = K.STUDIO;
    // on "diseases.": the Reaper's tally clipboard landed upright in the middle of the reading top, a loose tally
    // mark still fluttering down; the TV (ears up) and the dial with its exclamation mark on the two ends
    const clip = at(760, S.top + 4, 1.25, tallyBoard(K, C, 17), -6);
    const flutter = `<path d="M1160,330 l34,-8" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/><path d="M1136,306 q12,-14 28,-6 M1206,346 q12,-12 26,-4" fill="none" stroke="${C.line}" stroke-width="2.6"/>` +
      `<path d="M716,742 h-30 M806,742 h30" stroke="${C.line}" stroke-width="4" stroke-linecap="round"/>`;
    const svg = push(S, 1.06, H.host("smirk-smile", "idle", lecternTV(K, C, 556, S.top, 1.45, "", "up") + lecternDial(K, C, { spring: "!" }) + clip + flutter));
    return { svg, alt: "Wishonia smirks at the camera from her lectern; the Grim Reaper's tally clipboard has just dropped onto the middle of the lectern and landed standing up, a loose tally mark still fluttering down, with the little TV on its left end and the 3.5% dial with its exclamation mark on its right." };
  },
};
