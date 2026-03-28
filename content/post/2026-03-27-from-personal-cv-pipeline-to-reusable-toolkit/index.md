+++
title = "resume-toolkit: from personal CV pipeline to reusable toolkit"
author = ["Diego Zamboni"]
summary = "How my CV pipeline escaped my own resume repo and became a reusable tool, plus the evolution of the HTML theme into its own fork."
date = 2026-03-28T01:38:00+01:00
tags = ["jsonresume", "typst", "tools"]
draft = false
creator = "Emacs 30.2 (Org mode 9.7.39 + ox-hugo)"
featureimage = "img/tram-zurich.jpg"
toc = true
+++

{{< note >}}
If you just want a nice HTML and PDF rendering of your JSON Resume file, head here: <https://github.com/zzamboni/resume-toolkit>. If you are interested in more details, keep on reading!
{{< /note >}}

A few weeks ago I wrote about [porting my CV from Org+LaTeX to JSON Resume]({{< relref "2026-02-10-porting-cv-to-jsonresume" >}}). At the time, I had reached a point where my data lived in a much saner format, I could produce HTML and PDF output, and I had a publications pipeline that more or less did what I needed. It was already a big improvement over the old setup.

But there was still an obvious problem: it was **my** pipeline.

It lived inside my CV repository, it knew too much about my files and my directory structure, and although I had tried to keep things generic, the whole thing still felt like a personal construction project that happened to work. Reusing it would have required copying half the repository and then carefully undoing all the places where I had hardcoded my own name, information and assumptions.

That bothered me more than I expected.

If I was going to invest this much effort in moving to a semantic CV format, then I wanted the result to be genuinely reusable. Not “reusable if you don’t mind editing five scripts and reading my mind,” but actually reusable by someone else, or by future me after I had forgotten how it all fit together.

So the next phase of the project was to separate the tool from the data, and to turn the whole thing into something I could invoke on any JSON Resume file and get sensible output.


## Extracting the toolkit from my CV repo {#extracting-the-toolkit-from-my-cv-repo}

The first big step was to pull the build pipeline out of my CV repository and make it stand on its own. That sounds obvious in retrospect, but in practice it meant a lot of clean up.

I had to make paths configurable. I had to stop assuming that my publications always lived in a specific directory. I had to make the scripts work no matter where they were invoked from. I had to teach them how to find local assets, profile pictures, logos, and BibTeX files in a way that would make sense for arbitrary input files, not just for my own layout.

For this I relied heavily on [ChatGPT Codex](https://chatgpt.com/codex), which acted as a competent programmer, implementing my specifications. I was able to give instructions of what I wanted to do, and guide it step by step through making the necessary changes in the code. I am very impressed by its abilities.

The result is what is now [`resume-toolkit`](https://github.com/zzamboni/resume-toolkit): a standalone project that takes a JSON Resume file, optional BibTeX sources, and produces:

-   an HTML CV
-   a PDF CV
-   if BibTeX files are given:
    -   a standalone HTML publications page
    -   a standalone PDF publications list
    -   an aggregated BibTeX file for download

The important change was not that the scripts moved to another repository. The important change was that the **boundary** became cleaner: the toolkit is now the build system, while my CV repository is just content plus a little configuration.

That sounds mundane, but it changed the whole feel of the project.


## Making it reusable enough to trust {#making-it-reusable-enough-to-trust}

Once the pipeline lived on its own, the next challenge was making it robust enough that I could point it at other people’s JSON Resume files and not have it immediately fall apart. I tested it by grabbing random JSON Resume files from [the JSON Resume Registry](https://registry.jsonresume.org/explore) and testing the toolkit with them. This helped me identify several bugs and hidden assumptions that got fixed and resulted in several new useful features.

This turned out to be a very good forcing function.

As soon as I started trying random JSON Resume files “from the wild”, all the edge cases came out:

-   entries using `company` instead of `name` in work history
-   missing locations
-   missing profile images
-   image URLs with no filename extension
-   relative links that worked in HTML but not in downloaded PDFs
-   optional sections that were present in some resumes and absent in others
-   data that was valid enough for one renderer but broke another

Fixing those cases made the toolkit much better. In many ways, this was the point where it stopped being “my CV exporter” and started becoming a general-purpose tool.

I also wrapped the whole thing in a Docker image and a small `build-resume.sh` helper so the user-facing entry point became dead simple:

```sh
build-resume.sh resume.json
```

That script grew a few useful features over time: watch mode, serve mode, optional pulling of a newer image, automatic port selection for multiple local preview sessions, and so on. None of those are particularly glamorous, but they make the difference between “interesting code” and “something I actually enjoy using.”


## Pulling more configuration into the JSON {#pulling-more-configuration-into-the-json}

One thing I wanted from the start was to keep the source of truth in the data, not in the scripts.

The initial version still had too many decisions hidden in code: link definitions, publications behavior, section titles, PDF layout knobs, and little bits of rendering policy. It worked, but it was not very transparent.

So I kept moving configuration into the JSON file, mostly under the `meta` section. I created three new subsections in addition to the existing `meta.themeOptions` supported by the Even theme:

-   `meta.site` for defining the URL of the site where the resume will be published (to expand relative to full links in PDF rendering);
-   `meta.pdfthemeOptions` for configuring the PDF rendering;
-   `meta.publicationsOptions` for configuring the behavior of the publications section and the standalone publications page.

This turned out to be one of the nicest improvements in the whole project. Instead of editing Python or shell code, I can now control a lot of behavior directly from the resume data:

-   floating links in the HTML CV and publications page
-   publications grouping and section titles
-   whether publications are inlined in the PDF CV
-   whether inline publications use the full list or a filtered subset
-   bibliography filtering by explicit BibTeX entries or by keywords
-   PDF layout options for the `brilliant-cv` Typst theme
-   visible printable URLs in the PDF
-   footer URLs for both the CV and the publications PDF
-   base site URL handling for converting relative links into absolute PDF links

The more I did this, the more the system started feeling like a **toolkit** rather than a collection of scripts.

It also made the behavior easier to reason about. If something is controlled by the JSON, it is much easier to inspect, version, and reuse than if it lives in a Python function somewhere in the middle of the pipeline.


## Publications were their own little rabbit hole {#publications-were-their-own-little-rabbit-hole}

The publications side of the project kept evolving too.

I already had my publications in BibTeX, and I wanted to preserve that as the source of truth. At first the pipeline simply aggregated the BibTeX and rendered everything. But once I started using it more seriously, I wanted more control.

In particular, I wanted to distinguish between:

-   the **full** standalone publications list
-   a **selected** subset of publications shown inline in the CV

That led to support for filtering by BibTeX entry key and by BibTeX keywords, and to better separation between the standalone publications outputs and the inline bibliography used in the PDF CV.

I also added a command to write the selected publications back into the JSON Resume `publications` section, so the HTML CV can show the same curated subset without needing special support from the HTML theme.

This part was more fiddly than I expected, mostly because BibTeX is both wonderfully flexible and slightly chaotic. But in the end it gave me a setup I really like: BibTeX remains the canonical source, while the JSON Resume gets just enough derived data to render nicely everywhere.


## The HTML theme stopped being “just a few tweaks” {#the-html-theme-stopped-being-just-a-few-tweaks}

In my previous post I mentioned that I had started from [`jsonresume-theme-even`](https://github.com/rbardini/jsonresume-theme-even). That is still true. It was a great base and it gave me a clean starting point.

I started making some tweaks, but over time, the number of changes kept growing. Some were small visual touches. Some were structural changes. Some were features I wanted for my own CV that turned out to be generally useful:

-   grouped project sections
-   floating links
-   Font Awesome icon support
-   certification badges
-   better note-style entries
-   more configurable colors and layout behavior
-   support for my publications page conventions
-   lots of little fixes and polish

At some point I had to admit the obvious: this was no longer a small customization layer on top of the original theme.

I had been maintaining my changes as a large pull request against the upstream theme, but realistically they are too extensive, too opinionated, and too tightly coupled to the direction I want for this project. I don’t think that is a bad thing. It just means the project has its own identity now.

So I finally split it out as its own fork: [jsonresume-theme-eventide](https://github.com/zzamboni/jsonresume-theme-eventide).

I wanted a name that still nodded to the original `even` theme without implying “version 2” or “better” or anything like that. `eventide` seemed right: related, but clearly its own thing.


## What I like about the result {#what-i-like-about-the-result}

What I like most now is not any individual feature, but the shape of the system.

-   My CV repository is only content.
-   The toolkit repository is mostly machinery.
-   The theme repository is mostly HTML presentation.

That separation is not perfect, but it is much better than where I started.

It means I can evolve the pipeline without touching my CV data. I can evolve the theme without digging through the build scripts. I can test the toolkit with other resumes and make it more robust. And I can publish the whole thing as something that other people might actually reuse, instead of as a pile of personal glue code.

That was the real goal all along.


## Takeaways {#takeaways}

A few things I learned from this second phase:

-   extracting a personal tool into a reusable one is mostly about removing assumptions
-   testing with other people’s data is one of the fastest ways to harden your own code
-   pushing configuration into the data model makes the system easier to understand
-   once a heavily customized theme starts developing its own direction, it is better to acknowledge that honestly and fork it
-   small workflow improvements matter a lot when you run the same build loop dozens of times

I’m pretty happy with where `resume-toolkit` is now. It started as a side effect of moving my CV away from Org and LaTeX, but it has turned into a nice standalone project in its own right.

There is still plenty I could improve, of course. But it now feels like I’m building on top of a tool I trust, instead of constantly patching a one-off pipeline that only I understand.

If you use (or are interested in ) JSON Resume, please give [resume-toolkit](https://github.com/zzamboni/resume-toolkit) and [Eventide](https://github.com/zzamboni/jsonresume-theme-eventide) a try! I would be happy to hear your comments or feedback.
