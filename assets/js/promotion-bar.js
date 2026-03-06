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
  var BAR_HEIGHT_PX = 40;
  var UTM = 'utm_source=promo_bar&utm_medium=sticky_bar&utm_campaign=cross_site';

  // Pages where the bar is redundant
  var EXCLUDE_PATHS = ['/links', '/podcast'];

  // All available CTAs
  var ALL_CTAS = {
    vote:    { label: 'Vote Now',           url: 'https://WarOnDisease.org',                              ga: 'vote' },
    links:   { label: 'End War & Disease',  url: 'https://manual.WarOnDisease.org/knowledge/links.html',  ga: 'links' }
  };

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

  var primary = ALL_CTAS.vote;
  var secondary = ALL_CTAS.links;

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
    '  position: fixed; left: 50%; bottom: 10px; z-index: 999;',
    '  max-width: calc(100vw - 1rem);',
    '  background: rgba(17,24,39,0.94); color: #f8fafc;',
    '  border: 1px solid rgba(248,250,252,0.14);',
    '  border-radius: 999px;',
    '  box-shadow: 0 8px 24px rgba(0,0,0,0.24);',
    '  backdrop-filter: blur(6px);',
    '  transform: translate(-50%, calc(100% + 20px));',
    '  opacity: 0;',
    '  transition: transform 0.25s ease, opacity 0.25s ease;',
    '  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;',
    '}',
    '#wod-promo-bar.visible { transform: translate(-50%, 0); opacity: 1; }',
    '#wod-promo-bar .promo-inner {',
    '  display: flex; align-items: center; gap: 0.45rem;',
    '  padding: 0.35rem 0.5rem;',
    '}',
    '#wod-promo-bar .promo-ctas {',
    '  display: flex; align-items: center; gap: 0.35rem;',
    '}',
    '#wod-promo-bar .promo-btn {',
    '  display: inline-flex; align-items: center;',
    '  padding: 0.28rem 0.62rem; border-radius: 999px;',
    '  text-decoration: none !important; font-weight: 600; font-size: 0.78rem;',
    '  white-space: nowrap; line-height: 1.2;',
    '  transition: background 0.15s ease, color 0.15s ease;',
    '}',
    '#wod-promo-bar .promo-btn-primary {',
    '  background: #fbbf24; color: #111827 !important; border: 1px solid transparent;',
    '}',
    '#wod-promo-bar .promo-btn-primary:hover { background: #fcd34d; }',
    '#wod-promo-bar .promo-btn-secondary {',
    '  background: transparent; color: rgba(248,250,252,0.86) !important;',
    '  border: none; padding: 0.24rem 0.35rem;',
    '}',
    '#wod-promo-bar .promo-btn-secondary:hover { color: #ffffff !important; }',
    '#wod-promo-bar .promo-dismiss {',
    '  background: none; border: none; color: rgba(248,250,252,0.52);',
    '  cursor: pointer; font-size: 1rem; padding: 0.18rem 0.32rem; line-height: 1;',
    '  transition: color 0.15s ease;',
    '}',
    '#wod-promo-bar .promo-dismiss:hover { color: #ffffff; }',
    '',
    'body.wod-promo-active { padding-bottom: 0; }',
    'body.wod-promo-active #dark-mode-toggle { bottom: ' + (BAR_HEIGHT_PX + 12) + 'px !important; }',
    'body.wod-promo-active #uncertainty-toggle { bottom: ' + (BAR_HEIGHT_PX + 12) + 'px !important; }',
    'body.wod-promo-active #copy-citation-btn { bottom: ' + (BAR_HEIGHT_PX + 56) + 'px !important; }',
    'body.wod-promo-active #back-to-top { bottom: ' + (BAR_HEIGHT_PX + 98) + 'px !important; }',
    '',
    '@media (max-width: 600px) {',
    '  #wod-promo-bar { bottom: 8px; max-width: calc(100vw - 0.75rem); }',
    '  #wod-promo-bar .promo-inner { padding: 0.3rem 0.42rem; gap: 0.28rem; }',
    '  #wod-promo-bar .promo-btn { padding: 0.24rem 0.54rem; font-size: 0.74rem; }',
    '  #wod-promo-bar .promo-btn-secondary { display: none; }',
    '}',
    '',
    '@media print {',
    '  #wod-promo-bar { display: none !important; }',
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
    '  <span class="promo-ctas">',
    '    <a href="' + addUtm(primary.url, primary.ga) + '" class="promo-btn promo-btn-primary" data-ga="' + primary.ga + '" target="_blank" rel="noopener">',
    '      ' + primary.label,
    '    </a>',
    '    <a href="' + addUtm(secondary.url, secondary.ga) + '" class="promo-btn promo-btn-secondary" data-ga="' + secondary.ga + '" target="_blank" rel="noopener">',
    '      ' + secondary.label,
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
