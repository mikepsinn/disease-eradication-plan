/**
 * Promotion Bar - Cross-site sticky bottom CTA bar
 * ==================================================
 * Self-contained: injects its own CSS and HTML into the DOM.
 *
 * Usage (Quarto sites):
 *   Loaded automatically via assets/html/site-enhancements-loader.html
 *
 * Usage (external sites):
 *   <script src="https://manual.warondisease.org/assets/js/promotion-bar.js" defer></script>
 *
 * Configuration (optional meta tags):
 *   <meta name="wod-promo-hide" content="true">       - Hide on this page
 *   <meta name="wod-promo-primary" content="book">     - Override primary CTA
 *   <meta name="wod-promo-secondary" content="listen">  - Override secondary CTA
 */
(function() {
  'use strict';

  // ---------------------------------------------------------------------------
  // Configuration
  // ---------------------------------------------------------------------------
  var DISMISS_KEY = 'wod-promo-dismissed';
  var DISMISS_DAYS = 7;
  var SHOW_DELAY_MS = 1500;
  var BAR_HEIGHT_PX = 56;
  var UTM = 'utm_source=promo_bar&utm_medium=sticky_bar&utm_campaign=cross_site';

  // Pages where the bar is redundant
  var EXCLUDE_PATHS = ['/links', '/podcast'];

  // All available CTAs
  var ALL_CTAS = {
    vote:    { label: 'Vote Now',    url: 'https://WarOnDisease.org',                                      icon: '\u2694\uFE0F', ga: 'vote' },
    listen:  { label: 'Listen',      url: 'https://manual.WarOnDisease.org/knowledge/links.html',          icon: '\uD83C\uDFA7', ga: 'listen' },
    book:    { label: 'Get the Book',url: 'https://www.amazon.com/dp/B0GPLXFMMT',                          icon: '\uD83D\uDCD6', ga: 'book' },
    read:    { label: 'Read Free',   url: 'https://manual.WarOnDisease.org',                                icon: '\uD83D\uDCDA', ga: 'read' },
    youtube: { label: 'Subscribe',   url: 'https://www.youtube.com/@WarOnDisease?sub_confirmation=1',       icon: '\u25B6\uFE0F',  ga: 'youtube' }
  };

  // Secondary CTA rotation pool (one per day for natural A/B testing)
  var SECONDARY_POOL = ['listen', 'book', 'youtube'];

  // ---------------------------------------------------------------------------
  // Early exit checks
  // ---------------------------------------------------------------------------

  // Meta tag opt-out
  var hideMeta = document.querySelector('meta[name="wod-promo-hide"]');
  if (hideMeta && hideMeta.getAttribute('content') === 'true') return;

  // Excluded paths
  var path = window.location.pathname.toLowerCase();
  for (var i = 0; i < EXCLUDE_PATHS.length; i++) {
    if (path.indexOf(EXCLUDE_PATHS[i]) !== -1) return;
  }

  // Dismissed recently?
  try {
    var dismissed = localStorage.getItem(DISMISS_KEY);
    if (dismissed) {
      var ts = parseInt(dismissed, 10);
      if (!isNaN(ts) && Date.now() - ts < DISMISS_DAYS * 86400000) return;
    }
  } catch(e) { /* localStorage unavailable */ }

  // ---------------------------------------------------------------------------
  // CTA selection
  // ---------------------------------------------------------------------------

  // Primary CTA: always vote unless overridden
  var primaryKey = 'vote';
  var pmeta = document.querySelector('meta[name="wod-promo-primary"]');
  if (pmeta) primaryKey = pmeta.getAttribute('content') || primaryKey;

  // Secondary CTA: rotate daily unless overridden
  var secondaryKey;
  var smeta = document.querySelector('meta[name="wod-promo-secondary"]');
  if (smeta) {
    secondaryKey = smeta.getAttribute('content');
  } else {
    // Context-aware defaults
    var host = window.location.hostname.toLowerCase();
    if (host.indexOf('manual.') === 0) {
      // Already reading the book; push podcast
      secondaryKey = 'listen';
    } else if (host.indexOf('warondisease.org') !== -1) {
      // On a paper/sub-site; push the full book
      secondaryKey = 'read';
    } else {
      // External site: rotate daily
      var dayIdx = new Date().getDate() % SECONDARY_POOL.length;
      secondaryKey = SECONDARY_POOL[dayIdx];
    }
  }

  // Don't show same CTA twice
  if (secondaryKey === primaryKey) {
    secondaryKey = SECONDARY_POOL[0] !== primaryKey ? SECONDARY_POOL[0] : SECONDARY_POOL[1];
  }

  var primary = ALL_CTAS[primaryKey] || ALL_CTAS.vote;
  var secondary = ALL_CTAS[secondaryKey] || ALL_CTAS.listen;

  // ---------------------------------------------------------------------------
  // UTM helper
  // ---------------------------------------------------------------------------
  function addUtm(url, ctaName) {
    var sep = url.indexOf('?') !== -1 ? '&' : '?';
    return url + sep + UTM + '&utm_content=' + ctaName;
  }

  // ---------------------------------------------------------------------------
  // GA tracking helper
  // ---------------------------------------------------------------------------
  function track(action, label) {
    if (typeof gtag === 'function') {
      gtag('event', action, { event_category: 'promotion_bar', event_label: label });
    }
  }

  // ---------------------------------------------------------------------------
  // Inject CSS
  // ---------------------------------------------------------------------------
  var style = document.createElement('style');
  style.textContent = [
    '#wod-promo-bar {',
    '  position: fixed; bottom: 0; left: 0; right: 0; z-index: 999;',
    '  background: #1a1a2e; color: #e8e0d6;',
    '  padding: 0; margin: 0;',
    '  box-shadow: 0 -2px 12px rgba(0,0,0,0.2);',
    '  transform: translateY(100%);',
    '  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);',
    '  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;',
    '}',
    '#wod-promo-bar.visible { transform: translateY(0); }',
    '#wod-promo-bar .promo-inner {',
    '  max-width: 960px; margin: 0 auto;',
    '  display: flex; align-items: center; justify-content: center;',
    '  gap: 1rem; padding: 0.7rem 1rem;',
    '}',
    '#wod-promo-bar .promo-msg {',
    '  font-size: 0.92rem; font-weight: 500;',
    '  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;',
    '}',
    '#wod-promo-bar .promo-ctas {',
    '  display: flex; gap: 0.5rem; flex-shrink: 0;',
    '}',
    '#wod-promo-bar .promo-btn {',
    '  display: inline-flex; align-items: center; gap: 0.35rem;',
    '  padding: 0.4rem 1rem; border-radius: 6px;',
    '  text-decoration: none !important; font-weight: 600; font-size: 0.88rem;',
    '  white-space: nowrap; cursor: pointer;',
    '  transition: background 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;',
    '}',
    '#wod-promo-bar .promo-btn-primary {',
    '  background: #c9a84c; color: #1a1a2e !important; border: none;',
    '}',
    '#wod-promo-bar .promo-btn-primary:hover {',
    '  background: #dbb85c; transform: translateY(-1px);',
    '  box-shadow: 0 2px 8px rgba(201,168,76,0.3);',
    '}',
    '#wod-promo-bar .promo-btn-secondary {',
    '  background: transparent; color: #e8e0d6 !important;',
    '  border: 1.5px solid rgba(232,224,214,0.4);',
    '}',
    '#wod-promo-bar .promo-btn-secondary:hover {',
    '  background: rgba(232,224,214,0.08); transform: translateY(-1px);',
    '  border-color: rgba(232,224,214,0.7);',
    '}',
    '#wod-promo-bar .promo-dismiss {',
    '  background: none; border: none; color: #6b6360; cursor: pointer;',
    '  font-size: 1.15rem; padding: 0.3rem 0.5rem; line-height: 1;',
    '  flex-shrink: 0; transition: color 0.15s ease;',
    '}',
    '#wod-promo-bar .promo-dismiss:hover { color: #e8e0d6; }',
    '',
    '/* Push floating buttons up when bar is visible */',
    'body.wod-promo-active { padding-bottom: ' + BAR_HEIGHT_PX + 'px; }',
    'body.wod-promo-active #dark-mode-toggle { bottom: ' + (BAR_HEIGHT_PX + 20) + 'px !important; }',
    'body.wod-promo-active #uncertainty-toggle { bottom: ' + (BAR_HEIGHT_PX + 20) + 'px !important; }',
    'body.wod-promo-active #copy-citation-btn { bottom: ' + (BAR_HEIGHT_PX + 70) + 'px !important; }',
    'body.wod-promo-active #back-to-top { bottom: ' + (BAR_HEIGHT_PX + 120) + 'px !important; }',
    '',
    '/* Mobile */',
    '@media (max-width: 600px) {',
    '  #wod-promo-bar .promo-inner {',
    '    flex-wrap: wrap; gap: 0.4rem; padding: 0.6rem 0.7rem;',
    '    position: relative;',
    '  }',
    '  #wod-promo-bar .promo-msg {',
    '    width: 100%; text-align: center; font-size: 0.82rem;',
    '    padding-right: 1.5rem;',
    '  }',
    '  #wod-promo-bar .promo-ctas { width: 100%; justify-content: center; }',
    '  #wod-promo-bar .promo-btn { padding: 0.35rem 0.8rem; font-size: 0.82rem; }',
    '  #wod-promo-bar .promo-dismiss {',
    '    position: absolute; top: 0.3rem; right: 0.3rem;',
    '  }',
    '}',
    '',
    '/* Print */',
    '@media print {',
    '  #wod-promo-bar { display: none !important; }',
    '  body.wod-promo-active { padding-bottom: 0 !important; }',
    '}'
  ].join('\n');
  document.head.appendChild(style);

  // ---------------------------------------------------------------------------
  // Inject HTML
  // ---------------------------------------------------------------------------
  var bar = document.createElement('div');
  bar.id = 'wod-promo-bar';
  bar.setAttribute('role', 'complementary');
  bar.setAttribute('aria-label', 'Promotion');
  bar.innerHTML = [
    '<div class="promo-inner">',
    '  <span class="promo-msg">Help end war &amp; disease</span>',
    '  <span class="promo-ctas">',
    '    <a href="' + addUtm(primary.url, primary.ga) + '" class="promo-btn promo-btn-primary" data-ga="' + primary.ga + '" target="_blank" rel="noopener">',
    '      ' + primary.icon + ' ' + primary.label,
    '    </a>',
    '    <a href="' + addUtm(secondary.url, secondary.ga) + '" class="promo-btn promo-btn-secondary" data-ga="' + secondary.ga + '" target="_blank" rel="noopener">',
    '      ' + secondary.icon + ' ' + secondary.label,
    '    </a>',
    '  </span>',
    '  <button class="promo-dismiss" aria-label="Dismiss" title="Dismiss">&times;</button>',
    '</div>'
  ].join('\n');

  document.body.appendChild(bar);

  // ---------------------------------------------------------------------------
  // Show with delay (smooth slide-up)
  // ---------------------------------------------------------------------------
  setTimeout(function() {
    bar.classList.add('visible');
    document.body.classList.add('wod-promo-active');
    track('promotion_bar_impression', secondary.ga);
  }, SHOW_DELAY_MS);

  // ---------------------------------------------------------------------------
  // Dismiss handler
  // ---------------------------------------------------------------------------
  bar.querySelector('.promo-dismiss').addEventListener('click', function() {
    bar.classList.remove('visible');
    document.body.classList.remove('wod-promo-active');
    try { localStorage.setItem(DISMISS_KEY, Date.now().toString()); } catch(e) {}
    track('promotion_bar_dismiss', '');
    // Remove from DOM after animation
    setTimeout(function() { bar.parentNode && bar.parentNode.removeChild(bar); }, 500);
  });

  // ---------------------------------------------------------------------------
  // Click tracking
  // ---------------------------------------------------------------------------
  var btns = bar.querySelectorAll('.promo-btn');
  for (var b = 0; b < btns.length; b++) {
    btns[b].addEventListener('click', function() {
      track('promotion_bar_click', this.getAttribute('data-ga'));
    });
  }

})();
