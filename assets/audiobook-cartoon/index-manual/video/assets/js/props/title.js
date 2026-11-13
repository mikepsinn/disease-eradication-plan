// Shared props: the title card (cartoon-style-bible.md section 1, "Text on screen"; every part's first scene).
//
//   KIT.titleScene(opts)    builds a whole title card scene. look "atomic" (the default; needs assets/js/film.js):
//                           the period card, the heading in the cover font (Fraunces, cream) on plain navy under
//                           the film's emblem (an atom whose electrons are running papers), up from black and down
//                           to black, under the period film. look "office" (Part 1): the navy office wall and the
//                           sun on KIT.horizon, the words slamming in one per spoken word. Both take an optional pill
//                           subtitle and a hook for a small gag. Copy compositions/scenes/_templates/title-card.html.
//   KIT.props.titleSign(o)  the same card as a small SVG sign (on an easel, on posts, or bare) for other scenes.
//
// The layout is computed from the fonts' measured advance widths (below), not from the browser's layout, so it
// is the same before and after the fonts load and gags get exact word boxes in canvas pixels.
(function () {
  var K = window.KIT;
  K.props = K.props || { SHEET: [] };
  K.props.SHEET = K.props.SHEET || [];
  if (K.props.__title) return;
  K.props.__title = true;
  var C = K.C, ink = C.line;

  // The cover fonts (each composition declares them too; the props sheet page does not).
  if (!document.getElementById("kit-title-fonts")) {
    var fontCss = document.createElement("style");
    fontCss.id = "kit-title-fonts";
    fontCss.textContent =
      '@font-face{font-family:"Fraunces";src:url("assets/fonts/Fraunces-Black-Soft.woff2") format("woff2");font-weight:900;font-display:block}' +
      '@font-face{font-family:"Oswald";src:url("assets/fonts/Oswald-SemiBold.woff2") format("woff2");font-weight:600;font-display:block}' +
      '@font-face{font-family:"Inter";src:url("assets/fonts/Inter-Variable.woff2") format("woff2");font-weight:100 900;font-display:block}';
    document.head.appendChild(fontCss);
  }

  // ── Drawing helpers (the HUMANS section of kit.js) ──────────────────
  var LW = 4.4, uid = 0;
  function P(x, y) { return x.toFixed(1) + "," + y.toFixed(1); }
  function polyD(pts) { return "M" + pts.map(function (p) { return P(p[0], p[1]); }).join(" L") + " Z"; }
  function poly(pts) { return 'path d="' + polyD(pts) + '"'; }
  // Shapes drawn twice, a navy pass under the fill, so touching shapes of one color share one outline.
  function solid(tags, col, w) {
    w = w || LW;
    return tags.map(function (t) { return "<" + t + ' fill="' + ink + '" stroke="' + ink + '" stroke-width="' + w + '" stroke-linejoin="miter" stroke-miterlimit="8"/>'; }).join("") +
      tags.map(function (t) { return "<" + t + ' fill="' + col + '"/>'; }).join("");
  }
  function line(d, col, w) { return '<path d="' + d + '" fill="none" stroke="' + (col || ink) + '" stroke-width="' + (w || 2) + '" stroke-linejoin="miter" stroke-linecap="round"/>'; }
  // Print shading: halftone dots over the part of a light shape right of x0 (ids unique on the page).
  function dots(pts, x0, op) {
    var id = "kit-title-hd" + ++uid, ys = pts.map(function (p) { return p[1]; }), xs = pts.map(function (p) { return p[0]; });
    var y0 = Math.min.apply(null, ys) - 2, y1 = Math.max.apply(null, ys) + 2, x1 = Math.max.apply(null, xs) + 2;
    return '<defs><pattern id="' + id + 'd" width="3.6" height="3.6" patternUnits="userSpaceOnUse"><circle cx="1.8" cy="1.8" r="1" fill="' + ink + '"/></pattern><clipPath id="' + id + 'c"><path d="' + polyD(pts) + '"/></clipPath></defs>' +
      '<rect x="' + x0.toFixed(1) + '" y="' + y0.toFixed(1) + '" width="' + Math.max(0, x1 - x0).toFixed(1) + '" height="' + (y1 - y0).toFixed(1) + '" fill="url(#' + id + 'd)" opacity="' + (op || 0.3) + '" clip-path="url(#' + id + 'c)"/>';
  }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function copy(a, b) { var o = {}, k; for (k in a || {}) o[k] = a[k]; for (k in b || {}) o[k] = b[k]; return o; }
  function normT(s) { return String(s).toLowerCase().replace(/[^a-z0-9%$]/g, ""); }
  function add(a, b) { return a + b; }

  // ── Font metrics (measured in headless Chrome from assets/fonts, in em) ──
  // asc/desc: the font's ascent and descent; cap: cap height; gap: the space between words.
  var CHARS = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789%$.,:;'!?&-()/*#’\"";
  var FONTS = {
    F: { family: "Fraunces", weight: 900, italic: false, asc: 0.98, desc: 0.26, cap: 0.7, gap: 0.28,
      adv: [0.174,0.733,0.716,0.669,0.772,0.639,0.603,0.728,0.819,0.408,0.548,0.795,0.608,0.938,0.756,0.758,0.698,0.749,0.758,0.596,0.688,0.726,0.729,1.096,0.721,0.673,0.613,0.511,0.55,0.469,0.553,0.482,0.384,0.516,0.581,0.291,0.281,0.574,0.29,0.859,0.582,0.528,0.56,0.54,0.455,0.436,0.37,0.559,0.505,0.784,0.532,0.519,0.464,0.663,0.454,0.611,0.566,0.624,0.574,0.618,0.532,0.624,0.625,0.831,0.598,0.292,0.291,0.292,0.291,0.219,0.308,0.583,0.931,0.343,0.338,0.333,0.443,0.535,0.643,0.255,0.441] },
    O: { family: "Oswald", weight: 600, italic: false, asc: 1.19, desc: 0.29, cap: 0.81, gap: 0.25,
      adv: [0.25,0.538,0.574,0.553,0.573,0.438,0.425,0.572,0.6,0.29,0.339,0.552,0.433,0.695,0.554,0.576,0.552,0.576,0.583,0.505,0.438,0.578,0.522,0.704,0.508,0.49,0.43,0.449,0.493,0.456,0.49,0.46,0.313,0.489,0.495,0.257,0.261,0.493,0.264,0.737,0.493,0.471,0.492,0.491,0.37,0.413,0.342,0.49,0.413,0.595,0.431,0.436,0.382,0.543,0.384,0.506,0.506,0.515,0.502,0.531,0.428,0.516,0.53,0.982,0.486,0.232,0.227,0.261,0.27,0.161,0.247,0.483,0.578,0.32,0.329,0.314,0.411,0.418,0.524,0.198,0.34] },
    I: { family: "Inter", weight: 700, italic: true, asc: 0.97, desc: 0.24, cap: 0.73, gap: 0.26,
      adv: [0.237,0.747,0.662,0.74,0.722,0.607,0.587,0.75,0.747,0.281,0.584,0.719,0.565,0.932,0.762,0.771,0.648,0.777,0.657,0.655,0.667,0.732,0.747,1.038,0.738,0.731,0.664,0.581,0.63,0.588,0.63,0.596,0.398,0.632,0.623,0.271,0.271,0.58,0.271,0.913,0.623,0.613,0.63,0.63,0.407,0.56,0.366,0.623,0.6,0.85,0.58,0.602,0.573,0.674,0.431,0.63,0.646,0.676,0.622,0.649,0.582,0.651,0.649,1.016,0.655,0.334,0.334,0.334,0.343,0.339,0.338,0.56,0.672,0.468,0.377,0.377,0.388,0.559,0.649,0.311,0.552] },
  };
  // The width of `text` in em (track: extra letter spacing per letter, in em).
  function textW(text, font, track) {
    var f = FONTS[font], w = 0;
    for (var i = 0; i < text.length; i++) { var k = CHARS.indexOf(text[i]); w += k < 0 ? 0.6 : f.adv[k]; }
    return w + (track || 0) * text.length;
  }

  // ── KIT.titleScene ──────────────────────────────────────────────────
  // Line styles. scale: the size relative to the card's heading size S; how: the default entrance.
  //   big     the heading (Fraunces, cream with a cream outline and a navy drop shadow)
  //   small   a smaller heading line in the same font ("The Daily Deletion Event" under "THE PROBLEM")
  //   label   Oswald with a navy outline, like Part 1's "(for Busy People)"
  //   italic  Inter bold italic with a navy outline, for the book's italic lines ("Unlike Everything Else...")
  //   stamp   a red rubber-stamp plate with a cream border (Oswald capitals), tilted, landing with a shake; the
  //           whole line is one plate (one `spoken` entry), or one plate per word with split: true
  // Only big lines set the heading size S; a smaller line too wide for the card shrinks on its own.
  var STAMP_BW = 0.06;
  var STYLES = {
    big: { font: "F", scale: 1, how: "slam" },
    small: { font: "F", scale: 0.5, how: "slide" },
    label: { font: "O", scale: 0.42, how: "slide" },
    italic: { font: "I", scale: 0.3, how: "slide" },
    stamp: { font: "O", scale: 0.62, how: "stamp", track: 0.06, pad: [0.24, 0.12], upper: true },
  };
  var COLORS = { cream: C.cream, teal: C.med, med: C.med, red: C.war, war: C.war, mustard: C.yellow, yellow: C.yellow, orange: C.orange, money: C.money, tan: C.tan };
  function color(c) { return c ? COLORS[c] || c : null; }

  function normLines(lines) {
    if (!lines || !lines.length) throw new Error("KIT.titleScene: opts.lines is empty");
    return lines.map(function (ln, li) {
      var o = Array.isArray(ln) ? { words: ln } : copy(ln);
      if (!o.words || !o.words.length) throw new Error("KIT.titleScene: line " + li + " has no words");
      o.style = o.style || "big";
      o.st = STYLES[o.style];
      if (!o.st) throw new Error("KIT.titleScene: unknown line style '" + o.style + "'");
      o.f = FONTS[o.st.font];
      o.k = o.scale || o.st.scale;
      o.words = o.words.map(function (w) {
        var x = typeof w === "string" ? { text: w } : copy(w);
        if (o.st.upper) x.text = x.text.toUpperCase();
        return x;
      });
      // A stamp is one plate: its words land together (one `spoken` entry), unless split: true.
      if (o.style === "stamp" && !o.split) o.words = [copy(o.words[0], { text: o.words.map(function (x) { return x.text; }).join(" ") })];
      return o;
    });
  }
  // The layout in canvas pixels: one heading size S for the card (every big line fits the width; a smaller line
  // that would not fit shrinks on its own), the lines stacked and centered on cy. Each word's box is its cap
  // height (a stamp's: its plate).
  function fit(lines, o) {
    var V = o.V, avail = o.width || (V ? 940 : 1600), S = o.size || (V ? 140 : 160);
    lines.forEach(function (ln) {
      ln.em = ln.words.map(function (w) { return textW(w.text, ln.st.font, ln.st.track) + (ln.st.pad ? 2 * ln.st.pad[0] + 2 * STAMP_BW : 0); });
      ln.emW = ln.em.reduce(add, 0) + ln.f.gap * (ln.words.length - 1);
      if (ln.style === "big") S = Math.min(S, avail / (ln.emW * ln.k));
    });
    function size(ln, S) { return ln.style === "big" ? S * ln.k : Math.min(S * ln.k, avail / ln.emW); }
    function vh(ln, S) { var s = size(ln, S); return ln.st.pad ? (ln.f.cap + 2 * ln.st.pad[1] + 2 * STAMP_BW) * s : ln.f.cap * s; }
    function gap(a, b, S) { return 0.24 * Math.max(size(a, S), size(b, S)) + 8; }
    function total(S) { return lines.reduce(function (t, ln, i) { return t + vh(ln, S) + (i ? gap(lines[i - 1], ln, S) : 0); }, 0); }
    var maxH = o.maxH || (V ? 820 : 470);
    for (var it = 0; it < 4 && total(S) > maxH; it++) S *= maxH / total(S);
    var Hb = total(S), cy = o.cy || (V ? 560 : 370), top = Math.max(o.minTop || (V ? 190 : 100), cy - Hb / 2), y = top, words = [];
    var out = lines.map(function (ln, i) {
      if (i) y += gap(lines[i - 1], ln, S);
      var s = size(ln, S), h = vh(ln, S), lw = ln.emW * s, x = o.W / 2 - lw / 2, L = { y: y, h: h, size: s, w: lw, x: x, style: ln.style, words: [] };
      ln.words.forEach(function (w, j) {
        var ww = ln.em[j] * s;
        words.push({ line: i, text: w.text, x: x, y: y, w: ww, h: h, size: s });
        L.words.push(words.length - 1);
        x += ww + ln.f.gap * s;
      });
      y += h;
      return L;
    });
    return { S: S, top: top, bottom: y, cx: o.W / 2, lines: out, words: words };
  }
  // Eight hard offsets make an outline (CSS has no text stroke that survives the render).
  function ring(col, o) {
    return [[1, 1], [-1, 1], [1, -1], [-1, -1], [0, 1.3], [0, -1.3], [1.3, 0], [-1.3, 0]].map(function (d) { return (d[0] * o).toFixed(1) + "px " + (d[1] * o).toFixed(1) + "px 0 " + col; }).join(",");
  }
  function wordEl(b, ln, w) {
    var f = ln.f, st = ln.st, s = b.size, e = document.createElement("div"), col = color(w.color || ln.color);
    var css = "position:absolute;left:" + b.x.toFixed(1) + "px;width:" + b.w.toFixed(1) + "px;white-space:nowrap;text-align:center;font-family:" + f.family +
      ";font-weight:" + f.weight + ";font-style:" + (f.italic ? "italic" : "normal") + ";font-size:" + s.toFixed(1) + "px;";
    if (st.pad) {
      var bw = STAMP_BW * s, o = Math.max(2, 0.035 * s);
      css += "top:" + b.y.toFixed(1) + "px;height:" + b.h.toFixed(1) + "px;box-sizing:border-box;border:" + bw.toFixed(1) + "px solid " + C.cream + ";background:" + (col || C.war) +
        ";color:" + C.cream + ";line-height:" + (b.h - 2 * bw + (f.cap - f.asc + f.desc) * s).toFixed(1) + "px;letter-spacing:" + st.track + "em;text-indent:" + st.track + "em;" +
        "box-shadow:0 0 0 " + o.toFixed(1) + "px " + C.ink + "," + (0.05 * s).toFixed(1) + "px " + (0.07 * s).toFixed(1) + "px 0 " + o.toFixed(1) + "px " + C.ink + ";";
      e.__pin = [-bw, -bw, 0];
    } else {
      var lh = (f.asc + f.desc) * s;
      var shadow = st.font === "F" ? ring(C.cream, Math.max(1.5, 0.022 * s)) + "," + (0.04 * s).toFixed(1) + "px " + (0.053 * s).toFixed(1) + "px 0 " + C.ink : ring(C.ink, Math.max(1.5, 0.05 * s));
      css += "top:" + (b.y - (f.asc - f.cap) * s).toFixed(1) + "px;height:" + lh.toFixed(1) + "px;line-height:" + lh.toFixed(1) + "px;color:" + (col || C.cream) + ";text-shadow:" + shadow + ";";
      e.__pin = [0, 0, (f.asc - f.cap) * s];
    }
    e.style.cssText = css;
    e.textContent = w.text;
    return e;
  }
  // The entrances. els: the word elements; o: { size, y, h (the unit's box), dur, tilt, shake (element) }.
  function play(tl, els, how, t, o) {
    var s = o.size, d = o.dur;
    if (how === "slam") tl.fromTo(els, { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: d || 0.22, ease: "back.out(2)" }, t);
    else if (how === "slide") tl.fromTo(els, { opacity: 0, y: 0.5 * s }, { opacity: 1, y: 0, duration: d || 0.35, ease: "power3.out" }, t);
    else if (how === "drop") tl.fromTo(els, { opacity: 1, y: -(o.y + o.h + 200) }, { y: 0, duration: d || 0.55, ease: "bounce.out" }, t);
    else if (how === "pop") tl.fromTo(els, { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, duration: d || 0.3, ease: "back.out(2.6)" }, t);
    else if (how === "fade") tl.fromTo(els, { opacity: 0 }, { opacity: 1, duration: d || 0.3, ease: "none" }, t);
    else if (how === "bounce") {
      tl.fromTo(els, { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2)" }, t);
      tl.fromTo(els, { y: 0 }, { y: -0.24 * s, duration: 0.13, ease: "power2.out", immediateRender: false }, t + 0.24);
      tl.fromTo(els, { y: -0.24 * s }, { y: 0, duration: 0.45, ease: "bounce.out", immediateRender: false }, t + 0.37);
    } else if (how === "stamp") {
      var r = o.tilt === undefined ? -4 : o.tilt, dd = d || 0.14;
      tl.fromTo(els, { opacity: 0, scale: 2.6, rotation: r - 10 }, { opacity: 1, scale: 1, rotation: r, duration: dd, ease: "power4.in" }, t);
      tl.fromTo(o.shake, { x: 0 }, { x: Math.max(4, 0.04 * s), duration: 0.035, repeat: 5, yoyo: true, ease: "none", immediateRender: false }, t + dd);
    } else throw new Error("KIT.titleScene: unknown entrance '" + how + "'");
  }

  // The atomic card's emblem: three orbits round an orange nucleus, a war-money paper running round each orbit on its
  // stick legs, going nowhere. EMBLEM: its center, orbit radii and the papers' scale, per canvas shape.
  var EMBLEM = { tall: { at: [540, 600], rx: 250, ry: 76, k: 0.75 }, wide: { at: [960, 300], rx: 200, ry: 62, k: 0.62 } };
  var TILT = [0, 60, -60];
  function emblemSvg(id, E) {
    var cx = E.at[0], cy = E.at[1];
    var orbits = TILT.map(function (a) {
      return '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + E.rx + '" ry="' + E.ry + '" fill="none" stroke="' + C.cream + '" stroke-width="5" transform="rotate(' + a + " " + cx + " " + cy + ')"/>';
    }).join("");
    var bills = TILT.map(function (a, i) { return '<g id="' + id + "-e" + i + '"><g transform="scale(' + E.k + ')">' + K.money("war", 0) + "</g></g>"; }).join("");
    var nucleus = '<circle cx="' + cx + '" cy="' + cy + '" r="30" fill="' + C.orange + '" stroke="' + C.cream + '" stroke-width="5"/>' +
      '<circle cx="' + (cx - 9) + '" cy="' + (cy - 9) + '" r="8" fill="' + C.yellow + '"/>';
    return '<rect width="' + K.W + '" height="' + K.H + '" fill="' + C.navy + '"/>' + orbits + bills + nucleus;
  }
  function runEmblem(tl, id, E, D) {
    var els = TILT.map(function (a, i) { var e = document.getElementById(id + "-e" + i); return { el: e, legs: e.querySelector(".legs"), a: (a * Math.PI) / 180, p0: i * 2.1 }; });
    K.onTime(tl, D, function (t) {
      els.forEach(function (e, i) {
        var th = e.p0 + t * 2.4, ex = E.rx * Math.cos(th), ey = E.ry * Math.sin(th);
        var x = E.at[0] + ex * Math.cos(e.a) - ey * Math.sin(e.a), y = E.at[1] + ex * Math.sin(e.a) + ey * Math.cos(e.a);
        e.el.setAttribute("transform", "translate(" + x.toFixed(1) + "," + (y - 6).toFixed(1) + ")");
        var l = Math.floor(t * 10 + i) % 2;
        e.legs.setAttribute("d", "M-16,24 l" + (-6 + l * 10) + ",22 h-8 M16,24 l" + (6 - l * 10) + ",22 h8");
      });
    });
  }

  // Build a title card into the scene's standard elements: #<id>-cam holds #<id>-bg (the office wall), -sun,
  // -back (art behind the words), -words and -art (art in front); #<id>-grain sits outside the camera. Any of
  // them the scene file leaves out is made here (only -cam is required). Registers window.__timelines[id].
  //
  // opts:
  //   id         the scene id (required)
  //   lines      the 16:9 line breaks: [["THE", "HUMAN"], ["ECONOMY"]]. A line can also be an object
  //              { words: [...], style: "big"|"small"|"label"|"italic"|"stamp", scale, color, how, dur,
  //                cue, n, at, offset, t } (with cue or t the whole line comes in at once, and `spoken`
  //              skips its words). A word can be an object { text, color, how, dur, tilt }.
  //   linesTall  the 9:16 line breaks (the same words in the same order); defaults to lines.
  //   look       "atomic" (default) or "office" (above). The atomic card has no sun and no enter; every line fades
  //              in (opts.how or a line's own how overrides that), and without `spoken` the whole heading is on
  //              the card as it comes up from black. seed: the period film's seed (default 11).
  //   spoken     one entry per heading word (reading order, lines with their own cue left out): the spoken
  //              cue word that brings it in, "Human", or { cue: "one", show: "1%" } for a word said
  //              differently (show is checked against the line), with optional n (which occurrence; by default
  //              the first one after the previous entry), at "on"|"after"|"before" (KIT.cue/after/before),
  //              offset (s), t (an absolute scene time instead), how, dur, color, tilt.
  //   how, dur   the entrance for big words: "slam" (default), "slide", "drop", "pop", "bounce", "stamp", "fade".
  //   sub        an optional pill under the heading: "text" or { text, cue, n, at, offset, t } (default: a beat
  //              after the last heading word).
  //   size, width, cy, maxH, minTop   layout overrides (heading size cap, line width, block center, ...).
  //   sunScale   the office sun's size (default 1.15, as in Part 1); enter: a KIT.enter kind ("slide left", ...).
  //   gag        function (ctx) for a small part-specific gag. ctx = { id, tl, D, W, H, V, C, look, root, cam, bg,
  //              emblem (atomic: { at, rx, ry, k }), sun (office: the sun's untransformed <g>; it sits on
  //              (W/2, KIT.horizon)), back, art, wordsEl, sub (the pill),
  //              cue, after, before (word[, n] → scene seconds), layout { S, top, bottom, cx, lines, pillTop },
  //              words: [{ el, text, line, t (when it lands), how, box: { x, y, w, h } (canvas px, the cap
  //              height) }], word(k) (by index or text), pin(k, where, svg) }.
  //              pin puts an anchor inside word k's element at "right" (default), "left", "top", "bottom",
  //              "topleft", "topright", "bottomleft", "bottomright" or "center" of its capitals and draws svg
  //              (markup around (0,0), canvas px) there; it moves with the word. It returns the anchor <div>,
  //              which GSAP can tween (x, y, rotation, scale; transformOrigin "0 0" swings it on the anchor).
  // Returns ctx.
  function titleScene(opts) {
    var id = opts.id;
    if (!id) throw new Error("KIT.titleScene: opts.id is required");
    var sc = K.scene(id), D = sc.duration, W = K.W, H = K.H, V = K.V;
    var q = function (s) { return document.getElementById(id + "-" + s); };
    var cam = q("cam");
    if (!cam) throw new Error("KIT.titleScene: no #" + id + "-cam in the scene (copy compositions/scenes/_templates/title-card.html)");
    var root = cam.parentNode;
    function part(name) {
      var e = q(name);
      if (!e) { e = document.createElement("div"); e.id = id + "-" + name; }
      e.style.cssText = "position:absolute;inset:0;";
      return e;
    }
    var bg = part("bg"), sunEl = part("sun"), back = part("back"), wordsEl = part("words"), art = part("art"), grain = part("grain");
    [bg, sunEl, back, wordsEl, art].forEach(function (e) { cam.appendChild(e); });
    root.appendChild(grain); // outside the camera, so a zoom does not scale the grain (or the period film)
    var look = opts.look || "atomic", atomic = look === "atomic", E = V ? EMBLEM.tall : EMBLEM.wide, weave = null, black = null;
    if (!atomic && look !== "office") throw new Error("KIT.titleScene(" + id + "): look is \"atomic\" or \"office\", not '" + look + "'");
    if (atomic && !K.film) throw new Error("KIT.titleScene(" + id + "): the atomic look needs <script src=\"assets/js/film.js\"> after kit.js");
    if (atomic && opts.enter) throw new Error("KIT.titleScene(" + id + "): the atomic card comes up from black; it takes no enter");
    cam.style.cssText = "position:absolute;inset:0;";

    if (atomic) {
      // the weave wraps the camera; the period film (in -grain) and the black card sit over both
      weave = part("weave");
      root.insertBefore(weave, cam);
      weave.appendChild(cam);
      black = part("black");
      black.style.background = K.FILM_BLACK;
      root.appendChild(black);
      bg.innerHTML = K.svg(W, H, emblemSvg(id, E));
    } else {
      bg.innerHTML = K.office(-2000, 0, { noSun: true, noHalo: true });
      sunEl.innerHTML = K.svg(W, H, '<g id="' + id + '-sun-g">' + K.sun(W / 2, K.horizon, opts.sunScale || 1.15) + "</g>");
      grain.innerHTML = K.svg(W, H, K.grain(id));
    }

    var lines = normLines(V && opts.linesTall ? opts.linesTall : opts.lines);
    if (atomic) lines.forEach(function (ln) {
      if (!ln.how) ln.how = opts.how || "fade";
      if (!opts.spoken && ln.cue === undefined && typeof ln.t !== "number") ln.t = 0;
    });
    // the atomic card's heading sits under the emblem
    var LD = !atomic ? {} : V ? { size: 180, cy: 1080, maxH: 400, minTop: 900 } : { size: 200, cy: 700, maxH: 320, minTop: 540 };
    var L = fit(lines, { V: V, W: W, size: opts.size || LD.size, width: opts.width, cy: opts.cy || LD.cy, maxH: opts.maxH || LD.maxH, minTop: opts.minTop || LD.minTop });

    // Pair the heading words with their spoken cues, in reading order.
    var spoken = opts.spoken || [], si = 0, units = [];
    lines.forEach(function (ln, li) {
      var idx = L.lines[li].words;
      if (ln.cue !== undefined || typeof ln.t === "number") {
        ln.words.forEach(function (w) { w.spec = copy(ln, w); });
        units.push({ els: idx, spec: copy({ how: ln.how || ln.st.how }, ln), line: li });
        return;
      }
      ln.words.forEach(function (w, j) {
        var sp = spoken[si++];
        if (sp === undefined) throw new Error("KIT.titleScene(" + id + "): no spoken cue for heading word '" + w.text + "' (spoken has " + spoken.length + " entries)");
        sp = typeof sp === "string" ? { cue: sp } : sp;
        if (sp.show !== undefined && normT(sp.show) !== normT(w.text)) throw new Error("KIT.titleScene(" + id + "): spoken entry " + (si - 1) + " shows '" + sp.show + "' but the heading word is '" + w.text + "'");
        var spec = copy({ color: ln.color, dur: ln.dur || (ln.style === "big" ? opts.dur : undefined), how: ln.how || (ln.style === "big" ? opts.how : null) || ln.st.how, tilt: ln.tilt }, copy(w, sp));
        if (spec.how === undefined || spec.how === null) spec.how = ln.st.how;
        w.spec = spec;
        units.push({ els: [idx[j]], spec: spec, line: li });
      });
    });
    if (si !== spoken.length) throw new Error("KIT.titleScene(" + id + "): spoken has " + spoken.length + " entries for " + si + " heading words");

    // The words.
    var info = L.words.map(function (b, i) {
      var ln = lines[b.line], w = ln.words[L.lines[b.line].words.indexOf(i)];
      var el = wordEl(b, ln, { text: w.text, color: (w.spec && w.spec.color) || w.color });
      el.className = id + "-w";
      el.setAttribute("data-w", w.text);
      wordsEl.appendChild(el);
      return { el: el, text: w.text, line: b.line, size: b.size, box: { x: b.x, y: b.y, w: b.w, h: b.h } };
    });

    var tl = gsap.timeline({ paused: true });
    if (opts.enter) K.enter(tl, cam, opts.enter, opts.enterView);
    if (atomic) {
      // up from black like the head of a reel, a slow push, and down to black for the next shot
      K.film(tl, id, weave, grain, opts.seed || 11);
      runEmblem(tl, id, E, D);
      tl.fromTo(black, { opacity: 1 }, { opacity: 0, duration: 0.35, ease: "power1.out" }, 0);
      tl.fromTo(cam, { scale: 1, transformOrigin: "50% 45%" }, { scale: 1.045, transformOrigin: "50% 45%", duration: D, ease: "none" }, 0);
      tl.to(black, { opacity: 1, duration: 0.24, ease: "power1.in" }, D - 0.26);
    }

    // Each unit lands on its cue: the first occurrence at or after the previous unit's cue, unless n is given.
    var cursor = 0, lastCue = null;
    function nth(w, from) {
      var want = normT(w), n = 0, words = K.P.words;
      for (var i = 0; i < words.length; i++) {
        var x = words[i];
        if (x.s < sc.start - 0.05 || x.s >= sc.start + sc.duration || normT(x.w) !== want) continue;
        n++;
        if (x.s - sc.start >= from - 0.01) return n;
      }
      throw new Error("KIT.titleScene(" + id + "): no spoken '" + w + "' at or after " + from.toFixed(2) + " s" +
        (lastCue ? " (the previous cue, '" + lastCue[0] + "', is at " + from.toFixed(2) + " s: is that word missing from the part's audio cut?)" : ""));
    }
    function when(spec) {
      if (typeof spec.t === "number") return spec.t;
      var w = spec.cue, n = spec.n || nth(w, cursor);
      var start = K.cue(id, w, n);
      cursor = start;
      lastCue = [w, n];
      var t = spec.at === "after" ? K.after(id, w, n) : spec.at === "before" ? K.before(id, w, n) : start;
      return Math.max(0, t + (spec.offset || 0));
    }
    units.forEach(function (u) {
      var t = when(u.spec), els = u.els.map(function (i) { return info[i].el; }), b0 = info[u.els[0]];
      u.els.forEach(function (i) { info[i].t = t; info[i].how = u.spec.how; });
      play(tl, els, u.spec.how, t, { size: b0.size, y: b0.box.y, h: b0.box.h, dur: u.spec.dur, tilt: u.spec.tilt, shake: wordsEl });
    });

    // The pill subtitle.
    var pill = null, pillTop = V ? L.bottom + 80 : Math.max(L.bottom + 60, K.horizon + 40);
    if (opts.sub) {
      var sub = typeof opts.sub === "string" ? { text: opts.sub } : opts.sub;
      var row = document.createElement("div");
      row.id = id + "-sub-row";
      row.style.cssText = "position:absolute;left:0;right:0;top:" + pillTop.toFixed(0) + "px;display:flex;justify-content:center;";
      pill = document.createElement("div");
      pill.id = id + "-sub";
      pill.style.cssText = "padding:14px 40px;border-radius:999px;background:" + C.deep + ";border:4px solid " + C.orange + ";font-family:Inter;font-weight:700;font-size:" + (V ? 40 : 42) +
        "px;line-height:1.25;color:" + C.cream + ";text-align:center;max-width:" + (V ? 900 : 1500) + "px;";
      pill.textContent = sub.text;
      row.appendChild(pill);
      wordsEl.appendChild(row);
      var ts = sub.cue !== undefined || typeof sub.t === "number" ? when(sub) : lastCue ? Math.min(D - 0.45, K.after(id, lastCue[0], lastCue[1])) : 0.3;
      tl.fromTo(pill, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, ts);
    }

    var ctx = {
      id: id, tl: tl, D: D, W: W, H: H, V: V, C: C, look: look, root: root, cam: cam, bg: bg, emblem: atomic ? E : null, sun: document.getElementById(id + "-sun-g"), back: back, art: art, wordsEl: wordsEl, sub: pill,
      cue: function (w, n) { return K.cue(id, w, n); }, after: function (w, n) { return K.after(id, w, n); }, before: function (w, n) { return K.before(id, w, n); },
      layout: { S: L.S, top: L.top, bottom: L.bottom, cx: L.cx, lines: L.lines, pillTop: pillTop }, words: info,
    };
    ctx.word = function (k) {
      if (typeof k === "number") { if (!info[k]) throw new Error("KIT.titleScene(" + id + "): no word " + k); return info[k]; }
      for (var i = 0; i < info.length; i++) if (normT(info[i].text) === normT(k)) return info[i];
      throw new Error("KIT.titleScene(" + id + "): no heading word '" + k + "'");
    };
    ctx.pin = function (k, where, svgInner) {
      var wd = ctx.word(k), b = wd.box, off = wd.el.__pin, co = off[2];
      var A = { right: [b.w, co + b.h / 2], left: [0, co + b.h / 2], top: [b.w / 2, co], bottom: [b.w / 2, co + b.h], topleft: [0, co], topright: [b.w, co],
        bottomleft: [0, co + b.h], bottomright: [b.w, co + b.h], center: [b.w / 2, co + b.h / 2] }[where || "right"];
      if (!A) throw new Error("KIT.titleScene: unknown pin anchor '" + where + "'");
      var d = document.createElement("div");
      d.className = id + "-pin";
      d.style.cssText = "position:absolute;left:" + (A[0] + off[0]).toFixed(1) + "px;top:" + (A[1] + off[1]).toFixed(1) + "px;width:0;height:0;overflow:visible;text-shadow:none;letter-spacing:0;text-indent:0;";
      if (svgInner) d.innerHTML = '<svg width="1" height="1" style="position:absolute;left:0;top:0;overflow:visible">' + svgInner + "</svg>";
      wd.el.appendChild(d);
      return d;
    };
    if (opts.gag) opts.gag(ctx);
    tl.set({}, {}, D);
    window.__timelines[id] = tl;
    return ctx;
  }
  K.titleScene = titleScene;

  // ── KIT.props.titleSign ─────────────────────────────────────────────
  // The title card as a small sign: the navy office wall, the half-sun on its horizon, two atomic stars and the
  // heading in the cover font, in a navy board with an orange inner rule. Drawn around x 0, standing on y 0.
  // o: { lines (default the book title; words are strings or { text, color }), w (the board's width, default 260;
  //      the board is 16:9), stand "easel" (default, about 240 tall: a presentation easel beside a 180-tall human)
  //      | "posts" (a roadside sign) | "none" (the bare board, its bottom edge on y 0, to hang on a wall or hold),
  //      sub (a small pill line under the heading) }
  // Parts (untransformed groups; each carries its pivot as data-pivot="x y", for gsap.set(el, { svgOrigin })):
  //   .title-sign-board  the board without its stand; pivot: its bottom center (0, -lift), lift 70 (easel),
  //                      96 (posts) or 0 (bare), to wobble it or tip it over
  //   .title-sign-sun    the half-sun; pivot: its center on the horizon, to sink or raise it (it is clipped)
  //   .title-sign-w      one per heading word; pivot: the word's center, to slam the words in
  //   .title-sign-sub    the pill line; pivot: its center
  var SIGN_GAP = 0.42; // a wider word gap than the card's: at sign size the outline and shadow close up 0.28 em
  K.props.titleSign = function (o) {
    o = o || {};
    var w = o.w || 260, h = Math.round((w * 9) / 16), stand = o.stand || "easel";
    var lift = stand === "easel" ? 70 : stand === "posts" ? 96 : 0;
    var x0 = -w / 2, x1 = w / 2, y1 = -lift, y0 = y1 - h, hy = y0 + h * 0.7, cl = "kit-title-cl" + ++uid;
    var lines = (o.lines || [["HOW", "TO", "END"], ["WAR", "AND", "DISEASE"]]).map(function (ln) {
      return ln.map(function (x) { return typeof x === "string" ? { text: x } : x; });
    });

    // The stand, behind the board.
    var standSvg = "";
    if (stand === "easel") {
      var peak = [0, y0 - 22], fl = [-w * 0.36, 0], fr = [w * 0.36, 0];
      var leg = function (a, b, w0, w1) {
        var dx = b[0] - a[0], dy = b[1] - a[1], L = Math.sqrt(dx * dx + dy * dy), nx = -dy / L, ny = dx / L;
        return [[a[0] + (nx * w0) / 2, a[1] + (ny * w0) / 2], [b[0] + (nx * w1) / 2, b[1] + (ny * w1) / 2], [b[0] - (nx * w1) / 2, b[1] - (ny * w1) / 2], [a[0] - (nx * w0) / 2, a[1] - (ny * w0) / 2]];
      };
      var back = leg([4, y0 - 14], [w * 0.1, 0], 6, 8), left = leg(peak, fl, 7, 11), right = leg(peak, fr, 7, 11);
      var cross = [[-w * 0.3, -lift * 0.36 - 4], [w * 0.3, -lift * 0.36 - 4], [w * 0.29, -lift * 0.36 + 4], [-w * 0.29, -lift * 0.36 + 4]];
      var ledge = [[-w * 0.46, y1 - 1], [w * 0.46, y1 - 1], [w * 0.44, y1 + 11], [-w * 0.44, y1 + 11]];
      standSvg = solid([poly(back)], C.rust, 3) + solid([poly(left), poly(right), poly(cross)], C.tan, 3) + dots(right, 0, 0.28) + dots(cross, 0, 0.22) +
        '<circle cx="' + peak[0] + '" cy="' + (peak[1] + 3) + '" r="3.2" fill="' + C.yellow + '" stroke="' + ink + '" stroke-width="2"/>' +
        solid([poly(ledge)], C.tan, 3) + dots(ledge, 0, 0.28) + line("M" + P(-w * 0.45, y1 + 1) + " H" + (w * 0.45).toFixed(1), C.orange, 1.6);
    } else if (stand === "posts") {
      [-1, 1].forEach(function (sx) {
        var px = sx * w * 0.3, post = [[px - 6, y0 + 12], [px + 6, y0 + 12], [px + 6, 0], [px - 6, 0]], mound = [[px - 20, 1], [px - 11, -7], [px + 11, -7], [px + 20, 1]];
        standSvg += solid([poly(post)], C.tan, 3) + dots(post, px, 0.3) + solid([poly(mound)], C.rust, 2.6);
      });
    }

    // The board: the office wall in miniature, clipped to the board.
    var rect = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];
    var r = h * 0.3, sun = [[1, C.rust], [0.82, C.orange], [0.6, C.yellow]].map(function (g) {
      var rr = r * g[0];
      return '<path d="M' + P(-rr, hy) + " A" + rr.toFixed(1) + "," + rr.toFixed(1) + " 0 0 1 " + P(rr, hy) + ' Z" fill="' + g[1] + '"/>';
    }).join("");
    var tiles = [-3, -2, -1, 0, 1, 2, 3].map(function (i) { return line("M" + P(i * w * 0.06, hy) + " L" + P(i * w * 0.2, y1), C.navy, 1.4); }).join("") +
      line("M" + P(x0, hy + (y1 - hy) * 0.45) + " H" + x1.toFixed(1), C.navy, 1.4);
    var wall = '<defs><clipPath id="' + cl + '"><path d="' + polyD(rect) + '"/></clipPath></defs><g clip-path="url(#' + cl + ')">' +
      '<path d="' + polyD([[x0, y0], [x0 + w * 0.28, y0], [x0 + w * 0.18, hy], [x0, hy]]) + '" fill="' + C.slate + '"/>' +
      '<path d="' + polyD([[x1, y0], [x1 - w * 0.26, y0], [x1 - w * 0.16, hy], [x1, hy]]) + '" fill="' + C.deep + '"/>' +
      K.star(x0 + w * 0.1, y0 + h * 0.2, w * 0.035, C.yellow) + K.star(x1 - w * 0.1, y0 + h * 0.16, w * 0.03, C.cream) + K.star(x0 + w * 0.32, y0 + h * 0.09, w * 0.016, C.cream) +
      '<g class="title-sign-sun" data-pivot="0 ' + hy.toFixed(1) + '">' + sun + "</g>" +
      '<rect x="' + x0 + '" y="' + hy.toFixed(1) + '" width="' + w + '" height="' + (y1 - hy).toFixed(1) + '" fill="' + C.slate + '"/>' + tiles +
      '<rect x="' + x0 + '" y="' + (hy - 1.5).toFixed(1) + '" width="' + w + '" height="3" fill="' + C.yellow + '"/>' + "</g>";

    // The heading, fitted to the board.
    var ems = lines.map(function (ln) { return ln.map(function (x) { return textW(x.text, "F"); }); });
    var lineEm = ems.map(function (e) { return e.reduce(add, 0) + SIGN_GAP * (e.length - 1); });
    var fs = Math.min(h * 0.2, (w * 0.84) / Math.max.apply(null, lineEm)), gapY = 0.24 * fs;
    var block = function () { return lines.length * 0.7 * fs + (lines.length - 1) * gapY; };
    if (block() > h * 0.5) { fs *= (h * 0.5) / block(); gapY = 0.24 * fs; }
    var cy = y0 + h * (o.sub ? 0.33 : 0.36), ty = cy - block() / 2, words = "";
    lines.forEach(function (ln, li) {
      var x = -(lineEm[li] * fs) / 2, base = ty + 0.7 * fs;
      ln.forEach(function (x2, j) {
        var ww = ems[li][j] * fs, cx = x + ww / 2, col = color(x2.color) || C.cream, t = esc(x2.text);
        var attrs = 'text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="' + fs.toFixed(1) + '"';
        words += '<g class="title-sign-w" data-pivot="' + cx.toFixed(1) + " " + (base - 0.35 * fs).toFixed(1) + '">' +
          '<text x="' + (cx + 0.05 * fs).toFixed(1) + '" y="' + (base + 0.065 * fs).toFixed(1) + '" ' + attrs + ' fill="' + C.ink + '" stroke="' + C.ink + '" stroke-width="' + (0.05 * fs).toFixed(2) + '" stroke-linejoin="miter" stroke-miterlimit="2">' + t + "</text>" +
          '<text x="' + cx.toFixed(1) + '" y="' + base.toFixed(1) + '" ' + attrs + ' fill="' + col + '" stroke="' + C.ink + '" stroke-width="' + (0.05 * fs).toFixed(2) + '" stroke-linejoin="miter" stroke-miterlimit="2" paint-order="stroke">' + t + "</text></g>";
        x += ww + SIGN_GAP * fs;
      });
      ty += 0.7 * fs + gapY;
    });
    var subSvg = "";
    if (o.sub) {
      var ss = Math.min(h * 0.075, (w * 0.7) / (textW(o.sub, "I") + 1.6)), pw = (textW(o.sub, "I") + 1.6) * ss, ph = 1.6 * ss, py = y1 - h * 0.15;
      subSvg = '<g class="title-sign-sub" data-pivot="0 ' + py.toFixed(1) + '"><rect x="' + (-pw / 2).toFixed(1) + '" y="' + (py - ph / 2).toFixed(1) + '" width="' + pw.toFixed(1) + '" height="' + ph.toFixed(1) + '" rx="' + (ph / 2).toFixed(1) + '" fill="' + C.deep + '" stroke="' + C.orange + '" stroke-width="2"/>' +
        '<text x="0" y="' + (py + 0.36 * ss).toFixed(1) + '" text-anchor="middle" font-family="Inter" font-weight="700" font-size="' + ss.toFixed(1) + '" fill="' + C.cream + '">' + esc(o.sub) + "</text></g>";
    }
    var board = solid([poly(rect)], C.navy, 5) + wall + words + subSvg +
      '<path d="' + polyD([[x0 + 6, y0 + 6], [x1 - 6, y0 + 6], [x1 - 6, y1 - 6], [x0 + 6, y1 - 6]]) + '" fill="none" stroke="' + C.orange + '" stroke-width="2" stroke-linejoin="miter"/>' +
      line("M" + P(x1 - 2.5, y0 + 3) + " V" + (y1 - 3).toFixed(1) + " M" + P(x0 + 3, y1 - 2.5) + " H" + (x1 - 3).toFixed(1), C.orange, 1.8);
    return '<g class="title-sign">' + standSvg + '<g class="title-sign-board" data-pivot="0 ' + y1 + '">' + board + "</g></g>";
  };

  K.props.SHEET.push(["titleSign", {}, "TITLE SIGN (easel, the book title)"]);
  K.props.SHEET.push(["titleSign", { lines: [["THE", "HUMAN"], ["ECONOMY"]], stand: "posts" }, "TITLE SIGN (posts)"]);
  K.props.SHEET.push(["titleSign", { lines: [["THE", "SOLUTION"], ["A", { text: "1%", color: "teal" }, "TREATY"]], stand: "none", w: 300 }, "TITLE SIGN (bare board, teal 1%)"]);
  K.props.SHEET.push(["titleSign", { lines: [["HOW", "TO", "END"], ["WAR", "AND", "DISEASE"]], sub: "(for Busy People)" }, "TITLE SIGN (with a pill line)"]);
})();
