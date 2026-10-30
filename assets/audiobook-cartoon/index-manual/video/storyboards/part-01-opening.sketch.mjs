// Sketches for storyboards/part-01-opening.md (v3, the 1950s atomic-age film look of Part 2): each scene's key frame
// on a 1920 x 1080 frame (16:9), drawn with the production art. Host shots use the studio set (KIT.STUDIO positions);
// a plate frame is one framing as the camera sees it, the ground and the cast drawn large.
// Built into the review sheet by tools/storyboard-sheet.mjs.

const f = (n) => n.toFixed(1);
const copy = (a, b) => Object.assign({}, a, b || {});
const at = (x, y, k, inner, rot = 0) => `<g transform="translate(${f(x)},${f(y)})${rot ? ` rotate(${rot})` : ""} scale(${k})">${inner}</g>`;
// A person standing with its feet on screen y `feet` at scale k (KIT.person draws the feet at y 100).
const stand = (x, feet, k, inner) => at(x, feet - 100 * k, k, inner);
// A host shot's slow push in on her face (KIT.studio), k of the way along.
const push = (S, k, inner) => `<g transform="translate(${S.face[0]},${S.face[1]}) scale(${k}) translate(${-S.face[0]},${-S.face[1]})">${inner}</g>`;
// A walking paper (KIT.money, legs to y 48) with its feet on screen y `feet` at scale k.
const bill = (K, x, feet, k, kind, legs = 0.5) => at(x, feet - 48 * k, k, K.money(kind, legs));
// A seeded generator, so the sketches draw the same every time.
function rng(seed) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}

// Plate colors (as Part 2's money-loop and the-toll).
const SKY = "#EFE3C4", GROUND = "#C8B07B", GROUND_EDGE = "#B09363";
const field = (horizon) => `<rect width="1920" height="1080" fill="${SKY}"/><rect y="${horizon}" width="1920" height="${1080 - horizon}" fill="${GROUND}"/><path d="M0,${horizon} H1920" stroke="${GROUND_EDGE}" stroke-width="4"/>`;

// A four-point atomic-age star.
function star(x, y, r, color) {
  const pts = [];
  for (let i = 0; i < 8; i++) {
    const a = (Math.PI * i) / 4 - Math.PI / 2, rr = i % 2 ? r * 0.22 : r;
    pts.push(`${f(x + rr * Math.cos(a))},${f(y + rr * Math.sin(a))}`);
  }
  return `<polygon points="${pts.join(" ")}" fill="${color}"/>`;
}
// A six-armed snowflake, r long.
function flake(x, y, r, color, rot = 0) {
  let d = "";
  for (let i = 0; i < 3; i++) {
    const a = ((i * 60 + rot) * Math.PI) / 180, c = Math.cos(a), s = Math.sin(a);
    d += `M${f(x - r * c)},${f(y - r * s)} L${f(x + r * c)},${f(y + r * s)} `;
    for (const k of [-1, 1]) {
      const bx = x + k * r * 0.55 * c, by = y + k * r * 0.55 * s;
      for (const t of [-1, 1]) {
        const b = a + (k * t * Math.PI) / 4;
        d += `M${f(bx)},${f(by)} l${f(k * r * 0.3 * Math.cos(b))},${f(k * r * 0.3 * Math.sin(b))} `;
      }
    }
  }
  return `<path d="${d}" stroke="${color}" stroke-width="${f(r * 0.2)}" stroke-linecap="round" fill="none"/>`;
}
// Smoke wisps rising from (x, y).
function wisps(x, y, k, color = "#8A8478") {
  return [-14, 0, 14].map((dx) => `<path d="M${f(x + dx * k)},${f(y)} q${f(-8 * k)},${f(-12 * k)} 0,${f(-24 * k)} q${f(8 * k)},${f(-12 * k)} 0,${f(-24 * k)}" fill="none" stroke="${color}" stroke-width="${f(4 * k)}" stroke-linecap="round"/>`).join("");
}
// The atom (the film's emblem), with its electrons, around (x, y).
function atomDrawing(K, C, x, y, r) {
  const e = [0, 60, -60].map((a, i) => {
    const th = (i * 2.2 + 0.6), ar = (a * Math.PI) / 180, ex = r * Math.cos(th), ey = r * 0.31 * Math.sin(th);
    return `<circle cx="${f(x + ex * Math.cos(ar) - ey * Math.sin(ar))}" cy="${f(y + ex * Math.sin(ar) + ey * Math.cos(ar))}" r="${f(r * 0.07)}" fill="${C.yellow}" stroke="${C.line}" stroke-width="3"/>`;
  }).join("");
  return `<circle cx="${x}" cy="${y}" r="${f(r * 1.1)}" fill="${C.yellow}" opacity="0.25"/>` + K.atom(x, y, r, C.line) + e;
}

// ── The host shot's lectern props (eligible, my-surprise, earth-means-dirt; KIT.STUDIO 16:9) ──
// The PLANETS out-tray at the lectern's left end, with the other planets' files in it.
function planetsTray(H, C, withEarth) {
  const ink = C.line, x = 486, y = 706, w = 250;
  // a file: its body from body-top y down to the tray, its tab (with the planet's name) at tabX along it
  const file = (top, tabX, fill, text) => `<rect x="${x + 10}" y="${y + top}" width="${w - 20}" height="${80 - top}" fill="${fill}" stroke="${ink}" stroke-width="3"/>` +
    `<path d="M${x + tabX},${y + top} v-20 q0,-4 4,-4 h${tabW - 8} q4,0 4,4 v20 Z" fill="${fill}" stroke="${ink}" stroke-width="3"/>` + H.label(x + tabX + tabW / 2, y + top - 6, 14, text, "middle", ink);
  const tabW = 136;
  const files = file(28, 6, "#E9C27A", "VENUS: TOO HOT") + file(52, 106, C.tan, "MARS: NOBODY HOME") + (withEarth ? file(16, 58, "#E2B865", "EARTH: CASE #847") : "");
  const front = `<path d="M${x},${y + 52} H${x + w} L${x + w - 10},${y + 86} H${x + 10} Z" fill="${C.slate}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
    [0, 1, 2, 3, 4, 5, 6].map((i) => `<path d="M${x + 22 + i * 34},${y + 56} V${y + 82}" stroke="${C.peri}" stroke-width="2.5"/>`).join("") +
    `<rect x="${x + 70}" y="${y + 58}" width="110" height="22" rx="3" fill="${C.cream}" stroke="${ink}" stroke-width="2.5"/>` + H.label(x + 125, y + 76, 16, "PLANETS", "middle", ink);
  return files + front;
}
// The Earth case file on a little studio easel in the free wall right of the lectern, its cover sheet the
// eligibility form. o: { ticks, stamp, tab: "plain" | "dirt" }
function caseFile(H, K, C, o) {
  const ink = C.line, x = 1190, y = 450, w = 300, h = 270;
  const easel = `<path d="M${x + 40},1080 L${x + w / 2},${y - 30} L${x + w - 40},1080 M${x + w / 2},${y - 30} L${x + w / 2 + 30},1080" fill="none" stroke="${C.rust}" stroke-width="16" stroke-linecap="round"/>` +
    `<path d="M${x + 40},1080 L${x + w / 2},${y - 30} L${x + w - 40},1080" fill="none" stroke="${ink}" stroke-width="3"/>` +
    `<rect x="${x - 20}" y="${y + h - 4}" width="${w + 40}" height="22" rx="4" fill="${C.tan}" stroke="${ink}" stroke-width="4"/>`;
  let out = easel + `<g transform="rotate(-3 ${x + w / 2} ${y + h})">`;
  out += `<path d="M${x},${y + 30} H${x + 18} L${x + 30},${y} H${x + 216} L${x + 228},${y + 30} H${x + w} V${y + h} H${x} Z" fill="#E2B865" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>`;
  if (o.tab === "dirt") {
    out += H.label(x + 90, y + 24, 22, "EARTH", "middle", ink, 'opacity="0.8"') + `<path d="M${x + 54},${y + 16} L${x + 128},${y + 13}" stroke="${C.war}" stroke-width="7" stroke-linecap="round"/>` +
      H.label(x + 176, y + 24, 22, ": CASE #847", "middle", ink) +
      `<text x="${x + 96}" y="${y - 10}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="46" fill="${C.war}" transform="rotate(-6 ${x + 96} ${y - 10})">DIRT</text>`;
  } else out += H.label(x + 124, y + 24, 22, "EARTH: CASE #847", "middle", ink);
  // the cover sheet: the 1950s mail-in form, with only its boxes
  const fx = x + 20, fy = y + 42, fw = w - 40, fh = h - 56;
  out += `<rect x="${fx}" y="${fy}" width="${fw}" height="${fh}" fill="#FBF6E6" stroke="${ink}" stroke-width="3"/>` +
    H.label(fx + fw / 2, fy + 34, 24, "PLANET ELIGIBILITY CHECK", "middle", ink) + `<path d="M${fx + 14},${fy + 46} H${fx + fw - 14}" stroke="${C.orange}" stroke-width="3"/>`;
  [0, 1].forEach((i) => {
    const by = fy + 62 + i * 58;
    out += H.label(fx + 20, by + 30, 26, `${i + 1}.`, "start", ink) + K.checkbox(fx + 54, by + 2, 34) + H.label(fx + 98, by + 30, 22, "YES", "start", ink) +
      K.checkbox(fx + 150, by + 2, 34) + H.label(fx + 194, by + 30, 22, "NO", "start", ink);
    if (o.ticks) out += H.tick(fx + 50, by - 6, 44, C.med);
  });
  out += `<text x="${fx + 14}" y="${fy + fh - 10}" font-family="Inter" font-style="italic" font-weight="500" font-size="11" fill="${ink}" opacity="0.75">Please allow 4 to 6 weeks for optimization.</text>`;
  if (o.stamp) out += at(x + w / 2 + 4, y + 200, 0.7, K.props.stampMark({ text: "MAY BE ELIGIBLE\nFOR OPTIMIZATION", angle: -10, fontSize: 34 }));
  return out + "</g>";
}

// ── The plates' own drawings ──
// The 1950s sofa (back and front drawn apart, so people sit between them).
function sofaBack(C, x0, x1, top) {
  const ink = C.line;
  return `<path d="M${x0 + 30},${top + 30} Q${x0 + 30},${top} ${x0 + 70},${top} H${x1 - 70} Q${x1 - 30},${top} ${x1 - 30},${top + 30} V${top + 230} H${x0 + 30} Z" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>` +
    [1, 2].map((i) => `<path d="M${f(x0 + 30 + ((x1 - x0 - 60) * i) / 3)},${top + 24} V${top + 220}" stroke="#6E3A23" stroke-width="4"/>`).join("") +
    [0, 1, 2].map((i) => `<circle cx="${f(x0 + 30 + ((x1 - x0 - 60) * (i + 0.5)) / 3)}" cy="${top + 90}" r="6" fill="#6E3A23"/>`).join("");
}
function sofaFront(C, x0, x1, seat) {
  const ink = C.line, cush = (a, b) => `<rect x="${f(a)}" y="${seat}" width="${f(b - a)}" height="60" rx="14" fill="${C.orange}" stroke="${ink}" stroke-width="5"/>`;
  const third = (x1 - x0 - 160) / 3;
  return cush(x0 + 80, x0 + 80 + third) + cush(x0 + 80 + third, x0 + 80 + 2 * third) + cush(x0 + 80 + 2 * third, x1 - 80) +
    `<rect x="${x0 + 40}" y="${seat + 54}" width="${x1 - x0 - 80}" height="136" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>` +
    `<path d="M${x0 + 40},${seat + 150} H${x1 - 40}" stroke="#6E3A23" stroke-width="3"/>` +
    [x0, x1 - 90].map((ax) => `<rect x="${ax}" y="${seat - 50}" width="90" height="240" rx="26" fill="${C.rust}" stroke="${ink}" stroke-width="5"/>`).join("") +
    [x0 + 60, x1 - 60].map((lx) => `<path d="M${lx},${seat + 190} l-10,16 h14 l6,-16 Z" fill="${C.slate}" stroke="${ink}" stroke-width="3"/>`).join("");
}
// A picket fence section from x0 to x1, ground y g, h tall.
function fence(C, x0, x1, g, h) {
  const ink = C.line;
  let p = "";
  for (let x = x0; x <= x1 - 30; x += 40) p += `<path d="M${x},${g} V${g - h + 16} l15,-16 l15,16 V${g} Z" fill="${C.cream}" stroke="${ink}" stroke-width="3.5" stroke-linejoin="round"/>`;
  return `<rect x="${x0 - 6}" y="${g - h * 0.72}" width="${x1 - x0 + 12}" height="14" fill="${C.cream}" stroke="${ink}" stroke-width="3.5"/>` +
    `<rect x="${x0 - 6}" y="${g - h * 0.3}" width="${x1 - x0 + 12}" height="14" fill="${C.cream}" stroke="${ink}" stroke-width="3.5"/>` + p;
}
// A chrome 1950s toaster sitting on y 0, about 120 wide, with two slices up (fill: the toast).
function toaster(C, toast) {
  const ink = C.line;
  const slice = (x) => `<path d="M${x - 20},-96 Q${x - 22},-122 ${x},-124 Q${x + 22},-122 ${x + 20},-96 Z" fill="${toast}" stroke="${ink}" stroke-width="3"/>`;
  return slice(-22) + slice(22) +
    `<path d="M-60,0 V-70 Q-60,-100 -30,-100 H30 Q60,-100 60,-70 V0 Z" fill="#C9CED6" stroke="${ink}" stroke-width="4"/>` +
    `<path d="M-46,-80 Q-46,-90 -36,-90 H-10" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.8"/>` +
    `<rect x="62" y="-58" width="14" height="10" rx="3" fill="${C.slate}" stroke="${ink}" stroke-width="2.5"/>` +
    `<rect x="-66" y="-6" width="132" height="10" rx="4" fill="${C.slate}" stroke="${ink}" stroke-width="3"/>`;
}
// A stack of n bills (K.money flat, no legs), each 96 x 50 at scale k, bottom on y 0, lightly jittered.
function billStack(K, C, n, k, seed, kind = "war") {
  const r = rng(seed);
  let out = "";
  for (let i = 0; i < n; i++) out += at((r() - 0.5) * 10 * k, -25 * k - i * 30 * k, k, K.money(kind, 0).replace('class="legs"', 'class="legs" opacity="0"'));
  return out;
}

export default {
  "theme-music-video"(H) {
    const { C } = H;
    let tiles = "";
    for (let i = 0; i < 15; i++) {
      const x = (i % 4) * 480, y = Math.floor(i / 4) * 270;
      tiles += H.image(`assets/music-video/keyframes/scene-${String(i + 1).padStart(2, "0")}.jpg`, x, y, 480, 270) +
        `<rect x="${x + 12}" y="${y + 12}" width="58" height="40" rx="6" fill="${C.ink}" opacity="0.8"/>` + H.label(x + 41, y + 42, 26, String(i + 1), "middle", C.cream);
    }
    const svg = `<rect width="1920" height="1080" fill="${C.cream}"/>` + tiles +
      `<rect x="1440" y="810" width="480" height="270" fill="${C.navy}"/>` +
      H.label(1680, 890, 34, "THEME SONG", "middle", C.cyan) + H.label(1680, 934, 34, "MUSIC VIDEO", "middle", C.cyan) +
      H.text(1680, 984, 26, ["0:00 to 1:40 · 15 clips", "existing video, not redrawn"], { anchor: "middle", fill: C.cream, weight: 600 }) +
      [1, 2, 3].map((k) => `<path d="M${k * 480},0 V1080" stroke="${C.cream}" stroke-width="6"/><path d="M0,${k * 270} H1920" stroke="${C.cream}" stroke-width="6"/>`).join("");
    return { svg, alt: "The 15 keyframes of the existing theme song music video in a grid, in order, with a tile reading Theme song music video, 0:00 to 1:40, 15 clips." };
  },

  "title-card"(H) {
    const { K, C } = H;
    // KIT.titleScene's atomic card (16:9): the emblem over the heading, the label line and the subtitle pill
    const cx = 960, cy = 150, rx = 116;
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="22" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 7}" cy="${cy - 7}" r="6" fill="${C.yellow}"/>`;
    const orbits = [0, 60, -60].map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${f(rx * 0.31)}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const word = (y, s, text) => {
      const t0 = (dx, dy, extra) => `<text x="${960 + dx}" y="${y + dy}" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="${s}" ${extra}>${H.esc(text)}</text>`;
      return t0(0.04 * s, 0.053 * s, `fill="${C.ink}"`) + t0(0, 0, `fill="${C.cream}" stroke="${C.cream}" stroke-width="${f(0.044 * s)}" stroke-linejoin="round" style="paint-order:stroke"`);
    };
    const label = `<text x="960" y="632" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="56" letter-spacing="2" fill="${C.cream}" stroke="${C.ink}" stroke-width="8" style="paint-order:stroke">(for Busy People)</text>`;
    const pill = `<rect x="330" y="664" width="1260" height="74" rx="37" fill="${C.deep}" stroke="${C.orange}" stroke-width="4"/>` +
      H.text(960, 713, 34, ["A Step-by-Step Guide to Optimizing Your Terrible Civilization"], { anchor: "middle", fill: C.cream, weight: 700 });
    // the busy human sprinting along the bottom, his eyes on his wristwatch, and his speed lines
    const RUN = { tone: 2, outfit: "suit", hat: "bowler", mood: "eager", look: "right", arms: [[-60, -150], [70, 30]] };
    const R = K.rig(RUN), k = 0.95, rx0 = 1230, feet = 948;
    const watch = `<circle cx="${f(R.hand[0][0])}" cy="${f(R.hand[0][1])}" r="5" fill="${C.cream}" stroke="${C.ink}" stroke-width="2"/>`;
    const lines = [0, 1, 2].map((i) => `<path d="M${rx0 - 90 - i * 30},${feet - 130 + i * 40} H${rx0 - 190 - i * 50}" stroke="${C.cream}" stroke-width="5" stroke-linecap="round" opacity="0.6"/>`).join("");
    const runner = lines + stand(rx0, feet, k, `<g transform="rotate(8 0 60)">${K.person(RUN)}${watch}</g>`);
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + nucleus + word(420, 124, "HOW TO END") + word(562, 124, "WAR AND DISEASE") + label + pill + runner;
    return { svg, alt: "The period title card: the film's atom on plain navy, HOW TO END WAR AND DISEASE in big cream letters, (for Busy People) under it, the subtitle pill, and a busy man in a bowler sprinting along the bottom, checking his watch." };
  },

  "loved-ones"(H, id) {
    const { K, C } = H, ink = C.line;
    // the living room, then the portrait print the flash develops: the family as skeletons, the Reaper unchanged
    const r = rng(7);
    let paper = `<rect width="1920" height="1080" fill="#D9C08C"/>`;
    for (let y = 30; y < 820; y += 90) for (let x = (y / 90) % 2 ? 60 : 15; x < 1920; x += 90) paper += `<path d="M${x},${y - 14} l12,14 l-12,14 l-12,-14 Z" fill="${C.tan}" opacity="0.55"/>`;
    const floor = `<rect y="940" width="1920" height="140" fill="${C.slate}"/><path d="M0,940 H1920" stroke="${ink}" stroke-width="4"/>`;
    const lamp = `<path d="M230,960 V420" stroke="${ink}" stroke-width="8"/><path d="M190,960 h80" stroke="${ink}" stroke-width="10"/>` +
      `<path d="M150,420 L180,310 H280 L310,420 Z" fill="${C.cream}" stroke="${ink}" stroke-width="5"/>` +
      [...Array(9)].map((_, i) => `<path d="M${156 + i * 18},420 v16" stroke="${C.orange}" stroke-width="4"/>`).join("");
    const clock = `<rect x="1660" y="420" width="190" height="24" fill="${C.rust}" stroke="${ink}" stroke-width="4"/><path d="M1700,420 V340 Q1755,290 1810,340 V420 Z" fill="${C.tan}" stroke="${ink}" stroke-width="4"/>` +
      `<circle cx="1755" cy="365" r="26" fill="${C.cream}" stroke="${ink}" stroke-width="3"/><path d="M1755,365 V348 M1755,365 h12" stroke="${ink}" stroke-width="3"/>`;
    const k = 2.8, seat = 770;
    const FAM = [
      { o: { tone: 1, outfit: "shirt", color: 1, hair: 0, seed: 11 }, x: 640 },
      { o: { tone: 1, outfit: "shirt", color: 0, hair: 0, seed: 5, hat: null, build: { hs: 1.18, legs: 0.8 } }, x: 870, k: 2.0 },
      { o: { tone: 1, outfit: "dress", color: 3, hair: 1, seed: 4 }, x: 1090 },
    ];
    // sitting: the hips at the seat, the legs hidden by the sofa's front, which runs down to the floor
    const sit = (m) => { const kk = m.k || k, o = copy(m.o, { skeleton: true, arms: [[10, 30], [-10, -30]] }), R = K.rig(o); return at(m.x, seat + 14 - kk * R.hipY, kk, K.person(o)); };
    const grandpa = { tone: 1, outfit: "suit", color: 2, hair: 2, glasses: true, hat: null, seed: 8 };
    const back = stand(1390, 900, 2.8, K.person(copy(grandpa, { skeleton: true })));
    const reaper = at(1235, 900 - 100 * 2.5, 2.5, K.reaper({ pose: "puppet", only: "body" }));
    // the Reaper's bony arms round the grandfather's and the mother's shoulders: the puppet's arms, in front of them
    const arms = at(1235, 900 - 100 * 2.5, 2.5, K.reaper({ pose: "puppet", only: "arms", arms: [8, 16] }));
    const sitters = `<clipPath id="${id}-sit"><rect width="1920" height="930"/></clipPath><g clip-path="url(#${id}-sit)">${FAM.map(sit).join("")}</g>`;
    const room = paper + lamp + clock + floor + reaper + back + sofaBack(C, 400, 1540, 600) + sitters + arms + sofaFront(C, 400, 1540, seat);
    // the print: a white border with a deckled edge, tilted a little, on the dark of the cut
    let edge = "M150,60";
    for (let x = 150; x <= 1770; x += 18) edge += ` L${x},${60 + (r() < 0.5 ? 0 : 5)}`;
    for (let y = 60; y <= 1020; y += 18) edge += ` L${1770 - (r() < 0.5 ? 0 : 5)},${y}`;
    for (let x = 1770; x >= 150; x -= 18) edge += ` L${x},${1020 - (r() < 0.5 ? 0 : 5)}`;
    for (let y = 1020; y >= 60; y -= 18) edge += ` L${150 + (r() < 0.5 ? 0 : 5)},${y}`;
    const svg = `<rect width="1920" height="1080" fill="${C.deep}"/><g transform="rotate(-2 960 540)">` +
      `<path d="${edge} Z" fill="#000" opacity="0.35" transform="translate(14,16)"/><path d="${edge} Z" fill="#FBF6E6"/>` +
      `<defs><clipPath id="${id}-print"><rect x="190" y="98" width="1540" height="884"/></clipPath></defs>` +
      `<g clip-path="url(#${id}-print)"><g transform="translate(190,98) scale(0.802)">${room}</g></g></g>`;
    return { svg, alt: "The family portrait after the flash, developed as a print in a white deckled border: on a rust sofa in a 1950s living room, the father, the boy and the mother are grinning skeletons, the grandfather a skeleton in his glasses behind them, and the Grim Reaper grins between the heads with his bony arms round them." };
  },

  "nuclear-winters"(H) {
    const { K, C } = H, ink = C.line;
    const r = rng(3);
    let sky = `<rect width="1920" height="1080" fill="${C.navy}"/>`;
    for (let i = 0; i < 40; i++) sky += star(r() * 1920, r() * 1080, 6 + r() * 12, C.yellow);
    // the 122 red snowflakes hanging over the little planet, and the number among them
    let flakes = "";
    let n = 0;
    while (n < 122) {
      const x = 60 + r() * 1800, y = 40 + r() * 520;
      if (Math.abs(x - 960) < 220 && y > 60 && y < 290) continue;
      if (Math.abs(x - 960) < 160 && y > 290) continue;
      flakes += flake(x, y, 14 + r() * 8, C.war, r() * 60);
      n++;
    }
    let snow = "";
    for (let i = 0; i < 60; i++) snow += `<circle cx="${f(r() * 1920)}" cy="${f(560 + r() * 520)}" r="${f(3 + r() * 3)}" fill="${C.war}" opacity="0.8"/>`;
    // the little Earth, a cap of snow on top, the human in his scarf frozen in a block of ice, the drift to his knees
    const gx = 960, gr = 220, gc = 1080 - gr;
    const globe = at(gx, 1080, 1, K.props.earthGlobe({ r: gr, face: "none" }));
    const cap = `<path d="M${gx - 192},${gc - 112} A228,228 0 0,1 ${gx + 192},${gc - 112} Q${gx + 120},${gc - 150} ${gx + 60},${gc - 132} Q${gx},${gc - 170} ${gx - 70},${gc - 136} Q${gx - 130},${gc - 150} ${gx - 192},${gc - 112} Z" fill="#F7F3EA" stroke="${ink}" stroke-width="4"/>`;
    const MAN = { tone: 2, outfit: "shirt", color: 2, hair: 0, seed: 31, mood: "worried", arms: [[14, 20], [-20, -40]] };
    const R = K.rig(MAN), k = 1.9, feet = gc - gr + 14;
    const scarf = `<path d="M${f(R.neck[0] - 15)},${f(R.neck[1] + 1)} H${f(R.neck[0] + 15)} l-3,28 h-8 l-2,-20 Z" fill="${C.orange}" stroke="${ink}" stroke-width="2.5"/>`;
    const can = `<path d="M${f(R.hand[1][0] - 2)},${f(R.hand[1][1] - 6)} h18 v16 h-18 Z M${f(R.hand[1][0] + 16)},${f(R.hand[1][1] - 2)} l14,-8" fill="#9AA6B8" stroke="${ink}" stroke-width="2"/>`;
    const man = stand(gx, feet, k, K.person(MAN) + scarf + can);
    const top = feet - 100 * k + R.top[1] * k - 24;
    const drift = `<path d="M${gx - 170},${feet + 10} Q${gx - 90},${feet - 96} ${gx},${feet - 104} Q${gx + 90},${feet - 96} ${gx + 170},${feet + 10} Z" fill="#F7F3EA" stroke="${ink}" stroke-width="4"/>`;
    const ice = `<rect x="${gx - 112}" y="${f(top)}" width="224" height="${f(feet - top - 20)}" rx="10" fill="#BFE3EA" opacity="0.6" stroke="#F7FBFC" stroke-width="6"/>` +
      `<path d="M${gx - 88},${f(top + 24)} l36,0 M${gx - 92},${f(top + 44)} l18,0 M${gx + 64},${f(top + 70)} l24,48" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.9"/>`;
    const svg = sky + flakes + snow + globe + cap + man + ice + drift + H.big(960, 230, 160, "122", "middle", C.cream);
    return { svg, alt: "In the theme song's starry navy sky, a sky full of red snowflakes with 122 among them hangs over one little Earth capped with snow; on top, its one human in a scarf is frozen solid in a block of ice, the drift up to his chest." };
  },

  "eligible"(H) {
    const { K, C } = H, S = K.STUDIO;
    // just after "eligible": the stamp lifted again over the file, both YES ticked, the mark in red across the form
    const stamp = at(1350, 380, 1.5, K.props.stamp({ text: "", color: C.war }), -8);
    const front = planetsTray(H, C, false) + caseFile(H, K, C, { ticks: true, stamp: true, tab: "plain" }) + stamp;
    const svg = push(S, 1.03, H.host("happy-smile", "palms-down", front));
    return { svg, alt: "Wishonia at her lectern, smiling, palms down; on the lectern the Earth case file stands propped up, its eligibility-form cover with both YES boxes ticked and MAY BE ELIGIBLE FOR OPTIMIZATION stamped across it in red, the rubber stamp just lifted above it, and a PLANETS out-tray at the other end holding VENUS: TOO HOT and MARS: NOBODY HOME." };
  },

  "meet-wishonia"(H) {
    const { K, C } = H, S = K.STUDIO, ink = C.line;
    // the nameplate: on the lectern's front edge, grown out past its end and off the left of the frame, sagging
    const plate = `<path d="M1000,742 H520 C300,742 120,760 -40,800 V880 C120,842 300,826 520,826 H1000 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>` +
      `<path d="M1000,750 H530 C310,750 130,767 -40,806" fill="none" stroke="#F6D88A" stroke-width="4"/>` +
      H.label(800, 778, 36, "WISHONIA LOVE", "middle", ink) + H.label(800, 806, 20, "C.E.O. AND PRESIDENT", "middle", ink) +
      `<text font-family="Oswald" font-weight="600" font-size="22" letter-spacing="3" fill="${ink}"><textPath href="#meet-plate-line" startOffset="0">UNIVERSE OPTIMIZATION SERVICES</textPath></text>` +
      `<defs><path id="meet-plate-line" d="M-20,846 C120,812 300,800 640,800"/></defs>`;
    // the studio card on its strings, and the charred wreck of the converter under it with its singed card
    const card = `<path d="M1330,0 V150 M1690,0 V150" stroke="${ink}" stroke-width="3"/><rect x="1215" y="150" width="590" height="180" fill="${C.cream}" stroke="${ink}" stroke-width="6"/>` +
      `<rect x="1229" y="164" width="562" height="152" fill="none" stroke="${C.orange}" stroke-width="3"/>` + H.big(1510, 272, 76, "4,297 YEARS", "middle", C.navy);
    const machine = `<rect x="-170" y="-330" width="340" height="330" rx="10" fill="${C.peri}" stroke="${ink}" stroke-width="6"/>` +
      `<circle cx="-80" cy="-230" r="52" fill="${C.cream}" stroke="${ink}" stroke-width="5"/><circle cx="70" cy="-230" r="52" fill="${C.cream}" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M-80,-230 l20,-38 M70,-230 l-36,12" stroke="${ink}" stroke-width="5"/>` +
      `<rect x="-90" y="-120" width="180" height="22" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M-120,-330 L-150,-420 L-100,-430 L-90,-336 Z" fill="${C.slate}" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M120,-330 a26,26 0 1,1 40,0 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M170,-150 l40,10 l6,80" fill="none" stroke="${ink}" stroke-width="8" stroke-linecap="round"/>`;
    const gear = `<g transform="translate(-200,-300)"><path d="M0,0 q-20,-20 0,-40 q20,-20 0,-40" fill="none" stroke="${ink}" stroke-width="4"/>` +
      `<circle cx="0" cy="-70" r="30" fill="${C.tan}" stroke="${ink}" stroke-width="5"/>` +
      [...Array(8)].map((_, i) => `<rect x="-6" y="-110" width="12" height="14" fill="${C.tan}" stroke="${ink}" stroke-width="3" transform="rotate(${i * 45} 0 -70)"/>`).join("") + "</g>";
    const wreck = `<g transform="translate(1510,1040) rotate(4) skewX(-6)">${K.burn(machine + gear)}` +
      // its two dials are its eyes now, white in the soot, blinking
      `<ellipse cx="-80" cy="-230" rx="30" ry="22" fill="#FFFFFF" stroke="${ink}" stroke-width="3"/><ellipse cx="70" cy="-230" rx="30" ry="22" fill="#FFFFFF" stroke="${ink}" stroke-width="3"/>` +
      `<circle cx="-72" cy="-228" r="9" fill="${ink}"/><circle cx="78" cy="-228" r="9" fill="${ink}"/></g>`;
    const singed = `<g transform="translate(0,-130) rotate(-6 1520 990)"><path d="M1400,960 L1408,948 L1420,958 L1436,946 L1452,958 L1470,946 L1490,958 L1510,946 L1530,958 L1550,946 L1570,958 L1590,946 L1610,958 L1630,948 L1640,960 V1020 H1400 Z" fill="#E6D3A8" stroke="${ink}" stroke-width="4"/>` +
      H.label(1520, 1004, 34, "4,297 YEARS", "middle", ink) + "</g>";
    const smoke = wisps(1380, 640, 1.6) + wisps(1600, 620, 1.4);
    const front = plate + card + wreck + singed + smoke;
    const svg = push(S, 1.04, H.host("smirk-closed", "idle", front));
    return { svg, alt: "Wishonia at her lectern looks at the camera; her brass nameplate WISHONIA LOVE, C.E.O. AND PRESIDENT, UNIVERSE OPTIMIZATION SERVICES runs past the lectern's end and off the left of the frame, sagging; on the right a studio card reads 4,297 YEARS, and under it the charred, smoking wreck of the unit converter blinks its white eyes and spits out a singed card that reads 4,297 YEARS." };
  },

  "split-the-atom"(H) {
    const { K, C } = H, ink = C.line;
    // after "it.": the snip; the halves drop off the cushion, the tag flutters down, the Scientist grins
    const pedestal = `<rect x="860" y="600" width="200" height="330" fill="${C.cream}" stroke="${ink}" stroke-width="5"/>` +
      `<rect x="830" y="570" width="260" height="36" fill="${C.cream}" stroke="${ink}" stroke-width="5"/><rect x="830" y="926" width="260" height="30" fill="${C.cream}" stroke="${ink}" stroke-width="5"/>` +
      [895, 940, 985, 1030].map((x) => `<path d="M${x},612 V918" stroke="#D8CCAE" stroke-width="6"/>`).join("");
    const cushion = `<path d="M820,572 Q830,526 960,522 Q1090,526 1100,572 Z" fill="${C.war}" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M836,572 l-10,22 M1084,572 l10,22" stroke="${C.yellow}" stroke-width="5" stroke-linecap="round"/>`;
    // each half: half the glow, half the orbits and half the orange nucleus, its cut face glowing yellow
    const half = (x, y, rot, side) => {
      const clip = side < 0 ? "M-200,-200 H0 V200 H-200 Z" : "M0,-200 H200 V200 H0 Z";
      return `<g transform="translate(${x},${y}) rotate(${rot})"><clipPath id="atomhalf${side}"><path d="${clip}"/></clipPath><g clip-path="url(#atomhalf${side})">` +
        `<circle cx="0" cy="0" r="120" fill="${C.yellow}" opacity="0.3"/>` + K.atom(0, 0, 110, C.line) +
        `<circle cx="0" cy="0" r="46" fill="${C.orange}" stroke="${ink}" stroke-width="5"/><circle cx="${-side * 16}" cy="-14" r="12" fill="${C.yellow}"/></g>` +
        `<path d="M0,-46 V46" stroke="${C.yellow}" stroke-width="9" stroke-linecap="round"/></g>`;
    };
    const sparks = [[-20, -60], [30, -90], [0, -130], [-50, -110], [50, -40]].map(([dx, dy]) => star(960 + dx, 470 + dy, 18, C.yellow)).join("");
    const tag = `<g transform="rotate(18 980 360)"><path d="M980,300 q-10,-30 -40,-40" fill="none" stroke="${ink}" stroke-width="3"/>` +
      `<path d="M900,300 H1060 V370 H900 L880,335 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="4"/><circle cx="902" cy="335" r="6" fill="none" stroke="${ink}" stroke-width="3"/>` +
      H.label(985, 349, 34, "DO NOT CUT", "middle", C.war) + "</g>";
    // the Scientist with the giant shears, just closed over the cushion
    const SCI = K.castOpts("scientist", { mood: "grin", arms: [[70, 92], [60, 84]] });
    const RS = K.rig(SCI), ks = 2.4, sx = 470, sfeet = 960, oy = sfeet - 100 * ks;
    const hx = sx + ks * (RS.hand[0][0] + RS.hand[1][0]) / 2, hy = oy + ks * (RS.hand[0][1] + RS.hand[1][1]) / 2;
    const shears = `<path d="M${f(hx + 30)},${f(hy - 6)} L960,540 L${f(hx + 60)},${f(hy + 6)} Z" fill="#AEB6C2" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
      `<path d="M${f(hx + 40)},${f(hy + 8)} L960,552 L${f(hx + 70)},${f(hy + 22)} Z" fill="#C9CED6" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
      `<circle cx="${f(hx + 6)}" cy="${f(hy - 18)}" r="26" fill="none" stroke="${C.war}" stroke-width="11"/><circle cx="${f(hx + 18)}" cy="${f(hy + 26)}" r="26" fill="none" stroke="${C.war}" stroke-width="11"/>`;
    const sci = stand(sx, sfeet, ks, K.person(SCI));
    const svg = field(760) + pedestal + cushion + half(880, 470, -34, -1) + half(1045, 476, 30, 1) + sparks + tag + sci + shears;
    return { svg, alt: "On a plain field, the giant shears have just closed over a red velvet cushion on a pedestal: the glowing atom falls apart into two halves, sparks fly, a tag reading DO NOT CUT flutters down, and the Scientist in her lab coat and glasses grins at the snip." };
  },

  "my-surprise"(H) {
    const { K } = H, S = K.STUDIO;
    // the crash zoom on "surprise"
    const svg = push(S, 1.5, H.host("surprised-oh", "open-palms", planetsTray(H, H.C, true)));
    return { svg, alt: "A crash zoom on Wishonia's face at her lectern: eyes wide, mouth an O, surprised." };
  },

  "pointing-at-each-other"(H) {
    const { K, C } = H, ink = C.line;
    // on "That's": the cloud thinned away; both neighbors charred and smoking, still aiming over the fence
    const houses = at(420, 690, 1.25, K.burn(K.props.house({ variant: 0, smoke: false }))) + at(1500, 690, 1.25, K.burn(K.props.house({ variant: 1, smoke: false })));
    const puffs = [[760, 300, 90], [960, 240, 120], [1170, 300, 90], [880, 380, 70], [1060, 380, 70]].map(([x, y, rr]) => `<circle cx="${x}" cy="${y}" r="${rr}" fill="#E9E1CF" opacity="0.45"/>`).join("");
    const A = { tone: 1, outfit: "shirt", color: 2, hair: 0, seed: 21, charred: true, arms: [[70, 92], [62, 86]] };
    const B = { tone: 3, outfit: "shirt", color: 1, hair: 0, seed: 22, charred: true, look: "left", arms: [[-62, -86], [-70, -92]] };
    const k = 2.2, feet = 960;
    const left = stand(640, feet, k, K.person(A)), right = stand(1290, feet, k, K.person(B));
    const post = `<rect x="944" y="700" width="32" height="260" fill="${K.mix ? C.cream : C.cream}" stroke="${ink}" stroke-width="4"/>`;
    const tst = at(960, 704, 1.1, K.burn(toaster(C, "#2A1E14")));
    const svg = field(700) + houses + puffs + fence(C, 760, 1160, 960, 170) + post + tst + left + right;
    return { svg, alt: "In front of two charred ranch houses, two neighbors stand either side of a picket fence, charred black and smoking with their hair straight up and only their white eyes showing, still aiming at each other; the last of the mushroom cloud thins away over them and a charred toaster sits on the fence post." };
  },

  "fire-on-fire"(H) {
    const { K, C } = H, ink = C.line;
    // on "yourself": both cavemen on fire all over, running round the campfire
    const sky = `<rect width="1920" height="1080" fill="${SKY}"/>`;
    const hill = `<path d="M-20,1080 V380 L180,250 L520,170 L980,130 L1420,180 L1760,260 L1940,360 V1080 Z" fill="${C.tan}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>` +
      `<path d="M260,300 L420,260 M1500,240 L1660,300 M700,200 L820,180" stroke="#8C5E3C" stroke-width="6" stroke-linecap="round"/>`;
    const mouth = `<path d="M420,1080 V640 L540,420 L760,330 L1160,330 L1380,420 L1500,640 V1080 Z" fill="#2A2420" stroke="${ink}" stroke-width="6" stroke-linejoin="round"/>`;
    const ground = `<rect y="900" width="1920" height="180" fill="#A88A5E"/><path d="M0,900 H1920" stroke="${ink}" stroke-width="4"/>`;
    const logs = `<g stroke="${ink}" stroke-width="5"><rect x="840" y="880" width="240" height="34" rx="16" fill="${C.rust}" transform="rotate(12 960 897)"/><rect x="840" y="880" width="240" height="34" rx="16" fill="${C.rust}" transform="rotate(-12 960 897)"/></g>`;
    const fire = K.flames(960, 890, 1.6);
    const PELT = "#C99A5B";
    const spots = `<g fill="${C.rust}" opacity="0.8"><ellipse cx="-8" cy="10" rx="5" ry="4"/><ellipse cx="9" cy="24" rx="4" ry="3"/><ellipse cx="-4" cy="36" rx="5" ry="3.5"/></g>`;
    // small flames on the head, the shoulders, the raised hands and the back, so the yelling faces still show
    const burning = (o) => {
      const R = K.rig(o);
      return K.flames(R.top[0] + 6, R.top[1] + 10, 0.62) + K.flames(R.shoulder[0][0] - 8, R.shoulder[0][1] + 12, 0.45) + K.flames(R.shoulder[1][0] + 8, R.shoulder[1][1] + 12, 0.45) +
        K.flames(R.hand[0][0], R.hand[0][1] + 6, 0.38) + K.flames(R.hand[1][0], R.hand[1][1] + 6, 0.38) + K.flames(-22, R.hipY + 10, 0.6);
    };
    const man = (o) => burning(o) + K.person(o) + spots;
    const A = { tone: 0, outfit: "shirt", colorHex: PELT, hair: 0, seed: 41, mood: "eager", arms: [[150, 170], [-150, -170]] };
    const B = { tone: 2, outfit: "shirt", colorHex: PELT, hair: 0, seed: 42, mood: "eager", look: "left", arms: [[140, 175], [-140, -175]] };
    const svg = sky + hill + mouth + ground + logs + fire + stand(600, 960, 2.2, `<g transform="rotate(-8 0 100)">${man(A)}</g>`) + stand(1320, 960, 2.2, `<g transform="rotate(8 0 100)">${man(B)}</g>`) +
      [[520, 700], [1420, 700]].map(([x, y]) => `<path d="M${x},${y} q-40,-30 -80,-10 M${x},${y + 40} q-50,-20 -90,10" fill="none" stroke="${C.cream}" stroke-width="5" stroke-linecap="round" opacity="0.7"/>`).join("");
    return { svg, alt: "At the mouth of a dark cave, beside a campfire, two cavemen in spotted pelts are on fire all over, arms up, yelping, running round the fire." };
  },

  "earth-means-dirt"(H) {
    const { K, C } = H, S = K.STUDIO, ink = C.line;
    // on "want...": the shrug, the tab corrected, the marker hovering by it
    const marker = `<g transform="translate(1440,400) rotate(38)"><rect x="-14" y="-80" width="28" height="110" rx="6" fill="${C.war}" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="-14" y="-80" width="28" height="30" rx="6" fill="${C.cream}" stroke="${ink}" stroke-width="4"/><path d="M-10,30 L0,52 L10,30 Z" fill="${C.war}" stroke="${ink}" stroke-width="3"/></g>`;
    const front = planetsTray(H, C, false) + caseFile(H, K, C, { ticks: true, stamp: true, tab: "dirt" }) + marker;
    const svg = push(S, 1.07, H.host("skeptical-closed", "shrug", front));
    return { svg, alt: "Wishonia at her lectern shrugs, skeptical; on the case file propped on the lectern, EARTH on the tab is crossed out in red marker and DIRT written above it, the marker hovering beside it." };
  },

  "pentagon"(H) {
    const { K, C } = H, ink = C.line;
    // after "Square": the pull back on the row: the Pentagon, RECTANGLE, SQUARE and TRIANGLE
    const g = 840;
    // the five-sided building, seen from a little above: its roof (an outer pentagon over an inner courtyard) on walls
    const pent = (cx, cy, rx, ry) => [...Array(5)].map((_, i) => { const a = -Math.PI / 2 + (i * 2 * Math.PI) / 5; return [cx + rx * Math.cos(a), cy + ry * Math.sin(a)]; });
    const O = pent(330, 640, 230, 120), I = pent(330, 640, 92, 48);
    const P = (pts) => pts.map((p) => `${f(p[0])},${f(p[1])}`).join(" ");
    const walls = [2, 3].map((i) => { const a = O[i], b = O[(i + 1) % 5]; return `<polygon points="${f(a[0])},${f(a[1])} ${f(b[0])},${f(b[1])} ${f(b[0])},${f(b[1] + 90)} ${f(a[0])},${f(a[1] + 90)}" fill="#D8CCAE" stroke="${ink}" stroke-width="4"/>`; }).join("") +
      [1, 4].map((i) => { const a = O[i], b = O[(i + (i === 1 ? 1 : -1) + 5) % 5]; return `<polygon points="${f(a[0])},${f(a[1])} ${f(b[0])},${f(b[1])} ${f(b[0])},${f(b[1] + 90)} ${f(a[0])},${f(a[1] + 90)}" fill="#C4B693" stroke="${ink}" stroke-width="4"/>`; }).join("");
    const win = [...Array(9)].map((_, i) => `<rect x="${170 + i * 36}" y="${790 - (i < 4.5 ? 0 : 0)}" width="16" height="22" fill="${C.slate}"/>`).join("");
    const building = walls + `<polygon points="${P(O)}" fill="${C.cream}" stroke="${ink}" stroke-width="5"/><polygon points="${P(I)}" fill="#6E8E5A" stroke="${ink}" stroke-width="4"/>` + win;
    const sign = (x, text, w = 1) => at(x, g + 70, w, K.props.sign({ text, height: 60, fontSize: 34 }));
    const drips = [-70, -20, 40, 80].map((dx, i) => `<path d="M${330 + dx},${g - 10} v${16 + i * 7}" stroke="${C.war}" stroke-width="7" stroke-linecap="round"/>`).join("");
    const hospital = at(820, g, 0.95, K.props.hospital({ label: "RECTANGLE" }));
    // the square school with its bell
    const sx = 1300, sw = 300;
    let school = `<rect x="${sx - sw / 2}" y="${g - sw}" width="${sw}" height="${sw}" fill="#D9A55A" stroke="${ink}" stroke-width="5"/>` +
      `<path d="M${sx - sw / 2 - 14},${g - sw} H${sx + sw / 2 + 14}" stroke="${ink}" stroke-width="10"/>` +
      `<path d="M${sx - 34},${g - sw - 4} V${g - sw - 70} H${sx + 34} V${g - sw - 4} M${sx - 46},${g - sw - 70} L${sx},${g - sw - 110} L${sx + 46},${g - sw - 70} Z" fill="${C.rust}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
      `<path d="M${sx - 12},${g - sw - 20} Q${sx - 12},${g - sw - 50} ${sx},${g - sw - 50} Q${sx + 12},${g - sw - 50} ${sx + 12},${g - sw - 20} Z" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/>` +
      `<rect x="${sx - 30}" y="${g - 110}" width="60" height="110" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>`;
    for (let r = 0; r < 2; r++) for (let c = 0; c < 4; c++) if (!(r === 1 && (c === 1 || c === 2))) school += `<rect x="${sx - 120 + c * 64}" y="${g - 260 + r * 90}" width="46" height="56" fill="#8FB3B0" stroke="${ink}" stroke-width="3"/>`;
    // the triangle doghouse and the Democracy Dog in its door
    const dx = 1700;
    const dog = `<polygon points="${dx - 130},${g} ${dx},${g - 230} ${dx + 130},${g}" fill="${C.war}" stroke="${ink}" stroke-width="5" stroke-linejoin="round"/>` +
      `<path d="M${dx - 54},${g} V${g - 70} A54,54 0 0,1 ${dx + 54},${g - 70} V${g} Z" fill="#2A2420" stroke="${ink}" stroke-width="4"/>` +
      at(dx - 10, g + 2, 1.05, K.props.democracyDog({ face: "front", tail: "plain", mood: "smile" }));
    const puff = [[300, 610, 26], [330, 596, 32], [362, 612, 24]].map(([x, y, rr]) => `<circle cx="${x}" cy="${y}" r="${rr}" fill="#E9E1CF" stroke="${ink}" stroke-width="3"/>`).join("");
    const svg = field(g) + building + puff + drips + sign(330, "THE PENTAGON", 1) + hospital + school + sign(sx, "SQUARE", 1) + dog + sign(dx, "TRIANGLE", 0.9);
    return { svg, alt: "A row of four buildings on a plain field: a plain five-sided building with a green courtyard and a dripping freshly painted sign THE PENTAGON; a rectangle hospital whose cornice reads RECTANGLE; a square school with a bell, SQUARE; and a triangle doghouse, TRIANGLE, with the Democracy Dog smiling out of its door." };
  },

  "papers-with-presidents"(H) {
    const { K, C } = H, ink = C.line;
    // on "money,": every head snapped toward the paper, all but the bored human at the far left
    const g = 960;
    let pav = `<rect width="1920" height="1080" fill="#D6C49A"/><rect y="560" width="1920" height="520" fill="#C9B58A"/><path d="M0,560 H1920" stroke="${GROUND_EDGE}" stroke-width="4"/>`;
    for (let y = 600; y < 1080; y += 70) pav += `<path d="M0,${y} H1920" stroke="#B79F72" stroke-width="3"/>`;
    for (let y = 600, row = 0; y < 1080; y += 70, row++) for (let x = row % 2 ? 60 : 0; x < 1920; x += 120) pav += `<path d="M${x},${y} v70" stroke="#B79F72" stroke-width="3"/>`;
    const facade = `<rect x="0" y="200" width="1920" height="360" fill="#E6D7B4"/><path d="M0,200 H1920" stroke="${ink}" stroke-width="4"/>` +
      [...Array(8)].map((_, i) => `<rect x="${80 + i * 240}" y="270" width="110" height="160" fill="${C.slate}" stroke="${ink}" stroke-width="4"/><rect x="${70 + i * 240}" y="430" width="130" height="14" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>`).join("");
    const lamp = `<path d="M1620,${g} V380" stroke="${ink}" stroke-width="12"/><path d="M1590,${g} h60" stroke="${ink}" stroke-width="14"/><path d="M1585,380 L1600,330 H1640 L1655,380 Z" fill="${C.yellow}" stroke="${ink}" stroke-width="4"/>`;
    const CROWD = [
      { o: { tone: 0, outfit: "suit", color: 0, seed: 1 }, x: 380 },
      { o: { tone: 2, outfit: "dress", color: 1, hair: 1, seed: 2 }, x: 520 },
      { o: { tone: 1, outfit: "shirt", color: 3, seed: 3 }, x: 650 },
      { o: { tone: 3, outfit: "overalls", color: 2, seed: 4 }, x: 790 },
      { o: { tone: 0, outfit: "dress", color: 2, hair: 1, seed: 5 }, x: 920 },
      { o: { tone: 2, outfit: "suit", color: 3, seed: 6 }, x: 1050 },
      { o: { tone: 1, outfit: "shirt", color: 1, hair: 2, seed: 7 }, x: 1180 },
      { o: { tone: 3, outfit: "dress", color: 0, hair: 1, seed: 8 }, x: 1310 },
    ];
    const k = 1.85;
    const crowd = CROWD.map((m, i) => stand(m.x, g - (i % 2) * 18, k, K.person(copy(m.o, { look: "right", mood: "eager" })))).join("") +
      CROWD.map((m, i) => `<path d="M${m.x - 60},${g - 330 - (i % 2) * 18} q-20,10 -36,4 M${m.x - 64},${g - 300 - (i % 2) * 18} q-20,8 -30,2" fill="none" stroke="${C.cream}" stroke-width="5" stroke-linecap="round"/>`).join("");
    const bored = stand(170, g, k, K.person({ tone: 2, outfit: "shirt", color: 0, seed: 9, look: "left", mood: "flat" }));
    const paper = bill(K, 1520, g - 4, 2.0, "plain", 0.6);
    const svg = pav + facade + lamp + bored + crowd + paper;
    return { svg, alt: "In a plain town square, a crowd of eight everyday humans have all snapped their heads to the right toward one little paper bill standing on stick legs; one bored human at the far left keeps staring at the ground." };
  },

  "without-with-papers"(H) {
    const { K, C } = H, ink = C.line;
    // after "this).": the bomb has gone off in the Weapons Maker's face; he keeps hammering, grinning, charred
    const g = 930;
    const bench = `<rect x="560" y="700" width="620" height="40" fill="${C.tan}" stroke="${ink}" stroke-width="5"/><rect x="590" y="740" width="30" height="${g - 740}" fill="${C.rust}" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="1120" y="740" width="30" height="${g - 740}" fill="${C.rust}" stroke="${ink}" stroke-width="4"/><rect x="600" y="840" width="540" height="18" fill="${C.rust}" stroke="${ink}" stroke-width="4"/>`;
    const cloud = at(1430, 700, 0.62, K.nuke());
    const newBomb = at(760, 700, 1.5, K.props.bomb({ face: "grin" }));
    const WM = K.castOpts("weaponsMaker", { charred: true, arms: [[40, 70], [150, 200]] });
    const R = K.rig(WM), k = 2.3, wx = 1000, oy = g - 100 * k;
    const hand = [wx + k * R.hand[1][0], oy + k * R.hand[1][1]];
    const hammer = `<g transform="translate(${f(hand[0])},${f(hand[1])}) rotate(-30)"><rect x="-6" y="-90" width="12" height="96" fill="${C.tan}" stroke="${ink}" stroke-width="3"/><rect x="-30" y="-112" width="60" height="28" rx="4" fill="${C.slate}" stroke="${ink}" stroke-width="4"/></g>`;
    const grin = `<path d="M${f(wx + k * (R.mouth ? R.mouth[0] : 6) - 20)},${f(oy + k * (R.mouth ? R.mouth[1] : -20))} q20,16 40,0" fill="#FFFFFF" stroke="${ink}" stroke-width="2.5"/>`;
    const man = stand(wx, g, k, K.person(WM)) + grin + hammer;
    const bills = [[480, 0.9, 0.2], [620, 1, 0.8], [1240, 1, 0.3], [1380, 0.9, 0.7], [1520, 1, 0.1], [360, 0.9, 0.6]].map(([x, s, l]) => bill(K, x, g + 4, s * 1.3, "war", l)).join("");
    const svg = field(640) + cloud + bench + newBomb + man + bills + wisps(wx - 10, oy - 30, 2);
    return { svg, alt: "At a workbench, the Weapons Maker stands charred black and smoking from the bomb that just went off in his face, hard hat on, grinning, hammer raised to keep working; a little mushroom cloud rises behind him, a new grinning bomb pops onto the bench, and war-seal papers stand round his boots." };
  },

  "604-papers"(H) {
    const { K, C } = H, ink = C.line;
    // after "work.": the war paper standing on the flattened medicine paper at the foot of the stack
    const g = 880;
    const clouds = [[260, 240, 1], [1560, 170, 0.8]].map(([x, y, s]) => at(x, y, s, `<path d="M-120,30 Q-120,-20 -70,-20 Q-50,-70 0,-60 Q40,-90 80,-50 Q130,-50 130,0 Q150,30 110,40 H-100 Q-130,40 -120,30 Z" fill="#FBF6E6" stroke="${ink}" stroke-width="4"/>`)).join("");
    const stack = at(700, g, 1.6, billStack(K, C, 24, 1, 5, "war"));
    const flat = `<g transform="translate(1100,${g}) scale(1.6,0.34)">${K.money("med", 0).replace('class="legs"', 'class="legs" opacity="0"')}</g>`;
    const top = bill(K, 1104, g - 6, 1.6, "war", 0.5);
    const arm = `<path d="M1176,${g - 6} l22,-10 l10,-24" fill="none" stroke="${ink}" stroke-width="5" stroke-linecap="round"/><circle cx="1210" cy="${g - 44}" r="7" fill="${C.cream}" stroke="${ink}" stroke-width="3"/>` +
      `<path d="M1222,${g - 56} q8,-6 14,0 M1224,${g - 40} q10,0 14,6" fill="none" stroke="${ink}" stroke-width="2.5" stroke-linecap="round"/>`;
    const svg = field(g) + clouds + stack + flat + top + arm + H.big(1360, 380, 190, "604 : 1", "middle", C.navy);
    return { svg, alt: "On a plain field, a stack of green war-seal papers rises out of the top of the frame; at its foot, one war paper stands on the flattened medicine paper, whose little arm pokes out from under it and waves weakly; 604 : 1 in big type in the sky." };
  },
};
