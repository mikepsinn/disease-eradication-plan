#!/usr/bin/env python3
"""
GitHub Actions Workflow Generator

Auto-generates .github/workflows/publish.yml from Quarto config files.
Scans all _quarto-*.yml files, extracts metadata, and renders workflow template.
"""
import sys
if sys.platform == 'win32':
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')

from dataclasses import dataclass
from pathlib import Path
from typing import List
import yaml


@dataclass
class JobConfig:
    """Workflow job configuration extracted from Quarto config."""
    config_name: str              # "economics"
    display_name: str             # "Build Economics Site"
    project_type: str             # "book" or "website"
    timeout_minutes: int          # 10, 25, or 75
    build_dir: str                # "_build_temp/economics/_site/1-pct-treaty-impact"
    netlify_site_id: str | None   # Direct site ID from config (preferred)
    netlify_secret: str           # Fallback: "NETLIFY_ECONOMICS_SITE_ID"
    upload_to_zenodo: bool        # True for papers
    deploy_to_netlify: bool       # True for all

    @classmethod
    def from_quarto_config(cls, config_path: Path) -> "JobConfig":
        """Extract job config from _quarto-*.yml file."""
        config_name = config_path.stem.replace("_quarto-", "")

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # Extract metadata
        project_type = config['project']['type']
        output_dir = config['project']['output-dir']

        # Get title from book or website section
        if project_type == 'book':
            title = config.get('book', {}).get('title', '')
        else:
            title = config.get('website', {}).get('title', '')

        # Get Netlify site ID from dih-render section (preferred over secrets)
        dih_render = config.get('dih-render', {})
        netlify_site_id = dih_render.get('netlify-site-id')

        # Derive values
        display_name = derive_display_name(config_name, title)
        timeout = infer_timeout(config_name, project_type)
        build_dir = infer_build_dir(config_name, output_dir, project_type)
        netlify_secret = derive_netlify_secret(config_name)
        upload_zenodo = should_upload_to_zenodo(config_name, config)

        return cls(
            config_name=config_name,
            display_name=display_name,
            project_type=project_type,
            timeout_minutes=timeout,
            build_dir=build_dir,
            netlify_site_id=netlify_site_id,
            netlify_secret=netlify_secret,
            upload_to_zenodo=upload_zenodo,
            deploy_to_netlify=bool(netlify_site_id)  # Only deploy if site ID configured
        )


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
    else:
        return 30  # Standard papers and larger papers


def infer_build_dir(config_name: str, output_dir: str, project_type: str) -> str:
    """Infer build directory path from config metadata."""
    if project_type == "book":
        # Pattern: _build_temp/{config}/_book/{output_dir_name}
        dir_name = Path(output_dir).name
        return f"_build_temp/{config_name}/_book/{dir_name}"
    else:
        # Pattern: _build_temp/{config}/_site/{config}
        return f"_build_temp/{config_name}/_site/{config_name}"


def derive_netlify_secret(config_name: str) -> str:
    """Derive Netlify secret name from config name."""
    if config_name == "book":
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

        try:
            job_config = JobConfig.from_quarto_config(yml_path)
            configs.append(job_config)
        except Exception as e:
            print(f"[WARN] Skipping {yml_path.name}: {e}")

    # Sort by config name for consistent ordering
    return sorted(configs, key=lambda c: c.config_name)


def generate_workflow(project_root: Path, job_configs: List[JobConfig]) -> str:
    """
    Generate publish.yml content from template and job configs.

    Args:
        project_root: Project root directory
        job_configs: List of job configurations

    Returns:
        Generated workflow YAML content
    """
    from jinja2 import Environment, FileSystemLoader

    template_dir = project_root / "scripts" / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template("publish.yml.j2")

    return template.render(jobs=job_configs)


def regenerate_workflow(project_root: Path) -> None:
    """
    Main entry point: regenerate GitHub Actions workflow from Quarto configs.

    1. Scan _quarto-*.yml files
    2. Extract job configurations
    3. Render template
    4. Write to .github/workflows/publish.yml
    """
    print("[*] Regenerating GitHub Actions workflow from Quarto configs...")

    # Extract configs
    job_configs = extract_job_configs(project_root)
    print(f"[*] Found {len(job_configs)} Quarto configurations")

    if not job_configs:
        print("[ERROR] No Quarto configs found!")
        return

    # Generate workflow
    workflow_content = generate_workflow(project_root, job_configs)

    # Write to file
    workflow_path = project_root / ".github" / "workflows" / "publish.yml"
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.write_text(workflow_content, encoding='utf-8')

    print(f"[OK] Generated {workflow_path}")
    print(f"     {len(job_configs)} jobs: {', '.join(c.config_name for c in job_configs)}")
    print()


if __name__ == "__main__":
    # Allow running directly for testing
    project_root = Path(__file__).parent.parent.parent
    regenerate_workflow(project_root)
