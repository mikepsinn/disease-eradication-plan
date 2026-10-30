// Sketches for storyboards/part-13-one-percent-treaty.md (v3, the 1950s atomic-age film look): each scene's key frame on
// a 1920 x 1080 frame, drawn with the production art. H.K is the kit with film.js and the props library; H.host() is a
// whole host shot. A plate is drawn as the camera frames it at that moment (one framing, not the whole plate).
// Built into the review sheet by tools/storyboard-sheet.mjs.

const GROUND = "#C8B07B", SKY = "#EFE3C4", WOOD = "#B47E52", WOOD_DARK = "#7A5634";
const f1 = (n) => n.toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});
function rng(seed) {
  let s = seed >>> 0 || 1;
  return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
}

// A person (or any person-unit drawing) standing with its feet at (x, feet), drawn at scale k (KIT.person's feet are at y 100).
function stand(H, o, x, feet, k, extra = "", inner = null) {
  return H.at(x, feet - 100 * k, k, (inner || H.K.person(o)) + extra);
}
// The plates' plain field (the-toll's ground and sky), its horizon at hz.
function field(hz) {
  return `<rect width="1920" height="1080" fill="${GROUND}"/><rect width="1920" height="${hz}" fill="${SKY}"/><path d="M0,${hz} H1920" stroke="#8E7A55" stroke-width="3" opacity="0.6"/>`;
}
// Navy space with mustard four-point stars, as in the theme song.
function space(H, seed, n = 80) {
  const { K, C } = H, r = rng(seed);
  let s = `<rect width="1920" height="1080" fill="${C.navy}"/>`;
  for (let i = 0; i < n; i++) {
    const x = r() * 1920, y = r() * 1080, k = r();
    s += k < 0.22 ? K.star(x, y, 9 + k * 50, C.yellow) : `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(1.4 + k * 2.2)}" fill="${C.cream}" opacity="0.6"/>`;
  }
  return s;
}
// The engraved Earth (KIT.props.earthGlobe) at a size the prop is not drawn for: its engraving (the land's outline and
// halftone, the meridians) kept at a readable weight instead of growing with the radius.
function globe(H, r, face) {
  const k = r / 110, m = Math.min(k, 2.4);
  return H.K.props.earthGlobe({ r, face })
    .replace(/(<pattern id="kpl\d+h" width=")8(" height=")8("[^>]*><circle cx=")4(" cy=")4(" r=")1\.9/, (_, a, b, c, d, e) =>
      `${a}${f1((8 * m) / k)}${b}${f1((8 * m) / k)}${c}${f1((4 * m) / k)}${d}${f1((4 * m) / k)}${e}${((1.9 * m) / k).toFixed(3)}`)
    .replace('stroke-width="3.5" stroke-linejoin="round"', `stroke-width="${((3.5 * m) / k).toFixed(3)}" stroke-linejoin="round"`)
    .replace(new RegExp(`stroke-width="${f1(1.6 * k)}" opacity="0.5"`), `stroke-width="${f1(1.6 * m)}" opacity="0.5"`);
}

// ── The cast ──
// The leaders: the politician in a plain sash (no emblem). L0..L3 from the storyboard's notes, then four more with
// the sashes swapped.
const LEAD = [[0, "orange"], [1, "yellow"], [2, "peri"], [3, "tan"], [0, "yellow"], [1, "tan"], [2, "orange"], [3, "peri"]];
function withSash(H, o, col) {
  const { K, C } = H, ink = C.line, R = K.rig(o), T = R.shoulder[1][1] - 3, w = (R.shoulder[1][0] * 33) / 27, Wy = R.hipY - 8;
  const a = [-w * 0.66, T + 1], b = [13, Wy + 4], dx = b[0] - a[0], dy = b[1] - a[1], n = Math.hypot(dx, dy), nx = (-dy / n) * 5.5, ny = (dx / n) * 5.5;
  const pts = [[a[0] + nx, a[1] + ny], [b[0] + nx, b[1] + ny], [b[0] - nx, b[1] - ny], [a[0] - nx, a[1] - ny]];
  const band = `<path d="M${pts.map((p) => f1(p[0]) + "," + f1(p[1])).join(" L")} Z" fill="${col}" stroke="${ink}" stroke-width="2.2" stroke-linejoin="miter"/>`;
  return K.person(o).replace('<g class="arm-l">', band + '<g class="arm-l">');
}
function leader(H, i, extra) {
  const [tone, sash] = LEAD[i];
  const o = H.K.castOpts("politician", copy({ tone, flagPin: false }, extra));
  return { o, svg: withSash(H, o, H.C[sash]) };
}
const YOU = { tone: 2, outfit: "suit", hat: "bowler" };
// The carved cuckoo-clock bird on its zigzag spring (the "crazy" running gag), around the spring's base at (0, 0),
// pointing up, the bird facing +x; open: its beak open mid-cuckoo.
function cuckoo(C, open) {
  const ink = C.line, pt = (p) => p[0] + "," + p[1];
  const poly = (pts, fill, w) => `<path d="M${pts.map(pt).join(" L")} Z" fill="${fill}" stroke="${ink}" stroke-width="${w || 2.4}" stroke-linejoin="miter" stroke-miterlimit="8"/>`;
  const zig = [[0, 0]];
  for (let i = 1; i < 8; i++) zig.push([i % 2 ? -7 : 7, -7.5 * i]);
  zig.push([0, -60]);
  const spring = `<path d="M${zig.map(pt).join(" L")}" fill="none" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/><path d="M${zig.map(pt).join(" L")}" fill="none" stroke="${C.peri}" stroke-width="1.2"/>`;
  const jaw = open ? `<g transform="rotate(30 21 -79)">${poly([[21.5, -79], [30, -78], [20.5, -75.5]], C.orange, 2)}</g>` : poly([[21.5, -79], [30, -78], [20.5, -75.5]], C.orange, 2);
  return spring + poly([[-6, -63], [6, -63], [6, -58], [-6, -58]], C.rust, 2) + poly([[-13, -72], [-24, -84], [-22, -69], [-12, -63]], C.rust) +
    poly([[-15, -71], [-5, -79], [6, -81], [10, -88], [16, -91], [21, -88], [23, -81], [20, -73], [13, -65], [-2, -61], [-12, -63]], C.tan) +
    poly([[-9, -70], [2, -77], [9, -72], [4, -66], [-6, -65]], C.rust, 2.2) + poly([[21, -85], [31, -83], [21.5, -79.5]], C.orange, 2) + jaw +
    `<path d="M12.5,-84.5 Q16,-88 19.5,-85 Q16,-82 12.5,-84.5 Z" fill="${C.cream}" stroke="${ink}" stroke-width="1.2"/><circle cx="16.6" cy="-84.8" r="1.5" fill="${ink}"/>` +
    `<path d="M11.8,-84.2 Q16,-89.6 20.3,-85.4" fill="none" stroke="${ink}" stroke-width="2" stroke-linecap="round"/>`;
}
// A stack of flat bills seen edge on (the leaders' war papers): base at y 0, h tall, w wide; every third edge shows a
// dark green seal.
function billStack(C, h, w, seed) {
  const r = rng(seed), n = Math.round(h / 11);
  let s = "";
  for (let i = 0; i < n; i++) {
    const y = -(i + 1) * (h / n), j = Math.round((r() - 0.5) * 9);
    s += `<rect x="${f1(-w / 2 + j)}" y="${f1(y)}" width="${w}" height="${f1(h / n)}" rx="1.5" fill="${C.money}" stroke="${C.line}" stroke-width="2.2"/>` +
      (i % 3 === 1 ? `<circle cx="${f1(w / 2 + j - 11)}" cy="${f1(y + h / n / 2)}" r="3.2" fill="${C.moneyDark}" stroke="${C.line}" stroke-width="1"/>` : "");
  }
  return s;
}
// A wooden crate of 100 grinning warheads, standing on (0, 0): 150 wide, 104 tall, its warheads' noses poking out of the
// top. look: where the noses' eyes look (-1, 0, 1); gulp: sweat drops.
function crate(H, look = 0, gulp = false, stencil = true) {
  const { C } = H, ink = C.line;
  let noses = "";
  for (let i = 0; i < 5; i++) {
    const x = -56 + i * 28, y = -104 - (i % 2 ? 6 : 0);
    noses += `<path d="M${x - 11},${y + 8} L${x - 11},${y - 14} Q${x},${y - 34} ${x + 11},${y - 14} L${x + 11},${y + 8} Z" fill="${C.war}" stroke="${ink}" stroke-width="2.6" stroke-linejoin="round"/>` +
      `<path d="M${x - 7},${y - 20} Q${x},${y - 33} ${x + 7},${y - 20}" fill="${C.cream}" stroke="${ink}" stroke-width="1.8"/>` +
      `<circle cx="${x - 4 + look * 2}" cy="${y - 9}" r="1.8" fill="${ink}"/><circle cx="${x + 4 + look * 2}" cy="${y - 9}" r="1.8" fill="${ink}"/>` +
      (gulp ? `<path d="M${x - 4},${y - 2} h8" stroke="${ink}" stroke-width="1.8"/><path d="M${x + 12},${y - 22} q3,5 0,8 q-3,-3 0,-8 Z" fill="${C.cyan}" stroke="${ink}" stroke-width="1.2"/>`
        : `<path d="M${x - 5},${y - 3} Q${x},${y + 2} ${x + 5},${y - 3}" fill="none" stroke="${ink}" stroke-width="1.8"/>`);
  }
  const planks = [-78, -52, -26].map((y) => `<path d="M-72,${y} H72" stroke="${WOOD_DARK}" stroke-width="2.4"/>`).join("");
  return noses + `<rect x="-75" y="-104" width="150" height="104" fill="${WOOD}" stroke="${ink}" stroke-width="4"/>` + planks +
    `<path d="M-72,-101 L72,-3 M72,-101 L-72,-3" stroke="${WOOD_DARK}" stroke-width="3" opacity="0.5"/>` +
    (stencil ? `<text x="0" y="-38" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="40" fill="${C.ink}" opacity="0.85">100</text>` : "");
}
// A treaty lying flat on the table, seen from a little above (y squashed): w wide, its title, scribbled signatures.
function flatTreaty(H, x, y, w, title, sigs, singed = false, seed = 1) {
  const { C } = H, ink = C.line, h = 110, r = rng(seed);
  let s = `<rect x="0" y="0" width="${w}" height="${h}" fill="#FBF5E4" stroke="${ink}" stroke-width="3"/>` +
    `<text x="${w / 2}" y="26" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="22" fill="${ink}">${H.esc(title)}</text>`;
  for (let i = 0; i < sigs; i++) {
    const sx = 14 + (i % 4) * ((w - 28) / 4) + r() * 10, sy = 46 + Math.floor(i / 4) * 18 + r() * 4;
    s += `<path d="M${f1(sx)},${f1(sy)} q6,-9 10,0 t10,0 t9,-2 l8,3" fill="none" stroke="${C.navy}" stroke-width="1.8"/>`;
  }
  if (singed) s += `<path d="M0,${h} L0,${h - 16} Q${w * 0.2},${h - 6} ${w * 0.35},${h - 18} Q${w * 0.6},${h - 4} ${w * 0.8},${h - 20} L${w},${h - 10} L${w},${h} Z" fill="#3A2E24" stroke="${ink}" stroke-width="2"/>` +
    `<path d="M${w - 18},0 Q${w - 6},10 ${w},26 L${w},0 Z" fill="#3A2E24"/>`;
  return `<g transform="translate(${x},${y}) scale(1,0.62)">${s}</g>`;
}
// A small planet of 847-civilizations, on (cx, cy) with radius r: listened (lit teal, a little hospital) or not (charred,
// a little mushroom cloud); a copy of the manual on top either way.
function planet(H, cx, cy, r, col, lit, ring, seed) {
  const { K, C } = H, ink = C.line, w = Math.max(1.2, r * 0.05);
  const body = lit ? col : "#3A2E24";
  let s = lit ? `<circle cx="${cx}" cy="${cy}" r="${f1(r * 1.35)}" fill="${C.med}" opacity="0.35"/><circle cx="${cx}" cy="${cy}" r="${f1(r * 1.16)}" fill="${C.med}" opacity="0.4"/>` : "";
  if (ring) s += `<ellipse cx="${cx}" cy="${cy}" rx="${f1(r * 1.7)}" ry="${f1(r * 0.38)}" fill="none" stroke="${lit ? C.cream : "#5A4A3C"}" stroke-width="${f1(w * 1.6)}" transform="rotate(-14 ${cx} ${cy})"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${body}" stroke="${ink}" stroke-width="${f1(w)}"/>` +
    `<path d="M${f1(cx - r * 0.62)},${f1(cy - r * 0.05)} q${f1(r * 0.06)},${f1(-r * 0.42)} ${f1(r * 0.46)},${f1(-r * 0.52)}" fill="none" stroke="${lit ? C.cream : "#5A4A3C"}" stroke-width="${f1(w * 1.4)}" stroke-linecap="round" opacity="0.7"/>`;
  const top = cy - r, u = r / 60;
  // two little domed houses and the manual on the planet's top
  s += [-0.42, 0.3].map((dx) => `<path d="M${f1(cx + dx * r - 9 * u)},${f1(top + r * (1 - Math.cos(Math.asin(dx))) + 2 * u)} v${f1(-8 * u)} a${f1(9 * u)},${f1(9 * u)} 0 0,1 ${f1(18 * u)},0 v${f1(8 * u)} Z" fill="${lit ? C.cream : "#2A221B"}" stroke="${ink}" stroke-width="${f1(w)}"/>`).join("");
  s += `<rect x="${f1(cx - 7 * u)}" y="${f1(top - 4 * u)}" width="${f1(14 * u)}" height="${f1(5 * u)}" fill="${C.orange}" stroke="${ink}" stroke-width="${f1(w * 0.8)}"/>`;
  if (lit) s += `<rect x="${f1(cx + 0.02 * r)}" y="${f1(top - 20 * u)}" width="${f1(22 * u)}" height="${f1(16 * u)}" fill="${C.cream}" stroke="${ink}" stroke-width="${f1(w)}"/>` +
    `<path d="M${f1(cx + 0.02 * r + 11 * u)},${f1(top - 17 * u)} v${f1(10 * u)} M${f1(cx + 0.02 * r + 6 * u)},${f1(top - 12 * u)} h${f1(10 * u)}" stroke="${C.med}" stroke-width="${f1(3.4 * u)}"/>`;
  else s += H.at(cx + 0.15 * r, top + 2 * u, (r * 1.1) / 560, K.nuke()) +
    [-6, 4].map((dx) => `<path d="M${f1(cx + dx * u)},${f1(cy - 0.2 * r)} l${f1(-4 * u)},${f1(-6 * u)} l${f1(4 * u)},${f1(-6 * u)}" fill="none" stroke="#8C8782" stroke-width="${f1(w * 1.2)}"/>`).join("");
  return s;
}

export default {
  "one-percent-treaty-title"(H, fid) {
    const { K, C } = H;
    // the atomic card (KIT.titleScene): the emblem, then the heading under it (16:9: heading size 200, block on y 700)
    const cx = 960, cy = 300, rx = 200, ry = 62;
    const onOrbit = (a, th) => { const t = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th); return [cx + ex * Math.cos(t) - ey * Math.sin(t), cy + ex * Math.sin(t) + ey * Math.cos(t)]; };
    let s = `<rect width="1920" height="1080" fill="${C.navy}"/>` +
      [0, 60, -60].map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    // two electrons left on their orbits (the third is down at the "%")
    [[0, 0.5], [60, 3.6]].forEach(([a, th]) => { const p = onOrbit(a, th); s += H.at(f1(p[0]), f1(p[1] - 6), 0.62, K.money("war", 0)); });
    s += `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    const heading = (y, size, spans) => {
      const t = (main, dx, dy) => `<text x="${960 + dx}" y="${y + dy}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${size}" ` +
        (main ? `stroke="${C.cream}" stroke-width="${f1(size * 0.044)}" stroke-linejoin="round" style="paint-order:stroke"` : `fill="${C.ink}"`) + ">" +
        spans.map(([text, col]) => `<tspan${main ? ` fill="${col}"` : ""}>${H.esc(text)}</tspan>`).join("") + "</text>";
      return t(false, size * 0.04, size * 0.053) + t(true, 0, 0);
    };
    s += heading(637, 100, [["THE SOLUTION", C.cream]]) + heading(833, 200, [["A ", C.cream], ["1%", C.med], [" TREATY", C.cream]]);
    // the third electron, out of the bottom ring of the "%" with a cross on its seal, bowing
    s += `<g transform="translate(760,836) rotate(-24)"><g transform="translate(0,-30) scale(0.62)">${K.money("med", 0.5)}</g></g>` +
      K.star(818, 742, 18, C.yellow) + K.star(726, 770, 11, C.yellow) + K.star(806, 790, 8, C.cream);
    return { svg: s, alt: "The period title card: THE SOLUTION over A 1% TREATY in cream, the 1% in teal, on navy under the atom; one of the atom's three paper electrons has dropped through the % and stands at its foot with a cross seal, bowing, while the other two keep running round their orbits." };
  },

  "sounds-crazy"(H, fid) {
    const { K, C } = H;
    const front = K.mug(590, 721) + H.at(955, 793, 2.7, cuckoo(C, true)) +
      `<path d="M1048,560 q14,-10 24,4 M1060,530 q16,-12 28,4" fill="none" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>`;
    return { svg: H.host("sideeye-closed", "idle", front), alt: "Wishonia at her lectern side-eyes a carved wooden cuckoo-clock bird that has sprung up out of the lectern top on a zigzag spring, its beak open mid-cuckoo; her coffee mug on the lectern." };
  },

  "every-leader-at-once"(H, fid) {
    const { K, C } = H, ink = C.line;
    const G = [960, 1720], R = 1120;
    let s = space(H, 13, 70) + H.at(G[0], G[1] + R, 1, globe(H, R));
    // the funnel on the North Pole
    s += `<g transform="translate(${G[0]},${G[1]}) translate(0,${-R})"><g transform="scale(1.25)">${K.props.colorFlipFunnel({})}</g></g>`;
    // the leaders round the rim, each on his stack of war papers (stack 120 tall, the leader at 1.25)
    const k = 1.25, SH = 120;
    const ring = [[-35, 2, "late"], [-23, 4, "glare"], [-11.5, 0, "up"], [11.5, 1, "up"], [23, 5, "up"], [35, 3, "up"]];
    ring.forEach(([th, i, pose], n) => {
      let extra, held = "";
      if (pose === "late") extra = { mood: "worried", arms: [[34, 62], [18, 50]] };
      else extra = { mood: pose === "glare" ? "cross" : "grin", look: pose === "glare" ? "left" : undefined, arms: [[-162, -176], [162, 176]] };
      const L = leader(H, i, extra), Rg = K.rig(L.o);
      if (pose === "late") held = H.at(f1((Rg.hand[0][0] + Rg.hand[1][0]) / 2 + 6), f1((Rg.hand[0][1] + Rg.hand[1][1]) / 2 + 4), 0.5, K.money("war", 0).replace('class="legs"', 'class="legs" opacity="0"'));
      else held = H.at(f1((Rg.hand[0][0] + Rg.hand[1][0]) / 2), f1((Rg.hand[0][1] + Rg.hand[1][1]) / 2 - 16), 0.52, K.money("war", 0).replace('class="legs"', 'class="legs" opacity="0"'));
      const top = pose === "late" ? billStack(C, SH + 9, 104, n + 3) : billStack(C, SH, 104, n + 3);
      s += `<g transform="translate(${G[0]},${G[1]}) rotate(${th}) translate(0,${-R})">${top}<g transform="translate(0,${f1(-SH - 100 * k)}) scale(${k})">${L.svg}${held}</g></g>`;
    });
    return { svg: s, alt: "The top of a big engraved Earth floating in a starry navy sky: six leaders in plain sashes stand round its rim on stacks of green war papers, five of them lifting their top paper overhead at the same moment like a chorus line, the color-flip funnel on the North Pole between them; the leader on the far left is still bent over his stack, a beat late, and the one beside him turns and glares." };
  },

  "thats-the-treaty"(H, fid) {
    const { C } = H, ink = C.line;
    // the treaty hangs from her presenting hand, beside the lectern, and out of the bottom of the frame
    const x0 = 960, x1 = 1490, top = 690;
    const paper = `<rect x="${x0 + 8}" y="${top}" width="${x1 - x0 - 16}" height="460" fill="#FBF5E4" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="${x0 + 8}" y="${top}" width="${x1 - x0 - 16}" height="460" fill="none" stroke="${C.tan}" stroke-width="2" opacity="0.4" transform="translate(6,0)"/>` +
      `<text x="${(x0 + x1) / 2}" y="${top + 58}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="40" letter-spacing="2" fill="${ink}">THE 1% TREATY</text>` +
      `<path d="M${x0 + 70},${top + 76} H${x1 - 70}" stroke="${C.orange}" stroke-width="3"/>` +
      `<text x="${(x0 + x1) / 2}" y="${top + 114}" text-anchor="middle" font-family="Inter" font-weight="600" font-size="19" fill="${ink}">Redirect 1% of military spending to clinical trials.</text>` +
      [260, 330].map((y) => `<path d="M${x0 + 8},${top + y} H${x1 - 8}" stroke="${C.tan}" stroke-width="1.6" opacity="0.35"/>`).join("");
    const roll = `<rect x="${x0 - 6}" y="${top - 22}" width="${x1 - x0 + 12}" height="30" rx="15" fill="#F3E5C2" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M${x0 + 10},${top - 13} H${x1 - 10}" stroke="#FFFFFF" stroke-width="3" opacity="0.6"/>`;
    return { svg: H.host("smirk-smile", "presenting", paper + roll), alt: "Wishonia at her lectern holds up the 1% treaty by its top roll; the paper hangs down beside the lectern and out of the bottom of the frame: THE 1% TREATY, one line reading Redirect 1% of military spending to clinical trials., then nothing but empty paper." };
  },

  "enemies-will-invade"(H, fid) {
    const { K, C } = H, ink = C.line;
    let s = field(560);
    // the picket fence, running away from the camera between the two yards
    for (let i = 8; i >= 0; i--) {
      const t = i / 8, base = 960 - 380 * Math.pow(t, 0.8), h = 190 * (1 - 0.78 * t), w = 30 * (1 - 0.7 * t), x = 960 + 30 * t;
      s += `<path d="M${f1(x - w / 2)},${f1(base)} V${f1(base - h + w / 2)} L${f1(x)},${f1(base - h)} L${f1(x + w / 2)},${f1(base - h + w / 2)} V${f1(base)} Z" fill="#FBF5E4" stroke="${ink}" stroke-width="${f1(3.4 * (1 - 0.6 * t))}"/>`;
    }
    s += `<path d="M960,${960 - 150} L990,${580 - 0}" stroke="${ink}" stroke-width="3" opacity="0.4"/>`;
    // the heaps of grumpy missiles, lying on their sides, aimed across the fence
    const lying = (x, y, dir, k) => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${dir * 90}) scale(${k}) translate(0,80)">${K.props.missile({ mood: "grumpy", arms: "none" })}</g>`;
    const heap = (cx, dir) => {
      let h = "";
      [[3, 0], [2, 1], [1, 2]].forEach(([n, row]) => {
        for (let j = 0; j < n; j++) h += lying(cx + (j - (n - 1) / 2) * 120, 870 - row * 62, dir, 0.62);
      });
      return h + H.at(cx + dir * 150, 880 - 2 * 62 - 30, 0.9, K.props.priceTag({ text: "$" }));
    };
    // the two leaders, hugging their heaps and shaking; L1 on the left faces right, L3 on the right faces left
    const L1 = leader(H, 1, { mood: "worried", arms: [[52, 96], [36, 84]] }), L3 = leader(H, 3, { mood: "worried", look: "left", arms: [[-36, -84], [-52, -96]] });
    s += stand(H, null, 470, 905, 1.7, "", L1.svg) + stand(H, null, 1460, 905, 1.7, "", L3.svg) + heap(700, 1) + heap(1225, -1);
    // shiver lines round the real two
    s += [[355, 700], [585, 690], [1345, 690], [1575, 700]].map(([x, y]) => `<path d="M${x},${y} l-8,10 l8,10 l-8,10" fill="none" stroke="${ink}" stroke-width="3" opacity="0.6"/>`).join("");
    // the thought bubbles: in each, the thinker stands charred under a little mushroom cloud
    const bubble = (bx, by, who, dir, hx) => {
      const id = `${fid}-b${who}`, L = leader(H, who, { charred: true, look: dir < 0 ? "left" : undefined });
      return `<defs><clipPath id="${id}"><circle cx="${bx}" cy="${by}" r="150"/></clipPath></defs>` +
        [[0.3, 196, 20], [0.62, 262, 13], [0.86, 316, 8]].map(([u, dy, r]) => `<circle cx="${f1(bx + (hx - bx) * u)}" cy="${by + dy}" r="${r}" fill="#FBF5E4" stroke="${ink}" stroke-width="4"/>`).join("") +
        `<circle cx="${bx}" cy="${by}" r="150" fill="#FBF5E4" stroke="${ink}" stroke-width="5"/>` +
        `<g clip-path="url(#${id})"><rect x="${bx - 160}" y="${by + 70}" width="320" height="100" fill="${GROUND}"/>` +
        H.at(bx + dir * 40, by + 92, 0.36, K.nuke()) + stand(H, null, bx - dir * 30, by + 126, 0.88, "", L.svg) + "</g>";
    };
    s += bubble(360, 200, 1, 1, 470) + bubble(1560, 200, 3, -1, 1460);
    return { svg: s, alt: "Two leaders in plain sashes on either side of a white picket fence, each hugging his heap of grumpy price-tagged missiles aimed across it and shaking; over each, a thought bubble in which he stands charred black and smoking, hair up, under a little mushroom cloud." };
  },

  "one-twenty-one-apocalypses"(H, fid) {
    const { K, C } = H, ink = C.line;
    let s = field(560);
    // the fallen tower: its crates in a row to the horizon, each one going off
    const N = 15;
    for (let i = N - 1; i >= 0; i--) {
      const t = i / (N - 1), e = Math.pow(t, 0.6), x = 820 + 1050 * e, y = 905 - 335 * e, k = 0.62 * Math.pow(0.84, i);
      s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(130 * k * 1.6)}" ry="${f1(26 * k * 1.6)}" fill="#6E5A3E" opacity="0.55"/>` + H.at(f1(x), f1(y), (k * 1.25).toFixed(3), K.nuke());
    }
    // in front: the tiny Earth and its charred human, and the weapons maker, charred, hugging the one crate he pulled out
    s += H.at(560, 912, 1, globe(H, 70)) + stand(H, { tone: 1, outfit: "shirt", color: 2, charred: true }, 560, 772, 0.55);
    const WM = K.castOpts("weaponsMaker", { charred: true, arms: [[34, 80], [-10, -70]] }), Rw = K.rig(WM);
    const cr = H.at(f1(Rw.hand[0][0] + 34), f1(Rw.hand[0][1] + 30), 0.4, crate(H, 1, true, true));
    s += stand(H, WM, 270, 930, 2.0, cr);
    return { svg: s, alt: "A tan field under a cream sky: the fallen tower's crates go off in a row of mushroom clouds marching to the horizon; in front, the weapons maker, charred black and smoking, hugs the one crate he pulled out, its warheads' noses gulping at the clouds, beside a tiny Earth whose one human stands charred on top." };
  },

  "more-than-sufficient"(H, fid) {
    const { K, C } = H;
    // the steam off her mug, as a little mushroom cloud in cream and white
    const steam = K.nuke().replace(new RegExp(C.orange, "g"), "#E9E1CF").replace(new RegExp(C.yellow, "g"), "#F6F0DC").replace(new RegExp(C.tan, "g"), "#DCD3BD");
    const front = K.mug(870, 721) + H.at(894, 716, 0.24, steam);
    return { svg: H.host("smirk-closed", "idle", front), alt: "Wishonia at her lectern, deadpan, smirking; a little mushroom cloud of steam rises out of her coffee mug." };
  },

  "treaties-you-signed"(H, fid) {
    const { K, C } = H, ink = C.line;
    const bg = `<rect width="1920" height="1080" fill="${SKY}"/>`;
    let s = `<rect x="-200" y="700" width="2400" height="600" fill="${GROUND}"/><path d="M-200,700 H2200" stroke="#8E7A55" stroke-width="3" opacity="0.6"/>`;
    // behind the table: the weapons maker risen up with his baby missile and his hanky; charred YOU at the right
    const WM = K.castOpts("weaponsMaker", { mood: "sad" }), Rw = K.rig(WM);
    const hanky = `<path d="M${f1(Rw.mouth[0] - 2)},${f1(Rw.mouth[1] - 8)} l16,-6 l8,14 l-14,10 l-12,-6 Z" fill="#FFFFFF" stroke="${ink}" stroke-width="1.6"/>` +
      `<path d="M${f1(Rw.eyes[0] - 6)},${f1(Rw.eyes[1] + 3)} q-3,6 0,9 q3,-3 0,-9 Z" fill="${C.cyan}" stroke="${ink}" stroke-width="1.2"/>`;
    s += stand(H, WM, 640, 830, 2.5, hanky);
    const you = copy(YOU, { charred: true, look: "left", arms: [[-8, -3], [8, 3]] });
    s += stand(H, you, 1330, 900, 2.6) + `<path d="M1290,370 q-12,-14 0,-28 q12,-14 0,-28 M1250,390 q-10,-12 0,-24 q10,-12 0,-24" fill="none" stroke="#8C8782" stroke-width="5"/>`;
    // the table: a cream cloth with plain bunting, running out of the frame both ways
    s += `<path d="M-20,700 H1940 V790 H-20 Z" fill="#FBF5E4" stroke="${ink}" stroke-width="5"/><rect x="-20" y="790" width="1960" height="300" fill="#F3E5C2" stroke="${ink}" stroke-width="5"/>`;
    for (let i = 0; i < 26; i++) s += `<path d="M${i * 78 - 30},794 l39,46 l39,-46 Z" fill="${[C.orange, C.cream, C.peri][i % 3]}" stroke="${ink}" stroke-width="2.4"/>`;
    // on the table: the three treaties flattened (the first two running off the left), the third singed; the 1% treaty,
    // unsigned, in front of YOU, the pencil on its empty signature line
    s += flatTreaty(H, -150, 712, 250, "CHEMICAL WEAPONS BAN", 16, false, 3) + flatTreaty(H, 125, 716, 250, "BIOLOGICAL WEAPONS BAN", 16, false, 5) + flatTreaty(H, 400, 712, 230, "LANDMINE BAN", 16, true, 7);
    s += `<g transform="translate(960,710) scale(1,0.66)"><rect width="620" height="112" fill="#FBF5E4" stroke="${ink}" stroke-width="3"/>` +
      `<text x="310" y="30" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="28" fill="${ink}">THE 1% TREATY</text>` +
      `<text x="310" y="62" text-anchor="middle" font-family="Inter" font-weight="600" font-size="19" fill="${ink}">Redirect 1% of military spending to clinical trials.</text>` +
      `<path d="M340,98 H580" stroke="${ink}" stroke-width="2.4"/></g>` + H.at(1350, 776, 0.5, K.pencil(), 27);
    // the camera's framing: pushed in on the end of the table
    s = bg + `<g transform="translate(960,520) scale(1.3) translate(-960,-520)">${s}</g>`;
    return { svg: s, alt: "A long table with a cream cloth and bunting: three flattened treaties crowded with signatures (CHEMICAL WEAPONS BAN, BIOLOGICAL WEAPONS BAN, and LANDMINE BAN, singed); at the right end, charred YOU blinks down at the one-line 1% treaty, unsigned, a pencil on its signature line; behind the table the weapons maker cradles his baby missile and sniffles into a hanky." };
  },

  "847-civilizations"(H, fid) {
    const { K, C } = H, ink = C.line;
    let s = space(H, 847, 90);
    // the line of planets, curving away to the vanishing point
    const cols = [C.rust, C.peri, C.cyan, C.tan, C.yellow, C.orange];
    const N = 16;
    for (let i = N - 1; i >= 0; i--) {
      const t = i / (N - 1), e = Math.pow(t, 0.55), x = 760 + 1060 * e, y = 640 - 330 * e - Math.sin(e * Math.PI) * 60, r = 92 * Math.pow(0.8, i);
      s += planet(H, Math.round(x), Math.round(y), r, cols[i % cols.length], i % 2 === 0, i % 3 === 1, i);
    }
    // Earth, the 847th, nearest the camera: worried, sweating, a wisp of smoke off its edge; the manual on its top
    s += H.at(390, 1000, 1, globe(H, 250, "worried")) +
      `<path d="M168,640 q-16,-20 0,-40 q16,-20 0,-40" fill="none" stroke="#8C8782" stroke-width="6" stroke-linecap="round"/>` +
      H.at(390, 504, 0.9, K.props.manual({}), -6);
    s += H.big(1330, 236, 170, "847", "middle", C.cream);
    return { svg: s, alt: "Navy space with mustard stars: a long line of small planets curves away to the horizon, about half glowing teal with little hospitals, the rest charred under little mushroom clouds, a copy of the manual on every one; 847 in the sky; Earth, nearest the camera, sweats with a worried face, the manual on its top and a wisp of smoke off its edge." };
  },

  "next-page"(H, fid) {
    const { K, C } = H, ink = C.line;
    const G = [960, 3480], R = 2640;
    let s = space(H, 99, 50) + H.at(G[0], G[1] + R, 1, globe(H, R));
    // seven readers along Earth's top, their books snapped shut, the cuckoo's head stuck out of the first; YOU at the end
    const readers = [
      { tone: 0, outfit: "dress", color: 1, hair: 1, mood: "cross" },
      { tone: 3, outfit: "shirt", color: 2, mood: "flat" },
      { tone: 1, outfit: "overalls", color: 0, mood: "flat" },
      { tone: 2, outfit: "dress", color: 3, hair: 1, mood: "flat" },
      { tone: 0, outfit: "labcoat", color: 1, hair: 2, mood: "flat" },
      { tone: 3, outfit: "shirt", color: 0, hat: "fedora", mood: "flat" },
      copy(YOU, { mood: "eager" }),
    ];
    const arms = [[26, 108], [12, 100]];
    readers.forEach((o, i) => {
      const x = 215 + i * 248, th = (Math.asin((x - G[0]) / R) * 180) / Math.PI, oo = copy(o, { arms }), Rg = K.rig(oo);
      const hx = (Rg.hand[0][0] + Rg.hand[1][0]) / 2, hy = (Rg.hand[0][1] + Rg.hand[1][1]) / 2;
      let book;
      // the first book is snapped shut on the cuckoo: its head sticks out of the top, squawking
      if (i === 0) book = H.at(f1(hx + 12), f1(hy + 14), 0.95, cuckoo(C, true), 18) + H.at(f1(hx + 10), f1(hy + 30), 0.42, K.props.manual({})) +
        `<path d="M${f1(hx + 46)},${f1(hy - 66)} l12,-6 M${f1(hx + 48)},${f1(hy - 56)} l14,0 M${f1(hx + 44)},${f1(hy - 76)} l8,-10" stroke="${ink}" stroke-width="2.4" stroke-linecap="round"/>`;
      else if (i < 6) book = H.at(f1(hx + 10), f1(hy + 30), 0.42, K.props.manual({}));
      else {
        // YOU's book open, page 2 turning
        book = `<g transform="translate(${f1(hx + 6)},${f1(hy - 4)})"><path d="M-30,-22 L0,-16 L0,22 L-30,16 Z" fill="#FBF5E4" stroke="${ink}" stroke-width="2"/><path d="M0,-16 L30,-22 L30,16 L0,22 Z" fill="#FBF5E4" stroke="${ink}" stroke-width="2"/>` +
          `<path d="M0,-16 Q16,-40 34,-34 L30,4 Q14,-6 0,22 Z" fill="#F3E5C2" stroke="${ink}" stroke-width="2"/>` +
          [-8, -2, 4, 10].map((y) => `<path d="M-26,${y} L-4,${y + 4}" stroke="${ink}" stroke-width="1" opacity="0.5"/>`).join("") + "</g>";
      }
      s += `<g transform="translate(${G[0]},${G[1]}) rotate(${f1(th)}) translate(0,${-R})"><g transform="translate(0,${f1(-100 * 1.7)}) scale(1.7)">${K.person(oo)}${book}</g></g>`;
    });
    return { svg: s, alt: "On Earth's top under the stars, a row of seven readers stand with their copies of the manual snapped shut, a carved cuckoo's head sticking out of the first one; at the end of the row YOU in his bowler holds his copy open, turning to page 2." };
  },

  "bread-mold"(H, fid) {
    const { K, C } = H, ink = C.line;
    // the cave: a rust rock wall over a sandy floor, a campfire between the two cavemen
    let s = `<rect width="1920" height="1080" fill="#6E3A24"/>` +
      `<path d="M0,0 H1920 V120 Q1700,200 1500,150 Q1200,90 960,160 Q700,230 420,140 Q200,90 0,170 Z" fill="#4E2818"/>` +
      `<path d="M0,700 Q480,660 960,690 Q1440,720 1920,680 V1080 H0 Z" fill="${C.tan}" stroke="${ink}" stroke-width="4"/>`;
    for (const [x, y, w] of [[260, 420, 160], [700, 300, 120], [1240, 380, 150], [1640, 300, 110]]) s += `<path d="M${x},${y} l${w * 0.5},-40 l${w * 0.5},30 l-20,40 Z" fill="#5A2E1C" opacity="0.7"/>`;
    // behind them, the sick cavemen x-raying one after another into grinning skeletons
    const sick = [{ tone: 1, outfit: "shirt", color: 1, hair: 2 }, { tone: 3, outfit: "dress", color: 0, hair: 1 }, { tone: 0, outfit: "shirt", color: 3 }, { tone: 2, outfit: "shirt", color: 2, hair: 2 }, { tone: 1, outfit: "dress", color: 2, hair: 1 }];
    sick.forEach((o, i) => {
      const x = 470 + i * 240, bones = i < 3;
      s += stand(H, copy(o, bones ? { skeleton: true } : { light: "red", mood: "sad", look: "left", arms: [[-30, -150], [10, 4]] }), x, 712, 1.0);
    });
    // the glowing heap of flicked-off mold
    // the campfire, at the back
    s += `<path d="M880,760 L1040,740 M890,740 L1030,766" stroke="${WOOD_DARK}" stroke-width="16" stroke-linecap="round"/>` + K.flames(960, 748, 1.0);
    s += `<ellipse cx="960" cy="872" rx="190" ry="34" fill="${C.med}" opacity="0.4"/>`;
    const r = rng(5);
    for (let i = 0; i < 30; i++) s += `<circle cx="${f1(960 + (r() - 0.5) * 260)}" cy="${f1(872 - r() * 30)}" r="${f1(8 + r() * 8)}" fill="${r() < 0.5 ? C.med : C.cyan}" stroke="${ink}" stroke-width="2"/>`;
    s += [[860, 830], [1070, 826], [960, 808], [1010, 846]].map(([x, y]) => K.star(x, y, 15, C.cream)).join("");
    // the two cavemen, flicking the mold off their slices; A faces right, B faces left
    const slice = (mold) => `<rect x="-22" y="-20" width="44" height="40" rx="10" fill="#E9C07A" stroke="${ink}" stroke-width="3"/><rect x="-16" y="-14" width="32" height="30" rx="7" fill="#F6E1B0"/>` +
      (mold ? `<circle cx="8" cy="-6" r="7" fill="${C.med}" stroke="${ink}" stroke-width="1.6"/><circle cx="-6" cy="6" r="5" fill="${C.med}" stroke="${ink}" stroke-width="1.6"/>` : "");
    const spots = `<ellipse cx="-8" cy="-6" rx="3.6" ry="2.6" fill="${C.rust}"/><ellipse cx="8" cy="4" rx="3.6" ry="2.6" fill="${C.rust}"/><ellipse cx="-4" cy="20" rx="3.6" ry="2.6" fill="${C.rust}"/>`;
    const A = { tone: 2, outfit: "shirt", colorHex: "#C99A5E", hair: 0, plain: true, mood: "flat", arms: [[30, 90], [60, 110]] };
    const B = { tone: 0, outfit: "dress", colorHex: "#C99A5E", hair: 1, plain: true, mood: "flat", look: "left", arms: [[-60, -110], [-30, -90]] };
    const RA = K.rig(A), RB = K.rig(B);
    s += stand(H, A, 660, 900, 1.55, spots + H.at(f1(RA.hand[1][0] + 6), f1(RA.hand[1][1] - 8), 0.7, slice(true)) + `<circle cx="${f1(RA.hand[0][0] + 22)}" cy="${f1(RA.hand[0][1] - 10)}" r="5" fill="${C.med}" stroke="${ink}" stroke-width="1.4"/>`);
    s += stand(H, B, 1260, 900, 1.55, spots + H.at(f1(RB.hand[0][0] - 6), f1(RB.hand[0][1] - 8), 0.7, slice(true)));
    // the calendar on its rock, a page tearing off
    // (KIT.props.calendar, drawn here wider so the six-figure year fits)
    s += `<path d="M90,760 Q110,690 240,690 Q370,690 390,760 Z" fill="#5A4A3C" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="120" y="540" width="240" height="150" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><rect x="132" y="552" width="216" height="132" fill="#FBF5E4" stroke="${ink}" stroke-width="3"/>` +
      `<rect x="132" y="552" width="216" height="34" fill="${C.war}" stroke="${ink}" stroke-width="3"/><text x="240" y="578" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="24" letter-spacing="2" fill="${C.cream}">YEAR</text>` +
      `<text x="240" y="656" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="50" fill="${ink}">150,000</text>` +
      [170, 310].map((x) => `<rect x="${x - 6}" y="530" width="12" height="30" rx="4" fill="${C.yellow}" stroke="${ink}" stroke-width="2.4"/>`).join("") +
      `<g transform="translate(420,470) rotate(28)"><rect x="-60" y="-50" width="120" height="80" fill="#FBF5E4" stroke="${ink}" stroke-width="3"/><rect x="-60" y="-50" width="120" height="20" fill="${C.war}" stroke="${ink}" stroke-width="3"/></g>` +
      `<g transform="translate(520,380) rotate(-20)"><rect x="-50" y="-40" width="100" height="66" fill="#FBF5E4" stroke="${ink}" stroke-width="3"/><rect x="-50" y="-40" width="100" height="16" fill="${C.war}" stroke="${ink}" stroke-width="3"/></g>`;
    return { svg: s, alt: "The cave: two cavemen in hide spots by the campfire flick teal mold off their slices of bread onto a glowing heap at their feet, while behind them a row of sick cavemen with red chest lights x-ray one after another into grinning skeletons; on a rock, a tear-off calendar reads YEAR 150,000, a page flying off." };
  },

  "human-greed"(H, fid) {
    const { K, C } = H, ink = C.line, S = K.STUDIO;
    // the studio light flared to full: a bigger, brighter pool behind her (drawn over the set's own wall)
    const wall = K.studioWall() + `<ellipse cx="${S.pool[0]}" cy="${S.pool[1]}" rx="${S.pool[2] * 1.5}" ry="${S.pool[3] * 1.4}" fill="#F3E5BE"/><ellipse cx="${S.pool[0]}" cy="${S.pool[1] - 30}" rx="${S.pool[2] * 1.05}" ry="${S.pool[3] * 1.0}" fill="#FBF3D8"/>` +
      `<rect y="${S.rail}" width="1920" height="${1080 - S.rail}" fill="#B98C5A"/><rect y="${S.rail - 6}" width="1920" height="12" fill="${C.rust}"/>`;
    // the giant hamster wheel at stage right, on its stand, the fat cat running in it, on fire
    const W = [1510, 500], WR = 340;
    let wheel = `<path d="M${W[0] - 230},1080 L${W[0]},${W[1]} L${W[0] + 230},1080" fill="none" stroke="${ink}" stroke-width="22"/><path d="M${W[0] - 230},1080 L${W[0]},${W[1]} L${W[0] + 230},1080" fill="none" stroke="${C.slate}" stroke-width="14"/>`;
    wheel += `<circle cx="${W[0]}" cy="${W[1]}" r="${WR}" fill="none" stroke="${ink}" stroke-width="26"/><circle cx="${W[0]}" cy="${W[1]}" r="${WR}" fill="none" stroke="${C.rust}" stroke-width="16"/>`;
    for (let i = 0; i < 10; i++) { const a = (i * Math.PI) / 5 + 0.2; wheel += `<path d="M${W[0]},${W[1]} L${f1(W[0] + WR * Math.cos(a))},${f1(W[1] + WR * Math.sin(a))}" stroke="${ink}" stroke-width="5" opacity="0.7"/>`; }
    wheel += `<circle cx="${W[0]}" cy="${W[1]}" r="22" fill="${C.yellow}" stroke="${ink}" stroke-width="5"/>`;
    for (let i = 0; i < 30; i++) { const a = (i * Math.PI) / 15; wheel += `<path d="M${f1(W[0] + (WR - 8) * Math.cos(a))},${f1(W[1] + (WR - 8) * Math.sin(a))} L${f1(W[0] + (WR + 8) * Math.cos(a))},${f1(W[1] + (WR + 8) * Math.sin(a))}" stroke="${C.cream}" stroke-width="4"/>`; }
    // the fat cat: dollar eyes, running, a stick strapped to his top hat with a plain paper dangling in front of his nose
    const FC = K.castOpts("richHuman", { mood: "greedy", arms: [[40, 80], [60, 100]] });
    const Rf = K.rig(FC), hat = Rf.top;
    const stick = `<path d="M${f1(hat[0] - 6)},${f1(hat[1] - 30)} L${f1(hat[0] + 118)},${f1(hat[1] - 60)}" stroke="${WOOD_DARK}" stroke-width="5" stroke-linecap="round"/>` +
      `<path d="M${f1(hat[0] + 116)},${f1(hat[1] - 60)} V${f1(hat[1] - 18)}" stroke="${ink}" stroke-width="1.6"/>` +
      H.at(f1(hat[0] + 116), f1(hat[1] - 2), 0.45, K.money("plain", 0).replace('class="legs"', 'class="legs" opacity="0"'));
    // the cable from the axle to the knife switch on the lectern (behind him)
    wheel += `<path d="M${W[0]},${W[1]} C1300,760 1120,700 990,770" fill="none" stroke="${ink}" stroke-width="12"/><path d="M${W[0]},${W[1]} C1300,760 1120,700 990,770" fill="none" stroke="#3A3A3A" stroke-width="6"/>`;
    // on fire at the hips and shoulders, so the top hat and the dollar eyes still read
    const fire = K.flames(-2, Rf.hipY + 8, 0.95) + K.flames(Rf.shoulder[0][0] - 8, Rf.shoulder[0][1] + 12, 0.55) + K.flames(Rf.shoulder[1][0] + 8, Rf.shoulder[1][1] + 12, 0.55);
    wheel += stand(H, FC, W[0] - 40, W[1] + WR - 14, 2.3, stick + fire);
    // speed lines
    wheel += [[1150, 400], [1140, 500], [1160, 600]].map(([x, y]) => `<path d="M${x},${y} h-60" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`).join("");
    const cable = "";
    const sw = `<rect x="900" y="756" width="96" height="30" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><path d="M918,760 L978,742" stroke="${ink}" stroke-width="10" stroke-linecap="round"/><path d="M918,760 L978,742" stroke="#C9C2B5" stroke-width="5" stroke-linecap="round"/>` +
      `<rect x="972" y="728" width="20" height="22" rx="4" fill="${C.war}" stroke="${ink}" stroke-width="3"/>` + K.star(1000, 724, 22, C.yellow);
    const svg = wall + wheel + H.wish(S.wish.x, S.wish.y, S.wish.w, "excited-open", "fist") + K.lectern() + cable + sw;
    return { svg, alt: "The host's set with the studio light flared to full: Wishonia at her lectern, fist raised, has thrown a knife switch; at stage right the fat cat runs in a giant hamster wheel, harnessed to a paper dangling from a stick on his own top hat, on fire all over and still running, dollar signs in his eyes; a cable runs from the wheel's axle to the switch." };
  },
};
