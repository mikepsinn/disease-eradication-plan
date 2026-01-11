/**
 * Site Enhancements for Quarto Sites
 *
 * Features:
 * 1. Auto-expand collapsed callouts when navigating to hash anchors
 * 2. Smooth scroll to hash targets with visual highlight
 * 3. Toggle to show/hide uncertainty parameters (95% CI ranges)
 *
 * Note: Page loader is handled separately in page-loader.html
 *
 * Version: 3.1.0
 */

(function() {
  'use strict';

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
      expandHashTarget();
      createUncertaintyToggle();
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
