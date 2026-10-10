+++
title = "Posting links and photos from my phone with Netlify and iOS Shortcuts"
author = ["Diego Zamboni"]
summary = "How I turned shared links and photos into Hugo posts with iOS Shortcuts, Netlify Functions, GitHub, and a small amount of custom Blowfish styling."
date = 2026-10-07T22:34:00+02:00
tags = ["blogging", "hugo", "pagescms", "netlify", "shortcuts", "howto"]
draft = true
creator = "Emacs 30.2 (Org mode 9.7.39 + ox-hugo)"
toc = true
featureimage = "img/generated/2026-10-07-linkblog-and-photoblog-with-netlify-and-shortcuts.webp"
+++

In [my previous post]({{< relref "2026-09-28-using-pagescms-alongside-org-and-hugo" >}}), I described how I set up Pages CMS as a quick editing path alongside Org mode. But for the two things I share most often from my phone—a link I want to remember and a few photos I want to show—even opening an editor feels like an extra step. I wanted to use the iOS Share Sheet, add a title or a sentence if I felt like it, and get a draft into the same Git-backed site.

The result is two [iOS Shortcuts](https://support.apple.com/guide/shortcuts/welcome/ios) and two small [Netlify Functions](https://docs.netlify.com/build/functions/overview/). The Shortcuts collect input on the phone; the functions turn it into files in GitHub; Hugo and Blowfish render the files like any other post. The Shortcuts are available here: [Post Link](https://www.icloud.com/shortcuts/cad708218dd348598a43ba394e7f75b5) and [Post Photo](https://www.icloud.com/shortcuts/437c4651085e42da9b465c3f0d2857da). You need to configure your own endpoint and secret before using them.


## One publishing pipeline, different entry points {#one-publishing-pipeline-different-entry-points}

My longer articles still start in `content-org/zzamboni.org` and are exported by `ox-hugo` to `content/post/`. Shorter posts start in Pages CMS or in a Shortcut. The [Hugo mounts](https://github.com/zzamboni/zzamboni.org/blob/main/config/_default/module.toml) combine `content-pagescms/` and `content-photos/` with `content/post/` at build time. All of them show up in the same blog, while the source of each post remains clear. I can later edit a link in Pages CMS, or edit a photo post and its image list in the [Photos collection](https://github.com/zzamboni/zzamboni.org/blob/main/.pages.yml). An Org post still gets edited in Org.

The functions use a bearer secret to authorize a request and a GitHub token to write the result. I keep those credentials in the Netlify environment, rather than in the repository. Each function returns the new post's title and an edit URL, so the Shortcut can offer to open the entry in Pages CMS after posting. The request can ask for a draft; both functions default to draft unless I explicitly send `draft: false`. For a draft, my separate draft Netlify site gives me a place to check the result before publishing.


## A link is a post, but its title should take you to the link {#a-link-is-a-post-but-its-title-should-take-you-to-the-link}

The [linkblog function](https://github.com/zzamboni/zzamboni.org/blob/main/netlify/functions/linkblog.mjs) accepts a URL, optional title and commentary, date, tags, and draft setting. If I leave the title empty, it tries the linked page's metadata and falls back to the hostname. It writes a small TOML-front-matter Markdown file in `content-pagescms/`, including `externalUrl` and the `zznippets` tag. The supplied timestamp is normalized to Zürich local time, following the Pages CMS date convention I described in the previous post.

On a list page, a link title goes straight to `externalUrl`. I prefer that behavior when scanning links: one tap takes me to the thing I saved. There is still a local post page for my commentary and the archive. On that page, a [callout](https://github.com/zzamboni/zzamboni.org/blob/main/layouts/partials/extend-single-header.html) displays the full external URL near the top, so the destination is visible there too.

I wanted link entries to look like links rather than tiny ordinary articles. The [list partial](https://github.com/zzamboni/zzamboni.org/blob/main/layouts/partials/extend-article-link.html) shows a Link badge, domain, and tags; [custom CSS](https://github.com/zzamboni/zzamboni.org/blob/main/assets/css/custom.css) gives the entry a tinted background, left border, and compact layout. Instead of a large feature image, it gets a small site icon aligned near the top. A [GitHub Actions workflow](https://github.com/zzamboni/zzamboni.org/blob/main/.github/workflows/fetch-linkblog-favicons.yml) fetches and caches favicons in the repository; if no icon is available, the template shows a globe. Hugo does not need to request third-party icons when a visitor opens the page.

The post body can be just a line or two of my own commentary. When I leave its summary blank, the [summary workflow](https://github.com/zzamboni/zzamboni.org/blob/main/.github/workflows/generate-pagescms-summary.yml) may fill it in later. The Shortcut is for capturing the link quickly; Pages CMS remains useful for polishing the entry afterward.


## Photos are the content, not an attachment to it {#photos-are-the-content-not-an-attachment-to-it}

The [photo Shortcut](https://www.icloud.com/shortcuts/437c4651085e42da9b465c3f0d2857da) takes shared images, resizes and encodes them for the request, and asks for a title and optional commentary. The [photoblog function](https://github.com/zzamboni/zzamboni.org/blob/main/netlify/functions/photoblog.mjs) validates the uploaded images and creates a post bundle under `content-photos/` together with image files under `static/img/photos/`. It writes a `photos` list of image paths into the post's front matter and adds the `photos` tag. The post and its images land in one Git commit, avoiding a half-created gallery if the upload fails partway through.

The images live in a central media directory because I also wanted to manage them through Pages CMS's image field. The Markdown post is still a Hugo leaf bundle (`index.md`), but its image list points to those separately stored media files. The [Photos menu item](https://github.com/zzamboni/zzamboni.org/blob/main/config/_default/menus.en.toml) goes to `/tags/photos/`; I did not need a separate Hugo section to collect them. The short commentary, when present, appears above the gallery where a visitor will see it before scrolling through the pictures.

Blowfish supplies the gallery styling, while my [gallery partial](https://github.com/zzamboni/zzamboni.org/blob/main/layouts/partials/photo-gallery.html) reads the `photos` front matter and renders thumbnails linked to the original images. For viewing them, I use [GLightbox](https://github.com/biati-digital/glightbox), loaded only on pages with photos by [the head extension](https://github.com/zzamboni/zzamboni.org/blob/main/layouts/partials/extend-head-uncached.html). The small [integration script](https://github.com/zzamboni/zzamboni.org/blob/main/assets/js/photo-lightbox.js) adds next/previous navigation, touch and keyboard controls, a photo counter, and focus handling. That matters more than it sounds: opening and closing every image separately gets old quickly, especially on a phone. [A little CSS](https://github.com/zzamboni/zzamboni.org/blob/main/assets/css/photo-lightbox.css) keeps the controls and counter legible on small screens.


## What this setup buys me {#what-this-setup-buys-me}

These are deliberately small entry points into an existing publishing system. A link or photo can start in the Share Sheet, become a draft in GitHub, be reviewed on Netlify, and be edited in Pages CMS without changing how I write long articles. The visible site still consists of static Hugo pages and images.

There are tradeoffs. Uploading photos as JSON means resizing them on the phone, and storing media in Git is a conscious choice for this personal site. The function endpoints also need a secret and the correct target branch configured in Netlify; in particular, the photoblog function requires `PHOTOBLOG_BRANCH` so a staging upload cannot silently write to `main`. For me, the convenience of a one-tap capture path and a reviewable Git history has been worth that bit of plumbing.

If you want to adapt this, the [link](https://github.com/zzamboni/zzamboni.org/blob/main/netlify/functions/linkblog.mjs) and [photo](https://github.com/zzamboni/zzamboni.org/blob/main/netlify/functions/photoblog.mjs) functions, [Pages CMS configuration](https://github.com/zzamboni/zzamboni.org/blob/main/.pages.yml), and the two Shortcuts linked above are the best starting points. I expect the details to keep evolving, but the shape of the workflow feels right: capture on the device I have in hand, and keep the files where the rest of my site already lives.
