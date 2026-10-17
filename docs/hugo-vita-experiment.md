# JSON Resume Hugo renderer (experimental)

The public routes stay at `/vita/` and `/vita/publications/` through
`content/vita/` and two thin layout adapters in `layouts/vita/`.

Reusable presentation lives in `layouts/partials/jsonresume/` and
`assets/css/jsonresume*.css`. JSON snapshots live in
`data/jsonresume/resume.json` and `data/jsonresume/publications.json`.
The source of the resume snapshot is `zzamboni/vita/zamboni-vita-general.json`.
The publication snapshot comes from the upstream bibliography. Neither is
automatically synchronized.

The renderer's action links use the content section's URL as their base,
with `<resume>` expanded to that section's `zamboni-vita` stem.
Semantic link role filtering is site-controlled in `[jsonresume]` in
`config/_default/params.toml`.

CSS class names are namespaced `jsonresume-*`, but the public URL remains
`/vita/` and legacy PDF and BibTeX files under `static/vita/` are unchanged.

Test: `mise run serve`, then inspect both `/vita/` pages for TOC links,
icons, floating actions, publications, PDF downloads and responsive layout.
