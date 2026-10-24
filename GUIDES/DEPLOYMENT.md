# Deployment

Two sites deploy to Cloudflare Pages from `.github/workflows/publish.yml` on every push to `develop` (and on manual dispatch from the Actions tab). Pull requests build but do not deploy.

| Site | URL | Config | Pages project |
|---|---|---|---|
| The book | https://manual.warondisease.org | `_quarto-manual.yml` | `warondisease-manual` |
| Institute papers | https://papers.acceleratedmedicine.org | `_quarto-institute-papers.yml` | `institute-papers` |

`publish.yml` is generated. Edit `scripts/templates/publish.yml.j2` or the configs, then run `python scripts/lib/workflow_generator.py`. A config deploys when it sets `dih-render.cloudflare-pages-project`.

## What a run does

1. `validate`: Pyright and the workflow generator tests.
2. `build-manual` (75 minute limit) and `build-institute-papers` (120 minute limit, because it renders each member paper's PDF before the site): render, check Cloudflare's limits (20,000 files, 25 MiB per file), deploy.
3. `deploy-redirect-worker`: deploys the Worker that 301s legacy hosts, but only after every redirect target returns HTTP 200 on its own host.
4. `verify-live-sites`: checks all canonical URLs and legacy hosts from outside. A red run here means a live URL is wrong even though the deploys succeeded.

A push cancels a run still in progress on the same branch, so wait for a deploy to finish before pushing again.

## Everything else

`cloudflare/README.md` covers redirects, Worker routes, the API token, DNS, monitoring, and why the papers live on one site. Read it before changing any of those.

## Local render

```bash
# PYTHONPATH must point at the repo root, or render-quarto.py cannot import dih_models
PYTHONPATH=. python scripts/render-quarto.py manual --to html
PYTHONPATH=. python scripts/render-quarto.py institute-papers --to html
```

Output lands in `_build_temp/<config>/`. A local build can sweep in stray, gitignored HTML left in `knowledge/` by earlier renders and report validation errors for it; CI checks out a clean tree and never sees those files.

## Downloadable artifacts

`.github/workflows/build-artifacts.yml` (generated from `scripts/templates/build-artifacts.yml.j2`) builds the paper PDFs and the book's KDP files, then puts them on a GitHub release.

| Trigger | Builds | Release | Zenodo |
|---|---|---|---|
| Nightly from `develop` | Only if a file that can change an output changed since the last successful run | `latest-builds` | No |
| Manual dispatch | Always | `latest-builds` | Only with "Also upload the paper PDFs to Zenodo" checked |
| Push of a `v*` tag | Always | A release named after the tag | Yes |
| Pull request that changes the workflow | Always, as a test | None | No |

Uploads keep the file names, so `https://github.com/mikepsinn/disease-eradication-plan/releases/download/latest-builds/<file>` always points at the newest build. If one paper fails, the release still gets every other file and the run turns red. When every build passes, the release step also removes files that no build makes now, such as a renamed paper.

The book job renders `_quarto-manual-paperback.yml` once per format, because with `freeze: auto` a multi-format render reuses the first format's results and the later formats lose their figures. A format that fails is left out, and the others still reach the release. It releases the files KDP takes: the EPUB (Kindle-fixed by `render-quarto.py`), the eBook cover, the 7x10 paperback interior PDF, and a DOCX. The paperback cover (back, spine, and front in one PDF) is not built; make it with KDP Cover Creator. A Windows job then tries to turn the EPUB into a KPF with Kindle Previewer. Kindle Previewer writes a KPF only when Enhanced Typesetting works, so a missing KPF is a warning about the EPUB, and the job never blocks the release.

The Zenodo step publishes each paper that passes LLM PDF validation, which runs only when the `LLM_VALIDATION` secret is `true`.

## When a run fails

- `ConnectionReset` or a timeout in a render step is a network flake: use "Re-run failed jobs".
- "Graphviz did not install after 3 attempts" means apt could not reach the Ubuntu mirrors. `.github/actions/install-graphviz` caps and retries each apt call, so this fails in minutes instead of hanging; use "Re-run failed jobs".
- "More than one build made each of these files" means two builds wrote files with the same name. A release holds one file per name, so give one of them a different `pdf-output-file`.
- An authentication error in `deploy-redirect-worker` means the CI token does not cover a zone in `_ROUTE_ZONES`. See the API token section of `cloudflare/README.md`.
- "Redirect target is not live" means a site in the redirect map is not serving yet. The previous Worker stays deployed, so legacy links keep working.
- For a failing host in `verify-live-sites`, run `pnpm monitor:uptimerobot:check` locally to see where it ends up.
