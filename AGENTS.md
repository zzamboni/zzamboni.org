# Repository Guidelines

## Context & Branch Policy
- Read `docs/zzamboni-org-codex-handoff.md` for decisions and historical context. Verify dated claims against current files; suggestions are not authorization.
- GitHub is authoritative; GitLab is a downstream mirror. Inspect branch/worktree before editing; preserve local changes.
- Use `staging` for experiments/site changes unless directed otherwise; real content, including drafts, belongs on `main`. Promote only when asked; compare patches before reconciling divergent branches.
- Commands for Diego's terminal must use Elvish syntax.

## Content & Structure
- Edit long-form source in `content-org/zzamboni.org`; update its `content/post/` exports when requested. Never add explicit draft front matter to Org `DRAFT` headings (duplicate keys); `EXPORT_DATE` supports draft ordering.
- `content-pagescms/`, `content-photos/`, and `content-legacy/` mount into `content/post`. Legacy files remain canonical; not all `content/` files are Org exports. Preserve filenames, URLs, and source ownership.
- `.pages.yml` configures CMS collections. Lightweight posts default to drafts; zoneless dates use `Europe/Zurich`. Preserve explicit historical timezones.
- `layouts/` contains overrides; `themes/blowfish/` is pinned. `assets/` holds processed resources; `static/` is copied. Never hand-edit generated `public/`.
- Functions: `netlify/functions/`. Automation: `.github/workflows/`, `scripts/`. Consult relevant `docs/` guides before changing publishing flows.

## Development & Verification
- `mise run serve`: preview; `mise run serve-drafts`: include drafts.
- `mise run theme-check`: check releases/pins; `mise run theme-update`: update pins and report override diffs; `mise run theme-verify`: validate pins/build into temporary output.
- `python3 -m unittest discover -s scripts/tests`: Python tests (Python 3.11+).
- `npm ci`, then `npm run test:photoblog`: photo tests. Keep tests outside `netlify/functions/`.
- Hugo's authoritative pin is `mise.toml`; synchronize Netlify via the theme workflow. See `scripts/README-theme-updates.md`. Reproduce relevant draft/banner conditions from `netlify.toml`.

## Style & Review
- Match existing formatting; use singular `content/post/` paths. Use the Blowfish skill for theme work and review `scripts/theme-overrides.toml`. Preserve custom hooks, banners, tag clouds, galleries, and Blog photo filtering.
- Run relevant tests and visually check desktop/mobile pages; build success alone does not establish visual correctness.
- Separate content/tooling commits where practical. Automated subjects start with `auto:`. PRs include change descriptions, affected pages, verification, and screenshots for visual updates.
- Report branch/commit if created and remaining live checks. Batch pushes to conserve Netlify minutes; avoid unnecessary deployments or paid generation for validation.
