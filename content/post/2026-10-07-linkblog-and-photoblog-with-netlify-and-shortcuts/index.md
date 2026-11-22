+++
title = "Posting links and photos from my phone with Netlify and iOS Shortcuts"
author = ["Diego Zamboni"]
summary = "How I turn shared links and photos into Hugo posts with iOS Shortcuts, Netlify Functions, GitHub, and a small amount of custom Blowfish styling."
date = 2026-10-07T22:34:00+02:00
tags = ["blogging", "hugo", "pagescms", "netlify", "shortcuts", "howto"]
draft = true
creator = "Emacs (Org mode + ox-hugo)"
featureimage = "img/generated/2026-10-07-linkblog-and-photoblog-with-netlify-and-shortcuts.webp"
series = ["My website setup"]
series_order = 6
+++

In [a previous post]({{< relref "2026-09-28-using-pagescms-alongside-org-and-hugo" >}}), I described how I set up Pages CMS as a quicker editing path alongside Org mode. But for two things I most often share from my phone [Links](/tags/linky) and [Photos]({{< relref "photos" >}}), the friction has to be truly minimal: I want to use the iOS Share Sheet to produce a post in my website.

The result is two [iOS Shortcuts](https://support.apple.com/guide/shortcuts/welcome/ios) and two small custom [Netlify Functions](https://docs.netlify.com/build/functions/overview/). The Shortcuts collect input on the phone; the functions turn it into files in GitHub; Hugo and Blowfish render the files like any other post. The Shortcuts are available below. You need to configure your own endpoint and secret before using them.

{{< feature-grid >}}
{{< feature icon="link" title="Post Link" url="https://www.icloud.com/shortcuts/cad708218dd348598a43ba394e7f75b5" label="Get Shortcut" />}}
{{< feature icon="image" title="Post Photos" url="https://www.icloud.com/shortcuts/437c4651085e42da9b465c3f0d2857da" label="Get Shortcut" />}}
{{< /feature-grid >}}


## One publishing pipeline, different entry points {#one-publishing-pipeline-different-entry-points}

My longer articles still live in `content-org/zzamboni.org` and are exported by `ox-hugo` to `content/post/`. Shorter posts start in Pages CMS or in a Shortcut. The [Hugo mounts](https://github.com/zzamboni/zzamboni.org/blob/main/config/_default/module.toml) combine `content-pagescms/` and `content-photos/` with `content/post/` at build time. All of them end up in the same Hugo "post" section, while the source of each post remains clear and separate. For cosmetic reasons, the [Blog]({{< relref "post" >}}) listing excludes photo posts; photos have their own [Photos]({{< relref "photos" >}}) section and a separate column on the homepage. I can later edit both links and photos in Pages CMS (photos have their own [Photos collection](https://github.com/zzamboni/zzamboni.org/blob/main/.pages.yml) to make use of Pages CMS's photo-management capabilities).

{{< figure src="pagescms-collections.png" caption="<span class=\"figure-number\">Figure 1: </span>Pages CMS collections, showing \"Photos\" posts." >}}

The iOS shortcuts interact with two custom  [Netlify functions](https://github.com/zzamboni/zzamboni.org/tree/main/netlify/functions), one for Links and one for Photos. They use a bearer secret to authorize a request and a GitHub token to write the result. I keep those credentials as secrets in the Netlify environment, rather than in the repository. Each function returns the new post's title and an edit URL, so the Shortcut can offer to open the entry in Pages CMS after posting it. Both functions default to creating draft posts, but this can be configured in the shortcuts.

{{< figure src="photo-post-edit-dialog.png" caption="<span class=\"figure-number\">Figure 2: </span>Dialog after posting a photo, offering to edit the post in Pages CMS." >}}


## A link is a post, but its title should take you to the link {#a-link-is-a-post-but-its-title-should-take-you-to-the-link}

The [linkblog function](https://github.com/zzamboni/zzamboni.org/blob/main/netlify/functions/linkblog.mjs) accepts a URL, optional title, commentary and summary, date, tags, and draft setting. If I provide only commentary or only a summary, the function uses it for both the body and the summary; providing both keeps them separate. If I leave the title empty, it tries the linked page's metadata and falls back to the hostname. It writes a small TOML-front-matter Markdown file in `content-pagescms/`, including `externalUrl` and the `linky` tag.

On a Hugo list page (for example [Links](/tags/linky/)), link posts go straight to their `externalUrl` (the linked page). I prefer that behavior when scanning links, since one tap takes me to the thing I saved. There is still a local post page which shows my commentary if any (for example [Pages CMS](/post/pages-cms/)). On that page, a callout displays the full external URL near the top, so the destination is visible there too.

I wanted link entries to be visually distinct from ordinary articles. To this effect, a custom [list partial](https://github.com/zzamboni/zzamboni.org/blob/main/layouts/partials/extend-article-link.html) shows a Link badge, domain, and tags; [custom CSS](https://github.com/zzamboni/zzamboni.org/blob/main/assets/css/custom.css) gives the entry a distinct layout. Instead of a large feature image, it gets a small site icon aligned near the top. A [GitHub Actions workflow](https://github.com/zzamboni/zzamboni.org/blob/main/.github/workflows/enrich-pagescms-posts.yml) automatically fetches and caches favicons in the repository; if no icon is available, the template shows a globe.

{{< figure src="linky-list-layout.png" caption="<span class=\"figure-number\">Figure 3: </span>Custom styling for link posts, including a custom background and the site's favicon. Clicking anywhere in the box goes to the link." >}}

The post body can be just a line or two of my own commentary. When both commentary and summary are blank, an [enrichment workflow](https://github.com/zzamboni/zzamboni.org/blob/main/.github/workflows/enrich-pagescms-posts.yml) tries to fill the summary from the linked article later. I will describe that workflow and its limits in an upcoming article.


## Photos as first-class content {#photos-as-first-class-content}

The [photo Shortcut](https://www.icloud.com/shortcuts/437c4651085e42da9b465c3f0d2857da) takes shared images, resizes and encodes them, and asks for a title and optional commentary. The [photoblog function](https://github.com/zzamboni/zzamboni.org/blob/main/netlify/functions/photoblog.mjs) validates the uploaded images, applies their orientation, re-encodes them to discard embedded location metadata, and creates a post bundle under `content-photos/` together with image files under `static/img/photos/`. The list of images is stored in a `photos` list of image paths into the post's front matter, like this:

```toml
photos = ["/img/photos/2026-11-22-at-cdg-on-my-way-back-home-a9ce8f7e/feature.jpg"]
```

This enabled the use of Pages CMS's native image-management functionality:

{{< figure src="pagescms-image-mgmt.png" caption="<span class=\"figure-number\">Figure 4: </span>Pages CMS image management UI can be used on Photo posts." >}}

The function also adds the `photos` tag. The post and its images all land in a single Git commit.

Blowfish handles the [gallery](https://blowfish.page/docs/shortcodes/#gallery) layout. I use [GLightbox](https://github.com/biati-digital/glightbox) to bring all the galleries and standalone photos in an article together, with full-size images and captions where available. It works with touch and keyboard controls, so I can browse an entire post’s photos without opening and closing each one separately.


## What this setup buys me {#what-this-setup-buys-me}

These are deliberately focused entry points into my existing publishing system. A link or photo can start in the Share Sheet, become a draft in GitHub, be reviewed and edited in Pages CMS without changing how I write long articles. The visible site still consists of static Hugo pages and images.

Of course, there are tradeoffs. Uploading photos as JSON payload means resizing them on the phone, and storing media in Git is a conscious choice for my personal site. The function endpoints also need secret and branch configuration specific to my website. For me, the convenience of a one-tap capture path and a reviewable Git history has been worth that bit of plumbing.

If you want to adapt this, the [link](https://github.com/zzamboni/zzamboni.org/blob/main/netlify/functions/linkblog.mjs) and [photo](https://github.com/zzamboni/zzamboni.org/blob/main/netlify/functions/photoblog.mjs) functions, [Pages CMS configuration](https://github.com/zzamboni/zzamboni.org/blob/main/.pages.yml), and the two Shortcuts linked above are the best starting points. I expect the details to keep evolving, but the shape of the workflow feels right: capture on the device I have in hand, and keep the files where the rest of my site already lives.
