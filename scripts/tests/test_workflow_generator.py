import io
import sys
from pathlib import Path


if sys.platform == "win32" and isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LIB_DIR = PROJECT_ROOT / "scripts" / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from workflow_generator import (  # noqa: E402
    JobConfig,
    extract_artifact_job_configs,
    extract_deploy_job_configs,
    generate_workflow,
)


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
        bundle_pdf_with_site=False,
        cloudflare_pages_project="warondisease-manual",
        upload_to_zenodo=False,
        deploy_to_cloudflare=True,
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


def test_cloudflare_credentials_are_validated_before_expensive_build_steps() -> None:
    workflow = render_publish_workflow()
    build_job = workflow[workflow.index("  build-manual:"):]

    preflight = build_job.index("Validate Build How to End War and Disease Cloudflare Pages credentials")
    checkout = build_job.index("Check out repository")
    render = build_job.index("Render Build How to End War and Disease (HTML)")
    deploy = build_job.index("Deploy Build How to End War and Disease to Cloudflare Pages")

    assert preflight < checkout < render < deploy
    assert workflow.count("project_status=") == 1
    assert "NETLIFY_AUTH_TOKEN" not in workflow
    assert "CLOUDFLARE_API_TOKEN" in workflow


def test_pull_requests_validate_and_build_but_only_develop_deploys() -> None:
    workflow = render_publish_workflow()
    build_job = workflow[workflow.index("  build-manual:"):]
    deploy_step = build_job[build_job.index("Deploy Build How to End War and Disease to Cloudflare Pages"):]

    assert "pull_request:\n    branches: [develop]" in workflow
    assert "needs: validate" in build_job
    assert workflow.count("Run Python type check") == 1
    assert "github.event_name == 'push'" in deploy_step
    assert "github.ref == 'refs/heads/develop'" in deploy_step
    assert "github.event_name == 'pull_request'" not in deploy_step


def test_only_explicit_cloudflare_pages_projects_deploy() -> None:
    jobs = extract_deploy_job_configs(PROJECT_ROOT)

    assert {job.config_name for job in jobs} == {
        "dfda-spec",
        "manual",
        "right-to-trial",
        "right-to-trial-impact",
    }
    assert len({job.cloudflare_pages_project for job in jobs}) == len(jobs)


def test_pdf_llm_validation_is_explicitly_opt_in() -> None:
    expected = (
        "GOOGLE_GENERATIVE_AI_API_KEY: ${{ secrets.LLM_VALIDATION == 'true' "
        "&& secrets.GOOGLE_GENERATIVE_AI_API_KEY || '' }}"
    )
    workflow_cases = (
        (extract_deploy_job_configs(PROJECT_ROOT), "publish.yml.j2"),
        (extract_artifact_job_configs(PROJECT_ROOT), "build-artifacts.yml.j2"),
    )

    for jobs, template_name in workflow_cases:
        workflow = generate_workflow(PROJECT_ROOT, jobs, template_name)
        key_lines = [
            line.strip()
            for line in workflow.splitlines()
            if "GOOGLE_GENERATIVE_AI_API_KEY:" in line
        ]
        assert key_lines
        assert all(line == expected for line in key_lines)


def test_checked_in_workflows_match_their_generators() -> None:
    workflow_cases = (
        (
            PROJECT_ROOT / ".github" / "workflows" / "publish.yml",
            extract_deploy_job_configs(PROJECT_ROOT),
            "publish.yml.j2",
        ),
        (
            PROJECT_ROOT / ".github" / "workflows" / "build-artifacts.yml",
            extract_artifact_job_configs(PROJECT_ROOT),
            "build-artifacts.yml.j2",
        ),
    )

    for workflow_path, jobs, template_name in workflow_cases:
        generated = generate_workflow(PROJECT_ROOT, jobs, template_name)
        checked_in = workflow_path.read_text(encoding="utf-8")
        assert checked_in == generated, (
            f"{workflow_path.name} is stale; regenerate it with "
            "scripts/lib/workflow_generator.py"
        )
