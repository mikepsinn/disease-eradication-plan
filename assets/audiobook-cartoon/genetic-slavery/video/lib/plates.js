// Shared camera plates for the Genetic Slavery cartoon. Copied from the locked Part 1 sketch
// (storyboards/part-01-genetic-slavery.sketch.mjs): khaki field, cream sky, the kit cast, Fraunces
// numbers, Oswald signs. Scenes load this after kit.js, film.js and the props they use.
// The period film itself is KIT.film (outside the camera). This file does not draw grain.
(function () {
  var K = window.KIT;
  var C = K.C;
  var f = function (n) { return (+n).toFixed(1); };
  var SKY = "#EFE3C4", GROUND = "#C8B07B", HZ_LINE = "#8E7A55", SHADOW = "#9C8558", WHITE = "#FBF6E6";

  function at(x, y, k, inner, rot) {
    return '<g transform="translate(' + f(x) + "," + f(y) + ")" + (rot ? " rotate(" + rot + ")" : "") + (k !== 1 ? " scale(" + k + ")" : "") + '">' + inner + "</g>";
  }
  function stand(o, x, groundY, k) {
    return at(x, groundY - 100 * k, k, K.person(o));
  }
  function shadow(x, y, rx, op) {
    return '<ellipse cx="' + f(x) + '" cy="' + f(y) + '" rx="' + f(rx) + '" ry="' + f(rx * 0.16) + '" fill="' + SHADOW + '" opacity="' + (op == null ? 0.35 : op) + '"/>';
  }
  function field(horizon) {
    return '<rect width="1920" height="1080" fill="' + GROUND + '"/><rect width="1920" height="' + horizon + '" fill="' + SKY + '"/>' +
      '<path d="M0,' + horizon + ' H1920" stroke="' + HZ_LINE + '" stroke-width="3" opacity="0.6"/>';
  }
  function number(x, y, size, text, fill, shadowCol, anchor) {
    var a = 'text-anchor="' + (anchor || "middle") + '" font-family="Fraunces" font-weight="900" font-size="' + size + '" letter-spacing="' + (size * 0.02) + '"';
    return '<text x="' + f(x + size * 0.04) + '" y="' + f(y + size * 0.053) + '" ' + a + ' fill="' + shadowCol + '">' + text + "</text>" +
      '<text x="' + x + '" y="' + y + '" ' + a + ' fill="' + fill + '">' + text + "</text>";
  }
  function label(x, y, size, text, fill, extra) {
    return '<text x="' + x + '" y="' + y + '" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="' + size + '" letter-spacing="' + (size * 0.06) + '" fill="' + fill + '" ' + (extra || "") + ">" + text + "</text>";
  }
  function stone(cx, cy, rx, ry, seed, fill, ink) {
    var s = seed * 7919 + 17;
    var r = function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
    var n = 7 + Math.floor(r() * 3), pts = [];
    for (var i = 0; i < n; i++) {
      var a = (i / n) * Math.PI * 2 + r() * 0.3, kk = 0.86 + r() * 0.2;
      pts.push([cx + rx * kk * Math.cos(a), cy + ry * kk * Math.sin(a) * (Math.sin(a) > 0 ? 0.8 : 1)]);
    }
    var d = "M" + pts.map(function (p) { return f(p[0]) + "," + f(p[1]); }).join(" L") + " Z";
    var hi = "M" + f(cx - rx * 0.5) + "," + f(cy - ry * 0.35) + " L" + f(cx - rx * 0.1) + "," + f(cy - ry * 0.62);
    return '<path d="' + d + '" fill="' + fill + '" stroke="' + ink + '" stroke-width="5" stroke-linejoin="miter"/>' +
      '<path d="' + hi + '" stroke="#E4DDCB" stroke-width="5" stroke-linecap="round" opacity="0.7"/>';
  }
  function face(x, y, u, mood, o) {
    o = o || {};
    var ink = o.ink || "#112845", lc = o.line || ink, sp = 13 * u, rx = 8.5 * u, ry = 5.2 * u, look = (o.look || 0) * rx * 0.45;
    var tops = { flat: -ry * 0.55, smug: -ry * 0.55, sly: -ry * 0.5, cross: -ry * 1.2, sad: -ry * 1.6, eager: -ry * 2.4 };
    var bots = { flat: ry * 1, smug: ry * 0.5, sly: ry * 0.45, cross: ry * 1.1, sad: ry * 1.1, eager: ry * 1.7 };
    var top = tops[mood], bot = bots[mood], out = "";
    for (var si = 0; si < 2; si++) {
      var s = si ? 1 : -1;
      var ex = x + s * sp;
      var d = "M" + f(ex - rx) + "," + f(y) + " Q" + f(ex) + "," + f(y + top) + " " + f(ex + rx) + "," + f(y - 0.4 * u) + " Q" + f(ex) + "," + f(y + bot) + " " + f(ex - rx) + "," + f(y) + " Z";
      out += '<path d="' + d + '" fill="' + WHITE + '" stroke="' + ink + '" stroke-width="' + f(1.4 * u) + '"/>' +
        '<circle cx="' + f(ex + look) + '" cy="' + f(y + (top + bot) / 4) + '" r="' + f(ry * (mood === "eager" ? 0.5 : 0.6)) + '" fill="' + ink + '"/>' +
        '<path d="M' + f(ex - rx - 0.8 * u) + "," + f(y + 0.4 * u) + " Q" + f(ex) + "," + f(y + top - 0.8 * u) + " " + f(ex + rx + 0.6 * u) + "," + f(y - 0.6 * u) + '" fill="none" stroke="' + ink + '" stroke-width="' + f(2.6 * u) + '" stroke-linecap="round"/>';
      var brows = { flat: [-11, -12, -11], smug: [-10, -12, -14], sly: [-14, -11, -8], cross: [-14, -11, -7], sad: [-8, -10, -13], eager: [-14, -17, -15] }[mood];
      var bw = rx + 2 * u, ox = ex + s * bw, ix = ex - s * bw * 0.9;
      out += '<path d="M' + f(ox) + "," + f(y + brows[0] * u) + " L" + f(ex + s * bw * 0.1) + "," + f(y + brows[1] * u) + " L" + f(ix) + "," + f(y + brows[2] * u) + '" fill="none" stroke="' + lc + '" stroke-width="' + f(3 * u) + '" stroke-linejoin="miter" stroke-linecap="round"/>';
    }
    var my = y + (o.my || 17) * u, mw = (o.mw || 10) * u;
    var mouth = {
      flat: "M" + f(x - mw) + "," + f(my) + " L" + f(x + mw) + "," + f(my - u),
      smug: "M" + f(x - mw) + "," + f(my + 1 * u) + " Q" + f(x) + "," + f(my + 3 * u) + " " + f(x + mw * 1.1) + "," + f(my - 4 * u),
      sly: "M" + f(x - mw * 1.2) + "," + f(my - 3 * u) + " Q" + f(x - mw * 0.2) + "," + f(my + 6 * u) + " " + f(x + mw * 1.2) + "," + f(my - 5 * u),
      cross: "M" + f(x - mw) + "," + f(my + 2 * u) + " L" + f(x) + "," + f(my - u) + " L" + f(x + mw) + "," + f(my + 2 * u),
      sad: "M" + f(x - mw) + "," + f(my + 3 * u) + " Q" + f(x) + "," + f(my - 4 * u) + " " + f(x + mw) + "," + f(my + 3 * u),
      eager: "M" + f(x - mw) + "," + f(my - 2 * u) + " L" + f(x + mw) + "," + f(my - 2 * u) + " L" + f(x + mw * 0.6) + "," + f(my + 7 * u) + " L" + f(x - mw * 0.6) + "," + f(my + 7 * u) + " Z",
    }[mood];
    out += '<path d="' + mouth + '" fill="' + (mood === "eager" ? ink : "none") + '" stroke="' + lc + '" stroke-width="' + f(2.8 * u) + '" stroke-linecap="round" stroke-linejoin="round"/>';
    if (mood === "sly" || mood === "smug") out += '<path d="M' + f(x + mw * 1.2) + "," + f(my - 8 * u) + " q" + f(4 * u) + "," + f(3 * u) + " " + f(2 * u) + "," + f(8 * u) + '" fill="none" stroke="' + lc + '" stroke-width="' + f(1.8 * u) + '" stroke-linecap="round"/>';
    return out;
  }
  function g(id, inner, ox, oy) {
    return '<g id="' + id + '"' + (ox == null ? "" : ' data-ox="' + ox + '" data-oy="' + oy + '"') + ">" + inner + "</g>";
  }

  // Iron ball on a DNA chain. (0, 0) is the cuff. wide: the ball sits to the right. tall: it hangs below.
  function chain(tall) {
    var ink = C.ink, ballX = tall ? 8 : 250, ballY = tall ? 188 : 6, R = tall ? 36 : 52;
    var x0 = tall ? 4 : 28, y0 = tall ? 10 : 2, x1 = ballX - R * 0.72, y1 = ballY - (tall ? R * 0.2 : 4);
    var n = 80, amp = tall ? 16 : 18, waves = tall ? 4 : 3.2;
    function pt(u, s) {
      var x = x0 + (x1 - x0) * u + (tall ? s * amp * Math.sin(u * Math.PI * waves) : 0);
      var y = y0 + (y1 - y0) * u + (tall ? 0 : s * amp * Math.sin(u * Math.PI * waves)) + Math.sin(u * Math.PI) * (tall ? 8 : 16);
      return [x, y];
    }
    var helix = "", rungs = "";
    for (var si = 0; si < 2; si++) {
      var s = si ? 1 : -1;
      var d = "M" + Array.from({ length: n + 1 }, function (_, i) { return pt(i / n, s).map(f).join(","); }).join(" L");
      helix += '<path d="' + d + '" fill="none" stroke="' + ink + '" stroke-width="11" stroke-linecap="round"/>' +
        '<path d="' + d + '" fill="none" stroke="' + (s < 0 ? C.peri : "#8FA2BF") + '" stroke-width="6" stroke-linecap="round"/>';
    }
    var cols = [C.orange, C.yellow, C.red, C.med];
    for (var i = 1; i < 18; i++) {
      var u = i / 18, a = pt(u, -1), b = pt(u, 1);
      rungs += '<path d="M' + f(a[0]) + "," + f(a[1]) + " L" + f(b[0]) + "," + f(b[1]) + '" stroke="' + ink + '" stroke-width="8" stroke-linecap="round"/>' +
        '<path d="M' + f(a[0]) + "," + f(a[1]) + " L" + f(b[0]) + "," + f(b[1]) + '" stroke="' + cols[i % 4] + '" stroke-width="4"/>';
    }
    return '<g>' +
      '<rect x="-34" y="-16" width="68" height="30" rx="6" fill="' + C.peri + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<path d="M-22,-6 h44" stroke="#8FA2BF" stroke-width="3.4"/>' +
      rungs + helix +
      '<circle cx="' + ballX + '" cy="' + ballY + '" r="' + R + '" fill="#4B5674" stroke="' + ink + '" stroke-width="6"/>' +
      '<path d="M' + (ballX - R * 0.55) + "," + (ballY - R * 0.2) + " Q" + (ballX - R * 0.35) + "," + (ballY - R * 0.7) + " " + (ballX - R * 0.05) + "," + (ballY - R * 0.72) + '" fill="none" stroke="' + C.cream + '" stroke-width="6" stroke-linecap="round" opacity="0.8"/>' +
      "</g>";
  }

  // ── Part 1 plates (locked sketch), split into groups the scenes tween ──

  function sixOhFour(id) {
    var ink = C.line, G = 870, TX = 560, TW = 300, TOP = 262;
    var tower = "", s = 6047;
    var r = function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
    var bundles = 17, bh = (G - TOP) / bundles;
    for (var i = 0; i < bundles; i++) {
      var y = G - (i + 1) * bh, dx = (r() - 0.5) * 18, x = TX - TW / 2 + dx, edges = "";
      for (var k = 1; k < 6; k++) edges += '<path d="M' + f(x + 4) + "," + f(y + (k * bh) / 6) + " H" + f(x + TW - 4) + '" stroke="' + C.moneyDark + '" stroke-width="1.6" opacity="0.55"/>';
      tower += '<rect x="' + f(x) + '" y="' + f(y) + '" width="' + TW + '" height="' + f(bh) + '" fill="' + C.money + '" stroke="' + ink + '" stroke-width="3.4"/>' + edges +
        '<rect x="' + f(x + TW / 2 - 30) + '" y="' + f(y - 1) + '" width="60" height="' + f(bh + 2) + '" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="2.6"/>' +
        K.moneySeal("war", x + TW / 2, y + bh / 2, bh * 0.36);
    }
    var PY = 420, PW = 420, PH = 196;
    function screw(x, y) {
      return '<circle cx="' + x + '" cy="' + y + '" r="7" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="2.6"/>' +
        '<path d="M' + (x - 4) + "," + (y - 4) + ' l8,8" stroke="' + ink + '" stroke-width="2"/>';
    }
    var plaque = '<rect x="' + (TX - PW / 2 + 10) + '" y="' + (PY + 12) + '" width="' + PW + '" height="' + PH + '" fill="' + ink + '" opacity="0.35"/>' +
      '<rect x="' + (TX - PW / 2) + '" y="' + PY + '" width="' + PW + '" height="' + PH + '" rx="6" fill="' + C.yellow + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<rect x="' + (TX - PW / 2 + 12) + '" y="' + (PY + 12) + '" width="' + (PW - 24) + '" height="' + (PH - 24) + '" rx="3" fill="none" stroke="' + C.rust + '" stroke-width="2.4"/>' +
      screw(TX - PW / 2 + 24, PY + 24) + screw(TX + PW / 2 - 24, PY + 24) + screw(TX - PW / 2 + 24, PY + PH - 24) + screw(TX + PW / 2 - 24, PY + PH - 24) +
      label(TX, PY + 88, 66, "POLITICAL", ink) + label(TX, PY + 164, 66, "PROBLEM", ink);
    var xd = "M" + (TX - PW / 2 + 6) + "," + (PY - 26) + " L" + (TX + PW / 2 - 6) + "," + (PY + PH + 26) + " M" + (TX + PW / 2 - 6) + "," + (PY - 26) + " L" + (TX - PW / 2 + 6) + "," + (PY + PH + 26);
    var X = '<path d="' + xd + '" stroke="' + ink + '" stroke-width="17" stroke-linecap="round"/>' +
      '<path d="' + xd + '" stroke="' + C.war + '" stroke-width="10" stroke-linecap="round"/>';
    var WMK = 2.9, WMX = 960, SCK = 2.9, SCX = 1420;
    var wm = K.castOpts("weaponsMaker", { look: "left" });
    var sciWait = K.castOpts("scientist", { look: "left", mood: "flat", arms: [[-20, -8], [20, 8]] });
    var sciO = K.castOpts("scientist", { look: "left", mood: "eager", arms: [[-12, -6], [150, 172]] });
    var sr = K.rig(sciO), hand = [SCX + SCK * sr.hand[1][0], G - 100 * SCK + SCK * sr.hand[1][1]];
    var medBill = at(hand[0] + 10, hand[1] - 46, 1.9, K.money("med", 0).replace('class="legs"', 'class="legs" opacity="0"'), -8);
    var one = number(hand[0] + 10, hand[1] - 120, 150, "1", C.navy, C.cream);
    return field(600) +
      shadow(TX, G + 6, 220) + shadow(WMX, G + 4, 150) + shadow(SCX, G + 4, 110) +
      g(id + "-tower", tower, TX, G) +
      g(id + "-plaque", plaque, TX, PY + PH / 2) +
      g(id + "-xmark", X, TX, PY + PH / 2) +
      g(id + "-n604", number(TX, 220, 170, "604", C.navy, C.cream), TX, 160) +
      stand(wm, WMX, G, WMK) +
      g(id + "-sci-wait", stand(sciWait, SCX, G, SCK)) +
      g(id + "-sci-show", stand(sciO, SCX, G, SCK)) +
      g(id + "-med", medBill + one, hand[0] + 10, hand[1] - 80);
  }

  function hardware(id) {
    var ink = C.line, G = 880, HZ = 600;
    var ST = "#A9A391", ST2 = "#8F8A79", ST3 = "#C2BCA9";
    var hd = '<defs><pattern id="' + id + '-hd" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><circle cx="3.5" cy="3.5" r="1.5" fill="' + ink + '"/></pattern></defs>';
    var rows = [
      [[520, 770, 60, 38], [640, 760, 70, 40], [770, 764, 66, 38], [890, 772, 58, 36]],
      [[430, 820, 70, 42], [560, 818, 76, 44], [700, 822, 80, 42], [840, 818, 74, 44], [970, 824, 66, 40]],
      [[360, 866, 66, 38], [480, 870, 76, 40], [620, 874, 84, 38], [770, 874, 84, 40], [910, 870, 76, 40], [1040, 864, 62, 36]],
    ];
    var hoard = "", n = 0, ri, ci;
    for (ri = 0; ri < rows.length; ri++) for (ci = 0; ci < rows[ri].length; ci++) {
      var rk = rows[ri][ci];
      hoard += stone(rk[0], rk[1], rk[2], rk[3], ++n * 3 + 1, [ST, ST2, ST3][n % 3], ink);
    }
    var CX = 700, top = 236, bot = 744, L = CX - 270, R = CX + 270;
    var hewn = [[L + 6, bot], [L, top + 70], [L + 10, top + 26], [L + 46, top + 6], [CX - 70, top], [CX - 48, top + 14], [CX - 20, top + 2], [R - 46, top], [R - 8, top + 24],
      [R, top + 110], [R - 12, top + 132], [R + 2, top + 160], [R - 4, bot]];
    var hd2 = "M" + hewn.map(function (p) { return p.join(","); }).join(" L") + " Z";
    var cab = '<path d="' + hd2 + '" fill="' + ST + '" stroke="' + ink + '" stroke-width="6" stroke-linejoin="miter"/>' +
      '<clipPath id="' + id + '-cab"><path d="' + hd2 + '"/></clipPath><rect x="' + (R - 120) + '" y="' + top + '" width="140" height="' + (bot - top) + '" fill="url(#' + id + '-hd)" opacity="0.16" clip-path="url(#' + id + '-cab)"/>';
    var SL = L + 38, SY = top + 40, SW = 340, SH = 250;
    var screen = '<rect x="' + (SL - 16) + '" y="' + (SY - 16) + '" width="' + (SW + 32) + '" height="' + (SH + 32) + '" rx="40" fill="' + ST3 + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<rect x="' + SL + '" y="' + SY + '" width="' + SW + '" height="' + SH + '" rx="30" fill="' + C.slate + '" stroke="' + ink + '" stroke-width="6"/>';
    var smug = face(SL + SW / 2 - 6, SY + 100, 5.4, "smug", { look: 1, line: C.cream, ink: ink, my: 17, mw: 12 });
    function reel(x, y) {
      return '<circle cx="' + x + '" cy="' + y + '" r="58" fill="' + ST3 + '" stroke="' + ink + '" stroke-width="5"/>' +
        '<circle cx="' + x + '" cy="' + y + '" r="46" fill="none" stroke="' + ST2 + '" stroke-width="4"/>' +
        [0, 120, 240].map(function (a) {
          return '<circle cx="' + f(x + 26 * Math.cos(((a - 30) * Math.PI) / 180)) + '" cy="' + f(y + 26 * Math.sin(((a - 30) * Math.PI) / 180)) + '" r="13" fill="' + ST2 + '" stroke="' + ink + '" stroke-width="3"/>';
        }).join("") + '<circle cx="' + x + '" cy="' + y + '" r="8" fill="' + ink + '"/>';
    }
    var lamps = [0, 1, 2, 3, 4, 5, 6].map(function (i) {
      return '<circle cx="' + (L + 56 + i * 46) + '" cy="' + (top + 338) + '" r="13" fill="' + [C.orange, C.slate, C.yellow, C.slate, C.orange, C.yellow, C.slate][i] + '" stroke="' + ink + '" stroke-width="3.4"/>';
    }).join("");
    var corner = '<rect x="' + (L + 30) + '" y="' + (bot - 124) + '" width="336" height="58" fill="' + ST3 + '" stroke="' + ink + '" stroke-width="4"/>' +
      '<rect x="' + (L + 38) + '" y="' + (bot - 116) + '" width="320" height="42" fill="none" stroke="' + ST2 + '" stroke-width="2.4"/>' +
      label(L + 198, bot - 84, 28, "EST. 200,000 YEARS AGO", ink);
    var chim = '<path d="M' + (R - 150) + "," + (top + 2) + " L" + (R - 142) + "," + (top - 100) + " H" + (R - 72) + " L" + (R - 64) + "," + (top + 2) + ' Z" fill="' + ST2 + '" stroke="' + ink + '" stroke-width="5" stroke-linejoin="miter"/>' +
      '<path d="M' + (R - 148) + "," + (top - 100) + " H" + (R - 66) + '" stroke="' + ink + '" stroke-width="10"/>';
    var kb = '<path d="M' + (CX - 250) + "," + (bot + 12) + " L" + (CX - 222) + "," + (bot - 34) + " H" + (CX + 222) + " L" + (CX + 250) + "," + (bot + 12) + ' Z" fill="' + ST3 + '" stroke="' + ink + '" stroke-width="5" stroke-linejoin="miter"/>' +
      [0, 1, 2, 3, 4, 5, 6].map(function (i) {
        return '<rect x="' + (CX - 214 + i * 46) + '" y="' + (bot - 24) + '" width="36" height="22" rx="3" fill="' + ST2 + '" stroke="' + ink + '" stroke-width="2.4"/>';
      }).join("");
    var BX = CX + 160, BY = bot - 30;
    var dome = "M" + (BX - 46) + "," + (BY - 14) + " Q" + (BX - 46) + "," + (BY - 82) + " " + BX + "," + (BY - 82) + " Q" + (BX + 46) + "," + (BY - 82) + " " + (BX + 46) + "," + (BY - 14) + " Z";
    var button = '<rect x="' + (BX - 60) + '" y="' + (BY - 16) + '" width="120" height="24" rx="4" fill="' + C.yellow + '" stroke="' + ink + '" stroke-width="4"/>' +
      '<path d="' + dome + '" fill="' + C.war + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<clipPath id="' + id + '-dome"><path d="' + dome + '"/></clipPath>' +
      '<rect x="' + (BX - 9) + '" y="' + (BY - 90) + '" width="18" height="80" fill="' + C.med + '" clip-path="url(#' + id + '-dome)"/>' +
      '<path d="M' + BX + "," + (BY - 84) + " C" + (BX - 20) + "," + (BY - 122) + " " + (BX - 56) + "," + (BY - 112) + " " + (BX - 44) + "," + (BY - 88) + " C" + (BX - 36) + "," + (BY - 76) + " " + (BX - 14) + "," + (BY - 80) + " " + BX + "," + (BY - 84) +
      " Z M" + BX + "," + (BY - 84) + " C" + (BX + 20) + "," + (BY - 122) + " " + (BX + 56) + "," + (BY - 112) + " " + (BX + 44) + "," + (BY - 88) + " C" + (BX + 36) + "," + (BY - 76) + " " + (BX + 14) + "," + (BY - 80) + " " + BX + "," + (BY - 84) +
      ' Z" fill="' + C.med + '" stroke="' + ink + '" stroke-width="4"/>' +
      '<rect x="' + (BX - 10) + '" y="' + (BY - 94) + '" width="20" height="18" rx="5" fill="' + C.med + '" stroke="' + ink + '" stroke-width="3.6"/>';
    var NX = 1650, P0 = [R - 107, top - 120], P1 = [1150, -70], P2 = [NX - 40, HZ - 40], trail = "";
    for (var ti = 0; ti <= 20; ti++) {
      var u = ti / 20, a1 = (1 - u) * (1 - u), b1 = 2 * u * (1 - u), c1 = u * u;
      var x = a1 * P0[0] + b1 * P1[0] + c1 * P2[0], yy = a1 * P0[1] + b1 * P1[1] + c1 * P2[1];
      trail += '<circle cx="' + f(x) + '" cy="' + f(yy) + '" r="' + f(12 + 12 * u) + '" fill="#E9E1CF" stroke="' + ink + '" stroke-width="3.4" opacity="' + (0.45 + 0.55 * u).toFixed(2) + '"/>';
    }
    var cloud = at(NX, HZ + 34, 0.92, K.nuke());
    var SX = 1320, SK = 2.75;
    var aliveO = { tone: 2, outfit: "suit", seed: 4, look: "left", mood: "smile", arms: [[-36, -80], [146, 176]] };
    var charO = { tone: 2, outfit: "suit", seed: 4, look: "left", charred: true, arms: [[-36, -80], [146, 176]] };
    function bouquet(so, grey) {
      var rr = K.rig(so), h0 = [SX + SK * rr.hand[0][0], G - 100 * SK + SK * rr.hand[0][1]];
      var col = grey ? "rgb(84,76,68)" : C.orange, col2 = grey ? "rgb(58,52,47)" : C.yellow;
      function flower(x, y, rot) {
        return '<g transform="translate(' + x + "," + y + ") rotate(" + rot + ')">' +
          [0, 72, 144, 216, 288].map(function (a) {
            var cx = 8 * Math.cos((a * Math.PI) / 180), cy = 8 * Math.sin((a * Math.PI) / 180);
            return '<ellipse cx="' + f(cx) + '" cy="' + f(cy) + '" rx="7" ry="5" transform="rotate(' + a + " " + f(cx) + " " + f(cy) + ')" fill="' + col + '" stroke="' + ink + '" stroke-width="1.8"/>';
          }).join("") + '<circle r="4.5" fill="' + col2 + '" stroke="' + ink + '" stroke-width="1.6"/></g>';
      }
      var smoke = grey ? '<path d="M-14,-46 q-5,-6 0,-11 q5,-6 0,-11 M6,-52 q-5,-6 0,-11 q5,-6 0,-11" fill="none" stroke="#8C8782" stroke-width="2.4" stroke-linecap="round"/>' : "";
      return at(h0[0] - 6, h0[1] + 4, SK,
        '<path d="M0,6 Q-12,-14 -20,-26 M0,6 Q-2,-18 -4,-34 M0,6 Q10,-14 12,-26" fill="none" stroke="' + ink + '" stroke-width="2.6"/>' +
        flower(-22, -30, 30) + flower(-4, -38, 0) + flower(14, -30, -20) + smoke);
    }
    var machine = chim + cab + screen + reel(R - 84, top + 112) + reel(R - 84, top + 246) + lamps + kb +
      g(id + "-face", smug, SL + SW / 2, SY + 120) + g(id + "-corner", corner, L + 198, bot - 90) + g(id + "-button", button, BX, BY - 40);
    return hd + field(HZ) +
      g(id + "-cloud", cloud, NX, HZ + 34) +
      g(id + "-trail", trail) +
      shadow(700, G + 10, 380, 0.4) + shadow(SX, G + 4, 110) +
      g(id + "-hoard", hoard, 700, G) +
      g(id + "-machine", machine, CX, G) +
      g(id + "-stranger", stand(aliveO, SX, G, SK) + bouquet(aliveO, false)) +
      g(id + "-charred", stand(charO, SX, G, SK) + bouquet(charO, true));
  }

  function ownersManual(id) {
    var ink = C.line, FL = 740, G = 900;
    var WALL = "#E6D3A8", WALL2 = "#D9C192", FLOOR = "#9B6A45";
    var paper = "", y, x;
    for (y = 70; y < FL - 40; y += 150) for (x = (y / 150) % 2 ? 40 : 115; x < 1920; x += 150) paper += K.boomerang(x, y, 0.42, WALL2, ((x * 7 + y) % 360));
    var room = '<rect width="1920" height="1080" fill="' + FLOOR + '"/><rect width="1920" height="' + FL + '" fill="' + WALL + '"/>' + paper +
      '<rect y="' + (FL - 28) + '" width="1920" height="28" fill="' + C.rust + '"/><path d="M0,' + FL + ' H1920" stroke="' + ink + '" stroke-width="4"/>' +
      [0, 1, 2, 3, 4, 5].map(function (i) { return '<path d="M0,' + (FL + 56 + i * 58) + ' H1920" stroke="#86593A" stroke-width="3"/>'; }).join("") +
      '<ellipse cx="960" cy="' + (G - 8) + '" rx="640" ry="74" fill="' + C.orange + '" stroke="' + ink + '" stroke-width="4"/>' +
      '<ellipse cx="960" cy="' + (G - 8) + '" rx="580" ry="56" fill="none" stroke="' + C.yellow + '" stroke-width="5"/>';
    var lamp = '<path d="M330,' + G + " l-44,16 M330," + G + " l44,16 M330," + G + ' V300" stroke="' + ink + '" stroke-width="8" stroke-linecap="round"/>' +
      '<path d="M246,300 L278,186 H382 L414,300 Z" fill="' + C.yellow + '" stroke="' + ink + '" stroke-width="5"/>';
    var CHX = 720;
    var chairBack = '<path d="M' + (CHX - 200) + "," + (G - 130) + " L" + (CHX - 214) + "," + (G - 440) + " Q" + (CHX - 210) + "," + (G - 492) + " " + (CHX - 150) + "," + (G - 492) + " H" + (CHX + 150) + " Q" + (CHX + 210) + "," + (G - 492) + " " + (CHX + 214) + "," + (G - 440) + " L" + (CHX + 200) + "," + (G - 130) + ' Z" fill="' + C.orange + '" stroke="' + ink + '" stroke-width="6"/>' +
      '<path d="M' + (CHX - 176) + "," + (G - 40) + " L" + (CHX - 196) + "," + (G + 14) + " M" + (CHX + 176) + "," + (G - 40) + " L" + (CHX + 196) + "," + (G + 14) + '" stroke="' + ink + '" stroke-width="10" stroke-linecap="round"/>' +
      '<rect x="' + (CHX - 222) + '" y="' + (G - 180) + '" width="444" height="140" rx="18" fill="' + C.orange + '" stroke="' + ink + '" stroke-width="6"/>' +
      '<rect x="' + (CHX - 250) + '" y="' + (G - 300) + '" width="106" height="262" rx="30" fill="' + C.orange + '" stroke="' + ink + '" stroke-width="6"/>';
    var chairArm = '<rect x="' + (CHX + 150) + '" y="' + (G - 300) + '" width="106" height="262" rx="30" fill="' + C.orange + '" stroke="' + ink + '" stroke-width="6"/>';
    var RK = 3.4, RX = CHX - 20, SEAT = G - 176;
    var man = { tone: 1, outfit: "shirt", color: 1, hair: 0, seed: 7, look: "right", mood: "smile", arms: [[14, 70], [26, 76]], build: { legPose: [[84, 4], [84, 4]] } };
    var mr = K.rig(man);
    var lid = '<g id="' + id + '-lid"><ellipse cx="2" cy="-23" rx="16" ry="5.5" fill="' + C.ink + '" stroke="' + ink + '" stroke-width="1.6"/>' +
      '<path d="M-12,-22 Q2,-26 16,-23" fill="none" stroke="#E9B4C1" stroke-width="2.4"/>' +
      '<g transform="translate(-14,-23) rotate(-72)"><path d="M0,0 Q2,-20 16,-22 Q30,-20 32,0 Z" fill="' + ink + '" stroke="' + ink + '" stroke-width="2.2"/>' +
      '<path d="M2,-1.5 H30" stroke="#D9B48F" stroke-width="5"/></g></g>';
    var manSvg = K.person(man).replace("<!--face-end-->", lid + "<!--face-end-->");
    var manAt = [RX, SEAT - mr.hipY * RK];
    var head = [manAt[0] + RK * mr.top[0], manAt[1] + RK * mr.top[1]];
    var BW = 256, BHt = 300, BKX = RX + 40, BKY = head[1] + 168 + BHt / 2;
    var book = '<g transform="translate(' + f(BKX) + "," + f(BKY) + ') rotate(6)">' +
      '<rect x="' + (-BW / 2) + '" y="' + (-BHt / 2) + '" width="' + BW + '" height="' + BHt + '" fill="' + C.orange + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<rect x="' + (-BW / 2 + 12) + '" y="' + (-BHt / 2 + 12) + '" width="' + (BW - 24) + '" height="' + (BHt - 24) + '" fill="none" stroke="' + WHITE + '" stroke-width="3" opacity="0.8"/>' +
      '<rect x="' + (-BW / 2 + 12) + '" y="' + (-BHt / 2 + 30) + '" width="' + (BW - 24) + '" height="56" fill="' + C.navy + '"/>' +
      label(0, -BHt / 2 + 69, 26, "OWNER'S MANUAL", C.cream) +
      number(0, 70, 112, "YOU", WHITE, C.ink) + "</g>";
    var BRX = 1290, BRY = 560, BK = 1.35, pink = "#E9B4C1", fold = "#C98B9A";
    var brainBody = '<path d="M-120,10 C-150,-20 -140,-80 -96,-96 C-90,-140 -30,-150 -4,-122 C20,-152 84,-146 96,-104 C142,-96 156,-36 126,-4 C132,40 88,64 52,54 C30,80 -30,80 -48,56 C-96,70 -138,46 -120,10 Z" fill="' + pink + '" stroke="' + ink + '" stroke-width="6"/>' +
      '<path d="M-4,-122 C-10,-90 8,-60 -2,-30 C-10,-4 6,24 0,52" fill="none" stroke="' + fold + '" stroke-width="6" stroke-linecap="round"/>' +
      '<path d="M-96,-96 q30,10 26,40 q-4,26 24,34 M96,-104 q-30,14 -22,40 q6,24 -20,36" fill="none" stroke="' + fold + '" stroke-width="5" stroke-linecap="round"/>';
    var brainFace = face(-10, -36, 2.5, "sly", { look: -1, my: 18, mw: 14 });
    var legY = (G - BRY) / BK;
    var legs = '<path d="M-40,60 L-70,' + f(legY * 0.62) + " L-96," + f(legY - 4) + " M36,62 L40," + f(legY * 0.6) + " L70," + f(legY - 16) + '" fill="none" stroke="' + ink + '" stroke-width="9" stroke-linecap="round"/>';
    var armsB = '<path d="M-116,-40 L-146,-130 L-104,-214 M110,-64 L132,-150 L80,-218" fill="none" stroke="' + ink + '" stroke-width="9" stroke-linecap="round"/>';
    var bomb = g(id + "-bomb", at(-16, -196, 1.5, K.props.bomb({})));
    var brain = at(BRX, BRY, BK, legs + armsB + brainBody + brainFace + bomb, -9);
    var c0 = [head[0] + 6, head[1] + 8], c1 = [BRX - 30, BRY + 74];
    var cd = "M" + f(c0[0]) + "," + f(c0[1]) + " C" + f(c0[0] + 30) + "," + f(c0[1] - 230) + " " + f(c1[0] - 220) + "," + f(c1[1] - 260) + " " + f(c1[0] - 160) + "," + f(c1[1] + 30) +
      " S" + f(c1[0] - 40) + "," + f(c1[1] + 60) + " " + f(c1[0]) + "," + f(c1[1]);
    var cord = '<path d="' + cd + '" fill="none" stroke="' + ink + '" stroke-width="16" stroke-linecap="round"/>' +
      '<path d="' + cd + '" fill="none" stroke="' + pink + '" stroke-width="8" stroke-linecap="round"/>';
    return room + lamp + shadow(CHX, G + 10, 280, 0.4) + shadow(BRX, G + 6, 120, 0.4) + chairBack +
      at(manAt[0], manAt[1], RK, manSvg) + chairArm +
      g(id + "-book", book, BKX, BKY) +
      g(id + "-cord", cord) +
      g(id + "-brain", brain, BRX, BRY);
  }

  function universe(id) {
    var ink = C.line, AX = 960, AY = 560, NR = 110;
    var s = 4004;
    var r = function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
    var dust = "";
    for (var i = 0; i < 36; i++) dust += '<circle cx="' + f(r() * 1920) + '" cy="' + f(r() * 1080) + '" r="' + f(1 + r() * 1.6) + '" fill="' + C.cream + '" opacity="' + (0.15 + r() * 0.25).toFixed(2) + '"/>';
    function word(id2, x, y, size, text) {
      return g(id2, number(x, y, size, text, C.cream, "#000814"), x, y - size * 0.7);
    }
    var head = word(id + "-w-how", 960, 300, 120, "HOW") +
      word(id + "-w-h", 960, 450, 110, "HYDROGEN") +
      word(id + "-w-l", 620, 600, 84, "LEARNED") +
      word(id + "-w-to", 980, 600, 84, "TO") +
      word(id + "-w-w", 1320, 600, 84, "WORRY") +
      g(id + "-recap", label(960, 760, 42, "A 13.8 BILLION YEAR RECAP", C.yellow));
    var HAIR = "#EEE9DC", HAIR2 = "#B4AE9E", LID = "#C9712F";
    var eye = function (ex) {
      return '<ellipse cx="' + ex + '" cy="' + (AY - 28) + '" rx="26" ry="16" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="4"/>' +
        '<circle cx="' + (ex + 6) + '" cy="' + (AY - 22) + '" r="8" fill="' + ink + '"/>' +
        '<path d="M' + (ex - 28) + "," + (AY - 28) + " Q" + ex + "," + (AY - 22) + " " + (ex + 28) + "," + (AY - 28) + '" fill="' + LID + '" stroke="' + ink + '" stroke-width="4"/>';
    };
    var nucleus = '<circle cx="' + AX + '" cy="' + AY + '" r="' + NR + '" fill="' + C.orange + '" stroke="' + ink + '" stroke-width="6"/>' +
      '<circle cx="' + (AX - 40) + '" cy="' + (AY - 48) + '" r="16" fill="' + C.yellow + '" opacity="0.9"/>' +
      eye(AX - 36) + eye(AX + 36);
    var RX = 380, RY = 120, TILT = -16, tr = (TILT * Math.PI) / 180;
    function op(a) {
      return [AX + RX * Math.cos(a) * Math.cos(tr) - RY * Math.sin(a) * Math.sin(tr), AY + RX * Math.cos(a) * Math.sin(tr) + RY * Math.sin(a) * Math.cos(tr)];
    }
    var orbit = '<ellipse cx="' + AX + '" cy="' + AY + '" rx="' + RX + '" ry="' + RY + '" fill="none" stroke="' + C.cream + '" stroke-width="7" transform="rotate(' + TILT + " " + AX + " " + AY + ')" opacity="0.9"/>';
    var e0 = op(-0.4);
    var electron = '<circle id="' + id + '-electron" cx="' + f(e0[0]) + '" cy="' + f(e0[1]) + '" r="26" fill="' + C.med + '" stroke="' + ink + '" stroke-width="5"/>';
    var beard = '<path d="M' + (AX - 90) + "," + (AY + 20) + " Q" + (AX - 70) + "," + (AY + 220) + " " + AX + "," + (AY + 280) + " Q" + (AX + 70) + "," + (AY + 220) + " " + (AX + 90) + "," + (AY + 20) + " Q" + AX + "," + (AY + 70) + " " + (AX - 90) + "," + (AY + 20) + ' Z" fill="' + HAIR + '" stroke="' + ink + '" stroke-width="5"/>';
    var stache = '<path d="M' + (AX - 70) + "," + (AY + 24) + " Q" + AX + "," + (AY + 8) + " " + (AX + 70) + "," + (AY + 24) + " Q" + AX + "," + (AY + 55) + " " + (AX - 70) + "," + (AY + 24) + ' Z" fill="' + HAIR + '" stroke="' + ink + '" stroke-width="4"/>';
    var web = '<path d="M' + (AX - 300) + "," + (AY - 30) + " L" + (AX - 40) + "," + (AY - 50) + " M" + (AX - 260) + "," + (AY - 110) + " L" + (AX - 50) + "," + (AY + 30) + " M" + (AX - 220) + "," + (AY + 40) + " L" + (AX - 70) + "," + (AY - 90) + " M" + (AX - 180) + "," + (AY - 100) + " Q" + (AX - 140) + "," + (AY - 20) + " " + (AX - 90) + "," + (AY + 20) + '" fill="none" stroke="' + C.cream + '" stroke-width="5"/>' +
      '<circle cx="' + (AX - 70) + '" cy="' + (AY + 28) + '" r="11" fill="' + ink + '" stroke="' + C.cream + '" stroke-width="3"/>' +
      '<path d="M' + (AX - 78) + "," + (AY + 22) + " l-16,-12 M" + (AX - 62) + "," + (AY + 22) + " l16,-10 M" + (AX - 76) + "," + (AY + 34) + " l-14,12 M" + (AX - 62) + "," + (AY + 34) + ' l14,10" stroke="' + C.cream + '" stroke-width="3" fill="none"/>';
    var counter = g(id + "-count",
      '<text id="' + id + '-num-s" x="968" y="150" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="120" fill="#000814">0</text>' +
      '<text id="' + id + '-num" x="960" y="142" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="120" fill="' + C.cream + '">0</text>' +
      label(960, 210, 42, "YEARS", C.yellow));
    return '<rect width="1920" height="1080" fill="' + C.ink + '"/>' + dust +
      g(id + "-head", head) +
      counter +
      g(id + "-atom", orbit + nucleus + electron, AX, AY) +
      g(id + "-beard", beard + stache, AX, AY + 20) +
      g(id + "-web", web, AX - 160, AY);
  }

  function origin(el) {
    var ox = el.getAttribute("data-ox"), oy = el.getAttribute("data-oy");
    if (ox != null) gsap.set(el, { svgOrigin: ox + " " + oy });
  }

  function play(id, seed, build) {
    var tl = gsap.timeline({ paused: true });
    var q = function (s) { return document.getElementById(id + "-" + s); };
    var D = K.scene(id).duration;
    var svg = q("svg");
    svg.setAttribute("viewBox", "0 0 " + K.W + " " + K.H);
    svg.setAttribute("width", K.W);
    svg.setAttribute("height", K.H);
    K.film(tl, id, q("weave"), q("film"), seed);
    var cam = q("cam");
    var S = {
      id: id, tl: tl, q: q, cam: cam, D: D, C: C, V: K.V, W: K.W, H: K.H,
      cue: function (w, n) { return K.cue(id, w, n); },
      after: function (w, n) { return K.after(id, w, n); },
      before: function (w, n) { return Math.max(0, K.before(id, w, n)); },
      g: function (s) { return document.getElementById(id + "-" + s); },
      on: function (fn) { K.onTime(tl, D, fn); },
    };
    // A set at time 0 holds the start pose. A later fromTo does not: a seek before it
// snaps back to the untransformed drawing.
    S.drop = function (s, t, dur) {
      var el = S.g(s);
      tl.set(el, { opacity: 0, y: -220 }, 0);
      tl.to(el, { opacity: 1, y: 0, duration: dur || 0.4, ease: "bounce.out" }, t);
    };
    S.pop = function (s, t, dur) {
      var el = S.g(s);
      origin(el);
      tl.set(el, { opacity: 0, scale: 0.12 }, 0);
      tl.to(el, { opacity: 1, scale: 1, duration: dur || 0.32, ease: "back.out(1.7)" }, t);
    };
    S.grow = function (s, t, dur) {
      var el = S.g(s);
      origin(el);
      tl.set(el, { opacity: 0, scaleY: 0 }, 0);
      tl.to(el, { opacity: 1, scaleY: 1, duration: dur || 0.5, ease: "power2.out" }, t);
    };
    S.slam = function (s, t) {
      var el = S.g(s);
      origin(el);
      tl.set(el, { opacity: 0, scale: 1.65 }, 0);
      tl.to(el, { opacity: 1, scale: 1, duration: 0.14, ease: "power3.in" }, t);
    };
    S.hide = function (s) { tl.set(S.g(s), { opacity: 0 }, 0); };
    S.show = function (s, t) { tl.set(S.g(s), { opacity: 1 }, t); };
    build(S);
    var anchor = K.V ? [540, 700] : [960, 540];
    var views = S.views || { wide: K.V ? [960, 540, 0.5625] : [960, 540, 1] };
    var keys = S.keys || [[0, "wide"], [Math.max(0.01, D), "wide", 1.035]];
    var camera = K.camera(views, keys, anchor);
    K.onTime(tl, D, function (t) { camera.place(cam, camera.at(t)); });
    tl.set({}, {}, D);
    window.__timelines = window.__timelines || {};
    window.__timelines[id] = tl;
  }

  // One hydrogen and one lizard for the whole act. Feet of the lizard are at y 100, like a person.
  function hydrogen(o) {
    o = o || {};
    var r = o.r || 64, ink = C.line, col = o.orbit || ink;
    return '<ellipse cx="0" cy="0" rx="' + f(r * 2.15) + '" ry="' + f(r * 0.62) + '" fill="none" stroke="' + col + '" stroke-width="6" transform="rotate(-16)"/>' +
      '<circle r="' + r + '" fill="' + C.orange + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<circle cx="' + f(-r * 0.32) + '" cy="' + f(-r * 0.38) + '" r="' + f(r * 0.16) + '" fill="' + C.yellow + '"/>' +
      face(0, -r * 0.08, r / 32, o.mood || "flat", { look: o.look || 0, my: 14, mw: 7 }) +
      '<circle cx="' + f(r * 1.55) + '" cy="' + f(r * 0.28) + '" r="' + f(r * 0.26) + '" fill="' + C.med + '" stroke="' + ink + '" stroke-width="4"/>' +
      (o.mark ? label(0, r * 0.95, Math.max(18, r * 0.55), o.mark, C.navy) : "");
  }
  function lizard(o) {
    o = o || {};
    var ink = C.line, hide = "#5C7344", belly = "#E7D7A4", drive = o.pose === "drive";
    var arms = drive
      ? '<path d="M-22,4 L-48,36 L-16,50 M22,4 L48,36 L16,50" fill="none" stroke="' + ink + '" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
      : '<path d="M-24,2 L-52,28 M24,2 L52,28" fill="none" stroke="' + ink + '" stroke-width="8" stroke-linecap="round"/>';
    return '<path d="M18,46 C78,28 108,78 82,102 C58,86 36,80 20,70" fill="' + hide + '" stroke="' + ink + '" stroke-width="5" stroke-linejoin="round"/>' +
      '<path d="M-16,74 L-32,100 M-32,100 L-50,94 M16,74 L32,100 M32,100 L50,94" fill="none" stroke="' + ink + '" stroke-width="8" stroke-linecap="round"/>' +
      '<ellipse cx="0" cy="38" rx="38" ry="44" fill="' + hide + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<ellipse cx="0" cy="46" rx="20" ry="28" fill="' + belly + '"/>' +
      arms +
      '<ellipse cx="0" cy="-24" rx="32" ry="28" fill="' + hide + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<ellipse cx="0" cy="-8" rx="18" ry="12" fill="' + belly + '"/>' +
      face(0, -30, 1.35, o.mood || "flat", { look: o.look || 0, my: 14, mw: 8 });
  }
  function flask(mood) {
    var ink = C.line;
    return '<path d="M-16,-78 H16 V-36 L46,18 H-46 L-16,-36 Z" fill="' + WHITE + '" stroke="' + ink + '" stroke-width="5" stroke-linejoin="round"/>' +
      '<path d="M-34,2 H34 L28,18 H-28 Z" fill="' + C.med + '"/>' +
      '<rect x="-20" y="-92" width="40" height="16" fill="' + C.peri + '" stroke="' + ink + '" stroke-width="4"/>' +
      face(0, -16, 1.25, mood || "smug", { my: 12, mw: 7 });
  }
  function boot() {
    return '<path d="M-36,-8 L-24,-78 H8 L16,-22 H62 V14 H-48 L-36,-8 Z" fill="#3A2A22" stroke="' + C.line + '" stroke-width="5" stroke-linejoin="round"/>';
  }
  function teapot() {
    return '<path d="M-8,-36 L-4,-58 H16 L20,-36" fill="' + C.cream + '" stroke="' + C.line + '" stroke-width="5"/>' +
      '<ellipse cx="0" cy="0" rx="38" ry="30" fill="' + C.cream + '" stroke="' + C.line + '" stroke-width="5"/>' +
      '<path d="M36,-4 Q64,-16 50,18" fill="none" stroke="' + C.line + '" stroke-width="7"/>' +
      '<path d="M-38,-2 Q-64,-18 -44,14" fill="none" stroke="' + C.line + '" stroke-width="7"/>';
  }
  function duck() {
    return '<ellipse cx="-4" cy="10" rx="36" ry="24" fill="' + C.yellow + '" stroke="' + C.line + '" stroke-width="5"/>' +
      '<circle cx="24" cy="-16" r="16" fill="' + C.yellow + '" stroke="' + C.line + '" stroke-width="5"/>' +
      '<path d="M34,-18 H58 L34,-6 Z" fill="' + C.orange + '" stroke="' + C.line + '" stroke-width="4"/>' +
      '<circle cx="28" cy="-20" r="2.4" fill="' + C.line + '"/>';
  }
  function matchstick(lit) {
    var stick = '<rect x="-5" y="-10" width="10" height="78" rx="2" fill="#C4A574" stroke="' + C.line + '" stroke-width="3"/>';
    var head = '<ellipse cx="0" cy="-16" rx="12" ry="16" fill="' + C.war + '" stroke="' + C.line + '" stroke-width="3"/>';
    var flame = lit ? '<path d="M0,-28 C-16,-48 -8,-78 0,-96 C8,-78 16,-48 0,-28 Z" fill="' + C.orange + '" stroke="' + C.line + '" stroke-width="3"/><path d="M0,-40 C-6,-56 0,-72 0,-80 C4,-68 6,-54 0,-40 Z" fill="' + C.yellow + '"/>' : "";
    return stick + head + flame;
  }
  function card(x, y, w, h, fill) {
    return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="8" fill="' + fill + '" stroke="' + C.line + '" stroke-width="5"/>';
  }

  function lowExpectations(id) {
    var ink = C.line, G = 900;
    var desk = '<rect x="180" y="250" width="760" height="560" rx="8" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="6"/>' +
      [0, 1, 2, 3, 4, 5, 6].map(function (i) { return '<path d="M240,' + (360 + i * 52) + ' H860" stroke="' + C.peri + '" stroke-width="4" opacity="0.4"/>'; }).join("");
    var chair = '<path d="M1180,900 L1160,520 Q1160,470 1220,470 H1500 Q1560,470 1560,520 L1540,900" fill="' + C.orange + '" stroke="' + ink + '" stroke-width="6"/>';
    return field(520) + shadow(1360, G, 160) + chair +
      g(id + "-atom", at(1360, 430, 1, hydrogen({ r: 70, mood: "flat" })), 1360, 430) +
      desk +
      g(id + "-hired", at(560, 560, 4.2, K.props.stampMark({ text: "HIRED", color: C.war, fontSize: 26, angle: -8 })), 560, 500);
  }
  function calledStars(id) {
    var ink = C.line, G = 900;
    var rays = "";
    for (var i = 0; i < 14; i++) {
      var a = (i / 14) * Math.PI * 2;
      rays += '<path d="M' + f(760 + Math.cos(a) * 150) + "," + f(300 + Math.sin(a) * 150) + " L" + f(760 + Math.cos(a) * 230) + "," + f(300 + Math.sin(a) * 230) + '" stroke="' + C.yellow + '" stroke-width="12" stroke-linecap="round"/>';
    }
    var press = '<rect x="520" y="430" width="480" height="470" fill="' + C.slate + '" stroke="' + ink + '" stroke-width="6"/>' +
      '<rect x="470" y="860" width="580" height="40" fill="' + C.navy + '" stroke="' + ink + '" stroke-width="5"/>' +
      rays + '<circle cx="760" cy="300" r="150" fill="' + C.orange + '" stroke="' + ink + '" stroke-width="6"/>' +
      face(760, 290, 6, "cross", { my: 16, mw: 12 });
    var jaw = '<rect x="560" y="470" width="400" height="70" fill="' + C.peri + '" stroke="' + ink + '" stroke-width="5"/>';
    return field(500) + press +
      g(id + "-jaw", jaw, 760, 540) +
      g(id + "-hin", at(760, 250, 0.7, hydrogen({ r: 40, mood: "sad" })), 760, 250) +
      g(id + "-cball", at(1180, 700, 1, '<circle r="54" fill="#3A3A3A" stroke="' + ink + '" stroke-width="5"/>' + label(0, 12, 48, "C", C.cream)), 1180, 700) +
      g(id + "-oball", at(1360, 820, 1, '<circle r="54" fill="' + C.med + '" stroke="' + ink + '" stroke-width="5"/>' + label(0, 12, 48, "O", C.cream)), 1360, 820) +
      g(id + "-crack", '<path d="M560,500 L700,700 L640,860 M980,480 L860,680 L1040,900" fill="none" stroke="' + C.cream + '" stroke-width="8"/>');
  }
  function fatality(id) {
    var ink = C.line;
    var rubble = "";
    for (var i = 0; i < 8; i++) rubble += '<rect x="' + (180 + (i % 4) * 90) + '" y="' + (700 + Math.floor(i / 4) * 70) + '" width="120" height="28" transform="rotate(' + ((i - 3) * 8) + " " + (240 + i * 40) + ' 760)" fill="' + C.slate + '" stroke="' + ink + '" stroke-width="4"/>';
    var board = card(980, 160, 820, 760, C.yellow) +
      '<rect x="1004" y="184" width="772" height="712" fill="none" stroke="' + ink + '" stroke-width="4"/>' +
      label(1390, 280, 54, "FATALITY", ink);
    return field(480) + rubble +
      '<circle cx="360" cy="280" r="70" fill="' + C.orange + '" opacity="0.35"/>' +
      board +
      g(id + "-pct", number(1390, 520, 200, "100%", C.navy, C.cream), 1390, 420) +
      g(id + "-years", number(1390, 760, 64, "9,000,000,000", C.navy, C.cream) + label(1390, 830, 48, "YEARS", ink), 1390, 760);
  }
  function namedDirt(id) {
    var ink = C.line;
    var glass = '<path d="M560,860 L620,280 H1300 L1360,860 Z" fill="' + C.cream + '" opacity="0.35" stroke="' + ink + '" stroke-width="6"/>' +
      '<path d="M700,320 L760,800" stroke="' + WHITE + '" stroke-width="8" opacity="0.7"/>';
    var rock = stone(960, 700, 150, 90, 4, "#8A8172", ink);
    function mark(n, x, y) {
      return g(id + "-s" + n, at(x, y, 2.4, K.props.stampMark({ text: "UNREMARKABLE", color: C.war, fontSize: 18, angle: -6 })), x, y) +
        g(id + "-x" + n, '<path d="M' + (x - 150) + "," + (y - 40) + " L" + (x + 150) + "," + (y + 30) + " M" + (x + 140) + "," + (y - 36) + " L" + (x - 140) + "," + (y + 34) + '" stroke="' + ink + '" stroke-width="10" stroke-linecap="round"/>');
    }
    return field(500) + glass + rock +
      mark(1, 420, 300) + mark(2, 1500, 340) + mark(3, 430, 620) +
      g(id + "-plate", card(700, 860, 520, 90, C.navy) + label(960, 922, 54, "DIRT", C.cream), 960, 900);
  }
  function promiscuous(id) {
    var ink = C.line;
    function link(x, y) { return '<path d="M960,520 L' + x + "," + y + '" stroke="' + ink + '" stroke-width="8"/>'; }
    var carbon = '<circle r="86" fill="#2A2A2A" stroke="' + ink + '" stroke-width="6"/>' +
      '<circle cx="-22" cy="-30" r="10" fill="#5A5A5A"/>' +
      face(0, -22, 2.15, "sly", { look: 1, line: C.cream, ink: ink, my: 13, mw: 7 }) +
      label(0, 62, 52, "C", C.cream);
    return field(520) +
      g(id + "-links", link(360, 280) + link(1500, 260) + link(280, 780) + link(700, 820) + link(1200, 800) + link(1600, 700)) +
      at(960, 520, 1, carbon) +
      g(id + "-boot", at(360, 280, 1.3, boot()), 360, 280) +
      g(id + "-pot", at(1500, 260, 1.4, teapot()), 1500, 260) +
      g(id + "-duck", at(1600, 720, 1.5, duck()), 1600, 720) +
      g(id + "-hh", at(300, 800, 0.8, hydrogen({ r: 36, mood: "flat", mark: "H" })), 300, 800) +
      g(id + "-oo", at(720, 860, 0.8, hydrogen({ r: 36, mood: "eager", mark: "O", orbit: C.med })), 720, 860) +
      g(id + "-nn", at(1220, 840, 0.8, hydrogen({ r: 36, mood: "flat", mark: "N" })), 1220, 840);
  }
  function copyMachine(id) {
    var ink = C.line;
    var box = '<rect x="460" y="280" width="1000" height="560" rx="16" fill="' + C.slate + '" stroke="' + ink + '" stroke-width="6"/>' +
      '<rect x="520" y="340" width="520" height="300" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<rect x="1100" y="360" width="280" height="80" rx="8" fill="' + C.navy + '" stroke="' + ink + '" stroke-width="4"/>' +
      at(780, 490, 0.55, hydrogen({ r: 50, mood: "flat", mark: "C" }));
    var banner = card(540, 690, 840, 100, C.war) + label(960, 756, 40, "EVERYTHING WENT WRONG", C.cream);
    return field(500) + box +
      g(id + "-banner", banner, 960, 740) +
      g(id + "-sheet", card(1120, 470, 280, 200, C.cream) + at(1260, 560, 0.4, hydrogen({ r: 40, mark: "C" })), 1260, 560) +
      g(id + "-copy2", card(1500, 700, 240, 160, C.cream), 1620, 780) +
      g(id + "-fade", card(200, 700, 220, 150, C.cream), 310, 770);
  }
  function includingYou(id) {
    var ink = C.line;
    var lines = "";
    for (var i = 0; i < 8; i++) lines += '<path d="M260,' + (180 + i * 36) + " H" + (1500 - (i % 3) * 180) + '" stroke="' + C.peri + '" stroke-width="4" opacity="0.55"/>';
    var foot = card(160, 620, 1600, 360, C.cream) +
      '<path d="M160,620 L220,580 L300,640 L420,560 L560,650 L760,540 L980,660 L1200,560 L1400,640 L1600,590 L1760,640 L1760,980 H160 Z" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="6"/>' +
      number(960, 860, 92, "1. INCLUDING YOU", C.navy, WHITE);
    return '<rect width="1920" height="1080" fill="' + C.cream + '"/>' + lines +
      g(id + "-foot", foot, 960, 980);
  }
  function anxious(id) {
    var ink = C.line;
    var room = '<rect width="1920" height="1080" fill="#1C2438"/><rect y="700" width="1920" height="380" fill="#6B5438"/>' +
      '<rect x="180" y="80" width="460" height="300" fill="#0B1A33" stroke="' + ink + '" stroke-width="8"/>' +
      '<circle cx="300" cy="160" r="28" fill="' + C.cream + '"/><circle cx="420" cy="220" r="3" fill="' + C.cream + '"/><circle cx="520" cy="140" r="2.4" fill="' + C.cream + '"/><circle cx="360" cy="280" r="2" fill="' + C.cream + '"/>';
    var bed = '<rect x="640" y="560" width="980" height="280" rx="20" fill="' + C.navy + '" stroke="' + ink + '" stroke-width="6"/>' +
      '<rect x="680" y="500" width="280" height="120" rx="16" fill="' + WHITE + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<path d="M640,700 H1620" stroke="' + C.peri + '" stroke-width="10"/>';
    function bubble(x, y, w, h, lines, size) {
      var t = lines.map(function (ln, i) { return label(x, y - h / 2 + 54 + i * (size + 10), size, ln, ink); }).join("");
      return '<path d="M' + (x - w / 2) + "," + (y - h / 2) + " h" + w + " v" + h + " h" + (-w + 80) + ' l-30,50 l10,-50 h-60 z" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="5"/>' + t;
    }
    return room + bed +
      g(id + "-atom", at(980, 520, 1, hydrogen({ r: 64, mood: "sad", orbit: C.peri })), 980, 500) +
      g(id + "-ask", bubble(1280, 250, 820, 200, ["WHY AM I ANXIOUS", "ABOUT A MEETING TOMORROW?"], 36), 1280, 250) +
      g(id + "-ans", bubble(420, 520, 520, 120, ["ANXIETY COPIED BETTER"], 28), 420, 520);
  }
  function meatTaxi(id) {
    var ink = C.line, G = 940, k = 4.2, x = 960;
    var rider = { tone: 2, outfit: "shirt", color: 0, hair: 0, seed: 9, mood: "flat", arms: [[-10, -4], [10, 4]] };
    var crown = G - 100 * k;
    var sign = card(x - 140, crown - 430, 280, 84, C.yellow) + label(x, crown - 372, 44, "MEAT", ink) +
      '<path d="M' + x + "," + (crown - 346) + " V" + (crown - 250) + '" stroke="' + ink + '" stroke-width="8"/>';
    return field(560) + shadow(x, G, 180) +
      stand(rider, x, G, k) +
      g(id + "-flask", at(x, crown - 170, 1.85, flask("smug")), x, crown - 170) +
      g(id + "-sign", sign, x, crown - 380);
  }
  function badReno(id) {
    var ink = C.line;
    var room = '<rect width="1920" height="640" fill="#E6D3A8"/><rect y="640" width="1920" height="440" fill="#8C6239"/>' +
      '<path d="M0,640 H1920" stroke="' + ink + '" stroke-width="5"/>';
    var sofa = '<path d="M380,780 Q380,560 520,560 H1400 Q1540,560 1540,780 V900 H380 Z" fill="' + C.med + '" stroke="' + ink + '" stroke-width="6"/>' +
      '<rect x="460" y="640" width="1000" height="40" fill="' + C.cream + '" opacity="0.35"/>';
    var pipe = '<rect x="900" y="900" width="70" height="40" fill="' + C.peri + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<rect x="912" y="430" width="46" height="510" fill="#9AA3B2" stroke="' + ink + '" stroke-width="5"/>' +
      '<ellipse cx="935" cy="430" rx="40" ry="16" fill="#C5CDD8" stroke="' + ink + '" stroke-width="4"/>';
    return room + sofa + g(id + "-pipe", pipe, 935, 940);
  }
  function lizardBrain(id) {
    var ink = C.line;
    var road = '<rect y="820" width="1920" height="260" fill="#3E4654"/>' + '<path d="M0,940 H1920" stroke="' + C.yellow + '" stroke-width="8" stroke-dasharray="40 28"/>';
    var dash = '<path d="M220,860 L400,430 H1520 L1700,860 Z" fill="' + C.navy + '" stroke="' + ink + '" stroke-width="6"/>' +
      '<path d="M500,490 H1420 L1540,800 H380 Z" fill="#9EC4D4" stroke="' + ink + '" stroke-width="5"/>' +
      '<rect x="860" y="800" width="220" height="70" rx="8" fill="' + C.navy + '" stroke="' + ink + '" stroke-width="4"/>';
    var mirror = card(1120, 250, 520, 250, C.cream) +
      ["BREATHE", "EAT", "FIGHT", "FLEE"].map(function (w, i) {
        return '<rect x="1160" y="' + (278 + i * 52) + '" width="32" height="32" fill="' + WHITE + '" stroke="' + ink + '" stroke-width="3"/>' +
          label(1400, 306 + i * 52, 30, w, ink);
      }).join("");
    var ticks = [0, 1, 2, 3].map(function (i) {
      return g(id + "-t" + i, '<path d="M1166,' + (298 + i * 52) + " l9,11 l20,-22" + '" fill="none" stroke="' + C.med + '" stroke-width="6" stroke-linecap="round"/>');
    }).join("");
    return '<rect width="1920" height="820" fill="' + SKY + '"/>' + road + dash +
      at(860, 640, 2.35, lizard({ pose: "drive", mood: "flat", look: 1 })) +
      mirror + ticks;
  }
  function stillRunning(id) {
    var ink = C.line, G = 900;
    var sleeper = { tone: 1, outfit: "shirt", color: 3, hair: 0, seed: 2, mood: "flat", arms: [[-8, -2], [8, 2]] };
    var bed = '<rect x="1040" y="640" width="760" height="220" rx="18" fill="' + C.navy + '" stroke="' + ink + '" stroke-width="6"/>' +
      '<rect x="1080" y="590" width="200" height="110" rx="12" fill="' + WHITE + '" stroke="' + ink + '" stroke-width="5"/>';
    var heart = '<path d="M520,340 C520,280 430,260 410,330 C390,260 300,280 320,360 L460,510 L600,360 C620,280 520,280 520,340 Z" fill="' + C.war + '" stroke="' + ink + '" stroke-width="6"/>';
    var tag = card(700, 160, 820, 110, C.cream) + label(1110, 230, 34, "WITHOUT YOUR PERMISSION", ink);
    return field(520) + bed + shadow(420, G, 110) +
      at(400, 680, 2.5, lizard({ pose: "stand", mood: "flat" })) +
      at(1280, 760, 2.5, '<g transform="rotate(72)">' + K.person(sleeper) + "</g>") +
      g(id + "-heart", heart, 460, 420) +
      g(id + "-tag", tag, 1110, 210);
  }
  function nursery(id) {
    var ink = C.line;
    var crate = '<rect x="420" y="700" width="1080" height="220" fill="#C4A574" stroke="' + ink + '" stroke-width="6"/>' +
      '<path d="M420,770 H1500 M500,700 V920 M1420,700 V920" stroke="' + ink + '" stroke-width="4" opacity="0.4"/>' +
      label(960, 850, 64, "MISSILES", ink);
    var house = '<path d="M560,720 L960,280 L1360,720 V760 H560 Z" fill="#F3D6DE" stroke="' + ink + '" stroke-width="6"/>' +
      '<rect x="860" y="560" width="180" height="160" fill="' + C.navy + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<rect x="660" y="460" width="140" height="110" fill="#F7E7A8" stroke="' + ink + '" stroke-width="4"/>' +
      '<circle cx="720" cy="520" r="14" fill="' + C.orange + '"/>';
    var sign = card(1180, 160, 620, 110, C.cream) + label(1490, 230, 36, "GENUINE UPGRADE", C.navy);
    return field(860) + crate + g(id + "-house", house, 960, 640) + g(id + "-sign", sign, 1490, 210);
  }
  function committed(id) {
    var ink = C.line;
    var room = '<rect width="1920" height="780" fill="#E6D3A8"/><rect y="780" width="1920" height="300" fill="#8C6239"/>' +
      '<rect x="1180" y="80" width="620" height="460" fill="#87B4C9" stroke="' + ink + '" stroke-width="10"/>';
    var cloud = at(1500, 500, 0.55, K.nuke());
    var button = '<rect x="280" y="520" width="280" height="40" rx="8" fill="' + C.yellow + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<ellipse cx="420" cy="500" rx="90" ry="36" fill="' + C.war + '" stroke="' + ink + '" stroke-width="5"/>' +
      '<path d="M360,500 H480" stroke="' + C.yellow + '" stroke-width="6"/>';
    var walker = { tone: 1, outfit: "suit", seed: 6, look: "left", mood: "sad", arms: [[-20, -70], [30, 80]] };
    var paper = '<rect x="1120" y="660" width="170" height="210" fill="' + WHITE + '" stroke="' + ink + '" stroke-width="5"/>';
    return room + cloud + button +
      g(id + "-who", stand(walker, 980, 900, 3.3) + card(840, 600, 280, 64, C.yellow) + label(980, 644, 28, "THINKING", ink) + paper, 980, 760);
  }
  function nothingAbout(id) {
    var ink = C.line;
    var room = '<rect width="1920" height="700" fill="#E6D3A8"/><rect y="700" width="1920" height="380" fill="#8C6239"/>';
    var board = '<rect x="80" y="80" width="780" height="560" fill="#1C3A32" stroke="' + ink + '" stroke-width="8"/>' +
      '<ellipse cx="470" cy="340" rx="220" ry="80" fill="none" stroke="' + C.cream + '" stroke-width="6" transform="rotate(-18 470 340)"/>' +
      '<circle cx="640" cy="280" r="16" fill="' + C.orange + '"/>';
    var mirror = '<rect x="1280" y="120" width="520" height="700" rx="12" fill="#C9D4DE" stroke="' + ink + '" stroke-width="8"/>';
    var down = { tone: 1, outfit: "shirt", color: 1, hair: 1, seed: 4, mood: "flat", arms: [[-16, -8], [16, 8]] };
    var shrug = { tone: 1, outfit: "shirt", color: 1, hair: 1, seed: 4, mood: "flat", arms: [[-40, -130], [40, 130]] };
    function bones(up) {
      var arms = up ? "M0,-40 L-34,-72 M0,-40 L34,-72" : "M0,-40 L-40,-8 M0,-40 L40,-8";
      return '<circle cy="-78" r="16" fill="#E7E0D0" stroke="' + ink + '" stroke-width="3"/>' +
        '<ellipse cx="-6" cy="-82" rx="3" ry="4" fill="' + ink + '"/><ellipse cx="6" cy="-82" rx="3" ry="4" fill="' + ink + '"/>' +
        '<path d="M0,-62 V10 M-14,-26 H14 M-12,-8 H12" stroke="' + ink + '" stroke-width="4" fill="none"/>' +
        '<path d="' + arms + ' M0,10 L-16,48 L-8,96 M0,10 L16,48 L8,96" fill="none" stroke="' + ink + '" stroke-width="4" stroke-linecap="round"/>';
    }
    return room + board + mirror +
      g(id + "-me", stand(down, 1040, 900, 3.1)) +
      g(id + "-me-up", stand(shrug, 1040, 900, 3.1)) +
      g(id + "-skel", at(1540, 620, 2.15, bones(false))) +
      g(id + "-skel-up", at(1540, 620, 2.15, bones(true)));
  }
  function lookedFunny(id) {
    var ink = C.line;
    var room = '<rect width="1920" height="700" fill="#E6D3A8"/><rect y="700" width="1920" height="380" fill="#8C6239"/>';
    var genius = { tone: 0, outfit: "shirt", color: 2, hair: 1, seed: 8, mood: "flat", glasses: true };
    var watcher = { tone: 3, outfit: "shirt", color: 0, hair: 0, seed: 1, mood: "flat", look: "left" };
    var bucket = '<path d="M-70,-20 L-50,70 H50 L70,-20 Z" fill="' + C.peri + '" stroke="' + ink + '" stroke-width="5"/>' +
      label(0, 36, 22, "CORTISOL", C.cream) + '<path d="M-60,-20 H60" stroke="' + ink + '" stroke-width="6"/>';
    return room +
      stand(genius, 860, 900, 3.6) +
      g(id + "-watch", stand(watcher, 1560, 900, 3.2)) +
      g(id + "-bucket", at(860, 280, 2.2, bucket), 860, 300) +
      g(id + "-splash", '<path d="M790,400 C780,470 800,520 790,400 M860,410 C850,500 870,560 860,410 M930,400 C940,480 920,530 930,400" fill="none" stroke="' + C.peri + '" stroke-width="14" stroke-linecap="round"/>');
  }
  function noLicense(id) {
    var ink = C.line;
    var body = '<path d="M160,640 L280,640 L360,460 H1500 L1620,560 H1800 V780 H160 Z" fill="' + C.peri + '" stroke="' + ink + '" stroke-width="6"/>' +
      '<path d="M400,490 H720 V680 H360 Z" fill="#B7D3DE" stroke="' + ink + '" stroke-width="5"/>' +
      '<path d="M780,500 H1120 V680 H780 Z" fill="#B7D3DE" stroke="' + ink + '" stroke-width="5"/>' +
      '<path d="M1180,520 H1480 V680 H1220 Z" fill="#B7D3DE" stroke="' + ink + '" stroke-width="5"/>' +
      '<circle cx="480" cy="800" r="70" fill="#222" stroke="' + ink + '" stroke-width="6"/><circle cx="480" cy="800" r="28" fill="' + C.slate + '"/>' +
      '<circle cx="1500" cy="800" r="70" fill="#222" stroke="' + ink + '" stroke-width="6"/><circle cx="1500" cy="800" r="28" fill="' + C.slate + '"/>';
    var loved = { tone: 0, outfit: "dress", color: 3, hair: 1, seed: 2, mood: "smile" };
    var mind = { tone: 1, outfit: "shirt", color: 1, hair: 0, seed: 5, mood: "flat" };
    function lic(torn) {
      return '<rect x="-46" y="-28" width="92" height="56" fill="' + C.cream + '" stroke="' + ink + '" stroke-width="3"/>' +
        (torn ? '<path d="M0,-28 L8,0 L-4,28" stroke="' + ink + '" stroke-width="3"/>' : label(0, 6, 16, "OK", C.med));
    }
    function plaque(x, y, w, text, size) {
      return card(x - w / 2, y - 26, w, 46, C.navy) + label(x, y + 6, size, text, C.cream);
    }
    return field(470) + body +
      at(540, 500, 1.4, lizard({ pose: "drive", mood: "flat" })) +
      stand(loved, 960, 690, 1.35) +
      stand(mind, 1320, 700, 1.28) +
      '<g transform="translate(470,590) rotate(-24) scale(1.35)"><circle r="12" fill="none" stroke="' + C.yellow + '" stroke-width="4"/><circle r="4" fill="' + C.yellow + '"/><path d="M12,0 H42 M28,0 V11 M38,0 V8" stroke="' + C.yellow + '" stroke-width="5" stroke-linecap="round"/></g>' +
      plaque(560, 450, 180, "SURVIVE", 22) +
      g(id + "-loved", plaque(960, 455, 160, "LOVED", 22)) +
      g(id + "-under", plaque(1330, 470, 250, "UNDERSTAND", 20)) +
      g(id + "-good", at(680, 620, 1.3, lic(false))) +
      g(id + "-bad1", at(700, 960, 1.7, lic(true), -18)) +
      g(id + "-bad2", at(900, 990, 1.7, lic(true), 14));
  }
  function lineup(id) {
    var ink = C.line;
    var wall = '<rect width="1920" height="1080" fill="#D9C7A2"/>';
    var lines = "";
    for (var i = 0; i < 8; i++) lines += '<path d="M0,' + (160 + i * 110) + ' H1920" stroke="' + ink + '" stroke-width="3" opacity="0.35"/>' +
      label(80, 150 + i * 110, 22, String(8 - i), ink, 'text-anchor="start"');
    var sign = card(1280, 80, 520, 140, C.navy) + label(1540, 170, 64, "NOBODY", C.cream);
    return wall + lines + g(id + "-sign", sign, 1540, 150) +
      g(id + "-atom", at(860, 620, 1.3, hydrogen({ r: 80, mood: "sly", orbit: ink })), 860, 620) +
      g(id + "-match", at(1040, 560, 1.8, matchstick(false)), 1040, 520) +
      g(id + "-flame", at(1040, 500, 1.5, '<path d="M0,28 C-22,0 -8,-40 0,-62 C10,-36 22,0 0,28 Z" fill="' + C.orange + '" stroke="' + ink + '" stroke-width="4"/><path d="M0,12 C-6,-6 0,-24 0,-32 C5,-18 8,-4 0,12 Z" fill="' + C.yellow + '"/>'), 1040, 470);
  }

  window.GS = {
    C: C, SKY: SKY, GROUND: GROUND, WHITE: WHITE, f: f, at: at, stand: stand, shadow: shadow, field: field,
    number: number, label: label, stone: stone, face: face, g: g, chain: chain, play: play,
    hydrogen: hydrogen, lizard: lizard,
    sixOhFour: sixOhFour, hardware: hardware, ownersManual: ownersManual, universe: universe,
    lowExpectations: lowExpectations, calledStars: calledStars, fatality: fatality, namedDirt: namedDirt,
    promiscuous: promiscuous, copyMachine: copyMachine, includingYou: includingYou, anxious: anxious,
    meatTaxi: meatTaxi, badReno: badReno, lizardBrain: lizardBrain, stillRunning: stillRunning,
    nursery: nursery, committed: committed, nothingAbout: nothingAbout, lookedFunny: lookedFunny,
    noLicense: noLicense, lineup: lineup,
  };
})();
