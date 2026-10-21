# zzamboni.org

[![Netlify Status](https://api.netlify.com/api/v1/badges/e5ae9eeb-01ec-4b37-90ad-2f4b3877a7d6/deploy-status)](https://app.netlify.com/projects/zzamboni/deploys) 
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fzzamboni.org&up_message=zzamboni.org&down_message=zzamboni.org%20(down))](https://zzamboni.org)

This is the source for [zzamboni.org](https://zzamboni.org/), my little corner of the web. I write mostly about technology, security, automation, and whatever else catches my attention. I also share interesting links, post photos, and keep my CV and publications here.

I build the site with [Hugo](https://gohugo.io/) and the [Blowfish](https://blowfish.page/) theme, with a few custom layouts and styles to make it feel like home. [Netlify](https://www.netlify.com/) handles hosting and deployment. GitHub is the source of truth; I mirror the repository to [GitLab](https://gitlab.com/zzamboni/zzamboni.org).

## How I publish

I use a few different paths depending on what I'm posting:

- **Longer articles:** I write in Emacs and Org mode, in `content-org/zzamboni.org`, and export to `content/post/` with [ox-hugo](https://ox-hugo.scripter.co/). I edit the Org source rather than its generated Markdown.
- **Quick posts and links:** I use [Pages CMS](https://pagescms.org/) to edit posts in `content-pagescms/`. For links and photos, I also use iOS Shortcuts that call my Netlify functions, so I can post straight from my phone. Photo posts live in `content-photos/`.
- **Older posts:** I keep these in `content-legacy/`, with their original URLs. The [legacy content guide](docs/legacy-content.md) explains how I maintain them.

Hugo brings these sources together into one site. My [original blogging setup post](https://zzamboni.org/post/my-blogging-setup-with-emacs-org-mode-ox-hugo-hugo-gitlab-and-netlify/) describes how the Org workflow started, although the setup has grown since then.

## CV and publications

I keep my CV data in JSON Resume format and render it as native Hugo pages using my [hugo-jsonresume module](https://github.com/zzamboni/hugo-jsonresume). I also offer PDF and BibTeX downloads. The [CV integration guide](docs/hugo-vita-experiment.md) covers how the data, downloads, and renderer fit together.

## A little automation

I use GitHub Actions to take care of things like filling in missing summaries, fetching link icons, and generating feature images for review. I've documented [feature image generation](docs/feature-image-generation.md), [linkblog favicons](docs/linkblog-favicons.md), and [OpenAI usage reporting](docs/openai-usage.md) separately.

I publish real content, including drafts, on `main`, and use `staging` for experiments. Netlify provides separate production, draft, and staging sites. To keep build minutes under control, I skip unnecessary builds and trigger the draft site on demand; the details are in the [Netlify build guide](docs/netlify-builds.md).

## Working on the site

I use [mise](https://mise.jdx.dev/) to pin the local tools. After cloning the repository, I get a local preview running with:

```sh
git submodule update --init --recursive
mise install
mise run serve
```

I use `mise run serve-drafts` when I want to include drafts. Configuration lives in `config/_default/`, my theme customizations are in `layouts/` and `assets/`, and publishing functions live in `netlify/functions/`.

For maintenance, I keep a [theme and module update guide](scripts/README-theme-updates.md) and [repository guidelines](AGENTS.md). The rest of [docs/](docs/) has more focused notes when I need to dig into a particular part of the setup.
