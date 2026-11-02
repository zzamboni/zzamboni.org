+++
title = "From Org mode to a PDF cheat sheet with Typst"
author = ["Diego Zamboni"]
summary = "My Doom Emacs cheat sheet lives in Org mode and exports to PDF through ox-typst. A small Typst header controls the appearance, with one targeted adjustment for table widths and repeating headers."
date = 2026-10-31T00:00:00+01:00
tags = ["emacs", "orgmode", "typst", "documentation", "howto"]
draft = true
creator = "Emacs 30.2 (Org mode 9.8.9 + ox-hugo)"
toc = false
+++

I have used Emacs long enough to accumulate plenty of useful commands that I promptly forget when I need them. My solution is a [personal cheat sheet](https://github.com/zzamboni/dot-doom/blob/main/cheatsheet.org): short tables of tasks, keybindings, and command names for blogging, inserting images, and working with Org subtrees.

The source belongs in Org mode, where I can edit it while using the tools it describes. I also want a readable PDF that I can keep open beside Emacs. The first version used Org's LaTeX exporter; I recently switched it to [Typst](https://typst.app/) using [ox-typst](https://github.com/jmpunkt/ox-typst).


## Keep the source ordinary {#keep-the-source-ordinary}

Most of the file is still headings, short explanations, and three-column Org tables. For example:

```org
| Action                | Shortcut | Command                  |
|-----------------------+----------+--------------------------|
| Narrow to one subtree | C-x n s  | org-narrow-to-subtree     |
| Restore entire buffer | C-x n w  | widen                    |
```

I include command names because some shortcuts are specific to [my configuration](/post/my-doom-emacs-configuration-with-commentary/). The PDF should help me remember what a binding does, and the Org source should remain useful when read directly on GitHub.

The presentation settings live at the top of the same file, so I can change the layout without rewriting the reference material.


## Exporting through ox-typst {#exporting-through-ox-typst}

In my literate Doom configuration I install and load the exporter:

```emacs-lisp
;; Package declaration, tangled to packages.el:
(package! ox-typst)

;; Configuration, tangled to config.el:
(use-package! ox-typst
  :after org)
```

After changing package declarations I run `doom sync`. Typst itself also needs to be installed and available to Emacs. I can then run `M-x org-typst-export-to-pdf`. The exporter also registers a `y` prefix in Org's export dispatcher.

The pipeline is straightforward: Org source becomes Typst source, which Typst compiles to PDF. I keep the Org source and the resulting [PDF](https://github.com/zzamboni/dot-doom/blob/main/cheatsheet.pdf) in the repository; generated `.typ` files are ignored.


## A small layout header {#a-small-layout-header}

I chose the [cram-snap](https://typst.app/universe/package/cram-snap/) package as the starting point for the layout, pinned to version `0.2.2`. My header sets A4 paper, margins, fonts, colors, and spacing. Here is a reduced example of the arrangement:

```org
#+options: toc:nil num:nil author:nil date:nil
#+typst_header: #import "@preview/cram-snap:0.2.2": cram-snap
#+typst_header: #set page(paper: "a4", margin: 14mm)
#+typst_header: #set text(font: "Source Sans 3", size: 10pt)
#+typst_header: #show: doc => context cram-snap(title: document.title, column-number: 1, doc)
#+typst_header: #show raw: set text(font: "Cascadia Code", size: 8.2pt)
```

The real header adds the color and spacing adjustments. In the exporter version I am using, the title becomes document metadata, so I explicitly pass `document.title` to the template to make it visible.

The fonts need to be installed. Typst downloads the pinned package on first use and subsequently uses its cache. Pinning the package keeps a future export from silently picking up a different template release.


## Tables needed one extra step {#tables-needed-one-extra-step}

The main layout issue was the tables. In my export, `ox-typst` gave the three columns equal widths and represented the heading row as ordinary cells. That wastes space on short keybindings and leaves too little room for explanations.

I added a Typst show rule that rebuilds those tables with widths of `23%`, `20%`, and `57%`, and wraps the first three cells in `table.header(repeat: true, ...)`. Expanded for readability, the rule looks like this:

```typst
#show table: it => if it.children.first().func() == table.header {
  it
} else {
  table(
    columns: (23%, 20%, 57%),
    inset: (x: 5pt, y: 3pt),
    table.header(repeat: true, ..it.children.slice(0, 3)),
    ..it.children.slice(3),
  )
}
```

In the Org file this is another `#+typst_header:` line. It is tailored to my uniform three-column tables; it would need adjusting before applying it to a document with different table shapes. The repeated header helps when a table crosses a page boundary.


## A reference I can keep updating {#a-reference-i-can-keep-updating}

There is still layout code to maintain, but it is concentrated in a short header. Adding a new command usually means adding a row to an Org table and exporting again.

The [complete source](https://github.com/zzamboni/dot-doom/blob/main/cheatsheet.org) includes the details omitted here. For this small document, Org handles the writing and Typst handles the page layout, which is exactly the division of work I wanted.
