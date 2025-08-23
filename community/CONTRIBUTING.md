---
description: >-
  Guidelines for contributing to the Community Directory, including steps
  for getting started and making contributions via pull requests.
emoji: "\U0001F91D"
title: Contributing to the Community Directory
tags: 'dFDA, community-directory, contributing, open-source'
published: true
editor: markdown
date: '2025-02-12T16:51:44.377Z'
dateCreated: '2025-02-12T16:51:44.377Z'
---
# Contributing to the DFDA/DIH Wiki

Thank you for your interest in contributing. This document defines repo‑wide contribution rules, structure, and workflows. By participating in this project, you agree to abide by these terms.

## Repository organization (one level of folders)

- strategy: Treaty/DIH strategy, playbooks, roadmaps
- features: dFDA platform specs, technical roadmaps, treasury architecture
- economic-models: fundraising, tokenomics, ROI models
- regulatory: legal analysis, compliance, model acts
- reference: citations, datasets, appendices
- operations: SOPs, security, processes
- community: partners, templates, outreach

Keep files within one of these top‑level folders (no deep trees). Use cross‑links when content spans domains.

## Frontmatter requirements

All Markdown files start with YAML frontmatter. Standard fields remain mandatory: title, description, published, date, tags, editor, dateCreated. Add these governance fields:

- topic_id: stable identifier for the topic (e.g., dfda-technical-roadmap)
- canonical: true | false (exactly one canonical per topic_id)
- status: draft | active | deprecated | archived
- domains: [treaty | dih | dfda | cross]
- doc_type: strategy | spec | regulatory | model | ops | reference
- aliases: [./old-path.md, ./older-name.md] (use when moving/renaming or unpublishing)

Example:

```yaml
title: dFDA Platform Technical Roadmap
description: Phased build plan for the dFDA platform and agents
published: true
date: '2025-08-22T00:00:00.000Z'
tags: dfda, technical-roadmap
editor: markdown
dateCreated: '2025-08-22T00:00:00.000Z'
topic_id: dfda-technical-roadmap
canonical: true
status: active
domains: [dfda]
doc_type: spec
aliases: [../features/old-roadmap.md]
```

## Canonical content rules

- One canonical file per topic_id. Others must set canonical: false and link to the canonical.
- Use a hatnote at the top of non‑canonical files: “For the current version, see [canonical‑title](./relative/path.md).”
- Use summary style: overviews should link to main articles, not duplicate them.

## Deduplication & merging

When two files overlap:

1) Choose the canonical (newer/better structured/more linked).
2) Merge any unique, high‑value content into the canonical.
3) Set the other to status: archived (or deprecated), canonical: false, published: false.
4) Add a hatnote pointing to the canonical and an aliases entry for redirects.

## Placement map (what goes where)

- Treaty mandate, referendums, and political strategy → strategy/
- DIH treasury governance, tokenomics, architecture → strategy/ (concepts) and features/treasury/ (implementation)
- dFDA product specs, agents, UX, trials → features/
- Financial models and estimates → economic-models/
- Laws, model acts, jurisdiction analyses → regulatory/
- SOPs, security, incident response → operations/
- Citations, datasets, long tables → reference/

## Naming & linking

- Kebab‑case filenames, topic‑first: dfda-platform-technical-roadmap.md
- Use relative links (./, ../). Link to headings when helpful.
- Escape dollar signs in Markdown (write \$VICTORY, \$27B).
- Follow the Sourcing and Citation Standard: every quantitative claim must link to a source.

## Voice & messaging guidelines

- Use direct, powerful language over euphemisms.
- Core framing: "Make curing more profitable than killing" / "Bribe our way to a better world"
- Alternative framings: "Make peace more profitable than war" / "Capture the peace dividend" / "Bribe the shit out of everyone to act like a proper species"
- Avoid weak corporate speak; prefer honest, visceral language that matches the stakes.
- Quantify everything; moral arguments need data backing.

## Contributor workflow (PR checklist)

- Confirm frontmatter includes topic_id, canonical, status, domains, doc_type
- If moving/unpublishing, add aliases and a hatnote
- Avoid creating new top‑level folders; place files per Placement map
- Prefer updating the canonical over creating a parallel doc
- For major reorganizations, open a short RFC in the PR description

## Overlap resolution (lightweight RFC)

- Template (inline in PR): context, conflicting files, proposed canonical, migration plan (what merges where), redirects/aliases, owners pinged
- 48‑hour review window for maintainers; after that, proceed

## Automation (guidance)

- Link checker: no dead links; unpublished targets must have an explicit “archived” hatnote
- Frontmatter validator: fail CI if required fields missing or multiple canonicals for a topic_id
- Index generation: domain indexes and a canonical list are generated from frontmatter (do not hand‑curate)

## How to Contribute

### Getting Started

1. Read this CONTRIBUTING.
2. Decide where your contribution fits per Placement map.

### Making Contributions

1. Fork the repository to your GitHub account.
2. Clone your fork to your local machine.
3. Create a new branch for your contribution.
4. Make your changes in your branch.
5. Commit your changes with a clear and descriptive commit message.
6. Push your changes to your fork on GitHub.
7. Submit a pull request to the main repository.

### Pull Requests

- Ensure that your pull request adheres to the provided templates when applicable.
- Describe the changes you have made in detail and link any relevant issues.
- Pull requests will be reviewed by the community and maintainers for quality and relevance.

### Using Templates

- Use the `templates/project_proposal.md` for project proposals.
- Use the `templates/partner_introduction.md` for introducing new partners.
- Follow the structure and prompts provided in the templates to ensure consistency.

### Issues

- Use the GitHub issue tracker to report problems, propose ideas, or request new collaborations.
- Before creating a new issue, please check to see if an existing issue addresses your concern.
- Be specific and provide as much detail as possible in your issue.

## Code of Conduct

- Be respectful of other contributors.
- Engage in constructive dialogue.
- Avoid sharing any personal or sensitive information.
- Follow the ethical guidelines and best practices of your field.

## Updating Your Contributions

- Keep your content up-to-date with any new developments or changes.
- Regularly check your pull requests and issues for any feedback or required changes.

## Contact Information

- For general inquiries or assistance, please reach out to the project maintainers at [contact@email.com].
- For specific collaboration requests, use the contact information provided on the partner's Markdown page in the respective folder.

## Additional Guidelines

- Ensure that your contributions are accessible and easy to understand.
- Do not include any proprietary, confidential, or sensitive information in your contributions.
- Encourage community engagement by participating in discussions and sharing your expertise.

By following these guidelines, you help to maintain the quality and integrity of the Community Directory. We look forward to your valuable contributions and thank you for helping to advance the goals of the dFDA.

