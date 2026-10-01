# Linkblog favicons

Simple article lists show a compact site icon beside entries with
`externalUrl`. Ordinary posts retain their feature images. Missing icons use
Blowfish's globe icon.

The **Fetch linkblog favicons** workflow runs when Pages CMS posts change on
`main` or `staging`. Changes to its script/workflow also backfill existing
Pages CMS links. It discovers HTML icon and Apple touch icon links, resolves
relative URLs and redirects, and falls back to `/favicon.ico`. Unavailable or
unsupported icons produce log messages and leave the globe fallback in place.

Icons are converted from raster/ICO/SVG to small PNGs and cached under
`assets/img/linkblog-favicons/<sha256-of-lowercase-host>.png`. All posts linking
to the same host share the icon, including legacy or Org-authored posts. No
post frontmatter or Org source is modified. The template uses Hugo resources
and fingerprints the published image; browsers do not contact the linked site.
SVG conversion disables external resource loading.

Future generated icon commits use `auto: favicon: <hostname(s)>` and contain
only icon assets. They do not retrigger the workflow.

For local use (after installing `pillow` and `cairosvg`):

```
python scripts/fetch-linkblog-favicons.py content-pagescms/my-link.md
python scripts/fetch-linkblog-favicons.py --refresh
```

Without paths, local runs check all Pages CMS posts. Existing icons are reused
unless `--refresh` is specified. To backfill a legacy/Org-only host, use a Pages
CMS link to that host as the discovery source.

The workflow also supports **Run workflow**: select a branch, optionally supply
a Pages CMS post path, and optionally enable refresh. GitHub exposes manual
dispatch only after this workflow exists on the default branch.
