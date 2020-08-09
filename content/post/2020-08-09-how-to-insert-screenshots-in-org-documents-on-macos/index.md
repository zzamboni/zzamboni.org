+++
title = "How to insert screenshots in Org documents on macOS"
author = ["Diego Zamboni"]
summary = "As I'm taking notes or writing in Org-mode, I often want to insert screenshots inline with the text. While Org supports inserting and displaying inline images, the assumption is that the image is already somewhere in the file system and we just want to link to it. In this post I will show you how to automate the insertion of images from the clipboard into an org-mode document."
date = 2020-08-09T16:44:00+02:00
tags = ["emacs", "orgmode", "howto", "macos", "config"]
draft = false
creator = "Emacs 26.3 (Org mode 9.3.7 + ox-hugo)"
toc = true
featured_image = "/images/emacs-logo.svg"
+++

As I'm taking notes or writing in Org-mode, I often want to insert screenshots inline with the text. While Org supports [inserting and displaying inline images](https://orgmode.org/manual/Images.html), the assumption is that the image is already somewhere in the file system and we just want to link to it.

The [org-download](https://github.com/abo-abo/org-download) package eases the task of downloading or copying images and attaching them to a document, and it even has an `org-download-screenshot` command, but this assumes you want to initiate the screenshot from within Emacs, whereas the workflow I prefer is like this:

1.  Capture screenshot using the macOS built-in screenshot tool (`Shift​-​⌘​-​5`) and leave it in the clipboard.
2.  Paste the image into the document I'm working on.

Fortunately, `org-download` allows customizing the command used by the `org-download-screenshot` command. Together with the [pngpaste](https://github.com/jcsalterego/pngpaste) utility, this can be used to make `org-download-screenshot` store the image from the clipboard to disk, and insert it into the document. This is my configuration:

```emacs-lisp
(use-package org-download
  :after org
  :defer nil
  :custom
  (org-download-method 'directory)
  (org-download-image-dir "images")
  (org-download-heading-lvl nil)
  (org-download-timestamp "%Y%m%d-%H%M%S_")
  (org-image-actual-width 300)
  (org-download-screenshot-method "/usr/local/bin/pngpaste %s")
  :bind
  ("C-M-y" . org-download-screenshot)
  :config
  (require 'org-download))
```

With this configuration, images are stored in a directory named `images` under the current directory, in a flat directory structure and each file is prepended with a timestamp (I would prefer not to use timestamps, but `org-download` uses a fixed filename for screenshots, which makes it difficult to insert multiple screenshots in the same document). You may want to check the `org-download` documentation and configure these settings to your likely.

Finally, I bind `org-download-screenshot` to `Ctrl​-​⌘​-​y` to keep it similar to the default `Ctrl​-​y` for pasting the clipboard and to easily perform step 2 of the workflow described above.

Thanks to [this thread at Stack Overflow](https://stackoverflow.com/questions/17435995/paste-an-image-on-clipboard-to-emacs-org-mode-file-without-saving-it) for many of the base ideas and pointers.