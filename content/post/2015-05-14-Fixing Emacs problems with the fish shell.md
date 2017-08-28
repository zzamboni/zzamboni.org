---
categories: &1
- tips
- macosx
- emacs
date: '2015-05-14'
description: ''
keywords: []
title: Fixing Emacs problems with the fish shell
tags: *1
aliases:
- /new/blog/fixing-emacs-problems-with-the-fish-shell
slug: fixing-emacs-problems-with-the-fish-shell
---


I started getting errors from the TRAMP Emacs package because I was using <a href='http://fishshell.com'>fish</a> as my default shell, and it does not recognize certain standard syntax elements (such as `&&` to separate commands), and Emacs runs subcommands under the default shell. I fixed this by:


<ol>
<li>Changing my account's default shell back to `/bin/bash`</li>
<li>Changing my Terminal.app preferences to run `/usr/local/bin/fish` when a shell opens, instead of the default login shell:

<img hash='417871b0759962c66c27584a7a5a1c1e' src='/note/ef694fab-a850-4633-8a19-2cfa517f16a5/img/417871b0759962c66c27584a7a5a1c1e/General.png' style='height:auto;' type='image/png' width='485'/></li>
<li>Log out and back in to have everything reloaded properly.</li>
</ol>


This does not change my interactive experience at all, while leaving `/bin/bash` as the default for sub-shells, no only in Emacs but in any other applications that might break because of fish's non-standard syntax.


