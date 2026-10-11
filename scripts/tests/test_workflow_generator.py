import importlib.util
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
        "institute-papers",
        "manual",
    }
    assert len({job.cloudflare_pages_project for job in jobs}) == len(jobs)


def test_live_sites_are_verified_after_every_deploy() -> None:
    workflow = generate_workflow(PROJECT_ROOT, extract_deploy_job_configs(PROJECT_ROOT), "publish.yml.j2")
    verify_job = workflow[workflow.index("  verify-live-sites:"):]

    for job in extract_deploy_job_configs(PROJECT_ROOT):
        assert f"      - build-{job.config_name}\n" in verify_job
    assert "pnpm monitor:uptimerobot:check" in verify_job


def test_papers_site_job_builds_each_member_pdf_before_the_html() -> None:
    workflow = generate_workflow(PROJECT_ROOT, extract_deploy_job_configs(PROJECT_ROOT), "publish.yml.j2")
    papers_job = workflow[workflow.index("  build-institute-papers:"):workflow.index("  build-manual:")]

    assert "Install LaTeX" in papers_job
    assert papers_job.index("render-quarto.py dfda-spec --to pdf") < papers_job.index(
        "render-quarto.py institute-papers --to html"
    )


def test_redirect_worker_waits_for_live_standalone_targets() -> None:
    workflow = generate_workflow(PROJECT_ROOT, extract_deploy_job_configs(PROJECT_ROOT), "publish.yml.j2")
    worker_job = workflow[workflow.index("  deploy-redirect-worker:"):workflow.index("  verify-live-sites:")]

    assert "      - build-institute-papers\n" in worker_job
    assert "      - build-manual\n" not in worker_job
    assert worker_job.index("Check standalone redirect targets are live") < worker_job.index(
        "Deploy redirect Worker to Cloudflare"
    )


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


def render_artifacts_workflow() -> str:
    return generate_workflow(PROJECT_ROOT, extract_artifact_job_configs(PROJECT_ROOT), "build-artifacts.yml.j2")


def test_kdp_book_builds_artifacts_but_never_deploys_or_goes_to_zenodo() -> None:
    artifact_jobs = {job.config_name: job for job in extract_artifact_job_configs(PROJECT_ROOT)}
    book = artifact_jobs["manual-paperback"]

    assert "manual-paperback" not in {job.config_name for job in extract_deploy_job_configs(PROJECT_ROOT)}
    assert not book.upload_to_zenodo
    assert book.artifact_render_format is None
    assert [file.name for file in book.kdp_files] == [
        "How-to-End-War-and-Disease.epub",
        "How-to-End-War-and-Disease-ebook-cover.jpg",
        "How-to-End-War-and-Disease-Paperback.pdf",
        "How-to-End-War-and-Disease-Paperback.docx",
    ]
    # render-quarto.py fixes the EPUB for Kindle in assets/, not in _build_temp/
    assert book.kdp_files[0].source == "assets/epubs/How-to-End-War-and-Disease.epub"
    assert all(not job.kdp_files for name, job in artifact_jobs.items() if name != "manual-paperback")


def test_kdp_book_renders_each_format_separately_and_keeps_what_built() -> None:
    workflow = render_artifacts_workflow()
    book_job = workflow[workflow.index("  build-manual-paperback:"):workflow.index("  check-kindle-manual-paperback:")]

    # A multi-format render reuses the first format's frozen results, which lack the other formats' figures
    assert "render-quarto.py manual-paperback\n" not in book_job
    for render_format in ("epub", "pdf", "docx"):
        assert f"run: python scripts/render-quarto.py manual-paperback --to {render_format}\n" in book_job
    collect_step = book_job[book_job.index("Collect the KDP files"):book_job.index("Upload KDP files artifact")]
    assert 'if: "!cancelled()"' in collect_step
    assert "was not built" in collect_step


def test_artifacts_build_nightly_and_only_explicit_runs_reach_zenodo() -> None:
    workflow = render_artifacts_workflow()

    assert "schedule:" in workflow
    assert "refs/heads/master" not in workflow
    # A nightly run must queue behind a manual Zenodo run, not cancel it
    assert "cancel-in-progress: ${{ github.event_name != 'schedule' }}" in workflow
    zenodo_conditions = [
        line.strip()
        for line in workflow.splitlines()
        if line.strip().startswith("if:") and "publish_zenodo" in line
    ]
    assert zenodo_conditions
    assert all(
        condition == "if: startsWith(github.ref, 'refs/tags/v') "
        "|| (github.event_name == 'workflow_dispatch' && inputs.publish_zenodo)"
        for condition in zenodo_conditions
    )
    for job in extract_artifact_job_configs(PROJECT_ROOT):
        build_job = workflow[workflow.index(f"  build-{job.config_name}:"):]
        assert build_job.index("needs: changes") < build_job.index("if: needs.changes.outputs.build == 'true'")


def test_zenodo_steps_pass_only_arguments_the_upload_script_accepts(monkeypatch) -> None:
    script = PROJECT_ROOT / "scripts" / "upload-all-zenodo-and-save-dois.py"
    spec = importlib.util.spec_from_file_location("upload_all_zenodo", script)
    assert spec and spec.loader
    upload_script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(upload_script)

    commands = [
        line.split(f"python scripts/{script.name}", 1)[1].split()
        for line in render_artifacts_workflow().splitlines()
        if f"run: python scripts/{script.name}" in line
    ]
    assert commands
    for arguments in commands:
        monkeypatch.setattr(sys, "argv", [script.name, *arguments])
        # argparse exits with status 2 on an unknown flag
        upload_script.parse_args()


def test_optional_kindle_check_cannot_fail_the_release() -> None:
    workflow = render_artifacts_workflow()
    kindle_job = workflow[workflow.index("  check-kindle-manual-paperback:"):workflow.index("  release-builds:")]
    release_job = workflow[workflow.index("  release-builds:"):]

    assert "continue-on-error: true" in kindle_job
    # Kindle Previewer can stay open after converting; the step waits for its summary file, not its exit
    convert_step = kindle_job[kindle_job.index("Convert the EPUB to KPF"):kindle_job.index("Upload the KPF")]
    assert "-Wait" not in convert_step
    assert "Summary_Log.csv" in convert_step
    assert "Stop-Process" in convert_step
    assert "      - check-kindle-manual-paperback\n" in release_job
    assert 'select(.key | startswith("build-"))' in release_job
    assert "github.event_name != 'pull_request'" in release_job


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
