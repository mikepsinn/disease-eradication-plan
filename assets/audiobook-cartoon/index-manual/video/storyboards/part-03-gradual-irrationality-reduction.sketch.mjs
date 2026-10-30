// Sketches for storyboards/part-03-gradual-irrationality-reduction.md (v3, the atomic-age film look): each scene's key
// moment on a 1920 x 1080 frame, drawn with the production art (H.K: kit.js, film.js and the props library).
// Host shots use H.host (the studio set and the real sprites); a plate frame is one framing as the camera sees it.

const f = (n) => (+n).toFixed(1);

// ── Shared drawings (each takes the kit, so it can be used from any frame) ──

// A person standing on feetY at canvas scale k (KIT.person is drawn with its feet at y 100).
function man(H, o, x, feetY, k, extra = "") {
  return H.at(x, feetY - 100 * k, k, H.K.person(o) + extra);
}
// A walking paper bill with its legs hidden (for heaps and held bills).
function bill(K, kind) {
  return K.money(kind, 0).replace('class="legs"', 'class="legs" opacity="0"');
}
// A heap of bills: rows from the bottom up, each row narrower; the nearer (lower) rows are drawn last.
function heap(H, kind, cx, baseY, w, h, k, seed) {
  const r = H.K.rng(seed), rows = Math.max(2, Math.round(h / (34 * k))), out = [];
  for (let j = 0; j < rows; j++) {
    const y = baseY - 16 * k - j * (h / rows), half = (w / 2) * Math.pow(1 - j / rows, 0.7), step = 70 * k;
    let row = "";
    for (let x = -half; x <= half; x += step) row += H.at(cx + x + (r() - 0.5) * 20 * k, y + (r() - 0.5) * 10 * k, k, bill(H.K, kind), (r() - 0.5) * 50);
    out.unshift(row);
  }
  return out.join("");
}
// The nations' orange foam bat: its grip at (0, 0), pointing +x, len long.
function bat(C, len, w = 1) {
  const ink = C.line;
  return `<path d="M0,${-4 * w} L${f(len * 0.28)},${-6 * w} L${f(len)},${-16 * w} Q${f(len + 12 * w)},0 ${f(len)},${16 * w} L${f(len * 0.28)},${6 * w} L0,${4 * w} Z" fill="${C.orange}" stroke="${ink}" stroke-width="${3 * w}" stroke-linejoin="round"/>` +
    `<path d="M${f(len * 0.34)},${-4 * w} L${f(len * 0.94)},${-11 * w}" stroke="#F6C98A" stroke-width="${3 * w}" stroke-linecap="round"/>` +
    `<rect x="${-16 * w}" y="${-5 * w}" width="${18 * w}" height="${10 * w}" fill="${C.navy}" stroke="${ink}" stroke-width="${2.4 * w}"/>`;
}
// A tiny grinning skull with two antennae and ball tips (Wishonia's ancestors), about 28 wide, around (0, 0).
function aSkull(H, x, y, s) {
  const { C } = H, ink = C.line, bone = "#F1EAD6", blue = "#86B9D6";
  return H.at(x, y, s,
    `<path d="M-5,-12 L-10,-25 M5,-12 L10,-25" stroke="${ink}" stroke-width="2.6"/><path d="M-5,-12 L-10,-25 M5,-12 L10,-25" stroke="${blue}" stroke-width="1.2"/>` +
    `<circle cx="-10.5" cy="-27" r="3.4" fill="${blue}" stroke="${ink}" stroke-width="1.6"/><circle cx="10.5" cy="-27" r="3.4" fill="${blue}" stroke="${ink}" stroke-width="1.6"/>` +
    `<path d="M-12,-3 L-9,-12 L0,-15 L9,-12 L12,-3 L10,4 L5,7 L5,13 L-5,13 L-5,7 L-10,4 Z" fill="${bone}" stroke="${ink}" stroke-width="2.2" stroke-linejoin="miter"/>` +
    `<path d="M-8,-5 L-2,-6 L-2.6,0.5 L-7.4,0 Z M8,-5 L2,-6 L2.6,0.5 L7.4,0 Z M-1.5,5 L0,2 L1.5,5 Z" fill="${ink}"/>` +
    `<path d="M-6,9 Q0,12 6,9 M-3,8 V12 M0,8.6 V12.6 M3,8 V12" fill="none" stroke="${ink}" stroke-width="1.3"/>`);
}
// The snail from the title card (copied from the old irrationality-reduction-title.html): about 70 long, drawn round
// the middle of its foot, facing +x. o: { sit (the body squashed, the shell tipped back), wipe (an eye stalk wiping
// the brow), sweat (a drop by the head) }.
function snail(C, pid, o = {}) {
  const ink = C.line;
  const P = (x, y) => x.toFixed(1) + "," + y.toFixed(1);
  const polyD = (pts) => "M" + pts.map((p) => P(p[0], p[1])).join(" L") + " Z";
  const solid = (pts, col, w) => `<path d="${polyD(pts)}" fill="${ink}" stroke="${ink}" stroke-width="${w || 3.2}" stroke-linejoin="miter" stroke-miterlimit="8"/><path d="${polyD(pts)}" fill="${col}"/>`;
  const body = [[-32, 0], [-29, -4], [-9, -7], [13, -8], [20, -12], [23, -21], [28, -26], [35, -26], [39, -20], [38, -11], [41, -3], [39, 0]];
  const shell = [], sp = [];
  for (let i = 0; i < 12; i++) { const a = (i / 12) * Math.PI * 2; shell.push([-5 + 20 * Math.cos(a), -25 + 19 * Math.sin(a)]); }
  for (let i = 0; i <= 26; i++) { const t = i / 26, b = Math.PI * 0.15 + t * Math.PI * 3.7, r = 16 * (1 - t) + 1.8; sp.push([-5 + r * Math.cos(b), -25 + r * 0.95 * Math.sin(b)]); }
  const stalk = (k, x0, y0, x1, y1, rot) => {
    const dx = x1 - x0, dy = y1 - y0, L = Math.sqrt(dx * dx + dy * dy), nx = -dy / L, ny = dx / L;
    const q = [[x0 + nx * 2.4, y0 + ny * 2.4], [x1 + nx * 1.3, y1 + ny * 1.3], [x1 - nx * 1.3, y1 - ny * 1.3], [x0 - nx * 2.4, y0 - ny * 2.4]];
    return `<g id="${pid}-stalk-${k}"${rot ? ` transform="rotate(${rot} ${x0} ${y0})"` : ""}>` + solid(q, C.cream, 2.6) +
      `<circle cx="${x1}" cy="${y1}" r="4.4" fill="${C.cream}" stroke="${ink}" stroke-width="2.2"/><circle cx="${x1 + 1.2}" cy="${y1}" r="1.9" fill="${ink}"/></g>`;
  };
  const dotsId = pid + "-hd";
  return `<defs><pattern id="${dotsId}" width="3.6" height="3.6" patternUnits="userSpaceOnUse"><circle cx="1.8" cy="1.8" r="1" fill="${ink}"/></pattern></defs>` +
    stalk(0, 29, -25, 25, -45, o.sit ? 40 : 0) +
    `<g${o.sit ? ' transform="translate(-32,0) scale(1.08,0.72) translate(32,0)"' : ""}>` + solid(body, C.cream) +
    `<path d="${polyD(body)}" fill="url(#${dotsId})" opacity="0.25"/>` +
    `<path d="M33,-15 L39,-14" fill="none" stroke="${ink}" stroke-width="1.8" stroke-linecap="round"/>` +
    `<path d="M-24,-3 L-14,-4 M2,-5 L10,-5.5" fill="none" stroke="${ink}" stroke-width="1.3" opacity="0.55"/></g>` +
    `<g${o.sit ? ' transform="translate(0,5) rotate(-16 -5 -6)"' : ""}>` + solid(shell, C.yellow) +
    `<path d="M${P(sp[0][0], sp[0][1])}${sp.slice(1).map((p) => " L" + P(p[0], p[1])).join("")}" fill="none" stroke="${ink}" stroke-width="2.4" stroke-linejoin="miter"/>` +
    `<path d="M5,-10 L12,-17 L14,-27" fill="none" stroke="${C.orange}" stroke-width="2.4" stroke-linejoin="miter"/></g>` +
    stalk(1, 34, -24, 40, -44, o.wipe ? 112 : 0) +
    (o.sweat ? `<path d="M50,-36 Q55,-29 52,-25 Q47,-23 47,-29 Q48,-33 50,-36 Z" fill="#FFFFFF" stroke="${ink}" stroke-width="1.6"/>` : "");
}
// The plain tan dog (copied from the old compositions/scenes/part-03/dog-calculus.html, its DOG block): an angular
// 1950s mutt drawn like the humans, standing on y 0 in person units, facing right. o: { pose "sit" | "stand",
// head "side" | "front", mood "eager" | "flat" | "smug" (eyes shut), tilt, chalk, fire, steam, look }.
function makeDog(K, idp) {
  const C = K.C, ink = C.line, f1 = (n) => (+n).toFixed(1);
  const WHITE = "#FFFFFF", FUR = C.tan, FAR = C.rust, CREAM = C.cream, HS = 1.22;
  let uid = 0;
  const Pt = (x, y) => (+x).toFixed(1) + "," + (+y).toFixed(1);
  const polyD = (pts) => "M" + pts.map((p) => Pt(p[0], p[1])).join(" L") + " Z";
  const solid = (list, col, w) => {
    w = w || 4.4;
    return list.map((pts) => `<path d="${polyD(pts)}" fill="${ink}" stroke="${ink}" stroke-width="${w}" stroke-linejoin="miter" stroke-miterlimit="8"/>`).join("") +
      list.map((pts) => `<path d="${polyD(pts)}" fill="${col}"/>`).join("");
  };
  const line = (d, col, w) => `<path d="${d}" fill="none" stroke="${col || ink}" stroke-width="${w || 2}" stroke-linejoin="miter" stroke-linecap="round"/>`;
  function dots(pts, op) {
    const id = "dogdot-" + idp + "-" + ++uid, xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
    const x0 = Math.min(...xs), y0 = Math.min(...ys), x1 = Math.max(...xs), y1 = Math.max(...ys);
    return `<defs><pattern id="${id}d" width="3.6" height="3.6" patternUnits="userSpaceOnUse"><circle cx="1.8" cy="1.8" r="1" fill="${ink}"/></pattern><clipPath id="${id}c"><path d="${polyD(pts)}"/></clipPath></defs>` +
      `<rect x="${f1(x0)}" y="${f1(y0)}" width="${f1(x1 - x0)}" height="${f1(y1 - y0)}" fill="url(#${id}d)" opacity="${op || 0.26}" clip-path="url(#${id}c)"/>`;
  }
  function seg(x, y, a, len) {
    const r1 = (a[0] * Math.PI) / 180, r2 = (a[1] * Math.PI) / 180, ex = x + len * Math.sin(r1), ey = y + len * Math.cos(r1);
    return { x, y, ex, ey, hx: ex + len * Math.sin(r2), hy: ey + len * Math.cos(r2) };
  }
  function nrm(ax, ay, bx, by) { const dx = bx - ax, dy = by - ay, l = Math.sqrt(dx * dx + dy * dy) || 1; return [-dy / l, dx / l]; }
  function leg(s, w0, w1, w2) {
    const nA = nrm(s.x, s.y, s.ex, s.ey), nB = nrm(s.ex, s.ey, s.hx, s.hy), sx = nA[0] + nB[0], sy = nA[1] + nB[1], qq = sx * sx + sy * sy;
    const side = (k) => {
      const mid = qq > 0.6 ? [[s.ex + (k * sx * w1) / qq, s.ey + (k * sy * w1) / qq]] : [[s.ex + (k * nA[0] * w1) / 2, s.ey + (k * nA[1] * w1) / 2], [s.ex + (k * nB[0] * w1) / 2, s.ey + (k * nB[1] * w1) / 2]];
      return [[s.x + (k * nA[0] * w0) / 2, s.y + (k * nA[1] * w0) / 2]].concat(mid, [[s.hx + (k * nB[0] * w2) / 2, s.hy + (k * nB[1] * w2) / 2]]);
    };
    return side(1).concat(side(-1).reverse());
  }
  const paw = (x, y) => [[x - 4, y - 4], [x + 5, y - 5], [x + 8, y + 1], [x + 4, y + 6], [x - 3, y + 4]];
  const POSE = {
    sit: { head: [27, -84], neck: [18, -68], tail: [-40, -6], collar: [[12, -74], [31, -69], [31, -61], [12, -66]], tag: [24, -57] },
    stand: { head: [15, -121], neck: [6, -104], tail: [-19, -48], hip: [-6, -50], collar: [[-8, -104], [15, -102], [15, -94], [-8, -96]], tag: [8, -90] },
  };
  const TIPS = { side: [[-7, -38], [10, -33]], front: [[-20, -38], [20, -38]] };
  function eye(x, y, o, fur) {
    const mood = o.mood || "eager", rx = 4.8, ry = 3.6, lk = o.look || [0, 0];
    if (mood === "smug") return `<g class="eye">${line("M" + Pt(x - rx, y - 0.5) + " Q" + Pt(x, y + 3) + " " + Pt(x + rx, y - 0.5), ink, 2.2)}</g>`;
    const al = "M" + Pt(x - rx, y) + " Q" + Pt(x, y - ry * 1.6) + " " + Pt(x + rx, y - 0.3) + " Q" + Pt(x, y + ry * 1.15) + " " + Pt(x - rx, y) + " Z";
    let out = `<path d="${al}" fill="${WHITE}" stroke="${ink}" stroke-width="1.2"/><circle class="pupil" cx="${f1(x + lk[0])}" cy="${f1(y - 0.5 + lk[1])}" r="${mood === "eager" ? 1.6 : 1.9}" fill="${ink}"/>`;
    if (mood === "flat") out += `<path d="M${Pt(x - rx - 0.7, y - 0.6)} Q${Pt(x, y - ry * 1.95)} ${Pt(x + rx + 0.7, y - 1)} Z" fill="${fur}"/>` + line("M" + Pt(x - rx - 0.7, y - 0.6) + " L" + Pt(x + rx + 0.7, y - 1), ink, 2.2);
    else out += line("M" + Pt(x - rx - 0.7, y + 0.3) + " Q" + Pt(x, y - ry * 1.95) + " " + Pt(x + rx + 0.7, y - 0.6), ink, 1.9);
    return `<g class="eye">${out}</g>`;
  }
  const flamesAt = (tips) => `<g class="dog-fire">${tips.map((t) => K.flames(f1(t[0]), f1(t[1] + 6), 0.34)).join("")}</g>`;
  const steamAt = (tips) => tips.map((t) => [0, 1, 2].map((i) => `<circle cx="${f1(t[0] + (i - 1) * 5)}" cy="${f1(t[1] - 8 - i * 7)}" r="${6 - i}" fill="${CREAM}" stroke="${ink}" stroke-width="1.6"/>`).join("")).join("");
  const ear = (pts, inner, col) => solid([pts], col) + (inner ? solid([inner], FAR, 1.6) : "");
  function headSide(o) {
    const skull = [[2, -15], [-9, -15], [-16, -6], [-17, 6], [-11, 14], [2, 15], [18, 15], [33, 13], [34, 1], [30, -5], [12, -10]];
    const jaw = [[33, 6], [18, 6], [4, 3], [-4, 12], [2, 15], [18, 15], [33, 13]];
    return ear([[3, -14], [10, -33], [13, -10]], null, FAR) +
      solid([skull], FUR) + dots([[18, -9], [34, 1], [33, 6], [18, 6], [8, 13]], 0.22) + solid([jaw], CREAM, 3.2) + dots(jaw, 0.22) +
      solid([[[38, -3], [30, -6], [27, 0], [31, 5], [38, 3]]], ink, 1.6) + line("M33,9 L17,10 L13,8", ink, 1.8) +
      eye(8, -4, o, FUR) + line("M2,-10.5 L14,-11.5", ink, 2.2) +
      ear([[-14, -10], [-7, -38], [1, -14]], [[-10, -12], [-7, -30], [-3, -14]], FUR) +
      (o.steam ? steamAt(TIPS.side) : "") + (o.fire ? flamesAt(TIPS.side) : "");
  }
  function headFront(o) {
    const L = [[-17, -9], [-20, -38], [-6, -16]], Li = [[-15, -12], [-17, -31], [-9, -16]];
    const flip = (pts) => pts.map((p) => [-p[0], p[1]]);
    const skull = [[-16, -12], [-7, -17], [7, -17], [16, -12], [18, 2], [12, 15], [-12, 15], [-18, 2]];
    const muzzle = [[-11, 0], [11, 0], [13, 9], [7, 17], [-7, 17], [-13, 9]];
    const chalk = o.chalk ? solid([[[3, 10.5], [22, 12], [22, 15.5], [3, 14]]], WHITE, 1.8) : "";
    return ear(L, Li, FUR) + ear(flip(L), flip(Li), FUR) +
      solid([skull], FUR) + dots([[4, -17], [16, -12], [18, 2], [12, 15], [4, 15]], 0.22) + solid([muzzle], CREAM, 3.2) + dots(muzzle, 0.2) +
      solid([[[-6, -1], [6, -1], [4, 5], [-4, 5]]], ink, 1.6) + line("M0,5 V9 M-7,10 Q-3.5,14 0,9 Q3.5,14 7,10", ink, 1.8) +
      eye(-7.5, -5, o, FUR) + eye(7.5, -5, o, FUR) + line("M-13,-11.5 L-3,-10.5 M3,-10.5 L13,-11.5", ink, 2.2) + chalk +
      (o.steam ? steamAt(TIPS.front) : "") + (o.fire ? flamesAt(TIPS.front) : "");
  }
  function headAt(o, pose) {
    const h = POSE[pose].head, t = o.tilt || 0;
    return `<g transform="translate(${Pt(h[0], h[1])}) rotate(${t}) scale(${HS})">${o.head === "front" ? headFront(o) : headSide(o)}</g>`;
  }
  const collar = (pose) => solid([POSE[pose].collar], C.navy, 3) + `<circle cx="${POSE[pose].tag[0]}" cy="${POSE[pose].tag[1]}" r="4" fill="${C.yellow}" stroke="${ink}" stroke-width="2"/>`;
  return function draw(o = {}) {
    const pose = o.pose || "sit";
    let out;
    if (pose === "stand") {
      const farArm = seg(6, -92, [50, 150], 13), nearArm = seg(10, -90, [58, 160], 14);
      const torso = [[12, -48], [-18, -52], [-20, -80], [-14, -102], [2, -110], [14, -100], [16, -72]];
      const chest = [[14, -100], [6, -108], [0, -100], [2, -76], [10, -62], [16, -72]];
      out = solid([[[-14, 0], [8, 0], [8, -4], [-10, -5]]], FAR, 3.6) + solid([[[-18, -50], [-34, -60], [-37, -53], [-21, -44]]], FUR) +
        solid([[[-16, -56], [4, -54], [10, -40], [6, -26], [-2, -14], [2, -6], [22, -5], [22, 0], [-8, 0], [-12, -10], [-10, -20], [-18, -30], [-22, -44]]], FUR) +
        line("M-2,-14 L4,-30 L-4,-46", ink, 1.8) + solid([leg(farArm, 9, 8, 7), paw(farArm.hx, farArm.hy)], FAR, 3.6) +
        solid([torso], FUR) + dots([[-4, -104], [2, -110], [14, -100], [16, -72], [12, -48], [-4, -50]], 0.22) + solid([chest], CREAM, 3.2) + dots(chest, 0.24) +
        solid([[[-16, -62], [-19, -82], [-12, -96], [-6, -78]]], FAR, 2.4) + collar(pose) + headAt(o, pose) + solid([leg(nearArm, 10, 9, 8), paw(nearArm.hx, nearArm.hy)], FUR, 3.6);
    } else {
      const body = [[28, -58], [22, -72], [8, -76], [-6, -64], [-24, -48], [-38, -30], [-44, -14], [-40, -2], [-24, 0], [2, -2], [14, -20], [26, -34]];
      const chest = [[28, -56], [20, -66], [12, -60], [14, -40], [22, -34], [27, -42]];
      const farLeg = [[8, -40], [17, -40], [16, -5], [20, 0], [4, 0], [6, -5]], nearLeg = [[16, -42], [26, -42], [26, -6], [30, 0], [12, 0], [15, -6]];
      const saddle = [[-2, -64], [-18, -54], [-26, -44], [-12, -44], [2, -56]];
      out = solid([farLeg], FAR, 3.6) + solid([[[-38, -6], [-54, -20], [-58, -14], [-44, 0]]], FUR) +
        solid([body], FUR) + dots([[8, -76], [22, -72], [28, -58], [26, -34], [14, -20], [2, -2], [-6, -30]], 0.2) +
        line("M-6,-2 L-12,-28 L-30,-38", ink, 1.8) + solid([[[-8, 0], [12, 0], [12, -5], [-2, -8], [-8, -4]]], FUR, 3.6) +
        solid([saddle], FAR, 2.4) + solid([chest], CREAM, 3.2) + dots(chest, 0.24) + collar(pose) + headAt(o, pose) + solid([nearLeg], FUR, 3.6);
    }
    return `<g class="plain-dog">${out}</g>`;
  };
}
// Burn a drawing (KIT.burn, with pure white kept, so eyes stay white).
function burn(K, markup) {
  const ink = K.C.line.toUpperCase();
  return markup.replace(/(fill|stroke)="(#[0-9A-Fa-f]{6})"/g, (m, a, col) => {
    const u = col.toUpperCase();
    if (u === ink || u === "#FFFFFF") return m;
    const n = parseInt(col.slice(1), 16), l = (0.3 * (n >> 16) + 0.59 * ((n >> 8) & 255) + 0.11 * (n & 255)) / 255, v = Math.round(28 + l * 46);
    return `${a}="rgb(${v + 8},${v},${Math.max(0, v - 6)})"`;
  });
}
// Closed, sleeping eyes on a person (the two .eye groups become lid curves).
function sleepy(markup, ink) {
  const xs = [-2.5, 10.8];
  let i = 0;
  return markup.replace(/<g class="eye">[\s\S]*?<\/g>/g, () => {
    const x = xs[i++ % 2];
    return `<path d="M${x - 5},-4 Q${x},-0.5 ${x + 5},-4" fill="none" stroke="${ink}" stroke-width="2"/>`;
  });
}
// Squeezed-shut wailing eyes (><).
function squeezed(markup, ink) {
  const xs = [-2.5, 10.8];
  let i = 0;
  return markup.replace(/<g class="eye">[\s\S]*?<\/g>/g, () => {
    const x = xs[i++ % 2];
    return `<path d="M${x - 5},-7 L${x + 4},-4 L${x - 5},-1" fill="none" stroke="${ink}" stroke-width="2.2" stroke-linejoin="miter"/>`;
  });
}
// The open old manual (the theme song's book, aged: faded to tan, a cobweb, a chewed corner), standing on (0, 0),
// its cover swung open to the left so the yellowed pages show. In the prop's units (98 wide closed).
function oldBookOpen(C) {
  const ink = C.line, tan = "#B99A70", page = "#E6DABC";
  let lines = "";
  for (let y = -104; y < -14; y += 9) lines += `<path d="M-34,${y} H${y > -40 ? 18 : 30}" stroke="#9C8A68" stroke-width="2"/>`;
  return `<path d="M-42,0 L-108,-10 L-108,-128 L-42,-118 Z" fill="${tan}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
    `<path d="M-48,-8 L-102,-16 M-48,-112 L-102,-121" stroke="#8E7652" stroke-width="2"/>` +
    `<path d="M-42,0 L40,0 L40,-102 Q34,-104 33,-110 Q40,-112 40,-118 L-42,-118 Z" fill="${page}" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` + lines +
    // the chewed corner (top right), a cobweb across the bottom left, dust specks
    `<path d="M-42,-30 L-20,0 M-42,-18 L-32,0 M-42,-30 Q-34,-16 -20,0 M-42,-12 Q-36,-6 -32,0" fill="none" stroke="#FFFFFF" stroke-width="1.6" opacity="0.85"/>` +
    [[-20, -60], [6, -84], [22, -40], [-30, -96], [12, -20]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="2.2" fill="#8E7652"/>`).join("");
}
// The aged manual, closed: the prop recolored dusty, with a cobweb over its top corner.
function oldBookShut(K) {
  const C = K.C;
  return K.props.manual().replace(new RegExp(C.orange, "gi"), "#B99A70").replace(/#FBF6E6/gi, "#E6DABC") +
    `<path d="M40,-118 L14,-118 M40,-118 L40,-92 M40,-118 L20,-98 M28,-118 Q32,-108 40,-104 M18,-118 Q26,-102 40,-96" fill="none" stroke="#FFFFFF" stroke-width="1.6" opacity="0.9"/>`;
}
// The small grinning missile the Weapons Maker cradles (the cast's prop drawn bigger), pointing +x, around (0, 0).
function babyMissile(C) {
  const ink = C.line;
  return `<path d="M-34,-7 L14,-7 L30,0 L14,7 L-34,7 Z" fill="${C.war}" stroke="${ink}" stroke-width="2.6" stroke-linejoin="round"/>` +
    `<path d="M-34,-7 L-44,-17 L-40,-7 Z M-34,7 L-44,17 L-40,7 Z" fill="${C.war}" stroke="${ink}" stroke-width="2.4" stroke-linejoin="round"/>` +
    `<path d="M14,-7 L30,0 L14,7 Z" fill="${C.cream}" stroke="${ink}" stroke-width="2"/>` +
    `<path d="M-4,2 Q2,6 8,2" fill="none" stroke="${ink}" stroke-width="1.8" stroke-linecap="round"/><circle cx="-2" cy="-2.5" r="1.6" fill="${ink}"/><circle cx="6" cy="-2.5" r="1.6" fill="${ink}"/>`;
}
// A red paint chip with the war seal's little cream missile (or a teal pea with the cross), around (0, 0), ~24 wide.
function chip(C, rot = 0) {
  return `<g transform="rotate(${rot})"><path d="M-12,-7 L6,-10 L13,-2 L9,8 L-8,9 L-13,1 Z" fill="${C.war}" stroke="${C.line}" stroke-width="2.4" stroke-linejoin="miter"/>` +
    `<path d="M-5,3 L4,-4 l2,2 Z" fill="${C.cream}" stroke="${C.cream}" stroke-width="2.4" stroke-linejoin="round"/></g>`;
}
function pea(C) {
  return `<circle r="9" fill="${C.med}" stroke="${C.line}" stroke-width="2.4"/><path d="M0,-5 V5 M-5,0 H5" stroke="${C.cream}" stroke-width="2.4" stroke-linecap="round"/>`;
}

const SKY = "#E9DEC2", SEA = "#8FA2A6", SEA2 = "#A9B9B6", SAND = "#D9C08B", FIELD = "#C8B07B";

export default {
  "title-card"(H, fid) {
    const { K, C } = H;
    const cx = 960, cy = 258, rx = 190, ry = 59;
    const orbits = [0, 60, -60].map((a) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.cream}" stroke-width="5" transform="rotate(${a} ${cx} ${cy})"/>`).join("");
    const bills = [[0, 0.9], [60, 3.2], [-60, 5.0]].map(([a, th], i) => {
      const r = (a * Math.PI) / 180, ex = rx * Math.cos(th), ey = ry * Math.sin(th);
      const x = cx + ex * Math.cos(r) - ey * Math.sin(r), y = cy + ex * Math.sin(r) + ey * Math.cos(r);
      return H.at(x, y - 6, 0.6, K.money("war", i % 2));
    }).join("");
    const nucleus = `<circle cx="${cx}" cy="${cy}" r="30" fill="${C.orange}" stroke="${C.cream}" stroke-width="5"/><circle cx="${cx - 9}" cy="${cy - 9}" r="8" fill="${C.yellow}"/>`;
    // the progress bar under the heading (its fill a 1% sliver), the readout, and the snail sitting at its left end
    const x0 = 600, x1 = 1320, by = 822, bh = 44, inner = x1 - x0 - 12;
    const ch = (a, b, c, d, k) => `M${a + k},${b} H${c - k} L${c},${b + k} V${d - k} L${c - k},${d} H${a + k} L${a},${d - k} V${b + k} Z`;
    let ticks = "";
    for (let k = 1; k < 10; k++) { const x = x0 + 6 + (inner * k) / 10; ticks += `<path d="M${f(x)},${by + 9} V${by + bh - 9}" stroke="${C.slate}" stroke-width="3"/>`; }
    const bar = `<path d="${ch(x0, by, x1, by + bh, 8)}" fill="${C.deep}" stroke="${C.ink}" stroke-width="10" stroke-linejoin="miter"/>` +
      `<path d="${ch(x0, by, x1, by + bh, 8)}" fill="none" stroke="${C.cream}" stroke-width="4" stroke-linejoin="miter"/>` + ticks +
      `<rect x="${x0 + 6}" y="${by + 6}" width="${f(inner * 0.01)}" height="${bh - 12}" fill="${C.cyan}"/>` +
      `<text x="${x1 + 22}" y="${by + bh / 2 + 20}" font-family="Oswald" font-weight="600" font-size="56" fill="${C.cream}" stroke="${C.ink}" stroke-width="7" stroke-linejoin="miter" paint-order="stroke">1%</text>`;
    const s = 1.8, snl = H.at(x0 - 8 - 41 * s, by + bh, s, snail(C, fid + "-sn", { sit: true, wipe: true }));
    const svg = `<rect width="1920" height="1080" fill="${C.navy}"/>` + orbits + bills + nucleus +
      H.big(960, 528, 56, "THE GRADUAL", "middle", C.cream) + H.big(960, 648, 112, "IRRATIONALITY", "middle", C.cream) +
      H.big(960, 768, 112, "REDUCTION PROGRAM", "middle", C.cream) + bar + snl;
    return { svg, alt: "The period title card: the atom emblem with three war papers on its orbits, THE GRADUAL IRRATIONALITY REDUCTION PROGRAM in cream on navy, and under it a long progress bar at 1% with a snail sitting at its left end, wiping its brow with an eye stalk." };
  },

  "host-opens"(H, fid) {
    const { K, C } = H, ink = C.line;
    // the old book on the right end of the lectern top, open; its fold-out hangs down past the lectern and heaps
    // up on the free wall to the right
    const book = H.at(1004, 790, 1.35, oldBookOpen(C));
    let hang = "";
    for (let i = 0; i < 5; i++) {
      const y = 786 + i * 62, a = i % 2 ? 10 : 0, b = i % 2 ? 0 : 10;
      hang += `<path d="M${1046 + a},${y} H${1102 + a} L${1102 + b},${y + 62} H${1046 + b} Z" fill="${C.war}" stroke="${ink}" stroke-width="3.6" stroke-linejoin="miter"/>` +
        aSkull(H, 1079, y + 40, 1.15);
    }
    // the heap: the strip folded back and forth in bands, a loop at each turn joining one band to the next
    let pile = "";
    const layers = 9, band = 30, step = 34;
    for (let j = 0; j < layers; j++) {
      const y = 1086 - (j + 1) * step, l = 1124 + ((j * 13) % 29), r = 1500 - ((j * 17) % 37);
      pile += `<path d="M${l},${y} H${r} V${y + band} H${l} Z" fill="${C.war}" stroke="${ink}" stroke-width="3.6"/>`;
      for (let x = l + 42; x < r - 24; x += 74) pile += aSkull(H, x, y + 20, 0.95);
    }
    for (let j = 0; j < layers - 1; j++) {
      const y = 1086 - (j + 1) * step, right = j % 2 === 0, x = right ? Math.min(1500 - ((j * 17) % 37), 1500 - (((j + 1) * 17) % 37)) : Math.max(1124 + ((j * 13) % 29), 1124 + (((j + 1) * 13) % 29));
      const d = right ? 1 : -1;
      pile += `<path d="M${x},${y + band} C${x + d * 46},${y + band} ${x + d * 46},${y - step} ${x},${y - step} L${x},${y - step + band} C${x + d * 22},${y - step + band} ${x + d * 22},${y} ${x},${y} Z" fill="${C.rust}" stroke="${ink}" stroke-width="3.4" stroke-linejoin="round"/>`;
    }
    const front = pile + hang + book;
    return { svg: H.host("skeptical-closed", "shrug", front), alt: "Wishonia at her lectern shrugging; on the lectern her dusty old open manual, its red fold-out strip of panels, each with a tiny grinning antenna skull, hanging down beside the lectern and heaped in folds to lectern height on the right." };
  },

  "nations-foam-bats"(H, fid) {
    const { K, C } = H, ink = C.line;
    let waves = "";
    for (let i = 0; i < 26; i++) { const x = (i * 263) % 1880 + 20, y = 360 + ((i * 97) % 640); waves += `<path d="M${x},${y} q14,-8 28,0 q14,8 28,0" fill="none" stroke="${SEA2}" stroke-width="4" stroke-linecap="round"/>`; }
    const island = (x0, x1, top) => {
      const m = (x0 + x1) / 2;
      return `<path d="M${x0 - 60},840 L${x0},${top + 30} L${x0 + 60},${top} H${x1 - 60} L${x1},${top + 30} L${x1 + 60},840 Z" fill="${SAND}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
        `<path d="M${x0 + 10},${top + 26} L${x0 + 62},${top + 6} H${x1 - 62} L${x1 - 10},${top + 26} Z" fill="#9CA46B" stroke="${ink}" stroke-width="3" stroke-linejoin="miter"/>` +
        `<path d="M${x0 - 40},840 Q${m},826 ${x1 + 40},840" fill="none" stroke="${SEA2}" stroke-width="6"/>`;
    };
    // a crater where each capitol stood: the burnt, flattened dome and rubble, smoking
    const crater = (x, y) => H.at(x, y, 1, `<g transform="scale(0.62,0.2)">${burn(K, K.props.capitol())}</g>`) +
      `<ellipse cx="${x}" cy="${y - 4}" rx="150" ry="16" fill="#3B3229" stroke="${ink}" stroke-width="3"/>` +
      [0, 1, 2].map((i) => `<path d="M${x - 50 + i * 50},${y - 20} q-12,-22 0,-44 q12,-22 0,-44" fill="none" stroke="#8C8782" stroke-width="6" stroke-linecap="round" opacity="0.8"/>`).join("");
    const cal = K.props.calendar({ month: "YEAR", day: "10,000" }).replace(/font-size="32"/g, 'font-size="30" textLength="66" lengthAdjust="spacingAndGlyphs"');
    // the two politician skeletons, a long white beard and a wide tie each, pointing at each other
    const skel = (x, look, tie, arms, batArm) => {
      const o = K.castOpts("politician", { skeleton: true, look, arms, tieColor: tie });
      const R = K.rig(o), T = R.shoulder[0][1] - 4, hs = R.hs, jaw = R.hy + 15 * hs, d = look === "left" ? -1 : 1;
      const tieSvg = `<path d="M-3,${T} L3,${T} L12,${T + 34} L0,${T + 44} L-12,${T + 34} Z" fill="${tie}" stroke="${ink}" stroke-width="2.4" stroke-linejoin="miter"/>`;
      // the beard hangs from the jaw, a narrow gray-white wedge down to the shoes, in front of the tie's tip
      const bx = d * 2, low = 96, beard = `<path d="M${bx - 6},${jaw} L${bx + 6},${jaw} L${bx + 5},${jaw + 24} L${bx + 7},${jaw + 40} L${bx + 3},${(jaw + low) / 2 + 10} L${bx + 5},${low - 18} L${bx + 1},${low} L${bx - 2},${low - 22} L${bx - 5},${(jaw + low) / 2} L${bx - 3},${jaw + 30} L${bx - 7},${jaw + 14} Z" fill="#E4E1D8" stroke="${ink}" stroke-width="1.8" stroke-linejoin="miter"/>` +
        `<path d="M${bx - 1},${jaw + 6} L${bx},${jaw + 40} M${bx + 2},${jaw + 10} L${bx + 3},${jaw + 52}" stroke="#A9A496" stroke-width="1.2"/>`;
      const h = R.hand[batArm], b = `<g transform="translate(${f(h[0])},${f(h[1])}) rotate(${batArm ? 72 : 108})">${bat(C, 92, 0.8)}</g>`;
      return man(H, o, x, 712, 2.1, tieSvg + beard + b);
    };
    const svg = `<rect width="1920" height="1080" fill="${SEA}"/><rect width="1920" height="330" fill="${SKY}"/><path d="M0,330 H1920" stroke="${ink}" stroke-width="3"/>` + waves +
      island(170, 790, 690) + island(1130, 1750, 690) + crater(360, 698) + crater(1560, 698) +
      `<rect x="954" y="610" width="14" height="250" fill="#7A5634" stroke="${ink}" stroke-width="3"/>` + H.at(961, 620, 1.9, cal) +
      skel(600, "right", C.war, [[-8, -4], [88, 94]], 0) + skel(1320, "left", C.peri, [[-88, -94], [8, 4]], 1);
    return { svg, alt: "Two grinning politician skeletons with long white beards and wide ties, one red and one blue, stand on two cratered, smoking islands and point bony fingers at each other across the strait; a tear-off calendar on a post in the water reads YEAR 10,000." };
  },

  "toddlers-take-nap"(H, fid) {
    const { K, C } = H, ink = C.line;
    // far: the islands, small, up and right across the water, the skeletons bonking under a mushroom cloud
    const isl = (x0, x1, top) => `<path d="M${x0 - 30},560 L${x0},${top + 14} L${x0 + 30},${top} H${x1 - 30} L${x1},${top + 14} L${x1 + 30},560 Z" fill="${SAND}" stroke="${ink}" stroke-width="3.4" stroke-linejoin="miter"/>`;
    const skel = (x, look, arms, rot) => {
      const o = K.castOpts("politician", { skeleton: true, look, arms });
      const R = K.rig(o), h = R.hand[look === "left" ? 0 : 1];
      return man(H, o, x, 486, 0.95, `<g transform="translate(${f(h[0])},${f(h[1])}) rotate(${rot})">${bat(C, 120, 0.8)}</g>`);
    };
    const far = isl(1080, 1390, 470) + isl(1500, 1820, 470) +
      H.at(1450, 486, 0.5, K.nuke(), 0).replace("<g ", '<g opacity="0.82" ') +
      skel(1300, "right", [[-6, -3], [150, 160]], -10) + skel(1610, "left", [[-150, -160], [6, 3]], 190);
    // near: the cutaway house on the shore, its playroom open to us
    const wallpaper = `<defs><pattern id="${fid}-wp" width="60" height="60" patternUnits="userSpaceOnUse"><rect width="60" height="60" fill="#EFE3C4"/><path d="M30,8 L38,30 L30,52 L22,30 Z" fill="none" stroke="#E3C88F" stroke-width="3"/></pattern></defs>`;
    const house = wallpaper +
      `<path d="M70,404 L575,226 L1080,404 Z" fill="${C.rust}" stroke="${ink}" stroke-width="5" stroke-linejoin="miter"/>` +
      `<path d="M150,388 L575,246 L1000,388" fill="none" stroke="#B5684A" stroke-width="5"/>` +
      `<rect x="120" y="404" width="910" height="458" fill="url(#${fid}-wp)" stroke="${ink}" stroke-width="5"/>` +
      `<rect x="100" y="404" width="26" height="470" fill="${C.tan}" stroke="${ink}" stroke-width="4"/><rect x="1024" y="404" width="26" height="470" fill="${C.tan}" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="90" y="862" width="970" height="36" fill="#A8794E" stroke="${ink}" stroke-width="5"/>` +
      `<rect x="600" y="450" width="200" height="150" fill="${SEA2}" stroke="${ink}" stroke-width="5"/><path d="M700,450 V600 M600,525 H800" stroke="${ink}" stroke-width="4"/>` +
      `<ellipse cx="560" cy="846" rx="410" ry="34" fill="${C.orange}" stroke="${ink}" stroke-width="4"/><ellipse cx="560" cy="846" rx="350" ry="24" fill="none" stroke="${C.cream}" stroke-width="4"/>` +
      [[176, 832, C.war], [208, 832, C.med], [192, 802, C.yellow], [980, 832, C.peri]].map(([x, y, c]) => `<rect x="${x - 15}" y="${y - 15}" width="30" height="30" fill="${c}" stroke="${ink}" stroke-width="3"/>`).join("");
    const kid = (o) => sleepy(K.person(o), ink);
    const tod = (o, x, y, mirror) => {
      const body = H.at(0, 0, 2.2, kid(o), -90);
      return H.at(x, y, 1, mirror ? `<g transform="scale(-1,1)">${body}</g>` : body);
    };
    const A = { tone: 1, outfit: "overalls", color: 1, look: "right", mood: "smile", arms: [[60, 100], [-40, -70]], build: { hs: 1.35, legs: 0.55, th: 0.62, tw: 0.8, neck: 0.2 } };
    const B = { tone: 2, outfit: "dress", hair: 1, color: 3, look: "right", mood: "smile", arms: [[60, 100], [-40, -70]], build: { hs: 1.35, legs: 0.55, th: 0.62, tw: 0.8, neck: 0.2 } };
    // the winged pillow under the right one's head, the bats on the rug, the Z's
    const pillow = (x, y) => `<path d="M${x - 64},${y + 10} q-24,-30 6,-34 q-6,18 18,20 Z M${x + 64},${y + 10} q24,-30 -6,-34 q6,18 -18,20 Z" fill="#FFFFFF" stroke="${ink}" stroke-width="3"/>` +
      `<rect x="${x - 58}" y="${y - 20}" width="116" height="46" rx="20" fill="#FFFFFF" stroke="${ink}" stroke-width="4"/>`;
    const zs = (x, y) => [[0, 0, 44], [30, -50, 34], [54, -92, 26]].map(([dx, dy, s]) => H.label(x + dx, y + dy, s, "Z", "middle", C.navy)).join("");
    const kids = tod(A, 300, 812, false) + pillow(886, 830) + tod(B, 820, 808, true) +
      H.at(392, 868, 1, `<g transform="rotate(-4)">${bat(C, 150, 1.2)}</g>`) + H.at(728, 868, 1, `<g transform="rotate(184)">${bat(C, 150, 1.2)}</g>`) + zs(240, 720) + zs(900, 714);
    const svg = `<rect width="1920" height="1080" fill="${SEA}"/><rect width="1920" height="300" fill="${SKY}"/><path d="M0,300 H1920" stroke="${ink}" stroke-width="3"/>` +
      far + `<path d="M0,690 Q600,650 1300,700 T1920,690 V1080 H0 Z" fill="${SAND}" stroke="${ink}" stroke-width="4"/>` + house + kids;
    return { svg, alt: "Wide view: in a cutaway house on the near shore two toddlers sleep on the playroom rug, foam bats in hand, one on a pillow with little wings, Z's rising; across the water behind them, on two small islands, two politician skeletons still bonk each other with foam bats under a mushroom cloud." };
  },

  "dog-calculus"(H, fid) {
    const { K, C } = H, ink = C.line, CH = "#EFE8D2";
    const integral = (x, y, k) => `<path d="M${f(x + 18 * k)},${f(y - 40 * k)} C${f(x + 18 * k)},${f(y - 50 * k)} ${f(x + 8 * k)},${f(y - 50 * k)} ${f(x + 8 * k)},${f(y - 38 * k)} L${f(x)},${f(y + 8 * k)} C${f(x)},${f(y + 18 * k)} ${f(x - 10 * k)},${f(y + 18 * k)} ${f(x - 10 * k)},${f(y + 10 * k)}" fill="none" stroke="${CH}" stroke-width="${f(3.6 * k)}" stroke-linecap="round"/>`;
    const chalk = (x, y, s, t) => `<text x="${x}" y="${y}" font-family="Inter" font-weight="500" font-style="italic" font-size="${s}" fill="${CH}" opacity="0.92">${H.esc(t)}</text>`;
    const rows = [
      [120, 180, "x² dx = x³/3 + C", 640, "d/dx (sin x) = cos x", 1160, "e^iπ + 1 = 0"],
      [120, 280, "(x² + 1)⁻¹ dx = arctan x", 760, "Σ 1/n² = π²/6", 1150, "lim (1 + 1/n)ⁿ"],
      [120, 380, "f′(x) = lim [f(x+h) − f(x)]/h", 900, "∂²u/∂t² = c² ∇²u", 0, ""],
      [120, 480, "e^(−x²) dx = √π", 660, "dy/dx = ky  ⇒  y = Ce^(kx)", 0, ""],
      [120, 580, "sec³θ dθ = ½(secθ tanθ + ln|secθ + tanθ|)", 0, "", 0, ""],
      [120, 680, "x e^x dx = (x − 1)e^x + C", 700, "∮ F · dr = 0", 0, ""],
    ];
    let board = `<rect x="56" y="64" width="1500" height="700" fill="${C.tan}" stroke="${ink}" stroke-width="6"/><rect x="82" y="90" width="1448" height="648" fill="${C.slate}" stroke="${ink}" stroke-width="4"/>` +
      `<rect x="40" y="760" width="1532" height="22" fill="#8C6440" stroke="${ink}" stroke-width="4"/><rect x="300" y="748" width="40" height="12" fill="${CH}" stroke="${ink}" stroke-width="2"/>`;
    rows.forEach(([x, y, a, x2, b, x3, c]) => {
      board += integral(x, y - 14, 1.3) + chalk(x + 30, y, 40, a);
      if (b) board += (x2 % 2 ? "" : integral(x2 - 10, y - 14, 1.1)) + chalk(x2 + 16, y, 38, b);
      if (c) board += chalk(x3, y, 38, c);
    });
    // chalk dust in the air by the dog's mouth
    board += [[1010, 470], [1030, 500], [995, 520], [1050, 455]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="4" fill="${CH}" opacity="0.8"/>`).join("");
    const floor = `<rect y="860" width="1920" height="220" fill="#B48A5E"/><path d="M0,860 H1920" stroke="${ink}" stroke-width="5"/>` +
      [0, 1, 2, 3].map((i) => `<path d="M0,${900 + i * 46} H1920" stroke="#8C6440" stroke-width="3"/>`).join("");
    const dog = makeDog(K, fid)({ pose: "stand", head: "front", chalk: true, fire: true, mood: "eager" });
    const sci = K.castOpts("scientist", { look: "left", mood: "eager", arms: [[-150, -118], [10, 30]], holdL: "flask", holdR: null });
    const R = K.rig(sci), hp = R.hand[1];
    const pointer = `<path d="M${f(hp[0])},${f(hp[1])} L${f(hp[0] + 50)},${f(hp[1] + 40)}" stroke="#7A5634" stroke-width="4" stroke-linecap="round"/>`;
    const svg = `<rect width="1920" height="1080" fill="#E6D8B6"/>` + board + floor +
      H.at(1090, 862, 3.1, dog) + man(H, sci, 1440, 862, 3.0, pointer) +
      // bubbles rising from the raised flask
      [[0, 0, 9], [14, -26, 7], [-6, -50, 6]].map(([dx, dy, r]) => `<circle cx="${f(1440 + 3.0 * R.hand[0][0] + dx)}" cy="${f(862 - 300 + 3.0 * R.hand[0][1] - 90 + dy)}" r="${r}" fill="${C.med}" stroke="${ink}" stroke-width="2.4"/>`).join("");
    return { svg, alt: "A tan dog stands on its hind legs at a chalkboard crammed with chalk integrals, a stick of chalk in its mouth, its ears on fire, staring at the camera; beside it the Scientist in her lab coat raises her bubbling flask over its head." };
  },

  "host-manual"(H, fid) {
    const { K, C } = H, ink = C.line;
    const old = H.at(612, 790, 1.1, oldBookShut(K));
    // the new manual, its cover swung open to the left (its plain inside showing), a medicine bill boinging up out
    // of its pages on a spring
    let spring = "M0,-60";
    for (let i = 1; i <= 9; i++) spring += ` L${i % 2 ? 12 : -12},${-60 - i * 12}`;
    const m = K.props.manual(), cut = m.indexOf('<g class="manual-cover">');
    const inside = `<path d="M-42,0 L-108,-10 L-108,-128 L-42,-118 Z" fill="#C97A30" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>` +
      `<path d="M-48,-8 L-102,-16 V-120 L-48,-112" fill="none" stroke="${C.cream}" stroke-width="1.4" opacity="0.6"/>`;
    let lines = "";
    for (let y = -104; y < -14; y += 10) lines += `<path d="M-34,${y} H30" stroke="#B9B3A3" stroke-width="2"/>`;
    const fresh = m.slice(0, cut) + inside + lines + "</g>";
    const neu = H.at(968, 790, 1.2, fresh + `<path d="${spring}" fill="none" stroke="${C.slate}" stroke-width="3.6" stroke-linejoin="round"/>` +
      H.at(10, -180, 1, `<g transform="rotate(12) scale(0.9)">${bill(K, "med")}</g>`) +
      `<path d="M-48,-206 q-12,22 0,44 M70,-206 q12,22 0,44" fill="none" stroke="${ink}" stroke-width="3" stroke-linecap="round"/>`);
    const sparkle = (x, y, r) => `<path d="M${x},${y - r} L${x + r * 0.25},${y - r * 0.25} L${x + r},${y} L${x + r * 0.25},${y + r * 0.25} L${x},${y + r} L${x - r * 0.25},${y + r * 0.25} L${x - r},${y} L${x - r * 0.25},${y - r * 0.25} Z" fill="${C.cream}" stroke="${ink}" stroke-width="2"/>`;
    const snl = H.at(528, 793, 1.7, `<g transform="rotate(-6)">${snail(C, fid + "-sn")}</g>`);
    const front = old + neu + sparkle(1040, 700, 16) + sparkle(1060, 650, 10) + snl;
    return { svg: H.host("lookright-smile", "idle", front), alt: "Wishonia at her lectern looks down at the snail creeping onto the left end of the lectern top; beside her dusty old manual stands the new orange one, open, a green medicine bill boinging up out of its pages on a spring." };
  },

  "year-one-to-twenty"(H, fid) {
    const { K, C } = H, ink = C.line;
    // the factory (left, mostly out of frame) on pill bottles now: a conveyor of pill bottles, teal smoke
    const fac = H.at(120, 620, 1.15, K.props.factory({ label: "", smoke: false }));
    const conv = H.at(470, 620, 1.1, K.props.conveyor({ w: 300 }) + [-110, -40, 30, 100].map((x) => H.at(x, -66, 0.55, K.props.pillBottle({ face: "smile" }))).join(""));
    const teal = [[40, 160], [140, 120], [230, 175]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="34" fill="#9FD0C8" stroke="${ink}" stroke-width="3"/><circle cx="${x + 28}" cy="${y - 26}" r="24" fill="#9FD0C8" stroke="${ink}" stroke-width="3"/>`).join("");
    const strays = [[330, 860, 12], [400, 872, -18]].map(([x, y, r]) => H.at(x, y, 0.75, bill(K, "war"), r)).join("");
    // the funnel and the calendar on its post
    const funnel = H.at(800, 860, 1.5, K.props.colorFlipFunnel({ inN: 0, outN: 0 }));
    const cal = `<rect x="535" y="560" width="12" height="300" fill="#7A5634" stroke="${ink}" stroke-width="3"/>` + H.at(541, 570, 1.7, K.props.calendar({ month: "YEAR", day: 20 }));
    // the hospital (right) and its hill of medicine money
    const hosp = H.at(1720, 640, 1.05, K.props.hospital({ label: "" }));
    const hill = heap(H, "med", 1730, 790, 460, 190, 0.85, 31);
    const walkers = [[1010, 846], [1130, 852]].map(([x, y]) => H.at(x, y, 0.8, K.money("med", 1)));
    // the old Weapons Maker, stooped, in a lab coat, holding up the framed photo of his old missile
    const wm = K.castOpts("weaponsMaker", { kind: "lab", look: "right", mood: "smile", stache: true, cigar: false, arms: [[70, 120], [84, 112]], build: { hs: 0.7, tw: 1.1, arms: 1.35, legs: 0.78, neck: 0, hand: 1.35, hunch: 14 } });
    const RW = K.rig(wm), top = [(RW.hand[0][0] + RW.hand[1][0]) / 2 + 14, Math.min(RW.hand[0][1], RW.hand[1][1]) + 30];
    const photo = `<g transform="translate(${f(top[0])},${f(top[1] - 44)})"><rect x="-46" y="-34" width="92" height="64" fill="${C.yellow}" stroke="${ink}" stroke-width="3"/><rect x="-36" y="-25" width="72" height="46" fill="${C.cream}" stroke="${ink}" stroke-width="2"/>` +
      `<g transform="scale(0.95)">${babyMissile(C)}</g></g>`;
    // the grown man, his eyes out on springs and his jaw on the ground
    const guy = { tone: 1, outfit: "shirt", color: 0, hair: 0, look: "left", mood: "eager", arms: [[-20, -10], [20, 10]], build: { hs: 1, legs: 1.05, th: 1.05, tw: 1 } };
    const RG = K.rig(guy), ey = RG.eyes, mo = RG.mouth;
    const springs = [0, 1].map((i) => {
      const y0 = ey[1] - 2 + i * 2, x0 = ey[0] - i * 6, x1 = x0 - 58 - i * 10, y1 = y0 - 20 + i * 26;
      let d = `M${x0},${y0}`;
      for (let k = 1; k <= 8; k++) { const u = k / 8; d += ` L${f(x0 + (x1 - x0) * u)},${f(y0 + (y1 - y0) * u + (k % 2 ? -5 : 5))}`; }
      return `<path d="${d}" fill="none" stroke="${C.slate}" stroke-width="2.2"/><circle cx="${x1}" cy="${y1}" r="11" fill="#FFFFFF" stroke="${ink}" stroke-width="2.2"/><circle cx="${x1 - 4}" cy="${y1}" r="4.4" fill="${ink}"/>`;
    }).join("");
    const jaw = `<path d="M${f(mo[0] - 12)},${f(mo[1] - 2)} L${f(mo[0] + 10)},${f(mo[1] - 2)} L${f(mo[0] + 14)},96 L${f(mo[0] - 18)},96 Z" fill="#D9B48F" stroke="${ink}" stroke-width="2.6" stroke-linejoin="miter"/>` +
      `<path d="M${f(mo[0] - 8)},${f(mo[1] + 2)} L${f(mo[0] + 6)},${f(mo[1] + 2)} L${f(mo[0] + 8)},88 L${f(mo[0] - 12)},88 Z" fill="#3A1E1A"/><path d="M${f(mo[0] - 10)},88 Q${f(mo[0] - 2)},78 ${f(mo[0] + 6)},88 Z" fill="#D9707A"/>`;
    const svg = `<rect width="1920" height="1080" fill="${FIELD}"/><g transform="translate(960,540) scale(1.28) translate(-1160,-575)">` + teal + fac + conv + strays + hosp + hill + cal + funnel + walkers.join("") +
      man(H, wm, 1060, 862, 2.3, photo) + man(H, guy, 1440, 862, 2.3, jaw + springs) + "</g>";
    return { svg, alt: "Year 20: the calendar on its post by the color-flip funnel reads YEAR 20; the factory at the left runs pill bottles under teal smoke; a hill of medicine money stands by the hospital; the old, stooped Weapons Maker in a lab coat holds up a framed photo of his smiling missile, and the grown man facing him has his eyes out on springs and his jaw on the ground." };
  },

  "paint-chips"(H, fid) {
    const { K, C } = H, ink = C.line;
    // the wall painted war red, bitten bare in patches; a cracked window; a checkered floor
    const bites = [[600, 330, 70], [760, 250, 52], [990, 330, 64], [520, 520, 48], [1070, 520, 40], [680, 440, 36]].map(([x, y, r]) => {
      // a patch of bare plaster whose edge is a ring of little bites
      const n = 11, pts = [];
      for (let i = 0; i < n; i++) { const a = (i / n) * Math.PI * 2 + 0.3, rr = r * (0.82 + (0.18 * ((i * 7) % 3)) / 2); pts.push([x + rr * Math.cos(a), y + rr * 0.85 * Math.sin(a)]); }
      let d = `M${f(pts[0][0])},${f(pts[0][1])}`;
      for (let i = 1; i <= n; i++) { const q = pts[i % n]; d += ` A${f(r * 0.3)},${f(r * 0.3)} 0 0,0 ${f(q[0])},${f(q[1])}`; }
      return `<path d="${d} Z" fill="#E8DABA" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>`;
    }).join("");
    let floor = "";
    for (let r = 0; r < 5; r++) for (let c = 0; c < 24; c++) floor += `<rect x="${c * 80}" y="${770 + r * 66}" width="80" height="66" fill="${(c + r) % 2 ? C.cream : C.navy}"/>`;
    const win = `<rect x="1360" y="120" width="320" height="300" fill="${C.cream}" stroke="${ink}" stroke-width="6"/><rect x="1384" y="144" width="272" height="252" fill="#BCCFD0" stroke="${ink}" stroke-width="4"/>` +
      `<path d="M1520,144 V396 M1384,270 H1656" stroke="${ink}" stroke-width="5"/><path d="M1560,190 L1590,230 L1572,250 L1612,300 L1600,330" fill="none" stroke="${ink}" stroke-width="3"/><path d="M1590,230 L1630,214 M1572,250 L1546,276" fill="none" stroke="${ink}" stroke-width="2.4"/>`;
    // the high chair, the baby wailing, the tear jets, the mother with the bowl held high, the dog underneath
    const chair = `<path d="M790,600 L740,900 M930,600 L980,900 M800,600 L820,900 M920,600 L900,900" stroke="#8C6440" stroke-width="12" stroke-linecap="round"/><path d="M770,760 H950" stroke="#8C6440" stroke-width="10"/>` +
      `<rect x="770" y="420" width="180" height="190" rx="10" fill="#B48A5E" stroke="${ink}" stroke-width="5"/>`;
    const baby = { tone: 0, outfit: "shirt", color: 3, hair: 2, look: "right", mood: "sad", arms: [[30, 60], [-30, -60]], build: { hs: 1.6, legs: 0.5, th: 0.6, tw: 0.9, neck: 0.1, nose: 0.35, chin: 0.8 } };
    const RB = K.rig(baby), bk = 2.5, bx = 860, by = 612 - (RB.hipY - 0) * bk;
    const mo = RB.mouth;
    const wail = `<path d="M${f(mo[0] - 10)},${f(mo[1] - 7)} L${f(mo[0] + 14)},${f(mo[1] - 9)} L${f(mo[0] + 12)},${f(mo[1] + 16)} Q${f(mo[0] + 2)},${f(mo[1] + 22)} ${f(mo[0] - 8)},${f(mo[1] + 15)} Z" fill="#3A1E1A" stroke="${ink}" stroke-width="2"/>` +
      `<path d="M${f(mo[0] - 6)},${f(mo[1] + 12)} Q${f(mo[0] + 2)},${f(mo[1] + 6)} ${f(mo[0] + 10)},${f(mo[1] + 12)} L${f(mo[0] + 8)},${f(mo[1] + 16)} Q${f(mo[0] + 2)},${f(mo[1] + 20)} ${f(mo[0] - 6)},${f(mo[1] + 14)} Z" fill="#D9707A"/>` +
      // a single curl on top of the bald head
      `<path d="M${f(RB.top[0] - 2)},${f(RB.top[1] + 4)} q-2,-12 8,-12 q8,1 5,8 q-3,5 -7,1" fill="none" stroke="${ink}" stroke-width="2.4" stroke-linecap="round"/>`;
    const bib = `<path d="M-14,${f(RB.shoulder[0][1] - 2)} H14 L12,${f(RB.shoulder[0][1] + 20)} Q0,${f(RB.shoulder[0][1] + 30)} -12,${f(RB.shoulder[0][1] + 20)} Z" fill="#FFFFFF" stroke="${ink}" stroke-width="2"/>`;
    const babySvg = H.at(bx, by, bk, squeezed(K.person(baby), ink) + bib + wail);
    const eyeY = by + bk * RB.eyes[1], eyeX = bx + bk * RB.eyes[0];
    // a tear jet from (x0, y0) to (x1, y1), widening like a fire hose's spray
    const jet = (x0, y0, x1, y1) => {
      const mx = (x0 + x1) / 2, my = Math.min(y0, y1) - 34;
      return `<path d="M${f(x0)},${f(y0 - 8)} Q${f(mx)},${f(my - 10)} ${f(x1)},${f(y1 - 28)} L${f(x1)},${f(y1 + 28)} Q${f(mx)},${f(my + 30)} ${f(x0)},${f(y0 + 8)} Z" fill="#CFE6EE" stroke="${ink}" stroke-width="3.4" stroke-linejoin="round"/>` +
        `<path d="M${f(x0 + (x1 - x0) * 0.12)},${f(y0 - 6)} Q${f(mx)},${f(my)} ${f(x1 - (x1 - x0) * 0.06)},${f(y1 - 14)}" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>`;
    };
    const splat = (x, y) => `<path d="M${x},${y - 60} l14,32 l34,-22 l-12,36 l40,6 l-38,18 l26,30 l-38,-10 l-6,40 l-20,-34 l-30,26 l6,-38 l-40,-4 l36,-20 l-26,-30 l36,8 Z" fill="#CFE6EE" stroke="${ink}" stroke-width="3"/>`;
    const tray = `<rect x="730" y="604" width="260" height="22" rx="6" fill="#C79A66" stroke="${ink}" stroke-width="4"/>`;
    const mom = { tone: 0, outfit: "dress", hair: 1, color: 2, look: "left", mood: "worried", arms: [[-62, -28], [168, 182]], build: { hs: 0.95, legs: 1.02 } };
    const RM = K.rig(mom), hm = RM.hand[1], MK = 2.45, MX = 1290, MF = 902;
    const faceX = MX + MK * RM.eyes[0], faceY = MF - 100 * MK + MK * RM.eyes[1];
    const jets = jet(eyeX - 26, eyeY - 4, 380, eyeY - 4) + splat(350, eyeY - 4) + jet(eyeX + 26, eyeY - 4, faceX - 6, faceY + 6) +
      `<path d="M${f(faceX + 20)},${f(faceY - 40)} l70,-14 M${f(faceX + 26)},${f(faceY - 10)} l80,-4 M${f(faceX + 20)},${f(faceY + 20)} l70,8" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.9"/>`;
    const bowl = `<g transform="translate(${f(hm[0])},${f(hm[1] - 8)})"><path d="M-26,-4 H26 Q24,16 0,18 Q-24,16 -26,-4 Z" fill="${C.cream}" stroke="${ink}" stroke-width="2.4"/>` +
      [[-14, -8, 10], [0, -11, -20], [14, -8, 30]].map(([x, y, r]) => `<g transform="translate(${x},${y}) scale(0.5)">${chip(C, r)}</g>`).join("") + "</g>";
    const dog = H.at(870, 902, 2.0, makeDog(K, fid)({ pose: "sit", head: "front", mood: "flat" }));
    const flaps = `<path d="M818,666 q-24,-16 -40,-4 M922,666 q24,-16 40,-4" fill="none" stroke="${ink}" stroke-width="3" stroke-linecap="round"/>`;
    const svg = `<rect width="1920" height="1080" fill="${C.war}"/>` + bites + floor + `<path d="M0,770 H1920" stroke="${ink}" stroke-width="5"/>` + win +
      chair + dog + flaps + babySvg + tray + H.at(800, 598, 1, chip(C, 20)) +
      man(H, mom, MX, MF, MK, bowl) + jets;
    return { svg, alt: "A 1950s kitchen with a red wall bitten bare in patches: the baby in the high chair wails, two jets of tears shooting out sideways like fire hoses, one splatting the wall and one blowing back the mother, who holds the bowl of red paint chips high out of reach; the tan dog sits under the high chair." };
  },

  "host-closes"(H, fid) {
    const { K, C } = H, ink = C.line;
    // the dog sits on the free wall beside the lectern facing her, nose up, eyes shut; the chip it brought in on its nose tumbles away
    const dog = makeDog(K, fid)({ pose: "sit", head: "side", mood: "smug", tilt: -28 });
    const dogG = H.at(1330, 1068, 3.2, `<g transform="scale(-1,1)">${dog}</g>`);
    const flick = `<g transform="translate(1196,560) scale(2.2)">${chip(C, -35)}</g>` +
      `<path d="M1118,680 q12,-50 48,-84 M1140,694 q18,-44 52,-70" fill="none" stroke="${ink}" stroke-width="3" stroke-linecap="round" opacity="0.7"/>` +
      `<circle cx="1078" cy="722" r="13" fill="${C.cream}" stroke="${ink}" stroke-width="2.4"/><circle cx="1050" cy="704" r="9" fill="${C.cream}" stroke="${ink}" stroke-width="2.4"/>`;
    return { svg: H.host("sideeye-closed", "idle", dogG + flick), alt: "Wishonia at her lectern side-eyes the camera; beside the lectern the tan dog sits facing her with its nose in the air and its eyes shut, a snort puffing from its nose, the red paint chip it flicked off tumbling away above it." };
  },
};
