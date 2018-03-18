+++
title = "My Emacs Configuration, With Commentary"
author = ["Zamboni Diego"]
date = 2017-12-17T20:14:00+01:00
tags = ["config", "howto", "literate-programming", "emacs"]
draft = false
creator = "Emacs 25.3.2 (Org mode 9.1.7 + ox-hugo)"
featured_image = "/images/emacs-logo.svg"
toc = true
summary = "I have enjoyed slowly converting my configuration files to literate programming style using org-mode in Emacs. It's now the turn of my Emacs configuration file."
+++

Last update: **March 17th, 2018**

I have enjoyed slowly converting my configuration files to [literate programming](http://www.howardism.org/Technical/Emacs/literate-programming-tutorial.html) style style using org-mode in Emacs. I previously posted my [Elvish configuration](../my-elvish-configuration-with-commentary/), and now it's the turn of my Emacs configuration file. The text below is included directly from my [init.org](https://github.com/zzamboni/dot_emacs/blob/master/init.org) file. Please note that the text below is a snapshot as the file stands as of the date shown above, but it is always evolving. See the [init.org file in GitHub](https://github.com/zzamboni/dot_emacs/blob/master/init.org) for my current, live configuration, and the generated file at <https://github.com/zzamboni/dot_emacs/blob/master/init.el>.


## Customized variables {#customized-variables}

Emacs has its own [Customization mechanism](https://www.gnu.org/software/emacs/manual/html_node/emacs/Easy-Customization.html#Easy-Customization) for easily customizing many parameters. To make it easier to manage, I keep the customized variables and faces in a separate file and load it from the main file.

```emacs-lisp
(setq custom-file "~/.emacs.d/custom.el")
(load custom-file)
```

Here is the current contents of the [custom.el](https://github.com/zzamboni/dot-emacs/blob/master/custom.el) file.

```emacs-lisp
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(cfengine-indent 1)
 '(column-number-mode t)
 '(custom-safe-themes
   (quote
    ("8e4efc4bed89c4e67167fdabff77102abeb0b1c203953de1e6ab4d2e3a02939a" "a1a966cf2e87be6a148158c79863440ba2e45aa06cc214341feafe5c6deca4f2" "3eb2b5607b41ad8a6da75fe04d5f92a46d1b9a95a202e3f5369e2cdefb7aac5c" "3d0142352ce19c860047ad7402546944f84c270e84ae479beddbc2608268e0e5" "a33858123d3d3ca10c03c657693881b9f8810c9e242a62f1ad6380adf57b031c" "a40eac965142a2057269f8b2abd546b71a0e58e733c6668a62b1ad1aa7669220" "7be789f201ea16242dab84dd5f225a55370dbecae248d4251edbd286fe879cfa" "94dac4d15d12ba671f77a93d84ad9f799808714d4c5d247d5fd944df951b91d6" "4d8fab23f15347bce54eb7137789ab93007010fa47296c2f36757ff84b5b3c8a" default)))
 '(global-visible-mark-mode t)
 '(js-indent-level 2)
 '(lua-indent-level 2)
 '(org-agenda-files nil)
 '(org-mac-grab-Acrobat-app-p nil)
 '(org-mac-grab-devonthink-app-p nil)
 '(org-structure-template-alist
   (quote
    ((97 . "export ascii")
     (99 . "center")
     (67 . "comment")
     (101 . "example")
     (69 . "export")
     (104 . "export html")
     (108 . "export latex")
     (113 . "quote")
     (115 . "src")
     (118 . "verse")
     (110 . "notes"))))
 '(package-selected-packages
   (quote
    (ox-hugo adaptive-wrap yankpad smart-mode-line org-plus-contrib ob-cfengine3 org-journal ox-asciidoc org-jira ox-jira org-bullets ox-reveal lispy parinfer uniquify csv all-the-icons toc-org helm cider clojure-mode ido-completing-read+ writeroom-mode crosshairs ox-confluence ox-md inf-ruby ob-plantuml ob-ruby darktooth-theme kaolin-themes htmlize ag col-highlight nix-mode easy-hugo elvish-mode zen-mode racket-mode package-lint scala-mode go-mode wc-mode neotree applescript-mode ack magit clj-refactor yaml-mode visual-fill-column visible-mark use-package unfill typopunct smooth-scrolling smex smartparens rainbow-delimiters projectile markdown-mode magit-popup lua-mode keyfreq imenu-anywhere iedit ido-ubiquitous hl-sexp gruvbox-theme git-commit fish-mode exec-path-from-shell company clojure-mode-extra-font-locking clojure-cheatsheet aggressive-indent adoc-mode 4clojure)))
 '(reb-re-syntax (quote string))
 '(safe-local-variable-values
   (quote
    ((org-adapt-indentation)
     (org-edit-src-content-indentation . 2))))
 '(sml/replacer-regexp-list
   (quote
    (("^~/org" ":Org:")
     ("^~/\\.emacs\\.d/elpa/" ":ELPA:")
     ("^~/\\.emacs\\.d/" ":ED:")
     ("^/sudo:.*:" ":SU:")
     ("^~/Documents/" ":Doc:")
     ("^~/Dropbox/" ":DB:")
     ("^:\\([^:]*\\):Documento?s/" ":\\1/Doc:")
     ("^~/[Gg]it/" ":Git:")
     ("^~/[Gg]it[Hh]ub/" ":Git:")
     ("^~/[Gg]it\\([Hh]ub\\|\\)-?[Pp]rojects/" ":Git:")
     ("^:DB:Personal/writing/learning-cfengine-3/learning-cfengine-3/" "[cf-learn]")
     ("^:DB:Personal/devel/zzamboni.org/zzamboni.org/" "[zz.org]")
     ("^\\[zz.org\\]content/post/" "[zz.org/posts]"))))
 '(tab-width 2)
 '(tool-bar-mode nil))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(default ((t (:inherit nil :stipple nil :background "#282828" :foreground "#FDF4C1" :inverse-video nil :box nil :strike-through nil :overline nil :underline nil :slant normal :weight normal :height 160 :width normal :foundry "nil" :family "Inconsolata"))))
 '(col-highlight ((t (:background "#3c3836"))))
 '(fixed-pitch ((t (:inherit nil :stipple nil :background "#282828" :foreground "#fdf4c1" :inverse-video nil :box nil :strike-through nil :overline nil :underline nil :slant normal :weight normal :height 1.0 :width normal :foundry "nil" :family "Inconsolata"))))
 '(linum ((t (:background "#282828" :foreground "#504945" :height 140 :family "Inconsolata"))))
 '(markup-meta-face ((t (:foreground "gray40" :height 140 :family "Inconsolata"))))
 '(markup-title-0-face ((t (:inherit markup-gen-face :height 1.6))))
 '(markup-title-1-face ((t (:inherit markup-gen-face :height 1.5))))
 '(markup-title-2-face ((t (:inherit markup-gen-face :height 1.4))))
 '(markup-title-3-face ((t (:inherit markup-gen-face :weight bold :height 1.3))))
 '(markup-title-5-face ((t (:inherit markup-gen-face :underline t :height 1.1))))
 '(org-block ((t (:inherit fixed-pitch))))
 '(org-document-info ((t (:foreground "dark orange"))))
 '(org-document-info-keyword ((t (:inherit (shadow fixed-pitch)))))
 '(org-document-title ((((class color) (min-colors 16777215)) (:foreground "#3FD7E5" :weight bold)) (((class color) (min-colors 255)) (:foreground "#00d7ff" :weight bold))))
 '(org-level-1 ((((class color) (min-colors 16777215)) (:foreground "#FE8019")) (((class color) (min-colors 255)) (:foreground "#ff8700"))))
 '(org-level-2 ((((class color) (min-colors 16777215)) (:foreground "#B8BB26")) (((class color) (min-colors 255)) (:foreground "#afaf00"))))
 '(org-level-3 ((((class color) (min-colors 16777215)) (:foreground "#83A598")) (((class color) (min-colors 255)) (:foreground "#87afaf"))))
 '(org-level-4 ((((class color) (min-colors 16777215)) (:foreground "#FABD2F")) (((class color) (min-colors 255)) (:foreground "#ffaf00"))))
 '(org-level-5 ((((class color) (min-colors 16777215)) (:foreground "#427B58")) (((class color) (min-colors 255)) (:foreground "#5f8787"))))
 '(org-level-6 ((((class color) (min-colors 16777215)) (:foreground "#B8BB26")) (((class color) (min-colors 255)) (:foreground "#afaf00"))))
 '(org-level-7 ((((class color) (min-colors 16777215)) (:foreground "#FB4933")) (((class color) (min-colors 255)) (:foreground "#d75f5f"))))
 '(org-level-8 ((((class color) (min-colors 16777215)) (:foreground "#83A598")) (((class color) (min-colors 255)) (:foreground "#87afaf"))))
 '(org-link ((t (:foreground "royal blue" :underline t))))
 '(org-meta-line ((t (:inherit (font-lock-comment-face fixed-pitch)))))
 '(org-property-value ((t (:inherit fixed-pitch))) t)
 '(org-special-keyword ((t (:inherit (font-lock-comment-face fixed-pitch)))))
 '(org-tag ((t (:inherit (shadow fixed-pitch) :weight bold :height 0.8))))
 '(org-verbatim ((t (:inherit (shadow fixed-pitch)))))
 '(variable-pitch ((t (:weight light :height 180 :family "Source Sans Pro")))))
```


## Setting up the package system {#setting-up-the-package-system}

I use the [wonderful `use-package` package](https://www.masteringemacs.org/article/spotlight-use-package-a-declarative-configuration-tool). As this is not bundled yet with Emacs, the first thing we do is install it by hand. All other packages are then declaratively installed and configured with `use-package`. This makes it possible to fully bootstrap Emacs using only this config file, everything else is downloaded, installed and configured automatically.

First, we declare the package repositories to use.

```emacs-lisp
(setq package-archives '(("gnu"       . "https://elpa.gnu.org/packages/")
                         ("marmalade" . "https://marmalade-repo.org/packages/")
                         ("melpa"     . "https://melpa.org/packages/")
                         ;;("org"       . "http://orgmode.org/elpa/")
                         ))
```

Then we initialize the package system, refresh the list of packages and install `use-package` if needed.

```emacs-lisp
(package-initialize)

(when (not package-archive-contents)
  (package-refresh-contents))

(when (not (package-installed-p 'use-package))
  (package-install 'use-package))
```

We set some configuration for `use-package`.

```emacs-lisp
(require 'use-package)
(setq use-package-always-ensure t)
(setq use-package-verbose t)
```

This variable tells Emacs to prefer the `.el` file if it's newer, even if there is a corresponding `.elc` file. Also, use `auto-compile` to autocompile files as needed.

```emacs-lisp
(setq load-prefer-newer t)
(use-package auto-compile
  :config (auto-compile-on-load-mode))
```

Set the load path to the directories from where I sometimes load things outside the package system. For now I am loading `org-mode` from a checkout of its git repository, so I load all its packages and the contrib packages from there.

```emacs-lisp
(add-to-list 'load-path "~/.emacs.d/lisp/org-mode/lisp")
(add-to-list 'load-path "~/.emacs.d/lisp/org-mode/contrib/lisp")
```

Before, I used to manually install the `org-plus-contrib` package. The code below is disabled for now, but kept here for reference.

```emacs-lisp
(when (not (package-installed-p 'org-plus-contrib))
  (package-install 'org-plus-contrib))
```

Load `org` right away, to avoid any interference with the version of `org` included with Emacs.

```emacs-lisp
(require 'org)
```


## Settings {#settings}


### Proxy settings {#proxy-settings}

These are two short functions I wrote to be able to set/unset proxy settings within Emacs. I haven't bothered to improve or automate this, as I pretty much only need it to be able to install packages sometimes when I'm at work. For now I just call them manually with `M-x set/unset-proxy` when I need to.

```emacs-lisp
(defun set-proxy ()
  (interactive)
  (setq url-proxy-services '(("http" . "proxy.corproot.net:8079")
                             ("https" . "proxy.corproot.net:8079"))))
(defun unset-proxy ()
  (interactive)
  (setq url-proxy-services nil))
```


### Miscellaneous settings {#miscellaneous-settings}

-   This is probably one of my oldest settings - I remember adding it around 1993 when I started learning Emacs, and it has been in my config ever since. When `time-stamp` is run before every save, the string `Time-stamp: <>` in the first 8 lines of the file will be updated with the current timestamp.

    ```emacs-lisp
    (add-hook 'before-save-hook 'time-stamp)
    ```

-   When at the beginning of the line, make `Ctrl-K` remove the whole line, instead of just emptying it.

    ```emacs-lisp
    (setq kill-whole-line t)
    ```

-   Paste text where the cursor is, not where the mouse is.

    ```emacs-lisp
    (setq mouse-yank-at-point t)
    ```

-   Make completion case-insensitive.

    ```emacs-lisp
    (setq completion-ignore-case t)
    (setq read-file-name-completion-ignore-case t)
    ```

-   Show line numbers (disable for now because it causes performance issues in very large buffers).

    ```emacs-lisp
    ;; (global-linum-mode)
    ```

-   Highlight trailing whitespace in red, so it's easily visible

    ```emacs-lisp
    (setq-default show-trailing-whitespace t)
    ```

-   Highlight matching parenthesis

    ```emacs-lisp
    (show-paren-mode 1)
    ```

-   Don't use hard tabs

    ```emacs-lisp
    (setq-default indent-tabs-mode nil)
    ```

-   Emacs can automatically create backup files. This tells Emacs to [put all backups in ~/.emacs.d/backups](http://www.gnu.org/software/emacs/manual/html_node/elisp/Backup-Files.html).

    ```emacs-lisp
    (setq backup-directory-alist `(("." . ,(concat user-emacs-directory "backups"))))
    ```

-   [WinnerMode](http://emacswiki.org/emacs/WinnerMode) makes it possible to cycle and undo window configuration changes (i.e. arrangement of panels, etc.)

    ```emacs-lisp
    (when (fboundp 'winner-mode) (winner-mode 1))
    ```

-   Add "unfill" commands to parallel the "fill" ones.

    ```emacs-lisp
    (use-package unfill)
    ```

-   Save the place of the cursor in each file, and restore it upon opening it again.

    ```emacs-lisp
    (use-package saveplace
      :config
      (setq-default save-place t)
      (setq save-place-file (concat user-emacs-directory "places")))
    ```

-   Provide mode-specific "bookmarks" - press `M-i` and you will be presented with a list of elements to which you can navigate - they can be headers in org-mode, function names in emacs-lisp, etc.

    ```emacs-lisp
    (use-package imenu-anywhere
      :config
      (global-set-key (kbd "M-i") 'ido-imenu-anywhere))
    ```

-   Smooth scrolling (line by line) instead of jumping by half-screens.

    ```emacs-lisp
    (use-package smooth-scrolling
      :config
      (smooth-scrolling-mode 1))
    ```

-   Delete trailing whitespace before saving a file.

    ```emacs-lisp
    (add-hook 'before-save-hook 'delete-trailing-whitespace)
    ```


## Keybindings {#keybindings}


### Miscellaneous keybindings {#miscellaneous-keybindings}

-   `M-g` interactively asks for a line number and jump to it (`goto-line)`.

    ```emacs-lisp
    (global-set-key [(meta g)] 'goto-line)
    ```

-   `` M-` `` focuses the next frame, if multiple ones are active (emulate the Mac "next app window" keybinding)

    ```emacs-lisp
    (global-set-key [(meta \`)] 'other-frame)
    ```

-   Interactive search key bindings - make regex search the default. By default, `C-s` runs `isearch-forward`, so this swaps the bindings.

    ```emacs-lisp
    (global-set-key (kbd "C-s") 'isearch-forward-regexp)
    (global-set-key (kbd "C-r") 'isearch-backward-regexp)
    (global-set-key (kbd "C-M-s") 'isearch-forward)
    (global-set-key (kbd "C-M-r") 'isearch-backward)
    ```

-   Key binding to use "[hippie expand](http://www.emacswiki.org/emacs/HippieExpand)" for text autocompletion

    ```emacs-lisp
    (global-set-key (kbd "M-/") 'hippie-expand)
    ```


### Emulating vi's `%` key {#emulating-vi-s-key}

One of the few things I missed in Emacs from vi was the `%` key, which jumps to the parenthesis, bracket or brace which matches the one below the cursor. This function implements the functionality. Inspired by <http://www.emacswiki.org/emacs/NavigatingParentheses>, but modified to use `smartparens` instead of the default commands, and to work on brackets and braces.

```emacs-lisp
(defun goto-match-paren (arg)
  "Go to the matching paren/bracket, otherwise (or if ARG is not nil) insert %.
  vi style of % jumping to matching brace."
  (interactive "p")
  (if (not (memq last-command '(set-mark
                                cua-set-mark
                                goto-match-paren
                                down-list
                                up-list
                                end-of-defun
                                beginning-of-defun
                                backward-sexp
                                forward-sexp
                                backward-up-list
                                forward-paragraph
                                backward-paragraph
                                end-of-buffer
                                beginning-of-buffer
                                backward-word
                                forward-word
                                mwheel-scroll
                                backward-word
                                forward-word
                                mouse-start-secondary
                                mouse-yank-secondary
                                mouse-secondary-save-then-kill
                                move-end-of-line
                                move-beginning-of-line
                                backward-char
                                forward-char
                                scroll-up
                                scroll-down
                                scroll-left
                                scroll-right
                                mouse-set-point
                                next-buffer
                                previous-buffer
                                previous-line
                                next-line
                                )))
      (self-insert-command (or arg 1))
    (cond ((looking-at "\\s\(") (sp-forward-sexp) (backward-char 1))
          ((looking-at "\\s\)") (forward-char 1) (sp-backward-sexp))
          (t (self-insert-command (or arg 1))))))
```

We bind this function to the `%` key.

```emacs-lisp
(global-set-key (kbd "%") 'goto-match-paren)
```


## Org mode {#org-mode}

I have started using [org-mode](http://orgmode.org/) to writing, coding, presentations and more, thanks to the hearty recommendations and information from [Nick](http://www.cmdln.org/) and many others. I am duly impressed. I have been a fan of the idea of [literate programming](https://en.wikipedia.org/wiki/Literate_programming) for many years, and I have tried other tools before (most notably [noweb](https://www.cs.tufts.edu/~nr/noweb/), which I used during grad school for many of my homeworks and projects), but org-mode is the first tool I have encountered which seems to make it practical. Here are some of the resources I have found useful in learning it:

-   Howard Abrams' [Introduction to Literate Programming](http://www.howardism.org/Technical/Emacs/literate-programming-tutorial.html), which got me jumpstarted into writing code documented with org-mode.
-   Nick Anderson's [Level up your notes with Org](https://github.com/nickanderson/Level-up-your-notes-with-Org), which contains many useful tips and configuration tricks.
-   Sacha Chua's [Some tips for learning Org Mode for Emacs](http://sachachua.com/blog/2014/01/tips-learning-org-mode-emacs/), her [Emacs configuration](http://pages.sachachua.com/.emacs.d/Sacha.html) and many of her [other articles](http://sachachua.com/blog/category/emacs/).
-   Rainer König's [OrgMode Tutorial](https://www.youtube.com/playlist?list=PLVtKhBrRV_ZkPnBtt_TD1Cs9PJlU0IIdE) video series.

This is the newest and most-in-flux section of my Emacs config, since I'm still learning org-mode myself.

I use `use-package` to load the `org` package, and put all its Configuration inside the `:config` section (`<<org-mode-config>>` is replaced with all the org-related configuration blocks below).

```emacs-lisp
(use-package org
  :ensure nil
  :load-path "~/.emacs.d/lisp/org-mode/lisp"
  :config
  <<org-mode-config>>)
```


### Keybindings {#keybindings}

Set up `C-c l` to store a link to the current org object, in counterpart to the default `C-c C-l` to insert a link.

```emacs-lisp
(define-key global-map "\C-cl" 'org-store-link)
```

Set up `C-c a` to call up agenda mode.

```emacs-lisp
(define-key global-map "\C-ca" 'org-agenda)
```

The default keybinding for `org-mark-element` is `M-h`, which in macOS hides the current application, so I bind it to `A-h`.

```emacs-lisp
(define-key global-map (kbd "A-h") 'org-mark-element)
```

Load `org-tempo` to enable snippets such as `<s<TAB>` to insert a source block.

```emacs-lisp
(require 'org-tempo)
```


### General org-mode configuration {#general-org-mode-configuration}

Set `org-directory` to a directory inside my Dropbox so that my main files get synchronized automatically.

```emacs-lisp
(setq org-directory "~/Dropbox/org")
```

Automatically log done times in todo items (I haven't used this much yet).

```emacs-lisp
(setq org-log-done t)
```

Keep the indentation well structured by. OMG this is a must have. Makes it feel less like editing a big text file and more like a purpose built editor for org mode that forces the indentation. Thanks [Nick](https://github.com/nickanderson/Level-up-your-notes-with-Org/blob/master/Level-up-your-notes-with-Org.org#automatic-visual-indention) for the tip!

```emacs-lisp
(setq org-startup-indented t)
```


### Building presentations with org-mode {#building-presentations-with-org-mode}

[org-reveal](https://github.com/yjwen/org-reveal) is an awesome package for building presentations with org-mode.

```emacs-lisp
;; Set this to nil because a bug in ox-reveal otherwise breaks org-structure-template-alist
(setq org-reveal-note-key-char nil)
(use-package ox-reveal
  :config
  (setq org-reveal-root "file:///Users/taazadi1/Dropbox/org/reveal.js")
  (use-package htmlize))
```


### Various exporters {#various-exporters}

One of the big strengths of org-mode is the ability to export a document in many different formats. Here I load some of the exporters I have found useful.

-   Markdown

    ```emacs-lisp
    (require 'ox-md)
    ```

-   [Jira markup](https://github.com/stig/ox-jira.el). I also load `org-jira`, which provides a full interface to Jira through org-mode.

    ```emacs-lisp
    (use-package ox-jira)
    (use-package org-jira
      :config
      ;; (setq jiralib-url "https://tracker.mender.io:443")
      (setq jiralib-url "https://jira.swisscom.com")
      (setq org-jira-working-dir "~/.org-jira"))
    ```

-   Confluence markup. This is included in org's contrib, so we just load it with `require` instead of `use-package`.

    ```emacs-lisp
    (require 'ox-confluence)
    ```

-   AsciiDoc

    ```emacs-lisp
    (use-package ox-asciidoc)
    ```

-   TexInfo. I have found that the best way to produce a PDF from an org file is to export it to a `.texi` file, and then use `texi2pdf` to produce the PDF.

    ```emacs-lisp
    (require 'ox-texinfo)
    ```


### Keeping a Journal {#keeping-a-journal}

I use [750words](http://750words.com/) for my personal Journal, and I usually write my entries locally using Scrivener. I have been playing with `org-journal` for this, but I am not fully convinced yet.

```emacs-lisp
(use-package org-journal
  :config
  (setq org-journal-dir "~/Documents/logbook"))
```


### Literate programming using org-babel {#literate-programming-using-org-babel}

Org-mode is the first literate programming tool that seems practical and useful, since it's easy to edit, execute and document code from within the same tool (Emacs) using all of its existing capabilities (i.e. each code block can be edited in its native Emacs mode, taking full advantage of indentation, completion, etc.)

Plain literate programming is built-in, but the `ob-*` packages provide the ability to execute code in different languages, beyond those included with org-mode.

```emacs-lisp
(use-package ob-cfengine3)
(require 'ob-ruby)
(require 'ob-latex)
(require 'ob-plantuml)
(setq org-plantuml-jar-path
      (expand-file-name "/usr/local/Cellar/plantuml/1.2017.18/libexec/plantuml.jar"))
(require 'ob-python)
(require 'ob-shell)
(require 'ob-calc)
(require 'ob-elvish)
```

`inf-ruby` makes `ob-ruby` more powerful by providing a persistent Ruby REPL.

```emacs-lisp
(use-package inf-ruby)
```

This is potentially dangerous: it suppresses the query before executing code from within org-mode. I use it because I am very careful and only press `C-c C-c` on blocks I absolutely understand.

```emacs-lisp
(setq org-confirm-babel-evaluate nil)
```

This makes it so that code within `src` blocks is fontified according to their corresponding Emacs mode, making the file much more readable.

```emacs-lisp
(setq org-src-fontify-natively t)
```

In principle this makes it so that indentation in `src` blocks works as in their native mode, but in my experience it does not always work reliably. For full proper indentation, always edit the code in a native buffer by pressing `C-c '`.

```emacs-lisp
(setq org-src-tab-acts-natively t)
```

Automatically show inline images, useful when executing code that produces them, such as PlantUML or Graphviz.

```emacs-lisp
(add-hook 'org-babel-after-execute-hook 'org-redisplay-inline-images)
```

This little snippet has revolutionized my literate programming workflow. It automatically runs `org-babel-tangle` upon saving any org-mode buffer, which means the resulting files will be automatically kept up to date.

```emacs-lisp
(add-hook 'org-mode-hook
          (lambda () (add-hook 'after-save-hook 'org-babel-tangle
                               'run-at-end 'only-in-org-mode)))
```


### Beautifying org-mode {#beautifying-org-mode}

These settings make org-mode much more readable by using different fonts for headings, hiding some of the markup, etc. This was taken originally from <http://www.howardism.org/Technical/Emacs/orgmode-wordprocessor.html> and then tweaked by me.

```emacs-lisp
(setq org-hide-emphasis-markers t)
(font-lock-add-keywords 'org-mode
                        '(("^ *\\([-]\\) "
                           (0 (prog1 () (compose-region (match-beginning 1) (match-end 1) "•"))))))
(use-package org-bullets
  :config
  (add-hook 'org-mode-hook (lambda () (org-bullets-mode 1))))
(let* ((variable-tuple
        (cond ((x-list-fonts "Source Sans Pro") '(:font "Source Sans Pro"))
              ((x-list-fonts "Lucida Grande")   '(:font "Lucida Grande"))
              ((x-list-fonts "Verdana")         '(:font "Verdana"))
              ((x-family-fonts "Sans Serif")    '(:family "Sans Serif"))
              (nil (warn "Cannot find a Sans Serif Font.  Install Source Sans Pro."))))
       (base-font-color     (face-foreground 'default nil 'default))
       (headline           `(:inherit default :weight bold :foreground ,base-font-color)))

  (custom-theme-set-faces
   'user
   `(org-level-8 ((t (,@headline ,@variable-tuple))))
   `(org-level-7 ((t (,@headline ,@variable-tuple))))
   `(org-level-6 ((t (,@headline ,@variable-tuple))))
   `(org-level-5 ((t (,@headline ,@variable-tuple))))
   `(org-level-4 ((t (,@headline ,@variable-tuple :height 1.1))))
   `(org-level-3 ((t (,@headline ,@variable-tuple :height 1.25))))
   `(org-level-2 ((t (,@headline ,@variable-tuple :height 1.5))))
   `(org-level-1 ((t (,@headline ,@variable-tuple :height 1.75))))
   `(org-document-title ((t (,@headline ,@variable-tuple :height 2.0 :underline nil))))))
```

I am experimenting with using proportional fonts in org-mode for the text, while keeping fixed-width fonts for blocks, so that source code, tables, etc. are shown correctly. I am currently playing with these settings, which include:

-   Setting up `visual-line-mode` and making all my paragraphs one single line, so that the lines wrap around nicely in the window according to their proportional-font size, instead of at a fixed character count, which does not work so nicely when characters have varying widths.
-   Setting up the `variable-pitch` face (I only learned of its existence now while figuring this out) to the proportional font I like to use. I'm currently using [Source Sans Pro](https://en.wikipedia.org/wiki/Source_Sans_Pro). Another favorite is [Avenir Next](https://en.wikipedia.org/wiki/Avenir_(typeface)).
-   Setting up the `fixed-pitch` face to be the same as my usual `default` face. My current one is [Inconsolata](https://en.wikipedia.org/wiki/Inconsolata).
-   Configuring the corresponding org-mode faces for blocks, verbatim code, and maybe a couple of other things.
-   Setting up a hook that automatically enables `visual-line-mode` and `variable-pitch-mode` when entering org-mode.

```emacs-lisp
(add-hook 'org-mode-hook 'visual-line-mode)
(add-hook 'org-mode-hook 'variable-pitch-mode)
```


### Auto-generated table of contents {#auto-generated-table-of-contents}

The `toc-org` package allows us to insert a table of contents in headings marked with `:TOC:`. This is useful for org files that are to be viewed directly on GitHub, which renders org files correctly, but does not generate a table of contents at the top. For an example, see [this file on GitHub](https://github.com/zzamboni/dot-emacs/blob/master/init.org).

Note that this breaks HTML export by default, as the links generated by `toc-org` cannot be parsed properly by the html exporter. The [workaround](https://github.com/snosov1/toc-org/issues/35#issuecomment-275096511) is to use `:TOC:noexport:` as the marker, which removed the generated TOC from the export, but still allows `ox-html` to insert its own TOC at the top.

```emacs-lisp
(use-package toc-org
  :config
  (add-hook 'org-mode-hook 'toc-org-enable))
```


### Grabbing links from different Mac applications {#grabbing-links-from-different-mac-applications}

`org-mac-link` (included in contrib) implements the ability to grab links from different Mac apps and insert them in the file. Bind `C-c g` to call `org-mac-grab-link` to choose an application and insert a link.

```emacs-lisp
(require 'org-mac-link)
(add-hook 'org-mode-hook (lambda ()
                           (define-key org-mode-map (kbd "C-c g") 'org-mac-grab-link)))
```


### Reformatting an org buffer {#reformatting-an-org-buffer}

I picked up this little gem in the org mailing list. A function that reformats the current buffer by regenerating the text from its internal parsed representation. Quite amazing.

```emacs-lisp
(defun org-reformat-buffer ()
  (interactive)
  (when (y-or-n-p "Really format current buffer? ")
    (let ((document (org-element-interpret-data (org-element-parse-buffer))))
      (erase-buffer)
      (insert document)
      (goto-char (point-min)))))
```


### Snippets and templates {#snippets-and-templates}

The [yankpad](https://github.com/Kungsgeten/yankpad) package makes it easy to store snippets that can be inserted at arbitrary points. Together with [yasnippet](http://joaotavora.github.io/yasnippet/) it becomes more powerful.

```emacs-lisp
(use-package yasnippet)
(use-package yankpad
  :init
  (setq yankpad-file "~/Dropbox/org/yankpad.org")
  :config
  (bind-key "<f7>" 'yankpad-map)
  (bind-key "<f12>" 'yankpad-expand)
  ;; If you want to expand snippets with hippie-expand
  (add-to-list 'hippie-expand-try-functions-list #'yankpad-expand))
```


## System-specific configuration {#system-specific-configuration}

Some settings maybe OS-specific, and this is where we set them. For now I only use Emacs on my Mac, so only the Mac section is filled out, but there are sections for Linux and Windows as well.

```emacs-lisp
(cond ((eq system-type 'darwin)
       <<Mac settings>>
       )
      ((eq system-type 'windows-nt)
       <<Windows settings>>
       )
      ((eq system-type 'gnu/linux)
       <<Linux settings>>
       ))
```


### Mac {#mac}

First, we set the key modifiers correctly to my preferences: Make Command (⌘) act as Meta, Option as Alt, right-Option as Super

<a id="org1fd3ac1"></a>
```emacs-lisp
(setq mac-command-modifier 'meta)
(setq mac-option-modifier 'alt)
(setq mac-right-option-modifier 'super)
```

We also make it possible to use the familiar `⌘-+` and `⌘--` to increase and decrease the font size. ⌘-= is also bound to "increase" because it's on the same key in an English keyboard.

<a id="org5b43fa3"></a>
```emacs-lisp
(global-set-key (kbd "M-+") 'text-scale-increase)
(global-set-key (kbd "M-=") 'text-scale-increase)
(global-set-key (kbd "M--") 'text-scale-decrease)
```

Somewhat surprisingly, there seems to be no "reset" function, so I define my own and bind it to `⌘-0`.

<a id="org06e5961"></a>
```emacs-lisp
(defun text-scale-reset ()
  (interactive)
  (text-scale-set 0))
(global-set-key (kbd "M-0") 'text-scale-reset)
```

We also use the `exec-path-from-shell` to make sure the path settings from the shell are loaded into Emacs (usually it starts up with the default system-wide path).

<a id="org0b6e57c"></a>
```emacs-lisp
(use-package exec-path-from-shell
  :config
  (exec-path-from-shell-initialize))
```


### Linux {#linux}

There are no Linux-specific settings for now.


### Windows {#windows}

There are no Windows-specific settings for now.


## Appearance, buffer/file management and theming {#appearance-buffer-file-management-and-theming}

Here we take care of all the visual, UX and desktop-management settings.

The `diminish` package makes it possible to remove clutter from the modeline. Here we just load it, it gets enabled for individual packages in their corresponding declarations.

```emacs-lisp
(use-package diminish)
```

I have been playing with different themes, and I have settled for now in `gruvbox`. Some of my other favorites are also here so I don't forget about them.

```emacs-lisp
;;(use-package solarized-theme)
;;(use-package darktooth-theme)
;;(use-package kaolin-themes)
(use-package gruvbox-theme)
(load-theme 'gruvbox)
```

Install [smart-mode-line](https://github.com/Malabarba/smart-mode-line) for modeline goodness.

```emacs-lisp
(use-package smart-mode-line
  :config
  (sml/setup))
```

Enable desktop-save mode, which saves the current buffer configuration on exit and reloads it on restart.

```emacs-lisp
(use-package desktop
  :config
  (desktop-save-mode 1))
```

The `uniquify` package makes it much easier to identify different open files with the same name by prepending/appending their directory or some other information to them. I configure it to add the directory name after the filename. `uniquify` is included in Emacs, so I specify `:ensure nil` so that `use-package` doesn't try to install it, and just loads and configures it.

```emacs-lisp
(use-package uniquify
  :ensure nil
  :config
  (setq uniquify-after-kill-buffer-p t)
  (setq uniquify-buffer-name-style 'post-forward)
  (setq uniquify-strip-common-suffix nil))
```

I like to highlight the current line and column. I'm still deciding between two approaches:

-   Using the built-in `global-hl-mode` to always highlight the current line, together with the `col-highlight` package, which highlights the column only after a defined interval has passed
-   Using the `crosshairs` package, which combines both but always highlights both the column and the line. It also has a "highlight crosshairs when idle" mode, but I prefer to have the current line always highlighted, I'm only undecided about the always-on column highlighting.

Sometimes I find the always-highlighted column to be distracting, but other times I find it useful. So I have both pieces of code here, I'm still deciding.

```emacs-lisp
(global-hl-line-mode 1)
(use-package col-highlight
  :config
  (col-highlight-toggle-when-idle)
  (col-highlight-set-interval 2))
;; (use-package crosshairs
;;   :config
;;   (crosshairs-mode))
```

I use [IDO mode](https://www.masteringemacs.org/article/introduction-to-ido-mode) to get better matching capabilities everywhere in Emacs.

```emacs-lisp
(use-package ido
  :config
  (ido-mode t)
  (ido-everywhere 1)
  (setq ido-use-virtual-buffers t)
  (setq ido-enable-flex-matching t)
  (setq ido-use-filename-at-point nil)
  (setq ido-auto-merge-work-directories-length -1))

(use-package ido-completing-read+
  :config
  (ido-ubiquitous-mode 1))
```

I also use `recentf` to keep a list of recently open buffers, and define a function to trigger recentf with IDO integration, using `C-x C-r` as the keybinding.

```emacs-lisp
(use-package recentf
  :init
  (defun ido-recentf-open ()
    "Use `ido-completing-read' to \\[find-file] a recent file"
    (interactive)
    (if (find-file (ido-completing-read "Find recent file: " recentf-list))
        (message "Opening file...")
      (message "Aborting")))
  :config
  (recentf-mode 1)
  (setq recentf-max-menu-items 50)
  (global-set-key (kbd "C-x C-r") 'ido-recentf-open))
```

The [ibuffer](http://martinowen.net/blog/2010/02/03/tips-for-emacs-ibuffer.html) package allows all sort of useful operations on the list of open buffers. I haven't customized it yet, but I have a keybinding to open it.

```emacs-lisp
(use-package ibuffer
  :config
  (global-set-key (kbd "C-x C-b") 'ibuffer))
```

The [smex](https://github.com/nonsequitur/smex) package is incredibly useful, adding IDO integration and some other very nice features to `M-x`, which make it easier to discover and use Emacs commands. Highly recommended.

```emacs-lisp
(use-package smex
  :bind (("M-x" . smex))
  :config (smex-initialize))
```

[midnight-mode](https://www.emacswiki.org/emacs/MidnightMode) purges buffers which haven't been displayed in 3 days. We configure the period so that the cleanup happens every 2 hours (7200 seconds).

```emacs-lisp
(use-package midnight
  :config
  (setq midnight-mode 't)
  (setq midnight-period 7200))
```

For distraction-free writing, I'm testing out `writeroom-mode`.

```emacs-lisp
(use-package writeroom-mode)
```

[NeoTree](https://github.com/jaypei/emacs-neotree) shows a navigation tree on a sidebar, and allows a number of operations on the files and directories. I'm not much of a fan of this type of interface in Emacs, but I have set it up to check it out.

```emacs-lisp
(use-package neotree
  :config
  (setq neo-theme (if (display-graphic-p) 'icons 'arrow))
  (setq neo-smart-open t)
  (setq projectile-switch-project-action 'neotree-projectile-action)
  (defun neotree-project-dir ()
    "Open NeoTree using the git root."
    (interactive)
    (let ((project-dir (projectile-project-root))
          (file-name (buffer-file-name)))
      (neotree-toggle)
      (if project-dir
          (if (neo-global--window-exists-p)
              (progn
                (neotree-dir project-dir)
                (neotree-find file-name)))
        (message "Could not find git project root."))))
  (global-set-key [f8] 'neotree-project-dir))
```

`wc-mode` allows counting characters and words, both on demand and continuously. It also allows setting up a word/character goal.

```emacs-lisp
(use-package wc-mode)
```

The `all-the-icons` package provides a number of useful icons.

```emacs-lisp
(use-package all-the-icons)
```


## Coding {#coding}

Coding is my main use for Emacs, so it's understandably the largest section in my Emacs configuration.


### General settings and modules {#general-settings-and-modules}

When enabled, `subword` allows navigating "sub words" individually in CamelCaseIdentifiers. For now I only enable it in `clojure-mode`.

```emacs-lisp
(use-package subword
  :config
  (add-hook 'clojure-mode-hook #'subword-mode))
```

With `aggressive-indent`, indentation is always kept up to date in the whole buffer. Sometimes it gets in the way, but in general it's nice and saves a lot of work, so I enable it for all programming modes.

```emacs-lisp
(use-package aggressive-indent
  :diminish aggressive-indent-mode
  :config
  (add-hook 'prog-mode-hook #'aggressive-indent-mode))
```

With `company-mode`, we get automatic completion - when there are completions available, a popup menu will appear when you stop typing for a moment, and you can either continue typing or accept the completion using the Enter key. I enable it globally.

```emacs-lisp
(use-package company
  :diminish company-mode
  :config
  (add-hook 'after-init-hook #'global-company-mode))
```

`projectile-mode` allows us to perform project-relative operations such as searches, navigation, etc.

```emacs-lisp
(use-package projectile
  :diminish projectile-mode
  :config
  (projectile-global-mode))
```

I find `iedit` absolutely indispensable when coding. In short: when you hit `Ctrl-:`, all occurrences of the symbol under the cursor (or the current selection) are highlighted, and any changes you make on one of them will be automatically applied to all others. It's great for renaming variables in code.

```emacs-lisp
(use-package iedit
  :config (set-face-background 'iedit-occurrence "Magenta"))
```

Turn on the online documentation mode for all programming modes (not all of them support it) and for the Clojure REPL `cider` mode.

```emacs-lisp
(use-package eldoc
  :config
  (add-hook 'prog-mode-hook #'turn-on-eldoc-mode)
  (add-hook 'cider-repl-mode-hook #'turn-on-eldoc-mode))
```

On-the-fly spell checking. I enable it for all text modes.

```emacs-lisp
(use-package flyspell
  :config
  (define-key flyspell-mouse-map [down-mouse-3] #'flyspell-correct-word)
  (define-key flyspell-mouse-map [mouse-3] #'undefined)
  (add-hook 'text-mode-hook   'flyspell-mode))
```


### Clojure and LISP coding {#clojure-and-lisp-coding}

I dabble in Clojure and Emacs LISP, and Emacs has some fantastic support for them. There's a number of packages and configuration related to this, so I have a whole section for it.

The centerpiece is of course `clojure-mode`. In addition to files ending in `.clj`, I bind it automatically to `.boot` files (both by extension and by [shebang line](https://github.com/boot-clj/boot/wiki/For-Emacs-Users)) and to the [Riemann](http://riemann.io/) config files.

```emacs-lisp
(use-package clojure-mode
  :mode "\\.clj.*$"
  :mode "riemann.config"
  :mode "\\.boot"
  :config
  (add-to-list 'magic-mode-alist '(".* boot" . clojure-mode)))
```

Enable some additional fontification for Clojure code.

```emacs-lisp
(use-package clojure-mode-extra-font-locking)
```

The `cider` package provides a fantastic REPL built into Emacs. We configure a few aspects, including pretty printing, fontification, history size and others.

```emacs-lisp
(use-package cider
  :config
  ;; nice pretty printing
  (setq cider-repl-use-pretty-printing nil)

  ;; nicer font lock in REPL
  (setq cider-repl-use-clojure-font-lock t)

  ;; result prefix for the REPL
  (setq cider-repl-result-prefix "; => ")

  ;; never ending REPL history
  (setq cider-repl-wrap-history t)

  ;; looong history
  (setq cider-repl-history-size 5000)

  ;; persistent history
  (setq cider-repl-history-file "~/.emacs.d/cider-history")

  ;; error buffer not popping up
  (setq cider-show-error-buffer nil)

  ;; go right to the REPL buffer when it's finished connecting
  (setq cider-repl-pop-to-buffer-on-connect t))
```

We use `clj-refactor` for supporting advanced code refactoring in Clojure.

```emacs-lisp
(use-package clj-refactor
  :config
  (defun my-clojure-mode-hook ()
    (clj-refactor-mode 1)
    (yas-minor-mode 1) ; for adding require/use/import statements
    ;; This choice of keybinding leaves cider-macroexpand-1 unbound
    (cljr-add-keybindings-with-prefix "C-c C-m"))
  (add-hook 'clojure-mode-hook #'my-clojure-mode-hook))
```

Make the [Clojure cheatsheet](https://clojure.org/api/cheatsheet) available within Emacs when coding in Clojure.

```emacs-lisp
(use-package helm)
(use-package clojure-cheatsheet
  :config
  (eval-after-load 'clojure-mode
    '(progn
       (define-key clojure-mode-map (kbd "C-c C-h") #'clojure-cheatsheet))))
```

When coding in LISP-like languages, `rainbow-delimiters` is a must-have - it marks each concentric pair of parenthesis with different colors, which makes it much easier to understand expressions and spot mistakes.

```emacs-lisp
(use-package rainbow-delimiters
  :config
  (add-hook 'prog-mode-hook #'rainbow-delimiters-mode)
  (add-hook 'cider-repl-mode-hook #'rainbow-delimiters-mode))
```

Another useful addition for LISP coding - `smartparens` enforces parenthesis to match, and adds a number of useful operations for manipulating parenthesized expressions.

```emacs-lisp
(use-package smartparens
  :diminish smartparens-mode
  :config
  (require 'smartparens-config)
  (setq sp-base-key-bindings 'paredit)
  (add-hook 'clojure-mode-hook #'smartparens-strict-mode)
  (add-hook 'emacs-lisp-mode-hook #'smartparens-strict-mode)
  (add-hook 'lisp-mode-hook #'smartparens-strict-mode)
  (add-hook 'cider-repl-mode-hook #'smartparens-strict-mode))
```

Map `M-(` to enclose the next expression, as in `paredit`. Prefix argument can be used to indicate how many expressions to enclose instead of just 1. E.g. `C-u 3 M-(` will enclose the next 3 sexps.

```emacs-lisp
(defun sp-enclose-next-sexp (num) (interactive "p") (insert-parentheses (or num 1)))
(add-hook 'smartparens-mode-hook #'sp-use-paredit-bindings)
(add-hook 'smartparens-mode-hook (lambda () (local-set-key (kbd "M-(") 'sp-enclose-next-sexp)))
```

Minor mode for highlighting the current sexp in LISP modes.

```emacs-lisp
(use-package hl-sexp
  :config
  (add-hook 'clojure-mode-hook #'hl-sexp-mode)
  (add-hook 'lisp-mode-hook #'hl-sexp-mode)
  (add-hook 'emacs-lisp-mode-hook #'hl-sexp-mode))
```

Trying out [lispy](https://github.com/abo-abo/lispy) for LISP code editing (disabled for now).

```emacs-lisp
(use-package lispy
  :config
  (defun enable-lispy-mode ()
    (lispy-mode 1))
  (add-hook 'clojure-mode-hook #'enable-lispy-mode)
  (add-hook 'emacs-lisp-mode-hook #'enable-lispy-mode)
  (add-hook 'common-lisp-mode-hook #'enable-lispy-mode)
  (add-hook 'scheme-mode-hook #'enable-lispy-mode)
  (add-hook 'lisp-mode-hook #'enable-lispy-mode))
```

I am sometimes trying out [parinfer](https://shaunlebron.github.io/parinfer/) (disabled for now).

```emacs-lisp
(use-package parinfer
  :ensure t
  :bind
  (("C-," . parinfer-toggle-mode))
  :init
  (progn
    (setq parinfer-extensions
          '(defaults       ; should be included.
             pretty-parens  ; different paren styles for different modes.
             ;;evil           ; If you use Evil.
             lispy          ; If you use Lispy. With this extension, you should install Lispy and do not enable lispy-mode directly.
             paredit        ; Introduce some paredit commands.
             smart-tab      ; C-b & C-f jump positions and smart shift with tab & S-tab.
             smart-yank))   ; Yank behavior depend on mode.
    (add-hook 'clojure-mode-hook #'parinfer-mode)
    (add-hook 'emacs-lisp-mode-hook #'parinfer-mode)
    (add-hook 'common-lisp-mode-hook #'parinfer-mode)
    (add-hook 'scheme-mode-hook #'parinfer-mode)
    (add-hook 'lisp-mode-hook #'parinfer-mode)))
```


### Other programming languages {#other-programming-languages}

Many other programming languages are well served by a single mode, without so much setup as Clojure/LISP.

-   [CFEngine](http://cfengine.com/) policy files.

    ```emacs-lisp
    (use-package cfengine
      :commands cfengine3-mode
      :mode ("\\.cf\\'" . cfengine3-mode))
    ```

-   [Perl](https://www.perl.org/).

    ```emacs-lisp
    (use-package cperl-mode
      :mode "\\.p[lm]\\'"
      :interpreter "perl"
      :config
      (setq cperl-hairy t))
    ```

-   [Fish shell](http://fishshell.com/).

    ```emacs-lisp
    (use-package fish-mode
      :mode "\\.fish\\'"
      :interpreter "fish")
    ```

-   [Lua](https://www.lua.org/), which I use for [Hammerspoon](http://zzamboni.org/tags/hammerspoon/) configuration.

    ```emacs-lisp
    (use-package lua-mode)
    ```

-   YAML, generally useful

    ```emacs-lisp
    (use-package yaml-mode)
    ```

-   AppleScript

    ```emacs-lisp
    (use-package applescript-mode)
    ```

-   Go

    ```emacs-lisp
    (use-package go-mode)
    ```

-   Check MELPA package definitions

    ```emacs-lisp
    (use-package package-lint)
    ```

-   [Elvish shell](http://elvish.io/)

    ```emacs-lisp
    (use-package elvish-mode)
    ```

-   [Racket](https://racket-lang.org/)

    ```emacs-lisp
    (use-package racket-mode)
    ```

-   [Nix](https://nixos.org/nix/) package files

    ```emacs-lisp
    (use-package nix-mode)
    ```


## Other tools {#other-tools}

-   git interface with some simple configuration I picked up somewhere

    ```emacs-lisp
    (use-package magit
      :config
      (defadvice magit-status (around magit-fullscreen activate)
        "Make magit-status run alone in a frame."
        (window-configuration-to-register :magit-fullscreen)
        ad-do-it
        (delete-other-windows))

      (defun magit-quit-session ()
        "Restore the previous window configuration and kill the magit buffer."
        (interactive)
        (kill-buffer)
        (jump-to-register :magit-fullscreen))

      (define-key magit-status-mode-map (kbd "q") 'magit-quit-session)
      (global-set-key (kbd "C-c C-g") 'magit-status))
    ```

-   Interface to use the [silver-searcher](https://geoff.greer.fm/ag/)

    ```emacs-lisp
    (use-package ag)
    ```

-   Publishing with [Hugo](https://gohugo.io/)

    ```emacs-lisp
    (use-package easy-hugo
      :config
      (setq easy-hugo-basedir "~/Personal/devel/zzamboni.org/zzamboni.org/")
      (setq easy-hugo-url "http://zzamboni.org/")
      (setq easy-hugo-previewtime "300")
      (define-key global-map (kbd "C-c C-e") 'easy-hugo))
    ```

-   Function to randomize the order of lines in a region, from <https://www.emacswiki.org/emacs/RandomizeBuffer>.

    ```emacs-lisp
    (defun my-randomize-region (beg end)
      "Randomize lines in region from BEG to END."
      (interactive "*r")
      (let ((lines (split-string
                    (delete-and-extract-region beg end) "\n")))
        (when (string-equal "" (car (last lines 1)))
          (setq lines (butlast lines 1)))
        (apply 'insert
               (mapcar 'cdr
                       (sort (mapcar (lambda (x) (cons (random) (concat x "\n"))) lines)
                             (lambda (a b) (< (car a) (car b))))))))
    ```

-   [auto-insert mode](https://www.gnu.org/software/emacs/manual/html_node/autotype/Autoinserting.html) for automatically inserting user-defined templates for certain file types. It's included with Emacs, so I just configure its directory to one inside my Dropbox, and set the hook to run it automatically when opening a file.

    ```emacs-lisp
    (setq auto-insert-directory "~/Dropbox/emacs-auto-insert")
    (add-hook 'find-file-hook 'auto-insert)
    ```


## General text editing {#general-text-editing}

In addition to coding, I configure some modes that can be used for text editing.

-   [AsciiDoc](http://asciidoctor.org/docs/user-manual/), which I use for [my book](http://cf-learn.info/) and some other text.

    ```emacs-lisp
    (use-package adoc-mode
      :mode "\\.asciidoc\\'")
    ```

-   [Markdown](https://daringfireball.net/projects/markdown/syntax), generally useful.

    ```emacs-lisp
    (use-package markdown-mode)
    ```

-   When [typopunct](https://www.emacswiki.org/emacs/TypographicalPunctuationMarks) is enabled (needs to be enable by hand in my config), automatically inserts “pretty” quotes of the appropriate type.

    ```emacs-lisp
    (use-package typopunct
      :config
      (typopunct-change-language 'english t))
    ```


## Cheatsheet {#cheatsheet}

How to do different things, not necessarily used in my Emacs config but useful sometimes.

This is how we get a global header property in org-mode

```emacs-lisp
(alist-get :tangle
           (org-babel-parse-header-arguments
            (org-entry-get-with-inheritance "header-args")))
```
