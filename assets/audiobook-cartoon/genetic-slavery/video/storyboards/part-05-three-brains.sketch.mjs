function sky(C) {
  return `<rect width="1920" height="1080" fill="${C.deep}"/><rect y="880" width="1920" height="200" fill="${C.tan}"/>`;
}
export default {
  "lizard-brain"(H) {
    const { C } = H;
    const row = (y, word) => `<rect x="980" y="${y}" width="46" height="46" rx="4" fill="${C.cream}" stroke="${C.line}" stroke-width="4"/>` +
      `<path d="M990,${y + 24} l12,12 l24,-28" fill="none" stroke="${C.med}" stroke-width="6"/>` +
      H.label(1050, y + 36, 36, word, "start", C.cream);
    const svg = sky(C) +
      `<g transform="translate(420,620)"><ellipse cx="0" cy="40" rx="220" ry="80" fill="${C.med}" stroke="${C.line}" stroke-width="8"/><circle cx="150" cy="-10" r="70" fill="${C.med}" stroke="${C.line}" stroke-width="8"/><circle cx="170" cy="-20" r="8" fill="${C.line}"/></g>` +
      `<rect x="250" y="760" width="420" height="30" fill="${C.navy}"/>` +
      row(280, "BREATHE") + row(360, "EAT") + row(440, "FIGHT") + row(520, "FLEE");
    return { svg, alt: "A lizard in a driver's seat. A checklist beside it, breathe, eat, fight, flee, every box already ticked." };
  },
  "still-running"(H) {
    const { C } = H;
    const svg = sky(C) +
      `<g transform="translate(520,640)"><ellipse cx="0" cy="40" rx="200" ry="70" fill="${C.med}" stroke="${C.line}" stroke-width="8"/><circle cx="140" cy="0" r="60" fill="${C.med}" stroke="${C.line}" stroke-width="8"/></g>` +
      `<path d="M1120,500 C1120,450 1190,430 1220,480 C1250,430 1320,450 1320,500 C1320,570 1220,650 1220,650 C1220,650 1120,570 1120,500 Z" fill="${C.war}" stroke="${C.line}" stroke-width="8"/>` +
      `<rect x="980" y="680" width="520" height="80" rx="8" fill="${C.cream}" stroke="${C.line}" stroke-width="6"/>` +
      H.label(1240, 732, 28, "WITHOUT YOUR PERMISSION");
    return { svg, alt: "The lizard still at the wheel. A heart with a hang-tag that says WITHOUT YOUR PERMISSION." };
  },
  "nursery-depot"(H) {
    const { C } = H;
    const svg = sky(C) +
      `<rect x="480" y="620" width="960" height="200" fill="${C.tan}" stroke="${C.line}" stroke-width="8"/>` +
      H.label(960, 730, 42, "MISSILES", "middle", C.war) +
      `<rect x="620" y="360" width="680" height="260" fill="${C.cream}" stroke="${C.line}" stroke-width="8"/>` +
      `<rect x="700" y="470" width="200" height="100" rx="8" fill="${C.yellow}" stroke="${C.line}" stroke-width="6"/>` +
      `<ellipse cx="1120" cy="560" rx="50" ry="24" fill="${C.navy}"/>` +
      `<rect x="860" y="280" width="360" height="70" fill="${C.med}" stroke="${C.line}" stroke-width="6"/>` +
      H.label(1040, 328, 28, "GENUINE UPGRADE", "middle", C.cream);
    return { svg, alt: "A pastel nursery, crib and dog bowl, built on a crate stenciled MISSILES. A sign on the crib says GENUINE UPGRADE." };
  },
  "already-committed"(H) {
    const { K, C } = H;
    const svg = sky(C) +
      `<rect x="180" y="300" width="260" height="260" rx="130" fill="${C.war}" stroke="${C.line}" stroke-width="10"/>` +
      `<rect x="290" y="520" width="40" height="80" fill="${C.line}"/>` +
      H.label(310, 660, 28, "DOWN", "middle", C.cream) +
      H.at(1100, 520, 1.2, K.person({ tone: 1, mood: "flat" })) +
      `<rect x="1240" y="700" width="220" height="140" fill="${C.tan}" stroke="${C.line}" stroke-width="6"/>` +
      H.label(1350, 780, 28, "THINKING") +
      H.text(1280, 830, 24, ["blank paper"], { fill: C.line });
    return { svg, alt: "A large red button already pressed. A figure labeled THINKING is still arriving, briefcase full of blank paper." };
  },
};
