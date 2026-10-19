+++
title = "Bringing my JSON Resume CV home to Hugo"
author = ["Diego Zamboni"]
summary = "How I brought my JSON Resume CV and publications into Hugo, and extracted the renderer into a reusable Blowfish module without giving up the standalone toolkit, PDFs, or BibTeX sources."
date = 2026-10-18T00:00:00+02:00
tags = ["jsonresume", "hugo", "blowfish", "cv", "blogging"]
draft = true
creator = "Emacs 30.2 (Org mode 9.7.39 + ox-hugo)"
toc = true
featureimage = "img/generated/2026-10-18-bringing-json-resume-cv-home-to-hugo.webp"
+++

Earlier this year I wrote about [moving my CV from Org and LaTeX to JSON Resume]({{< relref "2026-02-10-porting-cv-to-jsonresume" >}}), and then about [extracting the build system into `resume-toolkit`]({{< relref "2026-03-27-from-personal-cv-pipeline-to-reusable-toolkit" >}}). That solved a problem I had wrestled with for years: keeping the content separate from how it is presented, while producing good-looking HTML and PDF versions of both my CV and publications.

There was one slightly awkward detail left. The CV on [my website](/vita/) was still a separate, pre-rendered HTML page using the [Eventide](https://github.com/zzamboni/jsonresume-theme-eventide) theme. It looked good, but it did not quite belong to the rest of the site, which uses [Hugo](https://gohugo.io/) and the [Blowfish](https://blowfish.page/) theme. It had its own navigation and styling. I wanted the CV to feel like part of the website without losing the independence I had worked so hard to create.


## One source, several presentations {#one-source-several-presentations}

I deliberately **did not** replace the JSON Resume source with Hugo content. My CV data still lives in [`zzamboni/vita`](https://github.com/zzamboni/vita), along with the BibTeX files and images. [`resume-toolkit`](https://github.com/zzamboni/resume-toolkit) still generates the standalone HTML and the PDF documents, and Eventide is still useful independently of my website.

The Hugo integration is simply another consumer of that data. The distinction matters: I can change my website theme without changing the source of my CV, and I can use the same source to produce documents that have nothing to do with Hugo.

The flow now looks like this:

{{< mermaid >}}
flowchart TD
  source["&lt;a href='https://github.com/zzamboni/vita'&gt;zzamboni/vita&lt;/a&gt;:&lt;br/&gt;JSON Resume, BibTeX&lt;br/&gt;and images"]
  toolkit["&lt;a href='https://github.com/zzamboni/resume-toolkit'&gt;resume-toolkit&lt;/a&gt;"]
  downloads["PDFs and BibTeX&lt;br/&gt;downloads"]
  publications["Normalized&lt;br/&gt;publications JSON"]
  hugo["Hugo / Blowfish with&lt;br/&gt;&lt;a href='https://github.com/zzamboni/hugo-jsonresume'&gt;hugo-jsonresume&lt;/a&gt;"]
  pages["&lt;a href='/vita/'&gt;/vita/&lt;/a&gt; and&lt;br/&gt;&lt;a href='/vita/publications/'&gt;/vita/publications/&lt;/a&gt;"]

  source --> toolkit
  source -->|JSON Resume&lt;br/&gt;and images| hugo
  toolkit --> downloads
  toolkit --> publications
  publications --> hugo
  hugo --> pages
  downloads -->|Static files linked&lt;br/&gt;from the pages| pages
{{< /mermaid >}}


## Let Hugo do the rendering {#let-hugo-do-the-rendering}

Instead of copying the toolkit's generated `index.html` into `static/vita/`, I added native Hugo pages for [the CV](/vita/) and [the publications list](/vita/publications/). They use the site's Blowfish layout, responsive table of contents, header and footer. Small Hugo templates render the sections and entries, and scoped CSS handles the details that are specific to a CV.

Those templates and styles initially lived in my website repository. They now live in [`hugo-jsonresume`](https://github.com/zzamboni/hugo-jsonresume), a reusable Hugo Module. The presentation code is deliberately separated from the public URL: my site's pages select the module's `jsonresume` type and the `cv` or `publications` layout, while the data snapshots live under `data/jsonresume/`. The module does not impose a `/vita/` route.

One pleasant benefit is that the CV no longer needs to pretend to be a different website. The same navigation and overall look that surround my posts now surround the CV as well.


## A module instead of another copy of the templates {#a-module-instead-of-another-copy-of-the-templates}

Once the integration worked, the renderer no longer needed anything specific to my website. I extracted it into [`hugo-jsonresume`](https://github.com/zzamboni/hugo-jsonresume) so another Blowfish site can use it without copying templates and CSS from mine.

It is a **Blowfish-specific Hugo Module**, not a standalone theme. It uses the host site's existing Blowfish installation and does not depend on Eventide or run `resume-toolkit` during a Hugo build. The host owns the content pages, JSON data, images, and downloadable files; the module supplies the rendering.

For a site already using Blowfish and initialized for Hugo Modules, installation means adding an import to `config/_default/module.toml`, alongside any existing imports and mounts:

```toml
[[imports]]
path = "github.com/zzamboni/hugo-jsonresume"
```

Then resolve a reviewed commit and commit the resulting `go.mod` and `go.sum`:

```elvish
hugo mod get github.com/zzamboni/hugo-jsonresume@COMMIT_SHA
```

`COMMIT_SHA` is a placeholder for the revision to use. Pinning it keeps builds reproducible; updating the renderer is a separate decision from refreshing the CV data.

A page such as `content/cv/_index.md` selects the renderer through its front matter:

```toml
+++
title = "Curriculum Vitae"
type = "jsonresume"
layout = "cv"
+++
```

The default inputs are `data/jsonresume/resume.json` and, optionally, `data/jsonresume/publications.json`. The latter is normalized JSON from the publications pipeline, not raw BibTeX. The [README](https://github.com/zzamboni/hugo-jsonresume#content-and-data) documents the publications child page and configuration options.

There is also a synthetic `exampleSite/` with no personal data, which doubles as a development fixture. From the module repository's root, clone the tested Blowfish version once, then start the example:

```elvish
git clone --depth 1 --branch v3.8.0 https://github.com/nunocoracao/blowfish.git exampleSite/themes/blowfish
hugo server --source exampleSite
```

The CV appears at `http://localhost:1313/cv/`. The example points back to the local module checkout, so it is useful for trying template and style changes before bringing them into my website.


## The bibliography was the interesting part {#the-bibliography-was-the-interesting-part}

The CV itself was relatively straightforward because JSON Resume is already structured data. Publications were more complicated. Their source is BibTeX, including LaTeX commands and braces that should not appear literally on a web page. I also wanted to keep the established grouping of books, papers, presentations, patents, and other work.

Initially, the Hugo page consumed an independently generated JSON snapshot, but some LaTeX markup leaked through. The right fix was not to teach Hugo how to parse BibTeX. I added a JSON export to `resume-toolkit`'s existing publications pipeline so the HTML and JSON outputs share the same normalization, selection, ordering, and section titles. That output includes data such as properly formatted titles and the links for the PDF and aggregated BibTeX downloads.

There is a useful boundary here: **resume-toolkit knows about BibTeX; Hugo knows about HTML pages**. Neither has to impersonate the other.


## Little details that matter {#little-details-that-matter}

As usual, most of the remaining work was in the details. Relative PDF and BibTeX links needed to resolve under `/vita/publications/`, not under `/vita/`. The CV has special note entries such as “Full list online” and “See full list on Credly,” whose titles are already links; treating them like ordinary entries produced redundant “view” links. We also adjusted the reusable templates to show affiliations and publishers and to avoid introducing a second HTML `main` landmark inside the site's existing one. Research reports now show the type together with the report number, such as “Research Report RZ 3609,” and metadata separators only appear between populated fields.

I also wanted certain navigation links to appear in the standalone Eventide version but not inside Hugo, where the site's navigation already provides them. A small, renderer-independent `role` field on the link, combined with Hugo's `excludeLinkRoles` setting, solved that without forcing website-specific behavior into the toolkit.


## Where things stand {#where-things-stand}

The native CV and publications pages are now in the site's main branch, while the PDFs and BibTeX downloads keep their established URLs. I'm pleased with the result not just because it looks more integrated, but because the underlying pieces remain separately useful: `resume-toolkit` produces the documents and normalized data, Eventide provides the standalone HTML presentation, and `hugo-jsonresume` brings the same data into a Blowfish site.

The next improvement is to make synchronization less manual. At the moment, updating the website involves generating the files from `zzamboni/vita` and copying the relevant JSON, PDFs, BibTeX, and images to the Hugo repository. I plan to turn that into a manually triggered GitHub workflow that proposes a pull request rather than deploying automatically.

It's a small architectural victory: **one source of truth, multiple outputs, and no need to rebuild the entire publishing system just to change how one page looks**.
