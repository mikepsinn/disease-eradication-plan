// Sketches for storyboards/part-01-opening.md: each scene's key moment as SVG on a 1920 x 1080 frame.
// Built into the review sheet by tools/storyboard-sheet.mjs. Coordinates follow the pilot's scenes:
// Wishonia's corner frame at (1760, 740), the desk top at y 905, captions below y 896.

const Q1 = ["1. Everyone you've ever loved: being", "slowly tortured and/or murdered by", "horrible diseases?"];
const Q2 = ["2. Enough nuclear bombs for", "122 nuclear winters?"];

function bulb(x, y, fill) {
  return `<g stroke="#1B1B1B" stroke-width="4"><circle cx="${x}" cy="${y}" r="30" fill="${fill}"/><rect x="${x - 14}" y="${y + 26}" width="28" height="22" fill="#F3EAD3"/><path d="M${x - 14},${y + 34} h28 M${x - 14},${y + 41} h28" stroke-width="2"/></g>`;
}
function atom(x, y, C) {
  const orbit = (r) => `<ellipse cx="${x}" cy="${y}" rx="44" ry="15" fill="none" stroke="${C.line}" stroke-width="3" transform="rotate(${r} ${x} ${y})"/>`;
  return `<circle cx="${x}" cy="${y}" r="58" fill="${C.war}" opacity="0.18"/><circle cx="${x}" cy="${y}" r="16" fill="${C.war}" stroke="${C.line}" stroke-width="3"/>` + orbit(0) + orbit(60) + orbit(120);
}
function flake(x, y, C) {
  return `<path d="M${x - 13},${y} H${x + 13} M${x - 6.5},${y - 11.3} L${x + 6.5},${y + 11.3} M${x - 6.5},${y + 11.3} L${x + 6.5},${y - 11.3}" stroke="${C.war}" stroke-width="3.2" stroke-linecap="round"/>`;
}
function flame(x, y, s, C, id) {
  return `<g transform="translate(${x},${y}) scale(${s})"><path d="M0,0 C-34,-10 -30,-60 -8,-96 C-6,-70 10,-62 14,-84 C34,-56 40,-14 0,0 Z" fill="${C.war}" stroke="${C.line}" stroke-width="4"/><path d="M0,0 C-34,-10 -30,-60 -8,-96 C-6,-70 10,-62 14,-84 C34,-56 40,-14 0,0 Z" fill="url(#${id}-hred)"/></g>`;
}
function sign(cx, y, text, H, C) {
  const w = text.length * 26 + 70;
  return `<path d="M${cx - w / 2 + 30},${y + 70} v70 M${cx + w / 2 - 30},${y + 70} v70" stroke="${C.line}" stroke-width="7"/>` +
    `<rect x="${cx - w / 2}" y="${y}" width="${w}" height="74" fill="#FBF5E4" stroke="${C.line}" stroke-width="5"/>` + H.label(cx, y + 52, 40, text);
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
    const svg = K.office(960) +
      H.big(960, 330, 150, "HOW TO END") + H.big(960, 490, 150, "WAR AND DISEASE") +
      `<text x="960" y="585" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="64" fill="${C.cream}" stroke="${C.ink}" stroke-width="8" style="paint-order:stroke">(for Busy People)</text>` +
      `<rect x="250" y="640" width="1420" height="84" rx="42" fill="${C.navy}" stroke="${C.ink}" stroke-width="5"/>` +
      H.text(960, 696, 42, ["A Step-by-Step Guide to Optimizing Your Terrible Civilization"], { anchor: "middle", fill: C.cream, weight: 700 });
    return { svg, alt: "Title card on the sunburst: HOW TO END WAR AND DISEASE (for Busy People), with the subtitle on a navy band." };
  },

  "loved-ones"(H, id) {
    const { K, C } = H;
    const family = [0, 1, 2, 3].map((t, i) => H.at(330 + i * 110, 540, 0.95, K.bean({ tone: t, light: "red", mouth: "smile", hair: i % 3, look: "camera", mood: "smile" }))).join("");
    const svg = K.paper(id) + H.board(116.3) +
      `<rect x="170" y="290" width="600" height="360" fill="${C.line}"/><rect x="190" y="310" width="560" height="320" fill="#FBF5E4"/><rect x="190" y="310" width="560" height="320" fill="url(#${id}-fine)" opacity="0.35"/>` + family +
      `<rect x="110" y="650" width="720" height="40" fill="url(#${id}-cross)" stroke="${C.line}" stroke-width="5"/><rect x="140" y="690" width="660" height="150" fill="url(#${id}-hatch)" stroke="${C.line}" stroke-width="5"/>` +
      H.form(880, 150, 820, "PLANET ELIGIBILITY CHECK", [{ lines: Q1, yes: true }], { size: 36 }) +
      H.at(1200, 480, 1, K.pencil()) +
      H.pip(id, "sad-closed") + H.cap("brutally murdered by horrible diseases?", "diseases");
    return { svg, alt: "A family portrait of four smiling bean humans on a mantel, every chest light red; the Planet Eligibility Check form with question 1 ticked YES; the countdown board in the corner; Wishonia sad in the corner frame." };
  },

  "nuclear-winters"(H, id) {
    const { K, C } = H;
    let flakes = "";
    for (let i = 0; i < 122; i++) flakes += flake(1190 + (i % 11) * 40, 200 + Math.floor(i / 11) * 44, C);
    const land = `<path d="M930,500 q30,-40 70,-20 q30,30 10,60 q-40,20 -60,0 Z M1010,600 q40,-10 60,20 q-10,40 -50,30 Z" fill="url(#${id}-hatch)" stroke="${C.line}" stroke-width="3"/>`;
    const svg = K.paper(id) + H.board(126.9) +
      H.form(110, 200, 720, "PLANET ELIGIBILITY CHECK", [{ lines: Q1, yes: true }, { lines: Q2, yes: true }], { size: 30 }) +
      `<circle cx="1000" cy="560" r="110" fill="#FBF5E4" stroke="${C.line}" stroke-width="6"/>` + land +
      H.label(1000, 730, 40, "CIVILIZATIONS: 1") + flakes + H.label(1390, 760, 40, "NUCLEAR WINTERS: 122", "middle", C.war) +
      H.pip(id, "thinking-closed") + H.cap("only having the one civilization to apocalypse?", "apocalypse");
    return { svg, alt: "The form with questions 1 and 2 ticked YES; one small Earth labeled Civilizations: 1 beside a grid of 122 red snowflakes labeled Nuclear winters: 122." };
  },

  "eligible"(H) {
    const { K, C } = H;
    const mini = H.at(150, 250, 0.62, H.form(0, 0, 820, "PLANET ELIGIBILITY CHECK", [{ lines: Q1, yes: true }, { lines: Q2, yes: true }], { size: 30 }));
    const folder = `<g transform="rotate(-3 900 740)"><path d="M620,610 h150 l20,-30 h120 l20,30 h340 v270 h-650 Z" fill="#E2B865" stroke="${C.ink}" stroke-width="6"/>` +
      H.label(850, 603, 22, "EARTH: CASE #847", "middle", C.ink) +
      `<g transform="rotate(-8 950 760)"><rect x="700" y="690" width="500" height="140" fill="none" stroke="${C.red}" stroke-width="7"/><rect x="712" y="702" width="476" height="116" fill="none" stroke="${C.red}" stroke-width="2.5"/>` +
      H.label(950, 752, 46, "MAY BE ELIGIBLE", "middle", C.red) + H.label(950, 806, 46, "FOR OPTIMIZATION", "middle", C.red) + "</g></g>";
    const stamp = `<g stroke="${C.ink}" stroke-width="6"><rect x="1080" y="470" width="150" height="40" rx="6" fill="${C.red}"/><rect x="1130" y="400" width="50" height="74" fill="#B65A2B"/><circle cx="1155" cy="388" r="34" fill="${C.ink}"/></g>`;
    const svg = K.office(1460) + K.wallScreen(110, 214, 640, 420) + mini + H.board(131) +
      H.wish(1200, 100, 600, "happy-smile", "palms-down") + K.desk(1080, 905, 820) + H.at(1760, 800, 1.5, K.mug(0, 0)) +
      folder + stamp + H.cap("your planet may be eligible for optimization.", "eligible");
    return { svg, alt: "The office: the eligibility form is on the wall screen; on the desk the Earth case file is stamped MAY BE ELIGIBLE FOR OPTIMIZATION; Wishonia smiles with the stamp lifted." };
  },

  "meet-wishonia"(H) {
    const { K, C } = H;
    const screen = H.label(520, 320, 40, "UPGRADING CIVILIZATIONS") + H.big(520, 425, 100, "4,297 years") +
      `<circle cx="330" cy="560" r="74" fill="#FBF5E4" stroke="${C.ink}" stroke-width="6"/>` +
      [...Array(9)].map((_, i) => { const a = Math.PI * (0.8 + i * 0.175); return `<path d="M${330 + 60 * Math.cos(a)},${560 + 60 * Math.sin(a)} L${330 + 70 * Math.cos(a)},${560 + 70 * Math.sin(a)}" stroke="${C.ink}" stroke-width="3"/>`; }).join("") +
      `<path d="M330,560 L374,516" stroke="${C.red}" stroke-width="6" stroke-linecap="round"/><circle cx="330" cy="560" r="8" fill="${C.ink}"/>` +
      H.label(640, 540, 30, "IN EARTH TIME") + H.big(640, 620, 64, "4,297 years");
    const plate = `<rect x="1130" y="790" width="500" height="106" rx="6" fill="#B65A2B" stroke="${C.ink}" stroke-width="6"/><rect x="1150" y="804" width="460" height="78" rx="4" fill="${C.yellow}" stroke="${C.ink}" stroke-width="3"/>` +
      H.label(1380, 842, 36, "WISHONIA LOVE", "middle", C.ink) + H.text(1380, 870, 19, ["CEO and President, Universe Optimization Services"], { anchor: "middle", fill: C.ink, weight: 600 });
    const svg = K.office(1420) + K.wallScreen(110, 190, 820, 520) + screen + H.board(144) +
      H.wish(1080, 70, 660, "smirk-smile", "open-palms") + K.desk(1000, 905, 900) + H.at(1780, 800, 1.5, K.mug(0, 0)) + plate +
      H.cap("which in your Earth time is four thousand, two hundred and ninety-seven years.", "earth");
    return { svg, alt: "Wishonia behind the desk with open palms and a smirk; a brass nameplate reads WISHONIA LOVE, CEO and President, Universe Optimization Services; the wall screen shows 4,297 years and a converter dial showing 4,297 years in Earth time." };
  },

  "split-the-atom"(H, id) {
    const { K, C } = H;
    const card = `<g transform="rotate(-6 330 250)"><rect x="150" y="190" width="300" height="120" fill="#FBF5E4" stroke="${C.line}" stroke-width="4"/>${H.label(300, 240, 30, "ATOM (GREEK):")}${H.text(300, 285, 26, ["unable to be"], { anchor: "middle", weight: 600 })}</g>` +
      `<g transform="rotate(8 610 260)"><rect x="470" y="205" width="260" height="120" fill="#FBF5E4" stroke="${C.line}" stroke-width="4"/>${H.text(600, 285, 26, ["cut"], { anchor: "middle", weight: 600 })}</g>` +
      `<path d="M458,170 l16,30 l-14,26 l18,28 l-12,30 l14,32" fill="none" stroke="${C.line}" stroke-width="3" stroke-dasharray="7 6"/>` +
      `<g stroke="${C.line}" stroke-width="5" fill="none"><circle cx="790" cy="170" r="20"/><circle cx="790" cy="228" r="20"/><path d="M806,182 L880,214 M806,216 L880,184"/></g>`;
    const bulbs = [...Array(7)].map((_, i) => bulb(560 + i * 130, 420, `url(#${id}-cross)`)).join("");
    const svg = K.paper(id) + H.board(170) + H.big(1330, 220, 120, "1945") + card + bulbs +
      H.at(640, 680, 1.5, K.bean({ tone: 0, light: "off", mouth: "flat", brows: true, arms: [[16, 8], [90, 90]] })) +
      H.at(1280, 680, 1.5, K.bean({ tone: 2, light: "off", mouth: "flat", brows: true, arms: [[-90, -90], [-16, -8]] })) +
      atom(820, 668, C) + atom(1100, 668, C) +
      H.pip(id, "surprised-oh") + H.cap("you were just pointing it at each other!", "pointing");
    return { svg, alt: "1945; a dictionary card reading ATOM (Greek): unable to be cut, cut in two by scissors; a row of dark light bulbs; two frowning bean humans each point a glowing red atom at the other." };
  },

  "fire-on-fire"(H, id) {
    const { K, C } = H;
    const cave = `<path d="M40,1040 V420 Q200,120 520,90 H1400 Q1720,120 1880,420 V1040 Z M240,1040 V520 Q360,250 640,230 H1280 Q1560,250 1680,520 V1040 Z" fill="url(#${id}-cross)" fill-rule="evenodd" stroke="${C.line}" stroke-width="5"/>`;
    const logs = `<g stroke="${C.line}" stroke-width="5"><rect x="700" y="770" width="240" height="34" rx="16" fill="#FBF5E4" transform="rotate(14 820 787)"/><rect x="700" y="770" width="240" height="34" rx="16" fill="#FBF5E4" transform="rotate(-14 820 787)"/></g>`;
    const svg = K.paper(id) + cave + `<path d="M240,820 H1680" stroke="${C.line}" stroke-width="5"/>` + H.board(178) +
      logs + flame(820, 770, 1.6, C, id) +
      H.at(1180, 700, 1.6, K.bean({ tone: 3, light: "off", mouth: "o", brows: true, arms: [[-135, -160], [-60, -100]] })) +
      flame(1092, 668, 0.42, C, id) +
      H.pip(id, "eyeroll-closed") + H.cap("using it to set yourself on fire.", "fire");
    return { svg, alt: "Inside a cross-hatched cave a campfire burns; a bean human beside it has a small flame on a raised sleeve and an open, surprised mouth." };
  },

  "earth-means-dirt"(H) {
    const { K, C } = H;
    const callout = `<rect x="640" y="330" width="560" height="190" rx="8" fill="${C.cream}" stroke="${C.ink}" stroke-width="6"/>` +
      `<text x="680" y="470" font-family="Oswald" font-weight="600" font-size="80" fill="${C.ink}">EARTH</text>` +
      `<path d="M672,442 H900" stroke="${C.red}" stroke-width="10" stroke-linecap="round"/>` +
      `<text x="912" y="470" font-family="Oswald" font-weight="600" font-size="44" fill="${C.ink}">: CASE #847</text>` +
      `<text x="730" y="400" font-family="Fraunces" font-weight="900" font-size="76" fill="${C.red}" transform="rotate(-6 730 400)">DIRT</text>` +
      `<path d="M640,500 L560,420" stroke="${C.ink}" stroke-width="5" stroke-dasharray="10 8"/>`;
    const svg = K.office(1420) + H.at(200, 330, 1.55, K.cabinet(0, 0)) + callout + H.board(188) +
      H.wish(1100, 80, 640, "skeptical-closed", "shrug") + K.desk(1000, 905, 900) + H.at(1780, 800, 1.5, K.mug(0, 0)) +
      H.cap("Okay, if that's what you want...", "want");
    return { svg, alt: "Wishonia shrugs behind the desk; a close-up of the case-file label shows EARTH crossed out in red and DIRT written above it." };
  },

  "pentagon"(H, id) {
    const { K, C } = H;
    const pent = (r) => [...Array(5)].map((_, i) => { const a = -Math.PI / 2 + (i * 2 * Math.PI) / 5; return `${(420 + r * Math.cos(a)).toFixed(1)},${(590 + r * Math.sin(a)).toFixed(1)}`; }).join(" ");
    const windows = (x0, y0, cols, rows, s) => { let w = ""; for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) w += `<rect x="${x0 + c * s}" y="${y0 + r * s}" width="${s * 0.6}" height="${s * 0.6}" fill="url(#${id}-hatch)" stroke="${C.line}" stroke-width="2.5"/>`; return w; };
    const svg = K.paper(id) + H.board(200) + `<path d="M100,790 H1600" stroke="${C.line}" stroke-width="5"/>` +
      `<polygon points="${pent(190)}" fill="url(#${id}-hatch)" stroke="${C.line}" stroke-width="6"/><polygon points="${pent(170)}" fill="none" stroke="${C.line}" stroke-width="2"/><polygon points="${pent(78)}" fill="#FBF5E4" stroke="${C.line}" stroke-width="5"/>` +
      sign(420, 230, "THE PENTAGON", H, C) +
      `<rect x="760" y="410" width="400" height="380" fill="#FBF5E4" stroke="${C.line}" stroke-width="6"/>` + windows(796, 446, 5, 4, 72) +
      `<rect x="920" y="700" width="80" height="90" fill="${C.line}"/><circle cx="960" cy="380" r="34" fill="${C.med}" stroke="${C.line}" stroke-width="4"/>${H.label(960, 393, 38, "H", "middle", "#FBF5E4")}` +
      sign(960, 230, "RECTANGLE", H, C) +
      `<rect x="1260" y="490" width="300" height="300" fill="#FBF5E4" stroke="${C.line}" stroke-width="6"/>` + windows(1294, 526, 4, 3, 66) +
      `<rect x="1380" y="710" width="60" height="80" fill="${C.line}"/>` + sign(1410, 310, "SQUARE", H, C) +
      H.pip(id, "smirk-smile") + H.cap("or calling a school “Square”.", "square");
    return { svg, alt: "Three plain buildings with signs: a five-sided plan labeled THE PENTAGON, a rectangle hospital labeled RECTANGLE, and a square school labeled SQUARE." };
  },

  "papers-with-presidents"(H, id) {
    const { K, C } = H;
    let crowd = "";
    for (let i = 0; i < 9; i++) crowd += H.at(230 + (i % 3) * 150 + Math.floor(i / 3) * 40, 520 + Math.floor(i / 3) * 110, 1.05, K.bean({ tone: i % 4, light: "off", mouth: i % 2 ? "o" : "flat", hair: i % 3, arms: [[30, 30], [60, 70]], look: "right", mood: i % 3 === 1 ? "smile" : "eager" }));
    const banner = `<path d="M210,130 H1610 l-40,70 l40,70 H210 l40,-70 Z" fill="#FBF5E4" stroke="${C.line}" stroke-width="5"/>` +
      H.label(910, 190, 44, "MONEY") + H.text(910, 244, 32, ["pretend value that becomes real value if everyone pretends hard enough"], { anchor: "middle", weight: 600 });
    const trail = `<path d="M880,620 C960,560 1040,600 1110,590" fill="none" stroke="${C.line}" stroke-width="4" stroke-dasharray="12 10"/>`;
    const svg = K.paper(id) + H.board(216) + banner + crowd + trail + H.at(1260, 590, 2.4, H.plainMoney(0.7)) +
      H.pip(id, "thinking-small") + H.cap("These papers are called “money,”", "money");
    return { svg, alt: "A crowd of bean humans turned toward one plain paper bill walking away on stick legs; the banner defines MONEY as pretend value that becomes real value if everyone pretends hard enough." };
  },

  "without-with-papers"(H, id) {
    const { K, C } = H;
    const left = `<rect x="150" y="300" width="170" height="130" fill="#FBF5E4" stroke="${C.line}" stroke-width="5"/><circle cx="235" cy="350" r="24" fill="${C.med}" stroke="${C.line}" stroke-width="3"/>${H.label(235, 362, 28, "H", "middle", "#FBF5E4")}` +
      `<path d="M400,300 h40 v50 l40,80 h-120 l40,-80 Z" fill="#FBF5E4" stroke="${C.line}" stroke-width="5"/><path d="M372,410 h96" stroke="${C.med}" stroke-width="14"/>` +
      [...Array(7)].map((_, i) => `<path d="M${560 + i * 30},440 v-110" stroke="${C.line}" stroke-width="3"/><ellipse cx="${560 + i * 30}" cy="322" rx="8" ry="18" fill="url(#${id}-hatch)" stroke="${C.line}" stroke-width="2.5"/>`).join("") +
      H.at(330, 560, 0.9, K.bean({ tone: 1, light: "off", mouth: "flat" })) + H.at(520, 560, 0.9, K.bean({ tone: 3, light: "off", mouth: "flat", hair: 1 })) +
      ["Save lives", "Cure diseases", "Feed hungry people"].map((t, i) => H.cross(150, 660 + i * 64, 44) + H.text(214, 696 + i * 64, 38, [t], { weight: 700 })).join("");
    const bills = [[1080, 300], [1220, 340], [1370, 300], [1160, 420], [1310, 430]].map(([x, y], i) => H.at(x, y, 0.85, K.money("war", i % 2 ? 0.8 : 0.2))).join("");
    const right = bills +
      `<circle cx="1500" cy="470" r="46" fill="${C.line}"/><path d="M1530,436 q20,-30 44,-26" fill="none" stroke="${C.line}" stroke-width="5"/><rect x="1430" y="510" width="80" height="36" fill="#FBF5E4" stroke="${C.line}" stroke-width="3" transform="rotate(-10 1470 528)"/>${H.label(1470, 538, 22, "$$$", "middle", C.war)}` +
      `<rect x="1040" y="480" width="260" height="140" fill="#FBF5E4" stroke="${C.line}" stroke-width="4"/><path d="M1070,590 q60,-80 120,-40 M1170,520 l20,30 l14,-36 Z" fill="none" stroke="${C.war}" stroke-width="7"/>` +
      ["Build bombs", "Start wars", "Destroy the planet"].map((t, i) => H.tick(1040, 654 + i * 64, 48, C.war) + H.text(1110, 696 + i * 64, 38, [t], { weight: 700 })).join("");
    const svg = K.paper(id) + H.board(245) +
      `<path d="M960,140 V860 M970,140 V860" stroke="${C.line}" stroke-width="3"/>` +
      H.label(480, 230, 54, "WITHOUT PAPERS") + H.label(1440, 230, 54, "WITH PAPERS", "middle", C.war) + left + right +
      H.pip(id, "eyeroll-smile") + H.cap("Destroy the planet (surprisingly profitable in papers).", "profitable");
    return { svg, alt: "Split screen. Left, WITHOUT PAPERS: a hospital, a lab and a wheat field with idle humans, and Save lives, Cure diseases, Feed hungry people crossed out. Right, WITH PAPERS: red bills rushing in, a bomb with a price tag and a war map, and Build bombs, Start wars, Destroy the planet ticked in red." };
  },

  "604-papers"(H, id) {
    const { K, C } = H;
    const svg = K.paper(id) + H.board(256) +
      `<rect x="700" y="150" width="200" height="672" fill="${C.war}" stroke="${C.line}" stroke-width="5"/><rect x="700" y="150" width="200" height="672" fill="url(#${id}-hred)"/>` +
      [...Array(28)].map((_, i) => `<path d="M700,${174 + i * 24} H900" stroke="${C.line}" stroke-width="1.6"/>`).join("") +
      H.at(800, 138, 2.08, K.money("war")) + H.at(1160, 797, 1, K.money("med")) +
      `<path d="M120,822 H1600" stroke="${C.line}" stroke-width="5"/>` +
      H.label(800, 872, 44, "WEAPONS", "middle", C.war) + H.label(1160, 872, 34, "TESTING WHICH MEDICINES WORK", "middle", "#157F78") +
      H.big(1330, 470, 170, "604 : 1") +
      H.pip(id, "sideeye-closed") + H.cap("for every one paper on testing which medicines work.", "work");
    return { svg, alt: "The 604 bar: a tall red stack of bills labeled WEAPONS next to one small teal bill labeled TESTING WHICH MEDICINES WORK, with 604 : 1 in big type." };
  },
};
