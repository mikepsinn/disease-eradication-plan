/**
 * Site Enhancements for Quarto Sites
 *
 * Features:
 * 1. Auto-expand collapsed callouts when navigating to hash anchors
 * 2. Smooth scroll to hash targets with visual highlight
 * 3. Toggle to show/hide uncertainty parameters (95% CI ranges)
 * 4. Dark mode toggle with localStorage persistence
 * 5. Copy citation button (BibTeX format)
 * 6. Back to top button
 *
 * Note: Page loader is handled separately in page-loader.html
 *
 * Version: 4.0.0
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

    // Case 1: Target is inside a collapse container directly
    calloutToExpand = targetElement.closest('.callout-collapse');

    // Case 2: Target is a section/heading, look for callout INSIDE it (Quarto structure)
    // Quarto puts #sec-xxx IDs on <section> elements that contain headings AND callouts
    if (!calloutToExpand) {
      var calloutInside = targetElement.querySelector('.callout .callout-collapse');
      if (calloutInside) {
        calloutToExpand = calloutInside;
      }
    }

    // Case 3: Look for first callout child within the target element
    if (!calloutToExpand) {
      var firstCallout = targetElement.querySelector('.callout');
      if (firstCallout) {
        var collapseDiv = firstCallout.querySelector('.callout-collapse');
        if (collapseDiv) {
          calloutToExpand = collapseDiv;
        }
      }
    }

    // Case 4: Target is heading, look for next sibling callout
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

    // Case 5: Target in parent callout
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
      expandCallout(calloutToExpand);
    }

    // Highlight heading (check both target and first heading child)
    var headingElement = targetElement;
    if (!headingElement.tagName || !headingElement.tagName.match(/^H[1-6]$/)) {
      headingElement = targetElement.querySelector('h1, h2, h3, h4, h5, h6');
    }
    if (headingElement && headingElement.tagName && headingElement.tagName.match(/^H[1-6]$/)) {
      headingElement.classList.add('hash-target-heading');
      setTimeout(function() {
        headingElement.classList.remove('hash-target-heading');
      }, 3000);
    }

    // Scroll to target after expansion
    setTimeout(function() {
      var headerOffset = 80;
      var elementPosition = targetElement.getBoundingClientRect().top;
      var offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }, 300);
  }

  function expandCallout(collapseDiv) {
    // Try Bootstrap Collapse API first
    if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
      try {
        var bsCollapse = bootstrap.Collapse.getOrCreateInstance(collapseDiv, { toggle: false });
        bsCollapse.show();
      } catch (e) {
        // Fallback to manual expansion
        manualExpandCallout(collapseDiv);
      }
    } else {
      manualExpandCallout(collapseDiv);
    }

    // Add highlight effect
    var calloutContainer = collapseDiv.closest('.callout');
    if (calloutContainer) {
      calloutContainer.classList.add('hash-target-highlight');
      setTimeout(function() {
        calloutContainer.classList.remove('hash-target-highlight');
      }, 2000);
    }
  }

  function manualExpandCallout(collapseDiv) {
    collapseDiv.classList.add('show');
    collapseDiv.style.height = '';

    var calloutContainer = collapseDiv.closest('.callout');
    if (calloutContainer) {
      // Update toggle button state
      var toggleBtn = calloutContainer.querySelector('.callout-btn-toggle, [data-bs-toggle="collapse"]');
      if (toggleBtn) {
        toggleBtn.setAttribute('aria-expanded', 'true');
        toggleBtn.classList.remove('collapsed');
      }
    }
  }

  // ========================================
  // UNCERTAINTY TOGGLE
  // ========================================

  var STORAGE_KEY = 'dih-hide-uncertainty';

  function createUncertaintyToggle() {
    // Check for parameter links with CI text in content (not title attribute)
    var paramLinks = document.querySelectorAll('a.parameter-link');
    var hasParameterWithCI = Array.from(paramLinks).some(function(link) {
      return link.textContent.includes('95% CI');
    });
    var hasUncertaintyData = hasParameterWithCI ||
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
    // Select parameter-link elements (CI text is in text content, not title attribute)
    var links = document.querySelectorAll('a.parameter-link');

    links.forEach(function(link) {
      var originalText = link.getAttribute('data-original-text');

      // Store original text on first encounter
      if (!originalText) {
        // Only process links that actually contain CI text
        if (!link.textContent.includes('95% CI')) {
          return;
        }
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
  // DARK MODE TOGGLE
  // ========================================

  var DARK_MODE_KEY = 'dih-dark-mode';

  function createDarkModeToggle() {
    if (document.getElementById('dark-mode-toggle')) {
      return;
    }

    var toggle = document.createElement('button');
    toggle.id = 'dark-mode-toggle';
    toggle.type = 'button';
    toggle.innerHTML = '<span class="toggle-icon">🌙</span>';
    toggle.title = 'Toggle dark mode';

    var isDark = localStorage.getItem(DARK_MODE_KEY) === 'true';
    if (isDark) {
      document.documentElement.classList.add('dark-mode');
      toggle.innerHTML = '<span class="toggle-icon">☀️</span>';
    }

    toggle.addEventListener('click', function() {
      var nowDark = document.documentElement.classList.toggle('dark-mode');
      toggle.innerHTML = nowDark ? '<span class="toggle-icon">☀️</span>' : '<span class="toggle-icon">🌙</span>';
      localStorage.setItem(DARK_MODE_KEY, nowDark);
    });

    document.body.appendChild(toggle);
  }

  // ========================================
  // COPY CITATION BUTTON
  // ========================================

  function createCopyCitationButton() {
    // Only create on pages with DOI metadata
    var doiMeta = document.querySelector('meta[name="citation_doi"]') ||
                  document.querySelector('meta[name="DC.identifier"]');
    var titleMeta = document.querySelector('meta[name="citation_title"]') ||
                    document.querySelector('meta[property="og:title"]') ||
                    document.querySelector('title');
    var authorMeta = document.querySelector('meta[name="citation_author"]') ||
                     document.querySelector('meta[name="author"]');

    // Skip if no meaningful citation data
    if (!titleMeta) {
      return;
    }

    if (document.getElementById('copy-citation-btn')) {
      return;
    }

    var btn = document.createElement('button');
    btn.id = 'copy-citation-btn';
    btn.type = 'button';
    btn.innerHTML = '<span class="btn-icon">📋</span><span class="btn-text">Cite</span>';
    btn.title = 'Copy citation (BibTeX)';

    btn.addEventListener('click', function() {
      var title = titleMeta.content || titleMeta.textContent || 'Untitled';
      var author = authorMeta ? (authorMeta.content || 'Unknown') : 'Sinn, Mike P.';
      var doi = doiMeta ? doiMeta.content : '';
      var url = window.location.href;
      var year = new Date().getFullYear();

      // Generate citation key from title
      var key = title.toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '')
        .substring(0, 30);

      var bibtex = '@article{' + key + '-' + year + ',\n' +
        '  title     = {' + title + '},\n' +
        '  author    = {' + author + '},\n' +
        '  year      = {' + year + '},\n' +
        (doi ? '  doi       = {' + doi + '},\n' : '') +
        '  url       = {' + url + '}\n' +
        '}';

      navigator.clipboard.writeText(bibtex).then(function() {
        var originalText = btn.innerHTML;
        btn.innerHTML = '<span class="btn-icon">✓</span><span class="btn-text">Copied!</span>';
        btn.classList.add('copied');
        setTimeout(function() {
          btn.innerHTML = originalText;
          btn.classList.remove('copied');
        }, 2000);
      }).catch(function() {
        // Fallback for older browsers
        var textarea = document.createElement('textarea');
        textarea.value = bibtex;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        btn.innerHTML = '<span class="btn-icon">✓</span><span class="btn-text">Copied!</span>';
        setTimeout(function() {
          btn.innerHTML = '<span class="btn-icon">📋</span><span class="btn-text">Cite</span>';
        }, 2000);
      });
    });

    document.body.appendChild(btn);
  }

  // ========================================
  // BACK TO TOP BUTTON
  // ========================================

  function createBackToTopButton() {
    if (document.getElementById('back-to-top')) {
      return;
    }

    var btn = document.createElement('button');
    btn.id = 'back-to-top';
    btn.type = 'button';
    btn.innerHTML = '↑';
    btn.title = 'Back to top';

    btn.addEventListener('click', function() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });

    function toggleVisibility() {
      if (window.pageYOffset > 300) {
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
      }
    }

    window.addEventListener('scroll', toggleVisibility, { passive: true });
    document.body.appendChild(btn);
    toggleVisibility();
  }

  // ========================================
  // INITIALIZATION
  // ========================================

  function onPageReady() {
    // Wait longer for large pages to fully render (loader takes 600ms to fade)
    setTimeout(function() {
      expandHashTarget();
      createUncertaintyToggle();
      createDarkModeToggle();
      createCopyCitationButton();
      createBackToTopButton();
    }, 800);
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
