// Shared props, set A: everyday objects for the episode cartoon (pill bottle, missile, bomb, stamp, stamp mark,
// price tag, sign, calendar, bond, scroll, the manual and a clipboard), drawn the way kit.js draws the humans:
// sharp polygons with mitred corners, thin navy outlines (a navy pass under each fill, so touching shapes of one
// color share one outline), print shading (halftone dots on light shapes, orange edges on navy) and KIT.C colors.
//
// Every prop is drawn around (0,0) standing on y 0 and rising toward -y, in the units of KIT.person (a person is
// about 180 tall with the feet at y 100, so translate a prop by +100 to stand it on a person's ground). The one
// exception is the price tag, which hangs from its knot at (0,0) (o.anchor "bottom" stands it on y 0 instead).
// o.size scales any prop. Every moving part is an untransformed <g class="..."> group; its pivot is given in the
// prop's own units (before o.size), ready for gsap.set(el, { svgOrigin: "x y" }). Ids are unique per call.
(function () {
  var K = window.KIT;
  K.props = K.props || { SHEET: [] };
  K.props.SHEET = K.props.SHEET || [];
  if (K.props.__objects_a) return;
  K.props.__objects_a = true;

  var C = K.C, ink = C.line, LW = 4.4, uid = 0;
  var WHITE = "#FBF6E6"; // the humans' white (shirts, lab coats), a touch brighter than the Layer B paper
  var SERIF = "Fraunces, Georgia, serif";

  // ── Helpers (from the HUMANS section of kit.js) ────────────────────
  function P(x, y) { return (+x).toFixed(1) + "," + (+y).toFixed(1); }
  function polyD(pts) { return "M" + pts.map(function (p) { return P(p[0], p[1]); }).join(" L") + " Z"; }
  function poly(pts) { return 'path d="' + polyD(pts) + '"'; }
  function flipX(pts) { return pts.map(function (p) { return [-p[0], p[1]]; }); }
  function shift(pts, dx, dy) { return pts.map(function (p) { return [p[0] + dx, p[1] + dy]; }); }
  function rect(x, y, w, h) { return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]; }
  // Shapes drawn twice, a navy pass under the fill, so touching shapes of one color share one outline.
  function solid(tags, col, w) {
    w = w || LW;
    return tags.map(function (t) { return "<" + t + ' fill="' + ink + '" stroke="' + ink + '" stroke-width="' + w + '" stroke-linejoin="miter" stroke-miterlimit="8"/>'; }).join("") +
      tags.map(function (t) { return "<" + t + ' fill="' + col + '"/>'; }).join("");
  }
  function line(d, col, w, extra) { return '<path d="' + d + '" fill="none" stroke="' + (col || ink) + '" stroke-width="' + (w || 2) + '" stroke-linejoin="miter" stroke-linecap="round"' + (extra || "") + "/>"; }
  function id(name) { return "kpa-" + name + "-" + ++uid; }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function hash(s) {
    var h = 2166136261;
    for (var i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
    return h >>> 0;
  }
  // Print shading: halftone dots over the part of a light shape right of `from` (0..1 across it).
  function dots(pts, from, op, step) {
    var xs = pts.map(function (p) { return p[0]; }), ys = pts.map(function (p) { return p[1]; });
    var x1 = Math.max.apply(null, xs), x0 = Math.min.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
    var a = x0 + (x1 - x0) * (from === undefined ? 0.55 : from), s = step || 3.6, i = id("hd");
    return '<defs><pattern id="' + i + 'd" width="' + s + '" height="' + s + '" patternUnits="userSpaceOnUse"><circle cx="' + s / 2 + '" cy="' + s / 2 + '" r="' + (s * 0.28).toFixed(2) + '" fill="' + ink + '"/></pattern>' +
      '<clipPath id="' + i + 'c"><path d="' + polyD(pts) + '"/></clipPath></defs>' +
      '<rect x="' + a.toFixed(1) + '" y="' + y0.toFixed(1) + '" width="' + (x1 - a).toFixed(1) + '" height="' + (y1 - y0).toFixed(1) + '" fill="url(#' + i + 'd)" opacity="' + (op || 0.3) + '" clip-path="url(#' + i + 'c)"/>';
  }
  // Oswald SemiBold, centered (anchor "start" for left aligned).
  function text(x, y, s, size, col, extra, anchor) {
    return '<text x="' + (+x).toFixed(1) + '" y="' + (+y).toFixed(1) + '" text-anchor="' + (anchor || "middle") + '" font-family="Oswald" font-weight="600" font-size="' + (+size).toFixed(1) + '" fill="' + col + '"' + (extra || "") + ">" + esc(s) + "</text>";
  }
  // How wide a line of Oswald SemiBold is (KIT.textWidth), with spacing px between letters.
  function textW(s, size, spacing) { return K.textWidth(s, size, "Oswald", 600, spacing); }
  // A tapered bar from a to b (a limb or a strap), w0 wide at a and w1 at b.
  function bar(a, b, w0, w1) {
    var dx = b[0] - a[0], dy = b[1] - a[1], L = Math.sqrt(dx * dx + dy * dy) || 1, nx = -dy / L, ny = dx / L;
    return poly([[a[0] + (nx * w0) / 2, a[1] + (ny * w0) / 2], [b[0] + (nx * w1) / 2, b[1] + (ny * w1) / 2], [b[0] - (nx * w1) / 2, b[1] - (ny * w1) / 2], [a[0] - (nx * w0) / 2, a[1] - (ny * w0) / 2]]);
  }
  // Points turned by deg degrees about the origin, then moved by (tx, ty).
  function rot(pts, deg, tx, ty) {
    var r = (deg * Math.PI) / 180, c = Math.cos(r), s = Math.sin(r);
    return pts.map(function (p) { return [p[0] * c - p[1] * s + (tx || 0), p[0] * s + p[1] * c + (ty || 0)]; });
  }
  // The prop's outer group (class cls), scaled by o.size.
  function wrap(cls, o, inner) {
    var s = o.size || 1;
    return '<g class="' + cls + '">' + (s === 1 ? inner : '<g transform="scale(' + s + ')">' + inner + "</g>") + "</g>";
  }

  // ── Faces ───────────────────────────────────────────────────────────
  // A front-view face in the humans' style (almond eyes with heavy lids, thin angled brows), for props that have
  // one. f: { x, y (the point between the eyes), sp (eye spacing), rx, ry (eye size), my (mouth below the eyes),
  // mw (mouth half width), look "left"|"right", line (brow and mouth color; cream on a dark prop) }.
  // mood: the humans' moods (smile, grin, smug, eager, sad, worried, cross, flat, greedy) plus grumpy (a heavy
  // scowl), scared (wide eyes, gritted teeth, a drop of sweat) and o. Parts, as on the humans: .eye with .pupil,
  // .brows, .mouth (and .teeth, .sweat).
  function face(mood, f) {
    f = f || {};
    var ox = f.x || 0, oy = f.y || 0, sp = f.sp || 10, rx = f.rx || 6, ry = f.ry || 4, my = f.my || 13, mw = f.mw || 8, lc = f.line || ink, u = ry / 4;
    function Q(x, y) { return P(x + ox, y + oy); }
    var wide = mood === "eager" || mood === "scared", happy = mood === "smile" || mood === "grin" || mood === "smug" || mood === "greedy";
    var top = mood === "flat" || mood === "smug" ? -ry * 0.6 : mood === "cross" || mood === "grumpy" ? -ry * 1.25 : -ry * (wide ? 2.5 : 1.8);
    var bot = happy ? ry * 0.55 : ry * (wide ? 1.8 : 1.2);
    var pr = ry * (mood === "scared" ? 0.34 : 0.56), py = (top + bot) / 4 + (mood === "sad" ? ry * 0.2 : 0);
    var px = f.look === "right" ? rx * 0.4 : f.look === "left" ? -rx * 0.4 : 0;
    var eyes = [-1, 1].map(function (s) {
      var x = s * sp;
      if (mood === "greedy") {
        var k = u * 1.2;
        return '<g class="eye"><path d="M' + Q(x + 3 * k, -3 * k) + " C" + Q(x + 3 * k, -6 * k) + " " + Q(x - 3 * k, -6 * k) + " " + Q(x - 3 * k, -3 * k) + " C" + Q(x - 3 * k, 0) + " " + Q(x + 3 * k, 0) + " " + Q(x + 3 * k, 3 * k) +
          " C" + Q(x + 3 * k, 6 * k) + " " + Q(x - 3 * k, 6 * k) + " " + Q(x - 3 * k, 3 * k) + " M" + Q(x, -7.5 * k) + " L" + Q(x, 7.5 * k) + '" fill="none" stroke="' + C.moneyDark + '" stroke-width="' + (2.4 * u).toFixed(2) + '"/></g>';
      }
      var d = "M" + Q(x - rx, 0) + " Q" + Q(x, top) + " " + Q(x + rx, -0.4 * u) + " Q" + Q(x, bot) + " " + Q(x - rx, 0) + " Z", cid = id("eye");
      return '<g class="eye"><defs><clipPath id="' + cid + '"><path d="' + d + '"/></clipPath></defs>' +
        '<path d="' + d + '" fill="' + WHITE + '" stroke="' + ink + '" stroke-width="' + (1.2 * u).toFixed(2) + '"/>' +
        '<g clip-path="url(#' + cid + ')"><circle class="pupil" cx="' + (x + ox + px).toFixed(1) + '" cy="' + (py + oy).toFixed(1) + '" r="' + pr.toFixed(2) + '" fill="' + ink + '"/></g>' +
        '<path d="M' + Q(x - rx - 0.8 * u, 0.5 * u) + " Q" + Q(x, top - 0.7 * u) + " " + Q(x + rx + 0.7 * u, -0.6 * u) + '" fill="none" stroke="' + ink + '" stroke-width="' + (2.2 * u).toFixed(2) + '" stroke-linecap="round"/></g>';
    }).join("");
    // brow heights (in eye heights, up is negative) at its inner end, middle and outer end
    var BR = { grumpy: [-0.7, -1.75, -2.8], cross: [-1.3, -1.95, -2.6], worried: [-3.2, -2.7, -2.0], sad: [-3.0, -2.6, -2.0], scared: [-4.0, -3.6, -3.0],
      flat: [-1.35, -1.4, -1.45], eager: [-3.1, -3.6, -3.1], smug: [-1.4, -1.5, -1.5] }[mood] || [-2.3, -2.8, -2.4];
    var brows = [-1, 1].map(function (s) {
      var b = mood === "smug" && s > 0 ? [-2.6, -3.4, -2.8] : BR;
      return "M" + Q(s * (sp + rx + u), b[2] * ry) + " L" + Q(s * sp, b[1] * ry) + " L" + Q(s * (sp - rx * 0.85), b[0] * ry);
    }).join(" ");
    var bw = (mood === "grumpy" ? 4.2 : mood === "cross" ? 3.2 : 2.5) * u;
    var y = my, fill = "none", mw2, d, teeth = "", extra = "";
    function L(pts) { return pts.map(function (p, i) { return (i ? " L" : "M") + Q(p[0], p[1]); }).join(""); }
    if (mood === "smile") {
      d = "M" + Q(-mw, y - u) + " Q" + Q(0, y + 1.5 * u) + " " + Q(mw, y - u) + " Q" + Q(0, y + mw * 1.25) + " " + Q(-mw, y - u) + " Z";
      fill = WHITE;
      extra = line("M" + Q(-mw - 2 * u, y - 3 * u) + " Q" + Q(-mw - 2.6 * u, y) + " " + Q(-mw - 0.6 * u, y + 2 * u) + " M" + Q(mw + 2 * u, y - 3 * u) + " Q" + Q(mw + 2.6 * u, y) + " " + Q(mw + 0.6 * u, y + 2 * u), lc, 1.4 * u);
    } else if (mood === "grin" || mood === "greedy") {
      mw2 = mw * 1.15;
      d = L([[-mw2, y - 2 * u], [mw2, y - 2 * u], [mw * 0.7, y + mw * 0.8], [-mw * 0.7, y + mw * 0.8]]) + " Z";
      fill = WHITE;
      teeth = line("M" + Q(-mw * 0.45, y - 2 * u) + " L" + Q(-mw * 0.42, y + mw * 0.8) + " M" + Q(0, y - 2 * u) + " L" + Q(0, y + mw * 0.8) + " M" + Q(mw * 0.45, y - 2 * u) + " L" + Q(mw * 0.42, y + mw * 0.8) +
        " M" + Q(-mw, y + mw * 0.3) + " L" + Q(mw, y + mw * 0.3), ink, 1.1 * u, ' class="teeth"');
    } else if (mood === "smug") {
      d = "M" + Q(-mw * 0.8, y + u) + " Q" + Q(mw * 0.1, y + 2.8 * u) + " " + Q(mw * 0.95, y - 3 * u);
      extra = line("M" + Q(mw * 0.95 + 0.6 * u, y - 5.5 * u) + " L" + Q(mw * 1.15, y - 1.5 * u), lc, 1.4 * u);
    } else if (mood === "eager") {
      d = L([[-mw * 0.75, y - u], [mw * 0.75, y - u], [mw * 0.5, y + mw * 0.85], [-mw * 0.5, y + mw * 0.85]]) + " Z";
      fill = ink;
    } else if (mood === "sad") {
      d = "M" + Q(-mw * 0.8, y + 3 * u) + " Q" + Q(0, y - 3.5 * u) + " " + Q(mw * 0.8, y + 3 * u);
    } else if (mood === "grumpy") {
      d = "M" + Q(-mw, y + 3.5 * u) + " Q" + Q(0, y - 5 * u) + " " + Q(mw, y + 3.5 * u);
      extra = line("M" + Q(-mw * 0.35, y + 7.5 * u) + " Q" + Q(0, y + 5.8 * u) + " " + Q(mw * 0.35, y + 7.5 * u), lc, 1.6 * u);
    } else if (mood === "cross") {
      d = L([[-mw * 0.8, y + 2 * u], [-mw * 0.45, y], [mw * 0.45, y], [mw * 0.8, y + 2 * u]]);
    } else if (mood === "worried") {
      var zz = [];
      for (var i = 0; i <= 6; i++) zz.push([-mw + (i * mw) / 3, y + (i % 2 ? -1.5 : 1.5) * u]);
      d = L(zz);
    } else if (mood === "scared") {
      d = L([[-mw - u, y + 1.5 * u], [-mw * 0.8, y - 3 * u], [mw * 0.8, y - 3 * u], [mw + u, y + 1.5 * u], [mw * 0.8, y + 5.5 * u], [-mw * 0.8, y + 5.5 * u]]) + " Z";
      fill = WHITE;
      teeth = line("M" + Q(-mw * 0.9, y + 1.2 * u) + " L" + Q(mw * 0.9, y + 1.2 * u) + " M" + Q(-mw * 0.45, y - 3 * u) + " L" + Q(-mw * 0.45, y + 5.5 * u) + " M" + Q(0, y - 3 * u) + " L" + Q(0, y + 5.5 * u) +
        " M" + Q(mw * 0.45, y - 3 * u) + " L" + Q(mw * 0.45, y + 5.5 * u), ink, 1.1 * u, ' class="teeth"');
      var sx = sp + rx + 4.5 * u, sy = -ry * 2.4;
      extra = '<path class="sweat" d="M' + Q(sx, sy - 5.5 * u) + " Q" + Q(sx + 4 * u, sy + u) + " " + Q(sx, sy + 3.6 * u) + " Q" + Q(sx - 4 * u, sy + u) + " " + Q(sx, sy - 5.5 * u) + ' Z" fill="' + WHITE + '" stroke="' + ink + '" stroke-width="' + (1.3 * u).toFixed(2) + '"/>';
    } else if (mood === "o") {
      d = "M" + Q(-3 * u, y + 2 * u) + " A" + (3 * u).toFixed(2) + "," + (3.4 * u).toFixed(2) + " 0 1 0 " + Q(3 * u, y + 2 * u) + " A" + (3 * u).toFixed(2) + "," + (3.4 * u).toFixed(2) + " 0 1 0 " + Q(-3 * u, y + 2 * u) + " Z";
      fill = ink;
    } else {
      d = L([[-mw * 0.7, y], [mw * 0.7, y]]);
    }
    var mwid = (mood === "grumpy" ? 3.2 : fill !== "none" ? 1.8 : 2.4) * u;
    return '<g class="face">' + eyes +
      '<path class="brows" d="' + brows + '" fill="none" stroke="' + lc + '" stroke-width="' + bw.toFixed(2) + '" stroke-linejoin="miter" stroke-linecap="round"/>' +
      '<path class="mouth" d="' + d + '" fill="' + fill + '" stroke="' + lc + '" stroke-width="' + mwid.toFixed(2) + '" stroke-linejoin="miter" stroke-linecap="round"/>' + teeth + extra + "</g>";
  }

  // ── PILL BOTTLE ─────────────────────────────────────────────────────
  // An orange pill bottle with a white child-proof cap and a label; o.face gives it a face (a mood, as the humans').
  // 58 wide, 106 tall. o: { size, face (none by default), look, label (default "Rx"; "" for none),
  // pills (default true: three capsules waiting under the cap) }.
  // Parts: .pill-cap (flip it open about its bottom left corner (-27, -84), or pop it straight up from (0, -84)),
  // .pill-pills (three capsules under the cap, around (0, -88): they show once the cap is off; fling them up),
  // and with a face: .eye .pupil .brows .mouth.
  function capsule(x, y, a) {
    var half = [[-8, -1.6], [-6.4, -3.6], [0, -3.6], [0, 3.6], [-6.4, 3.6], [-8, 1.6]];
    return '<g transform="translate(' + x + "," + y + ") rotate(" + a + ')">' + solid([poly(half)], C.med, 2.4) + solid([poly(flipX(half))], WHITE, 2.4) + "</g>";
  }
  K.props.pillBottle = function (o) {
    o = o || {};
    var f = o.face, lt = f ? -40 : -60, lb = -10, lab = o.label === undefined ? "Rx" : o.label;
    var body = [[-29, 0], [29, 0], [29, -74], [23, -80], [-23, -80], [-29, -74]];
    var neck = rect(-21, -86, 42, 8);
    var cap = [[-27, -84], [27, -84], [27, -102], [23, -106], [-23, -106], [-27, -102]];
    var label = rect(-29, lt, 58, lb - lt);
    var pills = '<g class="pill-pills">' + (o.pills === false ? "" : capsule(-9, -89, -32) + capsule(3, -92, 14) + capsule(12, -88, 62)) + "</g>";
    var labelArt = solid([poly(label)], WHITE) + dots(label, 0.62, 0.22) +
      (f ? (lab ? text(0, lt + 17, lab, 15, ink) : "") + '<g opacity="0.55">' + line("M-17,-17 H17", ink, 1.4) + line("M-12,-13 H12", ink, 1.4) + "</g>"
        : (lab ? text(0, lt + 25, lab, 22, ink) : "") + '<g opacity="0.55">' + line("M-18,-32 H18", ink, 1.4) + line("M-18,-26 H18", ink, 1.4) + line("M-12,-20 H12", ink, 1.4) + "</g>");
    var ridges = "";
    for (var x = -21; x <= 21; x += 6) ridges += line("M" + x + ",-88 V-101", ink, 1.2);
    var capArt = '<g class="pill-cap">' + solid([poly(cap)], WHITE) + dots(cap, 0.6, 0.25) + '<g opacity="0.5">' + ridges + "</g>" + line("M-27,-90 H27", ink, 1.6) + "</g>";
    return wrap("pill-bottle", o, pills + solid([poly(body), poly(neck)], C.orange) + dots(body, 0.6, 0.22) +
      '<path d="' + polyD([[-24, -8], [-19, -8], [-19, -72], [-24, -70]]) + '" fill="' + C.cream + '" opacity="0.75"/>' +
      line("M24,-6 V-72", C.rust, 2.2) + labelArt +
      (f ? face(f, { x: 0, y: -62, sp: 11, rx: 6.5, ry: 4.2, my: 12, mw: 7, look: o.look }) : "") + capArt);
  };

  // ── MISSILE ─────────────────────────────────────────────────────────
  // The grumpy hero missile of the theme song: a war-red bullet (o.color) with a navy nose cone, a riveted band
  // and navy fins it stands on, arms crossed, scowling. 100 wide (fins), 160 tall at size 1.
  // o: { size, mood "grumpy" (default) | "smug" | "scared" (or any face mood), arms "crossed" (default; "up" when
  // scared) | "up" | "none", flame (show the launch flame), look, color }.
  // Parts: .missile-flame (the launch flame under the nozzle, hidden unless o.flame: tween its opacity and scaleY
  // about (0, -8); its .flame tongues work with KIT.flicker), .missile-arm-l / .missile-arm-r (shoulders (-27, -62)
  // and (27, -62)), .eye .pupil .brows .mouth (and .sweat when scared).
  function fist(x, y, s) {
    return poly([[x - 5 * s, y - 4], [x + 2 * s, y - 6.5], [x + 7 * s, y - 2], [x + 5.5 * s, y + 5], [x - 2 * s, y + 6], [x - 6 * s, y + 1.5]]);
  }
  function openHand(x, y, s) {
    return poly([[x - 6 * s, y + 3], [x - 10 * s, y - 7], [x - 7.5 * s, y - 8.5], [x - 4 * s, y - 3], [x - 4.5 * s, y - 13], [x - 1.5 * s, y - 13.5], [x - 0.5 * s, y - 5], [x + 1.5 * s, y - 14], [x + 4.5 * s, y - 13],
      [x + 3 * s, y - 4], [x + 6 * s, y - 10.5], [x + 8.5 * s, y - 9], [x + 5.5 * s, y + 3]]);
  }
  K.props.missile = function (o) {
    o = o || {};
    var mood = o.mood || "grumpy", col = o.color || C.war, arms = o.arms || (mood === "scared" ? "up" : "crossed");
    var body = [[-28, -116], [28, -116], [28, -44], [21, -23], [13, -15], [-13, -15], [-21, -23], [-28, -44]];
    var nose = 'path d="M-28,-116 Q-27,-146 0,-160 Q27,-146 28,-116 Z"';
    var finL = [[-26, -70], [-50, -28], [-50, 0], [-37, 0], [-20, -25]];
    var flame = '<g class="missile-flame"' + (o.flame ? "" : ' opacity="0"') + '><g transform="translate(0,-8) rotate(180)">' + K.flames(0, 0, 0.44) + "</g></g>";
    var fins = solid([poly(finL), poly(flipX(finL))], ink, 3) + line("M-46,-29 L-46,-3", C.orange, 1.8) + line("M46,-29 L46,-3", C.orange, 1.8) + line("M-29,-64 L-46,-31", C.orange, 1.6);
    var shell = solid([poly(body)], col) + dots(body, 0.62, 0.22) +
      '<path d="' + polyD([[-23, -106], [-17.5, -106], [-17.5, -50], [-23, -50]]) + '" fill="' + C.cream + '" opacity="0.6"/>' +
      solid([nose, poly(rect(-28, -118, 56, 7))], ink) +
      '<path d="M-19,-121 Q-18,-141 -4,-152 Q-12,-139 -12,-121 Z" fill="' + C.cream + '" opacity="0.85"/>' + line("M23,-121 Q22,-139 7,-151", C.orange, 1.8) +
      solid([poly([[-28, -46], [28, -46], [28, -44], [26, -38], [-26, -38], [-28, -44]])], ink) + [-20, -12, -4, 4, 12, 20].map(function (x) { return '<circle cx="' + x + '" cy="-42" r="1.7" fill="' + C.cream + '"/>'; }).join("") +
      solid([poly([[-12, -16], [12, -16], [15, -6], [-15, -6]])], ink) + line("M11,-12 L13,-8", C.orange, 1.6) +
      solid([poly([[-4, -30], [4, -30], [5.5, 0], [-5.5, 0]])], ink, 3) + line("M2.5,-26 L3.5,-3", C.orange, 1.5);
    var faceArt = face(mood, { x: 0, y: -90, sp: 12.5, rx: 9.5, ry: 6, my: 17, mw: 9.5, look: o.look });
    var armArt = "";
    if (arms === "crossed") {
      armArt = '<g class="missile-arm-l">' + solid([bar([-27, -62], [-40, -44], 10, 9), bar([-40, -44], [11, -51], 9, 8), fist(11, -51, 1)], col) + "</g>" +
        '<g class="missile-arm-r">' + solid([bar([27, -62], [40, -44], 10, 9), bar([40, -44], [-11, -51], 9, 8), fist(-11, -51, -1)], col) + line("M-15,-53 L-9,-54.5", ink, 1.2) + "</g>";
    } else if (arms === "up") {
      armArt = [-1, 1].map(function (s) {
        return '<g class="missile-arm-' + (s < 0 ? "l" : "r") + '">' + solid([bar([s * 27, -62], [s * 47, -76], 10, 9), bar([s * 47, -76], [s * 51, -104], 9, 8), openHand(s * 51, -106, s)], col) + "</g>";
      }).join("");
    }
    return wrap("missile", o, flame + fins + shell + faceArt + armArt);
  };

  // ── BOMB ────────────────────────────────────────────────────────────
  // A round cartoon bomb: a navy-black ball 84 across sitting on y 0, a steel collar and a fuse curling up to a
  // spark at (84, -130). o: { size, lit (default true: the spark shows), face (a mood: cream brows and mouth),
  // look, text (painted on the ball in cream) }.
  // Parts: .bomb-spark (its own center is the fuse tip: pivot (0, 0); pulse its scale), .bomb-fuse (two paths with
  // pathLength 1: tween both paths' stroke-dashoffset 0 -> 1 to burn the fuse down to the collar; to keep the spark
  // on the burning end, set its x, y to fuse.getPointAtLength(fuse.getTotalLength() * (1 - offset)) minus (84, -130)),
  // .bomb-ball (the ball, collar and face: swell it about the ball's center (0, -42)).
  K.props.bomb = function (o) {
    o = o || {};
    var R = 42, cy = -42, ang = 40, sx = R * Math.sin((ang * Math.PI) / 180), sy = cy - R * Math.cos((ang * Math.PI) / 180);
    var collar = rot(rect(-11, -14, 22, 16), ang, sx, sy), rim = rot([[-11, -14], [11, -14]], ang, sx, sy);
    var fd = "M36,-85 C40,-100 58,-98 60,-110 C62,-122 70,-132 84,-130";
    var fuse = '<g class="bomb-fuse"><path d="' + fd + '" fill="none" stroke="' + ink + '" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0"/>' +
      '<path d="' + fd + '" fill="none" stroke="' + C.tan + '" stroke-width="3.4" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0"/></g>';
    var arc = function (a0, a1, r) {
      var p0 = [r * Math.cos((a0 * Math.PI) / 180), cy + r * Math.sin((a0 * Math.PI) / 180)], p1 = [r * Math.cos((a1 * Math.PI) / 180), cy + r * Math.sin((a1 * Math.PI) / 180)];
      return "M" + P(p0[0], p0[1]) + " A" + r + "," + r + " 0 0 1 " + P(p1[0], p1[1]);
    };
    var ball = '<g class="bomb-ball">' + solid([poly(collar)], C.peri, 3.6) + line("M" + P(rim[0][0], rim[0][1]) + " L" + P(rim[1][0], rim[1][1]), ink, 2.4) +
      line("M" + P(rot([[-6, -11]], ang, sx, sy)[0][0], rot([[-6, -11]], ang, sx, sy)[0][1]) + " L" + P(rot([[-6, 0]], ang, sx, sy)[0][0], rot([[-6, 0]], ang, sx, sy)[0][1]), C.cream, 2, ' opacity="0.7"') +
      solid(['circle cx="0" cy="' + cy + '" r="' + R + '"'], C.deep) +
      line(arc(8, 78, R - 5), C.orange, 2.4) +
      '<path d="M-31,-55 Q-27,-73 -11,-79 Q-23,-69 -25,-53 Z" fill="' + C.cream + '" opacity="0.9"/><circle cx="-32" cy="-46" r="2.6" fill="' + C.cream + '" opacity="0.9"/>' +
      (o.face ? face(o.face, { x: -3, y: -48, sp: 12, rx: 7.5, ry: 5, my: 15, mw: 9, look: o.look, line: C.cream }) : "") +
      (o.text ? text(-2, o.face ? -12 : -32, o.text, 16, C.cream, ' letter-spacing="1"') : "") + "</g>";
    var spark = '<g transform="translate(84,-130)"><g class="bomb-spark"' + (o.lit === false ? ' opacity="0"' : "") + ">" +
      K.star(0, 0, 19, C.orange, 6) + K.star(0, 0, 11, C.yellow, 6) + '<circle r="3.2" fill="#FFFFFF"/></g></g>';
    return wrap("bomb", o, fuse + ball + spark);
  };

  // ── STAMP ───────────────────────────────────────────────────────────
  // A rubber stamp standing on its rubber: a wooden knob and neck, a block with a label saying what it stamps
  // (o.text) and the inked rubber (o.color). 96 wide, 92 tall. o: { size, text (default "APPROVED"; "" for a
  // blank label), color (the ink, default war red), pad (an ink pad under it: the stamp then stands at y -16) }.
  // Parts: .stamp-head (the stamp itself: squash it about the middle of its rubber face (0, 0), or (0, -16) on
  // the pad; slam it down with y).
  K.props.stamp = function (o) {
    o = o || {};
    var b = o.pad ? -16 : 0, col = o.color || C.war, t = o.text === undefined ? "APPROVED" : String(o.text);
    function sh(pts) { return shift(pts, 0, b); }
    var rubber = sh(rect(-44, -7, 88, 7)), block = sh(rect(-48, -30, 96, 24)), bevel = sh([[-48, -29], [48, -29], [40, -37], [-40, -37]]);
    var neck = sh([[-9, -36], [9, -36], [6.5, -60], [-6.5, -60]]), knob = sh([[-13, -58], [13, -58], [19, -68], [19, -82], [12, -92], [-12, -92], [-19, -82], [-19, -68]]);
    var label = sh(rect(-38, -25, 76, 14)), fs = K.fitText(t, 11, 68, "Oswald", 600, 0.5);
    var head = '<g class="stamp-head">' + solid([poly(rubber)], col) + solid([poly(block)], C.tan) + dots(block, 0.6, 0.25) + solid([poly(bevel)], C.rust) +
      (t ? solid([poly(label)], WHITE, 2.4) + text(0, b - 18 + fs * 0.37, t, fs, col, ' letter-spacing="0.5"') : "") +
      solid([poly(neck)], C.tan) + solid([poly(knob)], C.rust) + '<path d="' + polyD(sh([[-14, -70], [-10, -70], [-9, -86], [-12, -84]])) + '" fill="' + C.cream + '" opacity="0.6"/>' +
      line("M" + P(15, b - 70) + " L" + P(15, b - 81), C.orange, 1.6) + "</g>";
    var pad = o.pad ? solid([poly(rect(-58, -12, 116, 12))], C.slate) + line("M54,-9 V-3", C.orange, 1.6) + solid([poly(rect(-52, -16, 104, 4))], col, 2.4) + text(0, -2.5, "INK", 8, C.cream, ' letter-spacing="1"') : "";
    return wrap("stamp", o, pad + head);
  };

  // ── STAMP MARK ──────────────────────────────────────────────────────
  // The inked impression of a rubber stamp: o.text (a "\n" breaks lines) in a double-ruled box, in o.color (default
  // war red), turned o.angle degrees (default -8), with worn ink. Its lowest corner sits on y 0. About 40 wide plus
  // 20 per letter at the default o.fontSize 34. o: { size, text (default "APPROVED"), color, angle, fontSize }.
  // Parts: .stamp-mark (slam it in from scale 1.8 and opacity 0 about its center (0, data-cy), e.g. (0, -38)).
  K.props.stampMark = function (o) {
    o = o || {};
    var col = o.color || C.war, fs = o.fontSize || 34, a = o.angle === undefined ? -8 : o.angle;
    var lines = String(o.text === undefined ? "APPROVED" : o.text).split("\n");
    var n = lines.length;
    var w = Math.max.apply(null, lines.map(function (l) { return textW(l, fs, fs * 0.08); })) + 40, lh = fs * 1.08, h = (n - 1) * lh + fs * 0.74 + 34;
    var r = (a * Math.PI) / 180, cy = -(w * Math.abs(Math.sin(r)) + h * Math.abs(Math.cos(r))) / 2;
    var mid = id("mk"), rnd = K.rng(hash(lines.join("|") + col)), specks = "";
    for (var i = 0; i < Math.round((w * h) / 70); i++) specks += '<circle cx="' + ((rnd() - 0.5) * w).toFixed(1) + '" cy="' + ((rnd() - 0.5) * h).toFixed(1) + '" r="' + (0.5 + rnd() * 1.4).toFixed(2) + '" fill="#000"/>';
    for (var k = 0; k < 7; k++) {
      var sx = (rnd() - 0.5) * w, sy = (rnd() - 0.5) * h;
      specks += '<path d="M' + P(sx, sy) + " l" + (6 + rnd() * 14).toFixed(1) + "," + ((rnd() - 0.5) * 3).toFixed(1) + '" stroke="#000" stroke-width="' + (0.8 + rnd()).toFixed(1) + '" stroke-linecap="round"/>';
    }
    var art = '<rect x="' + (-w / 2).toFixed(1) + '" y="' + (-h / 2).toFixed(1) + '" width="' + w.toFixed(1) + '" height="' + h.toFixed(1) + '" fill="none" stroke="' + col + '" stroke-width="5"/>' +
      '<rect x="' + (-w / 2 + 7).toFixed(1) + '" y="' + (-h / 2 + 7).toFixed(1) + '" width="' + (w - 14).toFixed(1) + '" height="' + (h - 14).toFixed(1) + '" fill="none" stroke="' + col + '" stroke-width="2.2"/>' +
      lines.map(function (l, i) { return text(0, (i - (n - 1) / 2) * lh + fs * 0.37, l, fs, col, ' letter-spacing="' + (fs * 0.08).toFixed(1) + '"'); }).join("");
    return wrap("stampmark", o, '<g class="stamp-mark" data-cy="' + cy.toFixed(1) + '"><defs><mask id="' + mid + '" maskUnits="userSpaceOnUse" x="' + (-w / 2 - 10).toFixed(1) + '" y="' + (-h / 2 - 10).toFixed(1) + '" width="' + (w + 20).toFixed(1) + '" height="' + (h + 20).toFixed(1) + '">' +
      '<rect x="' + (-w / 2 - 10).toFixed(1) + '" y="' + (-h / 2 - 10).toFixed(1) + '" width="' + (w + 20).toFixed(1) + '" height="' + (h + 20).toFixed(1) + '" fill="#FFF"/>' + specks + "</mask></defs>" +
      '<g transform="translate(0,' + cy.toFixed(1) + ") rotate(" + a + ')"><g mask="url(#' + mid + ')" opacity="0.92">' + art + "</g></g></g>");
  };

  // ── CASE FILE ───────────────────────────────────────────────────────
  // The Earth case file, a manila folder standing on y 0, 190 wide, its tab up to y -168 and as wide as its words:
  // o.tab (default "EARTH DIRT: CASE #847", EARTH struck out in red, as Part 1 renames the planet; "EARTH: CASE #847"
  // before that). o.stamps: how many of its marks are on the cover, in story order: 1 MAY BE ELIGIBLE FOR
  // OPTIMIZATION (Part 1), 2 SUBOPTIMAL (Part 12), 3 ELIGIBLE FOR OPTIMIZATION (Part 26). o.dusty grays it under
  // decades of dust. o: { size, tab, stamps, dusty }. Parts: .case-tab, .case-stamp-1 to .case-stamp-3 (each a
  // KIT.props.stampMark, slammed in about its own center).
  K.props.caseFile = function (o) {
    o = o || {};
    var tab = o.tab === undefined ? "EARTH DIRT: CASE #847" : String(o.tab), sp = 0.5, fs = K.fitText(tab, 12, 146, "Oswald", 600, sp);
    var half = textW(tab, fs, sp) / 2 + 10, manila = o.dusty ? "#BDB29A" : "#E7C98C", n = o.stamps || 0;
    var folder = [[-95, 0], [-95, -150], [-half - 10, -150], [-half, -168], [half, -168], [half + 10, -150], [95, -150], [95, 0]];
    var strike = "";
    if (/^EARTH DIRT/.test(tab)) {
      var x0 = -textW(tab, fs, sp) / 2, x1 = x0 + textW("EARTH", fs, sp);
      strike = line("M" + P(x0 - 1, -157.5) + " L" + P(x1 + 1, -159), C.war, 2.2);
    }
    var marks = [
      { text: "MAY BE ELIGIBLE\nFOR OPTIMIZATION", fontSize: 13, angle: -5, y: -80 },
      { text: "SUBOPTIMAL", fontSize: 20, angle: 4, y: -12 },
      { text: "ELIGIBLE FOR\nOPTIMIZATION", fontSize: 17, angle: -12, y: -36, color: C.med },
    ];
    var stamps = marks.slice(0, n).map(function (m, i) {
      return '<g transform="translate(0,' + m.y + ')"><g class="case-stamp-' + (i + 1) + '">' + K.props.stampMark(m) + "</g></g>";
    }).join("");
    var body = solid([poly(folder)], manila, 4) + (o.dusty ? "" : dots(folder, 0.6, 0.18)) +
      '<g class="case-tab">' + text(0, -154, tab, fs, ink, ' letter-spacing="' + sp + '"') + strike + "</g>" +
      '<g opacity="' + (o.dusty ? 0.45 : 1) + '">' + stamps + "</g>";
    return wrap("case-file", o, body);
  };

  // ── PRICE TAG ───────────────────────────────────────────────────────
  // A white card tag with a grommet, its price in o.text (default "$1,000,000"), hanging on a string from a knot at
  // (0, 0) and tilted down to the right: tie it to anything by placing (0, 0) there. o.anchor "bottom" stands it
  // on y 0 instead (the knot is then at (0, data-knot)). About 30 + 9 per character wide, 60 tall.
  // o: { size, text, angle (the tilt, default 22), color (the card), ink (the price, default navy), anchor }.
  // Parts: .tag-swing (the string and the card: swing it about the knot (0, 0)).
  K.props.priceTag = function (o) {
    o = o || {};
    var t = String(o.text === undefined ? "$1,000,000" : o.text), fs = 18, h = 30, tw = textW(t, fs), W = tw + 30, a = o.angle === undefined ? 22 : o.angle, hx = 3, hy = 28;
    var card = [[-12, -h / 2 + 8], [-3, -h / 2], [W, -h / 2], [W, h / 2], [-3, h / 2], [-12, h / 2 - 8]];
    var tag = '<g transform="translate(' + hx + "," + hy + ") rotate(" + a + ')">' + solid([poly(card)], o.color || WHITE, 4) + dots(card, 0.6, 0.22) +
      '<rect x="8" y="' + (-h / 2 + 4) + '" width="' + (W - 12).toFixed(1) + '" height="' + (h - 8) + '" fill="none" stroke="' + C.orange + '" stroke-width="1.3"/>' +
      '<circle r="6" fill="' + C.yellow + '" stroke="' + ink + '" stroke-width="1.6"/><circle r="2.8" fill="' + C.paper + '" stroke="' + ink + '" stroke-width="1.2"/>' +
      text((8 + W) / 2, fs * 0.36, t, fs, o.ink || ink, ' letter-spacing="0.4"') + "</g>";
    var string = line("M0,0 Q-6,14 " + hx + "," + hy, ink, 1.8) + '<circle r="2.6" fill="none" stroke="' + ink + '" stroke-width="1.6"/>' + line("M-1.5,2 L-5,8 M1.5,2 L3.5,9", ink, 1.4);
    var swing = '<g class="tag-swing">' + string + tag + "</g>";
    if (o.anchor !== "bottom") return wrap("price-tag", o, swing);
    var low = Math.max.apply(null, rot(card, a, hx, hy).map(function (p) { return p[1]; })) + 2.5;
    return wrap("price-tag", o, '<g transform="translate(0,' + (-low).toFixed(1) + ')" data-knot="' + (-low).toFixed(1) + '">' + swing + "</g>");
  };

  // ── SIGN ────────────────────────────────────────────────────────────
  // A sign card on two posts (o.posts 1: one pole), as Part 1's pentagon signs: o.text (a "\n" breaks lines) in
  // Oswald on a white card with an orange inner rule, its bottom o.height (default 70) above y 0. About 64 wide
  // plus 19 per letter at the default o.fontSize 34. o: { size, text, fontSize, color (the lettering, default
  // navy), height, posts }.
  // Parts: .sign-posts, .sign-card (wobble or flip it about its bottom middle (0, -height); spring the whole sign
  // up from (0, 0)), .sign-text (the lettering).
  K.props.sign = function (o) {
    o = o || {};
    var lines = String(o.text === undefined ? "SIGN" : o.text).split("\n"), size = o.fontSize || 34, n = lines.length, col = o.color || ink;
    var w = Math.round(Math.max.apply(null, lines.map(function (l) { return textW(l, size, size * 0.05); })) + 64), lh = size * 1.1, h = Math.round(size * 1.75 + (n - 1) * lh);
    var bottom = -(o.height === undefined ? 70 : o.height), top = bottom - h, cy = (top + bottom) / 2;
    var posts = o.posts === 1 ? '<path d="M0,' + (bottom - 8) + ' V0" stroke="' + ink + '" stroke-width="7" stroke-linecap="round"/>'
      : '<path d="M' + (-w / 2 + 30) + "," + (bottom - 8) + " V0 M" + (w / 2 - 30) + "," + (bottom - 8) + ' V0" stroke="' + ink + '" stroke-width="7"/>';
    var card = '<rect x="' + -w / 2 + '" y="' + top + '" width="' + w + '" height="' + h + '" rx="4" fill="' + WHITE + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<rect x="' + (-w / 2 + 8) + '" y="' + (top + 8) + '" width="' + (w - 16) + '" height="' + (h - 16) + '" rx="2" fill="none" stroke="' + C.orange + '" stroke-width="2"/>' +
      '<g class="sign-text">' + lines.map(function (l, i) { return text(0, cy + (i - (n - 1) / 2) * lh + size * 0.37, l, size, col, ' letter-spacing="' + (size * 0.05).toFixed(1) + '"'); }).join("") + "</g>";
    return wrap("sign", o, '<g class="sign-posts">' + posts + '</g><g class="sign-card">' + card + "</g>");
  };

  // ── CALENDAR ────────────────────────────────────────────────────────
  // A tear-off desk calendar: a slate stand and back board, a binding bar with two rings, and pages with the month
  // (o.month, default "JAN") on a red band over a big day (o.day, default 1). 100 wide, 112 tall.
  // o: { size, month, day, pages (default 1: how many tear-off pages; the top one shows o.day, each one under it the
  // next day), color (the month band) }.
  // Parts: .cal-page (one per tear-off page, data-day; the top page is the last in the group): tear it off about
  // its top middle (0, -98) or peel it from its top left corner (-40, -98); the page under it shows the next day.
  K.props.calendar = function (o) {
    o = o || {};
    var month = String(o.month === undefined ? "JAN" : o.month).toUpperCase(), d0 = o.day === undefined ? 1 : o.day, n = Math.max(1, o.pages || 1), band = o.color || C.war;
    var num = typeof d0 === "number" || /^\d+$/.test(String(d0));
    var dayAt = function (i) { return num ? String(+d0 + i) : String(d0); };
    var pg = rect(-40, -98, 80, 82);
    function page(i, cls) {
      var dd = dayAt(i), fs = dd.length > 2 ? 32 : 44;
      return '<g class="' + cls + '" data-day="' + esc(dd) + '">' + solid([poly(pg)], WHITE, 3.6) + dots(pg, 0.62, 0.2) + solid([poly(rect(-40, -98, 80, 19))], band, 3.6) +
        text(0, -84, month, 13, WHITE, ' letter-spacing="1.5"') +
        '<text x="0" y="-31" text-anchor="middle" font-family="' + SERIF + '" font-weight="900" font-size="' + fs + '" fill="' + ink + '">' + esc(dd) + "</text>" +
        line("M-20,-23 H20", C.orange, 1.6) + "</g>";
    }
    var pages = "";
    for (var i = n; i >= 0; i--) pages += page(i, i === n ? "cal-page-under" : "cal-page");
    return wrap("calendar", o, solid([poly(rect(-44, -104, 88, 92))], C.slate) + line("M41,-100 V-16", C.orange, 1.6) +
      solid([poly([[-50, 0], [50, 0], [46, -12], [-46, -12]])], C.navy) + line("M-44,-6 H44", C.orange, 1.6) +
      line("M-38,-14 H38", ink, 1.2) + pages +
      solid([poly(rect(-46, -106, 92, 9))], C.navy) + line("M-42,-102 H42", C.orange, 1.2) +
      [-22, 22].map(function (x) { return solid([poly(rect(x - 3, -111, 6, 15))], C.yellow, 2.4); }).join(""));
  };

  // ── BOND ────────────────────────────────────────────────────────────
  // A fancy bond certificate standing on its bottom edge: a money green guilloche border with corner rosettes, the
  // title o.text (default "BOND"), its value o.value (default "$1,000"; "" for none), a generic portrait in a wig (as
  // on the money), fine print, a signature, and a gold seal with ribbons (o.seal "war" or "med" puts the money's
  // missile or cross seal inside it). 176 wide, 116 tall. o: { size, text, value, seal }.
  // Parts: .bond-seal (spin or stamp it in about its center (54, -34)).
  K.props.bond = function (o) {
    o = o || {};
    var title = String(o.text === undefined ? "BOND" : o.text), value = o.value === undefined ? "$1,000" : String(o.value), green = C.moneyDark;
    var outer = rect(-88, -116, 176, 116);
    var band = '<path d="' + polyD(rect(-83, -111, 166, 106)) + " " + polyD(rect(-73, -101, 146, 86)) + '" fill="' + C.money + '" fill-rule="evenodd" stroke="' + green + '" stroke-width="1.4"/>';
    // the guilloche: a zigzag running round the middle of the band
    var zz = [], step = 4.4, k = 0;
    function run(x0, y0, x1, y1) {
      var L = Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0)), m = Math.round(L / step), nx = y1 === y0 ? 0 : 1, ny = y1 === y0 ? 1 : 0;
      for (var j = 0; j < m; j++, k++) { var t = j / m, s = k % 2 ? 2.6 : -2.6; zz.push([x0 + (x1 - x0) * t + nx * s, y0 + (y1 - y0) * t + ny * s]); }
    }
    run(-78, -106, 78, -106); run(78, -106, 78, -10); run(78, -10, -78, -10); run(-78, -10, -78, -106);
    var guilloche = '<path d="' + polyD(zz) + '" fill="none" stroke="' + green + '" stroke-width="1.1" stroke-linejoin="miter"/>';
    var rosette = function (x, y) { return '<circle cx="' + x + '" cy="' + y + '" r="9.5" fill="' + WHITE + '" stroke="' + green + '" stroke-width="1.6"/>' + K.star(x, y, 8, green, 8) + '<circle cx="' + x + '" cy="' + y + '" r="2" fill="' + WHITE + '"/>'; };
    var portrait = '<ellipse cx="-50" cy="-44" rx="13" ry="16" fill="' + C.cream + '" stroke="' + green + '" stroke-width="2"/>' +
      '<circle cx="-50" cy="-47" r="5" fill="none" stroke="' + green + '" stroke-width="1.8"/>' +
      '<path d="M-57,-49 q-3,6 0,10 M-43,-49 q3,6 0,10 M-56,-34 q6,-5 12,0" fill="none" stroke="' + green + '" stroke-width="1.6"/>';
    var fine = [-46, -40].map(function (y, i) { return line("M-30," + y + " H" + (i ? 18 : 34), green, 1.3, ' opacity="0.7"'); }).join("");
    var tfs = Math.min(18, 124 / Math.max(1, title.length * 0.72));
    var sealIn = o.seal === "war" || o.seal === "med" ? K.moneySeal(o.seal, 54, -34, 8.5) : '<circle cx="54" cy="-34" r="8.5" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="1.6"/>' + K.star(54, -34, 6.5, C.orange);
    var burst = [];
    for (var b = 0; b < 32; b++) { var ar = (Math.PI * b) / 16, rr = b % 2 ? 11.5 : 15; burst.push([54 + rr * Math.cos(ar), -34 + rr * Math.sin(ar)]); }
    var ribbon = o.seal === "med" ? C.med : C.war;
    var seal = '<g class="bond-seal">' + solid([poly([[48, -30], [41, -10], [45, -13], [48, -8], [54, -26]]), poly([[60, -30], [67, -10], [63, -13], [60, -8], [54, -26]])], ribbon, 2.4) +
      solid([poly(burst)], C.yellow, 2.6) + sealIn + "</g>";
    return wrap("bond", o, solid([poly(outer)], WHITE) + band + guilloche + rosette(-78, -106) + rosette(78, -106) + rosette(-78, -10) + rosette(78, -10) +
      '<text x="0" y="-80" text-anchor="middle" font-family="' + SERIF + '" font-weight="900" font-size="' + tfs.toFixed(1) + '" letter-spacing="0.5" fill="' + green + '">' + esc(title.toUpperCase()) + "</text>" +
      line("M-40,-72 H40", C.orange, 1.6) + (value ? text(2, -53, value, 14, green, ' letter-spacing="0.5"') : "") +
      portrait + fine + line("M-30,-21 H16", ink, 1.2) + line("M-26,-25 C-22,-33 -18,-21 -14,-28 C-11,-33 -8,-23 -4,-26 C0,-29 2,-24 7,-27", ink, 1.4) + seal);
  };

  // ── SCROLL ──────────────────────────────────────────────────────────
  // An unrolled scroll standing on its bottom roll: the title o.text, then o.lines (an array of strings) or squiggle
  // handwriting, o.signatures scribbled signatures (default 0), and a red wax seal (o.wax false: none).
  // 130 wide, 168 tall. o: { size, text (default "TREATY"), lines, signatures, wax }.
  // Parts: .scroll-roll-top, .scroll-paper (clipped to the .scroll-reveal rect: unroll it by tweening that rect's
  // height attribute 0 -> 150, from its top at y -158, while .scroll-roll-bottom moves y -150 -> 0, i.e. height - 150).
  K.props.scroll = function (o) {
    o = o || {};
    var title = String(o.text === undefined ? "TREATY" : o.text), cid = id("scr"), rnd = K.rng(hash(title + (o.signatures || 0)));
    var paper = rect(-56, -158, 112, 150);
    var tfs = K.fitText(title, 22, 92, "Oswald", 600, 1.5);
    var body = "", y, i, ns = Math.min(8, o.signatures || 0);
    if (o.lines) {
      o.lines.forEach(function (l, j) { body += text(0, -104 + j * 14, l, K.fitText(l, 11, 92), ink); });
    } else {
      // handwriting: an even up-and-down scrawl with gaps between the words
      var rows = 7 - Math.ceil(ns / 2);
      for (i = 0; i < rows; i++) {
        y = -104 + i * 11;
        var x = i === 0 ? -34 : -42, end = i === rows - 1 ? 6 : 38 + rnd() * 6, d = "M" + P(x, y), up = true;
        while (x < end) {
          x += 2.6 + rnd() * 1.2; up = !up;
          d += " L" + P(x, y + (up ? -2.2 : 1.2) * (0.8 + rnd() * 0.4));
          if (rnd() < 0.09 && x < end - 10) { x += 5; d += " M" + P(x, y); }
        }
        body += line(d, ink, 1.3, ' opacity="0.75"');
      }
    }
    var sigs = "";
    for (i = 0; i < ns; i++) {
      var col = i % 2, row = Math.floor(i / 2), sx = col ? -2 : -44, sy = -36 - (Math.ceil(ns / 2) - 1 - row) * 12, sd = "M" + P(sx, sy);
      for (var j = 0; j < 4; j++) sd += " C" + P(sx + j * 7 + 2, sy - 6 - rnd() * 4) + " " + P(sx + j * 7 + 4, sy + 4) + " " + P(sx + j * 7 + 7, sy - rnd() * 3);
      sigs += line(sd, ink, 1.3) + line("M" + P(sx - 2, sy + 3) + " H" + (sx + 30), ink, 0.9, ' opacity="0.6"');
    }
    var wax = o.wax === false ? "" : solid([poly([[37, -20], [41, -32], [33, -27]]), poly([[47, -20], [43, -32], [51, -27]])], C.rust, 2) +
      solid([poly([[42, -46], [49, -44], [53, -38], [52, -31], [47, -26], [39, -26], [33, -31], [32, -39], [36, -45]])], C.war, 2.6) + K.star(42.5, -36, 6, C.cream);
    var roll = function (yc, cls) {
      var r = [[-62, yc - 8], [62, yc - 8], [66, yc - 4], [66, yc + 4], [62, yc + 8], [-62, yc + 8], [-66, yc + 4], [-66, yc - 4]];
      return '<g class="' + cls + '">' + solid([poly(r)], WHITE) + line("M" + P(-60, yc + 5) + " H60", C.orange, 2) +
        [-1, 1].map(function (s) { return line("M" + P(s * 62, yc - 7) + " L" + P(s * 62, yc + 7) + " M" + P(s * 59, yc - 3) + " L" + P(s * 63.5, yc - 3) + " L" + P(s * 63.5, yc + 3) + " L" + P(s * 59.5, yc + 3), ink, 1.5); }).join("") + "</g>";
    };
    return wrap("scroll", o, '<defs><clipPath id="' + cid + '"><rect class="scroll-reveal" x="-62" y="-158" width="124" height="150"/></clipPath></defs>' +
      '<g class="scroll-paper" clip-path="url(#' + cid + ')">' + solid([poly(paper)], WHITE) + dots(paper, 0.66, 0.2) +
      text(0, -125, title.toUpperCase(), tfs, ink, ' letter-spacing="1.5"') + line("M-38,-118 H38 M-30,-115 H30", C.orange, 1.5) + body + sigs + wax + "</g>" +
      roll(-158, "scroll-roll-top") + roll(-8, "scroll-roll-bottom"));
  };

  // ── THE MANUAL ──────────────────────────────────────────────────────
  // The book "HOW TO END WAR AND DISEASE", closed and standing, its cover to the viewer and its navy spine to the
  // left, as the theme song draws it (an orange cover, a cream condensed title). 98 wide, 124 tall. o: { size }.
  // Parts: .manual-cover (the front cover: swing it open about the spine edge, scaleX 1 -> -1 about (-42, -59);
  // white pages are under it).
  K.props.manual = function (o) {
    o = o || {};
    var cover = rect(-42, -118, 84, 118), spine = [[-42, 0], [-42, -118], [-56, -124], [-56, -6]], topF = [[-42, -118], [42, -118], [28, -124], [-56, -124]];
    var title = [["HOW TO", 19, -93], ["END", 30, -66], ["WAR AND", 19, -44], ["DISEASE", 22, -19]].map(function (t) {
      return '<text x="0" y="' + t[2] + '" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="' + t[1] + '" textLength="64" lengthAdjust="spacingAndGlyphs" fill="' + WHITE + '">' + t[0] + "</text>";
    }).join("");
    return wrap("manual", o, solid([poly(spine)], ink) + line("M-46,-8 L-46,-117", C.orange, 1.6) +
      solid([poly([[-42, -100], [-56, -106], [-56, -101], [-42, -95]]), poly([[-42, -22], [-56, -28], [-56, -23], [-42, -17]])], C.yellow, 2) +
      solid([poly(topF)], WHITE, 3.6) + line("M-38,-120 H34 M-44,-122 H29", ink, 0.9, ' opacity="0.6"') +
      solid([poly(rect(-42, -117, 82, 117))], WHITE) +
      '<g class="manual-cover">' + solid([poly(cover)], C.orange) + dots(cover, 0.7, 0.18) +
      '<path d="' + polyD(rect(-36, -112, 72, 106)) + '" fill="none" stroke="' + WHITE + '" stroke-width="1.4" opacity="0.7"/>' + title +
      line("M-24,-58 H24", WHITE, 1.4, ' opacity="0.8"') + "</g>");
  };

  // ── CLIPBOARD ───────────────────────────────────────────────────────
  // A clipboard with a checklist: o.title (default "CHECKLIST") and o.items, each a string (an empty box) or
  // [text, "tick" | "cross"]. Every empty box holds a hidden tick ready to draw. 104 wide, 160 tall.
  // o: { size, title, items, tickColor (default war red, as Part 1's ticks) }.
  // Parts: .clip-item (one per row, data-i), each with a .clip-tick (a KIT.tick style path with pathLength 1:
  // KIT.drawTick(tl, el, t) draws it on) and, when crossed, a .clip-cross.
  K.props.clipboard = function (o) {
    o = o || {};
    var items = o.items || ["Item one", "Item two", "Item three"], title = o.title === undefined ? "CHECKLIST" : String(o.title), tc = o.tickColor || C.war;
    var board = rect(-52, -150, 104, 150), sheet = rect(-44, -140, 88, 132);
    var step = Math.min(20, (title ? 80 : 104) / Math.max(1, items.length)), y0 = title ? -88 : -114;
    var rows = items.map(function (it, i) {
      var t = Array.isArray(it) ? String(it[0]) : String(it), mark = Array.isArray(it) ? it[1] : null, y = y0 + i * step, fs = Math.min(13, 62 / Math.max(1, t.length * 0.5));
      var bx = -38, by = y - 11;
      var tick = '<path class="clip-tick tick" d="M' + P(bx + 2, by + 6) + " L" + P(bx + 5.5, by + 10) + " L" + P(bx + 14, by - 2) + '" fill="none" stroke="' + tc + '" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="' + (mark === "tick" ? 0 : 1) + '"/>';
      var cross = mark === "cross" ? '<path class="clip-cross" d="M' + P(bx + 2, by + 2) + " L" + P(bx + 9, by + 9) + " M" + P(bx + 9, by + 2) + " L" + P(bx + 2, by + 9) + '" stroke="' + ink + '" stroke-width="2" stroke-linecap="round"/>' : "";
      return '<g class="clip-item" data-i="' + i + '"><rect x="' + bx + '" y="' + by + '" width="11" height="11" fill="' + WHITE + '" stroke="' + ink + '" stroke-width="1.8"/>' +
        text(-22, y - 1, t, fs, ink, "", "start") + cross + tick + "</g>";
    }).join("");
    return wrap("clipboard", o, solid([poly(board)], C.tan) + dots(board, 0.7, 0.25) + line("M48,-146 V-4", C.rust, 1.8) +
      solid([poly(sheet)], WHITE, 3.4) + dots(sheet, 0.72, 0.16) +
      (title ? text(0, -114, title, K.fitText(title, 14, 76, "Oswald", 600, 1), ink, ' letter-spacing="1"') + line("M-30,-109 H30", C.orange, 1.6) : "") + rows +
      line("M-15,-152 L-11,-162 H11 L15,-152", ink, 3.4) + line("M-15,-152 L-11,-162 H11 L15,-152", C.peri, 1.6) +
      solid([poly([[-24, -154], [24, -154], [24, -140], [18, -134], [-18, -134], [-24, -140]])], C.peri) + line("M-20,-150 H20", C.cream, 1.4, ' opacity="0.7"') + line("M20,-151 V-140", ink, 1.2));
  };

  // ── Review sheet samples (node tools/props-sheet.mjs objects-a) ────
  K.props.SHEET.push(
    ["pillBottle", { face: "smile" }, "PILL BOTTLE (smile)"],
    ["pillBottle", { face: "sad", label: "CURE?" }, "PILL BOTTLE (sad, label)"],
    ["pillBottle", {}, "PILL BOTTLE (plain)"],
    ["bomb", {}, "BOMB"],
    ["missile", {}, "MISSILE (grumpy)"],
    ["missile", { mood: "smug", look: "left" }, "MISSILE (smug)"],
    ["missile", { mood: "scared", flame: true }, "MISSILE (scared, flame)"],
    ["bomb", { face: "grin" }, "BOMB (grin)"],
    ["stamp", {}, "STAMP"],
    ["stamp", { pad: true, text: "SUBOPTIMAL" }, "STAMP (on its pad)"],
    ["stampMark", { text: "SUBOPTIMAL" }, "STAMP MARK"],
    ["stampMark", { text: "ELIGIBLE FOR\nOPTIMIZATION", color: "#1F6E68", angle: 6, fontSize: 26 }, "STAMP MARK (2 lines, teal)"],
    ["caseFile", { tab: "EARTH: CASE #847" }, "CASE FILE (Part 1)"],
    ["caseFile", { stamps: 2 }, "CASE FILE (stamps 2)"],
    ["caseFile", { stamps: 3 }, "CASE FILE (stamps 3)"],
    ["priceTag", { anchor: "bottom" }, "PRICE TAG (anchor bottom)"],
    ["priceTag", { text: "$2.4 TRILLION", anchor: "bottom", ink: C.war }, "PRICE TAG (red)"],
    ["sign", { text: "WAR BUILDING", color: C.war }, "SIGN (2 posts)"],
    ["sign", { text: "CLINICAL\nTRIALS", posts: 1, fontSize: 28 }, "SIGN (1 pole, 2 lines)"],
    ["calendar", { month: "MARCH", day: 14 }, "CALENDAR"],
    ["calendar", { month: "DEC", day: 29, pages: 3, color: C.med }, "CALENDAR (3 pages)"],
    ["bond", { text: "Victory Bond" }, "BOND"],
    ["bond", { text: "1% Treaty Bond", value: "$10,000", seal: "med" }, "BOND (med seal)"],
    ["scroll", {}, "SCROLL"],
    ["scroll", { text: "1% Treaty", signatures: 6 }, "SCROLL (signed)"],
    ["manual", {}, "THE MANUAL"],
    ["clipboard", { title: "TO DO", items: [["Build bombs", "tick"], ["Start wars", "tick"], ["Cure diseases", "cross"], "Feed people"] }, "CLIPBOARD"]
  );
})();
