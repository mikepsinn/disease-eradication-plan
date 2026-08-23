import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LIB_DIR = PROJECT_ROOT / "scripts" / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from workflow_generator import JobConfig, generate_workflow  # noqa: E402


def render_publish_workflow() -> str:
    job = JobConfig(
        config_name="manual",
        display_name="Build How to End War and Disease",
        project_type="book",
        timeout_minutes=75,
        build_dir="_build_temp/manual/_manual/warondisease",
        configured_formats=["html"],
        downloadable_formats=[],
        artifact_render_format=None,
        netlify_site_id="test-site-id",
        netlify_secret="NETLIFY_MAIN_SITE_ID",
        upload_to_zenodo=False,
        deploy_to_netlify=True,
    )
    return generate_workflow(PROJECT_ROOT, [job], "publish.yml.j2")


def test_generated_workflow_identifies_its_source() -> None:
    workflow = render_publish_workflow()

    assert workflow.startswith(
        "# AUTO-GENERATED FILE. DO NOT EDIT DIRECTLY.\n"
        "# Source: scripts/templates/publish.yml.j2\n"
        "# Generator: scripts/lib/workflow_generator.py\n"
        "# Make changes in the source template or generator, then regenerate.\n"
    )


def test_netlify_credentials_are_validated_before_expensive_build_steps() -> None:
    workflow = render_publish_workflow()

    preflight = workflow.index("Validate Build How to End War and Disease Netlify credentials")
    checkout = workflow.index("Check out repository")
    render = workflow.index("Render Build How to End War and Disease (HTML)")
    deploy = workflow.index("Deploy Build How to End War and Disease to Netlify")

    assert preflight < checkout < render < deploy
    assert workflow.count("netlify_status=") == 1
