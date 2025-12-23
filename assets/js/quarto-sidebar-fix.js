/**
 * Quarto Sidebar Width-Based Visibility
 *
 * This script hides the quarto-margin-sidebar when window width is less than 1111px
 * and shows it when window width is greater than or equal to 1111px.
 *
 * Version: 3.0.0 - Performance optimized to eliminate layout thrashing
 */

(function() {
  'use strict';

  let retryCount = 0;
  const MAX_RETRIES = 50; // 10 seconds max (50 × 200ms)
  const WIDTH_THRESHOLD = 1111; // pixels

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

    if (!marginSidebar) {
      // Element not found yet, retry with limit to prevent infinite loop
      if (retryCount < MAX_RETRIES) {
        retryCount++;
        setTimeout(applyFix, 200);
      } else {
        console.warn('Quarto sidebar fix: Required element not found after maximum retries');
      }
      return;
    }

    // Add CSS for rollup state if not already present
    injectStyles();

    // Re-entry guard to prevent observer feedback loops
    let isUpdating = false;

    // Function to hide sidebar (single DOM mutation)
    function hideSidebar() {
      if (marginSidebar.classList.contains('rollup')) {
        return; // Already hidden
      }
      marginSidebar.classList.add('rollup');
    }

    // Function to show sidebar (single DOM mutation)
    function showSidebar() {
      if (!marginSidebar.classList.contains('rollup')) {
        return; // Already shown
      }
      marginSidebar.classList.remove('rollup');
    }

    // Check and update sidebar visibility based on window width
    function updateSidebarVisibility() {
      // Re-entry guard: prevent feedback loops
      if (isUpdating) {
        return;
      }

      isUpdating = true;

      // Use requestAnimationFrame for visual updates to avoid forced reflow
      requestAnimationFrame(() => {
        try {
          // Batch read: read layout property first
          const windowWidth = window.innerWidth || document.documentElement.clientWidth;

          // Batch write: modify DOM after all reads complete
          if (windowWidth < WIDTH_THRESHOLD) {
            hideSidebar();
          } else {
            showSidebar();
          }
        } finally {
          // Always reset the guard, even if an error occurs
          isUpdating = false;
        }
      });
    }

    // Monitor for window resize with debouncing (increased from 50ms to 150ms)
    let resizeTimeout;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(updateSidebarVisibility, 150);
    }, { passive: true });

    // Initial check
    updateSidebarVisibility();
  }

  // Inject CSS styles for .rollup class
  function injectStyles() {
    // Check if styles already injected
    if (document.getElementById('quarto-sidebar-fix-styles')) {
      return;
    }

    const style = document.createElement('style');
    style.id = 'quarto-sidebar-fix-styles';
    style.textContent = `
      #quarto-margin-sidebar.rollup > * {
        opacity: 0 !important;
        overflow: hidden !important;
        pointer-events: none !important;
      }
    `;
    document.head.appendChild(style);
  }
})();
