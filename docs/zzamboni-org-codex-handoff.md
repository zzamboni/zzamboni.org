# Codex handoff: zzamboni.org

> Imported on 2026-10-10 as a historical snapshot. See `../AGENTS.md` for
> maintained guidance; verify dated claims against current files. At import,
> local `main` has sharp `0.35.4`, not the remote-main `0.35.5` reported below.
> Mise tasks, test commands, mounts, and Zurich timezone were checked locally;
> remote heads and deployment settings were not rechecked. The skill URI below
> belongs to Work; use the Blowfish skill in the current session's catalog.

Prepared 2026-10-10 for Diego Zamboni. This is a context transfer for a Codex session on his laptop; it does not transfer laptop chat history or authorize new implementation work.

## Evidence and freshness

Repository: https://github.com/zzamboni/zzamboni.org. Public site: https://zzamboni.org/.

Current repository files were read through GitHub, together with the visible project instructions and conversation history. No local repository was available in this session. No builds, tests, live UI checks, Netlify settings inspection, or secret inspection were performed. Historical reports of successful deployments are identified separately below.

Verified branch heads at preparation time:

| Branch | Commit |
| --- | --- |
| main | `fd029bd6171dd0bc5d29144c4ac96fd932fa3bc1` |
| staging | `c1d349694cfe8ae0484785e94e6b267e13d67f49` |

Re-fetch before acting. The branches have diverged and several changes were cherry-picked. GitHub's compare reports 16 main-side and 193 staging-side commits since their merge base; these are history counts, not counts of missing changes. Compare actual files and patch equivalence before merging. Do not infer that staging's experiments should all reach main.

## Goals and confirmed decisions

The site is Diego's personal technical blog and portfolio. The current goal is lower-friction publishing, especially short posts, links, and photos from a phone, while retaining Org mode for substantial technical writing.

| Decision | Rationale and status |
| --- | --- |
| GitHub is the source of truth | Explicit project instruction; GitLab is a downstream mirror. Older GitLab-first descriptions are historical. |
| Hugo with Blowfish; Netlify hosting | Confirmed in repository configuration and README. Preserve established theme behavior when extending it. |
| Org mode + ox-hugo for long-form posts | Keeps literate authoring and Emacs workflow; edit canonical Org rather than generated Markdown. |
| Pages CMS for lightweight and mobile editing | Complements Org without mixing canonical sources. Separate directories are mounted into one Hugo post section. |
| main for real content, including drafts; staging for experiments | Explicit branch policy. Promotion to main happens when Diego asks. |
| Separate production, draft, and staging deployments | Historical confirmed setup: production from main excludes drafts; draft site from main sets `BUILD_DRAFTS=true`; staging from staging. Current Netlify account settings still need verification. |
| Zurich local timestamps for lightweight posts | Avoids marking local time as UTC. Hugo explicitly interprets zoneless timestamps in `Europe/Zurich`. Preserve timezone-bearing historical dates. |
| Feature-image generation creates a review PR | Confirmed current workflow; images require review and are not auto-merged. |
| Photo uploads commit content and images together | Current function uses Git blobs/tree/commit and a non-forced ref update with retries, avoiding partial posts. |
| Photos have their own card listing; Blog excludes photos | Confirmed in both branches; photo-tag filtering occurs before Blog pagination. |

## Project instructions for the receiving Codex session

These are Diego's current project instructions. Read repository `AGENTS.md` and any more specific instructions too, but prefer these explicit user instructions where they conflict with older generic guidance.

- Inspect the relevant files and target branch before changing anything. Current GitHub code/content outranks earlier chat descriptions.
- Use `staging` for experiments and site changes unless Diego specifies another branch. Bring changes to `main` when asked.
- Keep content commits separate from tooling/theme commits where practical. Report the branch and commit containing the result.
- Long-form source is `content-org/zzamboni.org`; exports are under `content/post/`. Edit Org source. Create/update Markdown previews when requested. Keep requested drafts unpublished.
- Do not add an explicit draft frontmatter property to an Org `DRAFT` heading: ox-hugo can otherwise emit duplicate draft keys. An `EXPORT_DATE` timestamp can provide useful draft ordering.
- Check existing Hugo, Blowfish, Pages CMS, linkblog, and photoblog conventions before changing those flows.
- All automated commit subjects should start with `auto:`. Existing categories include pagescms, summary, linkblog, photoblog, feature-image, and favicon. Current automation often uses paths rather than titles; do not assume the older title-only proposal is implemented everywhere.
- Netlify build minutes are limited. Run relevant local checks before pushing; batch related changes when sensible. A push can trigger production, draft, staging, or PR-preview builds. Do not launch unnecessary live builds.
- Explain what changed, what was verified, and what still needs a live deploy check.
- Commands intended for Diego's laptop must use Elvish syntax. Repository workflow scripts may use their existing shell.
- Use the installed `blowfish` skill when relevant. Its current catalog path is `skill://flora-user-skills/root/.codex/skills/remote-skills/skill-6ab907f964008191ae87c4d0dd7d5b6a`; locate the equivalent installed skill in the receiving environment if needed.
- Never edit generated `public/` by hand.

## Architecture and relevant paths

Paths below are relative to the checkout, not paths on Diego's laptop.

| Area | Paths and role |
| --- | --- |
| Instructions and overview | `AGENTS.md`, `README.md` |
| Canonical long-form content | `content-org/zzamboni.org`, `content-org/images/` |
| Org exports and ordinary site pages | `content/post/`, `content/`; do not treat all content as Org-generated |
| Lightweight posts | `content-pagescms/*.md`, TOML frontmatter |
| Photo posts | `content-photos/<bundle>/index.md`; uploaded photos in `static/img/photos/<bundle>/` |
| Legacy posts | `content-legacy/`, YAML-frontmatter Markdown/HTML; canonical editable source for these posts |
| CMS | `.pages.yml` |
| Hugo config | `config/_default/{hugo,module,params,menus.en,languages.en,markup}.toml` |
| Tool/deployment pins | `mise.toml`, `netlify.toml`, `.gitmodules`, `themes/blowfish` |
| Functions | `netlify/functions/linkblog.mjs`, `netlify/functions/photoblog.mjs` |
| Layouts and assets | `layouts/`, `assets/css/custom.css`, `assets/css/photo-lightbox.css`, `assets/js/photo-lightbox.js` |
| Automation | `.github/workflows/`, `scripts/`, `scripts/tests/` |
| Maintainer documentation | `docs/feature-image-generation.md`, `docs/linkblog-favicons.md`, `docs/openai-usage.md`, `docs/legacy-content.md`, `scripts/README-theme-updates.md` |

`config/_default/module.toml` mounts `content-pagescms`, `content-legacy`, and `content-photos` into `content/post`, alongside ordinary `content`. It also mounts `static/img` into `assets/img`, making those images available to Hugo resources. Preserve source ownership and URLs when altering mounts.

`hugo.toml` sets `timeZone = "Europe/Zurich"`, `buildDrafts = false`, `buildFuture = false`, post permalinks `/post/:slug`, and pagination size 100. Hugo generates Netlify `_redirects` and `_headers` using `layouts/index.redir` and `layouts/index.headers`; aliases are disabled in favor of those redirects.

Current main Hugo Extended pin is `0.166.0` in mise and Netlify. The Blowfish submodule pointer is `51a361e068b9975c7f1df8e2bb223db03fe49c2b`; a release version was not independently established. `.gitmodules` names upstream branch main, but the committed submodule SHA is the actual checkout pin.

## Customizations to preserve

- Custom homepage: `layouts/partials/home/custom.html` adapts the theme background homepage to display site title/content instead of the author profile. `scripts/theme-overrides.toml` records indirect upstream dependencies for review.
- Deployment identification: `layouts/partials/deployment-banner.html`, `layouts/_default/baseof.html`, `layouts/partials/head.html`, and `assets/css/custom.css` support non-production banners/title handling. History reports yellow STAGING/DRAFT banners, production links, and a fix for the hidden skip link intercepting clicks. Verify visual behavior when updating the theme.
- Linkblog: `externalUrl` is the current semantic marker. `layouts/partials/extend-article-link.html` supplies domain/link badges, tags, and cached favicons; `extend-single-header.html` displays the full external URL. CSS gives compact lists. History reports list entries linking directly to the external destination; verify the current theme integration before modifying it. The `linky` tag is legacy convention, not a requirement for current functions, which default to `zznippets`.
- Photo gallery: `layouts/partials/photo-gallery.html`, `layouts/_default/single.html`, and `layouts/partials/extend-head-uncached.html` render the `photos` frontmatter list and load gallery/GLightbox assets even without a gallery shortcode. Commentary appears above the gallery. The lightbox supports looping, touch/keyboard navigation, a counter, focus handling, and reduced motion.
- Blog filter: `layouts/post/list.html` removes entries tagged `photos` before pagination. This is scoped to the Blog section; do not assume search, homepage, RSS, or other taxonomies exclude photos.
- Photos page: `content/tags/photos/_index.md` sets `cardView: true`. This is the photos tag page, not a new physical Hugo photos section.
- Feature-image behavior: `layouts/partials/functions/feature-image.html`; consult it before changing fallbacks or bundles. `params.toml` enables list feature-image hover behavior and uses a custom homepage, ocean colors, dark default with automatic appearance switching, search, and accessibility options.
- Comments: `layouts/partials/comments.html` and its recorded upstream wrapper dependency preserve Disqus integration; current article-wide `showComments` is false.

## Publishing and automation workflows

### Pages CMS

Current `.pages.yml` defines Blog posts, Photos, read-only Org exports for image actions, and separate legacy Markdown/HTML collections. Legacy posts retain filenames, slugs, aliases, and raw HTML/shortcodes; create new lightweight posts in Blog posts instead.

Current Blog and Photos defaults are `draft: true`. The Blog `featureimage` field is visible with fallback `img/tram-zurich.jpg`. Older notes saying drafts default false and feature image is hidden are outdated. CMS dates use `yyyy-MM-dd'T'HH:mm:ss.SSS` without Z. Commit templates currently use `{path}`, or old/new paths for renames.

### Linkblog and photoblog from iOS

`linkblog.mjs` exposes POST `/api/linkblog`. It checks Bearer `LINKBLOG_SECRET`, writes using `LINKBLOG_GITHUB_TOKEN`, and targets `LINKBLOG_BRANCH` with fallback main. It accepts URL, optional title/commentary/date/tags/draft, fetches a title if omitted, normalizes dates to Zurich local time, and creates a Pages CMS post. Only boolean `draft: false` publishes. Response includes `ok`, `title`, `path`, and `editUrl`.

`photoblog.mjs` exposes POST `/api/photoblog`. Set `PHOTOBLOG_BRANCH` explicitly to main or staging in the Netlify **Function runtime** environment; build-time BRANCH is insufficient. It accepts 1–20 base64 strings in a JSON `photos` array, optional title/commentary/date/tags, and boolean draft. It supports JPEG, PNG, WebP, rejects animated/unsupported images, applies orientation, and re-encodes through sharp to discard embedded private metadata. Default tags include photos; default draft is true. It returns the CMS edit URL. Credentials can use `PHOTOBLOG_SECRET`/`PHOTOBLOG_GITHUB_TOKEN` or the respective LINKBLOG fallbacks.

Main `package.json` pins sharp `0.35.5`; staging currently pins `0.35.4`. The photoblog function itself is identical across the checked heads. Its nominal 2.5 MB/image and 3 MB total guards are commented out; do not describe these as enforced limits. The 50-million-input-pixel guard is active. Deployment/platform request limits were not checked.

### GitHub Actions

| Workflow | Behavior and supporting paths |
| --- | --- |
| `generate-pagescms-summary.yml` | On relevant main/staging post changes or CMS/manual action, fills blank summaries from commentary or a fetched linked article. Preserves existing summaries; skips access/error/placeholder sources instead of inventing content. Uses `gpt-5-mini`; commits `auto: summary: ...` with rebase/push retries. |
| `fetch-linkblog-favicons.yml` | Fetches/caches icons for Pages CMS links, shared by host across other authoring sources; fallback globe. `scripts/fetch-linkblog-favicons.py`, `assets/img/linkblog-favicons/`, `docs/linkblog-favicons.md`. No browser requests to linked sites for icons. |
| `generate-feature-image.yml` | Manual/CMS action with post/style/art direction/force inputs; `scripts/generate-feature-image.py`; stores WebP in `assets/img/generated/`; updates export and matching Org metadata where applicable; creates `ai-feature-image/` review PR against launch branch. |
| `refine-feature-image.yml` | Owner `/refine-image ...` comment on supported same-repository image PR edits the latest image and commits to that PR branch. `/refine-image --status` checks without paid generation. Trusted code runs from main; uses `scripts/refine-feature-image-pr.py`. Avoid rerunning a paid edit just because posting its reply failed. |
| `openai-usage.yml` | Reusable/manual report, called after summary/image-generation jobs even on failure. `scripts/openai-usage.py`; `OPENAI_ADMIN_KEY` is separate from generation's `OPENAI_API_KEY`. Optional `OPENAI_CREDIT_DATE` and `OPENAI_CREDIT_AMOUNT` estimate latest-reload remainder and annual expiry; otherwise reports today's and month-to-date costs. This is not the actual prepaid ledger. Missing inputs/API failures do not block generation. |
| `mirror-to-gitlab.yml` | Mirrors both main and staging on push/manual run to https://gitlab.com/zzamboni/zzamboni.org.git using `GITLAB_MIRROR_TOKEN`; preserves GitHub as source of truth. Older main-only mirror descriptions are outdated. |

At the checked heads, `.pages.yml`, summary/generation/refinement/usage workflows, photoblog function, Blog filter, and Photos index have identical blobs on main and staging. This is a targeted check, not a claim of complete branch parity.

## Completed work and evidence

Repository-confirmed recent main commits:

| Commit | Result |
| --- | --- |
| `2dde4f5` | Reusable OpenAI usage and credit reporting. Diego separately reported it working. |
| `cb640da`, `572fc1f`, `836e86e` | Image refinement from PR comments and fixes to replies/permissions. History reports the corrected test run working on October 8. |
| `2a4264d` | Photos tag card view promoted from staging. |
| `4762016` | Blog photo filter promoted from staging. |
| `3d4d69c` | Private embedded image metadata removed from new photoblog uploads. Does not establish that historical images were cleaned. |
| `21554a7` | Photoblog tests moved outside Netlify functions so they are not deployed as endpoints. |
| `fd029bd` | Main sharp dependency update to 0.35.5, PR #42. |
| `5544339` | Draft post about phone linkblog/photoblog publishing; export at `content/post/2026-10-07-linkblog-and-photoblog-with-netlify-and-shortcuts/index.md` still has `draft = true`. |

Current docs also describe a completed legacy migration of 334 posts (9 Markdown, 325 HTML), preserving bytes and URLs. That count is documentation evidence, not a recount in this handoff. Theme-update tooling now reviews overrides and synchronizes Hugo pins rather than blindly copying a Homebrew version.

## Known issues, pending work, and suggestions

| Item | Status and next action |
| --- | --- |
| Netlify build budget | Confirmed user concern after an October 8 warning. Diego asked about disabling automatic builds and triggering manually. No evidence here that any setting was changed. Inspect actual deployment settings before implementing a build policy. |
| Branch divergence | Confirmed. Do a file/patch-level reconciliation; do not merge all staging history blindly. The sharp patch update is a concrete main/staging difference. Updating staging is a suggested follow-up, not performed or newly authorized by this handoff. |
| `AGENTS.md` drift | Confirmed: says no automated tests, but tests now exist; names `servedebug`, while mise defines `serve-drafts`; presents a simplified Netlify build command. Updating this document is a suggestion. User project instructions already require `auto:` for automated commits. |
| Gallery disappearance/counter overlap | Historical reports, potentially resolved by later GLightbox work. Current implementation exists, but this session did not reproduce or dismiss the problems. Check mobile, refresh/load behavior, single/multiple images, and counter/button overlap if touching galleries. |
| iOS payload problems | Historical missing title/commentary/editURL, string-valued draft, and string instead of photos array. Current function expects true JSON types. Verify the installed phone shortcut before declaring this active; an older Cherri file is not proof of current phone state. |
| Pages CMS availability | Historical outages; self-hosting was considered and deferred. This is not an adopted migration plan. |
| Summary failures and OpenAI credits | Historical issues: empty link-post summaries and expired prepaid credit. Current summary workflow handles linked sources, and reporting exists. Current balance, expiration, and live workflow health were not checked. |
| Automatic feature-image generation | Older discussion describes generation when missing; current inspected workflow is manual dispatch/CMS action with a PR. Do not promise a push-triggered image generator. |
| Latest weekly blog draft request | Visible recent conversation asks for draft idea #2 on main in Org. The text of idea #2 and completion evidence are absent here. Retrieve the specific idea/conversation or ask Diego before creating another draft. Do not identify it with the October 7 draft without evidence. |
| Laptop Codex continuity | This handoff can be attached/pasted into a laptop session. No laptop-only conversations, uncommitted changes, or hidden decisions were imported. |

Do not treat suggestions above as approved changes. The already-requested Blog photo filter/card view are completed, not pending tasks.

## Start here in the laptop checkout

1. Read this handoff and current `AGENTS.md`; inspect `git status`, branch, remotes, and fetched main/staging heads. Preserve local work. Initialize/check the Blowfish submodule if needed.
2. Confirm the concrete task and intended branch. Read affected files and current maintainer docs before editing.
3. For site work use `mise run serve` or `mise run serve-drafts`. For a production build use the repository-pinned Hugo, production environment, and intended base URL; reproduce relevant banner/draft conditions from `netlify.toml` when needed.
4. Theme work: `mise run theme-check`, `mise run theme-update`, `mise run theme-verify`. See `scripts/README-theme-updates.md`; updates require Python 3.11+, Git, mise, and network. Review generated override diffs and rendered pages; a successful build alone does not validate visual behavior.
5. Relevant offline Python checks: `python3 -m unittest discover -s scripts/tests`. Photo decoding/privacy checks: install current Node dependencies, then `npm run test:photoblog`. These are current main commands; verify package availability on the selected branch. Do not put tests under `netlify/functions/`.
6. Inspect affected rendered pages, responsive layout, and draft exclusion locally. Batch commits/pushes sensibly and report branch/SHA plus any remaining live checks. Do not trigger paid image generation or unnecessary deployment just to validate this handoff.

## Source pointers

The repository snapshot can be inspected at https://github.com/zzamboni/zzamboni.org/tree/fd029bd6171dd0bc5d29144c4ac96fd932fa3bc1 and the staging snapshot at https://github.com/zzamboni/zzamboni.org/tree/c1d349694cfe8ae0484785e94e6b267e13d67f49. Current project instructions and visible September–October 2026 conversation history provide rationale and historical status. Treat fresh repository/deployment evidence as authoritative for implementation details.
