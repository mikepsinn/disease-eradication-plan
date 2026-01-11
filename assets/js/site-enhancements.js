/**
 * Site Enhancements for Quarto Sites
 *
 * Features:
 * 1. Impact loader with death counter (150K deaths/day from curable diseases)
 * 2. Auto-expand collapsed callouts when navigating to hash anchors
 * 3. Smooth scroll to hash targets with visual highlight
 * 4. Toggle to show/hide uncertainty parameters (95% CI ranges)
 *
 * Version: 3.0.0 - Impact Loader Edition
 */

(function() {
  'use strict';

  // ========================================
  // IMPACT LOADER - DEATH COUNTER
  // ========================================

  const DEATHS_PER_DAY = 150000;
  const DEATHS_PER_SECOND = DEATHS_PER_DAY / 86400; // 1.736 deaths/second
  const GRAVESTONE_ICONS = ['💀']; // Skulls only

  let loaderStartTime = null;
  let loaderUpdateInterval = null;
  let gravestoneInterval = null;
  let isLoaderActive = false;

  function startImpactLoader() {
    const loader = document.getElementById('page-loader');
    if (!loader) return;

    loaderStartTime = Date.now();
    isLoaderActive = true;

    const deathCounter = document.getElementById('deathCounter');
    const gravestoneGrid = document.getElementById('gravestoneGrid');

    if (!deathCounter || !gravestoneGrid) return;

    // Update death counter
    loaderUpdateInterval = setInterval(function() {
      if (!isLoaderActive) return;

      const elapsedSeconds = (Date.now() - loaderStartTime) / 1000;
      const deathCount = Math.floor(elapsedSeconds * DEATHS_PER_SECOND);

      deathCounter.textContent = deathCount.toLocaleString();
    }, 50);

    // Add gravestones periodically
    gravestoneInterval = setInterval(function() {
      if (!isLoaderActive) return;

      const currentDeaths = Math.floor(((Date.now() - loaderStartTime) / 1000) * DEATHS_PER_SECOND);
      const gravestoneCount = gravestoneGrid.querySelectorAll('.gravestone').length;

      if (currentDeaths > gravestoneCount) {
        const gravestone = document.createElement('div');
        gravestone.className = 'gravestone';
        gravestone.textContent = GRAVESTONE_ICONS[Math.floor(Math.random() * GRAVESTONE_ICONS.length)];
        gravestoneGrid.appendChild(gravestone);

        setTimeout(function() {
          gravestone.classList.add('show');
        }, 10);

        // Limit to 100 gravestones for performance
        const gravestones = gravestoneGrid.querySelectorAll('.gravestone');
        if (gravestones.length > 100) {
          gravestones[0].remove();
        }
      }
    }, 200);
  }

  function stopImpactLoader() {
    isLoaderActive = false;
    if (loaderUpdateInterval) clearInterval(loaderUpdateInterval);
    if (gravestoneInterval) clearInterval(gravestoneInterval);
  }

  function hideLoader() {
    const loader = document.getElementById('page-loader');
    if (loader) {
      stopImpactLoader();
      loader.classList.add('hidden');
      setTimeout(function() {
        if (loader.parentNode) {
          loader.parentNode.removeChild(loader);
        }
      }, 600);
    }
  }

  // ========================================
  // AUTO-EXPAND HASH TARGETS
  // ========================================

  function expandHashTarget() {
    var hash = window.location.hash;
    if (!hash || hash.length < 2) {
      return;
    }

    var targetId = hash.substring(1);
    var targetElement = document.getElementById(targetId);

    if (!targetElement) {
      return;
    }

    var calloutToExpand = null;

    // Case 1: Target inside collapse container
    calloutToExpand = targetElement.closest('.callout-collapse');

    // Case 2: Target is heading, look for next sibling callout
    if (!calloutToExpand) {
      var sibling = targetElement.nextElementSibling;
      while (sibling) {
        if (sibling.classList && sibling.classList.contains('callout')) {
          var collapseDiv = sibling.querySelector('.callout-collapse');
          if (collapseDiv) {
            calloutToExpand = collapseDiv;
          }
          break;
        }
        sibling = sibling.nextElementSibling;
      }
    }

    // Case 3: Target in parent callout
    if (!calloutToExpand) {
      var parentCallout = targetElement.closest('.callout');
      if (parentCallout) {
        var collapseDiv = parentCallout.querySelector('.callout-collapse');
        if (collapseDiv) {
          calloutToExpand = collapseDiv;
        }
      }
    }

    // Expand callout if found
    if (calloutToExpand && !calloutToExpand.classList.contains('show')) {
      if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
        var bsCollapse = new bootstrap.Collapse(calloutToExpand, { toggle: false });
        bsCollapse.show();
      } else {
        calloutToExpand.classList.add('show');
        var calloutContainer = calloutToExpand.closest('.callout');
        if (calloutContainer) {
          var toggleBtn = calloutContainer.querySelector('.callout-btn-toggle');
          if (toggleBtn) {
            toggleBtn.setAttribute('aria-expanded', 'true');
          }
        }
      }

      // Add highlight effect
      var calloutContainer = calloutToExpand.closest('.callout');
      if (calloutContainer) {
        calloutContainer.classList.add('hash-target-highlight');
        setTimeout(function() {
          calloutContainer.classList.remove('hash-target-highlight');
        }, 1500);
      }
    }

    // Highlight heading
    if (targetElement.tagName && targetElement.tagName.match(/^H[1-6]$/)) {
      targetElement.classList.add('hash-target-heading');
      setTimeout(function() {
        targetElement.classList.remove('hash-target-heading');
      }, 3000);
    }

    // Scroll to target
    setTimeout(function() {
      var headerOffset = 80;
      var elementPosition = targetElement.getBoundingClientRect().top;
      var offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }, 150);
  }

  // ========================================
  // UNCERTAINTY TOGGLE
  // ========================================

  var STORAGE_KEY = 'dih-hide-uncertainty';

  function createUncertaintyToggle() {
    var hasUncertaintyData = document.querySelector('a[title*="95% CI"]') ||
                             document.querySelector('.tippy-content') ||
                             document.body.textContent.includes('95% CI');

    if (!hasUncertaintyData) {
      return;
    }

    if (document.getElementById('uncertainty-toggle')) {
      return;
    }

    var toggle = document.createElement('button');
    toggle.id = 'uncertainty-toggle';
    toggle.type = 'button';
    toggle.innerHTML = '<span class="toggle-icon">📊</span><span class="toggle-text">Show CI</span>';
    toggle.title = 'Toggle visibility of 95% confidence intervals';

    var isHidden = localStorage.getItem(STORAGE_KEY) === 'true';
    if (isHidden) {
      document.body.classList.add('hide-uncertainty');
      toggle.classList.add('ci-hidden');
      toggle.querySelector('.toggle-text').textContent = 'Show CI';
    } else {
      toggle.querySelector('.toggle-text').textContent = 'Hide CI';
    }

    toggle.addEventListener('click', function() {
      var nowHidden = document.body.classList.toggle('hide-uncertainty');
      toggle.classList.toggle('ci-hidden', nowHidden);
      toggle.querySelector('.toggle-text').textContent = nowHidden ? 'Show CI' : 'Hide CI';
      localStorage.setItem(STORAGE_KEY, nowHidden);
      processUncertaintyText(nowHidden);
    });

    document.body.appendChild(toggle);

    if (isHidden) {
      processUncertaintyText(true);
    }
  }

  function processUncertaintyText(hide) {
    var links = document.querySelectorAll('a[title*="95% CI"]');

    links.forEach(function(link) {
      var originalText = link.getAttribute('data-original-text');

      if (!originalText) {
        link.setAttribute('data-original-text', link.textContent);
        link.setAttribute('data-original-title', link.getAttribute('title') || '');
        originalText = link.textContent;
      }

      if (hide) {
        var cleanText = originalText.replace(/\s*\(95% CI:[^)]+\)/gi, '');
        link.textContent = cleanText;
      } else {
        link.textContent = originalText;
      }
    });

    if (!hide) {
      var modified = document.querySelectorAll('[data-ci-hidden]');
      modified.forEach(function(el) {
        el.innerHTML = el.getAttribute('data-original-html');
        el.removeAttribute('data-ci-hidden');
        el.removeAttribute('data-original-html');
      });
    }
  }

  // ========================================
  // INITIALIZATION
  // ========================================

  function onPageReady() {
    setTimeout(function() {
      startImpactLoader();
      expandHashTarget();
      createUncertaintyToggle();
      // Hide loader after page is fully ready
      setTimeout(hideLoader, 200);
    }, 100);
  }

  if (document.readyState === 'complete') {
    onPageReady();
  } else {
    window.addEventListener('load', onPageReady);
  }

  // Handle hash changes
  window.addEventListener('hashchange', function() {
    expandHashTarget();
  });

  // Handle clicks on hash links
  document.addEventListener('click', function(e) {
    var link = e.target.closest('a[href*="#"]');
    if (link) {
      var href = link.getAttribute('href');
      if (href && (href.startsWith('#') || href.includes(window.location.pathname + '#'))) {
        setTimeout(expandHashTarget, 100);
      }
    }
  });

})();
