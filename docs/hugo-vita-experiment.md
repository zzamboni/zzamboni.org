# Hugo JSON Resume renderer: parameterization

This is the site-local Blowfish renderer pending extraction into a reusable
Hugo module. The page adapters in `layouts/vita/` define the public routes,
not the reusable partials. Site JSON snapshots remain in `data/jsonresume/`.

Configure the renderer via `[jsonresume]` in `config/_default/params.toml`:

| Parameter | Default | Purpose |
| --- | --- | --- |
| `dataNamespace` | `jsonresume` | Directory under Hugo `data/` |
| `resumeDataKey` | `resume` | Resume JSON filename without extension |
| `publicationsDataKey` | `publications` | Bibliography JSON filename without extension |
| `resumeFileStem` | empty | Filename stem for the `<resume>` placeholder, relative to the CV page |
| `publicationsPath` | `publications/` | Publications page relative to the CV section |
| `excludeLinkRoles` | empty | Metadata roles filtered from action links |

The publications title and description come from its Hugo content front
matter instead of the template. Action links resolve relative filenames
against the current CV or publications page; the `<resume>` replacement uses
the configured stem. The CV's bibliography note links to the publications
page resolved by Hugo's page tree where available.

The current site sets `resumeFileStem = "zamboni-vita"`, keeping
`/vita/zamboni-vita.pdf` stable. The module code contains no personal
filenames or hardcoded `/vita/` URLs. The site supplies its existing routes
via `content/vita/` and retains PDFs and BibTeX under `static/vita/`.

The underlying resume input is `zzamboni/vita/zamboni-vita-general.json`;
publications JSON is exported by resume-toolkit. Neither snapshot is synced
automatically yet.

For manual verification run `mise run serve` and inspect both `/vita/` pages,
including links, TOC, note entries, icons and mobile layout. A Hugo build and
Netlify deploy-preview are needed to verify template compatibility.
