# Upcoming series articles

The site overrides Blowfish's `series/series_base.html` to include unpublished
parts as plain text with an “Upcoming” label. Published parts retain their links
and the current article retains its usual label. No draft page is rendered.

The helper reads only TOML front matter from Markdown under `content/post/`,
recursively, once per production build through `partialCached`. This covers the
Org-authored articles in the series. Drafts in other content roots or using other
front matter formats are not included. There is no separate list to maintain:
`title`, `series`, `series_order`, and `draft` in the Markdown exports are the source.
Only draft titles and part numbers are exposed; bodies and summaries are not used.

Entries already present in Hugo's series collection take precedence, so a build
with `hugo -D` keeps draft links for reviewing. Publishing an article automatically replaces its
Upcoming row with a normal link on the next build.

## Local review

Run `mise run serve` to see production behavior and `mise run serve-drafts` to
check draft links. Expand the series on any article in “My website setup”. Check
both desktop and mobile widths and light/dark appearance. In the production build,
parts 3, 6, 7, 8, 11, and 12 should be unlinked Upcoming rows. Check that those
pages are absent from the production output, search index, RSS, and sitemap.

The series taxonomy landing page retains Blowfish's normal published-only listing.
The override applies to the series navigation at the top and bottom of articles.
