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

  // Build a Wishonia rig in `parent`. opts: { scene, x, y, w, pip: {cx, cy, r} }.
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
    if (opts.pip) {
      var r = opts.pip.r;
      frame.style.cssText = "position:absolute;left:" + (opts.pip.cx - r) + "px;top:" + (opts.pip.cy - r) + "px;width:" + 2 * r + "px;height:" + 2 * r + "px;border-radius:50%;overflow:hidden;" +
        "background:radial-gradient(circle at 50% 70%, #E8B04A 0, #E5903B 40%, #904B2E 68%, #112845 92%);" +
        "box-shadow:0 0 0 7px " + C.cream + ", 0 0 0 13px " + C.line + ";";
      rig.style.left = opts.x - (opts.pip.cx - r) + "px";
      rig.style.top = opts.y - (opts.pip.cy - r) + "px";
    } else {
      frame.style.cssText = "position:absolute;inset:0;";
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
    frame.appendChild(rig);
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
    });
    return { frame: frame, rig: rig };
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

  // Wishonia's round corner frame (Layer B): bottom right in 16:9, top right in 9:16.
  function pipOpts(scene) {
    var r = V ? 122 : 128, cx = V ? 902 : 1760, cy = V ? 300 : 740, w = V ? 266 : 280;
    return { scene: scene, x: cx - Math.round(w / 2), y: cy - Math.round(w * 0.54), w: w, pip: { cx: cx, cy: cy, r: r } };
  }
  // The countdown board, in the top-left corner from loved-ones on.
  function placeBoard(wrap, inner) {
    wrap.style.cssText = "position:absolute;left:" + (V ? 40 : 56) + "px;top:" + (V ? 70 : 52) + "px;";
    inner.style.cssText = "position:relative;transform-origin:0 0;transform:scale(" + (V ? 0.62 : 0.68) + ");";
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

  // The humans (cartoon-style-bible.md section 3): stick figures in simple clothes, drawn around
  // (0,0) with the head near y -78 and the feet at y 100, the same footprint as the old bean.
  // o: { tone 0..3 (skin), outfit "shirt"|"dress"|"suit"|"labcoat"|"scrubs"|"overalls", color 0..3,
  //      hair 0 short | 1 long | 2 bald, hat "top"|"bowler"|"hard"|"curlers", tie "wide", stache,
  //      prop "monocle"|"briefcase"|"megaphone"|"poster"|"clipboard", tall, light "red"|"teal",
  //      mood "smile"|"eager"|"sad"|"flat" (or the old mouth "smile"|"o"|"frown"|"flat"),
  //      look "right"|"left", arms [[a1, a2], [b1, b2]] (deg, 0 = down), brows }
  // No joint dots: the limbs bend without them. Parts animators reach with querySelector: .arm-l, .arm-r, .leg-l, .leg-r, .head, .brows, .mouth, .chest-light.
  var CLOTHES = ["#E5903B", "#5C6F8E", "#B47E52", "#E8B04A"];
  var PANTS = "#273049";
  function hatSvg(kind, cx, hatTop) {
    var ink = C.line;
    return {
      top: '<rect x="' + (cx - 16) + '" y="' + (hatTop - 30) + '" width="32" height="30" rx="2" fill="' + ink + '"/><rect x="' + (cx - 16) + '" y="' + (hatTop - 9) + '" width="32" height="5" fill="' + C.war + '"/><rect x="' + (cx - 27) + '" y="' + (hatTop - 3) + '" width="54" height="6" rx="3" fill="' + ink + '"/>',
      bowler: '<path d="M' + (cx - 18) + "," + (hatTop + 2) + " Q" + cx + "," + (hatTop - 22) + " " + (cx + 18) + "," + (hatTop + 2) + ' Z" fill="' + ink + '"/><rect x="' + (cx - 27) + '" y="' + hatTop + '" width="54" height="5" rx="2.5" fill="' + ink + '"/>',
      hard: '<path d="M' + (cx - 24) + "," + (hatTop + 6) + " Q" + cx + "," + (hatTop - 24) + " " + (cx + 24) + "," + (hatTop + 6) + ' Z" fill="' + C.yellow + '" stroke="' + ink + '" stroke-width="3"/><rect x="' + (cx - 29) + '" y="' + (hatTop + 3) + '" width="58" height="6" rx="3" fill="' + C.yellow + '" stroke="' + ink + '" stroke-width="2.4"/>',
      curlers: [-14, 0, 14].map(function (dx) { return '<circle cx="' + (cx + dx) + '" cy="' + (hatTop + 4) + '" r="6.5" fill="#E9B4C1" stroke="' + ink + '" stroke-width="2.2"/>'; }).join(""),
    }[kind] || "";
  }

  // The gag versions of a person (cartoon-style-bible.md, Comedy 6): o.skeleton draws the same pose as
  // bones, still smiling, still in its hat; o.charred draws it burnt black and smoking, hair blown
  // straight up, only the eyes white (its .smoke wisps can drift up). Same footprint and part classes.
  var BONE = "#F1EAD6";
  function skeleton(o) {
    var ink = C.line;
    var dir = o.look === "right" ? 1 : o.look === "left" ? -1 : 0, cx = dir * 2;
    var arms = o.arms || [[20, 10], [-20, -10]];
    var stretch = o.tall ? 1.35 : 1, hy = -56 - (stretch - 1) * 60, R = 22, neckY = hy + R, hipY = 30, sy = -26 - (stretch - 1) * 30;
    function bonePath(d, w) {
      return '<path d="' + d + '" fill="none" stroke="' + ink + '" stroke-width="' + (w + 4) + '" stroke-linecap="round" stroke-linejoin="round"/>' +
        '<path d="' + d + '" fill="none" stroke="' + BONE + '" stroke-width="' + w + '" stroke-linecap="round" stroke-linejoin="round"/>';
    }
    function knob(x, y, r) { return '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="' + r + '" fill="' + BONE + '" stroke="' + ink + '" stroke-width="2.2"/>'; }
    function limb(x0, y0, a, len, cls, foot) {
      var r1 = (a[0] * Math.PI) / 180, r2 = (a[1] * Math.PI) / 180;
      var ex = x0 + len * Math.sin(r1), ey = y0 + len * Math.cos(r1), hx = ex + len * Math.sin(r2), hy2 = ey + len * Math.cos(r2);
      return '<g class="' + cls + '">' + bonePath("M" + x0 + "," + y0 + " L" + ex.toFixed(1) + "," + ey.toFixed(1) + " L" + hx.toFixed(1) + "," + hy2.toFixed(1), 5) +
        (foot ? '<ellipse cx="' + (hx + foot * 5).toFixed(1) + '" cy="' + (hy2 + 2).toFixed(1) + '" rx="9" ry="4.5" fill="' + BONE + '" stroke="' + ink + '" stroke-width="2.2"/>' : knob(hx, hy2, 5)) + "</g>";
    }
    var ribs = "";
    for (var k = 0; k < 4; k++) {
      var y = neckY + 9 + k * 8, w = 15 - k * 1.8;
      ribs += bonePath("M" + -w + "," + (y + 5) + " Q0," + (y - 4) + " " + w + "," + (y + 5), 3);
    }
    var ex = function (s) { return cx + s * 8 + dir * 4; };
    var skull = '<g class="head"><circle cx="' + cx + '" cy="' + hy + '" r="' + R + '" fill="' + BONE + '" stroke="' + ink + '" stroke-width="4.5"/>' +
      '<ellipse cx="' + ex(-1) + '" cy="' + (hy - 3) + '" rx="5.5" ry="6.5" fill="' + ink + '"/><ellipse cx="' + ex(1) + '" cy="' + (hy - 3) + '" rx="5.5" ry="6.5" fill="' + ink + '"/>' +
      '<path d="M' + (cx + dir * 3 - 3) + "," + (hy + 6) + ' l3,-6 l3,6 Z" fill="' + ink + '"/>' +
      '<path class="mouth" d="M' + (cx - 10) + "," + (hy + 12) + " Q" + cx + "," + (hy + 17) + " " + (cx + 10) + "," + (hy + 12) + " M" + (cx - 5) + "," + (hy + 11) + " v5 M" + cx + "," + (hy + 12) + " v5 M" + (cx + 5) + "," + (hy + 11) + ' v5" fill="none" stroke="' + ink + '" stroke-width="2" stroke-linecap="round"/>' +
      hatSvg(o.hat, cx, hy - R) + "</g>";
    return '<g class="person skeleton">' + limb(-8, hipY, [-10, -4], 34, "leg-l", -1) + limb(8, hipY, [10, 4], 34, "leg-r", 1) +
      bonePath("M0," + neckY + " V" + (hipY - 4), 5) + ribs +
      '<path d="M-13,' + (hipY - 7) + " Q0," + (hipY + 9) + " 13," + (hipY - 7) + " Q0," + (hipY - 1) + " -13," + (hipY - 7) + ' Z" fill="' + BONE + '" stroke="' + ink + '" stroke-width="2.5"/>' +
      bonePath("M-17," + sy + " Q0," + (sy - 5) + " 17," + sy, 4) +
      '<circle class="chest-light" cx="0" cy="' + (neckY + 14) + '" r="0" fill="none"/>' +
      limb(-17, sy, arms[0], 26, "arm-l") + limb(17, sy, arms[1], 26, "arm-r") + skull + "</g>";
  }
  // Burn a person's markup: every fill and stroke but the ink turns a dark brown of the same lightness.
  function charify(markup, o) {
    var ink = C.line.toUpperCase();
    function dark(col) {
      var n = parseInt(col.slice(1), 16), l = (0.3 * (n >> 16) + 0.59 * ((n >> 8) & 255) + 0.11 * (n & 255)) / 255;
      var v = Math.round(28 + l * 46);
      return "rgb(" + (v + 8) + "," + v + "," + Math.max(0, v - 6) + ")";
    }
    var out = markup.replace(/(fill|stroke)="(#[0-9A-Fa-f]{6})"/g, function (m, attr, col) {
      return col.toUpperCase() === ink ? m : attr + '="' + dark(col) + '"';
    });
    var dir = o.look === "right" ? 1 : o.look === "left" ? -1 : 0, cx = dir * 2, hy = -56 - ((o.tall ? 1.35 : 1) - 1) * 60;
    var eye = function (s) {
      var x = cx + s * 8 + dir * 5;
      return '<circle cx="' + x + '" cy="' + (hy - 2) + '" r="5" fill="#FFFFFF" stroke="' + C.line + '" stroke-width="1.5"/><circle cx="' + x + '" cy="' + (hy - 2) + '" r="1.8" fill="' + C.line + '"/>';
    };
    var hair = '<path d="M' + (cx - 17) + "," + (hy - 14) + " l-8,-22 l12,10 l1,-24 l9,19 l6,-23 l5,22 l11,-16 l-3,23 l12,-6 l-9,15 Z" + '" fill="#1B1714" stroke="' + C.line + '" stroke-width="2"/>';
    var smoke = '<g class="smoke">' + [-12, 2, 15].map(function (dx, i) {
      var x = cx + dx, y = hy - 42 - i * 4;
      return '<path d="M' + x + "," + y + " q-7,-9 0,-18 q7,-9 0,-18" + '" fill="none" stroke="#8C8782" stroke-width="4" stroke-linecap="round" opacity="0.85"/>';
    }).join("") + "</g>";
    return out.replace("<!--head-end-->", hair + '<g class="char-eyes">' + eye(-1) + eye(1) + "</g>" + smoke);
  }
  function person(o) {
    o = o || {};
    if (o.skeleton) return skeleton(o);
    if (o.charred) {
      var plain = {}, k;
      for (k in o) plain[k] = o[k];
      plain.charred = false; plain.hair = 2; plain.mood = "flat"; plain.prop = null; plain.stache = false;
      if (!o.keepHat) plain.hat = null;
      return charify(person(plain), o);
    }
    var ink = C.line;
    var skin = TONES[(o.tone || 0) % TONES.length];
    var cloth = o.colorHex || CLOTHES[(o.color === undefined ? o.tone || 0 : o.color) % CLOTHES.length];
    var outfit = o.outfit || (o.hair === 1 ? "dress" : ["shirt", "suit", "shirt", "overalls"][(o.tone || 0) % 4]);
    var mood = o.mood || (o.mouth === "smile" ? "smile" : o.mouth === "o" ? "eager" : o.mouth === "frown" ? "sad" : "flat");
    if (o.brows && mood === "flat") mood = "cross";
    var dir = o.look === "right" ? 1 : o.look === "left" ? -1 : 0;
    var arms = o.arms || [[20, 10], [-20, -10]];
    var stretch = o.tall ? 1.35 : 1;
    var hy = -56 - (stretch - 1) * 60, R = 22;
    var neckY = hy + R, hipY = 30;
    var longCoat = outfit === "labcoat" || outfit === "scrubs";
    function seg(x, y, a1, a2, len) {
      var r1 = (a1 * Math.PI) / 180, r2 = (a2 * Math.PI) / 180;
      var ex = x + len * Math.sin(r1), ey = y + len * Math.cos(r1);
      return { ex: ex, ey: ey, hx: ex + len * Math.sin(r2), hy: ey + len * Math.cos(r2) };
    }
    var sleeve = outfit === "dress" || outfit === "overalls" ? null : outfit === "labcoat" ? "#F7F4EC" : outfit === "scrubs" ? "#DDE9E6" : outfit === "suit" ? "#2E3440" : cloth;
    function arm(x, a, cls) {
      var s = seg(x, -26 - (stretch - 1) * 30, a[0], a[1], 26);
      var x0 = x, y0 = -26 - (stretch - 1) * 30;
      return '<g class="' + cls + '">' +
        (sleeve ? '<path d="M' + x0 + "," + y0 + " L" + s.ex.toFixed(1) + "," + s.ey.toFixed(1) + '" stroke="' + ink + '" stroke-width="12" stroke-linecap="round"/><path d="M' + x0 + "," + y0 + " L" + s.ex.toFixed(1) + "," + s.ey.toFixed(1) + '" stroke="' + sleeve + '" stroke-width="8" stroke-linecap="round"/>' : "") +
        '<path d="M' + (sleeve ? s.ex.toFixed(1) + "," + s.ey.toFixed(1) : x0 + "," + y0 + " L" + s.ex.toFixed(1) + "," + s.ey.toFixed(1)) + " L" + s.hx.toFixed(1) + "," + s.hy.toFixed(1) + '" fill="none" stroke="' + ink + '" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>' +
        '<circle cx="' + s.hx.toFixed(1) + '" cy="' + s.hy.toFixed(1) + '" r="5.5" fill="' + skin + '" stroke="' + ink + '" stroke-width="2.4"/></g>';
    }
    function leg(sx, cls) {
      var s = seg(sx * 8, hipY, sx * 10, sx * 4, 34);
      var pants = outfit === "suit" || outfit === "overalls" || outfit === "scrubs";
      var col = outfit === "scrubs" ? "#DDE9E6" : PANTS;
      var d = "M" + sx * 8 + "," + hipY + " L" + s.ex.toFixed(1) + "," + s.ey.toFixed(1) + " L" + s.hx.toFixed(1) + "," + s.hy.toFixed(1);
      return '<g class="' + cls + '">' +
        (pants ? '<path d="' + d + '" fill="none" stroke="' + ink + '" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/><path d="' + d + '" fill="none" stroke="' + col + '" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
          : '<path d="' + d + '" fill="none" stroke="' + ink + '" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>') +
        '<ellipse cx="' + (s.hx + sx * 5).toFixed(1) + '" cy="' + (s.hy + 2).toFixed(1) + '" rx="10" ry="5" fill="' + ink + '"/></g>';
    }
    var top = neckY + 4, sh = 17;
    var body = {
      shirt: '<path d="M' + -sh + "," + top + " Q0," + (top - 4) + " " + sh + "," + top + " L14," + (hipY + 2) + " L-14," + (hipY + 2) + ' Z" fill="' + cloth + '" stroke="' + ink + '" stroke-width="3.5" stroke-linejoin="round"/>',
      dress: '<path d="M-12,' + top + " Q0," + (top - 4) + " 12," + top + " L32,52 Q0,58 -32,52 Z" + '" fill="' + cloth + '" stroke="' + ink + '" stroke-width="3.5" stroke-linejoin="round"/><path d="M-10,' + (top + 14) + ' H10" stroke="' + ink + '" stroke-width="2" opacity="0.5"/>',
      suit: '<path d="M' + -sh + "," + top + " Q0," + (top - 4) + " " + sh + "," + top + " L15," + (hipY + 4) + " L-15," + (hipY + 4) + ' Z" fill="#2E3440" stroke="' + ink + '" stroke-width="3.5" stroke-linejoin="round"/><path d="M-7,' + top + " L0," + (top + 16) + " L7," + top + ' Z" fill="#FFF" stroke="' + ink + '" stroke-width="2"/>' +
        (o.tie === "wide" ? '<path d="M-3,' + (top + 2) + " L-14," + (hipY - 2) + " L0," + (hipY + 6) + " L14," + (hipY - 2) + " L3," + (top + 2) + ' Z" fill="' + (o.tieColor || C.war) + '" stroke="' + ink + '" stroke-width="2"/>' : '<path d="M0,' + (top + 3) + " l-3,5 l3,14 l3,-14 z" + '" fill="' + (o.tieColor || ink) + '"/>'),
      labcoat: '<path d="M' + -sh + "," + top + " Q0," + (top - 4) + " " + sh + "," + top + " L18,58 L-18,58 Z" + '" fill="#F7F4EC" stroke="' + ink + '" stroke-width="3.5" stroke-linejoin="round"/><path d="M0,' + (top + 2) + ' V58 M-6,' + top + " L0," + (top + 14) + " L6," + top + '" fill="none" stroke="' + ink + '" stroke-width="2"/><rect x="5" y="' + (top + 20) + '" width="8" height="6" fill="none" stroke="' + ink + '" stroke-width="1.6"/>',
      scrubs: '<path d="M' + -sh + "," + top + " Q0," + (top - 4) + " " + sh + "," + top + " L15," + (hipY + 6) + " L-15," + (hipY + 6) + ' Z" fill="#DDE9E6" stroke="' + ink + '" stroke-width="3.5" stroke-linejoin="round"/><path d="M-6,' + top + " L0," + (top + 10) + " L6," + top + '" fill="none" stroke="' + ink + '" stroke-width="2"/>',
      overalls: '<path d="M-13,' + (top + 12) + " H13 L14," + (hipY + 4) + " L-14," + (hipY + 4) + ' Z" fill="' + cloth + '" stroke="' + ink + '" stroke-width="3.5" stroke-linejoin="round"/><path d="M-10,' + (top + 12) + " L-12," + top + " M10," + (top + 12) + " L12," + top + '" stroke="' + cloth + '" stroke-width="5"/><path d="M0,' + top + " V" + (top + 12) + '" stroke="' + ink + '" stroke-width="5" stroke-linecap="round"/>',
    }[outfit];
    var spine = outfit === "overalls" ? '<path d="M0,' + neckY + " V" + hipY + '" stroke="' + ink + '" stroke-width="6" stroke-linecap="round"/>' : "";
    var cx = dir * 2;
    var ex = function (k) { return cx + k * 8 + dir * 5; };
    var eyes = '<circle cx="' + ex(-1) + '" cy="' + (hy - 2) + '" r="' + (mood === "eager" ? 4.4 : 3.2) + '" fill="' + ink + '"/><circle cx="' + ex(1) + '" cy="' + (hy - 2) + '" r="' + (mood === "eager" ? 4.4 : 3.2) + '" fill="' + ink + '"/>';
    var brows = {
      eager: "M" + (ex(-1) - 5) + "," + (hy - 12) + " q5,-5 10,0 M" + (ex(1) - 5) + "," + (hy - 12) + " q5,-5 10,0",
      smile: "",
      sad: "M" + (ex(-1) - 5) + "," + (hy - 8) + " L" + (ex(-1) + 4) + "," + (hy - 12) + " M" + (ex(1) + 5) + "," + (hy - 8) + " L" + (ex(1) - 4) + "," + (hy - 12),
      cross: "M" + (ex(-1) - 5) + "," + (hy - 13) + " L" + (ex(-1) + 4) + "," + (hy - 9) + " M" + (ex(1) + 5) + "," + (hy - 13) + " L" + (ex(1) - 4) + "," + (hy - 9),
      flat: "M" + (ex(-1) - 5) + "," + (hy - 9) + " h10 M" + (ex(1) - 5) + "," + (hy - 9) + " h10",
    }[mood];
    var mx = cx + dir * 5, my = hy + 9;
    var mouth = {
      eager: "M" + (mx - 4) + "," + my + " a4.5,6 0 1 0 9,0 a4.5,6 0 1 0 -9,0",
      smile: "M" + (mx - 9) + "," + (my - 2) + " q9,9 18,0",
      sad: "M" + (mx - 8) + "," + (my + 3) + " q8,-6 16,0",
      cross: "M" + (mx - 7) + "," + (my + 1) + " h14",
      flat: "M" + (mx - 7) + "," + my + " h14",
    }[mood];
    var hair = o.hair === 1
      ? '<path d="M' + (cx - 25) + "," + (hy + 12) + " Q" + (cx - 28) + "," + (hy - 30) + " " + cx + "," + (hy - 28) + " Q" + (cx + 28) + "," + (hy - 30) + " " + (cx + 25) + "," + (hy + 12) + " Q" + (cx + 19) + "," + (hy - 12) + " " + cx + "," + (hy - 15) + " Q" + (cx - 19) + "," + (hy - 12) + " " + (cx - 25) + "," + (hy + 12) + ' Z" fill="' + (o.hairColor || ink) + '"/>'
      : o.hair === 2 ? "" : '<path d="M' + (cx - 20) + "," + (hy - 8) + " Q" + (cx - 18) + "," + (hy - 27) + " " + (cx + 2) + "," + (hy - 26) + " Q" + (cx + 22) + "," + (hy - 26) + " " + (cx + 21) + "," + (hy - 8) + " Q" + (cx + 4) + "," + (hy - 18) + " " + (cx - 20) + "," + (hy - 8) + ' Z" fill="' + (o.hairColor || ink) + '"/>';
    var hatTop = hy - R;
    var hat = hatSvg(o.hat, cx, hatTop);
    var stache = o.stache ? '<path d="M' + (mx - 10) + "," + (my - 4) + " q5,-5 10,0 q5,-5 10,0 q-10,5 -20,0 z" + '" fill="' + ink + '"/>' : "";
    var monocle = o.prop === "monocle" ? '<circle cx="' + ex(1) + '" cy="' + (hy - 2) + '" r="7.5" fill="none" stroke="' + C.yellow + '" stroke-width="2.4"/><path d="M' + (ex(1) + 6) + "," + (hy + 3) + " q8,14 2,28" + '" fill="none" stroke="' + C.yellow + '" stroke-width="1.6"/>' : "";
    var head = o.prop === "megaphone"
      ? '<g class="head"><path d="M-8,' + (hy + 16) + " L-8," + (hy - 4) + " L24," + (hy - 22) + " L24," + (hy + 34) + " Z" + '" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="4" stroke-linejoin="round"/><ellipse cx="24" cy="' + (hy + 6) + '" rx="6" ry="28" fill="' + ink + '"/></g>'
      : '<g class="head"><circle cx="' + cx + '" cy="' + hy + '" r="' + R + '" fill="' + skin + '" stroke="' + ink + '" stroke-width="4.5"/>' + hair + eyes +
        '<path class="brows" d="' + brows + '" fill="none" stroke="' + ink + '" stroke-width="3" stroke-linecap="round"' + (brows ? "" : ' opacity="0"') + "/>" +
        '<path class="mouth" d="' + mouth + '" fill="' + (mood === "eager" ? ink : "none") + '" stroke="' + ink + '" stroke-width="3" stroke-linecap="round"/>' + stache + monocle + hat + "<!--head-end--></g>";
    var handR = seg(17, -26 - (stretch - 1) * 30, arms[1][0], arms[1][1], 26);
    var handL = seg(-17, -26 - (stretch - 1) * 30, arms[0][0], arms[0][1], 26);
    var prop = {
      briefcase: '<g transform="translate(' + handR.hx.toFixed(1) + "," + handR.hy.toFixed(1) + ')"><rect x="-16" y="4" width="32" height="24" rx="3" fill="#6B4A2F" stroke="' + ink + '" stroke-width="2.6"/><path d="M-6,4 v-5 h12 v5" fill="none" stroke="' + ink + '" stroke-width="2.4"/><path d="M-12,28 L-4,40 H4 L12,28" fill="' + C.paper + '" stroke="' + ink + '" stroke-width="2.4"/></g>',
      poster: '<g transform="translate(' + handL.hx.toFixed(1) + "," + handL.hy.toFixed(1) + ')"><rect x="-34" y="-46" width="40" height="52" fill="' + C.paper + '" stroke="' + ink + '" stroke-width="2.6"/><text x="-14" y="-24" text-anchor="middle" font-family="Oswald" font-size="11" fill="' + C.war + '">BUY</text><text x="-14" y="-10" text-anchor="middle" font-family="Oswald" font-size="11" fill="' + ink + '">BONDS</text></g>',
      clipboard: '<g transform="translate(' + handR.hx.toFixed(1) + "," + handR.hy.toFixed(1) + ')"><rect x="-4" y="-24" width="22" height="30" rx="2" fill="#B98A55" stroke="' + ink + '" stroke-width="2.4"/><rect x="0" y="-20" width="14" height="22" fill="' + C.paper + '"/></g>',
    }[o.prop] || "";
    var light = o.light === "red" ? C.war : o.light === "teal" ? C.med : "#E9E1CC";
    return '<g class="person">' + (longCoat ? "" : leg(-1, "leg-l") + leg(1, "leg-r")) + spine +
      '<path d="M0,' + neckY + " V" + (top + 2) + '" stroke="' + ink + '" stroke-width="6" stroke-linecap="round"/>' + body +
      (longCoat ? leg(-1, "leg-l") + leg(1, "leg-r") : "") +
      '<circle class="chest-light" cx="0" cy="' + (top + 10) + '" r="6.5" fill="' + light + '" stroke="' + ink + '" stroke-width="2.6"/>' +
      arm(-17, arms[0], "arm-l") + arm(17, arms[1], "arm-r") + head + prop + "</g>";
  }
  // The recurring humans (style bible section 3), as presets for person().
  var CAST = {
    richHuman: { tone: 0, outfit: "suit", hat: "top", stache: true, prop: "monocle" },
    politician: { tone: 1, outfit: "suit", tie: "wide", hair: 0 },
    lobbyist: { tone: 2, outfit: "suit", hat: "bowler", prop: "briefcase" },
    weaponsMaker: { tone: 3, outfit: "overalls", color: 1, hat: "hard" },
    orderly: { tone: 2, outfit: "scrubs", tall: true, hair: 2 },
    grandma: { tone: 0, outfit: "dress", color: 3, hair: 1, hairColor: "#B9B5AE", hat: "curlers", prop: "poster" },
    loudHuman: { tone: 1, outfit: "shirt", color: 0, prop: "megaphone" },
    scientist: { tone: 3, outfit: "labcoat", hair: 1, prop: "clipboard" },
  };
  function cast(name, extra) {
    var o = {}, k;
    for (k in CAST[name]) o[k] = CAST[name][k];
    for (k in extra || {}) o[k] = extra[k];
    return person(o);
  }

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
  // Flames all over a person, in the person's own units (put it inside the person's group, after it).
  function fireOn(o) {
    var hy = -56 - ((o && o.tall ? 1.35 : 1) - 1) * 60;
    return '<g class="on-fire">' + flames(-2, 34, 0.95) + flames(-26, -14, 0.5) + flames(26, -14, 0.5) + flames(2, hy - 12, 0.62) + "</g>";
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

  // A walking paper bill around (0,0), 96 x 50, legs to y=48. color: "war" | "med".
  function money(color, legs) {
    var fill = color === "med" ? C.med : C.war;
    var dark = color === "med" ? "#1D5E59" : "#8E2E1E";
    var l = legs === undefined ? 0 : legs;
    return '<g class="money">' +
      '<path class="legs" d="M-16,24 l' + (-6 + l * 10) + ',22 h-8 M16,24 l' + (6 - l * 10) + ',22 h8" fill="none" stroke="' + C.line + '" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>' +
      '<rect x="-48" y="-25" width="96" height="50" rx="4" fill="' + fill + '" stroke="' + C.line + '" stroke-width="4"/>' +
      '<rect x="-41" y="-18" width="82" height="36" rx="2" fill="none" stroke="' + dark + '" stroke-width="2"/>' +
      '<ellipse cx="0" cy="0" rx="13" ry="15" fill="' + C.paper + '" stroke="' + dark + '" stroke-width="2"/>' +
      '<circle cx="0" cy="-2" r="5" fill="none" stroke="' + dark + '" stroke-width="1.8"/>' +
      '<path d="M-7,-4 q-3,6 0,10 M7,-4 q3,6 0,10 M-6,10 q6,-5 12,0" fill="none" stroke="' + dark + '" stroke-width="1.6"/>' +
      '<circle cx="-31" cy="0" r="5" fill="none" stroke="' + dark + '" stroke-width="2"/><circle cx="31" cy="0" r="5" fill="none" stroke="' + dark + '" stroke-width="2"/>' +
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

  // Countdown board: "HUMANS TERMINATED BY CURABLE DISEASES SINCE THIS VIDEO STARTED", 104 per minute.
  var PER_SECOND = 104 / 60;
  function countdownBoard() {
    var digits = "";
    for (var i = 0; i < 6; i++) {
      digits += '<span class="kit-flip"><span class="kit-flip-d">0</span></span>';
    }
    return '<div class="kit-board"><div class="kit-board-title">HUMANS TERMINATED BY CURABLE DISEASES<br>SINCE THIS VIDEO STARTED</div><div class="kit-board-digits">' + digits + "</div></div>";
  }
  function setBoard(board, t) {
    var n = Math.floor(t * PER_SECOND);
    var s = String(n);
    while (s.length < 6) s = "0" + s;
    var ds = board.querySelectorAll(".kit-flip-d");
    for (var i = 0; i < ds.length; i++) if (ds[i].textContent !== s[i]) ds[i].textContent = s[i];
  }

  // Shared CSS (fonts are declared in each composition file).
  var css =
    ".kit-board{position:absolute;width:560px;padding:16px 20px 18px;background:#061D3E;border:6px solid #0B1A33;border-radius:14px;box-shadow:0 0 0 4px #F3ECD0,0 0 0 9px #E5903B;}" +
    ".kit-board-title{font-family:Oswald;font-size:23px;line-height:1.2;letter-spacing:0.06em;color:#F3ECD0;text-align:center;margin-bottom:10px;}" +
    ".kit-board-digits{display:flex;gap:8px;justify-content:center;}" +
    ".kit-flip{position:relative;display:inline-flex;align-items:center;justify-content:center;width:64px;height:84px;background:#273049;border-radius:6px;font-family:Fraunces;font-size:64px;color:#E8B04A;overflow:hidden;}" +
    ".kit-flip::after{content:'';position:absolute;left:0;right:0;top:41px;height:2px;background:#0B1A33;}" +
    ".kit-big{font-family:Fraunces;font-weight:900;color:#1A1426;line-height:0.95;text-shadow:3px 3px 0 #F6EBD2,-3px 3px 0 #F6EBD2,3px -3px 0 #F6EBD2,-3px -3px 0 #F6EBD2,0 4px 0 #F6EBD2,0 -4px 0 #F6EBD2,4px 0 0 #F6EBD2,-4px 0 0 #F6EBD2,6px 8px 0 #1A1426;}" +
    ".kit-label{font-family:Oswald;font-weight:600;text-transform:uppercase;letter-spacing:0.04em;color:#1B1B1B;}";
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  window.KIT = {
    P: P, C: C, V: V, W: W, H: H, OFFICE: OFFICE, form: form, FORM_Q: FORM_Q, FORM_AT: FORM_AT, pipOpts: pipOpts, placeBoard: placeBoard, zoomView: zoomView, enter: enter, drawTick: drawTick,
    scene: scene, cue: cue, cueEnd: cueEnd, after: after, before: before, rng: rng, onTime: onTime,
    mountWishonia: mountWishonia, wishoniaAt: wishoniaAt,
    svg: svg, el: el, office: office, desk: desk, mug: mug, cabinet: cabinet, wallScreen: wallScreen,
    // bean is the old name: every human is now person() (the bean drawing stays as beanClassic).
    paper: paper, paperDefs: paperDefs, grain: grain, star: star, boomerang: boomerang, sun: sun, horizon: V ? 1180 : 610, person: person, cast: cast, CAST: CAST, bean: person, beanClassic: bean, money: money, tophat: tophat,
    flames: flames, fireOn: fireOn, flicker: flicker, nuke: nuke, boom: boom, xray: xray, reaper: reaper,
    checkbox: checkbox, tick: tick, checkSvg: checkSvg, pencil: pencil, countdownBoard: countdownBoard, setBoard: setBoard,
  };
})();
