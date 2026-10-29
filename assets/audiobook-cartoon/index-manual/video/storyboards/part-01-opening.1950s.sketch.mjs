// A 1950s educational-film version of five Part 1 scenes, to compare with the current look:
//   node tools/storyboard-sheet.mjs storyboards/part-01-opening.md --alt storyboards/part-01-opening.1950s.sketch.mjs
// Same key moments, layouts and words as part-01-opening.sketch.mjs; only the look changes.

// The theme song music video's palette.
const P = {
  navy: "#24304E", ink: "#1E1A1A", cream: "#F3E9D2", wall: "#E9D9B6", orange: "#D97A2B",
  mustard: "#E4B24A", teal: "#3E8C86", red: "#B8432F", blue: "#8FAFC4", brown: "#8B5A3C",
};

// Film grain, vignette, two scratches and the rounded corners of the projector gate.
function film(id) {
  return `<defs><radialGradient id="${id}-vig" cx="50%" cy="50%" r="72%"><stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#2A1A0A" stop-opacity="0.55"/></radialGradient>` +
    `<pattern id="${id}-grain" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="2" r="0.9" fill="#000" opacity="0.12"/><circle cx="5" cy="5.5" r="0.8" fill="#fff" opacity="0.12"/></pattern></defs>` +
    `<rect width="1920" height="1080" fill="url(#${id}-grain)"/><rect width="1920" height="1080" fill="url(#${id}-vig)"/>` +
    `<path d="M412,0 V1080" stroke="${P.cream}" stroke-width="2" opacity="0.22"/><path d="M1487,0 V1080" stroke="${P.ink}" stroke-width="1.5" opacity="0.18"/>` +
    `<path fill-rule="evenodd" fill="#0E0B08" d="M0,0 H1920 V1080 H0 Z M70,0 H1850 Q1920,0 1920,70 V1010 Q1920,1080 1850,1080 H70 Q0,1080 0,1010 V70 Q0,0 70,0 Z"/>`;
}
// The atomic-age four-point star.
function star(x, y, r, color, n = 4) {
  const pts = [];
  for (let i = 0; i < n * 2; i++) {
    const a = (Math.PI * i) / n - Math.PI / 2, rr = i % 2 ? r * 0.2 : r;
    pts.push(`${(x + rr * Math.cos(a)).toFixed(1)},${(y + rr * Math.sin(a)).toFixed(1)}`);
  }
  return `<polygon points="${pts.join(" ")}" fill="${color}"/>`;
}
function boomerang(x, y, s, color, rot = 0) {
  return `<path transform="translate(${x},${y}) rotate(${rot}) scale(${s})" d="M0,0 Q40,-55 100,-34 Q52,-22 32,22 Q22,6 0,0 Z" fill="${color}"/>`;
}
// Plain white subtitles, as a 1950s film would print them.
function cap(text) {
  const words = text.split(" "), lines = [[]];
  for (const w of words) {
    if ((lines[lines.length - 1].join(" ") + w).length > 50) lines.push([]);
    lines[lines.length - 1].push(w);
  }
  return lines.map((l, i) => `<text x="960" y="${1020 - (lines.length - 1 - i) * 56}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="46" fill="${P.cream}" stroke="${P.ink}" stroke-width="9" stroke-linejoin="round" style="paint-order:stroke">${l.join(" ").replace(/&/g, "&amp;").replace(/</g, "&lt;")}</text>`).join("");
}
function recolor(svg) {
  return svg.replace(/#D7322B/g, P.red).replace(/#8E1C17/g, "#7A2618").replace(/#1FA39A/g, P.teal).replace(/#0E5F59/g, "#22524E").replace(/#F3EAD3/g, P.cream).replace(/#FBF5E4/g, P.cream);
}
// Wishonia's corner frame as a 1950s television set.
function tv(H, id, head) {
  return `<defs><clipPath id="${id}-tv"><rect x="1618" y="612" width="200" height="164" rx="36"/></clipPath><linearGradient id="${id}-tvsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${P.blue}"/><stop offset="1" stop-color="#5E7F96"/></linearGradient></defs>` +
    `<path d="M1705,592 l-46,-62 M1735,592 l42,-66" stroke="${P.ink}" stroke-width="5" stroke-linecap="round"/>` +
    `<rect x="1596" y="590" width="292" height="250" rx="26" fill="${P.brown}" stroke="${P.ink}" stroke-width="6"/>` +
    `<rect x="1610" y="604" width="216" height="180" rx="42" fill="${P.ink}"/>` +
    `<g clip-path="url(#${id}-tv)"><rect x="1618" y="612" width="200" height="164" fill="url(#${id}-tvsky)"/>${H.wish(1640, 620, 156, head, "idle")}</g>` +
    `<circle cx="1856" cy="648" r="14" fill="${P.mustard}" stroke="${P.ink}" stroke-width="4"/><circle cx="1856" cy="700" r="14" fill="${P.mustard}" stroke="${P.ink}" stroke-width="4"/>` +
    `<path d="M1846,760 h22 M1846,772 h22" stroke="${P.ink}" stroke-width="3"/>`;
}
// The countdown board as a cream tally card.
function board(H, t) {
  const n = String(Math.floor((t * 104) / 60)).padStart(6, "0");
  let digits = "";
  for (let i = 0; i < 6; i++) digits += `<rect x="${22 + i * 48}" y="58" width="42" height="52" rx="5" fill="${P.navy}"/><text x="${43 + i * 48}" y="98" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="40" fill="${P.mustard}">${n[i]}</text>`;
  return `<g transform="translate(78,64)"><rect x="0" y="0" width="330" height="126" rx="14" fill="${P.cream}" stroke="${P.ink}" stroke-width="5"/>` +
    H.label(165, 28, 15, "HUMANS TERMINATED BY CURABLE DISEASES", "middle", P.ink) + H.label(165, 47, 15, "SINCE THIS FILM STARTED", "middle", P.ink) + digits + "</g>";
}
function shadowText(x, y, size, text, fill = P.cream, shadow = P.orange, anchor = "middle") {
  const t = (dx, dy, f) => `<text x="${x + dx}" y="${y + dy}" text-anchor="${anchor}" font-family="Fraunces" font-weight="900" font-size="${size}" fill="${f}">${text}</text>`;
  return t(size * 0.04, size * 0.06, shadow) + t(0, 0, fill);
}

const Q1 = ["1. Everyone you've ever loved: being", "slowly tortured and/or murdered by", "horrible diseases?"];

export default {
  label: "1950s educational film",
  dek: "The same five scenes drawn as a cheerful 1950s classroom film, to match the narrator's voice and the music video.",
  notes: [
    "**Palette** from the theme song music video: navy, orange, mustard, cream, with brick red and muted teal for the two kinds of money.",
    "**Earth scenes** become flat cut-paper shapes on colored walls and floors, with atomic stars and boomerangs, in place of the engraving.",
    "**The office** becomes a classroom set: a pull-down screen on a roller bar, a starburst clock and a kidney-shaped desk, in place of the 1970s sunburst.",
    "**Wishonia's corner frame** becomes a 1950s television set.",
    "**Film effects:** grain, a vignette, scratches and the rounded corners of a projector gate. The opening card names the film and the reel, so the episode can be cut into reels.",
    "**Plain white subtitles**, as a film of the time would print them.",
    "**The same** Wishonia sprites, bean humans, papers, layouts and words.",
  ],
  scenes: {
    "title-card"(H, id) {
      const svg = `<rect width="1920" height="1080" fill="${P.navy}"/>` +
        star(300, 230, 80, P.mustard) + star(1640, 270, 54, P.cream) + star(1500, 840, 44, P.mustard) + star(420, 860, 30, P.cream) +
        boomerang(150, 640, 1.6, P.orange, -20) + boomerang(1660, 560, 1.3, P.orange, 160) +
        H.label(960, 200, 34, "A WISHONIA OPTIMIZATION SERVICES FILM", "middle", P.mustard, 'letter-spacing="7"') +
        shadowText(960, 390, 150, "How to End") + shadowText(960, 540, 150, "War and Disease") +
        `<path d="M620,590 H1300 l-36,40 l36,40 H620 l36,-40 Z" fill="${P.mustard}"/>` + H.label(960, 648, 50, "(FOR BUSY PEOPLE)", "middle", P.navy) +
        H.label(960, 760, 32, "A STEP-BY-STEP GUIDE TO OPTIMIZING YOUR TERRIBLE CIVILIZATION", "middle", P.cream, 'letter-spacing="3"') +
        H.label(960, 880, 26, "REEL 1 · OPENING", "middle", P.mustard, 'letter-spacing="6"') + film(id);
      return { svg, alt: "A navy title card with atomic stars and boomerangs: A Wishonia Optimization Services Film, How to End War and Disease, (for Busy People) on a mustard ribbon, Reel 1, Opening." };
    },

    "loved-ones"(H, id) {
      const { K } = H;
      const family = [0, 1, 2, 3].map((t, i) => H.at(330 + i * 110, 520, 0.95, recolor(K.bean({ tone: t, light: "red", mouth: "smile", hair: i % 3 })))).join("");
      const svg = `<rect width="1920" height="1080" fill="${P.wall}"/><rect y="760" width="1920" height="320" fill="${P.navy}"/>` +
        `<rect x="860" y="120" width="880" height="420" fill="${P.teal}"/>` + star(1780, 600, 40, P.orange) + star(120, 180, 34, P.orange) +
        `<rect x="170" y="270" width="600" height="360" rx="8" fill="${P.brown}"/><rect x="194" y="294" width="552" height="312" fill="${P.cream}"/>` + family +
        `<rect x="110" y="640" width="720" height="34" rx="6" fill="${P.orange}"/><path d="M180,674 l-20,86 M760,674 l20,86" stroke="${P.ink}" stroke-width="8"/>` +
        recolor(H.form(880, 150, 820, "PLANET ELIGIBILITY CHECK", [{ lines: Q1, yes: true }], { size: 36 })) +
        H.at(1200, 480, 1, recolor(K.pencil())) + board(H, 116.3) + tv(H, id, "sad-closed") +
        cap("brutally murdered by horrible diseases?") + film(id);
      return { svg, alt: "A cut-paper living room: a family portrait of four smiling bean humans with red chest lights above an orange mantel, the eligibility form on a teal block with YES ticked, a tally card and Wishonia on a 1950s TV set." };
    },

    "meet-wishonia"(H, id) {
      const dial = `<circle cx="330" cy="560" r="74" fill="${P.cream}" stroke="${P.ink}" stroke-width="6"/>` +
        [...Array(9)].map((_, i) => { const a = Math.PI * (0.8 + i * 0.175); return `<path d="M${330 + 60 * Math.cos(a)},${560 + 60 * Math.sin(a)} L${330 + 70 * Math.cos(a)},${560 + 70 * Math.sin(a)}" stroke="${P.ink}" stroke-width="3"/>`; }).join("") +
        `<path d="M330,560 L374,516" stroke="${P.red}" stroke-width="6" stroke-linecap="round"/><circle cx="330" cy="560" r="8" fill="${P.ink}"/>`;
      const screen = `<rect x="100" y="150" width="840" height="26" rx="13" fill="${P.brown}" stroke="${P.ink}" stroke-width="4"/><rect x="120" y="176" width="800" height="520" fill="${P.cream}" stroke="${P.ink}" stroke-width="4"/>` +
        `<path d="M520,696 v40" stroke="${P.ink}" stroke-width="3"/><circle cx="520" cy="746" r="10" fill="none" stroke="${P.ink}" stroke-width="3"/>` +
        H.label(520, 300, 40, "UPGRADING CIVILIZATIONS", "middle", P.navy) + shadowText(520, 410, 100, "4,297 years", P.navy, P.mustard) +
        dial + H.label(640, 540, 30, "IN EARTH TIME", "middle", P.navy) + shadowText(640, 620, 64, "4,297 years", P.navy, P.mustard);
      const clock = star(1800, 150, 90, P.mustard, 6) + `<circle cx="1800" cy="150" r="40" fill="${P.cream}" stroke="${P.ink}" stroke-width="4"/><path d="M1800,150 V122 M1800,150 L1822,160" stroke="${P.ink}" stroke-width="5" stroke-linecap="round"/>`;
      const desk = `<path d="M980,905 Q980,850 1100,846 H1800 Q1910,850 1910,905 Z" fill="${P.orange}" stroke="${P.ink}" stroke-width="6"/><rect x="1000" y="905" width="890" height="175" fill="#B9621F" stroke="${P.ink}" stroke-width="6"/>`;
      const plate = `<rect x="1130" y="790" width="500" height="106" rx="6" fill="${P.brown}" stroke="${P.ink}" stroke-width="6"/><rect x="1150" y="804" width="460" height="78" rx="4" fill="${P.mustard}" stroke="${P.ink}" stroke-width="3"/>` +
        H.label(1380, 842, 36, "WISHONIA LOVE", "middle", P.ink) + H.text(1380, 870, 19, ["CEO and President, Universe Optimization Services"], { anchor: "middle", fill: P.ink, weight: 600 });
      const svg = `<rect width="1920" height="1080" fill="${P.blue}"/><rect x="980" y="0" width="560" height="1080" fill="#7E9DB3"/><circle cx="1410" cy="330" r="250" fill="${P.mustard}" opacity="0.9"/>` +
        clock + screen + H.wish(1080, 70, 660, "smirk-smile", "open-palms") + desk + plate + board(H, 144) +
        cap("which in your Earth time is four thousand, two hundred and ninety-seven years.") + film(id);
      return { svg, alt: "A 1950s classroom set: a pull-down screen showing 4,297 years and a converter dial, a starburst clock, and Wishonia behind a kidney-shaped orange desk with the WISHONIA LOVE nameplate." };
    },

    "split-the-atom"(H, id) {
      const { K } = H;
      const orbit = (cx, cy, rx, ry, r, color, w) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${color}" stroke-width="${w}" transform="rotate(${r} ${cx} ${cy})"/>`;
      const bigAtom = orbit(960, 300, 210, 62, 0, P.mustard, 10) + orbit(960, 300, 210, 62, 60, P.mustard, 10) + orbit(960, 300, 210, 62, 120, P.mustard, 10) +
        `<circle cx="960" cy="300" r="40" fill="${P.orange}" stroke="${P.ink}" stroke-width="5"/>` + star(1210, 150, 30, P.cream) + star(700, 460, 22, P.cream);
      const smallAtom = (x, y) => `<circle cx="${x}" cy="${y}" r="56" fill="${P.red}" opacity="0.25"/><circle cx="${x}" cy="${y}" r="16" fill="${P.red}" stroke="${P.ink}" stroke-width="3"/>` + orbit(x, y, 44, 15, 0, P.cream, 3) + orbit(x, y, 44, 15, 60, P.cream, 3) + orbit(x, y, 44, 15, 120, P.cream, 3);
      const card = `<g transform="rotate(-6 1450 220)"><rect x="1330" y="170" width="250" height="100" fill="${P.cream}"/>${H.label(1455, 212, 26, "ATOM (GREEK):", "middle", P.navy)}${H.text(1455, 250, 22, ["unable to be"], { anchor: "middle", fill: P.navy, weight: 600 })}</g>` +
        `<g transform="rotate(8 1700 230)"><rect x="1600" y="185" width="190" height="100" fill="${P.cream}"/>${H.text(1695, 250, 22, ["cut"], { anchor: "middle", fill: P.navy, weight: 600 })}</g>`;
      const bulbs = [...Array(7)].map((_, i) => `<circle cx="${560 + i * 130}" cy="580" r="26" fill="#3A4666" stroke="${P.cream}" stroke-width="3"/><rect x="${547 + i * 130}" y="603" width="26" height="18" fill="${P.cream}"/>`).join("");
      const svg = `<rect width="1920" height="1080" fill="${P.navy}"/><rect y="800" width="1920" height="280" fill="#1B2440"/>` + bigAtom +
        shadowText(330, 350, 120, "1945") + card + bulbs + board(H, 170) +
        H.at(640, 720, 1.5, recolor(K.bean({ tone: 0, light: "off", mouth: "flat", brows: true, arms: [[16, 8], [90, 90]] }))) +
        H.at(1280, 720, 1.5, recolor(K.bean({ tone: 2, light: "off", mouth: "flat", brows: true, arms: [[-90, -90], [-16, -8]] }))) +
        smallAtom(820, 708) + smallAtom(1100, 708) + tv(H, id, "surprised-oh") +
        cap("you were just pointing it at each other!") + film(id);
      return { svg, alt: "An A Is for Atom style frame: a big mustard atom on navy, 1945, the cut dictionary card, a row of dark bulbs, and two bean humans pointing glowing red atoms at each other." };
    },

    "604-papers"(H, id) {
      const { K } = H;
      const svg = `<rect width="1920" height="1080" fill="${P.wall}"/><rect x="1010" y="170" width="700" height="520" fill="${P.orange}"/>` + star(1600, 260, 70, P.mustard) +
        `<rect y="822" width="1920" height="258" fill="${P.navy}"/>` +
        `<rect x="700" y="150" width="200" height="672" fill="${P.red}" stroke="${P.ink}" stroke-width="5"/>` +
        [...Array(28)].map((_, i) => `<path d="M700,${174 + i * 24} H900" stroke="${P.cream}" stroke-width="1.6" opacity="0.5"/>`).join("") +
        H.at(800, 138, 2.08, recolor(K.money("war"))) + H.at(1160, 797, 1, recolor(K.money("med"))) +
        H.label(800, 872, 44, "WEAPONS", "middle", P.cream) + H.label(1160, 872, 34, "TESTING WHICH MEDICINES WORK", "middle", "#9FD6CF") +
        shadowText(1360, 480, 170, "604 : 1", P.cream, P.navy) + board(H, 256) + tv(H, id, "sideeye-closed") +
        cap("for every one paper on testing which medicines work.") + film(id);
      return { svg, alt: "The 604 bar in flat 1950s colors: a brick-red stack labeled WEAPONS beside one teal bill labeled TESTING WHICH MEDICINES WORK, with 604 : 1 in cream on an orange block." };
    },
  },
};
