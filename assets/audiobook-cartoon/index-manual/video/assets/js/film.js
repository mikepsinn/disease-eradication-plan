// The atomic-age instructional film (cartoon-style-bible.md section 1): the period film over every shot, the host's
// studio set, the iris, and the camera that travels over an illustrated plate. Load it after kit.js.
//
//   KIT.film(tl, id, weave, over, seed)       the period film. weave: the element that holds the whole picture (it
//                                             gets the gate weave); over: an empty full-frame element above it.
//   KIT.STUDIO                                the studio set's positions for this canvas shape
//   KIT.studio(tl, id, els, o)                a whole host shot (Layer A): the set, Wishonia, the desk, the push
//   KIT.studioWall(), KIT.console(), KIT.atom(x, y, r, color)   the set's drawings, for scenes that need them alone
//   KIT.iris(tl, id, el, at, mode, t0, t1)    the iris in or out on a point
//   KIT.camera(views, keys, anchor)           a keyed camera over one plate (Layer B)
//   KIT.smooth(u), KIT.mix(a, b, u), KIT.burn(markup)   smoothstep, a color between two, a drawing charred
//
// Copy the reference scenes in compositions/scenes/part-02/ for the element layout each one expects.
(function () {
  var K = window.KIT;
  if (K.film) return;
  var C = K.C, W = K.W, H = K.H, V = K.V, ink = C.line;
  var f = function (n) { return n.toFixed(1); };
  var BLACK = "#0B0805", FULL = "position:absolute;inset:0;";

  function smooth(u) { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); }
  // The color u of the way from a to b (both #rrggbb), as rgb().
  function mix(a, b, u) {
    var pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16);
    return "rgb(" + [16, 8, 0].map(function (sh) { var x = (pa >> sh) & 255, y = (pb >> sh) & 255; return Math.round(x + (y - x) * u); }).join(",") + ")";
  }
  // Burn a drawing (as KIT.person's charred people are burnt): every color but the ink turns a dark brown of the
  // same lightness. Works on #rrggbb fills and strokes.
  function burn(markup) {
    var inkU = ink.toUpperCase();
    return markup.replace(/(fill|stroke)="(#[0-9A-Fa-f]{6})"/g, function (m, a, col) {
      if (col.toUpperCase() === inkU) return m;
      var n = parseInt(col.slice(1), 16), l = (0.3 * (n >> 16) + 0.59 * ((n >> 8) & 255) + 0.11 * (n & 255)) / 255, v = Math.round(28 + l * 46);
      return a + '="rgb(' + (v + 8) + "," + v + "," + Math.max(0, v - 6) + ')"';
    });
  }

  // ── The period film ──
  // A faded warm wash, a soft vignette, two tiles of grain that boil every frame (48 and 71 px, so the repeat never
  // lines up), a little flicker, gate weave, and the odd speck, hair or scratch. `over` sits outside the camera (and
  // outside `weave`), so the camera never scales the grain. seed: any number, different per scene.
  function film(tl, id, weave, over, seed) {
    var D = K.scene(id).duration, g = id + "-grain", gr = K.rng(seed * 977 + 5);
    var tile = function (pid, s, n, rmax, op) {
      var dots = "";
      for (var i = 0; i < n; i++) dots += '<circle cx="' + f(gr() * s) + '" cy="' + f(gr() * s) + '" r="' + f(0.5 + gr() * rmax) + '" fill="' + (gr() < 0.55 ? "#000" : "#FFF") + '" opacity="' + (op * (0.5 + gr())).toFixed(3) + '"/>';
      return '<pattern id="' + pid + '" width="' + s + '" height="' + s + '" patternUnits="userSpaceOnUse">' + dots + "</pattern>";
    };
    var big = '<rect x="-80" y="-80" width="' + (W + 160) + '" height="' + (H + 160) + '"';
    over.innerHTML = '<div style="' + FULL + 'background:rgba(236,220,186,0.1)"></div>' +
      '<div style="' + FULL + 'background:radial-gradient(ellipse 72% 70% at 50% 48%, rgba(0,0,0,0) 52%, rgba(18,10,4,0.42) 100%)"></div>' +
      K.svg(W, H, "<defs>" + tile(g + "a", 48, 46, 0.8, 0.16) + tile(g + "b", 71, 22, 1.4, 0.09) + "</defs>" +
        '<g class="film-ga">' + big + ' fill="url(#' + g + 'a)"/></g><g class="film-gb">' + big + ' fill="url(#' + g + 'b)"/></g><g class="film-dust"></g>',
        'style="position:absolute;inset:0"') + '<div class="film-flick" style="' + FULL + "background:" + BLACK + ';opacity:0"></div>';
    var ga = over.querySelector(".film-ga"), gb = over.querySelector(".film-gb"), dust = over.querySelector(".film-dust"), flick = over.querySelector(".film-flick");
    K.onTime(tl, D, function (t) {
      var fr = Math.floor(t * 24 + 1e-6), r = K.rng(fr * 2654435761 + seed);
      ga.setAttribute("transform", "translate(" + f(-r() * 48) + "," + f(-r() * 48) + ")");
      gb.setAttribute("transform", "translate(" + f(-r() * 71) + "," + f(-r() * 71) + ")");
      var wx = 1.2 * Math.sin(t * 5.1) + 0.6 * Math.sin(t * 11.7 + 1.3) + (r() - 0.5) * 0.9;
      var wy = 0.9 * Math.sin(t * 4.3 + 2.1) + 0.5 * Math.sin(t * 13.9) + (r() - 0.5) * 0.9;
      weave.style.transform = "translate(" + wx.toFixed(2) + "px," + wy.toFixed(2) + "px) scale(1.008)";
      flick.style.opacity = (0.015 + 0.055 * r()).toFixed(3);
      var d = "", k = r(), x = r() * W, y = r() * H;
      if (k < 0.16) d += '<circle cx="' + f(x) + '" cy="' + f(y) + '" r="' + f(1.2 + r() * 2.4) + '" fill="#1A120A" opacity="0.55"/>';
      else if (k > 0.95) d += '<path d="M' + f(x) + "," + f(y) + " q" + f(8 + r() * 10) + "," + f(-6 - r() * 8) + " " + f(20 + r() * 14) + "," + f(r() * 6) + '" fill="none" stroke="#1A120A" stroke-width="1.3" opacity="0.5"/>';
      if (r() < 0.06) { var sx = r() * W; d += '<path d="M' + f(sx) + ",0 L" + f(sx + (r() - 0.5) * 30) + "," + H + '" stroke="#FFF6E2" stroke-width="1.4" opacity="0.22"/>'; }
      dust.innerHTML = d;
    });
  }

  // ── The host's set (Layer A) ──
  // Her observation deck (studioWall below) and Wishonia's
  // console (her desk). Positions in canvas px:
  //   wish  Wishonia's rig (KIT.mountWishonia x, y, w)   face  her face: the iris center and the push's origin
  //   lect  [her center x, her reach on the desk, unused]  top   the desk top.s y
  //   rail  the chair rail's y   floor  the floor's y (H: no floor in shot)   pool  [cx, cy, rx, ry] of the spotlight
  //   right the free wall right of the desk, [x0, x1], for a guest or a prop
  var STUDIO = V
    ? { wish: { x: 110, y: 400, w: 600 }, rail: 1180, top: 1100, lect: [410, 470, 330], floor: 1920, pool: [410, 760, 460, 520], face: [410, 690], right: [700, 1040] }
    : { wish: { x: 480, y: 130, w: 560 }, rail: 700, top: 790, lect: [760, 440, 300], floor: 1080, pool: [760, 420, 450, 420], face: [760, 390], right: [1100, 1880] };
  // The wall is her observation deck: generated art after the book cover (assets/art/deck/deck.webp, 1536 x 1024,
  // cover-fit to the frame), a glass wall onto deep space. Earth hangs in it at STUDIO.earth ([cx, cy, r], clear of
  // her head, for gags that happen on Earth: earth.webp is 667 x 651). A warm glow behind her keeps her black hair
  // off the navy (the same gradient id in every host scene, so a duplicate resolves to the same thing).
  var POOL = "#EDD9A6", POOL2 = "#F3E5BE";
  STUDIO.earth = V ? [850, 250, 150] : [1530, 330, 200];
  function studioWall() {
    var S = STUDIO, p = S.pool, e = S.earth;
    return '<image href="assets/art/deck/deck.webp" width="' + W + '" height="' + H + '" preserveAspectRatio="xMidYMid slice"/>' +
      '<image class="earth" href="assets/art/deck/earth.webp" x="' + f(e[0] - e[2]) + '" y="' + f(e[1] - e[2] * 651 / 667) + '" width="' + f(2 * e[2]) + '" height="' + f(2 * e[2] * 651 / 667) + '"/>' +
      '<defs><radialGradient id="studio-glow"><stop offset="0" stop-color="' + POOL2 + '" stop-opacity="0.75"/>' +
      '<stop offset="0.55" stop-color="' + POOL + '" stop-opacity="0.35"/><stop offset="1" stop-color="' + POOL + '" stop-opacity="0"/></radialGradient></defs>' +
      '<g class="pool"><ellipse cx="' + p[0] + '" cy="' + p[1] + '" rx="' + p[2] * 1.15 + '" ry="' + p[3] * 1.15 + '" fill="url(#studio-glow)"/></g>';
  }
  // The film's emblem: three orbits and an orange nucleus.
  function atom(x, y, r, col) {
    return [0, 60, -60].map(function (a) {
      return '<ellipse cx="' + x + '" cy="' + y + '" rx="' + r + '" ry="' + r * 0.31 + '" fill="none" stroke="' + col + '" stroke-width="' + f(r * 0.05) + '" transform="rotate(' + a + " " + x + " " + y + ')"/>';
    }).join("") + '<circle cx="' + x + '" cy="' + y + '" r="' + f(r * 0.15) + '" fill="' + C.orange + '" stroke="' + col + '" stroke-width="' + f(r * 0.04) + '"/>';
  }
  // Her console, as in the theme song: generated art (assets/art/console/console.webp, 1480 x 428; its sheet and the
  // theme song frame it copies are in sheets/). It runs off the left edge and stops just short of the free wall
  // (S.right); its cream ledge sits at S.top, so the case file and mug stand on it. Under it, the keys, two dials, a
  // readout and the big red button (STUDIO.button: [cx, cy, r], for the scene that presses it). (K.lectern is its
  // old name; K.desk is the old office desk in kit.js.)
  var CON = (function () {
    // 9:16: drawn larger, so its base stands on the deck's floor line (y 1575 there) instead of floating above it.
    var S = STUDIO, x1 = S.right[0] - 20, s = V ? 1.2 : (x1 + 260) / 1480, x0 = x1 - 1480 * s;
    return { x0: x0, x1: x1, s: s, y: S.top - 20 * s, h: 428 * s };
  })();
  STUDIO.button = [CON.x0 + 1317 * CON.s, CON.y + 113 * CON.s, 42 * CON.s];
  function desk() {
    var c = CON;
    return '<image href="assets/art/console/console.webp" x="' + f(c.x0) + '" y="' + f(c.y) + '" width="' + f(1480 * c.s) + '" height="' + f(c.h) + '"/>';
  }
  // A host shot. els: { cam, wall, wish, front } (full-frame elements; cam holds the other three). Draws the wall,
  // mounts Wishonia (her states come from the part file), draws the desk and o.front (more markup in front of
  // her, in canvas px) and pushes the camera slowly in on her face, from o.push[0] to o.push[1] (default 1 → 1.07).
  // Returns { S: KIT.STUDIO, pool: the spotlight pool's <g> }.
  function studio(tl, id, els, o) {
    o = o || {};
    var D = K.scene(id).duration, S = STUDIO;
    els.wall.innerHTML = K.svg(W, H, studioWall());
    K.mountWishonia(tl, els.wish, { scene: id, x: S.wish.x, y: S.wish.y, w: S.wish.w });
    els.front.innerHTML = K.svg(W, H, desk() + (o.front || ""));
    var push = o.push || [1, 1.07], origin = S.face[0] + "px " + S.face[1] + "px";
    tl.fromTo(els.cam, { scale: push[0], transformOrigin: origin }, { scale: push[1], transformOrigin: origin, duration: D, ease: "sine.inOut" }, 0);
    return { S: S, pool: els.wall.querySelector(".pool") };
  }

  // ── The iris ──
  // A black card with a round hole centered on `at` ([x, y], canvas px). mode "in": the hole opens from nothing over
  // [t0, t1] (eased) and then the card is gone; "out": it closes over [t0, t1] and the shot ends on black.
  // el: an empty full-frame element above the picture (inside the weave).
  function iris(tl, id, el, at, mode, t0, t1) {
    if (mode !== "in" && mode !== "out") throw new Error("KIT.iris: mode is \"in\" or \"out\", not " + mode);
    var D = K.scene(id).duration, x = at[0], y = at[1];
    el.innerHTML = K.svg(W, H, '<path fill="' + BLACK + '" fill-rule="evenodd" d=""/>');
    var p = el.querySelector("path"), R = Math.hypot(Math.max(x, W - x), Math.max(y, H - y)) + 40;
    var card = "M-60,-60 H" + (W + 60) + " V" + (H + 60) + " H-60 Z";
    K.onTime(tl, D, function (t) {
      var u = Math.min(1, Math.max(0, (t - t0) / (t1 - t0))), r;
      if (mode === "in") { if (u >= 1) { p.setAttribute("d", ""); return; } r = R * smooth(u); }
      else { if (t < t0) { p.setAttribute("d", ""); return; } r = R * (1 - u) * (1 - u); }
      p.setAttribute("d", card + (r > 1 ? " M" + f(x - r) + "," + y + " a" + f(r) + "," + f(r) + " 0 1,0 " + f(2 * r) + ",0 a" + f(r) + "," + f(r) + " 0 1,0 " + f(-2 * r) + ",0 Z" : ""));
    });
  }

  // ── The plate camera ──
  // views: { name: [plate x, plate y, scale] }; keys: [[time, view name, extra scale (default 1)], ...] in time
  // order. The camera eases from key to key (smoothstep, the scale in log space), so a key that repeats a view with a
  // slightly bigger extra scale is a slow drift, and a pair of keys close together is a quick move. Before the first
  // key it sits on the first; after the last, on the last. anchor: where the looked-at point sits on screen (default
  // the middle in 16:9; in 9:16, x 540, y 740, above the captions). cam.at(t) gives { x, y, s }, which a scene can
  // bend (to chase a missile) before cam.place(el, c) sets el's transform. Views can be added to `views` later.
  function camera(views, keys, anchor) {
    var A = anchor || (V ? [540, 740] : [960, 540]);
    function at(t) {
      var i = 0;
      while (i < keys.length - 2 && t >= keys[i + 1][0]) i++;
      var a = keys[i], b = keys[i + 1] || a, e = b[0] > a[0] ? smooth((t - a[0]) / (b[0] - a[0])) : 1;
      var va = views[a[1]], vb = views[b[1]];
      if (!va || !vb) throw new Error("KIT.camera: no view '" + (va ? b[1] : a[1]) + "'");
      var sa = Math.log(va[2] * (a[2] || 1)), sb = Math.log(vb[2] * (b[2] || 1));
      return { x: va[0] + (vb[0] - va[0]) * e, y: va[1] + (vb[1] - va[1]) * e, s: Math.exp(sa + (sb - sa) * e) };
    }
    function place(el, c) { el.setAttribute("transform", "translate(" + f(A[0] - c.x * c.s) + "," + f(A[1] - c.y * c.s) + ") scale(" + c.s.toFixed(4) + ")"); }
    return { at: at, place: place, A: A, views: views };
  }

  K.film = film;
  K.STUDIO = STUDIO;
  K.studio = studio;
  K.studioWall = studioWall;
  K.console = desk;
  K.lectern = desk;
  K.atom = atom;
  K.iris = iris;
  K.camera = camera;
  K.smooth = smooth;
  K.mix = mix;
  K.burn = burn;
  K.FILM_BLACK = BLACK;
})();
