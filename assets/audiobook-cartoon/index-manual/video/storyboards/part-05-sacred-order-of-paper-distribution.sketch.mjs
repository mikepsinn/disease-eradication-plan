// Part 5 storyboard sketches (v3, the 1950s atomic-age film look): each scene's key frame on a 1920 x 1080 frame,
// drawn with the production art (H.K: kit.js, film.js and the props). A host shot is the studio set with Wishonia at
// her lectern (H.host); a plate frame is one framing, as the camera sees it at that moment, not the whole plate.
// Used by tools/storyboard-sheet.mjs. Every id carries fid, so frames on one page do not collide.

const f = (n) => (+n).toFixed(1);
const at = (x, y, s, inner, rot = 0) => `<g transform="translate(${f(x)},${f(y)})${rot ? ` rotate(${f(rot)})` : ""}${s !== 1 ? ` scale(${s})` : ""}">${inner}</g>`;
const SKY = "#EFE3C4", GROUND = "#C8B07B", EDGE = "#B09363", CHAIR = "#3A4766", WHITE = "#FBF6E6";
// Fraunces Black advance widths (em), from assets/js/props/title.js, to place things at the end of a heading line.
const FCH = " ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const FADV = [0.174, 0.733, 0.716, 0.669, 0.772, 0.639, 0.603, 0.728, 0.819, 0.408, 0.548, 0.795, 0.608, 0.938, 0.756, 0.758, 0.698, 0.749, 0.758, 0.596, 0.688, 0.726, 0.729, 1.096, 0.721, 0.673, 0.613];
const fWidth = (text, size) => [...text].reduce((w, ch) => w + (FADV[FCH.indexOf(ch)] ?? 0.6), 0) * size;

function tools(H) {
  const { K, C } = H, ink = C.line;
  const T = {};
  T.ink = ink;
  // a person standing with feet on feetY, k times person size
  T.person = (o, x, feetY, k, extra = "") => at(x, feetY - 100 * k, k, K.person(o) + extra);
  // a plain bill without legs
  T.bill = (kind = "plain") => K.money(kind).replace(/<path class="legs"[^>]*\/>/, "");
  T.field = (horizon, sky = SKY, ground = GROUND) =>
    `<rect width="1920" height="${horizon}" fill="${sky}"/><rect y="${horizon}" width="1920" height="${1080 - horizon}" fill="${ground}"/><path d="M0,${horizon} H1920" stroke="${EDGE}" stroke-width="3"/>`;
  T.poly = (pts, fill, sw = 4, extra = "") => `<path d="M${pts.map((p) => f(p[0]) + "," + f(p[1])).join(" L")} Z" fill="${fill}" stroke="${ink}" stroke-width="${sw}" stroke-linejoin="miter" ${extra}/>`;
  T.light = (o) => {
    const m = K.person(o).match(/class="chest-light" cx="([-\d.]+)" cy="([-\d.]+)"/);
    return m ? [+m[1], +m[2]] : [0, 0];
  };
  // ── The Rich Human's hill: a dome of plain bills packed in rows on a dark green mound (canvas px) ──
  T.hill = (cx, base, half, height, seed = 5150, bs = 0.5) => {
    const top = (x) => base - height * Math.sqrt(Math.max(0, 1 - (x / half) ** 2));
    const pts = [];
    for (let i = 0; i <= 40; i++) { const x = -half + (2 * half * i) / 40; pts.push(`${f(cx + x)},${f(top(x) - 6)}`); }
    let out = `<path d="M${f(cx - half - 10)},${base} L${pts.join(" L")} L${f(cx + half + 10)},${base} Z" fill="${C.moneyDark}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>`;
    const rnd = K.rng(seed), rh = 46 * bs, rows = Math.ceil(height / rh);
    for (let i = rows - 1; i >= 0; i--) {
      const hgt = rh * (i + 0.5);
      if (hgt > height - 4) continue;
      const hw = half * Math.sqrt(Math.max(0, 1 - (hgt / height) ** 2)) - 26 * bs;
      if (hw < 24 * bs) continue;
      const y = base - rh * (i + 0.55), n = Math.max(1, Math.round((2 * hw) / (84 * bs))), sp = (2 * hw) / n;
      for (let k = 0; k < n; k++) {
        const bx = cx - hw + sp * (k + 0.5) + (i % 2 ? sp * 0.22 : -sp * 0.22) + (rnd() - 0.5) * 6;
        out += at(bx, y + (rnd() - 0.5) * 5, bs, T.bill(), (rnd() - 0.5) * 16);
      }
    }
    return out + `<path d="M${f(cx - half - 16)},${base + 2} H${f(cx + half + 16)}" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`;
  };
  // ── The swivel chair, in person units around its sitter (his feet at y 100 hide behind the seat front) ──
  T.chairBack = () => {
    let tufts = "";
    for (let y = -30; y <= 56; y += 22) for (let x = -32; x <= 32; x += 21) tufts += `<circle cx="${x + ((y / 22) % 2 ? 10 : 0)}" cy="${y}" r="2.2" fill="${ink}"/>`;
    return T.poly([[-58, 84], [-63, -28], [-50, -54], [50, -54], [63, -28], [58, 84]], CHAIR, 4.4) + tufts +
      `<path d="M-44,-44 H44" stroke="${C.peri}" stroke-width="3" opacity="0.7"/>`;
  };
  T.chairFront = () => T.poly([[-68, 78], [68, 78], [64, 104], [-64, 104]], CHAIR, 4.4) + `<path d="M-60,84 H60" stroke="${C.peri}" stroke-width="3" opacity="0.7"/>` +
    T.poly([[-78, 36], [-58, 36], [-58, 100], [-78, 100]], CHAIR, 4) + T.poly([[58, 36], [78, 36], [78, 100], [58, 100]], CHAIR, 4) +
    T.poly([[-7, 104], [7, 104], [7, 134], [-7, 134]], C.slate, 3.4) +
    `<path d="M0,134 L-58,150 M0,134 L58,150 M0,134 L-26,156 M0,134 L26,156" stroke="${ink}" stroke-width="7" stroke-linecap="round"/>` +
    [[-58, 150], [58, 150], [-26, 156], [26, 156]].map(([x, y]) => `<circle cx="${x}" cy="${y + 5}" r="5.5" fill="${C.slate}" stroke="${ink}" stroke-width="2.4"/>`).join("");
  // the UNREALISTIC sticker from Part 4, in the face's units, on the forehead
  T.sticker = `<g transform="translate(1,-12) rotate(-9)"><rect x="-17.5" y="-5" width="35" height="10" fill="${C.cream}" stroke="${ink}" stroke-width="1"/><text x="0" y="2.3" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="6.3" letter-spacing="0.2" fill="${C.war}">UNREALISTIC</text></g>`;
  T.richHuman = (extra = {}, opts = {}) => {
    const o = K.castOpts("richHuman", extra);
    let svg = K.person(o);
    if (opts.sticker !== false) svg = svg.replace("<!--face-end-->", T.sticker + "<!--face-end-->");
    if (opts.button) { const L = T.light(o); svg += T.button(L[0] + 9, L[1] - 15, 10); }
    return { o, svg, rig: K.rig(o) };
  };
  // the "I PREFER LIVING" button: a round cream pin, navy rim, teal letters
  T.button = (x, y, r) => `<g transform="translate(${f(x)},${f(y)})"><circle r="${r}" fill="${C.cream}" stroke="${ink}" stroke-width="${f(r * 0.16)}"/><circle r="${f(r * 0.8)}" fill="none" stroke="${C.med}" stroke-width="${f(r * 0.07)}"/>` +
    `<text y="${f(-r * 0.06)}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="${f(r * 0.34)}" fill="${C.med}">I PREFER</text><text y="${f(r * 0.4)}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="${f(r * 0.44)}" fill="${C.med}">LIVING</text></g>`;
  // ── The Reaper's tally clipboard (its top left at 0,0, w wide): a heart box and a skull box, then tally marks ──
  T.tally = (w = 60, ticked = null) => {
    const h = w * 1.36, u = w / 60;
    let out = T.poly([[0, 0], [w, 0], [w, h], [0, h]], "#B98A55", 2.4) + `<rect x="${f(4 * u)}" y="${f(7 * u)}" width="${f(w - 8 * u)}" height="${f(h - 11 * u)}" fill="${C.cream}" stroke="${ink}" stroke-width="1.2"/>` +
      T.poly([[w * 0.32, -4 * u], [w * 0.68, -4 * u], [w * 0.68, 6 * u], [w * 0.32, 6 * u]], C.slate, 1.8);
    const box = (x, y) => `<rect x="${f(x)}" y="${f(y)}" width="${f(9 * u)}" height="${f(9 * u)}" fill="${WHITE}" stroke="${ink}" stroke-width="${f(1.4 * u)}"/>`;
    const heart = (x, y) => `<path d="M${f(x)},${f(y + 2.5 * u)} c${f(-1.5 * u)},${f(-4 * u)} ${f(-7 * u)},${f(-1.5 * u)} ${f(-3.6 * u)},${f(2.6 * u)} l${f(3.6 * u)},${f(3.4 * u)} l${f(3.6 * u)},${f(-3.4 * u)} c${f(3.4 * u)},${f(-4.1 * u)} ${f(-2.1 * u)},${f(-6.6 * u)} ${f(-3.6 * u)},${f(-2.6 * u)} Z" fill="${C.war}" stroke="${ink}" stroke-width="${f(0.8 * u)}"/>`;
    const skull = (x, y) => `<circle cx="${f(x)}" cy="${f(y)}" r="${f(3.6 * u)}" fill="${WHITE}" stroke="${ink}" stroke-width="${f(0.9 * u)}"/><rect x="${f(x - 2 * u)}" y="${f(y + 2.4 * u)}" width="${f(4 * u)}" height="${f(2.4 * u)}" fill="${WHITE}" stroke="${ink}" stroke-width="${f(0.7 * u)}"/><circle cx="${f(x - 1.4 * u)}" cy="${f(y - 0.3 * u)}" r="${f(1 * u)}" fill="${ink}"/><circle cx="${f(x + 1.4 * u)}" cy="${f(y - 0.3 * u)}" r="${f(1 * u)}" fill="${ink}"/>`;
    out += box(9 * u, 12 * u) + heart(25 * u, 13.5 * u) + box(34 * u, 12 * u) + skull(50 * u, 16.5 * u);
    if (ticked === "heart") out += K.tick(7 * u, 8 * u, 13 * u, C.med).replace('stroke-dashoffset="1"', 'stroke-dashoffset="0"');
    let tallies = "";
    for (let r = 0; r < 6; r++) {
      const y = 30 * u + r * 8.5 * u;
      if (y > h - 9 * u) break;
      for (let g = 0; g < 3; g++) {
        const x0 = 9 * u + g * 15 * u;
        for (let k = 0; k < 4; k++) tallies += `M${f(x0 + k * 2.6 * u)},${f(y)} v${f(6 * u)} `;
        tallies += `M${f(x0 - 1.2 * u)},${f(y + 5 * u)} L${f(x0 + 9 * u)},${f(y + 1 * u)} `;
      }
    }
    return out + `<path d="${tallies}" fill="none" stroke="${ink}" stroke-width="${f(1.1 * u)}" stroke-linecap="round"/>`;
  };
  // ── A white die in 3/4, its base center on (0,0), s the front face; top (pips on the top face), fr (front) ──
  T.die = (s, top, fr, side) => {
    const dx = s * 0.34, dy = -s * 0.28, h = s / 2;
    const PIPS = { 1: [[0.5, 0.5]], 2: [[0.25, 0.25], [0.75, 0.75]], 3: [[0.22, 0.22], [0.5, 0.5], [0.78, 0.78]], 4: [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]], 5: [[0.25, 0.25], [0.75, 0.25], [0.5, 0.5], [0.25, 0.75], [0.75, 0.75]] };
    let out = T.poly([[-h, -s], [h, -s], [h, 0], [-h, 0]], WHITE, 4) + T.poly([[-h, -s], [-h + dx, -s + dy], [h + dx, -s + dy], [h, -s]], "#FFFDF4", 4) + T.poly([[h, -s], [h + dx, -s + dy], [h + dx, dy], [h, 0]], "#D9D0BB", 4);
    (PIPS[fr] || []).forEach(([u, v]) => { out += `<circle cx="${f(-h + u * s)}" cy="${f(-s + v * s)}" r="${f(s * 0.085)}" fill="${ink}"/>`; });
    (PIPS[side] || []).forEach(([u, v]) => { out += `<ellipse cx="${f(h + u * dx)}" cy="${f(-s * (1 - v) + u * dy)}" rx="${f(s * 0.04)}" ry="${f(s * 0.075)}" fill="${ink}"/>`; });
    (PIPS[top] || []).forEach(([u, v]) => { out += `<ellipse cx="${f(-h + u * s + v * dx)}" cy="${f(-s + v * dy)}" rx="${f(s * 0.11)}" ry="${f(s * 0.06)}" fill="${C.war}" stroke="${ink}" stroke-width="1.5"/>`; });
    return out;
  };
  // a homburg on (0,0) (its brim), about 80 wide: a gray crown with a dent down the middle, a navy band, the brim
  // curled up at both sides (the bowler is YOU's, so the dice businessman wears this)
  T.homburg = () => `<path d="M-24,0 L-22,-30 Q-12,-37 -2,-31 L0,-27 L2,-31 Q12,-37 22,-30 L24,0 Z" fill="#5B6476" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>` +
    `<path d="M0,-27 V-12" stroke="#3E4658" stroke-width="2.4"/><path d="M-23,-7 H23" stroke="${C.navy}" stroke-width="6"/>` +
    `<path d="M-41,-7 Q-38,3 -24,2 H24 Q38,3 41,-7 Q44,7 30,9 H-30 Q-44,7 -41,-7 Z" fill="#5B6476" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>`;
  // ── The Super PAC (Parts 17, 20 and 23 draw it from here): a rust canvas backpack, its base center on (0,0),
  // about 400 wide and 500 tall at scale 1; a darker top flap open like a mouth; navy straps as arms, fists on its
  // hips; a front pocket where the cream SUPER PAC patch (orange inner rule, navy Oswald) is sewn over BRIBERY,
  // painted in cream on the unfaded canvas; a war-red cape tied at its top. patch: "on" (flat) or "peeled"
  // (hanging from its top left corner, BRIBERY showing). No face, no mask.
  T.superPac = (patch = "on") => {
    let pac = T.poly([[110, -470], [330, -330], [310, 0], [150, -30]], C.war, 5);
    pac += T.poly([[-190, 0], [-206, -400], [-156, -462], [156, -462], [206, -400], [190, 0]], C.rust, 6) +
      `<path d="M-176,-24 L-188,-392 M176,-24 L188,-392" stroke="#A35A3A" stroke-width="5"/>`;
    pac += T.poly([[-156, -462], [156, -462], [130, -500], [-130, -500]], "#6E3622", 5);
    pac += `<path d="M-196,-370 L-280,-250 L-206,-170" fill="none" stroke="${C.navy}" stroke-width="28" stroke-linejoin="round" stroke-linecap="round"/><path d="M196,-370 L280,-250 L206,-170" fill="none" stroke="${C.navy}" stroke-width="28" stroke-linejoin="round" stroke-linecap="round"/>`;
    pac += T.poly([[-150, -330], [150, -330], [150, -170], [-150, -170]], "#A35A3A", 4) +
      `<text x="0" y="-215" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="84" letter-spacing="4" fill="${C.cream}">BRIBERY</text>`;
    const patchSvg = T.poly([[-150, -330], [150, -330], [150, -170], [-150, -170]], C.cream, 5) +
      `<rect x="-140" y="-320" width="280" height="140" fill="none" stroke="${C.orange}" stroke-width="3"/><text x="0" y="-228" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="60" letter-spacing="3" fill="${ink}">SUPER PAC</text>`;
    const peeled = T.poly([[-150, -330], [150, -330], [150, -230], [-150, -230]], C.cream, 5) +
      `<rect x="-140" y="-320" width="280" height="80" fill="none" stroke="${C.orange}" stroke-width="3"/><text x="0" y="-258" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="60" letter-spacing="3" fill="${ink}">SUPER PAC</text>`;
    return pac + (patch === "peeled" ? `<g transform="rotate(-24 -150 -330)">${peeled}</g>` : patchSvg);
  };
  // a puff of dust or smoke
  T.puff = (x, y, r, op = 0.85) => `<g opacity="${op}"><circle cx="${f(x)}" cy="${f(y)}" r="${f(r)}" fill="#E9E1CF" stroke="${ink}" stroke-width="3"/><circle cx="${f(x + r * 0.9)}" cy="${f(y + r * 0.2)}" r="${f(r * 0.7)}" fill="#E9E1CF" stroke="${ink}" stroke-width="3"/><circle cx="${f(x - r * 0.8)}" cy="${f(y + r * 0.3)}" r="${f(r * 0.6)}" fill="#E9E1CF" stroke="${ink}" stroke-width="3"/></g>`;
  // motion or impact lines from a center, n of them between angles a0 and a1 (deg), r0 to r1 long
  T.lines = (x, y, r0, r1, a0, a1, n, w = 6, col = ink) => {
    let d = "";
    for (let i = 0; i < n; i++) { const a = ((a0 + ((a1 - a0) * i) / Math.max(1, n - 1)) * Math.PI) / 180; d += `M${f(x + r0 * Math.cos(a))},${f(y + r0 * Math.sin(a))} L${f(x + r1 * Math.cos(a))},${f(y + r1 * Math.sin(a))} `; }
    return `<path d="${d}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`;
  };
  // the Grim Reaper without his scythe (he carries the clipboard instead)
  T.reaper = () => K.reaper({ pose: "puppet", arms: [0, 35] });
  // the neon infinity sign: a lying figure eight, a rust tube with a bright core, on two little wires
  T.neon = (x, y, w) => {
    const a = w / 2, b = w * 0.22;
    let d = "";
    for (let i = 0; i <= 64; i++) { const t = (i / 64) * Math.PI * 2, s = Math.sin(t), c = Math.cos(t), den = 1 + s * s; d += (i ? " L" : "M") + f(x + (a * c) / den) + "," + f(y + (b * 2 * s * c) / den); }
    return `<path d="M${f(x - a * 0.6)},${f(y - b * 2.4)} V${f(y - b * 0.4)} M${f(x + a * 0.6)},${f(y - b * 2.4)} V${f(y - b * 0.4)}" stroke="${ink}" stroke-width="3"/>` +
      `<path d="${d} Z" fill="none" stroke="${C.yellow}" stroke-width="${f(w * 0.12)}" opacity="0.35" stroke-linejoin="round"/>` +
      `<path d="${d} Z" fill="none" stroke="${ink}" stroke-width="${f(w * 0.06)}" stroke-linejoin="round"/><path d="${d} Z" fill="none" stroke="${C.orange}" stroke-width="${f(w * 0.042)}" stroke-linejoin="round"/>` +
      `<path d="${d} Z" fill="none" stroke="#FFE9B8" stroke-width="${f(w * 0.014)}" stroke-linejoin="round"/>`;
  };
  return T;
}

export default {
  // ── 1 · the period title card: the hooded electron papers file into the top hat at the end of the heading ──
  "sacred-order-title"(H, fid) {
    const { K, C } = H, T = tools(H), ink = C.line;
    const txt = (x, y, size, text) => `<text x="${f(x + size * 0.035)}" y="${f(y + size * 0.05)}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${size}" fill="#07142A">${text}</text>` +
      `<text x="${f(x)}" y="${f(y)}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${size}" fill="${C.cream}">${text}</text>`;
    const AX = 960, AY = 235, R = 190, BIG = 128, LINE2 = "PAPER DISTRIBUTION", L2X = 880, L2Y = 815;
    const end = L2X + fWidth(LINE2, BIG) / 2, capTop = L2Y - BIG * 0.7;
    // the emblem with its electrons gone: three orbits and the nucleus
    let out = `<rect width="1920" height="1080" fill="${C.navy}"/>` + K.atom(AX, AY, R, C.cream);
    out += txt(960, 560, 78, "THE SACRED ORDER OF") + txt(L2X, L2Y, BIG, LINE2);
    // the upturned top hat, standing on its crown on the baseline at the end of the line, like a full stop
    const hatX = end + 105, hb = L2Y;
    out += `<path d="M${hatX - 52},${hb} H${hatX + 52} L${hatX + 56},${hb - 104} H${hatX + 92} L${hatX + 84},${hb - 122} H${hatX - 84} L${hatX - 92},${hb - 104} H${hatX - 56} Z" fill="none" stroke="${C.cream}" stroke-width="14" stroke-linejoin="round"/>` +
      T.poly([[hatX - 52, hb], [hatX + 52, hb], [hatX + 56, hb - 104], [hatX - 56, hb - 104]], C.slate, 5) +
      `<rect x="${hatX - 54}" y="${hb - 34}" width="108" height="15" fill="${C.war}"/>` +
      T.poly([[hatX - 92, hb - 104], [hatX + 92, hb - 104], [hatX + 84, hb - 122], [hatX - 84, hb - 122]], C.slate, 5) +
      `<path d="M${hatX - 58},${hb - 113} H${hatX + 58}" stroke="#0B1220" stroke-width="10"/>`;
    // a hooded paper: a plain bill on its legs under a brown monk's cowl, its portrait looking out of the hood
    const hood = `<path d="M-56,12 L-54,-18 Q-46,-48 -10,-54 L2,-70 L10,-54 Q46,-46 56,-18 L58,12 L42,12 L40,-10 Q22,-27 0,-27 Q-22,-27 -40,-10 L-42,12 Z" fill="#6B4A2F" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
      `<path d="M-30,-36 Q0,-46 30,-36" fill="none" stroke="#8C6440" stroke-width="3"/>`;
    const monk = (legs) => K.money("plain", legs) + hood;
    const PK = 1.25, py = capTop - 48 * PK - 4;
    // the censer on a chain from the second paper's front corner, puffing
    const censer = `<path d="M46,8 L66,44" stroke="${C.yellow}" stroke-width="3"/><path d="M55,44 h22 l-3,15 h-16 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/><path d="M68,32 q-9,-14 2,-24 q9,-10 0,-22" fill="none" stroke="${C.cream}" stroke-width="4" opacity="0.7" stroke-linecap="round"/>`;
    out += at(end - 420, py, PK, monk(0)) + at(end - 250, py - 4, PK, monk(1) + censer);
    // the first one dives headfirst into the hat
    out += at(hatX - 30, hb - 150, PK, monk(1), 70);
    out += T.lines(hatX, hb - 130, 110, 140, -160, -110, 3, 5, C.cream) + T.lines(hatX, hb - 130, 110, 140, -70, -20, 3, 5, C.cream);
    return { svg: out, alt: "The period title card: THE SACRED ORDER OF PAPER DISTRIBUTION in cream on navy under the atom, its orbits empty; the electron papers, in monk hoods, walk in single file along the top of DISTRIBUTION, one swinging a censer, and the first dives into an upturned top hat standing at the end of the line like a full stop." };
  },

  // ── 2 · host: the pull-down chart of the money double helix, unrolled down out of the frame ──
  "sacred-scroll"(H, fid) {
    const { K, C } = H, T = tools(H), ink = C.line;
    const X0 = 1230, X1 = 1730, CX = (X0 + X1) / 2;
    let chart = T.poly([[X0, 40], [X1, 40], [X1, 1120], [X0, 1120]], C.cream, 5) + `<rect x="${X0 + 16}" y="58" width="${X1 - X0 - 32}" height="1100" fill="none" stroke="${C.orange}" stroke-width="3"/>`;
    // the helix: two navy strands, every rung a plain bill stretched across
    const A = 150, P = 330;
    let s1 = "", s2 = "", rungs = "";
    for (let y = 70; y <= 1100; y += 10) {
      const a = ((y - 70) / P) * Math.PI * 2, x1 = CX + A * Math.sin(a), x2 = CX - A * Math.sin(a);
      s1 += (y === 70 ? "M" : " L") + f(x1) + "," + y;
      s2 += (y === 70 ? "M" : " L") + f(x2) + "," + y;
    }
    for (let y = 95; y <= 1100; y += 55) {
      const a = ((y - 70) / P) * Math.PI * 2, w = Math.abs(2 * A * Math.sin(a));
      if (w < 40) continue;
      rungs += `<g transform="translate(${CX},${y}) scale(${f(w / 96 * 0.92)},0.5)">${T.bill()}</g>`;
    }
    chart += rungs + `<path d="${s1}" fill="none" stroke="${ink}" stroke-width="10" stroke-linecap="round"/><path d="${s2}" fill="none" stroke="${C.slate}" stroke-width="10" stroke-linecap="round"/>`;
    // the roller at the top of the frame on two brackets
    const roller = T.poly([[X0 - 40, 14], [X1 + 40, 14], [X1 + 40, 50], [X0 - 40, 50]], C.tan, 5) + `<path d="M${X0 - 34},26 H${X1 + 34}" stroke="#D8A877" stroke-width="5"/>` +
      T.poly([[X0 - 62, 0], [X0 - 40, 0], [X0 - 40, 62], [X0 - 62, 62]], C.slate, 4) + T.poly([[X1 + 40, 0], [X1 + 62, 0], [X1 + 62, 62], [X1 + 40, 62]], C.slate, 4);
    const motion = `<path d="M${X0 - 30},380 v120 M${X0 - 30},560 v140 M${X1 + 30},300 v150 M${X1 + 30},620 v130" stroke="${ink}" stroke-width="5" stroke-linecap="round" opacity="0.55"/>`;
    return {
      svg: H.host("lookright-smile", "point-right", chart + roller + motion),
      alt: "Wishonia at her lectern points at a classroom pull-down chart on the wall to her right: a money double helix, two navy strands whose rungs are plain green bills, unrolling from its roller at the top of the frame down out of the bottom.",
    };
  },

  // ── 3 · plate the-hill, on "but": the dice in the dust on snake eyes, their suit in a heap ──
  "step-1-dice-in-a-suit"(H, fid) {
    const { K, C } = H, T = tools(H), ink = C.line;
    let out = T.field(560);
    // the far field: a row of little hills on the horizon
    for (let x = 30; x < 1920; x += 92) out += `<path d="M${x - 40},562 Q${x},${540 - (x % 3) * 3} ${x + 40},562 Z" fill="${C.moneyDark}" stroke="${ink}" stroke-width="2" opacity="0.55"/>`;
    // the hill and the Rich Human standing on his chair, reaching for the dotted stack, his eyes ringing up
    const HX = 1340, HB = 780, HH = 330, HT = HB - HH, K1 = 1.3;
    out += T.hill(HX, HB, 470, HH);
    const chairY = HT + 6 - 150 * K1;
    const rh = T.richHuman({ mood: "greedy", arms: [[-162, -176], [158, 172]] });
    out += at(HX, chairY, K1, T.chairBack()) + at(HX, chairY + 78 * K1 - 100 * K1, K1, rh.svg) + at(HX, chairY, K1, T.chairFront());
    // the dotted stack floating just out of reach
    let ghost = "";
    for (let i = 0; i < 9; i++) ghost += `<rect x="${HX + 20}" y="${f(30 + i * 13)}" width="190" height="13" fill="none" stroke="${ink}" stroke-width="3" stroke-dasharray="9 7"/>`;
    out += `<rect x="${HX + 20}" y="30" width="190" height="117" fill="${C.cream}" opacity="0.45"/>` + ghost;
    // the dice in the dust, snake eyes, and the empty pinstripe suit and homburg in a heap beside them
    const GY = 880;
    out += T.puff(560, GY - 30, 34, 0.7) + T.puff(1010, GY - 18, 26, 0.6);
    // the empty suit: a crumpled jacket with pinstripes, the shirt collar, the tie and the homburg on top; the briefcase
    const jacket = [[-118, 0], [-104, -58], [-50, -84], [-14, -64], [16, -88], [78, -68], [120, -10], [116, 0]];
    let suit = T.poly(jacket, "#24304D", 4.4);
    for (let x = -96; x <= 100; x += 18) suit += `<path d="M${x},-2 L${x + 10},-70" stroke="#5C6F8E" stroke-width="2" opacity="0.8"/>`;
    suit += T.poly([[-10, -66], [2, -46], [14, -68]], WHITE, 3) + T.poly([[1, -50], [9, -40], [3, -10], [-5, -40]], C.war, 2.6);
    suit += at(-62, -78, 1.25, T.homburg(), -14);
    suit += T.poly([[132, -46], [208, -46], [208, 0], [132, 0]], "#6B4A2F", 4) + `<path d="M156,-46 V-56 H184 V-46" fill="none" stroke="${ink}" stroke-width="4"/>`;
    out += at(430, GY, 1.35, suit);
    out += at(770, GY, 1, T.die(150, 1, 3, 2)) + at(960, GY - 26, 1, T.die(132, 1, 2, 4));
    out += T.lines(840, GY - 210, 40, 70, -150, -30, 5, 5);
    return { svg: out, alt: "Low on the bare ground at the foot of the hill: two white dice face up on snake eyes in the dust, their empty pinstripe suit, tie, homburg and briefcase in a heap beside them; behind, the Rich Human stands on his chair on top of the hill of bills with dollar-sign eyes, reaching up for a dotted stack floating out of reach." };
  },

  // ── 4 · plate the-hill, after "living.": the spotlight on our fat cat and his new button ──
  "2800-top-hats"(H, fid) {
    const { K, C } = H, T = tools(H), ink = C.line;
    const HZ = 330, DSKY = "#8D8574", DGROUND = "#76694F";
    let out = T.field(HZ, DSKY, DGROUND);
    // rows of little hills to the horizon, a tiny top hat on each
    let rows = "";
    const DK = [];
    for (let d = 300; d >= 14; d *= 0.8) DK.push(d);
    DK.reverse().forEach((dk, k) => {
      const base = HZ + dk, sc = dk / 300, w = 230 * sc, h = 70 * sc, step = 300 * sc;
      for (let x = -step * 0.5 * (k % 2); x < 1920 + step; x += step) {
        rows += `<path d="M${f(x - w / 2)},${f(base)} Q${f(x)},${f(base - h * 1.7)} ${f(x + w / 2)},${f(base)} Z" fill="#4C5C45" stroke="${ink}" stroke-width="${f(Math.max(1, 3 * sc))}"/>`;
        if (sc > 0.12) rows += at(x, base - h * 0.85, sc * 1.1, K.tophat("#1A2238"));
      }
    });
    out += rows;
    out += `<text x="470" y="250" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="168" letter-spacing="4" fill="${C.cream}">2,800</text>`;
    // the dusk over everything but the spotlight's cone
    const cone = [[1000, -20], [1150, -20], [1420, 1100], [720, 1100]];
    out += `<path fill-rule="evenodd" d="M-20,-20 H1940 V1100 H-20 Z M${cone.map((p) => p.join(",")).join(" L")} Z" fill="#1A1408" opacity="0.32"/>`;
    // our hill in front, lit, and the Rich Human in his chair, waving the pencil, the button on his lapel
    const HX = 1070, HB = 1150, HH = 520, K4 = 2.15;
    out += T.hill(HX, HB, 640, HH, 77, 0.62);
    const chairY = HB - HH + 4 - 150 * K4;
    const rh = T.richHuman({ mood: "smug", look: null, arms: [[22, 72], [150, 166]] }, { button: true });
    const hand = rh.rig.hand[1];
    const pencil = at(hand[0] - 6, hand[1] + 4, 0.34, K.pencil(), -64);
    out += at(HX, chairY, K4, T.chairBack()) + at(HX, chairY, K4, rh.svg + pencil) + at(HX, chairY, K4, T.chairFront());
    // the lit top hat: rays round it
    const hatX = HX + (rh.rig.top[0] + 1) * K4, hatY = chairY + (rh.rig.top[1] - 22) * K4;
    out += T.lines(hatX, hatY, 70, 110, -165, -15, 7, 6, C.yellow);
    out += `<path d="M${cone.map((p) => p.join(",")).join(" L")} Z" fill="#FFF4D0" opacity="0.14"/>`;
    return { svg: out, alt: "Dusk over a field of little hills of bills to the horizon, a tiny top hat on each, 2,800 in cream in the sky; a spotlight cone from above lights our Rich Human in his chair on the hill in front, his top hat glowing, waving the Reaper's pencil, a new I PREFER LIVING button on his lapel and the UNREALISTIC sticker still on his forehead." };
  },

  // ── 5 · plate the-internet, on "thing": four megaphones blast at the camera ──
  "step-2-loud-humans"(H, fid) {
    const { K, C } = H, T = tools(H), ink = C.line;
    let out = T.field(640);
    const KS = 2.0, FEET = 900;
    const LOUD = [
      { x: 330, o: K.castOpts("loudHuman", { kind: "barrel", tone: 2, color: 1, arms: [[-50, -110], [50, 110]] }) },
      { x: 750, o: K.castOpts("loudHuman", { kind: "twig", tone: 0, color: 3, build: { legs: 1.3, neck: 2.0, hs: 0.8 }, arms: [[-40, -100], [40, 100]] }) },
      { x: 1170, o: K.castOpts("loudHuman", { kind: "hourglass", tone: 3, color: 2, arms: [[-46, -112], [46, 112]] }) },
      { x: 1590, o: K.castOpts("loudHuman", { kind: "box", tone: 1, colorHex: C.peri, arms: [[-44, -104], [44, 104]] }) },
    ];
    // the speech bubbles, all the same now: one neat row, a pill bottle in each
    LOUD.forEach((m, i) => {
      const bx = m.x + (i - 1.5) * 12, by = 190;
      out += `<path d="M${f(bx - 40)},${f(by + 80)} L${f(m.x - 4)},${f(by + 250)} L${f(bx + 14)},${f(by + 88)} Z" fill="${C.cream}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
        `<ellipse cx="${f(bx)}" cy="${by}" rx="150" ry="104" fill="${C.cream}" stroke="${ink}" stroke-width="5"/>` + at(bx, by + 60, 1.05, K.props.pillBottle({}));
    });
    // the four Loud Humans beside their laptops, every megaphone swung round to the camera, mid-blast
    LOUD.forEach((m) => {
      const R = K.rig(m.o), oy = FEET - 100 * KS, hy = oy + (R.hy + 4) * KS;
      // the laptop on its little stand, at his side
      const lx = m.x - 118, ty = oy + 40 * KS;
      out += T.poly([[lx - 62, ty], [lx + 62, ty], [lx + 62, ty + 14], [lx - 62, ty + 14]], C.tan, 4) + `<path d="M${lx - 50},${ty + 14} V${FEET} M${lx + 50},${ty + 14} V${FEET}" stroke="${ink}" stroke-width="7"/>` +
        at(lx, ty, 1.6, K.props.laptop({ screen: "" }));
      // the body without its side-on megaphone (the bell below is the megaphone turned to the camera)
      const body = K.person(m.o).replace(/<path d="M-8,16 L-8,-4 L24,-22 L24,34 Z"[^>]*\/><path d="M24,-22 L30,6 L24,34 Z"[^>]*\/>/, "");
      out += at(m.x, oy, KS, body);
      // the bell, seen from the front, and the shock rings
      out += `<circle cx="${m.x}" cy="${f(hy)}" r="46" fill="${C.cream}" stroke="${ink}" stroke-width="6"/><circle cx="${m.x}" cy="${f(hy)}" r="32" fill="${C.slate}" stroke="${ink}" stroke-width="3.4"/><circle cx="${m.x}" cy="${f(hy)}" r="11" fill="#0B1220"/>`;
      out += [66, 86, 106].map((r, k) => `<path d="M${f(m.x - r * 0.7)},${f(hy - r * 0.7)} A${r},${r} 0 0,1 ${f(m.x + r * 0.7)},${f(hy - r * 0.7)} M${f(m.x + r * 0.7)},${f(hy + r * 0.7)} A${r},${r} 0 0,1 ${f(m.x - r * 0.7)},${f(hy + r * 0.7)}" fill="none" stroke="${ink}" stroke-width="${6 - k * 1.4}" stroke-linecap="round" opacity="${0.9 - k * 0.2}"/>`).join("");
    });
    // the shake
    out += `<path d="M30,120 h70 M20,170 h50 M1830,140 h70 M1850,190 h50 M24,760 h60 M1840,780 h60" stroke="${ink}" stroke-width="7" stroke-linecap="round"/>`;
    return { svg: out, alt: "Four Loud Humans with megaphones for heads (a barrel, a beanpole, an hourglass and a refrigerator box) behind chunky laptops on little stands, every megaphone swung round to the camera and blasting, shock rings round each bell; over them a neat row of four identical speech bubbles, a pill bottle in each." };
  },

  // ── 6 · plate the-laundry, on "legal.": the LEGAL stamp lifts off the Politician's forehead ──
  "step-3-lobbyist-funnels"(H, fid) {
    const { K, C } = H, T = tools(H), ink = C.line;
    let out = T.field(640);
    // the washing machine behind him, in its campaign bunting and boater, the conveyor running into it
    const WX = 1440, WB = 860, WK = 1.5;
    let wm = T.poly([[-100, 0], [-100, -230], [100, -230], [100, 0]], WHITE, 5) + T.poly([[-100, -230], [100, -230], [100, -270], [-100, -270]], C.slate, 5) +
      `<circle cx="-56" cy="-250" r="11" fill="${C.cream}" stroke="${ink}" stroke-width="3"/><circle cx="-24" cy="-250" r="11" fill="${C.cream}" stroke="${ink}" stroke-width="3"/><rect x="20" y="-258" width="58" height="16" fill="${C.orange}" stroke="${ink}" stroke-width="3"/>` +
      `<circle cx="0" cy="-100" r="64" fill="${C.slate}" stroke="${ink}" stroke-width="8"/><circle cx="0" cy="-100" r="51" fill="#7FB5B0" stroke="${ink}" stroke-width="3"/>` +
      `<path d="M-44,-94 Q-22,-120 0,-94 T44,-94" fill="none" stroke="${WHITE}" stroke-width="6"/>` + at(8, -80, 0.45, T.bill(), 28) +
      `<rect x="-92" y="-8" width="20" height="14" fill="${ink}"/><rect x="72" y="-8" width="20" height="14" fill="${ink}"/>`;
    // bunting: a swag of pennants across the top of the front, and a straw boater on top
    let bunt = `<path d="M-108,-226 Q0,-198 108,-226" fill="none" stroke="${ink}" stroke-width="3"/>`;
    for (let i = 0; i < 7; i++) {
      const u = (i + 0.5) / 7, x = -108 + 216 * u, y = -226 + 14 * 4 * u * (1 - u);
      bunt += T.poly([[x - 13, y], [x + 13, y], [x, y + 26]], [C.war, WHITE, C.navy][i % 3], 2.6);
    }
    const boater = T.poly([[-46, -270], [-40, -300], [40, -300], [46, -270]], "#E8C26A", 4) + T.poly([[-74, -270], [74, -270], [70, -262], [-70, -262]], "#E8C26A", 4) + `<path d="M-43,-282 H43" stroke="${C.navy}" stroke-width="8"/>`;
    out += at(WX, WB, WK, wm + bunt + boater);
    out += at(WX - 250, WB, 1.3, K.props.conveyor({ w: 260 }));
    // the Politician, close, grinning; the paper back in his breast pocket; LEGAL on his forehead, the stamp lifting off
    const pk = 4.2, px = 720, feet = 1250;
    const po = K.castOpts("politician", { mood: "grin", arms: [[-8, -3], [8, 3]] });
    const mark = at(1.5, -11, 0.19, K.props.stampMark({ text: "LEGAL", angle: -8 }));
    let pol = K.person(po).replace("<!--face-end-->", mark + "<!--face-end-->");
    pol += at(13, -8, 0.3, T.bill(), -72);
    out += at(px, feet - 100 * pk, pk, pol);
    const R = K.rig(po), headY = feet - 100 * pk + R.hy * pk;
    out += at(px + 40, headY - 150, 2.3, K.props.stamp({ text: "LEGAL" }), -8);
    out += T.lines(px + 40, headY - 120, 150, 190, -170, -10, 7, 6);
    return { svg: out, alt: "Close on the Politician, grinning his toothy grin, a red LEGAL stamp mark on his forehead and the rubber stamp lifting off above it, the paper sticking up out of his breast pocket; behind him a 1950s washing machine draped in campaign bunting with a straw boater on top, a conveyor running into it." };
  },

  // ── 7 · plate the-rally, on "else.": the glove pats the SUPER PAC patch back down over BRIBERY ──
  "step-4-super-pac"(H, fid) {
    const { K, C } = H, T = tools(H), ink = C.line;
    let out = T.field(620);
    // bunting strung across the top of the rally ground
    out += `<path d="M-20,70 Q480,170 960,80 T1940,90" fill="none" stroke="${ink}" stroke-width="4"/>`;
    for (let i = 0; i < 17; i++) { const x = 30 + i * 118, y = 70 + 70 * Math.sin((i / 16) * Math.PI * 2 + 0.3) * 0.6 + 40; out += T.poly([[x - 22, y], [x + 22, y], [x, y + 48]], [C.war, WHITE, C.navy][i % 3], 3); }
    // the river of plain papers pouring in from the left into the Super PAC's open top
    const rnd = K.rng(42);
    for (let i = 0; i < 22; i++) {
      const u = i / 21, x = -60 + u * 920, y = 420 - Math.sin(u * Math.PI * 0.9) * 170 + (rnd() - 0.5) * 50;
      out += at(x, y, 0.85 + rnd() * 0.25, T.bill(), (rnd() - 0.5) * 60);
    }
    // the burst little PAC, flat on the grass in front, papers spilled
    out += T.poly([[180, 880], [210, 830], [330, 812], [470, 836], [500, 880]], C.tan, 5) + T.poly([[290, 828], [372, 822], [376, 856], [292, 862]], C.cream, 3) +
      `<text x="333" y="852" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="28" fill="${ink}" transform="rotate(-3 333 852)">PAC</text>` +
      `<path d="M230,834 l12,10 l10,-12 l12,10 M420,826 l10,12 l12,-10 l10,12" fill="none" stroke="${ink}" stroke-width="3"/>` + at(560, 864, 0.7, T.bill(), 18) + at(140, 868, 0.7, T.bill(), -24);
    // the Super PAC in its hero pose, the patch peeled up off BRIBERY, the river pouring into its open top
    const BX = 1000, BB = 880;
    const pac = T.superPac("peeled") + at(-30, -508, 0.9, T.bill(), 12) + at(66, -514, 0.9, T.bill(), -18);
    out += at(BX, BB, 1, pac, -4);
    // the Lobbyist's gloved hand reaching in from the right edge, palm down, about to pat it back
    const GX = 1330, GY = 430;
    out += T.poly([[1940, GY + 40], [GX + 150, GY - 6], [GX + 160, GY + 70], [1940, GY + 140]], "#3A4766", 5) +
      T.poly([[GX + 150, GY - 10], [GX + 176, GY - 14], [GX + 184, GY + 74], [GX + 158, GY + 76]], "#2A3550", 4);
    const glove = T.poly([[GX + 150, GY], [GX + 60, GY - 8], [GX + 40, GY + 14], [GX + 46, GY + 52], [GX + 150, GY + 66]], "#24304D", 4.4) +
      [0, 1, 2, 3].map((i) => T.poly([[GX + 64, GY + 2 + i * 15], [GX - 10, GY + 4 + i * 16], [GX - 14, GY + 16 + i * 16], [GX + 60, GY + 16 + i * 15]], "#24304D", 3.6)).join("") +
      T.poly([[GX + 90, GY + 60], [GX + 50, GY + 98], [GX + 38, GY + 90], [GX + 70, GY + 52]], "#24304D", 3.6);
    out += glove + T.lines(GX - 30, GY + 40, 30, 60, 120, 220, 4, 5);
    return { svg: out, alt: "The rally ground under bunting: a river of plain bills pours from the left into the open top of the Super PAC, a rust canvas backpack with navy straps and a war-red cape; its cream SUPER PAC patch is lifted at the bottom, showing BRIBERY painted underneath, as the Lobbyist's navy glove reaches in from the right to pat it down; the burst little PAC lies flat on the grass in front." };
  },

  // ── 8 · host: the $650 million aside; the pallet has flattened the Lobbyist ──
  "lobbying-budget"(H, fid) {
    const { K, C } = H, T = tools(H), ink = C.line;
    const PX = 1430, PY = 1060, PW = 380;
    let front = "";
    // the flattened Lobbyist: a trench coat squashed flat under the pallet, his fedora and his masked eyes peeking out
    front += T.poly([[PX - PW / 2 - 110, PY], [PX - PW / 2 - 96, PY - 30], [PX + PW / 2 + 20, PY - 30], [PX + PW / 2 + 40, PY]], "#3A4766", 4);
    front += T.poly([[PX - PW / 2 - 250, PY], [PX - PW / 2 - 232, PY - 40], [PX - PW / 2 - 140, PY - 50], [PX - PW / 2 - 100, PY - 4]], "#4A3A2E", 4.4) + `<path d="M${PX - PW / 2 - 238},${PY - 14} L${PX - PW / 2 - 108},${PY - 18}" stroke="${C.rust}" stroke-width="8"/>`;
    front += T.poly([[PX - PW / 2 - 104, PY - 30], [PX - PW / 2 - 30, PY - 30], [PX - PW / 2 - 30, PY - 10], [PX - PW / 2 - 104, PY - 10]], "#0B1220", 3) +
      `<ellipse cx="${PX - PW / 2 - 84}" cy="${PY - 20}" rx="9" ry="5" fill="${WHITE}"/><ellipse cx="${PX - PW / 2 - 52}" cy="${PY - 20}" rx="9" ry="5" fill="${WHITE}"/><circle cx="${PX - PW / 2 - 82}" cy="${PY - 20}" r="2.6" fill="${ink}"/><circle cx="${PX - PW / 2 - 50}" cy="${PY - 20}" r="2.6" fill="${ink}"/>`;
    // the pallet: slats, then bundles of plain bills in bands, stacked high
    front += T.poly([[PX - PW / 2, PY - 26], [PX + PW / 2, PY - 26], [PX + PW / 2, PY - 60], [PX - PW / 2, PY - 60]], C.tan, 4) + `<path d="M${PX - 120},${PY - 26} V${PY - 60} M${PX + 120},${PY - 26} V${PY - 60}" stroke="${ink}" stroke-width="4"/>`;
    for (let r = 0; r < 5; r++) for (let c = 0; c < 3; c++) {
      const x = PX - PW / 2 + 10 + c * ((PW - 20) / 3), y = PY - 60 - (r + 1) * 88, w = (PW - 20) / 3 - 8;
      front += T.poly([[x, y], [x + w, y], [x + w, y + 84], [x, y + 84]], C.money, 4);
      for (let k = 1; k < 6; k++) front += `<path d="M${f(x + 4)},${f(y + k * 14)} H${f(x + w - 4)}" stroke="${C.moneyDark}" stroke-width="2"/>`;
      front += `<rect x="${f(x + w / 2 - 12)}" y="${f(y - 1)}" width="24" height="86" fill="${C.cream}" stroke="${ink}" stroke-width="2.4"/>`;
    }
    // his arm out from under the right side, bent up, the glove giving a thumbs-up
    const AX = PX + PW / 2 + 30, AY = PY - 30;
    front += T.poly([[AX, AY], [AX + 120, AY - 6], [AX + 130, AY + 24], [AX, AY + 28]], "#3A4766", 4) +
      T.poly([[AX + 96, AY + 10], [AX + 132, AY - 2], [AX + 150, AY - 250], [AX + 116, AY - 250]], "#3A4766", 4);
    const fx = AX + 90, fy = AY - 340;
    front += T.poly([[fx, fy], [fx + 86, fy - 4], [fx + 92, fy + 86], [fx + 4, fy + 92]], "#24304D", 4.4) +
      [0, 1, 2].map((i) => `<path d="M${fx + 8},${fy + 24 + i * 22} H${fx + 70}" stroke="#5C6F8E" stroke-width="3.4"/>`).join("") +
      T.poly([[fx + 50, fy + 2], [fx + 84, fy - 2], [fx + 90, fy - 84], [fx + 62, fy - 90]], "#24304D", 4.4) +
      `<path d="M${fx + 66},${fy - 80} L${fx + 84},${fy - 78}" stroke="#5C6F8E" stroke-width="3"/>` + T.lines(fx + 72, fy - 60, 50, 80, -150, -30, 4, 5);
    // the shipping tag on its string from the top corner
    front += at(PX - PW / 2 + 30, PY - 60 - 5 * 88 + 6, 2.1, K.props.priceTag({ text: "$650,000,000", angle: 16 }));
    front += T.lines(PX, PY - 520, 30, 80, -150, -30, 5, 5);
    return { svg: H.host("smirk-smile", "hand-chest", front), alt: "Wishonia at her lectern, hand on her chest, tells the camera the aside; beside her a pallet stacked with bundles of plain bills has flattened the Lobbyist: his squashed fedora pokes out at one side, his navy glove gives a thumbs-up at the other, and a shipping tag on the pallet reads $650,000,000." };
  },

  // ── 9 · plate the-payout, on "diseases.": the skeleton on his hill, the Reaper scribbling, the scientist charging ──
  "step-5-treaty-split"(H, fid) {
    const { K, C } = H, T = tools(H), ink = C.line;
    let out = T.field(560);
    // the bank's corner at the left edge, where the stream came from
    out += at(-20, 640, 1.2, K.props.bank({ label: "" }));
    const HX = 1130, HB = 930, HH = 350, K9 = 1.9;
    // the Reaper behind the hill, scribbling his tallies as fast as he can
    const RX = 1560, RY = 640;
    out += at(RX, RY, 2.3, T.reaper()) + at(RX - 100, RY - 300, 1.6, T.tally(60)) + at(RX - 40, RY - 236, 0.3, K.pencil(), -130);
    out += `<path d="M${RX - 176},${RY - 340} l-24,-16 M${RX - 182},${RY - 300} l-30,-4 M${RX - 174},${RY - 260} l-26,10" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`;
    out += T.hill(HX, HB, 560, HH, 909, 0.55);
    // the papers climbing the hill on their stick legs into his arms: medicine papers, cross seals
    [[650, 900], [742, 846], [834, 790], [920, 736], [1000, 690]].forEach(([x, y], i) => { out += at(x, y - 40, 0.9, K.money("med", i % 2), -24); });
    // the skeleton in his chair, top hat, monocle and a long white beard, still hugging his returns
    const chairY = HB - HH + 6 - 150 * K9;
    const so = K.castOpts("richHuman", { skeleton: true, arms: [[-30, -80], [30, 80]] });
    const sR = K.rig(so), cx0 = sR.mouth[0] - 2, cy0 = sR.mouth[1] + 4;
    // the beard: a wavy white mane along a centerline from his jaw down over the seat and the slope
    const spine = (u) => [cx0 + 4 * Math.sin(u * 3) - 150 * u * u, cy0 + 236 * u];
    const left = [], right = [];
    for (let i = 0; i <= 36; i++) {
      const u = i / 36, p = spine(u), q = spine(Math.min(1, u + 0.01)), dx = q[0] - p[0], dy = q[1] - p[1], L = Math.hypot(dx, dy) || 1;
      const w = (18 - 8 * u) * (1 + 0.28 * Math.sin(i * 1.9)), nx = -dy / L, ny = dx / L;
      left.push([p[0] + nx * w, p[1] + ny * w]); right.push([p[0] - nx * w, p[1] - ny * w]);
    }
    let beard = T.poly(left.concat(right.reverse()), WHITE, 2.6);
    beard += `<path d="M${f(cx0 - 2)},${cy0 + 24} q-6,24 0,44 M${f(cx0 - 4)},${cy0 + 90} q-8,26 -24,44 M${f(cx0 - 50)},${cy0 + 170} q-26,20 -56,30" fill="none" stroke="#C9C1AE" stroke-width="2.2"/>`;
    const held = at(0, 26, 0.5, K.money("med", 0), -8);
    out += at(HX, chairY, K9, T.chairBack()) + at(HX, chairY, K9, K.person(so) + held) + at(HX, chairY, K9, T.chairFront() + beard);
    // the neon infinity sign over the hill
    out += T.neon(HX - 330, 150, 300);
    // the calendar on its stump, shedding its pages
    out += T.poly([[300, 900], [300, 830], [380, 830], [380, 900]], "#7A5634", 4) + at(340, 830, 1.1, K.props.calendar({ month: "JAN", day: 1 }));
    [[260, 690, -30], [420, 640, 20], [330, 580, -10], [480, 720, 34]].forEach(([x, y, r]) => { out += T.poly([[x - 26, y - 22], [x + 26, y - 22], [x + 26, y + 22], [x - 26, y + 22]], WHITE, 3, `transform="rotate(${r} ${x} ${y})"`); });
    // the scientist charging up the hill with her bubbling flask, a streak of dust behind her
    const sc = K.castOpts("scientist", { mood: "eager", arms: [[-60, -100], [150, 170]], holdR: "flask", holdL: null });
    out += T.puff(300, 790, 36, 0.75) + T.puff(410, 770, 30, 0.8) + `<path d="M180,760 H470 M220,800 H490 M200,720 H440" stroke="${ink}" stroke-width="6" stroke-linecap="round" opacity="0.6"/>`;
    out += at(640, 780 - 100 * 1.75, 1.75, K.person(sc), 14);
    return { svg: out, alt: "The Rich Human is a grinning skeleton in his chair on top of the hill of bills, top hat and monocle on and a long white beard pouring down the slope, still hugging his returns as medicine papers climb the hill into his arms; a neon infinity sign glows above; the Grim Reaper behind the hill scribbles tally marks on his clipboard; the scientist charges up the slope with her bubbling flask in a streak of dust; the calendar on a stump sheds its pages." };
  },

  // ── 10 · host: the ending; the Reaper's pencil snaps ──
  "works-out"(H, fid) {
    const { K, C } = H, T = tools(H), ink = C.line;
    const RX = 1500, FEET = 1075, RK = 3.0;
    const oy = FEET - 100 * RK;
    let front = at(RX, oy, RK, T.reaper());
    // the clipboard held at his chest, and the pencil in two halves over it, splinters flying
    front += at(RX - 120, oy - 92 * RK, 2.5, T.tally(60));
    front += at(RX + 70, oy - 60 * RK, 1.25, `<path d="M0,0 l18,-10 l52,-30 l10,16 l-52,30 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/><path d="M0,0 l18,-10 l2,14 Z" fill="${ink}"/><path d="M70,-40 l4,-8 l6,6 l4,-6 l2,14" fill="none" stroke="${ink}" stroke-width="3"/>`, -6);
    front += at(RX + 210, oy - 112 * RK, 1.25, `<path d="M0,0 l-4,-6 l6,-4 l-2,-6 l52,-30 l12,20 l-52,30 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/><path d="M52,-30 l12,20 l14,-8 l-12,-20 Z" fill="${C.war}" stroke="${ink}" stroke-width="4"/>`, 50);
    front += T.lines(RX + 190, oy - 90 * RK, 26, 70, -150, 20, 7, 6);
    // the bone hand on the clipboard
    front += `<circle cx="${RX + 46 * RK}" cy="${oy - 40 * RK}" r="${9 * RK}" fill="#F1EAD6" stroke="${ink}" stroke-width="7"/>`;
    return { svg: H.host("smirk-smile", "open-palms", front), alt: "Wishonia at her lectern smirks at the camera, palms open; at the right of the studio the Grim Reaper holds up his tally clipboard, and his pencil has just snapped in two, the halves and splinters flying." };
  },
};
