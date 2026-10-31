// Cut-out collage (cartoon-style-bible.md section 1): hand-tinted engraving cut-outs from assets/art/collage/ on
// aged paper, moving stiffly on twos (12 drawings a second), like paper under a rostrum camera.
//
//   KIT.collage(spec)   builds a whole collage scene from a short spec: { id, seed, cast, beats, views }.
//                       The spec's fields and every move are in video/README.md, "Writing a collage scene".
//   KIT.collage.SIZES   each cut-out's art size in px (add a new cut-out's size here)
//
// Load it after kit.js and film.js. Copy compositions/scenes/pilot-collage/*.html for the file around a spec.
(function () {
  var K = window.KIT;
  if (K.collage) return;
  if (!K.film) throw new Error("collage.js: load assets/js/film.js before it");
  var F = 1 / 12, ART = "assets/art/collage/";
  var INK = "#2B2033", RED = "#A8322A", CARD = "#F5ECD3";
  var SIZES = {
    atom: [370, 450], "general-head": [353, 493], general: [359, 686], globe: [381, 643], mushroom: [425, 626],
    scientist: [319, 753], "uncle-sam-head": [377, 611], "uncle-sam": [348, 704],
  };
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
  var DIRS = { left: [-1, 0], right: [1, 0], top: [0, -1], bottom: [0, 1] };
  var dir = function (d) { if (!DIRS[d]) throw new Error("KIT.collage: no direction '" + d + "'"); return DIRS[d]; };

  function collage(spec) {
    window.__timelines = window.__timelines || {};
    var ID = spec.id, D = K.scene(ID).duration, W = K.W, H = K.H;
    var q = function (s) { return document.getElementById(ID + "-" + s); };
    var cue = function (w, n) { return K.cue(ID, w, n); };
    var timeOf = function (u) { return u === undefined ? Infinity : typeof u === "number" ? u : Array.isArray(u) ? cue(u[0], u[1]) + (u[2] || 0) : cue(u); };
    var A = {}, pieces = {}, ops = [], events = {}, tickers = [], shakes = [], cams = [];
    var cast = [], cutLayer = [], back = [], front = [], unders = {};

    function actor(name, a) {
      if (A[name] || pieces[name]) throw new Error("KIT.collage: two things called '" + name + "'");
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
    // A cut-out from the cast: art, x, y, scale, anchor, pivot, clip, pieces, cut, points, eyes, smoke, faces, hidden.
    function cutout(name, o) {
      var sz = SIZES[o.art];
      if (!sz) throw new Error("KIT.collage: no size for art '" + o.art + "' (add it to KIT.collage.SIZES in collage.js)");
      var k = o.scale || 1, an = spot(o.anchor, sz[0], sz[1]), pv = spot(o.pivot, sz[0], sz[1]);
      var a = actor(name, { o: o, k: k, w: sz[0] * k, h: sz[1] * k, pivot: [pv[0] * k, pv[1] * k], points: o.points || {},
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
        var deco = a.eyes.map(function (e) { return '<div class="cg-eye" style="left:' + px(e[0] * k) + ";top:" + px(e[1] * k) + ';visibility:hidden"><i></i></div>'; }).join("");
        a.smoke.forEach(function (sm) { for (var i = 0; i < 3; i++) deco += '<div class="cg-puff" style="left:' + px(sm[0] * k) + ";top:" + px(sm[1] * k) + ';visibility:hidden"></div>'; });
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
      var w = sign ? sign.w - 88 : null, size = K.fitText(o.text, o.size || 56, sign ? w - 52 : 1000, "Oswald", 600);
      if (!sign) w = K.textWidth(o.text, size, "Oswald", 600) + 52;
      var h = size * 1.45;
      var a = actor(name, { w: w, h: h, pivot: [w / 2, h / 2], points: {}, eyes: [], smoke: [], faces: 1, hidden: true });
      a.left = sign ? 44 : (o.x === undefined ? W / 2 : o.x) - w / 2;
      a.top = sign ? 60 + (sign.titleSize || 0) : (o.y === undefined ? H / 2 : o.y) - h / 2;
      a.html = function () {
        return '<div id="' + ID + "-" + name + '" class="cg-ab" style="left:' + px(a.left) + ";top:" + px(a.top) + ";width:" + px(w) + ";height:" + px(h) + ";box-sizing:border-box;border:5px solid " + RED + ";color:" + RED +
          ";font:600 " + px(size) + "/" + px(size * 1.32) + ' Oswald;white-space:nowrap;text-align:center;visibility:hidden;transform-origin:50% 50%">' + o.text + "</div>";
      };
      if (sign) { sign.children.push(name); a.inside = true; } else front.push(name);
      return a;
    }

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
      camera: function (b) { cams.push(b); },
    };

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
      MOVES[b.do](b, b.who === undefined ? [] : [].concat(b.who), bi);
    });
    Object.keys(events).forEach(function (n) { events[n].sort(function (a, b) { return a.t - b.t || a.i - b.i; }); });

    var weave = q("weave"), film = q("film");
    weave.style.cssText = film.style.cssText = "position:absolute;inset:0";
    var layers = back.concat(cast, cutLayer, front), html = "";
    layers.forEach(function (n) { (unders[n] || []).forEach(function (u) { html += A[u].html(); }); html += A[n].html(); });
    weave.innerHTML = '<div id="' + ID + '-shake" style="position:absolute;inset:0"><div id="' + ID + '-stage" class="cg-stage" style="position:absolute;inset:0;transform-origin:0 0">' +
      '<div class="cg-full" style="background:' + PAPER + '"></div>' + html +
      '<svg id="' + ID + '-bolts" class="cg-ab" width="' + W + '" height="' + H + '" style="left:0;top:0"></svg>' +
      '<div id="' + ID + '-flash" class="cg-full" style="background:#FFF8E4;visibility:hidden"></div></div></div>';
    flashEl = q("flash");
    var shakeEl = q("shake"), stage = q("stage"), boltsEl = q("bolts"), names = Object.keys(A), pieceNames = Object.keys(pieces);
    names.forEach(function (n) {
      var a = A[n];
      a.el = q(n); a.art = a.el.querySelector(".cg-art");
      a.eyeEls = a.el.querySelectorAll(".cg-eye"); a.puffEls = a.el.querySelectorAll(".cg-puff");
    });
    pieceNames.forEach(function (n) { pieces[n].el = q(n); });
    var camera = null;
    if (spec.views) {
      var first = spec.view || Object.keys(spec.views)[0], prev = first, ck = [[0, first]];
      cams.sort(function (a, b) { return a.t - b.t; }).forEach(function (c) { ck.push([c.t, prev], [c.t + (c.dur || 0.6), c.view]); prev = c.view; });
      camera = K.camera(spec.views, ck, [W / 2, H / 2]);
    }

    var tl = gsap.timeline({ paused: true });
    K.film(tl, ID, weave, film, spec.seed || 300);
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
  collage.F = F;
  K.collage = collage;
})();
