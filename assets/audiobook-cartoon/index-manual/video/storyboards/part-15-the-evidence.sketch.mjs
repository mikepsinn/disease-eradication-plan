// Sketches for storyboards/part-15-the-evidence.md: each scene's key moment on a 1920 x 1080 frame, drawn with the
// production art (kit.js, film.js and the props library) in the atomic-age film look of Part 2. Built into the review
// sheet by tools/storyboard-sheet.mjs. Host shots use H.host (KIT.STUDIO's 16:9 set: Wishonia's rig x 480 to 1040,
// the lectern's reading top at y 790, the free wall right of it x 1100 to 1880). A plate frame is one framing of its
// plate as the camera sees it, the ground and the cast drawn large. Nothing important below y 900.

const FIELD = "#C8B07B"; // Part 2's plate field
const f1 = (n) => n.toFixed(1);

// A person standing with its feet at (x, feetY), at scale k (KIT.person's feet are at y 100).
function stand(H, x, feetY, k, inner) {
  return H.at(x, feetY - 100 * k, k, inner);
}

// ── The tower of forms (proof-required, sixty-five-years) ──
// Bundles of cream forms tied with string, stacked a little crooked from the floor out of the top of the frame.
// dusty: gray with dust, for sixty-five years later.
function tower(H, cx, w, dusty) {
  const { C } = H;
  const paper = dusty ? "#CFC6AE" : "#FBF6E6", edge = dusty ? "#B9AF96" : "#E6D9B4", string = dusty ? "#9C8F78" : C.rust;
  let out = "";
  const jit = [0, 14, -10, 8, -16, 6, 18, -6, 10, -14, 4, 16, -8, 12, -4, 8, -12];
  let y = 1090;
  for (let i = 0; i < 17; i++) {
    const h = 66 + (i % 3) * 6, x = cx - w / 2 + jit[i], ww = w - (i % 2) * 12;
    y -= h;
    let sheets = "";
    for (let s = y + 8; s < y + h - 4; s += 7) sheets += `<path d="M${x + 3},${s} H${x + ww - 3}" stroke="${edge}" stroke-width="2"/>`;
    out += `<rect x="${x}" y="${y}" width="${ww}" height="${h}" fill="${paper}" stroke="${C.line}" stroke-width="4"/>` + sheets +
      `<path d="M${x + ww * 0.32},${y} V${y + h} M${x},${y + h * 0.5} H${x + ww}" stroke="${string}" stroke-width="5"/>` +
      `<path d="M${x + ww * 0.32 - 10},${y + h * 0.5 - 8} l10,8 l10,-8" fill="none" stroke="${string}" stroke-width="4"/>`;
  }
  return out;
}

// A cobweb in a corner at (x, y): spokes over the angles a0..a1 (degrees, 0 = +x, 90 = down), length r, and sagging rings.
function cobweb(x, y, r, a0, a1, col = "#F6F1E1") {
  const n = 6, rings = [0.35, 0.62, 0.9];
  const pt = (a, rr) => [x + rr * Math.cos((a * Math.PI) / 180), y + rr * Math.sin((a * Math.PI) / 180)];
  let d = "";
  for (let i = 0; i < n; i++) {
    const a = a0 + ((a1 - a0) * i) / (n - 1), p = pt(a, r);
    d += `M${x},${y} L${f1(p[0])},${f1(p[1])} `;
  }
  for (const k of rings) {
    for (let i = 0; i < n - 1; i++) {
      const aa = a0 + ((a1 - a0) * i) / (n - 1), ab = a0 + ((a1 - a0) * (i + 1)) / (n - 1), p = pt(aa, r * k), q = pt(ab, r * k), m = pt((aa + ab) / 2, r * k * 0.86);
      d += `M${f1(p[0])},${f1(p[1])} Q${f1(m[0])},${f1(m[1])} ${f1(q[0])},${f1(q[1])} `;
    }
  }
  return `<path d="${d}" fill="none" stroke="${col}" stroke-width="2.4" opacity="0.85"/>`;
}
// Smoke curls rising from (x, y).
function smoke(x, y, s = 1, col = "#8C8782") {
  return [0, 1, 2].map((i) => `<path d="M${x + (i - 1) * 22 * s},${y - i * 6} q${-14 * s},${-22 * s} 0,${-44 * s} q${14 * s},${-22 * s} 0,${-44 * s}" fill="none" stroke="${col}" stroke-width="${6 * s}" stroke-linecap="round" opacity="0.8"/>`).join("");
}

// ── Money bills lying flat in a stack, seen from the front (postwar-boom) ──
function slab(H, x, y, w, h, seal = true) {
  const { C } = H;
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="3" fill="${C.money}" stroke="${C.line}" stroke-width="3.4"/>` +
    `<path d="M${x + 10},${y + h / 2} H${x + w - 10}" stroke="${C.moneyDark}" stroke-width="2"/>` +
    `<ellipse cx="${x + w / 2}" cy="${y + h / 2}" rx="${h * 0.6}" ry="${h * 0.32}" fill="${C.paper}" stroke="${C.moneyDark}" stroke-width="2"/>` +
    (seal ? `<circle cx="${x + w - 26}" cy="${y + h / 2}" r="${h * 0.36}" fill="${C.moneyDark}" stroke="${C.line}" stroke-width="2"/>` : "");
}

// The Earth case file as Part 12 draws it (its caseFile, copied): standing propped up on the lectern's left end, the
// tab "~~EARTH~~ DIRT: CASE #847", Part 1's MAY BE ELIGIBLE FOR OPTIMIZATION and Part 12's SUBOPTIMAL on its cover.
// dusty: under 65 years of dust (grayed, the stamps faded).
function caseFile(H, dusty) {
  const { C, K } = H, ink = C.line, S = K.STUDIO;
  const manila = dusty ? "#BDB29A" : "#E7C98C", fade = dusty ? 0.45 : 1;
  const s = `<path d="M-95,0 L-95,-150 L-40,-150 L-30,-166 L40,-166 L50,-150 L95,-150 L95,0 Z" fill="${manila}" stroke="${ink}" stroke-width="4" stroke-linejoin="miter"/>` +
    `<text x="5" y="-153" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="11" fill="${ink}"><tspan text-decoration="line-through">EARTH</tspan> DIRT: CASE #847</text>` +
    `<path d="M-23,-157 H6" stroke="${ink}" stroke-width="1.6"/>` +
    `<g opacity="${fade}"><g transform="translate(0,-100) rotate(-6)"><rect x="-82" y="-24" width="164" height="40" fill="none" stroke="${C.med}" stroke-width="3"/><text x="0" y="-6" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="15" fill="${C.med}">MAY BE ELIGIBLE</text><text x="0" y="11" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="15" fill="${C.med}">FOR OPTIMIZATION</text></g>` +
    `<g transform="translate(4,-36) rotate(4)"><rect x="-84" y="-22" width="168" height="40" fill="none" stroke="${C.war}" stroke-width="4"/><rect x="-78" y="-17" width="156" height="30" fill="none" stroke="${C.war}" stroke-width="1.6"/><text x="0" y="8" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="24" letter-spacing="1.5" fill="${C.war}">SUBOPTIMAL</text></g></g>`;
  return H.at(S.lect[0] - S.lect[1] / 2 + 120, S.top + 6, 0.82, s);
}
// Where the case file's top right corner sits (for the cobweb over it).
function caseCorner(H) {
  const S = H.K.STUDIO;
  return [S.lect[0] - S.lect[1] / 2 + 120 + 95 * 0.82, S.top + 6 - 150 * 0.82];
}

export default {
  "the-evidence-title"(H, id) {
    const { K, C } = H;
    // the atomic card: plain navy, the emblem (three orbits, an orange nucleus, three running war papers)
    const cx = 960, cy = 300, rx = 200, ry = 62;
    const orbits = [0, 60, -60].map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = [[0, 0.6], [60, 2.7], [-60, 4.8]].map(([a, th], i) => {
      const r = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return H.at(cx + ex * Math.cos(r) - ey * Math.sin(r), cy + ex * Math.sin(r) + ey * Math.cos(r) - 6, 0.62, K.money("war", i % 2));
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    const italic = `<text x="960" y="796" text-anchor="middle" font-family="Inter" font-weight="700" font-style="italic" font-size="44" fill="${C.cream}" stroke="${C.ink}" stroke-width="6" stroke-linejoin="round" style="paint-order:stroke">Unlike Everything Else Humanity Has Tried</text>`;
    // the stamp plate, tilted, just landed: the Lobbyist is under it
    const pw = 560, ph = 108, px = 960, py = 870;
    const plate = `<g transform="translate(${px},${py}) rotate(-4)">` +
      `<rect x="${-pw / 2 + 7}" y="${-ph / 2 + 9}" width="${pw}" height="${ph}" fill="${C.ink}"/>` +
      `<rect x="${-pw / 2}" y="${-ph / 2}" width="${pw}" height="${ph}" fill="${C.war}" stroke="${C.ink}" stroke-width="4"/>` +
      `<rect x="${-pw / 2 + 8}" y="${-ph / 2 + 8}" width="${pw - 16}" height="${ph - 16}" fill="none" stroke="${C.cream}" stroke-width="7"/>` +
      `<text x="0" y="26" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="74" letter-spacing="5" fill="${C.cream}">THE EVIDENCE</text></g>`;
    // the gag: his gloved hand pokes out under the plate's left end, letting go of a war bill; his fedora rolls out the right
    const glove = `<path d="M-64,-12 L-24,-14 L-22,12 L-64,14 Z" fill="${C.tan}" stroke="${C.cream}" stroke-width="3"/>` +
      `<path d="M-24,-10 L8,-12 L20,-20 L28,-12 L18,-5 L32,-2 L32,7 L16,9 L6,14 L-24,10 Z" fill="${C.slate}" stroke="${C.cream}" stroke-width="3" stroke-linejoin="miter"/>`;
    const hand = H.at(px - pw / 2 + 70, py + ph / 2 - 2, 1.6, glove, -4);
    const bill = H.at(px - pw / 2 + 96, py + ph / 2 + 70, 0.62, K.money("war", 1), -24);
    const fedora = H.at(px + pw / 2 + 70, py + 40, 1.6,
      `<path d="M-30,6 Q0,-2 30,6 L26,12 Q0,6 -26,12 Z" fill="${C.slate}" stroke="${C.cream}" stroke-width="2.6"/><path d="M-17,4 L-14,-16 Q0,-22 14,-16 L17,4 Z" fill="${C.slate}" stroke="${C.cream}" stroke-width="2.6"/><path d="M-16,-2 H16" stroke="${C.rust}" stroke-width="4"/>`, 28);
    const shoe = H.at(px + pw / 2 - 30, py + ph / 2 - 16, 1.4, `<path d="M-30,0 L10,-2 L34,8 L-30,10 Z" fill="${C.ink}" stroke="${C.cream}" stroke-width="2.6"/>`, -4);
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus +
      H.big(960, 600, 78, "WHY THIS COULD", "middle", C.cream) + H.big(960, 728, 138, "ACTUALLY WORK", "middle", C.cream) + italic +
      plate + shoe + hand + bill + fedora;
    return { svg, alt: "The navy period title card: the atom emblem with three running war bills, WHY THIS COULD ACTUALLY WORK, the italic line Unlike Everything Else Humanity Has Tried, and the red THE EVIDENCE stamp plate just slammed down on the Lobbyist, his gloved hand poking out and dropping a war bill, his fedora rolling away." };
  },

  "proof-required"(H, id) {
    const { K, C } = H;
    const forms = tower(H, 1330, 270, false);
    // the WAR console and the charred Politician, his finger on the button, still waving
    const k = 2.7, feet = 1066;
    const pol = stand(H, 150, feet, k, K.cast("politician", { charred: true, look: "right", arms: [[-160, -175], [40, 68]] }));
    const btn = H.at(372, feet, k, K.props.yesButton({ label: "WAR", color: C.war }));
    const note = H.at(318, feet - 92 * k, 1, `<rect x="-24" y="-24" width="48" height="44" fill="#F4E27A" stroke="${C.line}" stroke-width="3"/>`, -10);
    const puff = smoke(372, feet - 120 * k, 1.4) + smoke(170, feet - 205 * k, 1.1);
    const svg = H.host("skeptical-closed", "arms-crossed", caseFile(H, false) + forms + pol + btn + note + puff);
    return { svg, alt: "The studio set: Wishonia at her lectern with her arms folded; on her right a tower of tied bundles of forms runs out of the top of the frame; on her left the Politician stands charred black, hair up, eyes blinking, smoke rising, his finger still on a red WAR button with one blank sticky note on its console." };
  },

  "recovery-trial"(H, id) {
    const { K, C } = H;
    const wall = C.cream, low = K.mix(C.tan, C.cream, 0.45), floor = K.mix(C.tan, C.slate, 0.25);
    let svg = `<rect width="1920" height="1080" fill="${wall}"/><rect y="640" width="1920" height="130" fill="${low}"/><rect y="634" width="1920" height="10" fill="${C.rust}"/><rect y="770" width="1920" height="310" fill="${floor}"/><path d="M0,770 H1920" stroke="${C.line}" stroke-width="4"/>`;
    // the alarm light, spinning
    svg += `<g transform="translate(250,150)"><path d="M-40,0 A40,40 0 0 1 40,0 Z" fill="${C.war}" stroke="${C.line}" stroke-width="4"/><rect x="-50" y="0" width="100" height="16" fill="${C.slate}" stroke="${C.line}" stroke-width="4"/>` +
      [-150, -115, -65, -30].map((a) => { const r = (a * Math.PI) / 180; return `<path d="M${f1(60 * Math.cos(r))},${f1(60 * Math.sin(r))} L${f1(110 * Math.cos(r))},${f1(110 * Math.sin(r))}" stroke="${C.war}" stroke-width="8" stroke-linecap="round"/>`; }).join("") + "</g>";
    // the lab bench, boiling over, at the left
    svg += stand(H, 300, 860, 1.7, "<g transform=\"translate(0,100)\">" + K.props.lab({ liquid: "med", fire: true }) + "</g>");
    // the result board: six bottles on its top shelf, results chalked under them, the counter along the bottom
    const bx = 760, by = 150, bw = 640, bh = 470;
    svg += `<path d="M${bx + 60},${by + bh} L${bx + 40},${780} M${bx + bw - 60},${by + bh} L${bx + bw - 40},${780}" stroke="${C.rust}" stroke-width="14"/>` +
      `<rect x="${bx - 14}" y="${by - 14}" width="${bw + 28}" height="${bh + 28}" fill="${C.tan}" stroke="${C.line}" stroke-width="5"/>` +
      `<rect x="${bx}" y="${by}" width="${bw}" height="${bh}" fill="${C.slate}" stroke="${C.line}" stroke-width="4"/>` +
      `<rect x="${bx - 20}" y="${by + 128}" width="${bw + 40}" height="14" fill="${C.rust}" stroke="${C.line}" stroke-width="4"/>`;
    const chalk = "#EDE8D8";
    for (let i = 0; i < 6; i++) {
      const x = bx + 60 + i * 104;
      svg += H.at(x, by + 128, 1.1, K.props.pillBottle({ face: i < 2 ? "grin" : "flat", label: String(i + 1), pills: false }));
      if (i < 2) svg += H.tick(x - 34 + i * 18, 380, i === 1 ? 58 : 66, chalk);
    }
    // the chalk counter on a slate plaque hung over the board
    svg += `<path d="M${bx + bw / 2 - 120},${by - 14} L${bx + bw / 2 - 90},${by - 34} M${bx + bw / 2 + 120},${by - 14} L${bx + bw / 2 + 90},${by - 34}" stroke="${C.line}" stroke-width="4"/>` +
      `<rect x="${bx + bw / 2 - 190}" y="${by - 128}" width="380" height="96" fill="${C.slate}" stroke="${C.tan}" stroke-width="10"/><rect x="${bx + bw / 2 - 196}" y="${by - 134}" width="392" height="108" fill="none" stroke="${C.line}" stroke-width="3"/>` +
      `<text x="${bx + bw / 2}" y="${by - 50}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="74" fill="${chalk}" opacity="0.94">48,000</text>`;
    // the germs
    [[560, 260, 1.5, -12], [1500, 220, 1.3, 20], [1640, 470, 1.6, 0], [640, 520, 1.2, 30], [1460, 600, 1.1, -20], [480, 380, 1.0, 10]].forEach(([x, y, s, r]) => {
      svg += H.at(x, y, s, K.props.germ({ mood: "grin" }), r);
    });
    // the helpers, running in circles with their arms up, behind her at the right
    svg += stand(H, 1560, 900, 2.3, K.person({ tone: 1, outfit: "labcoat", hair: 2, mood: "worried", look: "left", arms: [[-160, -175], [160, 175]] }));
    svg += stand(H, 1760, 890, 2.2, K.person({ tone: 2, outfit: "labcoat", hair: 1, mood: "worried", look: "right", arms: [[-150, -170], [150, 170]] }));
    svg += `<path d="M1470,940 q90,30 180,0 M1680,930 q90,30 170,0" fill="none" stroke="${C.line}" stroke-width="4" stroke-dasharray="14 12"/>`;
    // the Scientist, on fire, running past the board chalking a tick under bottle 2
    const so = K.castOpts("scientist", { look: "left", arms: [[-174, -171], [60, 80]], holdR: "clipboard", holdL: null });
    const sk = 3.4, sxp = 1135, sfeet = 1020, sh = K.rig(so).hand[0];
    svg += stand(H, sxp, sfeet, sk, K.person(so) + K.fireOn(so));
    svg += `<circle cx="${f1(sxp + sh[0] * sk)}" cy="${f1(sfeet - 100 * sk + sh[1] * sk)}" r="8" fill="${chalk}" stroke="${C.line}" stroke-width="2"/>`;
    svg += `<path d="M1250,700 h120 M1260,760 h150 M1270,820 h110" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/>`;
    return { svg, alt: "The pandemic ward: the Scientist runs past the calm result board on fire, chalking a tick under bottle 2; six pill bottles on its shelf, the first two grinning, the chalked count 48,000 below; two helpers run in circles with their arms up, germs everywhere, the lab bench boiling over, the alarm light spinning." };
  },

  "postwar-boom"(H, id) {
    const { K, C } = H;
    const sky = K.mix(C.cream, FIELD, 0.35);
    let svg = `<rect width="1920" height="1080" fill="${sky}"/>`;
    // the top of today's stack, 30.6 war bills lying flat, running out of the bottom of the frame
    const sx = 520, sw = 560, sh = 34;
    const jit = [0, 8, -6, 10, -10, 4, -4, 12, -8, 6, -2, 8];
    for (let i = 0; i < 12; i++) svg += slab(H, sx + jit[i], 700 + i * sh, sw, sh);
    // the Weapons Maker, sitting on the stack top, his missile hugged in his left arm; his right hand is down at the
    // stack's edge, just done flicking the 1% slice off it like a crumb
    const wo = K.castOpts("weaponsMaker", { look: "right", mood: "smug", arms: [[32, 84], [25, 45]], holdL: "missile",
      build: { hs: 0.66, tw: 1.15, arms: 1.35, legs: 0.78, neck: 0, hand: 1.35, legPose: [[80, 5], [90, 10]] } });
    const wr = K.rig(wo), k = 3.1, wx = 800, wy = 700 - wr.hipY * k - 4;
    svg += H.at(wx, wy, k, K.person(wo));
    // the flick: snap marks at his fingertips
    const fx = wx + wr.hand[1][0] * k + 28, fy = wy + wr.hand[1][1] * k + 22;
    svg += [[-40, 26], [-10, 34], [22, 28]].map(([a, r]) => { const t = (a * Math.PI) / 180; return `<path d="M${f1(fx + 14 * Math.cos(t))},${f1(fy + 14 * Math.sin(t) - 10)} l${f1(r * Math.cos(t))},${f1(r * Math.sin(t))}" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/>`; }).join("");
    // the 1% slice, a third of a bill thick, tumbling away off the stack's edge toward the funnel far below, spin
    // marks at its ends
    const tx = 1320, ty = 650, tl = 440, tt = 18;
    svg += `<g transform="translate(${tx},${ty}) rotate(22)">` + slab(H, -tl / 2, -tt / 2, tl, tt) +
      `<path d="M${-tl / 2 - 18},-34 q-30,34 0,68 M${tl / 2 + 18},34 q30,-34 0,-68" fill="none" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/></g>`;
    svg += H.big(1560, 400, 210, "1%", "middle", C.ink);
    return { svg, alt: "High up on today's stack of war bills: the Weapons Maker sits on top hugging his smiling missile in one arm and, with his other hand, has just flicked the 1% slice off the stack like a crumb; it tumbles away to the right toward the funnel below; a big 1% beside it." };
  },

  "empty-podium"(H, id) {
    const { K, C } = H;
    let svg = `<rect width="1920" height="1080" fill="${K.mix(C.cream, FIELD, 0.4)}"/><rect y="820" width="1920" height="260" fill="${FIELD}"/><path d="M0,820 H1920" stroke="${C.line}" stroke-width="4"/>`;
    // the factory (no sign), its door rolled up, the hopper on its left side
    const fx = 1260, fk = 1.55, fg = 900;
    svg += H.at(fx, fg, fk, K.props.factory({ label: "", smoke: true }));
    // the hopper, bolted high on the factory's left wall: a funnel mouth with a chute into the brick
    const hx = fx - 216 * fk - 10, hy = fg - 250 * fk;
    svg += `<rect x="${hx - 6}" y="${hy + 20}" width="60" height="44" fill="${C.slate}" stroke="${C.line}" stroke-width="5"/>` +
      `<path d="M${hx - 130},${hy - 70} L${hx + 30},${hy - 70} L${hx + 10},${hy + 34} L${hx - 70},${hy + 34} Z" fill="${C.peri}" stroke="${C.line}" stroke-width="5" stroke-linejoin="round"/>` +
      `<path d="M${hx - 124},${hy - 58} H${hx + 26}" stroke="${C.orange}" stroke-width="4"/>` +
      `<path d="M${hx - 96},${hy - 72} q36,-34 74,0" fill="${C.rust}" stroke="${C.line}" stroke-width="3"/><path d="M${hx - 40},${hy - 96} l10,-26 l12,4 l-6,24" fill="${C.rust}" stroke="${C.line}" stroke-width="3"/>`;
    // the new missile in the stolen coat, popped out in front of the door, collar up round its smug face, snug
    const mk = 2.2, mx = fx, my = fg + 4;
    const coat = `<path d="M-31,-70 L31,-70 L38,-20 L4,-14 L0,-40 L-4,-14 L-38,-20 Z" fill="${C.rust}" stroke="${C.line}" stroke-width="3.4" stroke-linejoin="miter"/>` +
      `<path d="M-31,-70 L-36,-92 L-14,-74 Z M31,-70 L36,-92 L14,-74 Z" fill="${C.tan}" stroke="${C.line}" stroke-width="3" stroke-linejoin="miter"/>` +
      `<circle cx="-5" cy="-56" r="2.8" fill="${C.yellow}" stroke="${C.line}" stroke-width="1.4"/><circle cx="-5" cy="-42" r="2.8" fill="${C.yellow}" stroke="${C.line}" stroke-width="1.4"/><circle cx="-5" cy="-28" r="2.8" fill="${C.yellow}" stroke="${C.line}" stroke-width="1.4"/>` +
      `<path d="M-30,-64 L-44,-46 L10,-50 L12,-40 L-42,-36 L-40,-56 Z" fill="${C.rust}" stroke="${C.line}" stroke-width="3" stroke-linejoin="miter"/>` +
      `<path d="M30,-64 L44,-46 L-10,-46 L-10,-38 L42,-36 L40,-56 Z" fill="${C.rust}" stroke="${C.line}" stroke-width="3" stroke-linejoin="miter"/>`;
    svg += H.at(mx, my, mk, K.props.missile({ mood: "smug", arms: "none" }) + coat);
    svg += `<path d="M${mx - 120},${my - 260} l-24,-18 M${mx + 120},${my - 260} l24,-18 M${mx - 134},${my - 200} l-30,-4 M${mx + 134},${my - 200} l30,-4" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/>`;
    // the thin human with the empty spoon, and the shivering human in polka-dot underwear, under the hopper
    const thin = { tone: 1, outfit: "shirt", color: 1, hair: 0, seed: 3, mood: "sad", look: "right", arms: [[10, 4], [40, 120]], build: { tw: 0.7, legs: 1.2, neck: 1.4 } };
    const tk = 2.3, tx = 470, tf = 960;
    const tr = K.rig(thin);
    svg += stand(H, tx, tf, tk, K.person(thin) +
      `<g transform="translate(${f1(tr.hand[1][0])},${f1(tr.hand[1][1])}) rotate(-30)"><path d="M0,0 L22,0" stroke="#B9B5AE" stroke-width="3"/><ellipse cx="28" cy="0" rx="7" ry="4.5" fill="#D8D4CC" stroke="${C.line}" stroke-width="1.6"/></g>`);
    const cold = { tone: 0, outfit: "shirt", colorHex: "#F3ECD0", hair: 2, hat: "fedora", seed: 5, mood: "worried", look: "right", arms: [[30, -40], [-30, 40]], build: { tw: 1.05, legs: 0.9 } };
    const ck = 2.3, cx = 700, cf = 965, cr = K.rig(cold);
    const dots = [[-12, -10], [6, -16], [-4, 2], [12, 4], [-14, 14], [4, 16], [14, 22], [-6, 26]].map(([dx, dy]) => `<circle cx="${dx}" cy="${f1((cr.shoulder[0][1] + cr.hipY) / 2 + dy)}" r="2.6" fill="${C.war}"/>`).join("");
    const ice = `<path d="M${f1(cr.mouth[0] + 10)},${f1(cr.mouth[1] - 8)} l7,0 l-3,20 Z" fill="#DDEFF2" stroke="${C.line}" stroke-width="1.6"/>`;
    const shiver = `<path d="M-44,-20 l-6,6 l6,6 l-6,6 M44,-20 l6,6 l-6,6 l6,6" fill="none" stroke="${C.line}" stroke-width="2.4"/>`;
    svg += stand(H, cx, cf, ck, K.person(cold) + dots + ice + shiver);
    // the Lobbyist tiptoeing off at the left edge
    svg += stand(H, 170, 950, 2.4, K.cast("lobbyist", { look: "left" }));
    return { svg, alt: "The town square during the hold: a new missile wearing the stolen winter coat, buttoned up and smug, pops out of the factory door under its missile chimneys; beside the hopper a thin human holds an empty spoon and a human in polka-dot underwear and a fedora shivers with an icicle on his nose; the Lobbyist tiptoes off at the left." };
  },

  "sixty-five-years"(H, id) {
    const { K, C } = H;
    const forms = tower(H, 1330, 270, true);
    const k = 2.7, feet = 1066;
    const so = K.castOpts("politician", { skeleton: true, look: "right", arms: [[-10, -4], [42, 69]] }), sr = K.rig(so);
    const tie = `<path d="M${sr.neck[0] - 3},${f1(sr.neck[1] + 4)} h6 l9,40 l-12,11 l-12,-11 Z" fill="${C.war}" stroke="${C.line}" stroke-width="2.4" stroke-linejoin="miter"/>`;
    const bones = stand(H, 150, feet, k, K.person(so) + tie);
    const btn = H.at(372, feet, k, K.props.yesButton({ label: "WAR", color: C.war }));
    const webs = cobweb(1195, 780, 190, 95, 180) + cobweb(1465, 200, 150, 0, 90) + cobweb(372 - 50 * k, feet - 104 * k, 120, -90, 0) +
      cobweb(110, 760, 130, -60, 30) + cobweb(1010, 790, 120, -170, -100);
    const svg = H.host("sideeye-closed", "arms-crossed", caseFile(H, true) + cobweb(...caseCorner(H), 70, 90, 180) + forms + bones + btn + webs);
    return { svg, alt: "The studio set 65 years later: Wishonia side-eyes the camera with her arms folded; the tower of forms beside her is gray with dust and cobwebs, and so is the case file on her lectern; on her other side the Politician is a grinning skeleton with his finger still on the dusty, cobwebbed WAR button." };
  },
};
