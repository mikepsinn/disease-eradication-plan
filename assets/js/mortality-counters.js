/**
 * Arcade mortality scoreboard for the War on Disease manual.
 *
 * A sticky video-game HUD counts counterfactual schedule deaths: humans who die
 * because the disease-eradication date remains one day farther away than it would
 * be under immediate implementation of this plan or a better one. Clicking the
 * scoreboard opens a fullscreen CRT screen that explains the math.
 *
 * Embeddable on any website with a single tag:
 *   <script src="https://manual.warondisease.org/assets/js/mortality-counters.js" defer></script>
 * The script derives the site root from its own src, injects its stylesheet
 * (assets/css/scoreboard.css), and fetches live parameter values. Configure with:
 *   <meta name="dih-scoreboard-variant" content="minimal">  (bar design; see VARIANTS)
 *   <meta name="dih-disable-features" content="delay-counter-hud">  (counters without the bar)
 * JS API: window.dihScoreboard.setVariant/getVariant/show/hide/openOverlay.
 * Conversion tracking: every interaction dispatches a 'dih-scoreboard' CustomEvent
 * on document with {action, variant} in detail. Configurator + docs:
 * https://manual.warondisease.org/assets/scoreboard-embed.html
 */

(function() {
  'use strict';

  // Bump when this file or assets/css/scoreboard.css changes; it cache-busts
  // the injected stylesheet for embedders.
  var WIDGET_VERSION = '6.0.0';
  var SCRIPT_SRC = document.currentScript && document.currentScript.src ? document.currentScript.src : '';

  var VARIANTS = ['instrument-panel', 'sentence', 'tab', 'scoreline', 'minimal'];
  var DEFAULT_VARIANT = 'minimal';

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
      closingLine: 'You did not apply; you were born, which is how disease selects opponents.',
      sinceOpenedBefore: 'Since you opened this screen, disease scored ',
      sinceOpenedAfter: ' more. Each one was a person. It does not know you are here.',
      auditPre: 'Every number on this screen ',
      auditLinkText: 'links to its source and math',
      auditPost: ', plus a standing list of ways it could be wrong. Disputes are welcome. Rigged machines do not publish their wiring.',
      ctaPrimary: 'TAKE 30 SECONDS TO END WAR AND DISEASE',
      ctaSecondary: 'CHECK THE WIRING: WHERE AM I WRONG'
    }
  };

  var VOTE_URL = 'https://warondisease.org';
  var AUDIT_PAGE = 'knowledge/appendix/where-am-i-wrong.html';
  var CALC_ANCHOR = 'knowledge/appendix/parameters-and-calculations.html#sec-global_eventually_avoidable_disease_deaths_daily';

  var model = {};

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

  var currentVariant = DEFAULT_VARIANT;
  var currentVariantExplicit = false;

  // Conversion-tracking hook. Embedders (and our own analytics) listen with:
  //   document.addEventListener('dih-scoreboard', function(e) { ... e.detail ... });
  function emit(action, extra) {
    var detail = { action: action, variant: currentVariant };
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

  function scoreUnitLine() {
    return "brutally tortured and murdered by disease because " + leaderCountText() + " leaders haven't spent 30 seconds signing the 1% Treaty";
  }

  function scoreUnitLineShort() {
    return "murdered because " + leaderCountText() + " leaders won't spend 30 seconds";
  }

  function kickerText() {
    return 'EVERY DAY ' + leaderCountText() + ' LEADERS ARE LATE ON THEIR 30-SECOND TASK, DISEASE SCORES ' + format(delayDeathsPerDay(), false);
  }

  function tabHeadLeftText() {
    return "YOUR SPECIES' TAB · OPEN SINCE " + publicationDateText() + ', THE DAY THE FIX WAS PUBLISHED';
  }

  function openHintText() {
    return leaderCountText() + " leaders haven't spent 30 seconds. Tap to see the math.";
  }

  function deathSubText() {
    return format(delayDeathsPerDay(), false) + ' more per day. The 30-second task is still sitting on ' + leaderCountText() + ' desks.';
  }

  function sufferingYearsPerDay() {
    return model.dalyBurdenAnnual * model.eventuallyAvoidableDalyPct / 365.25;
  }

  function sufferingYearsPerSecond() {
    return sufferingHoursPerSecond() / 8766;
  }

  function sufferingDescText() {
    return "Every day they're late adds " + wordCompactFormat.format(sufferingYearsPerDay()) +
      " years of unnecessary suffering. That's " + format(sufferingYearsPerSecond(), false) + ' years per second.';
  }

  function dollarsDescText() {
    return 'For every $1 governments spend on clinical trials, they spend $' +
      format(model.militaryToGovernmentClinicalTrialsRatio, false) + ' on the capacity for mass murder.';
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
    counterEl.className = 'dih-delay-counter dih-arcade-variant-' + currentVariant + (hidden ? ' dih-delay-counter-hidden' : '');
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
      [ratioText, 'what governments spend on the capacity for mass murder vs clinical trials'],
      [formatMoney(model.militarySpendingAnnual, true), 'capacity for mass murder per year'],
      ['× ' + treatyPercent, '= ' + formatMoney(model.treatyAnnualFunding, true) + ' for clinical trials'],
      ['= ' + trialMultiplier, 'more trials than currently exist'],
      [format(model.diseasesWithoutEffectiveTreatment, false), 'diseases have no treatment'],
      ['÷ ' + format(model.newDiseaseFirstTreatmentsPerYear, false) + '/yr', 'current rate of first treatments'],
      ['= ' + statusQuoYears + ' yrs', 'to clear the queue at this pace'],
      [statusQuoYears + ' ÷ ' + trialMultiplier, ''],
      ['= ' + dfdaYears + ' yrs', 'if they sign']
    ];
    var mathHtml = '<div class="dih-arcade-math">';
    for (var i = 0; i < mathSteps.length; i++) {
      mathHtml += '<div class="dih-arcade-math-step">' +
        '<span class="dih-arcade-math-val">' + mathSteps[i][0] + '</span>' +
        (mathSteps[i][1] ? '<span class="dih-arcade-math-desc">' + mathSteps[i][1] + '</span>' : '') +
        '</div>';
    }
    mathHtml += '<p class="dih-arcade-math-punch">Every day before signing: ' + format(delayDeathsPerDay(), false) + ' lives.</p></div>';

    var terrorismBarWidth = model.annualDiseaseDeaths > 0 ? model.annualTerrorismDeaths / model.annualDiseaseDeaths * 100 : 0;
    var clinicalTrialsBarWidth = model.militarySpendingAnnual > 0
      ? model.governmentClinicalTrialsSpendingAnnual / model.militarySpendingAnnual * 100
      : 0;

    var barsHtml =
      barChartHtml('KILLED PER YEAR', [
        ['Disease', format(model.annualDiseaseDeaths, false), 100],
        ['Terrorism', format(model.annualTerrorismDeaths, false), terrorismBarWidth]
      ]) +
      barChartHtml('GOVERNMENT SPENDING PER YEAR', [
        ['Capacity for mass murder', formatMoney(model.militarySpendingAnnual, false), 100],
        ['Clinical trials', formatMoney(model.governmentClinicalTrialsSpendingAnnual, false), clinicalTrialsBarWidth]
      ]);

    overlayEl = document.createElement('div');
    overlayEl.id = 'dih-arcade-overlay';
    overlayEl.className = 'dih-arcade-overlay';
    overlayEl.setAttribute('role', 'dialog');
    overlayEl.setAttribute('aria-modal', 'true');
    overlayEl.setAttribute('aria-label', 'The math behind the scoreboard');
    overlayEl.innerHTML =
      '<button class="dih-arcade-overlay-close" type="button">✕ ' + o.closeText + '</button>' +
      '<div class="dih-arcade-screen">' +
        '<div class="dih-arcade-skull-big">' + skullSvg() + '</div>' +
        '<div class="dih-arcade-death-count">' +
          '<span class="dih-arcade-pts" data-dih-delay-value="since-publication">0</span>' +
        '</div>' +
        '<p class="dih-arcade-subtitle">' + scoreUnitLine() + '</p>' +
        '<p class="dih-arcade-death-sub">' + deathSubText() + '</p>' +
        sectionHtml(o.mathHeading, mathHtml) +
        barsHtml +
        '<section class="dih-arcade-section">' +
          '<h3 class="dih-arcade-heading">' + o.sufferingHeading + '</h3>' +
          '<div class="dih-arcade-sufferline">' +
            '<span class="dih-arcade-suffer" data-dih-delay-value="suffering-hours-since-publication">0</span>' +
            '<span class="dih-arcade-suffer-unit">hours</span>' +
          '</div>' +
          '<p>' + sufferingDescText() + '</p>' +
        '</section>' +
        '<section class="dih-arcade-section">' +
          '<h3 class="dih-arcade-heading">' + o.dollarsHeading + '</h3>' +
          '<div class="dih-arcade-sufferline">' +
            '<span class="dih-arcade-money" data-dih-delay-value="money-since-publication">$0</span>' +
          '</div>' +
          '<p>' + dollarsDescText() + '</p>' +
        '</section>' +
        '<p class="dih-arcade-closing">' + o.closingLine + '</p>' +
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
    overlayEl.querySelector('.dih-arcade-cta-primary').addEventListener('click', function() {
      emit('cta-clicked', { source: 'overlay' });
    });
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
    emit('overlay-opened', null);
  }

  function closeOverlay() {
    if (!overlayEl) return;
    var secondsOpen = overlayOpenedAt === null ? 0 : Math.round((Date.now() - overlayOpenedAt) / 1000);
    overlayEl.classList.remove('dih-arcade-overlay-visible');
    document.body.classList.remove('dih-arcade-overlay-open');
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
    if (counterEl) {
      counterEl.classList.remove('dih-arcade-variant-' + currentVariant);
      counterEl.classList.add('dih-arcade-variant-' + name);
    }
    currentVariant = name;
    currentVariantExplicit = true;
    emit('variant-changed', null);
    return currentVariant;
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
    defaultVariant: DEFAULT_VARIANT,
    version: WIDGET_VERSION,
    setVariant: setVariant,
    getVariant: function() { return currentVariant; },
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
