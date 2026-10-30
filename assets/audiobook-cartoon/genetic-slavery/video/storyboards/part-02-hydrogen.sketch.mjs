function sky(C) {
  return `<rect width="1920" height="1080" fill="${C.deep}"/>`;
}
export default {
  "low-expectations"(H) {
    const { C } = H;
    const svg = sky(C) +
      `<circle cx="700" cy="520" r="70" fill="${C.cream}" stroke="${C.line}" stroke-width="8"/>` +
      H.label(700, 530, 48, "H") +
      `<rect x="860" y="250" width="70" height="90" fill="${C.tan}" stroke="${C.line}" stroke-width="6"/>` +
      `<g transform="rotate(-8 1180 420)"><rect x="900" y="360" width="620" height="120" rx="8" fill="${C.cream}" stroke="${C.war}" stroke-width="8"/>` +
      H.label(1210, 440, 42, "LOW EXPECTATIONS", "middle", C.war) + `</g>` +
      `<g transform="translate(700,700)">${[0, 1, 2, 3, 4].map((i) => `<circle cx="${(i - 2) * 36}" cy="${i % 2 ? -20 : 10}" r="28" fill="${C.orange}" stroke="${C.line}" stroke-width="5"/>`).join("")}</g>`;
    return { svg, alt: "One hydrogen atom, a stamp reading LOW EXPECTATIONS, and a small clump already on fire." };
  },
  "called-stars"(H) {
    const { C } = H;
    const svg = sky(C) +
      `<g transform="translate(700,280)"><rect x="0" y="80" width="520" height="360" fill="${C.tan}" stroke="${C.line}" stroke-width="8"/><rect x="40" y="0" width="440" height="90" fill="${C.navy}" stroke="${C.cream}" stroke-width="6"/>` +
      H.label(260, 58, 42, "STARS", "middle", C.cream) +
      `<path d="M40,200 L180,80 L300,220 L480,60" fill="none" stroke="${C.war}" stroke-width="8"/>` +
      `<rect x="540" y="180" width="90" height="50" fill="${C.cream}" stroke="${C.line}" stroke-width="5"/>` +
      H.label(585, 214, 28, "C") +
      `<rect x="540" y="250" width="90" height="50" fill="${C.cream}" stroke="${C.line}" stroke-width="5"/>` +
      H.label(585, 284, 28, "O") + `</g>` +
      H.label(960, 860, 36, "IN", "middle", C.cream) + H.label(1500, 860, 36, "OUT, THEN THE ROOF", "middle", C.cream);
    return { svg, alt: "A factory with STARS on the roof, bars marked C and O leaving the side, and cracks in the wall." };
  },
  "fatality-rate"(H) {
    const { C } = H;
    const svg = sky(C) +
      `<g transform="translate(280,360)"><rect x="40" y="80" width="400" height="220" fill="${C.slate}" stroke="${C.line}" stroke-width="8" transform="rotate(-6 240 190)"/><rect x="80" y="20" width="300" height="70" fill="${C.navy}" transform="rotate(-18 230 50)"/>` +
      `<g transform="rotate(-8 360 200)"><rect x="60" y="140" width="560" height="110" fill="${C.cream}" stroke="${C.war}" stroke-width="8"/>` +
      H.label(340, 212, 36, "FATALITY RATE 100%", "middle", C.war) + `</g></g>` +
      `<rect x="1100" y="300" width="520" height="420" rx="8" fill="${C.cream}" stroke="${C.line}" stroke-width="8"/>` +
      H.label(1360, 380, 32, "ON THE JOB") +
      H.big(1360, 560, 64, "9,000,000,000", "middle", C.war) +
      H.label(1360, 640, 36, "YEARS");
    return { svg, alt: "A ruined factory with a stamp reading FATALITY RATE 100%, beside a calendar stopped at 9,000,000,000 YEARS." };
  },
};
