+++
title = "My blogging setup in 2026: more ways to write, reducing friction"
author = ["Diego Zamboni"]
summary = "My updated blogging setup: Org mode for longer articles, Pages CMS and iPhone Shortcuts for quick posts, hugo-jsonresume for the CV, and Hugo, GitHub and Netlify to bring it all together."
date = 2026-10-21T12:00:00+02:00
tags = ["blogging", "howto", "emacs", "orgmode", "hugo", "pagescms", "github", "netlify"]
draft = true
creator = "Emacs 30.2 (Org mode 9.7.39 + ox-hugo)"
toc = true
+++

In 2020 I wrote about [my blogging setup with Emacs, Org mode, ox-hugo, Hugo, GitLab and Netlify]({{< relref "2020-12-11-my-blogging-setup-and-workflow" >}}). Much of that setup is still here: I still write in Emacs, still export them with `ox-hugo`, and still let Hugo and Netlify turn files into a website.

Still, you may have noticed that I [barely posted anything](/archive/) since then! The biggest issue was friction: I wanted to make it easier to publish something small: a useful link, a few photos, or a note that did not need to become a full article. Opening my laptop and going through the whole writing, export and push routine was often enough friction for me to put it off.

For this reason, over the last few weeks I have added a few more ways to get content into the site. This post is an overview of the current setup, with links to the more focused articles (some of them not published yet) about specific aspects. My website's [repository](https://github.com/zzamboni/zzamboni.org) contains the complete setup; its [documentation directory](https://github.com/zzamboni/zzamboni.org/tree/main/docs) is where I keep maintenance details.

{{< note >}}
Like much of the world, I've started using AI tools to improve my workflows. Specifically, I've used ChatGPT and Codex extensively throughout this work, from discussing the architecture and exploring alternatives to implementing changes and debugging workflows. Being able to work through an idea, try it in the repository, and refine it together has made many of these improvements much easier to tackle. I still make the decisions and review the results, but a lot of the work described here has been a collaboration. Having an assistant that can transform a natural language description of how I want my website to look or function, and to transform it quickly into code, whether it's CSS, Javascript or Hugo markdown, it's an amazing advantage.
{{< /note >}}


## Org mode for long-form writing {#org-mode-for-long-form-writing}

For an article like this one, I still prefer writing in [`content-org/zzamboni.org`](https://github.com/zzamboni/zzamboni.org/blob/main/content-org/zzamboni.org). I can use the full power of Emacs and org-mode to develop the text, rearrange sections, include code, and keep related posts together. `ox-hugo` exports the article to Markdown under `content/post/`, which is what Hugo reads.

That distinction is worth keeping explicit: the Org file is the source, and the Markdown is an export. If I fix a paragraph only in the Markdown, the next export will erase that change. I keep both in Git, so building the website does not require Emacs or my personal Emacs configuration.

My [original article]({{< relref "2020-12-11-my-blogging-setup-and-workflow" >}}) goes into the Org and `ox-hugo` side in more detail. I have not replaced that workflow, but I created new posting paths for shorter things.

{{< figure src="20261029-161728_org-mode-writing.png" caption="<span class=\"figure-number\">Figure 1: </span>My Emacs screen while writing this article" >}}


## A browser editor for the smaller things {#a-browser-editor-for-the-smaller-things}

[Pages CMS](https://pagescms.org/) lets me edit posts through a browser, including on my phone. It adds and edits files directly  in my GitHub repository. Posts created with Pages CMS are stored in  `content-pagescms/` already in the format Hugo expects.

The useful trick here is Hugo's module mounts, which allow different locations to be merged into the same folder when Hugo builds the site. With modules, the Org exports and the CMS files can live in different directories, but Hugo presents them as posts in the same `post` section. Older Markdown and HTML posts have their own home in `content-legacy/`, which gets merged into `post` as well. Since Pages CMS supports multiple content _collections_, I can view and edit these different types of content from Pages CMS as well.

I described the arrangement in [Using Pages CMS alongside Org mode and Hugo]({{< relref "2026-09-28-using-pagescms-alongside-org-and-hugo" >}}). It's worth mentioning a [the timezone problem]({{< relref "2026-09-26-pages-cms-hugo-timezones" >}}) I ran into due to a bug in how Pages CMS (does not) handles timezone conversions.

{{< gallery >}}
{{< figure src="pagescms1.png" caption="<span class=\"figure-number\">Figure 2: </span>Pages CMS post list" >}}

{{< figure src="pagescms2.png" caption="<span class=\"figure-number\">Figure 3: </span>Pages CMS post collections" >}}

{{< figure src="pagescms3.png" caption="<span class=\"figure-number\">Figure 4: </span>Pages CMS post editing screen" >}}
{{< /gallery >}}


## Links and photos from the Share Sheet {#links-and-photos-from-the-share-sheet}

For links and photos, I wanted an even easier path, since these are things I most likely want to post on the fly from my phone, so it needs to be extremely low-friction. For this I developed a couple of specialized iOS Shortcuts paired with corresponding server-side functionality (in the form of [Netlify Functions](https://docs.netlify.com/build/functions/overview/)) that collect the shared URL or images, ask for a little context, and create the files in GitHub.

Link posts live alongside the other Pages CMS posts in `content-pagescms/`, while photo posts are stored under `content-photos/`, with images stored separately under `static/img/photos/`. Photos are configured as a separate collection in Pages CMS, which allows managing them through the Pages CMS [media management](https://pagescms.org/docs/configuration/media/) features. They still enter the same Hugo content model, but I give them different presentations: compact entries for links, and galleries with a lightbox for photos. The [homepage](/) has a separate recent-photo column, and I've created a separate [Photos](/tags/photos/) link in the top menu, separate from the [Blog](/post/) listing and [Archive](/archive/).

{{< gallery figureClass="grid-w33" >}}
{{< figure src="IMG_0275.jpg" caption="<span class=\"figure-number\">Figure 5: </span>Sharing an image from iOS." >}}

{{< figure src="IMG_0276.jpg" caption="<span class=\"figure-number\">Figure 6: </span>Adding optional commentary." >}}

{{< figure src="IMG_0278.jpg" caption="<span class=\"figure-number\">Figure 7: </span>Editing the photo post in Pages CMS." >}}

{{< figure src="IMG_0279.jpg" caption="<span class=\"figure-number\">Figure 8: </span>Sharing a link from iOS." >}}

{{< figure src="20261029-162927_link-photo-on-website.png" caption="<span class=\"figure-number\">Figure 9: </span>The end result: link and photo on my website homepage." >}}
{{< /gallery >}}

Both functions default to creating drafts, but this can be configured in the Shortcuts. I can capture something while I am out and finish it later, without treating a successful upload as a decision to publish. My upcoming post _Posting links and photos from my phone with Netlify and iOS Shortcuts_ walks through the functions, the Shortcuts, and how the pieces fit together.


## A specialized source for my CV {#a-specialized-source-for-my-cv}

My CV is another kind of content, with its own specialized source: [JSON Resume](https://jsonresume.org/). I keep my experience, education, projects, and other CV information as structured data, alongside BibTeX sources for my publications. That lets me reuse the information across my website and downloadable documents without maintaining each version by hand.

[resume-toolkit](https://github.com/zzamboni/resume-toolkit) produces the documents and normalized publication data, and my [hugo-jsonresume module](https://github.com/zzamboni/hugo-jsonresume) renders the data as native Hugo pages. The CV and publications share the site's navigation and styling, while PDF and BibTeX downloads remain available. It is another entry point into the same website, alongside Org mode, Pages CMS, and the phone Shortcuts.

I'll describe this in more detail in the forthcoming article [Bringing my JSON Resume CV home to Hugo]({{< relref "2026-10-18-bringing-json-resume-cv-home-to-hugo" >}}).


## One repository, a few places to preview {#one-repository-a-few-places-to-preview}

GitHub is now the source of truth for the site; GitLab is a downstream mirror. That is a change from the original article, where GitLab was at the center of the publishing process.

I keep real content, including drafts, on `main`. I use `staging` for experiments with templates, configuration, and tooling. A draft is a content state, not a branch: putting an unfinished article on `main` is fine as long as it stays marked as a draft.

Netlify gives me separate production, draft, and staging sites. Production builds `main` without drafts. The draft site builds the same branch with drafts included, when I request a refresh. Staging lets me try site changes before bringing them to `main`.

Locally I use [mise](https://mise.jdx.dev/) to select the repository's Hugo and Go versions. My usual preview commands are:

```elvish
mise run serve
mise run serve-drafts
```

I also became more deliberate about when Netlify builds. Documentation edits and many draft-only changes do not need a production deployment, and caching Hugo's generated resources saves repeated image work. I grouped those decisions in [Drafts, previews, and fewer Netlify builds]({{< relref "2026-10-21-hugo-drafts-and-netlify-builds" >}}).


## Small bits of automation {#small-bits-of-automation}

GitHub Actions handles some of the finishing work. For Pages CMS posts, an enrichment workflow fills missing summaries and caches favicons for linked sites. Keeping those changes together also avoids creating separate commits for two parts of the same bit of housekeeping.

Feature images work differently. I request an image, the workflow proposes it in a pull request, and I decide whether to use it. I am still wary of illustrations that look too obviously AI-generated, so having a review step matters more to me than having a completely automatic process.

[Automating blog housekeeping with GitHub Actions]({{< relref "2026-10-21-automating-blog-housekeeping" >}}) describes those boundaries, including image refinement and the usage report that helps me keep track of API spending.


## Making it feel like one website {#making-it-feel-like-one-website}

The site uses [Blowfish](https://blowfish.page/), with my custom layouts and styles layered on top. The goal is fairly modest: articles should be comfortable to read, links should be quick to scan, and photos should be easy to browse. The compact archive and related-article links also help older posts remain discoverable.

I keep the theme pinned and use the [theme update tooling](https://github.com/zzamboni/zzamboni.org/blob/main/scripts/README-theme-updates.md) to review the upstream changes that might affect my overrides. I enjoy tweaking the site, but I would rather not rediscover the same customization after every upgrade.


## What I want from all this {#what-i-want-from-all-this}

There are certainly more moving parts here than in the 2020 version. The payoff is that I can choose a writing path that matches the thing I want to publish, while the result still belongs to the same website and lives in Git.

For a long article, I open Emacs. For a short note, I open Pages CMS. For a link or photo, I use the Share Sheet. Then I can review, edit, and publish when I am ready. That is the part I wanted to make easier. Now I just have to remember to spend some of the time writing instead of improving the tools.
