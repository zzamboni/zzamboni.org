# Native CV page (experimental)

This branch renders `/vita/` as a native Hugo page inside Blowfish using a
snapshot of `zzamboni/vita/zamboni-vita-general.json` in
`data/vita/resume.json`. This JSON is a copied fixture, not a live sync.

- `content/vita/index.md`: Hugo page route and metadata.
- `layouts/vita/single.html`: Blowfish-compatible CV layout and section order.
- `layouts/partials/vita/entry.html`: shared section entry rendering.
- `assets/css/vita.css`: scoped responsive styling.

The former `static/vita/index.html` is removed to avoid an output collision.
PDF, BibTeX and the standalone publications page in `static/vita/` remain
available and unchanged. No deploy automation or upstream repository changes.

To test locally, run `mise run serve` and open `/vita/`; check light/dark
modes, desktop/mobile layout, PDF links, publications and generated page source.

Known limitations: this is a first pass at Eventide fidelity; the native page
does not yet reproduce every type-specific rendering detail, floating TOC,
badge artwork or Eventide typography.
