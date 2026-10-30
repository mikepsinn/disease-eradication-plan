// Shared kit for the episode cartoon: cue times, the Wishonia rig, and SVG art for both layers.
// Every function is deterministic (no Math.random, no Date), because the renderer seeks frame by frame.
(function () {
  if (window.KIT) return;
  var P = window.HF_PART;
  // Canvas: 16:9 (1920 x 1080) or the tall phone version, 9:16 (1080 x 1920), set by tools/build-part.mjs.
  var V = window.HF_ASPECT === "9x16";
  var W = V ? 1080 : 1920, H = V ? 1920 : 1080;

  // ── Colors (cartoon-style-bible.md section 1) ─────────────────────────
  // The theme song music video's palette (measured from its keyframes): burnt orange, deep navy,
  // slate, cream, rust and tan, with mustard stars; brick red and muted teal are the two kinds of money.
  var C = {
    // Layer A: Wishonia's office
    red: "#C8452E", orange: "#E5903B", yellow: "#E8B04A", peri: "#5C6F8E", cream: "#F3ECD0",
    navy: "#112845", deep: "#061D3E", slate: "#273049", rust: "#904B2E", tan: "#B47E52", cyan: "#7FB5B0", ink: "#0B1A33",
    // Layer B: the Earth diagrams
    paper: "#F3ECD0", line: "#112845", war: "#C8452E", med: "#2F8F86",
    // money is always money green; its seal says what it buys (red missile = war, teal cross = medicine)
    money: "#86AD6E", moneyDark: "#3B6644", moneyEdge: "#6F9A5C",
  };

  // ── Time ──────────────────────────────────────────────────────────────
  function scene(id) {
    for (var i = 0; i < P.scenes.length; i++) if (P.scenes[i].id === id) return P.scenes[i];
    throw new Error("No scene " + id);
  }
  function norm(s) {
    return s.toLowerCase().replace(/[^a-z0-9%$]/g, "");
  }
  // Start of the n-th (default 1st) spoken `text` in scene `id`, in that scene's local seconds.
  function cue(id, text, n) {
    var sc = scene(id);
    var want = norm(text);
    var count = n || 1;
    for (var i = 0; i < P.words.length; i++) {
      var w = P.words[i];
      if (w.s < sc.start - 0.05 || w.s >= sc.start + sc.duration) continue;
      if (norm(w.w) === want && --count === 0) return Math.round((w.s - sc.start) * 1000) / 1000;
    }
    throw new Error("Cue '" + text + "' not in scene " + id);
  }
  function cueEnd(id, text, n) {
    var sc = scene(id);
    var t = cue(id, text, n) + sc.start;
    for (var i = 0; i < P.words.length; i++) if (Math.abs(P.words[i].s - t) < 0.001) return P.words[i].e - sc.start;
    return t - sc.start;
  }
  // The comedy timing from the storyboards: a beat (0.35 s) after the word ends, or half a second before it starts.
  function after(id, text, n) {
    return cueEnd(id, text, n) + 0.35;
  }
  function before(id, text, n) {
    return Math.max(0, cue(id, text, n) - 0.5);
  }
  // Seeded pseudo-random numbers (deterministic).
  function rng(seed) {
    var s = seed >>> 0;
    return function () {
      s = (s * 1664525 + 1013904223) >>> 0;
      return s / 4294967296;
    };
  }
  // Run fn(localTime) on every seek of a scene timeline.
  function onTime(tl, duration, fn) {
    var o = { t: 0 };
    tl.fromTo(o, { t: 0 }, {
      t: duration, duration: duration, ease: "none",
      onUpdate: function () { fn(o.t); },
      onStart: function () { fn(o.t); },
    }, 0);
    fn(0);
  }

  // ── Wishonia rig (transmit/public/assets/js/characters.js) ─────────────
  var EXPRESSION_MOUTHS = {
    neutral: ["smile", "open", "oh", "ee", "closed", "small", "frown"],
    happy: ["smile", "open", "oh", "ee", "closed", "small"],
    excited: ["open", "ee", "oh", "closed"],
    sad: ["closed", "frown", "oh", "small"],
    annoyed: ["closed", "frown", "small"],
    skeptical: ["smile", "closed"],
    surprised: ["open", "oh", "ee"],
    eyeroll: ["closed", "frown", "smile"],
    smirk: ["smile", "ee", "closed"],
    thinking: ["oh", "closed", "small"],
    sideeye: ["closed"],
    lookright: ["smile", "closed", "open", "oh"],
    blink: ["smile"],
  };
  function getHeadName(expression, viseme) {
    var available = EXPRESSION_MOUTHS[expression];
    var mouth = available.indexOf(viseme) >= 0 ? viseme : "closed";
    if (available.indexOf(mouth) < 0) mouth = available[0];
    return expression + "-" + mouth;
  }
  function lastAt(list, t, key) {
    var hit = null;
    for (var i = 0; i < list.length; i++) {
      var at = key ? list[i][key] : list[i][0];
      if (at <= t + 1e-6) hit = list[i];
      else break;
    }
    return hit;
  }
  // The head and body to show at part time t.
  function wishoniaAt(t) {
    var st = lastAt(P.states, t, "t");
    var m = lastAt(P.mouth, t);
    var v = m ? m[1] : null;
    var head = v === null ? st.expr + "-" + st.rest : getHeadName(st.expr, v);
    for (var i = 0; i < P.blinks.length; i++) {
      var b = P.blinks[i];
      if (t >= b[0] && t < b[0] + b[1]) head = "blink-smile";
    }
    return { head: head, body: st.body, expr: st.expr };
  }
  // Idle rock: -2deg to +2deg and up 2px (at 140px wide), 7 s each way, holding at both ends.
  function bob(t) {
    var cycle = t % 14;
    var p = cycle < 7 ? cycle / 7 : 2 - cycle / 7;
    var k = p < 0.4 ? 0 : p > 0.6 ? 1 : (p - 0.4) / 0.2;
    k = k * k * (3 - 2 * k);
    return { rot: -2 + 4 * k, lift: k };
  }

  // Build a Wishonia rig in `parent`. opts: { scene, x, y, w, corner } (corner: from KIT.cornerOpts).
  // Head 95% of width, centered; body full width below, overlapping the head by 12/140 of the width.
  function mountWishonia(tl, parent, opts) {
    var sc = scene(opts.scene);
    var w = opts.w;
    var heads = { "blink-smile": 1 };
    var bodies = {};
    var first = lastAt(P.states, sc.start, "t");
    P.states.forEach(function (st) {
      if (st !== first && (st.t < sc.start || st.t >= sc.start + sc.duration)) return;
      EXPRESSION_MOUTHS[st.expr].forEach(function (m) { heads[st.expr + "-" + m] = 1; });
      bodies[st.body] = 1;
    });

    var frame = document.createElement("div");
    frame.className = "kit-wish-frame";
    frame.setAttribute("data-layout-allow-overflow", "");
    var rig = document.createElement("div");
    rig.className = "kit-wish-rig";
    rig.style.cssText = "position:absolute;left:" + opts.x + "px;top:" + opts.y + "px;width:" + w + "px;height:" + Math.round(w * 1.5) + "px;";
    frame.style.cssText = "position:absolute;inset:0;" + (opts.corner ? "overflow:hidden;" : "");
    var craft = frame;
    if (opts.corner) {
      // Mirrored, so her pointing and presenting bodies point into the frame; a cream-and-navy cut-out edge
      // keeps her readable over the diagram.
      rig.style.transform = "scaleX(-1)";
      rig.style.filter = ["4px 0", "-4px 0", "0 4px", "0 -4px"].map(function (d) { return "drop-shadow(" + d + " 0 " + C.cream + ")"; }).join(" ") + " " +
        ["3px 0", "-3px 0", "0 3px", "0 -3px"].map(function (d) { return "drop-shadow(" + d + " 0 " + C.line + ")"; }).join(" ");
      craft = document.createElement("div");
      craft.style.cssText = "position:absolute;inset:0;";
      frame.appendChild(craft);
    }
    var bodyBox = document.createElement("div");
    bodyBox.style.cssText = "position:absolute;left:0;top:" + Math.round(w * 0.95 - (w * 12) / 140) + "px;width:" + w + "px;height:" + Math.round((w * 768) / 1343) + "px;";
    var headBox = document.createElement("div");
    headBox.style.cssText = "position:absolute;left:" + Math.round(w * 0.025) + "px;top:0;width:" + Math.round(w * 0.95) + "px;height:" + Math.round(w * 0.95) + "px;transform-origin:50% 78%;";
    function addImg(box, name, store) {
      var img = document.createElement("img");
      img.src = "assets/sprites/" + name + ".png";
      img.alt = "";
      img.style.cssText = "position:absolute;inset:0;width:100%;height:100%;opacity:0;";
      box.appendChild(img);
      store[name] = img;
    }
    var headImgs = {};
    var bodyImgs = {};
    Object.keys(bodies).forEach(function (b) { addImg(bodyBox, "body-" + b, bodyImgs); });
    Object.keys(heads).forEach(function (h) { addImg(headBox, h, headImgs); });
    rig.appendChild(bodyBox);
    rig.appendChild(headBox);
    if (opts.corner === "saucer") craft.appendChild(saucerLayer(opts, true));
    craft.appendChild(rig);
    if (opts.corner === "saucer") craft.appendChild(saucerLayer(opts, false));
    parent.appendChild(frame);

    var shown = { head: null, body: null };
    onTime(tl, sc.duration, function (local) {
      var t = sc.start + local;
      var s = wishoniaAt(t);
      var body = "body-" + s.body;
      if (shown.head !== s.head) {
        if (shown.head) headImgs[shown.head].style.opacity = 0;
        headImgs[s.head].style.opacity = 1;
        shown.head = s.head;
      }
      if (shown.body !== body) {
        if (shown.body) bodyImgs[shown.body].style.opacity = 0;
        bodyImgs[body].style.opacity = 1;
        shown.body = body;
      }
      var b = bob(t);
      headBox.style.transform = "translateY(" + (-b.lift * w * 2 / 140).toFixed(2) + "px) rotate(" + b.rot.toFixed(3) + "deg)";
      // The saucer hovers: a slow bob and tilt.
      if (opts.corner === "saucer") craft.style.transform = "translateY(" + (Math.sin(t * 1.9) * 5).toFixed(2) + "px) rotate(" + (Math.sin(t * 1.1) * 1.2).toFixed(3) + "deg)";
    });
    return { frame: frame, rig: rig, craft: craft };
  }
  // Wishonia's flying saucer (9:16): the far rim behind her (back) or the hull in front, which hides
  // where the body sprite ends. Sized from the rig width; the rim sits at her hips.
  function saucerLayer(opts, back) {
    var k = opts.w / 280, cx = opts.x + opts.w / 2, cy = opts.y + 318 * k, rx = 150 * k, ry = 24 * k;
    var inner = back
      ? '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + rx + '" ry="' + ry + '" fill="' + C.slate + '" stroke="' + C.line + '" stroke-width="6"/>'
      : '<path d="M' + (cx - rx) + "," + cy + " A" + rx + "," + ry + " 0 0 0 " + (cx + rx) + "," + cy + " L" + (cx + rx * 1.12) + "," + (cy + 22 * k) + " Q" + cx + "," + (cy + 70 * k) + " " + (cx - rx * 1.12) + "," + (cy + 22 * k) + ' Z" fill="' + C.peri + '" stroke="' + C.line + '" stroke-width="6" stroke-linejoin="round"/>' +
        '<path d="M' + (cx - rx) + "," + cy + " A" + rx + "," + ry + " 0 0 0 " + (cx + rx) + "," + cy + '" fill="none" stroke="' + C.cream + '" stroke-width="7"/>' +
        '<path d="M' + (cx - rx * 0.8) + "," + (cy + 52 * k) + " Q" + cx + "," + (cy + 96 * k) + " " + (cx + rx * 0.8) + "," + (cy + 52 * k) + ' Z" fill="' + C.orange + '" stroke="' + C.line + '" stroke-width="5"/>' +
        [-0.7, -0.35, 0, 0.35, 0.7].map(function (d) { return '<circle cx="' + (cx + d * rx) + '" cy="' + (cy + 30 * k - Math.abs(d) * 12 * k) + '" r="' + 9 * k + '" fill="' + C.yellow + '" stroke="' + C.line + '" stroke-width="3"/>'; }).join("");
    var layer = document.createElement("div");
    layer.className = back ? "kit-saucer-back" : "kit-saucer";
    layer.style.cssText = "position:absolute;inset:0;";
    layer.innerHTML = '<svg width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + " " + H + '" style="position:absolute;inset:0;overflow:visible">' + inner + "</svg>";
    return layer;
  }

  // ── SVG helpers ──────────────────────────────────────────────────────
  function svg(w, h, inner, attrs) {
    return '<svg xmlns="http://www.w3.org/2000/svg" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + " " + h + '" ' + (attrs || "") + ">" + inner + "</svg>";
  }
  function el(html) {
    var d = document.createElement("div");
    d.innerHTML = html.trim();
    return d.firstChild;
  }

  // Layer A: sunburst rays from (cx, cy), in the cover colors, darker behind Wishonia.
  function sunburst(w, h, cx, cy, n) {
    var colors = [C.red, C.cream, C.orange, C.peri, C.yellow, C.cream];
    var rays = "";
    var count = n || 30;
    var R = Math.hypot(w, h) * 1.2;
    for (var i = 0; i < count; i++) {
      var a0 = Math.PI + (i / count) * Math.PI;
      var a1 = Math.PI + ((i + 1) / count) * Math.PI;
      rays += '<path d="M' + cx + "," + cy + " L" + (cx + R * Math.cos(a0)).toFixed(1) + "," + (cy + R * Math.sin(a0)).toFixed(1) +
        " L" + (cx + R * Math.cos(a1)).toFixed(1) + "," + (cy + R * Math.sin(a1)).toFixed(1) + ' Z" fill="' + colors[i % colors.length] + '"/>';
    }
    return rays;
  }
  function halfSun(cx, cy, r) {
    var rings = [[1, C.red], [0.84, C.orange], [0.68, C.yellow], [0.52, C.cream], [0.38, C.yellow]];
    return rings.map(function (g) {
      var rr = r * g[0];
      return '<path d="M' + (cx - rr) + "," + cy + " A" + rr + "," + rr + " 0 0 1 " + (cx + rr) + "," + cy + ' Z" fill="' + g[1] + '"/>';
    }).join("");
  }
  // Neon perspective grid floor from y0 to y1 with the vanishing point at (cx, y0 - lift).
  function gridFloor(w, y0, y1, cx) {
    var out = '<rect x="0" y="' + y0 + '" width="' + w + '" height="' + (y1 - y0) + '" fill="' + C.navy + '"/>';
    var vy = y0 - 60;
    for (var i = -24; i <= 24; i++) {
      var xb = cx + i * 150;
      var xt = cx + (xb - cx) * ((y0 - vy) / (y1 - vy));
      out += '<line x1="' + xt.toFixed(1) + '" y1="' + y0 + '" x2="' + xb.toFixed(1) + '" y2="' + y1 + '" stroke="' + C.cyan + '" stroke-width="2.2" opacity="0.85"/>';
    }
    for (var k = 1; k <= 12; k++) {
      var y = y0 + (y1 - y0) * Math.pow(k / 12, 2.1);
      out += '<line x1="0" y1="' + y.toFixed(1) + '" x2="' + w + '" y2="' + y.toFixed(1) + '" stroke="' + C.cyan + '" stroke-width="' + (1.2 + k * 0.22).toFixed(2) + '" opacity="0.85"/>';
    }
    out += '<rect x="0" y="' + (y0 - 3) + '" width="' + w + '" height="6" fill="' + C.cyan + '"/>';
    return out;
  }
  // Mid-century motifs: the four-point atomic star and the boomerang.
  function star(x, y, r, color, n) {
    var pts = [], k = n || 4;
    for (var i = 0; i < k * 2; i++) {
      var a = (Math.PI * i) / k - Math.PI / 2, rr = i % 2 ? r * 0.2 : r;
      pts.push((x + rr * Math.cos(a)).toFixed(1) + "," + (y + rr * Math.sin(a)).toFixed(1));
    }
    return '<polygon points="' + pts.join(" ") + '" fill="' + color + '"/>';
  }
  function boomerang(x, y, s, color, rot) {
    return '<path transform="translate(' + x + "," + y + ") rotate(" + (rot || 0) + ") scale(" + s + ')" d="M0,0 Q40,-55 100,-34 Q52,-22 32,22 Q22,6 0,0 Z" fill="' + color + '"/>';
  }
  // The full Layer A office backdrop: a navy wall with geometric panels and atomic stars, a rising
  // orange sun on the horizon, a tiled floor, and a mustard disc behind Wishonia's head at (hx, hcy).
  // The rising sun on the office horizon, alone (for scenes that animate it).
  function sun(cx, hy, scale) {
    return [[1, C.rust], [0.82, C.orange], [0.6, C.yellow]].map(function (g) {
      var r = (V ? 360 : 300) * g[0] * (scale || 1);
      return '<path d="M' + (cx - r) + "," + hy + " A" + r + "," + r + " 0 0 1 " + (cx + r) + "," + hy + ' Z" fill="' + g[1] + '"/>';
    }).join("");
  }
  // opts: { noSun, noHalo } leave out the sun or the disc behind Wishonia.
  function office(hx, hcy, opts) {
    opts = opts || {};
    var w = W, h = H, hy = V ? 1180 : 610, cx = W / 2;
    var cy = hcy === undefined ? (V ? 900 : 420) : hcy;
    var panels = '<path d="M0,0 H' + w * 0.28 + " L" + w * 0.18 + "," + hy + ' H0 Z" fill="' + C.slate + '"/>' +
      '<path d="M' + w + ",0 H" + w * 0.74 + " L" + w * 0.84 + "," + hy + " H" + w + ' Z" fill="' + C.deep + '"/>' +
      '<circle cx="' + w * 0.12 + '" cy="' + h * 0.16 + '" r="' + w * 0.05 + '" fill="' + C.rust + '"/>' +
      '<path d="M' + w * 0.86 + "," + h * 0.08 + " l" + w * 0.06 + "," + w * 0.06 + " l" + -w * 0.06 + "," + w * 0.06 + " l" + -w * 0.06 + "," + -w * 0.06 + ' Z" fill="' + C.tan + '" opacity="0.8"/>';
    var stars = [[0.07, 0.42, 22, C.yellow], [0.33, 0.1, 16, C.cream], [0.62, 0.07, 26, C.yellow], [0.93, 0.36, 18, C.cream], [0.24, 0.3, 12, C.cream], [0.78, 0.22, 12, C.yellow]]
      .map(function (s) { return star(w * s[0], hy * s[1] * 1.6, s[2], s[3]); }).join("");
    var tiles = "";
    for (var i = -12; i <= 12; i++) {
      var xb = cx + i * 170;
      tiles += '<path d="M' + (cx + i * 60) + "," + hy + " L" + xb + "," + h + '" stroke="' + C.slate + '" stroke-width="3"/>';
    }
    for (var k = 1; k <= 6; k++) {
      var y = hy + (h - hy) * Math.pow(k / 6, 1.7);
      tiles += '<path d="M0,' + y.toFixed(1) + " H" + w + '" stroke="' + C.slate + '" stroke-width="3"/>';
    }
    return svg(w, h,
      '<rect width="' + w + '" height="' + h + '" fill="' + C.navy + '"/>' + panels + stars +
      boomerang(w * 0.05, hy * 0.75, 1.2, C.orange, -20) + boomerang(w * 0.9, hy * 0.62, 1, C.orange, 160) +
      (opts.noSun ? "" : sun(cx, hy)) + '<rect x="0" y="' + hy + '" width="' + w + '" height="' + (h - hy) + '" fill="#1C2A44"/>' + tiles +
      '<rect x="0" y="' + (hy - 4) + '" width="' + w + '" height="8" fill="' + C.yellow + '"/>' +
      (opts.noHalo ? "" : '<circle cx="' + hx + '" cy="' + cy + '" r="' + (V ? 330 : 300) + '" fill="' + C.yellow + '" opacity="0.9"/>')
    );
  }
  // Retro office desk front (drawn in front of Wishonia). Top edge at y.
  function desk(x, y, w) {
    var h = H - y;
    return '<g stroke="' + C.ink + '" stroke-width="6" stroke-linejoin="round">' +
      '<path d="M' + (x - 20) + "," + y + " h" + (w + 40) + " l-18,34 h" + -(w + 4) + ' Z" fill="' + C.rust + '"/>' +
      '<rect x="' + x + '" y="' + (y + 34) + '" width="' + w + '" height="' + h + '" fill="' + C.tan + '"/>' +
      '<rect x="' + (x + 40) + '" y="' + (y + 70) + '" width="' + (w - 80) + '" height="' + (h - 70) + '" rx="10" fill="' + C.orange + '"/>' +
      '<path d="M' + (x + 70) + "," + (y + 110) + " h" + (w - 140) + '" stroke="' + C.cream + '" stroke-width="8" opacity="0.6"/>' +
      "</g>";
  }
  function mug(x, y) {
    return '<g stroke="' + C.ink + '" stroke-width="5" stroke-linejoin="round">' +
      '<path d="M' + (x + 44) + "," + (y + 14) + " q28,4 24,26 q-4,20 -26,16" + '" fill="none"/>' +
      '<path d="M' + x + "," + y + " h48 l-4,62 q-1,8 -9,8 h-22 q-8,0 -9,-8 Z" + '" fill="' + C.cream + '"/>' +
      '<path d="M' + (x + 6) + "," + (y + 24) + ' h36" stroke="' + C.red + '" stroke-width="8"/>' +
      "</g>";
  }
  function cabinet(x, y) {
    return '<g stroke="' + C.ink + '" stroke-width="6" stroke-linejoin="round">' +
      '<rect x="' + x + '" y="' + y + '" width="230" height="330" rx="10" fill="' + C.peri + '"/>' +
      [0, 1, 2].map(function (i) {
        var dy = y + 18 + i * 104;
        return '<rect x="' + (x + 16) + '" y="' + dy + '" width="198" height="92" rx="6" fill="#7486A3"/>' +
          '<rect x="' + (x + 90) + '" y="' + (dy + 56) + '" width="50" height="14" rx="7" fill="' + C.ink + '"/>' +
          (i === 0 ? '<rect x="' + (x + 36) + '" y="' + (dy + 12) + '" width="158" height="36" fill="' + C.cream + '" stroke-width="3"/>' +
            '<text x="' + (x + 115) + '" y="' + (dy + 36) + '" text-anchor="middle" font-family="Oswald" font-size="17" fill="' + C.ink + '" stroke="none">EARTH: CASE #847</text>' : "");
      }).join("") +
      "</g>";
  }
  // Retro wall screen (TV). Returns svg markup for the bezel; put content inside the hole (x+34, y+34, w-68, h-68).
  function wallScreen(x, y, w, h) {
    return '<g stroke="' + C.ink + '" stroke-width="7" stroke-linejoin="round">' +
      '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="34" fill="' + C.rust + '"/>' +
      '<rect x="' + (x + 34) + '" y="' + (y + 34) + '" width="' + (w - 68) + '" height="' + (h - 68) + '" rx="22" fill="' + C.paper + '"/>' +
      '<circle cx="' + (x + w - 18) + '" cy="' + (y + h + 24) + '" r="0" fill="none"/>' +
      '<path d="M' + (x + w * 0.3) + "," + (y + h) + " l-30,46 M" + (x + w * 0.7) + "," + (y + h) + ' l30,46" fill="none"/>' +
      "</g>";
  }

  // Layer B: flat cream paper with halftone-dot fills (the music video's printed look) and a few
  // atomic stars in the corners. The pattern ids keep their old names (hatch, cross, fine, hred, hteal).
  function dots(pid, step, r, color, angle) {
    return '<pattern id="' + pid + '" width="' + step + '" height="' + step + '" patternUnits="userSpaceOnUse" patternTransform="rotate(' + (angle || 45) + ')">' +
      '<circle cx="' + step / 2 + '" cy="' + step / 2 + '" r="' + r + '" fill="' + color + '"/></pattern>';
  }
  function paperDefs(id) {
    return "<defs>" +
      dots(id + "-hatch", 8, 1.9, C.line) + dots(id + "-cross", 6, 2.1, C.line) + dots(id + "-fine", 5, 1, C.line, 30) +
      dots(id + "-hred", 7, 2, "#8E2E1E") + dots(id + "-hteal", 7, 2, "#1D5E59") +
      "</defs>";
  }
  function paper(id) {
    return svg(W, H,
      paperDefs(id) +
      '<rect width="' + W + '" height="' + H + '" fill="' + C.paper + '"/>' +
      '<rect x="30" y="30" width="' + (W - 60) + '" height="' + (H - 60) + '" fill="none" stroke="' + C.line + '" stroke-width="5"/>' +
      '<rect x="44" y="44" width="' + (W - 88) + '" height="' + (H - 88) + '" fill="none" stroke="' + C.orange + '" stroke-width="2"/>' +
      star(W - 92, 96, 22, C.orange) + star(W - 130, 140, 10, C.yellow) + star(84, H - 84, 18, C.orange)
    );
  }
  // Print grain over a whole frame: a fine speckle pattern (not an SVG filter, which paints through
  // from scenes off screen in the render). Put it last in a frame.
  function grain(id) {
    return '<defs><pattern id="' + id + '-grain" width="9" height="9" patternUnits="userSpaceOnUse">' +
      '<circle cx="2" cy="3" r="0.9" fill="#000" opacity="0.1"/><circle cx="6.5" cy="7" r="0.8" fill="#FFF" opacity="0.12"/><circle cx="7" cy="1.5" r="0.6" fill="#000" opacity="0.08"/></pattern></defs>' +
      '<rect width="' + W + '" height="' + H + '" fill="url(#' + id + '-grain)" pointer-events="none"/>';
  }

  // The standard Layer A office layout for each shape: the wall screen box [x, y, w, h], its center
  // (the origin for the wall-screen zoom transitions), Wishonia's big rig, the desk, and the disc
  // behind her head (pass office.halo to office()).
  var OFFICE = V
    ? { screen: [90, 220, 900, 480], wish: { x: 300, y: 720, w: 480 }, desk: [60, 1250, 960] }
    : { screen: [110, 190, 820, 520], wish: { x: 1100, y: 80, w: 640 }, desk: [1000, 905, 900] };
  OFFICE.screenAt = [OFFICE.screen[0] + OFFICE.screen[2] / 2, OFFICE.screen[1] + OFFICE.screen[3] / 2];
  OFFICE.halo = [OFFICE.wish.x + OFFICE.wish.w / 2, OFFICE.wish.y + Math.round(OFFICE.wish.w * 0.45)];

  // The 1950s mail-in form, "PLANET ELIGIBILITY CHECK" (loved-ones, nuclear-winters, eligible).
  // items: [{ lines: [...] }]. Returns { svg, h, boxes }: boxes[i] is item i's YES box { x, y, s }.
  // Inside: each question line is a <text class="form-line" data-q="i">, and item i's tick is #<id>-tick-<i> .tick.
  function form(id, x, y, w, items, opts) {
    opts = opts || {};
    var s = opts.size || 36, lh = s * 1.3, cy = y + 120, rows = "", boxes = [];
    var label = function (lx, ly, text) {
      return '<text x="' + lx + '" y="' + ly + '" font-family="Oswald" font-weight="600" font-size="32" fill="' + C.line + '">' + text + "</text>";
    };
    items.forEach(function (it, q) {
      it.lines.forEach(function (line, i) {
        rows += '<text class="form-line" data-q="' + q + '" x="' + (x + 44) + '" y="' + (cy + s + i * lh) + '" font-family="Inter" font-weight="600" font-size="' + s + '" fill="' + C.line + '">' + line + "</text>";
      });
      var by = cy + it.lines.length * lh + 14;
      rows += checkbox(x + 44, by, 46) + label(x + 108, by + 38, "YES") + checkbox(x + 220, by, 46) + label(x + 284, by + 38, "NO") +
        '<g id="' + id + "-tick-" + q + '">' + tick(x + 40, by - 8, 58, C.med) + "</g>";
      boxes.push({ x: x + 44, y: by, s: 46 });
      cy = by + 46 + 34;
    });
    var h = cy - y + 40;
    var svgOut = '<rect x="' + (x + 10) + '" y="' + (y + 12) + '" width="' + w + '" height="' + h + '" fill="' + C.ink + '" opacity="0.85"/>' +
      '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="#FBF6E6" stroke="' + C.line + '" stroke-width="5"/>' +
      '<text x="' + (x + w / 2) + '" y="' + (y + 74) + '" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="44" letter-spacing="2" fill="' + C.line + '">PLANET ELIGIBILITY CHECK</text>' +
      '<path d="M' + (x + 40) + "," + (y + 98) + " H" + (x + w - 40) + '" stroke="' + C.orange + '" stroke-width="4"/>' + rows +
      '<text x="' + (x + 44) + '" y="' + (y + h - 22) + '" font-family="Inter" font-style="italic" font-weight="500" font-size="22" fill="' + C.line + '" opacity="0.75">Please allow 4 to 6 weeks for optimization.</text>';
    return { svg: svgOut, h: h, boxes: boxes };
  }
  // Where loved-ones puts the form (nuclear-winters starts from here, so the cut has no seam).
  var FORM_AT = V ? { x: 60, y: 990, w: 960, size: 34 } : { x: 880, y: 150, w: 820, size: 36 };
  var FORM_Q = [
    ["1. Everyone you've ever loved: being", "slowly tortured and/or murdered by", "horrible diseases?"],
    ["2. Enough nuclear bombs for", "122 nuclear winters?"],
  ];

  // Wishonia in Layer B: in 16:9 she stands in the bottom right corner, cut off at the thighs by the
  // frame's bottom edge; in 9:16 (where captions and the apps' buttons fill the bottom) she rides her
  // flying saucer in the top right. Both show her whole gesture body, mirrored to point into the frame.
  function cornerOpts(scene) {
    return V ? { scene: scene, x: 770, y: 70, w: 240, corner: "saucer" } : { scene: scene, x: 1626, y: 693, w: 274, corner: "stand" };
  }
  // Scene transitions (cartoon-script rule: Layer B is the footage on the office wall screen).
  // cam: a wrapper around the whole scene; at: the wall screen's center in this layout.
  // The zoom between an office scene and the Earth footage on its wall screen. screen: the wall screen
  // box [x, y, w, h] (default OFFICE.screen). One fixed point `at` maps the whole frame onto the screen's
  // picture, centered (scale `into`), and the picture onto the whole frame (scale `out` = 1 / into).
  // An office scene that zooms out draws the previous frame inside its screen with the SVG transform
  // `mini`, so the zoom starts exactly on that frame. (In 9:16 the screen is wide and the frame tall, so
  // the picture is a tall strip in the middle of the screen.)
  function zoomView(screen) {
    var s = screen || OFFICE.screen, hx = s[0] + 34, hy = s[1] + 34, hw = s[2] - 68, hh = s[3] - 68;
    var into = Math.min(hw / W, hh / H), out = 1 / into;
    var at = [(hx + hw / 2 - (into * W) / 2) / (1 - into), (hy + hh / 2 - (into * H) / 2) / (1 - into)];
    return { screen: s, at: at, into: into, out: out,
      mini: "translate(" + (at[0] * (1 - into)).toFixed(2) + "," + (at[1] * (1 - into)).toFixed(2) + ") scale(" + into.toFixed(5) + ")" };
  }
  // view: a zoomView, a wall screen box, or nothing (the standard screen). A plain [x, y] point is a
  // scene's own zoom origin, with fixed scales (earth-means-dirt computes its own).
  function enter(tl, cam, kind, view) {
    if (kind === "slide left") return tl.fromTo(cam, { x: W }, { x: 0, duration: 0.5, ease: "power3.out" }, 0);
    // (test for an array first: every array has an .at method)
    var z = view && !Array.isArray(view) ? view : view && view.length === 4 ? zoomView(view)
      : !view || (view[0] === OFFICE.screenAt[0] && view[1] === OFFICE.screenAt[1]) ? zoomView()
      : { at: view, into: V ? 0.22 : 0.34, out: V ? 4.7 : 2.9 };
    var origin = z.at[0] + "px " + z.at[1] + "px";
    if (kind === "zoom into the wall screen") {
      // the office stays around the screen as it grows, then the Earth frame fills the screen
      if (z.screen) {
        var room = document.createElement("div");
        room.style.cssText = "position:absolute;inset:0;";
        room.innerHTML = office(-2000, 0, { noHalo: true }).replace("</svg>", wallScreen.apply(null, z.screen) + "</svg>");
        cam.parentNode.insertBefore(room, cam);
        tl.fromTo(room, { scale: 1, transformOrigin: origin }, { scale: z.out, transformOrigin: origin, duration: 0.6, ease: "power2.inOut" }, 0);
        tl.set(room, { opacity: 0 }, 0.6);
      }
      tl.fromTo(cam, { scale: z.into, transformOrigin: origin }, { scale: 1, transformOrigin: origin, duration: 0.6, ease: "power2.inOut" }, 0);
    } else if (kind === "zoom out of the wall screen") {
      tl.fromTo(cam, { scale: z.out, transformOrigin: origin }, { scale: 1, transformOrigin: origin, duration: 0.6, ease: "power2.inOut" }, 0);
    }
  }
  // Draw on a KIT.tick (its path starts hidden).
  function drawTick(tl, el, t) {
    tl.fromTo(el, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.3, ease: "power2.out" }, t);
  }

  // A bean human, drawn around (0,0): body 84 x 124, feet at y=100.
  // o: { tone 0..3, light: "off"|"red"|"teal", arms: [[a1,a2],[b1,b2]] (deg, 0 = down), mouth: "flat"|"smile"|"frown"|"o", brows }
  var TONES = ["#F4E3CC", "#D9B48F", "#A87B57", "#6F4B33"];
  function bean(o) {
    o = o || {};
    var tone = TONES[(o.tone || 0) % TONES.length];
    var ink = C.line;
    var arms = o.arms || [[20, 10], [-20, -10]];
    function limb(x, y, a1, a2, len, cls) {
      var r1 = (a1 * Math.PI) / 180, r2 = (a2 * Math.PI) / 180;
      var ex = x + len * Math.sin(r1), ey = y + len * Math.cos(r1);
      var hx = ex + len * Math.sin(r2), hy = ey + len * Math.cos(r2);
      return '<g class="' + cls + '"><path d="M' + x + "," + y + " L" + ex.toFixed(1) + "," + ey.toFixed(1) + " L" + hx.toFixed(1) + "," + hy.toFixed(1) + '" fill="none" stroke="' + ink + '" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>' +
        '<circle cx="' + ex.toFixed(1) + '" cy="' + ey.toFixed(1) + '" r="4.5" fill="' + C.paper + '" stroke="' + ink + '" stroke-width="2.5"/>' +
        '<circle cx="' + hx.toFixed(1) + '" cy="' + hy.toFixed(1) + '" r="6" fill="' + tone + '" stroke="' + ink + '" stroke-width="3"/></g>';
    }
    var mouths = {
      flat: "M-9,-24 h18",
      smile: "M-11,-27 q11,10 22,0",
      frown: "M-10,-20 q10,-8 20,0",
      o: "M-4,-24 a4,4 0 1 0 8,0 a4,4 0 1 0 -8,0",
    };
    var light = o.light === "red" ? C.war : o.light === "teal" ? C.med : "#E9E1CC";
    return '<g class="bean">' +
      limb(-20, 52, 4, -4, 24, "leg-l") + limb(20, 52, -4, 4, 24, "leg-r") +
      '<path d="M0,-66 C34,-66 44,-36 42,-2 C40,38 30,62 0,62 C-30,62 -42,38 -42,0 C-42,-40 -30,-66 0,-66 Z" fill="' + tone + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<path d="M18,-50 C30,-36 33,-10 31,10 C29,34 22,48 8,55" fill="none" stroke="' + ink + '" stroke-width="2" opacity="0.5"/>' +
      '<path d="M22,-30 l8,8 M20,-14 l10,10 M18,2 l11,11 M15,18 l11,11 M10,34 l9,9" stroke="' + ink + '" stroke-width="1.6" opacity="0.5"/>' +
      (o.hair === 1 ? '<path d="M-26,-56 q26,-26 52,0 q-26,-10 -52,0 Z" fill="' + ink + '"/>' : o.hair === 2 ? '<path d="M-10,-66 q10,-16 20,0" fill="none" stroke="' + ink + '" stroke-width="4"/>' : "") +
      '<circle class="eye-l" cx="-13" cy="-38" r="4.6" fill="' + ink + '"/><circle class="eye-r" cx="13" cy="-38" r="4.6" fill="' + ink + '"/>' +
      (o.brows ? '<path class="brows" d="M-22,-52 l15,6 M22,-52 l-15,6" stroke="' + ink + '" stroke-width="4" stroke-linecap="round"/>' : "") +
      '<path class="mouth" d="' + (mouths[o.mouth || "flat"]) + '" fill="none" stroke="' + ink + '" stroke-width="3.4" stroke-linecap="round"/>' +
      '<circle class="chest-light" cx="0" cy="6" r="9" fill="' + light + '" stroke="' + ink + '" stroke-width="3"/>' +
      limb(-38, -6, arms[0][0], arms[0][1], 26, "arm-l") + limb(38, -6, arms[1][0], arms[1][1], 26, "arm-r") +
      "</g>";
  }

  // The humans (cartoon-style-bible.md section 3), drawn as the theme song draws them: stereotypes you read
  // from the silhouette. Each body is one big clothing shape (the fat cat an egg on stub legs, the politician
  // an inverted triangle with a jaw, the crook a hunched trench coat), a small 3/4 head with a big nose, one
  // stereotype tell, sharp polygons with thin navy lines, and print shading (orange edges on navy, halftone
  // dots on light cloth). Drawn around (0,0), feet at y 100.
  // o: { tone 0..3, outfit "shirt"|"dress"|"suit"|"labcoat"|"scrubs"|"overalls", color 0..3 (or colorHex),
  //      hair 0 short | 1 woman | 2 bald, hat "top"|"bowler"|"fedora"|"hard"|"curlers", tie "wide", tieColor,
  //      stache, cigar, glasses, mask, gloves, prop "monocle"|"megaphone"|"briefcase"|"poster"|"clipboard",
  //      hold (a prop between both hands) / holdL / holdR: "cash"|"bill"|"moneybag"|"briefcase"|"poster"|
  //      "clipboard"|"flask"|"cup"|"missile"|"magnifier", tall, light "red"|"teal",
  //      mood "smile"|"grin"|"smug"|"eager"|"sad"|"worried"|"cross"|"flat"|"greedy" ($ eyes),
  //      look "right"|"left" (no look faces right, eyes on the camera), arms [[a1, a2], [b1, b2]] (deg, 0 = down),
  //      brows, plain (the standard build: no random proportions), kind, head, hairStyle, build {...} }
  // A person without a kind gets a stable build of its own from its tone, color and outfit, so a crowd is a
  // cast of 1950s types. Parts: .arm-l .arm-r .leg-l .leg-r .head .eye .pupil .brows .mouth .chest-light;
  // KIT.rig(o) gives the pivots (shoulders, hips, neck, hands, mouth, eyes) in the person's units.
  // <!--head-end--> sits in the .head group in person units; <!--face-end--> in the face's own units.
  var BONE = "#F1EAD6"; // bone, for the skeletons and the Reaper
  var HUMANS = (function () {
    var ink = C.line;
    var SKIN = ["#F4E3CC", "#D9B48F", "#A87B57", "#6F4B33"];
    var CLOTH = ["#E5903B", "#5C6F8E", "#B47E52", "#E8B04A"];
    var PANTS = "#273049", NAVY = "#24304D", LAPEL = "#1A2238", WHITE = "#FBF6E6", COAT = "#3A4766", SCRUBS = "#DDE9E6";
    var LW = 4.4, uid = 0;
    function P(x, y) { return x.toFixed(1) + "," + y.toFixed(1); }
    function polyD(pts) { return "M" + pts.map(function (p) { return P(p[0], p[1]); }).join(" L") + " Z"; }
    function poly(pts) { return 'path d="' + polyD(pts) + '"'; }
    function flipX(pts) { return pts.map(function (p) { return [-p[0], p[1]]; }); }
    function copy(a, b) { var o = {}, k; for (k in a) o[k] = a[k]; for (k in b || {}) o[k] = b[k]; return o; }
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
    // A two-segment limb as one tapered polygon with a mitred (sharp) elbow or knee.
    function limb(s, w0, w1, w2) {
      var nA = nrm(s.x, s.y, s.ex, s.ey), nB = nrm(s.ex, s.ey, s.hx, s.hy);
      var sx = nA[0] + nB[0], sy = nA[1] + nB[1], q = sx * sx + sy * sy;
      function side(k) {
        var mid = q > 0.6 ? [[s.ex + (k * sx * w1) / q, s.ey + (k * sy * w1) / q]]
          : [[s.ex + (k * nA[0] * w1) / 2, s.ey + (k * nA[1] * w1) / 2], [s.ex + (k * nB[0] * w1) / 2, s.ey + (k * nB[1] * w1) / 2]];
        return [[s.x + (k * nA[0] * w0) / 2, s.y + (k * nA[1] * w0) / 2]].concat(mid, [[s.hx + (k * nB[0] * w2) / 2, s.hy + (k * nB[1] * w2) / 2]]);
      }
      return poly(side(1).concat(side(-1).reverse()));
    }
    // The first part of the upper arm (a short sleeve), as a tapered quad.
    function upperQuad(s, w0, w1, t) {
      var x1 = s.x + (s.ex - s.x) * t, y1 = s.y + (s.ey - s.y) * t, n = nrm(s.x, s.y, x1, y1);
      return poly([[s.x + n[0] * w0 / 2, s.y + n[1] * w0 / 2], [x1 + n[0] * w1 / 2, y1 + n[1] * w1 / 2], [x1 - n[0] * w1 / 2, y1 - n[1] * w1 / 2], [s.x - n[0] * w0 / 2, s.y - n[1] * w0 / 2]]);
    }
    // Print shading: halftone dots over the right part of a light shape (ids are unique on the page).
    function dots(pts, x0, op) {
      var id = "kit-hd" + ++uid;
      return '<defs><pattern id="' + id + 'd" width="3.6" height="3.6" patternUnits="userSpaceOnUse"><circle cx="1.8" cy="1.8" r="1" fill="' + ink + '"/></pattern><clipPath id="' + id + 'c"><path d="' + polyD(pts) + '"/></clipPath></defs>' +
        '<rect x="' + x0.toFixed(1) + '" y="-240" width="200" height="400" fill="url(#' + id + 'd)" opacity="' + (op || 0.3) + '" clip-path="url(#' + id + 'c)"/>';
    }
    function hatSvg(kind, cx, hatTop) {
      return {
        top: '<rect x="' + (cx - 15) + '" y="' + (hatTop - 36) + '" width="30" height="36" fill="' + ink + '"/><rect x="' + (cx - 15) + '" y="' + (hatTop - 11) + '" width="30" height="6" fill="' + C.orange + '"/><path d="M' + (cx - 27) + "," + (hatTop + 2) + " L" + (cx - 23) + "," + (hatTop - 4) + " H" + (cx + 23) + " L" + (cx + 27) + "," + (hatTop + 2) + ' Z" fill="' + ink + '"/>',
        bowler: '<path d="M' + (cx - 17) + "," + (hatTop + 1) + " L" + (cx - 13) + "," + (hatTop - 16) + " L" + cx + "," + (hatTop - 21) + " L" + (cx + 13) + "," + (hatTop - 16) + " L" + (cx + 17) + "," + (hatTop + 1) + ' Z" fill="' + ink + '"/><path d="M' + (cx - 28) + "," + (hatTop + 4) + " L" + (cx - 22) + "," + (hatTop - 1) + " H" + (cx + 22) + " L" + (cx + 28) + "," + (hatTop + 4) + ' Z" fill="' + ink + '"/>',
        // pulled low over the eyes, the brim tipped down in front
        fedora: '<path d="M' + (cx - 17) + "," + (hatTop + 9) + " L" + (cx - 14) + "," + (hatTop - 10) + " L" + (cx - 3) + "," + (hatTop - 6) + " L" + (cx + 6) + "," + (hatTop - 12) + " L" + (cx + 17) + "," + (hatTop - 6) + " L" + (cx + 18) + "," + (hatTop + 9) + ' Z" fill="' + NAVY + '" stroke="' + ink + '" stroke-width="2.2" stroke-linejoin="miter"/><path d="M' + (cx - 17) + "," + (hatTop + 4) + " H" + (cx + 18) + '" stroke="' + C.orange + '" stroke-width="3"/><path d="M' + (cx - 30) + "," + (hatTop + 6) + " L" + (cx - 18) + "," + (hatTop + 7) + " H" + (cx + 22) + " L" + (cx + 38) + "," + (hatTop + 16) + " L" + (cx + 20) + "," + (hatTop + 12) + " H" + (cx - 20) + ' Z" fill="' + NAVY + '" stroke="' + ink + '" stroke-width="2.2" stroke-linejoin="miter"/>',
        hard: '<path d="M' + (cx - 23) + "," + (hatTop + 5) + " L" + (cx - 18) + "," + (hatTop - 13) + " L" + cx + "," + (hatTop - 20) + " L" + (cx + 18) + "," + (hatTop - 13) + " L" + (cx + 23) + "," + (hatTop + 5) + ' Z" fill="' + C.yellow + '" stroke="' + ink + '" stroke-width="2.6" stroke-linejoin="miter"/><path d="M' + (cx - 30) + "," + (hatTop + 8) + " L" + (cx - 26) + "," + (hatTop + 3) + " H" + (cx + 26) + " L" + (cx + 30) + "," + (hatTop + 8) + ' Z" fill="' + C.yellow + '" stroke="' + ink + '" stroke-width="2.2" stroke-linejoin="miter"/>',
        curlers: [-14, 0, 14].map(function (dx) { return '<rect x="' + (cx + dx - 6) + '" y="' + (hatTop - 5) + '" width="12" height="11" rx="2" fill="#E9B4C1" stroke="' + ink + '" stroke-width="2"/>'; }).join(""),
      }[kind] || "";
    }
    // Props held in a hand (or between both), drawn around the hand.
    function cashStack(n) {
      var out = "";
      for (var i = 0; i < n; i++) out += '<rect x="' + (-17 + (i % 2)) + '" y="' + (-i * 4.2) + '" width="34" height="5" fill="' + C.money + '" stroke="' + ink + '" stroke-width="1.4"/>';
      return out + '<rect x="-4" y="' + (-n * 4.2 + 3) + '" width="8" height="' + (n * 4.2 + 2) + '" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="1.2"/>';
    }
    var PROPS = {
      cash: function () { return '<g transform="translate(0,-4)">' + cashStack(5) + "</g>"; },
      bill: function () { return '<g transform="rotate(-20)"><rect x="-15" y="-9" width="30" height="16" fill="' + C.money + '" stroke="' + ink + '" stroke-width="1.8"/><ellipse cx="0" cy="-1" rx="4.5" ry="5" fill="' + C.cream + '" stroke="' + C.moneyDark + '" stroke-width="1.2"/></g>'; },
      moneybag: function () { return solid([poly([[-6, -8], [6, -8], [3, -3], [14, 6], [16, 18], [8, 26], [-8, 26], [-16, 18], [-14, 6], [-3, -3]])], C.money, 3) + line("M-6,-3 H6", ink, 2.4) + '<path d="M3,6 C-4,4 -4,10 0,11 C4,12 4,18 -3,16 M0,4 V19" fill="none" stroke="' + C.cream + '" stroke-width="2.4"/>'; },
      briefcase: function () { return solid([poly([[-17, 6], [17, 6], [17, 30], [-17, 30]])], "#6B4A2F", 2.6) + line("M-6,6 V1 H6 V6", ink, 2.2) + '<g transform="translate(6,6) rotate(-25)">' + solid([poly([[-6, -12], [8, -12], [8, 0], [-6, 0]])], C.money, 1.8) + "</g>"; },
      poster: function () { return '<g transform="translate(-14,-20)">' + solid([poly([[-20, -26], [20, -26], [20, 26], [-20, 26]])], C.paper, 2.6) + '<text x="0" y="-4" text-anchor="middle" font-family="Oswald" font-size="11" fill="' + C.war + '">BUY</text><text x="0" y="10" text-anchor="middle" font-family="Oswald" font-size="11" fill="' + ink + '">BONDS</text></g>'; },
      clipboard: function () { return solid([poly([[-4, -26], [18, -26], [18, 6], [-4, 6]])], "#B98A55", 2.2) + '<rect x="0" y="-22" width="14" height="24" fill="' + C.paper + '"/>' + line("M2,-16 H12 M2,-11 H12 M2,-6 H9", ink, 1.2); },
      flask: function () { return solid([poly([[-3, -22], [3, -22], [3, -12], [11, 4], [-11, 4], [-3, -12]])], WHITE, 2.4) + '<path d="M' + P(-8, -2) + " L" + P(8, -2) + " L" + P(10.5, 3.5) + " L" + P(-10.5, 3.5) + ' Z" fill="' + C.med + '"/><circle cx="2" cy="-27" r="2.5" fill="' + C.med + '"/><circle cx="-2" cy="-33" r="1.8" fill="' + C.med + '"/>'; },
      cup: function () { return solid([poly([[-7, -10], [7, -10], [5, 2], [-5, 2]])], WHITE, 2.2) + '<circle cx="-1.5" cy="-12" r="2.2" fill="' + C.war + '"/><circle cx="2.5" cy="-12.5" r="2.2" fill="' + C.med + '"/>'; },
      // a small grinning missile, cradled like a baby
      missile: function () { return '<g transform="translate(0,-6) rotate(-14)">' + solid([poly([[-34, -7], [14, -7], [30, 0], [14, 7], [-34, 7]]), poly([[-34, -7], [-44, -17], [-40, -7]]), poly([[-34, 7], [-44, 17], [-40, 7]])], C.war, 2.6) + '<path d="M14,-7 L30,0 L14,7 Z" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="2"/>' + line("M-4,2 Q2,6 8,2", ink, 1.8) + '<circle cx="-2" cy="-2.5" r="1.6" fill="' + ink + '"/><circle cx="6" cy="-2.5" r="1.6" fill="' + ink + '"/></g>'; },
      magnifier: function () { return line("M0,0 L-6,14", ink, 5) + '<circle cx="5" cy="-11" r="11" fill="#FFFFFF" fill-opacity="0.35" stroke="' + ink + '" stroke-width="3.4"/>'; },
    };

    // ── Builds and the recurring cast ──────────────────────────────────
    var BUILD0 = { hs: 0.92, legs: 1, th: 1, tw: 1, neck: 0.8, nose: 1, chin: 1, arms: 1, armL: 1, feet: 1.15, hand: 1.15, hunch: 0, legPose: null };
    // The cast's signature props and pose come with its default arms; a scene that poses the arms gets the
    // person without them (pass hold/holdL/holdR to keep one).
    var CAST = {
      richHuman: { tone: 0, kind: "egg", head: "jowls", mood: "smug", hat: "top", stache: true, prop: "monocle", cigar: true, hold: "cash", arms: [[22, 72], [-22, -72]], build: { hs: 0.8, legs: 0.42, th: 1.25, tw: 1.08, neck: 0, nose: 1.2, feet: 1 } },
      politician: { tone: 1, kind: "vee", head: "jaw", hairStyle: "slick", mood: "grin", tie: "wide", flagPin: true, arms: [[-8, -3], [150, 172]], holdR: "bill", build: { hs: 1, legs: 1.08, tw: 1.1, neck: 0.5, chin: 1.25 } },
      lobbyist: { tone: 2, kind: "coat", head: "long", hat: "fedora", mask: true, gloves: true, mood: "smug", arms: [[-10, -4], [40, 150]], holdR: "cash", holdL: "briefcase", build: { hs: 0.9, legs: 0.95, th: 1.05, neck: 0.4, nose: 1.8, hunch: 14, legPose: [[-12, -26], [25, -5]] } },
      weaponsMaker: { tone: 3, kind: "barrel", head: "jaw", colorHex: "#5C6F8E", hat: "hard", mood: "grin", cigar: true, arms: [[32, 84], [-32, -84]], hold: "missile", build: { hs: 0.66, tw: 1.15, arms: 1.35, legs: 0.78, neck: 0, hand: 1.35 } },
      scientist: { tone: 3, kind: "lab", hair: 1, hairStyle: "bun", glasses: true, mood: "eager", arms: [[-30, -120], [-10, -4]], holdL: "flask", holdR: "clipboard", build: { hs: 1.08, legs: 0.95, neck: 0.8, hunch: 6 } },
      grandma: { tone: 0, kind: "pear", hair: 1, hairColor: "#B9B5AE", hat: "curlers", glasses: true, color: 3, mood: "smile", arms: [[-150, -172], [-10, -4]], holdL: "poster", build: { hs: 1, legs: 0.62, th: 0.88, hunch: 14, nose: 1.4, feet: 0.95 } },
      orderly: { tone: 2, kind: "twig", head: "plain", hair: 2, mood: "flat", arms: [[-6, -2], [60, 92]], holdR: "cup", build: { hs: 0.72, legs: 1.3, th: 1.2, neck: 2.4, armL: 1.25 } },
      loudHuman: { tone: 1, kind: "shirt", color: 0, prop: "megaphone", mood: "smile", build: { legs: 1.1, tw: 0.85 } },
    };
    function hash(o) {
      var h = 2166136261, s = [o.tone || 0, o.color === undefined ? -1 : o.color, o.outfit || "", o.hair || 0, o.seed || 0].join("|");
      for (var i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
      return h >>> 0;
    }
    var PLAIN_KIND = { suit: "vee", shirt: "shirt", dress: "hourglass", overalls: "barrel", labcoat: "lab", scrubs: "twig" };
    // An everyday human: the outfit picks a family of shapes, the hash picks one and its proportions.
    function everyday(o) {
      var r = rng(hash(o)), pick = function (a) { return a[Math.floor(r() * a.length)]; }, between = function (a, z) { return a + (z - a) * r(); };
      var woman = o.hair === 1, outfit = o.outfit || (woman ? "dress" : "shirt");
      var kind = { suit: pick(["box", "vee", "egg", "box"]), shirt: pick(["shirt", "shirt", "barrel", "twig"]), dress: pick(["hourglass", "hourglass", "pear"]), overalls: "barrel", labcoat: "lab", scrubs: "twig" }[outfit] || "shirt";
      var b = { hs: between(0.82, 1.06), legs: between(0.78, 1.15), th: between(0.9, 1.12), tw: between(0.88, 1.15), neck: between(0.3, 1.4), nose: between(0.9, 1.9), chin: between(0.9, 1.3) };
      if (kind === "egg") { b.legs = between(0.45, 0.65); b.hs = between(0.78, 0.9); b.neck = 0; }
      if (kind === "twig") { b.legs = between(1.15, 1.32); b.neck = between(1.2, 2.2); b.hs = between(0.72, 0.88); }
      return { kind: kind, b: b, head: woman ? "woman" : pick(["plain", "jaw", "jowls", "plain", "long"]), hairStyle: woman ? pick(["flip", "bun", "flip"]) : o.hair === 2 ? "bald" : pick(["short", "slick", "short", "bald"]), hat: !woman && r() < 0.25 ? "fedoraUp" : null, glasses: r() < 0.2 };
    }
    function resolve(o) {
      var woman = o.hair === 1, d = o.kind ? { kind: o.kind, b: {} } : o.plain ? { kind: PLAIN_KIND[o.outfit || (woman ? "dress" : "shirt")], b: o.outfit === "overalls" ? { tw: 0.6 } : {} } : everyday(o), b = copy(BUILD0, d.b), k;
      if (o.tall) { b.legs = Math.max(b.legs, 1.3); b.neck = Math.max(b.neck, 2); b.th = Math.max(b.th, 1.15); }
      for (k in o.build || {}) b[k] = o.build[k];
      return {
        kind: d.kind, b: b, head: o.head || d.head || (woman ? "woman" : "plain"),
        hairStyle: o.hairStyle || d.hairStyle || (woman ? "flip" : o.hair === 2 ? "bald" : "short"),
        hat: o.hat !== undefined ? o.hat : d.hat, glasses: o.glasses || d.glasses,
      };
    }
    function lay(b) {
      var L = 37 * b.legs, lp = b.legPose || [[-6, -2], [6, 2]];
      var drop = function (a) { return Math.cos((a[0] * Math.PI) / 180) + Math.cos((a[1] * Math.PI) / 180); };
      var hipY = 99.8 - L * Math.max(drop(lp[0]), drop(lp[1])), sY = hipY - 52 * b.th;
      return { L: L, lp: lp, hipY: hipY, sY: sY, T: sY - 4, Wy: hipY - 8 * b.th, hy: sY - 4 - 10 * b.neck - 19 * b.hs };
    }
    // Where each kind's arms hang: shoulder pivot (±ax, ay) and the length of each arm segment.
    function armGeo(kind, b, l) {
      var T = l.T, tw = b.tw;
      return {
        egg: [30 * tw, T + 9, 22], vee: [27 * tw, T + 3, 26], box: [26 * tw, T + 3, 26], coat: [19, T + 4, 26], hourglass: [13, T + 3, 25],
        lab: [19, T + 3, 26], barrel: [30 * tw, T + 6, 25], pear: [11, T + 4, 24], twig: [15, T + 3, 26], shirt: [17 * tw, T + 4, 26],
      }[kind];
    }
    // The pivots and points of a person, in the person's units. Shoulders, hips, neck and head are where the
    // part groups rotate (their svgOrigin); hands, mouth and eyes are where things touch them, after the lean.
    function rig(o) {
      o = o || {};
      if (o.skeleton) o = copy(o, { skeleton: false });
      var R = resolve(o), b = R.b, l = lay(b), g = armGeo(R.kind, b, l), dir = o.look === "right" ? 1 : o.look === "left" ? -1 : 0, f = dir || 1;
      var arms = o.arms || CAST_ARMS(o), len = g[2] * b.armL, hx = 7 * (0.7 + 0.3 * b.tw);
      var th = (b.hunch * f * Math.PI) / 180, cs = Math.cos(th), sn = Math.sin(th);
      var lean = function (p) { var x = p[0], y = p[1] - l.hipY; return [x * cs - y * sn, l.hipY + x * sn + y * cs]; };
      var hand = [0, 1].map(function (i) { var s = seg((i ? 1 : -1) * g[0], g[1], arms[i], len); return [s.hx, s.hy]; });
      var my = 12 + 2.5 * (b.chin - 1) + (R.head === "jaw" ? 2 : 0);
      return {
        kind: R.kind, build: b, hipY: l.hipY, hy: l.hy, hs: b.hs, facing: f, lean: b.hunch * f, armLength: len,
        shoulder: [[-g[0], g[1]], [g[0], g[1]]], hip: [[-hx, l.hipY], [hx, l.hipY]], neck: [dir * 2, l.hy + 18 * b.hs], head: [dir * 2, l.hy],
        handLocal: hand, hand: hand.map(lean), mouth: lean([dir * 2 + f * 7 * b.hs, l.hy + my * b.hs]), eyes: lean([dir * 2 + f * 4.2 * b.hs, l.hy - 4 * b.hs]),
        top: lean([dir * 2, l.hy - 23 * b.hs]), faceEyes: [4.2, -4],
      };
    }
    function CAST_ARMS(o) { return [[20, 10], [-20, -10]]; }

    // ── Heads: 3/4 view facing +x, around (0, 0) ─────────────────────
    function headPts(shape, b) {
      var n = b.nose - 1, c = b.chin - 1;
      return {
        plain: [[-16, -12], [-10, -21], [4, -23], [14, -16], [16, -6], [23 + 9 * n, 4 + 3 * n], [17, 6 + 1.5 * n], [17.5, 11], [16, 19 + 5 * c], [10, 24 + 6 * c], [-4, 22 + 6 * c], [-13, 13 + 3 * c], [-16, 2]],
        jaw: [[-15, -13], [-10, -22], [4, -24], [14, -17], [16, -7], [23 + 9 * n, 3 + 3 * n], [17, 5 + 1.5 * n], [18.5, 11], [19, 22 + 5 * c], [13, 28 + 6 * c], [-6, 27 + 6 * c], [-16, 17 + 3 * c], [-16, 2]],
        jowls: [[-15, -14], [-9, -22], [4, -23], [13, -17], [15, -8], [24 + 6 * n, -1], [25 + 6 * n, 5], [19, 8], [21, 15], [17, 22], [7, 26 + 3 * c], [-8, 25 + 3 * c], [-18, 18], [-20, 6], [-17, -4]],
        long: [[-14, -14], [-9, -24], [4, -25], [13, -18], [15, -7], [26 + 10 * n, 6 + 3 * n], [17, 7 + n], [17, 12], [14, 21 + 6 * c], [6, 30 + 7 * c], [-5, 23 + 6 * c], [-12, 12], [-14, 0]],
        woman: [[-15, -12], [-9, -21], [4, -22], [13, -15], [15, -5], [19.5 + 6 * n, 3 + 2 * n], [15.5, 5.5 + n], [16, 10], [13, 18 + 4 * c], [5, 24 + 6 * c], [-5, 19 + 5 * c], [-12, 10 + 2 * c], [-15, 1]],
      }[shape];
    }
    var EYES = [[-2.5, 6.2, 3.7], [10.8, 4.6, 3.4]]; // [x, half width, height] of the near and the far eye
    function face(o, R, mood, skin) {
      var b = R.b, woman = R.head === "woman", px = o.look ? 1.6 : 0, my = 12 + 2.5 * (b.chin - 1) + (R.head === "jaw" ? 2 : 0);
      var eyes = EYES.map(function (e, i) {
        var x = e[0], y = -4, rx = e[1] * (woman ? 1.1 : 1), ry = e[2] * (mood === "eager" ? 1.5 : 1);
        if (mood === "greedy") return '<g class="eye"><path d="M' + P(x + 3, y - 4) + " C" + P(x + 3, y - 7) + " " + P(x - 3, y - 7) + " " + P(x - 3, y - 4) + " C" + P(x - 3, y - 1) + " " + P(x + 3, y - 1) + " " + P(x + 3, y + 2) + " C" + P(x + 3, y + 5) + " " + P(x - 3, y + 5) + " " + P(x - 3, y + 2) + " M" + P(x, y - 8.5) + " V" + (y + 6.5) + '" fill="none" stroke="' + C.moneyDark + '" stroke-width="2.4"/></g>';
        var top = mood === "flat" || mood === "smug" ? y - ry * 0.55 : mood === "cross" ? y - ry * 1.1 : y - ry * 1.7;
        var bot = mood === "smile" || mood === "grin" || mood === "smug" ? y + ry * 0.45 : y + ry * 1.1;
        return '<g class="eye"><path d="M' + P(x - rx, y) + " Q" + P(x, top) + " " + P(x + rx, y - 0.4) + " Q" + P(x, bot) + " " + P(x - rx, y) + ' Z" fill="' + WHITE + '" stroke="' + ink + '" stroke-width="1"/>' +
          '<circle class="pupil" cx="' + (x + px * (i ? 0.7 : 1)).toFixed(1) + '" cy="' + (y - 0.3).toFixed(1) + '" r="' + (mood === "eager" ? 1.8 : mood === "worried" ? 1.6 : 2) + '" fill="' + ink + '"/>' +
          '<path d="M' + P(x - rx - 0.8, y + 0.4) + " Q" + P(x, top - 0.6) + " " + P(x + rx + 0.6, y - 0.6) + '" fill="none" stroke="' + ink + '" stroke-width="' + (woman ? 2.4 : 1.9) + '" stroke-linecap="round"/>' +
          (woman ? line("M" + P(i ? x + rx : x - rx - 0.5, y - 0.6) + " l" + (i ? 2.4 : -3.2) + ",-2.6", ink, 2) : "") + "</g>";
      }).join("");
      var BR = { smile: [-8.5, -11, -9.5], grin: [-9, -12, -10], eager: [-10.5, -13.5, -11.5], sad: [-7.5, -9, -11], worried: [-7, -9, -12], cross: [-11, -9, -6.5], flat: [-8.5, -8.5, -8.5], smug: [-9, -10, -12.5], greedy: [-11, -13, -11] }[mood] || [-8.5, -11, -9.5];
      var brows = EYES.map(function (e, i) {
        var x = e[0], w = e[1] + 0.8, y = -4, bb = i ? [BR[2], BR[1], BR[0]] : BR;
        if (mood === "sad" || mood === "cross" || mood === "worried") bb = i ? [BR[2], (BR[1] + BR[2]) / 2, BR[0]] : BR;
        return "M" + P(x - w, y + bb[0]) + " L" + P(x - w * 0.1, y + bb[1]) + " L" + P(x + w, y + bb[2]);
      }).join(" ");
      var grin = "M" + P(-1, my - 1) + " Q" + P(7, my + 1) + " " + P(15.5, my - 2) + " Q" + P(9, my + 8.5) + " " + P(-1, my - 1) + " Z";
      var mouth = {
        smile: grin, greedy: grin,
        grin: "M" + P(-4, my - 2) + " L" + P(17, my - 3) + " L" + P(12, my + 8) + " L" + P(2, my + 8) + " Z",
        smug: "M" + P(0, my + 1) + " Q" + P(8, my + 3) + " " + P(15, my - 3),
        eager: "M" + P(1, my - 1) + " L" + P(14, my - 1.5) + " L" + P(10.5, my + 7) + " L" + P(4, my + 7) + " Z",
        sad: "M" + P(0, my + 3) + " Q" + P(7, my - 2) + " " + P(14, my + 2),
        worried: "M" + P(0, my + 2) + " L" + P(4, my) + " L" + P(8, my + 2) + " L" + P(12, my) + " L" + P(15, my + 1.5),
        cross: "M" + P(1, my + 1) + " L" + P(14, my + 0.5) + " M" + P(1, my + 1) + " l-1.5,2",
        flat: "M" + P(2, my + 1) + " L" + P(13, my + 0.5),
      }[mood] || "M" + P(2, my + 1) + " L" + P(13, my + 0.5);
      var filled = mood === "smile" || mood === "grin" || mood === "greedy" ? WHITE : mood === "eager" ? ink : "none";
      var teeth = mood === "grin" ? line("M" + P(2.5, my - 2.5) + " V" + (my + 8) + " M" + P(7.5, my - 2.6) + " V" + (my + 8) + " M" + P(12.5, my - 2.8) + " V" + (my + 8) + " M" + P(-1, my + 3) + " H16", ink, 1.1) : "";
      var crease = mood === "smile" || mood === "grin" || mood === "smug" || mood === "greedy" ? line("M" + P(-3.5, my - 5) + " Q" + P(-5, my) + " " + P(-2, my + 3), ink, 1.5) : "";
      var hairCol = o.hairColor || ink, hs = ' fill="' + hairCol + '" stroke="' + ink + '" stroke-width="1.6" stroke-linejoin="miter"';
      var hair = {
        short: [[-16, 4], [-18, -8], [-14, -20], [-4, -27], [10, -28.5], [21, -22], [16, -18.5], [13, -14.5], [4, -15.5], [-6, -13], [-9, -7], [-10, 3], [-13, 4]],
        slick: [[-16, 2], [-18, -10], [-12, -24], [2, -30], [18, -28], [24, -21], [15, -17], [12, -14], [2, -16], [-7, -13], [-10, -6], [-11, 2]],
        bald: [[-16, 3], [-18, -6], [-15, -13], [-11, -8], [-10, 2]],
        flip: [[-15, -11], [-10, -22], [4, -24.5], [15, -18], [16.5, -13], [12, -13.5], [9.5, -11.5], [7, -14], [2, -13.5], [-1, -11.5], [-4, -14], [-11, -12.5], [-12, -5]],
        bun: [[-15, -9], [-11, -21], [4, -24], [15, -17], [16, -12], [6, -16], [-6, -13], [-12, -4]],
      }[R.hairStyle];
      var back = R.hairStyle === "flip" ? "<" + poly([[-22, 13], [-30, 18], [-25, 5], [-25, -14], [-15, -27], [2, -31], [17, -26], [24, -14], [23, 6], [30, 15], [17, 13], [12, 2], [-10, 2]]) + hs + "/>"
        : R.hairStyle === "bun" ? "<" + poly([[-24, -22], [-16, -32], [-6, -30], [-8, -20], [-18, -16]]) + hs + "/>" : "";
      var shine = R.hairStyle === "slick" ? line("M" + P(-4, -25) + " L" + P(12, -25.5), C.peri, 2.2) : R.hairStyle === "bald" ? line("M" + P(-6, -18) + " L" + P(3, -20.5), "#FFFFFF", 2.2) : "";
      var ear = "<" + poly([[-12, -3], [-17.5, -2], [-18, 6], [-12, 8]]) + ' fill="' + skin + '" stroke="' + ink + '" stroke-width="2" stroke-linejoin="miter"/>';
      var chinLine = R.head === "jowls" ? line("M" + P(-10, 20) + " Q" + P(3, 25) + " " + P(15, 18), ink, 1.6) + line("M" + P(17, 11) + " Q" + P(20, 14) + " " + P(17, 18), ink, 1.4) : R.head === "jaw" ? line("M" + P(7, 25 + 6 * (b.chin - 1)) + " v-3", ink, 1.4) : "";
      var stache = o.stache ? "<" + poly([[1, my - 3], [9, my - 5.5], [17, my - 4.5], [26, my - 10], [21, my - 1], [9, my - 1.5], [0, my - 0.5], [-7, my - 7]]) + ' fill="' + ink + '"/>' : "";
      var monocle = o.prop === "monocle" ? '<circle cx="' + EYES[1][0] + '" cy="-4" r="6.4" fill="none" stroke="' + C.yellow + '" stroke-width="2.4"/>' + line("M" + (EYES[1][0] + 5) + ",0 q7,14 0,30", C.yellow, 1.5) : "";
      var glasses = R.glasses ? '<path d="M-10,-10 H5 L4,0 H-9 Z M6.5,-10 L16,-9.5 L15.5,-0.5 L7,0 Z" fill="#FFFFFF" fill-opacity="0.2" stroke="' + ink + '" stroke-width="2.6" stroke-linejoin="miter"/>' + line("M5,-7 H6.5 M-10,-7 L-17,-5", ink, 2.6) + (woman ? line("M-10,-10 L-13,-13 M16,-9.5 L19,-13", ink, 2.6) : "") : "";
      var mask = o.mask ? '<path d="M-17,-11 L18,-12 L19,-1 L13,1 L9,-3 L4,1 L-4,-2 L-10,1 L-17,-1 Z" fill="' + ink + '"/>' +
        [0, 1].map(function (i) { var x = EYES[i][0]; return '<path d="M' + P(x - 4, -4.5) + " Q" + P(x, -8) + " " + P(x + 4, -5) + " Q" + P(x, -2) + " " + P(x - 4, -4.5) + ' Z" fill="' + WHITE + '"/><circle cx="' + (x + 1.2) + '" cy="-4.8" r="1.5" fill="' + ink + '"/>'; }).join("") : "";
      var cigar = o.cigar ? '<g transform="translate(' + P(13, my + 2) + ') rotate(-12)">' + solid([poly([[0, -2.6], [22, -2.6], [22, 2.6], [0, 2.6]])], "#7A4A2A", 2) + '<rect x="19" y="-2.6" width="4" height="5.2" fill="#C9C2B5"/><rect x="5" y="-2.6" width="3" height="5.2" fill="' + C.war + '"/></g>' +
        '<path d="M' + P(37, my - 6) + " q-5,-6 0,-11 q5,-6 0,-11" + '" fill="none" stroke="#8C8782" stroke-width="2.4" stroke-linecap="round"/>' : "";
      return back + solid([poly(headPts(R.head, b))], skin, LW) + ear + chinLine + (hair ? "<" + poly(hair) + hs + "/>" : "") + shine + eyes + mask + glasses +
        '<path class="brows" d="' + brows + '" fill="none" stroke="' + ink + '" stroke-width="' + (woman ? 1.9 : 2.6) + '" stroke-linejoin="miter"' + (o.mask ? ' opacity="0"' : "") + "/>" +
        '<path class="mouth" d="' + mouth + '" fill="' + filled + '" stroke="' + ink + '" stroke-width="' + (filled !== "none" ? 1.8 : 2.2) + '" stroke-linecap="round" stroke-linejoin="miter"/>' +
        teeth + crease + stache + cigar + monocle;
    }

    function person(o) {
      o = o || {};
      if (o.skeleton) return skeleton(o);
      if (o.charred) {
        var plain = copy(o, { charred: false, mood: "flat", stache: false, cigar: false, hold: null, holdL: null, holdR: null, prop: o.prop === "megaphone" ? "megaphone" : null, hairStyle: "bald" });
        if (!o.keepHat) plain.hat = null;
        return charify(person(plain), o);
      }
      if (o.prop === "briefcase" || o.prop === "clipboard") o = copy(o, { prop: null, holdR: o.holdR || o.prop });
      if (o.prop === "poster") o = copy(o, { prop: null, holdL: o.holdL || "poster" });
      var R = resolve(o), b = R.b, l = lay(b), T = l.T, hipY = l.hipY, Wy = l.Wy, kind = R.kind, g = armGeo(kind, b, l);
      var skin = SKIN[(o.tone || 0) % SKIN.length];
      var cloth = o.colorHex || CLOTH[(o.color === undefined ? o.tone || 0 : o.color) % CLOTH.length];
      var mood = o.mood || (o.mouth === "smile" ? "smile" : o.mouth === "o" ? "eager" : o.mouth === "frown" ? "sad" : "flat");
      if (o.brows && mood === "flat") mood = "cross";
      var dir = o.look === "right" ? 1 : o.look === "left" ? -1 : 0, f = dir || 1, tw = b.tw;
      var arms = o.arms || CAST_ARMS(o);
      var woman = R.head === "woman";
      var V = function (depth, col) { return '<path d="M-6,' + (T - 3) + " L0," + (T + depth) + " L6," + (T - 3) + ' Z" fill="' + (col || WHITE) + '"/>'; };
      var tie = function (len, wide) {
        return wide ? solid([poly([[-3, T + 1], [3, T + 1], [12, T + len - 8], [0, T + len + 2], [-12, T + len - 8]])], o.tieColor || C.war, 2.4)
          : solid([poly([[-2, T + 1], [2, T + 1], [3.5, T + len - 5], [0, T + len], [-3.5, T + len - 5]])], o.tieColor || C.orange, 2);
      };
      var lapels = function (len) {
        var L = [[-6, T - 3], [-13, T + 1], [-9.5, T + 7], [-13, T + 9], [-2.5, T + len], [0, T + len - 4]];
        return solid([poly(L), poly(flipX(L))], LAPEL, 2.2) + line("M" + P(-13, T + 9) + " L" + P(-2.5, T + len) + " M" + P(13, T + 9) + " L" + P(2.5, T + len), C.orange, 1.6);
      };
      var collar = V(7, skin) + solid([poly([[-1, T + 6], [-9, T - 3.5], [-10.5, T + 5]]), poly([[1, T + 6], [9, T - 3.5], [10.5, T + 5]])], WHITE, 2.6);
      var belt = function (y, w) { return '<rect x="' + -w + '" y="' + y + '" width="' + 2 * w + '" height="4.5" fill="' + ink + '"/><rect x="-3" y="' + (y - 0.5) + '" width="6" height="5.5" fill="' + C.yellow + '" stroke="' + ink + '" stroke-width="1.4"/>'; };
      var buttons = function (ys, x) { return ys.map(function (y) { return '<rect x="' + ((x || 0) - 1.3) + '" y="' + y.toFixed(1) + '" width="2.6" height="2.6" fill="' + C.cream + '"/>'; }).join(""); };
      var pocketSq = function (x, y) { return '<path d="M' + P(x, y) + " l7,0 l-2,-4.5 l-2,2.5 l-1.5,-2.5 Z" + '" fill="' + C.orange + '"/>'; };
      var edge = function (d) { return line(d, C.orange, 1.6); };

      // Each kind: the body, its sleeves (sl: widths at shoulder, elbow, wrist; bare: skin forearms with a short
      // sleeve), the trousers and the chest light.
      var KINDS = {
        egg: function () {
          var w = 44 * tw, bot = hipY + 14, h = bot - T;
          var pts = [[-20, T - 1], [20, T - 1], [w * 0.8, T + 10], [w, T + h * 0.42], [w * 0.92, T + h * 0.75], [w * 0.55, bot - 2], [0, bot + 1], [-w * 0.55, bot - 2], [-w * 0.92, T + h * 0.75], [-w, T + h * 0.42], [-w * 0.8, T + 10]];
          return { svg: solid([poly(pts)], NAVY) + V(20) + tie(28) + lapels(46) + line("M" + P(-22, T + h * 0.55) + " Q" + P(-8, T + h * 0.66) + " " + P(8, T + h * 0.55), C.yellow, 2) +
            buttons([T + h * 0.5, T + h * 0.68]) + pocketSq(-w * 0.62, T + 18) + edge("M" + P(w * 0.82, T + 14) + " L" + P(w * 0.97, T + h * 0.42)), sl: [15, 12.5, 11], pants: NAVY, light: [16, T + 16] };
        },
        vee: function () {
          var w = 33 * tw, pts = [[-6, T - 3], [6, T - 3], [w - 4, T - 1], [w, T + 4], [13, Wy], [15, hipY + 8], [2, hipY + 8], [0, hipY + 4], [-2, hipY + 8], [-15, hipY + 8], [-13, Wy], [-w, T + 4], [-w + 4, T - 1]];
          return { svg: solid([poly(pts)], NAVY) + V(24) + tie(28, o.tie === "wide") + lapels(28) + buttons([hipY - 3]) + pocketSq(-w * 0.62, T + 14) + edge("M" + P(w - 2, T + 5) + " L" + P(14.5, Wy)) +
            (o.flagPin ? '<rect x="' + w * 0.42 + '" y="' + (T + 9) + '" width="7" height="5" fill="' + C.war + '"/><rect x="' + w * 0.42 + '" y="' + (T + 9) + '" width="3" height="2.5" fill="' + NAVY + '"/>' : ""), sl: [11, 9, 7.5], pants: NAVY, light: [w * 0.35, T + 18] };
        },
        box: function () {
          var w = 31 * tw, pts = [[-w, T], [w, T], [w - 2, hipY + 8], [2, hipY + 8], [0, hipY + 4], [-2, hipY + 8], [-w + 2, hipY + 8]];
          return { svg: solid([poly(pts)], o.colorHex || NAVY) + V(24) + tie(26) + lapels(30) + buttons([hipY - 6, hipY]) + edge("M" + P(w - 3, T + 4) + " L" + P(w - 4.5, hipY + 4)), sl: [12, 10, 8], pants: NAVY, light: [w * 0.4, T + 16] };
        },
        coat: function () {
          var pts = [[-8, T - 2], [8, T - 2], [21, T + 2], [24, Wy], [31, hipY + 30], [-31, hipY + 30], [-24, Wy], [-21, T + 2]], cw = [[-6, T - 2], [-18, T - 18], [-22, T + 6], [-10, T + 14]];
          return { svg: solid([poly(pts)], COAT) + dots(pts, 8, 0.25) + solid([poly(cw), poly(flipX(cw))], COAT, 2.6) + belt(Wy + 2, 25) + buttons([T + 16, T + 24, Wy + 12, Wy + 20]) + buttons([T + 16, T + 24, Wy + 12, Wy + 20], -9) +
            '<g transform="translate(16,' + (Wy + 16) + ') rotate(-14)">' + solid([poly([[-6, -9], [8, -9], [8, 2], [-6, 2]])], C.money, 1.6) + "</g>" + solid([poly([[8, Wy + 14], [22, Wy + 14], [22, Wy + 19], [8, Wy + 19]])], COAT, 2), sl: [13, 11, 11], pants: PANTS, light: [-12, T + 10] };
        },
        hourglass: function () {
          var pts = [[-15, T + 2], [-11, T - 2], [-5, T - 3], [5, T - 3], [11, T - 2], [15, T + 2], [8, Wy], [31, hipY + 30], [16, hipY + 34], [0, hipY + 31], [-16, hipY + 34], [-31, hipY + 30], [-8, Wy]];
          return { svg: solid([poly(pts)], cloth) + dots(pts, 6, 0.28) + V(8, skin) + line("M-8," + Wy + " H8", ink, 3.4) + buttons([T + 10, T + 16]) +
            [-8, -4, 0, 4, 8].map(function (x) { return '<circle cx="' + x + '" cy="' + (T + 7 - Math.abs(x) * 0.25) + '" r="1.9" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="0.8"/>'; }).join(""), sl: [8.5, 7, 6], bare: true, short: cloth, light: [8, T + 13] };
        },
        lab: function () {
          var panel = [[-24, T + 2], [-18, T - 2], [-6, T - 3], [-2, T + 26], [-2, hipY + 34], [-25, hipY + 34]];
          return { svg: solid([poly([[-20, T], [20, T], [16, hipY], [-16, hipY]])], woman ? cloth : WHITE) + V(8, skin) + (woman ? "" : tie(20)) +
            solid([poly(panel), poly(flipX(panel))], "#F7F4EC") + dots(flipX(panel), 8, 0.22) + line("M" + P(-6, T - 3) + " L" + P(-11, T + 4) + " L" + P(-7, T + 8) + " M" + P(6, T - 3) + " L" + P(11, T + 4) + " L" + P(7, T + 8), ink, 1.6) +
            '<path d="M7,' + (T + 15) + ' h9 v7 h-9 z" fill="none" stroke="' + ink + '" stroke-width="1.6"/>' + line("M9.5," + (T + 16) + " v-6", C.war, 2.2) + line("M13," + (T + 16) + " v-5", C.med, 2.2), sl: [11, 9, 8], sleeve: "#F7F4EC", pants: PANTS, light: [-10, T + 14] };
        },
        barrel: function () {
          var shirt = [[-30, T + 4], [-22, T - 3], [22, T - 3], [30, T + 4], [36, T + 26], [30, hipY - 2], [-30, hipY - 2], [-36, T + 26]].map(function (p) { return [p[0] * tw, p[1]]; }), denim = o.colorHex || cloth;
          return { svg: solid([poly(shirt)], WHITE) + dots(shirt, 12 * tw, 0.22) + collar + solid([poly([[-15, T + 16], [15, T + 16], [17, hipY + 2], [-17, hipY + 2]])], denim, 3.6) +
            line("M-13," + (T + 16) + " L" + -20 * tw + "," + (T - 1) + " M13," + (T + 16) + " L" + 20 * tw + "," + (T - 1), denim, 4.5) + '<rect x="-14" y="' + (T + 17) + '" width="4" height="4" fill="' + C.yellow + '"/><rect x="10" y="' + (T + 17) + '" width="4" height="4" fill="' + C.yellow + '"/>', sl: [9, 13, 16], bare: true, short: WHITE, pants: denim, light: [-14, T + 8] };
        },
        pear: function () {
          var pts = [[-13, T + 2], [-9, T - 2], [9, T - 2], [13, T + 2], [20, Wy + 6], [28, hipY + 22], [0, hipY + 25], [-28, hipY + 22], [-20, Wy + 6]], apron = [[-11, Wy + 2], [11, Wy + 2], [16, hipY + 20], [-16, hipY + 20]];
          return { svg: solid([poly(pts)], cloth) + solid([poly(apron)], C.cream, 2.4) + dots(apron, 4, 0.2) + V(7, skin) + '<circle cx="-6" cy="' + (T + 8) + '" r="2.6" fill="' + C.war + '" stroke="' + ink + '" stroke-width="1"/>', sl: [8, 7, 6], sleeve: cloth, light: [6, T + 12] };
        },
        twig: function () {
          var col = o.colorHex || SCRUBS, pts = [[-17, T + 2], [-13, T - 2], [13, T - 2], [17, T + 2], [16, hipY + 6], [-16, hipY + 6]];
          return { svg: solid([poly(pts)], col) + dots(pts, 6, 0.22) + '<path d="M-6,' + (T - 2) + " L0," + (T + 10) + " L6," + (T - 2) + ' Z" fill="' + skin + '" stroke="' + ink + '" stroke-width="1.8" stroke-linejoin="miter"/><path d="M5,' + (T + 18) + ' h8 v7 h-8 z" fill="none" stroke="' + ink + '" stroke-width="1.6"/>', sl: [8, 7, 6], bare: true, short: col, pants: col, light: [-8, T + 12] };
        },
        shirt: function () {
          var w = 24 * tw, pts = [[-w, T + 2], [-w + 5, T - 2], [-5, T - 3], [5, T - 3], [w - 5, T - 2], [w, T + 2], [13.5, Wy], [14.5, hipY + 1], [-14.5, hipY + 1], [-13.5, Wy]];
          return { svg: solid([poly(pts)], cloth) + dots(pts, 6, 0.26) + collar + belt(hipY - 5, 14.5), sl: [6.5, 5.5, 4.5], bare: true, short: cloth, pants: PANTS, light: [w * 0.45, T + 13] };
        },
      };
      var body = KINDS[kind](), len = g[2] * b.armL, k = b.arms, hk = b.hand;

      function leg(i, sx, cls) {
        var a = l.lp[i].map(function (v) { return v * (b.legPose ? f : 1); });
        var s = seg(sx * 7 * (0.7 + 0.3 * tw), hipY, a, l.L), gx = b.legPose ? f : dir || sx, ax = s.hx, ay = s.hy, fl = b.feet;
        var shoe = poly([[ax - gx * 5 * fl, ay - 3.5], [ax + gx * 3 * fl, ay - 4], [ax + gx * (woman ? 11 : 14) * fl, ay + 2.5], [ax + gx * (woman ? 10 : 13) * fl, ay + 4.5], [ax - gx * 5 * fl, ay + 4.5]]);
        var heel = woman ? poly([[ax - gx * 4.5, ay + 3], [ax - gx * 1.5, ay + 3], [ax - gx * 2.5, ay + 7], [ax - gx * 4.5, ay + 7]]) : null;
        var ankle = { x: s.x, y: s.y, ex: s.ex, ey: s.ey, hx: s.hx, hy: s.hy - 2 };
        var lg = body.pants ? solid([limb(ankle, 11, 8.5, 7)], body.pants) : solid([limb(ankle, 6.5, 5, 4)], skin, 3.6);
        return '<g class="' + cls + '">' + lg + solid(heel ? [shoe, heel] : [shoe], ink, 2.4) + "</g>";
      }
      function hand(s, side, hold) {
        var a = (Math.atan2(s.hx - s.ex, s.hy - s.ey) * 180) / Math.PI, glove = o.gloves ? NAVY : skin;
        return '<g transform="translate(' + P(s.hx, s.hy) + ") rotate(" + (-a).toFixed(1) + ") scale(" + (-side * hk).toFixed(2) + "," + hk.toFixed(2) + ')">' +
          solid([poly([[-2.6, -1], [2.6, -1], [4, 6], [2.2, 11.5], [-1.2, 12], [-3.6, 7.5]]), poly([[2.4, 1.5], [7, 5.5], [3.4, 7]])], glove, 3 / hk) + "</g>" +
          (hold && PROPS[hold] ? '<g transform="translate(' + P(s.hx + side * 2, s.hy + 6) + ')">' + PROPS[hold]() + "</g>" : "");
      }
      function arm(i, sx, cls) {
        var s = seg(sx * g[0], g[1], arms[i], len), sl = body.sl, out;
        if (body.bare) out = solid([limb(s, sl[0] * Math.sqrt(k), sl[1] * k, sl[2] * k)], skin, 3.6) + solid([upperQuad(s, (sl[0] + 4.5) * Math.sqrt(k), (sl[0] + 3) * Math.sqrt(k), 0.72)], body.short);
        else out = solid([limb(s, sl[0] * k, sl[1] * k, sl[2] * k)], body.sleeve || NAVY) + (body.sleeve ? "" : solid([upperQuad({ x: s.ex + (s.hx - s.ex) * 0.84, y: s.ey + (s.hy - s.ey) * 0.84, ex: s.hx, ey: s.hy }, sl[2] * k, sl[2] * k, 1)], WHITE, 2.6));
        return '<g class="' + cls + '">' + out + hand(s, sx, i ? o.holdR : o.holdL) + "</g>";
      }
      var hs = b.hs;
      var head = o.prop === "megaphone"
        ? '<g class="head"><g transform="translate(0,' + l.hy.toFixed(1) + ')"><path d="M-8,16 L-8,-4 L24,-22 L24,34 Z" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="3.4" stroke-linejoin="miter"/><path d="M24,-22 L30,6 L24,34 Z" fill="' + ink + '"/><!--face-end--></g><!--head-end--></g>'
        : '<g class="head"><g transform="translate(' + dir * 2 + "," + l.hy.toFixed(1) + ") scale(" + (f * hs).toFixed(3) + "," + hs.toFixed(3) + ')">' + face(o, R, mood, skin) +
          (R.hat === "fedoraUp" ? hatSvg("fedora", 1, -26) : hatSvg(R.hat, 1, -22)) + "<!--face-end--></g><!--head-end--></g>";
      var neck = solid([poly([[-4 * hs + dir * 2, l.hy + 14 * hs], [4.5 * hs + dir * 2, l.hy + 16 * hs], [5.5, T + 1], [-5.5, T + 1]])], skin, 3.6);
      var held = "";
      if (o.hold && PROPS[o.hold]) {
        var hl = seg(-g[0], g[1], arms[0], len), hr = seg(g[0], g[1], arms[1], len);
        held = '<g transform="translate(' + P((hl.hx + hr.hx) / 2, (hl.hy + hr.hy) / 2 + 2) + ')">' + PROPS[o.hold]() + "</g>";
      }
      var light = o.light === "red" ? C.war : o.light === "teal" ? C.med : "#E9E1CC";
      // The upper body leans or hunches from the hips (forward = the way the head faces).
      return '<g class="person">' + leg(0, -1, "leg-l") + leg(1, 1, "leg-r") +
        '<g transform="rotate(' + (b.hunch * f).toFixed(1) + " 0 " + hipY.toFixed(1) + ')">' + neck + body.svg +
        '<circle class="chest-light" cx="' + body.light[0].toFixed(1) + '" cy="' + body.light[1].toFixed(1) + '" r="4.5" fill="' + light + '" stroke="' + ink + '" stroke-width="2"/>' +
        head + arm(0, -1, "arm-l") + arm(1, 1, "arm-r") + held + "</g></g>";
    }

    // The skeleton gag (cartoon-style-bible.md, Comedy 6): the same height and lean, bones as thin as anyone's
    // (a fat cat's too), still grinning, still in its hat, monocle, cigar or mask.
    function skeleton(o) {
      var R = resolve(o), b = R.b, l = lay(b), g = armGeo(R.kind, b, l), arms = o.arms || CAST_ARMS(o), f = o.look === "left" ? -1 : 1;
      function bone(d, w) {
        return '<path d="' + d + '" fill="none" stroke="' + ink + '" stroke-width="' + (w + 3.4) + '" stroke-linecap="square" stroke-linejoin="miter"/><path d="' + d + '" fill="none" stroke="' + BONE + '" stroke-width="' + w + '" stroke-linecap="square" stroke-linejoin="miter"/>';
      }
      function bones(x0, y0, a, len, cls, foot) {
        var s = seg(x0, y0, a, len);
        var end = foot ? solid([poly([[s.hx - foot * 5, s.hy - 2], [s.hx + foot * 14, s.hy + 2], [s.hx - foot * 5, s.hy + 4]])], BONE, 3) : solid([poly([[s.hx - 3.5, s.hy - 1], [s.hx + 3.5, s.hy - 1], [s.hx, s.hy + 10]])], BONE, 3);
        return '<g class="' + cls + '">' + bone("M" + P(x0, y0) + " L" + P(s.ex, s.ey) + " L" + P(s.hx, s.hy), 4) + end + "</g>";
      }
      var ribs = "", hx = 7 * (0.7 + 0.3 * b.tw);
      for (var k = 0; k < Math.max(3, Math.round(4 * b.th)); k++) { var y = l.sY + 4 + k * 7.5, w = 16 - k * 2; ribs += bone("M" + -w + "," + (y + 5) + " L0," + (y - 1) + " L" + w + "," + (y + 5), 2.6); }
      var skull = '<g class="head"><g transform="translate(0,' + l.hy.toFixed(1) + ") scale(" + (f * b.hs).toFixed(3) + "," + b.hs.toFixed(3) + ')">' +
        solid([poly([[-16, -6], [-12, -19], [0, -23], [12, -19], [16, -6], [14, 6], [8, 11], [8, 20], [-8, 20], [-8, 11], [-14, 6]])], BONE, LW) +
        '<path d="M-12,-6 L-3,-7 L-4,2 L-10,1 Z M12,-6 L3,-7 L4,2 L10,1 Z" fill="' + ink + '"/><path d="M-2.5,9 L0,3 L2.5,9 Z" fill="' + ink + '"/>' +
        '<path class="mouth" d="M-9,13 L9,13 M-4.5,11 v7 M0,11 v7 M4.5,11 v7" fill="none" stroke="' + ink + '" stroke-width="1.8"/>' +
        (o.prop === "monocle" ? '<circle cx="7" cy="-3" r="6.4" fill="none" stroke="' + C.yellow + '" stroke-width="2.4"/>' : "") +
        (o.cigar ? '<g transform="translate(6,14) rotate(-12)">' + solid([poly([[0, -2.6], [22, -2.6], [22, 2.6], [0, 2.6]])], "#7A4A2A", 2) + '<rect x="19" y="-2.6" width="4" height="5.2" fill="#C9C2B5"/></g>' : "") +
        (o.mask ? '<path d="M-17,-11 L18,-12 L19,-1 L13,1 L9,-3 L4,1 L-4,-2 L-10,1 L-17,-1 Z" fill="' + ink + '" opacity="0.92"/>' : "") +
        hatSvg(R.hat === "fedoraUp" ? "fedora" : R.hat, 0, -22) + "<!--face-end--></g><!--head-end--></g>";
      return '<g class="person skeleton">' + bones(-hx, l.hipY, l.lp[0], l.L, "leg-l", -1) + bones(hx, l.hipY, l.lp[1], l.L, "leg-r", 1) +
        '<g transform="rotate(' + (b.hunch * f).toFixed(1) + " 0 " + l.hipY.toFixed(1) + ')">' + bone("M0," + (l.hy + 20 * b.hs).toFixed(1) + " V" + (l.hipY - 4), 4) + ribs +
        solid([poly([[-14, l.hipY - 7], [14, l.hipY - 7], [8, l.hipY + 5], [-8, l.hipY + 5]])], BONE, 3) + bone("M" + -g[0] + "," + g[1] + " L0," + (l.sY - 4) + " L" + g[0] + "," + g[1], 3.4) +
        '<circle class="chest-light" cx="0" cy="' + (l.sY + 10) + '" r="0" fill="none"/>' + bones(-g[0], g[1], arms[0], g[2] * b.armL, "arm-l") + bones(g[0], g[1], arms[1], g[2] * b.armL, "arm-r") + skull + "</g></g>";
    }
    // The charred gag: every color but the ink goes a dark brown of the same lightness; the hair blows straight
    // up, only the eyes stay white (.char-eyes, pupils r 1.8), and .smoke wisps rise (all in the face's units).
    function charify(markup, o) {
      var inkU = ink.toUpperCase();
      function dark(col) {
        var n = parseInt(col.slice(1), 16), lum = (0.3 * (n >> 16) + 0.59 * ((n >> 8) & 255) + 0.11 * (n & 255)) / 255, v = Math.round(28 + lum * 46);
        return "rgb(" + (v + 8) + "," + v + "," + Math.max(0, v - 6) + ")";
      }
      var out = markup.replace(/(fill|stroke)="(#[0-9A-Fa-f]{3,6})"/g, function (m, attr, col) {
        if (col.length === 4) col = "#" + col[1] + col[1] + col[2] + col[2] + col[3] + col[3];
        return col.toUpperCase() === inkU ? m : attr + '="' + dark(col) + '"';
      });
      var eye = function (x) { return '<circle cx="' + x + '" cy="-4" r="4.6" fill="#FFFFFF" stroke="' + ink + '" stroke-width="1.4"/><circle cx="' + x + '" cy="-4" r="1.8" fill="' + ink + '"/>'; };
      var hair = "<" + poly([[-15, -14], [-22, -34], [-10, -24], [-7, -46], [0, -27], [6, -48], [10, -26], [20, -40], [17, -20], [26, -26], [16, -12]]) + ' fill="#1B1714" stroke="' + ink + '" stroke-width="1.8"/>';
      var smoke = '<g class="smoke">' + [-12, 2, 15].map(function (dx, i) { return line("M" + dx + "," + (-48 - i * 4) + " l-6,-9 l6,-9 l-6,-9", "#8C8782", 3.6); }).join("") + "</g>";
      return out.replace(/<g class="eye">[\s\S]*?<\/g>/g, "").replace("<!--face-end-->", hair + '<g class="char-eyes">' + eye(EYES[0][0]) + eye(EYES[1][0]) + "</g>" + smoke);
    }
    // Flames all over a person, on this build's hips, shoulders and head (put it inside the person's group).
    function fireOn(o) {
      var r = rig(o || {}), R = resolve(o || {}), l = lay(R.b);
      return '<g class="on-fire">' + flames(-2, l.hipY + 8, 0.95) + flames(r.shoulder[0][0] - 6, r.shoulder[0][1] + 10, 0.5) + flames(r.shoulder[1][0] + 6, r.shoulder[1][1] + 10, 0.5) + flames(r.top[0], r.top[1] + 8, 0.62) + "</g>";
    }
    // A cast member's options (for KIT.rig too): the preset, then the scene's.
    function castOpts(name, extra) {
      var o = copy(CAST[name], extra);
      if (extra && extra.arms) {
        if (!("hold" in extra)) o.hold = null;
        if (!("holdL" in extra)) o.holdL = null;
        if (!("holdR" in extra)) o.holdR = null;
      }
      return o;
    }
    function cast(name, extra) { return person(castOpts(name, extra)); }
    return { person: person, cast: cast, castOpts: castOpts, CAST: CAST, rig: rig, fireOn: fireOn };
  })();

  // ── Gags (cartoon-style-bible.md, Comedy 6) ─────────────────────────
  // A flame of three tongues, its base at (x, y), about 100 * s tall. Each tongue is an untransformed
  // .flame group: make them dance with KIT.flicker.
  var FLAME_D = "M0,0 C-34,-10 -30,-60 -8,-96 C-6,-70 10,-62 14,-84 C34,-56 40,-14 0,0 Z";
  function flames(x, y, s) {
    var tongue = function (fill, k, dx) {
      return '<g transform="translate(' + dx + ',0) scale(' + k + ')"><g class="flame"><path d="' + FLAME_D + '" fill="' + fill + '" stroke="' + C.line + '" stroke-width="' + (4 / k).toFixed(1) + '" stroke-linejoin="round"/></g></g>';
    };
    return '<g transform="translate(' + x + "," + y + ") scale(" + (s || 1) + ')"><g class="flames">' + tongue(C.war, 1, 0) + tongue(C.orange, 0.68, 2) + tongue(C.yellow, 0.38, 3) + "</g></g>";
  }
  // Flicker every .flame under `root` (an element or a selector) from t0 to t1, with finite repeats.
  function flicker(tl, root, t0, t1) {
    var els = typeof root === "string" ? document.querySelectorAll(root + " .flame") : root.querySelectorAll(".flame");
    Array.prototype.forEach.call(els, function (el, i) {
      var d = [0.11, 0.14, 0.09, 0.13][i % 4];
      gsap.set(el, { svgOrigin: "0 0" });
      tl.fromTo(el, { scaleY: 0.86, scaleX: 1.05 }, { scaleY: 1.12, scaleX: 0.94, duration: d, repeat: Math.max(1, Math.floor((t1 - t0) / d)), yoyo: true, ease: "sine.inOut" }, t0);
    });
  }
  // A mushroom cloud standing on the ground at (0,0): about 560 tall and 520 wide. Its parts are
  // untransformed groups (.nuke-base, .nuke-stem, .nuke-ring, .nuke-cap); KIT.boom plays the blast.
  function nuke() {
    function cloud(cls, circles, fill, hi) {
      var outline = circles.map(function (c) { return '<circle cx="' + c[0] + '" cy="' + c[1] + '" r="' + c[2] + '" fill="' + C.line + '" stroke="' + C.line + '" stroke-width="12"/>'; }).join("");
      var body = circles.map(function (c) { return '<circle cx="' + c[0] + '" cy="' + c[1] + '" r="' + c[2] + '" fill="' + fill + '"/>'; }).join("");
      var light = circles.filter(function (c, i) { return i % 2 === 0; }).map(function (c) {
        return '<circle cx="' + (c[0] - c[2] * 0.25) + '" cy="' + (c[1] - c[2] * 0.3) + '" r="' + c[2] * 0.45 + '" fill="' + hi + '" opacity="0.8"/>';
      }).join("");
      return '<g class="' + cls + '">' + outline + body + light + "</g>";
    }
    var base = cloud("nuke-base", [[-200, -30, 52], [-120, -44, 66], [-40, -50, 72], [40, -50, 72], [120, -44, 66], [200, -30, 52]], C.tan, C.cream);
    var stem = '<g class="nuke-stem"><path d="M-42,-60 C-30,-160 -40,-280 -52,-380 H52 C40,-280 30,-160 42,-60 Z" fill="' + C.orange + '" stroke="' + C.line + '" stroke-width="6" stroke-linejoin="round"/>' +
      '<path d="M-12,-70 C-6,-160 -12,-280 -18,-370" fill="none" stroke="' + C.yellow + '" stroke-width="14" stroke-linecap="round"/></g>';
    var ring = cloud("nuke-ring", [[-120, -250, 34], [-70, -262, 38], [0, -266, 40], [70, -262, 38], [120, -250, 34]], C.cream, "#FFFFFF");
    var cap = cloud("nuke-cap", [[-170, -390, 62], [170, -390, 62], [-110, -430, 88], [110, -430, 88], [-60, -500, 82], [60, -500, 82], [0, -460, 112], [0, -540, 70]], C.yellow, C.cream);
    return '<g class="nuke">' + base + stem + ring + cap + "</g>";
  }
  // The blast at time t: the cloud grows out of the ground and keeps billowing. root: the element that
  // holds a KIT.nuke(). opts.flash: a full-frame element (white) that flashes; opts.shake: an element to shake.
  function boom(tl, root, t, opts) {
    opts = opts || {};
    var part = function (c) { return (typeof root === "string" ? document.querySelector(root) : root).querySelector("." + c); };
    var base = part("nuke-base"), stem = part("nuke-stem"), ring = part("nuke-ring"), cap = part("nuke-cap");
    gsap.set(base, { svgOrigin: "0 0" }); gsap.set(stem, { svgOrigin: "0 -60" }); gsap.set(ring, { svgOrigin: "0 -258" }); gsap.set(cap, { svgOrigin: "0 -450" });
    tl.fromTo(base, { scaleX: 0.15, scaleY: 0.2, opacity: 0 }, { scaleX: 1, scaleY: 1, opacity: 1, duration: 0.45, ease: "power3.out" }, t);
    tl.fromTo(stem, { scaleY: 0, opacity: 0 }, { scaleY: 1, opacity: 1, duration: 0.7, ease: "power2.out" }, t + 0.05);
    tl.fromTo(cap, { scale: 0.15, y: 330, opacity: 0 }, { scale: 1, y: 0, opacity: 1, duration: 0.8, ease: "power2.out" }, t + 0.05);
    tl.fromTo(ring, { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.6)" }, t + 0.4);
    tl.to(cap, { y: -26, scale: 1.05, duration: 2.4, ease: "sine.out" }, t + 0.85);
    if (opts.flash) tl.fromTo(opts.flash, { opacity: 0 }, { opacity: 1, duration: 0.04 }, t).to(opts.flash, { opacity: 0, duration: 0.7, ease: "power2.in" }, t + 0.12);
    if (opts.shake) tl.fromTo(opts.shake, { x: 0 }, { x: 14, duration: 0.04, repeat: 9, yoyo: true, ease: "none", immediateRender: false }, t);
  }
  // Turn a person into a skeleton the old cartoon way: the picture flickers between the two drawings
  // (an x-ray), then stays on the bones. alive and bones are stacked groups; bones start hidden.
  function xray(tl, alive, bones, t) {
    tl.set(bones, { opacity: 0 }, 0);
    for (var i = 0; i < 7; i++) {
      tl.set(alive, { opacity: i % 2 ? 1 : 0 }, t + i * 0.06);
      tl.set(bones, { opacity: i % 2 ? 0 : 1 }, t + i * 0.06);
    }
  }
  // The Grim Reaper from the theme song: a hooded black robe, a grinning skull and a scythe. Drawn
  // around (0,0) with its feet at y 100, a head taller than a person. Parts: .reaper-scythe, .head.
  function reaper() {
    var ink = C.line, robe = "#141B2B";
    return '<g class="reaper">' +
      '<g class="reaper-scythe"><path d="M46,98 L64,-196" stroke="' + ink + '" stroke-width="13" stroke-linecap="round"/><path d="M46,98 L64,-196" stroke="' + C.tan + '" stroke-width="7" stroke-linecap="round"/>' +
      '<path d="M64,-196 C20,-236 -60,-236 -104,-196 C-60,-214 10,-210 60,-170 Z" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="5" stroke-linejoin="round"/></g>' +
      '<path d="M-46,100 C-52,20 -44,-60 -34,-110 C-30,-150 -16,-176 0,-178 C16,-176 30,-150 34,-110 C44,-60 52,20 46,100 Z" fill="' + robe + '" stroke="' + ink + '" stroke-width="5" stroke-linejoin="round"/>' +
      '<path d="M-26,-112 C-26,-146 -14,-160 0,-160 C14,-160 26,-146 26,-112 C14,-104 -14,-104 -26,-112 Z" fill="#000"/>' +
      '<g class="head"><circle cx="0" cy="-130" r="17" fill="' + BONE + '" stroke="' + ink + '" stroke-width="3"/><ellipse cx="-6" cy="-133" rx="4.5" ry="5.5" fill="' + ink + '"/><ellipse cx="6" cy="-133" rx="4.5" ry="5.5" fill="' + ink + '"/>' +
      '<path d="M-8,-120 Q0,-115 8,-120 M-4,-121 v4 M0,-120 v4 M4,-121 v4" fill="none" stroke="' + ink + '" stroke-width="1.8" stroke-linecap="round"/></g>' +
      '<circle cx="46" cy="-40" r="9" fill="' + BONE + '" stroke="' + ink + '" stroke-width="2.5"/>' +
      '<path d="M-40,40 C-30,10 -10,0 0,0 C10,0 30,10 40,40" fill="none" stroke="' + ink + '" stroke-width="3" opacity="0.5"/></g>';
  }

  // A walking paper bill around (0,0), 96 x 50, legs to y=48, always money green. kind: "war" (a red
  // missile seal), "med" (a teal cross seal) or "plain" (no seal).
  function moneySeal(kind, x, y, r) {
    if (kind !== "war" && kind !== "med") return "";
    var mark = kind === "war"
      ? '<path d="M' + (x - r * 0.55) + "," + (y + r * 0.35) + " L" + (x + r * 0.35) + "," + (y - r * 0.55) + " l" + r * 0.2 + "," + r * 0.2 + " Z" + '" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="' + (r * 0.28).toFixed(1) + '" stroke-linejoin="round"/>'
      : '<path d="M' + x + "," + (y - r * 0.55) + " V" + (y + r * 0.55) + " M" + (x - r * 0.55) + "," + y + " H" + (x + r * 0.55) + '" stroke="#FFFFFF" stroke-width="' + (r * 0.34).toFixed(1) + '" stroke-linecap="round"/>';
    return '<circle cx="' + x + '" cy="' + y + '" r="' + r + '" fill="' + (kind === "war" ? C.war : C.med) + '" stroke="' + C.line + '" stroke-width="2"/>' + mark;
  }
  function money(kind, legs) {
    var fill = C.money, dark = C.moneyDark;
    var l = legs === undefined ? 0 : legs;
    return '<g class="money">' +
      '<path class="legs" d="M-16,24 l' + (-6 + l * 10) + ',22 h-8 M16,24 l' + (6 - l * 10) + ',22 h8" fill="none" stroke="' + C.line + '" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>' +
      '<rect x="-48" y="-25" width="96" height="50" rx="4" fill="' + fill + '" stroke="' + C.line + '" stroke-width="4"/>' +
      '<rect x="-41" y="-18" width="82" height="36" rx="2" fill="none" stroke="' + dark + '" stroke-width="2"/>' +
      '<ellipse cx="0" cy="0" rx="13" ry="15" fill="' + C.paper + '" stroke="' + dark + '" stroke-width="2"/>' +
      '<circle cx="0" cy="-2" r="5" fill="none" stroke="' + dark + '" stroke-width="1.8"/>' +
      '<path d="M-7,-4 q-3,6 0,10 M7,-4 q3,6 0,10 M-6,10 q6,-5 12,0" fill="none" stroke="' + dark + '" stroke-width="1.6"/>' +
      '<circle cx="-31" cy="0" r="5" fill="none" stroke="' + dark + '" stroke-width="2"/>' +
      (kind === "war" || kind === "med" ? moneySeal(kind, 31, 0, 10) : '<circle cx="31" cy="0" r="5" fill="none" stroke="' + dark + '" stroke-width="2"/>') +
      "</g>";
  }
  function tophat(fill) {
    return '<g class="tophat"><rect x="-18" y="-40" width="36" height="38" rx="3" fill="' + (fill || C.line) + '" stroke="' + C.line + '" stroke-width="3"/>' +
      '<rect x="-18" y="-14" width="36" height="7" fill="' + C.war + '"/>' +
      '<rect x="-30" y="-6" width="60" height="9" rx="4" fill="' + (fill || C.line) + '" stroke="' + C.line + '" stroke-width="3"/></g>';
  }
  function checkbox(x, y, s) {
    return '<rect x="' + x + '" y="' + y + '" width="' + s + '" height="' + s + '" rx="3" fill="' + C.paper + '" stroke="' + C.line + '" stroke-width="4"/>';
  }
  function tick(x, y, s, color) {
    return '<path class="tick" d="M' + (x + s * 0.18) + "," + (y + s * 0.52) + " L" + (x + s * 0.42) + "," + (y + s * 0.8) + " L" + (x + s * 0.95) + "," + (y + s * 0.05) +
      '" fill="none" stroke="' + (color || C.med) + '" stroke-width="' + s * 0.16 + '" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>';
  }
  // Inline check mark for HTML text (fonts may lack the glyph).
  function checkSvg(size, color) {
    return '<svg width="' + size + '" height="' + size + '" viewBox="0 0 34 34" style="vertical-align:-0.08em"><path d="M4,18 L13,27 L30,5" fill="none" stroke="' + (color || C.med) + '" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  }
  function pencil() {
    return '<g class="pencil"><path d="M0,0 l18,-10 l120,-70 l12,20 l-120,70 Z" fill="' + C.yellow + '" stroke="' + C.line + '" stroke-width="4" stroke-linejoin="round"/>' +
      '<path d="M0,0 l18,-10 l2,14 Z" fill="' + C.line + '"/><path d="M138,-80 l12,20 l14,-8 l-12,-20 Z" fill="' + C.war + '" stroke="' + C.line + '" stroke-width="4"/></g>';
  }

  // Shared CSS (fonts are declared in each composition file).
  var css =
    ".kit-big{font-family:Fraunces;font-weight:900;color:#1A1426;line-height:0.95;text-shadow:3px 3px 0 #F6EBD2,-3px 3px 0 #F6EBD2,3px -3px 0 #F6EBD2,-3px -3px 0 #F6EBD2,0 4px 0 #F6EBD2,0 -4px 0 #F6EBD2,4px 0 0 #F6EBD2,-4px 0 0 #F6EBD2,6px 8px 0 #1A1426;}" +
    ".kit-label{font-family:Oswald;font-weight:600;text-transform:uppercase;letter-spacing:0.04em;color:#1B1B1B;}";
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  window.KIT = {
    P: P, C: C, V: V, W: W, H: H, OFFICE: OFFICE, form: form, FORM_Q: FORM_Q, FORM_AT: FORM_AT, cornerOpts: cornerOpts, zoomView: zoomView, enter: enter, drawTick: drawTick,
    scene: scene, cue: cue, cueEnd: cueEnd, after: after, before: before, rng: rng, onTime: onTime,
    mountWishonia: mountWishonia, wishoniaAt: wishoniaAt,
    svg: svg, el: el, office: office, desk: desk, mug: mug, cabinet: cabinet, wallScreen: wallScreen,
    // bean is the old name: every human is now person() (the bean drawing stays as beanClassic).
    paper: paper, paperDefs: paperDefs, grain: grain, star: star, boomerang: boomerang, sun: sun, horizon: V ? 1180 : 610, person: HUMANS.person, cast: HUMANS.cast, CAST: HUMANS.CAST, castOpts: HUMANS.castOpts, rig: HUMANS.rig, bean: HUMANS.person, beanClassic: bean, money: money, moneySeal: moneySeal, tophat: tophat,
    flames: flames, fireOn: HUMANS.fireOn, flicker: flicker, nuke: nuke, boom: boom, xray: xray, reaper: reaper,
    checkbox: checkbox, tick: tick, checkSvg: checkSvg, pencil: pencil,
  };
})();
