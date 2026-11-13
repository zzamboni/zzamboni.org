+++
title = "Cross-article linking in Org/Hugo"
author = ["Diego Zamboni"]
summary = "My new Org heading-link picker finds headings in included files, creates Hugo-aware links, and lets me update links without rewriting their description."
date = 2026-11-13T03:25:00+01:00
tags = ["emacs", "orgmode", "doom", "hugo", "howto"]
draft = false
creator = "Emacs (Org mode + ox-hugo)"
featureimage = "img/generated/2026-11-12-org-heading-links-across-hugo-articles.webp"
+++

A few years ago I wrote about [creating human-readable heading IDs in Org mode]({{< relref "2020-12-06-org-mode-human-readable-ids" >}}). At the time I used `counsel-org-link` with Ivy and a bit of custom code to insert links using `CUSTOM_ID` instead of opaque UUIDs.

I still want readable links, but my setup has become more complex. I write this blog in one Org file, with each article exported separately by [ox-hugo](https://ox-hugo.scripter.co/). Some articles, like [my Doom Emacs configuration]({{< relref "my-doom-emacs-configuration-with-commentary" >}}), also pull in other Org files using `#+include:`. I wanted to be able to interactively link to headings within those files as well.


## One shortcut for finding headings {#one-shortcut-for-finding-headings}

I still use `C-c l l h` to run my own `zz/org-insert-heading-link` command, but the function now uses Vertico to give me a searchable list of headings, including their outline paths and line numbers to distinguish similar titles. The picker also expands `#+include:` directives (including nested includes and line ranges) and identifies headings that came from another file. This is what it looks like:

{{< figure src="heading-picker.png" caption="<span class=\"figure-number\">Figure 1: </span>Extended heading picker. The \"included\" items come from my external [doom.org](https://github.com/zzamboni/dot-doom/blob/main/doom.org) file, so I can link directly to them from other posts" >}}

For headings in the main Org document, like before, the command reuses an existing `CUSTOM_ID` or creates one from the title, then inserts a normal Org link. Since ox-hugo knows which article owns each heading, this also works for links between articles defined in the same source file.

Included headings need different treatment. The picker doesn't modify the included files or add IDs to them. Instead, it uses their existing `CUSTOM_ID` when available, falling back to a plain Org-mode anchor based on the heading title.


## The trick: a Hugo-aware link for included headings {#the-trick-a-hugo-aware-link-for-included-headings}

Here are two links from my blog source:

```org
[[#how-to-easily-create-and-use-human-readable-ids-in-org-mode-and-doom-emacs][my earlier post]]
[[hugo-ref:/post/my-doom-emacs-configuration-with-commentary/index.md#links-between-headings][my heading-link configuration]]
```

The first is an ordinary Org heading link. The second points into an **included** Org file. An ordinary `#links-between-headings` link would fail during ox-hugo export because that heading doesn't exist in the Org file when the link is resolved.

To handle this, I added a custom `hugo-ref:` link type. It records the owning Hugo content file (i.e. the file in which the external file is included) and heading anchor. During Hugo export, my link handler turns it into Markdown containing Hugo's [`relref` shortcode](https://gohugo.io/shortcodes/relref/):

```markdown
[my heading-link configuration]({{</* relref "/post/my-doom-emacs-configuration-with-commentary/index.md#links-between-headings" */>}})
```

Hugo then resolves the content reference to the right permalink. For other Org export backends, the handler keeps only the link description as plain text. You can see the [full implementation in my Doom Emacs configuration]({{< relref "/post/my-doom-emacs-configuration-with-commentary/index.md#links-between-headings" >}}).


## A small bonus: changing an existing link {#a-small-bonus-changing-an-existing-link}

I also added a shortcut I keep needing while editing: with the cursor on a link, `C-u C-c l l h` runs the same picker but **replaces the destination while keeping the description**. That works for normal Org links and the new `hugo-ref:` links. No more deleting and recreating a link just because I chose the wrong heading.

There are still the usual caveats: title-derived anchors can change when a heading is renamed, and duplicate headings may produce ambiguous anchors. Ideally, for links I want to keep stable, I use an explicit, unique `CUSTOM_ID`.

The code is a little more involved than my original `counsel-org-link` customization, but the everyday workflow is simpler and more capable: press a shortcut, select a heading, and let Org and Hugo sort out the rest.
