# JSON Resume Hugo renderer

The CV and publications are native Hugo pages under `/vita/`, implemented through
thin `layouts/vita/` adapters and reusable `jsonresume` partials. JSON Resume
data is kept in `data/jsonresume/`, not inside the presentation code.

## Configuration

The host site supplies its data sources and download basename in
`config/_default/params.toml`:

```toml
[jsonresume]
  resumeData = "jsonresume.resume"
  publicationsData = "jsonresume.publications"
  resumeStem = "zamboni-vita"
  excludeLinkRoles = ["site-home"]
  # publicationsURL = "/vita/publications/"
```

The two data paths use dot-separated keys relative to Hugo's `data/` directory.
For example, `jsonresume.resume` reads `data/jsonresume/resume.json`.
The `resumeStem` option identifies the generated CV download stem, without
requiring a personal filename in the templates.

Link paths are resolved relative to the current page (and to the CV parent
for `<resume>` placeholders on publications). The CV's bibliography-note link
uses the child `publications/` page by default; `publicationsURL` overrides it.
The publication page title and description come from its Hugo front matter.

Reusable presentation is in `layouts/partials/jsonresume/` and scoped
`assets/css/jsonresume*.css`. It currently relies on Blowfish's icon,
breadcrumb and table-of-contents partials, and has not yet been extracted
into a standalone module.

Snapshots originate in `zzamboni/vita` and `resume-toolkit` and are
not automatically synchronized. Downloads remain under `static/vita/`.

## Review

Run `mise run serve` locally and inspect `/vita/` and
`/vita/publications/` for TOC links, icons, floating actions,
publication notes, PDF/BibTeX links, and mobile layout.
