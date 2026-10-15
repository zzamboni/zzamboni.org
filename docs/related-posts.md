# Related articles

Articles in Hugo's `post` section show up to three related articles below the
body/sharing links, before pagination and comments. This covers mounted Pages
CMS posts, Org exports, and legacy articles without changing their source files.
Linkblog posts (`externalUrl`), photo-tagged posts, and posts with a `photos`
gallery neither display the section nor appear as recommendations. Non-post
pages such as About are excluded too.

Hugo's built-in `Pages.Related` performs the ranking and excludes the current
article. `config/_default/hugo.toml` uses case-insensitive tags only, threshold
80, and `includeNewer = true`: older tutorials can recommend newer articles.
Author/date matching was removed to avoid recommendations based merely on the
same author or publication period. No matches means no empty heading/section.
Draft visibility follows the Hugo build: production excludes drafts; draft
previews may recommend them.

`config/_default/params.toml` enables `article.showRelatedContent` and sets
`article.relatedContentLimit = 3`. Individual articles can opt out with
`showRelatedContent = false` in their canonical front matter (use the Org export
mechanism for Org-owned posts). This hides the section on that article; it does
not remove the article from other recommendations.

`layouts/partials/related.html` is a small override of Blowfish's related partial.
It reuses the theme's localized heading and `article-link/card-related.html` in
a responsive one/two/three-column grid, with an accessible section label. No
new JavaScript, CSS build, or external recommendation service is needed.
`scripts/theme-overrides.toml` tracks the indirect card dependency for upgrades;
the matching related partial is reviewed automatically.

Local validation:

```sh
mise exec -- python3 -m unittest discover -s scripts/tests -p test_related_content.py
mise run serve
```

The isolated Hugo test checks both authoring paths, tag case/newer matching,
self exclusion, the result limit, opt-out, no matches, and link/photo/non-post/
production-draft exclusions. Inspect actual cards locally on desktop and mobile;
ranking quality remains dependent on the tags assigned to posts.
