/**
 * Quarto Sidebar Width-Based Visibility
 *
 * This script hides the quarto-margin-sidebar when window width is less than 1111px
 * and shows it when window width is greater than or equal to 1111px.
 *
 * Version: 2.0.0 - Simplified to width-based visibility only
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

    // Re-entry guard to prevent observer feedback loops
    let isUpdating = false;

    // Function to hide sidebar
    function hideSidebar() {
      // Check if already hidden - prevent unnecessary mutations
      if (marginSidebar.classList.contains('rollup')) {
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
      // Check if already shown - prevent unnecessary mutations
      if (!marginSidebar.classList.contains('rollup')) {
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

    // Check and update sidebar visibility based on window width
    function updateSidebarVisibility() {
      // Re-entry guard: prevent feedback loops
      if (isUpdating) {
        return;
      }

      isUpdating = true;

      try {
        const windowWidth = window.innerWidth || document.documentElement.clientWidth;

        if (windowWidth < WIDTH_THRESHOLD) {
          hideSidebar();
        } else {
          showSidebar();
        }
      } finally {
        // Always reset the guard, even if an error occurs
        isUpdating = false;
      }
    }

    // Monitor for window resize
    let resizeTimeout;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(updateSidebarVisibility, 50);
    });

    // Initial check
    updateSidebarVisibility();
  }
})();
