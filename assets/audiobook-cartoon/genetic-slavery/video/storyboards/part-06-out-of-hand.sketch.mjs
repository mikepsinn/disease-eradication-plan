function sky(C) {
  return `<rect width="1920" height="1080" fill="${C.deep}"/>`;
}
export default {
  "nothing-about-it"(H) {
    const { K, C } = H;
    const svg = sky(C) +
      `<rect x="200" y="220" width="700" height="520" fill="${C.navy}" stroke="${C.cream}" stroke-width="8"/>` +
      `<ellipse cx="420" cy="400" rx="160" ry="60" fill="none" stroke="${C.yellow}" stroke-width="6" transform="rotate(-20 420 400)"/>` +
      `<circle cx="620" cy="340" r="30" fill="${C.orange}"/>` +
      `<g transform="translate(1280,500)"><circle r="90" fill="${C.cream}" stroke="${C.line}" stroke-width="8"/><circle cx="-28" cy="-16" r="18" fill="${C.navy}"/><circle cx="28" cy="-16" r="18" fill="${C.navy}"/><path d="M0,8 l-14,22 h28 z" fill="${C.navy}"/><path d="M-36,48 h72 M-24,48 v22 M-8,48 v22 M8,48 v22 M24,48 v22" fill="none" stroke="${C.line}" stroke-width="6"/></g>` +
      H.at(1500, 560, 1.1, K.person({ tone: 3, mood: "flat" }));
    return { svg, alt: "A chalkboard with an orbit, a skull on the desk, and a person shrugging at it." };
  },
  "looked-funny"(H) {
    const { K, C } = H;
    const svg = sky(C) +
      `<rect x="240" y="240" width="760" height="480" fill="${C.cream}" stroke="${C.line}" stroke-width="8"/>` +
      `<path d="M280,300 C500,700 800,200 960,640" fill="none" stroke="${C.war}" stroke-width="28" stroke-linecap="round" opacity="0.85"/>` +
      `<rect x="1180" y="180" width="220" height="120" rx="8" fill="${C.yellow}" stroke="${C.line}" stroke-width="6" transform="rotate(20 1290 240)"/>` +
      H.label(1290, 250, 24, "CORTISOL", "middle", C.war) +
      H.at(1500, 520, 1.15, K.person({ tone: 5, mood: "flat", look: "left" }));
    return { svg, alt: "A chalkboard wiped by a splash from a bucket labeled CORTISOL. One person stands in the doorway, only looking." };
  },
  "no-license"(H) {
    const { C } = H;
    const svg = sky(C) + `<rect y="860" width="1920" height="220" fill="${C.tan}"/>` +
      `<g transform="translate(360,480)"><rect width="1100" height="320" rx="24" fill="${C.yellow}" stroke="${C.line}" stroke-width="8"/><rect x="40" y="40" width="240" height="120" fill="${C.peri}"/><rect x="320" y="40" width="240" height="120" fill="${C.peri}"/><rect x="600" y="40" width="240" height="120" fill="${C.peri}"/></g>` +
      `<ellipse cx="520" cy="620" rx="80" ry="32" fill="${C.med}" stroke="${C.line}" stroke-width="6"/>` +
      H.label(520, 560, 26, "SURVIVE") +
      H.label(800, 560, 26, "LOVED") +
      H.label(1080, 560, 26, "UNDERSTAND") +
      `<g transform="translate(430,900) rotate(-12)"><rect width="180" height="70" fill="${C.cream}" stroke="${C.war}" stroke-width="4"/><path d="M10,10 L170,60" stroke="${C.war}" stroke-width="6"/></g>` +
      `<g transform="translate(700,920) rotate(8)"><rect width="180" height="70" fill="${C.cream}" stroke="${C.war}" stroke-width="4"/><path d="M10,10 L170,60" stroke="${C.war}" stroke-width="6"/></g>` +
      `<rect x="500" y="760" width="140" height="70" fill="${C.cream}" stroke="${C.line}" stroke-width="4"/>` +
      H.label(570, 804, 22, "KEYS");
    return { svg, alt: "One car, three riders labeled SURVIVE, LOVED, and UNDERSTAND. Two torn licenses on the floor. The keys are with the lizard in front." };
  },
  "out-of-hand"(H) {
    const { C } = H;
    const svg = sky(C) +
      `<g transform="translate(1280,280)"><rect width="280" height="70" rx="8" fill="${C.tan}" stroke="${C.line}" stroke-width="6"/><polygon points="280,8 360,35 280,62" fill="${C.war}" stroke="${C.line}" stroke-width="6"/><rect x="40" y="70" width="28" height="90" fill="${C.orange}" stroke="${C.line}" stroke-width="4"/></g>` +
      `<rect x="1180" y="560" width="200" height="340" rx="16" fill="${C.navy}" stroke="${C.cream}" stroke-width="6"/>` +
      H.label(1280, 700, 28, "NO", "middle", C.war) +
      H.label(1280, 760, 28, "NO", "middle", C.war) +
      `<circle cx="460" cy="700" r="90" fill="${C.cream}" stroke="${C.line}" stroke-width="8"/>` +
      H.label(460, 716, 48, "H") +
      `<g transform="translate(600,640) rotate(-18)"><rect x="-8" y="0" width="16" height="150" rx="4" fill="${C.tan}" stroke="${C.line}" stroke-width="4"/><ellipse cx="0" cy="-8" rx="22" ry="30" fill="${C.orange}" stroke="${C.line}" stroke-width="4"/><ellipse cx="0" cy="-24" rx="10" ry="16" fill="${C.yellow}"/></g>` +
      `<rect x="760" y="180" width="420" height="120" fill="${C.cream}" stroke="${C.line}" stroke-width="8"/>` +
      H.big(970, 265, 72, "NOBODY");
    return { svg, alt: "One hydrogen atom holding a lit match. Behind it, a phone argument and a missile. A sign reads NOBODY." };
  },
};
