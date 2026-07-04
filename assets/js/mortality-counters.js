/**
 * Live mortality counters for the War on Disease manual.
 *
 * These counters estimate counterfactual schedule deaths: humans who die because
 * the disease-eradication date remains one day farther away than it would be
 * under immediate implementation of this plan or a better one.
 */

(function() {
  'use strict';

  var STORAGE_KEY = 'dih-delay-counter-dismissed';
  var DEFAULT_PUBLICATION_DATE = '2025-10-04';
  // Network-failure fallbacks only. Canonical values live in dih_models/parameters.py
  // (GLOBAL_DISEASE_DEATHS_DAILY, EVENTUALLY_AVOIDABLE_DEATH_PCT, DFDA_TRIAL_CAPACITY_PLUS_
  // EFFICACY_LAG_LIVES_SAVED/_DALYS) and are fetched from assets/json/parameters.json at runtime.
  var DEFAULTS = {
    diseaseDeathsDaily: 150000,
    eventuallyAvoidableDeathPct: 0.926,
    timelineLivesSaved: 10745517748.6,
    timelineDalys: 565243673351
  };

  var model = {
    diseaseDeathsDaily: DEFAULTS.diseaseDeathsDaily,
    eventuallyAvoidableDeathPct: DEFAULTS.eventuallyAvoidableDeathPct,
    timelineLivesSaved: DEFAULTS.timelineLivesSaved,
    timelineDalys: DEFAULTS.timelineDalys
  };

  var numberFormat = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });
  var compactFormat = new Intl.NumberFormat('en-US', {
    notation: 'compact',
    maximumFractionDigits: 2
  });

  var counterEl = null;
  var intervalId = null;

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
        model.timelineLivesSaved = pickParam(parameters, 'DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED', DEFAULTS.timelineLivesSaved);
        model.timelineDalys = pickParam(parameters, 'DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS', DEFAULTS.timelineDalys);
      })
      .catch(function() {
        model.diseaseDeathsDaily = DEFAULTS.diseaseDeathsDaily;
        model.eventuallyAvoidableDeathPct = DEFAULTS.eventuallyAvoidableDeathPct;
        model.timelineLivesSaved = DEFAULTS.timelineLivesSaved;
        model.timelineDalys = DEFAULTS.timelineDalys;
      });
  }

  function delayDeathsPerSecond() {
    return model.diseaseDeathsDaily * model.eventuallyAvoidableDeathPct / 86400;
  }

  function currentSincePublication() {
    var elapsedSeconds = Math.max(0, (Date.now() - getPublicationDate().getTime()) / 1000);
    return elapsedSeconds * delayDeathsPerSecond();
  }

  function format(value, compact) {
    return compact ? compactFormat.format(value) : numberFormat.format(value);
  }

  function textForValue(kind, compact) {
    if (kind === 'since-publication') return format(currentSincePublication(), compact);
    if (kind === 'per-day') return format(model.diseaseDeathsDaily * model.eventuallyAvoidableDeathPct, compact);
    if (kind === 'per-minute') return format(model.diseaseDeathsDaily * model.eventuallyAvoidableDeathPct / 1440, compact);
    if (kind === 'per-second') return format(delayDeathsPerSecond(), compact);
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

  function createCounter() {
    counterEl = document.getElementById('dih-delay-counter');
    if (counterEl) return;

    var hidden = getStoredDismissed();
    counterEl = document.createElement('aside');
    counterEl.id = 'dih-delay-counter';
    counterEl.className = 'dih-delay-counter' + (hidden ? ' dih-delay-counter-hidden' : '');
    counterEl.setAttribute('aria-label', 'Since an incentive-compatible way to end war and disease was discovered');
    counterEl.innerHTML =
      '<button class="dih-delay-counter-close" type="button" aria-label="Dismiss counter" title="Dismiss counter">' +
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>' +
      '</button>' +
      '<div class="dih-delay-counter-main">' +
        '<div class="dih-delay-counter-kicker">Since an incentive-compatible way to end war and disease was discovered</div>' +
        '<div class="dih-delay-counter-number"><span data-dih-delay-value="since-publication">0</span></div>' +
        '<div class="dih-delay-counter-copy">people will be unnecessarily tortured and brutally murdered by diseases. Every additional day we refrain from ending war and disease, about <span data-dih-delay-value="per-day" data-dih-delay-compact="true">139K</span> more join them.</div>' +
        '<div class="dih-delay-counter-note">If the math is wrong, fix it.</div>' +
      '</div>' +
      '<div class="dih-delay-counter-actions">' +
        '<a href="https://warondisease.org" target="_blank" rel="noopener">Please take 30 seconds to end war and disease</a>' +
      '</div>';

    document.body.appendChild(counterEl);
    document.body.classList.toggle('dih-delay-counter-visible', !hidden);

    counterEl.querySelector('.dih-delay-counter-close').addEventListener('click', function() {
      hideCounter();
    });
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
    var label = hidden ? 'Show body count' : 'Hide body count';
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
      getStoredDismissed() ? 'Show body count' : 'Hide body count',
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 16l3-5 4 3 4-8"/></svg>',
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
      intervalId = setInterval(updateCounters, 1000);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }

  window.addEventListener('beforeunload', function() {
    if (intervalId) clearInterval(intervalId);
  });
})();
