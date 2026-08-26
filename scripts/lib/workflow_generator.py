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

logger = logging.getLogger("dih.workflow")

DOWNLOADABLE_FORMATS = ("pdf", "epub", "docx")
GENERATED_WORKFLOW_HEADER = """# AUTO-GENERATED FILE. DO NOT EDIT DIRECTLY.
# Source: scripts/templates/{template_name}
# Generator: scripts/lib/workflow_generator.py
# Make changes in the source template or generator, then regenerate.

"""

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
    bundle_pdf_with_site: bool     # Render and bundle the PDF before the HTML deploy
    cloudflare_pages_project: str | None  # Explicit Pages project name and deploy opt-in
    upload_to_zenodo: bool        # True for papers
    deploy_to_cloudflare: bool    # True when cloudflare-pages-project is configured

    @classmethod
    def from_quarto_config(cls, config_path: Path) -> "JobConfig":
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

        # An explicit Pages project opts this config into production deployment.
        dih_render = config.get('dih-render', {})
        cloudflare_pages_project = dih_render.get('cloudflare-pages-project')
        configured_formats = list(config.get('format', {}).keys())
        downloadable_formats = [fmt for fmt in configured_formats if fmt in DOWNLOADABLE_FORMATS]
        artifact_render_format = infer_artifact_render_format(
            configured_formats=configured_formats,
            downloadable_formats=downloadable_formats,
        )
        bundle_pdf_with_site = bool(
            'html' in configured_formats
            and 'pdf' in configured_formats
            and dih_render.get('pdf-output-file')
        )

        # Derive values
        display_name = derive_display_name(config_name, title)
        timeout = infer_timeout(config_name, project_type)
        build_dir = infer_build_dir(config_name, output_dir, project_type)
        upload_zenodo = should_upload_to_zenodo(config_name, config)
        deploy_to_cloudflare = bool(cloudflare_pages_project)

        return cls(
            config_name=config_name,
            display_name=display_name,
            project_type=project_type,
            timeout_minutes=timeout,
            build_dir=build_dir,
            configured_formats=configured_formats,
            downloadable_formats=downloadable_formats,
            artifact_render_format=artifact_render_format,
            bundle_pdf_with_site=bundle_pdf_with_site,
            cloudflare_pages_project=cloudflare_pages_project,
            upload_to_zenodo=upload_zenodo,
            deploy_to_cloudflare=deploy_to_cloudflare,
        )


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


def extract_job_configs(project_root: Path) -> List[JobConfig]:
    """
    Scan _quarto-*.yml files and extract workflow job configs.

    Returns:
        List of JobConfig objects, one per discovered config
    """
    configs = []

    for yml_path in project_root.glob("_quarto-*.yml"):
        # Skip build temp files
        if "_build_temp" in str(yml_path):
            continue

        # Skip non-deployable configs (test, shared-defaults, etc.)
        config_name = yml_path.stem.replace("_quarto-", "")
        if config_name in NON_DEPLOYABLE_CONFIGS or not config_name or config_name == "quarto":
            continue

        try:
            job_config = JobConfig.from_quarto_config(yml_path)
            configs.append(job_config)
        except Exception as e:
            logger.warning("Skipping %s: %s", yml_path.name, e)

    # Sort by config name for consistent ordering
    return sorted(configs, key=lambda c: c.config_name)


def extract_deploy_job_configs(project_root: Path) -> List[JobConfig]:
    """Get jobs that should deploy to Cloudflare Pages."""
    return [job for job in extract_job_configs(project_root) if job.deploy_to_cloudflare]


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

    header = GENERATED_WORKFLOW_HEADER.format(template_name=template_name)
    return header + template.render(jobs=job_configs)


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
