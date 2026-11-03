# Blog archive

`/archive/` uses [hugo-blog-archive](https://github.com/zzamboni/hugo-blog-archive),
a theme-independent Hugo module with a Blowfish palette. Its shared partials
render the compact year/date/title list and linked posts-per-year chart.

The host-owned `content/archive/_index.md` retains its title and introduction.
`layouts/_default/archive.html` retains the site's Blowfish heading/base layout
and calls `blog-archive/render.html`. No head hook or JavaScript is required.

`config/_default/module.toml` imports the module and `go.mod`/`go.sum` pin it.
`params.toml` configures `blogArchive.sections = ["post"]`,
`excludeTags = ["photos"]`, `style = "blowfish"`, descending ordering, and the
chart. Mounted Org exports, Pages CMS, and legacy posts remain in the archive;
photo posts and other sections remain excluded. External destinations and draft
badges keep their previous behavior. Chart counts come from the listed pages;
empty years remain visible, and undated drafts stay outside the chart.
Existing `#year-YYYY` links are preserved.

Hugo's visibility rules still apply. Production omits unpublished content;
`mise run serve-drafts` includes drafts. This is a display filter, not a privacy
mechanism. The archive stays unpaginated. Module CSS and namespaced translations
replace the former site-owned archive CSS/partials/strings. The Blog link and
its `archive_browse` translation remain site-owned.

To update deliberately, run:

```sh
hugo mod get github.com/zzamboni/hugo-blog-archive@main
```

Review/commit the resulting module pin changes and verify the archive before
pushing. Do not commit a local module replacement.

Validate locally:

```sh
mise exec -- python3 -m unittest discover -s scripts/tests -p test_archive.py
mise run serve
```

The site test checks the real imported renderer with mounted content, ordering,
counts, publication visibility, external links, year anchors, empty/undated
archives and absence of pagination. Broader configuration/localization tests
live in the module repository. For development before publishing a module
revision, `HUGO_BLOG_ARCHIVE_DIR` can point the test at a local module checkout;
the test adds a replacement only inside its disposable fixture.

Inspect `/archive/` on desktop/mobile in light/dark mode, including long titles,
chart scrolling, focus visibility, and year jumps. The module's public example
sites demonstrate the generic and Blowfish presentations.
