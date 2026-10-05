# Legacy posts

`content-legacy/` contains posts maintained directly as Markdown or HTML, with YAML frontmatter. Hugo mounts this directory into `content/post`, preserving the original filenames, slugs, aliases, and URLs. Pages CMS exposes these files in the **Legacy posts** collection.

`content/post/` retains the Org-generated posts and their bundle resources, plus the section index. Edit these posts in `content-org/zzamboni.org` and export with ox-hugo. Standalone pages are outside this migration.

The initial migration matched inherited Org `EXPORT_HUGO_SECTION`, `EXPORT_HUGO_BUNDLE`, and `EXPORT_FILE_NAME` properties against the exported paths, with the frontmatter `creator` as an additional check. It moved 334 legacy posts (9 Markdown and 325 HTML) without changing their bytes.

The collection disables creation and renaming: create new lightweight posts in **Blog posts**. Its code editor preserves HTML and shortcodes; the date is a string to retain historical date-only and timezone-bearing values. The existing CMS merge setting preserves unexposed frontmatter, including aliases. URL slugs are read-only.

**Generate image** works for saved legacy posts, and feature-image candidate discovery includes this directory. Legacy files remain their own canonical source; image generation does not update Org metadata for them. Summary and favicon automation remain scoped to `content-pagescms/`.
