import importlib.util
import re
from pathlib import Path


def load_parameter_appendix_optimizer_module():
    module_path = Path(__file__).resolve().parents[1] / "lib" / "parameter_appendix_optimizer.py"
    spec = importlib.util.spec_from_file_location("parameter_appendix_optimizer", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parameters_appendix_images_are_deferred_until_hydration(tmp_path: Path) -> None:
    module = load_parameter_appendix_optimizer_module()
    html_path = tmp_path / "parameters-and-calculations.html"
    html_path.write_text(
        """<!doctype html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js" type="text/javascript"></script>
</head>
<body>
<section id="sec-target">
  <div class="callout">
    <div class="callout-collapse">
      <span class="math display">\\[x=1\\]</span>
      <img src="parameters-and-calculations_files/figure-html/cell-1-output-1.png" width="100" height="50">
    </div>
  </div>
</section>
<section id="sec-other">
  <div class="callout">
    <div class="callout-collapse">
      <img src="parameters-and-calculations_files/figure-html/cell-2-output-1.png" width="100" height="50">
    </div>
  </div>
</section>
</body>
</html>
""",
        encoding="utf-8",
    )

    updated = module.optimize_parameters_appendix_html(tmp_path)

    output = html_path.read_text(encoding="utf-8")
    assert updated == 2
    assert 'data-src="parameters-and-calculations_files/figure-html/cell-1-output-1.png"' in output
    assert 'data-src="parameters-and-calculations_files/figure-html/cell-2-output-1.png"' in output
    src_values = re.findall(r'(?<!data-)src="([^"]+)"', output)
    assert "parameters-and-calculations_files/figure-html/cell-1-output-1.png" not in src_values
    assert "parameters-and-calculations_files/figure-html/cell-2-output-1.png" not in src_values
    assert src_values.count(module.PARAMETER_APPENDIX_PLACEHOLDER_IMAGE) == 2
    assert 'data-parameter-lazy-chart="true"' in output
    assert "hydrateParameterAppendixImages" in output
    assert "dih:hash-target-ready" in output
    assert "shown.bs.collapse" in output
    assert "typesetParameterAppendixMath" in output
    assert "data-parameter-math-typeset" in output
    assert "dih-parameter-appendix-mathjax-config" in output
    assert output.index("dih-parameter-appendix-mathjax-config") < output.index("tex-chtml-full.js")
    mathjax_tag = re.search(r'<script[^>]*tex-chtml-full\.js[^>]*></script>', output)
    assert mathjax_tag is not None
    assert "defer" in mathjax_tag.group(0)


def test_parameters_appendix_optimizer_ignores_data_images(tmp_path: Path) -> None:
    module = load_parameter_appendix_optimizer_module()
    html_path = tmp_path / "parameters-and-calculations.html"
    html_path.write_text(
        """<!doctype html>
<html>
<body>
<img src="data:image/png;base64,abc" width="1" height="1">
</body>
</html>
""",
        encoding="utf-8",
    )

    updated = module.optimize_parameters_appendix_html(tmp_path)

    output = html_path.read_text(encoding="utf-8")
    assert updated == 0
    assert 'src="data:image/png;base64,abc"' in output
    assert "data-parameter-lazy-chart" not in output
