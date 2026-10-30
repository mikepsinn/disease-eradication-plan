// Shared props: the recurring non-human characters with faces (cartoon-style-bible.md section 3): the Democracy
// Dog, the Optimitron, the Calculator, a disease blob, a germ and a 1950s tin robot.
//
// Each K.props.<name>(o) returns SVG markup drawn around (0,0) standing on y 0 (it extends upward). KIT.person is
// about 180 tall with its feet at y 100, so to stand a prop on a person's ground, translate it by +100.
// Drawn like the humans (kit.js HUMANS): polygons with hard (miter) corners, every shape drawn twice (a navy pass
// under the fill), thin navy lines, halftone dots on the light side, orange edges on dark shapes, almond eyes
// with heavy lids and thin angled brows. Colors are KIT.C (plus the humans' eye white).
//
// Moving parts are untransformed <g> groups with a class and data-pivot="x y": the pivot in the prop's own units,
// ready for   gsap.set(el, { svgOrigin: el.getAttribute("data-pivot") });
// Every face has two .eye groups, each with a .pupil (clipped to the eye, so it can look around: tween its x/y by
// a few units), a .brows path and a .mouth group.
(function () {
  var K = window.KIT;
  K.props = K.props || { SHEET: [] };
  if (!K.props.SHEET) K.props.SHEET = [];
  if (K.props.__characters) return;
  K.props.__characters = true;

  var C = K.C, ink = C.line, LW = 4.4, uid = 0;
  var WHITE = "#FBF6E6"; // the humans' eye white (kit.js HUMANS)

  // ── Drawing helpers (copied from kit.js HUMANS) ─────────────────────
  function P(x, y) { return x.toFixed(1) + "," + y.toFixed(1); }
  function polyD(pts) { return "M" + pts.map(function (p) { return P(p[0], p[1]); }).join(" L") + " Z"; }
  function poly(pts) { return 'path d="' + polyD(pts) + '"'; }
  function flipX(pts) { return pts.map(function (p) { return [-p[0], p[1]]; }); }
  function shift(pts, dx, dy) { return pts.map(function (p) { return [p[0] + dx, p[1] + dy]; }); }
  // Shapes drawn twice, a navy pass under the fill, so touching shapes of one color share one outline.
  function solid(tags, col, w) {
    w = w || LW;
    return tags.map(function (t) { return "<" + t + ' fill="' + ink + '" stroke="' + ink + '" stroke-width="' + w + '" stroke-linejoin="miter" stroke-miterlimit="8"/>'; }).join("") +
      tags.map(function (t) { return "<" + t + ' fill="' + col + '"/>'; }).join("");
  }
  function line(d, col, w) { return '<path d="' + d + '" fill="none" stroke="' + (col || ink) + '" stroke-width="' + (w || 2) + '" stroke-linejoin="miter" stroke-linecap="round"/>'; }
  function seg(x, y, a, len) {
    var r1 = (a[0] * Math.PI) / 180, r2 = (a[1] * Math.PI) / 180;
    var ex = x + len * Math.sin(r1), ey = y + len * Math.cos(r1);
    return { x: x, y: y, ex: ex, ey: ey, hx: ex + len * Math.sin(r2), hy: ey + len * Math.cos(r2) };
  }
  function nrm(ax, ay, bx, by) { var dx = bx - ax, dy = by - ay, L = Math.sqrt(dx * dx + dy * dy) || 1; return [-dy / L, dx / L]; }
  // A two-segment limb as one tapered polygon with a mitred (sharp) joint.
  function limbPts(s, w0, w1, w2) {
    var nA = nrm(s.x, s.y, s.ex, s.ey), nB = nrm(s.ex, s.ey, s.hx, s.hy);
    var sx = nA[0] + nB[0], sy = nA[1] + nB[1], q = sx * sx + sy * sy;
    function side(k) {
      var mid = q > 0.6 ? [[s.ex + (k * sx * w1) / q, s.ey + (k * sy * w1) / q]]
        : [[s.ex + (k * nA[0] * w1) / 2, s.ey + (k * nA[1] * w1) / 2], [s.ex + (k * nB[0] * w1) / 2, s.ey + (k * nB[1] * w1) / 2]];
      return [[s.x + (k * nA[0] * w0) / 2, s.y + (k * nA[1] * w0) / 2]].concat(mid, [[s.hx + (k * nB[0] * w2) / 2, s.hy + (k * nB[1] * w2) / 2]]);
    }
    return side(1).concat(side(-1).reverse());
  }
  // Points drawn in a local frame whose +y runs from (x, y) along the direction (dx, dy) (claws, paws, pincers).
  function along(pts, x, y, dx, dy) {
    var L = Math.sqrt(dx * dx + dy * dy) || 1, fx = dx / L, fy = dy / L;
    return pts.map(function (p) { return [x + p[0] * fy + p[1] * fx, y - p[0] * fx + p[1] * fy]; });
  }
  // Print shading: halftone dots over the part of a shape right of x0 (ids are unique on the page).
  function dots(pts, x0, op, step) {
    var id = "kp-chr" + ++uid, st = step || 3.6;
    var xs = pts.map(function (p) { return p[0]; }), ys = pts.map(function (p) { return p[1]; });
    var y0 = Math.min.apply(null, ys) - 2, y1 = Math.max.apply(null, ys) + 2, x1 = Math.max.apply(null, xs) + 2;
    return '<defs><pattern id="' + id + 'd" width="' + st + '" height="' + st + '" patternUnits="userSpaceOnUse"><circle cx="' + st / 2 + '" cy="' + st / 2 + '" r="' + (st * 0.28).toFixed(2) + '" fill="' + ink + '"/></pattern>' +
      '<clipPath id="' + id + 'c"><path d="' + polyD(pts) + '"/></clipPath></defs>' +
      '<rect x="' + x0.toFixed(1) + '" y="' + y0.toFixed(1) + '" width="' + Math.max(0, x1 - x0).toFixed(1) + '" height="' + (y1 - y0).toFixed(1) + '" fill="url(#' + id + 'd)" opacity="' + (op || 0.3) + '" clip-path="url(#' + id + 'c)"/>';
  }
  // A faceted round shape: n corners on an ellipse (bump(i) nudges each corner's radius).
  function ngon(cx, cy, rx, ry, n, rot, bump) {
    var out = [];
    for (var i = 0; i < n; i++) {
      var a = (rot || 0) + (i * 2 * Math.PI) / n, r = bump ? 1 + bump(i, a) : 1;
      out.push([cx + rx * r * Math.cos(a), cy + ry * r * Math.sin(a)]);
    }
    return out;
  }
  function starPts(x, y, r, inner, n, rot) {
    var out = [];
    for (var i = 0; i < n * 2; i++) {
      var a = (rot || -Math.PI / 2) + (i * Math.PI) / n, rr = i % 2 ? r * inner : r;
      out.push([x + rr * Math.cos(a), y + rr * Math.sin(a)]);
    }
    return out;
  }
  // A KIT.C key ("peri") or a hex color, else the default.
  function colorOf(c, def) { return c && C[c] ? C[c] : typeof c === "string" && c.charAt(0) === "#" ? c : def; }
  function isDark(hex) {
    var n = parseInt(hex.slice(1), 16);
    return (0.3 * (n >> 16) + 0.59 * ((n >> 8) & 255) + 0.11 * (n & 255)) / 255 < 0.42;
  }
  function pivot(x, y) { return ' data-pivot="' + x.toFixed(1) + " " + y.toFixed(1) + '"'; }
  function text(x, y, s, size, col, anchor, extra) {
    return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" text-anchor="' + (anchor || "middle") + '" font-family="Oswald" font-weight="600" font-size="' + size.toFixed(1) + '" fill="' + (col || ink) + '"' + (extra || "") + ">" + s + "</text>";
  }

  // ── Faces (the humans' eyes, brows and mouths, seen from the front or in 3/4) ──
  // Eye opening [top, bottom] (times the eye's height), pupil radius, brows [outer, middle, inner] (y, face units).
  var EYE_OPEN = { flat: [1.7, 1.1], calm: [1.15, 0.9], smile: [1.7, 0.45], grin: [1.7, 0.45], smug: [0.65, 0.55], eager: [2.5, 1.6], cross: [1.0, 1.0], worried: [2.1, 1.3], scared: [2.7, 1.8], scream: [3, 2.1], sad: [1.4, 1.1] };
  var PUPIL = { eager: 1.8, worried: 1.6, scared: 1.15, scream: 1.0 };
  var BROW = { flat: [-8.5, -9.2, -8.5], calm: [-8.5, -9.5, -8.5], smile: [-8.5, -11, -9.5], grin: [-9, -12, -10], eager: [-11, -14, -12], cross: [-11.5, -9.5, -6],
    smug: [[-9.5, -9, -6.5], [-12, -14.5, -11.5]], worried: [-7, -9, -12.5], scared: [-8, -11.5, -14.5], scream: [-13, -16.5, -16], sad: [-7, -8.5, -11.5], dizzy: [-10, -11.5, -10], dead: [-10, -11, -10] };
  var EYES3 = [[-2.5, 6.2, 3.7], [10.8, 4.6, 3.4]]; // the humans' 3/4 view: [x, half width, height] of the near and the far eye
  // A face around (cx, cy), the point between the eyes; k scales a person's face (k 1 = a person's eyes).
  // f: { mood, mouth (a mouth kind, default the mood's), turn (3/4 view facing +x, as the humans), look -1..1 and
  //      lookY -1..1 (pupils), sep (eye half-spacing), browShift (moves the brows down), mouthX, mouthY, mouthW,
  //      ink (line color), tongue }.
  // Returns { eyes, brows, mouth, all }; mouth is the inside of the .mouth group (all wraps it).
  function face(cx, cy, k, f) {
    f = f || {};
    var mood = f.mood || "flat", lc = f.ink || ink, sw = Math.sqrt(k), sep = f.sep || 8.5;
    var X = function (x, y) { return P(cx + x * k, cy + y * k); };
    var op = EYE_OPEN[mood] || EYE_OPEN.flat, pr = PUPIL[mood] || 2, lx = (f.look || 0) * 2, ly = (f.lookY || 0) * 1.3;
    var spec = f.turn ? EYES3.map(function (e) { return { x: e[0], rx: e[1], ry: e[2], s: 1 }; })
      : [{ x: -sep, rx: 6.2, ry: 3.7, s: -1 }, { x: sep, rx: 6.2, ry: 3.7, s: 1 }];
    var noPupil = function (x) { return '<circle class="pupil" cx="' + (cx + x * k).toFixed(1) + '" cy="' + cy.toFixed(1) + '" r="0" fill="' + lc + '"/>'; };
    var eyes = spec.map(function (e) {
      var x = e.x, s = e.s, rx = e.rx, ry = e.ry;
      if (mood === "dizzy") {
        var sp = [];
        for (var t = 0; t <= 4.2 * Math.PI; t += 0.3) { var r = (0.4 + t * 0.4) * (rx / 6.2); sp.push(X(x + s * r * Math.cos(t), r * Math.sin(t) * 0.9)); }
        return '<g class="eye">' + line("M" + sp.join(" L"), lc, 1.7 * sw) + noPupil(x) + "</g>";
      }
      if (mood === "dead") {
        var d = rx * 0.7;
        return '<g class="eye">' + line("M" + X(x - d, -d * 0.75) + " L" + X(x + d, d * 0.75) + " M" + X(x - d, d * 0.75) + " L" + X(x + d, -d * 0.75), lc, 2.4 * sw) + noPupil(x) + "</g>";
      }
      var a = X(x - s * rx, 0.3), b = X(x + s * rx, -0.6), top = X(x, -ry * op[0]), bot = X(x, ry * op[1]);
      var almond = "M" + a + " Q" + top + " " + b + " Q" + bot + " " + a + " Z", id = "kp-chr-eye" + ++uid;
      var lid = "M" + X(x - s * (rx + 0.8), 0.7) + " Q" + X(x, -ry * op[0] - 0.6) + " " + X(x + s * (rx + 0.6), -1);
      return '<g class="eye"><defs><clipPath id="' + id + '"><path d="' + almond + '"/></clipPath></defs>' +
        '<path d="' + almond + '" fill="' + WHITE + '" stroke="' + lc + '" stroke-width="' + sw.toFixed(2) + '"/>' +
        '<g clip-path="url(#' + id + ')"><circle class="pupil" cx="' + (cx + (x + lx * (rx / 6.2)) * k).toFixed(1) + '" cy="' + (cy + (ly - 0.3) * k).toFixed(1) + '" r="' + (pr * k).toFixed(1) + '" fill="' + lc + '"/></g>' +
        '<path d="' + lid + '" fill="none" stroke="' + lc + '" stroke-width="' + (1.9 * sw).toFixed(2) + '" stroke-linecap="round"/></g>';
    }).join("");
    var bs = BROW[mood] || BROW.flat, pair = Array.isArray(bs[0]) ? bs : [bs, bs], bsh = f.browShift || 0;
    var browD = spec.map(function (e, i) {
      var w = e.rx + 0.8, bb = pair[i].map(function (v) { return v + bsh; }), x = e.x;
      if (f.turn) { var L = i ? [bb[2], bb[1], bb[0]] : bb; return "M" + X(x - w, L[0]) + " L" + X(x - w * 0.1, L[1]) + " L" + X(x + w, L[2]); }
      return "M" + X(x + e.s * w, bb[0]) + " L" + X(x + e.s * w * 0.1, bb[1]) + " L" + X(x - e.s * w, bb[2]);
    }).join(" ");
    var brows = '<path class="brows" d="' + browD + '" fill="none" stroke="' + lc + '" stroke-width="' + (2.6 * sw).toFixed(2) + '" stroke-linejoin="miter" stroke-linecap="round"/>';
    var mouth = mouthMarkup(f.mouth || mood, cx, cy, k, f, lc, sw);
    return { eyes: eyes, brows: brows, mouth: mouth, all: eyes + brows + '<g class="mouth">' + mouth + "</g>" };
  }
  function mouthMarkup(kind, cx, cy, k, f, lc, sw) {
    var mx = f.mouthX || 0, my = f.mouthY === undefined ? 11 : f.mouthY, mw = f.mouthW || 1, tongue = f.tongue || C.war;
    var M = function (x, y) { return P(cx + (mx + x * mw) * k, cy + (my + y) * k); };
    var fw = (1.8 * sw).toFixed(2), lw = (2.2 * sw).toFixed(2);
    var path = function (d, fill, w) { return '<path d="' + d + '" fill="' + (fill || "none") + '" stroke="' + lc + '" stroke-width="' + (w || lw) + '" stroke-linecap="round" stroke-linejoin="miter"/>'; };
    var crease = function (s) { return line("M" + M(s * 10.5, -3.5) + " Q" + M(s * 12.2, -0.5) + " " + M(s * 10.2, 2), lc, 1.5 * sw); };
    var lolling = function (x0) { return path("M" + M(x0, 1.5) + " L" + M(x0 + 5, 1) + " L" + M(x0 + 5.5, 7) + " L" + M(x0 + 2.8, 9.5) + " L" + M(x0 + 0.6, 7) + " Z", tongue, fw); };
    // a dark crescent with a row of pointed teeth along its top (menace)
    var fangs = function (rise) {
      var y0 = -3, yc = 1.5, y1 = -3 - rise, top = function (x) { var t = (x + 12) / 24, u = 1 - t; return u * u * y0 + 2 * u * t * yc + t * t * y1; };
      var teeth = "M" + M(-10.5, top(-10.5));
      for (var x = -10.5; x < 10.4; x += 3.5) teeth += " L" + M(x + 1.75, top(x + 1.75) + 3.2) + " L" + M(x + 3.5, top(x + 3.5));
      return path("M" + M(-12, y0) + " Q" + M(0, yc) + " " + M(12, y1) + " Q" + M(2, 11) + " " + M(-12, y0) + " Z", lc, fw) +
        path(teeth + " Z", WHITE, (1 * sw).toFixed(2)) + crease(1);
    };
    var m = {
      smile: function () { return path("M" + M(-9, -1) + " Q" + M(0, 2) + " " + M(9, -1) + " Q" + M(0, 10) + " " + M(-9, -1) + " Z", WHITE, fw) + crease(-1) + crease(1); },
      grin: function () {
        return path("M" + M(-11, -2) + " L" + M(11, -2) + " L" + M(7.5, 7) + " L" + M(-7.5, 7) + " Z", WHITE, fw) +
          line("M" + M(-4, -2) + " L" + M(-3, 7) + " M" + M(0, -2) + " L" + M(0, 7) + " M" + M(4, -2) + " L" + M(3, 7) + " M" + M(-9.4, 2.5) + " L" + M(9.4, 2.5), lc, 1.1 * sw) + crease(-1) + crease(1);
      },
      smug: function () { return path("M" + M(-8, 2) + " Q" + M(1, 4) + " " + M(10, -3)) + crease(1); },
      fangs: function () { return fangs(1.5); },
      bigfangs: function () { return fangs(0); },
      eager: function () { return path("M" + M(-6, -1) + " L" + M(6, -1) + " L" + M(4, 7) + " L" + M(-4, 7) + " Z", lc, fw) + path("M" + M(-3, 7) + " L" + M(3, 7) + " L" + M(2.2, 4.2) + " L" + M(-2.2, 4.2) + " Z", tongue, (1 * sw).toFixed(2)); },
      calm: function () { return path("M" + M(-6, 0) + " Q" + M(0, 3.5) + " " + M(6, 0)); },
      flat: function () { return path("M" + M(-6, 1) + " L" + M(6, 1)); },
      cross: function () {
        return path("M" + M(-8, -1) + " L" + M(8, -1) + " L" + M(7, 5) + " L" + M(-7, 5) + " Z", WHITE, fw) +
          line("M" + M(-3.5, -1) + " L" + M(-3.5, 5) + " M" + M(0, -1) + " L" + M(0, 5) + " M" + M(3.5, -1) + " L" + M(3.5, 5) + " M" + M(-7.5, 2) + " L" + M(7.5, 2), lc, 1 * sw);
      },
      worried: function () { return path("M" + M(-8, 1) + " L" + M(-4, -1) + " L" + M(0, 1) + " L" + M(4, -1) + " L" + M(8, 1)); },
      scared: function () { return path("M" + M(-6, -1) + " L" + M(6, -1) + " L" + M(4.5, 6) + " L" + M(-4.5, 6) + " Z", lc, fw) + path("M" + M(-5.6, -1) + " L" + M(5.6, -1) + " L" + M(5.3, 1) + " L" + M(-5.3, 1) + " Z", WHITE, (0.8 * sw).toFixed(2)); },
      sad: function () { return path("M" + M(-7, 3) + " Q" + M(0, -2) + " " + M(7, 3)); },
      scream: function () {
        return path("M" + M(-8, -3) + " L" + M(8, -3) + " L" + M(5.5, 15) + " L" + M(-5.5, 15) + " Z", lc, fw) +
          path("M" + M(-7.6, -3) + " L" + M(7.6, -3) + " L" + M(7.3, -0.6) + " L" + M(-7.3, -0.6) + " Z", WHITE, (0.9 * sw).toFixed(2)) +
          path("M" + M(-4.6, 14.6) + " L" + M(4.6, 14.6) + " L" + M(3.6, 10) + " L" + M(0, 8.6) + " L" + M(-3.6, 10) + " Z", tongue, (0.9 * sw).toFixed(2));
      },
      dizzy: function () { return path("M" + M(-7, 0) + " Q" + M(0, 4) + " " + M(7, 0)) + lolling(0.5); },
      dead: function () { return path("M" + M(-6, 1) + " L" + M(6, 1)) + lolling(-1); },
      // the robot's speaker grille
      grille: function () {
        return path("M" + M(-8, -2.5) + " L" + M(8, -2.5) + " L" + M(8, 4.5) + " L" + M(-8, 4.5) + " Z", C.slate, fw) +
          line("M" + M(-4.5, -1) + " L" + M(-4.5, 3) + " M" + M(-1.5, -1) + " L" + M(-1.5, 3) + " M" + M(1.5, -1) + " L" + M(1.5, 3) + " M" + M(4.5, -1) + " L" + M(4.5, 3), C.cream, 1.2 * sw);
      },
    };
    return (m[kind] || m.flat)();
  }

  // ── The Democracy Dog ─────────────────────────────────────────────
  // A round dog chasing its own tail (style bible section 3). Its head is Part 1 pentagon's dog head (tan fur, rust
  // floppy ears, a rust patch over one eye, a cream muzzle, a black nose), with the humans' almond eyes. It faces
  // left, its head turned back, snapping at a tail that curls over its back just out of reach. About 150 wide and
  // 145 tall (to the top of the tail): knee high next to a person.
  // o: { tail "papers" (green bills; o.seal "plain" | "war" | "med") | "pills" (teal capsules) | "plain" (fur),
  //      face "tail" (3/4, looking back at the tail) | "front" (at the camera, as in pentagon),
  //      mood "eager" (snapping, default) | "smile" | "cross" (growling) | "dizzy" (after the spin) }
  // Parts (data-pivot): .dog-head (the neck, -26,-72), .dog-ear-l (and .dog-ear-r in the front view; where each ear
  // hangs: flap them), .dog-tail
  // (the root, 46,-64: wag it), .dog-legs (6,-22) holding four .dog-leg (each at its hip: scramble them), .eye, .pupil,
  // .brows, .mouth. Spin the whole dog around the body's center (6,-50) to run in circles.
  var DOG = { body: [6, -50], neck: [-26, -72], tail: [46, -64], head: [-30, -98] };
  function dogTail(kind, seal) {
    var R = [46, -64], Q = [108, -150], E = [20, -134];
    var at = function (t) { var u = 1 - t; return [u * u * R[0] + 2 * u * t * Q[0] + t * t * E[0], u * u * R[1] + 2 * u * t * Q[1] + t * t * E[1]]; };
    var ang = function (t) { var u = 1 - t; return (Math.atan2(2 * u * (Q[1] - R[1]) + 2 * t * (E[1] - Q[1]), 2 * u * (Q[0] - R[0]) + 2 * t * (E[0] - Q[0])) * 180) / Math.PI; };
    var out = "";
    if (kind === "plain") {
      var L = [], Rr = [];
      for (var i = 0; i <= 8; i++) {
        var t = i / 8, p = at(t), a = (ang(t) * Math.PI) / 180, w = 7 * (1 - t) + 1.2;
        L.push([p[0] - Math.sin(a) * w, p[1] + Math.cos(a) * w]); Rr.push([p[0] + Math.sin(a) * w, p[1] - Math.cos(a) * w]);
      }
      var tip = at(1.06);
      out = solid([poly(L.concat([tip], Rr.reverse()))], C.tan);
    } else {
      // a fur stub at the root, then five bills (or pills) along the curl, smaller toward the tip
      out = solid([poly([[34, -60], [44, -74], [58, -80], [56, -64], [44, -54]])], C.tan);
      [0.1, 0.3, 0.5, 0.7, 0.9].forEach(function (t, i) {
        var p = at(t), s = 1 - i * 0.07;
        var g = '<g transform="translate(' + P(p[0], p[1]) + ") rotate(" + ang(t).toFixed(1) + ") scale(" + s.toFixed(2) + ')">';
        if (kind === "pills") {
          g += '<rect x="-14" y="-6" width="28" height="12" rx="6" fill="' + ink + '" stroke="' + ink + '" stroke-width="4"/>' +
            '<path d="M0,-6 H-8 A6,6 0 0 0 -8,6 H0 Z" fill="' + C.med + '"/><path d="M0,-6 H8 A6,6 0 0 1 8,6 H0 Z" fill="' + WHITE + '"/>' +
            line("M0,-6 V6", ink, 1.6) + line("M-9,-3 H-4", C.cream, 1.6);
        } else {
          g += solid([poly([[-16, -9], [16, -9], [16, 9], [-16, 9]])], C.money, 3.2) +
            '<rect x="-12.5" y="-5.5" width="25" height="11" fill="none" stroke="' + C.moneyDark + '" stroke-width="1.2"/>' +
            '<ellipse cx="-1" cy="0" rx="4" ry="4.6" fill="' + C.paper + '" stroke="' + C.moneyDark + '" stroke-width="1.1"/>' +
            (seal === "war" || seal === "med" ? K.moneySeal(seal, 9, 0, 3.6) : '<circle cx="9" cy="0" r="2.4" fill="none" stroke="' + C.moneyDark + '" stroke-width="1.1"/>');
        }
        out += g + "</g>";
      });
    }
    return '<g class="dog-tail"' + pivot(R[0], R[1]) + ">" + out + "</g>";
  }
  function democracyDog(o) {
    o = o || {};
    var mood = o.mood || "eager", front = o.face === "front", HX = DOG.head[0], HY = DOG.head[1];
    var H = function (pts) { return shift(pts, HX, HY); };
    // legs: front pair reaching forward (left), back pair pushing back, the far ones in the rust shade
    var legs = [[-28, [-22, 8], C.tan], [-12, [-30, 4], C.rust], [24, [26, -4], C.rust], [38, [18, -8], C.tan]];
    var legSvg = legs.map(function (L, i) {
      var s = seg(L[0], -24, L[1], 12.6), paw = [[s.hx + 4, -4], [s.hx - 6, -4.5], [s.hx - 11, 0], [s.hx + 5, 0]];
      return '<g class="dog-leg"' + pivot(L[0], -24) + ">" + solid([poly(limbPts(s, 13, 11, 9)), poly(paw)], L[2], 3.6) + "</g>";
    });
    // far legs first (behind), then the body, the near legs' paws stay under it
    var bodyPts = ngon(DOG.body[0], DOG.body[1], 50, 42, 13, -Math.PI / 2, function (i) { return [0, 0.03, -0.02, 0.04, 0, -0.03, 0.02, 0.03, -0.02, 0, 0.03, -0.03, 0.02][i]; });
    var body = solid([poly(bodyPts)], C.tan) + dots(bodyPts, 20, 0.26) +
      solid([poly(ngon(18, -42, 13, 10, 7, 0.4))], C.rust, 2.4);
    // the collar: a war-red band with a mustard star tag, where the head meets the body
    var collar = solid([poly([[-52, -78], [-14, -92], [-8, -82], [-46, -68]])], C.war, 3) +
      solid([poly(starPts(-30, -70, 7.5, 0.45, 5))], C.yellow, 2.4);
    var head;
    if (!front) {
      var faceF = face(HX, HY - 4, 1.55, { turn: true, mood: mood, look: 1, lookY: mood === "eager" ? -0.7 : 0 });
      var nearEar = H([[-14, -22], [-27, -26], [-39, -12], [-43, 10], [-35, 21], [-27, 7], [-22, -8]]);
      var muzzle = H([[-1, 5], [10, -3], [30, -6], [42, -1], [45, 9], [37, 19], [16, 22], [4, 17]]);
      var nose = H([[37, -6], [47, -5], [48, 1], [43, 4], [38, 2]]);
      var mouth = {
        eager: solid([poly(H([[14, 13], [43, 9], [38, 26], [19, 25]]))], ink, 2) + solid([poly(H([[22, 20], [32, 19], [33, 31], [27, 35], [22, 29]]))], C.war, 2.2),
        smile: line("M" + P(HX + 16, HY + 13) + " Q" + P(HX + 28, HY + 19) + " " + P(HX + 41, HY + 9), ink, 2.6) + solid([poly(H([[24, 16], [31, 15], [32, 23], [27, 26], [24, 21]]))], C.war, 2.2),
        cross: solid([poly(H([[14, 12], [43, 9], [40, 19], [17, 20]]))], ink, 2) + solid([poly(H([[17, 12], [21, 16], [25, 11.5], [29, 15.5], [33, 11], [37, 14.5], [41, 10]]))], WHITE, 1.4) + line("M" + P(HX + 30, HY - 4) + " l4,4 M" + P(HX + 25, HY - 3) + " l3,4", ink, 1.6),
        dizzy: line("M" + P(HX + 16, HY + 13) + " Q" + P(HX + 28, HY + 18) + " " + P(HX + 41, HY + 9), ink, 2.6) + solid([poly(H([[23, 16], [31, 15], [33, 30], [27, 35], [23, 27]]))], C.war, 2.2),
      }[mood] || "";
      head = solid([poly(ngon(HX, HY, 30, 27, 10, -0.2))], C.tan) + dots(ngon(HX, HY, 30, 27, 10, -0.2), HX + 6, 0.22) +
        solid([poly(H([[6, -18], [19, -23], [30, -15], [29, -1], [17, 1], [9, -6]]))], C.rust, 2) +
        solid([poly(muzzle)], C.cream, 3.6) + '<g class="mouth">' + mouth + "</g>" + solid([poly(nose)], ink, 2) +
        faceF.eyes + faceF.brows +
        '<g class="dog-ear-l"' + pivot(HX - 20, HY - 24) + ">" + solid([poly(nearEar)], C.rust, 3.6) + "</g>";
    } else {
      var ff = face(HX, HY - 8, 1.45, { mood: mood, sep: 10, mouth: "none" });
      var ear = function (k) { return H([[22 * k, -22], [36 * k, -26], [46 * k, -10], [48 * k, 14], [40 * k, 24], [32 * k, 8], [27 * k, -6]]); };
      var muzzleF = H([[-20, 6], [-10, 0], [10, 0], [20, 6], [22, 16], [12, 25], [-12, 25], [-22, 16]]);
      var mouthF = {
        eager: solid([poly(H([[-10, 17], [10, 17], [7, 29], [-7, 29]]))], ink, 2) + solid([poly(H([[-5, 23], [5, 23], [5, 33], [0, 36], [-5, 33]]))], C.war, 2.2),
        smile: line("M" + P(HX - 11, HY + 16) + " Q" + P(HX - 5.5, HY + 22) + " " + P(HX, HY + 16) + " Q" + P(HX + 5.5, HY + 22) + " " + P(HX + 11, HY + 16), ink, 2.6) + solid([poly(H([[-4, 20], [4, 20], [4, 29], [0, 31], [-4, 29]]))], C.war, 2),
        cross: solid([poly(H([[-12, 16], [12, 16], [10, 24], [-10, 24]]))], ink, 2) + solid([poly(H([[-10, 16.5], [-7, 20], [-4, 16.5], [-1, 20], [2, 16.5], [5, 20], [8, 16.5], [10, 16.5], [10, 18], [-10, 18]]))], WHITE, 1.2),
        dizzy: line("M" + P(HX - 11, HY + 16) + " Q" + P(HX - 5.5, HY + 22) + " " + P(HX, HY + 16) + " Q" + P(HX + 5.5, HY + 22) + " " + P(HX + 11, HY + 16), ink, 2.6) + solid([poly(H([[1, 19], [9, 19], [10, 33], [5, 36], [1, 30]]))], C.war, 2),
      }[mood] || "";
      head = solid([poly(ngon(HX, HY, 30, 27, 10, -0.15))], C.tan) + dots(ngon(HX, HY, 30, 27, 10, -0.15), HX + 8, 0.22) +
        solid([poly(H([[4, -26], [20, -30], [30, -18], [28, -4], [16, -2], [6, -10]]))], C.rust, 2) +
        solid([poly(muzzleF)], C.cream, 3.6) + '<g class="mouth">' + mouthF + "</g>" + solid([poly(H([[-8, 4], [8, 4], [6, 10], [0, 12], [-6, 10]]))], ink, 2) +
        ff.eyes + ff.brows +
        '<g class="dog-ear-l"' + pivot(HX - 28, HY - 22) + ">" + solid([poly(ear(-1))], C.rust, 3.6) + "</g>" +
        '<g class="dog-ear-r"' + pivot(HX + 28, HY - 22) + ">" + solid([poly(ear(1))], C.rust, 3.6) + "</g>";
    }
    return '<g class="democracy-dog">' +
      '<g class="dog-legs"' + pivot(6, -22) + ">" + legSvg[1] + legSvg[2] + legSvg[0] + legSvg[3] + "</g>" +
      body + dogTail(o.tail || "papers", o.seal || "plain") + collar +
      '<g class="dog-head"' + pivot(DOG.neck[0], DOG.neck[1]) + ">" + head + "</g></g>";
  }

  // ── The Optimitron ────────────────────────────────────────────────
  // A 1970s countertop toaster-microwave hybrid (style bible section 3): a harvest-orange box with a lit mustard
  // microwave window (its face), a chrome control panel with two big dials, HEALTH and WEALTH, a faux-wood band with
  // its name plate, and a toaster slot on top that pops out policy cards like toast. About 240 wide and 190 tall
  // (plus the card): chest high next to a person.
  // o: { mood (any face mood, default "smile"), health and wealth (dial angles in degrees, 0 = straight up,
  //      -135..135; defaults 30 and -30), card (the card's title, default "POLICY"), pop (how far the card stands
  //      out of the slot: default 62, 0 = down in the slot) }
  // Parts (data-pivot): .opt-dial-health (64,-121) and .opt-dial-wealth (64,-63): turn them; .opt-card (the slot,
  // 7,-178): tween its y by -pop to pop it, +pop to drop it (it is clipped at the slot); .opt-lever (the side
  // lever's hinge on its track, 120,-108); .eye, .pupil, .brows, .mouth.
  function optimitron(o) {
    o = o || {};
    var mood = o.mood || "smile", pop = o.pop === undefined ? 62 : o.pop, title = o.card || "POLICY";
    var FT = -170, FB = -14, FL = -112, FR = 112, DX = 16, DY = -16;
    var front = [[FL, FT], [FR, FT], [FR, FB], [FL, FB]];
    var top = [[FL, FT], [FL + DX, FT + DY], [FR + DX, FT + DY], [FR, FT]];
    var side = [[FR, FT], [FR + DX, FT + DY], [FR + DX, FB + DY], [FR, FB]];
    var feet = [[-98, FB], [-70, FB], [-66, 0], [-102, 0]];
    var slot = [[-44 + DX * 0.32, FT + DY * 0.32], [52 + DX * 0.32, FT + DY * 0.32], [52 + DX * 0.68, FT + DY * 0.68], [-44 + DX * 0.68, FT + DY * 0.68]];
    var slotY = FT + DY * 0.5, cx = 4 + DX * 0.5, cid = "kp-chr-slot" + ++uid;
    var ct = slotY - 6 - pop, cl = cx - 36, cr = cx + 36, size = K.fitText(title, 13, 62, "Oswald", 600, 1);
    var card = solid([poly([[cl, ct], [cr, ct], [cr, ct + 96], [cl, ct + 96]])], C.cream, 3.2) + dots([[cl, ct], [cr, ct], [cr, ct + 96], [cl, ct + 96]], cx + 14, 0.18) +
      text(cx, ct + 17, title, size, ink, "middle", ' letter-spacing="1"') + line("M" + P(cl + 7, ct + 23) + " H" + (cr - 7).toFixed(1), C.orange, 2.4) +
      line("M" + P(cl + 8, ct + 32) + " H" + (cr - 8).toFixed(1) + " M" + P(cl + 8, ct + 40) + " H" + (cr - 14).toFixed(1) + " M" + P(cl + 8, ct + 48) + " H" + (cr - 22).toFixed(1), ink, 1.4) +
      line("M" + P(cr - 22, ct + 54) + " l5,5 l10,-12", C.med, 3.4);
    // the window (a lit interior) with the face, and its chrome frame and handle
    var door = [[FL + 8, FT + 8], [14, FT + 8], [14, FB - 24], [FL + 8, FB - 24]];
    var win = [[FL + 16, FT + 16], [4, FT + 16], [4, FB - 32], [FL + 16, FB - 32]];
    var wcx = (FL + 16 + 4) / 2, f = face(wcx, -112, 2.5, { mood: mood, sep: 8.6 });
    var shine = [[FL + 20, FT + 50], [FL + 46, FT + 20], [FL + 56, FT + 20], [FL + 30, FT + 50]];
    // the control panel: two big dials with tick scales and labels
    var panel = [[24, FT + 8], [FR - 8, FT + 8], [FR - 8, FB - 24], [24, FB - 24]];
    function dial(cls, label, x, y, deg) {
      var ticks = "", pts = [], a = (deg * Math.PI) / 180;
      for (var i = 0; i < 7; i++) {
        var t = ((-135 + 45 * i) * Math.PI) / 180;
        ticks += "M" + P(x + 19.5 * Math.sin(t), y - 19.5 * Math.cos(t)) + " L" + P(x + 23.5 * Math.sin(t), y - 23.5 * Math.cos(t)) + " ";
      }
      for (var j = 0; j < 36; j++) { var b = (j * Math.PI) / 18, r = j % 2 ? 15.4 : 17; pts.push([x + r * Math.sin(b), y - r * Math.cos(b)]); }
      var ptr = [[x + 16 * Math.sin(a), y - 16 * Math.cos(a)], [x + 3.4 * Math.cos(a) - 2 * Math.sin(a), y + 3.4 * Math.sin(a) + 2 * Math.cos(a)], [x - 3.4 * Math.cos(a) - 2 * Math.sin(a), y - 3.4 * Math.sin(a) + 2 * Math.cos(a)]];
      return line(ticks, ink, 1.8) + text(x, y - 27.5, label, 11.5, ink, "middle", ' letter-spacing="1.4"') +
        '<g class="' + cls + '"' + pivot(x, y) + ">" + solid([poly(pts)], C.slate, 2.6) + '<circle cx="' + x + '" cy="' + y + '" r="10" fill="' + C.peri + '" stroke="' + ink + '" stroke-width="2"/>' +
        solid([poly(ptr)], C.cream, 1.8) + '<circle cx="' + x + '" cy="' + y + '" r="1.8" fill="' + ink + '"/></g>';
    }
    var wood = [[FL, FB - 18], [FR, FB - 18], [FR, FB], [FL, FB]];
    var grain = "M" + P(FL + 4, FB - 13) + " L" + P(-60, FB - 14) + " L" + P(-40, FB - 11) + " M" + P(10, FB - 6) + " L" + P(40, FB - 8) + " L" + P(70, FB - 5) + " L" + P(FR - 4, FB - 7) + " M" + P(30, FB - 13) + " L" + P(60, FB - 12);
    var lever = [[FR + 17, -113], [FR + 33, -113], [FR + 35, -104], [FR + 17, -104]];
    return '<g class="optimitron">' +
      solid([poly(feet), poly(flipX(feet))], C.slate, 3.4) +
      solid([poly(side)], C.rust) + line("M" + P(FR + 8, -120) + " V" + (-92).toFixed(1), ink, 2.6) +
      solid([poly(top)], C.yellow) + dots(top, 40, 0.22) + solid([poly(slot)], ink, 2) +
      '<defs><clipPath id="' + cid + '"><rect x="-200" y="' + (slotY - 400).toFixed(1) + '" width="400" height="400"/></clipPath></defs>' +
      '<g clip-path="url(#' + cid + ')"><g class="opt-card"' + pivot(cx, slotY) + ">" + card + "</g></g>" +
      line("M" + P(slot[0][0], slot[0][1]) + " L" + P(slot[1][0], slot[1][1]), ink, 2.4) +
      solid([poly(front)], C.orange) + line("M" + P(FR - 3, FT + 4) + " V" + (FB - 22).toFixed(1), C.cream, 2) +
      solid([poly(door)], C.peri, 3.6) + solid([poly(win)], C.yellow, 3.6) + dots(win, FL + 10, 0.16) +
      '<path d="' + polyD(shine) + '" fill="' + C.cream + '" opacity="0.55"/>' +
      '<path d="' + polyD(shift(shine, 16, 0).map(function (p, i) { return i === 0 || i === 3 ? [p[0] - 6, p[1]] : p; })) + '" fill="' + C.cream + '" opacity="0.4"/>' +
      f.all + solid([poly([[6, FT + 26], [11, FT + 26], [11, FB - 42], [6, FB - 42]])], C.cream, 2.4) +
      solid([poly(panel)], C.cream, 3.6) + dots(panel, 76, 0.18) +
      dial("opt-dial-health", "HEALTH", 64, -121, o.health === undefined ? 30 : o.health) +
      dial("opt-dial-wealth", "WEALTH", 64, -63, o.wealth === undefined ? -30 : o.wealth) +
      solid([poly(wood)], C.rust, 3.6) + line(grain, C.tan, 1.4) +
      solid([poly([[-86, FB - 15.5], [-6, FB - 15.5], [-6, FB - 2.5], [-86, FB - 2.5]])], C.cream, 2) + text(-46, FB - 5.5, "OPTIMITRON", 10, ink, "middle", ' letter-spacing="1.6"') +
      '<g class="opt-lever"' + pivot(FR + 8, -108) + ">" + line("M" + P(FR + 8, -108.5) + " H" + (FR + 18).toFixed(1), ink, 3.4) + solid([poly(lever)], C.cream, 2.6) + "</g></g>";
  }

  // ── The Calculator ────────────────────────────────────────────────
  // A tan 1970s desk calculator with eyes (style bible section 3: it shows "ERROR", screams and walks off the desk):
  // a display on top, a face, a keypad, and two stick legs in pointed shoes. About 110 wide and 155 tall: a big desk
  // machine (scale it to 0.5 to sit on a desk).
  // o: { display (text; default "0", or "ERROR" when screaming), mood "calm" (default) | "scream" | any face mood,
  //      legs (false: rubber feet and no legs, 16 lower) }
  // Parts (data-pivot): .calc-display (its center, 0,-129: flicker it), .calc-mouth (the mouth's center: scale it
  // open), .calc-leg-l (-18,-22) and .calc-leg-r (18,-22): walk them; .calc-shake (scream only: the shake lines and
  // a sweat drop); .eye, .pupil, .brows.
  function calculator(o) {
    o = o || {};
    var mood = o.mood || "calm", scream = mood === "scream", legs = o.legs !== false;
    var B = legs ? -22 : -6, T = B - 124, L = -50, R = 50, DX = 8, DY = -10;
    var shown = String(o.display === undefined ? (scream ? "ERROR" : "0") : o.display);
    var front = [[L, T], [R, T], [R, B], [L, B]], top = [[L, T], [L + DX, T + DY], [R + DX, T + DY], [R, T]], side = [[R, T], [R + DX, T + DY], [R + DX, B + DY], [R, B]];
    var disp = [[L + 7, T + 6], [R - 7, T + 6], [R - 7, T + 29], [L + 7, T + 29]], size = K.fitText(shown, 20, 74, "Oswald", 600, 1.5);
    var ey = T + 50, my = scream ? 8 : 11;
    var f = face(0, ey, 1.45, { mood: scream ? "scared" : mood, mouth: scream ? "scream" : undefined, browShift: scream ? 3.5 : 0, sep: 10, mouthY: my });
    var keys = "";
    for (var r = 0; r < 3; r++) for (var c = 0; c < 4; c++) {
      var kx = L + 6.5 + c * 23, ky = T + 88 + r * 10, op = c === 3, eq = op && r === 2;
      keys += solid([poly([[kx, ky], [kx + 18, ky], [kx + 18, ky + 7], [kx, ky + 7]])], eq ? C.orange : op ? C.rust : C.cream, 2);
    }
    var legSvg;
    if (legs) {
      legSvg = [-1, 1].map(function (s) {
        var hx = s * 18, fx = hx + s * 2, shoe = [[fx - 7, -5], [fx + 4, -6], [fx + 15, -1], [fx + 14, 0], [fx - 7, 0]];
        return '<g class="calc-leg-' + (s < 0 ? "l" : "r") + '"' + pivot(hx, B) + ">" + line("M" + P(hx, B) + " L" + P(hx + s, -11) + " L" + P(fx, -4), ink, 4.5) + solid([poly(shoe)], ink, 2) + "</g>";
      }).join("");
    } else {
      legSvg = solid([poly([[L + 6, B], [L + 22, B], [L + 20, 0], [L + 8, 0]]), poly([[R - 22, B], [R - 6, B], [R - 8, 0], [R - 20, 0]])], C.slate, 2.4);
    }
    var shake = scream ? '<g class="calc-shake">' + line("M" + P(L - 10, T + 22) + " l-8,4 l8,4 l-8,4 M" + P(L - 12, T + 62) + " l-10,3 l10,3 l-10,3 M" + P(R + DX + 10, T + 18) + " l8,4 l-8,4 l8,4 M" + P(R + DX + 12, T + 60) + " l10,3 l-10,3 l10,3", ink, 2.4) +
      solid([poly([[R + 20, T - 22], [R + 26, T - 12], [R + 24, T - 6], [R + 17, T - 6], [R + 15, T - 12]])], C.cyan, 1.8) + "</g>" : "";
    return '<g class="calculator">' + legSvg +
      solid([poly(side)], C.rust) + solid([poly(top)], C.yellow) + solid([poly(front)], C.tan) + dots(front, 18, 0.24) + line("M" + P(R - 3, T + 4) + " V" + (B - 4).toFixed(1), C.orange, 1.8) +
      '<g class="calc-display"' + pivot(0, T + 17.5) + ">" + solid([poly(disp)], C.navy, 3.6) +
      text(R - 12, T + 25, shown, size, scream ? C.orange : C.cyan, "end", ' letter-spacing="1.5"') + "</g>" +
      f.eyes + f.brows + '<g class="calc-mouth mouth"' + pivot(0, ey + (my + (scream ? 6 : 1)) * 1.45) + ">" + f.mouth + "</g>" + keys + shake + "</g>";
  }

  // ── A disease ─────────────────────────────────────────────────────
  // A lumpy, smug, menacing blob with spots, its claw tips pressed together like a villain. About 175 wide and 150
  // tall: a person's chest high, so it can loom over a hospital bed. Each seed gives a different lump.
  // o: { color (a KIT.C key or hex; default "peri"), mood "smug" (default) | "grin" | "cross" | "scared" | "dead",
  //      seed, label (a pageant sash: "CANCER"), arms "steeple" (default) | "up" (claws raised, pouncing) | "limp"
  //      (sprawled on the floor, the default when dead) | "none" }
  // Parts (data-pivot): .blob-body (the middle of its base, 0,0: squash and stretch it; the face rides along),
  // .blob-arm-l (-60,-52) and .blob-arm-r (60,-52); .eye, .pupil, .brows, .mouth.
  function diseaseBlob(o) {
    o = o || {};
    var col = colorOf(o.color, C.peri), mood = o.mood || "smug", seed = o.seed === undefined ? 3 : o.seed, rnd = K.rng(seed * 7919 + 101);
    var n = 22, pts = [];
    for (var i = 0; i < n; i++) {
      var a = -Math.PI / 2 + (i * 2 * Math.PI) / n;
      var k = 1 + 0.09 * Math.sin(3 * a + seed) + 0.06 * Math.cos(5 * a + seed * 0.7) + (i % 2 ? -0.05 : 0.04) + (rnd() - 0.5) * 0.06;
      var x = 82 * k * Math.cos(a), y = -72 + 70 * k * Math.sin(a);
      if (y > -8) { x *= 1.06; y = Math.min(y, 0); }
      pts.push([x, y]);
    }
    var dark = isDark(col), shade = dark ? line("M" + P(pts[3][0], pts[3][1]) + " L" + P(pts[4][0], pts[4][1]) + " L" + P(pts[5][0], pts[5][1]) + " L" + P(pts[6][0], pts[6][1]) + " L" + P(pts[7][0], pts[7][1]), C.orange, 2.2) : dots(pts, 24, 0.3);
    var spots = [[-54, -104, 9], [48, -116, 7], [-62, -44, 8], [56, -42, 10], [8, -132, 6], [-30, -128, 5]].map(function (s) {
      return '<path d="' + polyD(ngon(s[0] + (rnd() - 0.5) * 6, s[1] + (rnd() - 0.5) * 6, s[2], s[2] * 0.8, 6, rnd())) + '" fill="' + ink + '" opacity="0.22"/>';
    }).join("");
    var faceMood = mood === "grin" ? "cross" : mood, mouth = mood === "smug" ? "fangs" : mood === "grin" ? "bigfangs" : mood === "dead" ? "dead" : mood;
    var f = face(0, -98, 2.4, { mood: faceMood, mouth: mouth, mouthY: mood === "grin" ? 12 : 11, mouthW: mood === "grin" ? 1.3 : 1 });
    var sash = "";
    if (o.label) {
      var sid = "kp-chr-sash" + ++uid, band = [[-90, -36], [90, -10], [90, 6], [-90, -20]], deg = (Math.atan2(26, 180) * 180) / Math.PI, ts = K.fitText(o.label, 15, 120, "Oswald", 600, 1.5);
      sash = '<defs><clipPath id="' + sid + '"><path d="' + polyD(pts) + '"/></clipPath></defs><g clip-path="url(#' + sid + ')">' + solid([poly(band)], C.cream, 3.2) +
        '<g transform="translate(-8,-13) rotate(' + deg.toFixed(1) + ')">' + text(0, 5, o.label, ts, C.war, "middle", ' letter-spacing="1.5"') + "</g></g>";
    }
    // each pose: the left arm's shoulder, elbow and hand (the right arm mirrors it)
    var pose = { steeple: [[-60, -52], [-46, -24], [-12, -39]], up: [[-60, -52], [-92, -70], [-88, -112]], limp: [[-60, -52], [-86, -22], [-114, -7]] }[o.arms || (mood === "dead" ? "limp" : "steeple")];
    var armSvg = !pose ? "" : [-1, 1].map(function (s) {
      var q = pose.map(function (p) { return [-s * p[0], p[1]]; }), sg = { x: q[0][0], y: q[0][1], ex: q[1][0], ey: q[1][1], hx: q[2][0], hy: q[2][1] };
      var claw = along([[-5.5, -2], [5.5, -2], [8, 6], [4, 3.5], [2.5, 10], [0, 4.5], [-2.5, 10], [-4, 3.5], [-8, 6]], sg.hx, sg.hy, sg.hx - sg.ex, sg.hy - sg.ey);
      return '<g class="blob-arm-' + (s < 0 ? "l" : "r") + '"' + pivot(q[0][0], q[0][1]) + ">" + solid([poly(limbPts(sg, 16, 12, 9)), poly(claw)], col, 3.6) + "</g>";
    }).join("");
    return '<g class="disease-blob"><g class="blob-body"' + pivot(0, 0) + ">" + solid([poly(pts)], col) + shade + spots + sash + f.all + "</g>" + armSvg + "</g>";
  }

  // ── A germ ────────────────────────────────────────────────────────
  // A small spiky germ with an angry little face, about 60 across (a person's head size), its bottom spike on y 0.
  // o: { color (a KIT.C key or hex; default "yellow"), mood "grin" (default) | "cross" | "smug" | "scared" | "dead" }
  // Parts (data-pivot): .germ-body (its center, 0,-30: spin, wobble); .eye, .pupil, .brows, .mouth.
  function germ(o) {
    o = o || {};
    var col = colorOf(o.color, C.yellow), mood = o.mood || "grin";
    var pts = starPts(0, -30, 30, 0.66, 11, -Math.PI / 2 + Math.PI / 11);
    var body = ngon(0, -30, 19, 19, 11, 0);
    var f = face(0, -33, 1.05, { mood: mood === "grin" ? "cross" : mood, mouth: mood === "grin" ? "grin" : mood === "smug" ? "fangs" : mood, sep: 8, mouthY: 10 });
    return '<g class="germ"><g class="germ-body"' + pivot(0, -30) + ">" + solid([poly(pts)], col, 3.6) + (isDark(col) ? "" : dots(pts, 6, 0.3)) +
      '<path d="' + polyD(body) + '" fill="none" stroke="' + ink + '" stroke-width="1.2" opacity="0.35"/>' + f.all + "</g></g>";
  }

  // ── A 1950s tin robot ─────────────────────────────────────────────
  // A tin toy robot: a box head with a face plate and a bulb antenna, a riveted chest with a gauge and a chest
  // light (like the humans' check-engine light), tube arms with pincers, box legs. About 205 tall to the bulb (a
  // person's height to the top of its head).
  // o: { color (a KIT.C key or hex; default "peri"), mood (any face mood; default "flat", which gets the speaker
  //      grille for a mouth), arms [[a1, a2], [b1, b2]] (deg, 0 = down, as KIT.person), light "red" | "teal" }
  // Parts (data-pivot): .robot-head (the neck, 0,-140), .robot-antenna (its base, 0,-184), .robot-arm-l (-42,-126)
  // and .robot-arm-r (42,-126), .robot-leg-l (-15,-64) and .robot-leg-r (15,-64), .chest-light; .eye, .pupil, .brows,
  // .mouth.
  function robot(o) {
    o = o || {};
    var col = colorOf(o.color, C.peri), mood = o.mood || "flat", arms = o.arms || [[16, 6], [-16, -6]];
    var light = o.light === "red" ? C.war : o.light === "teal" ? C.med : C.cream, dark = isDark(col);
    var legs = [-1, 1].map(function (s) {
      var leg = [[s * 6, -64], [s * 24, -64], [s * 23, -12], [s * 7, -12]], foot = [[s * 2, -13], [s * 30, -13], [s * 33, 0], [s * -1, 0]];
      return '<g class="robot-leg-' + (s < 0 ? "l" : "r") + '"' + pivot(s * 15, -64) + ">" + solid([poly(leg)], col) + (dark ? "" : dots(leg, s * 15, 0.25)) +
        line("M" + P(s * 7, -46) + " H" + (s * 23).toFixed(1) + " M" + P(s * 7, -30) + " H" + (s * 23).toFixed(1), ink, 1.6) + solid([poly(foot)], C.slate, 3.6) + "</g>";
    }).join("");
    var torso = [[-38, -132], [38, -132], [32, -70], [-32, -70]];
    var rivets = [[-32, -126], [32, -126], [-28, -76], [28, -76]].map(function (r) { return '<circle cx="' + r[0] + '" cy="' + r[1] + '" r="2.2" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="1.2"/>'; }).join("");
    var panelPts = [[-22, -122], [22, -122], [22, -94], [-22, -94]];
    var gauge = '<path d="M' + P(-14, -100) + " A10,10 0 0 1 " + P(6, -100) + ' Z" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="1.6"/>' + line("M" + P(-4, -100) + " L" + P(2, -110), C.war, 1.8) +
      '<circle cx="14" cy="-114" r="3" fill="' + C.war + '" stroke="' + ink + '" stroke-width="1.2"/><circle cx="14" cy="-104" r="3" fill="' + C.yellow + '" stroke="' + ink + '" stroke-width="1.2"/>' + line("M-16,-116 H-4 M-16,-112 H-8", C.cyan, 1.6);
    var armSvg = [-1, 1].map(function (s, i) {
      var sg = seg(s * 42, -126, arms[i], 30), dx = sg.hx - sg.ex, dy = sg.hy - sg.ey;
      var prongs = [along([[-2, 0], [-7, 4], [-6, 13], [-3, 11], [-3, 5]], sg.hx, sg.hy, dx, dy), along([[2, 0], [7, 4], [6, 13], [3, 11], [3, 5]], sg.hx, sg.hy, dx, dy)];
      var rings = [0.3, 0.6].map(function (t) {
        var px = sg.x + (sg.ex - sg.x) * t, py = sg.y + (sg.ey - sg.y) * t, n = nrm(sg.x, sg.y, sg.ex, sg.ey), qx = sg.ex + (sg.hx - sg.ex) * t, qy = sg.ey + (sg.hy - sg.ey) * t, m = nrm(sg.ex, sg.ey, sg.hx, sg.hy);
        return "M" + P(px + n[0] * 5.5, py + n[1] * 5.5) + " L" + P(px - n[0] * 5.5, py - n[1] * 5.5) + " M" + P(qx + m[0] * 5, qy + m[1] * 5) + " L" + P(qx - m[0] * 5, qy - m[1] * 5);
      }).join(" ");
      return '<g class="robot-arm-' + (s < 0 ? "l" : "r") + '"' + pivot(s * 42, -126) + ">" + solid([poly(prongs[0]), poly(prongs[1])], C.slate, 3) + solid([poly(limbPts(sg, 12, 11, 10))], col, 3.6) + line(rings, ink, 1.4) +
        solid([poly(ngon(s * 42, -126, 6, 6, 8, 0.2))], C.slate, 2.6) + "</g>";
    }).join("");
    var headPts = [[-27, -184], [27, -184], [29, -142], [-29, -142]], plate = [[-21, -178], [21, -178], [22, -149], [-22, -149]];
    var f = face(0, -168, 1.25, { mood: mood, mouth: mood === "flat" ? "grille" : mood, sep: 8.4, mouthY: 10 });
    var head = '<g class="robot-head"' + pivot(0, -140) + ">" +
      solid([poly([[-34, -172], [-27, -172], [-27, -154], [-34, -154]]), poly([[34, -172], [27, -172], [27, -154], [34, -154]])], C.slate, 3) +
      '<g class="robot-antenna"' + pivot(0, -184) + ">" + line("M0,-184 V-200", ink, 3.6) + solid([poly(ngon(0, -204, 5.5, 5.5, 8, 0.2))], C.war, 2.6) + "</g>" +
      solid([poly(headPts)], col) + (dark ? line("M" + P(27, -182) + " L" + P(29, -144), C.orange, 2) : dots(headPts, 12, 0.25)) + solid([poly(plate)], C.cream, 3) + f.all + "</g>";
    return '<g class="robot">' + legs + solid([poly([[-30, -74], [30, -74], [26, -60], [-26, -60]])], C.slate, 3.6) +
      solid([poly([[-9, -146], [9, -146], [9, -130], [-9, -130]])], C.slate, 3) + line("M-9,-141 H9 M-9,-136 H9", C.cream, 1.4) +
      solid([poly(torso)], col) + (dark ? line("M" + P(37, -128) + " L" + P(32, -74), C.orange, 2) : dots(torso, 10, 0.25)) + rivets +
      solid([poly(panelPts)], C.navy, 3) + gauge +
      '<circle class="chest-light" cx="16" cy="-82" r="5" fill="' + light + '" stroke="' + ink + '" stroke-width="2"/>' +
      armSvg + head + "</g>";
  }

  K.props.democracyDog = democracyDog;
  K.props.optimitron = optimitron;
  K.props.calculator = calculator;
  K.props.diseaseBlob = diseaseBlob;
  K.props.germ = germ;
  K.props.robot = robot;

  K.props.SHEET.push(
    ["democracyDog", { tail: "papers" }, "DEMOCRACY DOG (papers)"],
    ["democracyDog", { tail: "pills", mood: "smile" }, "DEMOCRACY DOG (pills, smile)"],
    ["democracyDog", { face: "front", mood: "dizzy", tail: "papers", seal: "war" }, "DOG (front, dizzy, war papers)"],
    ["optimitron", {}, "OPTIMITRON"],
    ["optimitron", { mood: "eager", health: 120, wealth: 120, card: "CURE IT", pop: 70 }, "OPTIMITRON (eager, dials up)"],
    ["calculator", { display: "604" }, "CALCULATOR (calm)"],
    ["calculator", { mood: "scream" }, "CALCULATOR (scream)"],
    ["robot", {}, "TIN ROBOT"],
    ["diseaseBlob", {}, "DISEASE BLOB (smug)"],
    ["diseaseBlob", { color: "yellow", mood: "grin", label: "CANCER", seed: 8 }, "DISEASE BLOB (grin, sash)"],
    ["diseaseBlob", { color: "rust", mood: "dead", seed: 5 }, "DISEASE BLOB (dead)"],
    ["germ", {}, "GERM (grin)"],
    ["germ", { color: "orange", mood: "smug" }, "GERM (smug, orange)"],
    ["germ", { color: "peri", mood: "scared" }, "GERM (scared)"],
    ["robot", { mood: "eager", arms: [[150, 170], [-30, -10]], light: "red" }, "TIN ROBOT (eager, red light)"],
    ["democracyDog", { tail: "plain", mood: "cross" }, "DOG (plain tail, cross)"]
  );
})();
