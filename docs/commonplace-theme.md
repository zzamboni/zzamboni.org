# Commonplace theme experiment

The `experiment/commonplace-hugo` branch started from staging and now follows
`main`. The experiment adds a local Hugo theme over the site's pinned Blowfish
version. Its paper and forest palette, Georgia typography, notebook
illustration, editorial article lists, and reading layout come from
**Diego — Commonplace** (source commit `4fe89164b4a16e0fabb58acfd3da7292d9612b63`).

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

Use `mise run serve` or `mise run serve-drafts` on this branch. The Hugo
and Blowfish pins come from `main`. The overlay needs no Tailwind rebuild or
additional npm packages.

The draft pull request targets `main` so the Files changed view isolates the
presentation layer. To refresh the experiment, bring over the new `main` tree,
reapply the overlay changes, and compare production and draft builds with
`main`. Switch back to `main` for the production design.
