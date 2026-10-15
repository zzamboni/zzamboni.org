# Blog archive

`/archive/` provides a compact, unpaginated date/title listing grouped by year,
newest first, with year jump links and counts. It complements rather than
replaces `/post/`; the Blog header links to it and the archive introduction links
back. Main navigation is unchanged.

`content/archive/_index.md` selects `layouts/_default/archive.html`, which uses
the existing site base layout. `layouts/partials/archive-list.html` selects Hugo
regular pages in section `post`, including mounted Org, Pages CMS, and legacy
content. It matches the Blog's filter by excluding the `photos` tag. Linkblog
posts are retained, marked "Link", and point directly to `externalUrl`, matching
the existing listing behavior. Other sections are excluded.

Hugo's normal visibility rules apply: production omits drafts/future posts;
`mise run serve-drafts` includes drafts, which receive a draft badge. No special
source parsing, image processing, pagination, or client-side JavaScript is added.
No matching posts means the standard localized empty-list message.

Presentation uses the existing theme typography/colors and localized labels in
`i18n/en.yaml`, with narrowly scoped CSS in `assets/css/custom.css`. Dates occupy
a fixed narrow column; long titles wrap on small screens. Year headings have a
scroll offset for the fixed site header, and links have visible keyboard focus.

Validate locally:

```sh
mise exec -- python3 -m unittest discover -s scripts/tests -p test_archive.py
mise run serve
```

The isolated Hugo test checks mounted content, year/date ordering, counts,
external-link markers, photo/non-post exclusions, production/draft behavior,
empty output, and absence of pagination even with pager size 1. Inspect the
actual archive on desktop/mobile, including year jumps and long titles.
