/**
 * Arcade mortality scoreboard for the War on Disease manual.
 *
 * A sticky video-game HUD counts counterfactual schedule deaths: humans who die
 * because the disease-eradication date remains one day farther away than it would
 * be under immediate implementation of this plan or a better one. Clicking the
 * scoreboard opens a fullscreen CRT screen that explains the rules of the game.
 */

(function() {
  'use strict';

  var STORAGE_KEY = 'dih-delay-counter-dismissed';
  var DEFAULT_PUBLICATION_DATE = '2025-10-04';
  // Network-failure fallbacks only. Canonical values live in dih_models/parameters.py
  // (GLOBAL_DISEASE_DEATHS_DAILY, EVENTUALLY_AVOIDABLE_DEATH_PCT, GLOBAL_ANNUAL_DALY_BURDEN,
  // EVENTUALLY_AVOIDABLE_DALY_PCT, DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED/_DALYS)
  // and are fetched from assets/json/parameters.json at runtime.
  var DEFAULTS = {
    diseaseDeathsDaily: 150000,
    eventuallyAvoidableDeathPct: 0.926,
    dalyBurdenAnnual: 2880000000,
    eventuallyAvoidableDalyPct: 0.926,
    timelineLivesSaved: 10745517748.6,
    timelineDalys: 565243673351
  };

  var COPY = {
    hudAriaLabel: 'Live scoreboard of avoidable disease deaths',
    kicker: 'PLACEHOLDER KICKER',
    scoreLabel: 'DISEASE',
    scoreUnitLine: 'PLACEHOLDER UNIT LINE',
    sufferingLabel: 'PLACEHOLDER SUFFERING LABEL',
    highScoreLine: 'NEW HIGH SCORE',
    ctaText: 'PRESS START',
    openHint: 'PLACEHOLDER OPEN HINT',
    fabShow: 'Show the score',
    fabHide: 'Hide the score',
    closeHint: 'Hide the scoreboard',
    overlay: {
      closeText: 'RESUME IGNORING',
      title: 'PLACEHOLDER TITLE',
      subtitle: 'PLACEHOLDER SUBTITLE',
      diseaseLabel: 'DISEASE',
      diseaseFoot: 'PLACEHOLDER DISEASE FOOT',
      humanityLabel: 'HUMANITY',
      humanityScoreText: '0',
      humanityFootnote: 'PLACEHOLDER HUMANITY FOOT',
      rulesHeading: 'THE RULES',
      rules: ['PLACEHOLDER RULE'],
      player2Heading: 'HOW TO PLAY',
      player2: 'PLACEHOLDER PLAYER 2',
      cheatHeading: 'CHEAT CODE',
      cheatCode: 'PLACEHOLDER CHEAT CODE',
      sinceOpenedBefore: 'PLACEHOLDER SINCE ',
      sinceOpenedAfter: ' PLACEHOLDER AFTER',
      auditPre: 'PLACEHOLDER AUDIT ',
      auditLinkText: 'audit the scoreboard',
      auditPost: '.',
      ctaPrimary: 'PRESS START',
      ctaSecondary: 'AUDIT THE SCORE'
    }
  };

  var VOTE_URL = 'https://warondisease.org';
  var AUDIT_PAGE = 'knowledge/appendix/where-am-i-wrong.html';
  var CALC_ANCHOR = 'knowledge/appendix/parameters-and-calculations.html#sec-global_eventually_avoidable_disease_deaths_daily';

  var model = {
    diseaseDeathsDaily: DEFAULTS.diseaseDeathsDaily,
    eventuallyAvoidableDeathPct: DEFAULTS.eventuallyAvoidableDeathPct,
    dalyBurdenAnnual: DEFAULTS.dalyBurdenAnnual,
    eventuallyAvoidableDalyPct: DEFAULTS.eventuallyAvoidableDalyPct,
    timelineLivesSaved: DEFAULTS.timelineLivesSaved,
    timelineDalys: DEFAULTS.timelineDalys
  };

  var numberFormat = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });
  var compactFormat = new Intl.NumberFormat('en-US', {
    notation: 'compact',
    maximumFractionDigits: 2
  });

  var counterEl = null;
  var overlayEl = null;
  var overlayOpenedAt = null;
  var rafId = null;
  var lastTick = 0;

  // 13x12 pixel-grid skull, one array entry per row: [colStart, colEnd] runs.
  var SKULL_ROWS = [
    [[3, 9]],
    [[2, 10]],
    [[1, 11]],
    [[1, 11]],
    [[1, 2], [5, 7], [10, 11]],
    [[1, 2], [5, 7], [10, 11]],
    [[1, 11]],
    [[2, 5], [7, 10]],
    [[2, 10]],
    [[3, 9]],
    [[3, 3], [5, 5], [7, 7], [9, 9]],
    [[3, 3], [5, 5], [7, 7], [9, 9]]
  ];

  function skullSvg() {
    var rects = '';
    for (var y = 0; y < SKULL_ROWS.length; y++) {
      var runs = SKULL_ROWS[y];
      for (var r = 0; r < runs.length; r++) {
        rects += '<rect x="' + runs[r][0] + '" y="' + y + '" width="' + (runs[r][1] - runs[r][0] + 1) + '" height="1"/>';
      }
    }
    return '<svg viewBox="0 0 13 12" fill="currentColor" aria-hidden="true">' + rects + '</svg>';
  }

  function getOffset() {
    var meta = document.querySelector('meta[name="quarto:offset"]');
    var offset = meta ? meta.getAttribute('content') || '' : '';
    if (offset && offset.charAt(offset.length - 1) !== '/') offset += '/';
    return offset;
  }

  function getPublicationDate() {
    var meta = document.querySelector('meta[name="dih-publication-date"]');
    var value = meta && meta.content ? meta.content : DEFAULT_PUBLICATION_DATE;
    return new Date(value + 'T00:00:00Z');
  }

  function getStoredDismissed() {
    try {
      return localStorage.getItem(STORAGE_KEY) === 'true';
    } catch (error) {
      return false;
    }
  }

  function setStoredDismissed(value) {
    try {
      localStorage.setItem(STORAGE_KEY, value ? 'true' : 'false');
    } catch (error) {
      // Storage can fail in privacy-restricted contexts. The widget still works.
    }
  }

  function isDisabled() {
    var meta = document.querySelector('meta[name="dih-disable-features"]');
    if (!meta || !meta.content) return false;
    return meta.content.split(',').map(function(item) {
      return item.trim();
    }).indexOf('delay-counter') !== -1;
  }

  function pickParam(parameters, name, fallback) {
    return parameters && parameters[name] && typeof parameters[name].value === 'number'
      ? parameters[name].value
      : fallback;
  }

  function loadModel() {
    if (window.location.protocol === 'file:') return Promise.resolve();

    return fetch(getOffset() + 'assets/json/parameters.json')
      .then(function(response) {
        if (!response.ok) return null;
        return response.json();
      })
      .then(function(json) {
        var parameters = json && json.parameters ? json.parameters : null;
        model.diseaseDeathsDaily = pickParam(parameters, 'GLOBAL_DISEASE_DEATHS_DAILY', DEFAULTS.diseaseDeathsDaily);
        model.eventuallyAvoidableDeathPct = pickParam(parameters, 'EVENTUALLY_AVOIDABLE_DEATH_PCT', DEFAULTS.eventuallyAvoidableDeathPct);
        model.dalyBurdenAnnual = pickParam(parameters, 'GLOBAL_ANNUAL_DALY_BURDEN', DEFAULTS.dalyBurdenAnnual);
        model.eventuallyAvoidableDalyPct = pickParam(parameters, 'EVENTUALLY_AVOIDABLE_DALY_PCT', DEFAULTS.eventuallyAvoidableDalyPct);
        model.timelineLivesSaved = pickParam(parameters, 'DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED', DEFAULTS.timelineLivesSaved);
        model.timelineDalys = pickParam(parameters, 'DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS', DEFAULTS.timelineDalys);
      })
      .catch(function() {
        model.diseaseDeathsDaily = DEFAULTS.diseaseDeathsDaily;
        model.eventuallyAvoidableDeathPct = DEFAULTS.eventuallyAvoidableDeathPct;
        model.dalyBurdenAnnual = DEFAULTS.dalyBurdenAnnual;
        model.eventuallyAvoidableDalyPct = DEFAULTS.eventuallyAvoidableDalyPct;
        model.timelineLivesSaved = DEFAULTS.timelineLivesSaved;
        model.timelineDalys = DEFAULTS.timelineDalys;
      });
  }

  function delayDeathsPerSecond() {
    return model.diseaseDeathsDaily * model.eventuallyAvoidableDeathPct / 86400;
  }

  // 1 DALY = 1 year of healthy life = 8,766 hours. X DALYs/year accrue at
  // X * 8766 / 31,557,600 = X / 3600 hours per second.
  function sufferingHoursPerSecond() {
    return model.dalyBurdenAnnual * model.eventuallyAvoidableDalyPct / 3600;
  }

  function elapsedSincePublication() {
    return Math.max(0, (Date.now() - getPublicationDate().getTime()) / 1000);
  }

  function currentSincePublication() {
    return elapsedSincePublication() * delayDeathsPerSecond();
  }

  function format(value, compact) {
    return compact ? compactFormat.format(value) : numberFormat.format(value);
  }

  function textForValue(kind, compact) {
    if (kind === 'since-publication') return format(currentSincePublication(), compact);
    if (kind === 'per-day') return format(model.diseaseDeathsDaily * model.eventuallyAvoidableDeathPct, compact);
    if (kind === 'per-minute') return format(model.diseaseDeathsDaily * model.eventuallyAvoidableDeathPct / 1440, compact);
    if (kind === 'per-second') return compactFormat.format(delayDeathsPerSecond());
    if (kind === 'suffering-hours-since-publication') return format(elapsedSincePublication() * sufferingHoursPerSecond(), compact);
    if (kind === 'suffering-hours-per-second') return format(sufferingHoursPerSecond(), compact);
    if (kind === 'since-opened') {
      if (overlayOpenedAt === null) return '0';
      return format(Math.max(0, (Date.now() - overlayOpenedAt) / 1000) * delayDeathsPerSecond(), false);
    }
    if (kind === 'timeline-lives') return format(model.timelineLivesSaved, compact);
    if (kind === 'timeline-dalys') return format(model.timelineDalys, compact);
    if (kind === 'publication-date') return getPublicationDate().toISOString().slice(0, 10);
    return '';
  }

  function updateCounters() {
    var nodes = document.querySelectorAll('[data-dih-delay-value]');
    for (var i = 0; i < nodes.length; i++) {
      var node = nodes[i];
      var compact = node.getAttribute('data-dih-delay-compact') === 'true';
      node.textContent = textForValue(node.getAttribute('data-dih-delay-value'), compact);
    }
  }

  function tick(now) {
    // Deaths change ~1.6/s; suffering hours change ~741K/s. ~8 fps keeps the
    // long number visibly spinning without burning the battery.
    if (now - lastTick >= 125) {
      lastTick = now;
      if (!document.hidden) updateCounters();
    }
    rafId = window.requestAnimationFrame(tick);
  }

  function createCounter() {
    counterEl = document.getElementById('dih-delay-counter');
    if (counterEl) return;

    var hidden = getStoredDismissed();
    counterEl = document.createElement('aside');
    counterEl.id = 'dih-delay-counter';
    counterEl.className = 'dih-delay-counter' + (hidden ? ' dih-delay-counter-hidden' : '');
    counterEl.setAttribute('aria-label', COPY.hudAriaLabel);
    counterEl.innerHTML =
      '<button class="dih-arcade-open" type="button" title="' + COPY.openHint + '">' +
        '<span class="dih-arcade-skull">' + skullSvg() + '</span>' +
        '<span class="dih-arcade-score-block">' +
          '<span class="dih-arcade-kicker">' + COPY.kicker + '</span>' +
          '<span class="dih-arcade-score"><span data-dih-delay-value="since-publication">0</span></span>' +
          '<span class="dih-arcade-unitline">' + COPY.scoreUnitLine + '</span>' +
        '</span>' +
        '<span class="dih-arcade-suffer-block">' +
          '<span class="dih-arcade-suffer-label">' + COPY.sufferingLabel + '</span>' +
          '<span class="dih-arcade-suffer" data-dih-delay-value="suffering-hours-since-publication">0</span>' +
        '</span>' +
        '<span class="dih-arcade-blink">' + COPY.highScoreLine + '</span>' +
      '</button>' +
      '<a class="dih-arcade-cta" href="' + VOTE_URL + '" target="_blank" rel="noopener">' + COPY.ctaText + '</a>' +
      '<button class="dih-delay-counter-close" type="button" aria-label="' + COPY.closeHint + '" title="' + COPY.closeHint + '">' +
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>' +
      '</button>';

    document.body.appendChild(counterEl);
    document.body.classList.toggle('dih-delay-counter-visible', !hidden);

    counterEl.querySelector('.dih-arcade-open').addEventListener('click', openOverlay);
    counterEl.querySelector('.dih-delay-counter-close').addEventListener('click', hideCounter);
  }

  function sectionHtml(heading, bodyHtml) {
    return '<section class="dih-arcade-section">' +
      '<h3 class="dih-arcade-heading">' + heading + '</h3>' + bodyHtml + '</section>';
  }

  function createOverlay() {
    if (overlayEl) return;
    var o = COPY.overlay;
    var offset = getOffset();

    var rulesHtml = '<ul>';
    for (var i = 0; i < o.rules.length; i++) rulesHtml += '<li>' + o.rules[i] + '</li>';
    rulesHtml += '</ul>';

    overlayEl = document.createElement('div');
    overlayEl.id = 'dih-arcade-overlay';
    overlayEl.className = 'dih-arcade-overlay';
    overlayEl.setAttribute('role', 'dialog');
    overlayEl.setAttribute('aria-modal', 'true');
    overlayEl.setAttribute('aria-label', o.title);
    overlayEl.innerHTML =
      '<button class="dih-arcade-overlay-close" type="button">✕ ' + o.closeText + '</button>' +
      '<div class="dih-arcade-screen">' +
        '<div class="dih-arcade-skull-big">' + skullSvg() + '</div>' +
        '<h2 class="dih-arcade-title">' + o.title + '</h2>' +
        '<p class="dih-arcade-subtitle">' + o.subtitle + '</p>' +
        '<div class="dih-arcade-board">' +
          '<div class="dih-arcade-side dih-arcade-side-disease">' +
            '<span class="dih-arcade-team">' + o.diseaseLabel + '</span>' +
            '<span class="dih-arcade-pts" data-dih-delay-value="since-publication">0</span>' +
            '<span class="dih-arcade-foot">' + o.diseaseFoot + '</span>' +
          '</div>' +
          '<div class="dih-arcade-vs">VS</div>' +
          '<div class="dih-arcade-side dih-arcade-side-humanity">' +
            '<span class="dih-arcade-team">' + o.humanityLabel + '</span>' +
            '<span class="dih-arcade-pts">' + o.humanityScoreText + '</span>' +
            '<span class="dih-arcade-foot">' + o.humanityFootnote + '</span>' +
          '</div>' +
        '</div>' +
        '<div class="dih-arcade-sufferline">' + COPY.sufferingLabel +
          '<span class="dih-arcade-suffer" data-dih-delay-value="suffering-hours-since-publication">0</span>' +
        '</div>' +
        sectionHtml(o.rulesHeading, rulesHtml) +
        sectionHtml(o.player2Heading, '<p>' + o.player2 + '</p>') +
        sectionHtml(o.cheatHeading, '<p>' + o.cheatCode + '</p>') +
        '<div class="dih-arcade-sinceopened">' + o.sinceOpenedBefore +
          '<span class="dih-arcade-live" data-dih-delay-value="since-opened">0</span>' + o.sinceOpenedAfter +
        '</div>' +
        '<div class="dih-arcade-ctas">' +
          '<a class="dih-arcade-cta-primary" href="' + VOTE_URL + '" target="_blank" rel="noopener">' + o.ctaPrimary + '</a>' +
          '<a class="dih-arcade-cta-secondary" href="' + offset + AUDIT_PAGE + '">' + o.ctaSecondary + '</a>' +
        '</div>' +
        '<p class="dih-arcade-audit">' + o.auditPre +
          '<a href="' + offset + CALC_ANCHOR + '">' + o.auditLinkText + '</a>' + o.auditPost +
        '</p>' +
      '</div>';

    document.body.appendChild(overlayEl);
    overlayEl.querySelector('.dih-arcade-overlay-close').addEventListener('click', closeOverlay);
    document.addEventListener('keydown', function(event) {
      if (event.key === 'Escape' && overlayEl.classList.contains('dih-arcade-overlay-visible')) {
        closeOverlay();
      }
    });
  }

  function openOverlay() {
    createOverlay();
    overlayOpenedAt = Date.now();
    overlayEl.classList.add('dih-arcade-overlay-visible');
    document.body.classList.add('dih-arcade-overlay-open');
    updateCounters();
    overlayEl.querySelector('.dih-arcade-overlay-close').focus();
  }

  function closeOverlay() {
    if (!overlayEl) return;
    overlayEl.classList.remove('dih-arcade-overlay-visible');
    document.body.classList.remove('dih-arcade-overlay-open');
    overlayOpenedAt = null;
  }

  function hideCounter() {
    if (!counterEl) return;
    counterEl.classList.add('dih-delay-counter-hidden');
    document.body.classList.remove('dih-delay-counter-visible');
    setStoredDismissed(true);
    updateFabLabel();
  }

  function showCounter() {
    if (!counterEl) createCounter();
    counterEl.classList.remove('dih-delay-counter-hidden');
    document.body.classList.add('dih-delay-counter-visible');
    setStoredDismissed(false);
    updateCounters();
    updateFabLabel();
  }

  function toggleCounter() {
    if (counterEl && counterEl.classList.contains('dih-delay-counter-hidden')) {
      showCounter();
    } else {
      hideCounter();
    }
  }

  function updateFabLabel() {
    var btn = document.getElementById('dih-fab-delay-counter');
    if (!btn) return;
    var hidden = counterEl && counterEl.classList.contains('dih-delay-counter-hidden');
    var label = hidden ? COPY.fabShow : COPY.fabHide;
    btn.title = label;
    btn.setAttribute('aria-label', label);
    var labelEl = btn.querySelector('.dih-fab-action-label');
    if (labelEl) labelEl.textContent = label;
  }

  function registerFabAction(attempt) {
    attempt = attempt || 0;
    if (!window.dihFAB || typeof window.dihFAB.addAction !== 'function') {
      if (attempt < 40) {
        setTimeout(function() {
          registerFabAction(attempt + 1);
        }, 100);
      }
      return;
    }

    window.dihFAB.addAction(
      'delay-counter',
      getStoredDismissed() ? COPY.fabShow : COPY.fabHide,
      '<span style="display:inline-flex;width:18px;height:18px;">' + skullSvg() + '</span>',
      toggleCounter,
      { order: 45, closeFabOnClick: true }
    );
    updateFabLabel();
  }

  function start() {
    if (isDisabled()) return;

    loadModel().then(function() {
      createCounter();
      updateCounters();
      registerFabAction();
      rafId = window.requestAnimationFrame(tick);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }

  window.addEventListener('beforeunload', function() {
    if (rafId) window.cancelAnimationFrame(rafId);
  });
})();
