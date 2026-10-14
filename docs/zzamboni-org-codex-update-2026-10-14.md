# zzamboni.org: Curated Codex Context Update

Prepared **October 14, 2026**, Europe/Zurich. This updates the October 10 handoff; it is context, not authorization to merge, publish, deploy, or run paid generation.

## Scope and Evidence

Baseline: `docs/zzamboni-org-codex-handoff.md`, prepared October 10, 2026, including its local-import caveats. Inspected the current checkout, Git history since that date, the baseline-to-main diff, main/staging tree differences, `AGENTS.md`, configuration, layouts/CSS, publishing workflows, functions, dependencies, build scripts/tests, and maintainer docs. Rationale and validation below also use the available conversation in this Codex thread, including user-pasted Netlify logs and benchmark CSV.

| Inspected local ref | Full commit |
| --- | --- |
| `main` / cached `origin/main` | `acaa46048599fa9bd57976f9bc0cf4dca7ac977e` |
| `staging` / cached `origin/staging` (checkout HEAD) | `ad2b1cc5c8d215373c8005ef780d55ae094a54e4` |

No fetch or live GitHub/Netlify account inspection was performed for this update. Cached remote-tracking equality is not proof of current remote state or deployment. Other Codex sessions and the complete ChatGPT project history are not available in this thread; changes such as branding and the linkblog payload update are therefore documented from Git, without inventing their discussion or validation history. No new builds/tests were run for this documentation task. No credentials or hook URLs are included.

**Working tree was clean before creating this update.** Earlier uncommitted thumbnail, favicon, parser, and history-script work is now committed. This new document is the only uncommitted deliverable from this task.

### Branch Reconciliation

At these tips, main is an ancestor of staging (`main...staging`: 0 main-only, 219 staging-only commits). The count includes historical/cherry-picked work, not 219 outstanding features. Staging's `ad2b1cc5c` merged the latest main content.

Application code, configuration, workflows, scripts, dependencies, docs, and homepage CSS now match. The remaining 59 changed paths are content/images: staging-only photo posts and historical test images, two cached favicons, a lingering `Testing` line in `content-pagescms/2026-09-21-new-posting-workflow-pagescms.md`, and absence of main's fallback `featureimage` in `content-pagescms/2026-10-12-customize-web-app-icon.md`. Do not bulk-promote these differences without review.

## Completed Work

The following changes are present on both branch tips. Commit references below are representative **main** commits; staging often has separate cherry-pick identities. No new PR numbers were established for these changes.

| Area | Result and evidence paths | Main commits |
| --- | --- | --- |
| Repository context | Imported baseline into tracked `docs/`; refreshed branch/content/testing guidance in `AGENTS.md`; removed blanket docs exclusion from `.gitignore`. User explicitly prefers committing these documents. | `f770d292f` |
| Homepage feeds | Separate recent-post summaries and image-only recent-photo sidebar; configurable widths, square photos, localized labels, Links menu entry. | `2031c9fff`, `8cdc84fdd`, `00f19f355`, `09bf7f1aa`, `90dd4fd19` |
| Homepage image fixes | Removed accidental blanket thumbnail hiding; smaller uncropped desktop article thumbnails; alpha-aware shadows. | `50870b931`, `acaa46048` |
| Build suppression | Conservative file filtering, draft-project on-demand mode, maintenance/workflow exclusions. `scripts/netlify-ignore.mjs`, `netlify.toml`. | `650f65a90`, `07568ba73`, `93a18eec8`, `a9ed87fb4` |
| Draft build button | Repository-level Pages CMS action and `.github/workflows/build-draft-site.yml`. | `10d101fad` |
| Resource caching | Tracked Hugo Cache Resources plugin configuration and exact dependency pin. | `b6599a059` |
| Historical measurement | CLI-backed `scripts/netlify-build-history.py` writes logs, CSV, and dependency-free SVG. | `324fda267` |
| Draft-only filtering | Parse both committed post versions; preserve publishing/unpublishing builds; support CMS posts and Org Markdown exports. Vendored parser and tests. | `f775baa2e`, `7406215f9` |
| Linkblog payload | Accept `summary` as well as `commentary`, with mutual fallback instead of always writing a blank summary. | `b58ad0a77` |
| Branding | New transparent favicon family, enabled site logo, removed homepage background image. | `399fe692f`, `5ca3f5913`, `2fa5c8673`, `560b15d07`, `fdc57781a` |

### Homepage and Theme Behavior

`layouts/partials/home/custom.html` calls `home/feeds.html`. The feed reuses Blowfish's `article-link/simple.html` rather than duplicating article markup. `scripts/theme-overrides.toml` records that upstream dependency for theme upgrades.

- Select regular pages in section `post`; entries tagged `photos` go to the sidebar, others to the summary list, newest first. This is in addition to the existing Blog-section photo filter, not a global search/RSS exclusion.
- `config/_default/params.toml`: custom homepage, `showRecent = false` to avoid duplicate native feed, `showRecentItems = 10`, `showRecentPhotos = 6`, `photoColumnPercent = 20`.
- Homepage front matter can override `photoColumnPercent`. Valid range is 1-99; invalid values fail the build. Desktop grid share excludes the gap; below 768px feeds stack. No renderable photos means a posts-only layout.
- Sidebar skips image-less photo posts before applying the limit. Photos are square, center-cropped, linking to their posts. Article thumbnails are deliberately different: desktop width 180px, natural aspect ratio, no crop/hover scaling. Mobile retains theme sizing.
- `assets/css/custom.css` replaces homepage thumbnail-wrapper `box-shadow` with image `filter: drop-shadow(...)` and permits shadow overflow. Actual image transparency is required. Compact linkblog thumbnail hiding remains intentional; sidebar photos and other listings are unaffected.
- `i18n/en.yaml` supplies labels including **Recent posts**. `homepageImage` is now empty; do not restore the old background inadvertently.

Hugo Extended remains **0.166.0**, pinned through `mise.toml` and synchronized Netlify settings. Blowfish is **v3.8.0**, submodule `51a361e068b9975c7f1df8e2bb223db03fe49c2b`; no theme/version upgrade was introduced by this work.

### Branding and Authoring

`config/_default/languages.en.toml` enables `branding/favicon-source-2048.png` as the site logo. Sources live in `assets/branding/`; generated browser/platform icons live under `static/`. `static/site.webmanifest` replaces the old `static/manifest.json`; obsolete duplicate favicon assets were removed. Subsequent commits corrected transparent edges. Keep this pipeline separate from generated article feature images. Browser favicon caching can conceal updates.

Authoring ownership is unchanged: long-form Org source in `content-org/zzamboni.org`, exports in `content/post/`, lightweight CMS posts in `content-pagescms/`, photo bundles in `content-photos/`, and canonical legacy files in `content-legacy/`. Mounts still combine these into Hugo's post section.

The phone publishing tutorial remains a **draft** at `content/post/2026-10-07-linkblog-and-photoblog-with-netlify-and-shortcuts/index.md`; source/export edits continued through `30db51ba3`. Do not confuse it with an unidentified earlier weekly-draft request. The new favicon post in `content-pagescms/2026-10-13-a-new-favicon-for-zzamboni-org.md` has `draft = false` (repository status, not independent live verification).

## Netlify Policy and Workflow

Detailed maintained reference: `docs/netlify-builds.md`.

### Ignore Check

`netlify.toml` executes `node ./scripts/netlify-ignore.mjs` before dependency installation. It uses Git, Node, and vendored `smol-toml` **1.9.1** with its license in `scripts/vendor/smol-toml/`; no npm install is required for this check.

Precedence: `NETLIFY_FORCE_BUILD=true` builds; otherwise `NETLIFY_ON_DEMAND=true` skips; otherwise inspect `CACHED_COMMIT_REF` through `COMMIT_REF`. Exit **0 = skip**, **1 = build**. Missing/invalid refs, Git failures, and empty comparisons build conservatively. Renames are deletion plus addition. This spans all changes since the cached commit, not merely HEAD's parent.

Non-site paths: root `README.md`, `AGENTS.md`, `.pages.yml`; `docs/`, `scripts/`, `.github/workflows/`; `.org` files under `content-org/`. Their generated content/assets are NOT automatically ignored. Revisit these exclusions if build/runtime/template dependencies change; workflow-only changes still run GitHub Actions independently.

Eligible draft posts: `content-pagescms/*.md`, standalone `content/post/*.md`, and `content/post/<slug>/index.md`. Require valid TOML and explicit boolean draft status in both existing versions. Exclude top-level indexes, `_index.md`, other nested resources, YAML/HTML posts, images, and unknown paths.

| Before -> after | Decision when drafts are excluded |
| --- | --- |
| Absent -> draft; draft -> draft; draft -> absent | Skip if all other changed paths also qualify |
| Draft -> published | Build |
| Published -> draft or absent | Build to remove published output |
| Absent -> published; published -> published | Build |
| Invalid/unknown state, shared asset or other site change | Build conservatively |

`BUILD_DRAFTS=true` disables draft-only skipping. The filter also checks `HUGO_BUILDDRAFTS`, custom config environment overrides, and tracked config variants; unsupported config fails safe. This is source classification, not a Hugo output comparison. It assumes the standard build command/config and no direct template reads of excluded drafts; the implementation audit found no such dependency. Adding custom flags or source-reading templates requires reviewing the policy.

### On-Demand Draft Site

User configured the draft project with `NETLIFY_ON_DEMAND=true`, alongside `BUILD_DRAFTS=true`, and a build hook targeting main. Keep Netlify builds **Active**: stopping builds also disables hooks. Hooks bypass the ignore check. Do not set on-demand mode globally for production/staging unless separately requested.

The **Build draft site** sidebar action in `.pages.yml` dispatches `build-draft-site.yml` explicitly on **main**, regardless of the CMS branch. It builds saved main content, not unsaved edits or staging-only work. GitHub's Run workflow is an alternative; `payload` may be blank. The workflow rejects other branches, uses repository secret `NETLIFY_DRAFT_BUILD_HOOK`, needs no checkout/token permissions, and does not retry POSTs (avoid duplicate builds). A successful action means request accepted, NOT deployment completed; its summary links to Netlify and the draft site. Cancelling it cannot undo an accepted hook request.

### Caching and Other Savings

User explicitly disabled Lighthouse and obsolete Forms functionality, including form detection, through Netlify UI. These are user-confirmed account changes, not settings guaranteed by this repository.

`netlify-plugin-hugo-cache-resources` **0.2.1** is now enabled in `netlify.toml` for all contexts and pinned in `package.json` under regular dependencies because `NODE_ENV=production` omits dev dependencies. It persists generated Hugo resources, not browser/CDN responses. Each project's cache needs warming. `sharp` is **0.35.5** on both branches. Do not remove it as a build optimization: photoblog uses it.

## Validation and Deployment Evidence

These are prior results from this thread, not newly rerun checks:

| Evidence level | Result / boundary |
| --- | --- |
| Automated local tests | Ignore-filter suite grew to seven passing groups, including real temporary Git repositories, draft transitions, overrides, malformed TOML, renames, mixed changes, and Org exports. Command: `node --test scripts/tests/netlify-ignore.test.mjs`. |
| Local checks | Pinned Hugo builds succeeded after thumbnail fixes; rendered homepage contained thumbnail wrappers. Plugin TOML parsing/loading succeeded. Draft-hook shell syntax and seven mocked request/failure cases passed. History parser and CSV/SVG generation passed mocked checks. |
| User-confirmed behavior | Configurable homepage width, thumbnail/shadow appearance accepted; draft push successfully skipped; hook-triggered draft deploy completed. Historical graph utility ran and showed consistently reduced build times. |
| Pasted live logs | Earlier production processing: 85.0s, Hugo 13.5s, deployment 26.8s, Lighthouse about 16s. Later draft processing: 39.4s, Hugo 12.5s, deployment 5.2s, Forms explicitly skipped, no Lighthouse. Different projects and upload counts: not a controlled comparison. |
| Controlled draft benchmark | Three before + one warmup + three after runs: median Hugo 12.9s -> 3.9s; median total 39.3s -> 31.4s; cache about 950MB -> 973MB. All reported zero uploads. Commit columns were blank, so identical-source control rests on the experiment procedure, not recorded SHAs. |
| Longer-term user observation | Historical graphs showed approximately 45s -> 30s consistently. This is user-reported, not an independently recomputed dataset here. |

No inference that all branch-tip commits are deployed. Specifically, live draft-only skip/publish/unpublish transitions and removal of the duplicate UI plugin installation have not been confirmed in this thread. The supplied logs lacked a secrets-scanning stage in the later run; that is NOT evidence that disabling scanning was requested or advisable.

### Historical Timing Tool

`scripts/netlify-build-history.py PROJECT_ID BRANCH --days 90 --limit 200 --out OUTPUT_DIR` uses an authenticated Netlify CLI. It paginates deploy metadata, reads successful non-skipped builds' logs, and writes raw logs, `history.csv`, and `history.svg` without triggering builds or adding plotting dependencies. Limit means deploys examined, not plotted results. Retention/missing logs can bias historical coverage; failed/skipped builds are not charted.

CLI logs may omit the dashboard's final processing-duration line. The script falls back to build-image-start through cleanup timestamps (excluding queue wait), labels the source in CSV, and skips incomplete logs rather than using zero. Do not substitute creation-to-publication timestamps without considering queue/post-processing. Local-only Elvish `collect-build` was provided in chat for controlled runs; it is not a tracked repository tool. Reusing a deploy ID downloads the same run; commit SHA and build-hook ID can stay constant while new deployments have distinct IDs.

## Decisions, Remaining Work, and Corrections

**Confirmed user decisions:** configurable two-column homepage; 20% default photos; square sidebar photos but proportional smaller article thumbnails; alpha-aware shadows; tracked docs and plugin config; on-demand draft builds; broader non-site exclusions; draft-only skipping including Org exports. **Implementation choices:** conservative eligibility, vendored parser, inspecting both Git versions, safety fallback to build, fixed-main CMS action, and no automatic hook retries. These are adopted code, not general permission to widen scope.

| Item | Current status / next action |
| --- | --- |
| Draft-filter rollout | Implemented on both tips, locally tested. On a normal rollout, verify logs for draft creation/edit/deletion and publishing/unpublishing; do not manufacture extra paid builds solely for this update. |
| Plugin UI migration | Tracked config is present on both branches; whether the old draft-project UI installation was removed is unknown. Check before declaring cleanup complete. |
| Working-tree comparison mode | Explicitly deferred by user. Ignore script remains commit-only; do not add `--working-tree` unasked. |
| Broader draft/resource analysis | Not implemented: YAML/HTML, photo bundles, and draft-exclusive assets still build. Expanding this is a separate decision, not a pending promise. |
| Remaining branch content | Review deliberately if reconciling; code parity does not authorize promotion of test images/posts. |
| Documentation follow-up | `AGENTS.md` still suggests `npm ci`, but no package lockfile is tracked/present. Use `npm install` for current setup or separately agree on adding a lockfile. `docs/netlify-builds.md`'s broad exported-content/build wording must be read with its draft-only exceptions; its “standard library and Git” wording omits the vendored parser. Neither file was changed during this update. |
| Historical unknowns | No new evidence resolves every old gallery/mobile/phone-shortcut issue, Pages CMS outage, or OpenAI balance concern. Reproduce/check only when relevant; don't relabel them all as active bugs. Self-hosting Pages CMS remains unadopted. |

Explicit replacements for the original handoff:

- **Build-budget policy undecided** is superseded by the implemented filtering, on-demand draft hook, resource caching, and user-confirmed removal of Lighthouse/Forms.
- **Main/staging sharp mismatch and mutually divergent heads** are obsolete at these tips: sharp matches; main is an ancestor of staging; remaining tree differences are content/assets.
- **Homepage described only as a title/content adaptation** is incomplete: preserve the new feeds, settings, responsive sizing, shadow semantics, and removed background.
- **AGENTS drift merely suggested for repair** is largely resolved by `f770d292f`; the lockfile/test-command caveat above remains.
- **Linkblog always starts with blank summary** no longer applies: supplied summary/commentary populate each other when only one is present. The summary-generation workflow still fills genuinely blank summaries; no new automatic image-generation trigger was added.
- **Blowfish release unknown** is replaced by locally verified v3.8.0 at the same pinned SHA. Hugo remains 0.166.0.
- **Docs excluded/untracked** no longer applies: docs are intentionally committed. **No automated tests** is false: use existing Python/photo suites plus the new ignore suite.
- Baseline authoring mounts, Zurich date interpretation, privacy re-encoding of new photos, manual/CMS image PR review and owner refinement, GitLab mirroring, and OpenAI usage-report architecture remain in force. This period did not redesign them.

## Current Working Instructions

- GitHub is authoritative; GitLab is a mirror. Inspect status/branches first and preserve user edits. Use staging for implementation experiments; real content/drafts belong on main. Promote, commit, push, or deploy only when requested.
- Treat files as authoritative for implementation and conversation as evidence of intent. Never equate commits, remote-tracking refs, or accepted hook requests with successful deployments.
- Preserve authoring ownership and URLs. Edit long-form Org source, not only exports; do not add explicit draft front matter to Org `DRAFT` headings. Use `EXPORT_DATE` for draft ordering when appropriate.
- Automated commit subjects start `auto:`; separate tooling and content where practical. Keep docs tracked. Human commit requests should receive a short title and body.
- Use Elvish syntax for Diego's terminal commands. `mise run serve` / `mise run serve-drafts` use the pinned Hugo. Theme updates go through existing check/update/verify tooling and override review.
- Run relevant local tests; distinguish build success from visual desktop/mobile verification. Avoid unnecessary pushes/builds and paid generation. Force-build is an explicit escape hatch, not a default.
- Keep secrets and hook URLs out of Git, CMS configuration, and uploaded context. Preserve conservative ignore behavior if assumptions become uncertain.
