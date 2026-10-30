// Sketches for storyboards/part-11-civilization-countdown.md (v3, the atomic-age film look): each scene's key
// moment on a 1920 x 1080 frame, drawn with the production art. Host shots are H.host (KIT.studio's set, the
// real Wishonia sprites, the lectern); a plate frame is one framing of its plate as the camera sees it, on a
// plain field with its ground line at y 880 (16:9 keeps everything important above y 900).

const GROUND = "#C8B07B", SKY = "#E3D3A5", EDGE = "#B09363", ROAD = "#EEE3C4", DASH = "#C7AB78";
const G = 880;
const f1 = (n) => Math.round(n * 10) / 10;

// ── Drawing helpers ──────────────────────────────────────────────────────
// A plain field: a pale sky band over the ground, the horizon at hz.
function field(hz = 470) {
  return `<rect width="1920" height="1080" fill="${GROUND}"/><rect width="1920" height="${hz}" fill="${SKY}"/><rect y="${hz - 3}" width="1920" height="6" fill="${EDGE}"/>`;
}
// A person standing on ground line g at scale k (KIT.person units: feet at y 100).
function man(H, o, x, g, k, extra = "", rot = 0) {
  return H.at(x, g - 100 * k, k, H.K.person(o) + extra, rot);
}
// A paper bill (KIT.money), centered on (x, y).
function bill(H, kind, x, y, s = 1, rot = 0, legs = true, step = 0) {
  let m = H.K.money(kind, step);
  if (!legs) m = m.replace('class="legs"', 'class="legs" opacity="0"');
  return `<g transform="translate(${f1(x)},${f1(y)}) rotate(${rot}) scale(${s})">${m}</g>`;
}
// A stack of bills seen side on: n slabs of height dy, w wide, standing on `base`.
function slabs(H, x, base, w, n, dy = 16) {
  const { C } = H;
  let out = "";
  for (let i = 0; i < n; i++) {
    const y = base - (i + 1) * dy, ox = ((i * 37) % 11) - 5;
    out += `<rect x="${f1(x - w / 2 + ox)}" y="${f1(y)}" width="${w}" height="${dy}" fill="${C.money}" stroke="${C.line}" stroke-width="2.6"/>` +
      `<path d="M${f1(x - w / 2 + ox + 10)},${f1(y + dy / 2)} H${f1(x + w / 2 + ox - 30)}" stroke="${C.moneyDark}" stroke-width="2"/>` +
      `<circle cx="${f1(x + w / 2 + ox - 16)}" cy="${f1(y + dy / 2)}" r="${f1(dy * 0.3)}" fill="${C.moneyDark}"/>`;
  }
  return out;
}
// A Catmull-Rom curve through pts, sampled; returns { pts, len } with cumulative lengths.
function spline(pts, n = 14) {
  const out = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    for (let k = 0; k < n; k++) {
      const t = k / n, t2 = t * t, t3 = t2 * t;
      out.push([0, 1].map((d) => 0.5 * (2 * p1[d] + (-p0[d] + p2[d]) * t + (2 * p0[d] - 5 * p1[d] + 4 * p2[d] - p3[d]) * t2 + (-p0[d] + 3 * p1[d] - 3 * p2[d] + p3[d]) * t3)));
    }
  }
  out.push(pts[pts.length - 1]);
  const len = [0];
  for (let i = 1; i < out.length; i++) len.push(len[i - 1] + Math.hypot(out[i][0] - out[i - 1][0], out[i][1] - out[i - 1][1]));
  return { pts: out, len };
}
// The part of a sampled curve from its start to length L, as a path, and the point at L.
function upTo(s, L) {
  const total = s.len[s.len.length - 1];
  L = Math.max(0, Math.min(total, L));
  let d = `M${f1(s.pts[0][0])},${f1(s.pts[0][1])}`, end = s.pts[0];
  for (let i = 1; i < s.pts.length; i++) {
    if (s.len[i] >= L) {
      const u = (L - s.len[i - 1]) / (s.len[i] - s.len[i - 1] || 1);
      end = [s.pts[i - 1][0] + (s.pts[i][0] - s.pts[i - 1][0]) * u, s.pts[i - 1][1] + (s.pts[i][1] - s.pts[i - 1][1]) * u];
      d += ` L${f1(end[0])},${f1(end[1])}`;
      break;
    }
    d += ` L${f1(s.pts[i][0])},${f1(s.pts[i][1])}`;
    end = s.pts[i];
  }
  return { d, end, total };
}
// A fuse cord along d (a navy line under a tan one, as KIT.props.bomb draws it).
function cord(H, d, w = 1) {
  const { C } = H;
  return `<path d="${d}" fill="none" stroke="${C.ink}" stroke-width="${9 * w}" stroke-linecap="round" stroke-linejoin="round"/>` +
    `<path d="${d}" fill="none" stroke="${C.tan}" stroke-width="${4.6 * w}" stroke-linecap="round" stroke-linejoin="round"/>`;
}
function spark(H, x, y, s = 1) {
  const { K, C } = H;
  return H.at(x, y, s, K.star(0, 0, 20, C.orange, 6) + K.star(0, 0, 11, C.yellow, 6) + '<circle r="3.4" fill="#FFFFFF"/>');
}
// Your civilization as a cartoon bomb: a small Earth with a navy screw collar, standing on (x, y), radius r.
function earthBall(H, x, y, r) {
  const { K, C } = H;
  const top = y - 2 * r;
  return H.at(x, y, 1, K.props.earthGlobe({ r })) +
    `<path d="M${f1(x - r * 0.3)},${f1(top + r * 0.06)} L${f1(x - r * 0.26)},${f1(top - r * 0.28)} H${f1(x + r * 0.26)} L${f1(x + r * 0.3)},${f1(top + r * 0.06)} Z" fill="${C.navy}" stroke="${C.ink}" stroke-width="4" stroke-linejoin="miter"/>` +
    `<path d="M${f1(x - r * 0.26)},${f1(top - r * 0.12)} H${f1(x + r * 0.26)}" stroke="${C.orange}" stroke-width="3"/>`;
}
// The Earth-bomb on the lectern (16:9 host shots): the Earth on the lectern's right end, the fuse rising off the
// collar, making one small curl and running off up the wall to the right; frac of the fuse is left (the curl is
// between about 0.1 and 0.36 of it, counted from the collar); lit: the spark on its end; ring: a smoke ring instead.
// The host shots burn it down: official-murder-budget 0.9, considered-tuesday 0.62, once-it-starts 0.4 (just short
// of the curl), this-is-a-loop 0.09 (just out of it), you-defund-it 0.04 (out).
function lecternBomb(H, frac, lit = true, ring = false) {
  const x = 925, y = 790, r = 44;
  const s = spline([[x, y - 2 * r - r * 0.28], [x - 2, y - 134], [x + 14, y - 168], [x + 50, y - 176], [x + 70, y - 146], [x + 54, y - 116], [x + 22, y - 124], [x + 24, y - 162], [x + 62, y - 206], [x + 116, y - 222], [x + 170, y - 206], [x + 226, y - 226], [x + 280, y - 264], [x + 340, y - 268], [x + 392, y - 244], [x + 440, y - 262]]);
  const u = upTo(s, frac * s.len[s.len.length - 1]);
  let out = earthBall(H, x, y, r) + cord(H, u.d);
  if (lit) out += spark(H, u.end[0], u.end[1], 1.15);
  if (ring) {
    out += `<path d="M${f1(u.end[0])},${f1(u.end[1] - 4)} q-8,-14 4,-26 q12,-12 2,-26" fill="none" stroke="#9C9486" stroke-width="5" stroke-linecap="round"/>` +
      `<ellipse cx="${f1(u.end[0] + 6)}" cy="${f1(u.end[1] - 92)}" rx="30" ry="13" fill="none" stroke="#A9A193" stroke-width="7"/>`;
  }
  return out;
}
// Wishonia's mug, standing on (x, y).
function mug(H, x, y, k = 1, rot = 0) {
  const { C } = H;
  return H.at(x, y, k, `<path d="M-22,0 L-25,-52 H25 L22,0 Z" fill="${C.cream}" stroke="${C.ink}" stroke-width="4.5" stroke-linejoin="miter"/>` +
    `<path d="M24,-42 C46,-42 46,-12 22,-13" fill="none" stroke="${C.ink}" stroke-width="5"/><path d="M-24,-38 H24" stroke="${C.orange}" stroke-width="6"/>`, rot);
}
// A plain wooden table or desk, its top at height h above ground g, w wide, centered on x.
function desk(H, x, g, w, h, front = true) {
  const { C } = H;
  const top = g - h;
  return `<rect x="${x - w / 2}" y="${top}" width="${w}" height="14" fill="#9C6B3F" stroke="${C.ink}" stroke-width="4"/>` +
    (front ? `<rect x="${x - w / 2 + 10}" y="${top + 14}" width="${w - 20}" height="${h - 14}" fill="#7A5634" stroke="${C.ink}" stroke-width="4"/><path d="M${x - w / 2 + 10},${top + 40} H${x + w / 2 - 10}" stroke="${C.ink}" stroke-width="2.4" opacity="0.6"/>`
      : `<path d="M${x - w / 2 + 14},${top + 14} V${g} M${x + w / 2 - 14},${top + 14} V${g}" stroke="${C.ink}" stroke-width="10"/>`);
}
// A shopping cart (KIT.props.shoppingCart) standing on g at scale k, facing right, with optional load markup
// (in the cart's own units, inside the basket x -40..54, y -74..-38) drawn behind the wires.
function cart(H, x, g, k, load = "", flip = false) {
  return H.at(x, g, k, `<g transform="scale(${flip ? -1 : 1},1)">${load}${H.K.props.shoppingCart({})}</g>`);
}
// Smoke wisps rising from (x, y).
function wisps(x, y, s = 1) {
  return `<g transform="translate(${x},${y}) scale(${s})" fill="none" stroke="#8E877B" stroke-width="4" stroke-linecap="round">` +
    `<path d="M-14,0 q-8,-12 0,-24 q8,-12 0,-24"/><path d="M6,-6 q-8,-12 0,-24 q8,-12 0,-24"/><path d="M24,0 q-8,-12 0,-24 q8,-12 0,-24"/></g>`;
}
// A hammer held at (x, y), rotated rot, in px.
function hammer(H, x, y, s = 1, rot = 0) {
  const { C } = H;
  return H.at(x, y, s, `<rect x="-3" y="-34" width="6" height="40" fill="#9C6B3F" stroke="${C.ink}" stroke-width="2.2"/><rect x="-14" y="-44" width="28" height="12" fill="${C.peri}" stroke="${C.ink}" stroke-width="2.4"/>`, rot);
}
// Part 4's 1ST rosette (war-supply-chain, the hub of the war wheel), centered on (x, y), at half its Part 4 size.
function rosette(H, x, y, s = 1) {
  const { C } = H;
  const petals = Array.from({ length: 16 }, (_, i) => { const a = (i / 16) * Math.PI * 2; return `<circle cx="${f1(Math.cos(a) * 58)}" cy="${f1(Math.sin(a) * 58)}" r="18" fill="${C.med}" stroke="${C.ink}" stroke-width="3.4"/>`; }).join("");
  return H.at(x, y, s * 0.5, `<path d="M-22,20 L-40,110 L-14,94 L0,120 L4,30 Z M22,20 L40,110 L14,94 L0,120 L-4,30 Z" fill="${C.med}" stroke="${C.ink}" stroke-width="4" stroke-linejoin="miter"/>` +
    petals + `<circle r="56" fill="${C.cream}" stroke="${C.ink}" stroke-width="5"/><text y="18" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="50" fill="${C.navy}">1ST</text>`);
}
// A cartoon tank in px, its treads on g, facing right; flat: squashed like a pancake.
function tank(H, x, g, k = 1, flat = false) {
  const { C } = H;
  const body = `<path d="M-120,-20 L-104,-46 H104 L120,-20 L104,0 H-104 Z" fill="${C.slate}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    [-80, -40, 0, 40, 80].map((cx) => `<circle cx="${cx}" cy="-20" r="13" fill="${C.peri}" stroke="${C.ink}" stroke-width="4"/>`).join("") +
    `<path d="M-90,-46 L-84,-78 H60 L78,-46 Z" fill="#6E7A55" stroke="${C.ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    `<path d="M-40,-78 L-30,-112 H30 L40,-78 Z" fill="#6E7A55" stroke="${C.ink}" stroke-width="5" stroke-linejoin="miter"/>` +
    (flat ? `<path d="M30,-96 L150,-90 L230,-20 L224,-12 L144,-80 L30,-86 Z" fill="#6E7A55" stroke="${C.ink}" stroke-width="5" stroke-linejoin="miter"/>`
      : `<rect x="30" y="-101" width="140" height="13" fill="#6E7A55" stroke="${C.ink}" stroke-width="5"/>`) +
    `<path d="M-84,-74 H56" stroke="${C.orange}" stroke-width="3"/>`;
  return H.at(x, g, k, flat ? `<g transform="scale(1.45,0.26)">${body}</g>` : body);
}
// Price tag (KIT.props.priceTag) hanging from its knot at (x, y), at size s.
function tag(H, x, y, s, text, angle = 22) {
  return H.at(x, y, s, H.K.props.priceTag({ text, angle }));
}
// A stamped word (KIT.props.stampMark), its lowest corner on (x, y).
function mark(H, x, y, s, text, angle = -8, color) {
  return H.at(x, y, s, H.K.props.stampMark({ text, angle, color: color || H.C.war }));
}
// A gurney: a mattress on a steel frame with wheels, its top at y, from x0 to x1, on ground g.
function gurney(H, x0, x1, y, g) {
  const { C } = H;
  return `<path d="M${x0 + 30},${y + 20} V${g - 22} M${x1 - 30},${y + 20} V${g - 22} M${x0 + 30},${g - 60} H${x1 - 30}" stroke="${C.peri}" stroke-width="9"/>` +
    `<rect x="${x0}" y="${y + 6}" width="${x1 - x0}" height="16" fill="${C.peri}" stroke="${C.ink}" stroke-width="4"/>` +
    `<rect x="${x0 + 6}" y="${y - 14}" width="${x1 - x0 - 12}" height="22" fill="${C.cream}" stroke="${C.ink}" stroke-width="4"/>` +
    [x0 + 30, x1 - 30].map((cx) => `<circle cx="${cx}" cy="${g - 12}" r="12" fill="${C.slate}" stroke="${C.ink}" stroke-width="4"/>`).join("");
}
// A little plank hut, standing on (0, 0), about 120 wide, in its own units.
function hut(C) {
  let planks = "";
  for (let x = -54; x < 54; x += 18) planks += `<path d="M${x},-4 V-74" stroke="${C.ink}" stroke-width="2" opacity="0.5"/>`;
  return `<rect x="-60" y="-80" width="120" height="80" fill="#B98A55" stroke="${C.ink}" stroke-width="4"/>${planks}` +
    `<path d="M-72,-76 L0,-128 L72,-76 Z" fill="${C.rust}" stroke="${C.ink}" stroke-width="4" stroke-linejoin="miter"/>` +
    `<rect x="-16" y="-50" width="32" height="50" fill="${C.ink}"/>`;
}
// A mailbox on a post, its name plate under the box, standing on g.
function mailbox(H, x, g, text) {
  const { C } = H;
  const w = Math.max(120, text.length * 19 + 30);
  return `<rect x="${x - 6}" y="${g - 150}" width="12" height="150" fill="#7A5634" stroke="${C.ink}" stroke-width="3"/>` +
    `<path d="M${x - 46},${g - 150} V${g - 196} Q${x - 46},${g - 222} ${x - 20},${g - 222} H${x + 20} Q${x + 46},${g - 222} ${x + 46},${g - 196} V${g - 150} Z" fill="${C.peri}" stroke="${C.ink}" stroke-width="4"/>` +
    `<path d="M${x + 46},${g - 200} h18 v-22 h-10" fill="none" stroke="${C.war}" stroke-width="6"/>` +
    `<rect x="${x - w / 2}" y="${g - 140}" width="${w}" height="40" fill="${C.cream}" stroke="${C.ink}" stroke-width="3"/>` +
    H.label(x, g - 110, 26, text, "middle", C.ink);
}
// A gas can with the missile seal, standing on (x, y), at size s.
function gasCan(H, x, y, s = 1) {
  const { K, C } = H;
  return H.at(x, y, s, `<path d="M-30,0 V-70 L-18,-82 H22 L30,-74 V0 Z" fill="${C.war}" stroke="${C.ink}" stroke-width="4" stroke-linejoin="miter"/>` +
    `<path d="M10,-82 L18,-100 L26,-98 L22,-80" fill="${C.war}" stroke="${C.ink}" stroke-width="3"/>` + K.moneySeal("war", 0, -38, 14));
}

// A neat round crater in the ground, centered on (x, y), rx by ry: a rim of churned earth round a dark bowl.
function crater(H, x, y, rx, ry) {
  const { C } = H;
  let rim = "";
  for (let i = 0; i < 14; i++) {
    const a = Math.PI + (i * Math.PI) / 13, px = x + Math.cos(a) * rx * 1.04, py = y + Math.sin(a) * ry * 1.1;
    rim += `<path d="M${f1(px - 34)},${f1(py + 10)} L${f1(px - 14)},${f1(py - 18 - (i % 3) * 6)} L${f1(px + 16)},${f1(py - 14 - (i % 2) * 8)} L${f1(px + 36)},${f1(py + 10)} Z" fill="${i % 2 ? "#A88F5C" : "#B79E6A"}" stroke="${C.ink}" stroke-width="3.4" stroke-linejoin="miter"/>`;
  }
  return `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="#6E5A3A" stroke="${C.ink}" stroke-width="5"/>` +
    `<ellipse cx="${x}" cy="${y + ry * 0.25}" rx="${rx * 0.72}" ry="${ry * 0.6}" fill="#4F4029"/>` + rim;
}
// A wooden crate, standing on (0, 0), about 90 wide, in its own units.
function crate(C) {
  return `<rect x="-45" y="-70" width="90" height="70" fill="#B98A55" stroke="${C.ink}" stroke-width="4"/>` +
    `<path d="M-45,-48 H45 M-45,-22 H45" stroke="${C.ink}" stroke-width="2.4" opacity="0.6"/><path d="M-41,-4 L41,-66 M-41,-66 L41,-4" stroke="#8E6438" stroke-width="7"/><rect x="-45" y="-70" width="90" height="70" fill="none" stroke="${C.ink}" stroke-width="4"/>`;
}

// ── The host shots: the set, Wishonia, the lectern, then the lectern props in front ──
function lecternProps(H, frac, lit = true, ring = false, mugAt = null) {
  const m = mugAt || [610, 790, 0];
  return mug(H, m[0], m[1], 1, m[2]) + lecternBomb(H, frac, lit, ring);
}

export default {
  "civilization-countdown-title"(H, id) {
    const { K, C } = H;
    const cx = 960, cy = 300, rx = 200, ry = 62;
    const orbits = [0, 60, -60].map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = [[0, 2.6], [60, 0.4], [-60, 4.4]].map(([a, th]) => {
      const ex = rx * Math.cos(th), ey = ry * Math.sin(th), r = (a * Math.PI) / 180;
      return bill(H, "war", cx + ex * Math.cos(r) - ey * Math.sin(r), cy + ex * Math.sin(r) + ey * Math.cos(r) - 6, 0.62, 0, true);
    }).join("");
    // the fuse: out of the collar, between the orbits, and down the left side of the card to the bottom edge
    const s = spline([[cx, cy - 46], [cx - 30, cy - 150], [cx - 260, cy - 210], [cx - 560, cy - 150], [cx - 760, cy + 40], [cx - 800, cy + 360], [cx - 790, cy + 620], [cx - 770, cy + 700]]);
    const u = upTo(s, s.len[s.len.length - 1]);
    const heading = (y, size, text) => `<text x="${cx + size * 0.04}" y="${y + size * 0.05}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${size}" fill="${C.ink}" opacity="0.55">${text}</text>` +
      `<text x="${cx}" y="${y}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${size}" fill="${C.cream}">${text}</text>`;
    const wm = K.castOpts("weaponsMaker", { mood: "grin", arms: [[20, 10], [-20, -10]], hold: null });
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + cord(H, u.d) +
      earthBall(H, cx, cy + 34, 34) + spark(H, u.end[0], u.end[1], 1.3) +
      man(H, wm, 300, 1080 + 255, 2.6) + wisps(330, 900, 0.9) +
      heading(610, 84, "YOUR CIVILIZATION HAS A") + heading(810, 210, "COUNTDOWN");
    return { svg, alt: "The navy title card: YOUR CIVILIZATION HAS A COUNTDOWN under the film's atom, whose nucleus is a little Earth with a bomb's collar; its fuse runs down the left side of the card, lit, and the Weapons Maker's hard hat ducks below the bottom edge." };
  },

  "official-murder-budget"(H, id) {
    const { K, C } = H;
    const g = 1150, k = 3.2;
    const warheads = [[-26, -70, -14], [4, -80, 6], [30, -68, 18]].map(([x, y, r]) => H.at(x, y, 0.3, K.props.missile({ mood: "smug", arms: "none" }), r)).join("");
    const wm = K.castOpts("weaponsMaker", { look: "right", mood: "worried" });
    const W0 = [2090, 860, 360];
    const shadow = `<path d="M1150,640 L1920,500 V1080 H1080 Z" fill="${C.ink}" opacity="0.22"/>`;
    const wheel = `<circle cx="${W0[0]}" cy="${W0[1]}" r="${W0[2]}" fill="${C.slate}" stroke="${C.ink}" stroke-width="10"/><circle cx="${W0[0]}" cy="${W0[1]}" r="${W0[2] - 80}" fill="none" stroke="${C.peri}" stroke-width="8"/><circle cx="${W0[0]}" cy="${W0[1]}" r="90" fill="${C.peri}" stroke="${C.ink}" stroke-width="8"/>` +
      [160, 200, 240].map((a) => `<path d="M${W0[0]},${W0[1]} L${f1(W0[0] + (W0[2] - 80) * Math.cos((a * Math.PI) / 180))},${f1(W0[1] + (W0[2] - 80) * Math.sin((a * Math.PI) / 180))}" stroke="${C.peri}" stroke-width="10"/>`).join("") +
      `<path d="M1780,430 L1920,404" stroke="${C.ink}" stroke-width="18"/>`;
    const front = lecternProps(H, 0.9) +
      cart(H, 1420, g, k, warheads) + man(H, wm, 1150, g, k) +
      tag(H, 1420 + 4 * k, g - 128 * k, 1.75, "$2.72 TRILLION", 8) + mark(H, 1450, g - 128 * k + 104, 1.5, "OFFICIAL", -10) +
      shadow + wheel;
    const svg = H.host("sideeye-closed", "idle", front);
    return { svg, alt: "Wishonia at her lectern side-eyes the camera; beside her, Part 10's cart of grinning warheads with OFFICIAL stamped across its $2.72 TRILLION tag, the Weapons Maker leaning on it and looking up at a giant cart wheel that fills the right edge and throws its shadow over him. On the lectern, the Earth-bomb's long fuse burns." };
  },

  "cybercrime-10-trillion"(H, id) {
    const { K, C } = H;
    const ks = 2.0, kb = 4.0;
    const heap = slabs(H, 6, -38, 92, 3, 12);
    const small = cart(H, 330, G, ks, [[-26, -70, -14], [4, -80, 6], [30, -68, 18]].map(([x, y, r]) => H.at(x, y, 0.3, K.props.missile({ mood: "smug", arms: "none" }), r)).join(""));
    const crook = K.castOpts("lobbyist", { look: "left", mood: "grin", arms: [[-40, -55], [30, 60]], holdR: null, holdL: null });
    const wm = K.castOpts("weaponsMaker", { arms: [[-20, -10], [135, 125]], hold: null, mood: "grin" });
    const wx = 776, cxk = wx + 304;
    const chain = Array.from({ length: 18 }, (_, i) => `<ellipse cx="${450 + i * 29}" cy="${G - 40}" rx="17" ry="9" fill="none" stroke="${C.peri}" stroke-width="7"/>`).join("");
    const arcs = [[1270, 470, -20], [1350, 420, 10], [1420, 470, 30]].map(([x, y, r]) => bill(H, "war", x, y, 0.95, r, false)).join("");
    const svg = field(460) +
      small + chain + man(H, wm, wx, G, 2.2) +
      man(H, crook, cxk, 732, 2.4) +
      cart(H, 1190, G, kb, heap) +
      H.at(1300, G - 74 * kb + 2, 2.2, K.props.laptop({})) + arcs +
      tag(H, 1395, G - 74 * kb + 10, 1.6, "$10.5 TRILLION", 16) + tag(H, 1330, G - 52 * kb + 26, 1.4, "+15% A YEAR", 8);
    return { svg, alt: "On the field, Part 10's small cart and a cart twice its size chained together; the Weapons Maker reaches up to shake the Masked Crook's hand as the Crook leans out of the big cart's basket, both grinning at us; war papers arc out of the laptop on the big cart's rim, which wears the tags $10.5 TRILLION and +15% A YEAR." };
  },

  "crypto-afternoon"(H, id) {
    const { K, C } = H;
    const hx = 760, hk = 1.55;
    const note = H.at(hx + 64, G - 110, 1, `<rect x="-46" y="-30" width="92" height="56" fill="${C.cream}" stroke="${C.ink}" stroke-width="3"/>` + H.label(0, 8, 24, "RANSOM", "middle", C.war), 6);
    const marchers = [0, 1, 2, 3, 4].map((i) => bill(H, "war", 980 + i * 92, G - 42, 0.9, 0, true, i % 2)).join("");
    const patient = { tone: 1, outfit: "shirt", color: 2, seed: 9, skeleton: true, mood: "grin", arms: [[10, 4], [-10, -4]] };
    const svg = field(430) +
      H.at(1560, G, 1.25, K.props.factory({ label: "" })) +
      H.at(hx, G, hk, K.props.hospital({ sign: "closed" })) +
      H.at(hx, G - 22 * hk, 2.2, K.props.padlock({})) + note + marchers +
      gurney(H, 90, 470, G - 190, G) + man(H, patient, 270, G - 72, 1.55, "", -90);
    return { svg, alt: "The hospital with its CLOSED sign, a padlock on its doors and a RANSOM note; war papers march out from under the doors into the small missile factory next door; on a gurney outside, the patient is a grinning skeleton, still waiting." };
  },

  "war-through-wifi"(H, id) {
    const { K, C } = H;
    const crook = K.castOpts("lobbyist", { look: "right", arms: [[40, 80], [40, 80]], holdR: null, holdL: null });
    const tower = slabs(H, 1260, G - 34, 240, 38, 18);
    const eyes = `<rect x="960" y="${G - 52}" width="110" height="28" fill="${C.ink}" stroke="${C.ink}" stroke-width="3"/><circle cx="992" cy="${G - 38}" r="9" fill="#FFFFFF"/><circle cx="1036" cy="${G - 38}" r="9" fill="#FFFFFF"/><circle cx="995" cy="${G - 37}" r="3.8" fill="${C.ink}"/><circle cx="1039" cy="${G - 37}" r="3.8" fill="${C.ink}"/>` +
      `<path d="M930,${G - 54} q-20,-30 6,-50 q-26,-12 -10,-40" fill="none" stroke="${C.peri}" stroke-width="5"/><rect x="900" y="${G - 170}" width="70" height="18" fill="#6E7A55" stroke="${C.ink}" stroke-width="4" transform="rotate(-24 935 ${G - 160})"/>`;
    const pile = slabs(H, 1640, G, 110, 3, 14) + bill(H, "war", 1650, G - 52, 0.8, -8, false);
    const svg = field(430) +
      man(H, crook, 380, G, 2.3) + desk(H, 470, G, 340, 140) + H.at(560, G - 140, 2.0, K.props.laptop({})) +
      `<g fill="none" stroke="${C.cream}" stroke-width="7" stroke-linecap="round">${[50, 90, 130].map((r) => `<path d="M${f1(560 - r * 0.7)},${f1(G - 250 - r * 0.25)} Q560,${f1(G - 250 - r * 0.9)} ${f1(560 + r * 0.7)},${f1(G - 250 - r * 0.25)}"/>`).join("")}</g>` +
      tank(H, 1180, G, 2.0, true) + tower + eyes + pile;
    return { svg, alt: "The Masked Crook types at his desk; beside him the tank lies flattened like a pancake under a tower of war papers, its barrel bent to the ground, the Weapons Maker's two eyes blinking out of the flat hatch; the small pile of pay sits beside it." };
  },

  "destroy-beats-make"(H, id) {
    const { K, C } = H;
    // the fallen stack: slabs lying on their side across the field, the Builder flattened under its end
    let stack = "";
    for (let i = 0; i < 34; i++) {
      const x = 200 + i * 34, ox = ((i * 29) % 9) - 4;
      stack += `<rect x="${x}" y="${G - 170 + ox}" width="34" height="${170 - ox}" fill="${C.money}" stroke="${C.line}" stroke-width="2.6"/><path d="M${x + 17},${G - 150 + ox} V${G - 40}" stroke="${C.moneyDark}" stroke-width="2"/><circle cx="${x + 17}" cy="${G - 22}" r="6" fill="${C.moneyDark}"/>`;
      // a paper band round every bundle of six
      if (i % 6 === 3) stack += `<rect x="${x - 2}" y="${G - 112}" width="38" height="30" fill="${C.cream}" stroke="${C.line}" stroke-width="2.6"/>`;
    }
    const splinters = [[1360, G - 10, 20], [1400, G - 6, -14], [1330, G - 4, 60]].map(([x, y, r]) => `<rect x="${x - 30}" y="${y - 6}" width="60" height="12" fill="#B98A55" stroke="${C.ink}" stroke-width="3" transform="rotate(${r} ${x} ${y})"/>`).join("");
    const builderEyes = `<rect x="1366" y="${G - 52}" width="86" height="24" fill="${C.navy}"/><circle cx="1392" cy="${G - 40}" r="9" fill="#FFFFFF"/><circle cx="1424" cy="${G - 40}" r="9" fill="#FFFFFF"/><circle cx="1395" cy="${G - 38}" r="3.6" fill="${C.ink}"/><circle cx="1427" cy="${G - 38}" r="3.6" fill="${C.ink}"/>`;
    const arm = `<path d="M1440,${G - 70} L1488,${G - 180} L1500,${G - 290}" fill="none" stroke="${C.ink}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/><path d="M1440,${G - 70} L1488,${G - 180} L1500,${G - 290}" fill="none" stroke="#C99A6B" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>`;
    const post = `<rect x="1560" y="${G - 420}" width="34" height="420" fill="${C.war}" stroke="${C.ink}" stroke-width="5"/>` +
      `<rect x="1466" y="${G - 640}" width="222" height="230" fill="${C.war}" stroke="${C.ink}" stroke-width="6"/>` +
      `<rect x="1482" y="${G - 624}" width="190" height="132" fill="${C.cream}" stroke="${C.ink}" stroke-width="4"/>` +
      H.label(1577, G - 574, 30, "EMERGENCY", "middle", C.war) + H.label(1577, G - 524, 40, "PULL", "middle", C.ink) +
      `<path d="M1554,${G - 470} H1600 V${G - 432} H1554 Z" fill="${C.yellow}" stroke="${C.ink}" stroke-width="4"/>` +
      // the glass gray with dust: nobody has pulled it in years
      `<rect x="1482" y="${G - 624}" width="190" height="132" fill="#8E877B" opacity="0.38"/>` +
      `<g fill="#6F695F" opacity="0.5">${[[1500, 610], [1530, 560], [1590, 600], [1640, 540], [1620, 512], [1520, 508], [1660, 600], [1556, 536]].map(([x, y]) => `<circle cx="${x}" cy="${G - y}" r="3"/>`).join("")}</g>`;
    const wm = K.castOpts("weaponsMaker", { mood: "grin" });
    // the stack's top bill, face out at the far end, and loose bills that flew off as it fell
    const endBill = bill(H, "war", 1370, G - 92, 1.5, 90, false);
    const loose = [[300, G - 250, -30], [1120, G - 260, 20], [1260, G - 330, -12], [700, G - 300, 40], [180, G - 40, 8]].map(([x, y, r]) => bill(H, "war", x, y, 0.8, r, false)).join("");
    const hand = `<path d="M1492,${G - 288} l-6,-34 l8,-2 l6,30 l2,-36 l8,0 l0,36 l6,-32 l8,2 l-4,34 l10,-20 l7,4 l-14,32 Z" fill="#C99A6B" stroke="${C.ink}" stroke-width="3" stroke-linejoin="miter"/>`;
    const svg = field(430) + man(H, wm, 560, G - 166, 2.0) + stack + endBill + splinters + builderEyes + arm + hand + post + hammer(H, 1290, G - 4, 2, 80) + loose;
    return { svg, alt: "The tall war-paper stack lies toppled across the field, the Weapons Maker riding on it; under its end, the flattened Builder's two blinking eyes and one hand reaching up toward the dusty EMERGENCY PULL box on its post, falling short." };
  },

  "considered-tuesday"(H, id) {
    const { K, C } = H;
    const page = (x, y, r, day) => H.at(x, y, 1.3, `<rect x="-40" y="-98" width="80" height="82" fill="#FFFFFF" stroke="${C.ink}" stroke-width="3.6"/><rect x="-40" y="-98" width="80" height="19" fill="${C.war}" stroke="${C.ink}" stroke-width="3.6"/>` +
      `<text x="0" y="-84" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="13" fill="#FFFFFF" letter-spacing="1.5">TUESDAY</text>` +
      `<text x="0" y="-31" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="44" fill="${C.ink}">${day}</text>`, r);
    const front = lecternBomb(H, 0.62) + mug(H, 800, 748, 1, -8) +
      H.at(620, 790, 1.5, K.props.calendar({ month: "TUESDAY", day: 16, pages: 2 })) + page(420, 760, -24, 15) + page(330, 930, 18, 14);
    const svg = H.host("smirk-smile", "palms-down", front);
    return { svg, alt: "Wishonia at her lectern, smirking, her mug on its way down; on the lectern a desk calendar showing TUESDAY, and two torn pages, both TUESDAY, fluttering down beside it; the Earth-bomb's fuse is half gone." };
  },

  "build-or-steal"(H, id) {
    const { K, C } = H;
    // the seesaw at the left edge, down on the Crook's end (the right one, toward town), the Builder's end up like a slide
    const see = `<path d="M130,${G} L180,${G - 90} L230,${G} Z" fill="${C.rust}" stroke="${C.ink}" stroke-width="5"/>` +
      `<path d="M-60,${G - 150} L400,${G - 40}" stroke="${C.ink}" stroke-width="26" stroke-linecap="butt"/><path d="M-60,${G - 150} L400,${G - 40}" stroke="#B98A55" stroke-width="16"/>` + slabs(H, 340, G - 60, 120, 6, 16);
    // skid marks from the low end of the plank down main street to where they stopped
    const skids = `<g stroke="#8E7A55" stroke-width="6" stroke-linecap="round" opacity="0.7"><path d="M420,${G - 4} H1000"/><path d="M440,${G + 12} H990"/><path d="M1070,${G - 2} H1200"/></g>`;
    const bench = desk(H, 560, G, 280, 150, false) + hammer(H, 500, G - 154, 1.6, 90) +
      `<rect x="590" y="${G - 172}" width="90" height="18" fill="#B98A55" stroke="${C.ink}" stroke-width="3"/><rect x="600" y="${G - 190}" width="60" height="18" fill="#B98A55" stroke="${C.ink}" stroke-width="3"/>`;
    // the chair he made, tipped over on its back: a seat, a back and only its two back legs
    const chair = H.at(1190, G - 10, 1.7, `<rect x="-26" y="-12" width="66" height="12" fill="#B98A55" stroke="${C.ink}" stroke-width="3.4"/>` +
      `<rect x="-38" y="-92" width="12" height="138" fill="#B98A55" stroke="${C.ink}" stroke-width="3.4"/><rect x="-30" y="-88" width="12" height="134" fill="#9C6B3F" stroke="${C.ink}" stroke-width="3"/>` +
      `<rect x="-26" y="-84" width="6" height="10" fill="none"/><path d="M-26,-80 H-14 M-26,-60 H-14 M-26,-40 H-14" stroke="${C.ink}" stroke-width="3"/>` +
      `<path d="M40,-6 v8 M28,-6 v8" stroke="${C.ink}" stroke-width="4"/>`, -90);
    const builder = { tone: 1, outfit: "overalls", color: 0, seed: 7, mood: "worried", arms: [[150, 160], [-150, -160]] };
    const stars = [[1040, G - 150], [1100, G - 190], [1150, G - 140]].map(([x, y]) => H.at(x, y, 1, K.star(0, 0, 26, C.yellow, 5) + `<circle r="4" fill="${C.orange}"/>`)).join("");
    const clock = `<circle cx="1640" cy="${G - 470}" r="54" fill="${C.cream}" stroke="${C.ink}" stroke-width="6"/>` +
      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].map((i) => { const a = (i * Math.PI) / 6; return `<path d="M${f1(1640 + 42 * Math.sin(a))},${f1(G - 470 - 42 * Math.cos(a))} L${f1(1640 + 48 * Math.sin(a))},${f1(G - 470 - 48 * Math.cos(a))}" stroke="${C.ink}" stroke-width="3"/>`; }).join("") +
      `<path d="M1640,${G - 470} V${G - 506}" stroke="${C.ink}" stroke-width="6" stroke-linecap="round"/><path d="M1640,${G - 470} L${f1(1640 + 26 * Math.sin((5 * Math.PI) / 6))},${f1(G - 470 - 26 * Math.cos((5 * Math.PI) / 6))}" stroke="${C.war}" stroke-width="8" stroke-linecap="round"/>`;
    const note = H.at(1700, G - 110, 1, `<rect x="-46" y="-30" width="92" height="56" fill="${C.cream}" stroke="${C.ink}" stroke-width="3"/>` + H.label(0, 8, 24, "RANSOM", "middle", C.war), -8);
    const svg = field(430) + see + skids +
      H.at(1205, G + 6, 0.36, K.props.factory({ label: "", smoke: false }), -9) + H.at(1350, G + 2, 0.31, K.props.capitol({}), 7) +
      bench + chair + man(H, builder, 900, G + 168, 2.2, "", 90) + stars +
      H.at(1640, G, 1.35, K.props.hospital({ label: "" })) + clock + H.at(1640, G - 60 * 1.35, 2.4, K.props.padlock({})) + note;
    return { svg, alt: "Main street: at the left edge the seesaw down on the Crook's end under a heap of war papers; the Builder flat on his back by his workbench beside a two-legged chair, the little factory and capitol skidded to a stop crooked behind him, skid marks back to the plank; next door the small hospital padlocked with a RANSOM note, the clock over its door on 5." };
  },

  "production-irrational"(H, id) {
    const { K, C } = H;
    // where the factory stood: a neat round crater, the Builder's crate and hammer at the bottom of it
    const hole = crater(H, 560, G - 6, 330, 70) + H.at(600, G + 14, 1.1, crate(C), -8) + hammer(H, 500, G + 22, 1.6, 100) + wisps(520, G - 80, 1.3);
    const crook = K.castOpts("lobbyist", { look: "right", arms: [[40, 80], [40, 80]], holdR: null, holdL: null });
    const builder = { tone: 1, outfit: "overalls", color: 0, seed: 7, mood: "flat", look: "left", arms: [[-150, -175], [20, 10]] };
    const RB = K.rig(builder), kb = 2.2, bx = 1490, ey = [bx + RB.eyes[0] * kb, G - 100 * kb + RB.eyes[1] * kb];
    const mask = H.at(ey[0] - 4, ey[1], kb, `<path d="M-16,-6 Q-8,-11 0,-6 Q8,-11 16,-6 L18,2 Q8,7 2,1 Q0,-1 -2,1 Q-8,7 -18,2 Z" fill="${C.navy}" stroke="${C.cream}" stroke-width="1.8" stroke-linejoin="round"/>` +
      `<ellipse cx="-8" cy="-1" rx="3.4" ry="2.6" fill="#FFFFFF"/><ellipse cx="8" cy="-1" rx="3.4" ry="2.6" fill="#FFFFFF"/><path d="M18,-2 l10,-6 M18,0 l9,4" stroke="${C.navy}" stroke-width="1.8"/>`);
    const svg = field(430) + hole +
      man(H, crook, 1180, G, 2.2) + man(H, builder, bx, G, kb) + mask +
      desk(H, 1330, G, 460, 150) + H.at(1250, G - 150, 1.7, K.props.laptop({})) + H.at(1440, G - 150, 1.7, K.props.laptop({})) +
      slabs(H, 1760, G, 210, 34, 18);
    return { svg, alt: "Where the Builder's factory stood, a neat round crater, smoke curling out of it, his crate and hammer left at the bottom; at the desk next door the untouched Masked Crook types while the Builder, unburnt, sits down beside him at a spare laptop, putting on a domino mask; the Crook's tall pile of war papers stands at the right." };
  },

  "failed-states"(H, id) {
    const { K, C } = H;
    // the crater where the factory stood, caved in and filled: a low mound of loose earth, one corner of the crate poking out
    const pancake = H.at(250, G - 6, 0.9, crate(C), 34) +
      `<path d="M80,${G + 6} Q120,${G - 40} 210,${G - 34} Q300,${G - 58} 390,${G - 36} Q500,${G - 54} 600,${G - 30} Q700,${G - 36} 760,${G + 6} Z" fill="#A88F5C" stroke="${C.ink}" stroke-width="4" stroke-linejoin="round"/>` +
      [[170, -18], [330, -30], [450, -24], [660, -16]].map(([x, d]) => `<path d="M${x - 18},${G + d + 12} L${x - 4},${G + d - 4} L${x + 16},${G + d + 10} Z" fill="#8E7748" stroke="${C.ink}" stroke-width="2.4"/>`).join("");
    const booth = `<rect x="470" y="${G - 250}" width="150" height="250" fill="${C.tan}" stroke="${C.ink}" stroke-width="5"/><rect x="494" y="${G - 220}" width="102" height="80" fill="${C.ink}"/><path d="M456,${G - 250} L545,${G - 300} L634,${G - 250} Z" fill="${C.rust}" stroke="${C.ink}" stroke-width="5"/>`;
    let bar = "";
    for (let i = 0; i < 8; i++) bar += `<rect x="${640 + i * 50}" y="${G - 170}" width="50" height="26" fill="${i % 2 ? C.cream : C.war}" stroke="${C.ink}" stroke-width="3.4"/>`;
    const crook = K.castOpts("lobbyist", { mood: "grin", arms: [[-20, -10], [176, 180]], holdR: null, holdL: null });
    const R = K.rig(crook), kc = 2.3, cx = 960;
    const hand = [cx + R.hand[1][0] * kc, G - 100 * kc + R.hand[1][1] * kc];
    const helmet = `<path d="M-30,-10 Q-30,-52 0,-54 Q30,-52 30,-10 L42,-6 L-42,-6 Z" fill="#6E7A55" stroke="${C.ink}" stroke-width="3" stroke-linejoin="miter"/>`;
    const hb = { tone: 3, hair: 1, outfit: "dress", color: 2, seed: 5, mood: "worried", look: "left", arms: [[-20, -10], [-150, -120]] };
    const RB = K.rig(hb), kh = 2.3, bx = 1480, bh = [bx + RB.hand[1][0] * kh, G - 100 * kh + RB.hand[1][1] * kh];
    const queue = [0, 1].map((i) => bill(H, "war", 1660 + i * 100, G - 42, 0.9, 0, true, i % 2)).join("");
    const svg = field(430) + pancake + booth + bar +
      man(H, crook, cx, G, kc, H.at(R.top[0], R.top[1] + 22, 0.8, helmet)) + H.at(hand[0], hand[1] + 6, 1.8, hut(C)) +
      man(H, hb, bx, G, kh) + hammer(H, bh[0], bh[1], 2.2, -60) + queue +
      `<path d="M${bh[0] - 40},${bh[1] - 80} l-14,-10 M${bh[0] - 20},${bh[1] - 96} l-4,-16 M${bh[0] - 56},${bh[1] - 54} l-16,-2" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>`;
    return { svg, alt: "Where the factory stood, the crater caved in and filled, a corner of the Builder's crate poking out of the loose earth, and a toll gate on it; the Masked Crook in an army helmet three sizes too big holds the Hut Builder's little hut up over his head, out of her reach, while she keeps hammering the air below it; war papers queue at the gate." };
  },

  "neighbors-house"(H, id) {
    const { K, C } = H;
    // the flash going over to the cloud: a white burst behind it, the frame washed pale
    const flash = `<g opacity="0.9">${K.star(1270, G - 330, 900, "#FFFFFF", 14)}</g><rect width="1920" height="1080" fill="#FFFFFF" opacity="0.28"/>`;
    const debris = [[1010, G - 520, 30], [1520, G - 600, -50], [1120, G - 700, 70], [1450, G - 760, 10]].map(([x, y, r]) =>
      `<rect x="${x - 34}" y="${y - 8}" width="68" height="16" fill="#B98A55" stroke="${C.ink}" stroke-width="3" transform="rotate(${r} ${x} ${y})"/>`).join("");
    const flying = H.at(1690, 330, 0.9, mailbox(H, 0, 110, "YOU"), 38) +
      `<path d="M1600,470 q-30,30 -70,40 M1630,500 q-24,34 -60,52" fill="none" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>`;
    const svg = field(430) + flash +
      H.at(430, G, 1.6, K.burn(K.props.house({ variant: 1 }))) + wisps(430, G - 470, 1.8) +
      mailbox(H, 820, G, "FAILED STATE") +
      `<rect x="1000" y="${G - 30}" width="540" height="34" fill="#A79B86" stroke="${C.ink}" stroke-width="5"/>` +
      H.at(1270, G - 20, 1.3, K.nuke()) + debris + flying;
    return { svg, alt: "The white flash going over to a mushroom cloud where the Watcher's house stood, planks flying, his YOU mailbox spinning up into the air in front of it; at the left the neighbor's house a black charred frame by its FAILED STATE mailbox." };
  },

  "once-it-starts"(H, id) {
    const { C } = H;
    // the mug at her lips, tipped toward her
    const front = lecternBomb(H, 0.4) + mug(H, 850, 640, 1.35, -26);
    const svg = H.host("sideeye-closed", "idle", front);
    return { svg, alt: "Wishonia at her lectern with her mug at her lips, sipping, eyes on the camera; beside her on the lectern the Earth-bomb's spark fizzes with about a third of its fuse left, just short of the curl." };
  },

  "try-all-three"(H, id) {
    const { K, C } = H;
    const bulb = `<rect x="626" y="${G - 330}" width="14" height="330" fill="${C.peri}" stroke="${C.ink}" stroke-width="4"/><rect x="590" y="${G - 14}" width="86" height="14" fill="${C.slate}" stroke="${C.ink}" stroke-width="4"/>` +
      `<circle cx="633" cy="${G - 430}" r="78" fill="#A9A397" stroke="${C.ink}" stroke-width="6"/><rect x="603" y="${G - 360}" width="60" height="34" fill="${C.peri}" stroke="${C.ink}" stroke-width="5"/><path d="M612,${G - 440} q10,-30 21,0 q11,30 21,0" fill="none" stroke="${C.ink}" stroke-width="4"/>`;
    const rug = `<ellipse cx="1240" cy="${G - 6}" rx="300" ry="44" fill="${C.rust}" stroke="${C.ink}" stroke-width="6"/><ellipse cx="1240" cy="${G - 6}" rx="250" ry="32" fill="none" stroke="${C.orange}" stroke-width="5"/>`;
    const stand = `<path d="M1420,${G - 10} V${G - 330}" stroke="${C.slate}" stroke-width="10"/><path d="M1380,${G - 6} L1420,${G - 40} L1460,${G - 6}" fill="none" stroke="${C.slate}" stroke-width="8"/>` +
      `<path d="M1420,${G - 330} q-60,-30 -112,-4" fill="none" stroke="${C.ink}" stroke-width="6"/><circle cx="1306" cy="${G - 334}" r="12" fill="${C.ink}"/>`;
    const spot = `<path d="M1700,${G} L1740,${G - 230} L1780,${G}" fill="none" stroke="${C.slate}" stroke-width="9"/><g transform="translate(1740,${G - 260}) rotate(-28)"><rect x="-60" y="-44" width="110" height="88" fill="${C.slate}" stroke="${C.ink}" stroke-width="6"/><ellipse cx="-62" cy="0" rx="14" ry="44" fill="#3D4357" stroke="${C.ink}" stroke-width="5"/></g>`;
    const watcher = { tone: 0, outfit: "suit", color: 1, seed: 3, charred: true, look: "right", arms: [[10, 4], [60, 120]] };
    const svg = field(430) +
      H.at(300, G, 2.6, K.props.ballotBox({ ballot: true })) + bulb + rug + spot + stand +
      man(H, watcher, 1170, G - 8, 2.5, "", 10) + wisps(1170, G - 520, 1.2);
    return { svg, alt: "On the empty lot: the ballot box with his ballot stuck back out of its slot, the big light bulb gone dark, the spotlight off; on the round rug the charred Watcher leans in to the headset microphone on its stand, about to speak to nobody." };
  },

  "25-percent-by-2033"(H, id) {
    const { K, C } = H;
    const gauge = K.props.gauge({ value: 11.5 / 30, zones: [[25 / 30, 1, C.war]], marks: [[0, "0"], [0.5, "15"], [25 / 30, "25"], [1, "30"]], window: "2033", label: "% OF GDP" });
    const glow = "";
    const tv = H.at(330, G - 100 * 1.4, 1.4, K.props.tvSet({}));
    const gears = H.at(330, G, 1.4, K.props.gears({ n: 3, dark: true }));
    const crank = `<path d="M470,${G - 8} L540,${G - 30} L548,${G - 18}" fill="none" stroke="${C.ink}" stroke-width="12" stroke-linecap="round"/><path d="M470,${G - 8} L540,${G - 30} L548,${G - 18}" fill="none" stroke="${C.peri}" stroke-width="6" stroke-linecap="round"/><circle cx="550" cy="${G - 16}" r="9" fill="${C.yellow}" stroke="${C.ink}" stroke-width="3"/>`;
    const binder = H.at(830, G, 1, `<path d="M-70,0 V-250 H70 V0 Z" fill="${C.navy}" stroke="${C.ink}" stroke-width="6"/><rect x="-70" y="-250" width="26" height="250" fill="${C.slate}" stroke="${C.ink}" stroke-width="5"/>` +
      `<rect x="-36" y="-206" width="96" height="44" fill="${C.cream}" stroke="${C.ink}" stroke-width="3"/>` + H.label(12, -172, 34, "PLAN", "middle", C.ink) +
      `<g transform="translate(14,-96) rotate(-14)"><path d="M-62,-26 L58,-30 L62,24 L-58,28 Z" fill="${C.yellow}" stroke="${C.ink}" stroke-width="4"/>` + H.label(0, 12, 32, "TERRIBLE", "middle", C.war) + "</g>");
    const sprout = `<path d="M600,${G} q-4,-50 6,-80" fill="none" stroke="#5B7A3A" stroke-width="6"/>` + bill(H, "war", 588, G - 72, 0.42, -30, false) + bill(H, "war", 630, G - 92, 0.42, 26, false);
    const svg = field(430) + glow + H.at(1290, G, 3.1, gauge) +
      H.at(1050, G, 1.7, K.props.headstone({ text: "USSR" })) + gears + tv + crank + sprout + binder;
    return { svg, alt: "At the foot of the giant gauge, its red zone lit and 2033 in its window, a headstone reads USSR; beside the grave the old crank computer, a TV cabinet on a box of gears, its crank fallen to the ground, a tiny sprout of war papers, and a thick PLAN binder with a TERRIBLE sticker, standing up proud." };
  },

  "no-plan"(H, id) {
    const { K, C } = H;
    const gauge = K.props.gauge({ value: 13.4 / 30, zones: [[25 / 30, 1, C.war]], marks: [[0, "0"], [0.5, "15"], [25 / 30, "25"], [1, "30"]], window: "2033", label: "% OF GDP" });
    const gx = 960, gk = 2.6, dcy = G - 100 * gk;
    let vine = `<path d="M1240,${G - 10} C1200,${G - 120} 1160,${dcy + 120} ${gx + 160},${dcy + 40} C${gx + 240},${dcy - 80} ${gx + 120},${dcy - 220} ${gx},${dcy - 200} C${gx - 140},${dcy - 200} ${gx - 230},${dcy - 60} ${gx - 170},${dcy + 60}" fill="none" stroke="#5B7A3A" stroke-width="9" stroke-linecap="round"/>`;
    [[1215, G - 120, 30], [gx + 190, dcy + 10, -20], [gx + 150, dcy - 150, 40], [gx - 40, dcy - 205, -10], [gx - 190, dcy - 100, 20], [gx - 180, dcy + 40, -30]].forEach(([x, y, r]) => { vine += bill(H, "war", x, y, 0.5, r, false); });
    const rubble = [[300, -10], [360, 12], [420, -4], [470, 18], [340, 30], [410, 26]].map(([x, r], i) => `<path d="M${x - 40},${G} L${x - 30},${G - 40 - (i % 3) * 14} L${x + 26},${G - 52 - (i % 2) * 10} L${x + 40},${G} Z" fill="${i % 2 ? C.slate : C.navy}" stroke="${C.ink}" stroke-width="4" transform="rotate(${r} ${x} ${G})"/>`).join("");
    const pol = K.castOpts("politician", { arms: [[-40, -110], [150, 100]], holdR: null, holdL: null });
    const R = K.rig(pol), kp = 2.3, px = 1540;
    const lh = [px + R.hand[0][0] * kp, G - 100 * kp + R.hand[0][1] * kp], rh = [px + R.hand[1][0] * kp, G - 100 * kp + R.hand[1][1] * kp];
    const thumb = H.at(rh[0], rh[1], 2.2, `<rect x="-7" y="-6" width="14" height="14" rx="3" fill="#E0A877" stroke="${C.ink}" stroke-width="2"/><rect x="-3" y="-20" width="7" height="16" rx="3" fill="#E0A877" stroke="${C.ink}" stroke-width="2"/>`);
    const svg = field(430) + H.at(gx, G, gk, gauge) + vine + H.at(1240, G, 2, K.props.laptop({})) +
      H.at(560, G, 1.5, K.props.headstone({ text: "USSR" })) + rubble + wisps(390, G - 90, 1.2) + rosette(H, 390, G - 76, 1.1) +
      man(H, pol, px, G, kp) + H.at(lh[0] - 10, lh[1] + 70, 1.7, K.props.clipboard({ title: "PLAN:", items: [] })) + thumb;
    return { svg, alt: "The whole gauge, a vine of war papers wrapped round its dial and its needle a notch short of 15; on the left the Soviet side a smoking heap of rubble at the foot of the USSR headstone with the 1ST rosette on top; on the right the Politician grinning, thumbs up, holding a clipboard that says PLAN: and nothing else." };
  },

  "this-is-a-loop"(H, id) {
    // the spark just out of the curl: a ring of smoke hangs where the curl burned
    const x = 925, y = 790;
    const smoke = `<path d="M${x + 14},${y - 168} C${x + 34},${y - 182} ${x + 66},${y - 170} ${x + 70},${y - 146} C${x + 72},${y - 120} ${x + 44},${y - 108} ${x + 26},${y - 122} C${x + 10},${y - 136} ${x + 16},${y - 160} ${x + 30},${y - 172}" fill="none" stroke="#A9A193" stroke-width="10" stroke-linecap="round" opacity="0.75"/>` +
      wisps(x + 44, y - 190, 0.8);
    const front = mug(H, 610, 790) + smoke + lecternBomb(H, 0.09);
    const svg = H.host("sideeye-closed", "arms-crossed", front);
    return { svg, alt: "Wishonia at her lectern, arms crossed, side-eyeing the camera; beside her mug the Earth-bomb's spark has just come round the curl in its fuse, a ring of smoke hanging where the curl was, and only a stub of fuse left." };
  },

  "loop-not-line-item"(H, id) {
    const { K, C } = H;
    const HL = 500, RR = 260, cx = 960, cy = 570, RW = 90;
    const road = (w, col, extra = "") => `<path d="M${cx - HL},${cy - RR} H${cx + HL} A${RR},${RR} 0 0,1 ${cx + HL},${cy + RR} H${cx - HL} A${RR},${RR} 0 0,1 ${cx - HL},${cy - RR} Z" fill="none" stroke="${col}" stroke-width="${w}" ${extra}/>`;
    const k = 0.8;
    const ledger = H.at(cx, cy - 40, 0.72, `<path d="M-230,-120 L0,-100 L230,-120 L240,110 L0,130 L-240,110 Z" fill="${C.cream}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="miter"/><path d="M0,-100 V130" stroke="${C.ink}" stroke-width="4"/>` +
      [-70, -30, 10, 50, 90].map((y, i) => `<path d="M-210,${y} H-20 M20,${y} H210" stroke="${C.peri}" stroke-width="3"/>${i === 2 ? `<path d="M-200,${y - 30} H-30" stroke="${C.war}" stroke-width="3" stroke-dasharray="10 8"/>` : ""}`).join(""));
    const press = H.at(cx - 420, cy - RR - 62, 0.5, K.props.printingPress({ seal: "war", label: "1913" }));
    const pol = man(H, K.castOpts("politician", { look: "left", arms: [[-100, -110], [10, 4]], holdR: null }), cx - 300, cy - RR - 62, k);
    // the bread's price tag, swollen like a balloon, bursting
    const burst = [0, 1, 2, 3, 4, 5, 6, 7].map((i) => { const a = (i * Math.PI) / 4; return `<path d="M${f1(80 + 70 * Math.cos(a))},${f1(-170 + 70 * Math.sin(a))} L${f1(80 + 104 * Math.cos(a))},${f1(-170 + 104 * Math.sin(a))}" stroke="${C.ink}" stroke-width="5" stroke-linecap="round"/>`; }).join("");
    const bread = H.at(cx + 260, cy - RR - 62, 1, `<rect x="-70" y="-60" width="140" height="60" fill="${C.tan}" stroke="${C.ink}" stroke-width="4"/><path d="M-50,-60 Q-52,-84 -20,-86 Q20,-92 40,-74 Q52,-64 48,-60 Z" fill="#D49A4E" stroke="${C.ink}" stroke-width="3.4"/>` +
      `<path d="M30,-80 L70,-118" stroke="${C.ink}" stroke-width="2.4"/>` + burst +
      `<g transform="translate(80,-170) rotate(30)"><path d="M-62,-40 L44,-40 L74,0 L44,40 L-62,40 Z" fill="#FFFFFF" stroke="${C.ink}" stroke-width="4" stroke-linejoin="miter"/><circle cx="46" cy="0" r="7" fill="none" stroke="${C.ink}" stroke-width="3"/>` +
      `<text x="-10" y="20" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="58" fill="${C.ink}">$</text></g>`);
    const fac = H.at(cx + HL + RR + 10, cy - 30, 0.5, K.props.factory({ label: "", smoke: false }));
    const b1 = man(H, { tone: 1, outfit: "overalls", color: 0, seed: 7, mood: "sad", look: "left", arms: [[-20, -10], [-70, -80]] }, cx + HL + RR + 20, cy + 120, k) + bill(H, "plain", cx + HL + RR - 46, cy + 16, 0.14, 0, false);
    // stations 4 and 5 stand inside the loop, behind its bottom straight
    const by = cy + RR - 64;
    const deskS = man(H, K.castOpts("lobbyist", { arms: [[40, 80], [40, 80]], holdR: null, holdL: null }), cx + 300, by, k) +
      man(H, { tone: 1, outfit: "overalls", color: 0, seed: 7, mask: true, arms: [[40, 80], [40, 80]] }, cx + 460, by, k) + desk(H, cx + 380, by, 260, 70);
    const stack = slabs(H, cx - 390, by, 140, 20, 12) + man(H, K.castOpts("weaponsMaker", { arms: [[150, 170], [-150, -170]], hold: null }), cx - 390, by - 240, k) +
      H.at(cx - 380, by - 240 - 104, 0.4, K.props.missile({ mood: "smug", arms: "none" }), 12);
    const fly = [[cx + HL + RR - 10, cy - 200, 30], [cx + HL + RR + 20, cy + 230, -40], [cx - HL - RR - 20, cy - 120, -30], [cx - HL - RR + 10, cy + 260, 50], [cx + 200, cy - RR - 30, 0], [cx - 100, cy + RR + 10, 0], [cx + 360, cy + RR - 8, 0], [cx - 380, cy - RR + 6, 0]]
      .map(([x, y, r], i) => bill(H, "war", x, y, 0.62, r, true, i % 2)).join("");
    const svg = `<rect width="1920" height="1080" fill="${GROUND}"/>` + road(RW + 14, EDGE) + road(RW, ROAD) + road(5, DASH, 'stroke-dasharray="30 36"') +
      ledger + press + pol + bread + fac + b1 + stack + deskS + fly;
    return { svg, alt: "Pulled back on the whole loop of road: the Politician cranking the 1913 press, the bread whose swollen price tag just burst, the Builder at the factory gate with his sliver of a paycheck, the Builder masked at the laptop beside the Crook, the war-paper stack with the Weapons Maker on top; war papers run round the loop so fast they fly off the bends, and the ledger lies open in the middle with one line gone." };
  },

  "thats-homework"(H, id) {
    const { K, C } = H;
    const ruins = H.at(240, G - 40, 1.2, K.burn(K.props.house({ variant: 3 }))) + H.at(1720, G - 40, 1.25, K.burn(K.props.house({ variant: 0 }))) + wisps(1700, G - 420, 1.4);
    const kid = { tone: 2, outfit: "shirt", color: 3, seed: 11, mood: "eager", mask: true, build: { hs: 1.3, legs: 0.6, th: 0.75, neck: 0.5 }, arms: [[40, 70], [40, 80]] };
    const pol = K.castOpts("politician", { look: "left", mood: "grin", arms: [[-60, -80], [10, 4]], holdR: null });
    const RP = K.rig(pol), kp = 2.3, px = 1330, ph = [px + RP.hand[0][0] * kp, G - 100 * kp + RP.hand[0][1] * kp];
    // the worksheet propped on the desk, the gold star just going on from the Politician's hand
    const sheet = H.at(1010, G - 126, 1, `<path d="M-122,0 L-114,-124 L126,-132 L122,0 Z" fill="#FFFFFF" stroke="${C.ink}" stroke-width="4" stroke-linejoin="miter"/>` +
      `<text x="0" y="-38" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="40" fill="${C.ink}" transform="rotate(-2)">$ &lt; $$$$$</text>` +
      H.at(92, -104, 1, H.K.star(0, 0, 26, C.yellow, 5) + `<circle r="5" fill="${C.orange}"/>`), -2);
    const flatTank = tank(H, 380, G, 1.5, true) + `<g transform="translate(400,${G - 30}) scale(2.6,1.7)">${K.props.priceTag({ text: "$$$$$", anchor: "bottom", angle: 0 })}</g>`;
    const RK = K.rig(kid), kk = 2.4 * 0.7, kx = 790, kg = G - 20, ke = [kx + RK.eyes[0] * kk, kg - 100 * kk + RK.eyes[1] * kk];
    const kidMask = H.at(ke[0] - 4, ke[1], kk * 1.1, `<path d="M-16,-6 Q-8,-11 0,-6 Q8,-11 16,-6 L18,2 Q8,7 2,1 Q0,-1 -2,1 Q-8,7 -18,2 Z" fill="${C.navy}" stroke="${C.cream}" stroke-width="1.8" stroke-linejoin="round"/>` +
      `<ellipse cx="-8" cy="-1" rx="3.4" ry="2.6" fill="#FFFFFF"/><ellipse cx="8" cy="-1" rx="3.4" ry="2.6" fill="#FFFFFF"/>`);
    // the schoolhouse, its four walls fallen flat outward round the desk: the back wall and the stamped roof behind, the front wall in front
    const school = `<path d="M560,${G - 150} H1240 L1290,${G - 214} H470 Z" fill="${C.slate}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      mark(H, 520, G - 160, 0.8, "SANCTIONED", -2) +
      `<path d="M600,${G - 76} H1200 L1240,${G - 150} H560 Z" fill="${C.rust}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      [700, 900, 1100].map((wx) => `<path d="M${wx - 40},${G - 88} H${wx + 40} L${wx + 46},${G - 136} H${wx - 34} Z" fill="${C.cream}" stroke="${C.ink}" stroke-width="3.4"/>`).join("") +
      `<path d="M600,${G + 6} H1200 L1250,${G + 96} H550 Z" fill="${C.rust}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      [720, 1080].map((wx) => `<path d="M${wx - 50},${G + 26} H${wx + 50} L${wx + 58},${G + 76} H${wx - 58} Z" fill="${C.cream}" stroke="${C.ink}" stroke-width="3.4"/>`).join("");
    const svg = field(430) + ruins + flatTank + school +
      man(H, kid, kx, kg, kk) + kidMask + desk(H, 900, G, 400, 126) + H.at(830, G - 126, 1.5, K.props.laptop({})) + tag(H, 860, G - 190, 1.1, "$", 18) + sheet +
      man(H, pol, px, G, kp);
    return { svg, alt: "In the bombed town, among charred houses, the schoolhouse lies open with its walls fallen flat round its one desk, the SANCTIONED roof behind; the Kid, unhurt, in a tiny domino mask, sits at the desk; his worksheet reads $ < $$$$$ with a gold star on it; the Politician leans over him, grinning like a proud teacher; at the left, the flattened tank squashed flatter under a huge $$$$$ tag, and a $ tag on the Kid's laptop." };
  },

  "defund-the-loop"(H, id) {
    const { K, C } = H;
    const road = `<rect y="${G - 120}" width="1920" height="130" fill="${EDGE}"/><rect y="${G - 113}" width="1920" height="116" fill="${ROAD}"/><path d="M0,${G - 55} H1920" stroke="${DASH}" stroke-width="7" stroke-dasharray="46 54"/>`;
    const back = H.at(1380, 600, 0.85, K.props.colorFlipFunnel({ inN: 2, outN: 2 })) + H.at(1760, 600, 0.8, K.props.lab({})) +
      [0, 1].map((i) => bill(H, "med", 1530 + i * 70, 580, 0.5, 0, true, i % 2)).join("") +
      man(H, K.castOpts("scientist", { look: "left", arms: [[-30, -120], [-60, -100]], holdL: null, holdR: null }), 1640, 600, 1.0);
    const wm = man(H, K.castOpts("weaponsMaker", { mood: "sad", arms: [[40, 70], [-40, -70]], hold: null }), 260, 640, 1.2) +
      H.at(260, 600, 0.5, K.props.missile({ mood: "flat", arms: "none" }), 90) + H.label(330, 470, 36, "Z", "middle", C.ink) + H.label(360, 430, 26, "z", "middle", C.ink);
    const pol = K.castOpts("politician", { look: "right", mood: "grin", arms: [[-10, -4], [160, 120]], holdR: null });
    const R = K.rig(pol), kp = 2.3, px = 620, rh = [px + R.hand[1][0] * kp, G - 120 - 100 * kp + R.hand[1][1] * kp];
    const svg = field(430) + back + wm + road +
      H.at(880, G - 116, 2.2, K.props.sign({ text: "ILLEGAL", height: 90 }), 4) + man(H, pol, px, G - 120, kp) + hammer(H, rh[0], rh[1], 2.4, 40) +
      bill(H, "war", 1180, G - 66, 1.35, 0, true, 1) + `<path d="M1060,${G - 60} h-50 M1066,${G - 80} h-60 M1060,${G - 40} h-40" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>`;
    return { svg, alt: "Beside the loop's road the Politician hammers in an ILLEGAL sign while the last war paper runs straight past it; behind them medicine papers file out of the color-flip funnel to the Scientist's lab bench, and the Weapons Maker sits on the ground with his missile asleep." };
  },

  "you-defund-it"(H, id) {
    const front = lecternProps(H, 0.04, false, true);
    const svg = H.host("smirk-smile", "idle", front);
    return { svg, alt: "Wishonia at her lectern smirks at the camera; beside her mug the Earth-bomb's fuse is a stub, its spark out, one smoke ring rising." };
  },
};
