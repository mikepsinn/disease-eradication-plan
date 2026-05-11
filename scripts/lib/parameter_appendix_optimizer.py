#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post-process rendered parameter appendix HTML for faster initial loading."""

import re
from pathlib import Path


PARAMETER_APPENDIX_PLACEHOLDER_IMAGE = (
    "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="
)

PARAMETER_APPENDIX_IMAGE_HYDRATOR_ID = "dih-parameter-appendix-image-hydrator"
PARAMETER_APPENDIX_MATHJAX_CONFIG_ID = "dih-parameter-appendix-mathjax-config"

PARAMETER_APPENDIX_MATHJAX_CONFIG = f"""
<script id="{PARAMETER_APPENDIX_MATHJAX_CONFIG_ID}">
window.MathJax = window.MathJax || {{}};
window.MathJax.startup = window.MathJax.startup || {{}};
window.MathJax.startup.typeset = false;
</script>
""".strip()

PARAMETER_APPENDIX_IMAGE_HYDRATOR = f"""
<script id="{PARAMETER_APPENDIX_IMAGE_HYDRATOR_ID}">
(function() {{
  'use strict';

  var imageSelector = 'img[data-parameter-lazy-chart="true"][data-src]';
  var mathSelector = '.math';

  function hydrateImage(img) {{
    var src = img.getAttribute('data-src');
    if (!src) return;
    img.setAttribute('src', src);
    img.removeAttribute('data-src');
    img.setAttribute('data-parameter-chart-loaded', 'true');
  }}

  function hydrateParameterAppendixImages(root) {{
    root = root || document;
    if (root.matches && root.matches(imageSelector)) {{
      hydrateImage(root);
    }}

    var images = root.querySelectorAll ? root.querySelectorAll(imageSelector) : [];
    for (var i = 0; i < images.length; i++) {{
      hydrateImage(images[i]);
    }}
  }}

  function typesetParameterAppendixMath(root) {{
    root = root || document;
    if (!window.MathJax) return;
    if (root.getAttribute && root.getAttribute('data-parameter-math-typeset') === 'true') return;

    var hasMath = root.matches && root.matches(mathSelector);
    if (!hasMath && root.querySelector) {{
      hasMath = !!root.querySelector(mathSelector);
    }}
    if (!hasMath) return;

    if (window.MathJax.typesetPromise) {{
      window.MathJax.typesetPromise([root]).then(function() {{
        if (root.setAttribute) {{
          root.setAttribute('data-parameter-math-typeset', 'true');
        }}
      }});
      return;
    }}

    if (window.MathJax.typeset) {{
      window.MathJax.typeset([root]);
      if (root.setAttribute) {{
        root.setAttribute('data-parameter-math-typeset', 'true');
      }}
    }}
  }}

  function hydrateParameterAppendixDetails(root) {{
    hydrateParameterAppendixImages(root);
    typesetParameterAppendixMath(root);
  }}

  function hashTarget() {{
    if (!window.location.hash || window.location.hash.length < 2) return null;

    return document.getElementById(window.location.hash.slice(1));
  }}

  function hydrateHashTarget() {{
    var target = hashTarget();
    if (!target) return;

    hydrateParameterAppendixDetails(target);

    var containingCallout = target.closest ? target.closest('.callout') : null;
    if (containingCallout) {{
      hydrateParameterAppendixDetails(containingCallout);
    }}

    var firstCallout = target.querySelector ? target.querySelector('.callout') : null;
    if (firstCallout) {{
      hydrateParameterAppendixDetails(firstCallout);
    }}
  }}

  function hydrateToggleTarget(toggle) {{
    var targetSelector = toggle.getAttribute('data-bs-target') || toggle.getAttribute('href');
    var target = null;

    if (targetSelector && targetSelector.charAt(0) === '#') {{
      target = document.getElementById(targetSelector.slice(1));
    }}

    if (!target) {{
      var controls = toggle.getAttribute('aria-controls');
      if (controls) {{
        target = document.getElementById(controls);
      }}
    }}

    if (target) {{
      hydrateParameterAppendixDetails(target);
      return;
    }}

    var callout = toggle.closest ? toggle.closest('.callout') : null;
    if (callout) {{
      hydrateParameterAppendixDetails(callout);
    }}
  }}

  function observeVisibleImages() {{
    if (!('IntersectionObserver' in window)) return;

    var observer = new IntersectionObserver(function(entries) {{
      for (var i = 0; i < entries.length; i++) {{
        if (entries[i].isIntersecting) {{
          hydrateImage(entries[i].target);
          observer.unobserve(entries[i].target);
        }}
      }}
    }}, {{ rootMargin: '600px 0px' }});

    var images = document.querySelectorAll(imageSelector);
    for (var j = 0; j < images.length; j++) {{
      observer.observe(images[j]);
    }}
  }}

  function init() {{
    hydrateHashTarget();
    observeVisibleImages();
  }}

  document.addEventListener('dih:hash-target-ready', hydrateHashTarget, false);
  document.addEventListener('shown.bs.collapse', function(event) {{
    hydrateParameterAppendixDetails(event.target);
  }}, true);
  document.addEventListener('click', function(event) {{
    var toggle = event.target.closest
      ? event.target.closest('[data-bs-toggle="collapse"], .callout-btn-toggle')
      : null;
    if (toggle) {{
      window.setTimeout(function() {{
        hydrateToggleTarget(toggle);
      }}, 0);
    }}
  }}, true);
  window.addEventListener('hashchange', function() {{
    window.setTimeout(hydrateHashTarget, 0);
  }});

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', init, {{ once: true }});
  }} else {{
    init();
  }}

  window.hydrateParameterAppendixImages = hydrateParameterAppendixImages;
  window.typesetParameterAppendixMath = typesetParameterAppendixMath;
}})();
</script>
""".strip()


def _defer_parameters_appendix_img_tags(html: str) -> tuple[str, int]:
    """Defer parameter appendix chart URLs until the target or opened section needs them."""
    count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal count
        attrs = match.group(1)
        if re.search(r'\sdata-parameter-lazy-chart=', attrs, re.IGNORECASE):
            return match.group(0)

        src_match = re.search(r'\ssrc=(["\'])(.*?)\1', attrs, re.IGNORECASE)
        if not src_match:
            return match.group(0)

        quote = src_match.group(1)
        src = src_match.group(2)
        if src.startswith("data:"):
            return match.group(0)

        replacement = (
            f' src="{PARAMETER_APPENDIX_PLACEHOLDER_IMAGE}"'
            f" data-src={quote}{src}{quote}"
        )
        updated = attrs[:src_match.start()] + replacement + attrs[src_match.end():]

        if not re.search(r'\sloading=', updated, re.IGNORECASE):
            updated += ' loading="lazy"'
        if not re.search(r'\sdecoding=', updated, re.IGNORECASE):
            updated += ' decoding="async"'
        if not re.search(r'\sfetchpriority=', updated, re.IGNORECASE):
            updated += ' fetchpriority="low"'
        if not re.search(r'\sdata-parameter-lazy-chart=', updated, re.IGNORECASE):
            updated += ' data-parameter-lazy-chart="true"'

        count += 1
        return f"<img{updated}>"

    updated_html = re.sub(r"<img([^>]*?)>", replace, html, flags=re.IGNORECASE)
    return updated_html, count


def _inject_parameters_appendix_hydrator(html: str) -> str:
    if PARAMETER_APPENDIX_IMAGE_HYDRATOR_ID in html:
        return html

    body_close = re.search(r"</body\s*>", html, flags=re.IGNORECASE)
    if not body_close:
        return html + "\n" + PARAMETER_APPENDIX_IMAGE_HYDRATOR + "\n"

    return html[:body_close.start()] + PARAMETER_APPENDIX_IMAGE_HYDRATOR + "\n" + html[body_close.start():]


def _inject_parameters_appendix_mathjax_config(html: str) -> str:
    if PARAMETER_APPENDIX_MATHJAX_CONFIG_ID in html:
        return html

    mathjax_script = re.search(
        r'<script\b[^>]*\bsrc=(["\'])[^"\']*mathjax[^"\']*tex-chtml[^"\']*\1[^>]*>\s*</script>',
        html,
        flags=re.IGNORECASE,
    )
    if not mathjax_script:
        return html

    return (
        html[:mathjax_script.start()]
        + PARAMETER_APPENDIX_MATHJAX_CONFIG
        + "\n"
        + html[mathjax_script.start():]
    )


def _defer_parameters_appendix_mathjax_script(html: str) -> str:
    def replace(match: re.Match[str]) -> str:
        script_tag = match.group(0)
        if re.search(r'\sdefer(?:[\s=>]|$)', script_tag, flags=re.IGNORECASE):
            return script_tag

        return re.sub(r">\s*</script>\s*$", " defer></script>", script_tag, flags=re.IGNORECASE)

    return re.sub(
        r'<script\b[^>]*\bsrc=(["\'])[^"\']*mathjax[^"\']*tex-chtml[^"\']*\1[^>]*>\s*</script>',
        replace,
        html,
        count=1,
        flags=re.IGNORECASE,
    )


def optimize_parameters_appendix_html(output_dir: Path) -> int:
    """
    Post-process rendered parameter appendix pages so chart images load on demand.

    Quarto/Jupyter plot outputs are injected after the Pandoc filter stage, so
    the reliable place to defer chart src attributes is the final HTML.
    """
    total_updated = 0

    for html_path in output_dir.rglob("parameters-and-calculations*.html"):
        html = html_path.read_text(encoding="utf-8")
        updated_html, updated_count = _defer_parameters_appendix_img_tags(html)
        if updated_count == 0:
            continue

        updated_html = _inject_parameters_appendix_hydrator(updated_html)
        updated_html = _defer_parameters_appendix_mathjax_script(updated_html)
        updated_html = _inject_parameters_appendix_mathjax_config(updated_html)
        html_path.write_text(updated_html, encoding="utf-8", newline='\n')
        total_updated += updated_count

    return total_updated
