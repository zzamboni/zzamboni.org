+++
title = "When a local timestamp pretends to be UTC"
author = ["Diego Zamboni"]
summary = "The Pages CMS date field stores the right clock time but the wrong timezone. Here is why the post disappeared, and the workaround I chose."
date = 2026-09-27T17:21:00+02:00
tags = ["blogging", "hugo", "pagescms", "troubleshooting", "howto"]
draft = false
creator = "Emacs 30.2 (Org mode 9.7.39 + ox-hugo)"
toc = false
featureimage = "img/generated/2026-09-26-pages-cms-hugo-timezones.webp"
+++

I recently added [Pages CMS](https://pagescms.org/) as a way to write short posts for this site from a browser or my phone. My usual workflow is Emacs, Org mode, `ox-hugo` and Hugo, so the two editing paths need to agree on the meaning of a post's `date`. This resulted in an unexpected behavior.


## The disappearing post {#the-disappearing-post}

I first noticed the problem when, after creating a new post using Pages CMS, the new post was not rendered by Hugo when rebuilding my website. After some digging, I realized that Pages CMS's date-and-time field stores my local clock time, but with a format that includes a literal `Z`, representing a UTC timestamp. For example, if my post was created at 14:05 in Zürich in winter, the front matter written by Pages CMS would contain:

```toml
date = '2026-01-15T14:05:00.000Z'
```

The `Z` means **14:05 UTC**, which is 15:05 in Zürich in January. The intended time was 14:05 Zürich time, or 13:05 UTC. During daylight saving time the discrepancy is two hours. Hugo treats a post dated in the future as unpublished, so the post I had just created would be missing from the site. The problem was at the boundary between the browser's local time and the timestamp written to front matter, not in Hugo's parsing of that timestamp.

There is an [open Pages CMS pull request](https://github.com/hunvreus/pagescms/pull/410) to convert date fields to UTC on the client. That is the more general fix: preserve the actual instant when writing a timestamp with `Z`.


## My workaround {#my-workaround}

For now, my Pages CMS configuration writes a local timestamp **without** a timezone suffix:

```yaml
options:
  time: true
  format: "yyyy-MM-dd'T'HH:mm:ss.SSS"
```

I also set the site's default timezone in Hugo:

```toml
timeZone = "Europe/Zurich"
```

Now `2026-01-15T14:05:00.000` means 14:05 in Zürich when Hugo reads it. The named timezone also takes care of the seasonal switch between CET and CEST, since it gets interpreted correctly according to the time of the year.

This works for my single-timezone blog, but a timestamp without an offset is ambiguous outside the site's Hugo configuration. If I start editing while traveling or add collaborators in other timezones, the browser's local clock and `Europe/Zurich` could disagree. At that point I would prefer a proper UTC conversion in Pages CMS, while keeping explicit offsets from `ox-hugo` where available. I hope the pull request I mentioned above gets merged soon!
