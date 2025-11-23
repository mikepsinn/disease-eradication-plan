/**
 * Quarto Sidebar Horizontal Overlap Fix
 * 
 * This script fixes an issue where the quarto-margin-sidebar overlaps
 * the main content at medium screen widths (around 50% of screen width).
 * 
 * The fix adds horizontal overlap detection to the sidebar visibility logic,
 * ensuring the sidebar is hidden when it would overlap the main content area.
 */

(function() {
  'use strict';

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    // Wait a bit for Quarto's scripts to load
    setTimeout(applyFix, 100);
  }

  function applyFix() {
    const marginSidebar = document.getElementById('quarto-margin-sidebar');
    const documentContent = document.getElementById('quarto-document-content');
    
    if (!marginSidebar || !documentContent) {
      // Elements not found yet, try again later
      setTimeout(applyFix, 200);
      return;
    }

    // Function to check for horizontal overlap
    function checkHorizontalOverlap() {
      const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
      const contentRect = documentContent.getBoundingClientRect();
      const sidebarRect = marginSidebar.getBoundingClientRect();
      
      // Check if sidebar overlaps content horizontally
      const overlapBuffer = 20; // pixels of buffer
      const hasOverlap = sidebarRect.left < contentRect.right + overlapBuffer;
      
      // Also check if viewport is in problematic range (768px - 1000px)
      const inProblematicRange = viewportWidth < 1000 && viewportWidth > 768;
      
      return hasOverlap || inProblematicRange;
    }

    // Function to hide sidebar by converting to menu (mimicking Quarto's behavior)
    function hideSidebar() {
      // Only hide if not already hidden by Quarto's toggle
      const toggleExists = document.getElementById('quarto-toc-toggle');
      if (toggleExists) {
        // Quarto is already managing it, don't interfere
        return;
      }
      
      const sidebarChildren = marginSidebar.children;
      for (const child of sidebarChildren) {
        child.style.opacity = '0';
        child.style.overflow = 'hidden';
        child.style.pointerEvents = 'none';
      }
      marginSidebar.classList.add('rollup');
    }

    // Function to show sidebar
    function showSidebar() {
      // Only show if we're the ones who hid it (check for our rollup class)
      // and if Quarto's toggle doesn't exist
      const toggleExists = document.getElementById('quarto-toc-toggle');
      if (toggleExists) {
        // Quarto is managing it, don't interfere
        return;
      }
      
      const sidebarChildren = marginSidebar.children;
      for (const child of sidebarChildren) {
        child.style.opacity = '1';
        child.style.overflow = '';
        child.style.pointerEvents = '';
      }
      marginSidebar.classList.remove('rollup');
    }

    // Check and update sidebar visibility
    function updateSidebarVisibility() {
      // Only act if not in reader mode
      const isReaderMode = window.localStorage?.getItem('quarto-reader-mode') === 'true';
      if (isReaderMode) {
        return;
      }

      // Check if Quarto's toggle exists - if it does, Quarto is managing visibility
      const toggleExists = document.getElementById('quarto-toc-toggle');
      if (toggleExists) {
        // Quarto is managing it, don't interfere
        return;
      }

      // Only apply our fix if Quarto hasn't already converted it to a menu
      if (checkHorizontalOverlap()) {
        hideSidebar();
      } else {
        // Only show if we hid it (has rollup class but no toggle)
        if (marginSidebar.classList.contains('rollup')) {
          showSidebar();
        }
      }
    }

    // Monitor for changes
    let resizeTimeout;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(updateSidebarVisibility, 50);
    });

    let scrollTimeout;
    window.addEventListener('scroll', function() {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(updateSidebarVisibility, 50);
    });

    // Use MutationObserver to watch for changes to the sidebar
    const observer = new MutationObserver(function(mutations) {
      updateSidebarVisibility();
    });

    observer.observe(marginSidebar, {
      attributes: true,
      attributeFilter: ['class', 'style'],
      childList: false,
      subtree: false
    });

    // Initial check
    updateSidebarVisibility();

    // Also hook into Quarto's hideOverlappedSidebars if it exists
    // This ensures our check runs when Quarto's own visibility logic runs
    const originalHideOverlapped = window.hideOverlappedSidebars;
    if (typeof originalHideOverlapped === 'function') {
      window.hideOverlappedSidebars = function() {
        originalHideOverlapped.apply(this, arguments);
        updateSidebarVisibility();
      };
    }
  }
})();

