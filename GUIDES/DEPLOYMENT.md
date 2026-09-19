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

`.github/workflows/build-artifacts.yml` builds the PDFs, EPUBs, and DOCX files and uploads papers to Zenodo. It runs on manual dispatch, or on a push to `master`; the default branch is `develop`, so in practice it runs when someone starts it.

## When a run fails

- `ConnectionReset` or a timeout in a render step is a network flake: use "Re-run failed jobs".
- An authentication error in `deploy-redirect-worker` means the CI token does not cover a zone in `_ROUTE_ZONES`. See the API token section of `cloudflare/README.md`.
- "Redirect target is not live" means a site in the redirect map is not serving yet. The previous Worker stays deployed, so legacy links keep working.
- For a failing host in `verify-live-sites`, run `pnpm monitor:uptimerobot:check` locally to see where it ends up.
