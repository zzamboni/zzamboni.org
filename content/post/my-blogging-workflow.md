+++
title = "My blogging workflow with Emacs, org-mode+ox-hugo, Hugo and GitHub"
author = ["Diego Zamboni"]
tags = ["blogging", "howto", "emacs", "hugo", "orgmode", "github"]
draft = true
creator = "Emacs 26.1 (Org mode 9.2.3 + ox-hugo)"
+++

My blogging has seen [multiple iterations](/about/#my-online-past) over the years, and with it, the tools I use have changed. At the moment I use a set of tools and workflows which make it very easy to keep my blog updated, and I will describe them in this post. In short, they are:

-   **Writing:** Emacs, org-mode
-   **Exporting:** ox-hugo
-   **Publishing:** Hugo
-   **Hosting:** GitHub Pages

Let's take a closer look at each of the stages.


## Writing using Emacs and org-mode {#writing-using-emacs-and-org-mode}

I have been using Emacs for almost 30 years, so its use for me is second nature. However, I only recently started using [org-mode](https://orgmode.org/) for writing, blogging, coding, presentations and more, thanks to the hearty recommendations and information from [Nick](http://www.cmdln.org/) and many others. I am duly impressed. I have been a fan of the idea of [literate programming](https://en.wikipedia.org/wiki/Literate%5Fprogramming) for many years, and I have tried other tools before (most notably [noweb](https://www.cs.tufts.edu/~nr/noweb/), which I used during grad school for many of my homeworks and projects), but org-mode is the first tool I have encountered which seems to make it practical. Here are some of the resources I have found useful in learning it:

-   Howard Abrams' [Introduction to Literate Programming](http://www.howardism.org/Technical/Emacs/literate-programming-tutorial.html), which got me jumpstarted into writing code documented with org-mode.
-   Nick Anderson's [Level up your notes with Org](https://github.com/nickanderson/Level-up-your-notes-with-Org), which contains many useful tips and configuration tricks.
-   Sacha Chua's [Some tips for learning Org Mode for Emacs](http://sachachua.com/blog/2014/01/tips-learning-org-mode-emacs/), her [Emacs configuration](http://pages.sachachua.com/.emacs.d/Sacha.html) and many of her [other articles](http://sachachua.com/blog/category/emacs/).
-   Rainer König's [OrgMode Tutorial](https://www.youtube.com/playlist?list=PLVtKhBrRV%5FZkPnBtt%5FTD1Cs9PJlU0IIdE) video series.

You can see some examples in [my "literate config files" series](/tags/literateconfig/), and all recent posts in this blog are written using org-mode (you can find the [source file](https://github.com/zzamboni/zzamboni.org/blob/master/content-org/zzamboni.org) in GitHub).

Over time I have tweaked my Emacs configuration to make writing with org-mode more pleasant. You can see my tutorial on [Beautifying org-mode in Emacs](/post/beautifying-org-mode-in-emacs/), and also see the full [org-mode section of my Emacs config](/post/my-emacs-configuration-with-commentary/#org-mode) for reference.

So, I write posts using Emacs, in org-mode markup. What's next?


## Exporting {#exporting}

When I first started writing my blog posts in org-mode, I relied on Hugo's [built-in support for it](https://gohugo.io/content-management/formats/), which allows you to simply create posts in `.org` files instead of `.md` and have them parse in org-mode format. Unfortunately, the support is not perfect. Hugo relies on the [goorgeous](https://github.com/chaseadamsio/goorgeous) library which, while quite powerful, does not support the full org-mode markup capabilities, so many elements are not rendered or processed properly.

Happily, I discovered [ox-hugo](https://ox-hugo.scripter.co/), an org-mode exporter which produces Hugo-ready Markdown files from the org-mode source, from which Hugo can produce the final HTML output. This is a much better arrangement, because each component handles only its native format: ox-hugo processes the org-mode source with the full support of org-mode and Emacs, and Hugo processes Markdown files, which are its native input format. You can use the full range of org-mode markup in your posts, and they will be correctly converted to their equivalents in Markdown. Furthermore, your source files remain output-agnostic, as you can still use all other org-mode exporters if you need to produce other formats.

Ox-hugo supports [two ways of organizing your posts](https://ox-hugo.scripter.co/#screenshot-one-post-per-subtree): one post per org file, and one post per org subtree. In the first one, you write a separate org file for each post. In the second, you keep all your posts in a single org file, and specify (through org-mode properties) which subtrees should be exported as posts. The latter is the recommended way to organize posts. At first I was skeptical - who wants to keep everything in a single file? However, as I have worked more with it, I have come to realize its advantages. For one, it makes it easier to specify post metadata - for example, I have defined sections in [my org-mode source file](https://github.com/zzamboni/zzamboni.org/blob/master/content-org/zzamboni.org) for certain frequent topics, and those are tagged accordingly in the org source. When I create posts as subtrees of those sections, they inherit the top-level tags automatically, as well as any other properties, which I used to define (for example) the header images used in the posts. Having all posts in a single file also makes it easier to share other content, such as org macro definitions, ox-hugo configuration options, etc.

Note that ox-hugo is not limited to exporting blog posts, but any content processed by Hugo. For example, my org source file also includes all the static pages in my web site - they are differentiated from blog posts simply by the Hugo [section](https://gohugo.io/content-management/sections/) to which they belong, which is defined using the [HUGO\_SECTION property](https://ox-hugo.scripter.co/doc/usage/#before-you-export), which is interpreted accordingly by ox-hugo.

Since the full power of org markup is available when using ox-hugo, you can do very interesting things. For example, all posts in my [Literate Config Files](/tags/literateconfig/) category are automatically updated every time I export them with the actual, real content of the corresponding config files, which I also keep in org format. There is a lot of hidden power in org-mode and ox-hugo. My recommendation is to go through the source files for some of the websites listed in ox-hugo's [Real World Examples](https://ox-hugo.scripter.co/doc/examples/) section. For example, I have learned a lot by reading through the source files for the [ox-hugo website](https://github.com/kaushalmodi/ox-hugo/tree/master/doc) itself.


## Publishing {#publishing}

Using Netlify. Caveats:

-   Take care of invalid characters in filenames.
-   Disable Hugo redirects and implement aliases using Netlify aliases: <https://gohugo.io/news/http2-server-push-in-hugo/>

Once ox-hugo has generated the Markdown files for my posts, it is Hugo's turn to convert them into HTML files that can be published as a website. Ox-hugo knows the default structure expected by Hugo (a top-level `content/` directory in which you have directories for each section), so there's usually not much to do other than point ox-hugo to where your top-level Hugo directory is, using the [HUGO\_BASE\_DIR](https://ox-hugo.scripter.co/doc/usage/#before-you-export) property. Of course, this presumes you already have a Hugo site. If you have never used Hugo before, I would suggest you go through the [Quick Start](http://gohugo.io/getting-started/quick-start/) guide, which shows how to set up a basic website using the [Ananke](https://github.com/budparr/gohugo-theme-ananke) theme. This is the same theme I use for my website.

One particular piece of configuration I use to make publishing with GitHub pages easier: I change Hugo's `publishDir` parameter from its default value of `public` to `docs`, to make it easier to publish my final website from within the same repository (more below in the [Hosting](#hosting) section). This is done by specifying the parameter in Hugo's [`config.toml`](https://github.com/zzamboni/zzamboni.org/blob/master/config.toml#L9) file:

```conf-toml
publishDir = "docs"
```

Hugo has extensive capabilities and it is beyond the scope of this article to show you how to use it, but it has [very good documentation](https://gohugo.io/documentation/) which I would urge you to peruse to learn more about it. Feel free to peruse [my setup](https://github.com/zzamboni/zzamboni.org/blob/master/content-org/zzamboni.org) for ideas.


## Hosting {#hosting}

-   Publishing from docs/
-   Setting up SSL certificate


## What's next? {#what-s-next}

-   Automatic publishing using GitHub CI
-   Maybe migrate to GitLab pages?
