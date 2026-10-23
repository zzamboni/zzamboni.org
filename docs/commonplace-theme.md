# Commonplace theme experiment

Branch: `experiment/commonplace-hugo`, based on staging commit
`c43d8cb0a59389be17f2b2d11d4161ee0d14cac8` (15 October 2026).

This is a local Hugo presentation theme layered over the pinned Blowfish v3.8.0,
not a replacement CMS or a standalone distributable theme. It recreates the
paper/forest palette, Georgia typography, notebook illustration, editorial rows,
and reading layout from **Diego — Commonplace**, source commit
`4fe89164b4a16e0fabb58acfd3da7292d9612b63`. The illustration is copied from that
site's inline SVG; there are no external font requests, new packages or AI assets.

## Structure and behavior

- `config/_default/hugo.toml`: theme precedence `["commonplace", "blowfish"]`.
  Site-level layouts remain higher priority than either theme.
- `themes/commonplace/`: palette, presentation CSS, localized labels, masthead,
  editorial rows, hero illustration and feature-image resolver.
- `layouts/partials/head.html`: includes the Commonplace CSS after existing CSS.
- `layouts/partials/home/custom.html`: new hero plus the existing `home/feeds.html`.
  The configurable photo column, square photos, image-less photo skipping and
  Blog photo filtering remain. Article thumbnails give way to text-led rows;
  cover images are rendered on individual reading pages.
- `layouts/_default/single.html`: keeps galleries, TOC, series, sharing, related
  content and comments; adds a back link, standfirst and proportional cover.
  `hideFeatureImage` suppresses the cover. An explicit `showHero = true` uses
  the existing hero renderer instead of adding a second cover. Photos retain
  their gallery rather than repeating their first image above it.
- `scripts/theme-overrides.toml`: registers the local theme's upstream contracts,
  which the update script's automatic site-layout scan does not discover.

Light appearance is the default; automatic OS switching is disabled for the
paper design. The existing appearance switch still works, including saved user
preferences, with an accompanying dark palette. A browser with a saved dark
preference may therefore open in dark mode.

Existing navigation, search index/modal, archive, taxonomies, RSS, redirects,
favicon/logo, deployment banners and all content directories/URLs are retained.
Article titles/arrow links open local reading pages. Link posts additionally
provide their external destination and cached-domain/tag metadata. This keeps
both commentary and the linked resource reachable without nested links.
The reference's database editor, category model and author sign-in are not ported:
Org/ox-hugo, Pages CMS, linkblog and photoblog remain the publishing system.

## Preview and rollback

Use `mise run serve` or `mise run serve-drafts` on this branch. The repository's
Hugo Extended 0.166.0 pin and Blowfish submodule pin are unchanged. No Tailwind
build or npm installation is required for this presentation layer.

The experiment changes default config only on its own branch. Switching back to
`staging` restores the existing design; do not merge this branch wholesale as a
way to move unrelated staging content into main. Removing only the theme-array
entry is insufficient, because the site hooks deliberately call its partials.
Revert the experiment commit for a complete rollback.

Validation in the implementation session:

- Hugo Extended 0.166.0 production build: 738 pages, no build errors.
- Draft build with staging banner: 746 pages, no build errors.
- Baseline vs experiment: 7,154 HTML output paths unchanged (including copied
  static HTML); RSS, search JSON, sitemap, redirects and headers byte-identical.
- Three comparison articles: reading structure, summaries, available covers,
  local images/scripts/styles, code blocks and external destination checked.
- Four renderable homepage photos and their links match staging. Blog photo
  filtering, archive rows, search/menu/appearance element IDs, preview banner,
  and production exclusion of the phone-publishing draft checked.
- TOML parsing and `git diff --check` passed.

Browser rendering and interaction checks remain necessary before adoption:
no browser executable was installed, and the Chromium download failed. There
are consequently no desktop/mobile screenshots or claimed visual sign-off.
No live deployment is implied by a successful build or branch push.
