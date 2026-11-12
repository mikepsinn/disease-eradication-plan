// Part 27's busy-field plate, shared by its four field scenes. One wide strip of aged paper on the ground line G:
// YOU's desk at the far left, YOU, open ground (the star row, later the allocation bar), the bomb's pile, the lab, the
// friend on her lawn, the edge where the robot goes off, Grandma on her headstone at the far right.
// A scene that continues another "(no seam)" replays that scene's beats at negative times (P27.shift), so it starts on
// exactly its final frame: glowing-rectangle-share -> really-good-review, wishocratic-slider -> personally-to-blame.
(function () {
  var K = window.KIT, V = K.V, SZ = K.collage.SIZES, G = 1000;
  var X = { desk: 40, you: 380, star: 650, bomb: 720, rail: 1400, lab: 2260, friend: 3300, bush: 3570, edge: 4150, stone: 5000 };
  var hk = function (art, h) { return h / SZ[art][1]; };
  var cy = function (s) { return V ? G - 420 / s : G - 360 / s; };
  var views = V ? {
    you: [X.you + 20, cy(1.3), 1.3], stars: [X.you + 640, cy(0.85), 0.85], friend: [X.friend + 110, cy(1.2), 1.2],
    run: [2300, cy(0.5), 0.5], edge: [X.edge, cy(0.8), 0.8], grandma: [X.stone + 60, cy(0.95), 0.95],
    phone: [X.you, G - 330, 17], wide: [1430, G - 250 / 0.45, 0.45], bar: [1600, G - 250 / 0.53, 0.53], blame: [1850, G - 330 / 0.8, 0.8],
  } : {
    you: [X.you + 40, cy(1.3), 1.3], stars: [X.you + 560, cy(0.95), 0.95], friend: [X.friend + 60, cy(1.3), 1.3],
    run: [2300, cy(0.55), 0.55], edge: [X.edge, cy(0.9), 0.9], grandma: [X.stone + 80, cy(1), 1],
    phone: [X.you, G - 330, 24], wide: [1350, cy(0.62), 0.62], bar: [1560, cy(0.88), 0.88], blame: [1580, cy(0.95), 0.95],
  };
  // YOU on his bone legs (Part 26), as two pieces on the same feet: above the waist (which chars) and the bones.
  var YK = hk("you-bone-legs", 600), WAIST = 368;
  var youPart = function (top, extra) {
    var o = { art: "you-bone-legs", x: X.you, y: G, anchor: "bottom", pivot: "bottom", scale: YK,
      clip: top ? [[0, 0], [242, 0], [242, WAIST], [0, WAIST]] : [[0, WAIST - 2], [242, WAIST - 2], [242, 652], [0, 652]] };
    if (top) { o.points = { hold: [121, 300], fire0: [40, 330], fire1: [200, 320], fire2: [121, 150], watch: [-150, 250] }; o.eyes = [[103, 83], [141, 83]]; o.eyeSize = 17; o.smoke = [[95, 20], [150, 24]]; }
    for (var k in extra || {}) o[k] = extra[k];
    return o;
  };
  // The glowing rectangle (a slate with two TV knobs) in its three sizes, by width: tray, phone, matchbox.
  var phone = function (w, label, hidden) {
    var o = { art: "glowing-rectangle", x: X.you, y: G - 330, scale: w / SZ["glowing-rectangle"][0], hidden: hidden };
    if (label) o.label = { text: label, at: [124, 116], width: 180, size: w > 200 ? 44 : w > 100 ? 28 : 6 };
    return o;
  };
  // The bar the allocation is made on: the rail, its knob at the far right (604 to 1, a sliver for trials).
  var RK = 2.4, RW = SZ["slider-rail"][0] * RK, R0 = X.rail - RW / 2, TRACK = [R0 + 25 * RK, R0 + 458 * RK];
  var KNOB0 = TRACK[1] - (TRACK[1] - TRACK[0]) / 605, KNOB1 = 1260, KNOBY = G - (148 - 48) * RK;

  window.P27 = {
    G: G, X: X, V: V, views: views, hk: hk, YK: YK, KNOB0: KNOB0, KNOB1: KNOB1, KNOBY: KNOBY, TRACK: TRACK,
    // The times of another scene's words, moved by `by` seconds (negative: before this scene starts).
    shift: function (src, by) { return function (w, n) { return K.cue(src, w, n) + by; }; },

    // Scene 2's cast and beats: YOU buried in calendar pages at his desk, SHARE, the bolt to the friend, who chops
    // the missile, stomps the germ and sips. c(word, n) gives the scene-2 word's time in the caller's scene.
    share: function (cast, add, c) {
      var DESKK = 1.6, DESKTOP = G - (350 - 100) * DESKK;
      cast.desk = { art: "desk", x: X.desk, y: G, anchor: "bottom", scale: DESKK };
      cast.cal = { art: "calendar", x: X.desk + 120, y: DESKTOP + 4, anchor: "bottom", pivot: "bottom", scale: 1.1 };
      cast.chair = { art: "deckchair", x: X.friend + 150, y: G, anchor: "bottom", pivot: "bottom", scale: hk("deckchair", 330) };
      cast.bush = { art: "sprinkler", x: X.bush + 60, y: G + 6, anchor: "bottom", pivot: "bottom", scale: hk("sprinkler", 190) };
      var FK = hk("citizen-7", 560);
      cast.friend = { art: "citizen-7", x: X.friend, y: G, anchor: "bottom", pivot: "bottom", scale: FK, points: { mouth: [94, 50] } };
      cast.fSit = { art: "citizen-7", x: X.friend + 150, y: G - (372 - 236) * hk("deckchair", 330), anchor: [101, 190], pivot: [101, 294], scale: FK, hidden: true,
        clip: [[0, 0], [203, 0], [203, 190], [0, 190]] };
      cast.fphone = { art: "glowing-rectangle", x: X.friend - 72, y: G - 250, scale: 84 / SZ["glowing-rectangle"][0] };
      cast.cup = { art: "lemonade", x: X.friend + 74, y: G - 300, scale: hk("lemonade", 96), pivot: "center" };
      cast.yB = youPart(false);
      cast.yT = youPart(true);
      // The calendar's pages, heaped on YOU four, three, two, one (the rectangle pops up in front of them).
      var PK = hk("calendar-page", 215), PAGES = [], pr = 0, pc = 0;
      for (var i = 0; i < 10; i++) {
        var rl = 4 - pr, px = X.you + (pc - (rl - 1) / 2) * 112 + [6, -9, 12, -5, 8, -12, 4, -7, 10, -3][i], py = G - pr * 90;
        cast["pg" + i] = { art: "calendar-page", x: px, y: py, anchor: "bottom", pivot: "bottom", scale: PK, hidden: true };
        PAGES.push("pg" + i);
        if (++pc >= rl) { pc = 0; pr++; }
      }
      P27.PAGES = PAGES;
      cast.phone1 = phone(260, "SHARE", true);
      cast.germ = { art: "germ", x: X.friend - 175, y: G, anchor: "bottom", pivot: "bottom", scale: hk("germ", 170), hidden: true };
      cast.missile = { art: "missile-fly", x: X.friend - 150, y: G - 430, scale: hk("missile-fly", 150), cut: "lr", hidden: true };

      // YOU skids in to his desk; the calendar tears its own pages off, faster and faster, and buries him to the chin.
      add({ at: c("please") + 0.02, do: "slideIn", who: ["yT", "yB"], from: "left", dist: 760, over: 34, tilt: 6 });
      add({ at: c("press"), do: "shiver", who: "cal", dur: c("share") - c("press"), amp: 3, rot: 3 });
      PAGES.forEach(function (n, i) {
        var t = c("press") + (c("share") - 0.08 - c("press")) * Math.pow(i / 9, 0.6);
        add({ at: t, do: "slideIn", who: n, from: "top", dist: 1300, over: 10, tilt: [9, -12, 6, -8, 14, -6, 10, -14, 7, -9][i] });
      });
      // The glowing rectangle, tray-sized, pops up out of the pile in both hands; it glows on "glowing".
      add({ at: c("share"), do: "pop", who: "phone1", squash: true });
      add({ at: c("share"), do: "move", who: "phone1", to: "yT.hold", dur: 0.01 });
      add({ at: c("glowing"), do: "glow", who: "phone1", size: 330, dur: 0.6 });
      // SHARE: a bolt from his rectangle to hers, and the camera chases it across the field.
      add({ at: c("case"), do: "nudge", who: "phone1", by: [0, 14] });
      var BOLT = [], bx0 = X.you + 60, bx1 = X.friend - 90, by0 = G - 380, by1 = G - 250;
      for (var j = 0; j <= 14; j++) BOLT.push([bx0 + (bx1 - bx0) * j / 14, by0 + (by1 - by0) * j / 14 + (j % 2 ? -70 : 70) * (j && j < 14 ? 1 : 0)]);
      add({ at: c("case"), do: "line", id: "bolt", points: BOLT, dur: c("afternoon") - c("case"), color: "#F2C230", width: 22, ease: "linear", front: true });
      add({ at: c("afternoon") + 0.3, do: "hide", who: "bolt" });
      add({ at: c("case") + 0.05, do: "camera", view: "friend", dur: c("friends") - c("case") + 0.25 });
      add({ at: c("afternoon"), do: "hop", who: "fphone", height: 30 });
      add({ at: c("afternoon"), do: "glow", who: "fphone", size: 200, dur: 0.5 });
      // "war": a missile flies in; she karate-chops it in half, teacup level, and the halves drop.
      add({ at: c("end") - 0.05, do: "slideIn", who: "missile", from: "left", dist: 1100, over: 14 });
      add({ at: c("war") + 0.18, do: "nudge", who: "friend", by: [-60, -12] });
      add({ at: c("war") + 0.22, do: "split", who: "missile", gap: 170, spin: 40, shake: 10 });
      add({ at: c("war") + 0.5, do: "drop", who: ["missile.L", "missile.R"], dist: 700, spin: 70, dur: 0.5 });
      // "disease": a germ creeps up behind her; she stomps it flat.
      add({ at: c("and") - 0.15, do: "slideIn", who: "germ", from: "left", dist: 700, over: 8 });
      add({ at: c("disease") + 0.05, do: "hop", who: "friend", height: 80 });
      add({ at: c("disease") + 0.05, do: "hop", who: ["fphone", "cup"], height: 80 });
      add({ at: c("instead.") - 0.02, do: "flatten", who: "germ" });
      add({ at: c("instead.") - 0.02, do: "shake", frames: 3, y: 6 });
      // "instead.": she flops back into the deckchair, which folds up on her like a clam; the lemonade comes out of
      // the slats still level, and she sips.
      add({ at: c("instead.") + 0.12, do: "hide", who: ["friend", "fphone"] });
      add({ at: c("instead.") + 0.12, do: "show", who: "fSit" });
      add({ at: c("instead.") + 0.12, do: "move", who: "cup", to: [X.friend + 230, G - 250], dur: 0.12 });
      add({ at: c("instead.") + 0.45, do: "flatten", who: ["chair", "fSit"] });
      add({ at: c("instead.") + 0.45, do: "shake", frames: 2, y: 5 });
      // the lemonade comes up out of the folded chair, still level, and tips for a sip
      add({ at: c("instead.") + 0.5, do: "move", who: "cup", to: [X.friend + 175, G - 200], dur: 0.17 });
      add({ at: c("instead.") + 0.75, do: "move", who: "cup", by: [-10, -10], turn: -38, dur: 0.17 });
      add({ at: c("instead.") + 0.95, do: "move", who: "cup", by: [10, 10], turn: 0, dur: 0.17 });
    },

    // Scene 5's cast and beats: YOU on fire, charred, the stopwatch, the URL, the bar popping out of the matchbox
    // rectangle onto the robot, and YOU dragging the divider while the war bills march to the lab, flipping their seals.
    slider: function (cast, add, c) {
      cast.desk = { art: "desk", x: X.desk, y: G, anchor: "bottom", scale: 1.6 };
      cast.robot = { art: "robot-elbow", x: TRACK[1] + 120, y: G, anchor: "bottom", pivot: "bottom", scale: hk("robot-elbow", 470), hidden: true,
        eyes: [[300, 112], [322, 118]], eyeSize: 20, smoke: [[268, 40]] };
      cast.pileW = { art: "money-hill", x: X.bomb - 10, y: G + 10, anchor: "bottom", scale: hk("money-hill", 200), hidden: true };
      cast.bomb = { art: "bomb", x: X.bomb, y: G - 170, anchor: "bottom", pivot: "bottom", scale: hk("bomb", 300), hidden: true };
      cast.bench = { art: "lab-bench", x: X.lab, y: G, anchor: "bottom", scale: hk("lab-bench", 380), hidden: true };
      cast.sci = { art: "scientist", x: X.lab + 280, y: G, anchor: "bottom", pivot: "bottom", scale: hk("scientist", 540), hidden: true };
      cast.rail = { art: "slider-rail", x: X.rail, y: G, anchor: "bottom", pivot: "bottom", scale: RK, hidden: true };
      cast.knob = { art: "slider-knob", x: KNOB0, y: KNOBY, scale: 1.05, hidden: true };
      cast.watch = { art: "stopwatch", x: X.you - 150, y: G - 600, scale: hk("stopwatch", 250), hidden: true };
      cast.yB = youPart(false);
      cast.yT = youPart(true);
      cast.phone2 = phone(150, "REVIEW", false);
      cast.phone3 = phone(56, "", true);
      cast.phone4 = phone(56, "warondisease.org", true);
      ["f0", "f1", "f2"].forEach(function (n, i) {
        cast[n] = { art: "flames", x: X.you, y: G - 300, anchor: "bottom", pivot: "bottom", scale: hk("flames", [300, 280, 340][i]), hidden: true };
      });
      cast.puff = { art: "cloud-puff", x: X.you, y: G - 330, scale: hk("cloud-puff", 170), hidden: true };

      var D = function (w, n) { return c(w, n); };
      // Running on the spot from the last scene; the rectangle rides in his hands.
      add({ at: -30, do: "move", who: ["phone2", "phone3", "phone4"], to: "yT.hold", dur: 0.01 });
      ["f0", "f1", "f2"].forEach(function (n, i) { add({ at: -30, do: "move", who: n, to: "yT.fire" + i, dur: 0.01 }); });
      add({ at: -30, do: "bob", who: "yT", y: 12, r: 3, speed: 7, until: D("do", 1), fade: 0 });
      add({ at: -30, do: "bob", who: "yB", y: 12, r: 3, speed: 7, until: D("do", 1), fade: 0 });
      // "busy": the rectangle shrinks again, to a matchbox.
      add({ at: D("busy"), do: "swap", who: "phone2", to: "phone3" });
      // "do": his feet smoke and he bursts into flames, and runs in circles holding the matchbox out.
      add({ at: D("do", 1), do: "pop", who: ["f0", "f1", "f2"], squash: true });
      // round and round (as steps, so both pieces of him go together): two laps of an ellipse, back where he started
      var L0 = D("do", 1) + 0.1, L1 = D("least") - 0.1, NS = 16, prev = [0, 0];
      for (var k = 1; k <= NS; k++) {
        var ang = 2 * Math.PI * k / 8, pt = [240 * Math.sin(ang), -60 * (1 - Math.cos(ang))];
        add({ at: L0 + (k - 1) * (L1 - L0) / NS, do: "move", who: ["yT", "yB"], by: [pt[0] - prev[0], pt[1] - prev[1]], dur: (L1 - L0) / NS });
        prev = pt;
      }
      add({ at: D("do", 1) + 0.1, do: "shiver", who: ["f0", "f1", "f2"], dur: D("least") - D("do", 1), amp: 5, rot: 6 });
      // "least": out in a puff, charred above the waist, bones below, blinking.
      add({ at: D("least") - 0.05, do: "hide", who: ["f0", "f1", "f2"] });
      add({ at: D("least") - 0.05, do: "pop", who: "puff", squash: true });
      add({ at: D("least") + 0.45, do: "pop", who: "puff", out: true });
      add({ at: D("least"), do: "char", who: "yT" });
      add({ at: D("least") + 0.7, do: "blink", who: "yT" });
      add({ at: D("least") + 1.6, do: "blink", who: "yT" });
      add({ at: D("least") + 0.2, do: "glow", who: "phone3", size: 90, dur: 0.6 });
      // "15": a stopwatch pops up and counts down to 0 by "trials."
      add({ at: -30, do: "move", who: "watch", to: "yT.watch", dur: 0.01 });
      add({ at: D("15"), do: "pop", who: "watch", squash: true });
      add({ at: D("15") + 0.1, do: "counter", id: "secs", who: "watch", spot: [150, 250], from: 15, to: 0, dur: D("trials.") - D("15") - 0.1,
        size: 72, font: "oswald", card: false, enter: "none", style: "tick" });
      // The camera pushes into the matchbox until it fills the frame; the address on it.
      add({ at: D("go", 1), do: "camera", view: "phone", dur: 0.55 });
      add({ at: D("WarOnDisease.org") + 0.1, do: "hide", who: "phone3" });
      add({ at: D("WarOnDisease.org") + 0.1, do: "show", who: "phone4" });
      // "wishocratic": the bar pops out of it like toast, lands across the field, and its end flattens the robot.
      add({ at: D("make") - 0.1, do: "slideIn", who: "robot", from: "right", dist: 900, over: 6 });
      add({ at: D("make"), do: "char", who: "robot" });
      add({ at: D("make") + 0.1, do: "bob", who: "robot", y: 8, r: 5, speed: 4, until: D("allocation,") });
      add({ at: D("wishocratic") - 0.15, do: "camera", view: "wide", dur: 0.55 });
      add({ at: D("wishocratic"), do: "pop", who: "rail", squash: true });
      add({ at: D("wishocratic"), do: "shake", frames: 3, y: 10 });
      add({ at: D("wishocratic"), do: "pop", who: "knob" });
      add({ at: D("allocation,") - 0.05, do: "flatten", who: "robot" });
      add({ at: D("allocation,") - 0.05, do: "shake", frames: 3, y: 8 });
      // The split as it is today: a bomb on its pile of war money, a lab bench where the Scientist waits; YOU walks to the divider.
      add({ at: D("telling"), do: "pop", who: "pileW", squash: true });
      add({ at: D("telling") + 0.12, do: "stamp", who: "bomb", from: 1.5, shake: 6 });
      add({ at: D("us"), do: "pop", who: ["bench", "sci"], squash: true });
      add({ at: D("what"), do: "camera", view: "bar", dur: 1.3 });
      add({ at: D("what"), do: "move", who: ["yT", "yB"], by: [KNOB0 + 110 - X.you, 0], dur: 1.3, ease: "smooth" });
      add({ at: D("what"), do: "bob", who: "yT", y: 10, r: 2, speed: 7, until: D("what") + 1.3, fade: 0.1 });
      add({ at: D("what"), do: "bob", who: "yB", y: 10, r: 2, speed: 7, until: D("what") + 1.3, fade: 0.1 });
      add({ at: D("resources"), do: "banner", id: "boom", text: "EXPLOSIONS", x: V ? 1060 : 1010, y: V ? G - 900 : G - 640, size: V ? 150 : 110, width: V ? 700 : 520, pad: 44, color: "red", tilt: -3 });
      add({ at: D("clinical"), do: "banner", id: "trials", text: "CLINICAL TRIALS", x: V ? 2180 : 1660, y: V ? G - 720 : G - 640, size: V ? 130 : 90, width: V ? 720 : 600, pad: 40, color: "ink", tilt: 2 });
      // "explosions": his charred hand grabs the divider; "versus": he drags it toward the bomb, walking behind it.
      add({ at: D("explosions"), do: "nudge", who: "yT", by: [-30, 0] });
      add({ at: D("explosions"), do: "shiver", who: "bomb", dur: 0.4, amp: 3, rot: 3 });
      var DRAG0 = D("versus"), DRAG1 = D("trials.") - 0.1;
      add({ at: DRAG0, do: "move", who: "knob", to: [KNOB1, KNOBY], dur: DRAG1 - DRAG0, ease: "smooth" });
      add({ at: DRAG0, do: "move", who: ["yT", "yB"], by: [KNOB1 - KNOB0, 0], dur: DRAG1 - DRAG0, ease: "smooth" });
      // The war bills march out of the bomb, along the bar, and flip to crosses as they pass the divider.
      var MY = G - 148 * RK + 14, SPEED = 1150, N = 6, GAP = 135, M0 = DRAG0 - 0.25;
      add({ at: M0, do: "march", id: "wb", art: "bill-war", count: N, path: [[X.bomb + 40, MY], [TRACK[1] + 30, MY], [X.lab - 140, G - 362]], speed: SPEED, gap: GAP,
        height: 110, end: "stop", bob: 10, steps: 4 });
      add({ at: M0 + (KNOB1 - X.bomb - 40) / SPEED + 0.05, do: "xray", who: "wb", art: "bill-med", stagger: GAP / SPEED, flash: 0, frames: 2 });
      // "trials.": the bomb, empty, sputters, and a little BANG flag pokes out of it.
      add({ at: D("trials.") + 0.05, do: "shiver", who: "bomb", dur: 0.5, amp: 4, rot: 6 });
      add({ at: D("trials.") + 0.25, do: "banner", id: "bang", text: "BANG", x: V ? X.bomb + 60 : X.bomb - 150, y: V ? G - 520 : G - 470, size: 60, width: 200, pad: 26, color: "red", tilt: -14 });
    },
  };
})();
