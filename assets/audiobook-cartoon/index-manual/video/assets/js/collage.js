// Cut-out collage (cartoon-style-bible.md section 1): hand-tinted engraving cut-outs from assets/art/collage/ on
// aged paper, moving stiffly on twos (12 drawings a second), like paper under a rostrum camera.
//
//   KIT.collage(spec)   builds a whole collage scene from a short spec: { id, seed, cast, beats, views, host }.
//                       The spec's fields and every move are in video/README.md, "Writing a collage scene".
//   KIT.collage.SIZES   each cut-out's art size in px (generated: assets/js/art-sizes.js, loaded before this file)
//   KIT.collage.axes(o) a chart's axes ({ box, x, y, title, unit }), with pt(x, y), the canvas px of a data point;
//                       pass it as `chart` to the chart, rule, chain, bar, line and pile moves
//
// The moves that make copies of a cut-out (chain, pile/stack, march, pictogram) call them <id>.0, <id>.1, ...; a
// beat's `who` may name the id for all of them, and xray and pictogram take every, first, last, pick or random to
// choose some. line, pile, counter, xray, march, pictogram and lap are the moves added for the paperback chapters
// (KIT-PAPERBACK.md); compositions/scenes/kit-demo/ shows each one (parts/kit-demo.json).
//
// Load it after kit.js and film.js. Copy compositions/scenes/pilot-collage/*.html for the file around a spec.
(function () {
  var K = window.KIT;
  if (K.collage) return;
  if (!K.film) throw new Error("collage.js: load assets/js/film.js before it");
  var F = 1 / 12, ART = "assets/art/collage/";
  var INK = "#2B2033", RED = "#A8322A", CARD = "#F5ECD3";
  // every cut-out's size, from assets/js/art-sizes.js (tools/art-sizes.py; load it before this file)
  var SIZES = window.KIT_ART_SIZES || {};
  var PAPER = "radial-gradient(circle at 17% 80%, rgba(140,96,40,0.16) 0, rgba(140,96,40,0) 8%)," +
    "radial-gradient(circle at 86% 18%, rgba(140,96,40,0.13) 0, rgba(140,96,40,0) 6%)," +
    "radial-gradient(ellipse 30% 22% at 70% 86%, rgba(120,80,30,0.10) 0, rgba(120,80,30,0) 100%)," +
    "radial-gradient(ellipse 62% 58% at 50% 44%, #F3E7C8 0%, #E8D7AF 55%, #CDB283 100%)";
  var SHADOW = "drop-shadow(5px 7px 3px rgba(58,36,12,0.42))";
  var CHAR = SHADOW + " brightness(0.2) contrast(1.4) sepia(0.3)";

  if (!document.getElementById("kit-collage-css")) {
    var css = document.createElement("style");
    css.id = "kit-collage-css";
    css.textContent = ".cg-stage .cg-ab{position:absolute}.cg-stage .cg-full{position:absolute;left:0;top:0;width:100%;height:100%}" +
      ".cg-stage img{position:absolute;left:0;top:0;width:100%;height:100%}.cg-stage .cg-sh{filter:" + SHADOW + "}" +
      ".cg-stage .cg-eye{position:absolute;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;background:#FFFBEF;border:2px solid #120C08;box-sizing:border-box}" +
      ".cg-stage .cg-eye i{position:absolute;left:9px;top:9px;width:9px;height:9px;border-radius:50%;background:#120C08}" +
      ".cg-stage .cg-puff{position:absolute;width:60px;height:60px;margin:-30px 0 0 -30px;border-radius:50%;background:radial-gradient(circle at 40% 40%, #8C857A 0, #5E574E 70%)}";
    document.head.appendChild(css);
  }

  var px = function (n) { return n.toFixed(1) + "px"; };
  var clamp = function (u) { return u < 0 ? 0 : u > 1 ? 1 : u; };
  var smooth = function (u) { u = clamp(u); return u * u * (3 - 2 * u); };
  var twos = function (t) { return Math.floor(t * 12 + 1e-6) / 12; };
  // Piecewise-linear keys [[t, a, b, ...], ...] (t relative to t0) -> [a, b, ...] at t.
  function keys(t0, Ks, t) {
    t -= t0;
    if (t <= Ks[0][0]) return Ks[0].slice(1);
    for (var i = 0; i < Ks.length - 1; i++) {
      if (t < Ks[i + 1][0]) {
        var u = (t - Ks[i][0]) / (Ks[i + 1][0] - Ks[i][0]);
        return Ks[i].slice(1).map(function (v, j) { return v + (Ks[i + 1][j + 1] - v) * u; });
      }
    }
    return Ks[Ks.length - 1].slice(1);
  }
  function put(el, x, y, r, sx, sy) {
    if (sx === undefined) sx = 1;
    if (sy === undefined) sy = sx;
    el.style.transform = "translate(" + px(x) + "," + px(y) + ") rotate(" + (r || 0).toFixed(2) + "deg) scale(" + sx.toFixed(3) + "," + sy.toFixed(3) + ")";
  }
  // "inherit", never "visible": a visible child shows through its scene when the scene is hidden
  var vis = function (e, on) { e.style.visibility = on ? "inherit" : "hidden"; };
  // A point on the art: a keyword or art px.
  function spot(p, w, h) {
    if (!p || p === "center") return [w / 2, h / 2];
    var named = { bottom: [w / 2, h], top: [w / 2, 0], left: [0, h / 2], right: [w, h / 2], topleft: [0, 0] }[p];
    if (named) return named;
    if (!Array.isArray(p)) throw new Error("KIT.collage: no point '" + p + "'");
    return p;
  }
  function clipPts(c, w, h) {
    var m = { left: [[0, 0], [w / 2, 0], [w / 2, h], [0, h]], right: [[w / 2, 0], [w, 0], [w, h], [w / 2, h]],
      top: [[0, 0], [w, 0], [w, h / 2], [0, h / 2]], bottom: [[0, h / 2], [w, h / 2], [w, h], [0, h]] }[c];
    return m || c;
  }
  function img(name, clip, k) {
    var sz = SIZES[name];
    var cp = clip ? ' style="clip-path:polygon(' + clipPts(clip, sz[0], sz[1]).map(function (p) { return px(p[0] * k) + " " + px(p[1] * k); }).join(",") + ')"' : "";
    return '<div class="cg-full cg-sh"><img src="' + ART + name + '.webp"' + cp + "></div>";
  }
  function sunburstSvg(r) {
    var n = 28, s = "";
    for (var i = 0; i < n; i++) {
      var a0 = (i / n) * 2 * Math.PI, a1 = ((i + 1) / n) * 2 * Math.PI;
      s += '<path d="M0,0 L' + (r * Math.cos(a0)).toFixed(1) + "," + (r * Math.sin(a0)).toFixed(1) + " L" + (r * Math.cos(a1)).toFixed(1) + "," + (r * Math.sin(a1)).toFixed(1) + ' Z" fill="' + (i % 2 ? "#EDC566" : "#F6DD92") + '"/>';
    }
    return '<svg width="' + 2 * r + '" height="' + 2 * r + '" viewBox="' + -r + " " + -r + " " + 2 * r + " " + 2 * r + '" style="position:absolute;left:0;top:0">' + s +
      '<circle r="' + r * 0.2 + '" fill="#FFF3C4" opacity="0.8"/></svg>';
  }
  // A chart's axes: box [left, top, right, bottom] in canvas px; x and y [min, max, tick step]; xLabels and yLabels
  // (label every this much; the tick step); title; unit (after the y labels); size (label px, 34).
  function axes(o) {
    var b = o.box, X = o.x, Y = o.y;
    return { box: b, x: X, y: Y, title: o.title, subtitle: o.subtitle, unit: o.unit || "", size: o.size || 34, xLabels: o.xLabels || X[2], yLabels: o.yLabels || Y[2],
      pt: function (xv, yv) { return [b[0] + (xv - X[0]) / (X[1] - X[0]) * (b[2] - b[0]), b[3] - (yv - Y[0]) / (Y[1] - Y[0]) * (b[3] - b[1])]; } };
  }
  function axesSvg(c, W, H) {
    var b = c.box, z = c.size, s = "", every = function (v, v0, k) { var u = (v - v0) / k; return Math.abs(u - Math.round(u)) < 1e-6; };
    var tx = function (x, y, anchor, t, size, title) {
      return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" text-anchor="' + anchor + '" font-family="' + (title ? "Fraunces" : "Oswald") + '" font-weight="' + (title ? 900 : 600) +
        '" font-size="' + size.toFixed(1) + '" fill="' + INK + '">' + t + "</text>";
    };
    for (var yv = c.y[0]; yv <= c.y[1] + 1e-9; yv += c.y[2]) {
      var y = c.pt(c.x[0], yv)[1];
      if (yv > c.y[0]) s += '<line x1="' + b[0] + '" y1="' + y.toFixed(1) + '" x2="' + b[2] + '" y2="' + y.toFixed(1) + '" stroke="' + INK + '" stroke-opacity="0.16" stroke-width="2"/>';
      if (every(yv, c.y[0], c.yLabels)) s += tx(b[0] - 18, y + z * 0.36, "end", yv + c.unit, z);
    }
    for (var xv = c.x[0]; xv <= c.x[1] + 1e-9; xv += c.x[2]) {
      var x = c.pt(xv, c.y[0])[0];
      s += '<line x1="' + x.toFixed(1) + '" y1="' + b[3] + '" x2="' + x.toFixed(1) + '" y2="' + (b[3] + 14) + '" stroke="' + INK + '" stroke-width="4"/>';
      if (every(xv, c.x[0], c.xLabels)) s += tx(x, b[3] + 22 + z, "middle", xv, z);
    }
    s += '<path d="M' + b[0] + "," + (b[1] - 30) + " L" + b[0] + "," + b[3] + " L" + (b[2] + 30) + "," + b[3] + '" fill="none" stroke="' + INK + '" stroke-width="6"/>';
    if (c.title) s += tx(b[0] - 18, b[1] - (c.subtitle ? 78 : 56), "start", c.title, z * 1.35, true);
    if (c.subtitle) s += tx(b[0] - 18, b[1] - 34, "start", c.subtitle, z * 0.85);
    return '<svg class="cg-full" width="' + W + '" height="' + H + '">' + s + "</svg>";
  }
  // element ids the kit itself uses (<scene id>-<name>)
  var RESERVED = ["weave", "film", "shake", "stage", "bolts", "flash", "xflash", "hcam", "hwall", "hwish", "hfront", "hiris"];
  var DIRS = { left: [-1, 0], right: [1, 0], top: [0, -1], bottom: [0, 1] };
  var dir = function (d) { if (!DIRS[d]) throw new Error("KIT.collage: no direction '" + d + "'"); return DIRS[d]; };

  function collage(spec) {
    window.__timelines = window.__timelines || {};
    var ID = spec.id, D = K.scene(ID).duration, W = K.W, H = K.H;
    var q = function (s) { return document.getElementById(ID + "-" + s); };
    var cue = function (w, n) { return K.cue(ID, w, n); };
    var timeOf = function (u) { return u === undefined ? Infinity : typeof u === "number" ? u : Array.isArray(u) ? cue(u[0], u[1]) + (u[2] || 0) : cue(u); };
    var A = {}, pieces = {}, ops = [], events = {}, tickers = [], shakes = [], cams = [];
    var cast = [], cutLayer = [], back = [], front = [], unders = {}, afters = {}, chains = {};
    // groups: the copies a move made (chain, pile, march, pictogram), by its id; a beat's `who` may name one
    var groups = {}, grids = {}, xflashes = [], greyed = [];
    // spec.plate [x0, y0, x1, y1]: the area the paper (and a wash or a flash) covers, for a camera that travels past the
    // frame (default the frame)
    var PL = spec.plate || [0, 0, W, H];
    var plateBox = 'class="cg-ab" style="left:' + px(PL[0]) + ";top:" + px(PL[1]) + ";width:" + px(PL[2] - PL[0]) + ";height:" + px(PL[3] - PL[1]) + ";";

    function actor(name, a) {
      if (A[name] || pieces[name]) throw new Error("KIT.collage: two things called '" + name + "'");
      if (RESERVED.indexOf(name) >= 0) throw new Error("KIT.collage: '" + name + "' is the kit's own element; call the cast member something else");
      a.name = name; a.before = a.before || ""; a.children = a.children || [];
      a.home = function () { return [a.left + a.w / 2, a.top + a.h / 2]; };
      A[name] = a; events[name] = events[name] || [];
      return a;
    }
    function get(name) { if (!A[name]) throw new Error("KIT.collage: no cast member '" + name + "' in " + ID); return A[name]; }
    function box(a, inner, extra) {
      return '<div id="' + ID + "-" + a.name + '" class="cg-ab" style="left:' + px(a.left) + ";top:" + px(a.top) + ";width:" + px(a.w) + ";height:" + px(a.h) +
        ";transform-origin:" + px(a.pivot[0]) + " " + px(a.pivot[1]) + ";" + (extra || "") + '">' + inner + "</div>";
    }
    // Agencies and named institutions carry their names in every scene (art px; width sets the letter size), each on a sign plate.
    // A scene can pass its own label, or label: [] for none.
    var NAMES = {
        "nih-building": { text: "NIH", at: [127, 236], width: 96, size: 999, plaque: true },
        "irs-building": { text: "IRS", at: [110, 92], width: 100, size: 999, plaque: true },
        "sec-building": { text: "SEC", at: [155, 40], width: 90, size: 999, plaque: true },
        "bls-building": { text: "BLS", at: [110, 128], width: 72, size: 999, plaque: true },
        "census-building": { text: "CENSUS", at: [139, 70], width: 170, size: 999, plaque: true },
        "who-building": { text: "WHO", at: [150, 230], width: 110, size: 999, plaque: true },
        "pcori-building": { text: "PCORI", at: [120, 50], width: 95, size: 999, plaque: true },
        "fdic-office": { text: "FDIC", at: [130, 48], width: 95, size: 999, plaque: true },
        "wiv-building": { text: "WIV", at: [120, 258], width: 72, size: 999, plaque: true },
        "ecohealth-building": { text: "ECOHEALTH", at: [106, 106], width: 150, size: 999, plaque: true },
        "fifa-building": { text: "FIFA", at: [127, 104], width: 96, size: 999, plaque: true },
        "fda-building": { text: "FDA", at: [161, 220], width: 120, size: 999, plaque: true },
        "fda-folded": { text: "FDA", at: [222, 172], width: 112, size: 999, plaque: true, tilt: 10 },
        "fda-scared": { text: "FDA", at: [222, 168], width: 120, size: 999, plaque: true },
        "fda-sip": { text: "FDA", at: [174, 175], width: 116, size: 999, plaque: true },
        "fda-window": { text: "FDA", at: [190, 40], width: 130, size: 999, plaque: true },
        "fda-window-shut": { text: "FDA", at: [190, 40], width: 130, size: 999, plaque: true },
        "fda-pistol": { text: "FDA", at: [245, 140], width: 100, size: 999, plaque: true },
        "filing-cabinet-fda": { text: "FDA", at: [111, 128], width: 100, size: 999, plaque: true },
        "fed-crank-up": { text: "THE FED", at: [296, 118], width: 130, size: 999, plaque: true },
        "fed-crank-down": { text: "THE FED", at: [323, 118], width: 130, size: 999, plaque: true },
        "fed-mouth": { text: "THE FED", at: [205, 97], width: 110, size: 999, plaque: true },
        "fomc": { text: "FOMC", at: [214, 168], width: 110, size: 999, plaque: true },
        "bis-tower": { text: "BIS", at: [93, 60], width: 70, size: 999, plaque: true },
        "dendreon-building": { text: "DENDREON", at: [118, 120], width: 175, size: 999, plaque: true },
        "dih-building": { text: "DIH", at: [130, 133], width: 100, size: 999, plaque: true },
        "lehman-brothers": { text: "LEHMAN BROS.", at: [103, 122], width: 190, size: 999, plaque: true },
        "palantir": { text: "PALANTIR", at: [112, 229], width: 165, size: 999, plaque: true },
        "wall-street": { text: "WALL ST.", at: [113, 95], width: 150, size: 999, plaque: true },
        "bretton-woods-hotel": { text: "BRETTON WOODS", at: [168, 168], width: 230, size: 999, plaque: true },
        "supreme-court": { text: "SUPREME COURT", at: [140, 105], width: 235, size: 999, plaque: true },
        "oxford-college": { text: "OXFORD", at: [121, 205], width: 150, size: 999, plaque: true },
        "think-tank": { text: "THINK TANK", at: [205, 448], width: 270, size: 999, plaque: true },
        "hedge-fund": { text: "HEDGE FUND", at: [130, 300], width: 185, size: 999, plaque: true },
    };
    // A cut-out from the cast: art, x, y, scale, anchor, pivot, clip, pieces, cut, points, eyes, smoke, faces, hidden.
    function cutout(name, o) {
      var sz = SIZES[o.art];
      if (!sz) throw new Error("KIT.collage: no size for art '" + o.art + "' (run tools/art-sizes.py, and load assets/js/art-sizes.js before collage.js)");
      var k = o.scale || 1, an = spot(o.anchor, sz[0], sz[1]), pv = spot(o.pivot, sz[0], sz[1]);
      var a = actor(name, { o: o, k: k, w: sz[0] * k, h: sz[1] * k, pivot: [pv[0] * k, pv[1] * k], an: [an[0] * k, an[1] * k], points: o.points || {},
        faces: o.faces === "left" ? -1 : 1, hidden: o.hidden, eyes: o.eyes || [], smoke: o.smoke ? [].concat(o.smoke.length && Array.isArray(o.smoke[0]) ? o.smoke : [o.smoke]) : [] });
      a.left = (o.x === undefined ? W / 2 : o.x) - an[0] * k;
      a.top = (o.y === undefined ? H / 2 : o.y) - an[1] * k;
      var piecesHtml = function (ps) {
        return Object.keys(ps).map(function (pn) {
          var p = ps[pn], full = name + "." + pn, pp = spot(p.pivot, sz[0], sz[1]);
          if (A[full] || pieces[full]) throw new Error("KIT.collage: two things called '" + full + "'");
          pieces[full] = { actor: name };
          events[full] = [];
          return '<div id="' + ID + "-" + full + '" class="cg-full" style="transform-origin:' + px(pp[0] * k) + " " + px(pp[1] * k) + '">' +
            img(o.art, p.clip, k) + (p.pieces ? piecesHtml(p.pieces) : "") + "</div>";
        }).join("");
      };
      var artHtml = o.pieces ? piecesHtml(o.pieces) : img(o.art, o.clip, k);
      a.html = function () {
        var es = o.eyeSize || 30, deco = a.eyes.map(function (e) { return '<div class="cg-eye" style="left:' + px(e[0] * k) + ";top:" + px(e[1] * k) + (es !== 30 ? ";zoom:" + (es / 30).toFixed(3) : "") + ';visibility:hidden"><i></i></div>'; }).join("");
        a.smoke.forEach(function (sm) { for (var i = 0; i < 3; i++) deco += '<div class="cg-puff" style="left:' + px(sm[0] * k) + ";top:" + px(sm[1] * k) + ';visibility:hidden"></div>'; });
        [].concat(o.label !== undefined ? o.label : o.clip || o.pieces ? [] : NAMES[o.art] || []).forEach(function (l) {
          var size = K.fitText(l.text, l.size || 40, (l.width || 200) * k, "Fraunces", 900), lw = K.textWidth(l.text, size, "Fraunces", 900);
          deco += '<div class="cg-ab" style="left:' + px(l.at[0] * k - lw / 2) + ";top:" + px(l.at[1] * k - size * 0.6) + ";width:" + px(lw) + ";font:900 " + px(size) + "/1.2 Fraunces;color:" + INK +
            ";white-space:nowrap;transform:rotate(" + (l.tilt || 0) + "deg)" + (l.plaque ? ";width:auto;background:#F2E6C6;border:" + px(3 * k) + " solid " + INK + ";border-radius:" + px(6 * k) + ";padding:0 " + px(8 * k) + ";margin-left:" + px(-8 * k) : "") + '">' + l.text + "</div>";
        });
        deco += a.children.map(function (c) { return A[c].html(); }).join("");
        return a.before + box(a, '<div class="cg-full cg-art">' + artHtml + "</div>" + deco, a.hidden ? "visibility:hidden" : "");
      };
      if (o.cut) {
        var sides = { lr: ["L", "left", "R", "right"], tb: ["T", "top", "B", "bottom"] }[o.cut];
        if (!sides) throw new Error("KIT.collage: cut is 'lr' or 'tb'");
        a.cutAxis = o.cut;
        a.cutPieces = [name + "." + sides[0], name + "." + sides[2]];
        var po = function (clip) { var c = {}; for (var key in o) c[key] = o[key]; c.cut = undefined; c.pieces = undefined; c.clip = clip; c.hidden = true; return c; };
        cutLayer.push(cutout(a.cutPieces[0], po(sides[1])).name, cutout(a.cutPieces[1], po(sides[3])).name);
      }
      return a;
    }
    function op(name, fn) {
      if (!A[name] && !pieces[name]) throw new Error("KIT.collage: no cast member or piece '" + name + "' in " + ID);
      ops.push({ name: name, fn: fn });
    }
    function ev(name, t, on) { events[name].push({ t: t, on: on, i: events[name].length }); }
    // An entrance or exit made of scale keys.
    function scaleOp(name, t0, Ks) { op(name, function (s, t) { var v = keys(t0, Ks, t); s.sx *= v[0]; s.sy *= v.length > 1 ? v[1] : v[0]; }); }
    function shakeOp(t0, frames, ax, amp) {
      if (!amp) return;
      shakes.push(function (t, fr, sh) { if (t >= t0 && t < t0 + frames * F - 1e-6) sh[ax] += fr % 2 ? amp : -amp; });
    }
    var STAMP_KEYS = function (from) { return [[-F, from], [F, 0.94], [2 * F, 1]]; };

    // A text card (banner) or a hang-tag: sign actors.
    function card(name, o) {
      var sp = o.spacing || 0, size = K.fitText(o.text, o.size || 150, o.width || 1080, "Fraunces", 900, sp), lh = o.lineHeight || 1.25;
      var w = K.textWidth(o.text, size, "Fraunces", 900, sp) + (o.pad === undefined ? 110 : o.pad), h = size * lh;
      var col = o.color === "ink" ? INK : RED, b = o.color === "ink" ? [4, 7, 9] : [5, 8, 11];
      var a = actor(name, { w: w, h: h, pivot: [w / 2, h / 2], points: {}, eyes: [], smoke: [], faces: 1, hidden: true });
      a.left = (o.x === undefined ? W / 2 : o.x) - w / 2;
      a.top = (o.y === undefined ? 780 : o.y) - h / 2;
      a.html = function () {
        return box(a, '<div class="cg-full cg-sh"><div class="cg-full" style="background:' + CARD + ";border:" + b[0] + "px solid " + col + ";box-shadow:inset 0 0 0 " + b[1] + "px " + CARD + ",inset 0 0 0 " + b[2] + "px " + col + '"></div>' +
          '<div class="cg-full" style="font:900 ' + px(size) + "/" + px(h) + " Fraunces;color:" + INK + ";text-align:center;white-space:nowrap;letter-spacing:" + sp + 'px">' + o.text + "</div></div>", "visibility:hidden");
      };
      return a;
    }
    function tagSign(name, o, hungOn) {
      var w = o.w || 500, h = o.h || 250, hole = [26, 40], size = K.fitText(o.text, 104, w - 70, "Fraunces", 900);
      var on = get(hungOn), oc = on.home();
      var cx = o.x === undefined ? on.left + on.w + w / 2 + 40 : o.x, cy = o.y === undefined ? oc[1] : o.y;
      var a = actor(name, { w: w, h: h, pivot: hole, points: {}, eyes: [], smoke: [], faces: 1, hidden: true, titleSize: size });
      a.left = cx - w / 2; a.top = cy - h / 2;
      a.html = function () {
        return '<svg id="' + ID + "-" + name + '-string" class="cg-ab" width="' + W + '" height="' + H + '" style="left:0;top:0;visibility:hidden"><path d="" fill="none" stroke="' + INK + '" stroke-width="3"/></svg>' +
          box(a, '<div class="cg-full cg-sh"><div class="cg-full" style="background:' + CARD + ";border:4px solid " + INK + ";border-radius:6px 26px 26px 6px;box-shadow:inset 0 0 0 7px " + CARD + ",inset 0 0 0 9px " + INK + '"></div>' +
            '<div class="cg-ab" style="left:' + (hole[0] - 11) + "px;top:" + (hole[1] - 11) + "px;width:22px;height:22px;border-radius:50%;border:4px solid " + INK + ';box-sizing:border-box;background:#E8D7AF"></div>' +
            '<div class="cg-ab" style="left:40px;right:30px;top:34px;text-align:center;white-space:nowrap;font:900 ' + px(size) + "/1 Fraunces;color:" + INK + '">' + o.text + "</div>" +
            a.children.map(function (c) { return A[c].html(); }).join("") + "</div>", "visibility:hidden");
      };
      return a;
    }
    // A rubber-stamp mark: on a sign (inside it, under its title) or free-standing at x, y.
    function stampMark(name, o, sign) {
      var onArt = sign && sign.o, w = sign && !onArt ? sign.w - 88 : null, size = K.fitText(o.text, o.size || 56, w ? w - 52 : o.width || 1000, "Oswald", 600);
      if (!w) w = K.textWidth(o.text, size, "Oswald", 600) + 52;
      var h = size * 1.45;
      var a = actor(name, { w: w, h: h, pivot: [w / 2, h / 2], points: {}, eyes: [], smoke: [], faces: 1, hidden: true });
      if (onArt && !o.spot) throw new Error("KIT.collage: a stamp on cut-out '" + sign.name + "' needs spot: [x, y] (art px)");
      a.left = onArt ? o.spot[0] * sign.k - w / 2 : sign ? 44 : (o.x === undefined ? W / 2 : o.x) - w / 2;
      a.top = onArt ? o.spot[1] * sign.k - h / 2 : sign ? 60 + (sign.titleSize || 0) : (o.y === undefined ? H / 2 : o.y) - h / 2;
      a.html = function () {
        return '<div id="' + ID + "-" + name + '" class="cg-ab" style="left:' + px(a.left) + ";top:" + px(a.top) + ";width:" + px(w) + ";height:" + px(h) + ";box-sizing:border-box;border:5px solid " + RED + ";color:" + RED +
          ";font:600 " + px(size) + "/" + px(size * 1.32) + ' Oswald;white-space:nowrap;text-align:center;visibility:hidden;transform-origin:50% 50%">' + o.text + "</div>";
      };
      if (sign) { sign.children.push(name); a.inside = true; } else front.push(name);
      return a;
    }

    // ── Helpers for the moves that make copies or ride a path (line, pile, march, pictogram, lap, xray) ──
    // A copy's scale: `height` (canvas px, times `sizes[art]`) or `scale`.
    function fitScale(b, art) {
      if (!SIZES[art]) throw new Error("KIT.collage: no size for art '" + art + "'");
      return b.height ? b.height * ((b.sizes || {})[art] || 1) / SIZES[art][1] : b.scale || 1;
    }
    function copy(nm, art, x, y, b, more) {
      var o = { art: art, x: x, y: y, anchor: b.anchor || "bottom", pivot: "bottom", scale: fitScale(b, art), hidden: true, faces: b.faces };
      for (var key in more || {}) o[key] = more[key];
      var a = cutout(nm, o);
      cast.push(nm);
      return a;
    }
    // Where a cut-out's anchor is at state s (its offset, turn and scale about its pivot), and the offset that puts it on P.
    function anchorAt(a, s) {
      var an = a.an || [a.w / 2, a.h / 2], O = [a.left + a.pivot[0], a.top + a.pivot[1]];
      var vx = (a.left + an[0] - O[0]) * s.sx, vy = (a.top + an[1] - O[1]) * s.sy, c = Math.cos(s.r * Math.PI / 180), sn = Math.sin(s.r * Math.PI / 180);
      return [O[0] + s.x + vx * c - vy * sn, O[1] + s.y + vx * sn + vy * c];
    }
    function placeAt(a, s, P) { var p = anchorAt(a, s); s.x += P[0] - p[0]; s.y += P[1] - p[1]; }
    // A path through canvas points, measured along its length: at(d) is [x, y, heading in degrees] d px along it;
    // d(dist) is the SVG path drawn up to there; lenAtX(x) is how far along it first reaches canvas x.
    function track(pts, closed) {
      if (!pts || pts.length < 2) throw new Error("KIT.collage: a path needs two or more points");
      var P = closed ? pts.concat([pts[0]]) : pts, cum = [0];
      for (var i = 1; i < P.length; i++) cum.push(cum[i - 1] + Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]));
      var L = cum[cum.length - 1];
      var norm = function (d) { return closed ? ((d % L) + L) % L : d < 0 ? 0 : d > L ? L : d; };
      var seg = function (d) { var lo = 0, hi = P.length - 2; while (lo < hi) { var m = (lo + hi + 1) >> 1; if (cum[m] <= d) lo = m; else hi = m - 1; } return lo; };
      var at = function (d) {
        d = norm(d);
        var i = seg(d), a = P[i], e = P[i + 1], u = (d - cum[i]) / (cum[i + 1] - cum[i] || 1);
        return [a[0] + (e[0] - a[0]) * u, a[1] + (e[1] - a[1]) * u, Math.atan2(e[1] - a[1], e[0] - a[0]) * 180 / Math.PI];
      };
      return {
        L: L, P: P, at: at,
        d: function (d) {
          d = norm(d);
          if (d <= 0) return "";
          var i = seg(d), s = "M" + P[0][0].toFixed(1) + "," + P[0][1].toFixed(1), tip = at(d);
          for (var j = 1; j <= i; j++) s += " L" + P[j][0].toFixed(1) + "," + P[j][1].toFixed(1);
          return s + " L" + tip[0].toFixed(1) + "," + tip[1].toFixed(1);
        },
        lenAtX: function (x) {
          for (var i = 0; i < P.length - 1; i++) {
            var a = P[i][0], e = P[i + 1][0];
            if (x >= Math.min(a, e) && x <= Math.max(a, e)) return cum[i] + (cum[i + 1] - cum[i]) * (e === a ? 1 : (x - a) / (e - a));
          }
          return x <= P[0][0] ? 0 : L;
        },
      };
    }
    // Some of a group: every (every Nth, from index start), first, last, pick (indices) or random (that many, by seed).
    function pickOf(b, list, bi) {
      var idx = list.map(function (n, i) { return i; }), s0 = b.start || 0;
      if (b.pick) idx = [].concat(b.pick);
      if (b.every) idx = idx.filter(function (i) { return i >= s0 && (i - s0) % b.every === 0; });
      if (b.first !== undefined) idx = idx.slice(0, b.first);
      if (b.last !== undefined) idx = idx.slice(Math.max(0, idx.length - b.last));
      if (b.random !== undefined) {
        var r = K.rng(b.seed === undefined ? bi * 7919 + 31 : b.seed);
        for (var i = idx.length - 1; i > 0; i--) { var j = Math.floor(r() * (i + 1)), tmp = idx[i]; idx[i] = idx[j]; idx[j] = tmp; }
        idx = idx.slice(0, b.random).sort(function (x, y) { return x - y; });
      }
      return idx.map(function (i) { if (!list[i]) throw new Error("KIT.collage: no copy " + i); return list[i]; });
    }
    var colour = function (c, dflt) { return c === "red" ? RED : c === "ink" ? INK : c || dflt; };
    var POP_KEYS = [[-F, 0], [F, 1.12], [2 * F, 1]], SWAP_KEYS = [[0, 1.15, 0.88], [F, 0.95, 1.05], [2 * F, 1, 1]];
    // The time a move made of copies ends: `until` (a word or seconds) or b.t + dur.
    var endOf = function (b, dflt) { var tu = timeOf(b.until); return tu === Infinity ? b.t + (b.dur === undefined ? dflt : b.dur) : tu; };
    // When copy i of n arrives, faster and faster (accel 1 is even).
    var arrival = function (b, t1, i, n, accel) { return n === 1 ? b.t : b.t + (t1 - b.t) * Math.pow(i / (n - 1), accel); };

    // ── The moves (video/README.md lists each one with its options) ──
    var MOVES = {
      show: function (b, who) { who.forEach(function (n) { ev(n, b.t, true); }); },
      hide: function (b, who) { who.forEach(function (n) { ev(n, b.t, false); }); },
      slideIn: function (b, who) {
        who.forEach(function (n) {
          var a = get(n), d = dir(b.from || "left"), o = b.over === undefined ? 22 : b.over, tilt = b.tilt || 0;
          var dist = b.dist || (d[0] < 0 ? a.left + a.w : d[0] > 0 ? W - a.left : d[1] < 0 ? a.top + a.h : H - a.top) + 60;
          ev(n, b.t, true);
          op(n, function (s, t) {
            var v = keys(b.t, [[0, dist], [4 * F, -o], [5 * F, 0.3 * o], [6 * F, 0]], t)[0];
            s.x += d[0] * v; s.y += d[1] * v;
            s.r += keys(b.t, [[4 * F, 0], [5 * F, tilt], [6 * F, -tilt / 2], [7 * F, 0]], t)[0];
          });
        });
      },
      slideOut: function (b, who) {
        who.forEach(function (n) {
          var a = get(n), d = dir(b.to || "left"), dur = b.dur || 0.42;
          var dist = b.dist || (d[0] < 0 ? a.left + a.w : d[0] > 0 ? W - a.left : d[1] < 0 ? a.top + a.h : H - a.top) + 160;
          ev(n, b.t + dur, false);
          op(n, function (s, t) { var u = clamp((t - b.t) / dur); s.x += d[0] * dist * u * u; s.y += d[1] * dist * u * u; });
        });
      },
      hinge: function (b, who) {
        var a = b.angle === undefined ? 30 : b.angle, fr = (b.frames || 1) * F;
        var Ks = b.hold === undefined ? [[0, 0], [fr, a]] : [[0, 0], [fr, a], [b.hold, a], [b.hold + 2 * F, 0]];
        who.forEach(function (n) { op(n, function (s, t) { s.r += keys(b.t, Ks, t)[0]; }); });
      },
      bow: function (b, who) {
        var a = b.angle === undefined ? 27 : b.angle, h = b.hold === undefined ? 0.62 : b.hold;
        var Ks = [[0, 0], [2 * F, a * 1.15], [3 * F, a], [h, a], [h + 2 * F, -a * 0.11], [h + 3 * F, 0]];
        who.forEach(function (n) { op(n, function (s, t) { s.r += keys(b.t, Ks, t)[0]; }); });
      },
      stamp: function (b, who) {
        if (b.text) {
          var sign = who.length ? get(who[0]) : null, name = b.id || (sign ? sign.name + ".stamp" : "stamp");
          var m = stampMark(name, b, sign), tilt = b.tilt === undefined ? -3 : b.tilt;
          ev(name, b.t - F, true);
          op(name, function (s, t) { var v = keys(b.t, STAMP_KEYS(b.from || 1.9), t)[0]; s.sx *= v; s.sy *= v; s.r += tilt; });
          if (!sign) shakeOp(b.t, 4, 1, b.shake === undefined ? 7 : b.shake);
          return m;
        }
        who.forEach(function (n) { ev(n, b.t - F, true); scaleOp(n, b.t, STAMP_KEYS(b.from || 2.3)); });
        shakeOp(b.t, 4, 1, b.shake === undefined ? 7 : b.shake);
      },
      pop: function (b, who) {
        who.forEach(function (n) {
          if (b.out) { ev(n, b.t + 3 * F, false); scaleOp(n, b.t, [[0, 1], [2 * F, 0.55], [3 * F, 0]]); return; }
          ev(n, b.t - F, true);
          scaleOp(n, b.t, b.squash ? [[-F, 0.25, 0.08], [0, 0.8, 1.18], [F, 1.08, 0.9], [2 * F, 1, 1]] : [[-F, 0], [F, 1.12], [2 * F, 1]]);
          if (b.swell) scaleOp(n, b.t, [[2 * F, 1], [Math.max(D - b.t, 2 * F + 0.01), 1 + b.swell]]);
        });
      },
      swap: function (b, who) {
        who.forEach(function (n) { ev(n, b.t, false); });
        [].concat(b.to).forEach(function (n) { get(n); ev(n, b.t, true); scaleOp(n, b.t, [[0, 1.15, 0.88], [F, 0.95, 1.05], [2 * F, 1, 1]]); });
      },
      shiver: function (b, who, bi) {
        var dur = b.dur || 0.75, amp = b.amp === undefined ? 8 : b.amp, rot = b.rot === undefined ? 4 : b.rot;
        who.forEach(function (n, i) {
          op(n, function (s, t) {
            if (t < b.t || t >= b.t + dur) return;
            var r = K.rng(Math.round(t * 12) * 7919 + 13 + bi * 101 + i * 7);
            s.x += (r() - 0.5) * 2 * amp; s.r += (r() - 0.5) * 2 * rot;
          });
        });
      },
      bob: function (b, who) {
        var fade = b.fade === undefined ? 0.4 : b.fade, tu = timeOf(b.until), sp = b.speed || 1;
        var y = b.y === undefined ? 6 : b.y, rr = b.r === undefined ? 2 : b.r;
        who.forEach(function (n, i) {
          var ph = (b.phase || 0) + i * 1.7;
          op(n, function (s, t) {
            if (t < b.t) return;
            var f = (b.t > 0 && fade ? smooth((t - b.t) / fade) : 1) * (tu === Infinity ? 1 : fade ? 1 - smooth((t - tu) / fade) : t < tu ? 1 : 0);
            s.y += y * Math.sin(t * 3.1 * sp + ph) * f; s.r += rr * Math.sin(t * 2.2 * sp + ph) * f;
          });
        });
      },
      move: function (b, who) {
        var dur = b.dur || 4 * F, by = b.by || [0, 0];
        who.forEach(function (n) {
          var a = get(n), c = a.home();
          op(n, function (s, t) {
            if (t < b.t) return;
            var u = clamp((t - b.t) / dur), e = b.ease === "smooth" ? smooth(u) : u;
            var tx, ty;
            if (b.to === undefined) { tx = s.x + by[0]; ty = s.y + by[1]; } else { var p = target(b.to, t); tx = p[0] + by[0] - c[0]; ty = p[1] + by[1] - c[1]; }
            s.x += (tx - s.x) * e; s.y += (ty - s.y) * e - Math.sin(Math.PI * u) * (b.arc || 0);
            s.r += ((b.turn || 0) - s.r) * e;
            if (b.scale !== undefined) { s.sx += (b.scale - s.sx) * e; s.sy += (b.scale - s.sy) * e; }
          });
        });
      },
      nudge: function (b, who) {
        var by = b.by || [40, 0];
        who.forEach(function (n) {
          var f = get(n).faces;
          op(n, function (s, t) { var v = keys(b.t, [[0, 0], [F, 1], [4 * F, 0]], t)[0]; s.x += f * by[0] * v; s.y += by[1] * v; });
        });
      },
      hop: function (b, who) {
        var h = b.height === undefined ? 34 : b.height;
        who.forEach(function (n) { op(n, function (s, t) { s.y -= h * keys(b.t, [[0, 0], [F, 1], [3 * F, 0]], t)[0]; }); });
      },
      drop: function (b, who) {
        var dur = b.dur || 0.6, dist = b.dist || 1250, drift = b.drift || 0, spin = b.spin === undefined ? 30 : b.spin;
        who.forEach(function (n) {
          ev(n, b.t + dur, false);
          op(n, function (s, t) { var u = clamp((t - b.t) / dur); s.x += drift * u; s.y += dist * u * u; s.r += spin * u; });
        });
      },
      split: function (b, who) {
        var gap = b.gap === undefined ? 300 : b.gap, spin = b.spin === undefined ? 14 : b.spin;
        who.forEach(function (n) {
          var a = get(n);
          if (!a.cutPieces) throw new Error("KIT.collage: split needs cut: \"lr\" or \"tb\" on '" + n + "'");
          ev(n, b.t, false);
          a.cutPieces.forEach(function (pn, i) {
            var side = i ? 1 : -1, lr = a.cutAxis === "lr";
            ev(pn, b.t, true);
            op(pn, function (s, t) {
              if (t < b.t) return;
              var w = stateOf(n, b.t), k = keys(b.t, [[0, 0, 0, 0], [2 * F, 1.1 * gap, -40, spin * 1.857], [3 * F, 1.007 * gap, -22, spin * 1.143], [5 * F, gap, 16, spin]], t);
              s.x = w.x + (lr ? side * k[0] : k[1]); s.y = w.y + (lr ? k[1] : side * k[0]); s.r = w.r + side * k[2]; s.sx = w.sx; s.sy = w.sy;
            });
          });
        });
        shakeOp(b.t, 4, 0, b.shake === undefined ? 9 : b.shake);
      },
      shake: function (b) {
        shakeOp(b.t, b.frames || 4, 0, b.x || 0);
        shakeOp(b.t, b.frames || 4, 1, b.y === undefined && !b.x ? 8 : b.y || 0);
      },
      boom: function (b, who, bi) {
        var amp = b.shake === undefined ? 16 : b.shake, fl = b.flash === undefined ? 0.25 : b.flash;
        shakes.push(function (t, fr, sh) {
          if (t < b.t) return;
          var r = K.rng(fr * 104729 + 7 + bi), a = amp * Math.max(0, 1 - (t - b.t) / 0.6);
          sh[0] += (r() - 0.5) * 2 * a; sh[1] += (r() - 0.5) * 2 * a;
        });
        tickers.push(function (t) { var o = t >= b.t && fl ? Math.max(0, 1 - (t - b.t) / fl) : 0; vis(flashEl, o > 0); flashEl.style.opacity = o.toFixed(2); });
      },
      glow: function (b, who) {
        var dur = b.dur || 0.9, size = b.size || 220;
        who.forEach(function (n, i) {
          var a = get(n), gid = ID + "-" + n + "-glow" + b.i;
          a.before += '<div id="' + gid + '" class="cg-ab" style="left:' + px(-size / 2) + ";top:" + px(-size / 2) + ";width:" + size + "px;height:" + size + 'px;transform-origin:50% 50%;visibility:hidden;' +
            'border-radius:50%;background:radial-gradient(circle, rgba(255,246,200,0.95) 0, rgba(255,214,90,0.6) 38%, rgba(255,214,90,0) 70%)"></div>';
          tickers.push(function (t) {
            var el = document.getElementById(gid), g = clamp((t - b.t) / dur), on = shown(n, t) && g > 0, c = pointOf(n, null, t);
            vis(el, on);
            put(el, c[0], c[1], 0, (0.6 + 1.2 * g) * (1 + 0.12 * Math.sin(t * 23 + i)));
            el.style.opacity = g.toFixed(2);
          });
        });
      },
      sparks: function (b, who, bi) {
        if (who.length !== 2) throw new Error("KIT.collage: sparks needs who: [a, b]");
        var tu = timeOf(b.until);
        tickers.push(function (t, fr) {
          if (t < b.t || t >= tu || !shown(who[0], t) || !shown(who[1], t)) return;
          var r = K.rng(fr * 104729 + 7 + bi), P = who.map(function (n) { return pointOf(n, null, t); });
          var meet = [(P[0][0] + P[1][0]) / 2, (P[0][1] + P[1][1]) / 2 - 20];
          P.forEach(function (a) {
            var d = "M" + a[0].toFixed(0) + "," + a[1].toFixed(0);
            for (var j = 1; j <= 7; j++) { var v = j / 7; d += " L" + (a[0] + (meet[0] - a[0]) * v).toFixed(0) + "," + (a[1] + (meet[1] - a[1]) * v + (j < 7 ? (r() - 0.5) * 70 : 0)).toFixed(0); }
            bolts += '<path d="' + d + '" fill="none" stroke="#F2B230" stroke-width="16" stroke-linejoin="round" opacity="0.85"/><path d="' + d + '" fill="none" stroke="#FFF8D8" stroke-width="6" stroke-linejoin="round"/>';
          });
        });
      },
      char: function (b, who) { who.forEach(function (n) { var a = get(n); a.charT = Math.min(a.charT === undefined ? Infinity : a.charT, b.t); }); },
      blink: function (b, who) { who.forEach(function (n) { var a = get(n); (a.blinks = a.blinks || []).push(b.t); }); },
      ash: function (b, who) {
        var Ks = [[0, 1, 1], [F, 1.04, 0.82], [2 * F, 1.12, 0.55], [3 * F, 1.22, 0.3], [4 * F, 1.3, 0.17], [5 * F, 1.26, 0.23], [6 * F, 1.28, 0.2]];
        who.forEach(function (n) { scaleOp(n, b.t, Ks); });
      },
      sunburst: function (b) {
        var name = b.id || "sunburst", r = b.r || 1300, x = b.x === undefined ? W / 2 : b.x, y = b.y === undefined ? H / 2 : b.y, glow = b.glow !== false;
        var a = actor(name, { w: 2 * r, h: 2 * r, pivot: [r, r], points: {}, eyes: [], smoke: [], faces: 1, hidden: true });
        a.left = x - r; a.top = y - r;
        a.html = function () {
          return box(a, sunburstSvg(r), "visibility:hidden;opacity:0.9") + (glow ? '<div id="' + ID + "-" + name + '-glow" class="cg-ab" style="left:' + px(x - 400) + ";top:" + px(y - 320) +
            ';width:800px;height:640px;transform-origin:50% 50%;visibility:hidden;background:radial-gradient(ellipse at 50% 50%, rgba(255,240,170,0.95) 0, rgba(255,226,120,0.55) 35%, rgba(255,220,110,0) 70%)"></div>' : "");
        };
        back.push(name);
        ev(name, b.enter === "none" ? b.t : b.t - F, true);
        if (b.enter !== "none") scaleOp(name, b.t, [[-F, 0], [F, 1.12], [2 * F, 1]]);
        op(name, function (s, t) { s.r += (b.angle || 0) + Math.round(t * 12) * 1.6; });
        if (glow) tickers.push(function (t) { var g = q(name + "-glow"); vis(g, shown(name, t)); put(g, a.s.x, a.s.y, 0, a.s.sx * (1 + 0.04 * Math.sin(t * 9))); });
      },
      banner: function (b) {
        var name = b.id || "banner";
        card(name, b);
        front.push(name);
        ev(name, b.t - F, true);
        op(name, function (s, t) { var v = keys(b.t, STAMP_KEYS(b.from || 2.3), t)[0]; s.sx *= v; s.sy *= v; s.r += b.tilt === undefined ? -2 : b.tilt; });
        shakeOp(b.t, 4, 1, b.shake === undefined ? 7 : b.shake);
      },
      tag: function (b, who) {
        var name = b.id || "tag", on = who[0];
        if (!on) throw new Error("KIT.collage: tag needs who (the cut-out it hangs on)");
        var a = tagSign(name, b, on), knot = b.knot || null, swing = b.swing === undefined ? 3 : b.swing;
        if (b.under) (unders[b.under] = unders[b.under] || []).push(name); else front.push(name);
        ev(name, b.t - F, true);
        scaleOp(name, b.t, [[-F, 0], [F, 1.12], [2 * F, 1]]);
        op(name, function (s, t) { s.r += swing * Math.sin(t * 2.4); });
        tickers.push(function (t) {
          var str = q(name + "-string"), k = pointOf(on, knot, t), hx = a.left + a.pivot[0], hy = a.top + a.pivot[1];
          vis(str, shown(name, t) && shown(on, t) && t >= b.t + F);
          str.firstChild.setAttribute("d", "M" + k[0].toFixed(1) + "," + k[1].toFixed(1) + " Q" + ((k[0] + hx) / 2).toFixed(1) + "," + (Math.max(k[1], hy) + 40).toFixed(1) + " " + hx.toFixed(1) + "," + hy.toFixed(1));
        });
      },
      flatten: function (b, who) {
        who.forEach(function (n) { scaleOp(n, b.t, [[0, 1, 1], [F, 1.12, 0.4], [2 * F, 1.3, 0.12]]); });
      },
      // Charts: axes on the paper, a dashed rule at a value, and a chain of cut-outs that draws the line.
      chart: function (b) {
        var c = b.chart, name = b.id || "chart";
        if (!c || !c.pt) throw new Error("KIT.collage: chart needs chart: KIT.collage.axes({...})");
        var a = actor(name, { w: W, h: H, pivot: [W / 2, H / 2], points: {}, eyes: [], smoke: [], faces: 1, hidden: true });
        a.left = 0; a.top = 0;
        a.html = function () { return box(a, axesSvg(c, W, H), "visibility:hidden"); };
        back.push(name);
        if (b.enter) MOVES.slideIn({ t: b.t, from: b.enter, over: b.over === undefined ? 14 : b.over, dist: H + 60 }, [name]);
        else ev(name, b.t, true);
      },
      rule: function (b) {
        var c = b.chart, name = b.id || "rule", col = b.color === "ink" ? INK : RED, size = b.size || 32, dur = b.dur === undefined ? 0.5 : b.dur;
        var y = c.pt(c.x[0], b.y)[1], x0 = b.from === undefined ? c.box[0] : c.pt(b.from, 0)[0], x1 = b.to === undefined ? c.box[2] : c.pt(b.to, 0)[0];
        var a = actor(name, { w: x1 - x0, h: 6, pivot: [0, 3], points: {}, eyes: [], smoke: [], faces: 1, hidden: true });
        a.left = x0; a.top = y - 3;
        a.html = function () {
          return box(a, '<div class="cg-full" style="border-top:6px dashed ' + col + '"></div>' + (b.text ? '<div class="cg-ab" style="' + (b.labelAt === "left" ? "left:0" : "right:0") +
            (b.below ? ";top:20px" : ";bottom:16px") + ";font:600 " + px(size) + "/1 Oswald;color:" + col + ';white-space:nowrap;letter-spacing:1px">' + b.text + "</div>" : ""), "visibility:hidden;clip-path:inset(-300px 100% -300px -20px)");
        };
        back.push(name);
        ev(name, b.t, true);
        tickers.push(function (t) { var u = dur ? clamp((t - b.t) / dur) : 1; q(name).style.clipPath = "inset(-300px " + ((1 - u) * 100).toFixed(1) + "% -300px -20px)"; });
      },
      chain: function (b, who, bi) {
        var name = b.id || "chain", pts = b.points, c = b.chart, k = b.scale || 1, arts = [].concat(b.art), jig = b.jiggle === undefined ? 2 : b.jiggle;
        if (!pts) {
          if (!c || !b.f || !b.x) throw new Error("KIT.collage: chain needs points, or chart, f (y of x) and x: [from, to]");
          var step = b.step || 0.5, m = Math.round((b.x[1] - b.x[0]) / step);
          pts = [];
          for (var j = 0; j <= m; j++) { var xv = b.x[0] + j * step; pts.push(c.pt(xv, b.f(xv))); }
        }
        var n = pts.length, tu = timeOf(b.until), t1 = tu === Infinity ? b.t + (b.dur || 2) : tu, accel = b.accel === undefined ? 0.6 : b.accel;
        var join = b.join ? chains[b.join] : null, names = [];
        if (b.join && !join) throw new Error("KIT.collage: no chain '" + b.join + "' to join");
        pts.forEach(function (p, i) {
          var nm = name + "." + i, ti = n === 1 ? b.t : b.t + (t1 - b.t) * Math.pow(i / (n - 1), accel);
          var art = b.pose ? b.pose(i, n) : arts[i % arts.length], sz = SIZES[art];
          if (!sz) throw new Error("KIT.collage: no size for art '" + art + "'");
          cutout(nm, { art: art, x: p[0], y: p[1], anchor: b.anchor || "bottom", pivot: "bottom", scale: b.height ? b.height * ((b.sizes || {})[art] || 1) / sz[1] : k, hidden: true, faces: b.faces });
          cast.push(nm); names.push(nm);
          ev(nm, ti - F, true);
          var from = i ? pts[i - 1] : join ? join.pts[join.pts.length - 1] : null;
          if (from && b.hop !== false) {
            // it pops out of the one before and hops to its place
            var dx = from[0] - p[0], dy = from[1] - p[1];
            op(nm, function (s, t) { var v = keys(ti, [[-F, dx, dy, 0.6], [F, dx * 0.4, dy * 0.4 - 30, 1.06], [2 * F, 0, 0, 1]], t); s.x += v[0]; s.y += v[1]; s.sx *= v[2]; s.sy *= v[2]; });
          } else scaleOp(nm, ti, [[-F, 0], [F, 1.12], [2 * F, 1]]);
          if (jig) op(nm, function (s, t) {
            if (t < ti + 2 * F) return;
            var r = K.rng(Math.round(t * 12) * 31 + i * 977 + bi * 13);
            s.y += (r() - 0.5) * 2 * jig; s.r += (r() - 0.5) * 1.6 * jig;
          });
        });
        chains[name] = { pts: pts, names: names };
        groups[name] = names;
        if (b.line === false) return;
        var ln = name + "-line", lpts = (join ? [join.pts[join.pts.length - 1]] : []).concat(pts), lnames = (join ? [join.names[join.names.length - 1]] : []).concat(names);
        var la = actor(ln, { w: W, h: H, pivot: [W / 2, H / 2], points: {}, eyes: [], smoke: [], faces: 1 });
        la.left = 0; la.top = 0;
        la.html = function () {
          return box(la, '<svg class="cg-full" width="' + W + '" height="' + H + '"><path d="" fill="none" stroke="' + (b.lineColor === "red" ? RED : b.lineColor || INK) + '" stroke-width="' + (b.lineWidth || 5) + '" stroke-linejoin="round" stroke-linecap="round"/></svg>');
        };
        back.push(ln);
        tickers.push(function (t) {
          var d = "";
          lnames.forEach(function (nm, i) { if (shown(nm, t)) d += (d ? " L" : "M") + lpts[i][0].toFixed(1) + "," + lpts[i][1].toFixed(1); });
          q(ln).querySelector("path").setAttribute("d", d);
        });
      },
      // A bar on a chart: a hatched bar at x (data) that grows from its last height to `to` over dur; call again with
      // the same id to grow or shrink it again. It may run off the plate.
      bar: function (b) {
        var c = b.chart, name = b.id || "bar", dur = b.dur === undefined ? 0.6 : b.dur, a = A[name];
        if (!a) {
          if (!c || !c.pt) throw new Error("KIT.collage: bar needs chart");
          var w = b.width || 80, x = c.pt(b.x, 0)[0], base = c.box[3], size = b.size || 30;
          a = actor(name, { w: w, h: 1, pivot: [w / 2, 0], points: {}, eyes: [], smoke: [], faces: 1, hidden: true });
          a.left = x - w / 2; a.top = 0; a.keys = [[-1e9, 0]];
          a.html = function () {
            return '<div id="' + ID + "-" + name + '" class="cg-ab" style="left:' + px(a.left) + ";top:0;width:" + px(w) + ";height:" + H + 'px;visibility:hidden">' +
              '<div class="cg-ab cg-sh cg-barbody" style="left:0;width:100%;background-color:' + (b.fill || "#E9D9AE") + ";border:5px solid " + INK + ';box-sizing:border-box;' +
              'background-image:repeating-linear-gradient(135deg, rgba(43,32,51,0.18) 0 2px, transparent 2px 9px)"></div>' +
              (b.text ? '<div class="cg-ab cg-barlabel" style="left:-80px;right:-80px;text-align:center;font:600 ' + px(size) + "/1 Oswald;color:" + INK + ';white-space:nowrap">' + b.text + "</div>" : "") + "</div>";
          };
          back.push(name);
          ev(name, b.t, true);
          tickers.push(function (t) {
            var v = keys(0, a.keys, t)[0], top = c.pt(c.x[0], v)[1], el = q(name);
            var body = el.querySelector(".cg-barbody"), lab = el.querySelector(".cg-barlabel");
            body.style.top = px(Math.min(top, base)); body.style.height = px(Math.abs(base - top));
            if (lab) lab.style.top = px(top - size - 14);
          });
        }
        var from = keys(0, a.keys, b.t)[0];
        a.keys.push([b.t, from], [b.t + dur, b.to]);
      },
      // A flat colour over the plate that fades to `opacity` over dur: behind the whole cast, or just above the cast
      // member `above` (the cast written after it keeps its colour). blend "saturation" greys what is under it;
      // "normal" tints. Call again with the same id to change it.
      wash: function (b) {
        var name = b.id || "wash", dur = b.dur === undefined ? 0.8 : b.dur, a = A[name];
        if (!a) {
          a = actor(name, { w: W, h: H, pivot: [W / 2, H / 2], points: {}, eyes: [], smoke: [], faces: 1, hidden: true });
          a.left = 0; a.top = 0; a.keys = [[-1e9, 0]];
          a.html = function () {
            return '<div id="' + ID + "-" + name + '" ' + plateBox + "background:" + (b.color || "#888") + ";mix-blend-mode:" + (b.blend || "saturation") + ';opacity:0;visibility:hidden;pointer-events:none"></div>';
          };
          if (b.above) (afters[b.above] = afters[b.above] || []).push(name); else back.push(name);
          ev(name, b.t, true);
          tickers.push(function (t) { q(name).style.opacity = keys(0, a.keys, t)[0].toFixed(3); });
        }
        var from = keys(0, a.keys, b.t)[0];
        a.keys.push([b.t, from], [b.t + dur, b.opacity === undefined ? 1 : b.opacity]);
      },
      camera: function (b) { cams.push(b); },

      // A line that draws itself from its first point to its last over dur (or until): on a chart (f of x over x, or
      // points as data [x, y]) it advances at an even pace along x; free (points in canvas px) along its length. It may
      // run off the plate. `rider` (a cast member) rides its tip, its anchor on the line, tilting with the slope.
      line: function (b) {
        var name = b.id || "line", c = b.chart, pts = b.points;
        if (!pts) {
          if (!c || !b.f || !b.x) throw new Error("KIT.collage: line needs points, or chart, f (y of x) and x: [from, to]");
          var m = b.samples || 96;
          pts = [];
          for (var j = 0; j <= m; j++) { var xv = b.x[0] + (b.x[1] - b.x[0]) * j / m; pts.push(c.pt(xv, b.f(xv))); }
        } else if (c) pts = pts.map(function (p) { return c.pt(p[0], p[1]); });
        var tr = track(pts, false), byX = b.by ? b.by === "x" : !!c, t1 = endOf(b, 2), X0 = pts[0][0], X1 = pts[pts.length - 1][0];
        var prog = function (t) {
          var u = t1 > b.t ? clamp((t - b.t) / (t1 - b.t)) : t >= b.t ? 1 : 0;
          if (b.ease === "smooth") u = smooth(u);
          return byX ? tr.lenAtX(X0 + (X1 - X0) * u) : tr.L * u;
        };
        var a = actor(name, { w: W, h: H, pivot: [W / 2, H / 2], points: {}, eyes: [], smoke: [], faces: 1, hidden: true });
        a.left = 0; a.top = 0;
        a.html = function () {
          return box(a, '<svg class="cg-full" width="' + W + '" height="' + H + '" style="overflow:visible"><path d="" fill="none" stroke="' + colour(b.color, INK) + '" stroke-width="' + (b.width || 6) +
            '" stroke-linejoin="round" stroke-linecap="round"' + (b.dash ? ' stroke-dasharray="' + [].concat(b.dash).join(" ") + '"' : "") + "/></svg>", "visibility:hidden");
        };
        (b.front ? front : back).push(name);
        ev(name, b.t, true);
        tickers.push(function (t) { q(name).querySelector("path").setAttribute("d", tr.d(prog(t))); });
        if (b.rider) {
          var rd = get(b.rider), tilt = b.tilt === undefined ? 1 : b.tilt;
          ev(b.rider, b.t, true);
          op(b.rider, function (s, t) { if (t < b.t) return; var p = tr.at(prog(t)); s.r += p[2] * tilt; placeAt(rd, s, p); });
        }
      },
      // Copies of a cut-out fall onto a spot and stack, faster and faster, to `count` or `tall` (canvas px high), or on a
      // chart to the value `to` at data x. `heap` (copies in the bottom row) piles them into a heap instead of a column.
      pile: function (b, who, bi) {
        var name = b.id || "pile", arts = [].concat(b.art), c = b.chart, art0 = arts[0], k0 = fitScale(b, art0);
        var x = c ? c.pt(b.x, 0)[0] : b.x === undefined ? W / 2 : b.x, y = c ? c.box[3] : b.y === undefined ? H - 60 : b.y;
        var ch = SIZES[art0][1] * k0, cw = SIZES[art0][0] * k0, heap = b.heap || 0, gap = b.gap || ch * (heap ? 0.6 : 0.85), spread = b.spread || cw * 0.9;
        var height = c && b.to !== undefined ? y - c.pt(b.x, b.to)[1] : b.tall, n = b.count;
        if (!n) {
          if (!height) throw new Error("KIT.collage: pile needs count, tall, or chart and to");
          n = Math.max(1, Math.round((height - ch) / gap) + 1);
        }
        var t1 = endOf(b, 2), accel = b.accel === undefined ? 0.6 : b.accel, fall = b.fall || 4 * F, jit = b.jitter === undefined ? 6 : b.jitter, tilt = b.tilt === undefined ? 3 : b.tilt;
        var names = [], row = 0, col = 0;
        for (var i = 0; i < n; i++) {
          var rowLen = heap ? Math.max(1, heap - row) : 1, xi = x + (heap ? (col - (rowLen - 1) / 2) * spread : 0), yi = y - row * gap;
          var r = K.rng(bi * 7919 + i * 104729 + 17), dx = (r() - 0.5) * 2 * jit, rot = (r() - 0.5) * 2 * tilt;
          var art = arts[i % arts.length], nm = name + "." + i, ti = arrival(b, t1, i, n, accel), dist = b.dist || Math.max(500, yi + 60);
          copy(nm, art, xi + dx, yi, b, { scale: fitScale(b, art) });
          names.push(nm);
          ev(nm, ti - fall, true);
          (function (ti, dist, rot) {
            op(nm, function (s, t) { if (t < ti - fall) return; var u = clamp((t - ti + fall) / fall); s.y -= dist * (1 - u * u); s.r += rot; });
          })(ti, dist, rot);
          scaleOp(nm, ti, [[0, 1, 1], [F, 1.1, 0.86], [2 * F, 0.97, 1.04], [3 * F, 1, 1]]);
          if (++col >= rowLen) { col = 0; row++; }
        }
        groups[name] = names;
      },
      // A number on a card that rolls (an odometer) or ticks from `from` to `to` over dur, or at `rate` a second. The
      // same id again runs it on from where it is. Formatted with prefix, suffix, decimals and commas.
      counter: function (b, who) {
        var name = b.id || "counter", a = A[name];
        if (!a) {
          var sign = who.length ? get(who[0]) : null, size = b.size || 120, fam = b.font === "oswald" ? "Oswald" : "Fraunces", wt = fam === "Oswald" ? 600 : 900;
          var fm = { pre: b.prefix || "", suf: b.suffix || "", dec: b.decimals || 0, commas: b.commas !== false }, roll = b.style !== "tick", plain = b.card === false;
          var tw = function (s) { return s ? K.textWidth(s, size, fam, wt) : 0; };
          var chW = Math.max.apply(null, "0123456789".split("").map(tw)), lh = size * 1.2;
          var units = function (v) { return Math.round(Math.abs(v) * Math.pow(10, fm.dec) * 1e6) / 1e6; };
          var intDigits = function (v) { var n = Math.floor(units(v) / Math.pow(10, fm.dec) + 1e-9); return n < 1 ? 1 : Math.floor(Math.log10(n) + 1e-9) + 1; };
          var fmt = function (v) {
            var s = (Math.round(Math.abs(v) * Math.pow(10, fm.dec)) / Math.pow(10, fm.dec)).toFixed(fm.dec), p = s.split(".");
            if (fm.commas) p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            return (v < 0 && Number(s) > 0 ? "-" : "") + fm.pre + p.join(".") + fm.suf;
          };
          // the width of the number laid out in digit columns
          var rollW = function (v) {
            var n = intDigits(v), w = tw(fm.pre) + tw(fm.suf) + (n + fm.dec) * chW + (fm.dec ? tw(".") : 0) + (fm.commas ? Math.floor((n - 1) / 3) * tw(",") : 0);
            return w + (v < 0 && units(v) > 0 ? tw("-") : 0);
          };
          var first = [b.from || 0, b.to === undefined ? b.from || 0 : b.to];
          var cw = b.width || Math.max.apply(null, first.map(function (v) { return roll ? rollW(v) : tw(fmt(v)); })) + (b.pad === undefined ? (plain ? 0 : 90) : b.pad), chh = size * 1.3;
          a = actor(name, { w: cw, h: chh, pivot: [cw / 2, chh / 2], points: {}, eyes: [], smoke: [], faces: 1, hidden: true });
          a.segs = []; a.v0 = b.from || 0;
          a.val = function (t) {
            var v = a.v0;
            a.segs.forEach(function (sg) { if (t < sg.t0) return; var u = sg.t1 > sg.t0 ? clamp((t - sg.t0) / (sg.t1 - sg.t0)) : 1; v = sg.v0 + (sg.v1 - sg.v0) * (sg.ease === "smooth" ? smooth(u) : u); });
            return v;
          };
          if (sign) {
            var onArt = sign.o;
            if (!b.spot) throw new Error("KIT.collage: a counter on '" + sign.name + "' needs spot: [x, y] (art px, or the sign's px)");
            a.left = b.spot[0] * (onArt ? sign.k : 1) - cw / 2; a.top = b.spot[1] * (onArt ? sign.k : 1) - chh / 2;
            sign.children.push(name); a.inside = true;
          } else {
            a.left = (b.x === undefined ? W / 2 : b.x) - cw / 2; a.top = (b.y === undefined ? H / 2 : b.y) - chh / 2;
            front.push(name);
          }
          var col = colour(b.color, INK), bc = b.border === "ink" ? INK : RED, top = (chh - lh) / 2;
          var glyph = function (cls, s, extra) { return '<div class="cg-ab ' + cls + '" style="top:' + px(top) + ";height:" + px(lh) + ";font:" + wt + " " + px(size) + "/" + px(lh) + " " + fam + ";color:" + col + ";white-space:nowrap" + (extra || "") + '">' + s + "</div>"; };
          a.html = function () {
            var inner = "";
            if (roll) {
              // enough digit columns for the biggest number it reaches
              var nInt = Math.max.apply(null, [a.v0].concat(a.segs.map(function (sg) { return sg.v1; })).map(intDigits)), strip = [];
              for (var d = 0; d <= 10; d++) strip.push(d % 10);
              inner += glyph("cg-cn-neg", "-") + glyph("cg-cn-pre", fm.pre) + glyph("cg-cn-suf", fm.suf) + (fm.dec ? glyph("cg-cn-dot", ".") : "");
              for (var p = nInt - 1; p >= -fm.dec; p--) {
                inner += '<div class="cg-ab cg-cn-col" data-p="' + p + '" style="top:' + px(top) + ";width:" + px(chW) + ";height:" + px(lh) + ';overflow:hidden">' +
                  '<div class="cg-ab" style="left:0;top:0;width:100%;text-align:center;font:' + wt + " " + px(size) + "/" + px(lh) + " " + fam + ";color:" + col + '">' + strip.join("<br>") + "</div></div>";
                if (fm.commas && p > 0 && p % 3 === 0) inner += glyph("cg-cn-com", ",", '" data-p="' + p);
              }
            } else inner = glyph("cg-cn-txt", "", ";left:0;width:100%;text-align:center");
            var card = plain ? "" : '<div class="cg-full" style="background:' + CARD + ";border:5px solid " + bc + ";box-shadow:inset 0 0 0 8px " + CARD + ",inset 0 0 0 11px " + bc + '"></div>';
            return box(a, '<div class="cg-full cg-sh">' + card + inner + "</div>", "visibility:hidden");
          };
          var els = null;
          tickers.push(function (t) {
            var v = a.val(t), el = q(name);
            if (!roll) { el.querySelector(".cg-cn-txt").textContent = fmt(v); return; }
            if (!els) {
              els = { neg: el.querySelector(".cg-cn-neg"), pre: el.querySelector(".cg-cn-pre"), suf: el.querySelector(".cg-cn-suf"), dot: el.querySelector(".cg-cn-dot"), cols: [], coms: {} };
              Array.prototype.forEach.call(el.querySelectorAll(".cg-cn-col"), function (e) { els.cols.push(e); });
              Array.prototype.forEach.call(el.querySelectorAll(".cg-cn-com"), function (e) { els.coms[e.getAttribute("data-p")] = e; });
            }
            var x = units(v), n = intDigits(v), parts = [];
            if (v < 0 && x > 0) parts.push([els.neg, tw("-")]); else vis(els.neg, false);
            parts.push([els.pre, tw(fm.pre)]);
            els.cols.forEach(function (e) {
              var key = e.getAttribute("data-p"), p = Number(key);
              if (p >= n) { vis(e, false); if (els.coms[key]) vis(els.coms[key], false); return; }
              // the lowest column turns smoothly; each higher one turns while the one below goes from 9 to 0
              var yv = x / Math.pow(10, p + fm.dec), dg = Math.floor(yv + 1e-9), r = yv - dg, pos = (dg % 10) + (p === -fm.dec ? (r < 1e-6 ? 0 : r) : r > 0.9 ? (r - 0.9) * 10 : 0);
              e.firstChild.style.transform = "translateY(" + px(-(pos % 10) * lh) + ")";
              parts.push([e, chW]);
              if (els.coms[key]) parts.push([els.coms[key], tw(",")]);
              if (p === 0 && els.dot) parts.push([els.dot, tw(".")]);
            });
            parts.push([els.suf, tw(fm.suf)]);
            var total = parts.reduce(function (s, pp) { return s + pp[1]; }, 0), left = (cw - total) / 2;
            parts.forEach(function (pp) { vis(pp[0], true); pp[0].style.left = px(left); left += pp[1]; });
          });
          if (b.enter === "none") ev(name, b.t, true); else { ev(name, b.t - F, true); scaleOp(name, b.t, POP_KEYS); }
        }
        if (b.to === undefined) return;
        var v0 = b.from !== undefined && a.segs.length ? b.from : a.val(b.t), t1 = b.rate ? b.t + Math.abs(b.to - v0) / b.rate : endOf(b, 1);
        a.segs.push({ t0: b.t, t1: t1, v0: v0, v1: b.to, ease: b.ease });
        a.segs.sort(function (p, r) { return p.t0 - r.t0; });
      },
      // The x-ray: a flash, `frames` drawings flickering between the cut-out and its skeleton, and it stays the skeleton.
      // The skeleton is `to` (cast names, one per who) or made from the art + "-skeleton" (or `art`), the same height
      // on the same feet; it moves with the cut-out. `stagger` s between them; `back: true` turns it back.
      xray: function (b, who, bi) {
        who = pickOf(b, who, bi);
        var st = b.stagger || 0, fr = b.frames === undefined ? 4 : b.frames, fl = b.flash === undefined ? 0.25 : b.flash, tos = b.to === undefined ? null : [].concat(b.to);
        who.forEach(function (n, i) {
          var a = get(n), t = b.t + i * st, sk = b.back ? a.bones : tos ? tos[i] : a.bones;
          if (b.back && !sk) throw new Error("KIT.collage: xray back on '" + n + "' needs an xray before it");
          if (!sk) {
            var art = b.art || (a.o && a.o.art + "-skeleton"), sz = SIZES[art];
            if (!sz) throw new Error("KIT.collage: no skeleton art '" + art + "' for '" + n + "' (give xray to: or art:)");
            var k = a.h / sz[1], bx = a.left + a.w / 2, by = a.top + a.h, l = bx - sz[0] * k / 2, tp = by - sz[1] * k;
            sk = n + ".bones";
            cutout(sk, { art: art, x: bx, y: by, anchor: "bottom", pivot: [(a.left + a.pivot[0] - l) / k, (a.top + a.pivot[1] - tp) / k], scale: k, hidden: true, faces: a.o && a.o.faces });
            (afters[n] = afters[n] || []).push(sk);
          } else get(sk);
          if (a.bones !== sk && b.follow !== false) {
            // the skeleton goes where the cut-out goes
            op(sk, function (s, tt) { var w = stateOf(n, tt); s.x += w.x; s.y += w.y; s.r += w.r; s.sx *= w.sx; s.sy *= w.sy; });
          }
          a.bones = sk;
          var on = b.back ? n : sk, off = b.back ? sk : n;
          for (var j = 0; j < fr; j++) { ev(on, t + j * F, j % 2 === 0); ev(off, t + j * F, j % 2 === 1); }
          ev(on, t + fr * F, true); ev(off, t + fr * F, false);
        });
        if (fl) xflashes.push([b.t, fl]);
      },
      // Copies of a cut-out walk a path (canvas px) in single file at `speed`, `gap` apart, each popping in at its start
      // and bobbing on its own beat (by seed). At the end they stop nose to tail ("stop"), vanish ("hide") or, on a
      // `closed` path, go round ("loop"). They face the way they walk.
      march: function (b, who, bi) {
        var name = b.id || "march", arts = [].concat(b.art), n = b.count || 5, closed = !!b.closed, tr = track(b.path, closed);
        var sp = b.speed || 220, end = b.end || (closed ? "loop" : "stop"), tu = timeOf(b.until), k0 = fitScale(b, arts[0]);
        var gap = b.gap || SIZES[arts[0]][0] * k0 * 1.3, bobY = b.bob === undefined ? 8 : b.bob, rock = b.rock === undefined ? 3 : b.rock, steps = b.steps || 2.2, turn = b.turn !== false;
        var names = [], p0 = tr.at(0);
        for (var i = 0; i < n; i++) {
          var art = b.pose ? b.pose(i, n) : arts[i % arts.length], nm = name + "." + i, r = K.rng(bi * 7919 + i * 104729 + 3);
          var a = copy(nm, art, p0[0], p0[1], b), t0 = b.t + i * gap / sp;
          names.push(nm);
          ev(nm, t0, true);
          if (end === "hide") ev(nm, b.t + (tr.L + i * gap) / sp, false);
          (function (a, i, ph, rate, t0) {
            op(nm, function (s, t) {
              var raw = (Math.min(t, tu) - b.t) * sp - i * gap, stopAt = tr.L - i * gap, d = raw < 0 ? 0 : end === "stop" ? Math.min(raw, Math.max(0, stopAt)) : raw;
              var p = tr.at(d), walking = t >= t0 && t < tu && (end !== "stop" || raw < stopAt), w = (t - t0) * rate * Math.PI + ph;
              if (turn && Math.cos(p[2] * Math.PI / 180) * a.faces < -1e-6) s.sx = -s.sx;
              if (walking) s.r += rock * Math.sin(w);
              placeAt(a, s, p);
              if (walking) s.y -= bobY * Math.abs(Math.sin(w));
            });
          })(a, i, r() * 2 * Math.PI, steps * (0.85 + 0.3 * r()), t0);
          scaleOp(nm, t0, [[0, 0.4], [F, 1.1], [2 * F, 1]]);
        }
        groups[name] = names;
      },
      // N small copies of a cut-out in a grid over `box`, popping in row by row (or cell by cell). The same id again
      // changes some of them (every, first, last, pick, random): `grey` greys them out, `to` swaps them to another art.
      pictogram: function (b, who, bi) {
        var name = b.id || "pictogram", g = grids[name];
        if (!g) {
          var art0 = b.art, sz = SIZES[art0];
          if (!sz) throw new Error("KIT.collage: pictogram needs art");
          var n = b.count || 100, bx = b.box || [360, 140, 1560, 860], bw = bx[2] - bx[0], bh = bx[3] - bx[1];
          var cols = b.cols || Math.max(1, Math.round(Math.sqrt(n * bw / bh))), rows = Math.ceil(n / cols), cell = Math.min(bw / cols, bh / rows), fill = b.fill || 0.85;
          var ox = bx[0] + (bw - cell * cols) / 2, oy = bx[1] + (bh - cell * rows) / 2, dur = b.dur === undefined ? 1.2 : b.dur, accel = b.accel === undefined ? 1 : b.accel;
          g = grids[name] = { names: [], cell: cell * fill };
          for (var i = 0; i < n; i++) {
            var r = Math.floor(i / cols), c = i % cols, nm = name + "." + i, k = Math.min(cell * fill / sz[0], cell * fill / sz[1]);
            var ti = b.order === "cells" ? arrival(b, b.t + dur, i, n, accel) : arrival(b, b.t + dur, r, rows, accel);
            copy(nm, art0, ox + (c + 0.5) * cell, oy + (r + 0.5) * cell, b, { anchor: "center", pivot: "center", scale: k });
            g.names.push(nm);
            ev(nm, ti - F, true);
            scaleOp(nm, ti, POP_KEYS);
          }
          groups[name] = g.names;
          return;
        }
        var st = b.stagger || 0, dur2 = b.dur === undefined ? 0.3 : b.dur;
        pickOf(b, g.names, bi).forEach(function (n, j) {
          var a = get(n), t = b.t + j * st;
          if (b.grey !== undefined) {
            if (!a.greys) { a.greys = [[-1e9, 0]]; greyed.push(n); }
            a.greys.push([t, keys(0, a.greys, t)[0]], [t + dur2, b.grey === true ? 1 : b.grey || 0]);
          }
          if (b.to) {
            var sz2 = SIZES[b.to];
            if (!sz2) throw new Error("KIT.collage: no size for art '" + b.to + "'");
            var alt = n + "-" + b.i, c0 = a.home();
            cutout(alt, { art: b.to, x: c0[0], y: c0[1], scale: Math.min(g.cell / sz2[0], g.cell / sz2[1]), hidden: true });
            (afters[n] = afters[n] || []).push(alt);
            ev(n, t, false); ev(alt, t, true);
            scaleOp(alt, t, SWAP_KEYS);
          }
        });
      },
      // A cut-out goes round a closed loop `laps` times: `loop` [cx, cy, rx, ry] (an ellipse, starting at its bottom)
      // or `path` (closed, canvas px). Each lap takes `faster` times the one before; per lap it grows by `grow`, the
      // loop lifts by `rise` (a spiral) and it swaps to the next of `swap` (cast names or arts).
      lap: function (b, who) {
        var base = get(who[0] || (function () { throw new Error("KIT.collage: lap needs who"); })()), pts = b.path, dir = b.dir === -1 ? -1 : 1;
        if (!pts) {
          var lp = b.loop;
          if (!lp) throw new Error("KIT.collage: lap needs loop: [cx, cy, rx, ry] or path");
          pts = [];
          for (var j = 0; j < 96; j++) { var th = Math.PI / 2 + dir * j / 96 * 2 * Math.PI; pts.push([lp[0] + lp[2] * Math.cos(th), lp[1] + lp[3] * Math.sin(th)]); }
        } else if (dir < 0) pts = pts.slice().reverse();
        var tr = track(pts, true), laps = b.laps || 1, dur = b.dur || 2, fast = b.faster || 1, start = (b.from || 0) * tr.L, T = [b.t];
        for (var k = 0; k < laps; k++) T.push(T[k] + dur * Math.pow(fast, k));
        var ys = tr.P.map(function (p) { return p[1]; }), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
        var lapAt = function (t) { for (var k = 0; k < laps; k++) if (t < T[k + 1]) return k + (t - T[k]) / (T[k + 1] - T[k]); return laps; };
        var riders = [base.name].concat((b.swap || []).map(function (s, j) {
          if (A[s]) return s;
          var sz = SIZES[s];
          if (!sz) throw new Error("KIT.collage: lap swap '" + s + "' is neither a cast member nor an art");
          var nm = base.name + ".lap" + (j + 1), kk = base.h / sz[1], an = base.an || [base.w / 2, base.h / 2];
          cutout(nm, { art: s, x: base.left + an[0], y: base.top + an[1], anchor: [an[0] / base.w * sz[0], an[1] / base.h * sz[1]], pivot: "center", scale: kk, hidden: true, faces: base.o && base.o.faces });
          (afters[base.name] = afters[base.name] || []).push(nm);
          return nm;
        }));
        riders.forEach(function (rn, j) {
          var a = get(rn), last = j === riders.length - 1;
          if (j > 0) { ev(rn, T[Math.min(j, laps)], true); scaleOp(rn, T[Math.min(j, laps)], SWAP_KEYS); }
          if (!last) ev(rn, T[Math.min(j + 1, laps)], false);
          op(rn, function (s, t) {
            if (t < b.t) return;
            var L = lapAt(t), lk = Math.min(Math.floor(L), laps - 1), p = tr.at(start + (L - Math.floor(L)) * tr.L), g = Math.pow(b.grow || 1, lk);
            var f = b.depth ? 1 - b.depth * (y1 - p[1]) / (y1 - y0 || 1) : 1;
            p[1] -= (b.rise || 0) * L;
            s.sx *= g * f; s.sy *= g * f; s.r += p[2] * (b.tilt || 0);
            placeAt(a, s, p);
          });
        });
      },
    };
    MOVES.stack = MOVES.pile;

    // ── State: each thing's offset from home, rotation and scale at time t, from its moves in the order written ──
    var frameT = null, memo = {};
    function stateOf(name, t) {
      if (t === frameT && memo[name]) return memo[name];
      var s = { x: 0, y: 0, r: 0, sx: 1, sy: 1 };
      for (var i = 0; i < ops.length; i++) if (ops[i].name === name) ops[i].fn(s, t);
      if (t === frameT) memo[name] = s;
      return s;
    }
    function shown(name, t) {
      var e = events[name], on = A[name] && A[name].hidden !== undefined ? !A[name].hidden : !(e.length && e[0].on);
      for (var i = 0; i < e.length && e[i].t <= t + 1e-6; i++) on = e[i].on;
      return on;
    }
    // A point on a cut-out (art px; null for its middle) in canvas px at time t.
    function pointOf(name, p, t) {
      var a = get(name), s = stateOf(name, t);
      var P = p ? [a.left + p[0] * a.k, a.top + p[1] * a.k] : a.home(), O = [a.left + a.pivot[0], a.top + a.pivot[1]];
      var vx = (P[0] - O[0]) * s.sx, vy = (P[1] - O[1]) * s.sy, c = Math.cos(s.r * Math.PI / 180), sn = Math.sin(s.r * Math.PI / 180);
      return [O[0] + s.x + vx * c - vy * sn, O[1] + s.y + vx * sn + vy * c];
    }
    // "sam.tip" (a named point), "sam" (its middle) or [x, y]
    function target(ref, t) {
      if (Array.isArray(ref)) return ref;
      if (A[ref]) return pointOf(ref, null, t);
      var dot = ref.lastIndexOf("."), a = A[ref.slice(0, dot)], pn = ref.slice(dot + 1);
      if (!a || !a.points[pn]) throw new Error("KIT.collage: no point '" + ref + "' (give the cast member points: { " + pn + ": [x, y] })");
      return pointOf(a.name, a.points[pn], t);
    }

    // ── Build ──
    Object.keys(spec.cast || {}).forEach(function (n) { cast.push(cutout(n, spec.cast[n]).name); });
    var bolts = "", flashEl;
    (spec.beats || []).forEach(function (b, bi) {
      if (!MOVES[b.do]) throw new Error("KIT.collage: no move '" + b.do + "' (beat " + bi + " in " + ID + ")");
      b.i = bi;
      b.t = (b.at !== undefined ? b.at : b.on !== undefined ? cue(b.on, b.n) : 0) + (b.offset || 0);
      // a group's id stands for all its copies
      var whoList = [];
      (b.who === undefined ? [] : [].concat(b.who)).forEach(function (n) { whoList = whoList.concat(!A[n] && !pieces[n] && groups[n] ? groups[n] : [n]); });
      MOVES[b.do](b, whoList, bi);
    });
    Object.keys(events).forEach(function (n) { events[n].sort(function (a, b) { return a.t - b.t || a.i - b.i; }); });

    var weave = q("weave"), film = q("film");
    weave.style.cssText = film.style.cssText = "position:absolute;inset:0";
    var layers = back.concat(cast, cutLayer, front), html = "";
    layers.forEach(function (n) {
      (unders[n] || []).forEach(function (u) { html += A[u].html(); });
      html += A[n].html();
      (afters[n] || []).forEach(function (u) { html += A[u].html(); });
    });
    // A host shot (spec.host) puts the cast in front of Wishonia's console on the observation deck (KIT.studio), with
    // no paper; the studio's slow push moves both.
    var host = spec.host, ab = function (n) { return '<div id="' + ID + "-" + n + '" style="position:absolute;inset:0"></div>'; };
    var stageHtml = '<div id="' + ID + '-stage" class="cg-stage" style="position:absolute;inset:0;transform-origin:0 0">' +
      (host ? "" : "<div " + plateBox + "background:" + PAPER + '"></div>') + html +
      '<svg id="' + ID + '-bolts" class="cg-ab" width="' + W + '" height="' + H + '" style="left:0;top:0"></svg>' +
      '<div id="' + ID + '-flash" ' + plateBox + 'background:#FFF8E4;visibility:hidden"></div>' +
      (xflashes.length ? '<div id="' + ID + '-xflash" ' + plateBox + 'background:#F2F6FF;visibility:hidden"></div>' : "") + "</div>";
    weave.innerHTML = '<div id="' + ID + '-shake" style="position:absolute;inset:0">' +
      (host ? '<div id="' + ID + '-hcam" style="position:absolute;inset:0">' + ab("hwall") + ab("hwish") + ab("hfront") + stageHtml + "</div>" : stageHtml) + "</div>" + (host ? ab("hiris") : "");
    flashEl = q("flash");
    var shakeEl = q("shake"), stage = q("stage"), boltsEl = q("bolts"), names = Object.keys(A), pieceNames = Object.keys(pieces);
    names.forEach(function (n) {
      var a = A[n];
      a.el = q(n); a.art = a.el.querySelector(".cg-art");
      a.eyeEls = a.el.querySelectorAll(".cg-eye"); a.puffEls = a.el.querySelectorAll(".cg-puff");
    });
    pieceNames.forEach(function (n) { pieces[n].el = q(n); });
    // the x-ray flashes, and the copies a pictogram greyed out
    if (xflashes.length) {
      var xflashEl = q("xflash");
      tickers.push(function (t) {
        var o = 0;
        xflashes.forEach(function (f) { if (t >= f[0]) o = Math.max(o, 1 - (t - f[0]) / f[1]); });
        vis(xflashEl, o > 0); xflashEl.style.opacity = Math.max(0, o).toFixed(2);
      });
    }
    if (greyed.length) tickers.push(function (t) {
      greyed.forEach(function (n) {
        var g = keys(0, A[n].greys, t)[0];
        A[n].art.style.filter = g > 0 ? "grayscale(" + g.toFixed(2) + ") opacity(" + (1 - 0.6 * g).toFixed(2) + ")" : "";
      });
    });
    var camera = null;
    if (spec.views) {
      var first = spec.view || Object.keys(spec.views)[0], prev = first, ck = [[0, first]];
      cams.sort(function (a, b) { return a.t - b.t; }).forEach(function (c) { ck.push([c.t, prev], [c.t + (c.dur || 0.6), c.view]); prev = c.view; });
      camera = K.camera(spec.views, ck, [W / 2, H / 2]);
    }

    var tl = gsap.timeline({ paused: true });
    K.film(tl, ID, weave, film, spec.seed || 300);
    if (host) {
      var ho = host === true ? {} : host, set = K.studio(tl, ID, { cam: q("hcam"), wall: q("hwall"), wish: q("hwish"), front: q("hfront") }, { push: ho.push });
      // iris: ["in" or "out", t0, t1] (scene seconds), on her face
      if (ho.iris) K.iris(tl, ID, q("hiris"), set.S.face, ho.iris[0], ho.iris[1], ho.iris[2]);
    }
    K.onTime(tl, D, function (t0) {
      var t = twos(t0), fr = Math.round(t * 12);
      frameT = t; memo = {}; bolts = "";
      names.forEach(function (n) { var a = A[n], s = (a.s = stateOf(n, t)); put(a.el, s.x, s.y, s.r, s.sx, s.sy); vis(a.el, shown(n, t)); });
      pieceNames.forEach(function (n) { var s = stateOf(n, t); put(pieces[n].el, s.x, s.y, s.r, s.sx, s.sy); });
      tickers.forEach(function (f) { f(t, fr); });
      boltsEl.innerHTML = bolts;
      // charred cut-outs: black, with white eyes that blink, and smoke
      names.forEach(function (n, i) {
        var a = A[n];
        if (a.charT === undefined) return;
        var on = t >= a.charT, s = a.s, blink = (a.blinks || []).some(function (b) { return t >= b && t < b + 2 * F; });
        a.art.style.filter = on ? CHAR : "none";
        Array.prototype.forEach.call(a.eyeEls, function (e) { vis(e, on); put(e, 0, 0, 0, 1 / s.sx, (blink ? 0.12 : 1) / s.sy); });
        Array.prototype.forEach.call(a.puffEls, function (p, j) {
          var age = t - a.charT - 0.07 - (j % 3) * 0.28;
          vis(p, on && age > 0);
          if (on && age > 0) {
            var u = (age % 0.84) / 0.84, g = 0.5 + 1.1 * u;
            p.style.opacity = (0.85 * (1 - u)).toFixed(2);
            put(p, -a.faces * 18 * u + 8 * Math.sin(age * 5 + i), -150 * u, 0, g / s.sx, g / s.sy);
          }
        });
      });
      var sh = [0, 0];
      shakes.forEach(function (f) { f(t, fr, sh); });
      put(shakeEl, sh[0], sh[1]);
      if (camera) { var c = camera.at(t); stage.style.transform = "translate(" + px(W / 2 - c.x * c.s) + "," + px(H / 2 - c.y * c.s) + ") scale(" + c.s.toFixed(4) + ")"; }
    });
    tl.set({}, {}, D);
    window.__timelines[ID] = tl;
    return tl;
  }

  collage.SIZES = SIZES;
  collage.axes = axes;
  collage.F = F;
  K.collage = collage;
})();
