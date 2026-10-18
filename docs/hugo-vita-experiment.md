# JSON Resume Hugo renderer

The CV and publications are native Hugo pages under `/vita/`, implemented through
reusable `layouts/jsonresume/` page layouts and `jsonresume` partials. JSON
Resume data is kept in `data/jsonresume/`, not inside the presentation code.

The content pages select the renderer explicitly in their TOML front matter:

```toml
# content/vita/_index.md
type = "jsonresume"
layout = "cv"
```

```toml
# content/vita/publications/index.md
type = "jsonresume"
layout = "publications"
```

The page layouts define Blowfish's `main` block and call the corresponding
`jsonresume` partials. The `type` selects the template namespace; the content
paths retain `/vita/` and `/vita/publications/`. No site-specific
`layouts/vita/` adapters are needed.

## Configuration

The host site supplies its data sources and download basename in
`config/_default/params.toml`:

```toml
[jsonresume]
  resumeData = "jsonresume.resume"
  publicationsData = "jsonresume.publications"
  resumeStem = "zamboni-vita"
  publicationsDescription = "Books, research papers, reports, presentations and patents."
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
The publication page title comes from Hugo front matter; its description uses
the page description by default and can be overridden with
`publicationsDescription` for compatibility with an existing layout.

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
