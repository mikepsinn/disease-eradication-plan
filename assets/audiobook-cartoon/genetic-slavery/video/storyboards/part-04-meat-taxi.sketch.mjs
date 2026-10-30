function sky(C) {
  return `<rect width="1920" height="1080" fill="${C.deep}"/>`;
}
export default {
  "anxious-meeting"(H) {
    const { C } = H;
    const svg = sky(C) +
      `<circle cx="200" cy="120" r="6" fill="${C.cream}"/><circle cx="420" cy="80" r="4" fill="${C.cream}"/><circle cx="700" cy="140" r="5" fill="${C.cream}"/>` +
      `<rect x="620" y="640" width="200" height="40" fill="${C.tan}"/><rect x="680" y="560" width="80" height="90" fill="${C.navy}"/>` +
      `<circle cx="760" cy="500" r="70" fill="${C.yellow}" stroke="${C.line}" stroke-width="8"/>` +
      H.label(760, 512, 40, "H") +
      `<rect x="860" y="220" width="900" height="220" rx="28" fill="${C.cream}" stroke="${C.line}" stroke-width="6"/>` +
      H.label(1310, 320, 32, "WHY AM I ANXIOUS ABOUT") +
      H.label(1310, 380, 32, "A MEETING TOMORROW?") +
      `<rect x="1040" y="470" width="560" height="90" rx="16" fill="${C.cream}" stroke="${C.line}" stroke-width="6"/>` +
      H.label(1320, 528, 28, "ANXIETY COPIED BETTER");
    return { svg, alt: "A hydrogen atom in an office chair looking up at the stars, asking why it is anxious about a meeting tomorrow. A smaller balloon answers that anxiety copied better." };
  },
  "meat-taxi"(H) {
    const { K, C } = H;
    const svg = sky(C) + `<rect y="860" width="1920" height="220" fill="${C.tan}"/>` +
      `<g transform="translate(480,560)"><rect x="0" y="80" width="720" height="220" rx="20" fill="${C.yellow}" stroke="${C.line}" stroke-width="8"/><rect x="60" y="110" width="200" height="90" fill="${C.peri}" stroke="${C.line}" stroke-width="6"/><rect x="300" y="110" width="200" height="90" fill="${C.peri}" stroke="${C.line}" stroke-width="6"/><circle cx="160" cy="300" r="40" fill="${C.navy}"/><circle cx="560" cy="300" r="40" fill="${C.navy}"/>` +
      `<rect x="250" y="-70" width="220" height="70" rx="8" fill="${C.navy}"/>` + H.label(360, -22, 36, "MEAT", "middle", C.cream) + `</g>` +
      H.at(640, 760, 1, `<rect x="-28" y="-80" width="56" height="70" rx="8" fill="${C.med}" stroke="${C.line}" stroke-width="4"/><rect x="-8" y="-96" width="16" height="20" fill="${C.cream}" stroke="${C.line}" stroke-width="3"/>`) +
      H.at(900, 700, 0.55, K.person({ tone: 2, mood: "sad", look: "left" }));
    return { svg, alt: "A taxi with MEAT on the roof sign, a flask in the driver's seat, and a person in the back." };
  },
  "bad-renovation"(H) {
    const { C } = H;
    const floor = (y, fill, n) => `<rect x="560" y="${y}" width="800" height="200" fill="${fill}" stroke="${C.line}" stroke-width="8"/>` + H.label(620, y + 50, 32, n, "start", C.line);
    const svg = sky(C) + floor(640, C.tan, "1") + floor(440, C.cream, "2") + floor(240, C.yellow, "3") +
      `<path d="M700,840 V280 M900,840 V360 M1100,840 V300" fill="none" stroke="${C.war}" stroke-width="14" stroke-linecap="round"/>`;
    return { svg, alt: "A three-story building cut open. The pipes from the first floor run straight up through the rooms above." };
  },
};
