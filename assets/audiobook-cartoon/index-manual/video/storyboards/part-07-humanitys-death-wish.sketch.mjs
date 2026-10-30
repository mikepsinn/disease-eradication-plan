// Sketches for storyboards/part-07-humanitys-death-wish.md: each scene's key moment on a 1920 x 1080 frame, in the
// 1950s atomic-age film look (cartoon-style-bible.md section 1), drawn with the production art: H.K is the kit with
// film.js and the props library loaded, H.C the palette, H.host(head, body, front) a whole host shot.
// Built into the review sheet by tools/storyboard-sheet.mjs. Nothing important below y 900 (16:9 captions keep-out).

const f1 = (n) => (Math.round(n * 10) / 10).toString();

// The tourist (the part's spine): an everyday human, the same options in every scene that draws him.
const TOURIST = { tone: 1, outfit: "shirt", color: 3, seed: 7 };
const copy = (a, b) => Object.assign({}, a, b || {});

// His camera on a rust strap at his chest and the audio-guide handset on an orange lanyard (person units).
// Charred, the gear is charred with him.
function gear(K, C, o) {
  const burnt = o.charred, ink = C.line, soot = "#3A2A22";
  const col = (c) => (burnt ? "#4A3A30" : c);
  const R = K.rig(o), sy = R.shoulder[0][1];
  const m = K.person(o).match(/class="chest-light" cx="([-\d.]+)" cy="([-\d.]+)"/);
  const L = m ? [+m[1], +m[2]] : [0, sy + 20];
  const cx = L[0] + (o.look === "left" ? -20 : 20), cy = L[1] + 16;
  const strap = `<path d="M-7,${f1(sy - 8)} L${f1(cx - 8)},${f1(cy - 6)} M7,${f1(sy - 8)} L${f1(cx + 8)},${f1(cy - 6)}" fill="none" stroke="${burnt ? soot : C.rust}" stroke-width="2.2"/>`;
  const cam = `<rect x="${f1(cx - 11)}" y="${f1(cy - 7)}" width="22" height="14" fill="${col(C.slate)}" stroke="${ink}" stroke-width="2.2"/>` +
    `<rect x="${f1(cx - 7)}" y="${f1(cy - 10)}" width="8" height="3" fill="${col(C.tan)}" stroke="${ink}" stroke-width="1.6"/>` +
    `<circle cx="${f1(cx + 2)}" cy="${f1(cy)}" r="4.6" fill="${col(C.peri)}" stroke="${ink}" stroke-width="2"/><circle cx="${f1(cx + 2)}" cy="${f1(cy)}" r="1.8" fill="${burnt ? "#5A4A40" : C.cream}"/>`;
  const hx = L[0] - (o.look === "left" ? -12 : 12), hy = sy + 30;
  const guide = `<path d="M-4,${f1(sy - 9)} L${f1(hx)},${f1(hy - 9)}" fill="none" stroke="${burnt ? soot : C.orange}" stroke-width="1.6"/>` +
    `<g transform="translate(${f1(hx)},${f1(hy)}) rotate(-6)"><rect x="-4.2" y="-9" width="8.4" height="18" fill="${col("#2A3550")}" stroke="${ink}" stroke-width="2"/>` +
    `<path d="M-2,-6 H2 M-2,-3.5 H2 M-2,-1 H2" stroke="${burnt ? "#5A4A40" : C.cream}" stroke-width="1.1"/><circle cx="0" cy="4.5" r="1.8" fill="${col(C.orange)}"/></g>`;
  return strap + cam + guide;
}
// The tourist with his gear (the gear goes under his arms).
function tourist(K, C, extra) {
  const o = copy(TOURIST, extra);
  const s = K.person(o);
  return s.includes('<g class="arm-l">') ? s.replace('<g class="arm-l">', gear(K, C, o) + '<g class="arm-l">') : s + gear(K, C, o);
}

// The smiling baby missile (Part 2's money-loop), pointing +x, around (0, 0), about 74 long.
function babyMissile(C) {
  const ink = C.line;
  return `<g transform="translate(-2,0)"><path d="M-34,-7 L14,-7 L30,0 L14,7 L-34,7 Z" fill="${C.war}" stroke="${ink}" stroke-width="2.6" stroke-linejoin="round"/>` +
    `<path d="M-34,-7 L-44,-17 L-40,-7 Z M-34,7 L-44,17 L-40,7 Z" fill="${C.war}" stroke="${ink}" stroke-width="2.4" stroke-linejoin="round"/>` +
    `<path d="M14,-7 L30,0 L14,7 Z" fill="${C.cream}" stroke="${ink}" stroke-width="2"/>` +
    `<path d="M-4,2 Q2,6 8,2" fill="none" stroke="${ink}" stroke-width="1.8" stroke-linecap="round"/><circle cx="-2" cy="-2.5" r="1.6" fill="${ink}"/><circle cx="6" cy="-2.5" r="1.6" fill="${ink}"/></g>`;
}

// A four-point sparkle.
function sparkle(K, x, y, r, col) { return K.star(x, y, r, col, 4); }

// A puff of soot (canvas px).
function soot(x, y, r) {
  return `<g opacity="0.75"><circle cx="${x}" cy="${y}" r="${r}" fill="#4B4440"/><circle cx="${x + r * 0.8}" cy="${y - r * 0.5}" r="${r * 0.7}" fill="#5B5450"/><circle cx="${x - r * 0.7}" cy="${y - r * 0.4}" r="${r * 0.6}" fill="#3E3834"/></g>`;
}

// A white dove perched, facing right, around its feet (0, 0), about 46 long.
function dove(C) {
  const ink = C.line, W = "#FBF6E6";
  return `<path d="M-22,-14 L-6,-22 L10,-24 L18,-30 L26,-28 L30,-24 L22,-20 L18,-12 L4,-4 L-12,-6 L-26,-2 Z" fill="${W}" stroke="${ink}" stroke-width="2.4" stroke-linejoin="miter"/>` +
    `<path d="M-8,-20 L2,-36 L10,-22" fill="${W}" stroke="${ink}" stroke-width="2.2" stroke-linejoin="miter"/>` +
    `<path d="M30,-25 L36,-24 L30,-22 Z" fill="${C.orange}" stroke="${ink}" stroke-width="1.4"/><circle cx="23" cy="-26" r="1.6" fill="${ink}"/>` +
    `<path d="M2,-4 L0,0 M8,-5 L8,0" stroke="${C.orange}" stroke-width="2"/>`;
}

// A claw hammer, its grip at (0, 0), the handle along -y, about 110 long (person units).
function hammer(C) {
  const ink = C.line;
  return `<path d="M-3.5,6 L3.5,6 L3,-84 L-3,-84 Z" fill="#B07A45" stroke="${ink}" stroke-width="2" stroke-linejoin="miter"/>` +
    `<path d="M-6,-84 L22,-86 L24,-98 L-6,-100 Z" fill="#8E9AAE" stroke="${ink}" stroke-width="2.2" stroke-linejoin="miter"/>` +
    `<path d="M-6,-86 L-18,-80 L-24,-92 L-6,-98 Z" fill="#8E9AAE" stroke="${ink}" stroke-width="2.2" stroke-linejoin="miter"/>` +
    `<path d="M-2,-98 H18" stroke="${C.cream}" stroke-width="1.4" opacity="0.8"/>`;
}

// A cream diner mug with the film's atom on it, centered on (0, 0), about 120 x 130 (canvas px).
function mug(K, C) {
  const ink = C.ink;
  return `<path d="M50,-28 C86,-30 88,26 48,26" fill="none" stroke="${ink}" stroke-width="22"/><path d="M50,-28 C86,-30 88,26 48,26" fill="none" stroke="${C.cream}" stroke-width="12"/>` +
    `<path d="M-56,-62 L56,-62 L50,58 Q0,70 -50,58 Z" fill="${C.cream}" stroke="${ink}" stroke-width="6" stroke-linejoin="round"/>` +
    `<ellipse cx="0" cy="-62" rx="56" ry="12" fill="#5B3A22" stroke="${ink}" stroke-width="6"/>` + K.atom(0, 6, 30, C.rust);
}

export default {
  "death-wish-title"(H, fid) {
    const { K, C } = H;
    // the emblem: three orbits round an orange nucleus, a war paper running round each one (KIT.titleScene's)
    const E = { at: [960, 300], rx: 200, ry: 62, k: 0.62 }, TILT = [0, 60, -60];
    let emblem = TILT.map((a) => `<ellipse cx="${E.at[0]}" cy="${E.at[1]}" rx="${E.rx}" ry="${E.ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${E.at[0]} ${E.at[1]})"/>`).join("");
    emblem += TILT.map((a, i) => {
      const th = i * 2.1 + 1.25 * 2.4, ex = E.rx * Math.cos(th), ey = E.ry * Math.sin(th), r = (a * Math.PI) / 180;
      const x = E.at[0] + ex * Math.cos(r) - ey * Math.sin(r), y = E.at[1] + ex * Math.sin(r) + ey * Math.cos(r);
      return H.at(f1(x), f1(y - 6), E.k, K.money("war", i % 2));
    }).join("");
    emblem += `<circle cx="960" cy="300" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="951" cy="291" r="8" fill="${C.yellow}"/>`;
    // the falling star's sparkle trail, from high on the right down to the missile over WISH
    const path = [[1800, 70], [1700, 150], [1610, 250], [1540, 350], [1490, 440], [1455, 520]];
    const trail = path.map(([x, y], i) => sparkle(K, x, y, 10 + i * 4, i % 2 ? C.yellow : C.cream) + `<circle cx="${x + 26}" cy="${y - 18}" r="${2 + i * 0.6}" fill="${C.yellow}"/>`).join("") +
      `<path d="M1800,70 Q1560,280 1440,560" fill="none" stroke="${C.yellow}" stroke-width="5" stroke-dasharray="4 16" stroke-linecap="round" opacity="0.8"/>`;
    // the missile, still glowing like a star at its tail, nosing down at the top of WISH
    const mis = `<g transform="translate(1418,610) rotate(116) scale(2.4)">${babyMissile(C)}</g>` + sparkle(K, 1448, 548, 34, C.yellow);
    const heading = H.big(960, 637, 100, "HUMANITY'S", "middle", C.cream) + H.big(960, 833, 200, "DEATH WISH", "middle", C.cream);
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + emblem + trail + mis + heading;
    return { svg, alt: "The period title card: HUMANITY'S DEATH WISH in cream on navy under the atom emblem whose electrons are running war papers; a falling star has grown fins and a grin and dives as a smiling missile at the top of WISH, trailing sparkles." };
  },

  "host-knows"(H, fid) {
    const { K, C } = H;
    // the tourist at the right of the lectern, facing her: the hammer raised in his far hand, a thumbs-up in the near one
    const k = 3.3, fx = 1420, feet = 1066;
    const o = copy(TOURIST, { look: "left", mood: "grin", arms: [[-30, -160], [150, 196]] });
    const R = K.rig(o);
    const hand = R.hand[1], top = R.top;
    const ham = `<g transform="translate(${f1(hand[0])},${f1(hand[1])}) rotate(-38)">${hammer(C)}</g>`;
    const SK = "#D9B48F";
    const thumb = `<g transform="translate(${f1(R.hand[0][0])},${f1(R.hand[0][1])})"><path d="M-6,-5 L6,-6 L8,6 L-5,8 L-8,2 Z" fill="${SK}" stroke="${C.line}" stroke-width="1.8" stroke-linejoin="miter"/>` +
      `<path d="M-1,-5 L-3,-17 L2,-18 L4,-6 Z" fill="${SK}" stroke="${C.line}" stroke-width="1.8" stroke-linejoin="miter"/><path d="M-4,0 H6 M-4,3.5 H6" stroke="${C.line}" stroke-width="1.2"/></g>`;
    // the bump: a faceted dome swelling out of his hair, three stars circling it
    const bx = top[0] + 1, by = top[1] + 3;
    const bump = `<path d="M${f1(bx - 13)},${f1(by + 2)} L${f1(bx - 11)},${f1(by - 9)} L${f1(bx - 5)},${f1(by - 16)} L${f1(bx + 5)},${f1(by - 16)} L${f1(bx + 11)},${f1(by - 9)} L${f1(bx + 13)},${f1(by + 2)} Z" fill="#E6B392" stroke="${C.line}" stroke-width="2" stroke-linejoin="miter"/>` +
      `<path d="M${f1(bx - 6)},${f1(by - 11)} l5,-2" stroke="#FBF6E6" stroke-width="2" stroke-linecap="round"/>`;
    const stars = [[-26, -16, 8], [2, -34, 7], [28, -14, 8]].map(([dx, dy, r]) => K.star(bx + dx, by + dy, r, C.yellow, 5)).join("") +
      `<ellipse cx="${f1(bx + 1)}" cy="${f1(by - 20)}" rx="32" ry="10" fill="none" stroke="${C.yellow}" stroke-width="1.4" stroke-dasharray="3 4"/>`;
    const man = H.at(fx, feet - 100 * k, k, tourist(K, C, o) + ham + thumb + bump + stars);
    const svg = H.host("smirk-smile", "shrug", man);
    return { svg, alt: "Host shot: Wishonia at her lectern shrugs with a smirk; beside her the tourist in a mustard shirt, camera and audio guide round his neck, grins with a bump swelling out of his hair and stars circling it, a hammer raised in one hand and a thumbs-up in the other." };
  },

  "museum-of-knowing"(H, fid) {
    const { K, C } = H;
    const ink = C.line;
    // the gallery: a plain wall over a parquet floor; the framing is the prize stage
    const WALL = "#E7D6AA", DADO = "#CDB27D", FLOOR = "#B47E52", FL = 870;
    let floor = `<rect y="${FL}" width="1920" height="${1080 - FL}" fill="${FLOOR}"/>`;
    for (let x = -60; x < 1980; x += 120) floor += `<path d="M${x},${FL} L${x - 80},1080" stroke="#8E6440" stroke-width="3" opacity="0.6"/>`;
    const room = `<rect width="1920" height="1080" fill="${WALL}"/><rect y="560" width="1920" height="${FL - 560}" fill="${DADO}"/><rect y="552" width="1920" height="14" fill="${C.rust}" stroke="${ink}" stroke-width="3"/>` +
      `<rect y="${FL - 18}" width="1920" height="18" fill="${C.slate}"/>` + floor;
    // the stage: a low platform, its top seen a little from above; the curtain rod and the fallen curtain behind
    const S0 = 560, S1 = 1660, TOPB = 690, TOPF = 760, FRONT = 846;
    const stage = `<path d="M${S0 + 30},${TOPB} H${S1 - 30} L${S1},${TOPF} H${S0} Z" fill="#9C6B43" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/>` +
      `<rect x="${S0}" y="${TOPF}" width="${S1 - S0}" height="${FRONT - TOPF}" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><path d="M${S0 + 6},${TOPF + 8} H${S1 - 6}" stroke="${C.orange}" stroke-width="3"/>` +
      [0, 1, 2, 3, 4].map((i) => `<path d="M${S0 + 40 + i * 255},${TOPF + 22} v52" stroke="${C.orange}" stroke-width="2" opacity="0.5"/>`).join("");
    const rod = `<rect x="${S0 + 10}" y="210" width="${S1 - S0 - 20}" height="14" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/>` +
      [S0 + 40, S1 - 40].map((x) => `<path d="M${x},224 l-10,40 M${x},224 l10,40" stroke="${ink}" stroke-width="3"/><circle cx="${x}" cy="270" r="9" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/>`).join("");
    let curtain = "";
    for (let i = 0; i < 9; i++) {
      const x0 = S0 + 50 + i * 120;
      curtain += `<path d="M${x0},${TOPB + 4} Q${x0 + 30},${TOPB - 70} ${x0 + 70},${TOPB - 30} Q${x0 + 100},${TOPB - 64} ${x0 + 130},${TOPB + 4} Z" fill="${i % 2 ? "#8E2F24" : "#A63A2C"}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>`;
    }
    // the Weapons Maker behind the check, hands still up from letting go, grinning round his cigar
    const kw = 2.5, wx = 1210;
    const wm = H.at(wx, TOPB + 30 - 100 * kw, kw, K.cast("weaponsMaker", { arms: [[-160, -195], [160, 195]], mood: "grin" }));
    // the giant check flat on the stage where the winner stood, seen a little from above
    const cx0 = 760, cx1 = 1480, cyb = 712, cyf = 780, sk = 26;
    const check = `<path d="M${cx0 + sk},${cyb} H${cx1 + sk} L${cx1},${cyf} H${cx0} Z" fill="${C.money}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      `<path d="M${cx0},${cyf} H${cx1} V${cyf + 14} H${cx0} Z" fill="${C.moneyEdge}" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M${cx0 + sk + 16},${cyb + 9} H${cx1 + sk - 18} L${cx1 - 14},${cyf - 9} H${cx0 + 12} Z" fill="none" stroke="${C.moneyDark}" stroke-width="2.5"/>` +
      `<g transform="translate(1100,${cyf - 18}) scale(1,0.42)">${H.label(0, 0, 92, "PAY TO: PEACE", "middle", C.moneyDark)}</g>` +
      `<g transform="translate(1400,${(cyb + cyf) / 2}) scale(1.7,0.6)">${K.moneySeal ? K.moneySeal("war", 0, 0, 14) : ""}</g>`;
    // her arm poking up out from under the front edge, the dove perched on one finger, waving weakly
    const skin = "#A87B57", hx = 1010, hy = cyf + 8;
    const hand = `<path d="M${hx - 13},${hy} L${hx - 20},${hy - 66} L${hx + 6},${hy - 70} L${hx + 13},${hy} Z" fill="${skin}" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/>` +
      `<path d="M${hx - 24},${hy - 64} L${hx + 10},${hy - 72} L${hx + 12},${hy - 96} L${hx - 22},${hy - 92} Z" fill="${skin}" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/>` +
      `<path d="M${hx - 3},${hy - 93} L${hx + 1},${hy - 126} L${hx + 11},${hy - 126} L${hx + 9},${hy - 95} Z" fill="${skin}" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/>` +
      `<path d="M${hx - 22},${hy - 90} L${hx - 32},${hy - 84} L${hx - 30},${hy - 74} L${hx - 22},${hy - 76}" fill="${skin}" stroke="${ink}" stroke-width="3" stroke-linejoin="miter"/>` +
      `<path d="M${hx - 44},${hy - 96} q-14,-12 -8,-28 M${hx + 40},${hy - 112} q14,-10 10,-28" fill="none" stroke="${ink}" stroke-width="3.4" stroke-linecap="round"/>` +
      H.at(hx + 4, hy - 122, 2.1, dove(C));
    // the charred tourist at the left, applauding, soot puffing off his hands
    const kt = 2.7, tx = 330, ty = 900 - 100 * kt;
    const to = { charred: true, look: "right", arms: [[89, 131], [-72, -198]] };
    const R = K.rig(copy(TOURIST, to));
    const clap = [tx + kt * (R.hand[0][0] + R.hand[1][0]) / 2, ty + kt * (R.hand[0][1] + R.hand[1][1]) / 2];
    const tour = H.at(tx, ty, kt, tourist(K, C, to)) +
      soot(clap[0] + 52, clap[1] - 30, 26) + soot(clap[0] + 10, clap[1] - 74, 20) + soot(clap[0] + 60, clap[1] - 110, 13) +
      `<path d="M${clap[0] + 30},${clap[1] + 20} l22,8 M${clap[0] + 34},${clap[1] + 2} l26,-2 M${clap[0] - 30},${clap[1] - 20} l-18,-12" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`;
    // the camera pushed in on the stage (the floor line stays at y 870)
    const svg = room + `<g transform="translate(-190,-160) scale(1.2)">` + rod + curtain + stage + wm + check + hand + "</g>" + `<g transform="translate(-120,0)">${tour}</g>`;
    return { svg, alt: "Museum plate, the prize stage: the curtain lies fallen behind the stage; the Weapons Maker grins round his cigar with his hands still up; at his feet the giant money-green check PAY TO: PEACE lies flat where the winner stood, and her hand pokes out from under its front edge with a white dove on one finger; at the left the charred tourist applauds, soot puffing off his hands." };
  },

  "lose-elaborately"(H, fid) {
    const { K, C } = H;
    const ink = C.line;
    // the living room, the camera pulled back: a cyan wall, a rust rail, a tan floor and an oval rug
    const FL = 800;
    const room = `<rect width="1920" height="1080" fill="${C.cyan}"/><rect y="${FL}" width="1920" height="${1080 - FL}" fill="${C.tan}"/>` +
      `<rect y="500" width="1920" height="12" fill="${C.rust}" stroke="${ink}" stroke-width="3"/><rect y="${FL - 14}" width="1920" height="14" fill="${C.slate}"/>` +
      `<ellipse cx="960" cy="880" rx="620" ry="70" fill="${C.rust}" stroke="${ink}" stroke-width="4"/><ellipse cx="960" cy="880" rx="560" ry="54" fill="none" stroke="${C.orange}" stroke-width="3"/>`;
    // the sofa on the left, the mantel and the bookcase on the right
    const sofa = `<path d="M60,${FL - 230} L470,${FL - 230} L480,${FL - 120} L50,${FL - 120} Z" fill="${C.orange}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/>` +
      `<path d="M30,${FL - 140} L500,${FL - 140} L500,${FL - 40} L30,${FL - 40} Z" fill="#C97A2E" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M20,${FL - 170} L70,${FL - 170} L70,${FL - 40} L20,${FL - 40} Z M460,${FL - 170} L510,${FL - 170} L510,${FL - 40} L460,${FL - 40} Z" fill="${C.orange}" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M50,${FL - 40} l-8,40 M480,${FL - 40} l8,40" stroke="${ink}" stroke-width="6"/>`;
    const mantel = `<rect x="1500" y="${FL - 300}" width="360" height="300" fill="#E9DDBB" stroke="${ink}" stroke-width="4"/><rect x="1590" y="${FL - 190}" width="180" height="190" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="1480" y="${FL - 318}" width="400" height="22" fill="${C.rust}" stroke="${ink}" stroke-width="4"/>`;
    // the dominoes: fallen along the table's left end, off the edge, across the floor and up a propped book onto the
    // sofa, where the falling front is tipping; the rest still stand along the sofa, along the mantel and round the room
    const dom = (x, y, a) => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(a)})"><rect x="-8" y="-40" width="16" height="40" fill="${C.cream}" stroke="${ink}" stroke-width="2.6"/><path d="M-8,-20 H8" stroke="${ink}" stroke-width="1.6"/><circle cx="0" cy="-29" r="2.2" fill="${ink}"/><circle cx="0" cy="-11" r="2.2" fill="${ink}"/></g>`;
    let dominoes = "";
    const TT = 640;
    for (let x = 790; x >= 690; x -= 20) dominoes += dom(x, TT, -76);
    dominoes += dom(652, 712, -128);
    for (let x = 630; x >= 330; x -= 25) dominoes += dom(x, 842, -78);
    // the propped book, a ramp from the floor up to the sofa seat
    const ramp = `<path d="M318,846 L214,662 L236,650 L342,836 Z" fill="${C.peri}" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/>`;
    for (let u = 0.1; u < 0.95; u += 0.2) dominoes += dom(322 - 100 * u, 838 - 180 * u, -105);
    dominoes += dom(196, FL - 140, -38) + dom(172, FL - 140, -12);
    for (let x = 148; x >= 84; x -= 24) dominoes += dom(x, FL - 140, 0);
    for (let x = 100; x <= 440; x += 24) dominoes += dom(x, FL - 230, 0);
    for (let x = 1510; x < 1870; x += 26) dominoes += dom(x, FL - 318, 0);
    // the card table, the lamp on its cord, the missile on its string right over the tiny Earth on START
    const LX = 905;
    const table = `<rect x="660" y="${TT}" width="600" height="20" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><path d="M690,${TT + 20} L670,${FL + 40} M1230,${TT + 20} L1250,${FL + 40} M760,${TT + 20} L770,${FL + 20} M1160,${TT + 20} L1150,${FL + 20}" stroke="${ink}" stroke-width="8"/>`;
    let track = "";
    const TC = [C.orange, C.yellow, C.peri, C.rust]; // Part 24's track colors
    for (let i = 0; i < 9; i++) track += `<rect x="${928 + i * 32}" y="${TT - 26}" width="30" height="14" fill="${TC[i % 5]}" stroke="${ink}" stroke-width="1.6"/>`;
    const board = `<path d="M850,${TT - 4} L1240,${TT - 4} L1222,${TT - 40} L868,${TT - 40} Z" fill="${C.orange}" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/>` +
      `<path d="M862,${TT - 9} L1228,${TT - 9} L1212,${TT - 35} L878,${TT - 35} Z" fill="${C.cream}" stroke="${ink}" stroke-width="2"/>` + track +
      `<rect x="872" y="${TT - 26}" width="54" height="14" fill="${C.yellow}" stroke="${ink}" stroke-width="1.6"/>` + H.label(899, TT - 14.5, 12, "START", "middle", ink);
    const earth = H.at(LX - 6, TT - 26, 0.28, K.props.earthGlobe({ face: "worried" }));
    const lamp = `<path d="M${LX},-10 V250" stroke="${ink}" stroke-width="4"/><path d="M${LX - 60},330 L${LX + 60},330 L${LX + 30},250 L${LX - 30},250 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/><ellipse cx="${LX}" cy="334" rx="62" ry="10" fill="#FFF3C8" stroke="${ink}" stroke-width="3"/>`;
    const string = `<path d="M${LX},340 V440" stroke="${ink}" stroke-width="2.6"/>` + `<g transform="translate(${LX},488) rotate(90) scale(2.0)">${babyMissile(C)}</g>`;
    // the lit candle at the table's right end (where the run ends), its fuse curling up the lamp's cord to the string
    const candle = `<rect x="1140" y="${TT - 74}" width="18" height="70" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>` + K.flames(1149, TT - 74, 0.3) +
      `<path d="M1136,${TT - 6} C1080,${TT - 10} 1000,${TT - 60} ${LX + 10},400 L${LX + 2},396" fill="none" stroke="${ink}" stroke-width="6" stroke-linecap="round"/><path d="M1136,${TT - 6} C1080,${TT - 10} 1000,${TT - 60} ${LX + 10},400 L${LX + 2},396" fill="none" stroke="#C9A77A" stroke-width="3" stroke-dasharray="6 4"/>`;
    const books = ramp;
    // the lid, propped against the front table leg
    const lid = `<g transform="translate(690,${FL + 10}) rotate(-8)"><rect x="-120" y="-150" width="240" height="150" fill="${C.orange}" stroke="${ink}" stroke-width="4"/><rect x="-108" y="-138" width="216" height="126" fill="none" stroke="${C.cream}" stroke-width="3"/>` +
      H.label(0, -88, 40, "OBJECTIVE:", "middle", C.navy) + H.label(0, -36, 52, "LOSE", "middle", C.war) + "</g>";
    // the players behind the table, cheering
    const kp = 2.3;
    const pol = H.at(600, TT + 120 - 100 * kp, kp, K.cast("politician", { arms: [[-150, -170], [150, 170]], mood: "grin", look: "right" }));
    const wm = H.at(1320, TT + 120 - 100 * kp, kp, K.cast("weaponsMaker", { arms: [[-150, -175], [150, 175]], mood: "grin", look: "left" }));
    const sk = H.at(1090, TT + 90 - 100 * 2.1, 2.1, tourist(K, C, { skeleton: true, look: "left", arms: [[-150, -170], [150, 170]] }));
    const svg = room + sofa + mantel + lamp + sk + pol + wm + table + board + earth + candle + string + books + dominoes + lid;
    return { svg, alt: "Living-room plate, pulled back: at the card table under the lamp the Politician, the tourist's skeleton and the Weapons Maker cheer; the baby missile hangs on a string from the lamp over the tiny worried Earth on START; a line of dominoes has fallen off the table, down a stair of books and across the rug to the sofa, where the front is tipping, the rest still standing along the sofa and the mantel; the lid OBJECTIVE: LOSE leans on a table leg." };
  },

  "host-digress"(H, fid) {
    const { K, C } = H, St = K.STUDIO, ink = C.line;
    // At the very end: the war papers still marching across the lectern's reading top (y St.top) under the iris,
    // the mug set down at the right end; the iris closed almost to nothing on her face, and the last paper wedged
    // sideways across the little circle, legs braced on its left edge and arms on its right.
    const top = St.top, x0 = St.lect[0] - St.lect[1] / 2, x1 = St.lect[0] + St.lect[1] / 2;
    const marchers = [0, 1, 2, 3, 4].map((i) => H.at(x0 + 40 + i * 92, top - 46 * 0.8, 0.8, K.money("war", i % 2))).join("");
    const cup = H.at(x1 - 40, top - 32, 0.5, mug(K, C));
    // the iris: a black card with a small round hole on her face
    const [fx, fy] = St.face, r = 130;
    const iris = `<path fill="#000" fill-rule="evenodd" d="M-40,-40 H1960 V1120 H-40 Z M${fx - r},${fy} a${r},${r} 0 1,0 ${2 * r},0 a${r},${r} 0 1,0 ${-2 * r},0 Z"/>` + `<circle cx="${fx}" cy="${fy}" r="${r}" fill="none" stroke="#3A3A3A" stroke-width="3"/>`;
    // the wedged paper: on its side at the right of the hole (her eye stays clear), its stick legs braced down on the
    // hole's lower rim under her eye, its arms up on the upper rim
    const rim = (deg, d = 0) => [fx + (r + d) * Math.cos((deg * Math.PI) / 180), fy + (r + d) * Math.sin((deg * Math.PI) / 180)];
    const bx = fx + 72, by = fy + 38;
    const body = H.at(bx, by, 1.05, `<g transform="rotate(90)">${K.money("war", 0).replace(/<path class="legs"[^>]*[/]>/, "")}</g>`);
    const leg = (from, deg) => { const k = rim(deg, -16), e = rim(deg, -2); return `M${from[0]},${from[1]} L${k[0].toFixed(1)},${k[1].toFixed(1)} L${(e[0] - 14).toFixed(1)},${e[1].toFixed(1)}`; };
    const arm = (from, deg) => { const e = rim(deg, -3); return `M${from[0]},${from[1]} L${e[0].toFixed(1)},${e[1].toFixed(1)}`; };
    const limbs = `<path d="${leg([bx - 18, by + 30], 118)} ${leg([bx - 4, by + 44], 100)}" fill="none" stroke="${ink}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>` +
      `<path d="${arm([bx - 8, by - 40], -60)} ${arm([bx + 14, by - 40], -38)}" fill="none" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>` +
      [[118, 10], [100, 10], [-60, 12], [-38, 12]].map(([deg, d]) => { const a = rim(deg, d), b = rim(deg, d + 16); return `<path d="M${a[0].toFixed(1)},${a[1].toFixed(1)} L${b[0].toFixed(1)},${b[1].toFixed(1)}" stroke="${C.cream}" stroke-width="4" stroke-linecap="round"/>`; }).join("");
    const svg = H.host("sideeye-closed", "palms-down", marchers + cup) + iris + limbs + body;
    return { svg, alt: "The end of the part: the iris has closed almost to nothing on Wishonia's side-eye, and the last war paper is wedged sideways across the little circle, its stick legs braced on one edge and its arms on the other, holding it open; under the black, the papers are still marching across her lectern." };
  },
};
