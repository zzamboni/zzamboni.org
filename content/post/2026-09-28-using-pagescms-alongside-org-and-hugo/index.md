+++
title = "Using Pages CMS alongside Org mode and Hugo"
author = ["Diego Zamboni"]
summary = "How I added a lightweight writing path to my Org-mode blog, and the small configuration choices that make Pages CMS, Hugo, GitHub Actions and Netlify work together."
date = 2026-09-29T13:02:00+02:00
tags = ["blogging", "hugo", "pagescms", "howto"]
draft = true
creator = "Emacs 30.2 (Org mode 9.7.39 + ox-hugo)"
draft = true
toc = true
+++

My main blogging setup is still Emacs, Org mode and `ox-hugo`. I like having the source in one Org file, and I have no plans to give that up for longer posts. But a quick note or link is a different kind of writing. Over time, I have realized that for quick posts, friction matters a lot more than for longer ones. If I have to open my laptop, find the right heading, export, preview, commit and push, I might never write it down.

I wanted a low-friction path from an idea on my phone to a post in the same Hugo site. [Pages CMS](https://pagescms.org/) edits files in my GitHub repository, so it fits the existing Hugo and Netlify pipeline without introducing a new content database. The standard installation was uneventful; the interesting part was making this second authoring path coexist with the first one. In this post I focus on the decisions and the relevant pieces of [my configuration](https://github.com/zzamboni/zzamboni.org).


## Two authoring paths, one Hugo section {#two-authoring-paths-one-hugo-section}

The Org file `content-org/zzamboni.org` remains the source for my longer articles; `ox-hugo` exports those to `content/post/`. Pages CMS writes its own Markdown files under `content-pagescms/`. A Hugo module mount makes those files appear in the same `content/post` section at build time. I added the following to my [module.toml](https://github.com/zzamboni/zzamboni.org/blob/main/config/_default/module.toml) Hugo configuration file:

```toml
[[mounts]]
source = "content"
target = "content"

[[mounts]]
source = "content-pagescms"
target = "content/post"
```

This keeps ownership clear. If a post came from Org, I edit the Org source, not just its generated Markdown. If it came from Pages CMS, its Markdown file is the source. Hugo and Blowfish see both as ordinary posts.

In `.pages.yml`, I use `format: toml-frontmatter` to match the existing posts, and a dated, title-based filename so that the repository remains understandable outside the CMS:

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

  - name: externalUrl
    label: External link
    type: string

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


## The date is local time, and I mean it {#the-date-is-local-time-and-i-mean-it}

The least obvious setting is the date format:

```yaml
      - name: date
        type: date
        required: true
        options:
          time: true
          format: "yyyy-MM-dd'T'HH:mm:ss.SSS"
```

There is deliberately no `Z` or timezone offset. The timestamp is a Zürich wall-clock time, and Hugo's `timeZone` is set to `Europe/Zurich`. I arrived at this after Pages CMS wrote a local clock time with a `Z` suffix, which made Hugo interpret it as UTC and sometimes hide a just-created post as a future post. I wrote up [the bug and the tradeoff in more detail](/post/2026-09-26-pages-cms-hugo-timezones/) separately.

This is a pragmatic convention for a personal site with one expected timezone. It would need revisiting if I began editing across timezones or with collaborators. The small Netlify function behind my iOS link-sharing shortcut follows the same rule: it converts incoming timestamps to Zürich local time before storing them without an offset.


## Link posts still belong in the archive {#link-posts-still-belong-in-the-archive}

For quick links, a Pages CMS post can have an `externalUrl` field. The article list sends the title directly to the external site and gives link posts their own compact styling. The local page remains available for my commentary and as an archive, with a visible callout showing the full destination URL. I have created an iOS Share Sheet shortcut (topic for a future post!) to create one of these posts through a Netlify function, but I can also edit it in Pages CMS afterward.


## Help with summaries, review for images {#help-with-summaries-review-for-images}

If I leave the summary blank on a Pages CMS post, a GitHub Actions workflow generates a short one and commits it back to the file. A summary I have written myself is left alone. I also gave machine-made commits an `auto:` prefix, so I can filter them out while reviewing changes between `staging` and `main`.

Images have a different approval path. In the entry editor I added a **Generate image** action:

```yaml
    actions:
      - name: generate-image
        label: Generate image
        scope: entry
        workflow: generate-feature-image.yml
        ref: current
```

After I save the post, the button dispatches the workflow on the branch I am editing. The dialog also offers extra artistic direction and a checkbox to replace an existing image. The workflow reads the saved Markdown, creates a visual brief, generates a landscape WebP under `assets/img/generated/`, and sets `featureimage` to the corresponding `img/generated/...webp` path. Keeping the image in Hugo's `assets/` pipeline matters for Blowfish's resource lookup. For an Org-authored post, the same workflow can be run manually and updates the matching Org metadata as well.

The image workflow opens a pull request instead of merging its result. I can inspect the image and the Netlify deploy preview before accepting it. That little review step is especially useful for images: even an attractive result can be wrong for the post.


## The useful boundary {#the-useful-boundary}

The two writing paths now have distinct jobs. Org mode is where I develop a deeper article; Pages CMS is where I can capture and edit a short post without turning it into a laptop project. Both still end up as files in Git and pages built by Hugo. The configuration is a collection of small choices, but together they remove just enough friction that a quick idea has a reasonable chance of becoming an actual post.
