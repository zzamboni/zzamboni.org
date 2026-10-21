+++
title = "Drafts, previews, and fewer Netlify builds"
author = ["Diego Zamboni"]
summary = "How I separate content drafts from site experiments, preview drafts on demand, and avoid rebuilding my Hugo site when there is nothing new to publish."
date = 2026-10-21T12:01:00+02:00
tags = ["blogging", "hugo", "netlify", "automation", "howto"]
draft = true
toc = true
+++

<!-- Markdown preview exported from Org with Pandoc; edit the Org source. -->

Making it easier to post to my blog had an unexpected side effect: I started giving Netlify more work. A quick save, a generated summary, a fetched icon, a small correction---each could lead to another build. With production, draft, and staging sites, those little changes add up.

I wanted to keep the convenience of Git-based deployment while being more selective about the work it triggers. The result combines three fairly ordinary ideas: distinguish drafts from experiments, request draft previews when I need them, and preserve Hugo's generated resources between builds.

## Drafts belong with the content

I keep unfinished articles on `main`, marked as drafts. That means they share the real site's content history and can be edited through the same tools. Production excludes drafts; publishing an article means changing its state, not moving it from an experimental branch.

For Org posts, I use a `DRAFT` heading and let `ox-hugo` generate `draft = true` in the exported front matter. I do not also add a custom `draft` field: doing both can produce a duplicate TOML key. I can use an `EXPORT_DATE` property to give an unfinished article a useful place in the draft listing.

`staging` has a different job. I use it for changes to the site itself, such as a layout experiment or an adjustment to the publishing tools. Those changes get reviewed before I bring them to `main`.

## Preview when I need to preview

For local work, `mise run serve-drafts` is the quickest way to see unfinished articles. For checking from my phone, I also have a separate Netlify project that builds `main` with `BUILD_DRAFTS=true`.

I configured that draft project for on-demand builds. In Pages CMS, the **Build draft site** action dispatches a [GitHub workflow](https://github.com/zzamboni/zzamboni.org/blob/main/.github/workflows/build-draft-site.yml), which calls a Netlify build hook. I save my edits first, request the refresh, and wait for the Netlify deployment to finish.

There are two details that are easy to miss. The action builds saved content from `main`, even if I was browsing another branch in the CMS. And a successful GitHub workflow only means Netlify accepted the request; it does not mean the preview has finished deploying.

This is also not the same as stopping builds in Netlify. The draft project keeps builds active so its hook can run them; the ignore check suppresses ordinary automatic builds. A draft flag controls what Hugo publishes, not who can read the repository or a preview URL. I use this for unfinished public writing, not confidential notes.

## Deciding whether a change needs a build

The [ignore script](https://github.com/zzamboni/zzamboni.org/blob/main/scripts/netlify-ignore.mjs) runs before dependency installation. It compares the current commit with Netlify's cached commit, rather than looking only at the most recent commit. That matters when several changes have accumulated since the last build.

Some decisions are straightforward: changes limited to the README, maintenance documentation, or Org source do not affect the rendered site. Hugo reads the Org exports, so the Markdown change is the important part for publishing.

Drafts need more care. My script recognizes a limited set of ordinary Markdown post paths and checks their TOML front matter in both versions. If all relevant changes are drafts being added, edited, or removed, a build that excludes drafts can be skipped. But changing a published post into a draft must still build, so the old public page gets removed. Publishing a draft must build too.

| Change                                       | Production build |
|----------------------------------------------|------------------|
| Documentation only                           | Skip             |
| Eligible draft added or edited               | Skip             |
| Draft changed to published                   | Build            |
| Published post changed to draft              | Build            |
| Image, shared layout, or unrecognized change | Build            |

I deliberately keep the policy conservative. It does not try to prove that every image belongs only to a draft, and it does not cover every content format. Missing history or front matter it cannot confidently interpret causes a build. An unnecessary build is less annoying than a published site that silently stops following its source.

Netlify's ignore command convention is slightly surprising: exit status `0` means skip, and `1` means build. I have tests for that behavior, including publishing and unpublishing transitions. The [build guide](https://github.com/zzamboni/zzamboni.org/blob/main/docs/netlify-builds.md) has the exact rules and overrides.

## Reuse the expensive work

Avoiding builds is only half the story. I also enabled `netlify-plugin-hugo-cache-resources` in `netlify.toml` and pinned the package in `package.json`. It preserves Hugo's generated `resources/` directory between builds, including processed images.

In a small draft-site benchmark recorded in my build notes, the median Hugo step dropped from 12.9 to 3.9 seconds, and the total build process from 39.3 to 31.4 seconds. Those were repeated builds of unchanged content after warming the cache. A batch of new photos will still need processing, so I would not treat those numbers as a promise for every deployment.

This cache is also separate from browser or CDN caching: it helps produce the site, rather than changing how visitors receive it. I keep the configuration and the measurements in the same build guide so I can revisit the assumptions later.

## Less work between an edit and a page

The result is a workflow I can mostly forget about. I save drafts without rebuilding everything, request a remote preview when I want one, and let published-content changes trigger the normal deployment. Local previews still handle most of the iteration.

The implementation is specific to my repository, especially the paths that are safe to ignore. If you adapt it, start with your own content and build dependencies. The useful idea is to decide what actually changes the published site, then make that decision explicit enough to test.
