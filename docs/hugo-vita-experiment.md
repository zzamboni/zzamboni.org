# JSON Resume Hugo integration

The CV and publications at `/vita/` and `/vita/publications/` are native Hugo
pages rendered by the Blowfish-specific module
[`zzamboni/hugo-jsonresume`](https://github.com/zzamboni/hugo-jsonresume).
The reusable layouts, partials and three namespaced stylesheets now live in
that repository. There are no local renderer copies to keep in sync.

## Host responsibilities

- `content/vita/_index.md`: `type = "jsonresume"`, `layout = "cv"`.
- `content/vita/publications/index.md`: the same type, `layout = "publications"`.
- `data/jsonresume/resume.json` and `publications.json`: host-owned snapshots
  from `zzamboni/vita` and resume-toolkit. Automatic synchronization remains
  a separate follow-up.
- `static/vita/`: existing PDFs, BibTeX and images; URLs remain unchanged.
- `config/_default/params.toml`: data paths, download stem, introduction and
  semantic link-role filtering. These site-specific settings are not module
  defaults.
- `themes/blowfish/`: the existing pinned submodule supplies the base layout,
  icons, breadcrumbs and TOC. The renderer module does not import Blowfish.

The module is imported in `config/_default/module.toml` alongside the site's
existing mounts. `go.mod` pins its exact pseudo-version; `go.sum` records
checksums. Do not replace the pin with a moving branch or commit local Go
replacement paths. Go 1.25 is selected in mise and Netlify; install the local
tools with `mise install` before building.

## Configuration

```toml
[jsonresume]
  resumeData = "jsonresume.resume"
  publicationsData = "jsonresume.publications"
  resumeStem = "zamboni-vita"
  publicationsDescription = "Books, research papers, reports, presentations and patents."
  excludeLinkRoles = ["site-home"]
  # publicationsURL = "/vita/publications/"
```

The data paths use dot-separated Hugo data keys. Relative action links use
the current page; `<resume>` uses the CV page plus `resumeStem`, including
when linked from publications. The bibliography-note link defaults to the
CV's `publications/` child, with `publicationsURL` as an optional override.
Page front matter supplies the title and default description; this site
keeps its existing introduction via `publicationsDescription`.

## Updating the renderer

Implement and test renderer changes in the module repository first. Then,
from a site feature branch based on current staging, run the update task:

```sh
mise run jsonresume-update
```

It imports the latest module `main` commit and shows the `go.mod`/`go.sum`
diff. To select a reviewed commit or version tag instead:

```sh
mise run jsonresume-update COMMIT_SHA
mise run jsonresume-update v0.1.0
```

The tag example applies once that release exists. The task only updates the
module pin and shows the diff; preview, commit and push remain explicit steps.

Commit `go.mod` and `go.sum` together. Run a production build and compare both
CV pages and generated styles against the previous pin. Review the Netlify
preview on desktop/mobile before merging. Use `mise run serve` to preview
locally. Site-level overrides remain possible at the imported template/asset
paths, but should be deliberate and documented.

The module README owns the renderer's full data contract and its synthetic
example. This document owns the site's routes, inputs and integration.
