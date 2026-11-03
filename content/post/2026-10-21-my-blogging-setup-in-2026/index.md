+++
title = "My blogging setup in 2026: reducing friction"
author = ["Diego Zamboni"]
summary = "My updated blogging setup: Org mode for longer articles, Pages CMS and iPhone Shortcuts for quick posts, hugo-jsonresume for the CV, and Hugo, GitHub and Netlify to bring it all together."
date = 2026-11-02T14:16:00+01:00
tags = ["blogging", "howto", "emacs", "orgmode", "hugo", "pagescms", "github", "netlify"]
draft = false
creator = "Emacs (Org mode + ox-hugo)"
toc = true
featureimage = "img/generated/2026-10-21-my-blogging-setup-in-2026.webp"
series = ["My blogging setup"]
series_order = 1
+++

In 2020 I wrote about [my blogging setup with Emacs, Org mode, ox-hugo, Hugo, GitLab and Netlify]({{< relref "2020-12-11-my-blogging-setup-and-workflow" >}}). Much of that setup is still here: I still write my articles in Emacs and export them with `ox-hugo`, while Hugo and Netlify turn files into a website.

Still, you may have noticed that I [barely posted anything](/archive/) since then! The biggest issue was friction: I wanted to make it easier to publish something small: a useful link, a few photos, or a note that did not need to become a full article. Opening my laptop and going through the whole writing, export and push routine was often enough friction for me to put it off.

For this reason, over the last few weeks I have added a few more ways to get content into the site. This post is an overview of the current setup, with links to the more focused articles (some of them not published yet) about specific aspects. My website's [repository](https://github.com/zzamboni/zzamboni.org) contains the complete setup; its [documentation directory](https://github.com/zzamboni/zzamboni.org/tree/main/docs) is where I keep maintenance details.

{{< note >}}
Like much of the world, I've started using AI tools to improve my workflows. Specifically, I've used ChatGPT and Codex extensively throughout this work, from discussing the architecture and exploring alternatives to implementing changes and debugging workflows. Being able to work through an idea, try it in the repository, and refine it together has made many of these improvements much easier to tackle. I still make the decisions and review the results, but a lot of the work described here has been a collaboration. It's an amazing advantage to have an assistant that can transform a natural language description into code, whether it's CSS, JavaScript or Hugo markdown.
{{< /note >}}


## Overview {#overview}

My new setup makes it possible to combine multiple sources of content into a single website, using consistent formats and tooling, as shown in this diagram. The next sections go into more detail about its different paths.

{{< mermaid >}}
---
config:
  theme: base
  themeVariables:
    primaryTextColor: "#DCE7F5"
    primaryColor: "#26374D"
    primaryBorderColor: "#6599D4"
    lineColor: "#94A8BF"
    edgeLabelBackground: "#26374D"
    clusterBkg: "#26374D"
    clusterBorder: "#607C9B"
    tertiaryColor: "#26374D"
    fontSize: "16px"
  flowchart:
    htmlLabels: false
    curve: basis
    nodeSpacing: 40
    rankSpacing: 55
---
flowchart TB
    subgraph sources["CONTENT SOURCES"]
        direction LR
        org["🦄️ Org mode"]
        cms["📝 Pages CMS"]
        ios["📱 iOS Shortcuts"]
        cv["📄 JSON Resume"]
    end

git["🐙 GitHub Repo"]
hugo["🐡️ Hugo +<br/>Blowfish"]
netlify["☁️ Netlify"]
site["🌐 zzamboni.org"]

org -->|"ox-hugo"| git
cms --> git
ios -->|"Netlify Functions"| git
cv -->|"resume-toolkit"| git

git --> hugo
hugo --> netlify
netlify --> site

classDef source fill:#EAF3FF,stroke:#6699D0,color:#1D426B,stroke-width:1.5px
classDef repository fill:#F0EAFF,stroke:#9370D2,color:#493080,stroke-width:2px
classDef build fill:#E7F5F0,stroke:#55A58B,color:#205D4C,stroke-width:2px
classDef deploy fill:#FFF2E3,stroke:#E5A45A,color:#805020,stroke-width:2px
classDef website fill:#E7F0FF,stroke:#417ED4,color:#174782,stroke-width:2.5px

class org,cms,ios,cv source
class git repository
class hugo build
class netlify deploy
class site website

style sources fill:transparent,stroke:#A9B9CA,stroke-dasharray:4 4,color:#DCE7F5
{{< /mermaid >}}


## Org mode for long-form writing {#org-mode-for-long-form-writing}

For an article like this one, I still prefer writing in [`content-org/zzamboni.org`](https://github.com/zzamboni/zzamboni.org/blob/main/content-org/zzamboni.org). I can use the full power of Emacs and Org mode to develop the text, rearrange sections, include code, and keep related posts together. `ox-hugo` exports the article to Markdown under `content/post/`, which is what Hugo reads.

That distinction is worth keeping explicit: the Org file is the source, and the Markdown is an export. If I fix a paragraph only in the Markdown, the next export will erase that change. I keep both in Git, so building the website does not require Emacs or my personal Emacs configuration.

My [original article]({{< relref "2020-12-11-my-blogging-setup-and-workflow" >}}) goes into the Org and `ox-hugo` side in more detail. I have not replaced that workflow, but I created new posting paths for shorter things.

{{< figure src="20261029-161728_org-mode-writing.png" caption="<span class=\"figure-number\">Figure 1: </span>My Emacs screen while writing this article" >}}


## A browser editor for the smaller things {#a-browser-editor-for-the-smaller-things}

This whole thing started by asking myself how to reduce friction for posting. I have found [Pages CMS](https://pagescms.org/) is perfect for this: it lets me edit posts through a browser, including on my phone. It adds and edits files directly  in my GitHub repository. Posts created with Pages CMS are stored in  `content-pagescms/` already in the format Hugo expects.

The key trick here is [Hugo's module mounts](https://gohugo.io/configuration/module/#mounts), which allow different locations to be merged into the same folder when Hugo builds the site. With modules, the Org exports and the CMS files can live in different directories (which simplifies their management through different tools), but Hugo presents them as posts in the same section.

I described the arrangement in [Using Pages CMS alongside Org mode and Hugo]({{< relref "2026-09-28-using-pagescms-alongside-org-and-hugo" >}}). It's also worth mentioning [the timezone problem]({{< relref "2026-09-26-pages-cms-hugo-timezones" >}}) I ran into due to a bug in Pages CMS's handling of timezone conversions.

{{< gallery >}}
{{< figure src="pagescms1.png" caption="<span class=\"figure-number\">Figure 2: </span>Pages CMS post list" >}}

{{< figure src="pagescms2.png" caption="<span class=\"figure-number\">Figure 3: </span>Pages CMS post collections" >}}

{{< figure src="pagescms3.png" caption="<span class=\"figure-number\">Figure 4: </span>Pages CMS post editing screen" >}}
{{< /gallery >}}


## Links and photos from the Share Sheet {#links-and-photos-from-the-share-sheet}

For links and photos, I wanted an even simpler workflow. These are things I'm likely to share while using my phone, so minimizing friction is particularly important. For this I developed a couple of specialized iOS Shortcuts paired with corresponding server-side functionality (in the form of [Netlify Functions](https://docs.netlify.com/build/functions/overview/)) that collect the shared URL or images, ask for a little context, and create the files in GitHub.

{{< feature-grid >}}
{{< feature icon="link" title="Post Link" url="https://www.icloud.com/shortcuts/cad708218dd348598a43ba394e7f75b5" label="Get Shortcut" />}}
{{< feature icon="image" title="Post Photos" url="https://www.icloud.com/shortcuts/437c4651085e42da9b465c3f0d2857da" label="Get Shortcut" />}}
{{< /feature-grid >}}

Both links and photos end up in the same Hugo content model, but I give them different presentations: compact entries for links, and galleries with a lightbox for photos. I configured my [homepage](/) with a separate recent-photo column, and I've created a separate [Photos](/tags/photos/) link in the top menu, separate from the [Blog](/post/) listing and [Archive](/archive/).

The screenshots below show the complete process, from sharing a photo or link on my iPhone to seeing the resulting post on my website.

{{< gallery figureClass="grid-w33" >}}
{{< figure src="IMG_0275.jpg" caption="<span class=\"figure-number\">Figure 5: </span>Sharing an image from iOS." >}}

{{< figure src="IMG_0276.jpg" caption="<span class=\"figure-number\">Figure 6: </span>Adding optional commentary." >}}

{{< figure src="IMG_0279.jpg" caption="<span class=\"figure-number\">Figure 7: </span>Sharing a link from iOS." >}}
{{< /gallery >}}

{{< figure src="20261029-162927_link-photo-on-website.png" caption="<span class=\"figure-number\">Figure 8: </span>The end result: link and photo on my website homepage." >}}

Both shortcuts default to creating drafts, but this can be configured. My upcoming post _Posting links and photos from my phone with Netlify and iOS Shortcuts_ walks through the functions, the Shortcuts, and how the pieces fit together.


## A specialized source for my CV {#a-specialized-source-for-my-cv}

My [Curriculum Vitae](/vita/) is another kind of content, with its own specialized source format: [JSON Resume](https://jsonresume.org/) (I wrote about its transformation at [Porting my CV from Org+LaTeX to JSON Resume]({{< relref "2026-02-10-porting-cv-to-jsonresume" >}})). I keep my experience, education, projects, and other CV information as structured data, alongside BibTeX sources for my publications. That lets me reuse the information across my website and downloadable documents without maintaining each version by hand.

My own [resume-toolkit](https://github.com/zzamboni/resume-toolkit) produces the PDF documents and normalized publication data, and my [hugo-jsonresume Hugo module](https://github.com/zzamboni/hugo-jsonresume) renders the data as native Hugo pages. The CV and publications share the site's navigation and styling, while PDF and BibTeX downloads remain available. It is another entry point into the same website, alongside Org mode, Pages CMS, and the phone Shortcuts.

{{< figure src="cv-json-and-rendered.png" caption="<span class=\"figure-number\">Figure 9: </span>My CV's JSON Resume source, and the [rendered version in my website](/vita)." >}}

I'll describe this in more detail in the forthcoming article _Bringing my JSON Resume CV home to Hugo_.


## One repository, a few places to preview {#one-repository-a-few-places-to-preview}

I keep real content, including drafts, on the `main` branch of my [source repository](https://github.com/zzamboni/zzamboni.org). I use the `staging` branch for experiments with templates, configuration, and tooling.

Netlify gives me separate production, draft, and staging sites. Production builds `main` without drafts. The draft site builds the same branch with drafts included, when I request a refresh. Staging lets me try site changes before bringing them to `main`, and is also built upon request.

Locally I use [mise](https://mise.jdx.dev/) to select the repository's Hugo and Go versions. My usual preview commands are:

```elvish
mise run serve
mise run serve-drafts
```

I've also become more deliberate about triggering Netlify builds. I am lucky to be on a [Netlify free legacy plan](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-legacy-plans/legacy-pricing-plans/) which includes a very generous 300 build minutes per month, but I'm still able to exhaust them with all my tinkering :smile: Documentation edits and many draft-only changes do not need a production deployment, and caching Hugo's generated resources saves repeated image work. I grouped those decisions in the upcoming article _Drafts, previews, and fewer Netlify builds_.


## Small bits of automation {#small-bits-of-automation}

GitHub Actions handles some of the finishing work:

-   For Pages CMS posts, an enrichment workflow fills missing summaries and caches favicons for linked sites.
-   I also built some automation for AI-powered generation of feature images. I request an image, the workflow proposes it in a pull request, and I decide whether to use it. I am still wary of illustrations that look too obviously AI-generated, so having a review step matters more to me than having a completely automatic process.

The upcoming _Automating blog housekeeping with GitHub Actions_ describes those boundaries, including image refinement and the usage report that helps me keep track of API spending.


## Outcomes and what comes next {#outcomes-and-what-comes-next}

There are certainly more moving parts here than in the 2020 version. The payoff is that I can choose a writing path that matches the thing I want to publish, while the result still belongs to the same website and Git continues to be the source of truth for everything.

For a long article, I open Emacs. For a short note, I open Pages CMS. For a link or photo, I use the Share Sheet. Then I can review, edit, and publish when I am ready. That is the part I wanted to make easier. Now I just have to remember to spend some of the time writing instead of improving the tools!
