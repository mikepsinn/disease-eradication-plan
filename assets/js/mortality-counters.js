/**
 * Mortality scoreboard for the War on Disease manual.
 *
 * A sticky HUD counts counterfactual schedule deaths: humans who die
 * because the disease-eradication date remains one day farther away than it would
 * be under immediate implementation of this plan or a better one. Clicking the
 * scoreboard opens a fullscreen screen that explains the math.
 *
 * Embeddable on any website with a single tag:
 *   <script src="https://manual.warondisease.org/assets/js/mortality-counters.js" defer></script>
 * The script derives the site root from its own src, injects its stylesheet
 * (assets/css/scoreboard.css), and fetches live parameter values. Configure with:
 *   <meta name="dih-scoreboard-variant" content="minimal">  (bar layout; see VARIANTS)
 *   <meta name="dih-scoreboard-theme" content="arcade">  (visual theme; default is treaty)
 *   <meta name="dih-disable-features" content="delay-counter-hud">  (counters without the bar)
 * JS API: window.dihScoreboard.setVariant/setTheme/getVariant/getTheme/show/hide/openOverlay.
 * Conversion tracking: every interaction dispatches a 'dih-scoreboard' CustomEvent
 * on document with {action, variant, theme} in detail. Configurator + docs:
 * https://manual.warondisease.org/assets/scoreboard-embed.html
 */

(function() {
  'use strict';

  // Bump when this file or assets/css/scoreboard.css changes; it cache-busts
  // the injected stylesheet for embedders.
  var WIDGET_VERSION = '6.1.0';
  var SCRIPT_SRC = document.currentScript && document.currentScript.src ? document.currentScript.src : '';

  var VARIANTS = ['instrument-panel', 'sentence', 'tab', 'scoreline', 'minimal'];
  var DEFAULT_VARIANT = 'minimal';
  var THEMES = ['treaty', 'arcade'];
  var DEFAULT_THEME = 'treaty';

  var STORAGE_KEY = 'dih-delay-counter-dismissed';
  var DEFAULT_PUBLICATION_DATE = '2025-10-04';
  // Network-failure fallbacks only. Canonical values live in dih_models/parameters.py
  // (GLOBAL_DISEASE_DEATHS_DAILY, EVENTUALLY_AVOIDABLE_DEATH_PCT, GLOBAL_ANNUAL_DALY_BURDEN,
  // EVENTUALLY_AVOIDABLE_DALY_PCT, GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST,
  // GLOBAL_DISEASE_TOTAL_MARKET_COST_ANNUAL,
  // DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED/_DALYS)
  // and are fetched from assets/json/parameters.json at runtime.
  var DEFAULTS = {
    diseaseDeathsDaily: 150000,
    eventuallyAvoidableDeathPct: 0.926,
    dalyBurdenAnnual: 2880000000,
    eventuallyAvoidableDalyPct: 0.926,
    warCostAnnual: 11357100000000,
    diseaseCostAnnual: 14900000000000,
    timelineLivesSaved: 10745517748.6,
    timelineDalys: 565243673351,
    eventuallyAvoidableDiseaseDeathsDaily: 138941.7118512781,
    treatyReductionPct: 0.01,
    worldLeaderCount: 195,
    militaryToGovernmentClinicalTrialsRatio: 604.4444444444445,
    militarySpendingAnnual: 2720000000000,
    treatyAnnualFunding: 27200000000,
    trialCapacityMultiplier: 12.327913432666705,
    diseasesWithoutEffectiveTreatment: 6650,
    newDiseaseFirstTreatmentsPerYear: 15,
    statusQuoQueueClearanceYears: 443.3333333333333,
    dfdaQueueClearanceYears: 35.9617493872549,
    governmentClinicalTrialsSpendingAnnual: 4500000000,
    annualDiseaseDeaths: 55000000,
    annualTerrorismDeaths: 8300
  };

  var COPY = {
    scoreLabel: 'PLAYER 1: DISEASE',
    tabHeadRight: 'STILL RUNNING',
    sufferingLabel: 'HOURS OF UNNECESSARY SUFFERING',
    moneyLabel: 'DOLLARS WASTED ON WAR + DISEASE',
    highScoreLine: 'AWAITING PLAYER 2 SINCE 298,000 BC',
    ctaText: 'TAKE 30 SECONDS TO END WAR AND DISEASE',
    fabShow: 'Show the scoreboard',
    fabHide: 'Hide the scoreboard',
    closeHint: 'Hide the scoreboard',
    overlay: {
      closeText: 'RESUME IGNORING',
      mathHeading: 'THE MATH',
      sufferingHeading: 'UNNECESSARY SUFFERING',
      dollarsHeading: 'DOLLARS WASTED',
      ctaPrimary: 'TAKE 30 SECONDS TO END WAR AND DISEASE'
    }
  };

  var VOTE_URL = 'https://warondisease.org';
  var PARAM_PAGE = 'knowledge/appendix/parameters-and-calculations.html';
  var CALC_ANCHOR = 'knowledge/appendix/parameters-and-calculations.html#sec-global_eventually_avoidable_disease_deaths_daily';
  var KATEX_CSS = 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css';
  var KATEX_JS = 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js';

  var model = {};
  var parameterMetadata = null;
  var parameterMetadataPromise = null;
  var parameterDialogEl = null;
  var parameterDialogLastFocus = null;
  var katexPromise = null;

  var numberFormat = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });
  var oneDecimalFormat = new Intl.NumberFormat('en-US', { maximumFractionDigits: 1 });
  var wordCompactFormat = new Intl.NumberFormat('en-US', {
    notation: 'compact',
    compactDisplay: 'long',
    maximumFractionDigits: 1
  });
  var fullCurrencyFormat = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0
  });
  var compactCurrencyFormat = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    notation: 'compact',
    maximumFractionDigits: 2
  });
  var compactFormat = new Intl.NumberFormat('en-US', {
    notation: 'compact',
    maximumFractionDigits: 2
  });

  var counterEl = null;
  var overlayEl = null;
  var overlayOpenedAt = null;
  var rafId = null;
  var lastTick = 0;

  resetModelDefaults();

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
    // Embedders don't set the meta; derive the site root from this script's src.
    if (!offset && SCRIPT_SRC) {
      offset = SCRIPT_SRC.replace(/assets\/js\/mortality-counters\.js.*$/, '');
    }
    if (offset && offset.charAt(offset.length - 1) !== '/') offset += '/';
    return offset;
  }

  // The widget carries its own stylesheet so embedding is a single script tag.
  // Resolves once the CSS is loaded (or after a short timeout) so the bar
  // never renders unstyled.
  function injectStylesheet() {
    if (document.querySelector('link[href*="scoreboard.css"]')) {
      return Promise.resolve();
    }
    return new Promise(function(resolve) {
      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = getOffset() + 'assets/css/scoreboard.css?v=' + WIDGET_VERSION;
      var done = false;
      function finish() {
        if (!done) { done = true; resolve(); }
      }
      link.addEventListener('load', finish);
      link.addEventListener('error', finish);
      setTimeout(finish, 1500);
      document.head.appendChild(link);
    });
  }

  function getConfiguredVariant() {
    var meta = document.querySelector('meta[name="dih-scoreboard-variant"]');
    var value = meta && meta.content ? meta.content.trim() : '';
    return VARIANTS.indexOf(value) !== -1 ? value : DEFAULT_VARIANT;
  }

  function getConfiguredTheme() {
    var meta = document.querySelector('meta[name="dih-scoreboard-theme"]');
    var value = meta && meta.content ? meta.content.trim() : '';
    return THEMES.indexOf(value) !== -1 ? value : DEFAULT_THEME;
  }

  var currentVariant = DEFAULT_VARIANT;
  var currentVariantExplicit = false;
  var currentTheme = DEFAULT_THEME;
  var currentThemeExplicit = false;

  function themeClass(theme) {
    return 'dih-scoreboard-theme-' + theme;
  }

  // Conversion-tracking hook. Embedders (and our own analytics) listen with:
  //   document.addEventListener('dih-scoreboard', function(e) { ... e.detail ... });
  function emit(action, extra) {
    var detail = { action: action, variant: currentVariant, theme: currentTheme };
    if (extra) {
      for (var key in extra) {
        if (Object.prototype.hasOwnProperty.call(extra, key)) detail[key] = extra[key];
      }
    }
    document.dispatchEvent(new CustomEvent('dih-scoreboard', { detail: detail }));
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

  function hasDisableFlag(name) {
    var meta = document.querySelector('meta[name="dih-disable-features"]');
    if (!meta || !meta.content) return false;
    return meta.content.split(',').map(function(item) {
      return item.trim();
    }).indexOf(name) !== -1;
  }

  function isDisabled() {
    return hasDisableFlag('delay-counter');
  }

  // Embedders can run inline [data-dih-delay-value] counters without the
  // pinned scoreboard bar: <meta name="dih-disable-features" content="delay-counter-hud">
  function isHudDisabled() {
    return hasDisableFlag('delay-counter-hud');
  }

  function pickParam(parameters, name, fallback) {
    return parameters && parameters[name] && typeof parameters[name].value === 'number'
      ? parameters[name].value
      : fallback;
  }

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function loadParameterMetadata() {
    if (parameterMetadata) return Promise.resolve(parameterMetadata);
    if (window.dihScoreboardParameterMetadata) {
      parameterMetadata = window.dihScoreboardParameterMetadata;
      return Promise.resolve(parameterMetadata);
    }
    if (parameterMetadataPromise) return parameterMetadataPromise;

    parameterMetadataPromise = new Promise(function(resolve) {
      var script = document.createElement('script');
      script.src = getOffset() + 'assets/js/scoreboard-parameter-metadata.js?v=' + WIDGET_VERSION;
      script.async = true;
      script.onload = function() {
        parameterMetadata = window.dihScoreboardParameterMetadata || parameterMetadata;
        resolve(parameterMetadata);
      };
      script.onerror = function() {
        resolve(parameterMetadata);
      };
      document.head.appendChild(script);
    });
    return parameterMetadataPromise;
  }

  function loadKatex() {
    if (window.katex && typeof window.katex.render === 'function') return Promise.resolve(window.katex);
    if (katexPromise) return katexPromise;

    katexPromise = new Promise(function(resolve) {
      var css = document.querySelector('link[href="' + KATEX_CSS + '"]');
      var cssReady = Promise.resolve();
      if (!css) {
        cssReady = new Promise(function(done) {
          css = document.createElement('link');
          css.rel = 'stylesheet';
          css.href = KATEX_CSS;
          css.onload = done;
          css.onerror = done;
          document.head.appendChild(css);
        });
      }

      var script = document.querySelector('script[src="' + KATEX_JS + '"]');
      var jsReady = Promise.resolve();
      if (!script) {
        jsReady = new Promise(function(done) {
          script = document.createElement('script');
          script.src = KATEX_JS;
          script.async = true;
          script.onload = done;
          script.onerror = done;
          document.head.appendChild(script);
        });
      }

      Promise.all([cssReady, jsReady]).then(function() {
        resolve(window.katex && typeof window.katex.render === 'function' ? window.katex : null);
      });
    });
    return katexPromise;
  }

  function resetModelDefaults() {
    for (var key in DEFAULTS) {
      if (Object.prototype.hasOwnProperty.call(DEFAULTS, key)) model[key] = DEFAULTS[key];
    }
  }

  function loadModel() {
    if (window.location.protocol === 'file:') return Promise.resolve();

    return fetch(getOffset() + 'assets/json/parameters.json')
      .then(function(response) {
        if (!response.ok) return null;
        return response.json();
      })
      .then(function(json) {
        if (json && json.parameters) parameterMetadata = json;
        var parameters = json && json.parameters ? json.parameters : null;
        model.diseaseDeathsDaily = pickParam(parameters, 'GLOBAL_DISEASE_DEATHS_DAILY', DEFAULTS.diseaseDeathsDaily);
        model.eventuallyAvoidableDeathPct = pickParam(parameters, 'EVENTUALLY_AVOIDABLE_DEATH_PCT', DEFAULTS.eventuallyAvoidableDeathPct);
        model.dalyBurdenAnnual = pickParam(parameters, 'GLOBAL_ANNUAL_DALY_BURDEN', DEFAULTS.dalyBurdenAnnual);
        model.eventuallyAvoidableDalyPct = pickParam(parameters, 'EVENTUALLY_AVOIDABLE_DALY_PCT', DEFAULTS.eventuallyAvoidableDalyPct);
        model.warCostAnnual = pickParam(parameters, 'GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST', DEFAULTS.warCostAnnual);
        model.diseaseCostAnnual = pickParam(parameters, 'GLOBAL_DISEASE_TOTAL_MARKET_COST_ANNUAL', DEFAULTS.diseaseCostAnnual);
        model.timelineLivesSaved = pickParam(parameters, 'DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED', DEFAULTS.timelineLivesSaved);
        model.timelineDalys = pickParam(parameters, 'DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS', DEFAULTS.timelineDalys);
        model.eventuallyAvoidableDiseaseDeathsDaily = pickParam(parameters, 'GLOBAL_EVENTUALLY_AVOIDABLE_DISEASE_DEATHS_DAILY', DEFAULTS.eventuallyAvoidableDiseaseDeathsDaily);
        model.treatyReductionPct = pickParam(parameters, 'TREATY_REDUCTION_PCT', DEFAULTS.treatyReductionPct);
        model.worldLeaderCount = pickParam(parameters, 'CHAIN_WORLD_LEADER_COUNT', DEFAULTS.worldLeaderCount);
        model.militaryToGovernmentClinicalTrialsRatio = pickParam(parameters, 'MILITARY_TO_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO', DEFAULTS.militaryToGovernmentClinicalTrialsRatio);
        model.militarySpendingAnnual = pickParam(parameters, 'GLOBAL_MILITARY_SPENDING_ANNUAL_2024', DEFAULTS.militarySpendingAnnual);
        model.treatyAnnualFunding = pickParam(parameters, 'TREATY_ANNUAL_FUNDING', DEFAULTS.treatyAnnualFunding);
        model.trialCapacityMultiplier = pickParam(parameters, 'DFDA_TRIAL_CAPACITY_MULTIPLIER', DEFAULTS.trialCapacityMultiplier);
        model.diseasesWithoutEffectiveTreatment = pickParam(parameters, 'DISEASES_WITHOUT_EFFECTIVE_TREATMENT', DEFAULTS.diseasesWithoutEffectiveTreatment);
        model.newDiseaseFirstTreatmentsPerYear = pickParam(parameters, 'NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR', DEFAULTS.newDiseaseFirstTreatmentsPerYear);
        model.statusQuoQueueClearanceYears = pickParam(parameters, 'STATUS_QUO_QUEUE_CLEARANCE_YEARS', DEFAULTS.statusQuoQueueClearanceYears);
        model.dfdaQueueClearanceYears = pickParam(parameters, 'DFDA_QUEUE_CLEARANCE_YEARS', DEFAULTS.dfdaQueueClearanceYears);
        model.governmentClinicalTrialsSpendingAnnual = pickParam(parameters, 'GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL', DEFAULTS.governmentClinicalTrialsSpendingAnnual);
        model.annualDiseaseDeaths = pickParam(parameters, 'GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES', DEFAULTS.annualDiseaseDeaths);
        model.annualTerrorismDeaths = pickParam(parameters, 'GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS', DEFAULTS.annualTerrorismDeaths);
      })
      .catch(function() {
        resetModelDefaults();
      });
  }

  function delayDeathsPerDay() {
    return model.eventuallyAvoidableDiseaseDeathsDaily || model.diseaseDeathsDaily * model.eventuallyAvoidableDeathPct;
  }

  function delayDeathsPerSecond() {
    return delayDeathsPerDay() / 86400;
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

  // Annual economic cost of war ($11.4T) plus disease ($14.9T), spread per second.
  function wastedMoneyPerSecond() {
    return (model.warCostAnnual + model.diseaseCostAnnual) / 31557600;
  }

  function currentWastedMoneySince() {
    return elapsedSincePublication() * wastedMoneyPerSecond();
  }

  function format(value, compact) {
    return compact ? compactFormat.format(value) : numberFormat.format(value);
  }

  function formatMoney(value, compact) {
    return compact ? compactCurrencyFormat.format(value) : fullCurrencyFormat.format(value);
  }

  function formatRatio(value) {
    return format(value, false) + ':1';
  }

  function formatPercent(value) {
    return oneDecimalFormat.format(value * 100).replace(/\.0$/, '') + '%';
  }

  function formatMultiplier(value) {
    return oneDecimalFormat.format(value).replace(/\.0$/, '') + 'x';
  }

  function leaderCountText() {
    return format(model.worldLeaderCount, false);
  }

  function publicationDateText() {
    return getPublicationDate().toISOString().slice(0, 10);
  }

  function tabHeadLeftText() {
    return "YOUR SPECIES' TAB · OPEN SINCE " + publicationDateText() + ', THE DAY THE FIX WAS PUBLISHED';
  }

  function openHintText() {
    return leaderCountText() + " leaders have not completed their 30-second signing task. Tap to see the math.";
  }

  function sufferingYearsPerDay() {
    return model.dalyBurdenAnnual * model.eventuallyAvoidableDalyPct / 365.25;
  }

  function sufferingYearsPerSecond() {
    return sufferingHoursPerSecond() / 8766;
  }

  function sufferingDescText() {
    return 'Every day disease eradication is delayed adds ' +
      detailNumberHtml(wordCompactFormat.format(sufferingYearsPerDay()), 'GLOBAL_SCOREBOARD_SUFFERING_YEARS_PER_DAY') +
      " years of unnecessary suffering. That's " +
      detailNumberHtml(format(sufferingYearsPerSecond(), false), 'GLOBAL_SCOREBOARD_SUFFERING_YEARS_PER_SECOND') +
      ' years per second.';
  }

  function dollarsDescHtml(offset) {
    return 'Cost of delay since the 1% Treaty was proposed.';
  }

  function paramHref(offset, parameterName) {
    return offset + PARAM_PAGE + '#sec-' + parameterName.toLowerCase();
  }

  function detailButtonHtml(text, attrName, attrValue) {
    return '<button class="dih-arcade-source-number" type="button" ' + attrName + '="' +
      escapeHtml(attrValue) + '" title="Show source and math">' + text + '</button>';
  }

  function sourceNumberHtml(offset, text, parameterName) {
    return detailButtonHtml(text, 'data-dih-param', parameterName);
  }

  function detailNumberHtml(text, detailId) {
    return detailButtonHtml(text, 'data-dih-detail', detailId);
  }

  function ctaPrimaryHtml() {
    return COPY.overlay.ctaPrimary;
  }

  function scoreUnitLine() {
    return 'Humans will be unnecessarily brutally tortured and murdered by disease because disease eradication is delayed while ' +
      leaderCountText() + ' leaders have not completed their 30-second task of signing the ' +
      formatPercent(model.treatyReductionPct) + ' Treaty';
  }

  function scoreUnitLineShort() {
    return 'murdered because disease eradication is delayed';
  }

  function kickerText() {
    return 'EVERY DAY WE DELAY DISEASE ERADICATION, DISEASE SCORES ' + format(delayDeathsPerDay(), false);
  }

  function scoreUnitLineHtml(offset) {
    return 'Humans will be unnecessarily brutally tortured and murdered by disease because disease eradication is delayed while ' +
      escapeHtml(leaderCountText()) +
      ' leaders have not completed their ' +
      '30-second' +
      ' task of signing the ' +
      escapeHtml(formatPercent(model.treatyReductionPct)) + ' Treaty';
  }

  function deathSubHtml(offset) {
    return 'Every day we delay disease eradication: ' +
      sourceNumberHtml(offset, format(delayDeathsPerDay(), false), 'GLOBAL_EVENTUALLY_AVOIDABLE_DISEASE_DEATHS_DAILY') +
      ' lives.';
  }

  function textForValue(kind, compact) {
    if (kind === 'since-publication') return format(currentSincePublication(), compact);
    if (kind === 'per-day') return format(delayDeathsPerDay(), compact);
    if (kind === 'per-minute') return format(delayDeathsPerDay() / 1440, compact);
    if (kind === 'per-second') return compactFormat.format(delayDeathsPerSecond());
    if (kind === 'suffering-hours-since-publication') return format(elapsedSincePublication() * sufferingHoursPerSecond(), compact);
    if (kind === 'suffering-hours-per-second') return format(sufferingHoursPerSecond(), compact);
    // Full digits by default: a wasted-dollars counter should visibly count.
    // "$19.76T" is a statistic; "$19,762,834,551,203" climbing is a meter running.
    if (kind === 'money-since-publication') return formatMoney(currentWastedMoneySince(), compact);
    if (kind === 'money-per-second') return formatMoney(wastedMoneyPerSecond(), compact);
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
    counterEl.className = 'dih-delay-counter dih-arcade-variant-' + currentVariant + ' ' + themeClass(currentTheme) + (hidden ? ' dih-delay-counter-hidden' : '');
    counterEl.setAttribute('aria-label', 'Live scoreboard: avoidable disease deaths since ' + publicationDateText());
    counterEl.innerHTML =
      '<span class="dih-arcade-tab-head" role="button" tabindex="0">' +
        '<span>' + tabHeadLeftText() + '</span><span>' + COPY.tabHeadRight + '</span>' +
      '</span>' +
      '<button class="dih-arcade-open" type="button" title="' + openHintText() + '">' +
        '<span class="dih-arcade-skull">' + skullSvg() + '</span>' +
        '<span class="dih-arcade-score-block">' +
          '<span class="dih-arcade-kicker">' + kickerText() + '</span>' +
          '<span class="dih-arcade-score"><span class="dih-arcade-score-label">' + COPY.scoreLabel + '</span> <span data-dih-delay-value="since-publication">0</span></span>' +
          '<span class="dih-arcade-unitline">' + scoreUnitLine() + '</span>' +
          '<span class="dih-arcade-unitline-short">' + scoreUnitLineShort() + '</span>' +
        '</span>' +
        '<span class="dih-arcade-vs-block">' +
          '<span class="dih-arcade-vs-tag">VS</span>' +
          '<span class="dih-arcade-hum"><span class="dih-arcade-hum-team">HUMANITY</span><span class="dih-arcade-hum-pts">0</span></span>' +
        '</span>' +
        '<span class="dih-arcade-suffer-block">' +
          '<span class="dih-arcade-suffer-label">' + COPY.sufferingLabel + '</span>' +
          '<span class="dih-arcade-suffer" data-dih-delay-value="suffering-hours-since-publication">0</span>' +
        '</span>' +
        '<span class="dih-arcade-money-block">' +
          '<span class="dih-arcade-money-label">' + COPY.moneyLabel + '</span>' +
          '<span class="dih-arcade-money" data-dih-delay-value="money-since-publication">0</span>' +
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
    var tabHead = counterEl.querySelector('.dih-arcade-tab-head');
    tabHead.addEventListener('click', openOverlay);
    tabHead.addEventListener('keydown', function(event) {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); openOverlay(); }
    });
    counterEl.querySelector('.dih-arcade-cta').addEventListener('click', function() {
      emit('cta-clicked', { source: 'bar' });
    });

    if (!hidden) emit('bar-shown', null);
  }

  function sectionHtml(heading, bodyHtml) {
    return '<section class="dih-arcade-section">' +
      '<h3 class="dih-arcade-heading">' + heading + '</h3>' + bodyHtml + '</section>';
  }

  function barChartHtml(heading, rows) {
    var html = '<section class="dih-arcade-section dih-arcade-bar-chart">' +
      '<h3 class="dih-arcade-heading">' + heading + '</h3>';
    for (var i = 0; i < rows.length; i++) {
      var minW = rows[i][2] < 1 ? 'min-width:2px;' : '';
      html += '<div class="dih-arcade-bar-row">' +
        '<span class="dih-arcade-bar-label">' + rows[i][0] + '</span>' +
        '<div class="dih-arcade-bar-track">' +
          '<div class="dih-arcade-bar-fill' + (i === 0 ? ' dih-arcade-bar-fill-primary' : '') + '" style="width:' + rows[i][2] + '%;' + minW + '"></div>' +
        '</div>' +
        '<span class="dih-arcade-bar-value">' + rows[i][1] + '</span>' +
      '</div>';
    }
    html += '</section>';
    return html;
  }

  function titleFromParameterName(name) {
    return String(name || 'Parameter')
      .toLowerCase()
      .replace(/_/g, ' ')
      .replace(/\b\w/g, function(ch) { return ch.toUpperCase(); });
  }

  function getMetadataParam(paramName) {
    return parameterMetadata && parameterMetadata.parameters
      ? parameterMetadata.parameters[paramName]
      : null;
  }

  function citationForParam(param) {
    if (!param || !param.sourceRef || !parameterMetadata || !parameterMetadata.citations) return null;
    return parameterMetadata.citations[param.sourceRef] || null;
  }

  function syntheticDetail(detailId, displayText) {
    var commonDeathInputs = ['GLOBAL_EVENTUALLY_AVOIDABLE_DISEASE_DEATHS_DAILY'];
    if (detailId === 'GLOBAL_SCOREBOARD_DEATHS_SINCE_PUBLICATION') {
      return {
        displayName: 'Disease Score Since Publication',
        formatted: displayText,
        description: 'Live count of eventually avoidable disease deaths accumulated since the scoreboard publication date.',
        sourceType: 'calculated',
        formula: 'GLOBAL_EVENTUALLY_AVOIDABLE_DISEASE_DEATHS_DAILY × elapsed seconds since publication ÷ 86,400',
        latex: '\\begin{gathered}\nDeaths_{score} = \\frac{Deaths_{avoid,daily} \\times t_{elapsed}}{86{,}400}\n\\end{gathered}',
        inputs: commonDeathInputs
      };
    }
    if (detailId === 'GLOBAL_SCOREBOARD_DEATHS_SINCE_OPENED') {
      return {
        displayName: 'Disease Score Since Opening',
        formatted: displayText,
        description: 'Live count of eventually avoidable disease deaths accumulated since this explanation screen opened.',
        sourceType: 'calculated',
        formula: 'GLOBAL_EVENTUALLY_AVOIDABLE_DISEASE_DEATHS_DAILY × elapsed seconds since opening ÷ 86,400',
        latex: '\\begin{gathered}\nDeaths_{opened} = \\frac{Deaths_{avoid,daily} \\times t_{opened}}{86{,}400}\n\\end{gathered}',
        inputs: commonDeathInputs
      };
    }
    if (detailId === 'GLOBAL_SCOREBOARD_SUFFERING_HOURS_SINCE_PUBLICATION') {
      return {
        displayName: 'Suffering Hours Since Publication',
        formatted: displayText + ' hours',
        description: 'Live counter for avoidable disease burden accumulated since the scoreboard publication date.',
        sourceType: 'calculated',
        formula: 'GLOBAL_ANNUAL_DALY_BURDEN × EVENTUALLY_AVOIDABLE_DALY_PCT × 8,766 × elapsed seconds ÷ 31,557,600',
        latex: '\\begin{gathered}\nHours_{suffering} = \\frac{DALYs_{annual} \\times Pct_{avoid,DALY} \\times 8{,}766 \\times t_{elapsed}}{31{,}557{,}600}\n\\end{gathered}',
        inputs: ['GLOBAL_ANNUAL_DALY_BURDEN', 'EVENTUALLY_AVOIDABLE_DALY_PCT']
      };
    }
    if (detailId === 'GLOBAL_SCOREBOARD_SUFFERING_YEARS_PER_DAY') {
      return {
        displayName: 'Avoidable Suffering Years Per Day',
        formatted: displayText + ' years/day',
        description: 'Daily avoidable disease burden used by the scoreboard.',
        sourceType: 'calculated',
        formula: 'GLOBAL_ANNUAL_DALY_BURDEN × EVENTUALLY_AVOIDABLE_DALY_PCT ÷ 365.25',
        latex: '\\begin{gathered}\nYears_{suffering,daily} = \\frac{DALYs_{annual} \\times Pct_{avoid,DALY}}{365.25}\n\\end{gathered}',
        inputs: ['GLOBAL_ANNUAL_DALY_BURDEN', 'EVENTUALLY_AVOIDABLE_DALY_PCT']
      };
    }
    if (detailId === 'GLOBAL_SCOREBOARD_SUFFERING_YEARS_PER_SECOND') {
      return {
        displayName: 'Avoidable Suffering Years Per Second',
        formatted: displayText + ' years/second',
        description: 'Per-second avoidable disease burden used by the scoreboard.',
        sourceType: 'calculated',
        formula: 'GLOBAL_ANNUAL_DALY_BURDEN × EVENTUALLY_AVOIDABLE_DALY_PCT ÷ 31,557,600',
        latex: '\\begin{gathered}\nYears_{suffering,second} = \\frac{DALYs_{annual} \\times Pct_{avoid,DALY}}{31{,}557{,}600}\n\\end{gathered}',
        inputs: ['GLOBAL_ANNUAL_DALY_BURDEN', 'EVENTUALLY_AVOIDABLE_DALY_PCT']
      };
    }
    if (detailId === 'GLOBAL_SCOREBOARD_WAR_DISEASE_MARKET_COST_SINCE_PUBLICATION') {
      return {
        displayName: 'Delay Cost',
        formatted: displayText,
        description: 'Cost of delay since the 1% Treaty was proposed.',
        sourceType: 'calculated',
        formula: '(GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST + GLOBAL_DISEASE_TOTAL_MARKET_COST_ANNUAL) × elapsed seconds ÷ 31,557,600',
        latex: '\\begin{gathered}\nCost_{delay} = \\frac{(Cost_{war,annual} + Cost_{disease,annual}) \\times t_{elapsed}}{31{,}557{,}600}\n\\end{gathered}',
        inputs: ['GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST', 'GLOBAL_DISEASE_TOTAL_MARKET_COST_ANNUAL']
      };
    }
    return {
      displayName: titleFromParameterName(detailId),
      formatted: displayText,
      description: 'Scoreboard detail.',
      sourceType: 'calculated',
      formula: null,
      inputs: []
    };
  }

  function formatRangeValue(value, unit) {
    if (unit && unit.indexOf('USD') === 0) return formatMoney(value, true);
    if ((unit === 'percent' || unit === 'percentage' || unit === 'rate') && Math.abs(value) <= 1) {
      return formatPercent(value);
    }
    return format(value, true);
  }

  function confidenceIntervalHtml(param) {
    if (!param || !param.confidenceInterval || param.confidenceInterval.length !== 2) return '';
    return '<div class="dih-param-range">' +
      '<strong>Estimated range</strong><span>' +
      escapeHtml(formatRangeValue(param.confidenceInterval[0], param.unit)) + ' to ' +
      escapeHtml(formatRangeValue(param.confidenceInterval[1], param.unit)) +
      ' (95% confidence)</span></div>';
  }

  function modalIconHtml(type) {
    if (type === 'input') {
      return '<span class="dih-param-icon dih-param-icon-input" aria-hidden="true"><svg viewBox="0 0 16 16" focusable="false">' +
        '<path d="M2 8h8"></path><path d="M7 5l3 3-3 3"></path><path d="M12 3h2v10h-2"></path>' +
        '</svg></span>';
    }
    return '<span class="dih-param-icon dih-param-icon-link" aria-hidden="true"><svg viewBox="0 0 16 16" focusable="false">' +
      '<path d="M6.5 4H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9.5"></path>' +
      '<path d="M9 2h5v5"></path><path d="M8 8l6-6"></path>' +
      '</svg></span>';
  }

  function inputButtonsHtml(inputs) {
    if (!inputs || !inputs.length) return '';
    var html = '<div class="dih-param-inputs"><strong>Inputs</strong><div>';
    for (var i = 0; i < inputs.length; i++) {
      var title = titleFromParameterName(inputs[i]);
      html += '<button type="button" class="dih-param-chip dih-param-input-chip" data-dih-param="' +
        escapeHtml(inputs[i]) + '" title="Open input parameter" aria-label="Open input parameter: ' +
        escapeHtml(title) + '">' + modalIconHtml('input') + '<span>' + escapeHtml(title) + '</span></button>';
    }
    html += '</div></div>';
    return html;
  }

  function referenceActionLinkHtml(href, label) {
    return '<a class="dih-param-action-link" href="' + escapeHtml(href) +
      '" target="_blank" rel="noopener" title="Open ' + escapeHtml(label) +
      ' in a new tab" aria-label="Open ' + escapeHtml(label) +
      ' in a new tab">' + modalIconHtml('link') + '<span>' + escapeHtml(label) + '</span></a>';
  }

  function referenceActionsHtml(paramName, param) {
    var offset = getOffset();
    var html = '<div class="dih-param-actions">';
    if (paramName) {
      html += referenceActionLinkHtml(param.calculationUrl || paramHref(offset, paramName), 'Calculation');
    }
    if (param && param.chapterUrl) {
      html += referenceActionLinkHtml(param.chapterUrl, 'Chapter');
    }
    if (param && param.sourceUrl) {
      html += referenceActionLinkHtml(param.sourceUrl, 'Source');
    }
    html += '</div>';
    return html;
  }

  function citationHtml(citation) {
    if (!citation || !citation.title) return '';
    var parts = [escapeHtml(citation.title)];
    if (citation.author) parts.push(escapeHtml(citation.author));
    if (citation.year) parts.push(escapeHtml(citation.year));
    if (citation.source) parts.push(escapeHtml(citation.source));
    return '<p class="dih-param-citation">' + parts.join(' | ') + '</p>';
  }

  function readLatexGroup(text, start) {
    if (text.charAt(start) !== '{') return null;
    var depth = 0;
    var value = '';
    for (var i = start; i < text.length; i++) {
      var ch = text.charAt(i);
      if (ch === '{') {
        if (depth > 0) value += ch;
        depth += 1;
      } else if (ch === '}') {
        depth -= 1;
        if (depth === 0) return { value: value, next: i + 1 };
        value += ch;
      } else {
        value += ch;
      }
    }
    return null;
  }

  function replaceLatexFractions(text) {
    var output = '';
    var i = 0;
    while (i < text.length) {
      if (text.slice(i, i + 6) === '\\frac{') {
        var numerator = readLatexGroup(text, i + 5);
        var denominator = numerator ? readLatexGroup(text, numerator.next) : null;
        if (numerator && denominator) {
          output += '(' + replaceLatexFractions(numerator.value) + ') / (' +
            replaceLatexFractions(denominator.value) + ')';
          i = denominator.next;
          continue;
        }
      }
      output += text.charAt(i);
      i += 1;
    }
    return output;
  }

  function readableLatexFallback(latex) {
    return replaceLatexFractions(latex)
      .replace(/\\begin\{[^}]+\}/g, '')
      .replace(/\\end\{[^}]+\}/g, '')
      .replace(/\\text\{([^}]*)\}/g, '$1')
      .replace(/\\\\\[[^\]]+\]/g, '\n')
      .replace(/\\\\/g, '\n')
      .replace(/\\times/g, '×')
      .replace(/\\%/g, '%')
      .replace(/\\\$/g, '$')
      .replace(/\{,\}/g, ',')
      .replace(/\\left/g, '')
      .replace(/\\right/g, '')
      .replace(/[{}]/g, '')
      .replace(/[ \t]+\n/g, '\n')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
  }

  function equationHtml(detail) {
    if (detail.latex) {
      var renderable = detail.latex.length <= 520 && detail.latex.indexOf('\\text{where') === -1;
      var fallbackText = renderable ? detail.latex : readableLatexFallback(detail.latex);
      return '<div class="dih-param-equation' + (renderable ? '' : ' dih-param-equation-raw-only') + '"><strong>Equation</strong>' +
        (renderable ? '<div class="dih-param-equation-render" aria-hidden="true"></div>' : '') +
        '<pre class="dih-param-equation-raw">' + escapeHtml(fallbackText) + '</pre></div>';
    }
    if (detail.formula) {
      return '<div class="dih-param-formula"><strong>Formula</strong><code>' +
        escapeHtml(detail.formula) + '</code></div>';
    }
    return '';
  }

  function renderLatexInCard(card) {
    var blocks = card.querySelectorAll('.dih-param-equation');
    if (!blocks.length) return;
    loadKatex().then(function(katex) {
      if (!katex) return;
      for (var i = 0; i < blocks.length; i++) {
        var block = blocks[i];
        if (block.classList.contains('dih-param-equation-raw-only')) continue;
        var raw = block.querySelector('.dih-param-equation-raw');
        var target = block.querySelector('.dih-param-equation-render');
        if (!raw || !target) continue;
        katex.render(raw.textContent, target, {
          displayMode: true,
          throwOnError: false,
          strict: 'ignore',
          trust: false
        });
        target.scrollLeft = 0;
        block.classList.add('dih-param-equation-rendered');
      }
    });
  }

  function parameterDetailHtml(paramName, detailId, displayText) {
    var param = paramName ? getMetadataParam(paramName) : null;
    var detail = param || syntheticDetail(detailId, displayText);
    var citation = citationForParam(param);
    var title = detail.displayName || titleFromParameterName(paramName || detailId);
    var value = detail.formatted || displayText;
    var sourceType = detail.sourceType ? '<span>' + escapeHtml(detail.sourceType) + '</span>' : '';
    var confidence = detail.confidence ? '<span>' + escapeHtml(detail.confidence) + ' confidence</span>' : '';
    var badges = sourceType || confidence ? '<div class="dih-param-badges">' + sourceType + confidence + '</div>' : '';
    var description = detail.description ? '<p class="dih-param-description">' + escapeHtml(detail.description) + '</p>' : '';
    var equation = equationHtml(detail);

    return '<div class="dih-param-modal-head">' +
        '<h3>' + escapeHtml(title) + '</h3>' +
        '<button type="button" class="dih-param-modal-close" aria-label="Close">×</button>' +
      '</div>' +
      '<div class="dih-param-modal-body">' +
        '<div class="dih-param-value">' + escapeHtml(value) + '</div>' +
        badges +
        description +
        confidenceIntervalHtml(detail) +
        equation +
        inputButtonsHtml(detail.inputs) +
        referenceActionsHtml(paramName, detail) +
        citationHtml(citation) +
      '</div>';
  }

  function createParameterDialog() {
    if (parameterDialogEl) return;
    parameterDialogEl = document.createElement('div');
    parameterDialogEl.className = 'dih-param-modal ' + themeClass(currentTheme);
    parameterDialogEl.setAttribute('role', 'dialog');
    parameterDialogEl.setAttribute('aria-modal', 'true');
    parameterDialogEl.setAttribute('aria-label', 'Source and math');
    parameterDialogEl.innerHTML = '<div class="dih-param-modal-card"></div>';
    document.body.appendChild(parameterDialogEl);
    parameterDialogEl.addEventListener('click', function(event) {
      if (event.target === parameterDialogEl) closeParameterDialog();
      var input = event.target.closest && event.target.closest('.dih-param-chip');
      if (input) {
        event.preventDefault();
        event.stopPropagation();
        openParameterDialog(input);
      }
    });
  }

  function openParameterDialog(trigger) {
    parameterDialogLastFocus = trigger;
    createParameterDialog();
    var paramName = trigger.getAttribute('data-dih-param');
    var detailId = trigger.getAttribute('data-dih-detail');
    var displayText = trigger.textContent.trim();
    var card = parameterDialogEl.querySelector('.dih-param-modal-card');
    card.innerHTML = '<div class="dih-param-modal-loading">Loading source and math...</div>';
    parameterDialogEl.classList.add('dih-param-modal-visible');

    loadParameterMetadata().then(function() {
      card.innerHTML = parameterDetailHtml(paramName, detailId, displayText);
      card.querySelector('.dih-param-modal-close').addEventListener('click', closeParameterDialog);
      renderLatexInCard(card);
      card.querySelector('.dih-param-modal-close').focus();
    });
  }

  function closeParameterDialog() {
    if (!parameterDialogEl) return;
    parameterDialogEl.classList.remove('dih-param-modal-visible');
    if (parameterDialogLastFocus && parameterDialogLastFocus.focus) parameterDialogLastFocus.focus();
    parameterDialogLastFocus = null;
  }

  function handleParameterTriggerClick(event) {
    var target = event.target.closest && event.target.closest('[data-dih-param], [data-dih-detail]');
    if (!target) return;
    event.preventDefault();
    event.stopPropagation();
    openParameterDialog(target);
  }

  function createOverlay() {
    if (overlayEl) return;
    var o = COPY.overlay;
    var offset = getOffset();

    var ratioText = formatRatio(model.militaryToGovernmentClinicalTrialsRatio);
    var treatyPercent = formatPercent(model.treatyReductionPct);
    var trialMultiplier = formatMultiplier(model.trialCapacityMultiplier);
    var statusQuoYears = format(model.statusQuoQueueClearanceYears, false);
    var dfdaYears = format(model.dfdaQueueClearanceYears, false);
    var mathSteps = [
      [sourceNumberHtml(offset, ratioText, 'MILITARY_TO_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO'), 'what governments spend on the capacity for mass murder vs clinical trials'],
      [sourceNumberHtml(offset, formatMoney(model.militarySpendingAnnual, true), 'GLOBAL_MILITARY_SPENDING_ANNUAL_2024'), 'capacity for mass murder per year'],
      ['× ' + escapeHtml(treatyPercent), '= ' + sourceNumberHtml(offset, formatMoney(model.treatyAnnualFunding, true), 'TREATY_ANNUAL_FUNDING') + ' for clinical trials'],
      [sourceNumberHtml(offset, '= ' + trialMultiplier, 'DFDA_TRIAL_CAPACITY_MULTIPLIER'), 'more trials than currently exist'],
      [sourceNumberHtml(offset, format(model.diseasesWithoutEffectiveTreatment, false), 'DISEASES_WITHOUT_EFFECTIVE_TREATMENT'), 'diseases have no treatment'],
      ['÷ ' + sourceNumberHtml(offset, format(model.newDiseaseFirstTreatmentsPerYear, false) + '/yr', 'NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR'), 'current rate of first treatments'],
      [sourceNumberHtml(offset, '= ' + statusQuoYears + ' yrs', 'STATUS_QUO_QUEUE_CLEARANCE_YEARS'), 'to clear the queue at this pace'],
      [sourceNumberHtml(offset, statusQuoYears, 'STATUS_QUO_QUEUE_CLEARANCE_YEARS') + ' ÷ ' +
        sourceNumberHtml(offset, trialMultiplier, 'DFDA_TRIAL_CAPACITY_MULTIPLIER'), ''],
      [sourceNumberHtml(offset, '= ' + dfdaYears + ' yrs', 'DFDA_QUEUE_CLEARANCE_YEARS'), 'if they sign']
    ];
    var mathHtml = '<div class="dih-arcade-math">';
    for (var i = 0; i < mathSteps.length; i++) {
      mathHtml += '<div class="dih-arcade-math-step">' +
        '<span class="dih-arcade-math-val">' + mathSteps[i][0] + '</span>' +
        (mathSteps[i][1] ? '<span class="dih-arcade-math-desc">' + mathSteps[i][1] + '</span>' : '') +
        '</div>';
    }
    mathHtml += '</div>';

    var terrorismBarWidth = model.annualDiseaseDeaths > 0 ? model.annualTerrorismDeaths / model.annualDiseaseDeaths * 100 : 0;
    var clinicalTrialsBarWidth = model.militarySpendingAnnual > 0
      ? model.governmentClinicalTrialsSpendingAnnual / model.militarySpendingAnnual * 100
      : 0;

    var barsHtml =
      barChartHtml('KILLED PER YEAR', [
        ['Disease', sourceNumberHtml(offset, format(model.annualDiseaseDeaths, false), 'GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES'), 100],
        ['Terrorism', sourceNumberHtml(offset, format(model.annualTerrorismDeaths, false), 'GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS'), terrorismBarWidth]
      ]) +
      barChartHtml('GOVERNMENT SPENDING PER YEAR', [
        ['Capacity for mass murder', sourceNumberHtml(offset, formatMoney(model.militarySpendingAnnual, false), 'GLOBAL_MILITARY_SPENDING_ANNUAL_2024'), 100],
        ['Clinical trials', sourceNumberHtml(offset, formatMoney(model.governmentClinicalTrialsSpendingAnnual, false), 'GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL'), clinicalTrialsBarWidth]
      ]);

    overlayEl = document.createElement('div');
    overlayEl.id = 'dih-arcade-overlay';
    overlayEl.className = 'dih-arcade-overlay ' + themeClass(currentTheme);
    overlayEl.setAttribute('role', 'dialog');
    overlayEl.setAttribute('aria-modal', 'true');
    overlayEl.setAttribute('aria-label', 'The math behind the scoreboard');
    overlayEl.innerHTML =
      '<button class="dih-arcade-overlay-close" type="button">✕ ' + o.closeText + '</button>' +
      '<div class="dih-arcade-screen">' +
        '<div class="dih-arcade-skull-big">' + skullSvg() + '</div>' +
        '<div class="dih-arcade-death-count">' +
          detailNumberHtml('<span class="dih-arcade-pts" data-dih-delay-value="since-publication">0</span>', 'GLOBAL_SCOREBOARD_DEATHS_SINCE_PUBLICATION') +
        '</div>' +
        '<p class="dih-arcade-subtitle">' + scoreUnitLineHtml(offset) + '</p>' +
        '<p class="dih-arcade-death-sub">' + deathSubHtml(offset) + '</p>' +
        sectionHtml(o.mathHeading, mathHtml) +
        barsHtml +
        '<section class="dih-arcade-section">' +
          '<h3 class="dih-arcade-heading">' + o.sufferingHeading + '</h3>' +
          '<div class="dih-arcade-sufferline">' +
            detailNumberHtml('<span class="dih-arcade-suffer" data-dih-delay-value="suffering-hours-since-publication">0</span>', 'GLOBAL_SCOREBOARD_SUFFERING_HOURS_SINCE_PUBLICATION') +
            '<span class="dih-arcade-suffer-unit">hours</span>' +
          '</div>' +
          '<p>' + sufferingDescText() + '</p>' +
        '</section>' +
        '<section class="dih-arcade-section">' +
          '<h3 class="dih-arcade-heading">' + o.dollarsHeading + '</h3>' +
          '<div class="dih-arcade-sufferline">' +
            detailNumberHtml('<span class="dih-arcade-money" data-dih-delay-value="money-since-publication">$0</span>', 'GLOBAL_SCOREBOARD_WAR_DISEASE_MARKET_COST_SINCE_PUBLICATION') +
          '</div>' +
          '<p>' + dollarsDescHtml(offset) + '</p>' +
        '</section>' +
        '<div class="dih-arcade-ctas">' +
          '<a class="dih-arcade-cta-primary" href="' + VOTE_URL + '" target="_blank" rel="noopener">' + ctaPrimaryHtml() + '</a>' +
        '</div>' +
      '</div>';

    document.body.appendChild(overlayEl);
    overlayEl.addEventListener('click', handleParameterTriggerClick);
    overlayEl.querySelector('.dih-arcade-overlay-close').addEventListener('click', closeOverlay);
    overlayEl.querySelector('.dih-arcade-cta-primary').addEventListener('click', function() {
      emit('cta-clicked', { source: 'overlay' });
    });
    document.addEventListener('keydown', function(event) {
      if (event.key === 'Escape' && parameterDialogEl && parameterDialogEl.classList.contains('dih-param-modal-visible')) {
        closeParameterDialog();
        return;
      }
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
    emit('overlay-opened', null);
  }

  function closeOverlay() {
    if (!overlayEl) return;
    var secondsOpen = overlayOpenedAt === null ? 0 : Math.round((Date.now() - overlayOpenedAt) / 1000);
    overlayEl.classList.remove('dih-arcade-overlay-visible');
    document.body.classList.remove('dih-arcade-overlay-open');
    closeParameterDialog();
    overlayOpenedAt = null;
    emit('overlay-closed', { secondsOpen: secondsOpen });
  }

  function hideCounter() {
    if (!counterEl) return;
    counterEl.classList.add('dih-delay-counter-hidden');
    document.body.classList.remove('dih-delay-counter-visible');
    setStoredDismissed(true);
    updateFabLabel();
    emit('bar-dismissed', null);
  }

  function showCounter() {
    if (!counterEl) createCounter();
    counterEl.classList.remove('dih-delay-counter-hidden');
    document.body.classList.add('dih-delay-counter-visible');
    setStoredDismissed(false);
    updateCounters();
    updateFabLabel();
    emit('bar-shown', null);
  }

  function setVariant(name) {
    if (VARIANTS.indexOf(name) === -1) return currentVariant;
    if (name === currentVariant) {
      currentVariantExplicit = true;
      return currentVariant;
    }
    if (counterEl) {
      counterEl.classList.remove('dih-arcade-variant-' + currentVariant);
      counterEl.classList.add('dih-arcade-variant-' + name);
    }
    currentVariant = name;
    currentVariantExplicit = true;
    emit('variant-changed', null);
    return currentVariant;
  }

  function setTheme(name) {
    if (THEMES.indexOf(name) === -1) return currentTheme;
    if (name === currentTheme) {
      currentThemeExplicit = true;
      return currentTheme;
    }
    if (counterEl) {
      counterEl.classList.remove(themeClass(currentTheme));
      counterEl.classList.add(themeClass(name));
    }
    if (overlayEl) {
      overlayEl.classList.remove(themeClass(currentTheme));
      overlayEl.classList.add(themeClass(name));
    }
    if (parameterDialogEl) {
      parameterDialogEl.classList.remove(themeClass(currentTheme));
      parameterDialogEl.classList.add(themeClass(name));
    }
    currentTheme = name;
    currentThemeExplicit = true;
    emit('theme-changed', null);
    return currentTheme;
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

    if (!currentVariantExplicit) currentVariant = getConfiguredVariant();
    if (!currentThemeExplicit) currentTheme = getConfiguredTheme();

    Promise.all([injectStylesheet(), loadModel()]).then(function() {
      if (!isHudDisabled()) {
        createCounter();
        registerFabAction();
      }
      updateCounters();
      rafId = window.requestAnimationFrame(tick);
    });
  }

  // Public API for the configurator page and embedders.
  window.dihScoreboard = {
    variants: VARIANTS.slice(),
    themes: THEMES.slice(),
    defaultVariant: DEFAULT_VARIANT,
    defaultTheme: DEFAULT_THEME,
    version: WIDGET_VERSION,
    setVariant: setVariant,
    setTheme: setTheme,
    getVariant: function() { return currentVariant; },
    getTheme: function() { return currentTheme; },
    show: showCounter,
    hide: hideCounter,
    openOverlay: openOverlay,
    closeOverlay: closeOverlay
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }

  window.addEventListener('beforeunload', function() {
    if (rafId) window.cancelAnimationFrame(rafId);
  });
})();
