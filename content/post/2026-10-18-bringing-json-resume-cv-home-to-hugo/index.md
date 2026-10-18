+++
title = "Bringing my JSON Resume CV home to Hugo"
date = 2026-10-18
draft = true
tags = ["jsonresume", "hugo", "blowfish", "cv", "blogging"]
summary = "How I brought my JSON Resume CV and publications into my Hugo site without giving up the standalone toolkit, PDFs, or BibTeX sources."
showTableOfContents = true
+++

Earlier this year I wrote about [moving my CV from Org and LaTeX to JSON Resume](/post/porting-my-cv-from-org-latex-to-json-resume/), and then about [extracting the build system into `resume-toolkit`](/post/2026-03-27-from-personal-cv-pipeline-to-reusable-toolkit/). That solved a problem I had wrestled with for years: keeping the content separate from how it is presented, while producing good-looking HTML and PDF versions of both my CV and publications.

There was one slightly awkward detail left. The CV on [my website](/vita/) was still a separate, pre-rendered HTML page using the [Eventide](https://github.com/zzamboni/jsonresume-theme-eventide) theme. It looked good, but it did not quite belong to the rest of the site, which uses [Hugo](https://gohugo.io/) and [Blowfish](https://blowfish.page/). It had its own navigation and styling. I wanted the CV to feel like part of the website without losing the independence I had worked so hard to create.

## One source, several presentations

I deliberately **did not** replace the JSON Resume source with Hugo content. My CV data still lives in [`zzamboni/vita`](https://github.com/zzamboni/vita), along with the BibTeX files and images. [`resume-toolkit`](https://github.com/zzamboni/resume-toolkit) still generates standalone HTML and PDFs, and Eventide remains useful independently of my website.

The Hugo integration is simply another consumer of that data. The distinction matters: I can change my website theme without changing the source of my CV, and I can use the same source to produce documents that have nothing to do with Hugo.

```text
zzamboni/vita
  JSON Resume + BibTeX + images
          |
          v
    resume-toolkit
    |            |
    v            v
 PDFs/BibTeX   normalized publications JSON
    |            |
    +------ Hugo/Blowfish ------+
                 |
                 v
         /vita/ and /vita/publications/
```

## Let Hugo do the rendering

Instead of copying the toolkit's generated `index.html` into `static/vita/`, I added native Hugo pages for [the CV](/vita/) and [the publications list](/vita/publications/). They use the site's Blowfish layout, responsive table of contents, header and footer. Small Hugo templates under `layouts/partials/jsonresume/` render the sections and entries, and scoped CSS handles the details specific to a CV.

The presentation code is separated from the public URL: thin templates under `layouts/vita/` connect the pages to reusable `jsonresume` partials. The data snapshots live under `data/jsonresume/`.

One pleasant benefit is that the CV no longer needs to pretend to be a different website. The same navigation and overall look that surround my posts now surround the CV as well.

## The bibliography was the interesting part

The CV itself was relatively straightforward because JSON Resume is already structured data. Publications were more complicated. Their source is BibTeX, including LaTeX commands and braces that should not appear literally on a web page. I also wanted to keep the established grouping of books, papers, presentations, patents, and other work.

Initially, the Hugo page consumed an independently generated JSON snapshot, but some LaTeX markup leaked through. The right fix was not to teach Hugo how to parse BibTeX. I added a JSON export to `resume-toolkit`'s existing publications pipeline so the HTML and JSON outputs share the same normalization, selection, ordering, and section titles. That output includes formatted titles and links for the PDF and aggregated BibTeX downloads.

There is a useful boundary here: **resume-toolkit knows about BibTeX; Hugo knows about HTML pages**. Neither has to impersonate the other.

## Little details that matter

As usual, most of the remaining work was in the details. Relative PDF and BibTeX links needed to resolve under `/vita/publications/`, not under `/vita/`. The CV has special note entries such as “Full list online” and “See full list on Credly,” whose titles are already links; treating them like ordinary entries produced redundant “view” links. We also adjusted the reusable templates to show affiliations and publishers and to avoid introducing a second HTML `main` landmark inside the site's existing one.

I also wanted certain navigation links to appear in the standalone Eventide version but not inside Hugo, where the site's navigation already provides them. A small, renderer-independent `role` field on the link, combined with Hugo's `excludeLinkRoles` setting, solved that without forcing website-specific behavior into the toolkit.

## Where things stand

The native CV and publications pages are now in the site's main branch, while the PDFs and BibTeX downloads keep their established URLs. I'm pleased with the result not just because it looks more integrated, but because the underlying pieces remain separately useful.

The next improvement is to make synchronization less manual. At the moment, updating the website involves generating the files from `zzamboni/vita` and copying the relevant JSON, PDFs, BibTeX, and images to the Hugo repository. I plan to turn that into a manually triggered GitHub workflow that proposes a pull request rather than deploying automatically.

It's a small architectural victory: **one source of truth, multiple outputs, and no need to rebuild the entire publishing system just to change how one page looks**.
