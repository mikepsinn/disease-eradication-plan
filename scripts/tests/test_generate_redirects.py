import importlib.util
import json
import sys
from pathlib import Path

from dih_models.subdomain_redirects_generator import collect_subdomain_redirects

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore


def load_generate_redirects_module():
    module_path = Path(__file__).resolve().parents[1] / "generate_redirects.py"
    spec = importlib.util.spec_from_file_location("generate_redirects", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_paper_config(root: Path, name: str, redirect_from: str, site_url: str) -> None:
    (root / f"_quarto-{name}.yml").write_text(
        f"dih-render:\n  redirect-from: {redirect_from}\nwebsite:\n  site-url: {site_url}\n",
        encoding="utf-8",
    )


def test_a_paper_can_redirect_from_one_legacy_host_or_several(tmp_path: Path) -> None:
    write_paper_config(tmp_path, "one", "https://one.warondisease.org", "https://papers.example.org/one.html")
    write_paper_config(
        tmp_path,
        "many",
        "\n    - https://many.warondisease.org\n    - https://Many-Protocol.acceleratedmedicine.org",
        "https://papers.example.org/many.html/",
    )

    redirects = collect_subdomain_redirects(tmp_path)

    assert redirects["one.warondisease.org"] == "https://papers.example.org/one.html"
    assert redirects["many.warondisease.org"] == "https://papers.example.org/many.html"
    assert redirects["many-protocol.acceleratedmedicine.org"] == "https://papers.example.org/many.html"


def test_a_legacy_host_can_redirect_to_one_page_of_a_site(tmp_path: Path) -> None:
    (tmp_path / "_quarto-manual.yml").write_text(
        "dih-render:\n"
        "  page-redirects:\n"
        "    - from: https://listen.warondisease.org\n"
        "      to: knowledge/podcast.html\n"
        "book:\n  site-url: https://manual.WarOnDisease.org\n",
        encoding="utf-8",
    )

    redirects = collect_subdomain_redirects(tmp_path)

    # The mixed-case host in site-url must not leak into redirect targets.
    assert redirects == {"listen.warondisease.org": "https://manual.warondisease.org/knowledge/podcast.html"}


def test_every_redirect_is_declared_in_a_quarto_config() -> None:
    """The configs are the single source of truth: no host lists in generator code."""
    project_root = Path(__file__).resolve().parents[2]
    declared = collect_subdomain_redirects(project_root)
    generated = json.loads(
        (project_root / "cloudflare" / "redirect-worker" / "redirect-map.json").read_text(encoding="utf-8")
    )

    assert generated == declared


def test_worker_routes_cover_every_zone_that_has_legacy_hosts(tmp_path: Path) -> None:
    module = load_generate_redirects_module()
    write_paper_config(
        tmp_path,
        "spec",
        "\n    - https://dfda-spec.warondisease.org\n    - https://dfda-protocol.acceleratedmedicine.org\n    - https://spec.dfda.earth",
        "https://papers.acceleratedmedicine.org/dfda-protocol.html",
    )

    module.generate_cloudflare_redirects(tmp_path)

    worker_dir = tmp_path / "cloudflare" / "redirect-worker"
    config_text = (worker_dir / "wrangler.jsonc").read_text(encoding="utf-8")
    config = json.loads(config_text[config_text.index("{"):])
    routes = {(route["pattern"], route["zone_name"]) for route in config["routes"]}
    assert ("dfda-spec.warondisease.org/*", "warondisease.org") in routes
    assert ("dfda-protocol.acceleratedmedicine.org/*", "acceleratedmedicine.org") in routes
    assert ("spec.dfda.earth/*", "dfda.earth") in routes
    # The papers site itself must never be routed to the Worker.
    assert not any(pattern.startswith("papers.acceleratedmedicine.org") for pattern, _ in routes)
