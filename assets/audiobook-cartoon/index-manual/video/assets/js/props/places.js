// Shared props: buildings and places (review sheet: node tools/props-sheet.mjs places).
// Each KIT.props.<name>(o) returns SVG markup drawn around (0,0), standing on y 0 (it extends upward), in the
// units of KIT.person (about 180 tall, feet at y 100): to stand a prop on the same ground as a person, translate
// it by +100. Drawn like the HUMANS section of kit.js: sharp polygons with mitred corners, a thin navy outline
// (each shape drawn twice, a navy pass under the fill), orange edges on dark shapes, halftone dots on light ones.
//
// Every prop is wrapped in an untransformed <g class="prop-<name>"> with its pivot at the base center (0,0)
// (fold a house flat: scaleY 0 there). Every moving part is an untransformed <g class="..."> group with its
// pivot in data-ox / data-oy, in prop units, so a scene can do
//   gsap.set(el, { svgOrigin: el.dataset.ox + " " + el.dataset.oy })
// and the pivot stays right however the scene places or scales the prop (svgOrigin is in the parent's units).
// Ids (patterns, clip paths) are unique per call. No randomness: the same options draw the same picture.
(function () {
  var K = window.KIT;
  K.props = K.props || { SHEET: [] };
  if (K.props.__places) return;
  K.props.__places = true;

  var C = K.C, ink = C.line, LW = 4.4, uid = 0;

  // ── Helpers (the HUMANS section's, for buildings) ─────────────────────
  function n1(v) { var r = Math.round(v * 10) / 10; return String(r === 0 ? 0 : r); }
  function P(x, y) { return n1(x) + "," + n1(y); }
  function polyD(pts) { return "M" + pts.map(function (p) { return P(p[0], p[1]); }).join(" L") + " Z"; }
  function poly(pts) { return 'path d="' + polyD(pts) + '"'; }
  function R(x, y, w, h) { return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]; }
  function circ(cx, cy, r) { return 'circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(r) + '"'; }
  function mirror(pts, cx) { return pts.map(function (p) { return [2 * (cx || 0) - p[0], p[1]]; }); }
  function shift(pts, dx, dy) { return pts.map(function (p) { return [p[0] + dx, p[1] + dy]; }); }
  // Points on an elliptical arc from angle a0 to a1 (degrees, 0 = +x, 90 = up), n facets: round things stay faceted.
  function arc(cx, cy, rx, ry, a0, a1, n) {
    var out = [];
    for (var i = 0; i <= n; i++) {
      var a = ((a0 + ((a1 - a0) * i) / n) * Math.PI) / 180;
      out.push([cx + rx * Math.cos(a), cy - ry * Math.sin(a)]);
    }
    return out;
  }
  // Shapes drawn twice, a navy pass under the fill, so touching shapes of one color share one outline.
  function solid(tags, col, w) {
    w = w || LW;
    return tags.map(function (t) { return "<" + t + ' fill="' + ink + '" stroke="' + ink + '" stroke-width="' + w + '" stroke-linejoin="miter" stroke-miterlimit="8"/>'; }).join("") +
      tags.map(function (t) { return "<" + t + ' fill="' + col + '"/>'; }).join("");
  }
  function fill(tag, col, extra) { return "<" + tag + ' fill="' + col + '"' + (extra ? " " + extra : "") + "/>"; }
  function line(d, col, w, extra) { return '<path d="' + d + '" fill="none" stroke="' + (col || ink) + '" stroke-width="' + (w || 2) + '" stroke-linejoin="miter" stroke-linecap="round"' + (extra ? " " + extra : "") + "/>"; }
  function edge(d, w) { return line(d, C.orange, w || 2); }
  function bbox(list) {
    var b = [1e9, 1e9, -1e9, -1e9];
    list.forEach(function (pts) { pts.forEach(function (p) { b[0] = Math.min(b[0], p[0]); b[1] = Math.min(b[1], p[1]); b[2] = Math.max(b[2], p[0]); b[3] = Math.max(b[3], p[1]); }); });
    return b;
  }
  // Print shading: halftone dots over the right part of one polygon or a list of them (from: 0 = all of it,
  // 0.6 = its right 40%).
  function dots(shape, from, op, step, r) {
    var list = typeof shape[0][0] === "number" ? [shape] : shape, b = bbox(list), id = "kpl" + ++uid, s = step || 4.2;
    var x0 = b[0] + (b[2] - b[0]) * (from || 0);
    return '<defs><pattern id="' + id + 'd" width="' + s + '" height="' + s + '" patternUnits="userSpaceOnUse"><circle cx="' + s / 2 + '" cy="' + s / 2 + '" r="' + (r || 1.1) + '" fill="' + ink + '"/></pattern>' +
      '<clipPath id="' + id + 'c">' + list.map(function (pts) { return '<path d="' + polyD(pts) + '"/>'; }).join("") + "</clipPath></defs>" +
      '<rect x="' + n1(x0 - 1) + '" y="' + n1(b[1] - 1) + '" width="' + n1(b[2] - x0 + 2) + '" height="' + n1(b[3] - b[1] + 2) + '" fill="url(#' + id + 'd)" opacity="' + (op || 0.28) + '" clip-path="url(#' + id + 'c)"/>';
  }
  // A liquid in a vessel: everything below level y, clipped to the vessel's inside, with its surface line.
  function liquid(pts, y, col, extra) {
    var id = "kpl" + ++uid, b = bbox([pts]);
    return '<defs><clipPath id="' + id + 'v"><path d="' + polyD(pts) + '"/></clipPath></defs><g clip-path="url(#' + id + 'v)">' +
      '<rect x="' + n1(b[0] - 2) + '" y="' + n1(y) + '" width="' + n1(b[2] - b[0] + 4) + '" height="' + n1(b[3] - y + 2) + '" fill="' + col + '"/>' +
      line("M" + P(b[0] - 2, y) + " H" + n1(b[2] + 2), ink, 1.6) + (extra || "") + "</g>";
  }
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function text(x, y, size, t, col, extra) {
    return '<text x="' + n1(x) + '" y="' + n1(y) + '" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="' + size + '" fill="' + col + '"' + (extra ? " " + extra : "") + ">" + esc(t) + "</text>";
  }
  // A moving part: an untransformed group with its pivot.
  function part(cls, ox, oy, inner, extra) { return '<g class="' + cls + '" data-ox="' + n1(ox) + '" data-oy="' + n1(oy) + '"' + (extra ? " " + extra : "") + ">" + inner + "</g>"; }
  function wrap(name, inner) { return '<g class="prop-' + name + '" data-ox="0" data-oy="0">' + inner + "</g>"; }
  // A smoke puff of three circles around (cx, cy), radius r.
  function puff(cx, cy, r, col) {
    var cs = [[cx, cy, r], [cx - r * 0.72, cy + r * 0.3, r * 0.62], [cx + r * 0.74, cy + r * 0.34, r * 0.56]];
    return solid(cs.map(function (c) { return circ(c[0], c[1], c[2]); }), col || C.peri, 3.2) + fill(circ(cx - r * 0.32, cy - r * 0.34, r * 0.3), C.cream, 'opacity="0.55"');
  }
  // A column of three puffs rising (and drifting right) from (x, y): <g class="pre-smoke" data-i> holding
  // three .pre-puff groups, each pivoting on its own center (grow them, float them up, fade them).
  function smoke(pre, x, y, s, i) {
    return '<g class="' + pre + '-smoke" data-i="' + i + '">' + [[5, -14, 9], [16, -34, 12], [32, -58, 15]].map(function (p) {
      var cx = x + p[0] * s, cy = y + p[1] * s;
      return part(pre + "-puff", cx, cy, puff(cx, cy, p[2] * s));
    }).join("") + "</g>";
  }
  // A paper bill without legs, centered on (cx, cy), w wide: money green, its seal saying what it buys.
  function bill(cx, cy, w, kind) {
    var h = w * 0.52, d = C.moneyDark;
    return solid([poly(R(cx - w / 2, cy - h / 2, w, h))], C.money, 3) +
      '<rect x="' + n1(cx - w * 0.42) + '" y="' + n1(cy - h * 0.34) + '" width="' + n1(w * 0.84) + '" height="' + n1(h * 0.68) + '" fill="none" stroke="' + d + '" stroke-width="1.3"/>' +
      '<ellipse cx="' + n1(cx) + '" cy="' + n1(cy) + '" rx="' + n1(w * 0.13) + '" ry="' + n1(h * 0.3) + '" fill="' + C.cream + '" stroke="' + d + '" stroke-width="1.2"/>' +
      (kind === "war" || kind === "med" ? K.moneySeal(kind, cx + w * 0.31, cy, h * 0.2) : fill(circ(cx + w * 0.31, cy, h * 0.11), "none", 'stroke="' + d + '" stroke-width="1.2"'));
  }
  // A classical column, x the center, from the base at y0 up to the capital's top at y1.
  function column(x, y0, y1, w) {
    var shaft = R(x - w / 2, y1 + 7, w, y0 - y1 - 14);
    return solid([poly(shaft)], C.cream, 3.2) + dots(shaft, 0.55, 0.3) +
      line("M" + P(x - w * 0.18, y1 + 10) + " V" + n1(y0 - 10) + " M" + P(x + w * 0.18, y1 + 10) + " V" + n1(y0 - 10), ink, 1.2, 'opacity="0.55"') +
      solid([poly(R(x - w / 2 - 5, y1, w + 10, 7)), poly(R(x - w / 2 - 4, y0 - 7, w + 8, 7))], C.cream, 3.2);
  }
  // Wide stone steps: n steps of height sh, the bottom one w wide, each next one 2 * dw narrower.
  function steps(w, n, sh, dw, col) {
    var out = "";
    for (var i = 0; i < n; i++) out += solid([poly(R(-w / 2 + i * dw, -(i + 1) * sh, w - 2 * i * dw, sh))], col || C.cream, 3);
    return out;
  }

  // ── Factory ──────────────────────────────────────────────────────────
  // The war factory: a brick hall whose chimneys are three grinning missiles standing on the roof, puffing
  // smoke, with a big loading door a person fits in (172 tall), a sawtooth roof and lit windows. 432 x 417 (351 without smoke).
  // o: { label (default "WEAPONS"; "" for no sign), smoke (default true), sign "lit" (the sign glows) }
  // Parts: .factory-chimney (data-i 0..2; pivot the missile's base center on the roof: launch it, wobble it),
  // .factory-smoke (data-i) > .factory-puff (pivot each puff's center), .factory-sign (pivot its top center (0,-206)),
  // .factory-door (the rolling shutter of the main door; pivot its top edge (0,-172): scaleY 0 rolls it up onto
  // the dark inside), .factory-side-door (pivot (170,-118), the same).
  function missileChimney(x, yb, h) {
    var bw = 15, yt = yb - h, yn = yt + 34;
    var fin = [[x - bw, yb - 46], [x - bw - 19, yb - 12], [x - bw - 19, yb], [x - bw, yb]];
    var nose = [[x - bw, yn], [x + bw, yn], [x + bw * 0.6, yt + 11], [x + 5, yt], [x - 5, yt], [x - bw * 0.6, yt + 11]];
    return solid([poly(fin), poly(mirror(fin, x))], C.war, 3.4) + solid([poly(R(x - bw, yn, 2 * bw, yb - yn))], C.war) + solid([poly(nose)], C.cream) +
      fill(poly([[x - 5, yt], [x + 5, yt], [x + 4, yt + 4], [x - 4, yt + 4]]), ink) + line("M" + P(x - bw * 0.6 + 2, yt + 13) + " L" + P(x - bw + 3, yn - 2), ink, 1.2, 'opacity="0.5"') +
      solid([poly(R(x - bw, yb - 22, 2 * bw, 8))], C.yellow, 2.4) +
      line("M" + P(x - bw + 5, yb - 28) + " V" + n1(yn + 6), C.cream, 2.6, 'opacity="0.6"') +
      fill(circ(x - 5.5, yn + 14, 2.3), ink) + fill(circ(x + 5.5, yn + 14, 2.3), ink) + line("M" + P(x - 7, yn + 21) + " Q" + P(x, yn + 28) + " " + P(x + 7, yn + 21), ink, 2.2);
  }
  K.props.factory = function (o) {
    o = o || {};
    var label = o.label === undefined ? "WEAPONS" : o.label, out = "", fumes = "", roof = -222;
    // the sawtooth roof on the right, its glazing lit
    for (var i = 0; i < 3; i++) {
      var x0 = 80 + i * 42;
      out += solid([poly([[x0, roof + 1], [x0, roof - 36], [x0 + 42, roof + 1]])], C.slate) +
        solid([poly([[x0, roof + 1], [x0, roof - 34], [x0 + 9, roof - 27.3], [x0 + 9, roof + 1]])], C.yellow, 2.4) +
        edge("M" + P(x0 + 11, roof - 26) + " L" + P(x0 + 39, roof - 2.5));
    }
    // the chimneys: three missiles on the roof, nose up, smoke out of the nose
    [[-150, 108], [-62, 130], [26, 100]].forEach(function (c, j) {
      out += part("factory-chimney", c[0], roof + 1, missileChimney(c[0], roof + 1, c[1]), 'data-i="' + j + '"');
      if (o.smoke !== false) fumes += smoke("factory", c[0], roof + 1 - c[1], 0.9, j);
    });
    // the brick hall and its parapet
    var wall = R(-210, -210, 420, 210);
    out += solid([poly(wall)], C.rust) + dots(wall, 0.55, 0.22) + edge("M206,-206 V-4") +
      solid([poly(R(-216, roof, 432, 12))], C.slate) + edge("M-212," + (roof + 2) + " H212") +
      solid([poly(R(-214, -6, 428, 6))], C.slate, 3);
    // tall factory windows, lit (it works nights)
    [-188, -124, 70].forEach(function (x) {
      out += solid([poly(R(x, -150, 54, 110))], C.yellow, 3.6) +
        line("M" + n1(x + 18) + ",-150 V-40 M" + n1(x + 36) + ",-150 V-40 M" + x + ",-122 H" + (x + 54) + " M" + x + ",-95 H" + (x + 54) + " M" + x + ",-68 H" + (x + 54), ink, 2) +
        solid([poly(R(x - 4, -40, 62, 6))], C.slate, 2.4);
    });
    // the main loading door: the dark inside, a rolling shutter over it, a hazard band over that
    var band = R(-62, -182, 124, 10), bid = "kpl" + ++uid, stripes = "";
    for (var sx = -72; sx < 66; sx += 13) stripes += "M" + P(sx, -172) + " L" + P(sx + 10, -182) + " ";
    var shutter = solid([poly(R(-56, -172, 112, 172))], C.navy, 3.6);
    for (var y = -160; y < -4; y += 12) shutter += line("M-54," + y + " H54", C.peri, 2.2);
    shutter += edge("M53,-170 V-6") + solid([poly(R(-12, -14, 24, 6))], C.slate, 2);
    out += fill(poly(R(-56, -172, 112, 172)), C.ink) + part("factory-door", 0, -172, shutter) +
      solid([poly(band)], C.yellow, 3) + '<defs><clipPath id="' + bid + '"><path d="' + polyD(band) + '"/></clipPath></defs>' + line(stripes, ink, 4.5, 'clip-path="url(#' + bid + ')"');
    // the side door (for the conveyor)
    var side = solid([poly(R(146, -118, 48, 118))], C.navy, 3.4);
    for (var y2 = -108; y2 < -4; y2 += 11) side += line("M148," + y2 + " H192", C.peri, 2);
    out += fill(poly(R(146, -118, 48, 118)), C.ink) + part("factory-side-door", 170, -118, side) + solid([poly(R(142, -126, 56, 8))], C.yellow, 2.6);
    // the sign
    if (label) {
      var w = Math.max(150, label.length * 15 + 46), lit = o.sign === "lit";
      out += part("factory-sign", 0, -206, solid([poly(R(-w / 2, -206, w, 30))], lit ? C.yellow : C.cream, 3.4) +
        K.star(-w / 2 + 13, -191, 8, C.war) + K.star(w / 2 - 13, -191, 8, C.war) + text(0, -183, 22, label, ink, 'letter-spacing="2"'));
    }
    return wrap("factory", out + fumes);
  };

  // ── Hospital ─────────────────────────────────────────────────────────
  // A three-storey hospital: cream walls, a teal cornice with its name, an H sign on a post, a teal canopy over
  // glass double doors (140 tall), and an OPEN / CLOSED sign hanging on the doors. 320 x 364.
  // o: { sign "open" (default) | "closed", label (default "HOSPITAL"; "" for none) }
  // Parts: .hospital-sign (pivot the nail (0,-128): swing it) holding .hospital-open and .hospital-closed (one
  // shown, the other at opacity 0: flip them), .hospital-h (pivot the post's foot (0,-290)), .hospital-door-l and
  // .hospital-door-r (pivots their hinges (-42,-76) and (42,-76): scaleX 0 swings a door open onto the dark inside).
  function win(cx, y, w, h, glass) {
    return solid([poly(R(cx - w / 2, y, w, h))], glass || C.cyan, 3.6) +
      line("M" + P(cx, y) + " V" + n1(y + h) + " M" + P(cx - w / 2, y + h * 0.45) + " H" + n1(cx + w / 2), ink, 2) +
      line("M" + P(cx - w / 2 + 5, y + h * 0.36) + " L" + P(cx - w / 2 + 11, y + 5), C.cream, 2.4) +
      solid([poly(R(cx - w / 2 - 4, y + h, w + 8, 5))], C.tan, 2.4);
  }
  K.props.hospital = function (o) {
    o = o || {};
    var closed = o.sign === "closed", label = o.label === undefined ? "HOSPITAL" : o.label, out = "";
    out += part("hospital-h", 0, -290, solid([poly(R(-4, -312, 8, 24))], C.slate, 3) + solid([circ(0, -336, 26)], C.med) +
      fill(circ(0, -336, 20.5), "none", 'stroke="' + C.cream + '" stroke-width="2"') +
      '<path d="' + polyD(R(-12, -348, 7, 24)) + " " + polyD(R(5, -348, 7, 24)) + " " + polyD(R(-5, -339, 10, 6)) + '" fill="' + C.cream + '"/>');
    var wall = R(-150, -272, 300, 272);
    out += solid([poly(wall)], C.cream) + dots(wall, 0.62, 0.3) + solid([poly(R(-160, -292, 320, 22))], C.med) + edge("M-156,-272 H156", 1.6) +
      (label ? text(0, -275, 16, label, C.cream, 'letter-spacing="4"') : "");
    [-258, -208].forEach(function (y) { [-108, -36, 36, 108].forEach(function (x) { out += win(x, y, 40, 36); }); });
    out += win(-108, -124, 44, 46) + win(108, -124, 44, 46);
    // the canopy, the doors and the step
    out += fill(poly(R(-42, -146, 84, 140)), C.ink);
    var leaf = function (x0, cls, hx) {
      return part(cls, hx, -76, solid([poly(R(x0, -146, 42, 140))], C.slate, 3.4) + solid([poly(R(x0 + 7, -136, 28, 90))], C.cyan, 2.6) +
        line("M" + P(x0 + 11, -56) + " L" + P(x0 + 18, -128), C.cream, 2.4) + edge("M" + P(x0 + 40, -144) + " V-8", 1.6));
    };
    out += leaf(-42, "hospital-door-l", -42) + leaf(0, "hospital-door-r", 42);
    out += solid([poly([[-58, -160], [58, -160], [64, -146], [-64, -146]])], C.med) + edge("M-60,-148 H60", 1.6) + solid([poly(R(-54, -6, 108, 6))], C.tan, 3);
    // the OPEN / CLOSED sign on the doors
    var board = function (cls, col, word, show) {
      return '<g class="' + cls + '"' + (show ? "" : ' opacity="0"') + ">" + solid([poly(R(-33, -112, 66, 24))], col, 3) + text(0, -94.5, 15, word, C.cream, 'letter-spacing="1.5"') + "</g>";
    };
    out += part("hospital-sign", 0, -128, line("M-22,-112 L0,-128 L22,-112", ink, 1.6) + fill(circ(0, -128, 2.6), ink) +
      board("hospital-open", C.med, "OPEN", !closed) + board("hospital-closed", C.war, "CLOSED", closed));
    return wrap("hospital", out);
  };

  // ── Lab ──────────────────────────────────────────────────────────────
  // A lab bench (waist high, top at y -96) of bubbling glassware: a rack of test tubes, a big Erlenmeyer flask,
  // a round flask boiling over a burner on a tripod, a glass tube over to a beaker. 312 x 255.
  // o: { liquid "med" (teal, default) | "war" (red) | "money" (green) | "gold": the flask and the beaker,
  //      fire (default true): the burner's flame }
  // Parts: .lab-bubbles (data-i 0 = the Erlenmeyer's, 1 = the beaker's) > .lab-bubble (pivot each bubble's
  // center: float them up, pop them), .lab-flame (pivot the burner's nozzle (52,-128); its tongues are KIT.flames
  // .flame groups: KIT.flicker(tl, el, t0, t1)), .lab-drip (pivot the tube's end (122,-162): drop it into the
  // beaker), .lab-flask (the Erlenmeyer; pivot its base center (-40,-96): shake it).
  var LIQ = { med: C.med, war: C.war, money: C.money, gold: C.yellow };
  K.props.lab = function (o) {
    o = o || {};
    var liq = LIQ[o.liquid] || C.med, out = "", top = -96;
    // the bench
    var cab = R(-146, -86, 292, 78);
    out += solid([poly(cab)], C.tan) + dots(cab, 0.6, 0.26);
    [-138, -44, 50].forEach(function (x) {
      out += line("M" + P(x, -79) + " h88 v64 h-88 Z", ink, 1.6, 'opacity="0.6"') + solid([poly(R(x + 36, -72, 16, 5))], C.slate, 2);
    });
    out += solid([poly(R(-140, -8, 280, 8))], C.slate, 3) + solid([poly(R(-156, top, 312, 11))], C.slate) + edge("M-152," + (top + 2) + " H152", 1.8);
    // the test tubes in their rack
    [[-129, C.war], [-116, C.med], [-103, C.yellow]].forEach(function (t) {
      var x = t[0], tube = [[x - 5, -164], [x + 5, -164], [x + 5, -114], [x + 2, -107], [x - 2, -107], [x - 5, -114]];
      out += solid([poly(tube)], C.cream, 3) + liquid(tube, -134, t[1]) + line("M" + P(x - 2, -158) + " V-140", C.cream, 1.6);
    });
    out += solid([poly(R(-144, -142, 6, 36)), poly(R(-92, -142, 6, 36))], C.tan, 3) + solid([poly(R(-146, -142, 62, 7)), poly(R(-146, -107, 62, 11))], C.tan, 3);
    // the Erlenmeyer flask
    var fx = -40, flask = [[fx - 40, top], [fx + 40, top], [fx + 9, top - 58], [fx + 9, top - 92], [fx + 13, top - 97], [fx - 13, top - 97], [fx - 9, top - 92], [fx - 9, top - 58]];
    var inner = [[fx - 26, -104, 3], [fx - 6, -114, 2.6], [fx + 16, -106, 3.4], [fx + 4, -126, 2.2]].map(function (b) { return fill(circ(b[0], b[1], b[2]), C.cream, 'stroke="' + ink + '" stroke-width="1.2"'); }).join("");
    out += part("lab-flask", fx, top, solid([poly(flask)], C.cream) + liquid(flask, -134, liq, inner) +
      line("M" + P(fx - 30, top - 8) + " L" + P(fx - 8, top - 52), C.cream, 3) + line("M" + P(fx + 20, -128) + " h8 M" + P(fx + 25, -116) + " h8", ink, 1.4, 'opacity="0.6"'));
    // the burner, its flame, the tripod and the round flask on it
    var bx = 52;
    out += solid([poly([[bx - 18, top], [bx + 18, top], [bx + 14, top - 8], [bx - 14, top - 8]])], C.slate, 3) +
      solid([poly([[bx - 5, top - 8], [bx + 5, top - 8], [bx + 4, -128], [bx - 4, -128]])], C.peri, 2.6) + solid([poly(R(bx - 7, -118, 14, 5))], C.slate, 2.2);
    if (o.fire !== false) out += part("lab-flame", bx, -128, K.flames(bx, -128, 0.26));
    out += solid([poly([[bx - 28, -158], [bx - 22, -158], [bx - 30, top], [bx - 36, top]]), poly([[bx + 28, -158], [bx + 22, -158], [bx + 30, top], [bx + 36, top]])], C.slate, 3) +
      solid([poly(R(bx - 33, -164, 66, 6))], C.slate, 3);
    var rf = [[bx + 7, -226]].concat(arc(bx, -190, 26, 26, 74.4, -254.4, 16)).concat([[bx - 7, -226]]);
    var boil = [[bx - 12, -176, 3], [bx + 6, -170, 2.4], [bx + 13, -182, 2]].map(function (b) { return fill(circ(b[0], b[1], b[2]), C.cream, 'stroke="' + ink + '" stroke-width="1.2"'); }).join("");
    out += solid([poly(rf)], C.cream) + liquid(rf, -188, C.orange, boil) + line("M" + P(bx - 18, -198) + " L" + P(bx - 10, -208), C.cream, 2.6) +
      solid([poly(R(bx - 9, -234, 18, 10))], C.rust, 2.6);
    // the glass tube to the beaker, and the beaker
    out += line("M" + bx + ",-232 V-248 H122 V-166", ink, 8) + line("M" + bx + ",-232 V-248 H122 V-166", C.cream, 3.6);
    var bk = [[108, top], [148, top], [148, -172], [151, -177], [105, -177], [108, -172]];
    out += solid([poly(bk)], C.cream) + liquid(bk, -142, liq) + line("M140,-112 h7 M140,-127 h7 M140,-142 h7 M140,-157 h7", ink, 1.4) +
      line("M114,-106 L114,-150", C.cream, 2.6) +
      part("lab-drip", 122, -162, '<path d="M122,-160 q-4,6 0,9 q4,-3 0,-9 Z" fill="' + liq + '" stroke="' + ink + '" stroke-width="1.4"/>');
    // the bubbles over the flask and the beaker
    var bub = function (i, list) {
      return '<g class="lab-bubbles" data-i="' + i + '">' + list.map(function (b) { return part("lab-bubble", b[0], b[1], solid([circ(b[0], b[1], b[2])], C.cream, 2.4) + fill(circ(b[0] - b[2] * 0.35, b[1] - b[2] * 0.35, b[2] * 0.28), liq)); }).join("") + "</g>";
    };
    out += bub(0, [[fx + 3, -204, 5], [fx - 7, -222, 7], [fx + 5, -246, 9]]) + bub(1, [[139, -186, 4], [144, -200, 5.5], [138, -217, 7]]);
    return wrap("lab", out);
  };

  // ── House ────────────────────────────────────────────────────────────
  // A 1950s suburban ranch house: a long low hip roof with a brick chimney and a TV antenna, a picture window
  // with shutters, a front door (146 tall) with a diamond window, a garage wing, shrubs. 450 x 344.
  // o: { variant 0..3 (wall, roof and door colors, for a street of them), lit (windows glowing yellow),
  //      smoke (default true) }
  // Parts: .house-door (pivot the hinge (-46,-79): scaleX 0 opens it), .house-lit (the window glow, all windows;
  // tween its opacity), .house-smoke > .house-puff (pivot each puff's center), .house-antenna (pivot its foot
  // (40,-236): wobble it).
  var HOUSE = [
    { wall: C.cream, roof: C.slate, door: C.war, trim: C.peri, garage: C.tan },
    { wall: C.cyan, roof: C.rust, door: C.yellow, trim: C.cream, garage: C.cream },
    { wall: C.yellow, roof: C.slate, door: C.med, trim: C.peri, garage: C.cream },
    { wall: C.tan, roof: C.navy, door: C.orange, trim: C.cream, garage: C.cream },
  ];
  function siding(x0, x1, y0) {
    var d = "";
    for (var y = y0 + 13; y < -4; y += 13) d += "M" + x0 + "," + y + " H" + x1 + " ";
    return line(d, ink, 1.2, 'opacity="0.2"');
  }
  function shrub(cx, w, h) {
    var pts = [[cx - w / 2, 0], [cx - w / 2 + 3, -h * 0.55], [cx - w * 0.22, -h], [cx + w * 0.12, -h * 0.9], [cx + w / 2 - 3, -h * 0.5], [cx + w / 2, 0]];
    return solid([poly(pts)], C.moneyDark, 3.4) + fill(poly([[cx - w * 0.22, -h + 3], [cx - w * 0.06, -h * 0.55], [cx - w * 0.34, -h * 0.5]]), C.money) +
      line("M" + P(cx + w * 0.05, -h * 0.4) + " l6,-6 M" + P(cx - w * 0.25, -h * 0.25) + " l5,-5", C.money, 2);
  }
  K.props.house = function (o) {
    o = o || {};
    var v = HOUSE[(o.variant || 0) % HOUSE.length], lit = o.lit ? 1 : 0, out = "";
    // the chimney and the antenna, behind the roof
    out += solid([poly(R(-176, -274, 34, 70))], C.rust) + line("M-176,-260 H-142 M-176,-246 H-142 M-176,-232 H-142 M-160,-274 V-260 M-168,-260 V-246 M-152,-246 V-232", ink, 1.3, 'opacity="0.45"') +
      solid([poly(R(-181, -282, 44, 9))], C.slate);
    out += part("house-antenna", 40, -236, line("M40,-232 V-302", ink, 3) + line("M18,-292 L40,-296 L62,-292 M23,-280 L40,-284 L57,-280 M28,-268 L40,-272 L52,-268", ink, 2.6) + line("M40,-302 L52,-312", ink, 2.2));
    // the main block and its hip roof
    var mw = R(-200, -178, 300, 178);
    out += solid([poly(mw)], v.wall) + siding(-198, 98, -178) + dots(mw, 0.62, 0.24);
    var roof = [[-228, -170], [126, -170], [86, -236], [-188, -236]];
    out += solid([poly(roof)], v.roof) + line("M-218,-186 H118 M-208,-203 H108 M-198,-220 H98", ink, 1.4, 'opacity="0.45"') +
      solid([poly(R(-230, -174, 358, 8))], v.trim, 3) + (v.roof === C.slate || v.roof === C.navy ? edge("M-185,-234 H84") : "");
    // the picture window with its shutters and curtains, and the small window
    var pane = function (x, y, w, h, split) {
      var g = solid([poly(R(x, y, w, h))], C.slate, 3.6) + '<g class="house-lit"' + (lit ? "" : ' opacity="0"') + ">" + fill(poly(R(x, y, w, h)), C.yellow) + "</g>" +
        fill(poly([[x, y], [x + w * 0.24, y], [x + w * 0.1, y + h * 0.7], [x, y + h]]), C.cream) + fill(poly([[x + w, y], [x + w * 0.76, y], [x + w * 0.9, y + h * 0.7], [x + w, y + h]]), C.cream) +
        line("M" + P(x, y) + " L" + P(x + w * 0.1, y + h * 0.7) + " L" + P(x, y + h) + " M" + P(x + w, y) + " L" + P(x + w * 0.9, y + h * 0.7) + " L" + P(x + w, y + h), ink, 1.4);
      for (var i = 1; i < split; i++) g += line("M" + P(x + (w * i) / split, y) + " V" + n1(y + h), ink, 2.2);
      return g + line("M" + P(x + w * 0.4, y + h - 6) + " L" + P(x + w * 0.55, y + 8), C.cream, 2.2, 'opacity="0.7"') + solid([poly(R(x - 5, y + h, w + 10, 6))], v.trim, 2.6);
    };
    var shutter = function (x, y, h) {
      var s = solid([poly(R(x, y, 15, h))], v.trim, 3);
      for (var yy = y + 7; yy < y + h - 3; yy += 7) s += line("M" + P(x + 3, yy) + " h9", ink, 1.2, 'opacity="0.6"');
      return s;
    };
    out += shutter(-196, -148, 70) + shutter(-66, -148, 70) + pane(-178, -146, 108, 66, 3) + pane(30, -142, 48, 46, 2);
    // the front door, its frame, the porch light and the stoop
    var door = solid([poly(R(-46, -152, 50, 146))], v.door) + solid([poly([[-21, -136], [-11, -122], [-21, -108], [-31, -122]])], C.cyan, 2.4) +
      line("M-38,-92 h34 v40 h-34 Z M-38,-44 h34 v30 h-34 Z", ink, 1.4, 'opacity="0.55"') + solid([circ(-6, -76, 3.6)], C.yellow, 2) +
      (v.door === C.war || v.door === C.med || v.door === C.orange ? edge("M2,-150 V-8", 1.6) : "");
    out += solid([poly(R(-53, -159, 64, 159))], v.trim, 3) + fill(poly(R(-46, -152, 50, 146)), C.ink) + part("house-door", -46, -79, door) +
      solid([poly([[18, -132], [28, -132], [30, -120], [16, -120]])], C.yellow, 2.4) + solid([poly(R(-62, -6, 82, 6))], C.slate, 3);
    // the garage wing, in front of the main roof
    var gw = R(100, -150, 106, 150);
    out += solid([poly(gw)], v.wall) + siding(102, 204, -150) + dots(gw, 0.4, 0.24) +
      solid([poly([[88, -144], [218, -144], [153, -214]])], v.roof) + line("M108,-160 H198 M124,-178 H182 M141,-196 H165", ink, 1.4, 'opacity="0.45"') +
      solid([poly([[86, -146], [153, -218], [220, -146], [210, -146], [153, -207], [96, -146]])], v.trim, 3) + solid([circ(153, -168, 8)], C.slate, 2.6);
    var gd = R(116, -118, 74, 118);
    out += solid([poly(gd)], v.garage) + dots(gd, 0.5, 0.25) + line("M118,-96 H188 M118,-72 H188 M118,-48 H188 M118,-24 H188", ink, 1.6, 'opacity="0.6"') +
      [124, 141, 158, 175].map(function (x) { return solid([poly(R(x, -112, 11, 9))], C.slate, 2); }).join("");
    // shrubs along the front
    out += shrub(-182, 46, 34) + shrub(-136, 56, 44) + shrub(-90, 46, 30) + shrub(38, 40, 28);
    if (o.smoke !== false) out += smoke("house", -159, -282, 0.85, 0);
    return wrap("house", out);
  };

  // ── Printing press ───────────────────────────────────────────────────
  // A cast-iron screw press that stamps out green papers: a bed at waist height, a plate on a screw, a crank
  // wheel on the right (a person turns it by its knob), a paper tray on the left. 369 x 346.
  // o: { seal "war" | "med" | "plain" (default): the die's seal and the sheet on the bed, label (a plaque on the
  //      crosshead, for example "1913"), tray (sheets of blank paper in the tray, default 3; 0 = empty: a dark
  //      hole for the moth) }
  // Parts: .press-plate (the plate, its die and its screw; pivot its top (0,-346); moves straight down by
  // data-travel = 46 to stamp the sheet), .press-sheet (the green sheet lying on the bed; pivot its center (0,-97):
  // pop it out toward the camera), .press-crank (the wheel; pivot its axle (136,-150): rotate it; its knob is at
  // (178,-183) before turning), .press-tray (pivot where it bolts on (-112,-170)) holding .press-tray-paper.
  K.props.printingPress = function (o) {
    o = o || {};
    var seal = o.seal === "war" || o.seal === "med" ? o.seal : "plain", sheets = o.tray === undefined ? 3 : o.tray, out = "";
    // the tray on the left: its dark mouth, its blank sheets, its front
    var paper = "";
    for (var i = 0; i < Math.min(sheets, 5); i++) {
      var dx = -2 + i * 5, rot = -8 + i * 6;
      paper += '<g transform="translate(' + (-148 + dx) + ",-216) rotate(" + rot + ')">' + solid([poly(R(-22, -16, 44, 30))], C.cream, 3) + line("M-14,-8 H12 M-14,-1 H8", ink, 1.2, 'opacity="0.35"') + "</g>";
    }
    out += part("press-tray", -112, -170, fill(poly([[-184, -214], [-116, -214], [-112, -196], [-180, -196]]), C.ink, 'stroke="' + ink + '" stroke-width="3" stroke-linejoin="miter"') +
      '<g class="press-tray-paper">' + paper + "</g>" + solid([poly([[-180, -198], [-112, -198], [-112, -150], [-172, -150]])], C.tan) + dots([[-180, -198], [-112, -198], [-112, -150], [-172, -150]], 0.5, 0.28) +
      edge("M-178,-196 H-114", 1.6));
    // the bed's top, and the green sheet lying on it
    out += solid([poly([[-118, -90], [118, -90], [108, -104], [-108, -104]])], C.peri) + dots([[-118, -90], [118, -90], [108, -104], [-108, -104]], 0.6, 0.3) +
      part("press-sheet", 0, -97, '<g transform="translate(0,-97) scale(1,0.26)">' + bill(0, 0, 100, seal) + "</g>");
    // the plate on its screw (behind the crosshead)
    var rod = R(-7, -340, 14, 192), thread = "";
    for (var y = -334; y < -186; y += 8) thread += "M-7," + y + " L7," + (y - 5) + " ";
    var plate = solid([poly(rod)], C.tan, 3.2) + line(thread, ink, 1.3, 'opacity="0.55"') + solid([poly(R(-12, -346, 24, 10))], C.slate, 3) +
      solid([poly([[-82, -178], [82, -178], [86, -152], [-86, -152]])], C.slate) + edge("M-82,-154 H82") +
      solid([poly(R(-70, -152, 140, 6))], C.money, 2.6) + solid([circ(-68, -165, 4), circ(68, -165, 4)], C.peri, 2) +
      (seal === "plain" ? fill('ellipse cx="0" cy="-165" rx="8" ry="9"', C.cream, 'stroke="' + ink + '" stroke-width="2"') : K.moneySeal(seal, 0, -165, 9));
    out += part("press-plate", 0, -346, plate, 'data-travel="46"');
    // the frame: columns, crosshead, bed, plinth
    out += solid([poly(R(-116, -292, 28, 202)), poly(R(88, -292, 28, 202))], C.slate) + edge("M-91,-288 V-94") + edge("M113,-288 V-94") +
      solid([poly([[-134, -314], [134, -314], [126, -286], [-126, -286]])], C.navy) + edge("M-124,-288 H124") +
      solid([circ(-112, -300, 3.6), circ(112, -300, 3.6)], C.peri, 2) +
      (o.label ? solid([poly(R(-44, -310, 88, 20))], C.yellow, 2.6) + text(0, -294, 15, o.label, ink, 'letter-spacing="2"') : "") +
      solid([poly(R(-118, -90, 236, 50))], C.navy) + edge("M-116,-88 H116") + line("M-100,-64 H100", C.peri, 2, 'opacity="0.7"') +
      solid([poly([[-132, -40], [132, -40], [140, 0], [-140, 0]])], C.slate) + edge("M-130,-38 H130");
    // the crank wheel on the right
    // an open wheel: a rim and six spokes, the background showing between them
    var spokes = "";
    for (var k = 0; k < 6; k++) {
      var a = (k * Math.PI) / 3 + 0.2;
      spokes += "M" + P(136, -150) + " L" + P(136 + 40 * Math.cos(a), -150 - 40 * Math.sin(a)) + " ";
    }
    var crank = line(spokes, ink, 10.5) + line(spokes, C.navy, 6) + fill(circ(136, -150, 41), "none", 'stroke="' + ink + '" stroke-width="15"') +
      fill(circ(136, -150, 41), "none", 'stroke="' + C.navy + '" stroke-width="9.6"');
    crank += edge("M" + P(136 + 44 * Math.cos(-0.9), -150 - 44 * Math.sin(-0.9)) + " A44,44 0 0 0 " + P(136 + 44 * Math.cos(0.9), -150 - 44 * Math.sin(0.9)), 2.4) +
      solid([circ(136, -150, 9)], C.peri, 3) + solid([poly([[166, -173], [176, -186], [182, -182], [172, -169]])], C.tan, 2.6) + solid([circ(178, -183, 7)], C.yellow, 2.6);
    out += part("press-crank", 136, -150, crank);
    return wrap("printingPress", out);
  };

  // ── Headstone ────────────────────────────────────────────────────────
  // A gray stone slab with a faceted round top, an engraved line or two, a crack, on a fresh dirt mound with
  // tufts of grass. 132 x 126 (about chest high to a person).
  // o: { text (default "RIP"; "\n" for a second line), flowers (a little bunch leaning on it) }
  // Parts: .headstone-stone (the slab and its text; pivot its foot (0,-4): rise it out of the mound, wobble it),
  // .headstone-flowers (pivot their stems' foot (30,-12)).
  K.props.headstone = function (o) {
    o = o || {};
    var lines = String(o.text === undefined ? "RIP" : o.text).split("\n"), out = "";
    var face = [[-40, -4]].concat(arc(0, -80, 40, 40, 180, 0, 8)).concat([[40, -4]]);
    var longest = lines.reduce(function (m, l) { return Math.max(m, l.length); }, 1);
    var size = Math.min(30, 66 / (0.52 * longest), 62 / lines.length), lh = size * 1.05, y0 = -70 - ((lines.length - 1) * lh) / 2 + size * 0.36;
    var words = lines.map(function (l, i) {
      return text(1.4, y0 + i * lh + 1.4, n1(size), l, ink, 'letter-spacing="1"') + text(0, y0 + i * lh, n1(size), l, C.cream, 'letter-spacing="1"');
    }).join("");
    var stone = solid([poly(shift(face, 9, -6))], C.slate) + solid([poly(face)], C.peri) + dots(face, 0.55, 0.32) +
      edge("M" + P(37, -84) + " L" + P(31, -102), 1.6) + line("M-40,-64 L-31,-60 L-35,-51 L-27,-47", ink, 1.8) + words;
    out += part("headstone-stone", 0, -4, stone);
    var mound = [[-64, 0], [-56, -9], [-34, -15], [0, -17], [36, -15], [58, -8], [68, 0]];
    out += solid([poly(mound)], C.rust, 3.6) + dots(mound, 0.4, 0.3);
    [-58, -18, 52].forEach(function (x) {
      out += solid([poly([[x - 6, 0], [x - 5, -9], [x - 2, -4], [x, -13], [x + 2, -4], [x + 5, -10], [x + 7, 0]].map(function (p) { return [p[0], p[1] - (x === -18 ? 14 : 2)]; }))], C.moneyDark, 2.4);
    });
    if (o.flowers) {
      var fl = line("M30,-12 L22,-34 M30,-12 L32,-38 M30,-12 L41,-32", C.moneyDark, 2.6);
      [[22, -36, C.yellow], [32, -41, C.war], [42, -34, C.cream]].forEach(function (f) {
        fl += solid([poly(arc(f[0], f[1], 6, 6, 0, 360, 6).slice(0, 6))], f[2], 2.4) + fill(circ(f[0], f[1], 2), C.orange);
      });
      out += part("headstone-flowers", 30, -12, fl);
    }
    return wrap("headstone", out);
  };

  // ── Capitol ──────────────────────────────────────────────────────────
  // A generic domed legislature (no real building): a podium, steps, two wings, a portico of six columns in
  // front of a shadowed wall, a pediment with a star, a drum and a faceted dome with a lantern and a pennant.
  // 449 x 398.
  // o: { label (on the frieze, for example "LEGISLATURE"; default none) }
  // Parts: .capitol-dome (the dome, lantern and pennant; pivot its base center (0,-258): lift it like a lid),
  // .capitol-flag (pivot the pennant's root on the pole (0,-390): flap it with scaleX or skewY), .capitol-door (pivot its foot (0,-24)).
  K.props.capitol = function (o) {
    o = o || {};
    var out = "";
    // the drum (behind the pediment)
    var drum = R(-72, -250, 144, 64);
    out += solid([poly(drum)], C.cream) + dots(drum, 0.6, 0.3) + solid([poly(R(-78, -258, 156, 9))], C.tan, 3);
    for (var x = -60; x <= 60; x += 15) out += solid([poly(R(x - 4, -244, 8, 22))], C.slate, 2);
    // the dome, lantern and pennant
    var dome = arc(0, -258, 66, 72, 180, 0, 10), ribs = "";
    [-0.66, -0.33, 0, 0.33, 0.66].forEach(function (f) { ribs += "M" + P(66 * f, -258) + " Q" + P(66 * f * 1.12, -300) + " " + P(9 * f, -327) + " "; });
    var flag = line("M0,-366 V-398", ink, 3) + solid([poly([[2, -398], [40, -391], [2, -383]])], C.orange, 2.6) + line("M4,-390.5 H30", C.cream, 2);
    out += part("capitol-dome", 0, -258, solid([poly(dome)], C.cream) + dots(dome, 0.58, 0.32) + line(ribs, ink, 1.6) +
      [-40, -14, 14, 40].map(function (x) { return solid([poly(R(x - 3.5, -278, 7, 10))], C.slate, 1.8); }).join("") +
      solid([poly(R(-12, -352, 24, 26))], C.cream, 3) + line("M-4,-348 V-330 M4,-348 V-330", ink, 1.4) + solid([poly([[-16, -352], [16, -352], [0, -366]])], C.tan, 3) +
      part("capitol-flag", 0, -390, flag));
    // the podium and the wings
    var pod = R(-224, -22, 448, 22);
    out += solid([poly(pod)], C.cream) + dots(pod, 0.6, 0.3);
    [-1, 1].forEach(function (s) {
      var w = s < 0 ? R(-218, -130, 110, 108) : R(108, -130, 110, 108);
      out += solid([poly(w)], C.cream) + dots(w, 0.55, 0.28) + solid([poly(R(s < 0 ? -224 : 104, -142, 120, 12))], C.tan, 3) +
        solid([poly(R(s < 0 ? -220 : 108, -152, 112, 10))], C.cream, 3);
      for (var bx = 0; bx < 13; bx++) out += line("M" + n1((s < 0 ? -214 : 112) + bx * 8.6) + ",-150 v6", ink, 1.4, 'opacity="0.6"');
      [0, 1, 2].forEach(function (c) {
        var cx = (s < 0 ? -196 : 130) + c * 33;
        out += solid([poly(R(cx - 9, -114, 18, 30)), poly(R(cx - 9, -66, 18, 30))], C.navy, 3) + solid([poly(R(cx - 12, -84, 24, 4)), poly(R(cx - 12, -36, 24, 4))], C.cream, 2);
      });
    });
    // the portico: the shadowed wall, the door, the columns, the frieze and the pediment
    out += solid([poly(R(-112, -170, 224, 148))], C.slate);
    var door = solid([poly([[-12, -24], [12, -24], [12, -70], [0, -80], [-12, -70]])], C.rust, 3) + line("M0,-76 V-26", ink, 1.4) + fill(circ(5, -46, 1.8), C.yellow);
    out += part("capitol-door", 0, -24, door);
    out += steps(232, 3, 8, 9);
    [-95, -57, -19, 19, 57, 95].forEach(function (cx) { out += column(cx, -24, -152, 16); });
    out += solid([poly(R(-118, -170, 236, 18))], C.cream) + (o.label ? text(0, -156.5, 12.5, o.label, ink, 'letter-spacing="3"') : "");
    var ped = [[-126, -170], [126, -170], [0, -212]];
    out += solid([poly(ped)], C.cream) + dots(ped, 0.55, 0.3) + line("M-104,-174 L0,-206 L104,-174 Z", ink, 1.4, 'opacity="0.55"') + K.star(0, -184, 11, C.orange);
    return wrap("capitol", out);
  };

  // ── Bank ─────────────────────────────────────────────────────────────
  // A columned bank whose front door is a round vault door: a bronze frame, a steel door with bolts and a brass
  // wheel; behind it, the dark vault with stacks of cash. Its name on the frieze, a coin in the pediment.
  // 321 x 317.
  // o: { label (default "BANK"), open (the door swung open, the cash showing) }
  // Parts: .bank-vault (the door; pivot its hinge (-70,-100): scaleX to -0.3 swings it open), .bank-wheel (inside
  // the door; pivot its hub (0,-100): spin it), .bank-cash (the stacks inside; pivot their foot (0,-48)). With open: true the
  // door is drawn swung (a transformed wrapper around .bank-vault, which itself stays untransformed).
  K.props.bank = function (o) {
    o = o || {};
    var label = o.label === undefined ? "BANK" : o.label, out = "", cy = -100;
    out += solid([poly(R(-140, -236, 280, 212))], C.slate);
    // the vault: bronze frame, dark hole, cash, the door
    var hid = "kpl" + ++uid, cash = "";
    [[-44, 0], [-20, 0], [4, 0], [28, 0], [-32, 1], [-8, 1], [16, 1], [-20, 2], [4, 2], [-8, 3]].forEach(function (b) {
      var x = b[0], y = cy + 52 - b[1] * 13;
      cash += solid([poly(R(x - 11, y - 12, 22, 12))], C.money, 2.4) + solid([poly(R(x - 3, y - 12, 6, 12))], C.cream, 1.6);
    });
    cash += bill(38, cy + 38, 30, "plain");
    out += solid([circ(0, cy, 82)], C.tan) + dots([arc(0, cy, 82, 82, 0, 360, 24)], 0.55, 0.32) + solid([circ(0, cy, 70)], C.ink, 3) +
      '<defs><clipPath id="' + hid + '"><circle cx="0" cy="' + cy + '" r="69"/></clipPath></defs><g clip-path="url(#' + hid + ')">' + part("bank-cash", 0, -48, cash) + "</g>";
    var bolts = "";
    for (var i = 0; i < 12; i++) { var a = (i * Math.PI) / 6; bolts += solid([circ(58 * Math.cos(a), cy - 58 * Math.sin(a), 3.6)], C.slate, 2); }
    var wheel = "";
    for (var k = 0; k < 6; k++) { var b = (k * Math.PI) / 3 + 0.26; wheel += line("M" + P(0, cy) + " L" + P(27 * Math.cos(b), cy - 27 * Math.sin(b)), ink, 6) + line("M" + P(0, cy) + " L" + P(27 * Math.cos(b), cy - 27 * Math.sin(b)), C.yellow, 2.6) + solid([circ(28 * Math.cos(b), cy - 28 * Math.sin(b), 4.8)], C.yellow, 2.4); }
    wheel += fill(circ(0, cy, 19), "none", 'stroke="' + ink + '" stroke-width="7"') + fill(circ(0, cy, 19), "none", 'stroke="' + C.yellow + '" stroke-width="3.4"') + solid([circ(0, cy, 8)], C.yellow, 3);
    var doorD = [arc(0, cy, 66, 66, 0, 360, 28)];
    var vault = solid([poly(doorD[0])], C.peri) + dots(doorD, 0.5, 0.32) + fill(circ(0, cy, 48), "none", 'stroke="' + ink + '" stroke-width="2"') + bolts +
      solid([poly(R(-74, cy - 34, 12, 16)), poly(R(-74, cy + 18, 12, 16))], C.slate, 2.6) + edge("M" + P(52, cy - 40) + " A66,66 0 0 1 " + P(52, cy + 40), 2.4) +
      part("bank-wheel", 0, cy, wheel);
    vault = part("bank-vault", -70, cy, vault);
    out += o.open ? '<g transform="translate(-70,' + cy + ") scale(-0.3,1) translate(70," + -cy + ')">' + vault + "</g>" : vault;
    // the columns, the steps, the frieze and the pediment
    [-124, -96, 96, 124].forEach(function (cx) { out += column(cx, -24, -236, 18); });
    out += steps(320, 3, 8, 10);
    out += solid([poly(R(-152, -266, 304, 30))], C.cream) + (label ? text(0, -243.5, 22, label, ink, 'letter-spacing="6"') : "");
    var ped = [[-160, -266], [160, -266], [0, -316]];
    out += solid([poly(ped)], C.cream) + dots(ped, 0.55, 0.3) + line("M-132,-270 L0,-310 L132,-270 Z", ink, 1.4, 'opacity="0.55"') +
      solid([circ(0, -283, 11)], C.yellow, 3) + fill(circ(0, -283, 6.5), "none", 'stroke="' + ink + '" stroke-width="1.4"');
    return wrap("bank", out);
  };

  // ── World map ────────────────────────────────────────────────────────
  // An engraved map card of a made-up but world-like world: continents in halftone dots on an engraved sea,
  // curved meridians, a compass star, a navy and orange border, and a card shadow, which stands on y 0 (the card's
  // bottom edge is at y -9). w + 7 wide, 0.62 w + 9 tall.
  // o: { w (default 420), title (a red ribbon over the top edge), markers: [{ x, y, kind, label }] or
  //      [x, y, kind, label], x and y from 0 to 1 across the map (not the card), kind "pin" (default) | "war" (the
  //      money's missile seal) | "med" (its cross seal) | "boom" | "nuke" (a tiny mushroom cloud) | "skull" | "star" }
  // Parts: .map-marker (data-i, data-kind; pivot the marked point: pop it in, drop the pin), .map-land (all the
  // continents; pivot the map's center).
  // Land in a 400 x 220 map space.
  var LANDS = [
    [[22, 46], [40, 32], [62, 26], [86, 22], [112, 24], [132, 30], [146, 40], [138, 50], [126, 52], [122, 62], [132, 70], [120, 74], [108, 84], [100, 96], [96, 106], [104, 114], [98, 117], [88, 108], [84, 100], [76, 90], [66, 86], [58, 76], [46, 70], [40, 58], [30, 56]],
    [[150, 18], [168, 14], [184, 18], [178, 32], [164, 40], [154, 32]],
    [[106, 120], [120, 117], [136, 124], [148, 134], [142, 150], [130, 164], [120, 182], [110, 198], [104, 192], [102, 172], [96, 152], [94, 134]],
    [[188, 44], [198, 34], [214, 30], [232, 22], [256, 18], [284, 20], [312, 22], [340, 28], [366, 34], [384, 44], [378, 54], [364, 58], [356, 70], [342, 76], [330, 88], [318, 92], [308, 104], [300, 98], [296, 112], [290, 124], [284, 110], [278, 98], [268, 88], [256, 92], [244, 84], [232, 82], [222, 74], [210, 72], [200, 64], [192, 56]],
    [[176, 48], [184, 40], [187, 52], [180, 58]],
    [[198, 86], [214, 80], [230, 84], [244, 90], [252, 102], [262, 110], [256, 124], [246, 140], [238, 158], [226, 174], [216, 170], [212, 150], [206, 132], [196, 118], [190, 100]],
    [[262, 148], [268, 142], [271, 156], [264, 164]],
    [[318, 112], [332, 108], [338, 116], [324, 121]], [[344, 118], [356, 116], [360, 125], [348, 127]],
    [[370, 64], [376, 58], [381, 70], [374, 81]],
    [[322, 150], [340, 142], [358, 144], [372, 152], [370, 170], [356, 178], [338, 176], [326, 168]],
  ];
  function marker(kind, x, y, label) {
    var m;
    if (kind === "war" || kind === "med") m = K.moneySeal(kind, x, y, 11);
    else if (kind === "boom") {
      var pts = [];
      for (var i = 0; i < 20; i++) { var a = (i * Math.PI) / 10, r = i % 2 ? 7 : 15; pts.push([x + r * Math.cos(a), y + r * Math.sin(a)]); }
      m = solid([poly(pts)], C.war, 2.6) + fill(poly(pts.map(function (p) { return [x + (p[0] - x) * 0.5, y + (p[1] - y) * 0.5]; })), C.yellow);
    } else if (kind === "nuke") m = '<g transform="translate(' + P(x, y) + ') scale(0.075)">' + K.nuke() + "</g>";
    else if (kind === "skull") {
      m = solid([poly([[x - 9, y - 4], [x - 7, y - 13], [x, y - 16], [x + 7, y - 13], [x + 9, y - 4], [x + 6, y + 1], [x + 5, y + 6], [x - 5, y + 6], [x - 6, y + 1]])], C.cream, 2.6) +
        fill(poly([[x - 7, y - 6], [x - 2, y - 7], [x - 2.5, y - 2], [x - 6, y - 2.5]]), ink) + fill(poly([[x + 7, y - 6], [x + 2, y - 7], [x + 2.5, y - 2], [x + 6, y - 2.5]]), ink) + line("M" + P(x - 3, y + 3) + " h6", ink, 1.4);
    } else if (kind === "star") m = solid([poly(arc(x, y, 12, 12, 90, 450, 10).slice(0, 10).map(function (p, i) { return i % 2 ? [x + (p[0] - x) * 0.45, y + (p[1] - y) * 0.45] : p; }))], C.yellow, 2.6);
    else m = solid([poly([[x, y], [x - 7, y - 14], [x - 9, y - 22], [x - 5, y - 29], [x, y - 31], [x + 5, y - 29], [x + 9, y - 22], [x + 7, y - 14]])], C.war, 2.6) + fill(circ(x, y - 21, 3.6), C.cream);
    if (label) m += text(x, y + (kind === "pin" || !kind ? 16 : 26), 13, label, ink, 'stroke="' + C.cream + '" stroke-width="3.5" paint-order="stroke" letter-spacing="1"');
    return m;
  }
  K.props.worldMap = function (o) {
    o = o || {};
    var w = o.w || 420, h = Math.round(w * 0.62), x0 = -w / 2, y0 = -h - 9, m = Math.round(w * 0.055);
    var ix = x0 + m, iy = y0 + m, iw = w - 2 * m, ih = h - 2 * m, sx = iw / 400, sy = ih / 220;
    var at = function (p) { return [ix + p[0] * sx, iy + p[1] * sy]; };
    var out = fill(poly(R(x0 + 7, y0 + 9, w, h)), ink, 'opacity="0.85"') + solid([poly(R(x0, y0, w, h))], C.cream) +
      fill(poly(R(x0 + 7, y0 + 7, w - 14, h - 14)), "none", 'stroke="' + C.orange + '" stroke-width="2"');
    // the engraved sea and the graticule
    var sea = "";
    for (var y = iy + 5; y < iy + ih - 2; y += 6) sea += "M" + n1(ix + 2) + "," + n1(y) + " H" + n1(ix + iw - 2) + " ";
    var grid = "", cx = ix + iw / 2;
    for (var i = 1; i < 6; i++) { var gx = ix + (iw * i) / 6, bow = (gx - cx) * 0.14; grid += "M" + P(gx, iy) + " Q" + P(gx + bow, iy + ih / 2) + " " + P(gx, iy + ih) + " "; }
    for (var j = 1; j < 4; j++) grid += "M" + P(ix, iy + (ih * j) / 4) + " H" + n1(ix + iw) + " ";
    out += solid([poly(R(ix, iy, iw, ih))], C.cream, 3) + line(sea, C.peri, 1, 'opacity="0.35"') + line(grid, ink, 1.1, 'opacity="0.3" stroke-dasharray="5 4"');
    // the land
    var lands = LANDS.map(function (pts) { return pts.map(at); });
    out += part("map-land", cx, iy + ih / 2, solid(lands.map(function (pts) { return poly(pts); }), C.cream, 3) + dots(lands, 0, 0.55, 5, 1.5));
    // the compass star
    var sx0 = ix + iw * 0.07, sy0 = iy + ih * 0.84;
    out += K.star(sx0, sy0, 17 * (w / 420), ink) + K.star(sx0, sy0, 14 * (w / 420), C.orange) + fill(circ(sx0, sy0, 2.6), C.cream);
    (o.markers || []).forEach(function (mk, k) {
      var d = Array.isArray(mk) ? { x: mk[0], y: mk[1], kind: mk[2], label: mk[3] } : mk, p = [ix + d.x * iw, iy + d.y * ih];
      out += part("map-marker", p[0], p[1], marker(d.kind || "pin", p[0], p[1], d.label), 'data-i="' + k + '" data-kind="' + (d.kind || "pin") + '"');
    });
    if (o.title) {
      var tw = Math.max(110, String(o.title).length * 13 + 40);
      out += solid([poly([[-tw / 2 - 12, y0 - 2], [-tw / 2, y0 - 14], [tw / 2, y0 - 14], [tw / 2 + 12, y0 - 2], [tw / 2, y0 + 12], [-tw / 2, y0 + 12]])], C.war, 3.4) +
        text(0, y0 + 5.5, 18, o.title, C.cream, 'letter-spacing="3"');
    }
    return wrap("worldMap", out);
  };

  // ── Earth globe ──────────────────────────────────────────────────────
  // The engraved Earth of Part 1 (nuclear-winters, eligible): a cream circle with the same halftone continents,
  // plus engraved meridians and a dotted shadow, sitting on y 0 with no stand. Radius r (default 110, as in
  // Part 1), so 2r x 2r. An optional face, drawn like the humans' (almond eyes with heavy lids, angled brows).
  // o: { r (default 110), face "smile" | "sad" | "worried" | "none" (default) }
  // Parts: .globe (everything; pivot the center (0,-r): spin, wobble, squash), .globe-land (the continents, clipped
  // to the circle; pivot the center), .globe-face > .eye (each with a .pupil; pivot the eye's center), .brows,
  // .globe-mouth (holding the .mouth; pivot its center), .globe-tear (sad) / .globe-sweat (worried) (pivot the drop's top).
  var EARTH_LAND = "M-75,-45 C-60,-80 -10,-85 5,-60 C20,-40 -5,-20 10,0 C25,20 -10,35 -30,25 C-50,15 -85,0 -75,-45 Z " +
    "M25,15 C50,0 80,10 85,35 C88,60 60,80 40,70 C20,60 10,30 25,15 Z M40,-70 C55,-78 75,-60 65,-45 C55,-35 35,-50 40,-70 Z";
  function globeFace(mood, k, cy) {
    var p = function (x, y) { return P(x * k, cy + y * k); }, out = "";
    // every feature sits on a cream halo, so it reads over the dotted land (the cut-out edge of the corner Wishonia)
    var halo = function (d, w) { return '<path d="' + d + '" fill="none" stroke="' + C.cream + '" stroke-width="' + n1(w * k) + '" stroke-linecap="round" stroke-linejoin="round"/>'; };
    var stroke = function (d, w, cls) { return '<path' + (cls ? ' class="' + cls + '"' : "") + ' d="' + d + '" fill="none" stroke="' + ink + '" stroke-width="' + n1(w * k) + '" stroke-linecap="round" stroke-linejoin="miter"/>'; };
    var eyes = [-34, 34].map(function (ex) {
      var y = -14, rx = 19, ry = 12, tilt = mood === "sad" ? (ex < 0 ? 4 : -4) : 0;
      var top = mood === "smile" ? y - ry * 1.5 : mood === "worried" ? y - ry * 1.9 : y - ry * 1.2;
      var bot = mood === "smile" ? y + ry * 0.35 : y + ry * 1.1;
      var eyeD = "M" + p(ex - rx, y + tilt) + " Q" + p(ex, top) + " " + p(ex + rx, y - tilt) + " Q" + p(ex, bot) + " " + p(ex - rx, y + tilt) + " Z";
      var lidD = "M" + p(ex - rx - 2, y + tilt + 0.5) + " Q" + p(ex, top - 2) + " " + p(ex + rx + 2, y - tilt - 0.5);
      var pr = mood === "worried" ? 4.2 : 6, py = mood === "sad" ? y + 2.5 : mood === "smile" ? y - 1.5 : y;
      return part("eye", ex * k, cy + y * k, halo(eyeD, 10) + halo(lidD, 11) +
        '<path d="' + eyeD + '" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="' + n1(2.6 * k) + '" stroke-linejoin="miter"/>' +
        '<circle class="pupil" cx="' + n1((ex + 2) * k) + '" cy="' + n1(cy + py * k) + '" r="' + n1(pr * k) + '" fill="' + ink + '"/>' + stroke(lidD, 5));
    }).join("");
    var BR = { smile: [[-58, -36], [-37, -45], [-16, -39]], sad: [[-58, -33], [-37, -37], [-15, -49]], worried: [[-58, -44], [-37, -53], [-14, -57]] }[mood];
    var browD = ["M" + BR.map(function (q) { return p(q[0], q[1]); }).join(" L"), "M" + BR.map(function (q) { return p(-q[0], q[1]); }).join(" L")].join(" ");
    out += eyes + halo(browD, 12) + stroke(browD, 5.4, "brows");
    var mouth;
    if (mood === "smile") {
      var grin = "M" + p(-34, 20) + " Q" + p(0, 30) + " " + p(34, 20) + " Q" + p(0, 66) + " " + p(-34, 20) + " Z", cheeks = "M" + p(-40, 13) + " Q" + p(-43, 20) + " " + p(-37, 26) + " M" + p(40, 13) + " Q" + p(43, 20) + " " + p(37, 26);
      mouth = halo(grin, 10) + halo(cheeks, 9) + '<path class="mouth" d="' + grin + '" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="' + n1(3.4 * k) + '" stroke-linejoin="miter"/>' +
        line("M" + p(-30, 26) + " Q" + p(0, 37) + " " + p(30, 26), ink, n1(1.8 * k)) + stroke(cheeks, 3);
    } else {
      var d = mood === "sad" ? "M" + p(-28, 46) + " Q" + p(0, 20) + " " + p(28, 46)
        : "M" + p(-30, 36) + " L" + p(-18, 29) + " L" + p(-6, 36) + " L" + p(6, 29) + " L" + p(18, 36) + " L" + p(30, 29);
      mouth = halo(d, 12) + stroke(d, mood === "sad" ? 5.4 : 4.6, "mouth");
    }
    out += part("globe-mouth", 0, cy + 32 * k, mouth);
    var drop = function (cls, x, y, s) {
      var dd = "M" + p(x, y) + " Q" + p(x - 7 * s, y + 12 * s) + " " + p(x, y + 16 * s) + " Q" + p(x + 7 * s, y + 12 * s) + " " + p(x, y) + " Z";
      return part(cls, x * k, cy + y * k, halo(dd, 6) + '<path d="' + dd + '" fill="' + C.cyan + '" stroke="' + ink + '" stroke-width="' + n1(2.2 * k) + '" stroke-linejoin="miter"/>' +
        line("M" + p(x - 2 * s, y + 9 * s) + " L" + p(x - 2.5 * s, y + 12 * s), C.cream, n1(1.8 * k)));
    };
    if (mood === "sad") out += drop("globe-tear", -46, 0, 1.3);
    if (mood === "worried") out += drop("globe-sweat", 70, -66, 1.4);
    return '<g class="globe-face">' + out + "</g>";
  }
  K.props.earthGlobe = function (o) {
    o = o || {};
    var r = o.r || 110, k = r / 110, cy = -r, id = "kpl" + ++uid, mood = o.face && o.face !== "none" ? o.face : null;
    var defs = '<defs><pattern id="' + id + 'h" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><circle cx="4" cy="4" r="1.9" fill="' + ink + '"/></pattern>' +
      '<pattern id="' + id + 's" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="2.5" cy="2.5" r="1.1" fill="' + ink + '"/></pattern>' +
      '<clipPath id="' + id + 'c"><circle cx="0" cy="' + n1(cy) + '" r="' + n1(r) + '"/></clipPath></defs>';
    var grid = "";
    [0.42, 0.8].forEach(function (f) { grid += '<ellipse cx="0" cy="' + n1(cy) + '" rx="' + n1(r * f) + '" ry="' + n1(r) + '"/>'; });
    [-0.5, 0, 0.5].forEach(function (f) { var y = cy + r * f, hw = Math.sqrt(1 - f * f) * r; grid += '<path d="M' + P(-hw, y) + " H" + n1(hw) + '"/>'; });
    // the shadow: a crescent of fine dots on the lower right
    var q = r * 1.08, ox = -r * 0.2, crescent = "M" + P(-r, cy) + " A" + r + "," + r + " 0 1 0 " + P(r, cy) + " A" + r + "," + r + " 0 1 0 " + P(-r, cy) + " Z M" + P(ox - q, cy + ox) +
      " A" + n1(q) + "," + n1(q) + " 0 1 1 " + P(ox + q, cy + ox) + " A" + n1(q) + "," + n1(q) + " 0 1 1 " + P(ox - q, cy + ox) + " Z";
    var shade = '<defs><clipPath id="' + id + 'k"><path d="' + crescent + '" clip-rule="evenodd"/></clipPath></defs>' +
      '<rect x="' + n1(-r) + '" y="' + n1(cy - r) + '" width="' + n1(2 * r) + '" height="' + n1(2 * r) + '" fill="url(#' + id + 's)" opacity="0.5" clip-path="url(#' + id + 'k)"/>';
    var body = defs + fill(circ(0, cy, r), C.cream) +
      '<g clip-path="url(#' + id + 'c)"><g fill="none" stroke="' + C.peri + '" stroke-width="' + n1(1.6 * k) + '" opacity="0.5">' + grid + "</g>" +
      part("globe-land", 0, cy, '<g transform="translate(0,' + n1(cy) + ") scale(" + k.toFixed(3) + ')"><path d="' + EARTH_LAND + '" fill="url(#' + id + 'h)" stroke="' + ink + '" stroke-width="3.5" stroke-linejoin="round"/></g>') +
      shade + "</g>" + fill(circ(0, cy, r), "none", 'stroke="' + ink + '" stroke-width="6"') + (mood ? globeFace(mood, k, cy) : "");
    return wrap("earthGlobe", part("globe", 0, cy, body));
  };

  // ── Review sheet samples (tools/props-sheet.mjs) ──────────────────────
  K.props.SHEET.push(
    ["factory", {}, "FACTORY"],
    ["factory", { label: "SAFETY SYSTEM", sign: "lit", smoke: false }, "FACTORY (label, sign lit, no smoke)"],
    ["hospital", {}, "HOSPITAL (open)"],
    ["hospital", { sign: "closed" }, "HOSPITAL (closed)"],
    ["lab", {}, "LAB"],
    ["lab", { liquid: "war", fire: false }, "LAB (war liquid, no fire)"],
    ["house", {}, "HOUSE"],
    ["house", { variant: 1, lit: true }, "HOUSE (variant 1, lit)"],
    ["house", { variant: 2 }, "HOUSE (variant 2)"],
    ["house", { variant: 3, smoke: false }, "HOUSE (variant 3)"],
    ["printingPress", {}, "PRINTING PRESS"],
    ["printingPress", { seal: "war", label: "1913", tray: 0 }, "PRESS (war, 1913, empty tray)"],
    ["headstone", {}, "HEADSTONE"],
    ["headstone", { text: "HERE LIES\nBOB", flowers: true }, "HEADSTONE (two lines, flowers)"],
    ["capitol", {}, "CAPITOL"],
    ["capitol", { label: "LEGISLATURE" }, "CAPITOL (label)"],
    ["bank", {}, "BANK"],
    ["bank", { open: true }, "BANK (open)"],
    ["worldMap", {}, "WORLD MAP"],
    ["worldMap", { title: "THE WORLD", markers: [[0.25, 0.28, "pin", "HERE"], [0.55, 0.3, "war"], [0.6, 0.6, "med"], [0.82, 0.3, "nuke"], [0.3, 0.75, "skull"], [0.88, 0.72, "boom"], [0.45, 0.12, "star"]] }, "WORLD MAP (title, markers)"],
    ["earthGlobe", {}, "EARTH GLOBE"],
    ["earthGlobe", { face: "smile" }, "EARTH GLOBE (smile)"],
    ["earthGlobe", { face: "sad" }, "EARTH GLOBE (sad)"],
    ["earthGlobe", { face: "worried" }, "EARTH GLOBE (worried)"]
  );
})();
