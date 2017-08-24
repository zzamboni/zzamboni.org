---
title: "Hosting a Ghost Blog in Github - the easier way"
date: 2017-08-19T22:46:42+02:00
draft: true
featured_image: '/images/ghost-plus-github2.png'
---

Ghost is an easy-to-use, beautiful blogging engine. Ghost normally
needs an active server-side component, but it is also possible to host
a statically-generated Ghost website using GitHub Pages.

<!--more-->

While I was planning the reboot of this website, I seriously
considered using Ghost. The advantages of Ghost are many - very nice
UI, beautiful and usable theme out of the box, and a very active
community. Eventually I decided to use [Hugo](https://gohugo.io/),
because I want to have full control over everything in my web site,
including article aliases (so as not to forget old content), static
files, availability of
[shortcodes](https://gohugo.io/content-management/shortcodes/) while
writing articles, etc.

One of the advantages of Hugo is that it generates a static website,
which makes it possible to host it in GitHub Pages. Ghost normally
needs an active server-side component. However, while evaluating
Ghost, I discovered that it is possible to host a statically-generated
Ghost website using GitHub Pages.

# Generating a static website using Ghost

The approach,
[described](https://github.com/paladini/ghost-on-github-pages/blob/master/README.md)
[in](https://medium.com/aishik/publish-with-ghost-on-github-pages-2e5308db90ae)
[multiple](http://briank.im/i-see-ghosts/) articles I found, is the
following:

1. Install and run Ghost locally
2. Edit/create your content on your local install
3. Create a static copy of your Ghost site by scraping it off the
   local install.
4. Push the static website to GitHub Pages

So far, so good. It makes sense. But all those articles share one
thing: they suggest using a tool called
[buster](https://github.com/axitkhurana/buster) which, as far as I can
tell, it's a web-scraping tool, specialized for Ghost. However, it
seems to have some limitations -- for example, it does not slurp Ghost
static pages, and it hasn't been updated in a very long time (there's
[a fork](https://github.com/skosch/buster) with somewhat more recent
activity).

I found this puzzling, since there is a perfectly mature, functional
and complete tool for scraping off a copy of a website: good old
trusty [wget](https://en.wikipedia.org/wiki/Wget). It is included (or
easily available) in most Unix/Linux distributions, it is extremely
powerful, and has features that make it really easy to create a local,
working copy of a website (including proper translation of URLs). I
used it to create the [static archive of my old blog,
BrT](http://briank.im/i-see-ghosts/), when I decided to retire its
WordPress backend years ago.

Another thing I found is that most instructions suggest hosting only
the generated website in your GitHub repository. GitHub pages allows
serving the website [from different
sources](https://help.github.com/articles/configuring-a-publishing-source-for-github-pages/),
including the repo's `gh-pages` branch, its `master` branch, or the
`/docs` directory in the `master` branch. Personally, I prefer using
the `/docs` directory since it allows me to keep both the source and
the generated website in the same place, without any branch fiddling.

So, without further ado, here are the detailed instructions.

## Set up Ghost locally

## Generate a static copy of the website

 I learned the correct options in [this
blog
post](http://www.suodatin.com/fathom/How-to-retire-a-wordpress-blog-(make-wordpress-a-static-site)),
although it's not to hard to gather them from the [wget man
page](http://www.misc.cl.cam.ac.uk/cgi-bin/manpage?wget):

```
wget -r -E -T 2 -np -k URL
```

## Create and populate the GitHub repo

## Configure source for GitHub pages
