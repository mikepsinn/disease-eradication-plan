function plate(C) {
  return `<rect width="1920" height="1080" fill="${C.deep}"/><rect y="880" width="1920" height="200" fill="${C.tan}"/><rect y="880" width="1920" height="10" fill="${C.line}"/>`;
}
function atom(cx, cy, C) {
  const orbit = (r) => `<ellipse cx="${cx}" cy="${cy}" rx="150" ry="52" fill="none" stroke="${C.cream}" stroke-width="6" transform="rotate(${r} ${cx} ${cy})"/>`;
  return orbit(0) + orbit(60) + orbit(120) + `<circle cx="${cx}" cy="${cy}" r="28" fill="${C.orange}" stroke="${C.line}" stroke-width="6"/>`;
}

export default {
  "genetic-slavery-title"(H) {
    const { C } = H;
    const svg = `<rect width="1920" height="1080" fill="${C.deep}"/>` + atom(960, 300, C) +
      H.big(960, 640, 150, "GENETIC", "middle", C.cream) + H.big(960, 820, 150, "SLAVERY", "middle", C.cream);
    return { svg, alt: "Title card. An atom above the words GENETIC SLAVERY." };
  },
  "six-oh-four"(H) {
    const { K, C } = H;
    let stack = "";
    for (let i = 0; i < 8; i++) stack += H.at(560, 760 - i * 36, 2.4, K.money("war", 0));
    const svg = plate(C) + stack + H.at(1400, 760, 2.6, K.money("med", 0)) +
      H.big(560, 280, 180, "604", "middle", C.cream) + H.big(1400, 620, 120, "1", "middle", C.cream) +
      H.label(560, 960, 36, "WEAPONS", "middle", C.cream) + H.label(1400, 960, 36, "CURING DISEASE", "middle", C.cream) +
      `<g transform="translate(1180,90)"><rect x="0" y="0" width="520" height="90" rx="8" fill="${C.cream}" stroke="${C.line}" stroke-width="6"/>` +
      H.label(260, 58, 36, "POLITICAL PROBLEM") + `<path d="M30,20 L490,70 M490,20 L30,70" stroke="${C.war}" stroke-width="14" stroke-linecap="round"/></g>`;
    return { svg, alt: "A tall stack of war bills marked 604, one medicine bill marked 1, and a plaque reading POLITICAL PROBLEM crossed out." };
  },
  hardware(H) {
    const { K, C } = H;
    const rock = (x, y, rx, ry) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${C.tan}" stroke="${C.line}" stroke-width="6"/>`;
    const svg = plate(C) +
      `<g transform="translate(780,620)"><rect x="-200" y="-180" width="400" height="250" rx="16" fill="${C.tan}" stroke="${C.line}" stroke-width="8"/><rect x="-160" y="-150" width="320" height="150" rx="8" fill="${C.navy}"/>` +
      H.label(0, -60, 36, "SOFTWARE", "middle", C.cream) + `</g>` +
      `<g transform="translate(780,430)"><rect x="-230" y="-40" width="460" height="72" rx="6" fill="${C.cream}" stroke="${C.war}" stroke-width="6"/>` +
      H.label(0, 10, 32, "200,000 YEARS", "middle", C.war) + `</g>` +
      rock(560, 900, 70, 40) + rock(760, 910, 90, 44) + rock(980, 905, 60, 36) +
      H.at(1460, 620, 1.2, K.person({ tone: 4, mood: "cross", look: "left" })) +
      H.at(980, 700, 0.48, K.nuke());
    return { svg, alt: "A stone computer stamped 200,000 YEARS, three rocks, a stranger stepping back, and a mushroom cloud in front of the screen." };
  },
  "owners-manual"(H) {
    const { C } = H;
    const svg = plate(C) +
      `<g transform="translate(960,760)"><ellipse cx="-170" cy="0" rx="210" ry="110" fill="${C.cream}" stroke="${C.line}" stroke-width="8"/><ellipse cx="170" cy="0" rx="210" ry="110" fill="${C.cream}" stroke="${C.line}" stroke-width="8"/><path d="M-40,20 q40,50 80,0" fill="none" stroke="${C.line}" stroke-width="6"/></g>` +
      `<g transform="translate(760,470)"><rect width="400" height="220" rx="10" fill="${C.navy}" stroke="${C.cream}" stroke-width="8"/>` +
      H.big(200, 145, 100, "YOU", "middle", C.war) + `</g>`;
    return { svg, alt: "A brain on the floor with a book dropped on it. The cover says YOU." };
  },
  "universe-exploded"(H) {
    const { C } = H;
    const svg = `<rect width="1920" height="1080" fill="${C.deep}"/>` +
      `<circle cx="960" cy="460" r="18" fill="${C.yellow}" stroke="${C.line}" stroke-width="5"/>` +
      H.label(960, 560, 54, "NOTHING INTERESTING", "middle", C.cream) +
      H.label(960, 660, 48, "400,000,000 YEARS", "middle", C.cream);
    return { svg, alt: "One small spark in a dark field, the words NOTHING INTERESTING, and a counter at 400,000,000 YEARS." };
  },
};
