// Shared kit for the episode cartoon: cue times, the Wishonia rig, and SVG art for both layers.
// Every function is deterministic (no Math.random, no Date), because the renderer seeks frame by frame.
(function () {
  if (window.KIT) return;
  var P = window.HF_PART;

  // ── Colors (cartoon-style-bible.md section 1) ─────────────────────────
  var C = {
    // Layer A: the podcast cover
    red: "#E4432D", orange: "#F08A24", yellow: "#F7C548", peri: "#8F9BDB", cream: "#F6EBD2",
    navy: "#10173A", cyan: "#3FE8F0", ink: "#1A1426",
    // Layer B: the engraving
    paper: "#F3EAD3", line: "#1B1B1B", war: "#D7322B", med: "#1FA39A",
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
        "background:radial-gradient(circle at 50% 70%, #F7C548 0, #F08A24 34%, #E4432D 58%, #8F9BDB 80%);" +
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
  // The full Layer A office backdrop (sky, half-sun, grid floor, dark halo behind Wishonia at hx).
  function office(hx) {
    var w = 1920, h = 1080, hy = 610;
    return svg(w, h,
      "<defs>" +
        '<radialGradient id="kit-halo-' + hx + '" cx="' + hx + '" cy="420" r="560" gradientUnits="userSpaceOnUse">' +
        '<stop offset="0" stop-color="#10173A" stop-opacity="0.55"/><stop offset="0.7" stop-color="#10173A" stop-opacity="0.18"/><stop offset="1" stop-color="#10173A" stop-opacity="0"/></radialGradient>' +
      "</defs>" +
      '<rect width="' + w + '" height="' + h + '" fill="' + C.cream + '"/>' +
      sunburst(w, h, 960, hy, 30) +
      halfSun(960, hy, 250) +
      gridFloor(w, hy, h, 960) +
      '<rect width="' + w + '" height="' + h + '" fill="url(#kit-halo-' + hx + ')"/>'
    );
  }
  // Retro office desk front (drawn in front of Wishonia). Top edge at y.
  function desk(x, y, w) {
    var h = 1080 - y;
    return '<g stroke="' + C.ink + '" stroke-width="6" stroke-linejoin="round">' +
      '<path d="M' + (x - 20) + "," + y + " h" + (w + 40) + " l-18,34 h" + -(w + 4) + ' Z" fill="#B65A2B"/>' +
      '<rect x="' + x + '" y="' + (y + 34) + '" width="' + w + '" height="' + h + '" fill="#D9792F"/>' +
      '<rect x="' + (x + 40) + '" y="' + (y + 70) + '" width="' + (w - 80) + '" height="' + (h - 70) + '" rx="10" fill="#E8913E"/>' +
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
      '<rect x="' + x + '" y="' + y + '" width="230" height="330" rx="10" fill="#7C86C8"/>' +
      [0, 1, 2].map(function (i) {
        var dy = y + 18 + i * 104;
        return '<rect x="' + (x + 16) + '" y="' + dy + '" width="198" height="92" rx="6" fill="#9AA3DE"/>' +
          '<rect x="' + (x + 90) + '" y="' + (dy + 56) + '" width="50" height="14" rx="7" fill="' + C.ink + '"/>' +
          (i === 0 ? '<rect x="' + (x + 36) + '" y="' + (dy + 12) + '" width="158" height="36" fill="' + C.cream + '" stroke-width="3"/>' +
            '<text x="' + (x + 115) + '" y="' + (dy + 36) + '" text-anchor="middle" font-family="Oswald" font-size="17" fill="' + C.ink + '" stroke="none">EARTH: CASE #847</text>' : "");
      }).join("") +
      "</g>";
  }
  // Retro wall screen (TV). Returns svg markup for the bezel; put content inside the hole (x+34, y+34, w-68, h-68).
  function wallScreen(x, y, w, h) {
    return '<g stroke="' + C.ink + '" stroke-width="7" stroke-linejoin="round">' +
      '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="34" fill="#C8572A"/>' +
      '<rect x="' + (x + 34) + '" y="' + (y + 34) + '" width="' + (w - 68) + '" height="' + (h - 68) + '" rx="22" fill="' + C.paper + '"/>' +
      '<circle cx="' + (x + w - 18) + '" cy="' + (y + h + 24) + '" r="0" fill="none"/>' +
      '<path d="M' + (x + w * 0.3) + "," + (y + h) + " l-30,46 M" + (x + w * 0.7) + "," + (y + h) + ' l30,46" fill="none"/>' +
      "</g>";
  }

  // Layer B: paper with a double rule border and hatch patterns. `id` prefixes the pattern ids.
  function paperDefs(id) {
    return "<defs>" +
      '<pattern id="' + id + '-hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="9" stroke="' + C.line + '" stroke-width="1.6"/></pattern>' +
      '<pattern id="' + id + '-cross" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0,0 V9 M0,0 H9" stroke="' + C.line + '" stroke-width="1.5"/></pattern>' +
      '<pattern id="' + id + '-fine" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)"><line x1="0" y1="0" x2="0" y2="6" stroke="' + C.line + '" stroke-width="0.9"/></pattern>' +
      '<pattern id="' + id + '-hred" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#8E1C17" stroke-width="1.6"/></pattern>' +
      '<pattern id="' + id + '-hteal" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#0E5F59" stroke-width="1.6"/></pattern>' +
      "</defs>";
  }
  function paper(id) {
    return svg(1920, 1080,
      paperDefs(id) +
      '<rect width="1920" height="1080" fill="' + C.paper + '"/>' +
      '<rect x="30" y="30" width="1860" height="1020" fill="none" stroke="' + C.line + '" stroke-width="5"/>' +
      '<rect x="44" y="44" width="1832" height="992" fill="none" stroke="' + C.line + '" stroke-width="1.6"/>'
    );
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

  // A walking paper bill around (0,0), 96 x 50, legs to y=48. color: "war" | "med".
  function money(color, legs) {
    var fill = color === "med" ? C.med : C.war;
    var dark = color === "med" ? "#0E5F59" : "#8E1C17";
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
    ".kit-board{position:absolute;width:560px;padding:16px 20px 18px;background:#1E1B24;border:6px solid #1B1B1B;border-radius:14px;box-shadow:0 0 0 4px #F3EAD3;}" +
    ".kit-board-title{font-family:Oswald;font-size:23px;line-height:1.2;letter-spacing:0.06em;color:#F3EAD3;text-align:center;margin-bottom:10px;}" +
    ".kit-board-digits{display:flex;gap:8px;justify-content:center;}" +
    ".kit-flip{position:relative;display:inline-flex;align-items:center;justify-content:center;width:64px;height:84px;background:#2E2A36;border-radius:6px;font-family:Fraunces;font-size:64px;color:#F7C548;overflow:hidden;}" +
    ".kit-flip::after{content:'';position:absolute;left:0;right:0;top:41px;height:2px;background:#111;}" +
    ".kit-big{font-family:Fraunces;font-weight:900;color:#1A1426;line-height:0.95;text-shadow:3px 3px 0 #F6EBD2,-3px 3px 0 #F6EBD2,3px -3px 0 #F6EBD2,-3px -3px 0 #F6EBD2,0 4px 0 #F6EBD2,0 -4px 0 #F6EBD2,4px 0 0 #F6EBD2,-4px 0 0 #F6EBD2,6px 8px 0 #1A1426;}" +
    ".kit-label{font-family:Oswald;font-weight:600;text-transform:uppercase;letter-spacing:0.04em;color:#1B1B1B;}";
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  window.KIT = {
    P: P, C: C, scene: scene, cue: cue, cueEnd: cueEnd, rng: rng, onTime: onTime,
    mountWishonia: mountWishonia, wishoniaAt: wishoniaAt,
    svg: svg, el: el, office: office, desk: desk, mug: mug, cabinet: cabinet, wallScreen: wallScreen,
    paper: paper, paperDefs: paperDefs, bean: bean, money: money, tophat: tophat,
    checkbox: checkbox, tick: tick, checkSvg: checkSvg, pencil: pencil, countdownBoard: countdownBoard, setBoard: setBoard,
  };
})();
