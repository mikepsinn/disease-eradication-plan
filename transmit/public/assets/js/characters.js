/**
 * Modular character system for animated chat avatars.
 * Robot = CSS-drawn. Wishonia = sprite-based with lip-sync.
 * All characters respond to window.setRobotState('speaking'|'listening'|'idle').
 */
(function () {
  'use strict';

  var characters = [];
  var SPRITE_BASE = '/assets/sprites/alien/';

  // ─── Robot Character (unchanged) ──────────────────────────────────

  var robotCharacter = {
    name: 'robot',
    css: '\
      .robot-char { position: relative; width: 100px; height: 110px; }\
      .robot .head {\
        position: absolute; width: 80px; left: 12px; height: 60px;\
        border-radius: 490px 550px 550px 550px; overflow: hidden;\
        background: #ccc linear-gradient(to right, #b7a9a9 0%, #c1b1b1 40%, #c1b5b5 60%, #ab9c9c 100%);\
        transform-origin: 50% 100%;\
        animation: robot-bob 8000ms ease-in-out alternate infinite -1000ms;\
        border: 2px solid #000;\
      }\
      .robot .eyes {\
        position: absolute; top: calc(50% - 7px); right: 16px; left: 16px; height: 14px;\
        animation: robot-blink 10000ms linear forwards infinite;\
      }\
      .robot .eyeball {\
        position: absolute; width: 14px; height: 14px;\
        background: radial-gradient(ellipse, #dffdfe 0%, #11c1f3 50%, #387ef5 60%) no-repeat center;\
        background-size: 100%; border-radius: 100%; border: 2px solid #000;\
      }\
      .robot .eyeball_left { left: 0; }\
      .robot .eyeball_right { right: 0; }\
      .robot .mouth {\
        position: absolute; bottom: 10px; left: 30px; width: 20px; height: 4px;\
        background-color: #000; overflow: hidden; border-radius: 4px;\
        transition: height 100ms cubic-bezier(0.455,0.03,0.515,0.955);\
      }\
      .robot .mouth-container { position: absolute; inset: 0; }\
      .robot .mouth-container-line {\
        position: absolute; top: 30%; height: 0; background-color: limegreen; width: 100%; margin-top: -1px;\
      }\
      .robot.char_speaking .mouth { height: 12px; }\
      .robot.char_speaking .mouth-container { animation: robot-speakingAnim 0.3s infinite; }\
      .robot.char_speaking .mouth-container-line { height: 3px; }\
      .robot.char_listening .mouth { height: 6px; }\
      .robot.char_listening .mouth-container { animation: robot-listeningAnim 0.5s infinite; }\
      .robot.char_listening .mouth-container-line { height: 2px; }\
      .robot .neck {\
        position: absolute; bottom: 28px; left: calc(50% - 3px); width: 3px; height: 30px;\
        border-radius: 10px; border: 2px solid #000;\
        background: repeating-linear-gradient(180deg, rgba(0,0,0,0.2), rgba(0,0,0,0.2) 7%, #646464 10%), linear-gradient(to right, #ccc 0%, #e6e6e6 40%, #e6e6e6 60%, #ccc 100%);\
      }\
      .robot .torso {\
        position: absolute; bottom: 0; left: calc(50% - 12px); width: 24px; height: 36px;\
        border: 2px solid #000;\
        background: linear-gradient(to right, #b7afaf 0%, #b7b0b0 40%, #afa6a6 60%, #b9b0b0 100%);\
      }\
      .robot .arms { position: absolute; bottom: 0; left: 30px; right: 30px; height: 30px; }\
      .robot .arm {\
        position: absolute; border: 2px solid #000; top: 0; width: 7px; height: 30px;\
        border-radius: 7px 7px 0 0;\
        background: repeating-linear-gradient(180deg, rgba(0,0,0,0.2), rgba(0,0,0,0.2) 7%, #646464 10%), linear-gradient(to right, #ccc 0%, #e6e6e6 40%, #e6e6e6 60%, #ccc 100%);\
      }\
      .robot .arm_left { left: 0; }\
      .robot .arm_right { right: 0; }\
      @keyframes robot-bob {\
        0%  { transform: rotate(-3deg); }\
        40% { transform: rotate(-3deg); animation-timing-function: cubic-bezier(1,0,0,1); }\
        60% { transform: rotate(3deg); }\
        100%{ transform: rotate(3deg); }\
      }\
      @keyframes robot-blink {\
        50% { transform: scale(1,1); }\
        51% { transform: scale(1,0.1); }\
        52% { transform: scale(1,1); }\
      }\
      @keyframes robot-speakingAnim {\
        0%   { filter: url("#robot-speaking-0"); }\
        25%  { filter: url("#robot-speaking-1"); }\
        50%  { filter: url("#robot-speaking-2"); }\
        75%  { filter: url("#robot-speaking-3"); }\
        100% { filter: url("#robot-speaking-4"); }\
      }\
      @keyframes robot-listeningAnim {\
        0%   { filter: url("#robot-listening-0"); }\
        25%  { filter: url("#robot-listening-1"); }\
        50%  { filter: url("#robot-listening-2"); }\
        75%  { filter: url("#robot-listening-3"); }\
        100% { filter: url("#robot-listening-4"); }\
      }\
      @media (max-width: 800px) {\
        .robot-char { width: 70px; height: 55px; }\
        .robot .head { width: 56px; left: 8px; height: 42px; }\
        .robot .eyes { top: calc(50% - 5px); right: 12px; left: 12px; height: 10px; }\
        .robot .eyeball { width: 10px; height: 10px; }\
        .robot .mouth { bottom: 7px; left: 20px; width: 16px; height: 3px; }\
        .robot .neck, .robot .torso, .robot .arms { display: none; }\
      }\
    ',
    svgFilters: '\
      <filter id="robot-speaking-0"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="0"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="12"/></filter>\
      <filter id="robot-speaking-1"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="30"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="13"/></filter>\
      <filter id="robot-speaking-2"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="2"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="12"/></filter>\
      <filter id="robot-speaking-3"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="30"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="13"/></filter>\
      <filter id="robot-speaking-4"><feTurbulence baseFrequency="0.1" numOctaves="3" result="noise" seed="4"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="11"/></filter>\
      <filter id="robot-listening-0"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="0"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="2"/></filter>\
      <filter id="robot-listening-1"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="30"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="3"/></filter>\
      <filter id="robot-listening-2"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="2"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="2"/></filter>\
      <filter id="robot-listening-3"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="30"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="3"/></filter>\
      <filter id="robot-listening-4"><feTurbulence baseFrequency="0.1" numOctaves="3" result="noise" seed="4"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="1"/></filter>\
    ',
    buildDOM: function (wrapper) {
      wrapper.classList.add('robot-char');
      wrapper.innerHTML = '\
        <div class="robot" data-char-el>\
          <div class="neck"></div>\
          <div class="arms"><div class="arm arm_left"></div><div class="arm arm_right"></div></div>\
          <div class="torso"></div>\
          <div class="head">\
            <div class="eyes"><div class="eyeball eyeball_left"></div><div class="eyeball eyeball_right"></div></div>\
            <div class="mouth"><div class="mouth-container"><div class="mouth-container-line"></div></div></div>\
          </div>\
        </div>';
    }
  };

  // ─── Wishonia Lip-Sync Engine ─────────────────────────────────────

  var CHAR_TO_VISEME = {
    'a': 'open', 'e': 'ee', 'i': 'ee', 'o': 'oh', 'u': 'oh',
    'b': 'closed', 'm': 'closed', 'p': 'closed',
    'f': 'closed', 'v': 'closed',
    's': 'ee', 'z': 'ee', 'c': 'ee',
    't': 'small', 'd': 'small', 'n': 'small', 'l': 'small', 'r': 'small',
    'g': 'small', 'k': 'small', 'j': 'small',
    'w': 'oh', 'y': 'ee', 'h': 'small', 'q': 'oh', 'x': 'ee',
    ' ': 'closed', ',': 'closed', '.': 'closed', '!': 'closed', '?': 'closed'
  };

  // Which mouths exist per expression (for fallback)
  var EXPRESSION_MOUTHS = {
    'neutral': ['smile', 'open', 'oh', 'ee', 'closed', 'small', 'frown'],
    'happy':   ['smile', 'open', 'oh', 'ee', 'closed', 'small'],
    'excited': ['open', 'ee', 'oh', 'closed'],
    'sad':     ['closed', 'frown', 'oh', 'small'],
    'annoyed': ['closed', 'frown', 'small'],
    'skeptical': ['smile', 'closed'],
    'surprised': ['open', 'oh', 'ee'],
    'eyeroll': ['closed', 'frown', 'smile'],
    'smirk':   ['smile', 'ee', 'closed'],
    'thinking': ['oh', 'closed', 'small'],
    'sideeye': ['closed'],
    'lookright': ['smile', 'closed', 'open', 'oh'],
    'blink':   ['smile']
  };

  function getHeadName(expression, viseme) {
    var available = EXPRESSION_MOUTHS[expression] || EXPRESSION_MOUTHS['neutral'];
    var mouth = available.indexOf(viseme) >= 0 ? viseme : 'closed';
    if (available.indexOf(mouth) < 0) mouth = available[0];
    return expression + '-' + mouth;
  }

  function getIdleHead(expression) {
    var available = EXPRESSION_MOUTHS[expression] || ['smile'];
    if (available.indexOf('smile') >= 0) return expression + '-smile';
    if (available.indexOf('closed') >= 0) return expression + '-closed';
    return expression + '-' + available[0];
  }

  // ─── Wishonia Animator ────────────────────────────────────────────

  var alienHeadImg = null;
  var alienBodyImg = null;
  var blinkTimer = null;
  var speakTimer = null;
  var currentExpression = 'neutral';
  var isSpeaking = false;

  function setHead(name) {
    if (alienHeadImg) alienHeadImg.src = SPRITE_BASE + name + '.png';
  }

  function setBody(name) {
    if (alienBodyImg) alienBodyImg.src = SPRITE_BASE + 'body-' + name + '.png';
  }

  function startBlinking() {
    stopBlinking();
    blinkTimer = setInterval(function () {
      if (isSpeaking) return;
      setHead('blink-smile');
      setTimeout(function () {
        if (!isSpeaking) setHead(getIdleHead(currentExpression));
      }, 150);
    }, 4000 + Math.random() * 3000);
  }

  function stopBlinking() {
    if (blinkTimer) { clearInterval(blinkTimer); blinkTimer = null; }
  }

  function setIdle() {
    isSpeaking = false;
    if (speakTimer) { clearTimeout(speakTimer); speakTimer = null; }
    setHead(getIdleHead(currentExpression));
    startBlinking();
  }

  // Animate through visemes for a chunk of text
  function animateText(text, expression) {
    isSpeaking = true;
    stopBlinking();
    var chars = text.toLowerCase().split('');
    var idx = 0;

    function nextChar() {
      if (idx >= chars.length || !isSpeaking) return;
      var ch = chars[idx];
      var viseme = CHAR_TO_VISEME[ch] || 'small';
      setHead(getHeadName(expression, viseme));
      idx++;

      // Skip ahead through consecutive same-viseme chars
      while (idx < chars.length) {
        var nextViseme = CHAR_TO_VISEME[chars[idx]] || 'small';
        if (nextViseme !== viseme) break;
        idx++;
      }

      speakTimer = setTimeout(nextChar, 80);
    }

    nextChar();
  }

  // ─── Alien Character Config ───────────────────────────────────────

  var alienCharacter = {
    name: 'alien',
    css: '\
      .alien-char { position: relative; width: 140px; height: 220px; }\
      .alien-head-group {\
        position: relative; z-index: 2; width: 95%;\
        margin: 0 auto;\
        animation: alien-bob 7s ease-in-out alternate infinite;\
      }\
      .alien-head-group img { display: block; width: 100%; }\
      .alien-body-group {\
        position: relative; z-index: 1;\
        margin-top: -12px;\
        max-height: 80px; overflow: hidden;\
      }\
      .alien-body-group img { display: block; width: 100%; }\
      @keyframes alien-bob {\
        0%   { transform: rotate(-2deg) translateY(0); }\
        40%  { transform: rotate(-2deg) translateY(0); }\
        60%  { transform: rotate(2deg) translateY(-2px); }\
        100% { transform: rotate(2deg) translateY(-2px); }\
      }\
      @media (max-width: 800px) {\
        .alien-char { width: 100px; height: 160px; }\
      }\
    ',
    svgFilters: '',
    buildDOM: function (wrapper) {
      wrapper.classList.add('alien-char');
      wrapper.innerHTML = '\
        <div class="alien" data-char-el>\
          <div class="alien-head-group">\
            <img class="alien-head" src="' + SPRITE_BASE + 'neutral-smile.png" alt="">\
          </div>\
          <div class="alien-body-group">\
            <img class="alien-body" src="' + SPRITE_BASE + 'body-idle.png" alt="">\
          </div>\
        </div>';

      // Store refs for the animator
      alienHeadImg = wrapper.querySelector('.alien-head');
      alienBodyImg = wrapper.querySelector('.alien-body');

      // Start blinking
      startBlinking();
    }
  };

  // ─── Character System ─────────────────────────────────────────────

  var containerCSS = '\
    .characters-container {\
      position: absolute; z-index: 4; cursor: pointer;\
      right: 20px; display: flex; align-items: flex-end; gap: 4px;\
    }\
    @media (max-width: 800px) {\
      .characters-container { right: 10px !important; gap: 2px; }\
    }\
    .char-speech-bubble {\
      position: absolute; bottom: 100%; right: 0; margin-bottom: 8px;\
      background: rgba(30,30,40,0.92); color: #C6CBF5;\
      border: 1px solid rgba(255,255,255,0.15); border-radius: 12px;\
      padding: 8px 14px; font-size: 14px; white-space: nowrap;\
      pointer-events: none; animation: bubble-bob 2s ease-in-out infinite;\
      box-shadow: 0 2px 12px rgba(0,0,0,0.4);\
    }\
    .char-speech-bubble::after {\
      content: ""; position: absolute; bottom: -7px; right: 24px;\
      border-left: 7px solid transparent; border-right: 7px solid transparent;\
      border-top: 7px solid rgba(30,30,40,0.92);\
    }\
    @keyframes bubble-bob {\
      0%, 100% { transform: translateY(0); }\
      50% { transform: translateY(-4px); }\
    }\
  ';

  function injectCSS(css) {
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
  }

  function injectSVGFilters(filtersMarkup) {
    if (!filtersMarkup) return;
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('style', 'display:none');
    svg.innerHTML = '<defs>' + filtersMarkup + '</defs>';
    document.body.appendChild(svg);
  }

  function createCharacter(config, container) {
    var wrapper = document.createElement('div');
    config.buildDOM(wrapper);
    container.appendChild(wrapper);
    injectCSS(config.css);
    injectSVGFilters(config.svgFilters);
    var charEl = wrapper.querySelector('[data-char-el]');
    characters.push(charEl);
    return charEl;
  }

  function setAllCharacterStates(state) {
    // Robot: CSS class toggle
    for (var i = 0; i < characters.length; i++) {
      var el = characters[i];
      el.classList.remove('char_speaking', 'char_listening');
      if (state === 'speaking') el.classList.add('char_speaking');
      else if (state === 'listening') el.classList.add('char_listening');
    }

    // Wishonia: sprite-based state changes
    if (state === 'speaking') {
      currentExpression = 'happy';
      setBody('presenting');
      stopBlinking();
    } else if (state === 'listening') {
      isSpeaking = false;
      currentExpression = 'neutral';
      setHead('neutral-closed');
      setBody('listening');
      stopBlinking();
    } else if (state === 'thinking') {
      isSpeaking = false;
      currentExpression = 'thinking';
      setHead('thinking-closed');
      setBody('idle');
      stopBlinking();
    } else {
      // idle
      currentExpression = 'neutral';
      setIdle();
      setBody('idle');
    }
  }

  function positionCharacters(container) {
    var inputArea = document.querySelector('.chat-input-area');
    if (!inputArea || !container) return;
    var rect = inputArea.getBoundingClientRect();
    container.style.bottom = (window.innerHeight - rect.top - 40) + 'px';
  }

  // ─── Init ─────────────────────────────────────────────────────────

  function init() {
    var container = document.createElement('div');
    container.className = 'characters-container';
    container.id = 'characters-container';

    injectCSS(containerCSS);
    createCharacter(alienCharacter, container);

    var speechBubble = document.createElement('div');
    speechBubble.className = 'char-speech-bubble';
    speechBubble.textContent = 'click me to argue by voice';
    container.appendChild(speechBubble);

    // Append inside the chat panel so we share its stacking context
    // (allows input bar z-index to be above the character)
    function attachToPanel() {
      var panel = document.querySelector('.chat-panel');
      if (panel) {
        panel.appendChild(container);
        positionCharacters(container);
        return true;
      }
      return false;
    }

    // Chat panel may not exist yet or may get reparented - retry until found
    if (!attachToPanel()) {
      var retries = 0;
      var checkInterval = setInterval(function () {
        if (attachToPanel() || ++retries > 20) clearInterval(checkInterval);
      }, 200);
    }

    window.addEventListener('resize', function () { positionCharacters(container); });

    container.addEventListener('click', function () {
      if (speechBubble.parentNode) speechBubble.remove();
      var vcBtn = document.querySelector('.chat-voicechat-btn');
      if (vcBtn && vcBtn.style.display !== 'none') vcBtn.click();
    });

    // Backward compat
    window.setRobotState = setAllCharacterStates;
    window.positionCharacters = function () { positionCharacters(container); };

    // Expose animator for chat-widget.js to call
    var lastMouthUpdate = 0;
    window.wishoniaAnimator = {
      // Audio amplitude-driven lip sync (called from onAudio)
      setMouthFromAmplitude: function (amplitude) {
        var now = Date.now();
        if (now - lastMouthUpdate < 67) return; // throttle to ~15fps
        lastMouthUpdate = now;
        isSpeaking = true;

        var viseme;
        if (amplitude < 0.02) viseme = 'closed';
        else if (amplitude < 0.08) viseme = 'small';
        else if (amplitude < 0.15) viseme = 'oh';
        else if (amplitude < 0.25) viseme = 'open';
        else viseme = 'ee';

        setHead(getHeadName(currentExpression, viseme));
      },
      // Text-driven lip sync (fallback, used by test page TTS demo)
      speakText: function (text, expression) {
        animateText(text, expression || 'happy');
      },
      stopSpeaking: function () {
        setIdle();
      },
      setExpression: function (expr) {
        currentExpression = expr;
        if (!isSpeaking) setHead(getIdleHead(expr));
      },
      setBody: setBody
    };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
