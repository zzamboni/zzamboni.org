+++
title = "Automating blog housekeeping with GitHub Actions"
author = ["Diego Zamboni"]
summary = "How I use GitHub Actions for missing summaries, cached link icons, and feature images, with different levels of review for each kind of change."
date = 2026-10-21T12:02:00+02:00
tags = ["blogging", "github", "automation", "pagescms", "ai", "howto"]
draft = true
toc = true
+++

<!-- Markdown preview exported from Org with Pandoc; edit the Org source. -->

After [adding Pages CMS]({{< relref "2026-09-28-using-pagescms-alongside-org-and-hugo" >}}) to my blog, I kept finding small bits of work around a post: writing a summary for the listing, finding an icon for a link, and sometimes choosing a feature image. None of these needs to interrupt the moment when I have something to say.

I now use GitHub Actions to help with those jobs. The interesting part is deciding which changes can be made directly and which should wait for me to look at them.

## Fill a blank, leave my text alone

The [Enrich Pages CMS posts workflow](https://github.com/zzamboni/zzamboni.org/blob/main/.github/workflows/enrich-pagescms-posts.yml) runs for relevant changes on `main` and `staging`. For summaries, it checks the affected CMS posts and leaves any nonempty summary alone. If I have written one, that is the one I want.

When the summary is blank, the workflow uses the post body as its source. If there is no body but the post has an `externalUrl`, it tries to fetch and extract the linked article. This distinction matters for link posts: a summary of someone else's article should not accidentally claim that I wrote it or did the work it describes.

I have also had to account for pages that return a loading screen, login barrier, or error message instead of an article. A blank summary is better than a confident description of something the workflow never actually read. The extraction and generation steps try to skip those cases rather than guess from the title.

Pages CMS has an action for requesting a missing summary manually too. Like the other repository-backed actions, it operates on the saved file. It does not see text still sitting unsaved in my browser.

## Give links an icon without a browser dependency

The same workflow runs my [favicon script](https://github.com/zzamboni/zzamboni.org/blob/main/scripts/fetch-linkblog-favicons.py). It discovers icons from linked sites, converts them to small PNGs, and stores them under `assets/img/linkblog-favicons/`. Posts linking to the same host share the cached icon.

That lets the site display compact link entries without making every visitor's browser fetch an icon from the destination site. If discovery fails, a globe icon is a perfectly acceptable fallback. There is more detail in the [favicon notes](https://github.com/zzamboni/zzamboni.org/blob/main/docs/linkblog-favicons.md), although the current workflow combines this job with summary enrichment.

The workflow commits summary and favicon changes together. Besides keeping related housekeeping in one place in the history, this avoids a separate push for each step. The jobs can still fail independently, and the workflow reports failures rather than treating a partially completed run as a complete success.

## An image is a proposal

Images need more judgment. I can request a feature image from Pages CMS or by running the [image workflow](https://github.com/zzamboni/zzamboni.org/blob/main/.github/workflows/generate-feature-image.yml) manually. It reads the saved post, prepares a visual brief, generates an image, and opens a pull request containing the WebP file and the metadata changes.

I can choose a style and provide extra direction, but that does not guarantee I will like the result. Some images still look much too AI-generated for my taste. Keeping them in a PR gives me a chance to see the actual result in context and decide whether it belongs with the article.

For an Org-authored post, the workflow updates the corresponding Org metadata as well as the Markdown export. Otherwise the next export could undo the image selection. The image itself goes through Hugo's assets pipeline, alongside the other processed resources.

If an image is close, I can ask for a revision in the PR:

``` example
/refine-image Simplify the background and remove the text.
```

That is a paid generation request, not just a comment for my future self. The refinement workflow accepts these commands from my account and updates the image on the same PR branch. I still decide whether to merge it. The [feature-image guide](https://github.com/zzamboni/zzamboni.org/blob/main/docs/feature-image-generation.md) has the operating details.

## Keep the cost visible

The generation workflows also call a small [usage-reporting workflow](https://github.com/zzamboni/zzamboni.org/blob/main/.github/workflows/openai-usage.yml). It reports current-day and month-to-date costs, and can estimate what remains from a recorded credit purchase when I provide its date and amount.

I think of that estimate as a reminder, not an authoritative balance. It describes one recorded purchase, and does not reconstruct the provider's prepaid ledger. The report also needs an admin key with access to cost information, separate from the key used for generation. Missing reporting configuration should not prevent the main job from completing.

This is small enough to keep with the other automation rather than build a dashboard for it. The [usage notes](https://github.com/zzamboni/zzamboni.org/blob/main/docs/openai-usage.md) explain what the numbers mean and where their limitations are.

## Choosing what to automate

The boundary I have ended up with is practical: preserve text I supplied, make small missing-metadata changes easy to inspect in Git, and ask me to review generated images before using them. A summary can still be wrong, so I check the resulting post; putting something in a workflow does not make it editorially reliable.

I like that the automation leaves ordinary files behind. I can edit a generated summary, replace an icon, or close an image PR and carry on. The tools help finish a post, but they do not need to become another publishing system.
