function sky(C) {
  return `<rect width="1920" height="1080" fill="${C.deep}"/>`;
}
export default {
  "named-dirt"(H) {
    const { C } = H;
    const stamp = (x, y, rot) => `<g transform="translate(${x},${y}) rotate(${rot})"><rect x="-170" y="-40" width="340" height="80" fill="none" stroke="${C.war}" stroke-width="6"/>` +
      H.label(0, 12, 28, "UNREMARKABLE", "middle", C.war) + `<path d="M-150,-20 L150,20" stroke="${C.war}" stroke-width="8"/></g>`;
    const svg = sky(C) + stamp(420, 280, -8) + stamp(980, 240, 6) + stamp(1500, 300, -4) +
      `<ellipse cx="960" cy="700" rx="160" ry="90" fill="${C.tan}" stroke="${C.line}" stroke-width="8"/>` +
      `<rect x="760" y="560" width="400" height="80" rx="8" fill="${C.cream}" stroke="${C.line}" stroke-width="6"/>` +
      H.big(960, 622, 64, "DIRT");
    return { svg, alt: "Three crossed-out stamps reading UNREMARKABLE, and a small rock with a large nameplate DIRT." };
  },
  "promiscuous-carbon"(H) {
    const { C } = H;
    const ball = (x, y, letter, fill) => `<circle cx="${x}" cy="${y}" r="70" fill="${fill}" stroke="${C.line}" stroke-width="8"/>` + H.label(x, y + 16, 48, letter);
    const svg = sky(C) +
      `<path d="M960,520 L520,300 M960,520 L1400,280 M960,520 L1180,820" stroke="${C.cream}" stroke-width="10"/>` +
      ball(960, 520, "C", C.yellow) + ball(520, 300, "H", C.cream) + ball(1400, 280, "O", C.orange) + ball(1180, 820, "N", C.peri) +
      `<rect x="180" y="700" width="620" height="140" rx="10" fill="${C.cream}" stroke="${C.line}" stroke-width="6"/>` +
      H.label(490, 785, 32, "WILL BOND WITH ALMOST ANYTHING");
    return { svg, alt: "A carbon atom holding hands with hydrogen, oxygen, and nitrogen, and a clipboard that says it will bond with almost anything." };
  },
  "copy-themselves"(H) {
    const { C } = H;
    const group = (x) => `<g transform="translate(${x},520)"><circle cx="-40" cy="0" r="36" fill="${C.yellow}" stroke="${C.line}" stroke-width="6"/><circle cx="40" cy="-10" r="28" fill="${C.cream}" stroke="${C.line}" stroke-width="6"/><circle cx="10" cy="40" r="24" fill="${C.orange}" stroke="${C.line}" stroke-width="6"/></g>`;
    const svg = sky(C) + group(700) + group(1100) +
      `<rect x="260" y="160" width="1400" height="140" fill="${C.war}" stroke="${C.line}" stroke-width="8"/>` +
      H.big(960, 265, 72, "EVERYTHING WENT WRONG", "middle", C.cream);
    return { svg, alt: "Two identical little molecules under a banner that reads EVERYTHING WENT WRONG." };
  },
  "including-you"(H) {
    const { C } = H;
    const svg = `<rect width="1920" height="1080" fill="${C.cream}"/>` +
      H.label(200, 180, 36, "THE PLOT", "start") +
      H.text(200, 280, 42, ["ECONOMY", "POLITICS", "WARS", "clinical trials"], { fill: C.line, weight: 600 }) +
      `<path d="M160,560 H1760" stroke="${C.line}" stroke-width="3"/>` +
      H.big(200, 780, 92, "1. INCLUDING YOU", "start", C.war);
    return { svg, alt: "A page with four small lines, economy, politics, wars, clinical trials, and a huge footnote: 1. INCLUDING YOU." };
  },
};
