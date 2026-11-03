# Documentation

Maintainer documentation for [zzamboni.org](../README.md). The repository's current code and configuration on `main` are authoritative; dated notes and plans describe the state when written, not necessarily today's behavior.

## Site features and operating guides

| Guide | What it covers |
| --- | --- |
| [Blog archive](blog-archive.md) | Hugo archive module, chart, filters, configuration, and local checks. |
| [Callout blocks](callout-blocks.md) | Org-mode tip/note/warning blocks, generic Blowfish admonitions, alerts, and shortcode attributes. |
| [Feature image generation](feature-image-generation.md) | GitHub Actions image generation, styles, review PRs, and image refinement. |
| [Gallery and lightbox](gallery-lightbox.md) | GLightbox integration, figure behavior, captions, scroll locking, and browser regression checks. |
| [JSON Resume in Hugo](hugo-vita-experiment.md) | Site-owned CV/publications data, the `hugo-jsonresume` module, and updates. The filename is historical; this is an implemented integration. |
| [Legacy content](legacy-content.md) | Mounted legacy Markdown/HTML posts and their Pages CMS collections. |
| [Linkblog favicons](linkblog-favicons.md) | Icon discovery, caching, fallback behavior, and refresh workflow. |
| [Netlify builds](netlify-builds.md) | Build filtering, resource caching, and on-demand draft/staging deployments. |
| [OpenAI usage reporting](openai-usage.md) | Reporting workflow, required credentials, credit estimates, and limitations. |
| [Related articles](related-posts.md) | Hugo related-content ranking, eligibility, presentation, and tests. |

## Planning and editorial records

| Document | How to use it |
| --- | --- |
| [Blogging setup publication plan](blogging-setup-publication-plan.md) | **Historical snapshot (October 21, 2026).** Proposed article order and editorial checklist. Check current publication status and the site's [My website setup series](../content-org/zzamboni.org) before using the schedule. |
| [Roadmap ideas](2026-10-15-zzamboni-roadmap-ideas.md) | **Historical planning snapshot (October 15, 2026).** Some proposals, notably related articles and the archive, have since been implemented. Reassess remaining ideas against current code. |

## Historical project context

| Document | How to use it |
| --- | --- |
| [Codex handoff, October 10](zzamboni-org-codex-handoff.md) | Historical architecture, decisions, investigations, and caveats from an older checkout. |
| [Codex update, October 14](zzamboni-org-codex-update-2026-10-14.md) | Follow-up corrections and validation evidence at specific historical commit IDs; not a live status report. |

These handoffs are intentionally preserved as records. In particular, old branch comparisons, versions, workflow names, and pending tasks should be verified before reuse.

## Where to start

For day-to-day changes, read [AGENTS.md](../AGENTS.md) and the relevant feature guide above. For the authoring/publishing overview, start with the [repository README](../README.md). For theme maintenance, consult [theme update instructions](../scripts/README-theme-updates.md) and [override tracking](../scripts/theme-overrides.toml). For current implementation details, inspect `config/`, `layouts/`, `scripts/`, `.github/workflows/`, and `netlify/functions/` on the target branch.

Documentation-only edits normally do not require a Hugo build; changes to configuration, templates, or authoring behavior should be checked with the relevant local tests and preview. Avoid treating a successful workflow dispatch as proof of a completed Netlify deployment.
