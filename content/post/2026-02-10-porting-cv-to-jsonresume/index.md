+++
title = "Porting my CV from Org+LaTeX to JSON Resume"
author = ["Diego Zamboni"]
summary = "How I moved my CV source of truth from Org mode + LaTeX to JSON Resume, and built a pipeline that exports both my CV and publications to HTML and PDF."
date = 2026-02-11T13:21:00+01:00
tags = ["jsonresume", "orgmode", "latex", "cv"]
draft = false
creator = "Emacs 30.2 (Org mode 9.7.39 + ox-hugo)"
featureimage = "img/tram-zurich.jpg"
toc = true
+++

I have wished for a long time to have separation between my CV contents and layout. After maintaining it directly in LaTeX for a while, I switched years ago to org-mode with LaTeX as the main export target. It worked and it enforced a certain degree of separation (most of the "visual" decisions were left up to the LaTeX exporter, with the org-mode file focusing on the contents), but it was fragile: too many custom LaTeX bits, too much hand-editing, and a pipeline that was hard to reuse elsewhere. It was also impossible to produce a nice HTML version from it. In this post I'll document how I switched the source of truth to JSON Resume and built a custom pipeline that outputs **both** my CV and my publications in HTML and PDF. I'm very happy with the result, which you can find in this same website: [my full CV](http://localhost:1313/vita/).

This post is a quick walk-through of the steps, the trade-offs, and the pieces I ended up keeping. This was a months-long side project with many detours, so this post is necessarily lacking in detail, but I hope it provides you with a good overview. The end result is in my [vita](https://gitlab.com/zzamboni/vita) repo in GitLab, so feel free to use it as a starting point.


## Step 0: JSONresume, YAMLresume, RenderCV, oh my {#step-0-jsonresume-yamlresume-rendercv-oh-my}

I did a quick survey of the “semantic resume” ecosystem before committing. There are several options that are all pretty good and popular: [JSON Resume](https://jsonresume.org/), [YAML Resume](https://yamlresume.dev/), [RenderCV](https://rendercv.com/), and a few smaller variants. I picked JSON Resume mainly because the schema feels mature and stable, it is flexible enough for the kinds of entries I keep, and it has a large ecosystem of themes, validators, and exporters. The openness angle also mattered to me. YAML Resume and RenderCV are open, but both are tied to commercial products and workflows, which made me worry about drift or lock-in over time. JSON Resume felt like the most neutral, lowest‑friction baseline: I can keep the data portable, and still build my own pipeline around it without depending on any one vendor’s tooling.


## Step 1: Convert Org + LaTeX to JSON Resume {#step-1-convert-org-plus-latex-to-json-resume}

The first task was simply translating the structure. Org-mode let me be loose; JSON Resume forces me to be explicit, which is both a blessing and a constraint. I built a first cut of `zamboni-vita.json` by using ChatGPT to map headings to JSON Resume sections and then iterating until the HTML output looked reasonable. Early on I chose the [even](https://github.com/rbardini/jsonresume-theme-even) JSONresume theme. I like its' cleanliness and nice structure. However, I added many custom features to it, as you'll see below.

Key lessons:

-   Keep the JSON **flat and normalized**. I removed most of the presentation-specific markup and kept only semantic data. The only concession is to include Markdown in many of the JSONresume fields, to allow for some formatting and links.
-   Convert lists and sublists into fields instead of raw text. This makes them easier to render in multiple formats later.
-   Store links, dates, and IDs consistently (I ended up standardizing on ISO dates and stable IDs for publications).


## Step 2: Build the publications pipeline {#step-2-build-the-publications-pipeline}

The CV is one thing. My publications are another: they were already in BibTeX, and I wanted a separate publications page **and** a PDF. I kept the BibTeX source, and built a small pipeline around it:

-   [`scripts/build_publications.py`](https://gitlab.com/zzamboni/vita/-/blob/main/scripts/build_publications.py) reads my BibTeX sources from [`pubs-src`](https://gitlab.com/zzamboni/vita/-/tree/main/pubs-src).
-   It generates publications HTML with [`templates/publications.html.j2`](https://gitlab.com/zzamboni/vita/-/blob/main/templates/publications.html.j2).
-   It also writes an aggregated [`zamboni-pubs.bib`](http://localhost:1313/vita/publications/zamboni-pubs.bib) for download.

This kept the bibliographic source clean while giving me a consistent, reproducible output.


## Step 3: Tweak jsonresume-theme-even {#step-3-tweak-jsonresume-theme-even}

I used [`jsonresume-theme-even`](https://github.com/rbardini/jsonresume-theme-even) as a base, but I wanted it to look like **my** CV. I install the theme locally in my development environment so I could iterate without publishing anything upstream. I have contributed my changes to the upstream theme, you can find them [separately](https://github.com/rbardini/jsonresume-theme-even/pulls) or in an [aggregated pull request](https://github.com/rbardini/jsonresume-theme-even/pull/33).

These were the main changes I made:

-   support automated grouping of "[Projects](https://docs.jsonresume.org/schema#projects)" entries in JSONresume according to their type. This is how I create the "Research", "Teaching", "Software" and other sections in [my CV](https://zzamboni.org/vita/) while maintaining compatibility with the JSONresume schema.
-   reorder sections to match my preferred layout
-   add icons and lightweight UI polish so the HTML feels like a “document” and not just a web page. For example, I added support for a floating table of contents, for displaying certification badges, for FontAwesome icons (the upstream theme uses [Feather icons](https://feathericons.com/), but they don't have as many icons as FontAwesome), and for floating icons that can link to arbitrary URLs.

This is where JSON Resume started paying off: I could re-render quickly and keep the content stable while iterating on layout.


## Step 4: Export CV and publications to PDF {#step-4-export-cv-and-publications-to-pdf}

For generating the CV PDF I considered converting to RenderCV, but found its schema too limited, existing conversion tools and available themes not to my liking. From the visual point of view I really liked [Awesome CV](https://github.com/posquit0/Awesome-CV), the LaTeX template I was already using for my PDF CV. I decided to implement a custom JSONresume exporter to [Typst](https://typst.app/). I had heard of Typst and this gave me an excuse to start learning it. Furthermore, I found [Brilliant CV](https://typst.app/universe/package/brilliant-cv), a Typst template which replicates Awesome CV. In the end, my new [PDF CV](https://zzamboni.org/vita/zamboni-vita.pdf) looks **very similar** to the [previous one](https://gitlab.com/zzamboni/vita/-/raw/orgmode-cv/build/zamboni-vita/zamboni-vita.pdf?ref_type=heads&inline=true), which is good because I really like the format!

The main component here is the [`scripts/render_typst_cv.py`](https://gitlab.com/zzamboni/vita/-/blob/main/scripts/render_typst_cv.py?ref_type=heads) script, which converts JSON Resume into a self-contained Typst document which uses the `brilliant-cv` template.

For publications I tried to use Typst as well, since it has built-in support for [importing BibTeX files](https://typst.app/docs/reference/model/bibliography/). This worked well with a single bibliography, but I wanted to keep my [publications list](https://zzamboni.org/vita/publications/) structured by type. In the end I decided to stay with LaTeX and used a small wrapper so the output matches the HTML:

-   [`pubs-src/zamboni-pubs.tex`](https://gitlab.com/zzamboni/vita/-/blob/main/pubs-src/zamboni-pubs.tex) is the source for the publications PDF. Note that this still uses the old AwesomeCV class, so my publications list still has the same style as my new CV.
-   A [`tectonic`](https://tectonic-typesetting.github.io/) build step produces [the PDF version of my publications list](https://zzamboni.org/vita/publications/zamboni-pubs.pdf), with the same structure (and even order of entries) of the [online version](https://zzamboni.org/vita/publications/).

The output of both pipelines lands under `build/zamboni-jsonresume/{dev,prod}/vita/`, which mirrors the final website structure.


## Step 5: Wire it all together {#step-5-wire-it-all-together}

The last bit was making the whole thing repeatable. I added a few `mise` tasks so I can rebuild everything quickly:

-   `mise run build-dev` for local HTML + PDFs (the key difference is that the dev HTML outputs include some code for auto-reloading, and embedded debug information, which is omitted in the prod version)
-   `mise run build-prod` for the production outputs
-   `mise run deploy-prod` to sync the final output to my website

This was the ultimate payoff: JSON/BibTeX are the source of truth, and the rest is mechanical.

To further automate my development environment, I used the opportunity to learn about [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers), which make it easy to edit files locally, while running compilation/debug steps inside a container with all the necessary tools:

-   [devcontainer.json](https://gitlab.com/zzamboni/vita/-/blob/main/.devcontainer/devcontainer.json?ref_type=heads) defines the tools and environment that will be installed in the container. This way I can have all the necessary tools in a consistent and repeatable way, without polluting or depending on the setup of my local machine.
-   A few additional mise tasks help me interact with the devcontainer:
    -   `mise dev-up` to create the container and run the development loop inside it.
    -   `mise dev-rebuild-up` to force creation of a new container before startup.
    -   `mise dev-bash` to open a shell session in the running container.


## Takeaways {#takeaways}

-   Pick a semantic source format early. JSON Resume makes it easy to reuse the data.
-   Separate “content” from “layout” aggressively. Theme tweaks are now safe and quick.
-   Keep publications as a distinct pipeline. They have different constraints and I want the flexibility.

If you are thinking of a similar conversion, start with the data model and only then worry about the rendering. That order made the whole project go faster than I expected.

I was also impressed by how much AI tools helped me during the process. I used ChatGPT Codex and Claude Code for much of the process, and they helped me quickly create and fine tune the scripts, and also to understand and modify the JSONresume theme.
