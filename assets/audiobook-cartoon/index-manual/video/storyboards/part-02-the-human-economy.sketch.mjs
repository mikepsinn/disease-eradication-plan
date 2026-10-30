// Sketches for storyboards/part-02-the-human-economy.md: each scene's key frame on a 1920 x 1080 frame (16:9),
// drawn with the production art at the positions of the built scenes in compositions/scenes/part-02/.
// Built into the review sheet by tools/storyboard-sheet.mjs.

const f = (n) => n.toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});

// A plate framing as KIT.camera places it: plate point (x, y) in the middle of the frame, at scale s.
const view = (x, y, s, inner) => `<g transform="translate(${f(960 - x * s)},${f(540 - y * s)}) scale(${s})">${inner}</g>`;
// A host shot's slow push in on her face (KIT.studio), k of the way along.
const push = (S, k, inner) => `<g transform="translate(${S.face[0]},${S.face[1]}) scale(${k}) translate(${-S.face[0]},${-S.face[1]})">${inner}</g>`;
const at = (x, y, k, inner) => `<g transform="translate(${f(x)},${f(y)}) scale(${k})">${inner}</g>`;

// The loaf of bread from money-loop and the-toll, about 60 x 30 around (0, 0).
function loaf(ink) {
  return `<path d="M-30,6 Q-32,-14 -10,-16 Q8,-20 24,-12 Q34,-4 30,8 Q0,14 -30,6 Z" fill="#D49A4E" stroke="${ink}" stroke-width="3.2" stroke-linejoin="round"/>` +
    `<path d="M-16,-8 l8,-6 M-2,-9 l8,-6 M12,-8 l8,-6" stroke="#F3DFB0" stroke-width="3" stroke-linecap="round"/>`;
}
// The family of the loop (money-loop and the-toll use the same options): x on the plate and scale.
const FAM = [
  { o: { tone: 1, outfit: "shirt", color: 1, hair: 0, seed: 3 }, x: 380, k: 1.5 },
  { o: { tone: 1, outfit: "dress", color: 3, hair: 1, seed: 2 }, x: 500, k: 1.5 },
  { o: { tone: 1, outfit: "shirt", color: 0, hair: 0, seed: 5, build: { hs: 1.18, legs: 0.8 } }, x: 615, k: 1.08 },
];

export default {
  "title-card"(H, fid) {
    const { K, C } = H;
    // KIT.titleScene's atomic card (16:9): the emblem at (960, 300), rx 200, ry 62, papers at 0.62, as at t 1.9 s
    const cx = 960, cy = 300, rx = 200, ry = 62, TILT = [0, 60, -60], t = 1.86;
    const orbits = TILT.map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = TILT.map((a, i) => {
      const th = i * 2.1 + t * 2.4, ar = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return at(cx + ex * Math.cos(ar) - ey * Math.sin(ar), cy + ex * Math.sin(ar) + ey * Math.cos(ar) - 6, 0.62, K.money("war", i % 2));
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    // the heading: Fraunces, cream with a cream outline and a navy drop shadow; "THE HUMAN" at half the size of
    // "ECONOMY" (200), the lines' cap heights at y 567 to 637 and 693 to 833 (the card's measured layout)
    const word = (y, s, text) => {
      const t0 = (dx, dy, extra) => `<text x="${960 + dx}" y="${y + dy}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${s}" ${extra}>${H.esc(text)}</text>`;
      return t0(0.04 * s, 0.053 * s, `fill="${C.ink}"`) + t0(0, 0, `fill="${C.cream}" stroke="${C.cream}" stroke-width="${f(0.044 * s)}" stroke-linejoin="round" style="paint-order:stroke"`);
    };
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus + word(637, 100, "THE HUMAN") + word(833, 200, "ECONOMY");
    return { svg, alt: "The period title card: on plain navy, the film's atom with three little green war-seal papers running round its orbits on stick legs, and under it THE HUMAN ECONOMY in big cream letters." };
  },

  "host-opens"(H, fid) {
    const { K } = H, S = K.STUDIO, p = S.pool;
    // on "magnificent:": arms wide, the spotlight pool swelled a notch (1.12), the push about 1.06 along
    const wall = K.studioWall().replace('<g class="pool">', `<g class="pool" transform="translate(${p[0]},${p[1]}) scale(1.12) translate(${-p[0]},${-p[1]})">`);
    const svg = push(S, 1.055, wall + H.wish(S.wish.x, S.wish.y, S.wish.w, "excited-ee", "wide-gesture") + K.lectern());
    return { svg, alt: "Wishonia at her navy lectern with the atom on its front throws her arms wide, excited, in front of the mustard studio wall, its spotlight pool swelled behind her." };
  },

  "money-loop"(H, fid) {
    const { K } = H, S = 1.5;
    // the plate (money-loop.html): the stadium road, the rubble of the house at (560, 520), the mushroom cloud over
    // it, and the family on the road (feet y 652), charred. The framing: between the "boom" and "town" views.
    const HL = 850, RR = 640, RW = 160;
    const d = `M${-HL},${-RR} H${HL} A${RR},${RR} 0 0,1 ${HL},${RR} H${-HL} A${RR},${RR} 0 0,1 ${-HL},${-RR} Z`;
    const road = `<path d="${d}" fill="none" stroke="#B09363" stroke-width="${RW + 14}"/><path d="${d}" fill="none" stroke="#EEE3C4" stroke-width="${RW}"/>` +
      `<path d="${d}" fill="none" stroke="#C7AB78" stroke-width="7" stroke-dasharray="46 54"/>`;
    const rubble = at(560, 520, 1, `<g transform="scale(${S * 1.06},${S * 0.16})">${K.burn(K.props.house({ variant: 2, smoke: false }))}</g>`);
    const nuke = at(560, 520, 1.25, K.nuke());
    const fam = FAM.map((m) => at(m.x, 652 - 100 * m.k, m.k, K.person(copy(m.o, { charred: true, arms: [[14, 6], [-14, -6]] })))).join("");
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="#C8B07B"/>` + view(575, 296, 0.96, road + rubble + nuke + fam);
    return { svg, alt: "On the plate's road, the mushroom cloud stands over the flattened house, and in front of it the family of three stands charred black and smoking, hair straight up, only their white eyes showing." };
  },

  "the-toll"(H, fid) {
    const { K, C } = H, ink = C.line;
    // the-toll.html's wide view (0, -320, scale 1) during the HOLD: drained to gray, the rows of headstones up to
    // the horizon (y -530), the family as skeletons holding their loaves, the number in the sky
    const HZ = 530, STONE = "#E6E0D2", SHADE = "#A9AEB8", halfW = 960 + 80;
    const DK = [];
    for (let dd = 480; dd >= 16; dd *= 0.8) DK.push(dd);
    const rows = DK.map((dk) => {
      const base = -HZ + dk, sc = dk / HZ, w = 104 * sc, h = 160 * sc, step = 200 * sc;
      let body = "", side = "";
      for (let j = -Math.ceil(halfW / step); j <= Math.ceil(halfW / step); j++) {
        const x = j * step, l = x - w / 2, r = x + w / 2, top = base - h + w / 2;
        body += `M${f(l)},${f(base)} V${f(top)} A${f(w / 2)},${f(w / 2)} 0 0,1 ${f(r)},${f(top)} V${f(base)} Z `;
        side += `M${f(r - w * 0.24)},${f(base)} V${f(top - w * 0.06)} A${f(w / 2)},${f(w / 2)} 0 0,1 ${f(r)},${f(top)} V${f(base)} Z `;
      }
      const stroke = dk > 120 ? ` stroke="${ink}" stroke-width="${f(Math.max(1.2, 4 * sc))}" stroke-linejoin="round"` : "";
      const mound = dk > 120 ? `<path d="M${f(-halfW)},${f(base)} H${f(halfW)}" stroke="#8E7A55" stroke-width="${f(6 * sc)}" opacity="0.5"/>` : "";
      return mound + `<path d="${body}" fill="${STONE}"${stroke}/><path d="${side}" fill="${SHADE}"/>`;
    }).reverse().join("");
    const fam = FAM.map((m, i) => {
      const x = [-150, 0, 130][i], alive = copy(m.o, { charred: true, look: "left", arms: [[-22, -112], [-8, -106]] }), R = K.rig(alive);
      const held = at((R.hand[0][0] + R.hand[1][0]) / 2 - 4, (R.hand[0][1] + R.hand[1][1]) / 2 - 4, 0.62, loaf(ink));
      return at(x, -100 * m.k, m.k, K.person(copy(alive, { charred: false, skeleton: true })) + held);
    }).join("");
    const plate = `<rect x="-4000" y="${-HZ - 4000}" width="8000" height="4000" fill="#DCD8CE"/><path d="M-4000,${-HZ} H4000" stroke="#8E7A55" stroke-width="3" opacity="0.6"/>` + rows + fam;
    const svg = `<rect x="-100" y="-100" width="2120" height="1280" fill="#A9A69B"/>` + view(0, -320, 1.0, plate) +
      `<text x="960" y="200" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="172" letter-spacing="4" fill="${C.navy}">310,000,000</text>`;
    return { svg, alt: "A gray field of headstones running in rows to the horizon; in front, three grinning skeletons each hold a loaf of bread, the only color left; 310,000,000 stands in the sky." };
  },

  "host-closes"(H, fid) {
    const { K, C } = H, S = K.STUDIO, ink = C.line;
    // host-closes.html after "probably": the hungry human (MAN at x 1390, feet y 1066, scale 3.3) chewing, the
    // sandwich at his mouth with the bite out of it; Wishonia smirking (the "but" state); the push about 1.074
    const MAN = { kind: "shirt", head: "long", hairStyle: "short", tone: 2, color: 2, look: "left", build: { tw: 0.72, legs: 1.18, th: 1.12, neck: 1.6, hs: 0.95, nose: 1.5 } };
    const WALK = copy(MAN, { mood: "worried", arms: [[8, 4], [-8, -4]] }), CHEW = copy(MAN, { mood: "smile", arms: [[-30, -160], [-14, -158]] });
    const k = 3.3, mx = 1390, my = 1066 - 100 * k - 4, R0 = K.rig(WALK), RC = K.rig(CHEW);
    const pocket = (x, s) => `<path d="M${f(x)},${f(R0.hipY - 4)} l${13 * s},0 l${-3 * s},15 l${-9 * s},-3 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="2.2" stroke-linejoin="round"/>`;
    const man = at(mx, my, k, K.person(CHEW) + pocket(R0.hip[0][0] - 9, -1) + pocket(R0.hip[1][0] + 9, 1));
    const bread = (y, h) => `<rect x="-32" y="${y}" width="64" height="${h}" rx="7" fill="#E9C07A" stroke="${ink}" stroke-width="2.6"/>`;
    const body = bread(10, 11) + `<path d="M-33,8 q6,-6 11,0 q6,-6 11,0 q6,-6 11,0 q6,-6 11,0 q6,-6 11,0 q6,-6 11,0 v4 h-66 Z" fill="#9DB25A" stroke="${ink}" stroke-width="2"/>` +
      `<rect x="-31" y="0" width="62" height="7" fill="${C.war}" stroke="${ink}" stroke-width="2"/>` + bread(-10, 10) +
      `<rect x="-31" y="-17" width="62" height="7" fill="#D99A8F" stroke="${ink}" stroke-width="2"/><path d="M-31,-11 H31 V-8 l-5,7 l-4,-7 H-31 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="1.6"/>` + bread(-29, 12);
    const pick = `<path d="M4,-29 L1,-50" stroke="${C.tan}" stroke-width="2.4"/><circle cx="1" cy="-52" r="5.5" fill="#7E8C3A" stroke="${ink}" stroke-width="2"/><circle cx="1" cy="-52" r="2" fill="${C.war}"/>`;
    const bite = `<defs><clipPath id="${fid}-bite"><path d="M-60,-80 H6 V-31 Q16,-31 18,-22 Q7,-19 11,-10 Q3,-5 10,3 Q4,9 13,15 Q22,17 26,22 H60 V60 H-60 Z"/></clipPath></defs>`;
    const ks = k * 0.74, hx = mx + k * (RC.hand[0][0] + RC.hand[1][0]) / 2, hy = my + k * (RC.hand[0][1] + RC.hand[1][1]) / 2 - 14 * ks;
    const sand = at(hx, hy, ks, bite + `<g clip-path="url(#${fid}-bite)">${body + pick}</g>`);
    const svg = push(S, 1.074, H.host("smirk-closed", "idle", man + sand));
    return { svg, alt: "Wishonia smirks at her lectern while, beside it, a skinny human with his pockets turned out bites into a tall club sandwich with a toothpick and olive, a notch already out of its side." };
  },
};
