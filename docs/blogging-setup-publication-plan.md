# Blogging setup: publication plan

Prepared 2026-10-21 against `main`. This is a proposal, not a publication schedule. All five articles below remain drafts. Their canonical sources are subtrees in [content-org/zzamboni.org](../content-org/zzamboni.org); Markdown previews are linked below.

## Proposed order

Publish the focused articles first, then the overview as the updated entry point. This lets the overview link to working public articles from day one. The phone article also links to the two new supporting articles, so this order respects those dependencies.

| Order | Article | Status | Purpose / work before publishing |
| --- | --- | --- | --- |
| 1 | [Drafts, previews, and fewer Netlify builds](../content/post/2026-10-21-hugo-drafts-and-netlify-builds/index.md) | New draft | Groups branch roles, on-demand preview builds, conservative filtering, and resource caching. Review the account-specific description and historical timing figures; no new benchmark is needed. |
| 2 | [Automating blog housekeeping with GitHub Actions](../content/post/2026-10-21-automating-blog-housekeeping/index.md) | New draft | Groups summary enrichment, favicons, image generation/refinement, and usage reporting. Review the wording about AI assistance and optionally add one representative image PR screenshot. |
| 3 | [Posting links and photos from my phone with Netlify and iOS Shortcuts](../content/post/2026-10-07-linkblog-and-photoblog-with-netlify-and-shortcuts/index.md) | Existing draft, refreshed | Delivers the phone-publishing follow-up promised by the published Pages CMS article. Re-test both shared Shortcut imports and a link/photo round trip on the phone; verify their screenshots/instructions match the current versions. |
| 4 | [Bringing my JSON Resume CV home to Hugo](../content/post/2026-10-18-bringing-json-resume-cv-home-to-hugo/index.md) | Existing draft, refreshed | Continues the published CV/toolkit story. Now covers generic integration, configurable TOC, and the renderer-update workflow. Review the current CV data-copy procedure and the diagram in the draft preview. This article can move earlier independently. |
| 5 | [My blogging setup in 2026: more ways to write, one Hugo site](../content/post/2026-10-21-my-blogging-setup-in-2026/index.md) | New overview draft | The expanded README-style tour, about 1,100 words. Publish after the linked companions, then add a short update/link in the original 2020 article's Org source and re-export that article. Preserve its URL and historical text. |

If the overview should lead the series instead, temporarily replace links to unpublished companions with plain “forthcoming” mentions. Restore the links as each article is published. Hugo `relref` links to excluded drafts can fail a production build; don't publish the overview while its linked targets remain drafts.

Before publishing any article: review the text, set the intended publication date, change its Org state from `DRAFT` to `DONE`, export with ox-hugo, and check the resulting Markdown and local preview. Do not add a separate custom `draft` field. The dates currently attached to new drafts are drafting dates, not a promised publication schedule.

## Existing articles to reuse

These are already marked published in the repository; they do not need replacement drafts:

- [Original 2020 blogging setup](../content/post/2020-12-11-my-blogging-setup-and-workflow/index.md): historical baseline and later backlink to the new overview.
- [Using Pages CMS alongside Org mode and Hugo](../content/post/2026-09-28-using-pagescms-alongside-org-and-hugo/index.md): authoring separation, mounts, CMS fields, and draft defaults.
- [When a local timestamp pretends to be UTC](../content/post/2026-09-26-pages-cms-hugo-timezones/index.md): the focused timezone explanation.
- [Website redesign!](../content/post/2025-11-17-website-redesign/index.md): background on moving to Blowfish.
- [Porting my CV from Org+LaTeX to JSON Resume](../content/post/2026-02-10-porting-cv-to-jsonresume/index.md) and [resume-toolkit](../content/post/2026-03-27-from-personal-cv-pipeline-to-reusable-toolkit/index.md): predecessors to the Hugo CV article.

The published Pages CMS article still links to the old separate summary workflow. When publishing the housekeeping article, update that reference to `enrich-pagescms-posts.yml` in its Org source and export, and optionally add a link to the new article. This task leaves already-published articles untouched.

## Why only these new articles?

The existing Pages CMS and phone articles cover the publishing entry points. The CV draft covers the structured-data side. Build management and content housekeeping are the two remaining areas with enough substance for their own posts. Theme updates, the homepage, the archive, and related articles can stay as short overview mentions plus repository documentation links. Separate tutorials can wait until there is a specific story worth telling.

## Other drafts already in the repository

- [My blogging workflow with Emacs, org-mode+ox-hugo, Hugo and GitHub](../content/post/my-blogging-workflow.md) is an old, incomplete precursor to the published setup article. Treat it as superseded by the new overview rather than another publication in this series. It has been left untouched; removal can be a separate cleanup decision.
- [Enabling menubar indicators in Elementary OS](../content/post/2025-11-04-enabling-menubar-indicators-in-elementary-os/index.md), [CopyQ on Wayland](../content/post/2025-11-04-how-to-set-up-copyq-in-eos-with-wayland/index.md), [Networking-related setup](../content/post/2025-11-06-networking-related-setup/index.md), and [Vivaldi browser configuration in Linux](../content/post/2026-04-11-vivaldi-browser-configuration-in-linux/index.md) are separate Linux/browser backlog items. Their export files remain drafts; some are outlines. They do not block this series and need a current-system review before getting publication dates.

## Preview notes

The Markdown previews in this change were converted from the Org source with Pandoc because Emacs/ox-hugo was not available in the editing environment. Internal Org references were resolved to Hugo `relref` shortcodes, and front matter preserves draft status. Org remains canonical; normal future ox-hugo exports can replace these previews.

The Netlify draft site refreshes on demand. A repository commit does not itself establish that the remote draft preview is current. No live build or paid image generation is part of this drafting task.

Validation: Hugo Extended 0.166.0 completed both full draft and production builds using the pinned Blowfish revision. All five articles rendered with section headings and working article cross-links in the draft build, and all five were absent from production output. TOML metadata and repository/documentation link targets were checked locally. Phone interaction, Mermaid presentation, and the live Netlify preview still need editorial review.
