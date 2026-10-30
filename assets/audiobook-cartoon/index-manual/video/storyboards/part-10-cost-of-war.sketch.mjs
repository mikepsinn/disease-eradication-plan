// Sketches for storyboards/part-10-cost-of-war.md (v3, the 1950s atomic-age film look): each scene's key moment on a
// 1920 x 1080 frame, drawn with the production art (H.K: kit.js, film.js and the props library). Host shots use the
// studio set (H.host, or its parts when something must sit on the wall behind Wishonia); a plate frame is what the
// camera sees at that moment, one framing, with the ground and the cast drawn large. Built into the review sheet by
// tools/storyboard-sheet.mjs.

const GROUND = "#C8B07B", SKY = "#EFE3C4", ROAD = "#EEE3C4", EDGE = "#B09363", DUSTLINE = "#8E7A55", PUFF = "#E9E1CF";
const DESERT = "#D8B77C", DESERT_SKY = "#F1E2BE", CRACK = "#A8834F", WATER = "#5C8FA0", GLINT = "#BFE0E6";
const YOU = { tone: 2, outfit: "suit", hat: "bowler" };
const f = (n) => (+n).toFixed(1);
const copy = (a, b) => Object.assign({}, a, b);

// A plain field: the sky down to the horizon, the ground below it.
function plate(horizon, sky = SKY, ground = GROUND) {
  return `<rect width="1920" height="1080" fill="${ground}"/>` +
    (horizon > 0 ? `<rect width="1920" height="${horizon}" fill="${sky}"/><path d="M0,${horizon} H1920" stroke="${DUSTLINE}" stroke-width="3" opacity="0.6"/>` : "");
}
// A person standing with its feet on y `feet`, k times person size (KIT.person draws the feet at y 100).
function man(H, o, x, feet, k, extra = "", rot = 0) {
  return H.at(x, feet - 100 * k, k, H.K.person(o) + extra, rot);
}
// Where a person's point (a rig point in person units) lands on the canvas, for a person drawn by man(H, o, x, feet, k).
function onCanvas(p, x, feet, k) {
  return [x + k * p[0], feet - 100 * k + k * p[1]];
}
function handAt(H, o, x, feet, k, i) {
  return onCanvas(H.K.rig(o).hand[i], x, feet, k);
}
// Puffs of smoke or cloud: [x, y, r] circles sharing one navy outline.
function puffs(C, list, fill = PUFF) {
  return list.map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${C.line}" stroke="${C.line}" stroke-width="8"/>`).join("") +
    list.map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}"/>`).join("");
}
function wisps(x, y, n = 3, s = 1) {
  let out = "";
  for (let i = 0; i < n; i++) out += `<path d="M${x + i * 16 * s},${y - i * 6 * s} l${-10 * s},${-18 * s} l${10 * s},${-18 * s} l${-10 * s},${-18 * s}" fill="none" stroke="#8C8782" stroke-width="${6 * s}" stroke-linecap="round"/>`;
  return out;
}
function flake(x, y, r, col, w) {
  const a = r * 0.5, b = r * 0.866;
  return `<path d="M${f(x - r)},${f(y)} H${f(x + r)} M${f(x - a)},${f(y - b)} L${f(x + a)},${f(y + b)} M${f(x - a)},${f(y + b)} L${f(x + a)},${f(y - b)}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`;
}
// A big hanging card tag (canvas px): its knot at (x, y), the card w x h hanging below and right of it, with a grommet.
function bigTag(C, x, y, w, h, inner, tilt = 6) {
  const cx = x + 30, cy = y + 40;
  const card = `M${cx - 22},${cy + 24} L${cx},${cy} H${cx + w} V${cy + h} H${cx} L${cx - 22},${cy + h - 24} Z`;
  return `<path d="M${x},${y} Q${x - 10},${y + 24} ${cx + 8},${cy + 10}" fill="none" stroke="${C.line}" stroke-width="4"/>` +
    `<g transform="rotate(${tilt} ${cx} ${cy})"><path d="${card}" fill="${C.line}" stroke="${C.line}" stroke-width="9" stroke-linejoin="miter"/><path d="${card}" fill="#FBF6E6"/>` +
    `<rect x="${cx + 14}" y="${cy + 10}" width="${w - 26}" height="${h - 20}" fill="none" stroke="${C.orange}" stroke-width="2.5"/>` +
    `<circle cx="${cx - 6}" cy="${cy + h / 2}" r="11" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/><circle cx="${cx - 6}" cy="${cy + h / 2}" r="5" fill="${GROUND}" stroke="${C.line}" stroke-width="2"/>` +
    `<g transform="translate(${cx},${cy})">${inner}</g></g>`;
}
// The weapons maker's smiling baby missile (the cast prop, as Part 2's money-loop draws it), pointing +x around (0, 0),
// in a frilly cream bonnet tied with a pink ribbon over its nose cone.
function babyMissile(C, bonnet = true) {
  const ink = C.line;
  const body = `<path d="M-34,-7 L14,-7 L30,0 L14,7 L-34,7 Z" fill="${C.war}" stroke="${ink}" stroke-width="2.6" stroke-linejoin="round"/>` +
    `<path d="M-34,-7 L-44,-17 L-40,-7 Z M-34,7 L-44,17 L-40,7 Z" fill="${C.war}" stroke="${ink}" stroke-width="2.4" stroke-linejoin="round"/>` +
    `<path d="M14,-7 L30,0 L14,7 Z" fill="${C.cream}" stroke="${ink}" stroke-width="2"/>`;
  const face = `<path d="M-6,1.5 Q1,7 8,1.5" fill="none" stroke="${ink}" stroke-width="1.8" stroke-linecap="round"/><circle cx="-3" cy="-2.6" r="1.7" fill="${ink}"/><circle cx="6" cy="-2.6" r="1.7" fill="${ink}"/>` +
    `<circle cx="-7" cy="2" r="2" fill="#E07F95" opacity="0.7"/>`;
  let frill = "";
  if (bonnet) {
    // the hood over the nose, a ring of ruffles round its open edge, the ribbon tied under the "chin"
    const hood = `<path d="M10,-12 Q34,-16 38,0 Q34,16 10,12 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="2"/>`;
    let ruff = "";
    for (let i = 0; i < 7; i++) { const a = -1.2 + i * 0.4; ruff += `<circle cx="${f(11 + 2 * Math.cos(a))}" cy="${f(13 * Math.sin(a))}" r="3.4" fill="#FBF6E6" stroke="${ink}" stroke-width="1.4"/>`; }
    frill = hood + ruff + `<path d="M12,12 l-7,9 M12,12 l3,10" stroke="#E07F95" stroke-width="2.6" stroke-linecap="round"/><circle cx="12" cy="12" r="2.6" fill="#E07F95"/>`;
  }
  return `<g transform="translate(-2,0)">${body}${face}${frill}</g>`;
}
// A baby rattle, around (0, 0), its handle pointing down.
function rattle(C, s = 1) {
  return `<g transform="scale(${s})"><path d="M0,0 V22" stroke="${C.line}" stroke-width="4"/><circle cx="0" cy="-8" r="10" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/><circle cx="-3" cy="-11" r="3" fill="${C.cream}"/></g>`;
}
// Dotted outline: the nothing-papers, drawn as the outline of a paper and nothing else. Not in any key frame (the
// nothing-papers HOLD is Part 2's family); kept for the scene author: this is how the papers and the bomb look.
function dotted(svg, col) {
  return `<g stroke-dasharray="5 5">${svg.replace(/fill="#[0-9A-Fa-f]{6}"/g, 'fill="none"').replace(/stroke="#[0-9A-Fa-f]{6}"/g, `stroke="${col}"`)}</g>`;
}
// The crack the quake leaves zigzagging up the studio wall (probably, periscope).
function crack(C, x, y) {
  return `<path d="M${x},${y} l-18,-60 l26,-40 l-30,-56 l22,-48 l-14,-62 l20,-40" fill="none" stroke="${C.line}" stroke-width="7" stroke-linejoin="miter"/>` +
    `<path d="M${x + 8},${y - 100} l34,-14 l10,-30 M${x - 10},${y - 210} l-32,-10" fill="none" stroke="${C.line}" stroke-width="4"/>`;
}
// Wishonia's coffee mug, standing on (x, y), about 100 tall at s 1.15; chip: a notch out of its rim.
function mug(C, x, y, s = 1, chip = false) {
  const g = `<path d="M-38,-86 H38 L34,-4 Q34,0 30,0 H-30 Q-34,0 -34,-4 Z" fill="${C.cream}" stroke="${C.line}" stroke-width="5" stroke-linejoin="round"/>` +
    `<path d="M36,-70 Q68,-66 62,-40 Q58,-20 34,-22" fill="none" stroke="${C.line}" stroke-width="13"/><path d="M36,-70 Q68,-66 62,-40 Q58,-20 34,-22" fill="none" stroke="${C.cream}" stroke-width="6"/>` +
    `<rect x="-30" y="-62" width="60" height="16" fill="${C.orange}"/><path d="M-34,-80 H34" stroke="#6B4A2F" stroke-width="7"/>` +
    (chip ? `<path d="M8,-90 l7,12 l9,-12 Z" fill="${C.line}"/>` : "");
  return `<g transform="translate(${x},${y}) scale(${s})">${g}</g>`;
}
// The shelves of the murder mart, behind the aisle (canvas px): a long unit from y0 to y1.
function shelves(C, y0, y1) {
  const ink = C.line, step = (y1 - y0) / 3;
  return `<rect x="-20" y="${y0}" width="1960" height="${y1 - y0}" fill="${C.rust}" stroke="${ink}" stroke-width="6"/>` +
    [1, 2].map((i) => `<rect x="-20" y="${f(y0 + i * step - 8)}" width="1960" height="16" fill="${C.tan}" stroke="${ink}" stroke-width="4"/>`).join("") +
    `<rect x="-20" y="${y1 - 8}" width="1960" height="30" fill="${C.slate}"/>`;
}
// A little shed with a gable roof and a big door, standing on (0, 0), in canvas px at size 1: the workshop.
function workshop(C) {
  const ink = C.line;
  return `<path d="M-130,0 V-150 H130 V0 Z" fill="${C.tan}" stroke="${ink}" stroke-width="5"/><path d="M-150,-146 L0,-230 L150,-146 Z" fill="${C.slate}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    `<rect x="-60" y="-110" width="120" height="110" fill="${C.deep}" stroke="${ink}" stroke-width="5"/><path d="M-60,-110 L60,0 M60,-110 L-60,0" stroke="${C.tan}" stroke-width="6"/>`;
}

export default {
  "cost-of-war-title"(H, id) {
    const { K, C } = H;
    const cx = 960, cy = 280, rx = 200, ry = 62;
    const orbits = [0, 60, -60].map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = [[0, 0.5], [60, 2.6], [-60, 4.7]].map(([a, th]) => {
      const r = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return H.at(cx + ex * Math.cos(r) - ey * Math.sin(r), cy + ex * Math.sin(r) + ey * Math.cos(r) - 6, 0.62, K.money("war", 1));
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    // the tag hangs from the foot of the R, flipped to "$", and its ribbon of zeros runs off the bottom of the card
    const ribbon = `<path d="M1376,930 C1420,980 1380,1030 1430,1100 L1490,1100 C1440,1030 1480,980 1436,920 Z" fill="${C.line}" stroke="${C.line}" stroke-width="8"/>` +
      `<path d="M1376,930 C1420,980 1380,1030 1430,1100 L1490,1100 C1440,1030 1480,980 1436,920 Z" fill="#FBF6E6"/>` +
      `<text transform="translate(1404,948) rotate(68)" font-family="Oswald" font-weight="600" font-size="32" fill="${C.line}">000,000,000,0</text>`;
    const tag = bigTag(C, 1262, 782, 120, 96, H.label(64, 74, 64, "$"), 34);
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus +
      H.big(960, 560, 104, "THE COST OF", "middle", C.cream) + H.big(960, 790, 250, "WAR", "middle", C.cream) + ribbon + tag;
    return { svg, alt: "The period title card: THE COST OF WAR in cream on navy under the atom of running papers; a price tag hangs from the R, flipped to a dollar sign, and a ribbon of zeros runs from it off the bottom of the card." };
  },

  "cash-register"(H, id) {
    const { K, C } = H;
    const ink = C.line;
    // a side table at her right, its top level with the lectern's, and a brass register on it
    const table = `<rect x="1170" y="790" width="500" height="34" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M1200,824 V1080 M1640,824 V1080" stroke="${ink}" stroke-width="14"/><path d="M1200,824 V1080 M1640,824 V1080" stroke="${C.tan}" stroke-width="7"/>`;
    const rx = 1410, by = 790;
    let keys = "";
    for (let r = 0; r < 3; r++) for (let c = 0; c < 6; c++) keys += `<circle cx="${rx - 125 + c * 50 + r * 6}" cy="${by - 150 + r * 34}" r="14" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>`;
    const register =
      `<path d="M${rx - 200},${by} H${rx + 200} L${rx + 178},${by - 200} H${rx - 178} Z" fill="${C.yellow}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
      `<path d="M${rx + 186},${by - 8} L${rx + 168},${by - 192}" stroke="${C.rust}" stroke-width="5"/>` +
      `<path d="M${rx - 160},${by - 186} H${rx + 160} L${rx + 150},${by - 74} H${rx - 150} Z" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` + keys +
      `<rect x="${rx - 190}" y="${by - 300}" width="380" height="96" fill="${C.deep}" stroke="${ink}" stroke-width="6"/>` +
      `<rect x="${rx - 176}" y="${by - 288}" width="352" height="72" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>` +
      `<text x="${rx}" y="${by - 232}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="58" fill="${ink}">$2.72 TRILLION</text>` +
      `<path d="M${rx + 190},${by - 120} l40,-10 l0,-60" fill="none" stroke="${ink}" stroke-width="10"/><circle cx="${rx + 230}" cy="${by - 190}" r="12" fill="${C.war}" stroke="${ink}" stroke-width="3"/>` +
      `<path d="M${rx - 150},${by - 56} H${rx + 230} L${rx + 260},${by + 4} H${rx - 120} Z" fill="${C.tan}" stroke="${ink}" stroke-width="5"/>` +
      `<rect x="${rx + 40}" y="${by - 46}" width="80" height="12" fill="${C.money}" stroke="${ink}" stroke-width="2"/>`;
    // the baby missile on its jack-in-the-box spring, up out of the drawer, shaking its rattle
    let spring = "M1610,770";
    for (let i = 1; i <= 8; i++) spring += ` L${1610 + (i % 2 ? 44 : -16) + i * 8},${770 - i * 27}`;
    const springSvg = `<path d="${spring}" fill="none" stroke="${ink}" stroke-width="12" stroke-linejoin="miter"/><path d="${spring}" fill="none" stroke="${C.cream}" stroke-width="5" stroke-linejoin="miter"/>`;
    const baby = H.at(1775, 410, 4.4, babyMissile(C), -42) + H.at(1860, 500, 2.6, rattle(C), 34);
    const svg = H.host("sideeye-closed", "idle", table + register + springSvg + baby);
    return { svg, alt: "Wishonia at the lectern side-eyes a brass cash register on a side table; its window reads $2.72 TRILLION, and from its open drawer a grinning baby missile in a frilly bonnet bobs up on a spring, shaking a rattle." };
  },

  "warheads-in-the-cart"(H, id) {
    const { K, C } = H;
    const FLOOR = 880, k = 2.5, CK = 4.4, cartX = 960;
    const top = FLOOR - 74 * CK;
    const bomb = (x, y, s, face, tag) => H.at(x, y, s, K.props.bomb({ face, lit: false }) + (tag ? H.at(36, -76, 0.9, K.props.priceTag({ text: "$" })) : ""));
    let heap = "";
    [[-60, 0], [60, 0], [180, 0], [0, -1], [120, -1], [60, -2]].forEach(([dx, row], i) => {
      heap += bomb(cartX + dx, top + 20 + row * 100, 1.45, ["grin", "smile", "grin", "smug"][i % 4], i % 3 === 0);
    });
    // the SPARE warhead on top, its tag just caught on the fuse
    heap += bomb(cartX + 60, top - 270, 1.45, "grin", false) + H.at(cartX + 116, top - 400, 2.2, K.props.priceTag({ text: "SPARE", angle: 14 }));
    const cart = H.at(cartX, FLOOR, CK, K.props.shoppingCart());
    // the baby missile in the child seat by the handle, peeking over the basket's rim
    const baby = H.at(cartX - 140, top - 40, 2.8, babyMissile(C), -62);
    // the heap's big tag, hanging off the basket's front: 122 red snowflakes
    let grid = "";
    for (let i = 0; i < 122; i++) grid += flake(28 + (i % 11) * 25, 26 + Math.floor(i / 11) * 22, 8, C.war, 2.6);
    const tag = bigTag(C, cartX + 210, top + 60, 316, 300, grid, -4);
    // the politician pushing; the weapons maker by the bin, both arms up: ta-da
    const POL = K.castOpts("politician", { look: "right", mood: "grin", arms: [[150, 150], [140, 140]] });
    const WM = K.castOpts("weaponsMaker", { look: "left", mood: "grin", arms: [[-150, -170], [150, 170]] });
    const svg = plate(0) + shelves(C, 380, 830) + man(H, WM, 1560, FLOOR, k * 1.05) + man(H, POL, 560, FLOOR, k) + heap + baby + cart + tag;
    return { svg, alt: "The murder mart aisle: the politician pushes a giant shopping cart heaped with grinning warheads, each with a tiny price tag; the top one wears a SPARE tag; the heap's big tag is full of 122 red snowflakes; the baby missile in its bonnet peeks out of the child seat, and the weapons maker throws his arms up by the shelves." };
  },

  "cart-gadgets"(H, id) {
    const { K, C } = H;
    const FLOOR = 1010, CK = 4.6, cartX = 980, ink = C.line;
    const top = FLOOR - 74 * CK;
    let heap = "";
    [[-150, 0], [-20, 0], [110, 0], [240, 0], [-85, -1], [45, -1], [175, -1]].forEach(([dx, row], i) => {
      heap += H.at(cartX + dx, top + 30 + row * 104, 1.5, K.props.bomb({ face: ["grin", "smug"][i % 2], lit: false }));
    });
    // the Space Force guard: a grinning skeleton on top of the heap, in his fishbowl helmet, binoculars still up
    const GUARD = { tone: 1, outfit: "shirt", color: 1, kind: "twig", look: "right", arms: [[165, 200], [150, 205]], build: { legs: 1.3, neck: 1.8, hs: 0.8 } };
    const gk = 1.75, gx = cartX + 60, gf = top - 196;
    const head = onCanvas(K.rig(GUARD).head, gx, gf, gk);
    const bino = `<g transform="translate(${f(head[0] + 26)},${f(head[1] - 10)}) rotate(-38)"><rect x="-4" y="-22" width="36" height="18" rx="4" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><rect x="-4" y="2" width="36" height="18" rx="4" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><rect x="30" y="-24" width="10" height="22" fill="${ink}"/><rect x="30" y="0" width="10" height="22" fill="${ink}"/></g>`;
    const bowl = `<circle cx="${f(head[0] + 4)}" cy="${f(head[1] - 4)}" r="${f(gk * 30)}" fill="${GLINT}" fill-opacity="0.35" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M${f(head[0] - 26)},${f(head[1] - 32)} q10,-18 28,-20" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.8"/>` +
      `<rect x="${f(head[0] - 40)}" y="${f(head[1] + 40)}" width="88" height="15" rx="5" fill="${C.peri}" stroke="${ink}" stroke-width="4"/>`;
    const guard = man(H, copy(GUARD, { skeleton: true }), gx, gf, gk) + bowl + bino;
    // the murder-bot in the back of the basket, one pincer up, its zap still smoking
    const bot = H.at(cartX - 210, top + 40, 1.8, K.props.robot({ mood: "cross", light: "red", arms: [[20, 10], [150, 120]] }));
    const smoke = wisps(cartX - 100, top - 260, 3, 1.1);
    const cart = H.at(cartX, FLOOR, CK, K.props.shoppingCart());
    const baby = H.at(cartX - 150, top - 34, 2.8, babyMissile(C), -62);
    // the charred politician at the handle, blinking
    const POL = K.castOpts("politician", { look: "right", charred: true, arms: [[150, 150], [140, 140]] });
    const svg = plate(0) + shelves(C, 300, 860) + bot + smoke + heap + guard + baby + cart + man(H, POL, 440, FLOOR, 2.8);
    return { svg, alt: "Close on the cart: the frowning murder-bot in the basket with smoke curling off its raised pincer; on top of the warhead heap the Space Force guard is a grinning skeleton in a fishbowl helmet, still looking up through his binoculars; the charred politician blinks at the handle." };
  },

  probably(H, id) {
    const { K, C } = H;
    const S = K.STUDIO;
    const dust = [[610, 120], [700, 60], [860, 150], [930, 90], [780, 30], [660, 200], [990, 210]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="7" fill="#F6EEDA" opacity="0.9"/>`).join("") +
      [[640, 170, 24], [900, 120, 30], [760, 90, 22]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#F6EEDA" opacity="0.55"/>`).join("");
    const inner = H.K.studioWall() + crack(C, 1220, 700) + H.wish(S.wish.x, S.wish.y, S.wish.w, "skeptical-closed", "shrug") + dust + K.lectern() +
      H.at(1050, 770, 1, mug(C, 0, 0, 1.15), 24) + `<path d="M1000,800 l-20,-20 M1090,812 l16,-24" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/>`;
    const svg = `<rect width="1920" height="1080" fill="#0B0805"/><g transform="rotate(-2.5 960 540) translate(-24,0) scale(1.03)">${inner}</g>`;
    return { svg, alt: "Wishonia shrugs at the lectern while the studio jolts sideways: a crack zigzags up the wall behind her, plaster dust sifts onto her bob, and her coffee mug tips off the edge of the lectern." };
  },

  "nothing-papers"(H, id) {
    const { K, C } = H;
    const ink = C.line;
    // Part 2's own field (the-toll), framed as the-toll's wide view: the family's feet on screen y 860, the horizon
    // 530 above them, the ground and sky gone gray, rows of headstones receding to the vanishing point. The family,
    // their loaves, the stones and the number are the-toll's own drawing (copy them from
    // compositions/scenes/part-02/the-toll.html, not this sketch).
    const FEET = 860, HZ = 530, S = 1.5, X0 = 960;
    const STONE = "#E6E0D2", SHADE = "#A9AEB8";
    const DK = [];
    for (let d = 480; d >= 16; d *= 0.8) DK.push(d);
    const halfW = 1040;
    const rows = DK.map((dk) => {
      const base = FEET - HZ + dk, sc = dk / HZ, w = 104 * sc, h = 160 * sc, step = 200 * sc;
      let body = "", side = "";
      for (let j = -Math.ceil(halfW / step); j <= Math.ceil(halfW / step); j++) {
        const x = X0 + j * step, l = x - w / 2, r = x + w / 2, top = base - h + w / 2;
        body += `M${f(l)},${f(base)} V${f(top)} A${f(w / 2)},${f(w / 2)} 0 0,1 ${f(r)},${f(top)} V${f(base)} Z `;
        side += `M${f(r - w * 0.24)},${f(base)} V${f(top - w * 0.06)} A${f(w / 2)},${f(w / 2)} 0 0,1 ${f(r)},${f(top)} V${f(base)} Z `;
      }
      const stroke = dk > 120 ? ` stroke="${ink}" stroke-width="${f(Math.max(1.2, 4 * sc))}" stroke-linejoin="round"` : "";
      const mound = dk > 120 ? `<path d="M${X0 - halfW},${f(base)} H${X0 + halfW}" stroke="${DUSTLINE}" stroke-width="${f(6 * sc)}" opacity="0.5"/>` : "";
      return mound + `<path d="${body}" fill="${STONE}"${stroke}/><path d="${side}" fill="${SHADE}"/>`;
    }).reverse().join("");
    // the skeleton family from Part 2, still holding their loaves (only the bread in color)
    const loaf = `<path d="M-30,6 Q-32,-14 -10,-16 Q8,-20 24,-12 Q34,-4 30,8 Q0,14 -30,6 Z" fill="#D49A4E" stroke="${ink}" stroke-width="3.2" stroke-linejoin="round"/>` +
      `<path d="M-16,-8 l8,-6 M-2,-9 l8,-6 M12,-8 l8,-6" stroke="#F3DFB0" stroke-width="3" stroke-linecap="round"/>`;
    const LOAF_ARMS = [[-22, -112], [-8, -106]];
    const FAM = [
      { o: { tone: 1, outfit: "shirt", color: 1, hair: 0, seed: 3 }, x: -150, k: S },
      { o: { tone: 1, outfit: "dress", color: 3, hair: 1, seed: 2 }, x: 0, k: S },
      { o: { tone: 1, outfit: "shirt", color: 0, hair: 0, seed: 5, build: { hs: 1.18, legs: 0.8 } }, x: 130, k: S * 0.72 },
    ];
    const fam = FAM.map((m) => {
      const o = copy(m.o, { look: "left", arms: LOAF_ARMS, skeleton: true }), R = K.rig(o);
      const held = H.at((R.hand[0][0] + R.hand[1][0]) / 2 - 4, (R.hand[0][1] + R.hand[1][1]) / 2 - 4, 0.62, loaf);
      return H.at(X0 + m.x, FEET - 100 * m.k, m.k, K.person(o) + held);
    }).join("");
    // the last of the bomb's smoke, drifting off low across the field
    const smoke = [[520, 846, 150, 22], [700, 868, 120, 16], [1260, 852, 170, 24], [1450, 870, 110, 14]].map(([x, y, rx, ry]) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="#C9C5BB" opacity="0.7"/>`).join("") +
      wisps(690, 760, 2, 0.9) + wisps(1200, 770, 2, 0.9);
    const svg = `<rect width="1920" height="1080" fill="#A9A69B"/><rect width="1920" height="${FEET - HZ}" fill="#DCD8CE"/>` +
      `<path d="M0,${FEET - HZ} H1920" stroke="${DUSTLINE}" stroke-width="3" opacity="0.6"/>` + rows + smoke + fam +
      `<text x="960" y="200" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="172" letter-spacing="4" fill="${C.navy}">310,000,000</text>`;
    return { svg, alt: "The HOLD, an explicit callback to Part 2: its gray field of headstones running to the horizon, the same skeleton family still standing in the middle holding their loaves, the last of the bomb's smoke drifting off them, and the same 310,000,000 stamped in the sky in the same place." };
  },

  "paycheck-shrinks"(H, id) {
    const { K, C } = H;
    const HZ = 600, FEET = 900, ink = C.line;
    // the flattened town behind, folded like cardboard
    const flat = (x, v, sx, sy) => H.at(x, HZ + 60, 1, `<g transform="scale(${sx},${sy})">${K.props.house({ variant: v, smoke: false })}</g>`);
    const town = flat(160, 0, 1.0, 0.2) + flat(470, 1, 1.0, 0.18) + H.at(1500, HZ + 60, 1, `<g transform="scale(0.8,0.2)">${workshop(C)}</g>`) + flat(1800, 3, 1.0, 0.2);
    // the bakery, folded flat round their feet: the squashed shop, its striped awning lying on top, a loaf sign by it
    const shop = H.at(980, FEET + 8, 1, `<g transform="scale(3.0,0.17)">${K.props.house({ variant: 2, smoke: false })}</g>`);
    const awning = `<path d="M440,${FEET - 14} L470,${FEET - 46} H1490 L1520,${FEET - 14} Z" fill="${C.cream}" stroke="${ink}" stroke-width="6"/>` +
      Array.from({ length: 10 }, (_, i) => `<path d="M${f(474 + i * 104)},${FEET - 44} h52 l4,28 h-52 Z" fill="${C.rust}"/>`).join("") +
      `<g transform="translate(1600,${FEET - 4}) rotate(-8)"><path d="M-60,0 Q-64,-30 -30,-34 Q0,-40 30,-30 Q56,-20 56,0 Z" fill="#D49A4E" stroke="${ink}" stroke-width="5"/></g>` +
      `<path d="M560,${FEET - 50} l20,-26 l26,22 M1340,${FEET - 48} l14,-26 l30,18" fill="none" stroke="${ink}" stroke-width="5"/>`;
    // YOU holds up his sliver of paycheck and the one crumb to look at them; the baker keeps her tweezers out
    const YOUo = copy(YOU, { look: "right", mood: "worried", arms: [[10, 4], [150, 200]] });
    const BAKER = { tone: 1, hair: 1, kind: "pear", outfit: "dress", color: 0, look: "left", mood: "flat", arms: [[-60, -100], [-10, -4]], build: { hs: 1, legs: 0.7, th: 0.9 } };
    const yk = 3.1, yx = 740, bx = 1250;
    const hY = handAt(H, YOUo, yx, FEET - 40, yk, 1), hB = handAt(H, BAKER, bx, FEET - 40, yk, 0);
    const sliver = `<rect x="${f(hY[0] - 6)}" y="${f(hY[1] - 46)}" width="12" height="42" fill="${C.money}" stroke="${ink}" stroke-width="3"/>` +
      `<circle cx="${f(hY[0] + 22)}" cy="${f(hY[1] - 12)}" r="9" fill="#D49A4E" stroke="${ink}" stroke-width="3"/>`;
    const tweez = `<path d="M${f(hB[0])},${f(hB[1])} l-74,-8 M${f(hB[0])},${f(hB[1])} l-72,8" stroke="${C.peri}" stroke-width="6" stroke-linecap="round"/>`;
    const svg = plate(HZ, "#E6DDC8", "#C3B28A") + town + shop + awning + man(H, YOUo, yx, FEET - 40, yk) + man(H, BAKER, bx, FEET - 40, yk) + sliver + tweez;
    return { svg, alt: "The bakery has folded flat around their feet: YOU in his bowler and the pear-shaped baker stand in the open air of the flattened town; YOU holds up a sliver of paycheck and one crumb, and the baker still holds out her tweezers." };
  },

  "bought-the-other-thing"(H, id) {
    const { K, C } = H;
    const HZ = 470, TOP = 700, ink = C.line;
    const counter = `<rect x="80" y="${TOP}" width="1180" height="30" fill="${C.tan}" stroke="${ink}" stroke-width="6"/><rect x="100" y="${TOP + 30}" width="1140" height="260" fill="${C.rust}" stroke="${ink}" stroke-width="6"/>` +
      `<path d="M130,${TOP + 60} H1210" stroke="${C.orange}" stroke-width="3"/>`;
    const tilt = -28, s = 3.0, sx = 720;
    const scale = H.at(sx, TOP, s, K.props.balanceScale({ tilt }));
    const a = (tilt * Math.PI) / 180, L = [sx - s * 84 * Math.cos(a), TOP + s * (-150 - 84 * Math.sin(a) + 64)];
    // the war mountain on the low pan, SOLD on it
    let mount = "";
    [[-3, 0], [-1, 0], [1, 0], [3, 0], [-2, 1], [0, 1], [2, 1], [-1, 2], [1, 2], [0, 3]].forEach(([c, r], i) => { mount += H.at(L[0] + c * 40, L[1] - 18 - r * 38, 0.9, K.money("war", 0), (i % 3 - 1) * 8); });
    const sold = H.at(L[0] + 70, L[1] - 110, 2.4, K.props.priceTag({ text: "SOLD", ink: C.war, angle: 10 }));
    // the politician behind the counter, his thumb pressing the mountain down
    const POL = K.castOpts("politician", { look: "right", mood: "smug", arms: [[-8, -3], [110, 150]] });
    const pk = 2.6, pf = TOP + 120;
    const hP = handAt(H, POL, 0, pf, pk, 1), px = L[0] - hP[0] + 6;
    const pol = man(H, POL, px, pf, pk);
    // YOU in front with the long receipt, held up in both hands
    const YOUo = copy(YOU, { look: "left", mood: "flat", arms: [[-80, -130], [-60, -120]] });
    const yk = 2.7, yx = 1580, yf = 960;
    const h0 = handAt(H, YOUo, yx, yf, yk, 0), h1 = handAt(H, YOUo, yx, yf, yk, 1);
    const rx = h0[0] - 250, ry = Math.min(h0[1], h1[1]) - 170;
    const receipt = `<path d="M${sx + 30},${TOP + 16} C${sx + 220},${TOP + 70} ${rx - 60},${ry + 120} ${rx + 20},${ry + 40}" fill="none" stroke="${ink}" stroke-width="40"/>` +
      `<path d="M${sx + 30},${TOP + 16} C${sx + 220},${TOP + 70} ${rx - 60},${ry + 120} ${rx + 20},${ry + 40}" fill="none" stroke="#FBF6E6" stroke-width="32"/>` +
      `<g transform="rotate(-3 ${rx} ${ry})"><rect x="${rx}" y="${ry}" width="320" height="190" fill="#FBF6E6" stroke="${ink}" stroke-width="4"/>` +
      H.label(rx + 160, ry + 38, 26, "RECEIPT") +
      `<text x="${rx + 16}" y="${ry + 92}" font-family="Oswald" font-weight="600" font-size="25" fill="${ink}">WAR ....... $170,000,000,000,000</text>` +
      `<text x="${rx + 16}" y="${ry + 140}" font-family="Oswald" font-weight="600" font-size="25" fill="${ink}">CLINICAL TRIALS ......... $0.00</text></g>`;
    // the right pan stuck high: the crate on it and the scientist on the crate, holding her flask down toward YOU
    const R = [sx + s * 84 * Math.cos(a), TOP + s * (-150 + 84 * Math.sin(a) + 64)];
    const cw = 210, ch = 92;
    const crate = `<rect x="${R[0] - cw / 2}" y="${R[1] - ch}" width="${cw}" height="${ch}" fill="#C99A5E" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M${R[0] - cw / 2},${R[1] - ch} L${R[0] + cw / 2},${R[1]} M${R[0] + cw / 2},${R[1] - ch} L${R[0] - cw / 2},${R[1]}" stroke="#9C6B3F" stroke-width="5" opacity="0.55"/>` +
      `<rect x="${R[0] - cw / 2 + 12}" y="${R[1] - ch / 2 - 20}" width="${cw - 24}" height="40" fill="#C99A5E"/>` +
      `<text x="${R[0]}" y="${R[1] - ch / 2 + 11}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="30" fill="${ink}">38,000 YEARS</text>`;
    // mirrored, so her flask hand is on YOU's side
    const SCI = K.castOpts("scientist", { mood: "worried" });
    const sci = `<g transform="matrix(-1,0,0,1,${f(2 * (R[0] + 10))},0)">${man(H, SCI, R[0] + 10, R[1] - ch, 1.15)}</g>`;
    const svg = plate(HZ) + pol + counter + scale + mount + sold + crate + sci + man(H, YOUo, yx, yf, yk) + receipt;
    return { svg, alt: "The checkout: the brass scale on the counter tipped hard to the left, a mountain of war money on the low pan with a red SOLD tag and the politician's hand pressing it down; the right pan stuck high with the 38,000 YEARS crate on it and the scientist on top, holding her flask out toward YOU, far out of reach; YOU in his bowler holds up a long receipt reading WAR $170,000,000,000,000 and CLINICAL TRIALS $0.00." };
  },

  "stopped-in-1900"(H, id) {
    const { K, C } = H;
    const HZ = 380, ink = C.line, FEET = 760;
    // the road forks at the signpost; the left road up to the left, the right road up to the right
    const road = (d) => `<path d="${d}" fill="none" stroke="${EDGE}" stroke-width="250"/><path d="${d}" fill="none" stroke="${ROAD}" stroke-width="230"/>`;
    const roads = road(`M960,1140 L960,940 Q960,820 520,${FEET - 40} L-200,600`) + road(`M960,1140 L960,940 Q960,820 1400,${FEET - 40} L2100,600`);
    const post = H.at(960, 1010, 2.1, K.props.sign({ text: "1900", posts: 1, height: 60 }));
    // the life candles: the same height to start with; the right one bitten short and snuffed
    const candle = (x, feet, h, lit) => `<rect x="${x - 26}" y="${feet - h}" width="52" height="${h}" fill="${C.cream}" stroke="${ink}" stroke-width="5"/><path d="M${x},${feet - h} v-14" stroke="${ink}" stroke-width="4"/>` +
      (lit ? H.at(x, feet - h - 12, 0.4, K.flames(0, 0, 1)) : wisps(x - 6, feet - h - 16, 2, 0.9)) +
      `<rect x="${x - 42}" y="${feet - 12}" width="84" height="16" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/>`;
    // left road: the fat cat hugging his tall stack, leaning over to light his cigar off his candle
    const FAT = K.castOpts("richHuman", { look: "right", mood: "smug" });
    const fk = 2.5, fx = 430;
    const mouth = onCanvas(K.rig(FAT).mouth, fx, FEET, fk), CH = FEET - mouth[1] + 8;
    let stack = "";
    for (let i = 0; i < 22; i++) stack += H.at(250 + (i % 2) * 6, FEET - 20 - i * 22, 1.15, `<g transform="scale(1,0.5)">${K.money("plain", 0)}</g>`);
    stack += `<path d="M206,${FEET - 20 - 22 * 22 + 4} l20,-8 l14,6 l18,-10 l20,8 l14,-4 V${FEET - 20 - 22 * 22 + 18} H206 Z" fill="${C.money}" stroke="${ink}" stroke-width="3"/>`;
    const bigCheck = H.at(560, 170, 1, `<rect x="-180" y="-52" width="360" height="100" fill="${C.money}" stroke="${ink}" stroke-width="5"/><rect x="-170" y="-42" width="340" height="80" fill="none" stroke="${C.moneyDark}" stroke-width="3"/>` + H.label(0, 22, 50, "$333,636 / YEAR", "middle", C.line));
    // right road: the skeleton in the bowler, one paper, the bitten stub, his small paycheck held out, his jaw on the road
    const BONES = copy(YOU, { arms: [[-10, -4], [150, 170]] });
    const bk = 2.5, bxp = 1400;
    const hB = handAt(H, BONES, bxp, FEET, bk, 1);
    const smallCheck = H.at(hB[0] + 150, hB[1] - 30, 1, `<rect x="-150" y="-44" width="300" height="84" fill="${C.money}" stroke="${ink}" stroke-width="5"/>` + H.label(0, 16, 42, "$14,375 / YEAR", "middle", C.line));
    const oneBill = H.at(1200, FEET - 20, 1.15, `<g transform="scale(1,0.5)">${K.money("plain", 0)}</g>`);
    const jaw = `<path d="M1440,${FEET + 2} l30,-4 l26,4 l-4,10 l-46,2 Z" fill="#F1EAD6" stroke="${ink}" stroke-width="3"/>`;
    const svg = plate(HZ) + roads + post +
      stack + candle(fx + 120, FEET + 6, CH, true) + man(H, FAT, fx, FEET, fk) + bigCheck +
      candle(1690, FEET + 6, CH * 0.62, false) + oneBill + man(H, copy(BONES, { skeleton: true }), bxp, FEET, bk) + jaw + smallCheck;
    return { svg, alt: "The fork at the 1900 signpost: on the left road YOU is the fat cat in a top hat beside a stack of papers twice his height, lighting his cigar off his lit life candle, under his paycheck $333,636 / YEAR; on the right road his grinning skeleton in the bowler holds out $14,375 / YEAR beside one paper and a bitten, snuffed candle stub, his jaw on the road." };
  },

  "604-times-less"(H, id) {
    const { K, C } = H;
    const HZ = 520, FLOOR = 860, ink = C.line;
    // the toppled stack: a long heap of war papers lying across the field and off to the right
    let heap = "";
    for (let i = 0; i < 48; i++) {
      const x = 420 + i * 34 + (i % 3) * 7, y = FLOOR - 26 - ((i * 7) % 5) * 10 - (i > 2 ? 34 : 0) * ((i % 2) + 0.5);
      heap += H.at(x, y, 1.25, K.money("war", 0), ((i * 37) % 50) - 25);
    }
    // one little arm waving weakly out of the heap, and the dented hard hat rolled clear
    const arm = `<path d="M560,${FLOOR - 80} L574,${FLOOR - 170} L606,${FLOOR - 222}" fill="none" stroke="${ink}" stroke-width="8" stroke-linecap="round" stroke-linejoin="miter"/>` +
      `<path d="M606,${FLOOR - 222} l-6,-20 M606,${FLOOR - 222} l8,-19 M606,${FLOOR - 222} l18,-8" stroke="${ink}" stroke-width="6" stroke-linecap="round"/>` +
      `<path d="M630,${FLOOR - 250} q16,10 12,28 M578,${FLOOR - 254} q-16,12 -10,30" fill="none" stroke="${ink}" stroke-width="3"/>`;
    const hat = `<g transform="translate(250,${FLOOR - 4}) rotate(-18)"><path d="M-60,0 L-48,-44 L-6,-60 L8,-46 L20,-62 L48,-44 L60,0 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      `<path d="M-76,4 L-66,-8 H66 L76,4 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/><path d="M-6,-58 l12,18 l10,-18" fill="none" stroke="${ink}" stroke-width="3"/></g>`;
    const medCorner = H.at(520, FLOOR - 24, 1.25, K.money("med", 0), 8);
    const clouds = puffs(C, [[300, 160, 50], [380, 140, 64], [460, 165, 46], [1400, 120, 44], [1470, 100, 58], [1540, 126, 42]]);
    const svg = plate(HZ) + clouds + medCorner + heap + arm + hat;
    return { svg, alt: "The 604 stack has toppled across the field into a long heap of war money running off the frame; one little arm waves weakly out of it, the medicine paper's cross seal peeking from underneath, and its dented yellow hard hat has rolled clear." };
  },

  "odds-of-dying"(H, id) {
    const { K, C } = H;
    const HZ = 440, FLOOR = 900, ink = C.line, WY = 590, WR = 160;
    // a booth: a striped stall, a marquee on top, a prize wheel in it (slots: its wheel's markings)
    const booth = (cx, w, name, lit, slots) => {
      const x0 = cx - w / 2, stripes = Array.from({ length: 8 }, (_, i) => `<rect x="${x0 + (i * w) / 8}" y="360" width="${w / 16}" height="${FLOOR - 360}" fill="${C.cream}" opacity="0.9"/>`).join("");
      return `<rect x="${x0}" y="360" width="${w}" height="${FLOOR - 360}" fill="${C.rust}" stroke="${ink}" stroke-width="7"/>` + stripes +
        `<rect x="${x0 - 30}" y="220" width="${w + 60}" height="150" fill="${C.navy}" stroke="${ink}" stroke-width="7"/>` +
        H.label(cx, 284, 56, name, "middle", C.cream) + H.label(cx, 350, 50, lit, "middle", C.yellow) +
        `<circle cx="${cx}" cy="${WY}" r="${WR}" fill="${C.cream}" stroke="${ink}" stroke-width="8"/>` + slots +
        `<circle cx="${cx}" cy="${WY}" r="20" fill="${C.yellow}" stroke="${ink}" stroke-width="5"/><path d="M${cx - 20},${WY - WR - 28} H${cx + 20} L${cx},${WY - WR + 12} Z" fill="${C.war}" stroke="${ink}" stroke-width="5"/>`;
    };
    // the disease wheel: twelve slots, every one of them YOU
    const RX = 1360;
    let ys = "";
    for (let i = 0; i < 12; i++) {
      const a = (i * 30 * Math.PI) / 180, ta = ((i * 30 + 15) * Math.PI) / 180, tx = RX + 104 * Math.sin(ta), ty = WY - 104 * Math.cos(ta);
      ys += `<path d="M${RX},${WY} L${f(RX + WR * Math.sin(a))},${f(WY - WR * Math.cos(a))}" stroke="${ink}" stroke-width="3"/>` +
        `<text x="${f(tx)}" y="${f(ty + 8)}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="24" fill="${C.war}" transform="rotate(${i * 30 + 15} ${f(tx)} ${f(ty)})">YOU</text>`;
    }
    // the terrorism wheel: thousands of blank slots and one red sliver
    const LX = 470;
    let blanks = "";
    for (let i = 0; i < 72; i++) { const a = (i * 5 * Math.PI) / 180; blanks += `<path d="M${LX},${WY} L${f(LX + WR * Math.sin(a))},${f(WY - WR * Math.cos(a))}" stroke="${ink}" stroke-width="1.1" opacity="0.55"/>`; }
    blanks += `<path d="M${LX},${WY} L${f(LX + WR * Math.sin(2.1))},${f(WY - WR * Math.cos(2.1))}" stroke="${C.war}" stroke-width="2.5"/>`;
    // its fortress: sandbags, barbed wire, a ring of grumpy missiles, the weapons maker on guard
    const sand = (x, y) => `<path d="M${x - 46},${y} Q${x - 50},${y - 34} ${x},${y - 36} Q${x + 50},${y - 34} ${x + 46},${y} Z" fill="${C.tan}" stroke="${ink}" stroke-width="5"/>`;
    let bags = "";
    for (let r = 0; r < 3; r++) for (let i = 0; i < 9; i++) bags += sand(110 + i * 88 + (r % 2) * 44, FLOOR + 10 - r * 34);
    let wire = "";
    for (let i = 0; i < 16; i++) wire += `<path d="M${90 + i * 50},${FLOOR - 112} l25,-14 l25,14 M${100 + i * 50},${FLOOR - 126} l8,8 M${108 + i * 50},${FLOOR - 126} l-8,8" fill="none" stroke="${ink}" stroke-width="3"/>`;
    const missiles = [150, 280, 660, 790].map((x) => H.at(x, FLOOR - 70, 1.05, K.props.missile({ mood: "grumpy" }))).join("");
    const WM = K.castOpts("weaponsMaker", { look: "right", mood: "cross", arms: [[40, 90], [-40, -90]] });
    const left = booth(LX, 560, "TERRORISM", "1 IN 30,000,000", blanks);
    const right = booth(RX, 560, "DISEASE", "100%", ys);
    const blob = H.at(1730, FLOOR, 1.6, K.props.diseaseBlob({ mood: "grin", arms: "steeple" }));
    const YOUo = copy(YOU, { look: "right", mood: "worried", light: "red" });
    const svg = plate(HZ) + left + missiles + wire + bags + man(H, WM, 900, FLOOR + 20, 2.0) + right + blob + man(H, YOUo, 1250, FLOOR + 50, 2.5);
    return { svg, alt: "The HOLD at the midway: on the right the DISEASE booth's wheel, every slot reading YOU, stopped under its marquee 100%, YOU alone in front of it with his chest light red and a grinning disease blob at the wheel; on the left the TERRORISM booth, 1 IN 30,000,000, behind sandbags, barbed wire and grumpy missiles, the weapons maker on guard." };
  },

  "cancer-oil-reserves"(H, id) {
    const { K, C } = H;
    const HZ = 460, FLOOR = 880, ink = C.line;
    const cracks = `<path d="M0,700 l120,20 l60,-30 l140,40 M400,960 l90,-50 l120,10 l70,-60 M1300,760 l110,30 l50,-40 l160,20 M1100,1000 l80,-60 l140,10" fill="none" stroke="${CRACK}" stroke-width="5"/>`;
    // the charred cancer blob, blinking, Part 8's little derrick still pumping on its head (no gusher)
    const bx = 1080, bk = 2.7;
    const blob = H.at(bx, FLOOR, bk, K.burn(K.props.diseaseBlob({ mood: "cross", label: "CANCER", arms: "limp" })));
    const eyes = [[-24, -96], [18, -96]].map(([dx, dy]) => `<circle cx="${bx + dx * bk}" cy="${FLOOR + dy * bk}" r="14" fill="#FFFFFF" stroke="${ink}" stroke-width="3"/><circle cx="${bx + dx * bk + 3}" cy="${FLOOR + dy * bk}" r="6" fill="${ink}"/>`).join("");
    const dtop = FLOOR - 140 * bk;
    const lattice = [-300, -225, -150, -75].map((y) => {
      const w0 = 16 + 54 * (1 + y / 360), w1 = 16 + 54 * (1 + (y - 75) / 360);
      return `<path d="M${f(-w0)},${y} L${f(w1)},${y - 75} M${f(w0)},${y} L${f(-w1)},${y - 75} M${f(-w0)},${y} H${f(w0)}" stroke="#4A3B2C" stroke-width="4"/>`;
    }).join("");
    const derrick = H.at(bx - 10, dtop + 14, 0.72, `<path d="M-70,0 L-16,-360 H16 L70,0" fill="none" stroke="${ink}" stroke-width="11" stroke-linejoin="miter"/>` +
      `<path d="M-70,0 L-16,-360 H16 L70,0" fill="none" stroke="#4A3B2C" stroke-width="5"/>` + lattice +
      `<path d="M-22,-360 H22 V-376 H-22 Z" fill="${C.slate}" stroke="${ink}" stroke-width="3"/><rect x="-92" y="-12" width="184" height="16" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>`) +
      `<path d="M${bx - 70},${dtop - 150} l-16,-8 M${bx + 52},${dtop - 150} l16,-8" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`;
    // the pennant, planted in its head beside the derrick
    const poleX = bx + 120, poleTop = dtop - 230;
    const pennant = `<path d="M${poleX},${dtop + 60} V${poleTop}" stroke="${ink}" stroke-width="12"/><path d="M${poleX},${dtop + 60} V${poleTop}" stroke="${C.tan}" stroke-width="5"/>` +
      `<path d="M${poleX},${poleTop} L${poleX + 330},${poleTop + 46} L${poleX},${poleTop + 100} Z" fill="${C.line}" stroke="${C.line}" stroke-width="8" stroke-linejoin="miter"/><path d="M${poleX},${poleTop} L${poleX + 330},${poleTop + 46} L${poleX},${poleTop + 100} Z" fill="${C.cream}"/>` +
      `<text x="${poleX + 22}" y="${poleTop + 60}" font-family="Oswald" font-weight="600" font-size="38" fill="${C.war}" transform="rotate(4 ${poleX + 22} ${poleTop + 60})">CURED: 2003</text>`;
    // the army helmet: the kit's hard hat, in olive drab
    const OLIVE = "#7A7A4A";
    const helmet = (svg) => svg.replace(/(<path d="M-2[23],-17 [^"]*" )fill="[^"]*"/, `$1fill="${OLIVE}"`).replace(/(<path d="M-(?:29|30),-14 [^"]*" )fill="[^"]*"/, `$1fill="${OLIVE}"`);
    // the scientist, down off the tank, saluting the pennant she planted
    const SCI = K.castOpts("scientist", { hat: "hard", look: "left", mood: "eager", arms: [[-10, -4], [-150, -215]] });
    const sci = H.at(1620, FLOOR - 100 * 2.3, 2.3, helmet(K.person(SCI)));
    // the tank, skidded to a stop on the left on locked treads, the leash tied round its barrel, her flask fixed on
    // the end of it like a bayonet, two soldiers' helmets peeking out of the hatch
    const TX = 290;
    const peek = (x) => `<path d="M${x - 30},-238 Q${x - 28},-278 ${x},-280 Q${x + 28},-278 ${x + 30},-238 Z" fill="${OLIVE}" stroke="${ink}" stroke-width="5"/><path d="M${x - 38},-238 H${x + 38}" stroke="${ink}" stroke-width="6"/>` +
      `<circle cx="${x - 10}" cy="-225" r="7" fill="#FFFFFF" stroke="${ink}" stroke-width="2"/><circle cx="${x + 10}" cy="-225" r="7" fill="#FFFFFF" stroke="${ink}" stroke-width="2"/><circle cx="${x - 7}" cy="-225" r="3" fill="${ink}"/><circle cx="${x + 13}" cy="-225" r="3" fill="${ink}"/>`;
    const tank = puffs(C, [[TX - 215, FLOOR - 70, 34], [TX - 250, FLOOR - 36, 26], [TX - 190, FLOOR - 104, 22]], PUFF) + `<g transform="translate(${TX},${FLOOR})">` +
      `<path d="M-230,0 Q-250,-40 -210,-60 H210 Q250,-40 230,0 Z" fill="${C.slate}" stroke="${ink}" stroke-width="7"/>` +
      [-170, -85, 0, 85, 170].map((x) => `<circle cx="${x}" cy="-30" r="24" fill="${C.peri}" stroke="${ink}" stroke-width="5"/>`).join("") +
      `<path d="M-190,-60 L-160,-150 H160 L190,-60 Z" fill="${OLIVE}" stroke="${ink}" stroke-width="7"/><path d="M-90,-150 Q-80,-212 0,-216 Q80,-212 90,-150 Z" fill="${OLIVE}" stroke="${ink}" stroke-width="7"/>` +
      `<ellipse cx="0" cy="-214" rx="64" ry="10" fill="${ink}"/>` + peek(-28) + peek(32) +
      `<rect x="60" y="-196" width="300" height="26" fill="${OLIVE}" stroke="${ink}" stroke-width="6"/>` +
      `<path d="M300,-198 q8,16 0,30 M312,-198 q8,16 0,30" fill="none" stroke="${C.war}" stroke-width="5"/>` +
      `<g transform="translate(372,-183) rotate(90)"><path d="M-6,-34 H6 V-18 L20,8 H-20 L-6,-18 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="4"/><path d="M-14,-2 H14 L19,7 H-19 Z" fill="${C.med}"/></g></g>` +
      // the skid: two tread marks dragged across the desert behind it, and the dust it kicked up
      `<path d="M-40,${FLOOR + 8} H${TX - 236} M-40,${FLOOR + 22} H${TX - 236}" stroke="${CRACK}" stroke-width="9" stroke-dasharray="22 10"/>`;
    // Part 8's leashed missile, sitting up at the blob's feet without a scorch on it, wagging its fins; its red
    // leash (Part 8's) runs back to the tank's barrel
    const MX = 800, MF = FLOOR + 40, mk = 1.45;
    const missile = H.at(MX, MF, mk, `<g transform="rotate(-8)">${K.props.missile({ mood: "grin", arms: "none", look: "right" })}` +
      `<rect x="-29" y="-62" width="58" height="8" fill="${C.war}" stroke="${ink}" stroke-width="2.4"/><circle cx="-22" cy="-54" r="5" fill="none" stroke="${ink}" stroke-width="2.4"/></g>` +
      `<path d="M-64,-30 q-12,-14 -6,-30 M64,-30 q12,-14 6,-30 M-74,-8 q-14,-6 -14,-20 M74,-8 q14,-6 14,-20" fill="none" stroke="${ink}" stroke-width="3" stroke-linecap="round"/>`);
    const leash = `<path d="M${TX + 306},${FLOOR - 172} C${TX + 330},${FLOOR - 40} ${MX - 120},${FLOOR - 10} ${MX - 42},${MF - 73}" fill="none" stroke="${C.war}" stroke-width="5"/>`;
    const svg = plate(HZ, DESERT_SKY, DESERT) + cracks + tank + derrick + blob + eyes + pennant + leash + missile + sci;
    return { svg, alt: "In the cracked desert the cancer blob sits charred black and blinking, CANCER on its sash, Part 8's little oil derrick still pumping on its head; a pennant reading CURED: 2003 is planted beside the derrick and the scientist in an army helmet salutes it; at the blob's feet the smiling missile sits up wagging its fins, not a scorch on it, its red leash running back to the barrel of the tank skidded to a stop on the left, her flask fixed on the barrel's end like a bayonet and two soldiers' helmets peeking out of the hatch." };
  },

  "submarine-on-land"(H, id) {
    const { K, C } = H;
    const HZ = 420, ink = C.line;
    const cracks = `<path d="M0,620 l140,30 l80,-30 l160,40 l90,-20 M220,940 l110,-50 l140,20 l90,-60 M1200,700 l140,30 l60,-40 l180,30 l120,-10 M1260,980 l90,-70 l160,20" fill="none" stroke="${CRACK}" stroke-width="5"/>`;
    const funnel = H.at(1580, 560, 1.1, K.props.colorFlipFunnel({ outN: 0 }));
    // the puddle, and the submarine's stern sticking up out of it at a slant: the hull, the cross of fins, the propeller
    const px = 860, py = 800;
    const puddle = `<ellipse cx="${px}" cy="${py}" rx="240" ry="58" fill="${WATER}" stroke="${ink}" stroke-width="6"/><ellipse cx="${px - 80}" cy="${py - 16}" rx="70" ry="12" fill="${GLINT}" opacity="0.7"/>`;
    const hull = `<path d="M-80,30 L-80,-150 Q-78,-260 0,-330 Q78,-260 80,-150 L80,30 Z" fill="${C.peri}" stroke="${ink}" stroke-width="7"/>` +
      `<path d="M56,20 L56,-160 Q54,-240 6,-300" fill="none" stroke="${C.cream}" stroke-width="5" opacity="0.6"/>` +
      [-110, -60, -10].map((y) => [-50, -16, 18, 52].map((x) => `<circle cx="${x}" cy="${y}" r="4" fill="${ink}"/>`).join("")).join("") +
      `<path d="M-14,-250 L-22,-390 L22,-390 L14,-250 Z" fill="${C.slate}" stroke="${ink}" stroke-width="6"/>` +
      `<path d="M-74,-230 L-190,-200 L-190,-170 L-76,-180 Z M74,-230 L190,-200 L190,-170 L76,-180 Z" fill="${C.slate}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
      `<rect x="-8" y="-430" width="16" height="44" fill="${ink}"/>` +
      `<g transform="translate(0,-432)"><path d="M0,0 C-80,-34 -100,12 -10,8 Z M0,0 C80,-34 100,12 10,8 Z M0,0 C-20,-70 20,-70 0,0 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="5"/><circle r="13" fill="${C.orange}" stroke="${ink}" stroke-width="4"/></g>` +
      `<path d="M-70,-470 q-24,-12 -44,0 M70,-470 q24,-12 44,0 M-46,-500 q-16,-12 -32,-6" fill="none" stroke="${ink}" stroke-width="4"/>`;
    const sub = `<g transform="translate(${px + 30},${py + 4}) rotate(-28) scale(0.9)">${hull}</g>` +
      `<path d="M${px - 160},${py - 4} q34,-20 68,0 q34,-20 68,0 M${px + 110},${py + 6} q24,-14 48,0" fill="none" stroke="${GLINT}" stroke-width="5"/>` +
      [[px - 40, py - 70], [px + 150, py - 60], [px - 120, py - 40]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="7" fill="${GLINT}" stroke="${ink}" stroke-width="2"/>`).join("");
    // YOU flat on his face beside it, his bowler rolling away
    const YOUo = copy(YOU, { look: "right", mood: "worried", hat: null, arms: [[150, 170], [160, 175]] });
    const you = H.at(1290, 870, 2.4, K.person(YOUo), -90);
    const hat = `<g transform="translate(1560,890) rotate(20) scale(2.4)"><path d="M-17,1 L-13,-16 L0,-21 L13,-16 L17,1 Z" fill="${ink}"/><path d="M-28,4 L-22,-1 H22 L28,4 Z" fill="${ink}"/></g>` +
      `<path d="M1450,880 q30,-20 60,-4 M1180,700 l-14,-22 M1220,690 l2,-26 M1260,700 l14,-22" fill="none" stroke="${ink}" stroke-width="4"/>`;
    const svg = plate(HZ, DESERT_SKY, DESERT) + cracks + funnel + puddle + sub + you + hat;
    return { svg, alt: "In the dry, cracked desert a submarine's stern, fins and spinning propeller stick up out of a small puddle; YOU lies flat beside it where he tripped, his bowler rolling away; the color-flip funnel stands far behind." };
  },

  periscope(H, id) {
    const { K, C } = H;
    const S = K.STUDIO, ink = C.line;
    const mx = 958, my = 800, rim = my - 98;
    // the periscope up out of the coffee, its head turned to look at her
    const scope = `<path d="M${mx},${rim + 10} V${rim - 70}" stroke="${ink}" stroke-width="26"/><path d="M${mx},${rim + 10} V${rim - 70}" stroke="${C.slate}" stroke-width="16"/>` +
      `<path d="M${mx + 16},${rim - 62} V${rim - 100} H${mx - 74} V${rim - 62} Z" fill="${C.slate}" stroke="${ink}" stroke-width="6" stroke-linejoin="miter"/>` +
      `<rect x="${mx - 88}" y="${rim - 98}" width="16" height="34" fill="${GLINT}" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M${mx + 12},${rim - 44} l8,14 M${mx - 12},${rim - 24} l-6,14" stroke="#6B4A2F" stroke-width="5" stroke-linecap="round"/>` +
      `<circle cx="${mx + 20}" cy="${rim - 20}" r="5" fill="#6B4A2F"/><path d="M${mx - 30},${rim} q14,-10 28,0 q14,-10 28,0" fill="none" stroke="#6B4A2F" stroke-width="5"/>`;
    const svg = H.K.studioWall() + crack(C, 1220, 700) + H.wish(S.wish.x, S.wish.y, S.wish.w, "sideeye-closed", "arms-crossed") + K.lectern() + mug(C, mx, my, 1.15, true) + scope;
    return { svg, alt: "Wishonia at the lectern side-eyes a periscope that has risen out of her chipped coffee mug and turned to look at her; the crack from the quake still zigzags up the wall behind her." };
  },
};
