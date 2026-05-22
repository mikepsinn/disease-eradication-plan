#!/usr/bin/env python3
"""
GitHub Actions Workflow Generator

Auto-generates GitHub Actions workflows from Quarto config files.
Scans all _quarto-*.yml files, extracts metadata, and renders workflow templates.
"""
import sys
if sys.platform == 'win32':
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')

import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List
from urllib.parse import urlparse

logger = logging.getLogger("dih.workflow")

DOWNLOADABLE_FORMATS = ("pdf", "epub", "docx")

# Add project root to path for dih_models imports
_project_root = str(Path(__file__).parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from dih_models.yaml_utils import load_quarto_config

# Handle import from different contexts (direct run vs imported from scripts/)
try:
    from quarto_config_utils import NON_DEPLOYABLE_CONFIGS
except ModuleNotFoundError:
    _lib_dir = Path(__file__).parent
    if str(_lib_dir) not in sys.path:
        sys.path.insert(0, str(_lib_dir))
    from quarto_config_utils import NON_DEPLOYABLE_CONFIGS


@dataclass
class JobConfig:
    """Workflow job configuration extracted from Quarto config."""
    config_name: str              # "economics"
    display_name: str             # "Build Economics Site"
    project_type: str             # "book" or "website"
    timeout_minutes: int          # 10, 25, or 75
    build_dir: str                # "_build_temp/economics/_site/1-pct-treaty-impact"
    configured_formats: List[str] # e.g. ["html", "pdf"]
    downloadable_formats: List[str]  # subset of configured_formats
    artifact_render_format: str | None  # explicit --to format, or None for all configured formats
    netlify_site_id: str | None   # Configured site ID, used as a deploy opt-in
    netlify_secret: str           # GitHub secret that stores the deploy site ID
    upload_to_zenodo: bool        # True for papers
    deploy_to_netlify: bool       # True for all

    @classmethod
    def from_quarto_config(cls, config_path: Path, manual_host: str | None = None) -> "JobConfig":
        """Extract job config from _quarto-*.yml file."""
        config_name = config_path.stem.replace("_quarto-", "")

        config = load_quarto_config(config_path)

        # Extract metadata
        project_type = config['project']['type']
        output_dir = config['project']['output-dir']

        # Get title from book or website section
        if project_type == 'book':
            title = config.get('book', {}).get('title', '')
        else:
            title = config.get('website', {}).get('title', '')

        # Get Netlify site ID from dih-render section for setup inventory and deploy opt-in
        dih_render = config.get('dih-render', {})
        netlify_site_id = dih_render.get('netlify-site-id')
        site_url = get_config_site_url(config)
        configured_formats = list(config.get('format', {}).keys())
        downloadable_formats = [fmt for fmt in configured_formats if fmt in DOWNLOADABLE_FORMATS]
        artifact_render_format = infer_artifact_render_format(
            configured_formats=configured_formats,
            downloadable_formats=downloadable_formats,
        )

        # Derive values
        display_name = derive_display_name(config_name, title)
        timeout = infer_timeout(config_name, project_type)
        build_dir = infer_build_dir(config_name, output_dir, project_type)
        netlify_secret = derive_netlify_secret(config_name)
        upload_zenodo = should_upload_to_zenodo(config_name, config)
        deploy_to_netlify = should_deploy_to_netlify(
            config_name=config_name,
            site_url=site_url,
            netlify_site_id=netlify_site_id,
            manual_host=manual_host,
        )

        return cls(
            config_name=config_name,
            display_name=display_name,
            project_type=project_type,
            timeout_minutes=timeout,
            build_dir=build_dir,
            configured_formats=configured_formats,
            downloadable_formats=downloadable_formats,
            artifact_render_format=artifact_render_format,
            netlify_site_id=netlify_site_id,
            netlify_secret=netlify_secret,
            upload_to_zenodo=upload_zenodo,
            deploy_to_netlify=deploy_to_netlify,
        )


def get_config_site_url(config: dict) -> str | None:
    """Extract canonical site URL from website or book config."""
    return (
        config.get('website', {}).get('site-url')
        or config.get('book', {}).get('site-url')
    )


def get_hostname(url: str | None) -> str | None:
    """Extract lowercase hostname from URL."""
    if not url:
        return None
    hostname = urlparse(url).hostname
    return hostname.lower() if hostname else None


def infer_artifact_render_format(
    configured_formats: List[str],
    downloadable_formats: List[str],
) -> str | None:
    """
    Choose the most efficient render mode for artifact builds.

    Single downloadable format configs render that format only.
    Multi-format artifact configs render all configured formats.
    """
    if not downloadable_formats:
        return None

    if len(downloadable_formats) == 1:
        return downloadable_formats[0]

    return None


def derive_display_name(config_name: str, title: str) -> str:
    """Derive job display name from config name and title."""
    if config_name == "book":
        return "Build Main Book (HTML + PDF + EPUB)"
    elif title:
        # Use title if available
        return f"Build {title[:50]}"  # Limit length
    else:
        # Fallback to config name
        return f"Build {config_name.replace('-', ' ').title()}"


def infer_timeout(config_name: str, project_type: str) -> int:
    """Infer build timeout based on config and project type."""
    if config_name == "book":
        return 75  # HTML + PDF + EPUB
    elif config_name == "manual":
        return 75  # Large multi-format build
    else:
        return 30  # Standard papers and larger papers


def infer_build_dir(config_name: str, output_dir: str, project_type: str) -> str:
    """Infer build directory path from config metadata."""
    # Use output-dir directly from Quarto config - it's the source of truth
    # Pattern: _build_temp/{config}/{output_dir}
    return f"_build_temp/{config_name}/{output_dir}"


def derive_netlify_secret(config_name: str) -> str:
    """Derive Netlify secret name from config name."""
    if config_name in ("book", "manual"):
        return "NETLIFY_MAIN_SITE_ID"
    return f"NETLIFY_{config_name.upper().replace('-', '_')}_SITE_ID"


def should_upload_to_zenodo(config_name: str, config: dict) -> bool:
    """Determine if this config should upload to Zenodo."""
    # Skip for main book and test
    if config_name in ("book", "test"):
        return False
    # Check explicit zenodo flag in dih-render
    dih_render = config.get('dih-render', {})
    if dih_render.get('zenodo') is False:
        return False
    return True


def should_deploy_to_netlify(
    config_name: str,
    site_url: str | None,
    netlify_site_id: str | None,
    manual_host: str | None,
) -> bool:
    """
    Decide whether this config should get its own Netlify deploy job.

    Path-based papers that now live under the manual host are rendered and
    validated independently, but they should not deploy to their legacy
    standalone Netlify sites.
    """
    if not netlify_site_id:
        return False

    if config_name in {"manual", "book"}:
        return True

    site_host = get_hostname(site_url)
    if manual_host and site_host == manual_host:
        return False

    return True


def extract_job_configs(project_root: Path) -> List[JobConfig]:
    """
    Scan _quarto-*.yml files and extract workflow job configs.

    Returns:
        List of JobConfig objects, one per discovered config
    """
    configs = []

    manual_host = None
    manual_config_path = project_root / "_quarto-manual.yml"
    if manual_config_path.exists():
        try:
            manual_config = load_quarto_config(manual_config_path)
            manual_host = get_hostname(get_config_site_url(manual_config))
        except Exception as e:
            logger.warning("Could not determine manual host from %s: %s", manual_config_path.name, e)

    for yml_path in project_root.glob("_quarto-*.yml"):
        # Skip build temp files
        if "_build_temp" in str(yml_path):
            continue

        # Skip non-deployable configs (test, shared-defaults, etc.)
        config_name = yml_path.stem.replace("_quarto-", "")
        if config_name in NON_DEPLOYABLE_CONFIGS or not config_name or config_name == "quarto":
            continue

        try:
            job_config = JobConfig.from_quarto_config(yml_path, manual_host=manual_host)
            configs.append(job_config)
        except Exception as e:
            logger.warning("Skipping %s: %s", yml_path.name, e)

    # Sort by config name for consistent ordering
    return sorted(configs, key=lambda c: c.config_name)


def extract_deploy_job_configs(project_root: Path) -> List[JobConfig]:
    """Get jobs that should deploy to Netlify."""
    return [job for job in extract_job_configs(project_root) if job.deploy_to_netlify]


def extract_artifact_job_configs(project_root: Path) -> List[JobConfig]:
    """Get jobs that produce downloadable artifacts (pdf/epub/docx)."""
    return [job for job in extract_job_configs(project_root) if job.downloadable_formats]


def generate_workflow(project_root: Path, job_configs: List[JobConfig], template_name: str) -> str:
    """
    Generate workflow content from template and job configs.

    Args:
        project_root: Project root directory
        job_configs: List of job configurations
        template_name: Jinja template filename

    Returns:
        Generated workflow YAML content
    """
    from jinja2 import Environment, FileSystemLoader

    template_dir = project_root / "scripts" / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template(template_name)

    return template.render(jobs=job_configs)


def regenerate_workflow(project_root: Path) -> None:
    """
    Main entry point: regenerate GitHub Actions workflows from Quarto configs.

    1. Scan _quarto-*.yml files
    2. Extract deploy and artifact job configurations
    3. Render templates
    4. Write to .github/workflows/*.yml
    """
    logger.debug("Regenerating GitHub Actions workflows from Quarto configs...")

    deploy_jobs = extract_deploy_job_configs(project_root)
    artifact_jobs = extract_artifact_job_configs(project_root)
    logger.debug("Found %d deploy job(s)", len(deploy_jobs))
    logger.debug("Found %d artifact job(s)", len(artifact_jobs))

    if not deploy_jobs and not artifact_jobs:
        print("[ERROR] No Quarto workflow jobs found!", file=sys.stderr)
        return

    workflows_dir = project_root / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    if deploy_jobs:
        publish_content = generate_workflow(
            project_root,
            deploy_jobs,
            template_name="publish.yml.j2",
        )
        publish_path = workflows_dir / "publish.yml"
        publish_path.write_text(publish_content, encoding='utf-8')
        logger.debug("Generated %s", publish_path)
        logger.debug("     deploy jobs: %s", ", ".join(c.config_name for c in deploy_jobs))

    if artifact_jobs:
        artifacts_content = generate_workflow(
            project_root,
            artifact_jobs,
            template_name="build-artifacts.yml.j2",
        )
        artifacts_path = workflows_dir / "build-artifacts.yml"
        artifacts_path.write_text(artifacts_content, encoding='utf-8')
        logger.debug("Generated %s", artifacts_path)
        logger.debug("     artifact jobs: %s", ", ".join(c.config_name for c in artifact_jobs))


if __name__ == "__main__":
    # Allow running directly for testing
    project_root = Path(__file__).parent.parent.parent
    regenerate_workflow(project_root)
