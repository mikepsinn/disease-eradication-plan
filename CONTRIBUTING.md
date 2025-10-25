---
title: How to Contribute
description: Central guide for contribution guidelines, style standards, and project practices for the Complete Idiot's Guide to Ending War and Disease.
published: true
tags: [contributing, guidelines, standards, book, knowledge-base]
---

# How to Contribute to the Complete Idiot's Guide to Ending War and Disease

This document provides a central overview of the contribution process. For detailed standards, please refer to our specialized guides:

- **[Mission and Core Principles](GUIDES/MISSION_AND_PRINCIPLES.md)**: The project's mission, philosophy, and core principles.
- **[Writing Style Guide](GUIDES/STYLE_GUIDE.md)**: Tone, voice, and prose style.
- **[Design Guide](GUIDES/DESIGN_GUIDE.md)**: Visual standards for charts and diagrams.
- **[Technical Guide](GUIDES/TECHNICAL_GUIDE.md)**: Development setup and technical standards.
- **[Content and Style Standards](./GUIDES/CONTENT_STANDARDS.md)**: Standards for information architecture, quality assurance, and formatting.
- **[Economic Parameters](brain/book/appendix/economic_parameters.py)**: Single source of truth for all economic values (military spending, clinical trial costs, ROI calculations, etc.). See the module docstring for usage.
- **[Economics File Organization](GUIDES/ECONOMICS_HIERARCHY_FINAL.md)**: Structure and organization of economics-related files.

**Table of Contents**

- [Contributor Workflow](#contributor-workflow)
- [Automation and CI](#automation-and-ci)

## Contributor Workflow

The plan _is_ the repository. We're building a book that's so clear anyone can read it.

1.  **Set up your environment:** Follow the [Development Environment Setup](GUIDES/TECHNICAL_GUIDE.md#development-environment-setup).
2.  **Find something to improve:** Look at the `todo.md` for priorities.
3.  **If changing book structure:** Update the [Book Outline in README.md](./README.md#book-outline) first.
4.  **Make your changes:** Fork the repo and create a branch, or just edit on GitHub if you're not technical.
5.  **Follow the standards:** Use the rules in this document and the specialized guides.
6.  **Submit a pull request:** Explain how your change makes things better.

## Automation and CI

- **Link Checker:** Pull requests with dead internal links will fail.
- **Frontmatter Validator:** Pull requests will fail if required frontmatter fields are missing.
