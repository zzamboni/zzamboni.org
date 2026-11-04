+++
title = 'Badges in Org files in Github'
summary = 'How to display shields.io badges from an Org file in Github without resorting to HTML.'
date = '2026-11-04T12:09:00.000'
tags = [
	'tips',
	'orgmode',
]
draft = true
featureimage = 'img/tram-zurich.jpg'
toc = false
+++
I love badges - those little graphical status or information indicators often seen in Github README files, like this:

![Static Badge](https://img.shields.io/badge/this_is-a_cool_badge-blue?label=This%20is)

There's a whole service [https://shields.io/](https://shields.io/) devoted to this, but they can come from anywhere - for example Netlify provides its own [status badges](https://docs.netlify.com/manage/monitoring/status-badges/).

I love that Github also renders Org-mode files correctly, however I ran into a problem when trying to display badges within Org files - the badge was being shown as text instead of as an image. This could be solved by using Org's `#+HTML:` keywords to insert HTML code directly, but I prefer to stick to the native markup whenever possible.

I found the cause: Github's Org-mode parser expects image URLs to have an image extension, and often the badge image URLs don't. For example this is the URL for the badge above: `https://img.shields.io/badge/this_is-a_cool_badge-blue`

Fortunately, I also found the solution! Just add .svg to the end of the URL. This seems to work with both [shields.io](http://shields.io) and Netlify badges. In the example above, this means using `https://img.shields.io/badge/this_is-a_cool_badge-blue.svg`. The badge is shown without the extension. This works too for the Netlify badge URLs.

You can see this in action in my website's [README.org](https://github.com/zzamboni/zzamboni.org/blob/main/README.org) file. The Org-mode markup for the badges is this:

```
[[https://app.netlify.com/projects/zzamboni/deploys][https://api.netlify.com/api/v1/badges/e5ae9eeb-01ec-4b37-90ad-2f4b3877a7d6/deploy-status.svg]]
[[https://zzamboni.org][https://img.shields.io/website?url=https%3A%2F%2Fzzamboni.org&up_message=zzamboni.org&down_message=zzamboni.org%20(down).svg]]
```

