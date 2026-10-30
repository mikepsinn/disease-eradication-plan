// Sketches for storyboards/part-09-unexplored-therapeutic-frontier.md: each scene's key moment on a 1920 x 1080 frame,
// drawn with the production art (H.K: kit.js, film.js and the props library), in the film look of Part 2:
// the period title card, host shots at the lectern (H.host) and plate framings as the camera sees them.

const f1 = (n) => (+n).toFixed(1);
const GROUND = "#C8B07B", GROUND_D = "#B89D68", EDGE = "#B09363";
const BRICK = "#904B2E", MORTAR = "#74391F", WHITE = "#FBF6E6", BEARD = "#ECE7DA";

// A person standing with its feet on (x, feetY), k times person size; o: KIT.person options; extra: markup in person units.
function man(H, o, x, feetY, k, extra = "") {
  return H.at(x, feetY - 100 * k, k, H.K.person(o) + extra);
}
function copy(a, b) { return Object.assign({}, a, b); }

// The explorer's pith helmet, its brim centered on (cx, by): a tall khaki dome over a wide brim that dips front and back.
function helmet(C, cx, by, s = 1, rot = 0) {
  return `<g transform="translate(${f1(cx)},${f1(by)}) rotate(${rot}) scale(${s})">` +
    `<path d="M-21,2 C-23,-22 -9,-31 0,-31 C9,-31 23,-22 21,2 Z" fill="#E2CB92" stroke="${C.line}" stroke-width="2.6" stroke-linejoin="round"/>` +
    `<path d="M6,-28 C14,-24 19,-14 19,0" fill="none" stroke="#C9AE6E" stroke-width="5"/>` +
    `<path d="M-21,-3 C-8,0 8,0 21,-3 L21,2 C8,5 -8,5 -21,2 Z" fill="${C.rust}" stroke="${C.line}" stroke-width="1.8"/>` +
    `<path d="M-36,4 C-20,-2 20,-2 36,4 C24,13 -24,13 -36,4 Z" fill="#E2CB92" stroke="${C.line}" stroke-width="2.6" stroke-linejoin="round"/>` +
    `<circle cx="0" cy="-31" r="3" fill="${C.tan}" stroke="${C.line}" stroke-width="1.6"/></g>`;
}
// A tapered limb through points pts (2 or 3), widths ws at each point, as one polygon; plus a claw at the end.
function limb(pts, ws) {
  const nrm = pts.map((p, i) => {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1;
    return [-dy / l, dx / l];
  });
  const L = pts.map((p, i) => [p[0] + nrm[i][0] * ws[i] / 2, p[1] + nrm[i][1] * ws[i] / 2]);
  const R = pts.map((p, i) => [p[0] - nrm[i][0] * ws[i] / 2, p[1] - nrm[i][1] * ws[i] / 2]).reverse();
  return "M" + L.concat(R).map((q) => f1(q[0]) + "," + f1(q[1])).join(" L") + " Z";
}
// A tag on a string, hanging down and to the left of a knot at (0, 0); its grommet end is on the right.
function hangTag(H, text, size = 22) {
  const { C } = H;
  const w = 34 + text.length * size * 0.5, h = size * 1.5, x1 = -10, y1 = 40;
  const card = `M0,${-h / 2 + 7} L-8,${-h / 2} H${-w} V${h / 2} H-8 L0,${h / 2 - 7} Z`;
  return `<path d="M0,0 Q-8,20 ${x1},${y1}" fill="none" stroke="${C.line}" stroke-width="2.4"/>` +
    `<g transform="translate(${x1},${y1}) rotate(-16)"><path d="${card}" fill="${WHITE}" stroke="${C.line}" stroke-width="3" stroke-linejoin="round"/>` +
    `<circle cx="-7" cy="0" r="4" fill="${C.yellow}" stroke="${C.line}" stroke-width="1.6"/>` +
    H.label(-w / 2 - 6, size * 0.36, size, text, "middle", C.line) + "</g>";
}

// A disease on a leash, the queue's own thing: a knee-high KIT.props.diseaseBlob with a rust collar, sitting at its
// human's heel, its leash running up to his hand. In person units (KIT.person's feet on y 100): hand, the hand that
// holds the leash ([x, y], from KIT.rig); x, the blob's middle on the ground; k, its size (0.3 is knee high); o, its
// diseaseBlob options; placard, text on a placard it holds up on a stick (its claws up).
export function leashed(H, hand, x, k = 0.3, o = {}, placard = "") {
  const { K, C } = H;
  const bo = Object.assign({ mood: "smug" }, o, placard ? { arms: "up" } : {});
  let inner = K.props.diseaseBlob(bo) + `<path d="M-74,-62 Q0,-40 74,-62" fill="none" stroke="${C.line}" stroke-width="15"/><path d="M-74,-62 Q0,-40 74,-62" fill="none" stroke="${C.rust}" stroke-width="9"/>` +
    `<circle cx="0" cy="-50" r="7" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/>`;
  if (placard) {
    const w = 56 + placard.length * 34;
    inner += `<path d="M88,-112 V-250" stroke="${C.tan}" stroke-width="10"/><path d="M88,-112 V-250" stroke="${C.line}" stroke-width="2" opacity="0.5"/>` +
      `<rect x="${88 - w / 2}" y="-340" width="${w}" height="96" rx="6" fill="${WHITE}" stroke="${C.line}" stroke-width="7"/>` +
      H.label(88, -268, 70, placard, "middle", C.line);
  }
  const cx = x, cy = 100 - 50 * k;
  const sag = Math.max(hand[1], cy) + 10;
  const leash = `<path d="M${f1(hand[0])},${f1(hand[1])} Q${f1((hand[0] + cx) / 2)},${f1(sag)} ${f1(cx)},${f1(cy)}" fill="none" stroke="${C.rust}" stroke-width="2.6"/>`;
  return H.at(x, 100, k, inner) + leash;
}

// A coffee mug, centered on its body, about 40 x 44.
function mug(C) {
  return `<path d="M14,-10 C30,-10 30,12 14,12" fill="none" stroke="${C.line}" stroke-width="9"/><path d="M14,-10 C30,-10 30,12 14,12" fill="none" stroke="${C.yellow}" stroke-width="4"/>` +
    `<path d="M-18,-22 H16 L14,20 H-16 Z" fill="${C.yellow}" stroke="${C.line}" stroke-width="3.2" stroke-linejoin="round"/>` +
    `<path d="M-18,-22 H16" stroke="${C.line}" stroke-width="5"/><path d="M-14,-6 H12" stroke="${C.rust}" stroke-width="4"/>` +
    `<path d="M-6,-30 q-6,-8 0,-16 q6,-8 0,-16 M6,-30 q-6,-8 0,-16" fill="none" stroke="${C.cream}" stroke-width="3" stroke-linecap="round" opacity="0.9"/>`;
}

// The brick wall the window is cut into, filling x0..x1, y0..y1 (canvas px), bricks bw x bh.
function brickWall(x0, y0, x1, y1, bw = 120, bh = 46) {
  let lines = "";
  for (let y = y0 + bh, r = 0; y < y1; y += bh, r++) {
    lines += `<path d="M${x0},${y} H${x1}" stroke="${MORTAR}" stroke-width="3"/>`;
    for (let x = x0 + (r % 2 ? bw / 2 : 0); x < x1; x += bw) lines += `<path d="M${x},${y - bh} V${y}" stroke="${MORTAR}" stroke-width="3"/>`;
  }
  return `<rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" fill="${BRICK}"/>` + lines;
}

// The ticket window: an opening x0..x1, y0..y1 in the wall, a counter under it, and the roll-down shutter, down
// by `down` (0 open, 1 shut). inside: markup seen through the opening (clipped).
function windowBox(H, id, x0, y0, x1, y1, down, inside = "") {
  const { C } = H;
  const sh = (y1 - y0) * down;
  let slats = "";
  for (let y = y0 + 18; y < y0 + sh - 4; y += 22) slats += `<path d="M${x0 + 4},${y} H${x1 - 4}" stroke="${C.slate}" stroke-width="3"/>`;
  return `<defs><clipPath id="${id}-win"><rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}"/></clipPath></defs>` +
    `<rect x="${x0 - 26}" y="${y0 - 26}" width="${x1 - x0 + 52}" height="${y1 - y0 + 26}" fill="${C.tan}" stroke="${C.line}" stroke-width="5"/>` +
    `<rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" fill="${C.slate}" stroke="${C.line}" stroke-width="5"/>` +
    `<g clip-path="url(#${id}-win)">${inside}</g>` +
    (down > 0 ? `<rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${sh}" fill="${C.peri}" stroke="${C.line}" stroke-width="4"/>${slats}` +
      `<rect x="${x0}" y="${y0 + sh - 14}" width="${x1 - x0}" height="14" fill="${C.slate}" stroke="${C.line}" stroke-width="3"/>` : "") +
    `<rect x="${x0 - 40}" y="${y1}" width="${x1 - x0 + 80}" height="22" fill="${C.tan}" stroke="${C.line}" stroke-width="5"/>` +
    `<path d="M${x0 - 30},${y1 + 22} L${x0 - 10},${y1 + 52} M${x1 + 30},${y1 + 22} L${x1 + 10},${y1 + 52}" stroke="${C.line}" stroke-width="6"/>`;
}

// The window's sign: plain lettering on a cream board, centered on (cx, cy).
function fdaSign(H, cx, cy, size = 40) {
  const { C } = H;
  const text = "FOOD AND DRUG ADMINISTRATION", w = text.length * size * 0.5 + 70, h = size * 1.7;
  return `<rect x="${cx - w / 2}" y="${cy - h / 2}" width="${w}" height="${h}" rx="4" fill="${C.cream}" stroke="${C.line}" stroke-width="5"/>` +
    `<rect x="${cx - w / 2 + 9}" y="${cy - h / 2 + 9}" width="${w - 18}" height="${h - 18}" fill="none" stroke="${C.orange}" stroke-width="2"/>` +
    H.label(cx, cy + size * 0.36, size, text, "middle", C.line);
}

// The wait sign: an enamel sign on two chains, centered on (cx, top). top: its top line; wheels: the digits in its
// three wheels (null: spinning blur), unit: after the wheels.
function waitSign(H, cx, top, s, topLine, wheels, unit) {
  const { C } = H;
  const w = 560, h = 250;
  let out = `<path d="M${-w / 2 + 70},-120 L${-w / 2 + 70},0 M${w / 2 - 70},-120 L${w / 2 - 70},0" stroke="${C.line}" stroke-width="5" stroke-dasharray="10 5"/>` +
    `<rect x="${-w / 2 + 6}" y="8" width="${w}" height="${h}" rx="16" fill="${C.line}"/>` +
    `<rect x="${-w / 2}" y="0" width="${w}" height="${h}" rx="16" fill="${C.cream}" stroke="${C.line}" stroke-width="6"/>` +
    `<rect x="${-w / 2 + 14}" y="14" width="${w - 28}" height="86" rx="8" fill="${C.navy}"/>` +
    H.label(0, 76, 58, topLine, "middle", C.cream) +
    H.label(0, 150, 34, "WAIT TIME FROM HERE:", "middle", C.line);
  const dig = wheels ? wheels.split("") : [null, null, null];
  dig.forEach((d, i) => {
    const x = -170 + i * 70;
    out += `<rect x="${x}" y="170" width="60" height="68" rx="6" fill="${C.slate}" stroke="${C.line}" stroke-width="4"/>` +
      (d ? `<text x="${x + 30}" y="226" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="54" fill="${C.yellow}">${d}</text>`
        : `<path d="M${x + 10},186 H${x + 50} M${x + 8},204 H${x + 52} M${x + 10},222 H${x + 50}" stroke="${C.yellow}" stroke-width="5" opacity="0.7"/>`) +
      `<path d="M${x},204 H${x + 60}" stroke="#111" stroke-width="2"/>`;
  });
  out += H.label(70, 226, 50, unit, "start", C.line);
  return H.at(cx, top, s, out);
}

// A shelf of pill bottles, x0..x1 on the plank at y (canvas px), bottles at size k; tag: "NEVER TESTED FOR THIS" tags.
function shelf(H, x0, x1, y, k, tags, checkAt = -1) {
  const { K, C } = H;
  let out = `<rect x="${x0 - 20}" y="${y}" width="${x1 - x0 + 40}" height="${16 * k + 6}" fill="${C.tan}" stroke="${C.line}" stroke-width="4"/>`;
  const step = 70 * k;
  let i = 0;
  for (let x = x0 + step / 2; x < x1; x += step, i++) {
    out += H.at(x, y, k, K.props.pillBottle({ label: "" }));
    if (tags) {
      const tw = 128, th = 50;
      out += H.at(x + 2, y - 40 * k, k * 0.42, i === checkAt
        ? `<rect x="${-th / 2}" y="${-th / 2}" width="${th}" height="${th}" rx="4" fill="${WHITE}" stroke="${C.line}" stroke-width="4"/>` + K.tick(-th / 2 + 4, -th / 2 + 4, th - 8, C.med).replace('stroke-dashoffset="1"', 'stroke-dashoffset="0"')
        : `<rect x="${-tw / 2}" y="${-th / 2}" width="${tw}" height="${th}" rx="4" fill="${WHITE}" stroke="${C.line}" stroke-width="4"/>` +
          H.label(0, -4, 17, "NEVER TESTED", "middle", C.war) + H.label(0, 16, 17, "FOR THIS", "middle", C.war), (i % 3) - 1);
    }
  }
  return out;
}

// A cobweb strung from point a (the knuckles) to the shutter around point b, canvas px.
function cobweb(a, b) {
  const spokes = [[0, 0], [70, -60], [110, 10], [60, 80], [-20, 70], a.map((v, i) => v - b[i])];
  let out = spokes.map(([dx, dy]) => `<path d="M${b[0]},${b[1]} L${b[0] + dx},${b[1] + dy}" stroke="${WHITE}" stroke-width="2"/>`).join("");
  for (const r of [0.35, 0.65, 0.9]) {
    out += `<path d="M${spokes.slice(1).map(([dx, dy]) => `${f1(b[0] + dx * r)},${f1(b[1] + dy * r)}`).join(" L")}" fill="none" stroke="${WHITE}" stroke-width="1.6"/>`;
  }
  return `<g opacity="0.9">${out}</g>`;
}
function spider(C, x, y, s = 1) {
  const legs = [-1, 1].map((d) => [0, 1, 2, 3].map((i) => `<path d="M0,0 l${d * 10},${-6 + i * 4} l${d * 6},${6 + i * 2}" fill="none" stroke="${C.line}" stroke-width="2.4"/>`).join("")).join("");
  return `<g transform="translate(${x},${y}) scale(${s})"><path d="M0,-6 V-90" stroke="${WHITE}" stroke-width="1.6"/>${legs}<circle cx="0" cy="2" r="8" fill="${C.line}"/><circle cx="0" cy="-7" r="5" fill="${C.line}"/><circle cx="-2" cy="-8" r="1.3" fill="${C.cream}"/><circle cx="2" cy="-8" r="1.3" fill="${C.cream}"/></g>`;
}

// A 1950s convertible facing right, wheels on y 0, about 420 x 130; the driver is drawn separately, behind its door.
function car(C) {
  const body = `<path d="M-205,-34 L-196,-70 L-120,-76 L-70,-96 L40,-96 L80,-76 L190,-70 L210,-40 L205,-14 L-205,-14 Z" fill="${C.cyan}" stroke="${C.line}" stroke-width="5" stroke-linejoin="round"/>` +
    `<path d="M-205,-34 L-226,-74 L-196,-70" fill="${C.cyan}" stroke="${C.line}" stroke-width="5" stroke-linejoin="round"/>` +
    `<path d="M-190,-50 H196" stroke="${C.cream}" stroke-width="6"/><path d="M-190,-50 H196" stroke="${C.line}" stroke-width="1.6"/>` +
    `<rect x="-214" y="-22" width="434" height="14" rx="6" fill="#D8D5CB" stroke="${C.line}" stroke-width="4"/>` +
    `<circle cx="196" cy="-58" r="10" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/>` +
    `<path d="M40,-96 L60,-128 L66,-128 L50,-96" fill="#BFD6D8" stroke="${C.line}" stroke-width="3" opacity="0.9"/>`;
  const wheel = (x) => `<circle cx="${x}" cy="-8" r="34" fill="${C.ink}" stroke="${C.line}" stroke-width="4"/><circle cx="${x}" cy="-8" r="20" fill="${WHITE}" stroke="${C.line}" stroke-width="3"/><circle cx="${x}" cy="-8" r="8" fill="#B9B5AE" stroke="${C.line}" stroke-width="2"/>`;
  return body + wheel(-128) + wheel(130);
}

// The reader from Part 8 (falling-apart), copied from part-08-daily-deletion-event.sketch.mjs so the two parts draw
// him alike: his KIT.person options seated in his armchair, the armchair (in Part 8's plate units, the reader at
// scale 1.6 with his hips at y -58), his floor lamp and his red ticket bookmark.
const READER8 = { tone: 1, outfit: "shirt", color: 1, hair: 0, glasses: true, seed: 8 };
const SEATED8 = copy(READER8, { look: "left", build: { legPose: [[-88, -2], [-82, 4]] }, arms: [[-70, -128], [-58, -118]] });
function armchair8(H, front) {
  const { C } = H, ink = C.line;
  if (!front) {
    return `<path d="M-74,-56 L-82,-236 L-62,-272 L62,-272 L82,-236 L74,-56 Z" fill="${C.orange}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      `<path d="M-56,-236 L-52,-80 M56,-236 L52,-80" stroke="${C.rust}" stroke-width="3"/>` +
      `<path d="M-96,-66 L96,-66 L100,-34 L-100,-34 Z" fill="${C.rust}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>`;
  }
  const arm = (x, s) => `<path d="M${x},-124 L${x + s * 34},-128 L${x + s * 38},-30 L${x + s * 4},-28 Z" fill="${C.orange}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    `<path d="M${x - s * 4},-128 Q${x + s * 17},-150 ${x + s * 38},-128" fill="${C.orange}" stroke="${ink}" stroke-width="5"/>`;
  return arm(-112, 1) + arm(112, -1) + `<path d="M-100,-36 H100 V-14 H-100 Z" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>` +
    `<path d="M-92,-14 L-95,0 M92,-14 L95,0" stroke="${ink}" stroke-width="8" stroke-linecap="square"/>`;
}
function lamp8(H) {
  const { C } = H, ink = C.line;
  return `<path d="M-40,0 H40 L32,-14 H-32 Z" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><path d="M0,-14 V-400" stroke="${ink}" stroke-width="8"/><path d="M0,-14 V-400" stroke="#C9CED6" stroke-width="3.4"/>` +
    `<path d="M-58,-384 L-34,-474 H34 L58,-384 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/><path d="M-34,-474 H34" stroke="${C.orange}" stroke-width="4"/>`;
}
function ticket8(H) {
  const { C } = H, ink = C.line;
  return `<g transform="rotate(-12)"><path d="M-15,-8 H15 V8 H-15 l3,-2.7 l-3,-2.6 l3,-2.7 l-3,-2.7 l3,-2.6 Z" fill="${C.war}" stroke="${ink}" stroke-width="1.8" stroke-linejoin="miter"/>` +
    `<rect x="-7" y="-4" width="17" height="8" fill="none" stroke="${C.cream}" stroke-width="1.4"/><path d="M-4,0 h11" stroke="${C.cream}" stroke-width="1.6"/></g>`;
}

export default {
  "title-card"(H, id) {
    const { K, C } = H;
    const E = { rx: 200, ry: 62, k: 0.62 };
    const orbits = [0, 60, -60].map((a) => `<ellipse cx="960" cy="300" rx="${E.rx}" ry="${E.ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} 960 300)"/>`).join("");
    const bills = [[0, 2.2], [60, 4.1], [-60, 0.6]].map(([a, th]) => {
      const r = (a * Math.PI) / 180, ex = E.rx * Math.cos(th), ey = E.ry * Math.sin(th);
      return H.at(960 + ex * Math.cos(r) - ey * Math.sin(r), 294 + ex * Math.sin(r) + ey * Math.cos(r), E.k, K.money("war", 0));
    }).join("");
    const nucleus = `<circle cx="960" cy="300" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="951" cy="291" r="8" fill="${C.yellow}"/>`;
    const heading = H.big(960, 592, 70, "THE UNEXPLORED", "middle", C.cream) + H.big(960, 728, 136, "THERAPEUTIC", "middle", C.cream) + H.big(960, 866, 136, "FRONTIER", "middle", C.cream);
    // behind the words: the blob, five times her size, looming up over THERAPEUTIC, claws up, the explorer's helmet
    // just landing on its head
    const blob = H.at(1290, 772, 2.6, K.props.diseaseBlob({ mood: "grin", arms: "up", color: "peri" }) + helmet(C, 4, -136, 1.25, 12));
    // in front: the explorer running back flat out along the top of FRONTIER, arms up
    const SCI = K.castOpts("scientist", { look: "left", mood: "worried", arms: [[-150, -170], [150, 168]], build: { hs: 1.08, legs: 0.95, neck: 0.8, legPose: [[-38, -60], [30, 10]] } });
    const explorer = man(H, SCI, 740, 772, 1.0);
    const dash = [0, 1, 2].map((i) => `<path d="M${840 + i * 8},${700 + i * 22} h${70 - i * 14}" stroke="${C.cream}" stroke-width="5" stroke-linecap="round" opacity="0.85"/>`).join("");
    const dotted = `<path d="M1335,815 C1520,840 1700,800 1960,720" fill="none" stroke="${C.cream}" stroke-width="7" stroke-dasharray="3 16" stroke-linecap="round"/>`;
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus + blob + heading + dotted + dash + explorer;
    return { svg, alt: "The period title card: THE UNEXPLORED THERAPEUTIC FRONTIER in cream on navy under the atom. A tiny explorer runs back left along the top of FRONTIER, arms up, while a grinning disease blob five times her size looms up behind the heading, claws raised, her pith helmet landing on its head." };
  },

  "zero-treatments"(H, id) {
    const { K, C } = H;
    // the blob beside the lectern, the explorer's helmet on its head, raising Wishonia's mug to her in a toast
    const col = C.peri;
    const armL = `<path d="${limb([[-62, -56], [-104, -66], [-112, -108]], [18, 14, 11])}" fill="${col}" stroke="${C.line}" stroke-width="3.6" stroke-linejoin="miter"/>`;
    const armR = `<path d="${limb([[62, -52], [82, -26], [44, -30]], [18, 14, 10])}" fill="${col}" stroke="${C.line}" stroke-width="3.6" stroke-linejoin="miter"/>`;
    const cup = H.at(-118, -124, 0.85, mug(C), -10);
    const claw = `<path d="M-122,-114 l-6,-8 l6,2 l2,-8 l4,8 l4,-6 l0,10 Z" fill="${col}" stroke="${C.line}" stroke-width="2.4" stroke-linejoin="miter"/>`;
    const blob = H.at(1480, 1000, 3.0, K.props.diseaseBlob({ mood: "smug", color: "peri", arms: "none" }) + armR + armL + cup + helmet(C, 6, -136, 1.6, 6));
    const svg = H.host("sideeye-closed", "idle", blob);
    return { svg, alt: "Wishonia at her lectern side-eyes a smug disease blob beside it; the blob wears the explorer's pith helmet and raises her coffee mug to her in a toast." };
  },

  "back-soon"(H, id) {
    const { K, C } = H;
    const GY = 960; // the ground line in this framing
    const wall = brickWall(-20, -20, 1940, GY);
    const W0 = 930, W1 = 1500, WT = 360, WB = 650;
    const win = windowBox(H, id, W0, WT, W1, WB, 1);
    const sign = fdaSign(H, (W0 + W1) / 2, 250, 42);
    // the BACK SOON card on a nail, with a little clock face
    const card = `<path d="M1215,410 L1170,470 M1215,410 L1260,470" stroke="${C.line}" stroke-width="3"/><circle cx="1215" cy="408" r="6" fill="${C.line}"/>` +
      `<g transform="rotate(-4 1215 540)"><rect x="1105" y="468" width="220" height="140" rx="6" fill="${WHITE}" stroke="${C.line}" stroke-width="5"/>` +
      H.label(1215, 512, 34, "BACK SOON", "middle", C.war) +
      `<circle cx="1215" cy="564" r="34" fill="${C.cream}" stroke="${C.line}" stroke-width="4"/><path d="M1215,564 L1215,540 M1215,564 L1236,576" stroke="${C.line}" stroke-width="4" stroke-linecap="round"/></g>`;
    // the knocker: fedora, white hair and a beard to the ground, chest light red, his disease on its leash at his heel
    const K0 = { tone: 1, outfit: "shirt", color: 2, seed: 4, hat: "fedora", hairColor: BEARD, look: "right", mood: "sad", light: "red", arms: [[24, 64], [98, 126]] };
    const R = K.rig(K0), k = 2.7, px = 700, oy = GY - 100 * k;
    const mx = R.mouth[0], my = R.mouth[1];
    // the beard: from his chin, a long white wedge that waves down to the ground and curls at the tip
    const beard = `<path d="M${mx - 9},${my - 4} L${mx + 9},${my - 5} C${mx + 16},${my + 30} ${mx + 4},${my + 50} ${mx + 14},${my + 80} C${mx + 22},${my + 104} ${mx + 8},88 ${mx + 22},98 L${mx + 4},100 C${mx - 6},86 ${mx + 2},${my + 90} ${mx - 8},${my + 60} C${mx - 16},${my + 34} ${mx - 6},${my + 20} ${mx - 9},${my - 4} Z" fill="${BEARD}" stroke="${C.line}" stroke-width="2" stroke-linejoin="round"/>` +
      `<path d="M${mx},${my + 6} C${mx + 4},${my + 30} ${mx - 2},${my + 50} ${mx + 6},${my + 80}" fill="none" stroke="#C9C2B0" stroke-width="1.6"/>`;
    const held = leashed(H, R.hand[0], -46, 0.3, { seed: 4, color: "cyan" });
    const knocker = H.at(px, oy, k, held + K.person(K0) + beard);
    const knuck = [px + k * R.hand[1][0], oy + k * R.hand[1][1]];
    const web = cobweb(knuck, [W0 + 40, knuck[1] - 30]);
    const hatTop = [px + k * R.top[0], oy + k * (R.top[1] - 8)];
    const spi = spider(C, hatTop[0] + 6, hatTop[1] - 4, 1.6);
    const ground = `<rect x="-20" y="${GY}" width="1960" height="140" fill="${GROUND}"/><path d="M-20,${GY} H1940" stroke="${C.line}" stroke-width="5"/>`;
    const svg = wall + ground + sign + win + card + knocker + web + spi;
    return { svg, alt: "The shut window under FOOD AND DRUG ADMINISTRATION with a BACK SOON card and clock; a sick human with a white beard down to the ground knocks feebly, a cobweb from his knuckles to the shutter, a spider on his hat, his disease sitting smug on its leash at his heel." };
  },

  "no-roads"(H, id) {
    const { K, C } = H;
    const SKY = "#E6D7AE", TOP = 660;
    const sky = `<rect width="1920" height="1080" fill="${SKY}"/>`;
    // the field, ending in a cliff at x 1180; the rock face drops away below
    const field = `<path d="M-20,${TOP} H1180 L1196,${TOP + 60} L1170,${TOP + 140} L1204,${TOP + 240} L1180,1100 H-20 Z" fill="${GROUND}" stroke="${C.line}" stroke-width="5" stroke-linejoin="miter"/>` +
      `<path d="M1180,${TOP} L1196,${TOP + 60} L1170,${TOP + 140} L1204,${TOP + 240} L1180,1100 L1120,1100 L1140,${TOP + 220} L1110,${TOP + 120} L1130,${TOP + 40} Z" fill="${C.rust}" stroke="${C.line}" stroke-width="4" stroke-linejoin="miter"/>` +
      `<path d="M-20,${TOP + 26} H1130" stroke="${EDGE}" stroke-width="4"/>` +
      [140, 380, 620, 860, 1060].map((x) => `<path d="M${x},${TOP + 6} l8,-16 l4,14 l6,-12 l3,14" fill="none" stroke="#9E8A55" stroke-width="3"/>`).join("");
    // the department, far back on the left, and the ROAD sign pointing right, off the edge
    const dept = H.at(150, TOP + 4, 0.62, K.props.capitol({ label: "DEPARTMENT OF TRANSPORTATION" }));
    const sign = H.at(760, TOP + 10, 1.45, K.props.sign({ text: "ROAD", fontSize: 40, posts: 1, height: 96 })) +
      `<path d="M820,${TOP - 175} H880 V${TOP - 192} L912,${TOP - 160} L880,${TOP - 128} V${TOP - 145} H820 Z" fill="${C.war}" stroke="${C.line}" stroke-width="4" stroke-linejoin="round"/>`;
    // the car in the air just past the edge, nose dipping; the commuter at the wheel, turned to the camera
    const COM = { tone: 0, outfit: "suit", color: 1, seed: 2, hat: "fedora", mood: "flat", brows: true, arms: [[50, 90], [60, 96]], build: { legPose: [[84, 40], [88, 36]] } };
    const CX = 1470, CY = 640, rot = 9, DK = 1.55, RC = K.rig(COM);
    // seated: his hips on the seat (car y -58), so only his shoulders and head show over the door
    const driver = man(H, COM, -30, -58 + (100 - RC.hipY) * DK, DK);
    const wheel = `<g transform="translate(46,-150)"><ellipse rx="10" ry="34" fill="none" stroke="${C.line}" stroke-width="7"/><path d="M0,0 L-26,60" stroke="${C.line}" stroke-width="6"/></g>`;
    const carSvg = H.at(CX, CY, 1.05, driver + wheel + car(C), rot);
    const lines = [0, 1, 2].map((i) => `<path d="M${1150 - i * 30},${470 + i * 48} h-140" stroke="${C.line}" stroke-width="4" stroke-linecap="round" opacity="0.5"/>`).join("");
    const svg = sky + field + dept + sign + lines + carSvg;
    return { svg, alt: "A 1950s convertible hangs in the air just past a cliff edge, the commuter in a fedora at the wheel looking at the camera; behind him a ROAD sign points across the grass toward the edge, and the domed department building stands far back." };
  },

  "queue-to-not-die"(H, id) {
    const { K, C } = H;
    const GY = 900;
    const field = `<rect width="1920" height="1080" fill="${GROUND}"/>`;
    // the hill the line comes down: it rises to the right of the end of the line
    const sm = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); };
    const slope = (x) => GY - 390 * sm((x - 1110) / 640);
    let hp = `M1000,${GY}`;
    for (let x = 1000; x <= 1960; x += 20) hp += ` L${x},${f1(slope(x))}`;
    const hill = `<path d="${hp} L1960,1100 L1000,1100 Z" fill="${GROUND_D}" stroke="${C.line}" stroke-width="5" stroke-linejoin="round"/>`;
    // the skeletons in line coming down the hill, each still holding its disease on the leash
    let line = "";
    [1, 2, 0, 3, 1].forEach((t, i) => {
      const o = { skeleton: true, tone: t, outfit: ["shirt", "dress", "suit", "shirt", "dress"][i], hair: i % 2, color: i, seed: 10 + i, hat: i === 3 ? "fedora" : null, look: "left", arms: [[-6, -2], [40, 90]] };
      const x = 1860 - i * 150, R = K.rig(o);
      line += man(H, o, x, slope(x), 1.5, leashed(H, R.hand[1], -44, 0.3, { seed: 20 + i, color: ["peri", "orange", "cyan", "yellow", "rust"][i] }));
    });
    // the last of the line: a skeleton waving at the camera, its disease beside it holding up the 6,650 placard
    const LAST = { skeleton: true, tone: 2, outfit: "shirt", color: 2, seed: 21, arms: [[-30, -60], [152, 178]] };
    const RL = K.rig(LAST);
    line += man(H, LAST, 1060, GY, 1.75, leashed(H, RL.hand[0], -100, 0.34, { seed: 9, color: "orange", mood: "grin" }, "6,650"));
    const posts = [1150, 1450, 1750].map((x) => `<g transform="translate(${x},${f1(slope(x))})"><rect x="-6" y="-120" width="12" height="120" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/><circle cx="0" cy="-124" r="10" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/></g>`).join("");
    const ropePath = `<path d="M1060,${GY - 100} Q1110,${GY - 70} 1150,${f1(slope(1150) - 118)} Q1300,${f1(slope(1300) - 70)} 1450,${f1(slope(1450) - 118)} Q1600,${f1(slope(1600) - 70)} 1750,${f1(slope(1750) - 118)} Q1860,${f1(slope(1860) - 80)} 1960,${f1(slope(1960) - 110)}" fill="none" stroke="${C.war}" stroke-width="8"/>`;
    // the theme park: a roller coaster, flags; its short line faces its gate on the left under WAIT: 45 MIN, the fat
    // cat at the front, red in the face, steaming, his top hat flying off
    let coaster = "";
    const trk = (x) => 300 + 160 * Math.cos((x - 120) / 120) + (x - 60) * 0.15;
    for (let x = 40; x <= 760; x += 40) coaster += `<path d="M${x},${GY - 220} V${f1(trk(x))}" stroke="${C.tan}" stroke-width="6"/>`;
    for (let x = 40; x < 760; x += 40) coaster += `<path d="M${x},${f1(trk(x) + 30)} L${x + 40},${f1(trk(x + 40) + 70)} M${x + 40},${f1(trk(x + 40) + 30)} L${x},${f1(trk(x) + 70)}" stroke="${C.tan}" stroke-width="3"/>`;
    let track = "M40," + f1(trk(40));
    for (let x = 50; x <= 760; x += 10) track += " L" + x + "," + f1(trk(x));
    coaster += `<path d="${track}" fill="none" stroke="${C.line}" stroke-width="14"/><path d="${track}" fill="none" stroke="${C.rust}" stroke-width="8"/>` +
      `<rect x="-20" y="${GY - 230}" width="800" height="26" fill="${C.cream}" stroke="${C.line}" stroke-width="4"/>`;
    const flags = [300, 560].map((x, i) => `<path d="M${x},${GY - 205} V${GY - 470}" stroke="${C.line}" stroke-width="5"/><path d="M${x},${GY - 470} L${x + 70},${GY - 450} L${x},${GY - 430} Z" fill="${[C.yellow, C.med][i]}" stroke="${C.line}" stroke-width="3"/>`).join("");
    // the gate: a striped arch with the wait sign hung on it
    const parkSign = K.props.sign({ text: "WAIT: 45 MIN", fontSize: 40, posts: 1, height: 0 }).replace(/<g class="sign-posts">[\s\S]*?<\/g>/, "");
    const gate = `<path d="M50,${GY} V${GY - 330} M250,${GY} V${GY - 330}" stroke="${C.line}" stroke-width="12"/>` +
      `<path d="M30,${GY - 330} Q150,${GY - 400} 270,${GY - 330} L270,${GY - 300} Q150,${GY - 370} 30,${GY - 300} Z" fill="${C.war}" stroke="${C.line}" stroke-width="5"/>` +
      H.at(150, GY - 250, 1.0, parkSign);
    const FAT = K.castOpts("richHuman", { look: "left", mood: "cross", brows: true, hat: null, arms: [[-120, -160], [10, 30]], hold: null });
    const RF = K.rig(FAT);
    const watch = `<g transform="translate(${f1(RF.hand[0][0])},${f1(RF.hand[0][1] - 8)})"><circle r="9" fill="${C.yellow}" stroke="${C.line}" stroke-width="2.4"/><circle r="5.5" fill="${C.cream}"/><path d="M0,0 V-4 M0,0 H3" stroke="${C.line}" stroke-width="1.4"/></g>`;
    const FX = 400, FK = 1.9;
    const fat = H.at(FX, GY - 100 * FK, FK, K.person(FAT).replace(/#F4E3CC/gi, "#E07A5F") + watch);
    const top = FX + FK * RF.top[0], topY = GY - 100 * FK + FK * RF.top[1];
    const steam = [[0, -10, 20], [10, -48, 26], [-6, -92, 30], [14, -140, 34]].map(([dx, dy, r]) => `<circle cx="${f1(top + dx)}" cy="${f1(topY + dy)}" r="${r}" fill="${WHITE}" stroke="${C.line}" stroke-width="3" opacity="0.92"/>`).join("");
    const hat = H.at(top + 70, topY - 230, 2.4, K.tophat(), 28);
    const parkLine = [{ tone: 3, outfit: "dress", hair: 1, color: 1, seed: 7, look: "left" }, { tone: 1, outfit: "shirt", color: 3, seed: 8, look: "left" }]
      .map((o, i) => man(H, o, 590 + i * 150, GY, 1.6)).join("");
    const svg = field + coaster + flags + hill + posts + gate + parkLine + fat + steam + hat + line + ropePath;
    return { svg, alt: "The end of the queue: a skeleton waves at the camera at the foot of a hill, its disease beside it on the leash holding up a placard 6,650, the line of skeletons behind it each with its disease on a leash; right beside it a plain theme park with a roller coaster, a short line at its gate under WAIT: 45 MIN, and the fat cat at its front red in the face, steaming, his top hat flying off." };
  },

  "untested-warehouse"(H, id) {
    const { K, C } = H;
    const GY = 960;
    const wall = brickWall(-20, -20, 1940, GY);
    const ground = `<rect x="-20" y="${GY}" width="1960" height="140" fill="${GROUND}"/><path d="M-20,${GY} H1940" stroke="${C.line}" stroke-width="5"/>`;
    const W0 = 900, W1 = 1520, WT = 470, WB = 720;
    // through the window: the dark warehouse, shelves of tagged bottles, the ladder, the skeleton scientist walking back
    let inside = `<rect x="${W0}" y="${WT}" width="${W1 - W0}" height="${WB - WT}" fill="${C.slate}"/>`;
    inside += shelf(H, W0 - 40, W1 + 40, WT + 70, 0.55, true) + shelf(H, W0 - 40, W1 + 40, WT + 170, 0.55, true);
    inside += `<path d="M1420,${WT - 10} L1460,${WB} M1490,${WT - 10} L1530,${WB}" stroke="${C.tan}" stroke-width="8"/>` +
      [0, 1, 2, 3, 4].map((i) => `<path d="M${1424 + i * 8},${WT + 30 + i * 48} H${1494 + i * 8}" stroke="${C.tan}" stroke-width="6"/>`).join("");
    const SCI = { skeleton: true, tone: 3, hair: 1, outfit: "labcoat", seed: 3, look: "right", arms: [[10, 30], [-20, -10]], build: { hunch: 18, legPose: [[-20, -10], [20, 10]] } };
    const sciGlasses = `<circle cx="-7.5" cy="-3" r="6" fill="none" stroke="${C.line}" stroke-width="2.4"/><circle cx="7.5" cy="-3" r="6" fill="none" stroke="${C.line}" stroke-width="2.4"/><path d="M-1.5,-3 H1.5" stroke="${C.line}" stroke-width="2"/>`;
    const RS = K.rig(SCI);
    // her lab coat: two open white panels from the shoulders to the knees, the ribs showing between them
    const sx0 = RS.shoulder[0][0], sx1 = RS.shoulder[1][0], sy = RS.shoulder[0][1], hy = RS.hipY;
    const coat = `<g transform="rotate(18 0 ${f1(hy)})"><path d="M${sx0 - 3},${sy - 2} L${sx0 + 7},${sy - 2} L${sx0 + 5},${hy + 28} L${sx0 - 9},${hy + 28} Z M${sx1 - 7},${sy - 2} L${sx1 + 3},${sy - 2} L${sx1 + 9},${hy + 28} L${sx1 - 5},${hy + 28} Z" fill="${WHITE}" stroke="${C.line}" stroke-width="2.4" stroke-linejoin="miter"/></g>`;
    const sciSvg = K.person(SCI).replace("<!--face-end-->", sciGlasses + "<!--face-end-->");
    const cane = `<path d="M${f1(RS.hand[1][0])},${f1(RS.hand[1][1])} L${f1(RS.hand[1][0] + 10)},100" stroke="${C.rust}" stroke-width="4"/>`;
    inside += H.at(1260, WB + 50 - 100 * 1.6, 1.6, sciSvg + coat + cane);
    const win = windowBox(H, id, W0, WT, W1, WB, 0, inside);
    const sign = fdaSign(H, (W0 + W1) / 2, 400, 38);
    const wait = waitSign(H, (W0 + W1) / 2, 100, 0.92, "15 PER YEAR", "443", "YEARS");
    // the flat-nosed human from queue-to-not-die, now a skeleton, at the counter shaking its bottle; its disease on the
    // leash in its other hand, twice the size it was
    const S16 = { skeleton: true, tone: 1, outfit: "shirt", color: 0, seed: 16, look: "right", arms: [[20, 50], [130, 168]] };
    const R16 = K.rig(S16), k = 2.6;
    const bottle = H.at(R16.hand[1][0], R16.hand[1][1] + 4, 0.42, K.props.pillBottle({ face: "smile" }), 14);
    const shakes = `<path d="M${R16.hand[1][0] - 22},${R16.hand[1][1] - 40} l-8,-6 M${R16.hand[1][0] + 22},${R16.hand[1][1] - 44} l8,-8 M${R16.hand[1][0] + 26},${R16.hand[1][1] - 22} l10,-2" stroke="${C.line}" stroke-width="2.4" stroke-linecap="round"/>`;
    const tix = leashed(H, R16.hand[0], -60, 0.5, { seed: 16, color: "peri", mood: "grin" });
    const sk16 = man(H, S16, 640, GY, k, tix + bottle + shakes);
    const svg = wall + ground + win + sign + wait + sk16;
    return { svg, alt: "The ticket window from outside: the wait sign over it stopped on WAIT TIME FROM HERE: 443 YEARS; at the counter a skeleton shakes its pill bottle, delighted, its disease grinning on the leash beside it, twice the size; through the window, shelves of bottles tagged NEVER TESTED FOR THIS and the skeleton scientist in her lab coat and glasses shuffling back toward the ladder." };
  },

  "weirdly-calm"(H, id) {
    const { K, C } = H;
    // the YOU headstone on the floor right of the lectern, its 80 YEARS tag; the reader from Part 8 in his orange
    // armchair beside it under his floor lamp, his near elbow on the headstone, reading the manual
    const SX = 1400, SY = 1040, SK = 2.4;
    const stone = H.at(SX, SY, SK, K.props.headstone({ text: "YOU" }));
    const tag = H.at(SX - 38 * SK, SY - 104 * SK, 1.35, hangTag(H, "80 YEARS", 24));
    const g = 1.5, CX = 1680, FY = 1075; // Part 8's living-room units, scaled into the host shot
    const SEAT = copy(SEATED8, { mood: "smile", arms: [[-62, -100], [-58, -124]] });
    const R = K.rig(SEAT);
    const book = H.at(R.hand[1][0] - 6, R.hand[1][1] + 4, 0.4, K.props.manual()) + H.at(R.hand[1][0] - 4, R.hand[1][1] - 34, 0.7, ticket8(H), 70);
    const room = H.at(CX + 140 * g, FY, g, lamp8(H)) + H.at(CX, FY, g, armchair8(H, false)) +
      H.at(CX, FY + g * (-58 - R.hipY * 1.6), g * 1.6, K.person(SEAT) + book) + H.at(CX, FY, g, armchair8(H, true));
    const svg = H.host("skeptical-closed", "palms-down", stone + tag + room);
    return { svg, alt: "Wishonia at her lectern squints at the camera, palms down; beside her a headstone engraved YOU with an 80 YEARS tag, and the reader in his orange armchair under his floor lamp, his elbow on his own headstone, reading the manual calmly." };
  },
};
