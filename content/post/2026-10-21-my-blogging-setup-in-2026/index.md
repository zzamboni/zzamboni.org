+++
title = "My blogging setup in 2026: more ways to write, one Hugo site"
author = ["Diego Zamboni"]
summary = "My updated blogging setup: Org mode for longer articles, Pages CMS and iPhone Shortcuts for quick posts, and Hugo, GitHub and Netlify to bring it all together."
date = 2026-10-21T12:00:00+02:00
tags = ["blogging", "howto", "emacs", "orgmode", "hugo", "pagescms", "github", "netlify"]
draft = true
toc = true
+++

<!-- Markdown preview exported from Org with Pandoc; edit the Org source. -->

In 2020 I wrote about [my blogging setup with Emacs, Org mode, ox-hugo, Hugo, GitLab and Netlify]({{< relref "2020-12-11-my-blogging-setup-and-workflow" >}}). Much of that setup is still here. I still write longer articles in Emacs, still export them with `ox-hugo`, and still let Hugo and Netlify turn files into a website.

The biggest change is at the beginning of that process. I wanted to make it easier to publish something small: a useful link, a few photos, or a note that did not need to become a full article. Opening my laptop and going through the whole export-and-push routine was often enough friction for me to put it off.

So I have added a few more ways to get content into the site. This post is a tour of the current arrangement, with links to the more focused articles where the configuration gets interesting. The [repository](https://github.com/zzamboni/zzamboni.org) contains the complete setup; its [documentation directory](https://github.com/zzamboni/zzamboni.org/tree/main/docs) is where I keep maintenance details that would make this post unnecessarily long.

I should also give some credit to Cody, my AI assistant: I've used ChatGPT and Codex extensively throughout this work, from discussing the architecture and exploring alternatives to implementing changes, debugging workflows, and writing initial drafts of these articles. Being able to work through an idea, try it in the repository, and refine it together has made many of these improvements much easier to tackle. I still make the decisions and review the results, but a lot of the work described here has been a collaboration.

## Org mode is still where I write

For an article like this one, I still prefer a heading in `content-org/zzamboni.org`. I can develop the text, rearrange sections, include code, and keep related posts together. `ox-hugo` exports the article to Markdown under `content/post/`, which is what Hugo reads.

That distinction is worth keeping explicit: the Org subtree is the source, and the Markdown is an export. If I fix a paragraph only in the Markdown, the next export can erase that change. I keep both in Git, so building the website does not require Emacs or my personal Emacs configuration.

My original article goes into the Org and `ox-hugo` side in more detail. I have not replaced that workflow. I have given the shorter things somewhere else to start.

## A browser editor for the smaller things

[Pages CMS](https://pagescms.org/) lets me edit posts through a browser, including on my phone. Its content is still made of files in my GitHub repository. A saved post lands in `content-pagescms/`, with the title, date, summary, tags, and draft status in its front matter.

The useful trick is Hugo's module mounts. The Org exports and the CMS files live in different directories, but Hugo presents them as posts in the same section. Older Markdown and HTML posts have their own home in `content-legacy/` too. I do not need to convert everything before using a new editor, or let two editors compete over the same source file.

I described the arrangement in [Using Pages CMS alongside Org mode and Hugo]({{< relref "2026-09-28-using-pagescms-alongside-org-and-hugo" >}}). That post also links to [the timezone problem]({{< relref "2026-09-26-pages-cms-hugo-timezones" >}}) I ran into. A field that looks like an ordinary date can hide a surprising amount of trouble!

## Links and photos from the Share Sheet

For links and photos, I wanted an even shorter path. My iOS Shortcuts collect the shared URL or images, ask for a little context, and send the result to a Netlify Function. The function creates the files in GitHub and returns an edit link for Pages CMS.

Link posts live alongside the other CMS posts. Photo posts get bundles under `content-photos/`, with images stored separately under `static/img/photos/`. They still enter the same Hugo content model, but I give them different presentations: compact entries for links, and galleries with a lightbox for photos. The homepage has a separate recent-photo column, and the Blog listing leaves photos to their own page.

Both functions default to creating drafts. I can capture something while I am out and finish it later, without treating a successful upload as a decision to publish. [Posting links and photos from my phone with Netlify and iOS Shortcuts]({{< relref "2026-10-07-linkblog-and-photoblog-with-netlify-and-shortcuts" >}}) walks through the functions, the Shortcuts, and how the pieces fit together.

## One repository, a few places to preview

GitHub is now the source of truth for the site; GitLab is a downstream mirror. That is a change from the original article, where GitLab was at the center of the publishing process.

I keep real content, including drafts, on `main`. I use `staging` for experiments with templates, configuration, and tooling. A draft is a content state, not a branch: putting an unfinished article on `main` is fine as long as it stays marked as a draft.

Netlify gives me separate production, draft, and staging sites. Production builds `main` without drafts. The draft site builds the same branch with drafts included, when I request a refresh. Staging lets me try site changes before bringing them to `main`.

Locally I use [mise](https://mise.jdx.dev/) to select the repository's Hugo and Go versions. My usual preview commands are:

``` elvish
mise run serve
mise run serve-drafts
```

I also became more deliberate about when Netlify builds. Documentation edits and many draft-only changes do not need a production deployment, and caching Hugo's generated resources saves repeated image work. I grouped those decisions in [Drafts, previews, and fewer Netlify builds]({{< relref "2026-10-21-hugo-drafts-and-netlify-builds" >}}).

## Small bits of automation

GitHub Actions handles some of the finishing work. For Pages CMS posts, an enrichment workflow fills missing summaries and caches favicons for linked sites. Keeping those changes together also avoids creating separate commits for two parts of the same bit of housekeeping.

Feature images work differently. I request an image, the workflow proposes it in a pull request, and I decide whether to use it. I am still wary of illustrations that look too obviously AI-generated, so having a review step matters more to me than having a completely automatic process.

[Automating blog housekeeping with GitHub Actions]({{< relref "2026-10-21-automating-blog-housekeeping" >}}) describes those boundaries, including image refinement and the usage report that helps me keep track of API spending.

## Making it feel like one website

The site uses [Blowfish](https://blowfish.page/), with my custom layouts and styles layered on top. The goal is fairly modest: articles should be comfortable to read, links should be quick to scan, and photos should be easy to browse. The compact archive and related-article links also help older posts remain discoverable.

My CV and publications now fit into that same presentation. Their source remains JSON Resume and BibTeX, with [resume-toolkit](https://github.com/zzamboni/resume-toolkit) producing documents and normalized publication data. My [hugo-jsonresume module](https://github.com/zzamboni/hugo-jsonresume) renders the data inside Hugo, while PDF and BibTeX downloads remain available. [Bringing my JSON Resume CV home to Hugo]({{< relref "2026-10-18-bringing-json-resume-cv-home-to-hugo" >}}) tells that story separately.

I keep the theme pinned and use the [theme update tooling](https://github.com/zzamboni/zzamboni.org/blob/main/scripts/README-theme-updates.md) to review the upstream changes that might affect my overrides. I enjoy tweaking the site, but I would rather not rediscover the same customization after every upgrade.

## What I want from all this

There are certainly more moving parts here than in the 2020 version. The payoff is that I can choose a writing path that matches the thing I want to publish, while the result still belongs to the same website and lives in Git.

For a long article, I open Emacs. For a short note, I open Pages CMS. For a link or photo, I use the Share Sheet. Then I can review, edit, and publish when I am ready. That is the part I wanted to make easier. Now I just have to remember to spend some of the time writing instead of improving the tools.
