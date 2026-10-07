+++
title = "Using Pages CMS alongside Org mode and Hugo"
author = ["Diego Zamboni"]
summary = "How I added a lightweight writing path to my Org-mode blog, and the small configuration choices that make Pages CMS, Hugo, GitHub Actions and Netlify work together."
date = 2026-10-06T22:04:00+02:00
tags = ["blogging", "hugo", "pagescms", "howto"]
draft = false
creator = "Emacs 30.2 (Org mode 9.7.39 + ox-hugo)"
toc = true
featureimage = "img/generated/2026-09-28-using-pagescms-alongside-org-and-hugo.webp"
+++

My main blogging setup is with [Emacs, Org mode and `ox-hugo`]({{< relref "2020-12-11-my-blogging-setup-and-workflow" >}}). I like having the source in one Org file, and I have no plans to give that up for longer posts. But a quick note, link or a photo is a different kind of posting. Over time, I have realized that for quick posts, friction matters a lot more than for longer ones. If I have to open my laptop, find the right heading, export, preview, commit and push, I might never write it down.

I wanted a low-friction path from an idea on my phone to a post in my Hugo-powered website. I found [Pages CMS](https://pagescms.org/), which edits files directly in my GitHub repository, so it fits the existing Hugo and Netlify pipeline without introducing a new content source. The [standard Pages CMS installation](https://pagescms.org/docs/quick-start/) was uneventful; the interesting part was making this second authoring path coexist with the first one. In this post I focus on the decisions and the relevant pieces of [my configuration](https://github.com/zzamboni/zzamboni.org).


## Joining multiple directories into a single Hugo section {#joining-multiple-directories-into-a-single-hugo-section}

The Org file `content-org/zzamboni.org` remains the source for my longer articles; `ox-hugo` exports those to `content/post/`. Pages CMS writes its own Markdown files under `content-pagescms/`. I learned that Hugo [module mounts](https://gohugo.io/configuration/module/#mounts) can make multiple directories appear in the same `content/post` section at build time. I added the following to my [module.toml](https://github.com/zzamboni/zzamboni.org/blob/main/config/_default/module.toml) Hugo configuration file:

```toml
[[mounts]]
source = "content"
target = "content"

[[mounts]]
source = "content-pagescms"
target = "content/post"
```

This keeps the content ownership clear: If a post came from Org, I edit the Org source, not just its generated Markdown. If it came from Pages CMS, its Markdown file is the source. Hugo and Blowfish see both as ordinary posts.

In [`.pages.yml`](https://github.com/zzamboni/zzamboni.org/blob/main/.pages.yml), I use `format: toml-frontmatter` to match the existing posts, and a dated, title-based filename to match the filenames I have been using already for exporting from the org-mode file:

```yaml
content:
  - name: posts
    type: collection
    path: content-pagescms
    format: toml-frontmatter
    filename: "{year}-{month}-{day}-{primary}.md"
```

In the `.pages.yml` field configuration I put the title, summary and body near the top of the editor and leave the less frequently changed metadata below. Posts default to draft, so saving a new post does not immediately publish it.

```yaml
fields:
  - name: title
    label: Title
    type: string
    required: true

  - name: summary
    label: Summary
    type: text
    options:
      maxlength: 400

  - name: body
    label: Body
    type: rich-text

  - name: date
    label: Date
    type: date
    required: true
    options:
      time: true
      format: "yyyy-MM-dd'T'HH:mm:ss.SSS"

  - name: tags
    label: Tags
    type: string
    list: true

  - name: draft
    label: Draft
    type: boolean
    default: true

  - name: featureimage
    label: Feature image
    type: string
    default: "img/tram-zurich.jpg"
    hidden: false

  - name: toc
    label: Table of contents
    type: boolean
    default: false
```


## Time zone woes {#time-zone-woes}

The least obvious setting is the date format:

```yaml
      - name: date
        type: date
        required: true
        options:
          time: true
          format: "yyyy-MM-dd'T'HH:mm:ss.SSS"
```

There is deliberately no `Z` or timezone offset. The timestamp is a Zürich wall-clock time, and Hugo's `timeZone` is set to `Europe/Zurich`. This is to work around a bug in which Pages CMS writes the local clock time with a `Z` suffix, which makes Hugo interpret it as UTC and sometimes hide a just-created post as a future post. I wrote about [the bug and the tradeoff in more detail]({{< relref "2026-09-26-pages-cms-hugo-timezones" >}}) separately.

This is a pragmatic convention for a personal site with one expected timezone. It would need revisiting if I began editing across timezones or with collaborators, or when the [PR that fixes this](https://github.com/hunvreus/pagescms/pull/410) gets merged into Pages CMS.


## Help with summaries, review for images {#help-with-summaries-review-for-images}

If I leave the summary blank on a Pages CMS post, a GitHub Actions workflow ([generate-pagescms-summary.yml](https://github.com/zzamboni/zzamboni.org/blob/main/.github/workflows/generate-pagescms-summary.yml)) generates a short one and commits it back to the file. If the post already contains a summary (e.g. one I wrote when posting it), it is left alone. In addition to getting triggered automatically, I can also trigger it with an action button in Pages CMS:

```yaml
actions:
  - name: generate-summary
    label: Generate summary
    scope: entry
    workflow: generate-pagescms-summary.yml
    ref: current
    confirm:
      title: Generate a missing summary?
      message: Uses the saved post or linked article and commits a summary if the summary field is blank. Save your changes first.
      button: Generate summary
```

Another workflow ([generate-feature-image.yml](https://github.com/zzamboni/zzamboni.org/blob/main/.github/workflows/generate-feature-image.yml)) uses AI to generate an image to be used as the thumbnail of a new blog post (I'm not yet convinced that this is a good idea, the images look too "AI generated" for my taste). These are not generated automatically, only on request using an action button:

```yaml
actions:
  - name: generate-image
    label: Generate image
    scope: entry
    workflow: generate-feature-image.yml
    ref: current
```

After I save the post, the button dispatches the workflow on the branch I am editing. The dialog also offers the chance to provide extra artistic direction and a checkbox to replace an existing image. The workflow reads the saved Markdown, creates a visual brief, generates a landscape WebP under `assets/img/generated/`, and sets `featureimage` to the corresponding `img/generated/...webp` path. Keeping the image in Hugo's `assets/` pipeline matters for Blowfish's resource lookup. For an Org-authored post, the same workflow can be run manually and updates the matching Org metadata as well.

The image workflow opens a pull request instead of merging its result. I can inspect the image and the Netlify deploy preview before accepting it. That little review step is especially useful for images: even an attractive result can be wrong for the post.


## The useful boundary {#the-useful-boundary}

The two writing paths now have distinct jobs. Org mode is where I develop a deeper article; Pages CMS is where I can capture and edit a short post without turning it into a laptop project. Both still end up as files in Git and pages built by Hugo. The configuration is a collection of small choices, but together they remove just enough friction that a quick idea has a reasonable chance of becoming an actual post.

In future posts I'll show how I have created link- and photo-specific sections (including custom rendering) of my blog, and matching iOS Shortcuts to easily post them.
