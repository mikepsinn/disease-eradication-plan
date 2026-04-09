/**
 * Site Enhancements for Quarto Sites
 *
 * Features:
 * 1. Auto-expand collapsed callouts when navigating to hash anchors
 * 2. Smooth scroll to hash targets with visual highlight
 * 3. Unified FAB with spring-out sub-buttons:
 *    - Chat (Wishonia, registered by external chat-widget.js via window.dihFAB)
 *    - Copy citation (BibTeX)
 *    - Show/hide confidence intervals
 *    - Dark mode toggle
 *    - Back to top
 *
 * Note: Page loader is handled separately in page-loader.html
 *
 * Version: 5.2.0
 */

(function() {
  'use strict';

  function notifyHashTargetReady(detail) {
    if (typeof CustomEvent !== 'function') {
      return;
    }

    document.dispatchEvent(new CustomEvent('dih:hash-target-ready', {
      detail: detail || {}
    }));
  }

  // ========================================
  // AUTO-EXPAND HASH TARGETS
  // ========================================

  function expandHashTarget() {
    var hash = window.location.hash;
    if (!hash || hash.length < 2) {
      return false;
    }

    var targetId = hash.substring(1);
    var targetElement = document.getElementById(targetId);

    if (!targetElement) {
      notifyHashTargetReady({ found: false, targetId: targetId });
      return false;
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
      expandCallout(calloutToExpand, true);
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

    // Scroll after the expanded state has been applied.
    requestAnimationFrame(function() {
      var headerOffset = 80;
      var elementPosition = targetElement.getBoundingClientRect().top;
      var offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
      notifyHashTargetReady({ found: true, targetId: targetId });
    });

    return true;
  }

  function expandCallout(collapseDiv, instant) {
    if (instant) {
      manualExpandCallout(collapseDiv);
    } else if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
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
    collapseDiv.classList.remove('collapsing');
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
  // UNIFIED FAB (Floating Action Button)
  // ========================================

  var fabOpen = false;
  var fabContainer = null;
  var fabActions = []; // ordered list of {id, el} for sub-buttons

  function createUnifiedFAB() {
    if (document.getElementById('dih-fab')) return;

    fabContainer = document.createElement('div');
    fabContainer.id = 'dih-fab';
    fabContainer.className = 'dih-fab';

    var main = document.createElement('button');
    main.className = 'dih-fab-main';
    main.type = 'button';
    main.setAttribute('aria-label', 'Toggle tools menu');
    main.title = 'Tools';
    main.innerHTML = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>';
    main.addEventListener('click', function(e) {
      e.stopPropagation();
      toggleFAB();
    });

    fabContainer.appendChild(main);
    document.body.appendChild(fabContainer);

    // Close on outside click
    document.addEventListener('click', function(e) {
      if (fabOpen && !fabContainer.contains(e.target)) {
        closeFAB();
      }
    });

    // Close on Escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && fabOpen) closeFAB();
    });
  }

  function toggleFAB() {
    fabOpen ? closeFAB() : openFAB();
  }

  function openFAB() {
    fabOpen = true;
    fabContainer.classList.add('dih-fab-open');
  }

  function closeFAB() {
    fabOpen = false;
    fabContainer.classList.remove('dih-fab-open');
  }

  /**
   * Add a sub-action to the FAB. Called internally and by external scripts (e.g. chat widget).
   * @param {string} id - unique id for the action
   * @param {string} label - tooltip text
   * @param {string} icon - HTML for the icon (emoji or SVG)
   * @param {Function} onClick - click handler
   * @param {Object} [opts] - { order: number (lower = closer to main button), closeFabOnClick: bool }
   * @returns {HTMLElement} the created sub-button
   */
  function addFABAction(id, label, icon, onClick, opts) {
    opts = opts || {};
    if (document.getElementById('dih-fab-' + id)) {
      return document.getElementById('dih-fab-' + id);
    }

    var btn = document.createElement('button');
    btn.id = 'dih-fab-' + id;
    btn.className = 'dih-fab-action';
    btn.type = 'button';
    btn.title = label;
    btn.setAttribute('aria-label', label);
    btn.innerHTML = '<span class="dih-fab-action-icon">' + icon + '</span><span class="dih-fab-action-label">' + label + '</span>';
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      onClick(e);
      if (opts.closeFabOnClick !== false) closeFAB();
    });

    var order = opts.order != null ? opts.order : 50;
    btn.setAttribute('data-fab-order', order);

    // Higher-order actions sit farther from the gear (visually higher in the
    // stack); lower-order actions end up closer to it. With flex-direction:
    // column, that means higher-order = earlier in DOM, lower-order = later
    // (just before the main button, which is always the last child).
    var inserted = false;
    for (var i = 0; i < fabActions.length; i++) {
      var existingOrder = parseInt(fabActions[i].el.getAttribute('data-fab-order'), 10);
      if (order > existingOrder) {
        fabContainer.insertBefore(btn, fabActions[i].el);
        fabActions.splice(i, 0, { id: id, el: btn });
        inserted = true;
        break;
      }
    }
    if (!inserted) {
      // Fallback: insert just before the main button — closest to the gear.
      var mainBtn = fabContainer.querySelector('.dih-fab-main');
      fabContainer.insertBefore(btn, mainBtn);
      fabActions.push({ id: id, el: btn });
    }

    return btn;
  }

  // Expose global API for external scripts (chat widget)
  window.dihFAB = {
    addAction: addFABAction,
    open: function() { openFAB(); },
    close: function() { closeFAB(); },
    toggle: function() { toggleFAB(); }
  };

  // ========================================
  // UNCERTAINTY TOGGLE
  // ========================================

  var STORAGE_KEY = 'dih-hide-uncertainty';

  function createUncertaintyToggle() {
    var paramLinks = document.querySelectorAll('a.parameter-link');
    var hasParameterWithCI = Array.from(paramLinks).some(function(link) {
      return link.textContent.includes('95% CI');
    });
    var hasUncertaintyData = hasParameterWithCI ||
                             document.querySelector('.tippy-content') ||
                             document.body.textContent.includes('95% CI');

    if (!hasUncertaintyData) return;

    // Apply stored preference immediately
    var isShown = localStorage.getItem(STORAGE_KEY) === 'false';
    if (!isShown) {
      document.body.classList.add('hide-uncertainty');
    }

    var ciHidden = !isShown;

    addFABAction('ci-toggle',
      ciHidden ? 'Show confidence intervals' : 'Hide confidence intervals',
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="M7 16l4-8 4 4 5-10"/></svg>',
      function() {
        ciHidden = document.body.classList.toggle('hide-uncertainty');
        localStorage.setItem(STORAGE_KEY, ciHidden);
        processUncertaintyText(ciHidden);
        var btn = document.getElementById('dih-fab-ci-toggle');
        if (btn) btn.title = ciHidden ? 'Show confidence intervals' : 'Hide confidence intervals';
        if (btn) btn.querySelector('.dih-fab-action-label').textContent = ciHidden ? 'Show confidence intervals' : 'Hide confidence intervals';
      },
      { order: 30, closeFabOnClick: false }
    );

    if (ciHidden) {
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

  // Dark mode is now handled by Quarto's built-in light/dark theme toggle (see _quarto-manual.yml)

  // ========================================
  // COPY CITATION BUTTON
  // ========================================

  function createCopyCitationButton() {
    var doiMeta = document.querySelector('meta[name="citation_doi"]') ||
                  document.querySelector('meta[name="DC.identifier"]');
    var titleMeta = document.querySelector('meta[name="citation_title"]') ||
                    document.querySelector('meta[property="og:title"]') ||
                    document.querySelector('title');
    var authorMeta = document.querySelector('meta[name="citation_author"]') ||
                     document.querySelector('meta[name="author"]');

    if (!titleMeta) return;

    addFABAction('cite', 'Copy citation (BibTeX)',
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>',
      function() {
        var title = titleMeta.content || titleMeta.textContent || 'Untitled';
        var author = authorMeta ? (authorMeta.content || 'Unknown') : 'Sinn, Mike P.';
        var doi = doiMeta ? doiMeta.content : '';
        var url = window.location.href;
        var year = new Date().getFullYear();

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
          var btn = document.getElementById('dih-fab-cite');
          if (btn) {
            var origLabel = btn.querySelector('.dih-fab-action-label').textContent;
            btn.querySelector('.dih-fab-action-label').textContent = 'Copied!';
            setTimeout(function() {
              btn.querySelector('.dih-fab-action-label').textContent = origLabel;
            }, 2000);
          }
        });
      },
      { order: 20 }
    );
  }

  // ========================================
  // END-OF-CHAPTER SHARE BAR
  // ========================================

  function createShareBar() {
    // Only add on chapter pages (have #quarto-document-content), skip index/links
    var content = document.getElementById('quarto-document-content');
    if (!content) return;
    var path = window.location.pathname;
    if (path === '/' || path === '/index.html' || path.endsWith('/links.html') || path.endsWith('/podcast.html')) return;

    var pageUrl = encodeURIComponent(window.location.href);
    var pageTitle = encodeURIComponent(document.title);

    var bar = document.createElement('div');
    bar.id = 'chapter-share-bar';
    bar.innerHTML =
      '<span class="share-label">Share this chapter</span>' +
      '<div class="share-icons">' +
        '<a href="https://x.com/intent/tweet?url=' + pageUrl + '&text=' + pageTitle + '" target="_blank" rel="noopener" title="Share on X" class="share-icon">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>' +
        '</a>' +
        '<a href="https://www.linkedin.com/sharing/share-offsite/?url=' + pageUrl + '" target="_blank" rel="noopener" title="Share on LinkedIn" class="share-icon">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>' +
        '</a>' +
        '<a href="https://www.reddit.com/submit?url=' + pageUrl + '&title=' + pageTitle + '" target="_blank" rel="noopener" title="Share on Reddit" class="share-icon">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 0-.463.327.327 0 0 0-.462 0c-.545.533-1.684.73-2.512.73-.828 0-1.953-.197-2.498-.73a.327.327 0 0 0-.231-.094z"/></svg>' +
        '</a>' +
        '<a href="https://www.facebook.com/sharer/sharer.php?u=' + pageUrl + '" target="_blank" rel="noopener" title="Share on Facebook" class="share-icon">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>' +
        '</a>' +
        '<a href="mailto:?subject=' + pageTitle + '&body=' + pageUrl + '" title="Share via email" class="share-icon">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>' +
        '</a>' +
        '<button type="button" title="Copy link" class="share-icon" id="share-copy-link">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/></svg>' +
        '</button>' +
      '</div>';

    content.appendChild(bar);

    document.getElementById('share-copy-link').addEventListener('click', function() {
      var btn = this;
      navigator.clipboard.writeText(window.location.href).then(function() {
        btn.classList.add('copied');
        btn.title = 'Copied!';
        setTimeout(function() {
          btn.classList.remove('copied');
          btn.title = 'Copy link';
        }, 2000);
      });
    });
  }

  // ========================================
  // BACK TO TOP BUTTON
  // ========================================

  function createBackToTopButton() {
    addFABAction('top', 'Back to top',
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>',
      function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      },
      { order: 50 }
    );
  }

  // ========================================
  // CHAT LINK (via meta tag, no embedded widget)
  // ========================================

  function createChatLink() {
    var meta = document.querySelector('meta[name="dih-chat-url"]');
    if (!meta || !meta.content) return;
    var chatUrl = meta.content;

    addFABAction('chat', 'Argue with Wishonia',
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>',
      function() {
        window.open(chatUrl, '_blank', 'noopener');
      },
      { order: 10 }
    );
  }

  // ========================================
  // FEATURE FLAGS
  // ========================================

  function getDisabledFeatures() {
    var meta = document.querySelector('meta[name="dih-disable-features"]');
    if (!meta) return [];
    return meta.content.split(',').map(function(f) { return f.trim(); });
  }

  function isFeatureDisabled(name) {
    return getDisabledFeatures().indexOf(name) !== -1;
  }

  // ========================================
  // HIDE INDEX TITLE/DESCRIPTION
  // ========================================

  function hideIndexTitleElements() {
    var meta = document.querySelector('meta[name="dih-hide-index-title"]');
    if (!meta || meta.content !== 'true') return;

    var path = window.location.pathname;
    if (path === '/' || path === '/index.html' || path.endsWith('/index.html')) {
      // Hide title (already in navbar) and description (meta-only), keep subtitle visible
      var title = document.querySelector('#title-block-header .quarto-title > .title');
      if (title) title.style.display = 'none';
      var desc = document.querySelector('#title-block-header .description');
      if (desc) desc.style.display = 'none';
    }
  }

  // ========================================
  // INITIALIZATION
  // ========================================

  // Hide index title/description immediately to avoid flash of content
  hideIndexTitleElements();

  function onPageReady() {
    expandHashTarget();
    createUnifiedFAB();
    //createChatLink();
    if (!isFeatureDisabled('ci-toggle')) createUncertaintyToggle();
    if (!isFeatureDisabled('cite')) createCopyCitationButton();
    if (!isFeatureDisabled('share')) createShareBar();
    createBackToTopButton();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onPageReady, { once: true });
  } else {
    onPageReady();
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
