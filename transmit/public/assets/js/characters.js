/**
 * Modular character system for animated chat avatars.
 * Each character is a config with buildDOM(), css, and svgFilters.
 * All characters respond to window.setRobotState('speaking'|'listening'|'idle').
 */
(function () {
  'use strict';

  var characters = [];

  // ─── Robot Character ───────────────────────────────────────────────

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

  // ─── Alien Girl Character (Wishonia) ───────────────────────────────

  var alienCharacter = {
    name: 'alien',
    css: '\
      .alien-char { position: relative; width: 120px; height: 140px; }\
      /* --- Antennae --- */\
      .alien .antennae {\
        position: absolute; top: 0; left: 50%; width: 40px; margin-left: -20px; height: 30px; z-index: 5;\
      }\
      .alien .antenna {\
        position: absolute; bottom: 0; width: 3px; height: 24px;\
        background: linear-gradient(to top, #3a5a6a, #5a8a9a);\
        border-radius: 3px;\
      }\
      .alien .antenna::after {\
        content: ""; position: absolute; top: -9px; left: -4px;\
        width: 11px; height: 11px; border-radius: 50%;\
        background: radial-gradient(circle at 35% 35%, #a0e8ff, #5bb8d4 50%, #3a8aa0);\
        box-shadow: 0 0 8px rgba(90,184,212,0.6), 0 0 16px rgba(90,184,212,0.3);\
        animation: alien-glow 2s ease-in-out infinite alternate;\
      }\
      .alien .antenna_left { left: 4px; transform: rotate(-12deg); transform-origin: bottom center; animation: alien-sway-left 3s ease-in-out infinite alternate; }\
      .alien .antenna_right { right: 4px; transform: rotate(12deg); transform-origin: bottom center; animation: alien-sway-right 3s ease-in-out infinite alternate; }\
      /* --- Head (blue skin) --- */\
      .alien .head {\
        position: absolute; top: 18px; left: 10px; width: 100px; height: 96px;\
        border-radius: 50% 50% 46% 46%;\
        background: linear-gradient(135deg, #7fbdcc 0%, #6ba3b8 30%, #5b93a8 70%, #4e8298 100%);\
        transform-origin: 50% 100%;\
        animation: alien-bob 7000ms ease-in-out alternate infinite -500ms;\
        overflow: visible;\
      }\
      /* --- Hair: black 60s bob --- */\
      .alien .hair {\
        position: absolute; top: -6px; left: -6px; right: -6px; height: 42px;\
        background: #1a1a1a;\
        border-radius: 54px 54px 3px 3px;\
        z-index: 1;\
      }\
      .alien .hair::before {\
        content: ""; position: absolute; bottom: -14px; left: 1px;\
        width: 18px; height: 18px;\
        background: #1a1a1a;\
        border-radius: 0 0 0 12px;\
      }\
      .alien .hair::after {\
        content: ""; position: absolute; bottom: -14px; right: 1px;\
        width: 18px; height: 18px;\
        background: #1a1a1a;\
        border-radius: 0 0 12px 0;\
      }\
      /* Straight-across bangs */\
      .alien .fringe {\
        position: absolute; top: 10px; left: 8px; right: 8px; height: 8px;\
        background: #1a1a1a;\
        border-radius: 0 0 1px 1px;\
        z-index: 3;\
      }\
      .alien .face { position: absolute; inset: 0; z-index: 2; }\
      /* --- Eyebrows --- */\
      .alien .eyebrows {\
        position: absolute; top: 26px; left: 18px; right: 18px; height: 6px; z-index: 5;\
      }\
      .alien .eyebrow {\
        position: absolute; width: 22px; height: 3px;\
        border-top: 2.5px solid #1a2a30;\
        border-radius: 40% 40% 0 0;\
      }\
      .alien .eyebrow_left { left: 2px; transform: rotate(-5deg); }\
      .alien .eyebrow_right { right: 2px; transform: rotate(5deg); }\
      /* --- Eyes (big, almond-shaped, white sclera) --- */\
      .alien .eyes {\
        position: absolute; top: 36px; left: 14px; right: 14px; height: 24px;\
        animation: alien-blink 8000ms linear forwards infinite;\
        z-index: 4;\
      }\
      .alien .eyeball {\
        position: absolute; width: 28px; height: 22px;\
        background: #fff;\
        border-radius: 50% 50% 50% 50% / 55% 55% 45% 45%;\
        border: 2px solid #2a4a55;\
        overflow: hidden;\
      }\
      /* Iris */\
      .alien .eyeball::after {\
        content: ""; position: absolute; top: 3px; left: 8px;\
        width: 13px; height: 14px; border-radius: 50%;\
        background: radial-gradient(circle at 45% 40%, #2a5060 0%, #1a3a4a 70%, #0e2530 100%);\
      }\
      /* Highlight/catchlight */\
      .alien .eyeball::before {\
        content: ""; position: absolute; top: 5px; left: 12px;\
        width: 4px; height: 4px; border-radius: 50%;\
        background: rgba(255,255,255,0.9); z-index: 1;\
      }\
      .alien .eyeball_left { left: 0; }\
      .alien .eyeball_right { right: 0; }\
      /* --- Smile mouth --- */\
      .alien .mouth {\
        position: absolute; bottom: 16px; left: 50%; margin-left: -12px; width: 24px; height: 6px;\
        background-color: #2a4a55; overflow: hidden;\
        border-radius: 0 0 12px 12px;\
        transition: height 100ms cubic-bezier(0.455,0.03,0.515,0.955);\
        z-index: 4;\
      }\
      .alien .mouth-container { position: absolute; inset: 0; }\
      .alien .mouth-container-line {\
        position: absolute; top: 30%; height: 0; background-color: #5bb8d4; width: 100%; margin-top: -1px;\
      }\
      .alien.char_speaking .mouth { height: 12px; border-radius: 4px 4px 12px 12px; }\
      .alien.char_speaking .mouth-container { animation: alien-speakingAnim 0.3s infinite; }\
      .alien.char_speaking .mouth-container-line { height: 3px; }\
      .alien.char_listening .mouth { height: 8px; }\
      .alien.char_listening .mouth-container { animation: alien-listeningAnim 0.5s infinite; }\
      .alien.char_listening .mouth-container-line { height: 2px; }\
      /* --- Cheeks --- */\
      .alien .cheeks {\
        position: absolute; bottom: 22px; left: 12px; right: 12px; height: 12px;\
        z-index: 3; pointer-events: none;\
      }\
      .alien .cheek {\
        position: absolute; width: 16px; height: 10px; border-radius: 50%;\
        background: rgba(100,180,200,0.25);\
      }\
      .alien .cheek_left { left: 0; }\
      .alien .cheek_right { right: 0; }\
      /* --- Animations --- */\
      @keyframes alien-bob {\
        0%  { transform: rotate(-2deg) translateY(0); }\
        40% { transform: rotate(-2deg) translateY(0); animation-timing-function: cubic-bezier(1,0,0,1); }\
        60% { transform: rotate(2deg) translateY(-2px); }\
        100%{ transform: rotate(2deg) translateY(-2px); }\
      }\
      @keyframes alien-blink {\
        48% { transform: scale(1,1); }\
        49% { transform: scale(1,0.05); }\
        50% { transform: scale(1,1); }\
      }\
      @keyframes alien-sway-left {\
        0%   { transform: rotate(-12deg); }\
        100% { transform: rotate(-7deg); }\
      }\
      @keyframes alien-sway-right {\
        0%   { transform: rotate(12deg); }\
        100% { transform: rotate(7deg); }\
      }\
      @keyframes alien-glow {\
        0%   { box-shadow: 0 0 6px rgba(90,184,212,0.4), 0 0 12px rgba(90,184,212,0.2); }\
        100% { box-shadow: 0 0 12px rgba(90,184,212,0.8), 0 0 24px rgba(90,184,212,0.4); }\
      }\
      @keyframes alien-speakingAnim {\
        0%   { filter: url("#alien-speaking-0"); }\
        25%  { filter: url("#alien-speaking-1"); }\
        50%  { filter: url("#alien-speaking-2"); }\
        75%  { filter: url("#alien-speaking-3"); }\
        100% { filter: url("#alien-speaking-4"); }\
      }\
      @keyframes alien-listeningAnim {\
        0%   { filter: url("#alien-listening-0"); }\
        25%  { filter: url("#alien-listening-1"); }\
        50%  { filter: url("#alien-listening-2"); }\
        75%  { filter: url("#alien-listening-3"); }\
        100% { filter: url("#alien-listening-4"); }\
      }\
      @media (max-width: 800px) {\
        .alien-char { width: 80px; height: 85px; }\
        .alien .head { width: 68px; left: 6px; height: 64px; top: 14px; }\
        .alien .hair { top: -4px; left: -4px; right: -4px; height: 28px; }\
        .alien .hair::before, .alien .hair::after { bottom: -10px; width: 14px; height: 14px; }\
        .alien .fringe { top: 7px; left: 6px; right: 6px; height: 6px; }\
        .alien .eyebrows { top: 18px; left: 12px; right: 12px; }\
        .alien .eyebrow { width: 16px; }\
        .alien .eyes { top: 24px; left: 10px; right: 10px; height: 16px; }\
        .alien .eyeball { width: 20px; height: 16px; }\
        .alien .eyeball::after { top: 2px; left: 5px; width: 10px; height: 10px; }\
        .alien .eyeball::before { top: 3px; left: 8px; width: 3px; height: 3px; }\
        .alien .mouth { bottom: 10px; width: 18px; margin-left: -9px; height: 4px; }\
        .alien .cheeks { bottom: 14px; }\
        .alien .cheek { width: 12px; height: 7px; }\
        .alien .antennae { height: 20px; width: 30px; margin-left: -15px; }\
        .alien .antenna { height: 16px; }\
        .alien .antenna::after { width: 8px; height: 8px; top: -6px; left: -3px; }\
      }\
    ',
    svgFilters: '\
      <filter id="alien-speaking-0"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="0"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="10"/></filter>\
      <filter id="alien-speaking-1"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="30"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="11"/></filter>\
      <filter id="alien-speaking-2"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="2"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="10"/></filter>\
      <filter id="alien-speaking-3"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="30"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="11"/></filter>\
      <filter id="alien-speaking-4"><feTurbulence baseFrequency="0.1" numOctaves="3" result="noise" seed="4"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="9"/></filter>\
      <filter id="alien-listening-0"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="0"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="2"/></filter>\
      <filter id="alien-listening-1"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="30"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="3"/></filter>\
      <filter id="alien-listening-2"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="2"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="2"/></filter>\
      <filter id="alien-listening-3"><feTurbulence baseFrequency="0.02" numOctaves="3" result="noise" seed="30"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="3"/></filter>\
      <filter id="alien-listening-4"><feTurbulence baseFrequency="0.1" numOctaves="3" result="noise" seed="4"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="1"/></filter>\
    ',
    buildDOM: function (wrapper) {
      wrapper.classList.add('alien-char');
      wrapper.innerHTML = '\
        <div class="alien" data-char-el>\
          <div class="antennae">\
            <div class="antenna antenna_left"></div>\
            <div class="antenna antenna_right"></div>\
          </div>\
          <div class="head">\
            <div class="hair"></div>\
            <div class="fringe"></div>\
            <div class="face">\
              <div class="eyebrows"><div class="eyebrow eyebrow_left"></div><div class="eyebrow eyebrow_right"></div></div>\
              <div class="eyes">\
                <div class="eyeball eyeball_left"></div>\
                <div class="eyeball eyeball_right"></div>\
              </div>\
              <div class="cheeks"><div class="cheek cheek_left"></div><div class="cheek cheek_right"></div></div>\
              <div class="mouth"><div class="mouth-container"><div class="mouth-container-line"></div></div></div>\
            </div>\
          </div>\
        </div>';
    }
  };

  // ─── Character System ──────────────────────────────────────────────

  /** Container CSS */
  var containerCSS = '\
    .characters-container {\
      position: absolute; z-index: 20; cursor: pointer;\
      right: 20px; display: flex; align-items: flex-end; gap: 4px;\
    }\
    @media (max-width: 800px) {\
      .characters-container { right: 10px !important; gap: 2px; }\
    }\
  ';

  function injectCSS(css) {
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
  }

  function injectSVGFilters(filtersMarkup) {
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
    for (var i = 0; i < characters.length; i++) {
      var el = characters[i];
      el.classList.remove('char_speaking', 'char_listening');
      if (state === 'speaking') el.classList.add('char_speaking');
      else if (state === 'listening') el.classList.add('char_listening');
    }
  }

  function positionCharacters(container) {
    var inputArea = document.querySelector('.chat-input-area');
    if (!inputArea || !container) return;
    var rect = inputArea.getBoundingClientRect();
    container.style.bottom = (window.innerHeight - rect.top) + 'px';
  }

  // ─── Init ──────────────────────────────────────────────────────────

  function init() {
    var mainArea = document.getElementById('main-area');
    if (!mainArea) return;

    // Create container
    var container = document.createElement('div');
    container.className = 'characters-container';
    container.id = 'characters-container';
    mainArea.appendChild(container);

    injectCSS(containerCSS);

    // Add characters (alien on left, robot on right)
    createCharacter(alienCharacter, container);
    createCharacter(robotCharacter, container);

    // Position above input bar
    positionCharacters(container);
    window.addEventListener('resize', function () { positionCharacters(container); });

    // Click to trigger voice chat
    container.addEventListener('click', function () {
      var vcBtn = document.querySelector('.chat-voicechat-btn');
      if (vcBtn && vcBtn.style.display !== 'none') vcBtn.click();
    });

    // Expose global state setter (backward compat with chat-widget.js)
    window.setRobotState = setAllCharacterStates;

    // Expose for external positioning calls
    window.positionCharacters = function () { positionCharacters(container); };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
