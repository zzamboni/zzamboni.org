---
title: "Hosting a Ghost Blog in Github - the easier way"
date: 2017-08-19T22:46:42+02:00
draft: true
---

Although this website is generated with [Hugo](https://gohugo.io/), I
seriously considered using Ghost. The advantages of Ghost are many -
very nice UI, beautiful and usable theme out of the box, and a very
vibrant community. Eventually I decided for Hugo because I want to
have full control over everything in my web site, including article
aliases (so as not to forget old content), static files, availability
of [shortcodes](https://gohugo.io/content-management/shortcodes/)
while writing articles, etc.

While evaluating Ghost, I discovered that it is possible to host a
statically-generated Ghost website using GitHub Pages. The approach,
[described](https://github.com/paladini/ghost-on-github-pages/blob/master/README.md) [in](https://medium.com/aishik/publish-with-ghost-on-github-pages-2e5308db90ae) [multiple](http://briank.im/i-see-ghosts/) articles I found, is the following:

1. Install and run Ghost locally
2. Edit/create your content on your local install
3. Create a static copy of your Ghost site by scraping it off the
   local install.
4. Push the static website to GitHub Pages

So far, so good. It makes sense. After all, this is how I created the
[static archive of my old blog, BrT](http://briank.im/i-see-ghosts/),
when I decided to retire its WordPress backend.

But all those articles share one thing: they suggest using a tool
called [buster](https://github.com/axitkhurana/buster) which, as far
as I can tell, it's a web-scraping tool, specialized for
Ghost. However, it seems to have some limitations -- for example, it
does not slurp Ghost static pages, and it hasn't been updated in a
very long time (there's [a fork](https://github.com/skosch/buster)
with somewhat more recent activity).

http://www.suodatin.com/fathom/How-to-retire-a-wordpress-blog-(make-wordpress-a-static-site)

wget -r -E -T 2 -np -R xmlrpc.php,trackback -k http://[BLOG URL]

