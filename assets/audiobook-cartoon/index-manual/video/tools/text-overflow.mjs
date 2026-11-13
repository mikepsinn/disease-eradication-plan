// Find text that runs off the shape it sits on (a sign, a banner, a card, a button) in a page open in headless
// Chrome:  await page.evaluate(textOverflow, "<root selector>")
// A text's sign is the smallest filled shape drawn before it whose fill covers the middle of the text and which is
// at least half the text's size: first among its earlier siblings (and what they hold), then its parent's, then its
// grandparent's. Points around the letters are tested against the sign's real outline, so a curved or tilted sign
// is checked too. Returns
// [{ text, off }] for each text with letters off its sign, off being the share of test points that miss it.
// Used by tools/sheet-shot.mjs and tools/scene-check.mjs.
export function textOverflow(rootSelector) {
  const root = document.querySelector(rootSelector) || document.body;
  const SHAPES = "rect,path,polygon,polyline,ellipse,circle";
  const shown = (e) => {
    for (let n = e; n && n.nodeType === 1; n = n.parentNode) {
      const cs = getComputedStyle(n);
      if (cs.display === "none" || cs.visibility === "hidden" || Number(cs.opacity) === 0) return false;
    }
    return true;
  };
  // solid fills only: halftone patterns and see-through shading are drawn over a sign, not as one
  const filled = (e) => {
    const cs = getComputedStyle(e);
    return cs.fill !== "none" && !cs.fill.startsWith("url(") && Number(cs.fillOpacity) * Number(cs.opacity) >= 0.6 && shown(e);
  };
  const local = (s, x, y) => new DOMPoint(x, y).matrixTransform(s.getScreenCTM().inverse());
  const covers = (s, x, y) => { const p = local(s, x, y); return s.isPointInFill(p) || s.isPointInStroke(p); };
  const out = [];
  for (const t of root.querySelectorAll("text")) {
    const words = t.textContent.trim();
    if (!words || !shown(t)) continue;
    // test points in the text's own (possibly rotated) frame, put on screen
    const bb = t.getBBox(), m = t.getScreenCTM();
    if (bb.width * Math.hypot(m.a, m.b) < 6) continue;
    const screen = (x, y) => { const p = new DOMPoint(x, y).matrixTransform(m); return [p.x, p.y]; };
    const [cx, cy] = screen(bb.x + bb.width / 2, bb.y + bb.height / 2);
    const k2 = m.a * m.a + m.b * m.b, textArea = bb.width * bb.height * k2;
    let best = null, area = Infinity;
    // the nearest level that has a candidate wins: a sign is drawn just before its text, in the same group
    for (let node = t, level = 0; !best && node.parentNode && node !== root && level < 3; node = node.parentNode, level++) {
      for (let sib = node.previousElementSibling; sib; sib = sib.previousElementSibling) {
        for (const s of [sib, ...sib.querySelectorAll(SHAPES)]) {
          if (!s.matches(SHAPES) || !filled(s) || !covers(s, cx, cy)) continue;
          const r = s.getBoundingClientRect();
          // a sign is at least about half the text's size; smaller shapes under it are details
          if (r.width * r.height >= textArea * 0.5 && r.width * r.height < area) { best = s; area = r.width * r.height; }
        }
      }
    }
    if (!best) continue;
    // Each letter's own box (so text on a curve is followed), less the space above the capitals and below the
    // baseline, with a little room past the first and last letters so text jammed against an edge counts too.
    const n = t.getNumberOfChars(), pts = [];
    for (let i = 0; i < n; i++) {
      if (!t.textContent[i] || !t.textContent[i].trim()) continue;
      const r = t.getExtentOfChar(i), pad = i === 0 ? -r.height * 0.08 : 0, padR = i === n - 1 ? r.height * 0.08 : 0;
      const y0 = r.y + r.height * 0.28, y1 = r.y + r.height * 0.78, xl = r.x + 0.5 + pad, xr = r.x + r.width - 0.5 + padR;
      pts.push(screen(xl, y0), screen(xl, y1), screen(xr, y0), screen(xr, y1));
    }
    const miss = pts.filter(([x, y]) => !covers(best, x, y)).length;
    if (miss) out.push({ text: words.slice(0, 48), off: Math.round((miss / pts.length) * 100) });
  }
  return out;
}
