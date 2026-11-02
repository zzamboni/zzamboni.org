+++
title = "Goodbye org-download: native image attachments in Org mode"
author = ["Diego Zamboni"]
summary = "I replaced org-download and several custom image-capture functions with Org attachments and Emacs media pasting. A little configuration keeps images grouped by blog post and makes C-y do the right thing."
date = 2026-10-31T00:00:00+01:00
tags = ["emacs", "orgmode", "doom", "blogging", "howto"]
draft = true
creator = "Emacs 30.2 (Org mode 9.8.9 + ox-hugo)"
toc = false
+++

A few years ago I [wrote about inserting screenshots into Org documents](/post/how-to-insert-screenshots-in-org-documents-on-macos/) using `org-download` and `pngpaste`. That setup served me well, but my image-handling configuration gradually acquired wrappers for choosing filenames, copying existing files, and formatting links.

I recently revisited it and found that native Emacs and Org functionality now covers the parts I actually use. My current setup combines `org-attach` for storage, `yank-media` for clipboard images, and a small helper that chooses between pasting an image and yanking text.


## One attachment identity per post {#one-attachment-identity-per-post}

I keep this blog's Org-authored articles in a single file. Each post is a subtree, often with several child headings. I want an image inserted anywhere inside a post to belong to that post.

My attachment directory is relative to the Org document:

```emacs-lisp
(setq org-attach-id-dir "attachments/")
```

Org partitions ID-based attachments into directories beneath that location. With attachment inheritance enabled, child headings can use the post's attachment identity instead of requiring a new directory for every subsection. My post-capture template already supplies an ID, and Org can create one when needed elsewhere.

Here is the configuration from [my Doom configuration](https://github.com/zzamboni/dot-doom/blob/main/doom.org); `after!` is a Doom macro:

```emacs-lisp
(after! org
  (setq org-attach-use-inheritance t            ;; Inherit ID from higher headings, that way I can have a single ID per blog post
        org-attach-preferred-new-method 'id     ;; Create a new ID when needed
        org-attach-auto-tag nil                 ;; Do not add the ATTACH tag to headings
        org-yank-dnd-method 'attach             ;; Attach by default without asking for drag-and-drop
        org-yank-image-file-name-function 'org-yank-image-read-filename   ;; Ask for filename when attaching something
        org-image-actual-width nil              ;; Flexible image width, with a...
        org-image-max-width 300                 ;; ...maximum for inlined images in org buffers
  ))
```

The image-width settings affect previews in the Org buffer. They do not prescribe the image size on the website.

An inserted link looks like this:

```org
[[attachment:screenshot.png]]
```

The link stays readable without exposing the ID-based directory layout. The attachment files still need to travel with the source: I commit them alongside the Org document, then let `ox-hugo` resolve the attachment links when exporting the post.


## Making C-y choose sensibly {#making-c-y-choose-sensibly}

The remaining bit of custom code handles a small usability problem: I want `C-y` to paste an image when the clipboard contains one, and to behave like an ordinary Org yank otherwise.

```emacs-lisp
(defun zz/org-smart-yank (&optional arg)
  "Yank normally, or use `yank-media' for clipboard images."
  (interactive "P")
  (let ((targets (and (display-graphic-p)
                      (gui-get-selection 'CLIPBOARD 'TARGETS))))
    (if (and (not arg)
             (seq-some
              (lambda (type)
                (string-match-p
                 "^image/\\(png\\|jpeg\\|webp\\|gif\\)$"
                 (format "%s" type)))
              (append targets nil)))
        (yank-media)
      (org-yank arg))))

(after! org
  (map! :map org-mode-map
        "C-y" #'zz/org-smart-yank))
```

In graphical Emacs, this checks the clipboard's advertised formats for PNG, JPEG, WebP, or GIF. If it finds one, it invokes `yank-media`, which uses Org's media handling. Otherwise it calls `org-yank`. A prefix argument, `C-u C-y`, forces the latter path when the clipboard offers both an image and text.

This relies on graphical clipboard support and an Emacs/Org combination that provides `yank-media` and the image-yank options above. It does not turn a terminal session into a clipboard-image transport. When diagnosing a problem, `M-x yank-media` is a useful way to try the media-paste path directly.


## The everyday workflow {#the-everyday-workflow}

Now I copy an image, move to the right place in the post, press `C-y`, and choose a filename. I have left my old timestamp-prefix helper disabled: filenames are already separated by attachment identity, so I usually prefer a plain descriptive name.

For existing files I use `org-attach` (`C-c C-a`), choose copy, and then insert the stored attachment link with `C-c C-l`. For a URL, `org-attach-url` downloads the file. Leaving the link description empty lets Org display an inline image. Dragged files also use attachment storage with this configuration.

I still have a custom function, but it now only selects the action. Org and Emacs handle the storage, link insertion, and media capture. That is a useful reason to revisit an old configuration occasionally: some of the glue I once needed has become functionality I can simply configure.
