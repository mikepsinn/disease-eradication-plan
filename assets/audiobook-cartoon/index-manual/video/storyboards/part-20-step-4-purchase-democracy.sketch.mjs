// Sketches for storyboards/part-20-step-4-purchase-democracy.md: each scene's key moment on a 1920 x 1080 frame,
// drawn with the production art (H.K: kit.js, film.js and the props library). The film look: host shots are the
// studio set (H.host, the guest on the free wall at her right); a plate frame is one framing of an illustrated
// plate as the camera sees it, on Part 2's plain tan field. 16:9 only, no captions.

const GROUND = "#C8B07B", BOARDS = "#B09363", BOARD_LINE = "#9C8052", BONE = "#F1EAD6", WHITE = "#FBF6E6";
const f = (n) => n.toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});

// A person standing with its feet at (x, feet), k times person size (KIT.person has its feet at y 100).
function man(H, o, x, feet, k, extra = "") {
  return H.at(f(x), f(feet - 100 * k), k, H.K.person(o) + extra);
}
// A point in a person's own units, on the canvas.
function pt(x, feet, k, p) {
  return [x + p[0] * k, feet - 100 * k + p[1] * k];
}
const field = (col = GROUND) => `<rect x="-20" y="-20" width="1960" height="1120" fill="${col}"/>`;
// The auction hall's floor: darker tan boards from y down.
function floor(C, y) {
  let seams = "";
  for (let x = -40; x < 1960; x += 150) seams += `<path d="M${x},${y + 8} L${x - 60},1080" stroke="${BOARD_LINE}" stroke-width="3" opacity="0.6"/>`;
  return `<rect x="-20" y="${y}" width="1960" height="${1100 - y}" fill="${BOARDS}"/><path d="M-20,${y} H1940" stroke="${C.line}" stroke-width="5"/>` + seams;
}
// Motion lines.
function lines(C, pts, w = 5) {
  return pts.map(([x1, y1, x2, y2]) => `<path d="M${f(x1)},${f(y1)} L${f(x2)},${f(y2)}" stroke="${C.line}" stroke-width="${w}" stroke-linecap="round"/>`).join("");
}
// Smoke / dust puffs.
function puff(x, y, r, col = "#F6F1E4", ink = "#112845") {
  return `<g fill="${col}" stroke="${ink}" stroke-width="3"><circle cx="${f(x)}" cy="${f(y)}" r="${f(r)}"/><circle cx="${f(x - r * 0.8)}" cy="${f(y + r * 0.3)}" r="${f(r * 0.7)}"/><circle cx="${f(x + r * 0.85)}" cy="${f(y + r * 0.25)}" r="${f(r * 0.75)}"/></g>`;
}
// The Weapons Maker's grinning baby missile (the cast's held "missile" prop), around (0, 0), about 74 long, nose
// to the right; look "up" turns its eyes up.
function baby(C, look) {
  const ink = C.line, py = look === "up" ? -1.6 : 0;
  const body = (d) => `<path d="${d}" fill="${ink}" stroke="${ink}" stroke-width="2.6" stroke-linejoin="miter"/><path d="${d}" fill="${C.war}"/>`;
  return `<g transform="rotate(-14)">` + body("M-34,-7 L14,-7 L30,0 L14,7 L-34,7 Z") + body("M-34,-7 L-44,-17 L-40,-7 Z") + body("M-34,7 L-44,17 L-40,7 Z") +
    `<path d="M14,-7 L30,0 L14,7 Z" fill="${C.cream}" stroke="${ink}" stroke-width="2"/><path d="M-4,2 Q2,6 8,2" fill="none" stroke="${ink}" stroke-width="1.8" stroke-linecap="round"/>` +
    `<circle cx="-2" cy="${-2.5 + py}" r="1.6" fill="${ink}"/><circle cx="6" cy="${-2.5 + py}" r="1.6" fill="${ink}"/></g>`;
}
// The coin-op Politician's slot plate (person units, under his tie): a bill slot and a ballot slot, each with a
// little red mailbox flag (up = empty), and the vending flap at his belt buckle. bill: "war" | "med" | null (a paper
// sticking out of the bill slot). lean: the person's lean (KIT.rig(o).lean), so the plate tilts with the torso.
function slots(C, R, o = {}) {
  const ink = C.line, y = R.hipY - 22, sc = o.s || 1.45;
  const flag = (x, up) => up
    ? `<path d="M${x},${y + 1} V${y - 13}" stroke="${ink}" stroke-width="1.6"/><path d="M${x},${y - 13} h7 v4.5 h-7 Z" fill="${C.war}" stroke="${ink}" stroke-width="1.2"/>`
    : `<path d="M${x},${y + 1} H${x + 11}" stroke="${ink}" stroke-width="1.6"/><path d="M${x + 7},${y + 1} v4.5 h4 v-4.5 Z" fill="${C.war}" stroke="${ink}" stroke-width="1.2"/>`;
  const bill = o.bill ? `<g transform="translate(-7.5,${y + 0.5}) rotate(-8)"><rect x="-6.5" y="-7.5" width="13" height="7" fill="${C.money}" stroke="${ink}" stroke-width="1"/>` +
    `<ellipse cx="0" cy="-4" rx="1.8" ry="2.2" fill="${C.cream}" stroke="${C.moneyDark}" stroke-width="0.6"/>${H_seal(C, o.bill, 4.2, -4, 1.6)}</g>` : "";
  return `<g transform="rotate(${f(R.lean)} 0 ${f(R.hipY)})"><g transform="translate(0,${f(y)}) scale(${sc}) translate(0,${f(-y)})">` +
    `<rect x="-15" y="${y - 3}" width="15.5" height="9" rx="1.5" fill="#C9CCD1" stroke="${ink}" stroke-width="1.4"/><rect x="-12.5" y="${y}" width="10.5" height="1.8" fill="${ink}"/>` +
    `<rect x="1.5" y="${y - 3}" width="13.5" height="9" rx="1" fill="${C.tan}" stroke="${ink}" stroke-width="1.4"/><rect x="4" y="${y}" width="8.5" height="1.8" fill="${ink}"/>` +
    flag(-17, o.flags) + flag(16, o.flags) + bill +
    `</g><rect x="-4" y="${R.hipY - 7}" width="8" height="5" fill="#C9CCD1" stroke="${ink}" stroke-width="1.2"/></g>`;
}
function H_seal(C, kind, x, y, r) {
  const mark = kind === "war"
    ? `<path d="M${x - r * 0.55},${y + r * 0.35} L${x + r * 0.35},${y - r * 0.55}" stroke="${C.cream}" stroke-width="${r * 0.4}"/>`
    : `<path d="M${x},${y - r * 0.55} V${y + r * 0.55} M${x - r * 0.55},${y} H${x + r * 0.55}" stroke="${C.cream}" stroke-width="${r * 0.36}"/>`;
  return `<circle cx="${x}" cy="${y}" r="${r}" fill="${C.moneyDark}"/>` + mark;
}
// The tattooed arm (Part 2's pay-window forearm, drawn big): a hairy brown forearm with a little war-red missile
// tattoo and a navy cuff, running up (-y) from a fist at (0, 0) whose fingers curl down over the front of
// whatever it grips (to y about 34). About 120 wide and 600 long.
function tattooArm(C) {
  const ink = C.line, SKIN = "#6F4B33";
  const P = (pts, col, w = 5) => `<path d="M${pts.map((p) => p.join(",")).join(" L")} Z" fill="${col}" stroke="${ink}" stroke-width="${w}" stroke-linejoin="miter"/>`;
  let hair = "";
  for (let y = -110; y > -500; y -= 38) {
    const e = 36 + ((-y - 40) / 520) * 12;
    hair += `<path d="M${f(-e + 4)},${y} l-12,-10 M${f(e - 4)},${y - 18} l12,-10 M${f(-e / 3)},${y - 9} l-7,-9 M${f(e / 3)},${y - 26} l7,-9" stroke="${ink}" stroke-width="2.6" stroke-linecap="round"/>`;
  }
  // the tattoo: a little missile along the arm, nose up, and a ribbon under it
  const tat = `<g transform="translate(0,-270)"><path d="M-9,40 L-9,-24 L0,-44 L9,-24 L9,40 Z" fill="${C.war}"/><path d="M-9,26 L-22,44 L-9,40 Z M9,26 L22,44 L9,40 Z" fill="${C.war}"/>` +
    `<path d="M-30,52 Q0,64 30,52 L26,64 Q0,74 -26,64 Z" fill="none" stroke="${C.war}" stroke-width="3.5"/></g>`;
  return P([[-36, -38], [36, -38], [50, -540], [-50, -540]], SKIN) + hair + tat +
    P([[-56, -500], [56, -500], [60, -620], [-60, -620]], C.navy) + `<path d="M-52,-512 H52" stroke="${C.orange}" stroke-width="4"/>` +
    // the fist: the back of the hand, the thumb round the side, four fingers curled over the front
    P([[-50, -44], [50, -44], [60, -6], [-60, -6]], SKIN) +
    P([[-60, -24], [-80, -2], [-72, 22], [-54, 12]], SKIN, 4.4) +
    [-45, -15, 15, 45].map((x) => P([[x - 15, -10], [x + 15, -10], [x + 13, 30], [x + 4, 36], [x - 6, 36], [x - 14, 28]], SKIN, 4.4)).join("") +
    `<path d="M-44,-30 l8,-8 M-12,-32 l8,-8 M20,-30 l8,-8" stroke="${ink}" stroke-width="2.4" stroke-linecap="round"/>`;
}
// A bidding paddle: a cream card with rounded corners on a stick, the stick's foot at (0, 0); w x h, optional
// lines of text. rot turns it about the foot.
function paddle(C, w, h, text = [], rot = 0, stick = 70) {
  const ink = C.line, top = -stick - h;
  const t = text.map((l, i) => `<text x="0" y="${f(top + h * (text.length === 1 ? 0.62 : 0.42 + i * 0.36))}" text-anchor="middle" font-family="${l.font || "Fraunces"}" font-weight="${l.font ? 600 : 900}" font-size="${l.size}" fill="${ink}">${l.text}</text>`).join("");
  return `<g transform="rotate(${rot})"><path d="M0,0 V${-stick - 4}" stroke="${ink}" stroke-width="${f(Math.max(7, w * 0.07))}" stroke-linecap="round"/><path d="M0,0 V${-stick - 4}" stroke="${C.tan}" stroke-width="${f(Math.max(3.5, w * 0.04))}" stroke-linecap="round"/>` +
    `<rect x="${f(-w / 2)}" y="${f(top)}" width="${w}" height="${h}" rx="${f(Math.min(w, h) * 0.16)}" fill="${C.cream}" stroke="${ink}" stroke-width="${f(Math.max(4, w * 0.025))}"/>` +
    `<rect x="${f(-w / 2 + w * 0.06)}" y="${f(top + h * 0.08)}" width="${f(w * 0.88)}" height="${f(h * 0.84)}" rx="${f(Math.min(w, h) * 0.1)}" fill="none" stroke="${C.orange}" stroke-width="${f(Math.max(2, w * 0.012))}"/>` + t + "</g>";
}
// The Super PAC, as Part 5's step-4-super-pac sketch draws it: a rust canvas backpack with a darker rust top flap,
// navy straps for arms, a cream SUPER PAC patch with an orange inner rule on its front pocket, and a war-red cape
// ("fly": streaming to the left; "trail": streaming out past its bottom; otherwise billowing). No mask. Around its
// bottom middle (0, 0), 262 tall at k = 1.
function superPac(C, k, cape = "fly") {
  const ink = C.line, SEAM = "#A35A3A", FLAP = "#6E3622";
  const P = (pts, col, w = 4.4) => { const d = "M" + pts.map((p) => p.join(",")).join(" L") + " Z"; return `<path d="${d}" fill="${ink}" stroke="${ink}" stroke-width="${w}" stroke-linejoin="miter"/><path d="${d}" fill="${col}"/>`; };
  const capeD = cape === "fly"
    ? [[-96, -258], [96, -258], [40, -210], [-160, -200], [-290, -236], [-360, -196], [-280, -170], [-350, -130], [-250, -128], [-300, -84], [-180, -110], [-100, -120]]
    : cape === "trail" // streaming out past its bottom (toward a flier's feet)
    ? [[-96, -258], [96, -258], [150, -100], [176, 70], [124, 44], [96, 150], [44, 96], [0, 210], [-40, 116], [-92, 160], [-122, 52], [-168, 76], [-150, -100]]
    : [[-96, -258], [96, -258], [210, -230], [270, -170], [236, -150], [262, -100], [214, -96], [226, -40], [150, -40], [120, 0], [-40, 6], [-120, -4], [-130, -60]];
  const arm = (sx) => `<path d="M${sx * 104},-200 L${sx * 150},-136 L${sx * 112},-92" fill="none" stroke="${ink}" stroke-width="20" stroke-linejoin="round" stroke-linecap="round"/>` +
    `<path d="M${sx * 104},-200 L${sx * 150},-136 L${sx * 112},-92" fill="none" stroke="${C.navy}" stroke-width="14" stroke-linejoin="round" stroke-linecap="round"/>`;
  return `<g transform="scale(${k})">` + P(capeD, C.war) + arm(-1) + arm(1) +
    P([[-104, -248], [-92, -262], [92, -262], [104, -248], [114, -28], [102, -6], [-102, -6], [-114, -28]], C.rust) +
    `<path d="M-96,-20 L-102,-236 M96,-20 L102,-236" stroke="${SEAM}" stroke-width="4"/>` +
    P([[-92, -262], [92, -262], [98, -206], [0, -190], [-98, -206]], FLAP, 3.6) +
    P([[-84, -176], [84, -176], [88, -40], [-88, -40]], SEAM, 3.2) +
    `<rect x="-76" y="-150" width="152" height="56" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>` +
    `<rect x="-70" y="-144" width="140" height="44" fill="none" stroke="${C.orange}" stroke-width="2"/>` +
    `<text x="0" y="-112" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="25" letter-spacing="1.5" fill="${ink}">SUPER PAC</text></g>`;
}
// A running-track band along y (canvas): rust cinder with cream lane lines, w tall, from x0 to x1.
function track(C, y, w, x0 = -40, x1 = 1960) {
  let lanes = "";
  for (let i = 0; i <= 3; i++) lanes += `<path d="M${x0},${f(y + (i / 3) * w)} H${x1}" stroke="${C.cream}" stroke-width="5"/>`;
  return `<rect x="${x0}" y="${y}" width="${x1 - x0}" height="${w}" fill="#B8643F"/>` + lanes +
    `<path d="M${x0},${y - 6} H${x1} M${x0},${y + w + 6} H${x1}" stroke="${C.line}" stroke-width="4"/>`;
}

export default {
  "step-4-purchase-democracy-title"(H, fid) {
    const { K, C } = H;
    // KIT.titleScene's atomic card (16:9) on "Anyway": the emblem (smaller, four lines under it), STEP 4 stamped at
    // a tilt, PURCHASE on its line, the italic line; the tattooed arm, reaching down from the top of the card, lifts
    // DEMOCRACY off its line by the R, the D end drooping; one war bill flutters down into the gap.
    const cx = 960, cy = 170, rx = 150, ry = 46, TILT = [0, 60, -60], t = 1.2;
    const orbits = TILT.map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="4.5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = TILT.map((a, i) => {
      const th = i * 2.1 + t * 2.4, ar = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      return H.at(f(cx + ex * Math.cos(ar) - ey * Math.sin(ar)), f(cy + ex * Math.sin(ar) + ey * Math.cos(ar) - 5), 0.5, K.money("war", i % 2));
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="24" fill="${C.orange}" stroke="${C.cream}" stroke-width="4.5"/><circle cx="${cx - 7}" cy="${cy - 7}" r="6" fill="${C.yellow}"/>`;
    const word = (x, y, s, text, anchor) => {
      const t0 = (dx, dy, extra) => `<text x="${x + dx}" y="${y + dy}" text-anchor="${anchor}" font-family="Fraunces" font-weight="900" font-size="${s}" ${extra}>${H.esc(text)}</text>`;
      return t0(0.04 * s, 0.053 * s, `fill="${C.ink}"`) + t0(0, 0, `fill="${C.cream}" stroke="${C.cream}" stroke-width="${f(0.044 * s)}" stroke-linejoin="round" style="paint-order:stroke"`);
    };
    // the stamp line: a red plate with a cream border, tilted
    const stamp = `<g transform="translate(960,378) rotate(-6)"><rect x="-150" y="-52" width="300" height="104" rx="8" fill="${C.war}" stroke="${C.ink}" stroke-width="5"/>` +
      `<rect x="-138" y="-40" width="276" height="80" rx="5" fill="none" stroke="${C.cream}" stroke-width="5"/>` +
      `<text x="0" y="24" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="68" letter-spacing="6" fill="${C.cream}">STEP 4</text></g>`;
    const italic = `<text x="960" y="770" text-anchor="middle" font-family="Inter" font-style="italic" font-weight="700" font-size="62" fill="${C.cream}" stroke="${C.ink}" stroke-width="7" stroke-linejoin="round" style="paint-order:stroke">It's For Sale Anyway</text>`;
    // DEMOCRACY sat left-anchored at x 930 on baseline 640 (to x 1657); its R spans x 1345..1429, caps y 563..640.
    // The fist grips the top of the R (1387, 575) and has lifted it to (1400, 455), the word tipped 9 degrees, D down.
    const GRIP = [1387, 575], LIFT = [1400, 455];
    const lifted = H.at(LIFT[0], LIFT[1], 1, `<g transform="rotate(-9)">${word(930 - GRIP[0], 640 - GRIP[1], 110, "DEMOCRACY", "start")}</g>`) +
      H.at(LIFT[0], LIFT[1] - 8, 1, `<g transform="rotate(12)">${tattooArm(C)}</g>`);
    const bill = H.at(1235, 596, 1.25, K.money("war", 0), 16) + lines(C, [[1150, 560, 1170, 580], [1310, 552, 1290, 572]], 4);
    const lift = lines(C, [[1520, 552, 1520, 600], [1580, 540, 1580, 588], [1000, 636, 1000, 676], [1060, 624, 1060, 664]], 5);
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus + stamp +
      word(890, 640, 110, "PURCHASE", "end") + italic + bill + lift + lifted;
    return { svg, alt: "The period title card: the film's atom with its running war papers, a red STEP 4 stamp, PURCHASE in big cream letters and the italic line It's For Sale Anyway; a huge hairy fist with a missile tattoo on its forearm reaches down from the top of the card and lifts the word DEMOCRACY off its line like a plank, the D end drooping, while a single green war bill flutters down into the gap it left." };
  },

  "coin-op-politician"(H, fid) {
    const { K } = H;
    // after "jobs.": the Politician run down like a toy, folded forward at the waist, arms hanging, his grin gone
    // flat, both flags up beside his empty slots; Wishonia side-eyes him. Guest at x 1430, feet 1068, scale 3.3.
    const POL = K.castOpts("politician", { look: "left", mood: "flat", arms: [[14, 4], [6, -2]], holdR: null, build: { hs: 1, legs: 1.08, tw: 1.1, neck: 0.5, chin: 1.25, hunch: 30 } });
    const R = K.rig(POL), k = 3.3, X = 1430, FEET = 1068;
    const front = man(H, POL, X, FEET, k, slots(H.C, R, { flags: true })) +
      lines(H.C, [[1300, 520, 1270, 500], [1290, 560, 1255, 556]], 4);
    const svg = H.host("sideeye-closed", "idle", front);
    return { svg, alt: "Wishonia at her lectern side-eyes her guest: the toothy Politician, folded forward at the waist like a wind-up toy that has run down, arms hanging, a bill slot and a ballot slot on his belly with their little red flags standing up." };
  },

  "democracy-auction"(H, fid) {
    const { K, C } = H;
    // after "do),": close on the front of the crowd (the plate's "front" framing): the Weapons Maker a grinning
    // skeleton under his hard hat, the twins in his arms looking up at him, NOT THE ENEMY on its stick over him;
    // two Bidders behind him, chest lights blinking red, looking at him.
    const FL = 900;
    const WM = K.castOpts("weaponsMaker", { skeleton: true, look: "left", hold: null, arms: [[32, 84], [-32, -84]] });
    const R = K.rig(WM), k = 3.2, X = 700, FEET = 1010;
    const h = [pt(X, FEET, k, R.hand[0]), pt(X, FEET, k, R.hand[1])], mid = [(h[0][0] + h[1][0]) / 2, (h[0][1] + h[1][1]) / 2];
    // the twins lie one above the other in the crook of his arms, noses to the left, eyes up at him
    const twin = `<g transform="scale(-1,1)">${baby(C, "up")}</g>`;
    const twins = H.at(f(mid[0] - 4), f(mid[1] - 52), k * 0.78, twin) + H.at(f(mid[0] + 6), f(mid[1] - 4), k * 0.78, twin);
    const top = pt(X, FEET, k, R.top);
    const sign = H.at(f(top[0] + 6), f(top[1] - 30), 1.7, K.props.sign({ text: "NOT THE ENEMY", posts: 1, height: 64 }));
    const B1 = { tone: 0, outfit: "suit", color: 2, seed: 4, mood: "worried", look: "left", light: "red", arms: [[10, 30], [-8, -4]] };
    const B2 = { tone: 2, hair: 1, outfit: "dress", color: 3, seed: 9, mood: "worried", look: "left", light: "red", arms: [[10, 4], [-8, -4]] };
    const B3 = { tone: 1, outfit: "shirt", color: 0, seed: 13, mood: "flat", look: "left", light: "red", arms: [[10, 4], [-8, -4]] };
    // each bidder holds a blank paddle down at its side; red rays round the blinking chest light
    const blink = (o, x, feet, kk) => {
      const m = K.person(o).match(/class="chest-light" cx="([-\d.]+)" cy="([-\d.]+)"/), c = pt(x, feet, kk, [+m[1], +m[2]]);
      return [0, 1, 2, 3, 4, 5].map((i) => { const a = (i / 6) * Math.PI * 2 + 0.3; return `<path d="M${f(c[0] + 22 * Math.cos(a))},${f(c[1] + 22 * Math.sin(a))} L${f(c[0] + 34 * Math.cos(a))},${f(c[1] + 34 * Math.sin(a))}" stroke="${C.war}" stroke-width="5" stroke-linecap="round"/>`; }).join("");
    };
    const bid = (o, x, feet, kk) => { const r = K.rig(o), hh = pt(x, feet, kk, r.hand[1]); return man(H, o, x, feet, kk) + H.at(f(hh[0]), f(hh[1] - 6), kk * 0.9, paddle(C, 50, 40, [], 168, 34)) + blink(o, x, feet, kk); };
    const svg = field() + floor(C, FL) +
      bid(B3, 1740, 960, 2.4) + bid(B1, 1180, 990, 2.7) + bid(B2, 1480, 975, 2.6) +
      man(H, WM, X, FEET, k) + twins + sign +
      lines(C, [[top[0] - 150, top[1] - 120, top[0] - 120, top[1] - 90], [top[0] + 190, top[1] - 120, top[0] + 160, top[1] - 90]], 5);
    return { svg, alt: "Close on the front of the auction crowd: the Weapons Maker is now a grinning skeleton in his yellow hard hat, cigar in his teeth, cradling twin baby missiles that look up at him; a NOT THE ENEMY sign sticks up on a stick over his hat; the bidders behind him stare, their chest lights blinking red." };
  },

  "bidder-paddles"(H, fid) {
    const { K, C } = H;
    // on "cycle).": the crowd framing pulled back: the skeleton at the front (left) under his tower of eight paddles,
    // as tall as YOU's card and tipping over onto him; YOU at the back (right) under his barn-door paddle; the
    // Bidders between, holding out their empty hands. Floor at y 790.
    const FL = 790;
    const WM = K.castOpts("weaponsMaker", { skeleton: true, look: "right", hold: null, arms: [[150, 172], [32, 84]] });
    const R = K.rig(WM), k = 1.9, X = 470, FEET = 900;
    const hand = pt(X, FEET, k, R.hand[0]);
    // the tower: eight paddles, one on another, a column bending over to the left as it falls
    let tower = "", px = hand[0] + 6, py = hand[1] + 8, ang = 0;
    for (let i = 0; i < 8; i++) {
      tower += H.at(f(px), f(py), 1, paddle(C, 104, 76, i === 0 ? [{ text: "$198 MILLION", size: 15 }, { text: "/ YEAR", size: 15, font: "Oswald" }] : [], ang, 26));
      const r = (ang * Math.PI) / 180, d = 102;
      px += Math.sin(r) * d; py -= Math.cos(r) * d; ang -= 2.2 + i * 1.6;
    }
    const twin = `<g transform="scale(-1,1)">${baby(C, "up")}</g>`;
    const twins = H.at(f(X + 4), f(FEET - 142), k * 0.8, twin) + H.at(f(X + 10), f(FEET - 110), k * 0.8, twin);
    const YOU = { tone: 2, outfit: "suit", hat: "bowler", look: "left", mood: "smug", arms: [[-160, -178], [-10, -4]] };
    const RY = K.rig(YOU), ky = 1.75, YX = 1540, YF = 860, yh = pt(YX, YF, ky, RY.hand[0]);
    const big = H.at(f(yh[0]), f(yh[1] + 10), 1, paddle(C, 440, 320, [{ text: "$1 BILLION", size: 70 }, { text: "ONE TIME", size: 48, font: "Oswald" }], 0, 230));
    const shade = `<path d="M${f(yh[0] - 220)},${FL} L${f(yh[0] - 640)},${FL + 150} H${f(yh[0] + 90)} L${f(yh[0] + 220)},${FL} Z" fill="${C.line}" opacity="0.12"/>`;
    const B = [
      [{ tone: 0, outfit: "suit", color: 2, seed: 4 }, 800, 880, 1.7],
      [{ tone: 2, hair: 1, outfit: "dress", color: 3, seed: 9 }, 990, 868, 1.65],
      [{ tone: 1, outfit: "shirt", color: 0, seed: 13 }, 1170, 876, 1.7],
    ].map(([o, x, ft, kk]) => man(H, copy(o, { mood: "worried", look: "left", arms: [[-40, -100], [40, 100]] }), x, ft, kk)).join("");
    const REAPER = H.at(1790, 856 - 100 * 1.6, 1.6, K.reaper());
    const svg = field() + floor(C, FL) + shade + REAPER + B + man(H, YOU, YX, YF, ky) + big +
      man(H, WM, X, FEET, k) + twins + tower +
      lines(C, [[120, 150, 80, 200], [180, 110, 150, 165], [250, 90, 235, 150]], 5);
    return { svg, alt: "The auction crowd pulled back: at the front, the Weapons Maker's skeleton holds up his $198 MILLION / YEAR paddle with seven more paddles stacked on top of it, the tower as tall as YOU's card and tipping over onto him; at the back, YOU in his bowler holds up a paddle the size of a barn door, $1 BILLION / ONE TIME, beside the Grim Reaper; the bidders between them hold out their empty hands." };
  },

  "corrupt-the-corruption"(H, fid) {
    const { K, C } = H;
    // after "corruption." (second): the Politician in a teal tie, the CLEARANCE tag still swinging on it, a medicine
    // paper in his bill slot; Wishonia smirks, hands on hips.
    const POL = K.castOpts("politician", { look: "left", tieColor: C.med, arms: [[-8, -3], [150, 172]] });
    const R = K.rig(POL), k = 3.3, X = 1430, FEET = 1068;
    const tag = H.at(8, f(R.hy + 44), 0.34, K.props.priceTag({ text: "CLEARANCE", angle: 14 }));
    const front = man(H, POL, X, FEET, k, slots(C, R, { flags: false, bill: "med" }) + tag) +
      lines(C, [[1600, 735, 1626, 760], [1650, 700, 1680, 712]], 4);
    const svg = H.host("smirk-smile", "hands-hips", front);
    return { svg, alt: "Wishonia smirks at the camera, hands on hips; beside her the Politician grins every tooth in a new teal tie with a CLEARANCE price tag still swinging from it, and a medicine paper sticking out of the bill slot on his belly." };
  },

  "super-pac-rewards"(H, fid) {
    const { K, C } = H;
    // on "rewarded.": the near straight: the Politician rocketing right a foot off the track, flying flat out, the
    // Super PAC strapped to his back and firing like a jet pack, a flame and a spray of medicine papers behind him;
    // the YES button still bouncing at the trackside behind him.
    const TY = 720, TW = 220, ink = C.line;
    const POL = K.castOpts("politician", { look: "right", tieColor: C.med, mood: "grin", arms: [[178, 184], [170, 178]], holdR: null, build: { hs: 1, legs: 1.08, tw: 1.1, neck: 0.5, chin: 1.25, legPose: [[-4, -16], [10, -6]] } });
    const R = K.rig(POL), k = 2.35;
    // his body, in his own units, turned 78 degrees about the hip so he flies head first to the right, arms out ahead
    const pac = H.at(-30, f(R.hipY - 4), 0.21, superPac(C, 1, "trail"));
    const flame = H.at(-30, f(R.hipY - 2), 1.05, `<g transform="rotate(180)">${K.flames(0, 0, 1)}</g>`);
    const straps = `<path d="M${f(R.shoulder[0][0] + 6)},${f(R.shoulder[0][1] - 2)} L${f(R.hip[1][0] + 4)},${f(R.hipY - 4)} M${f(R.shoulder[1][0] - 8)},${f(R.shoulder[1][1] - 2)} L${f(R.hip[0][0] - 2)},${f(R.hipY - 6)}" stroke="${ink}" stroke-width="5.5"/>` +
      `<path d="M${f(R.shoulder[0][0] + 6)},${f(R.shoulder[0][1] - 2)} L${f(R.hip[1][0] + 4)},${f(R.hipY - 4)} M${f(R.shoulder[1][0] - 8)},${f(R.shoulder[1][1] - 2)} L${f(R.hip[0][0] - 2)},${f(R.hipY - 6)}" stroke="${C.orange}" stroke-width="2.5"/>`;
    const tag = H.at(8, f(R.hy + 44), 0.34, K.props.priceTag({ text: "CLEARANCE", angle: 30 }));
    const body = K.person(POL) + straps + slots(C, R, { flags: false, bill: "med" }) + tag + pac + flame;
    const flyer = `<g transform="translate(1110,560) scale(${k}) rotate(78) translate(0,${f(-R.hipY)})">${body}</g>`;
    const spray = [[-330, 70, -20], [-420, 20, 15], [-490, 110, -35], [-580, 50, 25], [-650, 130, -10], [-740, 80, 30], [-820, 30, -18]]
      .map(([dx, dy, r], i) => H.at(f(1110 + dx), f(560 + dy), 0.66 - i * 0.04, K.money("med", i % 2), r)).join("");
    const puffs = puff(760, 640, 34) + puff(660, 600, 24) + puff(600, 676, 18);
    const yes = H.at(250, 660, 1.6, K.props.yesButton({ label: "YES" })) + H.at(420, 660, 1.6, K.props.yesButton({ label: "NO", color: C.war }));
    const svg = field() + `<rect x="-20" y="${TY - 30}" width="1960" height="40" fill="#BBA16C"/>` + track(C, TY, TW) +
      `<rect x="-20" y="${TY + TW + 6}" width="1960" height="200" fill="${GROUND}"/>` +
      yes + lines(C, [[180, 580, 160, 548], [320, 580, 340, 548]], 4) +
      spray + puffs + flyer +
      lines(C, [[700, 420, 520, 420], [690, 490, 470, 490], [720, 360, 600, 360]], 6);
    return { svg, alt: "On the race track's near straight, the grinning Politician in his teal tie flies flat out to the right a foot off the cinders, the war-red-caped rust SUPER PAC backpack strapped to his back and firing like a jet pack, a flame, smoke puffs and a spray of green medicine papers streaming out behind him; back at the trackside the YES and NO buttons, YES still bouncing." };
  },

  "scenic-route-algorithm"(H, fid) {
    const { K, C } = H;
    // after "senator.": by the box of gears, the Politician, the new campaign poster in one hand, slaps the desk bell
    // on the box himself and stares at its empty toaster slot for the next one; the burst YES hoop behind him.
    const G = 900, ink = C.line;
    // the Politician standing at the box's right end, facing it: his near arm straight out, palm down on the button
    const POL = K.castOpts("politician", { look: "left", tieColor: C.med, mood: "grin", arms: [[-80, -110], [10, 30]], holdR: null });
    const R = K.rig(POL), k = 2.5, X = 880, FEET = G;
    const palm = pt(X, FEET, k, R.hand[0]), held = pt(X, FEET, k, R.hand[1]);
    // the box of gears: a riveted slate box, a window on its gears, a row of lamps, a toaster slot, the coaster's
    // track running into its left side, the desk bell on the right end of its top, right under his palm
    const BELL = [palm[0] + 2, palm[1] + 10], BT = BELL[1] + 54, BW = 420, BH = G - BT, BX = BELL[0] - 160;
    let rivets = "";
    for (let i = 0; i < 9; i++) rivets += `<circle cx="${BX - BW / 2 + 22 + i * 47}" cy="${BT + 18}" r="5" fill="${C.cream}" stroke="${ink}" stroke-width="2"/>`;
    const lamps = [0, 1, 2, 3].map((i) => `<circle cx="${BX - 160 + i * 50}" cy="${BT - 18}" r="15" fill="${i % 2 ? C.yellow : C.orange}" stroke="${ink}" stroke-width="4"/>`).join("");
    const box = `<rect x="${BX - BW / 2}" y="${BT}" width="${BW}" height="${BH}" fill="${C.slate}" stroke="${ink}" stroke-width="6"/>` + rivets +
      `<path d="M${BX - BW / 2 + 8},${BT + 34} H${BX + BW / 2 - 8}" stroke="${C.orange}" stroke-width="4"/>` +
      `<rect x="${BX - 150}" y="${BT + 70}" width="300" height="190" rx="10" fill="#1A2238" stroke="${ink}" stroke-width="5"/>` +
      `<defs><clipPath id="${fid}-win"><rect x="${BX - 146}" y="${BT + 74}" width="292" height="182" rx="8"/></clipPath></defs>` +
      `<g clip-path="url(#${fid}-win)">${H.at(BX, BT + 250, 1.25, K.props.gears({ n: 4, dark: true }))}</g>` +
      `<rect x="${BX - BW / 2 - 20}" y="${BT - 6}" width="${BW + 40}" height="16" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` + lamps +
      `<rect x="${BX + 10}" y="${BT - 14}" width="100" height="12" fill="${ink}"/>` +
      // the coaster track running into the box's left side
      `<path d="M-20,${BT + 40} Q160,${BT + 30} ${BX - BW / 2},${BT + 150}" fill="none" stroke="${ink}" stroke-width="30"/><path d="M-20,${BT + 40} Q160,${BT + 30} ${BX - BW / 2},${BT + 150}" fill="none" stroke="${C.cream}" stroke-width="20"/>` +
      `<path d="M60,${BT + 42} V${G} M180,${BT + 62} V${G}" stroke="${C.rust}" stroke-width="16"/>` +
      // the desk bell, its button under his palm
      `<g transform="translate(${f(BELL[0])},${f(BT - 6)})"><path d="M-34,0 H34 V-8 H-34 Z" fill="${C.slate}" stroke="${ink}" stroke-width="3"/><path d="M-26,-8 Q-26,-42 0,-44 Q26,-42 26,-8 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/><circle cy="-48" r="6" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/></g>`;
    // the ding: lines off the bell either side of his hand
    const ding = lines(C, [[BELL[0] - 44, BELL[1] - 26, BELL[0] - 66, BELL[1] - 52], [BELL[0] + 2, BELL[1] - 36, BELL[0] + 2, BELL[1] - 66], [BELL[0] + 40, BELL[1] + 22, BELL[0] + 70, BELL[1] + 12]], 4);
    // the burst paper hoop on its stand
    const HX = 1460, HY = 520, HR = 150;
    const shreds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((i) => { const a = (i / 10) * Math.PI * 2; return `<path d="M${f(HX + HR * 0.96 * Math.cos(a))},${f(HY + HR * 0.96 * Math.sin(a))} L${f(HX + HR * 0.6 * Math.cos(a + 0.18))},${f(HY + HR * 0.6 * Math.sin(a + 0.18))} L${f(HX + HR * 0.96 * Math.cos(a + 0.4))},${f(HY + HR * 0.96 * Math.sin(a + 0.4))} Z" fill="${C.cream}" stroke="${ink}" stroke-width="2.5"/>`; }).join("");
    const hoop = `<path d="M${HX},${HY + HR} V${G}" stroke="${ink}" stroke-width="14"/><path d="M${HX},${HY + HR} V${G}" stroke="${C.tan}" stroke-width="8"/><path d="M${HX - 70},${G} H${HX + 70}" stroke="${ink}" stroke-width="12"/>` +
      shreds + `<circle cx="${HX}" cy="${HY}" r="${HR}" fill="none" stroke="${ink}" stroke-width="18"/><circle cx="${HX}" cy="${HY}" r="${HR}" fill="none" stroke="${C.war}" stroke-width="10" stroke-dasharray="40 26"/>` +
      `<text x="${HX + 40}" y="${HY + 112}" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="34" fill="${C.med}" transform="rotate(18 ${HX + 40} ${HY + 112})">YES</text>`;
    // the poster hangs from his other hand by its top corner
    const poster = H.at(f(held[0] - 10), f(held[1] - 6), 1, `<g transform="rotate(-10)"><rect x="0" y="0" width="92" height="64" fill="${C.cream}" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="0" y="0" width="92" height="15" fill="${C.med}"/><text x="46" y="52" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="30" fill="${C.med}">YES</text></g>`);
    const tag = H.at(f(X + 8 * k), f(FEET - 100 * k + (R.hy + 44) * k), k * 0.34, K.props.priceTag({ text: "CLEARANCE", angle: 6 }));
    const svg = field() + `<rect x="-20" y="${G}" width="1960" height="200" fill="#BBA16C"/><path d="M-20,${G} H1940" stroke="${ink}" stroke-width="4"/>` +
      box + hoop + poster + man(H, POL, X, FEET, k, slots(C, R, { flags: false, bill: "med" })) + tag + ding;
    return { svg, alt: "By the riveted box of gears with its lamps and its empty toaster slot, the Politician in his teal tie, a YES campaign poster dangling from one hand, slaps the desk bell on the box himself and stares at the slot for the next one; behind him the paper hoop on its stand is burst open." };
  },

  "nra-letter-grade"(H, fid) {
    const { K, C } = H;
    // after "diseases.": the schoolroom: the No Politician squeezed behind the little school desk, knees poking up,
    // hugging his report card to his chest (GUNS crossed out, NOT DYING FROM DISEASES, a teal A), grinning, his tie
    // gone teal; the Reaper slumped by the board over a red F on his own clipboard; YOU tiptoeing off right with the
    // carbon paper.
    const ink = C.line, FL = 880;
    const wall = `<rect x="-20" y="-20" width="1960" height="${FL + 20}" fill="#B9C2C4"/>` + `<rect x="-20" y="${FL - 120}" width="1960" height="120" fill="#A4ADB1"/><path d="M-20,${FL - 120} H1940" stroke="${C.rust}" stroke-width="10"/>`;
    const floorS = `<rect x="-20" y="${FL}" width="1960" height="220" fill="${BOARDS}"/><path d="M-20,${FL} H1940" stroke="${ink}" stroke-width="5"/>`;
    const board = `<rect x="200" y="90" width="900" height="400" fill="#8A6236" stroke="${ink}" stroke-width="6"/><rect x="226" y="116" width="848" height="348" fill="#3F5A48"/>` +
      `<text x="650" y="260" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="120" letter-spacing="10" fill="#E9ECE4" opacity="0.92">N.R.A.</text>` +
      `<rect x="230" y="480" width="840" height="18" fill="#8A6236" stroke="${ink}" stroke-width="4"/><rect x="300" y="470" width="40" height="10" fill="${WHITE}"/>`;
    // the Reaper slumped by the board's left end, his clipboard with a red F stamped on it
    const reaper = H.at(150, FL - 100 * 2.1, 2.1, `<g transform="rotate(-8 0 100)">${K.reaper()}</g>`);
    const clip = H.at(250, 700, 1.15, `<g transform="rotate(14)">${K.props.clipboard({ title: "", items: [] })}${H.at(0, -40, 1, K.props.stampMark({ text: "F", fontSize: 70, angle: -10 }))}</g>`);
    // the desk: a tan top on a slate frame, the knees poking up behind it
    const DX = 960, DT = 800;
    const POL = K.castOpts("politician", { look: "left", tieColor: C.med, mood: "grin", arms: [[-30, -100], [30, 100]], holdR: null });
    const R = K.rig(POL), k = 2.7, X = 980, FEET = 990;
    const card = H.at(f(X - 6), 720, 1, `<g transform="rotate(-5)"><rect x="-130" y="-70" width="260" height="140" fill="${WHITE}" stroke="${ink}" stroke-width="5"/>` +
      `<text x="-116" y="-36" font-family="Oswald" font-weight="600" font-size="21" fill="${ink}">SUBJECT:</text>` +
      `<text x="-26" y="-36" font-family="Oswald" font-weight="600" font-size="23" fill="${ink}">GUNS</text><path d="M-32,-43 H44" stroke="${C.war}" stroke-width="5"/>` +
      `<text x="-116" y="0" font-family="Inter" font-weight="700" font-style="italic" font-size="18" fill="${C.slate}">NOT DYING FROM</text><text x="-116" y="24" font-family="Inter" font-weight="700" font-style="italic" font-size="18" fill="${C.slate}">DISEASES</text>` +
      `<rect x="42" y="-6" width="76" height="68" fill="none" stroke="${ink}" stroke-width="3"/><text x="80" y="52" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="66" fill="${C.med}">A</text></g>`);
    const desk = `<path d="M${DX - 250},${DT} H${DX + 250} L${DX + 270},${DT + 30} H${DX - 270} Z" fill="${C.tan}" stroke="${ink}" stroke-width="5"/>` +
      `<rect x="${DX - 240}" y="${DT + 30}" width="480" height="60" fill="#9C6B45" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M${DX - 220},${DT + 90} V${FL + 40} M${DX + 220},${DT + 90} V${FL + 40}" stroke="${C.slate}" stroke-width="14"/>`;
    const knees = `<path d="M${DX - 190},${DT + 2} L${DX - 150},${DT - 64} L${DX - 104},${DT + 2} Z M${DX + 110},${DT + 2} L${DX + 152},${DT - 68} L${DX + 196},${DT + 2} Z" fill="#24304D" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>`;
    const top = pt(X, FEET, k, R.top);
    const wisp = `<path d="M${f(top[0] + 4)},${f(top[1] - 4)} q-20,-30 0,-60 q20,-30 0,-60" fill="none" stroke="#8C8782" stroke-width="5" stroke-linecap="round"/>`;
    // YOU tiptoeing off right, holding the carbon paper up by a corner
    const YOU = { tone: 2, outfit: "suit", hat: "bowler", look: "right", mood: "smug", arms: [[-30, -10], [118, 156]], build: { legPose: [[-14, -30], [26, -6]] } };
    const RY = K.rig(YOU), ky = 2.2, YX = 1580, YF = 900, yh = pt(YX, YF, ky, RY.hand[1]);
    const carbon = H.at(f(yh[0] + 4), f(yh[1] - 4), 1, `<g transform="rotate(10)"><rect x="-6" y="0" width="104" height="134" fill="#1F2D55" stroke="${ink}" stroke-width="4"/><path d="M8,24 H84 M8,44 H74 M8,64 H80" stroke="#3B4C7E" stroke-width="5"/></g>`);
    const svg = wall + floorS + board + reaper + clip + man(H, POL, X, FEET, k) + card + knees + desk + wisp + man(H, YOU, YX, YF, ky) + carbon;
    return { svg, alt: "A 1950s schoolroom: N.R.A. chalked on the green board; the No Politician, squeezed behind a little school desk with his knees poking up, grins and hugs his report card, SUBJECT: GUNS crossed out and NOT DYING FROM DISEASES written in, a teal A in the grade box; the Grim Reaper slumps by the board over a red F stamped on his own clipboard; YOU tiptoes off to the right holding up a sheet of carbon paper." };
  },

  "most-problems-scroll"(H, fid) {
    const { K, C } = H;
    // after "problems.": the bond on the lectern's reading top; the scroll's first part running down the lectern's
    // front; its far end dropped back in from the top of the frame onto the lectern's right end, numbered in the
    // thousands, the strip slanting up out of the frame clear of her face; Wishonia shrugs and side-eyes the camera.
    // (The lectern's reading top is at y 790, x 540..980.)
    const ink = C.line, PAPER = "#F6EFD8";
    const bond = H.at(640, 792, 0.95, K.props.bond({ text: "INCENTIVE ALIGNMENT BOND" }));
    const entry = (x, y, s, text, rot = 0) => `<text x="${f(x)}" y="${f(y)}" font-family="Inter" font-weight="700" font-size="${s}" fill="${ink}"${rot ? ` transform="rotate(${rot} ${f(x)} ${f(y)})"` : ""}>${H.esc(text)}</text>`;
    // the strip down the lectern front, from the top roll
    const down = `<path d="M790,792 L950,792 L966,1090 L800,1090 Z" fill="${PAPER}" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="780" y="770" width="180" height="26" rx="12" fill="${C.tan}" stroke="${ink}" stroke-width="4"/>` +
      entry(808, 842, 23, "1. WAR") + entry(808, 884, 23, "2. DISEASE") + entry(808, 926, 23, "3. POTHOLES") + entry(810, 968, 23, "4. ...");
    // the far end: from the roll on the lectern's right end (x 930..1060, y 778) up and out of the top of the frame
    const B0 = [930, 778], B1 = [1060, 778], T0 = [1250, -20], T1 = [1380, -20], ang = (Math.atan2(T0[0] - B0[0], B0[1] - T0[1]) * 180) / Math.PI;
    const up = `<path d="M${T0[0]},${T0[1]} L${T1[0]},${T1[1]} L${B1[0]},${B1[1]} L${B0[0]},${B0[1]} Z" fill="${PAPER}" stroke="${ink}" stroke-width="4"/>` +
      ["4,812. TAXES", "4,813. TRAFFIC", "4,814. GERMS", "4,815. MONDAYS", "4,816. ..."].map((t, i) => {
        const u = 0.86 - i * 0.17, x = B0[0] + (T0[0] - B0[0]) * u + 12, y = B0[1] + (T0[1] - B0[1]) * u;
        return entry(x, y, 21, t, f(ang));
      }).join("") +
      `<rect x="914" y="762" width="166" height="30" rx="14" fill="${C.tan}" stroke="${ink}" stroke-width="4"/>` +
      lines(C, [[1100, 740, 1130, 712], [1110, 780, 1150, 780], [900, 742, 872, 716]], 4);
    const svg = H.host("sideeye-closed", "shrug", bond + down + up);
    return { svg, alt: "Wishonia shrugs at her lectern and side-eyes the camera; the INCENTIVE ALIGNMENT BOND stands on the lectern, the scroll of PROBLEMS (1. WAR, 2. DISEASE, 3. POTHOLES) runs down the lectern's front and out of the frame, and its far end, numbered in the thousands, has dropped back in from the top of the frame and landed on the lectern beside her." };
  },
};
