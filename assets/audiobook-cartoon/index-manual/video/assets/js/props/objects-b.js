// Shared props, part B: objects and machines. Padlock, gauge, shopping cart, laptop, TV set, rotary phone,
// balance scale, door, conveyor, gears, ballot box, color-flip funnel and the YES button.
//
// Drawn like the HUMANS in kit.js: flat 1950s print in KIT.C colors, sharp polygons with mitred corners,
// a navy pass under each fill (touching shapes of one color share one outline), halftone dots on light
// surfaces and orange edges on dark ones.
//
// Every prop is drawn around x 0 and stands on y 0 (it extends upward), in KIT.person units: a person is
// about 180 tall with its feet at y 100, so a prop on the same ground as a person is translated by +100.
// Moving parts are untransformed <g class="..."> groups; each prop's comment lists them with their pivots
// (svgOrigin, in the prop's own units). Position a prop with an outer group and tween the parts inside.
// Pattern and clip ids are unique per call. No Math.random, no Date.
(function () {
  var K = window.KIT;
  K.props = K.props || { SHEET: [] };
  K.props.SHEET = K.props.SHEET || [];
  if (K.props.__objects_b) return;
  K.props.__objects_b = true;

  var C = K.C, ink = C.line, LW = 4.4, uid = 0, PI = Math.PI;

  // ── Drawing helpers (the HUMANS technique from kit.js) ─────────────────
  function f(v) { return String(Math.round(v * 10) / 10); }
  function P(x, y) { return f(x) + "," + f(y); }
  function polyD(pts) { return "M" + pts.map(function (p) { return P(p[0], p[1]); }).join(" L") + " Z"; }
  function poly(pts) { return 'path d="' + polyD(pts) + '"'; }
  function pathT(d) { return 'path d="' + d + '"'; }
  function circ(cx, cy, r) { return 'circle cx="' + f(cx) + '" cy="' + f(cy) + '" r="' + f(r) + '"'; }
  function flipX(pts) { return pts.map(function (p) { return [-p[0], p[1]]; }); }
  function shift(pts, dx, dy) { return pts.map(function (p) { return [p[0] + dx, p[1] + dy]; }); }
  function rect(x0, y0, x1, y1) { return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]; }
  // A rectangle with its corners cut off (c), top-left (x0, y0) to bottom-right (x1, y1).
  function chamf(x0, y0, x1, y1, c) { return [[x0 + c, y0], [x1 - c, y0], [x1, y0 + c], [x1, y1 - c], [x1 - c, y1], [x0 + c, y1], [x0, y1 - c], [x0, y0 + c]]; }
  function rot(p, deg, cx, cy) {
    var a = (deg * PI) / 180, x = p[0] - cx, y = p[1] - cy;
    return [cx + x * Math.cos(a) - y * Math.sin(a), cy + x * Math.sin(a) + y * Math.cos(a)];
  }
  function rotAll(pts, deg, cx, cy) { return pts.map(function (p) { return rot(p, deg, cx, cy); }); }
  function bbox(pts) {
    var b = [1e9, 1e9, -1e9, -1e9];
    pts.forEach(function (p) { b[0] = Math.min(b[0], p[0]); b[1] = Math.min(b[1], p[1]); b[2] = Math.max(b[2], p[0]); b[3] = Math.max(b[3], p[1]); });
    return b;
  }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  // Shapes drawn twice, a navy pass under the fill, so touching shapes of one color share one outline.
  // ml: the miter limit (8, as the people; lower it where an acute box corner would grow a spike).
  function solid(tags, col, w, ml) {
    w = w || LW;
    return tags.map(function (t) { return "<" + t + ' fill="' + ink + '" stroke="' + ink + '" stroke-width="' + w + '" stroke-linejoin="miter" stroke-miterlimit="' + (ml || 8) + '"/>'; }).join("") +
      tags.map(function (t) { return "<" + t + ' fill="' + col + '"/>'; }).join("");
  }
  function fill(tag, col, extra) { return "<" + tag + ' fill="' + col + '"' + (extra || "") + "/>"; }
  function line(d, col, w) { return '<path d="' + d + '" fill="none" stroke="' + (col || ink) + '" stroke-width="' + (w || 2) + '" stroke-linejoin="miter" stroke-linecap="round"/>'; }
  function path(pts) { return "M" + pts.map(function (p) { return P(p[0], p[1]); }).join(" L"); }
  // Print shading: an orange edge on a dark shape.
  function edge(d, w) { return line(d, C.orange, w || 1.6); }
  function nid(stem) { return "kob-" + stem + ++uid; }
  // Small props are drawn at a larger design size inside sc(k, ...) groups (k = their scale), so their
  // lines thin out like the props in a person's hand; DK keeps the halftone dots at the people's size.
  var DK = 1;
  function sc(k, inner) { return '<g transform="scale(' + k + ')">' + inner + "</g>"; }
  // Print shading: halftone dots over the part of a light shape right of x0 (clipTag: the shape's tag).
  function dots(clipTag, x0, y0, x1, y1, op) {
    var id = nid("hd"), st = 3.6 / DK;
    return '<defs><pattern id="' + id + 'd" width="' + f(st) + '" height="' + f(st) + '" patternUnits="userSpaceOnUse"><circle cx="' + f(st / 2) + '" cy="' + f(st / 2) + '" r="' + f(1 / DK) + '" fill="' + ink + '"/></pattern>' +
      '<clipPath id="' + id + 'c"><' + clipTag + "/></clipPath></defs>" +
      '<rect x="' + f(x0) + '" y="' + f(y0) + '" width="' + f(Math.max(0, x1 - x0)) + '" height="' + f(Math.max(0, y1 - y0)) + '" fill="url(#' + id + 'd)" opacity="' + (op || 0.28) + '" clip-path="url(#' + id + 'c)"/>';
  }
  function dotsOn(pts, x0, op) { var b = bbox(pts); return dots(poly(pts), x0, b[1], b[2], b[3], op); }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function text(x, y, s, size, col) {
    return '<text x="' + f(x) + '" y="' + f(y) + '" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="' + f(size) + '" fill="' + col + '">' + esc(s) + "</text>";
  }
  // Lines of text ("\n" breaks a line) centred on (x, y), shrunk to fit maxW.
  function block(x, y, s, maxW, maxSize, col) {
    var L = String(s).split("\n"), longest = L.reduce(function (m, t) { return Math.max(m, t.length); }, 1);
    var size = Math.min(maxSize, maxW / (longest * 0.5)), lh = size * 1.08, y0 = y - ((L.length - 1) * lh) / 2 + size * 0.36;
    return L.map(function (t, i) { return text(x, y0 + i * lh, t, size, col); }).join("");
  }
  function el(r) { return typeof r === "string" ? document.querySelector(r) : r; }
  // A KIT.money bill at (x, y): the outer group places it, the inner .<cls> group is free to tween (straight
  // x/y in prop units), the innermost one tilts and scales it.
  function bill(kind, x, y, deg, s, cls) {
    return '<g transform="translate(' + P(x, y) + ')"><g class="' + cls + '"><g transform="rotate(' + f(deg) + ") scale(" + s + ')">' + K.money(kind) + "</g></g></g>";
  }
  // A flat bill without legs, for loads (s = 1 is KIT.money size, 96 x 50).
  function flatBill(x, y, deg, s) {
    return '<g transform="translate(' + P(x, y) + ") rotate(" + f(deg) + ") scale(" + s + ')">' +
      '<rect x="-48" y="-25" width="96" height="50" fill="' + C.money + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<rect x="-40" y="-17" width="80" height="34" fill="none" stroke="' + C.moneyDark + '" stroke-width="3"/>' +
      '<ellipse cx="0" cy="0" rx="12" ry="14" fill="' + C.paper + '" stroke="' + C.moneyDark + '" stroke-width="3"/></g>';
  }

  // A money seal drawn big (radius r) at (x, y): a dark green disc with a little cream missile flying up and
  // right ("war") or a cream cross ("med"): KIT.moneySeal's two seals, readable at sign size.
  function bigSeal(kind, x, y, r) {
    var k = r / 14, mark;
    if (kind === "war") {
      var m = function (pts) { return poly(rotAll(pts, -40, 0, 0).map(function (p) { return [x + p[0] * k, y + p[1] * k]; })); };
      mark = fill(m([[-8, -2.4], [3, -2.4], [9, 0], [3, 2.4], [-8, 2.4]]), C.cream) + fill(m([[-8, -2.4], [-11.5, -6.5], [-5, -2.4]]), C.cream) + fill(m([[-8, 2.4], [-11.5, 6.5], [-5, 2.4]]), C.cream);
    } else mark = fill(poly([[-2.6, -8], [2.6, -8], [2.6, -2.6], [8, -2.6], [8, 2.6], [2.6, 2.6], [2.6, 8], [-2.6, 8], [-2.6, 2.6], [-8, 2.6], [-8, -2.6], [-2.6, -2.6]].map(function (p) { return [x + p[0] * k, y + p[1] * k]; })), C.cream);
    return solid([circ(x, y, r)], C.moneyDark, 3) + mark;
  }

  // ── PADLOCK ───────────────────────────────────────────────────────────
  // A big cartoon padlock, about a head tall: a brass body 31 x 23 on y 0 under a steel shackle, 40 tall shut,
  // 49 open. o.open: the shackle raised 9, its short right leg out of the body. o.color: the body (C.yellow).
  // o.label: a word on the body ("FDA").
  // Parts: .padlock-shackle (snap an open lock shut: y 0 -> 9; pop a shut one open: y 0 -> -9),
  //        .padlock-body (shake it around svgOrigin "0 -11.5", its center).
  K.props.padlock = function (o) {
    o = o || {};
    var k = 0.5, Y = -46, up = o.open ? -18 : 0, col = o.color || C.yellow;
    DK = k;
    var sh = shift([[-20, Y + 26], [-20, Y - 20], [-12, Y - 34], [12, Y - 34], [20, Y - 20], [20, Y + 6], [12, Y + 6], [12, Y - 17], [7, Y - 25], [-7, Y - 25], [-12, Y - 17], [-12, Y + 26]], 0, up);
    var shackle = '<g class="padlock-shackle">' + sc(k, solid([poly(sh)], C.peri) + line(path([[-16, Y + up], [-16, Y - 18.5 + up], [-9.8, Y - 28.8 + up]]), C.cream, 1.8)) + "</g>";
    var body = [[-27, 0], [27, 0], [31, -4], [31, Y + 4], [27, Y], [-27, Y], [-31, Y + 4], [-31, -4]];
    var kh = o.label ? -33 : -25;
    var key = fill(circ(0, kh - 2, 5), ink) + fill(poly([[-2.4, kh], [2.4, kh], [4.2, kh + 12], [-4.2, kh + 12]]), ink);
    var plates = line("M-31," + (Y + 7) + " H31", ink, 1.4) + (o.label ? "" : line("M-31,-7 H31", ink, 1.4));
    var out = '<g class="padlock">' + shackle + '<g class="padlock-body">' + sc(k, solid([poly(body)], col) + dotsOn(body, 6, 0.3) + plates + key +
      (o.label ? block(0, -9, o.label, 46, 11, ink) : "")) + "</g></g>";
    DK = 1;
    return out;
  };

  // ── GAUGE ─────────────────────────────────────────────────────────────
  // A dial meter. Default mount "box": a rust cabinet 160 wide, 166 tall, the dial (radius 60) at (0, -100)
  // over a cream plate with o.label. o.mount "dial": the bare dial, 120 across, standing on y 0, center
  // (0, -62), o.label small inside the face.
  // o.value 0..1 (0.3): where the needle points; the scale sweeps 240 degrees, 0 at lower left, 1 at lower right.
  // o.zones: [[from, to, color]] colored bands (default [[0.8, 1, C.war]], [] for none).
  // o.marks: [[value, "text", color?]] long ticks with a small label. o.window: text in a counter window
  // under the pivot ("2033").
  // Part: .gauge-needle, pivoting at its center (0, -100) for the box, (0, -62) for the dial
  // (KIT.props.gauge.pivot(o)). Move the needle drawn at o.value to v: rotation (v - o.value) * 240
  // (KIT.props.gauge.turn(o.value, v)), svgOrigin "0 -100" or "0 -62".
  var G_SWEEP = 240;
  function gaugeCy(o) { return o && o.mount === "dial" ? -62 : -100; }
  K.props.gauge = function (o) {
    o = o || {};
    var dial = o.mount === "dial", cy = gaugeCy(o), R = 52, v0 = clamp(o.value === undefined ? 0.3 : +o.value, 0, 1), out = "";
    var ang = function (v) { return -G_SWEEP / 2 + G_SWEEP * v; };
    var at = function (v, r) { var a = (ang(v) * PI) / 180; return [r * Math.sin(a), cy - r * Math.cos(a)]; };
    var band = function (a, b, r0, r1) {
      var pts = [], n = Math.max(2, Math.ceil(Math.abs(b - a) * 24)), i;
      for (i = 0; i <= n; i++) pts.push(at(a + ((b - a) * i) / n, r1));
      for (i = n; i >= 0; i--) pts.push(at(a + ((b - a) * i) / n, r0));
      return pts;
    };
    if (!dial) {
      var box = [[-76, 0], [76, 0], [76, -148], [64, -166], [-64, -166], [-76, -148]];
      out += solid([poly(box)], C.rust) + edge(path([[73.4, -4], [73.4, -147], [62.6, -163.4], [-62, -163.4]]), 2) +
        solid([poly([[-80, 0], [80, 0], [78, -7], [-78, -7]])], C.slate, 3.4) +
        solid([poly(chamf(-58, -35, 58, -13, 3))], C.cream, 3) +
        (o.label ? block(0, -24, o.label, 106, 15, ink) : [-46, 46].map(function (x) { return fill(circ(x, -24, 2.2), ink); }).join(""));
    }
    out += solid([circ(0, cy, 60)], C.yellow) + dots(circ(0, cy, 60), 22, cy - 60, 60, cy + 60, 0.3) + solid([circ(0, cy, R)], C.cream, 3);
    (o.zones || [[0.8, 1, C.war]]).forEach(function (z) { out += fill(poly(band(z[0], z[1], 40, 49)), z[2] || C.war); });
    for (var i = 0; i <= 20; i++) {
      var a = at(i / 20, 49), b = at(i / 20, i % 2 ? 44 : 39);
      out += line("M" + P(a[0], a[1]) + " L" + P(b[0], b[1]), ink, i % 2 ? 1.3 : 2.4);
    }
    (o.marks || []).forEach(function (m) {
      var a = at(m[0], 50), b = at(m[0], 31), t = at(m[0], 22), col = m[2] || C.war;
      out += line("M" + P(a[0], a[1]) + " L" + P(b[0], b[1]), col, 3.2) + (m[1] ? block(t[0], t[1], m[1], 30, 9, col) : "");
    });
    if (o.window) out += solid([poly(chamf(-21, cy + 18, 21, cy + 34, 2))], C.slate, 2.6) + block(0, cy + 26, o.window, 36, 12, C.cream);
    if (dial && o.label) out += block(0, cy + (o.window ? 42 : 31), o.label, 56, 10, ink);
    var nd = rotAll([[0, -(R - 7)], [3.6, 1], [2.4, 13], [-2.4, 13], [-3.6, 1]], ang(v0), 0, 0).map(function (p) { return [p[0], p[1] + cy]; });
    out += '<g class="gauge-needle" data-cx="0" data-cy="' + cy + '">' + solid([poly(nd)], C.war, 3) + solid([circ(0, cy, 6)], C.yellow, 3) + fill(circ(0, cy, 2), ink) + "</g>";
    return '<g class="gauge">' + out + "</g>";
  };
  K.props.gauge.SWEEP = G_SWEEP;
  K.props.gauge.pivot = function (o) { return [0, gaugeCy(o)]; };
  K.props.gauge.turn = function (fromV, toV) { return (toV - fromV) * G_SWEEP; };

  // ── SHOPPING CART ─────────────────────────────────────────────────────
  // A 1950s wire cart facing right, 118 wide (x -60..56), 97 tall, its grip at (-53, -91), about a
  // standing person's hand height. The basket (to fill from a scene) spans x -40..54, y -74..-38.
  // o.load: "money" (a heap of green bills) or "goods" (a box, a can, a bottle). Mirror it with an outer
  // scale(-1, 1) to face left.
  // Parts: .cart-wheel x2, rolling around their centers (-28, -7.5) and (37, -7.5) (data-cx, data-cy).
  K.props.shoppingCart = function (o) {
    o = o || {};
    var bk = [[-40, -74], [54, -74], [44, -38], [-30, -38]], cid = nid("cart"), load = "", grid = "";
    var tube = function (d) { return line(d, ink, 5.2) + line(d, C.cream, 2.4); };
    if (o.load === "money") load = [[-24, -76, -16], [-4, -83, 10], [17, -79, -8], [38, -76, 14], [8, -71, 3], [-14, -70, 6]].map(function (b) { return flatBill(b[0], b[1], b[2], 0.36); }).join("");
    if (o.load === "goods") {
      load = solid([poly(rect(-32, -100, -8, -58))], C.orange, 3) + K.star(-20, -80, 7, C.cream) +
        solid([poly(rect(-4, -88, 13, -58))], C.peri, 3) + fill(poly(rect(-4, -80, 13, -68)), C.cream) +
        solid([poly([[21, -108], [27, -108], [27, -95], [31, -89], [31, -58], [17, -58], [17, -89], [21, -95]])], C.med, 3) +
        solid([poly(rect(34, -86, 50, -58))], C.yellow, 3);
    }
    for (var x = -32; x <= 52; x += 9) grid += line("M" + x + ",-74 V-38", ink, 1.3);
    grid = '<defs><clipPath id="' + cid + '"><' + poly(bk) + "/></clipPath></defs>" + '<g clip-path="url(#' + cid + ')">' + grid + line("M-40,-62 H54 M-40,-50 H54", ink, 1.3) + "</g>";
    var wheel = function (cx) {
      return '<g class="cart-wheel" data-cx="' + cx + '" data-cy="-7.5">' + solid([circ(cx, -7.5, 7.5)], C.slate, 3) +
        line("M" + (cx - 5) + ",-7.5 H" + (cx + 5), C.orange, 1.6) + fill(circ(cx, -7.5, 2.2), C.cream) + "</g>";
    };
    return '<g class="shopping-cart">' + fill(poly(bk), C.cream, ' opacity="0.55"') + load + grid +
      tube(polyD(bk)) + tube("M-40,-74 L-51,-89") + tube("M-30,-38 L-28,-15 M44,-38 L37,-15 M-38,-15 H48 M-28,-15 V-8 M37,-15 V-8") +
      solid([poly([[-47.2, -89.4], [-53.2, -97.4], [-58.8, -93.2], [-52.8, -85.2]])], C.orange, 3) +
      wheel(-28) + wheel(37) + "</g>";
  };

  // ── LAPTOP ────────────────────────────────────────────────────────────
  // A chunky open laptop on a desk at y 0, about a person's chest wide: 67 wide, 46 tall. o.screen: text on
  // the screen ("\n" breaks lines). o.color: the case (C.peri). o.screenColor (C.slate).
  // Parts: .laptop-lid (open it with scaleY 0 -> 1, svgOrigin "0 -7.2", the hinge), .laptop-screen (the
  // screen box x -23.4..23.4, y -41.4..-11.4). Content can go in place of the <!--laptop-screen--> marker, in
  // these units (clipped to the screen, under the glare).
  K.props.laptop = function (o) {
    o = o || {};
    var k = 0.6, col = o.color || C.peri, cid = nid("lap");
    var lid = [[-46, -12], [46, -12], [46, -70], [40, -76], [-40, -76], [-46, -70]];
    var scr = [[-39, -19], [39, -19], [39, -64], [34, -69], [-34, -69], [-39, -64]];
    var base = [[-56, 0], [56, 0], [56, -4], [47, -13], [-47, -13], [-56, -4]];
    var scrP = scr.map(function (p) { return [p[0] * k, p[1] * k]; });
    var screen = '<g class="laptop-screen">' + sc(k, solid([poly(scr)], o.screenColor || C.slate, 3) + (o.screen ? block(0, -44, o.screen, 68, 15, C.cream) : "")) +
      '<defs><clipPath id="' + cid + '"><' + poly(scrP) + '/></clipPath></defs><g clip-path="url(#' + cid + ')"><!--laptop-screen--></g>' +
      sc(k, fill(poly([[-39, -42], [-15, -69], [-3, -69], [-39, -27]]), C.cream, ' opacity="0.14"')) + "</g>";
    var keys = '<path d="M-44,-9.5 H44 M-50,-6 H50" fill="none" stroke="' + C.slate + '" stroke-width="2.4" stroke-dasharray="5 2.2"/>';
    return '<g class="laptop"><g class="laptop-lid">' + sc(k, solid([poly(lid)], col) + edge(path([[43.6, -14], [43.6, -69], [39, -73.6]]))) + screen + "</g>" +
      sc(k, solid([poly(base)], col) + keys + edge("M-54,-1.8 H54", 1.4)) + "</g>";
  };

  // ── TV SET ────────────────────────────────────────────────────────────
  // A 1950s console TV on splayed legs with rabbit ears: cabinet 164 wide, 150 tall, the antenna tips at
  // about y -220. o.screen: text on the screen. o.color: the cabinet (C.rust). o.screenColor (C.slate).
  // Parts: .tv-screen (the screen box x -63..17, y -134..-51, center (-23, -92.5); put content in place of
  // the <!--tv-screen--> marker, clipped to the screen, under the glare),
  // .tv-antenna-l and .tv-antenna-r (wiggle them around svgOrigin "0 -156", their base).
  K.props.tvSet = function (o) {
    o = o || {};
    var wood = o.color || C.rust, cid = nid("tv");
    var legL = [[-64, -36], [-52, -36], [-65, 0], [-71, 0]], legB = [[-40, -36], [-32, -36], [-37, -8], [-42, -8]], ferL = [[-71, 0], [-65, 0], [-62.5, -7], [-69.6, -7]];
    var cab = [[-82, -34], [82, -34], [82, -142], [74, -150], [-74, -150], [-82, -142]];
    var bez = chamf(-72, -142, 26, -42, 12), scr = chamf(-63, -134, 17, -51, 9), grille = chamf(34, -142, 72, -100, 4), slots = "";
    for (var x = 39; x <= 67; x += 5) slots += "M" + x + ",-137 V-105 ";
    var antenna = function (cls, tx, ty, sx) {
      return '<g class="' + cls + '">' + line("M" + P(sx, -156) + " L" + P(tx, ty), ink, 2.8) + solid([circ(tx, ty, 3.8)], C.yellow, 2.4) + "</g>";
    };
    var screen = '<g class="tv-screen">' + solid([poly(scr)], o.screenColor || C.slate, 3) +
      '<defs><clipPath id="' + cid + '"><' + poly(scr) + '/></clipPath></defs><g clip-path="url(#' + cid + ')">' +
      (o.screen ? block(-23, -92.5, o.screen, 66, 20, C.cream) : "") + "<!--tv-screen--></g>" +
      fill(poly([[-63, -100], [-29, -134], [-17, -134], [-63, -88]]), C.cream, ' opacity="0.13"') + "</g>";
    var knob = function (y) { return solid([circ(53, y, 8)], C.yellow, 3) + line("M53," + y + " L" + P(58, y - 4.5), ink, 2); };
    return '<g class="tv-set">' + solid([poly(legB), poly(flipX(legB))], C.slate, 3.4) + solid([poly(legL), poly(flipX(legL))], C.slate) +
      solid([poly(ferL), poly(flipX(ferL))], C.yellow, 2.6) +
      antenna("tv-antenna-l", -46, -214, -3) + antenna("tv-antenna-r", 42, -220, 3) +
      solid([poly(cab)], wood) + edge(path([[79.6, -37], [79.6, -141], [73, -147.6], [-73, -147.6]]), 2) +
      solid([poly([[-14, -149], [-10, -157], [0, -160], [10, -157], [14, -149]])], C.slate, 3) +
      solid([poly(bez)], C.cream) + dotsOn(bez, -10, 0.26) + screen +
      solid([poly(grille)], C.tan, 3) + line(slots, ink, 2) + knob(-82) + knob(-58) + "</g>";
  };

  // ── PHONE ─────────────────────────────────────────────────────────────
  // A rotary desk phone, 46 wide (61 with its cord), 30 tall: its handset is about a head long.
  // o.color: the phone (C.slate; C.war for the hotline gag). o.ring: jagged ring lines either side (.phone-ring).
  // Parts: .phone-handset (lift it: its center (0, -26.4); y -18 and a small rotation), .phone-dial (spin it
  // around svgOrigin "0 -10.8"), .phone-cord (stretch it with scaleY around "-20.4 -4.2"), .phone-ring (o.ring).
  K.props.phone = function (o) {
    o = o || {};
    var col = o.color || C.slate, cy = -18, ks = 0.6;
    var base = [[-38, 0], [38, 0], [34, -8], [24, -36], [-24, -36], [-34, -8]];
    var holes = "";
    for (var k = 0; k < 10; k++) {
      var a = ((-36 - 28 * k) * PI) / 180;
      holes += solid([circ(10.4 * Math.cos(a), cy + 10.4 * Math.sin(a), 2)], col, 1.5);
    }
    var fs = [15.6 * Math.cos(PI / 6), cy + 15.6 * Math.sin(PI / 6)], fe = [10 * Math.cos(PI / 6), cy + 10 * Math.sin(PI / 6)];
    // the coiled cord: a tight wave along a curve from the base to the handset's left cup
    var cord = [], c0 = [-34, -7], c1 = [-62, -8], c2 = [-42, -37];
    for (var i = 0; i <= 80; i++) {
      var t = i / 80, u = 1 - t, bx = u * u * c0[0] + 2 * u * t * c1[0] + t * t * c2[0], by = u * u * c0[1] + 2 * u * t * c1[1] + t * t * c2[1];
      var tx = 2 * u * (c1[0] - c0[0]) + 2 * t * (c2[0] - c1[0]), ty = 2 * u * (c1[1] - c0[1]) + 2 * t * (c2[1] - c1[1]), L = Math.sqrt(tx * tx + ty * ty) || 1, s = 2.6 * Math.sin(t * PI * 22) * Math.min(1, t * 8, (1 - t) * 8);
      cord.push([bx - (ty / L) * s, by + (tx / L) * s]);
    }
    var bar = [[-30, -45], [-20, -50], [20, -50], [30, -45], [30, -40], [20, -44.5], [-20, -44.5], [-30, -40]], cupL = [[-43, -50], [-27, -50], [-24, -37], [-46, -37]];
    return '<g class="phone">' + sc(ks, solid([poly(base)], col) + edge(path([[33, -9], [23.5, -34]]), 2) + line("M-34,-8 H34", ink, 1.4)) +
      '<g class="phone-dial" data-cx="0" data-cy="' + f(cy * ks) + '">' + sc(ks, solid([circ(0, cy, 15)], C.cream, 3) + holes + solid([circ(0, cy, 5)], C.cream, 2.2) + fill(circ(0, cy, 1.5), C.war)) + "</g>" +
      sc(ks, line("M" + P(fs[0], fs[1]) + " L" + P(fe[0], fe[1]), ink, 2.4) +
        solid([poly([[-24, -35], [-15, -35], [-16, -42], [-23, -42]]), poly([[15, -35], [24, -35], [23, -42], [16, -42]])], col, 3)) +
      '<g class="phone-cord">' + sc(ks, line(path(cord), ink, 2)) + "</g>" +
      '<g class="phone-handset">' + sc(ks, solid([poly(bar), poly(cupL), poly(flipX(cupL))], col) + edge("M-20,-48.4 H20", 1.8) + line("M-44,-39.6 H-25 M25,-39.6 H44", ink, 1.4)) + "</g>" +
      (o.ring ? '<g class="phone-ring">' + sc(ks, line("M-48,-56 L-56,-65 M-53,-48 L-65,-50 M48,-56 L56,-65 M53,-48 L65,-50 M50,-40 L60,-37", ink, 3)) + "</g>" : "") + "</g>";
  };

  // ── BALANCE SCALE ─────────────────────────────────────────────────────
  // Brass scales 240 wide (pans and all), 176 tall: the beam pivots at (0, -150) and is 168 long; each pan hangs 64 below
  // its beam end on two strings (the pans' rims are 86 above the ground at tilt 0).
  // o.tilt: degrees, positive = right pan down (drawn that way). o.left, o.right: words on the pans.
  // o.color (C.yellow).
  // Parts: .scale-beam (rotation around svgOrigin "0 -150"),
  // .scale-pan-l, .scale-pan-r (they hang straight: move them, do not rotate them). A pan's load sits on its
  // rim, 64 below its beam end: (-84 cos t, -150 - 84 sin t) left, (84 cos t, -150 + 84 sin t) right.
  // KIT.props.balanceScale.tilt(tl, root, at, dur, fromDeg, toDeg, drawnDeg, ease) tweens the beam and both
  // pans together (root: the element or selector holding this scale; drawnDeg: the o.tilt it was drawn with).
  var SC = { R: 84, py: -150, drop: 64 };
  function hookAt(side, deg) { var a = (deg * PI) / 180; return [side * SC.R * Math.cos(a), SC.py + side * SC.R * Math.sin(a)]; }
  K.props.balanceScale = function (o) {
    o = o || {};
    var col = o.color || C.yellow, t = +o.tilt || 0, py = SC.py, R = SC.R, d = SC.drop;
    var base = [[-48, 0], [48, 0], [42, -10], [-42, -10]], step = [[-26, -10], [26, -10], [20, -22], [-20, -22]];
    var stand = solid([poly(base), poly(step), poly([[-5, -22], [5, -22], [4, -140], [-4, -140]]), poly(rect(-9, -66, 9, -58)), poly(rect(-8, -124, 8, -117))], col) +
      dotsOn(base, 6) + dotsOn(step, 4) +
      solid([poly([[-11, -137], [11, -137], [0, py - 3]]), poly([[-2.2, py - 12], [2.2, py - 12], [2.2, py], [-2.2, py]]), poly([[0, py - 26], [6.5, py - 18], [0, py - 10], [-6.5, py - 18]])], col, 3.6);
    var pan = function (side, cls, lab) {
      var H = hookAt(side, t), hx = H[0], hy = H[1], dish = [[hx - 36, hy + d], [hx + 36, hy + d], [hx + 24, hy + d + 12], [hx - 24, hy + d + 12]];
      return '<g class="' + cls + '">' + line(path([[hx - 32, hy + d], [hx, hy], [hx + 32, hy + d]]), ink, 1.6) + solid([poly(dish)], col, 3.6) + dotsOn(dish, hx + 4, 0.3) +
        (lab ? block(hx, hy + d + 6.4, lab, 40, 9, ink) : "") + "</g>";
    };
    var mv = function (pts) { return rotAll(shift(pts, 0, py), t, 0, py); };
    var bm = [[-R - 3, -2], [-12, -4.5], [0, -6.5], [12, -4.5], [R + 3, -2], [R + 3, 2.5], [12, 4.5], [0, 6.5], [-12, 4.5], [-R - 3, 2.5]];
    var knob = function (x) { return [[x - 5.5, 0], [x, -5.5], [x + 5.5, 0], [x, 5.5]]; };
    var beam = '<g class="scale-beam" data-cx="0" data-cy="' + py + '">' +
      solid([poly(mv(bm)), poly(mv(knob(-R))), poly(mv(knob(R)))], col, 3.6) + dots(poly(mv(bm)), 4, py - 60, R + 10, py + 60, 0.3) +
      solid([circ(0, py, 4.4)], C.cream, 2.6) + "</g>";
    return '<g class="balance-scale">' + stand + pan(-1, "scale-pan-l", o.left) + pan(1, "scale-pan-r", o.right) + beam + "</g>";
  };
  K.props.balanceScale.hook = hookAt;
  K.props.balanceScale.tilt = function (tl, root, at, dur, fromDeg, toDeg, drawnDeg, ease) {
    root = el(root);
    var dr = drawnDeg || 0, e = ease || "power2.inOut", O = "0 " + SC.py;
    tl.fromTo(root.querySelector(".scale-beam"), { rotation: fromDeg - dr, svgOrigin: O }, { rotation: toDeg - dr, svgOrigin: O, duration: dur, ease: e }, at);
    [[-1, ".scale-pan-l"], [1, ".scale-pan-r"]].forEach(function (s) {
      var h0 = hookAt(s[0], dr), a = hookAt(s[0], fromDeg), b = hookAt(s[0], toDeg);
      tl.fromTo(root.querySelector(s[1]), { x: a[0] - h0[0], y: a[1] - h0[1] }, { x: b[0] - h0[0], y: b[1] - h0[1], duration: dur, ease: e }, at);
    });
  };

  // ── DOOR ──────────────────────────────────────────────────────────────
  // A paneled door in a frame, 128 wide, 214 tall (a person is 180): the doorway is x -48..48, y -202..0.
  // o.label: a sign on the door ("FDA"). o.color: the leaf (C.rust). o.slot: a mail slot. o.open 0..1 (or
  // true): drawn swung open toward the viewer.
  // Parts: .door-leaf (swing it open with scaleX 1 -> 0.16 around svgOrigin "-48 -102", the hinge side),
  // .door-slot (o.slot, inside the leaf, x -24..24, y -80..-66). Content behind the door goes in place of the
  // <!--door-inside--> marker (drawn over the dark doorway, under the leaf).
  K.props.door = function (o) {
    o = o || {};
    var op = o.open === true ? 1 : clamp(+o.open || 0, 0, 1), s = 1 - 0.84 * op, e = 0.1 * op, col = o.color || C.rust;
    // swung open toward the viewer: squeezed onto the hinge side, the free edge taller (its foot stays on the floor)
    var M = function (p) { var u = (p[0] + 48) / 96; return [-48 + (p[0] + 48) * s, p[1] * (1 + e * u)]; };
    var Mp = function (pts) { return pts.map(M); };
    var frame = rect(-60, -214, 60, 0), hole = rect(-48, -202, 48, 0), leaf = rect(-48, -202, 48, -1);
    var up = chamf(-36, -188, 36, -122, 6), lo = chamf(-36, -106, 36, -16, 6);
    var panel = function (pts) {
      return '<path d="' + polyD(Mp(pts)) + '" fill="none" stroke="' + ink + '" stroke-width="2.4" stroke-linejoin="miter"/>' +
        edge(path(Mp([[pts[2][0] - 3, pts[2][1]], [pts[3][0] - 3, pts[3][1]], [pts[4][0], pts[4][1] - 3], [pts[5][0], pts[5][1] - 3]])), 1.8);
    };
    var kc = M([35.5, -100]);
    var lg = solid([poly(Mp(leaf))], col) + edge(path(Mp([[45.6, -4], [45.6, -199.6]])), 2) + panel(up) + panel(lo) +
      solid([poly(Mp(rect(31, -112, 40, -88)))], C.yellow, 2.6) + solid(['ellipse cx="' + f(kc[0]) + '" cy="' + f(kc[1]) + '" rx="' + f(4.6 * Math.max(s, 0.3)) + '" ry="4.6"'], C.yellow, 2.6);
    if (o.label) {
      lg += solid([poly(Mp(chamf(-32, -180, 32, -150, 4)))], C.cream, 3) +
        '<g transform="matrix(' + f(s * 100) / 100 + ",0,0,1," + f(-48 + 48 * s) + ',0)">' + block(0, -165, o.label, 54, 18, ink) + "</g>";
    }
    if (o.slot) lg += '<g class="door-slot">' + solid([poly(Mp(chamf(-24, -80, 24, -66, 2)))], C.yellow, 2.6) + fill(poly(Mp(rect(-20, -75, 20, -71))), ink) + "</g>";
    return '<g class="door">' + solid([poly(frame)], C.tan) + dotsOn(frame, 30, 0.25) + solid([poly(hole)], C.deep, 3) + "<!--door-inside-->" +
      '<g class="door-leaf" data-cx="-48" data-cy="-102">' + lg + "</g>" +
      solid([poly(rect(-51, -186, -46, -172)), poly(rect(-51, -32, -46, -18))], C.slate, 2.4) +
      solid([poly(rect(-64, -5, 64, 0))], C.slate, 3) + "</g>";
  };

  // ── CONVEYOR ──────────────────────────────────────────────────────────
  // A belt on legs: o.w long (340), its top surface at y -o.h (-66, waist high), where loads sit. o.color: the frame
  // (C.peri).
  // Parts: .conveyor-belt (the belt's marks; slide it x 0 -> 22 (rightward) or 0 -> -22, ease "none",
  // repeated: the pattern repeats every 22), .conveyor-roller x2 (the end rollers, radius 7, rotating around
  // their centers (-w/2 + 7, -h + 7) and (w/2 - 7, -h + 7), in data-cx, data-cy).
  // KIT.props.conveyor.run(tl, root, at, dur, speed) runs both at speed units/s (negative = leftward).
  var CONV_P = 22, CONV_R = 7;
  K.props.conveyor = function (o) {
    o = o || {};
    var w = o.w || 340, h = o.h || 66, x0 = -w / 2, x1 = w / 2, top = -h, bt = 2 * CONV_R, rr = CONV_R, cid = nid("belt"), fr = o.color || C.peri;
    var beltD = "M" + P(x0 + rr, top) + " H" + f(x1 - rr) + " A" + rr + "," + rr + " 0 0 1 " + P(x1 - rr, top + bt) + " H" + f(x0 + rr) + " A" + rr + "," + rr + " 0 0 1 " + P(x0 + rr, top) + " Z";
    var marks = "";
    for (var x = x0 - 2 * CONV_P; x <= x1 + 2 * CONV_P; x += CONV_P) marks += "M" + P(x + 3, top + 2.5) + " L" + P(x - 3, top + bt - 2.5) + " ";
    var lx = w > 280 ? [x0 + 28, 0, x1 - 28] : [x0 + 28, x1 - 28];
    var legs = lx.map(function (lxi) { return poly([[lxi - 5, top + bt + 14], [lxi + 5, top + bt + 14], [lxi + 6, -5], [lxi - 6, -5]]); });
    var feet = lx.map(function (lxi) { return poly([[lxi - 11, 0], [lxi + 11, 0], [lxi + 8, -6], [lxi - 8, -6]]); });
    var rail = [[x0 + 10, top + bt - 2], [x1 - 10, top + bt - 2], [x1 - 14, top + bt + 15], [x0 + 14, top + bt + 15]], rivets = "";
    for (x = x0 + 24; x <= x1 - 20; x += 30) rivets += fill(circ(x, top + bt + 7, 1.6), ink);
    var roller = function (cx) {
      var cyR = top + rr;
      return '<g class="conveyor-roller" data-cx="' + f(cx) + '" data-cy="' + f(cyR) + '">' + solid([circ(cx, cyR, rr - 2)], C.cream, 2.2) +
        line("M" + P(cx - 3.4, cyR) + " H" + f(cx + 3.4) + " M" + P(cx, cyR - 3.4) + " V" + f(cyR + 3.4), ink, 1.4) + "</g>";
    };
    var brace = "M" + P(lx[0], -18) + " H" + f(lx[lx.length - 1]);
    return '<g class="conveyor">' + solid(legs, C.slate, 3.6) + line(brace, ink, 4.6) + line(brace, fr, 2) + solid(feet, ink, 2.4) +
      solid([poly(rail)], fr, 3.6) + rivets + line("M" + P(x0 + 13, top + bt + 2) + " H" + f(x1 - 13), C.cream, 1.4) +
      solid([pathT(beltD)], C.slate) +
      '<defs><clipPath id="' + cid + '"><path d="' + beltD + '"/></clipPath></defs><g clip-path="url(#' + cid + ')"><g class="conveyor-belt">' + line(marks, C.cream, 2) + "</g></g>" +
      edge("M" + P(x0 + rr, top + 1.4) + " H" + f(x1 - rr), 1.6) + roller(x0 + rr) + roller(x1 - rr) + "</g>";
  };
  K.props.conveyor.PERIOD = CONV_P;
  K.props.conveyor.run = function (tl, root, at, dur, speed) {
    root = el(root);
    var sp = speed || 60, n = Math.max(1, Math.round((dur * Math.abs(sp)) / CONV_P)), deg = ((sp * dur) / CONV_R) * (180 / PI);
    tl.fromTo(root.querySelector(".conveyor-belt"), { x: 0 }, { x: sp > 0 ? CONV_P : -CONV_P, duration: dur / n, ease: "none", repeat: n - 1 }, at);
    Array.prototype.forEach.call(root.querySelectorAll(".conveyor-roller"), function (g) {
      var O = g.getAttribute("data-cx") + " " + g.getAttribute("data-cy");
      tl.fromTo(g, { rotation: 0, svgOrigin: O }, { rotation: deg, svgOrigin: O, duration: dur, ease: "none" }, at);
    });
  };

  // ── GEARS ─────────────────────────────────────────────────────────────
  // o.n meshing gears (3, up to 8) in a zigzag chain, the lowest one touching y 0, centered on x 0 (3 gears
  // are about 200 wide and 110 tall; 5 about 330 wide). o.labels: text on each gear's hub ("1".."5").
  // o.dark: slate and steel gears with orange edges (a dark machine). o.colors: fills to cycle through.
  // o.teeth: tooth counts (default 12, 8, 14, 9, 12, ...; radius = 3 x teeth).
  // Parts: .gear, one per gear, with data-cx, data-cy (its center = its svgOrigin) and data-turn (how far it
  // turns per degree of gear 0, with its direction). The hubs and the shading stay still.
  // KIT.props.gears.spin(tl, root, at, dur, fromDeg, toDeg, ease) turns them all together.
  var GEAR = { m: 6, add: 5, teeth: [12, 8, 14, 9, 12, 10, 13, 8], dirs: [-22, 28, -18, 32, -26, 20, -30] };
  K.props.gears = function (o) {
    o = o || {};
    var n = clamp(o.n || 3, 1, 8), dark = !!o.dark, cols = o.colors || (dark ? [C.slate, C.peri] : [C.yellow, C.orange, C.peri, C.tan]), G = [], i, k;
    for (i = 0; i < n; i++) {
      var tn = (o.teeth && o.teeth[i]) || GEAR.teeth[i % GEAR.teeth.length], g = { t: tn, r: (GEAR.m * tn) / 2, cx: 0, cy: 0, ph: 0, turn: 1 };
      if (i) {
        var p = G[i - 1], a = GEAR.dirs[(i - 1) % GEAR.dirs.length], ar = (a * PI) / 180, dd = p.r + g.r;
        g.cx = p.cx + dd * Math.cos(ar);
        g.cy = p.cy + dd * Math.sin(ar);
        // mesh: a tooth of one gear faces a gap of the other along the line between their centers
        var pp = ((((a - p.ph) / (360 / p.t)) % 1) + 1) % 1;
        g.ph = a + 180 - (0.5 - pp) * (360 / tn);
        g.turn = (-p.turn * p.t) / tn;
      }
      G.push(g);
    }
    var minX = 1e9, maxX = -1e9, maxY = -1e9;
    G.forEach(function (g) { minX = Math.min(minX, g.cx - g.r - GEAR.add); maxX = Math.max(maxX, g.cx + g.r + GEAR.add); maxY = Math.max(maxY, g.cy + g.r + GEAR.add); });
    var dx = -(minX + maxX) / 2, dy = -maxY, gearsSvg = "", over = "";
    G.forEach(function (g, gi) {
      var cx = g.cx + dx, cy = g.cy + dy, pitch = 360 / g.t, ro = g.r + GEAR.add, ri = g.r - GEAR.add, pts = [], col = cols[gi % cols.length];
      var at = function (deg, r) { var x = (deg * PI) / 180; return [cx + r * Math.cos(x), cy + r * Math.sin(x)]; };
      for (k = 0; k < g.t; k++) {
        var c = g.ph + k * pitch;
        pts.push(at(c - 0.3 * pitch, ri), at(c - 0.16 * pitch, ro), at(c + 0.16 * pitch, ro), at(c + 0.3 * pitch, ri));
      }
      var nh = g.t >= 12 ? 5 : 4, holes = "";
      for (k = 0; k < nh; k++) {
        var hp = at(g.ph + (k * 360) / nh + pitch / 2, g.r * 0.5);
        holes += "<" + circ(hp[0], hp[1], g.r * 0.15) + ' fill="' + ink + '" fill-opacity="0.32" stroke="' + ink + '" stroke-width="1.4"/>';
      }
      gearsSvg += '<g class="gear" data-i="' + gi + '" data-cx="' + f(cx) + '" data-cy="' + f(cy) + '" data-turn="' + g.turn.toFixed(4) + '">' + solid([poly(pts)], col) + holes +
        '<circle cx="' + f(cx) + '" cy="' + f(cy) + '" r="' + f(g.r * 0.72) + '" fill="none" stroke="' + ink + '" stroke-width="1.4"/>' + "</g>";
      var lab = o.labels && o.labels[gi] !== undefined ? String(o.labels[gi]) : "";
      over += (dark ? edge("M" + P(cx + (ri - 3) * Math.cos(-PI / 3), cy + (ri - 3) * Math.sin(-PI / 3)) + " A" + f(ri - 3) + "," + f(ri - 3) + " 0 0 1 " + P(cx + (ri - 3) * Math.cos(PI / 3), cy + (ri - 3) * Math.sin(PI / 3)), 2)
        : dots(circ(cx, cy, ri - 1), cx + g.r * 0.15, cy - ri, cx + ri, cy + ri, 0.28)) +
        (lab ? solid([circ(cx, cy, 11)], C.cream, 3) + block(cx, cy, lab, 16, 14, ink) : solid([circ(cx, cy, 6.5)], dark ? C.peri : C.slate, 3) + fill(circ(cx, cy, 2), C.cream));
    });
    return '<g class="gears">' + gearsSvg + over + "</g>";
  };
  K.props.gears.spin = function (tl, root, at, dur, fromDeg, toDeg, ease) {
    root = el(root);
    Array.prototype.forEach.call(root.querySelectorAll(".gear"), function (g) {
      var k = +g.getAttribute("data-turn"), O = g.getAttribute("data-cx") + " " + g.getAttribute("data-cy");
      tl.fromTo(g, { rotation: fromDeg * k, svgOrigin: O }, { rotation: toDeg * k, svgOrigin: O, duration: dur, ease: ease || "none" }, at);
    });
  };

  // ── BALLOT BOX ────────────────────────────────────────────────────────
  // A wooden ballot box seen from above right, hip high: 70 wide, 62 tall, the slot on top at about (4, -57).
  // o.label: the front plate (default "VOTE"). o.color: the front (C.tan). o.ballot: a ballot standing in
  // the slot.
  // Part: .ballot-paper (o.ballot; clipped at the slot, so tweening it down drops it in: y 0 -> 32 is gone;
  // fromTo y -42 -> 0 brings one down to the slot).
  K.props.ballotBox = function (o) {
    o = o || {};
    var k = 0.7, col = o.color || C.tan, cid = nid("slot"), label = o.label === undefined ? "VOTE" : o.label;
    DK = k;
    var front = rect(-44, -74, 44, -6), topF = [[-44, -74], [44, -74], [56, -88], [-32, -88]], side = [[44, -74], [56, -88], [56, -20], [44, -6]];
    var ballot = o.ballot ? '<defs><clipPath id="' + cid + '"><rect x="-60" y="-300" width="140" height="' + f(300 - 81 * k) + '"/></clipPath></defs><g clip-path="url(#' + cid + ')"><g class="ballot-paper">' +
      sc(k, solid([poly([[-7, -120], [17, -121], [16, -79], [-8, -79]])], C.cream, 3) + line("M-3,-111 H12 M-3,-104 H12", ink, 1.4) + line("M-1,-96 L3,-91 L11,-101", C.med, 2.6)) + "</g></g>" : "";
    var out = '<g class="ballot-box">' + sc(k, solid([poly(side)], C.rust, LW, 2) + edge(path([[54, -84], [54, -21]]), 1.8) + solid([poly(topF)], C.cream, LW, 2) + dotsOn(topF, 10, 0.22) +
      fill(poly([[-12, -79], [20, -79], [24, -83], [-8, -83]]), ink)) + ballot +
      sc(k, solid([poly(front)], col) + dotsOn(front, 14, 0.24) +
        (label ? solid([poly(chamf(-34, -62, 34, -34, 4))], C.cream, 3) + block(0, -48, label, 48, 18, ink) + K.star(-27, -48, 5, C.orange) + K.star(27, -48, 5, C.orange) : "") +
        solid([poly(rect(-5, -74, 5, -65))], C.slate, 2.4) +
        solid([poly([[-42, 0], [-32, 0], [-32, -6], [-42, -6]]), poly([[32, 0], [42, 0], [42, -6], [32, -6]])], ink, 2)) + "</g>";
    DK = 1;
    return out;
  };

  // ── COLOR-FLIP FUNNEL ─────────────────────────────────────────────────
  // The seal-flip machine (bible, gag 2): war-seal bills drop into a striped funnel on top, a dark box with
  // a "missile seal -> cross seal" plate flips them, and medicine-seal bills walk out of a spout at the bottom.
  // 232 wide (x -116..116; the walking bill reaches x 125), the funnel mouth at y -262, its top bill at y -312.
  // o.label: text on the box (a lamp row without one). o.inN (3) war bills in the mouth, o.outN (2) med bills out.
  // Parts: .funnel-in (the war bills, clipped at the mouth's front lip; each is a .funnel-bill: tween its y
  // down 60 and it drops into the funnel; fromTo y -120 -> 0 drops a new one in from above), .funnel-out (the
  // med bills, each a .funnel-bill: the first stands under the spout at (0, -24),
  // the others walk off to the right), .funnel-lever (pull it: rotation 0 -> 50 around svgOrigin "80 -112").
  K.props.colorFlipFunnel = function (o) {
    o = o || {};
    var inN = o.inN === undefined ? 3 : o.inN, outN = o.outN === undefined ? 2 : o.outN, s = 0.55, cid = nid("mouth");
    var IN = [[-42, -262, -14], [34, -268, 17], [-4, -296, -5], [64, -290, 24], [-70, -284, -22]], OUT = [[0, -24, 0], [96, -24, 0], [150, -24, 0], [204, -24, 0]];
    var legL = [[-70, -66], [-56, -66], [-58, -6], [-68, -6]];
    var body = [[-74, -64], [74, -64], [74, -154], [64, -164], [-64, -164], [-74, -154]];
    var spout = [[-20, -65], [20, -65], [13, -47], [-13, -47]];
    var cone = [[-112, -258], [112, -258], [27, -178], [-27, -178]];
    var wAt = function (y) { return 27 + ((y + 178) / -80) * 85; };
    var stripe = function (ya, yb) { return [[-wAt(ya), ya], [wAt(ya), ya], [wAt(yb), yb], [-wAt(yb), yb]]; };
    var backRim = [[-116, -264], [-96, -278], [96, -278], [116, -264], [108, -262], [92, -270], [-92, -270], [-108, -262]];
    var mouth = [[-108, -262], [-92, -270], [92, -270], [108, -262], [92, -254], [-92, -254]];
    var lip = [[-116, -264], [-108, -262], [-92, -254], [92, -254], [108, -262], [116, -264], [114, -257], [96, -247], [-96, -247], [-114, -257]];
    var ins = "", outs = "", i;
    for (i = 0; i < Math.min(inN, IN.length); i++) ins += bill("war", IN[i][0], IN[i][1], IN[i][2], s, "funnel-bill");
    for (i = 0; i < Math.min(outN, OUT.length); i++) outs += bill("med", OUT[i][0], OUT[i][1], OUT[i][2], 0.5, "funnel-bill");
    var lamps = [[-40, C.war], [0, C.yellow], [40, C.med]].map(function (l) { return solid([circ(l[0], -86, 6)], l[1], 2.6); }).join("");
    var arrow = [[-13, -132], [3, -132], [3, -138], [15, -129], [3, -120], [3, -126], [-13, -126]];
    var rivets = [-62, -46, 46, 62].map(function (x) { return fill(circ(x, -73, 1.8), C.cream); }).join("");
    return '<g class="color-flip-funnel">' +
      solid([poly(legL), poly(flipX(legL))], C.slate) + solid([poly([[-74, 0], [-52, 0], [-55, -7], [-71, -7]]), poly([[52, 0], [74, 0], [71, -7], [55, -7]])], ink, 2.4) +
      '<g class="funnel-out">' + outs + "</g>" +
      solid([poly(spout)], C.peri) + fill(poly([[-13, -47], [13, -47], [11, -44], [-11, -44]]), ink) +
      solid([poly(body)], C.slate) + edge(path([[71.6, -67], [71.6, -153], [62.6, -161.6], [-62, -161.6]]), 2) +
      solid([poly(chamf(-58, -151, 58, -107, 5))], C.cream, 3) + dotsOn(chamf(-58, -151, 58, -107, 5), 22, 0.22) +
      bigSeal("war", -34, -129, 14) + fill(poly(arrow), ink) + bigSeal("med", 36, -129, 14) +
      (o.label ? block(0, -86, o.label, 120, 16, C.cream) : lamps) + rivets +
      solid([poly(rect(74, -124, 84, -100))], C.peri, 3) +
      '<g class="funnel-lever" data-cx="80" data-cy="-112">' + solid([poly([[77, -112], [83, -112], [113, -157], [109, -160]])], C.peri, 3.4) + solid([circ(111, -160, 7)], C.yellow, 3) + fill(circ(80, -112, 3.2), C.cream) + "</g>" +
      solid([poly(backRim)], C.orange, 3.4) + solid([poly(mouth)], C.deep, 2.6) +
      '<defs><clipPath id="' + cid + '"><' + poly([[-240, -700], [240, -700], [240, -264], [108, -262], [92, -254], [-92, -254], [-108, -262], [-240, -264]]) + "/></clipPath></defs>" +
      '<g clip-path="url(#' + cid + ')"><g class="funnel-in">' + ins + "</g></g>" +
      solid([poly(cone)], C.cream) + fill(poly(stripe(-238, -228)), C.orange) + fill(poly(stripe(-210, -202)), C.orange) +
      dotsOn(cone, 24, 0.24) + line("M-62,-250 L-15,-182 M62,-250 L15,-182", ink, 1.2) +
      solid([poly(lip)], C.orange, 3.4) +
      solid([poly(rect(-31, -182, 31, -163))], C.slate, 3.6) + [-22, -8, 8, 22].map(function (x) { return fill(circ(x, -172.5, 1.8), C.cream); }).join("") + "</g>";
  };

  // ── YES BUTTON ────────────────────────────────────────────────────────
  // A big round button on a console box, 100 wide, 104 tall, its top at a standing person's hand height.
  // o.label: the cap's word ("YES"). o.color: the cap (C.med). o.box: the box (C.slate). o.sub: a word on the
  // front plate ("TREATY").
  // Part: .yes-cap (press it: y 0 -> 9 and back; it sinks into its collar and the box front).
  K.props.yesButton = function (o) {
    o = o || {};
    var capCol = o.color || C.med, boxCol = o.box || C.slate, word = o.label === undefined ? "YES" : o.label;
    var topF = [[-46, -66], [46, -66], [38, -80], [-38, -80]], front = [[-50, 0], [50, 0], [46, -66], [-46, -66]];
    var cap = "M-30,-74 V-97 A30,6.5 0 0 1 30,-97 V-74 A30,6.5 0 0 1 -30,-74 Z";
    var collar = "M-36,-73 A36,7 0 0 0 36,-73 L31,-73 A31,5.5 0 0 1 -31,-73 Z";
    var plate = chamf(-34, -50, 34, -16, 4);
    return '<g class="yes-button">' + solid([poly(topF)], C.peri) +
      solid(['ellipse cx="0" cy="-73" rx="36" ry="7"'], C.cream, 2.6) + fill('ellipse cx="0" cy="-73" rx="31" ry="5.5"', ink) +
      '<g class="yes-cap">' + solid([pathT(cap)], capCol, 3.4) + dots(pathT(cap), 10, -105, 31, -66, 0.22) + solid(['ellipse cx="0" cy="-97" rx="30" ry="6.5"'], C.cyan, 2.4) +
      fill(poly([[-21, -98.4], [-8, -101.6], [-5, -100.2], [-18, -96.6]]), C.cream, ' opacity="0.8"') +
      (word ? block(0, -81, word, 46, 18, C.cream) : "") + "</g>" +
      solid([pathT(collar)], C.cream, 2.6) +
      solid([poly(front)], boxCol) + edge(path([[47.6, -2], [44, -63.6]]), 2) +
      solid([poly(plate)], C.cream, 3) + dotsOn(plate, 8, 0.22) +
      (o.sub ? block(0, -33, o.sub, 56, 16, ink) : K.star(-18, -33, 6, C.orange) + K.star(0, -33, 8, C.orange) + K.star(18, -33, 6, C.orange)) + "</g>";
  };

  // ── Sheet samples (node tools/props-sheet.mjs objects-b) ──────────────
  K.props.SHEET.push(
    ["padlock", {}, "PADLOCK"],
    ["padlock", { open: true, label: "FDA" }, "PADLOCK (open, label)"],
    ["gauge", { label: "SECURITY", value: 0.35 }, "GAUGE (box)"],
    ["gauge", { mount: "dial", value: 0.62, marks: [[0.15, "15%"]], window: "2033", label: "PARASITIC" }, "GAUGE (dial, mark, window)"],
    ["shoppingCart", {}, "SHOPPING CART"],
    ["shoppingCart", { load: "money" }, "SHOPPING CART (money)"],
    ["laptop", { screen: "BUY\nMISSILES" }, "LAPTOP (screen)"],
    ["tvSet", { screen: "NEWS" }, "TV SET (screen)"],
    ["phone", {}, "PHONE"],
    ["phone", { color: C.war, ring: true }, "PHONE (red, ringing)"],
    ["balanceScale", { tilt: 14, left: "CURES", right: "WAR" }, "BALANCE SCALE (tilt 14)"],
    ["door", { label: "FDA", slot: true }, "DOOR (label, slot)"],
    ["door", { label: "FDA", open: 1 }, "DOOR (open)"],
    ["conveyor", {}, "CONVEYOR"],
    ["gears", { n: 3 }, "GEARS (3)"],
    ["gears", { n: 5, labels: ["1", "2", "3", "4", "5"], dark: true }, "GEARS (5, labels, dark)"],
    ["ballotBox", { ballot: true }, "BALLOT BOX (ballot)"],
    ["colorFlipFunnel", {}, "COLOR-FLIP FUNNEL"],
    ["yesButton", {}, "YES BUTTON"],
    ["yesButton", { sub: "TREATY" }, "YES BUTTON (sub)"]
  );
})();
