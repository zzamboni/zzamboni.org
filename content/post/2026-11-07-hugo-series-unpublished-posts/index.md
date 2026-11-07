+++
title = "Making Hugo article series work with unpublished posts"
author = ["Diego Zamboni"]
summary = "My website setup series includes unfinished articles. A small template override lists their titles as Upcoming, preserving the numbering without publishing draft pages."
date = 2026-11-07T00:00:00+01:00
tags = ["blogging","hugo","blowfish","templates","howto"]
draft = true
creator = "Emacs (Org mode + ox-hugo)"
toc = false
+++

I recently grouped my blogging infrastructure articles into a [My website setup](/series/my-website-setup/) series. Some installments are published; others are still drafts. Blowfish orders the articles using `series_order`, so production visitors could see parts 1, 2, 4, and 5 with no explanation of the missing part 3.

I liked keeping the planned numbering: it gives the series a structure that does not change every time I publish an installment. I wanted the navigation to show what was coming, without offering links to pages that do not exist yet.

## The missing information is outside Hugo's page collection {#the-missing-information-is-outside-hugos-page-collection}

An article's front matter provides its series membership and position:

```toml
series = ["My website setup"]
series_order = 3
draft = true
```

In my Org source these values are export properties, and `ox-hugo` writes them into the Markdown front matter. A normal production build excludes draft pages from the series collection that the navigation uses. Sorting that collection differently cannot restore entries that are not there.

Enabling drafts for production would make their contents available too. Instead, I extended the navigation with a separate collection of editorial metadata.

## Read metadata from the exported files {#read-metadata-from-the-exported-files}

A small [helper partial](https://github.com/zzamboni/zzamboni.org/blob/main/layouts/partials/series/drafts.html) walks `content/post/` recursively. It opens Markdown files, extracts their TOML front matter, and keeps draft entries that have a series and part number. The records it returns contain only the title, series membership, and order:

```go-html-template
{{- if and $meta.draft $meta.series $meta.series_order -}}
  {{- $drafts = $drafts | append (dict
    "title" $meta.title
    "series" $meta.series
    "order" (int $meta.series_order)) -}}
{{- end -}}
```

The file is read to extract its front matter, but the helper does not render the draft body or turn it into a Hugo page. I call it through `partialCached` so the scan is shared across article navigations during the build.

This is deliberately specific to my current sources: TOML-frontmatter Markdown under `content/post/`, where my Org exports live. It does not discover drafts in the separate CMS content root, or drafts using YAML front matter. An Org draft must be exported before it can appear.

## Merge real pages and upcoming entries {#merge-real-pages-and-upcoming-entries}

My [series template override](https://github.com/zzamboni/zzamboni.org/blob/main/layouts/partials/series/series_base.html) first collects the pages Hugo already knows about. It then adds matching draft records only when their part number is missing, and sorts the combined list by order.

A record with a page gets the usual link, or the current-article label. A metadata-only record gets plain text and an _Upcoming_ label:

```text
Part 2: A published installment
Part 3: An unfinished installment — Upcoming
Part 4: Another published installment
```

There is no anchor around the upcoming row. The title itself is intentionally public, so I would not use this for a draft whose existence or working title should remain private. The series also needs unique part numbers, because those numbers are what the merge uses to detect an existing entry.

## The same sources work in previews {#the-same-sources-work-in-previews}

On the draft site, Hugo already includes the unfinished pages. Those page entries take precedence over the metadata records, so they retain working links for review. Publishing an installment changes its normal page metadata, and the next production build automatically replaces its upcoming row with a link.

The override applies to the series navigation at the top and bottom of articles. The series taxonomy landing page keeps its normal published-only listing.

For validation, I check both a regular build and one with drafts enabled: upcoming titles should be visible in production navigation, while their page output, search entries, RSS entries, and sitemap entries remain absent. In the draft build, the same installments should be linked.

The result is a small editorial improvement: readers can see the intended shape of the series, and I can keep publishing it one installment at a time. There is no second reading list to maintain; the exported article metadata supplies it.
